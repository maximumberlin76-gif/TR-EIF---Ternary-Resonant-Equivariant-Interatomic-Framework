
"""Time-origin-averaged transport observables for periodic polarizable FLiBe MD.

For each lag k, the declared origin set is

    O_k = {first + j * stride | first + j * stride + k < stop}.

Species-resolved mean-squared displacement and velocity autocorrelation
are averaged over all atoms of that species and all origins in O_k.
The output preserves the origin population for every lag and uses SI units.
Both laboratory and mass-weighted center-of-mass reference frames are
supported. The periodic trajectory is validated against the continuous
velocity-Verlet updates before its Cartesian coordinates are used.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from .periodic_polarizable_md import FLiBePeriodicMDRun
from .periodic_transport import (
    FLiBePeriodicTransportResult,
    FLiBeSpeciesTransportSeries,
    FLiBeTransportFrame,
    evaluate_flibe_periodic_transport,
)

_SPECIES = ("Li", "Be", "F")
_ZERO = (0.0, 0.0, 0.0)
_METHOD_ID = "tr-eif.flibe.periodic-multi-origin-msd-vacf.v1"


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    return value


def _finite_positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(f"{name} must be a real number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _mass_mean(vectors, masses) -> tuple[float, float, float]:
    total = fsum(masses)
    return tuple(
        fsum(mass * vector[axis] for mass, vector in zip(masses, vectors, strict=True))
        / total
        for axis in range(3)
    )  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class FLiBePeriodicMultiOriginResult:
    """Species transport series with explicit time-origin sampling metadata.

    ``observables.times_s`` contains nonnegative lag times, not absolute MD
    times. ``origin_stop_index`` is exclusive. Each lag has a distinct number
    of contributing origins recorded in ``origin_count_by_lag``.
    """

    observables: FLiBePeriodicTransportResult
    method_id: str
    origin_start_index: int
    origin_stop_index: int
    origin_stride: int
    origin_count_by_lag: tuple[int, ...]
    sampling_interval_s: float

    def __post_init__(self) -> None:
        if not isinstance(self.observables, FLiBePeriodicTransportResult):
            raise TypeError("observables must be FLiBePeriodicTransportResult.")
        if self.method_id != _METHOD_ID:
            raise ValueError("method_id must identify the multi-origin estimator.")
        start = self.origin_start_index
        stop = self.origin_stop_index
        if isinstance(start, bool) or not isinstance(start, int) or start < 0:
            raise ValueError("origin_start_index must be a nonnegative integer.")
        _positive_integer(stop, "origin_stop_index")
        stride = _positive_integer(self.origin_stride, "origin_stride")
        interval = _finite_positive(self.sampling_interval_s, "sampling_interval_s")
        if stop - start < 2:
            raise ValueError("the selected trajectory window needs two states.")
        counts = self.origin_count_by_lag
        if not isinstance(counts, tuple) or len(counts) != self.observables.sample_count:
            raise ValueError("origin counts must align with the lag-time series.")
        if len(counts) > stop - start:
            raise ValueError("the lag series exceeds the selected state window.")
        for lag, actual in enumerate(counts):
            expected = (stop - start - lag - 1) // stride + 1
            if isinstance(actual, bool) or not isinstance(actual, int) or actual != expected:
                raise ValueError("origin count must match the declared origin set.")
            target_time = lag * interval
            if not isclose(self.observables.times_s[lag], target_time,
                           rel_tol=1.0e-12, abs_tol=0.0):
                raise ValueError("lag times must follow the uniform sampling interval.")

    @property
    def trajectory_id(self) -> str:
        return self.observables.trajectory_id

    @property
    def frame(self) -> FLiBeTransportFrame:
        return self.observables.frame

    @property
    def lag_times_s(self) -> tuple[float, ...]:
        return self.observables.times_s

    @property
    def species_series(self) -> tuple[FLiBeSpeciesTransportSeries, ...]:
        return self.observables.species_series

    def for_species(self, symbol: str) -> FLiBeSpeciesTransportSeries:
        """Return a named species' time-origin-averaged MSD and VACF."""
        return self.observables.for_species(symbol)


