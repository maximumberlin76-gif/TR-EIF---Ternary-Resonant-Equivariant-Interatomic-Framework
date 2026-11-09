
"""Independent conservation and E(3) tests for rank-two TR-EIF energy.

Compare tensor contractions against direct Cartesian algebra, derive forces
from a second finite-difference stencil, and inspect retained ternary routing,
resonance channels, and the legacy scalar/vector energy boundary.
"""

from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.energy.rank_two_model import (
    RankTwoChannelEnergyWeights,
    RankTwoConservativeEnergyModel,
    RankTwoConservativeEnergyResult,
    RankTwoConservativeForceEvaluator,
    RankTwoInvariantEnergyReadout,
)
from tr_eif.energy.state import EnergyState
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
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import append_md_resonance_features
from tr_eif.resonance import ResonanceState, resonance_descriptor
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_vector_step,
    is_direct_opposite_transition,
)

CUTOFF = 2.3
DIFFERENCE_STEP = 1.0e-5
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
INVERSION = ((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, -1.0))


def _system():
    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=((0.0, 0.0, 0.0), (1.0, 0.2, 0.0), (0.25, 1.1, 0.35)),
    )
    base = NodeFeatureVector(nodes=(
        NodeFeatures(scalars=(1.1, -0.2), vectors=((1.0, 0.1, -0.3),)),
        NodeFeatures(scalars=(-0.4, 0.6), vectors=((-0.2, 1.0, 0.4),)),
        NodeFeatures(scalars=(0.7, 0.3), vectors=((0.3, -0.5, 1.0),)),
    ))
    tensors = RankTwoFeatureVector(nodes=(
        (
            RankTwoTensor(((1.0, 0.3, -0.2), (0.5, -0.6, 0.4), (0.1, -0.3, 0.8))),
            RankTwoTensor.outer((1.0, -0.5, 0.3), (0.2, 0.8, -0.4)),
        ),
        (
            RankTwoTensor(((0.5, -0.1, 0.4), (0.3, 1.2, -0.6), (0.2, 0.1, -0.7))),
            RankTwoTensor.outer((0.2, 1.0, -0.3), (1.1, 0.4, 0.5)),
        ),
        (
            RankTwoTensor(((-0.8, 0.4, 0.1), (0.2, 0.7, -0.5), (-0.6, 0.3, 1.0))),
            RankTwoTensor.outer((-0.2, 0.6, 1.0), (0.3, -0.7, 0.9)),
        ),
    ))
    execution = TernaryExecutionVector(states=(
        TernaryExecutionState(TernaryState.NEGATIVE),
        TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE),
        TernaryExecutionState(TernaryState.POSITIVE),
    ))
    return configuration, ScalarVectorTensorFeatures(base, tensors), execution


def _model(*, zero_tensor=False, resonance_channels=False):
    reference = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.15),
        conditioning=TernaryConditioning(
            negative_scale=0.6, neutral_scale=1.3, positive_scale=1.8,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=((0.4, -0.2, 0.3, -0.15)
                     if resonance_channels else (0.4, -0.2)),
            bias=0.05,
        ),
    )
    if zero_tensor:
        weights = (RankTwoChannelEnergyWeights(), RankTwoChannelEnergyWeights())
    else:
        weights = (
            RankTwoChannelEnergyWeights(
                trace=0.15, isotropic_norm_squared=0.08,
                symmetric_traceless_norm_squared=0.3,
                antisymmetric_norm_squared=0.2,
            ),
            RankTwoChannelEnergyWeights(
                trace=-0.25, isotropic_norm_squared=0.1,
                symmetric_traceless_norm_squared=-0.08,
                antisymmetric_norm_squared=0.12,
            ),
        )
    return RankTwoConservativeEnergyModel(
        reference_model=reference,
        tensor_readout=RankTwoInvariantEnergyReadout(weights),
        coupling=RankTwoMessageCoupling(
            tensor_scale=0.7, scalar_dyad_scale=0.4,
            vector_dyad_scale=-0.25,
            scalar_channel_index=1, vector_channel_index=0,
        ),
    )


def _evaluate(model, configuration, features, execution):
    graph = build_cutoff_graph(configuration, CUTOFF)
    return model.evaluate(configuration, graph, features, execution)


