"""Explicit uncertainty-propagation contract for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty uncertainty-contract identifier."""

    if not isinstance(value, str):
        raise TypeError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{field_name} must not be empty or whitespace."
        )

    return normalized


def _validate_uncertainty_value(value: float) -> float:
    """Validate one finite nonnegative uncertainty magnitude."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            "value must be a real number."
        )

    normalized = float(value)

    if not isfinite(normalized):
        raise ValueError(
            "value must be finite."
        )

    if normalized < 0.0:
        raise ValueError(
            "value must be nonnegative."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class UncertaintyMeasure:
    """One explicit uncertainty measure for one quantity at one model scale.

    ``representation_id`` identifies the caller-selected uncertainty
    representation, such as a standard-deviation, variance, interval, or
    another externally defined measure. This record does not interpret or
    convert between uncertainty representations.
    """

    quantity_id: str
    value: float
    unit: str
    representation_id: str
    scale_id: str
    state_domain_id: str
    source_id: str

    def __post_init__(self) -> None:
        quantity_id = _validate_identifier(
            self.quantity_id,
            field_name="quantity_id",
        )
        value = _validate_uncertainty_value(
            self.value
        )
        unit = _validate_identifier(
            self.unit,
            field_name="unit",
        )
        representation_id = _validate_identifier(
            self.representation_id,
            field_name="representation_id",
        )
        scale_id = _validate_identifier(
            self.scale_id,
            field_name="scale_id",
        )
        state_domain_id = _validate_identifier(
            self.state_domain_id,
            field_name="state_domain_id",
        )
        source_id = _validate_identifier(
            self.source_id,
            field_name="source_id",
        )

        object.__setattr__(
            self,
            "quantity_id",
            quantity_id,
        )
        object.__setattr__(
            self,
            "value",
            value,
        )
        object.__setattr__(
            self,
            "unit",
            unit,
        )
        object.__setattr__(
            self,
            "representation_id",
            representation_id,
        )
        object.__setattr__(
            self,
            "scale_id",
            scale_id,
        )
        object.__setattr__(
            self,
            "state_domain_id",
            state_domain_id,
        )
        object.__setattr__(
            self,
            "source_id",
            source_id,
        )


UncertaintyMeasures: TypeAlias = tuple[
    UncertaintyMeasure,
    ...,
]


def _measure_key(
    measure: UncertaintyMeasure,
) -> tuple[str, str, str, str]:
    """Return the canonical identity key for one uncertainty measure."""

    return (
        measure.scale_id,
        measure.quantity_id,
        measure.representation_id,
        measure.source_id,
    )


def _validate_measures(
    measures: UncertaintyMeasures,
    *,
    field_name: str,
) -> UncertaintyMeasures:
    """Validate one canonical nonempty uncertainty-measure collection."""

    if not isinstance(measures, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if len(measures) == 0:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    keys: list[tuple[str, str, str, str]] = []

    for index, measure in enumerate(measures):
        if not isinstance(
            measure,
            UncertaintyMeasure,
        ):
            raise TypeError(
                f"{field_name}[{index}] must be an "
                "UncertaintyMeasure instance."
            )

        keys.append(
            _measure_key(measure)
        )

    if len(set(keys)) != len(keys):
        raise ValueError(
            f"{field_name} must not contain duplicate uncertainty identities."
        )

    if keys != sorted(keys):
        raise ValueError(
            f"{field_name} must use canonical uncertainty ordering."
        )

    return measures


@dataclass(frozen=True, slots=True)
class UncertaintyPropagationContext:
    """Explicit assumptions for one multiscale uncertainty propagation."""

    target_scale_id: str
    propagation_id: str
    assumptions_id: str
    correlation_id: str
    normalization_id: str

    def __post_init__(self) -> None:
        target_scale_id = _validate_identifier(
            self.target_scale_id,
            field_name="target_scale_id",
        )
        propagation_id = _validate_identifier(
            self.propagation_id,
            field_name="propagation_id",
        )
        assumptions_id = _validate_identifier(
            self.assumptions_id,
            field_name="assumptions_id",
        )
        correlation_id = _validate_identifier(
            self.correlation_id,
            field_name="correlation_id",
        )
        normalization_id = _validate_identifier(
            self.normalization_id,
            field_name="normalization_id",
        )

        object.__setattr__(
            self,
            "target_scale_id",
            target_scale_id,
        )
        object.__setattr__(
            self,
            "propagation_id",
            propagation_id,
        )
        object.__setattr__(
            self,
            "assumptions_id",
            assumptions_id,
        )
        object.__setattr__(
            self,
            "correlation_id",
            correlation_id,
        )
        object.__setattr__(
            self,
            "normalization_id",
            normalization_id,
        )


@dataclass(frozen=True, slots=True)
class UncertaintyPropagationRecord:
    """Result of one explicit multiscale uncertainty propagation.

    The context identifies the selected propagation rule, assumptions,
    correlation model, normalization convention, and destination scale.
    Source and target measures retain their own units, uncertainty
    representations, state domains, and provenance anchors.

    This record does not assume Gaussianity, independence, linear error
    propagation, Monte Carlo sampling, confidence level, covariance model,
    or unit conversion.
    """

    source_measures: UncertaintyMeasures
    target_measures: UncertaintyMeasures
    context: UncertaintyPropagationContext

    def __post_init__(self) -> None:
        source_measures = _validate_measures(
            self.source_measures,
            field_name="source_measures",
        )
        target_measures = _validate_measures(
            self.target_measures,
            field_name="target_measures",
        )

        if not isinstance(
            self.context,
            UncertaintyPropagationContext,
        ):
            raise TypeError(
                "context must be an UncertaintyPropagationContext instance."
            )

        for index, measure in enumerate(target_measures):
            if measure.scale_id != self.context.target_scale_id:
                raise ValueError(
                    f"target_measures[{index}] scale_id must match "
                    "context target_scale_id."
                )

        object.__setattr__(
            self,
            "source_measures",
            source_measures,
        )
        object.__setattr__(
            self,
            "target_measures",
            target_measures,
        )


UncertaintyPropagationEvaluator: TypeAlias = Callable[
    [UncertaintyMeasures, UncertaintyPropagationContext],
    UncertaintyPropagationRecord,
]


def evaluate_uncertainty_propagation(
    source_measures: UncertaintyMeasures,
    context: UncertaintyPropagationContext,
    evaluator: UncertaintyPropagationEvaluator,
) -> UncertaintyPropagationRecord:
    """Evaluate one explicit uncertainty-propagation provider.

    The complete source uncertainty collection and propagation context are
    supplied explicitly. The provider must return a record bound to those
    exact inputs.

    This function performs no distribution selection, correlation inference,
    covariance construction, linearization, sampling, confidence conversion,
    uncertainty aggregation, unit conversion, or empirical calibration.
    """

    validated_source = _validate_measures(
        source_measures,
        field_name="source_measures",
    )

    if not isinstance(
        context,
        UncertaintyPropagationContext,
    ):
        raise TypeError(
            "context must be an UncertaintyPropagationContext instance."
        )

    if not callable(evaluator):
        raise TypeError(
            "evaluator must be callable."
        )

    result = evaluator(
        validated_source,
        context,
    )

    if not isinstance(
        result,
        UncertaintyPropagationRecord,
    ):
        raise TypeError(
            "evaluator must return an UncertaintyPropagationRecord instance."
        )

    if result.source_measures != validated_source:
        raise ValueError(
            "uncertainty-propagation result source measures must match input."
        )

    if result.context != context:
        raise ValueError(
            "uncertainty-propagation result context must match input context."
        )

    return result
