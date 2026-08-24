# Fundamental Theorems

## 1. Purpose

This chapter establishes the fundamental theorems of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The theorem layer builds on the definitions, axioms, state spaces, operators, mathematical structures, mappings, framework invariants, and fundamental lemmas established in Chapters 01–09.

The principal theorem families concern:

- typed composition;
- balanced ternary transition topology;
- active-neutral mediation;
- staged opposite-polarity execution;
- continuous-to-ternary separation;
- resonance-state classification;
- information preservation and reduction;
- equivariant composition;
- invariant observables;
- deterministic state closure;
- multiscale composition;
- integrated EIF-to-TR and TR-to-EIF coupling;
- preservation of framework invariants under specialization.

Theorems are stated only within their declared assumptions.

No theorem extends beyond those assumptions.

---

## 2. Theorem Convention

Each theorem contains:

1. assumptions;
2. statement;
3. proof;
4. consequences;
5. scope.

Unless explicitly stated otherwise, theorem provenance is:

`DERIVED`

The theorem layer does not redefine the axiomatic system.

---

## 3. Theorem 1 — Typed Chain Composition

### Assumptions

Let:

`X_0, X_1, ..., X_n`

be state spaces.

For every:

`k ∈ {1, ..., n}`

let:

`F_k: X_(k-1) → X_k`.

### Statement

The ordered composition:

`F_n ∘ F_(n-1) ∘ ... ∘ F_1`

is a well-defined mapping:

`X_0 → X_n`.

### Proof

By typed composition closure, the codomain of:

`F_1`

is exactly the domain of:

`F_2`.

Therefore:

`F_2 ∘ F_1: X_0 → X_2`.

Applying the same argument recursively gives:

`F_3 ∘ F_2 ∘ F_1: X_0 → X_3`.

Continuing through:

`F_n`

produces:

`F_n ∘ ... ∘ F_1: X_0 → X_n`.

### Consequences

A TR-EIF computational chain is mathematically valid only when adjacent mapping types are compatible or are connected through explicit intermediate transformations.

### Scope

The theorem establishes type-valid composition.

It does not establish injectivity, surjectivity, equivariance, conservation, or numerical stability.

---

## 4. Theorem 2 — Balanced Ternary State Closure

### Assumptions

Let:

`T = {-1, 0, 1}`.

Let every committed ternary update satisfy:

`F_T: T × X_ctrl → T`.

### Statement

If:

`t_exec[0] ∈ T`

then every finite committed execution sequence satisfies:

`t_exec[k] ∈ T`

for all:

`k ≥ 0`.

### Proof

The initial state belongs to:

`T`.

Assume:

`t_exec[k] ∈ T`.

Because the committed update has codomain:

`T`,

the next state satisfies:

`t_exec[k+1] ∈ T`.

By induction:

`t_exec[k] ∈ T`

for every finite execution coordinate.

### Consequences

No conforming committed update can produce a fourth ternary state.

The executed state remains exactly within:

`-1/0/1`.

### Scope

This theorem applies to committed ternary execution state.

It does not constrain auxiliary continuous variables.

---

## 5. Theorem 3 — Active-Neutral Mediation Theorem

### Assumptions

Let:

`T = {-1, 0, 1}`.

Let direct opposite committed transitions be forbidden:

`-1 ↛ 1`

`1 ↛ -1`.

Let the canonical polarity-changing edges include:

`-1 → 0`

`0 → 1`

`1 → 0`

`0 → -1`.

### Statement

Every admissible committed path between opposite ternary polarities contains active neutral:

`0`.

### Proof

Consider a path from:

`-1`

to:

`1`.

A direct edge is forbidden.

Since the state space contains only:

`-1`

`0`

`1`,

the only possible intermediate state distinct from both endpoints is:

`0`.

Therefore every admissible path from:

`-1`

to:

`1`

contains:

`0`.

The same argument applies to the reverse direction.

### Consequences

The canonical opposite-polarity routes are:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Active neutral is structurally necessary rather than optional for opposite-polarity committed execution.

### Scope

Retention at:

`0`

may occur for any admissible duration.

---

## 6. Theorem 4 — Minimum Opposite-Polarity Transition Length

### Assumptions

Use the assumptions of Theorem 3.

Count only committed state-changing edges.

### Statement

Every committed route between opposite polarities contains at least two state-changing legs.

### Proof

A one-leg route would require:

`-1 → 1`

or:

`1 → -1`.

Both are forbidden.

By the Active-Neutral Mediation Theorem, the route must pass through:

`0`.

Therefore at least two state-changing edges are required.

### Consequences

The shortest routes are exactly:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

### Scope

Neutral retention can increase execution duration but does not increase the number of polarity-changing legs required by the canonical shortest route.

---

## 7. Theorem 5 — Opposite-Polarity Separation

### Assumptions

Represent the committed ternary transition relation as a directed graph with vertices:

`{-1, 0, 1}`.

Direct opposite edges are absent.

### Statement

The active-neutral vertex:

`0`

separates:

`-1`

from:

`1`

with respect to admissible opposite-polarity paths.

### Proof

Remove vertex:

`0`.

The remaining graph contains only:

`-1`

and:

`1`.

Because no direct opposite edge exists, no directed path connects the two remaining vertices.

Therefore:

`0`

is a separating vertex for opposite-polarity reachability.

### Consequences

Neutral mediation is encoded directly in the topology of the transition graph.

### Scope

This theorem concerns the canonical three-state transition topology.

---

## 8. Theorem 6 — Staged Opposite-Polarity Execution

### Assumptions

Let complete ternary execution state contain:

`t_exec`

`t_target`

`t_pending`.

Suppose:

`t_exec = -1`

and:

`t_target = 1`.

Assume eventual target completion through admissible committed transitions.

### Statement

The execution necessarily contains at least two distinct committed state-changing events:

`-1 → 0`

followed later by:

`0 → 1`.

### Proof

By Theorem 3, every admissible route must contain:

`0`.

By Theorem 4, the route requires at least two state-changing legs.

The first state-changing event must therefore be:

`-1 → 0`.

The final state-changing event reaching the requested opposite polarity must be:

`0 → 1`.

The two events cannot be the same committed transition because they have different pre-states and post-states.

### Consequences

First-leg completion and second-leg completion are distinct execution events.

