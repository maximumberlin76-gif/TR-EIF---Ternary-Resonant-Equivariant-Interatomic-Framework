# Equivariance Constraints

## 1. Purpose

This chapter defines equivariance constraints for TR-EIP learning and optimization within TR-EIF.

The equivariance layer preserves the spatial and permutation transformation laws established in Volume 03 while model parameters are learned from data.

The canonical symmetry chain is:

`atomic configuration`

`→ symmetry transformation`

`→ graph transformation`

`→ equivariant representation`

`→ message passing`

`→ resonance transformation`

`→ ternary feature transformation`

`→ invariant energy`

`→ equivariant force`

`→ tensorial stress`.

Equivariance constraints apply to:

- atomic configurations;
- interaction graphs;
- node features;
- edge features;
- irreducible representations;
- messages;
- resonance state;
- ternary channels;
- energy;
- force;
- stress;
- uncertainty outputs where applicable.

---

## 2. Group Action

Let:

`G`

denote the declared symmetry group.

A group element is:

`g ∈ G`.

For a state space:

`X`

the group action is:

`rho_X(g)`.

---

## 3. Equivariance

A mapping:

`F: X → Y`

is equivariant when:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

This relation must hold for every admissible:

`x ∈ X`

and:

`g ∈ G`.

---

## 4. Invariance

A mapping is invariant when the output representation is trivial:

`F(rho_X(g)x) = F(x)`.

---

## 5. Equivariance versus Invariance

The distinction remains:

`equivariance ≠ invariance`.

Invariant output remains numerically unchanged.

Equivariant output transforms according to its representation.

---

## 6. Spatial Symmetry Groups

A TR-EIP model may declare:

- `SO(3)`;
- `O(3)`;
- `SE(3)`;
- `E(3)`;
- an explicitly defined subgroup.

The exact symmetry group is part of model identity.

---

## 7. Euclidean Transformation

For:

`g = (Q,c)`

the atomic coordinate action is:

`r_i' = Qr_i + c`.

Here:

`Q`

is orthogonal and:

`c`

is a translation vector.

---

## 8. Relative Vector Transformation

For:

`r_ij = r_j - r_i`

the transformed relative vector is:

`r_ij' = Qr_ij`.

Global translation cancels.

---

## 9. Distance Invariance

Pair distance:

`d_ij = ||r_ij||`

satisfies:

`d_ij' = d_ij`.

---

## 10. SO(3)

For:

`Q ∈ SO(3)`:

`Q^TQ = I`

and:

`det(Q) = 1`.

---

## 11. O(3)

For:

`Q ∈ O(3)`:

`Q^TQ = I`

and:

`det(Q) ∈ {-1,1}`.

---

## 12. Reflection

Improper orthogonal transformations have:

`det(Q) = -1`.

Reflection behavior must be explicit when the model declares:

`O(3)`

or:

`E(3)`

symmetry.

---

## 13. Translation

Translation is represented by:

`c ∈ R^3`.

Internal geometric relations based on relative coordinates remain translation invariant.

---

## 14. Atom Permutation

Let:

`pi`

denote an admissible species-preserving atom permutation.

Permutation acts on atom indexing independently of spatial transformation.

---

## 15. Combined Symmetry

A complete atomistic transformation may contain:

`(g,pi)`.

Spatial and permutation transformations remain separate operations even when evaluated jointly.

---

## 16. Configuration Equivariance

The configuration state transforms as:

`X_conf' = rho_conf(g,pi)X_conf`.

---

## 17. Graph Equivariance

Graph construction:

`P_G`

must satisfy:

`P_G(rho_conf(g,pi)X) = rho_G(g,pi)P_G(X)`.

---

## 18. Graph Node Permutation

Node indices must permute consistently with atom indices.

---

## 19. Graph Edge Permutation

Directed edge:

`j → i`

becomes:

`pi(j) → pi(i)`.

---

## 20. Periodic Edge Transformation

Periodic-image displacement vectors must transform consistently with the cell and atomic coordinates.

---

## 21. Graph Topology under Rigid Transformations

A distance-based graph must preserve adjacency under rigid translation and rotation.

---

## 22. Reflection-Compatible Graph

A graph defined through reflection-invariant quantities such as distance preserves topology under reflection.

---

## 23. Graph Equivariance versus Graph Identity

The transformed graph need not have byte-identical indexing.

It must represent the correctly transformed and permuted relational structure.

---

## 24. Scalar Feature

A scalar feature:

`s`

transforms as:

`s' = s`.

---

## 25. Vector Feature

A polar vector:

`v`

transforms as:

`v' = Qv`.

---

## 26. Tensor Feature

A rank-two Cartesian tensor transforms:

`T' = QTQ^T`.

---

## 27. Pseudoscalar

A pseudoscalar may change sign under improper rotations according to its parity.

---

## 28. Axial Vector

An axial vector has parity behavior distinct from a polar vector.

---

## 29. Irreducible Representation

A representation channel of degree:

`l`

transforms through:

`D^l(Q)`.

---

## 30. Representation Multiplicity

Multiple channels may share the same:

`l`

and parity while carrying independent learned features.

