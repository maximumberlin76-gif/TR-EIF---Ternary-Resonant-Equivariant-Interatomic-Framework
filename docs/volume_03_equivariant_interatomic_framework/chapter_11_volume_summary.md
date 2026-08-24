# Volume 03 — Equivariant Interatomic Framework: Summary

## 1. Purpose

Volume 03 defines the Equivariant Interatomic Framework of TR-EIF.

The volume establishes the complete atomistic modeling chain:

`atomic configuration`

`→ interaction graph`

`→ E(3) group actions`

`→ equivariant representations`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy functional`

`→ forces and stress`

`→ TR-EIP model family`.

The framework combines spatially structured interatomic modeling with the Ternary Resonance layer defined in Volume 02.

The canonical balanced ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

---

## 2. Volume Structure

Volume 03 consists of eleven chapters.

### Chapter 01 — Atomic Configuration Space

Defines:

- atomic positions;
- species;
- masses;
- velocities where required;
- simulation cells;
- periodic boundaries;
- Cartesian and fractional coordinates;
- relative geometry;
- local environments;
- configuration admissibility;
- translation, rotation, reflection, and permutation behavior.

### Chapter 02 — Interaction Graphs

Defines:

- graph nodes;
- directed and undirected edges;
- source/receiver semantics;
- geometric edge features;
- radius and k-nearest-neighbor graphs;
- periodic edges;
- dynamic graph construction;
- graph determinism;
- graph symmetry;
- multiscale graph structure.

### Chapter 03 — E(3) Group Actions

Defines:

- `SO(3)`;
- `O(3)`;
- `SE(3)`;
- `E(3)`;
- translations;
- rotations;
- reflections;
- parity;
- atom permutations;
- scalar, vector, tensor, polar, axial, and pseudoscalar transformation laws.

### Chapter 04 — Equivariant Representations

Defines:

- invariant scalar features;
- equivariant vector and tensor features;
- irreducible representation channels;
- parity;
- spherical harmonics;
- radial-angular decomposition;
- tensor products;
- Clebsch-Gordan coupling;
- equivariant nonlinearities;
- representation validation.

### Chapter 05 — Message Passing

Defines:

- directed message functions;
- receiver-oriented semantics;
- permutation-safe aggregation;
- equivariant updates;
- local and nonlocal propagation;
- recurrence;
- multiscale message transfer;
- deterministic message evaluation;
- interfaces to resonance and ternary state.

### Chapter 06 — Resonance Parameterization

Defines:

- local resonance state;
- edge resonance state;
- cluster resonance state;
- global resonance state;
- multiscale resonance;
- resonance transformation laws;
- resonance windows;
- resonance classification;
- retained resonance memory;
- EIF-to-TR coupling.

### Chapter 07 — Ternary Feature Channels

Defines:

- exact `-1/0/1` feature channels;
- active neutral;
- local, edge, cluster, and global ternary state;
- continuous-to-ternary mapping;
- target state;
- executed state;
- pending routes;
- hysteresis;
- persistence;
- ternary-conditioned representations and energy.

### Chapter 08 — Conservative Energy Functional

Defines:

- invariant scalar energy;
- local and many-body energy;
- resonance-conditioned energy;
- ternary-conditioned energy;
- energy surfaces;
- differentiability;
- conservative force relation;
- energy conservation interfaces;
- periodic-cell energy.

### Chapter 09 — Forces and Stress

Defines:

- atomic force;
- conservative and direct force paths;
- force equivariance;
- energy-force consistency;
- stress tensors;
- cell/strain interfaces;
- virial boundaries;
- force and stress validation.

### Chapter 10 — Model Family TR-EIP

Defines:

- complete TR-EIP architecture;
- model-family identity;
- architecture parameters;
- learned and calibrated parameters;
- model manifests;
- deterministic runtime;
- validation contracts;
- interfaces to Volumes 04–07.

### Chapter 11 — Volume Summary

Consolidates the complete Equivariant Interatomic Framework and closes Volume 03.

---

## 3. Atomic Configuration Foundation

The atomic configuration is the primary geometric state.

For:

`N`

atoms:

`R = (r_1, ..., r_N)`.

Each:

`r_i ∈ R^3`.

Species state is:

`A_N = (a_1, ..., a_N)`.

A minimal configuration is:

`X_conf = (R, A_N)`.

---

## 4. Periodic Configuration

For periodic systems, the configuration includes cell matrix:

`H ∈ R^(3×3)`.

The cell must satisfy:

`det(H) ≠ 0`.

The cell volume is:

`V_cell = |det(H)|`.

---

## 5. Fractional Coordinates

For fractional coordinate:

`s_i`:

`r_i = H s_i`.

Periodic image equivalence is represented through integer lattice translations.

---

## 6. Relative Geometry

For atoms:

`i`

and:

`j`:

`r_ij = r_j - r_i`

under the applicable image convention.

The pair distance is:

`d_ij = ||r_ij||`.

---

## 7. Geometric Symmetry

Relative geometry preserves:

`r_ji = -r_ij`

and:

`d_ji = d_ij`.

Distances are translation and rotation invariant.

Relative displacement is translation invariant and rotation equivariant.

---

## 8. Atomic Configuration Is Not Derived State

The framework preserves:

`atomic configuration ≠ interaction graph`

`atomic configuration ≠ equivariant representation`

`atomic configuration ≠ resonance state`

`atomic configuration ≠ ternary state`

`atomic configuration ≠ energy`

`atomic configuration ≠ force`

`atomic configuration ≠ stress`.

---

## 9. Interaction Graph

The interaction graph is:

`G = (V,E)`.

Each atom corresponds to one graph node.

A directed edge:

`j → i`

represents a model-defined information or interaction relation from source:

`j`

to receiver:

`i`.

---

## 10. Source/Receiver Convention

The canonical edge convention uses:

`j → i`

with:

`r_ij = r_j - r_i`.

This convention remains fixed throughout graph, message, resonance, energy, and validation layers.

---

## 11. Graph Edge Semantics

An interaction edge is a computational or model-defined relation.

The framework preserves:

`interaction edge ≠ chemical bond`

`interaction edge ≠ mechanical force`

`interaction edge ≠ resonance`

`interaction edge ≠ ternary state`.

---

## 12. Graph Construction

A graph is generated through:

`P_G: X_conf → X_G`.

The mapping may depend on:

- cutoff;
- species;
- periodicity;
- topology;
- local state;
- model parameters.

---

## 13. Radius Graph

A local radius graph may define:

`j ∈ N_i`

when:

`d_ij ≤ r_cut`.

The cutoff:

`r_cut`

is model-specific.

---

## 14. Dynamic Graph

For evolving geometry:

`G(t) = P_G(X_conf(t))`.

Continuous coordinate motion may therefore produce discrete graph-topology changes.

---

## 15. Graph Transition Boundary

The framework preserves:

`graph edge event ≠ structural transition`

`graph topology change ≠ resonance transition`

`graph topology change ≠ ternary transition`

`graph topology change ≠ physical phase transition`.

---

## 16. Graph Permutation Equivariance

For atom permutation:

`pi`

graph construction satisfies:

`P_G(pi · X) = pi · P_G(X)`

under the declared graph contract.

---

## 17. E(3) Structure

The Euclidean group is:

`E(3) = O(3) ⋉ R^3`.

A group element may be represented:

`g = (Q,c)`.

Its action is:

`r_i' = Q r_i + c`.

