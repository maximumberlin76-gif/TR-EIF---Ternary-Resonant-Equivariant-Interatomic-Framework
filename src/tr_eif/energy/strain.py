"""Cell-strain differentiation policy for TR-EIF energy models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class CellStrainDifferentiation:
    """Finite-difference policy for homogeneous cell-strain derivatives."""

    step: float = 1.0e-6

    def __post_init__(self) -> None:
        if not isinstance(self.step, (int, float)) or isinstance(
            self.step,
            bool,
        ):
            raise TypeError("step must be a real number.")

        if not isfinite(self.step):
            raise ValueError("step must be finite.")

        if self.step <= 0.0:
            raise ValueError("step must be positive.")

        object.__setattr__(
            self,
            "step",
            float(self.step),
        )

    @property
    def inverse_central_span(self) -> float:
        """Return the reciprocal of the central-difference strain span."""

        return 1.0 / (2.0 * self.step)
