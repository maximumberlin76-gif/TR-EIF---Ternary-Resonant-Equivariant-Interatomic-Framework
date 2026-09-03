"""Qualification tests for TR-EIF finite-value numerical invariants."""

import math

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
    CoordinateDifferentiation,
)
from tr_eif.equivariant import NodeFeatures
from tr_eif.observables import TraceRecord
from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)


@pytest.mark.parametrize(
    "invalid_value",
    (
        math.nan,
        math.inf,
        -math.inf,
    ),
)
def test_atomic_positions_reject_nonfinite_values(
    invalid_value: float,
) -> None:
    """Atomic Cartesian positions must contain only finite values."""

    with pytest.raises(
        ValueError,
        match="positions\\[0\\] must contain only finite values",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (invalid_value, 0.0, 0.0),
            ),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        math.nan,
        math.inf,
        -math.inf,
    ),
)
def test_cell_vectors_reject_nonfinite_values(
    invalid_value: float,
) -> None:
    """Simulation-cell vectors must contain only finite values."""

    with pytest.raises(
        ValueError,
        match="cell\\[0\\] must contain only finite values",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (0.0, 0.0, 0.0),
            ),
            cell=(
                (invalid_value, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        math.nan,
        math.inf,
        -math.inf,
    ),
)
def test_scalar_features_reject_nonfinite_values(
    invalid_value: float,
) -> None:
    """Invariant scalar feature channels must remain finite."""

    with pytest.raises(
        ValueError,
        match="scalars must contain only finite values",
    ):
        NodeFeatures(
            scalars=(invalid_value,),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        math.nan,
        math.inf,
        -math.inf,
    ),
)
def test_vector_features_reject_nonfinite_values(
    invalid_value: float,
) -> None:
    """Equivariant vector feature channels must remain finite."""

    with pytest.raises(
        ValueError,
        match="vectors\\[0\\] must contain only finite values",
    ):
        NodeFeatures(
            vectors=(
                (0.0, invalid_value, 0.0),
            ),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        math.nan,
        math.inf,
        -math.inf,
    ),
)
def test_trace_time_rejects_nonfinite_values(
    invalid_value: float,
) -> None:
    """Observable trace time must remain finite."""

    execution = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEUTRAL,
        )
    )

    with pytest.raises(
        ValueError,
        match="time must be finite",
    ):
        TraceRecord(
            step=0,
            time=invalid_value,
            ternary_execution=execution,
        )


@pytest.mark.parametrize(
    "invalid_step",
    (
        0.0,
        -1.0e-6,
        -1.0,
    ),
)
def test_coordinate_differentiation_requires_positive_step(
    invalid_step: float,
) -> None:
    """Coordinate finite-difference step must be strictly positive."""

    with pytest.raises(
        ValueError,
        match="step must be positive",
    ):
        CoordinateDifferentiation(
            step=invalid_step,
        )


@pytest.mark.parametrize(
    "invalid_step",
    (
        0.0,
        -1.0e-6,
        -1.0,
    ),
)
def test_cell_strain_differentiation_requires_positive_step(
    invalid_step: float,
) -> None:
    """Cell-strain finite-difference step must be strictly positive."""

    with pytest.raises(
        ValueError,
        match="step must be positive",
    ):
        CellStrainDifferentiation(
            step=invalid_step,
        )


@pytest.mark.parametrize(
    "invalid_step",
    (
        math.nan,
        math.inf,
        -math.inf,
    ),
)
@pytest.mark.parametrize(
    "differentiation_type",
    (
        CoordinateDifferentiation,
        CellStrainDifferentiation,
    ),
)
def test_differentiation_rejects_nonfinite_step(
    differentiation_type,
    invalid_step: float,
) -> None:
    """Finite-difference policies must reject nonfinite step values."""

    with pytest.raises(
        ValueError,
        match="step must be finite",
    ):
        differentiation_type(
            step=invalid_step,
        )


@pytest.mark.parametrize(
    "invalid_step",
    (
        True,
        False,
        "1e-6",
        None,
    ),
)
@pytest.mark.parametrize(
    "differentiation_type",
    (
        CoordinateDifferentiation,
        CellStrainDifferentiation,
    ),
)
def test_differentiation_rejects_nonreal_step_types(
    differentiation_type,
    invalid_step,
) -> None:
    """Finite-difference policies must reject non-real step types."""

    with pytest.raises(
        TypeError,
        match="step must be a real number",
    ):
        differentiation_type(
            step=invalid_step,
        )