---

## 18. SO(3)

Proper rotations satisfy:

`Q^T Q = I`

and:

`det(Q) = 1`.

They form:

`SO(3)`.

---

## 19. O(3)

Orthogonal transformations satisfy:

`Q^T Q = I`

and:

`det(Q) ∈ {-1,1}`.

They form:

`O(3)`.

---

## 20. SE(3)

When reflections are excluded:

`SE(3) = SO(3) ⋉ R^3`.

---

## 21. Spatial Transformation of Relative Geometry

Under:

`r_i' = Qr_i + c`

the relative vector satisfies:

`r_ij' = Q r_ij`.

The translation cancels.

---

## 22. Distance Invariance

Because:

`Q`

is orthogonal:

`||Q r_ij|| = ||r_ij||`.

Therefore:

`d_ij' = d_ij`.

---

## 23. Atom Permutations

Atom relabeling is a separate symmetry from spatial transformation.

The applicable permutation group exchanges atoms consistently with species identity.

---

## 24. Spatial and Permutation Symmetry

TR-EIP may carry a combined action:

`E(3) × S_species`.

Spatial transformations act on geometric state.

Permutations act on indexing.

---

## 25. Equivariance

For map:

`F: X → Y`

equivariance means:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

---

## 26. Invariance

A scalar invariant satisfies:

`F(rho_X(g)x) = F(x)`.

---

## 27. Equivariance versus Invariance

The distinction remains:

`equivariance ≠ invariance`.

Invariant outputs remain numerically unchanged.

Equivariant outputs transform according to a declared representation.

---

## 28. Scalar Representation

A scalar channel is invariant under spatial rotation.

In rotational irrep notation:

`l = 0`.

---

## 29. Vector Representation

A polar vector transforms:

`v' = Qv`.

The standard vector representation corresponds to:

`l = 1`.

---

## 30. Tensor Representation

A rank-two tensor transforms:

`T' = Q T Q^T`.

---

## 31. Parity

Under:

`O(3)`

a representation may additionally carry parity.

Scalar and pseudoscalar channels differ under orientation reversal.

Polar and axial vectors also differ under parity.

---

## 32. Irreducible Representations

For:

`SO(3)`

irreducible representation degree:

`l`

has dimension:

`2l + 1`.

---

## 33. Angular Representation

Directional information may be represented through spherical harmonics:

`Y_lm(e_hat_ij)`.

---

## 34. Radial Representation

Invariant radial features may be constructed from:

`d_ij`.

A radial basis is:

`R_n(d_ij)`.

---

## 35. Radial-Angular Decomposition

A geometric basis may be:

`R_n(d_ij) Y_lm(e_hat_ij)`.

The radial part is invariant.

The angular part carries equivariant structure.

---

## 36. Tensor Products

Representation channels may be coupled through tensor products.

For degrees:

`l_1`

and:

`l_2`

the permitted output degrees satisfy:

`|l_1-l_2| ≤ l ≤ l_1+l_2`.

---

## 37. Clebsch-Gordan Coupling

The decomposition of tensor products into irreducible channels uses the appropriate Clebsch-Gordan structure or equivalent representation basis transformation.

---

## 38. Representation Mapping

The EIF representation mapping is:

`P_EQ: X_conf × X_G → X_EQ`.

It satisfies:

`P_EQ(rho_in(g)x) = rho_EQ(g)P_EQ(x)`.

---

## 39. Representation Type Separation

The framework preserves:

`scalar ≠ vector`

