# Equivariant Interatomic Foundations

## 1. Purpose

This document establishes the mathematical foundations of the Equivariant Interatomic Framework layer of TR-EIF.

The chapter defines:

- the EIF system class;
- atomic configuration spaces;
- atomic identities and computational indices;
- interatomic relative geometry;
- interaction topology;
- local atomic environments;
- geometric transformation actions;
- permutation actions;
- translation actions;
- rotation actions;
- reflection handling;
- invariant and equivariant mappings;
- scalar, vector, and higher-order representation channels;
- local and global representation boundaries;
- topology and geometry separation;
- interatomic representation spaces;
- information-preservation and information-loss requirements;
- the distinction between representation, physical state, energy, force, and learned prediction;
- the independent mathematical closure required before EIF can be connected to the Ternary Resonant layer.

This chapter begins the standalone formalization of:

`EIF = Equivariant Interatomic Framework`

It does not yet define the TR-to-EIF integration layer.

## 2. Dependency

This chapter depends on the committed mathematical foundations of Volume 01 and respects the closed Ternary Resonant theory of Volume 02.

It inherits without redefinition:

- typed state spaces;
- domains and codomains;
- mathematical mappings;
- relations;
- invariants;
- configuration space `Q`;
- atomic-site set `V`;
- atomic identity notation `z_i`;
- position notation `x_i`;
- relative-displacement mappings;
- graph construction mappings;
- local-environment mappings;
- descriptor mappings;
- permutation-invariant mappings;
- permutation-equivariant mappings;
- transformation-action semantics;
- general invariance and equivariance definitions;
- provenance classes;
- validation boundaries.

Volume 02 remains closed.

This chapter does not alter any Ternary Resonant definitions.

## 3. Scientific Status Classes

The mathematical objects in this chapter are separated by scientific status.

### 3.1 CLASSICAL

The following concepts are classical mathematical or established computational concepts:

- Euclidean geometry;
- group actions;
- permutation actions;
- invariant mappings;
- equivariant mappings;
- Euclidean transformations;
- tensor transformation behavior;
- graph-based local environments;
- symmetry-aware atomistic representations.

### 3.2 EIF FORMAL / AUTHOR-DEFINED

The following are TR-EIF author-defined formal architecture:

- the exact EIF state decomposition;
- EIF interface boundaries;
- EIF representation contracts;
- information-loss requirements;
- transformation-contract requirements;
- interatomic representation hierarchy;
- EIF closure requirements;
- future compatibility boundary with the TR layer.

### 3.3 DERIVED

Relations obtained mathematically from declared EIF definitions are classified as:

`DERIVED`

### 3.4 OPERATIONAL / EXECUTABLE REFERENCE

No executable architecture is elevated to normative EIF theory in this chapter.

Existing equivariant machine-learning architectures may provide implementation examples, but they do not define the complete EIF mathematical layer.

### 3.5 EMPIRICAL / CALIBRATED

Any numerical relation to measured material behavior requires independent calibration or empirical validation.

### 3.6 UNVERIFIED

Any claimed physical meaning not established by the declared interatomic model or external evidence remains unverified.

## 4. Project Identity

The complete framework remains:

`TR-EIF = Ternary Resonant Equivariant Interatomic Framework`

with:

`TR = Ternary Resonant`

and:

`EIF = Equivariant Interatomic Framework`

The two layers are mathematically distinct before integration.

Therefore:

`TR ≠ EIF`

and:

`EIF ≠ TR`

Their eventual connection requires explicit typed mappings.

## 5. EIF Layer Identity

EIF is the mathematical layer responsible for representing interatomic systems under declared geometric and indexing transformations.

Its fundamental concern is not merely prediction.

Its fundamental concern is the relation:

`interatomic configuration`

`→ structured local or global representation`

under transformations whose effects are mathematically controlled.

EIF therefore includes:

- atomic configuration;
- atomic identity;
- interatomic geometry;
- topology;
- locality;
- symmetry actions;
- invariant representations;
- equivariant representations;
- transformation-aware mappings.

## 6. EIF Is Not a Single Neural-Network Architecture

EIF is not identified with any one existing machine-learning architecture.

In particular:

`EIF ≠ NequIP`

`EIF ≠ Allegro`

`EIF ≠ Tensor Field Networks`

`EIF ≠ e3nn`

`EIF ≠ message passing`

`EIF ≠ graph neural network`

Such systems may realize subsets of the mathematical requirements defined by EIF.

They do not define EIF itself.

## 7. EIF Is Not Automatically a Potential

The name:

`Equivariant Interatomic Framework`

is broader than:

`interatomic potential`

An EIF realization may eventually define:

- energy;
- forces;
- stress;
- response fields;
- structural descriptors;
- latent representations;
- other interatomic outputs.

None of those outputs is implied merely by the existence of an equivariant representation.

Therefore:

`EIF representation ≠ interatomic potential`

## 8. System Class

The basic EIF system class is a finite or otherwise explicitly bounded collection of represented atomic sites together with their identities, geometry, boundary data, and declared interaction structure.

For fixed cardinality `N`, the atomic-site index set is:

`V = {1, 2, ..., N}`

The integer label `i ∈ V` is a computational site index.

It is not itself an atomic species.

## 9. Atomic Identity

For every site `i ∈ V`, let:

`z_i ∈ Z`

where `Z` is the declared atomic-identity domain.

Depending on the specialization, `z_i` may represent:

- atomic number;
- element identity;
- species class;
- another explicitly defined atomic type.

The model must declare which interpretation is used.

## 10. Atomic Position

For spatial dimension `d`, the position of site `i` is:

`x_i ∈ ℝ^d`

For ordinary three-dimensional interatomic systems:

`d = 3`

The complete position state is:

`X = (x_1, x_2, ..., x_N) ∈ (ℝ^d)^N`

## 11. Identity State

The complete atomic-identity state is:

`Z_state = (z_1, z_2, ..., z_N)`

The identity state and position state are distinct.

Therefore:

`Z_state ≠ X`

## 12. Basic Atomic Configuration

A fixed-cardinality atomic configuration may be represented as:

`q = ((z_1, x_1), ..., (z_N, x_N))`

with:

`q ∈ Q`

where `Q` is the declared interatomic configuration space inherited from Volume 01.

## 13. Extended Atomic Configuration

A specialization may extend `q` with additional physical or boundary state such as:

- periodic-cell geometry;
- occupancy;
- charge state;
- spin state;
- velocity;
- external fields;
- constraints.

Every extension must have a separately declared state space.

Such variables are not implicitly present in the minimal configuration.

## 14. Computational Index Is Not Atomic Identity

A computational permutation may change the order in which atomic sites are stored.

It does not change their physical identity.

Therefore:

`index permutation ≠ atomic transmutation`

and:

`index label ≠ atomic species`

## 15. Relative Displacement

For sites `i` and `j`, define the relative displacement:

`r_ij = x_j - x_i`

with:

`r_ij ∈ ℝ^d`

The orientation is ordered.

Therefore:

`r_ji = -r_ij`

in an ordinary non-periodic Euclidean coordinate representation.

## 16. Interatomic Distance

Define the pair distance:

