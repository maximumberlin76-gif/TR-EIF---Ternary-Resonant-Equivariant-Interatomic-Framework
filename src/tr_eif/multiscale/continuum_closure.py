"""Explicit continuum closure contract for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias

from .mesoscale_closure import MesoscaleClosureRecord


@dataclass(frozen=True, slots=True)
class ContinuumClosureVariable:
    """One named finite numeric variable in a continuum closure state."""

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


ContinuumClosureVariables: TypeAlias = tuple[
    ContinuumClosureVariable,
    ...,
]


def _validate_variables(
    variables: ContinuumClosureVariables,
    *,
    field_name: str,
    require_nonempty: bool,
) -> ContinuumClosureVariables:
    """Validate one deterministic continuum-variable collection."""

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
            ContinuumClosureVariable,
        ):
            raise TypeError(
                f"{field_name}[{index}] must be a "
                "ContinuumClosureVariable instance."
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
    """Validate one nonempty continuum-closure identifier."""

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
class ContinuumClosureRecord:
    """Continuum closure bound to one explicit mesoscale closure state.

    ``continuum_variables`` are the explicit closure outputs.
    ``auxiliary_variables`` are caller-supplied result-affecting inputs that
    are not identified with the mesoscale closure itself.

    This record does not infer constitutive laws, material coefficients,
    boundary conditions, discretization topology, transport coefficients,
    uncertainty values, or empirical parameters.
    """

    mesoscale: MesoscaleClosureRecord
    closure_id: str
    source_id: str
    continuum_variables: ContinuumClosureVariables
    auxiliary_variables: ContinuumClosureVariables = ()

    def __post_init__(self) -> None:
        if not isinstance(
            self.mesoscale,
            MesoscaleClosureRecord,
        ):
            raise TypeError(
                "mesoscale must be a MesoscaleClosureRecord instance."
            )

        closure_id = _validate_identifier(
            self.closure_id,
            field_name="closure_id",
        )
        source_id = _validate_identifier(
            self.source_id,
            field_name="source_id",
        )
        continuum_variables = _validate_variables(
            self.continuum_variables,
            field_name="continuum_variables",
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
            "continuum_variables",
            continuum_variables,
        )
        object.__setattr__(
            self,
            "auxiliary_variables",
            auxiliary_variables,
        )

    @property
    def variable_count(self) -> int:
        """Return the number of explicit continuum closure variables."""

        return len(self.continuum_variables)

    def variable(
        self,
        name: str,
    ) -> ContinuumClosureVariable:
        """Return one continuum closure variable by normalized exact name."""

        normalized_name = _validate_identifier(
            name,
            field_name="name",
        )

        for variable in self.continuum_variables:
            if variable.name == normalized_name:
                return variable

        raise KeyError(
            f"continuum variable {normalized_name!r} is not present."
        )


ContinuumClosureEvaluator: TypeAlias = Callable[
    [MesoscaleClosureRecord, ContinuumClosureVariables],
    ContinuumClosureRecord,
]


def evaluate_continuum_closure(
    mesoscale: MesoscaleClosureRecord,
    evaluator: ContinuumClosureEvaluator,
    auxiliary_variables: ContinuumClosureVariables = (),
) -> ContinuumClosureRecord:
    """Evaluate one explicit mesoscale-to-continuum closure provider.

    The complete mesoscale closure input and all additional result-affecting
    variables are supplied explicitly. The provider must return a continuum
    record bound to those same inputs.

    No constitutive law, continuum discretization, boundary condition,
    transport relation, empirical coefficient, or uncertainty model is
    supplied by this function.
    """

    if not isinstance(
        mesoscale,
        MesoscaleClosureRecord,
    ):
        raise TypeError(
            "mesoscale must be a MesoscaleClosureRecord instance."
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
        mesoscale,
        validated_auxiliary,
    )

    if not isinstance(
        result,
        ContinuumClosureRecord,
    ):
        raise TypeError(
            "evaluator must return a ContinuumClosureRecord instance."
        )

    if result.mesoscale != mesoscale:
        raise ValueError(
            "continuum-closure result mesoscale input must match input."
        )

    if result.auxiliary_variables != validated_auxiliary:
        raise ValueError(
            "continuum-closure result auxiliary variables must match input."
        )

    return result