---

## 31. Representation-Type Constraint

Training must not mix incompatible representation types through arbitrary learned operations.

---

## 32. Scalar-Vector Mixing Boundary

A scalar cannot be added directly to a vector without an explicit representation-compatible mapping.

---

## 33. Vector-Tensor Mixing Boundary

Likewise:

`vector ≠ tensor`.

---

## 34. Parity Constraint

Channels of different parity must remain distinct unless combined through a mathematically valid parity-aware operation.

---

## 35. Equivariant Linear Map

A linear map:

`L`

between representation spaces is equivariant when:

`L rho_X(g) = rho_Y(g)L`.

---

## 36. Learned Equivariant Linear Map

Trainable parameters may vary while the map structure preserves the commutation relation.

---

## 37. Tensor-Product Constraint

Tensor products must couple representation channels through permitted angular-momentum paths.

---

## 38. Angular Selection Rule

For:

`l_1`

and:

`l_2`

the output degree satisfies:

`|l_1-l_2| ≤ l ≤ l_1+l_2`.

---

## 39. Clebsch-Gordan Structure

Coupling coefficients or equivalent basis transforms must preserve the declared representation decomposition.

---

## 40. Radial Features

Radial features derived from distance are rotationally invariant.

---

## 41. Angular Features

Angular features transform according to their declared irreducible representation.

---

## 42. Spherical Harmonics

For directional unit vector:

`e_hat_ij`

spherical harmonics:

`Y_lm(e_hat_ij)`

provide angular representation channels.

---

## 43. Radial-Angular Product

A feature:

`R_n(d_ij)Y_lm(e_hat_ij)`

transforms according to the angular channel:

`l`.

---

## 44. Equivariant Nonlinearity

Nonlinear operations must preserve representation type.

---

## 45. Scalar Nonlinearity

An arbitrary scalar nonlinearity may act on invariant scalar channels.

---

## 46. Vector Gating

A vector may be multiplied by an invariant scalar gate:

`v' = a v`.

This preserves vector transformation.

---

## 47. Tensor Gating

A tensor or irrep channel may likewise be scaled by an invariant scalar.

---

## 48. Componentwise Nonlinearity Boundary

Applying an arbitrary nonlinear function independently to Cartesian vector components generally does not preserve rotation equivariance.

---

## 49. Norm-Based Nonlinearity

A vector may be transformed using its invariant norm and preserved direction through an equivariant construction.

---

## 50. Message Equivariance

For message:

`m_ij`

the message function must satisfy its declared transformation law.

---

## 51. Scalar Message

A scalar message remains invariant under rigid rotation.

---

## 52. Vector Message

A vector message transforms:

`m_ij' = Qm_ij`.

---

## 53. Higher-Order Message

Higher-order messages transform according to their representation.

---

## 54. Message Aggregation

Aggregation over incoming neighbors must preserve representation type.

---

## 55. Sum Aggregation

Summation of compatible equivariant features preserves equivariance.

---

## 56. Mean Aggregation

Mean aggregation also preserves equivariance when the denominator is an invariant scalar.

---

## 57. Weighted Aggregation

For:

`m_i = sum_j a_ij m_ij`

the weight:

`a_ij`

must be an invariant scalar if:

`m_ij`

is to retain its representation type.

---

## 58. Attention Weight

An attention weight applied to an equivariant message must have appropriate transformation behavior.

For scalar attention, it must be invariant.

---

## 59. Componentwise Maximum Boundary

A componentwise maximum over Cartesian vector components is not generally rotation equivariant.

---

## 60. Neighbor Ordering

Message aggregation must remain independent of arbitrary neighbor ordering.

---

## 61. Permutation Equivariance of Messages

Atom permutation must induce corresponding permutation of:

- source nodes;
- receiver nodes;
- messages;
- aggregates;
- updated node state.

---

## 62. Node Update Equivariance

For node-update map:

`U`

the transformation law must remain compatible with node representation type.

---

## 63. Edge Update Equivariance

Dynamic edge states must preserve their declared scalar/equivariant structure.

---

## 64. Global State

A global state may contain:

- invariant scalars;
- global equivariant channels;
- externally defined frame-dependent state.

Each component requires an explicit transformation law.

---

## 65. Resonance Equivariance

The resonance mapping:

`P_R`

satisfies:

`P_R(rho_EQ(g)x) = rho_R(g)P_R(x)`.

---

## 66. Scalar Resonance Channel

A scalar resonance channel is invariant.

---

## 67. Vector Resonance Channel

A vector resonance channel transforms:

`r_v' = Qr_v`.

---

## 68. Tensor Resonance Channel

A tensor resonance channel transforms:

`R_T' = QR_TQ^T`.

---

## 69. Resonance-Class Invariance

A resonance class such as:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

should remain unchanged under a rigid transformation when its classifier depends only on invariant resonance geometry.

---

## 70. Resonance Window Symmetry

A resonance window used for invariant classification must itself be defined consistently with the resonance representation.

---

## 71. Laboratory-Axis Resonance Boundary

A resonance classifier depending on one fixed Cartesian axis breaks full rotational invariance unless that axis is an explicit external model state.

