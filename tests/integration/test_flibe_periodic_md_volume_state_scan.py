"""Independent qualification of the FLiBe periodic MD volume/state scan.

Recalculate density from atomic masses and cell volume, pressure from
per-frame tensor components, and each source-state screening count from
registered primary-source data. Record and qualify pressure sign brackets
without equating transient fixed-cell observations to equilibrium states.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from math import fsum, isclose, isfinite
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_md_volume_state_scan.py"
PAIR_SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
VIDRIO_SOURCE = ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
BARAL_SOURCE = ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-volume-state-scan.v1"
PAIR_DOI = "10.1016/j.molliq.2019.112165"
EDGES_BOHR = (8.0, 8.5, 9.0, 10.0, 12.0, 18.0)
BOHR_TO_M = 5.29177210903e-11
U_TO_KG = 1.66053906660e-27
MASSES_U = {"Li": 6.94, "Be": 9.0121831, "F": 18.998403163}
INVENTORY = {"Li": 2, "Be": 1, "F": 4}
SOURCE_ROW_COUNTS = (61, 9)
SOURCE_DOIS = (
    "10.1021/acs.jced.2c00212",
    "10.1021/acsomega.1c02528",
)
REFERENCE_PRESSURE_PA = 102000.0
TEMPERATURE_TOLERANCE_K = 5.0
PRESSURE_TOLERANCE_PA = 1000.0
STATIONARITY_LIMIT = 1.0e-10
DT_CODE = 0.001

CHECK_NAMES = {
    "registered_pair_provenance",
    "declared_monotone_cell_grid",
    "exact_stoichiometry_and_charge",
    "constant_cell_mass",
    "density_volume_identity",
    "density_decreases_with_volume",
    "temperature_initialization",
    "pressure_tensor_decomposition",
    "observed_pressure_role",
    "dipole_stationarity",
    "finite_numeric_observables",
    "source_fingerprints",
    "source_row_accounting",
    "residuals_require_complete_state",
    "source_density_range_spanned",
}


def _data(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _number(value: object, *, nonnegative: bool = False) -> float:
    assert type(value) in (int, float)
    result = float(value)
    assert isfinite(result)
    if nonnegative:
        assert result >= 0.0
    return result


def _near(
    actual: object,
    expected: float,
    *,
    atol: float = 1.0e-8,
) -> None:
    assert isclose(
        _number(actual),
        expected,
        rel_tol=1.0e-12,
        abs_tol=atol,
    )


def _run_cli() -> tuple[dict, bytes]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        value
        for value in (
            str(ROOT / "src"),
            env.get("PYTHONPATH", ""),
        )
        if value
    )

    completed = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        check=False,
        timeout=420,
    )

    assert completed.returncode == 0, (
        completed.stderr.decode("utf-8", errors="replace")
        + completed.stdout.decode(
            "utf-8",
            errors="replace",
        )[-4000:]
    )

    assert completed.stderr == b""

    result = json.loads(completed.stdout)
    assert isinstance(result, dict)

    return result, completed.stdout


@pytest.fixture(scope="module")
def executions() -> tuple[
    tuple[dict, bytes],
    tuple[dict, bytes],
]:
    assert BENCHMARK.is_file()
    return _run_cli(), _run_cli()


@pytest.fixture(scope="module")
def report(executions) -> dict:
    return executions[0][0]


def _reference_table():
    vidrio = _data(VIDRIO_SOURCE)
    baral = _data(BARAL_SOURCE)

    vidrio_values = tuple(
        float(row[2])
        for series in vidrio["runs"].values()
        for row in series
    )

    baral_values = tuple(
        1000.0 * float(row[3])
        for row in baral["samples"]
    )

    vidrio_temps = tuple(
        float(row[0]) + 273.15
        for series in vidrio["runs"].values()
        for row in series
    )

    baral_temps = tuple(
        float(row[0])
        for row in baral["samples"]
    )

    return (
        (
            vidrio,
            VIDRIO_SOURCE,
            vidrio_values,
            vidrio_temps,
            vidrio["domain"]["measured_composition"][
                "bef2_mol_percent"
            ] / 100.0,
            vidrio["domain"]["pressure_kpa"] * 1000.0,
        ),
        (
            baral,
            BARAL_SOURCE,
            baral_values,
            baral_temps,
            1.0 / 3.0,
            None,
        ),
    )


def _audit_geometry(document: dict) -> None:
    rows = document["results"]

    assert isinstance(rows, list)
    assert len(rows) == len(EDGES_BOHR)

    assert tuple(
        row["cell_edge_bohr"]
        for row in rows
    ) == EDGES_BOHR

    total_mass = fsum(
        INVENTORY[name] * MASSES_U[name]
        for name in INVENTORY
    ) * U_TO_KG

    for row, edge in zip(
        rows,
        EDGES_BOHR,
        strict=True,
    ):
        assert row["atom_count"] == 7
        assert row["formula_unit_count"] == 1
        assert row["formal_charge_total_e"] == 0.0

        _near(
            row["cell_volume_bohr3"],
            edge**3,
        )

        _near(
            row["total_cell_mass_kg"],
            total_mass,
            atol=1.0e-40,
        )

        _near(
            row["mean_density_kg_m3"],
            total_mass / (edge * BOHR_TO_M)**3,
        )

        assert row["model_source_sha256"] == _sha256(
            PAIR_SOURCE
        )

    assert all(
        left["mean_density_kg_m3"]
        > right["mean_density_kg_m3"]
        for left, right in zip(
            rows,
            rows[1:],
            strict=False,
        )
    )

    assert rows[0]["mean_density_kg_m3"] > 2100.0
    assert rows[-1]["mean_density_kg_m3"] < 200.0


def _audit_samples(document: dict) -> None:
    for row in document["results"]:
        samples = row["samples"]

        assert isinstance(samples, list)
        assert len(samples) == 2

        _near(
            row["mean_temperature_k"],
            fsum(
                _number(
                    sample["kinetic_temperature_k"],
                    nonnegative=True,
                )
                for sample in samples
            ) / len(samples),
        )

        _near(
            row["mean_signed_pressure_pa"],
            fsum(
                _number(sample["signed_total_pressure_pa"])
                for sample in samples
            ) / len(samples),
        )

        _near(
            samples[0]["kinetic_temperature_k"],
            850.0,
            atol=1.0e-8,
        )

        for index, sample in enumerate(samples):
            assert sample["state_index"] == index

            _near(
                sample["md_time_code"],
                DT_CODE * index,
                atol=1.0e-14,
            )

            _near(
                sample["density_kg_m3"],
                row["mean_density_kg_m3"],
            )

            _near(
                sample["signed_total_pressure_pa"],
                _number(sample["kinetic_pressure_pa"])
                + _number(
                    sample["configurational_pressure_pa"]
                ),
                atol=1.0e-3,
            )

            assert _number(
                sample["dipole_stationarity_residual_atomic"],
                nonnegative=True,
            ) <= STATIONARITY_LIMIT

            _number(sample["potential_energy_hartree"])

        assert _number(
            row["maximum_absolute_energy_change_hartree"],
            nonnegative=True,
        ) >= 0.0

        pressure = _number(
            row["mean_signed_pressure_pa"]
        )

        observed = row["observed_pressure_coordinate_pa"]

        if pressure < 0.0:
            assert observed is None
        else:
            _near(
                observed,
                pressure,
                atol=1.0e-3,
            )


def _audit_sources(document: dict) -> None:
    sources = document["sources"]

    assert isinstance(sources, list)
    assert len(sources) == 2

    reference = _reference_table()

    for index, (
        original,
        path,
        densities,
        _,
        _,
        _,
    ) in enumerate(reference):
        entry = sources[index]

        assert entry["dataset_id"] == original["dataset_id"]

        assert (
            entry["doi"]
            == original["source"]["doi"]
            == SOURCE_DOIS[index]
        )

        assert entry["file_sha256"] == _sha256(path)

        assert (
            entry["row_count"]
            == len(densities)
            == SOURCE_ROW_COUNTS[index]
        )

    _near(
        document["experimental_pressure_reference_pa"],
        REFERENCE_PRESSURE_PA,
    )

    for row in document["results"]:
        screens = row["source_screening"]

        assert isinstance(screens, list)
        assert len(screens) == 2

        for index, (
            original,
            path,
            densities,
            temperatures,
            be_fraction,
            pressure,
        ) in enumerate(reference):
            screen = screens[index]

            assert (
                screen["dataset_id"]
                == original["dataset_id"]
            )

            assert screen["source_sha256"] == _sha256(
                path
            )

            assert (
                screen["source_row_count"]
                == SOURCE_ROW_COUNTS[index]
            )

            assert screen[
                "missing_source_pressure_count"
            ] == (
                0
                if pressure is not None
                else len(densities)
            )

            assert screen[
                "missing_source_phase_count"
            ] == len(densities)

            assert screen["fully_matched_rows"] == 0
            assert screen["qualified_density_metrics"] is None

            assert screen[
                "source_density_range_kg_m3"
            ] == [
                min(densities),
                max(densities),
            ]

            assert screen[
                "model_density_within_source_range"
            ] is (
                min(densities)
                <= row["mean_density_kg_m3"]
                <= max(densities)
            )

            counts = screen["matched_count_by_axis"]

            assert set(counts) == {
                "composition",
                "temperature",
                "pressure",
                "physical_state",
                "normalization",
            }

            assert counts["composition"] == (
                len(densities)
                if be_fraction == (1.0 / 3.0)
                else 0
            )

            assert counts["temperature"] == sum(
                abs(
                    row["mean_temperature_k"]
                    - temperature
                ) <= TEMPERATURE_TOLERANCE_K
                for temperature in temperatures
            )

            assert counts["pressure"] == (
                len(densities)
                if (
                    pressure is not None
                    and row[
                        "observed_pressure_coordinate_pa"
                    ] is not None
                    and abs(
                        row[
                            "observed_pressure_coordinate_pa"
                        ] - pressure
                    ) <= PRESSURE_TOLERANCE_PA
                )
                else 0
            )

            assert counts["physical_state"] == 0

            assert counts["normalization"] == len(
                densities
            )


def _audit_pressure_brackets(document: dict) -> None:
    rows = document["results"]

    target = _number(
        document["experimental_pressure_reference_pa"]
    )

    expected = []

    for left, right in zip(
        rows,
        rows[1:],
    ):
        p_left = _number(
            left["mean_signed_pressure_pa"]
        ) - target

        p_right = _number(
            right["mean_signed_pressure_pa"]
        ) - target

        if p_left * p_right <= 0.0:
            expected.append(
                (
                    left["cell_edge_bohr"],
                    right["cell_edge_bohr"],
                    p_left,
                    p_right,
                )
            )

    registered = document["pressure_difference_brackets"]

    assert isinstance(registered, list)
    assert len(registered) == len(expected)

    for row, (
        first,
        second,
        p_first,
        p_second,
    ) in zip(
        registered,
        expected,
        strict=True,
    ):
        assert row["cell_edge_interval_bohr"] == [
            first,
            second,
        ]

        assert row[
            "pressure_difference_at_edges_pa"
        ] == pytest.approx(
            [p_first, p_second],
            rel=1.0e-12,
            abs=1.0e-3,
        )

    assert any(
        first == 9.0 and second == 10.0
        for first, second, *_ in expected
    )


def test_cli_identity_and_all_declared_checks(report):
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert set(report["checks"]) == CHECK_NAMES

    assert all(
        value is True
        for value in report["checks"].values()
    )


def test_fixed_nve_sampling_and_six_declared_cells(report):
    method = report["method"]

    assert method["ensemble"] == "NVE_FIXED_CELL"

    assert (
        method["geometry"]
        == "SHARED_FRACTIONAL_SEVEN_ATOM_FIXTURE"
    )

    assert method["cell_edges_bohr"] == list(
        EDGES_BOHR
    )

    assert method["temperature_initialization_k"] == 850.0
    assert method["velocity_frame"] == "CENTER_OF_MASS"
    assert method["time_step_code"] == DT_CODE
    assert method["integration_steps"] == 1
    assert method["stress_strain_step"] == 2.0e-5

    assert (
        method["pressure_operator"]
        == "KINETIC_PLUS_ENERGY_STRAIN_CONFIGURATIONAL"
    )

    assert method["phase_id"] == "UNCLASSIFIED_MD_PHASE"

    assert (
        method["temperature_match_tolerance_k"]
        == TEMPERATURE_TOLERANCE_K
    )

    assert (
        method["pressure_match_tolerance_pa"]
        == PRESSURE_TOLERANCE_PA
    )

    assert (
        method["source_residual_gate"]
        == "COMPLETE_FIVE_AXIS_STATE_MATCH"
    )


def test_registered_pair_source_and_exact_stoichiometry(report):
    pair = _data(PAIR_SOURCE)

    assert pair["source"]["doi"] == PAIR_DOI
    assert pair["provenance"] == "PRIMARY_SOURCE"
    assert len(pair["pair_coefficients"]) == 6

    assert INVENTORY == {
        "Li": 2,
        "Be": 1,
        "F": 4,
    }

    assert 2 * 1 + 1 * 2 - 4 == 0

    _audit_geometry(report)


def test_independent_mass_volume_density_at_every_cell(report):
    _audit_geometry(report)


def test_all_frame_temperatures_pressures_energy_and_stationarity(
    report,
):
    _audit_samples(report)


def test_primary_source_fingerprints_and_declared_ranges(
    report,
):
    _audit_sources(report)


def test_independently_recomputed_coordinate_gates_for_420_source_screens(
    report,
):
    _audit_sources(report)

    assert sum(
        screen["source_row_count"]
        for row in report["results"]
        for screen in row["source_screening"]
    ) == 6 * 70


def test_pressure_sign_brackets_are_derived_from_recorded_signed_pressure(
    report,
):
    _audit_pressure_brackets(report)


def test_no_unmatched_source_generates_density_error_metric(
    report,
):
    assert all(
        screen["fully_matched_rows"] == 0
        and screen["qualified_density_metrics"] is None
        for row in report["results"]
        for screen in row["source_screening"]
    )


def test_deterministic_full_benchmark_replay_and_canonical_json(
    executions,
):
    (first, stdout1), (second, stdout2) = executions

    assert second == first
    assert stdout2 == stdout1

    assert stdout1.decode("utf-8") == json.dumps(
        first,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"


def test_mutated_density_is_detected(report):
    altered = copy.deepcopy(report)

    altered["results"][2]["mean_density_kg_m3"] *= 1.02

    with pytest.raises(AssertionError):
        _audit_geometry(altered)


def test_mutated_pressure_component_is_detected(report):
    altered = copy.deepcopy(report)

    altered["results"][0]["samples"][0][
        "kinetic_pressure_pa"
    ] += 1.0e7

    with pytest.raises(AssertionError):
        _audit_samples(altered)


def test_mutated_source_coordinate_count_is_detected(
    report,
):
    altered = copy.deepcopy(report)

    altered["results"][0]["source_screening"][1][
        "matched_count_by_axis"
    ]["temperature"] += 1

    with pytest.raises(AssertionError):
        _audit_sources(altered)


def test_mutated_pressure_bracket_is_detected(report):
    altered = copy.deepcopy(report)

    altered["pressure_difference_brackets"][0][
        "pressure_difference_at_edges_pa"
    ][0] += 1.0e7

    with pytest.raises(AssertionError):
        _audit_pressure_brackets(altered)


def test_mutated_source_hash_is_detected(report):
    altered = copy.deepcopy(report)

    altered["sources"][0]["file_sha256"] = "0" * 64

    with pytest.raises(AssertionError):
        _audit_sources(altered)
