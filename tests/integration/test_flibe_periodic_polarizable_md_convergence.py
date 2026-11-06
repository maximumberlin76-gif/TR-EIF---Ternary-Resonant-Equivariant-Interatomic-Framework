"""Independent numerical and provenance contracts for FLiBe MD convergence."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from math import fsum, isclose, isfinite, ulp
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_polarizable_md_convergence.py"
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-polarizable-md-verlet-convergence.v1"
SOURCE_ID = "tr-eif.flibe.smith-2020.pim-pair-coefficients.v1"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
MODEL_ID = "FLIBE-PERIODIC-VERLET-CONVERGENCE-FIXTURE"

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
POSITIONS = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
VELOCITIES = (
    (0.05, 0.01, 0.0), (-0.03, -0.01, 0.02),
    (0.02, 0.04, -0.03), (0.0, -0.025, 0.015),
    (0.01, 0.005, -0.035), (-0.02, 0.02, 0.0),
    (-0.02, -0.016, 0.021),
)
CELL = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
SCHEDULE = ((0.1, 4), (0.05, 8), (0.025, 16))
REFERENCE_SCHEDULE = (0.0125, 32)
TOTAL_TIME = 0.4
CLOCK_TOL = 4.0 * 32 * ulp(TOTAL_TIME)
MINIMUM_ERROR_REDUCTION = 3.5
MAX_COARSE_DRIFT = 2.0e-8
MAX_FINE_POSITION_ERROR = 2.0e-8
MAX_FINE_VELOCITY_ERROR = 5.0e-9
MAX_MOMENTUM_CHANGE = 1.0e-12
MAX_NET_FORCE = 1.0e-10
MAX_STATIONARITY = 1.0e-10

CHECK_NAMES = {
    "source_fingerprint",
    "identical_start_states",
    "common_end_time",
    "cell_and_composition_retained",
    "stationary_dipoles",
    "momentum_conservation",
    "force_balance",
    "energy_drift_bound",
    "position_refinement_order",
    "velocity_refinement_order",
    "energy_refinement_order",
    "fine_position_error",
    "fine_velocity_error",
    "deterministic_replay",
    "finite_numerical_results",
}


def _number(value: object, *, nonnegative: bool = False) -> float:
    assert type(value) in (int, float)
    number = float(value)
    assert isfinite(number)
    if nonnegative:
        assert number >= 0.0
    return number


def _execute() -> tuple[dict[str, object], bytes]:
    """Execute the committed benchmark through a separate Python process."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT / "src"), environment.get("PYTHONPATH", "")) if part
    )
    completed = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        check=False,
        timeout=420,
    )
    assert completed.returncode == 0, (
        completed.stderr.decode("utf-8", errors="replace")
        + completed.stdout.decode("utf-8", errors="replace")[-2000:]
    )
    assert completed.stderr == b""
    document = json.loads(completed.stdout)
    assert isinstance(document, dict)
    return document, completed.stdout


@pytest.fixture(scope="module")
def executions() -> tuple[tuple[dict[str, object], bytes], ...]:
    return _execute(), _execute()


@pytest.fixture(scope="module")
def report(executions) -> dict[str, object]:
    return executions[0][0]


def _expect_ratio_records(document: dict[str, object]) -> None:
    """Recalculate every reported refinement ratio from the raw run metrics."""
    runs = document["runs"]
    refinements = document["refinements"]
    assert len(runs) == 3 and len(refinements) == 2
    keys = (
        ("position_rmse_to_fine_reference_bohr", "position_error_reduction_ratio"),
        ("velocity_rmse_to_fine_reference_code", "velocity_error_reduction_ratio"),
        ("maximum_absolute_energy_change_hartree", "energy_drift_reduction_ratio"),
    )
    for index, refinement in enumerate(refinements):
        coarse, fine = runs[index], runs[index + 1]
        assert refinement["coarse_time_step_code"] == SCHEDULE[index][0]
        assert refinement["fine_time_step_code"] == SCHEDULE[index + 1][0]
        for error_key, ratio_key in keys:
            coarse_error = _number(coarse[error_key], nonnegative=True)
            fine_error = _number(fine[error_key], nonnegative=True)
            assert fine_error > 0.0
            ratio = coarse_error / fine_error
            assert _number(refinement[ratio_key]) == pytest.approx(ratio, rel=1e-12)
            assert ratio >= MINIMUM_ERROR_REDUCTION


