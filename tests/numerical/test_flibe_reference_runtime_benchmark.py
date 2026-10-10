"""CI qualification for the structured FLiBe TR-EIP runtime benchmark."""

from __future__ import annotations

from functools import lru_cache
import json
from math import isfinite
from pathlib import Path
import subprocess
import sys


_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

_BENCHMARK_PATH = (
    _REPOSITORY_ROOT
    / "benchmarks"
    / "flibe"
    / "reference_runtime.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-runtime.v1"
)

_EXPECTED_REPLICA_COUNTS = (
    1,
    2,
    4,
    8,
)

_EXPECTED_CHECKS = {
    "replica_sequence",
    "atom_count_linear",
    "measurement_count",
    "positive_runtime",
    "runtime_ordering_valid",
    "runtime_per_atom_finite",
}


@lru_cache(maxsize=1)
def _run_benchmark() -> tuple[dict[str, object], bytes]:
    """Execute the runtime benchmark once in an independent Python process."""

    result = subprocess.run(
        [
            sys.executable,
            str(_BENCHMARK_PATH),
        ],
        cwd=_REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    )

    assert result.returncode == 0, (
        result.stderr.decode(
            "utf-8",
            errors="replace",
        )
    )

    assert result.stderr == b""

    decoded = result.stdout.decode("utf-8")
    report = json.loads(decoded)

    assert isinstance(report, dict)

    return report, result.stdout


def _samples(
    report: dict[str, object],
) -> list[dict[str, object]]:
    """Return the typed runtime sample collection."""

    observed = report["observed"]

    assert isinstance(observed, dict)

    samples = observed["samples"]

    assert isinstance(samples, list)

    for sample in samples:
        assert isinstance(sample, dict)

    return samples


def test_flibe_reference_runtime_benchmark_exists() -> None:
    """The committed runtime benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_reference_runtime_benchmark_passes() -> None:
    """The runtime measurement contract must complete successfully."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_all_runtime_contract_checks_pass() -> None:
    """Every structural runtime-measurement check must pass."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)
    assert set(checks) == _EXPECTED_CHECKS

    assert all(
        value is True
        for value in checks.values()
    )


def test_runtime_measurement_contract_is_explicit() -> None:
    """Clock, measurement scope, repetition counts, and limit policy must be explicit."""

    report, _ = _run_benchmark()

    measurement = report["measurement"]

    assert isinstance(measurement, dict)

    assert measurement["clock"] == "time.perf_counter_ns"
    assert measurement["scope"] == (
        "one complete FLiBe TR-EIP evaluation"
    )

    warmup_runs = measurement[
        "warmup_runs"
    ]
    measurement_runs = measurement[
        "measurement_runs"
    ]

    assert isinstance(
        warmup_runs,
        int,
    )
    assert isinstance(
        measurement_runs,
        int,
    )

    assert warmup_runs > 0
    assert measurement_runs > 0

    assert measurement[
        "absolute_runtime_limit"
    ] is None


def test_runtime_benchmark_uses_declared_replica_sequence() -> None:
    """Runtime evidence must retain the fixed size sequence."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    assert observed["replica_counts"] == list(
        _EXPECTED_REPLICA_COUNTS
    )

    samples = _samples(report)

    assert tuple(
        sample["replica_count"]
        for sample in samples
    ) == _EXPECTED_REPLICA_COUNTS


def test_runtime_samples_preserve_structural_scaling() -> None:
    """Measured systems must retain atom and graph cardinality semantics."""

    report, _ = _run_benchmark()
    samples = _samples(report)

    baseline_edges = samples[0][
        "graph_edge_count"
    ]

    assert isinstance(
        baseline_edges,
        int,
    )
    assert baseline_edges > 0

    for sample in samples:
        replica_count = sample[
            "replica_count"
        ]
        atom_count = sample[
            "atom_count"
        ]
        edge_count = sample[
            "graph_edge_count"
        ]

        assert isinstance(
            replica_count,
            int,
        )
        assert isinstance(
            atom_count,
            int,
        )
        assert isinstance(
            edge_count,
            int,
        )

        assert atom_count == (
            7 * replica_count
        )

        assert edge_count == (
            baseline_edges
            * replica_count
        )


