# Mathematical Operators

## 1. Purpose

This document defines the mathematical operator architecture of the Ternary Resonant Equivariant Interatomic Framework.

The operator architecture specifies how TR-EIF mathematical objects may be:

- transformed;
- propagated;
- projected;
- embedded;
- coupled;
- delayed;
- aggregated;
- differentiated;
- integrated;
- discretized;
- updated;
- filtered;
- constrained;
- routed;
- compared;
- observed;
- inherited;
- validated.

An operator is admissible only when its mathematical role, domain, codomain, input dependencies, output semantics, and applicable constraints are explicit.

An operator must not change the semantic type of a state variable silently.

## 2. Status of This Document

The operators defined in this chapter are part of the TR-EIF formal framework.

This chapter does not prescribe one universal evolution equation.

It establishes the operator classes from which model-specific mathematical constructions may be assembled.

This document depends on:

- `chapter_01_foundations.md`;
- `chapter_02_notation_and_definitions.md`;
- `chapter_03_axiomatic_system.md`;
- `chapter_04_state_spaces.md`.

The definitions established in those chapters remain authoritative.

## 3. Operator Definition

A mathematical operator is a declared mapping:

`L: A → B`

where:

- `A` is the operator domain;
- `B` is the operator codomain;
- `L` is the transformation rule.

For every TR-EIF operator, the following must be declared:

1. operator name;
2. symbol;
3. domain;
4. codomain;
5. input type;
6. output type;
7. parameter dependence;
8. time dependence where applicable;
9. regularity assumptions where applicable;
10. state dependencies;
11. dimensional behavior;
12. invariant behavior;
13. failure conditions;
14. numerical realization where implemented.

An operator is incomplete when its action is described without its domain or codomain.

## 4. Operator Classes

TR-EIF distinguishes the following operator classes:

1. identity operators;
2. composition operators;
3. projection operators;
4. embedding operators;
5. restriction operators;
6. continuous evolution operators;
7. discrete update operators;
8. ternary transition operators;
9. continuous-to-ternary operators;
10. ternary-conditioned continuous operators;
11. coupling operators;
12. delay operators;
13. history operators;
14. dissipation operators;
15. saturation operators;
16. resonance-selection operators;
17. symmetry-action operators;
18. equivariant mappings;
19. topology operators;
20. neighborhood operators;
21. interatomic aggregation operators;
22. structural-transition operators;
23. inheritance operators;
24. observable operators;
25. numerical discretization operators;
26. validation operators.

A model may use a subset of these classes.

Unused operator classes must not influence the model implicitly.

## 5. Identity Operator

### 5.1 Definition

The identity operator on space `A` is:

`I_A: A → A`

with:

`I_A(a) = a`

for every admissible:

`a ∈ A`

### 5.2 Role

The identity operator represents preservation of a mathematical object without semantic modification.

It may be used for:

- retained state;
- inactive transformation branches;
- no-op execution paths;
- explicit persistence;
- operator composition;
- reference comparisons.

### 5.3 Ternary identity

For the balanced ternary set:

`T = {-1, 0, 1}`

the identity operator is:

`I_T: T → T`

with:

`I_T(σ) = σ`

The identity operation does not count as a ternary transition event when the state value remains unchanged unless the execution contract explicitly records retained-state events.

## 6. Operator Composition

### 6.1 Definition

Let:

`F: A → B`

and:

`G: B → C`

Then the composition is:

`G ∘ F: A → C`

defined by:

`(G ∘ F)(a) = G(F(a))`

### 6.2 Compatibility

Composition is permitted only when the codomain of the first operator is compatible with the domain of the second operator.

An invalid operator chain must not be repaired through an undocumented conversion.

### 6.3 Semantic composition

Type compatibility alone is insufficient.

The semantic meaning of the intermediate state must also remain valid.

For example:

`continuous state → ternary projection → ternary transition`

is semantically distinct from:

`continuous state → observable projection → ternary classification`

even if both intermediate representations can be encoded numerically.

### 6.4 Explicit ordering

For noncommuting operators:

`F ∘ G ≠ G ∘ F`

may hold.

TR-EIF must preserve the declared operator order.

Operator reordering is a semantic change unless equivalence is established.

## 7. Projection Operators

### 7.1 Definition

A projection operator maps a larger representation into a reduced representation:

`P: A → B`

where `B` contains less information than `A` or exposes only selected components.

### 7.2 State projection

A state projection may be written as:

`P_X: S → X`

where `S` is the composite state space and `X` is one component state space.

### 7.3 Observable projection

The observable operator is a projection:

`O: S → Y`

where `Y` is the observable output space.

### 7.4 Lossy projection

A projection may discard information.

A lossy projection must identify:

- retained information;
- discarded information;
- aggregation rule;
- reconstruction limitations.

### 7.5 Projection non-equivalence

In general:

`P(S₁) = P(S₂)`

does not imply:

`S₁ = S₂`

unless injectivity has been established over the declared domain.

## 8. Embedding Operators

### 8.1 Definition

An embedding maps an object from a lower-dimensional or reduced representation into a larger representation:

`E: A → B`

### 8.2 State embedding

A reduced state may be embedded into a larger state space:

`E_S: S_red → S`

### 8.3 Added components

Every component introduced by an embedding must have explicit provenance.

An embedding must not assign undocumented values to:

- hidden variables;
- history state;
- ternary state;
- topology;
- boundary variables;
- numerical state.

### 8.4 Projection–embedding relation

When appropriate:

`P(E(a)) = a`

may hold.

The reverse relation:

`E(P(b)) = b`

does not generally hold when `P` is lossy.

## 9. Restriction Operators

### 9.1 Definition

A restriction operator limits an operator or state to a declared subset.

If:

`F: A → B`

and:

`A₀ ⊆ A`

then:

`F|A₀`

denotes the action of `F` restricted to `A₀`.

### 9.2 Model-region restriction

A model may define a valid region:

`S_valid ⊆ S_adm`

and restrict an evolution operator to that region.

### 9.3 Scope

A restricted operator must not be evaluated outside its declared domain without an extension rule.

An out-of-domain input must remain visible as:

- unsupported;
- invalid;
- rejected;
- explicitly extrapolated.

## 10. Continuous Evolution Operators

### 10.1 Definition

A continuous evolution operator maps a state through continuous time.

A generic notation is:

`Φ_t: S → S`

where `Φ_t(S₀)` is the state obtained after elapsed time `t` under the declared evolution law.

### 10.2 Generality

The notation `Φ_t` does not imply that every TR-EIF model forms a reversible flow.

A model may instead define:

- a flow;
- a semiflow;
- a non-autonomous evolution family;
- a delayed evolution operator;
- a history-dependent evolution;
- a stochastic transition law.

The mathematical structure must be declared.

### 10.3 State dependence

Continuous evolution may depend on:

- current state;
- time;
- boundary state;
- parameter vector;
- history;
- topology;
- ternary state;
- external forcing.

### 10.4 Evolution admissibility

A continuous evolution operator must preserve the admissible state space or report explicitly when the trajectory exits it.

## 11. Differential Operators

### 11.1 Time derivative

For a differentiable state variable `x(t)`, its time derivative is:

`d x(t) / dt`

The derivative represents the local rate of change with respect to the declared time coordinate.

### 11.2 Vector-state derivative

For continuous state:

`X(t)`

the time derivative may be written as:

`dX/dt`

when all required differentiability conditions are satisfied.

### 11.3 Partial derivative

For a multivariable function:

`F(x₁, ..., x_n)`

a partial derivative with respect to variable `x_i` is written as:

`∂F/∂x_i`

### 11.4 Gradient

For a scalar field:

`U: ℝ^d → ℝ`

the gradient is:

`∇U`

where the coordinate system and metric structure must be declared.

### 11.5 Jacobian

For:

`F: ℝ^n → ℝ^m`

the Jacobian is denoted by:

`J_F`

and contains the declared first partial derivatives of the output components with respect to the input components.

### 11.6 Differentiability boundary

A differential operator must not be applied across a discrete ternary transition or topology discontinuity as though the state were continuously differentiable there.

Hybrid trajectories require separate treatment of:

- continuous segments;
- discrete events.

## 12. Integral Operators

### 12.1 Time integral

For an integrable scalar quantity `f(t)`:

`∫ f(t) dt`

represents accumulation over the declared time interval.

A definite accumulation between `t_a` and `t_b` is written as:

`∫[t_a,t_b] f(t) dt`

### 12.2 Accumulated quantities

Integration may be used to represent:

- accumulated energy transfer;
- accumulated dissipation;
- accumulated structural work;
- phase accumulation;
- integrated forcing;
- exposure over time.

### 12.3 Integration domain

Every integral must define:

- integration variable;
- integration interval or domain;
- integrand;
- units;
- boundary conditions where required.

### 12.4 Numerical integration

A numerical approximation to an integral must remain distinct from the exact mathematical integral.

Its discretization method and error properties must be declared by the numerical model.

## 13. Discrete Update Operators

### 13.1 Definition

A discrete update operator maps one execution state to the next:

`U: S_n → S_n+1`

### 13.2 Update contents

A discrete update may include:

- state evaluation;
- guard evaluation;
- ternary transition;
- topology update;
- history update;
- numerical-state update;
- validation update;
- trace emission.

### 13.3 Update order

The update contract must define whether dependent operations use:

- pre-update state;
- partially updated state;
- committed post-update state.

Silent in-place ordering changes are prohibited when they affect results.

### 13.4 Deterministic update

A deterministic update produces the same next state for the same complete input state and execution context.

## 14. Ternary Transition Operator

### 14.1 Definition

The local ternary transition operator is:

`U_T: T × C_T → T`

where:

- `T = {-1, 0, 1}`;
- `C_T` is the set of declared transition conditions.

### 14.2 Permitted outputs

For input state `-1`, direct output `1` is forbidden.

For input state `1`, direct output `-1` is forbidden.

### 14.3 Valid transition relation

The local admissible transitions are:

`-1 → -1`

`-1 → 0`

`0 → -1`

`0 → 0`

`0 → 1`

`1 → 0`

`1 → 1`

The direct transitions:

`-1 → 1`

`1 → -1`

are not elements of the admissible transition relation.

### 14.4 Opposite-state mediation

An opposite-state target requires two operator applications:

`U_T(-1, C₁) = 0`

followed by:

`U_T(0, C₂) = 1`

or:

`U_T(1, C₁) = 0`

followed by:

`U_T(0, C₂) = -1`

The conditions `C₁` and `C₂` need not be identical.

### 14.5 Active-neutral persistence

The operator may return:

`U_T(0, C) = 0`

when the active neutral state must persist.

## 15. Global Ternary Update Operator

### 15.1 Definition

For global ternary configuration:

`σ ∈ T^N`

the global update operator is:

`U_Σ: T^N × C_Σ → T^N`

### 15.2 Local consistency

Every local component of a global update must satisfy the local ternary transition relation.

A globally valid output cannot contain a locally forbidden direct opposite transition.

### 15.3 Coupled updates

A global update may include dependencies among components.

The model must define:

- coupling rule;
- priority;
- capacity;
- conflict resolution;
- update ordering;
- atomicity of commit.

### 15.4 Global guards

A local transition may be valid while the global transition is blocked by:

- capacity;
- topology;
- conservation;
- mutual exclusion;
- synchronization;
- structural invariant.

## 16. Continuous-to-Ternary Projection Operator

### 16.1 Definition

The continuous-to-ternary projection is:

`Π: X → T^N`

### 16.2 Required structure

The projection must define:

- selected continuous variables;
- decision regions;
- negative-state region;
- active-neutral region;
- positive-state region;
- boundary treatment;
- uncertainty treatment;
- timing;
- parameter provenance.

### 16.3 Active-neutral region

The state `0` must correspond to an operationally defined region or decision state.

It must not be used automatically for:

- missing values;
- failed measurements;
- unsupported states;
- invalid inputs.

### 16.4 Hysteretic projection

When state classification depends on transition history, the operator must include the required memory:

`Π_H: X × H × T^N → T^N`

### 16.5 Forbidden projection behavior

A continuous-to-ternary operator must not produce a hidden direct:

`-1 → 1`

or:

`1 → -1`

state event.

If the projected target changes polarity, the executed ternary state must pass through `0`.

## 17. Ternary-Conditioned Continuous Operator

### 17.1 Definition

A ternary-conditioned continuous operator is:

`Γ: X × T^N → X`

### 17.2 Role

The operator defines how the ternary state modifies continuous evolution.

Possible model-specific actions may include:

- damping;
- excitation;
- retention;
- routing;
- balancing;
- gain selection;
- boundary selection;
- mode selection.

### 17.3 Neutral-state action

The action associated with state `0` must be explicit.

It must not be treated as no operation unless that behavior is specifically defined for the model.

### 17.4 Bidirectional coupling

When continuous state affects ternary state and ternary state affects continuous state, the coupled operator chain is:

`X`

`→ Π`

`→ T^N`

`→ Γ`

`→ X`

The update timing and order must be declared.

## 18. Coupling Operators

### 18.1 Definition

A coupling operator maps states of multiple components into an interaction contribution.

A generic pair coupling operator is:

`C_ij: X_i × X_j → Y_ij`

### 18.2 Collective coupling

For a network of components:

`C: X^N × G → X^N`

may represent the aggregate coupling contribution.

### 18.3 Coupling dependencies

A coupling operator may depend on:

- distance;
- orientation;
- phase difference;
- amplitude;
- species;
- local environment;
- topology;
- delay;
- ternary state;
- external parameters.

Every dependency must be explicit.

### 18.4 Directed coupling

For directed interaction:

`C_ij ≠ C_ji`

may hold.

Symmetry must not be assumed unless declared.

### 18.5 State-dependent coupling

A state-dependent coupling coefficient may be written as:

`K_ij = K_ij(S)`

The dependency rule must be defined before use.

## 19. Delay Operators

### 19.1 Definition

A delay operator returns a previous state value.

For delay `τ`:

`D_τ X(t) = X(t - τ)`

### 19.2 Domain requirement

The history required to evaluate `X(t - τ)` must exist.

For initial time `t₀`, the model must define the required prehistory.

### 19.3 Pair-dependent delay

For pair-dependent delay:

`D_τij X_j(t) = X_j(t - τ_ij)`

### 19.4 Variable delay

A state-dependent delay may be represented as:

`τ = τ(S, t)`

The resulting operator must define how history is sampled when the delay changes.

### 19.5 Delay interpolation

A numerical implementation must declare how delayed values are reconstructed when the requested time does not coincide with a stored sample.

## 20. History Operators

### 20.1 History extraction

A history extraction operator may be written as:

`H_τ: X → X_H`

where it returns the declared history segment required by the model.

### 20.2 History update

A history update operator is:

`U_H: X_H × S_new → X_H`

### 20.3 Finite-memory update

For a discrete history of depth `L`:

`H_n = (S_n, S_n-1, ..., S_n-L+1)`

the update shifts the history and inserts the new state.

### 20.4 Compressed memory

A compressed-memory update is:

`U_μ: X_μ × S → X_μ`

The compressed representation must identify which historical information is retained.

### 20.5 No hidden memory

An implementation must not depend on prior execution state that is absent from the declared history or execution-state representation.

## 21. Dissipation Operators

### 21.1 Definition

A dissipation operator represents irreversible redistribution from declared organized degrees of freedom.

A generic form is:

`D: X → X`

or:

`D: X → X × E_env`

when environmental transfer is represented explicitly.

### 21.2 Dissipative contribution

A dissipative operator may act on:

- amplitude;
- velocity;
- energy;
- phase organization;
- structural modes;
- coupling state.

### 21.3 Physical status

A dissipation operator represents physical model semantics only when its physical meaning is declared.

A numerical stabilization term is not automatically a physical dissipation operator.

