"""Independent Ewald fluoride polarization, stationarity, and symmetry tests."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from itertools import product
from math import cos, erfc, exp, factorial, fsum, pi, sin, sqrt
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.finite_cluster_polarization import FLiBeFiniteClusterPolarizationModel
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_polarization import (
    POLARIZATION_FUNCTIONAL_ID,
    FLiBePeriodicPolarizationModel,
    FLiBePeriodicPolarizationResult,
)
from tr_eif.flibe.registered_pair_coefficients import SOURCE_DOI, load_flibe_registered_pair_parameters
from tr_eif.flibe.units import ParameterProvenance


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
CELL = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
CHARGES = {"Li": 1, "Be": 2, "F": -1}
ALPHA_F = 7.09
DAMPING = {"Li": (1.81, 1.40), "Be": (1.78, 0.99)}
SOLUTION_TOL = 2.0e-10
ENERGY_TOL = 2.0e-10
VECTOR_TOL = 2.0e-9


def _configuration(species=SPECIES, positions=POSITIONS, cell=CELL, periodic=(True, True, True)):
    return FLiBeConfiguration(AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(value) for value in point) for point in positions),
        cell=None if cell is None else tuple(tuple(float(value) for value in edge) for edge in cell),
        periodic=periodic,
    ))


def _lif(cell_length=18.0, distance=4.0):
    return _configuration(
        species=("Li", "F"),
        positions=((0.0, 0.0, 0.0), (distance, 0.0, 0.0)),
        cell=((cell_length, 0.0, 0.0), (0.0, cell_length, 0.0), (0.0, 0.0, cell_length)),
    )


def _ewald(alpha=0.25, real_shell=3, reciprocal_shell=7, length_factor=1.0):
    return FLiBeEwaldParameters(
        alpha_inverse_bohr=alpha,
        real_image_shell=real_shell,
        reciprocal_image_shell=reciprocal_shell,
        coordinate_unit_to_bohr=length_factor,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="EWALD-POLARIZATION-INDEPENDENT-FIXTURE",
    )


def _model(*, parameters=None, ewald=None, damping_shell=1, stationarity=1.0e-10):
    return FLiBePeriodicPolarizationModel(
        model_id="FLIBE-PERIODIC-POLARIZATION-FIXTURE",
        parameters=load_flibe_registered_pair_parameters(SOURCE) if parameters is None else parameters,
        ewald_parameters=_ewald() if ewald is None else ewald,
        damping_image_shell=damping_shell,
        stationarity_absolute_tolerance=stationarity,
    )


def _dot(a, b):
    return fsum(x*y for x, y in zip(a, b, strict=True))


def _cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def _shifts(cell, shell):
    return tuple(tuple(fsum(index[j]*cell[j][axis] for j in range(3)) for axis in range(3))
                 for index in product(range(-shell, shell + 1), repeat=3))


def _independent_damping_field(configuration, damping_shell):
    """Direct table-driven (g-1) charge-field correction, separate from Ewald."""
    positions = configuration.configuration.positions
    species = configuration.configuration.species
    shifts = _shifts(configuration.configuration.cell, damping_shell)
    field = {}
    for i, ion in enumerate(species):
        if ion != "F":
            continue
        row = [0.0, 0.0, 0.0]
        for j, source in enumerate(species):
            if source not in DAMPING:
                continue
            beta, amplitude = DAMPING[source]
            for shift in shifts:
                delta = tuple(positions[i][axis] - positions[j][axis] + shift[axis]
                              for axis in range(3))
                distance = sqrt(_dot(delta, delta))
                z = beta*distance
                damping_adjustment = -amplitude*exp(-z)*fsum(
                    z**k / factorial(k) for k in range(5)
                )
                factor = CHARGES[source]*damping_adjustment / distance**3
                for axis in range(3):
                    row[axis] += factor*delta[axis]
        field[i] = tuple(row)
    return field


def _independent_ewald_hessian(configuration, ewald):
    """Construct the periodic dipole Hessian from differentiated Green sums."""
    atom_positions = configuration.configuration.positions
    cell = configuration.configuration.cell
    sites = tuple(i for i, symbol in enumerate(configuration.configuration.species) if symbol == "F")
    volume_signed = _dot(cell[0], _cross(cell[1], cell[2]))
    reciprocal_basis = tuple(tuple(2.0*pi*x/volume_signed for x in normal) for normal in
        (_cross(cell[1], cell[2]), _cross(cell[2], cell[0]), _cross(cell[0], cell[1])))
    real_shifts = _shifts(cell, ewald.real_image_shell)
    waves = _shifts(reciprocal_basis, ewald.reciprocal_image_shell)
    alpha = ewald.alpha_inverse_bohr
    dimension = 3*len(sites)
    matrix = [[0.0]*dimension for _ in range(dimension)]
    for local_i, i in enumerate(sites):
        for local_j, j in enumerate(sites):
            delta = tuple(atom_positions[i][axis] - atom_positions[j][axis] for axis in range(3))
            for shift in real_shifts:
                if i == j and shift == (0.0, 0.0, 0.0):
                    continue
                dr = tuple(delta[axis] + shift[axis] for axis in range(3))
                r2 = _dot(dr, dr)
                r = sqrt(r2)
                tail = erfc(alpha*r)
                gaussian = 2.0*alpha*exp(-alpha*alpha*r2)/sqrt(pi)
                radial = 3.0*tail/r**5 + gaussian*(3.0/r**4 + 2.0*alpha*alpha/r2)
                diagonal = tail/r**3 + gaussian/r2
                for a in range(3):
                    for b in range(3):
                        matrix[3*local_i+a][3*local_j+b] += (
                            radial*dr[a]*dr[b] - (diagonal if a == b else 0.0)
                        )
            for wave in waves:
                k2 = _dot(wave, wave)
                if k2 == 0.0:
                    continue
                amplitude = -4.0*pi/abs(volume_signed)*exp(-k2/(4.0*alpha**2)) / k2
                amplitude *= cos(_dot(wave, delta))
                for a in range(3):
                    for b in range(3):
                        matrix[3*local_i+a][3*local_j+b] += amplitude*wave[a]*wave[b]
            if local_i == local_j:
                for axis in range(3):
                    matrix[3*local_i+axis][3*local_j+axis] += 4.0*alpha**3/(3.0*sqrt(pi))
    return sites, matrix


def _independent_gaussian_solve(matrix, rhs):
    """Partial-pivot elimination independent of the implementation's Cholesky."""
    n = len(rhs)
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for j in range(n):
        pivot = max(range(j, n), key=lambda row: abs(augmented[row][j]))
        assert abs(augmented[pivot][j]) > 1.0e-12
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        for i in range(j+1, n):
            scale = augmented[i][j]/augmented[j][j]
            for k in range(j, n+1):
                augmented[i][k] -= scale*augmented[j][k]
    answer = [0.0]*n
    for i in range(n-1, -1, -1):
        answer[i] = (augmented[i][n] - fsum(augmented[i][j]*answer[j]
                                                  for j in range(i+1, n)))/augmented[i][i]
    return tuple(answer)


