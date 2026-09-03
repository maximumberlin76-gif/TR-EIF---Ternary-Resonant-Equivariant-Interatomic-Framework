"""Integration tests for the TR-EIF resonance-to-ternary execution chain."""

import math

import pytest

from tr_eif.resonance import (
    ResonanceState,
    resonance_descriptor,
)
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionState,
    TernaryState,
    TernaryTargetThresholds,
    execute_ternary_step,
    ternary_target_from_descriptor,
    ternary_target_from_resonance_state,
)


def _make_projection() -> ResonanceProjection:
    """Construct the reference continuous-to-ternary projection."""

    return ResonanceProjection(
        phase_order_weight=1.0,
        frequency_spread_weight=-1.0,
        bias=0.0,
    )


def _make_thresholds() -> TernaryTargetThresholds:
    """Construct symmetric ternary target thresholds."""

    return TernaryTargetThresholds(
        negative=-0.25,
        positive=0.25,
    )


def _make_positive_target_state() -> ResonanceState:
    """Construct a resonance state projected above the positive threshold."""

    return ResonanceState(
        phases=(
            0.0,
            0.0,
            0.0,
            0.0,
        ),
        frequencies=(
            0.0,
            0.0,
            0.0,
            0.0,
        ),
    )


def _make_negative_target_state() -> ResonanceState:
    """Construct a resonance state projected below the negative threshold."""

    return ResonanceState(
        phases=(
            0.0,
            0.5 * math.pi,
            math.pi,
            1.5 * math.pi,
        ),
        frequencies=(
            -1.0,
            -1.0,
            1.0,
            1.0,
        ),
    )


@pytest.mark.parametrize(
    ("resonance_state", "expected_target"),
    (
        (
            _make_positive_target_state(),
            TernaryState.POSITIVE,
        ),
        (
            _make_negative_target_state(),
            TernaryState.NEGATIVE,
        ),
    ),
)
def test_resonance_state_generates_requested_ternary_target(
    resonance_state: ResonanceState,
    expected_target: TernaryState,
) -> None:
    """Continuous resonance state must generate an explicit target."""

    projection = _make_projection()
    thresholds = _make_thresholds()

    descriptor = resonance_descriptor(resonance_state)

    descriptor_target = ternary_target_from_descriptor(
        descriptor,
        projection,
        thresholds,
    )

    state_target = ternary_target_from_resonance_state(
        resonance_state,
        projection,
        thresholds,
    )

    assert descriptor_target is expected_target
    assert state_target is expected_target


@pytest.mark.parametrize(
    ("initial", "resonance_state", "expected_target"),
    (
        (
            TernaryState.NEGATIVE,
            _make_positive_target_state(),
            TernaryState.POSITIVE,
        ),
        (
            TernaryState.POSITIVE,
            _make_negative_target_state(),
            TernaryState.NEGATIVE,
        ),
    ),
)
def test_opposite_resonance_target_enters_active_neutral_first(
    initial: TernaryState,
    resonance_state: ResonanceState,
    expected_target: TernaryState,
) -> None:
    """An opposite generated target must execute through active neutral."""

    requested_target = ternary_target_from_resonance_state(
        resonance_state,
        _make_projection(),
        _make_thresholds(),
    )

    assert requested_target is expected_target

    retained = TernaryExecutionState(
        retained_state=initial,
    )

    first_step = execute_ternary_step(
        state=retained,
        requested_target=requested_target,
    )

    assert first_step.committed
    assert first_step.route is not None
    assert first_step.previous.retained_state is initial
    assert first_step.current.retained_state is TernaryState.NEUTRAL
    assert first_step.current.pending_target is expected_target

    assert first_step.route.transition.source is initial
    assert (
        first_step.route.transition.target
        is TernaryState.NEUTRAL
    )


