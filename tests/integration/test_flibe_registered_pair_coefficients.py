"""Independent qualification of published FLiBe pair-coefficient registration."""

from __future__ import annotations

import hashlib
import json
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal, localcontext
from math import exp, factorial, fsum, isfinite
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.independent_pair_potential import (
    PAIR_FUNCTIONAL_ID,
    PAIR_ORDER,
    FLiBeIndependentPairModel,
)
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.registered_pair_coefficients import (
    CROSSCHECK_DOI,
    DATASET_ID,
    SOURCE_DOI,
    FLiBeChargeDipoleSourceParameter,
    FLiBeRegisteredPairParameters,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.species import FLiBeSpecies
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SOURCE_LOCATION = "Table 1, Parameter values for the LiF-BeF2 potentials"

# Independently transcribed published table in canonical Li, Be, F pair order.
# Columns: pair, A (hartree), alpha (bohr^-1), C6 (hartree*bohr^6),
# C8 (hartree*bohr^8), b6 (bohr^-1), b8 (bohr^-1).
EXPECTED_PAIRS = (
    ("Li", "Li", 195.91, 4.252, 0.0, 0.0, 1.0, 1.0),
    ("Li", "Be", 0.0, 1.0, 0.0, 0.0, 1.0, 1.0),
    ("Li", "F", 20.42, 2.052, 0.0, 0.0, 1.0, 1.0),
    ("Be", "Be", 106.16, 3.944, 0.0, 0.0, 1.0, 1.0),
    ("Be", "F", 41.72, 2.254, 0.0, 0.0, 1.0, 1.0),
    ("F", "F", 181.84, 2.267, 15.0, 150.0, 1.9, 1.9),
)
SOURCE_PAIR_ORDER = (
    ("F", "F"), ("Be", "F"), ("Li", "F"),
    ("Be", "Be"), ("Li", "Be"), ("Li", "Li"),
)
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
ENERGY_ABS_TOL = 2.0e-11
FORCE_ABS_TOL = 3.0e-6


def _load(path: Path = SOURCE) -> FLiBeRegisteredPairParameters:
    return load_flibe_registered_pair_parameters(path)


def _payload() -> dict[str, object]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _modified(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "pair_parameters_modified.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, allow_nan=True), encoding="utf-8")
    return path


def _configuration(species=SPECIES, positions=POSITIONS) -> FLiBeConfiguration:
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(v) for v in row) for row in positions),
    ))


def _analytic_pair_energy(species: tuple[str, ...], positions: tuple[tuple[float, ...], ...]) -> float:
    """Evaluate the published pair law with Decimal inputs and transcendental terms."""
    parameters = {frozenset((a, b)): (amplitude, alpha, c6, c8, b6, b8)
                  for a, b, amplitude, alpha, c6, c8, b6, b8 in EXPECTED_PAIRS}
    with localcontext() as context:
        context.prec = 55
        d = lambda value: Decimal(str(value))
        energy = Decimal(0)
        for i in range(len(species)):
            for j in range(i + 1, len(species)):
                delta = tuple(d(positions[i][axis]) - d(positions[j][axis])
                              for axis in range(3))
                r = sum(value * value for value in delta).sqrt()
                amplitude, alpha, c6, c8, b6, b8 = parameters[
                    frozenset((species[i], species[j]))
                ]
                term = Decimal(CHARGES[species[i]] * CHARGES[species[j]]) / r
                term += d(amplitude) * (-d(alpha) * r).exp()
                for power, dispersion, beta in ((6, c6, b6), (8, c8, b8)):
                    if dispersion == 0:
                        continue
                    z = d(beta) * r
                    polynomial = sum(
                        (z ** k / Decimal(factorial(k)) for k in range(power + 1)),
                        Decimal(0),
                    )
                    damping = Decimal(1) - (-z).exp() * polynomial
                    term -= d(dispersion) * damping / (r ** power)
                energy += term
        return float(energy)


