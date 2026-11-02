"""Independent fixed-cell energy-gradient tests for periodic FLiBe polarization."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_polarization_forces import (
    POLARIZATION_FORCE_FUNCTIONAL_ID,
    FLiBePeriodicPolarizationForceResult,
    evaluate_flibe_periodic_polarization_forces,
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
    (0.0, 0.0, 0.0),
    (8.0, 0.0, 0.0),
    (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0),
    (8.0, 5.0, 6.0),
    (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
CELL = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
FORCE_TOL = 2.0e-7
SYMMETRY_TOL = 3.0e-9
ENERGY_TOL = 2.0e-10
DERIVATIVE_STEP = 2.0e-5
COMPONENT_NAMES = (
    "charge_real", "charge_reciprocal", "charge_damping",
    "dipole_real", "dipole_reciprocal",
)


def _configuration(species=SPECIES, positions=POSITIONS, cell=CELL,
                   periodic=(True, True, True)):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(x) for x in p) for p in positions),
        cell=None if cell is None else tuple(tuple(float(x) for x in v) for v in cell),
        periodic=periodic,
    ))


def _model(*, alpha=0.25, real_shell=1, reciprocal_shell=3, damping_shell=1,
           length_factor=1.0, parameters=None):
    return FLiBePeriodicPolarizationModel(
        model_id="FLIBE-PERIODIC-POLARIZATION-FORCE-FIXTURE",
        parameters=(load_flibe_registered_pair_parameters(SOURCE)
                    if parameters is None else parameters),
        ewald_parameters=FLiBeEwaldParameters(
            alpha_inverse_bohr=alpha,
            real_image_shell=real_shell,
            reciprocal_image_shell=reciprocal_shell,
            coordinate_unit_to_bohr=length_factor,
            provenance=ParameterProvenance.TEST_FIXTURE,
            source_id="FIXED-CELL-EWALD-FORCE-FIXTURE",
        ),
        damping_image_shell=damping_shell,
        stationarity_absolute_tolerance=1.0e-10,
    )


def _lif(distance=4.0, cell_length=18.0):
    cell = tuple(tuple(cell_length if i == j else 0.0 for j in range(3))
                 for i in range(3))
    return _configuration(
        species=("Li", "F"),
        positions=((0.0, 0.0, 0.0), (distance, 0.0, 0.0)),
        cell=cell,
    )


def _shift(configuration, atom, axis, displacement):
    coordinates = [list(p) for p in configuration.configuration.positions]
    coordinates[atom][axis] += displacement
    return _configuration(
        species=configuration.configuration.species,
        positions=coordinates,
        cell=configuration.configuration.cell,
        periodic=configuration.configuration.periodic,
    )


def _independent_force(model, configuration, atom, axis, step=DERIVATIVE_STEP):
    """Differentiate reoptimized *energy*, without calling any force helper."""
    plus = model.evaluate(_shift(configuration, atom, axis, step)).polarization_energy_hartree
    minus = model.evaluate(_shift(configuration, atom, axis, -step)).polarization_energy_hartree
    return -(plus - minus) / (2.0 * step)


def _assert_vectors(actual, expected, absolute=SYMMETRY_TOL):
    assert len(actual) == len(expected)
    for found, target in zip(actual, expected, strict=True):
        assert found == pytest.approx(target, rel=0.0, abs=absolute)


@pytest.fixture(scope="module")
def model():
    return _model()


@pytest.fixture(scope="module")
def result(model):
    return evaluate_flibe_periodic_polarization_forces(model, _configuration())


def test_source_identity_stationarity_and_energy_binding(result):
    assert isinstance(result, FLiBePeriodicPolarizationForceResult)
    assert result.functional_id == POLARIZATION_FORCE_FUNCTIONAL_ID
    assert result.configuration.composition().formula_unit_fractions == (2.0/3.0, 1.0/3.0)
    assert result.polarization_result.source_doi == SOURCE_DOI
    assert result.polarization_result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert result.polarization_result.polarizable_indices == (3, 4, 5, 6)
    assert result.polarization_result.max_stationarity_residual_atomic <= 1.0e-10
    assert result.polarization_energy_hartree == result.polarization_result.polarization_energy_hartree
    assert result.configuration == result.polarization_result.configuration


def test_five_force_channels_add_to_stationary_total(result):
    assert tuple(name for name, _ in result.force_components) == COMPONENT_NAMES
    assert all(isinstance(component, ForceState) for _, component in result.force_components)
    assert len(result.polarization_forces.forces) == 7
    for atom in range(7):
        for axis in range(3):
            independently_summed = fsum(component.forces[atom][axis]
                                        for _, component in result.force_components)
            assert result.polarization_forces.forces[atom][axis] == pytest.approx(
                independently_summed, rel=0.0, abs=1.0e-12)
    assert any(abs(x) > 1.0e-12 for row in result.charge_damping_forces.forces for x in row)
    assert any(abs(x) > 1.0e-12 for row in result.charge_reciprocal_forces.forces for x in row)
    assert any(abs(x) > 1.0e-12 for row in result.dipole_real_forces.forces for x in row)


def test_analytic_forces_match_all_21_relaxed_energy_derivatives(model, result):
    configuration = _configuration()
    for atom in range(7):
        for axis in range(3):
            independent = _independent_force(model, configuration, atom, axis)
            assert result.polarization_forces.forces[atom][axis] == pytest.approx(
                independent, rel=0.0, abs=FORCE_TOL)


@pytest.mark.parametrize("atom,axis", ((0, 0), (2, 1), (5, 2)))
def test_gradient_step_refinement(model, result, atom, axis):
    configuration = _configuration()
    coarse = _independent_force(model, configuration, atom, axis, step=4.0e-5)
    fine = _independent_force(model, configuration, atom, axis, step=2.0e-5)
    analytic = result.polarization_forces.forces[atom][axis]
    assert abs(fine - analytic) <= FORCE_TOL
    assert abs(coarse - fine) <= FORCE_TOL


def test_two_ion_periodic_analytic_force_matches_relaxed_energy():
    configuration = _lif()
    m = _model(alpha=0.25, real_shell=2, reciprocal_shell=4)
    evaluated = evaluate_flibe_periodic_polarization_forces(m, configuration)
    for atom in range(2):
        for axis in range(3):
            assert evaluated.polarization_forces.forces[atom][axis] == pytest.approx(
                _independent_force(m, configuration, atom, axis),
                rel=0.0, abs=FORCE_TOL)
    _assert_vectors(evaluated.polarization_forces.forces[0:1],
                    (tuple(-x for x in evaluated.polarization_forces.forces[1]),),
                    absolute=1.0e-11)
    assert evaluated.polarization_result.polarizable_indices == (1,)
    assert abs(evaluated.polarization_forces.forces[1][0]) > 1.0e-6


def test_global_force_balance_holds_for_every_component(result):
    for _, component in (*result.force_components, ("combined", result.polarization_forces)):
        for axis in range(3):
            assert abs(fsum(row[axis] for row in component.forces)) < 1.0e-10


def test_rotation_translation_and_reflection_covariance(model, result):
    operations = (
        (lambda p: (-p[1]+3.0, p[0]-2.0, p[2]+1.0),
         lambda v: (-v[1], v[0], v[2])),
        (lambda p: (-p[0]+1.5, p[1]-4.0, p[2]+0.75),
         lambda v: (-v[0], v[1], v[2])),
    )
    for transform, linear in operations:
        changed = _configuration(
            positions=tuple(transform(point) for point in POSITIONS),
            cell=tuple(linear(edge) for edge in CELL),
        )
        evaluated = evaluate_flibe_periodic_polarization_forces(model, changed)
        assert evaluated.polarization_energy_hartree == pytest.approx(
            result.polarization_energy_hartree, abs=ENERGY_TOL, rel=0.0)
        for (left_name, left), (right_name, right) in zip(
            result.force_components, evaluated.force_components, strict=True
        ):
            assert left_name == right_name
            _assert_vectors(right.forces, tuple(linear(v) for v in left.forces))
        _assert_vectors(evaluated.polarization_forces.forces,
                        tuple(linear(v) for v in result.polarization_forces.forces))


def test_atomic_permutation_preserves_component_force_order(model, result):
    order = (6, 2, 0, 4, 1, 5, 3)
    changed = _configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS[i] for i in order),
    )
    evaluated = evaluate_flibe_periodic_polarization_forces(model, changed)
    assert evaluated.polarization_energy_hartree == pytest.approx(
        result.polarization_energy_hartree, rel=0.0, abs=ENERGY_TOL)
    for (name_a, component_a), (name_b, component_b) in zip(
        result.force_components, evaluated.force_components, strict=True
    ):
        assert name_a == name_b
        _assert_vectors(component_b.forces, tuple(component_a.forces[i] for i in order))
    _assert_vectors(evaluated.polarization_forces.forces,
                    tuple(result.polarization_forces.forces[i] for i in order))


def test_length_to_bohr_conversion_preserves_energy_and_scales_forces(model, result):
    scaled = replace(model, ewald_parameters=replace(
        model.ewald_parameters, coordinate_unit_to_bohr=0.5))
    configuration = _configuration(
        positions=tuple(tuple(2.0*x for x in p) for p in POSITIONS),
        cell=tuple(tuple(2.0*x for x in edge) for edge in CELL),
    )
    evaluated = evaluate_flibe_periodic_polarization_forces(scaled, configuration)
    assert evaluated.polarization_energy_hartree == pytest.approx(
        result.polarization_energy_hartree, abs=ENERGY_TOL, rel=0.0)
    for (_, before), (_, after) in zip(result.force_components, evaluated.force_components, strict=True):
        _assert_vectors(after.forces, tuple(tuple(0.5*x for x in v) for v in before.forces))
    _assert_vectors(evaluated.polarization_forces.forces,
                    tuple(tuple(0.5*x for x in v) for v in result.polarization_forces.forces))


def test_periodic_lattice_translation_at_refined_shells():
    # For a truncated image sum, use declared refined shells and finite tolerance.
    refined = _model(real_shell=3, reciprocal_shell=6, damping_shell=3)
    initial = _configuration()
    positions = list(POSITIONS)
    positions[3] = tuple(positions[3][i] + CELL[1][i] for i in range(3))
    before = evaluate_flibe_periodic_polarization_forces(refined, initial)
    after = evaluate_flibe_periodic_polarization_forces(refined, _configuration(positions=positions))
    assert after.polarization_energy_hartree == pytest.approx(
        before.polarization_energy_hartree, abs=2.0e-8, rel=0.0)
    _assert_vectors(after.polarization_forces.forces, before.polarization_forces.forces,
                    absolute=2.0e-8)


def test_deterministic_replay_and_immutable_result(model, result):
    assert result == evaluate_flibe_periodic_polarization_forces(model, _configuration())
    with pytest.raises(FrozenInstanceError):
        result.functional_id = "CHANGED"  # type: ignore[misc]


def test_result_constructor_rejects_broken_force_decomposition(result):
    with pytest.raises(ValueError, match="functional identity"):
        replace(result, functional_id="OTHER")
    with pytest.raises(TypeError, match="ForceState"):
        replace(result, polarization_forces=None)
    with pytest.raises(ValueError, match="cardinalities"):
        replace(result, polarization_forces=ForceState(((0.0, 0.0, 0.0),)))
    modified = list(result.polarization_forces.forces)
    modified[0] = (modified[0][0] + 0.1, *modified[0][1:])
    with pytest.raises(ValueError, match="sum of geometric components"):
        replace(result, polarization_forces=ForceState(tuple(modified)))
    with pytest.raises(TypeError, match="FLiBePeriodicPolarizationResult"):
        replace(result, polarization_result=None)


@pytest.mark.parametrize("model_input,configuration_input", (
    (None, "valid"),
    ("wrong", "valid"),
    ("valid", None),
    ("valid", "wrong"),
))
def test_rejects_invalid_model_and_configuration(model, model_input, configuration_input):
    candidate_model = model if model_input == "valid" else model_input
    candidate_configuration = _configuration() if configuration_input == "valid" else configuration_input
    with pytest.raises(TypeError):
        evaluate_flibe_periodic_polarization_forces(candidate_model, candidate_configuration)


def test_rejects_nonperiodic_geometry_and_unstable_hessian(model):
    with pytest.raises(ValueError, match="three periodic axes"):
        evaluate_flibe_periodic_polarization_forces(
            model, _configuration(cell=None, periodic=(False, False, False)))
    dense = _configuration(positions=(
        (0., 0., 0.), (0.8, 0., 0.), (0.5, 0.7, 0.),
        (0.1, 0.2, 0.5), (0.6, 0.4, 0.5),
        (0.2, 0.8, 0.9), (0.7, 0.7, 0.9),
    ))
    with pytest.raises(ValueError, match="positive definite"):
        evaluate_flibe_periodic_polarization_forces(model, dense)
