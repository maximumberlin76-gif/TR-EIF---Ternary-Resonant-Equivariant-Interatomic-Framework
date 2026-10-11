# Trace Specification

## 1. Scope

This document defines the repository-level observable trace specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- trace record semantics;
- trace sequence semantics;
- deterministic ordering;
- step and time coordinates;
- node cardinality;
- retained balanced-ternary execution state;
- active neutral state 0;
- pending target serialization;
- energy observables;
- force observables;
- stress observables;
- optional observable semantics;
- serialization;
- deterministic replay boundary;
- validation requirements;
- schema correspondence;
- provenance boundary;
- continuous/discrete separation;
- resonance boundary;
- multiscale boundary;
- executable reference correspondence.

The balanced-ternary state contract is defined in:

`docs/specifications/ternary_state_specification.md`

Transition semantics are defined in:

`docs/specifications/transition_semantics.md`

Active-neutral routing is defined in:

`docs/specifications/neutral_routing_specification.md`

Energy output is defined in:

`docs/specifications/energy_output_specification.md`

The structural trace schema is:

`schemas/transition_trace.schema.json`

---

## 2. Trace Purpose

A trace is an ordered observable record of executed model state.

It exists to support:

- deterministic replay;
- invariant checking;
- numerical validation;
- architecture validation;
- regression testing;
- benchmark comparison;
- reproducibility;
- provenance-preserving analysis.

A trace is evidence of recorded execution state.

It is not itself the dynamical system.

---

## 3. Trace Is Not Model State

A trace records selected model state and observables.

The trace representation does not replace:

- atomic configuration;
- resonance state;
- ternary execution machinery;
- energy model;
- molecular-dynamics state;
- multiscale state.

Therefore:

`trace ≠ complete model state`

unless a separately declared replay contract establishes complete reconstruction.

---

## 4. Trace Record

The executable reference record is:

`TraceRecord`

A record represents one ordered observation point.

The current trace record contains:

- `step`;
- `time`;
- `execution`;
- optional `energy`;
- optional `forces`;
- optional `stress`.

---

## 5. Step Coordinate

`step`

is a nonnegative integer execution index.

It identifies the discrete record order within the represented execution sequence.

A step index is not:

- ternary state;
- resonance classification;
- physical phase;
- model scale.

---

## 6. Time Coordinate

`time`

is a finite nonnegative real value.

It represents the declared trace time coordinate.

The trace specification does not impose one universal physical time unit.

The concrete execution contract must define the applicable unit.

---

## 7. Step and Time Are Distinct

The step coordinate is discrete.

The time coordinate is continuous numerical state.

Therefore:

`step ≠ time`

A model may use unequal time increments between successive trace records when its execution contract permits that behavior.

---

## 8. Sequence Step Ordering

Within one valid `TraceSequence`, step values are strictly increasing.

For consecutive records:

`step_(n+1) > step_n`

Duplicate step values are invalid.

Decreasing step values are invalid.

---

## 9. Sequence Time Ordering

Within one valid `TraceSequence`, time values are nondecreasing.

For consecutive records:

`time_(n+1) ≥ time_n`

The trace contract does not require strictly positive time increments.

---

## 10. Time Equality Does Not Mean State Equality

Two distinct committed or observed execution records may have the same declared time when the higher-level execution contract permits multiple ordered events at one time coordinate.

Therefore:

`equal time ≠ identical execution record`

Step ordering remains authoritative for record order.

---

## 11. Node Count

Each trace record exposes:

`node_count`

through its ternary execution vector.

A trace sequence requires one common node count across all records.

Node count must be positive.

---

## 12. Node Identity by Ordering

The current trace representation preserves node correspondence by stable positional ordering.

For a sequence with:

`N`

nodes, node index:

`i`

must retain the same declared entity correspondence across the sequence unless a higher-level contract explicitly defines remapping.

---

## 13. Node Index Is Not Ternary State

A node index is structural metadata.

Therefore:

`node index ≠ ternary state`

and:

`node index ≠ resonance class`

---

## 14. Ternary Execution State

Every trace record contains a complete:

`TernaryExecutionVector`

for the represented nodes.

Each node contains:

- retained executed state;
- optional pending target.

---

## 15. Canonical Ternary State

The retained execution state belongs to:

`{-1, 0, 1}`

Canonical notation is:

`-1/0/1`

The trace must preserve these values exactly.

---

## 16. Active Neutral in Trace

