# Fundamental Lemmas

## 1. Purpose

This chapter establishes the fundamental lemmas of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The lemmas are derived from the definitions, axioms, state spaces, operators, mathematical structures, mappings, and framework invariants established in Chapters 01–08.

They provide intermediate results required for the fundamental theorems developed in Chapter 10.

The principal subjects are:

- typed mapping composition;
- state-space preservation;
- balanced ternary closure;
- active-neutral mediation;
- opposite-polarity reachability;
- pending-route consistency;
- resonance-classification separation;
- continuous-discrete separation;
- circular phase representation;
- equivariance under composition;
- invariant aggregation;
- dimensional consistency;
- history and memory closure;
- information loss under non-injective mappings;
- cross-scale mapping composition;
- numerical representation boundaries;
- integrated TR-EIF mapping consistency.

All lemmas are stated within explicit domains.

No result is generalized beyond its stated assumptions.

---

## 2. Lemma Convention

Each lemma contains:

1. assumptions;
2. statement;
3. proof;
4. scope.

The proof establishes only the stated result.

The provenance of lemmas in this chapter is:

`DERIVED`

unless explicitly stated otherwise.

---

## 3. Lemma 1 — Typed Composition Closure

### Assumptions

Let:

`F: X → Y`

and:

`G: Y → Z`.

### Statement

The composition:

`G ∘ F`

is a well-defined mapping:

`G ∘ F: X → Z`.

### Proof

For every:

`x ∈ X`

the definition of `F` gives:

`F(x) ∈ Y`.

Because:

`G: Y → Z`

the value:

`G(F(x))`

is defined and belongs to:

`Z`.

Therefore:

`(G ∘ F)(x) = G(F(x)) ∈ Z`

for every:

`x ∈ X`.

Hence:

`G ∘ F: X → Z`.

### Scope

This lemma applies whenever the codomain of the first mapping is contained in the domain required by the second mapping.

---

## 4. Lemma 2 — Composition Failure under Type Mismatch

### Assumptions

Let:

`F: X → Y`

and:

`G: Z → W`

with no declared mapping or inclusion from:

`Y`

into:

`Z`.

### Statement

The formal composition:

`G ∘ F`

is not defined solely from the given mappings.

### Proof

For:

`x ∈ X`

the first mapping produces:

`F(x) ∈ Y`.

The mapping `G` requires an input in:

`Z`.

No assumption establishes that:

`F(x) ∈ Z`.

Therefore the expression:

`G(F(x))`

is not guaranteed to be defined.

Hence no valid composition follows from the stated mappings alone.

### Scope

This result establishes the necessity of an explicit intermediate mapping whenever adjacent semantic spaces are incompatible.

---

## 5. Lemma 3 — Product-State Projection Consistency

### Assumptions

Let:

`X = X_1 × X_2 × ... × X_n`

and:

`x = (x_1, ..., x_n) ∈ X`.

Let:

`pi_i: X → X_i`

be the canonical projection.

### Statement

For each:

`i ∈ {1, ..., n}`

the projection satisfies:

`pi_i(x) = x_i`.

### Proof

This follows directly from the definition of Cartesian-product projection.

Since:

`x ∈ X`

each component satisfies:

`x_i ∈ X_i`.

Therefore:

`pi_i(x) ∈ X_i`

and equals the corresponding component.

### Scope

The result applies to any product state space used throughout TR-EIF.

---

## 6. Lemma 4 — State-Space Membership Preservation under Closed Mapping

### Assumptions

Let:

`F: X → X`.

### Statement

If:

`x ∈ X`

then:

`F(x) ∈ X`.

### Proof

The codomain of `F` is:

`X`.

Therefore, by definition of mapping:

`F(x) ∈ X`

for every:

`x ∈ X`.

### Scope

This is a basic closure result for state-update mappings.

It does not establish any stronger invariant beyond membership in `X`.

---

## 7. Lemma 5 — Exact Closure of the Balanced Ternary Domain

### Assumptions

Let:

`T = {-1, 0, 1}`.

Let:

`F_T: T → T`.

### Statement

For every:

`t ∈ T`

the value:

`F_T(t)`

belongs exactly to:

`{-1, 0, 1}`.

### Proof

The codomain of:

`F_T`

is:

`T`.

Therefore:

`F_T(t) ∈ T`.

Since:

`T = {-1, 0, 1}`

the output must be exactly one of:

`-1`

`0`

`1`.

### Scope

This result applies to mappings explicitly typed:

`T → T`.

It does not authorize any transition prohibited by the ternary transition relation.

---

## 8. Lemma 6 — Active Neutral Is an Internal Ternary State

### Assumptions

Let:

`T = {-1, 0, 1}`.

### Statement

The value:

`0`

is an element of the balanced ternary state space and is therefore internal to the ternary state domain.

### Proof

By explicit definition:

`T = {-1, 0, 1}`.

Therefore:

`0 ∈ T`.

Hence active neutral is not external metadata, missingness, or an out-of-domain marker.

### Scope

This lemma concerns domain membership.

Its operational roles follow from the framework axioms and execution semantics.

---

## 9. Lemma 7 — Direct Opposite Transition Exclusion

### Assumptions

Let:

`R_T ⊆ T × T`

be the committed ternary transition relation.

Assume:

`(-1, 1) ∉ R_T`

and:

`(1, -1) ∉ R_T`.

### Statement

No single committed transition governed by:

`R_T`

can map:

`-1`

directly to:

`1`

or:

`1`

directly to:

`-1`.

### Proof

A committed transition:

`a → b`

is admissible only when:

`(a, b) ∈ R_T`.

By assumption:

`(-1, 1) ∉ R_T`

and:

`(1, -1) ∉ R_T`.

Therefore neither direct opposite transition is admissible.

### Scope

This lemma applies to committed ternary transitions.

It does not prohibit an upstream target from requesting opposite polarity.

---

## 10. Lemma 8 — Necessity of Neutral Mediation

### Assumptions

Let:

`T = {-1, 0, 1}`.

Assume direct opposite transitions are excluded:

`(-1, 1) ∉ R_T`

and:

`(1, -1) ∉ R_T`.

Assume the admissible polarity-changing transitions include:

`(-1, 0)`

`(0, 1)`

`(1, 0)`

`(0, -1)`.

### Statement

Any admissible committed transition path from:

`-1`

to:

`1`

must include:

`0`.

Any admissible committed transition path from:

`1`

to:

`-1`

must include:

`0`.

### Proof

The ternary domain contains exactly three states:

`-1`

`0`

`1`.

A path from:

`-1`

to:

`1`

cannot use the direct edge:

`(-1, 1)`.

The only remaining state capable of occurring between the endpoints is:

`0`.

Therefore any admissible path changing from:

`-1`

to:

`1`

must contain:

`0`.

The reverse argument applies identically to a path from:

`1`

to:

`-1`.

### Scope

This result follows from the exact three-state domain and exclusion of the direct opposite edges.

---

## 11. Lemma 9 — Minimum Opposite-Polarity Path Length

### Assumptions

Use the conditions of Lemma 8.

Define path length as the number of committed non-retention edges.

### Statement

Every admissible path from:

`-1`

to:

`1`

has length at least:

`2`.

Every admissible path from:

`1`

to:

`-1`

has length at least:

`2`.

### Proof

A path of length one would require the direct edge:

`-1 → 1`

or:

`1 → -1`.

Both are forbidden.

By Lemma 8, the path must pass through:

`0`.

Thus the shortest possible paths are:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each contains two non-retention edges.

Therefore the minimum path length is:

`2`.

### Scope

Retention events may increase the path length but cannot reduce it below two.

---

## 12. Lemma 10 — Neutral State Is a Vertex Cut for Opposite Polarities

### Assumptions

Consider the canonical ternary transition graph with vertices:

`{-1, 0, 1}`

and no direct opposite edge.

### Statement

Removing vertex:

`0`

eliminates every admissible directed path between:

`-1`

and:

`1`.

### Proof

After removing:

`0`

the remaining vertex set is:

`{-1, 1}`.

By assumption, neither:

`-1 → 1`

nor:

`1 → -1`

exists as a committed edge.

Therefore no directed path exists between the two remaining opposite-polarity vertices.

Hence:

`0`

is a vertex cut separating opposite polarities.

### Scope

This graph-theoretic result formalizes the mediation role of active neutral.

---

## 13. Lemma 11 — First-Leg Completion Does Not Imply Second-Leg Completion

### Assumptions

Let:

`t_exec = -1`

and:

`t_target = 1`.

Let the first committed event produce:

`t_exec' = 0`.

### Statement

The fact that:

`-1 → 0`

has occurred does not logically imply that:

`0 → 1`

has already occurred or is automatically authorized.

### Proof

The first committed event has post-state:

`t_exec' = 0`.

The second event would require a distinct state transition:

`0 → 1`.

By the independent-leg invariant, each arrow is a separate committed event.

Therefore completion of the first event establishes only:

`t_exec' = 0`.

It does not establish the occurrence or authorization of the second event.

### Scope

The reverse route:

`1 → 0 → -1`

follows identically.

---

## 14. Lemma 12 — Neutral Retention Does Not Destroy Route Possibility

### Assumptions

Let:

`t_exec = 0`

and let a valid pending destination:

`t_pending ∈ {-1, 1}`

be retained.

Assume:

`0 → 0`

is admissible.

### Statement

Any finite number of neutral-retention events leaves the system in an executed state compatible with later second-leg completion, provided the pending destination remains valid.

