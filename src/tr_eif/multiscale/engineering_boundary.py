"""Explicit engineering-scale boundary-condition contract for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias

from .continuum_closure import ContinuumClosureRecord


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty engineering-boundary identifier."""

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


def _validate_values(
    values: tuple[float, ...],
) -> tuple[float, ...]:
    """Validate one immutable finite boundary-value vector."""

    if not isinstance(values, tuple):
        raise TypeError(
            "values must be a tuple."
        )

    if len(values) == 0:
        raise ValueError(
            "values must not be empty."
        )

    normalized_values: list[float] = []

    for index, value in enumerate(values):
        if not isinstance(value, (int, float)) or isinstance(
            value,
            bool,
        ):
            raise TypeError(
                f"values[{index}] must be a real number."
            )

        normalized = float(value)

        if not isfinite(normalized):
            raise ValueError(
                f"values[{index}] must be finite."
            )

        normalized_values.append(normalized)

    return tuple(normalized_values)


@dataclass(frozen=True, slots=True)
class EngineeringBoundaryCondition:
    """One explicit boundary condition for an engineering-scale model.

    ``condition_id`` identifies the caller-selected mathematical boundary
    condition. The contract does not interpret the identifier as Dirichlet,
    Neumann, Robin, periodic, convective, radiative, mechanical, electrical,
    or any other physical boundary type unless the external provider defines
    that meaning.
    """

    boundary_id: str
    variable_id: str
    condition_id: str
    values: tuple[float, ...]
    unit: str
    source_id: str

    def __post_init__(self) -> None:
        boundary_id = _validate_identifier(
            self.boundary_id,
            field_name="boundary_id",
        )
        variable_id = _validate_identifier(
            self.variable_id,
            field_name="variable_id",
        )
        condition_id = _validate_identifier(
            self.condition_id,
            field_name="condition_id",
        )
        values = _validate_values(
            self.values
        )
        unit = _validate_identifier(
            self.unit,
            field_name="unit",
        )
        source_id = _validate_identifier(
            self.source_id,
            field_name="source_id",
        )

        object.__setattr__(
            self,
            "boundary_id",
            boundary_id,
        )
        object.__setattr__(
            self,
            "variable_id",
            variable_id,
        )
        object.__setattr__(
            self,
            "condition_id",
            condition_id,
        )
        object.__setattr__(
            self,
            "values",
            values,
        )
        object.__setattr__(
            self,
            "unit",
            unit,
        )
        object.__setattr__(
            self,
            "source_id",
            source_id,
        )


EngineeringBoundaryConditions: TypeAlias = tuple[
    EngineeringBoundaryCondition,
    ...,
]


def _condition_key(
    condition: EngineeringBoundaryCondition,
) -> tuple[str, str, str]:
    """Return the canonical identity key for one boundary condition."""

    return (
        condition.boundary_id,
        condition.variable_id,
        condition.condition_id,
    )


def _validate_conditions(
    conditions: EngineeringBoundaryConditions,
) -> EngineeringBoundaryConditions:
    """Validate one canonical nonempty boundary-condition collection."""

    if not isinstance(conditions, tuple):
        raise TypeError(
            "conditions must be a tuple."
        )

    if len(conditions) == 0:
        raise ValueError(
            "conditions must not be empty."
        )

    keys: list[tuple[str, str, str]] = []

    for index, condition in enumerate(conditions):
        if not isinstance(
            condition,
            EngineeringBoundaryCondition,
        ):
            raise TypeError(
                f"conditions[{index}] must be an "
                "EngineeringBoundaryCondition instance."
            )

        keys.append(
            _condition_key(condition)
        )

    if len(set(keys)) != len(keys):
        raise ValueError(
            "conditions must not contain duplicate boundary identities."
        )

    if keys != sorted(keys):
        raise ValueError(
            "conditions must use canonical boundary ordering."
        )

    return conditions


