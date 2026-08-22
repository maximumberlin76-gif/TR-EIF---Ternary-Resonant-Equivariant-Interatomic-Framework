# Ternary Resonance System Closure and EIF Interface Contract

## 1. Purpose

This document defines the system-closure contract of the Ternary Resonant layer of TR-EIF and the typed boundary through which that layer can participate in the complete Ternary Resonant Equivariant Interatomic Framework.

The chapter formalizes:

- the minimum complete TR system contract;
- admissible input, state, history, parameter, transformation, observable, and validation boundaries;
- composition of resonance dynamics with balanced ternary execution;
- separation of target generation from executed state;
- memory, delay, coupling, dissipation, topology, and multiscale requirements;
- separation of resonance, synchronization, phase locking, coherence, bifurcation, ternary transition, structural transition, and physical phase transition;
- the implementation-specialization boundary;
- the executable FRP specialization boundary;
- the typed EIF-to-TR and TR-to-EIF integration interfaces;
- the symmetry information required before an interatomic mapping may be called invariant or equivariant;
- the conditions under which the Ternary Resonant theory is internally closed as a framework layer without being confused with a physically closed system.

This chapter does not define the EIF mathematical theory itself. It defines the interface contract that prevents the TR and EIF layers from being merged by implication.

## 2. Dependency

This chapter depends on the committed mathematical definitions of Volume 01 and on Chapters 01–09 of Volume 02.

It inherits without redefinition:

- the system-modeling order from Volume 01;
- typed domains, codomains, mappings, relations, and invariants from Volume 01;
- provenance classes from Volume 01;
- resonance-coordinate space `X_R`;
- resonance-coordinate mapping `P_R`;
- admissible resonance domain `X_R,adm`;
- resonance window `W_R` and boundary `∂W_R`;
- canonical resonance-classification set `R_C = {OUTSIDE, BOUNDARY, INSIDE}`;
- canonical resonance classifier `C_R`;
- balanced ternary state set `T = {-1, 0, 1}`;
- active neutral semantics;
- ternary target and executed-state separation;
- neutral-mediated opposite-state transition semantics;
- coupling, synchronization, phase-locking, coherence, and phase-order distinctions;
- the Kuramoto–Sakaguchi module as one optional classical phase module rather than the whole framework;
- resonance-regime and bifurcation boundaries;
- multiscale and hierarchical resonance semantics;
- observable, trace, provenance, replay, and validation semantics from Chapter 09.

## 3. Scientific Status Classes

The objects in this chapter are separated by scientific status.

### 3.1 GENERAL MATHEMATICAL STRUCTURE

Typed state spaces, mappings, relations, product spaces, transformation actions, invariance, equivariance, and composition use general mathematical structure.

### 3.2 TR-EIF FORMAL / AUTHOR-DEFINED

The system-closure contract, active-neutral execution constraints, TR layer boundary, TR-to-EIF interface requirements, and integration admissibility rules are author-defined TR-EIF semantics.

### 3.3 FRP EXECUTABLE REFERENCE

The current FRP code provides one executable specialization of several TR execution semantics. FRP is used only where the implementation mechanism is directly verified in the current repository code.

### 3.4 EMPIRICAL / CALIBRATED

Any mapping from TR-EIF state to measured physical quantities requires independent empirical definition and calibration. No internal executable parameter becomes a universal physical constant through implementation alone.

### 3.5 UNVERIFIED

A physical, interatomic, symmetry, force, energy, bonding, or phase-transition claim remains unresolved when its required mapping, evidence, or validation relation has not been independently established.

## 4. Meaning of System Closure

In this chapter, `system closure` means closure of the formal specification boundary of the Ternary Resonant layer.

It does not mean:

- topological closure of a set;
- thermodynamic isolation;
- absence of external forcing;
- absence of dissipation;
- absence of input or output;
- convergence to an attractor;
- completion of the full EIF theory;
- completion of every physical specialization.

A TR model may remain nonlinear, driven, dissipative, delayed, history-dependent, open, multiscale, or hybrid while satisfying this system-closure contract.

## 5. TR Layer Identity

The complete project identity remains:

`TR-EIF = Ternary Resonant Equivariant Interatomic Framework`

with:

`TR = Ternary Resonant`

and:

`EIF = Equivariant Interatomic Framework`

The Ternary Resonant layer supplies a mathematical and computational state-transformation layer.

It is not by itself the complete TR-EIF architecture.

## 6. TR System Boundary

A conforming TR model must declare a system boundary before declaring its dynamics.

The boundary must identify:

- modeled entities or components;
- external inputs;
- internal state;
- retained history state where required;
- model parameters;
- topology or interaction structure where required;
- observable outputs;
- excluded physical interpretations;
- execution or evolution domain.

No equation becomes a complete TR model merely because it contains a resonance-like or oscillator-like term.

## 7. Input Space

Let `X_TR,in` denote the declared input space of a particular TR model.

An input value satisfies:

`x_in ∈ X_TR,in`

The meaning of `X_TR,in` is specialization-dependent.

It may contain external forcing, boundary conditions, encoded source features, control inputs, topology updates, or another declared input object.

An atomic configuration is not automatically an element of `X_TR,in` unless an explicit mapping establishes that relation.

## 8. Parameter Space

Let `Λ_TR` denote the declared parameter space of the TR model.

A parameter state satisfies:

`λ ∈ Λ_TR`

The parameter space must distinguish:

- mathematical parameters;
- implementation parameters;
- calibrated parameters;
- benchmark parameters;
- test-fixture parameters.

Their provenance must be preserved according to Volume 01.

## 9. State Space

Let `S_TR` denote the declared instantaneous state space of the TR model.

A state satisfies:

`s ∈ S_TR`

The state space must separate all state components whose independent evolution affects future model behavior.

A scalar resonance classification is not a substitute for the complete state when additional continuous, ternary, memory, coupling, topology, or multiscale state is dynamically active.

