# Model Family TR-EIP

## 1. Purpose

This chapter defines the TR-EIP model family within the Equivariant Interatomic Framework of TR-EIF.

The model family consolidates the complete Volume 03 architecture:

`atomic configuration`

`→ interaction graph`

`→ E(3) group action`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

A TR-EIP model is a concrete member of this architecture with explicitly declared:

- state spaces;
- graph construction;
- symmetry group;
- representation types;
- message-passing structure;
- resonance parameterization;
- ternary channels;
- energy functional;
- force construction;
- stress construction;
- parameters;
- numerical semantics;
- provenance;
- validation contract.

The model family does not collapse all admissible realizations into one universal parameter set.

---

## 2. Model-Family Definition

Let:

`M_TR-EIP`

denote the family of TR-EIP models.

A model:

`M ∈ M_TR-EIP`

is a concrete realization of the formal architecture defined in Volumes 01–03.

A model may be represented as:

`M = (AC, IG, SG, ER, MP, RP, TF, CEF, MECH, P, N, V)`.

Here:

- `AC` is atomic configuration structure;
- `IG` is interaction-graph structure;
- `SG` is spatial and permutation symmetry structure;
- `ER` is equivariant representation structure;
- `MP` is message passing;
- `RP` is resonance parameterization;
- `TF` is ternary feature structure;
- `CEF` is conservative energy structure;
- `MECH` is force/stress structure;
- `P` is parameter state;
- `N` is numerical realization;
- `V` is validation state and contract.

---

## 3. TR-EIP Identity

TR-EIP denotes the integrated interatomic model family combining:

- equivariant atomistic representation;
- resonance parameterization;
- balanced ternary feature semantics;
- conservative energy interfaces;
- mechanical outputs.

It is not one neural-network architecture.

It is not one interatomic potential.

It is not one material specialization.

It is not FRP.

---

## 4. TR-EIP and TR-EIF

The relation is:

`TR-EIP ⊂ TR-EIF`

at the model-family level.

TR-EIF contains the broader mathematical, learning, molecular-dynamics, multiscale, validation, and material-specialization architecture.

TR-EIP is the concrete equivariant interatomic model family defined within that framework.

---

## 5. TR-EIP and FRP

The relation remains:

`FRP ≠ TR-EIP`.

FRP provides executable reference behavior for selected ternary-resonant mechanisms.

TR-EIP applies the broader formal structure to equivariant interatomic modeling.

---

## 6. Canonical Forward Architecture

Every TR-EIP model follows the semantic chain:

`X_conf`

`→ X_G`

`→ X_EQ`

`→ X_R`

`→ X_T`

`→ E`

`→ F / Sigma`.

The exact implementation may fuse computational stages.

The semantic state boundaries remain explicit.

---

## 7. Atomic Configuration Component

The configuration component defines:

`AC = (N, A_N, R, H, PBC, X_atom, X_global, X_adm)`.

It specifies:

- atom count;
- species;
- positions;
- periodic cell;
- periodicity;
- per-atom attributes;
- global attributes;
- admissible domain.

---

## 8. Graph Component

The graph component defines:

`IG = (V, E, H_node, H_edge, G_global, P_G)`.

It specifies:

- node set;
- edge set;
- source/receiver convention;
- graph construction;
- cutoff;
- periodic-image handling;
- node features;
- edge features;
- dynamic graph behavior.

---

## 9. Symmetry Component

The symmetry component defines:

`SG = (G_space, G_perm, rho_conf, rho_G, rho_EQ, rho_R, rho_out)`.

It specifies:

- `E(3)`, `SE(3)`, `O(3)`, `SO(3)`, or declared subgroup;
- species-preserving permutation structure;
- representation actions;
- parity handling;
- external symmetry-breaking state.

---

## 10. Representation Component

The representation component defines:

`ER = (X_EQ, I, B_rad, B_ang, TP, N_EQ)`.

It specifies:

- scalar channels;
- vector channels;
- higher irreducible channels;
- parity;
- radial basis;
- angular basis;
- tensor-product paths;
- normalization;
- nonlinearities.

---

## 11. Message-Passing Component

The message component defines:

`MP = (M, A, U_N, U_E, U_G)`.

It specifies:

- directed message map;
- aggregation;
- node update;
- edge update;
- global update;
- message depth;
- locality;
- multiscale coupling.

---

## 12. Resonance Component

The resonance component defines:

`RP = (X_R, P_R, rho_R, W_R, C_R, X_R,M, A_R)`.

It specifies:

- resonance state;
- resonance transformation law;
- local and global resonance structure;
- windows;
- classification;
- memory;
- aggregation.

---

## 13. Ternary Component

