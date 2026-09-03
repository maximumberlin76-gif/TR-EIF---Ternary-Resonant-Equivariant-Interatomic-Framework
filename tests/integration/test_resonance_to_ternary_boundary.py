"""Qualification tests for the TR-EIF resonance-to-ternary boundary."""

import pytest

from tr_eif.resonance import (
    ResonanceDescriptor,
    ResonanceRegion,
    ResonanceSpace,
    ResonanceWindow,
    classify_resonance_region,
)
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryState,
    TernaryTargetThresholds,
    ternary_target_from_descriptor,
    ternary_target_from_scalar,
)


def test_resonance_region_and_ternary_state_are_distinct_types() -> None:
    """Resonance-window classification must not be a ternary state."""

    assert ResonanceRegion.OUTSIDE is not TernaryState.NEGATIVE
    assert ResonanceRegion.BOUNDARY is not TernaryState.NEUTRAL
    assert ResonanceRegion.INSIDE is not TernaryState.POSITIVE

    assert ResonanceRegion.OUTSIDE.value == "outside"
    assert ResonanceRegion.BOUNDARY.value == "boundary"
    assert ResonanceRegion.INSIDE.value == "inside"

    assert TernaryState.NEGATIVE.value == -1
    assert TernaryState.NEUTRAL.value == 0
    assert TernaryState.POSITIVE.value == 1


def test_resonance_window_classification_has_three_geometric_regions() -> None:
    """Window classification must preserve outside, boundary, and inside."""

    space = ResonanceSpace(
        dimension=2,
    )

    window = ResonanceWindow(
        space=space,
        lower=(0.25, 0.10),
        upper=(0.75, 0.50),
    )

    assert classify_resonance_region(
        (0.10, 0.30),
        window,
    ) is ResonanceRegion.OUTSIDE

    assert classify_resonance_region(
        (0.25, 0.30),
        window,
    ) is ResonanceRegion.BOUNDARY

    assert classify_resonance_region(
        (0.50, 0.30),
        window,
    ) is ResonanceRegion.INSIDE


def test_scalar_threshold_boundaries_map_to_active_neutral() -> None:
    """Both exact scalar thresholds belong to the neutral target interval."""

    thresholds = TernaryTargetThresholds(
        negative=-0.25,
        positive=0.25,
    )

    assert ternary_target_from_scalar(
        -0.250001,
        thresholds,
    ) is TernaryState.NEGATIVE

    assert ternary_target_from_scalar(
        -0.25,
        thresholds,
    ) is TernaryState.NEUTRAL

    assert ternary_target_from_scalar(
        0.0,
        thresholds,
    ) is TernaryState.NEUTRAL

    assert ternary_target_from_scalar(
        0.25,
        thresholds,
    ) is TernaryState.NEUTRAL

    assert ternary_target_from_scalar(
        0.250001,
        thresholds,
    ) is TernaryState.POSITIVE


@pytest.mark.parametrize(
    ("descriptor", "expected"),
    (
        (
            ResonanceDescriptor(
                phase_order=0.10,
                frequency_spread=0.60,
            ),
            TernaryState.NEGATIVE,
        ),
        (
            ResonanceDescriptor(
                phase_order=0.50,
                frequency_spread=0.50,
            ),
            TernaryState.NEUTRAL,
        ),
        (
            ResonanceDescriptor(
                phase_order=0.90,
                frequency_spread=0.10,
            ),
            TernaryState.POSITIVE,
        ),
    ),
)
def test_descriptor_projection_generates_requested_ternary_target(
    descriptor: ResonanceDescriptor,
    expected: TernaryState,
) -> None:
    """Continuous descriptors must pass through explicit projection."""

    projection = ResonanceProjection(
        phase_order_weight=1.0,
        frequency_spread_weight=-1.0,
        bias=0.0,
    )

    thresholds = TernaryTargetThresholds(
        negative=-0.20,
        positive=0.20,
    )

    target = ternary_target_from_descriptor(
        descriptor,
        projection,
        thresholds,
    )

    assert target is expected


def test_same_resonance_region_can_generate_different_ternary_targets() -> None:
    """Window membership alone must not determine a ternary target."""

    space = ResonanceSpace(
        dimension=2,
    )

    window = ResonanceWindow(
        space=space,
        lower=(0.0, 0.0),
        upper=(1.0, 1.0),
    )

    negative_descriptor = ResonanceDescriptor(
        phase_order=0.20,
        frequency_spread=0.80,
    )

    positive_descriptor = ResonanceDescriptor(
        phase_order=0.80,
        frequency_spread=0.20,
    )

    assert classify_resonance_region(
        negative_descriptor.as_coordinate(),
        window,
    ) is ResonanceRegion.INSIDE

    assert classify_resonance_region(
        positive_descriptor.as_coordinate(),
        window,
    ) is ResonanceRegion.INSIDE

    projection = ResonanceProjection(
        phase_order_weight=1.0,
        frequency_spread_weight=-1.0,
    )

    thresholds = TernaryTargetThresholds(
        negative=-0.25,
        positive=0.25,
    )

    assert ternary_target_from_descriptor(
        negative_descriptor,
        projection,
        thresholds,
    ) is TernaryState.NEGATIVE

    assert ternary_target_from_descriptor(
        positive_descriptor,
        projection,
        thresholds,
    ) is TernaryState.POSITIVE


def test_different_resonance_regions_can_generate_same_ternary_target() -> None:
    """Ternary projection must remain independent of window classification."""

    space = ResonanceSpace(
        dimension=2,
    )

    window = ResonanceWindow(
        space=space,
        lower=(0.25, 0.25),
        upper=(0.75, 0.75),
    )

    boundary_descriptor = ResonanceDescriptor(
        phase_order=0.25,
        frequency_spread=0.50,
    )

    outside_descriptor = ResonanceDescriptor(
        phase_order=0.10,
        frequency_spread=0.35,
    )

    assert classify_resonance_region(
        boundary_descriptor.as_coordinate(),
        window,
    ) is ResonanceRegion.BOUNDARY

    assert classify_resonance_region(
        outside_descriptor.as_coordinate(),
        window,
    ) is ResonanceRegion.OUTSIDE

    projection = ResonanceProjection(
        phase_order_weight=1.0,
        frequency_spread_weight=-1.0,
    )

    thresholds = TernaryTargetThresholds(
        negative=-0.50,
        positive=0.50,
    )

    assert ternary_target_from_descriptor(
        boundary_descriptor,
        projection,
        thresholds,
    ) is TernaryState.NEUTRAL

    assert ternary_target_from_descriptor(
        outside_descriptor,
        projection,
        thresholds,
    ) is TernaryState.NEUTRAL
