# Continuous-Discrete Dynamics Contract

## 1. Scope

This document defines the repository-level continuous-discrete dynamics contract of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The contract specifies:

- continuous-state semantics;
- discrete-state semantics;
- balanced ternary execution state;
- composite hybrid state;
- model time;
- numerical step;
- execution coordinate;
- target-evaluation coordinate;
- continuous evolution;
- numerical integration;
- descriptor construction;
- resonance projection;
- ternary-target generation;
- target registration;
- discrete execution;
- active-neutral mediation;
- pending-route state;
- feedback;
- history and memory;
- operator ordering;
- multirate evolution;
- event semantics;
- state closure;
- deterministic execution;
- trace boundaries;
- molecular-dynamics boundaries;
- implementation correspondence.

This document defines architectural interfaces between continuous and discrete dynamics.

Detailed mathematical definitions remain in the numbered mathematical volumes.

Detailed balanced ternary state membership and committed transition semantics remain in their corresponding specifications.

---

## 2. Architectural Principle

TR-EIF contains continuous and discrete dynamical components.

These components may interact.

They remain separately typed.

The canonical architectural chain is:

`continuous state`

`→ descriptor`

`→ resonance representation`

`→ ternary target`

`→ execution control`

`→ ternary execution`

`→ retained ternary state`

`→ feedback`

`→ subsequent continuous state`

No arrow in this chain is implicit.

Every implemented arrow corresponds to a declared mapping, update operator, or execution relation.

---

## 3. Continuous State Space

The continuous state space is denoted:

`X_C`

A continuous state is:

`x_C ∈ X_C`

The exact structure of `X_C` is model-specific.

A continuous state may contain quantities such as:

- Cartesian positions;
- velocities;
- momenta;
- oscillator phases;
- oscillator frequencies;
- retained continuous variables;
- continuous feature channels;
- continuous resonance coordinates;
- physical state variables;
- continuously represented control variables.

Membership in `X_C` does not assign balanced ternary semantics.

---

## 4. Discrete State Space

A generic discrete state space is denoted:

`X_D`

A discrete state is:

`x_D ∈ X_D`

Discrete state may contain:

- retained ternary state;
- pending destination;
- scheduler state;
- route-control state;
- discrete counters;
- execution flags;
- discrete memory variables;
- other explicitly defined categorical or integer-valued execution state.

Discrete state is not treated as continuous unless an explicit embedding is defined.

---

## 5. Balanced Ternary Execution State

The balanced ternary state space is:

`T = {-1, 0, 1}`

The canonical compact notation is:

`-1/0/1`

The retained executed ternary state is:

`t_exec ∈ T`

The requested ternary target is:

`t_target ∈ T`

Their codomains are identical.

Their semantic roles are distinct.

Therefore:

`target ≠ executed retained state`

remains an architectural invariant.

---

## 6. Active Neutral State

The state:

`0`

is an active neutral ternary state.

It may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Active neutral state is part of the discrete execution layer.

It is not a missing continuous value.

It is not a numerical zero inserted because a continuous value is unavailable.

---

## 7. Opposite-State Execution Constraint

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

are excluded.

Opposite-polarity execution uses:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

Each leg is a separate committed discrete transition.

Continuous dynamics do not bypass this execution constraint.

---

## 8. Hybrid State Space

A coupled continuous-discrete model may define a hybrid state space:

`X_HYB`

A representative decomposition is:

`X_HYB = X_C × X_R × T_target × T_exec × X_pending × X_ctrl × X_M`

where:

- `X_C` is continuous state;
- `X_R` is resonance state;
- `T_target` is the ternary-target domain;
- `T_exec` is the retained ternary-state domain;
- `X_pending` is pending-route state;
- `X_ctrl` is execution-control state;
- `X_M` is retained memory state.

A concrete specialization may contain additional explicitly declared factors.

---

## 9. Hybrid State

A representative hybrid state is:

`x_HYB = (x_C, x_R, t_target, t_exec, x_pending, x_ctrl, x_M)`

Each component retains its own mathematical type.

The Cartesian product does not make the components semantically interchangeable.

---

## 10. Model Time

Continuous model time is denoted:

`t`

with:

`t ∈ I_t`

where:

`I_t ⊆ R`

is the declared temporal domain.

Model time may represent physical time when the selected model defines that interpretation.

Model time is not a ternary state.

Model time is not a numerical step index.

Model time is not an execution tact.

---

## 11. Numerical Step

The numerical integration index is:

`n ∈ N_0`

A numerical state may be written:

`x_num[n]`

A numerical step indexes numerical evolution.

It is not automatically identical to:

- one physical-time unit;
- one execution tact;
- one target-generation event;
- one committed ternary event;
- one scheduler cycle.

---

## 12. Execution Coordinate

The discrete execution coordinate is denoted:

`k ∈ N_0`

The retained ternary state may be written:

`t_exec[k]`

