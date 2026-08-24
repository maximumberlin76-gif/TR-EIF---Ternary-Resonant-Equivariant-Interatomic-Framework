# E(3) Group Actions

## 1. Purpose

This chapter defines the Euclidean-group transformation structure used by the Equivariant Interatomic Framework.

The atomic configuration layer provides positions, species, periodic state, and interaction graphs.

The present chapter defines how these objects transform under:

- translation;
- proper rotation;
- reflection;
- inversion where applicable;
- Euclidean transformations;
- atom permutations;
- combined spatial and permutation actions.

The principal objective is to formalize the symmetry contract required by:

- equivariant representations;
- message passing;
- resonance parameterization;
- ternary feature channels;
- energy;
- forces;
- stress;
- multiscale transfer.

The canonical geometric chain is:

`atomic configuration`

`→ group action`

`→ invariant/equivariant representation`

`→ equivariant message passing`

`→ invariant scalar outputs`

`→ equivariant vector/tensor outputs`.

---

## 2. Euclidean Space

Atomic positions belong to:

`R^3`.

For atom:

`i`

the position is:

`r_i ∈ R^3`.

A complete atomic coordinate state is:

`R = (r_1, ..., r_N)`.

---

## 3. Translation Group

The translation group is:

`T(3) = (R^3, +)`.

For:

`c ∈ R^3`

the translation action on an atomic position is:

`r_i → r_i + c`.

---

## 4. Rotation Group

The proper rotation group is:

`SO(3)`.

A matrix:

`Q ∈ SO(3)`

satisfies:

`Q^T Q = I`

and:

`det(Q) = 1`.

---

## 5. Orthogonal Group

The orthogonal group is:

`O(3)`.

A matrix:

`Q ∈ O(3)`

satisfies:

`Q^T Q = I`

and:

`det(Q) ∈ {-1, 1}`.

Therefore:

`SO(3) ⊂ O(3)`.

---

## 6. Reflection

An orthogonal transformation with:

`det(Q) = -1`

contains orientation reversal.

Such transformations include reflections and improper rotations.

Whether the model requires:

`SO(3)`

or:

`O(3)`

equivariance must be explicit.

---

## 7. Euclidean Group

The Euclidean group is the semidirect product:

`E(3) = O(3) ⋉ R^3`.

An element may be represented as:

`g = (Q, c)`.

Its action on a position is:

`r_i' = Q r_i + c`.

---

## 8. Special Euclidean Group

If orientation-reversing transformations are excluded:

`SE(3) = SO(3) ⋉ R^3`.

The model must distinguish:

`E(3)`

from:

`SE(3)`.

---

## 9. Group Composition

For:

`g_1 = (Q_1, c_1)`

and:

`g_2 = (Q_2, c_2)`

the composition is:

`g_1 g_2 = (Q_1 Q_2, Q_1 c_2 + c_1)`.

This follows from successive action on:

`r`.

---

## 10. Identity Element

The Euclidean-group identity is:

`e = (I, 0)`.

It satisfies:

`e · r = r`.

---

## 11. Inverse Element

For:

`g = (Q, c)`

the inverse is:

`g^(-1) = (Q^T, -Q^T c)`.

---

## 12. Group Action on Atomic Configuration

Let:

`X_conf`

be an atomic configuration.

The spatial group action is:

`rho_conf(g): X_conf → X_conf`.

For positions:

`r_i' = Q r_i + c`.

Species remain unchanged under spatial transformation.

---

## 13. Species under Spatial Action

For spatial:

`g ∈ E(3)`

species identity satisfies:

`a_i' = a_i`.

Spatial transformations do not change chemical species.

---

## 14. Mass under Spatial Action

Atomic mass is a scalar under Euclidean transformations:

`m_i' = m_i`.

---

## 15. Charge under Spatial Action

Atomic charge is a scalar under spatial transformations:

`q_i' = q_i`.

---

## 16. Velocity Transformation

For rigid-frame rotation:

`v_i' = Q v_i`.

A global spatial translation of positions does not add to velocity under the static configuration-group action.

Time-dependent coordinate transformations require a separate dynamical treatment.

---

## 17. Force Transformation

A physical force vector transforms as:

`F_i' = Q F_i`.

Therefore force is rotation/reflection equivariant as a polar vector under the selected spatial group.

---

## 18. Stress Transformation

A second-order stress tensor transforms as:

`Sigma' = Q Sigma Q^T`.

This tensor transformation law must be preserved by the force/stress layer.

---

## 19. Relative Position under Euclidean Action

For:

`r_ij = r_j - r_i`

the transformed relative vector is:

`r_ij' = Q r_ij`.

The translation:

`c`

cancels.

---

## 20. Translation Invariance of Relative Position

Relative position satisfies:

`r_ij(R + c) = r_ij(R)`.

Therefore it is translation invariant.

---

## 21. Rotation Equivariance of Relative Position

For:

`Q ∈ O(3)`

the relative vector satisfies:

`r_ij(QR) = Q r_ij(R)`.

---

## 22. Distance Invariance

Pair distance is:

`d_ij = ||r_ij||`.

Because orthogonal transformations preserve norm:

`d_ij' = d_ij`.

Therefore distance is:

- translation invariant;
- rotation invariant;
- reflection invariant.

---

## 23. Inner Product Invariance

For vectors:

`u`

and:

`v`

and:

`Q ∈ O(3)`:

`(Qu) · (Qv) = u · v`.

Inner products therefore provide invariant scalar constructions.

---

## 24. Angle Invariance

For nonzero:

`u`

and:

`v`

the angle relation:

`cos(phi) = (u · v) / (||u|| ||v||)`

is invariant under:

`O(3)`.

---

## 25. Cross Product

For:

`Q ∈ SO(3)`:

`(Qu) × (Qv) = Q(u × v)`.

For:

`Q ∈ O(3)`:

`(Qu) × (Qv) = det(Q) Q(u × v)`.

Therefore the cross product transforms as an axial vector.

---

## 26. Polar Vector

A polar vector transforms as:

`v' = Q v`.

Examples include:

- position displacement;
- velocity;
- force.

---

## 27. Axial Vector

An axial vector transforms as:

`a' = det(Q) Q a`.

Examples can include angular-momentum-like quantities or cross products of polar vectors.

---

## 28. Scalar

A true scalar satisfies:

`s' = s`

under:

`O(3)`.

Examples include:

- distance;
- mass;
- scalar energy.

---

## 29. Pseudoscalar

A pseudoscalar satisfies:

`s' = det(Q) s`.

It is invariant under proper rotations but changes sign under orientation reversal.

---

## 30. Tensor

A rank-two polar tensor transforms as:

`T' = Q T Q^T`.

Higher-rank tensors transform with one factor of:

`Q`

per index.

---

## 31. Representation Space

Let:

`X_Y`

be a feature or output space.

A group representation is:

`rho_Y(g)`.

A map:

`F: X_conf → X_Y`

is equivariant when:

`F(rho_conf(g)x) = rho_Y(g) F(x)`.

---

## 32. Invariant Mapping

A map is invariant when:

`F(rho_conf(g)x) = F(x)`.

This corresponds to a trivial representation on the output.

---

## 33. Equivariance versus Invariance

The distinction is:

`equivariance ≠ invariance`.

Invariant outputs remain unchanged.

Equivariant outputs transform predictably.

---

## 34. Scalar Energy Invariance

For an isolated interatomic model without symmetry-breaking external fields:

`E(g · X) = E(X)`

for admissible:

`g`.

Energy is therefore a scalar invariant under the declared spatial symmetry.

---

## 35. Force Equivariance from Invariant Energy

If:

`E(R)`

is differentiable and rotation invariant, and:

`F_i = -grad_(r_i) E`,

then force transforms equivariantly:

`F_i(QR) = Q F_i(R)`

under the applicable assumptions.

---

## 36. Translation Invariance and Net Force

For a differentiable energy invariant under global translation:

`E(R + c) = E(R)`.

Differentiation with respect to:

`c`

gives:

`sum_i grad_(r_i) E = 0`.

Therefore:

`sum_i F_i = 0`

for the internal conservative force model under the corresponding assumptions.

---

## 37. Rotation Invariance and Torque Relation

Rotational invariance imposes a corresponding constraint on internal torque.

For conservative isolated systems this produces a relation involving:

`sum_i r_i × F_i`.

The precise form depends on origin and external-field assumptions.

---

## 38. Translation-Invariant Energy

A scalar interatomic energy should not depend on absolute origin unless an external position-dependent field is included.

---

## 39. External Field Boundary

An external field may alter symmetry.

For example, if:

`b ∈ R^3`

is a fixed laboratory vector and remains untransformed while atoms rotate, full rotational invariance is broken.

---

## 40. Joint Field Transformation

If an external vector field is part of the model state and transforms as:

`b' = Q b`,

then equivariance may be restored in the enlarged state space.

---

## 41. Symmetry Group Is Model-Relative

The applicable symmetry group depends on the complete state and external conditions.

TR-EIF does not assume full:

`E(3)`

symmetry when the physical model explicitly breaks it.

---

## 42. Permutation Group

For:

`N`

labeled atoms, the permutation group is:

`S_N`.

A permutation:

`pi ∈ S_N`

relabels atomic indices.

---

## 43. Species-Preserving Permutation Group

For systems containing different species, the physically admissible permutation subgroup exchanges atoms only within species-equivalent classes unless another model relation is defined.

---

## 44. Permutation Action on Positions

Under permutation:

`pi`

the position state transforms by reindexing:

`r_i' = r_(pi(i))`

under the selected convention.

---

## 45. Permutation Action on Species

Species labels transform consistently:

`a_i' = a_(pi(i))`.

---

## 46. Permutation Action on Per-Atom Features

A per-atom feature:

`h_i`

transforms by corresponding reindexing:

`h_i' = h_(pi(i))`.

---

## 47. Permutation-Invariant Global Output

A global scalar:

`y`

is permutation invariant when:

`y(pi · X) = y(X)`.

Energy belongs to this class under atom relabeling.

---

## 48. Permutation-Equivariant Per-Atom Output

A per-atom output:

`Y = (y_1, ..., y_N)`

must transform by the same permutation as the atoms.

Forces belong to this class with respect to atom indexing.

---

## 49. Combined Spatial and Permutation Action

A complete symmetry action may combine:

`g ∈ E(3)`

and:

`pi ∈ S_N`.

The combined action is:

`(g, pi) · X`.

Spatial and permutation transformations act on different aspects of state.

---

## 50. Commutation of Spatial and Permutation Actions

For standard atomic coordinates, global spatial transformation and atom relabeling commute:

`g · (pi · X) = pi · (g · X)`.

This permits product-group treatment in many representations.

---

## 51. Product Symmetry Structure

A configuration may therefore carry a symmetry action of:

`E(3) × S_species`

where:

`S_species`

denotes the applicable species-preserving permutation group.

---

## 52. Graph Transformation under Permutation

For interaction graph:

`G = (V, E)`

a permutation relabels nodes and edge endpoints consistently.

---

## 53. Graph Transformation under Translation

For geometry-based graph rules using relative state, translation leaves graph connectivity unchanged.

---

## 54. Graph Transformation under Rotation

For distance-based connectivity, rotation leaves topology unchanged while directional edge features rotate.

