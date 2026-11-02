"""Stationary periodic fluoride polarization with Ewald charge/dipole kernels.

The polarization energy in atomic units is

    U = sum_i |mu_i|^2/(2 alpha_F) - sum_i mu_i.E_i^q
        - (1/2) sum_ij mu_i.T_ij.mu_j.

The fluoride charge field E^q and the periodic dipole tensor T use the
same conducting-boundary 3D Ewald Green function and finite lattice shells.
The charge field includes source-registered cation-fluoride short-range
charge-dipole damping corrections, evaluated over a separate image shell.
The dipole self tensor includes the Gaussian Ewald self correction.

Only fluoride ions carry induced dipoles. The symmetric stationary Hessian
A = I/alpha_F - T is solved by Cholesky factorization. The polarization
energy remains separate from Ewald charge-charge and Born-Mayer/C6/C8 energy.
Cartesian coordinates are converted to bohr; energies are in hartree.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import cos, erfc, exp, fsum, isclose, isfinite, pi, sin, sqrt
from typing import TypeAlias

from .charge import configuration_formal_charges
from .configuration import FLiBeConfiguration
from .periodic_coulomb_ewald import FLiBeEwaldParameters
from .registered_pair_coefficients import FLiBeRegisteredPairParameters
from .species import FLiBeSpecies


Vector3: TypeAlias = tuple[float, float, float]
Cell3: TypeAlias = tuple[Vector3, Vector3, Vector3]
POLARIZATION_FUNCTIONAL_ID = "flibe.periodic.stationary_fluoride_polarization_ewald.v1"


def _dot(a: Vector3, b: Vector3) -> float:
    return fsum(a[i] * b[i] for i in range(3))


def _cross(a: Vector3, b: Vector3) -> Vector3:
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])


def _delta(a: Vector3, b: Vector3) -> Vector3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def _lattice(cell: Cell3) -> tuple[float, Cell3]:
    signed = _dot(cell[0], _cross(cell[1], cell[2]))
    if not isfinite(signed) or signed == 0.0:
        raise ValueError("periodic cell must have finite nonzero volume.")
    normals = (_cross(cell[1], cell[2]), _cross(cell[2], cell[0]),
               _cross(cell[0], cell[1]))
    reciprocal = tuple(tuple(2.0*pi*x/signed for x in normal)
                       for normal in normals)
    return abs(signed), reciprocal  # type: ignore[return-value]


def _images(cell: Cell3, shell: int) -> tuple[Vector3, ...]:
    return tuple(tuple(fsum(m[j] * cell[j][a] for j in range(3))
                       for a in range(3))
                 for m in product(range(-shell, shell+1), repeat=3))  # type: ignore[return-value]


def _screened_terms(r2: float, alpha: float) -> tuple[float, float]:
    """Return D and H for Hessian(G_real) = H*r*r - D*I.

    Electric field from charge q is q*D*r, where
    D = erfc(alpha*r)/r^3 + 2*alpha*exp(-alpha^2*r^2)/(sqrt(pi)*r^2).
    """
    if not isfinite(r2) or r2 <= 0.0:
        raise ValueError("Ewald image separation must be finite and positive.")
    r = sqrt(r2)
    gaussian = exp(-alpha*alpha*r2)
    screened = erfc(alpha*r)
    c = 2.0*alpha*gaussian/sqrt(pi)
    d = screened/(r2*r) + c/r2
    h = 3.0*screened/(r2*r2*r) + 3.0*c/(r2*r2) + 2.0*alpha*alpha*c/r2
    return d, h


def _damping_correction(radius: float, beta: float, amplitude: float) -> float:
    """Return g(r)-1 for source charge-dipole damping g(r)."""
    z = beta*radius
    if not isfinite(z) or z <= 0.0:
        raise ValueError("damping argument must be finite and positive.")
    if z >= 100.0:
        return 0.0
    polynomial = 1.0 + z*(1.0 + z*(0.5 + z*(1.0/6.0 + z/24.0)))
    return -amplitude*exp(-z)*polynomial


def _cholesky_solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Solve a symmetric positive-definite stationary dipole Hessian."""
    n = len(rhs)
    l = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            residual = matrix[i][j] - fsum(l[i][k]*l[j][k] for k in range(j))
            if i == j:
                if not isfinite(residual) or residual <= 0.0:
                    raise ValueError("periodic polarization Hessian must be positive definite.")
                l[i][j] = sqrt(residual)
            else:
                l[i][j] = residual/l[j][j]
    y = [0.0]*n
    for i in range(n):
        y[i] = (rhs[i] - fsum(l[i][j]*y[j] for j in range(i)))/l[i][i]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - fsum(l[j][i]*x[j] for j in range(i+1, n)))/l[i][i]
    if any(not isfinite(value) for value in x):
        raise ValueError("stationary periodic dipoles must be finite.")
    return x