Retained state:

`0`

is active neutral.

It may represent:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

The trace must not reinterpret active neutral as missing data.

---

## 17. Active Neutral Is an Executed State

When a trace record contains:

`retained_state = 0`

the model executed or retained active neutral state at that record.

It is not a placeholder for an unknown value.

Therefore:

`trace 0 = active executed state`

not:

`trace 0 = missing`

---

## 18. Pending Target

A trace may record:

`pending_target`

for a node in active neutral.

The pending target is separate from retained executed state.

Therefore:

`pending target ≠ executed state`

---

## 19. Pending Target Domain

A non-null pending target is restricted to:

`{-1, 1}`

The value:

`0`

is not a valid pending target.

Therefore:

`pending ≠ active neutral`

---

## 20. Pending Target Requires Active Neutral

A non-null pending target is valid only when:

`retained_state = 0`

A serialized state such as:

`retained_state = -1`

with:

`pending_target = 1`

is invalid.

Likewise:

`retained_state = 1`

with:

`pending_target = -1`

is invalid.

---

## 21. Opposite-Polarity Trace History

A valid opposite-polarity execution must appear as separate committed state history.

The route:

`-1 → 1`

must be represented through:

`-1`

then:

`0`

then:

`1`

across distinct committed execution events.

Likewise:

`1 → 0 → -1`

must remain explicit.

---

## 22. Trace Must Not Collapse Active Neutral

A trace exporter or replay implementation must not collapse:

`-1 → 0 → 1`

into:

`-1 → 1`

Likewise it must not collapse:

`1 → 0 → -1`

into:

`1 → -1`

Doing so would destroy the executable transition semantics.

---

## 23. Hold and Committed Retention

A held execution attempt and a committed self-transition are semantically distinct.

The retained state may be numerically identical before and after either operation.

Therefore:

`same retained state ≠ same execution event`

The current serialized execution-state snapshot alone does not necessarily encode every event-level distinction.

When event identity is required, the corresponding execution result or higher-level trace extension must preserve it explicitly.

---

## 24. Target Is Not Retained State

A requested target is not part of the canonical retained execution snapshot unless explicitly added by a higher-level trace.

Therefore a trace record must not infer:

`requested target = retained state`

from retained-state serialization alone.

---

## 25. Missing Data Is Not Ternary Zero

Missing, unavailable, invalid, failed, unknown, or abstained information must remain outside the balanced ternary state space.

Therefore:

`missing ≠ 0`

`invalid ≠ 0`

`unknown ≠ 0`

`error ≠ 0`

---

## 26. Observable Separation

The current trace may additionally contain:

- energy;
- forces;
- stress.

These are physical or model observables.

They remain semantically separate from ternary execution state.

---

## 27. Energy in Trace

When present, energy is represented by:

`EnergyState`

with:

- `atomic_energies`;
- `total_energy`.

Energy remains continuous scalar state.

---

## 28. Energy Is Not Ternary State

A trace containing:

`retained_state = 0`

does not imply:

`total_energy = 0`

Likewise:

`total_energy = 0`

does not imply:

`retained_state = 0`

Therefore:

`energy ≠ ternary state`

---

## 29. Missing Energy

Energy may be absent from a trace record.

Serialized absence is represented by:

`null`

It must not be represented by:

`0`

Therefore:

`missing energy = null`

not:

`missing energy = active neutral 0`

---

## 30. Atomic Energy Cardinality

When energy is present:

`len(atomic_energies) = node_count`

The trace record enforces this executable cardinality invariant.

---

## 31. Force in Trace

When present, force output is represented by:

`ForceState`

It contains one Cartesian vector per represented node.

---

## 32. Force Cardinality

When forces are present:

`len(forces) = node_count`

Each force vector has exactly three finite real Cartesian components.

---

## 33. Force Is Not Ternary State

A force component numerically equal to:

`-1`

`0`

or:

`1`

remains a force component.

Therefore:

`force ≠ ternary state`

and:

`zero force ≠ active neutral 0`

---

## 34. Missing Force

An unavailable force observable is represented by absence:

`null`

It is not represented by a zero force vector unless the actual force is explicitly calculated as zero.

---

## 35. Stress in Trace

When present, stress is represented by:

`StressState`

with one finite Cartesian:

`3 × 3`

tensor.

---

## 36. Stress Is Not Ternary State

Stress components remain continuous physical quantities.

Therefore:

