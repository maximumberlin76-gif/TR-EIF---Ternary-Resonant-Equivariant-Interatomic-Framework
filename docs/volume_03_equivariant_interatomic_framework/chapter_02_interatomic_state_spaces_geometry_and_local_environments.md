# Interatomic State Spaces, Geometry, and Local Environments

## 1. Purpose

This document formalizes the interatomic state spaces, geometric relations, topology construction, and local-environment semantics required by the Equivariant Interatomic Framework layer of TR-EIF.

The chapter develops the chain:

`interatomic system`

`→ configuration state`

`→ relative geometry`

`→ boundary-aware geometry`

`→ interaction topology`

`→ local atomic environment`

`→ environment state`

without yet defining the complete invariant or equivariant representation architecture.

The chapter establishes:

- fixed-cardinality and variable-cardinality interatomic configuration spaces;
- atomic identity and position state;
- optional physical state extensions;
- periodic-cell state;
- relative displacement and distance;
- boundary-aware displacement;
- neighborhood construction;
- graph topology;
- local-environment extraction;
- central-site and neighbor semantics;
- ordered and unordered interaction relations;
- species-aware environments;
- geometric degeneracy;
- cutoff and topology boundaries;
- locality;
- environment equivalence;
- information-preservation requirements;
- transformation behavior of configuration and environment state;
- the exact boundary between physical configuration, computational topology, and later EIF representations.

The purpose is to establish the source spaces on which later invariant and equivariant mappings operate.

## 2. Dependency

This chapter depends on:

- Volume 01, Mathematical Foundations;
- Volume 02, Ternary Resonance Theory;
- Volume 03, Chapter 01, Equivariant Interatomic Foundations.

It inherits without redefinition:

- configuration space `Q`;
- atomic-site set `V`;
- atomic identity domain `Z`;
- atomic identity `z_i`;
- atomic position `x_i`;
- topology state space `X_G`;
- local-environment space `X_env`;
- Euclidean transformation semantics;
- permutation semantics;
- invariance and equivariance definitions;
- information-loss requirements;
- provenance classes;
- validation boundaries.

The closed Ternary Resonant layer remains unchanged.

## 3. Scientific Status Classes

### 3.1 CLASSICAL

The following structures use standard mathematical and atomistic-modeling concepts:

- Cartesian configuration spaces;
- Euclidean distance;
- relative displacement;
- periodic-cell geometry;
- graph neighborhoods;
- permutation of indexed particles;
- local atomic environments;
- geometric cutoff neighborhoods.

### 3.2 EIF FORMAL / AUTHOR-DEFINED

The following are author-defined EIF architecture:

- the exact separation between configuration, topology, environment, and representation state;
- the environment-state contracts;
- topology provenance requirements;
- locality contracts;
- degeneracy handling requirements;
- boundary-aware environment construction requirements;
- information-preservation requirements;
- EIF conformance conditions.

### 3.3 DERIVED

Relations obtained directly from the declared state spaces and mappings are classified as:

`DERIVED`

### 3.4 EMPIRICAL / CALIBRATED

Numerical neighborhood radii, material-specific geometric thresholds, empirical coordination criteria, and physical structural classifications require independent provenance.

### 3.5 UNVERIFIED

A geometric or topological relation must not be promoted automatically to:

- chemical bond;
- force interaction;
- resonance;
- structural phase;
- physical phase transition;
- energetic relation.

Such interpretations require independent definitions.

## 4. EIF Source-Space Principle

The EIF layer begins from an explicitly represented interatomic state.

Representations are downstream objects.

The required order is:

`interatomic state`

`→ geometric relations`

`→ topology`

`→ local environments`

`→ representation`

Therefore:

`representation ≠ source state`

and:

`local descriptor ≠ local environment`

## 5. Atomic-Site Set

For a fixed-cardinality system containing `N ≥ 1` represented atomic sites, define:

`V_N = {1, 2, ..., N}`

The site index:

`i ∈ V_N`

is a computational identifier.

It is not a physical atomic property.

## 6. Atomic Identity Domain

Let:

`Z`

denote the declared atomic-identity domain.

For each site:

`z_i ∈ Z`

The interpretation of `z_i` must be fixed by the specialization.

Possible interpretations include:

- atomic number;
- chemical species label;
- coarse species category;
- another explicitly declared identity class.

The identity domain must not be inferred from numeric storage format alone.

## 7. Position Space

Let the spatial dimension be:

`d ∈ ℕ`

with:

`d ≥ 1`

The position of site `i` belongs to:

`x_i ∈ ℝ^d`

For ordinary three-dimensional atomistic systems:

`d = 3`

## 8. Position Configuration

For fixed `N`, define:

`Q_pos,N = (ℝ^d)^N`

A position configuration is:

`X = (x_1, ..., x_N) ∈ Q_pos,N`

This state contains positions only.

It does not include atomic identities automatically.

## 9. Identity Configuration

The corresponding identity configuration is:

`Z_N = (z_1, ..., z_N) ∈ Z^N`

The identities and positions remain distinct:

`Z_N ≠ X`

## 10. Minimal Interatomic Configuration

A minimal fixed-cardinality interatomic configuration may be represented as:

`q = ((z_1, x_1), ..., (z_N, x_N))`

with:

`q ∈ Q_N`

where:

`Q_N ⊆ (Z × ℝ^d)^N`

The subset relation permits a specialization to exclude invalid configurations.

## 11. Admissible Configuration Space

Define:

`Q_N,adm ⊆ Q_N`

as the admissible configuration subset.

A specialization must define any exclusions.

Possible exclusions include:

- coincident sites;
- forbidden identity assignments;
- invalid cell state;
- prohibited boundary states;
- unsupported cardinality;
- physically or computationally invalid geometry.

Invalidity must not be inferred silently.

## 12. Configuration and Physical State

The configuration `q` is the represented interatomic configuration.

It is not necessarily the complete physical state of a material system.

Additional physical variables may be required.

Therefore:

`interatomic configuration ≠ complete physical state`

in general.

## 13. Extended Interatomic State

Let:

`X_ext`

denote a declared auxiliary state space.

An extended state may be represented as:

`s_EIF = (q, ξ)`

with:

`q ∈ Q_N,adm`

and:

`ξ ∈ X_ext`

The auxiliary state may contain explicitly declared variables such as:

- velocity;
- charge;
- spin;
- occupancy;
- electronic-state proxy;
- cell state;
- external fields;
- constraints;
- dynamic topology state.

No such variable is implicit.

## 14. Velocity State

If velocities are represented, define:

`v_i ∈ ℝ^d`

and:

`V_state = (v_1, ..., v_N) ∈ (ℝ^d)^N`

