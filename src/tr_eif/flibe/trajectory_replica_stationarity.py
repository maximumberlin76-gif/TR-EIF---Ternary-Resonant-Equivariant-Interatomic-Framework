"""Sampling-stationarity diagnostics for registered periodic FLiBe MD replicas.

For each species-consistent and time-aligned ensemble, the operator reports
split-chain R-hat, a positive-pair autocorrelation-time estimate, its effective
sample count proxy, lag-one correlation, and within-trajectory half-window
shifts. The split diagnostic discards the central sample if the retained
length is odd. Distinct initial-condition SHA-256 records provide input
provenance; sampling diagnostics retain their numerical qualification scope.

The estimator uses original MD samples, with signed pressure in pascals,
kinetic temperature in kelvin, and density in kilograms per cubic meter.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite, sqrt
from statistics import mean, stdev

from .trajectory_replica_convergence import FLiBeReplicaThermodynamicTrace
from .trajectory_pressure import FLiBeVelocityFrame
from .units import ParameterProvenance

METHOD_ID = "tr-eif.flibe.replica-sampling-stationarity.v1"
_FIELDS = (
    ("temperature", "kinetic_temperature_k", "K"),
    ("pressure", "scalar_pressure_pa", "Pa"),
    ("density", "density_kg_m3", "kg/m^3"),
)


def _positive_real(value: float, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(f"{label} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{label} must be finite and positive.")
    return result


def _nonnegative_integer(value: int, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{label} must be an integer.")
    if value < 0:
        raise ValueError(f"{label} must be nonnegative.")
    return value


def _sample_variance(data: tuple[float, ...]) -> float:
    center = mean(data)
    return fsum((v - center) ** 2 for v in data) / (len(data) - 1)


def _pooled_lag_autocorrelation(
    chains: tuple[tuple[float, ...], ...], lag: int
) -> float | None:
    n = len(chains[0])
    variance = fsum(
        fsum((v - mean(row)) ** 2 for v in row) / n
        for row in chains
    ) / len(chains)
    if variance == 0.0:
        return None
    covariance = fsum(
        fsum((row[i] - center) * (row[i + lag] - center)
             for i in range(n - lag)) / (n - lag)
        for row in chains
        for center in (mean(row),)
    ) / len(chains)
    return max(-1.0, min(1.0, covariance / variance))


def _correlation_time(
    chains: tuple[tuple[float, ...], ...]
) -> tuple[float | None, float | None, float | None]:
    n = len(chains[0])
    coefficients = tuple(
        _pooled_lag_autocorrelation(chains, lag)
        for lag in range(1, n)
    )
    if coefficients[0] is None:
        return None, None, None
    # Geyer-style positive consecutive lag pairs. Each successive retained
    # pair is bounded by its predecessor to suppress noisy upward excursions.
    pair_totals = []
    for index in range(0, len(coefficients) - 1, 2):
        pair = coefficients[index] + coefficients[index + 1]
        if pair <= 0.0:
            break
        pair_totals.append(min(pair, pair_totals[-1]) if pair_totals else pair)
    tau = max(1.0, 1.0 + 2.0 * fsum(pair_totals))
    ess = len(chains) * n / tau
    return coefficients[0], tau, ess


def _split_rhat(chains: tuple[tuple[float, ...], ...]) -> float | None:
    half = len(chains[0]) // 2
    splits = tuple(part for chain in chains for part in (chain[:half], chain[-half:]))
    within = mean(tuple(_sample_variance(part) for part in splits))
    if within == 0.0:
        return None
    between = half * _sample_variance(tuple(mean(part) for part in splits))
    estimated = (half - 1) / half * within + between / half
    return sqrt(estimated / within)


def _half_shift(chains: tuple[tuple[float, ...], ...]) -> float | None:
    half = len(chains[0]) // 2
    shifts = []
    for chain in chains:
        first, last = chain[:half], chain[-half:]
        delta = abs(mean(last) - mean(first))
        sigma = stdev(chain)
        if sigma == 0.0:
            if delta != 0.0:
                return None
            shifts.append(0.0)
        else:
            shifts.append(delta / sigma)
    return max(shifts)


@dataclass(frozen=True, slots=True)
class FLiBeReplicaSamplingObservable:
    """Per-observable sample-mixing diagnostics with explicit SI units."""

    unit: str
    replica_means: tuple[float, ...]
    split_rhat: float | None
    pooled_lag_one_autocorrelation: float | None
    positive_pair_autocorrelation_time_samples: float | None
    effective_sample_size_proxy: float | None
    maximum_standardized_half_window_shift: float | None
    diagnostic_status: str

    def __post_init__(self) -> None:
        if self.unit not in ("K", "Pa", "kg/m^3"):
            raise ValueError("unit must be a supported SI unit.")
        if not isinstance(self.replica_means, tuple) or len(self.replica_means) < 2:
            raise ValueError("replica_means must contain at least two values.")
        if not all(isfinite(value) for value in self.replica_means):
            raise ValueError("replica means must be finite.")
        for name in (
            "split_rhat", "positive_pair_autocorrelation_time_samples",
            "effective_sample_size_proxy",
        ):
            value = getattr(self, name)
            if value is not None:
                _positive_real(value, name)
        for name in (
            "pooled_lag_one_autocorrelation",
            "maximum_standardized_half_window_shift",
        ):
            value = getattr(self, name)
            if value is not None and (not isfinite(value) or (
                name == "pooled_lag_one_autocorrelation" and not -1.0 <= value <= 1.0
            ) or (
                name == "maximum_standardized_half_window_shift" and value < 0.0
            )):
                raise ValueError(f"{name} must be finite and in its domain.")
        if self.diagnostic_status not in (
            "FIXED_SERIES_CONSTANT", "WITHIN_REPLICA_VARIANCE_ZERO",
            "SCREENING_CRITERIA_MET", "SCREENING_CRITERIA_FLAGGED",
        ):
            raise ValueError("unknown diagnostic status.")


@dataclass(frozen=True, slots=True)
class FLiBeTrajectoryStationarityDiagnostics:
    """Aligned replica sampling diagnostics and their declared criteria."""

    method_id: str
    model_id: str
    parameter_source_sha256: str
    provenance: ParameterProvenance
    velocity_frame: FLiBeVelocityFrame
    physical_state_id: str
    physical_state_method_id: str
    replica_ids: tuple[str, ...]
    initial_condition_sha256: tuple[str, ...]
    discarded_initial_samples: int
    retained_samples_per_replica: int
    central_sample_dropped_per_replica: int
    sampling_interval_s: float
    maximum_split_rhat: float
    minimum_effective_sample_size: float
    maximum_absolute_lag_one_correlation: float
    maximum_standardized_half_window_shift: float
    temperature: FLiBeReplicaSamplingObservable
    pressure: FLiBeReplicaSamplingObservable
    density: FLiBeReplicaSamplingObservable

    def __post_init__(self) -> None:
        if self.method_id != METHOD_ID:
            raise ValueError("method_id must match the stationarity estimator.")
        if not self.model_id or not self.physical_state_id or not self.physical_state_method_id:
            raise ValueError("model and physical-state identifiers must be nonempty.")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        if not isinstance(self.velocity_frame, FLiBeVelocityFrame):
            raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
        if len(self.parameter_source_sha256) != 64 or any(
            c not in "0123456789abcdef" for c in self.parameter_source_sha256
        ):
            raise ValueError("parameter_source_sha256 must be a lowercase SHA-256.")
        if len(self.replica_ids) < 2 or len(set(self.replica_ids)) != len(self.replica_ids):
            raise ValueError("replica_ids must contain distinct run identifiers.")
        if len(set(self.initial_condition_sha256)) != len(self.replica_ids):
            raise ValueError("each replica requires a distinct initialization digest.")
        _nonnegative_integer(self.discarded_initial_samples, "discarded_initial_samples")
        if self.retained_samples_per_replica < 8:
            raise ValueError("at least eight retained samples are required.")
        if self.central_sample_dropped_per_replica != self.retained_samples_per_replica % 2:
            raise ValueError("central split sample accounting differs.")
        for name in (
            "sampling_interval_s", "maximum_split_rhat", "minimum_effective_sample_size",
            "maximum_absolute_lag_one_correlation", "maximum_standardized_half_window_shift",
        ):
            _positive_real(getattr(self, name), name)
        if self.maximum_absolute_lag_one_correlation > 1.0:
            raise ValueError("correlation limit must not exceed one.")
        for name, _, unit in _FIELDS:
            item = getattr(self, name)
            if not isinstance(item, FLiBeReplicaSamplingObservable) or item.unit != unit:
                raise ValueError(f"{name} requires a {unit} diagnostic.")
            if len(item.replica_means) != len(self.replica_ids):
                raise ValueError("observable and replica populations differ.")

    @property
    def replica_count(self) -> int:
        return len(self.replica_ids)

    @property
    def observed_duration_s(self) -> float:
        return (self.retained_samples_per_replica - 1) * self.sampling_interval_s


def evaluate_flibe_replica_sampling_stationarity(
    traces: tuple[FLiBeReplicaThermodynamicTrace, ...],
    *,
    discarded_initial_samples: int = 0,
    retained_samples_per_replica: int | None = None,
    maximum_split_rhat: float = 1.05,
    minimum_effective_sample_size: float = 40.0,
    maximum_absolute_lag_one_correlation: float = 0.5,
    maximum_standardized_half_window_shift: float = 0.5,
) -> FLiBeTrajectoryStationarityDiagnostics:
    """Evaluate trace-aligned sampling diagnostics for registered FLiBe replicas.

    All replicas must use the same composition, model, parameter source,
    pressure operator, velocity frame, physical-state designation, sampling
    interval, and observation count. Each selected series has at least eight
    frames. The effective sample size is a positive-pair autocorrelation
    proxy based on within-replica centered data, and is screened together
    with split R-hat, drift, and lag-one correlation. Diagnostic statuses
    describe the declared finite-sample screening criteria.
    """
    if not isinstance(traces, tuple) or len(traces) < 2 or any(
        not isinstance(t, FLiBeReplicaThermodynamicTrace) for t in traces
    ):
        raise TypeError("traces must contain at least two typed FLiBe replicas.")
    discard = _nonnegative_integer(discarded_initial_samples, "discarded_initial_samples")
    for name, value in (
        ("maximum_split_rhat", maximum_split_rhat),
        ("minimum_effective_sample_size", minimum_effective_sample_size),
        ("maximum_absolute_lag_one_correlation", maximum_absolute_lag_one_correlation),
        ("maximum_standardized_half_window_shift", maximum_standardized_half_window_shift),
    ):
        _positive_real(value, name)
    if maximum_absolute_lag_one_correlation > 1.0:
        raise ValueError("maximum_absolute_lag_one_correlation must be at most one.")
    if retained_samples_per_replica is None:
        remaining = {len(r.thermodynamics.samples) - discard for r in traces}
        if len(remaining) != 1:
            raise ValueError("replica lengths differ; declare an identical retained count.")
        retained = remaining.pop()
    else:
        retained = _nonnegative_integer(
            retained_samples_per_replica, "retained_samples_per_replica"
        )
    if retained < 8:
        raise ValueError("split-chain diagnostics require at least eight retained samples.")

    replica_ids = tuple(r.replica_id for r in traces)
    initial_digests = tuple(r.initial_condition_sha256 for r in traces)
    trajectory_ids = tuple(
        r.thermodynamics.pressure_trace.density_trace.trajectory_id for r in traces
    )
    if any(len(set(row)) != len(row) for row in (replica_ids, initial_digests, trajectory_ids)):
        raise ValueError("replica, trajectory, and initial-condition identities must be unique.")
    template = traces[0]
    baseline = template.thermodynamics
    base_pressure = baseline.pressure_trace
    base_density = base_pressure.density_trace
    step_interval_s = None
    observations: dict[str, list[tuple[float, ...]]] = {
        name: [] for name, _, _ in _FIELDS
    }

    for record in traces:
        thermal = record.thermodynamics
        pressure = thermal.pressure_trace
        density = pressure.density_trace
        if record.parameter_source_sha256 != template.parameter_source_sha256:
            raise ValueError("parameter-source fingerprints differ.")
        if (
            density.model_id != base_density.model_id
            or density.composition != base_density.composition
            or density.atom_count != base_density.atom_count
            or density.total_mass_kg != base_density.total_mass_kg
            or density.provenance != base_density.provenance
            or density.coordinate_unit_to_meter != base_density.coordinate_unit_to_meter
            or density.mass_unit_to_kg != base_density.mass_unit_to_kg
            or pressure.velocity_frame != base_pressure.velocity_frame
            or pressure.time_unit_to_second != base_pressure.time_unit_to_second
            or pressure.stress_method_id != base_pressure.stress_method_id
            or pressure.source_id != base_pressure.source_id
            or pressure.provenance != base_pressure.provenance
            or thermal.degrees_of_freedom != baseline.degrees_of_freedom
            or thermal.physical_state_id != baseline.physical_state_id
            or thermal.physical_state_method_id != baseline.physical_state_method_id
        ):
            raise ValueError("replica physical coordinates or methods differ.")
        end = discard + retained
        if len(thermal.samples) < end:
            raise ValueError("a replica lacks the selected observation count.")
        selected_t = thermal.samples[discard:end]
        selected_p = pressure.samples[discard:end]
        selected_d = density.samples[discard:end]
        sample_interval = (selected_t[1].md_time - selected_t[0].md_time)
        if not isfinite(sample_interval) or sample_interval <= 0.0:
            raise ValueError("MD sample intervals must increase.")
        physical_interval = sample_interval * pressure.time_unit_to_second
        if step_interval_s is None:
            step_interval_s = physical_interval
        elif not isclose(step_interval_s, physical_interval, rel_tol=1e-12, abs_tol=0.0):
            raise ValueError("replica sampling intervals differ.")
        state_delta = selected_t[1].state_index - selected_t[0].state_index
        step_delta = selected_t[1].md_step - selected_t[0].md_step
        if state_delta <= 0 or step_delta <= 0:
            raise ValueError("MD state and step indices must increase.")
        for i, (t, p, d) in enumerate(zip(selected_t, selected_p, selected_d, strict=True)):
            coordinates = (t.state_index, t.md_step, t.md_time)
            if coordinates != (p.state_index, p.md_step, p.md_time) or coordinates != (
                d.state_index, d.md_step, d.md_time
            ):
                raise ValueError("thermal, pressure, and density frames differ.")
            if (
                t.state_index != selected_t[0].state_index + i * state_delta
                or t.md_step != selected_t[0].md_step + i * step_delta
                or not isclose(t.md_time, selected_t[0].md_time + i * sample_interval,
                               rel_tol=1e-10, abs_tol=1e-12 * sample_interval)
            ):
                raise ValueError("MD samples require a uniform physical time grid.")
            if not isclose(d.density_kg_m3 * d.cell_volume_m3,
                           density.total_mass_kg, rel_tol=1e-12, abs_tol=0.0):
                raise ValueError("density and mass-volume coordinates differ.")
            tensor_pressure = fsum(p.pressure_tensor_pa[axis][axis] for axis in range(3)) / 3.0
            if not isclose(p.scalar_pressure_pa, tensor_pressure,
                           rel_tol=1e-12, abs_tol=1e-6):
                raise ValueError("signed pressure and tensor trace differ.")
        observations["temperature"].append(tuple(t.kinetic_temperature_k for t in selected_t))
        observations["pressure"].append(tuple(p.scalar_pressure_pa for p in selected_p))
        observations["density"].append(tuple(d.density_kg_m3 for d in selected_d))

    assert step_interval_s is not None
    diagnostic: dict[str, FLiBeReplicaSamplingObservable] = {}
    for name, _, unit in _FIELDS:
        chains = tuple(observations[name])
        all_constant = all(value == chains[0][0] for chain in chains for value in chain)
        rhat = _split_rhat(chains)
        lag_one, tau, ess = _correlation_time(chains)
        half_shift = _half_shift(chains)
        if all_constant:
            status = "FIXED_SERIES_CONSTANT"
        elif None in (rhat, lag_one, tau, ess, half_shift):
            status = "WITHIN_REPLICA_VARIANCE_ZERO"
        elif (
            rhat <= maximum_split_rhat
            and ess >= minimum_effective_sample_size
            and abs(lag_one) <= maximum_absolute_lag_one_correlation
            and half_shift <= maximum_standardized_half_window_shift
        ):
            status = "SCREENING_CRITERIA_MET"
        else:
            status = "SCREENING_CRITERIA_FLAGGED"
        diagnostic[name] = FLiBeReplicaSamplingObservable(
            unit=unit,
            replica_means=tuple(mean(row) for row in chains),
            split_rhat=rhat,
            pooled_lag_one_autocorrelation=lag_one,
            positive_pair_autocorrelation_time_samples=tau,
            effective_sample_size_proxy=ess,
            maximum_standardized_half_window_shift=half_shift,
            diagnostic_status=status,
        )

    return FLiBeTrajectoryStationarityDiagnostics(
        method_id=METHOD_ID,
        model_id=base_density.model_id,
        parameter_source_sha256=template.parameter_source_sha256,
        provenance=base_density.provenance,
        velocity_frame=base_pressure.velocity_frame,
        physical_state_id=baseline.physical_state_id,
        physical_state_method_id=baseline.physical_state_method_id,
        replica_ids=replica_ids,
        initial_condition_sha256=initial_digests,
        discarded_initial_samples=discard,
        retained_samples_per_replica=retained,
        central_sample_dropped_per_replica=retained % 2,
        sampling_interval_s=step_interval_s,
        maximum_split_rhat=maximum_split_rhat,
        minimum_effective_sample_size=minimum_effective_sample_size,
        maximum_absolute_lag_one_correlation=maximum_absolute_lag_one_correlation,
        maximum_standardized_half_window_shift=maximum_standardized_half_window_shift,
        **diagnostic,
    )
