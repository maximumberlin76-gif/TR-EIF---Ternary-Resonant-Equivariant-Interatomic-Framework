"""Replica-count and observation-duration sensitivity of FLiBe MD statistics.

Each run supplies a complete aligned thermodynamic trace and registered
identifiers for its initial condition and potential-parameter source. Prefix
windows are evaluated with the established non-overlapping block operator.
Equal-size windows receive equal weight across distinct trajectory runs.

The between-trajectory standard error is the sample standard deviation of
trajectory means divided by the square root of the trajectory count. The
initial-condition fingerprints establish distinct registered inputs; the
statistical independence and equilibrium assumptions remain subjects of
separate physical qualification. Block correlations and within-run drifts
are retained alongside the between-run estimates.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import fsum, isclose, isfinite, sqrt
from statistics import median, stdev

from .trajectory_block_statistics import (
    FLiBeBlockObservable,
    FLiBeTrajectoryBlockStatistics,
    evaluate_flibe_trajectory_block_statistics,
)
from .trajectory_frame_thermodynamics import FLiBeFrameThermodynamicState
from .trajectory_pressure import FLiBeVelocityFrame
from .units import ParameterProvenance

_METHOD_ID = "tr-eif.flibe.trajectory-replica-duration-convergence.v1"
_UNITS = (
    ("temperature", "K"),
    ("pressure", "Pa"),
    ("density", "kg/m^3"),
)


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _digest(value: str, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(
        symbol not in "0123456789abcdef" for symbol in value
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest.")
    return value


def _integer(value: int, name: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}.")
    return value


def _real(value: float, name: str, *, nonnegative: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or (nonnegative and number < 0.0):
        raise ValueError(f"{name} must be finite and satisfy its sign constraint.")
    return number


@dataclass(frozen=True, slots=True)
class FLiBeReplicaThermodynamicTrace:
    """One run with a source fingerprint and registered initialization digest."""

    replica_id: str
    initial_condition_sha256: str
    parameter_source_sha256: str
    thermodynamics: FLiBeFrameThermodynamicState

    def __post_init__(self) -> None:
        _identifier(self.replica_id, "replica_id")
        _digest(self.initial_condition_sha256, "initial_condition_sha256")
        _digest(self.parameter_source_sha256, "parameter_source_sha256")
        if not isinstance(self.thermodynamics, FLiBeFrameThermodynamicState):
            raise TypeError(
                "thermodynamics must be FLiBeFrameThermodynamicState."
            )


@dataclass(frozen=True, slots=True)
class FLiBeReplicaObservableConvergence:
    """Within-run diagnostics and between-run statistics for one observable."""

    unit: str
    trajectory_means: tuple[float, ...]
    mean_of_trajectory_means: float
    between_trajectory_sample_sd: float
    between_trajectory_standard_error: float
    median_within_trajectory_block_se: float
    maximum_absolute_half_window_shift: float
    maximum_absolute_lag_one_block_correlation: float | None
    undefined_lag_one_correlation_count: int
    mean_change_from_previous_duration: float | None

    def __post_init__(self) -> None:
        if self.unit not in {unit for _, unit in _UNITS}:
            raise ValueError("unit must be K, Pa, or kg/m^3.")
        if not isinstance(self.trajectory_means, tuple) or len(self.trajectory_means) < 2:
            raise ValueError(
                "trajectory_means must include at least two trajectories."
            )
        for value in self.trajectory_means:
            _real(value, "trajectory mean")
        for name in (
            "mean_of_trajectory_means",
            "between_trajectory_sample_sd",
            "between_trajectory_standard_error",
            "median_within_trajectory_block_se",
            "maximum_absolute_half_window_shift",
        ):
            _real(
                getattr(self, name),
                name,
                nonnegative=name not in {"mean_of_trajectory_means"},
            )
        if self.maximum_absolute_lag_one_block_correlation is not None:
            correlation = _real(
                self.maximum_absolute_lag_one_block_correlation,
                "maximum_absolute_lag_one_block_correlation",
                nonnegative=True,
            )
            if correlation > 1.0:
                raise ValueError(
                    "lag-one correlation magnitude must not exceed one."
                )
        count = _integer(
            self.undefined_lag_one_correlation_count,
            "undefined_lag_one_correlation_count",
            0,
        )
        if count > len(self.trajectory_means):
            raise ValueError(
                "undefined correlation count exceeds the run count."
            )
        if self.mean_change_from_previous_duration is not None:
            _real(
                self.mean_change_from_previous_duration,
                "mean_change_from_previous_duration",
            )


@dataclass(frozen=True, slots=True)
class FLiBeReplicaConvergencePoint:
    """Equal-duration cumulative run ensemble and its three SI observables."""

    retained_samples_per_trajectory: int
    observed_duration_s: float
    replica_count: int
    trajectory_ids: tuple[str, ...]
    initial_condition_sha256: tuple[str, ...]
    temperature: FLiBeReplicaObservableConvergence
    pressure: FLiBeReplicaObservableConvergence
    density: FLiBeReplicaObservableConvergence

    def __post_init__(self) -> None:
        _integer(
            self.retained_samples_per_trajectory,
            "retained_samples_per_trajectory",
            2,
        )
        _real(
            self.observed_duration_s,
            "observed_duration_s",
            nonnegative=True,
        )
        count = _integer(self.replica_count, "replica_count", 2)
        if len(self.trajectory_ids) != count or len(set(self.trajectory_ids)) != count:
            raise ValueError(
                "trajectory_ids must be unique and match replica_count."
            )
        if (
            len(self.initial_condition_sha256) != count
            or len(set(self.initial_condition_sha256)) != count
        ):
            raise ValueError(
                "initialization fingerprints must be unique and match replica_count."
            )
        for key in self.trajectory_ids:
            _identifier(key, "trajectory_id")
        for key in self.initial_condition_sha256:
            _digest(key, "initial_condition_sha256")
        for name, unit in _UNITS:
            value = getattr(self, name)
            if (
                not isinstance(value, FLiBeReplicaObservableConvergence)
                or value.unit != unit
            ):
                raise ValueError(
                    f"{name} must retain SI unit {unit}."
                )
            if len(value.trajectory_means) != count:
                raise ValueError(
                    f"{name} must include every trajectory mean."
                )


@dataclass(frozen=True, slots=True)
class FLiBeTrajectoryReplicaConvergence:
    """Duration-by-replica-count matrix with aligned provenance and controls."""

    method_id: str
    model_id: str
    parameter_source_sha256: str
    provenance: ParameterProvenance
    velocity_frame: FLiBeVelocityFrame
    physical_state_id: str
    physical_state_method_id: str
    sampling_interval_s: float
    discarded_initial_samples: int
    block_size_samples: int
    retained_sample_lengths: tuple[int, ...]
    replica_ids: tuple[str, ...]
    points: tuple[FLiBeReplicaConvergencePoint, ...]

    def __post_init__(self) -> None:
        if self.method_id != _METHOD_ID:
            raise ValueError(
                "method_id must identify the replica-duration estimator."
            )
        _identifier(self.model_id, "model_id")
        _digest(self.parameter_source_sha256, "parameter_source_sha256")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        if not isinstance(self.velocity_frame, FLiBeVelocityFrame):
            raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
        _identifier(self.physical_state_id, "physical_state_id")
        _identifier(self.physical_state_method_id, "physical_state_method_id")
        if _real(
            self.sampling_interval_s,
            "sampling_interval_s",
            nonnegative=True,
        ) == 0.0:
            raise ValueError("sampling_interval_s must be positive.")
        _integer(
            self.discarded_initial_samples,
            "discarded_initial_samples",
            0,
        )
        _integer(self.block_size_samples, "block_size_samples", 2)
        if (
            not isinstance(self.retained_sample_lengths, tuple)
            or not self.retained_sample_lengths
        ):
            raise ValueError(
                "retained_sample_lengths must contain a duration grid."
            )
        if (
            not isinstance(self.replica_ids, tuple)
            or len(set(self.replica_ids)) < 2
        ):
            raise ValueError(
                "replica_ids must contain at least two unique identifiers."
            )
        if len(self.points) != (
            len(self.retained_sample_lengths) * (len(self.replica_ids) - 1)
        ):
            raise ValueError(
                "points must cover the duration-by-replica-count matrix."
            )

    @property
    def trajectory_count(self) -> int:
        return len(self.replica_ids)

    def at(self, samples: int, replicas: int) -> FLiBeReplicaConvergencePoint:
        """Select the accumulated ensemble at a declared duration and size."""
        for point in self.points:
            if (
                point.retained_samples_per_trajectory == samples
                and point.replica_count == replicas
            ):
                return point
        raise ValueError(
            "requested duration/replica count is outside the declared grid."
        )


def _prefix_thermodynamics(
    source: FLiBeFrameThermodynamicState,
    last_exclusive: int,
) -> FLiBeFrameThermodynamicState:
    """Keep a consistent typed prefix of three aligned observation series."""
    pressure = source.pressure_trace
    density = pressure.density_trace
    subset_density = replace(
        density,
        samples=density.samples[:last_exclusive],
    )
    subset_pressure = replace(
        pressure,
        density_trace=subset_density,
        samples=pressure.samples[:last_exclusive],
    )
    return replace(
        source,
        pressure_trace=subset_pressure,
        samples=source.samples[:last_exclusive],
    )


def _summary(
    records: tuple[FLiBeTrajectoryBlockStatistics, ...],
    observable_name: str,
    previous_mean: float | None,
) -> FLiBeReplicaObservableConvergence:
    values: tuple[FLiBeBlockObservable, ...] = tuple(
        getattr(item, observable_name) for item in records
    )
    means = tuple(value.mean for value in values)
    center = fsum(means) / len(means)
    variance_sd = stdev(means)
    correlations = tuple(
        abs(value.lag_one_block_correlation)
        for value in values
        if value.lag_one_block_correlation is not None
    )
    return FLiBeReplicaObservableConvergence(
        unit=values[0].unit,
        trajectory_means=means,
        mean_of_trajectory_means=center,
        between_trajectory_sample_sd=variance_sd,
        between_trajectory_standard_error=variance_sd / sqrt(len(means)),
        median_within_trajectory_block_se=median(
            value.block_mean_standard_error for value in values
        ),
        maximum_absolute_half_window_shift=max(
            abs(value.second_half_minus_first_half) for value in values
        ),
        maximum_absolute_lag_one_block_correlation=(
            max(correlations) if correlations else None
        ),
        undefined_lag_one_correlation_count=len(values) - len(correlations),
        mean_change_from_previous_duration=(
            None if previous_mean is None else center - previous_mean
        ),
    )


def evaluate_flibe_trajectory_replica_convergence(
    traces: tuple[FLiBeReplicaThermodynamicTrace, ...],
    *,
    block_size_samples: int,
    retained_sample_lengths: tuple[int, ...],
    discarded_initial_samples: int = 0,
) -> FLiBeTrajectoryReplicaConvergence:
    """Compute nested duration and cumulative-replica statistics.

    Each prefix is taken after a predeclared discard. Durations are specified
    in retained frame counts, strictly increase, and contain complete blocks.
    All replicas must have identical potential source, chemical inventory,
    physical-state designation, velocity frame, and sampled time spacing.
    The output describes sensitivity to run count and duration without
    assigning a thermodynamic equilibrium label.
    """
    if (
        not isinstance(traces, tuple)
        or len(traces) < 2
        or any(
            not isinstance(item, FLiBeReplicaThermodynamicTrace)
            for item in traces
        )
    ):
        raise TypeError(
            "traces must contain at least two typed replica records."
        )

    block_size = _integer(
        block_size_samples,
        "block_size_samples",
        2,
    )
    discarded = _integer(
        discarded_initial_samples,
        "discarded_initial_samples",
        0,
    )

    if (
        not isinstance(retained_sample_lengths, tuple)
        or not retained_sample_lengths
    ):
        raise ValueError(
            "retained_sample_lengths must be a nonempty tuple."
        )

    previous = 0
    for value in retained_sample_lengths:
        length = _integer(
            value,
            "retained sample length",
            2 * block_size,
        )
        if length <= previous or length % block_size:
            raise ValueError(
                "sample lengths must increase and contain complete blocks."
            )
        previous = length

    final_length = discarded + retained_sample_lengths[-1]

    replica_ids = tuple(item.replica_id for item in traces)
    trajectory_ids = tuple(
        item.thermodynamics.pressure_trace.density_trace.trajectory_id
        for item in traces
    )
    fingerprints = tuple(
        item.initial_condition_sha256 for item in traces
    )

    if any(
        len(set(items)) != len(items)
        for items in (replica_ids, trajectory_ids, fingerprints)
    ):
        raise ValueError(
            "replica, trajectory and initialization identifiers must be unique."
        )

    base = traces[0].thermodynamics
    pressure0 = base.pressure_trace
    density0 = pressure0.density_trace
    source_digest = traces[0].parameter_source_sha256
    sampled_interval_s = None

    for record in traces:
        current = record.thermodynamics
        pressure = current.pressure_trace
        density = pressure.density_trace

        if record.parameter_source_sha256 != source_digest:
            raise ValueError(
                "replica parameter source fingerprints differ."
            )

        if (
            density.model_id != density0.model_id
            or density.provenance != density0.provenance
            or density.composition != density0.composition
            or density.atom_count != density0.atom_count
            or density.total_mass_kg != density0.total_mass_kg
            or density.mass_unit_to_kg != density0.mass_unit_to_kg
            or density.coordinate_unit_to_meter != density0.coordinate_unit_to_meter
            or pressure.velocity_frame != pressure0.velocity_frame
            or pressure.stress_method_id != pressure0.stress_method_id
            or pressure.source_id != pressure0.source_id
            or pressure.provenance != pressure0.provenance
            or pressure.time_unit_to_second != pressure0.time_unit_to_second
            or current.degrees_of_freedom != base.degrees_of_freedom
            or current.physical_state_id != base.physical_state_id
            or current.physical_state_method_id != base.physical_state_method_id
        ):
            raise ValueError(
                "replica physical coordinates or observation methods differ."
            )

        if len(current.samples) < final_length:
            raise ValueError(
                "a replica lacks the required observation duration."
            )

        complete_prefix = _prefix_thermodynamics(
            current,
            final_length,
        )
        validated = evaluate_flibe_trajectory_block_statistics(
            complete_prefix,
            block_size_samples=block_size,
            discarded_initial_samples=discarded,
        )

        if sampled_interval_s is None:
            sampled_interval_s = validated.sampling_interval_s
        elif not isclose(
            validated.sampling_interval_s,
            sampled_interval_s,
            rel_tol=1.0e-12,
            abs_tol=0.0,
        ):
            raise ValueError(
                "replica observation sampling intervals differ."
            )

    assert sampled_interval_s is not None

    prior_by_count_and_observable: dict[tuple[int, str], float] = {}
    points: list[FLiBeReplicaConvergencePoint] = []

    for length in retained_sample_lengths:
        statistics = tuple(
            evaluate_flibe_trajectory_block_statistics(
                _prefix_thermodynamics(
                    record.thermodynamics,
                    discarded + length,
                ),
                block_size_samples=block_size,
                discarded_initial_samples=discarded,
            )
            for record in traces
        )

        for replica_count in range(2, len(traces) + 1):
            selected = statistics[:replica_count]
            fields = {}

            for name, _ in _UNITS:
                key = (replica_count, name)
                summary = _summary(
                    selected,
                    name,
                    prior_by_count_and_observable.get(key),
                )
                prior_by_count_and_observable[key] = (
                    summary.mean_of_trajectory_means
                )
                fields[name] = summary

            points.append(
                FLiBeReplicaConvergencePoint(
                    retained_samples_per_trajectory=length,
                    observed_duration_s=(
                        (length - 1) * sampled_interval_s
                    ),
                    replica_count=replica_count,
                    trajectory_ids=trajectory_ids[:replica_count],
                    initial_condition_sha256=fingerprints[:replica_count],
                    **fields,
                )
            )

    return FLiBeTrajectoryReplicaConvergence(
        method_id=_METHOD_ID,
        model_id=density0.model_id,
        parameter_source_sha256=source_digest,
        provenance=density0.provenance,
        velocity_frame=pressure0.velocity_frame,
        physical_state_id=base.physical_state_id,
        physical_state_method_id=base.physical_state_method_id,
        sampling_interval_s=sampled_interval_s,
        discarded_initial_samples=discarded,
        block_size_samples=block_size,
        retained_sample_lengths=retained_sample_lengths,
        replica_ids=replica_ids,
        points=tuple(points),
    )