## 10. History-State Space

Let `H_TR` denote the declared history-state space when the model is history-dependent.

A history state satisfies:

`h ∈ H_TR`

The history state may contain retained variables, delayed values, pending routes, hysteresis state, previous classifications, filtered state, or other explicitly declared memory.

A history-dependent model must not be represented as memoryless by omission.

## 11. Execution-Coordinate Domain

Let `D_exec` denote the declared execution-coordinate domain.

Depending on the model, `D_exec` may represent:

- continuous time;
- discrete time;
- tact index;
- solver step;
- event index;
- another explicitly declared ordered coordinate.

The execution coordinate must not be called physical time unless that interpretation is independently defined.

## 12. Evolution Contract

The TR layer does not impose one universal evolution equation.

A model must instead declare an evolution contract appropriate to its system class.

Admissible forms include:

- continuous evolution;
- discrete evolution;
- hybrid continuous-discrete evolution;
- delayed evolution;
- history-dependent evolution;
- event-driven evolution;
- multiscale coupled evolution.

The domain and codomain of every evolution operator or relation must be explicit.

## 13. Continuous Evolution

For a continuous model, the state trajectory belongs to a declared trajectory space over an interval of `D_exec`.

The differential or integral law must identify:

- the state variables being evolved;
- admissible inputs;
- parameters;
- delay or memory dependencies;
- regularity assumptions required by the selected mathematical treatment.

A local linear approximation does not replace the declared nonlinear model outside its stated approximation region.

## 14. Discrete Evolution

For a discrete model, a deterministic state-update map may be typed as:

`F_TR: S_TR × X_TR,in × Λ_TR → S_TR`

when the model is memoryless with respect to variables outside `S_TR`.

If additional retained history affects the update, the update contract must include that history explicitly or include it inside an augmented state.

## 15. Hybrid Evolution

A hybrid TR model must separate continuous evolution from discrete events.

A discrete transition may change:

- ternary state;
- route state;
- topology state;
- control mode;
- parameter branch;
- another declared discrete component.

Such a discrete event is not automatically a bifurcation of the underlying continuous dynamics.

## 16. Resonance-Coordinate Mapping

The canonical resonance-coordinate mapping inherited from Volume 02 remains:

`P_R: S × P → X_R`

for the general state and parameter spaces used by the originating model definition.

A concrete TR specialization must identify how its own `S_TR` and `Λ_TR` instantiate the source of that mapping.

If resonance coordinates depend on retained history, the model must provide a history-aware mapping with an explicitly declared source space.

## 17. Resonance Coordinate Is Not Frequency

A resonance coordinate:

`r ∈ X_R`

may include frequency-related information, but resonance is not reduced to frequency equality.

Therefore:

`resonance ≠ frequency equality`

A model may use a multidimensional, history-dependent, topology-dependent, or scale-dependent resonance coordinate space.

## 18. Admissible Resonance Domain

The resonance classifier operates on the declared admissible resonance domain:

`X_R,adm ⊆ X_R`

A state outside the admissible domain must not be assigned a valid resonance classification unless the model explicitly defines an extension of the classifier.

Invalid input and valid `OUTSIDE` resonance classification are different conditions.

## 19. Resonance Window

The resonance window remains:

`W_R ⊂ X_R`

with boundary:

`∂W_R`

The window is finite and model-relative.

It may be:

- parameter-dependent;
- history-dependent;
- hysteretic;
- topology-dependent;
- scale-dependent.

No universal TR-EIF resonance window is implied.

## 20. Resonance Classification

The canonical minimum classification set remains:

`R_C = {OUTSIDE, BOUNDARY, INSIDE}`

with classifier:

`C_R: X_R,adm → R_C`

The classifier is a classification mapping.

It is not the state evolution law.

## 21. Resonance Classification and Ternary State

The following automatic identification remains forbidden:

`OUTSIDE = -1`

`BOUNDARY = 0`

`INSIDE = 1`

A specific model may define an additional typed projection from resonance information into a ternary target, but the two state spaces remain distinct.

## 22. Phase Module Boundary

A phase-oscillator module may supply state or observables used by the resonance-coordinate mapping.

It does not replace the complete TR system model.

In particular, the Kuramoto–Sakaguchi module is one admissible classical phase module inside TR-EIF.

Therefore:

`phase dynamics ≠ complete TR-EIF dynamics`

## 23. Oscillator Phase Boundary

Oscillator phase belongs to a circular phase domain.

It must not be treated as an unrestricted real coordinate without a declared representation relation.

Oscillator phase is also distinct from the physical phase of matter:

`oscillator phase ≠ physical phase of matter`

## 24. Synchronization Boundary

Synchronization must be defined by a model-specific relation or observable.

It remains distinct from resonance and phase locking:

`synchronization ≠ resonance`

`synchronization ≠ phase locking`

## 25. Phase-Locking Boundary

Phase locking requires its own declared criterion.

It remains distinct from resonance:

`phase locking ≠ resonance`

A persistent phase relation may contribute to a resonance coordinate without becoming synonymous with the resonance state.

## 26. Coherence Boundary

Coherence requires an independently declared observable or relation.

It remains distinct from uniformity, resonance, and phase order:

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

The FRP-specific distinction remains:

`R(t) ≠ C(t)`

## 27. Ternary Domain

The balanced ternary state set remains exactly:

`T = {-1, 0, 1}`

Canonical notation remains:

`-1/0/1`

No fourth execution state is introduced by this chapter.

## 28. Active Neutral State

State `0` remains an active state.

Depending on the model, it may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

State `0` is not automatically:

- passive;
- absent;
- missing data;
- invalid state;
- error;
- no signal.

## 29. Ternary Target

A model may define a target-generation mapping from resonance state, history, current ternary state, parameters, or another declared source into a ternary target.

The target belongs to `T` but remains distinct from the executed state.

Therefore:

`target state ≠ executed state`