`d_ij = ||r_ij||`

with:

`d_ij ∈ ℝ_≥0`

For distinct sites in a non-degenerate configuration:

`d_ij > 0`

unless coincident positions are explicitly admitted.

## 17. Distance Symmetry

For Euclidean distance:

`d_ij = d_ji`

while:

`r_ij ≠ r_ji`

for a nonzero displacement.

This distinction is fundamental.

Distance is an invariant scalar under rotation.

Relative displacement is a geometric vector.

## 18. Configuration Geometry

The geometry of a configuration includes relational quantities derived from the positions.

Possible geometric objects include:

- relative displacements;
- distances;
- angles;
- oriented areas;
- local frames;
- higher-order geometric relations.

No particular set is universally sufficient.

## 19. Geometry Is Not Topology

Geometry and topology remain separately typed.

Geometry describes spatial relations.

Interaction topology describes which sites or local objects are connected by the selected interaction relation.

Therefore:

`geometry ≠ topology`

A topology may be derived from geometry, but only through an explicit mapping.

## 20. Interaction Graph

An interaction graph may be represented as:

`G = (V, E)`

where:

- `V` is the site set;
- `E` is the declared edge set.

An edge:

`(i, j) ∈ E`

means only that the model includes the ordered or unordered relation defined for that edge.

It does not automatically mean:

- chemical bond;
- mechanical contact;
- electron sharing;
- resonant coupling;
- force transmission.

## 21. Graph Construction Mapping

A graph construction mapping is typed as:

`G_C: Q → X_G`

where `X_G` is the declared graph space.

The mapping must define:

- node semantics;
- edge criterion;
- edge directionality;
- geometric cutoff if used;
- periodic treatment if used;
- tie handling;
- update behavior.

## 22. Cutoff Neighborhood

If a radial cutoff `r_c > 0` is used, a geometric neighborhood may be defined by:

`N_i = {j ∈ V \ {i} : d_ij ≤ r_c}`

This is one possible neighborhood definition.

It is not mandatory for all EIF models.

The value `r_c` is model-specific and requires provenance.

## 23. Neighborhood Is Model-Relative

A local environment depends on the declared neighborhood rule.

Two models may assign different local environments to the same atomic configuration.

Therefore:

`local environment ≠ configuration alone`

without specification of the neighborhood mapping.

## 24. Local Atomic Environment

Let `X_env` denote the local-environment space.

For site `i`, define:

`E_i: Q × X_G → X_env`

where:

`E_i(q, G)`

is the declared local environment of site `i`.

The environment may contain:

- central-site identity;
- neighbor identities;
- relative displacements;
- distances;
- edge attributes;
- periodic-image information;
- other declared local state.

## 25. Local Environment Is Not Descriptor

The physical or mathematical local environment and its encoded representation are different objects.

Let:

`D_env: X_env → X_desc`

be a descriptor mapping.

Then:

`D_env(E_i)`

is a representation of the environment.

It is not the environment itself.

Therefore:

`local environment ≠ descriptor`

## 26. Descriptor Information Loss

A descriptor mapping may be many-to-one.

If:

`D_env(E_a) = D_env(E_b)`

for distinct environments:

`E_a ≠ E_b`

then the representation loses information relevant to distinguishing those environments.

Every EIF representation must state what information it preserves and what information it may discard.

## 27. Global Transformation Set

Let `G_geom` denote a declared geometric transformation set acting on configurations.

The transformation set must be identified explicitly.

Possible elements include:

- translations;
- proper rotations;
- improper rotations or reflections;
- combinations of these transformations.

No generic word `symmetry` substitutes for the declaration of `G_geom`.

## 28. Group Action

Let a group `G` act on a space `X`.

The action is a mapping:

`ρ_X: G × X → X`

written:

`ρ_X(g)x`

for:

`g ∈ G`

and:

`x ∈ X`

The action must satisfy:

`ρ_X(e)x = x`

and:

`ρ_X(g_1 g_2)x = ρ_X(g_1)(ρ_X(g_2)x)`

where `e` is the identity element.

## 29. Action Must Be Space-Specific

The same abstract transformation may act differently on different spaces.

For a transformation `g`, the model may require:

- `ρ_Q(g)` on configurations;
- `ρ_X(g)` on features;
- `ρ_Y(g)` on outputs.

The notation must not imply that these actions are numerically identical.

## 30. Translation

For translation vector:

`a ∈ ℝ^d`

the translated position is:

`x_i' = x_i + a`

for every site `i`.

Relative displacements satisfy:

`r_ij' = r_ij`

under the same global translation.

## 31. Translation-Invariant Relative Geometry

Because:

`(x_j + a) - (x_i + a) = x_j - x_i`

relative displacement is invariant under common global translation of both endpoints as a relational coordinate.

The absolute position vector itself is not translation invariant.

## 32. Rotation

Let:

`R ∈ SO(d)`

denote a proper rotation.

A position transforms as:

`x_i' = R x_i`

when the origin convention is fixed accordingly.

A relative displacement transforms as:

`r_ij' = R r_ij`

## 33. Proper Rotation Group

In three dimensions:

`SO(3)`

denotes the group of orientation-preserving orthogonal transformations.

For:

`R ∈ SO(3)`

the defining relations are:

`R^T R = I`

and:

`det(R) = 1`

## 34. Orthogonal Group

In three dimensions:

`O(3)`

contains orthogonal transformations satisfying:

`R^T R = I`

with:

`det(R) ∈ {-1, 1}`

Thus `O(3)` contains both:

- proper rotations;
- improper orthogonal transformations such as reflections.

## 35. E(3) Boundary

The Euclidean group in three dimensions combines orthogonal transformations and translations.

An E(3) action on position may be represented as:

`x_i' = R x_i + a`

where:

`R ∈ O(3)`

and:

`a ∈ ℝ^3`

The exact transformation group used by an EIF specialization must be declared.

## 36. SE(3) Boundary

If only proper rotations and translations are included, the corresponding rigid-motion group is:

`SE(3)`

An `SE(3)`-equivariance claim is not automatically an `E(3)`-equivariance claim because reflection behavior is not determined by proper rotations alone.

Therefore:

`SE(3)-equivariance ≠ E(3)-equivariance`

## 37. Reflection

Reflection behavior must be specified explicitly when reflections are included in the transformation set.

A polar vector and an axial vector do not have identical transformation behavior under improper rotations.

Therefore reflection parity cannot be ignored when an `O(3)` or `E(3)` representation distinguishes parity.

## 38. Translation, Rotation, and Permutation Are Distinct

The framework preserves:

`translation ≠ rotation`

`rotation ≠ permutation`

`translation ≠ permutation`

These transformations act on different mathematical structures.

They must not be collapsed into one undifferentiated symmetry operation.

## 39. Atomic Permutation

Let:

`π ∈ S_N`

be a permutation of `N` computational site indices.

The permutation acts consistently on every site-indexed state.

A possible position action is:

`(π · X)_i = x_(π⁻¹(i))`

with the corresponding identity action:

`(π · Z_state)_i = z_(π⁻¹(i))`

The inverse convention ensures a left group action.

## 40. Permutation Must Preserve Correspondence

