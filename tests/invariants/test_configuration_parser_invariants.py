"""Qualification tests for the TR-EIF atomic-configuration parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from tr_eif.configuration import (
    AtomicConfiguration,
    ConfigurationParseError,
    load_atomic_configuration_json,
    parse_atomic_configuration,
    parse_atomic_configuration_json,
)


def test_parse_valid_mapping() -> None:
    """A valid mapping must produce the normalized immutable configuration."""

    configuration = parse_atomic_configuration(
        {
            "species": ["Li", "F"],
            "positions": [
                [0, 0.5, 1],
                [1.25, 2, 3.5],
            ],
        }
    )

    assert configuration == AtomicConfiguration(
        species=("Li", "F"),
        positions=(
            (0.0, 0.5, 1.0),
            (1.25, 2.0, 3.5),
        ),
    )


def test_parse_valid_json() -> None:
    """Valid JSON must parse through the public JSON parser."""

    configuration = parse_atomic_configuration_json(
        """
        {
          "species": ["Li", "F"],
          "positions": [[0, 0, 0], [1, 2, 3]]
        }
        """
    )

    assert configuration.species == ("Li", "F")
    assert configuration.positions == (
        (0.0, 0.0, 0.0),
        (1.0, 2.0, 3.0),
    )


def test_load_valid_json_file(tmp_path: Path) -> None:
    """A UTF-8 JSON file must load through the public file parser."""

    path = tmp_path / "configuration.json"
    path.write_text(
        """
        {
          "species": ["Li"],
          "positions": [[0.25, 0.5, 0.75]]
        }
        """,
        encoding="utf-8",
    )

    configuration = load_atomic_configuration_json(path)

    assert configuration == AtomicConfiguration(
        species=("Li",),
        positions=((0.25, 0.5, 0.75),),
    )


def test_default_periodic_state_is_nonperiodic() -> None:
    """Omitted cell and periodic fields must preserve the nonperiodic default."""

    configuration = parse_atomic_configuration(
        {
            "species": ["Li"],
            "positions": [[0, 0, 0]],
        }
    )

    assert configuration.cell is None
    assert configuration.periodic == (False, False, False)
    assert configuration.is_periodic is False


def test_parse_periodic_configuration() -> None:
    """Explicit cell and periodic flags must survive strict parsing."""

    configuration = parse_atomic_configuration(
        {
            "species": ["Li", "F"],
            "positions": [
                [0, 0, 0],
                [1, 1, 1],
            ],
            "cell": [
                [4, 0, 0],
                [0, 5, 0],
                [0, 0, 6],
            ],
            "periodic": [True, False, True],
        }
    )

    assert configuration.cell == (
        (4.0, 0.0, 0.0),
        (0.0, 5.0, 0.0),
        (0.0, 0.0, 6.0),
    )
    assert configuration.periodic == (True, False, True)
    assert configuration.is_periodic is True


def test_unknown_field_is_rejected() -> None:
    """Fields outside the strict parser contract must be rejected."""

    with pytest.raises(
        ConfigurationParseError,
        match=r"Unknown configuration field\(s\): extra\.",
    ):
        parse_atomic_configuration(
            {
                "species": ["Li"],
                "positions": [[0, 0, 0]],
                "extra": "not-permitted",
            }
        )


@pytest.mark.parametrize(
    ("payload", "missing_field"),
    (
        (
            {"species": ["Li"]},
            "positions",
        ),
        (
            {"positions": [[0, 0, 0]]},
            "species",
        ),
    ),
)
def test_missing_required_field_is_rejected(
    payload: dict[str, object],
    missing_field: str,
) -> None:
    """Both required fields must be present."""

    with pytest.raises(
        ConfigurationParseError,
        match=rf"Missing required configuration field\(s\): {missing_field}\.",
    ):
        parse_atomic_configuration(payload)


@pytest.mark.parametrize(
    "species",
    (
        "Li",
        [1],
        [""],
        ["   "],
    ),
)
def test_malformed_species_is_rejected(species: object) -> None:
    """Species must be a sequence of nonempty strings."""

    with pytest.raises(ConfigurationParseError):
        parse_atomic_configuration(
            {
                "species": species,
                "positions": [[0, 0, 0]],
            }
        )


@pytest.mark.parametrize(
    "positions",
    (
        "0,0,0",
        [0, 0, 0],
        [[0, 0]],
        [[0, 0, True]],
        [[0, "x", 0]],
    ),
)
def test_malformed_positions_are_rejected(positions: object) -> None:
    """Positions must be arrays of finite three-component numeric vectors."""

    with pytest.raises(ConfigurationParseError):
        parse_atomic_configuration(
            {
                "species": ["Li"],
                "positions": positions,
            }
        )


@pytest.mark.parametrize(
    "cell",
    (
        "cell",
        [[1, 0, 0], [0, 1, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0]],
        [[1, 0, 0], [0, 1, 0], [0, False, 1]],
    ),
)
def test_malformed_cell_is_rejected(cell: object) -> None:
    """A supplied cell must contain exactly three numeric lattice vectors."""

    with pytest.raises(ConfigurationParseError):
        parse_atomic_configuration(
            {
                "species": ["Li"],
                "positions": [[0, 0, 0]],
                "cell": cell,
            }
        )


@pytest.mark.parametrize(
    "periodic",
    (
        True,
        [True, False],
        [True, False, False, False],
        [1, False, False],
        [True, None, False],
    ),
)
def test_malformed_periodic_is_rejected(periodic: object) -> None:
    """Periodic metadata must contain exactly three Boolean flags."""

    with pytest.raises(ConfigurationParseError):
        parse_atomic_configuration(
            {
                "species": ["Li"],
                "positions": [[0, 0, 0]],
                "periodic": periodic,
            }
        )


def test_duplicate_json_keys_are_rejected() -> None:
    """Duplicate keys must not be silently overwritten by JSON decoding."""

    with pytest.raises(
        ConfigurationParseError,
        match=r"Duplicate JSON object key: species\.",
    ):
        parse_atomic_configuration_json(
            """
            {
              "species": ["Li"],
              "species": ["F"],
              "positions": [[0, 0, 0]]
            }
            """
        )


@pytest.mark.parametrize(
    "constant",
    (
        "NaN",
        "Infinity",
        "-Infinity",
    ),
)
def test_nonfinite_json_numbers_are_rejected(constant: str) -> None:
    """JSON NaN and infinity extensions are outside the parser contract."""

    with pytest.raises(
        ConfigurationParseError,
        match="Non-finite JSON number is not permitted",
    ):
        parse_atomic_configuration_json(
            f"""
            {{
              "species": ["Li"],
              "positions": [[0, 0, {constant}]]
            }}
            """
        )


@pytest.mark.parametrize(
    "text",
    (
        "[]",
        '"configuration"',
        "1",
        "null",
        "true",
    ),
)
def test_nonobject_json_root_is_rejected(text: str) -> None:
    """The top-level JSON value must be an object."""

    with pytest.raises(
        ConfigurationParseError,
        match="The top-level JSON value must be an object",
    ):
        parse_atomic_configuration_json(text)


@pytest.mark.parametrize(
    ("payload", "message"),
    (
        (
            {
                "species": [],
                "positions": [],
            },
            "must contain at least one atom",
        ),
        (
            {
                "species": ["Li", "F"],
                "positions": [[0, 0, 0]],
            },
            "must contain the same number of atoms",
        ),
        (
            {
                "species": ["Li"],
                "positions": [[0, 0, 0]],
                "periodic": [True, False, False],
            },
            "simulation cell is required",
        ),
        (
            {
                "species": ["Li"],
                "positions": [[0, 0, 0]],
                "cell": [
                    [1, 0, 0],
                    [2, 0, 0],
                    [0, 0, 1],
                ],
            },
            "must define a nonzero volume",
        ),
    ),
)
def test_atomic_configuration_invariants_are_propagated(
    payload: dict[str, object],
    message: str,
) -> None:
    """Final state invariants must be exposed as parser errors."""

    with pytest.raises(
        ConfigurationParseError,
        match=message,
    ) as captured:
        parse_atomic_configuration(payload)

    assert isinstance(captured.value.__cause__, ValueError)


def test_parse_result_is_deterministic() -> None:
    """Equivalent repeated parses must produce equal normalized states."""

    payload = {
        "species": ["Li", "F"],
        "positions": [
            [0, 0.5, 1],
            [1.25, 2, 3.5],
        ],
        "cell": [
            [4, 0, 0],
            [0, 5, 0],
            [0, 0, 6],
        ],
        "periodic": [True, True, True],
    }

    first = parse_atomic_configuration(payload)
    second = parse_atomic_configuration(payload)
    from_json = parse_atomic_configuration_json(
        """
        {
          "periodic": [true, true, true],
          "cell": [[4, 0, 0], [0, 5, 0], [0, 0, 6]],
          "positions": [[0, 0.5, 1], [1.25, 2, 3.5]],
          "species": ["Li", "F"]
        }
        """
    )

    assert first == second == from_json


def test_invalid_json_is_rejected() -> None:
    """Malformed JSON syntax must be wrapped in ConfigurationParseError."""

    with pytest.raises(
        ConfigurationParseError,
        match="Invalid JSON at line",
    ):
        parse_atomic_configuration_json(
            '{"species": ["Li"], "positions": [[0, 0, 0]]'
        )


def test_unreadable_file_is_rejected(tmp_path: Path) -> None:
    """Filesystem read failures must be exposed through the parser error type."""

    missing = tmp_path / "missing.json"

    with pytest.raises(
        ConfigurationParseError,
        match="Unable to read configuration file",
    ):
        load_atomic_configuration_json(missing)