`vector ≠ tensor`

`scalar ≠ pseudoscalar`

`polar vector ≠ axial vector`.

---

## 40. Representation Is Not Physical Output

The framework preserves:

`generic scalar ≠ energy`

`generic vector ≠ force`

`generic tensor ≠ stress`.

---

## 41. Message Passing

For edge:

`j → i`

a message is:

`m_ij = M(h_i,h_j,e_ij,g)`.

---

## 42. Message Aggregation

For receiver:

`i`:

`m_i = A({m_ij | j ∈ N_i})`.

The aggregation must be independent of arbitrary neighbor ordering.

---

## 43. Node Update

The receiver node update is:

`h_i' = U(h_i,m_i,g)`.

---

## 44. Message Equivariance

Messages preserve their declared representation type under spatial transformation.

---

## 45. Permutation-Safe Aggregation

Summation:

`m_i = sum_(j ∈ N_i) m_ij`

is invariant to neighbor ordering.

---

## 46. Message State Boundary

The framework preserves:

`message ≠ edge`

`message ≠ force`

`message ≠ energy`

`message ≠ chemical bond`

`message ≠ resonance`

`message ≠ ternary state`.

---

## 47. Message Depth

Repeated message passing creates:

`X_EQ^[0]`

`→ X_EQ^[1]`

`→ ...`

`→ X_EQ^[L]`.

The layer index is computational depth.

---

## 48. Message Depth versus Physical Time

The distinction remains:

`message-passing depth ≠ physical time`.

---

## 49. Message Depth versus Ternary Tact

The distinction remains:

`message-passing layer ≠ ternary execution tact`.

---

## 50. Receptive Field

Multiple message layers enlarge the graph-hop receptive field.

Graph-hop range is not identical to physical interaction range.

---

## 51. Resonance Parameterization

The resonance mapping is:

`P_R: X_EQ → X_R`.

A state-augmented form may additionally consume:

- graph state;
- geometry;
- phase state;
- history;
- global state.

---

## 52. Local Resonance State

For atom:

`i`:

`r_i ∈ X_R,local`.

---

## 53. Edge Resonance State

For edge:

`j → i`:

`r_ij ∈ X_R,edge`.

---

## 54. Cluster Resonance State

For cluster:

`C_a`:

`r_a ∈ X_R,cluster`.

---

## 55. Global Resonance State

For the complete system:

`r_G ∈ X_R,global`.

---

## 56. Multiscale Resonance

At scale:

`ell`:

`r^(ell) ∈ X_R^(ell)`.

Different scales may occupy different resonance regimes simultaneously.

---

## 57. Resonance Symmetry

A resonance map satisfies:

`P_R(rho_EQ(g)x) = rho_R(g)P_R(x)`.

---

## 58. Scalar Resonance

A scalar resonance coordinate remains invariant under the declared spatial symmetry.

---

## 59. Vector Resonance

A vector resonance coordinate transforms equivariantly.

---

## 60. Resonance Window

A resonance window is:

`W_R ⊂ X_R`.

Its boundary is:

`∂W_R`.

---

## 61. Resonance Classification

A minimal resonance classifier uses:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

---

## 62. Resonance Class Separation

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

---

## 63. Resonance State Separation

The framework preserves:

`geometry ≠ resonance`

`graph ≠ resonance`

`equivariant representation ≠ resonance`

`message state ≠ resonance`.

---

## 64. Resonance Scientific Separation

