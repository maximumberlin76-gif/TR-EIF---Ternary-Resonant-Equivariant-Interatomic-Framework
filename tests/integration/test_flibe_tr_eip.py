"""Integration tests for the FLiBe-specific TR-EIP reference realization."""

from dataclasses import FrozenInstanceError
from math import pi

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.resonance_descriptor import (
    FLiBeResonanceDescriptor,
    build_flibe_resonance_descriptor,
)
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import (
    RESONANCE_SCALAR_CHANNELS,
    FLiBeTREIPModel,
    append_flibe_resonance_channels,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)


def _configuration() -> FLiBeConfiguration:
    """Construct a non-collinear exact 2 LiF : 1 BeF2 fixture."""

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=(
                "Li",
                "Li",
                "Be",
                "F",
                "F",
                "F",
                "F",
            ),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.4, 0.9, 0.2),
                (0.2, 0.3, 1.0),
                (1.1, 0.7, 0.8),
                (1.7, 0.2, 0.5),
                (0.8, 1.5, 0.4),
            ),
        )
    )


def _graph(configuration: FLiBeConfiguration):
    """Build one deterministic nonempty interaction graph."""

    return build_cutoff_graph(
        configuration.configuration,
        cutoff=1.6,
    )


def _features() -> NodeFeatureVector:
    """Construct one scalar-plus-polar-vector feature state."""

    return NodeFeatureVector(
        nodes=tuple(
            NodeFeatures(
                scalars=(0.5 + 0.25 * index,),
                vectors=((1.0, 0.1 * index, -0.05 * index),),
            )
            for index in range(7)
        )
    )


def _execution() -> TernaryExecutionVector:
    """Construct one retained -1/0/1 execution state."""

    return TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
        )
    )


def _resonance_state() -> ResonanceState:
    """Construct one deterministic continuous resonance state."""

    return ResonanceState(
        phases=(
            0.0,
            0.25 * pi,
            0.5 * pi,
            0.75 * pi,
            pi,
            1.25 * pi,
            1.5 * pi,
        ),
        frequencies=(
            -0.3,
            -0.2,
            -0.1,
            0.0,
            0.1,
            0.2,
            0.3,
        ),
    )