### Proof

Each retention event maps:

`0 → 0`.

Therefore after any finite number of such events:

`t_exec = 0`.

If:

`t_pending`

is preserved, the pending route state remains available.

Thus the structural precondition:

`t_exec = 0`

for later completion remains satisfied.

Whether the second leg is actually authorized depends on the separate authorization condition.

### Scope

This lemma does not impose a maximum neutral residence duration.

---

## 15. Lemma 13 — Pending Destination Is Not Equivalent to Executed State

### Assumptions

Let:

`t_exec ∈ T_exec`

and:

`t_pending ∈ X_pending`.

Let:

`X_pending = {NONE, -1, 1}`.

### Statement

The pending destination and executed state are distinct semantic objects even when their numerical polarity values coincide.

### Proof

The variables belong to different semantic spaces:

`t_exec ∈ T_exec`

and:

`t_pending ∈ X_pending`.

Furthermore:

`X_pending`

contains:

`NONE`

while:

`T_exec`

contains active:

`0`.

Thus the two spaces are not identical.

Equality of numerical polarity in a particular state does not establish equality of semantic roles.

### Scope

This distinction remains necessary for staged opposite-polarity routing.

---

## 16. Lemma 14 — Target and Executed State Can Differ Consistently

### Assumptions

Let:

`t_target ∈ T_target`

and:

`t_exec ∈ T_exec`.

The value sets are both:

`{-1, 0, 1}`

but their semantic roles are distinct.

### Statement

A state satisfying:

`t_target ≠ t_exec`

is not contradictory.

### Proof

The variables occupy different semantic state components.

The target represents a requested or computed destination.

The executed state represents the retained committed state.

The execution mechanism may delay, mediate, reject, or stage the transition.

Therefore equality is not required at every execution coordinate.

### Scope

This result applies to all TR-EIF realizations preserving explicit target/execution separation.

---

## 17. Lemma 15 — Opposite Target Requires an Intermediate Executed Neutral State

### Assumptions

Let:

`t_exec[k] = -1`

and:

`t_target[k] = 1`.

Assume the target is eventually reached through valid committed transitions.

### Statement

There exists at least one later execution coordinate:

`m > k`

such that:

`t_exec[m] = 0`

before the first execution coordinate at which:

`t_exec = 1`.

### Proof

By Lemma 8, every admissible committed path from:

`-1`

to:

`1`

must include:

`0`.

Since the target is assumed eventually reached, the executed trajectory contains an admissible path from:

`-1`

to:

`1`.

Therefore an intermediate execution coordinate exists with executed state:

`0`.

### Scope

The result does not specify how long the system remains in neutral state.

---

## 18. Lemma 16 — Three-Class Resonance Classification Is Not Ternary Identity

### Assumptions

Let:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`

and:

`T = {-1, 0, 1}`.

No explicit bijection between:

`K_R`

and:

`T`

is defined.

### Statement

No elementwise identity between the two classification spaces follows from their equal cardinality.

### Proof

Both sets contain three elements.

Equal cardinality establishes only that a bijection can exist.

It does not specify which bijection, nor does it establish semantic equality between their elements.

Therefore statements such as:

`OUTSIDE = -1`

`BOUNDARY = 0`

`INSIDE = 1`

do not follow from cardinality alone.

### Scope

An explicit model may define a mapping between the spaces, but that mapping is an additional mathematical object.

---

## 19. Lemma 17 — Resonance Classification Composition Requires a Separate Ternary Mapping

### Assumptions

Let:

`C_R: X_R → K_R`.

Let ternary target space be:

`T_target`.

### Statement

A mapping from:

`X_R`

to:

`T_target`

through resonance classification requires an additional mapping:

`P_KT: K_R → T_target`

or another explicitly typed relation.

### Proof

The codomain of:

`C_R`

is:

`K_R`.

The desired target codomain is:

`T_target`.

Because:

`K_R`

and:

`T_target`

are distinct semantic spaces, direct composition into ternary state requires a mapping whose domain contains:

`K_R`

and whose codomain is:

`T_target`.

Therefore:

`P_KT`

or an equivalent explicit mapping is required.

### Scope

This result does not require the ternary target to depend only on resonance classification.

Auxiliary state may enlarge the domain.

---

## 20. Lemma 18 — Resonance-Window Membership Does Not Determine Bifurcation

### Assumptions

Let:

`r ∈ X_R`

and:

`W_R ⊂ X_R`.

Let:

`M_R(r)`

be a window-membership predicate.

### Statement

A change in:

`M_R(r)`

does not, from window membership alone, establish a bifurcation of the underlying dynamical system.

### Proof

The predicate:

`M_R`

classifies the location of:

`r`

relative to:

`W_R`.

A bifurcation concerns a qualitative structural change in a parameterized dynamical system.

No parameterized dynamical-family information, critical parameter condition, or change in dynamical structure is contained in the membership predicate alone.

Therefore window-membership change is insufficient to establish bifurcation.

### Scope

A particular model may exhibit a bifurcation at a resonance-window crossing, but additional bifurcation conditions are then required.

---

## 21. Lemma 19 — Phase Order Does Not Determine a Distinct Coherence Observable

### Assumptions

Let:

`P_order: X_phase → [0, 1]`

and:

`P_coh: X → X_C`

be separately defined mappings.

### Statement

Knowledge of:

`R = P_order(Theta)`

alone does not determine:

`C = P_coh(x)`

unless an additional relation between the two observables is defined.

### Proof

The mappings have distinct domains or codomains and independent definitions.

No functional relation:

`C = F(R)`

has been assumed.

Therefore one observable cannot be reconstructed from the other solely from the definitions given.

### Scope

This formalizes:

`R(t) ≠ C(t)`

as a mapping-level distinction.

---

## 22. Lemma 20 — Circular Representative Invariance

### Assumptions

Let:

`theta ∈ S^1 = R / (2 pi Z)`.

Let:

`theta_a`

and:

`theta_b`

be real representatives satisfying:

`theta_b = theta_a + 2 pi k`

for some:

`k ∈ Z`.

### Statement

The two representatives denote the same phase state.

### Proof

By definition of the quotient:

`R / (2 pi Z)`

two real numbers are equivalent when they differ by:

`2 pi k`

for:

`k ∈ Z`.

Therefore:

`theta_a`

and:

`theta_b`

belong to the same equivalence class in:

`S^1`.

### Scope

This result applies to oscillator phase, not to unrestricted real-valued state variables.

---

## 23. Lemma 21 — Wrapped Phase Difference Is Representative-Independent

### Assumptions

Let:

`theta_a`

and:

`theta_b`

be phases in:

`S^1`.

Let alternative representatives be:

`theta_a' = theta_a + 2 pi m`

and:

`theta_b' = theta_b + 2 pi n`

for:

`m, n ∈ Z`.

Let:

`Delta_S1`

return the canonical wrapped difference modulo:

`2 pi`.

### Statement

The wrapped phase difference is unchanged by the choice of representatives.

### Proof

The unwrapped difference of the alternative representatives is:

`theta_a' - theta_b'`

`= theta_a - theta_b + 2 pi(m - n)`.

The two differences therefore differ by an integer multiple of:

`2 pi`.

Wrapping modulo:

`2 pi`

maps both to the same element of the chosen canonical interval.

Hence:

`Delta_S1(theta_a', theta_b') = Delta_S1(theta_a, theta_b)`.

### Scope

This lemma supports representative-independent circular comparisons.

---

## 24. Lemma 22 — Phase Lag Does Not Introduce Temporal History

### Assumptions

Consider an interaction term:

`sin(theta_j(t) - theta_i(t) - gamma)`.

Assume:

`gamma`

is a phase-lag parameter and no delayed argument appears.

### Statement

The interaction term does not require access to past phase state solely because:

`gamma`

is nonzero.

### Proof

The expression depends on:

`theta_j(t)`

`theta_i(t)`

and:

`gamma`.

All phase values are evaluated at current time:

`t`.

No state of the form:

`theta(t - tau)`

appears.

Therefore no temporal-history access is introduced by the phase lag alone.

### Scope

This lemma establishes the mathematical distinction:

`phase lag ≠ temporal delay`.

---

## 25. Lemma 23 — Explicit Delay Requires History Access

### Assumptions

Let an evolution law contain:

`x(t - tau)`

with:

`tau > 0`.

### Statement

Evaluation of the delayed term at time:

`t`

requires knowledge of state at an earlier time:

`t - tau`.

### Proof

The argument of the state function is:

`t - tau < t`.

Therefore the current value:

`x(t)`

alone does not supply the delayed value unless the system state has been extended so that the required past information is encoded in the present complete state.

Hence either explicit history or an equivalent memory representation is required.

### Scope

This result applies to genuine delayed-state dependence.

---

## 26. Lemma 24 — Extended-State Representation of Finite Memory

### Assumptions

Suppose a discrete evolution has the form:

`x[k+1] = F(x[k], x[k-1], ..., x[k-m])`

for finite:

`m ≥ 1`.

Define extended state:

`z[k] = (x[k], x[k-1], ..., x[k-m])`.

### Statement

The evolution can be represented as a first-order discrete update:

`z[k+1] = G(z[k])`

for an explicitly defined:

`G`.

### Proof

The first component of:

`z[k+1]`

is:

`F(x[k], ..., x[k-m])`.

The remaining components are shifted copies:

`x[k]`

`x[k-1]`

through:

`x[k-m+1]`.

Thus define:

`G(z[k])`

as:

`(F(x[k], ..., x[k-m]), x[k], ..., x[k-m+1])`.

Every component of:

`z[k+1]`

is determined by:

`z[k]`.

Hence the finite-memory evolution has a first-order representation on the extended state space.

### Scope

This lemma applies to finite discrete memory.

Continuous functional-delay systems may require function-valued history spaces.

---

## 27. Lemma 25 — Hidden Result-Affecting Memory Breaks State Closure

### Assumptions

Let a declared state be:

`x ∈ X`.

Suppose future evolution also depends on memory:

`m`

but:

`m`

is neither included in:

`x`

nor fixed by immutable parameters or current inputs.

### Statement

The declared state:

`x`

is not sufficient to determine future evolution.

### Proof

Two executions may have the same declared:

`x`

but different:

`m`.

Because future evolution depends on:

`m`

the next state may differ between these executions.

Therefore the future is not determined from:

`x`

alone.

Hence:

`x`

is not a closed complete state for that evolution.

### Scope

This result applies to deterministic state closure and reproducibility analysis.

---

## 28. Lemma 26 — Dimensional Compatibility of Addition

### Assumptions

Let physical quantities:

`a`

and:

`b`

have dimensions:

`dim(a)`

and:

`dim(b)`.

### Statement

A physically typed sum:

`a + b`

requires:

`dim(a) = dim(b)`.

### Proof

Addition combines quantities within the same additive physical space.

If the dimensions differ, the operands belong to different physical quantity spaces.

No direct addition operator is defined between those spaces without an explicit dimensional transformation.

Therefore dimensional equality is required for direct physical addition.

### Scope

This lemma concerns dimensional physical quantities.

Dimensionless numerical encodings remain subject to their source semantics.

---

## 29. Lemma 27 — Nondimensionalization Produces a Dimensionless Quantity

### Assumptions

Let:

`q`

and nonzero reference:

`q_ref`

satisfy:

`dim(q) = dim(q_ref)`.

Define:

`q_star = q / q_ref`.

### Statement

The quantity:

`q_star`

is dimensionless.

### Proof

The dimension of a quotient is the quotient of dimensions.

Thus:

`dim(q_star) = dim(q) / dim(q_ref)`.

Since:

`dim(q) = dim(q_ref)`

their ratio is:

`1`.

Therefore:

`q_star`

is dimensionless.

### Scope

This lemma assumes a valid nonzero reference scale.

---

## 30. Lemma 28 — Non-Injective Mapping Prevents Unique Reconstruction

### Assumptions

Let:

`F: X → Y`

be non-injective.

### Statement

There exists at least one output:

`y ∈ Y`

for which the source state cannot be uniquely reconstructed from:

`y`

using `F` alone.

### Proof

Since:

`F`

is non-injective, there exist:

`x_1 ≠ x_2`

such that:

`F(x_1) = F(x_2) = y`.

Given only:

`y`

there is no basis within:

`F`

for selecting uniquely between:

`x_1`

and:

`x_2`.

Therefore unique reconstruction is impossible from:

`y`

alone.

### Scope

Additional auxiliary information may restore reconstructibility.

---

## 31. Lemma 29 — Injective Mapping Preserves Source Distinguishability

### Assumptions

Let:

`F: X → Y`

be injective.

### Statement

Distinct source states have distinct images.

### Proof

Assume:

`x_1 ≠ x_2`.

If:

`F(x_1) = F(x_2)`

injectivity would imply:

`x_1 = x_2`

which contradicts the assumption.

Therefore:

`F(x_1) ≠ F(x_2)`.

### Scope

This result applies over the domain on which injectivity holds.

---

## 32. Lemma 30 — Composition of Injective Mappings Is Injective

### Assumptions

Let:

`F: X → Y`

and:

`G: Y → Z`

both be injective.

### Statement

The composition:

`G ∘ F: X → Z`

is injective.

### Proof

Suppose:

`G(F(x_1)) = G(F(x_2))`.

Since `G` is injective:

`F(x_1) = F(x_2)`.

Since `F` is injective:

`x_1 = x_2`.

Therefore:

`G ∘ F`

is injective.

### Scope

This result supports information-preservation analysis of mapping chains.

---

## 33. Lemma 31 — Non-Injective Stage Makes Complete Composite Reconstruction Impossible

### Assumptions

Let:

`F: X → Y`

be non-injective.

Let:

`G: Y → Z`

be any mapping.

### Statement

The composition:

`G ∘ F`

cannot be injective.

### Proof

Because `F` is non-injective, there exist:

`x_1 ≠ x_2`

with:

`F(x_1) = F(x_2)`.

Applying `G` gives:

`G(F(x_1)) = G(F(x_2))`.

Thus distinct source states have the same composite output.

Therefore:

`G ∘ F`

is non-injective.

### Scope

This result applies without additional side information outside the composition.

---

## 34. Lemma 32 — Composition of Equivariant Mappings Is Equivariant

### Assumptions

Let group:

`G_sym`

act on:

`X`

`Y`

and:

`Z`

through:

`rho_X`

`rho_Y`

and:

`rho_Z`.

Let:

`F: X → Y`

satisfy:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

Let:

`H: Y → Z`

satisfy:

`H(rho_Y(g)y) = rho_Z(g)H(y)`.

### Statement

The composition:

`H ∘ F: X → Z`

is equivariant:

`(H ∘ F)(rho_X(g)x) = rho_Z(g)(H ∘ F)(x)`.

### Proof

Starting from the left-hand side:

`(H ∘ F)(rho_X(g)x)`

`= H(F(rho_X(g)x))`.

By equivariance of `F`:

`= H(rho_Y(g)F(x))`.

By equivariance of `H`:

`= rho_Z(g)H(F(x))`.

Therefore:

`= rho_Z(g)(H ∘ F)(x)`.

Hence the composition is equivariant.

### Scope

The intermediate action:

`rho_Y`

must be the same action used by both mappings.

---

## 35. Lemma 33 — Invariant Mapping after Equivariant Mapping Produces an Invariant Composite

### Assumptions

Let:

`F: X → Y`

be equivariant:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

Let:

`H: Y → Z`

be invariant:

`H(rho_Y(g)y) = H(y)`.

### Statement

The composition:

`H ∘ F: X → Z`

is invariant.

### Proof

For:

`g ∈ G_sym`

and:

`x ∈ X`:

`(H ∘ F)(rho_X(g)x)`

`= H(F(rho_X(g)x))`

`= H(rho_Y(g)F(x))`

by equivariance of `F`.

By invariance of `H`:

`= H(F(x))`

`= (H ∘ F)(x)`.

Therefore the composite is invariant.

### Scope

This lemma is central to invariant readout from equivariant intermediate representations.

---

## 36. Lemma 34 — Sum of Permutation-Equivariant Local Contributions Is Permutation Invariant

### Assumptions

Let local scalar contributions:

`e_i`

transform under permutation:

`pi ∈ S_N`

by index reordering:

`e_i' = e_(pi^(-1)(i))`.

Define:

`E = sum_i e_i`.

### Statement

The total:

`E`

is invariant under permutation.

### Proof

After permutation:

`E' = sum_i e_i'`

`= sum_i e_(pi^(-1)(i))`.

Because:

`pi`

is a bijection on:

`{1, ..., N}`,

the index set is merely reordered.

Therefore:

`sum_i e_(pi^(-1)(i)) = sum_j e_j`.

Hence:

`E' = E`.

### Scope

This result applies to scalar local contributions and ordinary finite summation.

---

## 37. Lemma 35 — Relative Displacement Is Translation Invariant

### Assumptions

Let:

`r_i, r_j ∈ R^3`.

Define:

`r_ij = r_j - r_i`.

Apply global translation:

`r_i' = r_i + a`

`r_j' = r_j + a`.

### Statement

The relative displacement is unchanged:

`r_ij' = r_ij`.

### Proof

Compute:

`r_ij' = r_j' - r_i'`

`= (r_j + a) - (r_i + a)`

`= r_j - r_i`

`= r_ij`.

### Scope

This result applies to ordinary Cartesian displacement before periodic-image specialization.

---

## 38. Lemma 36 — Euclidean Distance Is Translation Invariant

### Assumptions

Use the conditions of Lemma 35.

Define:

`d_ij = ||r_j - r_i||`.

### Statement

Global translation leaves:

`d_ij`

unchanged.

### Proof

By Lemma 35:

`r_ij' = r_ij`.

Therefore:

`d_ij' = ||r_ij'||`

`= ||r_ij||`

`= d_ij`.

### Scope

The same reasoning applies under a consistent periodic displacement mapping.

---

## 39. Lemma 37 — Euclidean Distance Is Rotation Invariant

### Assumptions

Let:

`Q ∈ SO(3)`.

Let:

`r_ij' = Q r_ij`.

### Statement

The Euclidean distance is unchanged:

`||r_ij'||_2 = ||r_ij||_2`.

### Proof

Since:

`Q^T Q = I`,

we have:

`||Qr_ij||_2^2`

`= r_ij^T Q^T Q r_ij`

`= r_ij^T r_ij`

`= ||r_ij||_2^2`.

Both norms are nonnegative, therefore:

`||Qr_ij||_2 = ||r_ij||_2`.

### Scope

This result applies to orthogonal transformations, including the rotation subgroup.

---

## 40. Lemma 38 — Geometry Transformation Alone Does Not Define Ternary Transformation

### Assumptions

Let:

`rho_geo(g): X_EIF → X_EIF`

be a geometric transformation.

Let:

`t_exec ∈ T`.

No mapping:

`G_sym × T → T`

is defined.

### Statement

No ternary state change follows solely from application of:

`rho_geo(g)`.

### Proof

The geometric transformation acts on:

`X_EIF`.

The ternary state belongs to:

`T`.

No mapping from the geometric transformation to a ternary update has been specified.

Therefore no mathematical rule exists that transforms:

`t_exec`

solely because:

`rho_geo(g)`

was applied.

### Scope

A specific model may define such coupling explicitly.

---

## 41. Lemma 39 — Energy from Invariant Representation Is Invariant

### Assumptions

Let:

`P_INV: X_EIF → X_INV`

be invariant under:

`G_sym`.

Let:

`E_model: X_INV → R`.

### Statement

The composite energy:

`E_total = E_model ∘ P_INV`

is invariant under:

`G_sym`.

### Proof

For transformed input:

`rho_X(g)x`:

`E_total(rho_X(g)x)`

`= E_model(P_INV(rho_X(g)x))`.

By invariance of:

`P_INV`:

`P_INV(rho_X(g)x) = P_INV(x)`.

Therefore:

`E_total(rho_X(g)x) = E_model(P_INV(x))`

`= E_total(x)`.

### Scope

No additional transformation dependence may enter:

`E_model`.

---

## 42. Lemma 40 — Force and Energy Have Distinct Codomains

### Assumptions

Let:

`E: X_pos → R`

and:

`F_force: X_pos → R^(3N)`.

### Statement

The outputs of the two mappings are not the same mathematical type for:

`N ≥ 1`.

### Proof

Energy output belongs to:

`R`.

Force output belongs to:

`R^(3N)`.

For:

`N ≥ 1`

these codomains represent different mathematical and physical objects.

Therefore energy and force remain separately typed even when force is derived from the energy gradient.

### Scope

The result concerns semantic and codomain distinction.

---

## 43. Lemma 41 — Scalar Ternary State Cannot Be Identified with Force by Type Alone

### Assumptions

Let:

`t ∈ T = {-1, 0, 1}`.

Let:

`F_i ∈ R^3`.

No mapping:

`T → R^3`

is specified.

### Statement

The ternary state cannot be identified with mechanical force.

### Proof

The ternary state belongs to a finite categorical set.

The force belongs to a three-dimensional vector space with physical dimensions.

The two objects have different domains, codomains, algebraic structure, and dimensions.

Without an explicit mapping there is no mathematical identity between them.

### Scope

This lemma does not prohibit a model-defined ternary modulation of a force law.

---

## 44. Lemma 42 — Ternary State Cannot Be Identified with Energy by Type Alone

### Assumptions

Let:

`t ∈ T`.

Let energy:

`E ∈ R`

with physical energy dimension.

### Statement

No identity:

`t = E`

follows from their numerical representations.

### Proof

The ternary state is categorical and dimensionless within:

`T`.

Energy belongs to a physically dimensioned scalar space.

Even if an energy value numerically equals:

`-1`

`0`

or:

`1`

the semantic types remain different.

Therefore numerical coincidence does not establish identity.

### Scope

An explicit mapping from ternary state to an energy-model parameter may be defined separately.

---

## 45. Lemma 43 — Phase Relation Does Not Define a Bond Relation without Mapping

### Assumptions

Let:

`Delta theta_ij`

be a phase relation.

Let:

`B_ij`

be a chemical-bond state in a separately defined bond space.

No mapping from phase relation to bond state is defined.

### Statement

The phase relation does not determine:

`B_ij`.

### Proof

The phase relation and bond state belong to different semantic spaces.

Without a declared mapping:

`F_bond(Delta theta_ij, ...)`

there is no mathematical rule connecting them.

Therefore bond identity cannot be inferred from phase relation alone.

### Scope

A later interatomic model may introduce an explicit relationship.

---

## 46. Lemma 44 — Tolerance Comparison Cannot Change Exact Ternary Membership

### Assumptions

Let:

`x ∈ R`

with:

`x ∉ {-1, 0, 1}`.

Let:

`epsilon > 0`.

### Statement

The fact that:

`|x - t| ≤ epsilon`

for some:

`t ∈ T`

does not imply:

`x ∈ T`.

### Proof

Membership in:

`T`

is exact set membership.

Approximate numerical proximity to an element of:

`T`

does not change the value of:

`x`.

Therefore:

`x`

remains outside:

`T`

unless:

`x`

is exactly one of:

`-1`

`0`

`1`.

### Scope

A separate quantization or classification mapping may map `x` into `T_target`, but that is a mapping rather than exact membership.

---

## 47. Lemma 45 — Quantization Is Not Ternary Semantics

### Assumptions

Let:

`Q_num: X → {q_1, q_2, q_3}`

be a three-level numerical quantizer.

### Statement

The output set of:

`Q_num`

does not constitute the TR-EIF balanced ternary state space merely because it has three levels.

### Proof

Balanced ternary state requires the explicitly defined semantic domain:

`T = {-1, 0, 1}`

with active-neutral and transition semantics.

A generic three-level quantizer supplies only three numerical output levels.

Equal cardinality does not establish equality of state semantics or transition structure.

Therefore the quantizer is not automatically a ternary-state mapping.

### Scope

A specific encoding may deliberately represent `T`, but this requires an explicit semantic contract.

---

## 48. Lemma 46 — Snapshot Does Not Imply Restart Completeness

### Assumptions

Let:

`P_snap: X_comp → X_snap`

be a state projection.

Let:

`P_CP: X_comp → X_CP`

be a restart-complete checkpoint mapping.

No assumption establishes:

`X_snap = X_CP`.

### Statement

A snapshot is not necessarily sufficient for exact restart.

### Proof

A projection may discard state components.

A restart-complete checkpoint must retain every state component required to determine future execution under its declared restart contract.

Since no assumption states that the snapshot retains all such components, restart completeness does not follow.

### Scope

A particular snapshot format may also be a checkpoint if completeness is explicitly established.

---

## 49. Lemma 47 — Deterministic Replay Requires Complete Result-Affecting State

### Assumptions

Suppose deterministic future execution depends on complete state:

`x_complete`.

Suppose a restart representation omits result-affecting component:

`z`.

### Statement

Exact deterministic replay from the incomplete representation is not guaranteed.

### Proof

Two complete states may share the same retained incomplete representation while differing in:

`z`.

Because:

`z`

affects future execution, the two continuations may diverge.

Therefore the incomplete representation does not uniquely determine future execution.

Hence exact deterministic replay is not guaranteed.

### Scope

This lemma motivates checkpoint closure without prescribing a specific serialization format.

---

## 50. Lemma 48 — Rejected Proposal Cannot Change Retained State under Rollback Semantics

### Assumptions

Let retained state be:

`x_acc`.

Let proposal be:

`x_prop`.

Assume rejection semantics define:

`Rollback(x_acc, x_prop) = x_acc`.

### Statement

A rejected proposal leaves retained state unchanged.

### Proof

By the definition of rollback:

`Rollback(x_acc, x_prop) = x_acc`.

Therefore the post-rejection retained state equals the pre-proposal accepted state.

### Scope

This result applies only to execution models implementing the stated rollback semantics.

---

## 51. Lemma 49 — Request Does Not Imply Commit

### Assumptions

Let:

`F_req: X → X_req`

and:

`F_commit: X × X_auth → X`.

### Statement

Generation of:

`q_req ∈ X_req`

does not itself imply a committed state change.

### Proof

The request belongs to:

`X_req`.

Commit requires an authorization object:

`X_auth`

and application of:

`F_commit`.

No identity or automatic mapping from request to committed state has been assumed.

Therefore request generation alone does not establish state mutation.

### Scope

This supports the request → authorization → commit architecture.

---

## 52. Lemma 50 — Authorization Does Not Equal Commit

### Assumptions

Let:

`a_auth ∈ X_auth`.

Let committed state update be performed only by:

`F_commit`.

### Statement

Existence of authorization does not mean the state has already been committed.

### Proof

Authorization is an object in:

`X_auth`.

Commit is a separate mapping:

`F_commit`.

Until this mapping is applied, the retained state need not change.

Therefore:

`authorization ≠ commit`.

### Scope

This applies to architectures preserving explicit commit boundaries.

---

## 53. Lemma 51 — Cross-Scale Composition Is Typed

### Assumptions

Let:

`M_ab: X^(ell_a) → X^(ell_b)`

and:

`M_bc: X^(ell_b) → X^(ell_c)`.

### Statement

The composite:

`M_bc ∘ M_ab`

is a valid mapping:

`X^(ell_a) → X^(ell_c)`.

### Proof

By:

`M_ab`

every source state maps into:

`X^(ell_b)`.

This is exactly the domain of:

`M_bc`.

Therefore the composition is defined and maps into:

`X^(ell_c)`.

### Scope

This establishes type compatibility only.

It does not establish information preservation or thermodynamic consistency.

---

## 54. Lemma 52 — Information Lost at a Fine-to-Coarse Stage Cannot Be Restored by Later Coarse Mapping Alone

### Assumptions

Let:

`M_ab: X_a → X_b`

be non-injective.

Let:

`M_bc: X_b → X_c`.

### Statement

The composite:

`M_bc ∘ M_ab`

cannot uniquely preserve all distinctions in:

`X_a`.

### Proof

By non-injectivity there exist:

`x_1 ≠ x_2`

such that:

`M_ab(x_1) = M_ab(x_2)`.

Then:

`M_bc(M_ab(x_1)) = M_bc(M_ab(x_2))`.

Thus the composite cannot distinguish:

`x_1`

from:

`x_2`.

### Scope

Additional side information may enable reconstruction, but not the composite mapping alone.

---

## 55. Lemma 53 — Scale Identity Is Preserved by Explicitly Typed Transfer

### Assumptions

Let:

`M_ab: X^(ell_a) → X^(ell_b)`.

### Statement

The source and target scale identities remain distinguishable after mapping.

### Proof

The source is explicitly typed as:

`X^(ell_a)`.

The target is explicitly typed as:

`X^(ell_b)`.

The mapping connects the two spaces but does not identify them.

Therefore scale identity is preserved as part of the mapping type.

### Scope

This result applies to explicitly typed multiscale mappings.

---

## 56. Lemma 54 — Validation Result Is Not Ternary State

### Assumptions

Let:

`K_val = {PASS, FAIL, UNRESOLVED}`

and:

`T = {-1, 0, 1}`.

No mapping between the sets is defined.

### Statement

A validation result cannot be identified with a balanced ternary state by set cardinality or positional analogy.

### Proof

The two sets have different semantic definitions.

Equal cardinality does not imply semantic identity.

In particular:

`UNRESOLVED`

means a validation outcome, while:

`0`

means active ternary neutral.

Therefore:

`UNRESOLVED ≠ 0`.

### Scope

A separate reporting mapping may encode validation results numerically, but this does not alter their semantics.

---

## 57. Lemma 55 — Missingness Is Distinct from Active Neutral

### Assumptions

Let:

`T_optional = T ∪ {NONE}`

with:

`NONE ∉ T`.

### Statement

`NONE`

and:

`0`

are distinct states in the optional representation.

### Proof

By construction:

`NONE ∉ T`.

But:

`0 ∈ T`.

Therefore:

`NONE ≠ 0`.

### Scope

This lemma applies to optional representations of ternary state.

---

## 58. Lemma 56 — Serialization Can Preserve Semantic Ternary State Only if Encoding Is Injective on T

### Assumptions

Let:

`Enc_T: T → X_ser`

encode ternary state.

### Statement

If two distinct ternary states have the same serialized representation, exact ternary-state recovery is impossible from that representation alone.

### Proof

Suppose:

`t_1 ≠ t_2`

but:

`Enc_T(t_1) = Enc_T(t_2)`.

Then deserialization receives the same serialized value for two distinct source states.

No deterministic decoder can return both original values uniquely.

Therefore exact recovery requires injectivity on:

`T`.

### Scope

This lemma applies to semantic ternary serialization.

---

## 59. Lemma 57 — Explicit Encoding Can Preserve Active Neutral Distinctly from Missingness

### Assumptions

Let:

`T_optional = {-1, 0, 1, NONE}`.

Let:

`Enc`

be injective on:

`T_optional`.

### Statement

The encoded representations of:

`0`

and:

`NONE`

are distinct.

### Proof

Because `Enc` is injective and:

`0 ≠ NONE`,

injectivity implies:

`Enc(0) ≠ Enc(NONE)`.

### Scope

This provides the minimal encoding condition required to preserve active-neutral semantics.

---

## 60. Lemma 58 — Forward TR-EIF Composition Produces a Target, Not an Executed State

### Assumptions

Let:

`P_EQ: X_EIF → X_EQ`.

Let:

`P_ER: X_EQ → X_R`.

Let:

`P_RT: X_R → T_target`.

Define:

`F_forward = P_RT ∘ P_ER ∘ P_EQ`.

### Statement

The codomain of:

`F_forward`

is:

`T_target`

and not:

`T_exec`.

### Proof

By typed composition:

`P_EQ`

maps into:

`X_EQ`;

`P_ER`

maps:

`X_EQ`

into:

`X_R`;

`P_RT`

maps:

`X_R`

into:

`T_target`.

Therefore the final codomain is:

`T_target`.

No ternary execution mapping appears in the composition.

Hence the result is a target, not an executed state.

### Scope

This lemma formalizes the upstream execution boundary.

---

## 61. Lemma 59 — Executed Ternary Update Requires an Execution Mapping

### Assumptions

Use the forward mapping of Lemma 58.

Let:

`E_T: X_Texec × X_ctrl → X_Texec`.

### Statement

A change in:

`t_exec`

requires application of:

`E_T`

or another explicitly equivalent execution mapping.

### Proof

The forward mapping ends in:

`T_target`.

By target/execution separation:

`T_target`

does not mutate:

`T_exec`

by identity.

The mapping:

`E_T`

is the declared structure responsible for executed-state evolution.

Therefore an executed-state change requires an execution mapping.

### Scope

This result applies to the canonical TR-EIF integration architecture.

---

## 62. Lemma 60 — EIF-to-TR Mapping Does Not Erase EIF State Type

### Assumptions

Let:

`F_E→TR: X_EIF → X_TR,in`.

### Statement

The existence of:

`F_E→TR`

does not imply:

`X_EIF = X_TR,in`.

### Proof

A mapping can connect distinct spaces.

Equality of domain and codomain is not part of the definition unless explicitly stated.

The mapping itself exists precisely to transform an object from one typed space into another.

Therefore the source and target spaces remain distinct.

### Scope

This formalizes separation-before-integration.

---

## 63. Lemma 61 — TR-to-EIF Feedback Request Is Not Committed EIF State

### Assumptions

Let:

`F_TR→E: X_TR × X_EIF → X_EIF,req`.

### Statement

The output of:

`F_TR→E`

belongs to:

`X_EIF,req`

and therefore is not, by type alone, a committed state in:

`X_EIF`.

### Proof

By definition:

`F_TR→E`

has codomain:

`X_EIF,req`.

Committed EIF state belongs to:

`X_EIF`.

Since the two semantic spaces are distinct, the output is a request rather than retained EIF state.

### Scope

A later authorization and commit mapping may convert an admissible request into updated EIF state.

---

## 64. Lemma 62 — Integrated Feedback Cannot Bypass Ternary Transition Invariants

### Assumptions

Let:

`t_exec`

be part of integrated state.

Assume all valid integrated updates must preserve the framework invariants.

### Statement

No EIF feedback, learning update, MD step, or multiscale mapping can validly produce a direct committed:

`-1 → 1`

or:

`1 → -1`

transition in:

`t_exec`.

### Proof

The opposite-transition exclusion is a framework-wide invariant on executed ternary state.

Any integrated mapping that changes:

`t_exec`

while violating that invariant produces a state outside the admissible framework relation.

Therefore such an update is not a valid TR-EIF state transition.

### Scope

This applies to any integrated mechanism with authority to affect executed ternary state.

---

## 65. Lemma 63 — Equivariance of a Submodule Does Not Establish Equivariance of a Non-Equivariant Composition

### Assumptions

Let:

`F: X → Y`

be equivariant.

Let:

`G: Y → Z`

not satisfy the required equivariance relation.

### Statement

Equivariance of:

`F`

alone is insufficient to establish equivariance of:

`G ∘ F`.

### Proof

For the composite to be equivariant, one requires:

`G(F(rho_X(g)x)) = rho_Z(g)G(F(x))`.

Equivariance of `F` gives:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

Thus the required equality becomes:

`G(rho_Y(g)F(x)) = rho_Z(g)G(F(x))`.

This is exactly an equivariance condition on:

`G`

over the image of `F`.

If `G` does not satisfy this relation, the composite need not be equivariant.

### Scope

This result motivates whole-chain equivariance validation.

---

## 66. Lemma 64 — Permutation-Invariant Aggregation Removes Storage-Order Dependence

### Assumptions

Let:

`Agg: X^N → Y`

satisfy:

`Agg(x_1, ..., x_N) = Agg(x_(pi(1)), ..., x_(pi(N)))`

for every:

`pi ∈ S_N`.

### Statement

The aggregate output is independent of storage ordering.

### Proof

Any storage reordering corresponds to some permutation:

`pi ∈ S_N`.

By permutation invariance, applying that permutation does not change the aggregate.

Therefore the output is independent of the chosen storage ordering.

### Scope

Semantic entity-associated values must be permuted consistently.

---

## 67. Lemma 65 — Scalar Equality Does Not Establish Semantic Equality

### Assumptions

Let two observables:

`a ∈ X_A`

and:

`b ∈ X_B`

have numerical representatives that happen to satisfy:

`a_num = b_num`.

Assume:

`X_A`

and:

`X_B`

are distinct semantic spaces.

### Statement

The numerical equality does not establish:

`a = b`

as semantic objects.

### Proof

Semantic identity requires equality within a common state or observable space.

Here the values belong to distinct spaces.

Their numeric carriers may coincide, but the objects retain different definitions, units, transformations, or interpretations.

Therefore numerical equality alone does not establish semantic identity.

### Scope

This applies, for example, to phase order and coherence, or ternary values and numerical observables.

---

## 68. Lemma 66 — Numerical Approximation Does Not Alter Formal Codomain

### Assumptions

Let:

`F: X → Y`

be a formal mapping.

Let:

`F_num`

be a numerical realization of `F`.

### Statement

Changing the numerical representation used by:

`F_num`

does not, by itself, redefine the formal codomain:

`Y`.

### Proof

The formal codomain is part of the definition of:

`F`.

A numerical representation specifies how elements or approximations of elements of:

`Y`

are encoded computationally.

