"""End-to-end validation tests across explicit TR-EIF multiscale boundaries."""

from __future__ import annotations

from tr_eif.configuration import AtomicConfiguration
from tr_eif.multiscale.continuum_closure import (
    ContinuumClosureRecord,
    ContinuumClosureVariable,
    evaluate_continuum_closure,
)
from tr_eif.multiscale.electronic_reference import (
    ElectronicReferenceRecord,
    evaluate_electronic_reference,
)
from tr_eif.multiscale.engineering_boundary import (
    EngineeringBoundaryCondition,
    EngineeringBoundaryContext,
    EngineeringBoundaryRecord,
    evaluate_engineering_boundaries,
)
from tr_eif.multiscale.mesoscale_closure import (
    MesoscaleClosureRecord,
    MesoscaleClosureVariable,
    evaluate_mesoscale_closure,
)
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.state import (
    CoarseScaleState,
    build_coarse_scale_state,
)
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


PROVENANCE = "TEST_FIXTURE:cross-scale-validation"


def _configuration() -> AtomicConfiguration:
    """Construct one deterministic fine-scale configuration."""

    return AtomicConfiguration(
        species=("A", "B", "C", "D"),
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (6.0, 0.0, 0.0),
        ),
    )


def _coarse_state() -> CoarseScaleState:
    """Construct one deterministic atomistic-to-coarse state transfer."""

    return build_coarse_scale_state(
        positions=_configuration().positions,
        masses=(1.0, 1.0, 2.0, 2.0),
        partition=MultiscalePartition(
            fine_to_coarse=(0, 0, 1, 1),
        ),
    )


def _electronic_reference() -> ElectronicReferenceRecord:
    """Evaluate one explicit test-fixture electronic reference provider."""

    configuration = _configuration()

    def evaluator(
        candidate: AtomicConfiguration,
    ) -> ElectronicReferenceRecord:
        return ElectronicReferenceRecord(
            configuration=candidate,
            total_energy=0.0,
            source_id=PROVENANCE,
            method_id="TEST_FIXTURE:electronic-reference-method",
        )

    return evaluate_electronic_reference(
        configuration,
        evaluator,
    )


