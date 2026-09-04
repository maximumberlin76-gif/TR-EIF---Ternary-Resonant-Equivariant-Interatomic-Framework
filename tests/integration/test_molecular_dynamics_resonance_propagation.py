"""Integration tests for explicit TR-EIF MD resonance propagation."""

from math import pi

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.resonance_propagation import (
    MolecularDynamicsResonanceStep,
    propagate_md_resonance_state,
)
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.resonance import (
    PhaseDynamicsParameters,
    ResonanceState,
    euler_step,
)


def _md_state(
    positions: tuple[tuple[float, float, float], ...] = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    ),
) -> MolecularDynamicsState:
    """Construct a deterministic nonperiodic MD state."""

    atom_count = len(positions)

    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=tuple(
                f"A{index}"
                for index in range(atom_count)
            ),
            positions=positions,
        ),
        velocities=tuple(
            (0.0, 0.0, 0.0)
            for _ in range(atom_count)
        ),
        masses=tuple(
            1.0
            for _ in range(atom_count)
        ),
        step=4,
        time=0.5,
    )


def _periodic_md_state() -> MolecularDynamicsState:
    """Construct a deterministic fully periodic MD state."""

    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=("A", "B"),
            positions=(
                (0.2, 0.0, 0.0),
                (9.8, 0.0, 0.0),
            ),
            cell=(
                (10.0, 0.0, 0.0),
                (0.0, 10.0, 0.0),
                (0.0, 0.0, 10.0),
            ),
            periodic=(True, True, True),
        ),
        velocities=(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        ),
        masses=(1.0, 1.0),
    )


def _resonance_state() -> ResonanceState:
    """Construct a deterministic two-oscillator resonance state."""

    return ResonanceState(
        phases=(0.0, 0.5 * pi),
        frequencies=(0.1, -0.2),
    )


def _parameters() -> PhaseDynamicsParameters:
    """Construct deterministic two-oscillator phase parameters."""

    return PhaseDynamicsParameters(
        coupling=(0.5, 0.25),
        phase_lag=(0.0, 0.0),
    )


def test_md_resonance_propagation_uses_current_cutoff_graph() -> None:
    """The MD configuration must determine the graph used for propagation."""

    md_state = _md_state()

    result = propagate_md_resonance_state(
        md_state=md_state,
        resonance_state=_resonance_state(),
        parameters=_parameters(),
        cutoff=1.1,
        time_step=0.2,
    )

    expected_graph = build_cutoff_graph(
        md_state.configuration,
        cutoff=1.1,
    )

    assert result.graph == expected_graph
    assert result.graph.node_count == md_state.atom_count
    assert result.graph.edge_count == 2


def test_md_resonance_propagation_matches_existing_euler_integrator() -> None:
    """The MD bridge must delegate phase evolution to the existing integrator."""

    md_state = _md_state()
    resonance_state = _resonance_state()
    parameters = _parameters()
    graph = build_cutoff_graph(
        md_state.configuration,
        cutoff=1.1,
    )

    expected = euler_step(
        state=resonance_state,
        parameters=parameters,
        graph=graph,
        time_step=0.2,
    )

    result = propagate_md_resonance_state(
        md_state=md_state,
        resonance_state=resonance_state,
        parameters=parameters,
        cutoff=1.1,
        time_step=0.2,
    )

    assert result.current == expected


def test_known_two_oscillator_phase_update_is_preserved() -> None:
    """Graph-coupled phase evolution must retain the declared KS semantics."""

    result = propagate_md_resonance_state(
        md_state=_md_state(),
        resonance_state=_resonance_state(),
        parameters=_parameters(),
        cutoff=1.1,
        time_step=0.2,
    )

    assert result.current.phases[0] == pytest.approx(0.12)
    assert result.current.phases[1] == pytest.approx(
        0.5 * pi - 0.09
    )


def test_frequency_vector_is_preserved() -> None:
    """The current explicit phase integrator must not alter frequencies."""

    resonance_state = _resonance_state()

    result = propagate_md_resonance_state(
        md_state=_md_state(),
        resonance_state=resonance_state,
        parameters=_parameters(),
        cutoff=1.1,
        time_step=0.2,
    )

    assert result.current.frequencies == resonance_state.frequencies
    assert result.previous.frequencies == resonance_state.frequencies


def test_md_state_is_not_modified_by_resonance_propagation() -> None:
    """Resonance propagation must not perform a hidden MD update."""

    md_state = _md_state()

    result = propagate_md_resonance_state(
        md_state=md_state,
        resonance_state=_resonance_state(),
        parameters=_parameters(),
        cutoff=1.1,
        time_step=0.2,
    )

    assert result.md_state is md_state
    assert result.md_state.configuration == md_state.configuration
    assert result.md_state.velocities == md_state.velocities
    assert result.md_state.masses == md_state.masses
    assert result.md_state.step == 4
    assert result.md_state.time == 0.5


def test_previous_resonance_state_is_retained_explicitly() -> None:
    """The propagation record must preserve the input resonance state."""

    resonance_state = _resonance_state()

    result = propagate_md_resonance_state(
        md_state=_md_state(),
        resonance_state=resonance_state,
        parameters=_parameters(),
        cutoff=1.1,
        time_step=0.2,
    )

    assert result.previous is resonance_state
    assert result.current is not resonance_state


