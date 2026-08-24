# Equivariant Representations

## 1. Purpose

This chapter defines equivariant representations within the Equivariant Interatomic Framework of TR-EIF.

The representation layer maps atomic configuration and interaction-graph state into structured features that preserve declared spatial and permutation transformation laws.

The canonical chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ energy / force / stress`.

The representation layer formalizes:

- invariant scalar features;
- equivariant vector features;
- higher-order tensor features;
- irreducible representation channels;
- parity;
- radial and angular bases;
- tensor products;
- representation mixing;
- local and global representations;
- permutation handling;
- periodic-state handling;
- normalization;
- representation truncation;
- representation validation;
- interfaces to resonance and ternary channels.

---

## 2. Representation Mapping

Let:

`X_conf`

be atomic configuration space and:

`X_G`

the interaction-graph state space.

The equivariant representation mapping is:

`P_EQ: X_conf × X_G → X_EQ`.

The output:

`x_EQ ∈ X_EQ`

contains features carrying explicitly declared transformation types.

---

## 3. Equivariance Condition

For spatial transformation:

`g`

with input action:

`rho_in(g)`

and representation action:

`rho_EQ(g)`,

equivariance requires:

`P_EQ(rho_in(g)x) = rho_EQ(g) P_EQ(x)`.

This relation is exact at the formal level.

---

## 4. Permutation Equivariance

For admissible atom permutation:

`pi`

the representation must satisfy:

`P_EQ(pi · x) = pi · P_EQ(x)`

for per-atom feature state.

Global invariant outputs remain unchanged under permutation.

---

## 5. Combined Symmetry

The representation may support the combined action of:

- spatial Euclidean symmetry;
- atom permutation.

A complete action may be written conceptually as:

`rho_EQ(g, pi)`.

---

## 6. Representation State

A representation state may be decomposed as:

`X_EQ = X_EQ^(0) ⊕ X_EQ^(1) ⊕ X_EQ^(2) ⊕ ...`.

Each component corresponds to a distinct transformation type.

---

## 7. Scalar Representation

A scalar feature:

`s`

is spatially invariant:

`s' = s`.

Scalar channels correspond to:

`l = 0`

under the standard rotational irreducible representation indexing.

---

## 8. Vector Representation

A polar vector:

`v ∈ R^3`

transforms:

`v' = Q v`.

Vector channels correspond to:

`l = 1`

under the standard proper-rotation representation.

---

## 9. Rank-Two Tensor Representation

A rank-two tensor:

`T`

transforms:

`T' = Q T Q^T`.

Tensor representations may be decomposed into irreducible components.

---

## 10. Higher-Order Representation

A rank:

`k`

tensor transforms with one factor of:

`Q`

for each index.

Direct tensor representations may be replaced computationally by irreducible representation channels.

---

## 11. Irreducible Representation

For:

`SO(3)`

an irreducible representation is indexed by:

`l = 0, 1, 2, ...`.

Its dimension is:

`2l + 1`.

---

## 12. Representation Block

A representation block may be written:

`x^(l) ∈ R^(2l+1)`

or in the corresponding real or complex basis adopted by the implementation.

The basis convention must remain explicit.

---

## 13. Multiplicity

A model may contain multiple channels of the same:

`l`.

Let:

`C_l`

denote multiplicity.

Then a representation block may have shape:

`C_l × (2l + 1)`.

---

## 14. O(3) Representation

When reflections are included, a representation additionally carries parity:

`(l, p)`.

Here:

`p ∈ {-1, 1}`

denotes parity under inversion according to the selected convention.

---

## 15. Even Parity

A parity-even feature remains unchanged in sign under inversion according to its representation type.

A true scalar is parity even.

---

## 16. Odd Parity

A parity-odd feature acquires the corresponding sign change under inversion.

Pseudoscalars and axial/polar distinctions require explicit parity treatment.

---

## 17. Scalar versus Pseudoscalar

A scalar and pseudoscalar both have:

`l = 0`

under proper rotations.

They differ under orientation-reversing transformations.

---

## 18. Polar versus Axial Vector

Polar and axial vectors both transform as vectors under:

`SO(3)`.

They differ under reflections or inversion.

---

## 19. Representation Type Metadata

Each feature channel must identify the applicable subset of:

- `l`;
- parity;
- multiplicity;
- unit or dimensional role;
- node/edge/global scope;
- learned or analytic origin.

---

## 20. Raw Scalar Features

Raw scalar node features may include:

- species encoding;
- atomic mass;
- charge;
- invariant material descriptors.

These remain scalar under spatial transformations.

---

## 21. Raw Vector Features

Raw vector features may include:

- relative displacement;
- velocity;
- external vector field;
- force reference.

Their transformation law must remain explicit.

---

## 22. Edge Geometry Representation

For edge:

`j → i`

the relative vector is:

`r_ij`.

Its norm:

`d_ij`

is invariant.

Its direction:

`e_hat_ij`

is equivariant.

---

## 23. Radial Representation

A radial basis maps:

`d_ij`

to:

`R_n(d_ij)`.

These features are invariant scalars.

---

## 24. Radial Basis Family

A radial basis may use:

- Gaussian functions;
- Bessel-type functions;
- polynomial bases;
- spline bases;
- learned radial functions.

The choice belongs to the model specialization.

---

## 25. Radial Cutoff

A radial feature may be multiplied by:

`f_cut(d_ij)`.

The cutoff function remains an invariant scalar.

---

## 26. Angular Representation

Angular dependence may be expanded using spherical harmonics:

`Y_lm(e_hat_ij)`.

This produces representation channels transforming under:

`l`.

---

## 27. Radial-Angular Basis

A geometric edge basis may be:

`B_nlm(r_ij) = R_n(d_ij) Y_lm(e_hat_ij)`.

The radial factor is invariant.

The angular factor carries rotational equivariance.

---

## 28. Translation Handling

Because:

`r_ij`

is translation invariant, edge representations constructed from relative geometry are translation invariant at the input level.

---

## 29. Rotation Handling

The angular representation transforms according to the declared rotational representation.

No coordinate-axis-specific rule may be introduced unless the corresponding external frame is part of the model state.

---

## 30. Reflection Handling

When:

`O(3)`

equivariance is required, parity of each channel must be preserved throughout representation operations.

---

## 31. Node Representation

For atom:

`i`

let:

`h_i`

denote its equivariant feature state.

A decomposition may be:

`h_i = {h_i^(l,p,c)}`.

---

## 32. Edge Representation

For edge:

`j → i`

let:

`e_ij`

contain:

- scalar radial features;
- angular irreducible features;
- periodic-image information;
- optional learned edge channels.

---

## 33. Global Representation

A global feature state may contain:

- invariant scalar state;
- equivariant global vectors;
- tensor fields;
- cell-level features.

---

## 34. Representation Initialization

Node representation may be initialized from species:

`h_i^(0) = Emb(a_i)`.

Species embeddings are scalar channels unless explicitly constructed otherwise.

---

## 35. Species Embedding

A learned species embedding maps:

`A → R^C`.

It is invariant under spatial transformation.

It permutes with atom indexing.

---

## 36. Species Embedding Is Not Species Identity

The embedding is a computational representation.

Species identity remains the underlying categorical state.

---

## 37. Vector Initialization

A vector representation may be initialized from geometry or external vector attributes.

Arbitrary learned nonzero vectors attached to species alone would introduce an orientation unless constructed equivariantly.

---

## 38. Zero Vector Initialization

An equivariant vector channel may be initialized to zero:

`v_i = 0`.

Zero is invariant under rotation as the zero vector.

This geometric zero is not ternary active neutral.

---

## 39. Representation Layer

A representation layer maps:

`X_EQ^(l) → X_EQ^(l+1)`.

The superscript here denotes network depth, not angular momentum unless separately identified.

Notation must distinguish these meanings where both appear.

---

## 40. Representation Depth versus Irrep Degree

The distinction is:

`network layer index ≠ irreducible degree l`.

---

## 41. Linear Equivariant Map

A linear map between representation spaces is equivariant when it intertwines the group actions:

`L rho_in(g) = rho_out(g) L`.

---

## 42. Intertwiner

An equivariant linear operator is an intertwiner between the input and output representations.

---

## 43. Scalar Linear Mixing

Channels with identical transformation type may be linearly mixed across multiplicities.

For scalar channels:

`h_out = W h_in`.

---

## 44. Vector Channel Mixing

Multiple vector channels may be mixed by scalar coefficients acting on multiplicity dimensions while preserving spatial vector components.

---

## 45. Cross-Type Linear Mixing

A generic linear map cannot mix inequivalent irreducible types while preserving equivariance.

Transformation-compatible coupling requires tensor-product structure or another valid equivariant construction.

---

## 46. Tensor Product

Given representation channels:

`x^(l1)`

and:

`y^(l2)`

their tensor product transforms under the product representation.

---

## 47. Clebsch-Gordan Coupling

The tensor product decomposes into irreducible channels:

`l ∈ {|l1-l2|, ..., l1+l2}`.

The coupling uses the corresponding Clebsch-Gordan coefficients or an equivalent basis transformation.

---

## 48. Tensor Product Output

A tensor product may produce several output degrees.

The selected architecture may retain all or a subset.

---

## 49. Parity Coupling

For:

`O(3)`

