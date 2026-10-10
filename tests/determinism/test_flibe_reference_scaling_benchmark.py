"""CI qualification for the structured FLiBe TR-EIP size-scaling benchmark."""

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
    / "reference_scaling.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-scaling.v1"
)

_EXPECTED_REPLICA_COUNTS = (
    1,
    2,
    4,
    8,
)

_EXPECTED_CHECKS = {
    "atom_count_linear",
    "graph_edge_count_linear",
    "atomic_energy_count_linear",
    "total_energy_extensive",
    "energy_per_replica_constant",
    "composition_preserved",
    "resonance_coordinate_preserved",
    "ternary_node_count_linear",
    "feature_channel_width_preserved",
}


def _run_benchmark() -> tuple[dict[str, object], bytes]:
    """Execute the scaling benchmark in an independent Python process."""

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
    """Return the typed scaling sample collection."""

    observed = report["observed"]

    assert isinstance(observed, dict)

    samples = observed["samples"]

    assert isinstance(samples, list)

    for sample in samples:
        assert isinstance(sample, dict)

    return samples


def test_flibe_reference_scaling_benchmark_exists() -> None:
    """The committed size-scaling benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_reference_scaling_benchmark_passes() -> None:
    """The benchmark must report PASS from an independent process."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_all_scaling_checks_pass() -> None:
    """Every structured size-scaling invariant must pass."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)
    assert set(checks) == _EXPECTED_CHECKS

    assert all(
        value is True
        for value in checks.values()
    )


def test_scaling_benchmark_uses_declared_replica_sequence() -> None:
    """The benchmark must retain its fixed structural scaling sequence."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    replica_counts = observed[
        "replica_counts"
    ]

    assert replica_counts == list(
        _EXPECTED_REPLICA_COUNTS
    )

    samples = _samples(report)

    assert tuple(
        sample["replica_count"]
        for sample in samples
    ) == _EXPECTED_REPLICA_COUNTS


def test_atom_count_scales_linearly() -> None:
    """Every isolated FLiBe replica must contribute exactly seven atoms."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    for sample in samples:
        replica_count = sample[
            "replica_count"
        ]
        atom_count = sample[
            "atom_count"
        ]

        assert isinstance(
            replica_count,
            int,
        )
        assert isinstance(
            atom_count,
            int,
        )

        assert atom_count == (
            7 * replica_count
        )


def test_graph_edge_count_scales_linearly() -> None:
    """Separated replicas must scale graph cardinality without cross-links."""

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
        edge_count = sample[
            "graph_edge_count"
        ]

        assert isinstance(
            replica_count,
            int,
        )
        assert isinstance(
            edge_count,
            int,
        )

        assert edge_count == (
            baseline_edges
            * replica_count
        )


def test_atomic_energy_cardinality_matches_atom_count() -> None:
    """The energy model must retain one atomic energy per graph node."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    for sample in samples:
        assert (
            sample["atomic_energy_count"]
            == sample["atom_count"]
        )


def test_total_energy_is_extensive_for_isolated_replicas() -> None:
    """Isolated identical replicas must reproduce linear total-energy scaling."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    tolerance = report[
        "absolute_tolerance"
    ]

    assert isinstance(
        tolerance,
        (int, float),
    )

    baseline_energy = samples[0][
        "total_energy"
    ]

    assert isinstance(
        baseline_energy,
        (int, float),
    )

    for sample in samples:
        replica_count = sample[
            "replica_count"
        ]
        total_energy = sample[
            "total_energy"
        ]

        assert isinstance(
            replica_count,
            int,
        )
        assert isinstance(
            total_energy,
            (int, float),
        )

        expected = (
            baseline_energy
            * replica_count
        )

        assert abs(
            total_energy - expected
        ) <= tolerance


def test_energy_per_replica_is_constant() -> None:
    """The intensive per-replica benchmark energy must remain unchanged."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    tolerance = report[
        "absolute_tolerance"
    ]

    assert isinstance(
        tolerance,
        (int, float),
    )

    baseline = samples[0][
        "energy_per_replica"
    ]

    assert isinstance(
        baseline,
        (int, float),
    )

    for sample in samples:
        value = sample[
            "energy_per_replica"
        ]

        assert isinstance(
            value,
            (int, float),
        )

        assert abs(
            value - baseline
        ) <= tolerance


def test_exact_flibe_composition_is_preserved_across_sizes() -> None:
    """Size scaling must not alter the exact LiF-BeF2 composition."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    tolerance = report[
        "absolute_tolerance"
    ]

    assert isinstance(
        tolerance,
        (int, float),
    )

    for sample in samples:
        lif_fraction = sample[
            "lif_fraction"
        ]
        bef2_fraction = sample[
            "bef2_fraction"
        ]

        assert isinstance(
            lif_fraction,
            (int, float),
        )
        assert isinstance(
            bef2_fraction,
            (int, float),
        )

        assert abs(
            lif_fraction
            - (2.0 / 3.0)
        ) <= tolerance

        assert abs(
            bef2_fraction
            - (1.0 / 3.0)
        ) <= tolerance


def test_resonance_coordinate_is_size_invariant() -> None:
    """Replicating the fixed oscillator pattern must preserve its coordinate."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    baseline = samples[0][
        "resonance_coordinate"
    ]

    assert isinstance(
        baseline,
        list,
    )
    assert len(baseline) == 2

    for sample in samples:
        assert (
            sample["resonance_coordinate"]
            == baseline
        )


def test_ternary_node_count_scales_with_atom_count() -> None:
    """Balanced ternary execution must retain one node per atom."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    for sample in samples:
        assert (
            sample["ternary_node_count"]
            == sample["atom_count"]
        )


def test_feature_channel_width_is_size_invariant() -> None:
    """Node count scaling must not alter TR-EIP feature representation width."""

    report, _ = _run_benchmark()

    samples = _samples(report)

    for sample in samples:
        assert (
            sample["scalar_channel_count"]
            == 3
        )
        assert (
            sample["vector_channel_count"]
            == 1
        )


def test_scaling_benchmark_output_is_byte_deterministic() -> None:
    """Independent executions must emit byte-identical structured JSON."""

    first_report, first_bytes = _run_benchmark()
    second_report, second_bytes = _run_benchmark()

    assert first_report == second_report
    assert first_bytes == second_bytes


def test_scaling_benchmark_has_no_unstructured_stdout() -> None:
    """Benchmark stdout must contain only canonical structured JSON."""

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