def test_source_fingerprint_and_dataset_metadata(report) -> None:
    assert BENCHMARK.is_file()
    assert SOURCE.is_file()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert source["dataset_id"] == SOURCE_ID
    assert source["source"]["doi"] == SOURCE_DOI
    assert source["record_kind"] == "PUBLISHED_INTERATOMIC_PARAMETER_TABLE"
    assert source["provenance"] == "PRIMARY_SOURCE"
    assert len(source["pair_coefficients"]) == 6
    assert report["source"] == {
        "doi": SOURCE_DOI,
        "relative_path": "data/reference/flibe_smith_2020_pim_pair_coefficients.json",
        "file_sha256": digest,
        "provenance": "PRIMARY_SOURCE",
    }
    assert all(entry["source_file_sha256"] == digest for entry in report["runs"])


def test_benchmark_identity_and_all_fifteen_qualification_gates(report) -> None:
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert set(report["checks"]) == CHECK_NAMES
    assert all(flag is True for flag in report["checks"].values())


def test_fixed_atomic_fixture_and_physical_composition(report) -> None:
    fixture = report["fixture"]
    assert fixture["provenance"] == "TEST_FIXTURE"
    assert fixture["model_id"] == MODEL_ID
    assert fixture["species"] == list(SPECIES)
    assert fixture["positions_bohr"] == [list(row) for row in POSITIONS]
    assert fixture["velocities_code"] == [list(row) for row in VELOCITIES]
    assert fixture["masses_code"] == list(MASSES)
    assert fixture["cell_bohr"] == [list(row) for row in CELL]
    assert sum(MASSES) == 27.0
    assert (SPECIES.count("Li"), SPECIES.count("Be"), SPECIES.count("F")) == (2, 1, 4)
    assert 2 * 1 + 1 * 2 + 4 * (-1) == 0
    momentum = tuple(fsum(m * v[a] for m, v in zip(MASSES, VELOCITIES, strict=True))
                     for a in range(3))
    assert momentum == pytest.approx((-0.05, 0.04, -0.045), abs=1e-15)


def test_units_and_source_resolved_numerical_settings(report) -> None:
    fixture = report["fixture"]
    assert fixture["units"] == {
        "mass_unit_to_kg": 1.0e-27,
        "coordinate_unit_to_meter": 5.29177210903e-11,
        "time_unit_to_second": 1.0e-15,
        "bohr_to_meter": 5.29177210903e-11,
        "hartree_to_joule": 4.3597447222071e-18,
    }
    assert fixture["ewald"] == {
        "alpha_inverse_bohr": 0.25,
        "real_image_shell": 1,
        "reciprocal_image_shell": 3,
        "short_range_image_shell": 1,
        "charge_dipole_damping_image_shell": 1,
        "stationarity_absolute_tolerance": MAX_STATIONARITY,
    }
    assert fixture["neighbor_cutoff_code"] == 4.0
    units = fixture["units"]
    kinetic = units["mass_unit_to_kg"] * (
        units["coordinate_unit_to_meter"] / units["time_unit_to_second"]
    )**2 / units["hartree_to_joule"]
    acceleration = units["hartree_to_joule"] * units["time_unit_to_second"]**2 / (
        units["mass_unit_to_kg"] * units["coordinate_unit_to_meter"]**2
    )
    assert kinetic * acceleration == pytest.approx(1.0, rel=1e-13)


