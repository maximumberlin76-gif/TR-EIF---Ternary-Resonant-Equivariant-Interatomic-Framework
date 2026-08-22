# Resonance Observables, Trace Semantics, and Validation

## 1. Purpose

This document defines the observable, trace, and validation layer of the Ternary Resonant Equivariant Interatomic Framework.

The chapter formalizes:

- typed resonance observables;
- state-to-observable mappings;
- history-dependent observables;
- local, global, and multiscale observation spaces;
- execution traces;
- observable traces;
- event traces;
- provenance-bearing evidence;
- sampling and resolution;
- trace completeness relative to a claim;
- deterministic replay;
- exact and numerical validation;
- claim-scoped validation predicates;
- executable FRP trace semantics;
- the output boundary of the ternary resonance layer before EIF integration.

The purpose of this layer is not to replace the mathematical state of the modeled system with telemetry.

Its purpose is to establish a typed chain:

`mathematical state`

`→ declared observable mapping`

`→ ordered trace`

`→ claim-scoped evidence`

`→ validation result`

while preserving the distinction between the complete TR-EIF architecture and any one executable specialization.

## 2. Dependency

This chapter depends on the committed definitions of Volume 01 and on Chapters 01–08 of Volume 02.

In particular, it inherits:

- typed state spaces and mappings from Volume 01;
- provenance classes from Volume 01;
- resonance-coordinate space `X_R`;
- resonance-coordinate mapping `P_R`;
- resonance window `W_R`;
- resonance boundary `∂W_R`;
- resonance classification semantics;
- balanced ternary domain `T = {-1, 0, 1}`;
- active neutral semantics;
- target-state and executed-state separation;
- transition-route semantics;
- phase-domain semantics;
- phase-order semantics;
- resonance-regime and bifurcation boundaries;
- multiscale and hierarchical resonance semantics.

This chapter does not redefine those objects.

It defines how they may be observed, serialized, compared, replayed, and validated.

## 3. Scientific Status Classes

The objects in this chapter are separated by scientific status.

### 3.1 GENERAL MATHEMATICAL STRUCTURE

Typed mappings, product spaces, ordered sequences, predicates, equivalence relations, sampling maps, and validation relations use general mathematical structure.

### 3.2 TR-EIF FORMAL / AUTHOR-DEFINED

The TR-EIF observable contracts, trace semantics, claim-scoped validation model, active-neutral trace requirements, provenance requirements, and TR-to-EIF output boundary are author-defined framework semantics.

### 3.3 FRP EXECUTABLE REFERENCE

Concrete trace fields, fixed-point telemetry, deterministic replay records, long-run checkpoint evidence, and Observatory interchange artifacts are executable reference semantics taken from the current FRP repository.

FRP-specific fields, identifiers, thresholds, fixed-point encodings, and telemetry names are implementation objects rather than universal TR-EIF physical quantities.

### 3.4 EMPIRICAL / CALIBRATED

An observable becomes empirically calibrated only when its relation to measured physical data is independently established.

Executable production of a value does not by itself establish empirical calibration.

### 3.5 UNVERIFIED

A claim lacking the required source, model relation, trace resolution, or empirical evidence remains unresolved under the applicable provenance and validation rules.

## 4. Position in the TR-EIF Architecture

The complete project identity remains:

`TR-EIF = Ternary Resonant Equivariant Interatomic Framework`

with:

`TR = Ternary Resonant`

and:

`EIF = Equivariant Interatomic Framework`

This chapter belongs to the TR layer.

It does not redefine TR-EIF as:

- only a ternary state machine;
- only a resonance classifier;
- only a phase-oscillator model;
- only a Kuramoto–Sakaguchi model;
- only an interatomic potential;
- only a machine-learning model;
- only FRP documentation.

The TR observable layer must remain sufficiently typed to connect later to the separately formalized EIF layer through explicit mappings.

## 5. System-to-Validation Chain

The modeling order remains:

`system class`

`→ boundaries`

`→ state spaces`

`→ variables`

`→ transformations`

`→ invariants`

`→ mathematical model`

`→ numerical realization`

`→ observable trace`

`→ validation`

Observables and validation therefore occur after the model state and its semantics have been declared.

A telemetry field must not be used to invent the state semantics that it is supposed to observe.

## 6. State Is Not Observable

Let `S_TR` denote the declared state space of a particular TR model.

Let `Y_O` denote an observable space.

A memoryless observable is a mapping:

`O: S_TR → Y_O`

For `s ∈ S_TR`, the observable value is:

`y = O(s)`

The observable value `y` is not automatically the complete state `s`.

Unless `O` is injective on the declared domain:

`O(s_1) = O(s_2)`

does not imply:

`s_1 = s_2`

## 7. Observable Space

Every observable must have a declared codomain.

Examples of admissible observable codomains include:

- a real interval;
- a circular phase domain;
- a finite classification set;
- the balanced ternary set `T`;
- a finite event set;
- a vector space;
- a product space;
- a structured record space.

The codomain must match the semantics of the observable.

A scalar field must not silently stand for a multiscale or structured state unless the aggregation rule is explicitly defined.

## 8. Observable Family

A model may expose multiple observable channels.

Let `I_O` be the finite index set of declared observable channels.

For every `a ∈ I_O`, let:

`O_a: S_TR → Y_a`

be the observable mapping for channel `a`.

The combined observable space is:

`Y_TR = ∏_(a ∈ I_O) Y_a`

and the combined observable mapping is:

`O_TR: S_TR → Y_TR`

with:

`O_TR(s) = (O_a(s))_(a ∈ I_O)`

The channel family is model-specific.

No universal scalar observable is imposed by TR-EIF.

## 9. History-Dependent Observable

Let `H_TR` denote the declared history-state space of a model.

A history-dependent observable is typed as:

`O_H: H_TR → Y_H`

where `Y_H` is its declared codomain.

If the observable depends on history, a current state snapshot is not sufficient to reproduce it unless the current state already contains a sufficient history state.

Therefore:

`history-dependent observable ≠ snapshot-only observable`

## 10. Event Observable

Let `X_Event` be a declared finite or countable event space.

An event extraction relation may be represented by:

`E_TR: H_TR → X_Event*`

where `X_Event*` denotes a finite ordered event sequence.

The event relation may depend on:

- current state;
- previous state;
- target state;
- transition guard;
- pending route;
- scheduler state;
- boundary crossing;
- history state.

An event is not necessarily reconstructible from one post-event state.

## 11. Local Observable

For local component `i` with local state space `S_i`, a local observable is:

`O_i: S_i → Y_i`

A local observable may describe:

- local resonance coordinates;
- local resonance classification;
- local phase;
- local ternary state;
- local route state;
- local thermal or other model state;
- local transition activity.

A local observable must not be interpreted automatically as a global observable.

## 12. Global Observable

For a complete model state `s ∈ S_TR`, a global observable may be defined as:

`O_G: S_TR → Y_G`

A global observable may aggregate local state, but its information content is determined by its mapping.

Therefore:

`global observable ≠ complete local-state reconstruction`

unless the mapping is explicitly invertible on the declared domain.

## 13. Multiscale Observable

Let `L` be the declared scale index set from Chapter 08.

For every scale `ell ∈ L`, let the scale state space be `S_ell` and the observable space be `Y_ell`.

A scale-specific observable is:

`O_ell: S_ell → Y_ell`

The multiscale observable state belongs to:

`Y_MS = ∏_(ell ∈ L) Y_ell`

This preserves scale separation.

One global scalar is not automatically equivalent to `Y_MS`.

## 14. Aggregate Observable

If a model reduces a multiscale observable state to an aggregate output, it must define an aggregation mapping:

`A_MS: Y_MS → Y_A`

where `Y_A` is the aggregate codomain.

The information loss of `A_MS` must remain explicit.

If `A_MS` is many-to-one, the aggregate value cannot reconstruct the complete multiscale state.

## 15. Observable Sufficiency

An observable family is sufficient for a claim only relative to that claim.

Let `q` denote a declared claim.

Let `Y_q` be the subset or projection of observable outputs required to evaluate `q`.

Observable sufficiency means that the evidence needed by the validation predicate for `q` is recoverable from the available trace and declared model metadata.

There is no universal notion of an observable set being sufficient for every possible claim.

## 16. Observation Index Set

Let:

`K_obs = {0, 1, ..., m}`

be a finite observation index set for a recorded execution with `m ≥ 0`.

The observation index is an ordering index.

It is not automatically physical time.

## 17. Execution Coordinate Domain

Let `D_exec` be the model's execution-coordinate domain.

Depending on the model, `D_exec` may represent:

- continuous time;
- discrete time;
- tact index;
- solver step;
- event index;
- another declared execution coordinate.

The meaning and units of `D_exec` must be explicit.

## 18. Sampling Map

A trace sampling map is:

`S_obs: K_obs → D_exec`

For observation index `k`, the execution coordinate is:

`d_k = S_obs(k)`

The sampling map must preserve ordering when ordered execution is claimed.

For `k_1 < k_2`, an order-preserving trace requires:

`S_obs(k_1) ≤ S_obs(k_2)`

with the appropriate ordering relation on `D_exec`.

## 19. Sampling Resolution

Sampling resolution is a property of the observation process rather than the mathematical dynamics alone.

If the execution contains states between two recorded samples, those states may be absent from a sampled observable trace.

Therefore:

`unobserved intermediate state ≠ nonexistent intermediate state`

and:

`sample adjacency ≠ execution adjacency`

unless the trace contract explicitly establishes that every execution step is represented.

## 20. Trace Record Space

Let `Y_TR` be the combined observable space.

Let `X_Event_0` be the event space augmented with a distinguished no-event record where the model uses such a representation.

Let `Y_Prov` be the declared provenance-record space.

A generic trace record belongs to:

`X_Record = D_exec × Y_TR × X_Event_0 × Y_Prov`

A concrete serialization may use named fields rather than a mathematical tuple.

The mathematical record type and the serialization format remain distinct.

## 21. Trace

Let `X_Trace` denote the set of finite ordered sequences over `X_Record`.

A finite trace is an element:

`tau ∈ X_Trace`

represented as:

`tau = (rho_0, rho_1, ..., rho_m)`

with:

`rho_k ∈ X_Record`

for every `k ∈ K_obs`.

Trace order is semantically significant whenever model behavior depends on execution order, transition order, delay, memory, hysteresis, or event causality.

## 22. Execution Trace

An execution trace records state or state-derived information at the execution boundary needed to reconstruct or validate model behavior.

An execution trace may contain:

- input state;
- scheduler state;
- target state;
- retained state;
- route state;
- model observables;
- counters;
- invariant states;
- event metadata.

An execution trace is not required to expose every internal variable unless the claim being validated requires those variables.

## 23. Observable Trace

An observable trace records values produced by declared observable mappings.

If the observable is memoryless and every source state is available, the trace may be represented pointwise as:

`tau_O = (O_TR(s_k))_(k ∈ K_obs)`

For a history-dependent observable, this pointwise expression is insufficient unless `s_k` contains a sufficient history state.

## 24. Event Trace

An event trace is an ordered sequence of declared semantic events.

For ternary resonance execution, event classes may include:

- target request;
- first-leg neutral transition;
- neutral retention;
- pending-route creation;
- pending-route cancellation;
- pending-route completion;
- branch recovery;
- branch redirection;
- resonance-window entry;
- resonance-window exit;
- regime-transition candidate;
- invariant violation.

These are semantic event classes.

They are not mandatory serialized field names.

## 25. State Trace and Event Trace Are Distinct

A state trace records state values.

An event trace records transitions or classified changes.

The same state value may persist across multiple execution steps without a state-changing event.

Conversely, an event may require both pre-event and post-event state for complete interpretation.

Therefore:

`state trace ≠ event trace`

## 26. Trace Ordering

A valid ordered trace must preserve the declared execution order.

A trace transport, export, transformation, or downstream consumer must not reorder records silently when order affects semantics.

If a transformation intentionally reorders records, it defines a different trace representation and must preserve an explicit relation to the source ordering.

## 27. Causal Ordering Boundary

Temporal or execution ordering is necessary for many causal claims but is not sufficient by itself to prove causality.

A model-defined causal relation requires an explicit dependency such as:

`resonance state`

`→ guard evaluation`

`→ transition authorization`

A trace may verify that this declared ordering occurred.

The trace alone does not create a causal law absent from the model.

## 28. Ternary Target Trace

Let `sigma_k ∈ T` denote the executed ternary state at observation index `k`.

Let `sigma_target,k ∈ T` denote a declared ternary target where such a target exists.

The trace must preserve:

`executed state ≠ target state`

A target of `1` while the executed state is `0` is a valid intermediate condition during an admissible opposite-state route.

## 29. Active Neutral Trace Semantics

The balanced ternary set remains:

`T = {-1, 0, 1}`

State `0` is active.

A trace containing:

`0`

must not interpret that state automatically as:

- missing data;
- invalid data;
- no signal;
- no event;
- passive state;
- failure state.

If missing or invalid data exist, they require a separate representation outside `T`.

## 30. Opposite-State Route Trace

The forbidden direct transitions remain:

`-1 → 1`

and:

`1 → -1`

The admissible opposite-state routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

A trace used to validate an opposite-state route must preserve both executed transition legs as separate events or otherwise provide sufficient execution evidence to reconstruct them separately.

## 31. Hidden Intermediate-State Boundary

Suppose a sampled trace contains consecutive observed values:

`-1, 1`

If the sampling contract does not guarantee execution-step completeness, this pair does not by itself prove that a forbidden direct transition occurred.

A valid intermediate execution may have been:

`-1 → 0 → 1`

between samples.

Likewise, the sampled pair does not prove that neutral mediation occurred.

The result is unresolved unless the required execution resolution or event trace is available.

## 32. Neutral Residence Trace

An active neutral state may persist for any number of admissible execution steps unless a specific model defines a stronger residence constraint.

Therefore a valid trace may contain:

`..., 0, 0, 0, ...`

without implying failure or missing data.

The trace must preserve any model-specific reason for neutral residence when that reason is required by the validation claim.

## 33. Pending Route Trace

If an implementation uses pending opposite-state routes, the trace or replay state must preserve sufficient information to determine:

- source component;
- pending target;
- route creation state;
- eligibility condition;
- completion condition;
- cancellation condition;
- completion or cancellation event.

A pending target is not an executed state.

## 34. Resonance-Coordinate Trace

A resonance-coordinate trace records values:

`r_k ∈ X_R`

or declared projections of those values.

Every recorded coordinate must preserve its:

- coordinate identity;
- domain;
- units or explicit dimensionless status;
- numerical representation;
- parameter provenance;
- validity state.

A malformed required coordinate invalidates any classification that depends on it.

## 35. Resonance-Classification Trace

Let the minimum resonance-classification space be:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`

A classification trace records:

`kappa_R,k ∈ K_R`

according to the declared classifier and window version.

The following mappings remain forbidden unless a particular model explicitly defines them:

`OUTSIDE = -1`

`BOUNDARY = 0`

`INSIDE = 1`

## 36. Resonance-Window Identity

A resonance classification is interpretable only relative to the resonance window used by the classifier.

If the window is parameter-dependent, time-dependent, history-dependent, hysteretic, topology-dependent, or scale-dependent, the trace must preserve or reference the state required to identify the applicable window.

A classification label without window identity may be insufficient evidence.

## 37. Window Versioning

If the numerical or model definition of `W_R` changes across executions, the trace must identify the applicable window definition or version.

Two records labeled `INSIDE` under different window definitions are not automatically equivalent observations.

## 38. History Trace

A history-dependent resonance or transition model must preserve the history state required for reproduction.

The trace may preserve history by:

- explicit history records;
- sufficient retained state;
- deterministic references to earlier records;
- another declared lossless mechanism for the required dependency.

The history mechanism must be explicit.

## 39. Phase Trace

A phase observable belongs to a circular domain.

If `theta_i` denotes a phase, its trace values must preserve the declared circular convention.

An unwrapped numerical representation may be used internally, but the relationship to the circular phase state must remain defined.

## 40. Circular Difference

Two phase values must not be compared as unrestricted real coordinates when the model semantics are circular.

Any phase-difference observable must use the declared circular difference convention inherited from the phase module.

This prevents artificial discontinuities at the representation boundary.

## 41. Phase-Order Trace

For a declared component group `G`, a Kuramoto-style phase-order magnitude is an observable of phase organization.

Its trace records the evolution of that observable.

It does not reconstruct the complete phase configuration of `G`.

Different phase configurations may produce the same phase-order magnitude.

## 42. Phase Order and Coherence Remain Distinct

The distinction established in Chapters 05, 06, and 08 remains mandatory:

`phase order ≠ complete coherence`

and:

`R(t) ≠ C(t)`

A field name containing the word `coherence` does not override the mathematical definition of the value it stores.

Semantic interpretation follows the declared relation, not the identifier alone.

## 43. Synchronization Trace

A synchronization claim requires an observable or relation appropriate to the declared synchronization definition.

A high phase-order value alone does not establish every form of synchronization.

Likewise:

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

The trace must preserve the criteria actually used by the claim.

## 44. Ternary Occupancy Trace

For `N` ternary components, occupancy observables may record counts or fractions of:

- `-1`;
- `0`;
- `1`.

Let `n_-1`, `n_0`, and `n_1` denote the corresponding component counts.

The counts must satisfy:

`n_-1 + n_0 + n_1 = N`

The neutral occupancy is a ternary-state observable.

It is not automatically a resonance-quality or disorder measure.

## 45. Transition-Activity Trace

A transition-activity observable must define what it counts.

Possible definitions include:

- state-changing legs;
- completed opposite-state routes;
- transition requests;
- prevented direct requests;
- neutral-routed events;
- retained-state events.

These event classes are not interchangeable.

## 46. Capacity Trace

If a model limits the number of transitions or requests that may be processed per execution step, capacity is part of the execution semantics.

A capacity trace may include:

- requested work;
- admitted work;
- deferred work;
- pending-route count;
- queue capacity;
- overflow count.

A capacity limit is not a resonance threshold unless a model explicitly defines such a relation.

## 47. Local and Global Trace Separation

A trace must preserve the distinction between local and global channels.

A global average may hide:

- local threshold crossing;
- local neutral residence;
- local route backlog;
- local phase disorder;
- localized perturbation;
- local thermal concentration.

A claim about local behavior requires local evidence or a proven sufficient mapping from the available global evidence.

## 48. Multiscale Trace

A multiscale trace must identify the scale associated with each scale-dependent observable.

For phase-order data, the trace may contain separate channels for:

- pair-domain order;
- cluster order;
- supercluster order;
- global order.

These channels must not be flattened into one scalar when the claim concerns cross-scale organization.

## 49. Cross-Scale Event Trace

A claimed cross-scale regime transition must preserve:

- source scale;
- destination scale;
- event order;
- scale-specific regime definitions;
- mapping between scales;
- causal status.

Temporal ordering across scales is evidence of sequence, not automatically evidence of causality.

## 50. Resonance-Regime Trace

A resonance-regime trace records the declared regime classification over the execution coordinate.

It must identify the classifier and any state required by persistence or hysteresis semantics.

A regime label is not sufficient to establish a bifurcation.

## 51. Bifurcation Evidence Boundary

A trace showing a threshold crossing or regime change may identify a bifurcation candidate.

It does not establish a named bifurcation class without the class-specific mathematical evidence defined in Chapter 07.

Therefore:

`trace-visible regime change ≠ established bifurcation`

## 52. Structural-Transition Evidence Boundary

A ternary or resonance trace does not by itself establish structural transition.

A structural-transition claim requires independently defined structural states and transition criteria.

The trace must contain or reference those structural observables when the claim depends on them.

## 53. Physical Phase-Transition Evidence Boundary

A physical phase-transition claim requires a physical model and evidence appropriate to that model.

Neither:

- oscillator phase;
- phase order;
- resonance classification;
- ternary state;
- scheduler state;

is by itself a physical phase-transition state.

## 54. Model Proxy

A model may expose a proxy observable that is mathematically derived from internal state.

A proxy must identify:

- source state;
- mapping;
- codomain;
- dimensional status;
- interpretation boundary;
- provenance.

A model proxy is not automatically a measured physical quantity.

## 55. Dimensional Status

Every numerical observable must declare whether it is:

- dimensional with specified units;
- dimensionless;
- a coded categorical value;
- a fixed-point encoding of another declared quantity;
- a count or index.

Numerical magnitude alone does not determine dimensional meaning.

## 56. Fixed-Point Representation

If a mathematical quantity `y` is represented by an integer word `q`, the implementation must define the encoding and decoding relation.

The integer word is not identical to the mathematical quantity unless the representation itself defines that identity.

Quantization error belongs to the numerical realization layer.

## 57. Provenance Record

Every claim-relevant observable, parameter, or validation threshold must retain provenance sufficient to identify its evidential status.

The allowed provenance classes inherited from Volume 01 are:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

## 58. Provenance Does Not Collapse into Validation Result

Provenance class and validation result are different objects.

For example:

- an `AUTHOR_DEFINED` rule may pass an internal invariant test;
- a `BENCHMARK` value may be reproducible without being a physical constant;
- a `REQUIRES_TEST` relation may be mathematically well typed while remaining empirically unverified.

Therefore:

`provenance class ≠ validation result`

## 59. Source Binding

A trace intended for reproducible executable evidence should bind to its source realization through sufficient identity information.

Depending on the implementation, this may include:

- repository revision;
- source file identity;
- artifact schema identity;
- parameter set;
- workload identity;
- deterministic seed;
- digest.

The binding mechanism is implementation-specific.

## 60. Derived Observable Binding

A derived observable must preserve the relation by which it was calculated.

Let `Y_1`, `Y_2`, and `Y_3` be declared observable spaces and let:

`F: Y_1 × Y_2 → Y_3`

For `y_1 ∈ Y_1` and `y_2 ∈ Y_2`, define:

`y_3 = F(y_1, y_2)`

Then validation of `y_3` requires both the declared mapping `F` and sufficient source values or equivalent evidence.

A stored derived field does not become self-justifying because it is present in a trace.

## 61. Serialization Is Not Mathematics

JSON, CSV, text vectors, binary words, or another transport format are serialization choices.

They do not redefine:

- the source state space;
- the observable codomain;
- transition legality;
- resonance semantics;
- physical interpretation.

The mathematical contract precedes the transport format.

## 62. Schema Validity

A schema may validate:

- required fields;
- data types;
- allowed values;
- structural shape;
- identifier consistency.

Schema validity does not by itself establish:

- correct dynamics;
- correct physical interpretation;
- invariant preservation;
- empirical validity.

Therefore:

`schema-valid ≠ scientifically validated`

## 63. Missing-Field Semantics

Missing data must remain distinguishable from valid numerical or ternary values.

In particular:

`absent field ≠ 0`

and:

`missing ternary state ≠ active neutral 0`

unless a specific serialization contract explicitly defines another representation without violating the ternary semantics.

## 64. Field Name Is Not Semantic Proof

An implementation identifier is not a mathematical definition.

The semantic meaning of a field is determined by:

- its source mapping;
- its declared codomain;
- its units or dimensionless status;
- its relation to other state variables;
- its validation contract.

A legacy or implementation-oriented field name must not silently override those definitions.

## 65. Trace Identity

Two traces are byte-identical only if their serialized byte sequences are identical under the declared serialization.

Two traces may be semantically equivalent without being byte-identical if a declared semantics-preserving transformation changes representation.

Conversely, byte identity proves reproducibility of the serialized output under the compared conditions, not universal correctness of the model.

## 66. Digest

A cryptographic digest may bind an artifact to exact bytes.

A digest match establishes byte identity with the referenced artifact under the digest algorithm.

It does not establish:

- physical validity;
- mathematical correctness;
- causal validity;
- semantic equivalence to a differently encoded artifact.

## 67. Deterministic Replay

A deterministic replay relation compares executions initialized with the same complete result-affecting state and execution conditions.

A complete replay contract must identify every state component that can affect the result.

Depending on the model, this includes:

- initial dynamic state;
- resonance state;
- ternary state;
- target state;
- pending routes;
- scheduler state;
- coupling state;
- phase state;
- frequency-memory state;
- gamma state;
- thermal state;
- parameter state;
- topology;
- pseudorandom state;
- input sequence;
- numerical configuration.

## 68. Replay Equivalence Relation

Let `tau_1, tau_2 ∈ X_Trace` be two traces produced under a declared replay contract.

A replay-equivalence relation `~_R` is defined on:

`X_Trace × X_Trace`

The statement:

`tau_1 ~_R tau_2`

must use a declared equivalence criterion.

Possible comparison rules include:

- exact byte identity;
- exact field equality;
- equality after canonical serialization;
- numerical equality within declared tolerances for selected continuous fields.

The comparison rule must be declared before the result is interpreted.

## 69. Determinism Is Not Correctness

A deterministic implementation can reproduce an incorrect model.

Therefore:

`deterministic replay ≠ model correctness`

and:

`deterministic replay ≠ physical validation`

Deterministic replay establishes reproducibility under the declared execution contract.

## 70. Exact Validation

Exact validation is required for discrete semantic invariants where approximation is not part of the model.

Examples include:

- ternary membership in `{-1,0,1}`;
- prohibition of direct opposite transitions;
- route ordering;
- finite-set classification labels;
- queue-capacity inequality when integer-exact;
- required field identity;
- exact scheduler-state encoding where specified.

A numerical tolerance must not turn an illegal discrete state into a legal one.

## 71. Numerical Validation

For a numerical claim comparing real-valued or quantized approximations, the model may define a tolerance:

`epsilon_val ≥ 0`

For two declared scalar values `a` and `b` in dimensionally compatible spaces, a comparison may use:

`|a - b| ≤ epsilon_val`

only when the tolerance has matching units or dimensionless status.

The tolerance must retain provenance.

## 72. Exact Boundary and Numerical Boundary Layer

The exact resonance boundary remains:

`∂W_R`

A numerical implementation may use a finite tolerance around that boundary.

The two objects remain distinct:

`exact boundary ≠ numerical boundary tolerance`

A trace must identify which classification rule generated a boundary result.

## 73. Circular Numerical Comparison

Phase comparison must respect circular topology.

A numerical phase comparator must use a declared circular distance or an equivalent periodic relation rather than unrestricted real subtraction alone.

The tolerance belongs to the numerical comparator, not to the definition of phase itself.

## 74. Validation Result Space

Define the author-defined validation-result space:

`X_Val = {PASS, FAIL, UNRESOLVED}`

These labels describe evaluation status.

They are not balanced ternary states.

Therefore:

`FAIL ≠ -1`

`UNRESOLVED ≠ 0`

`PASS ≠ 1`

## 75. Claim-Scoped Validator

Let `q` be a declared claim.

Let `E_q` be the evidence space required to evaluate that claim.

A validator is typed as:

`V_q: E_q → X_Val`

The validator must specify the evidence it consumes and the rule that produces its result.

A global `PASS` without a defined claim and evidence scope is not a mathematically complete validation statement.

## 76. Unresolved Result

`UNRESOLVED` means that the available evidence is insufficient to establish either `PASS` or `FAIL` under the declared validator.

It may result from:

- insufficient trace resolution;
- missing required state;
- missing provenance;
- incompatible units;
- unavailable history;
- ambiguous window identity;
- absent empirical calibration;
- unsupported physical interpretation.

`UNRESOLVED` must not be converted to active neutral `0`.

## 77. Claim-Relative Trace Completeness

Define a claim-relative completeness predicate:

`Complete_q: X_Trace → {true, false}`

A trace `tau ∈ X_Trace` is complete for claim `q` when `Complete_q(tau) = true`, meaning that the trace contains or losslessly references every evidence item required by `V_q`.

Trace completeness is therefore claim-relative.

A trace may be complete for ternary transition legality while incomplete for physical phase-transition validation.

## 78. Evidence Sufficiency

Evidence sufficiency requires more than field presence.

For claim `q`, evidence must satisfy the declared requirements for:

- semantic identity;
- domain validity;
- ordering;
- resolution;
- provenance;
- parameter identity;
- units;
- history;
- numerical tolerance where applicable.

## 79. Syntactic Validation

Syntactic validation checks representation-level correctness such as:

- parseability;
- required keys;
- allowed data types;
- structural constraints;
- encoding constraints.

It is a necessary layer for structured interchange when the schema requires it.

It is not sufficient for semantic validation.

## 80. Type Validation

Type validation checks whether every recorded value belongs to its declared mathematical or encoded domain.

Examples include:

- valid ternary state code;
- valid scheduler state;
- valid resonance-classification label;
- finite numeric range;
- declared scale index;
- declared component identity.

## 81. Invariant Validation

Invariant validation checks model invariants against the trace or execution state.

For the ternary kernel, required checks include:

- every executed state belongs to `{-1,0,1}`;
- `0` remains valid and active;
- no executed `-1 → 1` event exists;
- no executed `1 → -1` event exists;
- opposite routes preserve separate neutral-mediated legs;
- target state remains distinct from executed state.

## 82. Temporal Validation

Temporal validation checks ordering-dependent claims.

Examples include:

- target request precedes the transition it authorizes;
- first leg precedes second-leg completion;
- pending route exists before completion;
- window entry precedes residence;
- history state used by a classifier belongs to the applicable history interval.

## 83. Replay Validation

Replay validation checks whether the declared replay-equivalence relation holds across repeated executions.

It must identify:

- initial conditions;
- input sequence;
- parameter state;
- comparison rule;
- compared outputs.

Replay validation establishes reproducibility within that contract.

## 84. Cross-Realization Validation

When two implementations claim to realize the same semantics, a cross-realization validator must compare declared common interfaces.

The validator must distinguish:

- mathematical equivalence;
- encoded-value equivalence;
- event-sequence equivalence;
- tolerance-based numerical agreement;
- timing or cycle equivalence.

Agreement in one dimension does not establish all others automatically.

## 85. Benchmark Validation

A benchmark result belongs to the declared benchmark conditions.

It must preserve:

- workload identity;
- implementation identity;
- parameter state;
- measurement method;
- metric definition;
- hardware or software environment where relevant.

A benchmark value is not a universal physical or architectural constant.

## 86. Empirical Validation

Empirical validation requires comparison with independently obtained physical or experimental data under a declared measurement protocol.

The validation contract must define:

- measured quantity;
- measurement units;
- calibration state;
- uncertainty;
- model-to-measurement mapping;
- acceptance criterion.

Executable internal telemetry alone does not satisfy this requirement.

## 87. Calibration

Calibration is a mapping from model parameter or observable space to an independently defined reference or measurement relation.

A calibrated parameter must retain:

- calibration data identity;
- calibration procedure;
- fitted or selected parameter identity;
- uncertainty or applicable range;
- provenance class `CALIBRATED`.

A hard-coded implementation parameter is not calibrated merely because it produces stable execution.

## 88. Validation Promotion Is Forbidden

Evidence must not be silently promoted across validation classes.

In particular:

`schema PASS`

`≠ invariant PASS`

`≠ deterministic replay PASS`

`≠ benchmark superiority`

`≠ empirical validation`

`≠ universal physical law`

Each claim requires its own evidence boundary.

## 89. Failure-State Separation

Validation failure is not a valid model state unless a model explicitly defines a separate failure-state space.

Therefore:

`FAIL ≠ ternary -1`

`FAIL ≠ ternary 0`

`FAIL ≠ resonance OUTSIDE`

`FAIL ≠ low phase order`

Validation status must remain outside the modeled state domains it evaluates.

## 90. FRP Executable Reference Boundary

The current FRP repository supplies a concrete executable specialization for several trace and validation concepts in this chapter.

The reference is used to establish that specific mechanisms are executable and machine-observable.

It does not redefine the general TR-EIF mathematical layer.

The following sections describe only mechanisms verified in the current FRP code and generated artifact structure.

## 91. FRP Floating and Quantized Reference Traces

The current FRP semantic reference file:

`frp_prototype_v1_7_0.py`

contains both the floating processor realization and the quantized reference-shadow realization.

The quantized class:

`QuantizedReferenceShadowProcessor`

records tact-by-tact execution through its `tick` method and appends records to an ordered trace.

This is an executable implementation of a discrete observation map over the processor state.

## 92. FRP Tick-Level Trace Record

The current quantized reference tick record includes implementation fields for:

- tick index;
- reset state;
- scheduler mode;
- scheduler state;
- automatic-target enable state;
- request-valid mask;
- requested cell identifiers;
- requested target-state encodings;
- gamma-noise update state;
- packed ternary states;
- human-readable ternary states;
- pending-route count;
- switching-load proxy;
- global model heat proxy;
- quantized global phase-order field;
- processor-specific `C` quantity;
- processor-specific `P` quantity;
- `C - P` margin;
- requested direct events;
- prevented direct events;
- neutral-routed events;
- neutralized conflicts;
- actual direct events;
- reserved-state events;
- queue-overflow events;
- number of executed changes.

These are FRP implementation fields.

They are not a mandatory universal TR-EIF trace schema.

## 93. FRP Per-Cell Trace

The current quantized reference also records a per-cell trace containing implementation fields for:

- tick index;
- cell identifier;
- encoded ternary state;
- phase word;
- frequency target;
- retained current frequency;
- frequency lag;
- generated power proxy;
- local model heat state;
- thermal-overload proxy;
- gamma-noise state;
- effective gamma word;
- thermal node factor;
- hierarchical coupling field.

This per-cell trace preserves local information that cannot be reconstructed generally from one global scalar trace.

## 94. FRP Phase-Order Field Semantics

The executable tick field named:

`global_phase_coherence_q30`

is produced from the FRP multiscale phase-order calculation.

The current M27 telemetry semantics explicitly describes this field as a quantized global phase-order metric.

Therefore its mathematical interpretation remains:

`global phase-order observable`

rather than:

`complete structural coherence`

The identifier does not collapse the distinction:

`R(t) ≠ C(t)`

## 95. FRP Processor-Specific C and P Fields

The FRP trace contains processor-specific fields corresponding to:

`C_q16`

`P_q16`

and:

`C_minus_P_q16`

The M27 telemetry semantics describes corresponding derived quantities as model-derived, dimensionless processor proxies and margins.

They remain implementation observables.

They are not universal physical coherence, pressure, energy, or force variables.

## 96. FRP Target and Executed State Boundary

The FRP reference distinguishes phase-derived target generation from retained executed state.

An opposite-polarity target does not authorize a direct executed state change.

The downstream execution preserves:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

with pending-route state between legs where required.

A correct trace analysis must therefore distinguish requested target, active neutral state, pending route, and executed destination.

## 97. FRP Safety and Integrity Counters

The current FRP reference exposes counters including:

`actual_direct_events`

`reserved_state_events`

`queue_overflow_events`

These counters are implementation-level invariant observables.

A zero value is meaningful only because each counter has an independently declared event definition.

The number `0` in these counters is not the balanced ternary neutral state.

## 98. FRP M27 Telemetry Semantics

The current FRP file:

`frp_m27_long_run_stability_telemetry_qualification.py`

constructs a telemetry-semantics artifact through:

`build_telemetry_semantics`

The generated telemetry contract explicitly declares its published telemetry as:

- model-derived;
- dimensionless;
- not published physical measurements;
- not published physical units.

This is the correct interpretation boundary for those fields.

## 99. FRP M27 Derived Relations

The M27 telemetry semantics validates implementation relations including:

`transition pressure proxy = thermal state proxy + switching load proxy`

and:

`stability margin = coherence-capacity proxy - transition-pressure proxy`

These are FRP model relations.

They do not establish universal physical laws.

## 100. FRP M27 Long-Run Evidence

The current M27 long-run qualification records:

- workload identity;
- scheduler mode;
- checkpoint count;
- safety counters;
- pending-route bounds;
- transition-capacity bounds;
- deterministic checkpoint digests;
- final chain digest;
- deterministic rerun requirements.

The report explicitly classifies this evidence as deterministic model evidence rather than physical measurement evidence.

This distinction is part of the executable evidence boundary.

## 101. FRP M28 Observatory Interchange

The current FRP file:

`frp_m28_trace_observatory_upstream_interchange.py`

constructs an upstream trace interchange for the downstream FRP Trace Observatory.

The current canonical bundle combines declared source datasets from:

- M16 RTL execution traces;
- M16 FPGA-preparation execution traces;
- M27 long-run checkpoint evidence.

The source record ordering is preserved in the generated bundle.

## 102. FRP M28 Immutable Core Semantics

The M28 interchange contract explicitly preserves:

- balanced ternary notation `-1/0/1`;
- semantic values `[-1, 0, 1]`;
- active neutral state `0`;
- opposite transition routes `[-1, 0, 1]` and `[1, 0, -1]`;
- scheduler modes used by the reference artifacts.

These semantics are transported as implementation contract data rather than inferred downstream.

## 103. FRP M28 Missing-Field Policy

The current M28 interchange contract specifies:

`missing_field_policy = remain_absent`

and:

`absent_is_zero = false`

This executable rule is consistent with the TR-EIF requirement that missing data must not be converted silently into active neutral `0` or another valid zero-valued observable.

## 104. FRP M28 Source Authority

The current M28 interchange direction is upstream-to-downstream.

The FRP source remains the semantic authority for the exported FRP artifacts, while downstream source mutation and writeback are forbidden by the interchange contract.

This establishes a concrete producer-consumer boundary.

It does not make the Observatory an authority over the general TR-EIF mathematical theory.

## 105. FRP M28 Digest and Ordering Semantics

The M28 interchange uses SHA-256 digests for source-byte identity and preserves source order.

These mechanisms support:

- artifact identity;
- trace-order integrity;
- reproducible downstream consumption.

They do not independently establish physical or mathematical validity of the represented model.

## 106. FRP Measurement Contours Remain Separate

The M28 interchange contract explicitly preserves separate measurement contours across its source datasets.

This is important because RTL execution trace, FPGA-preparation execution trace, and long-run checkpoint evidence are different observation layers.

Combining them into one transport bundle does not make them one identical measurement process.

## 107. What the FRP Trace Reference Establishes

The current FRP executable reference establishes that a concrete architecture can implement:

- ordered tact-level traces;
- local and global observables;
- explicit scheduler-state telemetry;
- active-neutral ternary execution;
- pending-route observability;
- transition-capacity observability;
- invariant counters;
- deterministic checkpoint evidence;
- fixed-point model telemetry;
- versioned machine-readable interchange;
- source-order preservation;
- digest-based artifact identity.

These are executable facts of the reference realization.

## 108. What the FRP Trace Reference Does Not Establish

The FRP trace reference does not by itself establish:

- universal resonance coordinates;
- universal resonance thresholds;
- universal physical constants;
- universal interatomic mechanisms;
- chemical bonding;
- generic mechanical force laws;
- thermodynamic phase-transition identity;
- empirical calibration to an arbitrary material system;
- equivariance of an interatomic representation.

Those claims require separate formal or empirical evidence.

## 109. TR Output Channel Space

The TR layer must expose its results through typed channels rather than through an untyped scalar interface.

Let `I_TR,out` be the finite index set of output channels selected by a particular TR model.

For each channel `a ∈ I_TR,out`, let `Y_a` be its declared codomain.

Define:

`Y_TR,out = ∏_(a ∈ I_TR,out) Y_a`

The TR output mapping is:

`O_TR,out: S_TR → Y_TR,out`

or, for history-dependent outputs:

`O_TR,out,H: H_TR → Y_TR,out`

## 110. Admissible TR Output Families

Depending on the model, `Y_TR,out` may include typed channels for:

- resonance coordinates;
- resonance classification;
- phase organization;
- synchronization descriptors;
- coherence descriptors;
- ternary target;
- executed ternary state;
- pending route state;
- transition events;
- regime state;
- multiscale descriptors;
- validation status;
- provenance references.

The presence of a channel must be explicit.

No output channel acquires an interatomic physical meaning merely by being present in the TR output space.

## 111. TR Output Is Not EIF State

Let `S_EIF` denote the state space that will be defined independently by the later EIF formalism.

The TR output space and the EIF state space are different typed objects.

Therefore:

`Y_TR,out ≠ S_EIF`

in general.

An explicit integration mapping is required before TR observables can update or condition an EIF state.

## 112. EIF Input Boundary

The later EIF layer must define the source interatomic state, symmetry actions, local environments, topology, and equivariant or invariant representations independently.

Only after those objects are defined may an integration layer construct a mapping into the TR state or resonance spaces.

The present chapter does not assign oscillator phase, resonance coordinate, or ternary polarity directly to an atom without such a mapping.

## 113. Required EIF-to-TR Integration Mapping

A later integrated model requires an explicit typed relation of the form:

`interatomic state`

`→ equivariant representation`

`→ TR source state`

`→ resonance coordinate`

`→ resonance classification`

`→ ternary target`

`→ admissible -1/0/1 execution`

The precise domain, codomain, symmetry action, locality, and information loss of every mapping must be defined in the EIF and integration layers.

## 114. Required TR-to-EIF Feedback Mapping

If TR state feeds back into the interatomic representation, a separate mapping is required.

Abstractly, a later integration layer may define a typed map from:

`TR output state × EIF state`

into:

`updated EIF state`

The transformation behavior of that map must be proven or tested according to the declared symmetry semantics.

No such feedback is implied by the existence of a ternary or resonance observable alone.

## 115. No Direct Force Substitution

A TR observable is not automatically a force.

In particular:

`phase relation ≠ mechanical force`

`resonance classification ≠ force`

`ternary state ≠ force`

Any force interface requires an independently defined mapping with the appropriate transformation behavior and physical dimensions.

## 116. No Direct Energy Substitution

A TR observable is not automatically an energy.

In particular:

`ternary state ≠ energy`

`resonance classification ≠ energy`

Any energy interface must be independently defined and dimensionally valid.

## 117. No Direct Bond Substitution

A trace showing resonance, phase locking, synchronization, or persistent ternary state does not automatically establish a chemical bond.

A bond or interatomic interaction relation requires its own definition in the EIF or physical model.

## 118. Equivariance Boundary for Observables

An observable is invariant or equivariant only relative to declared transformation actions.

Let `G` be a declared transformation group or transformation set.

Let:

`rho_S(g): S_TR → S_TR`

be the input action and:

`rho_Y(g): Y_O → Y_O`

be the output action for `g ∈ G`.

An observable `O: S_TR → Y_O` is equivariant when:

`O(rho_S(g)(s)) = rho_Y(g)(O(s))`

for every admissible `g` and `s`.

If `rho_Y(g)` is the identity action, the observable is invariant under the declared transformation.

The actions must be defined rather than inferred from terminology.

## 119. Trace Equivariance Boundary

If an observable is equivariant, a trace transformation must also preserve:

- component identity under the transformation;
- record ordering;
- scale identity;
- event correspondence;
- provenance correspondence.

Equivariance of individual values does not automatically establish equivariance of an ordered event trace when transformation changes indexing or topology.

## 120. Permutation Boundary

Permutation invariance and permutation equivariance remain distinct.

A relabeling of components may preserve a scalar aggregate while transforming component-indexed outputs.

Therefore:

`permutation-invariant aggregate ≠ permutation-equivariant local trace`

The later EIF layer must specify the permutation action for atomic or local-environment representations.

## 121. Geometry and Ternary Polarity

Translation, rotation, or permutation of geometry does not automatically change ternary polarity.

A transformation of:

`-1/0/1`

requires an explicitly declared action on the ternary state space.

No geometric transformation is allowed to flip ternary state by implication alone.

## 122. Validation of Equivariance Claims

A validation claim for equivariance must identify:

- transformation set `G`;
- input action `rho_S`;
- output action `rho_Y`;
- tested or proven domain;
- comparison relation;
- numerical tolerance where applicable.

A single unchanged scalar output is insufficient to establish a broader equivariance claim.

## 123. Traceability Chain

Every important observable or validation claim must support the chain:

`claim`

`→ definition / source / calculation`

`→ scope`

`→ observable or state evidence`

`→ trace identity`

`→ validation rule`

`→ validation result`

For FRP executable-reference claims, the chain additionally includes:

`TR-EIF concept`

`→ FRP file / function / artifact`

`→ implemented field or state`

`→ established scope`

`→ non-established scope`

## 124. Minimal Observable Contract

A TR-EIF observable contract must define:

- source state space;
- observable mapping;
- codomain;
- local, global, or scale scope;
- dimensional status;
- history dependence where applicable;
- aggregation rule where applicable;
- provenance;
- invalid-data behavior.

## 125. Minimal Trace Contract

A TR-EIF trace contract must define:

- observation index set;
- execution-coordinate domain;
- sampling map;
- record order;
- included observable channels;
- event representation;
- target/executed-state distinction where applicable;
- active-neutral representation;
- missing-data representation;
- provenance binding;
- serialization identity where machine-readable interchange is claimed.

## 126. Minimal Ternary Trace Contract

A trace used to validate ternary execution must additionally preserve sufficient evidence for:

- state membership in `{-1,0,1}`;
- active neutral state;
- executed-state sequence;
- target-state sequence where targets are used;
- opposite-route first leg;
- neutral residence where present;
- pending-route state where present;
- second-leg completion;
- route cancellation or redirection where present;
- transition capacity where relevant.

## 127. Minimal Resonance Trace Contract

A trace used to validate resonance claims must preserve sufficient evidence for:

- resonance-coordinate identity;
- resonance-space identity;
- resonance-window identity;
- classification rule;
- boundary semantics;
- history state where required;
- scale identity where required;
- parameter provenance;
- numerical boundary tolerance where used.

## 128. Minimal Multiscale Trace Contract

A multiscale trace must additionally define:

- scale set;
- group or partition identity;
- group membership;
- scale-specific observable spaces;
- aggregation mappings;
- cross-scale correspondence;
- local-to-global information loss;
- cross-scale event semantics where claimed.

## 129. Minimal Validation Contract

A validation contract must define:

- claim `q`;
- evidence space `E_q`;
- validator `V_q`;
- result space `X_Val`;
- exact invariants;
- numerical tolerances where applicable;
- unresolved conditions;
- provenance requirements;
- replay requirements where applicable;
- empirical requirements where applicable.

## 130. Minimal FRP Trace Reference Contract

A model claiming compatibility with the current FRP trace specialization must preserve the relevant implemented semantics it claims to reproduce, including where applicable:

- ordered tact-level trace records;
- scheduler state;
- ternary target/executed-state separation;
- active-neutral routing;
- pending-route count or equivalent route state;
- transition-capacity semantics;
- local phase and retained-frequency state where compared;
- phase-order observable semantics;
- processor-specific `C`, `P`, and margin semantics where compared;
- invariant counters;
- fixed-point encoding contracts;
- deterministic replay state;
- source-order preservation for exported datasets;
- missing-field-not-zero semantics;
- artifact identity and digest semantics.

A partial consumer may implement a declared subset.

It must not claim full compatibility with omitted semantics.

## 131. Core Observable and Trace Invariants

The following invariants are mandatory.

1. State and observable remain separately typed.

2. Observable codomains are declared.

3. History-dependent observables identify required history state.

4. Local and global observables remain distinct.

5. Multiscale observables retain scale identity.

6. Aggregation does not imply invertibility.

7. Trace order is preserved when order affects semantics.

8. Sample adjacency does not imply execution adjacency unless the sampling contract establishes it.

9. Target state remains distinct from executed state.

10. The balanced ternary domain remains exactly `{-1,0,1}`.

11. Canonical ternary notation remains `-1/0/1`.

12. State `0` remains active.

13. Missing data are not encoded silently as ternary `0`.

14. Direct `-1 → 1` remains forbidden.

15. Direct `1 → -1` remains forbidden.

16. Opposite-state routes preserve separate neutral-mediated legs.

17. Neutral residence may persist.

18. Pending target is not executed state.

19. Resonance classification remains distinct from ternary state.

20. `OUTSIDE`, `BOUNDARY`, and `INSIDE` do not map automatically to `-1/0/1`.

21. Phase order remains distinct from complete coherence.

22. `R(t) ≠ C(t)` remains mandatory.

23. Resonance remains distinct from synchronization and phase locking.

24. Resonance-window crossing remains distinct from bifurcation.

25. Bifurcation remains distinct from ternary transition.

26. Ternary transition remains distinct from structural transition.

27. Structural transition remains distinct from physical phase transition.

28. Schema validity remains distinct from semantic validation.

29. Deterministic replay remains distinct from physical validation.

30. Digest identity remains distinct from scientific validity.

31. Validation status remains outside the ternary state domain.

32. Provenance class remains distinct from validation result.

33. Numerical tolerance remains distinct from exact mathematical semantics.

34. FRP implementation fields remain implementation-specific unless independently generalized.

35. FRP telemetry proxies remain distinct from physical measurements unless calibrated independently.

36. TR output remains distinct from EIF state until an explicit integration mapping is defined.

37. Equivariance claims require declared transformation actions.

38. Geometry transformation does not automatically flip ternary polarity.

39. Resonance state does not automatically define force, energy, or chemical bond.

40. Every validated claim retains a traceable evidence boundary.

## 132. Formal Non-Equivalences

The following non-equivalences are mandatory:

`state ≠ observable`

`observable ≠ complete state`

`local observable ≠ global observable`

`global scalar ≠ multiscale state`

`state trace ≠ event trace`

`sample adjacency ≠ execution adjacency`

`target state ≠ executed state`

`pending target ≠ executed state`

`state 0 ≠ missing data`

`state 0 ≠ invalid data`

`validation UNRESOLVED ≠ ternary 0`

`resonance classification ≠ ternary classification`

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`schema PASS ≠ semantic PASS`

`semantic PASS ≠ empirical validation`

`deterministic replay ≠ correctness`

`deterministic replay ≠ physical validation`

`byte identity ≠ universal validity`

`digest match ≠ physical validation`

`field name ≠ mathematical definition`

`model proxy ≠ physical measurement`

`fixed-point word ≠ physical quantity`

`provenance class ≠ validation result`

`TR output ≠ EIF state`

`hierarchy ≠ equivariance`

`phase relation ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ force`

`ternary state ≠ energy`

`resonance classification ≠ energy`

## 133. Formal Observable Dependency Chain

The TR-EIF observable chain is:

`complete TR state`

`→ declared observable family`

`→ local / global / multiscale observable state`

`→ ordered sampling`

`→ state / observable / event trace`

`→ provenance binding`

`→ claim-relative evidence selection`

`→ exact and/or numerical validation`

`→ PASS / FAIL / UNRESOLVED`

The validation result does not feed back into the balanced ternary state unless a separate model explicitly defines such a control relation.

## 134. Formal TR-to-EIF Boundary Chain

The TR layer terminates at a typed output boundary:

`TR dynamic state`

`→ resonance coordinates`

`→ resonance classification`

`→ ternary target`

`→ active-neutral -1/0/1 execution`

`→ multiscale TR state`

`→ observable / trace / validation output`

The later integration chain is separately defined as:

`interatomic state`

`→ equivariant representation`

`→ explicit EIF-to-TR mapping`

`→ TR state and execution`

`→ explicit TR-to-EIF feedback mapping where used`

This separation preserves the full identity of TR-EIF without collapsing TR and EIF into one undeclared state space.

## 135. Conformance Requirements

A mathematical model conforms to this chapter when:

- every observable has a declared source space and codomain;
- history-dependent observables identify their history state;
- local, global, and multiscale channels remain distinguishable;
- sampling semantics are explicit;
- trace ordering is explicit;
- target and executed ternary states remain distinct;
- active neutral `0` remains valid and explicit;
- missing or invalid data remain outside the ternary domain;
- resonance classification remains distinct from ternary classification;
- phase order remains distinct from complete coherence;
- validation predicates are claim-scoped;
- exact and numerical validation are separated;
- provenance remains attached to claim-relevant parameters and observables;
- unsupported physical interpretation is not inferred from model telemetry;
- equivariance claims define transformation actions;
- TR output remains separate from EIF state until explicit mappings are defined.

A computational realization conforms when:

- its trace order is reproducible;
- its state and event encodings are deterministic under the declared execution contract;
- opposite ternary routes remain neutral-mediated;
- required intermediate route evidence is recoverable;
- missing fields are not silently converted to valid zero-valued states;
- numerical tolerances are declared;
- deterministic replay dependencies are preserved;
- validation output distinguishes failure from unresolved evidence;
- machine-readable schema validation does not substitute for semantic or empirical validation;
- executable-reference claims identify their implementation scope.

## 136. Final Observable, Trace, and Validation Statement

TR-EIF does not treat observability as a substitute for mathematical state.

The formal relation is:

`state`

`→ observable`

`→ trace`

`→ evidence`

`→ validation`

with every stage separately typed.

For the ternary resonance layer, the execution invariants remain:

`-1/0/1`

with active:

`0`

and mandatory opposite-state routes:

`-1 → 0 → 1`

`1 → 0 → -1`

A valid trace must preserve enough execution semantics to test those invariants without confusing target state, executed state, missing data, or sampling gaps.

The FRP executable reference demonstrates one concrete realization of this boundary through tact-level and per-cell traces, deterministic long-run evidence, invariant counters, fixed-point model telemetry, versioned trace interchange, preserved source ordering, and digest-bound artifacts.

Those executable facts remain implementation evidence rather than universal physical law.

The terminal output of the TR layer is therefore a typed, provenance-bearing, validation-aware state interface.

It is not yet an interatomic energy, force, bond, or equivariant representation.

Those objects belong to the separately formalized EIF layer and to the later explicit integration mappings connecting:

`interatomic state`

`→ equivariant representation`

`→ resonant state`

`→ ternary state`

and, where defined:

`ternary / resonant state`

`→ equivariant interatomic update`

This boundary completes the observable and validation semantics required for the Ternary Resonant layer while preserving TR-EIF as an integrated mathematical and computational architecture rather than reducing it to any single constituent module.
