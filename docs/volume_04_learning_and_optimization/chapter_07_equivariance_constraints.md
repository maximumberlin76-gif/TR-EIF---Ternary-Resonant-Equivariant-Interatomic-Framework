# Equivariance Constraints

## 1. Purpose

This chapter defines equivariance constraints for the TR-EIF learning and optimization layer.

The equivariance layer specifies how model inputs, latent representations, resonance variables, ternary outputs, energies, forces, stresses, and uncertainty quantities transform under declared symmetry operations.

It also defines the distinction between:

- invariance;
- equivariance;
- permutation consistency;
- architectural symmetry;
- symmetry regularization;
- symmetry validation.

---

## 2. Dependencies

This chapter depends on:

- Volume 01 — Mathematical Foundations;
- Volume 02 — Ternary Resonance Theory;
- Volume 03 — Equivariant Interatomic Framework;
- Volume 04 Chapter 01 — Model Architecture;
- Volume 04 Chapter 02 — Training Data;
- Volume 04 Chapter 03 — Loss Functionals;
- Volume 04 Chapter 04 — Energy-Force-Stress Training;
- Volume 04 Chapter 05 — Ternary Regularization;
- Volume 04 Chapter 06 — Resonance Regularization.

---

## 3. Symmetry Group

Let:

`G`

denote the declared symmetry group.

For:

`g ∈ G`

the action of:

`g`

on an input space:

`X`

is represented by:

`rho_X(g)`.

---

## 4. Output Representation

For an output space:

`Y`

the corresponding group action is:

`rho_Y(g)`.

---

## 5. Equivariance

A mapping:

`F: X → Y`

is equivariant under:

`G`

when:

`F(rho_X(g)x) = rho_Y(g)F(x)`

for every admissible:

`g ∈ G`

and:

`x ∈ X`.

---

## 6. Invariance

A mapping is invariant when:

`rho_Y(g)`

acts trivially on its output.

Then:

`F(rho_X(g)x) = F(x)`.

---

## 7. Invariance versus Equivariance

The framework preserves:

`invariance ≠ equivariance`.

Invariance is a special transformation behavior in which the output remains unchanged.

Equivariance allows the output to transform according to its declared representation.

---

## 8. Declared Symmetry Scope

Every TR-EIF model must specify which symmetry group or subgroup applies to each relevant module.

Possible groups include:

- translation groups;
- rotation groups;
- reflection-inclusive orthogonal groups;
- rigid-motion groups;
- permutation groups;
- problem-specific symmetry subgroups.

---

## 9. Rotation Group

For three-dimensional proper rotations:

`SO(3)`

may be used.

---

## 10. Orthogonal Group

If reflections are included:

`O(3)`

may be used.

---

## 11. Euclidean Group

If translation and orthogonal transformations are included:

`E(3)`

may be used.

---

## 12. Special Euclidean Group

If translation and proper rotation are included without reflections:

`SE(3)`

may be used.

---

## 13. Group Declaration Requirement

The model must not use:

`SO(3)`

`O(3)`

`SE(3)`

or:

`E(3)`

interchangeably.

The selected group must be explicit.

---

## 14. Translation

For atomic positions:

`R_i`

a global translation:

`a`

acts as:

`R_i → R_i + a`.

---

## 15. Relative Coordinates

Relative displacement:

`R_ij = R_j - R_i`

is translation invariant.

---

## 16. Rotation

For rotation matrix:

`Q`

a position vector transforms as:

`R_i → Q R_i`.

---

## 17. Relative Vector Rotation

A relative vector transforms as:

`R_ij → Q R_ij`.

---

## 18. Reflection

For an orthogonal transformation:

`Q`

with:

`det(Q) = -1`

the transformation includes reflection or inversion-related behavior.

---

## 19. Translation Invariance of Scalar Energy

For an isolated system with no external position-dependent field:

`E({R_i + a}) = E({R_i})`.

---

## 20. Rotational Invariance of Scalar Energy

Under an admissible rotation:

`E({Q R_i}) = E({R_i})`.

---

## 21. Force Equivariance

For force:

`F_i`

under an admissible rotation:

`F_i({Q R_j}) = Q F_i({R_j})`.

---

## 22. Stress Transformation

For second-order stress tensor:

`Sigma`

under rotation:

`Q`

the transformed tensor is:

`Sigma' = Q Sigma Q^T`.

---

## 23. Scalar Quantity

A scalar transforms trivially under the declared spatial group.

Examples may include:

- total energy;
- invariant distance;
- scalar resonance coordinate;
- scalar uncertainty score.

---

## 24. Vector Quantity

A polar vector transforms through:

`Q`.

Examples include:

