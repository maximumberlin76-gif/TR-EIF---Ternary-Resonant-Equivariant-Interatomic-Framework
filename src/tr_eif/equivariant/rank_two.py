"""Cartesian rank-two E(3)-equivariant feature channels for TR-EIF.

A polar Cartesian rank-two tensor transforms as T' = Q T Q^T under the
orthogonal part Q of an E(3) transformation; a translation leaves its
components unchanged. Scalar, vector and rank-two channels remain separately
typed. The tensor decomposition isolates isotropic, symmetric-traceless and
antisymmetric parts without assigning mechanical stress or ternary semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

from .features import NodeFeatureVector
from .transform import E3Transformation

Tensor3x3: TypeAlias = tuple[Vector3, Vector3, Vector3]


def _tensor_rows(rows: Tensor3x3) -> Tensor3x3:
    if not isinstance(rows, tuple):
        raise TypeError("tensor rows must be a tuple.")
    if len(rows) != 3:
        raise ValueError("rank-two Cartesian tensor must have three rows.")
    normalized = []
    for index, row in enumerate(rows):
        if not isinstance(row, tuple):
            raise TypeError(f"tensor row {index} must be a tuple.")
        if len(row) != 3:
            raise ValueError(f"tensor row {index} must have three components.")
        for component in row:
            if isinstance(component, bool) or not isinstance(component, (int, float)):
                raise TypeError("tensor components must be real non-Boolean numbers.")
            if not isfinite(component):
                raise ValueError("tensor components must be finite.")
        normalized.append(tuple(float(value) for value in row))
    return (normalized[0], normalized[1], normalized[2])


def _vector(value: Vector3, name: str) -> Vector3:
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple.")
    if len(value) != 3:
        raise ValueError(f"{name} must contain three components.")
    result = []
    for component in value:
        if isinstance(component, bool) or not isinstance(component, (int, float)):
            raise TypeError(f"{name} components must be real non-Boolean numbers.")
        if not isfinite(component):
            raise ValueError(f"{name} components must be finite.")
        result.append(float(component))
    return (result[0], result[1], result[2])


@dataclass(frozen=True, slots=True)
class RankTwoTensor:
    """Immutable polar Cartesian second-order tensor with explicit E(3) action."""

    rows: Tensor3x3

    def __post_init__(self) -> None:
        object.__setattr__(self, "rows", _tensor_rows(self.rows))

    @classmethod
    def outer(cls, left: Vector3, right: Vector3) -> RankTwoTensor:
        """Construct the tensor product of two polar Cartesian vectors."""
        a = _vector(left, "left")
        b = _vector(right, "right")
        return cls(tuple(tuple(a[i] * b[j] for j in range(3)) for i in range(3)))

    @property
    def trace(self) -> float:
        """Return the rotation- and reflection-invariant tensor trace."""
        return fsum(self.rows[i][i] for i in range(3))

    @property
    def frobenius_norm_squared(self) -> float:
        """Return the invariant double contraction of the tensor with itself."""
        return fsum(x * x for row in self.rows for x in row)

    def double_contract(self, other: RankTwoTensor) -> float:
        """Contract two equally transforming rank-two tensors to a scalar."""
        if not isinstance(other, RankTwoTensor):
            raise TypeError("other must be RankTwoTensor.")
        return fsum(self.rows[i][j] * other.rows[i][j]
                    for i in range(3) for j in range(3))

    def transformed(self, transformation: E3Transformation) -> RankTwoTensor:
        """Apply Q T Q^T, with no contribution from Cartesian translation."""
        if not isinstance(transformation, E3Transformation):
            raise TypeError("transformation must be E3Transformation.")
        q = transformation.matrix
        t = self.rows
        return RankTwoTensor(tuple(
            tuple(fsum(q[i][a] * t[a][b] * q[j][b]
                       for a in range(3) for b in range(3))
                  for j in range(3))
            for i in range(3)
        ))

    def cartesian_decomposition(
        self,
    ) -> tuple[RankTwoTensor, RankTwoTensor, RankTwoTensor]:
        """Return isotropic, symmetric-traceless, and antisymmetric parts."""
        t = self.rows
        trace_third = self.trace / 3.0
        isotropic = RankTwoTensor(tuple(tuple(
            trace_third if i == j else 0.0 for j in range(3)
        ) for i in range(3)))
        traceless = RankTwoTensor(tuple(tuple(
            (t[i][j] + t[j][i]) / 2.0 - (trace_third if i == j else 0.0)
            for j in range(3)
        ) for i in range(3)))
        antisymmetric = RankTwoTensor(tuple(tuple(
            (t[i][j] - t[j][i]) / 2.0 for j in range(3)
        ) for i in range(3)))
        return isotropic, traceless, antisymmetric


@dataclass(frozen=True, slots=True)
class RankTwoFeatureVector:
    """One or more rank-two Cartesian feature channels per ordered node."""

    nodes: tuple[tuple[RankTwoTensor, ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.nodes, tuple):
            raise TypeError("nodes must be a tuple.")
        if not self.nodes:
            raise ValueError("rank-two feature nodes must not be empty.")
        count = None
        for index, channels in enumerate(self.nodes):
            if not isinstance(channels, tuple):
                raise TypeError(f"node {index} rank-two channels must be a tuple.")
            if not channels:
                raise ValueError("each node must retain a rank-two channel.")
            if any(not isinstance(t, RankTwoTensor) for t in channels):
                raise TypeError("rank-two feature channels must be RankTwoTensor.")
            if count is None:
                count = len(channels)
            elif len(channels) != count:
                raise ValueError("rank-two channel counts must match across nodes.")

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def tensor_channel_count(self) -> int:
        return len(self.nodes[0])

    def transformed(self, transformation: E3Transformation) -> RankTwoFeatureVector:
        """Transform rank-two channels without reordering nodes or channels."""
        if not isinstance(transformation, E3Transformation):
            raise TypeError("transformation must be E3Transformation.")
        return RankTwoFeatureVector(tuple(
            tuple(t.transformed(transformation) for t in channels)
            for channels in self.nodes
        ))


@dataclass(frozen=True, slots=True)
class ScalarVectorTensorFeatures:
    """Aligned scalar/vector and rank-two channels on one atom graph."""

    base: NodeFeatureVector
    rank_two: RankTwoFeatureVector

    def __post_init__(self) -> None:
        if not isinstance(self.base, NodeFeatureVector):
            raise TypeError("base must be NodeFeatureVector.")
        if not isinstance(self.rank_two, RankTwoFeatureVector):
            raise TypeError("rank_two must be RankTwoFeatureVector.")
        if self.base.node_count != self.rank_two.node_count:
            raise ValueError("scalar/vector and rank-two node counts must match.")

    @property
    def node_count(self) -> int:
        return self.base.node_count

    def transformed(self, transformation: E3Transformation) -> ScalarVectorTensorFeatures:
        """Apply the same E(3) action to all three representation classes."""
        if not isinstance(transformation, E3Transformation):
            raise TypeError("transformation must be E3Transformation.")
        return ScalarVectorTensorFeatures(
            base=transformation.transform_feature_vector(self.base),
            rank_two=self.rank_two.transformed(transformation),
        )
