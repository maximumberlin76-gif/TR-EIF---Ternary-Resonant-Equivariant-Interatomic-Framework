"""E(3) transformations for TR-EIF equivariant features."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.configuration import Vector3

from .features import NodeFeatures, NodeFeatureVector

Matrix3x3 = tuple[Vector3, Vector3, Vector3]

_ORTHOGONAL_TOLERANCE = 1.0e-12


def _validate_vector3(
    value: Vector3,
    *,
    field_name: str,
) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple.")

    if len(value) != 3:
        raise ValueError(
            f"{field_name} must contain exactly three components."
        )

    if not all(isfinite(component) for component in value):
        raise ValueError(
            f"{field_name} must contain only finite values."
        )


def _validate_matrix3x3(
    matrix: Matrix3x3,
    *,
    field_name: str,
) -> None:
    if not isinstance(matrix, tuple):
        raise TypeError(f"{field_name} must be a tuple.")

    if len(matrix) != 3:
        raise ValueError(
            f"{field_name} must contain exactly three rows."
        )

    for index, row in enumerate(matrix):
        _validate_vector3(
            row,
            field_name=f"{field_name}[{index}]",
        )


def _dot(left: Vector3, right: Vector3) -> float:
    return (
        left[0] * right[0]
        + left[1] * right[1]
        + left[2] * right[2]
    )


def _matrix_vector_product(
    matrix: Matrix3x3,
    vector: Vector3,
) -> Vector3:
    return (
        _dot(matrix[0], vector),
        _dot(matrix[1], vector),
        _dot(matrix[2], vector),
    )


def _validate_orthogonal_matrix(matrix: Matrix3x3) -> None:
    _validate_matrix3x3(
        matrix,
        field_name="matrix",
    )

    for left_index in range(3):
        for right_index in range(3):
            column_left = (
                matrix[0][left_index],
                matrix[1][left_index],
                matrix[2][left_index],
            )
            column_right = (
                matrix[0][right_index],
                matrix[1][right_index],
                matrix[2][right_index],
            )

            expected = 1.0 if left_index == right_index else 0.0
            actual = _dot(column_left, column_right)

            if abs(actual - expected) > _ORTHOGONAL_TOLERANCE:
                raise ValueError(
                    "matrix must be orthogonal."
                )


@dataclass(frozen=True, slots=True)
class E3Transformation:
    """Orthogonal spatial transformation with Cartesian translation."""

    matrix: Matrix3x3
    translation: Vector3 = (0.0, 0.0, 0.0)

    def __post_init__(self) -> None:
        _validate_orthogonal_matrix(self.matrix)
        _validate_vector3(
            self.translation,
            field_name="translation",
        )

    def transform_position(self, position: Vector3) -> Vector3:
        """Transform one Cartesian position."""

        _validate_vector3(
            position,
            field_name="position",
        )

        rotated = _matrix_vector_product(
            self.matrix,
            position,
        )

        return (
            rotated[0] + self.translation[0],
            rotated[1] + self.translation[1],
            rotated[2] + self.translation[2],
        )

    def transform_vector(self, vector: Vector3) -> Vector3:
        """Transform one polar Cartesian vector."""

        _validate_vector3(
            vector,
            field_name="vector",
        )

        return _matrix_vector_product(
            self.matrix,
            vector,
        )

    def transform_node_features(
        self,
        features: NodeFeatures,
    ) -> NodeFeatures:
        """Transform invariant scalar and equivariant vector channels."""

        if not isinstance(features, NodeFeatures):
            raise TypeError(
                "features must be a NodeFeatures instance."
            )

        return NodeFeatures(
            scalars=features.scalars,
            vectors=tuple(
                self.transform_vector(vector)
                for vector in features.vectors
            ),
        )

    def transform_feature_vector(
        self,
        features: NodeFeatureVector,
    ) -> NodeFeatureVector:
        """Transform an ordered collection of node features."""

        if not isinstance(features, NodeFeatureVector):
            raise TypeError(
                "features must be a NodeFeatureVector instance."
            )

        return NodeFeatureVector(
            nodes=tuple(
                self.transform_node_features(node)
                for node in features.nodes
            )
        )