## 30. Executed Ternary State

The executed ternary state is the retained state after application of all declared transition guards, routing rules, capacity constraints, scheduler conditions, and other execution constraints.

The presence of a target does not guarantee immediate execution.

## 31. Forbidden Direct Opposite Transitions

The following executed transitions remain forbidden:

`-1 → 1`

`1 → -1`

This is an exact semantic invariant rather than a numerical tolerance condition.

## 32. Required Opposite-State Routes

Opposite-polarity execution must use:

`-1 → 0 → 1`

or:

`1 → 0 → -1`

Each arrow denotes a distinct executed transition leg.

## 33. Transition-Leg Independence

Completion of the first leg does not automatically authorize the second leg.

After:

`-1 → 0`

or:

`1 → 0`

the model must evaluate the conditions governing any later second leg independently.

## 34. Neutral Residence

The neutral state may persist for any admissible number of execution steps unless a concrete model defines a stronger residence condition.

Thus:

`0 → 0`

may be a valid retained-state relation.

Neutral persistence is not automatically a failed transition.

## 35. Pending Route

A model may retain a pending destination after the first leg of an opposite-state route.

A pending route is stateful execution information.

It must preserve sufficient information to determine whether the route is later:

- completed;
- retained;
- cancelled;
- redirected.

A pending destination is not an executed destination.

## 36. Route Cancellation

A pending route may be cancelled when its later admissibility conditions no longer hold.

Cancellation must not be represented as if the second leg had executed.

The trace must preserve the difference between:

`route cancelled`

and:

`route completed`

## 37. Route Redirection

If a neutral state is re-evaluated and a different admissible branch becomes the next target, that change is a new decision under the model's route semantics.

The first leg of an earlier route does not create permanent authorization for its original destination.

## 38. Transition Guard

A ternary transition guard must consume only declared state and context.

The guard decides transition admissibility.

It does not redefine resonance classification, structural state, or physical phase state.

## 39. Capacity Constraint

If the execution model limits the number of admissible state changes per execution step, that capacity must be represented as an explicit execution constraint.

Capacity affects which authorized changes can execute at a particular step.

It is not a resonance threshold.

## 40. Scheduler Constraint

If a model includes scheduler states, the scheduler must be represented as a separate execution-state component or input.

Scheduler state may enable or block particular transition classes.

A scheduler-state change is not automatically:

- a resonance transition;
- a bifurcation;
- a structural transition;
- a physical phase transition.

## 41. Feedback

A TR model may feed ternary state, resonance state, transition activity, or another declared output back into its own continuous or discrete dynamics.

Every feedback mapping must define:

- source space;
- target space;
- update order;
- whether the dependence is instantaneous, delayed, or retained;
- any saturation or clipping relation.

Feedback does not permit implicit type conversion between unrelated state spaces.

## 42. Open-Loop and Closed-Loop TR Models

A TR specialization may be open-loop or closed-loop.

An open-loop model does not use selected TR outputs to modify later internal evolution.

A closed-loop model does.

Closed-loop execution does not mean a thermodynamically closed physical system.

## 43. Coupling State

Coupling must be represented by a declared coupling operator, relation, graph, matrix, field, hierarchy, or equivalent typed object.

Coupling may depend on:

- state;
- topology;
- distance;
- hierarchy;
- parameters;
- thermal state;
- other declared variables.

`phase coupling ≠ mechanical force`

unless an independent physical mapping establishes such a relation.

## 44. Delay

Delay must identify what variable is delayed and by what mechanism.

A delayed state relation is not interchangeable with phase lag.

Therefore:

`delay ≠ phase lag`

A model with retained frequency memory must not be rewritten as explicit pairwise delayed phase coupling unless that mapping is separately defined.

## 45. Memory

Memory may be represented through retained state rather than explicit delayed arguments.

Examples include:

- retained frequency;
- filtered coupling state;
- hysteresis state;
- pending route state;
- retained topology state.

Every memory mechanism must identify the retained variable and its update law.

## 46. Dissipation

A dissipative TR model must identify the state variables and terms through which dissipation enters the dynamics.

Dissipation is not synonymous with transition to ternary `0`.

Active neutralization may occur without being a physical dissipation law.

## 47. Saturation

If an update is bounded by saturation, clipping, finite capacity, or another nonlinear constraint, the constraint belongs to the model definition.

A linear approximation that omits the constraint is valid only within the region where the omitted nonlinearity does not affect the stated result.

## 48. Topology

Let a model contain an interaction topology when interactions are not all-to-all by definition.

The topology must define:

- component set;
- admissible interaction relations;
- directionality where applicable;
- weights where applicable;
- update rules if topology is dynamic.

Topology change and state change remain distinct events.

## 49. Multiscale State

A multiscale TR model must retain the scale distinctions defined in Chapter 08.

Scale-specific resonance states, phase-order states, ternary compositions, and regime descriptors must not be flattened into one scalar unless a declared aggregation mapping is sufficient for the claim being made.

## 50. Cross-Scale Mapping

A cross-scale mapping must specify:

- source scale;
- destination scale;
- domain;
- codomain;
- aggregation or expansion relation;
- information loss;
- ordering or causal interpretation where claimed.

A coarse state is not automatically invertible to the fine state.

## 51. Phase-Order Hierarchy

A multiscale phase-order representation may contain pair-domain, cluster, supercluster, and global channels or another declared hierarchy.

The global channel does not reconstruct the local hierarchy in general.

Therefore:

`global phase order ≠ multiscale phase-order state`

## 52. Resonance Regime

A resonance regime is defined by the regime classifier established in Chapter 07.

A regime transition is not automatically a bifurcation.

A threshold crossing is not automatically a regime transition unless the regime definition says so.

## 53. Bifurcation Boundary

A named bifurcation requires class-specific mathematical evidence.

The following remain distinct:

`threshold crossing ≠ bifurcation`

