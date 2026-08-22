# Fundamental Properties

## 1. Purpose

This document establishes the fundamental mathematical properties that follow from the previously defined TR-EIF foundations, notation, axiomatic system, state spaces, operators, mathematical structures, mappings, and framework invariants.

The properties in this chapter are restricted to statements that follow from already declared TR-EIF definitions and axioms.

This chapter does not introduce:

- empirical constants;
- material parameters;
- fitted thresholds;
- physical calibration values;
- implementation-specific tolerances;
- unverified physical laws.

The purpose is to derive reusable consequences of the TR-EIF formal structure.

## 2. Status of This Document

This document depends on:

- `chapter_01_foundations.md`;
- `chapter_02_notation_and_definitions.md`;
- `chapter_03_axiomatic_system.md`;
- `chapter_04_state_spaces.md`;
- `chapter_05_mathematical_operators.md`;
- `chapter_06_mathematical_structures.md`;
- `chapter_07_mathematical_mappings.md`;
- `chapter_08_framework_invariants.md`.

Definitions and axioms established in those chapters remain authoritative.

The statements below are classified as:

- definitions;
- lemmas;
- propositions;
- corollaries;
- framework consequences.

No empirical status is implied by a purely formal result.

## 3. Property Classes

The fundamental properties are grouped into:

1. balanced ternary properties;
2. state-space properties;
3. transition properties;
4. continuous-discrete coupling properties;
5. operator properties;
6. mapping properties;
7. graph and topology properties;
8. oscillatory and resonance properties;
9. symmetry and equivariance properties;
10. delay and memory properties;
11. structural-transition properties;
12. recursive-inheritance properties;
13. multiscale properties;
14. observable properties;
15. numerical and deterministic properties;
16. validation properties.

## 4. Balanced Ternary State Set

The primitive balanced ternary state set is:

`T = {-1, 0, 1}`

The canonical notation is:

`-1/0/1`

State `0` is active.

The admissible local transition relation is:

`R_T = {(-1,-1), (-1,0), (0,-1), (0,0), (0,1), (1,0), (1,1)}`

The pairs:

`(-1,1)`

and:

`(1,-1)`

do not belong to `R_T`.

## 5. Proposition 1 — Ternary Closure

### Statement

Every admissible local ternary transition begins and ends inside `T`.

### Proof

By definition:

`R_T ⊆ T × T`

Therefore, for every:

`(a,b) ∈ R_T`

both:

`a ∈ T`

and:

`b ∈ T`

hold.

Therefore the local transition relation is closed over the balanced ternary state set.

### Consequence

A conforming ternary transition cannot create an undeclared fourth logical state.

## 6. Proposition 2 — Direct Opposite-State Exclusion

### Statement

No admissible local transition connects `-1` directly to `1` or `1` directly to `-1`.

### Proof

The admissible transition relation excludes:

`(-1,1)`

and:

`(1,-1)`

Therefore:

`-1 → 1`

and:

`1 → -1`

cannot occur as single admissible transition events.

## 7. Proposition 3 — Neutral Mediation

### Statement

Every admissible path from `-1` to `1` contains state `0`.

Every admissible path from `1` to `-1` contains state `0`.

### Proof

The only non-self outgoing transition from `-1` is:

`-1 → 0`

The only admissible path from `0` toward the positive branch is:

`0 → 1`

Therefore any admissible polarity-changing path from `-1` to `1` contains:

`-1 → 0 → 1`

The reverse case follows symmetrically from:

`1 → 0`

and:

`0 → -1`

### Consequence

State `0` is structurally necessary for every completed opposite-polarity transition.

## 8. Proposition 4 — Minimum Opposite-State Path Length

### Statement

A completed opposite-state transition requires at least two state-changing transition events.

### Proof

A direct opposite transition is forbidden.

The shortest admissible negative-to-positive path is:

`-1 → 0 → 1`

The shortest admissible positive-to-negative path is:

`1 → 0 → -1`

Each path contains two state-changing edges.

Therefore the minimum number of state-changing events is two.

## 9. Corollary 4.1 — Final State Does Not Determine Event Count

Knowing only:

`initial state = -1`

and:

`final state = 1`

does not determine whether the transition was valid.

A trace must establish the intermediate state sequence.

## 10. Proposition 5 — Neutral-State Retention

### Statement

State `0` may persist for an arbitrary finite number of admissible self-transition steps unless a stricter model-specific rule limits that duration.

### Proof

The transition:

`0 → 0`

belongs to `R_T`.

Therefore repeated application:

`0 → 0 → 0 → ... → 0`

remains locally admissible.

