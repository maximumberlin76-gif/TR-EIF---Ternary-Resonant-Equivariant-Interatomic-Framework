"""Invariant tests for TR-EIF multiscale scalar reductions."""

import pytest

from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.reduction import (
    reduce_masses,
    reduce_scalar_sum,
)


def test_identity_partition_preserves_scalar_values() -> None:
    """Identity reduction must preserve each fine-scale scalar."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
        )
    )

    values = (
        -2.5,
        0.0,
        3.25,
        7.0,
    )

    coarse = reduce_scalar_sum(
        values=values,
        partition=partition,
    )

    assert coarse == values


def test_many_to_one_scalar_reduction_uses_partition_local_sums() -> None:
    """Fine-scale scalars must sum inside their assigned coarse entities."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            1,
            2,
        )
    )

    coarse = reduce_scalar_sum(
        values=(
            1.0,
            -1.0,
            2.0,
            3.0,
            -2.0,
            4.0,
        ),
        partition=partition,
    )

    assert coarse == (
        0.0,
        3.0,
        4.0,
    )


def test_interleaved_partition_reduces_by_assignment() -> None:
    """Reduction must follow explicit assignments rather than adjacency."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    coarse = reduce_scalar_sum(
        values=(
            1.0,
            10.0,
            2.0,
            20.0,
        ),
        partition=partition,
    )

    assert coarse == (
        3.0,
        30.0,
    )


def test_scalar_reduction_preserves_global_additive_total() -> None:
    """Partition-local sums must preserve the global scalar sum."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
            2,
        )
    )

    values = (
        -4.0,
        1.5,
        8.0,
        -2.0,
        0.5,
        3.0,
    )

    coarse = reduce_scalar_sum(
        values=values,
        partition=partition,
    )

    assert sum(coarse) == pytest.approx(
        sum(values)
    )


def test_scalar_reduction_allows_zero_values() -> None:
    """Zero is a valid value for a general additive scalar quantity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = reduce_scalar_sum(
        values=(
            0.0,
            0.0,
            0.0,
        ),
        partition=partition,
    )

    assert coarse == (
        0.0,
        0.0,
    )


def test_scalar_reduction_allows_signed_values() -> None:
    """General additive scalar reduction must not impose mass semantics."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    coarse = reduce_scalar_sum(
        values=(
            -3.0,
            1.0,
            -4.0,
            -2.0,
        ),
        partition=partition,
    )

    assert coarse == (
        -2.0,
        -6.0,
    )


def test_mass_reduction_preserves_identity_masses() -> None:
    """Identity partition must preserve each positive fine-scale mass."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    masses = (
        1.0,
        2.5,
        7.0,
    )

    coarse = reduce_masses(
        masses=masses,
        partition=partition,
    )

    assert coarse == masses


def test_mass_reduction_uses_partition_local_sums() -> None:
    """Coarse masses must equal sums of their fine-scale members."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            1,
            2,
        )
    )

    coarse = reduce_masses(
        masses=(
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
        ),
        partition=partition,
    )

    assert coarse == (
        3.0,
        12.0,
        6.0,
    )


def test_mass_reduction_preserves_total_mass() -> None:
    """Total coarse mass must equal total fine-scale mass."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            2,
            1,
            2,
        )
    )

    masses = (
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
    )

    coarse = reduce_masses(
        masses=masses,
        partition=partition,
    )

    assert sum(coarse) == pytest.approx(
        sum(masses)
    )


def test_every_coarse_mass_is_positive() -> None:
    """A valid positive fine-scale mass field yields positive coarse masses."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
        )
    )

    coarse = reduce_masses(
        masses=(
            0.5,
            1.5,
            2.0,
            3.0,
            4.0,
        ),
        partition=partition,
    )

    assert all(
        mass > 0.0
        for mass in coarse
    )


def test_scalar_reduction_requires_partition_instance() -> None:
    """Scalar reduction requires an explicit MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        reduce_scalar_sum(
            values=(
                1.0,
                2.0,
            ),
            partition=(0, 1),
        )


def test_scalar_reduction_requires_tuple_values() -> None:
    """The canonical fine-scale scalar container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match="values must be a tuple",
    ):
        reduce_scalar_sum(
            values=[1.0, 2.0],
            partition=partition,
        )


def test_scalar_reduction_rejects_empty_values() -> None:
    """Scalar reduction requires a nonempty fine-scale value field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="values must not be empty",
    ):
        reduce_scalar_sum(
            values=(),
            partition=partition,
        )


def test_scalar_reduction_requires_matching_fine_count() -> None:
    """One scalar value is required for every fine-scale entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="one scalar per fine-scale entity",
    ):
        reduce_scalar_sum(
            values=(
                1.0,
                2.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        True,
        False,
        "1.0",
        None,
    ),
)
def test_scalar_reduction_rejects_nonreal_values(
    invalid_value,
) -> None:
    """General scalar values must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"values\[1\] must be a real number",
    ):
        reduce_scalar_sum(
            values=(
                1.0,
                invalid_value,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_scalar_reduction_rejects_nonfinite_values(
    invalid_value: float,
) -> None:
    """General scalar reduction must reject nonfinite inputs."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"values\[1\] must be finite",
    ):
        reduce_scalar_sum(
            values=(
                1.0,
                invalid_value,
            ),
            partition=partition,
        )


def test_mass_reduction_requires_tuple_masses() -> None:
    """The canonical fine-scale mass container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match="masses must be a tuple",
    ):
        reduce_masses(
            masses=[1.0, 2.0],
            partition=partition,
        )


def test_mass_reduction_rejects_empty_masses() -> None:
    """Mass reduction requires a nonempty fine-scale mass field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="masses must not be empty",
    ):
        reduce_masses(
            masses=(),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        True,
        False,
        "1.0",
        None,
    ),
)
def test_mass_reduction_rejects_nonreal_mass(
    invalid_mass,
) -> None:
    """Fine-scale masses must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"masses\[1\] must be a real number",
    ):
        reduce_masses(
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_mass_reduction_rejects_nonfinite_mass(
    invalid_mass: float,
) -> None:
    """Fine-scale masses must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"masses\[1\] must be finite",
    ):
        reduce_masses(
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        0.0,
        -1.0,
        -10.5,
    ),
)
def test_mass_reduction_rejects_nonpositive_mass(
    invalid_mass: float,
) -> None:
    """Every fine-scale mass must be strictly positive."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"masses\[1\] must be greater than zero",
    ):
        reduce_masses(
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )


def test_mass_reduction_requires_matching_fine_count() -> None:
    """Mass count must agree with the fine-scale partition cardinality."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="one scalar per fine-scale entity",
    ):
        reduce_masses(
            masses=(
                1.0,
                2.0,
            ),
            partition=partition,
        )


def test_integer_scalar_inputs_are_normalized_to_float() -> None:
    """Accepted integer scalar values must produce canonical float output."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = reduce_scalar_sum(
        values=(
            1,
            2,
            3,
        ),
        partition=partition,
    )

    assert coarse == (
        3.0,
        3.0,
    )

    assert all(
        isinstance(value, float)
        for value in coarse
    )


def test_integer_mass_inputs_are_normalized_to_float() -> None:
    """Accepted integer masses must produce canonical float output."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = reduce_masses(
        masses=(
            1,
            2,
            3,
        ),
        partition=partition,
    )

    assert coarse == (
        3.0,
        3.0,
    )

    assert all(
        isinstance(mass, float)
        for mass in coarse
    )
