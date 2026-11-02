"""Independent energy, force, and boundary tests for periodic FLiBe fixed charge."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from itertools import product
from math import cos, erfc, exp, factorial, floor, fsum, pi, sqrt
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import EnergyState, ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import (
    FLiBeEwaldParameters,
    FLiBePeriodicEwaldModel,
)
from tr_eif.flibe.periodic_fixed_charge import (
    PERIODIC_FIXED_CHARGE_FUNCTIONAL_ID,
    FLiBePeriodicFixedChargeModel,
    FLiBePeriodicFixedChargeResult,
)
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_pair_coefficients import (
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
CHARGE = {"Li": 1, "Be": 2, "F": -1}
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

# Primary-source radial values in atomic units, independently specified.
PAIR_TABLE = {
    frozenset(("Li",)): (195.91, 4.252, 0.0, 0.0, 1.0, 1.0),
    frozenset(("Li", "Be")): (0.0, 1.0, 0.0, 0.0, 1.0, 1.0),
    frozenset(("Li", "F")): (20.42, 2.052, 0.0, 0.0, 1.0, 1.0),
    frozenset(("Be",)): (106.16, 3.944, 0.0, 0.0, 1.0, 1.0),
    frozenset(("Be", "F")): (41.72, 2.254, 0.0, 0.0, 1.0, 1.0),
    frozenset(("F",)): (181.84, 2.267, 15.0, 150.0, 1.9, 1.9),
}
PROVENANCE = ParameterProvenance.TEST_FIXTURE
ENERGY_TOL = 3.0e-10
FORCE_TOL = 2.0e-7
DIFFERENCE_STEP = 1.0e-5


def _configuration(*, species=SPECIES, positions=POSITIONS, cell=CELL,
                   periodic=(True, True, True)):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(v) for v in row) for row in positions),
        cell=None if cell is None else tuple(tuple(float(v) for v in row) for row in cell),
        periodic=periodic,
    ))


def _model(*, alpha=0.4, real_shell=1, reciprocal_shell=3,
           short_shell=1, coordinate_unit_to_bohr=1.0, parameters=None):
    source = load_flibe_registered_pair_parameters(SOURCE) if parameters is None else parameters
    ewald = FLiBePeriodicEwaldModel(
        model_id="EWALD-FIXTURE",
        parameters=FLiBeEwaldParameters(
            alpha_inverse_bohr=alpha,
            real_image_shell=real_shell,
            reciprocal_image_shell=reciprocal_shell,
            coordinate_unit_to_bohr=coordinate_unit_to_bohr,
            provenance=PROVENANCE,
            source_id="INDEPENDENT-EWALD-TEST-FIXTURE",
        ),
    )
    short_range = FLiBePeriodicShortRangeModel(
        model_id="SOURCE-SHORT-RANGE",
        parameters=source,
        coordinate_unit_to_bohr=coordinate_unit_to_bohr,
        image_shell=short_shell,
    )
    return FLiBePeriodicFixedChargeModel(
        model_id="FLIBE-PERIODIC-FIXED-CHARGE-FIXTURE",
        ewald_model=ewald,
        short_range_model=short_range,
    )


def _dot(first, second):
    return fsum(a * b for a, b in zip(first, second, strict=True))


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _translate(index, basis):
    return tuple(fsum(index[j] * basis[j][a] for j in range(3)) for a in range(3))


def _independent_ewald_energy(configuration, alpha, real_shell, reciprocal_shell):
    """Independent unordered-pair real sum and charge-pair reciprocal sum."""
    xyz = configuration.configuration.positions
    cell = configuration.configuration.cell
    charges = tuple(CHARGE[s] for s in configuration.configuration.species)
    signed_volume = _dot(cell[0], _cross(cell[1], cell[2]))
    volume = abs(signed_volume)
    reciprocal = tuple(
        tuple(2 * pi * component / signed_volume for component in normal)
        for normal in (_cross(cell[1], cell[2]), _cross(cell[2], cell[0]), _cross(cell[0], cell[1]))
    )
    real = []
    for image in product(range(-real_shell, real_shell + 1), repeat=3):
        shift = _translate(image, cell)
        if image != (0, 0, 0):
            length = sqrt(_dot(shift, shift))
            real.extend(0.5 * charge**2 * erfc(alpha * length) / length for charge in charges)
        for i in range(len(charges)):
            for j in range(i + 1, len(charges)):
                delta = tuple(xyz[i][a] - xyz[j][a] + shift[a] for a in range(3))
                r = sqrt(_dot(delta, delta))
                real.append(charges[i] * charges[j] * erfc(alpha * r) / r)
    reciprocal_terms = []
    for index in product(range(-reciprocal_shell, reciprocal_shell + 1), repeat=3):
        if index == (0, 0, 0):
            continue
        wave = _translate(index, reciprocal)
        k2 = _dot(wave, wave)
        factor = 2 * pi / volume * exp(-k2 / (4 * alpha**2)) / k2
        structure = fsum(q**2 for q in charges)
        structure += 2 * fsum(
            charges[i] * charges[j] * cos(_dot(wave, tuple(xyz[i][a] - xyz[j][a] for a in range(3))))
            for i in range(len(charges)) for j in range(i + 1, len(charges))
        )
        reciprocal_terms.append(factor * structure)
    self_term = -alpha / sqrt(pi) * fsum(q**2 for q in charges)
    return fsum(real), fsum(reciprocal_terms), self_term


def _independent_short_energy(configuration, shell):
    """Sum the published Born and damped dispersion terms without Coulomb."""
    xyz = configuration.configuration.positions
    species = configuration.configuration.species
    cell = configuration.configuration.cell
    normals = (_cross(cell[1], cell[2]), _cross(cell[2], cell[0]), _cross(cell[0], cell[1]))
    volume_signed = _dot(cell[0], normals[0])

    def radial(r, names):
        amplitude, decay, c6, c8, beta6, beta8 = PAIR_TABLE[frozenset(names)]
        energy = amplitude * exp(-decay * r)
        for n, coefficient, beta in ((6, c6, beta6), (8, c8, beta8)):
            if coefficient:
                z = beta * r
                damping = 1 - exp(-z) * fsum(z**k / factorial(k) for k in range(n + 1))
                energy -= coefficient * damping / r**n
        return energy

    cross_terms, self_terms = [], []
    for image in product(range(-shell, shell + 1), repeat=3):
        shift = _translate(image, cell)
        if image != (0, 0, 0):
            norm = sqrt(_dot(shift, shift))
            self_terms.extend(0.5 * radial(norm, (s, s)) for s in species)
        for i in range(len(species)):
            for j in range(i + 1, len(species)):
                delta = tuple(xyz[i][a] - xyz[j][a] for a in range(3))
                fractions = tuple(_dot(delta, normal) / volume_signed for normal in normals)
                offset = tuple(floor(f + 0.5) for f in fractions)
                centered = tuple(delta[a] - fsum(offset[k] * cell[k][a] for k in range(3)) for a in range(3))
                with_image = tuple(centered[a] + shift[a] for a in range(3))
                cross_terms.append(radial(sqrt(_dot(with_image, with_image)), (species[i], species[j])))
    return fsum(cross_terms), fsum(self_terms)


def _displaced(configuration, atom, axis, offset):
    points = [list(row) for row in configuration.configuration.positions]
    points[atom][axis] += offset
    return _configuration(
        species=configuration.configuration.species,
        positions=points,
        cell=configuration.configuration.cell,
        periodic=configuration.configuration.periodic,
    )


def _assert_forces(actual, reference, *, tolerance=FORCE_TOL):
    assert len(actual) == len(reference)
    for row, expected in zip(actual, reference, strict=True):
        assert row == pytest.approx(expected, rel=0, abs=tolerance)


def test_source_provenance_composition_and_five_term_registry():
    result = _model().evaluate(_configuration())
    assert result.model_id == "FLIBE-PERIODIC-FIXED-CHARGE-FIXTURE"
    assert result.functional_id == PERIODIC_FIXED_CHARGE_FUNCTIONAL_ID
    assert result.configuration.composition().formula_unit_fractions == (2 / 3, 1 / 3)
    assert result.ewald_result.formal_charges_e == (1, 1, 2, -1, -1, -1, -1)
    assert result.source_doi == SOURCE_DOI
    assert result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert all(pair.provenance is ParameterProvenance.PRIMARY_SOURCE
               for pair in result.short_range_result.parameters.pair_coefficients)
    assert result.energy_components_hartree == (
        ("ewald_real", result.ewald_result.real_energy_hartree),
        ("ewald_reciprocal", result.ewald_result.reciprocal_energy_hartree),
        ("ewald_self", result.ewald_result.self_energy_hartree),
        ("short_range_cross_atom", result.short_range_result.cross_atom_energy_hartree),
        ("short_range_self_image", result.short_range_result.self_image_energy_hartree),
    )


def test_independent_ewald_and_short_range_numerical_reference():
    configuration = _configuration()
    result = _model().evaluate(configuration)
    ewald = _independent_ewald_energy(configuration, .4, 1, 3)
    short = _independent_short_energy(configuration, 1)
    assert tuple(value for _, value in result.energy_components_hartree) == pytest.approx(
        (*ewald, *short), abs=ENERGY_TOL, rel=0,
    )
    assert result.ewald_result.energy.total_energy == pytest.approx(fsum(ewald), abs=ENERGY_TOL)
    assert result.short_range_result.energy.total_energy == pytest.approx(fsum(short), abs=ENERGY_TOL)
    assert result.energy.total_energy == pytest.approx(fsum((*ewald, *short)), abs=ENERGY_TOL)
    assert result.energy.total_energy == pytest.approx(1.5817561017982311, abs=ENERGY_TOL, rel=0)


def test_zero_short_range_coefficients_reduce_exactly_to_ewald():
    """Remove all Born and dispersion terms while retaining formal Coulomb charges."""
    source = load_flibe_registered_pair_parameters(SOURCE)
    cleared = tuple(replace(pair, born_amplitude_hartree=0.0,
                            c6_hartree_bohr6=0.0, c8_hartree_bohr8=0.0)
                    for pair in source.pair_coefficients)
    fixture = replace(source, pair_coefficients=cleared)
    result = _model(parameters=fixture, short_shell=1).evaluate(_configuration())
    assert result.short_range_result.energy.total_energy == 0.0
    assert all(row == (0.0, 0.0, 0.0) for row in result.short_range_result.forces.forces)
    assert result.energy.total_energy == pytest.approx(result.ewald_result.energy.total_energy, abs=1e-13)
    assert result.energy.atomic_energies == result.ewald_result.energy.atomic_energies
    assert result.forces == result.ewald_result.forces


def test_short_range_is_independent_of_ewald_splitting_parameter():
    configuration = _configuration()
    first = _model(alpha=0.28, real_shell=2, reciprocal_shell=4).evaluate(configuration)
    second = _model(alpha=0.43, real_shell=2, reciprocal_shell=4).evaluate(configuration)
    assert first.short_range_result == second.short_range_result
    assert first.ewald_result.parameters.alpha_inverse_bohr != second.ewald_result.parameters.alpha_inverse_bohr
    assert first.energy.total_energy - first.ewald_result.energy.total_energy == pytest.approx(
        first.short_range_result.energy.total_energy, abs=ENERGY_TOL,
    )


def test_combined_atomic_energies_and_forces_are_component_sums():
    result = _model().evaluate(_configuration())
    assert result.energy.total_energy == pytest.approx(fsum(result.energy.atomic_energies), abs=1e-12)
    for i in range(7):
        assert result.energy.atomic_energies[i] == pytest.approx(
            result.ewald_result.energy.atomic_energies[i] +
            result.short_range_result.energy.atomic_energies[i], abs=1e-12,
        )
        for axis in range(3):
            assert result.forces.forces[i][axis] == pytest.approx(
                result.ewald_result.forces.forces[i][axis] +
                result.short_range_result.forces.forces[i][axis], abs=1e-12,
            )
    for axis in range(3):
        assert abs(fsum(force[axis] for force in result.forces.forces)) <= 1e-11


@pytest.mark.parametrize("atom", range(7))
def test_cartesian_force_matches_total_energy_gradient_for_every_atom(atom):
    configuration = _configuration()
    model = _model()
    force = model.evaluate(configuration).forces.forces[atom]
    for axis in range(3):
        plus = model.evaluate(_displaced(configuration, atom, axis, DIFFERENCE_STEP)).energy.total_energy
        minus = model.evaluate(_displaced(configuration, atom, axis, -DIFFERENCE_STEP)).energy.total_energy
        independent = -(plus - minus) / (2 * DIFFERENCE_STEP)
        assert force[axis] == pytest.approx(independent, abs=FORCE_TOL, rel=0)


def test_e3_rotation_reflection_and_translation_covariance():
    model = _model()
    original = model.evaluate(_configuration())
    operations = (
        (lambda p: (-p[1] + 2., p[0] - 3., p[2] + 0.5), lambda v: (-v[1], v[0], v[2])),
        (lambda p: (-p[0] + 1., p[1] + 2., p[2] - 4.), lambda v: (-v[0], v[1], v[2])),
    )
    for transform, linear in operations:
        shifted = _configuration(
            positions=tuple(transform(p) for p in POSITIONS),
            cell=tuple(linear(c) for c in CELL),
        )
        actual = model.evaluate(shifted)
        assert actual.energy.total_energy == pytest.approx(original.energy.total_energy, abs=ENERGY_TOL)
        _assert_forces(actual.forces.forces, tuple(linear(row) for row in original.forces.forces))


def test_common_atom_permutation_preserves_scalar_and_reorders_vectors():
    order = (6, 2, 0, 4, 1, 5, 3)
    model = _model()
    original = model.evaluate(_configuration())
    changed = _configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS[i] for i in order),
    )
    actual = model.evaluate(changed)
    assert actual.energy.total_energy == pytest.approx(original.energy.total_energy, abs=ENERGY_TOL)
    assert actual.energy.atomic_energies == pytest.approx(
        tuple(original.energy.atomic_energies[i] for i in order), abs=ENERGY_TOL,
    )
    _assert_forces(actual.forces.forces, tuple(original.forces.forces[i] for i in order))


def test_coordinate_unit_bridge_scales_forces_and_preserves_energy():
    first = _model().evaluate(_configuration())
    second = _model(coordinate_unit_to_bohr=0.5).evaluate(_configuration(
        positions=tuple(tuple(2 * x for x in point) for point in POSITIONS),
        cell=tuple(tuple(2 * x for x in edge) for edge in CELL),
    ))
    assert second.coordinate_unit_to_bohr == 0.5
    assert second.energy.total_energy == pytest.approx(first.energy.total_energy, abs=ENERGY_TOL)
    _assert_forces(second.forces.forces,
                   tuple(tuple(0.5 * v for v in row) for row in first.forces.forces))


def test_periodic_cell_translation_at_declared_refinement():
    model = _model(alpha=0.3, real_shell=3, reciprocal_shell=6, short_shell=2)
    configuration = _configuration()
    original = model.evaluate(configuration)
    moved = list(POSITIONS)
    moved[3] = tuple(moved[3][axis] + CELL[1][axis] for axis in range(3))
    actual = model.evaluate(_configuration(positions=tuple(moved)))
    assert actual.energy.total_energy == pytest.approx(original.energy.total_energy, abs=4e-10)
    _assert_forces(actual.forces.forces, original.forces.forces, tolerance=3e-9)


def test_refinement_records_distinct_ewald_and_short_range_errors():
    configuration = _configuration()
    low = _model(real_shell=1, reciprocal_shell=3, short_shell=0).evaluate(configuration)
    medium = _model(real_shell=2, reciprocal_shell=4, short_shell=1).evaluate(configuration)
    high = _model(real_shell=3, reciprocal_shell=6, short_shell=2).evaluate(configuration)
    assert abs(high.energy.total_energy - medium.energy.total_energy) < abs(
        medium.energy.total_energy - low.energy.total_energy
    )
    assert abs(high.short_range_result.energy.total_energy - medium.short_range_result.energy.total_energy) < (
        abs(medium.short_range_result.energy.total_energy - low.short_range_result.energy.total_energy)
    )
    assert low.ewald_result.parameters.real_image_shell == 1
    assert high.ewald_result.parameters.real_image_shell == 3
    assert low.short_range_result.image_shell == 0
    assert high.short_range_result.image_shell == 2


def test_source_polarizability_is_not_an_implicit_fixed_charge_energy_term():
    original_source = load_flibe_registered_pair_parameters(SOURCE)
    changed = replace(original_source, fluoride_polarizability_bohr3=8.0)
    original = _model(parameters=original_source).evaluate(_configuration())
    modified = _model(parameters=changed).evaluate(_configuration())
    assert original.energy == modified.energy
    assert original.forces == modified.forces
    assert original.source_doi == modified.source_doi == SOURCE_DOI


def test_deterministic_replay_and_frozen_result():
    model = _model()
    first = model.evaluate(_configuration())
    second = model.evaluate(_configuration())
    assert first == second
    assert isinstance(first, FLiBePeriodicFixedChargeResult)
    with pytest.raises(FrozenInstanceError):
        first.model_id = "CHANGED"  # type: ignore[misc]


@pytest.mark.parametrize("field,invalid,error", (
    ("model_id", " ", ValueError),
    ("model_id", None, TypeError),
    ("ewald_model", None, TypeError),
    ("short_range_model", None, TypeError),
))
def test_invalid_composite_model_contracts(field, invalid, error):
    with pytest.raises(error):
        replace(_model(), **{field: invalid})


def test_mismatched_length_conversion_is_rejected():
    model = _model()
    incompatible = replace(model.short_range_model, coordinate_unit_to_bohr=0.5)
    with pytest.raises(ValueError, match="conversions must agree"):
        replace(model, short_range_model=incompatible)


def test_evaluation_rejects_invalid_and_nonperiodic_configuration():
    model = _model()
    with pytest.raises(TypeError, match="FLiBeConfiguration"):
        model.evaluate(None)
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(periodic=(True, False, True)))
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(periodic=(False, False, False), cell=None))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        model.evaluate(_configuration(species=("Li", "Be", "F"), positions=POSITIONS[:3]))


def test_result_rejects_corrupted_component_identity_and_energy_balance():
    result = _model().evaluate(_configuration())
    with pytest.raises(ValueError, match="functional identity"):
        replace(result, functional_id="OTHER")
    with pytest.raises(ValueError, match="component results must use"):
        changed = _configuration(positions=tuple(tuple(v + 0.1 for v in row) for row in POSITIONS))
        replace(result, configuration=changed)
    with pytest.raises(ValueError, match="combined energy must equal"):
        changed = EnergyState(result.energy.atomic_energies,
                              result.energy.total_energy + 1.0)
        replace(result, energy=changed)
    with pytest.raises(ValueError, match="combined atomic energy partition"):
        changed = EnergyState(
            (result.energy.atomic_energies[0] + 0.1, *result.energy.atomic_energies[1:]),
            result.energy.total_energy,
        )
        replace(result, energy=changed)
    with pytest.raises(ValueError, match="combined forces must equal"):
        modified = list(result.forces.forces)
        modified[0] = (modified[0][0] + 0.1, *modified[0][1:])
        replace(result, forces=ForceState(tuple(modified)))
    with pytest.raises(TypeError, match="ewald_result"):
        replace(result, ewald_result=None)
    with pytest.raises(TypeError, match="short_range_result"):
        replace(result, short_range_result=None)
