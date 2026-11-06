"""Fixed-composition periodic FLiBe MD volume and state-coordinate scan.

Six declared cubic cells share one fractional Li2BeF4 geometry, registered
interatomic parameters, and a center-of-mass kinetic temperature of 850 K.
Each fixed-cell trajectory supplies mass density, kinetic temperature,
energy-strain stress, and the full kinetic-plus-configurational pressure.
Registered experimental and AIMD records are independently screened by
composition, temperature, observed pressure, phase and normalization.
Source density ranges are retained as screening coordinates; qualified
residuals use the established complete-state correspondence contract.
"""

from __future__ import annotations

import hashlib
import json
from math import fsum, isclose, isfinite, sqrt
from pathlib import Path

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import CellStrainDifferentiation
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.mass import FLiBeMassParameters, configuration_masses
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_md import (
    FLiBePeriodicMDUnits, run_flibe_periodic_velocity_verlet,
)
from tr_eif.flibe.periodic_polarizable_stress import evaluate_flibe_periodic_polarizable_stress
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_density_cross_model import (
    MODEL_DENSITY_STATISTIC,
    FLiBeDensityObservableMapping,
    compare_flibe_registered_density_records,
)
from tr_eif.flibe.registered_density_sources import load_flibe_density_source_records
from tr_eif.flibe.registered_pair_coefficients import SOURCE_DOI, load_flibe_registered_pair_parameters
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_frame_thermodynamics import evaluate_flibe_frame_thermodynamics
from tr_eif.flibe.trajectory_pressure import (
    FLiBePotentialStressSample, FLiBeVelocityFrame, evaluate_flibe_trajectory_pressure,
)
from tr_eif.flibe.trajectory_state_correspondence import FLiBeTrajectoryStateCoordinates
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.md.state import MolecularDynamicsState

ROOT = Path(__file__).resolve().parents[2]
PAIR_PATH = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
REFERENCE_PATHS = (
    ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json",
    ROOT / "data/reference/flibe_baral_2021_aimd_density.json",
)
BENCHMARK_ID = "tr-eif.flibe.periodic-md-volume-state-scan.v1"
MODEL_ID = "FLIBE-PERIODIC-VOLUME-STATE-SCAN"
PROVENANCE = ParameterProvenance.BENCHMARK
CELL_EDGES_BOHR = (8.0, 8.5, 9.0, 10.0, 12.0, 18.0)
BASE_CELL_EDGE_BOHR = 18.0
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
BASE_POSITIONS_BOHR = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0), (8.0, 10.0, 11.0),
)
VELOCITY_PATTERN = (
    (0.03, 0.01, 0.0), (-0.03, -0.01, 0.02), (0.02, 0.03, -0.02),
    (0.0, -0.02, 0.01), (0.01, 0.005, -0.02),
    (-0.015, 0.02, 0.0), (-0.015, -0.015, 0.01),
)
MASS_PARAMETERS = FLiBeMassParameters(lithium=6.94, beryllium=9.0121831, fluorine=18.998403163)
U_TO_KG = 1.66053906660e-27
BOHR_TO_M = 5.29177210903e-11
HARTREE_TO_J = 4.3597447222071e-18
TIME_TO_S = 1.0e-15
BOLTZMANN_J_PER_K = 1.380649e-23
TARGET_INITIAL_TEMPERATURE_K = 850.0
DT_CODE = 0.001
STEP_COUNT = 1
STRAIN_STEP = 2.0e-5
TEMPERATURE_TOLERANCE_K = 5.0
PRESSURE_TOLERANCE_PA = 1000.0
EXPERIMENTAL_PRESSURE_PA = 102000.0


def _model() -> FLiBePeriodicPolarizableModel:
    pairs = load_flibe_registered_pair_parameters(PAIR_PATH)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25, real_image_shell=1, reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0, provenance=PROVENANCE,
        source_id="FLIBE-VOLUME-SCAN-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-VOLUME-SCAN-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-VOLUME-SCAN-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-VOLUME-SCAN-SHORT", parameters=pairs,
                coordinate_unit_to_bohr=1.0, image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-VOLUME-SCAN-POLARIZATION", parameters=pairs,
            ewald_parameters=ewald, damping_image_shell=1,
            stationarity_absolute_tolerance=1.0e-10,
        ),
    )