---

## 55. Graph Equivariance

Graph construction should satisfy:

`P_G((g, pi) · X) = (g, pi) · P_G(X)`

under the declared graph symmetry contract.

---

## 56. Node Scalar Feature

A scalar node feature:

`h_i^(0)`

is invariant under spatial rotation.

It still permutes under atom relabeling.

---

## 57. Node Vector Feature

A node vector:

`h_i^(1) ∈ R^3`

transforms:

`h_i^(1)' = Q h_(pi(i))^(1)`.

---

## 58. Edge Scalar Feature

A radial basis feature:

`phi(d_ij)`

is spatially invariant.

It reindexes with the edge under atom permutation.

---

## 59. Edge Vector Feature

Relative displacement transforms:

`r_ij' = Q r_(pi(i)pi(j))`

under the combined action, with indexing interpreted consistently.

---

## 60. Feature Type

Each feature channel must declare:

- spatial transformation type;
- permutation behavior;
- parity where reflections are included;
- tensor rank or irreducible representation type.

---

## 61. Feature-Type Mixing

Features with incompatible transformation laws must not be combined through arbitrary arithmetic if equivariance is to be preserved.

The allowed operations depend on representation type.

---

## 62. Scalar Addition

Two scalar channels may be added:

`s = s_1 + s_2`.

The result remains scalar.

---

## 63. Vector Addition

Two vectors transforming under the same representation may be added.

The result remains equivariant.

---

## 64. Scalar-Vector Multiplication

If:

`s`

is invariant scalar and:

`v`

is equivariant vector:

`s v`

transforms as a vector.

---

## 65. Vector Dot Product

For polar vectors:

`u`

and:

`v`

the dot product:

`u · v`

is an invariant scalar under:

`O(3)`.

---

## 66. Vector Outer Product

The outer product:

`u ⊗ v`

transforms as a rank-two tensor.

---

## 67. Tensor Contraction

Appropriate contraction of matching tensor indices can produce lower-rank equivariant or invariant features.

---

## 68. Nonlinearity on Scalars

An arbitrary scalar nonlinearity:

`f(s)`

preserves scalar invariance.

---

## 69. Nonlinearity on Vectors

Applying arbitrary componentwise nonlinearities to a vector generally does not preserve rotational equivariance.

Equivariant vector nonlinearities require structured operations.

---

## 70. Gated Vector Nonlinearity

A scalar gate:

`g`

may multiply vector:

`v`

as:

`g v`.

If:

`g`

is invariant, the result remains equivariant.

---

## 71. Norm-Based Nonlinearity

A vector may be transformed through its invariant norm:

`v' = f(||v||) v`.

This preserves vector equivariance when defined consistently.

---

## 72. Representation Direct Sum

Feature spaces may contain direct sums of representation types.

A state may be written conceptually as:

`X_feat = X_scalar ⊕ X_vector ⊕ X_tensor ⊕ ...`.

---

## 73. Irreducible Representation Label

For:

`SO(3)`

features may be organized by angular momentum index:

`l = 0, 1, 2, ...`.

Here:

- `l = 0` corresponds to scalar;
- `l = 1` corresponds to vector-like representation;
- higher `l` correspond to higher angular representation types.

---

## 74. Irreducible Representation Dimension

An:

`SO(3)`

irreducible representation of degree:

`l`

has dimension:

`2l + 1`.

---

## 75. O(3) Parity

For:

`O(3)`

an irreducible type additionally carries parity.

A channel may therefore be labeled by:

`(l, p)`.

---

## 76. Parity

The parity label distinguishes behavior under inversion or reflection.

The exact sign convention must remain consistent across representation construction and implementation.

---

## 77. Scalar Parity

A true scalar has even parity.

A pseudoscalar has odd parity.

---

## 78. Vector Parity

A polar vector and axial vector have different parity behavior under inversion.

This distinction matters in:

`O(3)`-equivariant models.

---

## 79. Spherical Harmonics

Directional dependence may be represented using spherical harmonics:

`Y_lm(e_hat_ij)`.

These form basis functions carrying:

`SO(3)`

irreducible transformation structure.

---

## 80. Spherical Harmonic Degree

For fixed:

`l`

the components:

`m = -l, ..., l`

transform together under rotation.

---

## 81. Rotation of Spherical Harmonics

Under rotation:

`Q`

the vector of:

`Y_lm`

components transforms through the corresponding representation matrix:

`D^l(Q)`.

---

## 82. Radial-Angular Separation

An equivariant edge feature may be built as:

`R_n(d_ij) Y_lm(e_hat_ij)`.

The radial part is invariant.

The angular part carries the rotational representation.

---

## 83. Tensor Product

Two representation channels may be combined through a tensor product.

The resulting representation decomposes into irreducible components.

---

## 84. Clebsch-Gordan Decomposition

For:

`SO(3)`

the tensor product of degrees:

`l_1`

and:

`l_2`

decomposes over:

`l`

satisfying:

`|l_1 - l_2| ≤ l ≤ l_1 + l_2`.

The coupling coefficients are given by the corresponding Clebsch-Gordan structure.

---

## 85. Equivariant Tensor Product

A tensor-product layer must preserve the group transformation law through appropriate representation coupling.

---

## 86. Scalar Extraction

An invariant scalar may be obtained by coupling representation channels to:

`l = 0`.

---

## 87. Vector Extraction

A vector-like output may be obtained through an:

`l = 1`

channel.

---

## 88. Energy Output Type

A scalar energy model terminates in an invariant:

`l = 0`

output with the applicable even parity.

---

## 89. Force Output Type

Force is a per-atom polar vector.

Its output representation must transform accordingly.

---

## 90. Stress Output Type

Stress is a rank-two tensor.

Its decomposition may include scalar and higher-order irreducible components depending on representation.

---

## 91. Equivariant Representation Mapping

The next chapter defines:

`P_EQ: X_conf × X_G → X_EQ`.

The present chapter supplies the transformation laws that:

`P_EQ`

must satisfy.

---

## 92. Equivariant Representation Condition

For:

`g`

in the declared symmetry group:

`P_EQ(g · X) = rho_EQ(g) P_EQ(X)`.

---

## 93. Message Equivariance

A message function:

`M`

must satisfy the corresponding transformation law.

For source:

`j`

and receiver:

`i`:

`m_ij' = rho_M(g) m_ij`

when inputs are transformed consistently.

---

## 94. Aggregation and Equivariance

Permutation-invariant aggregation across neighbors preserves node permutation equivariance when messages are reindexed consistently.

Spatial equivariance is preserved when summed messages belong to the same representation type.

---

## 95. Sum Aggregation

For messages of one representation type:

`m_i = sum_(j ∈ N_i) m_ij`

transforms according to the same representation.

---

## 96. Mean Aggregation

Mean aggregation also preserves the representation type when neighborhood normalization is invariant.

---

## 97. Weighted Aggregation

If:

`w_ij`

is an invariant scalar:

`m_i = sum_j w_ij m_ij`

preserves the transformation type of:

`m_ij`.

---

## 98. Direction-Dependent Weight

A directional weight must itself transform appropriately.

Using an arbitrary orientation-dependent scalar can break rotational invariance.

---

## 99. Attention Weight

An attention coefficient intended to be a scalar weight should be constructed from invariant quantities if the resulting message sum is expected to preserve rotation equivariance.

---

## 100. Equivariant Attention

More general attention mechanisms may carry representation-valued quantities.

Their transformation law must be explicitly defined.

---

## 101. Global Pooling

A global scalar pooling over node scalar features may use:

`sum_i h_i`.

This preserves permutation invariance.

---

## 102. Global Vector Pooling

Summing equivariant node vectors produces a global equivariant vector.

---

## 103. Centering

Global translation can be removed by using relative vectors or centered coordinates.

Centering does not itself create rotational invariance.

---

## 104. Center of Mass

The center of mass transforms:

`r_cm' = Q r_cm + c`.

Centered coordinates satisfy:

`r_i - r_cm → Q(r_i - r_cm)`.

---

## 105. Centering and Periodicity

Naive center-of-mass centering may be ambiguous under periodic boundaries.

Periodic systems require a compatible representation.

---

## 106. Periodic Translation

Under periodic boundaries, lattice translations represent equivalent images.

The group action must be compatible with the cell representation.

---

## 107. Cell Rotation

For global rotation:

`Q`

the cell matrix transforms according to the selected lattice-vector convention.

If columns are lattice vectors:

`H' = Q H`.

---

## 108. Fractional Coordinates under Rotation

If:

`r_i = H s_i`

and both:

`r_i`

and:

`H`

rotate by:

`Q`

then fractional coordinates may remain unchanged:

`s_i' = s_i`.

---

## 109. Periodic Image Shift

The integer image shift:

`n_ij`

is lattice-index metadata.

Under a rigid rotation of the entire cell and positions, the integer shift remains the same under the same lattice basis indexing.

---

## 110. Cell Deformation

A general cell deformation is not merely an:

`E(3)`

transformation.

It changes metric structure and can change energy and stress.

---

## 111. Strain versus Rotation

A pure rotation preserves distances.

A strain generally does not.

Therefore:

`rotation ≠ deformation`.

---

## 112. Stress and Cell Transformation

Stress transformation under rigid rotation follows tensor equivariance.

Stress response under strain belongs to the mechanical model.

---

## 113. Permutation and Cell State

Atom permutations do not alter the cell matrix.

---

## 114. Species-Permutation Compatibility

A spatial transformation does not change species identity.

A species-preserving permutation changes only atom indexing.

These operations remain semantically distinct.

---

## 115. Symmetry Orbit

For configuration:

`X`

the orbit is:

`Orb(X) = {g · X | g ∈ G}`.

An invariant scalar is constant along this orbit.

---

## 116. Stabilizer

The stabilizer is:

`Stab(X) = {g ∈ G | g · X = X}`.

It represents exact symmetries of the configuration.

---

## 117. Symmetric Structure

A crystal or molecular configuration may possess a nontrivial stabilizer subgroup.

This can constrain representation channels and degeneracies.

---

## 118. Symmetry-Equivalent Configurations

Two configurations on the same group orbit are symmetry-equivalent under the selected action.

---

## 119. Symmetry Equivalence versus Physical Equality

Symmetry-equivalent configurations need not have identical coordinate arrays.

They represent equivalent geometry under the declared symmetry.

---

## 120. Canonical Frame

A model may transform configurations into a canonical orientation.

Canonicalization is distinct from equivariant processing.

---

## 121. Canonicalization

A canonicalization map attempts to choose one representative from a symmetry orbit.

Such a map may be discontinuous or ambiguous for symmetric configurations.

---

## 122. Equivariance without Canonicalization

Equivariant architectures do not require selecting one canonical orientation.

They propagate transformation structure directly.

---

## 123. Frame Degeneracy

A local frame defined from geometry can become ambiguous when defining vectors are:

- zero;
- collinear;
- symmetry-degenerate.

Frame-based methods must define these cases explicitly.

---

## 124. Frame-Free Equivariance

Irreducible representation methods avoid the need for a unique geometric local frame.

---

## 125. Equivariance Error

For mapping:

`F`

define an equivariance residual:

`epsilon_eq(g, x) = d_Y(F(g · x), rho_Y(g)F(x))`.

The metric:

`d_Y`

must match the output representation.

---

## 126. Invariance Error

For invariant scalar mapping:

`f`

define:

`epsilon_inv(g, x) = |f(g · x) - f(x)|`.

---

## 127. Exact Mathematical Equivariance

In the formal model:

`epsilon_eq = 0`

for every admissible:

`g`

and:

`x`.

---

## 128. Numerical Equivariance

Finite-precision implementation may produce a nonzero residual.

The numerical acceptance tolerance must be defined separately.

---

## 129. Numerical Equivariance versus Formal Equivariance

The distinction is:

`formal equivariance ≠ finite-precision residual`.

The formal transformation law remains exact.

---

## 130. Permutation Residual

For permutation-equivariant per-atom output:

`epsilon_perm(pi, x)`

may compare permuted reference outputs with outputs of permuted input.

---

## 131. Translation Test

For arbitrary translation:

`c`

verify the declared transformation law.

Invariant quantities should remain unchanged.

Relative vectors should remain unchanged.

---

## 132. Rotation Test

For:

`Q ∈ SO(3)`

verify:

- scalar invariance;
- vector equivariance;
- tensor equivariance;
- per-atom permutation consistency where combined.

---

## 133. Reflection Test

For:

`Q ∈ O(3)`

with:

`det(Q) = -1`

verify parity-sensitive behavior when:

`O(3)`

symmetry is claimed.

---

## 134. Inversion Test

Spatial inversion may be represented by:

`Q = -I`.

Its determinant in three dimensions is:

`-1`.

This test distinguishes parity-even and parity-odd channels.

---

## 135. Combined Transformation Test

A strong test may apply:

- atom permutation;
- rotation;
- translation

simultaneously.

The output must satisfy the complete combined transformation law.

---

## 136. Sequential Transformation Test

For:

`g_1`

and:

`g_2`

verify:

`rho(g_1 g_2)x = rho(g_1)rho(g_2)x`.

This tests representation consistency.

---

## 137. Identity Test

Verify:

`rho(e)x = x`.

---

## 138. Inverse Test

Verify:

`rho(g^(-1))rho(g)x = x`

within the numerical comparison contract.

---

## 139. Distance Preservation Test

For orthogonal:

`Q`

verify:

`||Q r_ij|| = ||r_ij||`.

---

## 140. Inner-Product Preservation Test

Verify:

`(Q u) · (Q v) = u · v`.

---

## 141. Energy Invariance Test

For invariant energy model:

`E(g · X) = E(X)`

within numerical tolerance.

---

## 142. Force Equivariance Test

For force output:

`F_i(g · X) = Q F_i(X)`

with atom reindexing applied when permutation is included.

---

## 143. Stress Equivariance Test

For stress:

`Sigma(g · X) = Q Sigma(X) Q^T`.

---

## 144. Graph Equivariance Test

Transform atomic configuration, rebuild graph, and verify:

- topology consistency;
- edge reindexing;
- relative-vector transformation;
- invariant edge quantities.

---

## 145. Message Equivariance Test

Transform graph inputs and verify message outputs transform under the declared representation.

---

## 146. Layerwise Equivariance

An architecture may test equivariance after each representation layer.

This can localize violations.

---

## 147. End-to-End Equivariance

An end-to-end test verifies the final model transformation law.

Layerwise success and end-to-end success are distinct validation scopes.

---

## 148. Equivariance under Dynamic Graphs

When graph topology depends only on invariant geometric criteria such as distance, rigid spatial transformations should preserve graph connectivity.

The downstream equivariance test can then proceed on corresponding graphs.

---

## 149. Cutoff Boundary Sensitivity

If a pair lies numerically near:

`r_cut`

finite precision may cause topology differences after a transformation.

Equivariance tests should define treatment of cutoff-boundary cases.

---

## 150. Equivariance Domain

A model may claim equivariance only within a defined admissible domain.

The domain must be stated.

---

## 151. Symmetry-Breaking Inputs

Any state variable that is held fixed under a transformation while it physically should transform can break equivariance.

Therefore the complete input transformation must be defined.

---

## 152. Gauge-Like Internal Freedom

A learned latent basis may possess internal basis freedom unrelated to physical Euclidean symmetry.

Such internal transformations must not be conflated with:

`E(3)`.

---

## 153. Geometric Symmetry versus Feature Basis

Changing basis within a representation space is not the same as rotating the physical atomic configuration.

---

## 154. Coordinate Frame versus Physical State

A global coordinate-frame change should not change invariant physical outputs.

It should transform equivariant outputs predictably.

---

## 155. Physical Rotation versus Coordinate Rotation

For isolated Euclidean systems, rotating the physical configuration and rotating the coordinate frame can produce related mathematical descriptions.

The model contract should specify the active transformation convention used in tests.

---

## 156. Active Transformation

In an active transformation:

`r_i → Q r_i + c`.

The coordinate basis is held fixed while the configuration moves.

---

## 157. Passive Transformation

A passive coordinate change transforms coordinate representation instead of the physical object.

Active and passive conventions must not be mixed in one derivation.

---

## 158. TR-EIF Convention

TR-EIF transformation tests use explicit declared actions on state variables.

The implementation must remain internally consistent with that convention.

---

## 159. Resonance-State Transformation

A resonance state may contain:

- invariant scalar components;
- equivariant vector components;
- tensor components.

Its transformation law must be defined by:

`rho_R(g)`.

---

## 160. Scalar Resonance Coordinate

A scalar resonance coordinate satisfies:

`r_s(g · X) = r_s(X)`.

---

## 161. Vector Resonance Coordinate

A vector resonance coordinate satisfies:

`r_v(g · X) = Q r_v(X)`.

