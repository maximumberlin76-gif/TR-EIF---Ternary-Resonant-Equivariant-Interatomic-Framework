"""Atomic-configuration contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import AtomicConfiguration

from .composition import FLiBeComposition
from .species import (
    FLiBeSpecies,
    validate_flibe_species_sequence,
)


SpeciesCounts: TypeAlias = tuple[
    tuple[FLiBeSpecies, int],
    ...,
]


@dataclass(frozen=True)
class FLiBeConfiguration:
    """FLiBe-domain view of one atomic configuration."""

    configuration: AtomicConfiguration

    def __post_init__(self) -> None:
        """Validate the atomic configuration against the FLiBe species domain."""

        if not isinstance(
            self.configuration,
            AtomicConfiguration,
        ):
            raise TypeError(
                "configuration must be an AtomicConfiguration."
            )

        validate_flibe_species_sequence(
            self.configuration.species
        )

    @property
    def atom_count(self) -> int:
        """Return the number of atoms in the configuration."""

        return len(
            self.configuration.species
        )

    @property
    def species(self) -> tuple[FLiBeSpecies, ...]:
        """Return canonical FLiBe species for all atoms."""

        return validate_flibe_species_sequence(
            self.configuration.species
        )

    @property
    def species_counts(self) -> SpeciesCounts:
        """Return Li, Be, and F atom counts in canonical species order."""

        species = self.species

        return (
            (
                FLiBeSpecies.LITHIUM,
                species.count(
                    FLiBeSpecies.LITHIUM
                ),
            ),
            (
                FLiBeSpecies.BERYLLIUM,
                species.count(
                    FLiBeSpecies.BERYLLIUM
                ),
            ),
            (
                FLiBeSpecies.FLUORINE,
                species.count(
                    FLiBeSpecies.FLUORINE
                ),
            ),
        )

    @property
    def atomic_fractions(
        self,
    ) -> tuple[
        tuple[FLiBeSpecies, float],
        ...,
    ]:
        """Return atomic fractions derived from discrete species counts."""

        atom_count = self.atom_count

        return tuple(
            (
                species,
                count / atom_count,
            )
            for species, count in self.species_counts
        )

    def composition(self) -> FLiBeComposition:
        """Return the LiF-BeF2 composition implied by exact stoichiometry."""

        counts = dict(
            self.species_counts
        )

        lithium_count = counts[
            FLiBeSpecies.LITHIUM
        ]
        beryllium_count = counts[
            FLiBeSpecies.BERYLLIUM
        ]
        fluorine_count = counts[
            FLiBeSpecies.FLUORINE
        ]

        if fluorine_count != (
            lithium_count
            + 2 * beryllium_count
        ):
            raise ValueError(
                "FLiBe configuration does not satisfy "
                "LiF-BeF2 fluorine stoichiometry."
            )

        if (
            lithium_count == 0
            and beryllium_count == 0
        ):
            raise ValueError(
                "FLiBe configuration must contain Li "
                "or Be formula units."
            )

        return FLiBeComposition(
            lif_fraction=float(
                lithium_count
            ),
            bef2_fraction=float(
                beryllium_count
            ),
        )

    def matches_composition(
        self,
        composition: FLiBeComposition,
        *,
        absolute_tolerance: float = 0.0,
    ) -> bool:
        """Return whether the discrete configuration matches a composition."""

        if not isinstance(
            composition,
            FLiBeComposition,
        ):
            raise TypeError(
                "composition must be an FLiBeComposition."
            )

        tolerance = _validate_absolute_tolerance(
            absolute_tolerance
        )

        actual = self.composition()

        return (
            abs(
                actual.lif_fraction
                - composition.lif_fraction
            )
            <= tolerance
            and abs(
                actual.bef2_fraction
                - composition.bef2_fraction
            )
            <= tolerance
        )


def _validate_absolute_tolerance(
    value: float,
) -> float:
    """Validate one finite nonnegative absolute tolerance."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            "absolute_tolerance must be a real "
            "non-Boolean number."
        )

    normalized = float(
        value
    )

    if not isfinite(
        normalized
    ):
        raise ValueError(
            "absolute_tolerance must be finite."
        )

    if normalized < 0.0:
        raise ValueError(
            "absolute_tolerance must be nonnegative."
        )

    return normalized


def validate_flibe_configuration(
    configuration: AtomicConfiguration,
) -> FLiBeConfiguration:
    """Validate and return an FLiBe-domain configuration wrapper."""

    return FLiBeConfiguration(
        configuration=configuration
    )


def flibe_species_counts(
    configuration: AtomicConfiguration,
) -> SpeciesCounts:
    """Return canonical FLiBe species counts for a configuration."""

    return validate_flibe_configuration(
        configuration
    ).species_counts