def _independent_solution(configuration, ewald, damping_shell):
    """Use separate Ewald forces, source damping, and a Gaussian dipole solve."""
    charges = tuple(CHARGES[s] for s in configuration.configuration.species)
    coulomb = FLiBePeriodicEwaldModel("ELECTRIC-FIELD-FIXTURE", ewald).evaluate(configuration)
    correction = _independent_damping_field(configuration, damping_shell)
    fluoride, tensor = _independent_ewald_hessian(configuration, ewald)
    field = tuple(tuple(coulomb.forces.forces[i][axis]/charges[i] + correction[i][axis]
                        for axis in range(3)) for i in fluoride)
    rhs = tuple(value for vector in field for value in vector)
    matrix = [[(1.0/ALPHA_F if i == j else 0.0) - tensor[i][j]
               for j in range(len(rhs))] for i in range(len(rhs))]
    dipoles = _independent_gaussian_solve(matrix, rhs)
    polarization = -0.5*fsum(dipoles[i]*rhs[i] for i in range(len(rhs)))
    return fluoride, field, matrix, rhs, dipoles, polarization


def _assert_vectors(actual, expected, tolerance=VECTOR_TOL):
    assert len(actual) == len(expected)
    for found, reference in zip(actual, expected, strict=True):
        assert found == pytest.approx(reference, rel=0.0, abs=tolerance)


