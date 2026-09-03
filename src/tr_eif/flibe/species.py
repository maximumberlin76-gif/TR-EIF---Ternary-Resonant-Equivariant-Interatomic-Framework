"""Chemical species identifiers for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from enum import Enum
from typing import TypeAlias


class FLiBeSpecies(str, Enum):
    """Canonical chemical species represented in the FLiBe domain."""

    LITHIUM = "Li"
    BERYLLIUM = "Be"
    FLUORINE = "F"


SpeciesTuple: TypeAlias = tuple[FLiBeSpecies, ...]


FLIBE_SPECIES: SpeciesTuple = (
    FLiBeSpecies.LITHIUM,
    FLiBeSpecies.BERYLLIUM,
    FLiBeSpecies.FLUORINE,
)


def flibe_species_symbols() -> tuple[str, ...]:
    """Return canonical FLiBe species symbols in Li, Be, F order."""

    return tuple(
        species.value
        for species in FLIBE_SPECIES
    )


def flibe_species_from_symbol(
    symbol: str,
) -> FLiBeSpecies:
    """Return the canonical FLiBe species for one exact element symbol."""

    if not isinstance(
        symbol,
        str,
    ):
        raise TypeError(
            "symbol must be a string."
        )

    try:
        return FLiBeSpecies(
            symbol
        )
    except ValueError as error:
        raise ValueError(
            f"unsupported FLiBe species symbol: {symbol!r}."
        ) from error


def is_flibe_species_symbol(
    symbol: object,
) -> bool:
    """Return whether an object is an exact supported FLiBe symbol."""

    if not isinstance(
        symbol,
        str,
    ):
        return False

    try:
        FLiBeSpecies(
            symbol
        )
    except ValueError:
        return False

    return True


def validate_flibe_species_sequence(
    species: tuple[str, ...],
) -> SpeciesTuple:
    """Validate and canonicalize a nonempty FLiBe species sequence."""

    if not isinstance(
        species,
        tuple,
    ):
        raise TypeError(
            "species must be a tuple."
        )

    if len(species) == 0:
        raise ValueError(
            "species must not be empty."
        )

    return tuple(
        flibe_species_from_symbol(
            symbol
        )
        for symbol in species
    )
