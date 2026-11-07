
"""Block-size and sampling-window sensitivity of periodic polarizable FLiBe MD.

A registered Li2BeF4 potential generates one fixed-cell NVE trajectory.
Full-potential energy-strain stress, velocity-frame kinetic temperature, and
cell-mass density are evaluated on the same sampled states. Predeclared
block partitions retain statistical errors, lag-one block correlation,
and early-versus-late mean differences in their physical SI units.

All sampling diagnostics are computed from one explicitly identified
trajectory. Numerical acceptance gates verify conservation, sample alignment,
source provenance, statistical arithmetic, and reproducible bookkeeping.
"""

from __future__ import annotations

import hashlib
import json
from math import fsum, hypot, isclose, isfinite, sqrt
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
from tr_eif.flibe.trajectory_block_statistics import evaluate_flibe_trajectory_block_statistics
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_frame_thermodynamics import evaluate_flibe_frame_thermodynamics
from tr_eif.flibe.trajectory_pressure import (
    FLiBePotentialStressSample, FLiBeVelocityFrame, evaluate_flibe_trajectory_pressure,
)
from tr_eif.flibe.trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.md.state import MolecularDynamicsState

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SOURCE_RELATIVE = "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-thermodynamic-block-convergence.v1"
MODEL_ID = "FLIBE-PERIODIC-MD-THERMODYNAMIC-BLOCKS"
TRAJECTORY_ID = "FLIBE-PERIODIC-THERMODYNAMIC-SAMPLING"
PROVENANCE = ParameterProvenance.BENCHMARK
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
BASE_EDGE_BOHR = 18.0
EDGE_BOHR = 10.0
BASE_POSITIONS_BOHR = (
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
U_TO_KG = 1.66053906660e-27
BOHR_TO_M = 5.29177210903e-11
HARTREE_TO_J = 4.3597447222071e-18
TIME_TO_S = 1.0e-15
TEMPERATURE_TARGET_K = 850.0
TIME_STEP_CODE = 0.01
INTEGRATION_STEPS = 63
SAMPLE_STRIDE = 2
STRAIN_STEP = 2.0e-5
STATIONARITY_LIMIT = 1.0e-10
MAX_ABS_ADJACENT_BLOCK_CORRELATION = 0.5
MAX_BLOCK_SE_CHANGE_FRACTION = 0.25
MAX_WINDOW_MEAN_SHIFT_SCALED_BY_SE = 1.0
BLOCK_WINDOWS = (
    ("all_four_frame_blocks", 4, 0),
    ("all_eight_frame_blocks", 8, 0),
    ("discard_eight_samples", 4, 8),
    ("discard_sixteen_samples", 4, 16),
)


def _model() -> FLiBePeriodicPolarizableModel:
    pairs = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25, real_image_shell=1, reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0, provenance=PROVENANCE,
        source_id="FLIBE-BLOCKS-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-BLOCKS-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-BLOCKS-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-BLOCKS-SHORT", parameters=pairs,
                coordinate_unit_to_bohr=1.0, image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-BLOCKS-POLARIZATION", parameters=pairs,
            ewald_parameters=ewald, damping_image_shell=1,
            stationarity_absolute_tolerance=STATIONARITY_LIMIT,
        ),
    )


def _starting_state() -> MolecularDynamicsState:
    scale = EDGE_BOHR / BASE_EDGE_BOHR
    cell = (
        (EDGE_BOHR, 0.0, 0.0),
        (0.0, EDGE_BOHR, 0.0),
        (0.0, 0.0, EDGE_BOHR),
    )
    configuration = AtomicConfiguration(
        species=SPECIES,
        positions=tuple(tuple(scale * x for x in v) for v in BASE_POSITIONS_BOHR),
        cell=cell, periodic=(True, True, True),
    )
    masses = configuration_masses(FLiBeConfiguration(configuration), MASSES)
    total_mass = fsum(masses)
    mean_velocity = tuple(
        fsum(m * v[a] for m, v in zip(masses, VELOCITY_PATTERN, strict=True))
        / total_mass for a in range(3)
    )
    centered = tuple(
        tuple(v[a] - mean_velocity[a] for a in range(3))
        for v in VELOCITY_PATTERN
    )
    twice_kinetic = fsum(
        m * fsum(v[a] ** 2 for a in range(3))
        for m, v in zip(masses, centered, strict=True)
    ) * U_TO_KG * (BOHR_TO_M / TIME_TO_S)**2
    factor = sqrt(
        3 * (len(SPECIES) - 1) * BOLTZMANN_CONSTANT_J_PER_K
        * TEMPERATURE_TARGET_K / twice_kinetic
    )
    return MolecularDynamicsState(
        configuration=configuration,
        velocities=tuple(tuple(factor * x for x in v) for v in centered),
        masses=masses, step=0, time=0.0,
    )