The framework preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`.

---

## 65. Phase Order and Coherence

The canonical distinction remains:

`R(t) ≠ C(t)`.

---

## 66. Phase Interface

An EIF resonance mapping may consume oscillator phase state when such coupling is explicitly defined.

---

## 67. Oscillator Phase

Oscillator phase belongs to:

`S^1`.

It remains distinct from geometric orientation.

---

## 68. Phase Lag

A Sakaguchi phase lag is angular.

It is not explicit temporal delay.

---

## 69. Phase Coupling Boundary

The framework preserves:

`phase coupling ≠ mechanical force`.

---

## 70. Phase Relation Boundary

The framework preserves:

`phase relation ≠ chemical bond`.

---

## 71. Ternary Feature Domain

Ternary feature channels use exactly:

`T = {-1,0,1}`.

The compact notation remains:

`-1/0/1`.

---

## 72. Active Neutral

The state:

`0`

is active neutral.

It is a valid semantic state.

---

## 73. Active-Neutral Separation

The framework preserves:

`0 ≠ NONE`

`0 ≠ INVALID`

`0 ≠ NaN`

`0 ≠ MASKED`

`0 ≠ PADDING`

`0 ≠ zero vector`

`0 ≠ zero message`.

---

## 74. Ternary Mapping

A ternary feature is generated through:

`P_T: X_source → {-1,0,1}`.

---

## 75. Resonance-to-Ternary Mapping

A principal map is:

`P_RT: X_R → T_target`.

---

## 76. Exact Categorical Output

After classification:

`t ∈ {-1,0,1}`

exactly.

---

## 77. Scalar Threshold Mapping

For scalar:

`z`

one possible classifier is:

`z < eta_- → -1`

`eta_- ≤ z ≤ eta_+ → 0`

`z > eta_+ → 1`.

The thresholds are model-specific.

---

## 78. Multidimensional Mapping

For:

`z ∈ R^m`

decision regions may be:

`D_-`

`D_0`

`D_+`.

---

## 79. Ternary Feature Scales

Ternary channels may exist at:

- edge scale;
- atom scale;
- cluster scale;
- global scale;
- multiple scales simultaneously.

---

## 80. Ternary Feature versus Execution State

The framework preserves:

`ternary feature ≠ executed state`

unless a channel is explicitly defined as the execution state.

---

## 81. Target State

Execution-bound classification produces:

`t_target`.

---

## 82. Executed State

Committed state is:

`t_exec`.

---

## 83. Target/Execution Boundary

The invariant remains:

`target ≠ executed state`.

---

## 84. Pending Route

Opposite-polarity routing may retain:

`t_pending ∈ {-1,1}`

or:

`NONE`.

---

## 85. NONE versus Neutral

The distinction remains:

`NONE ≠ 0`.

---

## 86. Canonical Execution Graph

Committed execution uses:

`-1 ↔ 0 ↔ 1`.

---

## 87. Allowed State-Changing Edges

The canonical state-changing edges are:

`-1 → 0`

`0 → -1`

`0 → 1`

`1 → 0`.

---

## 88. Forbidden State-Changing Edges

Direct committed:

`-1 → 1`

and:

`1 → -1`

are forbidden.

---

## 89. Opposite Route

An opposite target requires:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

---

## 90. First Leg

The first leg enters active neutral.

---

## 91. Neutral Residence

The neutral state may persist for multiple execution opportunities.

---

## 92. Second Leg

The second leg leaves neutral toward the pending destination.

---

## 93. Algebraic Negation Boundary

Numeric negation:

`-1 ↔ 1`

is an algebraic operation.

It is not a direct committed transition.

---

## 94. Ternary Feature and Message Passing

A ternary channel may condition message passing through an explicit mapping.

---

## 95. Active-Neutral Message Policy

Active neutral does not require a zero message.

A model may define a distinct:

`M_0`.

---

## 96. Ternary Feature and Resonance Feedback

Ternary state may feed back into later resonance parameterization.

The source channel must be explicit.

---

## 97. Ternary Feature and Energy

Ternary state may condition energy.

The distinction remains:

`ternary state ≠ energy`.

---

## 98. Conservative Energy Functional

A conservative energy functional is:

`E: X_conf × X_aux → R`.

Its output is a scalar physical energy.

---

## 99. Energy Symmetry

For the declared rigid spatial symmetry:

`E(gX) = E(X)`.

---

## 100. Energy Permutation Invariance

For admissible atom permutation:

`E(pi · X) = E(X)`.

---

## 101. Energy Units

Energy carries declared physical units.

Latent invariant scalars do not become energy without an explicit energy head.

---

## 102. Energy Decomposition

A model may use:

`E = sum_i E_i`.

Local energy decomposition is not necessarily unique.

---

## 103. Many-Body Energy

TR-EIP supports many-body energy dependence through local environments and message-passed state.

---

## 104. Long-Range Energy

A model may combine:

`E = E_local + E_long`.

The long-range term must define its own physical and numerical contract.

---

## 105. Resonance-Conditioned Energy

A model may use:

`E = F_E(X_EQ,X_R)`.

---

## 106. Ternary-Conditioned Energy

A model may use:

`E = F_E(X_EQ,X_R,X_T)`.

---

## 107. Mode-Specific Energy Surfaces

Executed ternary state may select:

`E_-1`

`E_0`

`E_1`.

---

## 108. Neutral Energy Surface

The framework preserves:

`E_0 ≠ 0`

by identity.

---

## 109. Ternary Sign versus Energy Sign

The framework preserves:

`ternary -1 ≠ negative energy`

`ternary 1 ≠ positive energy`.

---

## 110. Conservative Force

For differentiable energy:

`F_i = -grad_(r_i) E`.

---

## 111. Force Equivariance

Under rigid rotation:

`F_i(QR) = QF_i(R)`.

---

## 112. Force Permutation Equivariance

Per-atom forces permute consistently with atom labels.

---

## 113. Generic Vector versus Force

The framework preserves:

`generic vector ≠ force`.

---

## 114. Message Vector versus Force

The framework preserves:

`message vector ≠ force`.

---

## 115. Resonance Vector versus Force

The framework preserves:

`resonance vector ≠ force`.

---

## 116. Ternary State versus Force

The framework preserves:

`ternary state ≠ force`.

---

## 117. Zero Force versus Active Neutral

The framework preserves:

`zero force ≠ active-neutral 0`.

---

## 118. Direct Force Model

A model may predict an equivariant force directly.

Such a force is not conservative by identity.

---

## 119. Equivariance versus Conservativity

The canonical distinction remains:

`equivariance ≠ conservativity`.

---

## 120. Energy-Force Consistency

For a conservative model:

`F + grad_R E = 0`.

This relation is exact at the formal level.

---

## 121. Stress

Stress is a second-order tensor:

`Sigma ∈ R^(3×3)`.

---

## 122. Stress Transformation

Under rigid rotation:

`Sigma' = Q Sigma Q^T`.

---

## 123. Stress Units

Stress carries:

`energy / volume`

or equivalent mechanical units.

---

## 124. Stress Type

A concrete model must specify whether reported stress is:

- Cauchy stress;
- Piola-Kirchhoff stress;
- virial stress;
- another explicitly defined tensor.

---

## 125. Stress versus Generic Tensor

The framework preserves:

`generic tensor ≠ stress`.

---

## 126. Resonance Tensor versus Stress

The framework preserves:

`resonance tensor ≠ stress`.

---

## 127. Ternary State versus Stress