`stress ≠ ternary state`

and:

`zero stress ≠ active neutral 0`

---

## 37. Missing Stress

Unavailable stress output is represented as:

`null`

It is not represented by a zero tensor unless the actual model output is explicitly zero.

---

## 38. Observable Optionality

The current trace record permits:

- energy only;
- forces only;
- stress only;
- any explicit combination;
- none of the three optional observables.

The ternary execution vector remains mandatory.

---

## 39. No Observable Inference

A missing observable must not be reconstructed from unrelated trace fields without an explicit model.

For example:

- missing force must not be inferred from energy alone without the force model;
- missing stress must not be inferred from ternary state;
- missing energy must not be inferred from resonance classification.

---

## 40. Trace Sequence

The executable sequence type is:

`TraceSequence`

It contains an ordered nonempty tuple of:

`TraceRecord`

instances.

---

## 41. Nonempty Sequence

A `TraceSequence` must contain at least one record.

An empty trace sequence is invalid under the current executable reference contract.

---

## 42. Common Node Cardinality

All records within one trace sequence must have the same node count.

A change in represented node cardinality requires:

- another trace sequence;
- or an explicitly extended topology-changing trace contract.

---

## 43. Sequence Record Count

Serialized sequence metadata includes:

`record_count`

The executable semantic relation is:

`record_count = len(records)`

The JSON structural schema alone does not establish this cross-field equality.

Executable validation does.

---

## 44. Sequence Node Count

Serialized sequence metadata includes:

`node_count`

The executable relation is:

`node_count = record.node_count`

for every record in the sequence.

---

## 45. Canonical Sequence Format

The current serialized root format identifier is:

`tr_eif.trace`

The current serialized version is:

`1`

These identify the trace wire format.

They are not model-family versions.

---

## 46. Trace Version Is Not Model Version

Trace schema or wire version and model version are different concepts.

Therefore:

`trace version ≠ TR-EIP model version`

and:

`trace version ≠ repository release version`

---

## 47. Deterministic Serialization

For an identical valid trace sequence, deterministic serialization must produce identical logical field values and canonical ordering under the declared serializer.

The current JSON exporter uses deterministic key ordering where declared.

---

## 48. Trace Mapping

The executable serializer maps one `TraceRecord` into a plain mapping.

The record mapping contains:

- `step`;
- `time`;
- `node_count`;
- `ternary_execution`;
- `energy`;
- `forces`;
- `stress`.

---

## 49. Ternary Execution Serialization

Each node execution state serializes:

- `retained_state`;
- `pending_target`.

The retained state is serialized numerically as one of:

`-1`

`0`

`1`

---

## 50. Pending Serialization

A missing pending target is serialized as:

`null`

A present pending target is serialized as:

`-1`

or:

`1`

Active neutral:

`0`

is not used as a pending absence marker.

---

## 51. Energy Serialization

When present, energy serializes:

- ordered `atomic_energies`;
- scalar `total_energy`.

When absent:

`energy = null`

---

## 52. Force Serialization

When present, forces serialize as an ordered array of Cartesian vectors.

When absent:

`forces = null`

---

## 53. Stress Serialization

When present, stress serializes as one:

`3 × 3`

Cartesian tensor.

When absent:

`stress = null`

---

## 54. Finite Numeric Requirement

Executable trace records reject nonfinite:

- time;
- energy values;
- force components;
- stress components.

NaN and infinity are invalid trace values.

---

## 55. NaN Is Not Active Neutral

NaN must never be mapped to ternary state:

`0`

Therefore:

`NaN ≠ active neutral`

The same rule applies to infinity and failed numerical evaluation.

---

## 56. Continuous and Discrete Separation

A trace combines continuous observables and discrete execution state without identifying them.

The trace may simultaneously contain:

- continuous time;
- continuous energy;
- continuous force;
- continuous stress;
- discrete `-1/0/1` execution state.

Their coexistence in one record does not collapse their semantic domains.

---

## 57. Resonance Boundary

The current base `TraceRecord` does not directly serialize:

- oscillator phases;
- oscillator frequencies;
- resonance descriptor;
- resonance region.

Therefore those values must not be inferred from trace fields that do exist.

---

## 58. Trace Does Not Imply Resonance State

A ternary state history does not uniquely reconstruct continuous resonance state.

Therefore:

`ternary trace ≠ resonance trajectory`

A resonance trace requires explicitly recorded resonance data or deterministic replay from sufficient declared inputs.