A pending destination can persist while:

`t_exec = 0`.

### Scope

The reverse route:

`1 → 0 → -1`

follows symmetrically.

---

## 9. Theorem 7 — Neutral Residence Preservation

### Assumptions

Suppose the first leg of an opposite-polarity route has completed.

Let:

`t_exec = 0`.

Let a valid:

`t_pending ∈ {-1, 1}`

remain preserved.

Assume:

`0 → 0`

is an admissible retention event.

### Statement

Any finite sequence of neutral-retention events preserves the structural possibility of later second-leg completion.

### Proof

Every retention event maps:

`0`

to:

`0`.

Therefore after any finite number of retention events:

`t_exec = 0`.

The pending destination remains preserved by assumption.

Thus the execution state remains at the required intermediate vertex with the intended destination retained.

A later authorized transition:

`0 → t_pending`

remains structurally admissible.

### Consequences

Neutral mediation does not require immediate second-leg execution.

Active neutral may have nonzero residence duration.

### Scope

The theorem does not guarantee that authorization for the second leg will occur.

---

## 10. Theorem 8 — Target-Execution Separation

### Assumptions

Let:

`T_target = {-1, 0, 1}`

and:

`T_exec = {-1, 0, 1}`.

Treat them as distinct semantic spaces.

Let:

`P_target: X_upstream → T_target`.

Let:

`E_T: X_Texec × X_ctrl → X_Texec`

be the execution mapping.

### Statement

Evaluation of:

`P_target`

does not itself constitute mutation of:

`t_exec`.

### Proof

The codomain of:

`P_target`

is:

`T_target`.

Executed state belongs to:

`T_exec`

within:

`X_Texec`.

The spaces have equal value sets but distinct semantic roles.

No identity mapping from target generation to committed execution has been assumed.

Committed execution occurs through:

`E_T`.

Therefore target evaluation alone does not mutate executed state.

### Consequences

A target can differ from executed state without contradiction.

Upstream continuous dynamics cannot bypass execution semantics merely by producing a target value.

### Scope

This theorem applies to every TR-EIF specialization preserving the target/execution boundary.

---

## 11. Theorem 9 — Pending-State Necessity for Exact Staged Restart

### Assumptions

Let complete execution state contain:

`(t_exec, t_target, t_pending)`.

Suppose two valid states exist:

`x_a = (0, 1, 1)`

and:

`x_b = (0, -1, -1)`.

Suppose future execution may complete the pending route.

### Statement

A restart representation containing only:

`t_exec`

cannot guarantee exact continuation of staged ternary execution.

### Proof

Both complete states project to:

`t_exec = 0`.

Therefore a representation storing only executed state maps:

`x_a`

and:

`x_b`

to the same restart representation.

Their pending destinations differ.

If the pending routes later complete, one continuation can execute:

`0 → 1`

while the other can execute:

`0 → -1`.

Thus the same incomplete restart representation corresponds to distinct valid future trajectories.

Exact continuation is therefore not guaranteed.

### Consequences

Result-affecting pending-route state belongs to restart-complete execution state.

### Scope

This theorem applies when pending routing is active and affects future execution.

---

## 12. Theorem 10 — Resonance-Ternary Non-Identity

### Assumptions

Let resonance classification space be:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

Let balanced ternary state be:

`T = {-1, 0, 1}`.

No explicit semantic identification is defined.

### Statement

The equality of cardinality:

`|K_R| = |T| = 3`

does not establish:

`K_R = T`.

### Proof

Two sets may have equal cardinality while containing semantically distinct elements.

The resonance classes describe relation to a resonance window.

The ternary states describe balanced ternary state and execution semantics.

No elementwise identity follows from cardinality.

Therefore the spaces remain distinct.

### Consequences

A resonance-to-ternary transformation requires an explicit mapping.

In particular, no automatic identities follow between:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

and:

`-1`

`0`

`1`.

### Scope

A specific model may define such a mapping explicitly.

---

## 13. Theorem 11 — Continuous-to-Ternary Mapping Separation

### Assumptions

Let:

`X_C`

be a continuous state space.

Let:

`P_CT: X_C → T_target`.

Let committed execution occur in:

`T_exec`

through a separate execution mapping.

### Statement

The continuous-to-ternary mapping produces a ternary target but does not eliminate the execution boundary.

### Proof

The codomain of:

`P_CT`

is:

`T_target`.

The committed state belongs to:

`T_exec`.

By the Target-Execution Separation Theorem, target generation is not committed execution.

Therefore continuous-state classification or projection cannot directly replace the execution mapping.

### Consequences

Threshold crossing, resonance classification, phase-derived classification, and other continuous-to-discrete mappings remain upstream of committed ternary execution.

### Scope

This theorem does not prescribe a particular continuous-to-ternary mapping.

---

## 14. Theorem 12 — Resonance-Window Classification Separation

### Assumptions

Let:

`r ∈ X_R`.

Let:

`W_R ⊂ X_R`.

Let:

`C_R: X_R → K_R`

classify resonance coordinates relative to the resonance window.

### Statement

The output of:

`C_R`

is a resonance classification and not, by itself:

- a ternary executed state;
- a bifurcation;
- a structural transition;
- a physical phase transition;
- an energy value.

### Proof

The codomain of:

`C_R`

is:

`K_R`.

Each listed object belongs to a different semantic space or mathematical structure.

No mappings from:

`K_R`

to those objects are assumed.

Therefore the resonance class cannot be identified with any of them solely by classification.

### Consequences

Each downstream interpretation requires an explicit mapping and its own assumptions.

### Scope

This theorem preserves semantic separation without prohibiting explicitly defined model couplings.

---

## 15. Theorem 13 — Resonance-Window Crossing Is Insufficient for Bifurcation

### Assumptions

Let a trajectory:

`r(t)`

cross:

`∂W_R`.

No additional bifurcation structure is assumed.

### Statement

The crossing alone does not establish a bifurcation.

### Proof

A resonance-window crossing establishes a change in classification relative to:

`W_R`.

A bifurcation requires a qualitative structural change in a parameterized dynamical system under specified critical conditions.

Window crossing alone supplies neither the required parameterized-family statement nor the required structural-change condition.

Therefore the crossing is insufficient to establish bifurcation.

### Consequences

The terms:

`window crossing`

and:

`bifurcation`

remain mathematically distinct.

### Scope

A model may separately prove that a particular window boundary coincides with a bifurcation boundary.

---

## 16. Theorem 14 — Phase-Lag and Delay Separation

### Assumptions

Consider a coupling term:

`sin(theta_j(t) - theta_i(t) - gamma)`.

No delayed phase argument is present.

### Statement

A nonzero:

`gamma`

does not introduce explicit temporal delay.

### Proof

The term depends on current-time phases:

`theta_j(t)`

and:

`theta_i(t)`.

The parameter:

`gamma`

shifts phase difference.

No quantity of the form:

`theta_j(t - tau)`

with:

`tau > 0`

appears.

Therefore the term contains phase lag but not explicit temporal delay.

### Consequences

`phase lag ≠ delay`.

A delayed coupling model requires separately defined history dependence.

### Scope

This theorem applies to the stated instantaneous coupling form.

---

## 17. Theorem 15 — Finite-Memory State Closure

### Assumptions

Let discrete dynamics satisfy:

`x[k+1] = F(x[k], x[k-1], ..., x[k-m])`

for finite:

`m`.

Define:

`z[k] = (x[k], x[k-1], ..., x[k-m])`.

### Statement

There exists a first-order update:

`G`

such that:

`z[k+1] = G(z[k])`.

### Proof

Define the first component of:

`G(z[k])`

as:

`F(x[k], ..., x[k-m])`.

Define the remaining components by shift:

`x[k]`

`x[k-1]`

through:

`x[k-m+1]`.

Every component of:

`z[k+1]`

is then determined by:

`z[k]`.

Therefore the finite-memory process is first-order on the extended state space.

### Consequences

Finite result-affecting memory can be incorporated into explicit complete state.

### Scope

Continuous delay equations may require function-valued history state.

---

## 18. Theorem 16 — Deterministic Restart Completeness

### Assumptions

Let a deterministic evolution be:

`x[k+1] = F(x[k], u[k], p)`.

Let restart representation:

`C(x[k])`

be injective over all result-affecting state components required by future evolution.

Assume identical future inputs:

`u[k:]`

and identical immutable parameters:

`p`.

### Statement

The complete restart representation determines the same future trajectory as uninterrupted execution.

### Proof

Injectivity of:

`C`

allows the required result-affecting state:

`x[k]`

to be recovered uniquely.

With identical:

`x[k]`

identical future inputs, identical parameters, and deterministic:

`F`,

the next state is identical.

Applying the same argument recursively yields identical subsequent states.

Therefore the restarted trajectory equals the uninterrupted trajectory.

### Consequences

Exact deterministic replay requires complete result-affecting state, not merely a convenient snapshot.

### Scope

This theorem assumes deterministic execution and exact preservation of all required state and inputs.

---

## 19. Theorem 17 — Non-Injective Restart Representation Cannot Guarantee Exact Replay

### Assumptions

Let:

`C: X_complete → X_checkpoint`

be non-injective.

Assume at least one omitted distinction can affect future evolution.

### Statement

Exact replay cannot be guaranteed from:

`C(x)`

alone.

### Proof

Since:

`C`

is non-injective, there exist:

`x_a ≠ x_b`

with:

`C(x_a) = C(x_b)`.

By assumption, the distinction between these complete states can affect future evolution.

Therefore the same checkpoint representation can correspond to different future trajectories.

Exact replay is not guaranteed.

### Consequences

Checkpoint completeness is a state-closure property rather than merely a serialization property.

### Scope

If all collapsed distinctions are provably future-irrelevant, a reduced restart state may still be sufficient.

---

## 20. Theorem 18 — Information-Loss Propagation

### Assumptions

Let:

`F: X → Y`

be non-injective.

Let:

`G: Y → Z`

be any mapping.

### Statement

The composite:

`G ∘ F`

is non-injective.

### Proof

Since:

`F`

is non-injective, there exist:

`x_a ≠ x_b`

such that:

`F(x_a) = F(x_b)`.

Applying:

`G`

gives:

`G(F(x_a)) = G(F(x_b))`.

Therefore distinct source states have the same composite output.

Hence:

`G ∘ F`

is non-injective.

### Consequences

Information lost by a mapping stage cannot be reconstructed by later mappings from that stage's output alone.

### Scope

External side information can alter reconstructibility but is outside the stated composition.

---

## 21. Theorem 19 — Injective Chain Preservation

### Assumptions

Let:

`F_k: X_(k-1) → X_k`

be injective for every:

`k ∈ {1, ..., n}`.

### Statement

The composition:

`F_n ∘ ... ∘ F_1`

is injective.

### Proof

Composition of two injective mappings is injective.

Applying this result recursively across the finite chain preserves injectivity at every composition step.

Therefore the full composition is injective.

### Consequences

A fully injective mapping chain preserves distinguishability of source states.

### Scope

This theorem does not imply surjectivity.

---

## 22. Theorem 20 — Ternary Reduction Theorem

### Assumptions

Let:

`X`

contain more than three distinguishable states.

Let:

`P_T: X → T`

where:

`T = {-1, 0, 1}`.

### Statement

`P_T`

cannot be injective over all of:

`X`.

### Proof

The codomain contains exactly three elements.

An injective mapping into a three-element set can have at most three distinct domain elements.

Since:

`X`

contains more than three distinguishable states, at least two distinct source states must map to the same ternary value.

Therefore:

`P_T`

is non-injective.

### Consequences

A ternary target is generally a reduced representation of richer upstream state.

### Scope

The theorem concerns direct mapping into exactly three target states.

---

## 23. Theorem 21 — Equivariant Chain Composition

### Assumptions

Let group:

`G_sym`

act on:

`X_0, X_1, ..., X_n`

through compatible representations:

`rho_0, rho_1, ..., rho_n`.

Let each:

`F_k: X_(k-1) → X_k`

satisfy:

`F_k(rho_(k-1)(g)x) = rho_k(g)F_k(x)`.

### Statement

The full composition:

`F_n ∘ ... ∘ F_1`

is equivariant:

`F_chain(rho_0(g)x) = rho_n(g)F_chain(x)`.

### Proof

Apply equivariance of:

`F_1`

to move the group action from:

`X_0`

to:

`X_1`.

