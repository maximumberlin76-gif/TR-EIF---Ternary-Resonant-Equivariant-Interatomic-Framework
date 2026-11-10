
"""Independent FLiBe rank-two TR-EIP stress and pending-route integration checks.

Reconstruct all six symmetric cell-strain derivatives using a four-point
energy stencil and a separate affine deformation implementation. The graph,
resonance-conditioned scalar/vector and tensor features, and retained ternary
execution stay fixed over each differentiation stencil.
"""

from __future__ import annotations

from math import fsum, isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.energy.rank_two_model import (
    RankTwoChannelEnergyWeights,
    RankTwoConservativeEnergyModel,
    RankTwoInvariantEnergyReadout,
)
from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator
from tr_eif.equivariant import (
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
from tr_eif.flibe.rank_two_tr_eip import FLiBeRankTwoTREIPModel
from tr_eif.flibe.rank_two_tr_eip_stress import evaluate_flibe_rank_two_tr_eip_stress
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import (
    TernaryExecutionGuard,
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
    execute_ternary_vector_step,
)

STRAIN_COMPONENTS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0),
    (1.1, 0.7, 0.8),
    (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
CELL = ((8.0, 0.0, 0.0), (0.0, 8.0, 0.0), (0.0, 0.0, 8.0))
PROVENANCE = ParameterProvenance.TEST_FIXTURE


@pytest.fixture(scope="module")
def setup():
    """Create an explicit periodic Li2BeF4 state and nonzero rank-two readout."""
    configuration = FLiBeConfiguration(AtomicConfiguration(
        species=SPECIES,
        positions=POSITIONS,
        cell=CELL,
        periodic=(True, True, True),
    ))
    graph = build_cutoff_graph(configuration.configuration, 1.6)
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=FLiBeThermodynamicState(850.0, 101325.0),
        resonance_state=ResonanceState(
            phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
            frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
        ),
        provenance=PROVENANCE,
    )
    base_features = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.25 * i,),
            vectors=((1.0, 0.1 * i, -0.05 * i),),
        )
        for i in range(len(SPECIES))
    ))
    tensors = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor((
            (1.0 + 0.1 * i, 0.2, -0.3),
            (0.4, 0.8 - 0.05 * i, 0.1),
            (-0.2, 0.3, 0.6),
        )),
    ) for i in range(len(SPECIES))))
    features = ScalarVectorTensorFeatures(base_features, tensors)
    reference = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5,
            neutral_scale=1.25,
            positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3), bias=0.1,
        ),
    )
    model = FLiBeRankTwoTREIPModel(
        tr_eip_model=FLiBeTREIPModel(reference, PROVENANCE),
        rank_two_model=RankTwoConservativeEnergyModel(
            reference_model=reference,
            tensor_readout=RankTwoInvariantEnergyReadout((
                RankTwoChannelEnergyWeights(
                    trace=0.15,
                    isotropic_norm_squared=0.08,
                    symmetric_traceless_norm_squared=0.30,
                    antisymmetric_norm_squared=0.20,
                ),
            )),
            coupling=RankTwoMessageCoupling(
                tensor_scale=0.7,
                scalar_dyad_scale=0.2,
                vector_dyad_scale=-0.15,
                scalar_channel_index=0,
                vector_channel_index=0,
            ),
        ),
    )
    evaluator = RankTwoConservativeStressEvaluator(
        CellStrainDifferentiation(step=1.0e-6)
    )
    return configuration, graph, descriptor, features, model, evaluator


def _stress(setup, execution):
    configuration, graph, descriptor, features, model, evaluator = setup
    return evaluate_flibe_rank_two_tr_eip_stress(
        model, evaluator, configuration, graph, features, descriptor, execution,
    )


def _affine(vector, i, j, deformation):
    """Apply (I + strain) to one Cartesian vector without library strain helpers."""
    components = list(vector)
    if i == j:
        components[i] += deformation * vector[i]
    else:
        components[i] += 0.5 * deformation * vector[j]
        components[j] += 0.5 * deformation * vector[i]
    return tuple(components)


def _deformed(configuration, i, j, deformation):
    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(_affine(p, i, j, deformation) for p in configuration.positions),
        cell=tuple(_affine(v, i, j, deformation) for v in configuration.cell),
        periodic=configuration.periodic,
    )


def _volume(cell):
    a, b, c = cell
    return abs(fsum((
        a[0] * (b[1] * c[2] - b[2] * c[1]),
        a[1] * (b[2] * c[0] - b[0] * c[2]),
        a[2] * (b[0] * c[1] - b[1] * c[0]),
    )))


