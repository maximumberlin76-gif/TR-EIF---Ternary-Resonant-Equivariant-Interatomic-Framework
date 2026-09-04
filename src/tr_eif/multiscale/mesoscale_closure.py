"""Explicit mesoscale closure contract for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias

from .state import CoarseScaleState


@dataclass(frozen=True, slots=True)
class MesoscaleClosureVariable:
    """One named finite numeric variable in a mesoscale closure state."""

    name: str
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError(
                "name must be a string."
            )

        normalized_name = self.name.strip()

        if not normalized_name:
            raise ValueError(
                "name must not be empty or whitespace."
            )

        if not isinstance(self.values, tuple):
            raise TypeError(
                "values must be a tuple."
            )

        if len(self.values) == 0:
            raise ValueError(
                "values must not be empty."
            )

        normalized_values: list[float] = []

        for index, value in enumerate(self.values):
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

        object.__setattr__(
            self,
            "name",
            normalized_name,
        )
        object.__setattr__(
            self,
            "values",
            tuple(normalized_values),
        )


MesoscaleClosureVariables: TypeAlias = tuple[
    MesoscaleClosureVariable,
    ...,
]


def _validate_variables(
    variables: MesoscaleClosureVariables,
    *,
    field_name: str,
    require_nonempty: bool,
) -> MesoscaleClosureVariables:
    """Validate deterministic ordering of one closure-variable collection."""

    if not isinstance(variables, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if require_nonempty and len(variables) == 0:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    names: list[str] = []

    for index, variable in enumerate(variables):
        if not isinstance(
            variable,
            MesoscaleClosureVariable,
        ):
            raise TypeError(
                f"{field_name}[{index}] must be a "
                "MesoscaleClosureVariable instance."
            )

        names.append(variable.name)

    if len(set(names)) != len(names):
        raise ValueError(
            f"{field_name} must not contain duplicate variable names."
        )

    if names != sorted(names):
        raise ValueError(
            f"{field_name} must use canonical name ordering."
        )

    return variables


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty mesoscale-closure identifier."""

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


@dataclass(frozen=True, slots=True)
class MesoscaleClosureRecord:
    """Closure information supplementing one explicit coarse-scale state.

    ``auxiliary_variables`` are caller-supplied variables required by the
    closure evaluation but not identified with the reduced state itself.
    ``closure_variables`` are the explicit closure output.

    No constitutive coefficients, unresolved-scale model, history variable,
    uncertainty value, or empirical parameter is inferred by this record.
    """

    state: CoarseScaleState
    closure_id: str
    source_id: str
    closure_variables: MesoscaleClosureVariables
    auxiliary_variables: MesoscaleClosureVariables = ()

    def __post_init__(self) -> None:
        if not isinstance(
            self.state,
            CoarseScaleState,
        ):
            raise TypeError(
                "state must be a CoarseScaleState instance."
            )

        closure_id = _validate_identifier(
            self.closure_id,
            field_name="closure_id",
        )
        source_id = _validate_identifier(
            self.source_id,
            field_name="source_id",
        )
        closure_variables = _validate_variables(
            self.closure_variables,
            field_name="closure_variables",
            require_nonempty=True,
        )
        auxiliary_variables = _validate_variables(
            self.auxiliary_variables,
            field_name="auxiliary_variables",
            require_nonempty=False,
        )

        object.__setattr__(
            self,
            "closure_id",
            closure_id,
        )
        object.__setattr__(
            self,
            "source_id",
            source_id,
        )
        object.__setattr__(
            self,
            "closure_variables",
            closure_variables,
        )
        object.__setattr__(
            self,
            "auxiliary_variables",
            auxiliary_variables,
        )

    @property
    def variable_count(self) -> int:
        """Return the number of explicit closure-output variables."""

        return len(self.closure_variables)

    def variable(
        self,
        name: str,
    ) -> MesoscaleClosureVariable:
        """Return one closure variable by its exact normalized name."""

        normalized_name = _validate_identifier(
            name,
            field_name="name",
        )

        for variable in self.closure_variables:
            if variable.name == normalized_name:
                return variable

        raise KeyError(
            f"closure variable {normalized_name!r} is not present."
        )


MesoscaleClosureEvaluator: TypeAlias = Callable[
    [CoarseScaleState, MesoscaleClosureVariables],
    MesoscaleClosureRecord,
]


def evaluate_mesoscale_closure(
    state: CoarseScaleState,
    evaluator: MesoscaleClosureEvaluator,
    auxiliary_variables: MesoscaleClosureVariables = (),
) -> MesoscaleClosureRecord:
    """Evaluate one explicit mesoscale closure provider.

    The coarse state and all auxiliary result-affecting variables are supplied
    explicitly. The provider must return a record bound to the same state and
    the same auxiliary-variable collection. This function does not infer
    hidden state, constitutive parameters, history, or uncertainty.
    """

    if not isinstance(
        state,
        CoarseScaleState,
    ):
        raise TypeError(
            "state must be a CoarseScaleState instance."
        )

    if not callable(evaluator):
        raise TypeError(
            "evaluator must be callable."
        )

    validated_auxiliary = _validate_variables(
        auxiliary_variables,
        field_name="auxiliary_variables",
        require_nonempty=False,
    )

    result = evaluator(
        state,
        validated_auxiliary,
    )

    if not isinstance(
        result,
        MesoscaleClosureRecord,
    ):
        raise TypeError(
            "evaluator must return a MesoscaleClosureRecord instance."
        )

    if result.state != state:
        raise ValueError(
            "mesoscale-closure result state must match input state."
        )

    if result.auxiliary_variables != validated_auxiliary:
        raise ValueError(
            "mesoscale-closure result auxiliary variables must match input."
        )

    return result
