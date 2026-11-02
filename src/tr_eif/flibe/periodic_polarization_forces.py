"""Conservative Cartesian forces for stationary periodic FLiBe polarization.

For fixed Ewald and damping shells, the stationarity condition of

    U(R, mu) = sum_i |mu_i|^2/(2 alpha_F) - sum_i mu_i.E_i(R)
               - (1/2) sum_ij mu_i.T_ij(R).mu_j

gives the coordinate derivative at the converged dipoles:

    F_a = sum_i mu_i.(partial E_i / partial R_a)
          + (1/2) sum_ij mu_i.(partial T_ij / partial R_a).mu_j.

The real-space, reciprocal-space, and registered charge-dipole damping
force terms are retained separately. Cell geometry and Ewald parameters
remain fixed during coordinate differentiation. Dipole self terms and
same-site lattice images have zero Cartesian derivative at fixed cell.
Energies are in hartree; forces are hartree per input coordinate unit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, erfc, exp, fsum, isclose, isfinite, pi, sin, sqrt

from tr_eif.energy import ForceState

from .charge import configuration_formal_charges
from .configuration import FLiBeConfiguration
from .periodic_polarization import (
    FLiBePeriodicPolarizationModel,
    FLiBePeriodicPolarizationResult,
    _delta,
    _dot,
    _images,
    _lattice,
    _screened_terms,
)


POLARIZATION_FORCE_FUNCTIONAL_ID = (
    "flibe.periodic.stationary_fluoride_polarization_forces.v1"
)


def _radial_third_derivative(r2: float, alpha: float) -> float:
    """Return H'(r)/r for T_ab = H(r) r_a r_b - D(r) delta_ab."""

    r = sqrt(r2)
    c = 2.0 * alpha * exp(-alpha * alpha * r2) / sqrt(pi)

    return (
        -15.0 * erfc(alpha * r) / (r2 * r2 * r2 * r)
        - 15.0 * c / (r2 * r2 * r2)
        - 10.0 * alpha * alpha * c / (r2 * r2)
        - 4.0 * alpha**4 * c / r2
    )


def _damping_and_derivative(
    radius: float,
    beta: float,
    amplitude: float,
) -> tuple[float, float]:
    """Return source correction g-1 and its radial derivative in bohr."""

    z = beta * radius

    if not isfinite(z) or z <= 0.0:
        raise ValueError(
            "charge-dipole damping argument must be finite and positive."
        )

    if z >= 100.0:
        return 0.0, 0.0

    tail = exp(-z)

    polynomial = (
        1.0
        + z * (
            1.0
            + z * (
                0.5
                + z * (
                    1.0 / 6.0
                    + z / 24.0
                )
            )
        )
    )

    correction = -amplitude * tail * polynomial
    derivative = amplitude * beta * tail * z**4 / 24.0

    return correction, derivative


def _force_state(
    terms: list[list[list[float]]],
    unit: float,
) -> ForceState:
    """Reduce per-coordinate contributions and convert Cartesian units."""

    rows = tuple(
        tuple(
            fsum(terms[i][axis]) * unit
            for axis in range(3)
        )
        for i in range(len(terms))
    )

    if any(
        not isfinite(value)
        for row in rows
        for value in row
    ):
        raise ValueError(
            "periodic polarization forces must be finite."
        )

    return ForceState(rows)


def _term_buffers(
    atom_count: int,
) -> list[list[list[float]]]:
    """Allocate ordered per-atom Cartesian contribution buffers."""

    return [
        [[] for _ in range(3)]
        for _ in range(atom_count)
    ]


def _add_pair(
    terms: list[list[list[float]]],
    i: int,
    j: int,
    force: tuple[float, float, float],
) -> None:
    """Accumulate equal and opposite Cartesian pair contributions."""

    for axis in range(3):
        terms[i][axis].append(force[axis])
        terms[j][axis].append(-force[axis])