def evaluate_flibe_periodic_multi_origin_transport(
    run: FLiBePeriodicMDRun,
    *,
    trajectory_id: str,
    frame: FLiBeTransportFrame = FLiBeTransportFrame.CENTER_OF_MASS,
    origin_start_index: int = 0,
    origin_stop_index: int | None = None,
    origin_stride: int = 1,
    maximum_lag_steps: int | None = None,
    position_tolerance_code: float = 1.0e-10,
    velocity_tolerance_code: float = 1.0e-10,
) -> FLiBePeriodicMultiOriginResult:
    """Compute species-resolved MSD and VACF averaged over selected origins.

    The selected state window is ``[origin_start_index, origin_stop_index)``.
    For every lag, all admissible origins in that window are sampled at the
    given stride. The estimator requires uniformly spaced mechanical states.
    Velocity-Verlet consistency, unwrapped coordinates, fixed periodic cell,
    species order, and masses are verified through the existing FLiBe operator.

    MSD uses continuous Cartesian displacements. In the center-of-mass frame
    each displacement subtracts the mass-weighted displacement over the same
    time interval; both endpoint velocities subtract their instantaneous
    mass-weighted velocities. Output units are m² and m²/s², respectively.
    """

    # The existing operator enforces the complete periodic Verlet trajectory
    # contract, frame contract, source identity, and identifier validity.
    validated = evaluate_flibe_periodic_transport(
        run,
        trajectory_id=trajectory_id,
        frame=frame,
        position_tolerance_code=position_tolerance_code,
        velocity_tolerance_code=velocity_tolerance_code,
    )
    states = run.trajectory.states
    count = len(states)
    if isinstance(origin_start_index, bool) or not isinstance(origin_start_index, int):
        raise TypeError("origin_start_index must be an integer.")
    if origin_start_index < 0 or origin_start_index >= count - 1:
        raise ValueError("origin_start_index must leave at least two states.")
    if origin_stop_index is None:
        stop = count
    else:
        stop = _positive_integer(origin_stop_index, "origin_stop_index")
    if stop > count or stop - origin_start_index < 2:
        raise ValueError("origin_stop_index must select at least two states within the run.")
    stride = _positive_integer(origin_stride, "origin_stride")
    available_lags = stop - origin_start_index - 1
    if maximum_lag_steps is None:
        lags = available_lags
    else:
        lags = _positive_integer(maximum_lag_steps, "maximum_lag_steps")
        if lags > available_lags:
            raise ValueError("maximum_lag_steps exceeds the selected state window.")

    # The clock is examined in MD code units before conversion to SI. A
    # uniform mechanical schedule gives one physical lag interval for all
    # time origins; otherwise an index-based average mixes distinct lag times.
    start_time = states[origin_start_index].time
    dt_code = _finite_positive(
        (states[stop - 1].time - start_time) / available_lags,
        "sampling interval in code units",
    )
    for index in range(origin_start_index, stop):
        elapsed = states[index].time - start_time
        if not isclose(elapsed, (index - origin_start_index) * dt_code,
                       rel_tol=1.0e-9, abs_tol=1.0e-12 * dt_code):
            raise ValueError("multi-origin averaging requires uniformly sampled MD states.")
    dt_s = _finite_positive(
        dt_code * run.units.time_unit_to_second, "sampling interval in seconds"
    )
    length_sq = run.units.coordinate_unit_to_meter**2
    speed_sq = (run.units.coordinate_unit_to_meter / run.units.time_unit_to_second)**2
    masses = states[0].masses
    species = states[0].configuration.species
    members = {
        symbol: tuple(i for i, entry in enumerate(species) if entry == symbol)
        for symbol in _SPECIES
    }
    velocities_com = (
        tuple(_mass_mean(state.velocities, masses) for state in states)
        if frame is FLiBeTransportFrame.CENTER_OF_MASS
        else tuple(_ZERO for _ in states)
    )

    msd = {symbol: [] for symbol in _SPECIES}
    vacf = {symbol: [] for symbol in _SPECIES}
    origin_counts: list[int] = []

    for lag in range(lags + 1):
        origins = range(origin_start_index, stop - lag, stride)
        selected_count = len(origins)
        origin_counts.append(selected_count)
        accumulated_msd = {symbol: [] for symbol in _SPECIES}
        accumulated_vacf = {symbol: [] for symbol in _SPECIES}
        for origin in origins:
            first = states[origin]
            final = states[origin + lag]
            differences = tuple(
                tuple(end[axis] - begin[axis] for axis in range(3))
                for begin, end in zip(
                    first.configuration.positions, final.configuration.positions, strict=True
                )
            )
            shift = (
                _mass_mean(differences, masses)
                if frame is FLiBeTransportFrame.CENTER_OF_MASS
                else _ZERO
            )
            first_center = velocities_com[origin]
            final_center = velocities_com[origin + lag]
            for symbol in _SPECIES:
                for atom in members[symbol]:
                    accumulated_msd[symbol].append(fsum(
                        (differences[atom][axis] - shift[axis])**2
                        for axis in range(3)
                    ))
                    accumulated_vacf[symbol].append(fsum(
                        (first.velocities[atom][axis] - first_center[axis])
                        * (final.velocities[atom][axis] - final_center[axis])
                        for axis in range(3)
                    ))
        for symbol in _SPECIES:
            divisor = selected_count * len(members[symbol])
            msd[symbol].append(fsum(accumulated_msd[symbol]) * length_sq / divisor)
            vacf[symbol].append(fsum(accumulated_vacf[symbol]) * speed_sq / divisor)

    observables = FLiBePeriodicTransportResult(
        trajectory_id=validated.trajectory_id,
        model_id=validated.model_id,
        source_file_sha256=validated.source_file_sha256,
        source_doi=validated.source_doi,
        units_source_id=validated.units_source_id,
        frame=frame,
        times_s=tuple(lag * dt_s for lag in range(lags + 1)),
        species_series=tuple(
            FLiBeSpeciesTransportSeries(
                species=symbol,
                atom_count=len(members[symbol]),
                mean_squared_displacement_m2=tuple(msd[symbol]),
                velocity_autocorrelation_m2_per_s2=tuple(vacf[symbol]),
            )
            for symbol in _SPECIES
        ),
    )
    return FLiBePeriodicMultiOriginResult(
        observables=observables,
        method_id=_METHOD_ID,
        origin_start_index=origin_start_index,
        origin_stop_index=stop,
        origin_stride=stride,
        origin_count_by_lag=tuple(origin_counts),
        sampling_interval_s=dt_s,
    )
