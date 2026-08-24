# Mathematical Mappings

## 1. Purpose

This chapter defines the canonical mapping architecture of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The mappings connect the state spaces, operators, and mathematical structures established in Chapters 01–06.

The purpose of this chapter is to formalize:

- state-to-state mappings;
- state-to-observable mappings;
- local-to-global mappings;
- geometric and graph mappings;
- invariant and equivariant mappings;
- interatomic-to-representation mappings;
- representation-to-resonance mappings;
- resonance-classification mappings;
- resonance-to-ternary mappings;
- ternary execution mappings;
- TR-to-EIF feedback mappings;
- history and memory mappings;
- learning mappings;
- molecular-dynamics mappings;
- multiscale mappings;
- numerical realization mappings;
- artifact and validation mappings.

The governing principle is:

`every semantic transition between mathematical spaces requires an explicit typed mapping`.

No conceptual adjacency is treated as an implicit identity.

---

## 2. General Mapping Definition

A mapping is written:

`F: X → Y`

where:

- `X` is the domain;
- `Y` is the codomain.

For:

`x ∈ X`

the mapped value is:

`F(x) ∈ Y`.

The domain and codomain are part of the mathematical definition of `F`.

---

## 3. Multi-Argument Mapping

A mapping may depend on several typed inputs.

For:

`X_1, ..., X_n`

define:

`F: X_1 × ... × X_n → Y`.

Each argument retains its own semantic role.

For example:

`F(x, h, p)`

may depend separately on:

- current state `x`;
- history `h`;
- parameter state `p`.

---

## 4. Parameterized Mapping

A parameterized mapping may be written:

`F_p: X → Y`

for:

`p ∈ P`.

Equivalently:

`F: X × P → Y`.

Parameter dependence must be explicit whenever the parameter affects the result.

---

## 5. Time-Dependent Mapping

A time-dependent mapping may be:

`F: X × I_t → Y`.

For:

`x ∈ X`

and:

`t ∈ I_t`

the result is:

`F(x, t)`.

Model time remains distinct from execution index and numerical step index.

---

## 6. Execution-Indexed Mapping

A discrete execution mapping may be written:

`F_k: X → Y`

or:

`F: X × N_0 → Y`.

Execution coordinate:

`k`

is not automatically physical time.

---

## 7. Mapping Composition

For:

`F: X → Y`

and:

`G: Y → Z`

the composition is:

`G ∘ F: X → Z`.

For:

`x ∈ X`

the result is:

`G(F(x))`.

Composition is valid only when the codomain of `F` is compatible with the domain of `G`.

---

## 8. Mapping Chain

A sequence:

`X_0 → X_1 → ... → X_n`

is valid only when each arrow corresponds to an explicitly defined mapping:

`F_i: X_(i-1) → X_i`.

The chain does not imply that adjacent state spaces are equivalent.

---

## 9. Identity Mapping

The identity mapping on:

`X`

is:

`Id_X: X → X`

with:

`Id_X(x) = x`.

Identity mapping preserves the complete mathematical object.

---

## 10. Inclusion Mapping

For:

`A ⊆ X`

the inclusion is:

`i_A: A → X`.

The mapping preserves the element while changing the declared ambient space.

---

## 11. Projection Mapping

For product state:

`X = X_1 × ... × X_n`

the projection:

`pi_i: X → X_i`

returns the `i`-th component.

Projection may discard information contained in the other components.

---

## 12. Embedding Mapping

An embedding:

`E: X → Y`

represents elements of `X` inside `Y` while preserving the declared structure.

An embedding is not assumed unless injectivity and structure preservation are established.

---

## 13. Reduction Mapping

A reduction mapping is:

`P_red: X → X_red`.

It produces a reduced representation of the source state.

The reduction must identify:

- retained information;
- discarded information;
- assumptions;
- approximation structure.

---

## 14. Reconstruction Mapping

A reconstruction mapping may be:

`R_rec: X_red × X_aux → X`.

Auxiliary information may be necessary when reduction is non-injective.

---

## 15. Injective Mapping

A mapping:

`F: X → Y`

is injective when:

`F(x_1) = F(x_2)`

implies:

`x_1 = x_2`.

Injectivity preserves distinguishability of source states.

---

## 16. Surjective Mapping

A mapping:

`F: X → Y`

is surjective when every:

`y ∈ Y`

has at least one:

`x ∈ X`

such that:

`F(x) = y`.

---

## 17. Bijective Mapping

A mapping is bijective when it is both injective and surjective.

A bijection admits an inverse:

`F^(-1): Y → X`.

---

## 18. Non-Injective Mapping

A mapping is non-injective when there exist:

`x_1 ≠ x_2`

such that:

`F(x_1) = F(x_2)`.

A non-injective mapping loses source-state distinguishability over the relevant domain.

---

## 19. Information-Loss Mapping

A mapping:

`F: X → Y`

is information-losing over domain `D ⊆ X` when source states in `D` cannot be uniquely reconstructed from the output.

Information loss must be treated as a property of the mapping and domain.

---

## 20. State-to-Observable Mapping

An observable mapping is:

`O: X → Y_obs`.

For state:

`x ∈ X`

the observable is:

`y = O(x)`.

The observable is distinct from retained state unless explicitly stored.

---

## 21. Local Observable Mapping

For local state:

`x_i ∈ X_i`

define:

`O_i: X_i → Y_i`.

A local observable remains associated with its local state scope.

---

## 22. Global Observable Mapping

For complete state:

`x ∈ X`

define:

`O_G: X → Y_G`.

A global observable may aggregate information from many local states.

---

## 23. Local-to-Global Aggregation Mapping

For local states:

`x_1, ..., x_N`

an aggregation mapping may be:

`A_G: X_loc^N → Y_G`.

The mapping must define:

- ordering behavior;
- normalization;
- weights;
- dimensional compatibility.

---

## 24. Global-to-Local Mapping

A global quantity may influence local states through:

`F_G→L: Y_G × X_i → X_i'`.

The mapping must define how global information is distributed or coupled locally.

A global observable is not automatically a local state.

---

## 25. Atomic Configuration Mapping

Let:

`X_conf`

be the atomic configuration space.

A configuration mapping may extract or transform:

- species;
- positions;
- cell state;
- boundary information.

All outputs must retain entity association.

---

## 26. Species Mapping

A species projection is:

`P_species: X_conf → X_species`.

It preserves categorical species identity.

---

## 27. Position Mapping

A position projection is:

`P_pos: X_conf → X_pos`.

The result is the complete coordinate state.

---

## 28. Cell Mapping

For periodic systems:

`P_cell: X_conf → X_cell`.

The result contains the simulation-cell representation.

---

## 29. Relative-Geometry Mapping

For entities `i` and `j`, define:

`P_rel: X_conf × I_atom × I_atom → X_disp`.

The output may be:

`r_ij`.

Periodic geometry requires the declared periodic displacement convention.

---

## 30. Distance Mapping

Define:

`P_dist: X_disp → R_0+`