---

## 72. Ternary Feature Equivariance

Canonical scalar ternary features satisfy:

`t(gX) = t(X)`.

---

## 73. Ternary Polarity

The states:

`-1`

and:

`1`

are semantic polarities.

They are not Cartesian directions.

---

## 74. Spatial Rotation versus Ternary Polarity

The invariant remains:

`spatial rotation ≠ ternary polarity reversal`.

---

## 75. Reflection versus Ternary Polarity

Reflection does not automatically map:

`-1 ↔ 1`.

Such behavior requires an explicitly defined parity-like ternary channel.

---

## 76. Active Neutral under Symmetry

The state:

`0`

remains active neutral under spatial transformation.

---

## 77. Ternary Decision Invariance

If ternary target is generated from invariant decision variable:

`z`

then:

`z(gX) = z(X)`

implies identical target classification under rigid transformation.

---

## 78. Equivariant Ternary Source

If a ternary decision originates from a vector or tensor state, it must first use a declared symmetry-compatible reduction or transformation rule.

---

## 79. Target State under Permutation

Per-atom targets must permute with atoms.

---

## 80. Executed State under Permutation

Per-atom executed states must permute with atoms.

---

## 81. Pending State under Permutation

Pending destinations must permute with their associated entities.

---

## 82. Execution Topology under Symmetry

Symmetry transformation does not alter the ternary execution graph:

`-1 ↔ 0 ↔ 1`.

---

## 83. Direct-Opposite Constraint

Spatial transformation cannot authorize:

`-1 → 1`

or:

`1 → -1`

as direct committed transitions.

---

## 84. Energy Invariance

Energy must satisfy:

`E(gX) = E(X)`

under the declared symmetry of the complete physical state.

---

## 85. Translation-Invariant Energy

For an isolated internal energy:

`E(R+c) = E(R)`.

---

## 86. Rotation-Invariant Energy

For rigid rotation:

`E(QR) = E(R)`.

---

## 87. Reflection-Invariant Energy

For an:

`O(3)`-invariant model:

`E(QR) = E(R)`

also for:

`det(Q) = -1`.

---

## 88. Permutation-Invariant Energy

For admissible atom permutation:

`E(pi X) = E(X)`.

---

## 89. Force Equivariance

For conservative force:

`F_i = -grad_(r_i)E`.

Under rotation:

`F_i(QR) = QF_i(R)`.

---

## 90. Translation Behavior of Force

For a translation-invariant internal model:

`F_i(R+c) = F_i(R)`.

---

## 91. Force Permutation Equivariance

Atom permutation must permute force vectors consistently.

---

## 92. Reflection Behavior of Force

A polar force vector transforms:

`F_i' = QF_i`

under improper orthogonal transformation.

---

## 93. Stress Equivariance

Stress transforms:

`Sigma' = QSigma Q^T`.

---

## 94. Stress Permutation Invariance

Global stress remains unchanged under atom relabeling.

---

## 95. Stress Reflection Behavior

The tensor transformation law remains valid under:

`O(3)`

when reflection symmetry is declared.

---

## 96. Pressure Invariance

A scalar pressure derived from rotational tensor invariants remains invariant under rigid rotation.

---

## 97. Conservative Relation and Symmetry

Energy invariance and differentiation produce force equivariance under the applicable smoothness assumptions.

---

## 98. Equivariance versus Conservativity

The distinction remains:

`equivariance ≠ conservativity`.

A direct force model can be equivariant without being the gradient of a scalar potential.

---

## 99. Architectural Equivariance

Architectural equivariance is satisfied by construction for all admissible parameter values.

---

## 100. Learned Equivariance

A generic architecture may instead attempt to learn approximate symmetry from data.

This is distinct from architectural equivariance.

---

## 101. Equivariance Constraint

A learning constraint may compare model output on transformed input with the transformed original output.

---

## 102. Transformation Pair

Given:

`X`

and:

`gX`

compute:

`Y = M(X)`

and:

`Y_g = M(gX)`.

The expected transformed output is:

`rho_Y(g)Y`.

---

## 103. Equivariance Residual

Define:

`epsilon_eq = d_Y(Y_g, rho_Y(g)Y)`.

---

## 104. Equivariance Loss

A soft constraint may use:

`L_eq = A(epsilon_eq)`.

---

## 105. Scalar Invariance Residual

For energy:

`epsilon_E = |E(gX) - E(X)|`.

---

## 106. Force Equivariance Residual

For force:

`epsilon_F = ||F(gX) - rho_F(g)F(X)||`.

---

## 107. Stress Equivariance Residual

For stress:

`epsilon_S = ||Sigma(gX) - QSigma(X)Q^T||`.

---

## 108. Resonance Equivariance Residual

For resonance:

`epsilon_R = d_R(P_R(gX), rho_R(g)P_R(X))`.

---

## 109. Representation Equivariance Residual

For latent equivariant representation:

`h`

define a representation-specific residual between:

`h(gX)`

and:

`rho_h(g)h(X)`.

---

## 110. Message Equivariance Residual

Individual message channels may be tested analogously.

---

## 111. Ternary Invariance Residual

