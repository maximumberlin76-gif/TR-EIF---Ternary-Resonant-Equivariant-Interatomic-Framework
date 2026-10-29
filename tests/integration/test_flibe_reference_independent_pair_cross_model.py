"""Independent numerical contracts for the FLiBe two-potential benchmark."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from decimal import Decimal, localcontext
from math import factorial, fsum, pi, sqrt
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.resonance import ResonanceState


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/reference_independent_pair_cross_model.py"
BENCHMARK_ID = "tr-eif.flibe.independent-pair-cross-model.v1"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0), (1.1, 0.7, 0.8), (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
CHARGES = {"Li": 1, "Be": 2, "F": -1}
SCALARS = tuple(0.5 + 0.25 * index for index in range(7))
TERNARY = (-1, 0, 1, 0, -1, 1, 0)
FACTORS = {-1: 0.5, 0: 1.25, 1: 1.5}
PAIR_KEYS = (("Li", "Li"), ("Li", "Be"), ("Li", "F"),
             ("Be", "Be"), ("Be", "F"), ("F", "F"))
HARTREE_FACTOR = 0.5
ENERGY_TOL = 1.0e-9
FORCE_TOL = 3.0e-6
EXPECTED_CHECKS = {
    "matched_atomic_configuration", "exact_formula_composition",
    "formal_charge_balance", "ternary_execution_retained",
    "independent_pair_cardinality", "pair_energy_partition",
    "tr_eip_energy_partition", "independent_pair_energy_anchor",
    "independent_tr_eip_energy_anchor", "signed_energy_difference",
    "exact_replay", "pair_energy_e3", "tr_eip_energy_e3",
    "pair_force_e3", "tr_eip_force_e3", "pair_net_force",
    "tr_eip_net_force",
}


def _execute() -> tuple[dict[str, object], bytes]:
    """Execute the committed benchmark with a reproducible import path."""
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
    payload = json.loads(completed.stdout)
    assert isinstance(payload, dict)
    return payload, completed.stdout


@pytest.fixture(scope="module")
def report() -> dict[str, object]:
    return _execute()[0]


@pytest.fixture(scope="module")
def benchmark_module():
    """Import the exact benchmark file for input-contract mutation tests."""
    spec = importlib.util.spec_from_file_location("flibe_pair_cross_model_test_module", BENCHMARK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _independent_coefficients():
    """Construct fixture coefficients independently of the potential implementation."""
    return {
        frozenset(pair): {
            "amplitude": 0.12 + 0.025 * index,
            "decay": 0.60 + 0.07 * index,
            "c6": 0.018 + 0.004 * index,
            "c8": 0.005 + 0.001 * index,
            "b6": 0.90 + 0.10 * index,
            "b8": 1.00 + 0.10 * index,
        }
        for index, pair in enumerate(PAIR_KEYS)
    }


def _independent_pair_energy_forces():
    """Evaluate all unordered Coulomb/Born/dispersion pairs in Decimal arithmetic."""
    coefficients = _independent_coefficients()
    with localcontext() as context:
        context.prec = 55
        d = lambda number: Decimal(str(number))
        positions = tuple(tuple(d(value) for value in row) for row in POSITIONS)
        atomic = [Decimal(0) for _ in SPECIES]
        forces = [[Decimal(0) for _ in range(3)] for _ in SPECIES]
        for i in range(len(SPECIES)):
            for j in range(i + 1, len(SPECIES)):
                difference = tuple(positions[i][axis] - positions[j][axis] for axis in range(3))
                radius = sum(component * component for component in difference).sqrt()
                pair = coefficients[frozenset((SPECIES[i], SPECIES[j]))]
                charge = Decimal(CHARGES[SPECIES[i]] * CHARGES[SPECIES[j]])
                amplitude, decay = d(pair["amplitude"]), d(pair["decay"])
                born = amplitude * (-decay * radius).exp()
                value = charge / radius + born
                derivative = -charge / radius**2 - decay * born
                for order in (6, 8):
                    coefficient = d(pair[f"c{order}"])
                    beta = d(pair[f"b{order}"])
                    z = beta * radius
                    exp_factor = (-z).exp()
                    polynomial = sum(
                        (z**k / Decimal(factorial(k)) for k in range(order + 1)),
                        Decimal(0),
                    )
                    damping = Decimal(1) - exp_factor * polynomial
                    damping_derivative = exp_factor * z**order / Decimal(factorial(order))
                    value -= coefficient * damping / radius**order
                    derivative -= coefficient * (
                        beta * damping_derivative / radius**order
                        - Decimal(order) * damping / radius**(order + 1)
                    )
                atomic[i] += value / 2
                atomic[j] += value / 2
                for axis in range(3):
                    force = -derivative * difference[axis] / radius
                    forces[i][axis] += force
                    forces[j][axis] -= force
        return (
            tuple(float(number) for number in atomic),
            tuple(tuple(float(value) for value in row) for row in forces),
        )


def _independent_tr_eip_energy_forces():
    """Evaluate the fixed-graph linear radial law and its analytic gradient."""
    radial_scale_squared = 1.1**2
    radius_cutoff_squared = 1.6**2
    phase_increment = 0.7 / 7.0 - 0.3 * 0.2
    coefficients = tuple(
        FACTORS[TERNARY[index]] * (0.4 * SCALARS[index] + phase_increment)
        for index in range(len(SPECIES))
    )
    atomic = [0.1 + coefficient for coefficient in coefficients]
    forces = [[0.0, 0.0, 0.0] for _ in SPECIES]
    directed_edges = 0
    for i in range(len(SPECIES)):
        for j in range(i + 1, len(SPECIES)):
            delta = tuple(POSITIONS[i][axis] - POSITIONS[j][axis] for axis in range(3))
            squared = fsum(component**2 for component in delta)
            if squared > radius_cutoff_squared:
                continue
            directed_edges += 2
            denominator = 1.0 + squared / radial_scale_squared
            atomic[i] += coefficients[j] / denominator
            atomic[j] += coefficients[i] / denominator
            factor = 2.0 * (coefficients[i] + coefficients[j]) / (
                radial_scale_squared * denominator**2
            )
            for axis in range(3):
                term = factor * delta[axis]
                forces[i][axis] += term
                forces[j][axis] -= term
    return (
        tuple(value * HARTREE_FACTOR for value in atomic),
        tuple(tuple(value * HARTREE_FACTOR for value in row) for row in forces),
        directed_edges,
    )


def _assert_forces(actual, expected, tolerance=FORCE_TOL):
    assert len(actual) == len(expected) == 7
    for observed, reference in zip(actual, expected, strict=True):
        assert observed == pytest.approx(reference, rel=0.0, abs=tolerance)


def _comparison_inputs(module):
    """Build the declared fixture inputs for independent validation of argument guards."""
    return {
        "configuration": FLiBeConfiguration(AtomicConfiguration(species=SPECIES, positions=POSITIONS)),
        "tr_eip_model": module._fixture_tr_eip_model(),
        "pair_model": module._fixture_model(),
        "features": module._fixture_features(),
        "oscillator": ResonanceState(
            phases=tuple(index * pi / 4 for index in range(7)),
            frequencies=(-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3),
        ),
        "execution": module._fixture_execution(),
        "state": FLiBeThermodynamicState(temperature=1000.0, pressure=0.0),
        "bridge": module.CrossModelUnitBridge(
            coordinate_unit_to_bohr=1.0,
            tr_eip_native_energy_to_hartree=HARTREE_FACTOR,
            provenance=ParameterProvenance.TEST_FIXTURE,
            source_id="FLIBE-CROSS-MODEL-UNIT-FIXTURE",
        ),
        "reference_state_id": "FLIBE-SEVEN-ATOM-NONPERIODIC-FIXTURE",
        "tr_eip_model_id": "TR-EIP-RESONANCE-CONDITIONED",
        "graph_cutoff": 1.6,
        "differentiation_step": 1.0e-6,
    }


def test_executable_status_and_exact_check_catalogue(report):
    assert BENCHMARK.is_file()
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert report["comparison_kind"] == "resonance_conditioned_tr_eip_vs_independent_rigid_ion_pair"
    assert report["provenance"] == "TEST_FIXTURE"
    assert set(report["checks"]) == EXPECTED_CHECKS
    assert all(value is True for value in report["checks"].values())


def test_matched_geometry_composition_and_discrete_state(report):
    comparison = report["comparison"]
    assert comparison["reference_state_id"] == "FLIBE-SEVEN-ATOM-NONPERIODIC-FIXTURE"
    assert comparison["atom_count"] == 7
    assert comparison["species"] == list(SPECIES)
    assert comparison["positions"] == [list(row) for row in POSITIONS]
    assert comparison["periodic"] == [False, False, False]
    assert comparison["composition"] == {"lif_fraction": 2 / 3, "bef2_fraction": 1 / 3}
    assert comparison["formal_charge"] == 0
    assert comparison["retained_execution"] == list(TERNARY)
    assert comparison["thermodynamic_state"] == {"temperature_k": 1000.0, "pressure_pa": 0.0}


def test_model_identity_provenance_and_units(report):
    comparison = report["comparison"]
    assert comparison["model_ids"] == {
        "tr_eip": "TR-EIP-RESONANCE-CONDITIONED",
        "pair": "PAIR-COULOMB-BORN-MAYER-DAMPED-C6-C8",
    }
    assert comparison["tr_eip_provenance"]["kind"] == "TEST_FIXTURE"
    assert comparison["units"] == {
        "energy": "hartree",
        "force": "hartree/input-coordinate-unit",
        "coordinate_unit_to_bohr": 1.0,
        "tr_eip_native_energy_to_hartree": HARTREE_FACTOR,
        "provenance": "TEST_FIXTURE",
        "source_id": "FLIBE-CROSS-MODEL-UNIT-FIXTURE",
    }
    assert report["numeric_criteria"] == {
        "energy_absolute_tolerance_hartree": ENERGY_TOL,
        "force_absolute_tolerance_hartree_per_coordinate": FORCE_TOL,
    }
    assert comparison["differentiation_step_input_unit"] == 1.0e-6


def test_graph_pairs_and_resonance_are_independently_derived(report):
    comparison = report["comparison"]
    _, _, expected_edges = _independent_tr_eip_energy_forces()
    assert comparison["graph"] == {
        "tr_eip_cutoff_input_unit": 1.6,
        "tr_eip_directed_edges": expected_edges,
        "pair_unordered_pairs": 21,
    }
    assert expected_edges == 38
    assert comparison["resonance"]["phase_order"] == pytest.approx(1 / 7, abs=1e-14)
    assert comparison["resonance"]["frequency_spread"] == pytest.approx(0.2, abs=1e-14)
    assert comparison["tr_eip_parameters"]["scalar_weights"] == [0.4, 0.7, -0.3]
    assert comparison["tr_eip_parameters"]["initial_scalar_features"] == [
        [value] for value in SCALARS
    ]
    assert comparison["tr_eip_parameters"]["initial_vector_features"] == [[]] * 7


def test_six_source_resolved_pair_parameter_channels(report):
    records = report["comparison"]["pair_coefficients"]
    assert len(records) == len(PAIR_KEYS) == 6
    for index, (record, species) in enumerate(zip(records, PAIR_KEYS, strict=True)):
        assert record["species"] == list(species)
        assert record["born_amplitude_hartree"] == pytest.approx(0.12 + 0.025 * index)
        assert record["born_decay_inverse_bohr"] == pytest.approx(0.60 + 0.07 * index)
        assert record["c6_hartree_bohr6"] == pytest.approx(0.018 + 0.004 * index)
        assert record["c8_hartree_bohr8"] == pytest.approx(0.005 + 0.001 * index)
        assert record["b6_inverse_bohr"] == pytest.approx(0.90 + 0.10 * index)
        assert record["b8_inverse_bohr"] == pytest.approx(1.00 + 0.10 * index)
        assert record["provenance"] == "TEST_FIXTURE"
        assert record["source_id"] == "FLIBE-INDEPENDENT-PAIR-ANALYTIC-FIXTURE"
        assert record["source_location"] == "benchmarks/flibe/reference_independent_pair_cross_model.py"


def test_independent_decimal_pair_energy_and_forces(report):
    expected_atomic, expected_forces = _independent_pair_energy_forces()
    comparison = report["comparison"]
    pair = comparison["energies_hartree"]
    assert pair["pair_atomic"] == pytest.approx(expected_atomic, rel=0.0, abs=ENERGY_TOL)
    assert pair["pair"] == pytest.approx(fsum(expected_atomic), rel=0.0, abs=ENERGY_TOL)
    assert pair["pair"] == pytest.approx(-2.7269592863955615, rel=0.0, abs=ENERGY_TOL)
    _assert_forces(comparison["forces_hartree_per_coordinate"]["pair"], expected_forces)


def test_independent_radial_tr_eip_energy_and_forces(report):
    expected_atomic, expected_forces, _ = _independent_tr_eip_energy_forces()
    comparison = report["comparison"]
    energies = comparison["energies_hartree"]
    assert energies["tr_eip_atomic"] == pytest.approx(expected_atomic, rel=0.0, abs=ENERGY_TOL)
    assert energies["tr_eip"] == pytest.approx(fsum(expected_atomic), rel=0.0, abs=ENERGY_TOL)
    assert energies["tr_eip"] == pytest.approx(8.175782059061284, rel=0.0, abs=ENERGY_TOL)
    _assert_forces(comparison["forces_hartree_per_coordinate"]["tr_eip"], expected_forces)


def test_independent_force_difference_and_error_metrics(report):
    _, pair_forces = _independent_pair_energy_forces()
    _, tr_forces, _ = _independent_tr_eip_energy_forces()
    expected = tuple(tuple(tr_forces[i][axis] - pair_forces[i][axis] for axis in range(3))
                     for i in range(7))
    observed = report["comparison"]["forces_hartree_per_coordinate"]
    _assert_forces(observed["tr_eip_minus_pair"], expected)
    values = tuple(value for row in expected for value in row)
    assert observed["component_mae"] == pytest.approx(
        fsum(abs(value) for value in values) / 21, rel=0.0, abs=FORCE_TOL
    )
    assert observed["component_rmse"] == pytest.approx(
        sqrt(fsum(value * value for value in values) / 21), rel=0.0, abs=FORCE_TOL
    )
    assert observed["maximum_absolute_component"] == pytest.approx(
        max(abs(value) for value in values), rel=0.0, abs=FORCE_TOL
    )


def test_signed_energy_difference_and_atomic_partition(report):
    energies = report["comparison"]["energies_hartree"]
    assert energies["tr_eip_minus_pair"] == pytest.approx(10.902741345456845, abs=ENERGY_TOL)
    assert energies["tr_eip_minus_pair"] == pytest.approx(
        energies["tr_eip"] - energies["pair"], abs=ENERGY_TOL
    )
    for name in ("tr_eip", "pair"):
        assert energies[name] == pytest.approx(fsum(energies[f"{name}_atomic"]), abs=ENERGY_TOL)


def test_pairwise_force_balance_for_each_independent_model(report):
    forces = report["comparison"]["forces_hartree_per_coordinate"]
    for name in ("tr_eip", "pair"):
        assert len(forces[name]) == 7
        for axis in range(3):
            assert abs(fsum(row[axis] for row in forces[name])) <= FORCE_TOL


def test_unit_bridge_scales_only_the_tr_eip_outputs(benchmark_module):
    arguments = _comparison_inputs(benchmark_module)
    first = benchmark_module.compare_models(**arguments)
    bridge = arguments["bridge"]
    arguments["bridge"] = benchmark_module.CrossModelUnitBridge(
        coordinate_unit_to_bohr=bridge.coordinate_unit_to_bohr,
        tr_eip_native_energy_to_hartree=1.0,
        provenance=bridge.provenance,
        source_id=bridge.source_id,
    )
    second = benchmark_module.compare_models(**arguments)
    assert second["energies_hartree"]["tr_eip"] == pytest.approx(
        2.0 * first["energies_hartree"]["tr_eip"]
    )
    assert second["energies_hartree"]["pair"] == pytest.approx(
        first["energies_hartree"]["pair"]
    )
    for old, new in zip(
        first["forces_hartree_per_coordinate"]["tr_eip"],
        second["forces_hartree_per_coordinate"]["tr_eip"],
        strict=True,
    ):
        assert new == pytest.approx([2 * value for value in old], rel=0, abs=FORCE_TOL)
    assert second["forces_hartree_per_coordinate"]["pair"] == (
        first["forces_hartree_per_coordinate"]["pair"]
    )


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (
        ("coordinate_unit_to_bohr", 0.0, ValueError),
        ("coordinate_unit_to_bohr", -2.0, ValueError),
        ("coordinate_unit_to_bohr", float("nan"), ValueError),
        ("coordinate_unit_to_bohr", False, TypeError),
        ("tr_eip_native_energy_to_hartree", 0.0, ValueError),
        ("tr_eip_native_energy_to_hartree", float("inf"), ValueError),
        ("tr_eip_native_energy_to_hartree", True, TypeError),
        ("provenance", "TEST_FIXTURE", TypeError),
        ("source_id", "", ValueError),
        ("source_id", " invalid ", ValueError),
    ),
)
def test_unit_bridge_rejects_invalid_conversion_or_provenance(
    benchmark_module, field, invalid, error
):
    arguments = dict(
        coordinate_unit_to_bohr=1.0,
        tr_eip_native_energy_to_hartree=HARTREE_FACTOR,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="FLIBE-CROSS-MODEL-UNIT-FIXTURE",
    )
    arguments[field] = invalid
    with pytest.raises(error):
        benchmark_module.CrossModelUnitBridge(**arguments)


@pytest.mark.parametrize(
    ("field", "invalid", "error", "message"),
    (
        ("configuration", None, TypeError, "FLiBeConfiguration"),
        ("tr_eip_model", None, TypeError, "FLiBeTREIPModel"),
        ("pair_model", None, TypeError, "FLiBeIndependentPairModel"),
        ("bridge", None, TypeError, "CrossModelUnitBridge"),
        ("state", None, TypeError, "FLiBeThermodynamicState"),
        ("reference_state_id", " ", ValueError, "reference_state_id"),
        ("tr_eip_model_id", "", ValueError, "tr_eip_model_id"),
        ("graph_cutoff", -1.0, ValueError, "graph_cutoff"),
        ("graph_cutoff", True, TypeError, "graph_cutoff"),
        ("differentiation_step", 0.0, ValueError, "differentiation_step"),
        ("differentiation_step", float("nan"), ValueError, "differentiation_step"),
    ),
)
def test_comparison_rejects_invalid_inputs(benchmark_module, field, invalid, error, message):
    arguments = _comparison_inputs(benchmark_module)
    arguments[field] = invalid
    with pytest.raises(error, match=message):
        benchmark_module.compare_models(**arguments)


def test_comparison_rejects_mismatched_coordinate_conversion(benchmark_module):
    arguments = _comparison_inputs(benchmark_module)
    arguments["bridge"] = benchmark_module.CrossModelUnitBridge(
        coordinate_unit_to_bohr=2.0,
        tr_eip_native_energy_to_hartree=HARTREE_FACTOR,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="OTHER-LENGTH-CONVERSION",
    )
    with pytest.raises(ValueError, match="coordinate units must agree"):
        benchmark_module.compare_models(**arguments)


def test_comparison_rejects_periodic_configuration(benchmark_module):
    arguments = _comparison_inputs(benchmark_module)
    arguments["configuration"] = FLiBeConfiguration(
        AtomicConfiguration(
            species=SPECIES, positions=POSITIONS,
            cell=((12.0, 0.0, 0.0), (0.0, 12.0, 0.0), (0.0, 0.0, 12.0)),
            periodic=(True, True, True),
        )
    )
    with pytest.raises(ValueError, match="nonperiodic Cartesian boundaries"):
        benchmark_module.compare_models(**arguments)


def test_comparison_rejects_oscillator_cardinality_mismatch(benchmark_module):
    arguments = _comparison_inputs(benchmark_module)
    arguments["oscillator"] = ResonanceState(phases=(0.0,), frequencies=(0.0,))
    with pytest.raises(ValueError, match="oscillator count"):
        benchmark_module.compare_models(**arguments)


def test_benchmark_stdout_replays_byte_identically():
    first, first_raw = _execute()
    second, second_raw = _execute()
    assert first == second
    assert first_raw == second_raw
    assert first_raw.decode("utf-8") == json.dumps(first, indent=2, sort_keys=True) + "\n"
