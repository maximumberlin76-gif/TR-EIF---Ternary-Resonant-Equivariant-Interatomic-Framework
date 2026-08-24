# State Spaces

## 1. Purpose

This chapter defines the state-space architecture of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The purpose of the state-space layer is to provide explicit mathematical domains for:

- continuous variables;
- circular phase variables;
- balanced ternary variables;
- resonance coordinates;
- atomic configurations;
- interatomic state;
- graph and topology state;
- invariant and equivariant representations;
- learning state;
- molecular-dynamics state;
- history and memory;
- multiscale state;
- uncertainty;
- validation and execution-control state.

The chapter develops the state-space consequences of the axiomatic system without introducing the mathematical operators, structures, mappings, lemmas, or theorems assigned to later chapters.

The governing principle is:

`different semantic roles → different typed spaces`.

Numerical compatibility does not imply mathematical identity.

---

## 2. General State-Space Form

Let:

`X`

denote the complete state space of a selected TR-EIF model.

A complete state is:

`x ∈ X`.

For a composite system:

`X = X_1 × X_2 × ... × X_n`.

A corresponding state is:

`x = (x_1, x_2, ..., x_n)`

with:

`x_i ∈ X_i`.

The product decomposition is semantic.

Each factor retains its own:

- topology;
- dimensional meaning;
- transformation behavior;
- update semantics;
- locality;
- scale;
- provenance where relevant.

---

## 3. State-Space Typing

Two state spaces are considered distinct whenever their elements have different mathematical or semantic roles.

For example:

`R`

used as an energy codomain is not the same semantic state space as:

`R`

used as a numerical coordinate carrier.

Likewise:

`{-1, 0, 1}`

used as balanced ternary state is not interchangeable with any other three-valued classification set.

The semantic type is part of the state-space definition.

---

## 4. Continuous State Space

A finite-dimensional continuous state space may be represented as:

`X_c ⊆ R^n`.

A state is:

`x_c ∈ X_c`.

The integer:

`n ≥ 1`

is model-dependent.

Continuous state may contain components such as:

- positions;
- velocities;
- momenta;
- continuous internal variables;
- continuous resonance coordinates;
- thermodynamic variables;
- continuous learned features.

Continuous state is not discretized merely because it is stored numerically.

---

## 5. Euclidean State Space

A Euclidean state space is a subset of:

`R^n`

equipped with the standard Euclidean structure unless another metric is explicitly defined.

For:

`x, y ∈ R^n`

the Euclidean distance is:

`d_E(x, y) = ||x - y||_2`.

Use of Euclidean distance is valid only for quantities whose mathematical structure supports this metric.

---

## 6. Circular Phase Space

Oscillator phase belongs to:

`S^1 = R / (2 pi Z)`.

A phase state is:

`theta ∈ S^1`.

For `N` oscillators:

`Theta ∈ (S^1)^N`.

The phase space is therefore:

`X_phase = (S^1)^N`.

A numerical representative may lie in:

`[0, 2 pi)`

or another declared canonical interval.

The representative interval is not the phase space itself.

---

## 7. Product of Circular and Euclidean State

A system may contain both phase and Euclidean variables.

For example:

`X = R^m × (S^1)^N`.

A state is:

`x = (z, Theta)`

with:

`z ∈ R^m`

and:

`Theta ∈ (S^1)^N`.

The Euclidean and circular factors require different comparison and update semantics.

---

## 8. Discrete State Space

A discrete state space is denoted:

`X_d`.

Its elements form a finite or countable set according to the selected model.

A discrete state is:

`x_d ∈ X_d`.

No metric, ordering, arithmetic, or interpolation is assumed unless explicitly defined.

---

## 9. Balanced Ternary State Space

The canonical balanced ternary state space is:

`T = {-1, 0, 1}`.

The canonical notation is:

`-1/0/1`.

A balanced ternary state is:

`t ∈ T`.

The three values are semantic states.

They are not labels for:

- negative/zero/positive energy;
- outside/boundary/inside resonance;
- failure/unknown/success;
- absent/neutral/present data.

Such interpretations require explicit mappings.

---

## 10. Active Neutral Substate

The element:

`0 ∈ T`

is an active state.

Its role may include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

The active-neutral state is not represented through a separate null or missing-value domain.

---

## 11. Executed Ternary State Space

The executed state uses the same value set:

`T_exec = T`

but has a distinct semantic role.

An executed state is:

`t_exec ∈ T_exec`.

The semantic label `T_exec` distinguishes retained execution state from other ternary-valued objects.

---

## 12. Ternary Target Space

The ternary target space is:

`T_target = T`.

A target is:

`t_target ∈ T_target`.

Although:

`T_target`

and:

`T_exec`

share the same underlying value set, they are different semantic spaces.

Therefore:

`t_target`

must not be substituted for:

`t_exec`

without a transition operation.

---

## 13. Pending Destination Space

For neutral-mediated opposite-polarity routing, define a pending-state domain:

`X_pending = {NONE, -1, 1}`

where:

`NONE`

denotes absence of a pending opposite-polarity destination.

This representation preserves the distinction:

`NONE ≠ 0`.

A pending state is:

`t_pending ∈ X_pending`.

The active-neutral value `0` is intentionally excluded as the absence marker.

---

## 14. Ternary Execution State Space

A minimal ternary execution state may therefore be represented as:

`X_Texec = T_exec × T_target × X_pending`.

An element is:

`x_Texec = (t_exec, t_target, t_pending)`.

More detailed execution models may extend this space with:

- scheduler state;
- route identity;
- authorization state;
- execution coordinate;
- capacity state.

Such additions remain separately typed.

---

## 15. Ternary Transition Admissibility

The committed state-transition relation operates on:

`T_exec`.

The forbidden direct pairs are:

`(-1, 1)`

and:

`(1, -1)`.

Opposite-polarity routing uses the state sequence:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

The intermediate state belongs to the same exact state set:

`T_exec`.

It is not an approximate intermediate value.

---

## 16. Resonance Coordinate Space

The resonance-coordinate space is:

`X_R`.

A resonance state is:

`r ∈ X_R`.

The space may be:

- one-dimensional;
- multidimensional;
- continuous;
- mixed;
- scale-indexed;
- history-augmented;
- topology-dependent.

No universal dimension is imposed.

---

## 17. Finite-Dimensional Resonance Space

A finite-dimensional resonance-coordinate space may be represented as:

`X_R ⊆ R^m`

for:

`m ≥ 1`.

The coordinates may represent model-defined quantities such as:

- frequency relations;
- phase relations;
- response amplitudes;
- coupling descriptors;
- dissipation descriptors;
- structural descriptors;
- memory-dependent coordinates.

Each coordinate must have a defined mathematical and dimensional type.

---

## 18. Mixed Resonance State Space

A resonance state need not be purely Euclidean.

For example:

`X_R = X_R,c × X_R,d`

may combine continuous coordinates and discrete descriptors.

The individual factors remain separately typed.

---

## 19. Resonance Window

A resonance window is a subset:

`W_R ⊂ X_R`.

Its boundary is:

`∂W_R`.

The window and its boundary are objects defined relative to the topology of `X_R`.

---

## 20. Resonance Classification Space

The minimal classification space is:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

A classification value is:

`k_R ∈ K_R`.

The classification space is distinct from:

`T`.

Therefore:

`K_R ≠ T`.

---

## 21. History-Augmented Resonance State

For history-dependent resonance, define:

`X_RH = X_R × X_H`.

A state is:

`x_RH = (r, h)`.

The history component:

`h ∈ X_H`

contains the information required by the selected resonance relation.

---

## 22. Topology-Augmented Resonance State

For topology-dependent resonance:

`X_RT = X_R × X_G`.

A state is:

`(r, g_top)`.

The topology state remains distinct from the resonance coordinate itself.

---

## 23. Scale-Augmented Resonance State

For scale-dependent resonance:

`X_RS = X_R × L`.

A state is:

`(r, ell)`.

The scale label:

`ell`

identifies the scale at which the resonance state is defined.

---

## 24. History State Space

The history state space is:

`X_H`.

A history state is:

`h ∈ X_H`.

The exact structure depends on the model.

Examples include:

- finite windows of previous states;
- delayed state functions;
- event histories;
- hysteresis branch state;
- retained trajectory segments.

---

## 25. Functional History Space

For delayed continuous systems, a history may be represented as a function.

For delay horizon:

`tau_max > 0`

and state space:

`X_c`,

a history function may belong to a space of functions:

`h: [-tau_max, 0] → X_c`.

The regularity class of the function space must be specified by the selected delay model.

---

## 26. Memory State Space

Memory state belongs to:

`X_M`.

A memory state is:

`m ∈ X_M`.

Memory variables may include:

- retained filtered state;
- internal relaxation state;
- hysteresis state;
- adaptive internal variables;
- persistent routing state.

Memory and history are distinct unless explicitly identified by the selected model.

---

## 27. Complete Non-Markovian State

A model that appears non-Markovian in visible state:

`x_visible`

may be represented as Markovian in an extended state:

`x_ext = (x_visible, m, h)`

when sufficient memory and history state are retained.

The complete state space is then:

`X_ext = X_visible × X_M × X_H`.

---

## 28. Atomic Species Space

Let:

`A_sp`

denote the species-label space.

For `N` atomic entities, the species state belongs to:

`X_species = A_sp^N`.

A species vector is:

`a = (a_1, ..., a_N)`.

Species labels are categorical variables.

---

## 29. Atomic Position Space

For `N` entities in three-dimensional Cartesian space:

`X_pos = R^(3N)`.

The position state is:

`R_pos = (r_1, ..., r_N)`

with:

`r_i ∈ R^3`.

For periodic systems, the position space is interpreted together with the simulation-cell and periodic-identification structure.

---

## 30. Atomic Velocity Space

The velocity state space is:

`X_vel = R^(3N)`.

A velocity state is:

`V = (v_1, ..., v_N)`.

Each:

`v_i ∈ R^3`.

---

## 31. Momentum Space

The momentum state space is:

`X_mom = R^(3N)`.

A momentum state is:

`P_mom = (p_1, ..., p_N)`.

Momentum and velocity spaces may be connected by a mass-dependent mapping introduced later.

They remain distinct state spaces.

---

## 32. Simulation-Cell Space

A three-dimensional simulation cell may be represented by a nonsingular matrix:

`H ∈ R^(3×3)`.

Define the admissible cell space:

`X_cell ⊆ R^(3×3)`

subject to the model's nondegeneracy and orientation conditions.

The exact admissibility conditions are defined by the selected molecular-dynamics model.

---

## 33. Atomic Configuration Space

A basic atomic configuration state space may be written:

`X_conf = X_species × X_pos × X_cell`

for a periodic system.

For a nonperiodic system, the cell factor may be omitted or replaced by another boundary specification.

A configuration state is:

`x_conf ∈ X_conf`.

---

## 34. Interatomic Dynamic State

A dynamic interatomic state may include:

`X_atom = X_species × X_pos × X_vel × X_cell`.

Alternative formulations may use momentum instead of velocity:

`X_atom = X_species × X_pos × X_mom × X_cell`.

The two representations must not be mixed without an explicit conversion.

---

## 35. Entity Identity Space

Let:

`I_atom`

denote the semantic identity space for atomic entities.

For each entity:

`id_i ∈ I_atom`.

Entity identity is distinct from storage index.

A permutation of storage order leaves the semantic identities unchanged.

---

## 36. Interaction Graph Space

Let:

`V`

be the entity set.

An interaction graph is:

`G = (V, E_G)`.

The graph state belongs to a graph space:

`X_G`.

Different graph states may differ in:

- edge set;
- edge attributes;
- node attributes;
- directedness;
- periodic-image relation.

---

## 37. Edge-State Space

Where edges carry model-defined attributes, define:

`X_edge`.

For edge:

`(i, j) ∈ E_G`

the edge state is:

`e_ij ∈ X_edge`.

Examples may include:

- displacement;
- distance;
- interaction type;
- learned feature;
- resonance descriptor.

---

## 38. Node-State Space

Where graph nodes carry features, define:

`X_node`.

For entity `i`:

`z_i ∈ X_node`.

Node features remain distinct from atomic identity and storage position.

---

## 39. Local Environment Space

For each entity `i`, define a local-environment space:

`X_env,i`.

Where all entities share a common representation type:

`X_env,i = X_env`.

A local environment state is:

`e_i ∈ X_env`.

It may encode geometry and topology surrounding entity `i`.

---

## 40. Locality Domain

A local environment is defined relative to a neighborhood:

`N_i`.

The neighborhood may depend on:

- geometric cutoff;
- graph topology;
- periodic images;
- species;
- model-specific interaction rules.

The neighborhood definition belongs to the local-state specification.

---

## 41. Invariant Representation Space

An invariant representation belongs to:

`X_INV`.

A state is:

`z_INV ∈ X_INV`.

Its defining property under a declared transformation action is invariance.

The dimensional structure of `X_INV` depends on the selected representation.

---

## 42. Equivariant Representation Space