The ternary component defines:

`TF = (X_T, P_T, X_M,T, A_T, P_FT, rho_T)`.

It specifies:

- ternary feature scope;
- exact `-1/0/1` domain;
- active-neutral semantics;
- decision mappings;
- target role;
- memory;
- aggregation;
- execution interface.

---

## 14. Energy Component

The energy component defines:

`CEF = (D_E, E, phi_E)`.

It specifies:

- energy domain;
- scalar energy functional;
- energy units;
- decomposition;
- resonance conditioning;
- ternary conditioning;
- differentiability;
- periodic behavior.

---

## 15. Mechanical Component

The mechanical component defines:

`MECH = (D_F, D_Sigma, P_F, P_Sigma)`.

It specifies:

- force path;
- conservative/direct force status;
- stress path;
- stress tensor type;
- sign convention;
- units;
- symmetry.

---

## 16. Parameter State

Let:

`P`

denote the complete model parameter state.

It may contain:

- fixed analytic parameters;
- learned parameters;
- calibrated parameters;
- material-specific parameters;
- numerical parameters;
- scheduler parameters where used.

---

## 17. Parameter Partition

A useful partition is:

`P = P_fixed × P_learned × P_cal × P_num`.

---

## 18. Fixed Parameters

`P_fixed`

contains model-defined constants and architecture settings.

---

## 19. Learned Parameters

`P_learned`

contains parameters optimized through the learning process.

---

## 20. Calibrated Parameters

`P_cal`

contains parameters estimated through calibration against declared reference data.

---

## 21. Numerical Parameters

`P_num`

contains implementation-level parameters such as:

- numerical precision;
- integration timestep where relevant;
- cutoff implementation;
- convergence tolerance;
- batching configuration.

---

## 22. Parameter Provenance

Every result-affecting parameter must carry appropriate provenance.

The canonical provenance classes remain:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 23. Model Signature

A model signature is a structured declaration of its architecture and parameter state.

A signature may contain:

- model-family version;
- symmetry group;
- species domain;
- cutoff;
- basis structure;
- `l_max`;
- message depth;
- resonance dimension;
- ternary channel set;
- energy structure;
- force path;
- stress path.

---

## 24. Model Identity

Two models are distinct if any result-affecting architecture, parameter, numerical, or state-semantic element differs.

---

## 25. Architecture Identity

Changing:

- symmetry group;
- graph rule;
- message map;
- resonance mapping;
- ternary semantics;
- energy functional

creates a different model architecture.

---

## 26. Parameter Identity

Two instances of the same architecture with different parameter values are different model instances.

---

## 27. Numerical Identity

Exact replay may also depend on numerical realization.

Thus the same mathematical model may have multiple numerical implementations.

---

## 28. Model Version

A model version must identify the complete result-affecting specification required for reproducibility.

---

## 29. Configuration Domain

Each model defines:

`D_conf`.

This domain specifies admissible:

- species;
- atom count;
- cell state;
- geometry;
- composition;
- periodicity.

---

## 30. Material Domain

A model may be:

- material-general;
- species-limited;
- composition-limited;
- material-specific.

The domain must be explicit.

---

## 31. Species Domain

Let:

`A_M`

denote the supported species set of model:

`M`.

---

## 32. Configuration Admissibility

A configuration:

`X`

is admissible when:

`X ∈ D_conf(M)`.

---

## 33. Out-of-Domain Configuration

An out-of-domain configuration must be represented separately from ordinary model outputs.

It is not ternary active neutral.

---

## 34. Model Input Contract

The model input contract defines:

- positions;
- species;
- cell;
- periodicity;
- optional charge;
- optional external fields;
- optional retained state;
- units.

---

## 35. Model Output Contract

A model may output:

- total energy;
- local energies;
- atomic forces;
- stress;
- resonance state;
- ternary features;
- uncertainty;
- auxiliary observables.

Each output remains separately typed.

---

## 36. Mandatory Output Boundary

No model-family definition requires every model to expose every internal latent feature.

The semantic interfaces required by its declared capabilities must remain available.

---

## 37. Energy-Capable Model

An energy-capable model defines:

`E`.

---

## 38. Conservative-Force Model

A conservative-force model defines:

`F_i = -grad_(r_i) E`.

---

## 39. Direct-Force Model

A direct-force model defines:

`P_F`

without requiring:

`F = -grad E`.

---

## 40. Stress-Capable Model

A stress-capable model defines a valid:

`P_Sigma`

with explicit tensor convention.

---

## 41. Resonance-Capable Model

Every TR-EIP member using the complete architecture defines:

`X_R`

and:

`P_R`.

---

## 42. Ternary-Capable Model

A model using ternary feature channels defines exact:

`-1/0/1`

semantics.

---

## 43. Full TR-EIP Member

A full member contains:

`X_conf`

`X_G`

`X_EQ`

`X_R`

`X_T`

`E`

and the declared mechanical outputs.

---

## 44. Reduced Member

A reduced model may omit selected optional output heads while retaining the declared TR-EIP state semantics.

The omitted capability must be explicit.

---

## 45. Symmetry Contract

Every TR-EIP member must declare its spatial symmetry group.

Examples include:

`E(3)`

`SE(3)`

`O(3)`

`SO(3)`.

---

## 46. Permutation Contract

Every atomistic member must preserve admissible atom-permutation semantics.

---

## 47. Energy Invariance Contract

If energy is present:

`E(gX) = E(X)`

under the declared symmetry group.

---

## 48. Force Equivariance Contract

If force is present:

`F(gX) = rho_F(g)F(X)`.

---

## 49. Stress Equivariance Contract

If stress is present:

`Sigma(gX) = Q Sigma(X) Q^T`

under rigid spatial rotation.

---

## 50. Graph Symmetry Contract

Graph construction must transform consistently under the model symmetry and atom permutations.

---

## 51. Representation Symmetry Contract

Every feature channel must preserve its declared representation type.

---

## 52. Resonance Symmetry Contract

Resonance state must preserve:

`rho_R`.

---

## 53. Ternary Symmetry Contract

Canonical scalar ternary channels remain invariant under rigid spatial transformation unless another explicit channel action is defined.

---

## 54. Canonical Ternary Kernel

The balanced ternary kernel remains exactly:

`-1/0/1`.

---

## 55. Active Neutral

The state:

`0`

remains active neutral.

---

## 56. Invalid-State Separation

The following remain outside the ternary semantic domain:

`NONE`

`INVALID`

`NaN`

`MASKED`

`PADDED`

`OUT_OF_DOMAIN`.

---

## 57. Target State

A model may define:

`t_target`.

---

## 58. Executed State

A model using the execution layer may define:

`t_exec`.

---

## 59. Pending State

Opposite-polarity routing may use:

`t_pending`.

---

## 60. Target/Execution Separation

The invariant remains:

`target ≠ executed state`.

---

## 61. Canonical Execution Graph

The committed execution graph is:

`-1 ↔ 0 ↔ 1`.

---

## 62. Forbidden Direct Transitions

Committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 63. Opposite Route

Opposite-polarity execution uses:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

---

## 64. First-Leg Commit

The first leg enters:

`0`.

---

## 65. Neutral Residence

The state:

`0`

may persist.

---

## 66. Second-Leg Commit

The second leg leaves:

`0`

toward the pending destination.

---

## 67. TR-EIP Ternary Scope

Ternary channels may exist at:

- edge scale;
- atom scale;
- cluster scale;
- global scale.

Each channel must declare whether it is:

- latent;
- target;
- executed;
- conditioning;
- diagnostic.

---

## 68. Ternary Feature versus Graph Mask

The distinction remains:

`ternary feature ≠ graph mask`.

---

## 69. Ternary Feature versus Energy

The distinction remains:

`ternary state ≠ energy`.

---

## 70. Ternary Feature versus Force

The distinction remains:

`ternary state ≠ force`.

---

## 71. Ternary Feature versus Stress

The distinction remains:

`ternary state ≠ stress`.

---

## 72. Resonance State Contract

A model must declare:

- resonance source;
- resonance dimension;
- transformation type;
- local/global scope;
- window structure;
- memory;
- target interface.

---

## 73. Resonance Window

If used:

`W_R ⊂ X_R`.

---

## 74. Resonance Classifier

If used:

`C_R: X_R → K_R`.

---

## 75. Resonance Class Separation

The relation remains:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

---

## 76. Resonance versus Synchronization

The distinction remains:

`resonance ≠ synchronization`.

---

## 77. Synchronization versus Phase Locking

The distinction remains:

`synchronization ≠ phase locking`.

---

## 78. Phase Locking versus Resonance

The distinction remains:

`phase locking ≠ resonance`.

---

## 79. Coherence versus Resonance

The distinction remains:

`coherence ≠ resonance`.

---

## 80. Phase Order versus Coherence

The invariant remains:

`R(t) ≠ C(t)`.

---

## 81. Phase-Layer Integration

A TR-EIP member may include oscillator phase state as an auxiliary resonance input.

---

## 82. Phase State

Oscillator phase belongs to:

`S^1`.

---

## 83. Phase Lag

A Sakaguchi phase lag remains distinct from temporal delay.

---

## 84. Phase Coupling Boundary

The distinction remains:

`phase coupling ≠ mechanical force`.

---

## 85. Phase Relation Boundary

The distinction remains:

`phase relation ≠ chemical bond`.

---

## 86. Geometry Boundary

The distinction remains:

`geometry ≠ resonance`.

---

## 87. Representation Boundary

The distinction remains:

`equivariant representation ≠ resonance`.

---

## 88. Message Boundary

The distinction remains:

`message passing ≠ resonance`.

---

## 89. Energy Boundary

The distinction remains:

`resonance classification ≠ energy`.

---

## 90. Mechanical Boundary

The distinction remains:

`generic vector feature ≠ force`.

---

## 91. Stress Boundary

The distinction remains:

`generic tensor feature ≠ stress`.

---

## 92. Conservative Model Family

A conservative TR-EIP member defines:

`E_M(X)`.

Force is:

`F_M = -grad_R E_M`.

---

## 93. Mode-Conditioned Conservative Family

A ternary-conditioned conservative member may define:

`E_M(X, q)`

with:

`q ∈ {-1,0,1}`.

---

## 94. Mode-Specific Surfaces

The model may contain:

`E_-1`

`E_0`

`E_1`.

---

## 95. Active-Neutral Surface

`E_0`

is not zero energy by identity.

---

## 96. Mode-Specific Forces

For each fixed mode:

`F_q = -grad_R E_q`

where the energy surface is differentiable.

---

## 97. Opposite Mechanical Mode Chain

If mechanics are keyed to:

`t_exec`:

`E_-1 → E_0 → E_1`

or:

`E_1 → E_0 → E_-1`.

The same applies to the corresponding force modes.

---

## 98. Direct Force Family

A nonconservative model-family member may define:

`F_direct`.

Its conservativity status must remain explicit.

---

## 99. Hybrid Energy/Force Family

A model may expose both:

- scalar energy;
- direct force.

The consistency relation must be explicitly declared.

---

## 100. Stress Family

Stress may be:

- energy-derived;
- virial-derived;
- directly predicted;
- hybrid.

The exact type must be explicit.

---

## 101. Locality Class

A model member may be:

- strictly local;
- local with finite message depth;
- local plus long range;
- explicitly nonlocal;
- multiscale.

---

## 102. Cutoff

A local member must define:

`r_cut`.

---

## 103. Species-Dependent Cutoff

A member may define:

`r_cut(a_i,a_j)`.

---

## 104. Graph Family

Model-family graph types may include:

- radius graph;
- k-nearest-neighbor graph;
- hybrid graph;
- multi-relation graph;
- multiscale graph.

---

## 105. Graph Choice Is Model-Defining

Changing the graph-construction rule changes the model member.

---

## 106. Representation Family

A model member may differ by:

- symmetry group;
- `l_max`;
- parity support;
- radial basis;
- angular basis;
- channel multiplicities.

---

## 107. Message Family

A model member may differ by:

- message depth;
- aggregation;
- tensor-product paths;
- attention;
- recurrence;
- global-state coupling.

---

## 108. Resonance Family

A model member may differ by:

- resonance dimension;
- local/global structure;
- memory;
- window geometry;
- classifier;
- phase coupling.

---

## 109. Ternary Family

A model member may differ by:

- number of ternary channels;
- source state;
- decision mapping;
- hysteresis;
- persistence;
- target aggregation;
- feedback role.

---

## 110. Energy Family

A model member may differ by:

- local energy decomposition;
- long-range terms;
- resonance conditioning;
- ternary conditioning;
- reference-energy terms.

---

## 111. Mechanical Family

A model member may differ by:

- conservative versus direct force;
- stress formulation;
- force regularization;
- cell coupling.

---

## 112. Multiscale Family

A model may contain several coupled graph and representation scales.

---

## 113. Atomistic Scale

The base scale contains individual atoms.

---

## 114. Cluster Scale

A higher scale may represent atom clusters.

---

## 115. Global Scale

A global state may represent complete-system observables.

---

## 116. Cross-Scale Mapping

A model must explicitly define:

`M^(a→b)`.

---

## 117. Cross-Scale Resonance

Resonance may be propagated across scales.

---

## 118. Cross-Scale Ternary State

Ternary channels may also exist independently at several scales.

---

## 119. Cross-Scale Energy

A multiscale model may contain scale-specific energy contributions.

Double counting must be controlled explicitly.

---

## 120. Cross-Scale Force

Force must remain a correctly typed atomistic mechanical output when propagated back to atomistic dynamics.

---

## 121. Model-State Closure

A complete runtime state includes every variable affecting future outputs.

---

## 122. Stateless Member

A stateless inference member may depend only on current configuration and fixed parameters.

---

