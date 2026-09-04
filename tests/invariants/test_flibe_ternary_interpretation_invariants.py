"""Invariant tests for the TR-EIF FLiBe ternary-interpretation contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.flibe.ternary_interpretation import (
    FLiBeTernaryInterpretation,
    interpret_flibe_ternary_target,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.resonance import ResonanceDescriptor, ResonanceState
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryState,
    TernaryTargetThresholds,
)


def _projection() -> ResonanceProjection:
    """Return one deterministic test-only resonance projection."""

    return ResonanceProjection(
        phase_order_weight=1.0,
        frequency_spread_weight=-1.0,
        bias=0.0,
    )


def _thresholds() -> TernaryTargetThresholds:
    """Return deterministic balanced target thresholds."""

    return TernaryTargetThresholds(
        negative=-0.25,
        positive=0.25,
    )


def _interpretation() -> FLiBeTernaryInterpretation:
    """Return one deterministic test-only FLiBe ternary interpretation."""

    return FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def test_interpretation_preserves_projection_and_thresholds() -> None:
    """Interpretation construction must retain its mapping objects."""

    projection = _projection()
    thresholds = _thresholds()

    interpretation = FLiBeTernaryInterpretation(
        projection=projection,
        thresholds=thresholds,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert interpretation.projection is projection
    assert interpretation.thresholds is thresholds


def test_interpretation_preserves_provenance_and_source() -> None:
    """Interpretation construction must retain provenance metadata."""

    interpretation = FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )

    assert interpretation.provenance is ParameterProvenance.DERIVED
    assert interpretation.source == "derived-record"


@pytest.mark.parametrize(
    "invalid_projection",
    (None, True, False, 1, 1.0, "projection", (), [], {}),
)
def test_interpretation_requires_resonance_projection(
    invalid_projection,
) -> None:
    """FLiBe interpretation must require ResonanceProjection."""

    with pytest.raises(
        TypeError,
        match="projection must be a ResonanceProjection",
    ):
        FLiBeTernaryInterpretation(
            projection=invalid_projection,
            thresholds=_thresholds(),
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_thresholds",
    (None, True, False, 1, 1.0, "thresholds", (), [], {}),
)
def test_interpretation_requires_target_thresholds(
    invalid_thresholds,
) -> None:
    """FLiBe interpretation must require TernaryTargetThresholds."""

    with pytest.raises(
        TypeError,
        match="thresholds must be a TernaryTargetThresholds",
    ):
        FLiBeTernaryInterpretation(
            projection=_projection(),
            thresholds=invalid_thresholds,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_provenance",
    (
        "TEST_FIXTURE",
        "PRIMARY_SOURCE",
        None,
        True,
        False,
        1,
        1.0,
        (),
    ),
)
def test_interpretation_requires_provenance_enum(
    invalid_provenance,
) -> None:
    """FLiBe interpretation provenance must use ParameterProvenance."""

    with pytest.raises(
        TypeError,
        match="provenance must be a ParameterProvenance",
    ):
        FLiBeTernaryInterpretation(
            projection=_projection(),
            thresholds=_thresholds(),
            provenance=invalid_provenance,
        )


@pytest.mark.parametrize(
    "provenance",
    (
        ParameterProvenance.DERIVED,
        ParameterProvenance.CALIBRATED,
        ParameterProvenance.AUTHOR_DEFINED,
        ParameterProvenance.BENCHMARK,
        ParameterProvenance.TEST_FIXTURE,
        ParameterProvenance.REQUIRES_SOURCE,
        ParameterProvenance.REQUIRES_TEST,
    ),
)
def test_non_primary_interpretation_allows_missing_source(
    provenance: ParameterProvenance,
) -> None:
    """Non-primary provenance classes may omit direct source metadata."""

    interpretation = FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=_thresholds(),
        provenance=provenance,
    )

    assert interpretation.source is None


def test_primary_interpretation_requires_source() -> None:
    """PRIMARY_SOURCE interpretation must carry source metadata."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        FLiBeTernaryInterpretation(
            projection=_projection(),
            thresholds=_thresholds(),
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_primary_interpretation_accepts_source() -> None:
    """PRIMARY_SOURCE interpretation must accept explicit source metadata."""

    interpretation = FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="primary-record",
    )

    assert interpretation.source == "primary-record"


