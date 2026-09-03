"""Balanced ternary conditioning for TR-EIF equivariant features."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)

from .features import NodeFeatures, NodeFeatureVector


@dataclass(frozen=True, slots=True)
class TernaryConditioning:
    """Explicit scalar conditioning parameters for balanced ternary states."""

    negative_scale: float
    neutral_scale: float
    positive_scale: float

    def __post_init__(self) -> None:
        for field_name, value in (
            ("negative_scale", self.negative_scale),
            ("neutral_scale", self.neutral_scale),
            ("positive_scale", self.positive_scale),
        ):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError(
                    f"{field_name} must be a real number."
                )

            value = float(value)

            if not (-float("inf") < value < float("inf")):
                raise ValueError(
                    f"{field_name} must be finite."
                )

            object.__setattr__(
                self,
                field_name,
                value,
            )

    def scale_for_state(
        self,
        state: TernaryState,
    ) -> float:
        """Return the configured conditioning scale for one ternary state."""

        if not isinstance(state, TernaryState):
            raise TypeError(
                "state must be a TernaryState instance."
            )

        if state is TernaryState.NEGATIVE:
            return self.negative_scale

        if state is TernaryState.NEUTRAL:
            return self.neutral_scale

        return self.positive_scale


def condition_node_features(
    features: NodeFeatures,
    state: TernaryState,
    conditioning: TernaryConditioning,
) -> NodeFeatures:
    """Condition one node-feature state by one retained ternary state."""

    if not isinstance(features, NodeFeatures):
        raise TypeError(
            "features must be a NodeFeatures instance."
        )

    if not isinstance(state, TernaryState):
        raise TypeError(
            "state must be a TernaryState instance."
        )

    if not isinstance(conditioning, TernaryConditioning):
        raise TypeError(
            "conditioning must be a TernaryConditioning instance."
        )

    scale = conditioning.scale_for_state(state)

    return NodeFeatures(
        scalars=tuple(
            scale * value
            for value in features.scalars
        ),
        vectors=tuple(
            (
                scale * vector[0],
                scale * vector[1],
                scale * vector[2],
            )
            for vector in features.vectors
        ),
    )


def condition_feature_vector(
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
    conditioning: TernaryConditioning,
) -> NodeFeatureVector:
    """Condition node features by the retained ternary execution vector."""

    if not isinstance(features, NodeFeatureVector):
        raise TypeError(
            "features must be a NodeFeatureVector instance."
        )

    if not isinstance(execution, TernaryExecutionVector):
        raise TypeError(
            "execution must be a TernaryExecutionVector instance."
        )

    if not isinstance(conditioning, TernaryConditioning):
        raise TypeError(
            "conditioning must be a TernaryConditioning instance."
        )

    if features.node_count != execution.node_count:
        raise ValueError(
            "feature and ternary execution node counts must match."
        )

    return NodeFeatureVector(
        nodes=tuple(
            condition_node_features(
                node_features,
                execution_state.retained_state,
                conditioning,
            )
            for node_features, execution_state in zip(
                features.nodes,
                execution.states,
                strict=True,
            )
        )
    )