Then apply equivariance of:

`F_2`

to move it to:

`X_2`.

Continue recursively through:

`F_n`.

The resulting expression is:

`rho_n(g)F_chain(x)`.

Therefore the full composition is equivariant.

### Consequences

Equivariance can be preserved through an entire compatible processing chain.

### Scope

All intermediate group actions must be compatible.

---

## 24. Theorem 22 — Invariant Readout from Equivariant Representation

### Assumptions

Let:

`F_EQ: X → Y`

be equivariant.

Let:

`F_INV: Y → Z`

be invariant under the action on:

`Y`.

### Statement

The composite:

`F_INV ∘ F_EQ`

is invariant.

### Proof

For:

`g ∈ G_sym`:

`F_INV(F_EQ(rho_X(g)x))`

equals:

`F_INV(rho_Y(g)F_EQ(x))`

by equivariance.

By invariance of:

`F_INV`,

this equals:

`F_INV(F_EQ(x))`.

Therefore the composite is invariant.

### Consequences

Invariant scalar observables may be constructed from equivariant intermediate representations.

### Scope

The readout must be invariant under the relevant intermediate representation.

---

## 25. Theorem 23 — Permutation-Invariant Extensive Aggregation

### Assumptions

Let local scalar contributions:

`e_i`

transform only by reindexing under:

`pi ∈ S_N`.

Define:

`E = sum_(i=1)^N e_i`.

### Statement

`E`

is invariant under permutation of entity labels.

### Proof

A permutation reorders the finite set of terms without changing their values.

Finite scalar addition is independent of ordering.

Therefore:

`E' = E`.

### Consequences

An extensive scalar constructed by summing permutation-equivariant local scalar contributions is permutation invariant.

### Scope

The theorem requires consistent permutation of entity-associated data.

---

## 26. Theorem 24 — Euclidean Relative-Geometry Invariance

### Assumptions

Let atomic positions be:

`r_i ∈ R^3`.

Let relative vectors be:

`r_ij = r_j - r_i`.

Let global translation be:

`r_i' = r_i + a`.

Let global rotation be:

`r_i'' = Qr_i`

with:

`Q ∈ SO(3)`.

### Statement

Relative distances:

`d_ij = ||r_ij||`

are invariant under global translations and rotations.

### Proof

Under translation:

`r_ij' = (r_j + a) - (r_i + a) = r_ij`.

Therefore:

`d_ij' = d_ij`.

Under rotation:

`r_ij'' = Qr_ij`.

Since:

`Q^T Q = I`,

the Euclidean norm is preserved:

`||Qr_ij|| = ||r_ij||`.

Therefore:

`d_ij'' = d_ij`.

### Consequences

Distance-based scalar geometric descriptors can be translation and rotation invariant.

### Scope

Periodic systems require a separately defined consistent periodic displacement mapping.

---

## 27. Theorem 25 — Invariant Energy Construction

### Assumptions

Let:

`P_INV: X_EIF → X_INV`

be invariant under the selected symmetry group.

Let:

`E_model: X_INV → R`.

Define:

`E_total = E_model ∘ P_INV`.

### Statement

`E_total`

is invariant under the selected symmetry group.

### Proof

For:

`g ∈ G_sym`:

`E_total(rho(g)x)`

`= E_model(P_INV(rho(g)x))`.

By invariance of:

`P_INV`:

`P_INV(rho(g)x) = P_INV(x)`.

Therefore:

`E_total(rho(g)x) = E_model(P_INV(x))`

`= E_total(x)`.

### Consequences

A scalar energy model can inherit symmetry invariance from its representation layer.

### Scope

No non-invariant auxiliary dependence may enter the energy mapping.

---

## 28. Theorem 26 — Semantic Type Preservation

### Assumptions

Consider distinct spaces:

`X_phase`

`X_R`

`K_R`

`T_target`

`T_exec`

`X_E`

`X_F`.

Let mappings connect some of these spaces.

### Statement

Composition between these spaces does not make their elements semantically identical.

### Proof

A mapping establishes a relation from one typed space to another.

It does not identify the domain with the codomain unless an explicit identity or isomorphism with semantic equivalence is established.

The listed spaces represent different objects:

- phase state;
- resonance coordinates;
- resonance class;
- ternary target;
- executed ternary state;
- energy;
- force.

Therefore they remain semantically distinct throughout composition.

### Consequences

The following distinctions remain mandatory:

`phase relation ≠ chemical bond`

`ternary state ≠ energy`

`phase coupling ≠ mechanical force`

`target ≠ executed state`

`resonance classification ≠ energy`.

### Scope

Explicit model-defined mappings may couple these quantities without identifying their types.

---

## 29. Theorem 27 — Exact Ternary Membership

### Assumptions

Let:

`T = {-1, 0, 1}`.

Let:

`x ∈ R`.

### Statement

`x ∈ T`

if and only if:

`x = -1`

or:

`x = 0`

or:

`x = 1`.

### Proof

This follows directly from exact set membership in:

`T`.

Approximate proximity to any element does not alter membership.

### Consequences

Tolerance tests and numerical neighborhoods cannot redefine the formal ternary domain.

### Scope

A quantization mapping may map non-ternary numerical values into:

`T_target`.

---

## 30. Theorem 28 — Active-Neutral and Missingness Separation

### Assumptions

Let:

`T_optional = {-1, 0, 1, NONE}`.

Assume all four values are distinct.

### Statement

No semantics-preserving representation may identify:

`0`

with:

`NONE`.

### Proof

`0`

is an element of the balanced ternary state space.

`NONE`

is explicitly outside:

`T`.

A semantics-preserving representation must distinguish distinct semantic states.

Therefore the two values cannot share one semantic representation.

### Consequences

Active neutral cannot be represented as missing, absent, null, unresolved, or uninitialized state.

### Scope

Serialized encodings may use arbitrary symbols provided decoding remains injective over these states.

---

## 31. Theorem 29 — Request-Authorization-Commit Separation

### Assumptions

Let:

`F_req: X → X_req`.

Let:

`F_auth: X_req × X_state → X_auth`.

Let:

`F_commit: X_state × X_auth → X_state`.

### Statement

The three stages:

`request`

`authorization`

`commit`

are mathematically distinct operations.

### Proof

Each stage has a distinct mapping signature and codomain.