An equivariant representation belongs to:

`X_EQ`.

A state is:

`z_EQ ∈ X_EQ`.

The space carries a declared group action:

`rho_EQ(g)`.

The action is part of the state-space definition.

---

## 43. Representation Decomposition

An EIF representation may contain both invariant and equivariant channels:

`X_rep = X_INV × X_EQ`.

An element is:

`z = (z_INV, z_EQ)`.

The two factors retain different transformation behavior.

---

## 44. Scalar Representation Channel

A rotational scalar channel may belong to:

`R^m`.

Its scalar status is defined by the transformation action, not by storage dimension alone.

---

## 45. Vector Representation Channel

A Cartesian vector channel may belong to:

`(R^3)^m`.

Under rotation:

`Q ∈ SO(3)`

each vector transforms under the declared vector action.

---

## 46. Higher-Order Representation Channel

Higher-order equivariant channels require their own representation spaces and transformation laws.

They are not defined solely by array rank.

---

## 47. Transformation Group State

The transformation group itself is not ordinary model state.

However, a transformation parameter used in a transformed fixture or transformed configuration belongs to its declared group:

`g ∈ G_sym`.

For rotations:

`Q ∈ SO(3)`.

For permutations:

`pi ∈ S_N`.

For translations:

`a ∈ R^3`.

---

## 48. E(3) Action Domain

An EIF state space may carry an action of:

`E(3)`.

Where reflections are excluded, a model may instead use:

`SE(3)`.

Where only rotations are relevant:

`SO(3)`.

The chosen group determines the applicable transformation structure.

---

## 49. Energy Codomain

A scalar energy value belongs to:

`X_energy = R`

or to a restricted subset determined by the model.

Energy is an observable or state component only when explicitly included.

It remains distinct from:

`T`

and:

`K_R`.

---

## 50. Force Space

For `N` atomic entities:

`X_force = R^(3N)`.

A force state or observable is:

`F ∈ X_force`.

Force has vector transformation semantics under spatial transformations.

---

## 51. Stress Space

A Cartesian stress tensor belongs to:

`X_stress ⊆ R^(3×3)`.

Additional symmetry constraints may restrict the admissible subset in a selected model.

Stress is separately typed from:

- force;
- energy;
- strain;
- pressure.

---

## 52. Thermodynamic State Space

A selected thermodynamic model may define:

`X_thermo`.

Its components may include:

- temperature;
- pressure;
- volume;
- density;
- enthalpy;
- composition variables.

Only quantities explicitly belonging to the selected thermodynamic model are included.

---

## 53. Physical Phase Space

Where a material-phase classification is defined, let:

`K_phase`

denote its classification space.

This space is distinct from oscillator phase:

`S^1`.

Therefore:

`K_phase ≠ S^1`.

---

## 54. Structural State Space

A structural state belongs to:

`X_S`.

A structural descriptor may be continuous, discrete, graph-valued, or composite.

Structural state is distinct from:

`T`

unless an explicit mapping connects them.

---

## 55. Learning Parameter Space

The trainable parameter space is:

`Theta`.

A trainable parameter state is:

`theta_param ∈ Theta`.

Trainable parameters are distinct from:

- atomic state;
- resonance state;
- oscillator phase;
- ternary state;
- validation state.

---

## 56. Dataset Space

Let:

`D`

denote the dataset space.

A datum is:

`d ∈ D`.

A dataset instance may contain:

- configurations;
- energies;
- forces;
- stresses;
- labels;
- metadata;
- uncertainty information.

The exact data structure is defined by the learning problem.

---

## 57. Loss Space

A scalar loss value belongs to:

`X_loss = R`.

Individual loss components may have different source spaces before normalization or weighting.

Their combination requires an explicit loss functional.

---

## 58. Optimization State Space

An optimizer may carry additional state:

`X_opt`.

An optimizer state is:

`x_opt ∈ X_opt`.

Examples include:

- momentum accumulators;
- adaptive learning-rate state;
- iteration counters;
- parameter-history state.

Optimizer state is computational learning state.

---

## 59. Complete Learning State

A complete trainable computational state may be represented as:

`X_learn = Theta × X_opt`.

Where stochastic training is used, the random state may extend the space:

`X_learn = Theta × X_opt × X_rng`.

---

## 60. Molecular-Dynamics State Space

A molecular-dynamics state may be represented as:

`X_MD = X_pos × X_mom × X_cell × X_aux`.

The auxiliary space:

`X_aux`

contains additional model state required by the selected realization.

---

## 61. TR-Augmented Molecular-Dynamics State

Where TR state participates directly in molecular dynamics:

`X_MD-TR = X_MD × X_TR`.

The two factors retain separate update rules.

A ternary state does not become position, momentum, force, or energy merely by belonging to the same composite state.

---

## 62. Thermostat State Space

Where an extended-system thermostat is used:

`X_thermostat`

denotes its internal state space.

Thermostat state belongs to complete dynamical state when it affects future evolution.

---

## 63. Barostat State Space

Where a barostat is used:

`X_barostat`

denotes its internal state space.

Barostat variables remain distinct from the physical simulation-cell state even when they influence it.

---

## 64. Extended Molecular-Dynamics State

A general extended state may be:

`X_MD,ext = X_MD × X_thermostat × X_barostat × X_TR × X_M`.

Only factors used by the selected model are included.

---

## 65. Numerical State Space

A numerical realization may require a computational state space:

`X_num`.

A numerical state is:

`x_num ∈ X_num`.

This space may contain encoded forms of mathematical state together with solver-specific state.

---

## 66. Solver State Space

Result-affecting solver state belongs to:

`X_solver`.

A state is:

`x_solver ∈ X_solver`.

Examples include:

- previous integration stages;
- adaptive-step controller state;
- nonlinear iteration state;
- multistep history;
- numerical caches.

---

## 67. Numerical Proposal Space

A proposed numerical state belongs to:

`X_prop`.

It is semantically distinct from accepted state.

A proposal becomes accepted only through the numerical acceptance relation.

---

## 68. Accepted Numerical State Space

An accepted numerical state belongs to:

`X_acc`.

The value may encode the same mathematical variables as a proposal while occupying a different execution role.

---

## 69. Scheduler State Space

Scheduler state belongs to:

`X_sched`.

A state is:

`x_sched ∈ X_sched`.

Scheduler state may include:

- current scheduler phase;
- cycle position;
- eligibility state;
- retained scheduling counters.

Scheduler state is not model time.

---

## 70. Request Space

Computational requests belong to:

`X_req`.

A request state is:

`q_req ∈ X_req`.

The request space may encode:

