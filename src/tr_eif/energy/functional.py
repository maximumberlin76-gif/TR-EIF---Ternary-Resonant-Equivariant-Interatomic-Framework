"""Reference invariant energy functional for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.equivariant import NodeFeatureVector

from .state import EnergyState


@dataclass(frozen=True, slots=True)
class LinearInvariantEnergyFunctional:
    """Reference linear energy functional over invariant scalar channels."""

    weights: tuple[float, ...]
    bias: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(self.weights, tuple):
            raise TypeError("weights must be a tuple.")

        if len(self.weights) == 0:
            raise ValueError("weights must not be empty.")

        validated_weights: list[float] = []

        for index, weight in enumerate(self.weights):
            if not isinstance(weight, (int, float)) or isinstance(
                weight,
                bool,
            ):
                raise TypeError(
                    f"weights[{index}] must be a real number."
                )

            if not isfinite(weight):
                raise ValueError(
                    f"weights[{index}] must be finite."
                )

            validated_weights.append(float(weight))

        if not isinstance(self.bias, (int, float)) or isinstance(
            self.bias,
            bool,
        ):
            raise TypeError("bias must be a real number.")

        if not isfinite(self.bias):
            raise ValueError("bias must be finite.")

        object.__setattr__(
            self,
            "weights",
            tuple(validated_weights),
        )
        object.__setattr__(
            self,
            "bias",
            float(self.bias),
        )

    @property
    def scalar_channel_count(self) -> int:
        """Return the required number of invariant scalar channels."""

        return len(self.weights)

    def evaluate(
        self,
        features: NodeFeatureVector,
    ) -> EnergyState:
        """Evaluate deterministic atomic and total scalar energy."""

        if not isinstance(features, NodeFeatureVector):
            raise TypeError(
                "features must be a NodeFeatureVector instance."
            )

        if features.scalar_channel_count != self.scalar_channel_count:
            raise ValueError(
                "feature scalar channel count must match energy weights."
            )

        atomic_energies = tuple(
            sum(
                weight * value
                for weight, value in zip(
                    self.weights,
                    node.scalars,
                    strict=True,
                )
            )
            + self.bias
            for node in features.nodes
        )

        return EnergyState.from_atomic_energies(
            atomic_energies
        )
