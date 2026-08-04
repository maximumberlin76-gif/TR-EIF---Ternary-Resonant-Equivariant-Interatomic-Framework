# State Spaces

## 1. Purpose

This document defines the state-space architecture of the Ternary Resonant Equivariant Interatomic Framework.

The state-space architecture establishes:

- which mathematical objects constitute a TR-EIF state;
- how continuous, ternary, topological, historical, parametric, and observable components are separated;
- how admissible states are distinguished from invalid states;
- how state trajectories are represented;
- how transformations act on state spaces;
- how continuous and discrete state layers interact;
- how structural transitions modify the effective state space;
- how deterministic execution preserves state provenance.

A TR-EIF model must define its state spaces before defining its complete evolution equations.

An evolution rule is not mathematically complete unless its domain, codomain, admissible inputs, and resulting state type are declared.

## 2. Status of This Document

The state-space architecture defined here is part of the TR-EIF formal system.

The definitions in this document are framework definitions.

They do not assert that every physical system must use every state component introduced here.

A specific TR-EIF model must select the state spaces required by its declared scope and must not reference omitted state components implicitly.

This document depends on:

- `chapter_01_foundations.md`;
- `chapter_02_notation_and_definitions.md`;
- `chapter_03_axiomatic_system.md`.

## 3. State-Space Construction Principle

A TR-EIF state space is constructed from explicitly typed components.

The general construction order is:

`physical system boundary`

`→ represented degrees of freedom`

`→ primitive state variables`

`→ component state spaces`

`→ admissibility conditions`

`→ composite state space`

`→ evolution domain`

`→ observable projection`

The state space must be sufficiently complete for the declared model.

Completeness is model-relative.

A state representation is sufficient when it contains every variable required to determine the permitted future evolution under the declared evolution contract.

## 4. State-Space Categories

TR-EIF distinguishes the following state-space categories:

1. continuous state space;
2. balanced ternary state space;
3. configuration state space;
4. topology state space;
5. interaction state space;
6. oscillatory state space;
7. history and memory state space;
8. structural state space;
9. parameter state space;
10. boundary and environment state space;
11. numerical execution state space;
12. observable output space;
13. validation and invariant state space.

These categories may overlap in implementation only when their semantic distinctions remain explicit.

A single serialized record may contain several state categories.

Serialization does not merge their mathematical meanings.

## 5. Continuous State Space

### 5.1 Definition

The continuous state space is denoted by:

`X`

A continuous state at time `t` is:

`X(t) ∈ X`

The continuous state space contains variables represented over continuous numerical domains.

Typical components may include:

- positions;
- velocities;
- amplitudes;
- phases;
- frequencies;
- energies;
- forces;
- stresses;
- coupling strengths;
- dissipative variables;
- delay variables;
- propagation variables;
- continuous structural descriptors.

### 5.2 Product representation

When the continuous state contains `M` components, it may be represented as a product space:

`X = X₁ × X₂ × ... × X_M`

where each `X_k` is the domain of one declared state component.

Each factor must define:

- value domain;
- dimensionality;
- units where applicable;
- coordinate convention;
- admissible range;
- transformation behavior.

### 5.3 Continuous state vector

A coordinate representation of the continuous state may be written as:

`X(t) = (x₁(t), x₂(t), ..., x_M(t))`

This notation does not require every component to be scalar.

A component may itself be:

- a vector;
- a matrix;
- a tensor;
- a field;
- a graph-associated value;
- a local-environment descriptor.

### 5.4 State-space dimension

The dimension of a finite-dimensional continuous state space is denoted by:

`dim(X)`

The dimension must be declared when required by:

- numerical integration;
- Jacobian construction;
- stability analysis;
- storage allocation;
- transformation definition;
- model comparison.

A dynamically changing number of represented objects may require:

- a variable-dimensional state space;
- a family of fixed-dimensional spaces;
- an embedding into a larger state space;
- an explicit birth, removal, or topology-change operation.

### 5.5 Coordinate dependence

A coordinate representation is not identical to the abstract state.

The same physical or mathematical state may have different coordinate representations.

A change of coordinates must identify:

- original coordinate space;
- target coordinate space;
- transformation rule;
- inverse rule where available;
- preserved quantities;
- singular regions.

## 6. Configuration State Space

### 6.1 Definition

The configuration state space contains the represented spatial and identity configuration of the interatomic system.

It is denoted by:

`Q`

A configuration at time `t` is:

`q(t) ∈ Q`

### 6.2 Atomic configuration

For `N` atomic sites in spatial dimension `d`, a configuration may contain:

`q(t) = ((z₁, x₁(t)), ..., (z_N, x_N(t)))`

where:

- `z_i` is the identity label of site `i`;
- `x_i(t) ∈ ℝ^d` is the position of site `i`.

The identity labels and positions remain distinct state components.

### 6.3 Fixed-cardinality configuration space

When the number of sites is fixed, the position component may be represented by:

`Q_pos = (ℝ^d)^N`

The complete configuration space may also include:

- atomic identities;
- cell geometry;
- periodic boundary data;
- occupancy states;
- site labels;
- external constraints.

### 6.4 Variable-cardinality configuration space

