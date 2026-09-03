"""Chemical composition primitives for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias


SpeciesAmount: TypeAlias = tuple[str, float]
SpeciesComposition: TypeAlias = tuple[SpeciesAmount, ...]


@dataclass(frozen=True)
class FLiBeComposition:
    """Normalized LiF-BeF2 composition expressed in formula-unit fractions."""

    lif_fraction: float
    bef2_fraction: float

    def __post_init__(self) -> None:
        """Validate and normalize the binary FLiBe composition."""

        lif_fraction = self._validate_fraction(
            self.lif_fraction,
            "lif_fraction",
        )
        bef2_fraction = self._validate_fraction(
            self.bef2_fraction,
            "bef2_fraction",
        )

        total = lif_fraction + bef2_fraction

        if total <= 0.0:
            raise ValueError(
                "FLiBe composition must contain a positive "
                "total formula-unit fraction."
            )

        object.__setattr__(
            self,
            "lif_fraction",
            lif_fraction / total,
        )
        object.__setattr__(
            self,
            "bef2_fraction",
            bef2_fraction / total,
        )

    @staticmethod
    def _validate_fraction(
        value: float,
        name: str,
    ) -> float:
        """Return one finite nonnegative composition fraction."""

        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise TypeError(
                f"{name} must be a real non-Boolean number."
            )

        normalized = float(value)

        if not isfinite(normalized):
            raise ValueError(
                f"{name} must be finite."
            )

        if normalized < 0.0:
            raise ValueError(
                f"{name} must be nonnegative."
            )

        return normalized

    @property
    def formula_unit_fractions(
        self,
    ) -> tuple[float, float]:
        """Return normalized fractions in LiF, BeF2 order."""

        return (
            self.lif_fraction,
            self.bef2_fraction,
        )

    @property
    def lithium_fraction(
        self,
    ) -> float:
        """Return the atomic fraction of lithium."""

        denominator = (
            2.0 * self.lif_fraction
            + 3.0 * self.bef2_fraction
        )

        return self.lif_fraction / denominator

    @property
    def beryllium_fraction(
        self,
    ) -> float:
        """Return the atomic fraction of beryllium."""

        denominator = (
            2.0 * self.lif_fraction
            + 3.0 * self.bef2_fraction
        )

        return self.bef2_fraction / denominator

    @property
    def fluorine_fraction(
        self,
    ) -> float:
        """Return the atomic fraction of fluorine."""

        denominator = (
            2.0 * self.lif_fraction
            + 3.0 * self.bef2_fraction
        )

        fluorine_amount = (
            self.lif_fraction
            + 2.0 * self.bef2_fraction
        )

        return fluorine_amount / denominator

    @property
    def atomic_fractions(
        self,
    ) -> SpeciesComposition:
        """Return Li, Be, and F atomic fractions."""

        return (
            (
                "Li",
                self.lithium_fraction,
            ),
            (
                "Be",
                self.beryllium_fraction,
            ),
            (
                "F",
                self.fluorine_fraction,
            ),
        )

    def formula_unit_amounts(
        self,
        total_formula_units: float = 1.0,
    ) -> tuple[float, float]:
        """Scale normalized LiF and BeF2 fractions by a positive amount."""

        if isinstance(
            total_formula_units,
            bool,
        ) or not isinstance(
            total_formula_units,
            (int, float),
        ):
            raise TypeError(
                "total_formula_units must be a real "
                "non-Boolean number."
            )

        total = float(
            total_formula_units
        )

        if not isfinite(total):
            raise ValueError(
                "total_formula_units must be finite."
            )

        if total <= 0.0:
            raise ValueError(
                "total_formula_units must be positive."
            )

        return (
            total * self.lif_fraction,
            total * self.bef2_fraction,
        )

    def atomic_amounts(
        self,
        total_formula_units: float = 1.0,
    ) -> SpeciesComposition:
        """Return Li, Be, and F amounts for a formula-unit amount."""

        lif_amount, bef2_amount = (
            self.formula_unit_amounts(
                total_formula_units
            )
        )

        return (
            (
                "Li",
                lif_amount,
            ),
            (
                "Be",
                bef2_amount,
            ),
            (
                "F",
                lif_amount
                + 2.0 * bef2_amount,
            ),
        )


def eutectic_flibe_composition() -> FLiBeComposition:
    """Return the reference 2 LiF : 1 BeF2 formula-unit composition."""

    return FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )
