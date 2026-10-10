"""FLiBe-specific resonance descriptor contract for the TR-EIF domain layer."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.resonance import (
    ResonanceDescriptor,
    ResonanceState,
    resonance_descriptor,
)

from .configuration import FLiBeConfiguration
from .coordination import FLiBeCoordinationState
from .thermodynamic_state import FLiBeThermodynamicState
from .units import ParameterProvenance


def _validate_source_metadata(
    source: str | None,
    provenance: ParameterProvenance,
) -> str | None:
    """Validate source metadata for one FLiBe resonance descriptor."""

    if source is not None and not isinstance(source, str):
        raise TypeError(
            "source must be a string or None."
        )

    if isinstance(source, str):
        if source == "":
            raise ValueError(
                "source must not be empty."
            )

        if source != source.strip():
            raise ValueError(
                "source must not contain leading or trailing whitespace."
            )

    if (
        provenance is ParameterProvenance.PRIMARY_SOURCE
        and source is None
    ):
        raise ValueError(
            "PRIMARY_SOURCE provenance requires source."
        )

    return source


@dataclass(frozen=True)
class FLiBeResonanceDescriptor:
    """Resonance descriptor bound to explicit FLiBe physical context.

    The continuous resonance descriptor is computed only from the supplied
    ResonanceState using the base TR-EIF resonance layer. FLiBe
    configuration, graph-relative coordination, and thermodynamic state are
    retained as explicit context and are not silently folded into the
    resonance coordinate.

    Graph-relative coordination is not identified with chemical bonding or
    experimental coordination. Thermodynamic temperature and pressure are not
    identified with oscillator phase, frequency, phase order, or resonance.
    """

    configuration: FLiBeConfiguration
    coordination: FLiBeCoordinationState
    thermodynamic_state: FLiBeThermodynamicState
    resonance_state: ResonanceState
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate all FLiBe/resonance context boundaries."""

        if not isinstance(
            self.configuration,
            FLiBeConfiguration,
        ):
            raise TypeError(
                "configuration must be an FLiBeConfiguration."
            )

        if not isinstance(
            self.coordination,
            FLiBeCoordinationState,
        ):
            raise TypeError(
                "coordination must be an FLiBeCoordinationState."
            )

        if not isinstance(
            self.thermodynamic_state,
            FLiBeThermodynamicState,
        ):
            raise TypeError(
                "thermodynamic_state must be an "
                "FLiBeThermodynamicState."
            )

        if not isinstance(
            self.resonance_state,
            ResonanceState,
        ):
            raise TypeError(
                "resonance_state must be a ResonanceState."
            )

        if not isinstance(
            self.provenance,
            ParameterProvenance,
        ):
            raise TypeError(
                "provenance must be a ParameterProvenance."
            )

        atom_count = self.configuration.atom_count

        if self.coordination.atom_count != atom_count:
            raise ValueError(
                "coordination atom count must match configuration atom count."
            )

        if self.resonance_state.oscillator_count != atom_count:
            raise ValueError(
                "resonance oscillator count must match configuration atom count."
            )

        configuration_species = self.configuration.species

        coordination_species = tuple(
            atom.species
            for atom in self.coordination.atoms
        )

        if coordination_species != configuration_species:
            raise ValueError(
                "coordination species ordering must match configuration species."
            )

        self.configuration.composition()

        normalized_source = _validate_source_metadata(
            self.source,
            self.provenance,
        )

        object.__setattr__(
            self,
            "source",
            normalized_source,
        )

    @property
    def descriptor(self) -> ResonanceDescriptor:
        """Return the base continuous resonance descriptor."""

        return resonance_descriptor(
            self.resonance_state
        )

    @property
    def coordinate(self) -> tuple[float, float]:
        """Return the base resonance coordinate without FLiBe feature mixing."""

        return self.descriptor.as_coordinate()

    @property
    def composition(self):
        """Return the exact LiF-BeF2 composition of the bound configuration."""

        return self.configuration.composition()

    @property
    def phase_order(self) -> float:
        """Return the base phase-order component."""

        return self.descriptor.phase_order

    @property
    def frequency_spread(self) -> float:
        """Return the base frequency-spread component."""

        return self.descriptor.frequency_spread


def build_flibe_resonance_descriptor(
    configuration: FLiBeConfiguration,
    coordination: FLiBeCoordinationState,
    thermodynamic_state: FLiBeThermodynamicState,
    resonance_state: ResonanceState,
    provenance: ParameterProvenance,
    source: str | None = None,
) -> FLiBeResonanceDescriptor:
    """Construct one validated FLiBe-specific resonance descriptor record."""

    return FLiBeResonanceDescriptor(
        configuration=configuration,
        coordination=coordination,
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance_state,
        provenance=provenance,
        source=source,
    )
