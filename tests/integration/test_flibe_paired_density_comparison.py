"""Independent paired FLiBe density comparison and state-matching contracts."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import sqrt
from pathlib import Path

import pytest

from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.paired_density_comparison import (
    FLiBePairedDensityComparison,
    FLiBePairedDensityRow,
    compare_flibe_paired_density_models,
)
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind
from tr_eif.flibe.registered_density_cross_model import (
    MODEL_DENSITY_STATISTIC,
    FLiBeDensityObservableMapping,
    compare_flibe_registered_density_records,
)
from tr_eif.flibe.registered_density_sources import (
    FLiBeRegisteredDensityRecord,
    load_flibe_density_source_records,
)
from tr_eif.flibe.trajectory_density import FLiBeDensitySample, FLiBeTrajectoryDensity
from tr_eif.flibe.trajectory_pressure import FLiBeVelocityFrame
from tr_eif.flibe.trajectory_state_correspondence import (
    FLiBeDensitySourceCoordinates,
    FLiBePressureCoordinate,
    FLiBePressureRole,
    FLiBeTrajectoryStateCoordinates,
)
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
VIDRIO = ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
BARAL = ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
COMPOSITION = FLiBeComposition(2.0, 1.0)
NORMALIZATION = "source-reported-mass-density"
DATASET_ID = "INDEPENDENT-PAIRED-DENSITY-FIXTURE"
DIGEST = "0123456789abcdef" * 4
PROVENANCE = ParameterProvenance.TEST_FIXTURE
MASS_KG = 27.0e-27
TEMPERATURE_K = 1000.0
PRESSURE_PA = 101325.0


def _model(
    name: str,
    *,
    densities: tuple[float, ...],
    temperature_k: float = TEMPERATURE_K,
    pressure_pa: float | None = PRESSURE_PA,
    pressure_role: FLiBePressureRole = FLiBePressureRole.OBSERVED,
    composition: FLiBeComposition = COMPOSITION,
    physical_state_id: str = "liquid",
) -> FLiBeTrajectoryStateCoordinates:
    # Each volume is specified independently by M / rho for fixed cell mass.
    samples = tuple(
        FLiBeDensitySample(
            state_index=index,
            md_step=index,
            md_time=0.25 * index,
            cell_volume_m3=MASS_KG / density,
            density_kg_m3=density,
        )
        for index, density in enumerate(densities)
    )
    trace = FLiBeTrajectoryDensity(
        model_id=name,
        trajectory_id=f"{name}-TRAJECTORY",
        provenance=PROVENANCE,
        composition=composition,
        atom_count=7,
        total_mass_kg=MASS_KG,
        mass_unit_to_kg=1.0e-27,
        coordinate_unit_to_meter=1.0e-10,
        samples=samples,
    )
    pressure = None if pressure_pa is None else FLiBePressureCoordinate(
        pressure_pa=pressure_pa,
        role=pressure_role,
        method_id="FIXTURE-PRESSURE-COORDINATE",
        source_id=f"{name}-PRESSURE",
        provenance=PROVENANCE,
    )
    return FLiBeTrajectoryStateCoordinates(
        density_trace=trace,
        kinetic_temperature_k=(temperature_k,) * len(samples),
        degrees_of_freedom=21,
        time_unit_to_second=1.0e-12,
        physical_state_id=physical_state_id,
        physical_state_method_id="DECLARED-FIXTURE-STATE",
        pressure=pressure,
    )


def _reference(index: int, density: float, **changes: object) -> FLiBeRegisteredDensityRecord:
    coordinates: dict[str, object] = {
        "density_kg_m3": density,
        "composition": COMPOSITION,
        "temperature_k": TEMPERATURE_K,
        "pressure_pa": PRESSURE_PA,
        "physical_state_id": "liquid",
        "normalization_id": NORMALIZATION,
        "evidence_kind": FLiBeEvidenceKind.FIRST_PRINCIPLES,
        "source_id": DATASET_ID,
        "method_id": "INDEPENDENT-NUMERICAL-FIXTURE",
        "provenance": PROVENANCE,
    }
    coordinates.update(changes)
    return FLiBeRegisteredDensityRecord(
        dataset_id=DATASET_ID,
        record_id=f"{DATASET_ID}/{index:03d}",
        doi="TEST-FIXTURE-NO-PUBLICATION",
        source_location="Independent numerical reference fixture",
        source_file_sha256=DIGEST,
        run_id="NUMERIC",
        row_index=index,
        source_columns=("temperature_k", "density_kg_m3"),
        source_values=(float(coordinates["temperature_k"]), density),
        coordinates=FLiBeDensitySourceCoordinates(**coordinates),
    )


def _mapping() -> FLiBeDensityObservableMapping:
    return FLiBeDensityObservableMapping(
        mapping_id="PAIRED-MEAN-CELL-DENSITY",
        model_statistic_id=MODEL_DENSITY_STATISTIC,
        source_normalization_id=NORMALIZATION,
        method_id="INDEPENDENT-PAIRED-REFERENCE-COMPARISON",
        provenance=PROVENANCE,
        assumptions=("fixed-cell-mass", "arithmetic-mean-cell-density"),
    )


def _reports(
    records: tuple[FLiBeRegisteredDensityRecord, ...],
    *,
    first: FLiBeTrajectoryStateCoordinates | None = None,
    second: FLiBeTrajectoryStateCoordinates | None = None,
    source_temperature_tolerance_k: float = 0.0,
    source_pressure_tolerance_pa: float = 0.0,
):
    first = _model("MODEL-A", densities=(730.0, 770.0)) if first is None else first
    second = _model("MODEL-B", densities=(750.0, 770.0)) if second is None else second
    mapping = _mapping()
    return tuple(
        compare_flibe_registered_density_records(
            model,
            records,
            mapping=mapping,
            temperature_tolerance_k=source_temperature_tolerance_k,
            pressure_tolerance_pa=source_pressure_tolerance_pa,
        )
        for model in (first, second)
    )


def _paired(
    records: tuple[FLiBeRegisteredDensityRecord, ...],
    *,
    first: FLiBeTrajectoryStateCoordinates | None = None,
    second: FLiBeTrajectoryStateCoordinates | None = None,
    first_frame: FLiBeVelocityFrame = FLiBeVelocityFrame.CENTER_OF_MASS,
    second_frame: FLiBeVelocityFrame = FLiBeVelocityFrame.CENTER_OF_MASS,
    model_temperature_tolerance_k: float = 0.0,
    model_pressure_tolerance_pa: float = 0.0,
    source_temperature_tolerance_k: float = 0.0,
    source_pressure_tolerance_pa: float = 0.0,
) -> FLiBePairedDensityComparison:
    first_report, second_report = _reports(
        records, first=first, second=second,
        source_temperature_tolerance_k=source_temperature_tolerance_k,
        source_pressure_tolerance_pa=source_pressure_tolerance_pa,
    )
    return compare_flibe_paired_density_models(
        first_report,
        second_report,
        comparison_id="TWO-INDEPENDENT-MODELS",
        first_velocity_frame=first_frame,
        second_velocity_frame=second_frame,
        model_temperature_tolerance_k=model_temperature_tolerance_k,
        model_pressure_tolerance_pa=model_pressure_tolerance_pa,
    )


def test_independent_volumes_and_model_densities() -> None:
    first, second = _reports((_reference(0, 740.0),))
    a = first.model.density_trace
    b = second.model.density_trace
    assert a.mean_density_kg_m3 == pytest.approx(750.0, abs=1e-12)
    assert b.mean_density_kg_m3 == pytest.approx(760.0, abs=1e-12)
    assert tuple(s.cell_volume_m3 for s in a.samples) == pytest.approx(
        (MASS_KG / 730.0, MASS_KG / 770.0), rel=1e-14,
    )
    assert a.model_id == "MODEL-A" and b.model_id == "MODEL-B"
    assert a.trajectory_id != b.trajectory_id


def test_paired_residuals_and_metrics_match_fixed_arithmetic() -> None:
    records = (_reference(0, 740.0), _reference(1, 780.0), _reference(2, 750.0))
    report = _paired(records)
    assert report.model_state_match
    assert report.paired_count == 3
    assert report.excluded_count == 0
    assert report.paired_record_ids == tuple(record.record_id for record in records)
    assert report.model_density_difference_kg_m3 == pytest.approx(10.0)
    assert tuple(row.first_residual_kg_m3 for row in report.rows) == pytest.approx(
        (10.0, -30.0, 0.0), abs=1e-12,
    )
    assert tuple(row.second_residual_kg_m3 for row in report.rows) == pytest.approx(
        (20.0, -20.0, 10.0), abs=1e-12,
    )
    assert tuple(row.second_minus_first_density_kg_m3 for row in report.rows) == pytest.approx(
        (10.0, 10.0, 10.0), abs=1e-12,
    )
    assert tuple(row.second_minus_first_absolute_error_kg_m3 for row in report.rows) == pytest.approx(
        (10.0, -10.0, 10.0), abs=1e-12,
    )
    metrics = report.metrics
    assert metrics is not None and metrics.count == 3
    assert metrics.first_bias_kg_m3 == pytest.approx(-20.0 / 3.0)
    assert metrics.second_bias_kg_m3 == pytest.approx(10.0 / 3.0)
    assert metrics.first_mae_kg_m3 == pytest.approx(40.0 / 3.0)
    assert metrics.second_mae_kg_m3 == pytest.approx(50.0 / 3.0)
    assert metrics.first_rmse_kg_m3 == pytest.approx(sqrt(1000.0 / 3.0))
    assert metrics.second_rmse_kg_m3 == pytest.approx(sqrt(300.0))
    assert metrics.second_minus_first_mae_kg_m3 == pytest.approx(10.0 / 3.0)
    assert metrics.second_minus_first_rmse_kg_m3 == pytest.approx(
        sqrt(300.0) - sqrt(1000.0 / 3.0),
    )
    assert metrics.mean_model_density_difference_kg_m3 == pytest.approx(10.0)


def test_source_mismatch_excludes_only_that_reference_row() -> None:
    records = (
        _reference(0, 740.0),
        _reference(1, 750.0, composition=FLiBeComposition(0.67, 0.33)),
        _reference(2, 780.0),
    )
    report = _paired(records)
    assert report.paired_record_ids == (records[0].record_id, records[2].record_id)
    assert report.paired_count == 2 and report.excluded_count == 1
    assert report.rows[1].model_state_match
    assert not report.rows[1].paired_state_match
    assert report.rows[1].model_density_difference_kg_m3 == pytest.approx(10.0)
    assert report.rows[1].first_residual_kg_m3 is None
    assert report.rows[1].second_residual_kg_m3 is None
    assert report.rows[1].second_minus_first_density_kg_m3 is None
    assert report.rows[1].second_minus_first_absolute_error_kg_m3 is None
    metrics = report.metrics
    assert metrics is not None and metrics.count == 2
    # The independent matched records are 740 and 780 kg/m^3.
    assert metrics.first_mae_kg_m3 == pytest.approx(20.0)
    assert metrics.second_mae_kg_m3 == pytest.approx(20.0)
    assert metrics.first_rmse_kg_m3 == pytest.approx(sqrt(500.0))
    assert metrics.second_rmse_kg_m3 == pytest.approx(20.0)


def test_model_difference_remains_available_when_source_axes_are_unknown() -> None:
    records = (_reference(0, 740.0, pressure_pa=None, physical_state_id=None),)
    report = _paired(records)
    assert report.model_state_match
    assert report.model_density_difference_kg_m3 == pytest.approx(10.0)
    assert report.rows[0].model_unmatched_axes == ()
    assert not report.rows[0].paired_state_match
    assert report.rows[0].first_residual_kg_m3 is None
    assert report.rows[0].second_residual_kg_m3 is None
    assert report.metrics is None
    assert report.paired_count == 0 and report.excluded_count == 1


def test_observed_model_pressure_is_required_for_model_pairing() -> None:
    reference = (_reference(0, 740.0),)
    for invalid_pressure in (None, FLiBePressureRole.CONTROL_TARGET):
        second = _model(
            "MODEL-B", densities=(750.0, 770.0),
            pressure_pa=None if invalid_pressure is None else PRESSURE_PA,
            pressure_role=(
                FLiBePressureRole.OBSERVED if invalid_pressure is None
                else invalid_pressure
            ),
        )
        report = _paired(reference, second=second)
        assert report.rows[0].model_unmatched_axes == ("pressure",)
        assert report.rows[0].model_pressure_difference_pa is None
        assert report.model_density_difference_kg_m3 is None
        assert report.metrics is None


@pytest.mark.parametrize(
    ("changes", "expected_axis"),
    (
        ({"composition": FLiBeComposition(0.67, 0.33)}, "composition"),
        ({"temperature_k": 1000.5}, "temperature"),
        ({"pressure_pa": 101375.0}, "pressure"),
        ({"physical_state_id": "solid"}, "physical_state"),
    ),
)
def test_model_state_axes_gate_model_difference(changes: dict[str, object], expected_axis: str) -> None:
    second = _model("MODEL-B", densities=(750.0, 770.0), **changes)
    report = _paired((_reference(0, 740.0),), second=second)
    assert report.rows[0].model_unmatched_axes == (expected_axis,)
    assert not report.model_state_match
    assert report.model_density_difference_kg_m3 is None
    assert report.paired_count == 0 and report.metrics is None


def test_velocity_frame_identity_is_separate_from_model_state() -> None:
    report = _paired(
        (_reference(0, 740.0),),
        first_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
        second_frame=FLiBeVelocityFrame.LABORATORY,
    )
    assert report.rows[0].model_unmatched_axes == ("velocity_frame",)
    assert report.model_density_difference_kg_m3 is None
    assert report.paired_count == 0


def test_model_tolerances_and_source_tolerances_are_separate() -> None:
    reference = (_reference(0, 740.0),)
    second = _model(
        "MODEL-B", densities=(750.0, 770.0),
        temperature_k=1000.25, pressure_pa=101375.0,
    )
    within_models = _paired(
        reference, second=second,
        model_temperature_tolerance_k=0.25,
        model_pressure_tolerance_pa=50.0,
        source_temperature_tolerance_k=0.0,
        source_pressure_tolerance_pa=0.0,
    )
    assert within_models.model_state_match
    assert within_models.model_density_difference_kg_m3 == pytest.approx(10.0)
    assert within_models.paired_count == 0 and within_models.metrics is None
    assert within_models.rows[0].second_residual_kg_m3 is None
    fully_matched = _paired(
        reference, second=second,
        model_temperature_tolerance_k=0.25,
        model_pressure_tolerance_pa=50.0,
        source_temperature_tolerance_k=0.25,
        source_pressure_tolerance_pa=50.0,
    )
    assert fully_matched.paired_count == 1
    assert fully_matched.rows[0].first_residual_kg_m3 == pytest.approx(10.0)
    assert fully_matched.rows[0].second_residual_kg_m3 == pytest.approx(20.0)
    assert not _paired(
        reference, second=second,
        model_temperature_tolerance_k=0.24,
        model_pressure_tolerance_pa=50.0,
    ).model_state_match
    assert not _paired(
        reference, second=second,
        model_temperature_tolerance_k=0.25,
        model_pressure_tolerance_pa=49.0,
    ).model_state_match


def test_zero_model_difference_is_a_valid_matched_result() -> None:
    second = _model("MODEL-B", densities=(730.0, 770.0))
    report = _paired((_reference(0, 750.0),), second=second)
    assert report.model_state_match
    assert report.model_density_difference_kg_m3 == pytest.approx(0.0)
    assert report.rows[0].second_minus_first_density_kg_m3 == pytest.approx(0.0)
    assert report.metrics is not None
    assert report.metrics.second_minus_first_mae_kg_m3 == pytest.approx(0.0)
    assert report.metrics.second_minus_first_rmse_kg_m3 == pytest.approx(0.0)


def test_registered_vidrio_rows_retained_without_source_residuals() -> None:
    records = load_flibe_density_source_records(VIDRIO)
    report = _paired(records)
    assert len(report.rows) == 61
    assert tuple(row.record_id for row in report.rows) == tuple(r.record_id for r in records)
    assert report.model_state_match
    assert report.model_density_difference_kg_m3 == pytest.approx(10.0)
    assert report.paired_count == 0 and report.excluded_count == 61
    assert report.metrics is None
    assert all(row.first_residual_kg_m3 is None for row in report.rows)
    assert all(row.second_residual_kg_m3 is None for row in report.rows)
    assert all(not row.paired_state_match for row in report.rows)
    assert all(row.first.source_record.coordinates.composition.bef2_fraction == pytest.approx(0.3358)
               for row in report.rows)


def test_registered_baral_unknown_coordinates_are_not_zero_filled() -> None:
    records = load_flibe_density_source_records(BARAL)
    report = _paired(records)
    assert len(report.rows) == 9
    assert report.paired_count == 0 and report.excluded_count == 9
    assert report.model_state_match
    assert report.model_density_difference_kg_m3 == pytest.approx(10.0)
    assert report.metrics is None
    assert all(row.first.source_record.coordinates.pressure_pa is None for row in report.rows)
    assert all(row.first.source_record.coordinates.physical_state_id is None for row in report.rows)
    assert all(row.first_residual_kg_m3 is None for row in report.rows)
    assert all(row.second_residual_kg_m3 is None for row in report.rows)


def test_distinct_model_ids_are_required_even_with_distinct_trajectories() -> None:
    records = (_reference(0, 740.0),)
    second = _model("MODEL-A", densities=(750.0, 770.0))
    with pytest.raises(ValueError, match="distinct model identifiers"):
        _paired(records, second=second)


def test_reference_row_order_and_selection_must_be_identical() -> None:
    records = (_reference(0, 740.0), _reference(1, 770.0))
    first, _ = _reports(records)
    reordered_second = _reports(tuple(reversed(records)))[1]
    with pytest.raises(ValueError, match="identical ordered source records"):
        compare_flibe_paired_density_models(
            first, reordered_second,
            comparison_id="ORDER-TEST",
            first_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            second_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            model_temperature_tolerance_k=0.0,
            model_pressure_tolerance_pa=0.0,
        )
    shorter_second = _reports(records[:1])[1]
    with pytest.raises(ValueError, match="equal lengths"):
        compare_flibe_paired_density_models(
            first, shorter_second,
            comparison_id="LENGTH-TEST",
            first_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            second_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            model_temperature_tolerance_k=0.0,
            model_pressure_tolerance_pa=0.0,
        )


def test_source_mapping_and_reference_criteria_must_agree() -> None:
    records = (_reference(0, 740.0),)
    first, second = _reports(records)
    changed_mapping = replace(second, mapping=replace(second.mapping, mapping_id="OTHER"))
    with pytest.raises(ValueError, match="observable mappings must agree"):
        replace(_paired(records), second=changed_mapping)
    changed_tolerance = replace(second, temperature_tolerance_k=0.1)
    with pytest.raises(ValueError, match="reference correspondence tolerances must agree"):
        replace(_paired(records), second=changed_tolerance)


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("model_temperature_tolerance_k", -0.1, ValueError),
        ("model_temperature_tolerance_k", float("nan"), ValueError),
        ("model_temperature_tolerance_k", float("inf"), ValueError),
        ("model_temperature_tolerance_k", False, TypeError),
        ("model_pressure_tolerance_pa", -1.0, ValueError),
        ("model_pressure_tolerance_pa", float("inf"), ValueError),
        ("model_pressure_tolerance_pa", True, TypeError),
        ("model_pressure_tolerance_pa", "0", TypeError),
    ),
)
def test_invalid_model_criteria_rejected(field: str, invalid: object, error: type[Exception]) -> None:
    first, second = _reports((_reference(0, 740.0),))
    arguments: dict[str, object] = {
        "comparison_id": "CRITERIA-TEST",
        "first_velocity_frame": FLiBeVelocityFrame.CENTER_OF_MASS,
        "second_velocity_frame": FLiBeVelocityFrame.CENTER_OF_MASS,
        "model_temperature_tolerance_k": 0.0,
        "model_pressure_tolerance_pa": 0.0,
    }
    arguments[field] = invalid
    with pytest.raises(error):
        compare_flibe_paired_density_models(first, second, **arguments)


@pytest.mark.parametrize("invalid", ("", " ", " spaced ", 5, None))
def test_invalid_pair_identity_rejected(invalid: object) -> None:
    report = _paired((_reference(0, 740.0),))
    with pytest.raises((ValueError, TypeError), match="comparison_id"):
        replace(report, comparison_id=invalid)


def test_untyped_inputs_and_velocity_frames_rejected() -> None:
    records = (_reference(0, 740.0),)
    first, second = _reports(records)
    with pytest.raises(TypeError, match="first and second"):
        compare_flibe_paired_density_models(
            object(), second, comparison_id="BAD-INPUT",
            first_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            second_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            model_temperature_tolerance_k=0.0, model_pressure_tolerance_pa=0.0,
        )
    with pytest.raises(TypeError, match="velocity frames"):
        compare_flibe_paired_density_models(
            first, second, comparison_id="BAD-FRAME",
            first_velocity_frame="CENTER_OF_MASS",
            second_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            model_temperature_tolerance_k=0.0, model_pressure_tolerance_pa=0.0,
        )


def test_pair_and_row_integrity_are_checked_on_replacement() -> None:
    records = (_reference(0, 740.0), _reference(1, 780.0))
    report = _paired(records)
    with pytest.raises(ValueError, match="preserve source record order"):
        replace(report, rows=tuple(reversed(report.rows)))
    with pytest.raises(ValueError, match="nonempty tuple"):
        replace(report, rows=())
    with pytest.raises(ValueError, match="paired row criteria"):
        replace(report, rows=(
            replace(report.rows[0], model_temperature_tolerance_k=1.0),
            report.rows[1],
        ))
    with pytest.raises(ValueError, match="exact reference record"):
        FLiBePairedDensityRow(
            first=report.first.rows[0],
            second=report.second.rows[1],
            first_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            second_velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
            model_temperature_tolerance_k=0.0,
            model_pressure_tolerance_pa=0.0,
        )


def test_repeatability_and_immutable_provenance() -> None:
    records = (_reference(0, 740.0), _reference(1, 780.0))
    first = _paired(records)
    second = _paired(records)
    assert first == second
    assert first.first.source_file_sha256 == DIGEST
    assert first.second.source_file_sha256 == DIGEST
    assert first.first.mapping.provenance is PROVENANCE
    assert first.second.mapping.provenance is PROVENANCE
    with pytest.raises(FrozenInstanceError):
        first.comparison_id = "CHANGED"  # type: ignore[misc]