The framework preserves:

`ternary state ≠ stress`.

---

## 128. Zero Stress versus Active Neutral

The framework preserves:

`zero stress ≠ active-neutral 0`.

---

## 129. Cell-Strain Interface

For periodic systems:

`E = E(R,H)`.

Stress may be derived through an explicitly declared derivative with respect to cell or strain state.

---

## 130. Rotation versus Deformation

The distinction remains:

`rotation ≠ deformation`.

Rigid rotation preserves the metric.

Strain changes metric structure.

---

## 131. Pressure versus Stress

The framework preserves:

`pressure ≠ stress tensor`.

Pressure may be derived as a scalar from stress under a declared convention.

---

## 132. TR-EIP Model Family

The complete model family is:

`M_TR-EIP`.

A concrete member may be represented:

`M = (AC,IG,SG,ER,MP,RP,TF,CEF,MECH,P,N,V)`.

---

## 133. Architecture State

The architecture defines:

- configuration domain;
- graph;
- symmetry;
- representation;
- messages;
- resonance;
- ternary channels;
- energy;
- force;
- stress.

---

## 134. Parameter State

The parameter state may be partitioned:

`P = P_fixed × P_learned × P_cal × P_num`.

---

## 135. Fixed Parameters

Fixed parameters define architecture or analytic model quantities.

---

## 136. Learned Parameters

Learned parameters are optimized from declared data and objectives.

---

## 137. Calibrated Parameters

Calibrated parameters are estimated against declared reference observables or datasets.

---

## 138. Numerical Parameters

Numerical parameters define the implementation realization.

---

## 139. Model Identity

Changing any result-affecting architecture, parameter, or numerical rule may create a different model instance or model version.

---

## 140. Model Manifest

A model manifest identifies:

- model architecture;
- parameter artifact;
- supported species;
- unit system;
- symmetry;
- graph rule;
- representation;
- resonance structure;
- ternary structure;
- output capabilities;
- numerical semantics;
- provenance.

---

## 141. Model Domain

A concrete model declares its admissible configuration domain.

---

## 142. Out-of-Domain State

Out-of-domain status is not a ternary state.

The framework preserves:

`OUT_OF_DOMAIN ≠ 0`.

---

## 143. Model Output

A full model may output:

`Y = (X_R,X_T,E,F,Sigma,U)`.

Here:

`U`

may contain uncertainty or auxiliary observables.

---

## 144. Stateful Model

A model may retain:

- resonance memory;
- ternary hysteresis;
- pending routes;
- scheduler state;
- recurrent representation state;
- adaptive parameters.

---

## 145. Restart Completeness

Every result-affecting retained state belongs to the restart contract.

---

## 146. Deterministic Model

For deterministic execution, identical complete:

- input;
- model state;
- parameters;
- arithmetic;
- ordering

produce identical declared outputs under the replay contract.

---

## 147. Exact Categorical Replay

Ternary states are compared exactly.

---

## 148. Continuous Numerical Replay

Continuous outputs may be compared:

- exactly;
- byte-identically;
- within declared tolerance.

The comparison contract must be explicit.

---

## 149. Graph Determinism

Graph construction must use deterministic conventions when exact replay requires it.

---

## 150. Reduction Determinism

Floating-point aggregation ordering may affect exact numerical results.

Canonical ordering may therefore belong to the implementation contract.

---

## 151. Symmetry Validation

A complete model may be tested under:

- translation;
- rotation;
- reflection where applicable;
- atom permutation;
- combined transformations.

---

## 152. Energy Validation

Energy validation verifies:

- scalar invariance;
- permutation invariance;
- units;
- finite output;
- periodic consistency.

---

## 153. Force Validation

Force validation verifies:

- vector equivariance;
- permutation equivariance;
- gradient consistency for conservative models.

---

## 154. Stress Validation

Stress validation verifies:

- tensor transformation;
- sign convention;
- unit convention;
- cell/strain consistency.

---

## 155. Resonance Validation

Resonance validation verifies:

- state domain;
- transformation law;
- window semantics;
- classifier;
- memory;
- replay.

---

## 156. Ternary Validation

Ternary validation verifies:

`t ∈ {-1,0,1}`

exactly.

---

## 157. Active-Neutral Validation

Validation must preserve:

`0`

as a valid active semantic state.

---

## 158. Target/Execution Validation

Target and executed states remain separately serialized and validated.

---

## 159. Opposite-Route Validation

Execution validation confirms:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 160. Direct-Opposite Rejection

Execution validation rejects:

`-1 → 1`

and:

`1 → -1`.

---

## 161. Provenance System

Volume 03 preserves the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 162. Primary-Source Layer

Established mathematical and scientific structures retain:

`PRIMARY_SOURCE`

provenance.

Examples include:

- Euclidean group theory;
- representation theory;
- spherical harmonics;
- conservative-force relations.

---

## 163. Derived Layer

Quantities derived from declared source state retain:

`DERIVED`

provenance where applicable.

Examples include:

- force from energy gradient;
- graph from atomic configuration;
- resonance coordinates from representation state.

---

## 164. Calibrated Layer

Fitted model quantities retain:

`CALIBRATED`

provenance.

---

## 165. Author-Defined Layer

TR-EIF-specific architectural constructs retain:

`AUTHOR_DEFINED`

provenance where applicable.

These include integration structures among:

- resonance;
- balanced ternary semantics;
- equivariant interatomic state;
- active-neutral execution.

---

## 166. Benchmark Layer

