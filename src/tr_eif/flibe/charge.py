"""Formal ionic-charge contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from .configuration import FLiBeConfiguration
from .species import FLiBeSpecies


FormalCharge: TypeAlias = int
SpeciesCharge: TypeAlias = tuple[
    FLiBeSpecies,
    FormalCharge,
]
SpeciesCharges: TypeAlias = tuple[
    SpeciesCharge,
    ...,
]


FLIBE_FORMAL_CHARGES: SpeciesCharges = (
    (
        FLiBeSpecies.LITHIUM,
        1,
    ),
    (
        FLiBeSpecies.BERYLLIUM,
        2,
    ),
    (
        FLiBeSpecies.FLUORINE,
        -1,
    ),
)


def formal_charge(
    species: FLiBeSpecies,
) -> FormalCharge:
    """Return the formal ionic charge assigned to one FLiBe species."""

    if not isinstance(
        species,
        FLiBeSpecies,
    ):
        raise TypeError(
            "species must be an FLiBeSpecies."
        )

    return dict(
        FLIBE_FORMAL_CHARGES
    )[species]


def formal_charge_from_symbol(
    symbol: str,
) -> FormalCharge:
    """Return the formal ionic charge for one canonical species symbol."""

    if not isinstance(
        symbol,
        str,
    ):
        raise TypeError(
            "symbol must be a string."
        )

    try:
        species = FLiBeSpecies(
            symbol
        )
    except ValueError as error:
        raise ValueError(
            f"unsupported FLiBe species symbol: {symbol!r}."
        ) from error

    return formal_charge(
        species
    )


def configuration_formal_charges(
    configuration: FLiBeConfiguration,
) -> tuple[FormalCharge, ...]:
    """Return per-atom formal charges in configuration atom order."""

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be an FLiBeConfiguration."
        )

    return tuple(
        formal_charge(
            species
        )
        for species in configuration.species
    )


def total_formal_charge(
    configuration: FLiBeConfiguration,
) -> FormalCharge:
    """Return the total formal charge of an FLiBe configuration."""

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be an FLiBeConfiguration."
        )

    return sum(
        configuration_formal_charges(
            configuration
        )
    )


def is_formally_neutral(
    configuration: FLiBeConfiguration,
) -> bool:
    """Return whether an FLiBe configuration has zero total formal charge."""

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be an FLiBeConfiguration."
        )

    return (
        total_formal_charge(
            configuration
        )
        == 0
    )


@dataclass(frozen=True)
class FormalChargeState:
    """Per-atom and total formal-charge state for an FLiBe configuration."""

    charges: tuple[FormalCharge, ...]
    total_charge: FormalCharge

    def __post_init__(self) -> None:
        """Validate the formal-charge state."""

        if not isinstance(
            self.charges,
            tuple,
        ):
            raise TypeError(
                "charges must be a tuple."
            )

        if len(
            self.charges
        ) == 0:
            raise ValueError(
                "charges must not be empty."
            )

        normalized_charges = tuple(
            _validate_formal_charge(
                charge,
                "charge",
            )
            for charge in self.charges
        )

        normalized_total = _validate_formal_charge(
            self.total_charge,
            "total_charge",
        )

        if sum(
            normalized_charges
        ) != normalized_total:
            raise ValueError(
                "total_charge must equal the sum of charges."
            )

        object.__setattr__(
            self,
            "charges",
            normalized_charges,
        )

        object.__setattr__(
            self,
            "total_charge",
            normalized_total,
        )

    @property
    def is_neutral(self) -> bool:
        """Return whether the total formal charge is zero."""

        return self.total_charge == 0


def _validate_formal_charge(
    value: int,
    name: str,
) -> FormalCharge:
    """Validate one finite integral formal-charge value."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        int,
    ):
        raise TypeError(
            f"{name} must be a non-Boolean integer."
        )

    if not isfinite(
        value
    ):
        raise ValueError(
            f"{name} must be finite."
        )

    return value


def build_formal_charge_state(
    configuration: FLiBeConfiguration,
) -> FormalChargeState:
    """Build the formal-charge state for one FLiBe configuration."""

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be an FLiBeConfiguration."
        )

    charges = configuration_formal_charges(
        configuration
    )

    return FormalChargeState(
        charges=charges,
        total_charge=sum(
            charges
        ),
    )
