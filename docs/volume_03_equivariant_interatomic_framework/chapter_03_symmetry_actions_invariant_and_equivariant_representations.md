# Symmetry Actions, Invariant and Equivariant Representations

## 1. Purpose

This document formalizes the symmetry-action and representation layer of the Equivariant Interatomic Framework.

The chapter continues the source-side chain established in Chapters 01–02:

`interatomic configuration`

`→ geometry`

`→ topology`

`→ local atomic environment`

and defines the next transformation:

`local / global environment`

`→ invariant and equivariant representation`

The chapter establishes:

- transformation groups and transformation sets;
- actions on configurations, topology, environments, and representation spaces;
- permutation actions;
- translation actions;
- proper-rotation actions;
- reflection and parity semantics;
- `SO(3)`, `O(3)`, `SE(3)`, and `E(3)` boundaries;
- invariant mappings;
- equivariant mappings;
- scalar, vector, and higher-order geometric channels;
- representation types;
- irreducible rotational channels;
- parity;
- spherical-harmonic geometric channels;
- tensor-product coupling;
- equivariant composition;
- invariant contraction;
- local and global representation semantics;
- information preservation and information loss;
- exact and numerical equivariance validation;
- transformation-aware output interfaces;
- the boundary between EIF representations and later physical or TR-EIF integration mappings.

This chapter does not define a universal neural-network architecture.

It defines mathematical transformation requirements that any EIF realization must satisfy when it claims invariance or equivariance.

## 2. Dependency

This chapter depends on:

- Volume 01, Mathematical Foundations;
- Volume 02, Ternary Resonance Theory;
- Volume 03, Chapter 01, Equivariant Interatomic Foundations;
- Volume 03, Chapter 02, Interatomic State Spaces, Geometry, and Local Environments.

It inherits without redefinition:

- atomic-site set `V_N`;
- atomic identity domain `Z`;
- configuration spaces `Q_N` and `Q_N,adm`;
- variable-cardinality configuration domain `Q_var`;
- position state;
- boundary-condition state;
- periodic-cell state where applicable;
- topology state space `X_G`;
- local-environment space `X_env`;
- local-environment mappings `E_i`;
- relative displacement `r_ij`;
- distance `d_ij`;
- topology construction semantics;
- permutation semantics;
- information-loss requirements;
- provenance classes;
- TR-EIF separation rules.

## 3. Scientific Status Classes

### 3.1 CLASSICAL

The following are classical mathematical or established representation-theoretic structures:

- groups and group actions;
- orthogonal groups;
- proper-rotation groups;
- Euclidean groups;
- permutation groups;
- invariant mappings;
- equivariant mappings;
- linear representations;
- irreducible representations;
- spherical harmonics;
- tensor products;
- Clebsch–Gordan coupling;
- scalar, vector, and higher-order transformation channels.

### 3.2 EIF FORMAL / AUTHOR-DEFINED

The following are author-defined EIF architecture:

- the exact hierarchy of EIF representation spaces;
- the representation contracts;
- transformation-compatibility requirements between EIF layers;
- information-preservation requirements;
- representation provenance rules;
- cross-layer conformance requirements;
- the explicit boundary between EIF representations and TR-EIF integration.

### 3.3 DERIVED

Consequences obtained directly from declared group actions and mappings are classified as:

`DERIVED`

### 3.4 OPERATIONAL / EXECUTABLE REFERENCE

Tensor Field Networks, NequIP, e3nn, Allegro, and related architectures are implementation precedents.

They do not define the complete EIF theory.

### 3.5 EMPIRICAL / CALIBRATED

Numerical architecture parameters, trained coefficients, learned radial functions, basis truncations, and dataset-dependent accuracy belong to empirical, calibrated, benchmark, or implementation-specific layers according to their provenance.

### 3.6 UNVERIFIED

Symmetry compliance does not establish physical correctness automatically.

Any physical interpretation not independently defined remains unverified.

## 4. Representation-Layer Position

The EIF source chain now becomes:

`q ∈ Q_N,adm`

`→ G ∈ X_G`

`→ e_i ∈ X_env`

`→ h_i ∈ Y_EIF,local`

where:

`h_i = Φ_i(e_i)`

and:

`Φ_i: X_env → Y_EIF,local`

is a declared local representation mapping.

The representation `h_i` is not the source environment itself.

Therefore:

`e_i ≠ h_i`

in general.

## 5. Transformation Must Be Declared Before Equivariance

A mapping cannot be called invariant or equivariant without a declared transformation domain.

Every such claim must identify:

- transformation group or transformation set;
- source space;
- target space;
- source action;
- target action;
- mapping being tested;
- scope over which the relation holds.

The word:

`equivariant`

is not a semantic substitute for those objects.

## 6. Symmetry Group

Let:

`G_sym`

denote a declared symmetry group.

Its elements are:

`g ∈ G_sym`

with identity:

`e_G ∈ G_sym`

Every group element has an inverse:

`g⁻¹ ∈ G_sym`

and composition remains inside `G_sym`.

## 7. Group Action

Let `X` be a state or representation space.

A left action of `G_sym` on `X` is:

`ρ_X: G_sym × X → X`

with:

`ρ_X(e_G, x) = x`

and:

`ρ_X(g_1 g_2, x) = ρ_X(g_1, ρ_X(g_2, x))`

for every admissible:

`g_1, g_2 ∈ G_sym`

and:

`x ∈ X`

## 8. Action Notation

For compactness, write:

`ρ_X(g)x`

for:

`ρ_X(g, x)`

The action remains a mapping with an explicitly declared domain and codomain.

## 9. Representation of a Group

When `X` is a vector space and every:

`ρ_X(g): X → X`

is linear, the action defines a linear representation of `G_sym` on `X`.

Not every EIF state space must be linear.

Configuration spaces and structured environment spaces may carry nonlinear group actions.

## 10. Configuration Action

Let:

`ρ_Q: G_sym × Q_N,adm → Q_N,adm`

be a declared action on admissible configurations.

The action must preserve all configuration components according to their respective transformation laws.

## 11. Environment Action

Let:

`ρ_env: G_sym × X_env → X_env`

be the declared action on local environments.

The action must preserve:

- central-site correspondence;
- neighbor correspondence;
- atomic identities;
- topology correspondence;
- geometric transformation behavior.

## 12. Representation Action

Let:

`Y_rep`

be a representation space.

Define:

`ρ_rep: G_sym × Y_rep → Y_rep`

The action determines how representation values transform.

The action must be specified before calling a representation channel invariant or equivariant.

## 13. Invariant Mapping

Let:

`F: X → Y`

and let `G_sym` act on `X`.

The mapping `F` is invariant under the declared action when:

`F(ρ_X(g)x) = F(x)`

for every admissible:

`g ∈ G_sym`

and:

`x ∈ X`

The output action is effectively the identity action on `Y`.

## 14. Equivariant Mapping

Let:

`F: X → Y`

with declared actions:

`ρ_X`

and:

`ρ_Y`

The mapping is equivariant when:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for every admissible:

`g ∈ G_sym`

and:

`x ∈ X`

## 15. Invariance Is a Special Equivariance Case

If:

`ρ_Y(g)y = y`

for every admissible `g` and `y`, then equivariance reduces to invariance.

This does not make the terms interchangeable.

The output transformation semantics remain different.