- source;
- destination;
- requested operation;
- payload;
- execution coordinate;
- provenance.

---

## 71. Authorization Space

Authorization results belong to:

`X_auth`.

An authorization state is:

`a_auth ∈ X_auth`.

This space is distinct from:

`X_req`

and from committed model state.

---

## 72. Commit-Event Space

Commit events belong to:

`X_commit`.

A commit event is:

`e_commit ∈ X_commit`.

A commit is an execution event rather than a physical state variable unless event history is explicitly retained as state.

---

## 73. Event Space

General execution events belong to:

`X_event`.

An event is:

`e ∈ X_event`.

Different event classes may form tagged subsets of `X_event`.

---

## 74. Trace Space

Trace records belong to:

`X_trace`.

A trace is an ordered sequence:

`Trace = (e_0, e_1, ..., e_m)`

with:

`e_j ∈ X_trace`.

The trace space is distinct from complete execution-state space.

---

## 75. Snapshot Space

State snapshots belong to:

`X_snap`.

A snapshot may contain a projection of retained state.

It is not necessarily restart-complete.

---

## 76. Checkpoint Space

Restart-complete checkpoints belong to:

`X_CP`.

A checkpoint must contain all result-affecting state required by the declared restart contract.

Therefore:

`X_CP`

may include representations of:

- model state;
- TR state;
- EIF state;
- pending routes;
- memory;
- history;
- solver state;
- scheduler state;
- random state.

---

## 77. Random-State Space

Where stochastic processes are present:

`X_rng`

denotes the random-generator state space.

A random state is:

`x_rng ∈ X_rng`.

It is included in execution closure when future results depend on it.

---

## 78. Configuration Space

A computational configuration belongs to:

`X_cfg`.

A configuration is:

`c ∈ X_cfg`.

Immutable configuration is distinct from evolving state.

If a configuration quantity evolves, its evolving value becomes state.

---

## 79. Validation Result Space

The validation result set is:

`K_val = {PASS, FAIL, UNRESOLVED}`.

A validation result is:

`v_val ∈ K_val`.

The space is distinct from:

`T`.

Therefore:

`UNRESOLVED ≠ 0`.

---

## 80. Boolean State Space

Boolean predicates take values in:

`B = {false, true}`.

This space is distinct from:

`T`.

A Boolean result is not a balanced ternary result.

---

## 81. Provenance Space

The provenance set is:

`P_prov = {PRIMARY_SOURCE, DERIVED, CALIBRATED, AUTHOR_DEFINED, BENCHMARK, TEST_FIXTURE, REQUIRES_SOURCE, REQUIRES_TEST}`.

A provenance value is:

`p_prov ∈ P_prov`.

Provenance is metadata rather than model state unless a workflow explicitly represents provenance as computational state.

---

## 82. Uncertainty State Space

Where uncertainty is explicitly represented:

`X_U`

denotes the uncertainty space.

A state is:

`u_unc ∈ X_U`.

Possible representations include:

- scalar uncertainty;
- covariance;
- interval;
- ensemble descriptor;
- distribution parameterization;
- categorical domain status.

The exact form is model-specific.

---

## 83. Domain-Status Space

A domain detector outputs into:

`K_D`.

A domain status is:

`k_D ∈ K_D`.

This space is separately defined from:

- balanced ternary state;
- resonance classification;
- validation state.

---

## 84. Multiscale State Family

Let:

`L`

be the scale set.

For each:

`ell ∈ L`

define a state space:

`X^(ell)`.

The family:

`{X^(ell)}_(ell∈L)`

forms the multiscale state architecture.

---

## 85. Electronic-Scale State

Where an electronic-scale model is included, define:

`X_elec`.

Its exact mathematical structure depends on the selected electronic representation.

No particular electronic-structure formalism is imposed at the foundation level.

---

## 86. Atomistic-Scale State

The atomistic state space is denoted:

`X_atom`.

It may contain:

- atomic configuration;
- velocities or momenta;
- interatomic features;
- TR state;
- auxiliary state.

---

## 87. Mesoscale State

A mesoscale state belongs to:

`X_meso`.

Its variables must be defined independently from atomistic variables.

Coarse-grained quantities are not treated as atomistic state.

---

## 88. Continuum State

A continuum-scale state belongs to:

`X_cont`.

Examples may include spatial fields such as:

- density;
- momentum density;
- temperature;
- stress;
- composition.

The selected continuum model defines the actual field spaces.

---

## 89. Engineering-Scale State

An engineering-scale model state belongs to:

`X_eng`.

Its variables may represent integrated or field-level quantities appropriate to the selected engineering model.

---

## 90. Cross-Scale Product State

A coupled multiscale system may use:

`X_multi = X_elec × X_atom × X_meso × X_cont × X_eng`

with unused factors omitted.

Each scale retains independent mathematical identity.

---

## 91. Scale Transfer State

Where a transfer operation requires auxiliary state, define:

`X_transfer`.

This may contain:

- mapping coefficients;
- averaging regions;
- closure variables;
- uncertainty state;
- transfer history.

Such state must be explicit when it affects future transfers.

---

## 92. FLiBe Reference State Space

The FLiBe reference-model state space is denoted:

`X_FLiBe`.

Its detailed structure is defined in Volume 07.

At the foundational level it is understood as a specialization of the general interatomic, thermodynamic, resonance, ternary, molecular-dynamics, and multiscale state architecture.

---

## 93. FLiBe Composition State

The material composition component belongs to:

`X_FLiBe,comp`.

Its exact variables and admissible composition domain are defined in the FLiBe reference-model volume.

---

## 94. FLiBe Thermodynamic State

The reference thermodynamic component belongs to:

`X_FLiBe,thermo`.

Its variables are defined from the selected FLiBe thermodynamic model and reference data.

---

## 95. FLiBe Structural State

Local-structure and coordination variables belong to:

`X_FLiBe,struct`.

They remain distinct from:

- ternary state;
- resonance classification;
- thermodynamic phase state.

---

## 96. Integrated TR State Space

The complete Ternary Resonant state space is denoted:

`X_TR`.

A general decomposition may be written:

`X_TR = X_phase × X_R × K_R × T_target × T_exec × X_pending × X_M × X_H`

with only the factors required by the selected TR model included.

The decomposition preserves semantic separation among:

- phase;
- resonance;
- classification;
- target;
- execution;
- routing;
- memory;
- history.

---

## 97. Integrated EIF State Space

The complete Equivariant Interatomic Framework state space is denoted:

`X_EIF`.

A general decomposition may include:

`X_EIF = X_conf × X_G × X_env × X_INV × X_EQ × X_aux,EIF`.