by:

`P_dist(r_ij) = ||r_ij||`.

Distance is a scalar geometric observable.

---

## 31. Neighborhood Mapping

For entity `i`, define:

`P_Ni: X_conf → P(V)`.

The output is:

`N_i`.

The neighborhood rule may depend on:

- cutoff;
- topology;
- species;
- periodic geometry;
- model parameters.

---

## 32. Interaction-Graph Mapping

Define:

`P_G: X_conf → X_G`.

The mapping constructs an interaction graph from the atomic configuration according to the selected model.

Graph state is not inferred solely from array adjacency.

---

## 33. Edge-Feature Mapping

For graph edge:

`(i, j)`

define:

`P_edge: X_conf × E_G → X_edge`.

Possible outputs include:

- displacement;
- distance;
- species pair;
- geometric descriptors;
- learned edge features.

---

## 34. Node-Feature Mapping

Define:

`P_node: X_conf × V → X_node`.

The output associates a typed node representation with an entity.

---

## 35. Local-Environment Mapping

For entity `i`:

`P_env,i: X_conf × X_G → X_env`.

The mapping constructs the local environment from:

- central entity;
- neighborhood;
- geometry;
- species;
- topology.

---

## 36. Permutation Action Mapping

For:

`pi ∈ S_N`

define:

`rho_perm(pi): X_indexed → X_indexed`.

This mapping changes indexed representation while preserving semantic entity associations.

---

## 37. Translation Action Mapping

For:

`a ∈ R^3`

define:

`rho_trans(a): X_pos → X_pos`.

For each entity:

`r_i → r_i + a`.

---

## 38. Rotation Action Mapping

For:

`Q ∈ SO(3)`

define:

`rho_rot(Q): X_vec → X_vec`.

For vector:

`v`

the action is:

`v → Qv`.

---

## 39. Orthogonal Action Mapping

For:

`Q ∈ O(3)`

define:

`rho_orth(Q)`.

This permits both proper and improper orthogonal transformations.

---

## 40. Euclidean Action Mapping

For:

`g = (Q, a) ∈ E(3)`

define:

`rho_E3(g): X_pos → X_pos`

with:

`r_i → Qr_i + a`.

---

## 41. Invariant Mapping

A mapping:

`F_inv: X → Y`

is invariant under group:

`G_sym`

when:

`F_inv(rho_X(g)x) = F_inv(x)`

for all admissible:

`g ∈ G_sym`.

---

## 42. Equivariant Mapping

A mapping:

`F_eq: X → Y`

is equivariant when:

`F_eq(rho_X(g)x) = rho_Y(g)F_eq(x)`.

The output action:

`rho_Y`

must be defined.

---

## 43. Permutation-Invariant Mapping

For:

`pi ∈ S_N`

a global mapping is permutation invariant when:

`F(rho_X(pi)x) = F(x)`.

---

## 44. Permutation-Equivariant Mapping

An indexed mapping is permutation equivariant when:

`F(rho_X(pi)x) = rho_Y(pi)F(x)`.

---

## 45. Translation-Invariant Mapping

A mapping is translation invariant when:

`F(rho_trans(a)x) = F(x)`.

---

## 46. Translation-Equivariant Mapping

A mapping is translation equivariant when its output transforms according to a declared translation action.

---

## 47. Rotation-Invariant Mapping

A mapping is rotation invariant when:

`F(rho_rot(Q)x) = F(x)`.

---

## 48. Rotation-Equivariant Mapping

A mapping is rotation equivariant when:

`F(rho_rot(Q)x) = rho_Y(Q)F(x)`.

---

## 49. E(3)-Equivariant Mapping

For:

`g ∈ E(3)`

define equivariance by:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

The exact output representation must be specified.

---

## 50. Interatomic-to-Representation Mapping

Define the EIF representation mapping:

`P_E: X_EIF → X_rep`.

The representation space may contain:

`X_rep = X_INV × X_EQ`.

The mapping may depend on:

- atomic configuration;
- graph topology;
- local environments;
- species;
- learned parameters.

---

## 51. Interatomic-to-Invariant Mapping

Define:

`P_INV: X_EIF → X_INV`.

Its output is invariant under the declared transformation group.

---

## 52. Interatomic-to-Equivariant Mapping

Define:

`P_EQ: X_EIF → X_EQ`.

Its output transforms under the declared output action.

---

## 53. Local Message Mapping

For edge:

`(i, j)`

define:

`M_ij: X_node × X_node × X_edge → X_msg`.

The message is a local representation object.

---

## 54. Message Aggregation Mapping

For entity `i`:

`Agg_i: X_msg^(|N_i|) → X_msg,agg`.

The aggregation must satisfy the required permutation behavior.

---

## 55. Node-Update Mapping

Define:

`U_i: X_node × X_msg,agg → X_node'`.

The update maps local representation state into a new representation state.

---

## 56. Message-Passing Layer Mapping

A complete message-passing layer may be represented as:

`MP: X_graphrep → X_graphrep'`.

The mapping is composed from:

- message generation;
- aggregation;
- node update.

---

## 57. Equivariant Message-Passing Mapping

An equivariant message-passing mapping must satisfy the declared group relation across the complete composition.

Equivariance of one submapping is insufficient if another submapping violates the required transformation law.

---

## 58. Invariant Readout Mapping

Define:

`R_INV: X_rep → Y_INV`.

The output is invariant under the declared transformation actions.

---

## 59. Equivariant Readout Mapping

Define:

`R_EQ: X_rep → Y_EQ`.

The output transforms under the declared output action.

---

## 60. Energy Mapping

A scalar interatomic energy mapping is:

`E_model: X_EIF → R`

or:

`E_model: X_rep → R`

depending on model architecture.

The domain must be explicit.

---

## 61. Local Energy Mapping

A local energy mapping may be:

`E_i: X_env,i → R`.

A total energy may then be constructed by an aggregation mapping.

---

## 62. Total Energy Mapping

For local energy contributions:

`E_i`

define:

`E_total = sum_i E_i`.

The aggregation must preserve permutation invariance and dimensional consistency.

---

## 63. Force Mapping from Energy

For differentiable:

`E_total: X_pos → R`

define:

`F_force: X_pos → X_force`

through:

`F_i = -partial E_total / partial r_i`.

This is a derivative mapping from scalar energy to vector force.

---

## 64. Stress Mapping

Define:

`F_stress: X_stress,src → X_stress`.

The source may include:

- positions;
- forces;
- cell;
- momentum;
- model-specific interaction terms.

The exact relation is defined by the selected stress convention.

---

## 65. Interatomic-to-Resonance Mapping

The integrated architecture requires an explicit path from EIF state to resonance state.

A direct form is:

`F_E→R: X_EIF → X_R`.

A factorized form is:

`X_EIF → X_EQ → X_R`.

---

## 66. Equivariant-to-Resonance Mapping

Define:

`P_ER: X_EQ → X_R`.

This mapping is the principal bridge between the EIF representation layer and the Ternary Resonant layer.

