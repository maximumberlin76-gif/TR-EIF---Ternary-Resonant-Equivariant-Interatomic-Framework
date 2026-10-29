"""Finite-cluster FLiBe rigid-ion pair energy and Cartesian forces.

The pair law is Coulomb + Born-Mayer + Tang-Toennies-damped C6/C8:

    V_ij(r) = q_i q_j / r + A_ij exp(-alpha_ij r)
              - C6_ij f6(b6_ij r) / r**6
              - C8_ij f8(b8_ij r) / r**8.

The coordinates are converted to bohr and energies are in hartree.
The boundary is an isolated finite cluster with explicit formal ionic charges.
Model coefficients, source identities, and provenance are supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, factorial, fsum, isfinite, sqrt

from tr_eif.energy import EnergyState, ForceState

from .charge import configuration_formal_charges
from .configuration import FLiBeConfiguration
from .species import FLIBE_SPECIES, FLiBeSpecies
from .units import ParameterProvenance


PAIR_FUNCTIONAL_ID = "flibe.finite_cluster.coulomb_born_mayer_tt.v1"
PAIR_ORDER = tuple(
    (FLIBE_SPECIES[i], FLIBE_SPECIES[j])
    for i in range(len(FLIBE_SPECIES))
    for j in range(i, len(FLIBE_SPECIES))
)


def _real(value: float, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result < 0.0 or (positive and result == 0.0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}.")
    return result


def _name(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _damped_inverse_power(r: float, b: float, order: int) -> tuple[float, float]:
    """Return f_n(br)/r**n and its radial derivative.

    f_n(z) = 1 - exp(-z) * sum(z**k/k!, k=0..n).
    The small-argument branch evaluates the complementary series to
    retain the r->0 limit of the damped dispersion derivative.
    """
    z = b * r
    if not isfinite(z):
        raise ValueError("damping argument must be finite.")
    if z < 4.0:
        term = 1.0 / factorial(order + 1)
        series = term
        derivative = 0.0
        for k in range(2, 150):
            derivative += (k - 1) * term / (order + k)
            term *= z / (order + k)
            series += term
            if term <= 1.0e-16 * series:
                break
        coefficient = b ** (order + 1) * exp(-z)
        value = coefficient * r * series
        radial_derivative = coefficient * (series * (1.0 - z) + r * b * derivative)
    else:
        inverse_r = 1.0 / r
        tail = exp(-z)
        polynomial = fsum(z ** k / factorial(k) for k in range(order + 1))
        damping = 1.0 - tail * polynomial
        derivative_z = tail * z ** order / factorial(order)
        value = damping * inverse_r ** order
        radial_derivative = (
            b * derivative_z * inverse_r ** order
            - order * damping * inverse_r ** (order + 1)
        )
    if not isfinite(value) or not isfinite(radial_derivative):
        raise ValueError("damped dispersion evaluation must be finite.")
    return value, radial_derivative


@dataclass(frozen=True, slots=True)
class FLiBePairCoefficients:
    """One unordered Li/Be/F pair with coefficient provenance in atomic units."""

    species_a: FLiBeSpecies
    species_b: FLiBeSpecies
    born_amplitude_hartree: float
    born_decay_inverse_bohr: float
    c6_hartree_bohr6: float
    c8_hartree_bohr8: float
    b6_inverse_bohr: float
    b8_inverse_bohr: float
    provenance: ParameterProvenance
    source_id: str
    source_location: str

    def __post_init__(self) -> None:
        if not isinstance(self.species_a, FLiBeSpecies) or not isinstance(
            self.species_b, FLiBeSpecies
        ):
            raise TypeError("pair species must be FLiBeSpecies values.")
        if (self.species_a, self.species_b) not in PAIR_ORDER:
            raise ValueError("pair species must follow canonical Li, Be, F order.")
        for name in (
            "born_amplitude_hartree",
            "born_decay_inverse_bohr",
            "c6_hartree_bohr6",
            "c8_hartree_bohr8",
            "b6_inverse_bohr",
            "b8_inverse_bohr",
        ):
            _real(getattr(self, name), name)
        if self.born_amplitude_hartree and self.born_decay_inverse_bohr == 0.0:
            raise ValueError("nonzero Born amplitude requires positive decay.")
        if self.c6_hartree_bohr6 and self.b6_inverse_bohr == 0.0:
            raise ValueError("nonzero C6 requires positive b6 damping.")
        if self.c8_hartree_bohr8 and self.b8_inverse_bohr == 0.0:
            raise ValueError("nonzero C8 requires positive b8 damping.")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        _name(self.source_id, "source_id")
        _name(self.source_location, "source_location")


@dataclass(frozen=True, slots=True)
class FLiBePairPotentialResult:
    """Pair energy and forces with retained coefficient provenance.

    Each pair energy contributes one-half to each participating atom.
    """

    configuration: FLiBeConfiguration
    energy: EnergyState
    forces: ForceState
    model_id: str
    pair_functional_id: str
    pair_count: int
    length_unit_to_bohr: float
    pair_coefficients: tuple[FLiBePairCoefficients, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        if not isinstance(self.energy, EnergyState) or not isinstance(self.forces, ForceState):
            raise TypeError("energy and forces must use their respective typed states.")
        if self.energy.atom_count != self.configuration.atom_count or (
            self.forces.atom_count != self.configuration.atom_count
        ):
            raise ValueError("energy and force cardinalities must match the configuration.")
        _name(self.model_id, "model_id")
        if self.pair_functional_id != PAIR_FUNCTIONAL_ID:
            raise ValueError("pair functional identifier differs.")
        count = self.configuration.atom_count
        if self.pair_count != count * (count - 1) // 2:
            raise ValueError("pair count must equal the finite-cluster unordered-pair count.")
        _real(self.length_unit_to_bohr, "length_unit_to_bohr", positive=True)
        if not isinstance(self.pair_coefficients, tuple) or len(self.pair_coefficients) != 6:
            raise ValueError("result must retain six pair coefficient records.")
        for expected, pair in zip(PAIR_ORDER, self.pair_coefficients, strict=True):
            if not isinstance(pair, FLiBePairCoefficients) or (
                pair.species_a, pair.species_b
            ) != expected:
                raise ValueError("result coefficient identities must follow canonical order.")


@dataclass(frozen=True, slots=True)
class FLiBeIndependentPairModel:
    """Finite-cluster pair model with separately supplied Li/Be/F parameters.

    The output forces are gradients of energy with respect to input Cartesian
    coordinates (hartree per input coordinate unit). Pairwise charge products
    use the existing formal ionic-charge contract. All six unordered species
    pairs are supplied and all unordered atom pairs are evaluated once.
    """

    model_id: str
    pair_coefficients: tuple[FLiBePairCoefficients, ...]
    length_unit_to_bohr: float

    def __post_init__(self) -> None:
        _name(self.model_id, "model_id")
        _real(self.length_unit_to_bohr, "length_unit_to_bohr", positive=True)
        if not isinstance(self.pair_coefficients, tuple) or len(self.pair_coefficients) != 6:
            raise ValueError("pair_coefficients must contain six canonical pairs.")
        for expected, pair in zip(PAIR_ORDER, self.pair_coefficients, strict=True):
            if not isinstance(pair, FLiBePairCoefficients):
                raise TypeError("pair_coefficients must contain FLiBePairCoefficients.")
            if (pair.species_a, pair.species_b) != expected:
                raise ValueError("pair coefficients must follow canonical pair order.")

    def evaluate(self, configuration: FLiBeConfiguration) -> FLiBePairPotentialResult:
        """Evaluate independent finite-cluster pair energy and exact radial forces."""
        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        if any(configuration.configuration.periodic):
            raise ValueError("finite-cluster pair evaluation requires nonperiodic axes.")
        configuration.composition()
        atom_count = configuration.atom_count
        charges = configuration_formal_charges(configuration)
        species = configuration.species
        positions = configuration.configuration.positions
        coefficients = dict(zip(PAIR_ORDER, self.pair_coefficients, strict=True))
        species_indices = {kind: i for i, kind in enumerate(FLIBE_SPECIES)}
        energies = [0.0] * atom_count
        forces = [[0.0, 0.0, 0.0] for _ in range(atom_count)]
        pair_energies: list[float] = []
        for i in range(atom_count):
            for j in range(i + 1, atom_count):
                pair_key = (species[i], species[j])
                if species_indices[pair_key[0]] > species_indices[pair_key[1]]:
                    pair_key = (pair_key[1], pair_key[0])
                pair = coefficients[pair_key]
                displacement = tuple(positions[i][a] - positions[j][a] for a in range(3))
                distance_code = sqrt(fsum(d * d for d in displacement))
                r = distance_code * self.length_unit_to_bohr
                if not isfinite(r) or r <= 0.0:
                    raise ValueError("pair distances in bohr must be finite and positive.")
                coulomb = charges[i] * charges[j] / r
                born = pair.born_amplitude_hartree * exp(-pair.born_decay_inverse_bohr * r)
                d_energy_dr = (-charges[i] * charges[j] / (r * r)
                               - pair.born_decay_inverse_bohr * born)
                value = coulomb + born
                for order, dispersion, damping in (
                    (6, pair.c6_hartree_bohr6, pair.b6_inverse_bohr),
                    (8, pair.c8_hartree_bohr8, pair.b8_inverse_bohr),
                ):
                    if dispersion:
                        term, radial_derivative = _damped_inverse_power(r, damping, order)
                        value -= dispersion * term
                        d_energy_dr -= dispersion * radial_derivative
                if not isfinite(value) or not isfinite(d_energy_dr):
                    raise ValueError("pair energy and radial gradient must be finite.")
                pair_energies.append(value)
                energies[i] += 0.5 * value
                energies[j] += 0.5 * value
                coefficient = -d_energy_dr * self.length_unit_to_bohr / distance_code
                for axis in range(3):
                    force = coefficient * displacement[axis]
                    forces[i][axis] += force
                    forces[j][axis] -= force
        if any(not isfinite(v) for row in forces for v in row):
            raise ValueError("Cartesian forces must be finite.")
        return FLiBePairPotentialResult(
            configuration=configuration,
            energy=EnergyState(
                atomic_energies=tuple(energies),
                total_energy=fsum(pair_energies),
            ),
            forces=ForceState(forces=tuple(tuple(row) for row in forces)),
            model_id=self.model_id,
            pair_functional_id=PAIR_FUNCTIONAL_ID,
            pair_count=len(pair_energies),
            length_unit_to_bohr=self.length_unit_to_bohr,
            pair_coefficients=self.pair_coefficients,
        )
