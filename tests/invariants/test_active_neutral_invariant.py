"""Qualification tests for TR-EIF active-neutral execution semantics."""

import pytest

from tr_eif.ternary import (
    TernaryExecutionGuard,
    TernaryExecutionState,
    TernaryState,
    execute_ternary_step,
)


@pytest.mark.parametrize(
    ("initial", "requested"),
    (
        (TernaryState.NEGATIVE, TernaryState.POSITIVE),
        (TernaryState.POSITIVE, TernaryState.NEGATIVE),
    ),
)
def test_pending_route_can_remain_in_active_neutral(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """A pending opposite route may remain retained in neutral."""

    initial_state = TernaryExecutionState(
        retained_state=initial,
    )

    entry_step = execute_ternary_step(
        state=initial_state,
        requested_target=requested,
    )

    neutral_state = entry_step.current

    assert neutral_state.retained_state is TernaryState.NEUTRAL
    assert neutral_state.pending_target is requested

    hold_step = execute_ternary_step(
        state=neutral_state,
        guard=TernaryExecutionGuard.hold(),
    )

    assert not hold_step.committed
    assert hold_step.route is None
    assert hold_step.current == neutral_state
    assert hold_step.current.retained_state is TernaryState.NEUTRAL
    assert hold_step.current.pending_target is requested


@pytest.mark.parametrize(
    ("initial", "requested"),
    (
        (TernaryState.NEGATIVE, TernaryState.POSITIVE),
        (TernaryState.POSITIVE, TernaryState.NEGATIVE),
    ),
)
def test_pending_target_survives_repeated_neutral_holds(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """Repeated holds must preserve retained neutral and pending target."""

    state = TernaryExecutionState(
        retained_state=initial,
    )

    state = execute_ternary_step(
        state=state,
        requested_target=requested,
    ).current

    guard = TernaryExecutionGuard.hold()

    for _ in range(4):
        step = execute_ternary_step(
            state=state,
            guard=guard,
        )

        assert not step.committed
        assert step.route is None
        assert step.current.retained_state is TernaryState.NEUTRAL
        assert step.current.pending_target is requested

        state = step.current


@pytest.mark.parametrize(
    ("initial", "requested"),
    (
        (TernaryState.NEGATIVE, TernaryState.POSITIVE),
        (TernaryState.POSITIVE, TernaryState.NEGATIVE),
    ),
)
def test_neutral_exit_guard_completes_pending_route(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """Neutral exit eligibility must complete a retained pending route."""

    state = TernaryExecutionState(
        retained_state=initial,
    )

    state = execute_ternary_step(
        state=state,
        requested_target=requested,
    ).current

    held_step = execute_ternary_step(
        state=state,
        guard=TernaryExecutionGuard.hold(),
    )

    exit_step = execute_ternary_step(
        state=held_step.current,
        guard=TernaryExecutionGuard.neutral_exit_only(),
    )

    assert exit_step.committed
    assert exit_step.route is not None
    assert exit_step.route.transition.source is TernaryState.NEUTRAL
    assert exit_step.route.transition.target is requested
    assert exit_step.current.retained_state is requested
    assert exit_step.current.pending_target is None


@pytest.mark.parametrize(
    "initial",
    (
        TernaryState.NEGATIVE,
        TernaryState.POSITIVE,
    ),
)
def test_neutral_entry_can_be_blocked_without_state_change(
    initial: TernaryState,
) -> None:
    """Blocked neutral entry must produce a hold rather than a transition."""

    requested = (
        TernaryState.POSITIVE
        if initial is TernaryState.NEGATIVE
        else TernaryState.NEGATIVE
    )

    state = TernaryExecutionState(
        retained_state=initial,
    )

    step = execute_ternary_step(
        state=state,
        requested_target=requested,
        guard=TernaryExecutionGuard.neutral_exit_only(),
    )

    assert not step.committed
    assert step.route is None
    assert step.current == state
    assert step.current.retained_state is initial
    assert step.current.pending_target is None
