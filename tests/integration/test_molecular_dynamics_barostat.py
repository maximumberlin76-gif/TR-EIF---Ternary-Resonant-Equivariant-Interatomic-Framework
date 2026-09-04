"""Integration tests for deterministic TR-EIF isotropic MD pressure coupling."""

from __future__ import annotations

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.md.barostat import (
    apply_isotropic_barostat,
    isotropic_barostat_scale,
    scale_periodic_configuration,
)
from tr_eif.md.state import MolecularDynamicsState


def _periodic_configuration() -> AtomicConfiguration:
    """Construct a fully periodic deterministic atomic configuration."""

    return AtomicConfiguration(
        species=("Li", "F"),
        positions=(
            (0.5, 1.0, 1.5),
            (1.0, 1.5, 2.0),
        ),
        cell=(
            (2.0, 0.0, 0.0),
            (0.0, 3.0, 0.0),
            (0.0, 0.0, 4.0),
        ),
        periodic=(True, True, True),
    )


def _state() -> MolecularDynamicsState:
    """Construct a deterministic fully periodic MD state."""

    return MolecularDynamicsState(
        configuration=_periodic_configuration(),
        velocities=(
            (1.0, 0.0, 0.0),
            (0.0, 2.0, 0.0),
        ),
        masses=(2.0, 1.0),
        step=11,
        time=2.5,
    )


def _cell_determinant(
    cell: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ],
) -> float:
    """Return the determinant of one 3x3 cell."""

    a, b, c = cell

    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def test_equal_current_and_target_pressure_gives_identity_scale() -> None:
    """Equal pressures must produce an isotropic scale of one."""

    scale = isotropic_barostat_scale(
        current_pressure=2.0,
        target_pressure=2.0,
        compressibility=0.1,
        time_step=0.5,
        coupling_time=2.0,
    )

    assert scale == 1.0


def test_scale_cube_matches_declared_volume_relation() -> None:
    """The linear scale cubed must equal the declared volume scale."""

    current_pressure = 3.0
    target_pressure = 1.0
    compressibility = 0.2
    time_step = 0.5
    coupling_time = 2.0

    scale = isotropic_barostat_scale(
        current_pressure=current_pressure,
        target_pressure=target_pressure,
        compressibility=compressibility,
        time_step=time_step,
        coupling_time=coupling_time,
    )

    expected_volume_scale = (
        1.0
        - (time_step / coupling_time)
        * compressibility
        * (target_pressure - current_pressure)
    )

    assert scale**3 == pytest.approx(expected_volume_scale)


def test_pressure_above_target_expands_cell_scale() -> None:
    """Current pressure above target must produce an expansion factor."""

    scale = isotropic_barostat_scale(
        current_pressure=2.0,
        target_pressure=1.0,
        compressibility=0.1,
        time_step=0.5,
        coupling_time=1.0,
    )

    assert scale > 1.0


def test_pressure_below_target_contracts_cell_scale() -> None:
    """Current pressure below target must produce a contraction factor."""

    scale = isotropic_barostat_scale(
        current_pressure=1.0,
        target_pressure=2.0,
        compressibility=0.1,
        time_step=0.5,
        coupling_time=1.0,
    )

    assert 0.0 < scale < 1.0


def test_configuration_scaling_is_affine_and_isotropic() -> None:
    """Positions and cell vectors must receive the same Cartesian scale."""

    configuration = _periodic_configuration()

    scaled = scale_periodic_configuration(
        configuration,
        linear_scale=2.0,
    )

    assert scaled.species == configuration.species
    assert scaled.periodic == configuration.periodic

    assert scaled.positions == (
        (1.0, 2.0, 3.0),
        (2.0, 3.0, 4.0),
    )

    assert scaled.cell == (
        (4.0, 0.0, 0.0),
        (0.0, 6.0, 0.0),
        (0.0, 0.0, 8.0),
    )


def test_isotropic_scaling_changes_volume_by_scale_cube() -> None:
    """Cell volume must scale by the cube of the linear factor."""

    configuration = _periodic_configuration()

    assert configuration.cell is not None

    linear_scale = 1.5

    scaled = scale_periodic_configuration(
        configuration,
        linear_scale=linear_scale,
    )

    assert scaled.cell is not None

    initial_volume = _cell_determinant(
        configuration.cell
    )
    scaled_volume = _cell_determinant(
        scaled.cell
    )

    assert scaled_volume == pytest.approx(
        initial_volume * linear_scale**3
    )


def test_identity_configuration_scaling_preserves_configuration() -> None:
    """A unit linear scale must reproduce the original configuration."""

    configuration = _periodic_configuration()

    scaled = scale_periodic_configuration(
        configuration,
        linear_scale=1.0,
    )

    assert scaled == configuration


def test_apply_barostat_scales_configuration_only() -> None:
    """Barostat application must retain velocity, mass, step, and time state."""

    state = _state()

    result = apply_isotropic_barostat(
        state,
        current_pressure=7.0,
        target_pressure=0.0,
        compressibility=1.0,
        time_step=1.0,
        coupling_time=1.0,
    )

    assert result.configuration.positions == (
        (1.0, 2.0, 3.0),
        (2.0, 3.0, 4.0),
    )

    assert result.configuration.cell == (
        (4.0, 0.0, 0.0),
        (0.0, 6.0, 0.0),
        (0.0, 0.0, 8.0),
    )

    assert result.velocities == state.velocities
    assert result.masses == state.masses
    assert result.step == state.step
    assert result.time == state.time