## 16. Invariance and Equivariance Remain Distinct

The framework preserves:

`invariance ≠ equivariance`

An invariant scalar can remain unchanged under a rotation.

An equivariant vector generally rotates.

Both can be valid outputs of the same model.

## 17. Transformation Scope

A symmetry statement is always scoped.

A mapping may be:

- translation invariant;
- rotation equivariant;
- permutation equivariant;
- reflection invariant;
- invariant under one subgroup but not another.

The statement:

`F is equivariant`

is incomplete without the transformation scope.

## 18. Permutation Group

For fixed cardinality `N`, let:

`S_N`

denote the permutation group acting on site indices.

For:

`π ∈ S_N`

the action must consistently reindex every site-associated object.

## 19. Permutation Action on Configuration

A consistent permutation action may be represented by:

`z_i' = z_(π⁻¹(i))`

and:

`x_i' = x_(π⁻¹(i))`

The inverse convention produces a left action.

Atomic identity remains paired with the corresponding atomic position.

## 20. Permutation Action on Local Features

For a site-indexed feature collection:

`H = (h_1, ..., h_N)`

the permutation action is:

`h_i' = h_(π⁻¹(i))`

when no additional internal transformation is associated with reindexing.

## 21. Permutation Equivariance

A site-indexed mapping:

`F: Q_N,adm → Y^N`

is permutation equivariant when:

`F(π · q) = π · F(q)`

for every admissible:

`π ∈ S_N`

and:

`q ∈ Q_N,adm`

## 22. Permutation Invariance

A global mapping:

`F_global: Q_N,adm → Y_global`

is permutation invariant when:

`F_global(π · q) = F_global(q)`

for every admissible site permutation.

## 23. Permutation Invariance Is Not Species Erasure

The permutation operation changes computational indexing.

It does not erase species identity.

Therefore:

`permutation invariance ≠ species invariance`

unless a separate species transformation is explicitly defined.

## 24. Permutation Equivariance and Invariance Are Different

For local outputs:

`permutation equivariance`

is usually the relevant relation.

For one global scalar output:

`permutation invariance`

may be relevant.

Therefore:

`permutation invariance ≠ permutation equivariance`

## 25. Translation Group

For Euclidean translations in `d` dimensions, let:

`a ∈ ℝ^d`

The translation action on positions is:

`x_i' = x_i + a`

for all represented sites.

## 26. Translation of Relative Geometry

For:

`r_ij = x_j - x_i`

a common global translation gives:

`r_ij' = r_ij`

Thus relative displacement removes common global translation from that relational coordinate.

## 27. Translation-Invariant Local Geometry

A local environment represented entirely through relative geometry may be translation invariant with respect to its geometric channels.

This does not establish:

- rotation invariance;
- rotation equivariance;
- permutation invariance;
- permutation equivariance.

Each property remains separate.

## 28. Orthogonal Group

In three dimensions:

`O(3)`

is the group of real `3 × 3` matrices `R` satisfying:

`R^T R = I`

with:

`det(R) ∈ {-1, 1}`

It includes proper and improper orthogonal transformations.

## 29. Proper-Rotation Group

The proper-rotation group is:

`SO(3) = {R ∈ O(3) : det(R) = 1}`

It contains orientation-preserving rotations only.

## 30. Reflection Boundary

Elements of:

`O(3) \ SO(3)`

have determinant:

`-1`

and reverse orientation.

Reflection-sensitive information therefore requires transformation semantics beyond proper-rotation behavior alone.

## 31. Euclidean Group

In three dimensions, an Euclidean transformation acts as:

`x → R x + a`

with:

`R ∈ O(3)`

and:

`a ∈ ℝ^3`

The corresponding group is:

`E(3)`

## 32. Special Euclidean Group

Restricting the orthogonal component to:

`R ∈ SO(3)`

gives:

`SE(3)`

which contains proper rotations and translations.

## 33. E(3) and SE(3) Remain Distinct

Because reflections belong to `E(3)` but not `SE(3)`:

`SE(3)-equivariance ≠ E(3)-equivariance`

Passing proper-rotation tests does not establish reflection behavior.

## 34. Rotation Action on Position

For:

`R ∈ SO(3)`

a position transforms as:

`x_i' = R x_i`

when the chosen origin convention is fixed.

A relative vector transforms as:

`r_ij' = R r_ij`

## 35. Rotation Action on Distance

Because orthogonal transformations preserve Euclidean norm:

`||R r_ij|| = ||r_ij||`

Therefore:

`d_ij' = d_ij`

Distance is rotationally invariant.

## 36. Geometry Contains Multiple Representation Types

A local atomic environment may simultaneously contain:

- invariant scalar distances;
- equivariant displacement vectors;
- orientation-sensitive higher-order quantities.

The complete environment cannot therefore be assigned one transformation type without specifying its components.

## 37. Scalar Channel

Let:

`s ∈ ℝ`

be a geometric scalar channel.

Under the trivial rotational action:

`s' = s`

Such a scalar is rotationally invariant.

## 38. Vector Channel

Let:

`v ∈ ℝ^3`

be a polar vector channel.

Under proper rotation:

`v' = R v`

This is the standard vector-equivariance relation.

## 39. Tensor Channel

Let:

`T`

belong to a declared tensor space.

Its transformation law depends on tensor type and rank.

For a second-order Cartesian tensor under the standard action:

`T' = R T R^T`

when that is the declared physical or mathematical transformation rule.

## 40. Tensor Rank Does Not Fully Determine Representation Type

Two objects with the same array shape may transform differently.

Examples include:

- polar vectors;
- axial vectors;
- ordinary tensors;
- pseudotensors.

Therefore:

`array shape ≠ transformation semantics`

## 41. Polar and Axial Vector Boundary

Under proper rotations, polar and axial vectors transform identically.

Under improper transformations, their parity behavior differs.

Therefore:

`SO(3) behavior alone`

does not fully distinguish all `O(3)` representation types.

## 42. Parity

For reflection-aware `O(3)` representation channels, introduce a parity label:

`p ∈ {-1, 1}`

The label describes the behavior associated with improper transformations according to the selected representation convention.

This `p` is not a ternary state.

## 43. Parity Is Not Ternary Polarity

The parity set:

`{-1, 1}`

belongs to representation transformation semantics.

The balanced ternary state set:

`T = {-1, 0, 1}`

belongs to the separate TR execution layer.

Therefore:

`representation parity ≠ ternary state`

## 44. Geometry Does Not Flip Ternary State

A reflection may alter a parity-sensitive EIF representation.

It does not automatically change a later TR state from:

`-1 → 1`

or:

`1 → -1`

No geometric action is permitted to define ternary transition semantics implicitly.

## 45. Irreducible Representation

A linear representation is irreducible when its representation space has no nontrivial proper invariant subspace under all group actions.

Irreducible representations provide elementary transformation channels from which more complex equivariant representations can be constructed.

## 46. SO(3) Irreducible Channels

Finite-dimensional irreducible representations of `SO(3)` relevant to ordinary equivariant atomistic constructions are indexed by a nonnegative integer:

`l ∈ {0, 1, 2, ...}`

The corresponding representation dimension is:

`2l + 1`

## 47. Scalar Irreducible Channel

For:

`l = 0`

the representation dimension is:

`1`

This is the scalar rotational channel.