def test_source_provenance_and_only_fluoride_sites_are_polarizable():
    result = _model().evaluate(_configuration())
    assert isinstance(result, FLiBePeriodicPolarizationResult)
    assert result.functional_id == POLARIZATION_FUNCTIONAL_ID
    assert result.source_doi == SOURCE_DOI
    assert result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert result.polarizable_indices == (3, 4, 5, 6)
    assert result.induced_dipoles_e_bohr[:3] == ((0.0, 0.0, 0.0),)*3
    assert result.charge_fields_atomic[:3] == ((0.0, 0.0, 0.0),)*3
    assert result.ewald_parameters.provenance is ParameterProvenance.TEST_FIXTURE


def test_seven_atom_field_hessian_and_dipoles_match_independent_solver():
    config = _configuration()
    model = _model()
    result = model.evaluate(config)
    sites, field, matrix, rhs, dipoles, energy = _independent_solution(
        config, model.ewald_parameters, model.damping_image_shell
    )
    assert sites == result.polarizable_indices
    _assert_vectors(tuple(result.charge_fields_atomic[i] for i in sites), field, 2e-11)
    _assert_vectors(tuple(result.induced_dipoles_e_bohr[i] for i in sites),
                    tuple(tuple(dipoles[3*j+a] for a in range(3)) for j in range(len(sites))),
                    2e-10)
    assert result.polarization_energy_hartree == pytest.approx(energy, abs=ENERGY_TOL)
    residual = max(abs(fsum(matrix[i][j]*dipoles[j] for j in range(len(rhs))) - rhs[i])
                   for i in range(len(rhs)))
    assert residual < SOLUTION_TOL
    assert result.max_stationarity_residual_atomic < SOLUTION_TOL


def test_lif_one_fluoride_reference_and_cubic_symmetry():
    config = _lif()
    model = _model(ewald=_ewald(alpha=0.25, real_shell=3, reciprocal_shell=6))
    result = model.evaluate(config)
    _, field, matrix, rhs, dipoles, energy = _independent_solution(
        config, model.ewald_parameters, model.damping_image_shell
    )
    assert result.polarizable_indices == (1,)
    assert result.charge_fields_atomic[1] == pytest.approx(field[0], abs=2e-12)
    assert result.induced_dipoles_e_bohr[1] == pytest.approx(dipoles, abs=2e-12)
    assert abs(result.induced_dipoles_e_bohr[1][1]) < 1e-13
    assert abs(result.induced_dipoles_e_bohr[1][2]) < 1e-13
    assert result.polarization_energy_hartree == pytest.approx(energy, abs=2e-12)
    assert result.polarization_energy_hartree == pytest.approx(-0.007500445501050205, abs=2e-11)
    assert matrix[0][0] > 0.0 and rhs[0] > 0.0


def test_stationary_quadratic_functional_is_minimized():
    model = _model()
    result = model.evaluate(_configuration())
    _, _, matrix, rhs, dipoles, energy = _independent_solution(
        result.configuration, model.ewald_parameters, model.damping_image_shell
    )
    shifted = list(dipoles)
    step = 0.01
    shifted[0] += step

    def quadratic(values):
        return 0.5*fsum(values[i]*matrix[i][j]*values[j] for i in range(len(rhs))
                        for j in range(len(rhs))) - fsum(values[i]*rhs[i]
                                                           for i in range(len(rhs)))

    assert quadratic(dipoles) == pytest.approx(energy, abs=2e-11)
    assert quadratic(shifted) - quadratic(dipoles) == pytest.approx(
        0.5*step*step*matrix[0][0], rel=0.0, abs=1e-12
    )
    assert result.polarization_energy_hartree == pytest.approx(energy, abs=ENERGY_TOL)


def test_ewald_field_and_short_range_damping_are_separately_accounted():
    config = _configuration()
    model = _model()
    polarization = model.evaluate(config)
    ewald = FLiBePeriodicEwaldModel("CHARGE-FIELD-TEST", model.ewald_parameters).evaluate(config)
    correction = _independent_damping_field(config, model.damping_image_shell)
    for i in polarization.polarizable_indices:
        expected = tuple(-ewald.forces.forces[i][axis] + correction[i][axis]
                         for axis in range(3))
        assert polarization.charge_fields_atomic[i] == pytest.approx(expected, abs=2e-11)
    assert polarization.polarization_energy_hartree == pytest.approx(
        0.5*polarization.charge_dipole_energy_hartree, abs=2e-11
    )
    assert polarization.polarization_energy_hartree == pytest.approx(fsum((
        polarization.self_energy_hartree, polarization.charge_dipole_energy_hartree,
        polarization.dipole_dipole_energy_hartree,
    )), abs=2e-11)