## 123. Stateful Member

A stateful member may retain:

- resonance memory;
- ternary hysteresis;
- scheduler state;
- pending routes;
- adaptive parameters;
- recurrent representation state.

---

## 124. Restart State

Every stateful member must define restart-complete state.

---

## 125. Deterministic Member

A deterministic member produces the same outputs from identical complete state, parameters, and inputs under its numerical contract.

---

## 126. Stochastic Member

A stochastic member must include random state in reproducibility semantics.

---

## 127. Random Seed

A seed may initialize stochastic state.

The complete generator state may also be required for exact restart.

---

## 128. Model Evaluation

A generic evaluation may be represented:

`Y = M(X; P)`.

---

## 129. Stateful Evaluation

A stateful evaluation may be:

`(Y, S_next) = M(X, S_current; P)`.

---

## 130. Output Set

A complete output state may include:

`Y = (E, F, Sigma, X_R, X_T, U)`.

Here:

`U`

may contain uncertainty or auxiliary observables.

---

## 131. Output Optionality

Each member declares which outputs are present.

Absent outputs are not encoded as ternary neutral.

---

## 132. Numerical Realization

A model member must define its numerical realization:

`N`.

---

## 133. Numerical Precision

The model declares:

- float64;
- float32;
- mixed precision;
- fixed point;
- another explicit representation.

---

## 134. Numerical Ordering

When operations do not commute numerically, update ordering is part of the model realization.

---

## 135. Graph Ordering

Canonical node and edge ordering may be required for deterministic replay.

---

## 136. Reduction Ordering

Floating-point reductions may require deterministic ordering.

---

## 137. Differentiation Path

A model must declare whether forces and stress use:

- automatic differentiation;
- analytic derivatives;
- direct prediction;
- finite differences for validation only.

---

## 138. Numerical Tolerance

Validation tolerances belong to the numerical contract.

They do not redefine formal invariants.

---

## 139. Exact Ternary Semantics

Ternary categorical equality remains exact even when continuous outputs use numerical tolerances.

---

## 140. Model Manifest

A TR-EIP model manifest should identify:

- model-family version;
- architecture identifier;
- parameter artifact;
- supported species;
- unit system;
- symmetry group;
- cutoff;
- representation structure;
- message depth;
- resonance structure;
- ternary structure;
- energy/force/stress capabilities;
- numerical precision;
- provenance.

---

## 141. Model Manifest versus Runtime State

The manifest defines the model.

Runtime state defines the current evolving state.

They are distinct.

---

## 142. Parameter Artifact

Learned or calibrated parameters should be represented as a versioned artifact.

---

## 143. Architecture Artifact

Architecture definition should remain separately identifiable from parameter values.

---

## 144. Schema Contract

Model manifests and outputs must conform to declared schemas.

---

## 145. Configuration Schema

The configuration schema defines valid atomic inputs.

---

## 146. Resonance Schema

The resonance schema defines:

`X_R`

serialization.

---

## 147. Ternary Schema

The ternary schema restricts semantic values to:

`-1`

`0`

`1`.

---

## 148. Energy Schema

The energy schema defines:

- value;
- units;
- decomposition;
- metadata.

---

## 149. Observable Schema

Mechanical and additional observables require explicit type and unit metadata.

---

## 150. Transition Trace Schema

Execution-bound models require explicit target, executed, and pending states.

---

## 151. Training Interface

Volume 04 consumes the TR-EIP parameterized model family.

---

## 152. Trainable Parameter Set

Let:

`P_train ⊆ P`.

Only declared trainable parameters are modified by optimization.

---

## 153. Frozen Parameters

The complement may remain fixed during training.

---

## 154. Energy Training

Energy references may train scalar energy outputs.

---

## 155. Force Training

Reference forces may train energy gradients or direct force outputs.

---

## 156. Stress Training

Stress references may train cell/strain response.

---

## 157. Ternary Training

Ternary features may be:

- fixed by author-defined mapping;
- calibrated;
- learned through surrogate structures.

The semantic forward domain remains exact when hard ternary state is used.

---

## 158. Resonance Training

Resonance mappings may contain learned parameters.

The resonance state space and semantic interfaces remain explicit.

---

## 159. Equivariance Constraints

Learning must preserve the declared equivariance contract.

---

## 160. Conservative Constraints

A conservative model must preserve the energy-force relation throughout training.

---

## 161. Molecular-Dynamics Interface

Volume 05 consumes:

- atomic positions;
- velocities;
- forces;
- energy;
- stress;
- ternary/resonance retained state where coupled.

---

## 162. MD State Update

TR-EIP supplies mechanical outputs.

The MD integrator advances dynamical state.

---

## 163. Model versus Integrator