@dataclass(frozen=True, slots=True)
class EngineeringBoundaryContext:
    """Explicit model context for one continuum-to-engineering boundary map."""

    engineering_model_id: str
    geometry_id: str
    mapping_id: str
    assumptions_id: str

    def __post_init__(self) -> None:
        engineering_model_id = _validate_identifier(
            self.engineering_model_id,
            field_name="engineering_model_id",
        )
        geometry_id = _validate_identifier(
            self.geometry_id,
            field_name="geometry_id",
        )
        mapping_id = _validate_identifier(
            self.mapping_id,
            field_name="mapping_id",
        )
        assumptions_id = _validate_identifier(
            self.assumptions_id,
            field_name="assumptions_id",
        )

        object.__setattr__(
            self,
            "engineering_model_id",
            engineering_model_id,
        )
        object.__setattr__(
            self,
            "geometry_id",
            geometry_id,
        )
        object.__setattr__(
            self,
            "mapping_id",
            mapping_id,
        )
        object.__setattr__(
            self,
            "assumptions_id",
            assumptions_id,
        )


@dataclass(frozen=True, slots=True)
class EngineeringBoundaryRecord:
    """Engineering-scale boundary conditions mapped from continuum closure.

    The continuum closure, engineering model, geometry, mapping assumptions,
    units, boundary identities, and numerical boundary values remain explicit.

    This record does not infer geometry, boundary type, constitutive law,
    load case, source term, coupling coefficient, discretization, or unit
    conversion.
    """

    continuum: ContinuumClosureRecord
    conditions: EngineeringBoundaryConditions
    context: EngineeringBoundaryContext

    def __post_init__(self) -> None:
        if not isinstance(
            self.continuum,
            ContinuumClosureRecord,
        ):
            raise TypeError(
                "continuum must be a ContinuumClosureRecord instance."
            )

        conditions = _validate_conditions(
            self.conditions
        )

        if not isinstance(
            self.context,
            EngineeringBoundaryContext,
        ):
            raise TypeError(
                "context must be an EngineeringBoundaryContext instance."
            )

        object.__setattr__(
            self,
            "conditions",
            conditions,
        )

    @property
    def condition_count(self) -> int:
        """Return the number of explicit engineering boundary conditions."""

        return len(self.conditions)


EngineeringBoundaryEvaluator: TypeAlias = Callable[
    [ContinuumClosureRecord, EngineeringBoundaryContext],
    EngineeringBoundaryRecord,
]


def evaluate_engineering_boundaries(
    continuum: ContinuumClosureRecord,
    context: EngineeringBoundaryContext,
    evaluator: EngineeringBoundaryEvaluator,
) -> EngineeringBoundaryRecord:
    """Evaluate one explicit continuum-to-engineering boundary provider.

    The continuum closure and complete engineering-boundary context are
    supplied explicitly. The provider must return a record bound to those
    exact inputs.

    This function performs no boundary-type inference, geometry generation,
    constitutive closure, load construction, discretization, interpolation,
    unit conversion, or empirical calibration.
    """

    if not isinstance(
        continuum,
        ContinuumClosureRecord,
    ):
        raise TypeError(
            "continuum must be a ContinuumClosureRecord instance."
        )

    if not isinstance(
        context,
        EngineeringBoundaryContext,
    ):
        raise TypeError(
            "context must be an EngineeringBoundaryContext instance."
        )

    if not callable(evaluator):
        raise TypeError(
            "evaluator must be callable."
        )

    result = evaluator(
        continuum,
        context,
    )

    if not isinstance(
        result,
        EngineeringBoundaryRecord,
    ):
        raise TypeError(
            "evaluator must return an EngineeringBoundaryRecord instance."
        )

    if result.continuum != continuum:
        raise ValueError(
            "engineering-boundary result continuum must match input continuum."
        )

    if result.context != context:
        raise ValueError(
            "engineering-boundary result context must match input context."
        )

    return result