### Consequence

Arrival at `0` does not imply immediate completion toward either polarity.

## 11. Proposition 6 — Neutral State Is Not a Null Symbol

### Statement

Within TR-EIF ternary semantics, state `0` cannot be replaced by absence of state without changing the formal system.

### Proof

State `0`:

- belongs to `T`;
- participates in admissible transitions;
- mediates opposite-state paths;
- may persist;
- may condition continuous evolution.

Absence of state does not possess these declared transition semantics.

Therefore state `0` and absence of state are not equivalent objects.

## 12. Proposition 7 — Transition Path Carries Information

### Statement

The transition path contains information not contained in the final ternary state alone.

### Proof

Consider two state histories ending at `1`:

`1 → 1`

and:

`-1 → 0 → 1`

Both end at state `1`.

Their preceding transition structures differ.

Therefore the mapping:

`transition history → final state`

is generally many-to-one.

### Consequence

Final-state equality does not imply transition-history equality.

## 13. Global Ternary Configuration

For `N` ternary components:

`Σ_T = T^N`

A global state is:

`σ = (σ_1, ..., σ_N)`

with:

`σ_i ∈ T`

for every component `i`.

## 14. Proposition 8 — Global State Cardinality

### Statement

For finite `N`, the unrestricted global ternary configuration space contains:

`3^N`

possible configurations.

### Proof

Each of the `N` components independently has three possible values in `T`.

By the product rule:

`|T^N| = 3^N`

### Boundary

A model-specific admissible subset:

`Σ_T,adm ⊆ T^N`

may contain fewer configurations because of global constraints.

## 15. Proposition 9 — Local Validity Is Necessary but Not Sufficient for Global Validity

### Statement

A global transition cannot be valid if one of its local transitions is forbidden.

However, local validity of every component does not by itself guarantee global validity.

### Proof

If one component contains:

`-1 → 1`

or:

`1 → -1`

the global transition violates the local transition invariant.

Conversely, every local transition may belong to `R_T` while the complete update violates a global condition such as:

- capacity;
- topology;
- mutual exclusion;
- conservation;
- structural admissibility.

Therefore local validity is necessary but not sufficient for global validity.

## 16. Proposition 10 — Ternary Numerical Ordering Is Not Semantic Ordering

### Statement

The arithmetic relation:

`-1 < 0 < 1`

does not establish a universal semantic ranking of TR-EIF ternary states.

### Reason

TR-EIF assigns operational meanings through model contracts.

State `0` has active mediation semantics.

Therefore numeric order alone cannot establish:

- quality;
- stability;
- priority;
- physical magnitude;
- structural value.

## 17. Composite State Property

A general TR-EIF state may be represented as:

`S = X × Σ_T × X_G × X_H × X_F × X_B × X_num × X_val`

A model may use a strict subset of these factors.

## 18. Proposition 11 — Component-Type Preservation

### Statement

Membership in a Cartesian product does not erase the mathematical type of each component.

### Proof

For:

`S = A × B`

an element:

`s = (a,b)`

satisfies:

`a ∈ A`

and:

`b ∈ B`

The product construction combines the components without identifying them.

### Consequence

A continuous state does not become ternary merely because both occur inside the same composite state.

## 19. Proposition 12 — Composite-State Equality

Two complete states are equal only if every declared state component is equal under its corresponding equality rule.

For:

`S_1 = (X_1, σ_1, G_1, H_1)`

and:

`S_2 = (X_2, σ_2, G_2, H_2)`

exact equality requires:

`X_1 = X_2`

`σ_1 = σ_2`

`G_1 = G_2`

`H_1 = H_2`

where those components belong to the declared model state.

Equality of only one component does not establish complete-state equality.

## 20. Proposition 13 — Observable Equality Does Not Imply State Equality

Let:

`O: S → Y`

be an observable mapping.

### Statement

In general:

`O(S_1) = O(S_2)`

does not imply:

`S_1 = S_2`

### Proof

An observable mapping may be many-to-one or lossy.

Unless injectivity of `O` is established over the relevant domain, different internal states may map to the same observable.

### Consequence

Observed equality and state equality remain separate claims.

## 21. Corollary 13.1 — Hidden-State Ambiguity

If `O` is non-injective, the inverse reconstruction of complete state from one observable value is not unique.

## 22. Proposition 14 — History Can Distinguish Instantaneously Equal States

### Statement

Two systems with equal instantaneous continuous and ternary components may remain dynamically distinct when their history states differ.

### Proof

Let:

`S_1(t) = (X, σ, H_1)`

and:

`S_2(t) = (X, σ, H_2)`