For scalar ternary state, a mismatch is:

`I(t(gX) ≠ t(X))`.

---

## 112. Permutation Residual

For per-atom output:

`Y_atom`

compare:

`Y_atom(pi X)`

with:

`pi Y_atom(X)`.

---

## 113. Global Permutation Residual

For invariant global output compare:

`Y_global(pi X)`

with:

`Y_global(X)`.

---

## 114. Combined Transformation Residual

A validation may apply both:

`g`

and:

`pi`

in one test.

---

## 115. Exact versus Numerical Symmetry

Formal symmetry may be exact.

Floating-point implementation may exhibit finite numerical residuals.

---

## 116. Numerical Tolerance

A validation tolerance:

`epsilon_tol`

must be declared for continuous outputs.

---

## 117. Exact Categorical Symmetry

Canonical ternary categorical outputs should match exactly under transformations that leave their semantic classifier invariant.

---

## 118. Tolerance Does Not Redefine Symmetry

A numerical tolerance is an implementation comparison rule.

It does not change the mathematical transformation law.

---

## 119. Relative Residual

A relative equivariance residual may normalize by output magnitude.

---

## 120. Absolute Residual

An absolute residual may be preferable near zero output.

---

## 121. Hybrid Residual

A combined absolute/relative criterion may be used.

The exact formula must be explicit.

---

## 122. Zero Vector Boundary

Relative error becomes ill-conditioned when reference vector norm approaches zero.

A numerical floor may therefore be required.

---

## 123. Zero Force Symmetry Test

A zero force vector remains exactly compatible with rotation.

Its numerical comparison must not create artificial direction.

---

## 124. Zero Tensor Symmetry Test

Likewise for zero stress or zero tensor state.

---

## 125. Symmetry Sampling

Training or validation need not enumerate every possible group element.

A declared subset may be sampled.

---

## 126. Rotation Sampling

Rotation tests may use:

- random rotations;
- fixed-axis rotations;
- canonical finite sets;
- adversarially selected rotations.

---

## 127. Uniform Rotation Sampling

Random rotations may be sampled according to a declared distribution over:

`SO(3)`.

---

## 128. Reflection Sampling

Reflection tests may use selected improper orthogonal matrices.

---

## 129. Translation Sampling

Translation vectors may be sampled from a declared domain.

---

## 130. Permutation Sampling

Permutations may be sampled within admissible species-preserving permutations.

---

## 131. Symmetry Augmentation

Training samples may be augmented using transformations from the declared symmetry group.

---

## 132. Augmentation Labels

Transformed labels must obey:

`energy → invariant`

`force → vector transformed`

`stress → tensor transformed`

`scalar ternary → invariant`.

---

## 133. Augmentation versus Constraint

The distinction remains:

`data augmentation ≠ equivariance constraint`.

---

## 134. Augmentation versus Architecture

The distinction remains:

`data augmentation ≠ architectural equivariance`.

---

## 135. Constraint versus Architecture

A soft symmetry penalty is not equivalent to a structurally equivariant architecture.

---

## 136. Architectural Constraint Priority

Where an invariant is fundamental to the declared model family, architectural enforcement provides exact state-space restriction independent of dataset coverage.

---

## 137. Equivariance Regularization

A symmetry penalty may still be used to monitor or reduce finite numerical residuals.

---

## 138. Layerwise Equivariance Testing

Symmetry can be tested at:

- graph layer;
- representation layer;
- message layer;
- resonance layer;
- energy layer;
- force layer;
- stress layer.

---

## 139. Layerwise Failure Localization

Testing intermediate states can identify the layer where transformation consistency first fails.

---

## 140. End-to-End Equivariance Test

An end-to-end test evaluates final outputs only.

---

## 141. Intermediate Equivariance Test

Intermediate tests evaluate internal representation states.

---

## 142. Invariant Hidden Scalar Test

Scalar hidden features should remain unchanged under declared rigid rotations.

---

## 143. Vector Hidden Feature Test

Vector hidden features should rotate by:

`Q`.

---

## 144. Higher-Irrep Test

For channel:

`l`

compare transformed features against:

`D^l(Q)`.

---

## 145. Parity Test

For:

`O(3)`

models, reflection tests verify parity behavior.

---

## 146. Periodic Equivariance

Periodic systems require simultaneous transformation of:

- atomic positions;
- cell vectors;
- periodic-image geometry.

---

## 147. Periodic Translation

Lattice-equivalent translations must preserve physical output.

---

## 148. Cell Rotation

For:

`H' = QH`

and:

`R' = QR`

energy remains invariant, forces rotate, and stress transforms tensorially.

---

## 149. Cell Reflection

If the model supports:

`O(3)`

and the transformed cell remains a valid representation of the reflected state, parity semantics must be preserved.

---

## 150. Cell Deformation Boundary

A nonrigid strain is not an element of rigid Euclidean symmetry.

Energy and stress may change under strain.

---

## 151. Rotation versus Deformation

The distinction remains:

`rotation ≠ deformation`.

---

## 152. External Field

A fixed external field can reduce the model symmetry group.

---

## 153. External Vector

