"""Independent FLiBe trajectory temperature and source-state qualification."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind, FLiBeReferenceObservable
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.trajectory_density import (
    FLiBeTrajectoryDensity,
    evaluate_flibe_trajectory_density,
)
from tr_eif.flibe.trajectory_state_correspondence import (
    BOLTZMANN_CONSTANT_J_PER_K,
    FLiBeDensitySourceCoordinates,
    FLiBePressureCoordinate,
    FLiBePressureRole,
    FLiBeTrajectoryStateCoordinates,
    compare_flibe_density_state_coordinates,
    evaluate_flibe_trajectory_state_coordinates,
    flibe_density_source_from_observable,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import InteractionGraph
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory


SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
POSITIONS = (
    (0.1, 0.1, 0.1),
    (0.6, 0.1, 0.1),
    (0.2, 0.6, 0.2),
    (0.3, 0.3, 0.7),
    (0.8, 0.3, 0.7),
    (0.4, 0.9, 1.1),
    (0.9, 0.7, 1.3),
)
CELL_EDGE_X = (2.0, 4.0, 6.0)
MASS_UNIT_KG = 1.0e-27
LENGTH_UNIT_M = 1.0e-10
TIME_UNIT_S = 1.0e-12
DEGREES_OF_FREEDOM = 21
PRESSURE_PA = 101325.0
NORMALIZATION = "mean-instantaneous-cell-density"
PROVENANCE = ParameterProvenance.TEST_FIXTURE
COMPOSITION = FLiBeComposition(2.0, 1.0)

# Independent analytic result: all seven atoms have velocity (s, 0, 0).
# The summed mass is 27 MD mass units and the Cartesian speed unit is 100 m/s.
EXPECTED_BASE_T_K = (
    27.0 * MASS_UNIT_KG * (LENGTH_UNIT_M / TIME_UNIT_S) ** 2
    / (DEGREES_OF_FREEDOM * 1.380649e-23)
)


def _state(index: int) -> MolecularDynamicsState:
    speed = float(index + 1)
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=POSITIONS,
            cell=(
                (CELL_EDGE_X[index], 0.0, 0.0),
                (0.0, 3.0, 0.0),
                (0.0, 0.0, 4.0),
            ),
            periodic=(True, True, True),
        ),
        velocities=((speed, 0.0, 0.0),) * len(SPECIES),
        masses=MASSES,
        step=index,
        time=0.25 * index,
    )


def _trajectory(
    states: tuple[MolecularDynamicsState, ...] | None = None,
) -> MolecularDynamicsTrajectory:
    sequence = tuple(_state(i) for i in range(3)) if states is None else states
    graph = InteractionGraph(node_count=len(SPECIES), edges=())
    zero_forces = ForceState(forces=((0.0, 0.0, 0.0),) * len(SPECIES))
    return MolecularDynamicsTrajectory(
        steps=tuple(
            MolecularDynamicsStepResult(
                previous=previous,
                current=current,
                graph_before=graph,
                graph_after=graph,
                forces_before=zero_forces,
                forces_after=zero_forces,
            )
            for previous, current in zip(sequence[:-1], sequence[1:], strict=True)
        )
    )


def _density(
    trajectory: MolecularDynamicsTrajectory,
    *,
    first_state_index: int = 0,
    stride: int = 1,
) -> FLiBeTrajectoryDensity:
    return evaluate_flibe_trajectory_density(
        trajectory,
        FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        model_id="TR-EIP-INDEPENDENT-FIXTURE",
        trajectory_id="MD-DENSITY-FIXTURE-001",
        provenance=PROVENANCE,
        mass_unit_to_kg=MASS_UNIT_KG,
        coordinate_unit_to_meter=LENGTH_UNIT_M,
        first_state_index=first_state_index,
        stride=stride,
    )


def _pressure(
    role: FLiBePressureRole = FLiBePressureRole.OBSERVED,
    pressure_pa: float = PRESSURE_PA,
) -> FLiBePressureCoordinate:
    return FLiBePressureCoordinate(
        pressure_pa=pressure_pa,
        role=role,
        method_id="PRESSURE-FIXTURE",
        source_id="SOURCE-PRESSURE-FIXTURE",
        provenance=PROVENANCE,
    )


def _coordinates(
    trajectory: MolecularDynamicsTrajectory | None = None,
    density: FLiBeTrajectoryDensity | None = None,
    *,
    degrees_of_freedom: int = DEGREES_OF_FREEDOM,
    time_unit_to_second: float = TIME_UNIT_S,
    physical_state_id: str = "liquid",
    physical_state_method_id: str = "STATE-FIXTURE",
    pressure: FLiBePressureCoordinate | None = None,
) -> FLiBeTrajectoryStateCoordinates:
    current = _trajectory() if trajectory is None else trajectory
    return evaluate_flibe_trajectory_state_coordinates(
        current,
        _density(current, stride=2) if density is None else density,
        degrees_of_freedom=degrees_of_freedom,
        time_unit_to_second=time_unit_to_second,
        physical_state_id=physical_state_id,
        physical_state_method_id=physical_state_method_id,
        pressure=pressure,
    )


def _source(**updates: object) -> FLiBeDensitySourceCoordinates:
    values: dict[str, object] = {
        "density_kg_m3": 780.0,
        "composition": COMPOSITION,
        "temperature_k": 5.0 * EXPECTED_BASE_T_K,
        "pressure_pa": PRESSURE_PA,
        "physical_state_id": "liquid",
        "normalization_id": NORMALIZATION,
        "evidence_kind": FLiBeEvidenceKind.EXPERIMENTAL,
        "source_id": "INDEPENDENT-DENSITY-FIXTURE",
        "method_id": "REFERENCE-TABLE-FIXTURE",
        "provenance": PROVENANCE,
    }
    values.update(updates)
    return FLiBeDensitySourceCoordinates(**values)


def _compare(
    *,
    model: FLiBeTrajectoryStateCoordinates | None = None,
    reference: FLiBeDensitySourceCoordinates | FLiBeReferenceObservable | None = None,
    temperature_tolerance_k: float = 1.0e-12,
    pressure_tolerance_pa: float = 0.0,
    normalization_id: str = NORMALIZATION,
):
    return compare_flibe_density_state_coordinates(
        _coordinates(pressure=_pressure()) if model is None else model,
        _source() if reference is None else reference,
        temperature_tolerance_k=temperature_tolerance_k,
        pressure_tolerance_pa=pressure_tolerance_pa,
        normalization_id=normalization_id,
    )


def test_temperature_uses_independently_computed_si_kinetic_energy() -> None:
    trajectory = _trajectory()
    result = _coordinates(trajectory, _density(trajectory))
    assert BOLTZMANN_CONSTANT_J_PER_K == 1.380649e-23
    assert result.density_trace.total_mass_kg == pytest.approx(27.0e-27)
    assert result.degrees_of_freedom == 21
    assert result.kinetic_temperature_k == pytest.approx(
        (EXPECTED_BASE_T_K, 4.0 * EXPECTED_BASE_T_K, 9.0 * EXPECTED_BASE_T_K),
        rel=1.0e-13,
    )
    assert result.mean_kinetic_temperature_k == pytest.approx(
        (14.0 / 3.0) * EXPECTED_BASE_T_K, rel=1.0e-13
    )
    assert result.pressure is None


def test_temperature_sampling_tracks_density_state_indices() -> None:
    result = _coordinates()
    assert tuple(sample.state_index for sample in result.density_trace.samples) == (0, 2)
    assert result.kinetic_temperature_k == pytest.approx(
        (EXPECTED_BASE_T_K, 9.0 * EXPECTED_BASE_T_K), rel=1.0e-13
    )
    assert result.mean_kinetic_temperature_k == pytest.approx(
        5.0 * EXPECTED_BASE_T_K, rel=1.0e-13
    )
    assert result.density_trace.mean_density_kg_m3 == pytest.approx(750.0)


def test_temperature_scales_with_declared_time_unit_and_freedom_count() -> None:
    baseline = _coordinates()
    longer_time = _coordinates(time_unit_to_second=2.0 * TIME_UNIT_S)
    fewer_degrees = _coordinates(degrees_of_freedom=7)
    assert longer_time.mean_kinetic_temperature_k == pytest.approx(
        baseline.mean_kinetic_temperature_k / 4.0
    )
    assert fewer_degrees.mean_kinetic_temperature_k == pytest.approx(
        baseline.mean_kinetic_temperature_k * 3.0
    )


def test_temperature_zero_velocity_is_distinct_from_missing_temperature() -> None:
    states = tuple(
        replace(_state(i), velocities=((0.0, 0.0, 0.0),) * len(SPECIES))
        for i in range(3)
    )
    trajectory = _trajectory(states)
    result = _coordinates(trajectory, _density(trajectory))
    assert result.kinetic_temperature_k == (0.0, 0.0, 0.0)
    assert result.mean_kinetic_temperature_k == 0.0


def test_pressure_provenance_remains_observed_or_control_target() -> None:
    observed = _pressure()
    target = _pressure(FLiBePressureRole.CONTROL_TARGET)
    assert observed.pressure_pa == PRESSURE_PA
    assert observed.role is FLiBePressureRole.OBSERVED
    assert target.role is FLiBePressureRole.CONTROL_TARGET
    assert target.source_id == "SOURCE-PRESSURE-FIXTURE"
    assert observed.provenance is PROVENANCE


def test_exact_source_coordinates_enable_signed_density_residual() -> None:
    result = _compare()
    assert result.coordinate_match
    assert all((result.composition_match, result.temperature_match,
                result.pressure_match, result.physical_state_match,
                result.normalization_match))
    assert result.temperature_difference_k == pytest.approx(0.0, abs=1.0e-12)
    assert result.pressure_difference_pa == 0.0
    assert result.density_residual_kg_m3 == pytest.approx(-30.0, abs=1.0e-11)
    assert result.reference.evidence_kind is FLiBeEvidenceKind.EXPERIMENTAL


def test_first_principles_source_uses_same_explicit_matching_contract() -> None:
    reference = _source(evidence_kind=FLiBeEvidenceKind.FIRST_PRINCIPLES)
    result = _compare(reference=reference)
    assert result.coordinate_match
    assert result.reference.evidence_kind is FLiBeEvidenceKind.FIRST_PRINCIPLES
    assert result.density_residual_kg_m3 == pytest.approx(-30.0)


@pytest.mark.parametrize(
    ("field", "value", "failed_flag"),
    (
        ("composition", FLiBeComposition(0.67, 0.33), "composition_match"),
        ("composition", FLiBeComposition(0.6642, 0.3358), "composition_match"),
        ("temperature_k", 5.0 * EXPECTED_BASE_T_K + 0.25, "temperature_match"),
        ("pressure_pa", PRESSURE_PA + 10.0, "pressure_match"),
        ("physical_state_id", "solid", "physical_state_match"),
        ("physical_state_id", None, "physical_state_match"),
        ("normalization_id", "density-at-mean-volume", "normalization_match"),
    ),
)
def test_mismatched_source_coordinates_preserve_individual_flags(
    field: str, value: object, failed_flag: str
) -> None:
    result = _compare(reference=_source(**{field: value}))
    assert not result.coordinate_match
    assert not getattr(result, failed_flag)
    with pytest.raises(ValueError, match="matched state coordinates"):
        _ = result.density_residual_kg_m3


@pytest.mark.parametrize("pressure", (None, _pressure(FLiBePressureRole.CONTROL_TARGET)))
def test_unknown_or_control_target_pressure_cannot_match_observation(
    pressure: FLiBePressureCoordinate | None,
) -> None:
    result = _compare(model=_coordinates(pressure=pressure))
    assert result.composition_match
    assert result.temperature_match
    assert not result.pressure_match
    assert not result.coordinate_match
    assert result.pressure_difference_pa is None
    with pytest.raises(ValueError, match="matched state coordinates"):
        _ = result.density_residual_kg_m3


def test_missing_aimd_pressure_and_state_are_preserved_as_unknown() -> None:
    source = _source(
        evidence_kind=FLiBeEvidenceKind.FIRST_PRINCIPLES,
        pressure_pa=None,
        physical_state_id=None,
    )
    assert source.pressure_pa is None
    assert source.physical_state_id is None
    result = _compare(reference=source)
    assert not result.pressure_match
    assert not result.physical_state_match
    assert result.pressure_difference_pa is None
    assert not result.coordinate_match


def test_pressure_differences_and_declared_threshold_boundaries() -> None:
    source = _source(pressure_pa=PRESSURE_PA + 5.0)
    passed = _compare(reference=source, pressure_tolerance_pa=5.0)
    failed = _compare(reference=source, pressure_tolerance_pa=4.0)
    assert passed.pressure_match
    assert passed.coordinate_match
    assert passed.pressure_difference_pa == -5.0
    assert not failed.pressure_match
    assert not failed.coordinate_match


def test_temperature_difference_and_predeclared_tolerance() -> None:
    source = _source(temperature_k=5.0 * EXPECTED_BASE_T_K + 0.25)
    passed = _compare(reference=source, temperature_tolerance_k=0.25000000001)
    failed = _compare(reference=source, temperature_tolerance_k=0.24999999999)
    assert passed.temperature_match
    assert not failed.temperature_match
    assert passed.temperature_difference_k == pytest.approx(-0.25, abs=1.0e-12)


def test_typed_reference_adapter_retains_source_and_method_identity() -> None:
    reference = FLiBeReferenceObservable(
        observable_id="mass_density",
        composition=COMPOSITION,
        thermodynamic_state=FLiBeThermodynamicState(
            temperature=5.0 * EXPECTED_BASE_T_K, pressure=PRESSURE_PA
        ),
        physical_state_id="liquid",
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        values=(780.0,),
        value_unit="kg/m^3",
        normalization_id=NORMALIZATION,
        source_id="INDEPENDENT-TYPED-FIXTURE",
        method_id="DENSITY-TABLE-FIXTURE",
        provenance=PROVENANCE,
    )
    source = flibe_density_source_from_observable(reference)
    assert source.source_id == reference.source_id
    assert source.method_id == reference.method_id
    assert source.provenance == reference.provenance
    assert source.temperature_k == reference.thermodynamic_state.temperature
    assert source.pressure_pa == reference.thermodynamic_state.pressure
    assert _compare(reference=reference).coordinate_match
    assert _compare(reference=reference).density_residual_kg_m3 == pytest.approx(-30.0)


@pytest.mark.parametrize(
    ("changes", "message"),
    (
        ({"observable_id": "structure_factor"}, "mass_density"),
        ({"value_unit": "g/cm^3"}, "kg/m\\^3"),
        ({"values": (780.0, 781.0)}, "one scalar density"),
        ({"axis": (1000.0,), "axis_unit": "K"}, "one scalar density"),
    ),
)
def test_typed_reference_adapter_rejects_different_observable_contract(
    changes: dict[str, object], message: str
) -> None:
    arguments: dict[str, object] = {
        "observable_id": "mass_density",
        "composition": COMPOSITION,
        "thermodynamic_state": FLiBeThermodynamicState(1000.0, PRESSURE_PA),
        "physical_state_id": "liquid",
        "evidence_kind": FLiBeEvidenceKind.EXPERIMENTAL,
        "values": (780.0,),
        "value_unit": "kg/m^3",
        "normalization_id": NORMALIZATION,
        "source_id": "TYPED-FIXTURE",
        "method_id": "REFERENCE-FIXTURE",
        "provenance": PROVENANCE,
    }
    arguments.update(changes)
    with pytest.raises(ValueError, match=message):
        flibe_density_source_from_observable(FLiBeReferenceObservable(**arguments))


def test_source_uncertainty_fields_preserve_units_and_zero_uncertainty() -> None:
    source = _source(
        density_standard_uncertainty_kg_m3=2.0,
        temperature_standard_uncertainty_k=0.1,
        pressure_standard_uncertainty_pa=1000.0,
        bef2_fraction_standard_uncertainty=0.0005,
    )
    assert source.density_standard_uncertainty_kg_m3 == 2.0
    assert source.temperature_standard_uncertainty_k == 0.1
    assert source.pressure_standard_uncertainty_pa == 1000.0
    assert source.bef2_fraction_standard_uncertainty == 0.0005
    assert _compare(reference=source).coordinate_match
    assert _source(density_standard_uncertainty_kg_m3=0.0).density_standard_uncertainty_kg_m3 == 0.0


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("density_kg_m3", 0.0, ValueError),
        ("density_kg_m3", float("nan"), ValueError),
        ("temperature_k", 0.0, ValueError),
        ("temperature_k", float("inf"), ValueError),
        ("pressure_pa", -1.0, ValueError),
        ("pressure_pa", float("nan"), ValueError),
        ("pressure_pa", False, TypeError),
        ("normalization_id", " ", ValueError),
        ("source_id", " untrimmed ", ValueError),
        ("method_id", "", ValueError),
        ("evidence_kind", "EXPERIMENTAL", TypeError),
        ("provenance", "TEST_FIXTURE", TypeError),
        ("density_standard_uncertainty_kg_m3", -0.1, ValueError),
        ("temperature_standard_uncertainty_k", float("nan"), ValueError),
        ("pressure_standard_uncertainty_pa", -10.0, ValueError),
        ("bef2_fraction_standard_uncertainty", 1.1, ValueError),
        ("bef2_fraction_standard_uncertainty", True, TypeError),
    ),
)
def test_source_rejects_invalid_physical_or_provenance_metadata(
    field: str, invalid: object, error: type[Exception]
) -> None:
    with pytest.raises(error):
        _source(**{field: invalid})


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("pressure_pa", -1.0, ValueError),
        ("pressure_pa", float("inf"), ValueError),
        ("pressure_pa", True, TypeError),
        ("role", "OBSERVED", TypeError),
        ("method_id", "bad ", ValueError),
        ("source_id", "", ValueError),
        ("provenance", "TEST_FIXTURE", TypeError),
    ),
)
def test_pressure_record_validates_observation_provenance(
    field: str, invalid: object, error: type[Exception]
) -> None:
    arguments: dict[str, object] = {
        "pressure_pa": PRESSURE_PA,
        "role": FLiBePressureRole.OBSERVED,
        "method_id": "PRESSURE-FIXTURE",
        "source_id": "SOURCE-PRESSURE-FIXTURE",
        "provenance": PROVENANCE,
    }
    arguments[field] = invalid
    with pytest.raises(error):
        FLiBePressureCoordinate(**arguments)


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("degrees_of_freedom", 0, ValueError),
        ("degrees_of_freedom", 22, ValueError),
        ("degrees_of_freedom", True, ValueError),
        ("time_unit_to_second", 0.0, ValueError),
        ("time_unit_to_second", float("nan"), ValueError),
        ("time_unit_to_second", False, TypeError),
        ("physical_state_id", "liquid ", ValueError),
        ("physical_state_method_id", "", ValueError),
    ),
)
def test_trajectory_state_rejects_invalid_axes_and_units(
    field: str, invalid: object, error: type[Exception]
) -> None:
    arguments: dict[str, object] = {
        "degrees_of_freedom": DEGREES_OF_FREEDOM,
        "time_unit_to_second": TIME_UNIT_S,
        "physical_state_id": "liquid",
        "physical_state_method_id": "STATE-FIXTURE",
    }
    arguments[field] = invalid
    with pytest.raises(error):
        _coordinates(**arguments)


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("temperature_tolerance_k", -0.1, ValueError),
        ("temperature_tolerance_k", float("inf"), ValueError),
        ("temperature_tolerance_k", False, TypeError),
        ("pressure_tolerance_pa", -0.1, ValueError),
        ("pressure_tolerance_pa", float("nan"), ValueError),
        ("normalization_id", " ", ValueError),
    ),
)
def test_comparison_rejects_invalid_predeclared_criteria(
    field: str, invalid: object, error: type[Exception]
) -> None:
    arguments: dict[str, object] = {
        "temperature_tolerance_k": 1.0e-12,
        "pressure_tolerance_pa": 0.0,
        "normalization_id": NORMALIZATION,
    }
    arguments[field] = invalid
    with pytest.raises(error):
        _compare(**arguments)


def test_comparison_rejects_untyped_inputs() -> None:
    with pytest.raises(TypeError, match="model must be"):
        compare_flibe_density_state_coordinates(
            None, _source(), normalization_id=NORMALIZATION
        )
    with pytest.raises(TypeError, match="typed FLiBe density source"):
        _compare(reference=object())
    with pytest.raises(TypeError, match="observable must be"):
        flibe_density_source_from_observable(None)


def test_mismatched_density_sample_time_rejected_before_temperature() -> None:
    trajectory = _trajectory()
    density = _density(trajectory, stride=2)
    sample = replace(density.samples[1], md_time=0.625)
    changed = replace(density, samples=(density.samples[0], sample))
    with pytest.raises(ValueError, match="step/time coordinates differ"):
        _coordinates(trajectory, changed)


def test_mismatched_density_cell_volume_rejected_before_temperature() -> None:
    trajectory = _trajectory()
    density = _density(trajectory, stride=2)
    sample = replace(density.samples[1], cell_volume_m3=1.5 * density.samples[1].cell_volume_m3)
    changed = replace(density, samples=(density.samples[0], sample))
    with pytest.raises(ValueError, match="cell volumes differ"):
        _coordinates(trajectory, changed)


def test_density_state_index_outside_trajectory_rejected() -> None:
    trajectory = _trajectory()
    density = _density(trajectory, stride=2)
    sample = replace(density.samples[1], state_index=3)
    changed = replace(density, samples=(density.samples[0], sample))
    with pytest.raises(ValueError, match="index exceeds trajectory length"):
        _coordinates(trajectory, changed)


def test_sampled_state_must_remain_periodic() -> None:
    states = tuple(_state(i) for i in range(3))
    changed = replace(
        states[2], configuration=replace(states[2].configuration, periodic=(True, True, False))
    )
    with pytest.raises(ValueError, match="three periodic axes"):
        _coordinates(_trajectory(states[:2] + (changed,)), _density(_trajectory()))


def test_density_mass_inventory_mismatch_is_detected() -> None:
    states = tuple(_state(i) for i in range(3))
    changed = replace(states[2], masses=MASSES[:-1] + (5.25,))
    with pytest.raises(ValueError, match="mass inventories differ"):
        _coordinates(_trajectory(states[:2] + (changed,)), _density(_trajectory()))


def test_replay_and_frozen_state_are_deterministic() -> None:
    first = _coordinates(pressure=_pressure())
    second = _coordinates(pressure=_pressure())
    assert first == second
    assert _compare(model=first) == _compare(model=second)
    with pytest.raises(FrozenInstanceError):
        first.physical_state_id = "solid"  # type: ignore[misc]
