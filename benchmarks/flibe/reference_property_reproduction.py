"""Structured source-backed FLiBe property-reproduction benchmark."""

from __future__ import annotations

import json
from math import isclose

from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.density import FLiBeDensityModel, evaluate_density
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.units import FLiBeUnit, ParameterProvenance


BENCHMARK_ID = "tr-eif.flibe.reference-property-reproduction.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "FLIBE-REFERENCE-JANZ-1974-DENSITY"

REFERENCE_LIF_MOL_PERCENT = 67.0
REFERENCE_BEF2_MOL_PERCENT = 33.0

TEMPERATURE_MIN_K = 800.0
TEMPERATURE_MAX_K = 1080.0

DENSITY_INTERCEPT_KG_M3 = 2413.0
DENSITY_SLOPE_KG_M3_PER_K = -0.488

ABSOLUTE_TOLERANCE_KG_M3 = 1.0e-9

REFERENCE_POINTS = (
    (800.0, 2022.6),
    (850.0, 1998.2),
    (900.0, 1973.8),
    (950.0, 1949.4),
    (1000.0, 1925.0),
    (1050.0, 1900.6),
    (1080.0, 1885.96),
)


def _reference_composition() -> FLiBeComposition:
    """Return the registered 67 mol% LiF / 33 mol% BeF2 composition."""

    return FLiBeComposition(
        lif_fraction=REFERENCE_LIF_MOL_PERCENT,
        bef2_fraction=REFERENCE_BEF2_MOL_PERCENT,
    )


def _exact_two_to_one_composition() -> FLiBeComposition:
    """Return exact 2 LiF : 1 BeF2 for the explicit composition distinction."""

    return FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )


def _density_evaluator(
    state: FLiBeThermodynamicState,
) -> float:
    """Evaluate the registered source-derived density correlation."""

    temperature = state.temperature

    if not (
        TEMPERATURE_MIN_K
        <= temperature
        <= TEMPERATURE_MAX_K
    ):
        raise ValueError(
            "temperature is outside the registered "
            "density-correlation range."
        )

    return (
        DENSITY_INTERCEPT_KG_M3
        + DENSITY_SLOPE_KG_M3_PER_K
        * temperature
    )


def _density_model() -> FLiBeDensityModel:
    """Construct the executable source-derived density model."""

    return FLiBeDensityModel(
        evaluator=_density_evaluator,
        provenance=ParameterProvenance.DERIVED,
        source=SOURCE_ID,
    )


def _evaluate_reference_domain(
    composition: FLiBeComposition,
    temperature: float,
):
    """Evaluate density only inside the registered composition/state domain."""

    if composition != _reference_composition():
        raise ValueError(
            "composition is outside the registered "
            "density-correlation composition."
        )

    return evaluate_density(
        _density_model(),
        FLiBeThermodynamicState(
            temperature=temperature,
            pressure=0.0,
        ),
    )


def _outside_domain_rejected() -> bool:
    """Verify rejection of temperature and composition domain violations."""

    try:
        _evaluate_reference_domain(
            _reference_composition(),
            TEMPERATURE_MIN_K - 1.0,
        )
    except ValueError:
        pass
    else:
        return False

    try:
        _evaluate_reference_domain(
            _exact_two_to_one_composition(),
            1000.0,
        )
    except ValueError:
        return True

    return False


def run_benchmark() -> dict[str, object]:
    """Run the source-backed FLiBe density reproduction benchmark."""

    composition = _reference_composition()
    exact_two_to_one = (
        _exact_two_to_one_composition()
    )

    samples: list[dict[str, object]] = []
    residuals: list[float] = []

    metadata_valid = True

    for temperature, expected_density in REFERENCE_POINTS:
        parameter = _evaluate_reference_domain(
            composition,
            temperature,
        )

        residual = (
            parameter.value
            - expected_density
        )

        residuals.append(
            residual
        )

        metadata_valid = (
            metadata_valid
            and parameter.unit
            is FLiBeUnit.KILOGRAM_PER_CUBIC_METER
            and parameter.provenance
            is ParameterProvenance.DERIVED
            and parameter.source
            == SOURCE_ID
        )

        samples.append(
            {
                "temperature_k": temperature,
                "reference_density_kg_m3": (
                    expected_density
                ),
                "model_density_kg_m3": (
                    parameter.value
                ),
                "residual_kg_m3": (
                    residual
                ),
            }
        )

    absolute_residuals = tuple(
        abs(value)
        for value in residuals
    )

    max_absolute_error = max(
        absolute_residuals
    )

    mean_absolute_error = (
        sum(
            absolute_residuals
        )
        / float(
            len(
                absolute_residuals
            )
        )
    )

    model_values = tuple(
        sample[
            "model_density_kg_m3"
        ]
        for sample in samples
    )

    checks = {
        "reference_composition": (
            isclose(
                composition.lif_fraction,
                0.67,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            and isclose(
                composition.bef2_fraction,
                0.33,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
        ),
        "exact_two_to_one_is_distinct": (
            composition
            != exact_two_to_one
        ),
        "reference_points_inside_registered_range": all(
            TEMPERATURE_MIN_K
            <= temperature
            <= TEMPERATURE_MAX_K
            for temperature, _
            in REFERENCE_POINTS
        ),
        "density_metadata_preserved": (
            metadata_valid
        ),
        "reference_values_reproduced": (
            max_absolute_error
            <= ABSOLUTE_TOLERANCE_KG_M3
        ),
        "density_decreases_over_registered_samples": all(
            current < previous
            for previous, current in zip(
                model_values[:-1],
                model_values[1:],
                strict=True,
            )
        ),
        "outside_domain_rejected": (
            _outside_domain_rejected()
        ),
    }

    status = (
        "PASS"
        if all(
            checks.values()
        )
        else "FAIL"
    )

    return {
        "benchmark_id": BENCHMARK_ID,
        "provenance": PROVENANCE,
        "status": status,
        "source_id": SOURCE_ID,
        "source_correlation": {
            "density_intercept_kg_m3": (
                DENSITY_INTERCEPT_KG_M3
            ),
            "density_slope_kg_m3_per_k": (
                DENSITY_SLOPE_KG_M3_PER_K
            ),
            "temperature_min_k": (
                TEMPERATURE_MIN_K
            ),
            "temperature_max_k": (
                TEMPERATURE_MAX_K
            ),
            "lif_mol_percent": (
                REFERENCE_LIF_MOL_PERCENT
            ),
            "bef2_mol_percent": (
                REFERENCE_BEF2_MOL_PERCENT
            ),
        },
        "absolute_tolerance_kg_m3": (
            ABSOLUTE_TOLERANCE_KG_M3
        ),
        "checks": checks,
        "observed": {
            "samples": samples,
            "mean_absolute_error_kg_m3": (
                mean_absolute_error
            ),
            "max_absolute_error_kg_m3": (
                max_absolute_error
            ),
            "exact_two_to_one_lif_fraction": (
                exact_two_to_one.lif_fraction
            ),
            "exact_two_to_one_bef2_fraction": (
                exact_two_to_one.bef2_fraction
            ),
        },
    }


def main() -> None:
    """Run the benchmark and emit deterministic structured JSON."""

    report = run_benchmark()

    print(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
    )

    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