A request belongs to:

`X_req`.

Authorization belongs to:

`X_auth`.

Committed state belongs to:

`X_state`.

Therefore no stage is identical to another by type.

### Consequences

A request does not imply authorization.

Authorization does not imply that commit has already occurred.

### Scope

A computational implementation may execute the stages within one external cycle while preserving their semantic separation.

---

## 32. Theorem 30 — Rejected-Proposal State Preservation

### Assumptions

Let:

`x_acc`

be accepted state.

Let:

`x_prop`

be proposed state.

Assume rejection applies rollback:

`Rollback(x_acc, x_prop) = x_acc`.

### Statement

A rejected proposal cannot alter retained accepted state.

### Proof

By rollback definition, the post-rejection state equals:

`x_acc`.

Therefore the retained state is unchanged.

### Consequences

Proposal evaluation can remain separate from committed state mutation.

### Scope

The theorem requires explicit rollback semantics.

---

## 33. Theorem 31 — Multiscale Typed Composition

### Assumptions

Let scales be:

`ell_0, ell_1, ..., ell_n`.

Let:

`M_k: X^(ell_(k-1)) → X^(ell_k)`.

### Statement

The complete multiscale chain:

`M_n ∘ ... ∘ M_1`

is a typed mapping:

`X^(ell_0) → X^(ell_n)`.

### Proof

The codomain of each mapping is the domain of the next.

The result follows from the Typed Chain Composition Theorem.

### Consequences

Cross-scale transfer requires explicit intermediate scale spaces.

### Scope

The theorem does not establish thermodynamic consistency, conservation, or information preservation.

---

## 34. Theorem 32 — Coarse-Graining Irreversibility under Non-Injective Mapping

### Assumptions

Let:

`M_FC: X_fine → X_coarse`

be non-injective.

No external side information is retained.

### Statement

No mapping from:

`X_coarse`

alone can uniquely reconstruct every state in:

`X_fine`.

### Proof

Because:

`M_FC`

is non-injective, there exist:

`x_a ≠ x_b`

such that:

`M_FC(x_a) = M_FC(x_b)`.

A reconstruction mapping receives the same coarse state for both fine states.

It cannot uniquely return both distinct originals.

Therefore universal unique reconstruction is impossible from coarse state alone.

### Consequences

Information discarded by coarse graining must be treated explicitly in multiscale closure.

### Scope

Statistical reconstruction or reconstruction using side information is not excluded.

---

## 35. Theorem 33 — Scale-Dependent State Closure

### Assumptions

Suppose mapping behavior depends on scale:

`ell`.

### Statement

A complete deterministic formulation must either include:

`ell`

in the result-affecting state or parameters, or define a scale-indexed mapping family:

`F^(ell)`.

### Proof

If identical apparent state values at two scales can produce different outputs, scale affects the result.

A deterministic mapping must include every result-affecting quantity in its domain or fixed parameterization.

Therefore scale identity must be explicit.

### Consequences

Scale cannot remain hidden when it changes resonance, coupling, coarse-graining, or closure behavior.

### Scope

Scale-independent mappings do not require an additional scale variable.

---

## 36. Theorem 34 — History-Dependent Resonance State Closure

### Assumptions

Let resonance window satisfy:

`W_R = F_WR(h)`.

Let:

`h ∈ X_H`

be history state.

### Statement

If history affects:

`W_R`,

then a complete resonance-classification state must contain:

`h`

or an equivalent sufficient memory representation.

### Proof

Suppose two histories:

`h_a`

and:

`h_b`

produce different windows.

For identical current resonance coordinate:

`r`,

classification may differ because membership is evaluated against different windows.

Therefore:

`r`

alone does not determine the classification.

The result-affecting history must be included explicitly or through an equivalent sufficient state.

### Consequences

Hysteretic resonance classification requires memory closure.

### Scope

The theorem applies only when resonance-window definition is history dependent.

---

## 37. Theorem 35 — Integrated Forward TR-EIF Mapping

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

`F_forward`

is a well-defined mapping:

`X_EIF → T_target`.

### Proof

The codomain of:

`P_EQ`

is:

`X_EQ`,

which is the domain of:

`P_ER`.

The codomain of:

`P_ER`

is:

`X_R`,

which is the domain of:

`P_RT`.

By typed chain composition:

`F_forward: X_EIF → T_target`.

### Consequences

The canonical forward chain is:

`interatomic state`

`→ equivariant representation`

`→ resonance state`

`→ ternary target`.

It terminates upstream of committed ternary execution.

### Scope

Additional intermediate spaces may be inserted if explicitly typed.

---

## 38. Theorem 36 — Integrated Ternary Execution Boundary

### Assumptions

Use the forward mapping of Theorem 35.

Let:

`E_T: X_Texec × X_ctrl → X_Texec`

govern committed ternary execution.

### Statement

The integrated forward mapping cannot directly replace:

`E_T`.

### Proof

The forward mapping has codomain:

`T_target`.

The execution mapping acts on:

`X_Texec`

and produces committed execution state.

By target-execution separation, target and executed state are distinct semantic objects.

Therefore the forward mapping cannot replace the execution mapping without violating the declared type boundary.

### Consequences

EIF-derived resonance information remains subject to:

- target registration;
- scheduler semantics;
- request handling;
- pending routing;
- active-neutral mediation;
- authorization;
- committed writeback;
- invariant enforcement.

### Scope

The exact implementation of these stages may vary while preserving their semantic contract.

---

## 39. Theorem 37 — Integrated Feedback Separation

### Assumptions

Let:

`F_TR→E: X_TR × X_EIF → X_EIF,req`.

Let committed EIF update occur through:

`F_Ecommit: X_EIF × X_EIF,req × X_auth → X_EIF`.

### Statement

TR-to-EIF feedback request does not itself constitute committed EIF-state mutation.

### Proof

The feedback mapping terminates in:

`X_EIF,req`.

Committed EIF state belongs to:

`X_EIF`.

The commit mapping is separately defined and requires authorization.

Therefore feedback generation and committed EIF mutation are distinct operations.

### Consequences

The integrated feedback chain can preserve explicit proposal and commit boundaries.

### Scope

The theorem does not prescribe the physical interpretation of the feedback request.

---

