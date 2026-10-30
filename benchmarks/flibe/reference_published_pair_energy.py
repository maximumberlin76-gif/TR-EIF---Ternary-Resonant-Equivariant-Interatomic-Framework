"""Source-parameter FLiBe finite-cluster pair-energy and force benchmark.

The registered Li/Be/F pair coefficients supply Coulomb, Born-Mayer,
and damped C6/C8 contributions. A separate high-precision evaluation
of the declared radial law provides energy and Cartesian force references.
Polarization parameters remain associated with the source registration.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal, localcontext
from math import factorial, fsum, isclose, sqrt
from pathlib import Path

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.charge import total_formal_charge
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.independent_pair_potential import PAIR_FUNCTIONAL_ID
from tr_eif.flibe.registered_pair_coefficients import (
    CROSSCHECK_DOI,
    DATASET_ID,
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.units import ParameterProvenance


BENCHMARK_ID = "tr-eif.flibe.published-pair-energy-force.v1"
DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
)
MODEL_ID = "FLIBE-SMITH-2020-FINITE-CLUSTER-PAIR"
ENERGY_TOL_HARTREE = 1.0e-9
FORCE_TOL_HARTREE_PER_BOHR = 3.0e-8
COORDINATE_UNIT_TO_BOHR = 1.0

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS_BOHR = (
    (0.0, 0.0, 0.0),
    (3.0, 0.3, 0.0),
    (1.0, 2.3, 0.2),
    (0.6, 0.3, 1.6),
    (2.9, 1.0, 2.2),
    (1.1, 3.0, 2.1),
    (3.2, 2.8, 0.8),
)
FORMAL_CHARGE = {"Li": 1, "Be": 2, "F": -1}

# Independent published Table 1 anchors, in canonical pair order.
# Columns: species, A, alpha, C6, C8, b6, b8, in atomic units.
SOURCE_ANCHORS = (
    ("Li", "Li", 195.91, 4.252, 0.0, 0.0, 1.0, 1.0),
    ("Li", "Be", 0.0, 1.0, 0.0, 0.0, 1.0, 1.0),
    ("Li", "F", 20.42, 2.052, 0.0, 0.0, 1.0, 1.0),
    ("Be", "Be", 106.16, 3.944, 0.0, 0.0, 1.0, 1.0),
    ("Be", "F", 41.72, 2.254, 0.0, 0.0, 1.0, 1.0),
    ("F", "F", 181.84, 2.267, 15.0, 150.0, 1.9, 1.9),
)


def _configuration(species, positions):
    return FLiBeConfiguration(
        AtomicConfiguration(species=tuple(species), positions=tuple(positions))
    )


def _direct_energy_forces(species, positions):
    """Evaluate the published radial potential and derivative in Decimal."""
    coefficient_by_pair = {
        frozenset((entry[0], entry[1])): entry[2:]
        for entry in SOURCE_ANCHORS
    }
    with localcontext() as context:
        context.prec = 60
        d = lambda value: Decimal(str(value))
        coordinates = tuple(tuple(d(value) for value in xyz) for xyz in positions)
        energies = [Decimal(0) for _ in species]
        forces = [[Decimal(0)] * 3 for _ in species]
        for i in range(len(species)):
            for j in range(i + 1, len(species)):
                vector = tuple(coordinates[i][k] - coordinates[j][k] for k in range(3))
                radius = sum(component * component for component in vector).sqrt()
                if radius <= 0:
                    raise ValueError("Reference pair distance must be positive.")
                a, alpha, c6, c8, b6, b8 = coefficient_by_pair[
                    frozenset((species[i], species[j]))
                ]
                charge_product = Decimal(FORMAL_CHARGE[species[i]] * FORMAL_CHARGE[species[j]])
                repulsion = d(a) * (-d(alpha) * radius).exp()
                energy = charge_product / radius + repulsion
                derivative = -charge_product / radius**2 - d(alpha) * repulsion
                for order, coefficient, b in ((6, c6, b6), (8, c8, b8)):
                    if coefficient == 0:
                        continue
                    z = d(b) * radius
                    exponential = (-z).exp()
                    polynomial = sum(
                        (z**k / Decimal(factorial(k)) for k in range(order + 1)),
                        Decimal(0),
                    )
                    damping = 1 - exponential * polynomial
                    damping_derivative = exponential * z**order / Decimal(factorial(order))
                    energy -= d(coefficient) * damping / radius**order
                    derivative -= d(coefficient) * (
                        d(b) * damping_derivative / radius**order
                        - Decimal(order) * damping / radius**(order + 1)
                    )
                energies[i] += energy / 2
                energies[j] += energy / 2
                for k in range(3):
                    force_component = -derivative * vector[k] / radius
                    forces[i][k] += force_component
                    forces[j][k] -= force_component
        return (
            tuple(float(value) for value in energies),
            tuple(tuple(float(value) for value in row) for row in forces),
        )


def _vectors_match(actual, expected, tolerance):
    return len(actual) == len(expected) and all(
        all(isclose(a, b, rel_tol=0.0, abs_tol=tolerance)
            for a, b in zip(vector, reference, strict=True))
        for vector, reference in zip(actual, expected, strict=True)
    )


def _scalar_match(a, b):
    return isclose(a, b, rel_tol=0.0, abs_tol=ENERGY_TOL_HARTREE)


def _rotate_translate(position):
    return (-position[1] + 3.0, position[0] - 2.0, position[2] + 1.25)


def _rotate_vector(vector):
    return (-vector[1], vector[0], vector[2])


def run_benchmark() -> dict[str, object]:
    """Evaluate source-bound pair forces, independent references, and E(3)."""
    source = load_flibe_registered_pair_parameters(DATA_PATH)
    model = source.build_finite_cluster_model(
        model_id=MODEL_ID, coordinate_unit_to_bohr=COORDINATE_UNIT_TO_BOHR
    )
    configuration = _configuration(SPECIES, POSITIONS_BOHR)
    observed = model.evaluate(configuration)
    replay = model.evaluate(configuration)
    analytical_energy, analytical_forces = _direct_energy_forces(SPECIES, POSITIONS_BOHR)
    reference_total = fsum(analytical_energy)

    lif = _configuration(("Li", "F"), ((0.0, 0.0, 0.0), (2.0, 0.0, 0.0)))
    lif_observed = model.evaluate(lif)
    lif_reference_energy, lif_reference_forces = _direct_energy_forces(
        ("Li", "F"), ((0.0, 0.0, 0.0), (2.0, 0.0, 0.0))
    )

    rotated = model.evaluate(_configuration(
        SPECIES, tuple(_rotate_translate(position) for position in POSITIONS_BOHR)
    ))
    permutation = (6, 2, 0, 4, 1, 5, 3)
    permuted = model.evaluate(_configuration(
        tuple(SPECIES[i] for i in permutation),
        tuple(POSITIONS_BOHR[i] for i in permutation),
    ))
    expected_rows = tuple(
        (pair.species_a.value, pair.species_b.value,
         pair.born_amplitude_hartree, pair.born_decay_inverse_bohr,
         pair.c6_hartree_bohr6, pair.c8_hartree_bohr8,
         pair.b6_inverse_bohr, pair.b8_inverse_bohr)
        for pair in source.pair_coefficients
    )
    force_residuals = tuple(
        observed.forces.forces[i][j] - analytical_forces[i][j]
        for i in range(len(SPECIES)) for j in range(3)
    )
    checks = {
        "registered_source_identity": source.dataset_id == DATASET_ID
            and source.source_doi == SOURCE_DOI
            and source.crosscheck_doi == CROSSCHECK_DOI,
        "source_file_fingerprint": source.source_file_sha256
            == hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(),
        "source_pair_table": expected_rows == SOURCE_ANCHORS,
        "source_pair_provenance": all(
            pair.provenance is ParameterProvenance.PRIMARY_SOURCE
            and pair.source_id == SOURCE_DOI
            for pair in source.pair_coefficients
        ),
        "pair_functional_identity": observed.pair_functional_id == PAIR_FUNCTIONAL_ID,
        "formal_charge_balance": total_formal_charge(configuration) == 0,
        "exact_formula_composition": configuration.composition().formula_unit_fractions
            == (2.0 / 3.0, 1.0 / 3.0),
        "cluster_pair_count": observed.pair_count == 21,
        "source_energy_reference": _scalar_match(observed.energy.total_energy, reference_total),
        "source_atomic_energy_reference": all(
            _scalar_match(a, b) for a, b in zip(
                observed.energy.atomic_energies, analytical_energy, strict=True
            )
        ),
        "source_force_reference": _vectors_match(
            observed.forces.forces, analytical_forces, FORCE_TOL_HARTREE_PER_BOHR
        ),
        "lif_energy_reference": _scalar_match(
            lif_observed.energy.total_energy, fsum(lif_reference_energy)
        ),
        "lif_force_reference": _vectors_match(
            lif_observed.forces.forces, lif_reference_forces, FORCE_TOL_HARTREE_PER_BOHR
        ),
        "atomic_partition": _scalar_match(
            observed.energy.total_energy, fsum(observed.energy.atomic_energies)
        ),
        "net_force_balance": all(
            abs(fsum(force[axis] for force in observed.forces.forces))
            <= FORCE_TOL_HARTREE_PER_BOHR for axis in range(3)
        ),
        "exact_replay": observed == replay,
        "e3_energy_invariance": _scalar_match(
            observed.energy.total_energy, rotated.energy.total_energy
        ),
        "e3_force_covariance": _vectors_match(
            rotated.forces.forces,
            tuple(_rotate_vector(vector) for vector in observed.forces.forces),
            FORCE_TOL_HARTREE_PER_BOHR,
        ),
        "permutation_energy_invariance": _scalar_match(
            observed.energy.total_energy, permuted.energy.total_energy
        ),
        "permutation_force_covariance": _vectors_match(
            permuted.forces.forces,
            tuple(observed.forces.forces[i] for i in permutation),
            FORCE_TOL_HARTREE_PER_BOHR,
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source": {
            "dataset_id": source.dataset_id,
            "doi": source.source_doi,
            "table_location": source.source_location,
            "crosscheck_doi": source.crosscheck_doi,
            "file_sha256": source.source_file_sha256,
            "provenance": ParameterProvenance.PRIMARY_SOURCE.value,
            "registered_fluoride_polarizability_bohr3": source.fluoride_polarizability_bohr3,
            "registered_separate_terms": list(source.separate_model_terms),
        },
        "model": {
            "model_id": model.model_id,
            "functional_id": PAIR_FUNCTIONAL_ID,
            "boundary": "isolated_nonperiodic_finite_cluster",
            "coordinate_unit_to_bohr": COORDINATE_UNIT_TO_BOHR,
            "energy_unit": "hartree",
            "force_unit": "hartree/bohr",
        },
        "fixture": {
            "species": list(SPECIES),
            "positions_bohr": [list(position) for position in POSITIONS_BOHR],
            "atom_count": configuration.atom_count,
            "pair_count": observed.pair_count,
            "model_energy_hartree": observed.energy.total_energy,
            "analytical_energy_hartree": reference_total,
            "energy_residual_hartree": observed.energy.total_energy - reference_total,
            "model_forces_hartree_per_bohr": [list(row) for row in observed.forces.forces],
            "force_max_abs_residual_hartree_per_bohr": max(
                abs(value) for value in force_residuals
            ),
            "force_rmse_hartree_per_bohr": sqrt(
                fsum(value * value for value in force_residuals) / len(force_residuals)
            ),
        },
        "two_atom_lif": {
            "separation_bohr": 2.0,
            "model_energy_hartree": lif_observed.energy.total_energy,
            "analytical_energy_hartree": fsum(lif_reference_energy),
        },
        "numeric_criteria": {
            "energy_absolute_tolerance_hartree": ENERGY_TOL_HARTREE,
            "force_absolute_tolerance_hartree_per_bohr": FORCE_TOL_HARTREE_PER_BOHR,
        },
        "checks": checks,
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if report["status"] == "PASS" else 1)
