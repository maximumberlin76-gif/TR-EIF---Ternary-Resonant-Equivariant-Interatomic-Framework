"""Integration tests for explicit TR-EIF MD ternary propagation."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.ternary_propagation import (
    MolecularDynamicsTernaryStep,
    propagate_md_ternary_state,
)
from tr_eif.ternary import (
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_vector_step,
)


def _md_state(atom_count: int = 3) -> MolecularDynamicsState:
    """Construct a deterministic nonperiodic MD state."""

    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=tuple(
                f"A{index}"
                for index in range(atom_count)
            ),
            positions=tuple(
                (float(index), 0.0, 0.0)
                for index in range(atom_count)
            ),
        ),
        velocities=tuple(
            (0.1 * index, 0.0, 0.0)
            for index in range(atom_count)
        ),
        masses=tuple(
            1.0 + index
            for index in range(atom_count)
        ),
        step=8,
        time=1.5,
    )


def test_md_ternary_propagation_matches_existing_vector_executor() -> None:
    """The MD bridge must delegate execution to the existing vector operator."""

    md_state = _md_state()
    ternary_state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )
    targets = (
        TernaryState.POSITIVE,
        TernaryState.POSITIVE,
        TernaryState.NEGATIVE,
    )

    expected = execute_ternary_vector_step(
        state=ternary_state,
        requested_targets=targets,
    )

    result = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=ternary_state,
        requested_targets=targets,
    )

    assert result.execution == expected
    assert result.previous == expected.previous
    assert result.current == expected.current


def test_opposite_requests_enter_active_neutral_with_pending_targets() -> None:
    """Opposite-polarity requests must commit only the neutral-entry leg."""

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
        )
    )

    result = propagate_md_ternary_state(
        md_state=_md_state(atom_count=2),
        ternary_state=state,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.NEGATIVE,
        ),
    )

    assert result.current.retained_states == (
        TernaryState.NEUTRAL,
        TernaryState.NEUTRAL,
    )
    assert (
        result.current.states[0].pending_target
        is TernaryState.POSITIVE
    )
    assert (
        result.current.states[1].pending_target
        is TernaryState.NEGATIVE
    )
    assert result.committed_count == 2
    assert result.held_count == 0


def test_pending_opposite_route_completes_on_separate_event() -> None:
    """Neutral exit to a pending target must occur on a later event."""

    md_state = _md_state(atom_count=1)

    initial = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEGATIVE,)
    )

    first = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=initial,
        requested_targets=(
            TernaryState.POSITIVE,
        ),
    )

    assert first.current.retained_states == (
        TernaryState.NEUTRAL,
    )
    assert (
        first.current.states[0].pending_target
        is TernaryState.POSITIVE
    )

    second = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=first.current,
        requested_targets=None,
    )

    assert second.previous == first.current
    assert second.current.retained_states == (
        TernaryState.POSITIVE,
    )
    assert second.current.states[0].pending_target is None
    assert second.committed_count == 1


def test_committed_routes_never_cross_directly_between_opposites() -> None:
    """Every committed MD ternary route must preserve the core invariant."""

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
        )
    )

    result = propagate_md_ternary_state(
        md_state=_md_state(atom_count=2),
        ternary_state=state,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.NEGATIVE,
        ),
    )

    for node_step in result.execution.node_steps:
        assert node_step.route is not None

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


def test_per_node_guards_are_preserved() -> None:
    """The MD bridge must preserve independent ternary execution guards."""

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEGATIVE,
        )
    )

    result = propagate_md_ternary_state(
        md_state=_md_state(atom_count=2),
        ternary_state=state,
        requested_targets=(
            TernaryState.POSITIVE,
            TernaryState.POSITIVE,
        ),
        guards=(
            TernaryExecutionGuard.hold(),
            TernaryExecutionGuard.neutral_entry_only(),
        ),
    )

    assert (
        result.current.states[0].retained_state
        is TernaryState.NEGATIVE
    )
    assert result.current.states[0].pending_target is None

    assert (
        result.current.states[1].retained_state
        is TernaryState.NEUTRAL
    )
    assert (
        result.current.states[1].pending_target
        is TernaryState.POSITIVE
    )

    assert result.committed_count == 1
    assert result.held_count == 1


def test_md_state_is_retained_unchanged() -> None:
    """Ternary propagation must not perform a hidden MD update."""

    md_state = _md_state()

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )

    result = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=state,
        requested_targets=(
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
        ),
    )

    assert result.md_state is md_state
    assert result.md_state.configuration == md_state.configuration
    assert result.md_state.velocities == md_state.velocities
    assert result.md_state.masses == md_state.masses
    assert result.md_state.step == 8
    assert result.md_state.time == 1.5


def test_md_geometry_does_not_derive_ternary_targets() -> None:
    """Different MD coordinates must not change identical ternary execution."""

    first_md = _md_state(atom_count=2)

    second_md = MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=("A0", "A1"),
            positions=(
                (100.0, 5.0, -2.0),
                (-50.0, 7.0, 9.0),
            ),
        ),
        velocities=first_md.velocities,
        masses=first_md.masses,
        step=first_md.step,
        time=first_md.time,
    )

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
        )
    )

    targets = (
        TernaryState.POSITIVE,
        TernaryState.POSITIVE,
    )

    first = propagate_md_ternary_state(
        md_state=first_md,
        ternary_state=state,
        requested_targets=targets,
    )

    second = propagate_md_ternary_state(
        md_state=second_md,
        ternary_state=state,
        requested_targets=targets,
    )

    assert first.execution == second.execution


def test_propagation_is_deterministic() -> None:
    """Repeated propagation from identical immutable inputs must be identical."""

    md_state = _md_state()

    state = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )

    targets = (
        TernaryState.POSITIVE,
        TernaryState.NEGATIVE,
        TernaryState.NEUTRAL,
    )

    first = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=state,
        requested_targets=targets,
    )

    second = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=state,
        requested_targets=targets,
    )

    assert first == second


def test_requested_targets_are_recorded_explicitly() -> None:
    """The result must retain the request vector supplied by the caller."""

    targets = (
        TernaryState.NEUTRAL,
    )

    result = propagate_md_ternary_state(
        md_state=_md_state(atom_count=1),
        ternary_state=TernaryExecutionVector.from_retained_states(
            (
                TernaryState.POSITIVE,
            )
        ),
        requested_targets=targets,
    )

    assert result.requested_targets is targets


def test_missing_targets_without_pending_state_is_rejected() -> None:
    """No hidden target generation is permitted when no target is pending."""

    with pytest.raises(
        ValueError,
        match="requested_targets are required when no targets are pending",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=1),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=None,
        )


def test_new_request_cannot_replace_existing_pending_target() -> None:
    """A pending final target must not be overwritten by a later request."""

    md_state = _md_state(atom_count=1)

    entered = propagate_md_ternary_state(
        md_state=md_state,
        ternary_state=TernaryExecutionVector.from_retained_states(
            (
                TernaryState.NEGATIVE,
            )
        ),
        requested_targets=(
            TernaryState.POSITIVE,
        ),
    ).current

    with pytest.raises(
        ValueError,
        match="cannot replace an existing pending target",
    ):
        propagate_md_ternary_state(
            md_state=md_state,
            ternary_state=entered,
            requested_targets=(
                TernaryState.NEGATIVE,
            ),
        )


def test_ternary_node_count_must_match_md_atom_count() -> None:
    """The bridge requires one ternary execution node per MD atom."""

    with pytest.raises(
        ValueError,
        match="ternary execution node count must match MD atom count",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=2),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                TernaryState.NEUTRAL,
            ),
        )


def test_requested_target_count_must_match_md_atom_count() -> None:
    """Request vectors must contain exactly one target per MD atom."""

    with pytest.raises(
        ValueError,
        match="requested_targets must match MD atom count",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=2),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                TernaryState.POSITIVE,
            ),
        )


def test_guard_count_must_match_md_atom_count() -> None:
    """Guard vectors must contain exactly one execution guard per MD atom."""

    with pytest.raises(
        ValueError,
        match="guards must match MD atom count",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=2),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                TernaryState.NEUTRAL,
                TernaryState.NEUTRAL,
            ),
            guards=(
                TernaryExecutionGuard.unrestricted(),
            ),
        )


def test_requested_targets_must_be_tuple_or_none() -> None:
    """The MD bridge must retain the immutable request-vector contract."""

    with pytest.raises(
        TypeError,
        match="requested_targets must be a tuple or None",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=1),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=[
                TernaryState.NEUTRAL,
            ],
        )


def test_guards_must_be_tuple_or_none() -> None:
    """The MD bridge must retain the immutable guard-vector contract."""

    with pytest.raises(
        TypeError,
        match="guards must be a tuple or None",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=1),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                TernaryState.NEUTRAL,
            ),
            guards=[
                TernaryExecutionGuard.unrestricted(),
            ],
        )


def test_each_guard_must_be_execution_guard() -> None:
    """Every guard entry must satisfy the existing guard type contract."""

    with pytest.raises(
        TypeError,
        match=r"guards\[0\] must be a TernaryExecutionGuard instance",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=1),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                TernaryState.NEUTRAL,
            ),
            guards=(
                None,
            ),
        )


def test_invalid_requested_ternary_value_is_rejected() -> None:
    """Invalid request values must remain outside the -1/0/1 state space."""

    with pytest.raises(
        ValueError,
        match="ternary state must be one of -1, 0, or 1",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=1),
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                2,
            ),
        )


def test_non_md_state_is_rejected() -> None:
    """The bridge must require a MolecularDynamicsState instance."""

    with pytest.raises(
        TypeError,
        match="md_state must be a MolecularDynamicsState instance",
    ):
        propagate_md_ternary_state(
            md_state=None,
            ternary_state=TernaryExecutionVector.from_retained_states(
                (
                    TernaryState.NEUTRAL,
                )
            ),
            requested_targets=(
                TernaryState.NEUTRAL,
            ),
        )


def test_non_execution_vector_is_rejected() -> None:
    """The bridge must require the retained ternary execution-vector type."""

    with pytest.raises(
        TypeError,
        match="ternary_state must be a TernaryExecutionVector instance",
    ):
        propagate_md_ternary_state(
            md_state=_md_state(atom_count=1),
            ternary_state=(
                TernaryState.NEUTRAL,
            ),
            requested_targets=(
                TernaryState.NEUTRAL,
            ),
        )


def test_result_record_rejects_execution_size_mismatch() -> None:
    """A result cannot bind one MD atom count to another execution size."""

    execution = execute_ternary_vector_step(
        state=TernaryExecutionVector.from_retained_states(
            (
                TernaryState.NEUTRAL,
            )
        ),
        requested_targets=(
            TernaryState.POSITIVE,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "previous ternary execution node count "
            "must match MD atom count"
        ),
    ):
        MolecularDynamicsTernaryStep(
            md_state=_md_state(atom_count=2),
            requested_targets=None,
            execution=execution,
        )