---

## 162. Tensor Resonance Coordinate

A tensor resonance coordinate transforms through the corresponding tensor representation.

---

## 163. Resonance Classification

A categorical resonance class intended to describe geometry-independent regime membership is typically invariant under rigid Euclidean transformation.

The classifier must satisfy:

`C_R(rho_R(g)r) = C_R(r)`

when that invariance is part of its definition.

---

## 164. Ternary Target Transformation

A scalar ternary target:

`t_target ∈ {-1, 0, 1}`

is spatially invariant unless the specialization explicitly defines a nontrivial geometric action on ternary channels.

---

## 165. Ternary State and Spatial Rotation

The canonical balanced ternary values:

`-1/0/1`

do not rotate as spatial vectors.

---

## 166. Geometry Does Not Flip Ternary Polarity by Identity

A rotation or reflection does not automatically imply:

`-1 ↔ 1`.

Any polarity transformation law requires an explicit semantic definition.

---

## 167. Active Neutral under Spatial Transformation

The ternary state:

`0`

remains:

`0`

under ordinary geometric transformation of the atomic configuration when the ternary channel is scalar invariant.

---

## 168. Ternary Feature Equivariance Boundary

If a future specialization assigns ternary states to orientation-dependent representation channels, the transformation law must be explicitly defined.

The standard balanced ternary scalar channel remains categorical and invariant.

---

## 169. TR Execution Invariance

Rigid spatial transformation does not alter the canonical execution topology:

`-1 ↔ 0 ↔ 1`.

---

## 170. Direct-Opposite Exclusion under Symmetry

The forbidden committed transitions remain:

`-1 → 1`

and:

`1 → -1`

under any geometric transformation.

---

## 171. Symmetry and Target/Execution Separation

Spatial symmetry does not collapse:

`t_target`

and:

`t_exec`.

Their semantic separation remains unchanged.

---

## 172. Resonance versus Geometry

A resonance descriptor may depend on geometry.

The descriptor is still distinct from the geometry itself.

---

## 173. Phase versus Spatial Rotation

Oscillator phase:

`theta`

belongs to:

`S^1`.

A spatial rotation:

`Q ∈ SO(3)`

does not act on oscillator phase by identity.

Any coupling between spatial orientation and oscillator phase must be explicitly defined.

---

## 174. Oscillator Phase versus Geometric Angle

The distinction is:

`oscillator phase ≠ geometric orientation angle`.

Both may be angular quantities but belong to different state spaces.

---

## 175. Phase Coupling versus Spatial Force

The distinction remains:

`phase coupling ≠ mechanical force`.

---

## 176. Phase Relation versus Chemical Bond

The distinction remains:

`phase relation ≠ chemical bond`.

---

## 177. Equivariance and Energy

Energy may depend on equivariant hidden representations while remaining a final invariant scalar.

---

## 178. Equivariance and Force

Forces may be produced directly by an equivariant vector head or derived from invariant energy.

The chosen force construction must preserve the required transformation law.

---

## 179. Conservative Force Path

For conservative model:

`E: X_conf → R`

and:

`F_i = -grad_(r_i) E`.

The energy remains invariant.

The force remains equivariant.

---

## 180. Direct Force Path

A model may predict forces directly:

`F: X_conf → R^(3N)`.

Then equivariance must be enforced directly:

`F(g · X) = rho_F(g)F(X)`.

---

## 181. Conservative versus Direct Force Model

A direct equivariant force model is not automatically conservative.

Conservativity requires an independently defined potential-energy relation.

---

## 182. Equivariance Does Not Imply Conservativity

The distinction is:

`equivariant force ≠ conservative force`.

---

## 183. Conservativity Does Not Alone Define Equivariance

A conservative force derived from a symmetry-breaking energy may fail the desired Euclidean equivariance.

Both properties require their own conditions.

---

## 184. Stress Invariance Boundary

Stress is not an invariant scalar.

It transforms as a tensor.

---

## 185. Scalar Pressure

Hydrostatic pressure is a scalar quantity under rigid rotation.

It may be derived from stress under a declared sign convention.

---

## 186. Virial-Like Tensor Boundary

A virial-like quantity involving:

`r_ij ⊗ F_ij`

is tensor-valued.

Its physical interpretation and counting convention must be separately defined.

---

## 187. Equivariant Message Passing Chain

The canonical equivariant graph chain is:

`node/edge representations`

`→ equivariant message`

`→ permutation-invariant aggregation`

`→ equivariant node update`

`→ invariant/equivariant output`.

---

## 188. Scalar Message

A scalar message is spatially invariant.

---

## 189. Vector Message

A vector message transforms as:

`m_ij' = Q m_ij`.

---

## 190. Tensor Message

A tensor message transforms according to its representation.

---

## 191. Receiver-State Dependence

A directed message:

`j → i`

may depend asymmetrically on:

`h_i`

and:

`h_j`.

This does not violate spatial equivariance when the transformation law is preserved.

---

## 192. Permutation-Safe Receiver Semantics

Under atom permutation, receiver identity is relabeled consistently.

Directed message orientation is preserved relative to the relabeled graph.

---

## 193. Resonance Parameterization Equivariance

Chapter 06 may define:

`P_R: X_EQ → X_R`.

This mapping must preserve the transformation law required by:

`X_R`.

---

## 194. Invariant Resonance Parameterization

If resonance coordinates are scalar invariants:

`P_R(rho_EQ(g)x) = P_R(x)`.

---

## 195. Equivariant Resonance Parameterization

If resonance state includes vectors or tensors:

`P_R(rho_EQ(g)x) = rho_R(g) P_R(x)`.

---

## 196. Ternary Mapping from Invariants

