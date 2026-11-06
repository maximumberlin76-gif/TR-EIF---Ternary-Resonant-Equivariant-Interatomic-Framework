"""Size-dependent runtime and Python allocation measurements for periodic FLiBe.

The published Li/Be/F pair table, Ewald shells, fluoride polarizability,
charge-dipole damping, and stationary solver are held fixed. One, two,
and four translated Li2BeF4 formula-unit fixtures occupy correspondingly
replicated periodic cells. Each run evaluates the complete potential,
including the reoptimized fluoride dipoles, energy, and Cartesian forces.

Wall-clock measurements cover model.evaluate only and exclude model and
configuration construction. Python allocation peaks are measured separately
with tracemalloc; they refer to traced Python allocations, not process RSS.
Numerical checks and timing/memory observations are recorded separately.
"""

from __future__ import annotations

import gc
import hashlib
import json
from math import fsum, isfinite
from pathlib import Path
from statistics import median
from time import perf_counter_ns
import tracemalloc

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_pair_coefficients import SOURCE_DOI, load_flibe_registered_pair_parameters
from tr_eif.flibe.units import ParameterProvenance


BENCHMARK_ID = "tr-eif.flibe.periodic-polarizable-size-scaling.v1"
SOURCE_RELATIVE_PATH = "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SOURCE_PATH = Path(__file__).resolve().parents[2] / SOURCE_RELATIVE_PATH
MODEL_ID = "FLIBE-PERIODIC-POLARIZABLE-SIZE-SCALING"
BASE_SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
BASE_POSITIONS_BOHR = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
CELL_EDGE_BOHR = 18.0
REPLICA_SHAPES = ((1, 1, 1), (2, 1, 1), (2, 2, 1))
TIME_REPEATS = 3
EWALD_ALPHA_INVERSE_BOHR = 0.25
EWALD_REAL_SHELL = 1
EWALD_RECIPROCAL_SHELL = 3
SHORT_RANGE_SHELL = 1
DAMPING_IMAGE_SHELL = 1
STATIONARITY_TOLERANCE = 1.0e-10
MAXIMUM_NET_FORCE_HARTREE_PER_BOHR = 1.0e-10
ENERGY_COMPONENT_TOLERANCE_HARTREE = 1.0e-10


def _model() -> FLiBePeriodicPolarizableModel:
    source = load_flibe_registered_pair_parameters(SOURCE_PATH)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=EWALD_ALPHA_INVERSE_BOHR,
        real_image_shell=EWALD_REAL_SHELL,
        reciprocal_image_shell=EWALD_RECIPROCAL_SHELL,
        coordinate_unit_to_bohr=1.0,
        provenance=ParameterProvenance.BENCHMARK,
        source_id="BENCHMARK:FLIBE-PERIODIC-SIZE-SCALING-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-SCALING-FIXED-CHARGE",
            ewald_model=FLiBePeriodicEwaldModel("FLIBE-SCALING-EWALD", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-SCALING-SHORT-RANGE",
                parameters=source,
                coordinate_unit_to_bohr=1.0,
                image_shell=SHORT_RANGE_SHELL,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-SCALING-POLARIZATION",
            parameters=source,
            ewald_parameters=ewald,
            damping_image_shell=DAMPING_IMAGE_SHELL,
            stationarity_absolute_tolerance=STATIONARITY_TOLERANCE,
        ),
    )


def _configuration(shape: tuple[int, int, int]) -> FLiBeConfiguration:
    nx, ny, nz = shape
    species: list[str] = []
    positions: list[tuple[float, float, float]] = []
    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                offset = (
                    CELL_EDGE_BOHR * ix,
                    CELL_EDGE_BOHR * iy,
                    CELL_EDGE_BOHR * iz,
                )
                species.extend(BASE_SPECIES)
                positions.extend(
                    tuple(point[a] + offset[a] for a in range(3))
                    for point in BASE_POSITIONS_BOHR
                )
    cell = (
        (CELL_EDGE_BOHR * nx, 0.0, 0.0),
        (0.0, CELL_EDGE_BOHR * ny, 0.0),
        (0.0, 0.0, CELL_EDGE_BOHR * nz),
    )
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species), positions=tuple(positions),
        cell=cell, periodic=(True, True, True),
    ))