Position and velocity remain different state components:

`X ≠ V_state`

## 15. Dynamical Interatomic State

A dynamical atomistic state may therefore contain:

`s_dyn = (q, V_state, ξ_dyn)`

where:

`ξ_dyn`

contains any additional declared dynamical variables.

This state is distinct from oscillator phase state defined in the TR layer.

## 16. Variable Cardinality

A variable-cardinality EIF model cannot be represented by one fixed Cartesian product alone.

Define a cardinality set:

`N_adm ⊆ ℕ`

For each:

`N ∈ N_adm`

let:

`Q_N,adm`

be the corresponding admissible configuration space.

A variable-cardinality configuration domain may be represented as the disjoint collection:

`Q_var = ⋃_(N ∈ N_adm) Q_N,adm`

with cardinality retained as part of state identity.

## 17. Cardinality Is State Information

For variable-cardinality models:

`N`

is result-affecting state information.

Site creation or removal must therefore be represented explicitly.

Silent array resizing is not an admissible state transition semantics.

## 18. Site Creation

A site-creation operation must define:

- new identity;
- new position;
- new computational index or reindexing rule;
- topology update;
- local-environment update;
- provenance of the event.

Site creation is not implied by a topology edge appearing.

## 19. Site Removal

A site-removal operation must define:

- removed site identity;
- removal condition;
- reindexing behavior;
- topology update;
- local-environment update;
- trace correspondence.

Deleting one array row without updating dependent indexed state is invalid.

## 20. Computational Reindexing

A reindexing changes computational labels while preserving the represented configuration under the declared permutation relation.

Therefore:

`reindexing ≠ physical motion`

`reindexing ≠ species change`

`reindexing ≠ atom creation`

`reindexing ≠ atom removal`

## 21. Species Preservation Under Reindexing

Let:

`π ∈ S_N`

be a permutation.

Under consistent reindexing:

`z_i' = z_(π⁻¹(i))`

and:

`x_i' = x_(π⁻¹(i))`

The identity-position pairing remains preserved.

## 22. Relative Displacement

For ordered sites `i` and `j`, define:

`r_ij = x_j - x_i`

with:

`r_ij ∈ ℝ^d`

For ordinary non-periodic Euclidean geometry:

`r_ji = -r_ij`

## 23. Pair Distance

Define:

`d_ij = ||r_ij||`

with:

`d_ij ∈ ℝ_≥0`

Then:

`d_ij = d_ji`

while the corresponding relative vectors retain orientation.

## 24. Pair Identity

A pair relation must specify whether it is ordered.

An ordered pair is:

`(i, j)`

An unordered pair is:

`{i, j}`

These are different mathematical objects.

## 25. Ordered Pair Geometry

For an ordered pair:

`(i, j)`

the relative vector is:

`r_ij`

Changing order changes the vector:

`r_ji = -r_ij`

for ordinary Euclidean displacement.

## 26. Unordered Pair Geometry

For an unordered pair:

`{i, j}`

a symmetric scalar such as distance may be attached consistently because:

`d_ij = d_ji`

An oriented vector cannot be assigned to an unordered pair without an additional orientation convention.

## 27. Coincident Sites

If:

`x_i = x_j`

for:

`i ≠ j`

then:

`d_ij = 0`

A model must state whether such configurations are:

- admissible;
- singular;
- rejected;
- regularized.

No universal rule is imposed.

## 28. Geometric Degeneracy

A geometric construction is degenerate when the mathematical object needed by the mapping loses the properties required by its definition.

Examples include:

- zero-length displacement;
- collinear triplets where a nonzero normal is required;
- coplanar configurations where a volume orientation is required;
- equal-distance ties in a ranking rule;
- vanishing local-frame basis vectors.

Degenerate cases require explicit handling.

## 29. Pair Angle Input

For nonzero vectors:

`r_ij`

and:

`r_ik`

an angular cosine may be defined as:

`c_jik = (r_ij · r_ik) / (d_ij d_ik)`

The definition requires:

`d_ij > 0`

and:

`d_ik > 0`

## 30. Angular Value Range

For valid Euclidean vectors:

`c_jik ∈ [-1, 1]`

Numerical implementations may require controlled handling of roundoff outside this interval.

The mathematical range itself remains exact.

## 31. Angle Is Not Orientation

An angle or angular cosine does not preserve all orientation information.

Two reflected environments may share the same pair distances and angular cosines.

Therefore:

`angular invariant ≠ complete oriented geometry`

## 32. Higher-Order Geometry

A local environment may require geometric relations involving more than two neighbors.

Examples include:

- triplet relations;
- oriented triple products;
- local volume elements;
- higher-order neighborhood correlations.

Such quantities require separately typed mappings.

## 33. Boundary Condition Space

Let:

`X_B`

denote the declared geometric boundary-condition space.

A boundary state satisfies:

`b ∈ X_B`

Boundary conditions may affect relative geometry and topology.

They are therefore part of the model contract when present.

## 34. Non-Periodic Boundary

For a non-periodic configuration, the direct displacement:

`r_ij = x_j - x_i`

may be sufficient for geometric relations within the represented domain.

No periodic image relation is implied.

## 35. Periodic Cell

For a periodic three-dimensional system, let the cell matrix be:

`H ∈ ℝ^(3×3)`

with:

`det(H) ≠ 0`

The columns or rows used as lattice vectors must be fixed by the selected convention.

The convention must not remain implicit.

## 36. Fractional Coordinates

A Cartesian position may be related to fractional coordinate:

`s_i ∈ ℝ^3`

through a declared convention such as:

`x_i = H s_i`

The model must use one consistent cell convention.

## 37. Periodic Equivalence

Under periodic boundary conditions, fractional coordinates related by an integer lattice vector describe periodic images:

`s_i ~ s_i + n`

for:

`n ∈ ℤ^3`

The equivalence relation belongs to the periodic geometry definition.

## 38. Periodic Displacement

A periodic pair displacement requires an image-selection rule.

A generic image displacement may be written:

`r_ij,n = H(s_j - s_i + n)`

with:

`n ∈ ℤ^3`

A specific periodic displacement mapping selects an admissible image according to the declared rule.

## 39. Minimum-Image Boundary

A minimum-image rule is one possible periodic displacement convention.

It is not universally valid for every cell geometry, cutoff, or interaction model.

The specialization must define when the selected image rule is admissible.

## 40. Periodic Image Identity

A periodic image of site `j` is not an additional physical atom merely because it appears as a separate geometric neighbor record.

The environment representation must distinguish:

- physical site identity;
- periodic image identifier.

## 41. Cell Geometry Is State

