"""FLiBe rank-two TR-EIP pressure coupling after a scheduled MD interval.

The pre-event, post-event and post-mechanical full-energy stress records are
preserved. An independently supplied kinetic pressure and an explicitly
converted strain-derived potential pressure form the barostat input in Pa.
The isotropic affine cell update occurs after the mechanical clock and is
followed by a fresh energy/stress evaluation on the updated periodic graph.
Resonance and balanced-ternary execution remain at their last committed
states; pending targets and the separate thermodynamic coordinate are kept.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.barostat import (
    apply_isotropic_barostat,
    isotropic_barostat_scale,
    scale_periodic_configuration,
)
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState

from .configuration import FLiBeConfiguration
from .coordination import build_flibe_coordination_state
from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_stress import (
    FLiBeRankTwoTREIPMDStressTrace,
    FLiBeRankTwoTREIPStressResult,
    evaluate_flibe_rank_two_tr_eip_md_stresses,
    evaluate_flibe_rank_two_tr_eip_stress,
)
from .resonance_descriptor import build_flibe_resonance_descriptor
from .units import FLiBeUnit, PhysicalParameter


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")
    normalized = float(value)
    if not isfinite(normalized) or normalized <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return normalized


def _pressure_parameter(value: PhysicalParameter, name: str) -> float:
    if not isinstance(value, PhysicalParameter):
        raise TypeError(f"{name} must be a PhysicalParameter.")
    if value.unit is not FLiBeUnit.PASCAL:
        raise ValueError(f"{name} must be in Pa.")
    return value.value


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPBarostatStep:
    """Full-energy stress evidence and the affine pressure-coupling boundary."""

    stress_trace: FLiBeRankTwoTREIPMDStressTrace
    target_pressure: PhysicalParameter
    kinetic_pressure: PhysicalParameter
    potential_stress_unit_to_pascal: float
    compressibility_per_pascal: float
    coupling_time: float
    mechanical_time_step: float
    current_pressure_pa: float
    linear_scale: float
    current: CoupledMolecularDynamicsState
    after_barostat: FLiBeRankTwoTREIPStressResult

    def __post_init__(self) -> None:
        if not isinstance(self.stress_trace, FLiBeRankTwoTREIPMDStressTrace):
            raise TypeError("stress_trace must be FLiBeRankTwoTREIPMDStressTrace.")
        target = _pressure_parameter(self.target_pressure, "target_pressure")
        kinetic = _pressure_parameter(self.kinetic_pressure, "kinetic_pressure")
        if kinetic < 0.0:
            raise ValueError("kinetic_pressure must be nonnegative.")
        conversion = _positive(
            self.potential_stress_unit_to_pascal, "potential_stress_unit_to_pascal"
        )
        beta = _positive(self.compressibility_per_pascal, "compressibility_per_pascal")
        tau = _positive(self.coupling_time, "coupling_time")
        dt = _positive(self.mechanical_time_step, "mechanical_time_step")
        scale = _positive(self.linear_scale, "linear_scale")
        if not isinstance(self.current, CoupledMolecularDynamicsState):
            raise TypeError("current must be CoupledMolecularDynamicsState.")
        if not isinstance(self.after_barostat, FLiBeRankTwoTREIPStressResult):
            raise TypeError("after_barostat must be FLiBeRankTwoTREIPStressResult.")

        coupled = self.stress_trace.coupled.coupled_step
        previous = coupled.previous
        mechanical = coupled.current
        if coupled.mechanical_update is None:
            raise ValueError("barostat step requires a completed mechanical interval.")
        actual_dt = mechanical.md_state.time - previous.md_state.time
        if not isclose(actual_dt, dt, rel_tol=1e-12, abs_tol=1e-15):
            raise ValueError("mechanical_time_step differs from the completed MD interval.")

        potential_pa = self.stress_trace.after_mechanics.potential_pressure * conversion
        expected_pressure = fsum((potential_pa, kinetic))
        if not isfinite(expected_pressure):
            raise ValueError("computed barostat pressure must be finite.")
        if not isclose(self.current_pressure_pa, expected_pressure,
                       rel_tol=1e-12, abs_tol=1e-9):
            raise ValueError("current_pressure_pa differs from the stress and kinetic sum.")
        expected_scale = isotropic_barostat_scale(
            expected_pressure, target, beta, dt, tau,
        )
        if not isclose(scale, expected_scale, rel_tol=1e-12, abs_tol=1e-15):
            raise ValueError("linear_scale differs from the declared barostat rule.")

        expected_configuration = scale_periodic_configuration(
            mechanical.md_state.configuration, scale,
        )
        if self.current.md_state.configuration != expected_configuration:
            raise ValueError("barostat configuration differs from isotropic affine scaling.")
        if (self.current.md_state.velocities != mechanical.md_state.velocities
                or self.current.md_state.masses != mechanical.md_state.masses
                or self.current.md_state.step != mechanical.md_state.step
                or self.current.md_state.time != mechanical.md_state.time):
            raise ValueError("barostat changed mechanical velocities, masses or clock.")
        if (self.current.resonance_state != mechanical.resonance_state
                or self.current.resonance_time != mechanical.resonance_time
                or self.current.resonance_step_count != mechanical.resonance_step_count
                or self.current.ternary_execution != mechanical.ternary_execution
                or self.current.ternary_event_count != mechanical.ternary_event_count):
            raise ValueError("barostat changed resonance or ternary execution clocks.")
        evaluation = self.after_barostat.evaluation
        if evaluation.configuration.configuration != self.current.md_state.configuration:
            raise ValueError("post-barostat energy and mechanical geometry differ.")
        if evaluation.execution != self.current.ternary_execution:
            raise ValueError("post-barostat retained ternary execution differs.")
        if evaluation.resonance.resonance_state != self.current.resonance_state:
            raise ValueError("post-barostat continuous resonance differs.")
        if evaluation.resonance.thermodynamic_state != self.stress_trace.coupled.thermodynamic_state:
            raise ValueError("post-barostat thermodynamic context differs.")
        if not isclose(
            self.after_barostat.stress.reference_volume,
            self.stress_trace.after_mechanics.stress.reference_volume * scale ** 3,
            rel_tol=1e-10, abs_tol=1e-12,
        ):
            raise ValueError("post-barostat cell volume differs from affine scaling.")

    @property
    def potential_pressure_pa(self) -> float:
        """Strain-derived configurational pressure before affine scaling, in Pa."""
        return (
            self.stress_trace.after_mechanics.potential_pressure
            * self.potential_stress_unit_to_pascal
        )

    @property
    def after_barostat_potential_pressure_pa(self) -> float:
        """Potential pressure re-evaluated on the scaled cell, in Pa."""
        return self.after_barostat.potential_pressure * self.potential_stress_unit_to_pascal

    @property
    def volume_ratio(self) -> float:
        """New periodic volume divided by the last mechanical-state volume."""
        return (
            self.after_barostat.stress.reference_volume
            / self.stress_trace.after_mechanics.stress.reference_volume
        )


def apply_flibe_rank_two_tr_eip_barostat(
    stress_trace: FLiBeRankTwoTREIPMDStressTrace,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    *,
    cutoff: float,
    target_pressure: PhysicalParameter,
    kinetic_pressure: PhysicalParameter,
    potential_stress_unit_to_pascal: float,
    compressibility_per_pascal: float,
    coupling_time: float,
) -> FLiBeRankTwoTREIPBarostatStep:
    """Apply one isotropic barostat update after completed rank-two FLiBe MD.

    Explicit kinetic and strain-derived potential pressures are combined in
    Pa. The conversion factor is supplied by the caller for the energy and
    cell-length units used by its conservative potential. The pressure and
    compressibility must use reciprocal Pa units; coupling_time uses the MD
    mechanical-clock time unit. The thermodynamic coordinate is unchanged.
    """
    if not isinstance(stress_trace, FLiBeRankTwoTREIPMDStressTrace):
        raise TypeError("stress_trace must be FLiBeRankTwoTREIPMDStressTrace.")
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(stress_evaluator, RankTwoConservativeStressEvaluator):
        raise TypeError("stress_evaluator must be RankTwoConservativeStressEvaluator.")
    cutoff = _positive(cutoff, "cutoff")
    conversion = _positive(potential_stress_unit_to_pascal,
                           "potential_stress_unit_to_pascal")
    beta = _positive(compressibility_per_pascal, "compressibility_per_pascal")
    tau = _positive(coupling_time, "coupling_time")
    target = _pressure_parameter(target_pressure, "target_pressure")
    kinetic = _pressure_parameter(kinetic_pressure, "kinetic_pressure")
    if kinetic < 0.0:
        raise ValueError("kinetic_pressure must be nonnegative.")

    # Bind the supplied trace to the exact full-energy model and strain method.
    if evaluate_flibe_rank_two_tr_eip_md_stresses(
        stress_trace.coupled, model, stress_evaluator,
    ) != stress_trace:
        raise ValueError("stress_trace differs from the supplied model or evaluator.")
    final = stress_trace.coupled.current
    coupled = stress_trace.coupled.coupled_step
    if coupled.mechanical_update is None:
        raise ValueError("barostat step requires a completed mechanical interval.")
    dt = final.md_state.time - coupled.previous.md_state.time
    dt = _positive(dt, "mechanical_time_step")

    previous_configuration = final.md_state.configuration
    previous_graph = build_cutoff_graph(previous_configuration, cutoff)
    if previous_graph != stress_trace.after_mechanics.evaluation.graph:
        raise ValueError("cutoff does not reproduce the completed MD interaction graph.")

    potential_pa = stress_trace.after_mechanics.potential_pressure * conversion
    current_pa = fsum((potential_pa, kinetic))
    if not isfinite(current_pa):
        raise ValueError("computed current pressure must be finite.")
    scale = isotropic_barostat_scale(current_pa, target, beta, dt, tau)
    scaled = apply_isotropic_barostat(
        final.md_state,
        current_pressure=current_pa,
        target_pressure=target,
        compressibility=beta,
        time_step=dt,
        coupling_time=tau,
    )
    current = replace(final, md_state=scaled)

    configuration = FLiBeConfiguration(scaled.configuration)
    graph = build_cutoff_graph(configuration.configuration, cutoff)
    resonance = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=stress_trace.coupled.thermodynamic_state,
        resonance_state=current.resonance_state,
        provenance=model.tr_eip_model.provenance,
        source=model.tr_eip_model.source,
    )
    after = evaluate_flibe_rank_two_tr_eip_stress(
        model, stress_evaluator, configuration, graph,
        stress_trace.coupled.after_mechanics.input_features,
        resonance, current.ternary_execution,
    )
    return FLiBeRankTwoTREIPBarostatStep(
        stress_trace=stress_trace,
        target_pressure=target_pressure,
        kinetic_pressure=kinetic_pressure,
        potential_stress_unit_to_pascal=conversion,
        compressibility_per_pascal=beta,
        coupling_time=tau,
        mechanical_time_step=dt,
        current_pressure_pa=current_pa,
        linear_scale=scale,
        current=current,
        after_barostat=after,
    )