When an atomic index is permuted, every dependent site-indexed object must be permuted consistently.

This includes, where applicable:

- positions;
- identities;
- velocities;
- forces;
- local features;
- node outputs;
- topology indices;
- trace identities.

Partial reindexing is invalid.

## 41. Permutation of Equivalent Physical Description

For ordinary atomistic representations, changing computational ordering must not change the represented physical configuration.

This does not mean that atomic identities are erased.

A permutation exchanges indexed records while preserving the identity attached to each represented atom.

## 42. Species-Aware Permutation

Permutation symmetry does not imply that different species become indistinguishable.

If a carbon and oxygen atom exchange computational array positions, their species labels must move with them.

Therefore:

`permutation invariance ≠ species erasure`

## 43. Invariant Mapping

Let:

`F: X → Y`

with a declared action `ρ_X` of group `G` on `X`.

The mapping is invariant under `G` when:

`F(ρ_X(g)x) = F(x)`

for every admissible:

`g ∈ G`

and:

`x ∈ X`

This definition requires the transformation set and input action to be known.

## 44. Equivariant Mapping

Let:

`F: X → Y`

with declared actions:

`ρ_X`

and:

`ρ_Y`

of group `G`.

The mapping is equivariant when:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for every admissible:

`g ∈ G`

and:

`x ∈ X`

Equivariance is therefore a relation among:

- a group;
- an input space;
- an output space;
- two actions;
- a mapping.

## 45. Equivariance Is Not Decorative Terminology

A mapping must not be called equivariant unless all of the following are defined:

1. transformation group or transformation set;
2. domain;
3. codomain;
4. input action;
5. output action;
6. equivariance relation;
7. scope over which the relation holds.

Without these objects, the equivariance claim is incomplete.

## 46. Invariance and Equivariance Are Different

An invariant output remains unchanged under the declared transformation.

An equivariant output transforms according to its declared output action.

Therefore:

`invariance ≠ equivariance`

An invariant scalar and an equivariant vector may both be valid outputs of the same architecture.

## 47. Scalar Representation

A geometric scalar channel has a trivial rotation action when it is rotationally invariant.

For scalar feature:

`s`

the rotational relation is:

`s' = s`

under the declared rotation.

Examples may include appropriately defined:

- distances;
- scalar species embeddings;
- scalar invariant contractions.

Not every numerical scalar is automatically a geometric invariant.

## 48. Vector Representation

A polar vector feature:

`v ∈ ℝ^3`

transforms under rotation as:

`v' = R v`

for:

`R ∈ SO(3)`

A vector output that remains numerically fixed under arbitrary rotation is generally not rotationally equivariant under the standard vector action.

## 49. Higher-Order Representation

Higher-order geometric features require explicitly defined transformation representations.

A feature space may be decomposed into channels transforming under irreducible or other declared representations of the selected group.

The representation type is part of the state semantics.

## 50. Representation Space

Let:

`Y_EIF`

denote a declared EIF representation space.

A configuration representation mapping may be typed as:

`Φ_EIF: Q → Y_EIF`

The mapping does not become equivariant merely because `Y_EIF` contains geometric tensors.

Its transformation relation must be established.

## 51. Representation Action

Let:

`ρ_Q(g): Q → Q`

be the transformation action on configurations.

Let:

`ρ_EIF(g): Y_EIF → Y_EIF`

be the corresponding output action.

EIF equivariance requires:

`Φ_EIF(ρ_Q(g)q) = ρ_EIF(g)Φ_EIF(q)`

for all transformations and configurations within the declared scope.

## 52. Local Representation

For local environment `E_i`, define a local representation mapping:

`Φ_i: X_env → Y_i`

where `Y_i` is the local representation space.

The local representation must specify:

- central-site identity;
- transformation behavior;
- permutation behavior;
- locality;
- retained geometric information.

## 53. Site-Indexed Equivariance

A complete set of local representations:

`H = (h_1, ..., h_N)`

may transform under both geometry and site permutation.

Geometric transformation acts on each representation according to its geometric representation type.

Permutation acts on the site index.

These are separate actions.

## 54. Combined Action

For a geometric transformation `g` and permutation `π`, a combined action may be defined on the configuration only after the model declares how the actions compose.

The framework must not assume commutativity unless it follows from the declared representation.

In ordinary consistent atom relabeling and global geometry transformation, the operations may commute at the configuration-description level, but that property must be established for the selected formalization.

## 55. Product Transformation Structure

When geometric and permutation transformations are independently represented, a model may work with a product-like transformation structure.

The exact algebraic structure must be declared before using it in proofs.

The phrase:

`geometric and permutation symmetry`

does not determine the group structure by itself.

## 56. Translation Treatment in Local Environments

Using relative displacement:

`r_ij = x_j - x_i`

removes dependence on common global translation from that geometric channel.

This is a standard route to translation-invariant local geometry.

It does not automatically establish rotational invariance or permutation invariance.

## 57. Rotation Treatment in Local Environments

Under rotation:

`r_ij → R r_ij`

Thus relative displacement retains orientation information equivariantly.

Distance:

`d_ij = ||r_ij||`

removes this orientation information and is rotationally invariant.

The choice between these representations determines information retained by the local model.

## 58. Invariant Distance Is Not Complete Geometry

Two distinct local configurations may share the same subset of pair distances.

Therefore a collection of distances must not be assumed to be a complete local-environment representation without a separate completeness result.

## 59. Angular Information

For nonzero relative vectors `r_ij` and `r_ik`, an angular relation may be represented through a normalized inner product:

`c_jik = (r_ij · r_ik) / (||r_ij|| ||r_ik||)`

This quantity is invariant under common orthogonal transformation of the vectors.

Its definition requires nonzero denominator.

## 60. Orientation Information

Invariant distances and inner products may remove orientation information.

If a model requires orientation-sensitive output, the representation must retain an appropriate equivariant channel or another orientation-aware structure.

Invariant preprocessing cannot later recover information that it destroyed unless the missing information is supplied independently.

## 61. Local Frame Boundary

A local coordinate frame may be used only if its construction is explicitly defined.

The frame construction must address:

- degeneracy;
- sign ambiguity;
- permutation behavior;
- rotation behavior;
- reflection behavior;
- discontinuity.

An arbitrary coordinate frame must not be presented as intrinsic geometry.

## 62. Degenerate Geometry

A representation must define its behavior when geometric objects used to construct it become degenerate.

Examples include:

- coincident sites;
- collinear vectors;
- vanishing cross products;
- equal-distance ties;
- symmetric neighborhoods.

A formula valid only for non-degenerate geometry must state that domain restriction.

## 63. Periodic Systems

For periodic systems, relative geometry requires an explicit periodic convention.

Possible required objects include:

- simulation cell;
- lattice vectors;
- image indices;
- wrapping convention;
- minimum-image rule where applicable.

The non-periodic expression:

`x_j - x_i`

must not silently replace a periodic displacement relation.

## 64. Cell Transformation

If the simulation cell itself transforms, the transformation law for cell geometry must be defined independently from the transformation of Cartesian atomic coordinates.

Rigid rotation and cell deformation are different transformations.

Therefore:

