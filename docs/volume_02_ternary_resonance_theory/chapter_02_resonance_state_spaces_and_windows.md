# Resonance State Spaces and Windows

## 1. Purpose

This document defines the resonance-state geometry used by the Ternary Resonant Equivariant Interatomic Framework.

The chapter formalizes:

- resonance-coordinate spaces;
- resonance-coordinate states;
- admissible resonance regions;
- finite resonance windows;
- resonance-window boundaries;
- interior, boundary, and exterior states;
- local and global resonance spaces;
- coupled resonance spaces;
- time-dependent resonance windows;
- state-dependent resonance windows;
- history-dependent resonance regions;
- hysteretic entry and exit regions;
- residence regions;
- multiscale resonance spaces;
- uncertainty-aware resonance regions;
- numerical representations of resonance boundaries;
- resonance-state observability;
- resonance-state validation.

The purpose is to establish the state-space structure required before model-specific resonance dynamics or resonance-driven ternary transitions are introduced.

## 2. Status of This Document

This chapter belongs to the TR-EIF author-defined formal layer.

It specializes the mathematical state-space, topology, mapping, and invariant structures established in Volume 01.

It also depends on:

`chapter_01_ternary_resonance_formalism.md`

No universal resonance frequency, coupling constant, threshold, material coefficient, or empirical parameter is introduced here.

All model-specific numerical boundaries remain subject to explicit provenance.

## 3. Dependency Structure

The resonance-state construction follows:

`system state S`

`→ resonance-coordinate mapping P_R`

`→ resonance-coordinate state r`

`→ resonance-coordinate space X_R`

`→ admissible resonance domain X_R,adm`

`→ resonance window W_R`

`→ boundary ∂W_R`

`→ classification`

The construction order is mandatory.

A resonance window cannot be defined before its coordinate space is defined.

## 4. Resonance-Coordinate Space

The resonance-coordinate space is:

`X_R`

A resonance-coordinate state is:

`r ∈ X_R`

The mapping into resonance space is:

`P_R: S × P → X_R`

with:

`r = P_R(S, p)`

where:

- `S` is the declared model state;
- `P` is the declared parameter space;
- `p ∈ P`;
- `P_R` is the resonance-coordinate mapping.

## 5. Resonance Coordinates

A resonance-coordinate state may contain one or more declared coordinates.

A generic finite-dimensional representation may be written as:

`r = (r_1, r_2, ..., r_m)`

with:

`r_k ∈ X_R,k`

for each coordinate `k`.

The complete resonance-coordinate space is then:

`X_R = X_R,1 × X_R,2 × ... × X_R,m`

when a Cartesian-product representation is appropriate.

## 6. Coordinate Meaning

Every resonance coordinate must have explicit semantics.

A coordinate may represent a declared relation involving:

- frequency;
- phase;
- amplitude;
- coupling;
- delay;
- dissipation;
- topology;
- geometry;
- history;
- structural state;
- boundary state;
- external forcing;
- another defined dynamic variable.

A coordinate symbol without a declared meaning is not a complete resonance coordinate.

## 7. Coordinate Provenance

Every coordinate of `r` must identify whether it is:

- primitive;
- derived;
- measured;
- estimated;
- calculated;
- normalized;
- author-defined.

Derived coordinates must identify their source variables and mapping.

## 8. Coordinate Units

A dimensional resonance coordinate retains its physical units.

A dimensionless coordinate must identify the normalization or construction that makes it dimensionless.

Coordinates with incompatible physical dimensions must not be combined through ordinary Euclidean geometry unless an explicit normalization establishes compatibility.

## 9. Coordinate Range

Each coordinate has a declared admissible domain:

`X_R,k,adm ⊆ X_R,k`

The admissible global resonance domain is:

`X_R,adm ⊆ X_R`

A resonance-coordinate state outside the admissible domain is not automatically classified as nonresonant.

It is first an invalid or unsupported resonance state.

## 10. Resonance-State Validity

A valid resonance-coordinate state satisfies:

`r ∈ X_R,adm`

A state outside this region must be represented explicitly as:

- invalid;
- unsupported;
- out of domain;
- requiring extrapolation;

according to the model contract.

Out-of-domain state must not be silently classified as:

`OUTSIDE`

the resonance window.

## 11. Resonance Window

A resonance window is:

`W_R ⊂ X_R,adm`

