# Mathematical Foundations

## 1. Purpose

This chapter establishes the foundational mathematical language of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

TR-EIF is organized as an integrated mathematical and computational architecture with two principal formal components:

- **TR — Ternary Resonant**
- **EIF — Equivariant Interatomic Framework**

These components are developed as separately typed mathematical layers and are connected only through explicitly defined mappings.

The foundational construction follows the dependency order:

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

This order is structural. A model equation is meaningful only after the mathematical objects on which it operates have been defined.

---

## 2. Foundational Scope

The mathematical foundation supports systems containing combinations of:

- continuous state;
- discrete state;
- circular state;
- graph state;
- geometric state;
- ternary state;
- resonance state;
- memory;
- history;
- delay;
- nonlinear dynamics;
- dissipative dynamics;
- coupled dynamics;
- propagation;
- saturation;
- multiscale organization;
- symmetry actions;
- invariant representations;
- equivariant representations;
- interatomic mappings.

No single state space is assumed to represent all components of a TR-EIF system.

---

## 3. System Definition

A TR-EIF system is represented abstractly by:

`S = (B, X, U, P, F, O, I)`

where:

- `B` is the system-boundary specification;
- `X` is the system state space;
- `U` is the admissible input space;
- `P` is the parameter space;
- `F` is the state-evolution structure;
- `O` is the observable structure;
- `I` is the invariant set or invariant predicate family.

The tuple defines the mathematical system class.

Specific TR-EIF models may introduce additional components when required by their state structure.

---

## 4. System Boundary

The system boundary:

`B`

defines what belongs to the modeled system and what enters through external interfaces.

A boundary specification may identify:

- modeled entities;
- spatial domain;
- temporal domain;
- external inputs;
- external fields;
- environmental variables;
- boundary conditions;
- exchanged quantities;
- excluded degrees of freedom.

The boundary is defined before state variables are assigned.

This prevents external quantities from being silently treated as internal state.

---

## 5. State Space

Let:

`X`

denote the complete state space of a selected model.

A composite TR-EIF state space may be written as:

`X = X_1 × X_2 × ... × X_n`

where each factor represents a separately typed state component.

A state is:

`x ∈ X`.

The product representation does not imply that all factors have the same mathematical structure.

One factor may be Euclidean, another circular, another discrete, another graph-valued, and another history-dependent.

---

## 6. Continuous State

A continuous state component may belong to a space such as:

`X_c ⊆ R^n`

for a finite-dimensional model.

Examples include:

- positions;
- velocities;
- continuous resonance coordinates;
- continuous internal variables;
- thermodynamic variables where defined.

The dimension `n` is model-dependent.

---

## 7. Circular State

Oscillator phase belongs to a circular state space.

Define the phase space:

`S^1 = R / (2 pi Z)`.

A phase variable is:

`theta ∈ S^1`.

A numerical realization may use a representative interval such as:

`[0, 2 pi)`

but the mathematical phase remains an element of `S^1`.

Therefore two representatives differing by an integer multiple of `2 pi` represent the same phase.

---

## 8. Discrete State

A discrete state component belongs to a discrete set:

`X_d`.

Its elements must be defined by the selected model.

Discrete state must not be treated as a continuous coordinate unless an explicit embedding is defined.

---

## 9. Balanced Ternary State

The TR-EIF balanced ternary state space is:

`T = {-1, 0, 1}`.

The canonical kernel notation is:

`-1/0/1`.

The three values are distinct semantic states.

The state `0` is active.

Depending on the selected model, active `0` may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

The value `0` does not intrinsically denote:

- absence;
- missing data;
- invalid state;
- error;
- unavailable state;
- no signal.

---

## 10. Ternary Transition Graph

The fundamental committed transition relation is constrained by:

`-1 → 1` forbidden

`1 → -1` forbidden.

Opposite-polarity transitions require neutral mediation:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each arrow denotes a separate transition event.

The first leg does not automatically authorize the second leg.

The state `0` may persist for any number of admissible execution steps unless a selected model defines an additional transition condition.

---

## 11. Ternary Target and Executed State

A ternary target and an executed ternary state are distinct objects.

Let:

`t_target ∈ T`

denote a target produced by an upstream mapping.

Let:

`t_exec ∈ T`

denote the currently executed retained state.

In general:

`t_target ≠ t_exec`

may hold during an admissible execution interval.

A transition mechanism determines whether and when the executed state changes.

This distinction is required for neutral-mediated routing and stateful execution.

---

## 12. Pending Ternary Destination

A model supporting staged opposite-polarity transitions may contain a pending destination:

`t_pending ∈ T`