---

## 67. Extended Equivariant-to-Resonance Mapping

Where additional state is required:

`P_ER: X_EQ × X_H × X_G × L × P → X_R`.

Only required arguments are included in a specific model.

---

## 68. Symmetry Contract of Resonance Mapping

For a resonance mapping:

`P_ER`

the transformation behavior must be explicit.

Possible cases include:

- invariant resonance coordinates;
- equivariant resonance coordinates;
- mixed invariant/equivariant coordinates.

The output action must be defined accordingly.

---

## 69. Locality Contract of Resonance Mapping

A local resonance mapping may be:

`P_ER,i: X_env,i → X_R,i`.

A global resonance mapping may instead depend on the complete representation state.

The locality class must be stated explicitly.

---

## 70. Scale Contract of Resonance Mapping

For scale:

`ell`

define:

`P_ER^(ell): X_EQ^(ell) → X_R^(ell)`.

Cross-scale resonance mapping requires an additional explicit transfer relation.

---

## 71. Resonance Projection Mapping

The canonical resonance projection remains:

`P_R: X_src → X_R`.

For:

`x ∈ X_src`

the output is:

`r = P_R(x)`.

---

## 72. Resonance-Window Mapping

A model may construct a resonance window through:

`F_WR: X_param × X_H × X_G × L → P(X_R)`.

The output is a subset:

`W_R ⊂ X_R`.

Not every model requires all listed arguments.

---

## 73. Static Resonance Window

A static window is fixed for a declared model configuration.

It may be represented as:

`W_R = constant subset of X_R`.

---

## 74. History-Dependent Resonance Window

A history-dependent window may be:

`W_R = F_WR(h)`.

Here:

`h ∈ X_H`.

The current resonance coordinate alone does not determine the window.

---

## 75. Topology-Dependent Resonance Window

A topology-dependent window may be:

`W_R = F_WR(g_top)`.

Here:

`g_top ∈ X_G`.

---

## 76. Scale-Dependent Resonance Window

A scale-dependent family is:

`W_R^(ell)`

for:

`ell ∈ L`.

---

## 77. Resonance Classification Mapping

The minimal classifier is:

`C_R: X_R → K_R`

where:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

---

## 78. Extended Resonance Classification Mapping

For history-dependent or state-dependent classification:

`C_R: X_R × X_H × X_aux → K_R`.

All required dependencies must be explicit.

---

## 79. Resonance-Boundary Mapping

A boundary-distance mapping may be:

`D_boundary: X_R → R_0+`.

It measures distance to:

`∂W_R`

under a declared resonance-space metric.

---

## 80. Resonance Membership Mapping

Define:

`M_R: X_R → {false, true}`.

It returns whether:

`r ∈ W_R`.

Membership and boundary classification remain separately definable.

---

## 81. Resonance Classification Is Not Ternary Mapping

The mapping:

`C_R: X_R → K_R`

does not map into:

`T`.

Therefore resonance classification is not the ternary-target mapping.

---

## 82. Resonance-to-Ternary Target Mapping

Define:

`P_RT: X_R → T_target`.

This mapping assigns a ternary target from a resonance state under an explicitly defined model rule.

---

## 83. Classification-Assisted Ternary Mapping

A model may use:

`P_KT: K_R × X_aux → T_target`.

This is a distinct mapping from the resonance classifier itself.

The existence of three resonance classes does not create an implicit identity with:

`-1/0/1`.

---

## 84. History-Dependent Ternary Target Mapping

Define:

`P_RT,H: X_R × X_H → T_target`.

History-dependent target assignment must include history in the domain.

---

## 85. Hysteretic Ternary Target Mapping

A hysteretic target mapping may depend on retained memory:

`P_RT,M: X_R × X_M → T_target`.

The same current resonance state may produce different targets for different memory states.

---

## 86. Phase-to-Resonance Mapping

Where oscillator phase contributes to resonance coordinates:

`P_phase→R: X_phase × X_aux → X_R`.

The exact construction is model-specific.

Phase state does not equal resonance state.

---

## 87. Phase-to-Ternary Target Mapping

A specialization may define:

`P_phase→T: X_phase → T_target`

or:

`P_phase→T: X_phase × X_aux → T_target`.

Such a mapping is an upstream target generator.

It does not bypass ternary execution semantics.

---

## 88. Phase-Order Mapping

Define:

`P_order: X_phase → [0, 1]`

by:

`P_order(Theta) = |(1/N) sum_j exp(i theta_j)|`.

The output is phase-order magnitude:

`R`.

---

## 89. Coherence Mapping

Define a separate mapping:

`P_coh: X → X_C`.

Its definition depends on the selected coherence model.

The architecture preserves:

`P_order ≠ P_coh`.

---

## 90. Synchronization Mapping

A synchronization classifier or observable may be:

`P_sync: X → K_sync`

or:

`P_sync: X → Y_sync`.

It remains separate from resonance and phase-locking mappings.

---

## 91. Phase-Locking Mapping

Define:

`P_lock: X_phase × X_H → K_lock`

when locking is assessed over trajectory history.

This mapping remains distinct from resonance classification.

---

## 92. Ternary Execution Mapping

The ternary execution layer maps:

`E_T: X_Texec × X_ctrl → X_Texec`.

It updates execution state according to:

- target;
- current state;
- pending destination;
- control state;
- transition invariants.

---

## 93. Direct-State Retention Mapping

For admissible retention:

`H_T: T_exec → T_exec`

with:

`H_T(t) = t`.

---

## 94. First-Leg Mapping

For opposite target:

`F_leg1: T_exec × T_target → T_exec × X_pending`.

The canonical opposite-polarity cases are:

`F_leg1(-1, 1) = (0, 1)`

`F_leg1(1, -1) = (0, -1)`.

---

## 95. Second-Leg Mapping

Define:

`F_leg2: T_exec × X_pending × X_auth → T_exec × X_pending`.

The mapping is admissible only when:

- `t_exec = 0`;
- pending destination is valid;
- authorization permits completion.

---

## 96. Pending-Clear Mapping

After successful second-leg completion:

`Clear_pending: X_pending → X_pending`

maps the completed route state to:

`NONE`.

---

## 97. Adjacent Ternary Mapping

For non-opposite target transitions, an execution mapping may permit:

`-1 → 0`

`0 → -1`

`0 → 1`

`1 → 0`

under the selected control semantics.

---

## 98. Forbidden Direct Mapping

No valid commit mapping has either:

`F(-1, 1) = 1`

or:

`F(1, -1) = -1`

in one direct committed event.

---

## 99. Neutral Retention Mapping

The mapping:

`F_hold(0) = 0`

remains admissible.

No fixed maximum neutral residence duration exists at the framework level.

---

## 100. Target-to-Executed Mapping Boundary

There is no universal identity mapping:

`Id: T_target → T_exec`.

Target and executed state share values but not semantic role.

Execution mediates the relation between them.

---

## 101. Request Mapping

A state update request is generated through:

`F_req: X → X_req`.

