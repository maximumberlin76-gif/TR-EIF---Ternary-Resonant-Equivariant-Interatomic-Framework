
"""Sampling diagnostics for real periodic polarizable FLiBe MD replicas.

Reuse the registered four-replica NVE workload and evaluate both the complete
nine-frame observation window and the eight frames following a declared
initial discard. Split R-hat, autocorrelation time, effective sample count,
and standardized within-replica drift are independently recalculated from
recorded physical observables in SI units.

Each diagnostic belongs to the interatomic MD qualification layer of TR-EIF.
The continuous resonance, balanced-ternary execution, and equivariant
mappings retain separate integration qualification contracts.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from dataclasses import asdict
from math import fsum, isclose, isfinite, sqrt
from pathlib import Path
from statistics import mean, stdev

from tr_eif.flibe.trajectory_replica_stationarity import (
    METHOD_ID,
    evaluate_flibe_replica_sampling_stationarity,
)

ROOT = Path(__file__).resolve().parents[2]
BUILDER_PATH = Path(__file__).with_name(
    "periodic_md_replica_duration_benchmark.py"
)
PAIR_PATH = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"

BENCHMARK_ID = "tr-eif.flibe.periodic-md-replica-stationarity-benchmark.v1"

WINDOWS = (
    ("all_nine_frames", 0, 9),
    ("discard_first_frame", 1, 8),
)

OBSERVABLES = (
    ("temperature", "temperature_k", "K"),
    ("pressure", "signed_pressure_pa", "Pa"),
    ("density", "density_kg_m3", "kg/m^3"),
)

MAX_RHAT = 1.05
MIN_ESS = 40.0
MAX_ABS_LAG_ONE = 0.5
MAX_HALF_SHIFT = 0.5


def _close(left: float | None, right: float | None) -> bool:
    if left is None or right is None:
        return left is None and right is None

    return isclose(
        left,
        right,
        rel_tol=1.0e-10,
        abs_tol=1.0e-11,
    )


def _independent_diagnostics(
    chains: tuple[tuple[float, ...], ...],
) -> dict[str, object]:
    """Reconstruct split variance, lag covariance, and sampling drift."""

    count = len(chains)
    length = len(chains[0])
    half = length // 2

    segments = tuple(
        part
        for chain in chains
        for part in (chain[:half], chain[-half:])
    )

    within = mean(stdev(part) ** 2 for part in segments)

    between = half * stdev(
        tuple(mean(part) for part in segments)
    ) ** 2

    rhat = (
        sqrt(
            ((half - 1) * within + between)
            / (half * within)
        )
        if within
        else None
    )

    centers = tuple(mean(chain) for chain in chains)

    variance = fsum(
        fsum(
            (value - center) ** 2
            for value in chain
        ) / length
        for chain, center in zip(
            chains,
            centers,
            strict=True,
        )
    ) / count

    if variance == 0.0:
        lag_one = tau = effective = None

    else:
        correlation = []

        for lag in range(1, length):
            covariance = fsum(
                fsum(
                    (chain[i] - center)
                    * (chain[i + lag] - center)
                    for i in range(length - lag)
                ) / (length - lag)
                for chain, center in zip(
                    chains,
                    centers,
                    strict=True,
                )
            ) / count

            correlation.append(
                max(-1.0, min(1.0, covariance / variance))
            )

        lag_one = correlation[0]
        positive_pairs = []

        for index in range(0, len(correlation) - 1, 2):
            pair = (
                correlation[index]
                + correlation[index + 1]
            )

            if pair <= 0.0:
                break

            positive_pairs.append(
                min(pair, positive_pairs[-1])
                if positive_pairs
                else pair
            )

        tau = max(
            1.0,
            1.0 + 2.0 * fsum(positive_pairs),
        )

        effective = count * length / tau

    shifts = []

    for chain in chains:
        difference = abs(
            mean(chain[-half:])
            - mean(chain[:half])
        )

        deviation = stdev(chain)

        shifts.append(
            difference / deviation
            if deviation
            else (0.0 if difference == 0.0 else None)
        )

    half_shift = (
        max(shifts)
        if all(value is not None for value in shifts)
        else None
    )

    constant = all(
        value == chains[0][0]
        for chain in chains
        for value in chain
    )

    if constant:
        status = "FIXED_SERIES_CONSTANT"

    elif None in (
        rhat,
        lag_one,
        tau,
        effective,
        half_shift,
    ):
        status = "WITHIN_REPLICA_VARIANCE_ZERO"

    elif (
        rhat <= MAX_RHAT
        and effective >= MIN_ESS
        and abs(lag_one) <= MAX_ABS_LAG_ONE
        and half_shift <= MAX_HALF_SHIFT
    ):
        status = "SCREENING_CRITERIA_MET"

    else:
        status = "SCREENING_CRITERIA_FLAGGED"

    return {
        "replica_means": centers,
        "split_rhat": rhat,
        "pooled_lag_one_autocorrelation": lag_one,
        "positive_pair_autocorrelation_time_samples": tau,
        "effective_sample_size_proxy": effective,
        "maximum_standardized_half_window_shift": half_shift,
        "diagnostic_status": status,
    }


def _window_record(result, tag: str) -> dict[str, object]:
    return {
        "window_id": tag,
        "method_id": result.method_id,
        "model_id": result.model_id,
        "parameter_source_sha256": result.parameter_source_sha256,
        "provenance": result.provenance.value,
        "velocity_frame": result.velocity_frame.value,
        "physical_state_id": result.physical_state_id,
        "physical_state_method_id": result.physical_state_method_id,
        "replica_ids": list(result.replica_ids),
        "initial_condition_sha256": list(
            result.initial_condition_sha256
        ),
        "discarded_initial_samples": result.discarded_initial_samples,
        "retained_samples_per_replica": result.retained_samples_per_replica,
        "central_sample_dropped_per_replica": (
            result.central_sample_dropped_per_replica
        ),
        "sampling_interval_s": result.sampling_interval_s,
        "observed_duration_s": result.observed_duration_s,
        "criteria": {
            "maximum_split_rhat": result.maximum_split_rhat,
            "minimum_effective_sample_size": (
                result.minimum_effective_sample_size
            ),
            "maximum_absolute_lag_one_correlation": (
                result.maximum_absolute_lag_one_correlation
            ),
            "maximum_standardized_half_window_shift": (
                result.maximum_standardized_half_window_shift
            ),
        },
        "observables": {
            name: asdict(getattr(result, name))
            for name, _, _ in OBSERVABLES
        },
    }


def run_benchmark() -> dict[str, object]:
    """Evaluate periodic MD replicas with two declared sampling windows."""

    builder = runpy.run_path(
        str(BUILDER_PATH),
        run_name="flibe_replica_builder",
    )

    model = builder["_model"]()
    replica_count = builder["REPLICA_COUNT"]

    data = tuple(
        builder["_run_replica"](index, model)
        for index in range(replica_count)
    )

    traces = tuple(item[0] for item in data)
    records = [item[1] for item in data]

    digest = hashlib.sha256(
        PAIR_PATH.read_bytes()
    ).hexdigest()

    results = []
    independently_verified = []
    flags_recomputed = []

    for tag, discard, length in WINDOWS:
        output = evaluate_flibe_replica_sampling_stationarity(
            traces,
            discarded_initial_samples=discard,
            retained_samples_per_replica=length,
            maximum_split_rhat=MAX_RHAT,
            minimum_effective_sample_size=MIN_ESS,
            maximum_absolute_lag_one_correlation=MAX_ABS_LAG_ONE,
            maximum_standardized_half_window_shift=MAX_HALF_SHIFT,
        )

        results.append(_window_record(output, tag))

        verified = []
        statuses = []

        for name, source_field, unit in OBSERVABLES:
            chains = tuple(
                tuple(
                    sample[source_field]
                    for sample in record["samples"][
                        discard:discard + length
                    ]
                )
                for record in records
            )

            expected = _independent_diagnostics(chains)
            measured = getattr(output, name)

            verified.append(
                measured.unit == unit
                and all(
                    _close(a, b)
                    for a, b in zip(
                        measured.replica_means,
                        expected["replica_means"],
                        strict=True,
                    )
                )
                and all(
                    _close(
                        getattr(measured, key),
                        expected[key],
                    )
                    for key in (
                        "split_rhat",
                        "pooled_lag_one_autocorrelation",
                        "positive_pair_autocorrelation_time_samples",
                        "effective_sample_size_proxy",
                        "maximum_standardized_half_window_shift",
                    )
                )
            )

            statuses.append(
                measured.diagnostic_status
                == expected["diagnostic_status"]
            )

        independently_verified.append(all(verified))
        flags_recomputed.append(all(statuses))

    initial = tuple(
        builder["_initial_state"](index)
        for index in range(replica_count)
    )

    mass_kg = (
        fsum(initial[0].masses)
        * builder["U_TO_KG"]
    )

    edge = builder["CELL_EDGE_BOHR"]

    density_si = (
        mass_kg
        / (edge * builder["BOHR_TO_M"]) ** 3
    )

    checks = {
        "registered_pair_fingerprint": all(
            row["source_file_sha256"] == digest
            for row in records
        ),

        "replica_initialization_distinctness": len({
            row["initial_condition_sha256"]
            for row in records
        }) == replica_count,

        "common_md_protocol": all(
            len(row["samples"]) == 9
            and all(
                sample["state_index"]
                == sample["md_step"]
                == 2 * n
                and isclose(
                    sample["md_time_code"],
                    0.02 * n,
                    abs_tol=1.0e-14,
                )
                for n, sample in enumerate(row["samples"])
            )
            for row in records
        ),

        "same_initial_temperature": all(
            isclose(
                row["samples"][0]["temperature_k"],
                850.0,
                rel_tol=1.0e-11,
            )
            for row in records
        ),

        "zero_initial_center_of_mass_velocity": all(
            abs(fsum(
                mass * velocity[axis]
                for mass, velocity in zip(
                    state.masses,
                    state.velocities,
                    strict=True,
                )
            )) <= 1.0e-12
            for state in initial
            for axis in range(3)
        ),

        "fixed_cell_density_identity": all(
            isclose(
                sample["density_kg_m3"],
                density_si,
                rel_tol=1.0e-12,
            )
            for row in records
            for sample in row["samples"]
        ),

        "finite_signed_pressures": all(
            isfinite(sample["signed_pressure_pa"])
            for row in records
            for sample in row["samples"]
        ),

        "dipole_stationarity": all(
            row[
                "maximum_dipole_stationarity_residual_atomic"
            ] <= 1.0e-10
            for row in records
        ),

        "two_declared_sampling_windows": all(
            row["discarded_initial_samples"] == discard
            and row["retained_samples_per_replica"] == length
            and row["central_sample_dropped_per_replica"]
            == length % 2
            and row["method_id"] == METHOD_ID
            for row, (_, discard, length) in zip(
                results,
                WINDOWS,
                strict=True,
            )
        ),

        "identical_physical_state_metadata": all(
            row["physical_state_id"] == "UNCLASSIFIED_MD_PHASE"
            and row["model_id"] == builder["MODEL_ID"]
            and row["parameter_source_sha256"] == digest
            for row in results
        ),

        "independently_recalculated_sampling_estimators": all(
            independently_verified
        ),

        "independently_recalculated_statuses": all(
            flags_recomputed
        ),

        "fixed_cell_density_status": all(
            row["observables"]["density"]["diagnostic_status"]
            == "FIXED_SERIES_CONSTANT"
            for row in results
        ),

        "finite_sample_size_boundary": all(
            row["observables"][name]["diagnostic_status"]
            != "SCREENING_CRITERIA_MET"
            for row in results
            for name in ("temperature", "pressure")
        ),
    }

    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,

        "source": {
            "doi": builder["SOURCE_DOI"],
            "relative_path": builder["SOURCE_RELATIVE"],
            "sha256": digest,
            "provenance": "PRIMARY_SOURCE",
        },

        "protocol": {
            "model_id": builder["MODEL_ID"],
            "md_ensemble": "NVE_FIXED_CELL",
            "cell_edge_bohr": edge,
            "species": list(builder["SPECIES"]),
            "time_step_code": builder["TIME_STEP"],
            "time_unit_to_second": builder["TIME_TO_S"],
            "integration_steps": builder["STEPS"],
            "sampling_stride": builder["SAMPLE_STRIDE"],
            "replica_count": replica_count,
            "windows": [list(w) for w in WINDOWS],
            "stationarity_estimator": METHOD_ID,
            "statistical_independence_qualification": "UNASSESSED",
            "thermodynamic_state_qualification": "UNASSESSED",

            "architectural_scope": {
                "executed_layer": "PERIODIC_POLARIZABLE_INTERATOMIC_MD",
                "continuous_resonance_coupling": "SEPARATE_CONTRACT",
                "balanced_ternary_execution": "SEPARATE_CONTRACT",
                "equivariant_mapping_coupling": "SEPARATE_CONTRACT",
            },
        },

        "replicas": records,
        "windows": results,
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(
        report,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ))
    raise SystemExit(
        0 if report["status"] == "PASS" else 1
    )