The execution coordinate orders execution events.

The execution coordinate is distinct from model time unless an explicit mapping relates them.

---

## 13. Target-Evaluation Coordinate

A target-evaluation coordinate may be denoted:

`m ∈ N_0`

A target sequence may be written:

`t_target[m]`

The target-evaluation coordinate is not required to coincide with:

`n`

or:

`k`

A specialization that uses one shared coordinate must define that identification explicitly.

---

## 14. Scheduler Coordinate

A scheduler state may be represented as:

`x_sched ∈ X_sched`

A scheduler phase or index may use its own discrete coordinate.

Scheduler state belongs to execution control.

It is not the continuous physical state.

It is not a ternary state unless separately mapped into `T`.

---

## 15. Multiple Coordinates

A numerical realization may simultaneously contain:

- model time `t`;
- numerical step `n`;
- target-evaluation index `m`;
- execution coordinate `k`;
- scheduler state or scheduler coordinate.

These quantities remain separately typed.

No coordinate is silently substituted for another.

---

## 16. Time Mapping

Where numerical step and model time are related by fixed timestep:

`t_n = t_0 + n Delta t`

with:

`Delta t > 0`

For variable-step integration:

`t_(n+1) = t_n + Delta t_n`

The timestep sequence becomes part of the numerical execution definition.

---

## 17. Continuous Evolution Law

A continuous model may be written:

`dx_C/dt = F_C(x_C, t_exec, x_M, u, p, t)`

where:

- `x_C` is continuous state;
- `t_exec` is retained ternary state when used by the continuous model;
- `x_M` is retained memory;
- `u` is external input;
- `p` is parameter state;
- `t` is model time.

The arguments actually used by a specialization must be declared.

---

## 18. Continuous Vector Field

The mapping:

`F_C`

defines a continuous vector field or another continuous evolution structure appropriate to the selected state space.

For Euclidean state:

`F_C: X_C × T × X_M × U × P × I_t → R^d`

may be used when the derivative space is `R^d`.

The exact domain and codomain are model-specific.

---

## 19. Exact Continuous Flow

Where an exact flow exists, it may be denoted:

`phi_Delta_t`

with:

`phi_Delta_t: X_C → X_C`

for the applicable fixed auxiliary state.

The exact flow and numerical integrator are separate objects.

---

## 20. Numerical Continuous Update

A numerical integrator is denoted:

`Phi_Delta_t`

A generic update is:

`x_C[n+1] = Phi_Delta_t(x_C[n], x_aux[n])`

where `x_aux[n]` contains all declared result-affecting auxiliary inputs.

The numerical operator approximates or realizes the declared continuous evolution.

It does not redefine the continuous state space.

---

## 21. Exact Flow and Numerical Integrator

The notation preserves:

`Phi_Delta_t ≠ phi_Delta_t`

unless exact equality has been established for the selected model and integrator.

Numerical approximation and continuous mathematical evolution remain separate artifact classes.

---

## 22. Continuous Integrator Scope

A continuous numerical integrator advances only the variables declared in its integration contract.

It must not silently modify:

- ternary target;
- retained ternary state;
- pending route;
- scheduler state;
- route-control state;
- unrelated provenance metadata;
- validation state.

Any such update requires an explicit coupled operator.

---

## 23. Descriptor State

A continuous descriptor space is denoted:

`X_DESC`

A descriptor is:

`d_C ∈ X_DESC`

A descriptor mapping is:

`P_DESC: X_C × X_aux → X_DESC`

The descriptor is derived from or associated with continuous state.

It remains distinct from the continuous source state.

---

## 24. Descriptor Update

At numerical coordinate `n`, a descriptor may be evaluated as:

`d_C[n] = P_DESC(x_C[n], x_aux[n])`

or after a continuous step:

`d_C[n+1] = P_DESC(x_C[n+1], x_aux[n+1])`

The selected evaluation order must be declared.

---

## 25. Resonance State

The resonance-coordinate space is:

`X_R`

A resonance state is:

`x_R ∈ X_R`

The resonance state is not a balanced ternary state.

The resonance state may be continuous or otherwise structured according to its formal definition.

---

## 26. Resonance Projection

A resonance projection may be defined as:

`P_R: X_SRC → X_R`

where `X_SRC` is the declared source domain.

For example:

`x_R = P_R(x_C, d_C, x_M)`

may be used when the specialized mapping requires these inputs.

---

## 27. Resonance State and Descriptor

Descriptor state and resonance state may coincide in a specialization only when explicitly defined as the same mathematical object.

In the general architecture:

`descriptor ≠ resonance state`

The mapping between them must be declared.

---

## 28. Resonance Classification

A resonance classifier may be written:

`C_R: X_R → K_R`

with:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`

The resonance classification remains distinct from balanced ternary state.

Therefore:

`K_R ≠ T`

---

## 29. Phase Order

A phase-order quantity such as:

`R`

is a continuous observable under its corresponding definition.

A phase-order value is not automatically:

- a resonance classification;
- a ternary target;
- a retained ternary state.

The relation:

`R(t) ≠ C(t)`

is preserved where `C(t)` denotes a separately defined coherence observable.

---

## 30. Continuous-to-Ternary Mapping

A continuous or resonance-derived target mapping may be written:

`P_CT: X_SRC → T`

For:

`x_src ∈ X_SRC`

the requested target is:

`t_target = P_CT(x_src)`

The source remains in its original state space.

The output belongs to:

`T`

---

## 31. Target Generation

Target generation is an upstream operation.

It computes or requests:

`t_target`

Target generation does not itself update:

`t_exec`

Therefore:

`target generation ≠ committed ternary execution`

---

## 32. Target Registration

A numerical realization may separate:

- target computation;
- target registration;
- target execution.

A registered target may be stored before it becomes eligible for execution.

This separation must remain explicit when present.

---

## 33. Threshold Mapping

A scalar target mapping may use thresholds.

For ordered thresholds:

`eta_negative < eta_positive`

the reference threshold semantics are:

`x < eta_negative → -1`

`eta_negative ≤ x ≤ eta_positive → 0`

`x > eta_positive → 1`

Threshold values are model parameters.

They are not members of the ternary state space solely because they affect ternary classification.

---

## 34. Threshold Crossing Boundary

A continuous source may cross one or more target-classification thresholds during continuous evolution.

This may change:

`t_target`

It does not directly commit:

`t_exec`

Therefore:

`threshold crossing ≠ committed ternary transition`

---

## 35. Resonance-Window Crossing Boundary

A resonance state may cross:

`∂W_R`

This is a resonance-coordinate event.

It does not by itself define:

- a bifurcation;
- a committed ternary transition;
- a structural transition;
- a physical phase transition.

The relations remain:

`resonance-window crossing ≠ bifurcation`

`resonance-window crossing ≠ committed ternary transition`

---

## 36. Bifurcation Boundary

A bifurcation is defined by the mathematical conditions of the selected dynamical system.

A change in ternary target is not by itself a bifurcation.

A committed ternary transition is not by itself a bifurcation.

Therefore:

`bifurcation ≠ ternary transition`

---

## 37. Discrete Execution Operator

A discrete ternary execution operator may be written:

`F_T`

A generic form is:

`x_T[k+1] = F_T(x_T[k], t_target[k], x_ctrl[k])`

where `x_T` contains the retained ternary execution state and any associated route state.

The exact domain is defined by the execution specialization.

---

## 38. Retained Ternary State

The retained ternary state changes only through the declared execution semantics.

A newly generated target does not overwrite retained state by assignment unless the resulting transition is valid and committed.

The invariant is:

`target ≠ executed retained state`

---

## 39. Committed Transition Relation

The canonical committed ternary relation is:

`R_T = {(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 0), (1, 1)}`

The direct opposite pairs:

`(-1, 1)`

and:

`(1, -1)`

are excluded.

Continuous-state evolution does not modify this relation.

---

## 40. Opposite Target Handling

A continuous-to-ternary mapping may request:

`t_target = 1`

while:

`t_exec = -1`

or request:

`t_target = -1`

while:

`t_exec = 1`

These are admissible target/execution configurations.

They do not permit a direct opposite committed transition.

---

## 41. Neutral-Mediated Execution

For:

`t_exec = -1`

and:

`t_target = 1`

the first state-changing committed execution leg is:

`-1 → 0`

For:

`t_exec = 1`

and:

`t_target = -1`

the first state-changing committed execution leg is:

`1 → 0`

The second leg is independently executed later when its execution conditions are satisfied.

---

## 42. Pending Route State

A pending route may be represented by:

`t_pending ∈ {NONE, -1, 1}`

The pending destination is discrete execution-control state.

It is distinct from:

- continuous state;
- descriptor state;
- resonance state;
- current target;
- retained ternary state.

---

## 43. Pending and Neutral Separation

The state:

`t_exec = 0`

may coexist with:

`t_pending = 1`

or:

`t_pending = -1`

The pending destination records an unresolved route destination.

It does not change the retained state from `0`.

Therefore:

`pending target ≠ active neutral state`

---

## 44. Execution Guard

A discrete execution guard may determine whether an otherwise valid transition leg is eligible to commit.

The guard may depend on:

- execution-control state;
- route state;
- scheduler state;
- capacity state;
- other explicitly declared variables.

A guard does not redefine the committed transition relation.

---

## 45. Hold Semantics

A blocked execution attempt may produce no committed transition route.

A hold condition is distinct from a committed self-transition.

Therefore:

`hold ≠ committed retention transition`

The continuous layer may continue evolving during a discrete hold if the coupled model defines that behavior.

---

## 46. Scheduler Boundary

A scheduler determines execution opportunities under its declared control semantics.

Scheduler decisions do not redefine:

- continuous state space;
- ternary state space;
- committed transition relation.

A scheduler may delay or block execution.

A scheduler cannot authorize a forbidden direct opposite committed transition.

---

## 47. Continuous Evolution during Discrete Hold

A coupled model may allow continuous evolution while discrete state is retained.

A generic interval may satisfy:

`t_exec[k+1] = t_exec[k]`

while:

`x_C[n+1] ≠ x_C[n]`

This is a valid continuous/discrete separation when declared by the model.

---

## 48. Discrete Transition with Fixed Continuous State

A discrete execution event may occur without simultaneously advancing continuous model time.

A generic event may satisfy:

`x_C^+ = x_C^-`

while:

`t_exec^+ ≠ t_exec^-`

when the event semantics treat the continuous state as fixed across the discrete event.

The selected event convention must be explicit.

---

## 49. Hybrid Event Form

A continuous-time hybrid realization may evolve according to:

`dx_C/dt = F_C(x_C, t_exec, x_aux)`

between events.

At an event coordinate:

`x_D^+ = J_D(x_D^-, x_C, t_target, x_ctrl)`

where:

`J_D`

is the discrete reset or execution mapping.

The pre-event and post-event states remain distinct.

---

## 50. Left and Right Event States

At a discrete event associated with model time `t_k`, a hybrid formulation may use:

`x_HYB(t_k^-)`

for the pre-event state and:

`x_HYB(t_k^+)`

for the post-event state.

A specialization using this notation must state which state components are continuous across the event and which may jump.

---

## 51. Operator Ordering

A coupled numerical step requires explicit operator ordering.

A representative ordering may be:

`continuous update`

`→ descriptor evaluation`

`→ resonance update`

`→ target generation`

`→ target registration`

`→ execution-control update`

`→ ternary execution`

`→ feedback`

Other orderings may be defined.

No ordering is assumed unless declared.

---

## 52. Ordering Is Result-Affecting State Definition

When two noncommuting update operators are applied in different orders, the resulting numerical realization may differ.

Therefore operator order belongs to the numerical execution contract.

A replay or validation record must use the same declared ordering when equality of results is required.

---

## 53. Operator Splitting

A coupled model may use operator splitting.

For continuous operator:

`Phi_C`

and discrete operator:

`Phi_D`

one realization may use:

`Phi_D ∘ Phi_C`

Another may use:

`Phi_C ∘ Phi_D`

These are distinct numerical operators unless equality is established.

---

## 54. No Hidden Discrete Update

A continuous update function must not silently:

- change retained ternary state;
- create or clear pending route;
- commit a ternary transition;
- advance scheduler state;

unless these operations are explicitly part of its declared coupled contract.

---

## 55. No Hidden Continuous Update

A discrete ternary execution function must not silently:

- advance atomic positions;
- advance velocities;
- integrate oscillator phase;
- update continuous model time;
- modify an unrelated continuous descriptor;

unless those operations are explicitly part of its declared coupled contract.

---

## 56. Feedback Mapping

A feedback mapping may transfer discrete execution state into a continuous or interatomic layer.

A generic mapping may be written:

`F_FB: T × X_C × X_aux → X_req`

where `X_req` is the declared update-request or conditioning space.

Feedback is an explicit mapping.

Ternary state does not directly become a continuous physical quantity without such a mapping.

---

## 57. Feedback Request and Physical Update

A feedback output may represent a request or conditioning variable rather than an immediate physical-state mutation.

Therefore:

`feedback request ≠ committed physical update`

when the architecture defines a separate physical update boundary.

---

## 58. Ternary Conditioning

An equivariant or continuous feature layer may use retained ternary state as an explicit conditioning input.

The conditioning mapping must state:

- input ternary state;
- conditioned feature space;
- transformation behavior;
- numerical parameters.

A target state is not substituted for retained state unless the conditioning contract explicitly specifies target conditioning.

---

## 59. Resonance Conditioning

A continuous or equivariant layer may use resonance state or resonance-derived parameters as explicit conditioning input.

Resonance conditioning does not identify:

- resonance coordinate with energy;
- oscillator phase with position;
- phase coupling with force;
- phase relation with chemical bond.

---

## 60. History State

History-dependent dynamics require explicit history state or an equivalent complete retained representation.

History state is denoted:

`x_H ∈ X_H`

When the next state depends on prior evolution not reconstructible from the current visible state, the required history belongs to the computational state closure.

---

## 61. Memory State

Retained memory is denoted:

`x_M ∈ X_M`

Memory may contain:

- retained frequency;
- hysteresis variables;
- persistence counters;
- previous classifier state;
- route state;
- adaptive parameters;
- numerical solver state;
- other result-affecting retained variables.

Memory state is not automatically ternary state.

---

## 62. Memoryless Model

A model is memoryless with respect to a declared state representation only when the next-state mapping depends solely on the current declared state, current input, and declared parameters.

Omitted result-affecting history invalidates a memoryless representation.

---

## 63. State Closure

A deterministic state representation must contain every retained result-affecting variable or provide a deterministic reconstruction of it.

The state closure may include:

- continuous state;
- ternary execution state;
- pending route;
- scheduler state;
- memory;
- solver state;
- time coordinates;
- adaptive timestep state;
- random-generator state when used;
- other result-affecting control state.

---

## 64. Static Parameter Boundary

A parameter remains a static parameter only while it does not evolve during execution.

If an adaptive process changes a value and the changed value affects future results, the evolved value belongs to retained state.

Therefore:

`dynamic result-affecting parameter → state`

under the deterministic state-closure contract.

---

## 65. External Input Boundary

External input belongs to:

`U`

An input is not retained system state unless the model stores it or its effects require retained information.

The input history must be represented when future dynamics depend on past input values.

---

## 66. Continuous Parameter Update

A model may contain continuously evolving parameters.

Once such a parameter evolves according to the system dynamics, it becomes part of the continuous or auxiliary state rather than remaining a fixed parameter.

---

## 67. Discrete Parameter Update

A model may contain parameters updated at discrete events.

A result-affecting updated value belongs to discrete or auxiliary retained state.

Its update event must have an explicit ordering relative to target generation and execution.

---

## 68. Multirate Dynamics

A coupled realization may operate at multiple rates.

For example:

- continuous integration may occur every numerical step;
- resonance evaluation may occur every selected step;
- target generation may occur at another cadence;
- ternary execution may occur at execution tacts.

The mappings between these coordinates must be explicit.

---

## 69. Sampling Boundary

When continuous state is sampled for target generation, the sampling coordinate and source state must be defined.

Possible source states include:

- pre-step continuous state;
- post-step continuous state;
- interpolated continuous state;
- event-localized state.

These sampling choices define different numerical realizations unless equivalence is established.

---

## 70. Target Persistence

A target may persist across multiple continuous numerical steps.

If target persistence is used, the retained target or its deterministic reconstruction belongs to the execution-state closure.

Continuous evolution during that interval does not silently recompute the target unless the selected cadence requires it.

---

## 71. Target Replacement

A newly generated target may replace a previous nonpending target according to the selected target-registration contract.

A pending opposite-route destination is a separate execution-control variable.

Replacement of a pending destination requires an explicitly defined route policy.

---

## 72. Event Detection

A continuous-discrete model may use event detection.

An event detector maps continuous or hybrid state into an event condition.

A generic predicate is:

`G_event: X_HYB → {true, false}`

Detection of an event does not itself constitute state execution.

---

## 73. Event Authorization

An event guard or scheduler may authorize an event after detection.

Therefore:

`event detection ≠ authorization`

and:

`authorization ≠ commit`

The committed update occurs only through the declared execution operator.

---

## 74. Event Localization

A numerical implementation may localize an event within a numerical interval.

Event localization affects the numerical realization.

It does not alter the formal distinction between continuous threshold crossing and discrete committed transition.

---

## 75. Continuous Threshold Hysteresis

A target classifier may contain hysteresis.

When hysteresis affects future target generation, the hysteresis state belongs to:

`X_M`

or another explicitly declared retained state space.

Classifier hysteresis is not active-neutral routing.

Therefore:

`classifier hysteresis ≠ neutral routing`

---

## 76. Resonance Window Hysteresis

A resonance window may be history-dependent or hysteretic.

Such behavior belongs to resonance-state or history-state semantics.

It does not itself define ternary pending-route state.

---

## 77. Neutral Routing and Continuous Dynamics

Neutral routing is a discrete execution mechanism.

A continuous trajectory passing numerically through zero is not active-neutral routing.

A continuous scalar equal to zero is not active ternary neutral state unless explicitly mapped into `T`.

---

## 78. Continuous Zero versus Active Neutral

Let:

`x ∈ R`

with:

`x = 0`

This is a continuous scalar value.

Let:

`t_exec = 0`

This is active ternary neutral state.

The relation is:

`continuous numeric zero ≠ active ternary neutral state`

unless an explicit mapping establishes a state correspondence.

---

## 79. Physical Observable Boundary

Physical observables such as:

- energy;
- force;
- stress;
- temperature;
- pressure;
- density;
- transport coefficients

remain separate from ternary state.

A physical observable may influence target generation through an explicit mapping.

Numerical equality with a ternary label does not assign ternary semantics.

---

## 80. Molecular-Dynamics State

A molecular-dynamics state may be represented as:

`x_MD = (configuration, velocities, masses, step, time)`

under the corresponding executable reference contract.

The molecular-dynamics state is a physical and numerical state.

It is not itself a ternary execution state.

---

## 81. Molecular-Dynamics Update Boundary

A molecular-dynamics integrator advances the variables declared in its molecular-dynamics state contract.

The reference molecular-dynamics step does not implicitly:

- evolve resonance state;
- generate a ternary target;
- execute ternary routing;
- mutate retained ternary state.

A coupled MD/TR realization requires explicit coupling operators.

---

## 82. Force-Evaluation Boundary

Force evaluation may occur within a molecular-dynamics update.

Force is derived under the energy and differentiation contracts.

Force evaluation does not itself update:

- oscillator phase;
- resonance classification;
- ternary target;
- retained ternary state.

---

## 83. Graph-Rebuild Boundary

A molecular-dynamics realization may rebuild an interaction graph between physical states.

Graph rebuilding and physical time integration are separate operations.

A force differentiation contract may hold graph topology fixed internally while the graph used at a later physical state is rebuilt.

These are different scopes.

---

## 84. Periodic Geometry Boundary

Periodic coordinate handling is a geometric operation.

Position wrapping, unwrapping, minimum-image selection, and ternary execution are unrelated operations unless explicitly coupled.

A periodic boundary crossing is not a ternary transition.

---

## 85. Multiscale Boundary

A multiscale transformation maps state between declared scales.

It is separate from continuous-time evolution and discrete ternary execution.

Therefore:

`scale transformation ≠ time evolution`

`scale transition ≠ ternary transition`

`scale transition ≠ physical phase transition`

---

## 86. Structural Transition Boundary

A structural transition belongs to the declared structural model.

It is not a ternary transition by definition.

A coupling between structural and ternary state requires an explicit mapping and explicit ordering.

---

## 87. Physical Phase Boundary

Physical phase of matter belongs to a physical state or classification space.

It is not oscillator phase.

It is not balanced ternary state.

Therefore:

`oscillator phase ≠ physical phase of matter`

and:

`ternary transition ≠ physical phase transition`

---

## 88. Learning Boundary

Training and optimization operate on learning-state variables and model parameters.

A training-stage transition is not a ternary transition.

A learned classifier may generate ternary targets.

The learned classifier remains upstream of discrete execution.

---

## 89. Classifier Temperature Boundary

A classifier temperature, softening parameter, or optimization temperature is not thermodynamic temperature unless explicitly defined as such.

Neither quantity is a ternary state.

---

## 90. Deterministic Update Contract

For a deterministic coupled realization, identical complete initial state, inputs, parameters, numerical settings, and operator ordering must produce identical declared outputs under the same execution environment contract.

Result-affecting hidden mutable state is excluded from a complete deterministic representation.

---

## 91. Deterministic Continuous Update

For deterministic:

`Phi_Delta_t`

identical admissible inputs produce identical updated continuous state.

If adaptive stepping is used, the result-affecting adaptive state belongs to the deterministic closure.

---

## 92. Deterministic Target Generation

For deterministic:

`P_CT`

identical complete source state and mapping parameters produce identical:

`t_target`

If target generation uses history, the required history belongs to the complete input state.

---

## 93. Deterministic Ternary Execution

For deterministic:

`F_T`

identical retained state, target, pending state, guard state, scheduler state, and other declared control state produce identical execution results.

---

## 94. Deterministic Coupled Step

A complete coupled step may be represented as:

`F_HYB: X_HYB × U × P → X_HYB`

for a discrete numerical realization.

Determinism of `F_HYB` requires every result-affecting component to be part of the declared input or retained state.

---

## 95. Replay Boundary

A deterministic replay must reproduce the declared observable or serialized representation under the replay contract.

Replay requires the same result-affecting:

- initial state;
- input sequence;
- parameters;
- numerical settings;
- operator ordering;
- state-update semantics.

---

## 96. State versus Trace

Execution state and trace state are separate.

Let:

`P_trace: X_exec → X_trace`

A trace records selected execution information.

It need not contain the complete restart state unless explicitly defined as a checkpoint representation.

---

## 97. Trace Ordering

A coupled trace should identify the coordinate associated with each record.

Possible coordinates include:

- model time;
- numerical step;
- execution coordinate;
- target-evaluation coordinate.

If multiple coordinates are present, their values remain distinct fields or explicitly related quantities.

---

## 98. Transition Trace

A ternary transition trace may contain:

- previous retained state;
- requested target;
- pending destination;
- execution route;
- resulting retained state.

An opposite-polarity route must preserve the intermediate neutral state as a separate committed execution state.

---

## 99. Continuous Trace

A continuous-state trace may contain:

- model time;
- positions;
- velocities;
- phase state;
- resonance descriptors;
- continuous observables.

Continuous trace values remain separate from discrete ternary execution state.

---

## 100. Coupled Trace

A coupled trace may contain continuous and discrete fields in one record.

Co-location in one serialized record does not merge their mathematical state spaces.

The schema or record contract must preserve field identity.

---

## 101. Checkpoint Boundary

A restart-complete checkpoint contains all result-affecting retained state required to continue deterministic execution.

A trace record is not automatically a restart-complete checkpoint.

The relation remains:

`trace record ≠ checkpoint`

unless a specific trace representation explicitly satisfies the checkpoint contract.

---

## 102. Serialization Boundary

Serialization maps computational state into a stored representation.

Serialization does not redefine:

- continuous state semantics;
- ternary state semantics;
- event ordering;
- target/execution separation.

A serialization format must preserve the distinctions required for its declared use.

---

## 103. Missing Data Boundary

Missing or unavailable continuous data is not active ternary state.

Missing observables are represented separately.

The following relations remain:

`missing ≠ 0`

`invalid ≠ 0`

`NaN ≠ 0`

`mask ≠ 0`

`padding ≠ 0`

where the right-hand `0` denotes active ternary neutral state.

---

## 104. Numerical Failure Boundary

A failed numerical solve is a numerical or validation condition.

It is not a ternary state by default.

A numerical failure must not be represented as active neutral `0` unless a separate explicit application mapping defines that behavior.

---

## 105. Validation-State Boundary

Validation status belongs to:

`K_val`

or another explicitly defined validation set.

It is not a continuous physical state.

It is not a ternary state.

Therefore:

`validation status ≠ ternary state`

---

## 106. Numerical Stability Boundary

Numerical stability is a property of a numerical method and model under specified conditions.

A stable numerical step is not a ternary state.

A ternary-state transition does not by itself establish numerical stability.

---

## 107. Mathematical Stability Boundary

Dynamical stability and numerical stability are separate concepts.

A mathematical stability condition applies to the declared dynamical system.

A numerical stability condition applies to the declared discretization.

Neither is automatically represented by ternary state.

---

## 108. Conservation Boundary

A conservation law belongs to the relevant physical or mathematical system.

A ternary transition may occur while a separately defined conserved quantity remains conserved.

Conservation status does not redefine the ternary transition relation.

---

## 109. Energy Boundary

Energy belongs to an energy space or scalar codomain.

Ternary state belongs to:

`T`

Therefore:

`energy ≠ ternary state`

A feedback model that uses ternary conditioning inside an energy model must still define energy through the energy functional.

---

## 110. Force Boundary

Force belongs to a vector-valued physical observable space.

Therefore:

`force ≠ ternary state`

Phase coupling is not mechanical force.

A discrete transition does not directly define a force vector without an explicit physical mapping.

---

## 111. Spatial Symmetry Boundary

A spatial transformation acts on geometric or equivariant state according to its representation.

A ternary transition acts on ternary execution state.

Therefore:

`spatial rotation ≠ ternary polarity reversal`

The two operators belong to separate transformation domains.

---

## 112. Graph Boundary

Interaction-graph evolution, when present, is a topological or geometric state update.

It is not a ternary transition.

A graph edge is not automatically:

- phase coupling;
- chemical bond;
- ternary relation.

Explicit mappings are required.

---

## 113. Provenance Boundary

Provenance metadata identifies origin or evidence classification.

It is not part of continuous dynamics unless the model explicitly treats provenance as computational metadata.

It is not ternary state.

Provenance changes do not constitute physical or ternary evolution.

---

## 114. Continuous-Discrete Interface Contract

Every continuous-to-discrete interface must identify:

1. source state space;
2. source variables;
3. descriptor mapping where used;
4. resonance mapping where used;
5. target-generation mapping;
6. target parameters;
7. sampling coordinate;
8. history dependence;
9. target registration semantics;
10. execution boundary.

---

## 115. Discrete-Continuous Feedback Contract

Every discrete-to-continuous feedback interface must identify:

1. retained discrete source state;
2. whether target state is also used;
3. feedback mapping;
4. feedback codomain;
5. physical or feature variables affected;
6. update timing;
7. update ordering;
8. retained memory effects;
9. dimensional interpretation where applicable;
10. validation conditions.

---

## 116. Coupled Operator Contract

A coupled numerical operator must state:

- input state;
- output state;
- temporal coordinate;
- numerical coordinate;
- execution coordinate;
- target-evaluation coordinate where separate;
- operator ordering;
- state components updated by each operator;
- state components held fixed by each operator;
- history requirements;
- deterministic state closure.

---

## 117. No Implicit Identification Rule

The following objects are not implicitly identified:

`continuous state ≠ descriptor`

`descriptor ≠ resonance state`

`resonance state ≠ resonance classification`

`resonance classification ≠ ternary target`

`ternary target ≠ retained ternary state`

`retained ternary state ≠ physical observable`

`physical observable ≠ validation status`

Each relation requires an explicit mapping if a model connects the two domains.

---

## 118. No Hidden Evolution Rule

An operator must not change a state component outside its declared update set.

If a function updates several architectural layers, it is a coupled operator and its complete update contract must state those layers.

---

## 119. State Ownership Rule

Every result-affecting variable must have a declared state-space owner.

Examples include:

- `X_C` for continuous state;
- `X_R` for resonance state;
- `T` for ternary state;
- `X_pending` for pending route;
- `X_sched` for scheduler state;
- `X_M` for memory;
- `X_solver` for solver state.

A variable must not change semantic ownership solely because it is stored in another software object.

---

## 120. Boundary Crossing Rule

A value crosses from one semantic state space to another only through an explicit mapping.

Examples are:

`X_C → X_DESC`

`X_DESC → X_R`

`X_R → T_target`

`T_exec × X_EIF → X_EIF,req`

Machine casting alone is not a semantic mapping.

---

## 121. Numerical Ordering Rule

When several update stages occur at the same nominal numerical step, their order is part of the numerical realization.

The implementation and its deterministic replay must use the same declared ordering.

---

## 122. Continuous-Discrete Consistency Rule

A coupled realization preserves continuous-discrete consistency when:

- continuous variables are updated only by declared continuous or coupled operators;
- ternary state is updated only by declared execution operators;
- target generation remains separate from execution;
- pending state remains separate from active neutral state;
- all cross-layer transfers use explicit mappings;
- all result-affecting retained variables belong to state closure.

---

## 123. Reference Resonance Implementation

The executable resonance package is located under:

`src/tr_eif/resonance/`

The reference implementation includes:

- resonance state;
- phase-dynamics parameters;
- phase derivatives;
- explicit integration;
- phase-order evaluation;
- resonance descriptors;
- resonance windows;
- resonance classification.

These interfaces remain separate from ternary execution.

---

## 124. Reference Ternary Implementation

The executable ternary package is located under:

`src/tr_eif/ternary/`

The reference implementation includes:

- ternary state;
- transition relation;
- routing;
- retained execution state;
- target mapping;
- resonance projection;
- vector execution;
- execution guards.

These interfaces define the executable discrete boundary.

---

## 125. Reference Molecular-Dynamics Implementation

The executable molecular-dynamics package is located under:

`src/tr_eif/md/`

Its current interfaces separate:

- physical MD state evolution;
- force evaluation;
- graph reconstruction between physical states;
- trajectory generation;
- MD observables.

Resonance and ternary evolution are not hidden inside the reference molecular-dynamics integration step.

---

## 126. Reference Observable Implementation

The executable observable package is located under:

`src/tr_eif/observables/`

It contains trace, serialization, export, and deterministic replay interfaces.

Observable production remains downstream of declared state evolution.

---

## 127. Mathematical References

Canonical notation is defined in:

`docs/volume_01_mathematical_foundations/chapter_02_notation_and_definitions.md`

Continuous-to-ternary mapping is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_05_continuous_to_ternary_mapping.md`

