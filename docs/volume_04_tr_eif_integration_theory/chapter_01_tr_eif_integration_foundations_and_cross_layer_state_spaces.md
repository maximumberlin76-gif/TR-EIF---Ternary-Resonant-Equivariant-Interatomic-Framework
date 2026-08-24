# TR-EIF Integration Foundations and Cross-Layer State Spaces

## 1. Purpose

This document establishes the mathematical foundations of the integration layer of the Ternary Resonant Equivariant Interatomic Framework.

Volumes 02 and 03 define two independently closed layers:

`TR = Ternary Resonant`

and:

`EIF = Equivariant Interatomic Framework`

The purpose of Volume 04 is to define their explicit composition without collapsing their state spaces, semantics, transformation laws, physical interpretations, or validation boundaries.

The integration architecture begins from the typed chain:

`interatomic state`

`→ equivariant representation`

`→ explicit EIF-to-TR mapping`

`→ TR input state`

`→ resonance coordinates`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated -1/0/1 execution`

and, where feedback is defined:

`TR output`

`→ explicit TR-to-EIF mapping`

`→ EIF update`

`→ updated interatomic state`

This chapter defines:

- the integration system boundary;
- cross-layer state spaces;
- source and target interfaces;
- forward and reverse mappings;
- cross-layer transformation compatibility;
- locality and scale contracts;
- dimensional compatibility;
- information-loss semantics;
- target-versus-executed-state separation;
- feedback typing;
- coupled state construction;
- history requirements;
- cross-layer invariants;
- integration admissibility;
- validation boundaries.

No EIF quantity becomes a TR quantity by notation, numerical equality, sign, dimensional resemblance, or implementation convenience.

No TR quantity becomes an interatomic physical quantity without an explicit typed mapping.

## 2. Dependency

This chapter depends on the closed mathematical definitions of:

- Volume 01, Mathematical Foundations;
- Volume 02, Ternary Resonance Theory;
- Volume 03, Equivariant Interatomic Framework.

In particular, it inherits:

- typed domains and codomains;
- mapping semantics;
- state and observable separation;
- provenance classes;
- validation semantics;
- `X_R`;
- `P_R`;
- `W_R`;
- `∂W_R`;
- resonance classification;
- `T = {-1, 0, 1}`;
- active-neutral semantics;
- target and executed-state separation;
- neutral-mediated opposite-state transitions;
- `X_TR,in`;
- `S_TR`;
- `Y_TR,out`;
- `S_EIF`;
- `Y_EIF,out`;
- EIF transformation actions;
- invariant and equivariant representation semantics;
- EIF physical-output boundaries;
- EIF multiscale semantics;
- EIF dynamic-state semantics.

Volume 04 does not redefine either closed layer.

It defines their composition.

## 3. Scientific Status

### 3.1 GENERAL MATHEMATICAL STRUCTURE

The following use general mathematical structure:

- product spaces;
- mappings;
- composition;
- group actions;
- commutation relations;
- state-transition systems;
- history-dependent mappings;
- dimensional mappings;
- information-preserving and information-losing transformations.

### 3.2 TR-EIF FORMAL / AUTHOR-DEFINED

The following are author-defined TR-EIF integration architecture:

- cross-layer state construction;
- EIF-to-TR interface semantics;
- TR-to-EIF feedback semantics;
- integration admissibility;
- cross-layer locality contracts;
- cross-layer scale contracts;
- integration invariants;
- integration validation boundaries.

### 3.3 DERIVED

Relations that follow directly from previously defined mappings, transformation actions, or state-transition rules are classified as:

`DERIVED`

when used as derived results.

### 3.4 EMPIRICAL / CALIBRATED

Any cross-layer mapping fitted to physical or computational reference data requires appropriate empirical or calibrated provenance.

### 3.5 OPERATIONAL / EXECUTABLE REFERENCE

An executable specialization may instantiate the integration contract.

Executable behavior establishes implementation behavior within its tested scope.

It does not by itself establish universal interatomic physics.

### 3.6 UNVERIFIED

A cross-layer physical interpretation remains unresolved when its required mapping, units, symmetry behavior, evidence, or validation relation has not been established.

## 4. Integration Identity

The integrated framework is:

`TR-EIF = Ternary Resonant Equivariant Interatomic Framework`

The integration relation is not:

`TR = EIF`

and not:

`EIF = TR`

Instead:

`TR-EIF = explicit composition of distinct TR and EIF layers`

The word `integration` therefore means typed coupling, not semantic identification.

## 5. Independent Layer Closure

Before integration:

`S_TR`

and:

`S_EIF`

are independently defined state spaces.

Likewise:

`X_TR,in`

and:

`Y_EIF,out`

are independently defined interface spaces.

No equality between them is inherited.

Therefore:

`S_TR ≠ S_EIF`

and, in general:

`Y_EIF,out ≠ X_TR,in`

## 6. Integration System Boundary

An integrated specialization must define a system boundary containing:

- the participating EIF subsystem;
- the participating TR subsystem;
- cross-layer forward interfaces;
- cross-layer feedback interfaces where present;
- external inputs;
- external outputs;
- retained cross-layer history;
- cross-layer parameters;
- timing or update semantics;
- validation scope.

The integrated system is incomplete if any result-affecting cross-layer dependency remains implicit.

## 7. EIF Source State

Let:

`s_E ∈ S_EIF`

denote an EIF state.

The state may contain configuration, geometry, topology, local environments, representations, multiscale state, dynamic state, and retained history according to the selected EIF specialization.

The integration layer does not redefine these components.

## 8. EIF Integration Output

Let:

`Y_EIF,out`

be the terminal typed output space of the EIF layer.

Let:

`O_E: S_EIF → Y_EIF,out`

be the declared EIF integration-output mapping.

Then:

`y_E = O_E(s_E)`

with:

`y_E ∈ Y_EIF,out`

The output may contain one or more declared channels.

## 9. EIF Output Is Not Complete EIF State

In general:

`y_E ≠ s_E`

The output may be a lossy projection of the complete EIF state.

Any information loss must be declared.

## 10. TR Input Space

Let:

`X_TR,in`

be the declared input space of the selected TR specialization.

An input satisfies:

`x_T ∈ X_TR,in`

The integration layer must not assume that an arbitrary EIF output already belongs to this space.

## 11. Forward Integration Mapping

Define the EIF-to-TR mapping:

`M_E→T: D_E→T → X_TR,in`

where:

`D_E→T ⊆ Y_EIF,out × H_E→T × Λ_E→T`

is the admissible forward-integration domain.

Here:

- `H_E→T` is the forward cross-layer history space;
- `Λ_E→T` is the forward integration parameter space.

For:

`(y_E, h_ET, λ_ET) ∈ D_E→T`

the TR input is:

`x_T = M_E→T(y_E, h_ET, λ_ET)`

A memoryless specialization may use a reduced domain.

## 12. Forward Mapping Is Mandatory

The following shortcut is forbidden:

`y_E = x_T`

unless equality is explicitly established by a declared identity mapping between compatible spaces.

The existence of equal numerical arrays does not establish such identity.

## 13. Forward Mapping Contract

Every `M_E→T` must define:

- domain;
- codomain;
- admissible inputs;
- units;
- transformation behavior;
- locality;
- scale;
- history dependence;
- parameter provenance;
- information loss;
- numerical realization where applicable;
- validation relation.

## 14. Forward History State

If the forward mapping depends on previous EIF outputs, previous TR states, filtered quantities, delayed quantities, or hysteresis, that dependence belongs to:

`H_E→T`

A history-dependent mapping must not be represented as memoryless.

## 15. Forward Parameter Space

Let:

`Λ_E→T`

contain all forward-integration parameters.

These may include:

- normalization parameters;
- projection parameters;
- learned parameters;
- calibrated parameters;
- scale-selection parameters;
- routing parameters;
- thresholds where explicitly defined.

No such parameter is a universal physical constant merely because it appears in an integration specialization.

## 16. TR State

Let:

`s_T ∈ S_TR`

denote the complete state of the selected Ternary Resonant subsystem.

The state may contain:

- continuous resonant variables;
- phase variables where used;
- resonance coordinates;
- ternary retained state;
- pending routes;
- memory;
- topology;
- multiscale state;
- scheduler state where used.

The exact decomposition is specialization-dependent.

## 17. TR Input Is Not TR State

In general:

`x_T ≠ s_T`

An input may affect state evolution without being retained as state.

The integration layer must preserve this distinction.

## 18. TR Evolution

Let:

`Φ_T`

denote the declared TR evolution or update relation.

In discrete form, a specialization may define:

`s_T[n + 1] = Φ_T(s_T[n], x_T[n], h_T[n], λ_T)`

where:

- `h_T[n]` is declared TR history where required;
- `λ_T` is the TR parameter state.

This notation does not impose a universal discrete-time model.

## 19. Resonance Mapping Remains Internal to TR

The EIF-to-TR mapping produces a valid TR input or source object.

It does not automatically produce resonance classification.

The TR chain remains:

`TR input`

`→ TR dynamics`

`→ resonance-coordinate mapping`

`→ resonance state`

`→ resonance-window relation`

`→ resonance classification`

unless a specialization explicitly defines a shorter typed composition.

## 20. Resonance Coordinate Boundary

The resonance state remains:

`r ∈ X_R`

The integration layer does not identify:

`Y_EIF,out`

with:

`X_R`

automatically.

Therefore:

`EIF output ≠ resonance state`

without a declared mapping.

## 21. Resonance Window Boundary

A resonance window remains:

`W_R ⊂ X_R`

with boundary:

`∂W_R`

An EIF quantity does not become inside, outside, or on the boundary of a resonance window until it has been mapped into the relevant resonance-coordinate space.

## 22. Resonance Classification Boundary

The canonical classification remains:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

These classes are not balanced ternary states.

Therefore:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless an additional model-specific mapping explicitly defines such a relation.

## 23. Ternary Target Mapping

Let:

`G_T`

denote a declared TR target-generation mapping.

Its output belongs to:

`T = {-1, 0, 1}`

The target:

`t_target ∈ T`

is a requested ternary destination.

It is not automatically the executed retained state.

## 24. Executed Ternary State

Let:

`t_exec ∈ T`

denote the executed retained ternary state.

The integration layer must preserve:

`target ≠ executed state`

as distinct semantic roles.

Numerical equality at one instant does not erase this distinction.

## 25. Active Neutral Invariant

The balanced ternary kernel is exactly:

`-1/0/1`

with:

`T = {-1, 0, 1}`

The state:

`0`

is active.

It may perform:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

It is not missing data.

## 26. Forbidden Direct Opposite Transitions

The executed transitions:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

Integration cannot override this invariant.

## 27. Required Opposite-State Routes

Opposite-state execution requires:

`-1 → 0 → 1`

or:

`1 → 0 → -1`

Each leg is a separate event.

The first leg does not automatically authorize the second.

## 28. EIF Input Cannot Bypass Neutral Mediation

An EIF-derived TR target requesting opposite polarity does not authorize a direct opposite executed transition.

The request remains subject to the closed TR transition semantics.

## 29. Neutral Retention

The executed state may remain:

`0`

for an arbitrary number of admissible execution steps unless a selected model defines a stronger rule.

Cross-layer coupling does not imply immediate completion of a pending opposite route.

## 30. TR Output Space

Let:

`Y_TR,out`

be the declared output space of the selected TR subsystem.

Define:

`O_T: S_TR → Y_TR,out`

with:

`y_T = O_T(s_T)`

The output may expose:

- ternary state;
- resonance coordinates;
- resonance classification;
- phase-order observables;
- coherence observables;
- multiscale observables;
- retained state;
- other declared channels.

## 31. TR Output Is Not EIF Update Automatically

In general:

`y_T ≠ Δs_E`

A TR output requires an explicit reverse mapping before it can affect EIF state.

## 32. Reverse Integration Mapping

Where feedback exists, define:

`M_T→E: D_T→E → U_E`

where:

- `D_T→E ⊆ Y_TR,out × S_EIF × H_T→E × Λ_T→E`;
- `H_T→E` is reverse cross-layer history;
- `Λ_T→E` is reverse integration parameter space;
- `U_E` is a declared EIF update space.

For admissible arguments:

`u_E = M_T→E(y_T, s_E, h_TE, λ_TE)`

with:

`u_E ∈ U_E`

## 33. EIF Update Space

`U_E`

must define what kind of EIF modification is represented.

Possible update types may include:

- representation update;
- parameter update;
- topology-control update;
- boundary-condition update;
- dynamical forcing input;
- another explicitly typed EIF update.

No universal update type is assumed.

## 34. Reverse Mapping Does Not Imply Physical Force

If:

`u_E`

is not explicitly force-valued, then:

`u_E ≠ force`

The same applies to energy, stress, displacement, velocity, and other physical quantities.

## 35. Reverse Mapping Does Not Imply Energy

A scalar TR output is not an energy correction merely because it is scalar.

An energy-valued feedback mapping must have an energy codomain and compatible units.

## 36. Reverse Mapping Does Not Imply Geometry

A ternary state does not define a coordinate displacement directly.

Any geometry update requires an explicit map into the appropriate geometric space.

## 37. Reverse Mapping Does Not Imply Bonding

A TR state does not create, remove, or classify a chemical bond automatically.

Any bonding interpretation requires an independently defined physical criterion.

## 38. EIF State Update

Let:

`Ψ_E`

denote the EIF state-update relation receiving:

`u_E`

where feedback is defined.

A discrete specialization may use:

`s_E[n + 1] = Ψ_E(s_E[n], u_E[n], x_E[n], h_E[n], λ_E)`

This notation does not impose a universal EIF dynamical law.

## 39. Complete Coupled State

A minimal coupled state may be represented as:

`S_C = S_EIF × S_TR × H_C`

where:

`H_C`

contains cross-layer retained history not already included in the component states.

A coupled state satisfies:

`s_C ∈ S_C`

## 40. Product Space Does Not Define Coupling

The expression:

`S_C = S_EIF × S_TR × H_C`

defines a state container.

It does not define:

- forward mapping;
- feedback mapping;
- timing;
- causality;
- update order;
- synchronization;
- physical interpretation.

These require separate definitions.

## 41. Coupled Parameter Space

Define:

`Λ_C = Λ_EIF × Λ_TR × Λ_E→T × Λ_T→E × Λ_X`

where:

`Λ_X`

contains additional explicitly cross-layer parameters where required.

A specialization may omit unused factors.

## 42. External Input Space

Let:

`X_C,in`

denote external inputs to the complete coupled system.

These inputs remain distinct from internal EIF-to-TR and TR-to-EIF communication.

## 43. External Output Space

Let:

`Y_C,out`

denote observable outputs of the integrated system.

An integrated observable mapping may be:

`O_C: S_C → Y_C,out`

## 44. Internal Interface Is Not External Observable

A cross-layer intermediate may remain internal.

Therefore:

`internal interface value ≠ public observable`

unless explicitly exposed by `O_C`.

## 45. Cross-Layer Timing

An integration specialization must define when forward and reverse mappings are evaluated.

Possible mathematical structures include:

- synchronous discrete updates;
- asynchronous event updates;
- continuous coupling;
- sampled coupling;
- multirate coupling.

No one timing model is universal.

## 46. Update Order

If update order affects future state, the order is part of the model.

For example:

`EIF → TR → EIF`

and:

`TR → EIF → TR`

are not automatically equivalent.

## 47. Simultaneous Update Boundary

A simultaneous mathematical update must be distinguished from sequential numerical evaluation.

Implementation order must not silently alter the declared model.

## 48. Multirate Boundary

If EIF and TR evolve at different rates, the integration contract must define:

- sampling;
- holding;
- interpolation;
- aggregation;
- synchronization points;
- history retention.

## 49. Delay Boundary

A delayed cross-layer mapping must represent delay explicitly.

A delay may require:

`h_ET`

or:

`h_TE`

to retain earlier values.

Delay is not phase lag.

## 50. Phase-Lag Boundary

A phase lag modifies a phase relation.

It does not automatically represent transmission or processing delay.

Therefore:

`delay ≠ phase lag`

## 51. Memory Boundary

Cross-layer memory exists when future integration output depends on retained past state beyond the current source values.

Such memory must belong to declared history state.

## 52. Hysteresis Boundary

If the forward or reverse map depends on path history, the corresponding hysteresis state must be explicit.

A static threshold does not represent hysteresis by itself.

## 53. Locality Contract

Every cross-layer map must define its locality.

Possible locality classes include:

- site-local;
- neighborhood-local;
- cluster-local;
- scale-local;
- global.

The class must correspond to an actual dependency relation.

## 54. Site Correspondence

If EIF sites and TR components are associated, define a correspondence relation:

`C_site ⊆ I_EIF × I_TR`

where:

- `I_EIF` is the relevant EIF object index set;
- `I_TR` is the relevant TR component index set.

No one-to-one correspondence is assumed.

## 55. Atom-to-Oscillator Non-Identity

Even when:

`C_site`

contains one pair per atom, the relation does not establish:

`atom = oscillator`

An oscillator is a TR model object with independently defined state and dynamics.

## 56. Local Environment-to-TR Mapping

A local EIF environment:

`e_i ∈ X_env`

may contribute to a TR input only through an explicit mapping.

The mapping must state whether it uses:

- invariant channels;
- equivariant channels;
- geometric channels;
- topology channels;
- multiscale channels;
- physical-output channels.

## 57. Locality Expansion

A mapping may enlarge the effective dependency region.

If a TR component receives an aggregated EIF neighborhood, its locality is the complete source region used by that aggregation.

## 58. Global Aggregation

A global EIF observable may feed a global TR component only through a declared mapping.

The aggregation may destroy site-resolved information.

That loss must be recorded.

## 59. Scale Contract

Let:

`L_E`

be the relevant EIF scale set.

Let:

`L_T`

be the relevant TR scale set.

A cross-layer scale relation may be represented by:

`C_scale ⊆ L_E × L_T`

The relation may be one-to-one, one-to-many, many-to-one, or partial.

## 60. Scale Identity Is Preserved Until Mapped

An EIF scale and a TR scale are not identical merely because both are called local, cluster, or global.

Scale correspondence requires:

`C_scale`

or another explicit map.

## 61. Multiscale Reduction

A many-to-one scale mapping must define its reduction operation.

Examples may include:

- invariant aggregation;
- weighted projection;
- learned projection;
- selected-channel routing.

No universal reduction is defined.

## 62. Multiscale Expansion

A one-to-many mapping must define how one source value is distributed across target scales.

Replication, interpolation, and learned expansion are distinct operations.

## 63. Dimensional Contract

Every cross-layer quantity must have declared dimensional status.

Let:

`dim(y)`

denote the physical dimension of a dimensional quantity where defined.

A mapping must not add or compare dimensionally incompatible quantities.

## 64. Dimensionless TR Coordinates

If a TR input coordinate is dimensionless while its EIF source is dimensional, the forward mapping must include an explicit dimensional transformation.

A raw dimensional value cannot be silently inserted into a dimensionless coordinate.

## 65. Normalization

A normalization mapping may be written:

`N: Y_phys → Y_norm`

Its contract must define:

- reference scale;
- units;
- zero point where relevant;
- parameter provenance;
- valid domain.

Normalization does not erase the physical meaning of the source.

## 66. Dimensional Reconstruction

If reverse feedback reconstructs a dimensional EIF quantity from dimensionless TR output, the reverse map must restore compatible dimensions explicitly.

## 67. Numerical Sign Boundary

For a scalar EIF value:

`a ∈ ℝ`

the sign of `a` does not automatically determine ternary polarity.

Therefore:

`a < 0` does not imply `-1`

`a = 0` does not imply active neutral `0`

`a > 0` does not imply `1`

A sign-based classifier is admissible only if explicitly defined as a model mapping.

## 68. Physical Zero Boundary

A zero-valued EIF quantity remains typed by its own space.

Examples:

- zero force;
- zero velocity;
- zero stress;
- zero displacement;
- zero latent component.

None is automatically the TR active neutral state.

## 69. Active Neutral Boundary

TR active neutral `0` is an element of:

`T = {-1, 0, 1}`

Its semantics derive from TR execution.

It is not a generic numerical zero.

## 70. Missing Data Boundary

Missing EIF data must not be mapped implicitly to TR `0`.

Missing data require separate validity semantics.

## 71. Invalid Data Boundary

An invalid EIF source state must not silently become a valid TR input.

The admissible domain:

`D_E→T`

must exclude or explicitly handle invalid inputs.

## 72. Representation Transformation Contract

Suppose an EIF output channel belongs to a representation space:

`Y_E`

with group action:

`ρ_E(g)`

The forward mapping must define how this transformation behavior relates to the target TR input space.

## 73. TR Input Transformation Action

If the TR input participates in a symmetry claim, define:

`ρ_T,in(g): X_TR,in → X_TR,in`

for the relevant transformation group or set.

Without this action, cross-layer equivariance is undefined.

## 74. Cross-Layer Equivariance

A forward map is equivariant with respect to declared actions when:

`M_E→T(ρ_E(g)y_E, transformed history, λ_ET)`

equals:

`ρ_T,in(g) M_E→T(y_E, h_ET, λ_ET)`

under the declared transformation of all participating state.

The exact history action must be defined when history is present.

## 75. Cross-Layer Invariance

If the TR input is intended to be invariant under a transformation, then the target action may be the identity.

In that case the mapping must satisfy the corresponding invariance relation.

## 76. Equivariance Is Not Automatic Under Projection

A projection from an equivariant EIF representation to TR input can:

- preserve equivariance;
- produce an invariant;
- break symmetry.

The outcome depends on the mapping.

## 77. Invariant Contraction

An equivariant representation may be reduced to an invariant quantity through an explicitly invariant contraction.

This operation is generally information-losing.

## 78. Orientation-Sensitive TR Input

If a TR input intentionally retains orientation-dependent information, its transformation action must be defined.

A coordinate-dependent value cannot be called invariant merely because it is numerically stable in one frame.

## 79. Permutation Contract

If the EIF source is site-indexed, permutation behavior must be defined through the EIF permutation action.

The forward map must define whether TR components:

- permute correspondingly;
- aggregate invariantly;
- use canonicalized indexing;
- follow another explicit rule.

## 80. Permutation Invariance Versus Equivariance

A global TR input may be permutation invariant.

A site-indexed TR input may be permutation equivariant.

These are different claims.

## 81. Translation Contract

If EIF geometry is translated globally, the forward mapping must preserve the declared translation behavior.

Relative geometric descriptors may be invariant even when raw coordinates are not.

## 82. Rotation Contract

For:

`R ∈ SO(3)`

the mapping must define whether target channels are:

- rotation invariant;
- rotation equivariant;
- intentionally frame-dependent.

## 83. Reflection Contract

If reflection behavior matters, `O(3)` or `E(3)` actions must be defined separately from proper rotations.

Passing rotational validation does not establish reflection behavior.

## 84. Geometry Does Not Flip Ternary Polarity Automatically

A rotation, translation, reflection, or permutation does not automatically map:

`-1 ↔ 1`

The ternary transformation rule must be independently defined.

## 85. Information-Loss Contract

For every forward mapping, define whether it is:

- injective;
- many-to-one;
- approximately invertible;
- invariant under a declared equivalence relation;
- intentionally lossy.

## 86. Lossy Mapping Boundary

If:

`M_E→T(y_a) = M_E→T(y_b)`

for distinct admissible EIF outputs:

`y_a ≠ y_b`

then the TR input cannot distinguish those source states through that mapping alone.

## 87. Feedback Reconstruction Boundary

A lossy forward mapping cannot generally be inverted by reverse feedback.

Therefore:

`M_T→E ≠ M_E→T^(-1)`

unless invertibility has been established.

## 88. Bidirectional Coupling Is Not Inversion

Forward and reverse integration mappings serve different roles.

A bidirectional architecture does not require them to be mathematical inverses.

## 89. Cross-Layer Causality

An integration specialization must state which state can affect which future state.

A feedback loop introduces causal dependence beyond one-way feature extraction.

## 90. One-Way Integration

A one-way architecture has:

`EIF → TR`

without:

`TR → EIF`

In this case TR observes or processes EIF-derived information without modifying EIF evolution through the integration layer.

## 91. Bidirectional Integration

A bidirectional architecture has:

`EIF → TR`

and:

`TR → EIF`

through separately typed mappings.

The existence of both directions creates a coupled dynamical system.

## 92. Coupled Update Operator

For a discrete bidirectional specialization, define a complete update operator:

`Φ_C: S_C × X_C,in × Λ_C → S_C`

such that:

`s_C[n + 1] = Φ_C(s_C[n], x_C[n], λ_C)`

The operator must encode the declared update order and cross-layer history.

## 93. Coupled Continuous Dynamics

A continuous-time specialization may define a coupled differential or differential-algebraic system.

The existence of such a specialization does not make continuous time mandatory for TR-EIF.

## 94. Hybrid Integration

Because TR may contain discrete ternary execution while EIF may contain continuous dynamics, the integrated system may be hybrid.

A hybrid specialization must define:

- continuous state;
- discrete state;
- guards;
- reset or update relations;
- event timing;
- retained history.

## 95. Continuous EIF and Discrete TR Remain Distinct

A continuous EIF variable does not become ternary merely because it drives a ternary target.

The classifier or mapping is the boundary between spaces.

## 96. Discrete TR Feedback and Continuous EIF Remain Distinct

A discrete ternary state does not become a continuous physical variable merely because it modulates one.

The reverse map defines the continuous effect.

## 97. Cross-Layer Target

A forward mapping may contribute to a TR target-generation process.

The resulting target remains a TR object.

It is not an executed EIF action.

## 98. Cross-Layer Guard

A specialization may define integration-specific admissibility guards before a source value is accepted by TR.

Such guards are distinct from the internal ternary transition guard.

## 99. Guard Composition

If both integration and TR execution guards exist, both must be represented.

Passing the cross-layer guard does not authorize a forbidden ternary transition.

## 100. Cross-Layer Saturation

If an integration mapping saturates or clips values, the saturation operation must be explicit.

Saturation changes the mapping and may create information loss.

## 101. Cross-Layer Capacity

If only a finite number of cross-layer requests can be processed per update, capacity is part of the integration model.

Capacity limits must not be hidden as implementation accidents.

## 102. Routing

When multiple EIF channels feed multiple TR components, routing must be represented explicitly.

A routing relation may depend on:

- site correspondence;
- topology;
- scale;
- channel type;
- scheduler state;
- another declared condition.

## 103. Routing Does Not Define Physics

Computational routing determines information flow.

It does not by itself establish physical interaction.

## 104. Cross-Layer Topology

Let:

`G_X`

denote a cross-layer interaction graph where a graph representation is used.

Its vertices may include EIF and TR objects.

Its edges represent declared cross-layer dependencies.

An edge does not automatically represent:

- chemical bond;
- mechanical force;
- energy interaction;
- physical contact.

## 105. Dynamic Cross-Layer Topology

If `G_X` changes with state, the update rule for cross-layer topology must be explicit.

Topology history may become part of the coupled state when future evolution depends on it.

## 106. Resonance Is Not Frequency Equality

The integration layer inherits:

`resonance ≠ frequency equality`

No EIF frequency-like quantity becomes resonant merely by matching a TR frequency.

## 107. Resonance Is Not Synchronization

The integration layer inherits:

`resonance ≠ synchronization`

A synchronized cross-layer signal does not establish resonance by itself.

## 108. Synchronization Is Not Phase Locking

The integration layer inherits:

`synchronization ≠ phase locking`

The exact relation depends on the selected dynamical definitions.

## 109. Phase Locking Is Not Resonance

A stable phase relation does not automatically establish a TR resonance-window condition.

## 110. Coherence Is Not Uniformity

Cross-layer coherence does not require every component to have identical state.

## 111. Coherence Is Not Resonance

A coherent integrated trajectory does not automatically lie inside a resonance window.

## 112. Phase Order Is Not Complete Coherence

Where phase order `R(t)` is used:

`R(t) ≠ C(t)`

unless a specialization explicitly defines an equality, which is not inherited from the closed TR theory.

## 113. Oscillator Phase Is Not Physical Phase of Matter

An oscillator phase variable remains a dynamical coordinate.

It is not automatically a thermodynamic or structural phase of the interatomic system.

## 114. Phase Coupling Is Not Mechanical Force

A TR phase-coupling term does not become an EIF mechanical force without an explicit force-valued mapping.

## 115. Phase Relation Is Not Chemical Bond

A phase relation between TR components does not establish a chemical bond between atoms.

## 116. Ternary State Is Not Energy

The states:

`-1`

`0`

`1`

are not energy values.

## 117. Resonance Classification Is Not Energy

`OUTSIDE`, `BOUNDARY`, and `INSIDE` are classification values, not energies.

## 118. Resonance-Window Crossing Is Not Bifurcation

The integration layer preserves:

`resonance-window crossing ≠ bifurcation`

## 119. Bifurcation Is Not Ternary Transition

The integration layer preserves:

`bifurcation ≠ ternary transition`

## 120. Ternary Transition Is Not Structural Transition

The integration layer preserves:

`ternary transition ≠ structural transition`

## 121. Structural Transition Is Not Physical Phase Transition

The integration layer preserves:

`structural transition ≠ physical phase transition`

A coupled model requires independent evidence before a physical phase-transition claim is made.

## 122. Integration-Induced Bifurcation Boundary

Cross-layer feedback may change the dynamical system and may, in a specific model, alter its bifurcation structure.

A named bifurcation requires class-specific mathematical evidence.

It cannot be assigned from threshold crossings, scheduler events, or visual inspection alone.

## 123. Integration-Induced Structural Change Boundary

A structural change in EIF state caused by feedback is a structural event under its declared criterion.

It is not automatically a physical phase transition.

## 124. Physical Interpretation Contract

Every cross-layer physical claim must identify:

- the physical source quantity;
- units;
- mapping;
- target quantity;
- symmetry behavior;
- calibration or derivation;
- validation evidence;
- domain of applicability.

## 125. Latent Representation Boundary

An EIF latent representation has mathematical transformation semantics.

It does not acquire a direct physical meaning unless such meaning is independently defined.

## 126. Learned Mapping Boundary

A learned `M_E→T` or `M_T→E` is an implementation/model mapping.

Its learned parameters require provenance.

Training performance does not establish universal physical law.

## 127. Calibrated Mapping Boundary

A calibrated cross-layer mapping is valid within the scope of its calibration evidence.

Calibration must not be presented as a derivation from first principles unless it actually is one.

## 128. Derived Mapping Boundary

A derived mapping must identify the definitions and assumptions from which it follows.

The derivation scope remains part of the claim.

## 129. Author-Defined Mapping Boundary

An author-defined integration mapping may be mathematically valid as a framework definition without being an established physical law.

Its provenance must remain:

`AUTHOR_DEFINED`

unless stronger evidence is independently supplied.

## 130. Provenance Contract

Cross-layer objects use the inherited provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

## 131. Parameter Provenance

Every cross-layer parameter that affects results must have an applicable provenance class.

A numeric constant without provenance is insufficient for a publication-ready integration specification.

## 132. Observable Provenance

An observable derived from state may use:

`DERIVED`

when the derivation is exact.

An empirically calibrated observable relation requires:

`CALIBRATED`

or another appropriate provenance class.

## 133. Integration Validation Result

The integration layer inherits the validation result space:

`X_Val = {PASS, FAIL, UNRESOLVED}`

These are validation statuses.

They are not ternary states.

## 134. Validation Status Is Not Balanced Ternary

The identifications:

`FAIL = -1`

`UNRESOLVED = 0`

`PASS = 1`

are forbidden.

## 135. Integration Claim Space

Let:

`Q_X`

denote the set of integration claims.

Examples include:

- dimensional compatibility;
- cross-layer equivariance;
- site correspondence;
- scale correspondence;
- target/executed-state separation;
- feedback correctness;
- deterministic replay;
- integrated physical accuracy.

## 136. Integration Evidence

For:

`q ∈ Q_X`

define an evidence space:

`E_q`

containing the state, parameters, transformations, traces, references, and tolerances required by the claim.

## 137. Integration Validator

Define:

`V_q: E_q → X_Val`

for each declared integration claim.

The validator must state the conditions for:

- `PASS`;
- `FAIL`;
- `UNRESOLVED`.

## 138. Exact Integration Validation

Exact validation applies to discrete structural invariants such as:

- valid index correspondence;
- valid state membership;
- forbidden-transition absence;
- exact routing relation;
- exact categorical mapping where specified.

## 139. Numerical Integration Validation

Numerical validation requires a declared metric or norm and tolerance.

Tolerance-based equality does not redefine exact mathematical equality.

## 140. Cross-Layer Equivariance Validation

For a memoryless forward map, an equivariance residual may compare:

`M_E→T(ρ_E(g)y_E)`

with:

`ρ_T,in(g)M_E→T(y_E)`

using the declared target-space metric.

For history-dependent mappings, transformed history must also be included.

## 141. Dimensional Validation

Dimensional validation verifies that cross-layer transformations are dimensionally admissible.

Numerical finite values do not establish dimensional compatibility.

## 142. Locality Validation

Locality validation must verify the complete source dependency region of each target channel.

## 143. Scale Validation

Scale validation must verify that every source-target scale relation follows the declared scale contract.

## 144. Information-Loss Validation

Where a mapping claims invertibility, sufficiency, or preservation of a property, that claim requires separate validation.

A lossy mapping must not be described as information-preserving.

## 145. Target/Execution Validation

An integrated trace must preserve the distinction between:

- EIF-derived input;
- TR target;
- executed TR state;
- pending route where applicable.

A trace that collapses these fields cannot validate neutral-mediated execution fully.

## 146. Feedback Validation

Feedback validation must identify:

- TR source output;
- reverse mapping;
- EIF update;
- resulting EIF state;
- timing;
- units;
- transformation behavior.

## 147. Integrated Symmetry Validation

Independent EIF equivariance does not prove integrated equivariance.

The complete chain:

`EIF state`

`→ EIF output`

`→ M_E→T`

`→ TR dynamics`

`→ M_T→E`

`→ EIF update`

must satisfy the declared integrated symmetry relation where such a claim is made.

## 148. Integrated Physical Validation

Independent correctness of TR and EIF layers does not establish physical correctness of their coupling.

Physical validation requires evidence from the coupled specialization.

## 149. Integrated Dynamic Validation

A coupled trajectory claim requires validation of the complete coupled evolution law.

Isolated trajectory validation of one layer is insufficient.

## 150. Integrated Replay

Deterministic replay requires preservation of all result-affecting:

- EIF state;
- TR state;
- cross-layer history;
- parameters;
- topology;
- timing state;
- scheduler state where used;
- external inputs;
- stochastic state where applicable.

## 151. Cross-Layer Trace

A complete integration trace must preserve enough information to reconstruct the causal sequence relevant to the validated claim.

Possible trace fields include:

- EIF source state identifier;
- EIF output channel;
- forward-map input;
- forward-map output;
- TR target;
- TR executed state;
- pending route;
- TR output;
- reverse-map output;
- EIF update;
- resulting EIF state.

No universal serialization format is imposed here.

## 152. Trace Resolution

Trace resolution must be sufficient to distinguish separate events.

In particular, opposite ternary transition legs must not be collapsed into one trace event.

## 153. Integration State Versus Observable

A cross-layer observable does not replace coupled state.

A state variable that affects future evolution must be retained in the state contract.

## 154. Integration Closure Criterion

An integrated specialization is formally closed when:

- both component layers are individually closed;
- forward mappings are typed;
- reverse mappings are typed where used;
- cross-layer history is explicit;
- timing semantics are explicit;
- locality is explicit;
- scale relations are explicit;
- dimensional behavior is explicit;
- transformation behavior is explicit;
- information loss is explicit;
- target and execution remain distinct;
- active-neutral invariants are preserved;
- observables and traces are defined;
- validation claims and evidence are defined.

## 155. Integration Does Not Require Bidirectional Feedback

A one-way specialization may be formally complete when no reverse influence is part of its declared system.

Bidirectionality is required only when the model claims feedback.

## 156. Integration Does Not Require Kuramoto–Sakaguchi

The Kuramoto–Sakaguchi module is one optional classical phase module inside TR.

TR-EIF integration does not require every specialization to use it.

## 157. Integration Does Not Require Machine Learning

EIF representations or cross-layer mappings may be analytical, algorithmic, learned, calibrated, or hybrid.

TR-EIF is not defined as a machine-learning framework.

## 158. Integration Does Not Require One Interatomic Potential

EIF can support different independently defined physical-output mappings.

TR-EIF is not defined by one interatomic potential.

## 159. Integration Does Not Require One Resonance Coordinate

`X_R`

may be multidimensional.

The integration architecture must not reduce resonance universally to one frequency or one scalar.

## 160. Integration Does Not Require One Scale

Both EIF and TR may be multiscale.

Cross-layer mappings must preserve or explicitly transform scale information.

## 161. Integration Does Not Require One-to-One Site Mapping

An EIF local environment may feed:

- one TR component;
- several TR components;
- an aggregate TR component.

Likewise, one TR component may receive information from multiple EIF objects.

The mapping must define the relation.

## 162. Integration Does Not Imply Atomic Oscillators

TR components may correspond to:

- sites;
- local environments;
- clusters;
- modes;
- abstract resonant components;
- another declared object.

The integration specialization must define the correspondence.

## 163. Integration Does Not Imply Mechanical Resonance

A TR resonance relation is a model-defined relation in resonance-coordinate space.

It is not automatically mechanical resonance of atoms.

## 164. Integration Does Not Imply Chemical Bonding

No cross-layer phase relation, resonance classification, or ternary state is a chemical bond by default.

## 165. Integration Does Not Imply Thermodynamic Phase

No TR phase variable or ternary state is a thermodynamic phase of matter by default.

## 166. Integration Does Not Imply Force

No cross-layer signal becomes mechanical force without a force-valued mapping.

## 167. Integration Does Not Imply Energy

No cross-layer scalar becomes energy without an energy-valued mapping.

## 168. Integration Does Not Imply Universal Physics

A mathematically closed integration architecture is not automatically a universal physical theory.

Physical scope requires independent evidence.

## 169. Core Cross-Layer Invariants

The following invariants are mandatory.

1. `TR ≠ EIF`.

2. `S_TR ≠ S_EIF` in general.

3. `Y_EIF,out ≠ X_TR,in` in general.

4. Every EIF-to-TR relation requires an explicit typed mapping.

5. Every TR-to-EIF feedback relation requires an explicit typed mapping.

6. Forward and reverse mappings are not assumed to be inverses.

7. Atom is not automatically oscillator.

8. Local environment is not automatically phase.

9. Equivariant feature is not automatically resonance coordinate.

10. Energy is not resonance state.

11. Force is not resonance state.

12. Stress is not resonance classification.

13. Topology is not ternary state.

14. Numerical sign is not ternary polarity.

15. Physical zero is not active neutral `0`.

16. Missing data are not active neutral `0`.

17. Resonance classification is not ternary state.

18. Ternary target is not executed ternary state.

19. Direct `-1 → 1` execution is forbidden.

20. Direct `1 → -1` execution is forbidden.

21. Opposite transitions require active-neutral mediation.

22. Each transition leg is a separate event.

23. First-leg execution does not authorize second-leg execution automatically.

24. Neutral retention remains admissible unless a stronger model rule is defined.

25. Cross-layer mapping cannot bypass TR execution invariants.

26. Delay is not phase lag.

27. Memory is not missing state.

28. Local state is not global state.

29. EIF scale is not TR scale without explicit correspondence.

30. Dimensional quantities require dimensional compatibility.

31. Equivariance is not physical correctness.

32. Integration can break equivariance.

33. Integration can break conservativity.

34. Integration can introduce memory.

35. Integration can introduce delay.

36. Integration can introduce new nonlinear dynamics.

37. Independent layer validation does not prove integrated validation.

38. Schema validity does not prove integration correctness.

39. Numerical stability does not prove physical validity.

40. Benchmark success does not prove universal physical validity.

## 170. Formal Non-Equivalences

The following non-equivalences remain mandatory:

`TR ≠ EIF`

`EIF output ≠ TR input automatically`

`TR input ≠ TR state`

`resonance state ≠ resonance classification`

`resonance classification ≠ ternary state`

`ternary target ≠ executed ternary state`

`active neutral 0 ≠ missing data`

`active neutral 0 ≠ physical zero`

`atom ≠ oscillator`

`local environment ≠ oscillator phase`

`equivariant representation ≠ resonance coordinate`

`energy ≠ resonance`

`force ≠ resonance`

`stress ≠ resonance classification`

`topology ≠ ternary state`

`sign ≠ ternary polarity`

`delay ≠ phase lag`

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`independent TR validation + independent EIF validation ≠ integrated validation`

## 171. Minimal Forward Integration Contract

Every forward integration mapping must define:

1. EIF source space;
2. EIF source channels;
3. admissible domain;
4. TR target input space;
5. mapping;
6. units;
7. transformation actions;
8. locality;
9. scale;
10. history dependence;
11. parameters;
12. information loss;
13. provenance;
14. validation relation.

## 172. Minimal Reverse Integration Contract

Every reverse feedback mapping must define:

1. TR source-output space;
2. EIF state context;
3. admissible domain;
4. EIF update space;
5. mapping;
6. units;
7. transformation actions;
8. locality;
9. scale;
10. history dependence;
11. parameters;
12. update semantics;
13. provenance;
14. validation relation.

## 173. Minimal Coupled-State Contract

Every bidirectionally coupled specialization must define:

1. `S_EIF`;
2. `S_TR`;
3. cross-layer history;
4. complete coupled state;
5. forward mapping;
6. reverse mapping;
7. update order;
8. external inputs;
9. parameters;
10. observables;
11. traces;
12. validation.

## 174. Minimal Symmetry Contract

Every integrated equivariance claim must define:

1. transformation group or set;
2. EIF source action;
3. TR input action;
4. TR state/output action where relevant;
5. EIF feedback-target action;
6. complete cross-layer relation;
7. exact or numerical validation criterion.

## 175. Minimal Dimensional Contract

Every dimensional cross-layer mapping must define:

1. source units;
2. source dimension;
3. normalization or dimensional transformation;
4. target dimensional status;
5. reverse dimensional reconstruction where used;
6. parameter units;
7. validation.

## 176. Minimal Locality Contract

Every cross-layer mapping must define:

1. source object set;
2. target object set;
3. dependency relation;
4. aggregation where used;
5. routing where used;
6. effective receptive region;
7. validation.

## 177. Minimal Scale Contract

Every multiscale cross-layer mapping must define:

1. EIF scale set;
2. TR scale set;
3. scale correspondence;
4. reduction or expansion mapping;
5. information loss;
6. transformation behavior;
7. validation.

## 178. Minimal Integration Validation Contract

Every integration claim must define:

1. claim;
2. scope;
3. evidence;
4. validator;
5. result space;
6. exact or numerical criterion;
7. tolerance where applicable;
8. provenance;
9. unresolved condition.

## 179. Formal Integration Chain

The minimal one-way chain is:

`S_EIF`

`→ O_E`

`→ Y_EIF,out`

`→ M_E→T`

`→ X_TR,in`

`→ TR evolution`

`→ resonance coordinates`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated ternary execution`

