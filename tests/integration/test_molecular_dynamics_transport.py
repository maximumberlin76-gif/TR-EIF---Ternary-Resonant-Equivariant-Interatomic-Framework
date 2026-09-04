"""Integration tests for TR-EIF molecular-dynamics transport observables."""

from __future__ import annotations

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.graph import InteractionGraph
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory
from tr_eif.md.transport import (
    MeanSquaredDisplacementSeries,
    VelocityAutocorrelationSeries,
    mean_squared_displacement,
    velocity_autocorrelation,
)


def _state(
    *,
    positions: tuple[tuple[float, float, float], ...],
    velocities: tuple[tuple[float, float, float], ...],
    step: int,
    time: float,
    species: tuple[str, ...] = ("A", "B"),
    masses: tuple[float, ...] = (1.0, 2.0),
    periodic: bool = False,
) -> MolecularDynamicsState:
    """Construct one deterministic two-atom MD state."""

    if periodic:
        configuration = AtomicConfiguration(
            species=species,
            positions=positions,
            cell=(
                (10.0, 0.0, 0.0),
                (0.0, 10.0, 0.0),
                (0.0, 0.0, 10.0),
            ),
            periodic=(True, True, True),
        )
    else:
        configuration = AtomicConfiguration(
            species=species,
            positions=positions,
        )

    return MolecularDynamicsState(
        configuration=configuration,
        velocities=velocities,
        masses=masses,
        step=step,
        time=time,
    )


def _step(
    previous: MolecularDynamicsState,
    current: MolecularDynamicsState,
) -> MolecularDynamicsStepResult:
    """Construct a trajectory step with neutral graph and force boundaries."""

    graph = InteractionGraph(
        node_count=previous.atom_count,
        edges=(),
    )
    forces = ForceState(
        forces=tuple(
            (0.0, 0.0, 0.0)
            for _ in range(previous.atom_count)
        )
    )

    return MolecularDynamicsStepResult(
        previous=previous,
        current=current,
        graph_before=graph,
        graph_after=graph,
        forces_before=forces,
        forces_after=forces,
    )