For external vector:

`b`

the complete state transforms consistently only if:

`b' = Qb`.

---

## 154. Fixed Laboratory Field

If the field remains fixed while atoms rotate, full rotational invariance is not expected.

---

## 155. Residual Symmetry Group

The correct symmetry constraint is defined by the complete system including external state.

---

## 156. Directional Boundary Condition

A directional boundary condition may likewise reduce symmetry.

---

## 157. Surface System

A surface may distinguish normal and tangential directions.

The admissible symmetry group may therefore be smaller than full:

`E(3)`.

---

## 158. Symmetry Declaration

Every model must declare the actual symmetry it claims to preserve.

---

## 159. Symmetry Mismatch

Testing a model against a symmetry not present in the complete physical state is an invalid validation condition.

---

## 160. Species Permutation

Only atoms whose relabeling is admissible under species semantics may be freely permuted.

---

## 161. Different Species Exchange

Swapping atom coordinates while also swapping species labels is a relabeling operation.

Changing species identity at fixed labels is a different physical configuration.

---

## 162. Permutation Invariance versus Chemical Exchange

The distinction remains:

`atom relabeling ≠ species transmutation`.

---

## 163. Batch Permutation

Reordering independent configurations inside a batch must not change per-configuration outputs.

---

## 164. Neighbor-List Permutation

Changing storage order of neighbors must not alter mathematical aggregation semantics.

---

## 165. Floating-Point Neighbor Ordering

Finite-precision sum ordering may produce small numerical differences.

Exact replay may therefore require canonical reduction order.

---

## 166. Equivariance and Determinism

Equivariance and deterministic replay are separate properties.

---

## 167. Equivariant but Nondeterministic

A stochastic model may preserve symmetry statistically while producing different samples.

---

## 168. Deterministic but Nonequivariant

A deterministic model may reproduce the same incorrect symmetry behavior.

---

## 169. Deterministic Equivariant Model

A model may satisfy both contracts.

---

## 170. Random State under Transformation

For stochastic equivariance tests, random-state treatment must be explicitly defined.

---

## 171. Shared Randomness Test

One validation strategy may use the same random realization for original and transformed inputs.

---

## 172. Distributional Equivariance

A stochastic output distribution may satisfy symmetry even when individual samples differ.

---

## 173. Distributional Metric

Distribution-level symmetry requires an appropriate statistical comparison.

---

## 174. Equivariance under Quantization

Numerical quantization may introduce finite equivariance residual.

---

## 175. Fixed-Point Representation

Fixed-point implementation requires explicit scaling for scalar, vector, and tensor channels.

---

## 176. Componentwise Saturation

Independent Cartesian saturation may break exact vector equivariance.

---

## 177. Norm-Preserving Saturation

Representation-aware magnitude control can preserve direction.

---

## 178. Quantization Validation

Quantized implementations should measure symmetry residuals after encoding and decoding.

---

## 179. Mixed Precision

Different channels may use different floating-point precision.

The resulting equivariance residual must remain within the declared numerical contract.

---

## 180. Compiler and Kernel Effects

Parallel kernel ordering and numerical approximations may affect measured residuals.

---

## 181. Equivariance Loss Weight

A soft symmetry loss may use:

`lambda_eq`.

---

## 182. Composite Symmetry Loss

A model may use:

`L_eq = lambda_G L_G + lambda_H L_H + lambda_R L_R + lambda_E L_E + lambda_F L_F + lambda_S L_S`.

---

## 183. Graph Symmetry Term

`L_G`

measures graph transformation consistency when graph construction is learned or approximate.

---

## 184. Hidden Representation Term

`L_H`

measures internal representation consistency.

---

## 185. Resonance Symmetry Term

`L_R`

measures resonance transformation consistency.

---

## 186. Energy Symmetry Term

`L_E`

measures scalar invariance.

---

## 187. Force Symmetry Term

`L_F`

measures vector equivariance.

---

## 188. Stress Symmetry Term

`L_S`

measures tensor transformation consistency.

---

## 189. Ternary Symmetry Term

A separate categorical or surrogate term may monitor scalar ternary invariance.

---

## 190. Loss Weight Scheduling

Symmetry-loss coefficients may vary through training.

---

## 191. Symmetry Curriculum

A training procedure may increase transformation complexity over time.

---

## 192. Curriculum Is Not Symmetry Definition

Training schedule does not alter the actual declared group.

---

## 193. Exact Architecture with Zero Symmetry Loss

For a mathematically exact equivariant architecture under exact arithmetic, the formal symmetry residual is zero.

Finite-precision implementations may produce nonzero numerical residuals.

---

## 194. Symmetry Loss and Data Fit

Symmetry and reference-data objectives may produce different parameter gradients in an approximately equivariant architecture.

---

## 195. Gradient Conflict

Conflicting optimization gradients are a training phenomenon.

They do not alter the symmetry definition.

---

## 196. Constraint Projection

A parameter update may be projected back onto a symmetry-compatible parameter manifold where such a parameterization is used.

---

## 197. Parameter Sharing

Symmetry may be encoded through parameter sharing.

---

## 198. Species-Shared Parameters