The resonance window contains resonance-coordinate states satisfying the declared resonance relation.

The window may be:

- connected;
- disconnected;
- convex;
- non-convex;
- simply connected;
- multiply connected;

depending on the model.

No one geometry is imposed universally.

## 12. Finite Window Requirement

The TR-EIF resonance formalism treats a resonance window as a finite region of the declared coordinate space.

This means the resonance relation is represented through a bounded or otherwise explicitly delimited admissible region rather than through an unspecified exact matching statement.

The mathematical meaning of finite must be defined relative to the topology or metric used by the model.

## 13. Window Dimensionality

The dimensionality of:

`W_R`

is determined by its containing resonance-coordinate space.

For:

`X_R ⊆ ℝ^m`

a resonance window may occupy a region in `m`-dimensional coordinate space.

A model must not reduce an `m`-dimensional resonance condition to one coordinate without an explicit reduction.

## 14. One-Dimensional Resonance Window

A one-dimensional resonance window may be represented as an interval in a declared scalar coordinate.

This is a valid special case.

It is not the universal TR-EIF resonance structure.

## 15. Multidimensional Resonance Window

For:

`r = (r_1, ..., r_m)`

membership may depend jointly on several coordinates.

Therefore:

`r_1 inside its local range`

does not by itself imply:

`r ∈ W_R`

unless all required coordinate relations are satisfied.

## 16. Coupled Coordinates

A resonance window need not factorize into independent coordinate intervals.

In general:

`W_R ≠ W_1 × W_2 × ... × W_m`

unless the model explicitly defines independent coordinate conditions.

Coupled resonance geometry may therefore depend on relations among coordinates.

## 17. Resonance Boundary

The resonance-window boundary is:

`∂W_R`

It separates the declared interior and exterior under the topology of `X_R`.

A boundary state is not automatically an interior state or exterior state.

It has its own formal status when the classifier distinguishes boundary membership.

## 18. Resonance Interior

The interior of the resonance window is denoted conceptually by:

`Int(W_R)`

A state inside the resonance window satisfies:

`r ∈ Int(W_R)`

under the declared topology.

## 19. Resonance Exterior

A valid resonance-coordinate state outside the window and outside its boundary belongs to the exterior region.

The exterior region is restricted to valid resonance space.

Therefore:

`invalid state`

and:

`valid state outside W_R`

remain distinct.

## 20. Resonance Classification Space

The minimum resonance classification set is:

`R_C = {OUTSIDE, BOUNDARY, INSIDE}`

The classifier is:

`C_R: X_R,adm → R_C`

The classifier must operate only on valid resonance-coordinate states unless an explicit extended validity state is included.

## 21. Extended Classification State

A model may use a larger result structure that separates resonance classification from validity.

For example, a result may contain:

`(validity_state, resonance_class)`

This is preferable to encoding invalidity as one of:

`OUTSIDE`

`BOUNDARY`

or:

`INSIDE`.

## 22. Boundary Membership

A state belongs to the boundary when it satisfies the model's exact boundary definition.

Numerical proximity to the boundary is not identical to exact mathematical boundary membership.

The distinction between:

`r ∈ ∂W_R`

and:

`r numerically close to ∂W_R`

must be preserved.

## 23. Numerical Boundary Layer

A numerical implementation may define a tolerance region around the exact boundary.

Let:

`B_ε(∂W_R)`

denote a numerical boundary neighborhood under a declared metric and tolerance `ε`.

The tolerance:

`ε`

belongs to the numerical validation contract.

It is not part of the exact resonance-window definition unless the mathematical model explicitly incorporates it.

## 24. Boundary Tolerance Provenance

Every numerical boundary tolerance must have explicit provenance.

Possible states include:

- `DERIVED`;
- `CALIBRATED`;
- `TEST_FIXTURE`;
- `REQUIRES_TEST`;
- another provenance class defined in Volume 01.

An arbitrary software constant must not become a scientific resonance threshold silently.

## 25. Resonance Metric

A resonance-coordinate space may use a declared metric:

`d_R: X_R × X_R → ℝ₊`

The metric must identify:

- coordinate normalization;
- weighting;
- dimensional treatment;
- circular coordinates;
- discrete components where present.

No universal resonance metric is imposed.

## 26. Metric Independence of Membership

A resonance window may be defined without a metric when membership is established through other mathematical relations.

