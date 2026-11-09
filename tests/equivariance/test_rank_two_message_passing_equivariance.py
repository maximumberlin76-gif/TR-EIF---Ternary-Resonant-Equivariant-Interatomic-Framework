
"""Independent qualification of rank-two TR-EIF message passing.

Reconstruct radial weights, dyadic messages and receiver aggregates from
Cartesian geometry, and compare against the coupled scalar/vector/tensor
layer. Check E(3) covariance, retained ternary conditioning, pending-target
isolation, periodic images, isolated nodes and deterministic execution.
"""

from dataclasses import FrozenInstanceError, replace
from math import sqrt

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
    conditioned_equivariant_layer_step,
)
from tr_eif.equivariant.rank_two import (
    RankTwoFeatureVector,
    RankTwoTensor,
    ScalarVectorTensorFeatures,
)
from tr_eif.equivariant.rank_two_message_passing import (
    RankTwoConditionedLayerResult,
    RankTwoDirectedMessage,
    RankTwoMessageCoupling,
    rank_two_conditioned_layer_step,
)
from tr_eif.graph import InteractionGraph, build_cutoff_graph
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_vector_step,
    is_direct_opposite_transition,
)

IDENTITY = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
INVERSION = ((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, -1.0))
CUTOFF = 1.7
SCALE = 1.3
CONDITIONING = TernaryConditioning(
    negative_scale=0.5,
    neutral_scale=1.25,
    positive_scale=1.8,
)
COUPLING = RankTwoMessageCoupling(
    tensor_scale=0.7,
    scalar_dyad_scale=0.3,
    vector_dyad_scale=-0.4,
    scalar_channel_index=1,
    vector_channel_index=0,
)


def _configuration():
    return AtomicConfiguration(
        species=("A", "B", "C", "D"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.2, 1.0, 0.15),
            (8.0, 0.0, 0.0),
        ),
    )


def _features():
    base = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + i, 0.3 * i - 0.4),
            vectors=((1.0 + i * 0.2, -0.2 + i * 0.15, 0.3 - i * 0.1),),
        )
        for i in range(4)
    ))
    tensors = RankTwoFeatureVector(nodes=tuple(
        (
            RankTwoTensor((
                (1.0 + i, 0.2, -0.5),
                (0.4, 2.0 - i * 0.3, 0.1),
                (0.3, -0.2, 0.8),
            )),
            RankTwoTensor.outer(
                (1.0, i + 0.5, -0.25),
                (0.2, 1.0, 0.1 + 0.3 * i),
            ),
        )
        for i in range(4)
    ))
    return ScalarVectorTensorFeatures(base, tensors)


def _execution():
    return TernaryExecutionVector(states=(
        TernaryExecutionState(TernaryState.NEGATIVE),
        TernaryExecutionState(
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        ),
        TernaryExecutionState(TernaryState.POSITIVE),
        TernaryExecutionState(TernaryState.NEUTRAL),
    ))


def _run(
    configuration=None,
    features=None,
    execution=None,
    coupling=COUPLING,
    graph=None,
):
    configuration = _configuration() if configuration is None else configuration
    features = _features() if features is None else features
    execution = _execution() if execution is None else execution
    graph = (
        build_cutoff_graph(configuration, CUTOFF)
        if graph is None else graph
    )
    return rank_two_conditioned_layer_step(
        configuration,
        graph,
        features,
        RadialMessageOperator(SCALE),
        execution,
        CONDITIONING,
        coupling,
    )


def _tensor_close(actual, expected, *, tol=1.0e-11):
    for row, reference in zip(actual.rows, expected, strict=True):
        assert row == pytest.approx(
            reference,
            rel=1.0e-11,
            abs=tol,
        )


def _reference_message(configuration, edge, features, execution, coupling):
    """Direct Cartesian reconstruction independent of tensor-message code."""
    source, receiver = edge.source, edge.receiver
    a = configuration.positions[source]
    b = configuration.positions[receiver]
    delta = tuple(b[k] - a[k] for k in range(3))
    distance = sqrt(sum(x * x for x in delta))
    unit = tuple(x / distance for x in delta)
    weight = 1.0 / (1.0 + (distance / SCALE) ** 2)
    scale = CONDITIONING.scale_for_state(
        execution.states[source].retained_state
    )
    node = features.base.nodes[source]
    scalar = (
        node.scalars[coupling.scalar_channel_index]
        if coupling.scalar_dyad_scale else 0.0
    )
    vector = (
        node.vectors[coupling.vector_channel_index]
        if coupling.vector_dyad_scale else (0.0, 0.0, 0.0)
    )
    return tuple(
        tuple(
            tuple(
                weight * scale * (
                    coupling.tensor_scale * tensor.rows[i][j]
                    + coupling.scalar_dyad_scale * scalar * unit[i] * unit[j]
                    + 0.5 * coupling.vector_dyad_scale
                    * (vector[i] * unit[j] + unit[i] * vector[j])
                )
                for j in range(3)
            )
            for i in range(3)
        )
        for tensor in features.rank_two.nodes[source]
    )