The exact factorization is model-specific.

---

## 98. Integrated TR-EIF State Space

The complete integrated state space is:

`X_TR-EIF = X_EIF × X_TR × X_int`

where:

`X_int`

contains explicit integration state required by the selected coupling architecture.

An integrated state is:

`x_TR-EIF = (x_EIF, x_TR, x_int)`.

---

## 99. Integration State Space

The integration state space:

`X_int`

may contain:

- forward-mapping state;
- reverse-mapping state;
- cross-layer pending requests;
- scale metadata;
- coupling history;
- cross-layer memory.

Only result-affecting integration state is included.

---

## 100. Forward-Interface State

The EIF-to-TR interface may use a state space:

`X_E→TR`.

Its elements contain the typed representation required to transfer information from EIF into TR.

This space is distinct from both:

`X_EIF`

and:

`X_TR`.

---

## 101. Reverse-Interface State

The TR-to-EIF interface may use:

`X_TR→E`.

Its elements contain typed feedback requests or representations.

This space is distinct from committed EIF state.

---

## 102. Information-Loss State Annotation

Where a mapping is lossy, the destination state may carry metadata identifying:

- source representation;
- retained coordinates;
- discarded coordinates;
- approximation level.

Such metadata belongs to a separate descriptive state or artifact layer unless required for future evolution.

---

## 103. Dimensionally Typed State

A physical state variable has both:

- a value domain;
- a dimensional type.

For quantity `q`:

`q ∈ X_q`

and:

`dim(q) = D_q`.

Two quantities may share the same numerical carrier while having different dimensional types.

---

## 104. Dimensionless State

A dimensionless variable belongs to a dimensionless state domain.

Dimensionless numerical representation does not imply absence of semantic structure.

For example, phase-order magnitude:

`R ∈ [0, 1]`

is dimensionless but remains a specific observable.

---

## 105. Bounded State Space

A bounded state space:

`X_b`

satisfies a declared boundedness condition under an appropriate metric.

For example:

`X_b = [a, b]`

for scalar:

`a ≤ b`.

Boundedness is a property of the space or reachable subset, not a synonym for stability.

---

## 106. Constrained State Space

A constrained state space may be written:

`X_C = {x ∈ X | C(x) = true}`

for a declared constraint predicate:

`C`.

Constraint satisfaction is part of admissible state membership.

---

## 107. Reachable State Set

For initial state:

`x_0`

and evolution relation:

`F`,

the reachable state set may be denoted:

`Reach(x_0)`.

The precise construction depends on continuous, discrete, or hybrid dynamics.

Reachability is developed further in later mathematical chapters.

---

## 108. Admissible State Set

The admissible subset of a state space may be denoted:

`X_adm ⊆ X`.

Membership in `X_adm` means that all model-defined state constraints are satisfied.

---

## 109. Invalid State

A value outside:

`X_adm`

is an invalid state for the selected model.

Invalidity is not encoded automatically through:

`0`

or another valid state value.

---

## 110. Missing State Representation

Missingness belongs to a separate representation layer.

Where a field may be absent, define an extended domain such as:

`X_optional = X ∪ {NONE}`

with:

`NONE ∉ X`.

For ternary state:

`NONE ≠ 0`.

---

## 111. Error State Representation

Computational error belongs to a distinct error space:

`X_err`.

An error value is:

`e_err ∈ X_err`.

It must not be inserted into physical, resonance, ternary, or validation state spaces without an explicit conversion contract.

---

## 112. State Identity

A state instance may carry an identifier:

`id_state`.

State identity is metadata.

Two different identifiers may reference semantically equal states.

Likewise, identical identifiers must not refer to different immutable state objects within one declared identity scope.

---

## 113. State Equality

Exact state equality requires equality of all fields included in the state definition.

For composite states:

`x = y`

requires equality in every component under the applicable exact relation.

---

## 114. State Equivalence

A weaker semantic equivalence relation may be defined:

`x ≡ y`.

The relation must specify which distinctions are ignored.

Equivalence is not identical to exact equality.

---

## 115. Numerical State Equivalence

For finite numerical state, an approximate equivalence relation may use a metric:

`d(x, y) ≤ epsilon`.

Such a relation is valid only for state components admitting tolerance-based comparison.

Exact categorical fields remain exact.

---

## 116. Mixed Exact/Approximate State Comparison

A composite state may require mixed comparison semantics.

For example:

- positions compared numerically;
- phases compared on `S^1`;
- ternary states compared exactly;
- identifiers compared exactly;
- resonance classifications compared exactly.

One global scalar tolerance cannot replace these typed comparisons.

---

## 117. Phase-State Equality

Phase states satisfy circular equivalence.

If:

`theta_a - theta_b = 2 pi k`

for:

`k ∈ Z`,

then they represent the same element of:

`S^1`.

---

## 118. Ternary-State Equality

Ternary-state equality is exact.

For:

`t_a, t_b ∈ T`,

equality is ordinary categorical equality.

No tolerance is used.

---

## 119. Graph-State Equality

Graph-state equality depends on the declared graph identity convention.

Storage-order equality and semantic graph equality are distinct when entity reindexing is admissible.

---

## 120. Permutation-Equivalent State

For:

`pi ∈ S_N`

two indexed representations may describe the same physical configuration under a permitted reindexing.

Permutation equivalence must preserve:

- entity identity;
- species association;
- geometry association;
- edge association;
- per-entity features.

---

## 121. Translation-Equivalent State

Where global translation is physically redundant, two configurations related by:

`r_i' = r_i + a`

for all `i`

may belong to the same translation-equivalence class under the selected model.

The quotient structure is model-dependent.

---

## 122. Rotation-Equivalent State

Where global rotation is treated through symmetry, two configurations related by:

`r_i' = Q r_i`

with:

`Q ∈ SO(3)`

may be symmetry-related states.

They remain different coordinate representatives unless a quotient representation is explicitly constructed.

---

## 123. Symmetry Orbit

For state:

`x ∈ X`

and transformation group:

`G_sym`,

the orbit is:

`Orb(x) = {rho_X(g)x | g ∈ G_sym}`.

The orbit contains states related by the declared symmetry action.

---

## 124. Quotient State Space

Where symmetry-equivalent states are identified, a quotient space may be defined:

`X / G_sym`.

Such quotient construction must specify the group action and equivalence relation.

It is not assumed automatically for EIF state.

---

## 125. Invariant Representation as Orbit-Compatible State

An invariant representation assigns equal output to states within the same declared transformation orbit.

The representation space itself remains distinct from the original configuration space.

