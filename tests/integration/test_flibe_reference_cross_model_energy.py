"""Independent numerical qualification of the FLiBe paired energy benchmark."""

from __future__ import annotations

import json
import os
from math import fsum, isfinite, sqrt
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/reference_cross_model_energy.py"
BENCHMARK_ID = "tr-eif.flibe.reference-cross-model-energy.v1"
BASELINE_ID = "REFERENCE-ONE-CHANNEL"
CONDITIONED_ID = "TR-EIP-RESONANCE-THREE-CHANNEL"
ENERGY_TOL = 1.0e-10
FORCE_TOL = 2.0e-6

# Independent seven-atom input fixture, in the benchmark's Cartesian units.
POSITIONS = (
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0),
    (1.1, 0.7, 0.8),
    (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
SCALARS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
CONDITIONING = (0.5, 1.25, 1.5, 1.25, 0.5, 1.5, 1.25)
CUTOFF_SQUARED = 1.6**2
DISTANCE_SCALE_SQUARED = 1.1**2

# Seven phases at multiples of pi/4 give R=1/7; the frequency spread is 0.2.
RESONANCE_INCREMENT = 0.7 * (1.0 / 7.0) - 0.3 * 0.2

EXPECTED_CHECKS = {
    "exact_composition",
    "directed_graph",
    "retained_ternary_alphabet",
    "baseline_analytical_energy",
    "tr_eip_analytical_energy",
    "total_baseline_sum",
    "total_tr_eip_sum",
    "signed_model_delta",
    "baseline_replay",
    "tr_eip_replay",
    "baseline_e3_invariance",
    "tr_eip_e3_invariance",
    "baseline_analytical_forces",
    "tr_eip_analytical_forces",
    "baseline_force_replay",
    "tr_eip_force_replay",
    "baseline_e3_force_covariance",
    "tr_eip_e3_force_covariance",
    "baseline_net_force_balance",
    "tr_eip_net_force_balance",
}


def _execute() -> tuple[dict[str, object], bytes]:
    """Execute the committed benchmark in a separate Python interpreter."""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT / "src"), env.get("PYTHONPATH", "")) if part
    )
    result = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert result.stderr == b""
    report = json.loads(result.stdout)
    assert isinstance(report, dict)
    return report, result.stdout


@pytest.fixture(scope="module")
def report() -> dict[str, object]:
    return _execute()[0]


def _analytic_expected():
    """Integrate the stated radial pair law without benchmark helper functions."""
    atom_count = len(POSITIONS)
    energies = [[0.1 + 0.4 * CONDITIONING[j] * SCALARS[j]
                 for j in range(atom_count)] for _ in range(2)]
    for j in range(atom_count):
        energies[1][j] += RESONANCE_INCREMENT * CONDITIONING[j]
    forces = [[[0.0, 0.0, 0.0] for _ in range(atom_count)] for _ in range(2)]
    directed_edges = 0
    for i in range(atom_count):
        for j in range(i + 1, atom_count):
            displacement = tuple(POSITIONS[i][a] - POSITIONS[j][a] for a in range(3))
            separation_squared = fsum(d * d for d in displacement)
            if separation_squared > CUTOFF_SQUARED:
                continue
            directed_edges += 2
            denominator = 1.0 + separation_squared / DISTANCE_SCALE_SQUARED
            radial = 1.0 / denominator
            for model_index in range(2):
                extra = RESONANCE_INCREMENT if model_index else 0.0
                source_i = CONDITIONING[i] * (0.4 * SCALARS[i] + extra)
                source_j = CONDITIONING[j] * (0.4 * SCALARS[j] + extra)
                energies[model_index][i] += radial * source_j
                energies[model_index][j] += radial * source_i
                gradient_factor = (2.0 * (source_i + source_j)
                                   / (DISTANCE_SCALE_SQUARED * denominator**2))
                for axis in range(3):
                    force = gradient_factor * displacement[axis]
                    forces[model_index][i][axis] += force
                    forces[model_index][j][axis] -= force
    return energies, forces, directed_edges


def _assert_vectors(actual: object, expected: list[list[float]]) -> None:
    assert isinstance(actual, list) and len(actual) == len(expected) == 7
    for reported, analytic in zip(actual, expected, strict=True):
        assert isinstance(reported, list) and len(reported) == 3
        assert all(isinstance(value, (int, float)) and not isinstance(value, bool)
                   and isfinite(value) for value in reported)
        assert reported == pytest.approx(analytic, rel=0.0, abs=FORCE_TOL)


