
"""FLiBe rank-two TR-EIP density and registered-state comparison benchmark.

Execute a prescribed seven-atom rank-two molecular-dynamics schedule, sample
post-barostat density, kinetic temperature and signed pressure, and compare
those observations with registered experimental and first-principles tables.

Each source row retains its identity, provenance, uncertainties and complete
physical-coordinate correspondence flags. Source residuals are recorded only
for rows satisfying the comparison contract. Resonance and ternary event
clocks remain distinct from mechanical sampling and barostat control inputs.
"""

from __future__ import annotations

import json
from math import fsum, isclose, isfinite
from pathlib import Path

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
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
from tr_eif.flibe.coupled_rank_two_tr_eip_md import (
    execute_flibe_rank_two_tr_eip_coupled_md_step,
)
from tr_eif.flibe.rank_two_tr_eip import FLiBeRankTwoTREIPModel
from tr_eif.flibe.rank_two_tr_eip_kinetic_barostat import (
    evaluate_flibe_rank_two_tr_eip_pressure,
)
from tr_eif.flibe.rank_two_tr_eip_pressure_coupled_observables import (
    evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables,
)
from tr_eif.flibe.rank_two_tr_eip_pressure_coupled_trajectory import (
    FLiBeRankTwoTREIPPressureCoupledInterval,
    run_flibe_rank_two_tr_eip_pressure_coupled_trajectory,
)
from tr_eif.flibe.rank_two_tr_eip_registered_density_correspondence import (
    compare_flibe_rank_two_registered_density,
)
from tr_eif.flibe.rank_two_tr_eip_stress import (
    evaluate_flibe_rank_two_tr_eip_md_stresses,
)
from tr_eif.flibe.registered_density_cross_model import (
    MODEL_DENSITY_STATISTIC,
    FLiBeDensityObservableMapping,
)
from tr_eif.flibe.registered_density_sources import load_flibe_density_source_records
from tr_eif.flibe.ternary_interpretation import FLiBeTernaryInterpretation
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.trajectory_pressure import FLiBeVelocityFrame
from tr_eif.flibe.units import ParameterProvenance, pressure_parameter
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
)


BENCHMARK_ID = "tr-eif.flibe.rank-two-registered-density-state-gate.v1"
MODEL_ID = "FLIBE-RANK-TWO-TR-EIP-ANALYTIC-MD-FIXTURE"
TRAJECTORY_ID = "FLIBE-RANK-TWO-THREE-INTERVAL-MD"
PROVENANCE = ParameterProvenance.BENCHMARK
SOURCE = "FLIBE-RANK-TWO-STATE-GATE-BENCHMARK"
ROOT = Path(__file__).resolve().parents[2]
SOURCES = (
    ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json",
    ROOT / "data/reference/flibe_baral_2021_aimd_density.json",
)
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0), (1.1, 0.7, 0.8), (1.7, 0.2, 0.5), (0.8, 1.5, 0.4),
)
CELL = ((8.0, 0.0, 0.0), (0.0, 8.0, 0.0), (0.0, 0.0, 8.0))
MASSES = (6.94, 6.94, 9.0121831, 18.998403163, 18.998403163,
          18.998403163, 18.998403163)
VELOCITIES = tuple(
    (0.001 * (i - 3), 0.0005 * ((i % 3) - 1), 0.00025 * (i % 2))
    for i in range(7)
)
MASS_TO_KG = 1.66053906660e-27
LENGTH_TO_M = 1.0e-10
TIME_TO_S = 1.0e-15
STRESS_TO_PA = 1.602176634e11
MECHANICAL_DT = 1.0e-4
CUTOFF = 1.6
COUPLING_TIME = 4.0e-4
COMPRESSIBILITY = 2.0e-14
VELOCITY_FRAME = FLiBeVelocityFrame.CENTER_OF_MASS


