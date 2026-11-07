"""Block statistics of aligned FLiBe MD temperature, pressure and density.

Complete, non-overlapping blocks are formed after a declared initial discard.
The selected frame sequence must have uniform, increasing MD time and step
coordinates. Each observable retains its SI unit, block means, sample
standard deviation, and standard error estimated from block means.

The block-mean standard error uses the sample variance of non-overlapping
block means divided by the block count. Its statistical interpretation
assumes sufficiently weak correlation between blocks. Lag-one correlation
and first/second-half differences are retained as sampling diagnostics.
Signed pressure and physical-state provenance are preserved throughout.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite, sqrt

from .trajectory_frame_thermodynamics import FLiBeFrameThermodynamicState
from .trajectory_pressure import FLiBeVelocityFrame
from .units import ParameterProvenance


def _integer(value: int, name: str, *, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}.")
    return value


def _real(value: float, name: str, *, nonnegative: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")
    result = float(value)
    if not isfinite(result) or (nonnegative and result < 0.0):
        raise ValueError(f"{name} must be finite and satisfy its sign constraint.")
    return result


def _mean(values: tuple[float, ...]) -> float:
    return fsum(values) / len(values)


@dataclass(frozen=True, slots=True)
class FLiBeBlockObservable:
    """Mean, fluctuations and block diagnostics for one physical observable."""

    unit: str
    mean: float
    sample_standard_deviation: float
    block_means: tuple[float, ...]
    block_mean_standard_error: float
    second_half_minus_first_half: float
    lag_one_block_correlation: float | None

    def __post_init__(self) -> None:
        if self.unit not in ("K", "Pa", "kg/m^3"):
            raise ValueError("unit must be K, Pa, or kg/m^3.")
        _real(self.mean, "mean")
        _real(self.sample_standard_deviation, "sample_standard_deviation", nonnegative=True)
        _real(self.block_mean_standard_error, "block_mean_standard_error", nonnegative=True)
        _real(self.second_half_minus_first_half, "second_half_minus_first_half")
        if not isinstance(self.block_means, tuple) or len(self.block_means) < 2:
            raise ValueError("block_means must contain at least two blocks.")
        for value in self.block_means:
            _real(value, "block mean")
        if self.lag_one_block_correlation is not None:
            correlation = _real(self.lag_one_block_correlation, "lag_one_block_correlation")
            if not -1.0 <= correlation <= 1.0:
                raise ValueError("lag_one_block_correlation must lie in [-1, 1].")


@dataclass(frozen=True, slots=True)
class FLiBeThermodynamicBlock:
    """Time and source indices of a contiguous block and its three means."""

    block_index: int
    first_state_index: int
    last_state_index: int
    first_time_s: float
    last_time_s: float
    mean_temperature_k: float
    mean_signed_pressure_pa: float
    mean_density_kg_m3: float

    def __post_init__(self) -> None:
        _integer(self.block_index, "block_index", minimum=0)
        first = _integer(self.first_state_index, "first_state_index", minimum=0)
        last = _integer(self.last_state_index, "last_state_index", minimum=first)
        first_time = _real(self.first_time_s, "first_time_s", nonnegative=True)
        last_time = _real(self.last_time_s, "last_time_s", nonnegative=True)
        if last_time < first_time:
            raise ValueError("block time bounds must be ordered.")
        _real(self.mean_temperature_k, "mean_temperature_k", nonnegative=True)
        _real(self.mean_signed_pressure_pa, "mean_signed_pressure_pa")
        _real(self.mean_density_kg_m3, "mean_density_kg_m3", nonnegative=True)


@dataclass(frozen=True, slots=True)
class FLiBeTrajectoryBlockStatistics:
    """Block-estimated observables and explicit equilibration/sampling scope."""

    model_id: str
    trajectory_id: str
    provenance: ParameterProvenance
    velocity_frame: FLiBeVelocityFrame
    stress_method_id: str
    pressure_source_id: str
    pressure_provenance: ParameterProvenance
    temperature_degrees_of_freedom: int
    physical_state_id: str
    physical_state_method_id: str
    discarded_initial_samples: int
    discarded_tail_samples: int
    block_size_samples: int
    sampling_interval_s: float
    blocks: tuple[FLiBeThermodynamicBlock, ...]
    temperature: FLiBeBlockObservable
    pressure: FLiBeBlockObservable
    density: FLiBeBlockObservable

    def __post_init__(self) -> None:
        for name in (
            "model_id", "trajectory_id", "stress_method_id", "pressure_source_id",
            "physical_state_id", "physical_state_method_id",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError(f"{name} must be a nonempty trimmed identifier.")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        if not isinstance(self.velocity_frame, FLiBeVelocityFrame):
            raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
        if not isinstance(self.pressure_provenance, ParameterProvenance):
            raise TypeError("pressure_provenance must be ParameterProvenance.")
        _integer(self.temperature_degrees_of_freedom, "temperature_degrees_of_freedom", minimum=1)
        _integer(self.discarded_initial_samples, "discarded_initial_samples", minimum=0)
        _integer(self.discarded_tail_samples, "discarded_tail_samples", minimum=0)
        block_size = _integer(self.block_size_samples, "block_size_samples", minimum=1)
        interval = _real(self.sampling_interval_s, "sampling_interval_s", nonnegative=True)
        if interval <= 0.0:
            raise ValueError("sampling_interval_s must be positive.")
        if not isinstance(self.blocks, tuple) or len(self.blocks) < 2:
            raise ValueError("at least two complete blocks are required.")
        if any(not isinstance(item, FLiBeThermodynamicBlock) or item.block_index != index
               or item.last_state_index < item.first_state_index
               for index, item in enumerate(self.blocks)):
            raise ValueError("blocks must be correctly indexed and typed.")
        for name, unit in (("temperature", "K"), ("pressure", "Pa"), ("density", "kg/m^3")):
            value = getattr(self, name)
            if not isinstance(value, FLiBeBlockObservable) or value.unit != unit:
                raise ValueError(f"{name} must have the corresponding SI unit.")
            if len(value.block_means) != len(self.blocks):
                raise ValueError(f"{name} must align with all blocks.")
        if any(self.blocks[i + 1].first_state_index <= self.blocks[i].last_state_index
               for i in range(len(self.blocks) - 1)):
            raise ValueError("block state indices must increase without overlap.")

    @property
    def selected_sample_count(self) -> int:
        """Number of retained frames included in complete blocks."""
        return len(self.blocks) * self.block_size_samples

    @property
    def block_count(self) -> int:
        return len(self.blocks)


def _correlation(block_means: tuple[float, ...]) -> float | None:
    if len(block_means) < 3:
        return None
    left, right = block_means[:-1], block_means[1:]
    left_mean, right_mean = _mean(left), _mean(right)
    left_var = fsum((value - left_mean) ** 2 for value in left)
    right_var = fsum((value - right_mean) ** 2 for value in right)
    denominator = sqrt(left_var * right_var)
    if denominator == 0.0:
        return None
    value = fsum(
        (a - left_mean) * (b - right_mean)
        for a, b in zip(left, right, strict=True)
    ) / denominator
    return max(-1.0, min(1.0, value))


def _observable(values: tuple[float, ...], block_size: int, unit: str) -> FLiBeBlockObservable:
    means = tuple(
        _mean(values[start:start + block_size])
        for start in range(0, len(values), block_size)
    )
    grand_mean = _mean(values)
    blocks_mean = _mean(means)
    sample_sd = sqrt(fsum((value - grand_mean) ** 2 for value in values) / (len(values) - 1))
    block_se = sqrt(fsum((value - blocks_mean) ** 2 for value in means) /
                    ((len(means) - 1) * len(means)))
    midpoint = len(means) // 2
    return FLiBeBlockObservable(
        unit=unit,
        mean=grand_mean,
        sample_standard_deviation=sample_sd,
        block_means=means,
        block_mean_standard_error=block_se,
        second_half_minus_first_half=_mean(means[midpoint:]) - _mean(means[:midpoint]),
        lag_one_block_correlation=_correlation(means),
    )


def evaluate_flibe_trajectory_block_statistics(
    thermodynamics: FLiBeFrameThermodynamicState,
    *,
    block_size_samples: int,
    discarded_initial_samples: int = 0,
    discard_incomplete_tail: bool = False,
) -> FLiBeTrajectoryBlockStatistics:
    """Aggregate aligned MD observables into complete non-overlapping blocks.

    The declared discarded initial samples define an analysis window, not an
    inferred equilibration point. Incomplete trailing frames are rejected
    unless discard_incomplete_tail is explicitly enabled. Block standard
    errors and half-window differences remain numerical sampling diagnostics.
    """
    if not isinstance(thermodynamics, FLiBeFrameThermodynamicState):
        raise TypeError("thermodynamics must be FLiBeFrameThermodynamicState.")
    size = _integer(block_size_samples, "block_size_samples", minimum=2)
    discard = _integer(discarded_initial_samples, "discarded_initial_samples", minimum=0)
    if not isinstance(discard_incomplete_tail, bool):
        raise TypeError("discard_incomplete_tail must be a bool.")

    pressure = thermodynamics.pressure_trace
    density = pressure.density_trace
    sample_count = len(thermodynamics.samples)
    if discard >= sample_count:
        raise ValueError("discarded_initial_samples exceeds the available frames.")
    available = sample_count - discard
    complete, tail = divmod(available, size)
    if complete < 2:
        raise ValueError("at least two complete sampling blocks are required.")
    if tail and not discard_incomplete_tail:
        raise ValueError("incomplete trailing block requires explicit discard.")
    stop = discard + complete * size
    selected_t = thermodynamics.samples[discard:stop]
    selected_p = pressure.samples[discard:stop]
    selected_r = density.samples[discard:stop]

    # Uniform physical sampling is necessary for equal-weight frame averages
    # and the interpretation of contiguous block means as time averages.
    indices = tuple(item.state_index for item in selected_t)
    steps = tuple(item.md_step for item in selected_t)
    times = tuple(item.md_time for item in selected_t)
    index_delta = indices[1] - indices[0]
    step_delta = steps[1] - steps[0]
    time_delta = times[1] - times[0]
    if index_delta <= 0 or step_delta <= 0 or not isfinite(time_delta) or time_delta <= 0.0:
        raise ValueError("selected sampling times and steps must increase.")
    for index, (thermal, press, rho) in enumerate(zip(
        selected_t, selected_p, selected_r, strict=True
    )):
        if (thermal.state_index, thermal.md_step, thermal.md_time) != (
            press.state_index, press.md_step, press.md_time
        ) or (thermal.state_index, thermal.md_step, thermal.md_time) != (
            rho.state_index, rho.md_step, rho.md_time
        ):
            raise ValueError("temperature, pressure and density frame indices differ.")
        if thermal.state_index != indices[0] + index * index_delta or (
            thermal.md_step != steps[0] + index * step_delta
        ) or not isclose(
            thermal.md_time, times[0] + index * time_delta, rel_tol=1.0e-10,
            abs_tol=1.0e-12 * time_delta,
        ):
            raise ValueError("selected MD observations require uniform sampling.")
        if not isclose(rho.density_kg_m3 * rho.cell_volume_m3,
                       density.total_mass_kg, rel_tol=1.0e-12, abs_tol=0.0):
            raise ValueError("density does not agree with mass and cell volume.")
        tensor_pressure = fsum(press.pressure_tensor_pa[axis][axis] for axis in range(3)) / 3.0
        if not isclose(press.scalar_pressure_pa, tensor_pressure, rel_tol=1.0e-12, abs_tol=1.0e-6):
            raise ValueError("signed pressure differs from pressure tensor trace.")
        if not isclose(
            thermal.kinetic_pressure_pa,
            fsum(press.kinetic_tensor_pa[axis][axis] for axis in range(3)) / 3.0,
            rel_tol=1.0e-12, abs_tol=1.0e-6,
        ):
            raise ValueError("kinetic temperature/pressure frames differ.")

    temperatures = tuple(item.kinetic_temperature_k for item in selected_t)
    pressures = tuple(item.scalar_pressure_pa for item in selected_p)
    densities = tuple(item.density_kg_m3 for item in selected_r)
    time_scale = pressure.time_unit_to_second
    blocks: list[FLiBeThermodynamicBlock] = []
    for block_index in range(complete):
        start = block_index * size
        end = start + size
        blocks.append(FLiBeThermodynamicBlock(
            block_index=block_index,
            first_state_index=selected_t[start].state_index,
            last_state_index=selected_t[end - 1].state_index,
            first_time_s=selected_t[start].md_time * time_scale,
            last_time_s=selected_t[end - 1].md_time * time_scale,
            mean_temperature_k=_mean(temperatures[start:end]),
            mean_signed_pressure_pa=_mean(pressures[start:end]),
            mean_density_kg_m3=_mean(densities[start:end]),
        ))
    return FLiBeTrajectoryBlockStatistics(
        model_id=density.model_id,
        trajectory_id=density.trajectory_id,
        provenance=density.provenance,
        velocity_frame=thermodynamics.velocity_frame,
        stress_method_id=pressure.stress_method_id,
        pressure_source_id=pressure.source_id,
        pressure_provenance=pressure.provenance,
        temperature_degrees_of_freedom=thermodynamics.degrees_of_freedom,
        physical_state_id=thermodynamics.physical_state_id,
        physical_state_method_id=thermodynamics.physical_state_method_id,
        discarded_initial_samples=discard,
        discarded_tail_samples=tail,
        block_size_samples=size,
        sampling_interval_s=time_delta * time_scale,
        blocks=tuple(blocks),
        temperature=_observable(temperatures, size, "K"),
        pressure=_observable(pressures, size, "Pa"),
        density=_observable(densities, size, "kg/m^3"),
    )
