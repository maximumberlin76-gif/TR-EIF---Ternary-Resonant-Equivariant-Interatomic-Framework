"""Conservative rank-two energy and force interfaces for TR-EIF.

The reference scalar/vector energy and an E(3)-invariant rank-two energy
readout share one ternary-conditioned message-passing result. Each tensor
channel contributes a trace and the squared norms of its isotropic,
symmetric-traceless, and antisymmetric parts with declared coefficients.
The full atomic energy is the sum of the two contributions.

Coordinate forces are negative central-difference derivatives of that same
full energy with fixed graph topology, retained ternary execution, resonance
feature inputs, and tensor feature inputs during each differentiation.
Continuous resonance updates and ternary transitions retain their separately
scheduled energy boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant.rank_two import RankTwoFeatureVector, ScalarVectorTensorFeatures
from tr_eif.equivariant.rank_two_message_passing import (
    RankTwoConditionedLayerResult,
    RankTwoMessageCoupling,
    rank_two_conditioned_layer_step,
)
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .differentiation import CoordinateDifferentiation
from .force import ForceState
from .model import ReferenceEnergyModel
from .state import EnergyState


def _finite_coefficient(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite.")
    return number


@dataclass(frozen=True, slots=True)
class RankTwoChannelEnergyWeights:
    """Energy coefficients for invariant contractions of one tensor channel."""

    trace: float = 0.0
    isotropic_norm_squared: float = 0.0
    symmetric_traceless_norm_squared: float = 0.0
    antisymmetric_norm_squared: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "trace",
            "isotropic_norm_squared",
            "symmetric_traceless_norm_squared",
            "antisymmetric_norm_squared",
        ):
            object.__setattr__(
                self, name, _finite_coefficient(getattr(self, name), name),
            )


@dataclass(frozen=True, slots=True)
class RankTwoInvariantEnergyReadout:
    """Invariant per-atom scalar energy from typed rank-two feature channels."""

    channel_weights: tuple[RankTwoChannelEnergyWeights, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.channel_weights, tuple):
            raise TypeError("channel_weights must be a tuple.")
        if not self.channel_weights:
            raise ValueError("at least one tensor channel weight is required.")
        if any(not isinstance(w, RankTwoChannelEnergyWeights) for w in self.channel_weights):
            raise TypeError("every tensor channel requires RankTwoChannelEnergyWeights.")

    @property
    def tensor_channel_count(self) -> int:
        return len(self.channel_weights)

    def evaluate(self, features: RankTwoFeatureVector) -> EnergyState:
        """Contract each rank-two channel to invariant scalar energy."""
        if not isinstance(features, RankTwoFeatureVector):
            raise TypeError("features must be RankTwoFeatureVector.")
        if features.tensor_channel_count != self.tensor_channel_count:
            raise ValueError("tensor feature and readout channel counts differ.")
        atomic_energies = []
        for channels in features.nodes:
            terms = []
            for tensor, weights in zip(channels, self.channel_weights, strict=True):
                isotropic, symmetric_traceless, antisymmetric = tensor.cartesian_decomposition()
                terms.append(fsum((
                    weights.trace * tensor.trace,
                    weights.isotropic_norm_squared * isotropic.frobenius_norm_squared,
                    weights.symmetric_traceless_norm_squared
                    * symmetric_traceless.frobenius_norm_squared,
                    weights.antisymmetric_norm_squared
                    * antisymmetric.frobenius_norm_squared,
                )))
            atomic_energies.append(fsum(terms))
        return EnergyState.from_atomic_energies(tuple(atomic_energies))


@dataclass(frozen=True, slots=True)
class RankTwoConservativeEnergyResult:
    """Separate scalar/vector and tensor energies with their summed total."""

    layer: RankTwoConditionedLayerResult
    reference_energy: EnergyState
    tensor_energy: EnergyState
    energy: EnergyState

    def __post_init__(self) -> None:
        if not isinstance(self.layer, RankTwoConditionedLayerResult):
            raise TypeError("layer must be RankTwoConditionedLayerResult.")
        for name in ("reference_energy", "tensor_energy", "energy"):
            if not isinstance(getattr(self, name), EnergyState):
                raise TypeError(f"{name} must be EnergyState.")
            if getattr(self, name).atom_count != self.layer.current.node_count:
                raise ValueError("energy and layer atom counts differ.")
        for reference, tensor, total in zip(
            self.reference_energy.atomic_energies,
            self.tensor_energy.atomic_energies,
            self.energy.atomic_energies,
            strict=True,
        ):
            if total != fsum((reference, tensor)):
                raise ValueError("atomic energy contributions must sum exactly.")
        if self.energy.total_energy != sum(self.energy.atomic_energies):
            raise ValueError("total energy must equal the atomic energy sum.")


@dataclass(frozen=True, slots=True)
class RankTwoConservativeEnergyModel:
    """Add tensor-invariant readout to the existing conditioned energy model."""

    reference_model: ReferenceEnergyModel
    tensor_readout: RankTwoInvariantEnergyReadout
    coupling: RankTwoMessageCoupling

    def __post_init__(self) -> None:
        if not isinstance(self.reference_model, ReferenceEnergyModel):
            raise TypeError("reference_model must be ReferenceEnergyModel.")
        if not isinstance(self.tensor_readout, RankTwoInvariantEnergyReadout):
            raise TypeError("tensor_readout must be RankTwoInvariantEnergyReadout.")
        if not isinstance(self.coupling, RankTwoMessageCoupling):
            raise TypeError("coupling must be RankTwoMessageCoupling.")

    def evaluate(
        self,
        configuration: AtomicConfiguration,
        graph: InteractionGraph,
        features: ScalarVectorTensorFeatures,
        execution: TernaryExecutionVector,
    ) -> RankTwoConservativeEnergyResult:
        """Evaluate additive E(3)-invariant energy on one fixed input state."""
        if not isinstance(configuration, AtomicConfiguration):
            raise TypeError("configuration must be AtomicConfiguration.")
        if not isinstance(graph, InteractionGraph):
            raise TypeError("graph must be InteractionGraph.")
        if not isinstance(features, ScalarVectorTensorFeatures):
            raise TypeError("features must be ScalarVectorTensorFeatures.")
        if not isinstance(execution, TernaryExecutionVector):
            raise TypeError("execution must be TernaryExecutionVector.")
        if features.rank_two.tensor_channel_count != self.tensor_readout.tensor_channel_count:
            raise ValueError("tensor input and energy readout channel counts differ.")

        layer = rank_two_conditioned_layer_step(
            configuration=configuration,
            graph=graph,
            features=features,
            radial_operator=self.reference_model.message_operator,
            execution=execution,
            conditioning=self.reference_model.conditioning,
            coupling=self.coupling,
        )
        reference = self.reference_model.energy_functional.evaluate(layer.current.base)
        tensor = self.tensor_readout.evaluate(layer.current.rank_two)
        energy = EnergyState.from_atomic_energies(tuple(
            fsum((left, right))
            for left, right in zip(reference.atomic_energies, tensor.atomic_energies, strict=True)
        ))
        return RankTwoConservativeEnergyResult(
            layer=layer,
            reference_energy=reference,
            tensor_energy=tensor,
            energy=energy,
        )


@dataclass(frozen=True, slots=True)
class RankTwoConservativeForceEvaluator:
    """Central-difference forces derived from the complete tensor-augmented energy."""

    differentiation: CoordinateDifferentiation

    def __post_init__(self) -> None:
        if not isinstance(self.differentiation, CoordinateDifferentiation):
            raise TypeError("differentiation must be CoordinateDifferentiation.")

    def evaluate(
        self,
        model: RankTwoConservativeEnergyModel,
        configuration: AtomicConfiguration,
        graph: InteractionGraph,
        features: ScalarVectorTensorFeatures,
        execution: TernaryExecutionVector,
    ) -> ForceState:
        """Differentiate full energy with fixed graph and event-state inputs."""
        if not isinstance(model, RankTwoConservativeEnergyModel):
            raise TypeError("model must be RankTwoConservativeEnergyModel.")
        if not isinstance(configuration, AtomicConfiguration):
            raise TypeError("configuration must be AtomicConfiguration.")
        if not isinstance(graph, InteractionGraph):
            raise TypeError("graph must be InteractionGraph.")
        if not isinstance(features, ScalarVectorTensorFeatures):
            raise TypeError("features must be ScalarVectorTensorFeatures.")
        if not isinstance(execution, TernaryExecutionVector):
            raise TypeError("execution must be TernaryExecutionVector.")
        if (graph.node_count != configuration.atom_count
                or features.node_count != configuration.atom_count
                or execution.node_count != configuration.atom_count):
            raise ValueError("atom, graph, feature and execution counts differ.")

        h = self.differentiation.step
        inverse_span = self.differentiation.inverse_central_span
        forces = []
        for atom in range(configuration.atom_count):
            components = []
            for axis in range(3):
                energies = []
                for signed_step in (h, -h):
                    positions = list(configuration.positions)
                    position = list(positions[atom])
                    position[axis] += signed_step
                    positions[atom] = tuple(position)
                    trial = AtomicConfiguration(
                        species=configuration.species,
                        positions=tuple(positions),
                        cell=configuration.cell,
                        periodic=configuration.periodic,
                    )
                    energies.append(model.evaluate(
                        trial, graph, features, execution,
                    ).energy.total_energy)
                components.append(-(energies[0] - energies[1]) * inverse_span)
            forces.append(tuple(components))
        return ForceState(forces=tuple(forces))