`rotation ≠ strain`

## 65. Interaction Locality

A representation is local only relative to a declared locality rule.

Locality may be defined through:

- radial cutoff;
- graph distance;
- fixed neighborhood;
- adaptive neighborhood;
- another explicit relation.

The word `local` has no complete mathematical meaning without that rule.

## 66. Strict Locality

A strictly local output for site `i` depends only on the declared local environment of `i` and model parameters.

If information from arbitrarily distant sites can influence the output through repeated propagation, the effective receptive field may exceed the original geometric neighborhood.

Strict locality and message-passing locality are therefore not automatically equivalent.

## 67. Message Passing Boundary

A message-passing architecture is one possible implementation of interatomic information propagation.

EIF does not require message passing universally.

Therefore:

`equivariance ≠ message passing`

and:

`interatomic representation ≠ message passing`

## 68. Edge Representation

For edge `(i, j)`, an edge representation may depend on:

- `z_i`;
- `z_j`;
- `r_ij`;
- `d_ij`;
- other declared local state.

The representation must specify whether the edge is ordered.

For ordered edges:

`h_ij`

and:

`h_ji`

need not be identical.

## 69. Directed and Undirected Edges

An undirected interaction relation satisfies:

`{i, j} = {j, i}`

as one edge object.

A directed interaction representation distinguishes:

`(i, j)`

from:

`(j, i)`

The graph type must be declared before interpreting edge-indexed quantities.

## 70. Node Representation

For site `i`, a node representation may combine:

- atomic identity;
- aggregated neighbor information;
- geometric tensor channels;
- scalar channels;
- history or dynamic state if explicitly included.

A node representation is not automatically a physical atomic state.

## 71. Latent Representation Boundary

A learned latent feature is an internal mathematical representation.

Unless separately calibrated and interpreted:

`latent feature ≠ physical observable`

`latent vector ≠ force`

`latent scalar ≠ energy`

`latent channel ≠ chemical bond`

## 72. Aggregation

Let a local aggregation mapping be:

`A_i: X_multiset → Y_i`

where `X_multiset` represents a declared collection of neighbor contributions.

If ordering of equivalent neighbors must not affect the result, `A_i` must satisfy the corresponding permutation-invariance relation.

## 73. Sum Aggregation

A finite sum of consistently typed neighbor contributions is permutation invariant with respect to reordering of those contributions.

This property concerns the aggregation order.

It does not by itself prove geometric invariance or equivariance of the contributions.

## 74. Equivariant Aggregation

If every contribution transforms in the same linear representation and the aggregation operator commutes with that action, the aggregate can preserve equivariance.

The required compatibility must be established rather than assumed.

## 75. Equivariant Composition

Let:

`F: X → Y`

and:

`G: Y → Z`

be equivariant under compatible actions of the same transformation group.

Then the composition:

`G ∘ F: X → Z`

is equivariant under those compatible actions.

Compatibility of the intermediate action on `Y` is required.

## 76. Invariant Readout

An equivariant internal representation may be mapped to an invariant output through a declared invariant readout.

This architecture is common in symmetry-aware interatomic models.

The invariant final output does not imply that all internal features are invariant.

## 77. Equivariant Readout

A vector or tensor output requires a corresponding nontrivial output transformation law.

For a force-like vector output, rotational covariance is necessary but is not sufficient to establish that the quantity is physically a force.

Physical semantics require an independent force definition.

## 78. Energy Boundary

If a specialization defines total potential energy:

`E: Q → ℝ`

and claims rigid-motion invariance, the corresponding invariance relation must be stated.

Energy is not introduced as a mandatory EIF output by this chapter.

Therefore:

`EIF state ≠ energy`

## 79. Force Boundary

If an energy-based specialization defines:

`f_i = -∂E / ∂x_i`

then force semantics arise from that independently defined differentiable energy model.

This relation is not inferred from generic equivariance alone.

Therefore:

`equivariance ≠ force law`

## 80. Force Transformation

For an ordinary polar force vector under a proper rotation `R`, a physically consistent rotational transformation is:

`f_i' = R f_i`

provided the force law and coordinate transformation satisfy the corresponding physical assumptions.

This is an equivariance requirement for that force representation.

It does not define the force magnitude or interaction law.

## 81. Energy Conservation Boundary

Obtaining forces as the negative gradient of a single differentiable scalar potential imposes a conservative-force structure within that model.

A generic equivariant vector predictor does not automatically satisfy that condition.

Therefore:

`equivariant force prediction ≠ conservative force field`

unless the conservative relation is independently enforced or established.

## 82. Stress Boundary

Stress is neither a scalar energy nor a polar vector force.

Any stress representation requires:

- its tensor space;
- coordinate convention;
- transformation law;
- units;
- physical definition.

Stress must not be introduced as an untyped output.

## 83. Physical Units

Geometric and physical quantities must retain dimensional meaning.

Examples include:

- position: length;
- displacement: length;
- distance: length;
- force: force dimension;
- energy: energy dimension.

A dimensionless latent representation may interact with dimensional quantities only through a dimensionally defined mapping.

## 84. Dimensionless Representation Does Not Erase Physical Units

A model may encode dimensional input into dimensionless internal features.

This does not make the original physical quantity dimensionless.

The encoding and decoding or output mapping must preserve dimensional interpretation where physical outputs are claimed.

## 85. Atomic Species Are Not Coordinates

Atomic identities remain unchanged under ordinary Euclidean coordinate transformations.

Thus for geometric transformation `g`:

`z_i' = z_i`

unless the model explicitly includes a non-geometric identity transformation.

Rotating geometry does not transform carbon into oxygen.

## 86. Euclidean Transformation Does Not Alter Ternary Polarity

The closed Volume 02 invariant remains applicable at the future integration boundary:

a translation, rotation, reflection, or atomic permutation does not automatically map:

`-1 ↔ 1`

or alter active neutral `0`.

Any nontrivial action on ternary state would require an explicit separately defined mapping.

## 87. Geometry Is Not Resonance State

The EIF geometric state and the TR resonance state remain separately typed.

Therefore:

`interatomic geometry ≠ resonance state`

`equivariant representation ≠ resonance coordinate`

A future integration mapping must establish any relation between them.

## 88. Geometry Is Not Oscillator Phase

No atomic coordinate or geometric orientation is automatically an oscillator phase.

Therefore:

`atomic position ≠ oscillator phase`

`bond angle ≠ oscillator phase`

`rotation angle ≠ TR oscillator phase`

An explicit mapping is required if a later integrated model connects these objects.

## 89. Geometric Neighborhood Is Not Chemical Bond Graph

A distance-based or cutoff-based neighbor relation does not automatically define chemical bonds.

Therefore:

`neighbor edge ≠ chemical bond`

Chemical interpretation requires a separate physical criterion.

## 90. Equivariant Representation Is Not Chemical Bond

An equivariant feature may encode geometry associated with an interatomic environment.

It does not by itself establish electronic bonding.

Therefore:

`equivariant feature ≠ chemical bond`

## 91. Interatomic Representation Is Not Mechanical Force

A representation may contribute to a later force model.

It is not itself a force unless a force mapping explicitly defines that interpretation.

