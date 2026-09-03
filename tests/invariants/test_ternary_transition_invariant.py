"""Qualification tests for the TR-EIF ternary transition invariant."""

import pytest

from tr_eif.ternary import (
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
def test_opposite_request_enters_active_neutral_first(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """Opposite requests must commit only the first leg into neutral."""

    state = TernaryExecutionState(
        retained_state=initial,
    )

    step = execute_ternary_step(
        state=state,
        requested_target=requested,
    )

    assert step.committed
    assert step.previous.retained_state is initial
    assert step.current.retained_state is TernaryState.NEUTRAL
    assert step.current.pending_target is requested

    assert step.route is not None
    assert step.route.transition.source is initial
    assert step.route.transition.target is TernaryState.NEUTRAL
    assert step.route.pending_target is requested


@pytest.mark.parametrize(
    ("initial", "requested"),
    (
        (TernaryState.NEGATIVE, TernaryState.POSITIVE),
        (TernaryState.POSITIVE, TernaryState.NEGATIVE),
    ),
)
def test_pending_opposite_target_requires_second_committed_leg(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """Pending opposite targets must leave neutral on a separate step."""

    initial_state = TernaryExecutionState(
        retained_state=initial,
    )

    first_step = execute_ternary_step(
        state=initial_state,
        requested_target=requested,
    )

    assert first_step.current.retained_state is TernaryState.NEUTRAL
    assert first_step.current.pending_target is requested

    second_step = execute_ternary_step(
        state=first_step.current,
    )

    assert second_step.committed
    assert second_step.previous.retained_state is TernaryState.NEUTRAL
    assert second_step.current.retained_state is requested
    assert second_step.current.pending_target is None

    assert second_step.route is not None
    assert second_step.route.transition.source is TernaryState.NEUTRAL
    assert second_step.route.transition.target is requested


@pytest.mark.parametrize(
    ("initial", "requested"),
    (
        (TernaryState.NEGATIVE, TernaryState.POSITIVE),
        (TernaryState.POSITIVE, TernaryState.NEGATIVE),
    ),
)
def test_no_committed_step_contains_direct_opposite_transition(
    initial: TernaryState,
    requested: TernaryState,
) -> None:
    """Neither committed leg may contain a direct opposite transition."""

    state = TernaryExecutionState(
        retained_state=initial,
    )

    first_step = execute_ternary_step(
        state=state,
        requested_target=requested,
    )

    second_step = execute_ternary_step(
        state=first_step.current,
    )

    committed_steps = (
        first_step,
        second_step,
    )

    for step in committed_steps:
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
