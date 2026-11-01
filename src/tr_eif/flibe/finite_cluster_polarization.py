"""Stationary fluoride polarization for the registered FLiBe finite-cluster PIM.

The induced-dipole functional is evaluated in atomic units:

    U(mu) = sum_i |mu_i|^2/(2 alpha_F) - sum_i mu_i.E_i^q
            - sum_{i<j} mu_i.D_ij.mu_j,

where i and j in the dipole terms index fluoride ions, E_i^q is the
charge field with registered cation-fluoride damping, and D_ij is the
vacuum dipole-dipole tensor. The stationary state solves A mu = E^q.
The source pair functional and polarization functional retain distinct
energy components and provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, fsum, isclose, isfinite, sqrt

from .charge import configuration_formal_charges
from .configuration import FLiBeConfiguration
from .independent_pair_potential import FLiBePairPotentialResult
from .registered_pair_coefficients import FLiBeRegisteredPairParameters
from .species import FLiBeSpecies


Vector3 = tuple[float, float, float]
POLARIZATION_FUNCTIONAL_ID = "flibe.finite_cluster.stationary_fluoride_polarization.v1"


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return result


def _name(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be a nonempty trimmed string.")
    return value


def _dot(a: Vector3, b: Vector3) -> float:
    return fsum(a[k] * b[k] for k in range(3))


def _displacement(a: Vector3, b: Vector3) -> Vector3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _damping(z: float, c: float) -> float:
    """Source charge-dipole damping 1-c*exp(-z)*sum(z**k/k!, k=0..4)."""
    if not isfinite(z) or z <= 0.0:
        raise ValueError("charge-dipole damping argument must be finite and positive.")
    if z >= 100.0:
        return 1.0
    polynomial = 1.0 + z * (1.0 + z * (0.5 + z * (1.0 / 6.0 + z / 24.0)))
    result = 1.0 - c * exp(-z) * polynomial
    if not isfinite(result):
        raise ValueError("charge-dipole damping must be finite.")
    return result


def _solve_positive_definite(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Cholesky factorization of the symmetric polarization Hessian."""
    n = len(rhs)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = matrix[i][j] - fsum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if not isfinite(value) or value <= 0.0:
                    raise ValueError("polarization Hessian must be positive definite.")
                lower[i][j] = sqrt(value)
            else:
                lower[i][j] = value / lower[j][j]
                if not isfinite(lower[i][j]):
                    raise ValueError("polarization factorization must remain finite.")
    y = [0.0] * n
    for i in range(n):
        y[i] = (rhs[i] - fsum(lower[i][j] * y[j] for j in range(i))) / lower[i][i]
    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = (y[i] - fsum(lower[j][i] * solution[j] for j in range(i + 1, n))) / lower[i][i]
    if any(not isfinite(value) for value in solution):
        raise ValueError("stationary dipoles must be finite.")
    return solution