The output describes a requested change.

---

## 102. Authorization Mapping

Authorization is:

`F_auth: X_req × X_ctrl × X → X_auth`.

It evaluates the requested update under the applicable constraints.

---

## 103. Commit Mapping

A commit is:

`F_commit: X × X_auth → X`.

The output is retained post-commit state.

---

## 104. Request-Authorization-Commit Chain

The computational mapping chain is:

`X`

`→ X_req`

`→ X_auth`

`→ X`.

Each step is distinct.

---

## 105. TR-to-EIF Feedback Mapping

Define:

`F_TR→E: X_TR × X_EIF × X_aux → X_EIF,req`.

The output is an EIF update request.

It is not committed EIF state.

---

## 106. Ternary-to-EIF Mapping

Where executed ternary state participates in EIF feedback:

`F_T→E: T_exec × X_EIF × X_aux → X_EIF,req`.

The mapping must define:

- physical interpretation;
- symmetry behavior;
- locality;
- scale;
- dimensions.

---

## 107. Resonance-to-EIF Mapping

Where resonance state directly affects EIF feedback:

`F_R→E: X_R × X_EIF × X_aux → X_EIF,req`.

Resonance coordinates must not be interpreted as force or energy without an explicit typed output relation.

---

## 108. TR Composite Feedback Mapping

A composite feedback mapping may depend on:

- resonance state;
- ternary state;
- memory;
- interatomic state.

For example:

`F_TR→E: X_R × T_exec × X_M × X_EIF → X_EIF,req`.

---

## 109. EIF Update Authorization Mapping

Define:

`F_Eauth: X_EIF,req × X_EIF × X_ctrl → X_EIF,auth`.

The mapping evaluates:

- domain constraints;
- symmetry constraints;
- dimensional constraints;
- execution guards.

---

## 110. EIF Commit Mapping

Define:

`F_Ecommit: X_EIF × X_EIF,auth → X_EIF`.

The result is retained updated EIF state.

---

## 111. Closed-Loop TR-EIF Mapping Chain

The integrated closed-loop chain is:

`X_EIF`

`→ X_EQ`

`→ X_R`

`→ K_R`

`→ T_target`

`→ T_exec`

`→ X_EIF,req`

`→ X_EIF,auth`

`→ X_EIF,next`.

Every arrow denotes a distinct mapping or execution relation.

---

## 112. Forward Composite Mapping

Where domains align:

`F_forward = P_RT ∘ P_ER ∘ P_EQ`.

The output belongs to:

`T_target`.

The composition does not include ternary execution.

---

## 113. Full TR Forward Mapping

A complete TR forward interface may be:

`F_TR: X_EIF × X_H × X_M × P → T_target × X_TR,aux`.

The exact auxiliary state depends on the selected model.

---

## 114. Feedback Composite Mapping

A feedback path may be:

`F_Ecommit ∘ F_Eauth ∘ F_TR→E`.

This composition requires the intermediate request and authorization objects to remain explicit in the formal definition.

---

## 115. Integrated State-Evolution Mapping

A complete discrete integrated step may be written:

`F_TR-EIF: X_TR-EIF × U × P → X_TR-EIF`.

The internal composition must preserve all component state semantics.

---

## 116. Continuous TR-EIF Evolution Mapping

Where selected components evolve continuously:

`f_TR-EIF: X_TR-EIF × U × P × I_t → T(X_TR-EIF)`.

Discrete ternary state changes remain governed by discrete transition semantics.

---

## 117. Hybrid TR-EIF Evolution Mapping

A hybrid model combines:

- continuous flow mapping;
- event mapping;
- target mapping;
- discrete execution mapping;
- feedback mapping.

The mathematical roles remain distinct.

---

## 118. History Mapping

A history extraction mapping may be:

`P_H: X_trajectory → X_H`.

The output contains the trajectory information required by the model.

---

## 119. History Shift Mapping

For execution advance:

`Shift_H: X_H × X_new → X_H`.

The mapping updates the retained history representation.

---

## 120. Delay Access Mapping

Define:

`D_tau: X_H → X_delayed`.

For a function-history representation:

`D_tau(h) = h(-tau)`.

The delay value must lie within the available history domain.

---

## 121. Memory Update Mapping

Define:

`F_M: X_M × X → X_M`.

The memory state evolves according to the selected model.

---

## 122. Relaxation Mapping

A discrete relaxation mapping may be:

`F_relax(x, x_target) = x + alpha(x_target - x)`.

The parameter:

`alpha`

and admissible domain must be specified.

---

## 123. Hysteresis Mapping

A hysteretic mapping is:

`F_hys: X × X_M → Y × X_M`.

The retained memory affects the output.

---

## 124. Adaptive Parameter Mapping

A parameter that evolves may be updated through:

`F_adapt: P_dyn × X → P_dyn`.

Once evolving and result-affecting, it is part of state.

---

## 125. Learning Model Mapping

A trainable model is:

`F_theta: X_input → Y_output`

with:

`theta_param ∈ Theta`.

The mapping is parameterized by learned state.

---

## 126. Dataset Mapping

A data-processing mapping may be:

`P_data: D_raw → D_train`.

The transformation must preserve the semantics required by the learning problem.

---

## 127. Label Mapping

A reference label mapping may be:

`P_label: D → Y_ref`.

The output type depends on the supervised learning target.

---

## 128. Loss Mapping

A loss functional is:

`L: Theta × D → R`.

It maps trainable parameters and data into a scalar objective.

---

## 129. Multi-Component Loss Mapping

For components:

`L_1, ..., L_m`

define:

`L_total = sum_j lambda_j L_j`.

The weights:

`lambda_j`

must be defined explicitly.

---

## 130. Energy-Loss Mapping

For predicted and reference energy:

`E_pred`

and:

`E_ref`

an energy loss maps:

`(E_pred, E_ref) → R_0+`.

The exact norm or metric is defined in Volume 04.

---

## 131. Force-Loss Mapping

A force loss maps:

`(F_pred, F_ref) → R_0+`.

The mapping must preserve vector and dimensional semantics.

---

## 132. Stress-Loss Mapping

A stress loss maps:

`(sigma_pred, sigma_ref) → R_0+`.

The tensor comparison convention must be explicit.

---

## 133. Ternary-Regularization Mapping

A ternary regularization mapping is:

`Omega_T: X_feat → R`.

It acts on the declared feature or target representation.

It does not modify the canonical executed ternary state domain.

---

## 134. Resonance-Regularization Mapping

Define:

`Omega_R: X_R → R`

or a more general mapping over resonance trajectories.

Its interpretation remains an optimization term.

---

## 135. Equivariance-Residual Mapping

Define:

`Res_EQ: G_sym × X → R_0+`

through comparison of:

`F(rho_X(g)x)`

and:

`rho_Y(g)F(x)`.

---

## 136. Optimization Mapping

A generic optimizer mapping is:

`Opt: Theta × X_opt × X_grad → Theta × X_opt`.

The optimizer state remains explicit.