@pytest.mark.parametrize(
    ("source", "error", "message"),
    (
        ("", ValueError, "source must not be empty"),
        (
            " source",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            "source ",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            "\tsource",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            "source\n",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (True, TypeError, "source must be a string or None"),
        (False, TypeError, "source must be a string or None"),
        (1, TypeError, "source must be a string or None"),
        (1.0, TypeError, "source must be a string or None"),
        ((), TypeError, "source must be a string or None"),
        ([], TypeError, "source must be a string or None"),
        ({}, TypeError, "source must be a string or None"),
    ),
)
def test_interpretation_rejects_invalid_source_metadata(
    source,
    error,
    message: str,
) -> None:
    """Interpretation source metadata must satisfy its explicit contract."""

    with pytest.raises(error, match=message):
        FLiBeTernaryInterpretation(
            projection=_projection(),
            thresholds=_thresholds(),
            provenance=ParameterProvenance.DERIVED,
            source=source,
        )


def test_interpretation_is_frozen() -> None:
    """FLiBe ternary-interpretation records must be immutable."""

    interpretation = _interpretation()

    with pytest.raises(FrozenInstanceError):
        interpretation.source = "replacement"


@pytest.mark.parametrize(
    ("descriptor", "expected"),
    (
        (
            ResonanceDescriptor(
                phase_order=0.0,
                frequency_spread=1.0,
            ),
            TernaryState.NEGATIVE,
        ),
        (
            ResonanceDescriptor(
                phase_order=0.5,
                frequency_spread=0.5,
            ),
            TernaryState.NEUTRAL,
        ),
        (
            ResonanceDescriptor(
                phase_order=1.0,
                frequency_spread=0.0,
            ),
            TernaryState.POSITIVE,
        ),
    ),
)
def test_descriptor_path_maps_all_balanced_ternary_targets(
    descriptor: ResonanceDescriptor,
    expected: TernaryState,
) -> None:
    """Descriptor path must expose all three requested target states."""

    result = _interpretation().target_from_descriptor(
        descriptor
    )

    assert result is expected


def test_negative_threshold_is_inclusive_neutral_boundary() -> None:
    """A scalar exactly equal to the negative threshold must map to neutral."""

    descriptor = ResonanceDescriptor(
        phase_order=0.25,
        frequency_spread=0.5,
    )

    assert _projection().project(
        descriptor
    ) == -0.25

    assert (
        _interpretation().target_from_descriptor(
            descriptor
        )
        is TernaryState.NEUTRAL
    )


def test_positive_threshold_is_inclusive_neutral_boundary() -> None:
    """A scalar exactly equal to the positive threshold must map to neutral."""

    descriptor = ResonanceDescriptor(
        phase_order=0.5,
        frequency_spread=0.25,
    )

    assert _projection().project(
        descriptor
    ) == 0.25

    assert (
        _interpretation().target_from_descriptor(
            descriptor
        )
        is TernaryState.NEUTRAL
    )


def test_scalar_just_below_negative_threshold_maps_negative() -> None:
    """A scalar below the negative threshold must request NEGATIVE."""

    descriptor = ResonanceDescriptor(
        phase_order=0.249,
        frequency_spread=0.5,
    )

    assert _projection().project(
        descriptor
    ) < -0.25

    assert (
        _interpretation().target_from_descriptor(
            descriptor
        )
        is TernaryState.NEGATIVE
    )


def test_scalar_just_above_positive_threshold_maps_positive() -> None:
    """A scalar above the positive threshold must request POSITIVE."""

    descriptor = ResonanceDescriptor(
        phase_order=0.501,
        frequency_spread=0.25,
    )

    assert _projection().project(
        descriptor
    ) > 0.25

    assert (
        _interpretation().target_from_descriptor(
            descriptor
        )
        is TernaryState.POSITIVE
    )


def test_neutral_interval_includes_internal_scalar() -> None:
    """A scalar strictly between thresholds must request the NEUTRAL target."""

    descriptor = ResonanceDescriptor(
        phase_order=0.6,
        frequency_spread=0.5,
    )

    scalar = _projection().project(
        descriptor
    )

    assert -0.25 < scalar < 0.25

    assert (
        _interpretation().target_from_descriptor(
            descriptor
        )
        is TernaryState.NEUTRAL
    )


@pytest.mark.parametrize(
    "invalid_descriptor",
    (None, True, False, 1, 1.0, "descriptor", (), [], {}),
)
def test_descriptor_path_requires_resonance_descriptor(
    invalid_descriptor,
) -> None:
    """Descriptor interpretation must require ResonanceDescriptor input."""

    with pytest.raises(
        TypeError,
        match="descriptor must be a ResonanceDescriptor",
    ):
        _interpretation().target_from_descriptor(
            invalid_descriptor
        )


def test_descriptor_path_matches_base_ternary_projection_semantics() -> None:
    """FLiBe interpretation must preserve supplied generic projection semantics."""

    descriptor = ResonanceDescriptor(
        phase_order=0.9,
        frequency_spread=0.2,
    )

    interpretation = _interpretation()
    scalar = interpretation.projection.project(
        descriptor
    )

    assert scalar == pytest.approx(
        0.7
    )

    assert (
        interpretation.target_from_descriptor(
            descriptor
        )
        is TernaryState.POSITIVE
    )


def test_projection_weights_are_not_hidden_or_rewritten() -> None:
    """Interpretation must use the explicitly supplied projection."""

    descriptor = ResonanceDescriptor(
        phase_order=0.8,
        frequency_spread=0.1,
    )

    first = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=-1.0,
            bias=0.0,
        ),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    second = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=-1.0,
            frequency_spread_weight=1.0,
            bias=0.0,
        ),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert (
        first.target_from_descriptor(
            descriptor
        )
        is TernaryState.POSITIVE
    )

    assert (
        second.target_from_descriptor(
            descriptor
        )
        is TernaryState.NEGATIVE
    )


def test_projection_bias_is_applied_explicitly() -> None:
    """Projection bias must affect target generation through the projection."""

    descriptor = ResonanceDescriptor(
        phase_order=0.5,
        frequency_spread=0.5,
    )

    neutral = FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    positive = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=-1.0,
            bias=1.0,
        ),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert (
        neutral.target_from_descriptor(
            descriptor
        )
        is TernaryState.NEUTRAL
    )

    assert (
        positive.target_from_descriptor(
            descriptor
        )
        is TernaryState.POSITIVE
    )


def test_threshold_choice_is_explicit_and_changes_target() -> None:
    """Target classification must depend on the supplied threshold object."""

    descriptor = ResonanceDescriptor(
        phase_order=0.7,
        frequency_spread=0.2,
    )

    narrow = FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=TernaryTargetThresholds(
            negative=-0.1,
            positive=0.1,
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    wide = FLiBeTernaryInterpretation(
        projection=_projection(),
        thresholds=TernaryTargetThresholds(
            negative=-1.0,
            positive=1.0,
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert (
        narrow.target_from_descriptor(
            descriptor
        )
        is TernaryState.POSITIVE
    )

    assert (
        wide.target_from_descriptor(
            descriptor
        )
        is TernaryState.NEUTRAL
    )


def test_one_oscillator_resonance_state_maps_positive() -> None:
    """Resonance-state path must use the base resonance descriptor layer."""

    state = ResonanceState(
        phases=(0.0,),
        frequencies=(0.0,),
    )

    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=0.0,
            bias=0.0,
        ),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert (
        interpretation.target_from_resonance_state(
            state
        )
        is TernaryState.POSITIVE
    )


def test_one_oscillator_resonance_state_maps_neutral_with_bias() -> None:
    """Explicit bias may move the same continuous state into neutral."""

    state = ResonanceState(
        phases=(1.0,),
        frequencies=(7.0,),
    )

    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=0.0,
            bias=-1.0,
        ),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert (
        interpretation.target_from_resonance_state(
            state
        )
        is TernaryState.NEUTRAL
    )


def test_one_oscillator_resonance_state_maps_negative_with_projection_sign() -> None:
    """Explicit projection sign may map phase-order magnitude negative."""

    state = ResonanceState(
        phases=(2.0,),
        frequencies=(3.0,),
    )

    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=-1.0,
            frequency_spread_weight=0.0,
            bias=0.0,
        ),
        thresholds=_thresholds(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert (
        interpretation.target_from_resonance_state(
            state
        )
        is TernaryState.NEGATIVE
    )


@pytest.mark.parametrize(
    "invalid_state",
    (None, True, False, 1, 1.0, "state", (), [], {}),
)
def test_resonance_state_path_requires_resonance_state(
    invalid_state,
) -> None:
    """State interpretation must require ResonanceState input."""

    with pytest.raises(
        TypeError,
        match="state must be a ResonanceState",
    ):
        _interpretation().target_from_resonance_state(
            invalid_state
        )


def test_resonance_state_path_does_not_mutate_state() -> None:
    """Target generation must leave the continuous resonance state unchanged."""

    state = ResonanceState(
        phases=(0.1, 0.2, 0.3),
        frequencies=(1.0, 2.0, 3.0),
    )

    original_phases = state.phases
    original_frequencies = state.frequencies

    _interpretation().target_from_resonance_state(
        state
    )

    assert state.phases == original_phases
    assert state.frequencies == original_frequencies


def test_public_interpreter_matches_descriptor_method() -> None:
    """Public FLiBe target function must delegate to descriptor interpretation."""

    interpretation = _interpretation()

    descriptor = ResonanceDescriptor(
        phase_order=1.0,
        frequency_spread=0.0,
    )

    assert (
        interpret_flibe_ternary_target(
            interpretation,
            descriptor,
        )
        is interpretation.target_from_descriptor(
            descriptor
        )
    )


@pytest.mark.parametrize(
    "invalid_interpretation",
    (
        None,
        True,
        False,
        1,
        1.0,
        "interpretation",
        (),
        [],
        {},
    ),
)
def test_public_interpreter_requires_flibe_interpretation(
    invalid_interpretation,
) -> None:
    """Public target boundary must require FLiBeTernaryInterpretation."""

    with pytest.raises(
        TypeError,
        match=(
            "interpretation must be an "
            "FLiBeTernaryInterpretation"
        ),
    ):
        interpret_flibe_ternary_target(
            invalid_interpretation,
            ResonanceDescriptor(
                phase_order=1.0,
                frequency_spread=0.0,
            ),
        )


@pytest.mark.parametrize(
    "invalid_descriptor",
    (None, True, False, 1, 1.0, "descriptor", (), [], {}),
)
def test_public_interpreter_preserves_descriptor_validation(
    invalid_descriptor,
) -> None:
    """Public target boundary must preserve descriptor type validation."""

    with pytest.raises(
        TypeError,
        match="descriptor must be a ResonanceDescriptor",
    ):
        interpret_flibe_ternary_target(
            _interpretation(),
            invalid_descriptor,
        )


def test_target_result_is_exactly_ternary_state() -> None:
    """Interpretation output must be a balanced TernaryState target."""

    result = interpret_flibe_ternary_target(
        _interpretation(),
        ResonanceDescriptor(
            phase_order=1.0,
            frequency_spread=0.0,
        ),
    )

    assert isinstance(
        result,
        TernaryState,
    )

    assert result in (
        TernaryState.NEGATIVE,
        TernaryState.NEUTRAL,
        TernaryState.POSITIVE,
    )


def test_requested_target_contains_no_pending_route_state() -> None:
    """Interpretation must return a target rather than execution state."""

    result = _interpretation().target_from_descriptor(
        ResonanceDescriptor(
            phase_order=0.5,
            frequency_spread=0.5,
        )
    )

    assert result is TernaryState.NEUTRAL
    assert not hasattr(
        result,
        "pending_target",
    )
    assert not hasattr(
        result,
        "retained_state",
    )
    assert not hasattr(
        result,
        "route",
    )


def test_opposite_requested_targets_do_not_execute_transition() -> None:
    """Generating opposite targets must not perform ternary execution."""

    interpretation = _interpretation()

    negative = interpretation.target_from_descriptor(
        ResonanceDescriptor(
            phase_order=0.0,
            frequency_spread=1.0,
        )
    )

    positive = interpretation.target_from_descriptor(
        ResonanceDescriptor(
            phase_order=1.0,
            frequency_spread=0.0,
        )
    )

    assert negative is TernaryState.NEGATIVE
    assert positive is TernaryState.POSITIVE


def test_neutral_target_is_not_missing_data_marker() -> None:
    """A neutral result must remain an explicit semantic ternary target."""

    result = _interpretation().target_from_descriptor(
        ResonanceDescriptor(
            phase_order=0.5,
            frequency_spread=0.5,
        )
    )

    assert result is TernaryState.NEUTRAL
    assert result.value == 0


def test_ternary_target_is_not_resonance_descriptor() -> None:
    """Continuous resonance descriptor and discrete target remain distinct."""

    descriptor = ResonanceDescriptor(
        phase_order=1.0,
        frequency_spread=0.0,
    )

    target = _interpretation().target_from_descriptor(
        descriptor
    )

    assert isinstance(
        descriptor,
        ResonanceDescriptor,
    )

    assert isinstance(
        target,
        TernaryState,
    )

    assert not isinstance(
        target,
        ResonanceDescriptor,
    )


def test_phase_order_equal_to_zero_does_not_automatically_mean_neutral() -> None:
    """Zero phase order must not be assigned ternary-neutral semantics directly."""

    descriptor = ResonanceDescriptor(
        phase_order=0.0,
        frequency_spread=1.0,
    )

    assert descriptor.phase_order == 0.0

    assert (
        _interpretation().target_from_descriptor(
            descriptor
        )
        is TernaryState.NEGATIVE
    )


def test_numeric_projection_value_one_is_not_automatically_positive_target() -> None:
    """Target semantics depend on thresholds rather than numeric labels alone."""

    descriptor = ResonanceDescriptor(
        phase_order=1.0,
        frequency_spread=0.0,
    )

    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=0.0,
            bias=0.0,
        ),
        thresholds=TernaryTargetThresholds(
            negative=0.5,
            positive=2.0,
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert interpretation.projection.project(
        descriptor
    ) == 1.0

    assert (
        interpretation.target_from_descriptor(
            descriptor
        )
        is TernaryState.NEUTRAL
    )
