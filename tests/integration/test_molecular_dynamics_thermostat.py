"""Integration tests for deterministic TR-EIF MD velocity rescaling."""

from math import sqrt

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.md.observables import kinetic_energy
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.thermostat import (
    kinetic_temperature,
    rescale_to_kinetic_temperature,
    rescale_velocities,
    velocity_rescaling_factor,
)


def _state(
    velocities: tuple[tuple[float, float, float], ...] = (
        (1.0, 0.0, 0.0),
        (0.0, 2.0, 0.0),
    ),
) -> MolecularDynamicsState:
    """Construct a deterministic two-atom MD state."""

    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=("Li", "F"),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
        ),
        velocities=velocities,
        masses=(2.0, 1.0),
        step=7,
        time=1.25,
    )


def test_kinetic_temperature_uses_explicit_dof_and_boltzmann_constant() -> None:
    """Kinetic temperature must follow T = 2 K / (f k_B)."""

    state = _state()

    assert kinetic_energy(state).total_kinetic_energy == 3.0
    assert kinetic_temperature(
        state,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    ) == 2.0


def test_velocity_rescaling_factor_is_square_root_temperature_ratio() -> None:
    """Global velocity scaling must use sqrt(target/current)."""

    assert velocity_rescaling_factor(2.0, 8.0) == 2.0
    assert velocity_rescaling_factor(8.0, 2.0) == 0.5
    assert velocity_rescaling_factor(2.0, 0.0) == 0.0


def test_rescale_velocities_changes_only_velocity_components() -> None:
    """Direct scaling must preserve configuration, masses, step, and time."""

    state = _state()
    rescaled = rescale_velocities(state, 2.0)

    assert rescaled.configuration == state.configuration
    assert rescaled.masses == state.masses
    assert rescaled.step == state.step
    assert rescaled.time == state.time
    assert rescaled.velocities == (
        (2.0, 0.0, 0.0),
        (0.0, 4.0, 0.0),
    )


def test_velocity_scaling_changes_kinetic_energy_quadratically() -> None:
    """Scaling velocities by s must scale kinetic energy by s squared."""

    state = _state()
    scale = 1.5
    rescaled = rescale_velocities(state, scale)

    initial = kinetic_energy(state).total_kinetic_energy
    final = kinetic_energy(rescaled).total_kinetic_energy

    assert final == pytest.approx(initial * scale * scale)


def test_rescale_to_target_temperature_reaches_requested_temperature() -> None:
    """Deterministic rescaling must reach the declared target temperature."""

    state = _state()
    result = rescale_to_kinetic_temperature(
        state,
        target_temperature=8.0,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    )

    assert result.velocities == (
        (2.0, 0.0, 0.0),
        (0.0, 4.0, 0.0),
    )
    assert kinetic_temperature(
        result,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    ) == pytest.approx(8.0)


def test_rescale_to_zero_temperature_sets_all_velocities_to_zero() -> None:
    """A zero target must deterministically remove all kinetic motion."""

    state = _state()
    result = rescale_to_kinetic_temperature(
        state,
        target_temperature=0.0,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    )

    assert result.velocities == (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )
    assert kinetic_temperature(
        result,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    ) == 0.0


def test_zero_temperature_to_zero_temperature_is_identity() -> None:
    """Zero-to-zero rescaling must leave a zero-velocity state unchanged."""

    state = _state(
        velocities=(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        )
    )

    result = rescale_to_kinetic_temperature(
        state,
        target_temperature=0.0,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    )

    assert result == state
    assert velocity_rescaling_factor(0.0, 0.0) == 1.0


def test_zero_temperature_cannot_be_rescaled_to_positive_temperature() -> None:
    """Deterministic scaling cannot create velocity from a zero state."""

    state = _state(
        velocities=(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        )
    )

    with pytest.raises(
        ValueError,
        match="positive target temperature cannot be reached",
    ):
        rescale_to_kinetic_temperature(
            state,
            target_temperature=1.0,
            degrees_of_freedom=6,
            boltzmann_constant=0.5,
        )


def test_rescaling_is_deterministic() -> None:
    """Repeated rescaling from the same immutable state must be identical."""

    state = _state()

    first = rescale_to_kinetic_temperature(
        state,
        target_temperature=5.0,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    )
    second = rescale_to_kinetic_temperature(
        state,
        target_temperature=5.0,
        degrees_of_freedom=6,
        boltzmann_constant=0.5,
    )

    assert first == second


def test_nonmaximum_declared_degrees_of_freedom_is_respected() -> None:
    """The estimator must use the explicitly declared valid DOF count."""

    state = _state()

    assert kinetic_temperature(
        state,
        degrees_of_freedom=3,
        boltzmann_constant=0.5,
    ) == 4.0


@pytest.mark.parametrize(
    ("degrees_of_freedom", "exception"),
    (
        (0, ValueError),
        (-1, ValueError),
        (7, ValueError),
        (1.5, TypeError),
        (True, TypeError),
    ),
)
def test_degrees_of_freedom_validation(
    degrees_of_freedom: object,
    exception: type[Exception],
) -> None:
    """Degrees of freedom must be a valid positive integer for the state."""

    state = _state()

    with pytest.raises(exception):
        kinetic_temperature(
            state,
            degrees_of_freedom=degrees_of_freedom,  # type: ignore[arg-type]
            boltzmann_constant=0.5,
        )


@pytest.mark.parametrize(
    ("boltzmann_constant", "exception"),
    (
        (0.0, ValueError),
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("kB", TypeError),
    ),
)
def test_boltzmann_constant_validation(
    boltzmann_constant: object,
    exception: type[Exception],
) -> None:
    """The supplied Boltzmann constant must be a positive finite real."""

    state = _state()

    with pytest.raises(exception):
        kinetic_temperature(
            state,
            degrees_of_freedom=6,
            boltzmann_constant=boltzmann_constant,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("current_temperature", "target_temperature", "exception"),
    (
        (-1.0, 1.0, ValueError),
        (1.0, -1.0, ValueError),
        (float("inf"), 1.0, ValueError),
        (1.0, float("nan"), ValueError),
        (True, 1.0, TypeError),
        (1.0, False, TypeError),
    ),
)
def test_temperature_validation_for_rescaling_factor(
    current_temperature: object,
    target_temperature: object,
    exception: type[Exception],
) -> None:
    """Temperature inputs must be nonnegative finite real scalars."""

    with pytest.raises(exception):
        velocity_rescaling_factor(
            current_temperature,  # type: ignore[arg-type]
            target_temperature,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("scale", "exception"),
    (
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("scale", TypeError),
    ),
)
def test_velocity_scale_validation(
    scale: object,
    exception: type[Exception],
) -> None:
    """Velocity scale must be a nonnegative finite real scalar."""

    with pytest.raises(exception):
        rescale_velocities(
            _state(),
            scale,  # type: ignore[arg-type]
        )


def test_rescaling_factor_matches_explicit_square_root() -> None:
    """The scalar factor must agree with direct square-root evaluation."""

    current = 3.0
    target = 7.0

    assert velocity_rescaling_factor(
        current,
        target,
    ) == sqrt(target / current)
