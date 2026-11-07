"""Fixed-cell periodic FLiBe structural-relaxation benchmark.

Three declared Li2BeF4 cells use the same fractional atomic geometry and
source-registered polarizable potential. The Armijo trajectory records total
energy, Cartesian force norms, fluoride-dipole stationarity, accepted step
sizes, and terminal reason. A second iteration budget checks prefix stability;
a translated initial structure checks covariance of the final configuration.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from math import floor, fsum, isclose, isfinite, sqrt
from pathlib import Path

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.periodic_structural_relaxation import (
    FLiBeRelaxationStopReason,
    FLiBeStructuralRelaxationSettings,
    relax_flibe_periodic_structure,
)
from tr_eif.flibe.registered_pair_coefficients import SOURCE_DOI, load_flibe_registered_pair_parameters
from tr_eif.flibe.units import ParameterProvenance

BENCHMARK_ID = "tr-eif.flibe.periodic-structural-relaxation.v1"
MODEL_ID = "FLIBE-STRUCTURAL-RELAXATION-BENCHMARK"
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SOURCE_RELATIVE_PATH = "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
BASE_EDGE_BOHR = 18.0
BASE_POSITIONS_BOHR = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
CELL_EDGES_BOHR = (9.0, 10.0, 12.0)
SHORT_BUDGET = 8
LONG_BUDGET = 24
LONG_BUDGET_EDGE_BOHR = 10.0
TRANSLATION_BOHR = (0.41, -0.27, 0.31)
STATIONARITY_TOLERANCE_ATOMIC = 1.0e-10
FORCE_TOLERANCE_HARTREE_PER_BOHR = 1.0e-5
MAXIMUM_DISPLACEMENT_BOHR = 0.08
MAXIMUM_LINE_SEARCH_TRIALS = 16


def _model() -> FLiBePeriodicPolarizableModel:
    parameters = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25, real_image_shell=1, reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0, provenance=ParameterProvenance.BENCHMARK,
        source_id="FLIBE-STRUCTURAL-RELAXATION-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-STRUCTURAL-RELAXATION-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-STRUCTURAL-RELAXATION-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-STRUCTURAL-RELAXATION-SHORT", parameters=parameters,
                coordinate_unit_to_bohr=1.0, image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-STRUCTURAL-RELAXATION-DIPOLES", parameters=parameters,
            ewald_parameters=ewald, damping_image_shell=1,
            stationarity_absolute_tolerance=STATIONARITY_TOLERANCE_ATOMIC,
        ),
    )


def _configuration(edge: float, shift=(0.0, 0.0, 0.0)) -> FLiBeConfiguration:
    factor = edge / BASE_EDGE_BOHR
    cell = ((edge, 0.0, 0.0), (0.0, edge, 0.0), (0.0, 0.0, edge))
    coordinates = tuple(
        tuple(factor * row[axis] + shift[axis] for axis in range(3))
        for row in BASE_POSITIONS_BOHR
    )
    return FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES, positions=coordinates, cell=cell, periodic=(True, True, True),
    ))


def _minimum_periodic_pair_distance(positions, edge: float) -> float:
    separations = []
    for index, first in enumerate(positions):
        for second in positions[index + 1:]:
            differences = tuple(
                (first[axis] - second[axis])
                - edge * floor((first[axis] - second[axis]) / edge + 0.5)
                for axis in range(3)
            )
            separations.append(sqrt(fsum(x * x for x in differences)))
    return min(separations)


def _maximum_geometric_center_shift(first, last) -> float:
    n = len(first)
    return max(abs(
        fsum(point[axis] for point in last) / n
        - fsum(point[axis] for point in first) / n
    ) for axis in range(3))


def _run(model, edge: float, iterations: int, shift=(0.0, 0.0, 0.0)):
    settings = FLiBeStructuralRelaxationSettings(
        maximum_iterations=iterations,
        maximum_trials_per_iteration=MAXIMUM_LINE_SEARCH_TRIALS,
        force_tolerance_hartree_per_bohr=FORCE_TOLERANCE_HARTREE_PER_BOHR,
        maximum_atom_displacement_bohr=MAXIMUM_DISPLACEMENT_BOHR,
        minimum_atom_displacement_bohr=1.0e-10,
        backtrack_factor=0.5,
        armijo_fraction=1.0e-4,
    )
    return relax_flibe_periodic_structure(
        _configuration(edge, shift), model, settings=settings,
    )


def _record(model, edge: float, result) -> dict[str, object]:
    first = result.initial_configuration.configuration
    final = result.final_configuration.configuration
    evaluation = model.evaluate(result.final_configuration)
    max_force = max(
        sqrt(fsum(component * component for component in row))
        / evaluation.coordinate_unit_to_bohr
        for row in evaluation.forces.forces
    )
    max_net_force = max(
        abs(fsum(row[axis] for row in evaluation.forces.forces))
        for axis in range(3)
    )
    return {
        "cell_edge_bohr": edge,
        "cell_volume_bohr3": edge**3,
        "iteration_budget": result.settings.maximum_iterations,
        "accepted_steps": result.accepted_steps,
        "stop_reason": result.stop_reason.value,
        "force_threshold_reached": result.converged,
        "initial_energy_hartree": result.initial_energy_hartree,
        "final_energy_hartree": result.final_energy_hartree,
        "initial_maximum_force_hartree_per_bohr": result.initial_maximum_force_hartree_per_bohr,
        "final_maximum_force_hartree_per_bohr": result.final_maximum_force_hartree_per_bohr,
        "direct_final_maximum_force_hartree_per_bohr": max_force,
        "direct_final_net_force_maximum_component_hartree_per_bohr": max_net_force,
        "final_dipole_stationarity_residual_atomic": result.final_dipole_stationarity_atomic,
        "direct_final_dipole_stationarity_residual_atomic": evaluation.max_stationarity_residual_atomic,
        "source_file_sha256": result.source_file_sha256,
        "source_doi": result.source_doi,
        "fixed_cell_retained": first.cell == final.cell and first.periodic == final.periodic,
        "species_retained": first.species == final.species,
        "maximum_geometric_center_shift_bohr": _maximum_geometric_center_shift(
            first.positions, final.positions,
        ),
        "minimum_initial_periodic_pair_distance_bohr": _minimum_periodic_pair_distance(first.positions, edge),
        "minimum_final_periodic_pair_distance_bohr": _minimum_periodic_pair_distance(final.positions, edge),
        "initial_positions_bohr": [list(point) for point in first.positions],
        "final_positions_bohr": [list(point) for point in final.positions],
        "accepted_step_history": [asdict(step) for step in result.steps],
        "direct_final_energy_hartree": evaluation.energy.total_energy,
        "direct_final_energy_component_sum_hartree": fsum(
            value for _, value in evaluation.energy_components_hartree
        ),
    }


def run_benchmark() -> dict[str, object]:
    """Evaluate declared cells, the extended budget, and two replay symmetries."""
    model = _model()
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    short_results = {edge: _run(model, edge, SHORT_BUDGET) for edge in CELL_EDGES_BOHR}
    long_result = _run(model, LONG_BUDGET_EDGE_BOHR, LONG_BUDGET)
    cases = [
        _record(model, edge, short_results[edge]) for edge in CELL_EDGES_BOHR
    ] + [_record(model, LONG_BUDGET_EDGE_BOHR, long_result)]
    short_reference = short_results[LONG_BUDGET_EDGE_BOHR]
    replay = _run(model, LONG_BUDGET_EDGE_BOHR, SHORT_BUDGET)
    translated = _run(model, LONG_BUDGET_EDGE_BOHR, SHORT_BUDGET, TRANSLATION_BOHR)
    position_difference = max(
        abs(point[axis] - reference[axis] - TRANSLATION_BOHR[axis])
        for point, reference in zip(
            translated.final_configuration.configuration.positions,
            short_reference.final_configuration.configuration.positions,
            strict=True,
        ) for axis in range(3)
    )
    translation_energy_difference = abs(
        translated.final_energy_hartree - short_reference.final_energy_hartree
    )
    checks = {
        "registered_parameter_source": all(
            row["source_file_sha256"] == source_hash and row["source_doi"] == SOURCE_DOI
            for row in cases
        ),
        "declared_cell_and_species_conservation": all(
            row["fixed_cell_retained"] and row["species_retained"] for row in cases
        ),
        "energy_monotone_on_accepted_steps": all(
            row["final_energy_hartree"] <= row["initial_energy_hartree"]
            and all(step["energy_after_hartree"] < step["energy_before_hartree"]
                    for step in row["accepted_step_history"])
            for row in cases
        ),
        "energy_step_chain_complete": all(
            row["accepted_steps"] == len(row["accepted_step_history"])
            and all(a["energy_after_hartree"] == b["energy_before_hartree"]
                    for a, b in zip(row["accepted_step_history"],
                                    row["accepted_step_history"][1:]))
            for row in cases
        ),
        "displacement_and_trial_limits": all(
            0.0 < step["maximum_atom_displacement_bohr"] <= MAXIMUM_DISPLACEMENT_BOHR * (1.0 + 1.0e-12)
            and 1 <= step["line_search_trials"] <= MAXIMUM_LINE_SEARCH_TRIALS
            for row in cases for step in row["accepted_step_history"]
        ),
        "stop_reason_matches_force_and_budget": all(
            (row["force_threshold_reached"]
             == (row["stop_reason"] == FLiBeRelaxationStopReason.FORCE_TOLERANCE.value))
            and (row["stop_reason"] != FLiBeRelaxationStopReason.MAXIMUM_ITERATIONS.value
                 or row["accepted_steps"] == row["iteration_budget"])
            and (row["stop_reason"] != FLiBeRelaxationStopReason.FORCE_TOLERANCE.value
                 or row["final_maximum_force_hartree_per_bohr"] <= FORCE_TOLERANCE_HARTREE_PER_BOHR)
            for row in cases
        ),
        "independent_final_energy_and_force": all(
            isclose(row["final_energy_hartree"], row["direct_final_energy_hartree"], rel_tol=1.0e-12)
            and isclose(row["final_energy_hartree"], row["direct_final_energy_component_sum_hartree"], rel_tol=1.0e-12)
            and isclose(row["final_maximum_force_hartree_per_bohr"], row["direct_final_maximum_force_hartree_per_bohr"], rel_tol=1.0e-12)
            for row in cases
        ),
        "final_dipole_stationarity": all(
            row["final_dipole_stationarity_residual_atomic"] <= STATIONARITY_TOLERANCE_ATOMIC
            and row["direct_final_dipole_stationarity_residual_atomic"] <= STATIONARITY_TOLERANCE_ATOMIC
            for row in cases
        ),
        "net_force_balance": all(
            row["direct_final_net_force_maximum_component_hartree_per_bohr"] <= 1.0e-10
            for row in cases
        ),
        "geometric_center_invariance": all(
            row["maximum_geometric_center_shift_bohr"] <= 1.0e-12 for row in cases
        ),
        "positive_pair_separation": all(
            row["minimum_initial_periodic_pair_distance_bohr"] > 0.0
            and row["minimum_final_periodic_pair_distance_bohr"] > 0.0
            for row in cases
        ),
        "extended_budget_reuses_exact_prefix": (
            short_reference.steps == long_result.steps[:short_reference.accepted_steps]
        ),
        "deterministic_identical_input_replay": replay == short_reference,
        "translation_covariance": (
            position_difference <= 1.0e-10 and translation_energy_difference <= 1.0e-11
        ),
        "finite_recorded_observables": all(
            isfinite(row[key]) for row in cases for key in (
                "initial_energy_hartree", "final_energy_hartree",
                "initial_maximum_force_hartree_per_bohr",
                "final_maximum_force_hartree_per_bohr",
                "final_dipole_stationarity_residual_atomic",
                "minimum_final_periodic_pair_distance_bohr",
            )
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source": {
            "doi": SOURCE_DOI,
            "relative_path": SOURCE_RELATIVE_PATH,
            "sha256": source_hash,
            "provenance": "PRIMARY_SOURCE",
        },
        "method": {
            "model_id": MODEL_ID,
            "periodic_axes": [True, True, True],
            "species": list(SPECIES),
            "cell_edges_bohr": list(CELL_EDGES_BOHR),
            "short_iteration_budget": SHORT_BUDGET,
            "long_iteration_budget": LONG_BUDGET,
            "long_iteration_cell_edge_bohr": LONG_BUDGET_EDGE_BOHR,
            "force_tolerance_hartree_per_bohr": FORCE_TOLERANCE_HARTREE_PER_BOHR,
            "maximum_atom_displacement_bohr": MAXIMUM_DISPLACEMENT_BOHR,
            "maximum_line_search_trials": MAXIMUM_LINE_SEARCH_TRIALS,
            "translation_bohr": list(TRANSLATION_BOHR),
            "relaxation_state": "FIXED_CELL_ZERO_K_POTENTIAL_ENERGY_MINIMIZATION",
        },
        "translation_replay": {
            "maximum_final_position_covariance_error_bohr": position_difference,
            "absolute_final_energy_difference_hartree": translation_energy_difference,
        },
        "cases": cases,
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if report["status"] == "PASS" else 1)