---

## 126. Equivariant Representation as Action-Carrying State

An equivariant representation retains transformation structure in its output space.

Its state space must therefore include the applicable output action.

---

## 127. Phase-Order Observable Space

The Kuramoto-style phase-order magnitude belongs to:

`X_Rorder = [0, 1]`.

A value:

`R ∈ X_Rorder`

is an observable derived from phase state.

This space is distinct from resonance-coordinate space:

`X_R`.

The shared letter `R` in established notation does not identify the two spaces.

---

## 128. Coherence Observable Space

A coherence observable belongs to a separately defined space:

`X_C`.

Its domain and range depend on the selected coherence definition.

No equality with:

`X_Rorder`

is assumed.

---

## 129. Synchronization-State Space

Where synchronization classification is required, define:

`K_sync`.

A synchronization state:

`k_sync ∈ K_sync`

is distinct from:

- resonance classification;
- phase-locking classification;
- ternary state.

---

## 130. Phase-Locking State Space

Where phase locking is classified, define:

`K_lock`.

A phase-locking state:

`k_lock ∈ K_lock`.

The space is independent of:

`K_R`

unless an explicit mapping is defined.

---

## 131. Bifurcation Parameter Space

A bifurcation analysis uses a parameter space:

`P_bif`.

A parameter:

`mu ∈ P_bif`.

The dynamical state remains in its original state space while `mu` indexes a family of systems.

---

## 132. Structural Classification Space

Where structural regimes are classified, define:

`K_struct`.

A structural classification:

`k_struct ∈ K_struct`

is distinct from:

`T`

and:

`K_R`.

---

## 133. Physical Phase Classification Space

Where material phases are classified, define:

`K_phys`.

A value:

`k_phys ∈ K_phys`

is distinct from oscillator phase:

`theta ∈ S^1`.

---

## 134. Composition State Space

For a material system containing `M` species, a composition vector may belong to:

`X_comp`.

If represented by normalized fractions:

`c_i ≥ 0`

and:

`sum_i c_i = 1`.

The exact composition representation is model-specific.

---

## 135. Constraint Manifold

A state space defined through smooth constraints may form a manifold:

`M_C ⊆ R^n`.

The manifold structure must be established from the selected constraints.

The term "manifold" is not inferred solely from dimensional reduction.

---

## 136. Tangent Space

For a smooth manifold:

`M`

and point:

`x ∈ M`,

the tangent space is:

`T_x M`.

Continuous evolution on a manifold has derivative state in the corresponding tangent space.

---

## 137. Tangent-Space Distinction

The state:

`x ∈ M`

and derivative:

`dx/dt ∈ T_x M`

belong to different mathematical spaces.

They must not be treated as identical vectors merely because they may share a coordinate representation.

---

## 138. State-Space Topology

Every state space requiring notions such as:

- continuity;
- boundary;
- convergence;
- neighborhood;
- compactness

must carry an appropriate topology.

For Euclidean spaces the standard topology may be used.

For product spaces the applicable product topology may be used.

---

## 139. Resonance-Window Boundary Topology

The expression:

`∂W_R`

is defined relative to the topology on:

`X_R`.

Changing the topology may change the boundary.

The topology must therefore be part of any rigorous resonance-window definition requiring boundary arguments.

---

## 140. Metric State Space

Where distance-based criteria are required, a metric:

`d_X: X × X → R_0+`

must be defined.

Different state spaces may require different metrics.

---

## 141. Product Metric

For product state:

`X = X_1 × X_2`

a product metric may be defined from metrics on the factors.

No universal product metric is imposed.

Weighting factors, normalization, and dimensional compatibility must be defined explicitly.

---

## 142. Dimensional Metrics

A metric combining dimensional quantities requires compatible normalization or a physically meaningful construction.

Raw addition of incompatible units is not permitted.

---

## 143. State-Space Measure

Where probability, integration, or statistical mechanics require a measure, the state space must be equipped with a declared measure.

No measure is assumed merely from the existence of a set.

---

## 144. Probability-State Space

Where stochastic state is modeled, define a probability space separately from the modeled physical state space.

Random variables map from the probability space into state spaces.

Probability is not balanced ternary uncertainty by default.

---

## 145. Ensemble State Space

An ensemble of states may belong to a product or distribution space derived from:

`X`.

An ensemble is not identical to one system state.

---

## 146. Distribution Space

Where distributions over states are modeled, define a distribution space:

`P(X)`

or another explicitly defined family of probability measures over `X`.

This is distinct from parameter space:

`P`.

Notation must be locally qualified if both are present.

---

## 147. Observable-State Separation

For:

`O: X → Y`

the observable value:

`y = O(x)`

belongs to:

`Y`.

The value remains outside `X` unless the model explicitly includes it as retained state.

---

## 148. Derived-State Space

A derived representation may belong to:

`X_der`.

Its elements are determined from another state through a mapping.

Derived state may be cached computationally while remaining mathematically derived.

---

## 149. Cached-State Space

A computational cache belongs to:

`X_cache`.

If the cache can be reconstructed deterministically and does not affect semantic results, it need not belong to the formal model state.

If it affects future results, it belongs to computational state closure.

---

## 150. Execution-Control State

Execution-control state belongs to:

`X_ctrl`.

It may include:

- scheduler;
- authorization;
- capacity;
- queue;
- commit-control;
- replay-control.

Execution-control state is distinct from modeled physical state.

---

## 151. Complete Computational State

A complete computational state may be represented as:

`X_comp = X_model × X_num × X_ctrl × X_cache,result × X_rng`

with only applicable factors included.

Here:

- `X_model` is the modeled mathematical state;
- `X_num` is result-affecting numerical state;
- `X_ctrl` is result-affecting execution-control state;
- `X_cache,result` is result-affecting cache state;
- `X_rng` is stochastic state where applicable.

---

## 152. Complete Restart State

A restart-complete state is the subset of computational state required to determine future execution after restoration.

Its exact space is model- and implementation-specific.

The restart state must include every result-affecting component not reconstructible deterministically from retained information.

---

## 153. State-Space Closure

A model state space is closed for its declared evolution when every variable required by the evolution relation belongs to:

- the current state;
- declared history;
- declared input;
- declared parameter state.

No undeclared variable may affect the next state.

---

## 154. Computational State Closure

A computational state is closed when all result-affecting variables required to reproduce future computation are represented.

This may extend mathematical state with:

- solver state;
- scheduler state;
- memory;
- cache state;
- random state.

---

## 155. TR State Closure

A TR execution state is closed only when all result-affecting components required by the selected TR model are present.

Depending on the model, these may include:

- phase;
- resonance coordinates;
- resonance classification;
- ternary target;
- executed ternary state;
- pending destination;
- memory;
- history;
- scheduler state.

---

## 156. EIF State Closure

An EIF state is closed only when all interatomic and representation variables required by the selected EIF mapping are available.

Depending on the model, these may include:

- species;
- geometry;
- topology;
- local environments;
- invariant features;
- equivariant features;
- model parameters;
- auxiliary state.

---

## 157. Integrated State Closure

An integrated TR-EIF state is closed only when both TR and EIF state closures are satisfied together with all result-affecting cross-layer state.

---

## 158. Multiscale State Closure

A multiscale state is closed only when every scale-specific evolution and cross-scale transfer has access to the state and closure variables it requires.

---

## 159. State-Space Extension

Given:

`X`

and new state space:

`Y`,

an extended state space is:

`X' = X × Y`.

The extension is admissible only when the semantic role of `Y` is defined.

---

## 160. State-Space Reduction

A reduced state space:

`X_red`

is obtained from:

`X`

through an explicit mapping:

`P_red: X → X_red`.

Any information loss must be characterized by the mapping.

---

## 161. State Embedding

An embedding:

`E_X: X → Y`

represents states of `X` inside a larger space `Y`.

Embedding does not make all of `Y` valid states of `X`.

---

## 162. State Projection

A projection:

`P_X: X × Y → X`

returns the `X` component from a product state.

Projection and physical reduction are distinct concepts.

---

## 163. State-Space Intersection

For compatible subsets:

`A ⊆ X`

and:

`B ⊆ X`

their intersection is:

`A ∩ B`.

Intersection is defined only when the sets belong to a common ambient space.

---

## 164. State-Space Union

For compatible subsets:

`A ⊆ X`

and:

`B ⊆ X`

their union is:

`A ∪ B`.

A union does not erase the semantic distinctions that generated its subsets.

---

## 165. Disjoint Union

For semantically distinct classification spaces, a disjoint union may be used where required.

This prevents identical machine labels from collapsing different semantic categories.

---

## 166. Tagged State Space

A tagged union may represent heterogeneous states:

`X_tagged = ({A} × X_A) ∪ ({B} × X_B)`.

The tag preserves semantic type.

This construction is appropriate when state alternatives belong to different spaces.

---

## 167. Optional State Space

Optional values should be represented by explicit extension:

`X_optional = X ∪ {NONE}`

with:

`NONE ∉ X`.

This construction is used instead of overloading a valid model value.

---

## 168. Ternary Optionality Rule

For ternary state:

`T_optional = T ∪ {NONE}`.

The distinction is:

`NONE ≠ -1`

`NONE ≠ 0`

`NONE ≠ 1`.

This prevents missingness from corrupting active-neutral semantics.

---

## 169. Validation-State Optionality

If a validation result is not yet available, its absence must remain distinct from:

`UNRESOLVED`.

`UNRESOLVED`

means that a validation process produced an unresolved outcome.

Absence means no result is present.

---

## 170. State-Space Provenance Annotation

A state or parameter may carry provenance metadata.

The annotated object may be represented conceptually as:

`(x, p_prov)`.

The provenance tag does not alter the mathematical value of `x`.

---

## 171. State-Space Version Annotation

Persistent computational state may carry a schema or representation version.

Version identity belongs to the representation layer.

It does not alter the underlying formal state unless the semantic contract itself changes.

---

## 172. FRP Reference State Boundary

FRP provides executable state structures for selected TR mechanisms.

When FRP state is used as a reference, each imported semantic field must be mapped to the corresponding TR-EIF state space explicitly.

FRP state structure does not replace the general TR-EIF state-space definitions.

---

## 173. FRP Phase State

A verified FRP phase field belongs to a computational representation of:

`S^1`.

Wrapped storage does not change its circular semantics.

---

## 174. FRP Ternary State

A verified FRP retained ternary state belongs to:

`T_exec = {-1, 0, 1}`.

The state preserves active `0`.

---

## 175. FRP Ternary Target

A verified FRP phase-derived target belongs to:

`T_target`.

It must remain distinct from:

`T_exec`.

---

## 176. FRP Pending State

A verified FRP pending destination maps into the TR-EIF pending-state semantics.

It represents staged opposite-polarity execution state.

---

## 177. FRP Scheduler State

Verified FRP scheduler variables belong to specialization-specific:

`X_sched`.

Their values do not redefine the general TR-EIF scheduler-state space.

---

## 178. FRP Memory State

Verified retained frequency or related memory variables belong to an implementation-specific subset of:

`X_M`.

They do not imply explicit delayed pairwise phase state.

---

## 179. State-Space Non-Equivalences

The following state-space distinctions are mandatory:

`T ≠ K_R`

`T ≠ K_val`

`T ≠ K_D`

`T ≠ X_energy`

`T ≠ X_force`

`T ≠ X_stress`

`S^1 ≠ K_phys`

`X_phase ≠ X_R`

`X_R ≠ X_Rorder`

`X_Rorder ≠ X_C`

`T_target ≠ T_exec`

`X_pending ≠ T_exec`

`X_req ≠ X_auth`

`X_auth ≠ X_commit`

`X_snap ≠ X_CP`

`X_model ≠ X_num`

`X_EIF ≠ X_TR`

`X_EQ ≠ X_R`

`X_atom ≠ X_cont`.

These inequalities express semantic non-identity even when some spaces share underlying numeric carriers.

---

## 180. Scientific Non-Equivalences Preserved by State Typing

The state-space architecture enforces:

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

`target ≠ executed state`.

---

## 181. State-Space Invariants

The following invariants govern state-space construction throughout TR-EIF.

1. Every state variable belongs to a declared state space.

2. Every state-space component has a defined semantic type.

3. Continuous and discrete state remain separately typed.

4. Circular phase remains an element of `S^1`.

5. The balanced ternary state set remains exactly `T = {-1, 0, 1}`.

6. The canonical ternary notation remains `-1/0/1`.

7. Active neutral `0` remains a valid state.

8. Missingness remains outside the balanced ternary state set.

9. Error state remains outside the balanced ternary state set.

10. Target and executed ternary state remain semantically distinct.

11. Pending destination remains explicit where required.

12. Direct opposite committed transitions remain excluded.

13. Resonance classification remains distinct from ternary state.

14. Resonance-coordinate space remains distinct from phase-order observable space.

15. Local and global states remain distinguishable.

16. Entity identity remains distinct from storage index.

17. Geometry and topology remain separately represented.

18. Invariant and equivariant representations retain separate transformation semantics.

