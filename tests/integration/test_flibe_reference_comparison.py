"""Integration tests for strict FLiBe experimental/first-principles comparison."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.reference_comparison import (
    FLiBeEvidenceKind,
    FLiBeReferenceComparison,
    FLiBeReferenceObservable,
    compare_flibe_experimental_first_principles,
)
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.units import ParameterProvenance


def _composition() -> FLiBeComposition:
    """Return the exact 2 LiF : 1 BeF2 formula-unit composition."""

    return FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )


def _state() -> FLiBeThermodynamicState:
    """Return one explicit comparison thermodynamic state."""

    return FLiBeThermodynamicState(
        temperature=1000.0,
        pressure=0.0,
    )


def _experimental(
    *,
    values: tuple[float, ...] = (1.0, 2.0, 3.0),
    axis: tuple[float, ...] | None = (0.1, 0.2, 0.3),
    axis_unit: str | None = "1/angstrom",
    observable_id: str = "structure_factor",
    composition: FLiBeComposition | None = None,
    thermodynamic_state: FLiBeThermodynamicState | None = None,
    physical_state_id: str = "liquid",
    value_unit: str = "dimensionless",
    normalization_id: str = "normalization-a",
) -> FLiBeReferenceObservable:
    """Construct one experimental reference observable."""

    return FLiBeReferenceObservable(
        observable_id=observable_id,
        composition=_composition() if composition is None else composition,
        thermodynamic_state=(
            _state()
            if thermodynamic_state is None
            else thermodynamic_state
        ),
        physical_state_id=physical_state_id,
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        values=values,
        value_unit=value_unit,
        normalization_id=normalization_id,
        source_id="FLIBE-PRIMARY-TEST",
        method_id="TEST_FIXTURE:experimental-method",
        provenance=ParameterProvenance.TEST_FIXTURE,
        axis=axis,
        axis_unit=axis_unit,
    )


def _first_principles(
    *,
    values: tuple[float, ...] = (1.5, 1.0, 4.0),
    axis: tuple[float, ...] | None = (0.1, 0.2, 0.3),
    axis_unit: str | None = "1/angstrom",
    observable_id: str = "structure_factor",
    composition: FLiBeComposition | None = None,
    thermodynamic_state: FLiBeThermodynamicState | None = None,
    physical_state_id: str = "liquid",
    value_unit: str = "dimensionless",
    normalization_id: str = "normalization-a",
) -> FLiBeReferenceObservable:
    """Construct one first-principles reference observable."""

    return FLiBeReferenceObservable(
        observable_id=observable_id,
        composition=_composition() if composition is None else composition,
        thermodynamic_state=(
            _state()
            if thermodynamic_state is None
            else thermodynamic_state
        ),
        physical_state_id=physical_state_id,
        evidence_kind=FLiBeEvidenceKind.FIRST_PRINCIPLES,
        values=values,
        value_unit=value_unit,
        normalization_id=normalization_id,
        source_id="FLIBE-FIRST-PRINCIPLES-TEST",
        method_id="TEST_FIXTURE:first-principles-method",
        provenance=ParameterProvenance.TEST_FIXTURE,
        axis=axis,
        axis_unit=axis_unit,
    )


def test_evidence_kind_values_are_explicit_nonternary_labels() -> None:
    """Evidence classes must remain separate from balanced-ternary states."""

    assert tuple(kind.value for kind in FLiBeEvidenceKind) == (
        "EXPERIMENTAL",
        "FIRST_PRINCIPLES",
    )


def test_reference_observable_normalizes_identifiers_and_values() -> None:
    """Reference metadata and accepted numeric vectors must normalize."""

    observable = FLiBeReferenceObservable(
        observable_id=" structure_factor ",
        composition=_composition(),
        thermodynamic_state=_state(),
        physical_state_id=" liquid ",
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        values=(1, 2.5),
        value_unit=" dimensionless ",
        normalization_id=" normalization-a ",
        source_id=" source-a ",
        method_id=" method-a ",
        provenance=ParameterProvenance.TEST_FIXTURE,
        axis=(1, 2.0),
        axis_unit=" 1/angstrom ",
    )

    assert observable.observable_id == "structure_factor"
    assert observable.physical_state_id == "liquid"
    assert observable.values == (1.0, 2.5)
    assert observable.value_unit == "dimensionless"
    assert observable.normalization_id == "normalization-a"
    assert observable.source_id == "source-a"
    assert observable.method_id == "method-a"
    assert observable.axis == (1.0, 2.0)
    assert observable.axis_unit == "1/angstrom"
    assert observable.sample_count == 2


@pytest.mark.parametrize(
    "field_name",
    (
        "observable_id",
        "physical_state_id",
        "value_unit",
        "normalization_id",
        "source_id",
        "method_id",
    ),
)
def test_reference_identifiers_must_be_strings(field_name: str) -> None:
    """Every reference identifier field must use the string contract."""

    arguments: dict[str, object] = {
        "observable_id": "structure_factor",
        "composition": _composition(),
        "thermodynamic_state": _state(),
        "physical_state_id": "liquid",
        "evidence_kind": FLiBeEvidenceKind.EXPERIMENTAL,
        "values": (1.0,),
        "value_unit": "dimensionless",
        "normalization_id": "normalization-a",
        "source_id": "source-a",
        "method_id": "method-a",
        "provenance": ParameterProvenance.TEST_FIXTURE,
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        FLiBeReferenceObservable(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "observable_id",
        "physical_state_id",
        "value_unit",
        "normalization_id",
        "source_id",
        "method_id",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        "",
        "   ",
        "\t\n",
    ),
)
def test_reference_identifiers_must_not_be_empty(
    field_name: str,
    value: str,
) -> None:
    """Reference identifiers must remain nonempty after normalization."""

    arguments = {
        "observable_id": "structure_factor",
        "composition": _composition(),
        "thermodynamic_state": _state(),
        "physical_state_id": "liquid",
        "evidence_kind": FLiBeEvidenceKind.EXPERIMENTAL,
        "values": (1.0,),
        "value_unit": "dimensionless",
        "normalization_id": "normalization-a",
        "source_id": "source-a",
        "method_id": "method-a",
        "provenance": ParameterProvenance.TEST_FIXTURE,
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        FLiBeReferenceObservable(**arguments)


def test_reference_requires_flibe_composition() -> None:
    """Comparison records must retain an explicit FLiBe composition."""

    with pytest.raises(
        TypeError,
        match="composition must be an FLiBeComposition instance",
    ):
        FLiBeReferenceObservable(
            observable_id="structure_factor",
            composition=None,  # type: ignore[arg-type]
            thermodynamic_state=_state(),
            physical_state_id="liquid",
            evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
            values=(1.0,),
            value_unit="dimensionless",
            normalization_id="normalization-a",
            source_id="source-a",
            method_id="method-a",
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


def test_reference_requires_flibe_thermodynamic_state() -> None:
    """Comparison records must retain an explicit thermodynamic state."""

    with pytest.raises(
        TypeError,
        match=(
            "thermodynamic_state must be an "
            "FLiBeThermodynamicState instance"
        ),
    ):
        FLiBeReferenceObservable(
            observable_id="structure_factor",
            composition=_composition(),
            thermodynamic_state=None,  # type: ignore[arg-type]
            physical_state_id="liquid",
            evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
            values=(1.0,),
            value_unit="dimensionless",
            normalization_id="normalization-a",
            source_id="source-a",
            method_id="method-a",
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "evidence_kind",
    (
        -1,
        0,
        1,
        "EXPERIMENTAL",
    ),
)
def test_evidence_kind_rejects_ternary_and_raw_values(
    evidence_kind: object,
) -> None:
    """Evidence class must not be substituted by ternary or raw values."""

    with pytest.raises(
        TypeError,
        match="evidence_kind must be an FLiBeEvidenceKind",
    ):
        FLiBeReferenceObservable(
            observable_id="structure_factor",
            composition=_composition(),
            thermodynamic_state=_state(),
            physical_state_id="liquid",
            evidence_kind=evidence_kind,  # type: ignore[arg-type]
            values=(1.0,),
            value_unit="dimensionless",
            normalization_id="normalization-a",
            source_id="source-a",
            method_id="method-a",
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


def test_reference_requires_parameter_provenance() -> None:
    """Reference provenance must use the canonical provenance enum."""

    with pytest.raises(
        TypeError,
        match="provenance must be a ParameterProvenance",
    ):
        FLiBeReferenceObservable(
            observable_id="structure_factor",
            composition=_composition(),
            thermodynamic_state=_state(),
            physical_state_id="liquid",
            evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
            values=(1.0,),
            value_unit="dimensionless",
            normalization_id="normalization-a",
            source_id="source-a",
            method_id="method-a",
            provenance="PRIMARY_SOURCE",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("values", "exception"),
    (
        ([], TypeError),
        ((), ValueError),
        ((True,), TypeError),
        (("1.0",), TypeError),
        ((float("inf"),), ValueError),
        ((float("nan"),), ValueError),
    ),
)
def test_reference_values_are_strictly_validated(
    values: object,
    exception: type[Exception],
) -> None:
    """Observable samples must be a nonempty finite-real tuple."""

    with pytest.raises(exception):
        FLiBeReferenceObservable(
            observable_id="structure_factor",
            composition=_composition(),
            thermodynamic_state=_state(),
            physical_state_id="liquid",
            evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
            values=values,  # type: ignore[arg-type]
            value_unit="dimensionless",
            normalization_id="normalization-a",
            source_id="source-a",
            method_id="method-a",
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


def test_scalar_reference_may_omit_axis() -> None:
    """A scalar observable may be represented without a sampled axis."""

    observable = _experimental(
        values=(2.5,),
        axis=None,
        axis_unit=None,
        observable_id="density",
        value_unit="test-unit",
    )

    assert observable.axis is None
    assert observable.axis_unit is None
    assert observable.sample_count == 1


def test_axis_unit_is_forbidden_when_axis_is_absent() -> None:
    """Axis units cannot be detached from actual axis coordinates."""

    with pytest.raises(
        ValueError,
        match="axis_unit must be None when axis is None",
    ):
        _experimental(
            values=(1.0,),
            axis=None,
            axis_unit="1/angstrom",
        )


def test_axis_requires_axis_unit() -> None:
    """Sampled observables must declare the axis unit explicitly."""

    with pytest.raises(
        ValueError,
        match="axis_unit is required when axis is present",
    ):
        _experimental(
            values=(1.0,),
            axis=(0.1,),
            axis_unit=None,
        )


def test_axis_and_values_must_have_same_length() -> None:
    """Directly sampled coordinate and observable vectors must align exactly."""

    with pytest.raises(
        ValueError,
        match="axis and values must have the same length",
    ):
        _experimental(
            values=(1.0, 2.0),
            axis=(0.1,),
            axis_unit="1/angstrom",
        )


@pytest.mark.parametrize(
    ("axis", "exception"),
    (
        ([0.1], TypeError),
        ((), ValueError),
        ((True,), TypeError),
        ((float("inf"),), ValueError),
        ((float("nan"),), ValueError),
    ),
)
def test_axis_values_are_strictly_validated(
    axis: object,
    exception: type[Exception],
) -> None:
    """Sample axes must use the same finite immutable numeric contract."""

    with pytest.raises(exception):
        _experimental(
            values=(1.0,),
            axis=axis,  # type: ignore[arg-type]
            axis_unit="1/angstrom",
        )


def test_direct_comparison_computes_signed_residuals() -> None:
    """Residual convention must be first-principles minus experimental."""

    comparison = compare_flibe_experimental_first_principles(
        _experimental(),
        _first_principles(),
    )

    assert comparison.residuals == pytest.approx(
        (0.5, -1.0, 1.0)
    )
    assert comparison.absolute_residuals == pytest.approx(
        (0.5, 1.0, 1.0)
    )


def test_direct_comparison_error_metrics_are_exactly_defined() -> None:
    """MAE, RMSE, and maximum absolute error must follow their definitions."""

    comparison = compare_flibe_experimental_first_principles(
        _experimental(),
        _first_principles(),
    )

    assert comparison.sample_count == 3
    assert comparison.mean_absolute_error == pytest.approx(2.5 / 3.0)
    assert comparison.root_mean_square_error == pytest.approx(
        (2.25 / 3.0) ** 0.5
    )
    assert comparison.max_absolute_error == pytest.approx(1.0)


def test_identical_records_have_zero_residual_metrics() -> None:
    """Numerically identical matched evidence must produce zero residuals."""

    values = (1.0, 2.0, 3.0)

    comparison = compare_flibe_experimental_first_principles(
        _experimental(values=values),
        _first_principles(values=values),
    )

    assert comparison.residuals == pytest.approx((0.0, 0.0, 0.0))
    assert comparison.mean_absolute_error == 0.0
    assert comparison.root_mean_square_error == 0.0
    assert comparison.max_absolute_error == 0.0


def test_comparison_requires_experimental_evidence_kind() -> None:
    """The experimental side cannot be replaced by first-principles evidence."""

    with pytest.raises(
        ValueError,
        match="experimental record must have EXPERIMENTAL evidence kind",
    ):
        FLiBeReferenceComparison(
            experimental=_first_principles(),
            first_principles=_first_principles(),
        )


def test_comparison_requires_first_principles_evidence_kind() -> None:
    """The computational side must be explicitly first-principles evidence."""

    with pytest.raises(
        ValueError,
        match=(
            "first_principles record must have "
            "FIRST_PRINCIPLES evidence kind"
        ),
    ):
        FLiBeReferenceComparison(
            experimental=_experimental(),
            first_principles=_experimental(),
        )


@pytest.mark.parametrize(
    ("field_name", "first_principles"),
    (
        (
            "observable_id",
            _first_principles(observable_id="pair_distribution"),
        ),
        (
            "composition",
            _first_principles(
                composition=FLiBeComposition(
                    lif_fraction=3.0,
                    bef2_fraction=1.0,
                )
            ),
        ),
        (
            "thermodynamic_state",
            _first_principles(
                thermodynamic_state=FLiBeThermodynamicState(
                    temperature=1100.0,
                    pressure=0.0,
                )
            ),
        ),
        (
            "physical_state_id",
            _first_principles(physical_state_id="solid"),
        ),
        (
            "value_unit",
            _first_principles(value_unit="other-unit"),
        ),
        (
            "normalization_id",
            _first_principles(normalization_id="normalization-b"),
        ),
        (
            "axis",
            _first_principles(axis=(0.1, 0.2, 0.4)),
        ),
        (
            "axis_unit",
            _first_principles(axis_unit="other-axis-unit"),
        ),
    ),
)
def test_direct_comparison_rejects_mismatched_contract_fields(
    field_name: str,
    first_principles: FLiBeReferenceObservable,
) -> None:
    """Direct comparison requires identity of every declared comparison field."""

    with pytest.raises(
        ValueError,
        match=(
            rf"experimental and first-principles {field_name} "
            "must match for direct comparison"
        ),
    ):
        compare_flibe_experimental_first_principles(
            _experimental(),
            first_principles,
        )


def test_direct_comparison_rejects_sample_count_mismatch_without_axis() -> None:
    """Scalar/vector records cannot be compared when sample counts differ."""

    with pytest.raises(
        ValueError,
        match=(
            "experimental and first-principles sample counts must match"
        ),
    ):
        compare_flibe_experimental_first_principles(
            _experimental(
                values=(1.0, 2.0),
                axis=None,
                axis_unit=None,
                observable_id="density_series",
                value_unit="test-unit",
            ),
            _first_principles(
                values=(1.0,),
                axis=None,
                axis_unit=None,
                observable_id="density_series",
                value_unit="test-unit",
            ),
        )


def test_source_and_method_identifiers_may_differ_across_evidence_paths() -> None:
    """Independent evidence paths must retain their own provenance metadata."""

    experimental = _experimental()
    first_principles = _first_principles()

    comparison = compare_flibe_experimental_first_principles(
        experimental,
        first_principles,
    )

    assert experimental.source_id != first_principles.source_id
    assert experimental.method_id != first_principles.method_id
    assert comparison.experimental is experimental
    assert comparison.first_principles is first_principles


def test_comparison_does_not_create_pass_fail_or_ternary_status() -> None:
    """Numerical residual reporting must remain separate from validation state."""

    comparison = compare_flibe_experimental_first_principles(
        _experimental(),
        _first_principles(),
    )

    assert not hasattr(comparison, "is_valid")
    assert not hasattr(comparison, "passed")
    assert not hasattr(comparison, "tolerance")
    assert not hasattr(comparison, "ternary_state")


def test_comparison_is_deterministic() -> None:
    """Identical explicit evidence records must reproduce the same comparison."""

    experimental = _experimental()
    first_principles = _first_principles()

    first = compare_flibe_experimental_first_principles(
        experimental,
        first_principles,
    )
    second = compare_flibe_experimental_first_principles(
        experimental,
        first_principles,
    )

    assert first == second
    assert first.residuals == second.residuals


def test_reference_observable_is_frozen() -> None:
    """Source-backed reference records must be immutable after validation."""

    observable = _experimental()

    with pytest.raises(FrozenInstanceError):
        observable.source_id = "replacement"  # type: ignore[misc]


def test_reference_comparison_is_frozen() -> None:
    """Matched evidence comparison records must be immutable."""

    comparison = compare_flibe_experimental_first_principles(
        _experimental(),
        _first_principles(),
    )

    with pytest.raises(FrozenInstanceError):
        comparison.experimental = _experimental()  # type: ignore[misc]
