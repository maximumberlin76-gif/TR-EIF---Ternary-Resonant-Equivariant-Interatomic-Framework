"""FLiBe-specific TR-EIP reference realization for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy import EnergyModelResult, ReferenceEnergyModel
from tr_eif.equivariant import NodeFeatures, NodeFeatureVector
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .configuration import FLiBeConfiguration
from .resonance_descriptor import FLiBeResonanceDescriptor
from .units import ParameterProvenance


RESONANCE_SCALAR_CHANNELS = (
    "phase_order",
    "frequency_spread",
)


def _validate_source_metadata(
    source: str | None,
    provenance: ParameterProvenance,
) -> str | None:
    """Validate provenance metadata for one FLiBe TR-EIP realization."""

    if source is not None and not isinstance(source, str):
        raise TypeError(
            "source must be a string or None."
        )

    if isinstance(source, str):
        if source == "":
            raise ValueError(
                "source must not be empty."
            )

        if source != source.strip():
            raise ValueError(
                "source must not contain leading or trailing whitespace."
            )

    if (
        provenance is ParameterProvenance.PRIMARY_SOURCE
        and source is None
    ):
        raise ValueError(
            "PRIMARY_SOURCE provenance requires source."
        )

    return source


def append_flibe_resonance_channels(
    features: NodeFeatureVector,
    descriptor: FLiBeResonanceDescriptor,
) -> NodeFeatureVector:
    """Append the declared global resonance invariants to every node.

    The executable reference realization uses exactly two additional scalar
    invariant channels, in the fixed order ``phase_order`` followed by
    ``frequency_spread``. Existing scalar and vector channels are retained.

    Repeating global invariant scalars across nodes does not identify geometry,
    thermodynamic state, coordination, or ternary state with resonance.
    """

    if not isinstance(features, NodeFeatureVector):
        raise TypeError(
            "features must be a NodeFeatureVector instance."
        )

    if not isinstance(descriptor, FLiBeResonanceDescriptor):
        raise TypeError(
            "descriptor must be an FLiBeResonanceDescriptor instance."
        )

    if features.node_count != descriptor.configuration.atom_count:
        raise ValueError(
            "feature node count must match FLiBe configuration atom count."
        )

    resonance_scalars = (
        descriptor.phase_order,
        descriptor.frequency_spread,
    )

    return NodeFeatureVector(
        nodes=tuple(
            NodeFeatures(
                scalars=(
                    *node.scalars,
                    *resonance_scalars,
                ),
                vectors=node.vectors,
            )
            for node in features.nodes
        )
    )


@dataclass(frozen=True, slots=True)
class FLiBeTREIPResult:
    """Result of one FLiBe-specific TR-EIP energy evaluation."""

    configuration: FLiBeConfiguration
    graph: InteractionGraph
    resonance: FLiBeResonanceDescriptor
    execution: TernaryExecutionVector
    input_features: NodeFeatureVector
    resonance_conditioned_features: NodeFeatureVector
    energy_result: EnergyModelResult

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError(
                "configuration must be an FLiBeConfiguration instance."
            )

        if not isinstance(self.graph, InteractionGraph):
            raise TypeError(
                "graph must be an InteractionGraph instance."
            )

        if not isinstance(self.resonance, FLiBeResonanceDescriptor):
            raise TypeError(
                "resonance must be an FLiBeResonanceDescriptor instance."
            )

        if not isinstance(self.execution, TernaryExecutionVector):
            raise TypeError(
                "execution must be a TernaryExecutionVector instance."
            )

        if not isinstance(self.input_features, NodeFeatureVector):
            raise TypeError(
                "input_features must be a NodeFeatureVector instance."
            )

        if not isinstance(
            self.resonance_conditioned_features,
            NodeFeatureVector,
        ):
            raise TypeError(
                "resonance_conditioned_features must be a "
                "NodeFeatureVector instance."
            )

        if not isinstance(self.energy_result, EnergyModelResult):
            raise TypeError(
                "energy_result must be an EnergyModelResult instance."
            )

        atom_count = self.configuration.atom_count

        if self.graph.node_count != atom_count:
            raise ValueError(
                "graph node count must match FLiBe configuration atom count."
            )

        if self.execution.node_count != atom_count:
            raise ValueError(
                "ternary execution node count must match "
                "FLiBe configuration atom count."
            )

        if self.input_features.node_count != atom_count:
            raise ValueError(
                "input feature node count must match "
                "FLiBe configuration atom count."
            )

        if self.resonance_conditioned_features.node_count != atom_count:
            raise ValueError(
                "resonance-conditioned feature node count must match "
                "FLiBe configuration atom count."
            )

        if self.resonance.configuration != self.configuration:
            raise ValueError(
                "resonance descriptor configuration must match "
                "TR-EIP configuration."
            )

        if (
            self.energy_result.layer_result.input_features
            != self.resonance_conditioned_features
        ):
            raise ValueError(
                "energy model input features must equal "
                "resonance-conditioned features."
            )

        if self.energy_result.energy.atom_count != atom_count:
            raise ValueError(
                "energy atom count must match FLiBe configuration atom count."
            )


@dataclass(frozen=True, slots=True)
class FLiBeTREIPModel:
    """Reference FLiBe specialization of the TR-EIP model family.

    The realization binds four distinct layers without collapsing them:

    - FLiBe atomic configuration and E(3)-equivariant geometry;
    - continuous resonance state through invariant resonance channels;
    - retained balanced ternary execution through -1/0/1 conditioning;
    - conservative scalar energy through the existing reference energy model.

    The model does not derive ternary targets, execute ternary transitions,
    evolve resonance dynamics, or infer physical parameters. Those operations
    remain explicit upstream contracts.
    """

    energy_model: ReferenceEnergyModel
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.energy_model, ReferenceEnergyModel):
            raise TypeError(
                "energy_model must be a ReferenceEnergyModel instance."
            )

        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError(
                "provenance must be a ParameterProvenance."
            )

        normalized_source = _validate_source_metadata(
            self.source,
            self.provenance,
        )

        object.__setattr__(
            self,
            "source",
            normalized_source,
        )

    @property
    def resonance_scalar_channel_count(self) -> int:
        """Return the number of explicit resonance scalar channels."""

        return len(RESONANCE_SCALAR_CHANNELS)

    def evaluate(
        self,
        configuration: FLiBeConfiguration,
        graph: InteractionGraph,
        features: NodeFeatureVector,
        resonance: FLiBeResonanceDescriptor,
        execution: TernaryExecutionVector,
    ) -> FLiBeTREIPResult:
        """Evaluate one explicit FLiBe TR-EIP energy state.

        Continuous resonance invariants are appended as scalar E(3)-invariant
        channels. The existing reference energy model then applies retained
        ternary conditioning before equivariant message passing and scalar
        energy evaluation.

        Requested ternary targets and transition execution are intentionally
        not generated here. ``target != executed state`` remains explicit.
        """

        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError(
                "configuration must be an FLiBeConfiguration instance."
            )

        if not isinstance(graph, InteractionGraph):
            raise TypeError(
                "graph must be an InteractionGraph instance."
            )

        if not isinstance(features, NodeFeatureVector):
            raise TypeError(
                "features must be a NodeFeatureVector instance."
            )

        if not isinstance(resonance, FLiBeResonanceDescriptor):
            raise TypeError(
                "resonance must be an FLiBeResonanceDescriptor instance."
            )

        if not isinstance(execution, TernaryExecutionVector):
            raise TypeError(
                "execution must be a TernaryExecutionVector instance."
            )

        atom_count = configuration.atom_count

        if graph.node_count != atom_count:
            raise ValueError(
                "graph node count must match FLiBe configuration atom count."
            )

        if features.node_count != atom_count:
            raise ValueError(
                "feature node count must match FLiBe configuration atom count."
            )

        if execution.node_count != atom_count:
            raise ValueError(
                "ternary execution node count must match "
                "FLiBe configuration atom count."
            )

        if resonance.configuration != configuration:
            raise ValueError(
                "resonance descriptor configuration must match "
                "TR-EIP configuration."
            )

        resonance_conditioned = append_flibe_resonance_channels(
            features,
            resonance,
        )

        expected_scalar_channels = (
            features.scalar_channel_count
            + self.resonance_scalar_channel_count
        )

        if (
            self.energy_model.energy_functional.scalar_channel_count
            != expected_scalar_channels
        ):
            raise ValueError(
                "energy functional scalar channel count must match "
                "base feature channels plus FLiBe resonance channels."
            )

        energy_result = self.energy_model.evaluate(
            configuration=configuration.configuration,
            graph=graph,
            features=resonance_conditioned,
            execution=execution,
        )

        return FLiBeTREIPResult(
            configuration=configuration,
            graph=graph,
            resonance=resonance,
            execution=execution,
            input_features=features,
            resonance_conditioned_features=resonance_conditioned,
            energy_result=energy_result,
        )