def _mesoscale() -> MesoscaleClosureRecord:
    """Evaluate one explicit coarse-to-mesoscale closure provider."""

    state = _coarse_state()

    def evaluator(
        candidate: CoarseScaleState,
        auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        return MesoscaleClosureRecord(
            state=candidate,
            closure_id="TEST_FIXTURE:mesoscale-closure",
            source_id=PROVENANCE,
            closure_variables=(
                MesoscaleClosureVariable(
                    name="coarse_mass_marker",
                    values=candidate.masses,
                ),
            ),
            auxiliary_variables=auxiliary,
        )

    return evaluate_mesoscale_closure(
        state,
        evaluator,
    )


def _continuum() -> ContinuumClosureRecord:
    """Evaluate one explicit mesoscale-to-continuum closure provider."""

    mesoscale = _mesoscale()

    def evaluator(
        candidate: MesoscaleClosureRecord,
        auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        return ContinuumClosureRecord(
            mesoscale=candidate,
            closure_id="TEST_FIXTURE:continuum-closure",
            source_id=PROVENANCE,
            continuum_variables=(
                ContinuumClosureVariable(
                    name="continuum_marker",
                    values=(candidate.state.total_mass,),
                ),
            ),
            auxiliary_variables=auxiliary,
        )

    return evaluate_continuum_closure(
        mesoscale,
        evaluator,
    )


def _engineering_boundary() -> EngineeringBoundaryRecord:
    """Evaluate one explicit continuum-to-engineering boundary provider."""

    continuum = _continuum()
    context = EngineeringBoundaryContext(
        engineering_model_id="TEST_FIXTURE:engineering-model",
        geometry_id="TEST_FIXTURE:geometry",
        mapping_id="TEST_FIXTURE:continuum-boundary-map",
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
                    boundary_id="boundary-a",
                    variable_id="continuum_marker",
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


def _transport_transfer() -> TransportCoefficientTransferRecord:
    """Evaluate one explicit atomistic-to-continuum transport transfer."""

    source = TransportCoefficient(
        coefficient_id="test_transport_coefficient",
        value=1.0,
        unit="test-unit",
        scale_id="atomistic",
        state_domain_id="TEST_FIXTURE:atomistic-domain",
        source_id=PROVENANCE,
    )
    context = TransportTransferContext(
        target_scale_id="continuum",
        mapping_id="TEST_FIXTURE:transport-map",
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


def _uncertainty_transfer() -> UncertaintyPropagationRecord:
    """Evaluate one explicit atomistic-to-continuum uncertainty transfer."""

    source = (
        UncertaintyMeasure(
            quantity_id="test_quantity",
            value=0.1,
            unit="test-unit",
            representation_id="TEST_FIXTURE:uncertainty-representation",
            scale_id="atomistic",
            state_domain_id="TEST_FIXTURE:atomistic-domain",
            source_id=PROVENANCE,
        ),
    )
    context = UncertaintyPropagationContext(
        target_scale_id="continuum",
        propagation_id="TEST_FIXTURE:uncertainty-map",
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
                    quantity_id="test_quantity",
                    value=0.2,
                    unit="test-unit",
                    representation_id=(
                        "TEST_FIXTURE:uncertainty-representation"
                    ),
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
    """Evaluate one explicit cross-scale thermodynamic validation fixture."""

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
        relation_id="TEST_FIXTURE:thermodynamic-relation",
        model_id="TEST_FIXTURE:thermodynamic-model",
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
            validation_id="TEST_FIXTURE:cross-scale-validation",
        )

    return evaluate_thermodynamic_consistency(
        source,
        target,
        context,
        evaluator,
    )


def test_electronic_reference_is_bound_to_fine_configuration() -> None:
    """The electronic-reference boundary must retain the fine configuration."""

    reference = _electronic_reference()

    assert reference.configuration == _configuration()
    assert reference.atom_count == 4
    assert reference.source_id == PROVENANCE


def test_atomistic_to_coarse_transfer_preserves_total_mass() -> None:
    """The deterministic coarse-state transfer must preserve fixture mass."""

    coarse = _coarse_state()

    assert coarse.fine_count == 4
    assert coarse.coarse_count == 2
    assert coarse.masses == (2.0, 4.0)
    assert coarse.total_mass == 6.0


def test_mesoscale_to_continuum_to_engineering_bindings_are_explicit() -> None:
    """Every closure boundary must retain the preceding typed record."""

    engineering = _engineering_boundary()
    continuum = engineering.continuum
    mesoscale = continuum.mesoscale

    assert mesoscale.state == _coarse_state()
    assert continuum.continuum_variables[0].values == (6.0,)
    assert engineering.conditions[0].values == (6.0,)
    assert engineering.context.mapping_id == (
        "TEST_FIXTURE:continuum-boundary-map"
    )


def test_transport_and_uncertainty_transfers_reach_declared_scale() -> None:
    """Independent cross-scale transfers must bind outputs to declared targets."""

    transport = _transport_transfer()
    uncertainty = _uncertainty_transfer()

    assert transport.source.scale_id == "atomistic"
    assert transport.target.scale_id == "continuum"
    assert transport.target.scale_id == transport.context.target_scale_id

    assert uncertainty.source_measures[0].scale_id == "atomistic"
    assert uncertainty.target_measures[0].scale_id == "continuum"
    assert (
        uncertainty.target_measures[0].scale_id
        == uncertainty.context.target_scale_id
    )


def test_thermodynamic_validation_status_is_explicit_cross_scale_evidence() -> None:
    """Thermodynamic consistency must remain an explicit validation result."""

    validation = _thermodynamic_validation()

    assert validation.source_variables[0].scale_id == "atomistic"
    assert validation.target_variables[0].scale_id == "continuum"
    assert validation.is_consistent is True
    assert validation.validation_id == "TEST_FIXTURE:cross-scale-validation"


def test_cross_scale_validation_chain_is_deterministic() -> None:
    """Repeated construction from identical fixtures must reproduce all records."""

    first = (
        _electronic_reference(),
        _coarse_state(),
        _mesoscale(),
        _continuum(),
        _engineering_boundary(),
        _transport_transfer(),
        _uncertainty_transfer(),
        _thermodynamic_validation(),
    )
    second = (
        _electronic_reference(),
        _coarse_state(),
        _mesoscale(),
        _continuum(),
        _engineering_boundary(),
        _transport_transfer(),
        _uncertainty_transfer(),
        _thermodynamic_validation(),
    )

    assert first == second