When the number of represented sites may change, the configuration space must define:

- admissible site creation;
- admissible site removal;
- identity assignment;
- index reassignment;
- conservation conditions where applicable;
- topology update;
- trace representation.

A change in cardinality must not occur through silent array resizing.

### 6.5 Configuration equivalence

Two coordinate configurations may represent the same physical arrangement under a declared transformation.

Possible equivalence relations include:

- global translation;
- global rotation;
- reflection where physically admissible;
- permutation of equivalent atomic labels;
- periodic-cell translation.

The equivalence relation must be declared before quotienting the configuration space.

## 7. Phase Space

### 7.1 Definition

A mechanical or dynamical phase space may combine configuration and momentum or velocity variables.

A generic phase space is denoted by:

`P_dyn`

A phase-space state may be written as:

`p_dyn(t) = (q(t), v(t))`

where:

- `q(t) ∈ Q` is the configuration;
- `v(t)` is the complete velocity state.

### 7.2 Separation from oscillator phase

The term phase space is distinct from the oscillator phase variable `θ_i(t)`.

The repository must not use the word phase ambiguously.

The following are different objects:

- dynamical phase space;
- oscillator phase;
- phase difference;
- phase relation;
- phase-locking state.

### 7.3 Extended phase space

An extended phase space may include additional variables such as:

- time;
- thermostat state;
- dissipative state;
- memory variables;
- control state;
- external forcing phase.

The extension must define all added dimensions explicitly.

## 8. Oscillatory State Space

### 8.1 Definition

The oscillatory state space contains the variables required to represent the oscillatory dynamics of one or more components.

It is denoted by:

`X_osc`

A generic oscillatory state for component `i` may be written as:

`x_osc,i(t) = (a_i(t), θ_i(t), ω_i(t), ξ_i(t))`

where:

- `a_i(t)` is amplitude;
- `θ_i(t)` is phase;
- `ω_i(t)` is angular frequency;
- `ξ_i(t)` represents additional declared internal variables.

### 8.2 Amplitude domain

The amplitude domain is:

`A_i ⊆ ℝ₊`

A model may use a signed amplitude only when the sign convention is defined explicitly.

The amplitude space must identify:

- lower bound;
- upper bound where present;
- saturation behavior;
- zero-amplitude semantics;
- units or normalization.

### 8.3 Phase domain

The phase domain is:

`Θ_i = 𝕊¹`

A numerical phase interval may be represented as:

`[0, 2π)`

or:

`(-π, π]`

The selected interval does not change the circular topology.

### 8.4 Frequency domain

The frequency domain is denoted by:

`Ω_i`

The model must distinguish among:

- intrinsic frequency;
- instantaneous frequency;
- effective frequency;
- externally imposed frequency;
- mode frequency;
- numerically estimated frequency.

### 8.5 Collective oscillatory state

For `N_osc` oscillatory components:

`X_osc = X_osc,1 × ... × X_osc,N_osc`

The collective state may contain coupling-dependent variables that are not reducible to independent local oscillator states.

Examples include:

- collective order parameters;
- mode populations;
- phase-cluster labels;
- coupling matrices;
- delayed phase relations.

## 9. Balanced Ternary State Space

### 9.1 Primitive ternary set

The balanced ternary state set is:

`T = {-1, 0, 1}`

The canonical notation is:

`-1/0/1`

### 9.2 Local ternary state

The ternary state of component `i` is:

`σ_i ∈ T`

The interpretation of `σ_i` must be defined by the corresponding model contract.

The values `-1`, `0`, and `1` must not be assigned undocumented physical meanings.

### 9.3 Global ternary configuration

For `N_T` ternary components:

`Σ_T = T^N_T`

A complete ternary configuration is:

`σ = (σ₁, ..., σ_N_T) ∈ Σ_T`

### 9.4 Active neutral state

The state `0` is active.

Its state-space role may include:

- mediation;
- balancing;
- routing;
- damping;
- retention;
- capacity waiting;
- transition staging;
- conflict resolution.

The neutral state occupies a valid region of the ternary state space.

It is not outside the state space.

### 9.5 Admissible ternary transitions

The local transition relation is denoted by:

`R_T ⊆ T × T`

The following local transitions are admissible unless a narrower model contract restricts them:

- `-1 → -1`;
- `-1 → 0`;
- `0 → -1`;
- `0 → 0`;
- `0 → 1`;
- `1 → 0`;
- `1 → 1`.

The following direct transitions are forbidden:

- `-1 → 1`;
- `1 → -1`.

### 9.6 Global ternary transition

A global ternary transition is:

`σ_n → σ_n+1`

where both configurations belong to `Σ_T`.

A global update may change:

- one local component;
- several independent local components;
- several coupled local components.

The update contract must define whether local state changes are evaluated:

- sequentially;
- synchronously;
- transactionally;
- by priority;
- by capacity;
- by graph partition.

### 9.7 Ternary admissible subset

A specific model may restrict the global ternary space to an admissible subset:

`Σ_T,adm ⊆ Σ_T`

Restrictions may arise from:

- capacity limits;
- conservation conditions;
- topology constraints;
- mutual exclusion;
- boundary conditions;
- structural invariants.