Parameters shared across atoms of the same species preserve permutation semantics when indexing does not enter arbitrarily.

---

## 199. Edge-Type Sharing

Relation-specific parameter sharing must depend on declared edge type rather than arbitrary edge index.

---

## 200. Rotationally Invariant Parameter

A scalar learned parameter has no orientation.

---

## 201. Learned Vector Parameter

A fixed learned laboratory-frame vector breaks rotational invariance unless it is part of an explicitly symmetry-breaking model.

---

## 202. Learned Tensor Parameter

A fixed anisotropic tensor likewise changes the symmetry group unless transformed as part of the state.

---

## 203. External Learned Frame

A learned frame is not automatically E(3)-equivariant.

Its construction must itself transform consistently.

---

## 204. Canonicalization Boundary

Choosing a canonical orientation can create discontinuities or ambiguities in symmetric configurations.

---

## 205. Equivariant Representation Preferred over Arbitrary Frame Fixing

An explicitly equivariant representation avoids dependence on arbitrary laboratory orientation.

---

## 206. Symmetry Breaking

A model may intentionally represent symmetry-broken states.

The relevant transformation laws must then include the symmetry-breaking order parameter or external state.

---

## 207. Spontaneous Symmetry Breaking Boundary

A symmetry-equivariant model can represent outputs whose particular state is not invariant.

Model equivariance and state symmetry remain distinct.

---

## 208. State Symmetry versus Model Symmetry

The distinction remains:

`symmetry of one configuration ≠ symmetry of model law`.

---

## 209. Crystal Symmetry

A particular crystal may possess a point-group symmetry smaller than:

`O(3)`.

The interatomic model may still be globally E(3)-equivariant.

---

## 210. Material Anisotropy

An anisotropic material response can emerge from configuration geometry while the model remains equivariant.

---

## 211. Equivariance versus Isotropy

The distinction remains:

`equivariance ≠ isotropic output`.

---

## 212. Stress Anisotropy

A stress tensor may be anisotropic while transforming correctly.

---

## 213. Resonance Anisotropy

A resonance tensor or vector may be anisotropic while preserving equivariance.

---

## 214. Force Direction

A nonzero force selects a direction in a particular configuration.

This does not violate rotational equivariance.

---

## 215. Symmetry Constraint and Energy Conservation

Equivariance constraints do not by themselves guarantee conservative force.

---

## 216. Symmetry Constraint and Momentum Conservation

Translation-invariant conservative energy implies the associated internal force-sum relation under applicable assumptions.

An arbitrary translation-equivariant direct force model does not automatically inherit the same conservative structure.

---

## 217. Rotation and Torque

Rotational invariance of a conservative energy supports the corresponding internal torque relation.

---

## 218. Equivariance versus Conservation

The framework preserves:

`equivariance ≠ conservation`.

---

## 219. Equivariance versus Stability

The framework preserves:

`equivariance ≠ stability`.

---

## 220. Equivariance versus Accuracy

The framework preserves:

`equivariance ≠ prediction accuracy`.

A symmetry-correct model may still fit reference data poorly.

---

## 221. Accuracy versus Symmetry

A numerically accurate model on one orientation may still violate symmetry elsewhere.

---

## 222. Symmetry Validation Domain

Equivariance must be evaluated across the declared configuration domain.

---

## 223. Transformation Coverage

Validation should cover a representative set of transformations relevant to the declared group.

---

## 224. Extreme Rotation

All rotations are mathematically equivalent under exact symmetry.

Numerical residuals may nevertheless depend on representation and arithmetic.

---

## 225. Reflection Coverage

Parity-sensitive models should include explicit improper-transform tests.

---

## 226. Near-Symmetric Configuration

Configurations with internal geometric symmetries can expose permutation or frame ambiguities.

---

## 227. Degenerate Geometry

Coincident or collinear geometries may create special representation behavior.

Their admissibility must be defined by the model domain.

---

## 228. Zero Relative Vector

When:

`r_ij = 0`

the direction:

`e_hat_ij`

is undefined.

Graph and representation layers must handle or exclude such configurations explicitly.

---

## 229. Symmetry Test Fixture

A deterministic symmetry fixture may contain:

- base configuration;
- transformation;
- expected transformed output.

---

## 230. Rotation Fixture

A rotation fixture specifies:

`Q`.

---

## 231. Translation Fixture

A translation fixture specifies:

`c`.

---

## 232. Reflection Fixture

A reflection fixture specifies an improper:

`Q`.

---

## 233. Permutation Fixture

A permutation fixture specifies:

`pi`.

---

## 234. Combined Fixture

A combined fixture may specify:

`(Q,c,pi)`.

---

## 235. Expected Energy Output

For symmetry-compatible rigid transformation:

`E' = E`.

---

## 236. Expected Force Output

`F' = QF`

with corresponding atom permutation where used.

---

## 237. Expected Stress Output

`Sigma' = QSigma Q^T`.

---

## 238. Expected Ternary Output

Scalar per-atom ternary channels permute but do not change semantic value under rigid spatial transformation.

---

## 239. Expected Resonance Output

Resonance output follows:

`rho_R`.