`resonance-window crossing ≠ bifurcation`

`resonance-regime transition ≠ bifurcation`

`scheduler change ≠ bifurcation`

`ternary transition ≠ bifurcation`

## 54. Structural Transition Boundary

A structural transition requires an independently defined structural state space and structural transition criterion.

Therefore:

`ternary transition ≠ structural transition`

and:

`resonance-regime transition ≠ structural transition`

unless an additional validated mapping establishes the relation for a particular model.

## 55. Physical Phase-Transition Boundary

A physical phase transition requires an independently defined physical model and appropriate evidence.

Therefore:

`structural transition ≠ physical phase transition`

and:

`oscillator phase ≠ physical phase of matter`

No phase-order increase alone establishes a physical phase transition.

## 56. Observable Output Space

Let `Y_TR,out` denote the typed TR output space established in Chapter 09.

A memoryless output mapping may be written as:

`O_TR,out: S_TR → Y_TR,out`

A history-dependent output mapping must use the appropriate history-state source.

The output space may contain multiple channels rather than one scalar.

## 57. Observable Is Not State

An observable remains a mapping from state or history state into an observable codomain.

Unless the mapping is injective on the declared domain:

`observable ≠ complete state`

The system-closure contract therefore cannot replace state semantics with telemetry semantics.

## 58. Trace Contract

An executable TR specialization must provide a trace contract sufficient for the claims it validates.

The trace must preserve, where relevant:

- execution order;
- target state;
- executed state;
- active neutral state;
- pending route state;
- scheduler state;
- resonance coordinates;
- classification;
- multiscale observables;
- invariant counters;
- provenance;
- parameter identity.

## 59. Sampling Boundary

Sample adjacency is not automatically execution adjacency.

Therefore a sampled pair:

`-1, 1`

cannot by itself prove a forbidden direct transition if intermediate execution states were not observed.

Conversely, it cannot prove neutral mediation either.

The result is unresolved without sufficient execution resolution.

## 60. Validation Result Space

The validation-result space remains separate from the ternary state domain.

Using the Chapter 09 validation semantics:

`X_Val = {PASS, FAIL, UNRESOLVED}`

The following identifications remain forbidden:

`FAIL = -1`

`UNRESOLVED = 0`

`PASS = 1`

## 61. Exact Validation

Discrete semantic invariants require exact validation.

Examples include:

- membership in `{-1,0,1}`;
- prohibition of direct opposite-state execution;
- valid finite-state classifications;
- exact route ordering where encoded discretely;
- exact absence of reserved state codes where required.

A numerical tolerance cannot legalize an invalid discrete state.

## 62. Numerical Validation

Continuous, approximate, floating-point, or quantized comparisons may use numerical tolerance only when:

- the compared quantities are type-compatible;
- their units are compatible;
- the tolerance is declared;
- the tolerance has provenance;
- the tolerance belongs to the numerical realization rather than the exact mathematical definition.

## 63. Deterministic Replay

A deterministic replay claim requires the complete result-affecting execution state.

Depending on the specialization, this may include:

- continuous state;
- ternary retained state;
- target state;
- pending routes;
- scheduler state;
- topology;
- retained memory;
- parameters;
- pseudorandom state;
- input sequence;
- numerical configuration.

Deterministic replay establishes reproducibility under the declared contract.

It does not establish universal model correctness or physical validity.

## 64. Provenance Closure

Every claim-relevant parameter, threshold, mapping, observable, or validation tolerance must preserve one of the established provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

A value without sufficient provenance cannot be promoted silently to a universal constant.

## 65. TR Formal Contract

A minimally complete TR formal contract contains:

1. system class;
2. system boundary;
3. input space;
4. parameter space;
5. instantaneous state space;
6. history-state space where required;
7. execution-coordinate domain;
8. evolution operators or relations;
9. resonance-coordinate space;
10. resonance-coordinate mapping;
11. admissible resonance domain;
12. resonance window and boundary;
13. resonance classifier;
14. ternary target mapping where used;
15. ternary transition semantics;
16. active-neutral semantics;
17. route and capacity semantics where used;
18. feedback semantics where used;
19. multiscale mappings where used;
20. observable mappings;
21. trace contract;
22. validation predicates;
23. provenance assignments.

A specialization may add further objects but may not omit any object required by its own claims.

## 66. Closure by Explicit Dependency

A TR model is formally closed at the specification level when every result-affecting dependency is either:

- contained in its declared state;
- contained in its declared history state;
- supplied through a declared input;
- supplied through a declared parameter;
- supplied through a declared topology or environment interface.

An undeclared dependency breaks the closure contract.

## 67. Closure by Typed Transformation

Every transformation in the TR execution chain must have a declared source and target space.

A semantically complete chain therefore cannot contain an implicit step such as:

`resonance value → force`

or:

`phase state → chemical bond`

without an independently defined mapping.

## 68. Closure by Invariant Preservation

A TR realization must preserve all invariants that apply to its selected model features.

For the balanced ternary kernel, the invariant set always includes:

- exact state domain `{-1,0,1}`;
- active neutral `0`;
- no direct `-1 → 1` execution;
- no direct `1 → -1` execution;
- separate transition legs for opposite-state routes;
- independent authorization of the second leg.

## 69. Closure by Validation Boundary

A claim is closed only relative to a declared validator and sufficient evidence.

A model may therefore be:

- mathematically defined;
- executable;
- deterministically reproducible;

while still having empirical claims classified as `REQUIRES_TEST`.

These states of evidence are not contradictory.

## 70. TR Input Does Not Imply Interatomic Meaning

The source of `X_TR,in` may be an interatomic or equivariant representation, but this meaning is not automatic.

Before an interatomic state can enter the TR layer, the integration model must define the source mapping explicitly.

Thus:

`interatomic state ≠ TR state`

unless connected by a typed mapping.

## 71. EIF Boundary

