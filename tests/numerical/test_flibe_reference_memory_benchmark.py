"""CI qualification for the structured FLiBe TR-EIP memory-use benchmark."""

from __future__ import annotations

from functools import lru_cache
import json
from math import isfinite, isclose
from pathlib import Path
import subprocess
import sys


_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

_BENCHMARK_PATH = (
    _REPOSITORY_ROOT
    / "benchmarks"
    / "flibe"
    / "reference_memory.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-memory.v1"
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
    "memory_measurements_positive",
    "peak_not_below_current",
    "peak_per_atom_positive",
    "ternary_node_count_matches_atoms",
    "resonance_coordinate_defined",
}


@lru_cache(maxsize=1)
def _run_benchmark() -> tuple[dict[str, object], bytes]:
    """Execute the memory benchmark once in an independent Python process."""

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
    """Return the typed memory benchmark sample collection."""

    observed = report["observed"]

    assert isinstance(observed, dict)

    samples = observed["samples"]

    assert isinstance(samples, list)

    for sample in samples:
        assert isinstance(sample, dict)

    return samples


def test_flibe_reference_memory_benchmark_exists() -> None:
    """The committed memory-use benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_reference_memory_benchmark_passes() -> None:
    """The benchmark must report PASS from an independent process."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_all_memory_benchmark_checks_pass() -> None:
    """Every structural memory-measurement check must pass."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)
    assert set(checks) == _EXPECTED_CHECKS

    assert all(
        value is True
        for value in checks.values()
    )


def test_memory_measurement_contract_is_explicit() -> None:
    """The report must state allocator, scope, and absence of a hard RAM gate."""

    report, _ = _run_benchmark()

    measurement = report["measurement"]

    assert isinstance(measurement, dict)
    assert measurement["allocator"] == "python-tracemalloc"
    assert measurement["absolute_memory_limit"] is None
    assert measurement["scope"] == (
        "traced Python allocations during one "
        "complete FLiBe TR-EIP evaluation"
    )


def test_memory_benchmark_uses_declared_replica_sequence() -> None:
    """Memory measurements must retain the fixed size sequence."""

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


def test_memory_samples_retain_structural_cardinality() -> None:
    """Each sample must preserve atom, graph, and ternary cardinalities."""

    report, _ = _run_benchmark()
    samples = _samples(report)

    baseline_edges = samples[0][
        "graph_edge_count"
    ]

    assert isinstance(
        baseline_edges,
        int,
    )

    for sample in samples:
        replica_count = sample[
            "replica_count"
        ]
        atom_count = sample[
            "atom_count"
        ]
        graph_edge_count = sample[
            "graph_edge_count"
        ]
        ternary_node_count = sample[
            "ternary_node_count"
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
            graph_edge_count,
            int,
        )
        assert isinstance(
            ternary_node_count,
            int,
        )

        assert atom_count == (
            7 * replica_count
        )

        assert graph_edge_count == (
            baseline_edges
            * replica_count
        )

        assert ternary_node_count == atom_count


def test_memory_samples_report_valid_traced_allocations() -> None:
    """Current and peak traced allocation metrics must be internally valid."""

    report, _ = _run_benchmark()
    samples = _samples(report)

    for sample in samples:
        atom_count = sample[
            "atom_count"
        ]
        current_bytes = sample[
            "current_traced_bytes"
        ]
        peak_bytes = sample[
            "peak_traced_bytes"
        ]
        peak_per_atom = sample[
            "peak_bytes_per_atom"
        ]

        assert isinstance(
            atom_count,
            int,
        )
        assert isinstance(
            current_bytes,
            int,
        )
        assert isinstance(
            peak_bytes,
            int,
        )
        assert isinstance(
            peak_per_atom,
            (int, float),
        )

        assert current_bytes >= 0
        assert peak_bytes > 0
        assert peak_bytes >= current_bytes
        assert peak_per_atom > 0.0

        assert isclose(
            float(peak_per_atom),
            peak_bytes / float(atom_count),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )


def test_memory_samples_retain_executable_tr_eip_outputs() -> None:
    """Every memory sample must represent a completed TR-EIP evaluation."""

    report, _ = _run_benchmark()
    samples = _samples(report)

    baseline_coordinate = samples[0][
        "resonance_coordinate"
    ]

    assert isinstance(
        baseline_coordinate,
        list,
    )
    assert len(baseline_coordinate) == 2

    for sample in samples:
        total_energy = sample[
            "total_energy"
        ]
        coordinate = sample[
            "resonance_coordinate"
        ]

        assert isinstance(
            total_energy,
            (int, float),
        )

        assert isfinite(
            float(total_energy)
        )

        assert coordinate == baseline_coordinate


def test_memory_benchmark_stdout_is_structured_json() -> None:
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