def test_apply_barostat_is_deterministic() -> None:
    """Repeated application to the same immutable state must be identical."""

    state = _state()

    first = apply_isotropic_barostat(
        state,
        current_pressure=2.0,
        target_pressure=1.0,
        compressibility=0.1,
        time_step=0.5,
        coupling_time=2.0,
    )

    second = apply_isotropic_barostat(
        state,
        current_pressure=2.0,
        target_pressure=1.0,
        compressibility=0.1,
        time_step=0.5,
        coupling_time=2.0,
    )

    assert first == second


def test_nonperiodic_configuration_is_rejected() -> None:
    """Barostat scaling requires a simulation cell and periodic geometry."""

    configuration = AtomicConfiguration(
        species=("Li",),
        positions=((0.0, 0.0, 0.0),),
    )

    with pytest.raises(
        ValueError,
        match="requires a simulation cell",
    ):
        scale_periodic_configuration(
            configuration,
            linear_scale=1.0,
        )


def test_partially_periodic_configuration_is_rejected() -> None:
    """The isotropic operator must not silently scale partial periodicity."""

    configuration = AtomicConfiguration(
        species=("Li",),
        positions=((0.0, 0.0, 0.0),),
        cell=(
            (2.0, 0.0, 0.0),
            (0.0, 2.0, 0.0),
            (0.0, 0.0, 2.0),
        ),
        periodic=(True, True, False),
    )

    with pytest.raises(
        ValueError,
        match="requires all three periodic axes",
    ):
        scale_periodic_configuration(
            configuration,
            linear_scale=1.0,
        )


@pytest.mark.parametrize(
    ("linear_scale", "exception"),
    (
        (0.0, ValueError),
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("scale", TypeError),
    ),
)
def test_linear_scale_validation(
    linear_scale: object,
    exception: type[Exception],
) -> None:
    """Direct affine scaling requires a positive finite real factor."""

    with pytest.raises(exception):
        scale_periodic_configuration(
            _periodic_configuration(),
            linear_scale=linear_scale,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("current_pressure", "target_pressure", "exception"),
    (
        (float("inf"), 1.0, ValueError),
        (float("nan"), 1.0, ValueError),
        (1.0, float("inf"), ValueError),
        (1.0, float("nan"), ValueError),
        (True, 1.0, TypeError),
        (1.0, False, TypeError),
        ("pressure", 1.0, TypeError),
    ),
)
def test_pressure_validation(
    current_pressure: object,
    target_pressure: object,
    exception: type[Exception],
) -> None:
    """Pressure inputs must be finite real scalars."""

    with pytest.raises(exception):
        isotropic_barostat_scale(
            current_pressure=current_pressure,  # type: ignore[arg-type]
            target_pressure=target_pressure,  # type: ignore[arg-type]
            compressibility=0.1,
            time_step=0.5,
            coupling_time=1.0,
        )


@pytest.mark.parametrize(
    ("compressibility", "exception"),
    (
        (0.0, ValueError),
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("beta", TypeError),
    ),
)
def test_compressibility_validation(
    compressibility: object,
    exception: type[Exception],
) -> None:
    """Compressibility must be a positive finite real scalar."""

    with pytest.raises(exception):
        isotropic_barostat_scale(
            current_pressure=2.0,
            target_pressure=1.0,
            compressibility=compressibility,  # type: ignore[arg-type]
            time_step=0.5,
            coupling_time=1.0,
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
    """Barostat time step must be a positive finite real scalar."""

    with pytest.raises(exception):
        isotropic_barostat_scale(
            current_pressure=2.0,
            target_pressure=1.0,
            compressibility=0.1,
            time_step=time_step,  # type: ignore[arg-type]
            coupling_time=1.0,
        )


@pytest.mark.parametrize(
    ("coupling_time", "exception"),
    (
        (0.0, ValueError),
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("tau", TypeError),
    ),
)
def test_coupling_time_validation(
    coupling_time: object,
    exception: type[Exception],
) -> None:
    """Pressure-coupling time must be a positive finite real scalar."""

    with pytest.raises(exception):
        isotropic_barostat_scale(
            current_pressure=2.0,
            target_pressure=1.0,
            compressibility=0.1,
            time_step=0.5,
            coupling_time=coupling_time,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("current_pressure", "target_pressure"),
    (
        (0.0, 1.0),
        (0.0, 2.0),
    ),
)
def test_nonpositive_volume_scale_is_rejected(
    current_pressure: float,
    target_pressure: float,
) -> None:
    """Pressure coupling must reject zero or negative resulting cell volume."""

    with pytest.raises(
        ValueError,
        match="volume scale must be greater than zero",
    ):
        isotropic_barostat_scale(
            current_pressure=current_pressure,
            target_pressure=target_pressure,
            compressibility=1.0,
            time_step=1.0,
            coupling_time=1.0,
        )


def test_apply_barostat_rejects_non_md_state() -> None:
    """The state-level operator must require MolecularDynamicsState."""

    with pytest.raises(
        TypeError,
        match="state must be a MolecularDynamicsState instance",
    ):
        apply_isotropic_barostat(
            None,  # type: ignore[arg-type]
            current_pressure=2.0,
            target_pressure=1.0,
            compressibility=0.1,
            time_step=0.5,
            coupling_time=1.0,
        )
