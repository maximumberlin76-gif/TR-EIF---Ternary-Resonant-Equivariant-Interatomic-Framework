
"""Replica-count and duration diagnostics from periodic polarizable FLiBe MD.

Four independently initialized Li2BeF4 NVE trajectories use the same cell,
registered potential, mass inventory and initial COM kinetic temperature.
Velocity perturbations are fixed before execution and recorded with SHA-256
initial-condition fingerprints. Each trajectory supplies temperature, signed
pressure and density at the same physical sampling times. An existing
replica-duration operator computes the duration-by-replica-count matrix.

The output separately records arithmetic acceptance and sampling diagnostics:
distinct initial conditions establish input provenance; finite short NVE runs
are evaluated for duration sensitivity and inter-run dispersion.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from math import fsum, isclose, isfinite, sqrt
from pathlib import Path
from statistics import mean, stdev

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import CellStrainDifferentiation
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.mass import FLiBeMassParameters, configuration_masses
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_md import FLiBePeriodicMDUnits, run_flibe_periodic_velocity_verlet
from tr_eif.flibe.periodic_polarizable_stress import evaluate_flibe_periodic_polarizable_stress
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_pair_coefficients import SOURCE_DOI, load_flibe_registered_pair_parameters
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_frame_thermodynamics import evaluate_flibe_frame_thermodynamics
from tr_eif.flibe.trajectory_pressure import (
    FLiBePotentialStressSample, FLiBeVelocityFrame, evaluate_flibe_trajectory_pressure,
)
from tr_eif.flibe.trajectory_replica_convergence import (
    FLiBeReplicaThermodynamicTrace,
    evaluate_flibe_trajectory_replica_convergence,
)
from tr_eif.flibe.trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.md.state import MolecularDynamicsState

ROOT = Path(__file__).resolve().parents[2]
PAIR_PATH = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SOURCE_RELATIVE = "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-replica-duration-convergence.v1"
MODEL_ID = "FLIBE-PERIODIC-REPLICA-DURATION-BENCHMARK"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
CELL_EDGE_BOHR = 10.0
CELL = (
    (CELL_EDGE_BOHR, 0.0, 0.0),
    (0.0, CELL_EDGE_BOHR, 0.0),
    (0.0, 0.0, CELL_EDGE_BOHR),
)
BASE_EDGE_BOHR = 18.0
BASE_POSITIONS = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
VELOCITY_PATTERN = (
    (0.03, 0.01, 0.0), (-0.03, -0.01, 0.02), (0.02, 0.03, -0.02),
    (0.0, -0.02, 0.01), (0.01, 0.005, -0.02),
    (-0.015, 0.02, 0.0), (-0.015, -0.015, 0.01),
)
MASSES = FLiBeMassParameters(lithium=6.94, beryllium=9.0121831, fluorine=18.998403163)
PROVENANCE = ParameterProvenance.BENCHMARK
U_TO_KG = 1.66053906660e-27
BOHR_TO_M = 5.29177210903e-11
HARTREE_TO_J = 4.3597447222071e-18
TIME_TO_S = 1.0e-15
TEMPERATURE_K = 850.0
TIME_STEP = 0.01
STEPS = 16
SAMPLE_STRIDE = 2
REPLICA_COUNT = 4
DISCARD_INITIAL_SAMPLES = 1
BLOCK_SIZE = 2
RETAINED_LENGTHS = (4, 6, 8)
STRAIN_STEP = 2.0e-5
DIPOLE_TOLERANCE = 1.0e-10
CORRELATION_SCREEN_LIMIT = 0.5
DURATION_SHIFT_SE_LIMIT = 1.0


def _model() -> FLiBePeriodicPolarizableModel:
    parameters = load_flibe_registered_pair_parameters(PAIR_PATH)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25, real_image_shell=1, reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0, provenance=PROVENANCE,
        source_id="FLIBE-REPLICA-DURATION-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-REPLICA-DURATION-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-REPLICA-DURATION-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-REPLICA-DURATION-SHORT", parameters=parameters,
                coordinate_unit_to_bohr=1.0, image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-REPLICA-DURATION-DIPOLES", parameters=parameters,
            ewald_parameters=ewald, damping_image_shell=1,
            stationarity_absolute_tolerance=DIPOLE_TOLERANCE,
        ),
    )


def _units() -> FLiBePeriodicMDUnits:
    return FLiBePeriodicMDUnits(
        mass_unit_to_kg=U_TO_KG, coordinate_unit_to_meter=BOHR_TO_M,
        time_unit_to_second=TIME_TO_S, bohr_to_meter=BOHR_TO_M,
        hartree_to_joule=HARTREE_TO_J, provenance=PROVENANCE,
        source_id="FLIBE-REPLICA-DURATION-SI",
    )


def _initial_state(replica_index: int) -> MolecularDynamicsState:
    if not 0 <= replica_index < REPLICA_COUNT:
        raise ValueError("replica index outside declared matrix")
    atomic = AtomicConfiguration(
        species=SPECIES,
        positions=tuple(
            tuple(CELL_EDGE_BOHR / BASE_EDGE_BOHR * x for x in row)
            for row in BASE_POSITIONS
        ),
        cell=CELL, periodic=(True, True, True),
    )
    masses = configuration_masses(FLiBeConfiguration(atomic), MASSES)
    varied = tuple(
        (
            base[0] + 0.0010 * replica_index * ((atom % 3) - 1),
            base[1] + 0.0015 * replica_index * (((atom + 1) % 3) - 1),
            base[2] + 0.0008 * replica_index * (((atom + 2) % 3) - 1),
        )
        for atom, base in enumerate(VELOCITY_PATTERN)
    )
    total_mass = fsum(masses)
    center = tuple(
        fsum(m * v[axis] for m, v in zip(masses, varied, strict=True)) / total_mass
        for axis in range(3)
    )
    centered = tuple(
        tuple(v[axis] - center[axis] for axis in range(3)) for v in varied
    )
    kinetic_twice = (
        fsum(m * fsum(x * x for x in v) for m, v in zip(masses, centered, strict=True))
        * U_TO_KG * (BOHR_TO_M / TIME_TO_S) ** 2
    )
    factor = sqrt(
        3 * (len(SPECIES) - 1) * BOLTZMANN_CONSTANT_J_PER_K * TEMPERATURE_K
        / kinetic_twice
    )
    return MolecularDynamicsState(
        configuration=atomic,
        velocities=tuple(tuple(factor * x for x in v) for v in centered),
        masses=masses, step=0, time=0.0,
    )


def _initial_fingerprint(state: MolecularDynamicsState) -> str:
    payload = {
        "species": state.configuration.species,
        "positions_bohr": state.configuration.positions,
        "cell_bohr": state.configuration.cell,
        "periodic": state.configuration.periodic,
        "velocities_bohr_per_fs": state.velocities,
        "masses_u": state.masses,
        "initial_step": state.step,
        "initial_time_code": state.time,
    }
    return hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")).hexdigest()


def _run_replica(replica_index: int, model: FLiBePeriodicPolarizableModel):
    initial = _initial_state(replica_index)
    run = run_flibe_periodic_velocity_verlet(
        initial, model, MASSES, _units(), time_step=TIME_STEP,
        step_count=STEPS, neighbor_cutoff=4.0,
    )
    density = evaluate_flibe_trajectory_density(
        run.trajectory, MASSES, model_id=run.model_id,
        trajectory_id=f"FLIBE-PERIODIC-REPLICA-{replica_index:02d}",
        provenance=PROVENANCE, mass_unit_to_kg=U_TO_KG,
        coordinate_unit_to_meter=BOHR_TO_M, stride=SAMPLE_STRIDE,
    )
    stresses = []
    for sample in density.samples:
        evaluated = evaluate_flibe_periodic_polarizable_stress(
            model,
            FLiBeConfiguration(run.trajectory.states[sample.state_index].configuration),
            CellStrainDifferentiation(step=STRAIN_STEP),
        )
        if evaluated.source_file_sha256 != run.source_file_sha256:
            raise ValueError("replica stress and MD source fingerprints differ")
        stresses.append(FLiBePotentialStressSample(
            state_index=sample.state_index, md_step=sample.md_step,
            md_time=sample.md_time, stress=evaluated.total_stress,
        ))
    pressure = evaluate_flibe_trajectory_pressure(
        run.trajectory, density, tuple(stresses),
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=HARTREE_TO_J / BOHR_TO_M**3,
        velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
        stress_method_id="PERIODIC-STATIONARY-DIPOLE-ENERGY-STRAIN",
        source_id="FLIBE-REPLICA-DURATION-PRESSURE", provenance=PROVENANCE,
    )
    thermal = evaluate_flibe_frame_thermodynamics(
        run.trajectory, pressure, degrees_of_freedom=3 * (len(SPECIES) - 1),
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED_UNCLASSIFIED_BENCHMARK_STATE",
    )
    record = FLiBeReplicaThermodynamicTrace(
        replica_id=f"REPLICA-{replica_index:02d}",
        initial_condition_sha256=_initial_fingerprint(initial),
        parameter_source_sha256=run.source_file_sha256,
        thermodynamics=thermal,
    )
    samples = [
        {
            "state_index": t.state_index,
            "md_step": t.md_step,
            "md_time_code": t.md_time,
            "temperature_k": t.kinetic_temperature_k,
            "signed_pressure_pa": p.scalar_pressure_pa,
            "density_kg_m3": d.density_kg_m3,
        }
        for t, p, d in zip(thermal.samples, pressure.samples, density.samples, strict=True)
    ]
    report = {
        "replica_id": record.replica_id,
        "trajectory_id": density.trajectory_id,
        "initial_condition_sha256": record.initial_condition_sha256,
        "initial_velocities_bohr_per_fs": [list(v) for v in initial.velocities],
        "source_file_sha256": run.source_file_sha256,
        "maximum_absolute_energy_change_hartree": run.maximum_absolute_energy_change_hartree,
        "maximum_dipole_stationarity_residual_atomic": max(
            ev.max_stationarity_residual_atomic for ev in run.evaluations
        ),
        "samples": samples,
    }
    return record, report


def _close(actual: float, expected: float, absolute: float = 1.0e-8) -> bool:
    return isclose(actual, expected, rel_tol=1.0e-11, abs_tol=absolute)


def _independently_check_matrix(points, recorded) -> bool:
    for point in points:
        duration = point.retained_samples_per_trajectory
        n = point.replica_count
        if point.trajectory_ids != tuple(
            row["trajectory_id"] for row in recorded[:n]
        ):
            return False
        for name, source_field in (
            ("temperature", "temperature_k"),
            ("pressure", "signed_pressure_pa"),
            ("density", "density_kg_m3"),
        ):
            actual = getattr(point, name)
            means = tuple(
                mean(s[source_field] for s in row["samples"][
                    DISCARD_INITIAL_SAMPLES:DISCARD_INITIAL_SAMPLES + duration
                ])
                for row in recorded[:n]
            )
            if not all(_close(a, b) for a, b in zip(
                actual.trajectory_means, means, strict=True
            )):
                return False
            if not _close(actual.mean_of_trajectory_means, mean(means)):
                return False
            if not _close(actual.between_trajectory_sample_sd, stdev(means)):
                return False
            if not _close(
                actual.between_trajectory_standard_error, stdev(means) / sqrt(n)
            ):
                return False
    return True


def run_benchmark() -> dict[str, object]:
    """Execute real periodic MD replicas and audit each ensemble estimator."""
    model = _model()
    pairs_digest = hashlib.sha256(PAIR_PATH.read_bytes()).hexdigest()
    outputs = tuple(_run_replica(index, model) for index in range(REPLICA_COUNT))
    traces = tuple(pair[0] for pair in outputs)
    records = [pair[1] for pair in outputs]
    replay = _run_replica(0, model)
    matrix = evaluate_flibe_trajectory_replica_convergence(
        traces, block_size_samples=BLOCK_SIZE,
        retained_sample_lengths=RETAINED_LENGTHS,
        discarded_initial_samples=DISCARD_INITIAL_SAMPLES,
    )
    final = matrix.at(RETAINED_LENGTHS[-1], REPLICA_COUNT)
    diagnostics = {}
    for name in ("temperature", "pressure", "density"):
        series = getattr(final, name)
        error = series.between_trajectory_standard_error
        change = series.mean_change_from_previous_duration
        scaled_change = (abs(change) / error if error > 0.0 else None) if change is not None else None
        correlation = series.maximum_absolute_lag_one_block_correlation
        constant = (
            name == "density" and all(
                all(sample["density_kg_m3"] == records[0]["samples"][0]["density_kg_m3"]
                    for sample in row["samples"])
                for row in records
            )
        )
        flags = {
            "weak_block_correlation": correlation is not None and correlation <= CORRELATION_SCREEN_LIMIT,
            "duration_mean_shift_within_between_replica_se": (
                scaled_change is not None and scaled_change <= DURATION_SHIFT_SE_LIMIT
            ),
        }
        diagnostics[name] = {
            "maximum_absolute_lag_one_block_correlation": correlation,
            "last_duration_mean_change": change,
            "last_duration_mean_change_scaled_by_between_replica_se": scaled_change,
            **flags,
            "diagnostic_status": (
                "FIXED_CELL_CONSTANT" if constant else
                "SCREENING_CRITERIA_MET" if all(flags.values()) else
                "SCREENING_CRITERIA_FLAGGED"
            ),
        }
    expected_mass_kg = fsum(_initial_state(0).masses) * U_TO_KG
    density_si = expected_mass_kg / (CELL_EDGE_BOHR * BOHR_TO_M) ** 3
    checks = {
        "source_fingerprint_and_doi": all(
            row["source_file_sha256"] == pairs_digest for row in records
        ) and model.fixed_charge_model.short_range_model.parameters.source_doi == SOURCE_DOI,
        "identical_first_replica_replay": replay == outputs[0],
        "zero_center_of_mass_initial_velocity": all(
            all(abs(fsum(m * velocity[axis] for m, velocity in zip(
                _initial_state(index).masses, _initial_state(index).velocities, strict=True
            ))) <= 1.0e-12 for axis in range(3))
            for index in range(REPLICA_COUNT)
        ),
        "different_initial_conditions": len({
            row["initial_condition_sha256"] for row in records
        }) == REPLICA_COUNT and len({
            json.dumps(row["initial_velocities_bohr_per_fs"])
            for row in records
        }) == REPLICA_COUNT,
        "uniform_replica_protocol": all(
            len(row["samples"]) == 1 + STEPS // SAMPLE_STRIDE
            for row in records
        ),
        "aligned_times_and_steps": all(
            all(
                sample["state_index"] == sample["md_step"] == index * SAMPLE_STRIDE
                and _close(sample["md_time_code"], index * SAMPLE_STRIDE * TIME_STEP,
                           absolute=1.0e-14)
                for index, sample in enumerate(row["samples"])
            ) for row in records
        ),
        "common_initial_kinetic_temperature": all(
            _close(row["samples"][0]["temperature_k"], TEMPERATURE_K)
            for row in records
        ),
        "mass_volume_density_identity": all(
            all(_close(sample["density_kg_m3"], density_si)
                for sample in row["samples"])
            for row in records
        ),
        "dipole_stationarity": all(
            row["maximum_dipole_stationarity_residual_atomic"] <= DIPOLE_TOLERANCE
            for row in records
        ),
        "finite_energy_drift_and_observables": all(
            isfinite(row["maximum_absolute_energy_change_hartree"])
            and row["maximum_absolute_energy_change_hartree"] >= 0.0
            and all(isfinite(sample[key]) for sample in row["samples"]
                    for key in ("temperature_k", "signed_pressure_pa", "density_kg_m3"))
            for row in records
        ),
        "complete_duration_replica_matrix": len(matrix.points) == (
            len(RETAINED_LENGTHS) * (REPLICA_COUNT - 1)
        ) and all(matrix.at(duration, count).replica_count == count
                  for duration in RETAINED_LENGTHS
                  for count in range(2, REPLICA_COUNT + 1)),
        "source_and_sampling_provenance": (
            matrix.parameter_source_sha256 == pairs_digest
            and matrix.model_id == MODEL_ID
            and matrix.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS
            and matrix.physical_state_id == "UNCLASSIFIED_MD_PHASE"
            and _close(matrix.sampling_interval_s,
                       SAMPLE_STRIDE * TIME_STEP * TIME_TO_S, absolute=1.0e-29)
        ),
        "independent_replica_mean_and_se_recalculation": _independently_check_matrix(
            matrix.points, records
        ),
        "diagnostic_values_finite_or_undefined": all(
            item["diagnostic_status"] in (
                "FIXED_CELL_CONSTANT", "SCREENING_CRITERIA_MET", "SCREENING_CRITERIA_FLAGGED"
            ) and all(value is None or isfinite(value) for value in (
                item["maximum_absolute_lag_one_block_correlation"],
                item["last_duration_mean_change"],
                item["last_duration_mean_change_scaled_by_between_replica_se"],
            ))
            for item in diagnostics.values()
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source": {
            "doi": SOURCE_DOI,
            "relative_path": SOURCE_RELATIVE,
            "sha256": pairs_digest,
            "provenance": "PRIMARY_SOURCE",
        },
        "protocol": {
            "model_id": MODEL_ID,
            "ensemble": "NVE_FIXED_CELL",
            "species": list(SPECIES),
            "cell_edge_bohr": CELL_EDGE_BOHR,
            "initial_kinetic_temperature_target_k": TEMPERATURE_K,
            "time_step_code": TIME_STEP,
            "time_unit_to_second": TIME_TO_S,
            "integration_steps": STEPS,
            "sampling_stride": SAMPLE_STRIDE,
            "replica_count": REPLICA_COUNT,
            "initial_condition_method": "DETERMINISTIC_DISTINCT_VELOCITY_PERTURBATIONS_WITH_COM_RESCALE",
            "discard_initial_samples": DISCARD_INITIAL_SAMPLES,
            "block_size_samples": BLOCK_SIZE,
            "retained_sample_lengths": list(RETAINED_LENGTHS),
            "stress_strain_step": STRAIN_STEP,
            "velocity_frame": "CENTER_OF_MASS",
            "physical_state_id": "UNCLASSIFIED_MD_PHASE",
            "statistical_scope": "DURATION_AND_REPLICA_COUNT_SENSITIVITY",
            "initial_input_distinctness": "SHA256_OF_INITIAL_FULL_MICROSTATE",
            "statistical_independence_qualification": "UNASSESSED",
            "equilibrium_qualification": "UNASSESSED",
        },
        "replicas": records,
        "convergence": {
            "sampling_interval_s": matrix.sampling_interval_s,
            "points": [asdict(point) for point in matrix.points],
        },
        "statistical_screening": {
            "correlation_limit": CORRELATION_SCREEN_LIMIT,
            "duration_shift_scaled_by_se_limit": DURATION_SHIFT_SE_LIMIT,
            "observables": diagnostics,
        },
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
    raise SystemExit(0 if report["status"] == "PASS" else 1)
