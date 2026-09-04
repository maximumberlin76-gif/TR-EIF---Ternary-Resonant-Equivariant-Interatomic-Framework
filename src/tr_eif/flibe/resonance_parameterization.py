"""Resonance-parameterization contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeAlias

from tr_eif.resonance import PhaseDynamicsParameters

from .coordination import FLiBeCoordinationState
from .units import ParameterProvenance


ResonanceParameterEvaluator: TypeAlias = Callable[
    [FLiBeCoordinationState],
    PhaseDynamicsParameters,
]


def _validate_source_metadata(
    source: str | None,
    provenance: ParameterProvenance,
) -> str | None:
    """Validate source metadata for one FLiBe resonance parameterization."""

    if source is not None and not isinstance(
        source,
        str,
    ):
        raise TypeError(
            "source must be a string or None."
        )

    if isinstance(
        source,
        str,
    ):
        if source == "":
            raise ValueError(
                "source must not be empty."
            )

        if source != source.strip():
            raise ValueError(
                "source must not contain leading "
                "or trailing whitespace."
            )

    if (
        provenance
        is ParameterProvenance.PRIMARY_SOURCE
        and source is None
    ):
        raise ValueError(
            "PRIMARY_SOURCE provenance requires source."
        )

    return source


@dataclass(frozen=True)
class FLiBeResonanceParameterization:
    """Explicit coordination-to-phase-parameter mapping with provenance."""

    evaluator: ResonanceParameterEvaluator
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate evaluator and provenance metadata."""

        if not callable(
            self.evaluator
        ):
            raise TypeError(
                "evaluator must be callable."
            )

        if not isinstance(
            self.provenance,
            ParameterProvenance,
        ):
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

    def evaluate(
        self,
        coordination: FLiBeCoordinationState,
    ) -> PhaseDynamicsParameters:
        """Evaluate phase-dynamics parameters for one coordination state."""

        if not isinstance(
            coordination,
            FLiBeCoordinationState,
        ):
            raise TypeError(
                "coordination must be an FLiBeCoordinationState."
            )

        parameters = self.evaluator(
            coordination
        )

        if not isinstance(
            parameters,
            PhaseDynamicsParameters,
        ):
            raise TypeError(
                "evaluator must return PhaseDynamicsParameters."
            )

        parameters.validate_oscillator_count(
            coordination.atom_count
        )

        return parameters


@dataclass(frozen=True)
class ConstantFLiBeResonanceParameters:
    """Explicit fixed phase-parameter set for controlled use."""

    parameters: PhaseDynamicsParameters
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate fixed parameters and provenance metadata."""

        if not isinstance(
            self.parameters,
            PhaseDynamicsParameters,
        ):
            raise TypeError(
                "parameters must be PhaseDynamicsParameters."
            )

        if not isinstance(
            self.provenance,
            ParameterProvenance,
        ):
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

    def evaluate(
        self,
        coordination: FLiBeCoordinationState,
    ) -> PhaseDynamicsParameters:
        """Return fixed phase parameters for a compatible coordination state."""

        if not isinstance(
            coordination,
            FLiBeCoordinationState,
        ):
            raise TypeError(
                "coordination must be an FLiBeCoordinationState."
            )

        self.parameters.validate_oscillator_count(
            coordination.atom_count
        )

        return self.parameters


def evaluate_resonance_parameters(
    model: FLiBeResonanceParameterization
    | ConstantFLiBeResonanceParameters,
    coordination: FLiBeCoordinationState,
) -> PhaseDynamicsParameters:
    """Evaluate one supported FLiBe resonance-parameterization model."""

    if not isinstance(
        model,
        (
            FLiBeResonanceParameterization,
            ConstantFLiBeResonanceParameters,
        ),
    ):
        raise TypeError(
            "model must be an FLiBeResonanceParameterization "
            "or ConstantFLiBeResonanceParameters."
        )

    return model.evaluate(
        coordination
    )
