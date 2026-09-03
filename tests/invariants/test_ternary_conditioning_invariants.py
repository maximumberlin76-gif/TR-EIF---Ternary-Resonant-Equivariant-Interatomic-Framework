"""Qualification tests for TR-EIF retained-state ternary conditioning."""

import pytest

from tr_eif.equivariant import (
    NodeFeatures,
    NodeFeatureVector,
    TernaryConditioning,
    condition_feature_vector,
    condition_node_features,
)
from tr_eif.ternary import (
    TernaryExecutionGuard,
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_step,
)


def _make_conditioning() -> TernaryConditioning:
    """Construct distinct scales for all retained ternary states."""

    return TernaryConditioning(
        negative_scale=-2.0,
        neutral_scale=0.5,
        positive_scale=3.0,
    )


def _make_node_features() -> NodeFeatures:
    """Construct scalar and polar-vector feature channels."""

    return NodeFeatures(
        scalars=(
            2.0,
            -4.0,
        ),
        vectors=(
            (1.0, -2.0, 3.0),
        ),
    )


@pytest.mark.parametrize(
    ("state", "scale"),
    (
        (
            TernaryState.NEGATIVE,
            -2.0,
        ),
        (
            TernaryState.NEUTRAL,
            0.5,
        ),
        (
            TernaryState.POSITIVE,
            3.0,
        ),
    ),
)
def test_each_retained_state_uses_its_explicit_scale(
    state: TernaryState,
    scale: float,
) -> None:
    """Each balanced ternary state must use its configured scale."""

    features = _make_node_features()

    conditioned = condition_node_features(
        features,
        state,
        _make_conditioning(),
    )

    assert conditioned.scalars == pytest.approx(
        tuple(
            scale * value
            for value in features.scalars
        )
    )

    assert conditioned.vectors[0] == pytest.approx(
        tuple(
            scale * value
            for value in features.vectors[0]
        )
    )


def test_active_neutral_scale_is_not_implicitly_zero() -> None:
    """Retained active neutral must use its explicit neutral scale."""

    features = _make_node_features()

    conditioned = condition_node_features(
        features,
        TernaryState.NEUTRAL,
        _make_conditioning(),
    )

    assert conditioned.scalars == pytest.approx(
        (
            1.0,
            -2.0,
        )
    )

    assert conditioned.vectors[0] == pytest.approx(
        (
            0.5,
            -1.0,
            1.5,
        )
    )


@pytest.mark.parametrize(
    "pending_target",
    (
        TernaryState.NEGATIVE,
        TernaryState.POSITIVE,
    ),
)
def test_pending_target_does_not_replace_retained_neutral_conditioning(
    pending_target: TernaryState,
) -> None:
    """Pending polarity must not act before its committed neutral exit."""

    features = NodeFeatureVector(
        nodes=(
            _make_node_features(),
        )
    )

    execution = TernaryExecutionVector(
        states=(
            TernaryExecutionState(
                retained_state=TernaryState.NEUTRAL,
                pending_target=pending_target,
            ),
        )
    )

    conditioned = condition_feature_vector(
        features,
        execution,
        _make_conditioning(),
    )

    assert conditioned.nodes[0].scalars == pytest.approx(
        (
            1.0,
            -2.0,
        )
    )

    assert conditioned.nodes[0].vectors[0] == pytest.approx(
        (
            0.5,
            -1.0,
            1.5,
        )
    )


@pytest.mark.parametrize(
    ("initial", "requested"),
    (
        (
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
        ),
        (
            TernaryState.POSITIVE,
            TernaryState.NEGATIVE,
        ),
    ),
)
def test_opposite_route_conditions_as_neutral_after_first_leg(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """First opposite-route leg must expose neutral conditioning."""

    first_step = execute_ternary_step(
        state=TernaryExecutionState(
            retained_state=initial,
        ),
        requested_target=requested,
    )

    assert first_step.current.retained_state is TernaryState.NEUTRAL
    assert first_step.current.pending_target is requested

    features = NodeFeatureVector(
        nodes=(
            _make_node_features(),
        )
    )

    execution = TernaryExecutionVector(
        states=(
            first_step.current,
        )
    )

    conditioned = condition_feature_vector(
        features,
        execution,
        _make_conditioning(),
    )

    assert conditioned.nodes[0].scalars == pytest.approx(
        (
            1.0,
            -2.0,
        )
    )


@pytest.mark.parametrize(
    ("initial", "requested", "expected_scale"),
    (
        (
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
            3.0,
        ),
        (
            TernaryState.POSITIVE,
            TernaryState.NEGATIVE,
            -2.0,
        ),
    ),
)
def test_pending_target_scale_applies_only_after_committed_exit(
    initial: TernaryState,
    requested: TernaryState,
    expected_scale: float,
) -> None:
    """Pending polarity may condition features only after neutral exit."""

    first_step = execute_ternary_step(
        state=TernaryExecutionState(
            retained_state=initial,
        ),
        requested_target=requested,
    )

    held_step = execute_ternary_step(
        state=first_step.current,
        guard=TernaryExecutionGuard.hold(),
    )

    held_execution = TernaryExecutionVector(
        states=(
            held_step.current,
        )
    )

    features = NodeFeatureVector(
        nodes=(
            _make_node_features(),
        )
    )

    held_features = condition_feature_vector(
        features,
        held_execution,
        _make_conditioning(),
    )

    assert held_features.nodes[0].scalars == pytest.approx(
        (
            1.0,
            -2.0,
        )
    )

    exit_step = execute_ternary_step(
        state=held_step.current,
        guard=TernaryExecutionGuard.neutral_exit_only(),
    )

    assert exit_step.current.retained_state is requested
    assert exit_step.current.pending_target is None

    exited_execution = TernaryExecutionVector(
        states=(
            exit_step.current,
        )
    )

    exited_features = condition_feature_vector(
        features,
        exited_execution,
        _make_conditioning(),
    )

    assert exited_features.nodes[0].scalars == pytest.approx(
        tuple(
            expected_scale * value
            for value in features.nodes[0].scalars
        )
    )


def test_conditioning_is_independent_per_node() -> None:
    """Each node must be conditioned by its own retained ternary state."""

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(scalars=(2.0,)),
            NodeFeatures(scalars=(2.0,)),
            NodeFeatures(scalars=(2.0,)),
        )
    )

    execution = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )

    conditioned = condition_feature_vector(
        features,
        execution,
        _make_conditioning(),
    )

    assert conditioned.nodes[0].scalars == pytest.approx((-4.0,))
    assert conditioned.nodes[1].scalars == pytest.approx((1.0,))
    assert conditioned.nodes[2].scalars == pytest.approx((6.0,))
