"""Training and validation configuration contracts for the TR-EIF FLiBe layer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

from .composition import FLiBeComposition
from .configuration import FLiBeConfiguration
from .thermodynamic_state import FLiBeThermodynamicState
from .units import ParameterProvenance


class FLiBeDatasetSplit(str, Enum):
    """Canonical immutable dataset split assignments."""

    TRAINING = "TRAINING"
    VALIDATION = "VALIDATION"
    TEST = "TEST"


FLiBeDatasetConfigurations: TypeAlias = tuple[
    "FLiBeDatasetConfiguration",
    ...,
]


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate one nonempty dataset identifier."""

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


def _validate_optional_identifier(
    value: str | None,
    *,
    field_name: str,
) -> str | None:
    """Validate one optional nonempty dataset identifier."""

    if value is None:
        return None

    return _validate_identifier(
        value,
        field_name=field_name,
    )


@dataclass(frozen=True, slots=True)
class FLiBeDatasetConfiguration:
    """One FLiBe configuration with explicit dataset role and provenance.

    The dataset split is metadata describing how the configuration is used by
    a learning or evaluation protocol. It does not modify atomic-state,
    thermodynamic-state, resonance, or balanced-ternary semantics.

    Missing, invalid, unknown, or abstained data are not encoded through the
    dataset split and are not encoded through ternary state 0.
    """

    sample_id: str
    configuration_id: str
    configuration: FLiBeConfiguration
    thermodynamic_state: FLiBeThermodynamicState
    split: FLiBeDatasetSplit
    provenance: ParameterProvenance
    source_id: str | None = None
    group_id: str | None = None
    trajectory_id: str | None = None
    parent_sample_id: str | None = None

    def __post_init__(self) -> None:
        sample_id = _validate_identifier(
            self.sample_id,
            field_name="sample_id",
        )
        configuration_id = _validate_identifier(
            self.configuration_id,
            field_name="configuration_id",
        )

        if not isinstance(
            self.configuration,
            FLiBeConfiguration,
        ):
            raise TypeError(
                "configuration must be an FLiBeConfiguration instance."
            )

        if not isinstance(
            self.thermodynamic_state,
            FLiBeThermodynamicState,
        ):
            raise TypeError(
                "thermodynamic_state must be an "
                "FLiBeThermodynamicState instance."
            )

        if not isinstance(
            self.split,
            FLiBeDatasetSplit,
        ):
            raise TypeError(
                "split must be an FLiBeDatasetSplit."
            )

        if not isinstance(
            self.provenance,
            ParameterProvenance,
        ):
            raise TypeError(
                "provenance must be a ParameterProvenance."
            )

        source_id = _validate_optional_identifier(
            self.source_id,
            field_name="source_id",
        )
        group_id = _validate_optional_identifier(
            self.group_id,
            field_name="group_id",
        )
        trajectory_id = _validate_optional_identifier(
            self.trajectory_id,
            field_name="trajectory_id",
        )
        parent_sample_id = _validate_optional_identifier(
            self.parent_sample_id,
            field_name="parent_sample_id",
        )

        if (
            self.provenance
            is ParameterProvenance.PRIMARY_SOURCE
            and source_id is None
        ):
            raise ValueError(
                "PRIMARY_SOURCE provenance requires source_id."
            )

        if parent_sample_id == sample_id:
            raise ValueError(
                "parent_sample_id must not equal sample_id."
            )

        object.__setattr__(
            self,
            "sample_id",
            sample_id,
        )
        object.__setattr__(
            self,
            "configuration_id",
            configuration_id,
        )
        object.__setattr__(
            self,
            "source_id",
            source_id,
        )
        object.__setattr__(
            self,
            "group_id",
            group_id,
        )
        object.__setattr__(
            self,
            "trajectory_id",
            trajectory_id,
        )
        object.__setattr__(
            self,
            "parent_sample_id",
            parent_sample_id,
        )

    @property
    def composition(self) -> FLiBeComposition:
        """Return the exact LiF-BeF2 composition of this configuration."""

        return self.configuration.composition()

    @property
    def is_training(self) -> bool:
        """Return whether this sample belongs to the training split."""

        return self.split is FLiBeDatasetSplit.TRAINING

    @property
    def is_validation(self) -> bool:
        """Return whether this sample belongs to the validation split."""

        return self.split is FLiBeDatasetSplit.VALIDATION

    @property
    def is_test(self) -> bool:
        """Return whether this sample belongs to the final test split."""

        return self.split is FLiBeDatasetSplit.TEST