Measured numerical and computational results retain:

`BENCHMARK`

provenance.

---

## 167. Test Fixtures

Controlled deterministic examples retain:

`TEST_FIXTURE`

provenance.

---

## 168. FRP Executable Reference

FRP provides executable reference behavior for selected ternary-resonant execution mechanisms.

Its relation to TR-EIF remains:

`FRP ≠ TR-EIF`.

Its relation to TR-EIP remains:

`FRP ≠ TR-EIP`.

---

## 169. FRP Role

FRP contributes executable reference semantics for selected mechanisms including:

- phase evolution;
- phase-to-target mapping;
- target registration;
- scheduler operation;
- pending routing;
- active neutral;
- retained ternary execution;
- deterministic qualification artifacts.

---

## 170. FRP Ternary Kernel

FRP preserves:

`-1/0/1`.

---

## 171. FRP Active Neutral

FRP preserves active neutral:

`0`.

---

## 172. FRP Opposite Routes

FRP preserves:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 173. FRP Phase Coupling

The applicable FRP phase interaction uses:

`sin(theta_j - theta_i - gamma_effective_i)`.

---

## 174. FRP Nominal Lag

The executable specialization uses:

`gamma_nominal = 0.30 pi`.

This remains FRP-specific.

---

## 175. FRP Coupling Baseline

The executable specialization uses:

`K_0 = 0.28`.

This remains FRP-specific.

---

## 176. FRP Retained Frequency

FRP contains retained-frequency memory.

The target-frequency mechanism remains implementation-specific.

---

## 177. FRP Phase Order

FRP computes:

`R = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

The distinction remains:

`R(t) ≠ C(t)`.

---

## 178. FRP Phase-to-Target Mapping

The executable reference uses:

`sin(theta_i)`

with threshold magnitude:

`0.33`.

---

## 179. FRP Positive Target

`sin(theta_i) > 0.33 → 1`.

---

## 180. FRP Negative Target

`sin(theta_i) < -0.33 → -1`.

---

## 181. FRP Neutral Target

The intermediate region maps to:

`0`.

---

## 182. FRP Threshold Scope

The value:

`0.33`

is an FRP specialization parameter.

It is not a universal TR-EIP parameter.

---

## 183. FRP Scheduler Modes

FRP includes:

`7/1`

and:

`1/7`.

---

## 184. FRP 7/1 Mode

The `7/1` mode is:

`seven balance tacts → one commit tact`.

---

## 185. FRP 1/7 Mode

The `1/7` mode is:

`one excite tact → seven neutralize tacts`.

---

## 186. FRP Execution Qualification

Applicable qualified artifacts preserve:

`actual_direct_events = 0`

`reserved_state_events = 0`

`queue_overflow_events = 0`

under the corresponding qualified configuration.

---

## 187. FRP Scope Boundary

FRP-specific:

- thresholds;
- scheduler ratios;
- coupling parameters;
- phase lag;
- retained-frequency parameters

remain executable specialization values.

They do not become universal TR-EIF constants.

---

## 188. TR-EIP Model Hierarchy

The model hierarchy is:

`TR-EIF`

`→ TR-EIP model family`

`→ concrete architecture`

`→ parameterized model instance`

`→ material specialization`

`→ runtime state`.

---

## 189. Volume 03 Canonical Forward Chain

The complete forward chain is:

`atomic configuration`

`→ interaction graph`

`→ group action`

`→ equivariant representation`

`→ message passing`

`→ resonance state`

`→ ternary feature state`

`→ energy`

`→ force/stress`.

---

## 190. Volume 03 Canonical TR Chain

The TR-facing chain is:

`X_EQ`

`→ X_R`

`→ T_target`

`→ scheduler/routing`

`→ T_exec`.

---

## 191. Volume 03 Canonical Mechanical Chain

The conservative mechanical chain is:

`X_conf`

`→ X_EQ`

`→ X_R`

`→ X_T`

`→ E`

`→ -grad_R E`

`→ F`.

---

## 192. Volume 03 Canonical Stress Chain

For cell-dependent models:

`X_conf + H`

`→ E`

`→ cell/strain derivative`

`→ Sigma`.

---

## 193. Volume 03 Canonical Feedback Chain

A coupled realization may use:

`T_exec`

`+ X_R`

`+ X_EQ`

`→ next representation / resonance / energy parameterization`.

Every feedback path remains explicit.

---

## 194. Volume 03 Canonical Multiscale Chain

A multiscale model may use:

`edge`

`→ atom`

`→ cluster`

`→ global`

states in:

- equivariant representation;
- resonance;
- ternary channels.

---

## 195. Canonical State Separation

Volume 03 preserves:

`configuration ≠ graph`

`graph ≠ representation`

`representation ≠ message`

`message ≠ resonance`

`resonance ≠ ternary state`

`ternary target ≠ executed state`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`.

---

## 196. Canonical Geometry Separation

Volume 03 preserves:

`geometric angle ≠ oscillator phase`

`relative vector ≠ mechanical force`

`graph distance ≠ Euclidean distance`

`graph density ≠ material density`.

---

## 197. Canonical Graph Separation

Volume 03 preserves:

`interaction edge ≠ chemical bond`

`interaction edge ≠ pair force`

`graph mask ≠ active-neutral state`

`graph topology change ≠ structural transition`.

---

## 198. Canonical Representation Separation

Volume 03 preserves:

`scalar channel ≠ energy`

`vector channel ≠ force`

`tensor channel ≠ stress`

