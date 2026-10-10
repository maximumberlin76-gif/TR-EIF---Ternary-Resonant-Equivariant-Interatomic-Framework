"""Invariant tests for the TR-EIF FLiBe dataset configuration contract."""

from __future__ import annotations

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.dataset_configuration import (
    FLiBeDatasetConfiguration,
    FLiBeDatasetSplit,
    validate_flibe_split_isolation,
)
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.units import ParameterProvenance


def _configuration(
    *,
    offset: float = 0.0,
) -> FLiBeConfiguration:
    """Construct one exact 2 LiF : 1 BeF2 test-fixture configuration."""

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=(
                "Li",
                "Li",
                "Be",
                "F",
                "F",
                "F",
                "F",
            ),
            positions=tuple(
                (
                    float(index) + offset,
                    0.0,
                    0.0,
                )
                for index in range(7)
            ),
        )
    )


def _thermodynamic_state(
    *,
    temperature: float = 1000.0,
    pressure: float = 0.0,
) -> FLiBeThermodynamicState:
    """Construct one explicit test-fixture thermodynamic state."""

    return FLiBeThermodynamicState(
        temperature=temperature,
        pressure=pressure,
    )


def _sample(
    *,
    sample_id: str,
    configuration_id: str,
    split: FLiBeDatasetSplit,
    configuration: FLiBeConfiguration | None = None,
    thermodynamic_state: FLiBeThermodynamicState | None = None,
    provenance: ParameterProvenance = ParameterProvenance.TEST_FIXTURE,
    source_id: str | None = None,
    group_id: str | None = None,
    trajectory_id: str | None = None,
    parent_sample_id: str | None = None,
) -> FLiBeDatasetConfiguration:
    """Construct one explicit dataset sample."""

    return FLiBeDatasetConfiguration(
        sample_id=sample_id,
        configuration_id=configuration_id,
        configuration=(
            _configuration()
            if configuration is None
            else configuration
        ),
        thermodynamic_state=(
            _thermodynamic_state()
            if thermodynamic_state is None
            else thermodynamic_state
        ),
        split=split,
        provenance=provenance,
        source_id=source_id,
        group_id=group_id,
        trajectory_id=trajectory_id,
        parent_sample_id=parent_sample_id,
    )


def test_dataset_split_values_are_explicit_nonternary_labels() -> None:
    """Dataset roles must remain separate from balanced-ternary state values."""

    assert tuple(split.value for split in FLiBeDatasetSplit) == (
        "TRAINING",
        "VALIDATION",
        "TEST",
    )


def test_dataset_configuration_normalizes_identifiers() -> None:
    """Required and optional identifiers must normalize surrounding whitespace."""

    sample = _sample(
        sample_id=" sample-a ",
        configuration_id=" configuration-a ",
        split=FLiBeDatasetSplit.TRAINING,
        source_id=" source-a ",
        group_id=" group-a ",
        trajectory_id=" trajectory-a ",
        parent_sample_id=" parent-a ",
    )

    assert sample.sample_id == "sample-a"
    assert sample.configuration_id == "configuration-a"
    assert sample.source_id == "source-a"
    assert sample.group_id == "group-a"
    assert sample.trajectory_id == "trajectory-a"
    assert sample.parent_sample_id == "parent-a"


def test_dataset_configuration_exposes_exact_composition() -> None:
    """Dataset metadata must not alter the wrapped FLiBe composition."""

    sample = _sample(
        sample_id="sample-a",
        configuration_id="configuration-a",
        split=FLiBeDatasetSplit.TRAINING,
    )

    composition = sample.composition

    assert composition.lif_fraction == pytest.approx(2.0 / 3.0)
    assert composition.bef2_fraction == pytest.approx(1.0 / 3.0)


@pytest.mark.parametrize(
    ("split", "is_training", "is_validation", "is_test"),
    (
        (FLiBeDatasetSplit.TRAINING, True, False, False),
        (FLiBeDatasetSplit.VALIDATION, False, True, False),
        (FLiBeDatasetSplit.TEST, False, False, True),
    ),
)
def test_dataset_role_properties_are_mutually_exclusive(
    split: FLiBeDatasetSplit,
    is_training: bool,
    is_validation: bool,
    is_test: bool,
) -> None:
    """Each sample must expose exactly its declared dataset role."""

    sample = _sample(
        sample_id="sample-a",
        configuration_id="configuration-a",
        split=split,
    )

    assert sample.is_training is is_training
    assert sample.is_validation is is_validation
    assert sample.is_test is is_test