with:

`H_1 ≠ H_2`

For a history-dependent evolution operator:

`U_H`

future evolution may depend explicitly on `H`.

Therefore:

`U_H(S_1)`

and:

`U_H(S_2)`

need not be equal.

## 23. Corollary 14.1 — Instantaneous Observation Is Insufficient for General History-Dependent Reconstruction

A model with explicit memory cannot generally be reconstructed from instantaneous observables alone.

## 24. Proposition 15 — Hybrid State Space Is Not Purely Continuous

### Statement

A state space containing a nontrivial ternary component is not a purely continuous state representation.

### Reason

The ternary factor:

`T^N`

is discrete.

The product:

`X × T^N`

therefore contains both continuous and discrete state structure.

### Consequence

A globally smooth continuous-time description cannot silently replace the discrete transition semantics.

## 25. Proposition 16 — Discrete Events Need Not Destroy Continuous Segments

### Statement

A hybrid trajectory may contain continuously evolving segments separated by discrete events.

### Form

A trajectory may be represented as:

`continuous segment`

`→ event`

`→ continuous segment`

`→ event`

### Consequence

Continuous differentiability may be valid within a segment without being valid across the event boundary.

## 26. Proposition 17 — Differential Operators Are Local to Differentiable Regions

A derivative such as:

`dX/dt`

is defined only where the required differentiability conditions hold.

A discrete ternary transition or topology change must not be treated as an ordinary smooth derivative event unless an explicit continuous embedding has been defined and justified.

## 27. Continuous-to-Ternary Projection

Let:

`Π: X → T^N`

be a continuous-to-ternary projection.

## 28. Proposition 18 — Continuous Projection Is Information-Reducing in the General Case

### Statement

When `X` contains more distinguishable states than `T^N`, a projection:

`Π: X → T^N`

cannot generally preserve all information contained in `X`.

### Reason

Multiple continuous states may occupy the same ternary decision region and therefore receive the same ternary output.

### Consequence

The ternary state must not be treated as a complete replacement for the source continuous state.

## 29. Proposition 19 — Projection and Transition Are Distinct Operations

### Statement

A projected target state does not itself constitute an executed state transition.

### Example

Suppose:

`current ternary state = -1`

and:

`Π(X) = 1`

The projection identifies a target classification.

The admissible executed path remains:

`-1 → 0 → 1`

### Consequence

A projection operator cannot bypass transition invariants.

## 30. Proposition 20 — History-Dependent Projection Is Not a Function of Current Continuous State Alone

If:

`Π_H: X × H × T^N → T^N`

then equal current continuous inputs may produce different outputs when:

- history differs;
- current ternary state differs.

Therefore a history-dependent projection cannot be reduced to:

`Π: X → T^N`

without information loss or additional assumptions.

## 31. Proposition 21 — Ternary State Labels Do Not Define Physical Magnitude

### Statement

The numeric labels `-1`, `0`, and `1` do not by themselves define physical values.

### Consequence

A mapping such as:

`state 1 → physical amplitude A`

requires an explicit model-specific relation.

The arithmetic value `1` alone does not establish the physical amplitude.

## 32. Operator Composition Property

Let:

`F: A → B`

and:

`G: B → C`

Then:

`G ∘ F: A → C`

is defined.

## 33. Proposition 22 — Domain-Codomain Compatibility Is Necessary for Composition

If the output of `F` does not belong to the domain required by `G`, then:

`G ∘ F`

is not a valid composition without an additional mapping.

### Consequence

An implementation cast or serialization conversion cannot silently repair a mathematical type mismatch.

## 34. Proposition 23 — Operator Order May Carry Semantics

In general:

`F ∘ G ≠ G ∘ F`

Therefore changing operation order may change the mathematical result.

Examples include:

`projection → transition`

versus:

`transition → projection`

and:

`topology update → neighborhood extraction`

versus:

`neighborhood extraction → topology update`

### Consequence

Execution order is part of the model contract whenever the operators do not commute.

## 35. Proposition 24 — Identity Preservation

For identity operator:

`I_A: A → A`

the relation:

`I_A(a) = a`

holds.

Therefore explicit state retention can be represented as a valid mathematical operation rather than as absence of execution.

## 36. Proposition 25 — Lossy Projection Has No Unique Exact Inverse

### Statement

If projection:

`P: A → B`

maps two distinct states:

`a_1 ≠ a_2`

to the same value:

`P(a_1) = P(a_2)`

then no inverse mapping from that output can uniquely recover both original states.

### Consequence

A reconstruction from a lossy projection requires:

- additional information;
- a selection rule;
- a probabilistic model;
- an approximate reconstruction rule.

It is not an exact inverse.

## 37. Graph Structure Property

Let:

`G = (V,E)`

be a declared interaction graph.

## 38. Proposition 26 — Graph Topology Does Not Determine Geometry

### Statement

The edge relation `E` does not uniquely determine the spatial coordinates of nodes.

### Reason

Different spatial configurations may share the same adjacency relation.

### Consequence

Graph topology and interatomic geometry must remain separate state components unless a specific model establishes a unique relation.

## 39. Proposition 27 — Geometry Does Not Universally Determine Interaction Topology

### Statement

Coordinates alone do not define graph edges without an interaction-graph construction rule.

### Reason

The graph may depend on:

- distance;
- species;
- channel;
- topology state;
- interaction criterion;
- boundary conditions.

### Consequence

A graph edge must arise from a declared mapping or external definition.

## 40. Proposition 28 — Reindexing Does Not Change Atomic Identity

Let:

`π`

be a permutation of computational indices.

If atomic identity and every associated state are transformed consistently under `π`, the computational ordering changes while the represented physical identity does not.

### Consequence

Node index and atomic identity are distinct objects.

## 41. Proposition 29 — Local Environment Is Representation-Dependent

A local environment:

`N_i`

depends on the declared neighborhood rule.

Different valid neighborhood constructions may produce different local environment sets from the same global configuration.

### Consequence

The neighborhood rule is part of the model definition.

## 42. Proposition 30 — Descriptor Equality Does Not Necessarily Imply Environment Equality

Let:

`D: X_N → X_D`

be a descriptor mapping.

If `D` is non-injective, then:

`D(N_1) = D(N_2)`

may hold while:

`N_1 ≠ N_2`

### Consequence

A descriptor must not be identified automatically with the complete physical local environment.

## 43. Circular Phase Property

Oscillator phase belongs to:

`𝕊¹`

## 44. Proposition 31 — Phase Is Periodic

Phase values differing by one complete revolution represent the same circular phase.

Therefore linear coordinate storage of phase requires a wrap convention.

## 45. Proposition 32 — Raw Linear Phase Difference Can Misrepresent Circular Separation

A direct numerical difference:

`θ_j - θ_i`

may lie outside the canonical phase interval.

Therefore phase comparison must use the declared circular wrapping rule whenever circular equivalence matters.

## 46. Proposition 33 — Phase Equality Is Not Required for Coherence

### Statement

TR-EIF coherence may preserve a declared nonzero phase relation.

Therefore:

`θ_i = θ_j`

is not a universal coherence condition.

### Consequence

Coherence and uniformity are formally distinct.

## 47. Proposition 34 — Phase Locking Is Not Equivalent to Resonance

Phase locking is one possible persistent dynamic relation.

Resonance may additionally depend on:

- amplitudes;
- frequency relations;
- coupling;
- geometry;
- delay;
- dissipation;
- modal structure.

Therefore phase locking alone is not the universal definition of resonance.

## 48. Resonance Window Property

A resonance window is:

`W_R ⊂ P_R`

where `P_R` is a declared resonance parameter or state space.

## 49. Proposition 35 — Resonance Is Model-Relative

### Statement

Membership in a resonance window is meaningful only relative to the declared resonance space, projection, and window definition.

### Proof

A state is classified through:

`S → P_R(S) → W_R`

Without:

- the projection `P_R`;
- coordinates of `P_R`;
- definition of `W_R`;

the membership statement is undefined.

## 50. Proposition 36 — A Multidimensional Resonance Window Is Not Determined by One Coordinate

If:

`P_R = P_1 × P_2 × ... × P_n`

with:

`n > 1`

then one coordinate alone does not generally determine membership in:

`W_R`

unless the model proves such a reduction.

### Consequence

A resonance region cannot generally be reduced to one universal frequency.

## 51. Proposition 37 — Resonance-Window Membership Does Not Imply Structural Transition

A state may satisfy:

`P_R(S) ∈ W_R`

while remaining in the same structural region:

`R_F,k`

Therefore resonance-window membership and structural transition are distinct properties.

## 52. Proposition 38 — Resonance Entry and Exit Need Not Be Symmetric

When resonance classification depends on:

- history;
- hysteresis;
- direction of trajectory;
- structural state;

the entry condition and exit condition may differ.

### Consequence

A resonance-window contract must define both when this distinction exists.

## 53. Symmetry Group Property

Let:

`G_sym`

be a declared transformation group with action:

`ρ_X(g): X → X`

## 54. Proposition 39 — Invariance Is Transformation-Relative

