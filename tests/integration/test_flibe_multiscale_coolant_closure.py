"""Integration tests for the FLiBe multiscale coolant closure chain."""

from __future__ import annotations

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.multiscale_coolant import FLiBeMultiscaleCoolantModel
from tr_eif.multiscale.continuum_closure import (
    ContinuumClosureRecord,
    ContinuumClosureVariable,
    evaluate_continuum_closure,
)
from tr_eif.multiscale.engineering_boundary import (
    EngineeringBoundaryCondition,
    EngineeringBoundaryContext,
    EngineeringBoundaryRecord,
    evaluate_engineering_boundaries,
)
from tr_eif.multiscale.hierarchy import MultiscaleHierarchy
from tr_eif.multiscale.mesoscale_closure import (
    MesoscaleClosureRecord,
    MesoscaleClosureVariable,
    evaluate_mesoscale_closure,
)
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.thermodynamic_consistency import (
    ThermodynamicConsistencyContext,
    ThermodynamicConsistencyRecord,
    ThermodynamicVariable,
    evaluate_thermodynamic_consistency,
)
from tr_eif.multiscale.transport_transfer import (
    TransportCoefficient,
    TransportCoefficientTransferRecord,
    TransportTransferContext,
    evaluate_transport_coefficient_transfer,
)
from tr_eif.multiscale.uncertainty_propagation import (
    UncertaintyMeasure,
    UncertaintyPropagationContext,
    UncertaintyPropagationRecord,
    evaluate_uncertainty_propagation,
)


PROVENANCE = "TEST_FIXTURE:flibe-multiscale-coolant"


def _configuration() -> FLiBeConfiguration:
    """Construct one exact 2 LiF : 1 BeF2 fine-scale fixture."""

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=("Li", "Li", "Be", "F", "F", "F", "F"),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.5, 1.0, 0.0),
                (0.0, 0.0, 1.0),
                (1.0, 1.0, 1.0),
                (2.0, 0.0, 0.0),
                (0.5, 2.0, 0.0),
            ),
        )
    )


def _coolant_model() -> FLiBeMultiscaleCoolantModel:
    """Construct a deterministic seven-to-three-to-one coolant hierarchy."""

    return FLiBeMultiscaleCoolantModel(
        hierarchy=MultiscaleHierarchy(
            partitions=(
                MultiscalePartition(
                    fine_to_coarse=(0, 0, 1, 1, 2, 2, 2),
                ),
                MultiscalePartition(
                    fine_to_coarse=(0, 0, 0),
                ),
            )
        ),
        mass_parameters=FLiBeMassParameters(
            lithium=2.0,
            beryllium=3.0,
            fluorine=5.0,
        ),
    )


def _hierarchy_state():
    """Build the FLiBe fine-to-coarse structural state hierarchy."""

    return _coolant_model().build_state(_configuration())


