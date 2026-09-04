"""Qualification tests for the TR-EIF atomic-configuration JSON Schema contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "schemas"
    / "configuration.schema.json"
)


def _load_schema() -> dict[str, object]:
    """Load the committed atomic-configuration schema."""

    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def _validator() -> Draft202012Validator:
    """Construct a Draft 2020-12 validator for the committed schema."""

    schema = _load_schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_configuration_schema_declares_draft_2020_12() -> None:
    """The configuration schema must declare the selected JSON Schema draft."""

    schema = _load_schema()

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(schema)


def test_minimal_nonperiodic_configuration_is_schema_valid() -> None:
    """The minimal parser-level structural configuration must validate."""

    instance = {
        "species": ["Li", "F"],
        "positions": [[0, 0, 0], [1.0, 2.0, 3.0]],
    }

    _validator().validate(instance)


def test_explicit_nonperiodic_configuration_without_cell_is_schema_valid() -> None:
    """Explicitly nonperiodic configurations do not require a cell."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "periodic": [False, False, False],
    }

    _validator().validate(instance)


def test_nonperiodic_configuration_with_null_cell_is_schema_valid() -> None:
    """A null cell is permitted when no periodic axis is active."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "cell": None,
        "periodic": [False, False, False],
    }

    _validator().validate(instance)


def test_periodic_configuration_with_cell_is_schema_valid() -> None:
    """Any active periodic axis is valid when a structural cell is supplied."""

    instance = {
        "species": ["Li", "Be", "F"],
        "positions": [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
        "cell": [[4, 0, 0], [0, 5, 0], [0, 0, 6]],
        "periodic": [True, False, True],
    }

    _validator().validate(instance)


@pytest.mark.parametrize(
    "instance",
    (
        {
            "positions": [[0, 0, 0]],
        },
        {
            "species": ["Li"],
        },
        {
            "species": [],
            "positions": [[0, 0, 0]],
        },
        {
            "species": [""],
            "positions": [[0, 0, 0]],
        },
        {
            "species": ["   "],
            "positions": [[0, 0, 0]],
        },
        {
            "species": ["Li"],
            "positions": [],
        },
    ),
)
def test_required_and_nonempty_arrays_are_enforced(
    instance: dict[str, object],
) -> None:
    """Required fields and nonempty structural arrays must be enforced."""

    assert not _validator().is_valid(instance)


@pytest.mark.parametrize(
    "positions",
    (
        [[0, 0]],
        [[0, 0, 0, 0]],
        [[0, "x", 0]],
        "0,0,0",
    ),
)
def test_position_vector_structure_is_enforced(positions: object) -> None:
    """Position entries must be numeric vectors with exactly three components."""

    instance = {
        "species": ["Li"],
        "positions": positions,
    }

    assert not _validator().is_valid(instance)


@pytest.mark.parametrize(
    "cell",
    (
        [[1, 0, 0], [0, 1, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0]],
        [[1, 0, 0], [0, 1, 0], [0, "x", 1]],
        "cell",
    ),
)
def test_cell_structure_is_enforced(cell: object) -> None:
    """A non-null cell must contain exactly three numeric three-vectors."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "cell": cell,
    }

    assert not _validator().is_valid(instance)


@pytest.mark.parametrize(
    "periodic",
    (
        [True, False],
        [True, False, False, False],
        [1, False, False],
        [True, None, False],
        True,
    ),
)
def test_periodic_axis_structure_is_enforced(periodic: object) -> None:
    """Periodic metadata must contain exactly three Boolean axis flags."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "cell": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "periodic": periodic,
    }

    assert not _validator().is_valid(instance)


def test_active_periodic_axis_requires_cell() -> None:
    """An active periodic axis must make the cell field structurally required."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "periodic": [True, False, False],
    }

    assert not _validator().is_valid(instance)


def test_active_periodic_axis_rejects_null_cell() -> None:
    """A periodic configuration must provide a non-null 3x3 cell."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "cell": None,
        "periodic": [False, True, False],
    }

    assert not _validator().is_valid(instance)


def test_unknown_configuration_field_is_rejected() -> None:
    """The schema must reject fields outside the configuration contract."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "unknown": 1,
    }

    assert not _validator().is_valid(instance)


def test_schema_does_not_encode_species_position_cardinality_invariant() -> None:
    """Cross-array cardinality remains an AtomicConfiguration invariant."""

    instance = {
        "species": ["Li", "F"],
        "positions": [[0, 0, 0]],
    }

    assert _validator().is_valid(instance)


def test_schema_does_not_encode_nonzero_cell_determinant_invariant() -> None:
    """Cell nondegeneracy remains an AtomicConfiguration invariant."""

    instance = {
        "species": ["Li"],
        "positions": [[0, 0, 0]],
        "cell": [[1, 0, 0], [2, 0, 0], [0, 0, 1]],
        "periodic": [True, True, True],
    }

    assert _validator().is_valid(instance)
