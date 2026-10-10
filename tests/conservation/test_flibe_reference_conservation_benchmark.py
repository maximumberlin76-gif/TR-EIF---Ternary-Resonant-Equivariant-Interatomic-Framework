"""CI qualification for the structured FLiBe conservation benchmark."""

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
    / "reference_conservation.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-conservation.v1"
)

_EXPECTED_CHECKS = {
    "atom_count_preserved",
    "state_count",
    "step_count",
    "finite_energy_components",
    "kinetic_plus_potential_identity",
    "total_energy_drift_bounded",
    "resonance_coordinate_fixed",
    "retained_ternary_state_preserved",
    "no_pending_ternary_targets",
}


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


def test_flibe_reference_conservation_benchmark_exists() -> None:
    """The committed conservation benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_reference_conservation_benchmark_passes() -> None:
    """The benchmark must report PASS from an independent process."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_all_conservation_checks_pass() -> None:
    """Every structured conservation check must pass."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)
    assert set(checks) == _EXPECTED_CHECKS

    assert all(
        value is True
        for value in checks.values()
    )


def test_energy_series_have_expected_cardinality() -> None:
    """Kinetic, potential, and total energy series must align with state count."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    state_count = observed["state_count"]

    kinetic = observed["kinetic_energies"]
    potential = observed["potential_energies"]
    total = observed["total_energies"]

    assert isinstance(state_count, int)
    assert isinstance(kinetic, list)
    assert isinstance(potential, list)
    assert isinstance(total, list)

    assert len(kinetic) == state_count
    assert len(potential) == state_count
    assert len(total) == state_count


def test_reported_total_energy_identity_is_reproducible() -> None:
    """Every reported total must equal kinetic plus potential energy."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    kinetic = observed["kinetic_energies"]
    potential = observed["potential_energies"]
    total = observed["total_energies"]

    assert isinstance(kinetic, list)
    assert isinstance(potential, list)
    assert isinstance(total, list)

    tolerance = report[
        "energy_identity_absolute_tolerance"
    ]

    assert isinstance(
        tolerance,
        (int, float),
    )

    for kinetic_value, potential_value, total_value in zip(
        kinetic,
        potential,
        total,
        strict=True,
    ):
        assert abs(
            total_value
            - (
                kinetic_value
                + potential_value
            )
        ) <= tolerance


def test_reported_energy_drift_is_within_declared_tolerance() -> None:
    """Maximum observed total-energy drift must satisfy the benchmark bound."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    drift = observed[
        "max_absolute_energy_drift"
    ]
    tolerance = report[
        "energy_drift_absolute_tolerance"
    ]

    assert isinstance(
        drift,
        (int, float),
    )
    assert isinstance(
        tolerance,
        (int, float),
    )

    assert drift >= 0.0
    assert drift <= tolerance


def test_final_signed_drift_matches_reported_endpoint_energies() -> None:
    """Reported final drift must equal final minus initial total energy."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    initial = observed[
        "initial_total_energy"
    ]
    final = observed[
        "final_total_energy"
    ]
    drift = observed[
        "final_signed_energy_drift"
    ]

    assert drift == (
        final - initial
    )


def test_conservation_benchmark_preserves_ternary_execution_state() -> None:
    """MD conservation evaluation must retain the declared -1/0/1 state."""

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


def test_conservation_benchmark_retains_resonance_coordinate() -> None:
    """The frozen-resonance MD benchmark must retain its continuous coordinate."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    coordinate = observed[
        "resonance_coordinate"
    ]

    assert isinstance(coordinate, list)
    assert len(coordinate) == 2


def test_conservation_benchmark_output_is_byte_deterministic() -> None:
    """Independent executions must emit byte-identical structured JSON."""

    first_report, first_bytes = _run_benchmark()
    second_report, second_bytes = _run_benchmark()

    assert first_report == second_report
    assert first_bytes == second_bytes


def test_conservation_benchmark_has_no_unstructured_stdout() -> None:
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