def _transform_configuration(configuration, transform):
    cell = (
        tuple(transform.transform_vector(x) for x in configuration.cell)
        if configuration.cell is not None else None
    )
    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(
            transform.transform_position(p)
            for p in configuration.positions
        ),
        cell=cell,
        periodic=configuration.periodic,
    )


def test_result_preserves_base_layer_and_all_tensor_channels():
    configuration, features, execution = (
        _configuration(), _features(), _execution()
    )
    graph = build_cutoff_graph(configuration, CUTOFF)
    result = _run(configuration, features, execution, graph=graph)
    reference = conditioned_equivariant_layer_step(
        configuration,
        graph,
        features.base,
        execution,
        CONDITIONING,
        RadialMessageOperator(SCALE),
    )
    assert isinstance(result, RankTwoConditionedLayerResult)
    assert result.previous == features
    assert result.base_layer == reference
    assert result.current.base == reference.current
    assert result.conditioned.base == reference.conditioned_features
    assert result.current.rank_two.tensor_channel_count == 2
    assert result.receiver_message_counts == (2, 2, 2, 0)
    assert len(result.tensor_messages) == graph.edge_count == 6
    assert tuple(message.edge for message in result.tensor_messages) == tuple(
        sorted(graph.edges, key=lambda e: (e.receiver, e.source, e.image))
    )


@pytest.mark.parametrize("coupling", (
    COUPLING,
    RankTwoMessageCoupling(),
    RankTwoMessageCoupling(
        tensor_scale=0.0,
        scalar_dyad_scale=1.0,
        scalar_channel_index=0,
    ),
    RankTwoMessageCoupling(
        tensor_scale=0.0,
        vector_dyad_scale=1.0,
        vector_channel_index=0,
    ),
    RankTwoMessageCoupling(
        tensor_scale=0.0,
        scalar_dyad_scale=0.5,
        vector_dyad_scale=0.25,
        scalar_channel_index=1,
        vector_channel_index=0,
    ),
))
def test_messages_and_receiver_updates_match_independent_arithmetic(coupling):
    configuration, features, execution = (
        _configuration(), _features(), _execution()
    )
    result = _run(configuration, features, execution, coupling)
    expected_messages = tuple(
        _reference_message(
            configuration, message.edge, features, execution, coupling
        )
        for message in result.tensor_messages
    )
    for recorded, expected in zip(
        result.tensor_messages, expected_messages, strict=True
    ):
        for tensor, rows in zip(recorded.tensors, expected, strict=True):
            _tensor_close(tensor, rows)

    for receiver in range(features.node_count):
        scale = CONDITIONING.scale_for_state(
            execution.states[receiver].retained_state
        )
        for channel, original in enumerate(features.rank_two.nodes[receiver]):
            conditioned = tuple(
                tuple(scale * value for value in row)
                for row in original.rows
            )
            _tensor_close(
                result.conditioned.rank_two.nodes[receiver][channel],
                conditioned,
            )
            expected_aggregate = tuple(
                tuple(
                    sum(
                        record[channel][i][j]
                        for record, message in zip(
                            expected_messages,
                            result.tensor_messages,
                            strict=True,
                        )
                        if message.edge.receiver == receiver
                    )
                    for j in range(3)
                )
                for i in range(3)
            )
            _tensor_close(
                result.tensor_aggregated.nodes[receiver][channel],
                expected_aggregate,
            )
            _tensor_close(
                result.current.rank_two.nodes[receiver][channel],
                tuple(
                    tuple(
                        conditioned[i][j] + expected_aggregate[i][j]
                        for j in range(3)
                    )
                    for i in range(3)
                ),
            )