---

## 240. Transformation Trace

A symmetry-validation trace may contain:

- transformation identifier;
- group element;
- input hash;
- output hash;
- residuals by layer;
- tolerance;
- pass/fail state.

---

## 241. Symmetry Pass Criterion

A continuous channel passes when its residual satisfies the declared numerical condition.

---

## 242. Ternary Pass Criterion

A canonical scalar ternary channel passes when transformed categorical output matches exactly after reindexing.

---

## 243. Graph Pass Criterion

Graph adjacency and edge geometry must match transformed construction under the declared equivalence relation.

---

## 244. Layerwise Residual Report

A report may include:

- graph residual;
- representation residual;
- message residual;
- resonance residual;
- energy residual;
- force residual;
- stress residual.

---

## 245. Maximum Residual

A validation suite may record maximum observed residual over tested transformations.

---

## 246. Mean Residual

Mean residual may also be reported.

Maximum and mean capture different failure behavior.

---

## 247. Relative Residual Distribution

A benchmark may report residual distributions across the validation set.

---

## 248. Symmetry Benchmark

Symmetry residuals measured on a declared dataset carry:

`BENCHMARK`

provenance.

---

## 249. Equivariance Provenance

Equivariance constraints and artifacts retain the canonical provenance system:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 250. Primary-Source Symmetry Relation

Established group-theoretic transformation laws carry:

`PRIMARY_SOURCE`.

---

## 251. Derived Symmetry Test

A test derived from a declared transformation law may carry:

`DERIVED`.

---

## 252. Author-Defined Symmetry Coupling

A TR-EIF-specific coupling of resonance or ternary channels to symmetry constraints may carry:

`AUTHOR_DEFINED`.

---

## 253. Calibrated Tolerance

A numerical tolerance determined through calibration carries:

`CALIBRATED`.

---

## 254. Benchmark Residual

Measured implementation residuals carry:

`BENCHMARK`.

---

## 255. Symmetry Test Fixture Provenance

Synthetic transformed configurations carry:

`TEST_FIXTURE`.

---

## 256. Graph-Equivariance Extension Rule

Any graph symmetry constraint must define:

1. graph construction;

2. transformation group;

3. node permutation;

4. edge permutation;

5. geometric edge transformation;

6. periodic handling;

7. comparison relation.

---

## 257. Representation-Equivariance Extension Rule

Any representation constraint must define:

1. representation type;

2. degree;

3. parity;

4. transformation matrix;

5. metric;

6. tolerance.

---

## 258. Message-Equivariance Extension Rule

Any message symmetry constraint must define:

1. source/receiver convention;

2. message representation;

3. edge transformation;

4. aggregation;

5. transformed comparison.

---

## 259. Resonance-Equivariance Extension Rule

Any resonance symmetry constraint must define:

1. resonance state;

2. transformation law;

3. scalar/vector/tensor scope;

4. window behavior;

5. classifier behavior;

6. metric.

---

## 260. Ternary-Symmetry Extension Rule

Any ternary symmetry constraint must define:

1. ternary channel scope;

2. spatial transformation behavior;

3. permutation behavior;

4. target/executed role;

5. exact comparison rule.

---

## 261. Energy-Invariance Extension Rule

Any energy symmetry constraint must define:

1. complete transformed state;

2. declared symmetry group;

3. external fields;

4. numerical tolerance;

5. periodic handling.

---

## 262. Force-Equivariance Extension Rule

Any force symmetry constraint must define:

1. polar-vector transformation;

2. atom permutation;

3. external-force state;

4. comparison metric;

5. tolerance.

---

## 263. Stress-Equivariance Extension Rule

Any stress symmetry constraint must define:

1. stress tensor type;

2. rotation law;

3. sign convention;

4. cell transformation;

5. comparison metric;

6. tolerance.

---

## 264. Combined-Symmetry Extension Rule

Any combined transformation test must define:

1. spatial group element;

2. permutation;

3. transformation order where implementation-dependent;

4. expected output transformation;

5. comparison relation.

---

## 265. Stochastic-Equivariance Extension Rule

Any stochastic symmetry test must define:

1. random-state handling;

2. sample-level or distribution-level criterion;

3. number of samples;

4. statistical metric;

5. confidence criterion.

---

## 266. Numerical-Equivariance Extension Rule

Any quantized or mixed-precision symmetry contract must define:

1. arithmetic representation;

2. scaling;

3. rounding;

4. saturation;

5. residual metric;

6. tolerance.

---

## 267. Canonical Equivariance Invariants

Every conforming TR-EIP model preserves:

1. explicit symmetry group;

2. explicit action on configuration;

3. explicit permutation action;

4. explicit representation type;

5. explicit output transformation law;

6. explicit periodic transformation semantics;

7. explicit numerical comparison contract.

---

## 268. Canonical Representation Invariants

The framework preserves:

`scalar → invariant`

`vector → equivariant`

`tensor → tensor transformed`

with parity distinctions where applicable.

---

## 269. Canonical Graph Invariants

Rigid transformations preserve the graph relation according to its declared geometry.

Atom permutation induces corresponding graph permutation.

---

