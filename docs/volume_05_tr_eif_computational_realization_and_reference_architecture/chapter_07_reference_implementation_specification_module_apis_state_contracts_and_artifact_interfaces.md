# Reference Implementation Specification, Module APIs, State Contracts, and Artifact Interfaces

## 1. Purpose

This chapter specifies the implementation-facing contract of the TR-EIF computational reference architecture.

The specification translates the architecture established in Chapters 01–06 into an executable implementation structure without identifying the formal theory with any particular programming language, runtime, repository layout, hardware target, or downstream specialization.

The reference implementation specification defines:

- module responsibilities;
- typed module APIs;
- state ownership;
- immutable and mutable boundaries;
- request and commit interfaces;
- numerical solver interfaces;
- EIF representation interfaces;
- TR state interfaces;
- resonance interfaces;
- ternary target and execution interfaces;
- forward and reverse integration interfaces;
- history and memory interfaces;
- scheduler interfaces;
- trace interfaces;
- checkpoint and replay interfaces;
- validation interfaces;
- artifact boundaries;
- serialization contracts;
- deterministic execution requirements;
- implementation conformance requirements.

The implementation chain is:

`formal state`

`→ typed computational representation`

`→ module API`

`→ deterministic operation`

`→ request`

`→ authorization`

`→ commit`

`→ retained state`

`→ observable trace`

`→ validation artifact`.

## 2. Dependency

This chapter depends on:

- Volume 01 mathematical foundations;
- Volume 02 ternary resonance theory;
- Volume 03 equivariant interatomic framework;
- Volume 04 TR-EIF integration theory;
- Volume 05 Chapter 01 computational realization foundations and execution model;
- Volume 05 Chapter 02 computational state representation, typed data structures, and numerical encoding;
- Volume 05 Chapter 03 deterministic computational operators, scheduling, and state-transition execution;
- Volume 05 Chapter 04 numerical realization, solver semantics, precision, and error control;
- Volume 05 Chapter 05 TR-EIF reference architecture, module boundaries, interfaces, and execution pipeline;
- Volume 05 Chapter 06 reference architecture conformance, qualification, and deterministic validation.

All previously established mathematical, dimensional, symmetry, numerical, ternary, provenance, execution, qualification, and scientific boundaries remain active.

## 3. Specification Status

The interfaces defined in this chapter are `AUTHOR_DEFINED` TR-EIF reference-implementation contracts.

They specify a canonical computational organization for conformance and interoperability.

They are not claims that one programming language, class hierarchy, package manager, serialization format, or hardware architecture is mathematically privileged.

## 4. Reference Implementation

Let:

`I_ref`

denote a computational realization that implements the mandatory contracts of the reference architecture for a declared scope.

An implementation conforms by behavior and contract satisfaction.

Conformance does not require identical internal source-code organization when the externally required semantics are preserved.

## 5. Formal Theory and Implementation

The architecture preserves:

`TR-EIF formal theory ≠ reference implementation`.

The formal theory defines mathematical objects and relations.

The reference implementation defines computational representations and executable contracts for selected realizations of those objects and relations.

## 6. Implementation Unit

An implementation unit is a computational component with:

- one semantic responsibility;
- declared inputs;
- declared outputs;
- declared read authority;
- declared write authority;
- declared failure behavior;
- declared deterministic scope;
- declared validation contract.

An implementation unit may be realized as:

- function;
- object;
- process;
- service;
- hardware block;
- software module;
- hybrid component.

The realization form does not alter its semantic contract.

## 7. Canonical Module Set

The reference architecture defines the following logical module set:

1. configuration module;
2. state module;
3. EIF representation module;
4. symmetry module;
5. topology and geometry module;
6. forward EIF-to-TR mapping module;
7. TR dynamics module;
8. numerical solver module;
9. resonance projection module;
10. resonance classification module;
11. ternary target module;
12. ternary execution module;
13. scheduler module;
14. reverse TR-to-EIF mapping module;
15. EIF update module;
16. history and memory module;
17. observable module;
18. trace module;
19. checkpoint module;
20. replay module;
21. validation module.

A conforming implementation may combine physical source files while preserving these logical boundaries.

## 8. Module Identifier

Every module participating in traceable execution must have a stable semantic identifier:

`module_id`.

The identifier denotes the logical module role.

It must not be inferred solely from a source filename.

## 9. API Contract

For a module `M`, define its API contract as:

`API_M = (D_M, C_M, R_M, W_M, E_M, F_M)`

where:

- `D_M` is the input domain;
- `C_M` is the output codomain;
- `R_M` is the readable retained-state set;
- `W_M` is the writable retained-state set;
- `E_M` is the declared error-result set;
- `F_M` is the execution contract.

## 10. Typed API

Every semantic API must identify the type of each input and output.

A generic numeric container does not replace semantic typing.

For example:

`phase`

`energy`

`force`

`ternary_target`

and:

`executed_ternary_state`

must not become interchangeable merely because they share a machine representation.

## 11. API Domain Validation

An API must reject or explicitly classify input outside its declared domain before the input can mutate retained semantic state.

## 12. API Codomain Validation

An API output must satisfy its declared codomain before downstream commit.

## 13. Immutable Input Contract

Unless mutation authority is explicitly declared, API inputs are semantically immutable.

Passing a reference to mutable storage does not grant semantic write authority.

## 14. State Ownership

Every retained state field has one declared semantic owner for each execution stage.

Ownership determines commit authority.

Read access does not imply write access.

## 15. State View

A state view is a typed read interface over retained state.

Let:

`V_X(S)`

denote the view of retained state `S` exposed to module `X`.

The view contains only fields that `X` is authorized to read.

## 16. Mutable State Interface

A mutable state interface is permitted only at an explicitly declared commit boundary.

General modules must not receive unrestricted mutable access to the complete retained state.

## 17. Request Object

A request is an immutable description of a proposed state change.

Define:

`Req = (source, destination, payload, coordinate, provenance)`.

A request does not itself mutate retained state.

## 18. Authorization Object

An authorization object records the decision that a request is admissible for a specified commit opportunity.

Define:

`Auth = (request_id, decision, coordinate, guards)`.

Authorization remains distinct from commit.

## 19. Commit Record

A commit record represents an executed retained-state mutation.

Define:

`Commit = (request_id, source_state_id, destination_state_id, coordinate, invariant_result)`.

A commit must be traceable to an authorized request.

## 20. Request-Commit Invariant

The implementation preserves:

`request ≠ authorization ≠ commit`.

No API may collapse these semantic stages unless the formal execution model explicitly defines a single atomic operation whose internal stages remain equivalent to the same contract.

## 21. State Snapshot

A state snapshot is an immutable representation of retained semantic state at a declared execution coordinate.

A snapshot is not automatically a complete restart checkpoint.

## 22. State Identifier

A retained state may carry:

`state_id`

for traceability.

The identifier is computational metadata.

It is not a physical observable.

## 23. Configuration Interface

The configuration module exposes immutable configuration state required by the declared implementation scope.

A configuration interface must distinguish:

- formal model parameters;
- numerical parameters;
- execution parameters;
- implementation parameters;
- validation parameters.

## 24. Configuration Immutability

A configuration declared immutable for a run must not change during that run.

Adaptive parameters must instead be represented as explicit result-affecting state.

## 25. Parameter Provenance

Every implementation-specific parameter must preserve applicable provenance.

Possible classes include:

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`.

Implementation parameters must not be promoted to universal physical constants.

## 26. EIF State Interface

The EIF state interface exposes the computational interatomic state required by the declared EIF realization.

Its fields may include, where defined:

- entity identities;
- species;
- positions;
- velocities;
- topology;
- local environments;
- invariant representations;
- equivariant representations;
- independently defined force or energy quantities;
- scale metadata;
- symmetry metadata.

No field is mandatory merely because it appears in this list; its presence depends on the selected EIF model.

## 27. Atomic Identity Contract

Atomic or interatomic entity identity must remain stable under storage reordering.

An index may locate an entity.

An index is not the entity identity itself.

## 28. Geometry Interface

The geometry interface must specify:

- coordinate representation;
- coordinate frame;
- dimensional units;
- periodicity where applicable;
- translation behavior;
- rotation behavior.

## 29. Topology Interface

The topology interface must distinguish:

- semantic interaction topology;
- neighbor search structure;
- derived adjacency cache;
- storage ordering.

A cache is not automatically semantic topology.

## 30. Local Environment Interface

A local environment API maps a declared interatomic state into a local environment representation.

Define:

`F_env: X_EIF → X_env`

for the selected domain.

Its locality rule must be explicit.

## 31. Symmetry Interface

Every equivariant or invariant API must declare:

- transformation group or set;
- input action;
- output action;
- domain;
- codomain;
- exact transformation relation.

## 32. Permutation API

Permutation behavior must distinguish:

`permutation invariance`

from:

`permutation equivariance`.

The API contract must state which relation applies.

## 33. Translation API

Translation behavior must be specified independently from permutation and rotation behavior.

## 34. Rotation API

Rotation behavior must identify the representation carried by each transformed output.

A scalar invariant and a vector equivariant output do not use the same transformation rule.

## 35. Symmetry Metadata

Where downstream validation depends on transformation semantics, symmetry metadata must remain accessible through the applicable interface.

## 36. Geometry-Ternary Boundary

No geometry API may automatically convert a translation, rotation, reflection, or storage permutation into a ternary polarity change unless an explicit model mapping defines that behavior.

## 37. Forward Mapping Interface

The EIF-to-TR mapping module exposes a typed mapping:

`F_E→TR: X_E → X_TR,in`

where:

- `X_E` is the selected EIF source representation;
- `X_TR,in` is the declared TR input space.

The mapping contract must specify:

- source domain;
- target codomain;
- locality;
- scale;
- dimensional behavior;
- symmetry behavior;
- history dependence;
- information loss;
- numerical behavior.

## 38. Forward Mapping Result

The forward mapping result must contain enough metadata to determine:

- source state identity;
- mapping configuration;
- output representation;
- execution coordinate;
- provenance.

## 39. Forward Mapping Failure

A forward mapping failure must not produce a fabricated valid TR state.

Failure remains distinct from active ternary `0`.

## 40. TR State Interface

The TR state interface exposes the continuous and discrete state required by the selected TR model.

Possible fields include:

- circular phase;
- frequency state;
- coupling state;
- resonance coordinates;
- history state;
- memory state;
- multiscale organization;
- resonance classification;
- ternary target;
- executed ternary state;
- pending destination.

Continuous and discrete fields remain semantically distinct.

## 41. Phase Interface

A phase API must preserve circular semantics.

A canonical computational representative may be used, but the formal phase remains an element of a circular state space.

## 42. Phase Difference API

A phase-difference operator must implement the declared circular difference relation.

It must not use unrestricted real subtraction as semantic phase difference without the required wrapping semantics.

## 43. Frequency Interface

A frequency state must specify dimensional semantics and whether it is:

- instantaneous;
- retained;
- filtered;
- target;
- derived.

These forms must not be silently conflated.

## 44. Delay Interface

A temporal-delay interface must identify the historical state and temporal coordinate accessed by the delayed relation.

## 45. Phase-Lag Interface

A phase-lag interface represents a phase relation.

It does not imply historical-state access.

The implementation preserves:

`delay ≠ phase lag`.

## 46. Memory Interface

A memory API must expose every result-affecting retained variable required by the selected memory model.

Hidden result-affecting memory violates deterministic closure.

## 47. History Interface

The history module provides typed historical state access.

A history query must specify:

- state field;
- temporal or execution coordinate;
- interpolation rule where required;
- boundary behavior.

## 48. Resonance Projection Interface

The resonance projection module implements:

`P_R: X_model → X_R`

for a declared model domain.

Its output is a resonance state:

`r ∈ X_R`.

## 49. Resonance Coordinate Contract

Every resonance coordinate must define its semantic meaning, representation, and dimensional status.

Resonance is not reduced automatically to one frequency coordinate.

## 50. Resonance Window Interface

A resonance window interface represents:

`W_R ⊂ X_R`.

It must expose sufficient information to evaluate membership and boundary semantics for the declared model.

## 51. Resonance Boundary Interface

Where the boundary:

`∂W_R`

is computationally evaluated, the API must distinguish exact formal boundary semantics from numerical tolerance used by the implementation.

## 52. Resonance Classification Interface

The minimal classification codomain is:

`X_RC = {OUTSIDE, BOUNDARY, INSIDE}`.

The classification API maps:

`C_R: X_R → X_RC`

or an explicitly history-dependent extension of that mapping.

## 53. Classification-Ternary Boundary

The API must not encode an implicit identity:

`OUTSIDE = -1`

`BOUNDARY = 0`

`INSIDE = 1`.

Any resonance-to-ternary mapping is a separate declared operator.

## 54. Resonance Scientific Boundary

The reference implementation preserves:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`phase locking ≠ resonance`

`coherence ≠ resonance`.

## 55. Phase-Order Interface

Where phase order is computed, its observable API must expose the declared mathematical definition.

For a classical Kuramoto-style global phase-order observable:

`R = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