The distinction remains:

`interatomic model ≠ molecular-dynamics integrator`.

---

## 164. Force Model versus Equation of Motion

The distinction remains:

`force model ≠ equation of motion`.

---

## 165. Multiscale Interface

Volume 06 consumes atomistic outputs and state representations for coarse-graining and closure.

---

## 166. FLiBe Interface

Volume 07 instantiates the model family for the FLiBe reference system.

---

## 167. Material Specialization

A material-specific TR-EIP member defines:

- supported species;
- composition domain;
- reference data;
- thermodynamic domain;
- transport domain;
- resonance parameters;
- ternary interpretation;
- validation matrix.

---

## 168. Material-General Member

A material-general architecture may support multiple species families.

Its valid domain must still be explicit.

---

## 169. FLiBe Is Not the Model Family

The relation remains:

`FLiBe specialization ≠ TR-EIP model family`.

FLiBe is one later reference specialization.

---

## 170. Model Hierarchy

The architecture hierarchy is:

`TR-EIF`

`→ TR-EIP model family`

`→ concrete model architecture`

`→ parameterized model instance`

`→ material specialization`

`→ numerical runtime state`.

---

## 171. Model-Family Registry

A future implementation may maintain a registry of model-family members.

Each entry should contain a unique model identifier.

---

## 172. Model Identifier

The identifier should remain stable for one declared architecture/version.

---

## 173. Parameter Identifier

A parameter artifact requires its own identifier or hash.

---

## 174. Dataset Identifier

Training and calibration artifacts should identify their source dataset.

---

## 175. Validation Identifier

Validation results should identify:

- model version;
- parameter version;
- dataset;
- numerical environment.

---

## 176. Model Reproducibility

A reproducible model result requires sufficient information to reconstruct:

- architecture;
- parameters;
- input;
- numerical realization;
- state;
- external conditions.

---

## 177. Deterministic Replay

For deterministic members:

`complete model state`

`+ complete input`

`+ parameters`

`+ numerical semantics`

must reproduce the declared output.

---

## 178. Byte-Identical Replay

A strict contract may require canonical serialization and deterministic arithmetic/order.

---

## 179. Tolerance-Based Replay

Continuous outputs may use tolerance-based comparison.

Categorical states remain exact.

---

## 180. Model Validation

Every concrete member must define validation appropriate to its claimed capabilities.

---

## 181. Configuration Validation

Validate:

- species;
- geometry;
- cell;
- periodicity;
- finite state.

---

## 182. Graph Validation

Validate:

- edge construction;
- source/receiver convention;
- periodic shifts;
- permutation behavior.

---

## 183. Equivariance Validation

Validate:

- translation;
- rotation;
- reflection where declared;
- permutation;
- combined transformations.

---

## 184. Representation Validation

Validate transformation laws of representation channels.

---

## 185. Message Validation

Validate directed message semantics and aggregation behavior.

---

## 186. Resonance Validation

Validate:

- resonance transformation;
- window semantics;
- classifier;
- memory;
- determinism.

---

## 187. Ternary Validation

Validate exact:

`-1/0/1`.

---

## 188. Active-Neutral Validation

Validate:

`0`

as a valid active state.

---

## 189. Target/Execution Validation

Validate separation of:

`t_target`

and:

`t_exec`.

---

## 190. Opposite-Route Validation

Validate:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 191. Direct-Opposite Rejection

Reject committed:

`-1 → 1`

and:

`1 → -1`.

---

## 192. Energy Validation

Validate scalar symmetry, units, determinism, and decomposition.

---

## 193. Force Validation

Validate:

`F_i = -grad_(r_i)E`

for conservative models.

---

## 194. Force Equivariance Validation

Validate:

`F(QR) = QF(R)`.

---

## 195. Stress Validation

Validate tensor transformation and energy/cell consistency where declared.

---

## 196. Conservation Interface Validation

For conservative models, validate applicable mechanical invariants within the corresponding dynamics layer.

---

## 197. Model-Domain Validation

Validate that test samples belong to the declared model domain.

---

## 198. Out-of-Domain Detection

Where implemented, out-of-domain status remains separate from model semantic outputs.

---

## 199. Uncertainty Validation

If uncertainty is exposed, its definition and calibration must be separately validated.

---

## 200. Benchmark Layer

A model member may expose benchmarks for:

- runtime;
- memory;
- scaling;
- energy error;
- force error;
- stress error;
- equivariance residual;
- deterministic replay;
- ternary transition statistics.

---

## 201. Benchmark Scope

Every benchmark must identify the full configuration under which it was measured.

---

## 202. Benchmark versus Model Invariant

A benchmark result is not a universal mathematical invariant.