The EIF layer concerns interatomic state, geometry, topology, local environments, transformation actions, invariant representations, equivariant representations, and interatomic mappings.

Those objects remain outside the mathematical scope of this chapter except where their interface with the TR layer must be typed.

The boundary is intentional.

## 72. Interatomic Source Space

Let `S_EIF` denote an EIF state space only after that space has been independently defined by the EIF formalism.

This chapter does not assign an internal structure to `S_EIF`.

It uses the symbol only to state the interface typing requirement.

## 73. EIF Representation Space

Let `Y_EIF` denote an independently defined EIF representation space.

A representation in `Y_EIF` may contain invariant and/or equivariant components according to its own symmetry contract.

No assumption is made here that every element of `Y_EIF` is scalar, invariant, local, or complete.

## 74. EIF-to-TR Mapping

An integration model connecting EIF to TR must define a typed mapping of the form:

`M_E→TR: Y_EIF → X_TR,in`

or a more structured mapping with additional declared parameters or history when required.

The mapping must specify:

- domain;
- codomain;
- locality;
- scale;
- transformation behavior;
- information loss;
- parameter dependence;
- physical interpretation.

The arrow cannot be assumed from shared terminology.

## 75. Direct Atomic-Phase Assignment Is Forbidden

An oscillator phase must not be assigned automatically to a literal atom merely because the EIF state contains atoms.

A model that associates phase variables with atoms, bonds, local environments, graph nodes, modes, or another interatomic object must define that association explicitly.

Therefore:

`atom ≠ oscillator phase`

## 76. Direct Geometry-to-Ternary Assignment Is Forbidden

Geometry does not automatically define ternary polarity.

A mapping from geometric or equivariant representation into ternary target must pass through an explicitly declared TR source and resonance mapping or another formally declared model route.

No coordinate sign, rotation, or permutation may silently become `-1`, `0`, or `1`.

## 77. TR-to-EIF Feedback Mapping

If TR state modifies an EIF representation or interatomic state, the integration model must define a separate feedback mapping.

A generic typed form is:

`M_TR→E: Y_TR,out × S_EIF → S_EIF`

when the feedback operates on the EIF state.

If the feedback instead operates on an intermediate EIF representation, its codomain must be changed accordingly and declared explicitly.

## 78. Feedforward and Feedback Are Distinct

The mapping:

`M_E→TR`

and the mapping:

`M_TR→E`

serve different directions and need not be inverses.

Information loss, locality, symmetry behavior, and dimensional meaning may differ between them.

Therefore:

`EIF-to-TR mapping ≠ TR-to-EIF feedback mapping`

## 79. Integration State

A coupled TR-EIF realization must distinguish the TR state from the EIF state even when they are updated in one numerical program.

A composite state may be represented as a product space such as:

`S_total = S_EIF × S_TR`

only after both component spaces have been independently defined.

The product-space notation does not itself define the coupling between the components.

## 80. Coupled Update

A coupled realization must specify the order or simultaneous relation between EIF and TR updates.

Possible formally declared arrangements include:

- EIF update followed by TR update;
- TR update followed by EIF update;
- operator splitting;
- jointly solved coupled update;
- event-triggered cross-layer update.

The chosen arrangement is part of the numerical or mathematical model and must not remain implicit.

## 81. Algebraic Loop Boundary

If EIF output depends instantaneously on TR output while TR output simultaneously depends on EIF output, the model contains an algebraic or implicitly coupled relation.

Such a relation requires an explicit solution condition.

It must not be implemented as an arbitrary update order while being described as simultaneous mathematics.

## 82. History Across the Integration Boundary

If either cross-layer mapping depends on history, the required history state must be declared.

A delayed EIF-to-TR signal and a delayed TR-to-EIF feedback signal are separate dependencies unless a model explicitly equates them.

## 83. Locality Across the Integration Boundary

Every cross-layer mapping must identify whether it is:

- local;
- neighborhood-local;
- graph-local;
- long-range;
- global;
- multiscale.

A global resonance observable must not silently update every local interatomic degree of freedom through an unspecified broadcast rule.

## 84. Information-Loss Boundary

If `M_E→TR` is many-to-one, the TR state cannot reconstruct the complete EIF representation in general.

If `M_TR→E` acts through a reduced TR output, the update cannot be assumed to contain information absent from that output.

Information loss must be acknowledged mathematically rather than hidden by implementation structure.

## 85. Dimensional Boundary

Cross-layer mappings must preserve dimensional consistency.

A dimensionless resonance classification or ternary state cannot be added directly to a dimensional interatomic quantity.

Any such coupling requires an independently defined dimensional mapping, coefficient, or transformation with valid units and provenance.

## 86. Energy Interface Boundary

An energy interface may exist only after an energy quantity and its mapping are independently defined.

Therefore:

`ternary state ≠ energy`

`resonance classification ≠ energy`

`phase order ≠ energy`

No energy-conservation or energy-gradient claim follows from the TR layer alone.

## 87. Force Interface Boundary

A force interface requires a vector or tensor transformation law appropriate to the physical model.

Therefore:

`phase coupling ≠ mechanical force`

`ternary state ≠ force`

`resonance state ≠ force`

A force law must be defined and validated independently.

## 88. Chemical-Bond Boundary

A chemical bond requires an independently defined interatomic or electronic criterion.

Therefore:

`phase relation ≠ chemical bond`

`phase locking ≠ chemical bond`

`resonance ≠ chemical bond`

`ternary state ≠ chemical bond`

## 89. Symmetry Contract

Every claim of invariance or equivariance requires a declared transformation group or transformation set `G`.

For each `g ∈ G`, the model must define:

- the action on the source space;
- the action on the target space;
- the domain on which the relation is asserted.

The word `equivariant` is not sufficient without these actions.

## 90. Equivariance Relation

Let:

`ρ_in(g): X → X`

and:

`ρ_out(g): Y → Y`

be declared actions on spaces `X` and `Y`.