This quantity remains a phase-order observable.

## 56. Phase Order and Coherence

The implementation preserves:

`phase order ≠ complete coherence`

and:

`R(t) ≠ C(t)`.

An API must not alias these quantities.

## 57. Multiscale Observable Interface

Where phase organization or resonance is represented at multiple scales, each observable must carry explicit scale identity.

Pair, cluster, supercluster, and global quantities must not be flattened into one scalar without an explicit aggregation mapping.

## 58. Ternary Target Interface

The ternary target API has codomain:

`T = {-1, 0, 1}`.

A target is a requested ternary destination.

It is not retained executed state.

## 59. Executed Ternary State Interface

The executed-state API exposes the currently retained balanced ternary state:

`q ∈ T`.

The canonical kernel is exactly:

`-1/0/1`.

## 60. Active Neutral Contract

The value:

`0`

is an active valid state.

The implementation must never reserve `0` automatically for:

- missing data;
- invalid state;
- error;
- absence;
- no signal.

## 61. Pending Destination Interface

A pending destination interface represents an opposite-polarity destination awaiting a later admissible second leg.

The pending destination must be distinguishable from:

- current executed state;
- current target;
- missing data;
- error state.

## 62. Ternary Execution API

Define the ternary execution operator:

`E_T: X_Texec → X_Texec × X_event`

where `X_Texec` contains the complete result-affecting ternary execution state.

The operator must preserve all ternary invariants.

## 63. Direct Opposite Transition Prohibition

The execution API must never directly commit:

`-1 → 1`

or:

`1 → -1`.

## 64. Neutral-Mediated Route

An opposite-polarity request must execute through:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

Each leg is a separate execution event.

## 65. First-Leg Contract

The first leg commits only the transition into active neutral.

It may create or retain a pending destination.

It does not commit the final opposite polarity.

## 66. Second-Leg Contract

The second leg may execute only under a later admissible execution event.

Completion of the first leg does not automatically authorize the second.

## 67. Neutral Retention Contract

The execution API must permit:

`0 → 0`

for any admissible number of execution steps unless the selected model imposes a stronger condition.

## 68. Same-State Retention

Where permitted, the API may retain:

`-1 → -1`

`0 → 0`

`1 → 1`.

Retention is an execution outcome, not missing execution.

## 69. Target-Executed Separation

The implementation must permit:

`target ≠ executed state`.

This is mandatory for correct opposite-polarity routing and other staged execution conditions.

## 70. Scheduler Interface

The scheduler API maps explicit scheduler state and eligible requests into scheduling decisions.

Define:

`S_sched: X_sched × X_req → X_decision`.

Scheduler state is computational execution-control state.

## 71. Scheduler Boundary

A scheduler is not a physical law.

A scheduler mode must not be interpreted automatically as:

- resonance;
- bifurcation;
- structural transition;
- physical phase transition.

## 72. Scheduler Determinism

For a deterministic scheduler, identical:

- scheduler state;
- request set;
- configuration;
- ordering context

must produce the same decision under the declared reproducibility contract.

## 73. Conflict Resolution Interface

Conflicting requests must enter an explicit conflict-resolution API.

The conflict rule must be deterministic when deterministic execution is claimed.

## 74. Capacity Interface

Where execution capacity is finite, capacity state must be represented explicitly.

Computational capacity is not automatically a physical capacity.

## 75. Authorization Interface

The authorization module evaluates requests against:

- guards;
- invariants;
- scheduler decisions;
- capacity;
- execution policy.

Its output is an authorization result, not a state mutation.

## 76. Commit Interface

Only the commit interface may apply authorized mutations to retained state fields within its declared ownership scope.

## 77. Atomic Commit

A multi-field state transition declared atomic must either commit all required fields or commit none of them.

Partial retained mutation is invalid.

## 78. Numerical Solver Interface

A numerical solver API must identify:

- mathematical problem;
- current accepted state;
- solver state;
- numerical parameters;
- proposed next state;
- diagnostics;
- acceptance status.

## 79. Solver Proposal

A solver proposal is not retained model state.

## 80. Solver Acceptance

Numerical acceptance authorizes a proposal for the next numerical stage.

It does not automatically constitute an architectural commit.

## 81. Rejected Numerical Step

A rejected numerical proposal must leave the previously accepted retained model state unchanged.

## 82. Numerical Failure and Neutral State

Numerical failure must never be represented implicitly as ternary `0`.

## 83. Precision Interface

The numerical API must expose or fix the precision semantics required by the reproducibility claim.

Possible representations include:

- floating point;
- fixed point;
- integer;
- exact rational;
- arbitrary precision.

## 84. Tolerance Interface

Every tolerance-based predicate must identify:

- compared quantity;
- absolute tolerance where applicable;
- relative tolerance where applicable;
- comparison rule;
- tolerance provenance.

## 85. Exact Predicate Interface

Exact categorical predicates, including ternary-state validity, must not be replaced by numerical tolerance.

## 86. Convergence Interface

A solver claiming convergence must expose the criterion used to determine convergence.

Iteration completion alone is not a convergence criterion.