`→ Y_TR,out`

The mapping boundaries remain explicit.

## 180. Formal Bidirectional Chain

Where feedback is defined:

`S_EIF`

`→ EIF output`

`→ M_E→T`

`→ TR input`

`→ TR state evolution`

`→ resonance state`

`→ ternary target`

`→ active-neutral execution`

`→ TR output`

`→ M_T→E`

`→ EIF update`

`→ updated S_EIF`

This creates a coupled system without identifying the component state spaces.

## 181. Formal Hybrid-State Chain

For a hybrid specialization:

`continuous EIF state`

`+`

`continuous TR state where used`

`+`

`discrete TR state`

`+`

`cross-layer history`

`→ guards`

`→ continuous evolution`

`→ discrete events`

`→ cross-layer updates`

`→ retained coupled state`

All continuous and discrete components remain typed separately.

## 182. Integration Readiness of EIF

EIF is integration-ready for a selected channel only when that channel has:

- defined source state;
- defined codomain;
- known units;
- known locality;
- known scale;
- known transformation behavior;
- known information-loss semantics;
- provenance;
- validation status.

## 183. Integration Readiness of TR

TR is integration-ready for a selected input only when that input has:

- defined input space;
- admissible domain;
- state-update role;
- resonance-mapping role where applicable;
- transformation semantics where claimed;
- dimensional status;
- validation semantics.