the output parity is determined by the parity product under the adopted convention.

Parity must remain explicit.

---

## 50. Scalar Product Channel

Coupling two compatible representations to:

`l = 0`

produces an invariant scalar channel.

---

## 51. Vector Product Channel

A coupling producing:

`l = 1`

creates a vector-like representation channel.

---

## 52. Higher Angular Channels

Higher:

`l`

channels encode progressively higher angular structure.

Their physical meaning depends on the learned or analytic mapping.

---

## 53. Angular Truncation

A practical model may restrict:

`l ≤ l_max`.

The value:

`l_max`

is an architecture parameter.

---

## 54. Truncation

Removing higher representation degrees reduces representation capacity.

It does not alter the transformation law of retained channels.

---

## 55. Multiplicity Truncation

A model may also limit:

`C_l`.

This controls feature capacity.

---

## 56. Representation Completeness

A truncated representation is not automatically complete with respect to atomic geometry.

Completeness depends on:

- basis;
- cutoff;
- angular order;
- radial resolution;
- network depth;
- aggregation.

---

## 57. Representation Information Loss

The mapping:

`P_EQ`

may be non-injective.

Different atomic environments may produce the same representation.

---

## 58. Representation Completeness Criterion

A representation is complete relative to a declared equivalence class if identical representations imply equivalence of the underlying configurations within the stated domain.

Such a property must be established for the concrete representation.

---

## 59. Scalar Nonlinearity

A scalar feature may use arbitrary pointwise nonlinearity:

`s' = f(s)`.

Spatial invariance is preserved.

---

## 60. Vector Nonlinearity

Arbitrary componentwise nonlinear transformation of a vector generally breaks rotation equivariance.

Structured equivariant nonlinearities are required.

---

## 61. Norm Gating

For vector:

`v`

an invariant scalar:

`g = f(||v||)`

may gate the vector:

`v' = g v`.

This preserves vector equivariance.

---

## 62. Scalar Gating

A learned invariant scalar channel may gate an equivariant feature:

`x_out^(l) = g x_in^(l)`.

The output retains the same transformation type.

---

## 63. Tensor Product Nonlinearity

Nonlinearity may also be introduced through equivariant tensor products followed by channel selection or gating.

---

## 64. Normalization

Representation normalization must preserve transformation structure.

---

## 65. Scalar Normalization

Scalar channels may be normalized using invariant statistics.

---

## 66. Vector Norm Normalization

A vector may be normalized using its invariant norm:

`v_norm = v / max(||v||, epsilon)`.

The regularization:

`epsilon`

belongs to numerical implementation.

---

## 67. Componentwise Vector Normalization

Independent normalization of Cartesian components can break rotational equivariance unless constructed in a transformation-consistent way.

---

## 68. Irrep-Norm Normalization

An irreducible block may be normalized using the invariant norm over its representation components.

---

## 69. Batch Statistics

Batch-dependent normalization must preserve symmetry and permutation semantics.

The exact statistics and axes must be defined.

---

## 70. Nodewise Normalization

Normalization may operate independently per node while respecting representation blocks.

---

## 71. Global Normalization

A global invariant scale may normalize all nodes.

The scale must itself be invariant.

---

## 72. Feature Units

Physical feature channels may carry units.

Learned hidden channels may be dimensionless unless explicitly assigned units.

---

## 73. Dimensional Mixing

Features with incompatible physical dimensions must not be added directly without an explicit dimensional mapping.

---

## 74. Learned Dimensionless Features

A latent scalar can be dimensionless while being computed from dimensional inputs through normalized or parameterized functions.

The dimensional contract must be explicit when physical interpretation is assigned.

---

## 75. Representation and Energy Units

An invariant representation is not energy by identity.

The energy head maps representation state to a scalar with energy units.

---

## 76. Representation and Force Units

A vector representation is not force by identity.

A force head or energy derivative assigns force semantics and units.

---

## 77. Representation and Stress Units

A rank-two representation is not stress by identity.

Stress requires an explicit mechanical output mapping.

---

## 78. Local Representation

A local node representation depends on a finite graph neighborhood.

---

## 79. One-Layer Receptive Field

After one local message-passing layer, node:

`i`

may depend on:

`N_i`.

---

## 80. Multi-Layer Receptive Field

After multiple message-passing layers, information may propagate through multiple graph hops.

---

## 81. Receptive Field versus Physical Interaction Range

Graph-hop receptive field is a computational quantity.

It is not automatically equal to a physical interaction range.

---

## 82. Global Representation

A global representation may aggregate all node features.

It is typically permutation invariant for scalar global outputs.

---

## 83. Pooling

A pooling map may be:

`P_pool: {h_i} → h_global`.