Therefore:

`interatomic representation ≠ mechanical force`

## 92. Symmetry Is Not Dynamics

Transformation behavior describes how representations change under transformed descriptions of a system.

It does not define how the system evolves through physical or computational time.

Therefore:

`symmetry action ≠ dynamical evolution`

## 93. Equivariance Is Not Conservation

Equivariance constrains transformation behavior.

A conservation law constrains evolution or admissible state relations.

Therefore:

`equivariance ≠ conservation law`

A model may be equivariant without conserving energy.

## 94. Equivariance Is Not Physical Correctness

A mapping can satisfy an exact equivariance relation while representing an incorrect physical law.

Therefore:

`equivariance PASS ≠ physical validation`

Equivariance is one structural requirement among several possible validation dimensions.

## 95. Locality Is Not Physical Sufficiency

A local representation may be computationally useful while omitting relevant long-range physics.

Therefore:

`local representation ≠ complete physical model`

The applicability of a locality assumption is model-relative and requires validation.

## 96. Representation Completeness

A representation `Φ_EIF` is complete with respect to a declared equivalence relation only if equivalent representation values imply equivalence of source configurations under that declared relation.

Formally, if:

`Φ_EIF(q_1) = Φ_EIF(q_2)`

then completeness requires:

`q_1 ~ q_2`

for the selected equivalence relation `~`.

Completeness must not be claimed without proof or test appropriate to the representation.

## 97. Representation Injectivity

Injectivity is stronger than many practical representation requirements.

A representation may intentionally identify configurations related by declared symmetry.

Therefore the relevant mathematical object may be injectivity on equivalence classes rather than injectivity on raw coordinates.

## 98. Quotient-Space Boundary

If configurations related by a declared symmetry are treated as physically equivalent for a specific task, the corresponding representation may operate effectively on equivalence classes.

The equivalence relation must be defined before such quotient reasoning is used.

The framework must not quotient out transformations whose effects are physically relevant to the target output.

## 99. Chirality Boundary

Reflection-sensitive structures require special care.

If reflections are treated as equivalent by a representation, chirality information may be lost.

An `O(3)`-invariant representation and an `SO(3)`-invariant representation therefore need not retain the same physical distinctions.

## 100. Parity Boundary

When improper rotations are included, representation channels may require parity labels or equivalent transformation semantics.

Two channels with the same rotational degree under `SO(3)` may transform differently under reflection.

Parity must not be omitted when the declared transformation group requires it.

## 101. Global Representation

Let:

`Φ_global: Q → Y_global`

be a global representation mapping.

A global representation may aggregate site-level information.

It must state:

- whether it is invariant or equivariant;
- what transformations are included;
- what site information is retained;
- what information is lost.

## 102. Local-to-Global Mapping

Let:

`A_global: Y_1 × ... × Y_N → Y_global`

be a declared aggregation mapping.

The global representation is:

`h_global = A_global(h_1, ..., h_N)`

A many-to-one aggregation does not allow reconstruction of all local representations.

Therefore:

`global representation ≠ complete local representation set`

in general.

## 103. Multiscale EIF Representation

EIF may support multiple geometric scales.

Let:

`L_EIF`

be a declared scale index set.

For each scale `ell ∈ L_EIF`, define representation space:

`Y_EIF,ell`

The complete multiscale representation may belong to:

`Y_EIF,MS = ∏_(ell ∈ L_EIF) Y_EIF,ell`

Scale identity must remain explicit.

## 104. Cross-Scale Mapping

A cross-scale EIF mapping:

`A_(ell→m): Y_EIF,ell → Y_EIF,m`

must define:

- source scale;
- target scale;
- aggregation or expansion rule;
- locality;
- symmetry behavior;
- information loss.

Scale aggregation does not automatically preserve all fine-scale information.

## 105. Dynamic EIF State

An EIF specialization may later include time-dependent or step-dependent interatomic representations.

If:

`q(t) ∈ Q`

then:

`Φ_EIF(q(t))`

is a time-indexed representation only through the time dependence of the configuration unless the representation itself has additional retained dynamics.

A static representation and a dynamical latent state are different objects.

## 106. History-Dependent EIF Representation

If an EIF representation depends on prior configurations, define an appropriate history space:

`H_EIF`

and mapping:

`Φ_EIF,H: H_EIF → Y_EIF`

The history dependence must not be hidden inside an apparently memoryless configuration mapping.

## 107. State and Representation Separation

The interatomic state and its representation remain distinct:

`q ∈ Q`

`h_EIF ∈ Y_EIF`

with:

`h_EIF = Φ_EIF(q)`

when the representation is memoryless.

Therefore:

`q ≠ h_EIF`

unless a particular representation is explicitly defined as the state itself.

## 108. Target and Prediction Separation

If a learned EIF realization predicts a quantity:

`ŷ`

from a reference target:

`y`

then:

`ŷ ≠ y`

as mathematical objects during validation.

Prediction error must remain independently observable.

A model output does not become reference truth because it is deterministic.

## 109. Training Boundary

Training is an implementation procedure for selecting model parameters.

It is not part of the universal mathematical definition of equivariance.

A mapping may be equivariant:

- analytically by construction;
- numerically within tolerance;
- approximately;
- not at all.

Its training procedure does not decide the definition.

## 110. Dataset Boundary

A dataset is evidence or parameter-estimation input.

It is not the atomic configuration space itself.

Therefore:

`dataset ≠ Q`

and:

`training distribution ≠ full model domain`

Generalization outside the sampled dataset requires independent evaluation.

## 111. Numerical Equivariance Test

For transformation `g`, input `x`, mapping `F`, and declared output action, define an equivariance residual in an appropriate normed output space as:

`e_eq = ||F(ρ_X(g)x) - ρ_Y(g)F(x)||`

A numerical test may require:

`e_eq ≤ epsilon_eq`

where:

`epsilon_eq ≥ 0`

is a numerical tolerance.

The exact mathematical definition remains:

`e_eq = 0`

## 112. Exact and Numerical Equivariance Are Distinct

The distinction is:

`exact equivariance ≠ numerical equivariance within tolerance`

A floating-point implementation may satisfy only a numerical comparison even when the underlying architecture is analytically equivariant.

The tolerance belongs to the numerical validation layer.

## 113. Permutation Equivariance Test

For site-indexed output `F(q)`, permutation equivariance requires:

`F(π · q) = π · F(q)`

under the declared permutation actions.

A scalar global output may instead be permutation invariant:

`F(π · q) = F(q)`

The required relation depends on the output type.

## 114. Translation Test

A translation-invariant scalar output `F` satisfies:

`F(T_a q) = F(q)`

where `T_a` is the declared global translation action.

A position-like equivariant output requires its own nontrivial translation action.

The output semantics determine the correct relation.

## 115. Rotation Test

For rotation `R`, a rotationally invariant scalar output satisfies:

`F(R · q) = F(q)`

A vector output satisfies the corresponding equivariant relation:

`F(R · q) = R · F(q)`

when the output action is the standard vector action.

## 116. Reflection Test

If the declared group includes reflections, validation must test the appropriate parity behavior.

Passing only proper-rotation tests is insufficient to establish full `O(3)` or `E(3)` behavior.

## 117. Composition Validation

If a complete EIF realization is composed of several mappings:

`F_n ∘ ... ∘ F_2 ∘ F_1`

then a global equivariance claim requires compatible transformation behavior across the complete composition.

One equivariant submodule does not make an arbitrary full pipeline equivariant.

## 118. Graph Construction Equivariance

If graph construction depends only on transformation-invariant geometric criteria such as pair distance and treats ties consistently, the graph relation may be preserved under rigid Euclidean transformations.

However, a graph construction algorithm must be validated independently.

A coordinate-sensitive or numerically unstable graph rule may break the intended correspondence.

## 119. Cutoff Boundary Events

When an interatomic distance is near a hard cutoff, a small geometric perturbation may add or remove an edge.

This is a topology change in the computational interaction graph.

It is not automatically:

- a physical structural transition;
- a chemical bond transition;
- a bifurcation;
- a TR ternary transition.

## 120. Smoothness Boundary

If differentiable energy or force outputs are required, discontinuities in neighborhood construction or representation may affect differentiability.

Equivariance alone does not guarantee smoothness.

Therefore:

`equivariance ≠ differentiability`

## 121. Continuity Boundary

A mapping may be exactly equivariant yet discontinuous.

Continuity must be established separately when required.

Similarly:

`continuity ≠ differentiability`

## 122. Local Environment Identity

A local environment must retain the identity of its central site or define explicitly why the central site is not distinguished.

Central-site and neighbor roles must not be silently exchanged.

## 123. Ordered Pair Semantics

For an ordered pair representation:

`h_ij`

the first and second indices have distinct roles.

Therefore:

`h_ij ≠ h_ji`

in general.

Equality requires an independently defined symmetry of that representation.

## 124. Many-Body Representation

An interatomic representation may depend jointly on more than two sites.

Many-body dependence does not require an explicit enumeration of fixed-order tuples if the architecture encodes such dependence through another declared construction.

The mathematical dependency scope must nevertheless be identifiable.

## 125. Pairwise Is Not Universal

EIF does not assume that all interatomic information is reducible to pairwise additive interactions.

Therefore:

`interatomic framework ≠ pair potential`

A pairwise specialization is one possible restricted model class.

## 126. Energy Decomposition Boundary

If a future potential model writes total energy as a sum of atomic or local contributions, that decomposition is a model construction.

Individual local energy contributions need not be uniquely defined by the underlying physics.

Only the declared total model output carries the exact semantics assigned by that model.

## 127. Learned Representation Boundary

Equivariant learned representations can encode information relevant to atomistic prediction while remaining difficult to interpret physically channel by channel.

No semantic promotion is allowed from:

`useful latent feature`

to:

`identified physical mechanism`

without independent evidence.

## 128. Classical Reference: Tensor Field Networks

Thomas et al. introduced Tensor Field Networks as neural networks for three-dimensional point clouds with local equivariance to rotations, translations, and point permutations.

The work provides a classical computational reference for geometric tensor features and transformation-aware operations.

This reference supports the general concept that non-scalar internal features can transform predictably under spatial transformations.

It does not define TR-EIF or EIF.

Provenance:

`PRIMARY_SOURCE`

## 129. Classical Reference: NequIP

Batzner et al. introduced Neural Equivariant Interatomic Potentials using E(3)-equivariant graph neural networks for atomistic energy and force modeling.

The work explicitly distinguishes invariant energy output from internal equivariant geometric tensor features.

This provides a primary interatomic reference for E(3)-equivariant atomistic representation.

It does not define the EIF architecture used by TR-EIF.

Provenance:

`PRIMARY_SOURCE`

## 130. Classical Reference: e3nn

Geiger and Smidt describe e3nn as a framework for constructing E(3)-equivariant functions from composable equivariant operations.

This provides a computational reference for representation-theoretic construction of Euclidean neural networks.

EIF does not depend on e3nn as a required implementation.

Provenance:

`PRIMARY_SOURCE`

## 131. Classical Reference: Allegro

Musaelian et al. introduced Allegro as a strictly local equivariant interatomic-potential architecture using learned equivariant representations.

The work provides a primary reference for the distinction between strict locality and atom-centered message-passing architectures in equivariant atomistic modeling.

EIF does not adopt Allegro as its universal computational form.

Provenance:

`PRIMARY_SOURCE`

## 132. Established Literature Boundary

The referenced architectures demonstrate that:

- atomistic representations can be designed with explicit Euclidean transformation behavior;
- invariant and equivariant channels can coexist;
- local equivariant representations can be used in interatomic models;
- scalar invariant energy outputs can coexist with equivariant internal features.

They do not establish:

- universal completeness of one representation;
- universal physical accuracy;
- universal locality;
- universal force laws;
- TR-EIF resonance mappings;
- balanced ternary semantics.

## 133. EIF Formal State Chain

The foundational EIF chain is:

`atomic identities + atomic geometry`

`→ configuration q ∈ Q`

`→ interaction topology G`

`→ local environments E_i`

`→ geometric and identity features`

`→ invariant / equivariant representation`

`→ local / global / multiscale EIF state`

The chain ends here for the present foundational chapter.

No resonance mapping is inserted into this chain yet.

## 134. Representation Contract

Every EIF representation must define:

1. source configuration space;
2. atomic identity domain;
3. spatial dimension;
4. boundary conditions;
5. interaction topology;
6. locality rule;
7. representation codomain;
8. transformation group or transformation set;
9. input action;
10. output action;
11. permutation behavior;
12. translation behavior;
13. rotation behavior;
14. reflection behavior where applicable;
15. dimensional status;
16. information retained;
17. information lost;
18. numerical representation if executable;
19. validation relation.

## 135. Local Environment Contract

Every local-environment mapping must define:

1. central-site identity;
2. neighbor membership;
3. geometry convention;
4. periodic convention where applicable;
5. ordering semantics;
6. topology semantics;
7. included species information;
8. included continuous state;
9. excluded state;
10. transformation behavior.

## 136. Equivariance Contract

Every EIF equivariance claim must define:

1. group or transformation set `G`;
2. domain `X`;
3. codomain `Y`;
4. input action `ρ_X`;
5. output action `ρ_Y`;
6. mapping `F`;
7. exact relation:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

8. admissible domain of `x`;
9. admissible transformations `g`;
10. numerical tolerance if only numerical validation is claimed.

## 137. Invariance Contract

Every EIF invariance claim must define:

1. transformation set;
2. input action;
3. mapping;
4. output semantics;
5. exact invariance relation;
6. numerical validation tolerance where applicable.

The word `invariant` must not be used without identifying what transformation leaves the output unchanged.

## 138. Permutation Contract

Every atom-index permutation claim must define:

- permutation domain;
- action on positions;
- action on identities;
- action on topology;
- action on local features;
- action on outputs.

Permutation of storage order must preserve all corresponding indexed state.

## 139. Physical-Output Contract

Before EIF exposes a physical output such as energy, force, or stress, the model must define:

- output space;
- physical units;
- transformation behavior;
- mapping from EIF representation;
- physical interpretation;
- provenance;
- validation criterion.