A ternary scalar channel may be generated from invariant scalar resonance features.

Then rigid spatial transformations leave the target unchanged.

---

## 197. Ternary Mapping from Equivariant State

If a ternary mapping consumes equivariant state, it must first use a transformation-consistent decision rule.

A scalar target cannot depend arbitrarily on coordinate components without breaking invariance.

---

## 198. Invariant Norm Decision

A scalar decision may use:

`||v||`

for equivariant vector:

`v`.

The norm is invariant.

---

## 199. Invariant Dot-Product Decision

A decision may use dot products of equivariant vectors.

These remain invariant under:

`O(3)`.

---

## 200. Orientation-Sensitive Decision

A decision may depend on orientation relative to an external vector.

Then the external vector must be included in the transformed state if equivariance is to be preserved.

---

## 201. Equivariance and Learning

Learning updates model parameters.

The architecture and parameterization must preserve the declared transformation laws throughout optimization.

---

## 202. Data Augmentation

Rotational or translational data augmentation can expose transformed samples to training.

Augmentation is not a substitute for architectural equivariance by identity.

---

## 203. Equivariant Architecture

An equivariant architecture preserves the transformation law structurally for all parameter values satisfying the architecture contract.

---

## 204. Learned Approximate Equivariance

A generic architecture may learn approximate symmetry from data.

This is distinct from exact architectural equivariance.

---

## 205. Equivariance Regularization

A loss term may penalize transformation residuals.

This is developed in Volume 04.

---

## 206. Exact versus Regularized Equivariance

The distinction is:

`architectural equivariance ≠ equivariance regularization`.

---

## 207. Symmetry Validation Set

A validation set may contain transformed copies of the same configuration.

Outputs are compared under the corresponding transformation rule.

---

## 208. Random Rotation Test

A random:

`Q ∈ SO(3)`

may be sampled to test rotational equivariance.

---

## 209. Random Translation Test

A random:

`c ∈ R^3`

may test translation handling.

---

## 210. Random Reflection Test

If:

`O(3)`

is claimed, random improper orthogonal transformations may be tested.

---

## 211. Permutation Test Family

Multiple species-preserving permutations may be sampled.

Global invariant outputs and per-atom equivariant outputs must transform correctly.

---

## 212. Exact Symmetry Fixture

Synthetic configurations with known symmetry can test stabilizer behavior.

---

## 213. Degenerate Symmetry Fixture

Collinear, planar, or highly symmetric configurations can expose frame or representation degeneracies.

---

## 214. Numerical Tolerance

Numerical symmetry tests require tolerance:

`epsilon_eq`.

This tolerance belongs to validation.

It does not change the exact formal symmetry law.

---

## 215. Relative Equivariance Error

A normalized residual may be defined:

`epsilon_rel = ||y_transformed - rho(g)y|| / max(||y||, epsilon_ref)`.

The exact formula is implementation-specific.

---

## 216. Scalar Energy Error

For energy invariance:

`epsilon_E = |E(gX) - E(X)|`.

---

## 217. Force Equivariance Error

For force:

`epsilon_F = ||F(gX) - rho_F(g)F(X)||`.

---

## 218. Stress Equivariance Error

For stress:

`epsilon_Sigma = ||Sigma(gX) - Q Sigma(X) Q^T||`.

---

## 219. Symmetry Failure Classification

A validation artifact may classify:

- translation failure;
- rotation failure;
- reflection/parity failure;
- permutation failure;
- combined-action failure.

These are validation categories.

They are not ternary states.

---

## 220. INVALID Symmetry State versus Active Neutral

A symmetry-validation failure must not be encoded as ternary:

`0`.

The two state spaces remain separate.

---

## 221. Symmetry Provenance

Group-theoretic relations may carry:

`PRIMARY_SOURCE`.

TR-EIF-specific representation choices may carry:

`AUTHOR_DEFINED`.

Derived consequences may carry:

`DERIVED`.

Numerical test results may carry:

`BENCHMARK`

or:

`TEST_FIXTURE`

where applicable.

---

## 222. Primary-Source Group Structure

The definitions of:

`O(3)`

`SO(3)`

`E(3)`

`SE(3)`

and representation theory belong to established mathematical structure.

---

## 223. Author-Defined Integration

The way TR-EIF composes:

- E(3)-equivariant interatomic representation;
- resonance state;
- ternary feature channels;
- neutral-mediated execution

belongs to the framework architecture.

---

## 224. Derived Force Transformation

Force equivariance derived from invariant differentiable energy is a mathematical consequence under the stated assumptions.

---

## 225. Benchmark Symmetry Result

Measured numerical equivariance residuals belong to benchmark or validation artifacts.

---

## 226. Test Fixture Transformation

Controlled rotations, reflections, translations, and permutations used for unit tests carry:

`TEST_FIXTURE`

provenance.

---

## 227. E(3) Extension Rule

Any extension using spatial symmetry must define:

1. symmetry group;
2. input action;
3. output action;
4. scalar/vector/tensor/parity types;
5. external symmetry-breaking state;
6. periodic treatment;
7. validation method;
8. numerical tolerance.

---

## 228. Feature Extension Rule

Any new feature type must define:

1. feature space;
2. transformation law;
3. permutation behavior;
4. parity where applicable;
5. units where physical;
6. allowed operations;
7. serialization.

---

## 229. Output Extension Rule

Any new physical output must define:

1. scalar/vector/tensor type;
2. transformation law;
3. units;
4. permutation behavior;
5. derivation or prediction mapping;
6. validation.

---

## 230. External-Field Extension Rule

Any external field must define:

1. field type;
2. spatial transformation;
3. coordinate-frame convention;
4. whether the field transforms with the atomic system;
5. resulting residual symmetry group.