def _independent_contraction(tensor, weights):
    """Compute the three irreducible Cartesian norms without model helpers."""
    t = tensor.rows
    tr = sum(t[i][i] for i in range(3))
    iso = tr * tr / 3.0
    symmetric = sum(
        ((t[i][j] + t[j][i]) / 2.0 - (tr / 3.0 if i == j else 0.0)) ** 2
        for i in range(3) for j in range(3)
    )
    antisymmetric = sum(
        ((t[i][j] - t[j][i]) / 2.0) ** 2
        for i in range(3) for j in range(3)
    )
    return fsum((
        weights.trace * tr,
        weights.isotropic_norm_squared * iso,
        weights.symmetric_traceless_norm_squared * symmetric,
        weights.antisymmetric_norm_squared * antisymmetric,
    ))


def _shift(configuration, atom, axis, displacement):
    positions = list(configuration.positions)
    position = list(positions[atom])
    position[axis] += displacement
    positions[atom] = tuple(position)
    return AtomicConfiguration(
        species=configuration.species, positions=tuple(positions),
        cell=configuration.cell, periodic=configuration.periodic,
    )


def _transform_configuration(configuration, transform):
    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(transform.transform_position(p) for p in configuration.positions),
    )


def _forces(model, configuration, features, execution, *, step=DIFFERENCE_STEP):
    return RankTwoConservativeForceEvaluator(
        CoordinateDifferentiation(step=step)
    ).evaluate(
        model, configuration, build_cutoff_graph(configuration, CUTOFF),
        features, execution,
    )


def test_energy_matches_independent_rank_two_contractions_and_legacy_layer():
    configuration, features, execution = _system()
    model = _model()
    actual = _evaluate(model, configuration, features, execution)
    assert isinstance(actual, RankTwoConservativeEnergyResult)
    assert actual.layer.current.node_count == len(configuration.species)
    assert actual.layer.current.rank_two.tensor_channel_count == 2
    legacy = model.reference_model.evaluate(
        configuration, build_cutoff_graph(configuration, CUTOFF),
        features.base, execution,
    )
    assert actual.reference_energy == legacy.energy
    assert actual.layer.base_layer.current == legacy.layer_result.current
    independent = tuple(
        fsum(_independent_contraction(tensor, weight)
             for tensor, weight in zip(node, model.tensor_readout.channel_weights, strict=True))
        for node in actual.layer.current.rank_two.nodes
    )
    assert actual.tensor_energy.atomic_energies == pytest.approx(independent, abs=1e-12)
    assert actual.tensor_energy.total_energy == pytest.approx(sum(independent), abs=1e-12)
    for a, b, total in zip(
        actual.reference_energy.atomic_energies,
        actual.tensor_energy.atomic_energies,
        actual.energy.atomic_energies, strict=True,
    ):
        assert total == fsum((a, b))
    assert actual.energy.total_energy == sum(actual.energy.atomic_energies)
    assert abs(actual.tensor_energy.total_energy) > 1e-5


def test_readout_invariant_decomposition_is_independently_reproduced():
    _, features, _ = _system()
    weights = _model().tensor_readout.channel_weights
    readout = RankTwoInvariantEnergyReadout(weights)
    result = readout.evaluate(features.rank_two)
    expected = tuple(
        fsum(_independent_contraction(tensor, weight)
             for tensor, weight in zip(channels, weights, strict=True))
        for channels in features.rank_two.nodes
    )
    assert result.atomic_energies == pytest.approx(expected, abs=1e-12)
    assert result.total_energy == pytest.approx(sum(expected), abs=1e-12)


def test_zero_tensor_weights_restore_reference_energy_and_forces():
    configuration, features, execution = _system()
    model = _model(zero_tensor=True)
    graph = build_cutoff_graph(configuration, CUTOFF)
    result = model.evaluate(configuration, graph, features, execution)
    baseline = model.reference_model.evaluate(configuration, graph, features.base, execution)
    assert result.energy == result.reference_energy == baseline.energy
    assert result.tensor_energy.atomic_energies == (0.0,) * 3
    combined = _forces(model, configuration, features, execution)
    reference = ConservativeForceEvaluator(
        CoordinateDifferentiation(step=DIFFERENCE_STEP)
    ).evaluate(model.reference_model, configuration, graph, features.base, execution)
    for actual, expected in zip(combined.forces, reference.forces, strict=True):
        assert actual == pytest.approx(expected, rel=1e-8, abs=1e-7)