- position displacement;
- force;
- declared vector-valued latent state.

---

## 25. Tensor Quantity

A second-order tensor transforms according to its declared tensor law.

---

## 26. Representation Type

Every latent or output quantity must have a declared transformation type.

---

## 27. Irreducible Representations

For rotation-equivariant architectures, features may be organized by irreducible representations indexed by angular degree:

`l`.

---

## 28. Scalar Irrep

For:

`l = 0`

the feature is rotationally invariant.

---

## 29. Higher-Order Irreps

For:

`l > 0`

features transform nontrivially under rotation.

---

## 30. Parity

Under reflection-inclusive groups, representation type may also require parity.

---

## 31. Parity Declaration

A feature's behavior under reflection must be explicit when:

`O(3)`

or:

`E(3)`

symmetry is claimed.

---

## 32. Polar versus Axial Vectors

Polar vectors and axial vectors have different reflection behavior.

The model must distinguish them when reflections are part of:

`G`.

---

## 33. Permutation Symmetry

For chemically identical entities, relabeling must not alter permutation-invariant global outputs.

---

## 34. Permutation Action

Let:

`pi`

denote an admissible permutation.

Per-entity quantities transform by corresponding reindexing.

---

## 35. Global Scalar under Permutation

For a permutation-invariant scalar output:

`E(pi X) = E(X)`.

---

## 36. Per-Entity Output under Permutation

For a per-entity output:

`Y`

equivariance requires:

`Y(pi X) = pi Y(X)`.

---

## 37. Species-Preserving Permutation

Permutation symmetry applies only to exchanges allowed by the declared species and entity typing.

---

## 38. Species Labels

Atomic species are part of the input state.

A permutation must preserve the semantic association between species and entity index.

---

## 39. Graph Representation

An interatomic configuration may be represented as a graph:

`G_X = (V, E)`.

---

## 40. Node Features

Node features may include:

- species;
- invariant scalar descriptors;
- equivariant latent features;
- resonance variables;
- ternary variables;
- uncertainty variables.

---

## 41. Edge Features

Edge features may include:

- relative distance;
- relative direction;
- pair descriptors;
- resonance-conditioned quantities.

---

## 42. Graph Permutation Equivariance

Graph message passing must remain consistent under admissible node reindexing.

---

## 43. Message Function

A message may be written:

`m_ij = M(h_i, h_j, e_ij)`.

---

## 44. Aggregation

A node update may use:

`m_i = A({m_ij})`.

---

## 45. Permutation-Invariant Aggregation

For neighbor ordering invariance, aggregation may use operations such as:

- sum;
- mean;
- another explicitly permutation-invariant operator.

---

## 46. Ordered Concatenation Constraint

Arbitrary neighbor-order concatenation does not preserve permutation invariance unless an explicit canonical ordering rule is defined.

---

## 47. Equivariant Linear Mapping

A linear map between representation spaces must intertwine the group actions:

`L rho_X(g) = rho_Y(g) L`.

---

## 48. Tensor Product

Equivariant architectures may construct higher-order features through tensor products of representations.

---

## 49. Tensor-Product Decomposition

The resulting representation must be decomposed according to the declared symmetry representation rules.

---

## 50. Nonlinearity Constraint

A nonlinear operation must preserve the transformation law of the representation on which it acts.

---

## 51. Scalar Nonlinearity

Ordinary pointwise nonlinearities may be applied directly to invariant scalar channels.

---

## 52. Non-Scalar Nonlinearity

A general component-wise nonlinearity applied independently to vector or higher-order representation components does not automatically preserve equivariance.

---

## 53. Equivariant Gating

A non-scalar equivariant feature may be modulated by an invariant scalar gate.

---

## 54. Norm-Based Nonlinearity

A feature norm may be used to construct an invariant scalar control quantity where the representation and norm are explicitly defined.

---

## 55. Normalization

Normalization operations must preserve the declared transformation structure.

---

## 56. Scalar Normalization

Invariant scalar channels may use scalar normalization schemes.

---

## 57. Equivariant Channel Normalization

Non-scalar channels require normalization that preserves orientation-dependent transformation behavior.

---

## 58. Coordinate Construction

Coordinate-dependent features must be constructed so their transformation law is known.

---

## 59. Distance

Euclidean distance:

`d_ij = ||R_j - R_i||`

is invariant under rigid translation and orthogonal transformation.

---

## 60. Direction

Normalized direction:

`u_ij = R_ij / ||R_ij||`

is translation invariant and rotation equivariant.

---

## 61. Zero-Distance Handling

Any use of:

`u_ij`

must define behavior for zero or numerically unresolved separation.

---

## 62. Angular Features

