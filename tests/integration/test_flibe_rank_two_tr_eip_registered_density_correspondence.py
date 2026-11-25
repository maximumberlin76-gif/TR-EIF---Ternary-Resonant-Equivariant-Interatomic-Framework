
"""Integration checks for registered-source FLiBe rank-two MD density.

Reconstruct densities, kinetic temperatures and post-barostat pressure from a
scheduled rank-two TR-EIP trajectory. Preserve reference-source fingerprints,
uncertainty fields, missing physical coordinates and active-neutral execution.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isclose, isfinite
from pathlib import Path

import pytest

from tr_eif.flibe.rank_two_tr_eip_registered_density_correspondence import (
    FLiBeRankTwoRegisteredDensityCorrespondence,
    compare_flibe_rank_two_registered_density,
)
from tr_eif.flibe.registered_density_cross_model import (
    MODEL_DENSITY_STATISTIC,
    FLiBeDensityObservableMapping,
)
from tr_eif.flibe.registered_density_sources import (
    FLiBeRegisteredDensityRecord,
    load_flibe_density_source_records,
)
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind
from tr_eif.flibe.trajectory_state_correspondence import (
    FLiBeDensitySourceCoordinates,
    FLiBePressureRole,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.ternary import TernaryState

# Register the complete transitive pytest fixture chain.
from test_flibe_rank_two_tr_eip_pressure_coupled_trajectory import (
    prepared_trajectory as prepared_trajectory,
)
from test_flibe_rank_two_tr_eip_pressure_coupled_observables import (
    observed as observed,
)


ROOT = Path(__file__).resolve().parents[2]
VIDRIO = ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
BARAL = ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
NORMALIZATION = "source-reported-mass-density"
PROVENANCE = ParameterProvenance.TEST_FIXTURE


def _mapping(normalization=NORMALIZATION):
    return FLiBeDensityObservableMapping(
        mapping_id="RANK-TWO-DENSITY-STATE-CORRESPONDENCE",
        model_statistic_id=MODEL_DENSITY_STATISTIC,
        source_normalization_id=normalization,
        method_id="POST-BAROSTAT-OBSERVED-COORDINATES",
        provenance=PROVENANCE,
        assumptions=(
            "fixed-mass-inventory",
            "arithmetic-mean-instantaneous-density",
        ),
    )


def _compare(observables, records, **changes):
    parameters = dict(
        model_id="RANK-TWO-TR-EIP-TEST",
        trajectory_id="PRESSURE-COUPLED-THREE-INTERVALS",
        physical_state_id="DECLARED-TEST-STATE",
        physical_state_method_id="FIXTURE-STATE-IDENTITY",
        observed_pressure_method_id="POST-BAROSTAT-HYDROSTATIC-PRESSURE",
        mapping=_mapping(),
        provenance=PROVENANCE,
        temperature_tolerance_k=1.0e-8,
        pressure_tolerance_pa=1.0e-5,
    )
    parameters.update(changes)
    return compare_flibe_rank_two_registered_density(
        observables, records, **parameters,
    )


@pytest.fixture(scope="module")
def sources():
    return (
        load_flibe_density_source_records(VIDRIO),
        load_flibe_density_source_records(BARAL),
    )


@pytest.fixture(scope="module")
def comparisons(observed, sources):
    _, observables = observed
    return (
        observables,
        _compare(observables, sources[0]),
        _compare(observables, sources[1]),
    )


def _source_record(index, coordinates):
    return FLiBeRegisteredDensityRecord(
        dataset_id="RANK-TWO-STATE-TEST-DATASET",
        record_id=f"RANK-TWO-STATE-TEST-DATASET/{index}",
        doi="TEST-FIXTURE-NO-PUBLICATION",
        source_location="Synthetic physical-coordinate fixture",
        source_file_sha256="0123456789abcdef" * 4,
        run_id="ANALYTIC",
        row_index=index,
        source_columns=("temperature_k", "density_kg_m3"),
        source_values=(
            coordinates.temperature_k,
            coordinates.density_kg_m3,
        ),
        coordinates=coordinates,
    )


def test_registered_sources_preserve_record_order_fingerprint_and_uncertainty(
    comparisons, sources,
):
    _, vidrio, baral = comparisons
    for report, records, count, kind in (
        (vidrio, sources[0], 61, FLiBeEvidenceKind.EXPERIMENTAL),
        (baral, sources[1], 9, FLiBeEvidenceKind.FIRST_PRINCIPLES),
    ):
        assert isinstance(report, FLiBeRankTwoRegisteredDensityCorrespondence)
        assert len(records) == len(report.comparison.rows) == count
        assert tuple(
            row.source_record for row in report.comparison.rows
        ) == records
        assert report.comparison.source_dataset_id == records[0].dataset_id
        assert report.comparison.source_file_sha256 == records[0].source_file_sha256
        assert all(
            row.source_record.coordinates.evidence_kind is kind
            for row in report.comparison.rows
        )
        assert all(
            row.source_record.coordinates == record.coordinates
            for row, record in zip(
                report.comparison.rows, records, strict=True,
            )
        )
        assert report.matched_source_count + report.unmatched_source_count == count

    assert sources[0][0].coordinates.density_standard_uncertainty_kg_m3 is not None
    assert sources[1][0].coordinates.pressure_pa is None


@pytest.mark.parametrize("first,stride,expected", (
    (0, 1, (0, 1, 2)),
    (0, 2, (0, 2)),
    (1, 1, (1, 2)),
    (1, 2, (1,)),
    (2, 1, (2,)),
))
def test_selected_frames_use_independent_mass_volume_and_clock_evidence(
    observed, sources, first, stride, expected,
):
    trajectory, observables = observed
    result = _compare(
        observables, sources[0],
        first_interval_index=first,
        stride=stride,
    )

    assert result.observables is observables
    assert result.selected_interval_indices == expected

    density_trace = result.model_coordinates.density_trace
    assert density_trace.sample_count == len(expected)
    assert (
        result.model_coordinates.degrees_of_freedom
        == observables.degrees_of_freedom
    )

    for k, index in enumerate(expected):
        recorded = density_trace.samples[k]
        sample = observables.samples[index]
        state = trajectory.steps[index].barostat.current.md_state
        mass_kg = (
            fsum(state.masses)
            * trajectory.steps[index].pressure.mass_unit_to_kg
        )

        assert recorded.state_index == index + 1
        assert recorded.md_step == state.step == sample.md_step
        assert recorded.md_time == state.time
        assert recorded.cell_volume_m3 == sample.volume_m3
        assert recorded.density_kg_m3 == pytest.approx(
            mass_kg / sample.volume_m3, rel=1e-12,
        )
        assert (
            result.model_coordinates.kinetic_temperature_k[k]
            == sample.kinetic_temperature_k
        )
        assert (
            result.signed_post_barostat_pressures_pa[k]
            == sample.total_pressure_pa
        )
        assert recorded.density_kg_m3 > 0.0

    assert density_trace.mean_density_kg_m3 == pytest.approx(
        fsum(
            observables.samples[i].density_kg_m3 for i in expected
        ) / len(expected),
        rel=1e-12,
    )


def test_signed_pressure_is_observed_not_barostat_target(comparisons):
    observables, report, _ = comparisons
    selected = report.selected_interval_indices
    expected = fsum(
        observables.samples[i].total_pressure_pa for i in selected
    ) / len(selected)

    assert isfinite(expected)
    assert report.mean_signed_pressure_pa == expected

    coordinate = report.model_coordinates.pressure
    if expected >= 0.0:
        assert coordinate is not None
        assert coordinate.role is FLiBePressureRole.OBSERVED
        assert coordinate.pressure_pa == pytest.approx(expected, abs=1e-8)
        assert (
            coordinate.source_id
            == report.model_coordinates.density_trace.trajectory_id
        )
    else:
        assert coordinate is None
        assert all(
            row.density_residual_kg_m3 is None
            for row in report.comparison.rows
        )

    assert (
        report.observables.trajectory.target_pressure.value
        == observables.trajectory.target_pressure.value
    )


def test_registered_source_missing_axes_remain_explicit(comparisons):
    _, vidrio, baral = comparisons

    assert all(
        "physical_state" in row.missing_source_axes
        for row in vidrio.comparison.rows
    )
    assert all(
        "pressure" in row.missing_source_axes
        for row in baral.comparison.rows
    )
    assert all(
        "physical_state" in row.missing_source_axes
        for row in baral.comparison.rows
    )

    assert vidrio.matched_source_count == 0
    assert baral.matched_source_count == 0
    assert vidrio.comparison.residual_metrics is None
    assert baral.comparison.residual_metrics is None

    assert all(
        row.density_residual_kg_m3 is None
        for row in (
            *vidrio.comparison.rows,
            *baral.comparison.rows,
        )
    )


def test_exact_synthetic_state_correspondence_preserves_numerical_residual(
    comparisons,
):
    observables, baseline, _ = comparisons
    coordinates = baseline.model_coordinates
    p = coordinates.pressure

    reference = FLiBeDensitySourceCoordinates(
        density_kg_m3=coordinates.density_trace.mean_density_kg_m3 - 10.0,
        composition=coordinates.density_trace.composition,
        temperature_k=coordinates.mean_kinetic_temperature_k,
        pressure_pa=p.pressure_pa if p is not None else None,
        physical_state_id=coordinates.physical_state_id,
        normalization_id=NORMALIZATION,
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        source_id="RANK-TWO-STATE-TEST-DATASET",
        method_id="ANALYTIC-NUMERIC-FIXTURE",
        provenance=PROVENANCE,
    )

    result = _compare(
        observables, (_source_record(0, reference),),
    )
    row = result.comparison.rows[0]

    assert row.correspondence.composition_match
    assert row.correspondence.temperature_match
    assert row.correspondence.normalization_match
    assert row.correspondence.physical_state_match

    if p is None:
        assert result.matched_source_count == 0
        assert row.unmatched_axes == ("pressure",)
        assert result.comparison.residual_metrics is None
    else:
        assert result.matched_source_count == 1
        assert row.density_residual_kg_m3 == pytest.approx(
            10.0, abs=1e-9,
        )
        assert result.comparison.residual_metrics is not None
        assert result.comparison.residual_metrics.root_mean_square_kg_m3 == (
            pytest.approx(10.0)
        )


def test_normalization_mapping_mismatch_is_recorded(comparisons):
    observables, _, baral = comparisons
    changed = _compare(
        observables,
        tuple(
            row.source_record for row in baral.comparison.rows
        ),
        mapping=_mapping("DIFFERENT-MASS-DENSITY-NORMALIZATION"),
    )

    assert changed.unmatched_source_count == 9
    assert all(
        "normalization" in row.unmatched_axes
        for row in changed.comparison.rows
    )
    assert changed.comparison.residual_metrics is None


def test_active_neutral_and_pending_are_preserved_without_source_projection(
    comparisons,
):
    observables, result, _ = comparisons

    assert observables.samples[0].retained_states == (
        TernaryState.NEUTRAL,
    ) * 7
    assert observables.samples[0].pending_target_count == 7
    assert observables.samples[1].retained_states == (
        TernaryState.POSITIVE,
    ) * 7
    assert observables.samples[1].pending_target_count == 0
    assert result.observables is observables
    assert (
        result.model_coordinates.density_trace.composition.bef2_fraction
        == pytest.approx(1 / 3)
    )


def test_deterministic_source_comparison_replay(comparisons, sources):
    observables, expected, _ = comparisons
    assert _compare(observables, sources[0]) == expected


@pytest.mark.parametrize("field,value,error", (
    ("first_interval_index", -1, ValueError),
    ("first_interval_index", 3, ValueError),
    ("first_interval_index", True, TypeError),
    ("first_interval_index", 0.5, TypeError),
    ("stride", 0, ValueError),
    ("stride", -2, ValueError),
    ("stride", True, TypeError),
    ("stride", 1.5, TypeError),
    ("model_id", " ", ValueError),
    ("trajectory_id", "TRAILING ", ValueError),
    ("physical_state_id", "", ValueError),
    ("physical_state_method_id", None, TypeError),
    ("observed_pressure_method_id", " ", ValueError),
    ("mapping", None, TypeError),
    ("provenance", "TEST_FIXTURE", TypeError),
    ("temperature_tolerance_k", -1.0, ValueError),
    ("pressure_tolerance_pa", -1.0, ValueError),
))
def test_invalid_selection_identity_and_mapping_are_rejected(
    observed, sources, field, value, error,
):
    _, observables = observed
    with pytest.raises(error):
        _compare(observables, sources[0], **{field: value})


def test_mixed_registered_dataset_and_fingerprint_are_rejected(
    observed, sources,
):
    _, observables = observed

    with pytest.raises(ValueError, match="dataset identity"):
        _compare(observables, (sources[0][0], sources[1][0]))

    changed = replace(
        sources[0][1],
        source_file_sha256="abcdef0123456789" * 4,
    )
    with pytest.raises(ValueError, match="fingerprint"):
        _compare(observables, (sources[0][0], changed))


def test_corrupted_comparison_records_are_rejected(comparisons, sources):
    observables, record, _ = comparisons
    other = _compare(
        observables, sources[0], first_interval_index=1,
    )

    with pytest.raises(ValueError):
        replace(record, selected_interval_indices=())

    with pytest.raises(ValueError):
        replace(record, selected_interval_indices=(1, 0, 2))

    with pytest.raises(ValueError):
        replace(record, selected_interval_indices=(0, 0, 1))

    with pytest.raises(ValueError):
        replace(
            record,
            signed_post_barostat_pressures_pa=(
                float("nan"),
                *record.signed_post_barostat_pressures_pa[1:],
            ),
        )

    with pytest.raises(ValueError):
        replace(record, comparison=other.comparison)

    with pytest.raises(TypeError):
        replace(record, model_coordinates=None)