---

## 203. Test Fixture

Controlled atomic and ternary states may be used as deterministic fixtures.

---

## 204. Scientific Source Boundary

Relations imported from scientific literature must retain source provenance.

---

## 205. Author-Defined Architecture

TR-EIP integration structures defined by the framework retain:

`AUTHOR_DEFINED`

provenance.

---

## 206. Derived Outputs

Outputs analytically or numerically derived from other declared quantities retain:

`DERIVED`

provenance where applicable.

---

## 207. Calibrated Model Member

A model containing calibrated parameters must preserve the calibration artifact and provenance.

---

## 208. Learned Model Member

A learned model must preserve:

- architecture;
- parameter artifact;
- training configuration;
- data provenance;
- loss definition.

---

## 209. Model-Family Extension Rule

Any new TR-EIP family member must define:

1. configuration domain;
2. graph structure;
3. symmetry group;
4. representation structure;
5. message structure;
6. resonance structure;
7. ternary channels;
8. energy model;
9. force model;
10. stress model;
11. parameters;
12. numerical semantics;
13. validation;
14. provenance.

---

## 210. Architecture Extension Rule

Any architecture modification must identify the changed component and resulting model-family member identity.

---

## 211. Parameter Extension Rule

Any new parameter must define:

1. role;
2. domain;
3. units where applicable;
4. provenance;
5. trainable/fixed/calibrated status;
6. serialization.

---

## 212. Output Extension Rule

Any new output must define:

1. output space;
2. units;
3. transformation law;
4. source state;
5. validation;
6. provenance.

---

## 213. State Extension Rule

Any retained state must define:

1. initialization;
2. update;
3. reset;
4. serialization;
5. deterministic replay role.

---

## 214. Ternary Extension Rule

Any new ternary channel must preserve:

`-1/0/1`

and explicitly define:

- scope;
- source;
- target/executed role;
- active-neutral behavior;
- symmetry;
- routing relation.

---

## 215. Resonance Extension Rule

Any new resonance variable must define:

- source state;
- transformation law;
- scale;
- units;
- window/classifier relation;
- target interface.

---

## 216. Energy Extension Rule

Any new energy term must define:

- units;
- state dependence;
- symmetry;
- differentiability;
- provenance;
- double-counting relation.

---

## 217. Force Extension Rule

Any new force path must define whether it is:

- conservative;
- direct;
- hybrid.

---

## 218. Stress Extension Rule

Any stress path must define:

- tensor type;
- sign;
- normalization;
- cell/strain convention.

---

## 219. Numerical Extension Rule

Any new numerical realization must define:

- arithmetic;
- precision;
- ordering;
- deterministic semantics;
- tolerances.

---

## 220. Canonical Model-Family Invariants

Every conforming TR-EIP model preserves:

1. explicit atomic configuration;

2. explicit graph construction;

3. explicit symmetry contract;

4. explicit representation types;

5. explicit message-passing semantics;

6. explicit resonance state;

7. exact ternary domain;

8. explicit energy semantics;

9. explicit mechanical output semantics;

10. explicit provenance;

11. explicit validation.

---

## 221. Canonical Ternary Invariants

Every execution-bound member preserves:

`T = {-1,0,1}`.

The state:

`0`

is active.

Direct committed:

`-1 → 1`

and:

`1 → -1`

are forbidden.

---

## 222. Canonical Opposite-Route Invariants

Opposite execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

The two state-changing legs remain distinct.

---

## 223. Canonical Symmetry Invariants

Every model preserves its declared spatial and permutation transformation laws.

---

## 224. Canonical Energy Invariants

Energy is an explicitly typed scalar physical quantity.

---

## 225. Canonical Force Invariants

Conservative force satisfies:

`F_i = -grad_(r_i) E`.

Direct-force models must explicitly declare non-derived force construction.

---

## 226. Canonical Stress Invariants

Stress remains a separately typed tensor output.

---

## 227. Canonical State-Separation Invariants

The model family preserves:

`atomic configuration ≠ graph`

`graph ≠ representation`

`representation ≠ resonance`

`resonance ≠ ternary state`

`ternary target ≠ executed state`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`

`message ≠ force`

`interaction edge ≠ chemical bond`.

---

## 228. Canonical Scientific Distinctions

The model family preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`phase lag ≠ temporal delay`

`threshold crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`equivariance ≠ conservativity`

`potential energy ≠ total mechanical energy`.

---

## 229. Canonical Model Construction Chain

A concrete member is constructed through:

`declare configuration domain`

`→ declare graph`

`→ declare symmetry`

`→ declare representation`

`→ declare message passing`

`→ declare resonance parameterization`

