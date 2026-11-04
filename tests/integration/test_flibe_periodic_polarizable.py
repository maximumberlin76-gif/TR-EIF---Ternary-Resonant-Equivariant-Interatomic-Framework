"""Independent full-energy, relaxed-force, and symmetry checks for periodic FLiBe."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import EnergyState, ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import (
    FLiBeEwaldParameters,
    FLiBePeriodicEwaldModel,
)
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import (
    POLARIZABLE_PERIODIC_FUNCTIONAL_ID,
    FLiBePeriodicPolarizableModel,
    FLiBePeriodicPolarizableResult,
)
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
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
COMPONENT_NAMES = (
    "ewald_real",
    "ewald_reciprocal",
    "ewald_self",
    "short_range_cross_atom",
    "short_range_self_image",
    "polarization_self",
    "polarization_charge_dipole",
    "polarization_dipole_dipole",
)
DERIVATIVE_STEP = 2.0e-5
ENERGY_ABSOLUTE_TOLERANCE = 3.0e-10
FORCE_ABSOLUTE_TOLERANCE = 3.0e-7
SYMMETRY_ABSOLUTE_TOLERANCE = 1.0e-8
STATIONARITY_ABSOLUTE_TOLERANCE = 1.0e-10


def _configuration(species=SPECIES, positions=POSITIONS, cell=CELL, *, periodic=(True, True, True)):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(v) for v in p) for p in positions),
        cell=None if cell is None else tuple(tuple(float(v) for v in e) for e in cell),
        periodic=periodic,
    ))


def _model(*, alpha=0.25, real_shell=1, reciprocal_shell=3,
           short_shell=1, damping_shell=1, unit=1.0):
    source = load_flibe_registered_pair_parameters(SOURCE)
    ewald_parameters = FLiBeEwaldParameters(
        alpha_inverse_bohr=alpha,
        real_image_shell=real_shell,
        reciprocal_image_shell=reciprocal_shell,
        coordinate_unit_to_bohr=unit,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="INDEPENDENT-PERIODIC-EWALD-FIXTURE",
    )
    fixed_charge = FLiBePeriodicFixedChargeModel(
        model_id="FIXED-CHARGE-FIXTURE",
        ewald_model=FLiBePeriodicEwaldModel("COULOMB-EWALD-FIXTURE", ewald_parameters),
        short_range_model=FLiBePeriodicShortRangeModel(
            model_id="PUBLISHED-SHORT-RANGE",
            parameters=source,
            coordinate_unit_to_bohr=unit,
            image_shell=short_shell,
        ),
    )
    polarization = FLiBePeriodicPolarizationModel(
        model_id="STATIONARY-FLUORIDE-FIXTURE",
        parameters=source,
        ewald_parameters=ewald_parameters,
        damping_image_shell=damping_shell,
        stationarity_absolute_tolerance=STATIONARITY_ABSOLUTE_TOLERANCE,
    )
    return FLiBePeriodicPolarizableModel(
        model_id="PERIODIC-POLARIZABLE-FLIBE-FIXTURE",
        fixed_charge_model=fixed_charge,
        polarization_model=polarization,
    )


def _independent_energy(model, configuration):
    """Evaluate fixed-charge and reoptimized dipoles as separate calculations."""
    fixed = model.fixed_charge_model.evaluate(configuration)
    polarization = model.polarization_model.evaluate(configuration)
    return fsum((fixed.energy.total_energy, polarization.polarization_energy_hartree))


def _shift(configuration, atom, axis, displacement):
    positions = [list(p) for p in configuration.configuration.positions]
    positions[atom][axis] += displacement
    return _configuration(
        species=configuration.configuration.species,
        positions=positions,
        cell=configuration.configuration.cell,
        periodic=configuration.configuration.periodic,
    )


def _finite_difference_force(model, configuration, atom, axis):
    plus = _independent_energy(model, _shift(configuration, atom, axis, DERIVATIVE_STEP))
    minus = _independent_energy(model, _shift(configuration, atom, axis, -DERIVATIVE_STEP))
    return -(plus - minus) / (2.0 * DERIVATIVE_STEP)


def _assert_forces(actual, expected, tol=SYMMETRY_ABSOLUTE_TOLERANCE):
    assert len(actual) == len(expected)
    for observed, reference in zip(actual, expected, strict=True):
        assert observed == pytest.approx(reference, abs=tol, rel=0.0)


@pytest.fixture(scope="module")
def model():
    return _model()


@pytest.fixture(scope="module")
def result(model):
    return model.evaluate(_configuration())


def test_eight_terms_are_separate_and_equal_independent_component_energies(model, result):
    fixed = model.fixed_charge_model.evaluate(_configuration())
    polar = model.polarization_model.evaluate(_configuration())
    expected = fixed.energy_components_hartree + (
        ("polarization_self", polar.self_energy_hartree),
        ("polarization_charge_dipole", polar.charge_dipole_energy_hartree),
        ("polarization_dipole_dipole", polar.dipole_dipole_energy_hartree),
    )
    assert isinstance(result, FLiBePeriodicPolarizableResult)
    assert result.functional_id == POLARIZABLE_PERIODIC_FUNCTIONAL_ID
    assert tuple(name for name, _ in result.energy_components_hartree) == COMPONENT_NAMES
    assert result.energy_components_hartree == expected
    assert result.energy.total_energy == pytest.approx(fsum(v for _, v in expected), abs=1e-12)
    assert result.energy.total_energy == pytest.approx(
        fsum((fixed.energy.total_energy, polar.polarization_energy_hartree)), abs=1e-12
    )
    assert result.polarization_force_result.polarization_result == polar
    assert result.fixed_charge_result == fixed


def test_source_stoichiometry_provenance_and_stationary_fluoride_indices(result):
    assert result.configuration.composition().formula_unit_fractions == (2.0 / 3.0, 1.0 / 3.0)
    assert result.source_doi == SOURCE_DOI
    assert result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert result.coordinate_unit_to_bohr == 1.0
    assert result.max_stationarity_residual_atomic <= STATIONARITY_ABSOLUTE_TOLERANCE
    pol = result.polarization_force_result.polarization_result
    assert pol.polarizable_indices == (3, 4, 5, 6)
    assert pol.induced_dipoles_e_bohr[:3] == ((0.0, 0.0, 0.0),) * 3
    assert all(pair.provenance is ParameterProvenance.PRIMARY_SOURCE
               for pair in result.fixed_charge_result.short_range_result.parameters.pair_coefficients)


def test_polarization_atomic_partition_uses_stationary_dipoles(result):
    pol = result.polarization_force_result.polarization_result
    expected = tuple(-0.5 * fsum(mu[axis] * field[axis] for axis in range(3))
                     for mu, field in zip(pol.induced_dipoles_e_bohr,
                                          pol.charge_fields_atomic, strict=True))
    assert result.polarization_atomic_energies_hartree == pytest.approx(expected, abs=1e-12)
    assert expected[:3] == (0.0, 0.0, 0.0)
    assert fsum(expected) == pytest.approx(pol.polarization_energy_hartree, abs=1e-12)
    assert result.energy.total_energy == pytest.approx(fsum(result.energy.atomic_energies), abs=1e-12)
    for i in range(7):
        assert result.energy.atomic_energies[i] == pytest.approx(
            result.fixed_charge_result.energy.atomic_energies[i] + expected[i], abs=1e-12
        )


def test_combined_forces_are_the_sum_of_independently_evaluated_channels(model, result):
    fixed = model.fixed_charge_model.evaluate(_configuration())
    pol_result = result.polarization_force_result
    assert tuple(name for name, _ in pol_result.force_components) == (
        "charge_real", "charge_reciprocal", "charge_damping", "dipole_real", "dipole_reciprocal"
    )
    for i in range(7):
        for axis in range(3):
            assert result.forces.forces[i][axis] == pytest.approx(fsum((
                fixed.ewald_result.forces.forces[i][axis],
                fixed.short_range_result.forces.forces[i][axis],
                *(component.forces[i][axis] for _, component in pol_result.force_components),
            )), abs=1e-12)


def test_all_twenty_one_cartesian_forces_match_reoptimized_energy_gradient(model, result):
    configuration = _configuration()
    for atom in range(configuration.atom_count):
        for axis in range(3):
            expected = _finite_difference_force(model, configuration, atom, axis)
            assert result.forces.forces[atom][axis] == pytest.approx(
                expected, rel=0.0, abs=FORCE_ABSOLUTE_TOLERANCE
            )


def test_force_balance_for_fixed_polarization_and_combined_components(result):
    components = (
        result.fixed_charge_result.forces,
        result.polarization_force_result.polarization_forces,
        result.forces,
    )
    for force_state in components:
        for axis in range(3):
            assert abs(fsum(force[axis] for force in force_state.forces)) < 1e-10


def test_e3_rotation_and_reflection_preserve_energy_and_transform_forces(model, result):
    operations = (
        (lambda p: (-p[1] + 2.0, p[0] - 3.0, p[2] + 0.5),
         lambda v: (-v[1], v[0], v[2])),
        (lambda p: (-p[0] + 4.0, p[1] + 2.0, p[2] - 1.0),
         lambda v: (-v[0], v[1], v[2])),
    )
    for transform, linear in operations:
        transformed = _configuration(
            positions=tuple(transform(p) for p in POSITIONS),
            cell=tuple(linear(v) for v in CELL),
        )
        actual = model.evaluate(transformed)
        assert actual.energy.total_energy == pytest.approx(
            result.energy.total_energy, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE
        )
        _assert_forces(actual.forces.forces, tuple(linear(v) for v in result.forces.forces))
        assert actual.polarization_atomic_energies_hartree == pytest.approx(
            result.polarization_atomic_energies_hartree, abs=ENERGY_ABSOLUTE_TOLERANCE
        )


def test_species_position_permutation_preserves_energy_and_reorders_forces(model, result):
    order = (6, 2, 0, 4, 1, 5, 3)
    changed = _configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS[i] for i in order),
    )
    actual = model.evaluate(changed)
    assert actual.energy.total_energy == pytest.approx(result.energy.total_energy, abs=ENERGY_ABSOLUTE_TOLERANCE)
    assert actual.energy.atomic_energies == pytest.approx(
        tuple(result.energy.atomic_energies[i] for i in order), abs=ENERGY_ABSOLUTE_TOLERANCE
    )
    _assert_forces(actual.forces.forces, tuple(result.forces.forces[i] for i in order))


def test_coordinate_conversion_preserves_energy_and_scales_forces(model, result):
    ewald = replace(model.fixed_charge_model.ewald_model,
                    parameters=replace(model.fixed_charge_model.ewald_model.parameters,
                                       coordinate_unit_to_bohr=0.5))
    short_range = replace(model.fixed_charge_model.short_range_model, coordinate_unit_to_bohr=0.5)
    fixed = replace(model.fixed_charge_model, ewald_model=ewald, short_range_model=short_range)
    pol = replace(model.polarization_model, ewald_parameters=ewald.parameters)
    scaled = replace(model, fixed_charge_model=fixed, polarization_model=pol)
    configuration = _configuration(
        positions=tuple(tuple(2.0 * v for v in p) for p in POSITIONS),
        cell=tuple(tuple(2.0 * v for v in edge) for edge in CELL),
    )
    actual = scaled.evaluate(configuration)
    assert actual.energy.total_energy == pytest.approx(result.energy.total_energy, abs=ENERGY_ABSOLUTE_TOLERANCE)
    _assert_forces(actual.forces.forces, tuple(tuple(0.5 * v for v in force) for force in result.forces.forces))


def test_periodic_translation_of_one_fluoride_at_refined_shells():
    refined = _model(alpha=0.25, real_shell=3, reciprocal_shell=6,
                     short_shell=2, damping_shell=3)
    initial = refined.evaluate(_configuration())
    moved = list(POSITIONS)
    moved[3] = tuple(moved[3][i] + CELL[1][i] for i in range(3))
    translated = refined.evaluate(_configuration(positions=tuple(moved)))
    assert translated.energy.total_energy == pytest.approx(
        initial.energy.total_energy, rel=0.0, abs=3.0e-8
    )
    _assert_forces(translated.forces.forces, initial.forces.forces, tol=3.0e-8)


def test_replay_is_deterministic_and_results_immutable(model, result):
    assert result == model.evaluate(_configuration())
    with pytest.raises(FrozenInstanceError):
        result.model_id = "CHANGED"  # type: ignore[misc]


@pytest.mark.parametrize("field,invalid,error", (
    ("model_id", " ", ValueError),
    ("model_id", None, TypeError),
    ("fixed_charge_model", None, TypeError),
    ("polarization_model", None, TypeError),
))
def test_model_rejects_invalid_constructor_inputs(model, field, invalid, error):
    with pytest.raises(error):
        replace(model, **{field: invalid})


def test_model_rejects_mismatched_ewald_and_coefficient_contracts(model):
    changed_ewald = replace(model.polarization_model.ewald_parameters,
                            alpha_inverse_bohr=0.3)
    with pytest.raises(ValueError, match="Ewald parameters must agree"):
        replace(model, polarization_model=replace(
            model.polarization_model, ewald_parameters=changed_ewald
        ))
    source = model.polarization_model.parameters
    altered_source = replace(source, fluoride_polarizability_bohr3=8.0)
    with pytest.raises(ValueError, match="coefficient tables must agree"):
        replace(model, polarization_model=replace(
            model.polarization_model, parameters=altered_source
        ))


def test_evaluator_rejects_invalid_and_nonperiodic_configuration(model):
    with pytest.raises(TypeError, match="FLiBeConfiguration"):
        model.evaluate(None)
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(cell=None, periodic=(False, False, False)))
    with pytest.raises(ValueError, match="three periodic axes"):
        model.evaluate(_configuration(periodic=(True, False, True)))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        model.evaluate(_configuration(species=("Li", "Be", "F"), positions=POSITIONS[:3]))


def test_result_rejects_corrupted_energy_force_and_component_provenance(result):
    with pytest.raises(ValueError, match="functional identity"):
        replace(result, functional_id="OTHER")
    with pytest.raises(ValueError, match="total energy must sum"):
        replace(result, energy=EnergyState(result.energy.atomic_energies,
                                           result.energy.total_energy + 1.0))
    with pytest.raises(ValueError, match="polarization atomic energies"):
        replace(result, polarization_atomic_energies_hartree=(0.0,))
    with pytest.raises(ValueError, match="atomic energy must sum"):
        replace(result, energy=EnergyState((
            result.energy.atomic_energies[0] + 0.1,
            result.energy.atomic_energies[1] - 0.1,
            *result.energy.atomic_energies[2:],
        ), result.energy.total_energy))
    altered_forces = list(result.forces.forces)
    altered_forces[0] = (altered_forces[0][0] + 0.1, *altered_forces[0][1:])
    with pytest.raises(ValueError, match="total Cartesian forces must sum"):
        replace(result, forces=ForceState(tuple(altered_forces)))
    with pytest.raises(TypeError, match="fixed_charge_result"):
        replace(result, fixed_charge_result=None)
    with pytest.raises(TypeError, match="polarization_force_result"):
        replace(result, polarization_force_result=None)
