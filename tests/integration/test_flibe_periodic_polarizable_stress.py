"""Independent homogeneous-strain stress contracts for periodic FLiBe."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import CellStrainDifferentiation, StressState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import (
    FLiBeEwaldParameters,
    FLiBePeriodicEwaldModel,
)
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_stress import (
    FLiBePeriodicPolarizableStressResult,
    FLiBePeriodicStrainSample,
    evaluate_flibe_periodic_polarizable_stress,
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
COMPONENTS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
STRESS_STEP = 2.0e-5
INDEPENDENT_STEP = 4.0e-5
STRESS_ABSOLUTE_TOLERANCE = 3.0e-9
SYMMETRY_ABSOLUTE_TOLERANCE = 4.0e-9
ENERGY_ABSOLUTE_TOLERANCE = 2.0e-10


def _configuration(species=SPECIES, positions=POSITIONS, cell=CELL,
                   periodic=(True, True, True)) -> FLiBeConfiguration:
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(x) for x in p) for p in positions),
        cell=None if cell is None else tuple(tuple(float(x) for x in v) for v in cell),
        periodic=periodic,
    ))


def _model(*, unit=1.0, alpha=0.25, real_shell=1, reciprocal_shell=3,
           short_shell=1, damping_shell=1) -> FLiBePeriodicPolarizableModel:
    source = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=alpha,
        real_image_shell=real_shell,
        reciprocal_image_shell=reciprocal_shell,
        coordinate_unit_to_bohr=unit,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="PERIODIC-STRESS-EWALD-FIXTURE",
    )
    fixed = FLiBePeriodicFixedChargeModel(
        model_id="PERIODIC-STRESS-FIXED-CHARGE",
        ewald_model=FLiBePeriodicEwaldModel("PERIODIC-STRESS-COULOMB", ewald),
        short_range_model=FLiBePeriodicShortRangeModel(
            model_id="PERIODIC-STRESS-SHORT-RANGE",
            parameters=source,
            coordinate_unit_to_bohr=unit,
            image_shell=short_shell,
        ),
    )
    polarized = FLiBePeriodicPolarizationModel(
        model_id="PERIODIC-STRESS-POLARIZATION",
        parameters=source,
        ewald_parameters=ewald,
        damping_image_shell=damping_shell,
        stationarity_absolute_tolerance=1.0e-10,
    )
    return FLiBePeriodicPolarizableModel(
        model_id="PERIODIC-STRESS-COMBINED",
        fixed_charge_model=fixed,
        polarization_model=polarized,
    )


def _affine(configuration, matrix):
    """Apply an independently specified Cartesian affine map to atoms and cell."""
    atomic = configuration.configuration

    def transform(vector):
        return tuple(
            fsum(matrix[a][b] * vector[b] for b in range(3))
            for a in range(3)
        )

    return _configuration(
        species=atomic.species,
        positions=tuple(transform(v) for v in atomic.positions),
        cell=tuple(transform(v) for v in atomic.cell),
        periodic=atomic.periodic,
    )


def _strain(configuration, component, displacement):
    """Generate I+epsilon, with symmetric engineering shear s/2."""
    a, b = component
    matrix = [[float(i == j) for j in range(3)] for i in range(3)]
    if a == b:
        matrix[a][a] += displacement
    else:
        matrix[a][b] += 0.5 * displacement
        matrix[b][a] += 0.5 * displacement
    return _affine(configuration, matrix)


def _separate_energies(model, configuration):
    """Evaluate independently bound fixed-charge and relaxed-dipole energies."""
    fixed = model.fixed_charge_model.evaluate(configuration)
    polarized = model.polarization_model.evaluate(configuration)
    return fixed.energy.total_energy, polarized.polarization_energy_hartree


def _direct_stress(model, configuration, component, step=INDEPENDENT_STEP):
    """Compute separate energy derivatives without the stress implementation."""
    plus = _separate_energies(model, _strain(configuration, component, step))
    minus = _separate_energies(model, _strain(configuration, component, -step))
    volume_bohr3 = 18.0**3 * model.fixed_charge_model.ewald_model.parameters.coordinate_unit_to_bohr**3
    return tuple((p - m) / (2.0 * step * volume_bohr3)
                 for p, m in zip(plus, minus, strict=True))


def _rotate(vector):
    return (-vector[1], vector[0], vector[2])


def _reflect(vector):
    return (-vector[0], vector[1], vector[2])


def _tensor_transform(tensor, rotation):
    """Calculate Q sigma Q^T through transformed Cartesian basis vectors."""
    basis = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    q = tuple(rotation(v) for v in basis)
    return tuple(tuple(
        fsum(q[k][i] * tensor[k][l] * q[l][j] for k in range(3) for l in range(3))
        for j in range(3)) for i in range(3))


def _assert_stress(actual, expected, tolerance=SYMMETRY_ABSOLUTE_TOLERANCE):
    for row, reference in zip(actual.tensor, getattr(expected, "tensor", expected), strict=True):
        assert row == pytest.approx(reference, rel=0.0, abs=tolerance)


@pytest.fixture(scope="module")
def model():
    return _model()


@pytest.fixture(scope="module")
def reference_configuration():
    return _configuration()


@pytest.fixture(scope="module")
def result(model, reference_configuration):
    return evaluate_flibe_periodic_polarizable_stress(
        model, reference_configuration, CellStrainDifferentiation(step=STRESS_STEP)
    )


def test_registered_source_configuration_and_reference_volume(result):
    assert isinstance(result, FLiBePeriodicPolarizableStressResult)
    assert result.configuration.species == result.reference.configuration.species
    assert result.configuration.composition().formula_unit_fractions == (2.0/3.0, 1.0/3.0)
    assert result.source_doi == SOURCE_DOI
    assert result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert result.reference_volume_bohr3 == pytest.approx(5832.0, rel=0.0, abs=1.0e-12)
    assert result.differentiation.step == STRESS_STEP
    assert result.reference.max_stationarity_residual_atomic <= 1.0e-10
    assert all(pair.provenance is ParameterProvenance.PRIMARY_SOURCE
               for pair in result.reference.fixed_charge_result.short_range_result.parameters.pair_coefficients)


def test_all_six_tensor_components_and_source_energies_are_registered(model, reference_configuration, result):
    assert tuple(sample.components for sample in result.samples) == COMPONENTS
    for sample in result.samples:
        assert isinstance(sample, FLiBePeriodicStrainSample)
        plus = _separate_energies(model, _strain(reference_configuration, sample.components, STRESS_STEP))
        minus = _separate_energies(model, _strain(reference_configuration, sample.components, -STRESS_STEP))
        assert (sample.fixed_plus_hartree, sample.polarization_plus_hartree) == pytest.approx(
            plus, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE)
        assert (sample.fixed_minus_hartree, sample.polarization_minus_hartree) == pytest.approx(
            minus, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE)
        assert all(isfinite(value) for value in (
            sample.fixed_plus_hartree, sample.fixed_minus_hartree,
            sample.polarization_plus_hartree, sample.polarization_minus_hartree,
        ))


@pytest.mark.parametrize("component", COMPONENTS)
def test_six_stress_components_match_independent_relaxed_energy_derivative(
    model, reference_configuration, result, component
):
    fixed, polar = _direct_stress(model, reference_configuration, component)
    a, b = component
    assert result.fixed_charge_stress.tensor[a][b] == pytest.approx(
        fixed, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)
    assert result.polarization_stress.tensor[a][b] == pytest.approx(
        polar, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)
    assert result.total_stress.tensor[a][b] == pytest.approx(
        fixed + polar, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)


def test_strain_tensor_is_symmetric_and_components_sum_exactly_by_contract(result):
    for state in (result.fixed_charge_stress, result.polarization_stress, result.total_stress):
        assert state.is_symmetric
    for a in range(3):
        for b in range(3):
            assert result.total_stress.tensor[a][b] == pytest.approx(
                result.fixed_charge_stress.tensor[a][b] + result.polarization_stress.tensor[a][b],
                rel=0.0, abs=1.0e-12)
    assert result.potential_pressure_hartree_per_bohr3 == pytest.approx(
        -fsum(result.total_stress.tensor[i][i] for i in range(3))/3.0,
        rel=0.0, abs=1.0e-14)


def test_independent_isotropic_volume_derivative_matches_stress_trace(model, reference_configuration, result):
    h = INDEPENDENT_STEP
    expansion = [[1.0+h, 0.0, 0.0], [0.0, 1.0+h, 0.0], [0.0, 0.0, 1.0+h]]
    compression = [[1.0-h, 0.0, 0.0], [0.0, 1.0-h, 0.0], [0.0, 0.0, 1.0-h]]
    plus = _separate_energies(model, _affine(reference_configuration, expansion))
    minus = _separate_energies(model, _affine(reference_configuration, compression))
    for channel, stress in ((0, result.fixed_charge_stress), (1, result.polarization_stress)):
        direct = (plus[channel]-minus[channel])/(2.0*h*result.reference_volume_bohr3)
        assert stress.trace == pytest.approx(direct, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)
    total_derivative = (fsum(plus)-fsum(minus))/(2.0*h*result.reference_volume_bohr3)
    assert result.potential_pressure_hartree_per_bohr3 == pytest.approx(
        -total_derivative/3.0, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)


def test_off_diagonal_engineering_shear_half_factor(model, reference_configuration, result):
    a, b = (0, 1)
    h = INDEPENDENT_STEP
    direct_fixed, direct_pol = _direct_stress(model, reference_configuration, (a, b), h)
    assert result.fixed_charge_stress.tensor[a][b] == pytest.approx(
        direct_fixed, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)
    assert result.polarization_stress.tensor[a][b] == pytest.approx(
        direct_pol, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)
    assert result.total_stress.tensor[a][b] == result.total_stress.tensor[b][a]
    assert abs(result.total_stress.tensor[a][b]) > 1.0e-8


def test_central_difference_refinement_preserves_predeclared_tolerances(model, reference_configuration, result):
    finer = evaluate_flibe_periodic_polarizable_stress(
        model, reference_configuration, CellStrainDifferentiation(step=STRESS_STEP/2.0))
    for first, second in (
        (result.fixed_charge_stress, finer.fixed_charge_stress),
        (result.polarization_stress, finer.polarization_stress),
        (result.total_stress, finer.total_stress),
    ):
        _assert_stress(first, second, tolerance=STRESS_ABSOLUTE_TOLERANCE)
    assert finer.reference.energy == result.reference.energy


def test_e3_quarter_turn_and_reflection_covariance(model, reference_configuration, result):
    for operation in (_rotate, _reflect):
        basis = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        columns = tuple(operation(v) for v in basis)
        matrix = tuple(tuple(columns[b][a] for b in range(3)) for a in range(3))
        rotated = _affine(reference_configuration, matrix)
        transformed = evaluate_flibe_periodic_polarizable_stress(
            model, rotated, CellStrainDifferentiation(step=STRESS_STEP))
        assert transformed.reference.energy.total_energy == pytest.approx(
            result.reference.energy.total_energy, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE)
        for before, after in (
            (result.fixed_charge_stress, transformed.fixed_charge_stress),
            (result.polarization_stress, transformed.polarization_stress),
            (result.total_stress, transformed.total_stress),
        ):
            _assert_stress(after, _tensor_transform(before.tensor, operation))
        assert transformed.potential_pressure_hartree_per_bohr3 == pytest.approx(
            result.potential_pressure_hartree_per_bohr3, rel=0.0, abs=STRESS_ABSOLUTE_TOLERANCE)


def test_atom_permutation_preserves_stress(model, reference_configuration, result):
    order = (6, 2, 0, 4, 1, 5, 3)
    changed = _configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS[i] for i in order),
    )
    evaluated = evaluate_flibe_periodic_polarizable_stress(
        model, changed, CellStrainDifferentiation(step=STRESS_STEP))
    for first, second in (
        (result.fixed_charge_stress, evaluated.fixed_charge_stress),
        (result.polarization_stress, evaluated.polarization_stress),
        (result.total_stress, evaluated.total_stress),
    ):
        _assert_stress(first, second)


def test_length_conversion_preserves_physical_stress(model, reference_configuration, result):
    unit = 0.5
    ewald = replace(model.fixed_charge_model.ewald_model,
                    parameters=replace(model.fixed_charge_model.ewald_model.parameters,
                                       coordinate_unit_to_bohr=unit))
    short = replace(model.fixed_charge_model.short_range_model, coordinate_unit_to_bohr=unit)
    fixed = replace(model.fixed_charge_model, ewald_model=ewald, short_range_model=short)
    polarization = replace(model.polarization_model, ewald_parameters=ewald.parameters)
    equivalent_model = replace(model, fixed_charge_model=fixed, polarization_model=polarization)
    equivalent_state = _configuration(
        positions=tuple(tuple(2.0*v for v in p) for p in POSITIONS),
        cell=tuple(tuple(2.0*v for v in edge) for edge in CELL),
    )
    scaled = evaluate_flibe_periodic_polarizable_stress(
        equivalent_model, equivalent_state, CellStrainDifferentiation(step=STRESS_STEP))
    assert scaled.reference_volume_bohr3 == pytest.approx(result.reference_volume_bohr3, rel=0.0, abs=1e-12)
    assert scaled.reference.energy.total_energy == pytest.approx(result.reference.energy.total_energy, abs=ENERGY_ABSOLUTE_TOLERANCE)
    _assert_stress(scaled.total_stress, result.total_stress, tolerance=STRESS_ABSOLUTE_TOLERANCE)
    _assert_stress(scaled.polarization_stress, result.polarization_stress, tolerance=STRESS_ABSOLUTE_TOLERANCE)


def test_deterministic_replay_and_immutable_stress_samples(model, reference_configuration, result):
    replay = evaluate_flibe_periodic_polarizable_stress(
        model, reference_configuration, CellStrainDifferentiation(step=STRESS_STEP))
    assert replay == result
    with pytest.raises(FrozenInstanceError):
        result.reference_volume_bohr3 = 1.0  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.samples[0].fixed_plus_hartree = 0.0  # type: ignore[misc]


@pytest.mark.parametrize("invalid", (None, "MODEL", 123))
def test_model_type_is_verified(invalid):
    with pytest.raises(TypeError, match="FLiBePeriodicPolarizableModel"):
        evaluate_flibe_periodic_polarizable_stress(
            invalid, _configuration(), CellStrainDifferentiation(step=STRESS_STEP))


@pytest.mark.parametrize("invalid", (None, "CONFIGURATION", 23))
def test_configuration_type_is_verified(invalid, model):
    with pytest.raises(TypeError, match="FLiBeConfiguration"):
        evaluate_flibe_periodic_polarizable_stress(
            model, invalid, CellStrainDifferentiation(step=STRESS_STEP))


def test_strain_policy_requires_typed_positive_subunit_step(model):
    with pytest.raises(TypeError, match="CellStrainDifferentiation"):
        evaluate_flibe_periodic_polarizable_stress(model, _configuration(), None)
    with pytest.raises(ValueError, match="smaller than one"):
        evaluate_flibe_periodic_polarizable_stress(
            model, _configuration(), CellStrainDifferentiation(step=1.0))
    with pytest.raises(ValueError, match="smaller than one"):
        evaluate_flibe_periodic_polarizable_stress(
            model, _configuration(), CellStrainDifferentiation(step=2.0))
    with pytest.raises(ValueError, match="step must be positive"):
        CellStrainDifferentiation(step=0.0)


def test_periodicity_and_composition_are_checked(model):
    with pytest.raises(ValueError, match="three periodic axes"):
        evaluate_flibe_periodic_polarizable_stress(
            model, _configuration(cell=None, periodic=(False, False, False)),
            CellStrainDifferentiation(step=STRESS_STEP))
    with pytest.raises(ValueError, match="three periodic axes"):
        evaluate_flibe_periodic_polarizable_stress(
            model, _configuration(periodic=(True, False, True)),
            CellStrainDifferentiation(step=STRESS_STEP))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        evaluate_flibe_periodic_polarizable_stress(
            model, _configuration(species=("Li", "Be", "F"), positions=POSITIONS[:3]),
            CellStrainDifferentiation(step=STRESS_STEP))


def test_result_contract_rejects_missing_and_reordered_samples(result):
    with pytest.raises(ValueError, match="six strain components"):
        replace(result, samples=result.samples[:-1])
    with pytest.raises(ValueError, match="canonical tensor order"):
        replace(result, samples=tuple(reversed(result.samples)))
    with pytest.raises(TypeError, match="FLiBePeriodicStrainSample"):
        replace(result, samples=(object(), *result.samples[1:]))
    with pytest.raises(ValueError, match="canonical tensor pair"):
        replace(result.samples[0], components=(2, 0))
    with pytest.raises(ValueError, match="fixed_plus_hartree"):
        replace(result.samples[0], fixed_plus_hartree=float("nan"))


def test_result_contract_rejects_corrupted_tensors_and_derivatives(result):
    with pytest.raises(TypeError, match="symmetric StressState"):
        replace(result, total_stress=None)
    with pytest.raises(TypeError, match="symmetric StressState"):
        replace(result, total_stress=StressState((
            (1., 2., 0.), (3., 0., 0.), (0., 0., 0.))))
    changed = list(result.total_stress.tensor)
    changed[0] = (changed[0][0] + 1.0e-3, *changed[0][1:])
    with pytest.raises(ValueError, match="strain-energy derivatives"):
        replace(result, total_stress=StressState(tuple(changed)))
    with pytest.raises(ValueError, match="strain-energy derivatives"):
        replace(result, samples=(
            replace(result.samples[0], fixed_plus_hartree=result.samples[0].fixed_plus_hartree + 0.1),
            *result.samples[1:],
        ))
    with pytest.raises(TypeError, match="FLiBePeriodicPolarizableResult"):
        replace(result, reference=None)


def test_result_volume_must_be_positive(result):
    with pytest.raises(ValueError, match="reference_volume_bohr3"):
        replace(result, reference_volume_bohr3=0.0)
    with pytest.raises(ValueError, match="reference_volume_bohr3"):
        replace(result, reference_volume_bohr3=float("inf"))
