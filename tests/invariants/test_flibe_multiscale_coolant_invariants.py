"""Invariant tests for the TR-EIF FLiBe multiscale coolant-model contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.multiscale_coolant import (
    FLiBeMultiscaleCoolantModel,
    build_flibe_multiscale_coolant_state,
)
from tr_eif.multiscale import (
    MultiscaleHierarchy,
    MultiscalePartition,
    MultiscaleStateHierarchy,
)


def _mass_parameters(
    scale: float = 1.0,
) -> FLiBeMassParameters:
    """Return deterministic test-only FLiBe mass parameters."""

    return FLiBeMassParameters(
        lithium=2.0 * scale,
        beryllium=3.0 * scale,
        fluorine=5.0 * scale,
    )


def _configuration(
    *,
    species: tuple[str, ...] = ("Li", "Be", "F", "F"),
    positions: tuple[tuple[float, float, float], ...] | None = None,
    periodic: tuple[bool, bool, bool] = (False, False, False),
) -> FLiBeConfiguration:
    """Build one deterministic FLiBe-domain atomic configuration."""

    if positions is None:
        positions = tuple(
            (2.0 * float(index), 0.0, 0.0)
            for index in range(len(species))
        )

    cell = None
    if any(periodic):
        cell = (
            (20.0, 0.0, 0.0),
            (0.0, 20.0, 0.0),
            (0.0, 0.0, 20.0),
        )

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=species,
            positions=positions,
            cell=cell,
            periodic=periodic,
        )
    )


def _hierarchy() -> MultiscaleHierarchy:
    """Return a deterministic four-to-two-to-one hierarchy."""

    return MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 0, 1, 1),
            ),
            MultiscalePartition(
                fine_to_coarse=(0, 0),
            ),
        )
    )


def _model() -> FLiBeMultiscaleCoolantModel:
    """Return one deterministic FLiBe multiscale coolant model."""

    return FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(),
    )


def test_model_preserves_hierarchy_and_mass_parameters() -> None:
    """Model construction must preserve explicit hierarchy and mass inputs."""

    hierarchy = _hierarchy()
    masses = _mass_parameters()

    model = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=masses,
    )

    assert model.hierarchy is hierarchy
    assert model.mass_parameters is masses


@pytest.mark.parametrize(
    "invalid_hierarchy",
    (None, True, False, 1, 1.0, "hierarchy", (), [], {}),
)
def test_model_requires_multiscale_hierarchy(
    invalid_hierarchy,
) -> None:
    """Coolant model hierarchy must use MultiscaleHierarchy."""

    with pytest.raises(
        TypeError,
        match="hierarchy must be a MultiscaleHierarchy",
    ):
        FLiBeMultiscaleCoolantModel(
            hierarchy=invalid_hierarchy,
            mass_parameters=_mass_parameters(),
        )


@pytest.mark.parametrize(
    "invalid_mass_parameters",
    (None, True, False, 1, 1.0, "masses", (), [], {}),
)
def test_model_requires_flibe_mass_parameters(
    invalid_mass_parameters,
) -> None:
    """Coolant model must use the explicit FLiBe mass contract."""

    with pytest.raises(
        TypeError,
        match="mass_parameters must be an FLiBeMassParameters",
    ):
        FLiBeMultiscaleCoolantModel(
            hierarchy=_hierarchy(),
            mass_parameters=invalid_mass_parameters,
        )


def test_model_is_frozen() -> None:
    """Coolant model records must be immutable after construction."""

    model = _model()

    with pytest.raises(FrozenInstanceError):
        model.mass_parameters = _mass_parameters(scale=2.0)


@pytest.mark.parametrize(
    "invalid_configuration",
    (None, True, False, 1, 1.0, "configuration", (), [], {}),
)
def test_build_state_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Multiscale state construction must require FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match="configuration must be an FLiBeConfiguration",
    ):
        _model().build_state(invalid_configuration)


def test_hierarchy_finest_count_must_match_atom_count() -> None:
    """Hierarchy finest cardinality must equal FLiBe atom count."""

    model = FLiBeMultiscaleCoolantModel(
        hierarchy=MultiscaleHierarchy(
            partitions=(
                MultiscalePartition(
                    fine_to_coarse=(0, 0, 1),
                ),
            )
        ),
        mass_parameters=_mass_parameters(),
    )

    with pytest.raises(
        ValueError,
        match=(
            "hierarchy finest_count must match "
            "FLiBe configuration atom_count"
        ),
    ):
        model.build_state(_configuration())


def test_build_state_returns_multiscale_state_hierarchy() -> None:
    """Successful coolant coarse-graining must return hierarchy state data."""

    result = _model().build_state(_configuration())

    assert isinstance(result, MultiscaleStateHierarchy)


def test_built_state_preserves_model_hierarchy() -> None:
    """Generated state hierarchy must retain the model hierarchy exactly."""

    model = _model()
    result = model.build_state(_configuration())

    assert result.hierarchy is model.hierarchy


def test_built_state_contains_one_state_per_scale_transition() -> None:
    """Generated coarse states must correspond one-to-one with transitions."""

    model = _model()
    result = model.build_state(_configuration())

    assert result.state_count == model.hierarchy.transition_count
    assert result.state_count == 2


def test_built_state_uses_expected_level_cardinalities() -> None:
    """Coolant coarse-graining must preserve hierarchy cardinality semantics."""

    result = _model().build_state(_configuration())

    assert result.hierarchy.level_counts == (4, 2, 1)
    assert result.state_at(1).coarse_count == 2
    assert result.state_at(2).coarse_count == 1


def test_first_coarse_state_uses_first_partition() -> None:
    """First generated state must use the first explicit partition."""

    model = _model()
    result = model.build_state(_configuration())

    assert result.state_at(1).partition == model.hierarchy.partition_at(0)


def test_second_coarse_state_uses_second_partition() -> None:
    """Second generated state must use the second explicit partition."""

    model = _model()
    result = model.build_state(_configuration())

    assert result.state_at(2).partition == model.hierarchy.partition_at(1)


def test_species_mass_parameters_propagate_to_first_coarse_state() -> None:
    """Per-species masses must be reduced according to the first partition."""

    configuration = _configuration(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (14.0, 0.0, 0.0),
        )
    )

    first = _model().build_state(configuration).state_at(1)

    assert first.masses == (5.0, 10.0)


def test_total_mass_is_preserved_at_every_coarse_level() -> None:
    """Additive mass reduction must preserve total represented mass."""

    result = _model().build_state(_configuration())

    assert result.state_at(1).total_mass == pytest.approx(15.0)
    assert result.state_at(2).total_mass == pytest.approx(15.0)


def test_first_level_centroids_use_species_mass_weighting() -> None:
    """First-level Cartesian centroids must use explicit species masses."""

    configuration = _configuration(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (14.0, 0.0, 0.0),
        )
    )

    first = _model().build_state(configuration).state_at(1)

    assert first.positions[0][0] == pytest.approx(1.2)
    assert first.positions[0][1:] == (0.0, 0.0)
    assert first.positions[1] == (12.0, 0.0, 0.0)


def test_coarsest_centroid_matches_full_mass_weighted_centroid() -> None:
    """Staged coarse-graining must preserve the physical mass centroid."""

    configuration = _configuration(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (14.0, 0.0, 0.0),
        )
    )

    coarsest = _model().build_state(configuration).coarsest_state

    assert coarsest.positions[0][0] == pytest.approx(8.4)
    assert coarsest.positions[0][1:] == (0.0, 0.0)
    assert coarsest.masses == (15.0,)


def test_uniform_mass_scaling_preserves_centroid_positions() -> None:
    """Uniform positive mass scaling must not change coarse centroids."""

    configuration = _configuration(
        positions=(
            (0.0, 1.0, 2.0),
            (2.0, 3.0, 4.0),
            (6.0, 5.0, 4.0),
            (8.0, 7.0, 6.0),
        )
    )

    first = FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(scale=1.0),
    ).build_state(configuration)

    second = FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(scale=7.0),
    ).build_state(configuration)

    for first_state, second_state in zip(first.states, second.states):
        for first_position, second_position in zip(
            first_state.positions,
            second_state.positions,
        ):
            for first_component, second_component in zip(
                first_position,
                second_position,
            ):
                assert second_component == pytest.approx(first_component)


def test_uniform_mass_scaling_scales_coarse_masses() -> None:
    """Uniform species-mass scaling must scale every coarse mass equally."""

    configuration = _configuration()

    first = FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(scale=1.0),
    ).build_state(configuration)

    second = FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(scale=4.0),
    ).build_state(configuration)

    for first_state, second_state in zip(first.states, second.states):
        assert second_state.masses == pytest.approx(
            tuple(4.0 * mass for mass in first_state.masses)
        )


def test_nonperiodic_configuration_uses_stored_positions_by_default() -> None:
    """Nonperiodic evaluation may use AtomicConfiguration positions directly."""

    positions = (
        (1.0, 2.0, 3.0),
        (4.0, 5.0, 6.0),
        (7.0, 8.0, 9.0),
        (10.0, 11.0, 12.0),
    )

    configuration = _configuration(positions=positions)
    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 1, 2, 3),
            ),
        )
    )

    result = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=_mass_parameters(),
    ).build_state(configuration)

    assert result.coarsest_state.positions == positions


def test_explicit_nonperiodic_positions_override_stored_positions() -> None:
    """Explicit fine positions must replace stored positions for coarse-graining."""

    configuration = _configuration()
    explicit_positions = (
        (10.0, 0.0, 0.0),
        (20.0, 0.0, 0.0),
        (30.0, 0.0, 0.0),
        (40.0, 0.0, 0.0),
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 1, 2, 3),
            ),
        )
    )

    result = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=_mass_parameters(),
    ).build_state(
        configuration,
        positions=explicit_positions,
    )

    assert result.coarsest_state.positions == explicit_positions
    assert result.coarsest_state.positions != configuration.configuration.positions


@pytest.mark.parametrize(
    "periodic",
    (
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ),
)
def test_any_periodic_axis_requires_explicit_unwrapped_positions(
    periodic: tuple[bool, bool, bool],
) -> None:
    """Any periodic axis must disable implicit Cartesian centroid input."""

    configuration = _configuration(periodic=periodic)

    with pytest.raises(
        ValueError,
        match=(
            "periodic FLiBe multiscale evaluation requires "
            "explicit unwrapped positions"
        ),
    ):
        _model().build_state(configuration)


def test_periodic_configuration_accepts_explicit_positions() -> None:
    """Periodic FLiBe evaluation must accept an explicit unwrapped position set."""

    configuration = _configuration(
        periodic=(True, True, True),
    )

    explicit_positions = (
        (0.0, 0.0, 0.0),
        (22.0, 0.0, 0.0),
        (44.0, 0.0, 0.0),
        (66.0, 0.0, 0.0),
    )

    result = _model().build_state(
        configuration,
        positions=explicit_positions,
    )

    assert isinstance(result, MultiscaleStateHierarchy)
    assert result.state_count == 2


def test_periodic_explicit_positions_are_not_wrapped_into_cell() -> None:
    """Explicit periodic coordinates must remain raw Cartesian inputs to centroids."""

    configuration = _configuration(
        periodic=(True, False, False),
    )

    explicit_positions = (
        (0.0, 0.0, 0.0),
        (22.0, 0.0, 0.0),
        (40.0, 0.0, 0.0),
        (50.0, 0.0, 0.0),
    )

    first = _model().build_state(
        configuration,
        positions=explicit_positions,
    ).state_at(1)

    assert first.positions[0][0] == pytest.approx(13.2)
    assert first.positions[1][0] == pytest.approx(45.0)


@pytest.mark.parametrize(
    "invalid_positions",
    ([], {}, "positions", 1, 1.0, True, False),
)
def test_explicit_positions_require_tuple(
    invalid_positions,
) -> None:
    """Explicit fine-position container must use tuple representation."""

    with pytest.raises(
        TypeError,
        match="positions must be a tuple or None",
    ):
        _model().build_state(
            _configuration(),
            positions=invalid_positions,
        )


@pytest.mark.parametrize(
    "positions",
    (
        (),
        ((0.0, 0.0, 0.0),),
        (
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        ),
        (
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (3.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
        ),
    ),
)
def test_explicit_position_count_must_match_atom_count(
    positions,
) -> None:
    """Explicit positions must contain exactly one vector per FLiBe atom."""

    with pytest.raises(
        ValueError,
        match="positions must contain one vector per FLiBe atom",
    ):
        _model().build_state(
            _configuration(),
            positions=positions,
        )


def test_explicit_position_vector_shape_validation_is_preserved() -> None:
    """Underlying multiscale geometry validation must reject malformed vectors."""

    positions = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (2.0, 0.0),
        (3.0, 0.0, 0.0),
    )

    with pytest.raises(
        ValueError,
        match=r"positions\[2\] must contain exactly three components",
    ):
        _model().build_state(
            _configuration(),
            positions=positions,
        )


def test_explicit_position_vector_type_validation_is_preserved() -> None:
    """Underlying multiscale geometry validation must reject non-tuple vectors."""

    positions = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        [2.0, 0.0, 0.0],
        (3.0, 0.0, 0.0),
    )

    with pytest.raises(
        TypeError,
        match=r"positions\[2\] must be a tuple",
    ):
        _model().build_state(
            _configuration(),
            positions=positions,
        )


@pytest.mark.parametrize(
    "component",
    (float("nan"), float("inf"), float("-inf")),
)
def test_explicit_positions_require_finite_components(
    component: float,
) -> None:
    """Underlying centroid layer must reject nonfinite Cartesian components."""

    positions = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (2.0, component, 0.0),
        (3.0, 0.0, 0.0),
    )

    with pytest.raises(
        ValueError,
        match=r"positions\[2\]\[1\] must be finite",
    ):
        _model().build_state(
            _configuration(),
            positions=positions,
        )


def test_integer_explicit_positions_are_normalized_downstream() -> None:
    """Accepted integer coordinates must become canonical floating values."""

    positions = (
        (0, 0, 0),
        (2, 0, 0),
        (10, 0, 0),
        (14, 0, 0),
    )

    result = _model().build_state(
        _configuration(),
        positions=positions,
    )

    assert all(
        isinstance(component, float)
        for state in result.states
        for position in state.positions
        for component in position
    )


def test_build_state_does_not_mutate_atomic_configuration() -> None:
    """Multiscale evaluation must not rewrite FLiBe atomic configuration data."""

    configuration = _configuration()
    original_species = configuration.configuration.species
    original_positions = configuration.configuration.positions
    original_periodic = configuration.configuration.periodic

    _model().build_state(configuration)

    assert configuration.configuration.species == original_species
    assert configuration.configuration.positions == original_positions
    assert configuration.configuration.periodic == original_periodic


def test_build_state_does_not_mutate_explicit_positions() -> None:
    """Explicit unwrapped position tuples must remain unchanged after evaluation."""

    positions = (
        (0.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
        (10.0, 0.0, 0.0),
        (14.0, 0.0, 0.0),
    )
    original = tuple(positions)

    _model().build_state(
        _configuration(),
        positions=positions,
    )

    assert positions == original


def test_build_state_does_not_mutate_mass_parameters() -> None:
    """Coolant coarse-graining must not mutate FLiBe mass parameters."""

    masses = _mass_parameters()
    original = masses.species_masses

    FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=masses,
    ).build_state(_configuration())

    assert masses.species_masses == original


def test_identity_hierarchy_preserves_fine_positions() -> None:
    """An identity scale partition must preserve every supplied position."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 1, 2, 3),
            ),
        )
    )
    configuration = _configuration()

    result = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=_mass_parameters(),
    ).build_state(configuration)

    assert result.coarsest_state.positions == configuration.configuration.positions


