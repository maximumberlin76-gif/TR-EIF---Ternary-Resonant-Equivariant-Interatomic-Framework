"""Partition-aware scalar reductions for TR-EIF multiscale models."""

from __future__ import annotations

from math import isfinite
from typing import TypeAlias

from .partition import MultiscalePartition


FineScalars: TypeAlias = tuple[float, ...]
CoarseScalars: TypeAlias = tuple[float, ...]
FineMasses: TypeAlias = tuple[float, ...]
CoarseMasses: TypeAlias = tuple[float, ...]


def _validate_finite_scalars(
    values: FineScalars,
    *,
    field_name: str,
) -> tuple[float, ...]:
    """Validate and normalize a fine-scale scalar sequence."""

    if not isinstance(values, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if len(values) == 0:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    normalized: list[float] = []

    for index, value in enumerate(values):
        if not isinstance(value, (int, float)) or isinstance(
            value,
            bool,
        ):
            raise TypeError(
                f"{field_name}[{index}] must be a real number."
            )

        scalar = float(value)

        if not isfinite(scalar):
            raise ValueError(
                f"{field_name}[{index}] must be finite."
            )

        normalized.append(scalar)

    return tuple(normalized)


def reduce_scalar_sum(
    values: FineScalars,
    partition: MultiscalePartition,
) -> CoarseScalars:
    """Reduce fine-scale scalar values by partition-local summation."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    normalized = _validate_finite_scalars(
        values,
        field_name="values",
    )

    if len(normalized) != partition.fine_count:
        raise ValueError(
            "values must contain one scalar per fine-scale entity."
        )

    coarse = [0.0] * partition.coarse_count

    for fine_index, value in enumerate(normalized):
        coarse_index = partition.coarse_index_for(
            fine_index
        )
        coarse[coarse_index] += value

    return tuple(coarse)


def reduce_masses(
    masses: FineMasses,
    partition: MultiscalePartition,
) -> CoarseMasses:
    """Reduce finite positive fine-scale masses by partition-local summation."""

    normalized = _validate_finite_scalars(
        masses,
        field_name="masses",
    )

    for index, mass in enumerate(normalized):
        if mass <= 0.0:
            raise ValueError(
                f"masses[{index}] must be greater than zero."
            )

    coarse = reduce_scalar_sum(
        values=normalized,
        partition=partition,
    )

    for index, mass in enumerate(coarse):
        if not isfinite(mass):
            raise ValueError(
                f"coarse masses[{index}] must be finite."
            )

        if mass <= 0.0:
            raise ValueError(
                f"coarse masses[{index}] must be greater than zero."
            )

    return coarse