together with an explicit predicate indicating whether a pending destination is active.

For example, if:

`t_exec = -1`

and:

`t_target = 1`,

the first committed transition may produce:

`t_exec: -1 → 0`

while retaining:

`t_pending = 1`.

A later admissible event may then produce:

`t_exec: 0 → 1`.

The pending destination is state.

It is not equivalent to the currently executed state.

---

## 13. Resonance Coordinate Space

TR-EIF does not define resonance through frequency equality alone.

Let:

`X_R`

denote a resonance-coordinate space.

Let:

`X_src`

be the source space from which resonance coordinates are constructed.

Define a resonance-coordinate mapping:

`P_R: X_src → X_R`.

For:

`x ∈ X_src`,

the resonance state is:

`r = P_R(x)`

with:

`r ∈ X_R`.

The structure and dimensionality of `X_R` are model-dependent.

---

## 14. Resonance Window

A resonance window is a model-defined subset:

`W_R ⊂ X_R`.

Its boundary is:

`∂W_R`.

The minimal resonance classification set is:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

A classification mapping may be defined as:

`C_R: X_R → K_R`

subject to the selected boundary convention.

The classification domain `K_R` is distinct from the ternary domain `T`.

Therefore:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless a separate explicit mapping between `K_R` and `T` is defined.

---

## 15. Resonance Window Dependence

A resonance window may depend on additional model state.

A generalized window may be represented as:

`W_R(h, q, s) ⊂ X_R`

where, for example:

- `h` is history state;
- `q` is topology or configuration state;
- `s` is scale state.

This permits finite resonance windows that are:

- multidimensional;
- history-dependent;
- hysteretic;
- topology-dependent;
- scale-dependent.

The dependency variables must be explicitly typed in the selected model.

---

## 16. Resonance and Frequency

Frequency may be one coordinate or parameter in a resonance model.

Frequency equality alone does not define the general TR-EIF resonance state.

Accordingly:

`resonance ≠ frequency equality`.

A resonance mapping may incorporate frequency relations together with additional coordinates such as:

- phase relations;
- coupling structure;
- amplitude response;
- topology;
- memory;
- dissipation;
- scale-dependent descriptors.

The exact coordinate construction belongs to the selected resonance model.

---

## 17. Phase Organization

For a system of `N ≥ 1` oscillator phases:

`theta_1, ..., theta_N ∈ S^1`,

the classical complex phase-order parameter is:

`Z = (1/N) sum_j exp(i theta_j)`.

Its magnitude is:

`R = |Z|`.

Equivalently:

`R = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

The quantity `R` measures phase organization under this definition.

It is not automatically a complete measure of structural coherence.

---

## 18. Phase Order and Coherence

TR-EIF distinguishes phase order from broader coherence observables.

If:

`R(t)`

denotes a phase-order observable and:

`C(t)`

denotes a separately defined coherence observable, then:

`R(t) ≠ C(t)`

unless a specific model explicitly defines equality.

Likewise:

`coherence ≠ uniformity`

and:

`coherence ≠ resonance`.

---

## 19. Synchronization and Phase Locking

Synchronization, phase locking, and resonance are separately defined concepts.

Phase locking concerns bounded or constant phase relations under a selected definition.

Synchronization may refer to coordinated dynamical behavior under an explicitly selected synchronization criterion.

Resonance concerns response or organization relative to a resonance model and its resonance coordinates.

Therefore:

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`resonance ≠ synchronization`.

---

## 20. State and Observable

A state variable participates in the information required to determine admissible future evolution under the selected model.

An observable is obtained from state through an observation mapping.

Let:

`X`

be a state space and:

`Y`

an observable space.

Define:

`O: X → Y`.

For:

`x ∈ X`,

the observable is:

`y = O(x)`.

An observable is not automatically part of retained state.

A retained state variable is not automatically an externally reported observable.

---

## 21. Local and Global State

Let a system contain indexed local states:

`x_i ∈ X_i`

for:

`i = 1, ..., N`.

The global state may be represented as:

`x = (x_1, ..., x_N) ∈ X_1 × ... × X_N`.

A local observable:

`O_i(x_i)`

and a global observable:

`O_G(x)`

are distinct mappings.

A global quantity must not be substituted for a local state without an explicit mapping.

---

## 22. Multiscale State

Let:

`L = {l_1, l_2, ..., l_m}`

be a finite set of modeled scales.

Each scale `l_k` has a state space:

`X^(l_k)`.

A cross-scale mapping is typed as:

`M_(a→b): X^(l_a) → X^(l_b)`.

The mapping must specify which information is:

- preserved;
- aggregated;
- projected;
- approximated;
- discarded.

Scale transfer is therefore an explicit mathematical transformation.

---

## 23. Atomic Configuration Space

For a system containing `N` atomic entities, an elementary configuration may contain:

- species labels;
- positions;
- simulation-cell information;
- boundary information.

Let:

`A`

denote the species-label space.

For nonperiodic Cartesian coordinates, positions may be represented by:

`R_pos ∈ R^(3N)`.

A basic labeled configuration space may therefore contain elements of:

`A^N × R^(3N)`.

Periodic systems require an additional cell and periodic-identification structure.

---

## 24. Interatomic State

An interatomic state may extend the configuration with quantities such as:

- velocities;
- momenta;
- interaction topology;
- local environments;
- internal features;
- model memory.

The exact interatomic state space is defined by the selected EIF model.

An oscillator phase is not automatically assigned to an atom.

Any mapping from atomic or interatomic state to oscillator or resonance state must be explicitly defined.

---

## 25. Interaction Graph

An interaction graph may be represented as:

`G = (V, E)`,

where:

- `V` is the entity set;
- `E` is the interaction-edge set.

Graph construction may depend on:

- geometry;
- cutoff rules;
- periodic images;
- species;
- topology;
- model-defined interaction criteria.

The graph is a mathematical representation of interaction structure.

---

## 26. Local Environment

For entity `i`, let:

`N_i`

denote a model-defined neighborhood.

A local environment:

`E_i`

may contain the information selected from `N_i` and the global configuration.

A local-environment mapping may be written:

`L_i: X_atomic → X_env,i`.

The mapping must preserve the transformation properties required by the selected EIF representation.

---

## 27. Transformation Group

Let:

`G_sym`

denote a transformation group acting on an input space `X`.

Let:

`rho_X(g): X → X`

denote the action of:

`g ∈ G_sym`

on `X`.

If an output space `Y` carries an action:

`rho_Y(g): Y → Y`,

then transformation behavior of mappings between `X` and `Y` can be defined precisely.

---

## 28. Invariant Mapping

A mapping:

`F: X → Y`

is invariant under `G_sym` when:

`F(rho_X(g)x) = F(x)`

for every admissible:

`g ∈ G_sym`

and:

`x ∈ X`.

The output does not transform under the selected action.

---

## 29. Equivariant Mapping

A mapping:

`F: X → Y`

is equivariant under `G_sym` when:

`F(rho_X(g)x) = rho_Y(g)F(x)`

for every admissible:

`g ∈ G_sym`

and:

`x ∈ X`.

Equivariance is therefore defined by:

- a group;
- an input action;
- an output action;
- a domain;
- a codomain;
- a transformation relation.

---

## 30. Permutation Behavior

Let:

`S_N`

denote the permutation group on `N` indexed entities.

Permutation invariance and permutation equivariance are distinct.

A scalar global property may be permutation invariant.

An indexed per-entity output may be permutation equivariant.

The selected transformation relation must match the mathematical type of the output.

---

## 31. Translation Behavior

For a translation vector:

`a ∈ R^3`,

a Cartesian position transforms as:

`r_i → r_i + a`.

A translation-invariant quantity remains unchanged under this action.

A translation-equivariant quantity transforms according to its declared output action.

Translation behavior is distinct from permutation behavior.

---

## 32. Rotation Behavior

For a rotation:

`Q ∈ SO(3)`,

a Cartesian vector transforms as:

`v → Qv`.

A scalar invariant under rotation remains unchanged.

A vector-valued equivariant output transforms according to the corresponding rotation action.

Rotation behavior is distinct from translation and permutation behavior.

---

## 33. E(3) Transformation Structure

The Euclidean group `E(3)` combines orthogonal transformations and translations in three-dimensional Euclidean space.

A selected EIF model must state whether its transformation contract uses:

- `SO(3)`;
- `O(3)`;
- `SE(3)`;
- `E(3)`;
- or another explicitly defined transformation set.

The transformation group must not be inferred from the word "equivariant" alone.

---

## 34. Geometry and Ternary State

A geometric transformation does not intrinsically change ternary polarity.

Rotation, translation, reflection, or permutation must not produce:

`-1 ↔ 1`

unless an explicitly defined model mapping requires such behavior.

Geometry and ternary semantics occupy distinct mathematical layers.

---

## 35. Interatomic to Equivariant Mapping

Let:

`X_A`

denote an atomic or interatomic state space.

Let:

`X_E`

denote an equivariant representation space.

Define:

`P_E: X_A → X_E`.

The mapping must specify:

- source state;
- target representation;
- transformation group;
- input action;
- output action;
- locality;
- retained information;
- discarded information.

---

## 36. Equivariant to Resonance Mapping

Let:

`X_E`

be an equivariant representation space and:

`X_R`

a resonance-coordinate space.

Define:

`P_ER: X_E → X_R`.

This mapping establishes the formal interface between EIF representation and TR resonance representation.

Its transformation behavior must be defined by the selected integrated model.

---

## 37. Resonance to Ternary Mapping

Let:

`X_R`

be the resonance-coordinate space.

A ternary-target mapping is:

`P_RT: X_R → T`.

More generally, if history or auxiliary state is required:

`P_RT: X_R × X_H → T`

where:

`X_H`

is the required history or auxiliary state space.

The mapping produces a ternary target.

It does not itself imply immediate execution of that target.

---

## 38. Ternary Feedback Mapping

Where ternary state influences an interatomic representation, define an explicit feedback mapping.

For example:

`P_TE: T × X_E → X_E'`