def test_registered_dataset_identity_and_sha256() -> None:
    assert SOURCE.is_file()
    registered = _load()
    assert registered.dataset_id == DATASET_ID
    assert registered.source_doi == SOURCE_DOI == "10.1016/j.molliq.2019.112165"
    assert registered.crosscheck_doi == CROSSCHECK_DOI == "10.1016/j.crci.2007.03.002"
    assert registered.source_location == SOURCE_LOCATION
    assert registered.crosscheck_location == "Table 1, Potential parameters"
    assert registered.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert len(registered.source_file_sha256) == 64
    assert registered.source_authors == (
        "A. L. Smith", "E. Capelli", "R. J. M. Konings", "A. E. Gheribi"
    )
    assert registered == load_flibe_registered_pair_parameters(str(SOURCE))


@pytest.mark.parametrize("index", range(6))
def test_all_six_published_pair_rows_match_independent_anchors(index: int) -> None:
    record = _load().pair_coefficients[index]
    a, b, amplitude, decay, c6, c8, beta6, beta8 = EXPECTED_PAIRS[index]
    assert (record.species_a.value, record.species_b.value) == (a, b)
    assert (record.species_a, record.species_b) == PAIR_ORDER[index]
    assert record.born_amplitude_hartree == amplitude
    assert record.born_decay_inverse_bohr == decay
    assert record.c6_hartree_bohr6 == c6
    assert record.c8_hartree_bohr8 == c8
    assert record.b6_inverse_bohr == beta6
    assert record.b8_inverse_bohr == beta8
    assert record.provenance is ParameterProvenance.PRIMARY_SOURCE
    assert record.source_id == SOURCE_DOI
    assert record.source_location == SOURCE_LOCATION


def test_original_table_order_and_unit_registry() -> None:
    payload = _payload()
    assert tuple(map(tuple, payload["source_table_pair_order"])) == SOURCE_PAIR_ORDER
    assert tuple(map(tuple, payload["canonical_pair_order"])) == tuple(
        (row[0], row[1]) for row in EXPECTED_PAIRS
    )
    assert payload["parameter_units"] == {
        "born_amplitude_hartree": "hartree",
        "born_decay_inverse_bohr": "bohr^-1",
        "c6_hartree_bohr6": "hartree*bohr^6",
        "c8_hartree_bohr8": "hartree*bohr^8",
        "b6_inverse_bohr": "bohr^-1",
        "b8_inverse_bohr": "bohr^-1",
    }
    assert payload["pair_functional"]["functional_id"] == PAIR_FUNCTIONAL_ID
    assert payload["material"]["formal_charges_e"] == CHARGES


def test_polarization_parameters_preserved_outside_pair_model() -> None:
    registered = _load()
    assert registered.fluoride_polarizability_bohr3 == 7.09
    assert len(registered.charge_dipole_damping) == 2
    assert all(isinstance(item, FLiBeChargeDipoleSourceParameter)
               for item in registered.charge_dipole_damping)
    assert tuple((value.species_pair[0].value, value.species_pair[1].value,
                  value.b_inverse_bohr, value.c_dimensionless)
                 for value in registered.charge_dipole_damping) == (
        ("Be", "F", 1.78, 0.99), ("Li", "F", 1.81, 1.4)
    )
    assert registered.separate_model_terms == (
        "induced-dipole polarization", "periodic long-range electrostatics"
    )