## 48. Vector-Like Rotational Channel

For:

`l = 1`

the representation dimension is:

`3`

This rotational representation corresponds to the ordinary three-dimensional vector transformation type under `SO(3)`.

## 49. Higher-Order Irreducible Channels

For:

`l ≥ 2`

the channels carry higher-order angular transformation information.

They are not reducible to scalar magnitude alone without information loss.

## 50. Irreducible Channel Is Not Physical Tensor Identity

An `l`-channel specifies transformation behavior.

It does not automatically identify a physical observable.

Therefore:

`l = 1 channel ≠ physical force automatically`

and:

`l = 2 channel ≠ physical stress automatically`

Physical meaning requires an independent output definition.

## 51. O(3) Representation Label

When reflection parity is represented explicitly, a channel may be labeled by:

`(l, p)`

where:

`l`

defines rotational degree and:

`p ∈ {-1, 1}`

defines parity according to the selected convention.

## 52. Feature Multiplicity

A representation may contain multiple channels of the same transformation type.

Let:

`m_(l,p) ≥ 0`

denote the multiplicity of representation type `(l,p)`.

Multiplicity is an architecture dimension.

It is not a universal physical constant.

## 53. Structured Representation Space

A finite EIF representation may be decomposed conceptually as a direct collection of typed channels:

`Y_rep = ⊕_(l,p) Y_(l,p)`

where each component carries a declared transformation action.

The selected set of `(l,p)` channels is specialization-dependent.

## 54. Representation Truncation

An implementation may restrict:

`l ≤ l_max`

for a finite:

`l_max`

This is an implementation or model-design choice.

EIF defines no universal:

`l_max`

## 55. Truncation Implies Representation Restriction

If higher `l` channels are omitted, transformation information expressible only through those channels may not be represented directly.

The consequences depend on the complete architecture.

Therefore:

`finite l_max ≠ universal representational completeness`

## 56. Spherical Direction

For nonzero relative displacement:

`r_ij ≠ 0`

define the unit direction:

`u_ij = r_ij / ||r_ij||`

with:

`u_ij ∈ S^2`

in three dimensions.

The direction is undefined when:

`r_ij = 0`

## 57. Radial and Angular Separation

A relative displacement can be decomposed conceptually into:

- radius `d_ij`;
- direction `u_ij`.

The radial scalar is rotationally invariant.

The direction transforms under rotation.

## 58. Spherical Harmonics

Spherical harmonics provide a classical angular basis on the sphere.

For each:

`l ≥ 0`

there are:

`2l + 1`

angular basis components associated with:

`m = -l, ..., l`

The basis transforms within the same `l` subspace under rotations.

## 59. Spherical-Harmonic Channel

Let:

`Y_l(u)`

denote the vector of spherical-harmonic components of degree `l` evaluated at direction `u`.

Under rotation `R`, there exists a representation matrix:

`D^(l)(R)`

such that the transformed channel obeys the corresponding degree-`l` rotation law.

The exact numerical convention for real or complex spherical harmonics must be declared by the implementation.

## 60. Basis Convention

A spherical-harmonic implementation must identify:

- real or complex basis;
- normalization;
- component ordering;
- phase convention where relevant;
- parity convention.

Different conventions may encode equivalent mathematics with different numerical arrays.

## 61. Basis Convention Is Not Physical Difference

Two implementations using different but consistently related basis conventions may represent the same underlying transformation structure.

Therefore:

`different basis coordinates ≠ different physical state automatically`

## 62. Radial Function

Let:

`R_n: ℝ_≥0 → ℝ`

be a declared radial basis or radial feature function indexed by `n`.

Radial functions act on distance or another declared radial coordinate.

They are scalar under rotation when their input is rotationally invariant distance.

## 63. Radial Parameters

Any:

- radial cutoff;
- basis width;
- basis center;
- number of radial channels;
- learned radial coefficient;

is model-specific unless independently established otherwise.

EIF defines none of these as universal constants.

## 64. Geometric Edge Feature

A transformation-aware edge representation may combine:

- atomic identities;
- radial scalar features;
- angular equivariant features;
- additional declared edge state.

Its transformation behavior follows from the transformation types of its components.

## 65. Tensor Product

Let:

`V_a`

and:

`V_b`

be representation spaces carrying group actions.

Their tensor product:

`V_a ⊗ V_b`

carries an induced representation.

Tensor products therefore provide a mechanism for combining transformation-aware features without discarding their group structure.

## 66. Tensor Product Is Not Ordinary Concatenation

Concatenation places feature arrays beside one another.

A tensor product forms multiplicative combinations with a defined transformation law.

Therefore:

`tensor product ≠ concatenation`

## 67. Clebsch–Gordan Coupling

For `SO(3)` irreducible representations with degrees:

`l_1`

and:

`l_2`

their tensor product decomposes into irreducible channels with degrees:

`l`

satisfying:

`|l_1 - l_2| ≤ l ≤ l_1 + l_2`

with integer steps.

This is a classical angular-momentum coupling structure used by many equivariant architectures.

## 68. Coupling Selection Rule

A requested output degree outside:

`|l_1 - l_2| ≤ l ≤ l_1 + l_2`

does not occur in the corresponding irreducible tensor-product decomposition.

This is a representation-theoretic constraint, not a learned empirical rule.

## 69. Parity Under Product

When parity is explicitly represented, the parity of a tensor-product channel follows the declared product representation.

For multiplicative parity labels under the standard convention:

`p_out = p_1 p_2`

The convention must remain consistent throughout the implementation.

## 70. Equivariant Linear Map

A linear map:

`L: X → Y`

between representation spaces is equivariant when:

`L ρ_X(g) = ρ_Y(g) L`

for every:

`g ∈ G_sym`

This is the intertwining relation.

## 71. Intertwiner

An equivariant linear map between representation spaces is also called an intertwiner.

The existence and structure of such maps depend on the representation types of the source and target spaces.

## 72. Arbitrary Mixing Can Break Equivariance

An arbitrary linear transformation mixing incompatible representation types need not be equivariant.

Feature mixing must respect transformation structure.

Therefore:

`linear layer ≠ equivariant layer automatically`

## 73. Same-Type Channel Mixing

Multiple channels carrying the same representation type can be mixed through operations that act on multiplicity indices while preserving the geometric representation action.

The precise implementation must preserve the corresponding intertwining relation.

## 74. Scalar Nonlinearity

A pointwise nonlinear function applied to an invariant scalar remains invariant when its input is invariant and the function depends only on that scalar.

This simple result does not generalize automatically to arbitrary componentwise nonlinearities on non-scalar equivariant channels.

## 75. Nonlinearity Boundary

Applying an arbitrary nonlinear function independently to Cartesian vector components generally does not preserve rotational equivariance.

Equivariant nonlinearities therefore require transformation-compatible constructions.

## 76. Gating

One transformation-compatible construction multiplies a non-scalar equivariant channel by an invariant scalar gate.

If:

`a`

is invariant and:

`v`

transforms equivariantly, then:

`a v`

transforms with the same representation type as `v`.

## 77. Norm-Based Scalar

For a vector transforming orthogonally, its Euclidean norm is invariant:

`||R v|| = ||v||`

An invariant scalar derived from a norm can therefore participate in transformation-compatible gating or other scalar operations.

## 78. Norm Loses Direction