def _resonance_descriptor(
    configuration: FLiBeConfiguration | None = None,
    resonance_state: ResonanceState | None = None,
) -> FLiBeResonanceDescriptor:
    """Construct one FLiBe resonance descriptor from graph-relative context."""

    if configuration is None:
        configuration = _configuration()

    graph = _graph(configuration)

    return build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(
            configuration,
            graph,
        ),
        thermodynamic_state=FLiBeThermodynamicState(
            temperature=1000.0,
            pressure=0.0,
        ),
        resonance_state=(
            _resonance_state()
            if resonance_state is None
            else resonance_state
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _energy_model(
    *,
    scalar_channel_count: int = 3,
) -> ReferenceEnergyModel:
    """Construct the reference conditioned equivariant energy model."""

    weights = (0.4, 0.7, -0.3)

    if scalar_channel_count != 3:
        weights = tuple(
            0.25 + 0.1 * index
            for index in range(scalar_channel_count)
        )

    return ReferenceEnergyModel(
        message_operator=RadialMessageOperator(
            distance_scale=1.1,
        ),
        conditioning=TernaryConditioning(
            negative_scale=0.5,
            neutral_scale=1.25,
            positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=weights,
            bias=0.1,
        ),
    )


def _model(
    *,
    scalar_channel_count: int = 3,
    provenance: ParameterProvenance = ParameterProvenance.TEST_FIXTURE,
    source: str | None = None,
) -> FLiBeTREIPModel:
    """Construct one FLiBe TR-EIP model fixture."""

    return FLiBeTREIPModel(
        energy_model=_energy_model(
            scalar_channel_count=scalar_channel_count,
        ),
        provenance=provenance,
        source=source,
    )


def test_resonance_scalar_channel_contract_is_fixed() -> None:
    """The executable reference channel order must remain explicit."""

    assert RESONANCE_SCALAR_CHANNELS == (
        "phase_order",
        "frequency_spread",
    )
    assert _model().resonance_scalar_channel_count == 2


def test_append_resonance_channels_preserves_base_features() -> None:
    """Resonance augmentation must retain all existing scalar/vector channels."""

    features = _features()
    descriptor = _resonance_descriptor()

    augmented = append_flibe_resonance_channels(
        features,
        descriptor,
    )

    assert augmented.node_count == features.node_count
    assert augmented.scalar_channel_count == 3
    assert augmented.vector_channel_count == features.vector_channel_count

    for original, current in zip(
        features.nodes,
        augmented.nodes,
        strict=True,
    ):
        assert current.scalars[0] == original.scalars[0]
        assert current.scalars[1:] == pytest.approx(
            (
                descriptor.phase_order,
                descriptor.frequency_spread,
            )
        )
        assert current.vectors == original.vectors


def test_resonance_channels_are_global_invariant_scalars() -> None:
    """Each node must receive the same declared continuous resonance coordinate."""

    descriptor = _resonance_descriptor()
    augmented = append_flibe_resonance_channels(
        _features(),
        descriptor,
    )

    for node in augmented.nodes:
        assert node.scalars[-2:] == pytest.approx(
            descriptor.coordinate
        )


def test_model_evaluation_binds_all_four_architectural_layers() -> None:
    """TR-EIP must bind geometry, resonance, ternary execution, and energy."""

    configuration = _configuration()
    graph = _graph(configuration)
    features = _features()
    resonance = _resonance_descriptor(configuration)
    execution = _execution()

    result = _model().evaluate(
        configuration=configuration,
        graph=graph,
        features=features,
        resonance=resonance,
        execution=execution,
    )

    assert result.configuration is configuration
    assert result.graph is graph
    assert result.resonance is resonance
    assert result.execution is execution
    assert result.input_features is features
    assert result.energy_result.energy.atom_count == configuration.atom_count


def test_energy_model_receives_resonance_augmented_features() -> None:
    """Continuous resonance channels must enter the energy model explicitly."""

    configuration = _configuration()
    resonance = _resonance_descriptor(configuration)

    result = _model().evaluate(
        configuration=configuration,
        graph=_graph(configuration),
        features=_features(),
        resonance=resonance,
        execution=_execution(),
    )

    assert (
        result.energy_result.layer_result.input_features
        == result.resonance_conditioned_features
    )
    assert result.resonance_conditioned_features.scalar_channel_count == 3


def test_retained_ternary_state_conditions_resonance_augmented_features() -> None:
    """Retained -1/0/1 must condition the complete augmented feature vector."""

    configuration = _configuration()
    execution = _execution()
    model = _model()

    result = model.evaluate(
        configuration=configuration,
        graph=_graph(configuration),
        features=_features(),
        resonance=_resonance_descriptor(configuration),
        execution=execution,
    )

    conditioned = result.energy_result.layer_result.conditioned_features
    augmented = result.resonance_conditioned_features

    expected_scales = (
        0.5,
        1.25,
        1.5,
        1.25,
        0.5,
        1.5,
        1.25,
    )

    for original, current, scale in zip(
        augmented.nodes,
        conditioned.nodes,
        expected_scales,
        strict=True,
    ):
        assert current.scalars == pytest.approx(
            tuple(scale * value for value in original.scalars)
        )
        assert current.vectors[0] == pytest.approx(
            tuple(scale * value for value in original.vectors[0])
        )


def test_active_neutral_has_explicit_nonpassive_conditioning() -> None:
    """Neutral retained state must use its configured active scaling channel."""

    configuration = _configuration()
    execution = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL,) * 7
    )
    model = _model()

    result = model.evaluate(
        configuration=configuration,
        graph=_graph(configuration),
        features=_features(),
        resonance=_resonance_descriptor(configuration),
        execution=execution,
    )

    augmented = result.resonance_conditioned_features
    conditioned = result.energy_result.layer_result.conditioned_features

    for before, after in zip(
        augmented.nodes,
        conditioned.nodes,
        strict=True,
    ):
        assert after.scalars == pytest.approx(
            tuple(1.25 * value for value in before.scalars)
        )


def test_pending_target_does_not_replace_retained_state_conditioning() -> None:
    """Pending target metadata must remain distinct from executed neutral state."""

    configuration = _configuration()

    states_without_pending = (
        TernaryExecutionState(
            retained_state=TernaryState.NEUTRAL,
        ),
        *(
            TernaryExecutionState(
                retained_state=TernaryState.POSITIVE,
            )
            for _ in range(6)
        ),
    )

    states_with_pending = (
        TernaryExecutionState(
            retained_state=TernaryState.NEUTRAL,
            pending_target=TernaryState.POSITIVE,
        ),
        *(
            TernaryExecutionState(
                retained_state=TernaryState.POSITIVE,
            )
            for _ in range(6)
        ),
    )

    without_pending = TernaryExecutionVector(
        states=states_without_pending
    )
    with_pending = TernaryExecutionVector(
        states=states_with_pending
    )

    model = _model()
    graph = _graph(configuration)
    features = _features()
    resonance = _resonance_descriptor(configuration)

    first = model.evaluate(
        configuration,
        graph,
        features,
        resonance,
        without_pending,
    )
    second = model.evaluate(
        configuration,
        graph,
        features,
        resonance,
        with_pending,
    )

    assert first.energy_result == second.energy_result
    assert (
        second.execution.states[0].retained_state
        is TernaryState.NEUTRAL
    )
    assert (
        second.execution.states[0].pending_target
        is TernaryState.POSITIVE
    )


