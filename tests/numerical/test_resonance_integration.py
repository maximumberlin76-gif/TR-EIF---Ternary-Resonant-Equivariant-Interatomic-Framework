"""Qualification tests for TR-EIF resonance integration."""

import math

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import (
    PhaseDynamicsParameters,
    ResonanceState,
    euler_step,
    state_phase_order,
)


def _make_reference_system() -> tuple[
    ResonanceState,
    PhaseDynamicsParameters,
    object,
]:
    """Construct a deterministic three-oscillator reference system."""

    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 0.75, 0.0),
        ),
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    state = ResonanceState(
        phases=(
            0.1,
            2.0,
            5.5,
        ),
        frequencies=(
            0.25,
            -0.10,
            0.05,
        ),
    )

    parameters = PhaseDynamicsParameters(
        coupling=(
            0.30,
            0.20,
            0.40,
        ),
        phase_lag=(
            0.10,
            0.20,
            0.15,
        ),
    )

    return state, parameters, graph


def test_repeated_euler_step_is_deterministic() -> None:
    """Identical resonance inputs must produce identical next states."""

    state, parameters, graph = _make_reference_system()

    first = euler_step(
        state=state,
        parameters=parameters,
        graph=graph,
        time_step=0.01,
    )

    second = euler_step(
        state=state,
        parameters=parameters,
        graph=graph,
        time_step=0.01,
    )

    assert first == second


def test_long_integration_keeps_phases_finite_and_wrapped() -> None:
    """Repeated phase integration must retain finite wrapped phases."""

    state, parameters, graph = _make_reference_system()

    for _ in range(2000):
        state = euler_step(
            state=state,
            parameters=parameters,
            graph=graph,
            time_step=0.01,
        )

        for phase in state.phases:
            assert math.isfinite(phase)
            assert 0.0 <= phase < 2.0 * math.pi


def test_euler_step_preserves_frequency_vector() -> None:
    """Phase integration must not overwrite retained frequencies."""

    state, parameters, graph = _make_reference_system()

    expected_frequencies = state.frequencies

    for _ in range(100):
        state = euler_step(
            state=state,
            parameters=parameters,
            graph=graph,
            time_step=0.02,
        )

        assert state.frequencies == expected_frequencies


def test_phase_order_parameter_remains_bounded() -> None:
    """The phase-order magnitude must remain in its mathematical range."""

    state, parameters, graph = _make_reference_system()

    for _ in range(500):
        order = state_phase_order(state)

        assert math.isfinite(order)
        assert order >= 0.0
        assert order <= 1.0 + 1.0e-15

        state = euler_step(
            state=state,
            parameters=parameters,
            graph=graph,
            time_step=0.01,
        )


def test_identical_phases_have_unit_phase_order() -> None:
    """Equal oscillator phases must give phase-order magnitude one."""

    state = ResonanceState(
        phases=(
            1.25,
            1.25,
            1.25,
            1.25,
        ),
        frequencies=(
            0.0,
            0.0,
            0.0,
            0.0,
        ),
    )

    assert state_phase_order(state) == pytest.approx(
        1.0,
        abs=1.0e-15,
    )


def test_uniform_quadrature_phases_have_zero_phase_order() -> None:
    """Four uniformly distributed phases must cancel in phase order."""

    state = ResonanceState(
        phases=(
            0.0,
            0.5 * math.pi,
            math.pi,
            1.5 * math.pi,
        ),
        frequencies=(
            0.0,
            0.0,
            0.0,
            0.0,
        ),
    )

    assert state_phase_order(state) == pytest.approx(
        0.0,
        abs=1.0e-15,
    )


@pytest.mark.parametrize(
    "invalid_time_step",
    (
        0.0,
        -1.0e-3,
        math.nan,
        math.inf,
        -math.inf,
    ),
)
def test_euler_step_rejects_invalid_time_step(
    invalid_time_step: float,
) -> None:
    """Euler integration must reject nonpositive or nonfinite steps."""

    state, parameters, graph = _make_reference_system()

    with pytest.raises(ValueError):
        euler_step(
            state=state,
            parameters=parameters,
            graph=graph,
            time_step=invalid_time_step,
        )


@pytest.mark.parametrize(
    "invalid_time_step",
    (
        True,
        False,
        "0.01",
        None,
    ),
)
def test_euler_step_rejects_nonreal_time_step(
    invalid_time_step,
) -> None:
    """Euler integration must reject non-real time-step types."""

    state, parameters, graph = _make_reference_system()

    with pytest.raises(
        TypeError,
        match="time_step must be a real number",
    ):
        euler_step(
            state=state,
            parameters=parameters,
            graph=graph,
            time_step=invalid_time_step,
        )