Angular quantities constructed from relative vectors must have declared transformation and parity properties.

---

## 63. Local Reference Frames

A local reference frame may be used only when its construction is deterministic and symmetry-compatible.

---

## 64. Frame Ambiguity

Degenerate local environments may make a local frame non-unique.

Such cases require explicit handling.

---

## 65. External Reference Frame

A laboratory-frame axis is not symmetry-neutral.

If used, it becomes part of the model input or reduces the symmetry group.

---

## 66. External Field

An external vector or tensor field must transform with the system when full covariance is intended.

---

## 67. Reduced Symmetry

A fixed external field may reduce:

`G`

to a subgroup that preserves that field configuration.

---

## 68. Periodic Systems

For periodic boundary conditions, symmetry definitions must include the simulation cell and periodic-image convention.

---

## 69. Cell Matrix

Let:

`H`

denote the periodic cell matrix.

Under rigid rotation:

`H → Q H`.

---

## 70. Fractional Coordinates

Fractional coordinates transform differently from Cartesian coordinates and must not be treated as ordinary physical vectors under arbitrary cell transformation.

---

## 71. Minimum-Image Convention

Neighbor construction under periodic boundaries must preserve consistency under equivalent periodic representations.

---

## 72. Lattice Translation

Periodic image relabeling must not change physical predictions.

---

## 73. Resonance State Symmetry

Each resonance quantity must have a declared transformation behavior.

---

## 74. Scalar Resonance Quantity

If:

`r_scalar`

is a scalar invariant:

`r_scalar(gX) = r_scalar(X)`.

---

## 75. Vector Resonance Quantity

If:

`r_vec`

is equivariant:

`r_vec(gX) = rho_R(g) r_vec(X)`.

---

## 76. Tensor Resonance Quantity

A tensorial resonance quantity transforms according to its declared tensor representation.

---

## 77. Resonance Window Symmetry

A resonance window:

`W_R`

must be compatible with the transformation law of its ambient resonance space.

---

## 78. Invariant Resonance Window

If:

`W_R`

is defined only in invariant scalar coordinates, rigid spatial transformations leave its membership relation unchanged.

---

## 79. Equivariant Resonance Window

If a window is defined in an equivariant vector or tensor space, the window itself must transform consistently.

---

## 80. Resonance Classification Invariance

For an invariant resonance classifier:

`C_R(gX) = C_R(X)`.

---

## 81. Resonance Class Permutation

Per-entity resonance classifications must permute with their associated entities.

---

## 82. Resonance Boundary

The boundary:

`∂W_R`

must transform consistently with:

`W_R`.

---

## 83. Resonance Symmetry Is Not Resonance Identity

Symmetry behavior does not determine whether a state is:

`OUTSIDE`

`BOUNDARY`

or:

`INSIDE`.

---

## 84. Resonance Classification Is Not Ternary State

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

---

## 85. Ternary State Symmetry

The semantic ternary state space is:

`T = {-1,0,1}`.

These values are semantic states.

They are not spatial vector components.

---

## 86. Active Neutral

The state:

`0`

remains active neutral.

Its semantics are not defined by spatial orientation.

---

## 87. Spatial Rotation and Ternary State

An admissible rigid rotation does not exchange:

`-1`

and:

`1`

for a scalar ternary variable.

---

## 88. Spatial Reflection and Ternary State

An admissible spatial reflection does not automatically exchange:

`-1`

and:

`1`.

---

## 89. Spatial Rotation Is Not Ternary Polarity Reversal

The framework preserves:

`spatial rotation ≠ ternary polarity reversal`.

---

## 90. Spatial Reflection Is Not Ternary Polarity Reversal

The framework preserves:

`spatial reflection ≠ ternary polarity reversal`

unless a separate semantic transformation is explicitly defined.

---

## 91. Scalar Ternary Invariance

For an invariant scalar ternary target:

`t_target(gX) = t_target(X)`.

---

## 92. Per-Entity Ternary Permutation

For per-entity ternary targets:

`t_target(pi X) = pi t_target(X)`.

---

## 93. Executed State Symmetry

Per-entity executed ternary states must permute consistently with entity indexing.

---

## 94. Pending State Symmetry

Pending destinations must permute with the associated entities.

---

## 95. Target, Pending, and Executed Separation

The framework preserves:

`t_target ≠ t_pending ≠ t_exec`

as semantic roles.

---

## 96. Equivariance Does Not Alter Ternary Execution Topology

The committed ternary graph remains:

`-1 ↔ 0 ↔ 1`.

---

## 97. Forbidden Direct Opposite Transitions

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 98. Neutral-Mediated Opposite Routes

The required routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 99. Symmetry Does Not Collapse Transition Legs