19. Energy, force, stress, phase, resonance, and ternary state remain separately typed.

20. History and memory are explicit when result-affecting.

21. Solver and execution-control state are explicit when result-affecting.

22. Scale identity is explicit.

23. Cross-scale states remain distinct until connected by mappings.

24. Optionality does not overload valid model states.

25. Validation and provenance remain outside physical and ternary state spaces.

---

## 182. Integrated State-Space Architecture

The integrated state architecture can be represented as:

`X_TR-EIF = X_EIF × X_TR × X_int`.

A computational realization may extend this to:

`X_total = X_TR-EIF × X_num × X_ctrl × X_rng`

with only applicable factors present.

For multiscale execution:

`X_total,multi = X_total × X_multi`.

For molecular dynamics:

`X_total,MD = X_MD × X_TR × X_int × X_num × X_ctrl`.

These products are structural decompositions.

They do not imply semantic equivalence among their factors.

---

## 183. Canonical Integration State Chain

The state spaces participating in the principal TR-EIF integration path are:

`X_EIF`

`→ X_EQ`

`→ X_R`

`→ K_R`

`→ T_target`

`→ T_exec`

`→ X_EIF,req`.

Each arrow connects different spaces.

The corresponding mappings are defined in later chapters.

The state-space layer establishes only the domains and codomains required by those mappings.

---

## 184. Separation of Classification and Execution

The resonance classifier produces:

`k_R ∈ K_R`.

A ternary-target mapping produces:

`t_target ∈ T_target`.

The execution mechanism retains:

`t_exec ∈ T_exec`.

These are three distinct state roles:

`resonance classification`

`→ ternary target`

`→ executed ternary state`.

No identity relation is assumed between them.

---

## 185. Separation of Physical and Computational State

A complete implementation may contain both:

`X_phys`

and:

`X_comp`.

The physical or modeled state contains variables belonging to the selected mathematical model.

Computational state contains additional result-affecting execution variables.

The distinction is:

`modeled state ≠ implementation state`.

---

## 186. Separation of State and Artifact

A serialized artifact represents state or a projection of state.

The artifact representation space is not identical to the underlying mathematical state space.

Serialization therefore introduces an additional representation layer.

---

## 187. Separation of State and Validation

Validation evaluates state, transitions, mappings, or artifacts.

Validation result is not part of the validated state unless an explicit supervisory system stores it as control state.

---

## 188. State-Space Construction Rule

Every later TR-EIF state space must be introduced by specifying:

1. state-space name;
2. mathematical carrier;
3. semantic meaning;
4. admissible elements;
5. dimensional type where applicable;
6. topology or metric where required;
7. transformation behavior where required;
8. relation to existing spaces;
9. optionality or invalidity representation where applicable;
10. provenance where applicable.

---

## 189. State Variable Introduction Rule

Every state variable must be defined before use.

The definition must identify the space to which the variable belongs.

For example:

`x ∈ X`

or:

`t_exec ∈ T_exec`.

A variable without a state-space declaration is incomplete.

---

## 190. State-Space Extension Rule

A new model component extends the existing state space through an explicit product, tagged union, function space, graph space, or other defined construction.

No hidden state-space extension is permitted.

---

## 191. State-Space Reduction Rule

A reduced representation requires an explicit projection or reduction mapping.

A reduced state must not be treated as containing information discarded by the reduction.

---

## 192. State-Space Transformation Rule

A transformation of state must preserve the declared transformation law of the state space.

For equivariant representations, the output action is part of the definition.

---

## 193. State-Space Comparison Rule

Comparison between states requires a relation appropriate to the state space.

Examples include:

- exact equality;
- circular equality;
- graph isomorphism or indexed equality;
- numerical metric comparison;
- symmetry equivalence.

No universal comparison rule applies to all TR-EIF state spaces.

---

## 194. State-Space Closure Rule

Before a dynamical or computational model is considered complete, all result-affecting state required by its evolution must appear explicitly in the declared state architecture.

---

## 195. Repository-Wide State Consistency

The state spaces defined in documentation must remain consistent with:

- source implementation;
- schemas;
- tests;
- examples;
- benchmarks;
- validation artifacts.

A schema or implementation field cannot redefine the semantic meaning of a documented state without an explicit model revision.

---

## 196. Foundation for Mathematical Operators

The state spaces defined here provide the domains and codomains for the operators introduced later in Volume 01.

These operators may act on:

- Euclidean state;
- circular state;
- graph state;
- resonance state;
- ternary state;
- equivariant representation;
- multiscale state;
- history state;
- numerical state.

Operator definitions must preserve the state-space distinctions established here.

---

## 197. Foundation for Mathematical Structures

Later structural definitions may combine the state spaces introduced here into:

- dynamical systems;
- graphs;
- manifolds;
- group actions;
- product systems;
- hybrid systems;
- multiscale systems;
- coupled TR-EIF systems.

The existence of these structures does not collapse their component state spaces.

---

## 198. Foundation for Mathematical Mappings

The state architecture supplies the domains and codomains for later mappings including:

`atomic state → local environment`

`interatomic state → equivariant representation`

`equivariant representation → resonance coordinates`

`resonance coordinates → resonance classification`

`resonance state → ternary target`

`ternary target → executed ternary state`

`TR state → EIF update request`

`fine-scale state → coarse-scale state`.

Each mapping remains independently defined.

---

## 199. Foundation for Framework Invariants

The framework invariants developed later depend on the state-space distinctions established here.

An invariant can be evaluated only after the state domain to which it applies is known.

Examples include:

- ternary-domain invariants;
- transition invariants;
- symmetry invariants;
- dimensional invariants;
- conservation invariants;
- state-closure invariants.

---

## 200. Final State-Space Statement

TR-EIF is a multi-space mathematical architecture.

Its central state organization preserves:

`atomic/interatomic state`

`≠ equivariant representation`

`≠ resonance state`

`≠ resonance classification`

`≠ ternary target`

`≠ executed ternary state`

`≠ physical observable`

`≠ numerical state`

`≠ validation state`.

The canonical balanced ternary domain remains:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and active neutral:

`0`.

The principal integration sequence is represented by distinct spaces:

`X_EIF`

`→ X_EQ`

`→ X_R`

`→ K_R`

`→ T_target`

`→ T_exec`

`→ X_EIF,req`.

The mathematical mappings connecting these spaces are introduced separately.

This typed state-space architecture provides the domain structure required for mathematical operators, mathematical structures, mappings, invariants, lemmas, theorems, corollaries, numerical implementations, molecular dynamics, multiscale modeling, and the FLiBe reference model.
