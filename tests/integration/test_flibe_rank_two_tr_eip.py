
"""Independent FLiBe rank-two TR-EIP energy and force correspondence tests.

The shared reference energy, tensor readout, continuous resonance channels,
retained ternary execution, graph-relative coordination and full-energy
coordinate derivatives are checked at typed domain boundaries. Proper and
improper E(3) transformations preserve scalar energy while polar forces
transform covariantly.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.energy.force import ForceState
from tr_eif.energy.rank_two_model import (
    RankTwoChannelEnergyWeights,
    RankTwoConservativeEnergyModel,
    RankTwoConservativeForceEvaluator,
    RankTwoInvariantEnergyReadout,
)
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.equivariant.rank_two import (
    RankTwoFeatureVector,
    RankTwoTensor,
    ScalarVectorTensorFeatures,
)
from tr_eif.equivariant.rank_two_message_passing import RankTwoMessageCoupling
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.rank_two_tr_eip import (
    FLiBeRankTwoTREIPForceResult,
    FLiBeRankTwoTREIPModel,
    FLiBeRankTwoTREIPResult,
)
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_vector_step,
    is_direct_opposite_transition,
)

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0), (1.1, 0.7, 0.8), (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
CUTOFF = 1.6
PROVENANCE = ParameterProvenance.TEST_FIXTURE
TEMPERATURE_PRESSURE = FLiBeThermodynamicState(850.0, 101325.0)
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def _resonance_state() -> ResonanceState:
    return ResonanceState(
        phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
        frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
    )


def _features() -> ScalarVectorTensorFeatures:
    base = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.25 * i,),
            vectors=((1.0, 0.1 * i, -0.05 * i),),
        ) for i in range(7)
    ))
    rank_two = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor((
            (1.0 + 0.1 * i, 0.2, -0.3),
            (0.4, 0.8 - 0.05 * i, 0.1),
            (-0.2, 0.3, 0.6),
        )),
        RankTwoTensor.outer(
            (1.0, 0.25 * i - 0.5, 0.3),
            (0.2, 0.8, -0.1 * i),
        ),
    ) for i in range(7)))
    return ScalarVectorTensorFeatures(base, rank_two)


def _execution() -> TernaryExecutionVector:
    return TernaryExecutionVector(states=(
        TernaryExecutionState(TernaryState.NEGATIVE),
        TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE),
        TernaryExecutionState(TernaryState.POSITIVE),
        TernaryExecutionState(TernaryState.NEGATIVE),
        TernaryExecutionState(TernaryState.NEUTRAL),
        TernaryExecutionState(TernaryState.POSITIVE),
        TernaryExecutionState(TernaryState.NEGATIVE),
    ))


def _model(*, zero_tensor: bool = False) -> FLiBeRankTwoTREIPModel:
    shared = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3), bias=0.1,
        ),
    )
    weights = (
        RankTwoChannelEnergyWeights() if zero_tensor else
        RankTwoChannelEnergyWeights(
            trace=0.15, isotropic_norm_squared=0.08,
            symmetric_traceless_norm_squared=0.3,
            antisymmetric_norm_squared=0.2,
        ),
        RankTwoChannelEnergyWeights() if zero_tensor else
        RankTwoChannelEnergyWeights(
            trace=-0.12, isotropic_norm_squared=0.05,
            symmetric_traceless_norm_squared=-0.08,
            antisymmetric_norm_squared=0.1,
        ),
    )
    return FLiBeRankTwoTREIPModel(
        tr_eip_model=FLiBeTREIPModel(shared, PROVENANCE),
        rank_two_model=RankTwoConservativeEnergyModel(
            reference_model=shared,
            tensor_readout=RankTwoInvariantEnergyReadout(weights),
            coupling=RankTwoMessageCoupling(
                tensor_scale=0.7,
                scalar_dyad_scale=0.2,
                vector_dyad_scale=-0.15,
                scalar_channel_index=0,
                vector_channel_index=0,
            ),
        ),
    )


def _context(configuration=None, resonance_state=None, thermodynamic_state=None):
    config = FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES, positions=POSITIONS,
    )) if configuration is None else configuration
    graph = build_cutoff_graph(config.configuration, CUTOFF)
    descriptor = build_flibe_resonance_descriptor(
        configuration=config,
        coordination=build_flibe_coordination_state(config, graph),
        thermodynamic_state=(TEMPERATURE_PRESSURE if thermodynamic_state is None
                             else thermodynamic_state),
        resonance_state=(_resonance_state() if resonance_state is None
                         else resonance_state),
        provenance=PROVENANCE,
    )
    return config, graph, descriptor


def _evaluate(model=None, features=None, execution=None, context=None):
    model = _model() if model is None else model
    features = _features() if features is None else features
    execution = _execution() if execution is None else execution
    config, graph, descriptor = _context() if context is None else context
    return model.evaluate(config, graph, features, descriptor, execution)


def _direct_tensor_contribution(tensor, weights):
    rows = tensor.rows
    trace = sum(rows[i][i] for i in range(3))
    isotropic_norm = trace * trace / 3.0
    symmetric_norm = sum(
        ((rows[i][j] + rows[j][i]) / 2.0
         - (trace / 3.0 if i == j else 0.0)) ** 2
        for i in range(3) for j in range(3)
    )
    antisymmetric_norm = sum(
        ((rows[i][j] - rows[j][i]) / 2.0) ** 2
        for i in range(3) for j in range(3)
    )
    return fsum((
        weights.trace * trace,
        weights.isotropic_norm_squared * isotropic_norm,
        weights.symmetric_traceless_norm_squared * symmetric_norm,
        weights.antisymmetric_norm_squared * antisymmetric_norm,
    ))


def _force_evaluator(step=1.0e-5):
    return RankTwoConservativeForceEvaluator(CoordinateDifferentiation(step=step))


def _shift_configuration(configuration, atom, axis, amount):
    positions = list(configuration.configuration.positions)
    changed = list(positions[atom])
    changed[axis] += amount
    positions[atom] = tuple(changed)
    return FLiBeConfiguration(AtomicConfiguration(
        species=configuration.species,
        positions=tuple(positions),
        cell=configuration.configuration.cell,
        periodic=configuration.configuration.periodic,
    ))


def test_reference_and_extended_models_share_exact_energy_and_layer():
    model = _model()
    config, graph, descriptor = _context()
    features, execution = _features(), _execution()
    actual = _evaluate(model, features, execution, (config, graph, descriptor))
    baseline = model.tr_eip_model.evaluate(
        config, graph, features.base, descriptor, execution,
    )
    assert isinstance(actual, FLiBeRankTwoTREIPResult)
    assert model.rank_two_model.reference_model is model.tr_eip_model.energy_model
    assert actual.reference_result == baseline
    assert actual.reference_energy == baseline.energy_result.energy
    assert actual.augmented_result.reference_energy == actual.reference_energy
    assert actual.augmented_result.layer.base_layer == baseline.energy_result.layer_result
    assert actual.resonance_features.base == baseline.resonance_conditioned_features
    assert actual.resonance_features.rank_two == features.rank_two
    assert actual.input_features == features
    assert actual.configuration == config and actual.graph == graph
    assert actual.execution == execution and actual.resonance == descriptor
    assert actual.energy == actual.augmented_result.energy


def test_tensor_energy_is_independently_reconstructed_from_cartesian_components():
    model = _model()
    result = _evaluate(model)
    expected = tuple(
        fsum(_direct_tensor_contribution(tensor, weights)
             for tensor, weights in zip(channels,
                                        model.rank_two_model.tensor_readout.channel_weights,
                                        strict=True))
        for channels in result.augmented_result.layer.current.rank_two.nodes
    )
    assert result.tensor_energy.atomic_energies == pytest.approx(expected, rel=1e-12)
    assert result.tensor_energy.total_energy == pytest.approx(sum(expected), rel=1e-12)
    assert abs(result.tensor_energy.total_energy) > 1e-7
    for base, tensor, total in zip(
        result.reference_energy.atomic_energies,
        result.tensor_energy.atomic_energies,
        result.energy.atomic_energies, strict=True,
    ):
        assert total == fsum((base, tensor))
    assert result.energy.total_energy == sum(result.energy.atomic_energies)


def test_zero_tensor_readout_restores_original_tr_eip_energy_and_forces():
    model = _model(zero_tensor=True)
    config, graph, descriptor = _context()
    features, execution = _features(), _execution()
    output = model.evaluate(config, graph, features, descriptor, execution)
    assert output.energy == output.reference_energy
    assert output.tensor_energy.atomic_energies == (0.0,) * 7
    extended_force = model.evaluate_forces(
        config, graph, features, descriptor, execution, _force_evaluator(),
    )
    baseline = model.rank_two_model.reference_model
    from tr_eif.energy import ConservativeForceEvaluator
    reference_forces = ConservativeForceEvaluator(
        CoordinateDifferentiation(step=1.0e-5)
    ).evaluate(
        baseline, config.configuration, graph,
        output.resonance_features.base, execution,
    )
    for actual, expected in zip(extended_force.forces.forces,
                                reference_forces.forces, strict=True):
        assert actual == pytest.approx(expected, rel=1e-6, abs=1e-6)


def test_forces_are_gradients_of_complete_domain_energy():
    model = _model()
    config, graph, descriptor = _context()
    features, execution = _features(), _execution()
    output = model.evaluate_forces(
        config, graph, features, descriptor, execution, _force_evaluator(),
    )
    assert isinstance(output, FLiBeRankTwoTREIPForceResult)
    assert output.evaluation == model.evaluate(config, graph, features, descriptor, execution)
    assert output.forces.atom_count == len(SPECIES)
    independent_step = 2.5e-5
    for atom in (0, 2, 5):
        for axis in (0, 1, 2):
            trial_energies = []
            for sign in (1.0, -1.0):
                trial = _shift_configuration(config, atom, axis, sign * independent_step)
                trial_descriptor = build_flibe_resonance_descriptor(
                    configuration=trial,
                    coordination=build_flibe_coordination_state(trial, graph),
                    thermodynamic_state=descriptor.thermodynamic_state,
                    resonance_state=descriptor.resonance_state,
                    provenance=PROVENANCE,
                )
                trial_energies.append(model.evaluate(
                    trial, graph, features, trial_descriptor, execution,
                ).energy.total_energy)
            independent = -(trial_energies[0] - trial_energies[1]) / (2 * independent_step)
            assert output.forces.forces[atom][axis] == pytest.approx(
                independent, rel=5e-4, abs=5e-5,
            )
    assert all(isfinite(v) for force in output.forces.forces for v in force)


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (2.0, -3.0, 1.0)),
    (REFLECTION, (-1.0, 0.7, 2.0)),
))
def test_e3_invariant_energies_and_covariant_forces(matrix, translation):
    transform = E3Transformation(matrix, translation)
    config, graph, descriptor = _context()
    features, execution = _features(), _execution()
    model = _model()
    baseline = model.evaluate_forces(
        config, graph, features, descriptor, execution, _force_evaluator(),
    )
    transformed_config = FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES,
        positions=tuple(transform.transform_position(p)
                        for p in config.configuration.positions),
    ))
    transformed_context = _context(
        transformed_config, resonance_state=descriptor.resonance_state,
        thermodynamic_state=descriptor.thermodynamic_state,
    )
    transformed = model.evaluate_forces(
        transformed_context[0], transformed_context[1],
        features.transformed(transform), transformed_context[2],
        execution, _force_evaluator(),
    )
    for label in ("reference_energy", "tensor_energy", "energy"):
        a = getattr(baseline.evaluation, label)
        b = getattr(transformed.evaluation, label)
        assert b.total_energy == pytest.approx(a.total_energy, rel=1e-11, abs=1e-9)
        assert b.atomic_energies == pytest.approx(a.atomic_energies, rel=1e-11, abs=1e-9)
    for original, changed in zip(baseline.forces.forces,
                                 transformed.forces.forces, strict=True):
        assert changed == pytest.approx(transform.transform_vector(original),
                                        rel=1e-4, abs=2e-5)
    assert transformed.evaluation.execution == execution
    assert transformed.evaluation.resonance.coordinate == pytest.approx(descriptor.coordinate)


def test_active_neutral_pending_does_not_change_energy_conditioning():
    pending = _execution()
    ordinary = TernaryExecutionVector(states=(
        pending.states[0],
        TernaryExecutionState(TernaryState.NEUTRAL),
        *pending.states[2:],
    ))
    a = _evaluate(execution=pending)
    b = _evaluate(execution=ordinary)
    assert a.reference_energy == b.reference_energy
    assert a.tensor_energy == b.tensor_energy
    assert a.energy == b.energy
    assert a.augmented_result.layer.current == b.augmented_result.layer.current
    assert a.execution.has_pending_targets
    assert not b.execution.has_pending_targets


@pytest.mark.parametrize("start,target", (
    (TernaryState.NEGATIVE, TernaryState.POSITIVE),
    (TernaryState.POSITIVE, TernaryState.NEGATIVE),
))
def test_opposite_requests_route_via_two_separate_neutral_events(start, target):
    original = TernaryExecutionVector.from_retained_states((start,) * 7)
    entry = execute_ternary_vector_step(original, requested_targets=(target,) * 7)
    assert entry.current.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(node.pending_target is target for node in entry.current.states)
    exit_step = execute_ternary_vector_step(entry.current)
    assert exit_step.current.retained_states == (target,) * 7
    assert not exit_step.current.has_pending_targets
    for stage in (entry, exit_step):
        assert stage.committed_count == 7
        assert all(not is_direct_opposite_transition(
            node.route.transition.source, node.route.transition.target,
        ) for node in stage.node_steps if node.route is not None)
    energies = tuple(_evaluate(execution=execution).energy.atomic_energies
                     for execution in (original, entry.current, exit_step.current))
    assert any(abs(x - y) > 1e-8 for x, y in zip(energies[0], energies[1], strict=True))
    assert any(abs(x - y) > 1e-8 for x, y in zip(energies[1], energies[2], strict=True))


def test_resonance_change_reaches_scalar_energy_without_implicit_tensor_mix():
    model = _model()
    config, graph, initial = _context()
    changed_phases = ResonanceState(
        phases=(0.0, 0.8, 1.5, 2.2, 2.8, 3.4, 4.0),
        frequencies=initial.resonance_state.frequencies,
    )
    next_context = _context(config, resonance_state=changed_phases)
    a = _evaluate(model=model, context=(config, graph, initial))
    b = _evaluate(model=model, context=(config, graph, next_context[2]))
    assert a.resonance.coordinate != b.resonance.coordinate
    assert a.reference_energy != b.reference_energy
    assert a.tensor_energy == b.tensor_energy
    assert a.energy != b.energy
    assert a.resonance_features.base.scalar_channel_count == 3
    for node_before, node_after in zip(a.resonance_features.base.nodes,
                                       b.resonance_features.base.nodes, strict=True):
        assert node_before.scalars[0] == node_after.scalars[0]
        assert node_before.scalars[-2:] != node_after.scalars[-2:]


def test_thermodynamic_context_is_retained_without_relabeling_oscillators():
    config, graph, first = _context()
    second = _context(config, thermodynamic_state=FLiBeThermodynamicState(900.0, 202650.0))
    a = _evaluate(context=(config, graph, first))
    b = _evaluate(context=(config, graph, second[2]))
    assert a.resonance.thermodynamic_state != b.resonance.thermodynamic_state
    assert a.resonance.coordinate == b.resonance.coordinate
    assert a.reference_energy == b.reference_energy
    assert a.tensor_energy == b.tensor_energy
    assert a.energy == b.energy


def test_shared_energy_model_identity_is_enforced():
    model = _model()
    independent_copy = replace(model.tr_eip_model.energy_model)
    assert independent_copy == model.tr_eip_model.energy_model
    assert independent_copy is not model.tr_eip_model.energy_model
    with pytest.raises(ValueError, match="share one ReferenceEnergyModel instance"):
        replace(model, rank_two_model=replace(
            model.rank_two_model, reference_model=independent_copy,
        ))


@pytest.mark.parametrize("field", ("configuration", "graph", "features", "resonance", "execution"))
def test_untyped_domain_inputs_are_rejected(field):
    config, graph, descriptor = _context()
    values = dict(configuration=config, graph=graph, features=_features(),
                  resonance=descriptor, execution=_execution())
    values[field] = None
    with pytest.raises(TypeError):
        _model().evaluate(**values)


def test_resonance_and_configuration_must_refer_to_same_geometry():
    config, graph, descriptor = _context()
    translated = FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES,
        positions=tuple((p[0] + 0.25, p[1], p[2]) for p in POSITIONS),
    ))
    with pytest.raises(ValueError, match="resonance and energy evaluation configurations differ"):
        _model().evaluate(translated, graph, _features(), descriptor, _execution())


def test_tensor_channel_count_and_mismatched_node_count_are_rejected():
    model = _model()
    config, graph, descriptor = _context()
    one_channel = replace(
        model.rank_two_model,
        tensor_readout=RankTwoInvariantEnergyReadout((RankTwoChannelEnergyWeights(),)),
    )
    with pytest.raises(ValueError, match="channel counts"):
        replace(model, rank_two_model=one_channel).evaluate(
            config, graph, _features(), descriptor, _execution(),
        )
    one_node = TernaryExecutionVector.from_retained_states((TernaryState.NEUTRAL,))
    with pytest.raises(ValueError, match="atom counts differ"):
        model.evaluate(config, graph, _features(), descriptor, one_node)


def test_force_result_type_and_size_contracts_are_checked():
    model = _model()
    config, graph, descriptor = _context()
    result = model.evaluate_forces(config, graph, _features(), descriptor,
                                   _execution(), _force_evaluator())
    with pytest.raises(TypeError, match="forces must be ForceState"):
        replace(result, forces=None)
    with pytest.raises(TypeError, match="differentiation must be CoordinateDifferentiation"):
        replace(result, differentiation=None)
    with pytest.raises(ValueError, match="force and FLiBe configuration atom counts differ"):
        replace(result, forces=ForceState(((0.0, 0.0, 0.0),)))
    with pytest.raises(TypeError, match="force_evaluator"):
        model.evaluate_forces(config, graph, _features(), descriptor, _execution(), None)


def test_result_detects_incompatible_resonance_features_and_is_immutable():
    result = _evaluate()
    with pytest.raises(ValueError, match="resonance-augmented scalar/vector channels differ"):
        replace(result, resonance_features=result.input_features)
    with pytest.raises(TypeError, match="augmented_result"):
        replace(result, augmented_result=None)
    with pytest.raises(FrozenInstanceError):
        result.reference_result = None
    with pytest.raises(FrozenInstanceError):
        result.energy.total_energy = 0.0


def test_deterministic_replay_preserves_energy_and_forces():
    model = _model()
    config, graph, descriptor = _context()
    features, execution = _features(), _execution()
    first = model.evaluate_forces(config, graph, features, descriptor, execution, _force_evaluator())
    second = model.evaluate_forces(config, graph, features, descriptor, execution, _force_evaluator())
    assert first == second and first is not second
    assert first.evaluation.energy == second.evaluation.energy
    assert first.forces == second.forces
