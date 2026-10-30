"""Load registered FLiBe PIM pair coefficients into the finite-cluster model.

The source table supplies Born-Mayer and damped C6/C8 parameters;
formal ionic charges determine the Coulomb term. Induced-dipole
polarization and periodic electrostatics retain separate source metadata.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from math import isfinite
from pathlib import Path

from .charge import FLIBE_FORMAL_CHARGES
from .independent_pair_potential import (
    PAIR_FUNCTIONAL_ID,
    PAIR_ORDER,
    FLiBeIndependentPairModel,
    FLiBePairCoefficients,
)
from .species import FLIBE_SPECIES, FLiBeSpecies
from .units import ParameterProvenance


DATASET_ID = "tr-eif.flibe.smith-2020.pim-pair-coefficients.v1"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
CROSSCHECK_DOI = "10.1016/j.crci.2007.03.002"

_PARAMETER_UNITS = {
    "born_amplitude_hartree": "hartree",
    "born_decay_inverse_bohr": "bohr^-1",
    "c6_hartree_bohr6": "hartree*bohr^6",
    "c8_hartree_bohr8": "hartree*bohr^8",
    "b6_inverse_bohr": "bohr^-1",
    "b8_inverse_bohr": "bohr^-1",
}
_SOURCE_PAIR_ORDER = (
    ("F", "F"),
    ("Be", "F"),
    ("Li", "F"),
    ("Be", "Be"),
    ("Li", "Be"),
    ("Li", "Li"),
)
_CANONICAL_PAIR_ORDER = tuple((a.value, b.value) for a, b in PAIR_ORDER)
_SOURCE_TERMS = (
    "induced-dipole polarization",
    "periodic long-range electrostatics",
)
_MAPPED_TERMS = (
    "formal-charge Coulomb",
    "Born-Mayer repulsion",
    "Tang-Toennies-damped C6 and C8 dispersion",
)
_COEFFICIENT_FIELDS = ("species_a", "species_b", *_PARAMETER_UNITS)
_ROOT_FIELDS = (
    "dataset_id", "record_kind", "provenance", "source",
    "independent_table_crosscheck", "material", "parameter_units",
    "pair_functional", "source_table_pair_order", "canonical_pair_order",
    "pair_coefficients", "additional_source_model_terms", "implementation_mapping",
)
_PAIR_FUNCTIONAL = {
    "functional_id": PAIR_FUNCTIONAL_ID,
    "coulomb": "q_i*q_j/r",
    "born_repulsion": "A_ij*exp(-alpha_ij*r)",
    "damped_dispersion": "-C6_ij*f6(b6_ij*r)/r^6-C8_ij*f8(b8_ij*r)/r^8",
    "damping": "f_n(z)=1-exp(-z)*sum(z^k/k!,k=0..n)",
    "distance_unit": "bohr",
    "energy_unit": "hartree",
}


def _object(value: object, name: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(k, str) for k in value):
        raise ValueError(f"{name} must be a JSON object with string keys.")
    return value


def _fields(obj: dict[str, object], expected: tuple[str, ...], name: str) -> None:
    if set(obj) != set(expected):
        raise ValueError(f"{name} fields differ from the registered contract.")


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{name} must be a nonempty trimmed string.")
    return value


def _number(value: object, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number < 0.0 or (positive and number == 0.0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}.")
    return number


def _pair(value: object, name: str) -> tuple[FLiBeSpecies, FLiBeSpecies]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{name} must contain two species symbols.")
    if not all(isinstance(symbol, str) for symbol in value):
        raise ValueError(f"{name} species must be element symbols.")
    try:
        return (FLiBeSpecies(value[0]), FLiBeSpecies(value[1]))
    except ValueError as error:
        raise ValueError(f"{name} contains an unsupported FLiBe species.") from error


def _pair_order(value: object, name: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list) or len(value) != len(PAIR_ORDER):
        raise ValueError(f"{name} must contain six species pairs.")
    return tuple(tuple(symbol.value for symbol in _pair(item, name)) for item in value)


def _text_sequence(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a nonempty array.")
    return tuple(_text(item, name) for item in value)


@dataclass(frozen=True, slots=True)
class FLiBeChargeDipoleSourceParameter:
    """Registered charge-dipole damping parameter, stored outside pair energy."""

    species_pair: tuple[FLiBeSpecies, FLiBeSpecies]
    b_inverse_bohr: float
    c_dimensionless: float

    def __post_init__(self) -> None:
        if self.species_pair not in (
            (FLiBeSpecies.BERYLLIUM, FLiBeSpecies.FLUORINE),
            (FLiBeSpecies.LITHIUM, FLiBeSpecies.FLUORINE),
        ):
            raise ValueError("charge-dipole species pair differs.")
        _number(self.b_inverse_bohr, "b_inverse_bohr", positive=True)
        _number(self.c_dimensionless, "c_dimensionless")


@dataclass(frozen=True, slots=True)
class FLiBeRegisteredPairParameters:
    """Typed primary-source parameters, data fingerprint, and model boundary."""

    dataset_id: str
    source_doi: str
    source_location: str
    source_authors: tuple[str, ...]
    crosscheck_doi: str
    crosscheck_location: str
    source_file_sha256: str
    pair_coefficients: tuple[FLiBePairCoefficients, ...]
    fluoride_polarizability_bohr3: float
    charge_dipole_damping: tuple[FLiBeChargeDipoleSourceParameter, ...]
    separate_model_terms: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.dataset_id != DATASET_ID or self.source_doi != SOURCE_DOI:
            raise ValueError("registered source identity differs.")
        if self.crosscheck_doi != CROSSCHECK_DOI:
            raise ValueError("crosscheck DOI differs.")
        _text(self.source_location, "source_location")
        _text(self.crosscheck_location, "crosscheck_location")
        if not self.source_authors or any(not isinstance(s, str) or not s.strip()
                                          for s in self.source_authors):
            raise ValueError("source_authors must be specified.")
        digest = self.source_file_sha256
        if not isinstance(digest, str) or len(digest) != 64 or any(
            c not in "0123456789abcdef" for c in digest
        ):
            raise ValueError("source_file_sha256 must be a lowercase SHA-256 digest.")
        if len(self.pair_coefficients) != len(PAIR_ORDER):
            raise ValueError("six canonical pair coefficients are required.")
        for expected, coefficient in zip(PAIR_ORDER, self.pair_coefficients, strict=True):
            if not isinstance(coefficient, FLiBePairCoefficients) or (
                coefficient.species_a, coefficient.species_b
            ) != expected:
                raise ValueError("pair coefficients must follow canonical species order.")
            if coefficient.provenance is not ParameterProvenance.PRIMARY_SOURCE:
                raise ValueError("pair provenance must be PRIMARY_SOURCE.")
            if coefficient.source_id != self.source_doi or (
                coefficient.source_location != self.source_location
            ):
                raise ValueError("pair source DOI and table location must agree.")
        _number(self.fluoride_polarizability_bohr3, "fluoride_polarizability_bohr3", positive=True)
        if not isinstance(self.charge_dipole_damping, tuple) or len(self.charge_dipole_damping) != 2:
            raise ValueError("two charge-dipole source records are required.")
        if not all(isinstance(item, FLiBeChargeDipoleSourceParameter)
                   for item in self.charge_dipole_damping):
            raise TypeError("charge_dipole_damping must contain typed source parameters.")
        if tuple(item.species_pair for item in self.charge_dipole_damping) != (
            (FLiBeSpecies.BERYLLIUM, FLiBeSpecies.FLUORINE),
            (FLiBeSpecies.LITHIUM, FLiBeSpecies.FLUORINE),
        ):
            raise ValueError("charge-dipole damping pair order differs.")
        if self.separate_model_terms != _SOURCE_TERMS:
            raise ValueError("PIM non-pair term identities differ.")

    def build_finite_cluster_model(
        self, *, model_id: str, coordinate_unit_to_bohr: float
    ) -> FLiBeIndependentPairModel:
        """Bind the registered pair terms to an isolated finite-cluster model."""
        return FLiBeIndependentPairModel(
            model_id=model_id,
            pair_coefficients=self.pair_coefficients,
            length_unit_to_bohr=coordinate_unit_to_bohr,
        )


def load_flibe_registered_pair_parameters(path: str | Path) -> FLiBeRegisteredPairParameters:
    """Read the published pair table with original source metadata and SHA-256.

    Pair coefficients populate FLiBeIndependentPairModel; fluoride polarizability,
    charge-dipole damping, and periodic electrostatics remain separately recorded.
    The caller supplies the dataset file path and the model's Cartesian unit.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or pathlib.Path.")
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    data = _object(json.loads(raw.decode("utf-8")), "registered dataset")
    _fields(data, _ROOT_FIELDS, "registered dataset")
    if data.get("dataset_id") != DATASET_ID or data.get("record_kind") != (
        "PUBLISHED_INTERATOMIC_PARAMETER_TABLE"
    ) or data.get("provenance") != "PRIMARY_SOURCE":
        raise ValueError("registered dataset identity or provenance differs.")

    source = _object(data.get("source"), "source")
    crosscheck = _object(data.get("independent_table_crosscheck"), "independent_table_crosscheck")
    doi = _text(source.get("doi"), "source DOI")
    location = _text(source.get("source_location"), "source_location")
    crosscheck_doi = _text(crosscheck.get("doi"), "crosscheck DOI")
    crosscheck_location = _text(crosscheck.get("source_location"), "crosscheck location")
    if doi != SOURCE_DOI or crosscheck_doi != CROSSCHECK_DOI:
        raise ValueError("registered primary or crosscheck DOI differs.")
    if source.get("year") != 2020 or crosscheck.get("year") != 2007:
        raise ValueError("source publication year differs.")
    if crosscheck.get("table_relation") != "Same six pair coefficient sets in atomic units":
        raise ValueError("source table crosscheck relation differs.")
    if source.get("source_model_family") != "polarizable ion model (PIM)":
        raise ValueError("source model family differs.")
    authors = _text_sequence(source.get("authors"), "source authors")
    _text(source.get("title"), "source title")
    _text(source.get("journal"), "source journal")
    _text(crosscheck.get("title"), "crosscheck title")
    _text_sequence(crosscheck.get("authors"), "crosscheck authors")

    material = _object(data.get("material"), "material")
    if (material.get("system") != "LiF-BeF2"
        or material.get("composition_domain") != "LiF-BeF2 binary mixture"
        or material.get("ionic_species_order") != [s.value for s in FLIBE_SPECIES]):
        raise ValueError("material species or system contract differs.")
    charges = _object(material.get("formal_charges_e"), "formal_charges_e")
    expected_charges = {species.value: q for species, q in FLIBE_FORMAL_CHARGES}
    if set(charges) != set(expected_charges) or any(
        type(charges[name]) is not int or charges[name] != value
        for name, value in expected_charges.items()
    ):
        raise ValueError("formal charges differ from the FLiBe charge contract.")

    if _object(data.get("parameter_units"), "parameter_units") != _PARAMETER_UNITS:
        raise ValueError("pair parameter units differ from the atomic-unit contract.")
    functional = _object(data.get("pair_functional"), "pair_functional")
    if functional != _PAIR_FUNCTIONAL:
        raise ValueError("pair functional or energy/length units differ.")

    if _pair_order(data.get("source_table_pair_order"), "source_table_pair_order") != _SOURCE_PAIR_ORDER:
        raise ValueError("source table pair order differs.")
    if _pair_order(data.get("canonical_pair_order"), "canonical_pair_order") != (
        _CANONICAL_PAIR_ORDER
    ):
        raise ValueError("canonical pair order differs.")
    values = data.get("pair_coefficients")
    if not isinstance(values, list) or len(values) != len(PAIR_ORDER):
        raise ValueError("six canonical pair coefficient rows are required.")
    coefficients: list[FLiBePairCoefficients] = []
    for index, raw_row in enumerate(values):
        row = _object(raw_row, f"pair_coefficients[{index}]")
        _fields(row, _COEFFICIENT_FIELDS, f"pair_coefficients[{index}]")
        species_a, species_b = _pair(
            [row["species_a"], row["species_b"]], f"pair_coefficients[{index}]"
        )
        if (species_a, species_b) != PAIR_ORDER[index]:
            raise ValueError("pair coefficient rows must follow canonical species order.")
        coefficients.append(FLiBePairCoefficients(
            species_a=species_a,
            species_b=species_b,
            **{name: _number(row[name], name) for name in _PARAMETER_UNITS},
            provenance=ParameterProvenance.PRIMARY_SOURCE,
            source_id=doi,
            source_location=location,
        ))

    remaining = _object(data.get("additional_source_model_terms"), "additional_source_model_terms")
    polarizability = _number(remaining.get("fluoride_polarizability_bohr3"),
                            "fluoride_polarizability_bohr3", positive=True)
    dampings = remaining.get("charge_dipole_damping")
    if not isinstance(dampings, list) or len(dampings) != 2:
        raise ValueError("two charge-dipole damping source rows are required.")
    damping_records: list[FLiBeChargeDipoleSourceParameter] = []
    for index, raw_item in enumerate(dampings):
        item = _object(raw_item, f"charge_dipole_damping[{index}]")
        _fields(item, ("species_pair", "b_inverse_bohr", "c_dimensionless"),
                f"charge_dipole_damping[{index}]")
        damping_records.append(FLiBeChargeDipoleSourceParameter(
            species_pair=_pair(item["species_pair"], f"charge_dipole_damping[{index}].species_pair"),
            b_inverse_bohr=_number(item["b_inverse_bohr"], "b_inverse_bohr", positive=True),
            c_dimensionless=_number(item["c_dimensionless"], "c_dimensionless"),
        ))
    if tuple((p.species_pair[0].value, p.species_pair[1].value)
             for p in damping_records) != (("Be", "F"), ("Li", "F")):
        raise ValueError("charge-dipole damping pair identities differ.")
    roles = _text_sequence(remaining.get("term_roles"), "term_roles")
    if roles != _SOURCE_TERMS:
        raise ValueError("PIM non-pair term identities differ.")

    target = _object(data.get("implementation_mapping"), "implementation_mapping")
    if (target.get("target_module") != "src/tr_eif/flibe/independent_pair_potential.py"
        or target.get("target_model") != "FLiBeIndependentPairModel"
        or target.get("parameter_type") != "FLiBePairCoefficients"
        or target.get("target_boundary") != "isolated nonperiodic finite cluster"
        or target.get("mapped_terms") != list(_MAPPED_TERMS)
        or target.get("separately_modeled_terms") != list(_SOURCE_TERMS)):
        raise ValueError("source terms or finite-cluster implementation boundary differ.")

    return FLiBeRegisteredPairParameters(
        dataset_id=DATASET_ID,
        source_doi=doi,
        source_location=location,
        source_authors=authors,
        crosscheck_doi=crosscheck_doi,
        crosscheck_location=crosscheck_location,
        source_file_sha256=digest,
        pair_coefficients=tuple(coefficients),
        fluoride_polarizability_bohr3=polarizability,
        charge_dipole_damping=tuple(damping_records),
        separate_model_terms=roles,
    )
