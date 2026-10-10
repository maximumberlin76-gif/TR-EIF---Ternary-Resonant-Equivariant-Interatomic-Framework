"""Explicit transport-coefficient transfer contract for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty transport-transfer identifier."""

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


def _validate_value(value: float) -> float:
    """Validate one finite transport-coefficient value."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            "value must be a real number."
        )

    normalized = float(value)

    if not isfinite(normalized):
        raise ValueError(
            "value must be finite."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class TransportCoefficient:
    """One explicit transport coefficient at one declared model scale.

    The value, unit, scale, state domain, and source are supplied by the
    caller. The record performs no unit conversion, sign restriction,
    constitutive inference, or physical parameter lookup.
    """

    coefficient_id: str
    value: float
    unit: str
    scale_id: str
    state_domain_id: str
    source_id: str

    def __post_init__(self) -> None:
        coefficient_id = _validate_identifier(
            self.coefficient_id,
            field_name="coefficient_id",
        )
        value = _validate_value(
            self.value
        )
        unit = _validate_identifier(
            self.unit,
            field_name="unit",
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
            "coefficient_id",
            coefficient_id,
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


@dataclass(frozen=True, slots=True)
class TransportTransferContext:
    """Explicit assumptions and normalization for one scale transfer."""

    target_scale_id: str
    mapping_id: str
    normalization_id: str
    assumptions_id: str

    def __post_init__(self) -> None:
        target_scale_id = _validate_identifier(
            self.target_scale_id,
            field_name="target_scale_id",
        )
        mapping_id = _validate_identifier(
            self.mapping_id,
            field_name="mapping_id",
        )
        normalization_id = _validate_identifier(
            self.normalization_id,
            field_name="normalization_id",
        )
        assumptions_id = _validate_identifier(
            self.assumptions_id,
            field_name="assumptions_id",
        )

        object.__setattr__(
            self,
            "target_scale_id",
            target_scale_id,
        )
        object.__setattr__(
            self,
            "mapping_id",
            mapping_id,
        )
        object.__setattr__(
            self,
            "normalization_id",
            normalization_id,
        )
        object.__setattr__(
            self,
            "assumptions_id",
            assumptions_id,
        )


@dataclass(frozen=True, slots=True)
class TransportCoefficientTransferRecord:
    """Result of one explicit cross-scale transport-coefficient mapping.

    ``context`` identifies the selected mapping, normalization convention,
    physical-assumption set, and destination scale. The source and target
    records retain their own units, state-domain identifiers, and provenance
    anchors.

    This contract does not assert that a coefficient is scale invariant and
    does not derive one coefficient from another without an explicit external
    evaluator.
    """

    source: TransportCoefficient
    target: TransportCoefficient
    context: TransportTransferContext

    def __post_init__(self) -> None:
        if not isinstance(
            self.source,
            TransportCoefficient,
        ):
            raise TypeError(
                "source must be a TransportCoefficient instance."
            )

        if not isinstance(
            self.target,
            TransportCoefficient,
        ):
            raise TypeError(
                "target must be a TransportCoefficient instance."
            )

        if not isinstance(
            self.context,
            TransportTransferContext,
        ):
            raise TypeError(
                "context must be a TransportTransferContext instance."
            )

        if self.target.coefficient_id != self.source.coefficient_id:
            raise ValueError(
                "target coefficient_id must match source coefficient_id."
            )

        if self.target.scale_id != self.context.target_scale_id:
            raise ValueError(
                "target scale_id must match context target_scale_id."
            )


TransportCoefficientTransferEvaluator: TypeAlias = Callable[
    [TransportCoefficient, TransportTransferContext],
    TransportCoefficientTransferRecord,
]


def evaluate_transport_coefficient_transfer(
    source: TransportCoefficient,
    context: TransportTransferContext,
    evaluator: TransportCoefficientTransferEvaluator,
) -> TransportCoefficientTransferRecord:
    """Evaluate one explicit transport-coefficient scale-transfer provider.

    The source coefficient and the complete transfer context are supplied to
    the provider explicitly. The provider must return a record bound to those
    same inputs.

    No normalization, unit conversion, averaging rule, constitutive relation,
    empirical coefficient, state-domain conversion, or uncertainty transfer
    is performed by this function.
    """

    if not isinstance(
        source,
        TransportCoefficient,
    ):
        raise TypeError(
            "source must be a TransportCoefficient instance."
        )

    if not isinstance(
        context,
        TransportTransferContext,
    ):
        raise TypeError(
            "context must be a TransportTransferContext instance."
        )

    if not callable(evaluator):
        raise TypeError(
            "evaluator must be callable."
        )

    result = evaluator(
        source,
        context,
    )

    if not isinstance(
        result,
        TransportCoefficientTransferRecord,
    ):
        raise TypeError(
            "evaluator must return a "
            "TransportCoefficientTransferRecord instance."
        )

    if result.source != source:
        raise ValueError(
            "transport-transfer result source must match input source."
        )

    if result.context != context:
        raise ValueError(
            "transport-transfer result context must match input context."
        )

    return result