def test_alpha_splitting_convergence_with_predeclared_lattice_shells():
    config = _configuration()
    energies = []
    for alpha in (0.20, 0.25, 0.30):
        model = _model(ewald=_ewald(alpha=alpha, real_shell=3, reciprocal_shell=7))
        energies.append(model.evaluate(config).polarization_energy_hartree)
    assert abs(energies[0] - energies[1]) < 1.0e-9
    assert abs(energies[1] - energies[2]) < 1.0e-9


def test_explicit_shell_refinement_reduces_energy_difference():
    config = _configuration()
    values = tuple(_model(ewald=_ewald(real_shell=r, reciprocal_shell=k))
                   .evaluate(config).polarization_energy_hartree
                   for r, k in ((1, 3), (2, 5), (3, 7)))
    assert abs(values[2] - values[1]) < abs(values[1] - values[0])
    assert abs(values[2] - values[1]) < 1e-8


def test_periodic_cell_translation_and_e3_symmetries():
    model = _model(damping_shell=2)
    baseline = model.evaluate(_configuration())
    translate = list(POSITIONS)
    translate[3] = tuple(POSITIONS[3][axis] + CELL[1][axis] for axis in range(3))
    moved = model.evaluate(_configuration(positions=tuple(translate)))
    assert moved.polarization_energy_hartree == pytest.approx(
        baseline.polarization_energy_hartree, rel=0.0, abs=1e-9
    )
    _assert_vectors(moved.induced_dipoles_e_bohr, baseline.induced_dipoles_e_bohr, 1e-8)
    operations = (
        (lambda v: (-v[1], v[0], v[2]), (2.0, -1.0, 3.0)),
        (lambda v: (-v[0], v[1], v[2]), (4.0, 2.0, -0.5)),
    )
    for rotation, shift in operations:
        rotated = model.evaluate(_configuration(
            positions=tuple(tuple(rotation(p)[axis] + shift[axis] for axis in range(3))
                            for p in POSITIONS),
            cell=tuple(rotation(edge) for edge in CELL),
        ))
        assert rotated.polarization_energy_hartree == pytest.approx(
            baseline.polarization_energy_hartree, abs=ENERGY_TOL
        )
        _assert_vectors(rotated.induced_dipoles_e_bohr,
                        tuple(rotation(v) for v in baseline.induced_dipoles_e_bohr), 1e-9)
        _assert_vectors(rotated.charge_fields_atomic,
                        tuple(rotation(v) for v in baseline.charge_fields_atomic), 1e-9)


def test_atom_permutation_covariance():
    model = _model()
    baseline = model.evaluate(_configuration())
    indices = (6, 2, 0, 4, 1, 5, 3)
    changed = model.evaluate(_configuration(
        species=tuple(SPECIES[i] for i in indices),
        positions=tuple(POSITIONS[i] for i in indices),
    ))
    assert changed.polarization_energy_hartree == pytest.approx(
        baseline.polarization_energy_hartree, abs=ENERGY_TOL
    )
    _assert_vectors(changed.induced_dipoles_e_bohr,
                    tuple(baseline.induced_dipoles_e_bohr[i] for i in indices), 1e-9)
    assert changed.polarizable_indices == (0, 3, 5, 6)


def test_coordinate_unit_rescaling_preserves_energy_and_dipoles():
    reference = _model().evaluate(_configuration())
    scaled = _model(ewald=_ewald(length_factor=0.5)).evaluate(_configuration(
        positions=tuple(tuple(2.0*x for x in point) for point in POSITIONS),
        cell=tuple(tuple(2.0*x for x in edge) for edge in CELL),
    ))
    assert scaled.polarization_energy_hartree == pytest.approx(
        reference.polarization_energy_hartree, abs=ENERGY_TOL
    )
    _assert_vectors(scaled.induced_dipoles_e_bohr, reference.induced_dipoles_e_bohr, 1e-9)