---

## 137. Training Mapping

A training process may be represented as:

`Train: D × Theta_init × X_opt,init → Theta_trained × X_opt,final`.

This is an iterative computational mapping.

---

## 138. Model-to-Energy Mapping

A trained EIF model may map:

`X_EIF → R`

through:

`E_theta`.

---

## 139. Model-to-Force Mapping

For differentiable energy model:

`E_theta`

the force mapping is obtained through coordinate differentiation.

This connects learned parameter state to molecular-dynamics force state.

---

## 140. Molecular-Dynamics State Mapping

A molecular-dynamics step is:

`Phi_MD: X_MD → X_MD`.

Its exact form depends on:

- equations of motion;
- integrator;
- timestep;
- thermostat/barostat state.

---

## 141. Position Update Mapping

For a selected integrator:

`F_pos: X_pos × X_mom × X_aux → X_pos`.

The precise mapping belongs to Volume 05.

---

## 142. Momentum Update Mapping

Define:

`F_mom: X_mom × X_force × X_aux → X_mom`.

The exact update depends on the integrator.

---

## 143. Force Evaluation Mapping

Define:

`F_eval: X_EIF × Theta → X_force`.

The force may be generated from a learned energy model or another declared interatomic force model.

---

## 144. Thermostat Mapping

A thermostat update maps:

`X_MD × X_thermostat → X_MD × X_thermostat`.

Its exact structure belongs to the selected thermostat model.

---

## 145. Barostat Mapping

A barostat update maps:

`X_MD × X_barostat → X_MD × X_barostat`.

Cell and momentum transformations must follow the selected model.

---

## 146. Periodic-Wrapping Mapping

Define:

`P_wrap: X_pos × X_cell → X_pos,wrapped`.

Wrapped coordinate and unwrapped physical trajectory remain distinct representations.

---

## 147. Neighbor-List Mapping

Define:

`P_NL: X_conf × P_NL → X_neighborlist`.

The output is a computational acceleration structure.

---

## 148. Neighbor-List Refresh Mapping

Define:

`F_refresh: X_neighborlist × X_conf → X_neighborlist`.

The update condition belongs to the neighbor-list policy.

---

## 149. MD-to-Observable Mapping

Define:

`O_MD: X_MD → Y_obs`.

Possible observables include:

- energy;
- temperature;
- pressure;
- structural descriptors.

History-dependent transport observables require extended domains.

---

## 150. Trajectory-to-Transport Mapping

A transport mapping may be:

`P_transport: X_H,MD → Y_transport`.

The exact form depends on the selected transport coefficient.

---

## 151. Time-Correlation Mapping

Define:

`P_corr: X_H,obs × Tau → Y_corr`.

The output is a time-correlation quantity over a declared averaging convention.

---

## 152. Multiscale Mapping Family

For scale set:

`L`

define mappings:

`M_(a→b): X^(ell_a) → X^(ell_b)`.

Each mapping is individually typed.

---

## 153. Electronic-to-Interatomic Mapping

Define:

`M_elec→EIF: X_elec → X_EIF`.

The mapping must identify:

- transferred observables;
- approximation;
- closure;
- information loss;
- units.

---

## 154. Interatomic-to-Atomistic Mapping

Where EIF representation is used inside molecular dynamics:

`M_EIF→atom: X_EIF → X_atom,model`.

The output supplies the interatomic model state required by atomistic evolution.

---

## 155. Atomistic-to-Mesoscale Mapping

Define:

`M_atom→meso: X_atom × X_H → X_meso`.

History may be required for coarse observables or constitutive inference.

---

## 156. Mesoscale-to-Continuum Mapping

Define:

`M_meso→cont: X_meso → X_cont`.

Closure information must be explicit.

---

## 157. Continuum-to-Engineering Mapping

Define:

`M_cont→eng: X_cont → X_eng`.

The target variables must be specified by the engineering model.

---

## 158. Coarse-Graining Mapping

A coarse-graining map:

`C_G: X_fine → X_coarse`

is generally non-injective.

Its information loss must be characterized.

---

## 159. Refinement Mapping

A refinement map:

`R_G: X_coarse × X_closure → X_fine,rep`

constructs a fine-scale representation from coarse state and closure information.

---

## 160. Closure Mapping

Define:

`C_close: X_coarse × X_aux → X_closure`.

The closure mapping supplies information unavailable from the reduced state alone.

---

## 161. Uncertainty Transfer Mapping

Define:

`M_U: X_U^(ell_a) × X^(ell_a) → X_U^(ell_b)`.

The uncertainty representation at the destination scale may differ from the source representation.

---

## 162. Transport-Coefficient Transfer Mapping

A coefficient transfer may be:

`M_transport: Y_transport^(ell_a) → Y_transport^(ell_b)`.

Its physical assumptions and normalization must be explicit.

---

## 163. Thermodynamic Mapping

A thermodynamic mapping may connect state variables under an explicitly defined relation.

For example:

`F_thermo: X_thermo → Y_thermo`.

No generic thermodynamic mapping is assumed without a selected model.

---

## 164. FLiBe Composition Mapping

The FLiBe reference model will define mappings from composition state into:

- atomic configuration;
- interatomic parameters;
- thermodynamic reference state.

These mappings are specialized in Volume 07.

---

## 165. FLiBe Interatomic Mapping

Define at the reference-model level:

`M_FLiBe,int: X_FLiBe → X_EIF`.

The exact source fields and parameterization belong to Volume 07.

---

## 166. FLiBe Resonance Mapping

A FLiBe-specific resonance mapping will have the form:

`M_FLiBe,R: X_FLiBe,struct × X_EIF → X_R`.

The resonance coordinates remain explicitly defined.

---

## 167. FLiBe Ternary Mapping

A FLiBe-specific ternary interpretation will map a declared resonance or structural state into:

`T_target`

through an explicit model rule.

No direct identification is assumed.

---

## 168. FLiBe Multiscale Mapping

A reference coolant model may map:

`X_FLiBe,atom → X_FLiBe,meso → X_FLiBe,cont`.

The exact mappings are defined in Volume 07.

---

## 169. Numerical Encoding Mapping

A mathematical state may be encoded as:

`Enc: X_math → X_num`.

The mapping defines how mathematical values are represented computationally.

---

## 170. Numerical Decoding Mapping

Define:

`Dec: X_num,valid → X_math`.

For lossless encoding:

`Dec(Enc(x)) = x`.

For approximate encoding, a declared equivalence relation is required.

---

## 171. Floating-Point Mapping

A real-valued mathematical quantity may be mapped into a floating representation through:

`Enc_fp: X_real → X_fp`.

The mapping is finite-precision and generally non-injective.

---

## 172. Fixed-Point Mapping

A fixed-point encoding may be:

`Enc_fx: X_real → X_int`.

Scaling, rounding, and saturation must be explicit.

---

## 173. Quantization Mapping

A quantizer is:

`Q_num: X_cont → X_quant`.

Quantization remains distinct from:

`P_RT`.

Therefore:

`quantization ≠ ternary classification`.

---

## 174. Phase Encoding Mapping

A phase may be encoded through:

`Enc_phase: S^1 → X_phase,num`.

The encoding must preserve circular equivalence.

---

## 175. Ternary Encoding Mapping

A ternary encoding is:

`Enc_T: T → X_T,num`.

The mapping must be injective over:

`{-1, 0, 1}`.

The value `0` must remain distinguishable from invalid or missing representation.

---

## 176. Optional-Value Encoding Mapping

For optional state:

`X_optional = X ∪ {NONE}`

the encoding must distinguish:

`NONE`

from every valid:

`x ∈ X`.

---

## 177. Error Encoding Mapping

An error representation maps into a separate error space:

`Enc_err: X_error → X_err,serialized`.

Error encoding must not reuse valid ternary state values as error markers.

---

## 178. Serialization Mapping

Define:

`Ser: X_art → B_ser`.

The mapping converts a typed artifact into a serialized representation.

---

## 179. Deserialization Mapping

Define:

`Des: B_ser,valid → X_art`.

A valid round trip may satisfy:

`Des(Ser(x)) ≡ x`.

---

## 180. Snapshot Mapping

Define:

`P_snap: X_comp → X_snap`.

A snapshot may contain only a selected projection of computational state.

---

## 181. Checkpoint Mapping

Define:

`P_CP: X_comp → X_CP`.

The mapping must include all state required for the declared restart scope.

---

## 182. Restore Mapping

Define:

`Restore: X_CP,valid → X_comp`.

Restore reconstructs retained state without performing model evolution.

---

## 183. Trace Mapping

Define:

`P_trace: X_exec → X_trace`.

The trace mapping extracts the state and event evidence required by the trace contract.

---

## 184. Event Mapping

A state-dependent event mapping is:

`P_event: X → X_event`.

The event remains distinct from the committed transition that may follow.

---

## 185. Validation Mapping

Define:

`V: X_val → K_val`

where:

`K_val = {PASS, FAIL, UNRESOLVED}`.

The codomain is distinct from:

`T`.

---

## 186. Invariant Validation Mapping

For invariant predicate:

`I`

define:

`V_I: X → K_val`.

The validator returns:

`PASS`

when the invariant is satisfied and:

`FAIL`

when violated.

---

## 187. Numerical Validation Mapping

A numerical validator may be:

`V_num: X_num × X_ref × P_tol → K_val`.

The tolerance structure must be explicit.

---

## 188. Equivariance Validation Mapping

Define:

`V_EQ: G_sym × X × P_tol → K_val`.

The validator compares:

`F(rho_X(g)x)`

with:

`rho_Y(g)F(x)`.

---

## 189. Conservation Validation Mapping

Define:

`V_cons: X_H × P_tol → K_val`.

The validator evaluates the selected conserved quantity over the trajectory.

---

## 190. Ternary Transition Validation Mapping

Define:

`V_transition: X_trace → K_val`.

It must detect committed direct opposite transitions:

`-1 → 1`

and:

`1 → -1`.

---

## 191. Pending Route Validation Mapping

Define:

`V_pending: X_trace → K_val`.

The mapping verifies:

- first-leg execution;
- pending-state retention;
- separate second-leg completion.

---

## 192. Active-Neutral Validation Mapping

Define:

`V_zero: X_trace × X_schema → K_val`.

The validator confirms that:

`0`

is represented and processed as an active valid ternary state.

---

## 193. Resonance-Ternary Separation Mapping

A validator may inspect schema or execution representation through:

`V_RTsep: X_art → K_val`.

It confirms that:

`K_R`

and:

`T`

remain separately typed.

---

## 194. R-C Separation Mapping

Define:

`V_RC: X_art → K_val`.

The validator checks that phase-order and coherence observables remain distinct where both are present.

---

## 195. Delay-Lag Separation Mapping

Define:

`V_DL: X_model → K_val`.

It checks that temporal delay uses explicit history state and phase lag remains an angular interaction parameter.

---

## 196. Dimensional Validation Mapping

Define:

`V_dim: X_expr → K_val`.

The mapping evaluates dimensional compatibility of the declared physical expression.

---

## 197. Mapping Provenance

Every significant mapping may be associated with:

`p_prov ∈ P_prov`.

Examples include:

- classical transformation mapping — `PRIMARY_SOURCE`;
- derived force mapping — `DERIVED`;
- calibrated resonance mapping — `CALIBRATED`;
- TR-EIF integration mapping — `AUTHOR_DEFINED`;
- benchmark transformation — `BENCHMARK`;
- validation fixture mapping — `TEST_FIXTURE`.

---

## 198. Author-Defined Mapping

A TR-EIF-specific mapping is marked:

`AUTHOR_DEFINED`

when it introduces framework-specific semantics.

Examples include:

- resonance-to-ternary target mapping;
- neutral-mediated execution mapping;
- TR-to-EIF feedback mapping;
- integrated multiscale coupling mapping.

---

## 199. Derived Mapping

A mapping mathematically constructed from previously defined mappings may be:

`DERIVED`.

Its derivation must be traceable through composition or calculation.

---

## 200. Calibrated Mapping

A mapping containing calibrated parameters retains:

`CALIBRATED`

provenance for those parameterized components.

---

## 201. Mapping Traceability

Every important mapping should admit:

`mapping`

`→ domain`

`→ codomain`

`→ definition`

`→ provenance`

`→ implementation`

`→ output state or observable`

`→ validation evidence`.

---

## 202. Mapping Domain Validation

Before application:

`x ∈ X`

must hold for:

`F: X → Y`.

Out-of-domain input cannot be silently accepted as valid semantic input.

---

## 203. Mapping Codomain Validation

For valid input:

`x ∈ X`

a valid mapping result must satisfy:

`F(x) ∈ Y`.

A result outside `Y` violates the mapping contract.

---

## 204. Mapping Dimensional Validation

A physical mapping must define the dimensional relation between input and output.

If:

`F: X_q → X_y`

then the transformation from:

`dim(q)`

to:

`dim(y)`

must be mathematically valid.

---

## 205. Mapping Symmetry Validation

An invariant or equivariant mapping must satisfy its declared transformation relation.

No symmetry property follows from naming alone.

---

## 206. Mapping Locality Validation

A mapping declared local must depend only on the state contained in its declared neighborhood or locality domain.

---

## 207. Mapping Scale Validation

A scale-dependent mapping must preserve explicit source and target scale identity.

---

## 208. Mapping History Validation

A history-dependent mapping must include sufficient history state in its domain.

---

## 209. Mapping Memory Validation

A memory-dependent mapping must include retained memory state or an equivalent complete state representation.

---

## 210. Mapping Determinism

A deterministic mapping produces one declared output for each complete admissible input.

Hidden result-affecting state violates deterministic mapping closure.

---

## 211. Mapping Stochasticity

A stochastic mapping must include explicit random state or probability structure.

---

## 212. Exact Mapping Equality