No latent representation satisfies this contract automatically.

## 140. Information-Loss Contract

For every mapping:

`F: X → Y`

that is relevant to physical or integration semantics, the model must identify whether the mapping is:

- injective;
- many-to-one;
- invertible on its image;
- deliberately invariant to a declared equivalence relation;
- information-reducing in another defined way.

Unknown information loss must not be treated as proven preservation.

## 141. EIF Validation Classes

EIF validation must separate at least:

- type validation;
- topology validation;
- permutation validation;
- translation validation;
- rotation validation;
- reflection or parity validation where applicable;
- locality validation;
- numerical equivariance validation;
- physical-output validation where outputs exist;
- empirical validation where physical data are claimed.

These validation classes are not interchangeable.

## 142. Type Validation

Type validation checks that every EIF object belongs to its declared space.

Examples include:

- valid atomic identity;
- valid coordinate dimension;
- valid node index;
- valid edge index;
- valid representation channel;
- valid tensor or feature type.

## 143. Topology Validation

Topology validation checks:

- valid nodes;
- valid edges;
- allowed self-edge behavior;
- directionality;
- neighborhood rule;
- boundary handling;
- consistency under reindexing.

Topology validity does not prove physical validity.

## 144. Permutation Validation

Permutation validation checks whether the model preserves the declared permutation relation.

For a site-indexed equivariant output, this requires correspondence under relabeling.

For a global invariant output, this requires equality under allowed reordering.

## 145. Geometric Validation

Geometric validation checks the declared response to:

- translation;
- rotation;
- reflection where applicable.

Each transformation class must be evaluated separately.

Passing rotation validation does not imply passing translation or permutation validation.

## 146. Representation Validation

Representation validation checks whether the encoded representation satisfies its declared mathematical properties.

This may include:

- equivariance;
- invariance;
- locality;
- continuity;
- completeness relative to a declared equivalence;
- numerical stability.

No one property implies all others.

## 147. Physical Validation Boundary

Physical validation begins only when the EIF layer asserts a physical output.

For such a claim, symmetry validation is necessary only to the extent required by the physical semantics.

It is not sufficient alone.

## 148. Provenance

The following provenance classes inherited from Volume 01 remain mandatory:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

Every numerical cutoff, learned parameter, empirical coefficient, or validation tolerance must carry the appropriate provenance.

## 149. No Universal Cutoff

EIF defines no universal neighbor cutoff.

Therefore:

`r_c`

is always specialization-dependent when used.

It must not be promoted to a universal physical constant.

## 150. No Universal Representation Dimension

EIF defines no universal number of scalar, vector, tensor, latent, radial, angular, or channel features.

Representation dimensionality belongs to the model realization.

## 151. No Universal Maximum Angular Order

EIF defines no universal maximum angular representation order.

Any truncation or maximum order is an implementation or specialization choice with its own accuracy and computational consequences.

## 152. No Universal Interaction Depth

EIF defines no universal graph depth or message-passing depth.

Such depth is architecture-specific.

Strictly local architectures may use a different information-propagation structure entirely.

## 153. No Universal Energy Model

EIF defines no universal energy functional in this foundational chapter.

Any later energy model must be introduced as a separately typed mapping.

## 154. No Universal Force Model

EIF defines no universal force equation in this foundational chapter.

Any later force relation must be derived from or connected to an independently defined physical model.

## 155. No Automatic Machine-Learning Requirement

The mathematical EIF layer does not require that its mappings be learned.

A conforming realization may contain:

- analytic mappings;
- learned mappings;
- hybrid mappings;
- tabulated mappings;
- algorithmic geometric transforms.

Equivariance is a property of the mapping, not of whether it was learned.

## 156. No Automatic Neural-Network Requirement

EIF does not require a neural network.

Therefore:

`EIF ≠ neural network`

A neural architecture is one possible computational realization.

## 157. No Automatic Graph Requirement

Although graph structures are natural for many atomistic models, a graph is not mandatory unless the specialization defines one.

Therefore:

`EIF ≠ graph representation only`

The framework allows other explicitly typed interatomic structures.

## 158. No Automatic Three-Dimensional Restriction

The primary interatomic use case is three-dimensional space.

However, the mathematical foundations distinguish general spatial dimension `d` from the specialization:

`d = 3`

Group definitions must correspond to the chosen dimension.

## 159. Fixed and Variable Cardinality Boundary

This chapter primarily formulates fixed `N` for clarity.

A variable-cardinality EIF model must additionally define:

- site creation;
- site removal;
- identity assignment;
- reindexing;
- topology reconstruction;
- transformation correspondence;
- trace correspondence.

No variable-cardinality behavior is implied by fixed-size notation.

## 160. EIF and TR Boundary

The closed TR layer established the output space:

`Y_TR,out`

The present EIF chapter establishes the beginning of the independent interatomic side through:

`Q`

`X_G`

`X_env`

`Y_EIF`

No mapping between:

`Y_EIF`

and:

`X_TR,in`

is defined in this chapter.

## 161. Integration Is Deliberately Deferred

The eventual TR-EIF architecture requires:

`interatomic state`

`→ equivariant representation`

`→ resonant state`

`→ ternary state`

and, where defined:

`ternary / resonant state`

`→ interatomic update`

This chapter defines only the mathematical source side required for the first arrows.

It does not create those arrows prematurely.

## 162. Future Integration Must Preserve Equivariance

When an EIF representation later enters the TR layer, the integration mapping must state what happens to the transformation semantics.

An equivariant EIF representation cannot be connected to an arbitrary TR input mapping while retaining an equivariance claim automatically.

The cross-layer mapping itself must satisfy the required transformation relation.

## 163. Future Feedback Must Preserve Type Semantics

If TR state later feeds back into EIF, the feedback mapping must specify:

- which EIF object is modified;
- the transformation behavior;
- locality;
- dimensional meaning;
- information source;
- physical interpretation.

A ternary value must not be added directly to a coordinate, force, or energy without a typed mapping.

## 164. Ternary State Remains Separate

The balanced ternary domain remains:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and active state:

`0`

This domain is not part of the foundational EIF configuration space unless a later integration model explicitly includes it.

## 165. No Geometry-to-Ternary Shortcut

The following direct inference is forbidden:

`geometry → -1/0/1`

unless an explicit typed mapping is defined.

Translation, rotation, reflection, or permutation does not automatically determine ternary polarity.

## 166. No Equivariance-to-Resonance Shortcut

The following implication is forbidden:

`equivariant representation → resonance`

Equivariance describes transformation behavior.

Resonance belongs to the separately defined TR formalism.

The relation between them requires an explicit mapping.

## 167. No Phase-to-Bond Shortcut

The Volume 02 boundary remains:

`phase relation ≠ chemical bond`

The EIF layer does not reinterpret that statement.

A later integrated model must retain the distinction.

## 168. No Resonance-to-Force Shortcut

The Volume 02 boundary remains:

`resonance ≠ force`

EIF does not supply a missing force law merely by introducing geometry or equivariant representations.

A force mapping must remain independently defined.

## 169. EIF Core Invariants

The following invariants are mandatory.

