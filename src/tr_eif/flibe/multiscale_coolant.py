"""Multiscale coolant-model contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from tr_eif.configuration import Vector3
from tr_eif.multiscale import (
    MultiscaleHierarchy,
    MultiscaleStateHierarchy,
    build_multiscale_state_hierarchy,
)

from .configuration import FLiBeConfiguration
from .mass import (
    FLiBeMassParameters,
    configuration_masses,
)


FinePositions: TypeAlias = tuple[Vector3, ...]


@dataclass(frozen=True)
class FLiBeMultiscaleCoolantModel:
    """Explicit FLiBe fine-to-coarse mass and geometry mapping."""

    hierarchy: MultiscaleHierarchy
    mass_parameters: FLiBeMassParameters

    def __post_init__(self) -> None:
        """Validate the multiscale hierarchy and mass-parameter contract."""

        if not isinstance(
            self.hierarchy,
            MultiscaleHierarchy,
        ):
            raise TypeError(
                "hierarchy must be a MultiscaleHierarchy."
            )

        if not isinstance(
            self.mass_parameters,
            FLiBeMassParameters,
        ):
            raise TypeError(
                "mass_parameters must be an FLiBeMassParameters."
            )

    def build_state(
        self,
        configuration: FLiBeConfiguration,
        *,
        positions: FinePositions | None = None,
    ) -> MultiscaleStateHierarchy:
        """Build coarse FLiBe states across the configured hierarchy."""

        if not isinstance(
            configuration,
            FLiBeConfiguration,
        ):
            raise TypeError(
                "configuration must be an FLiBeConfiguration."
            )

        if self.hierarchy.finest_count != configuration.atom_count:
            raise ValueError(
                "hierarchy finest_count must match "
                "FLiBe configuration atom_count."
            )

        selected_positions = _select_fine_positions(
            configuration,
            positions,
        )

        masses = configuration_masses(
            configuration,
            self.mass_parameters,
        )

        return build_multiscale_state_hierarchy(
            positions=selected_positions,
            masses=masses,
            hierarchy=self.hierarchy,
        )


def _select_fine_positions(
    configuration: FLiBeConfiguration,
    positions: FinePositions | None,
) -> FinePositions:
    """Select explicit fine positions without hiding periodic unwrapping."""

    if positions is None:
        if any(
            configuration.configuration.periodic
        ):
            raise ValueError(
                "periodic FLiBe multiscale evaluation requires "
                "explicit unwrapped positions."
            )

        return configuration.configuration.positions

    if not isinstance(
        positions,
        tuple,
    ):
        raise TypeError(
            "positions must be a tuple or None."
        )

    if len(positions) != configuration.atom_count:
        raise ValueError(
            "positions must contain one vector per FLiBe atom."
        )

    return positions


def build_flibe_multiscale_coolant_state(
    model: FLiBeMultiscaleCoolantModel,
    configuration: FLiBeConfiguration,
    *,
    positions: FinePositions | None = None,
) -> MultiscaleStateHierarchy:
    """Build one FLiBe multiscale coolant state hierarchy."""

    if not isinstance(
        model,
        FLiBeMultiscaleCoolantModel,
    ):
        raise TypeError(
            "model must be an FLiBeMultiscaleCoolantModel."
        )

    return model.build_state(
        configuration,
        positions=positions,
    )