The restriction must be explicit and testable.

## 10. Topology State Space

### 10.1 Definition

The topology state space contains all interaction-graph configurations permitted by the model.

It is denoted by:

`X_G`

A topology state is:

`G(t) ∈ X_G`

### 10.2 Fixed topology

For fixed topology:

`G(t) = G₀`

for every permitted time `t`.

The graph structure remains constant while graph-associated values may still change.

### 10.3 Dynamic topology

For dynamic topology:

`G(t₁) ≠ G(t₂)`

may hold for distinct times `t₁` and `t₂`.

A topology transition must define:

- edge creation rule;
- edge removal rule;
- node creation rule where permitted;
- node removal rule where permitted;
- weight update rule;
- direction update rule;
- invariant checks;
- trace event.

### 10.4 Graph state decomposition

A topology state may contain:

`G(t) = (V(t), E(t), W(t), C(t))`

where:

- `V(t)` is the node set;
- `E(t)` is the edge set;
- `W(t)` is the collection of edge weights;
- `C(t)` is the collection of edge or node channel labels.

Every component must have a declared type.

### 10.5 Topology admissibility

The admissible topology subset is:

`X_G,adm ⊆ X_G`

Admissibility conditions may include:

- connectivity;
- bounded degree;
- permitted species relations;
- geometric cutoff;
- symmetry;
- direction constraints;
- channel compatibility;
- capacity constraints.

## 11. Interaction State Space

### 11.1 Definition

The interaction state space contains the variables that characterize active interactions independently of the node configuration.

It is denoted by:

`X_int`

An interaction state may include:

- coupling strengths;
- edge activation states;
- interaction channels;
- pairwise delays;
- local impedance;
- transmission coefficients;
- dissipative coefficients;
- ternary edge states.

### 11.2 Edge-local interaction state

For edge `e_ij`, an interaction state may be written as:

`χ_ij(t) ∈ X_ij`

The complete interaction state is:

`χ(t) ∈ ∏ X_ij`

where the product extends over the active edge set.

### 11.3 Interaction-state dependence

The interaction state may depend on:

- atomic identities;
- distance;
- orientation;
- local environment;
- phase relation;
- amplitude;
- topology;
- history;
- external forcing;
- ternary routing state.

The dependency must be represented by explicit mappings.

## 12. History State Space

### 12.1 Definition

The history state space contains the prior information required for future evolution.

It is denoted by:

`X_H`

A history state at time `t` is:

`H(t) ∈ X_H`

### 12.2 Finite-history representation

For maximum delay `τ_max`, a continuous history segment may be represented as:

`H_X(t) = {X(s) | s ∈ [t - τ_max, t]}`

The numerical implementation must define:

- sampling rule;
- interpolation rule;
- storage interval;
- precision;
- initialization.

### 12.3 Discrete history representation

A discrete history of depth `L` may be written as:

`H_n = (S_n, S_n-1, ..., S_n-L+1)`

where `L` is the number of retained states.

### 12.4 Compressed memory state

A model may replace full history by a compressed memory state:

`μ(t) ∈ X_μ`

The update rule must define:

`μ(t) → μ(t + Δt)`

The compressed state must retain the information required by the declared model.

A compressed memory representation must not be described as equivalent to full history unless that equivalence is established.

### 12.5 Hysteretic state

A hysteretic state records path-dependent regime information.

It may include:

- previous threshold-crossing direction;
- retained branch identity;
- previous extrema;
- switching state;
- accumulated structural work;
- prior topology regime.

## 13. Structural State Space

### 13.1 Definition

The structural state space contains the variables and relations used to distinguish declared structural forms.

It is denoted by:

`X_F`

A structural state is:

`f_struct(t) ∈ X_F`

### 13.2 Structural form

A structural form is denoted by:

`F_k`

Each form corresponds to a declared admissible region:

`R_F,k ⊆ X_F`

A state belongs to form `F_k` when its structural state satisfies the conditions defining `R_F,k`.

### 13.3 Structural variables

Structural variables may include:

- topology class;
- symmetry class;
- local-environment distribution;
- phase-cluster configuration;
- mode population;
- energy-pathway organization;
- ternary-state distribution;
- defect state;
- connectivity;
- retained memory.

### 13.4 Structural boundary

The boundary of a structural region is:

`∂R_F,k`

Crossing `∂R_F,k` is not sufficient by itself to establish a completed structural transition.

The model must also define:

- transition trajectory;
- post-transition admissibility;
- stabilization condition;
- retained invariants;
- broken invariants.

### 13.5 Structural transition map

A structural transition may be represented by:

`Ψ_F: R_F,k × C_F → R_F,k+1`

where:

- `C_F` is the set of declared transition conditions;
- `R_F,k` is the pre-transition region;
- `R_F,k+1` is the post-transition region.

The transition map may be deterministic or nondeterministic.

Its status must be declared.

## 14. Parameter State Space

### 14.1 Definition

The parameter space is denoted by:

`P`

A parameter state is:

`p ∈ P`

Parameters are distinct from dynamic state variables unless the model explicitly permits parameter evolution.