def test_active_neutral_pending_target_does_not_change_conditioning():
    state = _execution()
    no_pending = replace(state.states[1], pending_target=None)
    without_pending = TernaryExecutionVector(states=(
        state.states[0],
        no_pending,
        state.states[2],
        state.states[3],
    ))
    pending = _run(execution=state)
    plain = _run(execution=without_pending)
    assert pending == plain
    assert CONDITIONING.scale_for_state(TernaryState.NEUTRAL) != 0.0
    assert CONDITIONING.scale_for_state(TernaryState.NEUTRAL) != (
        CONDITIONING.scale_for_state(TernaryState.POSITIVE)
    )


@pytest.mark.parametrize("start,target", (
    (TernaryState.NEGATIVE, TernaryState.POSITIVE),
    (TernaryState.POSITIVE, TernaryState.NEGATIVE),
))
def test_opposite_state_routes_and_tensor_scaling_use_committed_legs(
    start, target
):
    initial = TernaryExecutionVector.from_retained_states((start,) * 4)
    first = execute_ternary_vector_step(
        initial, requested_targets=(target,) * 4
    )
    assert first.current.retained_states == (TernaryState.NEUTRAL,) * 4
    assert all(
        node.pending_target is target for node in first.current.states
    )
    middle = _run(execution=first.current)
    assert middle.conditioned.rank_two.nodes[0][0].trace == pytest.approx(
        CONDITIONING.neutral_scale * _features().rank_two.nodes[0][0].trace
    )
    second = execute_ternary_vector_step(first.current)
    assert second.current.retained_states == (target,) * 4
    assert not second.current.has_pending_targets
    for step in (first, second):
        assert all(
            not is_direct_opposite_transition(
                node.route.transition.source,
                node.route.transition.target,
            )
            for node in step.node_steps
            if node.route is not None
        )
    after = _run(execution=second.current)
    assert after.conditioned.rank_two.nodes[0][0].trace == pytest.approx(
        CONDITIONING.scale_for_state(target)
        * _features().rank_two.nodes[0][0].trace
    )


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (3.0, -2.0, 1.0)),
    (REFLECTION, (-1.0, 0.5, 2.0)),
    (INVERSION, (0.0, 0.0, 0.0)),
    (IDENTITY, (5.0, -3.0, 8.0)),
))
def test_complete_layer_is_e3_equivariant(matrix, translation):
    transform = E3Transformation(matrix, translation)
    configuration, features, execution = (
        _configuration(), _features(), _execution()
    )
    reference = _run(configuration, features, execution)
    rotated = _run(
        _transform_configuration(configuration, transform),
        features.transformed(transform),
        execution,
    )
    assert (
        rotated.receiver_message_counts
        == reference.receiver_message_counts
    )
    assert rotated.current.rank_two.tensor_channel_count == 2

    for old, new in zip(
        reference.tensor_messages, rotated.tensor_messages, strict=True
    ):
        assert new.edge == old.edge
        for a, b in zip(old.tensors, new.tensors, strict=True):
            _tensor_close(b, a.transformed(transform).rows)
            assert b.trace == pytest.approx(a.trace, abs=1.0e-10)
            assert b.frobenius_norm_squared == pytest.approx(
                a.frobenius_norm_squared, abs=1.0e-10
            )

    for field in ("conditioned", "current"):
        original = getattr(reference, field)
        changed = getattr(rotated, field)
        for original_node, changed_node in zip(
            original.base.nodes, changed.base.nodes, strict=True
        ):
            assert changed_node.scalars == pytest.approx(
                original_node.scalars
            )
            for vector, transformed_vector in zip(
                original_node.vectors, changed_node.vectors, strict=True
            ):
                assert transformed_vector == pytest.approx(
                    transform.transform_vector(vector), abs=1.0e-10
                )
        for original_channels, changed_channels in zip(
            original.rank_two.nodes,
            changed.rank_two.nodes,
            strict=True,
        ):
            for tensor, transformed_tensor in zip(
                original_channels, changed_channels, strict=True
            ):
                _tensor_close(
                    transformed_tensor,
                    tensor.transformed(transform).rows,
                )


def test_isolated_node_retains_conditioned_tensor_features():
    result = _run()
    assert result.receiver_message_counts[-1] == 0
    for channel in range(2):
        assert (
            result.current.rank_two.nodes[-1][channel]
            == result.conditioned.rank_two.nodes[-1][channel]
        )
        assert (
            result.tensor_aggregated.nodes[-1][channel].frobenius_norm_squared
            == 0.0
        )
    assert result.current.base.nodes[-1] == result.conditioned.base.nodes[-1]