Mapping:

`v → ||v||`

is many-to-one.

It discards directional information.

Therefore:

`vector norm ≠ vector representation`

and:

`invariant contraction may lose equivariant information`

## 79. Invariant Contraction

An equivariant representation may be contracted into invariant scalars through a declared invariant operation.

The contraction changes the representation type.

It may also reduce information.

## 80. Dot Product

For vectors transformed by the same orthogonal matrix:

`(R a) · (R b) = a · b`

Thus the dot product is rotationally invariant.

It does not preserve the original vector directions.

## 81. Cross Product Boundary

In three dimensions, the cross product of two polar vectors transforms as an axial vector under improper transformations.

Therefore its full `O(3)` transformation semantics differ from those of an ordinary polar vector.

## 82. Reflection Awareness Is Necessary for Chirality

A representation that removes all reflection-sensitive information cannot distinguish configurations differing only by reflection when the remaining representation is reflection invariant.

Such a representation may therefore be insufficient for chirality-sensitive claims.

## 83. SO(3)-Invariant and O(3)-Invariant Representations Differ

An `SO(3)`-invariant representation may retain information that changes under reflection.

An `O(3)`-invariant representation identifies both proper rotations and reflections according to its transformation contract.

Therefore:

`SO(3)-invariant ≠ O(3)-invariant`

## 84. Translation Handling by Relative Geometry

If all geometric representation channels depend only on boundary-consistent relative displacements, common translation dependence can be removed before rotational processing.

This is one construction strategy.

It is not the only mathematically possible strategy.

## 85. E(3) Equivariance by Structured Composition

An E(3)-equivariant atomistic mapping may be constructed through a composition that:

- treats translation through relative geometry;
- treats rotation and reflection through `O(3)` representations;
- treats atom indexing through permutation-consistent operations.

Each component must satisfy its declared transformation relation.

## 86. Combined Transformation Claims

A claim that a mapping is:

`E(3)-equivariant and permutation equivariant`

contains more information than a rotational-equivariance claim alone.

Every transformation component must be validated.

## 87. Independent Transformation Actions

Permutation and Euclidean transformation act on different aspects of the atomic state.

A consistent model must define both.

It must not assume that satisfying one implies the other.

## 88. Commuting Actions

For standard global Euclidean transformations and consistent atom reindexing, the two actions may commute on ordinary indexed configuration data.

If a model relies on this property, the selected state and auxiliary data must preserve it.

It must not be assumed for arbitrary extended state.

## 89. Topology Under Rigid Transformation

A topology constructed exclusively from rigid-motion invariant criteria such as species identity and pair distance can remain correspondingly unchanged under rigid Euclidean transformations, provided numerical boundary decisions are consistent.

This is a property of the topology constructor, not of graph notation alone.

## 90. Topology Under Permutation

Under site permutation, graph connectivity must be reindexed consistently.

For an edge:

`(i, j)`

the corresponding permuted edge follows the declared index action.

Graph storage order is not physical state.

## 91. Environment-to-Representation Mapping

For local environment:

`e_i ∈ X_env`

define:

`Φ_local: X_env → Y_EIF,local`

The representation is:

`h_i = Φ_local(e_i)`

The mapping must define its transformation relation.

## 92. Local Representation Equivariance

If `G_sym` acts on environments and local representations, local equivariance requires:

`Φ_local(ρ_env(g)e_i) = ρ_local(g)Φ_local(e_i)`

for every admissible transformation and environment.

## 93. Local Representation Invariance

If the local representation is intentionally invariant:

`Φ_local(ρ_env(g)e_i) = Φ_local(e_i)`

for all transformations in the declared invariance group.

This may be appropriate for some outputs but loses transformation-sensitive information by construction.

## 94. Mixed Representation

A local EIF representation may contain both invariant and equivariant channels.

For example, its structured state may include:

- `l = 0` scalar channels;
- `l = 1` vector-like channels;
- higher-order `l` channels;
- parity-distinguished channels when using `O(3)` semantics.

The representation must retain channel type metadata.

## 95. Type Metadata

A machine-readable equivariant feature must preserve enough metadata to identify:

- transformation group;
- representation degree;
- parity where relevant;
- multiplicity;
- component convention;
- scale;
- central-site identity where local.

An untyped numeric array is insufficient as a complete mathematical representation contract.

## 96. Local Representation Collection

For all sites:

`H_local = (h_1, ..., h_N)`

The collection remains site-indexed.

Under atomic permutation, the site association must transform correspondingly.

## 97. Global Representation

Let:

`Y_EIF,global`

be a declared global representation space.

A global mapping may be:

`Φ_global: Q_N,adm → Y_EIF,global`

or may be constructed from the local representation collection through a declared aggregation mapping.

## 98. Global Invariant Readout

A global invariant readout:

`A_inv: Y_EIF,local^N → Y_inv`

must satisfy the appropriate permutation and geometric invariance relations.

A sum of scalar local invariant contributions is one possible construction.

It is not a universal requirement of EIF.

## 99. Global Equivariant Readout

A global output may instead transform nontrivially.

For example, a vector-valued global output requires a corresponding output action.

The output type determines the required transformation relation.

## 100. Pooling Boundary

Pooling may reduce:

- site identity;
- spatial locality;
- orientation information;
- higher-order channel information.

The information loss depends on the pooling operation.

Therefore:

`global pooling ≠ lossless representation automatically`

## 101. Sum Pooling

For site-indexed scalar values:

`s_i`

the sum:

`S = Σ_i s_i`

is invariant to reordering of the site index.

Permutation invariance of the sum does not establish rotational invariance unless the `s_i` themselves have the required rotational semantics.

## 102. Mean Pooling

Mean pooling is also permutation invariant over a fixed nonzero site set.

It changes cardinality scaling relative to sum pooling.

Therefore:

`sum pooling ≠ mean pooling`

and their physical interpretation must not be interchanged.

## 103. Extensive and Intensive Boundary

If a physical output is later intended to be extensive, sum-like aggregation may have relevant scaling properties.

If it is intended to be intensive, another normalization may be required.

The physical semantics must be defined independently.

EIF does not impose a universal aggregation rule.

## 104. Multiscale Representation

Let:

`L_EIF`

be a declared finite scale set.

For each:

`ell ∈ L_EIF`

define:

`Y_EIF,ell`

The multiscale representation space is:

`Y_EIF,MS = ∏_(ell ∈ L_EIF) Y_EIF,ell`

Scale identity remains explicit.

## 105. Symmetry Across Scales

Every scale-specific representation must define its transformation action.

A global invariant channel does not establish equivariance of local channels.

Likewise, equivariance at one scale does not automatically establish compatibility across all scales.

## 106. Cross-Scale Mapping

Let:

`A_(ell→m): Y_EIF,ell → Y_EIF,m`

be a declared cross-scale mapping.

If equivariance is claimed, the mapping must satisfy the corresponding intertwining relation between the source and target scale actions.

## 107. Hierarchy Is Not Equivariance

A hierarchical representation may organize information across scales.

That organization does not by itself imply any symmetry property.

Therefore:

`hierarchy ≠ equivariance`

## 108. Message Passing Boundary

A message-passing operation may be equivariant if its message construction, aggregation, and update operations satisfy the required transformation relations.

Message passing itself does not guarantee equivariance.