A symmetry operation does not merge separate committed transition events.

---

## 100. Energy Symmetry

Total energy is a scalar invariant under the declared rigid-motion symmetry when no external symmetry-breaking field is present.

---

## 101. Atomic Energy Decomposition

If energy is decomposed into per-entity scalar contributions:

`E = sum_i E_i`

then each:

`E_i`

must permute with the associated entity index.

---

## 102. Force Symmetry

Force is a polar vector field.

---

## 103. Force from Energy

For a conservative energy model:

`F_i = -grad_(R_i) E`.

---

## 104. Energy Invariance Implies Force Equivariance

If the differentiable scalar energy is invariant under the declared rotation group and coordinates transform conventionally, its coordinate gradient transforms covariantly as the corresponding force vector.

---

## 105. Direct Force Branch

A directly predicted force branch must satisfy force equivariance independently of whether an energy branch is present.

---

## 106. Energy-Force Consistency

Equivariance does not by itself guarantee:

`F_i = -grad_(R_i) E`.

---

## 107. Equivariance Is Not Conservativity

The framework preserves:

`equivariance ≠ conservativity`.

---

## 108. Equivariance Is Not Accuracy

The framework preserves:

`equivariance ≠ predictive accuracy`.

---

## 109. Conservativity Is Not Accuracy

The framework preserves:

`conservativity ≠ predictive accuracy`.

---

## 110. Stress Symmetry

Stress transforms as a second-order tensor under the declared spatial transformation.

---

## 111. Scalar Pressure

If scalar pressure is defined from stress through a trace operation under a declared convention, it transforms invariantly.

---

## 112. Virial Terms

Virial-like quantities involving positions and forces must preserve the required tensor transformation behavior.

---

## 113. Stress Convention

The exact stress sign, normalization, volume convention, and cell derivative definition must remain explicit.

---

## 114. Equivariant Latent Architecture

A latent state may contain multiple representation types.

---

## 115. Typed Latent State

A latent state may be represented as:

`H = {H^(l,p)}`

where:

- `l` identifies rotation representation order;
- `p` identifies parity where applicable.

---

## 116. Typed Message Passing

Messages between nodes must map declared input representation types to declared output representation types.

---

## 117. Scalar-to-Scalar Mapping

An invariant scalar input may generate invariant scalar output.

---

## 118. Scalar-to-Vector Mapping

A scalar alone cannot define an oriented vector without an equivariant directional input.

---

## 119. Vector-to-Scalar Mapping

An invariant scalar may be formed from vector quantities through an invariant contraction.

---

## 120. Tensor Contraction

Contraction rules must preserve the intended representation type.

---

## 121. Representation Mixing

Features with different transformation types must not be mixed through unrestricted arithmetic that destroys their declared behavior.

---

## 122. Residual Connections

Residual connections require matching representation types.

---

## 123. Concatenation

Features may be concatenated within a representation structure only when the resulting transformation law remains explicit.

---

## 124. Attention

Attention mechanisms must preserve the declared symmetry properties of:

- queries;
- keys;
- values;
- attention weights;
- aggregation.

---

## 125. Scalar Attention Weight

An invariant scalar attention weight may modulate an equivariant value without changing the value's representation type.

---

## 126. Direction-Dependent Attention

Direction-dependent attention must itself transform consistently.

---

## 127. Equivariance Constraint Functional

Let:

`R_EQ`

denote an equivariance regularization functional.

A general form may be:

`R_EQ = R_E + R_F + R_S + R_R + R_T + R_H + R_aux`.

---

## 128. Energy Invariance Residual

For transformed input:

`gX`

an energy residual may be:

`epsilon_E(g,X) = |E(gX) - E(X)|`.

---

## 129. Force Equivariance Residual

For force prediction:

`epsilon_F(g,X) = ||F(gX) - rho_F(g)F(X)||`.

---

## 130. Stress Equivariance Residual

For stress:

`epsilon_S(g,X) = ||Sigma(gX) - rho_S(g)Sigma(X)||`.

---

## 131. Resonance Equivariance Residual

For resonance quantity:

`r`

the residual is:

`epsilon_R(g,X) = ||r(gX) - rho_R(g)r(X)||`.

---

## 132. Ternary Symmetry Residual

For exact scalar ternary prediction, a categorical mismatch indicator may be used.

---

## 133. Latent Equivariance Residual

For latent representation:

`H`

a residual may compare:

`H(gX)`

with:

`rho_H(g)H(X)`.

---

## 134. Residual Norm

Every equivariance residual must define:

- norm;
- normalization;
- aggregation;
- tolerance.

---

## 135. Absolute Tolerance

A validation may use:

`epsilon ≤ tau_abs`.

