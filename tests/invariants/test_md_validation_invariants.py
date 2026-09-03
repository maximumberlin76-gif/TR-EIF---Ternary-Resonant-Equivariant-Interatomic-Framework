"""Validation-invariant tests for TR-EIF molecular dynamics."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.md import (
    MolecularDynamicsState,
    accelerations_from_forces,
    velocity_verlet_position,
    velocity_verlet_positions,
    velocity_verlet_velocities,
)


def _configuration(
    atom_count: int = 2,
) -> AtomicConfiguration:
    """Construct a deterministic nonperiodic atomic configuration."""

    if atom_count == 1:
        return AtomicConfiguration(
            species=("A",),
            positions=((0.0, 0.0, 0.0),),
        )

    return AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
    )


def test_md_state_rejects_velocity_count_mismatch() -> None:
    """MD state requires exactly one velocity vector per atom."""

    with pytest.raises(
        ValueError,
        match="velocities must contain one vector per atom",
    ):
        MolecularDynamicsState(
            configuration=_configuration(),
            velocities=((0.0, 0.0, 0.0),),
            masses=(1.0, 1.0),
        )


def test_md_state_rejects_mass_count_mismatch() -> None:
    """MD state requires exactly one mass per atom."""

    with pytest.raises(
        ValueError,
        match="masses must contain one value per atom",
    ):
        MolecularDynamicsState(
            configuration=_configuration(),
            velocities=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            masses=(1.0,),
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        0.0,
        -1.0,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_md_state_rejects_nonpositive_or_nonfinite_mass(
    invalid_mass: float,
) -> None:
    """MD state masses must be finite and strictly positive."""

    with pytest.raises(ValueError):
        MolecularDynamicsState(
            configuration=_configuration(atom_count=1),
            velocities=((0.0, 0.0, 0.0),),
            masses=(invalid_mass,),
        )


@pytest.mark.parametrize(
    "invalid_component",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_md_state_rejects_nonfinite_velocity_component(
    invalid_component: float,
) -> None:
    """Every Cartesian velocity component must be finite."""

    with pytest.raises(
        ValueError,
        match="must be finite",
    ):
        MolecularDynamicsState(
            configuration=_configuration(atom_count=1),
            velocities=((invalid_component, 0.0, 0.0),),
            masses=(1.0,),
        )


def test_md_state_rejects_negative_step() -> None:
    """MD discrete step index must remain nonnegative."""

    with pytest.raises(
        ValueError,
        match="step must be nonnegative",
    ):
        MolecularDynamicsState(
            configuration=_configuration(atom_count=1),
            velocities=((0.0, 0.0, 0.0),),
            masses=(1.0,),
            step=-1,
        )


@pytest.mark.parametrize(
    "invalid_time",
    (
        -1.0,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_md_state_rejects_invalid_time(
    invalid_time: float,
) -> None:
    """MD time must be finite and nonnegative."""

    with pytest.raises(ValueError):
        MolecularDynamicsState(
            configuration=_configuration(atom_count=1),
            velocities=((0.0, 0.0, 0.0),),
            masses=(1.0,),
            time=invalid_time,
        )


def test_accelerations_require_matching_mass_count() -> None:
    """Force-to-acceleration conversion requires one mass per force."""

    forces = ForceState(
        forces=(
            (1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
        )
    )

    with pytest.raises(
        ValueError,
        match="masses must contain one value per force vector",
    ):
        accelerations_from_forces(
            forces=forces,
            masses=(1.0,),
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_accelerations_reject_nonfinite_mass_directly(
    invalid_mass: float,
) -> None:
    """Force-to-acceleration boundary independently rejects nonfinite mass."""

    forces = ForceState(
        forces=((1.0, 2.0, 3.0),)
    )

    with pytest.raises(
        ValueError,
        match="masses\\[0\\] must be finite",
    ):
        accelerations_from_forces(
            forces=forces,
            masses=(invalid_mass,),
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        0.0,
        -1.0,
    ),
)
def test_accelerations_reject_nonpositive_mass_directly(
    invalid_mass: float,
) -> None:
    """Force-to-acceleration boundary requires strictly positive mass."""

    forces = ForceState(
        forces=((1.0, 2.0, 3.0),)
    )

    with pytest.raises(
        ValueError,
        match="masses\\[0\\] must be greater than zero",
    ):
        accelerations_from_forces(
            forces=forces,
            masses=(invalid_mass,),
        )


def test_accelerations_preserve_force_atom_count() -> None:
    """Valid force-to-acceleration conversion preserves atom count."""

    forces = ForceState(
        forces=(
            (2.0, 4.0, 6.0),
            (-3.0, 0.0, 9.0),
        )
    )

    accelerations = accelerations_from_forces(
        forces=forces,
        masses=(2.0, 3.0),
    )

    assert accelerations == (
        (1.0, 2.0, 3.0),
        (-1.0, 0.0, 3.0),
    )
    assert len(accelerations) == forces.atom_count


@pytest.mark.parametrize(
    "invalid_time_step",
    (
        0.0,
        -0.01,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_verlet_position_rejects_invalid_time_step(
    invalid_time_step: float,
) -> None:
    """Velocity-Verlet drift requires a finite positive timestep."""

    with pytest.raises(ValueError):
        velocity_verlet_position(
            position=(0.0, 0.0, 0.0),
            velocity=(1.0, 0.0, 0.0),
            acceleration=(0.0, 0.0, 0.0),
            time_step=invalid_time_step,
        )


def test_verlet_positions_require_matching_velocity_count() -> None:
    """Vectorized Verlet drift requires one velocity per position."""

    with pytest.raises(
        ValueError,
        match="velocities must contain one vector per position",
    ):
        velocity_verlet_positions(
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            velocities=((0.0, 0.0, 0.0),),
            accelerations=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            time_step=0.01,
        )


def test_verlet_positions_require_matching_acceleration_count() -> None:
    """Vectorized Verlet drift requires one acceleration per position."""

    with pytest.raises(
        ValueError,
        match="accelerations must contain one vector per position",
    ):
        velocity_verlet_positions(
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            velocities=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            accelerations=((0.0, 0.0, 0.0),),
            time_step=0.01,
        )


def test_verlet_velocities_require_matching_before_count() -> None:
    """Velocity completion requires one pre-step acceleration per atom."""

    with pytest.raises(
        ValueError,
        match="accelerations_before must contain one vector per velocity",
    ):
        velocity_verlet_velocities(
            velocities=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            accelerations_before=((0.0, 0.0, 0.0),),
            accelerations_after=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            time_step=0.01,
        )


def test_verlet_velocities_require_matching_after_count() -> None:
    """Velocity completion requires one post-step acceleration per atom."""

    with pytest.raises(
        ValueError,
        match="accelerations_after must contain one vector per velocity",
    ):
        velocity_verlet_velocities(
            velocities=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            accelerations_before=(
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ),
            accelerations_after=((0.0, 0.0, 0.0),),
            time_step=0.01,
        )