@dataclass(frozen=True, slots=True)
class FLiBePeriodicPolarizationForceResult:
    """Stationary polarization force and five geometric-gradient components."""

    polarization_result: FLiBePeriodicPolarizationResult
    charge_real_forces: ForceState
    charge_reciprocal_forces: ForceState
    charge_damping_forces: ForceState
    dipole_real_forces: ForceState
    dipole_reciprocal_forces: ForceState
    polarization_forces: ForceState
    functional_id: str = POLARIZATION_FORCE_FUNCTIONAL_ID

    def __post_init__(self) -> None:
        if not isinstance(
            self.polarization_result,
            FLiBePeriodicPolarizationResult,
        ):
            raise TypeError(
                "polarization_result must be FLiBePeriodicPolarizationResult."
            )

        if self.functional_id != POLARIZATION_FORCE_FUNCTIONAL_ID:
            raise ValueError(
                "periodic polarization force functional identity differs."
            )

        components = self.force_components

        if not isinstance(self.polarization_forces, ForceState) or any(
            not isinstance(component, ForceState)
            for _, component in components
        ):
            raise TypeError(
                "polarization forces and components must be ForceState."
            )

        number = self.polarization_result.configuration.atom_count

        if self.polarization_forces.atom_count != number or any(
            component.atom_count != number
            for _, component in components
        ):
            raise ValueError(
                "force component cardinalities must match atom count."
            )

        for i in range(number):
            for axis in range(3):
                expected = fsum(
                    component.forces[i][axis]
                    for _, component in components
                )

                if not isclose(
                    self.polarization_forces.forces[i][axis],
                    expected,
                    rel_tol=1.0e-12,
                    abs_tol=1.0e-12,
                ):
                    raise ValueError(
                        "polarization forces must equal the sum "
                        "of geometric components."
                    )

    @property
    def configuration(self) -> FLiBeConfiguration:
        """Return the evaluated atomic configuration."""

        return self.polarization_result.configuration

    @property
    def polarization_energy_hartree(self) -> float:
        """Return the stationary polarization energy."""

        return self.polarization_result.polarization_energy_hartree

    @property
    def force_components(self) -> tuple[tuple[str, ForceState], ...]:
        """Return Cartesian force contributions in stable kernel order."""

        return (
            ("charge_real", self.charge_real_forces),
            ("charge_reciprocal", self.charge_reciprocal_forces),
            ("charge_damping", self.charge_damping_forces),
            ("dipole_real", self.dipole_real_forces),
            ("dipole_reciprocal", self.dipole_reciprocal_forces),
        )