---

## 231. Periodic Symmetry Extension Rule

Any periodic realization must define:

1. cell transformation;
2. fractional-coordinate behavior;
3. image-shift behavior;
4. rigid rotation handling;
5. cell deformation boundary.

---

## 232. Canonical Group Invariants

Every conforming E(3) layer preserves:

1. explicit symmetry group;

2. explicit action on positions;

3. explicit action on features;

4. explicit atom-permutation behavior;

5. explicit parity where reflections are supported;

6. explicit periodic handling;

7. explicit symmetry-breaking inputs.

---

## 233. Canonical Geometric Invariants

Under rigid Euclidean transformation:

`r_ij → Q r_ij`

`d_ij → d_ij`

`u · v → u · v`.

Translations cancel from relative geometry.

---

## 234. Canonical Output Invariants

The layer preserves:

- scalar energy invariance;
- force vector equivariance;
- stress tensor equivariance;
- permutation invariance of global scalar outputs;
- permutation equivariance of per-atom outputs.

---

## 235. Canonical Representation Invariants

The framework preserves:

`equivariance ≠ invariance`

`scalar ≠ vector`

`polar vector ≠ axial vector`

`scalar ≠ pseudoscalar`

`physical rotation ≠ atom permutation`

`rotation ≠ deformation`.

---

## 236. Canonical TR Integration Invariants

The symmetry layer preserves:

`geometry ≠ resonance`

`resonance ≠ ternary state`

`spatial rotation ≠ ternary polarity reversal`

`active neutral ≠ geometric zero`

`target ≠ executed state`.

---

## 237. Canonical Scientific Distinctions

The framework preserves:

`oscillator phase ≠ geometric orientation`

`oscillator phase ≠ physical phase of matter`

`phase relation ≠ chemical bond`

`phase coupling ≠ mechanical force`

`interaction edge ≠ chemical bond`

`equivariant force ≠ conservative force`

`physical energy ≠ representation norm`

`graph topology change ≠ symmetry transformation`

`ternary state ≠ energy`.

---

## 238. Canonical E(3) Chain

The canonical symmetry chain is:

`atomic coordinates`

`→ E(3) action`

`→ relative geometry`

`→ invariant/equivariant feature types`

`→ equivariant representation`

`→ equivariant message passing`

`→ invariant energy`

`→ equivariant force/stress`.

---

## 239. Canonical TR-EIF Integration Chain

The integrated forward path is:

`X_conf`

`→ X_G`

`→ X_EQ`

`→ X_R`

`→ T_target`

`→ T_exec`.

Spatial symmetry is preserved through:

`X_conf`

`X_G`

`X_EQ`

and every later mapping according to its declared output type.

---

## 240. Interface to Chapter 04

Chapter 04 develops Equivariant Representations.

It uses the group actions defined here to construct:

- scalar channels;
- vector channels;
- higher-order channels;
- irreducible representation blocks;
- parity-aware features;
- invariant contractions;
- equivariant tensor products.

---

## 241. Interface to Chapter 05

Chapter 05 develops Message Passing.

Messages and aggregation must preserve both:

- atom-permutation semantics;
- E(3) transformation semantics.

---

## 242. Interface to Chapter 06

Chapter 06 develops Resonance Parameterization.

Resonance coordinates inherit explicit invariant or equivariant transformation laws from the representations defined in Chapters 03 and 04.

---

## 243. Interface to Chapter 07

Chapter 07 develops Ternary Feature Channels.

Ternary scalar channels derived from geometric state must use invariant decision variables unless a nontrivial transformation law is explicitly defined.

---

## 244. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

The energy output must satisfy the declared scalar invariance.

---

## 245. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

Force and stress outputs must satisfy the vector and tensor transformation laws defined here.

---

## 246. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each model family member must declare:

- symmetry group;
- representation types;
- parity support;
- periodic treatment;
- output transformation contract.

---

## 247. Final Formal Structure

The E(3) symmetry layer may be represented as:

`SG = (G_space, G_perm, rho_conf, rho_graph, rho_EQ, rho_R, rho_out)`.

Here:

- `G_space` is `E(3)`, `SE(3)`, `O(3)`, `SO(3)`, or a declared subgroup;
- `G_perm` is the applicable atom-permutation group;
- `rho_conf` acts on atomic configuration;
- `rho_graph` acts on graph state;
- `rho_EQ` acts on equivariant representation;
- `rho_R` acts on resonance state;
- `rho_out` acts on physical outputs.

A conforming mapping satisfies its declared equivariance relation:

`F(rho_in(g)x) = rho_out(g)F(x)`.

---

## 248. Final Statement

The E(3) group-action layer defines the geometric symmetry structure of the Equivariant Interatomic Framework.

Atomic coordinates transform under rigid Euclidean transformations:

`r_i' = Q r_i + c`.

Relative vectors transform as:

`r_ij' = Q r_ij`.

Distances remain invariant.

Scalar, vector, tensor, pseudoscalar, polar-vector, axial-vector, and parity-aware representation types retain distinct transformation laws.

Atom permutations form a separate symmetry acting on indexing rather than physical spatial orientation.

The framework preserves:

`equivariance ≠ invariance`

`rotation ≠ permutation`

`rotation ≠ deformation`

`spatial rotation ≠ ternary polarity reversal`

`oscillator phase ≠ geometric orientation`

`equivariant force ≠ conservative force`.

Energy may terminate in an invariant scalar representation.

Forces must transform equivariantly.

Stress must transform as a tensor.

Resonance and ternary channels inherit explicitly defined transformation behavior from the equivariant interatomic representation.

These definitions establish the symmetry contract required for the Equivariant Representations developed in Chapter 04.