def test_common_physical_interval_and_fixed_refinement_schedule(report) -> None:
    contract = report["numerical_contract"]
    assert contract["integrator"] == "velocity_verlet"
    assert contract["ensemble"] == "NVE_fixed_cell"
    assert contract["total_time_code"] == TOTAL_TIME
    assert contract["step_schedules"] == [
        {"time_step_code": dt, "step_count": steps} for dt, steps in SCHEDULE
    ]
    assert contract["reference_schedule"] == {
        "time_step_code": REFERENCE_SCHEDULE[0],
        "step_count": REFERENCE_SCHEDULE[1],
    }
    assert contract["maximum_clock_roundoff_code"] == CLOCK_TOL
    for entry, (dt, steps) in zip(report["runs"], SCHEDULE, strict=True):
        assert entry["time_step_code"] == dt
        assert entry["step_count"] == steps
        assert dt * steps == pytest.approx(TOTAL_TIME, rel=0.0, abs=CLOCK_TOL)
        assert abs(_number(entry["final_time_code"]) - TOTAL_TIME) <= CLOCK_TOL
    assert REFERENCE_SCHEDULE[0] * REFERENCE_SCHEDULE[1] == TOTAL_TIME


def test_predeclared_accuracy_conservation_and_clock_limits(report) -> None:
    contract = report["numerical_contract"]
    assert contract["minimum_refinement_error_ratio"] == MINIMUM_ERROR_REDUCTION
    assert contract["maximum_coarse_energy_drift_hartree"] == MAX_COARSE_DRIFT
    assert contract["maximum_fine_position_rmse_bohr"] == MAX_FINE_POSITION_ERROR
    assert contract["maximum_fine_velocity_rmse_code"] == MAX_FINE_VELOCITY_ERROR
    assert contract["maximum_momentum_change_code"] == MAX_MOMENTUM_CHANGE
    assert contract["maximum_net_force_hartree_per_bohr"] == MAX_NET_FORCE
    assert contract["maximum_clock_roundoff_code"] == CLOCK_TOL
    assert _number(report["runs"][0]["maximum_absolute_energy_change_hartree"], nonnegative=True) <= MAX_COARSE_DRIFT
    assert _number(report["runs"][-1]["position_rmse_to_fine_reference_bohr"], nonnegative=True) <= MAX_FINE_POSITION_ERROR
    assert _number(report["runs"][-1]["velocity_rmse_to_fine_reference_code"], nonnegative=True) <= MAX_FINE_VELOCITY_ERROR


def test_every_run_preserves_momentum_force_balance_and_stationarity(report) -> None:
    for entry in report["runs"]:
        assert _number(entry["maximum_absolute_momentum_change_code"], nonnegative=True) <= MAX_MOMENTUM_CHANGE
        assert _number(entry["maximum_net_force_hartree_per_bohr"], nonnegative=True) <= MAX_NET_FORCE
        assert _number(entry["maximum_dipole_stationarity_residual_atomic"], nonnegative=True) <= MAX_STATIONARITY
        assert isfinite(_number(entry["final_total_energy_hartree"]))
    reference = report["reference"]
    assert isfinite(_number(reference["final_total_energy_hartree"]))
    assert _number(reference["maximum_dipole_stationarity_residual_atomic"], nonnegative=True) <= MAX_STATIONARITY
    assert _number(reference["maximum_absolute_energy_change_hartree"], nonnegative=True) <= (
        report["runs"][-1]["maximum_absolute_energy_change_hartree"]
    )


def test_independently_recomputed_convergence_ratios(report) -> None:
    _expect_ratio_records(report)
    assert [row["time_step_code"] for row in report["runs"]] == [0.1, 0.05, 0.025]
    for name in (
        "position_rmse_to_fine_reference_bohr",
        "velocity_rmse_to_fine_reference_code",
        "maximum_absolute_energy_change_hartree",
    ):
        measured = [_number(row[name], nonnegative=True) for row in report["runs"]]
        assert measured[0] > measured[1] > measured[2] > 0.0