def _thermodynamic_trajectory():
    model = _model()
    units = FLiBePeriodicMDUnits(
        mass_unit_to_kg=U_TO_KG, coordinate_unit_to_meter=BOHR_TO_M,
        time_unit_to_second=TIME_TO_S, bohr_to_meter=BOHR_TO_M,
        hartree_to_joule=HARTREE_TO_J, provenance=PROVENANCE,
        source_id="FLIBE-BLOCKS-SI",
    )
    run = run_flibe_periodic_velocity_verlet(
        _starting_state(), model, MASSES, units,
        time_step=TIME_STEP_CODE, step_count=INTEGRATION_STEPS,
        neighbor_cutoff=4.0,
    )
    density = evaluate_flibe_trajectory_density(
        run.trajectory, MASSES, model_id=run.model_id,
        trajectory_id=TRAJECTORY_ID, provenance=PROVENANCE,
        mass_unit_to_kg=U_TO_KG, coordinate_unit_to_meter=BOHR_TO_M,
        stride=SAMPLE_STRIDE,
    )
    stresses = []
    for sample in density.samples:
        evaluated = evaluate_flibe_periodic_polarizable_stress(
            model,
            FLiBeConfiguration(run.trajectory.states[sample.state_index].configuration),
            CellStrainDifferentiation(step=STRAIN_STEP),
        )
        if evaluated.source_file_sha256 != run.source_file_sha256:
            raise ValueError("stress and MD parameter source fingerprints differ")
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
        source_id="FLIBE-BLOCKS-MEASURED-PRESSURE",
        provenance=PROVENANCE,
    )
    thermal = evaluate_flibe_frame_thermodynamics(
        run.trajectory, pressure, degrees_of_freedom=3 * (len(SPECIES) - 1),
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED_UNCLASSIFIED_BENCHMARK_STATE",
    )
    return run, thermal


def _independent_stats(values: tuple[float, ...], size: int) -> dict[str, object]:
    means = tuple(mean(values[i:i + size]) for i in range(0, len(values), size))
    midpoint = len(means) // 2
    return {
        "mean": mean(values),
        "block_means": means,
        "sample_standard_deviation": stdev(values),
        "block_mean_standard_error": stdev(means) / sqrt(len(means)),
        "second_half_minus_first_half": mean(means[midpoint:]) - mean(means[:midpoint]),
    }


def _series_dict(observation) -> dict[str, object]:
    return {
        "unit": observation.unit,
        "mean": observation.mean,
        "sample_standard_deviation": observation.sample_standard_deviation,
        "block_means": list(observation.block_means),
        "block_mean_standard_error": observation.block_mean_standard_error,
        "second_half_minus_first_half": observation.second_half_minus_first_half,
        "lag_one_block_correlation": observation.lag_one_block_correlation,
    }


def _matches(observation, independently) -> bool:
    for name in (
        "mean", "sample_standard_deviation", "block_mean_standard_error",
        "second_half_minus_first_half",
    ):
        if not isclose(getattr(observation, name), independently[name],
                       rel_tol=1.0e-11, abs_tol=1.0e-10):
            return False
    return len(observation.block_means) == len(independently["block_means"]) and all(
        isclose(a, b, rel_tol=1.0e-11, abs_tol=1.0e-10)
        for a, b in zip(observation.block_means, independently["block_means"], strict=True)
    )