def _independent_stress(record, model, components, h):
    """Differentiate full energy with an independently coded four-point stencil."""
    evaluation = record.evaluation
    configuration = evaluation.configuration.configuration
    i, j = components

    def channels(multiplier):
        trial = _deformed(configuration, i, j, multiplier * h)
        sampled = model.rank_two_model.evaluate(
            trial,
            evaluation.graph,
            evaluation.resonance_features,
            evaluation.execution,
        )
        return (
            sampled.reference_energy.total_energy,
            sampled.tensor_energy.total_energy,
            sampled.energy.total_energy,
        )

    minus_two = channels(-2.0)
    minus_one = channels(-1.0)
    plus_one = channels(1.0)
    plus_two = channels(2.0)
    denominator = 12.0 * h * _volume(configuration.cell)
    return tuple(
        fsum((minus_two[channel], -8.0 * minus_one[channel],
              8.0 * plus_one[channel], -plus_two[channel])) / denominator
        for channel in range(3)
    )


@pytest.mark.parametrize("state", (
    TernaryState.NEGATIVE,
    TernaryState.NEUTRAL,
    TernaryState.POSITIVE,
))
@pytest.mark.parametrize("components", STRAIN_COMPONENTS)
def test_six_strains_match_independent_four_point_energy_derivatives(
    setup, state, components,
):
    execution = TernaryExecutionVector.from_retained_states((state,) * len(SPECIES))
    record = _stress(setup, execution)
    _, _, _, _, model, _ = setup
    i, j = components

    independent = _independent_stress(record, model, components, 4.0e-4)
    observed = (
        record.stress.reference_stress.tensor[i][j],
        record.stress.tensor_stress.tensor[i][j],
        record.stress.total_stress.tensor[i][j],
    )
    assert all(isfinite(value) for value in (*independent, *observed))
    for actual, expected in zip(observed, independent, strict=True):
        assert actual == pytest.approx(expected, rel=2.0e-4, abs=2.0e-7)
    assert record.stress.total_stress.tensor[j][i] == pytest.approx(observed[2], abs=1e-12)
    assert observed[2] == pytest.approx(fsum(observed[:2]), abs=1.0e-12)


@pytest.mark.parametrize("pending_target", (
    TernaryState.NEGATIVE, TernaryState.POSITIVE,
))
def test_pending_request_preserves_all_six_stresses_until_commit(setup, pending_target):
    neutral = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL,) * len(SPECIES)
    )
    pending = TernaryExecutionVector(states=tuple(
        TernaryExecutionState(TernaryState.NEUTRAL, pending_target)
        for _ in SPECIES
    ))
    _, _, _, _, model, _ = setup
    baseline = _stress(setup, neutral)
    requested = _stress(setup, pending)

    assert neutral.retained_states == pending.retained_states
    assert pending.has_pending_targets
    assert baseline.evaluation.energy == requested.evaluation.energy
    assert baseline.stress.reference_stress == requested.stress.reference_stress
    assert baseline.stress.tensor_stress == requested.stress.tensor_stress
    assert baseline.stress.total_stress == requested.stress.total_stress
    assert baseline.potential_pressure == requested.potential_pressure

    for components in STRAIN_COMPONENTS:
        expected = _independent_stress(baseline, model, components, 4.0e-4)
        observed = _independent_stress(requested, model, components, 4.0e-4)
        assert observed == pytest.approx(expected, abs=1.0e-12)

    held = execute_ternary_vector_step(
        pending, guards=(TernaryExecutionGuard.hold(),) * len(SPECIES)
    )
    assert held.current == pending
    assert held.committed_count == 0
    assert _stress(setup, held.current).stress == requested.stress

    committed = execute_ternary_vector_step(pending)
    assert committed.committed_count == len(SPECIES)
    assert committed.current.retained_states == (pending_target,) * len(SPECIES)
    assert not committed.current.has_pending_targets
    after_commit = _stress(setup, committed.current)
    assert after_commit.evaluation.energy != requested.evaluation.energy
    assert after_commit.stress.total_stress != requested.stress.total_stress


def test_four_point_step_stability_and_potential_pressure(setup):
    execution = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEUTRAL,) * len(SPECIES)
    )
    record = _stress(setup, execution)
    _, _, _, _, model, _ = setup
    assert record.stress.reference_volume == pytest.approx(_volume(CELL), abs=1.0e-12)

    for components in STRAIN_COMPONENTS:
        narrow = _independent_stress(record, model, components, 2.0e-4)
        wide = _independent_stress(record, model, components, 8.0e-4)
        assert narrow == pytest.approx(wide, rel=1.0e-5, abs=1.0e-8)

    diagonal = record.stress.total_stress.tensor
    expected_pressure = -fsum(diagonal[i][i] for i in range(3)) / 3.0
    assert record.potential_pressure == pytest.approx(expected_pressure, abs=1.0e-12)
    assert record.evaluation.resonance.thermodynamic_state.pressure == 101325.0