Representation choice does not change the formal definition unless the mathematical model itself is revised.

### Scope

This result separates mathematical models from numerical realization.

---

## 69. Lemma 67 — Exact Invariant and Numerical Diagnostic Are Distinct

### Assumptions

Let exact invariant predicate be:

`I: X → {true, false}`.

Let numerical diagnostic be:

`D: X_num → R_0+`.

### Statement

A small diagnostic value does not logically replace the exact invariant predicate unless an explicit equivalence has been established.

### Proof

The two mappings have different codomains and definitions.

`I`

returns an exact logical state.

`D`

returns a numerical magnitude.

Without an additional theorem connecting a bound on:

`D`

to truth of:

`I`

the diagnostic and invariant remain distinct.

### Scope

This distinction is essential for exact ternary invariants versus floating numerical diagnostics.

---

## 70. Lemma 68 — Repository Representation Does Not Change Mathematical Meaning

### Assumptions

Let one mathematical object be represented consistently in:

- documentation;
- schema;
- source code;
- trace artifact.

Assume explicit encoding and decoding mappings preserve its semantic state.

### Statement

The change of repository representation does not change the underlying mathematical object.

### Proof

Each representation is connected to the same formal object through semantic-preserving mappings.

If those mappings preserve the defining information and type, the mathematical identity is unchanged even though serialized or implementation representations differ.

### Scope

This result requires semantic-preserving mappings.

Conflicting representations violate the premise.

---

## 71. Lemma 69 — FRP Executable Specialization Does Not Imply Formal Identity with TR-EIF

### Assumptions

Let:

`F_FRP`

be an executable realization of a selected TR-EIF formal mechanism:

`F_TR`.

### Statement

The existence of an implementation relation:

`F_TR → F_FRP`

does not imply:

`TR-EIF = FRP`.

### Proof

FRP realizes a selected subset or specialization of formal TR mechanisms.

TR-EIF additionally contains the broader formal TR architecture, EIF, learning, molecular dynamics, multiscale mappings, and reference-model structure.

Therefore realization of selected mappings does not establish identity of the complete systems.

### Scope

The architectural relation remains:

`TR-EIF formal theory → FRP executable specialization/reference`.

---

## 72. Lemma 70 — Implementation Parameter Reuse Does Not Establish Universality

### Assumptions

Let:

`p_impl`

be a parameter defined in an implementation specialization.

Suppose the same value is reused in several executions.

### Statement

Repeated use of:

`p_impl`

does not by itself make it a universal TR-EIF constant.

### Proof

Universality is a property of the formal theory, not of frequency of implementation reuse.

No assumption promotes:

`p_impl`

from implementation parameter to framework-wide constant.

Therefore its scope remains implementation-specific.

### Scope

Formal promotion requires a separate explicit definition.

---

## 73. Lemma 71 — Phase-Derived Target Remains Upstream of Neutral-Mediated Execution

### Assumptions

Let:

`P_phase→T: X_phase → T_target`.

Let current executed state be:

`t_exec`.

### Statement

The output of:

`P_phase→T`

does not bypass the ternary execution relation.

### Proof

The codomain of:

`P_phase→T`

is:

`T_target`.

Executed state belongs to:

`T_exec`.

By Lemma 59, changing executed state requires the execution mapping.

Therefore a phase-derived target remains upstream of neutral-mediated execution.

### Scope

This applies to FRP executable references and any other TR-EIF specialization using phase-derived targets.

---

## 74. Lemma 72 — Retained Frequency Memory Is a State Variable when It Affects Future Phase Evolution

### Assumptions

Let retained frequency:

`omega_ret`

affect future phase update.

### Statement

`omega_ret`

belongs to complete result-affecting state.

### Proof

By assumption, future phase evolution depends on the current retained frequency.

Two executions with identical visible phase state but different:

`omega_ret`

may therefore produce different future phase trajectories.

Hence retained frequency is necessary to determine future evolution and belongs to complete state.

### Scope

This lemma applies to implementations containing retained-frequency dynamics.

---

## 75. Lemma 73 — Retained Frequency Memory Does Not Imply Pairwise Delay

### Assumptions

Let phase evolution depend on retained frequency state:

`omega_ret`.

Assume no term of the form:

`theta_j(t - tau_ij)`

is present.

### Statement

The presence of retained-frequency memory does not establish explicit pairwise delayed phase coupling.

### Proof

Retained-frequency memory modifies phase evolution through an internal state variable.

Explicit pairwise delay requires past phase evaluation at:

`t - tau_ij`.

Since such an argument is absent by assumption, the two mechanisms are mathematically distinct.

### Scope

Both mechanisms may coexist in a different model if independently defined.

---

## 76. Lemma 74 — Phase-Order Aggregation Produces a Global Observable

### Assumptions

Let:

`Theta = (theta_1, ..., theta_N)`.

Define:

`Z = (1/N) sum_j exp(i theta_j)`.

Let:

`R = |Z|`.

### Statement

`R`

is a global observable of the complete phase configuration.

### Proof

The expression depends on all:

`theta_j`

through a system-wide sum.

Therefore:

`R`

is obtained by a mapping from:

`(S^1)^N`

into:

`[0, 1]`.

It is not a local phase state of any one oscillator.

### Scope

Subset or hierarchical order parameters require separately defined subsets or scales.

---

## 77. Lemma 75 — Global Phase Order Cannot Reconstruct the Full Phase State

### Assumptions

Let:

`N ≥ 2`.

Define:

`P_order: (S^1)^N → [0, 1]`

by the Kuramoto phase-order magnitude.

### Statement

`P_order`

is non-injective.

### Proof

Consider any phase configuration:

`Theta`.

Apply a common phase shift:

`theta_j' = theta_j + alpha`

for all `j`.

Then:

`Z' = exp(i alpha) Z`.

Therefore:

`|Z'| = |Z|`.

For:

`alpha`

not equal to an integer multiple of:

`2 pi`

the phase configurations are distinct as coordinate states, but they have the same:

`R`.

Therefore:

`P_order`

is non-injective.

### Scope

This proves that global phase-order magnitude does not contain the complete phase state.

---

## 78. Lemma 76 — Resonance Coordinate Reduction May Be Information-Losing

### Assumptions

Let:

`P_R: X_src → X_R`.

Suppose:

`P_R`

is non-injective.

### Statement

The resonance state:

`r = P_R(x)`

does not uniquely determine source state:

`x`.

### Proof

By non-injectivity, there exist:

`x_1 ≠ x_2`

with:

`P_R(x_1) = P_R(x_2)`.

Therefore the same resonance state can correspond to multiple source states.

Hence source-state reconstruction from:

`r`

alone is not unique.

### Scope

This is compatible with resonance classification because classification often intentionally reduces information.

---

## 79. Lemma 77 — Resonance Classification Is At Least as Information-Reducing as a Non-Injective Resonance Classifier

### Assumptions

Let:

`C_R: X_R → K_R`

be non-injective.

### Statement

The resonance class does not uniquely determine the resonance coordinate.

### Proof

Non-injectivity means there exist:

`r_1 ≠ r_2`

such that:

`C_R(r_1) = C_R(r_2)`.

Therefore one class label corresponds to multiple resonance states.

Hence classification is a reduced representation of resonance state.

### Scope

This is typical for window-based classification.

---

## 80. Lemma 78 — Ternary Target Is Generally a Reduced Representation of Upstream Continuous State

### Assumptions

Let:

`P_RT: X_R → T_target`.

Assume:

`X_R`

contains more than three distinguishable states and:

`P_RT`

maps into exactly three target values.

### Statement

`P_RT`

cannot be injective over all of:

`X_R`.

### Proof

The codomain contains exactly three values.

If the domain contains more than three distinct states, an injective mapping from the entire domain into a three-element codomain is impossible.

Therefore at least two distinct resonance states must share one ternary target.

### Scope

This follows from cardinality for finite domains and from the impossibility of injection from a set with cardinality greater than three into a three-element set.

---

## 81. Lemma 79 — Ternary Execution Can Preserve Information Not Present in Current Executed Polarity

### Assumptions

Let execution state contain:

`(t_exec, t_target, t_pending)`.

### Statement

Two execution states with identical:

`t_exec`

may remain distinguishable through target or pending state.

### Proof

Consider:

`x_1 = (0, 1, 1)`

and:

`x_2 = (0, -1, -1)`.

Both have:

`t_exec = 0`.

However their target and pending components differ.

Therefore the complete execution states are distinct even though the currently executed polarity is identical.

### Scope

This establishes why active neutral alone cannot encode pending-route semantics.

---

## 82. Lemma 80 — Projection to Executed Ternary State Is Non-Injective for Staged Execution

### Assumptions

Let:

`X_Texec = T_exec × T_target × X_pending`.

Define projection:

`pi_exec: X_Texec → T_exec`.

### Statement

`pi_exec`

is non-injective whenever more than one valid complete execution state shares the same executed polarity.

### Proof

Using the states:

`(0, 1, 1)`

and:

`(0, -1, -1)`,

their projections are both:

`0`.

The complete states differ.

Therefore:

`pi_exec`

is non-injective.

### Scope

The result demonstrates that executed polarity alone is not restart-complete for staged routes.

---

## 83. Lemma 81 — Exact Restart of Pending Routing Requires Pending-State Preservation

### Assumptions

Let two complete states have:

`t_exec = 0`

but different valid pending destinations.

Future execution may complete those pending routes.

### Statement

