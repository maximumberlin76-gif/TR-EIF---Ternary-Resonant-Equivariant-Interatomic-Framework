"""Homogeneous-strain stress for stationary periodic FLiBe potentials.

The reference-cell strain convention is

    sigma_ab = (1/V_0) dE/depsilon_ab,

where Cartesian positions and all three cell vectors undergo the same
homogeneous deformation. Symmetric off-diagonal strain uses the increment
(epsilon_ab, epsilon_ba) = (s/2, s/2), so dE/ds = V_0 sigma_ab.

The fixed-charge (Ewald plus Born-Mayer/C6/C8) and stationary fluoride
polarization energies are evaluated separately at each strained state.
Stationary dipoles are recomputed for every positive and negative strain.
Ewald splitting, image shells, material coefficients, and their source
identities are retained during the finite difference.

Output stress has units hartree/bohr**3. Positive tensile strain derivative
and the potential contribution to hydrostatic pressure follow the convention
P_potential = -trace(sigma)/3.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import CellStrainDifferentiation, StressState

from .configuration import FLiBeConfiguration
from .periodic_polarizable import (
    FLiBePeriodicPolarizableModel,
    FLiBePeriodicPolarizableResult,
)


_STRAIN_COMPONENTS = (
    (0, 0),
    (1, 1),
    (2, 2),
    (0, 1),
    (0, 2),
    (1, 2),
)


def _volume(
    cell: tuple[tuple[float, float, float], ...],
) -> float:
    """Return the absolute cell volume in its stated Cartesian units."""

    a, b, c = cell

    determinant = (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )

    if not isfinite(determinant) or determinant == 0.0:
        raise ValueError(
            "reference cell volume must be finite and nonzero."
        )

    return abs(determinant)


def _deform(
    configuration: FLiBeConfiguration,
    component_a: int,
    component_b: int,
    strain: float,
) -> FLiBeConfiguration:
    """Apply a symmetric homogeneous strain to positions and cell vectors."""

    atomic = configuration.configuration

    matrix = [
        [float(a == b) for b in range(3)]
        for a in range(3)
    ]

    if component_a == component_b:
        matrix[component_a][component_a] += strain
    else:
        matrix[component_a][component_b] += 0.5 * strain
        matrix[component_b][component_a] += 0.5 * strain

    def transformed(
        vector: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        return tuple(
            fsum(
                matrix[a][b] * vector[b]
                for b in range(3)
            )
            for a in range(3)
        )  # type: ignore[return-value]

    return FLiBeConfiguration(
        AtomicConfiguration(
            species=atomic.species,
            positions=tuple(
                transformed(position)
                for position in atomic.positions
            ),
            cell=tuple(
                transformed(vector)
                for vector in atomic.cell
            ),
            periodic=atomic.periodic,
        )
    )


@dataclass(frozen=True, slots=True)
class FLiBePeriodicStrainSample:
    """Independent fixed-charge and relaxed-polarization energies at +/- strain."""

    components: tuple[int, int]
    fixed_plus_hartree: float
    fixed_minus_hartree: float
    polarization_plus_hartree: float
    polarization_minus_hartree: float

    def __post_init__(self) -> None:
        if self.components not in _STRAIN_COMPONENTS:
            raise ValueError(
                "strain components must be a canonical tensor pair."
            )

        for name in (
            "fixed_plus_hartree",
            "fixed_minus_hartree",
            "polarization_plus_hartree",
            "polarization_minus_hartree",
        ):
            value = getattr(self, name)

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not isfinite(value)
            ):
                raise ValueError(
                    f"{name} must be finite."
                )


@dataclass(frozen=True, slots=True)
class FLiBePeriodicPolarizableStressResult:
    """Two stress channels and their fixed-cell sum, retaining energy evidence."""

    reference: FLiBePeriodicPolarizableResult
    differentiation: CellStrainDifferentiation
    reference_volume_bohr3: float
    samples: tuple[FLiBePeriodicStrainSample, ...]
    fixed_charge_stress: StressState
    polarization_stress: StressState
    total_stress: StressState

    def __post_init__(self) -> None:
        if not isinstance(
            self.reference,
            FLiBePeriodicPolarizableResult,
        ):
            raise TypeError(
                "reference must be FLiBePeriodicPolarizableResult."
            )

        if not isinstance(
            self.differentiation,
            CellStrainDifferentiation,
        ):
            raise TypeError(
                "differentiation must be CellStrainDifferentiation."
            )

        if (
            not isfinite(self.reference_volume_bohr3)
            or self.reference_volume_bohr3 <= 0.0
        ):
            raise ValueError(
                "reference_volume_bohr3 must be finite and positive."
            )

        if (
            not isinstance(self.samples, tuple)
            or len(self.samples) != len(_STRAIN_COMPONENTS)
        ):
            raise ValueError(
                "samples must contain all six strain components."
            )

        if any(
            not isinstance(s, FLiBePeriodicStrainSample)
            for s in self.samples
        ):
            raise TypeError(
                "samples must contain FLiBePeriodicStrainSample values."
            )

        if (
            tuple(s.components for s in self.samples)
            != _STRAIN_COMPONENTS
        ):
            raise ValueError(
                "strain samples must follow canonical tensor order."
            )

        for name in (
            "fixed_charge_stress",
            "polarization_stress",
            "total_stress",
        ):
            tensor = getattr(self, name)

            if (
                not isinstance(tensor, StressState)
                or not tensor.is_symmetric
            ):
                raise TypeError(
                    f"{name} must be a symmetric StressState."
                )

        inverse_span_volume = (
            self.differentiation.inverse_central_span
            / self.reference_volume_bohr3
        )

        for sample in self.samples:
            a, b = sample.components

            fixed_reference = (
                sample.fixed_plus_hartree
                - sample.fixed_minus_hartree
            ) * inverse_span_volume

            polarized_reference = (
                sample.polarization_plus_hartree
                - sample.polarization_minus_hartree
            ) * inverse_span_volume

            expected = (
                (
                    self.fixed_charge_stress,
                    fixed_reference,
                ),
                (
                    self.polarization_stress,
                    polarized_reference,
                ),
                (
                    self.total_stress,
                    fsum((
                        fixed_reference,
                        polarized_reference,
                    )),
                ),
            )

            for state, value in expected:
                if not isclose(
                    state.tensor[a][b],
                    value,
                    rel_tol=1e-10,
                    abs_tol=1e-12,
                ):
                    raise ValueError(
                        "stress tensor components must match "
                        "their strain-energy derivatives."
                    )

    @property
    def potential_pressure_hartree_per_bohr3(self) -> float:
        """Return signed potential hydrostatic pressure from stress trace."""

        return -self.total_stress.trace / 3.0

    @property
    def configuration(self) -> FLiBeConfiguration:
        return self.reference.configuration

    @property
    def source_doi(self) -> str:
        return self.reference.source_doi

    @property
    def source_file_sha256(self) -> str:
        return self.reference.source_file_sha256


def evaluate_flibe_periodic_polarizable_stress(
    model: FLiBePeriodicPolarizableModel,
    configuration: FLiBeConfiguration,
    differentiation: CellStrainDifferentiation,
) -> FLiBePeriodicPolarizableStressResult:
    """Differentiate both energy channels under six homogeneous strains.

    Coordinates, cell vectors, and stationary dipoles follow each strained
    configuration. Source coefficients, numerical shells, and Ewald alpha
    are held fixed. The reference volume is calculated in bohr**3.
    """

    if not isinstance(
        model,
        FLiBePeriodicPolarizableModel,
    ):
        raise TypeError(
            "model must be FLiBePeriodicPolarizableModel."
        )

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be FLiBeConfiguration."
        )

    if not isinstance(
        differentiation,
        CellStrainDifferentiation,
    ):
        raise TypeError(
            "differentiation must be CellStrainDifferentiation."
        )

    atomic = configuration.configuration

    if (
        atomic.periodic != (True, True, True)
        or atomic.cell is None
    ):
        raise ValueError(
            "periodic stress requires three periodic axes and a cell."
        )

    if differentiation.step >= 1.0:
        raise ValueError(
            "strain step must be smaller than one."
        )

    unit = (
        model.fixed_charge_model
        .ewald_model
        .parameters
        .coordinate_unit_to_bohr
    )

    volume = _volume(atomic.cell) * unit**3

    if not isfinite(volume) or volume <= 0.0:
        raise ValueError(
            "converted cell volume must be finite and positive."
        )

    reference = model.evaluate(configuration)

    samples: list[FLiBePeriodicStrainSample] = []

    fixed_values = [
        [0.0] * 3
        for _ in range(3)
    ]

    polarization_values = [
        [0.0] * 3
        for _ in range(3)
    ]

    total_values = [
        [0.0] * 3
        for _ in range(3)
    ]

    inverse_span_volume = (
        differentiation.inverse_central_span
        / volume
    )

    for a, b in _STRAIN_COMPONENTS:
        plus = _deform(
            configuration,
            a,
            b,
            differentiation.step,
        )

        minus = _deform(
            configuration,
            a,
            b,
            -differentiation.step,
        )

        fixed_plus = (
            model.fixed_charge_model
            .evaluate(plus)
            .energy.total_energy
        )

        fixed_minus = (
            model.fixed_charge_model
            .evaluate(minus)
            .energy.total_energy
        )

        polarization_plus = (
            model.polarization_model
            .evaluate(plus)
            .polarization_energy_hartree
        )

        polarization_minus = (
            model.polarization_model
            .evaluate(minus)
            .polarization_energy_hartree
        )

        sample = FLiBePeriodicStrainSample(
            components=(a, b),
            fixed_plus_hartree=fixed_plus,
            fixed_minus_hartree=fixed_minus,
            polarization_plus_hartree=polarization_plus,
            polarization_minus_hartree=polarization_minus,
        )

        samples.append(sample)

        value_fixed = (
            fixed_plus - fixed_minus
        ) * inverse_span_volume

        value_polarization = (
            polarization_plus - polarization_minus
        ) * inverse_span_volume

        for i, j in ((a, b), (b, a)):
            fixed_values[i][j] = value_fixed

            polarization_values[i][j] = (
                value_polarization
            )

            total_values[i][j] = fsum((
                value_fixed,
                value_polarization,
            ))

    def stress(
        values: list[list[float]],
    ) -> StressState:
        return StressState(
            tuple(
                tuple(row)
                for row in values
            )
        )  # type: ignore[arg-type]

    return FLiBePeriodicPolarizableStressResult(
        reference=reference,
        differentiation=differentiation,
        reference_volume_bohr3=volume,
        samples=tuple(samples),
        fixed_charge_stress=stress(fixed_values),
        polarization_stress=stress(polarization_values),
        total_stress=stress(total_values),
    )