When the cell may vary:

`H`

is state information.

A deformation of `H` is not equivalent to a rigid translation or rotation of all atoms.

## 42. Rigid Rotation of Cell and Coordinates

If a periodic configuration is rigidly rotated by:

`R ∈ SO(3)`

then a consistent transformation may require both:

`x_i' = R x_i`

and:

`H' = R H`

under the selected cell convention.

Rotating atoms while leaving a physically co-rotating cell unchanged numerically describes a different operation.

## 43. Cell Deformation

A general change:

`H → H'`

need not be a rigid Euclidean transformation.

It may represent strain or another deformation.

Therefore:

`cell deformation ≠ rigid rotation`

## 44. Geometry-State Space

Let:

`X_geom`

denote the declared geometric relation space derived from a configuration and boundary state.

A geometry extraction mapping may be typed as:

`G_geom: Q × X_B → X_geom`

The codomain must identify which geometric relations are retained.

## 45. Geometry Extraction Is a Mapping

The geometry extraction mapping may include:

- relative vectors;
- distances;
- angular relations;
- periodic-image data;
- cell-relative quantities.

It does not change the source configuration.

Therefore:

`geometry extraction ≠ state evolution`

## 46. Interaction Topology

Let:

`X_G`

denote the topology state space inherited from Volume 01.

A topology state is:

`G ∈ X_G`

A graph realization may be represented as:

`G = (V, E)`

with additional declared edge or node attributes where required.

## 47. Topology Construction

A topology-construction mapping is:

`G_C: Q × X_B × Λ_G → X_G`

where:

`Λ_G`

is the topology-parameter space.

This extends the simpler configuration-only mapping when boundary conditions or topology parameters affect construction.

## 48. Topology Parameters

Topology parameters may include:

- cutoff radii;
- neighbor-count limits;
- species-dependent rules;
- graph-direction rules;
- periodic-image restrictions;
- hysteresis parameters;
- adaptive-neighborhood parameters.

Every numerical parameter requires provenance.

## 49. Geometry and Topology Remain Distinct

The source configuration determines geometry under the boundary convention.

Topology is produced through a declared construction rule.

Therefore:

`geometry ≠ topology`

and:

`distance ≠ edge`

A distance may contribute to an edge decision without being the edge itself.

## 50. Cutoff Topology

For cutoff:

`r_c > 0`

one possible neighbor relation is:

`j ∈ N_i`

when:

`j ≠ i`

and:

`d_ij ≤ r_c`

under the declared boundary-aware distance.

This rule defines a computational neighborhood.

It does not define a chemical bond.

## 51. Open and Closed Cutoff Conventions

A model must distinguish between:

`d_ij < r_c`

and:

`d_ij ≤ r_c`

when exact boundary behavior matters.

The two rules differ at:

`d_ij = r_c`

## 52. Cutoff Boundary

The set:

`d_ij = r_c`

is a topology-decision boundary for a hard-cutoff construction.

Crossing this boundary may alter the graph.

It is not automatically:

- a physical phase transition;
- a structural transition;
- a chemical bond event;
- a bifurcation;
- a TR ternary transition.

## 53. Species-Dependent Cutoff

A specialization may define:

`r_c(z_i, z_j)`

instead of one global cutoff.

The domain and symmetry of this function must be declared.

For an unordered pair relation, the model may require:

`r_c(z_i, z_j) = r_c(z_j, z_i)`

but this symmetry must not be assumed automatically.

## 54. Fixed-Count Neighborhood

A topology may select the nearest:

`k`

neighbors rather than using one radial cutoff.

The rule must define:

- value of `k`;
- tie handling;
- periodic treatment;
- behavior when fewer than `k` admissible sites exist.

## 55. Tie Handling

If two candidate neighbors have identical ranking values under the topology rule, the implementation must preserve deterministic and permutation-consistent semantics.

An arbitrary storage-order tie break may violate permutation behavior.

## 56. Adaptive Neighborhood

An adaptive neighborhood may depend on configuration-dependent parameters.

The resulting topology is state-dependent.

Its construction rule remains separate from the downstream representation.

## 57. Dynamic Topology

For evolving configuration:

`q(t)`

a topology may also evolve:

`G(t) = G_C(q(t), b(t), λ_G)`

A change in `G(t)` is a topology event.

It does not automatically imply a physical structural transition.

## 58. Topology Hysteresis

A topology constructor may use different edge-entry and edge-exit criteria.

Such a rule is history-dependent.

The topology state or sufficient history must then be included in the source of the update relation.

## 59. History-Dependent Topology Update

A generic topology update may be typed as:

`U_G: X_G × Q × X_B × Λ_G → X_G`

The previous topology is part of the input.

This is different from a memoryless construction:

`G_C: Q × X_B × Λ_G → X_G`

## 60. Directed Topology

For a directed graph:

`(i, j) ∈ E`

does not imply:

`(j, i) ∈ E`

The direction may encode computational message direction or another declared relation.

Direction must not be assigned undocumented physical meaning.

## 61. Undirected Topology

For an undirected graph:

`{i, j} ∈ E`

is one symmetric edge object.

An implementation may store two directed records internally while representing one mathematical undirected interaction.

Representation and storage must remain distinguished.

## 62. Self Edges

A graph constructor must declare whether:

`(i, i)`

is admissible.

Self edges may have computational use.

They are not implied by atomistic geometry.

## 63. Edge Attributes

Let:

`X_E`

denote an edge-attribute space.

An edge attribute may be generated through:

`A_E: Q × X_B × E → X_E`

Possible attributes include:

- relative displacement;
- distance;
- species pair;
- periodic image;
- cutoff weight;
- other declared geometric information.

## 64. Edge Attribute Is Not Edge Existence

The existence of an edge and its attribute are different objects.

Therefore:

`edge relation ≠ edge feature`

An edge feature may change while the edge remains present.

## 65. Node Attributes

Let:

`X_V`

denote a node-attribute space.

A node attribute may include:

- atomic identity;
- local physical state;
- occupancy;
- external-field state;
- other declared site-associated quantities.

Position may be stored as node data but remains geometric state rather than species identity.

## 66. Locality

Locality is defined only relative to a declared dependency relation.

A mapping is not local merely because it operates on a graph.

The dependency radius or topology depth must be explicit.

## 67. Geometric Locality

A geometric local environment may be defined through a bounded spatial neighborhood around a central site.

The bound may depend on:

- radial distance;
- cell geometry;
- species;
- adaptive local state.

## 68. Graph Locality

A graph-local environment may instead be defined through graph distance.

For integer:

`k ≥ 0`

a `k`-hop environment contains nodes reachable from the center within at most `k` graph edges under the declared direction convention.