@dataclass(frozen=True, slots=True)
class FLiBeFiniteClusterPolarizationResult:
    """Source-resolved pair energy and stationary fluoride-dipole energy."""

    configuration: FLiBeConfiguration
    pair_result: FLiBePairPotentialResult
    model_id: str
    functional_id: str
    source_doi: str
    source_file_sha256: str
    polarizable_indices: tuple[int, ...]
    induced_dipoles_e_bohr: tuple[Vector3, ...]
    charge_fields_atomic: tuple[Vector3, ...]
    self_energy_hartree: float
    charge_dipole_energy_hartree: float
    dipole_dipole_energy_hartree: float
    polarization_energy_hartree: float
    total_energy_hartree: float
    max_stationarity_residual_atomic: float

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        if not isinstance(self.pair_result, FLiBePairPotentialResult):
            raise TypeError("pair_result must be FLiBePairPotentialResult.")
        if self.pair_result.configuration != self.configuration:
            raise ValueError("pair result must use the same atomic configuration.")
        _name(self.model_id, "model_id")
        if self.functional_id != POLARIZATION_FUNCTIONAL_ID:
            raise ValueError("polarization functional identifier differs.")
        _name(self.source_doi, "source_doi")
        if not isinstance(self.source_file_sha256, str) or len(self.source_file_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_file_sha256
        ):
            raise ValueError("source_file_sha256 must be a lowercase SHA-256 digest.")
        if len(self.induced_dipoles_e_bohr) != self.configuration.atom_count or len(
            self.charge_fields_atomic
        ) != self.configuration.atom_count:
            raise ValueError("dipole and charge-field arrays must follow atomic cardinality.")
        expected = tuple(i for i, species in enumerate(self.configuration.species)
                         if species is FLiBeSpecies.FLUORINE)
        if self.polarizable_indices != expected:
            raise ValueError("polarizable indices must select fluoride ions in atom order.")
        if any(not isinstance(v, tuple) or len(v) != 3 or any(not isfinite(x) for x in v)
               for v in (*self.induced_dipoles_e_bohr, *self.charge_fields_atomic)):
            raise ValueError("dipoles and charge fields must be finite Cartesian vectors.")
        if any(self.induced_dipoles_e_bohr[i] != (0.0, 0.0, 0.0)
               for i in range(self.configuration.atom_count) if i not in expected):
            raise ValueError("only fluoride positions carry induced dipoles.")
        for name in (
            "self_energy_hartree", "charge_dipole_energy_hartree",
            "dipole_dipole_energy_hartree", "polarization_energy_hartree",
            "total_energy_hartree", "max_stationarity_residual_atomic",
        ):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
                raise ValueError(f"{name} must be finite.")
        if self.max_stationarity_residual_atomic < 0.0:
            raise ValueError("stationarity residual must be nonnegative.")
        components = fsum((
            self.self_energy_hartree,
            self.charge_dipole_energy_hartree,
            self.dipole_dipole_energy_hartree,
        ))
        if not isclose(self.polarization_energy_hartree, components,
                       rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("polarization components must sum to polarization energy.")
        combined = fsum((self.pair_result.energy.total_energy,
                         self.polarization_energy_hartree))
        if not isclose(self.total_energy_hartree, combined,
                       rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("pair and polarization energies must sum to total energy.")


@dataclass(frozen=True, slots=True)
class FLiBeFiniteClusterPolarizationModel:
    """Published-parameter stationary induced-dipole energy on a finite cluster."""

    model_id: str
    parameters: FLiBeRegisteredPairParameters
    coordinate_unit_to_bohr: float
    stationarity_absolute_tolerance: float

    def __post_init__(self) -> None:
        _name(self.model_id, "model_id")
        if not isinstance(self.parameters, FLiBeRegisteredPairParameters):
            raise TypeError("parameters must be FLiBeRegisteredPairParameters.")
        _positive(self.coordinate_unit_to_bohr, "coordinate_unit_to_bohr")
        _positive(self.stationarity_absolute_tolerance, "stationarity_absolute_tolerance")

    def evaluate(self, configuration: FLiBeConfiguration) -> FLiBeFiniteClusterPolarizationResult:
        """Solve fluoride dipoles and combine stationary and source-pair energies.

        Ion charges use the existing FLiBe formal-charge contract. Cation-to-F
        charge fields use the source's g_FBe and g_FLi damping functions.
        The dipole-dipole tensor uses its vacuum r^-3 interaction. A symmetric
        positive-definite Hessian defines the stationary minimum on the selected
        geometry; the residual is checked against the declared tolerance.
        """
        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        if any(configuration.configuration.periodic):
            raise ValueError("finite-cluster polarization requires nonperiodic axes.")
        configuration.composition()
        factor = self.coordinate_unit_to_bohr
        positions = tuple(tuple(float(x) * factor for x in p)
                          for p in configuration.configuration.positions)
        if any(not isfinite(v) for pos in positions for v in pos):
            raise ValueError("atomic positions in bohr must be finite.")
        charges = configuration_formal_charges(configuration)
        species = configuration.species
        fluoride = tuple(i for i, item in enumerate(species)
                         if item is FLiBeSpecies.FLUORINE)
        if not fluoride:
            raise ValueError("at least one fluoride is required for polarization.")

        charge_damping = {pair.species_pair[0]: (pair.b_inverse_bohr, pair.c_dimensionless)
                          for pair in self.parameters.charge_dipole_damping}
        fields: list[Vector3] = []
        for i in fluoride:
            field = [0.0, 0.0, 0.0]
            for j in range(configuration.atom_count):
                if i == j:
                    continue
                delta = _displacement(positions[i], positions[j])
                r2 = _dot(delta, delta)
                if not isfinite(r2) or r2 <= 0.0:
                    raise ValueError("distinct atom positions must have positive separation.")
                distance = sqrt(r2)
                damping = 1.0
                if species[j] in charge_damping:
                    beta, c = charge_damping[species[j]]
                    damping = _damping(beta * distance, c)
                prefactor = charges[j] * damping / (r2 * distance)
                for axis in range(3):
                    field[axis] += prefactor * delta[axis]
            fields.append(tuple(field))

        dimension = 3 * len(fluoride)
        alpha = self.parameters.fluoride_polarizability_bohr3
        hessian = [[0.0] * dimension for _ in range(dimension)]
        for i in range(dimension):
            hessian[i][i] = 1.0 / alpha
        for local_i, atom_i in enumerate(fluoride):
            for local_j in range(local_i + 1, len(fluoride)):
                atom_j = fluoride[local_j]
                delta = _displacement(positions[atom_i], positions[atom_j])
                r2 = _dot(delta, delta)
                if not isfinite(r2) or r2 <= 0.0:
                    raise ValueError("distinct fluoride positions must have positive separation.")
                distance = sqrt(r2)
                inv_r3 = 1.0 / (r2 * distance)
                inv_r5 = inv_r3 / r2
                for a in range(3):
                    for b in range(3):
                        d_ab = 3.0 * delta[a] * delta[b] * inv_r5
                        if a == b:
                            d_ab -= inv_r3
                        hessian[3 * local_i + a][3 * local_j + b] = -d_ab
                        hessian[3 * local_j + b][3 * local_i + a] = -d_ab
        electric = [value for field in fields for value in field]
        dipole_components = _solve_positive_definite(hessian, electric)
        residual = max(abs(fsum(hessian[i][j] * dipole_components[j]
                                 for j in range(dimension)) - electric[i])
                       for i in range(dimension))
        if not isfinite(residual) or residual > self.stationarity_absolute_tolerance:
            raise ValueError("stationary dipole residual exceeds declared tolerance.")

        dipoles = [(0.0, 0.0, 0.0)] * configuration.atom_count
        all_fields = [(0.0, 0.0, 0.0)] * configuration.atom_count
        for local, index in enumerate(fluoride):
            dipoles[index] = tuple(dipole_components[3 * local + a] for a in range(3))
            all_fields[index] = fields[local]
        self_energy = fsum(_dot(dipoles[i], dipoles[i]) / (2.0 * alpha) for i in fluoride)
        charge_energy = -fsum(_dot(dipoles[i], all_fields[i]) for i in fluoride)
        dipole_energy = 0.0
        for local_i, i in enumerate(fluoride):
            for j in fluoride[local_i + 1:]:
                delta = _displacement(positions[i], positions[j])
                r2 = _dot(delta, delta)
                inv_r3 = 1.0 / (r2 * sqrt(r2))
                cross = _dot(dipoles[i], dipoles[j]) - (
                    3.0 * _dot(dipoles[i], delta) * _dot(dipoles[j], delta) / r2
                )
                dipole_energy += cross * inv_r3
        polarization = fsum((self_energy, charge_energy, dipole_energy))
        # At the stationary minimum: U_pol = -0.5 * sum(mu_i . E_i^q).
        stationary_energy = 0.5 * charge_energy
        scale = max(1.0, abs(stationary_energy))
        if not isclose(polarization, stationary_energy, rel_tol=0.0,
                       abs_tol=self.stationarity_absolute_tolerance * scale):
            raise ValueError("stationary polarization energy identity differs.")

        pair_model = self.parameters.build_finite_cluster_model(
            model_id=f"{self.model_id}-pair",
            coordinate_unit_to_bohr=factor,
        )
        pair_result = pair_model.evaluate(configuration)
        total = fsum((pair_result.energy.total_energy, polarization))
        if not isfinite(total):
            raise ValueError("combined finite-cluster energy must be finite.")
        return FLiBeFiniteClusterPolarizationResult(
            configuration=configuration,
            pair_result=pair_result,
            model_id=self.model_id,
            functional_id=POLARIZATION_FUNCTIONAL_ID,
            source_doi=self.parameters.source_doi,
            source_file_sha256=self.parameters.source_file_sha256,
            polarizable_indices=fluoride,
            induced_dipoles_e_bohr=tuple(dipoles),
            charge_fields_atomic=tuple(all_fields),
            self_energy_hartree=self_energy,
            charge_dipole_energy_hartree=charge_energy,
            dipole_dipole_energy_hartree=dipole_energy,
            polarization_energy_hartree=polarization,
            total_energy_hartree=total,
            max_stationarity_residual_atomic=residual,
        )