def _model_and_state():
    state = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(
                species=SPECIES, positions=POSITIONS,
                cell=CELL, periodic=(True, True, True),
            ),
            velocities=VELOCITIES, masses=MASSES, step=4, time=0.3,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
            frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states(
            (TernaryState.NEGATIVE,) * 7,
        ),
        resonance_time=0.4, resonance_step_count=2, ternary_event_count=5,
    )
    base = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.25 * i,),
            vectors=((1.0, 0.1 * i, -0.05 * i),),
        )
        for i in range(7)
    ))
    tensors = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor((
            (1.0 + 0.1 * i, 0.2, -0.3),
            (0.4, 0.8 - 0.05 * i, 0.1),
            (-0.2, 0.3, 0.6),
        )),
        RankTwoTensor.outer(
            (1.0, 0.25 * i - 0.5, 0.3), (0.2, 0.8, -0.1 * i),
        ),
    ) for i in range(7)))
    features = ScalarVectorTensorFeatures(base, tensors)
    reference = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3), bias=0.1,
        ),
    )
    weights = (
        RankTwoChannelEnergyWeights(
            trace=0.15, isotropic_norm_squared=0.08,
            symmetric_traceless_norm_squared=0.3,
            antisymmetric_norm_squared=0.2,
        ),
        RankTwoChannelEnergyWeights(
            trace=-0.12, isotropic_norm_squared=0.05,
            symmetric_traceless_norm_squared=-0.08,
            antisymmetric_norm_squared=0.1,
        ),
    )
    model = FLiBeRankTwoTREIPModel(
        tr_eip_model=FLiBeTREIPModel(reference, PROVENANCE),
        rank_two_model=RankTwoConservativeEnergyModel(
            reference_model=reference,
            tensor_readout=RankTwoInvariantEnergyReadout(weights),
            coupling=RankTwoMessageCoupling(
                tensor_scale=0.7, scalar_dyad_scale=0.2,
                vector_dyad_scale=-0.15,
                scalar_channel_index=0, vector_channel_index=0,
            ),
        ),
    )
    resources = dict(
        model=model,
        force_evaluator=RankTwoConservativeForceEvaluator(
            CoordinateDifferentiation(step=1.0e-5),
        ),
        stress_evaluator=RankTwoConservativeStressEvaluator(
            CellStrainDifferentiation(step=1.0e-6),
        ),
        features=features,
        thermodynamic_state=FLiBeThermodynamicState(850.0, 101325.0),
        interpretation=FLiBeTernaryInterpretation(
            projection=ResonanceProjection(1.0, -0.1),
            thresholds=TernaryTargetThresholds(negative=-0.25, positive=0.5),
            provenance=PROVENANCE,
        ),
        cutoff=CUTOFF,
    )
    return state, resources


def _observed_trajectory():
    state, resources = _model_and_state()
    phase_parameters = PhaseDynamicsParameters(
        coupling=(0.35,) * 7, phase_lag=(0.13,) * 7,
    )
    schedule = (
        FLiBeRankTwoTREIPPressureCoupledInterval(
            mechanical_time_step=MECHANICAL_DT,
            phase_parameters=phase_parameters,
            phase_time_step=0.1,
            ternary_event=True,
        ),
        FLiBeRankTwoTREIPPressureCoupledInterval(
            mechanical_time_step=MECHANICAL_DT,
            ternary_event=True,
        ),
        FLiBeRankTwoTREIPPressureCoupledInterval(
            mechanical_time_step=MECHANICAL_DT,
            phase_parameters=phase_parameters,
            phase_time_step=0.05,
        ),
    )
    first = execute_flibe_rank_two_tr_eip_coupled_md_step(
        state,
        model=resources["model"],
        force_evaluator=resources["force_evaluator"],
        features=resources["features"],
        thermodynamic_state=resources["thermodynamic_state"],
        interpretation=resources["interpretation"],
        cutoff=resources["cutoff"],
        phase_parameters=phase_parameters,
        phase_time_step=0.1,
        ternary_event=True,
        mechanical_time_step=MECHANICAL_DT,
    )
    stress = evaluate_flibe_rank_two_tr_eip_md_stresses(
        first, resources["model"], resources["stress_evaluator"],
    )
    pressure = evaluate_flibe_rank_two_tr_eip_pressure(
        stress,
        mass_unit_to_kg=MASS_TO_KG,
        coordinate_unit_to_meter=LENGTH_TO_M,
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=STRESS_TO_PA,
        velocity_frame=VELOCITY_FRAME,
        provenance=PROVENANCE,
        source=SOURCE,
    )
    target = pressure_parameter(
        max(101325.0, pressure.total_pressure.value + 100_000_000.0),
        PROVENANCE,
    )
    trajectory = run_flibe_rank_two_tr_eip_pressure_coupled_trajectory(
        state,
        schedule=schedule,
        **resources,
        target_pressure=target,
        mass_unit_to_kg=MASS_TO_KG,
        coordinate_unit_to_meter=LENGTH_TO_M,
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=STRESS_TO_PA,
        velocity_frame=VELOCITY_FRAME,
        compressibility_per_pascal=COMPRESSIBILITY,
        coupling_time=COUPLING_TIME,
        provenance=PROVENANCE,
        source=SOURCE,
    )
    observable = evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables(
        trajectory,
        energy_unit_to_joule=STRESS_TO_PA * LENGTH_TO_M**3,
        degrees_of_freedom=18,
    )
    return observable