For invariant mapping:

`F`

the relation:

`F(ρ_X(g)x) = F(x)`

applies only to the declared transformations `g`.

### Consequence

Invariance under translation does not imply invariance under rotation, reflection, scaling, or permutation unless those transformations are also included and validated.

## 55. Proposition 40 — Equivariance Is Not Output Equality

For equivariant mapping:

`F: X → Y`

the defining relation is:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

The transformed output may differ numerically from the original output.

### Consequence

Equivariance preserves transformation consistency, not necessarily output value.

## 56. Proposition 41 — Invariance Is a Special Transformation Behavior

If the output action is the identity:

`ρ_Y(g) = I_Y`

then the equivariance relation becomes:

`F(ρ_X(g)x) = F(x)`

which is invariance under the declared transformation.

## 57. Proposition 42 — Equivariant Composition

Let:

`F: X → Y`

and:

`G: Y → Z`

satisfy:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

and:

`G(ρ_Y(g)y) = ρ_Z(g)G(y)`

Then:

`G ∘ F`

is equivariant under the compatible actions.

### Proof

Starting from transformed input:

`G(F(ρ_X(g)x))`

Using equivariance of `F`:

`= G(ρ_Y(g)F(x))`

Using equivariance of `G`:

`= ρ_Z(g)G(F(x))`

Therefore:

`(G ∘ F)(ρ_X(g)x) = ρ_Z(g)(G ∘ F)(x)`

## 58. Corollary 42.1 — Intermediate Action Compatibility Is Required

If the output action of `F` does not match the input action expected by `G`, the composition does not inherit the equivariance property automatically.

## 59. Proposition 43 — Geometric Symmetry Does Not Automatically Flip Ternary Polarity

A geometric action on positions or vectors has no automatic semantic authority over:

`T = {-1,0,1}`

Therefore ternary values remain unchanged under a geometric transformation unless a specific ternary transformation action:

`ρ_T(g)`

is explicitly defined.

## 60. Delay Property

For delay:

`τ > 0`

a delayed dependency may use:

`X(t - τ)`

## 61. Proposition 44 — Instantaneous State Is Insufficient for Generic Delay Dynamics

If future evolution depends on:

`X(t - τ)`

then knowledge of `X(t)` alone is insufficient unless the delayed state can be uniquely derived from the current state.

### Consequence

The effective state of a delayed model requires history or an equivalent memory representation.

## 62. Proposition 45 — Delay Requires Initial History

For execution beginning at:

`t_0`

evaluation of:

`X(t - τ)`

for:

`t ∈ [t_0, t_0 + τ)`

requires state information before `t_0`.

Therefore a delayed model requires an initial history contract.

## 63. Proposition 46 — Memory Compression Can Be Lossy

Let:

`C_H: X_H → X_μ`

compress history.

If two histories:

`H_1 ≠ H_2`

satisfy:

`C_H(H_1) = C_H(H_2)`

then exact history cannot be uniquely reconstructed from the compressed memory state.

## 64. Proposition 47 — Hysteresis Produces Path Dependence

If a mapping depends on history:

`F_H: X × H → Y`

then two equal current inputs may produce different outputs when their histories differ.

Therefore hysteresis is a formal mechanism of path dependence.

## 65. Dissipation Property

TR-EIF separates:

`physical dissipation`

from:

`numerical loss`

## 66. Proposition 48 — Numerical Residual Does Not Establish Physical Dissipation

### Statement

A discrepancy in numerical energy accounting does not by itself establish a physical dissipation channel.

### Reason

The discrepancy may result from:

- discretization;
- truncation;
- rounding;
- solver error;
- incomplete numerical convergence.

### Consequence

A physical interpretation requires an explicitly defined physical dissipation mapping.

## 67. Proposition 49 — Stable Organization May Coexist With Dissipation

The TR-EIF system class permits open dissipative systems.

Therefore preservation of a declared structural form does not require zero dissipation.

A maintained form may coexist with:

- energy input;
- redistribution;
- output;
- dissipation.

No equilibrium assumption follows automatically.

## 68. Structural Form Property

A structural form:

`F_k`

is defined through a declared region or relation in structural state space.

## 69. Proposition 50 — Coordinate Equality Is Not Required for Structural Equivalence

Two states may occupy different coordinates while preserving the same declared structural invariants.

Therefore structural equivalence can be weaker than exact state equality.

## 70. Proposition 51 — Structural Transition Requires More Than State Change

Every structural transition is a state change.

Not every state change is a structural transition.

### Reason

A structural transition additionally requires:

- departure from the previous structural regime;
- declared transition conditions;
- post-transition structural membership;
- stabilization where required.