## 184. Cross-Layer Readiness

The two layers are cross-layer ready only when a valid mapping exists between their compatible declared interfaces.

Independent readiness does not itself define the mapping.

## 185. No Semantic Collapse at the Interface

The interface must preserve the sequence:

`source object`

`→ mapping`

`→ target object`

The mapping cannot be removed from the specification merely because the source and target have equal dimensions.

## 186. No Dimensional Collapse at the Interface

Equal array shape does not establish dimensional compatibility.

## 187. No Symmetry Collapse at the Interface

Equal array shape does not establish equal transformation behavior.

## 188. No Locality Collapse at the Interface

Equal array shape does not establish equal locality.

## 189. No Scale Collapse at the Interface

Equal array shape does not establish equal scale.

## 190. No Physical Collapse at the Interface

Equal numerical values do not establish equal physical meaning.

## 191. Integration Foundation Closure

This chapter closes the foundational integration boundary when the following objects are available for a specialization:

`S_EIF`

`Y_EIF,out`

`M_E→T`

`X_TR,in`

`S_TR`

`Y_TR,out`

and, where feedback exists:

`M_T→E`

`U_E`

together with:

- cross-layer history;
- parameters;
- timing;
- locality;
- scale;
- dimensional semantics;
- transformation semantics;
- provenance;
- validation.

