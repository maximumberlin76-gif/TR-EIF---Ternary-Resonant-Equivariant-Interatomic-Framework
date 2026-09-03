"""Qualification tests for deterministic TR-EIF message aggregation."""

from itertools import permutations

from tr_eif.equivariant import (
    EquivariantMessage,
    aggregate_messages,
)


def _make_messages() -> tuple[EquivariantMessage, ...]:
    """Construct a deterministic multiset of equivariant messages."""

    return (
        EquivariantMessage(
            source=2,
            receiver=0,
            scalars=(1.0e16, 2.0),
            vectors=((1.0e16, 1.0, -2.0),),
        ),
        EquivariantMessage(
            source=1,
            receiver=0,
            scalars=(-1.0e16, 3.0),
            vectors=((-1.0e16, 2.0, 4.0),),
        ),
        EquivariantMessage(
            source=0,
            receiver=0,
            scalars=(1.0, -1.0),
            vectors=((1.0, -3.0, 5.0),),
        ),
        EquivariantMessage(
            source=0,
            receiver=1,
            scalars=(0.25, 4.0),
            vectors=((2.0, 0.0, 1.0),),
        ),
        EquivariantMessage(
            source=2,
            receiver=1,
            scalars=(0.75, -2.0),
            vectors=((-1.0, 3.0, 0.0),),
        ),
    )


def test_aggregation_is_identical_for_all_input_permutations() -> None:
    """One message multiset must aggregate identically in every order."""

    messages = _make_messages()

    reference = aggregate_messages(
        messages=messages,
        node_count=3,
    )

    for permutation in permutations(messages):
        candidate = aggregate_messages(
            messages=permutation,
            node_count=3,
        )

        assert candidate == reference


def test_canonical_aggregation_preserves_receiver_assignment() -> None:
    """Canonical ordering must not change message receiver semantics."""

    messages = _make_messages()

    result = aggregate_messages(
        messages=messages,
        node_count=3,
    )

    assert result.nodes[0].scalars == (
        0.0,
        4.0,
    )

    assert result.nodes[0].vectors == (
        (0.0, 0.0, 7.0),
    )

    assert result.nodes[1].scalars == (
        1.0,
        2.0,
    )

    assert result.nodes[1].vectors == (
        (1.0, 3.0, 1.0),
    )

    assert result.nodes[2].scalars == (
        0.0,
        0.0,
    )

    assert result.nodes[2].vectors == (
        (0.0, 0.0, 0.0),
    )


def test_unaddressed_node_receives_zero_feature_channels() -> None:
    """A node without incoming messages must receive explicit zero channels."""

    messages = _make_messages()

    result = aggregate_messages(
        messages=messages,
        node_count=3,
    )

    unaddressed = result.nodes[2]

    assert unaddressed.scalars == (
        0.0,
        0.0,
    )

    assert unaddressed.vectors == (
        (0.0, 0.0, 0.0),
    )


def test_repeated_aggregation_is_exactly_identical() -> None:
    """Repeated aggregation of identical input must compare exactly equal."""

    messages = _make_messages()

    first = aggregate_messages(
        messages=messages,
        node_count=3,
    )

    second = aggregate_messages(
        messages=messages,
        node_count=3,
    )

    assert first == second