### 21.4 Dissipation accounting

When energy accounting is used, the dissipated contribution must remain traceable separately from:

- external work;
- stored energy;
- numerical residual;
- structural work.

## 22. Saturation Operators

### 22.1 Definition

A saturation operator limits a declared response within a bounded or state-dependent regime.

It is written generically as:

`S_sat: A → A`

### 22.2 Required definition

A saturation operator must identify:

- affected variable;
- activation region;
- output rule;
- limiting behavior;
- continuity properties;
- reversibility;
- hysteresis;
- physical or numerical status.

### 22.3 Physical saturation

A physical saturation operator represents a declared physical limiting mechanism.

### 22.4 Numerical clamp

A numerical clamp exists only to constrain numerical representation or execution.

It must be identified separately.

A numerical clamp must not be interpreted as a physical saturation mechanism.

## 23. Resonance-Selection Operators

### 23.1 Definition

A resonance-selection operator evaluates whether a state or parameter configuration belongs to a declared resonance window.

For parameter-state projection:

`R_W: P_R → {OUTSIDE, BOUNDARY, INSIDE}`

### 23.2 Resonance-window region

The resonance window is:

`W_R ⊂ P_R`

### 23.3 Evaluation

The resonance operator must define:

- coordinates of `P_R`;
- window geometry;
- entry criterion;
- exit criterion;
- boundary handling;
- tolerance;
- uncertainty.

### 23.4 State projection

When resonance depends on the complete state:

`P_R: S → P_R`

may first project the state into resonance-coordinate space.

The complete evaluation becomes:

`S → P_R(S) → R_W(P_R(S))`

### 23.5 No automatic structural transition

An output of `INSIDE` from the resonance-selection operator does not imply that a structural transition has occurred.

Structural transition requires its own operator and conditions.

## 24. Phase-Difference Operator

### 24.1 Definition

For phases:

`θ_i`

and:

`θ_j`

the phase-difference operator is:

`Δ_θ(θ_i, θ_j) = wrap(θ_j - θ_i)`

### 24.2 Wrap operator

The wrap operator maps a phase value into the declared canonical phase interval.

The interval must be specified by the model.

### 24.3 Circular semantics

Phase subtraction must respect the circular structure of:

`𝕊¹`

A raw linear difference must not replace the wrapped phase relation when circular equivalence matters.

## 25. Coherence Operators

### 25.1 Definition

A coherence operator maps a declared state relation into a coherence representation:

`Coh: S → Y_coh`

### 25.2 Model dependence

TR-EIF does not assign one universal formula to coherence.

A specific coherence operator must define:

- source variables;
- spatial domain;
- temporal domain;
- normalization;
- output range;
- weighting;
- phase treatment;
- interpretation.

### 25.3 Coherence and uniformity

A coherence operator must not require equality of all local states unless that equality is part of the declared coherence definition.

Coherent states may contain:

- fixed nonzero phase offsets;
- phase clusters;
- counterphase relations;
- spatially structured relations.

## 26. Symmetry-Action Operators

### 26.1 Definition

For transformation:

`g ∈ G_sym`

the action on state space is:

`ρ_S(g): S → S`

### 26.2 Component actions

The complete transformation action may contain distinct operations on:

- coordinates;
- vectors;
- tensors;
- graph nodes;
- graph edges;
- atomic labels;
- ternary states;
- observables.

### 26.3 Geometric transformations

A geometric transformation must preserve the correct transformation class of each object.

A scalar may remain invariant while a vector transforms.

### 26.4 Permutation action

For equivalent indexed components, a permutation may act on:

- node indices;
- atomic-site order;
- edge indices;
- local descriptors;
- state arrays.

The physical identity of the represented configuration must remain consistent.

## 27. Equivariant Operators

### 27.1 Definition

Let:

`F: X → Y`

with input action:

`ρ_X(g)`

and output action:

`ρ_Y(g)`.

The operator `F` is equivariant under the declared transformations when:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for every admissible:

`x ∈ X`

and:

`g ∈ G_sym`

### 27.2 Invariant operator

An invariant operator satisfies:

`F(ρ_X(g)x) = F(x)`

### 27.3 Declared scope

Equivariance must be stated relative to:

- a transformation group or set;
- an input action;
- an output action;
- an admissible domain.

An operator may be equivariant under one transformation class and not another.

### 27.4 Numerical equivariance

A numerical implementation may introduce finite numerical deviation from an exact mathematical equivariance relation.

Such deviation must be measured separately from the mathematical definition.

## 28. Topology Operators

### 28.1 Definition

A topology operator acts on interaction graph:

`G = (V, E)`

### 28.2 Edge-addition operator

An edge-addition operator may be written as:

`A_e: G → G'`

where `G'` contains a declared new edge.

### 28.3 Edge-removal operator

An edge-removal operator is:

`R_e: G → G'`

where the declared edge is removed.

### 28.4 Edge-weight update

An edge-weight operator is:

`U_w: G × W → G'`

### 28.5 Node operations

Node creation or removal is permitted only when the model supports variable-cardinality state spaces.

The operation must update consistently:

- site set;
- coordinate state;
- identity state;
- edge set;
- local environments;
- state indexing;
- traces.

### 28.6 Topology validation

A topology operator must evaluate every invariant affected by the graph change.

## 29. Neighborhood Operators

### 29.1 Definition