@dataclass(frozen=True, slots=True)
class FLiBePeriodicPolarizationResult:
    """Source-resolved stationary fluoride dipoles and polarization energies."""

    configuration: FLiBeConfiguration
    model_id: str
    source_doi: str
    source_file_sha256: str
    ewald_parameters: FLiBeEwaldParameters
    damping_image_shell: int
    polarizable_indices: tuple[int, ...]
    induced_dipoles_e_bohr: tuple[Vector3, ...]
    charge_fields_atomic: tuple[Vector3, ...]
    self_energy_hartree: float
    charge_dipole_energy_hartree: float
    dipole_dipole_energy_hartree: float
    polarization_energy_hartree: float
    max_stationarity_residual_atomic: float
    functional_id: str = POLARIZATION_FUNCTIONAL_ID

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        if self.functional_id != POLARIZATION_FUNCTIONAL_ID:
            raise ValueError("periodic polarization functional identity differs.")
        if not isinstance(self.model_id, str) or not self.model_id.strip() or self.model_id != self.model_id.strip():
            raise ValueError("model_id must be a nonempty trimmed string.")
        if not isinstance(self.ewald_parameters, FLiBeEwaldParameters):
            raise TypeError("ewald_parameters must be FLiBeEwaldParameters.")
        if not isinstance(self.source_doi, str) or not self.source_doi:
            raise ValueError("source DOI must be specified.")
        digest = self.source_file_sha256
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError("source_file_sha256 must be a lowercase SHA-256 digest.")
        if isinstance(self.damping_image_shell, bool) or not isinstance(self.damping_image_shell, int) or self.damping_image_shell < 0:
            raise ValueError("damping_image_shell must be a nonnegative integer.")
        expected = tuple(i for i, s in enumerate(self.configuration.species) if s is FLiBeSpecies.FLUORINE)
        if self.polarizable_indices != expected:
            raise ValueError("polarizable_indices must select all fluoride ions in order.")
        if len(self.induced_dipoles_e_bohr) != self.configuration.atom_count or len(self.charge_fields_atomic) != self.configuration.atom_count:
            raise ValueError("dipole and field arrays must match atom count.")
        for name in ('induced_dipoles_e_bohr', 'charge_fields_atomic'):
            for v in getattr(self, name):
                if not isinstance(v, tuple) or len(v) != 3 or any(not isinstance(x, (float, int)) or isinstance(x, bool) or not isfinite(x) for x in v):
                    raise ValueError(f"{name} must contain finite Cartesian vectors.")
        if any(self.induced_dipoles_e_bohr[i] != (0.0, 0.0, 0.0) for i in range(self.configuration.atom_count) if i not in expected):
            raise ValueError("only fluoride sites may carry induced dipoles.")
        values = (self.self_energy_hartree, self.charge_dipole_energy_hartree,
                  self.dipole_dipole_energy_hartree, self.polarization_energy_hartree,
                  self.max_stationarity_residual_atomic)
        if any(not isinstance(v, (float, int)) or isinstance(v, bool) or not isfinite(v) for v in values):
            raise ValueError("polarization energies and residual must be finite.")
        if self.max_stationarity_residual_atomic < 0.0:
            raise ValueError("stationarity residual must be nonnegative.")
        if not isclose(self.polarization_energy_hartree, fsum(values[:3]), rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("polarization energy must equal its three components.")


@dataclass(frozen=True, slots=True)
class FLiBePeriodicPolarizationModel:
    """Stationary F-ion polarization using source damping and periodic Ewald."""

    model_id: str
    parameters: FLiBeRegisteredPairParameters
    ewald_parameters: FLiBeEwaldParameters
    damping_image_shell: int
    stationarity_absolute_tolerance: float

    def __post_init__(self) -> None:
        if not isinstance(self.model_id, str) or not self.model_id.strip() or self.model_id != self.model_id.strip():
            raise ValueError("model_id must be a nonempty trimmed string.")
        if not isinstance(self.parameters, FLiBeRegisteredPairParameters):
            raise TypeError("parameters must be FLiBeRegisteredPairParameters.")
        if not isinstance(self.ewald_parameters, FLiBeEwaldParameters):
            raise TypeError("ewald_parameters must be FLiBeEwaldParameters.")
        if isinstance(self.damping_image_shell, bool) or not isinstance(self.damping_image_shell, int) or self.damping_image_shell < 0:
            raise ValueError("damping_image_shell must be a nonnegative integer.")
        if isinstance(self.stationarity_absolute_tolerance, bool) or not isinstance(self.stationarity_absolute_tolerance, (int, float)) or not isfinite(self.stationarity_absolute_tolerance) or self.stationarity_absolute_tolerance <= 0.0:
            raise ValueError("stationarity_absolute_tolerance must be finite and positive.")

    def evaluate(self, configuration: FLiBeConfiguration) -> FLiBePeriodicPolarizationResult:
        """Calculate Ewald charge fields, dipole Hessian, and stationary dipoles.

        Conducting-boundary Ewald sums use the real and reciprocal shells in
        ewald_parameters. The reciprocal dipole Hessian includes all k != 0.
        The regularized self dipole tensor contains +4*alpha^3/(3*sqrt(pi)) I.
        The registered cation-F damping adds (g-1)*q*r/r^3 per image to the
        undamped Ewald charge field, without modifying charge-charge energy.
        """
        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        atomic = configuration.configuration
        if atomic.periodic != (True, True, True) or atomic.cell is None:
            raise ValueError("periodic polarization requires three periodic axes and a cell.")
        configuration.composition()
        charges = configuration_formal_charges(configuration)
        if sum(charges) != 0:
            raise ValueError("periodic polarization requires an exactly neutral cell.")
        factor = self.ewald_parameters.coordinate_unit_to_bohr
        positions = tuple(tuple(x*factor for x in xyz) for xyz in atomic.positions)
        cell = tuple(tuple(x*factor for x in xyz) for xyz in atomic.cell)
        if any(not isfinite(x) for xyz in (*positions, *cell) for x in xyz):
            raise ValueError("atomic positions and cell must be finite in bohr.")
        volume, reciprocal = _lattice(cell)  # type: ignore[arg-type]
        alpha = self.ewald_parameters.alpha_inverse_bohr
        real_images = _images(cell, self.ewald_parameters.real_image_shell)  # type: ignore[arg-type]
        damping_images = _images(cell, self.damping_image_shell)  # type: ignore[arg-type]
        reciprocal_images = _images(reciprocal, self.ewald_parameters.reciprocal_image_shell)
        waves: list[tuple[Vector3, float]] = []
        for k in reciprocal_images:
            k2 = _dot(k, k)
            if k2 == 0.0:
                continue
            weight = 4.0*pi/volume*exp(-k2/(4.0*alpha*alpha))/k2
            waves.append((k, weight))
        fluoride = tuple(i for i, s in enumerate(configuration.species) if s is FLiBeSpecies.FLUORINE)
        beta_c = {item.species_pair[0]: (item.b_inverse_bohr, item.c_dimensionless)
                  for item in self.parameters.charge_dipole_damping}
        fields = [[0.0, 0.0, 0.0] for _ in fluoride]
        for local_i, i in enumerate(fluoride):
            for j, q in enumerate(charges):
                displacement = _delta(positions[i], positions[j])
                for shift in real_images:
                    if i == j and shift == (0.0, 0.0, 0.0):
                        continue
                    r = tuple(displacement[a] + shift[a] for a in range(3))
                    d, _ = _screened_terms(_dot(r, r), alpha)  # type: ignore[arg-type]
                    for a in range(3):
                        fields[local_i][a] += q*d*r[a]
                for k, weight in waves:
                    phase = _dot(k, displacement)
                    for a in range(3):
                        fields[local_i][a] += q*weight*sin(phase)*k[a]
                if configuration.species[j] in beta_c:
                    beta, c = beta_c[configuration.species[j]]
                    for shift in damping_images:
                        r = tuple(displacement[a] + shift[a] for a in range(3))
                        r2 = _dot(r, r)
                        if not isfinite(r2) or r2 <= 0.0:
                            raise ValueError("cation-fluoride image separation must be positive.")
                        correction = q*_damping_correction(sqrt(r2), beta, c)/(r2*sqrt(r2))
                        for a in range(3):
                            fields[local_i][a] += correction*r[a]

        m = 3*len(fluoride)
        tensor = [[0.0]*m for _ in range(m)]
        for local_i, i in enumerate(fluoride):
            for local_j, j in enumerate(fluoride):
                base = _delta(positions[i], positions[j])
                for shift in real_images:
                    if i == j and shift == (0.0, 0.0, 0.0):
                        continue
                    r = tuple(base[a] + shift[a] for a in range(3))
                    d, h = _screened_terms(_dot(r, r), alpha)  # type: ignore[arg-type]
                    for a in range(3):
                        for b in range(3):
                            tensor[3*local_i+a][3*local_j+b] += h*r[a]*r[b] - (d if a == b else 0.0)
                for k, weight in waves:
                    phase_factor = -weight*cos(_dot(k, base))
                    for a in range(3):
                        for b in range(3):
                            tensor[3*local_i+a][3*local_j+b] += phase_factor*k[a]*k[b]
                if i == j:
                    for a in range(3):
                        tensor[3*local_i+a][3*local_j+a] += 4.0*alpha**3/(3.0*sqrt(pi))
        polarizability = self.parameters.fluoride_polarizability_bohr3
        hessian = [[(1.0/polarizability if i == j else 0.0)-tensor[i][j]
                    for j in range(m)] for i in range(m)]
        asymmetry = max(abs(hessian[i][j]-hessian[j][i])
                        for i in range(m) for j in range(i)) if m > 1 else 0.0
        if not isfinite(asymmetry) or asymmetry > 1e-11:
            raise ValueError("periodic dipole Hessian must be symmetric.")
        # Symmetric Ewald shells may retain roundoff-level asymmetry.
        for i in range(m):
            for j in range(i):
                mean = 0.5*(hessian[i][j]+hessian[j][i])
                hessian[i][j] = mean
                hessian[j][i] = mean
        electric = [x for row in fields for x in row]
        dipoles = _cholesky_solve(hessian, electric)
        residual = max(abs(fsum(hessian[i][j]*dipoles[j] for j in range(m))-electric[i])
                       for i in range(m))
        if not isfinite(residual) or residual > self.stationarity_absolute_tolerance:
            raise ValueError("periodic dipole stationarity residual exceeds declared tolerance.")
        self_energy = fsum(x*x for x in dipoles)/(2.0*polarizability)
        charge_energy = -fsum(dipoles[i]*electric[i] for i in range(m))
        dipole_energy = -0.5*fsum(dipoles[i]*tensor[i][j]*dipoles[j]
                                  for i in range(m) for j in range(m))
        polarization = fsum((self_energy, charge_energy, dipole_energy))
        if not isclose(polarization, 0.5*charge_energy, rel_tol=0.0,
                       abs_tol=self.stationarity_absolute_tolerance*max(1.0, abs(polarization))):
            raise ValueError("periodic stationary polarization energy identity differs.")
        complete = [(0.0, 0.0, 0.0)]*configuration.atom_count
        all_fields = [(0.0, 0.0, 0.0)]*configuration.atom_count
        for local_i, i in enumerate(fluoride):
            complete[i] = tuple(dipoles[3*local_i+a] for a in range(3))
            all_fields[i] = tuple(fields[local_i])
        return FLiBePeriodicPolarizationResult(
            configuration=configuration, model_id=self.model_id,
            source_doi=self.parameters.source_doi,
            source_file_sha256=self.parameters.source_file_sha256,
            ewald_parameters=self.ewald_parameters,
            damping_image_shell=self.damping_image_shell,
            polarizable_indices=fluoride,
            induced_dipoles_e_bohr=tuple(complete),
            charge_fields_atomic=tuple(all_fields),
            self_energy_hartree=self_energy,
            charge_dipole_energy_hartree=charge_energy,
            dipole_dipole_energy_hartree=dipole_energy,
            polarization_energy_hartree=polarization,
            max_stationarity_residual_atomic=residual,
        )