Therefore:

`message passing ≠ equivariance`

## 109. Strict Locality Boundary

A strictly local equivariant model can operate without multi-hop message propagation.

Allegro provides an established computational example of this design class.

Therefore:

`equivariant representation ≠ message-passing representation`

## 110. Graph Neural Network Boundary

A graph neural network may operate only on invariant scalar edge geometry or may maintain higher-order equivariant features.

The category:

`graph neural network`

does not determine transformation behavior.

## 111. Neural-Network Boundary

Equivariance is a property of a mapping.

The mapping may be:

- analytic;
- learned;
- neural;
- kernel-based;
- hybrid;
- algorithmic.

Therefore:

`equivariance ≠ neural network`

## 112. Learned Weight Boundary

Learned scalar coefficients do not automatically break equivariance when they operate only on channels in a transformation-compatible manner.

Learned arbitrary mixing across incompatible representation types can break equivariance.

The architectural contract determines the result.

## 113. Radial Learning

A learned radial function of invariant distance can remain rotationally invariant as a scalar channel.

Learning the function does not change the transformation type of its scalar input.

## 114. Angular Learning

Learned operations involving angular channels must preserve their declared representation transformations.

Data augmentation alone does not make an arbitrary mapping exactly equivariant.

## 115. Data Augmentation and Equivariance Are Different

Training on rotated examples may improve approximate rotational behavior.

It does not mathematically impose exact equivariance.

Therefore:

`rotation augmentation ≠ exact rotational equivariance`

## 116. Architectural Equivariance

An architecture built entirely from compatible equivariant operations can satisfy the transformation relation by construction at the mathematical level.

Its finite-precision implementation may still require numerical verification.

## 117. Exact and Numerical Equivariance

The exact relation is:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

A numerical implementation may instead satisfy:

`d_Y(F(ρ_X(g)x), ρ_Y(g)F(x)) ≤ epsilon_eq`

where:

- `d_Y` is a declared distance or error measure on the output representation;
- `epsilon_eq ≥ 0` is a numerical tolerance.

## 118. Numerical Tolerance Is Not Exact Symmetry

The framework preserves:

`exact equivariance ≠ equivariance within numerical tolerance`

The tolerance belongs to numerical validation.

It does not modify the mathematical definition.

## 119. Equivariance Residual

Define:

`e_eq(x, g) = d_Y(F(ρ_X(g)x), ρ_Y(g)F(x))`

The residual is meaningful only after:

- `d_Y`;
- `F`;
- `ρ_X`;
- `ρ_Y`;
- `x`;
- `g`;

have been defined.

## 120. Relative and Absolute Error

An implementation may use absolute or relative error metrics.

Relative error requires a denominator convention and explicit handling near zero.

No universal numerical equivariance metric is imposed by EIF.

## 121. Transformation Sampling

A numerical test over finitely many transformations verifies only the sampled test set unless a stronger analytical result applies.

Therefore:

`sampled equivariance PASS ≠ proof over the complete group`

## 122. Analytical Equivariance

If each component of a composition is mathematically equivariant under compatible actions, the composition is equivariant.

This can establish the exact property independently of finite transformation sampling, subject to the validity of the component assumptions.

## 123. Equivariant Composition

Let:

`F: X → Y`

and:

`G: Y → Z`

be equivariant under compatible group actions.

Then:

`G ∘ F: X → Z`

is equivariant because:

`G(F(ρ_X(g)x))`

equals:

`G(ρ_Y(g)F(x))`

which equals:

`ρ_Z(g)G(F(x))`

for every admissible `g` and `x`.

## 124. Compatibility of Intermediate Action

The composition result requires the output action of `F` on `Y` to match the input action expected by `G`.

Typed-space compatibility alone is not enough if the transformation semantics differ.

## 125. Equivariant Residual Layer

If a model adds two features:

`a`

and:

`b`

they must belong to compatible representation spaces under the declared action.

Adding incompatible transformation types is not a valid equivariant operation.

## 126. Addition of Same-Type Channels

If:

`a`

and:

`b`

transform under the same linear representation:

`ρ`

then:

`a + b`

transforms under the same representation.

This supports equivariant residual addition between compatible channels.

## 127. Scalar Multiplication

If:

`a`

is invariant and:

`v`

is equivariant, then:

`a v`

inherits the transformation type of `v`.

This follows from the invariance of `a`.

## 128. Multiplication of Non-Scalar Channels

Multiplying non-scalar representation channels componentwise does not automatically produce a valid target representation.

A representation-compatible tensor-product or other declared operation is required.

## 129. Normalization Boundary

Normalization of equivariant features must preserve transformation semantics.

A scalar normalization factor derived from invariant quantities can be compatible.

Arbitrary componentwise normalization may break equivariance.

## 130. Bias Boundary

Adding a constant bias to an invariant scalar channel can preserve scalar invariance.

Adding a fixed nonzero Cartesian vector bias to a vector-equivariant channel generally selects a preferred direction and breaks rotational equivariance.

## 131. Preferred Direction

A model may legitimately include a preferred direction when an external field, interface normal, crystal orientation, or other physical state defines it.

The direction must then be part of the source state and transformation contract.

It must not enter as an undocumented constant.

## 132. External Field

If an external vector field:

`f_ext ∈ ℝ^3`

is part of the state, it must transform under the declared geometric action when the physical system is transformed.

Treating transformed geometry while keeping a co-transforming external vector numerically fixed describes a different transformation experiment.

## 133. Boundary Geometry

Interfaces, cells, surfaces, and external coordinate structures can carry their own transformation state.

Equivariance validation must transform every source object belonging to the modeled system consistently.

## 134. Partial Transformation Is a Different Input

Rotating only atomic coordinates while leaving transformation-covariant auxiliary state unchanged numerically may not represent a symmetry transformation of the complete state.

The state boundary must therefore precede symmetry validation.

## 135. Representation Completeness

Let:

`Φ: X → Y`

be a representation.

Relative to an equivalence relation:

`~`

on `X`, a completeness claim may require:

`Φ(x_1) = Φ(x_2)`

to imply:

`x_1 ~ x_2`

within the declared domain.

Completeness is always relative to the chosen equivalence relation.

## 136. Invariance and Completeness Tension

An invariant representation deliberately identifies states related by the declared symmetry.

Therefore raw injectivity on `X` is not the correct completeness criterion when symmetry-equivalent states are intentionally merged.

The relevant object is distinguishability of equivalence classes.

## 137. Equivariant Representation Can Preserve More Information

An equivariant representation can retain transformation-sensitive information that a fully invariant representation removes.

This can be useful when downstream outputs themselves transform nontrivially or when orientation information is needed internally.

## 138. Invariant Representation Can Be Sufficient for Some Claims

An invariant representation may be sufficient for a scalar target whose value is invariant under the same transformations.

This sufficiency is target-relative.

It is not universal.

## 139. Information-Loss Declaration

Every representation mapping must declare known or designed information loss.

Possible sources include:

- finite cutoff;
- neighbor truncation;
- invariant contraction;
- finite angular truncation;
- finite radial basis;
- pooling;
- dimensional bottleneck;
- quantization.

## 140. Information Loss Is Layered

The full chain may lose information at multiple stages:

`configuration`

`→ topology`

`→ local environment`

`→ equivariant features`

`→ invariant features`

