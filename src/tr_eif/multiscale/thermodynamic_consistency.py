"""Explicit thermodynamic-consistency contract for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty thermodynamic-contract identifier."""

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
    """Validate one finite thermodynamic variable value."""

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
class ThermodynamicVariable:
    """One explicitly identified thermodynamic variable at one model scale.

    The value, unit, scale, state domain, and provenance are supplied by the
    caller. This record does not infer temperature, pressure, internal energy,
    free energy, enthalpy, entropy, or any other thermodynamic quantity.
    """

    variable_id: str
    value: float
    unit: str
    scale_id: str
    state_domain_id: str
    source_id: str

    def __post_init__(self) -> None:
        variable_id = _validate_identifier(
            self.variable_id,
            field_name="variable_id",
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
            "variable_id",
            variable_id,
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


ThermodynamicVariables: TypeAlias = tuple[
    ThermodynamicVariable,
    ...,
]


def _validate_variables(
    variables: ThermodynamicVariables,
    *,
    field_name: str,
) -> ThermodynamicVariables:
    """Validate one canonical collection of thermodynamic variables."""

    if not isinstance(variables, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if len(variables) == 0:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    keys: list[tuple[str, str]] = []

    for index, variable in enumerate(variables):
        if not isinstance(
            variable,
            ThermodynamicVariable,
        ):
            raise TypeError(
                f"{field_name}[{index}] must be a "
                "ThermodynamicVariable instance."
            )

        keys.append(
            (
                variable.scale_id,
                variable.variable_id,
            )
        )

    if len(set(keys)) != len(keys):
        raise ValueError(
            f"{field_name} must not contain duplicate "
            "scale_id/variable_id pairs."
        )

    if keys != sorted(keys):
        raise ValueError(
            f"{field_name} must use canonical scale/name ordering."
        )

    return variables


@dataclass(frozen=True, slots=True)
class ThermodynamicConsistencyContext:
    """Explicit model and assumptions for one consistency evaluation."""

    relation_id: str
    model_id: str
    assumptions_id: str
    normalization_id: str

    def __post_init__(self) -> None:
        relation_id = _validate_identifier(
            self.relation_id,
            field_name="relation_id",
        )
        model_id = _validate_identifier(
            self.model_id,
            field_name="model_id",
        )
        assumptions_id = _validate_identifier(
            self.assumptions_id,
            field_name="assumptions_id",
        )
        normalization_id = _validate_identifier(
            self.normalization_id,
            field_name="normalization_id",
        )

        object.__setattr__(
            self,
            "relation_id",
            relation_id,
        )
        object.__setattr__(
            self,
            "model_id",
            model_id,
        )
        object.__setattr__(
            self,
            "assumptions_id",
            assumptions_id,
        )
        object.__setattr__(
            self,
            "normalization_id",
            normalization_id,
        )


@dataclass(frozen=True, slots=True)
class ThermodynamicConsistencyRecord:
    """Result of one explicit thermodynamic-consistency evaluation.

    ``is_consistent`` is a validation status produced by the selected external
    evaluator. It is not a balanced-ternary state and does not encode -1/0/1.

    No equation of state, ensemble relation, free-energy model, tolerance,
    constitutive law, or cross-scale thermodynamic identity is supplied by
    this record.
    """

    source_variables: ThermodynamicVariables
    target_variables: ThermodynamicVariables
    context: ThermodynamicConsistencyContext
    is_consistent: bool
    validation_id: str

    def __post_init__(self) -> None:
        source_variables = _validate_variables(
            self.source_variables,
            field_name="source_variables",
        )
        target_variables = _validate_variables(
            self.target_variables,
            field_name="target_variables",
        )

        if not isinstance(
            self.context,
            ThermodynamicConsistencyContext,
        ):
            raise TypeError(
                "context must be a ThermodynamicConsistencyContext instance."
            )

        if not isinstance(self.is_consistent, bool):
            raise TypeError(
                "is_consistent must be a Boolean validation status."
            )

        validation_id = _validate_identifier(
            self.validation_id,
            field_name="validation_id",
        )

        object.__setattr__(
            self,
            "source_variables",
            source_variables,
        )
        object.__setattr__(
            self,
            "target_variables",
            target_variables,
        )
        object.__setattr__(
            self,
            "validation_id",
            validation_id,
        )


ThermodynamicConsistencyEvaluator: TypeAlias = Callable[
    [
        ThermodynamicVariables,
        ThermodynamicVariables,
        ThermodynamicConsistencyContext,
    ],
    ThermodynamicConsistencyRecord,
]


def evaluate_thermodynamic_consistency(
    source_variables: ThermodynamicVariables,
    target_variables: ThermodynamicVariables,
    context: ThermodynamicConsistencyContext,
    evaluator: ThermodynamicConsistencyEvaluator,
) -> ThermodynamicConsistencyRecord:
    """Evaluate one explicit thermodynamic-consistency provider.

    Both variable collections and the complete relation/model context are
    supplied explicitly. The provider must return a record bound to those
    exact inputs.

    This function performs no unit conversion, thermodynamic-variable
    inference, ensemble selection, equation-of-state evaluation, tolerance
    selection, or empirical calibration.
    """

    validated_source = _validate_variables(
        source_variables,
        field_name="source_variables",
    )
    validated_target = _validate_variables(
        target_variables,
        field_name="target_variables",
    )

    if not isinstance(
        context,
        ThermodynamicConsistencyContext,
    ):
        raise TypeError(
            "context must be a ThermodynamicConsistencyContext instance."
        )

    if not callable(evaluator):
        raise TypeError(
            "evaluator must be callable."
        )

    result = evaluator(
        validated_source,
        validated_target,
        context,
    )

    if not isinstance(
        result,
        ThermodynamicConsistencyRecord,
    ):
        raise TypeError(
            "evaluator must return a "
            "ThermodynamicConsistencyRecord instance."
        )

    if result.source_variables != validated_source:
        raise ValueError(
            "thermodynamic-consistency result source variables must match input."
        )

    if result.target_variables != validated_target:
        raise ValueError(
            "thermodynamic-consistency result target variables must match input."
        )

    if result.context != context:
        raise ValueError(
            "thermodynamic-consistency result context must match input context."
        )

    return result
