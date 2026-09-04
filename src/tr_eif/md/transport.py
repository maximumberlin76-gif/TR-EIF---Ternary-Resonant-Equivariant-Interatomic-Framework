"""Transport observables for TR-EIF molecular-dynamics trajectories."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .state import MolecularDynamicsState
from .trajectory import MolecularDynamicsTrajectory


def _validate_series(
    times: tuple[float, ...],
    values: tuple[float, ...],
    *,
    nonnegative_values: bool,
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Validate one immutable transport-observable series."""

    if not isinstance(times, tuple):
        raise TypeError(
            "times must be a tuple."
        )

    if not isinstance(values, tuple):
        raise TypeError(
            "values must be a tuple."
        )

    if len(times) == 0:
        raise ValueError(
            "transport-observable series must not be empty."
        )

    if len(times) != len(values):
        raise ValueError(
            "times and values must have the same length."
        )

    normalized_times: list[float] = []
    normalized_values: list[float] = []
    previous_time: float | None = None

    for index, time in enumerate(times):
        if not isinstance(
            time,
            (int, float),
        ) or isinstance(time, bool):
            raise TypeError(
                f"times[{index}] must be a real number."
            )

        if not isfinite(time):
            raise ValueError(
                f"times[{index}] must be finite."
            )

        normalized_time = float(time)

        if normalized_time < 0.0:
            raise ValueError(
                f"times[{index}] must be nonnegative."
            )

        if (
            previous_time is not None
            and normalized_time <= previous_time
        ):
            raise ValueError(
                "times must be strictly increasing."
            )

        normalized_times.append(
            normalized_time
        )
        previous_time = normalized_time

    for index, value in enumerate(values):
        if not isinstance(
            value,
            (int, float),
        ) or isinstance(value, bool):
            raise TypeError(
                f"values[{index}] must be a real number."
            )

        if not isfinite(value):
            raise ValueError(
                f"values[{index}] must be finite."
            )

        normalized_value = float(value)

        if (
            nonnegative_values
            and normalized_value < 0.0
        ):
            raise ValueError(
                f"values[{index}] must be nonnegative."
            )

        normalized_values.append(
            normalized_value
        )

    return (
        tuple(normalized_times),
        tuple(normalized_values),
    )


@dataclass(frozen=True, slots=True)
class MeanSquaredDisplacementSeries:
    """Mean-squared displacement from the initial stored coordinates."""

    times: tuple[float, ...]
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        times, values = _validate_series(
            self.times,
            self.values,
            nonnegative_values=True,
        )

        object.__setattr__(
            self,
            "times",
            times,
        )
        object.__setattr__(
            self,
            "values",
            values,
        )

    @property
    def state_count(self) -> int:
        """Return the number of trajectory states represented."""

        return len(self.values)


@dataclass(frozen=True, slots=True)
class VelocityAutocorrelationSeries:
    """Per-atom mean velocity autocorrelation from the initial state."""

    times: tuple[float, ...]
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        times, values = _validate_series(
            self.times,
            self.values,
            nonnegative_values=False,
        )

        object.__setattr__(
            self,
            "times",
            times,
        )
        object.__setattr__(
            self,
            "values",
            values,
        )

    @property
    def state_count(self) -> int:
        """Return the number of trajectory states represented."""

        return len(self.values)


def _validate_trajectory(
    trajectory: MolecularDynamicsTrajectory,
) -> tuple[MolecularDynamicsState, ...]:
    """Validate particle identity and return the ordered MD states."""

    if not isinstance(
        trajectory,
        MolecularDynamicsTrajectory,
    ):
        raise TypeError(
            "trajectory must be a MolecularDynamicsTrajectory instance."
        )

    states = trajectory.states

    reference_species = (
        states[0].configuration.species
    )
    reference_masses = states[0].masses

    for state in states[1:]:
        if (
            state.configuration.species
            != reference_species
        ):
            raise ValueError(
                "transport observables require "
                "invariant species ordering."
            )

        if state.masses != reference_masses:
            raise ValueError(
                "transport observables require "
                "invariant atomic masses."
            )

    return states


def _elapsed_times(
    trajectory: MolecularDynamicsTrajectory,
) -> tuple[float, ...]:
    """Return trajectory times relative to the initial MD state."""

    states = trajectory.states
    initial_time = states[0].time

    return tuple(
        state.time - initial_time
        for state in states
    )


def mean_squared_displacement(
    trajectory: MolecularDynamicsTrajectory,
) -> MeanSquaredDisplacementSeries:
    """Evaluate mean-squared displacement from initial stored positions.

    The observable is the arithmetic mean over atoms of the squared
    Cartesian displacement from the initial trajectory state.

    Periodic trajectories are rejected because the current MD trajectory
    representation does not carry explicit image counters or an
    independently validated unwrapped-coordinate history. No hidden
    periodic-boundary unwrapping is performed by this operator.
    """

    states = _validate_trajectory(
        trajectory
    )

    if any(
        state.configuration.is_periodic
        for state in states
    ):
        raise ValueError(
            "mean-squared displacement requires explicit "
            "unwrapped coordinates; periodic trajectories "
            "are not accepted by this operator."
        )

    reference_positions = (
        states[0].configuration.positions
    )
    atom_count = states[0].atom_count

    values: list[float] = []

    for state in states:
        squared_sum = 0.0

        for reference, current in zip(
            reference_positions,
            state.configuration.positions,
            strict=True,
        ):
            dx = (
                current[0]
                - reference[0]
            )
            dy = (
                current[1]
                - reference[1]
            )
            dz = (
                current[2]
                - reference[2]
            )

            squared_sum += (
                dx * dx
                + dy * dy
                + dz * dz
            )

        values.append(
            squared_sum
            / float(atom_count)
        )

    return MeanSquaredDisplacementSeries(
        times=_elapsed_times(
            trajectory
        ),
        values=tuple(values),
    )


def velocity_autocorrelation(
    trajectory: MolecularDynamicsTrajectory,
) -> VelocityAutocorrelationSeries:
    """Evaluate mean velocity autocorrelation from the initial state.

    For each trajectory state, the observable is the arithmetic mean over
    atoms of v_i(0) dot v_i(t).

    No mass weighting, normalization, time-origin averaging, thermostat
    correction, Green-Kubo integration, or transport-coefficient inference
    is applied.
    """

    states = _validate_trajectory(
        trajectory
    )

    reference_velocities = (
        states[0].velocities
    )
    atom_count = states[0].atom_count

    values: list[float] = []

    for state in states:
        dot_sum = 0.0

        for reference, current in zip(
            reference_velocities,
            state.velocities,
            strict=True,
        ):
            dot_sum += (
                reference[0] * current[0]
                + reference[1] * current[1]
                + reference[2] * current[2]
            )

        values.append(
            dot_sum
            / float(atom_count)
        )

    return VelocityAutocorrelationSeries(
        times=_elapsed_times(
            trajectory
        ),
        values=tuple(values),
    )