Therefore a metric is optional unless required by:

- boundary distance;
- nearest-region classification;
- uncertainty propagation;
- numerical tolerance;
- optimization;
- validation.

## 27. Circular Coordinates

When a resonance coordinate contains oscillator phase or phase difference, the corresponding coordinate belongs to circular rather than unrestricted linear geometry.

A phase coordinate must preserve its periodic equivalence.

A resonance-space metric containing phase must therefore respect circular distance.

## 28. Mixed Resonance Space

A resonance-coordinate space may contain different mathematical factors.

For example, it may combine:

- real-valued amplitude coordinates;
- circular phase coordinates;
- graph-derived coordinates;
- discrete structural labels;
- history-derived variables.

A mixed resonance space must preserve the mathematical type of every factor.

## 29. Hybrid Resonance Space

A resonance state may belong to a hybrid space such as:

`X_R = X_c × X_θ × X_g × X_h`

where the factors represent different declared coordinate classes.

The product representation does not imply that every factor can be combined through ordinary vector arithmetic.

## 30. Local Resonance Space

For site or component `i`, define:

`X_R,i`

with local state:

`r_i ∈ X_R,i`

and local resonance window:

`W_R,i ⊂ X_R,i`

A local resonance classifier is:

`C_R,i: X_R,i,adm → R_C`

## 31. Heterogeneous Local Spaces

Different component classes may use different local resonance-coordinate spaces.

Therefore:

`X_R,i`

and:

`X_R,j`

need not be identical.

A global aggregation must account for this difference explicitly.

## 32. Pairwise Resonance Space

For components `i` and `j`, define pairwise resonance space:

`X_R,ij`

with:

`r_ij ∈ X_R,ij`

and window:

`W_R,ij ⊂ X_R,ij`

Pairwise resonance may depend on quantities unavailable in either isolated local state.

## 33. Neighborhood Resonance Space

For a neighborhood `N_i`, define:

`X_R,N_i`

and:

`r_N_i ∈ X_R,N_i`

A neighborhood resonance state may depend on collective relations among more than two components.

It must not be reduced automatically to pairwise resonance.

## 34. Global Resonance Space

A global resonance state is:

`r_G ∈ X_R,G`

with global resonance window:

`W_R,G ⊂ X_R,G`

The corresponding mapping may be:

`P_R,G: S → X_R,G`

A global state may contain information not available from individual local classifiers.

## 35. Local and Global Classification

The statements:

`C_R,i(r_i) = INSIDE`

for every local component do not universally imply:

`C_R,G(r_G) = INSIDE`

Similarly, a global `INSIDE` classification does not require every local component to have identical classification.

## 36. Collective Resonance Region

A collective resonance region is defined over a state representing several interacting components.

Its membership may depend on:

- relative phases;
- coupling topology;
- cluster relations;
- spatial organization;
- delayed interactions;
- collective modes.

Collective resonance is therefore not the sum of independent local classifications unless a specific decomposition is established.

## 37. Product Resonance Window

If a model proves that resonance coordinates are independent for classification purposes, the window may factorize:

`W_R = W_1 × ... × W_m`

This factorization is a model property.

It must not be assumed merely because the state space is a Cartesian product.

## 38. Conditional Resonance Window

A resonance window may depend on additional state.

A conditional resonance window may be represented conceptually as:

`W_R(q)`

where:

`q`

is a declared conditioning state.

The conditioning state may include:

- structural form;
- topology;
- boundary state;
- interaction class;
- another explicitly defined variable.

## 39. Parameter-Dependent Resonance Window

A parameter-dependent resonance window may be written as:

`W_R(p)`

with:

`p ∈ P`

The parameter set must have declared provenance.

Two executions with different `p` may therefore use different valid resonance regions.

## 40. Time-Dependent Resonance Window

A time-dependent window may be represented as:

`W_R(t)`

Time dependence must correspond to a declared model dependency.

A window must not change merely because implementation code mutates an undocumented threshold.

## 41. State-Dependent Resonance Window

A state-dependent window may be:

`W_R(S)`

Such a model must avoid circular ambiguity between:

- state used to define the window;
- resonance state being classified;
- resulting state update.

The evaluation order must be explicit.

## 42. History-Dependent Resonance Window

A history-dependent resonance window may be:

`W_R(H_R)`

where:

`H_R`

is the declared resonance-history state.