def test_benchmark_is_committed_and_executable(report: dict[str, object]) -> None:
    assert BENCHMARK.is_file()
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert report["comparison_kind"] == "reference_baseline_vs_resonance_conditioned_tr_eip"
    assert report["reference_state_id"] == "FLIBE-7-ATOM-ANALYTIC-FIXTURE"
    assert report["provenance"] == "TEST_FIXTURE"


def test_all_declared_energy_and_force_checks_are_executed(report: dict[str, object]) -> None:
    checks = report["checks"]
    assert isinstance(checks, dict)
    assert set(checks) == EXPECTED_CHECKS
    assert all(value is True for value in checks.values())


def test_composition_resonance_and_ternary_fixture_are_preserved(report: dict[str, object]) -> None:
    state = report["declared_fixture_state"]
    assert state["atom_count"] == 7
    assert state["composition"] == {
        "lif_fraction": 2.0 / 3.0, "bef2_fraction": 1.0 / 3.0
    }
    assert state["temperature_k"] == 1000.0
    assert state["pressure_pa"] == 0.0
    assert state["retained_execution"] == [-1, 0, 1, 0, -1, 1, 0]
    assert state["resonance"]["phase_order"] == pytest.approx(1.0 / 7.0, abs=1e-14)
    assert state["resonance"]["frequency_spread"] == pytest.approx(0.2, abs=1e-14)
    assert state["directed_edge_count"] == _analytic_expected()[2] == 38


def test_two_model_configs_and_units_are_explicit(report: dict[str, object]) -> None:
    models = report["models"]
    assert set(models) == {BASELINE_ID, CONDITIONED_ID}
    assert models[BASELINE_ID]["type"] == "ReferenceEnergyModel"
    assert models[BASELINE_ID]["base_scalar_weights"] == [0.4]
    assert models[CONDITIONED_ID]["type"] == "FLiBeTREIPModel"
    assert models[CONDITIONED_ID]["base_and_resonance_weights"] == [0.4, 0.7, -0.3]
    contract = report["numeric_contract"]
    assert contract == {
        "energy_absolute_tolerance": ENERGY_TOL,
        "force_absolute_tolerance": FORCE_TOL,
        "force_derivative_step": 1.0e-6,
        "energy_unit": "model-native-energy",
        "force_unit": "model-native-energy-per-coordinate",
    }


@pytest.mark.parametrize("model_index,model_id", [(0, BASELINE_ID), (1, CONDITIONED_ID)])
def test_atomic_energies_match_independent_radial_sum(
    report: dict[str, object], model_index: int, model_id: str
) -> None:
    expected, _, _ = _analytic_expected()
    observed = report["models"][model_id]["atomic_energy"]
    assert len(observed) == len(expected[model_index])
    assert all(isfinite(value) for value in observed)
    assert observed == pytest.approx(expected[model_index], rel=0.0, abs=ENERGY_TOL)
    assert report["models"][model_id]["total_energy"] == pytest.approx(
        fsum(expected[model_index]), rel=0.0, abs=ENERGY_TOL
    )


@pytest.mark.parametrize("model_index,model_id", [(0, BASELINE_ID), (1, CONDITIONED_ID)])
def test_forces_match_independent_pair_gradient(
    report: dict[str, object], model_index: int, model_id: str
) -> None:
    _, force_reference, _ = _analytic_expected()
    _assert_vectors(report["models"][model_id]["cartesian_forces"],
                    force_reference[model_index])


def test_fixed_energy_anchors_and_signed_conditioning_difference(report: dict[str, object]) -> None:
    a = report["models"][BASELINE_ID]["total_energy"]
    b = report["models"][CONDITIONED_ID]["total_energy"]
    assert a == pytest.approx(15.21885682072469, rel=0.0, abs=ENERGY_TOL)
    assert b == pytest.approx(16.351564118122567, rel=0.0, abs=ENERGY_TOL)
    assert b - a == pytest.approx(1.132707297397877, rel=0.0, abs=ENERGY_TOL)
    assert report["signed_energy_difference"] == pytest.approx(b - a, abs=ENERGY_TOL)
    assert report["analytical_energy_difference"] == pytest.approx(b - a, abs=ENERGY_TOL)


@pytest.mark.parametrize("model_id", [BASELINE_ID, CONDITIONED_ID])
def test_net_cartesian_force_is_balanced(report: dict[str, object], model_id: str) -> None:
    forces = report["models"][model_id]["cartesian_forces"]
    assert len(forces) == len(POSITIONS)
    for component in range(3):
        assert abs(fsum(force[component] for force in forces)) <= FORCE_TOL


def test_benchmark_stdout_is_canonical_and_deterministic() -> None:
    first, raw_first = _execute()
    second, raw_second = _execute()
    assert first == second
    assert raw_first == raw_second
    assert raw_first.decode("utf-8") == json.dumps(first, indent=2, sort_keys=True) + "\n"
