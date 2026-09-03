"""Typed observable trace records for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.energy import EnergyState, ForceState, StressState
from tr_eif.ternary import TernaryExecutionVector


@dataclass(frozen=True, slots=True)
class TraceRecord:
    """Immutable observable record for one TR-EIF execution step."""

    step: int
    time: float
    ternary_execution: TernaryExecutionVector
    energy: EnergyState | None = None
    forces: ForceState | None = None
    stress: StressState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.step, int) or isinstance(self.step, bool):
            raise TypeError("step must be an integer.")

        if self.step < 0:
            raise ValueError("step must be nonnegative.")

        if not isinstance(self.time, (int, float)) or isinstance(
            self.time,
            bool,
        ):
            raise TypeError("time must be a real number.")

        if not isfinite(self.time):
            raise ValueError("time must be finite.")

        if self.time < 0.0:
            raise ValueError("time must be nonnegative.")

        if not isinstance(
            self.ternary_execution,
            TernaryExecutionVector,
        ):
            raise TypeError(
                "ternary_execution must be a "
                "TernaryExecutionVector instance."
            )

        if self.energy is not None:
            if not isinstance(self.energy, EnergyState):
                raise TypeError(
                    "energy must be an EnergyState instance or None."
                )

            if self.energy.atom_count != self.node_count:
                raise ValueError(
                    "energy atom count must match trace node count."
                )

        if self.forces is not None:
            if not isinstance(self.forces, ForceState):
                raise TypeError(
                    "forces must be a ForceState instance or None."
                )

            if self.forces.atom_count != self.node_count:
                raise ValueError(
                    "force atom count must match trace node count."
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
            "time",
            float(self.time),
        )

    @property
    def node_count(self) -> int:
        """Return the number of ternary execution nodes."""

        return self.ternary_execution.node_count

    @property
    def retained_states(self) -> tuple[int, ...]:
        """Return retained balanced-ternary states as integer values."""

        return tuple(
            int(state)
            for state in self.ternary_execution.retained_states
        )

    @property
    def has_pending_targets(self) -> bool:
        """Return whether any neutral-mediated route remains pending."""

        return self.ternary_execution.has_pending_targets