def test_model_does_not_execute_ternary_transitions() -> None:
    """TR-EIP evaluation must consume but not mutate ternary execution state."""

    configuration = _configuration()
    execution = _execution()

    result = _model().evaluate(
        configuration=configuration,
        graph=_graph(configuration),
        features=_features(),
        resonance=_resonance_descriptor(configuration),
        execution=execution,
    )

    assert result.execution is execution
    assert result.execution.retained_states == execution.retained_states
    assert result.execution.has_pending_targets is False


def test_model_does_not_evolve_resonance_state() -> None:
    """TR-EIP energy evaluation must consume but not advance resonance dynamics."""

    configuration = _configuration()
    descriptor = _resonance_descriptor(configuration)
    state = descriptor.resonance_state

    result = _model().evaluate(
        configuration=configuration,
        graph=_graph(configuration),
        features=_features(),
        resonance=descriptor,
        execution=_execution(),
    )

    assert result.resonance is descriptor
    assert result.resonance.resonance_state is state


def test_resonance_state_changes_energy_with_fixed_ternary_state() -> None:
    """Continuous resonance channels must have an executable energy pathway."""

    configuration = _configuration()
    model = _model()
    graph = _graph(configuration)
    features = _features()
    execution = _execution()

    first_resonance = _resonance_descriptor(
        configuration
    )

    second_resonance = _resonance_descriptor(
        configuration,
        ResonanceState(
            phases=(0.0,) * 7,
            frequencies=(0.0,) * 7,
        ),
    )

    first = model.evaluate(
        configuration,
        graph,
        features,
        first_resonance,
        execution,
    )
    second = model.evaluate(
        configuration,
        graph,
        features,
        second_resonance,
        execution,
    )

    assert first_resonance.coordinate != second_resonance.coordinate
    assert first.energy_result.energy.total_energy != pytest.approx(
        second.energy_result.energy.total_energy
    )


def test_ternary_state_changes_energy_with_fixed_resonance_state() -> None:
    """Retained ternary conditioning must have an independent energy pathway."""

    configuration = _configuration()
    model = _model()
    graph = _graph(configuration)
    features = _features()
    resonance = _resonance_descriptor(configuration)

    negative = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEGATIVE,) * 7
    )
    positive = TernaryExecutionVector.from_retained_states(
        (TernaryState.POSITIVE,) * 7
    )

    first = model.evaluate(
        configuration,
        graph,
        features,
        resonance,
        negative,
    )
    second = model.evaluate(
        configuration,
        graph,
        features,
        resonance,
        positive,
    )

    assert first.energy_result.energy.total_energy != pytest.approx(
        second.energy_result.energy.total_energy
    )


def test_tr_eip_total_energy_is_e3_invariant() -> None:
    """The full FLiBe TR-EIP scalar energy must remain invariant under E(3)."""

    configuration = _configuration()
    features = _features()
    execution = _execution()
    resonance_state = _resonance_state()
    model = _model()

    reference = model.evaluate(
        configuration=configuration,
        graph=_graph(configuration),
        features=features,
        resonance=_resonance_descriptor(
            configuration,
            resonance_state,
        ),
        execution=execution,
    )

    transformation = E3Transformation(
        matrix=(
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        translation=(3.0, -2.0, 5.0),
    )

    transformed_configuration = FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=configuration.configuration.species,
            positions=tuple(
                transformation.transform_position(position)
                for position in configuration.configuration.positions
            ),
        )
    )

    transformed_features = transformation.transform_feature_vector(
        features
    )

    transformed = model.evaluate(
        configuration=transformed_configuration,
        graph=_graph(transformed_configuration),
        features=transformed_features,
        resonance=_resonance_descriptor(
            transformed_configuration,
            resonance_state,
        ),
        execution=execution,
    )

    assert transformed.resonance.coordinate == pytest.approx(
        reference.resonance.coordinate
    )

    assert transformed.energy_result.energy.total_energy == pytest.approx(
        reference.energy_result.energy.total_energy,
        rel=1.0e-12,
        abs=1.0e-12,
    )