The pooling operation must preserve the declared symmetry.

---

## 84. Scalar Sum Pooling

Summing scalar node features yields an invariant global scalar feature.

---

## 85. Vector Sum Pooling

Summing equivariant vectors yields an equivariant global vector.

---

## 86. Tensor Pooling

Summing same-type tensor features preserves tensor transformation.

---

## 87. Mean Pooling

Mean pooling changes size scaling relative to sum pooling.

This affects extensive versus intensive output behavior.

---

## 88. Extensive Quantity Representation

An extensive quantity such as total energy may naturally use sum aggregation of local contributions.

The actual decomposition is model-specific.

---

## 89. Intensive Quantity Representation

An intensive quantity may use normalized aggregation or another scaling rule.

---

## 90. Atomic Energy Representation

A model may predict local scalar contributions:

`E_i`.

The total energy may be:

`E = sum_i E_i`.

Each:

`E_i`

must be spatially invariant.

---

## 91. Local Energy Nonuniqueness

The decomposition into:

`E_i`

need not be unique even when total energy is well defined.

---

## 92. Representation under Permutation

Per-atom feature arrays must permute with atom ordering.

Global scalar outputs remain invariant.

---

## 93. Neighbor Aggregation

For messages:

`m_ij`

aggregation:

`m_i = sum_(j ∈ N_i) m_ij`

is invariant to neighbor order.

---

## 94. Ordered Neighbor Input

A model must not derive physical output from arbitrary neighbor-list ordering unless the architecture compensates for permutation.

---

## 95. Edge Representation under Reversal

For reverse edge:

`i → j`

the geometric representation may obey parity/sign relations inherited from:

`r_ji = -r_ij`.

---

## 96. Symmetric Edge Scalar

A distance-derived scalar satisfies:

`s_ij = s_ji`

when no ordered species dependence is present.

---

## 97. Directed Edge Representation

A directed edge representation may depend asymmetrically on:

- receiver node features;
- source node features;
- ordered species pair.

This remains compatible with equivariance.

---

## 98. Periodic Representation

Periodic edge features include lattice-image displacement:

`r_ij = r_j + H n_ij - r_i`.

The representation must treat:

`n_ij`

and:

`H`

consistently.

---

## 99. Cell Representation

The simulation cell may contribute invariant and equivariant global features.

Examples include:

- volume;
- metric tensor;
- lattice vectors.

---

## 100. Cell Volume

`V_cell = |det(H)|`

is invariant under rigid rotation of the full cell.

---

## 101. Cell Metric

A lattice metric may be:

`G_cell = H^T H`.

It is invariant under global rigid rotation:

`H → QH`.

---

## 102. Lattice Vectors

The columns of:

`H`

transform equivariantly under rigid rotation.

---

## 103. Cell Deformation Representation

Strain or deformation state is not part of rigid:

`E(3)`

symmetry.

It changes metric structure.

---

## 104. External Field Representation

A scalar external field may enter as invariant state.

A vector external field must transform equivariantly when included in the symmetry action.

---

## 105. Symmetry-Breaking Representation

If an external field is fixed in laboratory coordinates and excluded from the transformation, the residual symmetry group is reduced.

---

## 106. Residual Symmetry

A representation need only be equivariant under the symmetry group actually preserved by the complete model.

---

## 107. Representation of Resonance Inputs

Chapter 06 consumes representation features to construct resonance coordinates.

The mapping is:

`P_R: X_EQ → X_R`.

---

## 108. Scalar Resonance Input

Invariant scalar channels may directly enter scalar resonance coordinates.

---

## 109. Vector Resonance Input

Equivariant vector channels may enter vector or tensor resonance coordinates or be contracted into invariant decision variables.

---

## 110. Tensor Resonance Input

Higher-order channels may encode anisotropic local environment structure relevant to resonance parameterization.

---

## 111. Resonance Representation Is Distinct

The equivariant representation:

`X_EQ`

is not itself resonance state:

`X_R`.

The two spaces are connected by:

`P_R`.

---

## 112. Ternary Representation Boundary

Chapter 07 introduces ternary feature channels.

The mapping from:

`X_EQ`

or:

`X_R`

to:

`-1/0/1`

must remain explicit.

---

## 113. Ternary Scalar Channel

A standard scalar ternary feature is invariant under rigid spatial transformations.

---

## 114. Equivariant Feature to Scalar Ternary Decision

An equivariant input may be reduced through an invariant functional before scalar ternary classification.

Examples include:

- norm;
- inner product;
- invariant tensor contraction.

---

## 115. Coordinate Component Decision

A scalar ternary decision based directly on one Cartesian component is not rotationally invariant unless an external orientation is part of the model.

---