## 69. Geometric and Graph Locality Are Different

A `k`-hop graph neighborhood does not correspond universally to one fixed Euclidean radius.

Likewise, one Euclidean cutoff neighborhood does not determine a fixed graph-hop receptive field after repeated propagation.

Therefore:

`geometric locality ≠ graph-hop locality`

## 70. Effective Receptive Field

If a computational architecture repeatedly propagates information through local edges, its effective dependency region may exceed the first-hop environment.

A model claiming strict locality must specify the final dependency boundary, not only the first graph construction step.

## 71. Local Atomic Environment

For central site:

`i ∈ V`

define a local-environment mapping:

`E_i: Q × X_G × X_B → X_env`

The output:

`e_i = E_i(q, G, b)`

belongs to:

`X_env`

## 72. Environment Central Site

The local environment must preserve the identity of the central site unless the specialization explicitly defines a center-free object.

The central site satisfies:

`z_i ∈ Z`

and retains its computational correspondence under permutation.

## 73. Environment Neighbor Set

Let:

`N_i(G)`

denote the declared neighbor set of central site `i`.

The environment may contain records for:

`j ∈ N_i(G)`

The environment definition must state whether neighbor ordering is meaningful.

## 74. Canonical Environment Content

A local environment may contain:

- central identity `z_i`;
- neighbor identities `z_j`;
- relative vectors `r_ij`;
- distances `d_ij`;
- periodic-image identifiers;
- edge attributes;
- selected auxiliary state.

Every included field must have declared semantics.

## 75. Environment as Structured Object

A local environment should be treated as a structured object rather than an untyped concatenated vector.

A generic representation is:

`e_i = (z_i, M_i, ξ_i)`

where:

- `M_i` is a declared collection of neighbor records;
- `ξ_i` contains optional local auxiliary state.

The exact structure is specialization-dependent.

## 76. Neighbor Record

For an ordered neighbor relation, one generic neighbor record may be:

`m_ij = (z_j, r_ij, d_ij, η_ij)`

where:

`η_ij`

denotes other declared edge information.

A model should not include both `r_ij` and `d_ij` under the assumption that they are independent variables.

Distance is derived from the displacement when both use the same geometry convention.

## 77. Derived Environment Fields

If:

`d_ij = ||r_ij||`

then `d_ij` is derived from `r_ij`.

Its presence as an explicit stored field may improve computational access but does not make it an independent geometric degree of freedom.

## 78. Environment Ordering

If neighbor records are stored in a sequence, storage order must be separated from mathematical environment semantics.

A physically unordered neighborhood must not acquire physical ordering merely from array position.

## 79. Permutation of Neighbor Storage

Let:

`π_i`

permute only the storage order of neighbor records in `M_i`.

For an order-independent environment semantics, the represented environment must remain equivalent under this reordering.

Any later descriptor must preserve the declared permutation behavior.

## 80. Global Atomic Permutation

A global site permutation changes all site indices consistently.

The local environment associated with physical atom `i` is carried to the corresponding permuted index.

The environment collection therefore transforms equivariantly under atomic reindexing.

## 81. Environment Collection

For all sites, define:

`E(q, G, b) = (e_1, ..., e_N)`

The collection belongs to a declared product or indexed-family space.

The local environment collection retains site correspondence.

## 82. Environment Collection and Global Descriptor

The complete environment collection is not identical to a global invariant descriptor.

A global aggregation may discard site correspondence.

Therefore:

`environment collection ≠ global descriptor`

## 83. Species Awareness

Two local environments with identical geometry but different species assignments are not automatically equivalent.

The equivalence relation must define whether species identity is preserved.

For ordinary interatomic modeling, species labels are part of the environment state.

## 84. Same-Species Permutation

Permutation of neighbors carrying the same species identity may preserve an order-independent environment description.

The mapping must still preserve their geometric records as a set or multiset.

## 85. Different-Species Exchange

Exchanging the species labels of two geometrically distinct neighbors changes the environment state unless the model explicitly declares the species classes equivalent.

Therefore:

`permutation symmetry ≠ arbitrary species exchange`

## 86. Environment Translation Behavior

Under global translation:

`x_k' = x_k + a`

for all sites `k`.

Relative vectors satisfy:

`r_ij' = r_ij`

Therefore a local environment represented entirely through relative geometry can be translation invariant with respect to that geometric channel.

## 87. Environment Rotation Behavior

Under proper rotation:

`R ∈ SO(d)`

relative vectors transform as:

`r_ij' = R r_ij`

while distances satisfy:

`d_ij' = d_ij`

Thus one environment may contain both:

- rotationally equivariant vector channels;
- rotationally invariant scalar channels.

## 88. Environment Reflection Behavior

For:

`R ∈ O(3)`

with:

`det(R) = -1`

polar relative vectors still transform as:

`r_ij' = R r_ij`

but orientation-sensitive derived objects may exhibit parity-dependent behavior.

Reflection handling must therefore remain explicit.

## 89. Environment Transformation Is Not Environment Equality

A rotated environment is not numerically identical to the original environment when oriented vector channels are retained.

Instead, the two may be related by a declared transformation action.

Therefore:

`equivalent under symmetry ≠ numerically identical representation`

## 90. Environment Equivalence Relation

Let:

`~_env`

be a declared equivalence relation on `X_env`.

The relation may identify environments differing only by selected transformations such as:

- translation;
- proper rotation;
- reflection where admissible;
- permutation of computational indices.

The exact equivalence set must be declared before constructing quotient-like representations.

## 91. No Universal Environment Equivalence

An environment equivalence appropriate to one output may be inappropriate to another.

For example, identifying mirror images may destroy information needed for a chirality-sensitive quantity.

Therefore:

`environment equivalence is task-relative`

## 92. Environment Completeness

An environment definition is complete relative to a claim only when it contains all source information required by that claim.

Completeness is therefore not absolute.

A local environment sufficient for a short-range scalar energy model may be insufficient for:

- long-range electrostatics;
- global topology;
- external-field response;
- history-dependent dynamics.

## 93. Environment Truncation

A finite neighborhood truncates information outside the declared locality boundary.

This is an explicit information-loss mechanism.

Therefore:

`finite local environment ≠ complete global configuration`

## 94. Locality Assumption

When a downstream model uses only `e_i`, it assumes that the selected target for site `i` can be represented sufficiently from that local state and model parameters.

This assumption requires validation for the intended application domain.

## 95. Long-Range Dependence

Physical interactions with long-range dependence require one of the following:

- explicit long-range state;
- enlarged environment;
- global channel;
- hierarchical channel;
- another declared representation mechanism.

