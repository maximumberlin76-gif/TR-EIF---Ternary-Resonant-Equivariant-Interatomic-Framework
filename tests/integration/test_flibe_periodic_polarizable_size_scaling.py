
"""Independent qualification of periodic polarizable FLiBe size-scaling evidence.

The benchmark is executed through its command-line interface. The tests
recompute stoichiometry, periodic term counts, energy balances, timing
statistics, traced-allocation ratios, and source fingerprints from its
recorded measurements. A separately constructed potential checks the
seven-atom numerical reference and translation covariance of forces.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from math import fsum, isfinite, prod
from pathlib import Path
from statistics import median

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_pair_coefficients import load_flibe_registered_pair_parameters
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_polarizable_size_scaling.py"
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-polarizable-size-scaling.v1"
DATASET_ID = "tr-eif.flibe.smith-2020.pim-pair-coefficients.v1"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
SOURCE_RELATIVE_PATH = "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SHAPES = ((1, 1, 1), (2, 1, 1), (2, 2, 1))
ATOM_COUNTS = (7, 14, 28)
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0),
    (8.0, 0.0, 0.0),
    (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0),
    (8.0, 5.0, 6.0),
    (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
EDGE_BOHR = 18.0
REPEATS = 3
REAL_SHELL = 1
RECIPROCAL_SHELL = 3
SHORT_RANGE_SHELL = 1
STATIONARITY_LIMIT = 1.0e-10
FORCE_LIMIT = 1.0e-10
ENERGY_LIMIT = 1.0e-10
CHECK_NAMES = {
    "published_source_identity",
    "source_fingerprint",
    "formula_unit_cardinality",
    "balanced_species_inventory",
    "neutral_charge",
    "periodic_cell_volume",
    "ewald_real_term_count",
    "ewald_reciprocal_term_count",
    "short_range_cross_term_count",
    "short_range_self_term_count",
    "polarization_hessian_cardinality",
    "energy_decomposition",
    "stationarity",
    "force_balance",
    "deterministic_numerical_replay",
    "runtime_measurements",
    "memory_measurements",
    "finite_numeric_outputs",
}


def _finite(value: object, *, nonnegative: bool = False) -> float:
    assert type(value) in (int, float)
    number = float(value)
    assert isfinite(number)
    if nonnegative:
        assert number >= 0.0
    return number


def _integer(value: object, *, positive: bool = False) -> int:
    assert type(value) is int
    if positive:
        assert value > 0
    return value


def _measurements(document: dict[str, object]) -> list[dict[str, object]]:
    rows = document["measurements"]
    assert isinstance(rows, list) and len(rows) == len(SHAPES)
    assert all(isinstance(row, dict) for row in rows)
    return rows


def _execute() -> tuple[dict[str, object], bytes]:
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
        timeout=300,
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
def execution() -> tuple[dict[str, object], bytes]:
    return _execute()


@pytest.fixture(scope="module")
def report(execution) -> dict[str, object]:
    return execution[0]


def _check_source(document: dict[str, object]) -> None:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert document["source"] == {
        "doi": SOURCE_DOI,
        "relative_path": SOURCE_RELATIVE_PATH,
        "file_sha256": digest,
        "provenance": "PRIMARY_SOURCE",
    }
    assert all(row["source_file_sha256"] == digest for row in _measurements(document))


def _check_structure(document: dict[str, object]) -> None:
    for row, shape, atoms in zip(
        _measurements(document), SHAPES, ATOM_COUNTS, strict=True
    ):
        units = prod(shape)
        assert row["replica_shape"] == list(shape)
        assert _integer(row["formula_unit_count"], positive=True) == units
        assert _integer(row["atom_count"], positive=True) == atoms == 7 * units
        assert _integer(row["fluoride_count"], positive=True) == 4 * units
        assert _finite(row["formal_charge_total_e"]) == 0.0
        assert _finite(row["cell_volume_bohr3"]) == EDGE_BOHR**3 * units
        assert _integer(row["polarization_hessian_dimension"], positive=True) == 12 * units


def _check_interaction_counts(document: dict[str, object]) -> None:
    real_images = (2 * REAL_SHELL + 1) ** 3
    reciprocal_vectors = (2 * RECIPROCAL_SHELL + 1) ** 3 - 1
    short_images = (2 * SHORT_RANGE_SHELL + 1) ** 3
    for row in _measurements(document):
        atoms = row["atom_count"]
        assert _integer(row["real_terms_evaluated"], positive=True) == (
            atoms**2 * real_images - atoms
        )
        assert _integer(row["reciprocal_vectors_evaluated"], positive=True) == (
            reciprocal_vectors
        )
        assert _integer(row["short_range_cross_image_terms"], positive=True) == (
            atoms * (atoms - 1) // 2 * short_images
        )
        assert _integer(row["short_range_self_image_terms"], positive=True) == (
            atoms * (short_images - 1)
        )


def _check_energies_and_residuals(document: dict[str, object]) -> None:
    for row in _measurements(document):
        total = _finite(row["total_energy_hartree"])
        components = _finite(row["energy_component_sum_hartree"])
        per_unit = _finite(row["energy_per_formula_unit_hartree"])
        assert _integer(row["energy_component_count"]) == 8
        assert abs(components - total) <= ENERGY_LIMIT
        assert per_unit == pytest.approx(
            total / row["formula_unit_count"], rel=1.0e-13, abs=1.0e-13
        )
        assert _finite(
            row["maximum_net_force_hartree_per_bohr"], nonnegative=True
        ) <= FORCE_LIMIT
        assert _finite(
            row["maximum_dipole_stationarity_residual_atomic"], nonnegative=True
        ) <= STATIONARITY_LIMIT
        assert row["deterministic_numerical_replay"] is True


def _check_measurements(document: dict[str, object]) -> None:
    for row in _measurements(document):
        times = row["timing_ns"]
        assert isinstance(times, list) and len(times) == REPEATS
        assert all(_integer(item, positive=True) > 0 for item in times)
        assert _finite(row["median_wall_time_seconds"]) == pytest.approx(
            median(times) * 1.0e-9, rel=1.0e-12
        )
        peak = _integer(row["peak_traced_python_bytes"], positive=True)
        retained = _integer(row["traced_python_bytes_after_evaluation"])
        assert peak >= retained >= 0


def _check_size_ratios(document: dict[str, object]) -> None:
    rows = _measurements(document)
    ratios = document["observed_size_ratios"]
    assert isinstance(ratios, list) and len(ratios) == len(rows) - 1
    for first, second, record in zip(rows[:-1], rows[1:], ratios, strict=True):
        assert isinstance(record, dict)
        assert set(record) == {
            "from_atom_count",
            "to_atom_count",
            "median_runtime_ratio",
            "peak_python_allocation_ratio",
        }
        assert record["from_atom_count"] == first["atom_count"]
        assert record["to_atom_count"] == second["atom_count"]
        runtime_ratio = (
            median(second["timing_ns"]) / median(first["timing_ns"])
        )
        allocation_ratio = (
            second["peak_traced_python_bytes"] / first["peak_traced_python_bytes"]
        )
        assert _finite(record["median_runtime_ratio"]) == pytest.approx(
            runtime_ratio, rel=1.0e-12
        )
        assert _finite(record["peak_python_allocation_ratio"]) == pytest.approx(
            allocation_ratio, rel=1.0e-12
        )
        assert runtime_ratio > 0.0
        assert allocation_ratio > 0.0


def test_benchmark_identity_and_all_eighteen_gates(report) -> None:
    assert BENCHMARK.is_file() and SOURCE.is_file()
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert set(report["checks"]) == CHECK_NAMES
    assert all(value is True for value in report["checks"].values())


def test_source_fingerprint_matches_published_parameter_record(report) -> None:
    dataset = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert dataset["dataset_id"] == DATASET_ID
    assert dataset["record_kind"] == "PUBLISHED_INTERATOMIC_PARAMETER_TABLE"
    assert dataset["provenance"] == "PRIMARY_SOURCE"
    assert dataset["source"]["doi"] == SOURCE_DOI
    assert len(dataset["pair_coefficients"]) == 6
    _check_source(report)


def test_fixed_fixture_and_measurement_scope(report) -> None:
    fixture = report["fixture"]
    assert fixture["provenance"] == "BENCHMARK"
    assert fixture["base_species"] == list(SPECIES)
    assert fixture["base_positions_bohr"] == [list(point) for point in POSITIONS]
    assert fixture["base_cell_edge_bohr"] == EDGE_BOHR
    assert fixture["replica_shapes"] == [list(shape) for shape in SHAPES]
    assert fixture["ewald_alpha_inverse_bohr"] == 0.25
    assert fixture["ewald_real_shell"] == REAL_SHELL
    assert fixture["ewald_reciprocal_shell"] == RECIPROCAL_SHELL
    assert fixture["short_range_shell"] == SHORT_RANGE_SHELL
    assert fixture["damping_image_shell"] == 1
    assert fixture["stationarity_absolute_tolerance"] == STATIONARITY_LIMIT
    assert fixture["time_repeats"] == REPEATS
    assert fixture["runtime_measurement"] == "untraced_wall_clock_per_potential_evaluation"
    assert fixture["memory_measurement"] == (
        "peak_tracemalloc_python_allocations_during_one_evaluation"
    )
    assert report["numerical_contract"] == {
        "energy_component_absolute_tolerance_hartree": ENERGY_LIMIT,
        "maximum_net_force_hartree_per_bohr": FORCE_LIMIT,
    }


def test_exact_formula_unit_inventory_and_periodic_cell_scaling(report) -> None:
    _check_structure(report)


def test_ewald_and_short_range_image_cardinalities(report) -> None:
    _check_interaction_counts(report)


def test_energy_component_balance_forces_and_stationary_dipoles(report) -> None:
    _check_energies_and_residuals(report)


def test_untraced_runtime_samples_and_traced_allocation_measurements(report) -> None:
    _check_measurements(report)


def test_scaling_ratios_recomputed_from_raw_samples(report) -> None:
    _check_size_ratios(report)


def test_canonical_structured_stdout(execution) -> None:
    report, raw = execution
    assert raw.decode("utf-8") == json.dumps(
        report, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"


def test_independently_constructed_polarizable_baseline_and_translation(report) -> None:
    parameters = load_flibe_registered_pair_parameters(SOURCE)
    ewald_parameters = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25,
        real_image_shell=REAL_SHELL,
        reciprocal_image_shell=RECIPROCAL_SHELL,
        coordinate_unit_to_bohr=1.0,
        provenance=ParameterProvenance.BENCHMARK,
        source_id="FLIBE-SCALING-INDEPENDENT-EWALD",
    )
    model = FLiBePeriodicPolarizableModel(
        model_id="FLIBE-SCALING-INDEPENDENT",
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FLIBE-SCALING-INDEPENDENT-FIXED",
            ewald_model=FLiBePeriodicEwaldModel(
                "FLIBE-SCALING-INDEPENDENT-EWALD", ewald_parameters
            ),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="FLIBE-SCALING-INDEPENDENT-SHORT",
                parameters=parameters,
                coordinate_unit_to_bohr=1.0,
                image_shell=SHORT_RANGE_SHELL,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="FLIBE-SCALING-INDEPENDENT-POLARIZATION",
            parameters=parameters,
            ewald_parameters=ewald_parameters,
            damping_image_shell=1,
            stationarity_absolute_tolerance=STATIONARITY_LIMIT,
        ),
    )
    cell = ((EDGE_BOHR, 0.0, 0.0), (0.0, EDGE_BOHR, 0.0), (0.0, 0.0, EDGE_BOHR))

    def evaluate(positions):
        return model.evaluate(FLiBeConfiguration(AtomicConfiguration(
            species=SPECIES,
            positions=positions,
            cell=cell,
            periodic=(True, True, True),
        )))

    result = evaluate(POSITIONS)
    baseline = _measurements(report)[0]
    assert result.source_doi == SOURCE_DOI
    assert result.source_file_sha256 == report["source"]["file_sha256"]
    assert result.energy.total_energy == pytest.approx(
        baseline["total_energy_hartree"], rel=1.0e-12, abs=1.0e-12
    )
    assert fsum(value for _, value in result.energy_components_hartree) == pytest.approx(
        baseline["energy_component_sum_hartree"], rel=1.0e-12, abs=1.0e-12
    )
    maximum_net_force = max(
        abs(fsum(vector[axis] for vector in result.forces.forces))
        for axis in range(3)
    )
    assert maximum_net_force == pytest.approx(
        baseline["maximum_net_force_hartree_per_bohr"], abs=1.0e-12
    )
    shift = (0.25, 0.5, 0.75)
    translated = evaluate(tuple(
        tuple(position[axis] + shift[axis] for axis in range(3))
        for position in POSITIONS
    ))
    assert translated.energy.total_energy == pytest.approx(
        result.energy.total_energy, rel=1.0e-12, abs=1.0e-11
    )
    for original_force, translated_force in zip(
        result.forces.forces, translated.forces.forces, strict=True
    ):
        assert translated_force == pytest.approx(original_force, abs=1.0e-10)


def test_report_corruption_is_detected_by_independent_recomputation(report) -> None:
    changed = copy.deepcopy(report)
    changed["measurements"][2]["reciprocal_vectors_evaluated"] += 1
    with pytest.raises(AssertionError):
        _check_interaction_counts(changed)

    changed = copy.deepcopy(report)
    changed["measurements"][1]["energy_per_formula_unit_hartree"] *= 1.1
    with pytest.raises(AssertionError):
        _check_energies_and_residuals(changed)

    changed = copy.deepcopy(report)
    changed["measurements"][0]["median_wall_time_seconds"] *= 1.1
    with pytest.raises(AssertionError):
        _check_measurements(changed)

    changed = copy.deepcopy(report)
    changed["observed_size_ratios"][1]["peak_python_allocation_ratio"] *= 1.1
    with pytest.raises(AssertionError):
        _check_size_ratios(changed)

    changed = copy.deepcopy(report)
    changed["measurements"][0]["source_file_sha256"] = "0" * 64
    with pytest.raises(AssertionError):
        _check_source(changed)

    changed = copy.deepcopy(report)
    changed["measurements"][2]["formula_unit_count"] += 1
    with pytest.raises(AssertionError):
        _check_structure(changed)