## 71. Proposition 52 — Resonance-Window Crossing Is Not Sufficient for Structural Transition

Crossing:

`∂W_R`

changes resonance-window classification.

A structural transition additionally requires the structural-transition conditions defined for:

`F_k → F_k+1`

Therefore the two events are formally distinct.

## 72. Proposition 53 — Structural Transition Can Preserve Some Invariants and Replace Others

Let:

`F_k → F_k+1`

be a structural transition.

The transition may preserve a subset of previous invariants while terminating others and establishing new invariants.

### Consequence

A structural transition need not imply destruction of all prior structure.

## 73. Structural Work Property

Structural work is evaluated relative to a declared form.

## 74. Proposition 54 — Structural-Work Sign Is Reference-Dependent

A process may be negative relative to:

`F_k`

while positive relative to:

`F_k+1`

because the evaluation criteria are associated with different structural forms.

### Consequence

The sign of structural work has no universal meaning without its reference form.

## 75. Proposition 55 — Stable Outcome Does Not Determine Structural Value

A stable attractor may correspond to:

- retention;
- reinforcement;
- simplification;
- degradation;
- another declared outcome.

Therefore dynamical stability alone does not determine constructive or degradative classification.

## 76. Recursive Inheritance Property

Let:

`Λ_I: S_n,final → X_I`

extract inherited state.

Let:

`J_I: X_I × X_B × P → S_n+1,initial`

construct the next-cycle initial state.

## 77. Proposition 56 — Recursive Evolution Can Carry Historical Information Across Cycles

If:

`I_n→n+1`

contains state derived from cycle `n`, then cycle `n+1` depends on the result of cycle `n`.

Therefore successive cycles are not independent.

## 78. Proposition 57 — Lossy Inheritance Reduces Historical Identifiability

If:

`Λ_I`

is many-to-one, different final states may produce the same inherited state.

Therefore the next cycle cannot reconstruct all distinctions of the previous final state from inherited state alone.

## 79. Proposition 58 — Reset and Inheritance Are Distinct Operations

A state component may be:

- inherited;
- recalculated;
- externally initialized;
- reset.

These operations have different provenance.

A reset component must not be described as inherited.

## 80. Multiscale Property

Let:

`M_s→r: S_s → S_r`

map scale `s` to scale `r`.

## 81. Proposition 59 — Fine-to-Coarse Mapping May Be Many-to-One

Distinct microscopic states may produce the same coarse representation.

### Consequence

The coarse state generally does not uniquely identify the fine state.

## 82. Proposition 60 — Downward Mapping Is Not Automatic Inversion

A coarse-to-fine mapping:

`M_r→s`

does not become the inverse of:

`M_s→r`

unless inverse properties are established.

### Consequence

Cross-scale reconstruction requires additional assumptions or information.

## 83. Proposition 61 — Cross-Scale Similarity Does Not Establish Identical Physical Mechanism

Two scales may preserve a declared relational invariant while using different state variables or physical carriers.

Therefore formal self-similarity does not imply identical microscopic physics.

## 84. Proposition 62 — Multiscale Consistency Requires a Comparison Mapping

States:

`S_s`

and:

`S_r`

belong to different spaces.

A consistency claim requires a declared relation or mapping that brings the compared quantities into compatible form.

## 85. Observable Projection Property

Let:

`O: S → Y`

## 86. Proposition 63 — Observable Projection Can Change Apparent Dynamics

A measurement or observable mapping may include:

- sampling;
- averaging;
- filtering;
- finite resolution.

Therefore the observed trajectory may have lower temporal or spatial detail than the internal state trajectory.

## 87. Proposition 64 — Apparent Instantaneity Can Be Resolution-Dependent

If a process duration is much shorter than the observation interval:

`τ_proc << Δt_obs`

the internal transition may appear instantaneous at the selected observational resolution.

This does not imply zero physical or modeled duration.

## 88. Proposition 65 — Apparent Staticity Can Be Resolution-Dependent

If:

`τ_proc >> Δt_obs`

a slowly changing process may appear approximately static during the selected observation interval.

This does not establish a mathematically constant state over longer intervals.

## 89. Proposition 66 — Sampling Can Remove Transition Detail

A sampled observable may omit intermediate states occurring between sample times.

### Consequence

Transition-path invariants must be validated from sufficiently resolved state or event traces rather than from undersampled final observables alone.

## 90. Numerical Representation Property

A numerical state:

`X_n`

approximates or encodes a mathematical state under a declared numerical representation.

## 91. Proposition 67 — Numerical Equality Depends on Representation Contract