Long-range information must not be claimed to emerge from a strictly bounded environment without a defined path.

## 96. Environment Boundary Discontinuity

A hard cutoff may cause the neighbor set to change discontinuously as a site crosses the cutoff boundary.

The topology discontinuity is separate from continuity of any later weighted representation.

## 97. Smooth Cutoff Weight

A downstream representation may use a weight:

`w_c(d)`

that approaches zero near a cutoff.

The function must define:

- domain;
- codomain;
- cutoff behavior;
- continuity;
- differentiability where required.

No universal cutoff function is defined by EIF.

## 98. Weight Does Not Define Neighbor Existence Automatically

A graph may retain an edge with weight zero, or remove the edge when a threshold is crossed, depending on the topology contract.

Therefore:

`zero edge weight ≠ absent edge`

unless explicitly defined.

## 99. Topology and Representation Smoothness

A smooth edge feature does not guarantee a smooth complete model if topology itself changes discontinuously.

Conversely, a fixed topology may support smooth geometric features over a restricted domain.

The two layers must be validated separately.

## 100. Periodic Local Environment

For periodic systems, an environment must preserve sufficient image information to reconstruct the selected relative geometry.

A neighbor record may therefore require:

- physical site index;
- image vector;
- periodic displacement.

Using only the physical site index may be insufficient when multiple images of the same site are admissible.

## 101. Duplicate Periodic Images

A local environment may contain multiple periodic images associated with the same physical site under sufficiently large neighborhoods.

These are separate geometric neighbor records but not separate physical site identities.

## 102. Periodic Permutation Semantics

A permutation of physical atom indices must preserve:

- atom identity;
- position correspondence;
- image correspondence;
- environment membership.

Periodic image labels must not be confused with computational atom permutations.

## 103. Central Cell Convention

A periodic implementation may choose a canonical representative of each physical atom inside a reference cell.

This is a coordinate convention.

Changing the representative by a lattice translation does not necessarily change the physical periodic configuration.

## 104. Wrapped and Unwrapped Coordinates

Wrapped and unwrapped trajectory coordinates may represent the same periodic physical state while differing numerically.

The geometry mapping must state which representation it consumes.

## 105. Trajectory Continuity Boundary

Wrapped coordinates can exhibit coordinate jumps at cell boundaries even when physical motion is continuous.

Therefore:

`coordinate discontinuity ≠ physical discontinuity`

A dynamical environment mapping must use a boundary-aware convention appropriate to the claim.

## 106. Static and Dynamic Environments

A static environment mapping depends on one configuration state.

A dynamic environment may include:

- velocities;
- prior configurations;
- retained topology;
- local history;
- external driving state.

These are different source spaces.

## 107. History-Dependent Environment

Let:

`H_EIF`

denote a declared interatomic history space.

A history-dependent environment mapping may be typed as:

`E_i,H: H_EIF × X_G × X_B → X_env,H`

The history source must be explicit.

## 108. Snapshot and History Remain Distinct

A snapshot environment does not reconstruct a history-dependent state in general.

Therefore:

`snapshot environment ≠ history state`

This distinction becomes essential for later dynamic integration.

## 109. Environment and Oscillator State

No local atomic environment automatically contains TR oscillator variables.

The following remain distinct:

`local atomic environment ≠ oscillator state`

`relative vector ≠ oscillator phase`

`interatomic distance ≠ resonance coordinate`

Any connection requires a later typed integration mapping.

## 110. Environment and Ternary State

The balanced ternary domain remains:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and active neutral:

`0`

No environment state is automatically assigned a ternary value.

Therefore:

`local environment ≠ ternary state`

## 111. Geometry-to-Ternary Shortcut Is Forbidden

The following direct rules are not implied by EIF:

`short distance → -1`

`cutoff boundary → 0`

`long distance → 1`

or any equivalent geometric-to-ternary identification.

A later TR-EIF integration layer must define any such mapping explicitly and justify its semantics.

## 112. Neighbor Status Is Not Resonance Classification

The binary relation:

`neighbor / non-neighbor`

is a topology classification.

It is not the TR resonance classification:

`OUTSIDE / BOUNDARY / INSIDE`

Therefore:

`graph cutoff boundary ≠ resonance-window boundary`

## 113. Topology Transition Is Not Ternary Transition

An edge appearing or disappearing in `G` is a topology event.

It is not automatically a transition in:

`T = {-1, 0, 1}`

The two event spaces remain distinct.

## 114. Topology Transition Is Not Structural Transition

A computational graph may change because of a modeling cutoff even when no independently defined structural phase changes.

Therefore:

`graph change ≠ structural transition`

## 115. Topology Transition Is Not Physical Phase Transition

A topology edge event does not by itself establish thermodynamic phase behavior.

Therefore:

`graph change ≠ physical phase transition`

## 116. Neighbor Edge Is Not Force

The presence of:

`(i, j) ∈ E`

does not define a force vector.

A later force model requires an independently defined mapping into the appropriate vector space.

## 117. Neighbor Edge Is Not Energy

The presence of an edge does not define an interaction energy.

A later energy model must define its energy mapping independently.

## 118. Neighbor Edge Is Not Chemical Bond

A computational neighbor relation may be broader or narrower than a chemically defined bonding relation.

Therefore:

`neighbor relation ≠ chemical bond`

without a separate bonding definition.

## 119. Local Environment Is Not Physical Phase

A local environment may encode geometric information relevant to structural analysis.

It is not itself a physical phase state.

A physical phase classification requires an independently defined physical criterion.

## 120. Environment Descriptor Boundary

Let:

`D_env: X_env → X_desc`

be a future environment-descriptor mapping.

The descriptor is downstream of the environment.

The present chapter does not prescribe the form of `X_desc`.

## 121. Representation Boundary

Let:

`Φ_EIF: X_env → Y_EIF,local`

represent a future local EIF representation mapping.

The representation may be invariant, equivariant, or mixed according to its transformation contract.

This chapter defines the source environment but does not yet select the representation architecture.

## 122. Information Loss Under Descriptor Mapping

If:

`D_env(e_a) = D_env(e_b)`

for:

`e_a ≠ e_b`

then the descriptor cannot distinguish those environments.

Whether that information loss is acceptable depends on the claim and output space.

## 123. Information Loss Under Topology Construction

Topology construction itself may be information-reducing.

A graph that stores only connectivity may discard exact distances and directions.

Therefore:

`G_C(q)`

does not generally allow reconstruction of:

`q`

## 124. Information Loss Under Local Extraction

A local environment excludes state outside its declared locality region.

Therefore:

`E_i(q, G, b)`

does not generally allow reconstruction of the full global configuration.