def _trajectory() -> MolecularDynamicsTrajectory:
    """Construct a three-state nonperiodic transport fixture."""

    state_0 = _state(
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
        velocities=(
            (1.0, 0.0, 0.0),
            (0.0, 2.0, 0.0),
        ),
        step=4,
        time=0.50,
    )
    state_1 = _state(
        positions=(
            (1.0, 0.0, 0.0),
            (1.0, 2.0, 0.0),
        ),
        velocities=(
            (0.5, 0.0, 0.0),
            (0.0, 1.0, 0.0),
        ),
        step=5,
        time=0.75,
    )
    state_2 = _state(
        positions=(
            (2.0, 0.0, 0.0),
            (1.0, 4.0, 0.0),
        ),
        velocities=(
            (-1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        ),
        step=6,
        time=1.00,
    )

    return MolecularDynamicsTrajectory(
        steps=(
            _step(state_0, state_1),
            _step(state_1, state_2),
        )
    )


def _periodic_trajectory() -> MolecularDynamicsTrajectory:
    """Construct a two-state fully periodic transport fixture."""

    state_0 = _state(
        positions=(
            (9.9, 0.0, 0.0),
            (5.0, 0.0, 0.0),
        ),
        velocities=(
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
        ),
        step=0,
        time=0.0,
        periodic=True,
    )
    state_1 = _state(
        positions=(
            (0.1, 0.0, 0.0),
            (5.0, 0.0, 0.0),
        ),
        velocities=(
            (0.5, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        ),
        step=1,
        time=0.25,
        periodic=True,
    )

    return MolecularDynamicsTrajectory(
        steps=(
            _step(state_0, state_1),
        )
    )


def test_mean_squared_displacement_matches_cartesian_definition() -> None:
    """MSD must average squared displacement from the initial state."""

    result = mean_squared_displacement(
        _trajectory()
    )

    assert result.times == pytest.approx(
        (0.0, 0.25, 0.50)
    )
    assert result.values == pytest.approx(
        (0.0, 2.5, 10.0)
    )
    assert result.state_count == 3


def test_velocity_autocorrelation_matches_initial_time_origin_definition() -> None:
    """VACF must average v_i(0) dot v_i(t) over atoms."""

    result = velocity_autocorrelation(
        _trajectory()
    )

    assert result.times == pytest.approx(
        (0.0, 0.25, 0.50)
    )
    assert result.values == pytest.approx(
        (2.5, 1.25, -1.5)
    )
    assert result.state_count == 3


def test_transport_times_are_relative_to_initial_md_time() -> None:
    """Transport series must use elapsed rather than absolute MD time."""

    trajectory = _trajectory()

    assert trajectory.initial.time == 0.50
    assert mean_squared_displacement(trajectory).times == pytest.approx(
        (0.0, 0.25, 0.50)
    )
    assert velocity_autocorrelation(trajectory).times == pytest.approx(
        (0.0, 0.25, 0.50)
    )


def test_initial_mean_squared_displacement_is_zero() -> None:
    """The initial state must have zero displacement from itself."""

    assert mean_squared_displacement(
        _trajectory()
    ).values[0] == 0.0


def test_initial_velocity_autocorrelation_is_mean_squared_speed() -> None:
    """VACF at zero lag must equal the per-atom mean squared speed."""

    assert velocity_autocorrelation(
        _trajectory()
    ).values[0] == pytest.approx(2.5)


def test_velocity_autocorrelation_allows_negative_values() -> None:
    """Velocity reversal may produce a negative autocorrelation."""

    result = velocity_autocorrelation(
        _trajectory()
    )

    assert result.values[-1] < 0.0


def test_periodic_trajectory_is_rejected_for_msd() -> None:
    """MSD must not perform implicit periodic-coordinate unwrapping."""

    with pytest.raises(
        ValueError,
        match="requires explicit unwrapped coordinates",
    ):
        mean_squared_displacement(
            _periodic_trajectory()
        )


def test_periodic_trajectory_is_accepted_for_velocity_autocorrelation() -> None:
    """VACF does not depend on coordinate unwrapping."""

    result = velocity_autocorrelation(
        _periodic_trajectory()
    )

    assert result.times == pytest.approx(
        (0.0, 0.25)
    )
    assert result.values == pytest.approx(
        (1.0, -0.25)
    )


def test_species_order_must_remain_invariant() -> None:
    """Transport observables require stable particle identity ordering."""

    state_0 = _state(
        positions=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        velocities=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        step=0,
        time=0.0,
        species=("A", "B"),
    )
    state_1 = _state(
        positions=((0.1, 0.0, 0.0), (1.0, 0.0, 0.0)),
        velocities=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        step=1,
        time=0.1,
        species=("B", "A"),
    )
    trajectory = MolecularDynamicsTrajectory(
        steps=(_step(state_0, state_1),)
    )

    with pytest.raises(
        ValueError,
        match="invariant species ordering",
    ):
        mean_squared_displacement(trajectory)

    with pytest.raises(
        ValueError,
        match="invariant species ordering",
    ):
        velocity_autocorrelation(trajectory)


def test_atomic_masses_must_remain_invariant() -> None:
    """Transport observables require stable atomic masses."""

    state_0 = _state(
        positions=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        velocities=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        step=0,
        time=0.0,
        masses=(1.0, 2.0),
    )
    state_1 = _state(
        positions=((0.1, 0.0, 0.0), (1.0, 0.0, 0.0)),
        velocities=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        step=1,
        time=0.1,
        masses=(1.0, 3.0),
    )
    trajectory = MolecularDynamicsTrajectory(
        steps=(_step(state_0, state_1),)
    )

    with pytest.raises(
        ValueError,
        match="invariant atomic masses",
    ):
        mean_squared_displacement(trajectory)

    with pytest.raises(
        ValueError,
        match="invariant atomic masses",
    ):
        velocity_autocorrelation(trajectory)


def test_transport_observables_are_deterministic() -> None:
    """Repeated evaluation of one immutable trajectory must be identical."""

    trajectory = _trajectory()

    assert (
        mean_squared_displacement(trajectory)
        == mean_squared_displacement(trajectory)
    )
    assert (
        velocity_autocorrelation(trajectory)
        == velocity_autocorrelation(trajectory)
    )


def test_transport_functions_require_trajectory_instance() -> None:
    """Transport evaluation must reject non-trajectory inputs."""

    with pytest.raises(
        TypeError,
        match="trajectory must be a MolecularDynamicsTrajectory instance",
    ):
        mean_squared_displacement(None)  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="trajectory must be a MolecularDynamicsTrajectory instance",
    ):
        velocity_autocorrelation(None)  # type: ignore[arg-type]


def test_msd_series_normalizes_numeric_values_to_float() -> None:
    """MSD series construction must normalize accepted numeric inputs."""

    series = MeanSquaredDisplacementSeries(
        times=(0, 1),
        values=(0, 2),
    )

    assert series.times == (0.0, 1.0)
    assert series.values == (0.0, 2.0)


def test_vacf_series_allows_negative_values() -> None:
    """VACF series validation must permit signed autocorrelation values."""

    series = VelocityAutocorrelationSeries(
        times=(0.0, 1.0),
        values=(2.0, -1.0),
    )

    assert series.values == (2.0, -1.0)


@pytest.mark.parametrize(
    "series_type",
    (
        MeanSquaredDisplacementSeries,
        VelocityAutocorrelationSeries,
    ),
)
def test_transport_series_reject_empty_data(series_type: type) -> None:
    """A transport-observable series must contain at least one state."""

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        series_type(
            times=(),
            values=(),
        )


@pytest.mark.parametrize(
    "series_type",
    (
        MeanSquaredDisplacementSeries,
        VelocityAutocorrelationSeries,
    ),
)
def test_transport_series_require_matching_lengths(series_type: type) -> None:
    """Time and observable vectors must have identical cardinality."""

    with pytest.raises(
        ValueError,
        match="must have the same length",
    ):
        series_type(
            times=(0.0, 1.0),
            values=(0.0,),
        )


@pytest.mark.parametrize(
    "times",
    (
        (0.0, 0.0),
        (1.0, 0.5),
    ),
)
def test_transport_series_require_strictly_increasing_times(
    times: tuple[float, ...],
) -> None:
    """Transport series cannot contain repeated or decreasing time points."""

    with pytest.raises(
        ValueError,
        match="times must be strictly increasing",
    ):
        VelocityAutocorrelationSeries(
            times=times,
            values=(1.0, 1.0),
        )


@pytest.mark.parametrize(
    "times",
    (
        (-1.0,),
        (float("inf"),),
        (float("nan"),),
    ),
)
def test_transport_series_reject_invalid_times(
    times: tuple[float, ...],
) -> None:
    """Transport times must be finite and nonnegative."""

    with pytest.raises(ValueError):
        VelocityAutocorrelationSeries(
            times=times,
            values=(1.0,),
        )


def test_msd_series_rejects_negative_value() -> None:
    """MSD values must remain nonnegative by definition."""

    with pytest.raises(
        ValueError,
        match=r"values\[0\] must be nonnegative",
    ):
        MeanSquaredDisplacementSeries(
            times=(0.0,),
            values=(-1.0,),
        )


@pytest.mark.parametrize(
    "series_type",
    (
        MeanSquaredDisplacementSeries,
        VelocityAutocorrelationSeries,
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        float("inf"),
        float("nan"),
    ),
)
def test_transport_series_reject_nonfinite_values(
    series_type: type,
    value: float,
) -> None:
    """Transport observable values must be finite."""

    with pytest.raises(
        ValueError,
        match=r"values\[0\] must be finite",
    ):
        series_type(
            times=(0.0,),
            values=(value,),
        )
