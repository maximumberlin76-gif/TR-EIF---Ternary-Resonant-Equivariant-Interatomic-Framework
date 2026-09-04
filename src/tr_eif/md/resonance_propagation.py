"""Explicit resonance-state propagation for TR-EIF molecular dynamics."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.graph import InteractionGraph, build_cutoff_graph
from tr_eif.resonance import (
    PhaseDynamicsParameters,
    ResonanceState,
    euler_step,
)

from .state import MolecularDynamicsState


def _validate_positive_finite(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one positive finite real scalar."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(value):
        raise ValueError(
            f"{field_name} must be finite."
        )

    normalized = float(value)

    if normalized <= 0.0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class MolecularDynamicsResonanceStep:
    """Result of one explicit resonance update on one MD configuration."""

    md_state: MolecularDynamicsState
    previous: ResonanceState
    current: ResonanceState
    graph: InteractionGraph
    cutoff: float
    time_step: float

    def __post_init__(self) -> None:
        if not isinstance(self.md_state, MolecularDynamicsState):
            raise TypeError(
                "md_state must be a MolecularDynamicsState instance."
            )

        if not isinstance(self.previous, ResonanceState):
            raise TypeError(
                "previous must be a ResonanceState instance."
            )

        if not isinstance(self.current, ResonanceState):
            raise TypeError(
                "current must be a ResonanceState instance."
            )

        if not isinstance(self.graph, InteractionGraph):
            raise TypeError(
                "graph must be an InteractionGraph instance."
            )

        cutoff = _validate_positive_finite(
            self.cutoff,
            field_name="cutoff",
        )
        time_step = _validate_positive_finite(
            self.time_step,
            field_name="time_step",
        )

        atom_count = self.md_state.atom_count

        if self.previous.oscillator_count != atom_count:
            raise ValueError(
                "previous resonance oscillator count must match MD atom count."
            )

        if self.current.oscillator_count != atom_count:
            raise ValueError(
                "current resonance oscillator count must match MD atom count."
            )

        if self.graph.node_count != atom_count:
            raise ValueError(
                "graph node count must match MD atom count."
            )

        if self.current.frequencies != self.previous.frequencies:
            raise ValueError(
                "resonance propagation must preserve the frequency vector "
                "under the current explicit Euler phase integrator."
            )

        object.__setattr__(
            self,
            "cutoff",
            cutoff,
        )
        object.__setattr__(
            self,
            "time_step",
            time_step,
        )


def propagate_md_resonance_state(
    md_state: MolecularDynamicsState,
    resonance_state: ResonanceState,
    parameters: PhaseDynamicsParameters,
    cutoff: float,
    time_step: float,
) -> MolecularDynamicsResonanceStep:
    """Advance resonance dynamics on the interaction graph of one MD state.

    The atomic configuration determines the graph used by the existing
    continuous resonance integrator. The molecular-dynamics state itself is
    not modified, and no ternary target or ternary execution step is produced.

    Oscillator state is associated one-to-one with graph nodes for this
    executable interface. Oscillator phase is not identified with a physical
    phase of matter.
    """

    if not isinstance(md_state, MolecularDynamicsState):
        raise TypeError(
            "md_state must be a MolecularDynamicsState instance."
        )

    if not isinstance(resonance_state, ResonanceState):
        raise TypeError(
            "resonance_state must be a ResonanceState instance."
        )

    if not isinstance(parameters, PhaseDynamicsParameters):
        raise TypeError(
            "parameters must be a PhaseDynamicsParameters instance."
        )

    atom_count = md_state.atom_count

    if resonance_state.oscillator_count != atom_count:
        raise ValueError(
            "resonance oscillator count must match MD atom count."
        )

    parameters.validate_oscillator_count(atom_count)

    validated_cutoff = _validate_positive_finite(
        cutoff,
        field_name="cutoff",
    )
    validated_time_step = _validate_positive_finite(
        time_step,
        field_name="time_step",
    )

    graph = build_cutoff_graph(
        configuration=md_state.configuration,
        cutoff=validated_cutoff,
    )

    current = euler_step(
        state=resonance_state,
        parameters=parameters,
        graph=graph,
        time_step=validated_time_step,
    )

    return MolecularDynamicsResonanceStep(
        md_state=md_state,
        previous=resonance_state,
        current=current,
        graph=graph,
        cutoff=validated_cutoff,
        time_step=validated_time_step,
    )