## 125. Layered Information-Loss Chain

The chain:

`q`

`→ G`

`→ e_i`

`→ descriptor`

may lose information at multiple stages.

Each stage must identify what is retained.

Information lost at an earlier stage cannot be recovered from a later stage without an independent information source.

## 126. Configuration Equivalence

Two configurations may be considered equivalent under a declared transformation relation.

Possible transformations include:

- translation;
- rotation;
- reflection when included;
- computational permutation;
- periodic lattice translation.

The equivalence relation must be specified explicitly.

## 127. Raw Equality and Physical Equivalence

Numerical coordinate equality is stronger than many physically relevant equivalence relations.

Two configurations may have different coordinate arrays while representing the same state under a permitted rigid transformation.

Therefore:

`raw array equality ≠ configuration equivalence`

## 128. Configuration Transformation Action

Let:

`G_cfg`

be the declared configuration-transformation group.

An action is:

`ρ_Q: G_cfg × Q → Q`

The action must transform every configuration component consistently.

## 129. Euclidean Position Action

For Euclidean transformation:

`g = (R, a)`

with:

`R ∈ O(d)`

and:

`a ∈ ℝ^d`

the position action is:

`x_i' = R x_i + a`

Atomic identity remains:

`z_i' = z_i`

under pure geometric transformation.

## 130. Configuration Permutation Action

For:

`π ∈ S_N`

the permutation action maps:

`((z_1, x_1), ..., (z_N, x_N))`

to consistently reindexed identity-position pairs.

Species and coordinates must remain paired.

## 131. Combined Transformation

A model may apply both a Euclidean transformation and a computational permutation.

The combined action must specify:

- transformation order;
- action on positions;
- action on identities;
- action on topology;
- action on environments.

No implicit combined group structure is assumed beyond the declared model.

## 132. Environment Transformation Action

Let:

`ρ_env(g): X_env → X_env`

be the induced environment action for a declared geometric transformation.

A consistent environment extractor should satisfy the appropriate relation between:

`E_i(ρ_Q(g)q, ...)`

and:

`ρ_env(g)E_i(q, ...)`

under the transformation of all required auxiliary objects.

The exact relation depends on indexing and topology semantics.

## 133. Permuted Central-Site Correspondence

Under global permutation `π`, the environment previously associated with site `i` is associated with the corresponding permuted site index.

Local environments therefore transform as an indexed family rather than as one invariant scalar.

## 134. Environment Extraction Equivariance

For a consistently transformed configuration, topology, and central-site identity, local-environment extraction should preserve the declared geometric and permutation correspondence.

This property belongs to the environment extractor before any learned representation is introduced.

## 135. Topology Transformation Consistency

If topology is constructed from rigid-motion-invariant geometric criteria, a transformed configuration should produce a correspondingly transformed or identical connectivity relation under the declared index correspondence.

This condition must be tested for the actual topology algorithm.

## 136. Numerical Topology Sensitivity

Floating-point comparison near a cutoff may cause numerically unstable edge classification.

A computational topology contract must define:

- comparison rule;
- numeric precision;
- tolerance policy if used;
- deterministic tie behavior.

The tolerance is an implementation parameter.

## 137. Exact and Numerical Cutoff Boundaries

The exact mathematical boundary:

`d_ij = r_c`

is distinct from a numerical tolerance region around `r_c`.

Therefore:

`exact cutoff boundary ≠ numerical cutoff tolerance`

## 138. Invalid Geometry State

An invalid geometry state must have a representation separate from valid numeric values.

For example, a failed displacement computation must not be represented silently as:

`r_ij = 0`

because zero displacement is itself a valid mathematical value in a domain that admits coincident sites.

## 139. Missing Neighbor Data

Missing neighbor data must remain distinct from an empty neighborhood.

Therefore:

`missing environment data ≠ empty neighbor set`

An empty environment may be a valid state under some models.

## 140. Empty Neighborhood

A central site may have:

`N_i = ∅`

under a finite cutoff or sparse configuration.

The model must define downstream behavior for this valid case.

It must not automatically classify the environment as invalid.

## 141. Isolated Site

An isolated site under the computational topology is not necessarily a physically noninteracting atom.

It means only that the declared topology contains no selected neighbor edge for that site.

## 142. Environment Cardinality

Define:

`n_i = |N_i|`

for a finite neighborhood.

The value `n_i` is a topology-derived count.

It is not automatically:

- coordination number in a chemical sense;
- bond count;
- valence;
- structural phase label.

## 143. Coordination Definition Boundary

If a specialization uses the term:

`coordination number`

it must define the underlying neighbor criterion.

Different geometric or chemical criteria may produce different coordination values for the same configuration.

## 144. Local Density Boundary

A local neighbor count or distance-weighted sum may be used to define a model-specific local-density proxy.

Such a proxy is not automatically thermodynamic mass density or number density without the required volume definition and units.

## 145. Environment Scale

Every local environment has an implied or explicit spatial/topological scale.

The scale is determined by its locality construction.

A later multiscale EIF model must preserve scale identity rather than mixing environment radii silently.

## 146. Multiple Environment Scales

Let:

`L_env`

be a finite environment-scale index set.

For each:

`ell ∈ L_env`

define:

`E_i,ell: Q × X_G,ell × X_B → X_env,ell`

Different scales may use different:

- cutoffs;
- topology rules;
- feature content.

## 147. Multiscale Environment State

A multiscale local environment may belong to:

`X_env,MS = ∏_(ell ∈ L_env) X_env,ell`

Scale identity must remain explicit.

A single merged neighbor list is not automatically equivalent to this product state.

## 148. Cross-Scale Information

A larger environment may contain geometrically more sites than a smaller environment.

It does not automatically replace all specialized short-range representation channels.

Different scales may carry different transformation or physical semantics.

## 149. Local-to-Global Environment Relation

The collection:

`(e_1, ..., e_N)`

provides local views of the global configuration.

These views may overlap.

They are not an independent partition of the global state unless a model explicitly constructs them as one.

## 150. Overlapping Environments

One physical pair or site may appear in several local environments.

Such repetition is a representation property.

It does not imply duplication of the physical atom.

## 151. Environment Provenance

A serialized or computed environment should retain sufficient provenance to identify:

- source configuration;
- topology rule;
- boundary convention;
- cutoff or neighborhood parameters;
- central-site identity;
- software or algorithm version where executable evidence is claimed.

## 152. Topology Provenance

A topology-dependent claim must retain the provenance of:

- topology-construction mapping;
- numerical parameters;
- species-dependent rules;
- boundary handling;
- dynamic update rule where applicable.

A graph without its construction semantics may be insufficient evidence.