Two mappings:

`F`

and:

`G`

are exactly equal on domain:

`D`

when:

`F(x) = G(x)`

for every:

`x ∈ D`.

---

## 213. Mapping Equivalence

Two mappings may be semantically equivalent under relation:

`≡`

when:

`F(x) ≡ G(x)`

for every admissible:

`x`.

The equivalence relation must be defined.

---

## 214. Numerical Mapping Equivalence

Numerical realizations may be compared through:

`d(F_num(x), G_num(x)) ≤ epsilon`.

This is a numerical equivalence relation, not exact mathematical equality.

---

## 215. Mapping Commutativity

For compatible mappings:

`F`

and:

`G`

a commuting relation is:

`F ∘ G = G ∘ F`.

Commutativity is never assumed without definition or proof.

---

## 216. Symmetry-Commuting Diagram

Equivariance can be represented by the commuting relation:

`F ∘ rho_X(g) = rho_Y(g) ∘ F`.

This is equivalent to:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

---

## 217. Invariance Diagram

Invariance may be expressed as:

`F ∘ rho_X(g) = F`.

---

## 218. Mapping Preservation of Ternary Domain

Every mapping producing:

`T_target`

or:

`T_exec`

must output exactly one of:

`-1`

`0`

`1`.

No other value is admissible.

---

## 219. Mapping Preservation of Active Neutral

Any mapping into:

`T`

must treat:

`0`

as a valid semantic state.

The value must not be overloaded as missingness or error.

---

## 220. Mapping Preservation of Neutral-Mediated Execution

No mapping with commit authority may collapse:

`-1 → 0 → 1`

into:

`-1 → 1`.

Likewise for the opposite direction.

---

## 221. Mapping Preservation of Independent Legs

The first and second legs remain separate mappings or separate events within one stateful execution mapping.

---

## 222. Mapping Preservation of Target/Execution Separation

A mapping producing:

`t_target`

must not silently overwrite:

`t_exec`.

---

## 223. Mapping Preservation of Resonance/Ternary Separation

A resonance classifier maps to:

`K_R`.

A ternary mapping maps to:

`T`.

The two codomains remain distinct.

---

## 224. Mapping Preservation of Phase/Resonance Separation

A phase mapping into resonance space is explicit.

Phase itself is not automatically a resonance coordinate.

---

## 225. Mapping Preservation of Phase Order/Coherence Separation

A phase-order mapping and a coherence mapping retain distinct codomains and definitions.

Therefore:

`R(t) ≠ C(t)`.

---

## 226. Mapping Preservation of Delay/Phase-Lag Separation

A delayed-state mapping accesses history.

A phase-lag mapping modifies phase interaction.

The two mapping classes remain distinct.

---

## 227. Mapping Preservation of Geometry/Ternary Separation

A geometric group-action mapping does not automatically alter ternary polarity.

---

## 228. Mapping Preservation of Phase/Force Separation

A phase interaction mapping does not become a mechanical-force mapping without an explicit interatomic physical relation.

---

## 229. Mapping Preservation of Phase/Bond Separation

A phase-relation mapping does not become a chemical-bond mapping without an explicit interatomic definition.

---

## 230. Mapping Preservation of Ternary/Energy Separation

No mapping may interpret ternary state as energy without an explicit independently defined energy mapping.

---

## 231. Mapping Preservation of Resonance/Energy Separation

No resonance-classification mapping is an energy mapping.

---

## 232. Mapping Preservation of Transition/Bifurcation Separation

Threshold, resonance-window, ternary-transition, and bifurcation mappings remain distinct.

---

## 233. Mapping Preservation of Structural/Physical Phase Separation

A structural-state mapping does not automatically produce a physical phase classification.

---

## 234. Mapping Preservation of Mathematical/Numerical Separation

A numerical encoding mapping does not redefine the formal mathematical mapping it represents.

---

## 235. FRP Executable Mapping Reference

FRP may provide executable instances of selected TR-EIF mappings.

These may include verified mappings for:

- phase update;
- retained frequency update;
- hierarchical coupling;
- phase-order observation;
- phase-derived ternary target;
- scheduler selection;
- neutral routing;
- pending-state update;
- executed ternary commit.

---

## 236. FRP Phase Mapping

A verified FRP phase step realizes a numerical mapping on a computational representation of:

`(S^1)^N`.

Wrapped phase semantics remain circular.

---

## 237. FRP Coupling Mapping

A verified FRP coupling term may instantiate a Sakaguchi-type phase mapping.

Its implementation-specific lag and coupling parameters remain scoped to FRP.

---

## 238. FRP Retained-Frequency Mapping

The retained frequency mechanism provides an executable memory mapping:

`X_freq × X_aux → X_freq`.

It is a retained-state mapping.

---

## 239. FRP Phase-Order Mapping

The verified phase-order mapping computes:

`R = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

Its codomain remains phase-order magnitude.

---

## 240. FRP Phase-to-Target Mapping

The verified FRP executable reference includes a phase-derived ternary target mapping based on:

`sin(theta_i)`

and an implementation-specific threshold.

Its output belongs to:

`T_target`.

The threshold remains implementation-specific.

---

## 241. FRP Ternary Execution Mapping

The verified FRP execution layer instantiates:

- active neutral;
- forbidden direct opposite transitions;
- first-leg routing;
- pending destination;
- later second-leg completion.

---

## 242. FRP Scheduler Mapping

Verified FRP scheduler modes instantiate a control mapping over scheduler state.

They remain execution-specific parameters rather than universal TR-EIF timing laws.

---

## 243. FRP-to-TR-EIF Mapping Boundary

An FRP field or operation becomes a TR-EIF executable reference only through an explicit semantic mapping from:

`FRP implementation object`

to:

`TR-EIF formal object`.

Filename similarity or conceptual resemblance is insufficient.

---

## 244. Repository Mapping Architecture

The repository-level mapping chain is:

`documentation definitions`

`→ specifications`

`→ schemas`

`→ source implementation`

`→ tests`

`→ artifacts`

`→ validation results`.

Each layer maps formal meaning into a more concrete representation.

---

## 245. Documentation-to-Specification Mapping

A specification maps formal definitions into computational contracts.

It must preserve:

- type;
- domain;
- codomain;
- invariants;
- semantics.

---

## 246. Specification-to-Schema Mapping

A schema maps computational contracts into machine-readable field structures.

Schema fields must preserve semantic typing.

---

## 247. Schema-to-Implementation Mapping

Implementation state and APIs must correspond to the schema and specification semantics they claim to realize.

---

## 248. Implementation-to-Test Mapping

Tests instantiate controlled inputs and evaluate declared properties of implementation mappings.

---

## 249. Test-to-Validation Mapping

Validation aggregates test evidence under explicit acceptance criteria.

---

## 250. Mapping Dependency Graph

Mappings themselves may form a dependency graph:

`G_map = (V_map, E_map)`.

A directed edge:

`F_i → F_j`

means that:

`F_j`

depends on the output or semantics of:

`F_i`.

---

## 251. Acyclic Forward Mapping Chain

A pure forward representation pipeline may be acyclic:

`X_EIF → X_EQ → X_R → T_target`.

Feedback introduces a cycle only through an explicitly defined reverse mapping and later state update.

---

## 252. Feedback Mapping Cycle

A closed-loop TR-EIF mapping cycle is:

`X_EIF`

`→ X_TR`

`→ X_EIF,req`

`→ X_EIF,next`.

The temporal or execution ordering of the feedback must be explicit.

---

## 253. No Instantaneous Hidden Feedback

A mapping must not read the state it is simultaneously mutating unless the model defines a simultaneous relation or implicit solve.

---

## 254. Simultaneous Coupled Mapping

A simultaneous relation may be represented as a joint solve:

`F_joint(x, y) = 0`.

The coupled variables are determined together under explicit mathematical conditions.

---

## 255. Sequential Mapping

A sequential update uses an ordered composition:

`F_n ∘ ... ∘ F_1`.

Changing the order may change the result when the mappings do not commute.

---

## 256. Mapping Causality

A causal mapping uses:

- current state;
- past state;
- current admissible input.

It does not depend on future state as already-known data.

---

## 257. Mapping Closure

A mapping is closed for its declared purpose when every required argument is present in its explicit domain or fixed parameter context.

---

## 258. Forward Integration Closure

The forward EIF-to-TR mapping is closed only when every required:

- interatomic state;
- representation state;
- topology;
- history;
- scale;
- parameter

is available.

---

## 259. Ternary Execution Closure

The ternary execution mapping is closed only when all required:

- executed state;
- target;
- pending state;
- authorization/control state

are available.

---

## 260. Reverse Integration Closure

The TR-to-EIF mapping is closed only when the source TR state and required EIF context are available.

---

## 261. Multiscale Mapping Closure

A scale-transfer mapping is closed only when all required:

- source state;
- closure state;
- uncertainty state;
- scale metadata

are available.

---

## 262. Mapping Extension Rule

A new mapping must define:

1. mapping name;
2. source domain;
3. target codomain;
4. mathematical action;
5. parameters;
6. locality;
7. scale;
8. symmetry behavior;
9. dimensional behavior;
10. history or memory dependence;
11. information loss;
12. provenance.

---

## 263. Mapping Composition Rule

Mappings may be composed only when their intermediate semantic spaces are compatible.

Numerical storage compatibility alone is insufficient.

---

## 264. Mapping Replacement Rule

A replacement implementation mapping must preserve the formal mapping contract required by its declared conformance scope.

---

## 265. Mapping Specialization Rule

A specialized mapping may fix:

- material;
- scale;
- topology;
- parameter values;
- numerical representation.

It remains a specialization of the parent typed mapping.

---

## 266. Mapping Validation Rule

Every mapping used in executable or scientific claims must expose enough evidence to test the properties relevant to that claim.

---

## 267. Mapping Non-Equivalences

The following distinctions are mandatory:

`state projection ≠ state evolution`

`resonance projection ≠ resonance classification`

`resonance classification ≠ ternary mapping`

`ternary target mapping ≠ ternary execution`

`ternary execution ≠ structural transition mapping`

`phase-order mapping ≠ coherence mapping`

`phase-lag mapping ≠ delay mapping`

`phase relation mapping ≠ chemical-bond mapping`

`phase coupling mapping ≠ mechanical-force mapping`

`ternary mapping ≠ energy mapping`

`quantization mapping ≠ ternary classification`

`schema mapping ≠ physical mapping`

`serialization mapping ≠ dynamical mapping`

`validation mapping ≠ state mapping`.

---

## 268. Canonical TR-EIF Mapping Chain

The principal formal chain is:

`X_EIF`

`→ P_EQ`

`X_EQ`

`→ P_ER`

`X_R`

`→ C_R`

`K_R`

`→ P_KT or P_RT`

`T_target`

`→ E_T`

`T_exec`

`→ F_TR→E`

`X_EIF,req`

`→ F_Eauth`

`X_EIF,auth`

`→ F_Ecommit`

`X_EIF,next`.

No step in this chain is implicit.

---

## 269. Canonical Ternary Mapping Invariants

Every mapping touching ternary execution must preserve:

`T = {-1, 0, 1}`

and canonical notation:

`-1/0/1`.

The state:

`0`

remains active.

No direct committed mapping may produce:

`-1 → 1`

or:

`1 → -1`.

---

## 270. Canonical Opposite-Polarity Mapping

The required path is:

`-1`

`→ first-leg mapping`

`0`

`→ later authorized second-leg mapping`

`1`.

The reverse path is:

`1`

`→ first-leg mapping`

`0`

`→ later authorized second-leg mapping`

`-1`.

The two legs remain distinct mapping events.

---

## 271. Canonical Resonance Mapping Invariants

The resonance layer preserves:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`phase locking ≠ resonance`

`coherence ≠ resonance`.

The resonance coordinate space remains:

`X_R`.

---

## 272. Canonical Scientific Mapping Boundaries

The mapping architecture preserves:

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

## 273. Foundation for Framework Invariants

The mappings defined here establish the transformations over which Chapter 08 defines framework invariants.

Examples include:

- domain-preservation invariants;
- ternary-transition invariants;
- symmetry invariants;
- dimensional invariants;
- information-flow invariants;
- state-closure invariants;
- cross-layer consistency invariants.

---

## 274. Foundation for Fundamental Lemmas

The mappings defined in this chapter provide the formal objects required for later lemmas concerning:

- composition;
- state preservation;
- neutral-mediated reachability;
- mapping closure;
- symmetry preservation;
- information loss;
- dimensional consistency.

---

## 275. Foundation for Fundamental Theorems

Later theorems may establish stronger properties of mapping chains under explicit assumptions.

No theorem is implied solely by the existence of the mappings defined here.

---

## 276. Final Mapping Statement

TR-EIF is connected through explicit typed mappings rather than semantic shortcuts.

The central integration architecture is:

`interatomic state`

`→ equivariant representation`

`→ resonance state`

`→ resonance classification`

`→ ternary target`

`→ neutral-mediated -1/0/1 execution`

`→ interatomic update request`

`→ interatomic commit`.

The balanced ternary kernel remains exactly:

`-1/0/1`

with:

`T = {-1, 0, 1}`.

The state:

`0`

remains active.

Direct committed mappings:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

Opposite-polarity execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

through separate execution events.

The mapping layer preserves explicit separation among:

- atomic configuration;
- graph topology;
- invariant representation;
- equivariant representation;
- phase state;
- resonance state;
- resonance classification;
- ternary target;
- executed ternary state;
- energy;
- force;
- stress;
- structural state;
- physical phase state;
- numerical state;
- artifact state;
- validation state.

Every later invariant, lemma, theorem, corollary, numerical implementation, molecular-dynamics model, multiscale model, and FLiBe specialization therefore has a formally defined path through the state spaces and structures of TR-EIF.