def test_primary_source_model_binding_and_analytical_lif_energy() -> None:
    parameters = _load()
    model = parameters.build_finite_cluster_model(
        model_id="FLIBE-SMITH-2020-SOURCE-PAIR",
        coordinate_unit_to_bohr=1.0,
    )
    assert isinstance(model, FLiBeIndependentPairModel)
    assert model.pair_coefficients == parameters.pair_coefficients
    assert model.length_unit_to_bohr == 1.0
    configuration = _configuration(("Li", "F"), ((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    result = model.evaluate(configuration)
    # Published Li-F Born term and formal Coulomb charge product at r=2 bohr.
    expected_energy = -0.5 + 20.42 * exp(-2.052 * 2.0)
    expected_radial_derivative = 0.25 - 2.052 * 20.42 * exp(-2.052 * 2.0)
    assert result.energy.total_energy == pytest.approx(
        expected_energy, rel=0.0, abs=ENERGY_ABS_TOL
    )
    assert result.energy.atomic_energies == pytest.approx(
        (expected_energy / 2.0,) * 2, rel=0.0, abs=ENERGY_ABS_TOL
    )
    assert result.forces.forces[0] == pytest.approx(
        (expected_radial_derivative, 0.0, 0.0), rel=0.0, abs=ENERGY_ABS_TOL
    )
    assert result.forces.forces[1] == pytest.approx(
        (-expected_radial_derivative, 0.0, 0.0), rel=0.0, abs=ENERGY_ABS_TOL
    )
    assert result.pair_count == 1
    assert result.pair_coefficients == parameters.pair_coefficients


def test_seven_atom_flibe_energy_matches_independent_decimal_reference() -> None:
    parameters = _load()
    model = parameters.build_finite_cluster_model(
        model_id="FLIBE-SOURCE-SEVEN-ATOM", coordinate_unit_to_bohr=1.0
    )
    configuration = _configuration()
    assert configuration.composition().formula_unit_fractions == (
        2.0 / 3.0, 1.0 / 3.0
    )
    result = model.evaluate(configuration)
    expected = _analytic_pair_energy(SPECIES, POSITIONS)
    assert result.energy.total_energy == pytest.approx(
        expected, rel=0.0, abs=ENERGY_ABS_TOL
    )
    assert result.energy.total_energy == pytest.approx(
        fsum(result.energy.atomic_energies), rel=0.0, abs=ENERGY_ABS_TOL
    )
    assert result.pair_count == 21
    assert all(isfinite(value) for row in result.forces.forces for value in row)
    for axis in range(3):
        assert abs(fsum(row[axis] for row in result.forces.forces)) <= 1.0e-10


def test_loaded_source_model_is_deterministic_and_immutable() -> None:
    parameters = _load()
    first = parameters.build_finite_cluster_model(
        model_id="REGISTERED-PAIR", coordinate_unit_to_bohr=1.0
    ).evaluate(_configuration())
    second = parameters.build_finite_cluster_model(
        model_id="REGISTERED-PAIR", coordinate_unit_to_bohr=1.0
    ).evaluate(_configuration())
    assert first == second
    with pytest.raises(FrozenInstanceError):
        parameters.source_doi = "modified"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        parameters.pair_coefficients[0].source_id = "modified"  # type: ignore[misc]


def test_valid_source_change_updates_digest_coefficient_and_energy(tmp_path: Path) -> None:
    baseline = _load()
    payload = _payload()
    payload["pair_coefficients"][2]["born_amplitude_hartree"] += 0.5
    revised = _load(_modified(tmp_path, payload))
    assert revised.source_file_sha256 != baseline.source_file_sha256
    assert revised.pair_coefficients[2].born_amplitude_hartree == 20.92
    assert revised.pair_coefficients[:2] == baseline.pair_coefficients[:2]
    configuration = _configuration(("Li", "F"), ((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    a = baseline.build_finite_cluster_model(
        model_id="ORIGINAL", coordinate_unit_to_bohr=1.0
    ).evaluate(configuration).energy.total_energy
    b = revised.build_finite_cluster_model(
        model_id="ALTERED", coordinate_unit_to_bohr=1.0
    ).evaluate(configuration).energy.total_energy
    assert b - a == pytest.approx(0.5 * exp(-2.052 * 2.0), rel=0, abs=1.0e-12)


def test_polarization_metadata_remains_independent_of_pair_energy(tmp_path: Path) -> None:
    baseline = _load()
    payload = _payload()
    payload["additional_source_model_terms"]["fluoride_polarizability_bohr3"] = 8.0
    revised = _load(_modified(tmp_path, payload))
    assert revised.source_file_sha256 != baseline.source_file_sha256
    assert revised.fluoride_polarizability_bohr3 == 8.0
    assert revised.pair_coefficients == baseline.pair_coefficients
    a = baseline.build_finite_cluster_model(model_id="PAIR", coordinate_unit_to_bohr=1.0)
    b = revised.build_finite_cluster_model(model_id="PAIR", coordinate_unit_to_bohr=1.0)
    assert a.evaluate(_configuration()).energy == b.evaluate(_configuration()).energy


@pytest.mark.parametrize(
    ("section", "key", "invalid", "error"),
    (
        (None, "dataset_id", "OTHER", ValueError),
        (None, "provenance", "TEST_FIXTURE", ValueError),
        (None, "record_kind", "DERIVED", ValueError),
        ("source", "doi", "10.0000/incorrect", ValueError),
        ("source", "year", 2021, ValueError),
        ("source", "source_model_family", "other", ValueError),
        ("independent_table_crosscheck", "doi", "10.0000/incorrect", ValueError),
        ("material", "composition_domain", "OTHER", ValueError),
        ("material", "ionic_species_order", ["F", "Li", "Be"], ValueError),
        ("material", "formal_charges_e", {"Li": 1, "Be": 2, "F": 0}, ValueError),
        ("parameter_units", "c6_hartree_bohr6", "eV*angstrom^6", ValueError),
        ("pair_functional", "distance_unit", "angstrom", ValueError),
        ("implementation_mapping", "target_boundary", "periodic", ValueError),
        ("additional_source_model_terms", "term_roles", ["pair"], ValueError),
        ("additional_source_model_terms", "fluoride_polarizability_bohr3", -1.0, ValueError),
    ),
)
def test_source_contract_rejects_changed_identity_or_units(
    tmp_path: Path, section: str | None, key: str, invalid: object, error: type[Exception]
) -> None:
    payload = _payload()
    container = payload if section is None else payload[section]
    container[key] = invalid
    with pytest.raises(error):
        _load(_modified(tmp_path, payload))


@pytest.mark.parametrize(
    ("index", "field", "invalid", "error"),
    (
        (0, "species_a", "F", ValueError),
        (1, "species_b", "Li", ValueError),
        (2, "born_amplitude_hartree", -0.1, ValueError),
        (2, "born_amplitude_hartree", float("nan"), ValueError),
        (2, "born_decay_inverse_bohr", 0.0, ValueError),
        (5, "c6_hartree_bohr6", -1.0, ValueError),
        (5, "b6_inverse_bohr", 0.0, ValueError),
        (5, "b8_inverse_bohr", False, TypeError),
    ),
)
def test_source_contract_rejects_invalid_pair_coefficients(
    tmp_path: Path, index: int, field: str, invalid: object, error: type[Exception]
) -> None:
    payload = _payload()
    payload["pair_coefficients"][index][field] = invalid
    with pytest.raises(error):
        _load(_modified(tmp_path, payload))


def test_source_contract_rejects_missing_extra_and_reordered_pairs(tmp_path: Path) -> None:
    payload = _payload()
    payload["pair_coefficients"] = payload["pair_coefficients"][:-1]
    with pytest.raises(ValueError):
        _load(_modified(tmp_path, payload))
    payload = _payload()
    payload["pair_coefficients"][0], payload["pair_coefficients"][1] = (
        payload["pair_coefficients"][1], payload["pair_coefficients"][0]
    )
    with pytest.raises(ValueError):
        _load(_modified(tmp_path, payload))
    payload = _payload()
    payload["pair_coefficients"][0]["unregistered"] = 1.0
    with pytest.raises(ValueError):
        _load(_modified(tmp_path, payload))
    payload = _payload()
    del payload["additional_source_model_terms"]
    with pytest.raises(ValueError):
        _load(_modified(tmp_path, payload))


def test_source_contract_rejects_polarization_pair_mismatch(tmp_path: Path) -> None:
    payload = _payload()
    payload["additional_source_model_terms"]["charge_dipole_damping"][0][
        "species_pair"
    ] = ["F", "Li"]
    with pytest.raises(ValueError):
        _load(_modified(tmp_path, payload))
    payload = _payload()
    payload["additional_source_model_terms"]["charge_dipole_damping"][1][
        "b_inverse_bohr"
    ] = 0.0
    with pytest.raises(ValueError):
        _load(_modified(tmp_path, payload))


@pytest.mark.parametrize("invalid", (None, 17, True, 2.5, object()))
def test_loader_rejects_nonpath_arguments(invalid: object) -> None:
    with pytest.raises(TypeError):
        load_flibe_registered_pair_parameters(invalid)


def test_loader_reports_missing_file_and_malformed_json(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        _load(tmp_path / "missing.json")
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        _load(malformed)