`→ global aggregation`

Every loss boundary must remain identifiable.

## 141. Lost Information Is Not Recovered Automatically

If a mapping discards orientation, species distinction, locality, or scale identity, a downstream mapping cannot reconstruct that information unless an independent channel supplies it.

Therefore:

`downstream complexity ≠ recovery of absent source information`

## 142. Representation Is Not Physical Observable

A latent equivariant feature is a mathematical model state.

Unless independently interpreted and validated:

`equivariant feature ≠ physical observable`

## 143. Representation Is Not Energy

An invariant scalar representation is not automatically an energy.

Energy requires:

- energy units;
- a defined mapping;
- physical interpretation;
- validation.

Therefore:

`invariant scalar ≠ energy automatically`

## 144. Representation Is Not Force

A vector-equivariant representation is not automatically a force.

Force requires an independently defined physical mapping and units.

Therefore:

`equivariant vector ≠ force automatically`

## 145. Representation Is Not Stress

A higher-order equivariant channel is not automatically a stress tensor.

Stress requires:

- a specific tensor space;
- physical units;
- physical interpretation;
- coordinate convention;
- validation.

## 146. Representation Is Not Chemical Bond

A representation may encode geometric and species information relevant to bonding.

It does not establish a bond relation by itself.

Therefore:

`equivariant representation ≠ chemical bond`

## 147. Representation Is Not Resonance State

The EIF representation space and TR resonance-coordinate space remain distinct:

`Y_EIF ≠ X_R`

unless an explicit later mapping establishes a relation.

## 148. Representation Is Not Ternary State

The balanced ternary set remains:

`T = {-1, 0, 1}`

An EIF feature does not automatically belong to `T`.

Therefore:

`EIF representation ≠ ternary state`

## 149. No Representation-to-Ternary Threshold by Implication

No scalar EIF channel receives an automatic rule such as:

`negative → -1`

`near zero → 0`

`positive → 1`

Such a mapping would be an additional author-defined integration mapping requiring explicit semantics.

## 150. No Equivariance-to-Resonance Shortcut

Equivariance controls transformation behavior.

Resonance controls a separately defined TR relation.

Therefore:

`equivariance ≠ resonance`

and:

`equivariant representation ≠ resonance classification`

## 151. No Symmetry-to-Dynamics Shortcut

A symmetry action relates transformed descriptions or states.

It does not define time evolution.

Therefore:

`symmetry action ≠ dynamical evolution`

## 152. No Symmetry-to-Conservation Shortcut

A model may use symmetry to derive conservation laws under additional dynamical assumptions, but equivariance of a representation alone does not establish a conservation law.

Therefore:

`equivariance ≠ conservation`

## 153. No Symmetry-to-Accuracy Shortcut

A mathematically equivariant model can still predict incorrect outputs.

Therefore:

`equivariance PASS ≠ predictive accuracy`

## 154. No Symmetry-to-Physical-Validity Shortcut

Likewise:

`equivariance PASS ≠ physical validation`

Physical validation requires appropriate reference evidence.

## 155. Energy Interface Boundary

If a later EIF specialization defines:

`E: Q_N,adm → ℝ`

as potential energy, it must separately define:

- energy units;
- physical scope;
- invariance requirements;
- parameter provenance;
- validation evidence.

Its scalar nature alone is insufficient.

## 156. Energy Invariance

For an isolated system whose potential energy is intended to be rigid-motion invariant, the declared model may require:

`E(ρ_Q(g)q) = E(q)`

for the appropriate rigid-motion group.

The scope depends on the physical boundary conditions.

## 157. Force Interface Boundary

If a later differentiable energy model defines:

`f_i = -grad_(x_i) E`

then `f_i` belongs to a vector-valued physical output space.

The relation must be interpreted under the model's differentiability and coordinate assumptions.

## 158. Force Equivariance

For proper rotation:

`R ∈ SO(3)`

a polar force vector should satisfy:

`f_i' = R f_i`

under a consistently rotated physical state.

This transformation requirement does not determine the force law itself.

## 159. Conservative Force Boundary

A force obtained as the negative gradient of one differentiable scalar potential has conservative structure within the defined model domain.

A generic equivariant vector predictor does not automatically have this property.

Therefore:

`equivariant vector prediction ≠ conservative force field`

## 160. Stress Interface Boundary

A later stress output requires a separately declared tensor action.

Its transformation law must be compatible with the chosen stress convention.

EIF does not define one universal stress output in this chapter.

## 161. Tensor Field Networks Reference

Thomas et al. introduced Tensor Field Networks for three-dimensional point-cloud data with local equivariance to rotations, translations, and permutations.

The architecture uses spherical-harmonic filters and transformation-aware scalar, vector, and higher-order tensor channels.

This provides a primary computational precedent for layered equivariant feature construction.

Provenance:

`PRIMARY_SOURCE`

## 162. NequIP Reference

Batzner et al. introduced Neural Equivariant Interatomic Potentials using E(3)-equivariant graph neural-network operations for atomistic energy and force modeling.

The architecture maintains internal geometric tensor features with explicit E(3) transformation behavior while producing invariant energy output.

This provides a primary interatomic precedent for the distinction between:

`equivariant internal representation`

and:

`invariant physical output`

Provenance:

`PRIMARY_SOURCE`

## 163. e3nn Reference

Geiger and Smidt describe e3nn as a framework for constructing E(3)-equivariant trainable functions through composable equivariant operations including spherical harmonics and tensor products.

This provides a computational reference for typed Euclidean representation channels and their composition.

EIF does not require e3nn as an implementation.

Provenance:

`PRIMARY_SOURCE`

## 164. Allegro Reference

Musaelian et al. introduced Allegro as a strictly local equivariant interatomic-potential architecture using learned equivariant representations and tensor-product operations without requiring atom-centered message passing.

This provides an established example that:

`equivariant interatomic representation`

does not require:

`multi-hop message passing`

as a universal architecture.

Provenance:

`PRIMARY_SOURCE`

## 165. Literature Boundary

The cited architectures establish computational precedent for:

- Euclidean-equivariant feature construction;
- spherical-harmonic geometric channels;
- tensor-product feature coupling;
- invariant and equivariant channel coexistence;
- equivariant atomistic local representations;
- invariant energy readout;
- local equivariant interatomic architectures.

They do not establish:

- one universal EIF architecture;
- universal physical completeness;
- universal feature multiplicity;
- universal angular cutoff;
- universal locality radius;
- universal energy law;
- universal force law;
- TR resonance semantics;
- balanced ternary semantics;
- automatic EIF-to-TR mappings.

## 166. Primary Sources

1. Thomas, N., Smidt, T., Kearnes, S., Yang, L., Li, L., Kohlhoff, K., and Riley, P. "Tensor Field Networks: Rotation- and Translation-Equivariant Neural Networks for 3D Point Clouds." arXiv:1802.08219, 2018. https://arxiv.org/abs/1802.08219

2. Batzner, S., Musaelian, A., Sun, L., Geiger, M., Mailoa, J. P., Kornbluth, M., Molinari, N., Smidt, T. E., and Kozinsky, B. "E(3)-Equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials." Nature Communications 13, 2453, 2022. DOI: `10.1038/s41467-022-29939-5`

3. Geiger, M., and Smidt, T. "e3nn: Euclidean Neural Networks." arXiv:2207.09453, 2022. https://arxiv.org/abs/2207.09453