def test_refinement_qualification_detects_corrupted_reported_metrics(report) -> None:
    changed = copy.deepcopy(report)
    changed["runs"][1]["position_rmse_to_fine_reference_bohr"] *= 2.0
    with pytest.raises(AssertionError):
        _expect_ratio_records(changed)
    changed = copy.deepcopy(report)
    changed["refinements"][0]["energy_drift_reduction_ratio"] *= 1.1
    with pytest.raises(AssertionError):
        _expect_ratio_records(changed)


def test_stdout_is_canonical_and_byte_deterministic(executions) -> None:
    (first, first_raw), (second, second_raw) = executions
    assert first == second
    assert first_raw == second_raw
    assert first_raw.decode("utf-8") == json.dumps(
        first, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"


def test_initial_and_saved_md_energies_from_independent_mechanical_sums(report) -> None:
    """Recompute a short MD trajectory directly from saved states and forces."""
    spec = importlib.util.spec_from_file_location("flibe_md_convergence_benchmark", BENCHMARK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    direct = module._run(module._model(), module._units(), SCHEDULE[0])
    states = direct.trajectory.states
    assert len(states) == SCHEDULE[0][1] + 1
    initial = states[0]
    assert initial.configuration.species == SPECIES
    assert initial.masses == MASSES
    assert initial.velocities == VELOCITIES
    kinetic_factor = (1.0e-27 * (5.29177210903e-11 / 1.0e-15)**2
                      / 4.3597447222071e-18)
    initial_kinetic_code = 0.5 * fsum(
        mass * fsum(component**2 for component in velocity)
        for mass, velocity in zip(MASSES, VELOCITIES, strict=True)
    )
    assert initial_kinetic_code == pytest.approx(0.0185925, rel=1e-14)
    assert direct.kinetic_energies_hartree[0] == pytest.approx(
        initial_kinetic_code * kinetic_factor, rel=1e-13
    )
    first_energy = direct.total_energies_hartree[0]
    maximum_drift = 0.0
    maximum_momentum_change = 0.0
    maximum_net_force = 0.0
    maximum_stationarity = 0.0
    initial_momentum = tuple(fsum(m*v[a] for m, v in zip(initial.masses, initial.velocities, strict=True))
                             for a in range(3))
    for state, evaluation, kinetic, total in zip(
        states, direct.evaluations, direct.kinetic_energies_hartree,
        direct.total_energies_hartree, strict=True,
    ):
        independent_kinetic = 0.5 * fsum(
            m * fsum(v*v for v in velocity)
            for m, velocity in zip(state.masses, state.velocities, strict=True)
        ) * kinetic_factor
        assert kinetic == pytest.approx(independent_kinetic, rel=1e-12, abs=1e-14)
        assert total == pytest.approx(kinetic + evaluation.energy.total_energy, rel=1e-12)
        maximum_drift = max(maximum_drift, abs(total - first_energy))
        momentum = tuple(fsum(m*v[a] for m, v in zip(state.masses, state.velocities, strict=True))
                         for a in range(3))
        maximum_momentum_change = max(maximum_momentum_change, *(
            abs(momentum[a] - initial_momentum[a]) for a in range(3)
        ))
        maximum_net_force = max(maximum_net_force, *(
            abs(fsum(force[a] for force in evaluation.forces.forces)) for a in range(3)
        ))
        maximum_stationarity = max(
            maximum_stationarity, evaluation.max_stationarity_residual_atomic
        )
    observed = report["runs"][0]
    assert observed["maximum_absolute_energy_change_hartree"] == pytest.approx(maximum_drift, abs=1e-14)
    assert observed["maximum_absolute_momentum_change_code"] == pytest.approx(maximum_momentum_change, abs=1e-14)
    assert observed["maximum_net_force_hartree_per_bohr"] == pytest.approx(maximum_net_force, abs=1e-14)
    assert observed["maximum_dipole_stationarity_residual_atomic"] == pytest.approx(maximum_stationarity, abs=1e-14)
    assert direct.source_file_sha256 == report["source"]["file_sha256"]
