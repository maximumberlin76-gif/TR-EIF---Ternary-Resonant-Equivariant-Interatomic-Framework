"""Qualification tests for the complete TR-EIF root JSON Schema set."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


_SCHEMA_DIRECTORY = (
    Path(__file__).resolve().parents[2]
    / "schemas"
)

_EXPECTED_SCHEMA_FILES = (
    "configuration.schema.json",
    "resonance_state.schema.json",
    "ternary_state.schema.json",
    "transition_trace.schema.json",
    "energy_output.schema.json",
    "observables.schema.json",
    "model_manifest.schema.json",
)

_DRAFT_2020_12 = (
    "https://json-schema.org/draft/2020-12/schema"
)


def _schema_path(
    filename: str,
) -> Path:
    """Return the absolute path of one committed root schema."""

    return (
        _SCHEMA_DIRECTORY
        / filename
    )


def _load_schema(
    filename: str,
) -> dict[str, object]:
    """Load one committed JSON Schema object."""

    path = _schema_path(
        filename
    )

    document = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    assert isinstance(
        document,
        dict,
    )

    return document


def _schema_with_local_id(
    filename: str,
) -> dict[str, object]:
    """Return one schema with a local retrieval URI for reference resolution."""

    schema = _load_schema(
        filename
    )

    if "$id" not in schema:
        schema = dict(
            schema
        )
        schema["$id"] = (
            _schema_path(
                filename
            ).as_uri()
        )

    return schema


def _registry() -> Registry:
    """Build a registry containing every committed TR-EIF root schema."""

    registry = Registry()

    for filename in _EXPECTED_SCHEMA_FILES:
        schema = _schema_with_local_id(
            filename
        )

        registry = registry.with_resource(
            _schema_path(
                filename
            ).as_uri(),
            Resource.from_contents(
                schema
            ),
        )

    return registry


def _validator(
    filename: str,
) -> Draft202012Validator:
    """Construct one Draft 2020-12 validator with local references enabled."""

    schema = _schema_with_local_id(
        filename
    )

    Draft202012Validator.check_schema(
        schema
    )

    return Draft202012Validator(
        schema,
        registry=_registry(),
    )


def _collect_refs(
    value: object,
) -> tuple[str, ...]:
    """Collect every JSON Schema reference recursively."""

    refs: list[str] = []

    def visit(
        node: object,
    ) -> None:
        if isinstance(
            node,
            dict,
        ):
            reference = node.get(
                "$ref"
            )

            if isinstance(
                reference,
                str,
            ):
                refs.append(
                    reference
                )

            for child in node.values():
                visit(
                    child
                )

        elif isinstance(
            node,
            list,
        ):
            for child in node:
                visit(
                    child
                )

    visit(
        value
    )

    return tuple(
        refs
    )


def test_root_schema_set_is_complete() -> None:
    """The committed root schema set must match the approved repository plan."""

    actual = tuple(
        sorted(
            path.name
            for path in _SCHEMA_DIRECTORY.glob(
                "*.schema.json"
            )
        )
    )

    expected = tuple(
        sorted(
            _EXPECTED_SCHEMA_FILES
        )
    )

    assert actual == expected


def test_every_root_schema_declares_draft_2020_12() -> None:
    """Every root schema must use the same explicit JSON Schema dialect."""

    for filename in _EXPECTED_SCHEMA_FILES:
        schema = _load_schema(
            filename
        )

        assert (
            schema["$schema"]
            == _DRAFT_2020_12
        )


def test_every_root_schema_is_schema_valid() -> None:
    """Every committed root schema must itself satisfy Draft 2020-12."""

    for filename in _EXPECTED_SCHEMA_FILES:
        Draft202012Validator.check_schema(
            _schema_with_local_id(
                filename
            )
        )


def test_every_external_schema_reference_resolves_locally() -> None:
    """Cross-file references must resolve inside the committed root schema set."""

    expected = set(
        _EXPECTED_SCHEMA_FILES
    )

    for filename in _EXPECTED_SCHEMA_FILES:
        schema = _load_schema(
            filename
        )

        for reference in _collect_refs(
            schema
        ):
            target = reference.split(
                "#",
                1,
            )[0]

            if not target:
                continue

            if "://" in target:
                continue

            if not target.endswith(
                ".schema.json"
            ):
                continue

            target_name = Path(
                target
            ).name

            assert target_name in expected

            assert _schema_path(
                target_name
            ).is_file()


def test_configuration_schema_accepts_reference_configuration() -> None:
    """The root schema set must retain the qualified configuration contract."""

    instance = {
        "species": [
            "Li",
            "Be",
            "F",
        ],
        "positions": [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        "cell": [
            [4.0, 0.0, 0.0],
            [0.0, 4.0, 0.0],
            [0.0, 0.0, 4.0],
        ],
        "periodic": [
            True,
            True,
            True,
        ],
    }

    _validator(
        "configuration.schema.json"
    ).validate(
        instance
    )


def test_resonance_state_schema_accepts_continuous_state() -> None:
    """Resonance state must remain a continuous oscillator-state artifact."""

    instance = {
        "phases": [
            0.0,
            1.0,
            2.0,
        ],
        "frequencies": [
            -0.1,
            0.0,
            0.1,
        ],
    }

    _validator(
        "resonance_state.schema.json"
    ).validate(
        instance
    )


def test_active_ternary_state_schema_accepts_all_retained_states() -> None:
    """The canonical retained execution states must remain exactly -1/0/1."""

    validator = _validator(
        "ternary_state.schema.json"
    )

    for retained_state in (
        -1,
        0,
        1,
    ):
        validator.validate(
            {
                "retained_state": retained_state,
                "pending_target": None,
            }
        )


def test_active_neutral_state_accepts_pending_opposite_target() -> None:
    """Active neutral 0 must support explicitly staged nonneutral targets."""

    validator = _validator(
        "ternary_state.schema.json"
    )

    validator.validate(
        {
            "retained_state": 0,
            "pending_target": -1,
        }
    )

    validator.validate(
        {
            "retained_state": 0,
            "pending_target": 1,
        }
    )


def test_nonzero_retained_state_rejects_pending_target() -> None:
    """Pending routing must not be attached to an already nonneutral state."""

    validator = _validator(
        "ternary_state.schema.json"
    )

    assert not validator.is_valid(
        {
            "retained_state": -1,
            "pending_target": 1,
        }
    )

    assert not validator.is_valid(
        {
            "retained_state": 1,
            "pending_target": -1,
        }
    )


def test_active_neutral_is_not_a_pending_target() -> None:
    """Pending target 0 must remain forbidden because pending != active neutral."""

    validator = _validator(
        "ternary_state.schema.json"
    )

    assert not validator.is_valid(
        {
            "retained_state": 0,
            "pending_target": 0,
        }
    )


def test_energy_output_schema_accepts_conservative_energy_state() -> None:
    """The energy wire contract must retain atomic and total scalar energies."""

    instance = {
        "atomic_energies": [
            1.0,
            2.0,
        ],
        "total_energy": 3.0,
    }

    _validator(
        "energy_output.schema.json"
    ).validate(
        instance
    )


def test_observable_bundle_resolves_energy_schema_reference() -> None:
    """Observable validation must resolve its external energy-schema reference."""

    instance = {
        "node_count": 2,
        "energy": {
            "atomic_energies": [
                1.0,
                2.0,
            ],
            "total_energy": 3.0,
        },
        "forces": {
            "forces": [
                [1.0, 0.0, 0.0],
                [-1.0, 0.0, 0.0],
            ]
        },
        "stress": {
            "tensor": [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        },
    }

    _validator(
        "observables.schema.json"
    ).validate(
        instance
    )


def test_missing_observable_is_null_not_ternary_zero() -> None:
    """Absent physical observables must use JSON null rather than active state 0."""

    validator = _validator(
        "observables.schema.json"
    )

    valid_instance = {
        "node_count": 1,
        "energy": None,
        "forces": None,
        "stress": None,
    }

    validator.validate(
        valid_instance
    )

    invalid_instance = {
        "node_count": 1,
        "energy": 0,
        "forces": None,
        "stress": None,
    }

    assert not validator.is_valid(
        invalid_instance
    )


def test_transition_trace_resolves_active_ternary_reference() -> None:
    """Trace validation must resolve ternary-state schema across files."""

    instance = {
        "format": "tr_eif.trace",
        "version": 1,
        "record_count": 1,
        "node_count": 2,
        "records": [
            {
                "step": 0,
                "time": 0.0,
                "node_count": 2,
                "ternary_execution": [
                    {
                        "retained_state": -1,
                        "pending_target": None,
                    },
                    {
                        "retained_state": 0,
                        "pending_target": 1,
                    },
                ],
                "energy": {
                    "atomic_energies": [
                        1.0,
                        2.0,
                    ],
                    "total_energy": 3.0,
                },
                "forces": {
                    "forces": [
                        [1.0, 0.0, 0.0],
                        [-1.0, 0.0, 0.0],
                    ]
                },
                "stress": None,
            }
        ],
    }

    _validator(
        "transition_trace.schema.json"
    ).validate(
        instance
    )


def test_transition_trace_rejects_invalid_pending_state() -> None:
    """Trace schema must preserve active-neutral pending-target semantics."""

    instance = {
        "format": "tr_eif.trace",
        "version": 1,
        "record_count": 1,
        "node_count": 1,
        "records": [
            {
                "step": 0,
                "time": 0.0,
                "node_count": 1,
                "ternary_execution": [
                    {
                        "retained_state": 1,
                        "pending_target": -1,
                    }
                ],
                "energy": None,
                "forces": None,
                "stress": None,
            }
        ],
    }

    assert not _validator(
        "transition_trace.schema.json"
    ).is_valid(
        instance
    )


def test_model_manifest_schema_accepts_tr_eip_fixture() -> None:
    """The manifest schema must represent one concrete TR-EIP realization."""

    instance = {
        "format": "tr_eif.model_manifest",
        "schema_version": 1,
        "model_family": "TR-EIP",
        "model_family_version": "TEST_FIXTURE:1",
        "architecture_id": "TEST_FIXTURE:tr-eip-architecture",
        "parameter_artifact": None,
        "supported_species": [
            "Li",
            "Be",
            "F",
        ],
        "unit_system_id": "TEST_FIXTURE:units",
        "symmetry_group": "E(3)",
        "graph_rule": {
            "rule_id": "TEST_FIXTURE:cutoff-graph",
            "cutoff": 1.6,
        },
        "representation": {
            "representation_id": "TEST_FIXTURE:scalar-polar-vector",
            "scalar_channels": 3,
            "polar_vector_channels": 1,
            "higher_order_channels": 0,
        },
        "message_depth": 1,
        "resonance": {
            "structure_id": "TEST_FIXTURE:continuous-resonance",
            "descriptor_id": "TEST_FIXTURE:resonance-descriptor",
            "state_domain": "continuous",
        },
        "ternary": {
            "structure_id": "TEST_FIXTURE:balanced-ternary",
            "canonical_states": [
                -1,
                0,
                1,
            ],
            "active_neutral_state": 0,
            "direct_opposite_committed_transitions": False,
        },
        "capabilities": {
            "energy": True,
            "forces": True,
            "stress": True,
        },
        "numerical_semantics": {
            "precision_id": "TEST_FIXTURE:python-float",
            "differentiation_id": "TEST_FIXTURE:central-difference",
            "determinism_id": "TEST_FIXTURE:canonical-order",
        },
        "provenance": "TEST_FIXTURE",
    }

    _validator(
        "model_manifest.schema.json"
    ).validate(
        instance
    )


def test_model_manifest_rejects_binary_reduction_of_ternary_contract() -> None:
    """A concrete manifest must retain the complete -1/0/1 state space."""

    instance = {
        "format": "tr_eif.model_manifest",
        "schema_version": 1,
        "model_family": "TR-EIP",
        "model_family_version": "TEST_FIXTURE:1",
        "architecture_id": "TEST_FIXTURE:tr-eip-architecture",
        "parameter_artifact": None,
        "supported_species": [
            "Li",
            "Be",
            "F",
        ],
        "unit_system_id": "TEST_FIXTURE:units",
        "symmetry_group": "E(3)",
        "graph_rule": {
            "rule_id": "TEST_FIXTURE:cutoff-graph",
            "cutoff": 1.6,
        },
        "representation": {
            "representation_id": "TEST_FIXTURE:scalar-polar-vector",
            "scalar_channels": 3,
            "polar_vector_channels": 1,
            "higher_order_channels": 0,
        },
        "message_depth": 1,
        "resonance": {
            "structure_id": "TEST_FIXTURE:continuous-resonance",
            "descriptor_id": "TEST_FIXTURE:resonance-descriptor",
            "state_domain": "continuous",
        },
        "ternary": {
            "structure_id": "TEST_FIXTURE:balanced-ternary",
            "canonical_states": [
                -1,
                1,
            ],
            "active_neutral_state": 0,
            "direct_opposite_committed_transitions": False,
        },
        "capabilities": {
            "energy": True,
            "forces": True,
            "stress": True,
        },
        "numerical_semantics": {
            "precision_id": "TEST_FIXTURE:python-float",
            "differentiation_id": "TEST_FIXTURE:central-difference",
            "determinism_id": "TEST_FIXTURE:canonical-order",
        },
        "provenance": "TEST_FIXTURE",
    }

    assert not _validator(
        "model_manifest.schema.json"
    ).is_valid(
        instance
    )