Two identical instantaneous resonance-coordinate states may then have different effective admissibility or classification because their histories differ.

## 43. Entry Region

A hysteretic model may define an entry region:

`W_R,in`

A state satisfies resonance-entry conditions only when it meets the declared entry relation.

The entry region need not equal the retention region.

## 44. Retention Region

A resonance-retention region may be:

`W_R,hold`

A state already classified as resonant may remain resonant while:

`r ∈ W_R,hold`

even when the state no longer satisfies the stricter entry condition.

## 45. Exit Region

A resonance-exit relation defines when the system ceases to satisfy the resonance-retention condition.

The corresponding region or boundary must be explicitly defined.

## 46. Hysteretic Geometry

For a hysteretic resonance model:

`W_R,in`

`W_R,hold`

and the effective exit condition may differ.

This difference is part of the formal model.

It must not be treated as numerical noise.

## 47. No Universal Hysteresis

TR-EIF permits hysteretic resonance classification.

It does not require hysteresis in every model.

A memoryless resonance classifier remains valid when explicitly defined.

## 48. Resonance Trajectory

For continuous time:

`r(t) ∈ X_R`

For discrete execution:

`r_n ∈ X_R`

The resonance trajectory is the ordered path of resonance-coordinate states.

Classification may be applied along this trajectory.

## 49. Window Entry

A resonance-window entry event occurs when an admissible trajectory moves from the valid exterior to the interior according to the declared boundary semantics.

Entry is an event associated with trajectory order.

It is not simply the statement:

`r ∈ W_R`

## 50. Window Exit

A resonance-window exit event occurs when a previously interior or retained resonant state leaves the declared retention relation.

Exit is therefore history-sensitive when the model distinguishes prior classification.

## 51. Residence Interval

A residence interval is a maximal or otherwise declared interval during which the resonance classification remains:

`INSIDE`

or satisfies the declared resonance-retention state.

The exact residence convention must be defined by the model.

## 52. Residence Duration

Residence duration is derived from the resonance trajectory and time representation.

No universal minimum resonance residence time is defined by TR-EIF.

Any required minimum duration must have explicit provenance.

## 53. Boundary Residence

A model may allow a trajectory to remain on or near the declared resonance boundary.

Boundary residence must not be counted as interior residence unless the classification contract explicitly defines that behavior.

## 54. Multiple Resonance Windows

A resonance-coordinate space may contain several distinct resonance windows:

`W_R,1`

`W_R,2`

`...`

`W_R,k`

These windows may represent different resonance regimes.

They must have distinct definitions or identifiers.

## 55. Disjoint Windows

Two resonance windows may be disjoint.

A trajectory moving between them may pass through a nonresonant region.

A transition between two resonance regimes therefore does not imply continuous resonant classification throughout the path.

## 56. Overlapping Windows

Two declared resonance windows may overlap.

In the overlap region, the model must define whether:

- both classifications apply;
- one has priority;
- a combined regime exists;
- the state is considered ambiguous.

Overlap semantics must not remain implicit.

## 57. Nested Resonance Windows

A resonance window may be contained within another:

`W_R,a ⊂ W_R,b`

The inner and outer windows must have distinct semantic roles.

For example, one may represent a stricter resonance condition than the other.

No such hierarchy is assumed unless defined.

## 58. Resonance Regime Set

For multiple resonance regimes, define a regime set:

`R_set = {R_1, R_2, ..., R_k}`

A regime classifier may map:

`X_R,adm → R_set`

or into a richer structure when overlap is possible.

This regime classification remains distinct from balanced ternary state.

## 59. No Automatic Ternary Correspondence

Multiple resonance regions must not be assigned automatically to:

`-1`

`0`

and:

`1`

The mappings:

`R_1 → -1`

`R_2 → 0`

`R_3 → 1`

exist only if a specific ternary projection explicitly defines them.

## 60. Structural-State-Conditioned Window

A resonance window may depend on structural form:

`W_R(F_k)`

This permits different resonance conditions for different structural states.

The structural form and resonance region remain separately typed.

## 61. Topology-Conditioned Window

A resonance window may depend on interaction topology:

`W_R(G)`

A topology change may therefore modify the active resonance geometry.

The topology change itself remains distinct from resonance-window entry or exit.

## 62. Boundary-Conditioned Window

External or boundary conditions may influence the resonance region.