## 270. Canonical Energy Invariant

For every admissible rigid symmetry transformation:

`E(gX) = E(X)`.

---

## 271. Canonical Force Invariant

Force transforms as a polar vector:

`F(gX) = rho_F(g)F(X)`.

---

## 272. Canonical Stress Invariant

Stress transforms:

`Sigma(gX) = QSigma(X)Q^T`.

---

## 273. Canonical Resonance Invariant

Resonance state follows:

`rho_R`.

Scalar resonance channels remain invariant.

---

## 274. Canonical Ternary Invariant

Canonical scalar ternary channels remain semantically unchanged under rigid spatial transformation and permute with their associated entities.

---

## 275. Canonical Execution Invariant

Equivariance constraints do not alter the balanced ternary execution graph:

`-1 ↔ 0 ↔ 1`.

---

## 276. Canonical Active-Neutral Invariant

The state:

`0`

remains active neutral under every admissible spatial or permutation transformation.

---

## 277. Canonical Opposite Routes

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

Opposite routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 278. Canonical State-Separation Invariants

The equivariance layer preserves:

`scalar ≠ vector`

`vector ≠ tensor`

`energy ≠ generic scalar`

`force ≠ generic vector`

`stress ≠ generic tensor`

`spatial rotation ≠ ternary polarity reversal`

`atom permutation ≠ species transmutation`

`rotation ≠ deformation`

`equivariance ≠ invariance`.

---

## 279. Canonical Scientific Distinctions

The equivariance layer preserves:

`equivariance ≠ conservativity`

`equivariance ≠ stability`

`equivariance ≠ accuracy`

`architectural equivariance ≠ data augmentation`

`architectural equivariance ≠ symmetry penalty`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`resonance state ≠ ternary state`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 280. Canonical Symmetry Chain

The complete symmetry chain is:

`X`

`→ rho_X(g)X`

`→ model evaluation`

`→ Y_g`

and:

`X`

`→ model evaluation`

`→ Y`

`→ rho_Y(g)Y`.

Equivariance requires:

`Y_g = rho_Y(g)Y`.

---

## 281. Canonical Learning Constraint Chain

During optimization:

`base sample`

`+ transformed sample`

`→ paired model outputs`

`→ transformation residual`

`→ equivariance loss`

`→ parameter update`.

---

## 282. Canonical Validation Chain

For validation:

`configuration`

`→ transformation set`

`→ layerwise/end-to-end evaluation`

`→ residuals`

`→ tolerance comparison`

`→ symmetry report`.

---

## 283. Interface to Chapter 08

Chapter 08 develops Uncertainty and Domain Detection.

It defines how uncertainty estimates and out-of-domain state behave under the same symmetry and permutation contracts.

---

## 284. Interface to Chapter 09

Chapter 09 develops Optimization.

It consumes:

- mechanical loss;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty objectives

to update the trainable parameter set.

---

## 285. Final Formal Structure

The equivariance-constraint layer may be represented as:

`EQC = (G, rho_X, rho_G, rho_EQ, rho_R, rho_T, rho_E, rho_F, rho_Sigma, L_eq, V_eq)`.

Here:

- `G` is the declared symmetry group;
- `rho_X` is the configuration action;
- `rho_G` is the graph action;
- `rho_EQ` is the equivariant representation action;
- `rho_R` is the resonance action;
- `rho_T` is the ternary-channel action;
- `rho_E` is the scalar energy action;
- `rho_F` is the force action;
- `rho_Sigma` is the stress action;
- `L_eq` is optional symmetry regularization;
- `V_eq` is the symmetry-validation contract.

The canonical equivariance equation is:

`M(rho_X(g)X) = rho_Y(g)M(X)`.

For energy:

`E(gX) = E(X)`.

For force:

`F(gX) = rho_F(g)F(X)`.

For stress:

`Sigma(gX) = QSigma(X)Q^T`.

---

## 286. Final Statement

Equivariance constraints preserve the geometric and permutation structure of TR-EIP throughout learning, validation, and inference.

The model explicitly distinguishes:

- invariant scalars;
- equivariant vectors;
- tensors;
- parity-sensitive channels;
- atom permutations;
- spatial transformations.

The canonical transformation laws remain:

`energy → invariant`

`force → polar-vector equivariant`

`stress → tensor transformed`

`scalar resonance → invariant`

`vector resonance → equivariant`

`scalar ternary → invariant`.

The framework preserves:

`equivariance ≠ invariance`

`equivariance ≠ conservativity`

`equivariance ≠ accuracy`

`rotation ≠ deformation`

`atom permutation ≠ species transmutation`

`generic scalar ≠ energy`

`generic vector ≠ force`

`generic tensor ≠ stress`

`spatial rotation ≠ ternary polarity reversal`.

Architectural equivariance, symmetry regularization, data augmentation, and numerical symmetry validation remain separate mechanisms.

The balanced ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

No spatial transformation, permutation, equivariance penalty, data augmentation procedure, numerical tolerance, or learned representation may bypass the committed execution topology:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

These definitions establish the symmetry constraints required for Uncertainty and Domain Detection developed in Chapter 08.
