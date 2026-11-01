"""Independent energy-gradient and symmetry tests for FLiBe polarization forces."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import exp, factorial, fsum
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.finite_cluster_polarization import FLiBeFiniteClusterPolarizationModel
from tr_eif.flibe.finite_cluster_polarization_forces import (
    FORCE_FUNCTIONAL_ID,
    FLiBeFiniteClusterPolarizationForceResult,
    evaluate_flibe_finite_cluster_polarization_forces,
)
from tr_eif.flibe.registered_pair_coefficients import (
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS_BOHR = (
    (0.0, 0.0, 0.0),
    (8.0, 0.0, 0.0),
    (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0),
    (8.0, 5.0, 6.0),
    (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
DIFFERENCE_STEP = 2.0e-5
FORCE_ABSOLUTE_TOLERANCE = 2.0e-7
SYMMETRY_ABSOLUTE_TOLERANCE = 1.0e-9
ENERGY_ABSOLUTE_TOLERANCE = 2.0e-11
STATIONARITY_ABSOLUTE_TOLERANCE = 1.0e-10


@pytest.fixture(scope="module")
def parameters():
    return load_flibe_registered_pair_parameters(SOURCE)


@pytest.fixture(scope="module")
def model(parameters):
    return FLiBeFiniteClusterPolarizationModel(
        model_id="FLIBE-PUBLISHED-POLARIZATION-FORCE-FIXTURE",
        parameters=parameters,
        coordinate_unit_to_bohr=1.0,
        stationarity_absolute_tolerance=STATIONARITY_ABSOLUTE_TOLERANCE,
    )


def _configuration(species=SPECIES, positions=POSITIONS_BOHR, *, periodic=False):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(value) for value in point) for point in positions),
        cell=((20.0, 0.0, 0.0), (0.0, 20.0, 0.0), (0.0, 0.0, 20.0)) if periodic else None,
        periodic=(periodic, periodic, periodic),
    ))


def _lif(distance=4.0):
    return _configuration(("Li", "F"), ((0.0, 0.0, 0.0), (distance, 0.0, 0.0)))


def _bef2(distance=4.0):
    return _configuration(
        ("Be", "F", "F"),
        ((0.0, 0.0, 0.0), (distance, 0.0, 0.0), (-distance, 0.0, 0.0)),
    )


def _perturbed(configuration, atom, axis, offset):
    positions = [list(point) for point in configuration.configuration.positions]
    positions[atom][axis] += offset
    return _configuration(configuration.configuration.species, positions)


def _finite_difference_force(model, configuration, atom, axis, *, polarization_only=False):
    """Reoptimize dipoles at each displaced geometry; differentiate energy only."""
    plus = model.evaluate(_perturbed(configuration, atom, axis, DIFFERENCE_STEP))
    minus = model.evaluate(_perturbed(configuration, atom, axis, -DIFFERENCE_STEP))
    quantity = "polarization_energy_hartree" if polarization_only else "total_energy_hartree"
    return -(getattr(plus, quantity) - getattr(minus, quantity)) / (2 * DIFFERENCE_STEP)


def _assert_forces(actual, expected, tol=FORCE_ABSOLUTE_TOLERANCE):
    assert len(actual) == len(expected)
    for first, second in zip(actual, expected, strict=True):
        assert first == pytest.approx(second, rel=0.0, abs=tol)


def test_lif_damped_polarization_force_has_independent_closed_form(model):
    """Derive F from U_pol(r)=-alpha_F*g(r)^2/(2*r^4), with relaxed mu."""
    alpha, beta, c = 7.09, 1.81, 1.40
    for r in (4.0, 6.0):
        z = beta * r
        g = 1.0 - c * exp(-z) * fsum(z**k / factorial(k) for k in range(5))
        dg_dr = c * beta * exp(-z) * z**4 / factorial(4)
        energy = -alpha * g**2 / (2.0 * r**4)
        radial_force_on_f = alpha * (g * dg_dr / r**4 - 2.0 * g**2 / r**5)
        result = evaluate_flibe_finite_cluster_polarization_forces(model, _lif(r))
        assert result.polarization_result.polarization_energy_hartree == pytest.approx(
            energy, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE
        )
        _assert_forces(result.polarization_forces.forces, (
            (-radial_force_on_f, 0.0, 0.0),
            (radial_force_on_f, 0.0, 0.0),
        ), tol=1.0e-11)
        assert result.total_energy_hartree == result.polarization_result.total_energy_hartree


@pytest.mark.parametrize("configuration_factory", (_lif, _bef2, _configuration))
def test_total_force_matches_full_reoptimized_energy_gradient(model, configuration_factory):
    configuration = configuration_factory()
    result = evaluate_flibe_finite_cluster_polarization_forces(model, configuration)
    for atom in range(configuration.atom_count):
        for axis in range(3):
            numerical = _finite_difference_force(model, configuration, atom, axis)
            assert result.total_forces.forces[atom][axis] == pytest.approx(
                numerical, rel=0.0, abs=FORCE_ABSOLUTE_TOLERANCE
            )
    assert result.polarization_result.max_stationarity_residual_atomic <= (
        STATIONARITY_ABSOLUTE_TOLERANCE
    )


def test_polarization_force_matches_derivative_of_relaxed_polarization_energy(model):
    configuration = _configuration()
    result = evaluate_flibe_finite_cluster_polarization_forces(model, configuration)
    for atom in range(configuration.atom_count):
        for axis in range(3):
            numerical = _finite_difference_force(
                model, configuration, atom, axis, polarization_only=True
            )
            assert result.polarization_forces.forces[atom][axis] == pytest.approx(
                numerical, rel=0.0, abs=FORCE_ABSOLUTE_TOLERANCE
            )


def test_force_decomposition_preserves_source_pair_and_polarization_channels(model, parameters):
    result = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    source_pair = parameters.build_finite_cluster_model(
        model_id="INDEPENDENT-SOURCE-PAIR", coordinate_unit_to_bohr=1.0
    ).evaluate(_configuration())
    assert result.polarization_result.pair_result.energy == source_pair.energy
    assert result.polarization_result.pair_result.forces == source_pair.forces
    assert any(abs(value) > 1e-8 for row in result.polarization_forces.forces for value in row)
    for i in range(result.configuration.atom_count):
        for axis in range(3):
            assert result.total_forces.forces[i][axis] == pytest.approx(
                source_pair.forces.forces[i][axis] + result.polarization_forces.forces[i][axis],
                rel=0.0, abs=1e-12,
            )
    assert result.total_energy_hartree == pytest.approx(
        source_pair.energy.total_energy + result.polarization_result.polarization_energy_hartree,
        rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE,
    )


def test_all_force_channels_obey_translation_balance(model):
    result = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    for forces in (
        result.polarization_result.pair_result.forces.forces,
        result.polarization_forces.forces,
        result.total_forces.forces,
    ):
        for axis in range(3):
            assert abs(fsum(row[axis] for row in forces)) <= 1e-10


def test_e3_rotation_translation_and_reflection_covariance(model):
    base = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    actions = (
        (lambda p: (-p[1] + 2.0, p[0] - 3.0, p[2] + 1.25),
         lambda v: (-v[1], v[0], v[2])),
        (lambda p: (-p[0] + 1.0, p[1] + 2.0, p[2] - 0.75),
         lambda v: (-v[0], v[1], v[2])),
    )
    for transform, linear in actions:
        changed = _configuration(positions=tuple(transform(p) for p in POSITIONS_BOHR))
        observed = evaluate_flibe_finite_cluster_polarization_forces(model, changed)
        assert observed.total_energy_hartree == pytest.approx(
            base.total_energy_hartree, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE,
        )
        _assert_forces(
            observed.polarization_forces.forces,
            tuple(linear(row) for row in base.polarization_forces.forces),
            tol=SYMMETRY_ABSOLUTE_TOLERANCE,
        )
        _assert_forces(
            observed.total_forces.forces,
            tuple(linear(row) for row in base.total_forces.forces),
            tol=SYMMETRY_ABSOLUTE_TOLERANCE,
        )


def test_species_and_position_permutation_preserves_energy_and_force_order(model):
    order = (6, 2, 0, 4, 1, 5, 3)
    base = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    changed = _configuration(
        species=tuple(SPECIES[i] for i in order),
        positions=tuple(POSITIONS_BOHR[i] for i in order),
    )
    observed = evaluate_flibe_finite_cluster_polarization_forces(model, changed)
    assert observed.total_energy_hartree == pytest.approx(
        base.total_energy_hartree, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE
    )
    _assert_forces(observed.total_forces.forces,
                   tuple(base.total_forces.forces[i] for i in order),
                   tol=SYMMETRY_ABSOLUTE_TOLERANCE)
    _assert_forces(observed.polarization_forces.forces,
                   tuple(base.polarization_forces.forces[i] for i in order),
                   tol=SYMMETRY_ABSOLUTE_TOLERANCE)


def test_coordinate_conversion_changes_force_units_by_chain_rule(model):
    base = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    scaled_model = replace(model, coordinate_unit_to_bohr=0.5)
    scaled = evaluate_flibe_finite_cluster_polarization_forces(
        scaled_model, _configuration(positions=tuple(
            tuple(2.0 * component for component in point) for point in POSITIONS_BOHR
        ))
    )
    assert scaled.total_energy_hartree == pytest.approx(
        base.total_energy_hartree, rel=0.0, abs=ENERGY_ABSOLUTE_TOLERANCE
    )
    _assert_forces(scaled.total_forces.forces,
                   tuple(tuple(0.5 * x for x in row) for row in base.total_forces.forces),
                   tol=SYMMETRY_ABSOLUTE_TOLERANCE)
    _assert_forces(scaled.polarization_forces.forces,
                   tuple(tuple(0.5 * x for x in row) for row in base.polarization_forces.forces),
                   tol=SYMMETRY_ABSOLUTE_TOLERANCE)


def test_publication_provenance_source_digest_and_repeatability(model):
    first = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    second = evaluate_flibe_finite_cluster_polarization_forces(model, _configuration())
    assert first == second
    assert first.functional_id == FORCE_FUNCTIONAL_ID
    assert first.configuration.composition().formula_unit_fractions == (2/3, 1/3)
    assert first.polarization_result.source_doi == SOURCE_DOI
    assert first.polarization_result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert all(pair.provenance is ParameterProvenance.PRIMARY_SOURCE
               for pair in first.polarization_result.pair_result.pair_coefficients)
    with pytest.raises(FrozenInstanceError):
        first.functional_id = "CHANGED"  # type: ignore[misc]


def test_constructor_enforces_typed_force_components_and_cardinality(model):
    result = evaluate_flibe_finite_cluster_polarization_forces(model, _lif())
    with pytest.raises(ValueError, match="force functional identity"):
        replace(result, functional_id="OTHER")
    with pytest.raises(TypeError, match="polarization_forces must be ForceState"):
        replace(result, polarization_forces=None)
    with pytest.raises(TypeError, match="total_forces must be ForceState"):
        replace(result, total_forces=None)
    with pytest.raises(ValueError, match="force cardinality"):
        replace(result, total_forces=ForceState(((0.0, 0.0, 0.0),)))
    changed = list(result.total_forces.forces)
    changed[1] = (changed[1][0] + 0.01, changed[1][1], changed[1][2])
    with pytest.raises(ValueError, match="total forces must sum"):
        replace(result, total_forces=ForceState(tuple(changed)))
    with pytest.raises(TypeError, match="polarization_result must be"):
        replace(result, polarization_result=None)


@pytest.mark.parametrize("model_input,configuration_input,error", (
    (None, _lif(), TypeError),
    ("MODEL", _lif(), TypeError),
    ("actual", None, TypeError),
    ("actual", "CONFIG", TypeError),
))
def test_evaluator_rejects_untyped_arguments(model, model_input, configuration_input, error):
    selected = model if model_input == "actual" else model_input
    with pytest.raises(error):
        evaluate_flibe_finite_cluster_polarization_forces(selected, configuration_input)


def test_finite_cluster_boundaries_and_unstable_hessian_are_enforced(model):
    with pytest.raises(ValueError, match="nonperiodic"):
        evaluate_flibe_finite_cluster_polarization_forces(model, _configuration(periodic=True))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        evaluate_flibe_finite_cluster_polarization_forces(
            model, _configuration(("Li", "F", "F"), ((0.,0.,0.),(4.,0.,0.),(-4.,0.,0.)))
        )
    with pytest.raises(ValueError, match="positive separation"):
        evaluate_flibe_finite_cluster_polarization_forces(model, _lif(0.0))
    with pytest.raises(ValueError, match="positive definite"):
        evaluate_flibe_finite_cluster_polarization_forces(model, _bef2(0.25))