A mapping:

`F: X → Y`

is equivariant with respect to those actions when:

`F(ρ_in(g)(x)) = ρ_out(g)(F(x))`

for every admissible `g ∈ G` and `x ∈ X`.

The relation must be proven or tested over the stated scope.

## 91. Invariance Relation

A mapping is invariant under a declared transformation when the output action is the identity action on its codomain.

Invariance of one output channel does not imply equivariance of all internal states or local outputs.

## 92. Permutation Boundary

Permutation invariance and permutation equivariance remain distinct.

A global scalar may be invariant under relabeling while a local component-indexed representation transforms equivariantly under the same relabeling.

These two claims require different output actions.

## 93. Translation Boundary

Translation behavior must be specified independently from permutation behavior.

A representation may be translation invariant, translation equivariant, or neither, depending on its definition.

Translation must not be merged into an unspecified generic symmetry label.

## 94. Rotation Boundary

Rotation behavior must be specified independently from translation and permutation behavior.

Vector, tensor, and higher-order equivariant outputs require the corresponding declared rotation action.

A scalar resonance label does not by itself establish rotational equivariance of the interatomic architecture.

## 95. Geometry Does Not Flip Ternary Polarity

No translation, rotation, or permutation is permitted to flip ternary polarity automatically.

If a transformation acts nontrivially on `T`, that action must be explicitly defined.

Absent such a definition, geometric transformation and ternary polarity remain separate semantics.

## 96. Multiscale Symmetry Boundary

A multiscale integration model must specify how transformation actions propagate across scales.

A symmetry valid for a global aggregate does not automatically establish the same transformation law for local or intermediate-scale channels.

## 97. Trace Equivariance Boundary

If transformed inputs are compared through execution traces, the correspondence between trace records must preserve:

- transformed component identities;
- execution order;
- event correspondence;
- scale identity;
- state-space typing.

Value-wise agreement without record correspondence is insufficient for a trace-level equivariance claim.

## 98. Numerical Solver Boundary

The mathematical TR model and the numerical solver remain distinct objects.

Changing:

- step size;
- integration scheme;
- quantization;
- fixed-point width;
- update order;
- convergence tolerance;

may change the numerical realization without changing the formal model definition.

Any equivalence claim must specify which level is being compared.

## 99. Serialization Boundary

JSON, CSV, binary words, text traces, or another transport format do not redefine the mathematical model.

Serialization may encode state and observables, but:

`serialization schema ≠ state-space definition`

and:

`schema validity ≠ scientific validation`

## 100. Implementation Specialization

A computational implementation is a specialization of the TR formal contract when it assigns concrete representations and algorithms to selected formal objects.

Implementation-specific choices may include:

- discrete scheduler modes;
- finite capacity;
- fixed-point encodings;
- particular thresholds;
- particular coupling topology;
- particular memory coefficients;
- specific trace fields.

Such choices remain implementation parameters unless independently generalized.

## 101. FRP Executable Reference Role

The current Fractal Resonance Processor repository provides an executable specialization of selected TR semantics.

The relation is:

`TR-EIF formal theory`

`→ FRP executable specialization/reference`

It is not:

`TR-EIF = FRP`

FRP establishes executable realization of specific mechanisms, not universal physical law.

## 102. FRP Upstream Target Generation

In the current executable reference file:

`frp_prototype_v1_7_0.py`

the function `target_state` derives a ternary target from `sin(phase)` using the implementation threshold magnitude `0.33`.

This establishes an executable target-generation mechanism.

The threshold is an FRP implementation parameter and is not a universal TR-EIF resonance threshold.

## 103. FRP Target and Retained-State Separation

The current FRP floating reference keeps the phase-derived desired state separate from the retained cell state.

When current and desired states have opposite nonzero polarity, the implementation does not execute the desired opposite state directly.

It first applies active neutral `0` and records the destination as a pending neutral route.

## 104. FRP Pending-Route Completion

The current FRP function:

`process_pending_neutral_routes`

processes retained pending destinations separately from their first-leg creation.

A pending destination executes only when its later conditions are satisfied, including the cell still being in neutral state and available transition capacity.

This is a concrete executable realization of transition-leg independence.

## 105. FRP Transition Capacity

The current floating reference computes a per-tick maximum number of changes and processes pending routes, explicit requests, and automatic targets under that capacity.

The capacity bound controls execution throughput.

It is not a universal resonance quantity.

## 106. FRP Retained Frequency Memory

The current floating reference updates retained frequency toward a frequency target through a relaxation relation implemented in `update_delay_dynamics`.

The target depends on base frequency, absolute ternary state, and switching activity.

This establishes a concrete memory/lag channel.

It does not establish an explicit pairwise delay term of the form `theta_j(t - tau_ij)`.

## 107. FRP Phase Update

The current floating reference updates wrapped phase tact by tact after coupling, retained-frequency, thermal, and local phase-lag related updates.

The wrapped phase state remains circular.

Its execution order is an implementation specialization rather than a universal ordering imposed on every TR-EIF model.

## 108. FRP Multiscale Phase Order

The current floating reference computes multiscale phase-order descriptors over its dyadic hierarchy.

This provides concrete local-to-global phase-order observability.

It does not collapse multiscale order into complete structural coherence.

## 109. FRP RTL Boundary

The current file `rtl/m16/frp_m16_core.sv` implements the M16 RTL composition. This RTL layer begins downstream of upstream ternary-target generation.

The verified RTL composition includes:

`scheduler`

`→ request handling`

`→ pending-route processing`

`→ active-neutral transition generation`

`→ transition-capacity guard`

`→ retained-state writeback`

`→ invariant checks`

This is a concrete downstream execution boundary rather than the complete upstream resonance model.

## 110. FRP Scheduler Specialization

The current file `rtl/m16/frp_m16_scheduler.sv` implements scheduler specialization supporting the modes:

`7/1`

and:

`1/7`