def test_large_cell_approaches_nonperiodic_single_fluoride_response():
    source = load_flibe_registered_pair_parameters(SOURCE)
    isolated = FLiBeFiniteClusterPolarizationModel(
        model_id="ISOLATED-LIF", parameters=source,
        coordinate_unit_to_bohr=1.0, stationarity_absolute_tolerance=1e-10,
    ).evaluate(_configuration(species=("Li", "F"),
                              positions=((0.0, 0.0, 0.0), (4.0, 0.0, 0.0)),
                              cell=None, periodic=(False, False, False)))

    def periodic(length, alpha):
        return _model(ewald=_ewald(alpha=alpha, real_shell=3, reciprocal_shell=8)) \
            .evaluate(_lif(cell_length=length)).polarization_energy_hartree

    first = periodic(40.0, 0.10)
    second = periodic(80.0, 0.07)
    assert abs(second - isolated.polarization_energy_hartree) < abs(
        first - isolated.polarization_energy_hartree
    )
    assert abs(second - isolated.polarization_energy_hartree) < 2e-5


def test_published_pair_amplitudes_do_not_enter_polarization_energy():
    source = load_flibe_registered_pair_parameters(SOURCE)
    original = _model(parameters=source).evaluate(_configuration())
    modified_pair = replace(source.pair_coefficients[2], born_amplitude_hartree=25.42)
    edited = replace(source, pair_coefficients=(*source.pair_coefficients[:2],
                                               modified_pair, *source.pair_coefficients[3:]))
    changed = _model(parameters=edited).evaluate(_configuration())
    assert changed.polarization_energy_hartree == original.polarization_energy_hartree
    assert changed.induced_dipoles_e_bohr == original.induced_dipoles_e_bohr


def test_negative_ill_conditioned_hessian_is_rejected():
    dense = _configuration(
        species=("Li", "Li", "Be", "F", "F", "F", "F"),
        positions=((0., 0., 0.), (0.8, 0., 0.), (0.5, 0.7, 0.),
                   (0.1, 0.2, 0.5), (0.6, 0.4, 0.5),
                   (0.2, 0.8, 0.9), (0.7, 0.7, 0.9)),
    )
    with pytest.raises(ValueError, match="positive definite"):
        _model().evaluate(dense)


def test_rejects_nonperiodic_and_invalid_configuration():
    with pytest.raises(TypeError, match="FLiBeConfiguration"):
        _model().evaluate(None)
    with pytest.raises(ValueError, match="three periodic axes"):
        _model().evaluate(_configuration(periodic=(True, False, True)))
    with pytest.raises(ValueError, match="three periodic axes"):
        _model().evaluate(_configuration(periodic=(False, False, False), cell=None))
    with pytest.raises(ValueError, match="fluorine stoichiometry"):
        _model().evaluate(_configuration(species=("Li", "Be", "F"), positions=POSITIONS[:3]))
    with pytest.raises(ValueError, match="separation"):
        _model().evaluate(_lif(distance=0.0))


@pytest.mark.parametrize("field,invalid,error", (
    ("model_id", " ", ValueError),
    ("parameters", None, TypeError),
    ("ewald_parameters", None, TypeError),
    ("damping_image_shell", -1, ValueError),
    ("damping_image_shell", True, ValueError),
    ("damping_image_shell", 0.5, ValueError),
    ("stationarity_absolute_tolerance", 0.0, ValueError),
    ("stationarity_absolute_tolerance", float("nan"), ValueError),
    ("stationarity_absolute_tolerance", False, ValueError),
))
def test_model_rejects_invalid_parameters(field, invalid, error):
    with pytest.raises(error):
        replace(_model(), **{field: invalid})


def test_result_rejects_broken_polarization_contracts():
    result = _model().evaluate(_configuration())
    with pytest.raises(ValueError, match="functional identity"):
        replace(result, functional_id="OTHER")
    with pytest.raises(ValueError, match="SHA-256"):
        replace(result, source_file_sha256="broken")
    with pytest.raises(ValueError, match="polarizable_indices"):
        replace(result, polarizable_indices=(2, 3, 4, 5))
    with pytest.raises(ValueError, match="three components"):
        replace(result, self_energy_hartree=result.self_energy_hartree + 0.1)
    with pytest.raises(ValueError, match="nonnegative"):
        replace(result, max_stationarity_residual_atomic=-1.0)
    with pytest.raises(ValueError, match="only fluoride"):
        replace(result, induced_dipoles_e_bohr=((1.0, 0.0, 0.0),
                *result.induced_dipoles_e_bohr[1:]))
    with pytest.raises(FrozenInstanceError):
        result.model_id = "CHANGED"  # type: ignore[misc]


def test_deterministic_replay_retains_source_and_order():
    model = _model()
    first = model.evaluate(_configuration())
    assert first == model.evaluate(_configuration())
    assert first.charge_fields_atomic == model.evaluate(_configuration()).charge_fields_atomic