---

## 136. Relative Tolerance

A relative residual may use a scale-normalized criterion.

---

## 137. Mixed Tolerance

A numerical validation may use both absolute and relative thresholds.

---

## 138. Numerical Tolerance Is Not Semantic Approximation

Finite arithmetic tolerance does not redefine the exact mathematical transformation law.

---

## 139. Architectural Equivariance

A model is architecturally equivariant when its permitted operations preserve the declared group action by construction.

---

## 140. Soft Equivariance

A model may instead use an ordinary architecture plus a finite symmetry penalty.

---

## 141. Architectural Equivariance versus Soft Constraint

The framework preserves:

`architectural equivariance ≠ symmetry-penalty training`.

---

## 142. Data Augmentation

A dataset may contain symmetry-transformed samples.

---

## 143. Data Augmentation versus Architectural Equivariance

The framework preserves:

`data augmentation ≠ architectural equivariance`.

---

## 144. Symmetry Loss versus Exact Symmetry

The framework preserves:

`finite symmetry loss ≠ exact mathematical equivariance`.

---

## 145. Combined Strategy

A model may use:

- architectural equivariance;
- symmetry augmentation;
- numerical symmetry validation;
- optional residual penalties.

These mechanisms remain separately identifiable.

---

## 146. Symmetry Sampling

For numerical validation or regularization, transformations:

`g`

may be sampled from the declared group.

---

## 147. Rotation Sampling

Rotation sampling must define the distribution over:

`SO(3)`

or the selected subgroup.

---

## 148. Reflection Sampling

If reflections are part of:

`G`

they must be included explicitly.

---

## 149. Permutation Sampling

Permutation tests must use admissible species-preserving permutations.

---

## 150. Translation Sampling

Translation tests may apply arbitrary global shifts consistent with the coordinate and boundary convention.

---

## 151. Deterministic Symmetry Fixtures

A validation suite may use fixed transformations as:

`TEST_FIXTURE`.

---

## 152. Random Symmetry Tests

Randomly sampled transformations may supplement fixed fixtures.

---

## 153. Symmetry Test Provenance

The source of each transformation set must be traceable.

---

## 154. Numerical Precision

Equivariance residuals depend on arithmetic precision.

---

## 155. Floating-Point Effects

Floating-point roundoff may produce nonzero numerical residual even for an architecturally equivariant implementation.

---

## 156. Mixed Precision

Mixed-precision execution may change residual magnitude.

---

## 157. Fixed-Point Arithmetic

Fixed-point implementations require explicit scale, rounding, and saturation behavior.

---

## 158. Quantization

Quantized representations may introduce symmetry residuals if transformed values cross quantization boundaries differently.

---

## 159. Quantization Validation

Quantized implementations must evaluate equivariance under their deployed arithmetic contract.

---

## 160. Quantization Residual Is Not Symmetry Redefinition

Quantization error does not redefine the mathematical group action.

---

## 161. Determinism versus Equivariance

The framework preserves:

`determinism ≠ equivariance`.

---

## 162. Equivariance versus Deterministic Replay

A deterministic model may violate equivariance.

An equivariant model may use stochastic components unless constrained otherwise.

---

## 163. Reproducibility

A symmetry test should record:

- model version;
- code revision;
- arithmetic precision;
- transformation;
- tolerance;
- random seed where applicable.

---

## 164. External Fields

A model may include:

- electric field;
- magnetic field;
- strain direction;
- flow direction;
- another external vector or tensor.

---

## 165. Field Transformation

If the field is physically transformed with the system, it must transform according to its declared representation.

---

## 166. Fixed Laboratory Field

If an external field is held fixed while the atomic system is rotated, the transformed state represents a different physical configuration.

---

## 167. Symmetry Group with External Field

The admissible symmetry group must be reduced or extended to include the field transformation contract.

---

## 168. Anisotropic Material

A material may possess internal anisotropy.

The relevant symmetry group must correspond to the declared physical configuration and material representation.

---

## 169. Crystal Symmetry

Crystal point-group or space-group structure may impose a subgroup distinct from full:

`SO(3)`

or:

`E(3)`.

---

## 170. Learned Representation and Crystal Symmetry

The architecture may retain full Euclidean covariance while the input structure itself possesses lower physical symmetry.

---

## 171. Symmetry of Data versus Symmetry of Model

The symmetry of a particular sample is not identical to the covariance group of the model mapping.

---

## 172. Symmetric Sample

A specific configuration may be invariant under a subgroup of:

`G`.

---

## 173. Generic Sample

A generic configuration may have no nontrivial stabilizer while the model remains equivariant under:

`G`.

---

## 174. Stabilizer

For input:

`X`

the stabilizer is:

`Stab(X) = {g ∈ G | rho_X(g)X = X}`.

---

## 175. Symmetric Output Constraint

If:

`g ∈ Stab(X)`

equivariance constrains the output to satisfy:

`F(X) = rho_Y(g)F(X)`.

---

## 176. Force at Symmetry Center

Symmetry may constrain particular force components to vanish when required by the stabilizer representation.

---

## 177. Equivariance and Resonance Conditioning

A resonance-conditioned model may be written:

`F(X, r)`.

The pair:

`(X, r)`

must transform consistently.

---

## 178. Invariant Resonance Conditioning

If:

`r`

is invariant, it may condition equivariant mappings as an invariant scalar control variable.

---

## 179. Equivariant Resonance Conditioning

If:

`r`

is vectorial or tensorial, conditioning operations must preserve its representation type.

---

## 180. Resonance Window and External Axes

A resonance window defined relative to a preferred axis must include that axis in the transformation contract.

---

## 181. Equivariance and Ternary Conditioning

A scalar ternary variable may condition an equivariant interaction as an invariant semantic channel.

---

## 182. Ternary State Is Not Spatial Orientation

The framework preserves:

`ternary state ≠ spatial direction`.

---

## 183. Ternary State Is Not Irreducible Representation Index

The values:

`-1/0/1`

must not be interpreted as:

`l`

indices or parity labels.

---

## 184. Equivariance and Uncertainty

Uncertainty outputs require transformation typing.

---

## 185. Scalar Uncertainty

A scalar uncertainty score should remain invariant under admissible rigid transformations.

---

## 186. Per-Entity Uncertainty

Per-entity scalar uncertainty values must permute with entities.

---

## 187. Vector Uncertainty

If a vector-valued uncertainty representation is defined, it must transform equivariantly.

---

## 188. Tensor Uncertainty

A covariance tensor must transform according to its tensor law.

---

## 189. Uncertainty Is Not Equivariance Residual

The framework preserves:

`predictive uncertainty ≠ symmetry residual`.

---

## 190. Symmetry Residual as Diagnostic

A symmetry residual is a validation quantity for transformation consistency.

It is not automatically a calibrated predictive uncertainty measure.

---

## 191. Domain Detection

A domain detector must preserve the declared symmetry structure.

---

## 192. Scalar Domain Score

A scalar in-domain or out-of-domain score should remain invariant under admissible rigid transformations.

---

## 193. Domain Class

For invariant domain classification:

`D(gX) = D(X)`.

---

## 194. OOD Is Not Symmetry Violation

The framework preserves:

`OUT_OF_DOMAIN ≠ equivariance failure`.

---

## 195. Symmetry Violation Is Not OOD

The reverse distinction also holds:

`equivariance residual ≠ domain state`.

---

## 196. Missing Data

Missing data are represented separately from symmetry states.

---

## 197. Mask Transformation

Per-entity masks must permute with entities.

---

## 198. Mask Is Not Ternary Neutral

The framework preserves:

`mask ≠ ternary 0`.

---

## 199. Padding

Padding elements must be excluded through an explicit mask or equivalent mechanism.

---

## 200. Padding Permutation

Padding behavior must not change physical predictions under admissible permutations of real entities.

---

## 201. Invalid Coordinates

Invalid coordinates must not be converted into valid invariant or equivariant features silently.

---

## 202. Non-Finite Input Handling

NaN or infinite values require an explicit validity path.

---

## 203. Provenance Classes

Equivariance definitions, constraints, and tests use the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 204. Primary-Source Symmetry Definition

A symmetry construction adopted from an external mathematical or architectural source uses:

`PRIMARY_SOURCE`.

---

## 205. Derived Transformation Rule

A transformation law derived from established tensor or group definitions may use:

`DERIVED`.

---

## 206. Author-Defined Constraint

A TR-EIF-specific symmetry interface or validation rule may use:

`AUTHOR_DEFINED`.

---

## 207. Calibrated Tolerance

A numerical tolerance fitted or selected through an explicit calibration protocol uses:

`CALIBRATED`.

---

## 208. Benchmark Symmetry Result

Measured symmetry residuals under a benchmark protocol use:

`BENCHMARK`.

---

## 209. Symmetry Test Fixture

Fixed transformed configurations used for testing use:

`TEST_FIXTURE`.

---

## 210. Requires Source

A claimed external symmetry property without established support uses:

`REQUIRES_SOURCE`.

---

## 211. Requires Test

An implementation-level symmetry claim without validation uses:

`REQUIRES_TEST`.

---

## 212. Equivariance Constraint Coefficient

If a soft equivariance penalty is used, let:

`lambda_EQ ≥ 0`.

---

## 213. Component Coefficients

A composite symmetry regularizer may be:

`R_EQ = sum_k lambda_k R_EQ,k`.

---

## 214. Coefficient Declaration

Every:

`lambda_k`

must have explicit:

- value;
- schedule;
- provenance;
- dimensional interpretation where applicable.

---

## 215. Hard Equivariance

Architectural group constraints are hard model-structure constraints.

---

## 216. Soft Equivariance Penalty

A finite:

`R_EQ`

is an optimization objective.

---

## 217. Hard versus Soft Symmetry

The framework preserves:

`architectural symmetry constraint ≠ soft symmetry loss`.

---

## 218. Symmetry Validation Set

A validation suite should contain transformations representing the complete declared symmetry contract.

---

## 219. Translation Validation

The suite may include global translations.

---

## 220. Rotation Validation

The suite may include proper rotations.

---

## 221. Reflection Validation

The suite must include reflections if reflection covariance or invariance is claimed.

---

## 222. Permutation Validation

The suite must include admissible entity permutations.

---

## 223. Periodic Validation

Periodic systems require tests under equivalent image and cell representations.

---

## 224. Energy Validation

For each admissible transformation:

`epsilon_E`

is measured.

---

## 225. Force Validation

For each admissible transformation:

`epsilon_F`

is measured.

---

## 226. Stress Validation

For each admissible transformation:

`epsilon_S`

is measured.

---

## 227. Resonance Validation

For each declared resonance representation:

`epsilon_R`

is measured.

---

## 228. Ternary Validation

For invariant scalar ternary targets, transformed predictions must match exactly apart from declared numerical decision-boundary behavior.

---

## 229. Latent Validation

Intermediate latent representations may be tested directly when their group action is available.

---

## 230. Numerical Tolerance Contract

Every floating-point equivariance test must define its acceptance tolerance.

---

## 231. Exact Categorical Contract

Discrete semantic states may require exact equality rather than floating-point tolerance.

---

## 232. Ternary Exactness

A semantic ternary value must remain exactly one of:

`-1`

`0`

`1`.

---

## 233. Reserved Codes

Any storage-level reserved code must remain outside semantic ternary equality tests.

---

## 234. Validation Failure

A failed symmetry test records a transformation inconsistency under the declared test contract.

---

## 235. Validation Failure Is Not Physical Phase Transition

The framework preserves:

`symmetry-test failure ≠ physical phase transition`.

---

## 236. Validation Failure Is Not Ternary State

The framework preserves:

`validation status ≠ ternary state`.

---

## 237. Validation Failure Is Not Resonance Class

The framework preserves:

`validation status ≠ resonance class`.

---

## 238. Equivariance Extension Rule

Any new equivariant mapping must define:

1. symmetry group;

2. input space;

3. input representation;

4. output space;

5. output representation;

6. transformation equation;

7. implementation mechanism;

8. validation residual;

9. tolerance;

10. provenance.

---

## 239. Invariant Quantity Extension Rule

Any new invariant quantity must define:

1. source variables;

2. symmetry group;

3. invariance equation;

4. units;

5. scale;

6. provenance;

7. validation.

---

## 240. Vector Quantity Extension Rule

Any new vector quantity must define:

1. polar or axial type;

2. translation behavior;

3. rotation behavior;

4. reflection behavior where applicable;

5. units;

6. validation.

---

## 241. Tensor Quantity Extension Rule

Any tensor quantity must define:

1. rank;

2. index convention;

3. transformation law;

4. symmetry or antisymmetry properties;

5. units;

6. validation.

---

## 242. Latent Representation Extension Rule

Any latent equivariant representation must define:

1. group;

2. representation type;

3. parity where applicable;

4. multiplicity;

5. nonlinear operations;

6. normalization;

7. validation.

---

## 243. Resonance Equivariance Extension Rule

Any resonance quantity must define:

1. resonance state space;

2. spatial transformation type;

3. permutation behavior;

4. window transformation;

5. classification transformation;

6. validation.

---

## 244. Ternary Equivariance Extension Rule

Any ternary output must define:

1. semantic role;

2. scalar or other transformation behavior;

3. permutation behavior;

4. target field;

5. executed field where applicable;

6. pending field where applicable;

7. exact validation.

---

## 245. Mechanical Equivariance Extension Rule

Any mechanical prediction interface must define:

1. energy transformation;

2. force transformation;

3. stress transformation;

4. conservativity relation where used;

5. numerical tolerance;

6. validation.

---

## 246. Uncertainty Equivariance Extension Rule

Any uncertainty quantity must define:

1. mathematical type;

2. spatial transformation law;

3. permutation behavior;