---

## 59. Resonance Classification Is Not Ternary Trace State

The resonance regions:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

must not be inferred as:

`-1`

`0`

`1`

from a trace unless an explicit mapping is part of the model contract.

---

## 60. Phase Order Is Not Trace Ternary State

A phase-order value is a continuous resonance observable.

It is not encoded by retained ternary state.

Therefore:

`R(t) ≠ ternary state`

---

## 61. Coherence Boundary

Coherence remains distinct from trace uniformity.

A sequence in which every node has the same retained ternary state does not by itself establish continuous coherence.

Therefore:

`uniform ternary vector ≠ complete coherence`

---

## 62. Trace and Molecular Dynamics

A molecular-dynamics trajectory and an observable trace are related but distinct representations.

A trajectory records molecular-dynamics state evolution.

A trace records selected observable or execution state.

Neither representation automatically contains all information from the other.

---

## 63. Trace and Configuration

The current base trace record does not contain complete atomic positions.

Therefore a trace is not a full atomic trajectory.

Atomic configuration replay requires the corresponding configuration or deterministic trajectory reconstruction contract.

---

## 64. Trace and Velocities

The current base trace record does not serialize atomic velocities.

Therefore kinetic state cannot be reconstructed from the base trace alone.

---

## 65. Trace and Graph

The current base trace record does not serialize the interaction graph.

Therefore graph topology must not be inferred from trace node count alone.

---

## 66. Trace and Model Manifest

A trace sequence is not a model manifest.

A reproducible execution may require:

- model manifest;
- trace;
- configuration;
- external parameters;
- additional execution inputs.

The exact replay bundle is defined by the reproducibility contract.

---

## 67. Deterministic Replay

The executable observables layer includes deterministic replay support.

Replay validation compares actual regenerated trace output against expected trace output under the declared replay inputs.

---

## 68. Replay Is Not Simulation Guessing

Deterministic replay must use explicit declared inputs.

It must not reconstruct missing state through heuristic similarity.

Therefore:

`replay ≠ approximate regeneration`

---

## 69. Exact Replay Boundary

When a replay contract declares exact deterministic equivalence, the comparison is between defined serialized or structured outputs.

Numerical tolerances may be used only where the applicable numerical contract explicitly requires them.

They must not be introduced merely to force a passing result.

---

## 70. Replay Input Completeness

A deterministic replay bundle must include all result-affecting inputs required by the selected execution path.

Hidden result-affecting state invalidates strict replay claims.

---

## 71. Trace Determinism

For identical complete deterministic execution inputs, the resulting trace sequence must be reproducible within the declared numerical environment.

No hidden random state may alter trace output.

---

## 72. Canonical Node Ordering

Trace serialization preserves node ordering.

A permutation of node order is not byte-identical trace output.

Permutation-equivalent physical states and identical serialized traces are separate validation concepts.

---

## 73. Physical Equivalence vs Serialized Identity

Two physical states may be equivalent under a symmetry transformation while producing different coordinate-dependent external representations.

Likewise, two trace files may be semantically equivalent under an explicitly permitted mapping without being byte-identical.

The chosen validation relation must be declared.

---

## 74. Byte Determinism

Where byte determinism is claimed, independent executions must emit identical serialized bytes.

This is a stronger condition than semantic equivalence.

TR-EIF benchmark qualifications explicitly test byte determinism where that property is part of the benchmark contract.

---

## 75. Trace Provenance

A trace may require provenance metadata at the surrounding artifact or replay-bundle level.

The current base `TraceRecord` does not embed a general provenance field.

Therefore provenance must not be fabricated from observable values.

---

## 76. Benchmark Trace

A trace generated from:

`BENCHMARK`

inputs remains benchmark evidence.

It does not become:

`PRIMARY_SOURCE`

because it passed deterministic replay.

---

## 77. Experimental Evidence Boundary

An experimental observable record is not automatically a TR-EIF execution trace.

Experimental evidence and executable trace evidence are different evidence classes.

A comparison between them requires an explicit comparison contract.

---

## 78. First-Principles Evidence Boundary

A first-principles trajectory or observable sequence is not automatically a TR-EIF trace.

Conversion into a TR-EIF comparison or replay structure requires an explicit mapping.

---

## 79. Validation Status Is Not Ternary State

Trace validation outcomes such as:

- PASS;
- FAIL;
- unresolved;
- not evaluated

are not balanced-ternary states.