def _source_report(observations, source_path: Path):
    records = load_flibe_density_source_records(source_path)
    mapping = FLiBeDensityObservableMapping(
        mapping_id="RANK-TWO-OBSERVED-DENSITY-STATE-CORRESPONDENCE",
        model_statistic_id=MODEL_DENSITY_STATISTIC,
        source_normalization_id="source-reported-mass-density",
        method_id="POST-BAROSTAT-MEAN-DENSITY-AND-OBSERVED-PRESSURE",
        provenance=PROVENANCE,
        assumptions=(
            "fixed-atom-mass-inventory",
            "mean-instantaneous-cell-density",
            "post-barostat-pressure-observation",
            "separate-resonance-ternary-mechanical-clocks",
        ),
    )
    report = compare_flibe_rank_two_registered_density(
        observations, records,
        model_id=MODEL_ID,
        trajectory_id=TRAJECTORY_ID,
        physical_state_id="DECLARED-ANALYTIC-FIXTURE-STATE",
        physical_state_method_id="ANALYTIC-FIXTURE-CLASSIFICATION",
        observed_pressure_method_id="POST-BAROSTAT-HYDROSTATIC-STRESS-AND-MOMENTUM",
        mapping=mapping,
        provenance=PROVENANCE,
        temperature_tolerance_k=1.0e-8,
        pressure_tolerance_pa=1.0e-5,
    )
    missing_counts = {
        axis: sum(axis in row.missing_source_axes for row in report.comparison.rows)
        for axis in ("pressure", "physical_state")
    }
    rows = tuple({
        "record_id": row.record_id,
        "temperature_k": row.source_record.coordinates.temperature_k,
        "density_kg_m3": row.source_record.coordinates.density_kg_m3,
        "density_standard_uncertainty_kg_m3": (
            row.source_record.coordinates.density_standard_uncertainty_kg_m3
        ),
        "temperature_standard_uncertainty_k": (
            row.source_record.coordinates.temperature_standard_uncertainty_k
        ),
        "pressure_standard_uncertainty_pa": (
            row.source_record.coordinates.pressure_standard_uncertainty_pa
        ),
        "bef2_fraction_standard_uncertainty": (
            row.source_record.coordinates.bef2_fraction_standard_uncertainty
        ),
        "lif_formula_fraction": row.source_record.coordinates.composition.lif_fraction,
        "bef2_formula_fraction": row.source_record.coordinates.composition.bef2_fraction,
        "pressure_pa": row.source_record.coordinates.pressure_pa,
        "physical_state_id": row.source_record.coordinates.physical_state_id,
        "source_location": row.source_record.source_location,
        "method_id": row.source_record.coordinates.method_id,
        "source_values": row.source_record.source_values,
        "matched_axes": row.matched_axes,
        "unmatched_axes": row.unmatched_axes,
        "missing_source_axes": row.missing_source_axes,
        "density_residual_kg_m3": row.density_residual_kg_m3,
    } for row in report.comparison.rows)
    matched_metrics = report.comparison.residual_metrics
    return {
        "dataset_id": records[0].dataset_id,
        "doi": records[0].doi,
        "source_file_sha256": records[0].source_file_sha256,
        "source_evidence_kind": records[0].coordinates.evidence_kind.value,
        "source_row_count": len(records),
        "matched_source_row_count": report.matched_source_count,
        "unmatched_source_row_count": report.unmatched_source_count,
        "missing_source_axis_counts": missing_counts,
        "model_mean_density_kg_m3": (
            report.model_coordinates.density_trace.mean_density_kg_m3
        ),
        "model_mean_kinetic_temperature_k": (
            report.model_coordinates.mean_kinetic_temperature_k
        ),
        "model_mean_signed_observed_pressure_pa": report.mean_signed_pressure_pa,
        "model_pressure_coordinate_pa": (
            report.model_coordinates.pressure.pressure_pa
            if report.model_coordinates.pressure is not None else None
        ),
        "model_physical_state_id": report.model_coordinates.physical_state_id,
        "source_mapping_id": report.comparison.mapping.mapping_id,
        "temperature_tolerance_k": report.comparison.temperature_tolerance_k,
        "pressure_tolerance_pa": report.comparison.pressure_tolerance_pa,
        "matched_density_metrics": (
            {
                "count": matched_metrics.count,
                "mean_signed_kg_m3": matched_metrics.mean_signed_kg_m3,
                "mean_absolute_kg_m3": matched_metrics.mean_absolute_kg_m3,
                "root_mean_square_kg_m3": matched_metrics.root_mean_square_kg_m3,
                "maximum_absolute_kg_m3": matched_metrics.maximum_absolute_kg_m3,
            }
            if matched_metrics is not None else None
        ),
        "rows": rows,
        "source_record_order_preserved": all(
            row.record_id == record.record_id
            for row, record in zip(report.comparison.rows, records, strict=True)
        ),
        "density_residual_only_for_matched_state": all(
            (row.density_residual_kg_m3 is not None)
            == row.correspondence.coordinate_match
            for row in report.comparison.rows
        ),
        "source_metadata_preserved": all(
            row.source_record == original
            for row, original in zip(report.comparison.rows, records, strict=True)
        ),
    }