A neighborhood operator maps a global configuration into a local environment:

`N_i: Q × G → X_N`

for site `i`.

### 29.2 Neighborhood rule

The operator must define how neighbors are selected.

Possible criteria may depend on:

- graph adjacency;
- geometric distance;
- interaction channel;
- topology;
- species;
- boundary conditions.

### 29.3 Ordering

If a local environment representation depends on neighbor order, the ordering rule must be explicit.

### 29.4 Permutation treatment

When equivalent atom ordering should not affect the result, the neighborhood representation must preserve the declared permutation relation.

## 30. Relative-Geometry Operators

### 30.1 Relative displacement

For sites `i` and `j`:

`R_ij = x_j - x_i`

### 30.2 Distance operator

The pair-distance operator is:

`D_ij = ||x_j - x_i||`

### 30.3 Angular operators

An angular operator may derive orientation relations from declared vectors.

Its coordinate and normalization conventions must be explicit.

### 30.4 Boundary-aware geometry

For periodic or transformed domains, relative geometry must use the declared boundary convention.

Raw coordinate subtraction must not silently replace a boundary-aware relation.

## 31. Interatomic Aggregation Operators

### 31.1 Definition

An aggregation operator combines local or pair contributions into a larger representation:

`A: {y_i} → Y`

or:

`A: {y_ij} → Y`

### 31.2 Aggregation classes

Aggregation may include:

- sum;
- mean;
- weighted sum;
- maximum;
- minimum;
- histogram;
- set aggregation;
- graph aggregation.

### 31.3 Physical meaning

The aggregation rule must match the semantics of the quantity.

An extensive quantity and an intensive quantity must not be aggregated through the same rule without justification.

### 31.4 Permutation behavior

For unordered equivalent components, an aggregation operator may be permutation invariant.

That property must be established explicitly.

## 32. Structural-State Operators

### 32.1 Structural classifier

A structural classifier maps a complete or projected state into a declared structural form:

`C_F: S → F_set`

where `F_set` is the declared set of structural forms.

### 32.2 Structural region

For form `F_k`, the corresponding region is:

`R_F,k ⊆ X_F`

### 32.3 Classification boundary

Boundary states must have explicit treatment.

A state near:

`∂R_F,k`

must not be assigned arbitrarily when uncertainty affects classification.

### 32.4 Structural descriptor operator

A structural descriptor operator maps a state into the structural-state space:

`D_F: S → X_F`

The classification chain is:

`S → D_F(S) → C_F(D_F(S))`

## 33. Structural-Transition Operator

### 33.1 Definition

A structural-transition operator is:

`Ψ_F: R_pre × C_F → R_post`

where:

- `R_pre` is the pre-transition state region;
- `C_F` is the set of transition conditions;
- `R_post` is the post-transition state region.

### 33.2 Requirements

The operator must define:

- transition trigger;
- admissibility guard;
- changing state components;
- preserved state components;
- topology changes;
- symmetry changes;
- ternary-state changes;
- history updates;
- stabilization condition.

### 33.3 Transition trajectory

The transition operator may produce an intermediate trajectory through:

`R_tr`

rather than an instantaneous mapping.

### 33.4 Failure

A failed transition must produce an explicit failure or recovery state.

It must not be reported as a completed structural transition.

## 34. Structural-Work Operators

### 34.1 Definition

A structural-work operator evaluates dynamic activity relative to a declared form:

`W_F: γ[t_a,t_b] × F_k → W_s`

where:

- `γ[t_a,t_b]` is a declared trajectory segment;
- `F_k` is the reference structural form;
- `W_s` is the resulting structural-work representation.

### 34.2 Relative meaning

The sign and interpretation of `W_s` depend on the declared structural evaluation criterion.

### 34.3 No universal scalar

TR-EIF does not prescribe one universal scalar formula for structural work.

A specific model must define:

- evaluated structural capacity;
- trajectory variables;
- accumulation rule;
- sign convention;
- units or normalization;
- validation criterion.

## 35. Inheritance Operators

### 35.1 Extraction operator

The inheritance extraction operator is:

`Λ_I: S_final → X_I`

where `X_I` is the inherited-state space.

### 35.2 Initialization operator

The next-cycle initialization operator is:

`J_I: X_I × X_B → S_initial`

### 35.3 Preserved information

The inheritance operator may preserve declared components such as:

- topology;
- phase organization;
- local environment;
- retained ternary state;
- defects;
- residual stress;
- mode occupation;
- coupling state;
- hysteresis state.

### 35.4 Lossy inheritance

When inheritance discards information, the loss must be explicit.

### 35.5 Recursive composition

A recursive cycle may be written as:

`S_n,final`

`→ Λ_I`

`→ I_n→n+1`

`→ J_I`

`→ S_n+1,initial`

## 36. Observable Operators

### 36.1 Definition

An observable operator is:

`O: S → Y`

### 36.2 Local observable

A local observable may act on one component or neighborhood:

`O_i: S → Y_i`

### 36.3 Global observable

A global observable may aggregate across the full represented system:

`O_global: S → Y_global`

### 36.4 Temporal observable

A temporal observable may depend on a trajectory or history:

`O_H: X_H → Y`

### 36.5 Measurement operator

When a physical measurement chain is represented, the measurement operator must include the declared:

- sampling;
- filtering;
- finite resolution;
- noise model;
- delay;
- quantization;
- calibration.

