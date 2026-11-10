
"""Independent cell-strain stress qualification for rank-two TR-EIF energy.

Reconstruct homogeneous strain energies using Cartesian matrix arithmetic,
compare the reference energy derivative with the established stress evaluator,
and verify rank-two pressure, E(3), force-virial correspondence, resonance
channels, and retained balanced-ternary execution on fixed graph topology.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
    ConservativeStressEvaluator,
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.energy.rank_two_model import (
    RankTwoChannelEnergyWeights,
    RankTwoConservativeEnergyModel,
    RankTwoConservativeForceEvaluator,
    RankTwoInvariantEnergyReadout,
)
from tr_eif.energy.rank_two_stress import (
    RankTwoConservativeStressEvaluator,
    RankTwoConservativeStressResult,
    RankTwoStrainEnergySample,
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

PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
IDENTITY = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
CUTOFF = 2.2


def _system(*, zero_tensor=False, resonance_channels=False):
    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=((0.1, 0.2, 0.3), (1.1, 0.4, 0.5), (0.4, 1.35, 0.8)),
        cell=((5.0, 0.0, 0.0), (0.0, 5.0, 0.0), (0.0, 0.0, 5.0)),
        periodic=(True, True, True),
    )
    base = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(1.0 + 0.2 * i, 0.6 - 0.1 * i),
            vectors=((0.3 + 0.1 * i, 0.2 - 0.05 * i, -0.25),),
        ) for i in range(3)
    ))
    tensors = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor((
            (1.0 + 0.1 * i, 0.3, -0.2),
            (-0.4, 0.8 - 0.05 * i, 0.1),
            (0.2, -0.1, 0.7),
        )),
        RankTwoTensor.outer((1.0, 0.3 * i - 0.5, 0.2), (0.1, 0.8, -0.3)),
    ) for i in range(3)))
    features = ScalarVectorTensorFeatures(base, tensors)
    execution = TernaryExecutionVector(states=(
        TernaryExecutionState(TernaryState.NEGATIVE),
        TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE),
        TernaryExecutionState(TernaryState.POSITIVE),
    ))
    reference = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.15),
        conditioning=TernaryConditioning(
            negative_scale=0.6, neutral_scale=1.25, positive_scale=1.8,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.5, -0.3, 0.2, -0.1) if resonance_channels else (0.5, -0.3),
            bias=0.05,
        ),
    )
    weights = (
        (RankTwoChannelEnergyWeights(), RankTwoChannelEnergyWeights())
        if zero_tensor else (
            RankTwoChannelEnergyWeights(
                trace=0.15, isotropic_norm_squared=0.08,
                symmetric_traceless_norm_squared=0.25,
                antisymmetric_norm_squared=0.12,
            ),
            RankTwoChannelEnergyWeights(
                trace=-0.1, isotropic_norm_squared=0.05,
                symmetric_traceless_norm_squared=-0.06,
                antisymmetric_norm_squared=0.09,
            ),
        )
    )
    model = RankTwoConservativeEnergyModel(
        reference_model=reference,
        tensor_readout=RankTwoInvariantEnergyReadout(weights),
        coupling=RankTwoMessageCoupling(
            tensor_scale=0.7, scalar_dyad_scale=0.25,
            vector_dyad_scale=-0.15,
            scalar_channel_index=1, vector_channel_index=0,
        ),
    )
    graph = build_cutoff_graph(configuration, CUTOFF)
    assert graph.edge_count == 6
    assert all(edge.image == (0, 0, 0) for edge in graph.edges)
    return configuration, graph, features, execution, model


def _axial_system():
    configuration = AtomicConfiguration(
        species=("A", "A"),
        positions=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        cell=((4.0, 0.0, 0.0), (0.0, 4.0, 0.0), (0.0, 0.0, 4.0)),
        periodic=(True, True, True),
    )
    identity_tensor = RankTwoTensor(IDENTITY)
    features = ScalarVectorTensorFeatures(
        NodeFeatureVector(nodes=(
            NodeFeatures(scalars=(1.0,)), NodeFeatures(scalars=(1.0,)),
        )),
        RankTwoFeatureVector(nodes=((identity_tensor,), (identity_tensor,))),
    )
    execution = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL, TernaryState.NEUTRAL)
    )
    reference = ReferenceEnergyModel(
        RadialMessageOperator(1.0), TernaryConditioning(1.0, 1.0, 1.0),
        LinearInvariantEnergyFunctional((1.0,)),
    )
    model = RankTwoConservativeEnergyModel(
        reference,
        RankTwoInvariantEnergyReadout((RankTwoChannelEnergyWeights(trace=0.25),)),
        RankTwoMessageCoupling(),
    )
    return configuration, build_cutoff_graph(configuration, 2.0), features, execution, model


def _deform(configuration, i, j, magnitude):
    """Independent symmetric strain construction at fixed fractional ordering."""
    matrix = [[float(a == b) for b in range(3)] for a in range(3)]
    if i == j:
        matrix[i][j] += magnitude
    else:
        matrix[i][j] += magnitude / 2.0
        matrix[j][i] += magnitude / 2.0

    def apply(vector):
        return tuple(sum(matrix[a][b] * vector[b] for b in range(3)) for a in range(3))

    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(apply(point) for point in configuration.positions),
        cell=tuple(apply(vector) for vector in configuration.cell),
        periodic=configuration.periodic,
    )


def _volume(configuration):
    a, b, c = configuration.cell
    return abs(
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def _evaluate(configuration, graph, features, execution, model, step=1.0e-6):
    return RankTwoConservativeStressEvaluator(
        CellStrainDifferentiation(step=step)
    ).evaluate(model, configuration, graph, features, execution)


def _transform(configuration, features, transformation):
    return (
        AtomicConfiguration(
            species=configuration.species,
            positions=tuple(transformation.transform_position(p) for p in configuration.positions),
            cell=tuple(transformation.transform_vector(v) for v in configuration.cell),
            periodic=configuration.periodic,
        ),
        features.transformed(transformation),
    )


def _rotated_tensor(tensor, matrix):
    return tuple(tuple(
        sum(matrix[i][a] * tensor[a][b] * matrix[j][b]
            for a in range(3) for b in range(3))
        for j in range(3)
    ) for i in range(3))


@pytest.fixture(scope="module")
def reference():
    inputs = _system()
    return inputs, _evaluate(*inputs)


def test_analytic_axial_pair_reference_tensor_and_pressure():
    config, graph, features, execution, model = _axial_system()
    result = _evaluate(config, graph, features, execution, model)
    assert result.reference_volume == pytest.approx(64.0)
    assert result.reference_evaluation.reference_energy.total_energy == pytest.approx(3.0)
    assert result.reference_evaluation.tensor_energy.total_energy == pytest.approx(2.25)
    assert result.reference_stress.tensor[0][0] == pytest.approx(-1.0 / 64, abs=1e-9)
    assert result.tensor_stress.tensor[0][0] == pytest.approx(-0.75 / 64, abs=1e-9)
    assert result.total_stress.tensor[0][0] == pytest.approx(-1.75 / 64, abs=1e-9)
    assert result.potential_pressure == pytest.approx(1.75 / (3 * 64), abs=1e-9)
    for i in range(3):
        for j in range(3):
            if (i, j) != (0, 0):
                assert result.total_stress.tensor[i][j] == pytest.approx(0.0, abs=1e-8)


def test_six_strain_records_match_independent_energy_samples(reference):
    (config, graph, features, execution, model), result = reference
    assert isinstance(result, RankTwoConservativeStressResult)
    assert result.reference_evaluation == model.evaluate(config, graph, features, execution)
    assert result.reference_volume == pytest.approx(_volume(config))
    assert tuple(s.components for s in result.samples) == PAIRS
    assert len(result.samples) == 6
    h = result.differentiation.step
    for sample in result.samples:
        i, j = sample.components
        plus = model.evaluate(_deform(config, i, j, h), graph, features, execution)
        minus = model.evaluate(_deform(config, i, j, -h), graph, features, execution)
        assert sample.reference_plus == pytest.approx(plus.reference_energy.total_energy, abs=1e-12)
        assert sample.reference_minus == pytest.approx(minus.reference_energy.total_energy, abs=1e-12)
        assert sample.tensor_plus == pytest.approx(plus.tensor_energy.total_energy, abs=1e-12)
        assert sample.tensor_minus == pytest.approx(minus.tensor_energy.total_energy, abs=1e-12)
        assert sample.total_plus == pytest.approx(plus.energy.total_energy, abs=1e-12)
        assert sample.total_minus == pytest.approx(minus.energy.total_energy, abs=1e-12)
        scale = 1.0 / (2 * h * result.reference_volume)
        assert result.reference_stress.tensor[i][j] == pytest.approx(
            (plus.reference_energy.total_energy - minus.reference_energy.total_energy) * scale,
            abs=1e-9,
        )
        assert result.tensor_stress.tensor[i][j] == pytest.approx(
            (plus.tensor_energy.total_energy - minus.tensor_energy.total_energy) * scale,
            abs=1e-9,
        )


def test_full_stress_is_symmetric_and_componentwise_additive(reference):
    _, result = reference
    for name in ("reference_stress", "tensor_stress", "total_stress"):
        stress = getattr(result, name)
        assert stress.is_symmetric
        assert all(isfinite(x) for row in stress.tensor for x in row)
    for i in range(3):
        for j in range(3):
            assert result.total_stress.tensor[i][j] == fsum((
                result.reference_stress.tensor[i][j], result.tensor_stress.tensor[i][j]
            ))
    assert result.potential_pressure == -result.total_stress.trace / 3.0


def test_reference_channel_matches_existing_stress_operator(reference):
    (config, graph, features, execution, model), result = reference
    old = ConservativeStressEvaluator(result.differentiation).evaluate(
        model.reference_model, config, graph, features.base, execution,
    )
    for a, b in zip(result.reference_stress.tensor, old.tensor, strict=True):
        assert a == pytest.approx(b, rel=1e-11, abs=1e-10)


def test_zero_tensor_weights_restore_original_stress():
    config, graph, features, execution, model = _system(zero_tensor=True)
    result = _evaluate(config, graph, features, execution, model)
    original = ConservativeStressEvaluator(result.differentiation).evaluate(
        model.reference_model, config, graph, features.base, execution,
    )
    assert result.reference_stress == original
    for row in result.tensor_stress.tensor:
        assert row == pytest.approx((0.0, 0.0, 0.0), abs=1e-12)
    assert result.total_stress == result.reference_stress
    assert result.reference_evaluation.tensor_energy.total_energy == 0.0


def test_independent_wider_strain_stencil_converges(reference):
    (config, graph, features, execution, model), result = reference
    larger_step = 2.5e-5
    for i, j in PAIRS:
        plus = model.evaluate(_deform(config, i, j, larger_step), graph, features, execution)
        minus = model.evaluate(_deform(config, i, j, -larger_step), graph, features, execution)
        scale = 1 / (2.0 * larger_step * result.reference_volume)
        for name, channel in (
            ("reference_stress", "reference_energy"),
            ("tensor_stress", "tensor_energy"),
            ("total_stress", "energy"),
        ):
            expected = (getattr(plus, channel).total_energy
                        - getattr(minus, channel).total_energy) * scale
            assert getattr(result, name).tensor[i][j] == pytest.approx(
                expected, rel=2e-4, abs=2e-6
            )


def test_force_virial_correspondence_for_nonperiodic_image_graph(reference):
    (config, graph, features, execution, model), result = reference
    forces = RankTwoConservativeForceEvaluator(CoordinateDifferentiation(step=1.0e-5)).evaluate(
        model, config, graph, features, execution,
    )
    volume = result.reference_volume
    for i, j in PAIRS:
        expected = -fsum(
            (point[i] * force[j] + point[j] * force[i]) / 2.0
            for point, force in zip(config.positions, forces.forces, strict=True)
        ) / volume
        assert result.total_stress.tensor[i][j] == pytest.approx(
            expected, rel=3e-4, abs=3e-6
        )


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (2.0, -3.0, 0.5)),
    (REFLECTION, (-1.0, 0.7, 2.0)),
    (IDENTITY, (4.0, 0.5, -2.0)),
))
def test_stress_is_e3_covariant_under_rotation_reflection_and_translation(
    reference, matrix, translation,
):
    (config, graph, features, execution, model), original = reference
    transformation = E3Transformation(matrix, translation)
    changed_config, changed_features = _transform(config, features, transformation)
    changed_graph = build_cutoff_graph(changed_config, CUTOFF)
    changed = _evaluate(changed_config, changed_graph, changed_features, execution, model)
    assert changed.reference_volume == pytest.approx(original.reference_volume, rel=1e-12)
    for name in ("reference_stress", "tensor_stress", "total_stress"):
        expected = _rotated_tensor(getattr(original, name).tensor, matrix)
        observed = getattr(changed, name).tensor
        for row, desired in zip(observed, expected, strict=True):
            assert row == pytest.approx(desired, rel=1e-4, abs=2e-6)
    assert changed.potential_pressure == pytest.approx(original.potential_pressure, abs=2e-6)
    assert changed.reference_evaluation.energy.total_energy == pytest.approx(
        original.reference_evaluation.energy.total_energy, abs=1e-9
    )


def test_pending_destination_does_not_replace_committed_neutral_stress(reference):
    (config, graph, features, execution, model), result = reference
    plain = TernaryExecutionVector(states=(
        execution.states[0],
        TernaryExecutionState(TernaryState.NEUTRAL),
        execution.states[2],
    ))
    without_pending = _evaluate(config, graph, features, plain, model)
    assert result == without_pending
    assert model.reference_model.conditioning.neutral_scale != 0.0


@pytest.mark.parametrize("start,target", (
    (TernaryState.NEGATIVE, TernaryState.POSITIVE),
    (TernaryState.POSITIVE, TernaryState.NEGATIVE),
))
def test_opposite_requests_change_stress_only_on_committed_neutral_legs(start, target):
    config, graph, features, _, model = _system()
    initial = TernaryExecutionVector.from_retained_states((start,) * 3)
    entry = execute_ternary_vector_step(initial, requested_targets=(target,) * 3)
    assert entry.current.retained_states == (TernaryState.NEUTRAL,) * 3
    assert all(node.pending_target is target for node in entry.current.states)
    exit_step = execute_ternary_vector_step(entry.current)
    assert exit_step.current.retained_states == (target,) * 3
    assert not exit_step.current.has_pending_targets
    for stage in (entry, exit_step):
        assert stage.committed_count == 3
        for node in stage.node_steps:
            assert node.route is not None
            assert not is_direct_opposite_transition(
                node.route.transition.source, node.route.transition.target
            )
    stress = tuple(
        _evaluate(config, graph, features, state, model).total_stress.tensor
        for state in (initial, entry.current, exit_step.current)
    )
    assert any(abs(a - b) > 1e-8 for row_a, row_b in zip(stress[0], stress[1])
               for a, b in zip(row_a, row_b))
    assert any(abs(a - b) > 1e-8 for row_a, row_b in zip(stress[1], stress[2])
               for a, b in zip(row_a, row_b))


def test_resonance_scalar_channels_preserve_tensor_stress_contribution():
    config, graph, features, execution, model = _system(resonance_channels=True)
    initial = ResonanceState(
        phases=(0.0, 0.1, 0.2), frequencies=(-0.2, 0.0, 0.3),
    )
    evolved = ResonanceState(
        phases=(0.0, 0.9, 2.3), frequencies=initial.frequencies,
    )

    def with_phase(state):
        return ScalarVectorTensorFeatures(
            base=append_md_resonance_features(features.base, resonance_descriptor(state)),
            rank_two=features.rank_two,
        )

    a = _evaluate(config, graph, with_phase(initial), execution, model)
    b = _evaluate(config, graph, with_phase(evolved), execution, model)
    assert a.tensor_stress == b.tensor_stress
    assert a.reference_stress != b.reference_stress
    assert a.total_stress != b.total_stress
    assert a.reference_evaluation.layer.previous.rank_two == features.rank_two


def test_stress_replay_is_deterministic_and_immutable(reference):
    (config, graph, features, execution, model), result = reference
    assert result == _evaluate(config, graph, features, execution, model)
    assert result is not _evaluate(config, graph, features, execution, model)
    with pytest.raises(FrozenInstanceError):
        result.samples = ()
    with pytest.raises(FrozenInstanceError):
        result.total_stress = result.reference_stress


@pytest.mark.parametrize("field", ("model", "configuration", "graph", "features", "execution"))
def test_evaluator_rejects_untyped_inputs(field):
    config, graph, features, execution, model = _system()
    kwargs = dict(model=model, configuration=config, graph=graph,
                  features=features, execution=execution)
    kwargs[field] = None
    with pytest.raises(TypeError):
        RankTwoConservativeStressEvaluator(CellStrainDifferentiation()).evaluate(**kwargs)


def test_requires_periodic_cell_and_matching_node_counts():
    config, graph, features, execution, model = _system()
    no_cell = AtomicConfiguration(species=config.species, positions=config.positions)
    with pytest.raises(ValueError, match="simulation cell"):
        _evaluate(no_cell, graph, features, execution, model)
    bad_execution = TernaryExecutionVector.from_retained_states((TernaryState.NEUTRAL,))
    with pytest.raises(ValueError, match="atom counts differ"):
        _evaluate(config, graph, features, bad_execution, model)
    smaller_features = ScalarVectorTensorFeatures(
        NodeFeatureVector(nodes=features.base.nodes[:2]),
        RankTwoFeatureVector(nodes=features.rank_two.nodes[:2]),
    )
    with pytest.raises(ValueError, match="atom counts differ"):
        _evaluate(config, graph, smaller_features, execution, model)


def test_result_validates_strain_samples_and_recorded_derivatives(reference):
    _, result = reference
    sample = result.samples[0]
    with pytest.raises(ValueError, match="canonical"):
        replace(sample, components=(2, 1))
    with pytest.raises(TypeError, match="real"):
        replace(sample, tensor_plus=True)
    with pytest.raises(ValueError, match="strain energies"):
        replace(result, samples=(replace(sample, reference_plus=sample.reference_plus + 1.0),
                                 *result.samples[1:]))
    with pytest.raises(ValueError, match="symmetric strain ordering"):
        replace(result, samples=result.samples[::-1])
    with pytest.raises(TypeError, match="StressState"):
        replace(result, tensor_stress=None)
    with pytest.raises(ValueError, match="positive"):
        replace(result, reference_volume=0.0)


def test_evaluator_and_sample_reject_bad_numeric_contracts():
    with pytest.raises(TypeError, match="CellStrainDifferentiation"):
        RankTwoConservativeStressEvaluator(None)
    with pytest.raises(ValueError, match="canonical"):
        RankTwoStrainEnergySample((-1, 0), 1.0, 1.0, 1.0, 1.0)
    with pytest.raises(ValueError, match="finite"):
        RankTwoStrainEnergySample((0, 0), 1.0, 1.0, float("nan"), 1.0)