def _initial_velocities(masses: tuple[float, ...]) -> tuple[tuple[float, float, float], ...]:
    mass_sum = fsum(masses)
    center = tuple(
        fsum(mass * row[axis] for mass, row in zip(masses, VELOCITY_PATTERN, strict=True))
        / mass_sum for axis in range(3)
    )
    centered = tuple(
        tuple(row[axis] - center[axis] for axis in range(3))
        for row in VELOCITY_PATTERN
    )
    kinetic_twice_j = fsum(
        mass * fsum(component * component for component in row)
        for mass, row in zip(masses, centered, strict=True)
    ) * U_TO_KG * (BOHR_TO_M / TIME_TO_S)**2
    degree_count = 3 * (len(SPECIES) - 1)
    coefficient = sqrt(
        degree_count * BOLTZMANN_J_PER_K * TARGET_INITIAL_TEMPERATURE_K
        / kinetic_twice_j
    )
    return tuple(tuple(coefficient * v for v in row) for row in centered)


def _configuration(edge_bohr: float) -> FLiBeConfiguration:
    scale = edge_bohr / BASE_CELL_EDGE_BOHR
    cell = tuple(
        tuple(edge_bohr if axis == component else 0.0 for component in range(3))
        for axis in range(3)
    )
    return FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES,
        positions=tuple(tuple(scale * x for x in row) for row in BASE_POSITIONS_BOHR),
        cell=cell,
        periodic=(True, True, True),
    ))


def _scan_case(
    model: FLiBePeriodicPolarizableModel,
    edge_bohr: float,
    sources: tuple[tuple, ...],
    mapping: FLiBeDensityObservableMapping,
) -> dict[str, object]:
    configuration = _configuration(edge_bohr)
    masses = configuration_masses(configuration, MASS_PARAMETERS)
    initial = MolecularDynamicsState(
        configuration=configuration.configuration,
        velocities=_initial_velocities(masses),
        masses=masses, step=0, time=0.0,
    )
    units = FLiBePeriodicMDUnits(
        mass_unit_to_kg=U_TO_KG, coordinate_unit_to_meter=BOHR_TO_M,
        time_unit_to_second=TIME_TO_S, bohr_to_meter=BOHR_TO_M,
        hartree_to_joule=HARTREE_TO_J, provenance=PROVENANCE,
        source_id="FLIBE-VOLUME-SCAN-SI",
    )
    run = run_flibe_periodic_velocity_verlet(
        initial, model, MASS_PARAMETERS, units,
        time_step=DT_CODE, step_count=STEP_COUNT, neighbor_cutoff=4.0,
    )
    density = evaluate_flibe_trajectory_density(
        run.trajectory, MASS_PARAMETERS, model_id=run.model_id,
        trajectory_id=f"FLIBE-VOLUME-SCAN-{edge_bohr:g}",
        provenance=PROVENANCE, mass_unit_to_kg=U_TO_KG,
        coordinate_unit_to_meter=BOHR_TO_M,
    )
    stresses = []
    polarization_residuals = []
    for idx, state in enumerate(run.trajectory.states):
        stress = evaluate_flibe_periodic_polarizable_stress(
            model, FLiBeConfiguration(state.configuration),
            CellStrainDifferentiation(step=STRAIN_STEP),
        )
        if stress.reference.source_file_sha256 != run.source_file_sha256:
            raise ValueError("periodic stress and MD potential source fingerprints differ")
        stresses.append(FLiBePotentialStressSample(
            state_index=idx, md_step=state.step,
            md_time=state.time, stress=stress.total_stress,
        ))
        polarization_residuals.append(
            run.evaluations[idx].polarization_force_result.polarization_result.max_stationarity_residual_atomic
        )
    pressure = evaluate_flibe_trajectory_pressure(
        run.trajectory, density, tuple(stresses),
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=HARTREE_TO_J / BOHR_TO_M**3,
        velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
        stress_method_id="PERIODIC-STATIONARY-DIPOLE-ENERGY-STRAIN",
        source_id="FLIBE-VOLUME-SCAN-MEASURED-PRESSURE",
        provenance=PROVENANCE,
    )
    thermal = evaluate_flibe_frame_thermodynamics(
        run.trajectory, pressure,
        degrees_of_freedom=3 * (len(SPECIES) - 1),
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED_UNCLASSIFIED_BENCHMARK_STATE",
    )
    mean_signed_pressure = pressure.mean_pressure_pa
    observed_pressure = (
        pressure.to_observed_pressure_coordinate() if mean_signed_pressure >= 0.0 else None
    )
    coordinates = FLiBeTrajectoryStateCoordinates(
        density_trace=density,
        kinetic_temperature_k=tuple(s.kinetic_temperature_k for s in thermal.samples),
        degrees_of_freedom=thermal.degrees_of_freedom,
        time_unit_to_second=TIME_TO_S,
        physical_state_id=thermal.physical_state_id,
        physical_state_method_id=thermal.physical_state_method_id,
        pressure=observed_pressure,
    )
    screened = []
    for records in sources:
        compared = compare_flibe_registered_density_records(
            coordinates, records, mapping=mapping,
            temperature_tolerance_k=TEMPERATURE_TOLERANCE_K,
            pressure_tolerance_pa=PRESSURE_TOLERANCE_PA,
        )
        count_by_axis = {
            axis: sum(axis in row.matched_axes for row in compared.rows)
            for axis in ("composition", "temperature", "pressure", "physical_state", "normalization")
        }
        densities = tuple(r.coordinates.density_kg_m3 for r in records)
        screened.append({
            "dataset_id": compared.source_dataset_id,
            "source_sha256": compared.source_file_sha256,
            "source_row_count": len(compared.rows),
            "matched_count_by_axis": count_by_axis,
            "fully_matched_rows": compared.matched_count,
            "qualified_density_metrics": None if compared.residual_metrics is None else {
                "count": compared.residual_metrics.count,
                "root_mean_square_kg_m3": compared.residual_metrics.root_mean_square_kg_m3,
            },
            "source_density_range_kg_m3": [min(densities), max(densities)],
            "model_density_within_source_range": (
                min(densities) <= density.mean_density_kg_m3 <= max(densities)
            ),
            "missing_source_pressure_count": sum(
                row.source_record.coordinates.pressure_pa is None for row in compared.rows
            ),
            "missing_source_phase_count": sum(
                row.source_record.coordinates.physical_state_id is None for row in compared.rows
            ),
        })
    samples = []
    for idx, (d, p, t) in enumerate(zip(
        density.samples, pressure.samples, thermal.samples, strict=True,
    )):
        kinetic_p = fsum(p.kinetic_tensor_pa[a][a] for a in range(3)) / 3.0
        config_p = fsum(p.configurational_tensor_pa[a][a] for a in range(3)) / 3.0
        samples.append({
            "state_index": idx,
            "md_time_code": d.md_time,
            "density_kg_m3": d.density_kg_m3,
            "kinetic_temperature_k": t.kinetic_temperature_k,
            "kinetic_pressure_pa": kinetic_p,
            "configurational_pressure_pa": config_p,
            "signed_total_pressure_pa": p.scalar_pressure_pa,
            "potential_energy_hartree": run.evaluations[idx].energy.total_energy,
            "dipole_stationarity_residual_atomic": polarization_residuals[idx],
        })
    return {
        "cell_edge_bohr": edge_bohr,
        "cell_volume_bohr3": edge_bohr**3,
        "atom_count": len(SPECIES),
        "formula_unit_count": 1,
        "formal_charge_total_e": fsum(run.evaluations[0].fixed_charge_result.ewald_result.formal_charges_e),
        "total_cell_mass_kg": density.total_mass_kg,
        "model_source_sha256": run.source_file_sha256,
        "mean_density_kg_m3": density.mean_density_kg_m3,
        "mean_temperature_k": thermal.mean_kinetic_temperature_k,
        "mean_signed_pressure_pa": mean_signed_pressure,
        "observed_pressure_coordinate_pa": (
            observed_pressure.pressure_pa if observed_pressure is not None else None
        ),
        "maximum_absolute_energy_change_hartree": run.maximum_absolute_energy_change_hartree,
        "samples": samples,
        "source_screening": screened,
    }