## 40. Theorem 38 — Integrated Ternary Invariant Preservation

### Assumptions

Let complete integrated state be:

`X_TR-EIF = X_EIF × X_TR × X_int`.

Assume every valid integrated committed update preserves the framework-wide ternary invariants.

### Statement

No valid integrated update can directly commit:

`-1 → 1`

or:

`1 → -1`

in executed ternary state.

### Proof

Direct opposite committed transitions are prohibited framework invariants.

A valid integrated update must preserve those invariants.

Therefore any update containing either direct opposite transition violates the admissible integrated transition relation.

Hence no valid integrated update can commit such a transition.

### Consequences

Learning, molecular dynamics, equivariant mappings, feedback, multiscale transfer, and reference-model specialization cannot bypass neutral mediation when affecting executed ternary state.

### Scope

This theorem concerns committed executed ternary state.

---

## 41. Theorem 39 — Specialization Invariant Preservation

### Assumptions

Let:

`S`

be a specialization of TR-EIF.

Assume specialization conformance requires preservation of a framework invariant set:

`I_core`.

### Statement

Every conforming execution of:

`S`

satisfies every invariant in:

`I_core`.

### Proof

Suppose a conforming execution violates some:

`I ∈ I_core`.

Then the execution fails the required invariant-preservation condition.

It is therefore not conforming.

By contradiction, every conforming execution preserves all:

`I ∈ I_core`.

### Consequences

A specialization may strengthen constraints but cannot silently weaken core invariants while remaining conforming.

### Scope

The theorem applies only to invariants declared framework-wide.

---

## 42. Theorem 40 — FRP Specialization Boundary

### Assumptions

Let FRP implement an executable specialization of selected TR mechanisms.

Let TR-EIF contain a broader formal architecture including EIF and additional layers.

### Statement

FRP conformance to selected TR-EIF mechanisms does not imply identity:

`FRP = TR-EIF`.

### Proof

Implementation of selected mappings establishes a realization relation.

Identity would require equality of complete state spaces, mapping families, semantics, and architectural scope.

TR-EIF contains formal and interatomic layers not identified with the FRP executable specialization.

Therefore realization does not imply identity.

### Consequences

FRP can provide executable reference behavior for selected TR mechanisms while TR-EIF remains the broader framework.

### Scope

The exact FRP implementation layer used as reference must be identified by the relevant artifact or release context.

---

## 43. Theorem 41 — Implementation Parameter Non-Universality

### Assumptions

Let:

`p_impl`

be defined by a particular executable specialization.

No framework axiom declares:

`p_impl`

universal.

### Statement

`p_impl`

is not a universal TR-EIF constant solely because it appears in the specialization.

### Proof

A universal constant must be established at framework level.

An implementation parameter belongs to the implementation parameterization unless formally promoted.

No such promotion is assumed.

Therefore:

`p_impl`

remains implementation-specific.

### Consequences

Executable reference parameters cannot be silently converted into universal physical or mathematical constants.

### Scope

A later formal definition may explicitly promote a parameter.

---

## 44. Theorem 42 — Phase-Derived Target Boundary

### Assumptions

Let:

`P_phase→T: X_phase → T_target`.

Let committed execution be governed by:

`E_T`.

### Statement

A phase-derived target cannot directly bypass neutral-mediated ternary execution.

### Proof

The phase mapping produces an element of:

`T_target`.

By the Target-Execution Separation Theorem, this is not committed executed state.

Any committed opposite-polarity route remains subject to the Active-Neutral Mediation Theorem.

Therefore a phase-derived opposite target still requires:

`-1 → 0 → 1`

or:

`1 → 0 → -1`

when executed.

### Consequences

Continuous phase dynamics remain upstream of ternary execution invariants.

### Scope

This theorem applies to any phase-based target mapping, including executable specializations.

---

## 45. Theorem 43 — Retained-Memory State Necessity

### Assumptions

Let retained variable:

`m[k]`

affect future evolution.

### Statement

Any deterministic complete state sufficient for exact continuation must preserve:

`m[k]`

or an equivalent sufficient representation.

### Proof

Suppose:

`m[k]`

is omitted.

Then two complete states may agree on every retained component while differing in:

`m[k]`.

Because:

`m[k]`

affects future evolution, their continuations may differ.

Therefore the reduced state is insufficient for exact deterministic continuation.

### Consequences

Retained-frequency memory, hysteresis variables, pending routes, scheduler state, and other result-affecting retained variables belong to complete state when present.

### Scope

Variables provably irrelevant to future evolution need not be retained.

---

## 46. Theorem 44 — Retained Frequency Does Not Establish Pairwise Delay

### Assumptions

Let:

`omega_ret`

be a retained frequency state affecting phase evolution.

Assume no phase term contains:

`theta_j(t - tau_ij)`.

### Statement

The model contains frequency memory but does not contain explicit pairwise phase delay solely by virtue of:

`omega_ret`.

### Proof

Frequency memory is encoded through a retained internal variable.

Pairwise delay requires past phase evaluation.

Since no delayed phase argument exists, the mathematical mechanisms are distinct.

### Consequences

`frequency memory ≠ pairwise temporal delay`.

### Scope

A different model may contain both mechanisms independently.

---

## 47. Theorem 45 — Global Phase-Order Reduction

### Assumptions

Let:

`Theta ∈ (S^1)^N`

with:

`N ≥ 2`.

Define:

`Z = (1/N) sum_j exp(i theta_j)`

and:

`R = |Z|`.

### Statement

The mapping:

`Theta → R`

is non-injective.

### Proof

Apply a common phase shift:

`theta_j' = theta_j + alpha`.

Then:

`Z' = exp(i alpha)Z`.

Therefore:

`|Z'| = |Z|`.

For nontrivial:

`alpha`

the coordinate phase configurations differ while producing the same:

`R`.

Thus the mapping is non-injective.

### Consequences

Global phase order does not uniquely determine the full phase configuration.

It also does not become identical to a separately defined coherence observable.

### Scope

The theorem concerns the magnitude of the global complex order parameter.

---

## 48. Theorem 46 — Coherence-Order Independence without Explicit Functional Relation

### Assumptions

Let:

`R = P_order(Theta)`.

Let:

`C = P_coh(x)`.

No function:

`F`

is defined such that:

`C = F(R)`.

### Statement

