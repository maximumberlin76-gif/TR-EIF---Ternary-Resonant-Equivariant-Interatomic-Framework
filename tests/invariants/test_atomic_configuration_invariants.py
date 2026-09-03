"""Qualification tests for TR-EIF atomic-configuration invariants."""

import pytest

from tr_eif.configuration import AtomicConfiguration


def test_configuration_requires_at_least_one_atom() -> None:
    """Atomic configuration must not be empty."""

    with pytest.raises(
        ValueError,
        match="must contain at least one atom",
    ):
        AtomicConfiguration(
            species=(),
            positions=(),
        )


def test_species_and_positions_must_have_equal_length() -> None:
    """Species and Cartesian positions must describe the same atoms."""

    with pytest.raises(
        ValueError,
        match="must contain the same number of atoms",
    ):
        AtomicConfiguration(
            species=("A", "B"),
            positions=(
                (0.0, 0.0, 0.0),
            ),
        )


@pytest.mark.parametrize(
    "invalid_species",
    (
        "",
        "   ",
        "\t",
        "\n",
    ),
)
def test_species_labels_must_not_be_empty(
    invalid_species: str,
) -> None:
    """Species labels must contain non-whitespace text."""

    with pytest.raises(
        ValueError,
        match=r"species\[0\] must not be empty",
    ):
        AtomicConfiguration(
            species=(invalid_species,),
            positions=(
                (0.0, 0.0, 0.0),
            ),
        )


@pytest.mark.parametrize(
    "invalid_species",
    (
        1,
        1.0,
        None,
        True,
    ),
)
def test_species_labels_must_be_strings(
    invalid_species,
) -> None:
    """Species entries must be strings."""

    with pytest.raises(
        TypeError,
        match=r"species\[0\] must be a string",
    ):
        AtomicConfiguration(
            species=(invalid_species,),
            positions=(
                (0.0, 0.0, 0.0),
            ),
        )


@pytest.mark.parametrize(
    "position",
    (
        (0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    ),
)
def test_positions_require_three_cartesian_components(
    position,
) -> None:
    """Each atomic position must be a three-component Cartesian vector."""

    with pytest.raises(
        ValueError,
        match=r"positions\[0\] must contain exactly three components",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(position,),
        )


def test_periodic_flags_require_three_axes() -> None:
    """Periodic boundary specification must contain three axis flags."""

    with pytest.raises(
        ValueError,
        match="periodic must contain exactly three boolean flags",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (0.0, 0.0, 0.0),
            ),
            periodic=(True, False),
        )


@pytest.mark.parametrize(
    "periodic",
    (
        (1, False, False),
        (False, 0, False),
        (False, False, None),
    ),
)
def test_periodic_axes_require_boolean_flags(
    periodic,
) -> None:
    """Periodic-axis entries must be explicit boolean values."""

    with pytest.raises(
        TypeError,
        match="periodic must contain only boolean flags",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (0.0, 0.0, 0.0),
            ),
            periodic=periodic,
        )


@pytest.mark.parametrize(
    "periodic",
    (
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, True),
    ),
)
def test_periodic_configuration_requires_cell(
    periodic,
) -> None:
    """Any enabled periodic axis requires an explicit simulation cell."""

    with pytest.raises(
        ValueError,
        match="simulation cell is required",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (0.0, 0.0, 0.0),
            ),
            periodic=periodic,
        )


@pytest.mark.parametrize(
    "cell",
    (
        (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
        ),
        (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 1.0),
        ),
    ),
)
def test_cell_requires_three_lattice_vectors(
    cell,
) -> None:
    """Simulation cell must contain exactly three lattice vectors."""

    with pytest.raises(
        ValueError,
        match="cell must contain exactly three lattice vectors",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (0.0, 0.0, 0.0),
            ),
            cell=cell,
        )


def test_cell_requires_nonzero_volume() -> None:
    """Linearly dependent lattice vectors must be rejected."""

    with pytest.raises(
        ValueError,
        match="must define a nonzero volume",
    ):
        AtomicConfiguration(
            species=("A",),
            positions=(
                (0.0, 0.0, 0.0),
            ),
            cell=(
                (1.0, 0.0, 0.0),
                (2.0, 0.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
        )


def test_valid_nonperiodic_configuration_preserves_state() -> None:
    """A valid finite nonperiodic configuration must preserve its data."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 2.0, 3.0),
        ),
    )

    assert configuration.atom_count == 2
    assert not configuration.is_periodic
    assert configuration.cell is None
    assert configuration.periodic == (
        False,
        False,
        False,
    )


def test_valid_periodic_configuration_reports_periodicity() -> None:
    """A valid periodic configuration must expose its periodic state."""

    configuration = AtomicConfiguration(
        species=("A",),
        positions=(
            (0.25, 0.50, 0.75),
        ),
        cell=(
            (4.0, 0.0, 0.0),
            (0.0, 5.0, 0.0),
            (0.0, 0.0, 6.0),
        ),
        periodic=(
            True,
            False,
            True,
        ),
    )

    assert configuration.atom_count == 1
    assert configuration.is_periodic
    assert configuration.periodic == (
        True,
        False,
        True,
    )