4. Musaelian, A., Batzner, S., Johansson, A., Sun, L., Owen, C. J., Kornbluth, M., and Kozinsky, B. "Learning Local Equivariant Representations for Large-Scale Atomistic Dynamics." Nature Communications 14, 579, 2023. DOI: `10.1038/s41467-023-36329-y`

These sources establish relevant classical and computational precedents.

EIF-specific representation contracts, TR-EIF boundaries, provenance requirements, conformance rules, and integration restrictions remain author-defined framework structure.

## 167. Minimal Symmetry Contract

Every EIF symmetry claim must define:

1. transformation group or transformation set;
2. transformation element;
3. source space;
4. target space;
5. source action;
6. target action;
7. mapping;
8. transformation relation;
9. admissible source domain;
10. numerical tolerance where applicable;
11. provenance of implementation-specific parameters.

## 168. Minimal Permutation Contract

Every permutation-aware representation must define:

1. site-index set;
2. atomic identity correspondence;
3. position correspondence;
4. topology correspondence;
5. environment correspondence;
6. local-feature correspondence;
7. global-output behavior;
8. variable-cardinality behavior where applicable.

## 169. Minimal Euclidean Contract

Every Euclidean transformation claim must define:

1. whether the group is `SO(3)`, `O(3)`, `SE(3)`, `E(3)`, or another declared group;
2. translation action;
3. rotation action;
4. reflection behavior where applicable;
5. cell transformation where periodic state is included;
6. external-field transformation where applicable;
7. representation action;
8. output action.

## 170. Minimal Representation Contract

Every EIF representation must define:

1. source environment or configuration space;
2. representation codomain;
3. transformation group;
4. representation types;
5. multiplicities;
6. parity where relevant;
7. basis convention where relevant;
8. locality;
9. scale;
10. information retained;
11. information lost;
12. numerical encoding where executable;
13. validation relation.

## 171. Minimal Invariant-Readout Contract

An invariant readout must define:

1. source representation;
2. invariant target space;
3. transformations under which invariance is claimed;
4. contraction or aggregation mapping;
5. information loss;
6. permutation behavior;
7. physical interpretation if one is assigned.

## 172. Minimal Equivariant-Readout Contract

An equivariant readout must define:

1. source representation;
2. target representation type;
3. target action;
4. transformation relation;
5. physical units where applicable;
6. physical interpretation where applicable;
7. validation rule.

## 173. Exact Equivariance Validation

Exact mathematical validation asks whether:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

holds over the declared domain.

An analytical construction may establish this relation directly.

A finite numerical test cannot by itself prove the relation over an infinite transformation group.

## 174. Numerical Equivariance Validation

A numerical implementation must define:

- transformation samples;
- source samples;
- error metric;
- tolerance;
- numeric precision;
- basis convention;
- deterministic comparison procedure.

The output is a numerical validation result, not a redefinition of exact equivariance.

## 175. Permutation Validation

Permutation validation must test that reindexing does not alter physical identity correspondence.

For local site-indexed outputs, the expected result is corresponding reindexing.

For declared global invariant outputs, the expected result is equality.

## 176. Translation Validation

A translation validation test must transform all position-dependent source state consistently.

Relative-geometry representations intended to be translation invariant must preserve their declared values within numerical tolerance.

## 177. Rotation Validation

A rotation validation test must compare each representation channel according to its own rotation action.

Scalar and vector channels cannot be validated through the same equality rule.

## 178. Reflection Validation

When `O(3)` or `E(3)` behavior is claimed, reflection tests must evaluate the declared parity semantics.

Passing only `SO(3)` tests is insufficient.

## 179. Composite-Pipeline Validation

A pipeline claiming end-to-end equivariance must validate the complete mapping:

`source state`

`→ environment`

`→ representation`

`→ processing`

`→ readout`

An equivariant internal layer does not guarantee equivariance of an arbitrary surrounding pipeline.

## 180. Basis-Conversion Validation

If two modules use different equivalent representation bases, the interface must define the basis-conversion map.

The conversion itself must preserve the intended transformation relation.

## 181. Serialization Boundary

Serialized representation arrays must retain sufficient metadata to recover their mathematical channel semantics.

JSON, binary arrays, tensor layouts, or framework-specific tensor objects are storage formats.

They do not replace the representation contract.

## 182. Machine Precision Boundary

Floating-point roundoff may produce small nonzero equivariance residuals in an analytically equivariant architecture.

Such residuals belong to numerical realization.

They do not alter the exact mathematical relation.

## 183. Quantization Boundary

Fixed-point or integer quantization may also perturb equivariance numerically.

A quantized realization requires its own validation tolerance or exact encoded symmetry rule.

No quantization scheme is imposed in this chapter.

## 184. Representation Provenance

Every executable representation configuration should preserve provenance for:

- transformation group;
- basis convention;
- included `l` values;
- parity convention;
- feature multiplicities;
- radial basis;
- cutoff;
- numerical precision;
- architecture revision.

These are implementation facts, not universal constants.

## 185. Model Parameter Provenance

Learned or selected representation parameters must use the provenance classes inherited from Volume 01.

Examples include:

`CALIBRATED`

`BENCHMARK`

`AUTHOR_DEFINED`

`TEST_FIXTURE`

or other applicable inherited classes.

## 186. Core Symmetry Invariants

The following invariants are mandatory.

1. Every symmetry claim identifies its transformation scope.

2. Every group action has a declared source space.

3. Invariance remains distinct from equivariance.

4. Permutation invariance remains distinct from permutation equivariance.

5. Translation remains distinct from rotation.

6. Rotation remains distinct from reflection.

7. Euclidean transformation remains distinct from computational permutation.

8. `SO(3)` remains distinct from `O(3)`.

9. `SE(3)` remains distinct from `E(3)`.

10. Relative displacement remains rotation equivariant and translation invariant under the declared ordinary geometric action.

11. Distance remains rotationally invariant under orthogonal transformations.

12. Representation type remains distinct from array shape.

13. Scalar, vector, and higher-order channels remain separately typed.

14. Parity remains distinct from ternary state.

15. Irreducible degree remains distinct from physical observable identity.

16. Tensor product remains distinct from concatenation.

17. Arbitrary nonlinear processing is not assumed equivariant.

18. Arbitrary channel mixing is not assumed equivariant.

19. Equivariant composition requires compatible intermediate actions.

20. Invariant contraction may lose directional information.

21. Pooling may lose locality and site identity.

22. Hierarchy remains distinct from equivariance.

23. Message passing remains distinct from equivariance.

24. Neural architecture remains distinct from equivariance.

25. Data augmentation remains distinct from exact equivariance.

26. Exact equivariance remains distinct from numerical tolerance compliance.

27. Sampled transformation validation remains distinct from analytical proof.

28. Equivariance remains distinct from predictive accuracy.

29. Equivariance remains distinct from physical validation.

30. Equivariance remains distinct from conservation.

31. EIF representation remains distinct from physical observable.

32. Invariant scalar remains distinct from energy.

33. Equivariant vector remains distinct from force.

34. Higher-order equivariant channel remains distinct from stress.

35. Equivariant representation remains distinct from chemical bond.

36. EIF representation remains distinct from TR resonance state.