def run_benchmark() -> dict[str, object]:
    """Execute one registered trajectory and independently audit all partitions."""
    run, thermal = _thermodynamic_trajectory()
    pressure_trace = thermal.pressure_trace
    density_trace = pressure_trace.density_trace
    raw = {
        "temperature": tuple(sample.kinetic_temperature_k for sample in thermal.samples),
        "pressure": tuple(sample.scalar_pressure_pa for sample in pressure_trace.samples),
        "density": tuple(sample.density_kg_m3 for sample in density_trace.samples),
    }
    windows = []
    individual_checks = []
    for window_id, size, discard in BLOCK_WINDOWS:
        observation = evaluate_flibe_trajectory_block_statistics(
            thermal, block_size_samples=size, discarded_initial_samples=discard,
        )
        names = ("temperature", "pressure", "density")
        own = {name: _independent_stats(raw[name][discard:], size) for name in names}
        individual_checks.append(all(
            _matches(getattr(observation, name), own[name]) for name in names
        ))
        windows.append({
            "window_id": window_id,
            "block_size_samples": size,
            "discarded_initial_samples": discard,
            "discarded_tail_samples": observation.discarded_tail_samples,
            "block_count": observation.block_count,
            "selected_sample_count": observation.selected_sample_count,
            "sampling_interval_s": observation.sampling_interval_s,
            "first_state_index": observation.blocks[0].first_state_index,
            "last_state_index": observation.blocks[-1].last_state_index,
            "block_state_ranges": [
                [block.first_state_index, block.last_state_index]
                for block in observation.blocks
            ],
            "temperature": _series_dict(observation.temperature),
            "pressure": _series_dict(observation.pressure),
            "density": _series_dict(observation.density),
        })

    base, wider, discard_eight, discard_sixteen = windows
    sensitivity = {
        name: {
            "eight_frame_minus_four_frame_mean": wider[name]["mean"] - base[name]["mean"],
            "discard_eight_minus_full_mean": discard_eight[name]["mean"] - base[name]["mean"],
            "discard_sixteen_minus_full_mean": discard_sixteen[name]["mean"] - base[name]["mean"],
            "eight_frame_minus_four_frame_standard_error": (
                wider[name]["block_mean_standard_error"]
                - base[name]["block_mean_standard_error"]
            ),
        }
        for name in ("temperature", "pressure", "density")
    }
    diagnostics = {}
    for name in ("temperature", "pressure", "density"):
        full = base[name]
        coarser = wider[name]
        late = discard_sixteen[name]
        shift = late["mean"] - full["mean"]
        combined_error = hypot(
            full["block_mean_standard_error"],
            late["block_mean_standard_error"],
        )
        scaled_shift = (
            abs(shift) / combined_error if combined_error > 0.0
            else (0.0 if shift == 0.0 else None)
        )
        largest_error = max(
            full["block_mean_standard_error"],
            coarser["block_mean_standard_error"],
        )
        error_change = (
            abs(coarser["block_mean_standard_error"]
                - full["block_mean_standard_error"]) / largest_error
            if largest_error > 0.0 else 0.0
        )
        adjacent_correlation = full["lag_one_block_correlation"]
        constant = full["sample_standard_deviation"] == 0.0
        correlation_condition = (
            adjacent_correlation is not None
            and abs(adjacent_correlation) <= MAX_ABS_ADJACENT_BLOCK_CORRELATION
        )
        window_condition = (
            scaled_shift is not None
            and scaled_shift <= MAX_WINDOW_MEAN_SHIFT_SCALED_BY_SE
        )
        block_condition = error_change <= MAX_BLOCK_SE_CHANGE_FRACTION
        diagnostics[name] = {
            "mean_shift_last_sixteen_minus_full": shift,
            "mean_shift_scaled_by_quadrature_block_se": scaled_shift,
            "block_se_change_fraction": error_change,
            "lag_one_block_correlation": adjacent_correlation,
            "weak_adjacent_block_correlation": correlation_condition,
            "window_mean_shift_within_threshold": window_condition,
            "block_size_se_within_threshold": block_condition,
            "diagnostic_status": (
                "FIXED_CELL_CONSTANT" if constant else
                ("SCREENING_CRITERIA_MET" if (
                    correlation_condition and window_condition and block_condition
                ) else "SCREENING_CRITERIA_FLAGGED")
            ),
        }

    sampling = []
    for temp, pressure, density in zip(
        thermal.samples, pressure_trace.samples, density_trace.samples, strict=True,
    ):
        sampling.append({
            "state_index": temp.state_index,
            "md_step": temp.md_step,
            "md_time_code": temp.md_time,
            "kinetic_temperature_k": temp.kinetic_temperature_k,
            "kinetic_energy_j": temp.kinetic_energy_j,
            "signed_pressure_pa": pressure.scalar_pressure_pa,
            "kinetic_pressure_pa": temp.kinetic_pressure_pa,
            "configurational_pressure_pa": fsum(
                pressure.configurational_tensor_pa[a][a] for a in range(3)
            ) / 3.0,
            "density_kg_m3": density.density_kg_m3,
            "volume_m3": density.cell_volume_m3,
        })

    checks = {
        "registered_parameter_fingerprint": (
            run.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
            and run.evaluations[0].source_doi == SOURCE_DOI
        ),
        "expected_species_and_periodic_cell": (
            run.trajectory.initial.configuration.species == SPECIES
            and all(state.configuration.periodic == (True, True, True)
                    and state.configuration.cell == run.trajectory.initial.configuration.cell
                    for state in run.trajectory.states)
        ),
        "exact_stride_and_sample_count": (
            [sample.state_index for sample in density_trace.samples]
            == list(range(0, INTEGRATION_STEPS + 1, SAMPLE_STRIDE))
            and len(sampling) == 32
        ),
        "density_mass_volume_identity": all(isclose(
            sample["density_kg_m3"], density_trace.total_mass_kg / sample["volume_m3"],
            rel_tol=1.0e-12,
        ) for sample in sampling),
        "aligned_thermodynamic_samples": all(
            sample["state_index"] == sample["md_step"]
            and isclose(sample["md_time_code"], sample["md_step"] * TIME_STEP_CODE,
                        rel_tol=1.0e-12, abs_tol=1.0e-15)
            for sample in sampling
        ),
        "kinetic_temperature_identity": all(isclose(
            sample["kinetic_temperature_k"],
            2 * sample["kinetic_energy_j"]
            / (3 * (len(SPECIES) - 1) * BOLTZMANN_CONSTANT_J_PER_K),
            rel_tol=1.0e-12,
        ) for sample in sampling),
        "signed_pressure_decomposition": all(isclose(
            sample["signed_pressure_pa"],
            sample["kinetic_pressure_pa"] + sample["configurational_pressure_pa"],
            rel_tol=1.0e-12, abs_tol=1.0e-3,
        ) for sample in sampling),
        "initial_kinetic_temperature_target": isclose(
            sampling[0]["kinetic_temperature_k"], TEMPERATURE_TARGET_K,
            rel_tol=1.0e-12,
        ),
        "predeclared_nonoverlapping_block_windows": (
            [(item["block_size_samples"], item["discarded_initial_samples"],
              item["block_count"]) for item in windows]
            == [(4, 0, 8), (8, 0, 4), (4, 8, 6), (4, 16, 4)]
            and all(item["discarded_tail_samples"] == 0 for item in windows)
        ),
        "independently_recomputed_block_moments": all(individual_checks),
        "block_grouping_preserves_full_sample_mean": all(isclose(
            base[name]["mean"], wider[name]["mean"],
            rel_tol=1.0e-12, abs_tol=1.0e-10,
        ) for name in ("temperature", "pressure", "density")),
        "finite_sampling_diagnostics": all(isfinite(number) for item in windows
            for name in ("temperature", "pressure", "density")
            for key in ("mean", "sample_standard_deviation",
                        "block_mean_standard_error", "second_half_minus_first_half")
            for number in (item[name][key],)),
        "constant_fixed_cell_density": all(isclose(
            value, raw["density"][0], rel_tol=1.0e-12,
        ) for value in raw["density"]),
        "finite_md_energy_drift": isfinite(run.maximum_absolute_energy_change_hartree)
                                    and run.maximum_absolute_energy_change_hartree >= 0.0,
        "sampling_diagnostic_bookkeeping": all(
            diagnostic["diagnostic_status"] in (
                "FIXED_CELL_CONSTANT", "SCREENING_CRITERIA_MET",
                "SCREENING_CRITERIA_FLAGGED",
            ) and all(value is None or isfinite(value) for value in (
                diagnostic["mean_shift_scaled_by_quadrature_block_se"],
                diagnostic["block_se_change_fraction"],
                diagnostic["lag_one_block_correlation"],
            ))
            for diagnostic in diagnostics.values()
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source": {
            "doi": SOURCE_DOI,
            "relative_path": SOURCE_RELATIVE,
            "sha256": run.source_file_sha256,
            "provenance": "PRIMARY_SOURCE",
        },
        "protocol": {
            "model_id": MODEL_ID,
            "trajectory_id": TRAJECTORY_ID,
            "ensemble": "NVE_FIXED_CELL",
            "velocity_frame": "CENTER_OF_MASS",
            "physical_state_id": thermal.physical_state_id,
            "cell_edge_bohr": EDGE_BOHR,
            "species": list(SPECIES),
            "kinetic_temperature_initial_target_k": TEMPERATURE_TARGET_K,
            "time_step_code": TIME_STEP_CODE,
            "time_unit_to_second": TIME_TO_S,
            "integration_steps": INTEGRATION_STEPS,
            "sample_stride": SAMPLE_STRIDE,
            "strain_step": STRAIN_STEP,
            "block_windows": [list(item) for item in BLOCK_WINDOWS],
            "statistical_interpretation": "SAMPLING_WINDOW_AND_BLOCK_SIZE_SENSITIVITY",
        },
        "trajectory": {
            "sample_count": len(sampling),
            "total_cell_mass_kg": density_trace.total_mass_kg,
            "maximum_absolute_energy_drift_hartree": run.maximum_absolute_energy_change_hartree,
            "samples": sampling,
        },
        "windows": windows,
        "sensitivity": sensitivity,
        "statistical_screening": {
            "scope": "DIAGNOSTIC_SAMPLING_CRITERIA",
            "max_abs_adjacent_block_correlation": MAX_ABS_ADJACENT_BLOCK_CORRELATION,
            "max_block_se_change_fraction": MAX_BLOCK_SE_CHANGE_FRACTION,
            "max_window_mean_shift_scaled_by_se": MAX_WINDOW_MEAN_SHIFT_SCALED_BY_SE,
            "comparison_windows_overlap": True,
            "observables": diagnostics,
        },
    }


if __name__ == "__main__":
    result = run_benchmark()
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