A boundary-conditioned window may be:

`W_R(B)`

where:

`B`

belongs to the declared boundary-state space.

Changing the boundary state changes the model configuration only through an explicit dependency.

## 63. Scale-Specific Resonance Space

For scale `s`:

`r_s ∈ X_R,s`

with:

`W_R,s ⊂ X_R,s`

Different scales may use different resonance coordinates and different windows.

A cross-scale comparison therefore requires an explicit mapping.

## 64. Cross-Scale Resonance Mapping

For scales `s` and `q`, a mapping may be:

`M_R,s→q: X_R,s → X_R,q`

or into a common comparison space.

The mapping must identify information loss and preserved relations.

## 65. Cross-Scale Resonance Equivalence

Two states at different scales must not be called resonance-equivalent solely because their numeric coordinates look similar.

Equivalence requires a declared comparison relation or invariant.

## 66. Uncertainty in Resonance Coordinates

A resonance-coordinate state may be uncertain.

An uncertainty representation may be:

- interval-valued;
- set-valued;
- probabilistic;
- covariance-based;
- another declared form.

The uncertainty representation remains distinct from the nominal resonance state.

## 67. Uncertain Window Membership

When uncertainty intersects a resonance boundary, exact classification may not be justified.

A model may represent states such as:

- definitely outside;
- definitely inside;
- boundary-intersecting uncertainty;
- unresolved.

Such uncertainty states must not be encoded automatically as ternary `0`.

## 68. Set-Valued Resonance State

An uncertain resonance state may be represented as:

`U_R ⊆ X_R`

Classification then concerns the relation between:

`U_R`

and:

`W_R`

Possible relations include:

- `U_R ∩ W_R = ∅`;
- `U_R ⊆ W_R`;
- partial intersection.

The interpretation must be explicit.

## 69. Probabilistic Resonance Membership

A stochastic model may define a probability of resonance-window membership.

This probability is not itself the deterministic resonance classification.

A probability threshold requires explicit provenance if used to make a discrete decision.

## 70. Resonance-State Projection Loss

Because:

`P_R: S × P → X_R`

may discard information, two complete states may satisfy:

`P_R(S_1,p) = P_R(S_2,p)`

while:

`S_1 ≠ S_2`

Therefore resonance-state equality does not generally imply complete-state equality.

## 71. Resonance-State Sufficiency

A resonance-coordinate state is sufficient for a particular resonance classification only when the classifier depends entirely on the information contained in that state and any explicitly declared history or parameters.

Sufficiency must not be assumed for other model operations.

## 72. Resonance Observability

A resonance state may be:

- directly observable;
- indirectly observable;
- inferred;
- latent.

The status depends on the mapping between internal state and available observables.

An inferred resonance state must not be described as directly measured unless it is directly measured.

## 73. Resonance Observable Space

A resonance observable belongs to:

`Y_R`

with mapping:

`O_R: S → Y_R`

or:

`O_R: X_R → Y_R`

depending on the model.

The observable space may contain only part of the information in `X_R`.

## 74. Observable Classification

A resonance classification derived from observables may differ in epistemic status from classification derived from complete internal model state.

The source of classification must therefore remain traceable.

## 75. Sampling Effects

A sampled resonance trajectory may omit:

- brief boundary contacts;
- short window entries;
- fast exits;
- intermediate coordinate extrema.

Sampling resolution must therefore be included in any claim about observed residence or transition timing.

## 76. Discrete-Time Resonance Space

In discrete execution:

`r_n = P_R(S_n,p_n)`

Window classification is evaluated at declared execution indices.

An event occurring between discrete samples cannot be inferred without an interpolation or event-detection model.

## 77. Continuous-Time Resonance Space

In continuous time:

`r(t)`

is a trajectory in `X_R`.

Window crossings may be defined by continuous trajectory intersection with:

`∂W_R`

when the required regularity conditions hold.

No smoothness is assumed across discrete hybrid events.

## 78. Hybrid Resonance Trajectory

A hybrid resonance trajectory may contain:

`continuous segment`

`→ discrete event`

`→ continuous segment`

The discrete event may change:

- ternary state;
- topology;
- structural state;
- boundary condition;
- another declared variable.

This may alter the subsequent resonance space or window.

## 79. Window Change Event

If the resonance window itself changes because of state, parameter, topology, or boundary evolution, the change must be represented explicitly.

