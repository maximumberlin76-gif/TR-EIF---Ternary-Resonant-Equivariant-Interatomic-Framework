"""CI qualification for the structured FLiBe numerical-convergence benchmark."""

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
    / "reference_numerical_convergence.py"
)

_EXPECTED_BENCHMARK_ID = (
    "tr-eif.flibe.reference-numerical-convergence.v1"
)

_EXPECTED_CHECKS = {
    "finite_errors",
    "strict_error_reduction",
    "second_order_reduction",
    "final_error_bounded",
    "resonance_coordinate_fixed",
    "retained_ternary_state_preserved",
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


def test_flibe_numerical_convergence_benchmark_exists() -> None:
    """The committed numerical-convergence benchmark must remain present."""

    assert _BENCHMARK_PATH.is_file()


def test_flibe_numerical_convergence_benchmark_passes() -> None:
    """The benchmark must report PASS from an independent process."""

    report, _ = _run_benchmark()

    assert report["benchmark_id"] == _EXPECTED_BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["status"] == "PASS"


def test_all_numerical_convergence_checks_pass() -> None:
    """Every structured numerical-convergence check must pass."""

    report, _ = _run_benchmark()

    checks = report["checks"]

    assert isinstance(checks, dict)
    assert set(checks) == _EXPECTED_CHECKS

    assert all(
        value is True
        for value in checks.values()
    )


def test_convergence_steps_are_strictly_decreasing() -> None:
    """Differentiation steps must form the declared refinement sequence."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    steps = observed["steps"]

    assert isinstance(steps, list)
    assert len(steps) >= 2

    step_values = tuple(
        entry["step"]
        for entry in steps
    )

    assert all(
        current < previous
        for previous, current in zip(
            step_values[:-1],
            step_values[1:],
            strict=True,
        )
    )


def test_force_error_decreases_under_refinement() -> None:
    """Force-component error must decrease at every refinement step."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    steps = observed["steps"]

    assert isinstance(steps, list)

    errors = tuple(
        entry["max_force_component_error"]
        for entry in steps
    )

    assert all(
        error >= 0.0
        for error in errors
    )

    assert all(
        current < previous
        for previous, current in zip(
            errors[:-1],
            errors[1:],
            strict=True,
        )
    )


def test_error_reduction_satisfies_declared_second_order_bound() -> None:
    """Observed refinement ratios must satisfy the benchmark convergence bound."""

    report, _ = _run_benchmark()

    minimum_ratio = report[
        "minimum_error_reduction_ratio"
    ]

    observed = report["observed"]

    assert isinstance(observed, dict)

    ratios = observed[
        "error_reduction_ratios"
    ]

    assert isinstance(
        minimum_ratio,
        (int, float),
    )
    assert isinstance(ratios, list)
    assert ratios

    assert all(
        ratio >= minimum_ratio
        for ratio in ratios
    )


def test_final_force_error_satisfies_declared_tolerance() -> None:
    """The finest reported force estimate must satisfy the absolute error bound."""

    report, _ = _run_benchmark()

    tolerance = report[
        "final_error_tolerance"
    ]

    observed = report["observed"]

    assert isinstance(observed, dict)

    steps = observed["steps"]

    assert isinstance(steps, list)
    assert steps

    final_error = steps[-1][
        "max_force_component_error"
    ]

    assert isinstance(
        tolerance,
        (int, float),
    )
    assert isinstance(
        final_error,
        (int, float),
    )

    assert final_error <= tolerance


def test_reference_step_is_finer_than_convergence_steps() -> None:
    """The reference differentiation step must be finer than sampled steps."""

    report, _ = _run_benchmark()

    reference_step = report[
        "reference_step"
    ]

    observed = report["observed"]

    assert isinstance(observed, dict)

    steps = observed["steps"]

    assert isinstance(steps, list)
    assert steps

    assert all(
        reference_step < entry["step"]
        for entry in steps
    )


def test_convergence_benchmark_preserves_resonance_coordinate() -> None:
    """Numerical refinement must not alter the continuous resonance state."""

    report, _ = _run_benchmark()

    observed = report["observed"]

    assert isinstance(observed, dict)

    coordinate = observed[
        "resonance_coordinate"
    ]

    assert isinstance(coordinate, list)
    assert len(coordinate) == 2


def test_convergence_benchmark_preserves_ternary_execution_state() -> None:
    """Numerical refinement must retain the declared balanced -1/0/1 state."""

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


def test_convergence_benchmark_output_is_byte_deterministic() -> None:
    """Independent executions must emit byte-identical structured JSON."""

    first_report, first_bytes = _run_benchmark()
    second_report, second_bytes = _run_benchmark()

    assert first_report == second_report
    assert first_bytes == second_bytes


def test_convergence_benchmark_has_no_unstructured_stdout() -> None:
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