def test_complete_force_matches_independent_wider_energy_gradient():
    configuration, features, execution = _system()
    model = _model()
    evaluated = _forces(model, configuration, features, execution)
    graph = build_cutoff_graph(configuration, CUTOFF)
    h = 2.5 * DIFFERENCE_STEP
    for atom, force in enumerate(evaluated.forces):
        for axis, actual in enumerate(force):
            plus = model.evaluate(
                _shift(configuration, atom, axis, h), graph, features, execution
            ).energy.total_energy
            minus = model.evaluate(
                _shift(configuration, atom, axis, -h), graph, features, execution
            ).energy.total_energy
            independent = -(plus - minus) / (2.0 * h)
            assert actual == pytest.approx(independent, rel=2e-4, abs=3e-6)
    assert evaluated.atom_count == len(configuration.species)
    assert all(isfinite(v) for vector in evaluated.forces for v in vector)


def test_tensor_channel_adds_nontrivial_coordinate_force():
    configuration, features, execution = _system()
    combined = _forces(_model(), configuration, features, execution)
    baseline = _forces(_model(zero_tensor=True), configuration, features, execution)
    assert any(
        abs(a - b) > 1e-5
        for f, g in zip(combined.forces, baseline.forces, strict=True)
        for a, b in zip(f, g, strict=True)
    )


def test_total_internal_force_sums_to_zero_for_translation_invariant_energy():
    configuration, features, execution = _system()
    result = _forces(_model(), configuration, features, execution)
    assert tuple(fsum(f[axis] for f in result.forces) for axis in range(3)) == pytest.approx(
        (0.0, 0.0, 0.0), abs=3e-7
    )


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (2.0, -3.0, 0.5)),
    (REFLECTION, (-1.0, 0.7, 4.0)),
    (INVERSION, (0.4, -1.0, 2.0)),
))
def test_energy_is_e3_invariant_and_force_is_covariant(matrix, translation):
    configuration, features, execution = _system()
    model = _model()
    transformation = E3Transformation(matrix=matrix, translation=translation)
    changed_configuration = _transform_configuration(configuration, transformation)
    changed_features = features.transformed(transformation)
    original = _evaluate(model, configuration, features, execution)
    changed = _evaluate(model, changed_configuration, changed_features, execution)
    for label in ("reference_energy", "tensor_energy", "energy"):
        before = getattr(original, label)
        after = getattr(changed, label)
        assert after.total_energy == pytest.approx(before.total_energy, rel=1e-11, abs=1e-10)
        assert after.atomic_energies == pytest.approx(before.atomic_energies, abs=1e-10)
    initial_forces = _forces(model, configuration, features, execution)
    changed_forces = _forces(model, changed_configuration, changed_features, execution)
    for force, transformed_force in zip(initial_forces.forces, changed_forces.forces, strict=True):
        assert transformed_force == pytest.approx(
            transformation.transform_vector(force), rel=1e-4, abs=5e-6
        )
    assert execution.retained_states == (TernaryState.NEGATIVE, TernaryState.NEUTRAL,
                                         TernaryState.POSITIVE)


def test_pending_target_does_not_replace_active_neutral_conditioning():
    configuration, features, pending = _system()
    without_pending = TernaryExecutionVector(states=(
        pending.states[0], TernaryExecutionState(TernaryState.NEUTRAL), pending.states[2],
    ))
    with_pending = _evaluate(_model(), configuration, features, pending)
    without = _evaluate(_model(), configuration, features, without_pending)
    assert with_pending == without
    assert _model().reference_model.conditioning.neutral_scale != 0.0


@pytest.mark.parametrize("start,end", (
    (TernaryState.NEGATIVE, TernaryState.POSITIVE),
    (TernaryState.POSITIVE, TernaryState.NEGATIVE),
))
def test_opposite_requests_commit_two_distinct_legs_before_energy_changes(start, end):
    configuration, features, _ = _system()
    model = _model()
    initial = TernaryExecutionVector.from_retained_states((start,) * 3)
    entered = execute_ternary_vector_step(initial, requested_targets=(end,) * 3)
    assert entered.current.retained_states == (TernaryState.NEUTRAL,) * 3
    assert entered.current.has_pending_targets
    assert all(item.pending_target is end for item in entered.current.states)
    exited = execute_ternary_vector_step(entered.current)
    assert exited.current.retained_states == (end,) * 3
    assert not exited.current.has_pending_targets
    for event in (entered, exited):
        assert event.committed_count == 3
        assert all(
            not is_direct_opposite_transition(node.route.transition.source,
                                              node.route.transition.target)
            for node in event.node_steps if node.route is not None
        )
    energy = tuple(_evaluate(model, configuration, features, execution).energy.total_energy
                   for execution in (initial, entered.current, exited.current))
    assert energy[0] != pytest.approx(energy[1], abs=1e-9)
    assert energy[1] != pytest.approx(energy[2], abs=1e-9)


