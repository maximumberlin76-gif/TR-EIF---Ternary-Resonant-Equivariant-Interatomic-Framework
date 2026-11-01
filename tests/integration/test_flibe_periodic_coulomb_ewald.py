"""Independent Ewald energy, force, symmetry, and convergence qualification."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from itertools import product
from math import cos, erfc, exp, fsum, pi, sqrt

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import EnergyState, ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import (
    EWALD_FUNCTIONAL_ID,
    FLiBeEwaldParameters,
    FLiBePeriodicEwaldModel,
    FLiBePeriodicEwaldResult,
)
from tr_eif.flibe.units import ParameterProvenance


SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.7, 0.8, 0.9), (3.2, 2.5, 1.4), (6.0, 3.8, 2.2),
    (1.3, 5.5, 6.0), (8.2, 1.3, 6.7), (4.5, 7.0, 8.0),
    (9.0, 8.0, 3.8),
)
CELL = ((12.0, 0.0, 0.0), (1.5, 11.0, 0.0), (0.8, 1.1, 10.0))
CHARGE = {"Li": 1, "Be": 2, "F": -1}
PROVENANCE = ParameterProvenance.TEST_FIXTURE
MADELUNG_CSCL = 1.7626747730709884
MADELUNG_NACL = 1.7475645946331822
ENERGY_TOL = 3.0e-10
FORCE_TOL = 2.0e-7
DERIVATIVE_STEP = 1.0e-5


def _configuration(species=SPECIES, positions=POSITIONS, cell=CELL, periodic=(True, True, True)):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(x) for x in point) for point in positions),
        cell=None if cell is None else tuple(tuple(float(x) for x in edge) for edge in cell),
        periodic=periodic,
    ))


def _model(alpha=0.4, real_shell=2, reciprocal_shell=4, length_factor=1.0):
    return FLiBePeriodicEwaldModel(
        model_id="FLIBE-NEUTRAL-EWALD-FIXTURE",
        parameters=FLiBeEwaldParameters(
            alpha_inverse_bohr=alpha,
            real_image_shell=real_shell,
            reciprocal_image_shell=reciprocal_shell,
            coordinate_unit_to_bohr=length_factor,
            provenance=PROVENANCE,
            source_id="INDEPENDENT-EWALD-TEST-FIXTURE",
        ),
    )


def _cscl(length=6.0):
    """A periodic unit-charge CsCl geometry represented by Li and F labels."""
    return _configuration(
        species=("Li", "F"),
        positions=((0.0, 0.0, 0.0), (length / 2, length / 2, length / 2)),
        cell=((length, 0.0, 0.0), (0.0, length, 0.0), (0.0, 0.0, length)),
    )


def _dot(a, b):
    return fsum(x * y for x, y in zip(a, b, strict=True))


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _independent_ewald_terms(configuration, alpha, real_shell, reciprocal_shell):
    """Calculate independent unordered-pair/image and charge-pair cosine sums."""
    atomic = configuration.configuration
    q = tuple(CHARGE[item] for item in atomic.species)
    xyz = atomic.positions
    a, b, c = atomic.cell
    signed_volume = _dot(a, _cross(b, c))
    volume = abs(signed_volume)
    reciprocal = tuple(
        tuple(2.0 * pi * x / signed_volume for x in normal)
        for normal in (_cross(b, c), _cross(c, a), _cross(a, b))
    )

    def shift(index, basis):
        return tuple(fsum(index[j] * basis[j][d] for j in range(3)) for d in range(3))

    real_terms = []
    for index in product(range(-real_shell, real_shell + 1), repeat=3):
        displacement = shift(index, (a, b, c))
        norm = sqrt(_dot(displacement, displacement))
        if index != (0, 0, 0):
            real_terms.extend(
                0.5 * charge**2 * erfc(alpha * norm) / norm for charge in q
            )
        for i in range(len(q)):
            for j in range(i + 1, len(q)):
                delta = tuple(xyz[i][d] - xyz[j][d] + displacement[d] for d in range(3))
                distance = sqrt(_dot(delta, delta))
                real_terms.append(q[i] * q[j] * erfc(alpha * distance) / distance)

    reciprocal_terms = []
    for index in product(range(-reciprocal_shell, reciprocal_shell + 1), repeat=3):
        if index == (0, 0, 0):
            continue
        k = shift(index, reciprocal)
        k2 = _dot(k, k)
        structure_pair_sum = fsum(charge**2 for charge in q)
        structure_pair_sum += 2.0 * fsum(
            q[i] * q[j] * cos(_dot(k, tuple(xyz[i][d] - xyz[j][d] for d in range(3))))
            for i in range(len(q)) for j in range(i + 1, len(q))
        )
        reciprocal_terms.append(
            (2.0 * pi / volume) * exp(-k2 / (4.0 * alpha**2))
            * structure_pair_sum / k2
        )
    return (
        fsum(real_terms),
        fsum(reciprocal_terms),
        -alpha / sqrt(pi) * fsum(charge**2 for charge in q),
    )


def _change_coordinate(configuration, atom, axis, delta):
    positions = [list(point) for point in configuration.configuration.positions]
    positions[atom][axis] += delta
    return _configuration(
        species=configuration.configuration.species,
        positions=positions,
        cell=configuration.configuration.cell,
        periodic=configuration.configuration.periodic,
    )


def _rotate_vector(v):
    return (-v[1], v[0], v[2])


def test_cscl_madelung_constant_and_symmetry_for_unit_charges():
    """Reference CsCl Madelung constant 1.7626747730709884, nearest-ion scaling."""
    length = 6.0
    result = _model(alpha=0.4, real_shell=2, reciprocal_shell=4).evaluate(_cscl(length))
    nearest_distance = sqrt(3.0) * length / 2.0
    assert result.energy.total_energy == pytest.approx(
        -MADELUNG_CSCL / nearest_distance, rel=0.0, abs=2.0e-12
    )
    assert -result.energy.total_energy * nearest_distance == pytest.approx(
        MADELUNG_CSCL, rel=0.0, abs=2.0e-11
    )
    assert result.formal_charges_e == (1, -1)
    for force in result.forces.forces:
        assert force == pytest.approx((0.0, 0.0, 0.0), abs=5.0e-13)


def test_nacl_madelung_constant_with_eight_ion_cubic_cell():
    """Conventional NaCl charge lattice: four unit-charge pairs per cubic cell."""
    length = 8.0
    half = length / 2.0
    positions = (
        (0.0, 0.0, 0.0), (0.0, half, half),
        (half, 0.0, half), (half, half, 0.0),
        (half, 0.0, 0.0), (0.0, half, 0.0),
        (0.0, 0.0, half), (half, half, half),
    )
    configuration = _configuration(
        species=("Li",) * 4 + ("F",) * 4,
        positions=positions,
        cell=((length, 0.0, 0.0), (0.0, length, 0.0), (0.0, 0.0, length)),
    )
    result = _model(alpha=0.4, real_shell=2, reciprocal_shell=5).evaluate(configuration)
    expected = -4.0 * MADELUNG_NACL / half
    assert result.energy.total_energy == pytest.approx(expected, rel=0.0, abs=2.0e-12)
    for force in result.forces.forces:
        assert force == pytest.approx((0.0, 0.0, 0.0), abs=5.0e-13)


def test_independent_unordered_pair_and_reciprocal_cosine_energy():
    configuration = _configuration()
    result = _model().evaluate(configuration)
    assert isinstance(result, FLiBePeriodicEwaldResult)
    real, reciprocal, self_term = _independent_ewald_terms(configuration, 0.4, 2, 4)
    assert result.real_energy_hartree == pytest.approx(real, rel=0.0, abs=1.0e-12)
    assert result.reciprocal_energy_hartree == pytest.approx(reciprocal, rel=0.0, abs=1.0e-12)
    assert result.self_energy_hartree == pytest.approx(self_term, rel=0.0, abs=1.0e-12)
    assert result.energy.total_energy == pytest.approx(
        fsum((real, reciprocal, self_term)), rel=0.0, abs=1.0e-12
    )
    assert result.cell_volume_bohr3 == pytest.approx(1320.0, rel=0.0, abs=1.0e-12)
    assert result.real_terms_evaluated == 7 * 7 * 5**3 - 7
    assert result.reciprocal_vectors_evaluated == 9**3 - 1
    assert result.functional_id == EWALD_FUNCTIONAL_ID
    assert result.parameters.provenance is PROVENANCE


def test_atomic_partition_formal_charge_and_closed_force_balance():
    result = _model().evaluate(_configuration())
    assert result.formal_charges_e == (1, 1, 2, -1, -1, -1, -1)
    assert sum(result.formal_charges_e) == 0
    assert result.energy.total_energy == pytest.approx(
        fsum(result.energy.atomic_energies), rel=0.0, abs=1.0e-12
    )
    assert result.self_energy_hartree == pytest.approx(
        -10.0 * 0.4 / sqrt(pi), rel=0.0, abs=1.0e-12
    )
    for axis in range(3):
        assert abs(fsum(force[axis] for force in result.forces.forces)) < 5.0e-12


def test_analytic_forces_match_independent_total_energy_differences():
    configuration = _configuration()
    model = _model()
    observed = model.evaluate(configuration)
    for atom in range(configuration.atom_count):
        for axis in range(3):
            plus = model.evaluate(_change_coordinate(configuration, atom, axis, DERIVATIVE_STEP))
            minus = model.evaluate(_change_coordinate(configuration, atom, axis, -DERIVATIVE_STEP))
            reference_force = -(plus.energy.total_energy - minus.energy.total_energy) / (
                2.0 * DERIVATIVE_STEP
            )
            assert observed.forces.forces[atom][axis] == pytest.approx(
                reference_force, rel=0.0, abs=FORCE_TOL
            )


def test_energy_and_forces_transform_under_e3_and_atom_permutation():
    configuration = _configuration()
    model = _model()
    baseline = model.evaluate(configuration)
    transformed = _configuration(
        positions=tuple(
            tuple(_rotate_vector(p)[axis] + (2.0, -1.0, 0.75)[axis] for axis in range(3))
            for p in POSITIONS
        ),
        cell=tuple(_rotate_vector(edge) for edge in CELL),
    )
    rotated = model.evaluate(transformed)
    assert rotated.energy.total_energy == pytest.approx(
        baseline.energy.total_energy, rel=0.0, abs=ENERGY_TOL
    )
    for actual, original in zip(rotated.forces.forces, baseline.forces.forces, strict=True):
        assert actual == pytest.approx(_rotate_vector(original), rel=0.0, abs=FORCE_TOL)

    order = (6, 2, 0, 4, 1, 5, 3)
    reordered = model.evaluate(_configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS[i] for i in order),
    ))
    assert reordered.energy.total_energy == pytest.approx(
        baseline.energy.total_energy, rel=0.0, abs=ENERGY_TOL
    )
    for actual, index in zip(reordered.forces.forces, order, strict=True):
        assert actual == pytest.approx(baseline.forces.forces[index], rel=0.0, abs=FORCE_TOL)


def test_coordinate_unit_rescaling_preserves_physical_energy():
    original = _model().evaluate(_configuration())
    scaled = _model(length_factor=0.5).evaluate(_configuration(
        positions=tuple(tuple(2.0 * value for value in point) for point in POSITIONS),
        cell=tuple(tuple(2.0 * value for value in edge) for edge in CELL),
    ))
    assert scaled.cell_volume_bohr3 == pytest.approx(original.cell_volume_bohr3)
    assert scaled.energy.total_energy == pytest.approx(
        original.energy.total_energy, rel=0.0, abs=ENERGY_TOL
    )
    for actual, original_force in zip(scaled.forces.forces, original.forces.forces, strict=True):
        assert actual == pytest.approx(
            tuple(0.5 * value for value in original_force), rel=0.0, abs=FORCE_TOL
        )


def test_ewald_splitting_and_lattice_truncation_convergence():
    configuration = _configuration()
    # Both real and reciprocal shell limits are predeclared for each alpha.
    reference = _model(alpha=0.25, real_shell=3, reciprocal_shell=5).evaluate(configuration)
    alternative = _model(alpha=0.35, real_shell=3, reciprocal_shell=6).evaluate(configuration)
    refined = _model(alpha=0.45, real_shell=4, reciprocal_shell=8).evaluate(configuration)
    assert alternative.energy.total_energy == pytest.approx(
        reference.energy.total_energy, rel=0.0, abs=1.0e-9
    )
    assert refined.energy.total_energy == pytest.approx(
        reference.energy.total_energy, rel=0.0, abs=1.0e-9
    )
    for first, second in zip(reference.forces.forces, refined.forces.forces, strict=True):
        assert first == pytest.approx(second, rel=0.0, abs=1.0e-8)


def test_periodic_lattice_translation_of_one_ion_at_converged_shells():
    configuration = _configuration()
    model = _model(alpha=0.3, real_shell=3, reciprocal_shell=6)
    baseline = model.evaluate(configuration)
    shift = CELL[1]
    positions = list(POSITIONS)
    positions[3] = tuple(positions[3][axis] + shift[axis] for axis in range(3))
    moved = model.evaluate(_configuration(positions=tuple(positions)))
    assert moved.energy.total_energy == pytest.approx(
        baseline.energy.total_energy, rel=0.0, abs=3.0e-10
    )
    for actual, original in zip(moved.forces.forces, baseline.forces.forces, strict=True):
        assert actual == pytest.approx(original, rel=0.0, abs=2.0e-9)


def test_deterministic_replay_and_immutable_parameter_identity():
    model = _model()
    first = model.evaluate(_configuration())
    assert first == model.evaluate(_configuration())
    assert first.model_id == "FLIBE-NEUTRAL-EWALD-FIXTURE"
    assert first.parameters.source_id == "INDEPENDENT-EWALD-TEST-FIXTURE"
    with pytest.raises(FrozenInstanceError):
        first.model_id = "ALTERED"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("alpha_inverse_bohr", 0.0, ValueError),
        ("alpha_inverse_bohr", float("nan"), ValueError),
        ("alpha_inverse_bohr", False, TypeError),
        ("real_image_shell", -1, ValueError),
        ("real_image_shell", 1.5, TypeError),
        ("real_image_shell", True, TypeError),
        ("reciprocal_image_shell", 0, ValueError),
        ("reciprocal_image_shell", 2.0, TypeError),
        ("coordinate_unit_to_bohr", -1.0, ValueError),
        ("coordinate_unit_to_bohr", float("inf"), ValueError),
        ("provenance", "TEST_FIXTURE", TypeError),
        ("source_id", " bad ", ValueError),
    ),
)
def test_invalid_ewald_parameters_are_rejected(field, invalid, error):
    parameters = _model().parameters
    with pytest.raises(error):
        replace(parameters, **{field: invalid})


def test_periodic_boundary_and_configuration_contract():
    model = _model()
    with pytest.raises(TypeError, match="FLiBeConfiguration"):
        model.evaluate(None)
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(periodic=(True, False, True)))
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(periodic=(False, False, False)))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        model.evaluate(_configuration(
            species=("Li", "Be", "F"), positions=POSITIONS[:3]
        ))
    with pytest.raises(ValueError, match="positive"):
        model.evaluate(_configuration(
            species=("Li", "F"), positions=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        ))


def test_result_rejects_incorrect_energy_force_and_shell_metadata():
    result = _model().evaluate(_configuration())
    with pytest.raises(ValueError, match="functional identifier"):
        replace(result, functional_id="OTHER")
    with pytest.raises(ValueError, match="formal charges"):
        replace(result, formal_charges_e=(0,) * 7)
    with pytest.raises(ValueError, match="component energies"):
        replace(result, real_energy_hartree=result.real_energy_hartree + 1.0)
    with pytest.raises(ValueError, match="atomic energy partition"):
        replace(result, energy=EnergyState(
            atomic_energies=(result.energy.atomic_energies[0] + 0.1, *result.energy.atomic_energies[1:]),
            total_energy=result.energy.total_energy,
        ))
    with pytest.raises(ValueError, match="force cardinality"):
        replace(result, forces=ForceState(((0.0, 0.0, 0.0),)))
    with pytest.raises(ValueError, match="directed term count"):
        replace(result, real_terms_evaluated=result.real_terms_evaluated - 1)
    with pytest.raises(ValueError, match="reciprocal lattice vector count"):
        replace(result, reciprocal_vectors_evaluated=result.reciprocal_vectors_evaluated - 1)
