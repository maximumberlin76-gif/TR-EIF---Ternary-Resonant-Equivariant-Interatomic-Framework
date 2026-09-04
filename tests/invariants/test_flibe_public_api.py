"""Invariant tests for the TR-EIF FLiBe public API."""

import tr_eif.flibe as flibe
from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import InteractionEdge, InteractionGraph
from tr_eif.multiscale import MultiscaleHierarchy, MultiscalePartition
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceDescriptor
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryState,
    TernaryTargetThresholds,
)


EXPECTED_PUBLIC_API = {
    "AtomicMass",
    "ConstantFLiBeDensity",
    "ConstantFLiBeResonanceParameters",
    "Density",
    "DensityEvaluator",
    "FLIBE_FORMAL_CHARGES",
    "FLIBE_SPECIES",
    "FLiBeAtomCoordination",
    "FLiBeComposition",
    "FLiBeConfiguration",
    "FLiBeCoordinationState",
    "FLiBeDensityModel",
    "FLiBeMassParameters",
    "FLiBeMultiscaleCoolantModel",
    "FLiBeResonanceParameterization",
    "FLiBeSpecies",
    "FLiBeTernaryInterpretation",
    "FLiBeThermodynamicState",
    "FLiBeUnit",
    "FinePositions",
    "FormalCharge",
    "FormalChargeState",
    "ParameterProvenance",
    "ParameterValue",
    "PhysicalParameter",
    "Pressure",
    "ResonanceParameterEvaluator",
    "SpeciesAmount",
    "SpeciesCharge",
    "SpeciesCharges",
    "SpeciesComposition",
    "SpeciesCoordination",
    "SpeciesCounts",
    "SpeciesMass",
    "SpeciesMasses",
    "SpeciesTuple",
    "Temperature",
    "atomic_mass_parameter",
    "build_flibe_coordination_state",
    "build_flibe_multiscale_coolant_state",
    "build_formal_charge_state",
    "configuration_formal_charges",
    "configuration_masses",
    "density_parameter",
    "eutectic_flibe_composition",
    "evaluate_density",
    "evaluate_resonance_parameters",
    "flibe_species_counts",
    "flibe_species_from_symbol",
    "flibe_species_symbols",
    "formal_charge",
    "formal_charge_from_symbol",
    "interpret_flibe_ternary_target",
    "is_flibe_species_symbol",
    "is_formally_neutral",
    "pressure_parameter",
    "temperature_parameter",
    "total_configuration_mass",
    "total_formal_charge",
    "validate_flibe_configuration",
    "validate_flibe_species_sequence",
}


def _atomic_configuration() -> AtomicConfiguration:
    """Return one deterministic FLiBe-compatible atomic configuration."""

    return AtomicConfiguration(
        species=("Li", "Be", "F"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        ),
    )


def _configuration() -> flibe.FLiBeConfiguration:
    """Return one deterministic FLiBe-domain configuration."""

    return flibe.FLiBeConfiguration(
        configuration=_atomic_configuration()
    )


def _coordination() -> flibe.FLiBeCoordinationState:
    """Return one deterministic public coordination state."""

    return flibe.build_flibe_coordination_state(
        _configuration(),
        InteractionGraph(
            node_count=3,
            edges=(
                InteractionEdge(source=0, receiver=1),
                InteractionEdge(source=1, receiver=2),
            ),
        ),
    )


def test_public_api_matches_declared_contract() -> None:
    """The exported FLiBe API must match the declared contract exactly."""

    assert set(flibe.__all__) == EXPECTED_PUBLIC_API


def test_public_api_contains_no_duplicate_exports() -> None:
    """Every public FLiBe symbol must occur exactly once in __all__."""

    assert len(flibe.__all__) == len(set(flibe.__all__))


def test_every_declared_public_symbol_is_available() -> None:
    """Every name declared in __all__ must be package-accessible."""

    for name in flibe.__all__:
        assert hasattr(flibe, name)


def test_public_api_excludes_internal_names() -> None:
    """Private implementation names must not enter the public boundary."""

    assert all(not name.startswith("_") for name in flibe.__all__)


def test_species_interfaces_are_publicly_executable() -> None:
    """Species identity and exact-symbol lookup must execute through the API."""

    assert flibe.flibe_species_symbols() == ("Li", "Be", "F")
    assert flibe.flibe_species_from_symbol("Li") is flibe.FLiBeSpecies.LITHIUM
    assert flibe.is_flibe_species_symbol("F") is True
    assert flibe.validate_flibe_species_sequence(("Li", "F")) == (
        flibe.FLiBeSpecies.LITHIUM,
        flibe.FLiBeSpecies.FLUORINE,
    )


def test_composition_interface_is_publicly_executable() -> None:
    """FLiBe composition construction must execute through the package API."""

    composition = flibe.FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )

    assert composition.formula_unit_fractions == (
        2.0 / 3.0,
        1.0 / 3.0,
    )
    assert flibe.eutectic_flibe_composition() == composition


def test_configuration_interface_is_publicly_executable() -> None:
    """FLiBe configuration validation must execute through the package API."""

    atomic = _atomic_configuration()
    configuration = flibe.validate_flibe_configuration(atomic)

    assert isinstance(configuration, flibe.FLiBeConfiguration)
    assert configuration.configuration is atomic
    assert flibe.flibe_species_counts(atomic) == (
        (flibe.FLiBeSpecies.LITHIUM, 1),
        (flibe.FLiBeSpecies.BERYLLIUM, 1),
        (flibe.FLiBeSpecies.FLUORINE, 1),
    )