Therefore:

`PASS ≠ 1`

`FAIL ≠ -1`

`unresolved ≠ 0`

---

## 80. Validation Failure Does Not Rewrite Trace

A failed validation result must not mutate a recorded ternary state to represent failure.

The trace remains execution evidence.

Validation remains a separate evidence layer.

---

## 81. Schema Validation

The root trace schema is:

`schemas/transition_trace.schema.json`

The schema validates structural wire representation.

It does not replace executable cross-record invariants.

---

## 82. Structural Schema Boundary

JSON Schema can validate structural properties such as:

- required fields;
- value types;
- allowed ternary values;
- nullable observables;
- tensor dimensions;
- local pending-target semantics.

Cross-record invariants remain executable validation responsibilities where JSON Schema does not express them directly.

---

## 83. Executable Cross-Record Invariants

Executable trace-sequence validation includes:

- nonempty records;
- common node count;
- strictly increasing steps;
- nondecreasing times.

These are part of trace semantics even where not encoded completely by structural JSON Schema.

---

## 84. Energy Algebra Boundary

The structural trace schema can require:

- atomic energy array;
- total energy scalar.

It does not by itself prove:

`total_energy = sum(atomic_energies)`

That relation remains an executable energy invariant.

---

## 85. Node Cardinality Boundary

The structural schema can require nonempty arrays.

Executable validation additionally establishes:

`len(ternary_execution) = node_count`

and when present:

`len(atomic_energies) = node_count`

`len(forces) = node_count`

---

## 86. Trace Export

The observables package includes structured export support.

Current export layers include mapping and JSON or file serialization.

Export must preserve the logical trace content.

---

## 87. Export Must Not Change Ternary Semantics

Serialization must not:

- convert active neutral `0` to null;
- convert null to active neutral `0`;
- remove pending target state;
- collapse opposite-polarity routes;
- reinterpret retained state as requested target.

---

## 88. Export Must Not Change Physical Semantics

Serialization must not:

- replace missing energy with zero;
- replace missing forces with zero vectors;
- replace missing stress with zero tensor;
- change force sign;
- change stress convention;
- reorder node observables silently.

---

## 89. File Export

A file exporter writes serialized trace representation to a declared path.

Successful file creation is not by itself scientific validation.

The file contents must still satisfy:

- structural schema;
- executable trace invariants;
- applicable replay contract.

---

## 90. Replay Comparison

A replay comparison must specify what equality means.

Possible relations include:

- exact object equality;
- exact serialized equality;
- byte equality;
- declared numerical equivalence.

The selected relation must not change between runs to obtain a passing result.

---

## 91. Numerical Tolerance Boundary

A tolerance is legitimate only when required by the declared numerical comparison.

Tolerance must be:

- explicit;
- fixed before evaluation;
- applicable to the compared quantity;
- independent of observed pass or fail outcome.

Tolerance must not be tuned after seeing the result.

---

## 92. Trace and E(3)

A scalar-energy trace should preserve scalar energy invariance under an E(3)-equivalent model evaluation.

Force traces should transform according to the declared polar-vector rule.

However, a raw serialized trace is not automatically E(3)-invariant because coordinate-dependent quantities may differ under transformation.

---

## 93. Trace and Permutation

A physical permutation of atom identity applied consistently may preserve model-level physical outputs while changing serialized ordering.

Therefore:

`permutation invariance ≠ byte-identical trace`

unless canonical relabeling is part of the trace contract.

---

## 94. Trace and Multiscale State

A coarse-scale trace and fine-scale trace are different artifacts.

A scale mapping between them requires an explicit multiscale mapping.

Therefore:

`fine trace ≠ coarse trace`

without a declared transfer operator.

---

## 95. Ternary Coarse-Graining Prohibition

Fine-scale ternary states must not be arithmetically averaged into a coarse trace.

For example:

`mean(-1, 1) = 0`

does not establish active-neutral coarse state.

Therefore:

`arithmetic zero ≠ active neutral`

---

## 96. Trace and Uncertainty

Uncertainty associated with an observable is not currently encoded as balanced-ternary execution state.

If uncertainty metadata is added to a trace extension, it must remain explicitly typed.

Therefore:

`uncertainty ≠ ternary state`

---

## 97. Trace and Thermodynamic State

The base trace does not automatically include complete thermodynamic state.

A temperature or pressure history requires explicit recording or deterministic reconstruction from sufficient model state.