def _measure(model: FLiBePeriodicPolarizableModel,
             configuration: FLiBeConfiguration,
             replica_shape: tuple[int, int, int]) -> dict[str, object]:
    times_ns: list[int] = []
    reference = None
    replay_equal = True
    for _ in range(TIME_REPEATS):
        start = perf_counter_ns()
        current = model.evaluate(configuration)
        elapsed = perf_counter_ns() - start
        times_ns.append(elapsed)
        if reference is None:
            reference = current
        else:
            replay_equal = replay_equal and (
                current.energy == reference.energy
                and current.forces == reference.forces
                and current.polarization_force_result.polarization_result.induced_dipoles_e_bohr
                == reference.polarization_force_result.polarization_result.induced_dipoles_e_bohr
            )
    assert reference is not None

    gc.collect()
    tracemalloc.start()
    tracemalloc.reset_peak()
    try:
        measured = model.evaluate(configuration)
        current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    replay_equal = replay_equal and measured.energy == reference.energy and measured.forces == reference.forces

    atom_count = configuration.atom_count
    formula_units = atom_count // len(BASE_SPECIES)
    fluoride_count = configuration.species.count("F")
    energy_components = reference.energy_components_hartree
    net_force = max(abs(fsum(force[axis] for force in reference.forces.forces)) for axis in range(3))
    ewald = reference.fixed_charge_result.ewald_result
    short = reference.fixed_charge_result.short_range_result
    pol = reference.polarization_force_result.polarization_result

    return {
        "replica_shape": list(replica_shape),
        "formula_unit_count": formula_units,
        "atom_count": atom_count,
        "fluoride_count": fluoride_count,
        "cell_volume_bohr3": CELL_EDGE_BOHR**3 * formula_units,
        "formal_charge_total_e": sum(ewald.formal_charges_e),
        "real_terms_evaluated": ewald.real_terms_evaluated,
        "reciprocal_vectors_evaluated": ewald.reciprocal_vectors_evaluated,
        "short_range_cross_image_terms": short.cross_atom_image_terms,
        "short_range_self_image_terms": short.self_atom_image_terms,
        "polarization_hessian_dimension": 3 * fluoride_count,
        "total_energy_hartree": reference.energy.total_energy,
        "energy_per_formula_unit_hartree": reference.energy.total_energy / formula_units,
        "energy_component_count": len(energy_components),
        "energy_component_sum_hartree": fsum(value for _, value in energy_components),
        "maximum_net_force_hartree_per_bohr": net_force,
        "maximum_dipole_stationarity_residual_atomic": pol.max_stationarity_residual_atomic,
        "timing_ns": times_ns,
        "median_wall_time_seconds": median(times_ns) * 1.0e-9,
        "peak_traced_python_bytes": peak_bytes,
        "traced_python_bytes_after_evaluation": current_bytes,
        "deterministic_numerical_replay": replay_equal,
        "source_file_sha256": reference.source_file_sha256,
    }