## 87. Numerical Event Interface

A numerical event detector must return:

- event identity;
- event coordinate;
- localization result;
- numerical uncertainty or tolerance where applicable.

A numerical event is not automatically a bifurcation.

## 88. Reverse Mapping Interface

The reverse integration module implements:

`F_TR→E: X_TR,eligible → X_E,req`

where:

`X_E,req`

is the EIF update-request space.

The output remains a request until accepted by the EIF update boundary.

## 89. Reverse Mapping Contract

The reverse mapping must declare:

- source domain;
- target codomain;
- dimensional behavior;
- symmetry behavior;
- locality;
- scale;
- information loss;
- history dependence;
- physical interpretation.

## 90. Force Interface Boundary

A reverse mapping may produce a force-related request only when force is independently defined with valid dimensional and transformation semantics.

The implementation preserves:

`ternary state ≠ force`.

## 91. Energy Interface Boundary

A reverse mapping may produce an energy-related quantity only when energy is independently defined.

The implementation preserves:

`ternary state ≠ energy`

and:

`resonance classification ≠ energy`.

## 92. Chemical-Bond Boundary

No API may identify phase locking or resonance directly with a chemical bond without an independently defined interatomic mapping.

The implementation preserves:

`phase relation ≠ chemical bond`.

## 93. Mechanical-Force Boundary

No phase-coupling API is automatically a mechanical-force API.

The implementation preserves:

`phase coupling ≠ mechanical force`.

## 94. EIF Update Request

An EIF update request is a typed proposal to modify EIF state.

It must identify:

- destination fields;
- proposed values or increments;
- source mapping;
- execution coordinate;
- dimensional metadata;
- provenance.

## 95. EIF Update Authorization

EIF update authorization verifies the request against:

- EIF state domain;
- dimensional constraints;
- symmetry constraints;
- topology constraints;
- model-specific guards;
- commit policy.

## 96. EIF Commit

Only an authorized EIF update may modify retained EIF state.

## 97. Integrated Execution API

The integrated execution API coordinates:

`EIF state`

`→ equivariant representation`

`→ forward EIF-to-TR mapping`

`→ TR evolution`

