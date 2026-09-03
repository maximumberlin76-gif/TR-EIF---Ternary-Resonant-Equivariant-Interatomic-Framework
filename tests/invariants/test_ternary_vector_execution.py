"""Qualification tests for TR-EIF vector ternary execution."""

from tr_eif.ternary import (
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_vector_step,
)


def test_vector_execution_routes_opposite_requests_through_neutral() -> None:
    """Opposite requests must enter neutral independently per node."""

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )

    step = execute_ternary_vector_step(
        state=state,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
            TernaryState.NEGATIVE,
        ),
    )

    assert step.current.retained_states == (
        TernaryState.NEUTRAL,
        TernaryState.NEUTRAL,
        TernaryState.NEUTRAL,
    )

    assert step.current.states[0].pending_target is TernaryState.POSITIVE
    assert step.current.states[1].pending_target is None
    assert step.current.states[2].pending_target is TernaryState.NEGATIVE

    assert step.committed_count == 3
    assert step.held_count == 0


def test_vector_guards_hold_nodes_independently() -> None:
    """Per-node guards must not block eligible transitions on other nodes."""

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEGATIVE,
        )
    )

    step = execute_ternary_vector_step(
        state=state,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.POSITIVE,
        ),
        guards=(
            TernaryExecutionGuard.hold(),
            TernaryExecutionGuard.neutral_entry_only(),
        ),
    )

    assert not step.node_steps[0].committed
    assert step.node_steps[0].route is None
    assert (
        step.current.states[0].retained_state
        is TernaryState.NEGATIVE
    )
    assert step.current.states[0].pending_target is None

    assert step.node_steps[1].committed
    assert (
        step.current.states[1].retained_state
        is TernaryState.NEUTRAL
    )
    assert (
        step.current.states[1].pending_target
        is TernaryState.POSITIVE
    )

    assert step.committed_count == 1
    assert step.held_count == 1


def test_vector_pending_routes_can_complete_independently() -> None:
    """Pending neutral routes must respect independent exit eligibility."""

    initial = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
        )
    )

    entered = execute_ternary_vector_step(
        state=initial,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.NEGATIVE,
        ),
    ).current

    assert entered.has_pending_targets

    step = execute_ternary_vector_step(
        state=entered,
        guards=(
            TernaryExecutionGuard.neutral_exit_only(),
            TernaryExecutionGuard.hold(),
        ),
    )

    assert (
        step.current.states[0].retained_state
        is TernaryState.POSITIVE
    )
    assert step.current.states[0].pending_target is None

    assert (
        step.current.states[1].retained_state
        is TernaryState.NEUTRAL
    )
    assert (
        step.current.states[1].pending_target
        is TernaryState.NEGATIVE
    )

    assert step.committed_count == 1
    assert step.held_count == 1


def test_vector_commits_never_contain_direct_opposite_transition() -> None:
    """Every committed vector transition must satisfy the ternary invariant."""

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )

    first = execute_ternary_vector_step(
        state=state,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.POSITIVE,
            TernaryState.NEGATIVE,
        ),
    )

    second = execute_ternary_vector_step(
        state=first.current,
    )

    for vector_step in (first, second):
        for node_step in vector_step.node_steps:
            if node_step.route is None:
                continue

            source = node_step.route.transition.source
            target = node_step.route.transition.target

            assert not (
                source is TernaryState.NEGATIVE
                and target is TernaryState.POSITIVE
            )

            assert not (
                source is TernaryState.POSITIVE
                and target is TernaryState.NEGATIVE
            )