def run_benchmark() -> dict[str, object]:
    """Measure full periodic-potential evaluation at three fixed cell sizes."""
    model = _model()
    source_hash = hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest()
    measurements = tuple(_measure(model, _configuration(shape), shape) for shape in REPLICA_SHAPES)
    checks = {
        "published_source_identity": model.fixed_charge_model.short_range_model.parameters.source_doi == SOURCE_DOI,
        "source_fingerprint": all(row["source_file_sha256"] == source_hash for row in measurements),
        "formula_unit_cardinality": all(
            row["formula_unit_count"] == shape[0] * shape[1] * shape[2]
            for row, shape in zip(measurements, REPLICA_SHAPES, strict=True)
        ),
        "balanced_species_inventory": all(
            row["atom_count"] == 7 * row["formula_unit_count"]
            and row["fluoride_count"] == 4 * row["formula_unit_count"]
            for row in measurements
        ),
        "neutral_charge": all(row["formal_charge_total_e"] == 0 for row in measurements),
        "periodic_cell_volume": all(
            row["cell_volume_bohr3"] == CELL_EDGE_BOHR**3 * row["formula_unit_count"]
            for row in measurements
        ),
        "ewald_real_term_count": all(
            row["real_terms_evaluated"] == row["atom_count"]**2 * (2*EWALD_REAL_SHELL+1)**3 - row["atom_count"]
            for row in measurements
        ),
        "ewald_reciprocal_term_count": all(
            row["reciprocal_vectors_evaluated"] == (2*EWALD_RECIPROCAL_SHELL+1)**3 - 1
            for row in measurements
        ),
        "short_range_cross_term_count": all(
            row["short_range_cross_image_terms"] == row["atom_count"] * (row["atom_count"]-1) // 2 * (2*SHORT_RANGE_SHELL+1)**3
            for row in measurements
        ),
        "short_range_self_term_count": all(
            row["short_range_self_image_terms"] == row["atom_count"] * ((2*SHORT_RANGE_SHELL+1)**3-1)
            for row in measurements
        ),
        "polarization_hessian_cardinality": all(
            row["polarization_hessian_dimension"] == 12 * row["formula_unit_count"]
            for row in measurements
        ),
        "energy_decomposition": all(
            row["energy_component_count"] == 8
            and abs(row["energy_component_sum_hartree"]-row["total_energy_hartree"]) <= ENERGY_COMPONENT_TOLERANCE_HARTREE
            for row in measurements
        ),
        "stationarity": all(
            row["maximum_dipole_stationarity_residual_atomic"] <= STATIONARITY_TOLERANCE
            for row in measurements
        ),
        "force_balance": all(
            row["maximum_net_force_hartree_per_bohr"] <= MAXIMUM_NET_FORCE_HARTREE_PER_BOHR
            for row in measurements
        ),
        "deterministic_numerical_replay": all(row["deterministic_numerical_replay"] is True for row in measurements),
        "runtime_measurements": all(
            len(row["timing_ns"]) == TIME_REPEATS
            and all(type(t) is int and t > 0 for t in row["timing_ns"])
            and isfinite(row["median_wall_time_seconds"])
            and row["median_wall_time_seconds"] > 0
            for row in measurements
        ),
        "memory_measurements": all(
            type(row["peak_traced_python_bytes"]) is int
            and row["peak_traced_python_bytes"] > 0
            and row["peak_traced_python_bytes"] >= row["traced_python_bytes_after_evaluation"] >= 0
            for row in measurements
        ),
        "finite_numeric_outputs": all(
            isfinite(row[key])
            for row in measurements
            for key in ("total_energy_hartree", "energy_per_formula_unit_hartree", "maximum_net_force_hartree_per_bohr", "maximum_dipole_stationarity_residual_atomic")
        ),
    }
    ratios = tuple({
        "from_atom_count": first["atom_count"],
        "to_atom_count": second["atom_count"],
        "median_runtime_ratio": second["median_wall_time_seconds"] / first["median_wall_time_seconds"],
        "peak_python_allocation_ratio": second["peak_traced_python_bytes"] / first["peak_traced_python_bytes"],
    } for first, second in zip(measurements[:-1], measurements[1:], strict=True))
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
            "provenance": "BENCHMARK",
            "base_species": list(BASE_SPECIES),
            "base_positions_bohr": [list(point) for point in BASE_POSITIONS_BOHR],
            "base_cell_edge_bohr": CELL_EDGE_BOHR,
            "replica_shapes": [list(shape) for shape in REPLICA_SHAPES],
            "ewald_alpha_inverse_bohr": EWALD_ALPHA_INVERSE_BOHR,
            "ewald_real_shell": EWALD_REAL_SHELL,
            "ewald_reciprocal_shell": EWALD_RECIPROCAL_SHELL,
            "short_range_shell": SHORT_RANGE_SHELL,
            "damping_image_shell": DAMPING_IMAGE_SHELL,
            "stationarity_absolute_tolerance": STATIONARITY_TOLERANCE,
            "time_repeats": TIME_REPEATS,
            "runtime_measurement": "untraced_wall_clock_per_potential_evaluation",
            "memory_measurement": "peak_tracemalloc_python_allocations_during_one_evaluation",
        },
        "numerical_contract": {
            "energy_component_absolute_tolerance_hartree": ENERGY_COMPONENT_TOLERANCE_HARTREE,
            "maximum_net_force_hartree_per_bohr": MAXIMUM_NET_FORCE_HARTREE_PER_BOHR,
        },
        "measurements": list(measurements),
        "observed_size_ratios": list(ratios),
        "checks": checks,
    }


if __name__ == "__main__":
    result = run_benchmark()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