def test_resonance_scalar_channels_preserve_energy_and_tensor_representation():
    configuration, features, execution = _system()
    original = ResonanceState(phases=(0.0, 0.2, 0.4), frequencies=(-0.1, 0.0, 0.3))
    evolved = ResonanceState(phases=(0.0, 0.7, 1.4), frequencies=original.frequencies)

    def with_resonance(state):
        base = append_md_resonance_features(features.base, resonance_descriptor(state))
        return ScalarVectorTensorFeatures(base=base, rank_two=features.rank_two)

    augmented = with_resonance(original)
    modified = with_resonance(evolved)
    model = _model(resonance_channels=True)
    first = _evaluate(model, configuration, augmented, execution)
    second = _evaluate(model, configuration, modified, execution)
    assert augmented.base.scalar_channel_count == 4
    assert modified.rank_two == features.rank_two
    assert first.energy.total_energy != pytest.approx(second.energy.total_energy, abs=1e-9)
    assert first.tensor_energy == second.tensor_energy


def test_identical_inputs_replay_deterministically_and_result_is_frozen():
    configuration, features, execution = _system()
    first = _evaluate(_model(), configuration, features, execution)
    second = _evaluate(_model(), configuration, features, execution)
    assert first == second and first is not second
    assert _forces(_model(), configuration, features, execution) == _forces(
        _model(), configuration, features, execution
    )
    with pytest.raises(FrozenInstanceError):
        first.energy = first.reference_energy
    with pytest.raises(FrozenInstanceError):
        first.layer = None


@pytest.mark.parametrize("invalid,error", (
    (True, TypeError),
    (float("nan"), ValueError),
    (float("inf"), ValueError),
    ("0.1", TypeError),
))
def test_tensor_weights_reject_invalid_numeric_coefficients(invalid, error):
    with pytest.raises(error):
        RankTwoChannelEnergyWeights(trace=invalid)


def test_readout_and_models_reject_incorrect_types_and_channel_counts():
    with pytest.raises(ValueError):
        RankTwoInvariantEnergyReadout(())
    with pytest.raises(TypeError):
        RankTwoInvariantEnergyReadout((None,))
    configuration, features, execution = _system()
    model = _model()
    with pytest.raises(TypeError):
        model.evaluate(configuration, build_cutoff_graph(configuration, CUTOFF), None, execution)
    with pytest.raises(TypeError):
        model.evaluate(configuration, build_cutoff_graph(configuration, CUTOFF), features, None)
    wrong = replace(model, tensor_readout=RankTwoInvariantEnergyReadout(
        (RankTwoChannelEnergyWeights(trace=1.0),)
    ))
    with pytest.raises(ValueError, match="channel counts"):
        _evaluate(wrong, configuration, features, execution)
    with pytest.raises(TypeError):
        RankTwoConservativeForceEvaluator(None)


def test_force_evaluator_rejects_mismatched_node_and_feature_counts():
    configuration, features, execution = _system()
    graph = build_cutoff_graph(configuration, CUTOFF)
    one_node = TernaryExecutionVector.from_retained_states((TernaryState.NEUTRAL,))
    with pytest.raises(ValueError, match="counts differ"):
        RankTwoConservativeForceEvaluator(CoordinateDifferentiation()).evaluate(
            _model(), configuration, graph, features, one_node
        )


def test_energy_result_detects_corrupted_additive_components():
    configuration, features, execution = _system()
    result = _evaluate(_model(), configuration, features, execution)
    altered = EnergyState.from_atomic_energies(tuple(
        x + 0.1 for x in result.tensor_energy.atomic_energies
    ))
    with pytest.raises(ValueError, match="atomic energy contributions"):
        replace(result, tensor_energy=altered)
    with pytest.raises(TypeError, match="reference_energy"):
        replace(result, reference_energy=None)