A checkpoint omitting pending destination cannot guarantee exact continuation of staged ternary execution.

### Proof

Two complete states can produce the same checkpoint representation if pending state is omitted.

Their future second-leg destinations can differ because one may target:

`1`

and the other:

`-1`.

Therefore the checkpoint does not uniquely determine continuation.

Hence exact restart requires preservation of pending-state information when pending routing is active.

### Scope

This applies only when pending destination affects future execution.

---

## 84. Lemma 82 — A Local Mapping Cannot Depend on Undeclared Global State

### Assumptions

Let:

`F_i: X_env,i → Y_i`

be declared local.

### Statement

If evaluation of:

`F_i`

requires a variable not contained in:

`X_env,i`

or fixed parameters, then the declared domain is incomplete.

### Proof

A mapping must have all result-affecting inputs in its domain or fixed parameter context.

If another global variable changes the output while not appearing in the domain, two identical declared inputs can produce different outputs.

Therefore:

`F_i`

is not fully defined as:

`X_env,i → Y_i`.

### Scope

The mapping may be corrected by extending its domain.

---

## 85. Lemma 83 — Scale-Aware Mapping Cannot Discard Scale Identity when Behavior Is Scale-Dependent

### Assumptions

Let mapping behavior differ between scales:

`ell_a`

and:

`ell_b`.

### Statement

A complete scale-dependent mapping must include scale identity explicitly or be represented as a scale-indexed family.

### Proof

If the same apparent input state produces different outputs at different scales, then scale affects the result.

A result-affecting variable must appear in the mapping domain or parameterization.

Therefore scale identity must be included explicitly or through a family:

`F^(ell)`.

### Scope

This applies to scale-dependent resonance, coarse graining, and multiscale closure.

---

## 86. Lemma 84 — A History-Dependent Resonance Window Cannot Be Fully Defined from Current Resonance Coordinates Alone

### Assumptions

Let:

`W_R = F_WR(h)`

with:

`h ∈ X_H`.

### Statement

Current resonance coordinate:

`r`

alone is insufficient to determine window membership in general.

### Proof

Two histories:

`h_1`

and:

`h_2`

may generate different windows:

`W_R(h_1) ≠ W_R(h_2)`.

For the same:

`r`

membership may therefore differ between the two windows.

Thus current resonance coordinate alone does not determine the classification.

### Scope

This lemma formalizes history-dependent and hysteretic resonance boundaries.

---

## 87. Lemma 85 — Structural Transition Cannot Be Derived from Ternary Transition without Mapping

### Assumptions

Let:

`t_exec ∈ T`

and:

`s ∈ X_S`.

No mapping:

`T × X_S → X_S`

or ternary-to-structural classifier is defined.

### Statement

A change in:

`t_exec`

does not mathematically determine a change in:

`s`.

### Proof

The two variables occupy separate state spaces.

No mapping connects the ternary transition to structural-state evolution.

Therefore the structural consequence is undefined from ternary change alone.

### Scope

An integrated model may define such a mapping explicitly.

---

## 88. Lemma 86 — Structural Transition Cannot Define Physical Phase Transition without Physical Classification Mapping

### Assumptions

Let:

`s ∈ X_S`

and:

`k_phys ∈ K_phys`.

No mapping:

`X_S → K_phys`

is defined.

### Statement

A structural-state transition does not determine a physical-phase transition.

### Proof

The physical phase classifier has a separate codomain and requires its own physical criterion.

Without a mapping from structural state to physical phase class, no mathematical implication exists.

### Scope

A material model may establish such a relation under explicit conditions.

---

## 89. Lemma 87 — Formal Mapping Chain Preserves Semantic Boundaries

### Assumptions

Consider the typed chain:

`X_EIF → X_EQ → X_R → K_R → T_target → T_exec`.

### Statement

Each intermediate object retains its semantic type even when all mappings are evaluated during one computational step.

### Proof

Each mapping has a separately declared codomain.

The output of one mapping becomes the input to another but does not thereby become identical to all later outputs.

Composition connects spaces; it does not identify them.

Therefore each intermediate representation remains semantically distinct.

### Scope

This applies regardless of whether an implementation stores intermediate values explicitly or computes them transiently, provided the semantics are preserved.

---

## 90. Lemma 88 — Integrated State Is More Informative than Any One Projection when Projection Is Non-Injective

### Assumptions

Let:

`X_TR-EIF = X_EIF × X_TR × X_int`.

Let:

`P: X_TR-EIF → Y`

be a non-injective projection.

### Statement

The projected value:

`P(x)`

cannot uniquely reconstruct the complete integrated state.

### Proof

By non-injectivity there exist:

`x_1 ≠ x_2`

with:

`P(x_1) = P(x_2)`.

Therefore the projected value does not distinguish all complete states.

Hence it contains less distinguishing information than the full integrated state.

### Scope

This applies to observables, traces, reduced descriptors, and classification outputs.

---

## 91. Lemma 89 — Repository-Level Semantic Consistency Requires Compatible Encodings

### Assumptions

Let one formal object:

`x ∈ X`

have documentation, schema, source-code, and artifact representations.

### Statement

If one representation maps the same encoded value to two incompatible semantic states, repository-wide semantic consistency is violated.

### Proof

A consistent representation system must preserve the formal object's semantic identity across layers.

If the same encoded value is interpreted as two incompatible states, the decoding relation is not well-defined.

Therefore the representation system cannot preserve a unique formal semantic object.

### Scope

This is particularly critical for `0`, `NONE`, target, executed state, and resonance classification.

---

## 92. Lemma 90 — Provenance Does Not Alter Mathematical Value

### Assumptions

Let:

`x ∈ X`

carry provenance:

`p_prov ∈ P_prov`.

### Statement

Changing provenance metadata without changing the underlying value does not mathematically transform:

`x`.

### Proof

The annotated representation may be:

`(x, p_prov)`.

The provenance component describes source or evidence status.

The mathematical component remains:

`x`.

Therefore provenance annotation is not a state transformation of the mathematical value itself.

### Scope

Invalid provenance metadata can still constitute a documentation or traceability error.

---

## 93. Lemma 91 — Derived Mapping Provenance Does Not Make Its Output a New State Type

### Assumptions

Let:

`F: X → Y`

be a derived mapping with provenance:

`DERIVED`.

### Statement

The provenance of the mapping does not alter the codomain type:

`Y`.

### Proof

Provenance classifies the origin of the mapping.

The codomain is defined independently by the mathematical mapping signature.

Therefore an output remains an element of:

`Y`

regardless of whether the mapping is:

`DERIVED`

`AUTHOR_DEFINED`

or otherwise classified.

### Scope

This preserves separation between provenance and state-space typing.

---

## 94. Lemma 92 — Exact Opposite-Transition Invariant Is Preserved under Any Conforming Specialization

### Assumptions

Let a specialization preserve the framework-wide ternary invariants.

### Statement

Its committed transition relation cannot contain:

`(-1, 1)`

or:

`(1, -1)`.

### Proof

Framework-wide invariant preservation is part of specialization conformance.

The exclusion of direct opposite transitions is a framework-wide ternary invariant.

Therefore any specialization containing either forbidden edge would contradict the preserved invariant and would not be conforming.

### Scope

A specialization may strengthen transition conditions but may not weaken this invariant.

---

## 95. Lemma 93 — Additional Scheduler Constraints Cannot Shorten the Minimum Opposite-Polarity Path

### Assumptions

Let the canonical ternary graph exclude direct opposite edges.

Let a scheduler specialization remove or delay some otherwise admissible transition events without adding forbidden direct edges.

### Statement

The minimum number of committed polarity-changing legs from one opposite state to the other cannot become less than two.

### Proof

The only way to obtain a one-leg opposite-polarity path is to add:

`-1 → 1`

or:

`1 → -1`.

By assumption the scheduler does not add these edges.

Removing or delaying admissible transitions cannot create a shorter path.

Therefore the minimum remains at least two.

### Scope

Scheduler restrictions may increase the number of execution steps or make a destination temporarily unreachable.

---

## 96. Lemma 94 — Retention Events Do Not Change Ternary Polarity

### Assumptions

Let:

`Hold_T(t) = t`.

### Statement

Any finite sequence of retention events leaves executed polarity unchanged.

### Proof

For one event:

`Hold_T(t) = t`.

Applying the same mapping repeatedly yields:

`Hold_T^n(t) = t`

for every finite nonnegative integer:

`n`.

Therefore retention does not change polarity.

### Scope

This applies to `-1`, `0`, and `1`.

---

## 97. Lemma 95 — Opposite-Polarity Route with Retention Still Contains Exactly Two Polarity-Changing Legs

### Assumptions

Consider an admissible path:

`-1 → 0`

followed by zero or more:

`0 → 0`

retentions, followed by:

`0 → 1`.

### Statement

The path contains exactly two polarity-changing committed edges.

### Proof

The first edge changes state from:

`-1`

to:

`0`.

Every retention edge:

`0 → 0`

does not change state.

The final edge changes:

`0`

to:

`1`.

Therefore exactly two edges change the executed ternary value.

### Scope

The reverse route is identical by symmetry of the transition topology.

---

## 98. Lemma 96 — Global Translation Does Not Change a Translation-Invariant Resonance Mapping

### Assumptions

Let:

`P_R: X_EIF → X_R`

be translation invariant:

`P_R(rho_trans(a)x) = P_R(x)`.

### Statement

A global translation of the source configuration leaves the resonance state unchanged.

### Proof

