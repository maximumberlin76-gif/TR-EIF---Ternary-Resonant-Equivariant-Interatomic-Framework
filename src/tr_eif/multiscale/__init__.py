"""Multiscale interfaces for TR-EIF."""

from .composition import compose_partitions
from .electronic_reference import (
    ElectronicReferenceEvaluator,
    ElectronicReferenceRecord,
    evaluate_electronic_reference,
)
from .geometry import (
    CoarsePositions,
    FineMasses,
    FinePositions,
    mass_weighted_centroids,
)
from .hierarchy import MultiscaleHierarchy
from .hierarchy_state import (
    MultiscaleStateHierarchy,
    build_multiscale_state_hierarchy,
)
from .partition import MultiscalePartition
from .prolongation import (
    CoarseScalars,
    CoarseVectors,
    FineScalars,
    FineVectors,
    prolong_scalar_broadcast,
    prolong_vector_broadcast,
)
from .reduction import (
    CoarseMasses,
    reduce_masses,
    reduce_scalar_sum,
)
from .state import (
    CoarseScaleState,
    build_coarse_scale_state,
)
from .vector_average import mass_weighted_vector_average
from .vector_reduction import reduce_vector_sum

__all__ = [
    "CoarseMasses",
    "CoarsePositions",
    "CoarseScaleState",
    "CoarseScalars",
    "CoarseVectors",
    "ElectronicReferenceEvaluator",
    "ElectronicReferenceRecord",
    "FineMasses",
    "FinePositions",
    "FineScalars",
    "FineVectors",
    "MultiscaleHierarchy",
    "MultiscalePartition",
    "MultiscaleStateHierarchy",
    "build_coarse_scale_state",
    "build_multiscale_state_hierarchy",
    "compose_partitions",
    "evaluate_electronic_reference",
    "mass_weighted_centroids",
    "mass_weighted_vector_average",
    "prolong_scalar_broadcast",
    "prolong_vector_broadcast",
    "reduce_masses",
    "reduce_scalar_sum",
    "reduce_vector_sum",
]
