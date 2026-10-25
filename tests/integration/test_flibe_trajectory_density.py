"""Independent integration contracts for periodic FLiBe trajectory density."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
    ForceState,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind, FLiBeReferenceObservable
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.trajectory_density import (
    FLiBeDensityReferenceComparison,
    FLiBeTrajectoryDensity,
    compare_flibe_trajectory_density_to_reference,
    evaluate_flibe_trajectory_density,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import InteractionGraph
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory, run_velocity_verlet_trajectory
from tr_eif.ternary import TernaryExecutionVector, TernaryState


SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
POSITIONS = (
    (0.1, 0.1, 0.1),
    (0.6, 0.1, 0.1),
    (0.2, 0.6, 0.2),
    (0.3, 0.3, 0.7),
    (0.8, 0.3, 0.7),
    (0.4, 0.9, 1.1),
    (0.9, 0.7, 1.3),
)
CELLS = (
    ((2.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)),
    ((4.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)),
    ((6.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)),
)
MASS_FACTOR = 1.0e-27
LENGTH_FACTOR = 1.0e-10
NORMALIZATION = "mean-instantaneous-cell-density"
THERMODYNAMIC_STATE = FLiBeThermodynamicState(temperature=1000.0, pressure=0.0)


def _parameters() -> FLiBeMassParameters:
    return FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0)


def _state(
    index: int,
    cell: tuple[tuple[float, float, float], ...],
) -> MolecularDynamicsState:
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=POSITIONS,
            cell=cell,
            periodic=(True, True, True),
        ),
        velocities=((0.0, 0.0, 0.0),) * len(SPECIES),
        masses=MASSES,
        step=index,
        time=0.25 * index,
    )


def _states() -> tuple[MolecularDynamicsState, ...]:
    return tuple(_state(i, cell) for i, cell in enumerate(CELLS))


def _trajectory(
    states: tuple[MolecularDynamicsState, ...] | None = None,
) -> MolecularDynamicsTrajectory:
    ordered = _states() if states is None else states
    graph = InteractionGraph(node_count=len(SPECIES), edges=())
    forces = ForceState(forces=((0.0, 0.0, 0.0),) * len(SPECIES))
    return MolecularDynamicsTrajectory(
        steps=tuple(
            MolecularDynamicsStepResult(
                previous=previous,
                current=current,
                graph_before=graph,
                graph_after=graph,
                forces_before=forces,
                forces_after=forces,
            )
            for previous, current in zip(ordered[:-1], ordered[1:], strict=True)
        )
    )


def _density(
    trajectory: MolecularDynamicsTrajectory | None = None,
    **overrides: object,
) -> FLiBeTrajectoryDensity:
    arguments: dict[str, object] = {
        "trajectory": _trajectory() if trajectory is None else trajectory,
        "mass_parameters": _parameters(),
        "model_id": "TR-EIP-TEST-FIXTURE",
        "trajectory_id": "PERIODIC-CELL-FIXTURE",
        "provenance": ParameterProvenance.TEST_FIXTURE,
        "mass_unit_to_kg": MASS_FACTOR,
        "coordinate_unit_to_meter": LENGTH_FACTOR,
    }
    arguments.update(overrides)
    return evaluate_flibe_trajectory_density(**arguments)


def _reference(**overrides: object) -> FLiBeReferenceObservable:
    arguments: dict[str, object] = {
        "observable_id": "mass_density",
        "composition": FLiBeComposition(2.0, 1.0),
        "thermodynamic_state": THERMODYNAMIC_STATE,
        "physical_state_id": "liquid",
        "evidence_kind": FLiBeEvidenceKind.EXPERIMENTAL,
        "values": (700.0,),
        "value_unit": "kg/m^3",
        "normalization_id": NORMALIZATION,
        "source_id": "INDEPENDENT-DENSITY-TEST-FIXTURE",
        "method_id": "TEST-FIXTURE-DIRECT-DENSITY",
        "provenance": ParameterProvenance.TEST_FIXTURE,
    }
    arguments.update(overrides)
    return FLiBeReferenceObservable(**arguments)


def _compare(
    density: FLiBeTrajectoryDensity | None = None,
    reference: FLiBeReferenceObservable | None = None,
    **overrides: object,
) -> FLiBeDensityReferenceComparison:
    arguments: dict[str, object] = {
        "model_trace": _density() if density is None else density,
        "reference": _reference() if reference is None else reference,
        "thermodynamic_state": THERMODYNAMIC_STATE,
        "physical_state_id": "liquid",
        "normalization_id": NORMALIZATION,
    }
    arguments.update(overrides)
    return compare_flibe_trajectory_density_to_reference(**arguments)


def test_periodic_cell_densities_match_independent_mass_and_volume_fixture() -> None:
    """Seven fixed atoms with M=27 units occupy 24, 48, and 72 volume units."""
    density = _density()

    assert density.composition == FLiBeComposition(2.0, 1.0)
    assert density.atom_count == 7
    assert density.total_mass_kg == pytest.approx(27.0e-27, rel=1e-14)
    assert density.sample_count == 3
    assert tuple(sample.state_index for sample in density.samples) == (0, 1, 2)
    assert tuple(sample.md_step for sample in density.samples) == (0, 1, 2)
    assert tuple(sample.md_time for sample in density.samples) == (0.0, 0.25, 0.5)
    assert tuple(sample.cell_volume_m3 for sample in density.samples) == pytest.approx(
        (24.0e-30, 48.0e-30, 72.0e-30), rel=1e-13
    )
    assert tuple(sample.density_kg_m3 for sample in density.samples) == pytest.approx(
        (1125.0, 562.5, 375.0), rel=1e-13
    )
    assert density.mean_density_kg_m3 == pytest.approx(687.5, rel=1e-13)
    assert density.mean_cell_volume_m3 == pytest.approx(48.0e-30, rel=1e-13)
    assert density.density_at_mean_volume_kg_m3 == pytest.approx(562.5, rel=1e-13)
    assert density.mean_density_kg_m3 != pytest.approx(density.density_at_mean_volume_kg_m3)
    assert density.provenance is ParameterProvenance.TEST_FIXTURE
    assert density.model_id == "TR-EIP-TEST-FIXTURE"
    assert density.trajectory_id == "PERIODIC-CELL-FIXTURE"


def test_sampling_stride_and_start_index_preserve_state_identity() -> None:
    selected = _density(first_state_index=0, stride=2)
    assert tuple(sample.state_index for sample in selected.samples) == (0, 2)
    assert tuple(sample.md_time for sample in selected.samples) == (0.0, 0.5)
    assert selected.mean_density_kg_m3 == pytest.approx(750.0, rel=1e-13)

    trailing = _density(first_state_index=1, stride=2)
    assert tuple(sample.state_index for sample in trailing.samples) == (1,)
    assert trailing.samples[0].density_kg_m3 == pytest.approx(562.5, rel=1e-13)


def test_explicit_si_factors_control_density_dimensions() -> None:
    density = _density(mass_unit_to_kg=2.0e-27, coordinate_unit_to_meter=2.0e-10)
    assert density.total_mass_kg == pytest.approx(54.0e-27, rel=1e-13)
    assert density.samples[0].cell_volume_m3 == pytest.approx(192.0e-30, rel=1e-13)
    assert density.samples[0].density_kg_m3 == pytest.approx(281.25, rel=1e-13)


def test_absolute_determinant_for_skew_and_reversed_periodic_cell() -> None:
    skew = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (1.0, 1.0, -4.0))
    trajectory = _trajectory(tuple(_state(i, skew) for i in range(3)))
    density = _density(trajectory)
    assert all(sample.density_kg_m3 == pytest.approx(1125.0) for sample in density.samples)


def test_trajectory_density_replays_with_equal_ordered_outputs() -> None:
    first = _density()
    second = _density()
    assert first == second
    assert replace(second, trajectory_id="SECOND-TRAJECTORY") != first
    with pytest.raises(FrozenInstanceError):
        first.model_id = "CHANGED"  # type: ignore[misc]


def test_velocity_verlet_trajectory_integrates_with_density_operator() -> None:
    """Exercise the actual MD integrator with a fixed periodic-cell energy fixture."""
    initial = _state(0, CELLS[0])
    model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.0),
        conditioning=TernaryConditioning(
            negative_scale=1.0, neutral_scale=1.0, positive_scale=1.0
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.0,), bias=0.0
        ),
    )
    trajectory = run_velocity_verlet_trajectory(
        initial_state=initial,
        model=model,
        force_evaluator=ConservativeForceEvaluator(
            differentiation=CoordinateDifferentiation(step=1.0e-6)
        ),
        features=NodeFeatureVector(
            nodes=tuple(
                NodeFeatures(scalars=(0.5,), vectors=((1.0, 0.0, 0.0),))
                for _ in SPECIES
            )
        ),
        execution=TernaryExecutionVector.from_retained_states(
            (TernaryState.NEGATIVE, TernaryState.NEUTRAL, TernaryState.POSITIVE,
             TernaryState.NEUTRAL, TernaryState.NEGATIVE,
             TernaryState.POSITIVE, TernaryState.NEUTRAL)
        ),
        cutoff=0.5,
        time_step=0.01,
        step_count=2,
    )
    density = _density(trajectory)
    assert trajectory.step_count == 2
    assert density.sample_count == 3
    assert tuple(sample.md_step for sample in density.samples) == (0, 1, 2)
    assert all(sample.density_kg_m3 == pytest.approx(1125.0) for sample in density.samples)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    (
        ("mass_unit_to_kg", 0.0, ValueError),
        ("mass_unit_to_kg", False, TypeError),
        ("coordinate_unit_to_meter", -1.0, ValueError),
        ("coordinate_unit_to_meter", float("nan"), ValueError),
        ("coordinate_unit_to_meter", float("inf"), ValueError),
        ("first_state_index", -1, ValueError),
        ("first_state_index", 3, ValueError),
        ("first_state_index", True, TypeError),
        ("stride", 0, ValueError),
        ("stride", False, TypeError),
        ("model_id", " ", ValueError),
        ("trajectory_id", "LEADING ", ValueError),
        ("provenance", "TEST_FIXTURE", TypeError),
        ("mass_parameters", None, TypeError),
    ),
)
def test_density_rejects_invalid_inputs(field: str, value: object, error: type[Exception]) -> None:
    with pytest.raises(error):
        _density(**{field: value})


def test_density_rejects_changed_atomic_mass_inventory() -> None:
    states = _states()
    changed = replace(states[2], masses=MASSES[:-1] + (6.0,))
    with pytest.raises(ValueError, match="mass inventory"):
        _density(_trajectory(states[:2] + (changed,)))


def test_density_rejects_species_reordering() -> None:
    states = _states()
    changed = replace(
        states[2],
        configuration=replace(
            states[2].configuration,
            species=("Li", "Be", "Li", "F", "F", "F", "F"),
        ),
    )
    with pytest.raises(ValueError, match="ordered FLiBe species"):
        _density(_trajectory(states[:2] + (changed,)))


def test_density_rejects_nonperiodic_sampling_state() -> None:
    states = _states()
    changed = replace(
        states[2],
        configuration=replace(states[2].configuration, periodic=(True, True, False)),
    )
    with pytest.raises(ValueError, match="three periodic cell axes"):
        _density(_trajectory(states[:2] + (changed,)))


def test_density_rejects_inconsistent_first_state_mass_parameters() -> None:
    states = _states()
    changed = replace(states[0], masses=MASSES[:-1] + (6.0,))
    with pytest.raises(ValueError, match="declared FLiBe species masses"):
        _density(_trajectory((changed,) + states[1:]))


@pytest.mark.parametrize("evidence_kind", tuple(FLiBeEvidenceKind))
def test_direct_reference_residuals_use_independent_fixture(
    evidence_kind: FLiBeEvidenceKind,
) -> None:
    reference = _reference(evidence_kind=evidence_kind)
    comparison = _compare(reference=reference)
    assert comparison.reference is reference
    assert comparison.thermodynamic_state == THERMODYNAMIC_STATE
    assert comparison.residual_kg_m3 == pytest.approx(-12.5, abs=1e-11)
    assert comparison.absolute_residual_kg_m3 == pytest.approx(12.5, abs=1e-11)
    assert comparison.relative_residual == pytest.approx(-12.5 / 700.0, rel=1e-12)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("composition", FLiBeComposition(0.67, 0.33), "compositions must match"),
        ( "thermodynamic_state", FLiBeThermodynamicState(950.0, 0.0),
         "thermodynamic coordinates must match"),
        ( "thermodynamic_state", FLiBeThermodynamicState(1000.0, 101325.0),
         "thermodynamic coordinates must match"),
        ("physical_state_id", "solid", "physical state identifiers must match"),
        ("normalization_id", "mass-over-mean-volume", "normalization must match"),
        ("value_unit", "g/cm^3", "unit must be kg/m\\^3"),
        ("observable_id", "structure_factor", "observable must be mass_density"),
        ("values", (700.0, 710.0), "one scalar density"),
        ("values", (-700.0,), "density must be positive"),
    ),
)
def test_direct_reference_rejects_mismatched_observable_state_or_units(
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _compare(reference=_reference(**{field: value}))


def test_direct_reference_rejects_axis_labeled_sample() -> None:
    with pytest.raises(ValueError, match="one scalar density"):
        _compare(reference=_reference(axis=(1000.0,), axis_unit="K"))


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("thermodynamic_state", FLiBeThermodynamicState(900.0, 0.0),
         "thermodynamic coordinates must match"),
        ("physical_state_id", "solid", "physical state identifiers must match"),
        ("normalization_id", "alternate", "normalization must match"),
    ),
)
def test_direct_reference_rejects_inconsistent_supplied_comparison_coordinates(
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _compare(**{field: value})