A state may change classification even when:

`r`

does not move, because:

`W_R`

changes.

This is distinct from trajectory crossing through a fixed window boundary.

## 80. State-Motion and Window-Motion Distinction

The following mechanisms are different:

`r changes while W_R remains fixed`

and:

`W_R changes while r remains fixed`

and:

`both r and W_R change`

A classification change must preserve which mechanism occurred.

## 81. Resonance Accessibility

A resonance window may exist mathematically but be dynamically inaccessible from a particular initial state under the declared evolution.

Therefore:

`W_R exists`

does not imply:

`trajectory can reach W_R`

Accessibility is a dynamical property, not a geometric property alone.

## 82. Reachable Resonance Region

For a given initial condition and evolution contract, define conceptually the reachable resonance set:

`Reach_R(S_0) ⊆ X_R`

A resonance window is dynamically accessible from `S_0` only if:

`Reach_R(S_0) ∩ W_R ≠ ∅`

This is a general formal relation.

Its actual computation is model-specific.

## 83. Resonance Accessibility Is Initial-State Dependent

Different initial states may have different reachable resonance sets.

Therefore the accessibility of one resonance window may depend on:

- initial state;
- history;
- topology;
- parameter state;
- external forcing.

## 84. Resonance Accessibility Is Not Membership

A state may be outside a resonance window while the window remains dynamically accessible.

Likewise, a mathematically defined window may be inaccessible from the current state.

These are separate statements.

## 85. Resonance Basin

A model may define a set of initial conditions whose trajectories enter or remain within a specified resonance regime.

Such a set may be called a resonance-accessibility basin when its mathematical definition is supplied.

This term must not be confused automatically with a basin of attraction.

## 86. Attractor and Resonance Window Distinction

A resonance window is a region defined by resonance criteria.

An attractor is a dynamical object defined by trajectory behavior.

Therefore:

`resonance window ≠ attractor`

A resonance window may:

- contain an attractor;
- intersect an attractor;
- contain no attractor;
- be traversed transiently.

## 87. Resonance Stability Region

A model may define a subset:

`W_R,stable ⊆ W_R`

in which the resonance organization satisfies additional stability criteria.

The stability criteria must be defined separately from basic resonance membership.

## 88. Transient Resonance Region

A trajectory may pass through a resonance window without satisfying a declared persistence or stability criterion.

Such a state may be classified as transient resonance when the model defines that category.

Basic window membership and persistent resonance remain distinct.

## 89. Resonance Retention Region

A retention region may define conditions under which an existing resonance regime remains valid.

Retention is history-aware when current classification depends on the prior resonance state.

## 90. Resonance Loss

Resonance loss is an event in which a previously retained resonance regime ceases to satisfy its declared retention relation.

It is not equivalent automatically to:

- structural degradation;
- energy loss;
- ternary state `-1`;
- loss of coherence.

Those relations require explicit model definitions.

## 91. Resonance Recovery

A resonance regime may be re-entered after exit.

A recovery event must preserve:

- prior exit;
- nonresonant interval;
- new entry.

Recovery does not erase the previous resonance loss from the trajectory history.

## 92. Resonance-State Serialization

A serialized resonance state must preserve:

- coordinate identity;
- coordinate value;
- units where applicable;
- validity state;
- coordinate-space version;
- window identifier;
- classification;
- relevant parameter reference;
- time or execution index.

Exact schema design belongs to the computational layer.

## 93. Window Versioning

A resonance-window definition is version-sensitive.

A semantic change occurs when changing:

- coordinate definition;
- coordinate normalization;
- membership rule;
- boundary rule;
- entry condition;
- exit condition;
- hysteresis rule;
- uncertainty rule.

Validation of an earlier window definition does not automatically validate the changed one.

## 94. Resonance-State Traceability

Every resonance classification used by a downstream model should be traceable to:

`source state`

`→ resonance-coordinate mapping`

`→ resonance-coordinate state`

`→ active window definition`

`→ classification result`

This chain prevents a categorical resonance label from losing its mathematical origin.

## 95. Resonance-State Validation

A resonance-state validator must verify at least:

1. coordinate-space identity;

2. coordinate-domain validity;

3. unit consistency;

4. parameter provenance;

5. window identity;

6. window-definition validity;

7. boundary semantics;

8. classification consistency;

9. history availability where required;

10. numerical-tolerance declaration where used.