`R`

alone does not determine:

`C`.

### Proof

The two observables are independently defined.

No mathematical relation allowing reconstruction of:

`C`

from:

`R`

has been assumed.

Therefore determination of:

`C`

from:

`R`

does not follow.

### Consequences

`R(t) ≠ C(t)`

remains a formal distinction unless a particular model explicitly establishes a relation.

### Scope

Numerical coincidence at selected states does not establish identity.

---

## 49. Theorem 47 — Geometry-to-Ternary Non-Implication

### Assumptions

Let:

`rho_geo(g)`

act on interatomic geometry.

No direct group action on:

`T`

or geometry-to-ternary transition rule is defined.

### Statement

A geometric transformation does not, by itself, imply a ternary polarity change.

### Proof

The transformation acts on:

`X_EIF`.

The ternary state belongs to:

`T`.

No mapping from the geometric action directly to ternary-state mutation is specified.

Therefore no ternary transition follows solely from the geometric transformation.

### Consequences

Geometric symmetry and ternary execution remain separately defined layers.

### Scope

A model may couple them through explicit equivariant, resonance, and ternary mappings.

---

## 50. Theorem 48 — Structural Transition Separation

### Assumptions

Let:

`t_exec ∈ T`.

Let structural state be:

`s ∈ X_S`.

Let physical phase class be:

`k_phys ∈ K_phys`.

No direct identity mappings are assumed.

### Statement

The implication chain:

`ternary transition → structural transition → physical phase transition`

does not follow automatically.

### Proof

Each object belongs to a distinct semantic space.

A ternary transition affects:

`T`.

A structural transition affects:

`X_S`.

A physical phase transition changes classification in:

`K_phys`

under a separately defined physical criterion.

Without explicit mappings and conditions connecting these spaces, none of the implications follows solely from the preceding transition.

### Consequences

The distinctions remain:

`ternary transition ≠ structural transition`

and:

`structural transition ≠ physical phase transition`.

### Scope

A specific material model may establish conditional relations between these transitions.

---

## 51. Theorem 49 — Whole-Chain Equivariance Requirement

### Assumptions

Let an integrated observable be produced by composition:

`F = F_n ∘ ... ∘ F_1`.

Suppose the desired transformation property is equivariance or invariance under:

`G_sym`.

### Statement

A single equivariant submodule is insufficient to establish the desired transformation property of the complete chain.

### Proof

The complete transformation behavior depends on every mapping after the transformed input enters the chain.

If any subsequent mapping violates the required compatibility relation, the final output can violate equivariance or invariance even when an earlier mapping is equivariant.

Therefore the property must be established for the complete relevant composition.

### Consequences

Equivariance validation must test the whole declared mapping boundary rather than infer it from one component.

### Scope

A non-equivariant intermediate implementation can still produce an equivariant total mapping only if the total property is independently established.

---

## 52. Theorem 50 — Integrated Semantic Boundary Preservation

### Assumptions

Consider the canonical chain:

`X_EIF`

`→ X_EQ`

`→ X_R`

`→ K_R`

`→ T_target`

`→ X_Texec`

`→ X_EIF,req`

`→ X_EIF`.

### Statement

The integrated chain preserves distinct semantic boundaries between all declared intermediate spaces.

### Proof

Each arrow is a mapping between explicitly typed spaces.

Mapping composition connects outputs to inputs but does not identify distinct domain and codomain semantics.

Therefore:

- interatomic state remains interatomic state;
- equivariant representation remains an equivariant representation;
- resonance coordinates remain resonance coordinates;
- resonance class remains resonance class;
- ternary target remains a target;
- executed ternary state remains committed execution state;
- EIF feedback request remains a request;
- committed EIF state remains committed state.

### Consequences

Integration does not collapse the framework into one undifferentiated state variable.

### Scope

Implementations may optimize storage while preserving these formal semantic distinctions.

---

## 53. Theorem 51 — Canonical TR-EIF Forward-Execution-Feedback Architecture

### Assumptions

Let the following mappings be defined:

`P_EQ: X_EIF → X_EQ`

`P_ER: X_EQ → X_R`

`P_RC: X_R → K_R`

`P_KT: K_R × X_aux → T_target`

`E_T: X_Texec × T_target × X_ctrl → X_Texec`

`F_TR→E: X_TR × X_EIF → X_EIF,req`

`F_Ecommit: X_EIF × X_EIF,req × X_auth → X_EIF`.

### Statement

The canonical integrated architecture forms the typed cycle:

`interatomic state`

`→ equivariant representation`