## 192. Final Integration-Foundation Statement

The TR-EIF integration layer begins only after the Ternary Resonant and Equivariant Interatomic layers have been independently formalized.

Its foundational relation is not identity.

It is typed composition:

`interatomic state`

`→ EIF representation`

`→ EIF output`

`→ explicit EIF-to-TR mapping`

`→ TR input`

`→ resonance coordinates`

`→ resonance classification`

`→ ternary target`

`→ active-neutral -1/0/1 execution`

and, where feedback is defined:

`TR output`

`→ explicit TR-to-EIF mapping`

`→ EIF update`

`→ updated interatomic state`

The balanced ternary kernel remains exactly:

`-1/0/1`

with active neutral:

`0`

and mandatory opposite-state mediation:

`-1 → 0 → 1`

`1 → 0 → -1`

No EIF quantity is identified automatically with resonance, ternary polarity, force, energy, bond, oscillator phase, or physical phase of matter.

No TR quantity is identified automatically with an interatomic physical quantity.

Every cross-layer relation must therefore specify:

- source;
- target;
- mapping;
- dimensions;
- transformation behavior;
- locality;
- scale;
- information loss;
- state-update semantics;
- provenance;
- validation.

This typed separation is the mathematical condition that allows TR and EIF to form one integrated architecture without destroying the invariants of either closed layer.