## 153. Configuration Provenance

For scientific traceability, configuration provenance may include:

- source dataset or calculation;
- simulation state;
- measurement or generated-state identity;
- units;
- coordinate convention;
- periodic-cell convention.

The exact metadata schema is implementation-specific.

## 154. Units

All dimensional geometry must retain units.

Positions, displacements, distances, and cell vectors share a length dimension under ordinary Cartesian geometry.

A numerical cutoff must use a compatible length unit.

## 155. Unit Consistency

A comparison such as:

`d_ij ≤ r_c`

is valid only when:

`d_ij`

and:

`r_c`

use compatible units.

Implicit unit conversion is not part of the mathematical inequality.

## 156. Dimensionless Internal Coordinates

A numerical implementation may normalize distances or positions.

The normalization mapping must be defined.

A normalized coordinate remains related to the dimensional source through that mapping.

## 157. Coordinate Normalization Is Not Geometric Transformation

Scaling all coordinates numerically by a normalization factor for computational purposes is not automatically an element of the Euclidean rigid-motion group.

Therefore:

`normalization scaling ≠ rigid Euclidean symmetry`

## 158. Physical Scaling

A physical dilation of a configuration changes interatomic distances.

It is not a translation or rotation.

A model must not include dilation inside `E(3)` by mistake.

## 159. Geometry and Symmetry Scope

The relevant transformation group depends on the claim.

Possible scopes include:

- translations only;
- proper rigid motions;
- full Euclidean transformations including reflections;
- permutations;
- combinations of geometric and permutation actions.

The scope must be declared before validation.

## 160. Local Environment Validation

A local-environment implementation must validate:

- central-site identity;
- neighbor membership;
- relative geometry;
- periodic image handling;
- species correspondence;
- ordering semantics;
- transformation behavior;
- degeneracy handling.

## 161. Topology Validation

A topology implementation must validate:

- edge criterion;
- edge directionality;
- self-edge rule;
- cutoff boundary;
- periodic handling;
- tie behavior;
- deterministic reconstruction;
- permutation correspondence.

## 162. Periodic Geometry Validation

Periodic geometry validation must include configurations that exercise:

- cell-boundary crossing;
- equivalent periodic images;
- minimum-image or selected-image behavior;
- cell transformations;
- multiple admissible images where the model allows them.

## 163. Permutation Validation

Given a valid site permutation, reconstruction after permutation must preserve:

- species-position pairing;
- graph correspondence;
- environment correspondence;
- local geometric relations.

An implementation that depends on arbitrary storage order fails this requirement.

## 164. Translation Validation

For a global translation of all positions, relative local geometry must remain unchanged under the declared non-periodic or consistently transformed periodic convention.

Absolute-position channels, if intentionally present, follow their separately declared behavior.

## 165. Rotation Validation

For:

`R ∈ SO(d)`

relative vectors must transform according to:

`r_ij' = R r_ij`

and distances must satisfy:

`d_ij' = d_ij`

within the numerical tolerance of the implementation.

## 166. Reflection Validation

If reflections belong to the declared transformation set, environment extraction must preserve the corresponding parity-sensitive geometry correctly.

Proper-rotation validation alone is insufficient.

## 167. Cardinality Validation

For variable-cardinality systems, validation must check:

- creation;
- removal;
- reindexing;
- topology reconstruction;
- environment reconstruction;
- trace identity.

Fixed-cardinality tests do not establish variable-cardinality correctness.

## 168. Information-Loss Validation

A model must identify at which stages information is discarded.

Relevant stages include:

`configuration → topology`

`configuration + topology → local environment`

`local environment → representation`

The information-loss declaration is part of the model contract.

## 169. Environment Sufficiency Is Claim-Scoped

Define a claim:

`q_claim`

An environment is sufficient only when it contains the source information required to evaluate the downstream mapping relevant to `q_claim`.

There is no universal local-environment size sufficient for all interatomic claims.

## 170. Classical Reference: Atom-Centered Symmetry Functions

Behler and Parrinello introduced an atom-centered neural-network construction for high-dimensional potential-energy surfaces in which the total system is represented through local atomic environments and symmetry-preserving inputs.

The work provides an established computational precedent for local atom-centered environment representations in interatomic modeling.

It does not define EIF.

Provenance:

`PRIMARY_SOURCE`

## 171. Classical Reference: Chemical Environment Representations

Bartók, Kondor, and Csányi analyzed representations of atomic neighborhood environments and emphasized the requirements associated with translation, rotation, reflection, and permutation behavior, together with representation faithfulness.

The work provides a primary reference for the distinction between an atomic environment and its descriptor.

It does not define EIF.

Provenance:

`PRIMARY_SOURCE`

## 172. Literature Boundary

The cited works establish precedent for local atomic environment representations and symmetry-aware atomistic descriptors.

They do not establish:

- one universal neighborhood definition;
- one universal cutoff;
- complete physical sufficiency of local environments;
- TR resonance semantics;
- balanced ternary semantics;
- automatic chemical-bond interpretation;
- automatic EIF-to-TR mappings.

## 173. Primary Sources

1. Behler, J., and Parrinello, M. "Generalized Neural-Network Representation of High-Dimensional Potential-Energy Surfaces." Physical Review Letters 98, 146401, 2007. DOI: `10.1103/PhysRevLett.98.146401`

2. Bartók, A. P., Kondor, R., and Csányi, G. "On Representing Chemical Environments." Physical Review B 87, 184115, 2013. DOI: `10.1103/PhysRevB.87.184115`

These references provide primary atomistic precedent for local-environment and symmetry-aware representation concepts used in the classical boundary of this chapter.

EIF-specific state separation, topology contracts, locality contracts, provenance rules, and TR-EIF integration boundaries remain author-defined framework structure.

## 174. Interatomic Source-State Contract

A minimally defined EIF source state must specify:

1. site cardinality;
2. site-index set;
3. atomic-identity domain;
4. identity state;
5. position state;
6. spatial dimension;
7. admissible configuration domain;
8. boundary-condition state;
9. periodic-cell state where applicable;
10. auxiliary physical state where applicable;
11. units;
12. coordinate convention.

## 175. Geometry Contract

A geometry mapping must specify:

1. source configuration;
2. boundary convention;
3. relative-displacement rule;
4. distance rule;
5. periodic-image rule where applicable;
6. angular or higher-order relations where used;
7. degeneracy behavior;
8. dimensional units;
9. transformation behavior.

## 176. Topology Contract

A topology mapping must specify:

1. node set;
2. edge type;
3. directed or undirected semantics;
4. self-edge semantics;
5. construction rule;
6. cutoff or ranking parameters;
7. periodic behavior;
8. species dependence;
9. tie handling;
10. dynamic update semantics where applicable;
11. history dependence where applicable;
12. provenance.

## 177. Local-Environment Contract

Every local environment must specify:

1. central-site identity;
2. neighborhood relation;
3. neighbor identities;
4. relative geometry;
5. periodic-image semantics;
6. edge attributes;
7. included auxiliary state;
8. excluded state;
9. neighbor-order semantics;
10. locality scale;
11. transformation behavior;
12. information loss;
13. provenance.

## 178. Core Invariants

The following invariants are mandatory.

1. Computational site index remains distinct from atomic identity.

2. Atomic identity remains distinct from position.

3. Configuration remains distinct from complete physical state.

4. Geometry remains distinct from topology.

5. Relative displacement remains distinct from distance.

6. Ordered pairs remain distinct from unordered pairs.

7. A graph edge remains distinct from a chemical bond.

8. A graph edge remains distinct from force.

9. A graph edge remains distinct from energy.

10. A cutoff boundary remains distinct from a resonance-window boundary.

11. A topology transition remains distinct from a ternary transition.

12. A topology transition remains distinct from a structural transition.

13. A topology transition remains distinct from a physical phase transition.

14. Periodic image identity remains distinct from physical site identity.

15. Cell deformation remains distinct from rigid rotation.

16. Translation remains distinct from rotation.

17. Rotation remains distinct from permutation.

18. Geometry scaling remains distinct from Euclidean rigid motion.

19. Local environment remains distinct from descriptor.

20. Local environment remains distinct from invariant or equivariant representation.

21. Local environment remains distinct from TR resonance state.

22. Local environment remains distinct from ternary state.

23. Atomic coordinate remains distinct from oscillator phase.

24. Neighbor status remains distinct from resonance classification.

25. Empty neighborhood remains distinct from missing data.

26. Invalid geometry remains distinct from zero geometry.

27. Storage order remains distinct from physical neighbor ordering.

28. Species identity is preserved under computational permutation.

29. Locality remains model-relative.

30. Finite locality implies explicit information truncation.

31. Exact cutoff semantics remain distinct from numerical tolerance.

32. Units remain explicit.

33. History-dependent topology includes its history state.

34. Variable cardinality is represented explicitly.

35. No geometry-to-ternary shortcut is permitted.

36. No geometry-to-resonance shortcut is permitted.

37. No topology-to-bond shortcut is permitted.

38. No local environment is assumed physically complete without validation.

39. Information loss is traceable.

40. Later invariant and equivariant representations operate on explicitly defined source environments.

## 179. Formal Non-Equivalences

The following non-equivalences are mandatory:

`computational index ≠ atomic identity`

`atomic identity ≠ position`

`configuration ≠ complete physical state`

`configuration ≠ representation`

`geometry ≠ topology`

`distance ≠ edge`

`relative displacement ≠ distance`

`ordered pair ≠ unordered pair`

`neighbor edge ≠ chemical bond`

`neighbor edge ≠ force`

`neighbor edge ≠ energy`

`periodic image ≠ additional physical atom`

`cell deformation ≠ rigid rotation`

`translation ≠ rotation`

`rotation ≠ permutation`

`normalization scaling ≠ Euclidean rigid transformation`

`local environment ≠ descriptor`

`local environment ≠ latent representation`

`local environment ≠ resonance state`

`local environment ≠ ternary state`

`atomic position ≠ oscillator phase`

`graph cutoff boundary ≠ resonance-window boundary`

`graph change ≠ ternary transition`

`graph change ≠ structural transition`

`graph change ≠ physical phase transition`

`neighbor count ≠ chemical coordination automatically`

`empty neighborhood ≠ missing environment data`

`zero displacement ≠ invalid geometry automatically`

`sample storage order ≠ physical neighbor order`

`finite local environment ≠ complete global configuration`

`geometric locality ≠ graph-hop locality`

`exact cutoff boundary ≠ numerical cutoff tolerance`

## 180. Formal EIF Source Chain

The source-side EIF chain is:

`atomic identities`

`+`

`atomic positions`

`+`

`boundary state`

`+`

`declared auxiliary state`

`→ admissible interatomic configuration`

`→ boundary-aware relative geometry`

`→ interaction topology`

`→ local neighborhood`

`→ structured local atomic environment`

`→ invariant / equivariant representation`

The final representation arrow belongs to the next formal layer and is not specified by this chapter.

## 181. TR-EIF Boundary

The complete architecture still requires the later chain:

`interatomic state`

`→ equivariant representation`

`→ resonant state`

`→ ternary state`

and, where independently defined:

`ternary / resonant state`

`→ interatomic update`

This chapter establishes only the interatomic source state, geometry, topology, and local-environment side.

No EIF object defined here is assigned automatically to:

`X_R`

`R_C`

or:

`T = {-1, 0, 1}`

## 182. Conformance Requirements

An EIF source-state implementation conforms to this chapter when:

- atomic identities and computational indices remain distinct;
- positions have a declared dimension and unit;
- configuration admissibility is explicit;
- boundary conditions are explicit;
- periodic image handling is explicit when used;
- geometry is derived through a declared mapping;
- topology is constructed through a declared mapping;
- graph edges do not acquire undocumented physical meaning;
- local environments preserve central-site and species correspondence;
- neighbor ordering semantics are explicit;
- degeneracies are handled explicitly;
- locality and information loss are declared;
- transformation behavior is defined;
- history is represented when topology or environment semantics depend on it;
- no TR state is inserted without an explicit integration mapping.

## 183. Final Statement

The interatomic source layer of EIF is defined by the chain:

`configuration`

`→ geometry`

`→ topology`

`→ local environment`

The configuration contains the represented atomic identities and positions together with explicitly declared boundary and auxiliary state.

Geometry defines relational spatial information.

Topology defines the computational interaction relation selected by the model.

A local environment combines the central-site identity with the declared neighborhood and its boundary-aware relative geometry.

These objects remain distinct.

A graph edge is not automatically a bond.

A distance is not automatically an interaction.

A cutoff crossing is not automatically a structural transition.

A local environment is not automatically an invariant descriptor.

A local environment is not automatically an equivariant representation.

A geometric state is not automatically a resonance state.

The balanced ternary kernel remains independently defined as:

`-1/0/1`

with active:

`0`

and no geometric rule in EIF is permitted to alter or assign that state without an explicit later mapping.

The resulting source-space architecture is therefore:

`interatomic state`

`→ geometry`

`→ topology`

`→ local environment`

which provides the mathematically typed input required for the subsequent construction of invariant and equivariant interatomic representations.