`→ resonance state`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated ternary execution`

`→ interatomic feedback request`

`→ authorized interatomic commit`.

### Proof

Each mapping consumes an object from the preceding declared semantic space and produces an object in the next declared semantic space.

The ternary execution stage preserves the framework transition invariants by assumption.

The feedback stage produces a request rather than direct committed state.

The final commit stage updates the interatomic state only through its explicit authorization boundary.

Therefore the complete cycle is a typed composition with preserved semantic and execution boundaries.

### Consequences

The architecture integrates continuous, equivariant, resonant, ternary, and interatomic dynamics without identifying their state spaces.

### Scope

Specific TR-EIF model families may extend the cycle with additional state, observables, learning variables, molecular-dynamics variables, and multiscale state.

---

## 54. Theorem 52 — Core Invariant Persistence under Integrated Evolution

### Assumptions

Let:

`F_integrated: X_TR-EIF → X_TR-EIF`

be a committed integrated update.

Assume:

`F_integrated`

is conforming and preserves the core invariant set.

### Statement

If the initial integrated state satisfies the core invariants, every finite sequence of conforming integrated committed updates also satisfies them.

### Proof

The initial state satisfies the invariant set.

Assume the state at execution coordinate:

`k`

satisfies the invariants.

Because:

`F_integrated`

is conforming, its output also satisfies them.

By induction, every finite subsequent committed state satisfies the invariant set.

### Consequences

Core invariant preservation is stable under repeated conforming integrated evolution.

In particular:

- ternary state remains in `-1/0/1`;
- active neutral remains distinct;
- direct opposite committed transitions remain excluded;
- semantic target/execution separation remains intact.

### Scope

The theorem applies only to updates satisfying the declared conformance conditions.

---

## 55. Fundamental Theorem Set

The theorem layer establishes the following principal results.

1. Compatible typed mappings compose into valid mapping chains.

2. Executed balanced ternary state remains exactly within:

`-1/0/1`.

3. Active neutral is structurally necessary for every committed opposite-polarity route.

4. Opposite-polarity execution requires at least two state-changing legs.

5. Active neutral separates opposite polarities in the canonical transition graph.

6. Opposite-polarity execution is necessarily staged.

7. Neutral residence can persist between route legs.

8. Ternary target and executed ternary state remain distinct.

9. Exact staged restart requires result-affecting pending-route state.

10. Resonance classification and ternary state remain distinct spaces.

11. Continuous-to-ternary mapping remains upstream of execution.

12. Resonance-window classification does not become bifurcation, structural transition, physical phase transition, or energy.

13. Resonance-window crossing alone is insufficient to establish bifurcation.

14. Phase lag and explicit temporal delay are distinct mechanisms.

15. Finite memory can be represented by an extended first-order state.

16. Exact deterministic restart requires complete result-affecting state.

17. Non-injective restart state cannot guarantee exact replay when omitted distinctions affect future evolution.

18. Information loss at one mapping stage propagates through downstream composition.

19. Fully injective chains preserve source-state distinguishability.

20. Mapping a richer state space into exactly three ternary states is information reducing.

21. Compatible equivariant mappings compose equivariantly.

22. Invariant readout from equivariant representation produces invariant output.

23. Symmetric aggregation yields permutation-invariant extensive scalars.

24. Relative Euclidean geometry preserves translation and rotation invariance.

25. Energy constructed from invariant representation remains invariant.

26. Semantic types remain distinct under composition.

27. Balanced ternary membership is exact.

28. Active neutral and missingness cannot be identified.

29. Request, authorization, and commit are distinct operations.

30. Rejected proposals preserve retained state under rollback semantics.

31. Multiscale mappings compose through typed scale spaces.

32. Non-injective coarse graining cannot be universally inverted without side information.

33. Scale-dependent dynamics require explicit scale state or parameterization.

34. History-dependent resonance requires explicit history closure.

35. EIF state maps through equivariant and resonance layers into ternary target.

36. The forward mapping cannot replace ternary execution.

37. TR-to-EIF feedback remains separate from committed EIF mutation.

38. Integrated dynamics cannot bypass ternary invariants.

39. Conforming specializations preserve framework-wide invariants.

40. FRP remains an executable specialization/reference rather than an identity with TR-EIF.

41. Implementation parameters remain implementation-specific unless formally promoted.

42. Phase-derived targets remain subject to neutral-mediated execution.

43. Result-affecting retained memory belongs to complete deterministic state.

44. Retained-frequency memory does not imply pairwise temporal delay.

45. Global phase-order magnitude is an information-reducing observable.

46. Phase order does not determine separately defined coherence without an explicit relation.

47. Geometric transformation does not itself imply ternary polarity transformation.

48. Ternary, structural, and physical phase transitions remain distinct.

49. Equivariance and invariance must hold across the relevant complete mapping chain.

50. Integrated TR-EIF composition preserves semantic boundaries.

51. The canonical framework forms a typed forward-execution-feedback cycle.

52. Core invariants persist under repeated conforming integrated evolution.

---

## 56. Canonical Invariant Consequences

The fundamental theorems preserve the exact balanced ternary kernel:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`.

The active neutral state remains:

`0`.

The forbidden direct committed transitions remain:

`-1 ↛ 1`

`1 ↛ -1`.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each arrow remains a distinct committed transition event.

Neutral retention remains admissible when allowed by the execution relation.

A target does not equal an executed state by semantic identity.

A pending destination does not equal an executed state by semantic identity.

---

## 57. Canonical Semantic Consequences

The theorem layer preserves the distinctions:

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

`request ≠ authorization`

`authorization ≠ commit`

`mathematical model ≠ numerical realization`.

These distinctions are consequences of typed state spaces, explicit mappings, and execution boundaries.

---

## 58. Canonical Integrated Architecture

The theorem layer supports the canonical TR-EIF architecture:

`interatomic configuration`

`→ geometric and local-environment representation`

`→ equivariant representation`

`→ resonance coordinates`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated ternary execution`

`→ feedback request`

`→ authorization`

`→ interatomic state update`.

The architecture may be embedded in:

- learning systems;
- interatomic model families;
- molecular dynamics;
- multiscale materials models;
- reference material systems;
- executable specializations.

Every embedding remains subject to the relevant framework invariants and typed mapping contracts.

---

## 59. Relation to FRP

FRP provides an executable specialization/reference for selected ternary-resonant mechanisms.

The formal relationship is:

`TR-EIF formal mechanism`

`→ executable specialization/reference`

rather than:

`TR-EIF = FRP`.

FRP reference behavior preserves the balanced ternary kernel:

`-1/0/1`

and neutral-mediated opposite-polarity execution.

Implementation-specific scheduling, phase parameters, coupling coefficients, thresholds, fixed-point representations, register structures, benchmark formats, and execution artifacts remain implementation-layer objects unless independently defined at TR-EIF framework level.

---

## 60. Preparation for Corollaries

The fundamental theorems establish the results required for the corollary layer in Chapter 11.

The corollaries may derive direct consequences concerning:

- reachability;
- forbidden transitions;
- neutral-route persistence;
- checkpoint completeness;
- information reduction;
- symmetry-preserving observables;
- invariant energy construction;
- multiscale information loss;
- specialization conformance;
- integrated mapping behavior.

Every corollary must identify the theorem or theorem set from which it follows.

---

## 61. Final Statement

The fundamental theorem layer establishes the mathematical architecture connecting the principal TR-EIF state spaces without collapsing their meanings.

The balanced ternary kernel remains exactly:

`-1/0/1`.

Active neutral remains a genuine state and the mandatory mediator of committed opposite-polarity execution.

The continuous, resonant, ternary, equivariant, interatomic, and multiscale layers remain connected through explicit typed mappings.

The integrated architecture therefore preserves both composition and separation:

`interatomic`

`→ equivariant`

`→ resonant`

`→ ternary target`

`→ neutral-mediated execution`

`→ feedback`

`→ interatomic`.

These theorems form the formal basis for the corollaries developed in Chapter 11.
