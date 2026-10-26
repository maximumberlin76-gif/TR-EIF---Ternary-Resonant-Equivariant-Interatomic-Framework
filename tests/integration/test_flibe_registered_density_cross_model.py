"""Independent FLiBe MD-to-source density comparison qualification."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import sqrt
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind
from tr_eif.flibe.registered_density_cross_model import (
    MODEL_DENSITY_STATISTIC,
    FLiBeDensityObservableMapping,
    FLiBeRegisteredDensityComparison,
    FLiBeRegisteredDensityComparisonRow,
    FLiBeRegisteredDensityRecord,
    compare_flibe_registered_density_records,
)
from tr_eif.flibe.registered_density_sources import load_flibe_density_source_records
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_state_correspondence import (
    FLiBeDensitySourceCoordinates,
    FLiBePressureCoordinate,
    FLiBePressureRole,
    FLiBeTrajectoryStateCoordinates,
    compare_flibe_density_state_coordinates,
    evaluate_flibe_trajectory_state_coordinates,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import InteractionGraph
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory


ROOT = Path(__file__).resolve().parents[2]
VIDRIO = ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
BARAL = ROOT / "data/reference/flibe_baral_2021_aimd_density.json"

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
POSITIONS = (
    (0.1, 0.1, 0.1), (0.6, 0.1, 0.1), (0.2, 0.6, 0.2),
    (0.3, 0.3, 0.7), (0.8, 0.3, 0.7), (0.4, 0.9, 1.1),
    (0.9, 0.7, 1.3),
)
MASS_UNIT_KG = 1.0e-27
LENGTH_UNIT_M = 1.0e-10
TIME_UNIT_S = 1.0e-12
PRESSURE_PA = 101325.0
NORMALIZATION = "source-reported-mass-density"
SYNTHETIC_DATASET = "TR-EIF-ANALYTIC-DENSITY-FIXTURE"
SYNTHETIC_DIGEST = "0123456789abcdef" * 4
PROVENANCE = ParameterProvenance.TEST_FIXTURE

# Independently calculated from M=27 mass units and speeds 1 and 3 MD units.
# Selected cells have volumes 24 and 72 coordinate units: rho=(1125+375)/2.
BASE_KINETIC_T = (
    27.0 * MASS_UNIT_KG * (LENGTH_UNIT_M / TIME_UNIT_S) ** 2
    / (21.0 * 1.380649e-23)
)
EXPECTED_TEMPERATURE_K = 5.0 * BASE_KINETIC_T
EXPECTED_DENSITY_KG_M3 = 750.0


def _state(index: int) -> MolecularDynamicsState:
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=POSITIONS,
            cell=((2.0 * (index + 1), 0.0, 0.0),
                  (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)),
            periodic=(True, True, True),
        ),
        velocities=((float(index + 1), 0.0, 0.0),) * len(SPECIES),
        masses=MASSES,
        step=index,
        time=0.25 * index,
    )


def _trajectory() -> MolecularDynamicsTrajectory:
    states = tuple(_state(index) for index in range(3))
    graph = InteractionGraph(node_count=len(SPECIES), edges=())
    forces = ForceState(forces=((0.0, 0.0, 0.0),) * len(SPECIES))
    return MolecularDynamicsTrajectory(
        steps=tuple(
            MolecularDynamicsStepResult(
                previous=before,
                current=after,
                graph_before=graph,
                graph_after=graph,
                forces_before=forces,
                forces_after=forces,
            )
            for before, after in zip(states[:-1], states[1:], strict=True)
        )
    )


def _model(
    pressure: FLiBePressureCoordinate | None = None,
) -> FLiBeTrajectoryStateCoordinates:
    trajectory = _trajectory()
    density = evaluate_flibe_trajectory_density(
        trajectory,
        FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        model_id="TR-EIP-NUMERIC-FIXTURE",
        trajectory_id="MD-SAMPLED-FIXTURE",
        provenance=PROVENANCE,
        mass_unit_to_kg=MASS_UNIT_KG,
        coordinate_unit_to_meter=LENGTH_UNIT_M,
        stride=2,
    )
    if pressure is None:
        pressure = _pressure()
    return evaluate_flibe_trajectory_state_coordinates(
        trajectory,
        density,
        degrees_of_freedom=21,
        time_unit_to_second=TIME_UNIT_S,
        physical_state_id="liquid",
        physical_state_method_id="EXPLICIT-TEST-STATE",
        pressure=pressure,
    )


def _pressure(
    role: FLiBePressureRole = FLiBePressureRole.OBSERVED,
    value: float = PRESSURE_PA,
) -> FLiBePressureCoordinate:
    return FLiBePressureCoordinate(
        pressure_pa=value,
        role=role,
        method_id="TEST-PRESSURE-COORDINATE",
        source_id="TEST-PRESSURE-RECORD",
        provenance=PROVENANCE,
    )


def _mapping(**updates: object) -> FLiBeDensityObservableMapping:
    arguments: dict[str, object] = {
        "mapping_id": "EXPLICIT-MEAN-CELL-DENSITY-MAPPING",
        "model_statistic_id": MODEL_DENSITY_STATISTIC,
        "source_normalization_id": NORMALIZATION,
        "method_id": "ANALYTIC-FIXTURE-COMPARISON",
        "provenance": PROVENANCE,
        "assumptions": ("fixed-cell-mass", "arithmetic-mean-cell-density"),
    }
    arguments.update(updates)
    return FLiBeDensityObservableMapping(**arguments)


def _record(index: int, density: float, **changes: object) -> FLiBeRegisteredDensityRecord:
    coordinates: dict[str, object] = {
        "density_kg_m3": density,
        "composition": FLiBeComposition(2.0, 1.0),
        "temperature_k": EXPECTED_TEMPERATURE_K,
        "pressure_pa": PRESSURE_PA,
        "physical_state_id": "liquid",
        "normalization_id": NORMALIZATION,
        "evidence_kind": FLiBeEvidenceKind.FIRST_PRINCIPLES,
        "source_id": SYNTHETIC_DATASET,
        "method_id": "ANALYTIC-NUMERICAL-FIXTURE",
        "provenance": PROVENANCE,
    }
    coordinates.update(changes)
    return FLiBeRegisteredDensityRecord(
        dataset_id=SYNTHETIC_DATASET,
        record_id=f"{SYNTHETIC_DATASET}/{index:03d}",
        doi="TEST-FIXTURE-NO-PUBLICATION",
        source_location="Independent numerical fixture",
        source_file_sha256=SYNTHETIC_DIGEST,
        run_id="ANALYTIC",
        row_index=index,
        source_columns=("temperature_k", "density_kg_m3"),
        source_values=(float(coordinates["temperature_k"]), density),
        coordinates=FLiBeDensitySourceCoordinates(**coordinates),
    )


def _compare(
    records: tuple[FLiBeRegisteredDensityRecord, ...],
    *,
    model: FLiBeTrajectoryStateCoordinates | None = None,
    mapping: FLiBeDensityObservableMapping | None = None,
    temperature_tolerance_k: float = 1.0e-12,
    pressure_tolerance_pa: float = 0.0,
) -> FLiBeRegisteredDensityComparison:
    return compare_flibe_registered_density_records(
        _model() if model is None else model,
        records,
        mapping=_mapping() if mapping is None else mapping,
        temperature_tolerance_k=temperature_tolerance_k,
        pressure_tolerance_pa=pressure_tolerance_pa,
    )


def test_model_density_and_temperature_have_independent_expected_values() -> None:
    model = _model()
    assert model.density_trace.sample_count == 2
    assert model.density_trace.mean_density_kg_m3 == pytest.approx(
        EXPECTED_DENSITY_KG_M3, rel=1.0e-13
    )
    assert model.mean_kinetic_temperature_k == pytest.approx(
        EXPECTED_TEMPERATURE_K, rel=1.0e-13
    )
    assert model.density_trace.composition == FLiBeComposition(2.0, 1.0)


def test_three_matched_records_use_independent_signed_residuals_and_metrics() -> None:
    records = (_record(0, 740.0), _record(1, 770.0), _record(2, 750.0))
    report = _compare(records)
    assert tuple(row.record_id for row in report.rows) == tuple(
        record.record_id for record in records
    )
    assert all(row.correspondence.coordinate_match for row in report.rows)
    assert tuple(row.density_residual_kg_m3 for row in report.rows) == pytest.approx(
        (10.0, -20.0, 0.0), abs=1.0e-10
    )
    assert report.matched_count == 3
    assert report.unmatched_count == 0
    metrics = report.residual_metrics
    assert metrics is not None
    assert metrics.count == 3
    assert metrics.mean_signed_kg_m3 == pytest.approx(-10.0 / 3.0, abs=1.0e-10)
    assert metrics.mean_absolute_kg_m3 == pytest.approx(10.0, abs=1.0e-10)
    assert metrics.root_mean_square_kg_m3 == pytest.approx(
        sqrt(500.0 / 3.0), abs=1.0e-10
    )
    assert metrics.maximum_absolute_kg_m3 == pytest.approx(20.0, abs=1.0e-10)


def test_unmatched_rows_do_not_enter_statistical_aggregation() -> None:
    records = (
        _record(0, 740.0),
        _record(1, 770.0),
        _record(2, 750.0),
        _record(3, 999.0, composition=FLiBeComposition(0.67, 0.33)),
        _record(4, 50.0, pressure_pa=PRESSURE_PA + 25.0),
    )
    report = _compare(records)
    assert report.matched_count == 3
    assert report.unmatched_count == 2
    assert tuple(row.density_residual_kg_m3 for row in report.rows[3:]) == (None, None)
    assert report.rows[3].unmatched_axes == ("composition",)
    assert report.rows[4].unmatched_axes == ("pressure",)
    assert report.residual_metrics is not None
    assert report.residual_metrics.count == 3
    assert report.residual_metrics.mean_absolute_kg_m3 == pytest.approx(10.0)


def test_single_exact_match_keeps_zero_residual_and_zero_error() -> None:
    report = _compare((_record(0, 750.0),))
    assert report.matched_count == 1
    assert report.rows[0].density_residual_kg_m3 == pytest.approx(0.0, abs=1.0e-11)
    assert report.residual_metrics is not None
    assert report.residual_metrics.mean_signed_kg_m3 == pytest.approx(0.0, abs=1.0e-11)
    assert report.residual_metrics.root_mean_square_kg_m3 == pytest.approx(0.0, abs=1.0e-11)


def test_source_missing_pressure_and_phase_remain_explicit_axes() -> None:
    record = _record(0, 760.0, pressure_pa=None, physical_state_id=None)
    row = _compare((record,)).rows[0]
    assert row.missing_source_axes == ("pressure", "physical_state")
    assert row.unmatched_axes == ("pressure", "physical_state")
    assert row.matched_axes == ("composition", "temperature", "normalization")
    assert row.pressure_difference_pa is None
    assert row.density_residual_kg_m3 is None


def test_declared_normalization_must_match_source_identity() -> None:
    report = _compare(
        (_record(0, 760.0),),
        mapping=_mapping(source_normalization_id="DIFFERENT-NORMALIZATION"),
    )
    assert report.rows[0].unmatched_axes == ("normalization",)
    assert report.rows[0].density_residual_kg_m3 is None
    assert report.residual_metrics is None


@pytest.mark.parametrize(
    ("changes", "failed_axis"),
    (
        ({"composition": FLiBeComposition(0.67, 0.33)}, "composition"),
        ({"composition": FLiBeComposition(0.6642, 0.3358)}, "composition"),
        ({"temperature_k": EXPECTED_TEMPERATURE_K + 0.5}, "temperature"),
        ({"pressure_pa": PRESSURE_PA + 10.0}, "pressure"),
        ({"pressure_pa": None}, "pressure"),
        ({"physical_state_id": "solid"}, "physical_state"),
        ({"physical_state_id": None}, "physical_state"),
        ({"normalization_id": "density-at-mean-volume"}, "normalization"),
    ),
)
def test_individual_state_axis_mismatch_excludes_residual(
    changes: dict[str, object], failed_axis: str
) -> None:
    row = _compare((_record(0, 760.0, **changes),)).rows[0]
    assert failed_axis in row.unmatched_axes
    assert failed_axis not in row.matched_axes
    assert row.density_residual_kg_m3 is None


def test_predeclared_temperature_and_pressure_tolerance_boundaries() -> None:
    record = _record(
        0, 740.0,
        temperature_k=EXPECTED_TEMPERATURE_K + 0.25,
        pressure_pa=PRESSURE_PA + 20.0,
    )
    within = _compare((record,), temperature_tolerance_k=0.25,
                      pressure_tolerance_pa=20.0)
    outside_temperature = _compare((record,), temperature_tolerance_k=0.24,
                                   pressure_tolerance_pa=20.0)
    outside_pressure = _compare((record,), temperature_tolerance_k=0.25,
                                pressure_tolerance_pa=19.0)
    assert within.matched_count == 1
    assert within.rows[0].density_residual_kg_m3 == pytest.approx(10.0)
    assert outside_temperature.rows[0].unmatched_axes == ("temperature",)
    assert outside_pressure.rows[0].unmatched_axes == ("pressure",)


def test_pressure_control_target_is_not_observed_pressure() -> None:
    control = _model(pressure=_pressure(role=FLiBePressureRole.CONTROL_TARGET))
    report = _compare((_record(0, 740.0),), model=control)
    assert report.rows[0].unmatched_axes == ("pressure",)
    assert report.rows[0].pressure_difference_pa is None
    assert report.residual_metrics is None


def test_rows_preserve_registered_source_provenance_and_order() -> None:
    records = load_flibe_density_source_records(VIDRIO)
    report = _compare(records)
    assert len(records) == len(report.rows) == 61
    assert tuple(row.source_record for row in report.rows) == records
    assert tuple(row.record_id for row in report.rows) == tuple(
        record.record_id for record in records
    )
    assert report.source_dataset_id == records[0].dataset_id
    assert report.source_file_sha256 == records[0].source_file_sha256
    assert tuple(row.source_record.run_id for row in report.rows[:2]) == ("0A", "0A")
    assert all(row.source_record.coordinates.provenance is
               ParameterProvenance.PRIMARY_SOURCE for row in report.rows)
    assert all(row.density_residual_kg_m3 is None for row in report.rows)
    assert report.matched_count == 0
    assert report.unmatched_count == 61
    assert report.residual_metrics is None


def test_vidrio_composition_pressure_and_unreported_phase_are_not_inferred() -> None:
    report = _compare(load_flibe_density_source_records(VIDRIO))
    for row in report.rows:
        assert row.source_record.coordinates.composition.bef2_fraction == pytest.approx(0.3358)
        assert row.bef2_fraction_difference == pytest.approx(1.0 / 3.0 - 0.3358)
        assert row.pressure_difference_pa == -675.0
        assert row.missing_source_axes == ("physical_state",)
        assert "composition" in row.unmatched_axes
        assert "physical_state" in row.unmatched_axes
        assert row.density_residual_kg_m3 is None


def test_baral_source_unknown_pressure_and_phase_block_direct_residuals() -> None:
    records = load_flibe_density_source_records(BARAL)
    report = _compare(records)
    assert len(report.rows) == 9
    assert report.matched_count == 0
    assert report.unmatched_count == 9
    assert report.residual_metrics is None
    for row in report.rows:
        assert row.source_record.coordinates.evidence_kind is FLiBeEvidenceKind.FIRST_PRINCIPLES
        assert row.missing_source_axes == ("pressure", "physical_state")
        assert row.pressure_difference_pa is None
        assert row.bef2_fraction_difference == pytest.approx(0.0, abs=1.0e-14)
        assert row.correspondence.composition_match
        assert row.density_residual_kg_m3 is None


def test_reports_replay_deterministically_on_real_source_files() -> None:
    first = _compare(load_flibe_density_source_records(BARAL))
    second = _compare(load_flibe_density_source_records(BARAL))
    assert first == second
    assert first.mapping.provenance is PROVENANCE
    assert first.model.density_trace.trajectory_id == "MD-SAMPLED-FIXTURE"
    with pytest.raises(FrozenInstanceError):
        first.source_dataset_id = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value", "exception", "match"),
    (
        ("model_statistic_id", "density-at-mean-volume", ValueError, "MD mean density"),
        ("mapping_id", " ", ValueError, "nonempty trimmed"),
        ("method_id", "", ValueError, "nonempty trimmed"),
        ("provenance", "TEST_FIXTURE", TypeError, "ParameterProvenance"),
        ("assumptions", (), ValueError, "identify the comparison"),
        ("assumptions", ("fixed-cell-mass", "fixed-cell-mass"), ValueError, "distinct"),
        ("assumptions", ["fixed-cell-mass"], TypeError, "must be a tuple"),
        ("assumptions", ("",), ValueError, "nonempty trimmed"),
    ),
)
def test_mapping_rejects_invalid_contracts(
    field: str, value: object, exception: type[Exception], match: str
) -> None:
    with pytest.raises(exception, match=match):
        _mapping(**{field: value})


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    (
        ("temperature_tolerance_k", -0.1, ValueError),
        ("temperature_tolerance_k", float("inf"), ValueError),
        ("temperature_tolerance_k", float("nan"), ValueError),
        ("temperature_tolerance_k", True, TypeError),
        ("pressure_tolerance_pa", -1.0, ValueError),
        ("pressure_tolerance_pa", float("nan"), ValueError),
        ("pressure_tolerance_pa", False, TypeError),
    ),
)
def test_comparison_rejects_invalid_tolerances(
    field: str, value: object, exception: type[Exception]
) -> None:
    with pytest.raises(exception):
        _compare((_record(0, 740.0),), **{field: value})


def test_comparison_rejects_untyped_inputs_and_empty_rows() -> None:
    model = _model()
    mapping = _mapping()
    record = _record(0, 740.0)
    with pytest.raises(TypeError, match="model must be"):
        compare_flibe_registered_density_records(
            None, (record,), mapping=mapping,
            temperature_tolerance_k=0.0, pressure_tolerance_pa=0.0,
        )
    with pytest.raises(TypeError, match="mapping must be"):
        compare_flibe_registered_density_records(
            model, (record,), mapping=None,
            temperature_tolerance_k=0.0, pressure_tolerance_pa=0.0,
        )
    with pytest.raises(ValueError, match="nonempty tuple"):
        _compare(())
    with pytest.raises(ValueError, match="nonempty tuple"):
        _compare([record])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="FLiBeRegisteredDensityRecord"):
        _compare((record, object()))  # type: ignore[arg-type]


def test_mixed_datasets_and_source_fingerprints_are_rejected() -> None:
    first = _record(0, 740.0)
    second = _record(1, 770.0)
    with pytest.raises(ValueError, match="source dataset identities"):
        _compare((first, replace(second, dataset_id="ANOTHER-DATASET")))
    with pytest.raises(ValueError, match="source file fingerprints"):
        _compare((first, replace(second, source_file_sha256="f" * 64)))
    vidrio = load_flibe_density_source_records(VIDRIO)[0]
    baral = load_flibe_density_source_records(BARAL)[0]
    with pytest.raises(ValueError, match="source dataset identities"):
        _compare((vidrio, baral))


def test_duplicate_record_id_rejected_before_statistical_aggregation() -> None:
    first = _record(0, 740.0)
    with pytest.raises(ValueError, match="must be unique"):
        _compare((first, first))


def test_report_rejects_malformed_source_digest_and_changed_model() -> None:
    report = _compare((_record(0, 740.0),))
    with pytest.raises(ValueError, match="SHA-256"):
        replace(report, source_file_sha256="not-a-digest")
    with pytest.raises(ValueError, match="source file fingerprints"):
        replace(report, source_file_sha256="e" * 64)
    with pytest.raises(ValueError, match="selected model state"):
        replace(report, model=replace(report.model, physical_state_id="solid"))


def test_row_rejects_reference_state_mismatch() -> None:
    record = _record(0, 740.0)
    correspondence = compare_flibe_density_state_coordinates(
        _model(), record.coordinates,
        temperature_tolerance_k=1.0e-12,
        pressure_tolerance_pa=0.0,
        normalization_id=NORMALIZATION,
    )
    with pytest.raises(ValueError, match="source row and correspondence"):
        FLiBeRegisteredDensityComparisonRow(
            source_record=_record(1, 770.0),
            correspondence=correspondence,
        )