or another model-specific typed mapping.

The source space, target space, transformation behavior, locality, and physical interpretation must be specified.

This closes an integrated path of the form:

`interatomic state`

`→ equivariant representation`

`→ resonance state`

`→ ternary target`

`→ ternary execution`

`→ interatomic representation update`.

---

## 39. Continuous and Discrete Coupling

Let:

`x_c ∈ X_c`

be continuous state and:

`t ∈ T`

be ternary state.

A coupled system may be represented through mappings:

`F_c: X_c × T × P → X_c`

and:

`F_t: X_c × T × P → T_target`

for a discrete-time realization.

Here:

`T_target = T`

as a value set, while its semantic role remains that of a target.

Execution of the target is governed by a separate transition relation.

This preserves the distinction between continuous evolution, classification, and committed discrete state.

---

## 40. Continuous-Time Evolution

A continuous-time subsystem may be represented by:

`dx/dt = f(x, u, p, t)`

with:

`x ∈ X_c`

`u ∈ U`

`p ∈ P`.

The vector field:

`f`

must map admissible state, input, parameter, and time values to the tangent structure appropriate to `X_c`.

For Euclidean state:

`f: X_c × U × P × R → R^n`.

---

## 41. Discrete-Time Evolution

A discrete-time subsystem may be represented by:

`x_(k+1) = F(x_k, u_k, p)`.

The update map is:

`F: X × U × P → X`.

The index `k` denotes an execution step, not automatically physical time.

A physical-time interpretation requires an explicit time mapping.

---

## 42. Hybrid Evolution

TR-EIF may contain coupled continuous and discrete evolution.

A hybrid state may be written:

`z = (x_c, x_d) ∈ X_c × X_d`.

Its evolution may combine:

- continuous flow;
- discrete events;
- state-dependent transitions;
- scheduled transitions;
- retained memory.

The transition semantics must identify which state components are updated by each operation.

---

## 43. Memory State

A variable that influences future evolution and cannot be reconstructed from the instantaneous Markov state chosen for the remaining variables must be included in the complete state.

Let:

`m ∈ X_M`

denote memory state.

The complete state may then be:

`x = (x_base, m)`.

Memory is not an informal annotation; it is part of the dynamical state.

---

## 44. History State

For a history-dependent system, let:

`H_t`

denote the history required at time `t`.

A state evolution law may be written:

`dx/dt = f(x(t), H_t, u(t), p)`.

The history domain must be defined by the selected model.

History dependence must not be hidden inside an apparently memoryless mapping.

---

## 45. Delay

A delayed interaction may depend on a previous state such as:

`x_j(t - tau_ij)`

where:

`tau_ij ≥ 0`

is a defined delay.

A delay requires access to past state.

It is distinct from a phase-lag parameter appearing directly inside an interaction function.

Therefore:

`delay ≠ phase lag`.

---

## 46. Dissipation

A dissipative term represents model-defined loss, relaxation, contraction, or irreversible transfer.

Its mathematical form and dimensional units must be defined within the selected model.

Dissipation is not inferred solely from decreasing values of an arbitrary observable.

---

## 47. Saturation

A saturation operator limits a variable or response according to a declared rule.

For scalar bounds:

`a ≤ b`,

a clipping operator may be defined as:

`clip(x; a, b) = min(max(x, a), b)`.

A numerical saturation operator and a physical saturation mechanism are distinct unless the model explicitly identifies them.

---

## 48. Nonlinearity

TR-EIF permits nonlinear mappings and nonlinear evolution laws.

A linear approximation may be used locally when its expansion point, retained terms, and domain of applicability are defined.

A local linear approximation does not replace the nonlinear model outside its stated domain.