### 14.2 Fixed parameters

A fixed parameter remains constant during one declared execution.

Examples may include:

- atomic masses;
- model coefficients;
- boundary dimensions;
- numerical tolerances;
- benchmark settings.

### 14.3 Dynamic parameters

A dynamic parameter becomes part of the state when its value evolves during execution.

A time-dependent quantity must not remain classified as a fixed parameter when it affects future evolution.

### 14.4 Parameter product space

The parameter space may be represented as:

`P = P₁ × ... × P_K`

Each parameter component must define:

- symbol;
- domain;
- units;
- provenance;
- admissible range;
- uncertainty where applicable;
- execution role.

### 14.5 Parameter admissibility

The admissible parameter subset is:

`P_adm ⊆ P`

A parameter vector outside `P_adm` must produce:

- explicit rejection;
- explicit unsupported-state result;
- explicit failure trace.

It must not produce a silently qualified result.

## 15. Boundary and Environment State Space

### 15.1 Definition

The boundary and environment state space contains external variables that affect the represented system.

It is denoted by:

`X_B`

A boundary state is:

`b(t) ∈ X_B`

### 15.2 Boundary-state components

Boundary variables may include:

- external force;
- imposed displacement;
- pressure;
- temperature;
- field value;
- incoming wave state;
- outgoing-wave condition;
- material flux;
- control input;
- spatial constraint;
- periodic-cell parameters.

### 15.3 Autonomous and driven systems

An autonomous model does not depend explicitly on an external time-dependent input.

A driven model depends on a declared boundary or forcing trajectory:

`b: I_t → X_B`

The forcing trajectory must be included in the execution record.

### 15.4 Environment coupling map

A boundary-coupling map may be written as:

`C_B: S × X_B → X`

The map defines how the environment affects the internal continuous state.

A separate map may define system output into the environment.

## 16. Numerical Execution State Space

### 16.1 Definition

The numerical execution state space contains computational variables required for deterministic realization but not necessarily part of the physical model state.

It is denoted by:

`X_num`

### 16.2 Numerical-state components

The numerical state may include:

- integration-stage values;
- iteration counters;
- solver status;
- convergence state;
- random-number-generator state;
- precision mode;
- queue state;
- buffer state;
- pending transition state;
- overflow flags;
- error estimates.

### 16.3 Physical and numerical separation

The complete computational state may be written as:

`S_comp = (S_phys, S_num)`

where:

- `S_phys` is the represented physical or mathematical model state;
- `S_num` is the numerical execution state.

A numerical variable must not be interpreted as a physical state variable unless an explicit physical mapping is defined.

### 16.4 Deterministic sufficiency

For deterministic replay, the numerical execution state must contain or reference every computational variable that can affect future results.

This may include:

- random generator state;
- pending event order;
- floating-point mode;
- solver branch;
- adaptive-step history;
- thread or task ordering where relevant.

## 17. Validation State Space

### 17.1 Definition

The validation state space contains invariant states, error states, qualification states, and execution-status values.

It is denoted by:

`X_val`

### 17.2 Invariant state

For invariant `I_j`, the validation state may contain:

`v_j ∈ {PASS, FAIL, NOT_EVALUATED}`

A binary representation may be used only when the unevaluated state is represented elsewhere.

### 17.3 Failure state

A failure state must identify:

- failure class;
- affected component;
- time or execution step;
- source state;
- preceding event;
- resulting action;
- trace location.

### 17.4 Qualification state

A qualification state may distinguish:

- untested;
- tested;
- passed;
- failed;
- unsupported;
- invalidated;
- superseded.

These statuses must not be collapsed into one boolean when the distinction affects interpretation.

## 18. Observable Output Space

### 18.1 Definition

The observable output space is denoted by:

`Y`

An observable is:

`y(t) ∈ Y`

### 18.2 Observable mapping

The observable mapping is:

`O: S → Y`

The mapping may be:

- lossless;
- lossy;
- local;
- global;
- instantaneous;
- delayed;
- averaged;
- sampled;
- stochastic.

Its properties must be declared.

### 18.3 Observable product space

When several observables are emitted:

`Y = Y₁ × ... × Y_R`

Each observable component must define:

- source state;
- mapping rule;
- units;
- precision;
- temporal index;
- spatial index;
- uncertainty;
- provenance.

### 18.4 Hidden state

A state component not included in `Y` remains part of the internal state when required by the model.

Equality of observables:

`O(S₁) = O(S₂)`

does not imply:

`S₁ = S₂`

unless injectivity of `O` is established over the declared domain.

## 19. Composite TR-EIF State Space

### 19.1 General composition

A general TR-EIF state space may be written as:

`S = X × Σ_T × X_G × X_H × X_F × X_B × X_num × X_val`

where:

- `X` is the continuous state space;
- `Σ_T` is the global ternary state space;
- `X_G` is the topology state space;
- `X_H` is the history state space;
- `X_F` is the structural state space;
- `X_B` is the boundary state space;
- `X_num` is the numerical execution state space;
- `X_val` is the validation state space.

A specific model may use a strict subset of these factors.

### 19.2 Composite state

A complete state may be written as:

`S(t) = (X(t), σ(t), G(t), H(t), f_struct(t), b(t), n_state(t), v_state(t))`

Each component must belong to its declared factor space.

### 19.3 Model-specific reduction

A reduced model may define:

`S_red ⊂ S`

The reduction must identify:

- omitted components;
- fixed components;
- approximated dependencies;
- validity conditions;
- information loss;
- resulting limitations.

### 19.4 No implicit components

A model must not omit a component from its declared state while allowing that component to affect future evolution through hidden implementation state.

## 20. Admissible State Space

### 20.1 Definition

The admissible state space is denoted by:

`S_adm ⊆ S`

A state is admissible when it satisfies every applicable:

- domain condition;
- boundary condition;
- topology condition;
- ternary invariant;
- physical constraint;
- numerical constraint;
- structural constraint;
- provenance requirement.

### 20.2 Invalid state

An invalid state is:

`S_invalid ∈ S \ S_adm`

An invalid state must not be silently projected into `S_adm`.

The execution contract must define whether an invalid state causes:

- rejection;
- rollback;
- guarded retention;
- transition to active neutral state where semantically valid;
- explicit failure;
- controlled recovery.

### 20.3 Admissibility predicate

An admissibility predicate may be written as:

`A_S: S → {true, false}`

The state is admissible when:

`A_S(S) = true`

The predicate must identify every tested condition.

### 20.4 Local and global admissibility

A state may satisfy all local conditions while violating a global invariant.

Examples include:

- local ternary validity with global capacity overflow;
- local distance validity with global topology inconsistency;
- local energy validity with global accounting residual;
- local symmetry compliance with global transformation failure.

Both local and global admissibility must be checked where applicable.

## 21. State Constraints

### 21.1 Equality constraints

An equality constraint has the form:

`C_eq(S) = 0`

The meaning and units of `C_eq` must be declared.

### 21.2 Inequality constraints

An inequality constraint may have the form:

`C_ineq(S) ≤ 0`

The sign convention must be explicit.

### 21.3 Discrete constraints

A discrete constraint may restrict:

- permitted ternary configurations;
- graph connectivity;
- state labels;
- event ordering;
- capacity;
- mode membership.

### 21.4 Constraint provenance

A constraint must be classified as:

- mathematical;
- physical;
- numerical;
- structural;
- implementation;
- validation;
- benchmark-specific.

A numerical convenience constraint must not be presented as a physical law.

## 22. State-Space Metrics and Distances

### 22.1 Metric definition

A metric on state space `S` is a mapping:

`d_S: S × S → ℝ₊`

A declared metric must define how differences between state components are combined.

### 22.2 Continuous-state distance

A continuous-state distance may use a norm:

`d_X(X₁, X₂) = ||X₁ - X₂||`

The selected norm must be declared.

### 22.3 Ternary-state distance

A ternary-state distance may count differing local states:

`d_T(σ¹, σ²) = number of indices i for which σ_i¹ ≠ σ_i²`

Alternative weighted distances may be used when defined explicitly.

### 22.4 Graph-state distance

A graph-state distance may compare:

- edge sets;
- node sets;
- edge weights;
- topology classes;
- spectral descriptors.

The graph metric must remain distinct from geometric distance.

### 22.5 Composite distance

A composite state distance may be written as:

`d_S = w_X d_X + w_T d_T + w_G d_G + w_H d_H + w_F d_F`

where each weight `w_*` has declared provenance and normalization.

A weighted sum is not universal.

It is a model-specific construction.

### 22.6 Dimensional consistency

Quantities with incompatible physical units must not be added directly.

Normalization or nondimensionalization must be defined before constructing a composite metric.

## 23. State-Space Topology

### 23.1 Topological structure

A state space may require a topological structure to define:

- continuity;
- neighborhoods;
- convergence;
- connected regions;
- boundaries;
- trajectories.

### 23.2 Continuous and discrete product topology

A composite state space containing continuous and discrete factors has mixed topology.

A change in a discrete ternary component may be discontinuous even when continuous variables evolve continuously.

### 23.3 Connected components

An admissible state space may contain several disconnected regions.

Transitions between disconnected regions require:

- a discrete event;
- a structural transition;
- a topology change;
- an extension of the active state space.

### 23.4 Boundary states

A boundary state belongs to the closure of an admissible region and may require special transition rules.

Examples include:

- saturation boundary;
- resonance-window boundary;
- topology-change boundary;
- structural-form boundary;
- numerical stability boundary.

## 24. State Trajectories

### 24.1 Continuous trajectory

A continuous trajectory is a mapping:

`γ_X: I_t → X`

where `I_t` is the declared time interval.

### 24.2 Discrete trajectory

A discrete trajectory is a sequence:

`{S_n} for n ∈ ℕ`

### 24.3 Hybrid trajectory

A hybrid trajectory contains continuous evolution and discrete state events.

It may be represented as:

`γ_H = {(S(t), e_k)}`

where `e_k` is the event occurring at event time `t_k`.

### 24.4 Trajectory admissibility

A trajectory is admissible when:

- every state belongs to `S_adm`;
- every transition is permitted;
- every event order is valid;
- every invariant is preserved or explicitly reports failure;
- every boundary crossing follows its declared rule.

