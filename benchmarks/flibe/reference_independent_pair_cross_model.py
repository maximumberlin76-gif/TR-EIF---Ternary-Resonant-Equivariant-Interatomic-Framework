"""Matched finite-cluster comparison of FLiBe TR-EIP and an independent pair model.

Both models receive identical ordered atomic positions. A caller-supplied
energy conversion maps the TR-EIP native energy unit to hartree, while both
force outputs use hartree per input Cartesian coordinate unit. Source and
parameter identities remain attached to every numerical comparison.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import fsum, isclose, isfinite, pi, sqrt

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator, CoordinateDifferentiation,
    LinearInvariantEnergyFunctional, ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    NodeFeatures, NodeFeatureVector, RadialMessageOperator, TernaryConditioning,
)
from tr_eif.flibe.charge import total_formal_charge
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.independent_pair_potential import (
    PAIR_ORDER, FLiBeIndependentPairModel, FLiBePairCoefficients,
)
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import TernaryExecutionVector, TernaryState


BENCHMARK_ID = "tr-eif.flibe.independent-pair-cross-model.v1"
STATE_ID = "FLIBE-SEVEN-ATOM-NONPERIODIC-FIXTURE"
ENERGY_TOLERANCE_HARTREE = 1.0e-9
FORCE_TOLERANCE_HARTREE_PER_COORDINATE = 3.0e-6
DIFFERENTIATION_STEP = 1.0e-6
GRAPH_CUTOFF = 1.6

# Independent analytic fixture totals at the declared geometry and parameters.
EXPECTED_PAIR_ENERGY_HARTREE = -2.7269592863955615
EXPECTED_TR_EIP_ENERGY_HARTREE = 8.175782059061284

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0), (1.1, 0.7, 0.8), (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
PHASES = tuple(index * pi / 4.0 for index in range(7))
FREQUENCIES = (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3)
EXECUTED = (-1, 0, 1, 0, -1, 1, 0)


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


@dataclass(frozen=True, slots=True)
class CrossModelUnitBridge:
    """Explicit Cartesian and energy-unit conversion with source provenance."""

    coordinate_unit_to_bohr: float
    tr_eip_native_energy_to_hartree: float
    provenance: ParameterProvenance
    source_id: str

    def __post_init__(self) -> None:
        _positive(self.coordinate_unit_to_bohr, "coordinate_unit_to_bohr")
        _positive(self.tr_eip_native_energy_to_hartree, "tr_eip_native_energy_to_hartree")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        _identifier(self.source_id, "source_id")


def compare_models(
    configuration: FLiBeConfiguration,
    tr_eip_model: FLiBeTREIPModel,
    pair_model: FLiBeIndependentPairModel,
    features: NodeFeatureVector,
    oscillator: ResonanceState,
    execution: TernaryExecutionVector,
    state: FLiBeThermodynamicState,
    bridge: CrossModelUnitBridge,
    *,
    reference_state_id: str,
    tr_eip_model_id: str,
    graph_cutoff: float,
    differentiation_step: float,
) -> dict[str, object]:
    """Evaluate and compare both models at one frozen atomic configuration.

    TR-EIP differentiation holds graph, descriptor and execution fixed.
    The pair model evaluates every unordered atom pair without a cutoff.
    All returned energies are hartree and all forces are hartree per input
    Cartesian coordinate unit after applying the supplied unit bridge.
    """
    if not isinstance(configuration, FLiBeConfiguration):
        raise TypeError("configuration must be FLiBeConfiguration.")
    if not isinstance(tr_eip_model, FLiBeTREIPModel):
        raise TypeError("tr_eip_model must be FLiBeTREIPModel.")
    if not isinstance(pair_model, FLiBeIndependentPairModel):
        raise TypeError("pair_model must be FLiBeIndependentPairModel.")
    if not isinstance(bridge, CrossModelUnitBridge):
        raise TypeError("bridge must be CrossModelUnitBridge.")
    if not isinstance(state, FLiBeThermodynamicState):
        raise TypeError("state must be FLiBeThermodynamicState.")
    if configuration.configuration.periodic != (False, False, False):
        raise ValueError("the paired comparison requires nonperiodic Cartesian boundaries.")
    if pair_model.length_unit_to_bohr != bridge.coordinate_unit_to_bohr:
        raise ValueError("pair model and comparison coordinate units must agree.")
    if oscillator.oscillator_count != configuration.atom_count:
        raise ValueError("oscillator count must equal atomic configuration cardinality.")

    _identifier(reference_state_id, "reference_state_id")
    _identifier(tr_eip_model_id, "tr_eip_model_id")
    cutoff = _positive(graph_cutoff, "graph_cutoff")
    step = _positive(differentiation_step, "differentiation_step")

    graph = build_cutoff_graph(configuration.configuration, cutoff=cutoff)
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=state,
        resonance_state=oscillator,
        provenance=tr_eip_model.provenance,
        source=tr_eip_model.source,
    )
    tr_output = tr_eip_model.evaluate(
        configuration=configuration, graph=graph, features=features,
        resonance=descriptor, execution=execution,
    )
    pair_output = pair_model.evaluate(configuration)

    tr_force = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(step=step)
    ).evaluate(
        tr_eip_model.energy_model, configuration.configuration, graph,
        tr_output.resonance_conditioned_features, execution,
    )

    conversion = bridge.tr_eip_native_energy_to_hartree
    tr_energy = tr_output.energy_result.energy.total_energy * conversion
    pair_energy = pair_output.energy.total_energy
    tr_forces = tuple(tuple(component * conversion for component in row)
                      for row in tr_force.forces)
    pair_forces = pair_output.forces.forces

    difference = tuple(
        tuple(tr_forces[i][axis] - pair_forces[i][axis] for axis in range(3))
        for i in range(configuration.atom_count)
    )
    flattened = tuple(component for row in difference for component in row)

    if not all(isfinite(value) for value in (tr_energy, pair_energy, *flattened)):
        raise ValueError("converted energies and forces must be finite.")

    return {
        "reference_state_id": reference_state_id,
        "model_ids": {"tr_eip": tr_eip_model_id, "pair": pair_model.model_id},
        "tr_eip_provenance": {
            "kind": tr_eip_model.provenance.value,
            "source": tr_eip_model.source,
        },
        "tr_eip_parameters": {
            "radial_distance_scale_input_unit":
                tr_eip_model.energy_model.message_operator.distance_scale,
            "ternary_conditioning": {
                "negative_scale":
                    tr_eip_model.energy_model.conditioning.negative_scale,
                "neutral_scale":
                    tr_eip_model.energy_model.conditioning.neutral_scale,
                "positive_scale":
                    tr_eip_model.energy_model.conditioning.positive_scale,
            },
            "scalar_weights": list(
                tr_eip_model.energy_model.energy_functional.weights
            ),
            "energy_bias": tr_eip_model.energy_model.energy_functional.bias,
            "initial_scalar_features": [
                list(node.scalars) for node in features.nodes
            ],
            "initial_vector_features": [
                [list(vec) for vec in node.vectors] for node in features.nodes
            ],
            "oscillator_phases": list(oscillator.phases),
            "oscillator_frequencies": list(oscillator.frequencies),
        },
        "atom_count": configuration.atom_count,
        "species": list(configuration.configuration.species),
        "positions": [
            list(row) for row in configuration.configuration.positions
        ],
        "periodic": list(configuration.configuration.periodic),
        "composition": {
            "lif_fraction": configuration.composition().lif_fraction,
            "bef2_fraction": configuration.composition().bef2_fraction,
        },
        "formal_charge": total_formal_charge(configuration),
        "thermodynamic_state": {
            "temperature_k": state.temperature,
            "pressure_pa": state.pressure,
        },
        "resonance": {
            "phase_order": descriptor.phase_order,
            "frequency_spread": descriptor.frequency_spread,
        },
        "retained_execution": [
            item.value for item in execution.retained_states
        ],
        "graph": {
            "tr_eip_cutoff_input_unit": cutoff,
            "tr_eip_directed_edges": graph.edge_count,
            "pair_unordered_pairs": pair_output.pair_count,
        },
        "units": {
            "energy": "hartree",
            "force": "hartree/input-coordinate-unit",
            "coordinate_unit_to_bohr": bridge.coordinate_unit_to_bohr,
            "tr_eip_native_energy_to_hartree": conversion,
            "provenance": bridge.provenance.value,
            "source_id": bridge.source_id,
        },
        "pair_coefficients": [
            {
                "species": [pair.species_a.value, pair.species_b.value],
                "born_amplitude_hartree": pair.born_amplitude_hartree,
                "born_decay_inverse_bohr": pair.born_decay_inverse_bohr,
                "c6_hartree_bohr6": pair.c6_hartree_bohr6,
                "c8_hartree_bohr8": pair.c8_hartree_bohr8,
                "b6_inverse_bohr": pair.b6_inverse_bohr,
                "b8_inverse_bohr": pair.b8_inverse_bohr,
                "provenance": pair.provenance.value,
                "source_id": pair.source_id,
                "source_location": pair.source_location,
            }
            for pair in pair_output.pair_coefficients
        ],
        "energies_hartree": {
            "tr_eip": tr_energy,
            "pair": pair_energy,
            "tr_eip_minus_pair": tr_energy - pair_energy,
            "tr_eip_atomic": [
                value * conversion
                for value in tr_output.energy_result.energy.atomic_energies
            ],
            "pair_atomic": list(pair_output.energy.atomic_energies),
        },
        "forces_hartree_per_coordinate": {
            "tr_eip": [list(row) for row in tr_forces],
            "pair": [list(row) for row in pair_forces],
            "tr_eip_minus_pair": [list(row) for row in difference],
            "component_rmse": sqrt(
                fsum(value * value for value in flattened) / len(flattened)
            ),
            "component_mae": (
                fsum(abs(value) for value in flattened) / len(flattened)
            ),
            "maximum_absolute_component": max(
                abs(value) for value in flattened
            ),
        },
        "differentiation_step_input_unit": step,
    }


def _fixture_model() -> FLiBeIndependentPairModel:
    coefficients = tuple(
        FLiBePairCoefficients(
            species_a=a,
            species_b=b,
            born_amplitude_hartree=0.12 + 0.025 * i,
            born_decay_inverse_bohr=0.60 + 0.07 * i,
            c6_hartree_bohr6=0.018 + 0.004 * i,
            c8_hartree_bohr8=0.005 + 0.001 * i,
            b6_inverse_bohr=0.90 + 0.10 * i,
            b8_inverse_bohr=1.00 + 0.10 * i,
            provenance=ParameterProvenance.TEST_FIXTURE,
            source_id="FLIBE-INDEPENDENT-PAIR-ANALYTIC-FIXTURE",
            source_location="benchmarks/flibe/reference_independent_pair_cross_model.py",
        )
        for i, (a, b) in enumerate(PAIR_ORDER)
    )

    return FLiBeIndependentPairModel(
        model_id="PAIR-COULOMB-BORN-MAYER-DAMPED-C6-C8",
        pair_coefficients=coefficients,
        length_unit_to_bohr=1.0,
    )


def _fixture_tr_eip_model() -> FLiBeTREIPModel:
    energy_model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5,
            neutral_scale=1.25,
            positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3),
            bias=0.1,
        ),
    )

    return FLiBeTREIPModel(
        energy_model=energy_model,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _fixture_features() -> NodeFeatureVector:
    return NodeFeatureVector(
        nodes=tuple(
            NodeFeatures(scalars=(0.5 + 0.25 * index,))
            for index in range(len(SPECIES))
        )
    )


def _fixture_execution() -> TernaryExecutionVector:
    return TernaryExecutionVector.from_retained_states(
        tuple(TernaryState(value) for value in EXECUTED)
    )


def _rotate_translate(
    vector: tuple[float, float, float],
) -> tuple[float, float, float]:
    return (
        -vector[1] + 3.0,
        vector[0] - 2.0,
        vector[2] + 1.25,
    )


def _rotate_force(
    vector: list[float],
) -> tuple[float, float, float]:
    return (-vector[1], vector[0], vector[2])


def _close_vector(
    first: list[float],
    second: tuple[float, float, float],
    tolerance: float,
) -> bool:
    return all(
        isclose(a, b, abs_tol=tolerance, rel_tol=0.0)
        for a, b in zip(first, second, strict=True)
    )


def run_benchmark() -> dict[str, object]:
    """Run a two-model test fixture and independently check its numeric contracts."""

    bridge = CrossModelUnitBridge(
        coordinate_unit_to_bohr=1.0,
        tr_eip_native_energy_to_hartree=0.5,
        provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="FLIBE-CROSS-MODEL-UNIT-FIXTURE",
    )

    tr_model = _fixture_tr_eip_model()
    pair_model = _fixture_model()
    features = _fixture_features()
    oscillator = ResonanceState(
        phases=PHASES,
        frequencies=FREQUENCIES,
    )
    execution = _fixture_execution()
    state = FLiBeThermodynamicState(
        temperature=1000.0,
        pressure=0.0,
    )

    def evaluate(positions):
        return compare_models(
            configuration=FLiBeConfiguration(
                AtomicConfiguration(
                    species=SPECIES,
                    positions=positions,
                )
            ),
            tr_eip_model=tr_model,
            pair_model=pair_model,
            features=features,
            oscillator=oscillator,
            execution=execution,
            state=state,
            bridge=bridge,
            reference_state_id=STATE_ID,
            tr_eip_model_id="TR-EIP-RESONANCE-CONDITIONED",
            graph_cutoff=GRAPH_CUTOFF,
            differentiation_step=DIFFERENTIATION_STEP,
        )

    first = evaluate(POSITIONS)
    replay = evaluate(POSITIONS)
    transformed = evaluate(
        tuple(_rotate_translate(position) for position in POSITIONS)
    )

    energies = first["energies_hartree"]
    forces = first["forces_hartree_per_coordinate"]
    energy_transformed = transformed["energies_hartree"]
    forces_transformed = transformed["forces_hartree_per_coordinate"]

    checks = {
        "matched_atomic_configuration": (
            first["species"] == list(SPECIES)
            and first["positions"] == [list(row) for row in POSITIONS]
        ),
        "exact_formula_composition": first["composition"] == {
            "lif_fraction": 2.0 / 3.0,
            "bef2_fraction": 1.0 / 3.0,
        },
        "formal_charge_balance": first["formal_charge"] == 0,
        "ternary_execution_retained": (
            first["retained_execution"] == list(EXECUTED)
        ),
        "independent_pair_cardinality": (
            first["graph"]["pair_unordered_pairs"] == 21
        ),
        "pair_energy_partition": isclose(
            energies["pair"],
            fsum(energies["pair_atomic"]),
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "tr_eip_energy_partition": isclose(
            energies["tr_eip"],
            fsum(energies["tr_eip_atomic"]),
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "independent_pair_energy_anchor": isclose(
            energies["pair"],
            EXPECTED_PAIR_ENERGY_HARTREE,
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "independent_tr_eip_energy_anchor": isclose(
            energies["tr_eip"],
            EXPECTED_TR_EIP_ENERGY_HARTREE,
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "signed_energy_difference": isclose(
            energies["tr_eip_minus_pair"],
            energies["tr_eip"] - energies["pair"],
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "exact_replay": first == replay,
        "pair_energy_e3": isclose(
            energies["pair"],
            energy_transformed["pair"],
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "tr_eip_energy_e3": isclose(
            energies["tr_eip"],
            energy_transformed["tr_eip"],
            rel_tol=0.0,
            abs_tol=ENERGY_TOLERANCE_HARTREE,
        ),
        "pair_force_e3": all(
            _close_vector(
                other,
                _rotate_force(original),
                FORCE_TOLERANCE_HARTREE_PER_COORDINATE,
            )
            for other, original in zip(
                forces_transformed["pair"],
                forces["pair"],
                strict=True,
            )
        ),
        "tr_eip_force_e3": all(
            _close_vector(
                other,
                _rotate_force(original),
                FORCE_TOLERANCE_HARTREE_PER_COORDINATE,
            )
            for other, original in zip(
                forces_transformed["tr_eip"],
                forces["tr_eip"],
                strict=True,
            )
        ),
        "pair_net_force": all(
            abs(fsum(row[axis] for row in forces["pair"]))
            <= FORCE_TOLERANCE_HARTREE_PER_COORDINATE
            for axis in range(3)
        ),
        "tr_eip_net_force": all(
            abs(fsum(row[axis] for row in forces["tr_eip"]))
            <= FORCE_TOLERANCE_HARTREE_PER_COORDINATE
            for axis in range(3)
        ),
    }

    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "comparison_kind":
            "resonance_conditioned_tr_eip_vs_independent_rigid_ion_pair",
        "provenance": "TEST_FIXTURE",
        "numeric_criteria": {
            "energy_absolute_tolerance_hartree":
                ENERGY_TOLERANCE_HARTREE,
            "force_absolute_tolerance_hartree_per_coordinate":
                FORCE_TOLERANCE_HARTREE_PER_COORDINATE,
        },
        "comparison": first,
        "checks": checks,
    }


if __name__ == "__main__":
    report = run_benchmark()
    print(json.dumps(
        report,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ))
    raise SystemExit(0 if report["status"] == "PASS" else 1)
