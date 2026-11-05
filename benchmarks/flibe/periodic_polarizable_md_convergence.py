"""Fixed-duration velocity-Verlet convergence for periodic polarizable FLiBe.

The reference and refinement runs use one initial periodic configuration,
one source-registered interatomic parameter set, and identical Ewald kernels.
Each force evaluation relaxes the induced fluoride dipoles. Endpoint position
and velocity differences are measured against the declared finest-step run.
The energy-drift and momentum criteria are evaluated on every saved state.
The initial MD mass and velocity parameters carry TEST_FIXTURE provenance.
"""

from __future__ import annotations

import hashlib
import json
from math import fsum, isfinite, sqrt, ulp
from pathlib import Path

from tr_eif.configuration import AtomicConfiguration
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_md import (
    FLiBePeriodicMDRun,
    FLiBePeriodicMDUnits,
    run_flibe_periodic_velocity_verlet,
)
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_pair_coefficients import (
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.units import ParameterProvenance

BENCHMARK_ID = "tr-eif.flibe.periodic-polarizable-md-verlet-convergence.v1"
SOURCE_PATH = (Path(__file__).resolve().parents[2]
               / "data/reference/flibe_smith_2020_pim_pair_coefficients.json")
SOURCE_RELATIVE_PATH = "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
MODEL_ID = "FLIBE-PERIODIC-VERLET-CONVERGENCE-FIXTURE"

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS_BOHR = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
VELOCITIES_CODE = (
    (0.05, 0.01, 0.0), (-0.03, -0.01, 0.02),
    (0.02, 0.04, -0.03), (0.0, -0.025, 0.015),
    (0.01, 0.005, -0.035), (-0.02, 0.02, 0.0),
    (-0.02, -0.016, 0.021),
)
CELL_BOHR = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
MASSES_CODE = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
MASS_UNIT_TO_KG = 1.0e-27
BOHR_TO_METER = 5.29177210903e-11
HARTREE_TO_JOULE = 4.3597447222071e-18
TIME_UNIT_TO_SECOND = 1.0e-15

SCHEDULE = ((0.1, 4), (0.05, 8), (0.025, 16))
REFERENCE_SCHEDULE = (0.0125, 32)
TOTAL_TIME_CODE = 0.4
EWALD_ALPHA_INVERSE_BOHR = 0.25
EWALD_REAL_SHELL = 1
EWALD_RECIPROCAL_SHELL = 3
SHORT_RANGE_SHELL = 1
DAMPING_SHELL = 1
NEIGHBOR_CUTOFF_CODE = 4.0
STATIONARITY_TOLERANCE_ATOMIC = 1.0e-10

MINIMUM_REFINEMENT_ERROR_RATIO = 3.5
MAXIMUM_COARSE_ENERGY_DRIFT_HARTREE = 2.0e-8
MAXIMUM_FINE_POSITION_RMSE_BOHR = 2.0e-8
MAXIMUM_FINE_VELOCITY_RMSE_CODE = 5.0e-9
MAXIMUM_MOMENTUM_CHANGE_CODE = 1.0e-12
MAXIMUM_NET_FORCE_CODE = 1.0e-10
MAXIMUM_CLOCK_ROUNDOFF_CODE = 4.0 * REFERENCE_SCHEDULE[1] * ulp(TOTAL_TIME_CODE)


def _model() -> FLiBePeriodicPolarizableModel:
    source = load_flibe_registered_pair_parameters(SOURCE_PATH)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=EWALD_ALPHA_INVERSE_BOHR,
        real_image_shell=EWALD_REAL_SHELL,
        reciprocal_image_shell=EWALD_RECIPROCAL_SHELL,
        coordinate_unit_to_bohr=1.0,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="FLIBE-MD-CONVERGENCE-EWALD-FIXTURE",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-MD-CONVERGENCE-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-MD-CONVERGENCE-EWALD", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-MD-CONVERGENCE-SHORT-RANGE",
                parameters=source,
                coordinate_unit_to_bohr=1.0,
                image_shell=SHORT_RANGE_SHELL,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-MD-CONVERGENCE-POLARIZATION",
            parameters=source,
            ewald_parameters=ewald,
            damping_image_shell=DAMPING_SHELL,
            stationarity_absolute_tolerance=STATIONARITY_TOLERANCE_ATOMIC,
        ),
    )


def _initial_state() -> MolecularDynamicsState:
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=POSITIONS_BOHR,
            cell=CELL_BOHR,
            periodic=(True, True, True),
        ),
        velocities=VELOCITIES_CODE,
        masses=MASSES_CODE,
        step=0,
        time=0.0,
    )


def _units() -> FLiBePeriodicMDUnits:
    return FLiBePeriodicMDUnits(
        mass_unit_to_kg=MASS_UNIT_TO_KG,
        coordinate_unit_to_meter=BOHR_TO_METER,
        time_unit_to_second=TIME_UNIT_TO_SECOND,
        bohr_to_meter=BOHR_TO_METER,
        hartree_to_joule=HARTREE_TO_JOULE,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="FLIBE-MD-CONVERGENCE-UNITS-FIXTURE",
    )