def test_energy_functional_channel_count_must_include_resonance_channels() -> None:
    """Energy width must equal base scalar channels plus resonance channels."""

    configuration = _configuration()

    with pytest.raises(
        ValueError,
        match=(
            "energy functional scalar channel count must match "
            "base feature channels plus FLiBe resonance channels"
        ),
    ):
        _model(
            scalar_channel_count=2,
        ).evaluate(
            configuration=configuration,
            graph=_graph(configuration),
            features=_features(),
            resonance=_resonance_descriptor(configuration),
            execution=_execution(),
        )


def test_feature_node_count_must_match_configuration() -> None:
    """TR-EIP requires one feature node per FLiBe atom."""

    configuration = _configuration()

    truncated = NodeFeatureVector(
        nodes=_features().nodes[:-1]
    )

    with pytest.raises(
        ValueError,
        match="feature node count must match FLiBe configuration atom count",
    ):
        _model().evaluate(
            configuration=configuration,
            graph=_graph(configuration),
            features=truncated,
            resonance=_resonance_descriptor(configuration),
            execution=_execution(),
        )


def test_ternary_node_count_must_match_configuration() -> None:
    """TR-EIP requires one retained ternary execution node per atom."""

    configuration = _configuration()

    truncated = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL,) * 6
    )

    with pytest.raises(
        ValueError,
        match=(
            "ternary execution node count must match "
            "FLiBe configuration atom count"
        ),
    ):
        _model().evaluate(
            configuration=configuration,
            graph=_graph(configuration),
            features=_features(),
            resonance=_resonance_descriptor(configuration),
            execution=truncated,
        )


def test_resonance_configuration_must_match_model_configuration() -> None:
    """A resonance descriptor cannot be rebound to another atomic geometry."""

    configuration = _configuration()

    other = FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=configuration.configuration.species,
            positions=tuple(
                (x + 10.0, y, z)
                for x, y, z in configuration.configuration.positions
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "resonance descriptor configuration must match "
            "TR-EIP configuration"
        ),
    ):
        _model().evaluate(
            configuration=configuration,
            graph=_graph(configuration),
            features=_features(),
            resonance=_resonance_descriptor(other),
            execution=_execution(),
        )


def test_append_resonance_channels_rejects_node_count_mismatch() -> None:
    """Resonance augmentation must not broadcast across another node count."""

    truncated = NodeFeatureVector(
        nodes=_features().nodes[:-1]
    )

    with pytest.raises(
        ValueError,
        match="feature node count must match FLiBe configuration atom count",
    ):
        append_flibe_resonance_channels(
            truncated,
            _resonance_descriptor(),
        )


def test_model_provenance_contract() -> None:
    """TR-EIP realization provenance must remain explicit."""

    model = _model(
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="FLIBE-PRIMARY-TEST",
    )

    assert model.provenance is ParameterProvenance.PRIMARY_SOURCE
    assert model.source == "FLIBE-PRIMARY-TEST"


@pytest.mark.parametrize(
    ("source", "exception", "message"),
    (
        (
            "",
            ValueError,
            "source must not be empty",
        ),
        (
            " source",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            True,
            TypeError,
            "source must be a string or None",
        ),
    ),
)
def test_invalid_model_source_metadata_is_rejected(
    source: object,
    exception: type[Exception],
    message: str,
) -> None:
    """TR-EIP source metadata must satisfy the provenance contract."""

    with pytest.raises(
        exception,
        match=message,
    ):
        _model(
            source=source,  # type: ignore[arg-type]
        )


def test_primary_source_model_requires_source() -> None:
    """PRIMARY_SOURCE provenance cannot omit its source anchor."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        _model(
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_model_is_frozen() -> None:
    """The configured TR-EIP realization must be immutable."""

    model = _model()

    with pytest.raises(FrozenInstanceError):
        model.source = "replacement"  # type: ignore[misc]


def test_evaluation_is_deterministic() -> None:
    """Identical explicit inputs must reproduce the same TR-EIP result."""

    configuration = _configuration()
    graph = _graph(configuration)
    features = _features()
    resonance = _resonance_descriptor(configuration)
    execution = _execution()
    model = _model()

    first = model.evaluate(
        configuration,
        graph,
        features,
        resonance,
        execution,
    )

    second = model.evaluate(
        configuration,
        graph,
        features,
        resonance,
        execution,
    )

    assert first == second