with their established balance/commit and excite/neutralize tact semantics.

These scheduler modes are FRP execution semantics.

They are not universal TR-EIF timing constants.

## 111. FRP Active-Neutral RTL Semantics

The current M16 RTL composes `frp_m16_pending_routes.sv`, `frp_m16_active_neutral.sv`, `frp_m16_capacity_guard.sv`, and `frp_m16_state_update.sv` under the core boundary.

Its qualification targets include zero actual direct opposite-polarity execution.

This provides hardware-facing executable evidence for the same core ternary invariant:

`-1/0/1`

with mandatory neutral mediation of opposite transitions.

## 112. FRP Is Not EIF

The current FRP implementation does not by itself define the complete Equivariant Interatomic Framework.

FRP execution traces, scheduler semantics, phase dynamics, ternary routing, and RTL invariants therefore must not be used as substitutes for:

- atomic configuration spaces;
- local atomic environments;
- permutation actions;
- translation actions;
- rotation actions;
- equivariant interatomic representations;
- force or energy mappings.

## 113. FRP Evidence Boundary

The current FRP code establishes that selected TR execution semantics are implementable and observable.

It does not by itself prove:

- universal physical constants;
- universal interatomic resonance;
- chemical bonding;
- physical phase transitions;
- generic force laws;
- generic energy laws;
- empirical validity for an arbitrary material system.

## 114. Minimal Computational Realization Contract

A computational realization of a selected TR model must define:

- state representation;
- history representation where required;
- parameter representation;
- update ordering;
- numerical method;
- target generation;
- transition guarding;
- active-neutral execution;
- capacity and scheduler semantics where used;
- observable extraction;
- trace serialization;
- deterministic replay state;
- validation rules.

## 115. Minimal EIF Integration Contract

A TR-EIF integration is not admissible until it defines:

1. `S_EIF` or the relevant EIF source state;
2. `Y_EIF` or the relevant EIF representation space;
3. transformation group or transformation set;
4. source actions;
5. target actions;
6. `M_E→TR` with domain and codomain;
7. locality and scale of `M_E→TR`;
8. information loss of `M_E→TR`;
9. TR source state and resonance mapping;
10. ternary target and execution semantics;
11. `M_TR→E` when feedback exists;
12. transformation behavior of `M_TR→E`;
13. dimensional compatibility;
14. observable and validation contract;
15. empirical interpretation boundary.

## 116. Integration Admissibility

An integration claim is admissible only when every cross-layer arrow is explicitly typed.

A diagram containing arrows between named modules is not sufficient by itself.

Each arrow must correspond to a mapping, relation, or declared data-transfer contract with known source and target semantics.

## 117. Invalid Integration Shortcuts

The following shortcuts are invalid unless independently defined:

`atomic coordinate → ternary polarity`

`atomic label → oscillator phase`

`phase locking → chemical bond`

`resonance → force`

`resonance classification → energy`

`ternary state → physical phase`

`geometry transform → ternary sign flip`

`FRP telemetry → universal material observable`

## 118. Claim Traceability

Every major integrated claim must support the chain:

`claim`

`→ source definition or primary source`

`→ typed mapping`

`→ parameter provenance`

`→ execution or calculation`

`→ observable`

`→ trace`

`→ validator`

`→ evidence boundary`

A missing link prevents promotion of the claim beyond its supported scope.

## 119. TR Closure Invariants

The following invariants define the closed TR layer contract.

1. `TR` means Ternary Resonant.
2. `EIF` means Equivariant Interatomic Framework.
3. The TR layer is not the complete TR-EIF architecture.
4. Every modeled state has a declared state space.
5. Every mapping has a declared domain and codomain.
6. Continuous, discrete, and hybrid states remain distinguishable.
7. History-dependent relations declare history state.
8. Delay remains distinct from phase lag.
9. Circular phase remains distinct from an unrestricted real coordinate.
10. Resonance remains distinct from frequency equality.
11. Resonance remains distinct from synchronization.
12. Synchronization remains distinct from phase locking.
13. Phase locking remains distinct from resonance.
14. Coherence remains distinct from uniformity.
15. Coherence remains distinct from resonance.
16. Phase order remains distinct from complete coherence.
17. `R(t) ≠ C(t)` remains mandatory.
18. Resonance classification remains distinct from ternary state.
19. `OUTSIDE`, `BOUNDARY`, and `INSIDE` do not map automatically to `-1/0/1`.
20. The ternary domain remains exactly `{-1,0,1}`.
21. Canonical notation remains `-1/0/1`.
22. State `0` remains active.
23. Direct `-1 → 1` execution remains forbidden.
24. Direct `1 → -1` execution remains forbidden.
25. Opposite-state routes remain neutral-mediated.
26. Transition legs remain independent events.
27. The first leg does not authorize the second leg automatically.
28. Neutral residence remains admissible.
29. Pending target remains distinct from executed state.
30. Capacity remains distinct from resonance classification.
31. Scheduler state remains distinct from resonance state.
32. Resonance-window crossing remains distinct from bifurcation.
33. Bifurcation remains distinct from ternary transition.
34. Ternary transition remains distinct from structural transition.
35. Structural transition remains distinct from physical phase transition.
36. Oscillator phase remains distinct from physical phase of matter.
37. Observable remains distinct from complete state unless invertibility is established.
38. Trace serialization remains distinct from mathematical semantics.
39. Exact mathematics remains distinct from numerical tolerance.
40. Validation status remains distinct from ternary state.
41. Provenance class remains distinct from validation result.
42. Deterministic replay remains distinct from physical validation.
43. Implementation parameters remain distinct from universal constants.
44. FRP remains an executable specialization/reference rather than the complete TR-EIF theory.
45. TR output remains distinct from EIF state.
46. Interatomic meaning requires explicit cross-layer mapping.
47. Equivariance requires declared transformation actions.
48. Permutation, translation, and rotation remain distinct transformation semantics.
49. Geometry transformation does not automatically flip ternary polarity.
50. Force, energy, and chemical-bond meanings require independent definitions.