## 96. Window Validation

A resonance window is formally specified only when all of the following exist:

- containing resonance-coordinate space;
- admissible coordinate domain;
- membership relation;
- boundary relation;
- parameter dependencies;
- history dependencies;
- uncertainty semantics;
- numerical realization contract where implemented.

A collection of numerical thresholds without these relations is not a complete TR-EIF resonance-window specification.

## 97. Core Resonance-Space Invariants

The following invariants apply throughout Volume 02.

1. Every resonance state belongs to a declared `X_R`.

2. Every coordinate has declared semantics.

3. Every dimensional coordinate has declared units.

4. Every resonance window belongs to a declared coordinate space.

5. Every resonance window has an explicit boundary relation.

6. Invalid resonance states remain distinct from valid exterior states.

7. Boundary states remain distinct from interior and exterior states when the classifier uses three classes.

8. Numerical tolerance remains distinct from exact mathematical boundary.

9. Multiple coordinates are not reduced to one without an explicit mapping or proof.

10. Local and global resonance remain distinct.

11. Pairwise and collective resonance remain distinct.

12. History-dependent resonance requires explicit history.

13. Hysteresis requires distinct entry, retention, or exit semantics where applicable.

14. Resonance-window membership remains distinct from structural transition.

15. Resonance-window membership remains distinct from balanced ternary state.

16. Resonance coordinates remain distinct from observables.

17. Resonance-window geometry remains distinct from dynamical accessibility.

18. A resonance window remains distinct from an attractor.

19. Window changes remain distinguishable from state motion.

20. Window definitions remain versioned and traceable.

## 98. Formal Non-Equivalences

The following non-equivalences are mandatory:

`invalid resonance state ≠ OUTSIDE`

`resonance boundary ≠ numerical tolerance band`

`resonance window ≠ single universal frequency`

`resonance window ≠ attractor`

`resonance membership ≠ resonance accessibility`

`resonance membership ≠ persistent resonance`

`resonance loss ≠ structural degradation`

`local resonance ≠ global resonance`

`pairwise resonance ≠ collective resonance`

`resonance state ≠ observable`

`resonance state ≠ ternary state`

`resonance regime ≠ ternary branch`

`window change ≠ state trajectory crossing`

`resonance window ≠ structural region`

`resonance-window membership ≠ structural transition`

## 99. Minimal Resonance-Space Contract

A conforming model must define:

- `X_R`;
- every resonance coordinate;
- `P_R`;
- `X_R,adm`;
- `W_R`;
- `∂W_R`;
- `C_R`;
- validity semantics;
- entry semantics;
- exit semantics;
- history semantics where applicable;
- uncertainty semantics where applicable;
- numerical boundary semantics where implemented.

If multiple resonance regimes exist, every regime must have its own identifiable mathematical definition.

## 100. Conformance Requirements

A TR-EIF resonance-state model conforms to this chapter when:

- the resonance-coordinate space is explicitly defined;
- all coordinates have defined mathematical types;
- coordinate units are consistent;
- the admissible domain is explicit;
- resonance windows are defined as regions of the declared space;
- boundary states are mathematically specified;
- invalid states are not misclassified as valid exterior states;
- local and global resonance spaces remain separated;
- history and hysteresis are represented when required;
- numerical boundary tolerances are separated from exact mathematics;
- uncertainty does not collapse into ternary `0`;
- resonance membership does not substitute for structural state;
- all active window parameters have provenance.

## 101. Final Resonance-State-Space Statement

The TR-EIF resonance layer represents resonance through explicitly typed state-space geometry.

The fundamental construction is:

`S`

`→ P_R`

`→ r ∈ X_R`

`→ X_R,adm`

`→ W_R`

`→ ∂W_R`

`→ C_R(r)`

A resonance window is therefore not a symbolic frequency label but a declared region of a defined resonance-coordinate space.

Its geometry may depend on:

- multiple coordinates;
- coupling;
- phase;
- delay;
- dissipation;
- topology;
- structure;
- history;
- scale;
- boundary conditions.

The formalism preserves the distinction between:

`state validity`

`resonance-space location`

`window membership`

`window accessibility`

`resonance persistence`

`ternary state`

`structural state`

and:

`observable representation`

This state-space architecture establishes the geometric foundation required for the subsequent TR-EIF resonance dynamics and ternary resonance transition theory.