def validate_flibe_split_isolation(
    samples: FLiBeDatasetConfigurations,
) -> FLiBeDatasetConfigurations:
    """Validate strict configuration-level split isolation.

    The validator requires unique sample identifiers and prevents one exact
    configuration identity, configuration value, group, trajectory, or known
    parent/derived lineage from crossing training, validation, and test
    boundaries.

    This is a strict split-validation operator. It does not generate a split,
    choose random seeds, infer structural similarity, or classify near
    duplicates.
    """

    if not isinstance(samples, tuple):
        raise TypeError(
            "samples must be a tuple."
        )

    if len(samples) == 0:
        raise ValueError(
            "samples must not be empty."
        )

    for index, sample in enumerate(samples):
        if not isinstance(
            sample,
            FLiBeDatasetConfiguration,
        ):
            raise TypeError(
                f"samples[{index}] must be an "
                "FLiBeDatasetConfiguration instance."
            )

    sample_ids = tuple(
        sample.sample_id
        for sample in samples
    )

    if len(set(sample_ids)) != len(sample_ids):
        raise ValueError(
            "sample_id values must be unique."
        )

    split_by_configuration_id: dict[
        str,
        FLiBeDatasetSplit,
    ] = {}
    split_by_configuration_value: dict[
        FLiBeConfiguration,
        FLiBeDatasetSplit,
    ] = {}
    split_by_group: dict[
        str,
        FLiBeDatasetSplit,
    ] = {}
    split_by_trajectory: dict[
        str,
        FLiBeDatasetSplit,
    ] = {}

    sample_by_id = {
        sample.sample_id: sample
        for sample in samples
    }

    for sample in samples:
        previous_split = split_by_configuration_id.get(
            sample.configuration_id
        )

        if (
            previous_split is not None
            and previous_split is not sample.split
        ):
            raise ValueError(
                "configuration_id must not cross dataset splits."
            )

        split_by_configuration_id[
            sample.configuration_id
        ] = sample.split

        previous_split = split_by_configuration_value.get(
            sample.configuration
        )

        if (
            previous_split is not None
            and previous_split is not sample.split
        ):
            raise ValueError(
                "exact FLiBe configuration must not cross dataset splits."
            )

        split_by_configuration_value[
            sample.configuration
        ] = sample.split

        if sample.group_id is not None:
            previous_split = split_by_group.get(
                sample.group_id
            )

            if (
                previous_split is not None
                and previous_split is not sample.split
            ):
                raise ValueError(
                    "group_id must not cross dataset splits."
                )

            split_by_group[
                sample.group_id
            ] = sample.split

        if sample.trajectory_id is not None:
            previous_split = split_by_trajectory.get(
                sample.trajectory_id
            )

            if (
                previous_split is not None
                and previous_split is not sample.split
            ):
                raise ValueError(
                    "trajectory_id must not cross dataset splits."
                )

            split_by_trajectory[
                sample.trajectory_id
            ] = sample.split

    for sample in samples:
        if sample.parent_sample_id is None:
            continue

        parent = sample_by_id.get(
            sample.parent_sample_id
        )

        if parent is None:
            continue

        if parent.split is not sample.split:
            raise ValueError(
                "parent and derived sample must not cross dataset splits."
            )

    return samples
