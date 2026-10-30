"""Independent qualification of the published-coefficient FLiBe energy benchmark."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from decimal import Decimal, localcontext
from math import factorial, fsum, isfinite, sqrt
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/reference_published_pair_energy.py"
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.published-pair-energy-force.v1"
DATASET_ID = "tr-eif.flibe.smith-2020.pim-pair-coefficients.v1"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
CROSSCHECK_DOI = "10.1016/j.crci.2007.03.002"
MODEL_ID = "FLIBE-SMITH-2020-FINITE-CLUSTER-PAIR"
ENERGY_TOL = 1.0e-9
FORCE_TOL = 3.0e-8

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0),
    (3.0, 0.3, 0.0),
    (1.0, 2.3, 0.2),
    (0.6, 0.3, 1.6),
    (2.9, 1.0, 2.2),
    (1.1, 3.0, 2.1),
    (3.2, 2.8, 0.8),
)
CHARGES = {"Li": 1, "Be": 2, "F": -1}

# Independent transcription of the registered source table, in canonical order.
# The six numeric columns are A, alpha, C6, C8, b6, b8 in atomic units.
PAIR_PARAMETERS = (
    ("Li", "Li", 195.91, 4.252, 0.0, 0.0, 1.0, 1.0),
    ("Li", "Be", 0.0, 1.0, 0.0, 0.0, 1.0, 1.0),
    ("Li", "F", 20.42, 2.052, 0.0, 0.0, 1.0, 1.0),
    ("Be", "Be", 106.16, 3.944, 0.0, 0.0, 1.0, 1.0),
    ("Be", "F", 41.72, 2.254, 0.0, 0.0, 1.0, 1.0),
    ("F", "F", 181.84, 2.267, 15.0, 150.0, 1.9, 1.9),
)

CHECK_NAMES = {
    "registered_source_identity",
    "source_file_fingerprint",
    "source_pair_table",
    "source_pair_provenance",
    "pair_functional_identity",
    "formal_charge_balance",
    "exact_formula_composition",
    "cluster_pair_count",
    "source_energy_reference",
    "source_atomic_energy_reference",
    "source_force_reference",
    "lif_energy_reference",
    "lif_force_reference",
    "atomic_partition",
    "net_force_balance",
    "exact_replay",
    "e3_energy_invariance",
    "e3_force_covariance",
    "permutation_energy_invariance",
    "permutation_force_covariance",
}


def _execute() -> tuple[dict[str, object], bytes]:
    """Run the committed benchmark with an explicit package import path."""
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
        timeout=90,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    assert completed.stderr == b""
    result = json.loads(completed.stdout)
    assert isinstance(result, dict)
    return result, completed.stdout


@pytest.fixture(scope="module")
def report() -> dict[str, object]:
    return _execute()[0]


def _reference_energy_forces(species, positions):
    """Evaluate the source-table pair law and radial derivative in Decimal."""
    table = {
        frozenset((a, b)): (amplitude, decay, c6, c8, beta6, beta8)
        for a, b, amplitude, decay, c6, c8, beta6, beta8 in PAIR_PARAMETERS
    }
    with localcontext() as context:
        context.prec = 65
        d = lambda value: Decimal(str(value))
        coordinates = tuple(tuple(d(value) for value in xyz) for xyz in positions)
        atom_energies = [Decimal(0) for _ in species]
        forces = [[Decimal(0) for _ in range(3)] for _ in species]
        for i in range(len(species)):
            for j in range(i + 1, len(species)):
                vector = tuple(
                    coordinates[i][axis] - coordinates[j][axis]
                    for axis in range(3)
                )
                radius = sum(component * component for component in vector).sqrt()
                assert radius > 0
                amplitude, decay, c6, c8, beta6, beta8 = table[
                    frozenset((species[i], species[j]))
                ]
                charges = Decimal(CHARGES[species[i]] * CHARGES[species[j]])
                repulsion = d(amplitude) * (-d(decay) * radius).exp()
                pair_energy = charges / radius + repulsion
                radial_gradient = -charges / radius**2 - d(decay) * repulsion
                for order, coefficient, beta in (
                    (6, c6, beta6), (8, c8, beta8)
                ):
                    if coefficient == 0.0:
                        continue
                    z = d(beta) * radius
                    tail = (-z).exp()
                    polynomial = sum(
                        (z**k / Decimal(factorial(k)) for k in range(order + 1)),
                        Decimal(0),
                    )
                    damping = Decimal(1) - tail * polynomial
                    derivative_z = tail * z**order / Decimal(factorial(order))
                    pair_energy -= d(coefficient) * damping / radius**order
                    radial_gradient -= d(coefficient) * (
                        d(beta) * derivative_z / radius**order
                        - Decimal(order) * damping / radius**(order + 1)
                    )
                atom_energies[i] += pair_energy / 2
                atom_energies[j] += pair_energy / 2
                for axis in range(3):
                    component = -radial_gradient * vector[axis] / radius
                    forces[i][axis] += component
                    forces[j][axis] -= component
        return (
            tuple(float(value) for value in atom_energies),
            tuple(tuple(float(value) for value in row) for row in forces),
        )


def _benchmark_module():
    """Load the exact benchmark source for failure-path qualification."""
    spec = importlib.util.spec_from_file_location("flibe_published_pair_benchmark", BENCHMARK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_committed_benchmark_runs_and_emits_declared_catalogue(report):
    assert BENCHMARK.is_file()
    assert SOURCE.is_file()
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert set(report["checks"]) == CHECK_NAMES
    assert all(value is True for value in report["checks"].values())


def test_source_doi_fingerprint_and_parameter_provenance(report):
    source = report["source"]
    assert source["dataset_id"] == DATASET_ID
    assert source["doi"] == SOURCE_DOI
    assert source["crosscheck_doi"] == CROSSCHECK_DOI
    assert source["table_location"] == "Table 1, Parameter values for the LiF-BeF2 potentials"
    assert source["file_sha256"] == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert source["provenance"] == "PRIMARY_SOURCE"
    assert source["registered_fluoride_polarizability_bohr3"] == 7.09
    assert source["registered_separate_terms"] == [
        "induced-dipole polarization", "periodic long-range electrostatics"
    ]


def test_fixture_species_coordinates_and_boundary(report):
    fixture = report["fixture"]
    assert fixture["atom_count"] == 7
    assert fixture["species"] == list(SPECIES)
    assert fixture["positions_bohr"] == [list(point) for point in POSITIONS]
    assert fixture["pair_count"] == 21
    model = report["model"]
    assert model == {
        "model_id": MODEL_ID,
        "functional_id": "flibe.finite_cluster.coulomb_born_mayer_tt.v1",
        "boundary": "isolated_nonperiodic_finite_cluster",
        "coordinate_unit_to_bohr": 1.0,
        "energy_unit": "hartree",
        "force_unit": "hartree/bohr",
    }


def test_numeric_criteria_are_declared(report):
    assert report["numeric_criteria"] == {
        "energy_absolute_tolerance_hartree": ENERGY_TOL,
        "force_absolute_tolerance_hartree_per_bohr": FORCE_TOL,
    }


def test_seven_atom_energy_matches_decimal_source_equation(report):
    atomic, _ = _reference_energy_forces(SPECIES, POSITIONS)
    total = fsum(atomic)
    fixture = report["fixture"]
    assert total == pytest.approx(2.7944865610939633, rel=0.0, abs=ENERGY_TOL)
    assert fixture["analytical_energy_hartree"] == pytest.approx(total, rel=0.0, abs=ENERGY_TOL)
    assert fixture["model_energy_hartree"] == pytest.approx(total, rel=0.0, abs=ENERGY_TOL)
    assert fixture["energy_residual_hartree"] == pytest.approx(
        fixture["model_energy_hartree"] - total, rel=0.0, abs=ENERGY_TOL
    )


def test_seven_atom_forces_match_independent_decimal_gradients(report):
    _, expected = _reference_energy_forces(SPECIES, POSITIONS)
    actual = report["fixture"]["model_forces_hartree_per_bohr"]
    assert len(actual) == len(expected) == 7
    for observed, reference in zip(actual, expected, strict=True):
        assert len(observed) == 3
        assert all(isinstance(value, (float, int)) and isfinite(value) for value in observed)
        assert observed == pytest.approx(reference, rel=0.0, abs=FORCE_TOL)


def test_force_residual_metrics_are_independently_reduced(report):
    _, expected = _reference_energy_forces(SPECIES, POSITIONS)
    observed = report["fixture"]["model_forces_hartree_per_bohr"]
    residuals = tuple(
        observed[i][axis] - expected[i][axis]
        for i in range(len(SPECIES)) for axis in range(3)
    )
    fixture = report["fixture"]
    assert fixture["force_max_abs_residual_hartree_per_bohr"] == pytest.approx(
        max(abs(value) for value in residuals), rel=0.0, abs=FORCE_TOL
    )
    assert fixture["force_rmse_hartree_per_bohr"] == pytest.approx(
        sqrt(fsum(value * value for value in residuals) / len(residuals)),
        rel=0.0, abs=FORCE_TOL,
    )
    assert fixture["force_max_abs_residual_hartree_per_bohr"] <= FORCE_TOL
    assert fixture["force_rmse_hartree_per_bohr"] <= FORCE_TOL


def test_lif_energy_and_force_are_independent_two_atom_anchors(report):
    species = ("Li", "F")
    positions = ((0.0, 0.0, 0.0), (2.0, 0.0, 0.0))
    energies, forces = _reference_energy_forces(species, positions)
    actual = report["two_atom_lif"]
    assert actual["separation_bohr"] == 2.0
    assert actual["model_energy_hartree"] == pytest.approx(
        -0.16293692071674035, rel=0.0, abs=ENERGY_TOL
    )
    assert actual["analytical_energy_hartree"] == pytest.approx(
        fsum(energies), rel=0.0, abs=ENERGY_TOL
    )
    assert actual["model_energy_hartree"] == pytest.approx(
        fsum(energies), rel=0.0, abs=ENERGY_TOL
    )
    assert forces[0][0] == pytest.approx(-forces[1][0], rel=0.0, abs=FORCE_TOL)
    assert forces[0][1:] == (0.0, 0.0)
    assert forces[1][1:] == (0.0, 0.0)


def test_forces_obey_closed_pair_balance(report):
    forces = report["fixture"]["model_forces_hartree_per_bohr"]
    for axis in range(3):
        assert abs(fsum(force[axis] for force in forces)) <= FORCE_TOL


def test_registered_table_has_fixed_primary_coefficients():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert payload["dataset_id"] == DATASET_ID
    assert payload["provenance"] == "PRIMARY_SOURCE"
    actual = tuple(
        (row["species_a"], row["species_b"], row["born_amplitude_hartree"],
         row["born_decay_inverse_bohr"], row["c6_hartree_bohr6"],
         row["c8_hartree_bohr8"], row["b6_inverse_bohr"], row["b8_inverse_bohr"])
        for row in payload["pair_coefficients"]
    )
    assert actual == PAIR_PARAMETERS


def test_independent_source_table_change_sets_failed_check(tmp_path, monkeypatch):
    """A valid coefficient alteration changes source identity and check outcome."""
    module = _benchmark_module()
    modified = json.loads(SOURCE.read_text(encoding="utf-8"))
    modified["pair_coefficients"][2]["born_amplitude_hartree"] = 21.42
    path = tmp_path / "altered_pair_table.json"
    path.write_text(json.dumps(modified, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(module, "DATA_PATH", path)
    report = module.run_benchmark()
    assert report["status"] == "FAIL"
    assert report["checks"]["source_pair_table"] is False
    assert report["source"]["file_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert report["source"]["file_sha256"] != hashlib.sha256(SOURCE.read_bytes()).hexdigest()



def test_polarizability_metadata_does_not_change_pair_energy(tmp_path, monkeypatch):
    """Preserve the distinction between registered PIM terms and pair energy."""
    baseline = _execute()[0]
    module = _benchmark_module()
    modified = json.loads(SOURCE.read_text(encoding="utf-8"))
    modified["additional_source_model_terms"]["fluoride_polarizability_bohr3"] = 8.0
    path = tmp_path / "changed_polarization_metadata.json"
    path.write_text(json.dumps(modified, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(module, "DATA_PATH", path)
    report = module.run_benchmark()
    assert report["status"] == "PASS"
    assert report["source"]["registered_fluoride_polarizability_bohr3"] == 8.0
    assert report["source"]["file_sha256"] != baseline["source"]["file_sha256"]
    assert report["fixture"]["model_energy_hartree"] == baseline["fixture"]["model_energy_hartree"]
    assert report["fixture"]["model_forces_hartree_per_bohr"] == baseline["fixture"]["model_forces_hartree_per_bohr"]


def test_benchmark_output_is_byte_deterministic():
    first, first_raw = _execute()
    second, second_raw = _execute()
    assert first == second
    assert first_raw == second_raw
    assert first_raw.decode("utf-8") == json.dumps(
        first, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"