## 116. Spatial Symmetry and Ternary Polarity

Rigid rotation does not automatically exchange:

`-1`

and:

`1`.

The balanced ternary state remains a semantic channel separate from spatial vector orientation.

---

## 117. Active Neutral Representation Boundary

The ternary state:

`0`

is not the zero vector or zero tensor by identity.

---

## 118. Zero Equivariant Feature

An equivariant feature may be exactly zero.

That does not imply:

`t_target = 0`

or:

`t_exec = 0`

without an explicit mapping.

---

## 119. Representation Compression

A model may compress feature multiplicity between layers.

Compression must preserve the declared representation types.

---

## 120. Representation Expansion

A model may increase channel multiplicity while preserving angular type.

---

## 121. Bottleneck Representation

A bottleneck may retain selected irreducible channels while discarding others.

The information loss is architecture-specific.

---

## 122. Residual Connection

Residual connections may combine features of matching transformation type:

`h_out = h_in + delta_h`.

---

## 123. Cross-Type Residual Prohibition

A scalar channel cannot be added directly to a vector channel while preserving type semantics.

---

## 124. Skip Connection

A skip connection preserves equivariance when source and destination representation types are compatible.

---

## 125. Concatenation

Channels of the same transformation metadata may be concatenated along multiplicity dimensions.

Different types remain separately indexed.

---

## 126. Representation Dictionary

An implementation may store features as a mapping:

`(l, p) → tensor`.

This is a computational organization.

---

## 127. Packed Representation

A packed tensor representation may also be used if offsets and transformation types are unambiguous.

---

## 128. Representation Schema

A schema should preserve:

- scope;
- `l`;
- parity;
- multiplicity;
- numeric dtype;
- units where applicable;
- feature name or role.

---

## 129. Serialization

Serialized equivariant features must include enough metadata to reconstruct their transformation semantics.

---

## 130. Representation Precision

Finite precision affects numerical equivariance residuals.

It does not change the formal group representation.

---

## 131. Float Precision

A model may use:

- float64;
- float32;
- lower precision.

The precision belongs to implementation.

---

## 132. Mixed Precision

Mixed precision may be used across representation operations.

Numerical symmetry tolerance must account for the chosen arithmetic.

---

## 133. Fixed-Point Representation

A hardware-facing implementation may encode selected features in fixed-point form.

Scaling and saturation must preserve enough information for the declared numerical contract.

---

## 134. Quantization of Equivariant Features

Independent componentwise quantization can introduce representation error.

The validation layer must measure the resulting equivariance residual.

---

## 135. Quantization Is Not Ternary Mapping

The distinction remains:

`numeric quantization ≠ semantic ternary classification`.

---

## 136. Representation Noise

Numerical or stochastic perturbation may be added to feature channels.

Its transformation behavior must be defined when symmetry preservation is required.

---

## 137. Isotropic Noise

A rotationally isotropic random perturbation may preserve symmetry statistically.

The random-state transformation contract must remain explicit.

---

## 138. Deterministic Representation

A deterministic representation layer produces the same features from identical complete input and parameters.

---

## 139. Representation Replay

Exact replay may require:

- canonical graph ordering;
- deterministic reductions;
- identical arithmetic;
- identical parameters.

---

## 140. Representation Hash

A serialized representation hash identifies bytes, not physical equivalence unless canonicalization is applied.

---

## 141. Symmetry-Equivalent Representations

Two transformed configurations produce different numeric equivariant vectors while remaining related exactly through:

`rho_EQ(g)`.

---

## 142. Invariant Representation Equality

Invariant scalar features should remain equal under the declared symmetry transformation within numerical tolerance.

---

## 143. Equivariance Residual

For representation:

`P_EQ`

define:

`epsilon_EQ(g,x) = d_EQ(P_EQ(g·x), rho_EQ(g)P_EQ(x))`.

---

## 144. Representation Metric

The metric:

`d_EQ`

must compare representation blocks according to their stored basis and multiplicities.

---

## 145. Blockwise Residual

A residual may be computed separately for each:

`(l,p)`.

This identifies which transformation type violates equivariance.

---

## 146. Scalar Residual

For invariant scalar block:

`epsilon_0 = ||s(gx) - s(x)||`.

---

## 147. Vector Residual

For vector block:

`epsilon_1 = ||v(gx) - Qv(x)||`.

---

## 148. Tensor Residual

For rank-two tensor:

`epsilon_2 = ||T(gx) - Q T(x) Q^T||`.

---

## 149. Permutation Residual

For per-atom representation:

`epsilon_perm = d(P_EQ(pi·x), pi·P_EQ(x))`.

---

## 150. Combined Residual

A combined transformation test may use:

`(g,pi)`.

The expected output is:

`rho_EQ(g,pi)P_EQ(x)`.

---

## 151. Identity Test

Verify:

`P_EQ(e·x) = P_EQ(x)`.

---

## 152. Composition Test

Verify representation consistency under:

`g1 g2`.

The expected output satisfies the representation composition law.

---

## 153. Inverse Test

Transform by:

`g`

and then:

`g^(-1)`.

The representation should return to the original state within numerical tolerance.

---

## 154. Reflection/Parity Test

For:

`O(3)`

models, test parity-even and parity-odd blocks separately.

---

## 155. Permutation Test

Permute atoms and verify all node, edge, and global features transform according to their declared permutation semantics.

---

## 156. Periodic-Image Test

Equivalent periodic-image descriptions must produce equivalent representation state under the periodicity contract.

---

## 157. Cutoff-Boundary Test

Configurations near graph cutoff boundaries require explicit treatment because a tiny numerical perturbation may change graph topology.

---

## 158. Representation Validation Domain

Equivariance validation should operate on configurations for which the graph correspondence under transformation is well defined according to the graph contract.

---

## 159. Graph Change and Representation Test

If a transformed input produces a different graph because of finite-precision cutoff ambiguity, this must be classified as a graph-boundary issue rather than silently as a representation failure.

---

## 160. Local Representation Validation

Local environment representations may be tested independently for:

- translation invariance;
- rotation equivariance;
- permutation handling;
- parity.

---

## 161. End-to-End Representation Validation

The full:

`configuration → graph → representation`

chain can be tested under combined transformations.

---

## 162. Message-Passing Compatibility

Chapter 05 requires every message representation to be constructible from the representation types defined here.

---

## 163. Message Input Types

A message may consume:

- receiver representations;
- source representations;
- radial scalars;
- angular representations;
- global invariant state.

---

## 164. Message Output Type

Every message must have an explicitly declared output representation type.

---

## 165. Aggregation Type Preservation

Messages aggregated by summation must belong to matching representation types.

---

## 166. Node Update Compatibility

The node update combines:

- current node state;
- aggregated message;
- optional invariant gates.

Only compatible types may be added directly.

---

## 167. Equivariant Residual Update

A residual update:

`h_i' = h_i + delta_i`

requires:

`h_i`

and:

`delta_i`

to carry the same representation type.

---

## 168. Representation Depth

Multiple layers may progressively encode larger graph neighborhoods.

Spatial transformation law remains unchanged at every depth.

---

## 169. Representation Scale

Representations may exist at:

- edge;
- atom;
- cluster;
- global

scales.

Each retains its own transformation and permutation contract.

---

## 170. Cluster Representation

A cluster may have scalar, vector, and tensor features derived from member atoms.

---

## 171. Cluster Position

If a cluster position is defined, it transforms as a point under Euclidean action.

---

## 172. Cluster Orientation

An orientation descriptor may transform nontrivially and may be undefined for symmetric clusters.

---

## 173. Multiscale Representation

A multiscale representation may be:

`X_EQ = X_EQ^(atom) × X_EQ^(cluster) × X_EQ^(global)`.

---

## 174. Cross-Scale Equivariance

Mappings between scale levels must preserve the relevant spatial transformation laws.

---

## 175. Pooling Equivariance

Pooling atom vectors into a cluster vector by summation preserves equivariance.

---

## 176. Invariant Pooling

Pooling scalar channels by sum or mean preserves spatial invariance and permutation invariance over the pooled set.

---

## 177. Unpooling

A coarse-to-fine mapping must distribute features in a permutation-consistent and equivariant manner.

---

## 178. Multiscale Information Loss

Pooling is generally non-injective.

Coarse representations cannot reconstruct the complete fine atomic state by identity.

---

## 179. Representation and Stability

Bounded representation norm does not imply stability of the complete dynamical system.

---

## 180. Representation Norm

An irrep block has an invariant Euclidean norm under orthogonal representation matrices when the basis is orthonormal.

---

## 181. Norm Is Not Physical Energy

The distinction remains:

`representation norm ≠ physical energy`.

---

## 182. Representation Change versus Structural Transition

A learned hidden representation may change continuously or abruptly without constituting a physical structural transition.

---

## 183. Representation Change versus Resonance Transition

A representation change may alter resonance coordinates.

It is not itself a resonance transition.

---

## 184. Representation Change versus Ternary Transition

Likewise:

`representation change ≠ ternary transition`.

---

## 185. Symmetry Channel versus Physical Phase

An irrep label:

`l`

does not represent a physical phase of matter.

---

## 186. Angular Degree versus Oscillator Phase

The angular representation degree:

`l`

is not oscillator phase:

`theta`.

---

## 187. Representation Vector versus Mechanical Force

