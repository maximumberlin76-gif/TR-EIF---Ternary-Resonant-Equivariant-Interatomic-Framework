
"""Cell-strain stress from the complete rank-two TR-EIF interatomic energy.

A symmetric Cartesian strain acts on atomic positions and the simulation cell.
Each strain point is evaluated using the same interaction graph, continuous
resonance feature inputs, rank-two features, and retained ternary execution.
The reference scalar/vector and rank-two contributions are differentiated
separately and combined into one symmetric stress tensor.

Stress follows sigma_ab = (1/V0) dE/d(epsilon_ab) at the reference cell.
Off-diagonal strain varies epsilon_ab and epsilon_ba by half the scalar
increment. Potential hydrostatic pressure is -trace(sigma)/3. Energy and
volume use the Cartesian units of the supplied model and configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant.rank_two import ScalarVectorTensorFeatures
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .rank_two_model import (
    RankTwoConservativeEnergyModel,
    RankTwoConservativeEnergyResult,
)
from .strain import CellStrainDifferentiation
from .stress import StressState
from .stress_evaluator import _determinant_3x3, _strain_configuration


_STRAIN_PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite.")
    return number


@dataclass(frozen=True, slots=True)
class RankTwoStrainEnergySample:
    """Scalar/vector and rank-two energies at both signed strain points."""

    components: tuple[int, int]
    reference_plus: float
    reference_minus: float
    tensor_plus: float
    tensor_minus: float

    def __post_init__(self) -> None:
        if self.components not in _STRAIN_PAIRS:
            raise ValueError("components must be a canonical symmetric strain pair.")
        for name in (
            "reference_plus", "reference_minus", "tensor_plus", "tensor_minus",
        ):
            object.__setattr__(self, name, _finite(getattr(self, name), name))

    @property
    def total_plus(self) -> float:
        return fsum((self.reference_plus, self.tensor_plus))

    @property
    def total_minus(self) -> float:
        return fsum((self.reference_minus, self.tensor_minus))


@dataclass(frozen=True, slots=True)
class RankTwoConservativeStressResult:
    """Separated invariant-energy strain derivatives and full stress tensor."""

    reference_evaluation: RankTwoConservativeEnergyResult
    differentiation: CellStrainDifferentiation
    reference_volume: float
    samples: tuple[RankTwoStrainEnergySample, ...]
    reference_stress: StressState
    tensor_stress: StressState
    total_stress: StressState

    def __post_init__(self) -> None:
        if not isinstance(self.reference_evaluation, RankTwoConservativeEnergyResult):
            raise TypeError("reference_evaluation must be RankTwoConservativeEnergyResult.")
        if not isinstance(self.differentiation, CellStrainDifferentiation):
            raise TypeError("differentiation must be CellStrainDifferentiation.")
        volume = _finite(self.reference_volume, "reference_volume")
        if volume <= 0.0:
            raise ValueError("reference_volume must be positive.")
        object.__setattr__(self, "reference_volume", volume)
        if not isinstance(self.samples, tuple):
            raise TypeError("samples must be a tuple.")
        if len(self.samples) != len(_STRAIN_PAIRS) or any(
            not isinstance(sample, RankTwoStrainEnergySample)
            for sample in self.samples
        ):
            raise ValueError("samples must contain six typed strain-energy records.")
        if tuple(sample.components for sample in self.samples) != _STRAIN_PAIRS:
            raise ValueError("samples must use canonical symmetric strain ordering.")
        for name in ("reference_stress", "tensor_stress", "total_stress"):
            value = getattr(self, name)
            if not isinstance(value, StressState):
                raise TypeError(f"{name} must be StressState.")
            if not value.is_symmetric:
                raise ValueError(f"{name} must be symmetric.")

        scale = self.differentiation.inverse_central_span / volume
        for sample in self.samples:
            i, j = sample.components
            expected_reference = (sample.reference_plus - sample.reference_minus) * scale
            expected_tensor = (sample.tensor_plus - sample.tensor_minus) * scale
            expected_total = fsum((expected_reference, expected_tensor))
            for state, expected in (
                (self.reference_stress, expected_reference),
                (self.tensor_stress, expected_tensor),
                (self.total_stress, expected_total),
            ):
                if not isclose(state.tensor[i][j], expected, rel_tol=1e-10, abs_tol=1e-12):
                    raise ValueError("stress components must match the recorded strain energies.")

    @property
    def potential_pressure(self) -> float:
        """Potential hydrostatic pressure in model energy-per-cell-volume units."""
        return -self.total_stress.trace / 3.0


def _stress_from_samples(
    samples: tuple[RankTwoStrainEnergySample, ...],
    scale: float,
    plus_name: str,
    minus_name: str,
) -> StressState:
    rows = [[0.0] * 3 for _ in range(3)]
    for sample in samples:
        i, j = sample.components
        derivative = (
            getattr(sample, plus_name) - getattr(sample, minus_name)
        ) * scale
        rows[i][j] = derivative
        rows[j][i] = derivative
    return StressState(tensor=tuple(tuple(row) for row in rows))


@dataclass(frozen=True, slots=True)
class RankTwoConservativeStressEvaluator:
    """Differentiate both energy channels under homogeneous Cartesian strain."""

    differentiation: CellStrainDifferentiation

    def __post_init__(self) -> None:
        if not isinstance(self.differentiation, CellStrainDifferentiation):
            raise TypeError("differentiation must be CellStrainDifferentiation.")

    def evaluate(
        self,
        model: RankTwoConservativeEnergyModel,
        configuration: AtomicConfiguration,
        graph: InteractionGraph,
        features: ScalarVectorTensorFeatures,
        execution: TernaryExecutionVector,
    ) -> RankTwoConservativeStressResult:
        """Calculate reference, rank-two and full stress at one retained state."""
        if not isinstance(model, RankTwoConservativeEnergyModel):
            raise TypeError("model must be RankTwoConservativeEnergyModel.")
        if not isinstance(configuration, AtomicConfiguration):
            raise TypeError("configuration must be AtomicConfiguration.")
        if not isinstance(graph, InteractionGraph):
            raise TypeError("graph must be InteractionGraph.")
        if not isinstance(features, ScalarVectorTensorFeatures):
            raise TypeError("features must be ScalarVectorTensorFeatures.")
        if not isinstance(execution, TernaryExecutionVector):
            raise TypeError("execution must be TernaryExecutionVector.")
        if configuration.cell is None:
            raise ValueError("stress evaluation requires a simulation cell.")
        if (graph.node_count != configuration.atom_count
                or features.node_count != configuration.atom_count
                or execution.node_count != configuration.atom_count):
            raise ValueError("configuration, graph, feature, and execution atom counts differ.")

        volume = _finite(abs(_determinant_3x3(configuration.cell)), "reference_volume")
        if volume <= 0.0:
            raise ValueError("stress evaluation requires a positive cell volume.")
        reference_evaluation = model.evaluate(configuration, graph, features, execution)
        step = self.differentiation.step
        samples = []
        for i, j in _STRAIN_PAIRS:
            plus = model.evaluate(
                _strain_configuration(configuration, i, j, step), graph, features, execution,
            )
            minus = model.evaluate(
                _strain_configuration(configuration, i, j, -step), graph, features, execution,
            )
            samples.append(RankTwoStrainEnergySample(
                components=(i, j),
                reference_plus=plus.reference_energy.total_energy,
                reference_minus=minus.reference_energy.total_energy,
                tensor_plus=plus.tensor_energy.total_energy,
                tensor_minus=minus.tensor_energy.total_energy,
            ))
        records = tuple(samples)
        scale = self.differentiation.inverse_central_span / volume
        reference_stress = _stress_from_samples(
            records, scale, "reference_plus", "reference_minus",
        )
        tensor_stress = _stress_from_samples(
            records, scale, "tensor_plus", "tensor_minus",
        )
        total_stress = StressState(tensor=tuple(
            tuple(fsum((reference_stress.tensor[i][j], tensor_stress.tensor[i][j]))
                  for j in range(3))
            for i in range(3)
        ))
        return RankTwoConservativeStressResult(
            reference_evaluation=reference_evaluation,
            differentiation=self.differentiation,
            reference_volume=volume,
            samples=records,
            reference_stress=reference_stress,
            tensor_stress=tensor_stress,
            total_stress=total_stress,
        )