def _run(model: FLiBePeriodicPolarizableModel, units: FLiBePeriodicMDUnits,
         schedule: tuple[float, int]) -> FLiBePeriodicMDRun:
    dt, steps = schedule
    return run_flibe_periodic_velocity_verlet(
        initial_state=_initial_state(),
        model=model,
        mass_parameters=FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        units=units,
        time_step=dt,
        step_count=steps,
        neighbor_cutoff=NEIGHBOR_CUTOFF_CODE,
    )


def _momentum(state: MolecularDynamicsState) -> tuple[float, float, float]:
    return tuple(fsum(mass * velocity[axis]
                      for mass, velocity in zip(state.masses, state.velocities, strict=True))
                 for axis in range(3))


def _end_point_rmse(first: FLiBePeriodicMDRun, second: FLiBePeriodicMDRun,
                    *, velocities: bool) -> float:
    a = first.trajectory.states[-1]
    b = second.trajectory.states[-1]
    x = a.velocities if velocities else a.configuration.positions
    y = b.velocities if velocities else b.configuration.positions
    return sqrt(fsum((u[k] - v[k])**2 for u, v in zip(x, y, strict=True)
                     for k in range(3)) / (3 * len(x)))


def _max_momentum_change(run: FLiBePeriodicMDRun) -> float:
    initial = _momentum(run.trajectory.initial)
    return max(abs(momentum[axis] - initial[axis])
               for state in run.trajectory.states
               for momentum in (_momentum(state),)
               for axis in range(3))


def _max_net_force(run: FLiBePeriodicMDRun) -> float:
    return max(abs(fsum(force[axis] for force in evaluation.forces.forces))
               for evaluation in run.evaluations for axis in range(3))


def _max_stationarity(run: FLiBePeriodicMDRun) -> float:
    return max(evaluation.max_stationarity_residual_atomic
               for evaluation in run.evaluations)