---

## 98. Thermodynamic Temperature Is Not Trace Time

Temperature and trace time are different physical dimensions.

Therefore:

`temperature ≠ time`

Likewise classifier temperature parameters, when used, remain distinct from thermodynamic temperature.

---

## 99. Trace and Physical Phase

A trace transition does not automatically indicate a physical phase transition.

Therefore:

`trace state change ≠ physical phase transition`

A physical phase transition requires its own physical observables and validation criteria.

---

## 100. Trace and Structural Transition

A change in graph, geometry, or another structural observable is not automatically a balanced-ternary transition.

Therefore:

`structural transition ≠ ternary transition`

These may interact only through explicit model mappings.

---

## 101. Trace and Bifurcation

A change in recorded ternary state does not establish a dynamical bifurcation.

Therefore:

`ternary transition ≠ bifurcation`

and:

`bifurcation ≠ ternary transition`

---

## 102. Trace and Resonance-Window Crossing

A resonance-window crossing, if recorded by an extended trace, does not itself constitute a bifurcation or ternary transition.

Therefore:

`resonance-window crossing ≠ bifurcation`

and:

`resonance-window crossing ≠ ternary transition`

without explicit mappings.

---

## 103. Error Handling

A trace-construction failure is an execution or validation error.

It is not encoded by:

`retained_state = 0`

Errors must remain explicit outside the balanced-ternary state domain.

---

## 104. Unknown Values

Unknown values must remain explicitly unknown or unavailable according to the surrounding data contract.

They must not be silently coerced to:

`0`

---

## 105. Abstention

An abstention or intentionally unevaluated output is not active neutral state.

Therefore:

`abstention ≠ 0`

---

## 106. Reference Serialization Contract

The current structural root representation contains:

`format = "tr_eif.trace"`

`version = 1`

`record_count`

`node_count`

and:

`records`

The exact content of each record is defined by the transition trace schema and executable serializer.

---

## 107. Minimal Record Semantics

A minimal valid record may contain:

- step;
- time;
- ternary execution vector;
- no energy;
- no forces;
- no stress.

The absence of physical observables does not remove the ternary execution snapshot.

---

## 108. Rich Record Semantics

A record may contain:

- ternary execution state;
- energy;
- forces;
- stress

simultaneously.

Their simultaneous presence allows cross-layer validation while retaining type separation.

---

## 109. Trace Completeness Is Contract-Relative

A trace is complete only relative to a declared validation or replay purpose.

A trace sufficient for ternary replay may be insufficient for molecular-dynamics reconstruction.

A trace sufficient for energy validation may be insufficient for resonance-state reconstruction.

---

## 110. No Universal Trace Sufficiency

TR-EIF does not claim that one trace format contains all possible state required by every future model realization.

Extensions must remain versioned and explicit.

---

## 111. Versioning Requirement

A change that modifies trace wire semantics requires an explicit trace-format version decision.

Silent reinterpretation of an existing version is prohibited.

---

## 112. Backward Interpretation

A reader of a versioned trace must interpret fields according to the declared trace version.

Later semantics must not be retroactively imposed on an earlier trace without a documented conversion.

---

## 113. Deterministic Replay Architecture

The replay chain is:

`declared execution inputs`

`→ deterministic execution`

`→ generated trace`

`→ comparison against expected trace`

The comparison result belongs to validation state.

It does not become ternary execution state.

---

## 114. Trace Equality Boundary

Exact trace equality requires equality of all fields included in the declared trace comparison.

Partial observable equality must not be described as full trace equality.

---

## 115. Reproducibility Boundary

Trace reproducibility requires:

- declared model identity;
- declared parameters;
- declared input state;
- declared numerical semantics;
- declared execution ordering;
- declared trace format.

A trace file alone may not contain all of these artifacts.

---

## 116. FRP Boundary

FRP may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

TR-EIF trace architecture does not import:

- FRP repository structure;
- FRP RTL architecture;
- FRP scheduler modes;
- FRP-specific coefficients;
- FRP module naming.

Therefore:

`FRP ≠ TR-EIF`

and:

`FRP ≠ TR-EIP`

---

## 117. Confirmed Ternary Semantic Correspondence

The trace preserves confirmed shared ternary semantics:

- canonical `-1/0/1`;
- active neutral `0`;
- no direct committed opposite-polarity transitions;
- target distinct from executed state;
- pending target distinct from active neutral.

