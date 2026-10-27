"""Independent tensor, frame, and provenance tests for FLiBe MD pressure."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
    ConservativeStressEvaluator,
    ForceState,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
    StressState,
)
from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_pressure import (
    FLiBePotentialStressSample,
    FLiBeTrajectoryPressure,
    FLiBeVelocityFrame,
    evaluate_flibe_trajectory_pressure,
)
from tr_eif.flibe.trajectory_state_correspondence import (
    FLiBeDensitySourceCoordinates,
    FLiBePressureRole,
    compare_flibe_density_state_coordinates,
    evaluate_flibe_trajectory_state_coordinates,
)
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.equivariant import (
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.graph import InteractionGraph, build_cutoff_graph
from tr_eif.ternary import TernaryExecutionVector, TernaryState
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory


SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
POSITIONS = (
    (0.1, 0.1, 0.1), (0.6, 0.1, 0.1), (0.2, 0.6, 0.2),
    (0.3, 0.3, 0.7), (0.8, 0.3, 0.7), (0.4, 0.9, 1.1),
    (0.9, 0.7, 1.3),
)

# All three components of the mass-weighted total momentum vanish.
# Independently summed mass-weighted velocity products are:
# [[4, 8, 0], [8, 20.8, 0], [0, 0, 40]].
VELOCITIES = (
    (1.0, 2.0, 0.0), (-1.0, -2.0, 0.0), (0.0, 1.0, 0.0),
    (0.0, -0.6, 0.0), (0.0, 0.0, 2.0), (0.0, 0.0, -2.0),
    (0.0, 0.0, 0.0),
)
POTENTIAL_STRESS = (
    (1.5, 0.25, 0.0),
    (0.25, -0.5, 0.0),
    (0.0, 0.0, 2.0),
)
MASS_UNIT_KG = 1.0e-27
LENGTH_UNIT_M = 1.0e-10
TIME_UNIT_S = 1.0e-12
STRESS_UNIT_PA = 1.0e5
PROVENANCE = ParameterProvenance.TEST_FIXTURE
MOMENT = ((4.0, 8.0, 0.0), (8.0, 20.8, 0.0), (0.0, 0.0, 40.0))


def _cell(index: int):
    return ((2.0 * (index + 1), 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0))


def _state(
    index: int,
    *,
    velocities=VELOCITIES,
    cell=None,
    positions=POSITIONS,
) -> MolecularDynamicsState:
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=positions,
            cell=_cell(index) if cell is None else cell,
            periodic=(True, True, True),
        ),
        velocities=velocities,
        masses=MASSES,
        step=index,
        time=0.25 * index,
    )


def _trajectory(states=None) -> MolecularDynamicsTrajectory:
    sequence = tuple(_state(i) for i in range(3)) if states is None else states
    graph = InteractionGraph(node_count=len(SPECIES), edges=())
    zero_forces = ForceState(forces=((0.0, 0.0, 0.0),) * len(SPECIES))
    return MolecularDynamicsTrajectory(
        steps=tuple(
            MolecularDynamicsStepResult(
                previous=previous,
                current=current,
                graph_before=graph,
                graph_after=graph,
                forces_before=zero_forces,
                forces_after=zero_forces,
            )
            for previous, current in zip(sequence[:-1], sequence[1:], strict=True)
        )
    )


def _density(trajectory: MolecularDynamicsTrajectory, **changes):
    args = dict(
        trajectory=trajectory,
        mass_parameters=FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        model_id="TR-EIP-PRESSURE-FIXTURE",
        trajectory_id="TRAJECTORY-PRESSURE-001",
        provenance=PROVENANCE,
        mass_unit_to_kg=MASS_UNIT_KG,
        coordinate_unit_to_meter=LENGTH_UNIT_M,
    )
    args.update(changes)
    return evaluate_flibe_trajectory_density(**args)


def _stresses(density, tensor=POTENTIAL_STRESS):
    return tuple(
        FLiBePotentialStressSample(
            state_index=sample.state_index,
            md_step=sample.md_step,
            md_time=sample.md_time,
            stress=StressState(tensor=tensor),
        )
        for sample in density.samples
    )


def _evaluate(
    trajectory=None, density=None, stresses=None, **changes
) -> FLiBeTrajectoryPressure:
    current = _trajectory() if trajectory is None else trajectory
    selected = _density(current) if density is None else density
    args = dict(
        trajectory=current,
        density_trace=selected,
        potential_stresses=_stresses(selected) if stresses is None else stresses,
        time_unit_to_second=TIME_UNIT_S,
        potential_stress_unit_to_pascal=STRESS_UNIT_PA,
        velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
        stress_method_id="ENERGY-STRAIN-FIXTURE",
        source_id="INDEPENDENT-PRESSURE-FIXTURE",
        provenance=PROVENANCE,
    )
    args.update(changes)
    return evaluate_flibe_trajectory_pressure(**args)


def _expected_tensor(cell_volume_units: float):
    # Independent analytic moment tensor; one mass-velocity-product unit
    # corresponds to 1e7 / cell_volume_units pascal under the selected units.
    scale_pa = 1.0e7 / cell_volume_units
    return tuple(
        tuple(MOMENT[i][j] * scale_pa - POTENTIAL_STRESS[i][j] * STRESS_UNIT_PA
              for j in range(3))
        for i in range(3)
    )


def _assert_tensor(actual, expected):
    for i in range(3):
        assert actual[i] == pytest.approx(expected[i], rel=1e-12, abs=1e-7)


def test_analytic_kinetic_configurational_and_total_pressure_tensor() -> None:
    result = _evaluate()
    first = result.samples[0]
    assert first.state_index == first.md_step == 0
    assert first.md_time == 0.0
    assert first.cell_volume_m3 == pytest.approx(24.0e-30, rel=1e-13)
    assert result.density_trace.total_mass_kg == pytest.approx(27.0e-27)
    kinetic_scale = 1.0e7 / 24.0
    for i in range(3):
        assert first.kinetic_tensor_pa[i] == pytest.approx(
            tuple(value * kinetic_scale for value in MOMENT[i]), rel=1e-12, abs=1e-7
        )
        assert first.configurational_tensor_pa[i] == pytest.approx(
            tuple(-value * STRESS_UNIT_PA for value in POTENTIAL_STRESS[i])
        )
    _assert_tensor(first.pressure_tensor_pa, _expected_tensor(24.0))
    assert first.pressure_tensor_pa[0][1] == pytest.approx(
        8.0 * kinetic_scale - 0.25 * STRESS_UNIT_PA
    )
    assert first.pressure_tensor_pa[1][0] == pytest.approx(first.pressure_tensor_pa[0][1])
    assert first.scalar_pressure_pa == pytest.approx(
        (64.8 * kinetic_scale - 3.0 * STRESS_UNIT_PA) / 3.0
    )


def test_frame_identity_sampling_and_arithmetic_pressure_average() -> None:
    trajectory = _trajectory()
    density = _density(trajectory, first_state_index=0, stride=2)
    result = _evaluate(trajectory, density)
    assert tuple(sample.state_index for sample in result.samples) == (0, 2)
    assert tuple(sample.md_step for sample in result.samples) == (0, 2)
    assert tuple(sample.md_time for sample in result.samples) == (0.0, 0.5)
    assert tuple(sample.cell_volume_m3 for sample in result.samples) == pytest.approx(
        (24.0e-30, 72.0e-30), rel=1e-13
    )
    _assert_tensor(result.samples[0].pressure_tensor_pa, _expected_tensor(24.0))
    _assert_tensor(result.samples[1].pressure_tensor_pa, _expected_tensor(72.0))
    expected_average = tuple(
        tuple((_expected_tensor(24.0)[i][j] + _expected_tensor(72.0)[i][j]) / 2.0
              for j in range(3))
        for i in range(3)
    )
    _assert_tensor(result.mean_pressure_tensor_pa, expected_average)
    assert result.mean_pressure_pa == pytest.approx(
        (result.samples[0].scalar_pressure_pa + result.samples[1].scalar_pressure_pa) / 2.0
    )
    assert result.mean_pressure_pa == pytest.approx(
        sum(expected_average[i][i] for i in range(3)) / 3.0
    )


def test_center_of_mass_removes_uniform_velocity_boost() -> None:
    boost = (3.0, -4.0, 7.0)
    shifted_velocities = tuple(
        tuple(v[i] + boost[i] for i in range(3)) for v in VELOCITIES
    )
    shifted = _trajectory(tuple(_state(i, velocities=shifted_velocities) for i in range(3)))
    baseline = _evaluate()
    com = _evaluate(shifted, velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS)
    lab = _evaluate(shifted, velocity_frame=FLiBeVelocityFrame.LABORATORY)
    for before, after in zip(baseline.samples, com.samples, strict=True):
        _assert_tensor(after.pressure_tensor_pa, before.pressure_tensor_pa)
        assert after.scalar_pressure_pa == pytest.approx(before.scalar_pressure_pa)
    # Original total momentum is zero, and the boost adds M b_a b_b / V.
    scale = 27.0 * 1.0e7 / 24.0
    assert lab.samples[0].pressure_tensor_pa[0][1] - baseline.samples[0].pressure_tensor_pa[0][1] == pytest.approx(
        scale * boost[0] * boost[1]
    )
    assert lab.samples[0].scalar_pressure_pa - baseline.samples[0].scalar_pressure_pa == pytest.approx(
        scale * sum(value * value for value in boost) / 3.0
    )


def test_temperature_and_pressure_velocity_conventions_remain_explicit() -> None:
    boost = (3.0, -4.0, 7.0)
    shifted = tuple(
        tuple(v[i] + boost[i] for i in range(3)) for v in VELOCITIES
    )
    reference_trajectory = _trajectory()
    boosted_trajectory = _trajectory(tuple(_state(i, velocities=shifted) for i in range(3)))
    reference_pressure = _evaluate(reference_trajectory)
    boosted_pressure = _evaluate(
        boosted_trajectory, velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS
    )
    assert boosted_pressure.mean_pressure_pa == pytest.approx(reference_pressure.mean_pressure_pa)

    reference_temperature = evaluate_flibe_trajectory_state_coordinates(
        reference_trajectory, _density(reference_trajectory),
        degrees_of_freedom=21, time_unit_to_second=TIME_UNIT_S,
        physical_state_id="liquid", physical_state_method_id="KINETIC-LAB-FIXTURE",
    ).mean_kinetic_temperature_k
    boosted_temperature = evaluate_flibe_trajectory_state_coordinates(
        boosted_trajectory, _density(boosted_trajectory),
        degrees_of_freedom=21, time_unit_to_second=TIME_UNIT_S,
        physical_state_id="liquid", physical_state_method_id="KINETIC-LAB-FIXTURE",
    ).mean_kinetic_temperature_k
    expected_increment = (
        27.0 * MASS_UNIT_KG * (LENGTH_UNIT_M / TIME_UNIT_S) ** 2
        * sum(value * value for value in boost) / (21.0 * 1.380649e-23)
    )
    assert boosted_temperature - reference_temperature == pytest.approx(expected_increment)


def test_cartesian_quarter_turn_preserves_scalar_pressure_and_rotates_tensor() -> None:
    # Q maps (x, y, z) to (-y, x, z).
    def q(vector):
        return (-vector[1], vector[0], vector[2])

    def rotate_tensor(tensor):
        return (
            (tensor[1][1], -tensor[1][0], -tensor[1][2]),
            (-tensor[0][1], tensor[0][0], tensor[0][2]),
            (-tensor[2][1], tensor[2][0], tensor[2][2]),
        )

    rotated_states = tuple(
        _state(
            index,
            velocities=tuple(q(v) for v in VELOCITIES),
            positions=tuple(q(position) for position in POSITIONS),
            cell=tuple(q(edge) for edge in _cell(index)),
        )
        for index in range(3)
    )
    trajectory = _trajectory(rotated_states)
    density = _density(trajectory)
    rotated_stress = tuple(
        FLiBePotentialStressSample(
            state_index=sample.state_index,
            md_step=sample.md_step,
            md_time=sample.md_time,
            stress=StressState(tensor=rotate_tensor(POTENTIAL_STRESS)),
        )
        for sample in density.samples
    )
    original = _evaluate()
    rotated = _evaluate(trajectory, density, rotated_stress)
    for before, after in zip(original.samples, rotated.samples, strict=True):
        _assert_tensor(after.pressure_tensor_pa, rotate_tensor(before.pressure_tensor_pa))
        assert after.scalar_pressure_pa == pytest.approx(before.scalar_pressure_pa)


def test_pressure_consumes_actual_energy_strain_derivative() -> None:
    trajectory = _trajectory()
    density = _density(trajectory, stride=3)
    configuration = trajectory.initial.configuration
    graph = build_cutoff_graph(configuration, cutoff=0.5)
    features = NodeFeatureVector(
        nodes=tuple(NodeFeatures(scalars=(1.0,)) for _ in SPECIES)
    )
    execution = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL,) * len(SPECIES)
    )
    model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.0),
        conditioning=TernaryConditioning(
            negative_scale=1.0, neutral_scale=1.0, positive_scale=1.0
        ),
        energy_functional=LinearInvariantEnergyFunctional(weights=(1.0,), bias=0.0),
    )
    h = 1.0e-6
    energy_stress = ConservativeStressEvaluator(
        differentiation=CellStrainDifferentiation(step=h)
    ).evaluate(model, configuration, graph, features, execution)

    def strained(factor: float) -> AtomicConfiguration:
        return replace(
            configuration,
            positions=tuple((x * factor, y, z) for x, y, z in POSITIONS),
            cell=tuple((x * factor, y, z) for x, y, z in configuration.cell),
        )

    direct_derivative = (
        model.evaluate(strained(1.0 + h), graph, features, execution).energy.total_energy
        - model.evaluate(strained(1.0 - h), graph, features, execution).energy.total_energy
    ) / (2.0 * h * 24.0)
    assert direct_derivative != pytest.approx(0.0, abs=1e-8)
    assert energy_stress.tensor[0][0] == pytest.approx(direct_derivative, abs=1e-9)
    assert energy_stress.is_symmetric
    stresses = _stresses(density, tensor=energy_stress.tensor)
    pressure = _evaluate(trajectory, density, stresses)
    assert len(pressure.samples) == 1
    assert pressure.samples[0].configurational_tensor_pa[0][0] == pytest.approx(
        -direct_derivative * STRESS_UNIT_PA, abs=1e-4
    )
    assert pressure.samples[0].pressure_tensor_pa[0][0] == pytest.approx(
        4.0 * (1.0e7 / 24.0) - direct_derivative * STRESS_UNIT_PA, abs=1e-4
    )


def test_negative_pressure_is_preserved_and_incompatible_coordinate_is_rejected() -> None:
    rest = ((0.0, 0.0, 0.0),) * len(SPECIES)
    trajectory = _trajectory(tuple(_state(i, velocities=rest) for i in range(3)))
    result = _evaluate(trajectory)
    for sample in result.samples:
        assert sample.kinetic_tensor_pa == ((0.0, 0.0, 0.0),) * 3
        assert sample.scalar_pressure_pa == pytest.approx(-100000.0)
    assert result.mean_pressure_pa == pytest.approx(-100000.0)
    with pytest.raises(ValueError, match="requires nonnegative pressure"):
        result.to_observed_pressure_coordinate()


def test_computed_positive_pressure_integrates_with_state_correspondence() -> None:
    trajectory = _trajectory()
    density = _density(trajectory)
    pressure = _evaluate(trajectory, density).to_observed_pressure_coordinate()
    assert pressure.role is FLiBePressureRole.OBSERVED
    assert pressure.provenance is PROVENANCE
    assert pressure.source_id == "INDEPENDENT-PRESSURE-FIXTURE"
    assert pressure.method_id == "ENERGY-STRAIN-FIXTURE"
    model = evaluate_flibe_trajectory_state_coordinates(
        trajectory, density,
        degrees_of_freedom=21,
        time_unit_to_second=TIME_UNIT_S,
        physical_state_id="liquid",
        physical_state_method_id="EXPLICIT-TEST-STATE",
        pressure=pressure,
    )
    # Sum m_i |v_i|^2 = 64.8 in the independent velocity fixture.
    analytic_t = 64.8 * MASS_UNIT_KG * (LENGTH_UNIT_M / TIME_UNIT_S) ** 2 / (
        21.0 * 1.380649e-23
    )
    assert model.mean_kinetic_temperature_k == pytest.approx(analytic_t, rel=1e-12)
    source = FLiBeDensitySourceCoordinates(
        density_kg_m3=700.0,
        composition=FLiBeComposition(2.0, 1.0),
        temperature_k=analytic_t,
        pressure_pa=pressure.pressure_pa,
        physical_state_id="liquid",
        normalization_id="source-reported-mass-density",
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        source_id="SYNTHETIC-PRESSURE-SOURCE",
        method_id="ANALYTIC-FIXTURE",
        provenance=PROVENANCE,
    )
    comparison = compare_flibe_density_state_coordinates(
        model, source,
        temperature_tolerance_k=1e-10,
        pressure_tolerance_pa=1e-6,
        normalization_id="source-reported-mass-density",
    )
    assert comparison.coordinate_match
    assert comparison.density_residual_kg_m3 == pytest.approx(
        (1125.0 + 562.5 + 375.0) / 3.0 - 700.0, abs=1e-10
    )
    changed_pressure = replace(source, pressure_pa=source.pressure_pa + 1000.0)
    comparison = compare_flibe_density_state_coordinates(
        model, changed_pressure,
        temperature_tolerance_k=1e-10,
        pressure_tolerance_pa=1e-6,
        normalization_id="source-reported-mass-density",
    )
    assert not comparison.pressure_match
    assert not comparison.coordinate_match


def test_explicit_units_scale_kinetic_pressure_independently_of_stress() -> None:
    original = _evaluate().samples[0]
    twice_time = _evaluate(time_unit_to_second=2.0 * TIME_UNIT_S).samples[0]
    assert twice_time.kinetic_tensor_pa[0][0] == pytest.approx(
        original.kinetic_tensor_pa[0][0] / 4.0
    )
    assert twice_time.configurational_tensor_pa == original.configurational_tensor_pa
    twice_stress = _evaluate(potential_stress_unit_to_pascal=2.0 * STRESS_UNIT_PA).samples[0]
    assert twice_stress.kinetic_tensor_pa == original.kinetic_tensor_pa
    assert twice_stress.configurational_tensor_pa[0][0] == pytest.approx(
        original.configurational_tensor_pa[0][0] * 2.0
    )
    trajectory = _trajectory()
    twice_mass = _density(trajectory, mass_unit_to_kg=2.0 * MASS_UNIT_KG)
    doubled = _evaluate(trajectory, twice_mass).samples[0]
    assert doubled.kinetic_tensor_pa[0][0] == pytest.approx(
        original.kinetic_tensor_pa[0][0] * 2.0
    )
    doubled_length = _density(trajectory, coordinate_unit_to_meter=2.0 * LENGTH_UNIT_M)
    rescaled = _evaluate(trajectory, doubled_length).samples[0]
    assert rescaled.kinetic_tensor_pa[0][0] == pytest.approx(
        original.kinetic_tensor_pa[0][0] / 2.0
    )


def test_skewed_reversed_cell_preserves_absolute_volume() -> None:
    skew_reversed = ((2.0, 0.0, 0.0), (1.0, 3.0, 0.0), (1.0, 1.0, -4.0))
    trajectory = _trajectory(tuple(_state(i, cell=skew_reversed) for i in range(3)))
    pressure = _evaluate(trajectory)
    assert all(sample.cell_volume_m3 == pytest.approx(24.0e-30) for sample in pressure.samples)
    for sample in pressure.samples:
        _assert_tensor(sample.pressure_tensor_pa, _expected_tensor(24.0))


def test_stress_indices_must_match_selected_density_frames() -> None:
    trajectory = _trajectory()
    density = _density(trajectory, stride=2)
    stresses = _stresses(density)
    assert tuple(s.state_index for s in stresses) == (0, 2)
    assert len(_evaluate(trajectory, density, stresses).samples) == 2
    for changed in (
        replace(stresses[1], state_index=1),
        replace(stresses[1], md_step=1),
        replace(stresses[1], md_time=0.25),
    ):
        with pytest.raises(ValueError, match="state identities"):
            _evaluate(trajectory, density, (stresses[0], changed))
    with pytest.raises(ValueError, match="sample counts"):
        _evaluate(trajectory, density, (stresses[0],))
    with pytest.raises(TypeError, match="FLiBePotentialStressSample"):
        _evaluate(trajectory, density, (stresses[0], object()))


def test_density_and_trajectory_are_revalidated_before_pressure_computation() -> None:
    trajectory = _trajectory()
    density = _density(trajectory)
    altered_density = replace(density, samples=(
        replace(density.samples[0], cell_volume_m3=2.0 * density.samples[0].cell_volume_m3),
        *density.samples[1:],
    ))
    with pytest.raises(ValueError, match="cell volumes must agree"):
        _evaluate(trajectory, altered_density)
    altered_mass = replace(density, total_mass_kg=1.1 * density.total_mass_kg)
    with pytest.raises(ValueError, match="mass inventories must agree"):
        _evaluate(trajectory, altered_mass)
    altered_sample = replace(density.samples[2], state_index=3)
    altered_density = replace(density, samples=(*density.samples[:2], altered_sample))
    with pytest.raises(ValueError, match="state index exceeds"):
        _evaluate(trajectory, altered_density)
    altered_density = replace(density, samples=(
        replace(density.samples[0], density_kg_m3=2.0 * density.samples[0].density_kg_m3),
        *density.samples[1:],
    ))
    with pytest.raises(ValueError, match="sample must match"):
        _evaluate(trajectory, altered_density)


def test_species_mass_and_periodicity_changes_are_detected() -> None:
    original = tuple(_state(i) for i in range(3))
    initial_density = _density(_trajectory())
    swapped = replace(original[2], configuration=replace(
        original[2].configuration, species=("Be", "Li", "Li", "F", "F", "F", "F")
    ))
    with pytest.raises(ValueError, match="ordered species"):
        _evaluate(_trajectory(original[:2] + (swapped,)), initial_density)
    new_masses = replace(original[2], masses=MASSES[:-1] + (6.0,))
    with pytest.raises(ValueError, match="atomic masses"):
        _evaluate(_trajectory(original[:2] + (new_masses,)), initial_density)
    partial_periodic = replace(original[2], configuration=replace(
        original[2].configuration, periodic=(True, True, False)
    ))
    with pytest.raises(ValueError, match="fully periodic"):
        _evaluate(_trajectory(original[:2] + (partial_periodic,)), initial_density)


def test_asymmetric_energy_stress_is_rejected_exactly() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        FLiBePotentialStressSample(
            state_index=0, md_step=0, md_time=0.0,
            stress=StressState(tensor=((1.0, 0.2, 0.0), (0.1, 1.0, 0.0), (0.0, 0.0, 1.0))),
        )


@pytest.mark.parametrize(
    ("field", "value", "error"),
    (
        ("time_unit_to_second", 0.0, ValueError),
        ("time_unit_to_second", float("nan"), ValueError),
        ("time_unit_to_second", False, TypeError),
        ("potential_stress_unit_to_pascal", -1.0, ValueError),
        ("potential_stress_unit_to_pascal", float("inf"), ValueError),
        ("velocity_frame", "CENTER_OF_MASS", TypeError),
        ("stress_method_id", " ", ValueError),
        ("source_id", "bad ", ValueError),
        ("provenance", "TEST_FIXTURE", TypeError),
        ("potential_stresses", [], TypeError),
    ),
)
def test_pressure_operator_rejects_invalid_units_and_metadata(field, value, error) -> None:
    with pytest.raises(error):
        _evaluate(**{field: value})


@pytest.mark.parametrize(
    ("field", "value", "error"),
    (
        ("state_index", -1, ValueError),
        ("state_index", True, ValueError),
        ("md_step", -1, ValueError),
        ("md_time", -0.1, ValueError),
        ("md_time", float("nan"), ValueError),
        ("md_time", False, TypeError),
        ("stress", None, TypeError),
    ),
)
def test_potential_stress_sample_rejects_invalid_coordinates(field, value, error) -> None:
    arguments = dict(state_index=0, md_step=0, md_time=0.0, stress=StressState(POTENTIAL_STRESS))
    arguments[field] = value
    with pytest.raises(error):
        FLiBePotentialStressSample(**arguments)


def test_pressure_sample_enforces_trace_and_tensor_contracts() -> None:
    sample = _evaluate().samples[0]
    with pytest.raises(ValueError, match="one-third tensor trace"):
        replace(sample, scalar_pressure_pa=sample.scalar_pressure_pa + 100.0)
    with pytest.raises(ValueError, match="three tensor rows"):
        replace(sample, pressure_tensor_pa=((1.0, 2.0, 3.0),))
    with pytest.raises(ValueError, match="three components per row"):
        replace(sample, kinetic_tensor_pa=((0.0,), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    with pytest.raises(ValueError, match="finite real components"):
        replace(sample, configurational_tensor_pa=((float("nan"), 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    with pytest.raises(ValueError, match="finite and positive"):
        replace(sample, cell_volume_m3=0.0)
    with pytest.raises(FrozenInstanceError):
        sample.scalar_pressure_pa = 0.0  # type: ignore[misc]


def test_reproducible_immutable_result_preserves_provenance() -> None:
    first = _evaluate()
    second = _evaluate()
    assert first == second
    assert first.provenance is PROVENANCE
    assert first.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS
    assert first.stress_method_id == "ENERGY-STRAIN-FIXTURE"
    assert first.source_id == "INDEPENDENT-PRESSURE-FIXTURE"
    assert len(first.samples) == first.density_trace.sample_count == 3
    with pytest.raises(FrozenInstanceError):
        first.source_id = "changed"  # type: ignore[misc]


def test_constructor_checks_density_sample_alignment_and_tensor_trace() -> None:
    result = _evaluate()
    with pytest.raises(ValueError, match="sample identities must agree"):
        replace(result, samples=(replace(result.samples[0], md_step=99), *result.samples[1:]))
    with pytest.raises(ValueError, match="sample counts must agree"):
        replace(result, samples=result.samples[:-1])
    with pytest.raises(ValueError, match="cell volumes must agree"):
        replace(result, samples=(replace(result.samples[0], cell_volume_m3=1.1 * result.samples[0].cell_volume_m3), *result.samples[1:]))