def run_benchmark() -> dict[str, object]:
    """Execute the prescribed MD fixture and serialize source-resolved evidence."""
    observations = _observed_trajectory()
    trajectory = observations.trajectory
    source_reports = tuple(_source_report(observations, path) for path in SOURCES)
    samples = tuple({
        "interval_index": sample.interval_index,
        "md_step": sample.md_step,
        "md_time_s": sample.md_time_s,
        "density_kg_m3": sample.density_kg_m3,
        "volume_m3": sample.volume_m3,
        "kinetic_temperature_k": sample.kinetic_temperature_k,
        "signed_observed_pressure_pa": sample.total_pressure_pa,
        "resonance_step_count": sample.resonance_step_count,
        "ternary_event_count": sample.ternary_event_count,
        "retained_states": tuple(int(state) for state in sample.retained_states),
        "pending_target_count": sample.pending_target_count,
    } for sample in observations.samples)
    checks = {
        "three_mechanical_intervals": trajectory.interval_count == 3,
        "registered_source_cardinalities": tuple(
            item["source_row_count"] for item in source_reports
        ) == (61, 9),
        "source_record_order": all(
            item["source_record_order_preserved"] for item in source_reports
        ),
        "source_row_metadata": all(
            item["source_metadata_preserved"] for item in source_reports
        ),
        "density_residual_domain": all(
            item["density_residual_only_for_matched_state"]
            for item in source_reports
        ),
        "fixed_mass_inventory": all(
            state.md_state.masses == trajectory.initial.md_state.masses
            for state in trajectory.states
        ),
        "neutral_mediation": (
            observations.samples[0].retained_states
            == (TernaryState.NEUTRAL,) * 7
            and observations.samples[0].pending_target_count == 7
            and observations.samples[1].retained_states
            == (TernaryState.POSITIVE,) * 7
        ),
        "signed_observed_pressures": all(
            isfinite(sample.total_pressure_pa)
            and isclose(
                sample.total_pressure_pa,
                fsum((sample.kinetic_pressure_pa,
                      sample.configurational_pressure_pa)),
                rel_tol=1e-12, abs_tol=1e-6,
            )
            for sample in observations.samples
        ),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "model_id": MODEL_ID,
        "trajectory_id": TRAJECTORY_ID,
        "provenance": PROVENANCE.value,
        "source_ids": tuple(item["dataset_id"] for item in source_reports),
        "barostat_target_pressure_pa": trajectory.target_pressure.value,
        "observed_state_samples": samples,
        "source_comparisons": source_reports,
        "checks": checks,
    }


def main() -> None:
    result = run_benchmark()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if not all(result["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