---

## 49. Coupling

For indexed subsystems, coupling represents dependence of one subsystem's evolution on states or observables of others.

A general coupling term for subsystem `i` may be written:

`K_i(x_1, ..., x_N, p)`.

The exact coupling structure may depend on:

- graph topology;
- distance;
- phase;
- species;
- scale;
- memory;
- model parameters.

A coupling term must not be assigned a physical interpretation not defined by the model.

---

## 50. Kuramoto-Type Phase Module

For a phase-oscillator subsystem, a classical Kuramoto-type model may take the form:

`d theta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i)`.

A Sakaguchi-type phase-lag extension may take the form:

`d theta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i - gamma)`.

TR-EIF may use such phase dynamics as one module within a larger resonance architecture.

The phase module does not define the complete TR-EIF state.

---

## 51. Phase and Physical State

Oscillator phase is a mathematical circular coordinate.

It is distinct from a thermodynamic phase of matter.

Therefore:

`oscillator phase ≠ physical phase of matter`.

Likewise, a phase relation does not intrinsically define a chemical bond, and phase coupling does not intrinsically define a mechanical force.

---

## 52. Bifurcation

A bifurcation concerns a qualitative change in the mathematical structure of a dynamical system as a parameter varies.

Identification of a named bifurcation requires the mathematical conditions associated with that bifurcation class.

A threshold crossing alone does not establish a bifurcation.

Accordingly:

`resonance-window crossing ≠ bifurcation`.

---

## 53. Ternary Transition

A ternary transition is a change in the executed state belonging to:

`T = {-1, 0, 1}`.

It is governed by the ternary transition relation.

It is distinct from a dynamical-system bifurcation.

Therefore:

`bifurcation ≠ ternary transition`.

---

## 54. Structural Transition

A structural transition is a change in a separately defined structural state or structural observable.

It is not automatically identical to a ternary transition.

Therefore:

`ternary transition ≠ structural transition`.

---

## 55. Physical Phase Transition

A physical phase transition is defined through the physical model and corresponding thermodynamic or statistical-mechanical structure.

It is not identified solely from a structural or ternary state change.

Therefore:

`structural transition ≠ physical phase transition`.

---

## 56. Energy

Let:

`E: X_Energy → R`

denote a scalar energy functional over its declared domain.

The domain must specify the physical or model state from which energy is evaluated.

A ternary state is not itself an energy.

A resonance classification is not itself an energy.

Therefore:

`ternary state ≠ energy`

and:

`resonance classification ≠ energy`.

---

## 57. Conservative Force

Where a differentiable conservative energy functional:

`E(R_pos)`

is defined over Cartesian coordinates, the corresponding conservative force is:

`F = -grad_R E`.

For atom `i`:

`F_i = -partial E / partial r_i`.

The gradient relation applies to the selected differentiable energy model.

Other force components require their own definitions.

---

## 58. Stress

Stress is a tensorial quantity requiring a defined geometric and mechanical convention.

Its definition may depend on:

- simulation cell;
- volume;
- virial convention;
- kinetic contribution;
- interaction model;
- boundary conditions.

Stress must therefore be defined separately from scalar energy and vector force.

---

## 59. Dimensional Consistency

Every dimensional quantity belongs to a dimensional class.

Addition and subtraction require dimensional compatibility.

If:

`a`

and:

`b`

have incompatible physical dimensions, then:

`a + b`

is not an admissible physical expression unless an explicit transformation maps them to a common dimension.

Dimensionless quantities must be identified as such.

---

## 60. Parameters

Let:

`P`

denote a model parameter space.

A parameter:

`p ∈ P`

is distinct from dynamic state unless the model explicitly promotes it to an evolving state variable.

Implementation parameters must remain distinguishable from universal constants.

---

## 61. Calibrated Parameters

A parameter obtained from empirical or computational calibration carries provenance:

`CALIBRATED`.

Its admissible domain and calibration context must be recorded.

Calibration does not change the mathematical type of the parameter.

---

## 62. Author-Defined Structures

A mathematical structure introduced specifically by TR-EIF carries provenance:

`AUTHOR_DEFINED`

when appropriate.

Author-defined structures may include:

- mappings;
- state classifications;
- execution semantics;
- composite descriptors;
- integration contracts.

Their definitions must be explicit and internally consistent.

---

## 63. Derived Quantities

A quantity obtained mathematically from previously defined objects carries provenance:

`DERIVED`

when appropriate.

The derivation must preserve:

- mathematical typing;
- dimensions;
- domain restrictions;
- assumptions.

---

## 64. Primary Sources