Active-neutral dynamics are defined in:

`docs/volume_02_ternary_resonance_theory/chapter_06_active_neutral_state_dynamics.md`

Neutral routing is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_07_neutral_routing.md`

Coupled continuous-discrete dynamics are defined in:

`docs/volume_02_ternary_resonance_theory/chapter_08_coupled_continuous_discrete_dynamics.md`

Numerical time evolution is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_10_numerical_time_evolution.md`

---

## 128. Repository-Level References

The framework architecture is defined in:

`docs/architecture/framework_architecture.md`

The balanced ternary state specification is defined in:

`docs/specifications/ternary_state_specification.md`

Committed transition semantics are defined in:

`docs/specifications/transition_semantics.md`

---

## 129. Contract Invariants

The continuous-discrete architecture preserves:

`T = {-1, 0, 1}`

`target ≠ executed retained state`

`pending target ≠ active neutral state`

`-1 → 1` is not a direct committed transition.

`1 → -1` is not a direct committed transition.

`-1 → 0 → 1`

`1 → 0 → -1`

`continuous state ≠ ternary state`

`continuous zero ≠ active ternary neutral state`

`descriptor ≠ ternary target`

`resonance classification ≠ ternary state`

`threshold crossing ≠ committed ternary transition`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`model time ≠ numerical step`

`numerical step ≠ execution coordinate`

`target generation ≠ ternary execution`

`hold ≠ committed retention transition`

`request ≠ commit`

`authorization ≠ commit`

`scale transformation ≠ time evolution`

`scale transition ≠ ternary transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`ternary state ≠ energy`

`ternary state ≠ force`

`validation status ≠ ternary state`

---

## 130. Contract Closure

The repository-level continuous-discrete dynamics boundary is:

`continuous state`

`→ explicit descriptor mapping`

`→ explicit resonance mapping`

`→ explicit ternary-target mapping`

`→ execution-control boundary`

`→ neutral-mediated ternary execution`

`→ retained ternary state`

`→ explicit feedback mapping`

`→ subsequent continuous state`

Continuous and discrete layers may be coupled through these interfaces.

They remain separately typed.

Their update operators, temporal coordinates, execution coordinates, retained memory, and cross-layer mappings remain explicit parts of the model and numerical realization contracts.