### 36.6 Observable non-completeness

An observable output does not automatically reconstruct the full internal state.

## 37. Filtering Operators

### 37.1 Definition

A filter maps an input signal or state sequence into a transformed representation:

`F_filter: X_H → Y_filter`

### 37.2 Filter purpose

A filter may be used for:

- noise attenuation;
- band selection;
- smoothing;
- trend extraction;
- state estimation preprocessing.

### 37.3 Physical distinction

A filter changes the representation of the observed or simulated signal.

It does not automatically represent a physical mechanism.

### 37.4 Causality

A real-time filter must declare whether it is causal.

A filter using future values must not be described as an online causal operator.

## 38. Normalization Operators

### 38.1 Definition

A normalization operator maps a quantity into a declared normalized representation:

`N: A → A_norm`

### 38.2 Required metadata

Normalization must define:

- reference value;
- scale;
- offset;
- output domain;
- inverse mapping where available.

### 38.3 Dimensional meaning

Normalization may remove physical units from the numerical representation.

The original dimensional provenance must remain recoverable when required.

### 38.4 No silent normalization

A normalized value must not be presented as the original dimensional quantity.

## 39. Nondimensionalization Operators

### 39.1 Definition

A nondimensionalization operator maps physical quantities into dimensionless variables using declared reference scales.

### 39.2 Reference scales

Every reference scale must have:

- definition;
- units;
- provenance;
- applicable model scope.

### 39.3 Inverse reconstruction

When required, the inverse dimensional mapping must be defined.

### 39.4 Cross-model comparison

Dimensionless quantities from different models are comparable only when their nondimensionalization conventions are compatible.

## 40. Numerical Discretization Operators

### 40.1 Definition

A discretization operator maps a continuous mathematical object into a numerical representation.

A generic form is:

`D_h: X → X_h`

where `h` denotes the declared discretization parameters.

### 40.2 Time discretization

A continuous trajectory may be represented at:

`t_n = t_0 + nΔt`

for uniform time step `Δt`.

### 40.3 Spatial discretization

A continuous spatial domain may be represented by a finite set of points, cells, basis functions, or graph elements.

### 40.4 Discretization metadata

The operator must define:

- discretization scale;
- numerical representation;
- boundary treatment;
- approximation order where applicable;
- error metric;
- stability conditions where applicable.

### 40.5 Mathematical–numerical separation

The discretized operator is not identical to the original continuous operator.

The distinction must remain explicit.

## 41. Quantization Operators

### 41.1 Definition

A quantization operator maps a numerical value into a finite representable set:

`Q: A → A_q`

### 41.2 Quantization rule

The operator must define:

- representable values;
- resolution;
- rounding rule;
- saturation behavior;
- overflow behavior;
- signedness;
- precision.

### 41.3 Quantization and ternary projection

Quantization is not the same operation as ternary projection.

A fixed-point or integer value may remain a continuous-variable approximation in model semantics.

A ternary state belongs specifically to:

`{-1, 0, 1}`

with TR-EIF transition semantics.

## 42. Constraint Operators

### 42.1 Definition

A constraint operator evaluates whether a state satisfies a declared condition:

`C: S → {true, false}`

### 42.2 Constraint classes

Constraints may be:

- mathematical;
- physical;
- topological;
- structural;
- numerical;
- implementation-specific;
- validation-specific.

### 42.3 Constraint enforcement

A constraint may be enforced by:

- rejection;
- guarded retention;
- projection;
- corrective update;
- transition inhibition;
- failure.

The enforcement mechanism must be explicit.

### 42.4 No hidden correction

An invalid state must not be silently modified into an admissible state without traceable operator action.

## 43. Guard Operators

### 43.1 Definition

A guard operator determines whether an event or transition may execute:

`G_e: S × C → {ALLOW, BLOCK}`

### 43.2 Guard dependencies

A guard may depend on:

- current state;
- previous state;
- topology;
- capacity;
- history;
- resonance state;
- structural state;
- boundary conditions;
- invariant status.

### 43.3 Blocked transition

A blocked transition must define the resulting state.

Possible outcomes include:

- retain current state;
- enter active neutral state;
- remain in active neutral state;
- queue transition;
- fail execution.

The result must follow the model contract.

## 44. Routing Operators

### 44.1 Definition

A routing operator selects an admissible processing or transition path:

`R: S × C → Path`

### 44.2 Ternary routing

For opposite-state transitions, routing must preserve:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

### 44.3 Route persistence

A pending route may become part of the execution state when completion is delayed.

### 44.4 Routing conflict

When several routes compete, the conflict-resolution rule must be explicit.

## 45. Comparison Operators

### 45.1 Exact comparison

Exact state comparison evaluates equality under the declared exact representation.

### 45.2 Numerical comparison

A numerical comparison operator may use:

- absolute tolerance;
- relative tolerance;
- norm-based tolerance;
- component-specific tolerance.

### 45.3 Structural comparison

A structural comparison operator evaluates declared relations or invariants rather than coordinate identity.

### 45.4 Observable comparison

An observable comparison operates only in observable space.

It must not be interpreted automatically as full-state equality.

## 46. Metric Operators

### 46.1 State metric

A state metric is:

`d_S: S × S → ℝ₊`

when the metric axioms are satisfied over the declared space.

### 46.2 Pseudometric

When distinct states may have zero declared distance, the construction is not a metric unless the state equivalence is quotient-defined.