These semantic correspondences do not make the two project architectures identical.

---

## 118. Core Trace Invariants

The trace layer preserves the following invariants:

1. A trace sequence is nonempty.
2. Record step values strictly increase.
3. Record time values do not decrease.
4. Node count is positive.
5. Node count remains constant within one sequence.
6. Every record contains a complete ternary execution vector.
7. Retained state belongs to `-1/0/1`.
8. State `0` is active neutral.
9. A pending target is distinct from executed state.
10. A pending target is never `0`.
11. A non-null pending target requires retained state `0`.
12. Missing data are not encoded by active neutral.
13. Missing physical observables serialize as `null`.
14. Energy remains separate from ternary execution.
15. Force remains separate from ternary execution.
16. Stress remains separate from ternary execution.
17. Energy atomic-contribution cardinality equals node count when energy is present.
18. Force cardinality equals node count when forces are present.
19. Stress remains a finite Cartesian `3 × 3` tensor when present.
20. Nonfinite trace values are invalid.
21. A ternary trace does not uniquely reconstruct resonance state.
22. A trace does not uniquely reconstruct atomic configuration unless explicitly extended.
23. A trace does not uniquely reconstruct velocities unless explicitly extended.
24. A trace does not imply graph topology.
25. Deterministic replay requires complete result-affecting inputs.
26. Replay comparison semantics must be declared.
27. Numerical tolerance must not be selected after observing the result.
28. Validation status is not ternary state.
29. Uncertainty is not ternary state.
30. Structural transition is not ternary transition.
31. Physical phase transition is not ternary transition.
32. Bifurcation is not ternary transition.
33. Resonance-window crossing is not bifurcation.
34. Export must not alter execution semantics.
35. Export must not alter physical observable semantics.
36. Trace wire-format version is distinct from model and repository versions.
37. Deterministic trace serialization requires deterministic ordering.
38. Byte identity is stronger than semantic equivalence.
39. Provenance is not inferred from trace values.
40. Fine-scale ternary states are not arithmetically averaged into active-neutral coarse state.

---

## 119. Executable Reference Correspondence

The current executable trace implementation is distributed across:

`src/tr_eif/observables/trace.py`

`src/tr_eif/observables/sequence.py`

`src/tr_eif/observables/serialization.py`

`src/tr_eif/observables/json_export.py`

`src/tr_eif/observables/file_export.py`

`src/tr_eif/observables/replay.py`

`src/tr_eif/observables/replay_runner.py`

The associated execution-state implementation is distributed across:

`src/tr_eif/ternary/state.py`

`src/tr_eif/ternary/execution.py`

`src/tr_eif/ternary/vector_execution.py`

---

## 120. Principal Trace Interfaces

The principal executable trace interfaces include:

`TraceRecord`

`TraceSequence`

trace-record mapping serialization

trace-sequence mapping serialization

JSON export

file export

deterministic replay

replay runner

The exact exported public API remains governed by the package implementation.

---

## 121. Schema Correspondence

The principal root schemas associated with trace output are:

`schemas/ternary_state.schema.json`

`schemas/energy_output.schema.json`

`schemas/observables.schema.json`

`schemas/transition_trace.schema.json`

These schemas define wire structure.

Executable Python types retain the stronger runtime invariants defined by their constructors and validation logic.

---

## 122. Replay Evidence Boundary

A successful deterministic replay establishes agreement under the declared replay contract.

It does not automatically establish:

- physical correctness;
- experimental accuracy;
- first-principles accuracy;
- thermodynamic validity;
- complete model validity.

Those require separate evidence.

---

## 123. Scientific Validation Boundary

Trace validation may demonstrate that execution followed declared architecture.

Scientific validation additionally requires comparison to the relevant mathematical, numerical, experimental, or first-principles reference.

Therefore:

`trace validity ≠ scientific validity`

---

## 124. Mathematical Validation Boundary

A trace can provide evidence that an invariant was respected during execution.

The trace does not itself prove the mathematical theorem that defines the invariant.

Formal proof and execution evidence remain distinct.

---

## 125. Numerical Validation Boundary

A trace may expose:

- energy drift;
- force behavior;
- stress behavior;
- state transitions;
- deterministic replay.

Interpretation of those values requires the declared numerical method and tolerance contract.

---

## 126. Benchmark Boundary

A benchmark trace must retain:

- benchmark identity;
- fixed inputs;
- provenance;
- measurement or validation contract;
- structured output.

