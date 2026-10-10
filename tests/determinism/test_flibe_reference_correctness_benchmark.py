"""Deterministic CI qualification for the FLiBe correctness benchmark."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

_BENCHMARK_PATH = (
    _REPOSITORY_ROOT
    / "benchmarks"
    / "flibe"
    / "reference_correctness.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-correctness.v1"
)


def _run_benchmark() -> tuple[dict[str, object], bytes]:
    """Execute the benchmark in an independent Python process."""

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

    report = json.loads(
        result.stdout.decode("utf-8")
    )

    assert isinstance(report, dict)

    return report, result.stdout


def test_flibe_reference_correctness_benchmark_exists() -> None:
    """The committed correctness benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_reference_correctness_benchmark_passes() -> None:
    """The benchmark must report PASS from an independent process."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_all_flibe_reference_correctness_checks_pass() -> None:
    """Every structured benchmark correctness check must pass."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)
    assert checks
    assert all(
        value is True
        for value in checks.values()
    )


def test_correctness_benchmark_contains_required_architectural_checks() -> None:
    """The benchmark must retain the TR-EIF architectural observables."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)

    required = {
        "atom_count",
        "graph_node_count",
        "graph_edge_count",
        "lif_fraction",
        "bef2_fraction",
        "phase_order",
        "frequency_spread",
        "retained_ternary_state",
        "scalar_channel_count",
        "vector_channel_count",
        "atomic_energies",
        "total_energy",
    }

    assert set(checks) == required


def test_correctness_benchmark_retains_balanced_ternary_state() -> None:
    """Structured output must retain canonical -1/0/1 execution state."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    assert observed["retained_ternary_state"] == [
        -1,
        0,
        1,
        0,
        -1,
        1,
        0,
    ]


def test_correctness_benchmark_retains_resonance_coordinate() -> None:
    """Structured output must retain the continuous resonance coordinate."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    coordinate = observed["resonance_coordinate"]

    assert isinstance(coordinate, list)
    assert len(coordinate) == 2


def test_correctness_benchmark_output_is_byte_deterministic() -> None:
    """Independent executions must emit byte-identical structured JSON."""

    first_report, first_bytes = _run_benchmark()
    second_report, second_bytes = _run_benchmark()

    assert first_report == second_report
    assert first_bytes == second_bytes


def test_correctness_benchmark_has_no_unstructured_stdout() -> None:
    """Benchmark stdout must consist only of one structured JSON document."""

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