A classical equation, definition, or physical relation taken from the scientific literature carries provenance:

`PRIMARY_SOURCE`

when supported by the corresponding source record.

The source layer is maintained separately from author-defined extensions.

---

## 65. Benchmark Results

A measured computational benchmark may carry provenance:

`BENCHMARK`.

Benchmark quantities must retain the implementation and measurement context required for interpretation.

---

## 66. Test Fixtures

Controlled validation inputs may carry provenance:

`TEST_FIXTURE`.

Fixtures define reproducible test conditions and expected structural properties.

---

## 67. Unresolved Source Requirement

A claim requiring an external scientific source that has not yet been attached to the claim carries:

`REQUIRES_SOURCE`.

This status is distinct from a mathematical state or ternary value.

---

## 68. Unresolved Test Requirement

A computational claim requiring an execution test that has not yet been completed carries:

`REQUIRES_TEST`.

This status is distinct from:

`0`

and from every other model state.

---

## 69. Provenance Set

The foundational provenance set is:

`P_prov = {PRIMARY_SOURCE, DERIVED, CALIBRATED, AUTHOR_DEFINED, BENCHMARK, TEST_FIXTURE, REQUIRES_SOURCE, REQUIRES_TEST}`.

Provenance identifies origin or evidentiary status.

It is not part of the balanced ternary state domain.

---

## 70. Mathematical Model

A mathematical model is a typed collection of:

- state spaces;
- parameter spaces;
- input spaces;
- mappings;
- evolution laws;
- constraints;
- invariants;
- observables.

The model is defined independently of a particular programming language or hardware backend.

---

## 71. Numerical Realization

A numerical realization maps a mathematical model into finite computational operations.

It may specify:

- discretization;
- solver;
- time step;
- precision;
- tolerance;
- operation ordering;
- approximation;
- finite representation;
- stopping criteria.

The numerical realization and mathematical model are distinct layers.

---

## 72. Exact Equality and Numerical Comparison

Exact mathematical equality is written:

`a = b`.

A numerical comparison may instead use a declared tolerance relation.

For a metric:

`d`

and tolerance:

`epsilon ≥ 0`,

one may define numerical agreement by:

`d(a, b) ≤ epsilon`.

The tolerance belongs to the numerical comparison contract.

It does not redefine exact equality.

---

## 73. Numerical State

Finite-precision representation may introduce numerical state not present in the exact mathematical model.

Examples include:

- accumulated roundoff;
- solver state;
- adaptive-step state;
- cached neighbor data;
- numerical history buffers.

Such state must be included where it affects future computation.

---

## 74. Observable Trace

Let:

`X`

be the execution state space and:

`Y_trace`

a trace-record space.

A trace projection is:

`P_trace: X → Y_trace`.

For an execution sequence:

`x_0, x_1, ..., x_n`,

the corresponding trace is:

`P_trace(x_0), P_trace(x_1), ..., P_trace(x_n)`.

A trace is a projection of execution state.

It need not contain the complete state.

---

## 75. Validation Predicate

Let:

`X_val`

be the domain of a validation check.

A validation predicate is:

`V: X_val → {PASS, FAIL}`.

Where evidence may be incomplete, an extended validation result set may be defined:

`K_val = {PASS, FAIL, UNRESOLVED}`.

These validation values are not ternary states.

In particular:

`UNRESOLVED ≠ 0`.

---

## 76. Invariant

An invariant is a property preserved under a declared transformation or evolution relation.

For a state predicate:

`I: X → {true, false}`,

an execution invariant requires:

`I(x_k) = true`

for every admissible execution state in its declared scope.

Different invariants may apply to different state components.

---

## 77. Ternary Invariant

The ternary state-domain invariant is:

`t_exec ∈ {-1, 0, 1}`.

For neutral-mediated opposite transitions, the transition invariant excludes committed edges:

`(-1, 1)`

and:

`(1, -1)`.

These restrictions apply to the executed transition relation.

---

## 78. Symmetry Invariant

A symmetry invariant is defined relative to a specified transformation action.

It must identify:

- transformation group;
- input action;
- quantity being tested;
- expected transformation behavior.

The term "symmetry" alone is insufficient to define an invariant.

---

## 79. Conservation Law

A conservation law identifies a quantity preserved under the selected model dynamics and boundary conditions.

For quantity:

`Q: X → R`,

exact conservation may be expressed as:

`Q(x(t)) = Q(x(0))`

over the declared domain.

A numerical realization may instead evaluate conservation error under a separate numerical criterion.

---

## 80. Boundedness

A state or observable is bounded on a domain when it remains inside a defined bounded set over the specified evolution interval.