def run_benchmark() -> dict[str, object]:
    """Execute the declared geometry series and register source-state screens."""
    model = _model()
    source_records = tuple(load_flibe_density_source_records(path) for path in REFERENCE_PATHS)
    mapping = FLiBeDensityObservableMapping(
        mapping_id="FLIBE-VOLUME-SCAN-DENSITY-MAPPING",
        model_statistic_id=MODEL_DENSITY_STATISTIC,
        source_normalization_id="source-reported-mass-density",
        method_id="FIVE-AXIS-VOLUME-STATE-SCREENING",
        provenance=PROVENANCE,
        assumptions=("fixed-cell-NVE", "fractionally-scaled-seven-atom-geometry"),
    )
    results = [
        _scan_case(model, edge, source_records, mapping) for edge in CELL_EDGES_BOHR
    ]
    target_pressure = source_records[0][0].coordinates.pressure_pa
    if target_pressure is None:
        raise ValueError("experimental source requires a pressure coordinate")
    pressure_brackets = []
    for left, right in zip(results, results[1:]):
        p0 = left["mean_signed_pressure_pa"] - target_pressure
        p1 = right["mean_signed_pressure_pa"] - target_pressure
        if p0 * p1 <= 0.0:
            pressure_brackets.append({
                "cell_edge_interval_bohr": [left["cell_edge_bohr"], right["cell_edge_bohr"]],
                "pressure_difference_at_edges_pa": [p0, p1],
            })
    source_hashes = tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in REFERENCE_PATHS)
    mass_kg = results[0]["total_cell_mass_kg"]
    checks = {
        "registered_pair_provenance": all(
            row["model_source_sha256"] == hashlib.sha256(PAIR_PATH.read_bytes()).hexdigest()
            for row in results
        ) and model.fixed_charge_model.short_range_model.parameters.source_doi == SOURCE_DOI,
        "declared_monotone_cell_grid": all(
            a < b for a, b in zip(CELL_EDGES_BOHR, CELL_EDGES_BOHR[1:])
        ),
        "exact_stoichiometry_and_charge": all(
            row["atom_count"] == 7 and row["formula_unit_count"] == 1
            and row["formal_charge_total_e"] == 0.0 for row in results
        ),
        "constant_cell_mass": all(row["total_cell_mass_kg"] == mass_kg for row in results),
        "density_volume_identity": all(isclose(
            row["mean_density_kg_m3"], mass_kg / (row["cell_edge_bohr"] * BOHR_TO_M)**3,
            rel_tol=1.0e-12,
        ) for row in results),
        "density_decreases_with_volume": all(
            a["mean_density_kg_m3"] > b["mean_density_kg_m3"]
            for a, b in zip(results, results[1:])
        ),
        "temperature_initialization": all(isclose(
            row["samples"][0]["kinetic_temperature_k"], TARGET_INITIAL_TEMPERATURE_K,
            rel_tol=1.0e-12,
        ) for row in results),
        "pressure_tensor_decomposition": all(isclose(
            s["kinetic_pressure_pa"] + s["configurational_pressure_pa"],
            s["signed_total_pressure_pa"], rel_tol=1.0e-12, abs_tol=1.0e-3,
        ) for row in results for s in row["samples"]),
        "observed_pressure_role": all(
            (row["observed_pressure_coordinate_pa"] is None) ==
            (row["mean_signed_pressure_pa"] < 0.0)
            for row in results
        ),
        "dipole_stationarity": all(
            s["dipole_stationarity_residual_atomic"] <= 1.0e-10
            for row in results for s in row["samples"]
        ),
        "finite_numeric_observables": all(
            all(isfinite(s[key]) for key in (
                "density_kg_m3", "kinetic_temperature_k", "kinetic_pressure_pa",
                "configurational_pressure_pa", "signed_total_pressure_pa",
                "potential_energy_hartree",
            )) for row in results for s in row["samples"]
        ),
        "source_fingerprints": all(
            screen["source_sha256"] == source_hashes[idx]
            for row in results for idx, screen in enumerate(row["source_screening"])
        ),
        "source_row_accounting": all(
            tuple(screen["source_row_count"] for screen in row["source_screening"]) == (61, 9)
            for row in results
        ),
        "residuals_require_complete_state": all(
            (screen["qualified_density_metrics"] is None)
            == (screen["fully_matched_rows"] == 0)
            for row in results for screen in row["source_screening"]
        ),
        "source_density_range_spanned": all(
            results[-1]["mean_density_kg_m3"] < min(
                r.coordinates.density_kg_m3 for r in records
            ) < max(r.coordinates.density_kg_m3 for r in records)
            < results[0]["mean_density_kg_m3"]
            for records in source_records
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "method": {
            "ensemble": "NVE_FIXED_CELL",
            "geometry": "SHARED_FRACTIONAL_SEVEN_ATOM_FIXTURE",
            "cell_edges_bohr": list(CELL_EDGES_BOHR),
            "temperature_initialization_k": TARGET_INITIAL_TEMPERATURE_K,
            "velocity_frame": "CENTER_OF_MASS",
            "time_step_code": DT_CODE,
            "integration_steps": STEP_COUNT,
            "stress_strain_step": STRAIN_STEP,
            "pressure_operator": "KINETIC_PLUS_ENERGY_STRAIN_CONFIGURATIONAL",
            "phase_id": "UNCLASSIFIED_MD_PHASE",
            "temperature_match_tolerance_k": TEMPERATURE_TOLERANCE_K,
            "pressure_match_tolerance_pa": PRESSURE_TOLERANCE_PA,
            "source_residual_gate": "COMPLETE_FIVE_AXIS_STATE_MATCH",
        },
        "sources": [
            {"dataset_id": records[0].dataset_id, "doi": records[0].doi,
             "file_sha256": source_hashes[idx], "row_count": len(records)}
            for idx, records in enumerate(source_records)
        ],
        "experimental_pressure_reference_pa": target_pressure,
        "pressure_difference_brackets": pressure_brackets,
        "results": results,
    }


if __name__ == "__main__":
    output = run_benchmark()
    print(json.dumps(output, sort_keys=True, indent=2, allow_nan=False))
    raise SystemExit(0 if output["status"] == "PASS" else 1)