### 46.3 Component metrics

Different state components may require distinct distance functions.

Examples include:

- Euclidean distance for coordinate vectors;
- circular phase distance;
- ternary mismatch count;
- graph difference;
- structural descriptor distance.

### 46.4 Composite metric

A composite metric must define normalization before combining quantities with different dimensions or scales.

## 47. Validation Operators

### 47.1 Invariant evaluator

For invariant `I_k`, an evaluation operator is:

`V_k: S → {PASS, FAIL}`

or, when evaluation may be unavailable:

`V_k: S → {PASS, FAIL, NOT_EVALUATED}`

### 47.2 Aggregate validation

A validation aggregate operator may combine several invariant states.

The aggregation rule must not allow a failed required invariant to disappear behind an average score.

### 47.3 Transition validation

A ternary transition validator must inspect the transition path, not only the final state.

### 47.4 Trace validation

A trace-validation operator may evaluate:

- schema validity;
- state continuity;
- transition legality;
- event order;
- invariant visibility;
- version consistency;
- deterministic replay requirements.

## 48. Failure Operators

### 48.1 Definition

A failure operator maps an invalid execution condition into an explicit failure state:

`F_fail: S × E_fail → S_fail`

### 48.2 Failure record

A failure operation must preserve:

- failure class;
- location;
- time or step;
- triggering state;
- triggering event;
- affected operator;
- resulting action.

### 48.3 Failure non-substitution

Failure must not be encoded as:

- valid ternary `0`;
- numeric zero;
- empty output;
- successful completion.

## 49. Operator Commutativity

### 49.1 Definition

Two operators `A` and `B` commute when:

`A ∘ B = B ∘ A`

over the declared domain.

### 49.2 No default commutativity

TR-EIF does not assume operator commutativity.

For example, the order of:

- projection and evolution;
- quantization and transformation;
- filtering and thresholding;
- topology update and neighborhood extraction;
- ternary update and continuous update;

may change the result.

### 49.3 Proof requirement

Operator reordering is permitted only when commutativity or an applicable equivalence relation is established.

## 50. Operator Associativity

### 50.1 Composition associativity

For compatible mappings:

`H ∘ (G ∘ F) = (H ∘ G) ∘ F`

at the level of mathematical function composition.

### 50.2 Numerical realization

A numerical implementation may produce different floating-point results when arithmetic evaluation is regrouped.

Mathematical associativity and finite-precision arithmetic behavior must remain distinct.

## 51. Operator Invertibility

### 51.1 Inverse operator

An operator:

`F: A → B`

is invertible over its declared domain when there exists:

`F^-1: B → A`

such that the declared inverse relations hold.

### 51.2 Lossy operators

Projection, aggregation, filtering, quantization, and coarse-graining may be non-invertible.

### 51.3 No implicit reconstruction

A non-invertible operator must not be treated as invertible through arbitrary reconstruction.

Any approximate inverse must be defined as a separate operator.

## 52. Operator Linearity

### 52.1 Linear operator

For an operator `L` over an appropriate vector space, linearity requires preservation of the declared additive and scalar-multiplicative structure.

### 52.2 Nonlinear operator

An operator that does not satisfy the declared linearity relation is nonlinear.

### 52.3 TR-EIF default

TR-EIF does not assume global linearity of system evolution.

Linear operators may appear as local or component operations inside a nonlinear model.

### 52.4 Local linearization

A nonlinear operator may be locally approximated by a linear operator around a declared reference state.

The reference state and validity region must be explicit.

## 53. Time-Dependent Operators

### 53.1 Definition

A time-dependent operator is written as:

`L_t`

or:

`L(t)`

### 53.2 Sources of time dependence

Time dependence may arise from:

- external forcing;
- changing boundary conditions;
- dynamic topology;
- parameter modulation;
- scheduled execution;
- evolving environment.

### 53.3 Autonomous operators

An autonomous operator has no explicit dependence on absolute time, although it may depend on the current state.

## 54. State-Dependent Operators

### 54.1 Definition

A state-dependent operator may be represented as:

`L_S`

or:

`L(S)`

### 54.2 Examples

State dependence may modify:

- coupling;
- delay;
- dissipation;
- topology;
- projection thresholds;
- saturation;
- transition guards.

### 54.3 Operator-state consistency

When the operator itself changes with system state, the state required to construct the operator must be part of the declared execution dependency.

## 55. Parameterized Operators

### 55.1 Definition

A parameterized operator is:

`L_p: A → B`

where:

`p ∈ P`

### 55.2 Parameter provenance

Every parameter affecting an operator must have declared provenance.

### 55.3 Parameter domain

The valid parameter subset must be explicit:

`P_L ⊆ P`

An operator evaluated outside `P_L` must produce an explicit unsupported or invalid state unless a documented extrapolation rule exists.

## 56. Stochastic Operators

### 56.1 Definition

A stochastic operator maps an input state into a probability distribution or stochastic outcome.

### 56.2 Random source

Every stochastic implementation must identify:

- random-number generator;
- seed;
- distribution;
- parameters;
- sampling procedure.

### 56.3 Deterministic replay

A stochastic model may support deterministic computational replay when its complete random state is preserved.

### 56.4 Stochastic and uncertain distinction

Stochastic dynamics and uncertainty about a deterministic state are different mathematical objects.

They must not be conflated.