### 24.5 Trajectory segment

A finite trajectory segment is:

`γ[t_a, t_b]`

It contains the state evolution between times `t_a` and `t_b`.

A structural transition analysis must identify the relevant trajectory segment.

## 25. Evolution Maps

### 25.1 Continuous evolution

A continuous evolution map may be written as:

`Φ_t: S_adm → S`

The map must identify whether it forms:

- a flow;
- a semiflow;
- a non-autonomous evolution family;
- a delayed evolution operator;
- a stochastic evolution rule.

No stronger structure may be claimed without establishing its conditions.

### 25.2 Discrete update

A discrete update map is:

`U: S_n → S_n+1`

The map must define:

- evaluation inputs;
- update order;
- transition guards;
- retained state;
- failure behavior;
- output state.

### 25.3 Event map

An event map is:

`E_k: S_before → S_after`

An event map may represent:

- ternary transition;
- topology change;
- boundary change;
- structural transition;
- mode activation;
- failure;
- recovery.

### 25.4 Hybrid evolution

A hybrid evolution alternates continuous propagation and discrete event maps.

A generic sequence is:

`S_n`

`→ continuous evolution`

`→ event detection`

`→ guard evaluation`

`→ event map`

`→ invariant evaluation`

`→ S_n+1`

## 26. Continuous–Ternary Product State

### 26.1 Combined state

The coupled continuous and ternary state space is:

`S_XT = X × Σ_T`

A coupled state is:

`S_XT(t) = (X(t), σ(t))`

### 26.2 Continuous-to-ternary projection

The projection is:

`Π: X → Σ_T`

The projection must define an active-neutral region.

The projection must not generate a direct opposite-state transition.

### 26.3 Ternary-conditioned continuous update

The update is:

`Γ: X × Σ_T → X`

The effect of ternary state `0` must be explicit.

Possible effects may include:

- damping;
- holding;
- routing;
- balancing;
- reduced gain;
- transition preparation;
- conflict resolution.

### 26.4 Coupled consistency

A coupled state is consistent when:

- the continuous state supports the current ternary classification;
- the ternary state satisfies transition history;
- the projection rule is not violated;
- retained neutral state remains admissible;
- no hidden direct transition has occurred.

## 27. State Projection and Embedding

### 27.1 Projection

A projection reduces state information:

`P_red: S → S_red`

The projection must define which information is:

- retained;
- aggregated;
- discarded;
- approximated.

### 27.2 Embedding

An embedding maps a reduced state into a larger state space:

`E_full: S_red → S`

The embedding must define all added components.

Unknown components must not be assigned arbitrary values without provenance.

### 27.3 Projection–embedding consistency

A projection and embedding may satisfy:

`P_red(E_full(S_red)) = S_red`

This relation does not imply:

`E_full(P_red(S)) = S`

because projection may discard information.

### 27.4 Coarse-graining

A coarse-graining map reduces microscopic state information into a lower-dimensional representation.

A coarse-grained state must identify:

- source scale;
- target scale;
- aggregation rule;
- lost variables;
- retained invariants;
- uncertainty.

## 28. Multiscale State Spaces

### 28.1 Scale-indexed spaces

A state space at scale `s` is denoted by:

`S_s`

The complete multiscale state may be represented as:

`S_multi = ∏ S_s`

over the declared scale index set.

### 28.2 Cross-scale mapping

A cross-scale mapping is:

`M_s→r: S_s → S_r`

where `s` and `r` are distinct scales.

The mapping must define:

- source variables;
- target variables;
- averaging or reconstruction rule;
- retained quantities;
- lost information;
- validity region.

### 28.3 Upward mapping

An upward mapping constructs a coarser representation from a finer-scale state.

### 28.4 Downward mapping

A downward mapping applies coarse-scale information, constraints, or fields to a finer-scale state.

A downward mapping does not reconstruct missing microscopic detail unless a reconstruction rule is defined.

### 28.5 Cross-scale consistency

Two scale representations are consistent when their mapped quantities satisfy the declared compatibility conditions.

Cross-scale consistency must not be inferred from qualitative resemblance alone.

## 29. Symmetry Actions on State Spaces

### 29.1 State-space action

For transformation `g ∈ G_sym`, the action on state space is:

`ρ_S(g): S → S`

### 29.2 Component actions

The complete state action may contain:

- position action;
- velocity action;
- force action;
- tensor action;
- graph action;
- identity permutation;
- ternary-state action;
- observable action.

Each component action must be declared separately.

### 29.3 State-space invariance

An admissible state space is invariant under a transformation when:

`ρ_S(g)(S_adm) ⊆ S_adm`

for every permitted transformation `g`.

### 29.4 Ternary transformation action

The default assumption is not that a geometric transformation changes ternary state values.

A ternary transformation action must be introduced explicitly when required.

### 29.5 Quotient state space

When states related by a declared symmetry are treated as equivalent, a quotient state space may be formed.

The equivalence relation must be defined before quotient construction.

## 30. Resonance-Window State Regions

### 30.1 Resonance parameter space

A resonance analysis uses a declared parameter or state space:

`P_R`

### 30.2 Resonance-window region

A resonance window is:

`W_R ⊂ P_R`

The coordinates of `P_R` may include:

- frequency ratios;
- phase differences;
- amplitudes;
- coupling strengths;
- delay values;
- dissipation values;
- geometric parameters;
- mode populations;
- structural variables.

### 30.3 Entry and exit states

A resonance-window entry state belongs to:

`∂W_R`

and satisfies the declared entry direction and guard.

An exit state may satisfy a different condition.

Entry and exit criteria must not be assumed symmetric.

### 30.4 Resonance regime state

A resonance regime state is a complete model state whose projection into `P_R` belongs to `W_R`.

The projection must be declared.

### 30.5 Resonance and structural state

A state may belong to a resonance window without undergoing a structural transition.

A structural transition requires its own state-space conditions.

## 31. Structural-Transition State Paths

### 31.1 Pre-transition region

The pre-transition state region is:

`R_pre ⊆ S_adm`

### 31.2 Transition region

The transition region is:

`R_tr ⊆ S`

It may contain:

- temporary instability;
- neutral ternary staging;
- topology modification;
- mode competition;
- energy redistribution;
- symmetry reduction;
- delayed stabilization.

### 31.3 Post-transition region

The post-transition region is:

`R_post ⊆ S_adm`

### 31.4 Completed transition

A structural transition is completed when:

- the trajectory leaves `R_pre`;
- it passes through an admissible transition path;
- it enters `R_post`;
- post-transition invariants hold;
- the stabilization condition is satisfied.

### 31.5 Failed transition

A failed transition occurs when:

- a guard fails;
- no admissible path exists;
- an invariant fails;
- the system returns to `R_pre`;
- the execution enters an explicit failure state.

## 32. Recursive Inheritance State Space

### 32.1 Inheritance space

The inherited-state space is denoted by:

`X_I`

An inherited state is:

`I_n→n+1 ∈ X_I`

### 32.2 Inheritance mapping

The inheritance mapping is:

`Λ_I: S_n,final → I_n→n+1`

The next-cycle initialization map is:

`J_I: I_n→n+1 × B_n+1 → S_n+1,initial`

where `B_n+1` contains declared new boundary or input conditions.

### 32.3 Inherited components

Inherited state may contain:

- topology;
- defects;
- residual stress;
- phase organization;
- mode occupation;
- local-environment statistics;
- ternary retention;
- coupling weights;
- hysteretic variables;
- accumulated structural descriptors.

### 32.4 Inheritance loss

An inheritance projection may discard part of the previous state.

The discarded information must be identified.

Lossy inheritance must not be presented as complete state transfer.

## 33. Initial State Space

### 33.1 Initial-state set

The permitted initial states form:

`S₀ ⊆ S_adm`

### 33.2 Initial-state requirements

An initial state must define:

- continuous variables;
- ternary variables;
- topology;
- history where required;
- boundary state;
- parameter vector;
- numerical state;
- validation state.

### 33.3 Initial history

For delayed models, a single state at `t₀` may be insufficient.

The model must provide a history function or history record over the required interval.

### 33.4 Initialization provenance

Every initialized value must have provenance.

Possible classes include:

- measured;
- derived;
- calibrated;
- source-defined;
- author-defined;
- benchmark;
- test fixture.

## 34. Terminal and Absorbing States

### 34.1 Terminal state

A terminal state ends the declared execution.

Possible terminal causes include:

- completed simulation interval;
- completed structural transition;
- explicit stop condition;
- invariant failure;
- unsupported state;
- unrecoverable numerical failure.

### 34.2 Absorbing state

An absorbing state maps to itself under the declared evolution:

`U(S_abs) = S_abs`

An absorbing state must be identified as:

- physical;
- logical;
- numerical;
- validation-related.

### 34.3 Failure absorption

A failure state may be absorbing when execution is prohibited from continuing.

The trace must preserve the original failure cause.

## 35. State Equivalence

### 35.1 Exact state equality

Two states are exactly equal when every declared state component is equal under its exact comparison rule.

### 35.2 Numerical state equivalence

Two numerical states may be equivalent within a declared tolerance.

The tolerance must specify:

- compared variables;
- norm;
- absolute tolerance;
- relative tolerance;
- precision mode.

### 35.3 Structural equivalence

Two states are structurally equivalent when they satisfy the same declared structural relations and invariants.

Structural equivalence does not require coordinate equality.

### 35.4 Observable equivalence

Two states are observably equivalent when:

`O(S₁) = O(S₂)`

Observable equivalence does not imply structural or exact state equivalence.

### 35.5 Symmetry equivalence

Two states are symmetry-equivalent when one is obtained from the other by a permitted transformation.

The transformation must belong to the declared symmetry action.

## 36. State Identifiability

### 36.1 Full identifiability

A state is fully identifiable from observables when the observable mapping uniquely determines the state over the declared domain.

### 36.2 Partial identifiability

A state is partially identifiable when observables determine only a subset or equivalence class of internal states.

### 36.3 Non-identifiability

Non-identifiability occurs when distinct admissible states produce the same observable output.