Exact bitwise equality, exact integer equality, and tolerance-based floating-point equality are different comparison relations.

A validation result must specify which relation it uses.

## 92. Proposition 68 — Quantization Is Generally Many-to-One

A quantization mapping converts a larger numerical domain into a finite representable set.

Multiple source values may therefore map to one quantized value.

### Consequence

Quantization generally loses information.

## 93. Proposition 69 — Quantization Does Not Create Ternary Semantics

A quantized representation acquires balanced ternary semantics only when its codomain is explicitly:

`T = {-1,0,1}`

and its transition rules satisfy the TR-EIF ternary contract.

Finite numeric representation alone is insufficient.

## 94. Proposition 70 — Numerical Approximation Does Not Redefine Exact Mathematics

A numerical operator:

`L_h`

may approximate mathematical operator:

`L`

The existence of finite approximation error does not alter the mathematical definition of `L`.

### Consequence

Implementation behavior must be validated against the mathematical contract rather than used silently to redefine it.

## 95. Deterministic Execution Property

A deterministic execution is determined by its complete declared execution state and input.

## 96. Proposition 71 — Hidden Mutable State Breaks Declared Determinism

If two executions with identical declared inputs can differ because of an undeclared mutable state, then the declared execution record is insufficient for deterministic replay.

### Consequence

All result-affecting state must be declared or captured.

## 97. Proposition 72 — Randomized Computation Can Be Replay-Deterministic

A computation using pseudorandom values may remain deterministically replayable when the complete random-generator state or equivalent deterministic seed contract is preserved.

### Boundary

Deterministic replay does not remove the stochastic interpretation of a stochastic mathematical model.

## 98. Proposition 73 — Update Ordering Is Part of Deterministic State

If two noncommuting updates may execute in different orders, then output can differ.

Therefore deterministic execution requires deterministic ordering or a proven order-independent update relation.

## 99. Trace Property

A trace is an ordered representation of execution-relevant states and events.

## 100. Proposition 74 — A Trace Can Be Semantically Incomplete Despite Being Syntactically Valid

A serialized trace may satisfy its data syntax while omitting information required by the mathematical execution contract.

Examples include omission of:

- neutral transition legs;
- invariant failures;
- execution order;
- parameters;
- version identifiers.

### Consequence

Schema validity and semantic trace completeness are distinct properties.

## 101. Proposition 75 — Transition Trace Must Preserve Neutral Mediation

For a completed opposite-state transition, a valid trace must represent the intermediate state `0`.

A trace containing only:

`-1`

followed by:

`1`

cannot establish conformance with the ternary transition invariant.

## 102. Proposition 76 — Failure History Is Part of Execution History

A recovered execution remains historically distinct from an execution in which the failure never occurred.

### Reason

The conforming trace contains:

`failure`

`→ recovery`

whereas the unaffected execution does not.

### Consequence

Recovery does not erase provenance.

## 103. Validation Property

Let:

`V_k`

evaluate invariant `I_k`.

## 104. Proposition 77 — Not Evaluated Does Not Imply Pass

The validation states:

`PASS`

and:

`NOT_EVALUATED`

are distinct.

Therefore absence of a detected failure cannot establish successful validation when the invariant was not evaluated.

## 105. Proposition 78 — Aggregate Success Cannot Override a Required Failure

If one required invariant evaluates to:

`FAIL`

then an aggregate arithmetic score over unrelated passing checks cannot convert that invariant result into `PASS`.

### Consequence

Required invariant failures remain individually authoritative.

## 106. Proposition 79 — Validation Is Version-Relative

A validation result applies to the mathematical and computational artifacts actually tested.

If a semantic change alters:

- state definition;
- operator;
- mapping;
- invariant;
- parameter;
- execution order;

the previous validation does not automatically establish the changed artifact.

## 107. Proposition 80 — Mathematical Validity and Empirical Validity Are Distinct

A mathematically consistent model may satisfy its formal definitions and invariants without having been empirically validated.

Conversely, an empirical comparison requires:

- measurement;
- provenance;
- comparison mapping;
- uncertainty treatment.

### Consequence

Formal consistency and empirical correspondence remain separate scientific claims.

## 108. Fundamental Non-Equivalences

The following non-equivalences follow from the TR-EIF architecture:

`state 0 ≠ missing state`

`state 0 ≠ invalid state`

`continuous state ≠ ternary state`

`projected target ≠ executed transition`

`final ternary state ≠ transition history`

`observable ≠ complete internal state`

`observable equality ≠ state equality`

`coordinate representation ≠ physical state`

`node index ≠ atomic identity`

