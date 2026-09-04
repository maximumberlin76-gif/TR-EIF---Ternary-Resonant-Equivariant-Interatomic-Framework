"""Strict configuration parsing for TR-EIF atomic configurations."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path

from .state import AtomicConfiguration, Cell3x3, PeriodicAxes, Vector3

_REQUIRED_FIELDS = frozenset({"species", "positions"})
_ALLOWED_FIELDS = frozenset({"species", "positions", "cell", "periodic"})


class ConfigurationParseError(ValueError):
    """Raised when serialized configuration data violates the parser contract."""


def _require_sequence(value: object, *, field_name: str) -> Sequence[object]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ConfigurationParseError(f"{field_name} must be an array.")

    return value


def _parse_number(value: object, *, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigurationParseError(f"{field_name} must be a finite number.")

    result = float(value)

    if not (-float("inf") < result < float("inf")):
        raise ConfigurationParseError(f"{field_name} must be a finite number.")

    return result


def _parse_vector3(value: object, *, field_name: str) -> Vector3:
    sequence = _require_sequence(value, field_name=field_name)

    if len(sequence) != 3:
        raise ConfigurationParseError(
            f"{field_name} must contain exactly three components."
        )

    return (
        _parse_number(sequence[0], field_name=f"{field_name}[0]"),
        _parse_number(sequence[1], field_name=f"{field_name}[1]"),
        _parse_number(sequence[2], field_name=f"{field_name}[2]"),
    )


def _parse_species(value: object) -> tuple[str, ...]:
    sequence = _require_sequence(value, field_name="species")
    result: list[str] = []

    for index, symbol in enumerate(sequence):
        if not isinstance(symbol, str):
            raise ConfigurationParseError(
                f"species[{index}] must be a string."
            )

        if not symbol.strip():
            raise ConfigurationParseError(
                f"species[{index}] must not be empty."
            )

        result.append(symbol)

    return tuple(result)


def _parse_positions(value: object) -> tuple[Vector3, ...]:
    sequence = _require_sequence(value, field_name="positions")

    return tuple(
        _parse_vector3(
            position,
            field_name=f"positions[{index}]",
        )
        for index, position in enumerate(sequence)
    )


def _parse_cell(value: object) -> Cell3x3 | None:
    if value is None:
        return None

    sequence = _require_sequence(value, field_name="cell")

    if len(sequence) != 3:
        raise ConfigurationParseError(
            "cell must contain exactly three lattice vectors."
        )

    return (
        _parse_vector3(sequence[0], field_name="cell[0]"),
        _parse_vector3(sequence[1], field_name="cell[1]"),
        _parse_vector3(sequence[2], field_name="cell[2]"),
    )


def _parse_periodic(value: object) -> PeriodicAxes:
    sequence = _require_sequence(value, field_name="periodic")

    if len(sequence) != 3:
        raise ConfigurationParseError(
            "periodic must contain exactly three boolean flags."
        )

    if not all(isinstance(flag, bool) for flag in sequence):
        raise ConfigurationParseError(
            "periodic must contain only boolean flags."
        )

    return (
        sequence[0],
        sequence[1],
        sequence[2],
    )


def parse_atomic_configuration(
    data: Mapping[str, object],
) -> AtomicConfiguration:
    """Parse a strict mapping into an immutable atomic configuration."""

    keys = set(data)

    missing = sorted(_REQUIRED_FIELDS - keys)
    unknown = sorted(keys - _ALLOWED_FIELDS)

    if missing:
        raise ConfigurationParseError(
            "Missing required configuration field(s): "
            + ", ".join(missing)
            + "."
        )

    if unknown:
        raise ConfigurationParseError(
            "Unknown configuration field(s): "
            + ", ".join(unknown)
            + "."
        )

    species = _parse_species(data["species"])
    positions = _parse_positions(data["positions"])
    cell = _parse_cell(data.get("cell"))
    periodic = _parse_periodic(
        data.get(
            "periodic",
            (False, False, False),
        )
    )

    try:
        return AtomicConfiguration(
            species=species,
            positions=positions,
            cell=cell,
            periodic=periodic,
        )
    except (TypeError, ValueError) as exc:
        raise ConfigurationParseError(str(exc)) from exc


def _object_without_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}

    for key, value in pairs:
        if key in result:
            raise ConfigurationParseError(
                f"Duplicate JSON object key: {key}."
            )

        result[key] = value

    return result


def _reject_nonfinite_json_constant(value: str) -> object:
    raise ConfigurationParseError(
        f"Non-finite JSON number is not permitted: {value}."
    )


def parse_atomic_configuration_json(
    text: str,
) -> AtomicConfiguration:
    """Parse JSON text into an immutable atomic configuration."""

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    try:
        payload = json.loads(
            text,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except json.JSONDecodeError as exc:
        raise ConfigurationParseError(
            f"Invalid JSON at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}."
        ) from exc

    if not isinstance(payload, Mapping):
        raise ConfigurationParseError(
            "The top-level JSON value must be an object."
        )

    return parse_atomic_configuration(payload)


def load_atomic_configuration_json(
    path: str | Path,
) -> AtomicConfiguration:
    """Load a UTF-8 JSON atomic configuration from a filesystem path."""

    source = Path(path)

    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ConfigurationParseError(
            f"Unable to read configuration file: {source}."
        ) from exc

    return parse_atomic_configuration_json(text)