The model must not claim unique internal-state reconstruction under non-identifiability.

### 36.4 History-sensitive identifiability

A current observable may be insufficient to determine the memory state.

History-sensitive models must include the required prior information in reconstruction procedures.

## 37. State Uncertainty

### 37.1 Uncertain state

An uncertain state is represented by a region, distribution, interval, or set of possible states rather than one exact state.

### 37.2 State uncertainty set

An uncertainty set is:

`U_S ⊆ S`

### 37.3 Ternary uncertainty

Uncertainty must not be encoded automatically as ternary state `0`.

The active neutral state has operational semantics and is not a missing-information marker.

### 37.4 Uncertainty propagation

An uncertainty propagation rule must define how `U_S` evolves under the model.

### 37.5 Measurement uncertainty

Measurement uncertainty belongs to the observable layer unless explicitly mapped into the internal state.

## 38. State Serialization

### 38.1 Serialized state

A serialized state is a machine-readable representation of selected state components.

### 38.2 Required metadata

A serialized state must identify:

- schema version;
- model version;
- software version;
- time or execution step;
- state-space type;
- component dimensions;
- units;
- precision;
- provenance;
- validity status.

### 38.3 Missing values

Missing values must use an explicit missing-value representation.

They must not be encoded as:

- ternary `0`;
- numeric `0`;
- empty string;
- valid physical value;

unless the schema defines that exact meaning.

### 38.4 State compatibility

Two serialized states are compatible only when their:

- schema versions;
- state-space definitions;
- dimensions;
- units;
- indexing conventions;
- precision rules;

satisfy an explicit compatibility contract.

## 39. State-Space Versioning

### 39.1 Semantic change

A state-space definition changes semantically when any of the following changes:

- state variable meaning;
- domain;
- codomain;
- dimension;
- units;
- admissible range;
- transition semantics;
- topology representation;
- missing-value semantics;
- serialization field meaning.

### 39.2 Version impact

A semantic state-space change must identify:

- affected files;
- affected equations;
- affected code;
- affected schemas;
- affected tests;
- affected traces;
- affected validation results.

### 39.3 Backward compatibility

Backward compatibility must not be claimed solely because a parser accepts an older file.

Semantic compatibility requires preservation or explicit translation of state meaning.

## 40. State-Space Invariants

The following invariants apply to TR-EIF state spaces.

1. Every state component belongs to a declared domain.

2. Continuous and ternary state components remain separately typed.

3. The balanced ternary domain is exactly `{-1, 0, 1}`.

4. The canonical ternary notation is `-1/0/1`.

5. The state `0` remains active.

6. Direct `-1 → 1` transitions are forbidden.

7. Direct `1 → -1` transitions are forbidden.

8. Opposite-state transitions pass through `0`.

9. Missing or invalid data are not encoded silently as `0`.

10. Every dynamic dependency is represented in the state or explicit execution context.

11. Every topology change is represented explicitly.

12. Every delayed dependency has an associated history representation.

13. Every observable is derived through a declared mapping.

14. Equality of observables does not imply equality of complete states unless proven.

15. Numerical state and physical state remain distinct.

16. Physical failure and numerical failure remain distinguishable.

17. Every admissibility condition is explicit.

18. Every invalid state remains visible.

19. Every projection identifies discarded information.

20. Every state-space extension identifies its semantic and version impact.

## 41. State-Space Conformance Requirements

A TR-EIF model conforms to this state-space architecture when:

- all required state spaces are declared;
- all state variables are typed;
- all domains and codomains are specified;
- all admissibility conditions are explicit;
- continuous and ternary layers remain separate;
- state dependencies are complete;
- topology and history are represented when required;
- observable mappings are declared;
- invalid states remain visible.

A TR-EIF implementation conforms when:

- the implemented state structure matches the approved mathematical structure;
- no hidden mutable state affects execution;
- no state component changes meaning during execution;
- no direct opposite ternary transition is produced;
- serialization preserves declared semantics;
- deterministic replay preserves required execution state.

## 42. State-Space Dependency Structure

The state-space dependency order is:

`system boundary`

`→ configuration space`

`→ continuous dynamic space`

`→ oscillatory space`

`→ balanced ternary space`

`→ interaction and topology spaces`

`→ history and memory space`

`→ structural space`

`→ parameter and boundary spaces`

`→ numerical execution space`

`→ validation space`

`→ composite admissible state space`

`→ evolution maps`

`→ observable output space`

`→ deterministic trace`

A later component may depend on an earlier component only through a declared mapping.

## 43. Final State-Space Statement

TR-EIF represents a complete model state as an explicitly typed composition of continuous, balanced ternary `-1/0/1`, topological, interaction, historical, structural, boundary, numerical, and validation components.

The state `0` remains an active element of the ternary state space.

Continuous quantities are not silently collapsed into ternary states.

Topological change, delayed dependence, structural transition, uncertainty, numerical execution, and observable projection remain explicit state-space operations.

Every admissible trajectory is therefore defined by:

`declared initial state`

`→ declared state space`

`→ explicit evolution maps`

`→ admissible transitions`

`→ invariant evaluation`

`→ observable projection`

`→ traceable final state`