def test_no_edge_graph_advances_only_by_intrinsic_frequency() -> None:
    """Without interaction edges, Euler evolution must use intrinsic frequencies."""

    result = propagate_md_resonance_state(
        md_state=_md_state(),
        resonance_state=_resonance_state(),
        parameters=_parameters(),
        cutoff=0.5,
        time_step=0.2,
    )

    assert result.graph.edge_count == 0
    assert result.current.phases[0] == pytest.approx(0.02)
    assert result.current.phases[1] == pytest.approx(
        0.5 * pi - 0.04
    )


def test_periodic_graph_uses_existing_minimum_image_semantics() -> None:
    """Periodic resonance propagation must preserve cutoff-graph PBC semantics."""

    md_state = _periodic_md_state()
    resonance_state = ResonanceState(
        phases=(0.0, 0.5 * pi),
        frequencies=(0.0, 0.0),
    )
    parameters = PhaseDynamicsParameters(
        coupling=(0.5, 0.5),
        phase_lag=(0.0, 0.0),
    )

    result = propagate_md_resonance_state(
        md_state=md_state,
        resonance_state=resonance_state,
        parameters=parameters,
        cutoff=0.5,
        time_step=0.1,
    )

    direct = build_cutoff_graph(
        md_state.configuration,
        cutoff=0.5,
    )

    assert result.graph == direct
    assert result.graph.edge_count == 2


def test_propagation_is_deterministic() -> None:
    """Repeated propagation from identical immutable inputs must be identical."""

    md_state = _md_state()
    resonance_state = _resonance_state()
    parameters = _parameters()

    first = propagate_md_resonance_state(
        md_state=md_state,
        resonance_state=resonance_state,
        parameters=parameters,
        cutoff=1.1,
        time_step=0.2,
    )
    second = propagate_md_resonance_state(
        md_state=md_state,
        resonance_state=resonance_state,
        parameters=parameters,
        cutoff=1.1,
        time_step=0.2,
    )

    assert first == second


def test_resonance_oscillator_count_must_match_md_atom_count() -> None:
    """The executable bridge requires one oscillator per MD graph node."""

    resonance_state = ResonanceState(
        phases=(0.0,),
        frequencies=(0.0,),
    )

    with pytest.raises(
        ValueError,
        match="resonance oscillator count must match MD atom count",
    ):
        propagate_md_resonance_state(
            md_state=_md_state(),
            resonance_state=resonance_state,
            parameters=PhaseDynamicsParameters(
                coupling=(0.0,),
                phase_lag=(0.0,),
            ),
            cutoff=1.1,
            time_step=0.2,
        )


def test_parameter_vector_size_must_match_md_atom_count() -> None:
    """Phase-dynamics parameter vectors must match the MD node count."""

    with pytest.raises(
        ValueError,
        match="does not match the parameter-vector size",
    ):
        propagate_md_resonance_state(
            md_state=_md_state(),
            resonance_state=_resonance_state(),
            parameters=PhaseDynamicsParameters(
                coupling=(0.5,),
                phase_lag=(0.0,),
            ),
            cutoff=1.1,
            time_step=0.2,
        )


@pytest.mark.parametrize(
    ("cutoff", "exception"),
    (
        (0.0, ValueError),
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("cutoff", TypeError),
    ),
)
def test_cutoff_validation(
    cutoff: object,
    exception: type[Exception],
) -> None:
    """MD resonance propagation requires a positive finite real cutoff."""

    with pytest.raises(exception):
        propagate_md_resonance_state(
            md_state=_md_state(),
            resonance_state=_resonance_state(),
            parameters=_parameters(),
            cutoff=cutoff,  # type: ignore[arg-type]
            time_step=0.2,
        )


@pytest.mark.parametrize(
    ("time_step", "exception"),
    (
        (0.0, ValueError),
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("dt", TypeError),
    ),
)
def test_time_step_validation(
    time_step: object,
    exception: type[Exception],
) -> None:
    """MD resonance propagation requires a positive finite real time step."""

    with pytest.raises(exception):
        propagate_md_resonance_state(
            md_state=_md_state(),
            resonance_state=_resonance_state(),
            parameters=_parameters(),
            cutoff=1.1,
            time_step=time_step,  # type: ignore[arg-type]
        )


def test_result_record_rejects_frequency_mutation() -> None:
    """The result contract must reject implicit frequency evolution."""

    md_state = _md_state()
    previous = _resonance_state()
    current = ResonanceState(
        phases=previous.phases,
        frequencies=(0.2, -0.2),
    )
    graph = build_cutoff_graph(
        md_state.configuration,
        cutoff=1.1,
    )

    with pytest.raises(
        ValueError,
        match="must preserve the frequency vector",
    ):
        MolecularDynamicsResonanceStep(
            md_state=md_state,
            previous=previous,
            current=current,
            graph=graph,
            cutoff=1.1,
            time_step=0.2,
        )


def test_result_record_rejects_graph_node_count_mismatch() -> None:
    """A propagation record cannot bind the MD state to a different graph size."""

    md_state = _md_state()
    previous = _resonance_state()
    current = euler_step(
        state=previous,
        parameters=_parameters(),
        graph=build_cutoff_graph(
            md_state.configuration,
            cutoff=1.1,
        ),
        time_step=0.2,
    )
    one_atom_graph = build_cutoff_graph(
        _md_state(
            positions=((0.0, 0.0, 0.0),)
        ).configuration,
        cutoff=1.1,
    )

    with pytest.raises(
        ValueError,
        match="graph node count must match MD atom count",
    ):
        MolecularDynamicsResonanceStep(
            md_state=md_state,
            previous=previous,
            current=current,
            graph=one_atom_graph,
            cutoff=1.1,
            time_step=0.2,
        )