def _mesoscale() -> MesoscaleClosureRecord:
    """Bind one explicit mesoscale closure to the FLiBe coarsest state."""

    state = _hierarchy_state().coarsest_state

    def evaluator(
        candidate,
        auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        return MesoscaleClosureRecord(
            state=candidate,
            closure_id="TEST_FIXTURE:flibe-mesoscale-closure",
            source_id=PROVENANCE,
            closure_variables=(
                MesoscaleClosureVariable(
                    name="total_mass_marker",
                    values=(candidate.total_mass,),
                ),
            ),
            auxiliary_variables=auxiliary,
        )

    return evaluate_mesoscale_closure(
        state,
        evaluator,
    )


def _continuum() -> ContinuumClosureRecord:
    """Bind one explicit continuum closure to the FLiBe mesoscale state."""

    mesoscale = _mesoscale()

    def evaluator(
        candidate: MesoscaleClosureRecord,
        auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        return ContinuumClosureRecord(
            mesoscale=candidate,
            closure_id="TEST_FIXTURE:flibe-continuum-closure",
            source_id=PROVENANCE,
            continuum_variables=(
                ContinuumClosureVariable(
                    name="coolant_mass_marker",
                    values=(candidate.state.total_mass,),
                ),
            ),
            auxiliary_variables=auxiliary,
        )

    return evaluate_continuum_closure(
        mesoscale,
        evaluator,
    )


def _transport() -> TransportCoefficientTransferRecord:
    """Evaluate one explicit FLiBe transport scale transfer fixture."""

    source = TransportCoefficient(
        coefficient_id="test_transport",
        value=1.0,
        unit="test-unit",
        scale_id="atomistic",
        state_domain_id="TEST_FIXTURE:atomistic-domain",
        source_id=PROVENANCE,
    )
    context = TransportTransferContext(
        target_scale_id="continuum",
        mapping_id="TEST_FIXTURE:flibe-transport-map",
        normalization_id="TEST_FIXTURE:transport-normalization",
        assumptions_id="TEST_FIXTURE:transport-assumptions",
    )

    def evaluator(
        candidate: TransportCoefficient,
        candidate_context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        return TransportCoefficientTransferRecord(
            source=candidate,
            target=TransportCoefficient(
                coefficient_id=candidate.coefficient_id,
                value=2.0,
                unit="test-unit",
                scale_id=candidate_context.target_scale_id,
                state_domain_id="TEST_FIXTURE:continuum-domain",
                source_id=PROVENANCE,
            ),
            context=candidate_context,
        )

    return evaluate_transport_coefficient_transfer(
        source,
        context,
        evaluator,
    )


def _uncertainty() -> UncertaintyPropagationRecord:
    """Evaluate one explicit FLiBe uncertainty propagation fixture."""

    source = (
        UncertaintyMeasure(
            quantity_id="test_transport",
            value=0.1,
            unit="test-unit",
            representation_id="TEST_FIXTURE:standard-deviation",
            scale_id="atomistic",
            state_domain_id="TEST_FIXTURE:atomistic-domain",
            source_id=PROVENANCE,
        ),
    )
    context = UncertaintyPropagationContext(
        target_scale_id="continuum",
        propagation_id="TEST_FIXTURE:flibe-uncertainty-map",
        assumptions_id="TEST_FIXTURE:uncertainty-assumptions",
        correlation_id="TEST_FIXTURE:correlation-model",
        normalization_id="TEST_FIXTURE:uncertainty-normalization",
    )

    def evaluator(
        candidate: tuple[UncertaintyMeasure, ...],
        candidate_context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        return UncertaintyPropagationRecord(
            source_measures=candidate,
            target_measures=(
                UncertaintyMeasure(
                    quantity_id="test_transport",
                    value=0.2,
                    unit="test-unit",
                    representation_id="TEST_FIXTURE:standard-deviation",
                    scale_id=candidate_context.target_scale_id,
                    state_domain_id="TEST_FIXTURE:continuum-domain",
                    source_id=PROVENANCE,
                ),
            ),
            context=candidate_context,
        )

    return evaluate_uncertainty_propagation(
        source,
        context,
        evaluator,
    )


def _thermodynamic_validation() -> ThermodynamicConsistencyRecord:
    """Evaluate one explicit FLiBe cross-scale thermodynamic fixture."""

    source = (
        ThermodynamicVariable(
            variable_id="test_thermodynamic_variable",
            value=1.0,
            unit="test-unit",
            scale_id="atomistic",
            state_domain_id="TEST_FIXTURE:atomistic-domain",
            source_id=PROVENANCE,
        ),
    )
    target = (
        ThermodynamicVariable(
            variable_id="test_thermodynamic_variable",
            value=1.0,
            unit="test-unit",
            scale_id="continuum",
            state_domain_id="TEST_FIXTURE:continuum-domain",
            source_id=PROVENANCE,
        ),
    )
    context = ThermodynamicConsistencyContext(
        relation_id="TEST_FIXTURE:flibe-thermodynamic-relation",
        model_id="TEST_FIXTURE:flibe-coolant-model",
        assumptions_id="TEST_FIXTURE:thermodynamic-assumptions",
        normalization_id="TEST_FIXTURE:thermodynamic-normalization",
    )

    def evaluator(
        candidate_source: tuple[ThermodynamicVariable, ...],
        candidate_target: tuple[ThermodynamicVariable, ...],
        candidate_context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        return ThermodynamicConsistencyRecord(
            source_variables=candidate_source,
            target_variables=candidate_target,
            context=candidate_context,
            is_consistent=True,
            validation_id="TEST_FIXTURE:flibe-thermodynamic-validation",
        )

    return evaluate_thermodynamic_consistency(
        source,
        target,
        context,
        evaluator,
    )


def _engineering_boundary() -> EngineeringBoundaryRecord:
    """Bind the continuum closure to one explicit engineering boundary."""

    continuum = _continuum()
    context = EngineeringBoundaryContext(
        engineering_model_id="TEST_FIXTURE:flibe-engineering-model",
        geometry_id="TEST_FIXTURE:engineering-geometry",
        mapping_id="TEST_FIXTURE:coolant-boundary-map",
        assumptions_id="TEST_FIXTURE:boundary-assumptions",
    )

    def evaluator(
        candidate: ContinuumClosureRecord,
        candidate_context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        return EngineeringBoundaryRecord(
            continuum=candidate,
            conditions=(
                EngineeringBoundaryCondition(
                    boundary_id="coolant-boundary",
                    variable_id="coolant_mass_marker",
                    condition_id="TEST_FIXTURE:boundary-condition",
                    values=candidate.continuum_variables[0].values,
                    unit="test-unit",
                    source_id=PROVENANCE,
                ),
            ),
            context=candidate_context,
        )

    return evaluate_engineering_boundaries(
        continuum,
        context,
        evaluator,
    )


def test_exact_flibe_composition_is_preserved_at_fine_scale() -> None:
    """The coolant closure chain must begin from exact LiF-BeF2 stoichiometry."""

    composition = _configuration().composition()

    assert composition.lif_fraction == pytest.approx(2.0 / 3.0)
    assert composition.bef2_fraction == pytest.approx(1.0 / 3.0)


def test_flibe_multiscale_hierarchy_preserves_total_mass() -> None:
    """Structural coarse-graining must conserve represented fixture mass."""

    hierarchy = _hierarchy_state()

    assert hierarchy.hierarchy.level_counts == (7, 3, 1)
    assert hierarchy.state_at(1).total_mass == pytest.approx(27.0)
    assert hierarchy.coarsest_state.total_mass == pytest.approx(27.0)


def test_mesoscale_and_continuum_closures_bind_same_coolant_mass() -> None:
    """FLiBe closure records must remain bound to the coarse coolant state."""

    mesoscale = _mesoscale()
    continuum = _continuum()

    assert mesoscale.state.total_mass == pytest.approx(27.0)
    assert mesoscale.variable("total_mass_marker").values == pytest.approx(
        (27.0,)
    )
    assert continuum.mesoscale == mesoscale
    assert continuum.variable("coolant_mass_marker").values == pytest.approx(
        (27.0,)
    )


def test_transport_transfer_reaches_explicit_continuum_scale() -> None:
    """Transport transfer must retain explicit atomistic and continuum scales."""

    transfer = _transport()

    assert transfer.source.scale_id == "atomistic"
    assert transfer.target.scale_id == "continuum"
    assert transfer.target.scale_id == transfer.context.target_scale_id


def test_uncertainty_propagation_reaches_explicit_continuum_scale() -> None:
    """Uncertainty transfer must remain explicit across the coolant scale map."""

    propagation = _uncertainty()

    assert propagation.source_measures[0].scale_id == "atomistic"
    assert propagation.target_measures[0].scale_id == "continuum"
    assert (
        propagation.target_measures[0].scale_id
        == propagation.context.target_scale_id
    )


def test_thermodynamic_consistency_remains_validation_status() -> None:
    """Cross-scale thermodynamic consistency must remain Boolean evidence."""

    validation = _thermodynamic_validation()

    assert validation.source_variables[0].scale_id == "atomistic"
    assert validation.target_variables[0].scale_id == "continuum"
    assert validation.is_consistent is True
    assert isinstance(validation.is_consistent, bool)


def test_engineering_boundary_is_bound_to_continuum_coolant_closure() -> None:
    """Engineering boundary data must bind to the explicit continuum record."""

    boundary = _engineering_boundary()

    assert boundary.continuum == _continuum()
    assert boundary.condition_count == 1
    assert boundary.conditions[0].values == pytest.approx((27.0,))


def test_flibe_multiscale_coolant_closure_chain_is_deterministic() -> None:
    """Identical explicit FLiBe inputs must reproduce the same closure chain."""

    first = (
        _hierarchy_state(),
        _mesoscale(),
        _continuum(),
        _transport(),
        _uncertainty(),
        _thermodynamic_validation(),
        _engineering_boundary(),
    )
    second = (
        _hierarchy_state(),
        _mesoscale(),
        _continuum(),
        _transport(),
        _uncertainty(),
        _thermodynamic_validation(),
        _engineering_boundary(),
    )

    assert first == second