def run_benchmark() -> dict[str, object]:
    """Record matched-time convergence, conservation, and source provenance."""
    source_hash = hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest()
    model = _model()
    units = _units()
    reference = _run(model, units, REFERENCE_SCHEDULE)
    runs = tuple(_run(model, units, schedule) for schedule in SCHEDULE)

    entries = []
    for (dt, steps), run in zip(SCHEDULE, runs, strict=True):
        entries.append({
            "time_step_code": dt,
            "step_count": steps,
            "final_time_code": run.trajectory.states[-1].time,
            "position_rmse_to_fine_reference_bohr": _end_point_rmse(run, reference, velocities=False),
            "velocity_rmse_to_fine_reference_code": _end_point_rmse(run, reference, velocities=True),
            "maximum_absolute_energy_change_hartree": run.maximum_absolute_energy_change_hartree,
            "maximum_absolute_momentum_change_code": _max_momentum_change(run),
            "maximum_net_force_hartree_per_bohr": _max_net_force(run),
            "maximum_dipole_stationarity_residual_atomic": _max_stationarity(run),
            "final_total_energy_hartree": run.total_energies_hartree[-1],
            "source_file_sha256": run.source_file_sha256,
        })

    refinements = []
    for coarse, fine in zip(entries[:-1], entries[1:], strict=True):
        refinements.append({
            "coarse_time_step_code": coarse["time_step_code"],
            "fine_time_step_code": fine["time_step_code"],
            "position_error_reduction_ratio": (
                coarse["position_rmse_to_fine_reference_bohr"]
                / fine["position_rmse_to_fine_reference_bohr"]
            ),
            "velocity_error_reduction_ratio": (
                coarse["velocity_rmse_to_fine_reference_code"]
                / fine["velocity_rmse_to_fine_reference_code"]
            ),
            "energy_drift_reduction_ratio": (
                coarse["maximum_absolute_energy_change_hartree"]
                / fine["maximum_absolute_energy_change_hartree"]
            ),
        })

    final = entries[-1]
    checks = {
        "source_fingerprint": all(run.source_file_sha256 == source_hash
                                  for run in (*runs, reference)),
        "identical_start_states": all(run.trajectory.initial == reference.trajectory.initial
                                      for run in runs),
        "common_end_time": all(abs(run.trajectory.states[-1].time - TOTAL_TIME_CODE)
                               <= MAXIMUM_CLOCK_ROUNDOFF_CODE
                               for run in (*runs, reference)),
        "cell_and_composition_retained": all(
            state.configuration.cell == CELL_BOHR
            and state.configuration.periodic == (True, True, True)
            and state.configuration.species == SPECIES
            for run in (*runs, reference) for state in run.trajectory.states
        ),
        "stationary_dipoles": all(_max_stationarity(run) <= STATIONARITY_TOLERANCE_ATOMIC
                                  for run in (*runs, reference)),
        "momentum_conservation": all(_max_momentum_change(run) <= MAXIMUM_MOMENTUM_CHANGE_CODE
                                     for run in (*runs, reference)),
        "force_balance": all(_max_net_force(run) <= MAXIMUM_NET_FORCE_CODE
                             for run in (*runs, reference)),
        "energy_drift_bound": entries[0]["maximum_absolute_energy_change_hartree"]
                              <= MAXIMUM_COARSE_ENERGY_DRIFT_HARTREE,
        "position_refinement_order": all(
            r["position_error_reduction_ratio"] >= MINIMUM_REFINEMENT_ERROR_RATIO
            for r in refinements
        ),
        "velocity_refinement_order": all(
            r["velocity_error_reduction_ratio"] >= MINIMUM_REFINEMENT_ERROR_RATIO
            for r in refinements
        ),
        "energy_refinement_order": all(
            r["energy_drift_reduction_ratio"] >= MINIMUM_REFINEMENT_ERROR_RATIO
            for r in refinements
        ),
        "fine_position_error": final["position_rmse_to_fine_reference_bohr"]
                               <= MAXIMUM_FINE_POSITION_RMSE_BOHR,
        "fine_velocity_error": final["velocity_rmse_to_fine_reference_code"]
                               <= MAXIMUM_FINE_VELOCITY_RMSE_CODE,
        "deterministic_replay": runs[1] == _run(model, units, SCHEDULE[1]),
    }

    numeric = [entry[key] for entry in entries for key in (
        "position_rmse_to_fine_reference_bohr",
        "velocity_rmse_to_fine_reference_code",
        "maximum_absolute_energy_change_hartree",
        "maximum_absolute_momentum_change_code",
        "maximum_net_force_hartree_per_bohr",
        "maximum_dipole_stationarity_residual_atomic",
        "final_total_energy_hartree",
    )]
    numeric.extend(v for ratio in refinements
                   for k, v in ratio.items() if k.endswith("ratio"))
    checks["finite_numerical_results"] = all(isfinite(value) for value in numeric)

    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source": {
            "doi": SOURCE_DOI,
            "relative_path": SOURCE_RELATIVE_PATH,
            "file_sha256": source_hash,
            "provenance": "PRIMARY_SOURCE",
        },
        "fixture": {
            "provenance": "TEST_FIXTURE",
            "model_id": MODEL_ID,
            "species": list(SPECIES),
            "positions_bohr": [list(v) for v in POSITIONS_BOHR],
            "velocities_code": [list(v) for v in VELOCITIES_CODE],
            "masses_code": list(MASSES_CODE),
            "cell_bohr": [list(v) for v in CELL_BOHR],
            "units": {
                "mass_unit_to_kg": MASS_UNIT_TO_KG,
                "coordinate_unit_to_meter": BOHR_TO_METER,
                "time_unit_to_second": TIME_UNIT_TO_SECOND,
                "bohr_to_meter": BOHR_TO_METER,
                "hartree_to_joule": HARTREE_TO_JOULE,
            },
            "ewald": {
                "alpha_inverse_bohr": EWALD_ALPHA_INVERSE_BOHR,
                "real_image_shell": EWALD_REAL_SHELL,
                "reciprocal_image_shell": EWALD_RECIPROCAL_SHELL,
                "short_range_image_shell": SHORT_RANGE_SHELL,
                "charge_dipole_damping_image_shell": DAMPING_SHELL,
                "stationarity_absolute_tolerance": STATIONARITY_TOLERANCE_ATOMIC,
            },
            "neighbor_cutoff_code": NEIGHBOR_CUTOFF_CODE,
        },
        "numerical_contract": {
            "integrator": "velocity_verlet",
            "ensemble": "NVE_fixed_cell",
            "total_time_code": TOTAL_TIME_CODE,
            "step_schedules": [{"time_step_code": dt, "step_count": steps}
                               for dt, steps in SCHEDULE],
            "reference_schedule": {
                "time_step_code": REFERENCE_SCHEDULE[0],
                "step_count": REFERENCE_SCHEDULE[1],
            },
            "minimum_refinement_error_ratio": MINIMUM_REFINEMENT_ERROR_RATIO,
            "maximum_coarse_energy_drift_hartree": MAXIMUM_COARSE_ENERGY_DRIFT_HARTREE,
            "maximum_fine_position_rmse_bohr": MAXIMUM_FINE_POSITION_RMSE_BOHR,
            "maximum_fine_velocity_rmse_code": MAXIMUM_FINE_VELOCITY_RMSE_CODE,
            "maximum_momentum_change_code": MAXIMUM_MOMENTUM_CHANGE_CODE,
            "maximum_net_force_hartree_per_bohr": MAXIMUM_NET_FORCE_CODE,
            "maximum_clock_roundoff_code": MAXIMUM_CLOCK_ROUNDOFF_CODE,
        },
        "reference": {
            "final_total_energy_hartree": reference.total_energies_hartree[-1],
            "maximum_absolute_energy_change_hartree": reference.maximum_absolute_energy_change_hartree,
            "maximum_dipole_stationarity_residual_atomic": _max_stationarity(reference),
        },
        "runs": entries,
        "refinements": refinements,
        "checks": checks,
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if report["status"] == "PASS" else 1)