`representation norm ≠ physical energy`.

---

## 199. Canonical Resonance Separation

Volume 03 preserves:

`resonance ≠ synchronization`

`resonance ≠ phase locking`

`resonance ≠ coherence`

`resonance classification ≠ energy`

`resonance classification ≠ ternary state`.

---

## 200. Canonical Ternary Separation

Volume 03 preserves:

`ternary 0 ≠ zero energy`

`ternary 0 ≠ zero force`

`ternary 0 ≠ zero vector`

`ternary 0 ≠ missing state`

`ternary negation ≠ direct executed reversal`.

---

## 201. Canonical Mechanical Separation

Volume 03 preserves:

`equivariance ≠ conservativity`

`potential energy ≠ total mechanical energy`

`force ≠ acceleration`

`force ≠ momentum`

`pressure ≠ stress`

`virial tensor ≠ every stress definition by identity`.

---

## 202. Canonical Transition Distinctions

Volume 03 preserves:

`threshold crossing ≠ bifurcation`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`resonance transition ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 203. Canonical Phase Distinctions

Volume 03 preserves:

`oscillator phase ≠ geometric orientation`

`oscillator phase ≠ physical phase of matter`

`phase lag ≠ temporal delay`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`.

---

## 204. Canonical Ternary Invariants

Every conforming execution-bound TR-EIP realization preserves:

1. `T = {-1,0,1}`;

2. compact notation `-1/0/1`;

3. active neutral `0`;

4. target/execution separation;

5. pending-route separation;

6. forbidden committed `-1 → 1`;

7. forbidden committed `1 → -1`;

8. neutral-mediated opposite routing;

9. separate first and second commits;

10. possible neutral residence.

---

## 205. Canonical Equivariance Invariants

Every conforming TR-EIP realization preserves:

1. declared spatial group;

2. declared atom-permutation group;

3. explicit representation actions;

4. scalar invariance;

5. vector equivariance;

6. tensor equivariance;

7. parity semantics where applicable;

8. consistent periodic transformations.

---

## 206. Canonical Energy Invariants

Every conforming energy-capable member preserves:

1. scalar energy output;

2. declared physical units;

3. declared spatial invariance;

4. atom-permutation invariance;

5. explicit differentiability contract;

6. explicit provenance.

---

## 207. Canonical Force Invariants

Every conservative force member preserves:

`F_i = -grad_(r_i) E`.

Every direct-force member explicitly declares that force path separately.

---

## 208. Canonical Stress Invariants

Every stress-capable member preserves:

- explicit tensor type;
- explicit units;
- explicit sign convention;
- explicit cell/strain relation;
- rotation covariance.

---

## 209. Canonical Validation Invariants

Validation remains layered.

Separate validation applies to:

- configuration;
- graph;
- equivariance;
- representation;
- messages;
- resonance;
- ternary mapping;
- execution;
- energy;
- force;
- stress;
- deterministic replay.

---

## 210. Interface to Volume 04

Volume 04 develops Learning and Optimization.

The principal exported object from Volume 03 is the parameterized model family:

`M_TR-EIP(P)`.

Volume 04 will define:

- training data;
- target quantities;
- loss functionals;
- energy-force-stress training;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty;
- optimization.

---

## 211. Learning Boundary

Volume 03 defines the model structure.

Volume 04 defines how selected parameters are learned or optimized.

---

## 212. Trainable Parameter Set

A model may define:

`P_train ⊆ P`.

The remaining parameter state may remain fixed or calibrated.

---

## 213. Learning Does Not Redefine Semantics

Optimization may alter parameter values.

It does not alter:

- the meaning of `-1/0/1`;
- active-neutral semantics;
- force/energy type;
- symmetry transformation law

unless a new model architecture is explicitly defined.

---

## 214. Interface to Volume 05

Volume 05 develops Molecular Dynamics.

The principal mechanical outputs are:

`E`

`F`

`Sigma`.

The complete coupled state may also contain:

`X_R`

and:

`X_T`.

---

## 215. Molecular-Dynamics Boundary

TR-EIP supplies interatomic outputs.

The molecular-dynamics layer supplies:

- equations of motion;
- integration;
- thermostats;
- barostats;
- periodic evolution;
- trajectory observables.

---

## 216. Force versus Integrator

The distinction remains:

`interatomic force model ≠ molecular-dynamics integrator`.

---

## 217. Interface to Volume 06

Volume 06 develops Multiscale Materials Modeling.

Volume 03 exports:

- atomistic configuration;
- equivariant features;
- resonance state;
- ternary state;
- energy;
- force;
- stress

as inputs to cross-scale mappings.

---

## 218. Multiscale Boundary

Coarse-grained state remains distinct from atomistic state.

Cross-scale mappings must explicitly describe information loss and closure.

---

## 219. Interface to Volume 07

Volume 07 develops the FLiBe Reference Model.

It instantiates the general TR-EIP model family for a specific material system.

---

## 220. FLiBe Boundary

FLiBe is a material specialization.

It does not define the universal Volume 03 architecture.

---

## 221. Volume 03 Output Contract

Volume 03 exports the following principal objects:

`X_conf`

`X_G`

`X_EQ`

`X_R`

`X_T`

`E`

`F`

`Sigma`

`M_TR-EIP`.

---

## 222. Configuration Output

`X_conf`

provides atomistic geometry, species, and cell state.

---

## 223. Graph Output

`X_G`

provides relational interaction structure.

---

## 224. Equivariant Output