def test_identity_hierarchy_preserves_per_atom_masses() -> None:
    """Identity scale mapping must preserve one explicit mass per atom."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 1, 2, 3),
            ),
        )
    )

    result = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=_mass_parameters(),
    ).build_state(_configuration())

    assert result.coarsest_state.masses == (2.0, 3.0, 5.0, 5.0)


def test_single_coarse_entity_collects_complete_configuration_mass() -> None:
    """A many-to-one partition must collect all explicit atomic mass."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 0, 0, 0),
            ),
        )
    )

    result = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=_mass_parameters(),
    ).build_state(_configuration())

    assert result.coarsest_state.masses == (15.0,)
    assert result.coarsest_state.total_mass == pytest.approx(15.0)


def test_interleaved_partition_follows_explicit_scale_mapping() -> None:
    """Coarse membership must follow partition indices rather than atom adjacency."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(0, 1, 0, 1),
            ),
        )
    )

    configuration = _configuration(
        positions=(
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (20.0, 0.0, 0.0),
        )
    )

    result = FLiBeMultiscaleCoolantModel(
        hierarchy=hierarchy,
        mass_parameters=_mass_parameters(),
    ).build_state(configuration)

    coarse = result.coarsest_state

    assert coarse.masses == (7.0, 8.0)
    assert coarse.positions[0][0] == pytest.approx(20.0 / 7.0)
    assert coarse.positions[1][0] == pytest.approx(130.0 / 8.0)


def test_nonstoichiometric_supported_species_configuration_is_allowed() -> None:
    """Multiscale mapping must remain separate from LiF-BeF2 stoichiometry checks."""

    configuration = _configuration(
        species=("Li", "Li", "Li", "Li"),
    )

    result = _model().build_state(configuration)

    assert result.state_at(1).masses == (4.0, 4.0)
    assert result.coarsest_state.masses == (8.0,)


def test_scale_mapping_does_not_require_thermodynamic_state() -> None:
    """Coolant multiscale state construction has no hidden thermodynamic input."""

    model = _model()

    assert tuple(model.__dataclass_fields__) == (
        "hierarchy",
        "mass_parameters",
    )


def test_scale_mapping_does_not_require_density_model() -> None:
    """Density modeling must remain separate from geometric mass coarse-graining."""

    result = _model().build_state(_configuration())

    assert isinstance(result, MultiscaleStateHierarchy)
    assert not hasattr(result, "density")


def test_generated_state_contains_no_hidden_fine_state_level_zero() -> None:
    """Generated hierarchy states begin after the finest input scale."""

    result = _model().build_state(_configuration())

    with pytest.raises(
        IndexError,
        match="level is out of range for generated coarse states",
    ):
        result.state_at(0)


def test_scale_level_indices_are_not_ternary_state_values() -> None:
    """Hierarchy level indices must remain structural scale identifiers."""

    result = _model().build_state(_configuration())

    assert result.hierarchy.level_counts == (4, 2, 1)
    assert result.state_at(1).coarse_count == 2
    assert result.state_at(2).coarse_count == 1


def test_public_builder_matches_model_method() -> None:
    """Public FLiBe builder must preserve model build-state semantics."""

    model = _model()
    configuration = _configuration()

    direct = model.build_state(configuration)
    public = build_flibe_multiscale_coolant_state(
        model,
        configuration,
    )

    assert public == direct


def test_public_builder_preserves_explicit_positions() -> None:
    """Public builder must forward explicit fine positions unchanged in semantics."""

    positions = (
        (0.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
        (10.0, 0.0, 0.0),
        (14.0, 0.0, 0.0),
    )

    model = _model()
    configuration = _configuration(periodic=(True, False, False))

    direct = model.build_state(
        configuration,
        positions=positions,
    )
    public = build_flibe_multiscale_coolant_state(
        model,
        configuration,
        positions=positions,
    )

    assert public == direct


@pytest.mark.parametrize(
    "invalid_model",
    (None, True, False, 1, 1.0, "model", (), [], {}),
)
def test_public_builder_requires_flibe_multiscale_model(
    invalid_model,
) -> None:
    """Public builder must reject objects outside its explicit model contract."""

    with pytest.raises(
        TypeError,
        match="model must be an FLiBeMultiscaleCoolantModel",
    ):
        build_flibe_multiscale_coolant_state(
            invalid_model,
            _configuration(),
        )


@pytest.mark.parametrize(
    "invalid_configuration",
    (None, True, False, 1, 1.0, "configuration", (), [], {}),
)
def test_public_builder_preserves_configuration_validation(
    invalid_configuration,
) -> None:
    """Public builder must preserve FLiBe configuration type validation."""

    with pytest.raises(
        TypeError,
        match="configuration must be an FLiBeConfiguration",
    ):
        build_flibe_multiscale_coolant_state(
            _model(),
            invalid_configuration,
        )


def test_public_builder_preserves_periodic_unwrapped_requirement() -> None:
    """Public builder must not bypass the explicit periodic-position boundary."""

    with pytest.raises(
        ValueError,
        match="explicit unwrapped positions",
    ):
        build_flibe_multiscale_coolant_state(
            _model(),
            _configuration(periodic=(True, False, False)),
        )


def test_multilevel_result_preserves_staged_partition_structure() -> None:
    """Stored hierarchy states must retain adjacent partitions rather than flattening them."""

    result = _model().build_state(_configuration())

    assert result.state_at(1).partition.fine_to_coarse == (0, 0, 1, 1)
    assert result.state_at(2).partition.fine_to_coarse == (0, 0)
    assert result.coarsest_state.partition != result.hierarchy.composed_partition()


def test_scale_coarse_graining_is_deterministic_for_same_inputs() -> None:
    """Identical explicit structural inputs must produce equal hierarchy states."""

    model = _model()
    configuration = _configuration()

    first = model.build_state(configuration)
    second = model.build_state(configuration)

    assert first == second


def test_changed_partition_changes_coarse_state_structure() -> None:
    """Different explicit scale mappings may produce distinct coarse states."""

    configuration = _configuration()

    first = FLiBeMultiscaleCoolantModel(
        hierarchy=MultiscaleHierarchy(
            partitions=(
                MultiscalePartition(
                    fine_to_coarse=(0, 0, 1, 1),
                ),
            )
        ),
        mass_parameters=_mass_parameters(),
    ).build_state(configuration)

    second = FLiBeMultiscaleCoolantModel(
        hierarchy=MultiscaleHierarchy(
            partitions=(
                MultiscalePartition(
                    fine_to_coarse=(0, 1, 0, 1),
                ),
            )
        ),
        mass_parameters=_mass_parameters(),
    ).build_state(configuration)

    assert first != second


def test_changed_mass_contract_changes_coarse_mass_state() -> None:
    """Explicit mass parameters must remain active inputs to coarse-scale state."""

    configuration = _configuration()

    first = FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(scale=1.0),
    ).build_state(configuration)

    second = FLiBeMultiscaleCoolantModel(
        hierarchy=_hierarchy(),
        mass_parameters=_mass_parameters(scale=2.0),
    ).build_state(configuration)

    assert first.coarsest_state.masses == (15.0,)
    assert second.coarsest_state.masses == (30.0,)
    assert first != second