Boundedness must identify:

- quantity;
- domain;
- evolution interval;
- bound.

Boundedness is distinct from stability.

---

## 81. Stability

Stability is defined relative to:

- a state or invariant set;
- a metric or topology;
- perturbations;
- an evolution law.

No generic use of "stable" substitutes for a mathematical stability definition.

Specific stability classes are introduced only where their conditions are defined.

---

## 82. Locality

A mapping is local relative to a declared neighborhood relation when its output for an entity depends only on state contained within the specified neighborhood.

Locality depends on the selected topology or geometry.

It is not inferred solely from computational implementation.

---

## 83. Globality

A global mapping may depend on the complete modeled system state.

Global observables and local observables must remain separately typed.

---

## 84. Information Preservation

For a mapping:

`F: X → Y`,

information preservation depends on the properties of `F`.

If `F` is injective over the relevant domain, distinct source states remain distinguishable in the target representation.

If `F` is non-injective, multiple source states may map to the same target state.

Information loss must therefore be evaluated relative to the mapping and domain.

---

## 85. Composition of Mappings

For mappings:

`F: X → Y`

and:

`G: Y → Z`,

their composition is:

`G ∘ F: X → Z`

defined by:

`(G ∘ F)(x) = G(F(x))`.

Composition is valid only when the codomain of the first mapping is compatible with the domain of the second.

---

## 86. Integrated TR-EIF Mapping Chain

A principal integrated mapping chain may be represented as:

`X_A → X_E → X_R → T_target → T_exec`.

With feedback, the chain may extend to:

`X_A → X_E → X_R → T_target → T_exec → X_E'`.

Each arrow represents a separately defined mapping or execution relation.

No arrow is implied merely by adjacency of conceptual layers.

---

## 87. Learning Layer Interface

Let:

`Theta`

denote a trainable parameter space.

A parameterized model may be written:

`F_theta`

with:

`theta ∈ Theta`.

Training defines an optimization problem over `Theta` using explicitly defined data and objective functionals.

The learned parameter state is distinct from the physical or dynamical state evaluated by the model.

---

## 88. Loss Functional

A loss functional may be written:

`L: Theta → R`

for a fixed dataset and training configuration, or more generally over the relevant model, data, and parameter spaces.

Individual loss components must preserve dimensional and semantic consistency.

Weighted combinations require explicitly defined weights and normalization conventions.

---

## 89. Regularization

A regularization functional adds a declared structural constraint or preference to an optimization objective.

TR-EIF may define regularization associated with:

- ternary structure;
- resonance structure;
- equivariance;
- parameter magnitude;
- smoothness.

Regularization terms remain distinct from physical observables unless explicitly defined otherwise.

---

## 90. Molecular Dynamics Interface

A molecular-dynamics state may be represented abstractly as:

`X_MD = X_pos × X_mom × X_cell × X_model`

where:

- `X_pos` contains positions;
- `X_mom` contains momenta or equivalent velocity state;
- `X_cell` contains simulation-cell state;
- `X_model` contains additional model state.

TR-EIF resonance, ternary, routing, and memory state may be included in `X_model` when used by the selected realization.

---

## 91. Time Integration

A time integrator maps a numerical state at one integration coordinate to the next.

For fixed step:

`Delta t > 0`,

a discrete numerical update may be written:

`x_(n+1) = Phi_(Delta t)(x_n)`.

The map:

`Phi_(Delta t)`

is a numerical realization of the selected equations of motion.

It is distinct from the exact continuous flow unless explicitly equal for the selected system.

---

## 92. Thermodynamic Control State

Thermostat and barostat variables, when used, are part of the complete dynamical or extended-system state according to the selected method.

They must not be treated as external metadata when they influence future evolution.

---

## 93. Periodic Boundary Structure

A periodic system requires a defined simulation cell and equivalence under lattice translations.

Coordinate wrapping is a representation operation.

Physical displacement, wrapped coordinate, and image index must not be conflated.

---

## 94. Neighbor Structure

Neighbor lists are computational structures derived from configuration and cutoff rules.

A neighbor list may be cached state in a numerical realization.

Its update policy belongs to the computational contract.

The underlying interaction definition remains distinct from the cache used to evaluate it.

---

## 95. Multiscale Interface

For scales:

`a`

and:

`b`,

a multiscale transfer:

`M_(a→b): X_a → X_b`

must define:

- source representation;
- target representation;
- transferred observables;
- closure assumptions;
- uncertainty treatment;
- dimensional transformation.

Cross-scale mappings are explicit framework objects.

---

## 96. Uncertainty State