1. `EIF` means Equivariant Interatomic Framework.

2. EIF remains distinct from the closed TR layer.

3. Atomic site index remains distinct from atomic identity.

4. Atomic identity remains distinct from coordinate.

5. Configuration remains distinct from representation.

6. Local environment remains distinct from descriptor.

7. Geometry remains distinct from topology.

8. Graph edge remains distinct from chemical bond.

9. Relative displacement remains distinct from distance.

10. Translation remains distinct from rotation.

11. Rotation remains distinct from permutation.

12. Proper rotations remain distinct from reflections.

13. `SO(3)` remains distinct from `O(3)`.

14. `SE(3)` equivariance remains distinct from `E(3)` equivariance.

15. Invariance remains distinct from equivariance.

16. Every equivariance claim defines input and output actions.

17. Permutation invariance remains distinct from permutation equivariance.

18. Species identity is preserved under computational reindexing.

19. Geometric transformation does not alter species identity.

20. Geometric transformation does not automatically alter ternary polarity.

21. Scalar representation remains distinct from vector representation.

22. Higher-order representation channels retain declared transformation types.

23. Global representation remains distinct from complete local-state information.

24. Locality remains model-relative.

25. Equivariance remains distinct from locality.

26. Equivariance remains distinct from continuity.

27. Equivariance remains distinct from differentiability.

28. Equivariance remains distinct from conservation.

29. Equivariance remains distinct from physical correctness.

30. Latent representation remains distinct from physical observable.

31. Equivariant feature remains distinct from force.

32. Equivariant feature remains distinct from energy.

33. Equivariant feature remains distinct from chemical bond.

34. No universal cutoff is defined.

35. No universal representation size is defined.

36. No universal force law is defined.

37. No universal energy model is defined.

38. Information loss must remain explicit.

39. Numerical equivariance tolerance remains distinct from exact equivariance.

40. TR-EIF integration requires explicit cross-layer mappings.

## 170. Formal Non-Equivalences

The following non-equivalences are mandatory:

`EIF ≠ TR`

`EIF ≠ FRP`

`EIF ≠ NequIP`

`EIF ≠ Allegro`

`EIF ≠ Tensor Field Networks`

`EIF ≠ e3nn`

`EIF ≠ neural network`

`EIF ≠ graph neural network`

`EIF ≠ interatomic potential only`

`computational index ≠ atomic identity`

`atomic identity ≠ atomic coordinate`

`configuration ≠ representation`

`local environment ≠ descriptor`

`geometry ≠ topology`

`neighbor edge ≠ chemical bond`

`relative displacement ≠ distance`

`translation ≠ rotation`

`translation ≠ permutation`

`rotation ≠ permutation`

`SO(3) ≠ O(3)`

`SE(3) ≠ E(3)`

`invariance ≠ equivariance`

`permutation invariance ≠ permutation equivariance`

`locality ≠ equivariance`

`equivariance ≠ continuity`

`equivariance ≠ differentiability`

`equivariance ≠ conservation law`

`equivariance ≠ physical validation`

`latent feature ≠ physical observable`

`equivariant feature ≠ mechanical force`

`equivariant feature ≠ energy`

`equivariant feature ≠ chemical bond`

`interatomic geometry ≠ resonance state`

`equivariant representation ≠ resonance coordinate`

`atomic position ≠ oscillator phase`

`geometry transformation ≠ ternary polarity change`

`TR state ≠ EIF state`

## 171. Minimal EIF Foundation Contract

A minimally specified EIF model must define:

1. atomic-site set;
2. atomic-identity domain;
3. configuration space;
4. spatial dimension;
5. boundary conditions;
6. relative-geometry mappings;
7. topology representation if topology is used;
8. local-environment mapping;
9. representation space;
10. transformation group or transformation set;
11. transformation action on configurations;
12. transformation action on representations;
13. permutation behavior;
14. translation behavior;
15. rotation behavior;
16. reflection behavior where relevant;
17. locality;
18. information-loss properties;
19. dimensional status;
20. validation conditions.

## 172. Foundation Conformance Requirements

An EIF mathematical realization conforms to this chapter when:

- every atomic identity is typed;
- every coordinate belongs to the declared spatial domain;
- configuration and representation spaces are distinct;
- all topology is explicitly defined;
- every local environment has a declared extraction rule;
- every invariant claim identifies its transformation;
- every equivariant claim identifies both transformation actions;
- permutation, translation, rotation, and reflection semantics are not collapsed;
- information loss is explicit;
- physical semantics are not inferred from latent representation alone;
- energy, force, stress, and bond meanings are introduced only through independent definitions;
- no TR state is inserted into EIF without a typed integration mapping.

## 173. Primary Sources

The classical and computational symmetry statements used in this chapter are consistent with the following primary sources.

1. Thomas, N., Smidt, T., Kearnes, S., Yang, L., Li, L., Kohlhoff, K., and Riley, P. "Tensor Field Networks: Rotation- and Translation-Equivariant Neural Networks for 3D Point Clouds." arXiv:1802.08219, 2018. https://arxiv.org/abs/1802.08219

2. Batzner, S., Musaelian, A., Sun, L., Geiger, M., Mailoa, J. P., Kornbluth, M., Molinari, N., Smidt, T. E., and Kozinsky, B. "E(3)-Equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials." Nature Communications 13, 2453, 2022. https://doi.org/10.1038/s41467-022-29939-5

3. Geiger, M., and Smidt, T. "e3nn: Euclidean Neural Networks." arXiv:2207.09453, 2022. https://arxiv.org/abs/2207.09453

4. Musaelian, A., Batzner, S., Johansson, A., Sun, L., Owen, C. J., Kornbluth, M., and Kozinsky, B. "Learning Local Equivariant Representations for Large-Scale Atomistic Dynamics." Nature Communications 14, 579, 2023. https://doi.org/10.1038/s41467-023-36329-y

These sources establish relevant classical and computational precedents.

TR-EIF-specific architecture, state separation, integration boundaries, and conformance rules remain author-defined framework structure.

## 174. Final Foundation Statement

The Equivariant Interatomic Framework begins from the represented interatomic configuration:

`q ∈ Q`

and constructs mathematically controlled representations through the chain:

`atomic identities + positions`

`→ relative geometry`

`→ interaction topology`

`→ local atomic environments`

`→ invariant and equivariant mappings`

`→ local / global / multiscale EIF representations`

Every transformation claim is defined through explicit actions.

Every representation has a declared domain and codomain.

Permutation, translation, rotation, and reflection remain independently specified.

Invariant and equivariant outputs remain distinct.

Representation and physical interpretation remain distinct.

EIF therefore provides the interatomic geometric and transformation-aware half of TR-EIF without reducing the framework to a particular neural architecture or potential model.

The Ternary Resonant layer remains independently defined and closed.

No direct identification is made between:

`interatomic geometry`

and:

`resonance state`

or between:

`equivariant representation`

and:

`ternary state`

The future integration layer can therefore connect:

`interatomic state`

`→ equivariant representation`

`→ resonant state`

`→ ternary state`

only through explicit typed mappings whose symmetry behavior, locality, information loss, dimensional meaning, and validation scope are independently defined.