Benchmark evidence must not be relabeled as physical source evidence.

---

## 127. Cross-Model Comparison Boundary

Two model traces may be compared only under a declared common comparison domain.

The comparison must specify:

- common inputs;
- observable mapping;
- units;
- ordering;
- normalization;
- tolerance where applicable.

Numerical proximity without a declared correspondence is not model equivalence.

---

## 128. Identity Criterion

TR-EIF trace comparison follows the distinction:

`similar ≠ identical`

A claim of identity requires the declared equality relation to hold.

A claim of equivalence requires the declared equivalence relation to hold.

Visual or numerical resemblance alone is insufficient.

---

## 129. No Hidden State Reconstruction

Replay and trace analysis must not invent hidden state merely because a likely state would make the output consistent.

If a required result-affecting input is absent, the replay contract is incomplete.

Incomplete replay input must remain explicit.

---

## 130. Trace Extension Rule

A future trace extension may add fields such as:

- resonance state;
- resonance descriptor;
- atomic configuration;
- velocities;
- interaction graph;
- uncertainty metadata;
- multiscale state.

Such additions require explicit versioning and schema updates.

They must not silently change version-1 semantics.

---

## 131. Active Neutral Preservation Rule

Every trace extension that includes balanced-ternary state must preserve the semantic identity of active neutral `0`.

No extension may reinterpret `0` as:

- null;
- missing;
- invalid;
- unknown;
- failed;
- abstained.

---

## 132. Opposite-Polarity Preservation Rule

Every trace or replay extension must preserve separate execution events for:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

Direct opposite-polarity committed transitions remain prohibited.

---

## 133. Continuous-Dynamics Preservation Rule

Continuous state must remain continuous unless an explicit mapping produces a discrete target.

A trace implementation must not quantize continuous resonance, energy, force, stress, or thermodynamic state into `-1/0/1` merely for storage convenience.

---

## 134. Layer-Preservation Rule

A trace may bring multiple layers into one serialized artifact.

It must still preserve the distinctions:

`continuous resonance ≠ ternary execution`

`ternary execution ≠ energy`

`energy ≠ force`

`force ≠ stress`

`validation status ≠ ternary state`

`missing data ≠ active neutral`

---

## 135. Determinism Requirement

For a deterministic trace-producing execution, all result-affecting inputs must be explicit or fixed by the declared execution environment.

A hidden random seed, hidden mutable state, environment-dependent ordering, or undeclared parameter invalidates a strict determinism claim.

---

## 136. Structured Output Requirement

Machine-consumable trace output must be structurally parseable without interpreting prose.

The root format and record fields must remain explicit.

Structured output validation belongs to the automated validation layer.

---

## 137. Human-Readable Documentation Boundary

Human-readable documentation explains trace semantics.

It is not the executable trace format.

Changes to prose alone do not modify serialized trace semantics unless the corresponding executable and schema contracts also change.

---

## 138. Release Audit Requirement

Before release, trace artifacts require audit for:

- executable/schema correspondence;
- version consistency;
- deterministic replay;
- structured serialization;
- internal references;
- provenance;
- scientific claims;
- reproducibility.

A green unit test alone is not a complete release audit.

---

## 139. Non-Claims

The trace layer does not by itself establish:

- resonance of a physical material;
- chemical bonding;
- material transmutation;
- thermodynamic equilibrium;
- physical phase transition;
- first-principles accuracy;
- experimental accuracy;
- universal model validity.

It records and validates execution evidence under declared contracts.

---

## 140. Summary

TR-EIF trace architecture records continuous observables and balanced-ternary execution without collapsing their semantic domains.

The canonical trace chain is:

`declared model execution`

`→ ordered TraceRecord objects`

`→ TraceSequence`

`→ deterministic structural serialization`

`→ schema validation`

`→ replay or scientific validation`

The trace preserves:

`-1/0/1`

with active neutral:

`0`

as an executed state.

It preserves:

`pending target ≠ executed state`

It preserves:

`null ≠ active neutral`

It preserves:

`energy ≠ ternary state`

`force ≠ ternary state`

`stress ≠ ternary state`

and:

`resonance state ≠ ternary trace state`

A trace is valid only when its structure, ordering, cardinality, execution semantics, and declared replay conditions remain explicit and reproducible.

Similarity is not identity.

Replay is not guessing.

Validation status is not execution state.

Active neutral remains an active state of the balanced-ternary architecture.