def test_formal_charge_interfaces_are_publicly_executable() -> None:
    """Formal charge bookkeeping must execute through the package API."""

    configuration = _configuration()

    charges = flibe.configuration_formal_charges(configuration)
    state = flibe.build_formal_charge_state(configuration)

    assert charges == (1, 2, -1)
    assert state.charges == charges
    assert state.total_charge == 2
    assert flibe.total_formal_charge(configuration) == 2
    assert flibe.is_formally_neutral(configuration) is False
    assert flibe.formal_charge_from_symbol("F") == -1


def test_mass_interfaces_are_publicly_executable() -> None:
    """Explicit FLiBe mass mapping must execute through the package API."""

    parameters = flibe.FLiBeMassParameters(
        lithium=2.0,
        beryllium=3.0,
        fluorine=5.0,
    )
    configuration = _configuration()

    assert flibe.configuration_masses(configuration, parameters) == (
        2.0,
        3.0,
        5.0,
    )
    assert flibe.total_configuration_mass(configuration, parameters) == 10.0


def test_thermodynamic_and_units_interfaces_are_publicly_executable() -> None:
    """Thermodynamic state and explicit-unit constructors must be public."""

    state = flibe.FLiBeThermodynamicState(
        temperature=7.0,
        pressure=11.0,
    )
    parameter = flibe.temperature_parameter(
        state.temperature,
        flibe.ParameterProvenance.TEST_FIXTURE,
    )

    assert state.temperature == 7.0
    assert state.pressure == 11.0
    assert parameter.value == 7.0
    assert parameter.unit is flibe.FLiBeUnit.KELVIN
    assert parameter.provenance is flibe.ParameterProvenance.TEST_FIXTURE


def test_density_interface_is_publicly_executable() -> None:
    """Explicit density models must evaluate through the package API."""

    state = flibe.FLiBeThermodynamicState(
        temperature=2.0,
        pressure=3.0,
    )
    model = flibe.ConstantFLiBeDensity(
        density=5.0,
        provenance=flibe.ParameterProvenance.TEST_FIXTURE,
    )

    result = flibe.evaluate_density(model, state)

    assert result.value == 5.0
    assert result.unit is flibe.FLiBeUnit.KILOGRAM_PER_CUBIC_METER


def test_coordination_interface_is_publicly_executable() -> None:
    """Species-resolved graph coordination must execute through the API."""

    state = _coordination()

    assert state.atom_count == 3
    assert state.total_neighbor_records == 2
    assert state.atoms[1].lithium_neighbors == 1
    assert state.atoms[2].beryllium_neighbors == 1


def test_resonance_parameterization_interface_is_publicly_executable() -> None:
    """FLiBe resonance parameterization must execute through the API."""

    coordination = _coordination()
    parameters = PhaseDynamicsParameters(
        coupling=(0.2, 0.3, 0.4),
        phase_lag=(0.1, 0.2, 0.3),
    )
    model = flibe.ConstantFLiBeResonanceParameters(
        parameters=parameters,
        provenance=flibe.ParameterProvenance.TEST_FIXTURE,
    )

    result = flibe.evaluate_resonance_parameters(
        model,
        coordination,
    )

    assert result is parameters


def test_ternary_interpretation_interface_is_publicly_executable() -> None:
    """Requested ternary targets must execute through the public FLiBe API."""

    interpretation = flibe.FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=-1.0,
            bias=0.0,
        ),
        thresholds=TernaryTargetThresholds(
            negative=-0.25,
            positive=0.25,
        ),
        provenance=flibe.ParameterProvenance.TEST_FIXTURE,
    )

    target = flibe.interpret_flibe_ternary_target(
        interpretation,
        ResonanceDescriptor(
            phase_order=1.0,
            frequency_spread=0.0,
        ),
    )

    assert target is TernaryState.POSITIVE


def test_multiscale_coolant_interface_is_publicly_executable() -> None:
    """FLiBe multiscale coolant construction must execute through the API."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 0, 0),
            ),
        )
    )
    model = flibe.FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=flibe.FLiBeMassParameters(
            lithium=2.0,
            beryllium=3.0,
            fluorine=5.0,
        ),
    )

    result = flibe.build_flibe_multiscale_coolant_state(
        model,
        _configuration(),
    )

    assert result.coarsest_state.masses == (10.0,)
    assert result.coarsest_state.total_mass == 10.0


def test_public_api_keeps_formal_charge_and_ternary_domains_distinct() -> None:
    """Formal charge values and ternary targets must remain separate types."""

    formal_charge = flibe.formal_charge_from_symbol("F")
    interpretation = flibe.FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0,
            frequency_spread_weight=0.0,
            bias=-1.0,
        ),
        thresholds=TernaryTargetThresholds(
            negative=-0.25,
            positive=0.25,
        ),
        provenance=flibe.ParameterProvenance.TEST_FIXTURE,
    )
    target = flibe.interpret_flibe_ternary_target(
        interpretation,
        ResonanceDescriptor(
            phase_order=1.0,
            frequency_spread=0.0,
        ),
    )

    assert formal_charge == -1
    assert type(formal_charge) is int
    assert target is TernaryState.NEUTRAL