@pytest.mark.parametrize(
    ("initial", "resonance_state", "expected_target"),
    (
        (
            TernaryState.NEGATIVE,
            _make_positive_target_state(),
            TernaryState.POSITIVE,
        ),
        (
            TernaryState.POSITIVE,
            _make_negative_target_state(),
            TernaryState.NEGATIVE,
        ),
    ),
)
def test_active_neutral_can_retain_generated_pending_target(
    initial: TernaryState,
    resonance_state: ResonanceState,
    expected_target: TernaryState,
) -> None:
    """Generated pending target must survive an active-neutral hold."""

    requested_target = ternary_target_from_resonance_state(
        resonance_state,
        _make_projection(),
        _make_thresholds(),
    )

    neutral_state = execute_ternary_step(
        state=TernaryExecutionState(
            retained_state=initial,
        ),
        requested_target=requested_target,
    ).current

    held = execute_ternary_step(
        state=neutral_state,
        guard=TernaryExecutionGuard.hold(),
    )

    assert not held.committed
    assert held.route is None
    assert held.current.retained_state is TernaryState.NEUTRAL
    assert held.current.pending_target is expected_target


@pytest.mark.parametrize(
    ("initial", "resonance_state", "expected_target"),
    (
        (
            TernaryState.NEGATIVE,
            _make_positive_target_state(),
            TernaryState.POSITIVE,
        ),
        (
            TernaryState.POSITIVE,
            _make_negative_target_state(),
            TernaryState.NEGATIVE,
        ),
    ),
)
def test_generated_opposite_target_completes_on_separate_exit_step(
    initial: TernaryState,
    resonance_state: ResonanceState,
    expected_target: TernaryState,
) -> None:
    """Pending generated target must complete on a separate neutral exit."""

    requested_target = ternary_target_from_resonance_state(
        resonance_state,
        _make_projection(),
        _make_thresholds(),
    )

    first_step = execute_ternary_step(
        state=TernaryExecutionState(
            retained_state=initial,
        ),
        requested_target=requested_target,
    )

    held_step = execute_ternary_step(
        state=first_step.current,
        guard=TernaryExecutionGuard.hold(),
    )

    exit_step = execute_ternary_step(
        state=held_step.current,
        guard=TernaryExecutionGuard.neutral_exit_only(),
    )

    assert exit_step.committed
    assert exit_step.route is not None

    assert (
        exit_step.previous.retained_state
        is TernaryState.NEUTRAL
    )
    assert (
        exit_step.previous.pending_target
        is expected_target
    )

    assert (
        exit_step.route.transition.source
        is TernaryState.NEUTRAL
    )
    assert (
        exit_step.route.transition.target
        is expected_target
    )

    assert exit_step.current.retained_state is expected_target
    assert exit_step.current.pending_target is None


@pytest.mark.parametrize(
    ("initial", "resonance_state"),
    (
        (
            TernaryState.NEGATIVE,
            _make_positive_target_state(),
        ),
        (
            TernaryState.POSITIVE,
            _make_negative_target_state(),
        ),
    ),
)
def test_full_chain_contains_no_direct_opposite_commit(
    initial: TernaryState,
    resonance_state: ResonanceState,
) -> None:
    """The integrated chain must never commit a direct opposite transition."""

    requested_target = ternary_target_from_resonance_state(
        resonance_state,
        _make_projection(),
        _make_thresholds(),
    )

    first_step = execute_ternary_step(
        state=TernaryExecutionState(
            retained_state=initial,
        ),
        requested_target=requested_target,
    )

    second_step = execute_ternary_step(
        state=first_step.current,
    )

    for step in (
        first_step,
        second_step,
    ):
        assert step.route is not None

        source = step.route.transition.source
        target = step.route.transition.target

        assert not (
            source is TernaryState.NEGATIVE
            and target is TernaryState.POSITIVE
        )

        assert not (
            source is TernaryState.POSITIVE
            and target is TernaryState.NEGATIVE
        )
