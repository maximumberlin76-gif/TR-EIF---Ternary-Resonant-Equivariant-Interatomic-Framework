"""Ternary-target interpretation contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.resonance import ResonanceDescriptor, ResonanceState
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryState,
    TernaryTargetThresholds,
    ternary_target_from_descriptor,
    ternary_target_from_resonance_state,
)

from .units import ParameterProvenance


def _validate_source_metadata(
    source: str | None,
    provenance: ParameterProvenance,
) -> str | None:
    """Validate source metadata for one FLiBe ternary interpretation."""

    if source is not None and not isinstance(source, str):
        raise TypeError(
            "source must be a string or None."
        )

    if isinstance(source, str):
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
        provenance is ParameterProvenance.PRIMARY_SOURCE
        and source is None
    ):
        raise ValueError(
            "PRIMARY_SOURCE provenance requires source."
        )

    return source


@dataclass(frozen=True)
class FLiBeTernaryInterpretation:
    """Explicit resonance-to-ternary-target mapping with provenance."""

    projection: ResonanceProjection
    thresholds: TernaryTargetThresholds
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate interpretation parameters and provenance metadata."""

        if not isinstance(
            self.projection,
            ResonanceProjection,
        ):
            raise TypeError(
                "projection must be a ResonanceProjection."
            )

        if not isinstance(
            self.thresholds,
            TernaryTargetThresholds,
        ):
            raise TypeError(
                "thresholds must be a TernaryTargetThresholds."
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

    def target_from_descriptor(
        self,
        descriptor: ResonanceDescriptor,
    ) -> TernaryState:
        """Return a requested ternary target from one resonance descriptor."""

        if not isinstance(
            descriptor,
            ResonanceDescriptor,
        ):
            raise TypeError(
                "descriptor must be a ResonanceDescriptor."
            )

        return ternary_target_from_descriptor(
            descriptor,
            self.projection,
            self.thresholds,
        )

    def target_from_resonance_state(
        self,
        state: ResonanceState,
    ) -> TernaryState:
        """Return a requested ternary target from one resonance state."""

        if not isinstance(
            state,
            ResonanceState,
        ):
            raise TypeError(
                "state must be a ResonanceState."
            )

        return ternary_target_from_resonance_state(
            state,
            self.projection,
            self.thresholds,
        )


def interpret_flibe_ternary_target(
    interpretation: FLiBeTernaryInterpretation,
    descriptor: ResonanceDescriptor,
) -> TernaryState:
    """Evaluate one FLiBe ternary target from a resonance descriptor."""

    if not isinstance(
        interpretation,
        FLiBeTernaryInterpretation,
    ):
        raise TypeError(
            "interpretation must be an FLiBeTernaryInterpretation."
        )

    return interpretation.target_from_descriptor(
        descriptor
    )