`→ declare ternary channels`

`→ declare energy`

`→ declare force/stress`

`→ declare parameters`

`→ declare numerical realization`

`→ declare validation contract`.

---

## 230. Canonical Runtime Chain

A runtime evaluation proceeds conceptually as:

`configuration`

`→ graph`

`→ equivariant features`

`→ message-passed state`

`→ resonance state`

`→ ternary features`

`→ energy`

`→ forces/stress`

`→ output artifacts`.

---

## 231. Canonical Execution-Bound Chain

For execution-enabled members:

`resonance state`

`→ ternary target`

`→ target registration`

`→ scheduler`

`→ request handling`

`→ pending route`

`→ active neutral`

`→ executed state`

`→ conditioned next model state`.

---

## 232. Canonical Feedback Chain

A coupled member may use:

`T_exec`

`+ X_R`

`+ X_EQ`

`→ next representation / resonance / energy parameters`.

The feedback map must remain explicit.

---

## 233. Canonical Training Chain

Volume 04 will specialize:

`model family`

`+ reference data`

`→ loss functionals`

`→ optimization`

`→ parameterized model instance`.

---

## 234. Canonical MD Chain

Volume 05 will specialize:

`TR-EIP force`

`+ atomic dynamical state`

`→ equations of motion`

`→ numerical integrator`

`→ next atomic configuration`.

---

## 235. Canonical Multiscale Chain

Volume 06 will specialize:

`atomistic TR-EIP state`

`→ mesoscale mapping`

`→ continuum closure`

`→ engineering-scale state`.

---

## 236. Canonical FLiBe Chain

Volume 07 will specialize:

`TR-EIP model family`

`→ FLiBe species/composition`

`→ FLiBe interatomic reference data`

`→ FLiBe thermodynamic/transport state`

`→ FLiBe resonance and ternary interpretation`

`→ validation matrix`.

---

## 237. Interface to Chapter 11

Chapter 11 closes Volume 03.

It consolidates:

- atomic configuration;
- interaction graphs;
- E(3) symmetry;
- equivariant representations;
- message passing;
- resonance parameterization;
- ternary feature channels;
- conservative energy;
- forces and stress;
- TR-EIP model family.

---

## 238. Interface to Volume 04

Volume 04 develops Learning and Optimization.

The principal exported object is:

`M_TR-EIP(P)`.

Volume 04 determines how selected:

`P_train`

are optimized from data while preserving the architecture contracts defined here.

---

## 239. Interface to Volume 05

Volume 05 develops Molecular Dynamics.

The principal TR-EIP mechanical interface is:

`(E, F, Sigma)`.

The complete coupled state may additionally contain resonance and ternary state.

---

## 240. Interface to Volume 06

Volume 06 develops Multiscale Materials Modeling.

TR-EIP supplies the atomistic model state and observables required for cross-scale transfer.

---

## 241. Interface to Volume 07

Volume 07 develops the FLiBe Reference Model.

It instantiates a concrete material specialization from the TR-EIP family.

---

## 242. Final Formal Structure

The TR-EIP model family may be represented as:

`M_TR-EIP = {M(theta) | theta ∈ Theta_arch × Theta_param × Theta_num}`.

Here:

- `Theta_arch` identifies admissible architecture choices;
- `Theta_param` identifies model parameter state;
- `Theta_num` identifies numerical realization.

Each concrete model satisfies:

`M: X_input × X_state → X_output × X_state,next`

where statefulness is present.

A canonical full output may contain:

`(X_R, X_T, E, F, Sigma)`.

The exact balanced ternary domain remains:

`{-1,0,1}`.

---

## 243. Final Statement

The TR-EIP model family is the complete interatomic realization layer connecting equivariant atomic geometry, resonance state, balanced ternary features, conservative energy, forces, and stress.

Every concrete member declares its:

- atomic domain;
- graph;
- symmetry;
- representation;
- message passing;
- resonance state;
- ternary channels;
- energy functional;
- force path;
- stress path;
- parameters;
- numerical realization;
- validation contract;
- provenance.

The family preserves the exact semantic boundaries:

`configuration ≠ graph`

`graph ≠ representation`

`representation ≠ resonance`

`resonance ≠ ternary state`

`ternary target ≠ executed state`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`

`equivariance ≠ conservativity`

`message ≠ force`

`interaction edge ≠ chemical bond`.

The balanced ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

For execution-bound channels, the only opposite-polarity committed routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

The model family exports the parameterized interatomic architecture required by Learning and Optimization, Molecular Dynamics, Multiscale Materials Modeling, and the later FLiBe reference specialization.

These definitions complete the concrete TR-EIP model-family layer required for the Volume 03 summary.
