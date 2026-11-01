"""Three-dimensional periodic Ewald electrostatics for neutral FLiBe cells.

The atomic-unit energy comprises screened real-space, reciprocal-space,
and Gaussian self-interaction terms under conducting boundary conditions.
The real and reciprocal lattice sums use explicit symmetric integer shells.
Born-Mayer, dispersion, and induced-dipole energies are separate operators.

All Cartesian coordinates are converted to bohr before evaluation. Energies
are in hartree and forces in hartree per input Cartesian coordinate unit.
The caller declares the Ewald splitting parameter and truncation shells.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import cos, erfc, exp, fsum, isclose, isfinite, pi, sin, sqrt
from typing import TypeAlias

from tr_eif.energy import EnergyState, ForceState

from .charge import configuration_formal_charges
from .configuration import FLiBeConfiguration
from .units import ParameterProvenance


Vector3: TypeAlias = tuple[float, float, float]
Cell3: TypeAlias = tuple[Vector3, Vector3, Vector3]
EWALD_FUNCTIONAL_ID = "flibe.periodic.neutral_3d_ewald.v1"


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return result


def _shell(value: int, name: str, *, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}.")
    return value


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be a nonempty trimmed string.")
    return value


def _dot(a: Vector3, b: Vector3) -> float:
    return fsum(a[d] * b[d] for d in range(3))


def _cross(a: Vector3, b: Vector3) -> Vector3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _lattice(cell: Cell3) -> tuple[float, Cell3]:
    a, b, c = cell
    signed_volume = _dot(a, _cross(b, c))
    if not isfinite(signed_volume) or signed_volume == 0.0:
        raise ValueError("periodic cell must have finite nonzero volume.")
    reciprocal = tuple(
        tuple(2.0 * pi * component / signed_volume for component in normal)
        for normal in (_cross(b, c), _cross(c, a), _cross(a, b))
    )
    return abs(signed_volume), reciprocal  # type: ignore[return-value]


def _indices(shell: int):
    return product(range(-shell, shell + 1), repeat=3)


def _translate(cell: Cell3, index: tuple[int, int, int]) -> Vector3:
    return tuple(fsum(index[j] * cell[j][axis] for j in range(3)) for axis in range(3))  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class FLiBeEwaldParameters:
    """Ewald splitting, symmetric lattice shells, and unit provenance."""

    alpha_inverse_bohr: float
    real_image_shell: int
    reciprocal_image_shell: int
    coordinate_unit_to_bohr: float
    provenance: ParameterProvenance
    source_id: str

    def __post_init__(self) -> None:
        _positive(self.alpha_inverse_bohr, "alpha_inverse_bohr")
        _shell(self.real_image_shell, "real_image_shell", minimum=0)
        _shell(self.reciprocal_image_shell, "reciprocal_image_shell", minimum=1)
        _positive(self.coordinate_unit_to_bohr, "coordinate_unit_to_bohr")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        _identifier(self.source_id, "source_id")


@dataclass(frozen=True, slots=True)
class FLiBePeriodicEwaldResult:
    """Source-resolved periodic Coulomb energy decomposition and forces."""

    configuration: FLiBeConfiguration
    model_id: str
    parameters: FLiBeEwaldParameters
    functional_id: str
    formal_charges_e: tuple[int, ...]
    cell_volume_bohr3: float
    real_energy_hartree: float
    reciprocal_energy_hartree: float
    self_energy_hartree: float
    energy: EnergyState
    forces: ForceState
    real_terms_evaluated: int
    reciprocal_vectors_evaluated: int

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        _identifier(self.model_id, "model_id")
        if not isinstance(self.parameters, FLiBeEwaldParameters):
            raise TypeError("parameters must be FLiBeEwaldParameters.")
        if self.functional_id != EWALD_FUNCTIONAL_ID:
            raise ValueError("functional identifier differs.")
        if self.formal_charges_e != configuration_formal_charges(self.configuration):
            raise ValueError("formal charges must correspond to ordered species.")
        if sum(self.formal_charges_e) != 0:
            raise ValueError("periodic Ewald cell must have zero total formal charge.")
        _positive(self.cell_volume_bohr3, "cell_volume_bohr3")
        for name in ("real_energy_hartree", "reciprocal_energy_hartree", "self_energy_hartree"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
                raise ValueError(f"{name} must be finite.")
        if not isinstance(self.energy, EnergyState) or not isinstance(self.forces, ForceState):
            raise TypeError("energy and forces must be their typed states.")
        if self.energy.atom_count != self.configuration.atom_count or self.forces.atom_count != self.configuration.atom_count:
            raise ValueError("energy and force cardinality must equal atom count.")
        component_sum = fsum((self.real_energy_hartree, self.reciprocal_energy_hartree, self.self_energy_hartree))
        if not isclose(self.energy.total_energy, component_sum, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Ewald component energies must sum to total energy.")
        if not isclose(self.energy.total_energy, fsum(self.energy.atomic_energies), rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Ewald atomic energy partition must sum to total energy.")
        n = self.configuration.atom_count
        r = self.parameters.real_image_shell
        k = self.parameters.reciprocal_image_shell
        if self.real_terms_evaluated != n * n * (2 * r + 1) ** 3 - n:
            raise ValueError("real-space directed term count differs.")
        if self.reciprocal_vectors_evaluated != (2 * k + 1) ** 3 - 1:
            raise ValueError("reciprocal lattice vector count differs.")


@dataclass(frozen=True, slots=True)
class FLiBePeriodicEwaldModel:
    """Neutral, 3D-periodic formal-charge Coulomb evaluation in atomic units."""

    model_id: str
    parameters: FLiBeEwaldParameters

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        if not isinstance(self.parameters, FLiBeEwaldParameters):
            raise TypeError("parameters must be FLiBeEwaldParameters.")

    def evaluate(self, configuration: FLiBeConfiguration) -> FLiBePeriodicEwaldResult:
        """Compute symmetric truncated Ewald sums and their Cartesian gradients.

        The reciprocal sum includes both +k and -k; the k=0 vector is excluded.
        Self subtraction corresponds to the selected Gaussian splitting alpha.
        The simulation cell uses conducting (tin-foil) boundary conditions.
        """
        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        atomic = configuration.configuration
        if atomic.periodic != (True, True, True) or atomic.cell is None:
            raise ValueError("periodic Ewald requires three periodic axes and a cell.")
        configuration.composition()
        charges = configuration_formal_charges(configuration)
        if sum(charges) != 0:
            raise ValueError("periodic Ewald requires an exactly neutral cell.")

        unit = self.parameters.coordinate_unit_to_bohr
        cell = tuple(tuple(value * unit for value in axis) for axis in atomic.cell)
        positions = tuple(tuple(value * unit for value in position) for position in atomic.positions)
        if any(not isfinite(value) for vec in (*cell, *positions) for value in vec):
            raise ValueError("atomic coordinates and cell must be finite in bohr.")
        volume, reciprocal_basis = _lattice(cell)  # type: ignore[arg-type]
        alpha = self.parameters.alpha_inverse_bohr
        n = configuration.atom_count
        real_atom = [0.0] * n
        reciprocal_atom = [0.0] * n
        forces = [[0.0, 0.0, 0.0] for _ in range(n)]

        for image in _indices(self.parameters.real_image_shell):
            shift = _translate(cell, image)  # type: ignore[arg-type]
            for i in range(n):
                for j in range(n):
                    if i == j and image == (0, 0, 0):
                        continue
                    delta = tuple(positions[i][axis] - positions[j][axis] + shift[axis] for axis in range(3))
                    squared = _dot(delta, delta)  # type: ignore[arg-type]
                    if not isfinite(squared) or squared <= 0.0:
                        raise ValueError("periodic ionic separations must be finite and positive.")
                    distance = sqrt(squared)
                    product_charge = charges[i] * charges[j]
                    screened = erfc(alpha * distance)
                    gaussian = exp(-(alpha * distance) ** 2)
                    real_atom[i] += 0.5 * product_charge * screened / distance
                    radial = product_charge * (
                        screened / (squared * distance)
                        + 2.0 * alpha * gaussian / (sqrt(pi) * squared)
                    )
                    for axis in range(3):
                        forces[i][axis] += radial * delta[axis]

        prefactor = 2.0 * pi / volume
        for image in _indices(self.parameters.reciprocal_image_shell):
            if image == (0, 0, 0):
                continue
            wave = _translate(reciprocal_basis, image)  # type: ignore[arg-type]
            norm_squared = _dot(wave, wave)
            if not isfinite(norm_squared) or norm_squared <= 0.0:
                raise ValueError("reciprocal wave vectors must have positive finite norm.")
            weight = prefactor * exp(-norm_squared / (4.0 * alpha**2)) / norm_squared
            phases = tuple(_dot(wave, position) for position in positions)
            cosine = tuple(cos(angle) for angle in phases)
            sine = tuple(sin(angle) for angle in phases)
            rho_real = fsum(charge * cosine[i] for i, charge in enumerate(charges))
            rho_imag = fsum(charge * sine[i] for i, charge in enumerate(charges))
            for i, charge in enumerate(charges):
                reciprocal_atom[i] += weight * charge * (
                    cosine[i] * rho_real + sine[i] * rho_imag
                )
                force_weight = 2.0 * weight * charge * (
                    sine[i] * rho_real - cosine[i] * rho_imag
                )
                for axis in range(3):
                    forces[i][axis] += force_weight * wave[axis]

        self_atom = tuple(-alpha / sqrt(pi) * charge**2 for charge in charges)
        real_energy = fsum(real_atom)
        reciprocal_energy = fsum(reciprocal_atom)
        self_energy = fsum(self_atom)
        atomic_energies = tuple(
            fsum((real_atom[i], reciprocal_atom[i], self_atom[i])) for i in range(n)
        )
        energy_total = fsum((real_energy, reciprocal_energy, self_energy))
        forces_in_input_units = tuple(tuple(
            value * unit for value in force
        ) for force in forces)
        if not isfinite(energy_total) or any(
            not isfinite(value) for row in forces_in_input_units for value in row
        ):
            raise ValueError("periodic Ewald energy and forces must be finite.")
        return FLiBePeriodicEwaldResult(
            configuration=configuration,
            model_id=self.model_id,
            parameters=self.parameters,
            functional_id=EWALD_FUNCTIONAL_ID,
            formal_charges_e=charges,
            cell_volume_bohr3=volume,
            real_energy_hartree=real_energy,
            reciprocal_energy_hartree=reciprocal_energy,
            self_energy_hartree=self_energy,
            energy=EnergyState(atomic_energies, energy_total),
            forces=ForceState(forces_in_input_units),
            real_terms_evaluated=n * n * (2 * self.parameters.real_image_shell + 1) ** 3 - n,
            reciprocal_vectors_evaluated=(2 * self.parameters.reciprocal_image_shell + 1) ** 3 - 1,
        )
