
"""Observed-state density correspondence for periodic polarizable FLiBe MD.

Execute a fixed-cell velocity-Verlet trajectory with registered pair parameters,
compute mass density, kinetic temperature, and energy-strain-derived pressure,
then compare the resulting physical coordinates with both registered density
sources. Every source row retains its provenance, uncertainty, and individual
axis-matching flags. Density residuals are emitted only for complete matches.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from math import fsum, isclose, isfinite, sqrt
from pathlib import Path

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
    FLiBePotentialStressSample,
    FLiBeVelocityFrame,
    evaluate_flibe_trajectory_pressure,
)
from tr_eif.flibe.trajectory_state_correspondence import FLiBeTrajectoryStateCoordinates
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.md.state import MolecularDynamicsState

ROOT = Path(__file__).resolve().parents[2]
PAIR_SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
REFERENCE_PATHS = (
    ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json",
    ROOT / "data/reference/flibe_baral_2021_aimd_density.json",
)
BENCHMARK_ID = "tr-eif.flibe.periodic-md-density-source-state-gate.v1"
MODEL_ID = "FLIBE-PERIODIC-DENSITY-SOURCE-GATE"
PROVENANCE = ParameterProvenance.BENCHMARK

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS_BOHR = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0), (8.0, 10.0, 11.0),
)
VELOCITIES_BOHR_PER_FS = (
    (0.03, 0.01, 0.0), (-0.03, -0.01, 0.02), (0.02, 0.03, -0.02),
    (0.0, -0.02, 0.01), (0.01, 0.005, -0.02),
    (-0.015, 0.02, 0.0), (-0.015, -0.015, 0.01),
)
CELL_BOHR = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
MASSES_U = FLiBeMassParameters(lithium=6.94, beryllium=9.0121831, fluorine=18.998403163)
U_TO_KG = 1.66053906660e-27
BOHR_TO_M = 5.29177210903e-11
HARTREE_TO_J = 4.3597447222071e-18
TIME_TO_S = 1.0e-15
TARGET_INITIAL_TEMPERATURE_K = 850.0
BOLTZMANN_J_PER_K = 1.380649e-23
TIME_STEP_CODE = 0.001
STEP_COUNT = 1
STRAIN_STEP = 2.0e-5
TEMPERATURE_TOLERANCE_K = 5.0
PRESSURE_TOLERANCE_PA = 1000.0


def _model() -> FLiBePeriodicPolarizableModel:
    pairs = load_flibe_registered_pair_parameters(PAIR_SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25, real_image_shell=1, reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0, provenance=PROVENANCE,
        source_id="FLIBE-DENSITY-GATE-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-DENSITY-GATE-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-DENSITY-GATE-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-DENSITY-GATE-SHORT", parameters=pairs,
                coordinate_unit_to_bohr=1.0, image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-DENSITY-GATE-DIPOLES", parameters=pairs,
            ewald_parameters=ewald, damping_image_shell=1,
            stationarity_absolute_tolerance=1.0e-10,
        ),
    )


def _target_velocities():
    """Rescale a fixed velocity pattern to a declared COM kinetic temperature."""
    masses = configuration_masses(FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES, positions=POSITIONS_BOHR, cell=CELL_BOHR,
        periodic=(True, True, True),
    )), MASSES_U)
    total_mass = fsum(masses)
    center = tuple(
        fsum(mass * velocity[axis] for mass, velocity in zip(
            masses, VELOCITIES_BOHR_PER_FS, strict=True,
        )) / total_mass for axis in range(3)
    )
    mass_weighted_speed_squared = fsum(
        mass * fsum((velocity[axis] - center[axis])**2 for axis in range(3))
        for mass, velocity in zip(masses, VELOCITIES_BOHR_PER_FS, strict=True)
    )
    kinetic_temperature = (
        mass_weighted_speed_squared * U_TO_KG * (BOHR_TO_M / TIME_TO_S)**2
        / (3 * (len(SPECIES) - 1) * BOLTZMANN_J_PER_K)
    )
    scale = sqrt(TARGET_INITIAL_TEMPERATURE_K / kinetic_temperature)
    return tuple(
        tuple(scale * component for component in velocity)
        for velocity in VELOCITIES_BOHR_PER_FS
    )


def _observed_run():
    model = _model()
    atomic = AtomicConfiguration(
        species=SPECIES, positions=POSITIONS_BOHR, cell=CELL_BOHR,
        periodic=(True, True, True),
    )
    flibe = FLiBeConfiguration(atomic)
    initial = MolecularDynamicsState(
        configuration=atomic,
        velocities=_target_velocities(),
        masses=configuration_masses(flibe, MASSES_U),
        step=0, time=0.0,
    )
    units = FLiBePeriodicMDUnits(
        mass_unit_to_kg=U_TO_KG, coordinate_unit_to_meter=BOHR_TO_M,
        time_unit_to_second=TIME_TO_S, bohr_to_meter=BOHR_TO_M,
        hartree_to_joule=HARTREE_TO_J,
        provenance=PROVENANCE, source_id="FLIBE-DENSITY-GATE-SI",
    )
    run = run_flibe_periodic_velocity_verlet(
        initial, model, MASSES_U, units,
        time_step=TIME_STEP_CODE, step_count=STEP_COUNT, neighbor_cutoff=4.0,
    )
    density = evaluate_flibe_trajectory_density(
        run.trajectory, MASSES_U, model_id=run.model_id,
        trajectory_id="FLIBE-DENSITY-GATE-TRAJECTORY",
        provenance=PROVENANCE, mass_unit_to_kg=U_TO_KG,
        coordinate_unit_to_meter=BOHR_TO_M,
    )
    strain = CellStrainDifferentiation(step=STRAIN_STEP)
    stress_rows = []
    for sample in density.samples:
        state = run.trajectory.states[sample.state_index]
        evaluated = evaluate_flibe_periodic_polarizable_stress(
            model, FLiBeConfiguration(state.configuration), strain,
        )
        if evaluated.source_file_sha256 != run.source_file_sha256:
            raise ValueError("stress and trajectory pair-source fingerprints differ")
        stress_rows.append(FLiBePotentialStressSample(
            state_index=sample.state_index, md_step=sample.md_step,
            md_time=sample.md_time, stress=evaluated.total_stress,
        ))
    pressure = evaluate_flibe_trajectory_pressure(
        run.trajectory, density, tuple(stress_rows),
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=HARTREE_TO_J / BOHR_TO_M**3,
        velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
        stress_method_id="PERIODIC-STATIONARY-DIPOLE-ENERGY-STRAIN",
        source_id="FLIBE-DENSITY-GATE-COMPUTED-PRESSURE",
        provenance=PROVENANCE,
    )
    thermal = evaluate_flibe_frame_thermodynamics(
        run.trajectory, pressure, degrees_of_freedom=3 * (len(SPECIES) - 1),
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED_UNCLASSIFIED_BENCHMARK_STATE",
    )
    # Signed mechanical pressure is retained in the tensor record. The
    # nonnegative thermodynamic-pressure domain is applied independently.
    observed_pressure = (
        pressure.to_observed_pressure_coordinate()
        if pressure.mean_pressure_pa >= 0.0 else None
    )
    model_coordinates = FLiBeTrajectoryStateCoordinates(
        density_trace=density,
        kinetic_temperature_k=tuple(s.kinetic_temperature_k for s in thermal.samples),
        degrees_of_freedom=thermal.degrees_of_freedom,
        time_unit_to_second=TIME_TO_S,
        physical_state_id=thermal.physical_state_id,
        physical_state_method_id=thermal.physical_state_method_id,
        pressure=observed_pressure,
    )
    return run, model_coordinates, pressure


def _source_report(
    model_coordinates: FLiBeTrajectoryStateCoordinates,
    signed_pressure_pa: float,
    path: Path,
):
    records = load_flibe_density_source_records(path)
    mapping = FLiBeDensityObservableMapping(
        mapping_id="FLIBE-DENSITY-GATE-OBSERVABLE-MAPPING",
        model_statistic_id=MODEL_DENSITY_STATISTIC,
        source_normalization_id="source-reported-mass-density",
        method_id="EXACT-COMPOSITION-STATE-GATED-COMPARISON",
        provenance=PROVENANCE,
        assumptions=("fixed-NVE-cell", "mean-instantaneous-cell-density"),
    )
    result = compare_flibe_registered_density_records(
        model_coordinates, records, mapping=mapping,
        temperature_tolerance_k=TEMPERATURE_TOLERANCE_K,
        pressure_tolerance_pa=PRESSURE_TOLERANCE_PA,
    )
    rows = []
    for item in result.rows:
        reference = item.source_record
        coordinate = reference.coordinates
        rows.append({
            "record_id": item.record_id,
            "run_id": reference.run_id,
            "source_temperature_k": coordinate.temperature_k,
            "source_density_kg_m3": coordinate.density_kg_m3,
            "source_pressure_pa": coordinate.pressure_pa,
            "source_physical_state_id": coordinate.physical_state_id,
            "source_bef2_fraction": coordinate.composition.bef2_fraction,
            "source_bef2_fraction_standard_uncertainty": (
                coordinate.bef2_fraction_standard_uncertainty
            ),
            "source_density_standard_uncertainty_kg_m3": coordinate.density_standard_uncertainty_kg_m3,
            "source_temperature_standard_uncertainty_k": coordinate.temperature_standard_uncertainty_k,
            "source_pressure_standard_uncertainty_pa": coordinate.pressure_standard_uncertainty_pa,
            "matched_axes": list(item.matched_axes),
            "unmatched_axes": list(item.unmatched_axes),
            "missing_source_axes": list(item.missing_source_axes),
            "temperature_difference_k": item.temperature_difference_k,
            "pressure_difference_pa": item.pressure_difference_pa,
            "bef2_fraction_difference": item.bef2_fraction_difference,
            "signed_md_minus_source_pressure_pa": (
                signed_pressure_pa - coordinate.pressure_pa
                if coordinate.pressure_pa is not None else None
            ),
            "qualified_density_residual_kg_m3": item.density_residual_kg_m3,
        })
    return {
        "dataset_id": result.source_dataset_id,
        "doi": records[0].doi,
        "evidence_kind": records[0].coordinates.evidence_kind.value,
        "source_file_sha256": result.source_file_sha256,
        "record_count": len(records),
        "matched_count": result.matched_count,
        "unmatched_count": result.unmatched_count,
        "residual_metrics": (
            asdict(result.residual_metrics) if result.residual_metrics is not None else None
        ),
        "records": rows,
    }


def run_benchmark() -> dict[str, object]:
    run, model, pressure = _observed_run()
    sources = tuple(
        _source_report(model, pressure.mean_pressure_pa, path)
        for path in REFERENCE_PATHS
    )
    checks = {
        "registered_pair_source": run.source_file_sha256 == hashlib.sha256(PAIR_SOURCE.read_bytes()).hexdigest(),
        "complete_potential_state_observations": len(run.evaluations) == STEP_COUNT + 1,
        "target_initial_kinetic_temperature": isclose(
            model.kinetic_temperature_k[0], TARGET_INITIAL_TEMPERATURE_K,
            rel_tol=1.0e-12,
        ),
        "aimd_temperature_coordinate_exercised": any(
            "temperature" in row["matched_axes"] for row in sources[1]["records"]
        ),
        "physical_mass_and_cell_density": all(
            isclose(s.density_kg_m3, model.density_trace.total_mass_kg / s.cell_volume_m3,
                    rel_tol=1.0e-12) for s in model.density_trace.samples
        ),
        "computed_pressure_tensor_trace": all(
            isclose(s.scalar_pressure_pa, sum(s.pressure_tensor_pa[i][i] for i in range(3)) / 3.0,
                    rel_tol=1.0e-12, abs_tol=1.0e-6) for s in pressure.samples
        ),
        "finite_model_coordinates": all(isfinite(v) for v in (
            model.mean_kinetic_temperature_k,
            model.density_trace.mean_density_kg_m3,
            pressure.mean_pressure_pa,
        )),
        "registered_source_counts": tuple(s["record_count"] for s in sources) == (61, 9),
        "registered_source_fingerprints": all(
            s["source_file_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
            for s, path in zip(sources, REFERENCE_PATHS, strict=True)
        ),
        "all_rows_state_screened": all(
            source["record_count"] == source["matched_count"] + source["unmatched_count"]
            for source in sources
        ),
        "residual_only_on_matched_coordinates": all(
            (row["qualified_density_residual_kg_m3"] is not None)
            == (not row["unmatched_axes"])
            for source in sources for row in source["records"]
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "comparison_contract": {
            "composition_matching": "EXACT_FORMULA_UNIT_FRACTIONS",
            "temperature_tolerance_k": TEMPERATURE_TOLERANCE_K,
            "pressure_tolerance_pa": PRESSURE_TOLERANCE_PA,
            "physical_state_matching": "EXACT_REPORTED_STATE_IDENTIFIER",
            "pressure_role": "OBSERVED_ONLY",
            "normalization": "source-reported-mass-density",
            "qualified_residual_eligibility": "ALL_FIVE_STATE_COORDINATES_MATCH",
        },
        "model": {
            "model_id": run.model_id,
            "provenance": PROVENANCE.value,
            "initial_species": list(SPECIES),
            "atom_count": len(SPECIES),
            "mass_values_u": {"Li": MASSES_U.lithium, "Be": MASSES_U.beryllium, "F": MASSES_U.fluorine},
            "initial_cell_bohr": CELL_BOHR,
            "ensemble": "NVE_FIXED_CELL",
            "initial_temperature_target_k": TARGET_INITIAL_TEMPERATURE_K,
            "initial_temperature_target_role": "CONTROL_TARGET",
            "time_step_code": TIME_STEP_CODE,
            "integration_steps": STEP_COUNT,
            "pressure_method": pressure.stress_method_id,
            "velocity_frame": pressure.velocity_frame.value,
            "physical_state_id": model.physical_state_id,
            "pair_source_doi": SOURCE_DOI,
            "pair_source_sha256": run.source_file_sha256,
        },
        "observed": {
            "mean_density_kg_m3": model.density_trace.mean_density_kg_m3,
            "mean_kinetic_temperature_k": model.mean_kinetic_temperature_k,
            "mean_signed_pressure_pa": pressure.mean_pressure_pa,
            "pressure_coordinate_pa": (
                model.pressure.pressure_pa if model.pressure is not None else None
            ),
            "bef2_fraction": model.density_trace.composition.bef2_fraction,
            "density_statistic_id": MODEL_DENSITY_STATISTIC,
            "energy_drift_hartree": run.maximum_absolute_energy_change_hartree,
            "samples": [
                {
                    "state_index": d.state_index,
                    "md_time_code": d.md_time,
                    "density_kg_m3": d.density_kg_m3,
                    "kinetic_temperature_k": t,
                    "signed_pressure_pa": p.scalar_pressure_pa,
                }
                for d, t, p in zip(model.density_trace.samples,
                                    model.kinetic_temperature_k, pressure.samples, strict=True)
            ],
        },
        "sources": list(sources),
    }


if __name__ == "__main__":
    output = run_benchmark()
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if output["status"] == "PASS" else 1)