`X_EQ`

provides transformation-preserving atomistic representation.

---

## 225. Resonance Output

`X_R`

provides explicitly typed resonance state.

---

## 226. Ternary Output

`X_T`

provides exact:

`-1/0/1`

feature state.

---

## 227. Energy Output

`E`

provides scalar interatomic energy.

---

## 228. Force Output

`F`

provides per-atom mechanical vectors.

---

## 229. Stress Output

`Sigma`

provides a mechanical tensor under the declared convention.

---

## 230. Model-Family Output

`M_TR-EIP`

provides the complete parameterized interatomic model family.

---

## 231. Volume 03 Formal Structure

The complete EIF layer may be represented:

`EIF = (AC,IG,SG,ER,MP,RP,TF,CEF,MECH,M_TR-EIP)`.

---

## 232. AC Component

`AC`

defines atomic configuration space.

---

## 233. IG Component

`IG`

defines graph structure.

---

## 234. SG Component

`SG`

defines spatial and permutation symmetry.

---

## 235. ER Component

`ER`

defines equivariant representation.

---

## 236. MP Component

`MP`

defines graph information propagation.

---

## 237. RP Component

`RP`

defines resonance parameterization.

---

## 238. TF Component

`TF`

defines ternary feature channels.

---

## 239. CEF Component

`CEF`

defines conservative energy.

---

## 240. MECH Component

`MECH`

defines force and stress.

---

## 241. Model-Family Component

`M_TR-EIP`

binds these components into concrete model instances.

---

## 242. Integrated Forward Mapping

A complete model evaluation may be represented conceptually as:

`X_conf`

`→ P_G`

`→ X_G`

`→ P_EQ`

`→ X_EQ`

`→ MP`

`→ X_EQ'`

`→ P_R`

`→ X_R`

`→ P_T`

`→ X_T`

`→ E`

`→ F,Sigma`.

---

## 243. Execution-Bound Ternary Mapping

When a ternary channel participates in retained execution:

`X_R`

`→ t_target`

`→ target registration`

`→ scheduler`

`→ routing`

`→ t_exec`.

---

## 244. Feedback Mapping

A coupled model may define:

`F_feedback: X_EQ × X_R × X_T → X_next_request`.

The exact destination may include:

- representation parameters;
- resonance parameters;
- energy parameters;
- graph control;
- continuous state.

---

## 245. Formal Symmetry Relation

For a declared group action:

`M(gX)`

must transform according to the declared output representation.

For scalar energy:

`E(gX) = E(X)`.

For force:

`F(gX) = rho_F(g)F(X)`.

For stress:

`Sigma(gX) = Q Sigma(X) Q^T`.

---

## 246. Formal Conservative Relation

For conservative force:

`F = -grad_R E`.

---

## 247. Formal Ternary Relation

For execution-bound ternary state:

`T_exec = {-1,0,1}`

with graph:

`-1 ↔ 0 ↔ 1`.

---

## 248. Formal Resonance Relation

Resonance is produced through:

`P_R: X_EQ → X_R`

or a declared state-augmented mapping.

---

## 249. Formal Model-Family Relation

The model family may be written:

`M_TR-EIP = {M(theta) | theta ∈ Theta_arch × Theta_param × Theta_num}`.

---

## 250. Architecture Parameter Space

`Theta_arch`

contains architecture choices such as:

- graph;
- symmetry;
- representation;
- message structure;
- resonance structure;
- ternary structure;
- energy structure;
- force/stress path.

---

## 251. Parameter Space

`Theta_param`

contains fixed, learned, and calibrated model parameters.

---

## 252. Numerical Space

`Theta_num`

contains numerical realization choices.

---

## 253. Model Runtime Map

A stateful model may be written:

`(Y,S_next) = M(X,S_current;P)`.

---

## 254. Complete Runtime State

Runtime state may include:

- atomic state;
- graph cache;
- equivariant recurrent state;
- resonance memory;
- ternary hysteresis state;
- target;
- executed state;
- pending destination;
- scheduler state.

---

## 255. Volume Closure

Volume 03 establishes the complete Equivariant Interatomic Framework of TR-EIF.

It defines atomic configuration space, interaction graphs, Euclidean symmetry actions, equivariant representations, message passing, resonance parameterization, balanced ternary feature channels, conservative energy, force, stress, and the TR-EIP model family.

The core atomistic architecture is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance`

`→ ternary state`

`→ energy`

`→ forces and stress`.

Spatial structure remains governed by explicit:

- translation;
- rotation;
- reflection where applicable;
- permutation;
- periodic-image

transformation contracts.

The interatomic representation remains equivariant.

Energy remains an invariant scalar.

Forces remain equivariant vectors.

Stress remains a tensor.

Resonance remains separately typed from geometry, coherence, synchronization, energy, and ternary state.

The balanced ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Target and executed state remain distinct.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The required opposite-polarity execution routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

The framework preserves the scientific and mathematical distinctions required throughout TR-EIF:

`configuration ≠ graph`

`graph ≠ representation`

`representation ≠ resonance`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`resonance ≠ ternary state`

`ternary target ≠ executed state`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`

`interaction edge ≠ chemical bond`

`phase relation ≠ chemical bond`

`phase coupling ≠ mechanical force`

`equivariance ≠ conservativity`

`threshold crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

Volume 03 therefore closes the complete TR-EIP interatomic architecture and exports the parameterized model family required by:

`Volume 04 — Learning and Optimization`.