A generic:

`l=1`

feature is not force.

Force is one specific vector-valued physical output.

---

## 188. Scalar Representation versus Energy

A generic:

`l=0`

feature is not energy.

Energy is one specific invariant scalar output with physical units and semantics.

---

## 189. Tensor Representation versus Stress

A generic tensor feature is not stress.

Stress requires the appropriate mechanical output contract.

---

## 190. Equivariance versus Conservativity

The distinction remains:

`equivariance ≠ conservativity`.

A model may be equivariant but nonconservative.

---

## 191. Energy-Conservative Path

A conservative model uses invariant scalar energy:

`E`

and obtains forces by differentiation.

---

## 192. Direct Equivariant Force Path

A model may predict an equivariant vector force directly.

Such a force requires a separate conservativity criterion if conservation is desired.

---

## 193. Representation Provenance

Representation components may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 194. Primary-Source Representation Structure

Established group representation theory, spherical harmonics, and Clebsch-Gordan structures retain:

`PRIMARY_SOURCE`

provenance.

---

## 195. Author-Defined Representation Architecture

TR-EIF-specific organization of equivariant channels and their connection to resonance and ternary layers carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 196. Derived Representation Feature

A feature analytically derived from existing geometry may carry:

`DERIVED`

provenance.

---

## 197. Calibrated Representation Parameter

A radial cutoff, basis scale, or representation parameter obtained through calibration carries:

`CALIBRATED`

provenance.

---

## 198. Benchmark Representation Result

Measured equivariance residual, throughput, memory use, or scaling behavior carries:

`BENCHMARK`

provenance.

---

## 199. Representation Test Fixture

Synthetic transformed configurations and expected representation relations carry:

`TEST_FIXTURE`

provenance.

---

## 200. Representation Scaling

Computational cost depends on:

- node count;
- edge count;
- channel multiplicity;
- `l_max`;
- tensor-product paths;
- network depth.

---

## 201. Angular Complexity

Increasing:

`l_max`

increases angular representation capacity and computational cost.

---

## 202. Multiplicity Complexity

Increasing:

`C_l`

increases channel capacity and memory.

---

## 203. Tensor-Product Path Count

The number of allowed tensor-product couplings depends on the retained input and output irreducible types.

---

## 204. Sparse Coupling

A model may restrict tensor-product paths to reduce cost.

The retained paths must still satisfy transformation rules.

---

## 205. Representation Pruning

Channels or coupling paths may be removed according to an architecture rule.

Pruning must not create invalid transformation mixing.

---

## 206. Learned Channel Selection

A learned invariant gate may suppress or activate channels.

The gate must preserve the representation type of the gated feature.

---

## 207. Representation Extension Rule

Any new representation channel must define:

1. scope;
2. transformation type;
3. `l`;
4. parity where applicable;
5. multiplicity;
6. units or dimensional semantics;
7. initialization;
8. allowed operations;
9. serialization;
10. validation.

---

## 208. Radial-Basis Extension Rule

Any new radial basis must define:

1. distance domain;
2. units;
3. basis functions;
4. cutoff behavior;
5. normalization;
6. numerical precision.

---

## 209. Angular-Basis Extension Rule

Any angular basis must define:

1. angular domain;
2. representation type;
3. basis convention;
4. parity;
5. truncation;
6. transformation validation.

---

## 210. Tensor-Product Extension Rule

Any tensor-product layer must define:

1. input irreducible types;
2. allowed output types;
3. coupling convention;
4. parity rule;
5. multiplicity mapping;
6. normalization;
7. numerical validation.

---

## 211. Normalization Extension Rule

Any normalization must define:

1. representation scope;
2. invariant statistics;
3. numerical epsilon;
4. per-node or global behavior;
5. transformation preservation.

---

## 212. Multiscale Representation Extension Rule

Any multiscale representation must define:

1. scale levels;
2. representation types per scale;
3. pooling;
4. cross-scale transformation;
5. information loss;
6. reconstruction or feedback semantics.

---

## 213. Canonical Representation Invariants

Every conforming equivariant representation preserves:

1. explicit spatial transformation type;

2. explicit atom-permutation behavior;

3. explicit parity where reflections are included;

4. explicit feature scope;

5. explicit representation coupling rules;

6. explicit numerical basis convention;

7. explicit validation method.

---

## 214. Canonical Scalar Invariant

Scalar representation channels satisfy the declared invariant transformation law.

---

## 215. Canonical Vector Invariant

Vector representation channels transform with the declared spatial vector representation.

---

## 216. Canonical Tensor Invariant

Tensor channels transform according to their declared tensor or irreducible representation.

---

## 217. Canonical Permutation Invariant

Per-atom representations permute consistently with atom labels.

