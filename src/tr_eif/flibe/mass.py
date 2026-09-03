"""Atomic-mass parameter contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from .configuration import FLiBeConfiguration
from .species import FLiBeSpecies


AtomicMass: TypeAlias = float
SpeciesMass: TypeAlias = tuple[
    FLiBeSpecies,
    AtomicMass,
]
SpeciesMasses: TypeAlias = tuple[
    SpeciesMass,
    ...,
]


def _validate_atomic_mass(
    value: float,
    name: str,
) -> AtomicMass:
    """Validate one finite positive atomic-mass parameter."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            f"{name} must be a real non-Boolean number."
        )

    normalized = float(
        value
    )

    if not isfinite(
        normalized
    ):
        raise ValueError(
            f"{name} must be finite."
        )

    if normalized <= 0.0:
        raise ValueError(
            f"{name} must be positive."
        )

    return normalized


@dataclass(frozen=True)
class FLiBeMassParameters:
    """Explicit atomic-mass parameters for Li, Be, and F."""

    lithium: AtomicMass
    beryllium: AtomicMass
    fluorine: AtomicMass

    def __post_init__(self) -> None:
        """Validate and normalize all species mass parameters."""

        object.__setattr__(
            self,
            "lithium",
            _validate_atomic_mass(
                self.lithium,
                "lithium",
            ),
        )

        object.__setattr__(
            self,
            "beryllium",
            _validate_atomic_mass(
                self.beryllium,
                "beryllium",
            ),
        )

        object.__setattr__(
            self,
            "fluorine",
            _validate_atomic_mass(
                self.fluorine,
                "fluorine",
            ),
        )

    @property
    def species_masses(
        self,
    ) -> SpeciesMasses:
        """Return mass parameters in canonical Li, Be, F order."""

        return (
            (
                FLiBeSpecies.LITHIUM,
                self.lithium,
            ),
            (
                FLiBeSpecies.BERYLLIUM,
                self.beryllium,
            ),
            (
                FLiBeSpecies.FLUORINE,
                self.fluorine,
            ),
        )

    def mass_for_species(
        self,
        species: FLiBeSpecies,
    ) -> AtomicMass:
        """Return the mass parameter for one canonical FLiBe species."""

        if not isinstance(
            species,
            FLiBeSpecies,
        ):
            raise TypeError(
                "species must be an FLiBeSpecies."
            )

        return dict(
            self.species_masses
        )[species]

    def mass_for_symbol(
        self,
        symbol: str,
    ) -> AtomicMass:
        """Return the mass parameter for one canonical species symbol."""

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

        return self.mass_for_species(
            species
        )


def configuration_masses(
    configuration: FLiBeConfiguration,
    parameters: FLiBeMassParameters,
) -> tuple[AtomicMass, ...]:
    """Return per-atom masses in configuration atom order."""

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be an FLiBeConfiguration."
        )

    if not isinstance(
        parameters,
        FLiBeMassParameters,
    ):
        raise TypeError(
            "parameters must be an FLiBeMassParameters."
        )

    return tuple(
        parameters.mass_for_species(
            species
        )
        for species in configuration.species
    )


def total_configuration_mass(
    configuration: FLiBeConfiguration,
    parameters: FLiBeMassParameters,
) -> AtomicMass:
    """Return the total mass parameter of an FLiBe configuration."""

    return sum(
        configuration_masses(
            configuration,
            parameters,
        )
    )
