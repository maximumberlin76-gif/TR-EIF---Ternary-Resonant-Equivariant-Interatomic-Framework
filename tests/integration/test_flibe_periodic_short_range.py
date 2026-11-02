"""Independent periodic FLiBe short-range energy and force qualification."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal, localcontext
from itertools import product
from math import factorial, floor, fsum, sqrt
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import EnergyState, ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_short_range import (
    SHORT_RANGE_FUNCTIONAL_ID,
    FLiBePeriodicShortRangeModel,
    FLiBePeriodicShortRangeResult,
)
from tr_eif.flibe.registered_pair_coefficients import (
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.5, 0.4, 0.5),
    (3.2, 0.8, 0.7),
    (2.0, 3.3, 1.1),
    (0.8, 2.1, 3.5),
    (3.8, 2.9, 3.0),
    (1.4, 4.0, 4.6),
    (4.5, 1.6, 5.0),
)
CELL = (
    (14.0, 0.0, 0.0),
    (1.0, 13.0, 0.0),
    (0.5, 0.8, 15.0),
)
CHARGES = {"Li": 1, "Be": 2, "F": -1}

# Independent transcription of the primary-source pair parameters.
# Entries are (A, alpha, C6, C8, b6, b8) in atomic units.
PAIR_TABLE = {
    ("Li", "Li"): (195.91, 4.252, 0.0, 0.0, 1.0, 1.0),
    ("Li", "Be"): (0.0, 1.0, 0.0, 0.0, 1.0, 1.0),
    ("Li", "F"): (20.42, 2.052, 0.0, 0.0, 1.0, 1.0),
    ("Be", "Be"): (106.16, 3.944, 0.0, 0.0, 1.0, 1.0),
    ("Be", "F"): (41.72, 2.254, 0.0, 0.0, 1.0, 1.0),
    ("F", "F"): (181.84, 2.267, 15.0, 150.0, 1.9, 1.9),
}
ENERGY_TOL = 2.0e-10
FORCE_TOL = 2.0e-8
DIFFERENCE_STEP = 1.0e-5


def _parameters():
    return load_flibe_registered_pair_parameters(SOURCE)


def _model(shell=0, *, parameters=None, coordinate_unit_to_bohr=1.0):
    return FLiBePeriodicShortRangeModel(
        model_id="FLIBE-SOURCE-SHORT-RANGE-FIXTURE",
        parameters=_parameters() if parameters is None else parameters,
        coordinate_unit_to_bohr=coordinate_unit_to_bohr,
        image_shell=shell,
    )


def _configuration(species=SPECIES, positions=POSITIONS, cell=CELL,
                   periodic=(True, True, True)):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(value) for value in row) for row in positions),
        cell=None if cell is None else tuple(tuple(float(value) for value in row) for row in cell),
        periodic=periodic,
    ))


def _cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def _dot(a, b):
    return fsum(x*y for x, y in zip(a, b, strict=True))


def _central_displacement(first, second, cell):
    """Independently reduce pair separation using the reciprocal cell geometry."""
    difference = tuple(first[k] - second[k] for k in range(3))
    normals = (_cross(cell[1], cell[2]), _cross(cell[2], cell[0]), _cross(cell[0], cell[1]))
    determinant = _dot(cell[0], normals[0])
    integer_shifts = tuple(floor(_dot(difference, vector)/determinant + 0.5) for vector in normals)
    return tuple(difference[axis] - sum(integer_shifts[k]*cell[k][axis] for k in range(3))
                 for axis in range(3))


def _independent_radial(radius, coefficients):
    """Calculate the Born and Tang-Toennies potential and its derivative in Decimal."""
    with localcontext() as context:
        context.prec = 55
        d = lambda value: Decimal(str(value))
        r = d(radius)
        amplitude, alpha, c6, c8, b6, b8 = (d(value) for value in coefficients)
        repulsion = amplitude * (-alpha * r).exp()
        energy = repulsion
        derivative = -alpha * repulsion
        for power, dispersion, beta in ((6, c6, b6), (8, c8, b8)):
            if dispersion == 0:
                continue
            z = beta * r
            tail = (-z).exp()
            polynomial = sum((z**k / Decimal(factorial(k)) for k in range(power+1)), Decimal(0))
            damping = 1 - tail*polynomial
            damping_derivative = beta * tail * z**power / Decimal(factorial(power))
            energy -= dispersion * damping / r**power
            derivative -= dispersion * (
                damping_derivative / r**power - Decimal(power)*damping / r**(power+1)
            )
        return float(energy), float(derivative)


def _independent_periodic_sum(configuration, shell):
    """Sum unordered pair images and half-weighted self images independently."""
    positions = configuration.configuration.positions
    species = configuration.configuration.species
    cell = configuration.configuration.cell
    labels = {frozenset(names): values for names, values in PAIR_TABLE.items()}
    atomic_energy = [0.0] * len(species)
    force_components = [[0.0, 0.0, 0.0] for _ in species]
    cross_energy_terms = []
    self_energy_terms = []
    for index in product(range(-shell, shell+1), repeat=3):
        translation = tuple(sum(index[k] * cell[k][axis] for k in range(3)) for axis in range(3))
        if index != (0, 0, 0):
            r = sqrt(_dot(translation, translation))
            for i, label in enumerate(species):
                value, _ = _independent_radial(r, labels[frozenset((label,))])
                contribution = 0.5 * value
                self_energy_terms.append(contribution)
                atomic_energy[i] += contribution
        for i in range(len(species)):
            for j in range(i+1, len(species)):
                delta0 = _central_displacement(positions[i], positions[j], cell)
                delta = tuple(delta0[k] + translation[k] for k in range(3))
                r = sqrt(_dot(delta, delta))
                value, derivative = _independent_radial(r, labels[frozenset((species[i],species[j]))])
                cross_energy_terms.append(value)
                atomic_energy[i] += 0.5 * value
                atomic_energy[j] += 0.5 * value
                for axis in range(3):
                    force = -derivative * delta[axis] / r
                    force_components[i][axis] += force
                    force_components[j][axis] -= force
    return (
        fsum(cross_energy_terms),
        fsum(self_energy_terms),
        tuple(atomic_energy),
        tuple(tuple(row) for row in force_components),
    )


def _assert_forces(actual, reference, absolute=FORCE_TOL):
    assert len(actual) == len(reference)
    for row, expected in zip(actual, reference, strict=True):
        assert row == pytest.approx(expected, rel=0.0, abs=absolute)


def _shift_atom(configuration, atom, shift):
    positions = [list(p) for p in configuration.configuration.positions]
    positions[atom] = [positions[atom][axis] + shift[axis] for axis in range(3)]
    return _configuration(configuration.configuration.species, positions,
                          configuration.configuration.cell, configuration.configuration.periodic)


def test_source_registration_and_parameter_boundaries():
    source = _parameters()
    assert source.source_doi == SOURCE_DOI == "10.1016/j.molliq.2019.112165"
    assert source.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert len(source.pair_coefficients) == 6
    assert all(pair.provenance is ParameterProvenance.PRIMARY_SOURCE for pair in source.pair_coefficients)
    assert tuple((pair.species_a.value, pair.species_b.value) for pair in source.pair_coefficients) == tuple(PAIR_TABLE)
    for pair in source.pair_coefficients:
        assert (pair.born_amplitude_hartree, pair.born_decay_inverse_bohr,
                pair.c6_hartree_bohr6, pair.c8_hartree_bohr8,
                pair.b6_inverse_bohr, pair.b8_inverse_bohr) == PAIR_TABLE[(pair.species_a.value, pair.species_b.value)]


def test_li_f_repulsive_born_energy_and_analytical_force_without_coulomb():
    distance = 4.0
    configuration = _configuration(("Li", "F"), ((0.,0.,0.), (distance,0.,0.)))
    result = _model().evaluate(configuration)
    energy, derivative = _independent_radial(distance, PAIR_TABLE[("Li", "F")])
    assert result.energy.total_energy == pytest.approx(energy, abs=ENERGY_TOL)
    assert result.energy.atomic_energies == pytest.approx((energy/2, energy/2), abs=ENERGY_TOL)
    assert result.forces.forces[0] == pytest.approx((derivative, 0., 0.), abs=FORCE_TOL)
    assert result.forces.forces[1] == pytest.approx((-derivative, 0., 0.), abs=FORCE_TOL)
    assert result.cross_atom_image_terms == 1
    assert result.self_atom_image_terms == 0
    assert result.source_doi == SOURCE_DOI


@pytest.mark.parametrize("shell", (0, 1, 2))
def test_independent_periodic_energy_components_and_force_gradients(shell):
    configuration = _configuration()
    result = _model(shell).evaluate(configuration)
    cross, self_image, atomic_energy, forces = _independent_periodic_sum(configuration, shell)
    assert result.cross_atom_energy_hartree == pytest.approx(cross, rel=0.0, abs=ENERGY_TOL)
    assert result.self_image_energy_hartree == pytest.approx(self_image, rel=0.0, abs=ENERGY_TOL)
    assert result.energy.total_energy == pytest.approx(cross+self_image, rel=0.0, abs=ENERGY_TOL)
    assert result.energy.atomic_energies == pytest.approx(atomic_energy, rel=0.0, abs=ENERGY_TOL)
    _assert_forces(result.forces.forces, forces)
    assert result.cross_atom_image_terms == 21 * (2*shell+1)**3
    assert result.self_atom_image_terms == 7 * ((2*shell+1)**3 - 1)
    assert result.functional_id == SHORT_RANGE_FUNCTIONAL_ID


def test_zero_shell_agrees_with_finite_cluster_after_removing_coulomb():
    configuration = _configuration()
    finite = _parameters().build_finite_cluster_model(model_id="FINITE-SOURCE", coordinate_unit_to_bohr=1.0)
    nonperiodic = _configuration(cell=None, periodic=(False,False,False))
    full = finite.evaluate(nonperiodic)
    short = _model(0).evaluate(configuration)
    coulomb_energy = 0.0
    coulomb_forces = [[0.,0.,0.] for _ in SPECIES]
    for i in range(7):
        for j in range(i+1,7):
            delta = tuple(POSITIONS[i][axis]-POSITIONS[j][axis] for axis in range(3))
            r2 = _dot(delta,delta)
            r = sqrt(r2)
            charge = CHARGES[SPECIES[i]]*CHARGES[SPECIES[j]]
            coulomb_energy += charge/r
            for axis in range(3):
                force = charge*delta[axis]/(r2*r)
                coulomb_forces[i][axis] += force
                coulomb_forces[j][axis] -= force
    assert short.energy.total_energy == pytest.approx(full.energy.total_energy - coulomb_energy, abs=ENERGY_TOL)
    expected = tuple(tuple(full.forces.forces[i][axis] - coulomb_forces[i][axis] for axis in range(3)) for i in range(7))
    _assert_forces(short.forces.forces, expected)


def test_unit_conversion_preserves_energy_and_scales_cartesian_forces():
    original = _model(1).evaluate(_configuration())
    scaled = _model(1, coordinate_unit_to_bohr=0.5).evaluate(_configuration(
        positions=tuple(tuple(2*x for x in p) for p in POSITIONS),
        cell=tuple(tuple(2*x for x in p) for p in CELL),
    ))
    assert scaled.energy.total_energy == pytest.approx(original.energy.total_energy, abs=ENERGY_TOL)
    _assert_forces(scaled.forces.forces, tuple(tuple(0.5*f for f in row) for row in original.forces.forces))


def test_periodic_integer_translation_of_single_atom():
    configuration = _configuration()
    original = _model(1).evaluate(configuration)
    translated = _model(1).evaluate(_shift_atom(configuration, 3, CELL[1]))
    assert translated.energy.total_energy == pytest.approx(original.energy.total_energy, abs=ENERGY_TOL)
    _assert_forces(translated.forces.forces, original.forces.forces)


def test_global_translation_and_e3_rotation_reflection():
    model = _model(1)
    original = model.evaluate(_configuration())
    for transform, linear in (
        (lambda p: (-p[1]+2.0, p[0]-3.0, p[2]+0.5), lambda v: (-v[1],v[0],v[2])),
        (lambda p: (-p[0]+1.0, p[1]+2.0, p[2]-4.0), lambda v: (-v[0],v[1],v[2])),
    ):
        positions = tuple(transform(p) for p in POSITIONS)
        cell = tuple(linear(p) for p in CELL)
        transformed = model.evaluate(_configuration(positions=positions, cell=cell))
        assert transformed.energy.total_energy == pytest.approx(original.energy.total_energy, abs=ENERGY_TOL)
        _assert_forces(transformed.forces.forces, tuple(linear(force) for force in original.forces.forces))


def test_atom_permutation_preserves_energy_and_covariant_forces():
    order = (6, 2, 0, 4, 1, 5, 3)
    model = _model(1)
    first = model.evaluate(_configuration())
    other = model.evaluate(_configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS[i] for i in order),
    ))
    assert other.energy.total_energy == pytest.approx(first.energy.total_energy, abs=ENERGY_TOL)
    assert other.energy.atomic_energies == pytest.approx(tuple(first.energy.atomic_energies[i] for i in order), abs=ENERGY_TOL)
    _assert_forces(other.forces.forces, tuple(first.forces.forces[i] for i in order))


def test_force_matches_finite_difference_of_total_periodic_energy():
    configuration = _configuration()
    model = _model(1)
    evaluated = model.evaluate(configuration)
    for atom in range(configuration.atom_count):
        for axis in range(3):
            delta = [0., 0., 0.]
            delta[axis] = DIFFERENCE_STEP
            plus = model.evaluate(_shift_atom(configuration, atom, delta)).energy.total_energy
            minus = model.evaluate(_shift_atom(configuration, atom, tuple(-v for v in delta))).energy.total_energy
            finite_difference = -(plus-minus)/(2*DIFFERENCE_STEP)
            assert evaluated.forces.forces[atom][axis] == pytest.approx(finite_difference, abs=FORCE_TOL, rel=0.0)


def test_symmetric_pair_force_balance_and_atomic_energy_partition():
    result = _model(2).evaluate(_configuration())
    assert result.energy.total_energy == pytest.approx(fsum(result.energy.atomic_energies), abs=ENERGY_TOL)
    assert result.energy.total_energy == pytest.approx(result.cross_atom_energy_hartree + result.self_image_energy_hartree, abs=ENERGY_TOL)
    for axis in range(3):
        assert abs(fsum(force[axis] for force in result.forces.forces)) < 1.0e-10


def test_image_shell_convergence_is_measured_without_changing_source_parameters():
    energies = tuple(_model(shell).evaluate(_configuration()).energy.total_energy for shell in (0,1,2,3))
    differences = tuple(abs(energies[i+1]-energies[i]) for i in range(3))
    assert differences[0] > differences[1] > differences[2]
    assert differences[1] < 1.0e-5
    assert differences[2] < 2.0e-6


def test_registered_polarization_metadata_is_separate_from_short_range_pair_energy():
    parameters = _parameters()
    changed = replace(parameters, fluoride_polarizability_bohr3=8.0)
    first = _model(1, parameters=parameters).evaluate(_configuration())
    second = _model(1, parameters=changed).evaluate(_configuration())
    assert first.energy == second.energy
    assert first.forces == second.forces
    assert first.source_doi == second.source_doi == SOURCE_DOI


def test_deterministic_replay_and_immutable_source_identity():
    first = _model(1).evaluate(_configuration())
    second = _model(1).evaluate(_configuration())
    assert first == second
    assert first.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    with pytest.raises(FrozenInstanceError):
        first.model_id = "changed"  # type: ignore[misc]


@pytest.mark.parametrize("field,invalid,error", (
    ("model_id", " ", ValueError),
    ("model_id", None, TypeError),
    ("parameters", None, TypeError),
    ("coordinate_unit_to_bohr", 0., ValueError),
    ("coordinate_unit_to_bohr", float("nan"), ValueError),
    ("coordinate_unit_to_bohr", False, TypeError),
    ("image_shell", -1, ValueError),
    ("image_shell", 1.5, TypeError),
    ("image_shell", True, TypeError),
))
def test_invalid_model_contracts_rejected(field, invalid, error):
    with pytest.raises(error):
        replace(_model(), **{field: invalid})


def test_periodicity_configuration_and_invalid_geometry_guards():
    model = _model()
    with pytest.raises(TypeError, match="FLiBeConfiguration"):
        model.evaluate(None)
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(cell=None, periodic=(False,False,False)))
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(periodic=(True, False, True)))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        model.evaluate(_configuration(
            species=("Li", "Be", "F"), positions=POSITIONS[:3],
        ))
    with pytest.raises(ValueError, match="periodic separation"):
        model.evaluate(_configuration(
            species=("Li", "F"), positions=((0.,0.,0.),(0.,0.,0.)),
        ))


def test_result_rejects_corrupt_component_energy_force_and_metadata():
    result = _model(1).evaluate(_configuration())
    assert isinstance(result, FLiBePeriodicShortRangeResult)
    with pytest.raises(ValueError, match="functional identity"):
        replace(result, functional_id="OTHER")
    with pytest.raises(ValueError, match="components must sum"):
        replace(result, cross_atom_energy_hartree=result.cross_atom_energy_hartree+0.1)
    with pytest.raises(ValueError, match="atomic partition"):
        replace(result, energy=EnergyState(
            (result.energy.atomic_energies[0]+0.1, *result.energy.atomic_energies[1:]),
            result.energy.total_energy,
        ))
    with pytest.raises(ValueError, match="force cardinalities"):
        replace(result, forces=ForceState(((0.0,0.0,0.0),)))
    with pytest.raises(ValueError, match="cross-atom image term count"):
        replace(result, cross_atom_image_terms=result.cross_atom_image_terms-1)
    with pytest.raises(ValueError, match="self-atom image term count"):
        replace(result, self_atom_image_terms=result.self_atom_image_terms-1)