`→ resonance projection`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated ternary execution`

`→ reverse TR-to-EIF request`

`→ EIF authorization`

`→ EIF commit`.

## 98. Integrated State

The integrated retained state must contain every result-affecting field required to continue the selected closed-loop execution.

## 99. Integrated State Ownership

Each field of integrated retained state must have one declared semantic owner per execution stage.

## 100. Integrated Commit Boundary

A closed-loop execution step must identify where each layer commits its retained state.

Intermediate derived values must not silently become retained state.

## 101. No Instantaneous Recursive Feedback

Feedback from TR into EIF must enter through a declared subsequent execution coordinate unless the mathematical model explicitly defines a simultaneous coupled solve.

## 102. Simultaneous Solve Boundary

If a simultaneous coupled solve is used, its joint state space, equations, numerical method, convergence criterion, and commit semantics must be explicitly defined.

It must not be approximated by undeclared recursive API calls.

## 103. History Module API

The history module owns retained historical data required by:

- delay;
- memory;
- hysteresis;
- filtering;
- history-dependent resonance windows;
- history-dependent mappings.

## 104. History Append Contract

A history append operation occurs only after the corresponding source state reaches the declared retention point.

## 105. History Query Contract

A history query must not access future state.

The implementation preserves computational causality.

## 106. Interpolation Contract

If a requested historical coordinate is not stored exactly, interpolation requires an explicitly declared interpolation operator.

## 107. Extrapolation Contract

Extrapolation must be explicit.

It must not masquerade as historical observation.

## 108. Memory State API

Result-affecting memory state must be part of checkpoint and replay closure.

## 109. Observable Interface

An observable API maps retained or explicitly derived state into an observable value without modifying semantic state.

Define:

`O: X_state → X_obs`.

## 110. Observable Purity

An observable declared pure must not alter:

- modeled state;
- scheduler state;
- history;
- pending routes;
- solver state.

## 111. Local Observable

A local observable must identify its entity, locality, or scale.

## 112. Global Observable

A global observable is derived from a declared global aggregation or global state relation.

It must not overwrite local state.

## 113. Trace Interface

The trace module records execution evidence.

A trace record must be immutable after emission.

## 114. Core Trace Record

A core trace record should contain, where applicable:

- trace schema identifier;
- execution coordinate;
- model-time coordinate;
- module identifier;
- source state identifier;
- request identifier;
- authorization result;
- commit identifier;
- target state;
- executed state;
- pending destination;
- relevant observables;
- validation flags.

Only fields applicable to the recorded event are required.

## 115. Trace Event Type

Trace event type must distinguish events such as:

- proposal;
- request;
- authorization;
- rejection;
- commit;
- numerical acceptance;
- numerical rejection;
- ternary first leg;
- ternary second leg;
- checkpoint;
- restore;
- validation result.

## 116. Ternary Trace Contract

A ternary trace must make direct opposite committed transitions detectable.

It must preserve separate events for both legs of an opposite-polarity route.

## 117. Integrated Trace Contract

An integrated trace must permit reconstruction of the semantic chain from EIF source state through TR processing and back to an EIF update request and commit.

## 118. Trace Non-Interference

Trace collection must not alter semantic execution under the declared deterministic criterion.

## 119. Artifact Interface

An artifact is a persistent computational object emitted or consumed at a declared architecture boundary.

Examples include:

- configuration;
- serialized state;
- trace;
- checkpoint;
- validation report;
- benchmark result;
- test fixture;
- schema;
- deterministic reference output.

## 120. Artifact Identity

Every persistent artifact intended for machine interpretation must have an unambiguous artifact identity.

The identity may include:

- artifact type;
- schema identifier;
- schema version;
- implementation identifier;
- configuration identifier;
- creation coordinate;
- provenance.

## 121. Artifact Schema

Machine-readable artifacts must have a declared schema or equivalent formal structural contract.

## 122. Schema Version

A serialized artifact must identify the schema version required for interpretation.

## 123. Schema Compatibility

Compatibility between schema versions must be explicit.

An implementation must not silently reinterpret incompatible fields.

## 124. Semantic Version Boundary

A schema version identifies an artifact contract.

It does not by itself establish the scientific maturity of the entire TR-EIF framework.

## 125. Serialization Interface

Serialization maps an in-memory typed object into a persistent representation.

Define:

`Ser: X → B`

where `B` is the selected serialized representation space.

## 126. Deserialization Interface

Deserialization maps a valid serialized representation back into a typed computational object:

`Des: B_valid → X`.

## 127. Round-Trip Contract

For a lossless serialization contract:

`Des(Ser(x)) = x`

under the declared semantic equality relation.

Byte identity is not required unless explicitly claimed.

## 128. Lossy Artifact Contract

If serialization is intentionally lossy, the lost information must be declared.

A lossy artifact must not be used as a complete checkpoint unless the discarded information is irrelevant to restart semantics.

## 129. Canonical Serialization

Where byte-identical reproducibility is claimed, serialization must define any result-affecting canonicalization requirements, including ordering and numeric formatting where applicable.

## 130. Checkpoint Interface

A checkpoint artifact must contain all state required for the declared restart scope.

## 131. Checkpoint State Classes

A complete checkpoint may require:

- EIF retained state;
- TR retained state;
- ternary executed state;
- ternary target where result-affecting;
- pending destination;
- history;
- memory;
- solver state;
- scheduler state;
- topology state;
- configuration identity;
- random state where applicable.

## 132. Checkpoint Completeness

A state snapshot lacking required restart state is not a complete checkpoint.

## 133. Checkpoint Validation

Before restoration, a checkpoint must be validated for:

- schema;
- configuration compatibility;
- state-domain validity;
- ternary invariants;
- dimensional consistency;
- required state completeness.

## 134. Restore Interface

Restore reconstructs a complete retained execution state from a valid checkpoint.

Restore must not execute model evolution.

## 135. Replay Interface

Replay resumes execution from restored state under a declared input and configuration sequence.

## 136. Replay Comparison Interface

Replay comparison must specify one of the applicable relations:

- semantic equivalence;
- tolerance equivalence;
- exact state equality;
- byte identity.

## 137. Determinism Scope

A deterministic implementation claim must identify the environment scope in which reproducibility is expected.

## 138. Hidden-State Prohibition

Any hidden result-affecting state that is absent from deterministic closure violates the reference implementation contract.

## 139. Randomness Interface

Where stochastic behavior exists, random-state management must be explicit.

A random seed alone is sufficient only when it fully determines the required random stream under the declared implementation scope.

## 140. Validation Interface

The validation module evaluates evidence against explicit acceptance criteria.

Its result domain is:

`X_Val = {PASS, FAIL, UNRESOLVED}`.

## 141. Validation-Ternary Separation

The implementation preserves:

`PASS / FAIL / UNRESOLVED ≠ -1/0/1`.

`UNRESOLVED` must never be encoded as active neutral `0`.

## 142. Validation Claim Interface

A validation claim must expose:

- claim identifier;
- claim statement;
- scope;
- evidence references;
- acceptance criterion;
- result.

## 143. Validation Evidence Interface

Evidence must identify the implementation and configuration that produced it.

## 144. Qualification Artifact

A qualification artifact records one or more validated claims for a fixed implementation scope.

It does not expand the scope beyond the claims it contains.

## 145. Failure Interface

Every module must expose failure through an explicit failure contract.

Failure must not silently mutate semantic state unless the architecture explicitly defines a recovery transaction.

## 146. Failure Result

A failure result should identify:

- module;
- operation;
- execution coordinate;
- failure class;
- affected request or state;
- whether retained state changed.

## 147. Failure Atomicity

A failed atomic operation must leave retained state at the pre-operation semantic state.

## 148. Invalid Ternary Input

Any attempted retained ternary value outside:

`{-1, 0, 1}`

must be rejected.

## 149. Invalid Direct Transition

Any request attempting direct committed:

`-1 → 1`

or:

`1 → -1`

must be rejected or converted into the defined neutral-mediated routing procedure.

It must never commit directly.

## 150. Invalid Numerical State

A nonfinite or otherwise invalid numerical state must follow the numerical error contract.

It must not be converted silently into a valid model state.

## 151. Invalid Cross-Layer Mapping

A cross-layer mapping output outside its declared codomain must not enter downstream retained state.

## 152. Invalid Symmetry Contract

A mapping that fails a mandatory declared symmetry condition is nonconforming for that condition.

## 153. API Side-Effect Contract

Every API must declare whether it is:

- pure;
- request-producing;
- state-mutating;
- artifact-emitting.

An API must not have undeclared semantic side effects.

## 154. Pure API

A pure API reads its declared input and produces output without modifying retained state.

## 155. Request-Producing API

A request-producing API may create a proposed mutation but does not apply it.

## 156. State-Mutating API

A state-mutating API exists only at a declared commit boundary.

## 157. Artifact-Emitting API

An artifact-emitting API writes persistent evidence or state representation without changing modeled state unless that effect is independently declared.

## 158. API Idempotence

Where an API is declared idempotent, repeated invocation with the same admissible state must not produce additional semantic mutation beyond the first valid application.

Idempotence must not be assumed for all APIs.

## 159. API Ordering

When API order affects results, the execution pipeline must define that order explicitly.

## 160. API Reentrancy

Reentrancy is an implementation property.

It must not be claimed unless shared state, mutable caches, and execution-control state preserve the declared semantics under reentrant use.

## 161. Concurrency Boundary

Concurrency is permitted only when it preserves the required ordering, ownership, and deterministic contracts.

## 162. Parallel Read

Multiple modules may read immutable state concurrently when the implementation guarantees consistent semantics.

## 163. Parallel Write

Parallel writes require explicit ownership and conflict semantics.

Uncoordinated writes to the same semantic state are nonconforming.

## 164. Reduction Interface

Parallel reductions must specify ordering or comparison semantics sufficient for the claimed reproducibility level.

## 165. Cache Interface

A derived cache must declare whether it is:

- semantically irrelevant;
- result-affecting.

## 166. Pure Derived Cache

Rebuilding a pure derived cache must not change semantic output.

## 167. Result-Affecting Cache

A result-affecting cache is state.

It must participate in ownership, checkpoint, and deterministic closure.

## 168. Backend Interface

A conforming implementation may support multiple computational backends.

A backend may alter:

- performance;
- precision;
- storage representation;
- execution parallelism.

It must not silently alter formal semantics.

## 169. Backend Capability Descriptor

A backend should declare supported:

- numeric representations;
- deterministic scope;
- symmetry operations;
- solver operations;
- serialization features;
- hardware-specific constraints.

## 170. Backend Equivalence

Two backends are semantically equivalent only under a declared comparison relation and tested scope.

## 171. Hardware Boundary

A hardware realization may implement selected module APIs directly.

Hardware implementation does not change the formal type or semantic contract of those APIs.

## 172. Software Boundary

A software realization may implement the same logical contract using software structures.

Source-language constructs do not define the formal semantics.

## 173. Hybrid Boundary

A hybrid implementation must make hardware/software transfer boundaries explicit.

## 174. Transfer Artifact

A hardware/software transfer object must preserve:

- semantic type;
- encoding;
- ordering;
- dimensional metadata where required;
- validity information.

## 175. Quantization Boundary

Quantization is a numerical representation operation.

It is not automatically ternary classification.

The implementation preserves:

`quantization ≠ ternary state assignment`.

## 176. Saturation Boundary

Numerical saturation must not silently alter categorical ternary semantics.

## 177. Overflow Boundary

Overflow must follow an explicit error or saturation contract.

Wraparound is valid only if explicitly defined for that numerical field.

## 178. Implementation Directory Boundary

The reference specification defines logical modules, not mandatory filesystem paths.

A conforming repository may organize source files differently provided that:

- module responsibilities remain identifiable;
- APIs remain testable;
- ownership remains enforceable;
- artifacts remain traceable;
- qualification evidence remains attributable.

## 179. Package Boundary

A package or namespace is an implementation convenience.

Package identity must not replace semantic module identity.

## 180. Public API Boundary

A public implementation API is an interface intended for use outside its defining module.

Its contract must be stable within the compatibility policy declared by the implementation.

## 181. Internal API Boundary

An internal API may change without external compatibility guarantees, but it must still preserve architecture invariants.

## 182. Entry Point

A reference implementation must expose an execution entry point for each declared runnable scope.

An entry point must identify:

- configuration;
- initial state or checkpoint;
- execution horizon or stopping condition;
- external input source;
- artifact destinations;
- validation mode where applicable.

## 183. Initialization API

Initialization constructs valid retained state from admissible configuration and initial data.

## 184. Initialization Closure

Initialization must establish all mandatory state fields before normal evolution begins.

Uninitialized semantic state is invalid.

## 185. Initial Ternary State

Every initialized executed ternary state must belong to:

`T = {-1, 0, 1}`.

## 186. Initial Pending State

Pending destination must be explicitly absent or valid.

It must not contain an undefined machine value.

## 187. Initial History

If the model requires prehistory, initialization must provide it explicitly or use a declared boundary condition.

## 188. Initial Solver State

Any solver state required for deterministic execution must be initialized explicitly.

## 189. Initial Scheduler State

Any result-affecting scheduler state must be initialized explicitly.

## 190. Execution Step API

A canonical execution step accepts a complete valid retained state and returns:

- next retained state;
- emitted trace events;
- emitted artifacts where applicable;
- execution status.

## 191. Execution Step Atomicity

A step may contain multiple internal stages, but retained-state commit semantics must remain explicit.

## 192. Execution Status

Execution status is control metadata.

It is not a ternary state and not a resonance classification.

## 193. Stopping Condition Interface

A stopping condition must be explicit.

Examples include:

- execution-coordinate limit;
- model-time limit;
- convergence criterion;
- declared event;
- external stop request;
- validation failure.

## 194. Stop Is Not Neutral

Stopping execution does not imply ternary `0`.

## 195. External Input Interface

External inputs must enter through typed validated interfaces.

External input must not bypass module guards and state ownership.

## 196. External Output Interface

External outputs must be produced through observable, trace, or artifact interfaces.

External output generation must not silently mutate modeled state.

## 197. Artifact Input Validation

A consumed artifact must be validated before semantic use.

Validation may include:

- schema;
- version;
- checksum where defined;
- dimensional metadata;
- domain constraints;
- configuration compatibility.

## 198. Artifact Output Validation

A generated artifact must satisfy its declared schema before publication or downstream consumption.

## 199. Artifact Provenance

Artifacts carrying scientific or qualification significance must preserve applicable provenance.

## 200. Artifact Traceability

A persistent artifact should be traceable through:

`artifact`

`→ implementation`

`→ configuration`

`→ source state or fixture`

`→ execution`

`→ schema`

`→ provenance`.

## 201. Reference Implementation Manifest

A reference implementation may expose a machine-readable manifest describing:

- implementation identity;
- supported architecture scope;
- supported artifact schemas;
- supported numerical backends;
- supported deterministic level;
- supported qualification sets.

The manifest reports capability.

It does not itself prove conformance.

## 202. Capability and Qualification

The architecture preserves:

`declared capability ≠ qualified capability`.

A capability becomes qualified only through applicable evidence.

## 203. API Conformance Testability

Every mandatory API contract must be testable through:

- direct module test;
- interface test;
- integrated trace;
- or another explicit qualification mechanism.

## 204. State Contract Testability

Every retained-state invariant must be externally inspectable or testable through controlled execution evidence.

## 205. Artifact Contract Testability

Every persistent artifact schema must be machine-validatable or equivalently testable.

## 206. Deterministic API Testability

Every deterministic API claim must define the comparison relation used for repeated execution.

## 207. Symmetry API Testability

Every equivariance or invariance claim must identify transformations suitable for controlled qualification.

## 208. Numerical API Testability

Every numerical acceptance claim must expose the diagnostics required by its acceptance criterion.

## 209. Integrated API Testability

Every cross-layer mapping must permit traceability of source and destination states.

## 210. Minimal Configuration API Contract

A conforming configuration API must provide:

1. configuration identity;
2. formal model parameters;
3. numerical parameters;
4. execution parameters;
5. implementation parameters;
6. provenance;
7. validation before use.

## 211. Minimal State API Contract

A conforming state API must provide:

1. typed retained fields;
2. state identity;
3. execution coordinate;
4. ownership metadata or enforceable ownership semantics;
5. validity checking;
6. immutable read access outside commit authority.

## 212. Minimal EIF API Contract

A conforming EIF API must preserve, where applicable:

1. entity identity;
2. geometry;
3. topology;
4. locality;
5. dimensional semantics;
6. permutation behavior;
7. translation behavior;
8. rotation behavior;
9. invariant/equivariant representation semantics.

## 213. Minimal TR API Contract

A conforming TR API must preserve, where applicable:

1. circular phase;
2. frequency semantics;
3. coupling state;
4. resonance coordinates;
5. resonance window semantics;
6. history and memory;
7. phase-order observables;
8. resonance classification;
9. target/executed-state separation.

## 214. Minimal Ternary API Contract

A conforming ternary API must preserve:

1. exact domain `{-1, 0, 1}`;
2. canonical `-1/0/1` notation;
3. active neutral `0`;
4. target/executed-state separation;
5. pending destination;
6. forbidden direct opposite commits;
7. neutral-mediated opposite routes;
8. separate execution legs;
9. independent second-leg authorization;
10. neutral retention.

## 215. Minimal Forward Mapping API Contract

A conforming EIF-to-TR API must define:

1. source domain;
2. target codomain;
3. symmetry behavior;
4. locality;
5. scale;
6. dimensional behavior;
7. history dependence;
8. information loss;
9. numerical behavior;
10. traceability.

## 216. Minimal Reverse Mapping API Contract

A conforming TR-to-EIF API must define:

1. source domain;
2. request codomain;
3. dimensional behavior;
4. symmetry behavior;
5. locality;
6. scale;
7. history dependence;
8. physical interpretation;
9. request/commit separation;
10. traceability.

## 217. Minimal Numerical Solver API Contract

A conforming numerical solver API must provide:

1. accepted current state;
2. solver state;
3. numerical parameters;
4. proposal;
5. diagnostics;
6. acceptance result;
7. failure result;
8. precision semantics;
9. tolerance semantics;
10. rollback on rejection.

## 218. Minimal Scheduler API Contract

A conforming scheduler API must provide:

1. scheduler state;
2. eligible requests;
3. deterministic decision rule where claimed;
4. conflict resolution;
5. capacity semantics where applicable;
6. explicit separation from physical time and physical law.

## 219. Minimal Trace API Contract

A conforming trace API must provide enough evidence to reconstruct the claims for which the trace is used.

For ternary execution this includes:

- target;
- executed state;
- pending state where applicable;
- separate transition legs;
- commit identity.

## 220. Minimal Checkpoint API Contract

A conforming checkpoint API must provide:

1. complete result-affecting retained state;
2. configuration identity;
3. schema identity;
4. validation;
5. restore semantics;
6. pending-route state;
7. history and memory;
8. solver and scheduler state where required.

## 221. Minimal Replay API Contract

A conforming replay API must provide:

1. validated checkpoint;
2. restored state;
3. declared continuation input;
4. deterministic scope;
5. comparison relation;
6. replay evidence.

## 222. Minimal Validation API Contract

A conforming validation API must provide:

1. claim;
2. scope;
3. evidence;
4. acceptance criterion;
5. result in `{PASS, FAIL, UNRESOLVED}`;
6. implementation identity;
7. configuration identity.

## 223. Mandatory Implementation Invariants

The reference implementation must preserve the following invariants.

1. Formal theory remains distinct from implementation.

2. Logical module identity remains distinct from source filename.

3. Semantic type remains distinct from machine representation.

4. Every retained state field has declared semantic ownership.

5. Read access does not imply write authority.

6. Request remains distinct from authorization.

7. Authorization remains distinct from commit.

8. Numerical proposal remains distinct from accepted numerical state.

9. Numerical acceptance remains distinct from architectural commit.

10. Observable evaluation does not mutate modeled state unless explicitly defined otherwise.

11. Trace remains distinct from modeled state.

12. Snapshot remains distinct from complete checkpoint.

13. Validation result remains distinct from balanced ternary state.

14. Missingness remains distinct from balanced ternary `0`.

15. Error remains distinct from balanced ternary `0`.

16. The ternary domain remains exactly `{-1, 0, 1}`.

17. The canonical kernel remains exactly `-1/0/1`.

18. `0` remains an active valid state.

19. Direct committed `-1 → 1` remains forbidden.

20. Direct committed `1 → -1` remains forbidden.

21. Opposite-polarity execution remains neutral-mediated.

22. Every leg of an opposite route remains a separate execution event.

23. The first leg does not automatically authorize the second.

24. Neutral may remain retained for multiple admissible execution steps.

25. Ternary target remains distinct from executed ternary state.

26. Resonance classification remains distinct from ternary state.

27. Resonance remains distinct from frequency equality.

28. Resonance remains distinct from synchronization.

29. Synchronization remains distinct from phase locking.

30. Phase locking remains distinct from resonance.

31. Coherence remains distinct from uniformity.

32. Coherence remains distinct from resonance.

33. Phase order remains distinct from complete coherence.

34. `R(t)` remains distinct from `C(t)`.

35. Resonance-window crossing remains distinct from bifurcation.

36. Bifurcation remains distinct from ternary transition.

37. Ternary transition remains distinct from structural transition.

38. Structural transition remains distinct from physical phase transition.

39. Oscillator phase remains distinct from physical phase of matter.

40. Phase coupling remains distinct from mechanical force.

41. Phase relation remains distinct from chemical bond.

42. Ternary state remains distinct from force.

43. Ternary state remains distinct from energy.

44. Resonance classification remains distinct from energy.

45. Delay remains distinct from phase lag.

46. Permutation invariance remains distinct from permutation equivariance.

47. Translation, rotation, and permutation remain separately represented transformation behaviors.

48. Geometry transformation does not automatically alter ternary polarity.

49. Quantization remains distinct from ternary classification.

50. FRP remains distinct from TR-EIF.

## 224. FRP Executable Reference Interface

FRP may be connected to the reference architecture through explicit specialization interfaces for mechanisms verified in the current executable source.

Such an interface may expose verified:

- phase evolution;
- retained frequency dynamics;
- phase-order observables;
- phase-derived ternary targets;
- scheduler state;
- pending opposite-polarity routing;
- active-neutral execution;
- deterministic trace fields.

## 225. FRP Specialization Boundary

FRP-specific values remain implementation parameters.

Examples of verified specialization parameters may include:

- phase-lag values;
- coupling constants;
- scheduler ratios;
- phase-to-target thresholds;
- memory coefficients.

They must not enter the general TR-EIF API as universal constants.

## 226. FRP Target Interface Boundary

A phase-derived FRP ternary classification used as a target must enter the general ternary execution interface as:

`ternary_target`.

It must not bypass the execution boundary and directly overwrite:

`executed_ternary_state`.

## 227. FRP Scheduler Interface Boundary

FRP scheduler modes may specialize the scheduler API.

They do not redefine the general scheduler contract.

## 228. FRP Phase-Order Interface Boundary

A verified FRP Kuramoto-style phase-order observable may implement a phase-order API.

It must not be exported as complete coherence.

The distinction:

`R(t) ≠ C(t)`

remains mandatory.

## 229. FRP Memory Interface Boundary

A verified retained-frequency lag mechanism may implement one memory channel.

It must not be relabeled as explicit pairwise temporal delay unless such delayed historical access is independently implemented.

## 230. Reference Implementation Traceability

Every important implementation claim should follow:

`TR-EIF formal concept`

`→ reference architecture contract`

`→ module API`

`→ implementation object`

`→ executable state or observable`

`→ artifact`

`→ qualification evidence`

`→ scope`.

## 231. Cross-Layer Traceability

Every integrated execution should permit:

`EIF source state`

`→ equivariant representation`

`→ forward mapping`

`→ TR state`

`→ resonance state`

`→ resonance classification`

`→ ternary target`

`→ executed ternary transition`

`→ reverse mapping request`

`→ EIF authorization`

`→ EIF commit`.

## 232. No Hidden Semantic Conversion

No module may perform an undeclared conversion between semantic domains.

In particular, the implementation must not silently convert:

- resonance class into ternary state;
- phase order into coherence;
- phase relation into bond identity;
- ternary state into force;
- ternary state into energy;
- geometry transformation into polarity inversion;
- numerical failure into neutral state.

## 233. Implementation Closure

A runnable reference implementation scope is computationally closed only when all result-affecting state is represented through declared contracts.

Closure includes, where applicable:

- modeled state;
- integration state;
- history;
- memory;
- solver state;
- scheduler state;
- pending routes;
- topology state;
- configuration;
- random state.

## 234. API Closure

API closure requires that every inter-module semantic dependency crosses a declared interface.

Undeclared shared mutable state violates API closure.

## 235. Artifact Closure

Artifact closure requires that every persistent object required for restart, replay, validation, or downstream machine interpretation has a declared artifact contract.

## 236. Qualification Closure

Implementation closure does not imply qualification closure.

Qualification closure requires the evidence and acceptance conditions established in Chapter 06.

## 237. Language Independence

The contracts in this chapter are language-independent.

A programming-language binding must preserve:

- semantic types;
- module boundaries;
- ownership;
- transition semantics;
- numerical contracts;
- symmetry contracts;
- artifact contracts.

## 238. Runtime Independence

The reference architecture is not identified with a particular operating system, runtime, interpreter, virtual machine, or accelerator.

Runtime-specific behavior must remain inside the implementation boundary.

## 239. Hardware Independence

The reference specification permits software, hardware, and hybrid realizations.

A hardware implementation remains conforming only when it preserves the same declared semantic contracts.

## 240. Repository Independence

The formal module graph is not a mandatory repository directory tree.

Repository structure may evolve without changing the theory provided that semantic boundaries and traceability remain intact.

## 241. Implementation Acceptance

A concrete implementation is accepted as a TR-EIF reference implementation for a declared scope only when:

1. its supported module scope is explicit;
2. its APIs satisfy the applicable contracts;
3. retained-state ownership is explicit;
4. cross-layer mappings are typed;
5. numerical semantics are explicit;
6. ternary execution preserves `-1/0/1`;
7. active neutral semantics are preserved;
8. direct opposite commits are absent;
9. checkpoint and replay state is complete for claimed deterministic restart;
10. artifacts satisfy declared schemas;
11. mandatory qualification claims for that scope are `PASS`.

## 242. Final Statement

The TR-EIF reference implementation is defined by semantic contracts rather than by one programming language, one repository layout, or one executable specialization.

Its computational structure preserves:

`formal theory`

`→ typed state`

`→ explicit module API`

`→ deterministic or explicitly stochastic operation`

`→ request`

`→ authorization`

`→ commit`

`→ retained state`

`→ observable`

`→ artifact`

`→ qualification evidence`.

The balanced ternary kernel remains exactly:

`-1/0/1`

with:

`T = {-1, 0, 1}`.

The state:

`0`

remains active.

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

Opposite-polarity execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

with independent execution and authorization of each leg.

The implementation preserves:

`target ≠ executed state`

`request ≠ authorization`

`authorization ≠ commit`

`numerical proposal ≠ accepted numerical state`

`numerical acceptance ≠ architectural commit`

`resonance classification ≠ ternary state`

`validation result ≠ ternary state`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ force`

`ternary state ≠ energy`

`resonance classification ≠ energy`

`delay ≠ phase lag`

`permutation invariance ≠ permutation equivariance`

`quantization ≠ ternary classification`

`FRP ≠ TR-EIF`.

EIF and TR remain mathematically distinct layers until connected through explicit typed mappings.

The implementation therefore realizes the integrated architecture without erasing the semantic boundaries that make the architecture testable, reproducible, and scientifically traceable.