`local environment ≠ descriptor`

`graph topology ≠ spatial geometry`

`graph edge ≠ physical bond`

`oscillator phase ≠ dynamical phase space`

`phase locking ≠ resonance`

`synchronization ≠ resonance`

`coherence ≠ uniformity`

`resonance-window membership ≠ structural transition`

`ordinary state update ≠ structural transition`

`structural stability ≠ constructive outcome`

`numerical loss ≠ physical dissipation`

`quantization ≠ ternary semantics`

`coarse-graining ≠ exact reversible reduction`

`numerical approximation ≠ mathematical definition`

`schema validity ≠ semantic trace completeness`

`formal validation ≠ empirical validation`

## 109. Fundamental Implication Chain

The preceding properties establish the following formal dependency chain:

`balanced ternary state definition`

`→ constrained transition relation`

`→ active neutral mediation`

`→ path-dependent transition validity`

`→ explicit continuous-discrete mapping`

`→ hybrid state evolution`

`→ history-aware dynamics`

`→ declared resonance regions`

`→ explicit transformation actions`

`→ equivariant structural mapping`

`→ structural-state classification`

`→ explicit structural transition`

`→ recursive inheritance`

`→ observable projection`

`→ deterministic numerical realization`

`→ invariant-preserving trace`

`→ validation`

## 110. Framework Property Set

The minimum fundamental property set of TR-EIF is therefore:

1. The ternary domain is exactly `-1/0/1`.

2. State `0` is active.

3. Direct opposite-state transitions are excluded.

4. Opposite-state transitions require neutral mediation.

5. Transition history contains information beyond final state.

6. Continuous and ternary states remain mathematically distinct.

7. Continuous-to-ternary projection may be information-reducing.

8. Projection and execution are separate operations.

9. Hybrid state evolution may combine continuous trajectories and discrete events.

10. History-dependent systems cannot generally be reduced to instantaneous-state descriptions.

11. Graph topology and geometry remain distinct.

12. Oscillator phase has circular structure.

13. Resonance is defined relative to a declared parameter or state region.

14. Resonance-window membership does not imply structural transition.

15. Coherence does not require uniformity.

16. Invariance and equivariance are transformation-relative properties.

17. Compatible equivariant mappings preserve equivariance under composition.

18. Geometric transformation does not automatically transform ternary polarity.

19. Structural transitions require explicit pre-transition and post-transition definitions.

20. Structural work is relative to a declared structural form.

21. Recursive inheritance permits path-dependent inter-cycle evolution.

22. Fine-to-coarse mappings may lose microscopic information.

23. Observables may not uniquely identify internal states.

24. Observation resolution can alter apparent temporal structure.

25. Quantization generally loses information.

26. Quantization does not automatically create ternary semantics.

27. Numerical approximation remains distinct from exact mathematical definition.

28. Deterministic replay requires complete execution dependencies.

29. Trace validity requires semantic event completeness.

30. Validation applies only to the artifacts and conditions actually evaluated.

31. Mathematical consistency and empirical validation remain distinct.

## 111. Conformance Requirements

A later TR-EIF mathematical construction conforms to the properties in this chapter when:

- it preserves the balanced ternary transition relation;
- it preserves active neutral semantics;
- it does not infer transition validity from final state alone;
- it maintains state-space typing;
- it declares every continuous-discrete conversion;
- it represents required history explicitly;
- it preserves graph and geometry distinctions;
- it defines resonance relative to declared coordinates;
- it declares transformation actions before symmetry claims;
- it preserves structural-transition conditions;
- it identifies information loss in projections and scale mappings;
- it distinguishes observables from complete states;
- it distinguishes mathematical objects from numerical realizations;
- it preserves deterministic replay dependencies;
- it keeps invariant failures visible.

## 112. Final Fundamental Property Statement

The defining mathematical behavior of TR-EIF does not arise from one isolated equation.

It arises from the coupled preservation of:

`typed state spaces`

`→ balanced ternary -1/0/1 semantics`

`→ active neutral mediation`

`→ explicit continuous-discrete mappings`

`→ nonlinear and history-dependent evolution`

`→ graph-structured interatomic relations`

`→ circular phase organization`

`→ finite resonance regions`

`→ declared symmetry actions`

`→ invariant and equivariant mappings`

`→ explicit structural transitions`

`→ recursive inheritance`

`→ multiscale information mappings`

`→ observable projections`

`→ deterministic numerical realization`

`→ traceable invariant validation`

These properties form the mathematical consequences of the TR-EIF foundations established in Volume 01 and constrain all subsequent mathematical and computational layers.