## 57. Multiscale Operators

### 57.1 Upward operator

A scale-transfer operator from fine scale `s` to coarse scale `r` is:

`M_s→r: S_s → S_r`

### 57.2 Downward operator

A coarse-to-fine influence operator is:

`M_r→s: S_r → S_s`

### 57.3 Loss of information

An upward coarse-graining operator may be lossy.

### 57.4 Reconstruction

A downward operator must not be assumed to reconstruct discarded microscopic information.

### 57.5 Cross-scale consistency

A pair of scale-transfer operators must define the compatibility relations used to compare the two scale descriptions.

## 58. Hybrid Operator Sequence

A general TR-EIF hybrid execution may be represented by the operator sequence:

`S_n`

`→ continuous evolution`

`→ delayed-state evaluation`

`→ coupling evaluation`

`→ resonance-state evaluation`

`→ continuous-to-ternary projection`

`→ transition-guard evaluation`

`→ ternary update`

`→ topology or structural update where triggered`

`→ history update`

`→ invariant validation`

`→ observable projection`

`→ trace emission`

`→ S_n+1`

This sequence is a formal operator architecture.

A specific model must define the operators it actually uses and their exact execution order.

## 59. Operator Dependency Rules

The following dependency rules apply:

1. An operator must not consume an undefined state object.

2. An operator must not return an undeclared state type.

3. A projection must identify lost information.

4. An embedding must identify introduced information.

5. A transition operator must preserve ternary admissibility.

6. A delay operator must have sufficient history.

7. A topology operator must update affected graph-dependent states.

8. A structural-transition operator must identify changed invariants.

9. An observable operator must remain distinct from the complete state.

10. A numerical operator must remain distinct from its continuous mathematical source.

11. A validation operator must not suppress failure.

12. A parameterized operator must preserve parameter provenance.

## 60. Operator Invariants

The following invariants apply to TR-EIF mathematical operators.

1. Every operator has a declared domain.

2. Every operator has a declared codomain.

3. Every operator preserves state-type semantics unless an explicit mapping changes type.

4. Continuous and ternary operators remain distinct.

5. The balanced ternary codomain is exactly `{-1, 0, 1}` where applicable.

6. The active state `0` remains operationally active.

7. No operator may produce a direct `-1 → 1` transition.

8. No operator may produce a direct `1 → -1` transition.

9. Opposite-state transitions require separate neutral-mediated legs.

10. Missing data are not mapped silently to ternary `0`.

11. Projection loss is explicit.

12. Embedding additions have provenance.

13. Delay operators preserve required history dependence.

14. Physical dissipation and numerical stabilization remain distinguishable.

15. Resonance evaluation and structural transition remain separate operations.

16. Equivariance claims define both transformation actions.

17. Topology changes are explicit operator events.

18. Structural inheritance is represented by declared mappings.

19. Numerical discretization remains distinguishable from continuous mathematics.

20. Validation failures remain visible.

## 61. Operator Conformance Requirements

A TR-EIF mathematical model conforms to this operator architecture when:

- every operator is defined before use;
- every domain and codomain is explicit;
- every composition is type-compatible;
- every transition operator preserves ternary invariants;
- every continuous-discrete conversion is explicit;
- every delay has history support;
- every topology operation is traceable;
- every structural operation identifies its conditions;
- every observable is produced by a declared projection;
- every numerical approximation identifies its mathematical source.

A TR-EIF implementation conforms when:

- the implemented operator order matches the approved mathematical order;
- no hidden operator modifies state;
- no operator silently changes state type;
- no invalid ternary transition occurs;
- numerical and physical operations remain distinguishable;
- failures remain visible in execution traces.

## 62. Operator Separation Rules

The following operator classes must not be silently substituted for one another:

`projection ≠ embedding`

`projection ≠ measurement`

`quantization ≠ ternary projection`

`filtering ≠ physical dissipation`

`numerical clamp ≠ physical saturation`

`resonance selection ≠ structural transition`

`state update ≠ topology update`

`topology update ≠ structural transition`

`observable mapping ≠ full-state reconstruction`

`coarse-graining ≠ exact reduction`

`approximate inverse ≠ exact inverse`

`numerical derivative ≠ exact derivative`

`numerical integral ≠ exact integral`

`operator equality ≠ approximate numerical agreement`

## 63. Operator Construction Order

The operator construction order for a TR-EIF model is:

`state-space definition`

`→ operator domain`

`→ operator codomain`

`→ mathematical action`

`→ parameter dependence`

`→ state dependence`

`→ transformation behavior`

`→ admissibility conditions`

`→ invariant behavior`

`→ numerical realization`

`→ validation`

An implementation must not precede the mathematical definition of the operator it claims to realize.

## 64. Final Operator Statement

TR-EIF mathematical evolution is represented through explicit typed operators acting on declared state spaces.

The operator architecture preserves the separation between:

- continuous evolution;
- balanced ternary `-1/0/1` transition semantics;
- active neutral mediation;
- delayed and historical dependence;
- interatomic coupling;
- topology;
- resonance-state evaluation;
- equivariant transformation;
- structural transition;
- recursive inheritance;
- observable projection;
- numerical realization;
- validation.

Every mathematical transformation must therefore be expressible as a traceable relation of the form:

`declared input space`

`→ declared operator`

`→ declared output space`

`→ invariant evaluation`

`→ traceable state result`