## 120. Formal Non-Equivalences

The following non-equivalences remain mandatory:

`TR-EIF ≠ ternary state machine only`

`TR-EIF ≠ resonance model only`

`TR-EIF ≠ Kuramoto–Sakaguchi model`

`TR-EIF ≠ interatomic potential only`

`TR-EIF ≠ machine-learning framework only`

`TR-EIF ≠ FRP documentation`

`TR layer ≠ EIF layer`

`interatomic state ≠ TR state`

`EIF representation ≠ resonance state`

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`resonance classification ≠ ternary state`

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

`target state ≠ executed state`

`pending target ≠ executed state`

`state 0 ≠ missing data`

`state 0 ≠ invalid state`

`delay ≠ phase lag`

`capacity limit ≠ resonance threshold`

`scheduler change ≠ bifurcation`

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

`observable ≠ complete state`

`sample adjacency ≠ execution adjacency`

`schema validity ≠ semantic validation`

`deterministic replay ≠ physical validation`

`implementation parameter ≠ universal physical constant`

`hierarchy ≠ equivariance`

`permutation invariance ≠ permutation equivariance`

`EIF-to-TR mapping ≠ TR-to-EIF feedback mapping`

## 121. Formal TR Dependency Chain

The closed Ternary Resonant dependency chain is:

`system class`

`→ boundary`

`→ input / parameter / state / history spaces`

`→ continuous, discrete, or hybrid evolution`

`→ coupling / delay / memory / dissipation / topology`

`→ resonance-coordinate mapping`

`→ resonance state in X_R`

`→ resonance-window relation`

`→ resonance classification`

`→ ternary target generation`

`→ transition guard`

`→ capacity / scheduler constraints where used`

`→ active-neutral -1/0/1 execution`

`→ retained state and pending-route update`

`→ feedback into declared TR dynamics where used`

`→ local / global / multiscale organization`

`→ observable mapping`

`→ ordered trace`

`→ provenance-bound evidence`

`→ claim-scoped validation`

No arrow in this chain implies an undeclared physical identity.

## 122. Formal TR-EIF Integration Chain

The integrated architecture requires the separately typed chain:

`interatomic state`

`→ EIF representation`

`→ explicit EIF-to-TR mapping`

`→ TR source state`

`→ resonance state`

`→ ternary target`

`→ active-neutral ternary execution`

`→ TR observable / retained state`

`→ explicit TR-to-EIF feedback mapping where defined`

`→ updated EIF representation or interatomic state`

This chain preserves both halves of the project name.

## 123. System-Closure Criterion

A TR specialization satisfies the system-closure criterion when all of the following are true:

- the system boundary is explicit;
- every result-affecting state variable is represented;
- every external dependency enters through a declared interface;
- every mapping is typed;
- resonance classification is defined relative to an admissible resonance domain and window;
- ternary target and executed state are separated;
- the `-1/0/1` invariants are exact;
- history, delay, and memory are represented when active;
- local, global, and multiscale states remain distinguishable;
- observables do not replace state definitions;
- trace resolution is sufficient for the claims being validated;
- validation scope and provenance are explicit;
- implementation-specific quantities remain implementation-specific;
- no interatomic, force, energy, bond, or physical phase meaning is inserted without an explicit mapping;
- EIF integration is represented only through typed cross-layer interfaces.

## 124. Conformance Requirements

A mathematical TR model conforms to this chapter when:

- it satisfies the system-closure criterion;
- it preserves all inherited Volume 01 and Volume 02 invariants applicable to its selected modules;
- it does not collapse distinct state spaces or scientific concepts;
- it declares every cross-layer dependency explicitly;
- it separates formal theory from implementation specialization and empirical calibration.

A computational realization conforms when:

- its numerical state corresponds to declared mathematical state or encoding relations;
- its execution order is explicit;
- target and retained state remain distinguishable;
- active neutral mediation is preserved exactly for opposite ternary transitions;
- history and retained state required for replay are preserved;
- trace and validation contracts are sufficient for its claims;
- implementation constants are not promoted to universal physical constants.

An integrated TR-EIF realization conforms when, in addition:

- the EIF state and representation spaces are independently defined;
- the transformation actions are independently defined;
- EIF-to-TR and TR-to-EIF mappings are typed;
- their locality, dimensional meaning, information loss, and symmetry behavior are explicit;
- equivariance or invariance claims satisfy their exact transformation relations.

## 125. Final System-Closure Statement

The Ternary Resonant layer of TR-EIF is a typed mathematical and computational system layer rather than a single equation, classifier, oscillator model, or state machine.

Its complete internal chain is:

`state and history`

`→ dynamics`

`→ resonance coordinates`

`→ resonance classification`

`→ ternary target`

`→ guarded active-neutral -1/0/1 execution`

`→ retained and multiscale state`

`→ observables`

`→ traces`

`→ validation`

The balanced ternary kernel remains exactly:

`-1/0/1`

with active:

`0`

and mandatory opposite-state mediation:

`-1 → 0 → 1`

`1 → 0 → -1`

The FRP repository demonstrates one executable specialization of selected TR dynamics, target generation, retained-frequency memory, neutral routing, pending-route continuation, capacity control, scheduler semantics, multiscale phase-order observability, and downstream RTL execution invariants.

Those mechanisms establish executable reference behavior within their implementation scope. They do not replace the general TR-EIF theory and do not establish universal interatomic physics.

The EIF side remains a separately typed mathematical layer. The only admissible connection is through explicit mappings with declared domains, codomains, symmetry actions, locality, dimensional behavior, information loss, and validation scope.

The resulting architectural identity is therefore preserved as:

`Ternary Resonant`

`+`

`Equivariant Interatomic Framework`

connected by explicit mathematical interfaces rather than by semantic collapse.