Where uncertainty is modeled explicitly, define an uncertainty representation space:

`X_U`.

An uncertainty mapping may take the form:

`U_map: X → X_U`.

Uncertainty representation is distinct from ternary state and resonance classification.

---

## 97. Domain Detection

A model-domain detector may be represented as:

`D: X → K_D`

where `K_D` is an explicitly defined domain-status set.

Domain status must not be encoded implicitly through balanced ternary values unless a model explicitly defines such a mapping.

---

## 98. Reference-System Specialization

A reference material system specializes the general TR-EIF architecture by defining:

- species;
- composition;
- configuration domain;
- reference data;
- interatomic model;
- thermodynamic state range;
- transport observables;
- resonance parameterization;
- ternary interpretation;
- validation conditions.

The reference-system layer uses the general mathematical contracts established by preceding volumes.

---

## 99. FLiBe Reference Domain

The repository defines a dedicated FLiBe reference-model volume.

Its mathematical state and physical quantities are introduced through explicit model definitions and source records.

The FLiBe specialization connects:

- interatomic representation;
- thermodynamic properties;
- transport properties;
- local structure;
- resonance descriptors;
- ternary state;
- multiscale coolant modeling.

---

## 100. FRP Executable Reference

The Fractal Resonance Processor (FRP) provides an executable specialization/reference for selected Ternary Resonant mechanisms.

The architectural relation is:

`TR-EIF formal theory → FRP executable specialization/reference`.

FRP implementation mechanisms may provide executable realizations of:

- balanced ternary state;
- active neutral state;
- neutral-mediated transitions;
- pending routing;
- scheduling;
- phase evolution;
- hierarchical phase organization;
- retained memory;
- phase-derived ternary targets.

Implementation-specific FRP parameters remain implementation parameters.

---

## 101. Formal and Executable Layers

The framework distinguishes:

`formal definition`

`→ computational specification`

`→ implementation`

`→ execution`

`→ observable artifact`

`→ validation`.

A formal relation may have multiple computational realizations.

A computational realization must preserve the formal invariants required by its declared conformance scope.

---

## 102. Traceability Chain

An important mathematical or computational claim is represented through:

`claim`

`→ definition or source`

`→ scope`

`→ mapping or calculation`

`→ implementation where applicable`

`→ observable or artifact`

`→ validation evidence`.

This traceability structure applies throughout the repository.

---

## 103. Fundamental Distinctions

The following distinctions are foundational:

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

`local state ≠ global observable`

`mathematical model ≠ numerical realization`.

---

## 104. Foundational Invariants

The following invariants apply throughout TR-EIF unless a more specific definition strengthens them without contradiction:

1. The balanced ternary kernel is exactly `-1/0/1`.

2. The ternary state set is exactly `T = {-1, 0, 1}`.

3. The state `0` is active.

4. Direct committed `-1 → 1` transitions are forbidden.

5. Direct committed `1 → -1` transitions are forbidden.

6. Opposite-polarity transitions require active-neutral mediation.

7. Each transition leg is a distinct event.

8. Completion of the first transition leg does not automatically authorize the second.

9. Neutral state may persist until a valid subsequent transition is authorized.

10. Ternary target and executed ternary state are distinct.

11. Resonance classification and ternary state are distinct.

12. Continuous and discrete state spaces remain separately typed.

13. Circular phase remains a circular variable.

14. State and observable remain distinct.

15. Local and global quantities remain separately typed.

16. History and memory are represented as state when they affect future evolution.

17. Delay and phase lag remain distinct.

18. Mathematical models and numerical realizations remain distinct.

19. Exact equality and numerical tolerance remain distinct.

20. Equivariance claims require explicit transformation actions.

21. Permutation, translation, and rotation behavior remain separately defined.

22. Geometry transformations do not automatically change ternary polarity.

23. Energy, force, stress, resonance state, and ternary state remain separately typed quantities.

24. Cross-scale transfer requires an explicit mapping.

25. Implementation-specific parameters do not become universal constants through reuse.

---

## 105. Foundation for Subsequent Chapters

This chapter establishes the system-level objects required by the remainder of Volume 01.

Subsequent mathematical development operates on the defined distinctions between:

- systems and boundaries;
- state spaces and observables;
- continuous and discrete states;
- circular and Euclidean variables;
- resonance and ternary states;
- local and global quantities;
- invariant and equivariant mappings;
- interatomic and resonance representations;
- exact and numerical relations;
- formal and executable structures.

The complete TR-EIF architecture is constructed by composing explicitly typed mathematical objects rather than collapsing distinct physical, dynamical, geometric, resonance, and ternary concepts into a single state description.
