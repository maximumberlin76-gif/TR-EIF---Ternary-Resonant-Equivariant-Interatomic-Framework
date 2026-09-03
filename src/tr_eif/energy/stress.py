"""Stress representation for conservative TR-EIF energy models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

StressTensor: TypeAlias = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]


def _validate_stress_tensor(
    tensor: StressTensor,
) -> StressTensor:
    if not isinstance(tensor, tuple):
        raise TypeError("tensor must be a tuple.")

    if len(tensor) != 3:
        raise ValueError(
            "tensor must contain exactly three rows."
        )

    validated_rows: list[tuple[float, float, float]] = []

    for row_index, row in enumerate(tensor):
        if not isinstance(row, tuple):
            raise TypeError(
                f"tensor[{row_index}] must be a tuple."
            )

        if len(row) != 3:
            raise ValueError(
                f"tensor[{row_index}] must contain "
                "exactly three components."
            )

        validated_components: list[float] = []

        for component_index, component in enumerate(row):
            if not isinstance(
                component,
                (int, float),
            ) or isinstance(component, bool):
                raise TypeError(
                    f"tensor[{row_index}]"
                    f"[{component_index}] must be a real number."
                )

            if not isfinite(component):
                raise ValueError(
                    f"tensor[{row_index}]"
                    f"[{component_index}] must be finite."
                )

            validated_components.append(float(component))

        validated_rows.append(
            (
                validated_components[0],
                validated_components[1],
                validated_components[2],
            )
        )

    return (
        validated_rows[0],
        validated_rows[1],
        validated_rows[2],
    )


@dataclass(frozen=True, slots=True)
class StressState:
    """Immutable Cartesian stress-tensor representation."""

    tensor: StressTensor

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "tensor",
            _validate_stress_tensor(self.tensor),
        )

    @property
    def trace(self) -> float:
        """Return the Cartesian tensor trace."""

        return (
            self.tensor[0][0]
            + self.tensor[1][1]
            + self.tensor[2][2]
        )

    @property
    def is_symmetric(self) -> bool:
        """Return whether the tensor is exactly symmetric."""

        return (
            self.tensor[0][1] == self.tensor[1][0]
            and self.tensor[0][2] == self.tensor[2][0]
            and self.tensor[1][2] == self.tensor[2][1]
        )