4. aggregation;

5. calibration relation;

6. validation.

---

## 247. External-Field Extension Rule

Any external field must define:

1. field type;

2. transformation law;

3. whether it co-transforms with the system;

4. resulting symmetry group;

5. units;

6. validation.

---

## 248. Canonical Equivariance Invariants

Every conforming TR-EIF equivariance layer preserves:

1. explicit symmetry group;

2. explicit group action on each input type;

3. explicit group action on each output type;

4. explicit permutation behavior;

5. explicit scalar/vector/tensor typing;

6. explicit resonance transformation behavior;

7. explicit ternary transformation behavior;

8. explicit mechanical transformation behavior;

9. explicit numerical validation;

10. explicit provenance.

---

## 249. Canonical Mechanical Distinctions

The framework preserves:

`equivariance ≠ conservativity`

`equivariance ≠ accuracy`

`conservativity ≠ accuracy`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`.

---

## 250. Canonical Ternary Distinctions

The framework preserves:

`spatial rotation ≠ ternary polarity reversal`

`spatial reflection ≠ ternary polarity reversal`

`ternary state ≠ vector`

`ternary state ≠ energy`

`ternary state ≠ force`.

---

## 251. Canonical Resonance Distinctions

The framework preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

---

## 252. Canonical Domain Distinctions

The framework preserves:

`OUT_OF_DOMAIN ≠ symmetry failure`

`symmetry residual ≠ uncertainty`

`domain state ≠ ternary state`

`resonance class ≠ domain state`.

---

## 253. Canonical State Distinctions

The framework preserves:

`t_target ≠ t_pending`

`t_pending ≠ t_exec`

`t_target ≠ t_exec`.

---

## 254. Canonical Ternary Execution Invariants

The semantic kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 255. Interface to Chapter 08

Chapter 08 defines uncertainty and domain detection.

The equivariance interface requires:

- invariant global scalar uncertainty where applicable;
- permutation-consistent per-entity uncertainty;
- declared covariance transformation for tensor uncertainty;
- invariant domain classification under admissible symmetry operations;
- separation between symmetry residual and uncertainty.

---

## 256. Interface to Chapter 09

Chapter 09 defines optimization.

The equivariance interface supplies:

- hard architectural constraints;
- optional soft symmetry residuals;
- symmetry-aware parameterization;
- transformed training fixtures;
- numerical validation metrics.

---

## 257. Interface to Molecular Dynamics

The molecular-dynamics layer receives mechanical outputs with the transformation behavior established here.

The interface preserves:

- scalar energy invariance;
- force equivariance;
- stress tensor transformation;
- permutation consistency;
- resonance transformation behavior;
- ternary semantic invariance.

---

## 258. Final Formal Structure

The equivariance layer may be represented as:

`EQ = (G, rho_X, rho_H, rho_R, rho_T, rho_E, rho_F, rho_S, rho_U, C_EQ, V_EQ)`.

Here:

- `G` is the declared symmetry group;
- `rho_X` is the action on model inputs;
- `rho_H` is the action on latent representations;
- `rho_R` is the action on resonance quantities;
- `rho_T` is the action on ternary quantities;
- `rho_E` is the energy representation;
- `rho_F` is the force representation;
- `rho_S` is the stress representation;
- `rho_U` is the uncertainty representation;
- `C_EQ` is the set of architectural or soft symmetry constraints;
- `V_EQ` is the symmetry validation contract.

For every equivariant mapping:

`F`

the defining relation is:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

For every invariant scalar mapping:

`S`

the defining relation is:

`S(rho_X(g)x) = S(x)`.

---

## 259. Final Statement

The equivariance layer defines the transformation contract connecting atomic configurations, latent representations, resonance variables, ternary variables, mechanical outputs, uncertainty quantities, and domain quantities within TR-EIF.

The framework preserves explicit distinctions among:

- invariance;
- equivariance;
- permutation symmetry;
- architectural constraints;
- soft symmetry penalties;
- numerical symmetry residuals.

Scalar energy remains invariant under the declared admissible rigid transformations.

Force remains polar-vector equivariant.

Stress remains tensorially transformed.

Scalar resonance quantities remain invariant when defined in invariant coordinates.

Vector and tensor resonance quantities transform according to their declared representations.

Scalar ternary states remain semantic values:

`-1/0/1`.

They are not spatial directions.

The state:

`0`

remains active neutral.

Spatial rotation or reflection does not automatically exchange:

`-1`

and:

`1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Equivariance does not redefine resonance, ternary semantics, energy, force, stress, uncertainty, domain state, or physical dynamics.

These definitions establish the symmetry constraints required by the uncertainty and optimization layers that follow.