def test_runtime_samples_have_declared_measurement_cardinality() -> None:
    """Every size must contain exactly the declared number of timed executions."""

    report, _ = _run_benchmark()

    measurement = report["measurement"]

    assert isinstance(measurement, dict)

    expected_count = measurement[
        "measurement_runs"
    ]

    assert isinstance(
        expected_count,
        int,
    )

    for sample in _samples(report):
        durations = sample[
            "durations_ns"
        ]

        assert isinstance(
            durations,
            list,
        )

        assert sample[
            "measurement_count"
        ] == expected_count

        assert len(
            durations
        ) == expected_count

        assert all(
            isinstance(
                duration,
                int,
            )
            for duration in durations
        )

        assert all(
            duration > 0
            for duration in durations
        )


def test_runtime_summary_matches_raw_measurements() -> None:
    """Minimum, median envelope, and maximum must agree with raw timings."""

    report, _ = _run_benchmark()

    for sample in _samples(report):
        durations = sample[
            "durations_ns"
        ]

        assert isinstance(
            durations,
            list,
        )

        minimum = sample[
            "minimum_runtime_ns"
        ]
        median_runtime = sample[
            "median_runtime_ns"
        ]
        maximum = sample[
            "maximum_runtime_ns"
        ]

        assert isinstance(
            minimum,
            int,
        )
        assert isinstance(
            median_runtime,
            (int, float),
        )
        assert isinstance(
            maximum,
            int,
        )

        assert minimum == min(
            durations
        )

        assert maximum == max(
            durations
        )

        assert (
            minimum
            <= median_runtime
            <= maximum
        )


def test_runtime_per_atom_is_finite_and_consistent() -> None:
    """Reported normalized runtime must equal median runtime divided by atom count."""

    report, _ = _run_benchmark()

    for sample in _samples(report):
        atom_count = sample[
            "atom_count"
        ]
        median_runtime = sample[
            "median_runtime_ns"
        ]
        per_atom = sample[
            "median_runtime_ns_per_atom"
        ]

        assert isinstance(
            atom_count,
            int,
        )
        assert isinstance(
            median_runtime,
            (int, float),
        )
        assert isinstance(
            per_atom,
            (int, float),
        )

        assert isfinite(
            float(per_atom)
        )
        assert per_atom > 0.0

        assert per_atom == (
            median_runtime
            / float(atom_count)
        )


def test_runtime_samples_are_completed_tr_eip_evaluations() -> None:
    """Every timed execution must retain a finite TR-EIP energy output."""

    report, _ = _run_benchmark()

    for sample in _samples(report):
        total_energy = sample[
            "total_energy"
        ]

        assert isinstance(
            total_energy,
            (int, float),
        )

        assert isfinite(
            float(total_energy)
        )


def test_runtime_benchmark_does_not_encode_performance_threshold() -> None:
    """Runner-dependent timing must not become a false correctness invariant."""

    report, _ = _run_benchmark()

    measurement = report["measurement"]

    assert isinstance(measurement, dict)

    assert measurement[
        "absolute_runtime_limit"
    ] is None

    checks = report["checks"]

    assert isinstance(checks, dict)

    assert "runtime_below_limit" not in checks
    assert "runtime_monotonic" not in checks
    assert "runtime_scaling_ratio" not in checks


def test_runtime_benchmark_stdout_is_structured_json() -> None:
    """Benchmark stdout must contain one canonical structured JSON document."""

    _, output = _run_benchmark()

    decoded = output.decode("utf-8")
    parsed = json.loads(decoded)

    assert isinstance(parsed, dict)

    canonical = json.dumps(
        parsed,
        indent=2,
        sort_keys=True,
    ) + "\n"

    assert decoded == canonical