def test_periodic_image_edges_are_shared_between_base_and_tensor_layers():
    configuration = AtomicConfiguration(
        species=("Li", "F"),
        positions=((0.2, 0.0, 0.0), (4.8, 0.0, 0.0)),
        cell=(
            (5.0, 0.0, 0.0),
            (0.0, 5.0, 0.0),
            (0.0, 0.0, 5.0),
        ),
        periodic=(True, True, True),
    )
    original = _features()
    features = ScalarVectorTensorFeatures(
        NodeFeatureVector(nodes=original.base.nodes[:2]),
        RankTwoFeatureVector(nodes=original.rank_two.nodes[:2]),
    )
    execution = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL, TernaryState.POSITIVE)
    )
    graph = build_cutoff_graph(configuration, cutoff=1.0)
    assert graph.edge_count == 2
    result = _run(configuration, features, execution, graph=graph)
    assert result.receiver_message_counts == (1, 1)
    assert tuple(m.edge for m in result.tensor_messages) == tuple(
        sorted(graph.edges, key=lambda e: (e.receiver, e.source, e.image))
    )
    assert any(edge.image != (0, 0, 0) for edge in graph.edges)
    assert result.current.rank_two.tensor_channel_count == 2


def test_repeated_execution_is_deterministic_and_frozen():
    first, second = _run(), _run()
    assert first == second
    assert first is not second
    with pytest.raises(FrozenInstanceError):
        first.current = None
    with pytest.raises(FrozenInstanceError):
        first.tensor_messages[0].edge = None


@pytest.mark.parametrize("kwargs,error", (
    ({"tensor_scale": 0.0}, ValueError),
    (
        {"tensor_scale": 0.0, "scalar_dyad_scale": 1.0},
        ValueError,
    ),
    (
        {"tensor_scale": 0.0, "vector_dyad_scale": 1.0},
        ValueError,
    ),
    ({"tensor_scale": True}, TypeError),
    ({"tensor_scale": float("nan")}, ValueError),
    ({"scalar_channel_index": True}, TypeError),
    ({"vector_channel_index": -1}, ValueError),
))
def test_invalid_coupling_configurations_are_rejected(kwargs, error):
    with pytest.raises(error):
        RankTwoMessageCoupling(**kwargs)


@pytest.mark.parametrize("name", (
    "configuration",
    "graph",
    "features",
    "radial_operator",
    "execution",
    "conditioning",
    "coupling",
))
def test_untyped_dependencies_are_rejected(name):
    configuration, features, execution = (
        _configuration(), _features(), _execution()
    )
    inputs = dict(
        configuration=configuration,
        graph=build_cutoff_graph(configuration, CUTOFF),
        features=features,
        radial_operator=RadialMessageOperator(SCALE),
        execution=execution,
        conditioning=CONDITIONING,
        coupling=COUPLING,
    )
    inputs[name] = None
    if name == "coupling":
        inputs[name] = "wrong"
    with pytest.raises(TypeError):
        rank_two_conditioned_layer_step(**inputs)


def test_rejects_out_of_range_channels_mismatched_counts_and_empty_graph():
    configuration, features, execution = (
        _configuration(), _features(), _execution()
    )
    invalid_channel = RankTwoMessageCoupling(
        tensor_scale=0.0,
        scalar_dyad_scale=1.0,
        scalar_channel_index=99,
    )
    with pytest.raises(ValueError, match="selected scalar channel"):
        _run(coupling=invalid_channel)

    wrong_nodes = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL,)
    )
    with pytest.raises(ValueError, match="node counts differ"):
        _run(execution=wrong_nodes)

    empty = InteractionGraph(node_count=4, edges=())
    with pytest.raises(ValueError, match="at least one graph edge"):
        _run(graph=empty)


def test_result_contract_detects_message_and_receiver_corruption():
    result = _run()
    with pytest.raises(ValueError, match="message accounting"):
        replace(
            result,
            tensor_messages=result.tensor_messages[:-1],
        )
    with pytest.raises(ValueError, match="receiver counts"):
        replace(
            result,
            receiver_message_counts=(2, 2, 2, 1),
        )
    with pytest.raises(ValueError, match="edge ordering"):
        replace(
            result,
            tensor_messages=result.tensor_messages[::-1],
        )
    with pytest.raises(TypeError, match="tensor_aggregated"):
        replace(result, tensor_aggregated=None)