This is exactly the translation-invariance relation assumed for:

`P_R`.

Thus:

`r' = P_R(rho_trans(a)x)`

`= P_R(x)`

`= r`.

### Scope

This result applies only when the selected resonance mapping is translation invariant.

---

## 99. Lemma 97 — Equivariant Resonance Coordinates Transform Predictably

### Assumptions

Let:

`P_ER: X_EQ → X_R`

be equivariant with actions:

`rho_EQ`

and:

`rho_R`.

### Statement

For:

`g ∈ G_sym`

the transformed resonance state is:

`P_ER(rho_EQ(g)z) = rho_R(g)P_ER(z)`.

### Proof

This is the defining equivariance relation for:

`P_ER`.

Therefore the transformation of resonance coordinates is determined by:

`rho_R`.

### Scope

No claim of invariance follows unless:

`rho_R`

is the trivial action.

---

## 100. Lemma 98 — Invariant Resonance Classification from Equivariant Resonance State Requires Classifier Invariance

### Assumptions

Let:

`P_ER`

be equivariant into:

`X_R`.

Let:

`C_R: X_R → K_R`.

### Statement

The composite classification:

`C_R ∘ P_ER`

is invariant under the transformation group if:

`C_R(rho_R(g)r) = C_R(r)`.

### Proof

For transformed source representation:

`z' = rho_EQ(g)z`.

By equivariance:

`P_ER(z') = rho_R(g)P_ER(z)`.

Then:

`C_R(P_ER(z'))`

`= C_R(rho_R(g)P_ER(z))`.

By classifier invariance:

`= C_R(P_ER(z))`.

Therefore the composite classification is invariant.

### Scope

Classifier invariance is an explicit condition and cannot be inferred automatically.

---

## 101. Lemma 99 — Invariant Ternary Target under Geometry Requires Invariant Upstream Mapping Chain

### Assumptions

Let the chain be:

`X_EIF → X_EQ → X_R → T_target`.

Assume each composed stage yields a final target mapping:

`F_target: X_EIF → T_target`.

### Statement

The ternary target is invariant under transformation group:

`G_sym`

only if:

`F_target(rho_EIF(g)x) = F_target(x)`.

### Proof

Ternary target belongs to a discrete target space with no geometric polarity transformation assumed.

Therefore geometry invariance of the target requires equality of the final target under transformed input.

If any upstream stage causes the target to change, invariance fails.

Thus invariance is a property of the complete target mapping chain.

### Scope

A model could define nontrivial transformation behavior on ternary targets, but such behavior must be explicit.

---

## 102. Lemma 100 — The Canonical TR-EIF Chain Is Not an Identity Chain

### Assumptions

Consider:

`X_EIF`

`→ X_EQ`

`→ X_R`

`→ K_R`

`→ T_target`

`→ T_exec`.

### Statement

The chain cannot be treated as repeated identity mappings under the established framework definitions.

### Proof

The spaces differ in semantic type:

- interatomic state;
- equivariant representation;
- resonance coordinates;
- resonance classification;
- ternary target;
- executed ternary state.

At least several pairs have different cardinality, algebraic structure, transformation behavior, or execution role.

Therefore they cannot all be the same space connected by identity mappings.

Explicit transformations are required.

### Scope

This lemma summarizes the separation-before-integration architecture.

---

## 103. Fundamental Lemma Set

The lemmas established in this chapter imply the following derived structural facts.

1. Typed mappings compose only through compatible intermediate spaces.

2. Closed mappings preserve state-space membership.

3. The balanced ternary state domain is exactly:

`T = {-1, 0, 1}`.

4. Active neutral:

`0`

is internal to the ternary state space.

5. Direct opposite committed transitions are excluded.

6. Every opposite-polarity committed path contains active neutral.

7. The minimum opposite-polarity committed path contains at least two polarity-changing legs.

8. Active neutral separates opposite polarities in the canonical transition graph.

9. First-leg completion does not imply second-leg completion.

10. Neutral retention can occur between the two legs without collapsing the route.

11. Target, pending destination, and executed state are separately typed.

12. Equal cardinality does not identify resonance classification with balanced ternary state.

13. Resonance classification requires a separate mapping before it can produce ternary targets.

14. Resonance-window crossing alone does not establish bifurcation.

15. Circular phase results are independent of representative modulo `2 pi`.

16. Phase lag does not imply temporal delay.

17. Genuine delay requires history or an equivalent extended state.

18. Result-affecting memory belongs to complete state.

19. Physical addition requires dimensional compatibility.

20. Non-injective mappings lose unique source-state reconstructibility.

21. Composition of injective mappings remains injective.

22. A non-injective stage makes the complete downstream composition non-injective.

23. Composition of compatible equivariant mappings remains equivariant.

24. Invariant readout after an equivariant mapping produces an invariant composite.

25. Symmetric aggregation can produce permutation-invariant global outputs.

26. Relative displacement and Euclidean distance are translation invariant.

27. Euclidean distance is rotation invariant.

28. Geometry transformation alone does not define ternary polarity transformation.

29. Energy constructed from an invariant representation remains invariant.

30. Energy, force, ternary state, and resonance classification remain separately typed.

31. Numerical tolerance cannot redefine exact ternary membership.

32. Three-level quantization does not imply balanced ternary semantics.

33. Snapshot state does not imply restart completeness.

34. Exact replay requires complete result-affecting state.

35. Request, authorization, and commit remain separate stages.

36. Cross-scale mappings compose only through typed intermediate scales.

37. Information lost during coarse graining is not restored by later mappings alone.

38. Validation state remains separate from ternary state.

39. Serialization must distinguish active neutral from missingness.

40. Forward EIF-to-TR composition produces a ternary target rather than executed state.

41. Executed ternary state changes only through an explicit execution mapping.

42. TR and EIF remain distinct spaces despite explicit coupling.

43. TR-to-EIF feedback produces a request before committed EIF state.

44. Integrated execution cannot bypass ternary invariants.

45. Whole-chain equivariance requires compatible equivariance throughout the relevant composition.

46. Numerical representation does not redefine formal mathematical codomain.

47. FRP executable specialization does not become identical to TR-EIF.

48. Implementation parameter reuse does not establish universality.

49. Phase-derived ternary targets remain upstream of execution.

50. Retained-frequency dynamics are memory state when they affect future evolution.

51. Retained-frequency memory is distinct from explicit pairwise delay.

52. Global phase-order magnitude is a reduced global observable.

53. Phase-order magnitude does not reconstruct complete phase state.

54. Resonance projection and classification may be information-reducing mappings.

55. Ternary targets generally reduce upstream continuous state information.

56. Executed neutral alone does not determine complete pending-route state.

57. Exact restart of staged routing requires preservation of result-affecting pending state.

58. Local mappings require complete local domains.

59. Scale-dependent mappings require explicit scale identity.

60. History-dependent resonance requires explicit history state.

61. Ternary transition does not determine structural transition without an explicit mapping.

62. Structural transition does not determine physical phase transition without an explicit physical classification mapping.

63. Typed integration preserves semantic boundaries among intermediate spaces.

64. Framework-wide ternary invariants survive every conforming specialization.

65. Scheduler constraints cannot create forbidden shorter opposite-polarity paths.

66. Retention events do not change ternary polarity.

67. Opposite-polarity routing remains a two-leg polarity-changing process even with arbitrary neutral retention.

68. Transformation behavior of resonance state and ternary target depends on the complete declared mapping chain.

69. The canonical TR-EIF integration chain is not an identity chain.

---

## 104. Dependency on the Axiomatic System

Every lemma in this chapter depends only on previously defined objects and assumptions.

No lemma changes:

`T = {-1, 0, 1}`.

No lemma changes the canonical notation:

`-1/0/1`.

No lemma turns:

`0`

into passive state.

No lemma identifies:

`K_R`

with:

`T`.

No lemma identifies:

`R(t)`

with:

`C(t)`.

No lemma identifies:

`delay`

with:

`phase lag`.

No lemma identifies:

`ternary transition`

with:

`bifurcation`.

No lemma identifies:

`ternary state`

with:

`energy`

or:

`force`.

---

## 105. Preparation for Fundamental Theorems

The results established here provide the principal intermediate statements required by Chapter 10.

The theorem layer can therefore build on:

- exact ternary-domain closure;
- neutral mediation;
- graph separation of opposite polarities;
- minimum transition-path length;
- staged-routing consistency;
- mapping-composition closure;
- information-loss properties;
- equivariant composition;
- invariant readout;
- explicit history closure;
- dimensional compatibility;
- integrated TR-EIF type preservation.

Theorems in Chapter 10 must state explicitly which lemmas, axioms, and invariants they use.

---

## 106. Final Statement

The fundamental lemmas establish that the core TR-EIF architecture is mathematically constrained by its typed spaces and explicit mappings.

The balanced ternary kernel remains:

`-1/0/1`

with:

`T = {-1, 0, 1}`.

The active neutral state:

`0`

is structurally necessary for every admissible committed path between opposite polarities.

The canonical paths remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Target, pending destination, and executed state remain distinct.

The integration chain remains:

`interatomic state`

`→ equivariant representation`

`→ resonance state`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated execution`

`→ interatomic feedback`.

The lemmas also preserve the foundational distinctions:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`

`resonance classification ≠ energy`

`delay ≠ phase lag`

`target ≠ executed state`

`mathematical model ≠ numerical realization`.

These derived results form the immediate mathematical foundation for the fundamental theorems of TR-EIF.