Global scalar outputs remain permutation invariant.

---

## 218. Canonical Type-Separation Invariants

The framework preserves:

`scalar ≠ vector`

`vector ≠ tensor`

`scalar ≠ pseudoscalar`

`polar vector ≠ axial vector`

`representation ≠ atomic configuration`

`representation ≠ resonance state`

`representation ≠ ternary state`

`representation norm ≠ energy`

`generic vector feature ≠ force`

`generic tensor feature ≠ stress`.

---

## 219. Canonical TR Integration Invariants

The representation layer remains upstream of:

`resonance`

`→ ternary target`

`→ neutral-mediated execution`.

A geometric representation does not directly mutate:

`t_exec`.

---

## 220. Canonical Ternary Boundary

Any scalar ternary feature generated from equivariant state must map explicitly into:

`-1/0/1`.

The state:

`0`

remains active neutral.

Zero-valued geometric or representation features remain distinct from ternary neutral.

---

## 221. Canonical Scientific Distinctions

The representation layer preserves:

`equivariance ≠ invariance`

`equivariance ≠ conservativity`

`generic scalar ≠ energy`

`generic vector ≠ force`

`generic tensor ≠ stress`

`angular irrep degree ≠ oscillator phase`

`representation change ≠ structural transition`

`representation change ≠ resonance transition`

`representation change ≠ ternary transition`

`spatial rotation ≠ ternary polarity reversal`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`.

---

## 222. Canonical Representation Chain

The complete representation chain is:

`atomic configuration`

`→ graph geometry`

`→ radial invariant basis`

`+ angular equivariant basis`

`→ irreducible representation channels`

`→ tensor-product coupling`

`→ equivariant hidden state`

`→ message passing`.

---

## 223. Canonical TR-EIF Chain

The integrated chain is:

`X_conf`

`→ X_G`

`→ X_EQ`

`→ X_R`

`→ T_target`

`→ T_exec`

`→ energy / force / stress feedback interfaces`.

Each transition between spaces is explicit.

---

## 224. Interface to Chapter 05

Chapter 05 develops Message Passing.

It uses the representation types defined here for:

- source node state;
- receiver node state;
- edge geometry;
- messages;
- aggregation;
- node updates;
- residual paths.

---

## 225. Interface to Chapter 06

Chapter 06 develops Resonance Parameterization.

It maps invariant and equivariant representation channels into:

`X_R`.

The resonance transformation law must be declared.

---

## 226. Interface to Chapter 07

Chapter 07 develops Ternary Feature Channels.

It defines exact mappings from selected invariant or transformation-compatible features into:

`-1/0/1`.

---

## 227. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

The energy head consumes equivariant representations and terminates in an invariant scalar with physical energy semantics.

---

## 228. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

It defines vector and tensor outputs and their relation to the conservative energy functional.

---

## 229. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each family member must declare:

- representation group;
- parity support;
- `l_max`;
- channel multiplicities;
- radial basis;
- tensor-product paths;
- pooling;
- output heads.

---

## 230. Final Formal Structure

The equivariant representation layer may be represented as:

`ER = (X_EQ, I, P_EQ, rho_EQ, B_rad, B_ang, TP, N_EQ)`.

Here:

- `X_EQ` is the representation state space;
- `I` is the set of representation types;
- `P_EQ` maps configuration and graph state into representation state;
- `rho_EQ` is the group action on representation state;
- `B_rad` is the radial basis family;
- `B_ang` is the angular basis family;
- `TP` is the tensor-product coupling structure;
- `N_EQ` denotes transformation-preserving nonlinear and normalization operators.

A conforming representation satisfies:

`P_EQ(rho_in(g)x) = rho_EQ(g)P_EQ(x)`.

---

## 231. Final Statement

Equivariant representations provide the transformation-preserving feature space connecting atomic geometry to learned and analytic interatomic mappings.

Scalar channels remain invariant.

Vector, tensor, and higher irreducible channels transform according to their declared group representations.

Parity distinguishes transformation behavior under reflections and inversion.

Radial functions encode invariant distance dependence.

Angular bases encode directional structure.

Tensor products couple representation channels without destroying equivariance.

Permutation symmetry remains distinct from spatial symmetry and is preserved through atom-index-consistent feature transformation and neighbor aggregation.

The framework preserves:

`representation ≠ configuration`

`representation ≠ resonance`

`representation ≠ ternary state`

`generic scalar ≠ energy`

`generic vector ≠ force`

`generic tensor ≠ stress`

`equivariance ≠ conservativity`

`spatial rotation ≠ ternary polarity reversal`.

The canonical path remains:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

These definitions establish the representation structure required for the Message Passing formalism developed in Chapter 05.
