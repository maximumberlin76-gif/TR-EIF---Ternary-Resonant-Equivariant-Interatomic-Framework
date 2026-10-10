"""CI qualification for the structured FLiBe E(3) equivariance benchmark."""

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
    / "reference_equivariance.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-equivariance.v1"
)

_EXPECTED_TRANSFORMATIONS = (
    "translation",
    "rotation_z_90",
    "reflection_x",
    "cyclic_axis_rotation",
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

    decoded = result.stdout.decode("utf-8")
    report = json.loads(decoded)

    assert isinstance(report, dict)

    return report, result.stdout


def test_flibe_reference_equivariance_benchmark_exists() -> None:
    """The committed E(3) benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_reference_equivariance_benchmark_passes() -> None:
    """The benchmark must report PASS from an independent process."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_equivariance_benchmark_covers_declared_transformations() -> None:
    """The benchmark must retain its full E(3) transformation set."""

    report, _ = _run_benchmark()

    transformations = report["transformations"]

    assert isinstance(transformations, list)

    identifiers = tuple(
        entry["transformation_id"]
        for entry in transformations
    )

    assert identifiers == _EXPECTED_TRANSFORMATIONS


def test_every_equivariance_transformation_passes() -> None:
    """Every independently reported E(3) transformation must pass."""

    report, _ = _run_benchmark()

    transformations = report["transformations"]

    assert isinstance(transformations, list)
    assert transformations

    assert all(
        entry["status"] == "PASS"
        for entry in transformations
    )


def test_every_transformation_retains_required_checks() -> None:
    """Each transformation must verify geometry, resonance, energy, and forces."""

    report, _ = _run_benchmark()

    transformations = report["transformations"]

    assert isinstance(transformations, list)

    required = {
        "graph_edge_count_preserved",
        "resonance_coordinate_preserved",
        "energy_invariant",
        "forces_equivariant",
    }

    for entry in transformations:
        checks = entry["checks"]

        assert isinstance(checks, dict)
        assert set(checks) == required
        assert all(
            value is True
            for value in checks.values()
        )


def test_equivariance_benchmark_reports_finite_error_bounds() -> None:
    """Observed numerical errors must remain inside declared tolerances."""

    report, _ = _run_benchmark()

    energy_tolerance = report[
        "energy_absolute_tolerance"
    ]
    force_tolerance = report[
        "force_absolute_tolerance"
    ]

    assert isinstance(
        energy_tolerance,
        (int, float),
    )
    assert isinstance(
        force_tolerance,
        (int, float),
    )

    transformations = report["transformations"]

    assert isinstance(transformations, list)

    for entry in transformations:
        observed = entry["observed"]

        assert isinstance(observed, dict)

        energy_error = observed[
            "energy_absolute_error"
        ]
        force_error = observed[
            "force_max_absolute_error"
        ]

        assert energy_error >= 0.0
        assert force_error >= 0.0

        assert energy_error <= energy_tolerance
        assert force_error <= force_tolerance


def test_equivariance_benchmark_preserves_resonance_coordinate() -> None:
    """E(3) transformations must not modify the continuous resonance coordinate."""

    report, _ = _run_benchmark()

    reference = report["reference"]

    assert isinstance(reference, dict)

    reference_coordinate = reference[
        "resonance_coordinate"
    ]

    transformations = report["transformations"]

    assert isinstance(transformations, list)

    for entry in transformations:
        observed = entry["observed"]

        assert isinstance(observed, dict)

        assert (
            observed["resonance_coordinate"]
            == reference_coordinate
        )


def test_equivariance_benchmark_preserves_graph_edge_count() -> None:
    """Rigid E(3) transformations must preserve cutoff-graph cardinality."""

    report, _ = _run_benchmark()

    reference = report["reference"]

    assert isinstance(reference, dict)

    reference_edge_count = reference[
        "graph_edge_count"
    ]

    transformations = report["transformations"]

    assert isinstance(transformations, list)

    for entry in transformations:
        observed = entry["observed"]

        assert isinstance(observed, dict)

        assert (
            observed["graph_edge_count"]
            == reference_edge_count
        )


def test_equivariance_benchmark_output_is_byte_deterministic() -> None:
    """Independent executions must emit byte-identical structured JSON."""

    first_report, first_bytes = _run_benchmark()
    second_report, second_bytes = _run_benchmark()

    assert first_report == second_report
    assert first_bytes == second_bytes


def test_equivariance_benchmark_has_no_unstructured_stdout() -> None:
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