37. EIF representation remains distinct from ternary state.

38. Geometry transformation does not automatically alter ternary polarity.

39. Representation parity does not define ternary polarity.

40. EIF-to-TR semantics require an explicit typed integration mapping.

## 187. Formal Non-Equivalences

The following non-equivalences are mandatory:

`invariance ≠ equivariance`

`permutation invariance ≠ permutation equivariance`

`translation ≠ rotation`

`rotation ≠ reflection`

`rotation ≠ permutation`

`SO(3) ≠ O(3)`

`SE(3) ≠ E(3)`

`representation type ≠ array shape`

`scalar channel ≠ vector channel`

`vector channel ≠ physical force`

`higher-order channel ≠ physical stress`

`representation parity ≠ ternary state`

`l = 1 channel ≠ force automatically`

`l = 2 channel ≠ stress automatically`

`tensor product ≠ concatenation`

`message passing ≠ equivariance`

`graph neural network ≠ equivariance`

`neural network ≠ equivariance`

`data augmentation ≠ exact equivariance`

`hierarchy ≠ equivariance`

`locality ≠ equivariance`

`equivariance ≠ continuity`

`equivariance ≠ differentiability`

`equivariance ≠ conservation`

`equivariance ≠ predictive accuracy`

`equivariance ≠ physical validation`

`exact equivariance ≠ numerical equivariance within tolerance`

`sampled equivariance PASS ≠ proof over complete group`

`invariant contraction ≠ lossless transformation`

`global pooling ≠ complete local representation`

`equivariant feature ≠ physical observable`

`invariant scalar ≠ energy automatically`

`equivariant vector ≠ force automatically`

`equivariant tensor ≠ stress automatically`

`equivariant representation ≠ chemical bond`

`EIF representation ≠ resonance state`

`EIF representation ≠ ternary state`

`representation parity ≠ ternary polarity`

`geometric reflection ≠ ternary polarity inversion`

## 188. Formal Representation Chain

The EIF representation chain is:

`interatomic configuration`

`→ boundary-aware geometry`

`→ topology`

`→ local atomic environment`

`→ typed geometric channels`

`→ invariant / equivariant representation`

`→ local representation collection`

`→ optional multiscale representation`

`→ invariant or equivariant readout`

Every arrow has its own source and target semantics.

No arrow implies physical meaning that has not been separately defined.

## 189. Representation-Type Chain

For a three-dimensional symmetry-aware realization, one possible abstract decomposition is:

`relative geometry`

`→ radial invariant channels`

`+ angular transformation channels`

`→ typed (l, p) representation channels`

`→ transformation-compatible coupling`

`→ local equivariant state`

`→ invariant and/or equivariant outputs`

This is a formal design pattern.

It is not a mandatory neural architecture.

## 190. EIF-to-TR Boundary

The output of the present layer belongs to an EIF representation space such as:

`Y_EIF`

or:

`Y_EIF,MS`

It does not yet belong to:

`X_TR,in`

`X_R`

`R_C`

or:

`T = {-1, 0, 1}`

A later integration mapping must define:

`M_E→TR: Y_EIF → X_TR,in`

or a more structured typed relation.

## 191. Transformation Requirement for Future EIF-to-TR Mapping

If a later integrated model claims that the EIF-to-TR mapping preserves or transforms symmetry structure, then `M_E→TR` itself must define:

- source action on `Y_EIF`;
- target action on `X_TR,in`;
- exact transformation relation;
- information loss;
- locality;
- scale.

Equivariance of `Y_EIF` does not automatically propagate through an arbitrary integration map.

## 192. Future TR Feedback Boundary

If TR state later modifies an EIF representation, that feedback mapping must specify its transformation behavior independently.

A ternary value cannot be inserted into an equivariant vector or higher-order channel without a declared action-compatible mapping.

## 193. Balanced Ternary Boundary

The closed TR kernel remains exactly:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and active neutral:

`0`

No representation-theoretic use of the numbers `-1` or `1` changes these semantics.

## 194. No Symbolic Collision Across Layers

The same numeric values may appear in:

- parity labels;
- signs;
- tensor coefficients;
- ternary states.

Their mathematical types remain distinct.

Numeric equality does not imply semantic equality.

## 195. Symmetry-Layer Conformance Requirements

An EIF representation conforms to this chapter when:

- its source state is explicitly defined;
- its transformation group is explicitly defined;
- source and target actions are explicitly defined;
- local environment correspondence is preserved;
- permutation semantics are correct;
- translation semantics are correct;
- rotation semantics are correct;
- reflection semantics are correct when claimed;
- representation channels retain their declared transformation types;
- incompatible channel operations are not used without a valid coupling rule;
- information loss is declared;
- exact and numerical equivariance are distinguished;
- physical interpretation is not inferred from representation type alone;
- no TR semantics are introduced without an explicit cross-layer mapping.

## 196. Computational Conformance Requirements

A computational realization additionally conforms when:

- basis conventions are fixed;
- feature channel layouts are typed;
- transformation tests cover every claimed transformation class;
- permutation tests preserve species correspondence;
- numerical tolerances are declared;
- degenerate geometry behavior is defined;
- cutoff-dependent topology behavior is deterministic;
- representation metadata are preserved;
- serialization does not erase transformation type;
- finite precision is separated from exact theory;
- benchmark results are not promoted to universal mathematical claims.

## 197. Primary-Literature Validation Boundary

The primary literature cited in this chapter supports established computational use of:

- tensor-field equivariance;
- spherical-harmonic angular representations;
- tensor-product coupling;
- E(3)-equivariant atomistic representations;
- invariant-energy / equivariant-feature separation;
- strictly local equivariant interatomic representations.

EIF extends these precedents into a broader author-defined framework contract.

The extension must not be attributed to those source architectures.

## 198. Final Statement

The symmetry-aware representation layer of EIF is defined by the chain:

`local atomic environment`

`→ declared transformation actions`

`→ typed invariant and equivariant channels`

`→ transformation-compatible composition`

`→ local / global / multiscale EIF representation`

The fundamental relation is:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for equivariant mappings and:

`F(ρ_X(g)x) = F(x)`

for invariant mappings.

These relations are meaningful only when:

- the transformation group;
- source space;
- target space;
- source action;
- target action;
- mapping;
- admissible domain;

are explicitly defined.

Permutation, translation, proper rotation, reflection, and parity remain distinct transformation semantics.

`SO(3)`, `O(3)`, `SE(3)`, and `E(3)` remain distinct groups.

Invariant scalar channels, equivariant vector channels, and higher-order representation channels remain mathematically distinct.

No representation type is assigned physical meaning automatically.

In particular:

`invariant scalar ≠ energy`

`equivariant vector ≠ force`

`higher-order channel ≠ stress`

`equivariant representation ≠ chemical bond`

and:

`equivariant representation ≠ resonance state`

The balanced ternary layer remains independently defined as:

`-1/0/1`

with active:

`0`

No geometric transformation, reflection parity, invariant contraction, or equivariant feature determines ternary polarity by implication.

The resulting EIF chain is now:

`interatomic state`

`→ geometry`

`→ topology`

`→ local environment`

`→ invariant / equivariant representation`

This establishes the transformation-aware representation foundation required before interatomic mappings, physical output interfaces, multiscale EIF dynamics, or explicit EIF-to-TR integration can be defined.
