"""Explicit balanced-ternary propagation for TR-EIF molecular dynamics."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.ternary import (
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryVector,
    TernaryVectorExecutionStep,
    execute_ternary_vector_step,
)

from .state import MolecularDynamicsState


@dataclass(frozen=True, slots=True)
class MolecularDynamicsTernaryStep:
    """Result of one explicit ternary execution step on an MD state."""

    md_state: MolecularDynamicsState
    requested_targets: TernaryVector | None
    execution: TernaryVectorExecutionStep

    def __post_init__(self) -> None:
        if not isinstance(
            self.md_state,
            MolecularDynamicsState,
        ):
            raise TypeError(
                "md_state must be a MolecularDynamicsState instance."
            )

        if not isinstance(
            self.execution,
            TernaryVectorExecutionStep,
        ):
            raise TypeError(
                "execution must be a TernaryVectorExecutionStep instance."
            )

        atom_count = self.md_state.atom_count

        if self.execution.previous.node_count != atom_count:
            raise ValueError(
                "previous ternary execution node count must match "
                "MD atom count."
            )

        if self.execution.current.node_count != atom_count:
            raise ValueError(
                "current ternary execution node count must match "
                "MD atom count."
            )

        if self.requested_targets is not None:
            if not isinstance(self.requested_targets, tuple):
                raise TypeError(
                    "requested_targets must be a tuple or None."
                )

            if len(self.requested_targets) != atom_count:
                raise ValueError(
                    "requested_targets must match MD atom count."
                )

    @property
    def previous(self) -> TernaryExecutionVector:
        """Return the ternary execution vector before this event."""

        return self.execution.previous

    @property
    def current(self) -> TernaryExecutionVector:
        """Return the ternary execution vector after this event."""

        return self.execution.current

    @property
    def committed_count(self) -> int:
        """Return the number of committed ternary transition legs."""

        return self.execution.committed_count

    @property
    def held_count(self) -> int:
        """Return the number of nodes that committed no transition leg."""

        return self.execution.held_count


def propagate_md_ternary_state(
    md_state: MolecularDynamicsState,
    ternary_state: TernaryExecutionVector,
    requested_targets: TernaryVector | None = None,
    guards: tuple[TernaryExecutionGuard, ...] | None = None,
) -> MolecularDynamicsTernaryStep:
    """Execute one explicit balanced-ternary event for one MD state.

    The executable mapping is one ternary execution node per MD atom.

    Requested targets are supplied explicitly. This operator does not derive
    ternary targets from resonance state, phase order, energy, force,
    temperature, geometry, or any other molecular-dynamics observable.

    Existing balanced-ternary execution semantics remain authoritative:
    direct committed transitions between -1 and 1 are forbidden, opposite
    polarity routing enters active neutral first, pending targets remain
    distinct from retained neutral, and each committed route leg is one
    separate execution event.

    The molecular-dynamics state is retained unchanged by this operator.
    """

    if not isinstance(
        md_state,
        MolecularDynamicsState,
    ):
        raise TypeError(
            "md_state must be a MolecularDynamicsState instance."
        )

    if not isinstance(
        ternary_state,
        TernaryExecutionVector,
    ):
        raise TypeError(
            "ternary_state must be a TernaryExecutionVector instance."
        )

    if ternary_state.node_count != md_state.atom_count:
        raise ValueError(
            "ternary execution node count must match MD atom count."
        )

    if requested_targets is not None:
        if not isinstance(requested_targets, tuple):
            raise TypeError(
                "requested_targets must be a tuple or None."
            )

        if len(requested_targets) != md_state.atom_count:
            raise ValueError(
                "requested_targets must match MD atom count."
            )

    if guards is not None:
        if not isinstance(guards, tuple):
            raise TypeError(
                "guards must be a tuple or None."
            )

        if len(guards) != md_state.atom_count:
            raise ValueError(
                "guards must match MD atom count."
            )

        for index, guard in enumerate(guards):
            if not isinstance(
                guard,
                TernaryExecutionGuard,
            ):
                raise TypeError(
                    f"guards[{index}] must be a "
                    "TernaryExecutionGuard instance."
                )

    execution = execute_ternary_vector_step(
        state=ternary_state,
        requested_targets=requested_targets,
        guards=guards,
    )

    return MolecularDynamicsTernaryStep(
        md_state=md_state,
        requested_targets=requested_targets,
        execution=execution,
    )