def evaluate_flibe_periodic_polarization_forces(
    model: FLiBePeriodicPolarizationModel,
    configuration: FLiBeConfiguration,
) -> FLiBePeriodicPolarizationForceResult:
    """Differentiate the stationary periodic polarization functional.

    The same finite real, reciprocal, and damping image shells used to
    construct stationary dipoles are used for force derivatives.

    Charges and fluoride dipoles are taken from the typed polarization
    result. Cartesian force components follow the declared input-unit
    conversion.

    Fixed-cell differentiation retains the Ewald splitting parameter,
    lattice vectors, source damping parameters, and shell truncations.
    """

    if not isinstance(model, FLiBePeriodicPolarizationModel):
        raise TypeError(
            "model must be FLiBePeriodicPolarizationModel."
        )

    if not isinstance(configuration, FLiBeConfiguration):
        raise TypeError(
            "configuration must be FLiBeConfiguration."
        )

    result = model.evaluate(configuration)

    atomic = configuration.configuration
    unit = model.ewald_parameters.coordinate_unit_to_bohr

    positions = tuple(
        tuple(unit * x for x in xyz)
        for xyz in atomic.positions
    )

    cell = tuple(
        tuple(unit * x for x in xyz)
        for xyz in atomic.cell
    )

    charges = configuration_formal_charges(configuration)

    fluoride = result.polarizable_indices
    dipoles = result.induced_dipoles_e_bohr

    alpha = model.ewald_parameters.alpha_inverse_bohr

    volume, reciprocal = _lattice(cell)

    real_images = _images(
        cell,
        model.ewald_parameters.real_image_shell,
    )

    damping_images = _images(
        cell,
        model.damping_image_shell,
    )

    waves = tuple(
        (
            k,
            4.0 * pi / volume
            * exp(-_dot(k, k) / (4.0 * alpha**2))
            / _dot(k, k),
        )
        for k in _images(
            reciprocal,
            model.ewald_parameters.reciprocal_image_shell,
        )
        if _dot(k, k) > 0.0
    )

    damping_by_source = {
        item.species_pair[0]: (
            item.b_inverse_bohr,
            item.c_dimensionless,
        )
        for item in model.parameters.charge_dipole_damping
    }

    atom_count = configuration.atom_count

    charge_real = _term_buffers(atom_count)
    charge_reciprocal = _term_buffers(atom_count)
    charge_damping = _term_buffers(atom_count)
    dipole_real = _term_buffers(atom_count)
    dipole_reciprocal = _term_buffers(atom_count)

    # Charge-field derivatives, including source-registered damping.

    for i in fluoride:
        mu = dipoles[i]

        for j, charge in enumerate(charges):
            if j == i:
                continue

            base = _delta(
                positions[i],
                positions[j],
            )

            # Real-space screened charge-field gradient.

            for shift in real_images:
                delta = tuple(
                    base[axis] + shift[axis]
                    for axis in range(3)
                )

                d, h = _screened_terms(
                    _dot(delta, delta),
                    alpha,
                )

                projection = _dot(mu, delta)

                pair_force = tuple(
                    charge * (
                        d * mu[axis]
                        - h * projection * delta[axis]
                    )
                    for axis in range(3)
                )

                _add_pair(
                    charge_real,
                    i,
                    j,
                    pair_force,
                )

            # Reciprocal-space charge-field gradient.

            for wave, weight in waves:
                phase = _dot(wave, base)

                strength = (
                    charge
                    * weight
                    * cos(phase)
                    * _dot(mu, wave)
                )

                _add_pair(
                    charge_reciprocal,
                    i,
                    j,
                    tuple(
                        strength * wave[axis]
                        for axis in range(3)
                    ),
                )

            # Source charge-dipole damping derivative.

            if configuration.species[j] in damping_by_source:
                beta, amplitude = damping_by_source[
                    configuration.species[j]
                ]

                for shift in damping_images:
                    delta = tuple(
                        base[axis] + shift[axis]
                        for axis in range(3)
                    )

                    r2 = _dot(delta, delta)

                    if not isfinite(r2) or r2 <= 0.0:
                        raise ValueError(
                            "cation-fluoride damping image distance "
                            "must be positive."
                        )

                    radius = sqrt(r2)

                    g, derivative = _damping_and_derivative(
                        radius,
                        beta,
                        amplitude,
                    )

                    projection = _dot(mu, delta)

                    radial = (
                        derivative / (r2 * r2)
                        - 3.0 * g / (r2 * r2 * radius)
                    )

                    _add_pair(
                        charge_damping,
                        i,
                        j,
                        tuple(
                            charge * (
                                g * mu[axis] / (r2 * radius)
                                + radial
                                * projection
                                * delta[axis]
                            )
                            for axis in range(3)
                        ),
                    )

    # Dipole-dipole tensor derivatives for distinct fluoride sites.

    for local_i, i in enumerate(fluoride):
        mu_i = dipoles[i]

        for j in fluoride[local_i + 1:]:
            mu_j = dipoles[j]

            base = _delta(
                positions[i],
                positions[j],
            )

            mu_inner = _dot(mu_i, mu_j)

            # Real-space dipole tensor derivative.

            for shift in real_images:
                delta = tuple(
                    base[axis] + shift[axis]
                    for axis in range(3)
                )

                r2 = _dot(delta, delta)

                _, h = _screened_terms(
                    r2,
                    alpha,
                )

                third = _radial_third_derivative(
                    r2,
                    alpha,
                )

                projection_i = _dot(mu_i, delta)
                projection_j = _dot(mu_j, delta)

                _add_pair(
                    dipole_real,
                    i,
                    j,
                    tuple(
                        h * (
                            projection_i * mu_j[axis]
                            + projection_j * mu_i[axis]
                            + mu_inner * delta[axis]
                        )
                        + third
                        * projection_i
                        * projection_j
                        * delta[axis]
                        for axis in range(3)
                    ),
                )

            # Reciprocal-space dipole tensor derivative.

            for wave, weight in waves:
                strength = (
                    weight
                    * sin(_dot(wave, base))
                    * _dot(mu_i, wave)
                    * _dot(mu_j, wave)
                )

                _add_pair(
                    dipole_reciprocal,
                    i,
                    j,
                    tuple(
                        strength * wave[axis]
                        for axis in range(3)
                    ),
                )

    # Preserve all five force contributions separately.

    buffers = (
        charge_real,
        charge_reciprocal,
        charge_damping,
        dipole_real,
        dipole_reciprocal,
    )

    components = tuple(
        _force_state(terms, unit)
        for terms in buffers
    )

    combined = ForceState(
        tuple(
            tuple(
                fsum(
                    component.forces[i][axis]
                    for component in components
                )
                for axis in range(3)
            )
            for i in range(atom_count)
        )
    )

    return FLiBePeriodicPolarizationForceResult(
        polarization_result=result,
        charge_real_forces=components[0],
        charge_reciprocal_forces=components[1],
        charge_damping_forces=components[2],
        dipole_real_forces=components[3],
        dipole_reciprocal_forces=components[4],
        polarization_forces=combined,
    )
