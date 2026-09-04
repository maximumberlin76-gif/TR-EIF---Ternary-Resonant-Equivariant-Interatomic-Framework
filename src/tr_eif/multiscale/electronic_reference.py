"""Electronic-reference data contract for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState, StressState

ElectronicReferenceEvaluator: TypeAlias = Callable[
    [AtomicConfiguration],
    "ElectronicReferenceRecord",
]


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty external-reference identifier."""

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


def _validate_total_energy(value: float) -> float:
    """Validate one finite total-energy reference value."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            "total_energy must be a real number."
        )

    normalized = float(value)

    if not isfinite(normalized):
        raise ValueError(
            "total_energy must be finite."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class ElectronicReferenceRecord:
    """Immutable externally supplied electronic-reference observables.

    The record binds one atomic configuration to an externally supplied
    total energy and optional force and stress observables. It does not
    perform an electronic-structure calculation and does not infer missing
    observables.

    ``source_id`` and ``method_id`` are explicit provenance anchors supplied
    by the caller. Their interpretation remains outside this data contract.
    """

    configuration: AtomicConfiguration
    total_energy: float
    source_id: str
    method_id: str
    forces: ForceState | None = None
    stress: StressState | None = None

    def __post_init__(self) -> None:
        if not isinstance(
            self.configuration,
            AtomicConfiguration,
        ):
            raise TypeError(
                "configuration must be an AtomicConfiguration instance."
            )

        total_energy = _validate_total_energy(
            self.total_energy
        )
        source_id = _validate_identifier(
            self.source_id,
            field_name="source_id",
        )
        method_id = _validate_identifier(
            self.method_id,
            field_name="method_id",
        )

        if self.forces is not None:
            if not isinstance(self.forces, ForceState):
                raise TypeError(
                    "forces must be a ForceState instance or None."
                )

            if self.forces.atom_count != self.configuration.atom_count:
                raise ValueError(
                    "force atom count must match configuration atom count."
                )

        if self.stress is not None and not isinstance(
            self.stress,
            StressState,
        ):
            raise TypeError(
                "stress must be a StressState instance or None."
            )

        object.__setattr__(
            self,
            "total_energy",
            total_energy,
        )
        object.__setattr__(
            self,
            "source_id",
            source_id,
        )
        object.__setattr__(
            self,
            "method_id",
            method_id,
        )

    @property
    def atom_count(self) -> int:
        """Return the number of atoms represented by this reference record."""

        return self.configuration.atom_count

    @property
    def has_forces(self) -> bool:
        """Return whether atomic force references are present."""

        return self.forces is not None

    @property
    def has_stress(self) -> bool:
        """Return whether a stress reference is present."""

        return self.stress is not None


def evaluate_electronic_reference(
    configuration: AtomicConfiguration,
    evaluator: ElectronicReferenceEvaluator,
) -> ElectronicReferenceRecord:
    """Evaluate one explicit external electronic-reference provider.

    The provider must return an ``ElectronicReferenceRecord`` bound to the
    exact input configuration. This function adds no physical parameters,
    unit conversions, interpolation, or empirical corrections.
    """

    if not isinstance(
        configuration,
        AtomicConfiguration,
    ):
        raise TypeError(
            "configuration must be an AtomicConfiguration instance."
        )

    if not callable(evaluator):
        raise TypeError(
            "evaluator must be callable."
        )

    result = evaluator(configuration)

    if not isinstance(
        result,
        ElectronicReferenceRecord,
    ):
        raise TypeError(
            "evaluator must return an ElectronicReferenceRecord instance."
        )

    if result.configuration != configuration:
        raise ValueError(
            "electronic-reference result configuration must match input configuration."
        )

    return result