def test_primary_source_requires_source_id() -> None:
    """PRIMARY_SOURCE samples must retain an explicit source identifier."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source_id",
    ):
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_primary_source_accepts_explicit_source_id() -> None:
    """PRIMARY_SOURCE is valid when the provenance anchor is supplied."""

    sample = _sample(
        sample_id="sample-a",
        configuration_id="configuration-a",
        split=FLiBeDatasetSplit.TRAINING,
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source_id="FLIBE-PRIMARY-TEST",
    )

    assert sample.source_id == "FLIBE-PRIMARY-TEST"


def test_nonprimary_fixture_does_not_require_source_id() -> None:
    """Test fixtures may remain explicitly source-free test metadata."""

    sample = _sample(
        sample_id="sample-a",
        configuration_id="configuration-a",
        split=FLiBeDatasetSplit.TRAINING,
    )

    assert sample.provenance is ParameterProvenance.TEST_FIXTURE
    assert sample.source_id is None


def test_parent_sample_id_must_not_equal_sample_id() -> None:
    """A sample cannot declare itself as its own parent."""

    with pytest.raises(
        ValueError,
        match="parent_sample_id must not equal sample_id",
    ):
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            parent_sample_id=" sample-a ",
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "sample_id",
        "configuration_id",
    ),
)
def test_required_identifiers_must_be_strings(field_name: str) -> None:
    """Required dataset identifiers must use the string contract."""

    arguments: dict[str, object] = {
        "sample_id": "sample-a",
        "configuration_id": "configuration-a",
        "configuration": _configuration(),
        "thermodynamic_state": _thermodynamic_state(),
        "split": FLiBeDatasetSplit.TRAINING,
        "provenance": ParameterProvenance.TEST_FIXTURE,
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        FLiBeDatasetConfiguration(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "sample_id",
        "configuration_id",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        "",
        "   ",
        "\t\n",
    ),
)
def test_required_identifiers_must_not_be_empty(
    field_name: str,
    value: str,
) -> None:
    """Required dataset identifiers must remain nonempty after normalization."""

    arguments = {
        "sample_id": "sample-a",
        "configuration_id": "configuration-a",
        "configuration": _configuration(),
        "thermodynamic_state": _thermodynamic_state(),
        "split": FLiBeDatasetSplit.TRAINING,
        "provenance": ParameterProvenance.TEST_FIXTURE,
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        FLiBeDatasetConfiguration(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_id",
        "group_id",
        "trajectory_id",
        "parent_sample_id",
    ),
)
def test_optional_identifiers_reject_nonstring_values(
    field_name: str,
) -> None:
    """Optional identifiers must be strings when present."""

    arguments: dict[str, object] = {
        "sample_id": "sample-a",
        "configuration_id": "configuration-a",
        "configuration": _configuration(),
        "thermodynamic_state": _thermodynamic_state(),
        "split": FLiBeDatasetSplit.TRAINING,
        "provenance": ParameterProvenance.TEST_FIXTURE,
        field_name: 1,
    }

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        FLiBeDatasetConfiguration(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "source_id",
        "group_id",
        "trajectory_id",
        "parent_sample_id",
    ),
)
def test_optional_identifiers_reject_whitespace_values(
    field_name: str,
) -> None:
    """Present optional identifiers must not normalize to empty strings."""

    arguments: dict[str, object] = {
        "sample_id": "sample-a",
        "configuration_id": "configuration-a",
        "configuration": _configuration(),
        "thermodynamic_state": _thermodynamic_state(),
        "split": FLiBeDatasetSplit.TRAINING,
        "provenance": ParameterProvenance.TEST_FIXTURE,
        field_name: "   ",
    }

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        FLiBeDatasetConfiguration(**arguments)


def test_configuration_requires_flibe_configuration() -> None:
    """Dataset samples must use the typed FLiBe configuration boundary."""

    with pytest.raises(
        TypeError,
        match="configuration must be an FLiBeConfiguration instance",
    ):
        FLiBeDatasetConfiguration(
            sample_id="sample-a",
            configuration_id="configuration-a",
            configuration=None,  # type: ignore[arg-type]
            thermodynamic_state=_thermodynamic_state(),
            split=FLiBeDatasetSplit.TRAINING,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


def test_thermodynamic_state_requires_flibe_state() -> None:
    """Dataset samples must retain an explicit typed thermodynamic state."""

    with pytest.raises(
        TypeError,
        match=(
            "thermodynamic_state must be an "
            "FLiBeThermodynamicState instance"
        ),
    ):
        FLiBeDatasetConfiguration(
            sample_id="sample-a",
            configuration_id="configuration-a",
            configuration=_configuration(),
            thermodynamic_state=None,  # type: ignore[arg-type]
            split=FLiBeDatasetSplit.TRAINING,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "split",
    (
        -1,
        0,
        1,
        "TRAINING",
    ),
)
def test_dataset_split_does_not_accept_ternary_or_untyped_values(
    split: object,
) -> None:
    """Dataset roles must not be substituted by ternary or raw string values."""

    with pytest.raises(
        TypeError,
        match="split must be an FLiBeDatasetSplit",
    ):
        FLiBeDatasetConfiguration(
            sample_id="sample-a",
            configuration_id="configuration-a",
            configuration=_configuration(),
            thermodynamic_state=_thermodynamic_state(),
            split=split,  # type: ignore[arg-type]
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


def test_provenance_requires_parameter_provenance() -> None:
    """Dataset provenance must use the canonical provenance enum."""

    with pytest.raises(
        TypeError,
        match="provenance must be a ParameterProvenance",
    ):
        FLiBeDatasetConfiguration(
            sample_id="sample-a",
            configuration_id="configuration-a",
            configuration=_configuration(),
            thermodynamic_state=_thermodynamic_state(),
            split=FLiBeDatasetSplit.TRAINING,
            provenance="TEST_FIXTURE",  # type: ignore[arg-type]
        )


def test_split_isolation_requires_tuple() -> None:
    """Split validation must use an immutable sample collection."""

    with pytest.raises(
        TypeError,
        match="samples must be a tuple",
    ):
        validate_flibe_split_isolation([])  # type: ignore[arg-type]


def test_split_isolation_requires_nonempty_collection() -> None:
    """An empty collection is not a valid split-isolation input."""

    with pytest.raises(
        ValueError,
        match="samples must not be empty",
    ):
        validate_flibe_split_isolation(())


def test_split_isolation_rejects_untyped_sample() -> None:
    """Every split-isolation entry must be a dataset configuration."""

    with pytest.raises(
        TypeError,
        match=r"samples0 must be an FLiBeDatasetConfiguration instance",
    ):
        validate_flibe_split_isolation((None,))  # type: ignore[arg-type]


def test_sample_ids_must_be_unique() -> None:
    """One sample identity cannot occur more than once in a dataset manifest."""

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=0.0),
        ),
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-b",
            split=FLiBeDatasetSplit.VALIDATION,
            configuration=_configuration(offset=10.0),
        ),
    )

    with pytest.raises(
        ValueError,
        match="sample_id values must be unique",
    ):
        validate_flibe_split_isolation(samples)


def test_configuration_id_must_not_cross_splits() -> None:
    """One declared configuration identity cannot leak across dataset roles."""

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-shared",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=0.0),
        ),
        _sample(
            sample_id="sample-b",
            configuration_id="configuration-shared",
            split=FLiBeDatasetSplit.VALIDATION,
            configuration=_configuration(offset=10.0),
        ),
    )

    with pytest.raises(
        ValueError,
        match="configuration_id must not cross dataset splits",
    ):
        validate_flibe_split_isolation(samples)


def test_exact_configuration_value_must_not_cross_splits() -> None:
    """Exact geometry/species duplicates cannot cross split boundaries."""

    configuration = _configuration()

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=configuration,
        ),
        _sample(
            sample_id="sample-b",
            configuration_id="configuration-b",
            split=FLiBeDatasetSplit.TEST,
            configuration=configuration,
            thermodynamic_state=_thermodynamic_state(
                temperature=1200.0
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="exact FLiBe configuration must not cross dataset splits",
    ):
        validate_flibe_split_isolation(samples)


def test_group_id_must_not_cross_splits() -> None:
    """Explicitly grouped related samples must remain in one split."""

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=0.0),
            group_id="group-a",
        ),
        _sample(
            sample_id="sample-b",
            configuration_id="configuration-b",
            split=FLiBeDatasetSplit.VALIDATION,
            configuration=_configuration(offset=10.0),
            group_id="group-a",
        ),
    )

    with pytest.raises(
        ValueError,
        match="group_id must not cross dataset splits",
    ):
        validate_flibe_split_isolation(samples)


def test_trajectory_id_must_not_cross_splits() -> None:
    """Frames from one explicit trajectory must remain in one split."""

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=0.0),
            trajectory_id="trajectory-a",
        ),
        _sample(
            sample_id="sample-b",
            configuration_id="configuration-b",
            split=FLiBeDatasetSplit.TEST,
            configuration=_configuration(offset=10.0),
            trajectory_id="trajectory-a",
        ),
    )

    with pytest.raises(
        ValueError,
        match="trajectory_id must not cross dataset splits",
    ):
        validate_flibe_split_isolation(samples)


def test_known_parent_and_derived_sample_must_not_cross_splits() -> None:
    """Known parent-derived lineage must remain isolated to one split."""

    samples = (
        _sample(
            sample_id="parent-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=0.0),
        ),
        _sample(
            sample_id="child-a",
            configuration_id="configuration-b",
            split=FLiBeDatasetSplit.VALIDATION,
            configuration=_configuration(offset=10.0),
            parent_sample_id="parent-a",
        ),
    )

    with pytest.raises(
        ValueError,
        match="parent and derived sample must not cross dataset splits",
    ):
        validate_flibe_split_isolation(samples)


def test_same_configuration_id_is_allowed_within_one_split() -> None:
    """Repeated declared identity is allowed when it does not leak across splits."""

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-shared",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=0.0),
        ),
        _sample(
            sample_id="sample-b",
            configuration_id="configuration-shared",
            split=FLiBeDatasetSplit.TRAINING,
            configuration=_configuration(offset=10.0),
        ),
    )

    assert validate_flibe_split_isolation(samples) is samples


def test_group_and_trajectory_may_repeat_within_same_split() -> None:
    """Related samples may coexist when their split assignment is identical."""

    samples = (
        _sample(
            sample_id="sample-a",
            configuration_id="configuration-a",
            split=FLiBeDatasetSplit.VALIDATION,
            configuration=_configuration(offset=0.0),
            group_id="group-a",
            trajectory_id="trajectory-a",
        ),
        _sample(
            sample_id="sample-b",
            configuration_id="configuration-b",
            split=
