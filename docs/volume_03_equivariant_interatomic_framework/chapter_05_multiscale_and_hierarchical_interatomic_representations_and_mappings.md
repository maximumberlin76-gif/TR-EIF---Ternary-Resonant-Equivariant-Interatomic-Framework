# Multiscale and Hierarchical Interatomic Representations and Mappings

## 1. Purpose

This document formalizes the multiscale and hierarchical representation layer of the Equivariant Interatomic Framework.

The chapter continues the established EIF chain:

`interatomic configuration`

`→ geometry`

`→ topology`

`→ local atomic environment`

`→ invariant / equivariant representation`

`→ interatomic physical-output interface`

and extends it into:

`→ multiscale interatomic representation`

`→ cross-scale mapping`

`→ hierarchical interatomic state`

The chapter establishes:

- explicit scale sets;
- scale-specific state spaces;
- scale-specific topology;
- scale-specific local environments;
- scale-specific invariant and equivariant representations;
- hierarchical partitions;
- overlapping and non-overlapping scale domains;
- aggregation;
- restriction;
- coarse-graining;
- refinement interfaces;
- cross-scale mappings;
- information loss;
- scale-dependent locality;
- symmetry preservation across scales;
- permutation correspondence across scales;
- hierarchical representation composition;
- scale-specific physical outputs;
- multiscale energy mappings;
- force-consistency boundaries;
- double-counting boundaries;
- scale-dependent provenance;
- exact and numerical cross-scale validation;
- the boundary between multiscale EIF state and future dynamic or Ternary Resonant integration.

This chapter does not define one universal coarse-graining method.

It defines the mathematical contract that any multiscale EIF realization must satisfy.

## 2. Dependency

This chapter depends on:

- Volume 01, Mathematical Foundations;
- Volume 02, Ternary Resonance Theory;
- Volume 03, Chapter 01, Equivariant Interatomic Foundations;
- Volume 03, Chapter 02, Interatomic State Spaces, Geometry, and Local Environments;
- Volume 03, Chapter 03, Symmetry Actions, Invariant and Equivariant Representations;
- Volume 03, Chapter 04, Interatomic Mappings, Energy, Force, and Stress Interfaces.

It inherits without redefinition:

- admissible interatomic configuration spaces;
- topology spaces;
- local-environment spaces;
- EIF representation spaces;
- invariant and equivariant mapping semantics;
- permutation, translation, rotation, and reflection actions;
- information-loss requirements;
- physical-output contracts;
- energy-force consistency requirements;
- provenance classes;
- closed TR invariants.

## 3. Scientific Status Classes

### 3.1 GENERAL MATHEMATICAL STRUCTURE

The following use general mathematical structures:

- finite index sets;
- product spaces;
- partitions;
- covers;
- mappings;
- compositions;
- projections;
- equivalence relations;
- group actions;
- commutative transformation relations.

### 3.2 EIF FORMAL / AUTHOR-DEFINED

The following are author-defined EIF architecture:

- the exact scale-space hierarchy;
- scale-specific environment contracts;
- cross-scale representation contracts;
- hierarchy-consistency requirements;
- information-loss accounting;
- cross-scale equivariance requirements;
- multiscale physical-output contracts;
- double-counting constraints;
- multiscale conformance conditions.

### 3.3 DERIVED

Relations following from declared scale maps, group actions, and physical-output mappings are classified as:

`DERIVED`

### 3.4 EMPIRICAL / CALIBRATED

Scale radii, partition thresholds, learned coarse-graining parameters, empirical interaction ranges, resolution cutoffs, and calibrated scale weights require explicit provenance.

### 3.5 OPERATIONAL / EXECUTABLE REFERENCE

A computational implementation may instantiate the multiscale contracts with graphs, hierarchical neighborhoods, tensor fields, clusters, meshes, or other data structures.

No implementation structure is elevated automatically to universal EIF mathematics.

## 4. Multiscale Principle

An interatomic system may contain relevant structure at more than one spatial, topological, or representational scale.

EIF therefore permits a family of scale-indexed representations rather than requiring one universal local environment.

The multiscale principle is:

`one physical configuration`

`→ multiple explicitly declared scale views`

`→ scale-specific representations`

`→ typed cross-scale relations`

The different scale views remain mathematically distinct.

## 5. Scale Index Set

Let:

`L_EIF`

be a finite nonempty scale index set.

Its elements are written:

`ell ∈ L_EIF`

A scale index is an abstract identifier.

It does not by itself imply:

- physical length;
- graph depth;
- time scale;
- energy scale;
- resonance scale.

The interpretation of every scale must be declared.

## 6. Ordered Scale Set

A model may define an ordering:

`ell_0 < ell_1 < ... < ell_M`

when the scale semantics support such an order.

The order may represent increasing:

- spatial support;
- graph support;
- aggregation level;
- coarse-graining level;
- another explicitly defined quantity.

An ordering must not be introduced when the scales are not meaningfully ordered.

## 7. Scale Is Not Necessarily Length

A scale may be defined through a physical radius, but it may also be defined through:

- graph depth;
- partition hierarchy;
- interaction class;
- representation resolution;
- environment family.

Therefore:

`scale index ≠ physical length automatically`

## 8. Scale Parameter Space

For every scale `ell`, define a scale-parameter space:

`Λ_ell`

with parameter state:

`λ_ell ∈ Λ_ell`

Scale parameters may include:

- cutoff radius;
- neighborhood depth;
- cluster rule;
- basis resolution;
- channel multiplicity;
- coarse-graining parameters;
- physical-output parameters.

Every numerical parameter requires provenance.

## 9. Scale-Specific Source State

The same interatomic configuration:

`q ∈ Q_adm`

may generate different scale-specific source states.

Define:

`S_ell`

as the source state space used at scale `ell`.

A scale extraction mapping is:

`P_ell: Q_adm × Λ_ell → S_ell`

## 10. Scale Projection

The mapping:

`P_ell`

may be:

- lossless;
- information-reducing;
- local;
- global;
- topology-dependent;
- history-dependent in a later dynamic specialization.

Its information behavior must be declared.

## 11. Scale Projection Is Not Coordinate Projection Automatically

The word:

`projection`

in the multiscale architecture means a declared mapping into a scale-specific state.

It does not imply an orthogonal linear projection unless that property is explicitly defined.

## 12. Scale-Specific Topology

Let:

`X_G,ell`

be the topology space at scale `ell`.

A scale-specific topology constructor is:

`G_ell: Q_adm × X_B × Λ_ell → X_G,ell`

The topology may differ across scales.

## 13. Scale-Specific Neighborhood

For central site `i`, let:

`N_i,ell`

denote its neighborhood at scale `ell`.

Different scales may produce:

`N_i,ell_a ≠ N_i,ell_b`

for the same configuration.

## 14. Nested Neighborhoods

A model may require:

`N_i,ell_a ⊆ N_i,ell_b`

when:

`ell_a < ell_b`

Such nesting is a model property.

It is not universal.

## 15. Non-Nested Neighborhoods

Scale-specific neighborhoods may also be non-nested.

For example, one scale may represent:

- short-range geometric interactions;

while another represents:

- chemically selected or topology-defined interactions.

Therefore:

`multiscale ≠ nested cutoffs only`

## 16. Scale-Specific Local Environment

Define:

`X_env,ell`

as the local-environment space at scale `ell`.

The environment mapping is:

`E_i,ell: Q_adm × X_G,ell × X_B → X_env,ell`

with:

`e_i,ell = E_i,ell(q, G_ell, b)`

## 17. Scale Identity Must Be Preserved

Two environments with numerically identical stored values but belonging to different scale contracts are not automatically the same mathematical object.

Therefore:

`e_i,ell_a ≠ e_i,ell_b`

as typed objects unless an explicit identification is defined.

## 18. Multiscale Environment State

For a fixed site `i`, define:

`X_env,MS = ∏_(ell ∈ L_EIF) X_env,ell`

A multiscale environment state is:

`e_i,MS = (e_i,ell)_(ell ∈ L_EIF)`

## 19. Scale Product Does Not Imply Independence

The product-space representation records separate scale channels.

It does not imply statistical, dynamical, or physical independence between them.

## 20. Scale-Specific Representation Space

For each scale `ell`, define:

`Y_EIF,ell`

as the representation space.

A scale-specific representation mapping is:

`Φ_ell: X_env,ell → Y_EIF,ell`

## 21. Scale-Specific Local Representation

For site `i`:

`h_i,ell = Φ_ell(e_i,ell)`

with:

`h_i,ell ∈ Y_EIF,ell`

The representation type may differ between scales.

## 22. Scale-Specific Transformation Action

Let the declared symmetry group be:

`G_sym`

For every scale `ell`, define:

`ρ_ell: G_sym × Y_EIF,ell → Y_EIF,ell`

The action may contain scale-specific representation channels.

## 23. Scale-Specific Equivariance

A scale representation is equivariant when:

`Φ_ell(ρ_env,ell(g)e) = ρ_ell(g)Φ_ell(e)`

for all admissible:

`g ∈ G_sym`

and:

`e ∈ X_env,ell`

## 24. Scale-Specific Invariance

If the output action is trivial at scale `ell`, then:

`Φ_ell(ρ_env,ell(g)e) = Φ_ell(e)`

for the transformations included in the invariance contract.

## 25. Symmetry Can Differ Across Outputs

A model may contain:

- invariant channels at one scale;
- equivariant channels at another;
- mixed channels within one scale.

Multiscale structure does not require identical output types at every scale.

## 26. Multiscale Representation Space

Define:

`Y_EIF,MS = ∏_(ell ∈ L_EIF) Y_EIF,ell`

The complete scale-indexed representation is:

`h_i,MS = (h_i,ell)_(ell ∈ L_EIF)`

## 27. Multiscale Representation Is Not One Scalar

The complete state:

`h_i,MS`

must not be replaced silently by one scalar aggregate when scale-specific information matters.

Therefore:

`multiscale representation ≠ global scalar`

## 28. Hierarchical Structure

A multiscale representation becomes hierarchical when explicit parent-child or coarse-fine relations are defined between scale objects.

Hierarchy requires relations.

A collection of multiple scales alone does not establish a hierarchy.

Therefore:

`multiscale ≠ hierarchical automatically`

## 29. Hierarchy Index Relation

Let:

`≺`

denote a declared parent-child relation on scale objects or scale indices.

For example:

`ell_a ≺ ell_b`

may indicate that `ell_b` is a coarser parent scale of `ell_a`.

The relation must be defined independently of notation.

## 30. Hierarchical Partition

At scale `ell`, let:

`P_ell = {B_ell,1, ..., B_ell,n_ell}`

be a partition of a declared site set when a partition-based hierarchy is used.

Each block:

`B_ell,k`

is a nonempty subset of sites.

## 31. Partition Requirements

A partition satisfies:

- every block is nonempty;
- blocks are pairwise disjoint;
- their union equals the declared represented set.

If overlaps are allowed, the structure is not a partition and must be represented as a cover or another relation.

## 32. Hierarchical Partition Refinement

A fine partition `P_a` refines a coarse partition `P_b` when every fine block is contained in a coarse block.

This relation may be used to define a strict hierarchy.

It is not mandatory for all multiscale EIF models.

## 33. Overlapping Scale Cover

Let:

`C_ell = {C_ell,1, ..., C_ell,m_ell}`

be an overlapping cover.

Then different elements may satisfy:

`C_ell,a ∩ C_ell,b ≠ ∅`

Overlapping covers can represent shared local or mesoscale environments.

## 34. Overlap Is Not Duplication of Physical Atoms

A physical site may appear in more than one scale object or cluster.

This is representation overlap.

It does not mean that the physical atom has been duplicated.

## 35. Group-Level State

Let:

`B ⊆ V_N`

be a declared site group.

A group representation may belong to:

`Y_B`

and may be produced through:

`A_B: ∏_(i ∈ B) Y_i → Y_B`

## 36. Aggregation Mapping

An aggregation mapping combines fine-scale objects into a coarser representation.

For scales:

`ell_f`

and:

`ell_c`

define:

`A_(ell_f→ell_c): Y_EIF,ell_f → Y_EIF,ell_c`

when such a direct cross-scale map exists.

## 37. Aggregation Domain May Be Structured

The aggregation source may instead be a family:

`∏_(k ∈ I_c) Y_EIF,ell_f,k`

associated with the children of one coarse object.

The exact domain must be declared.

## 38. Aggregation Is Not Necessarily Linear

A cross-scale aggregation may be:

- linear;
- nonlinear;
- learned;
- analytical;
- invariant;
- equivariant.

No universal form is imposed.

## 39. Coarse-Graining

A coarse-graining mapping is an information-reducing transformation from a finer representation or state into a coarser one.

A generic map is:

`C_(f→c): Y_f → Y_c`

The map must declare what information it preserves.

## 40. Coarse-Graining Is Not Averaging Automatically

A coarse-graining map may use averaging, but it may also use:

- sums;
- moments;
- invariant contractions;
- equivariant aggregation;
- learned mappings;
- graph pooling;
- physically constrained reduction.

Therefore:

`coarse-graining ≠ averaging`

## 41. Restriction Mapping

A restriction mapping selects or computes a lower-resolution representation from a higher-resolution state.

Write:

`R_(f→c): Y_f → Y_c`

The word `restriction` does not imply a specific numerical algorithm.

## 42. Refinement Mapping

A refinement or lifting mapping may be defined as:

`L_(c→f): Y_c → Y_f`

It produces a fine-space representation from coarse information.

## 43. Refinement Is Not Inverse Automatically

In general:

`L_(c→f)(R_(f→c)(y_f)) ≠ y_f`

because coarse-graining can destroy information.

Therefore:

`refinement ≠ exact inversion`

unless an inverse property is explicitly proven.

## 44. Information Loss Under Coarse-Graining

If there exist:

`y_a ≠ y_b`

such that:

`C_(f→c)(y_a) = C_(f→c)(y_b)`

then the coarse-graining map is many-to-one.

The lost distinction cannot be recovered from the coarse state alone.

## 45. Coarse State Is Not Fine State

Therefore:

`coarse representation ≠ compressed notation for exact fine state`

unless the mapping is known to be invertible over the declared domain.

## 46. Scale-Specific Information Content

Every scale representation must declare the categories of information it retains.

Possible retained information includes:

- composition;
- local geometry;
- orientation;
- symmetry type;
- aggregate density;
- tensor moments;
- topology;
- physical outputs.

No universal content set is imposed.

## 47. Scale-Specific Information Loss

Possible losses include:

- exact atomic coordinates;
- site identity;
- orientation;
- chirality;
- local topology;
- high-angular-order channels;
- long-range correlations;
- fine-scale physical outputs.

These losses must be traceable.

## 48. Cross-Scale Symmetry Contract

A cross-scale mapping claiming equivariance must define transformation actions on both source and target spaces.

For:

`A: Y_f → Y_c`

equivariance requires:

`A(ρ_f(g)y) = ρ_c(g)A(y)`

for every admissible:

`g ∈ G_sym`

and:

`y ∈ Y_f`

## 49. Cross-Scale Intertwiner

An equivariant linear cross-scale map is an intertwiner between the fine and coarse representation actions.

Arbitrary pooling is not an intertwiner automatically.

## 50. Invariant Cross-Scale Map

A cross-scale map producing an invariant output may satisfy:

`A(ρ_f(g)y) = A(y)`

The target then carries the trivial action for the declared transformation.

## 51. Permutation Across Scale Aggregation

When fine-scale site indices are permuted consistently, a group-level representation must remain invariant or transform according to the declared group-object correspondence.

The exact relation depends on whether the coarse objects themselves retain labels.

## 52. Unlabeled Group Representation

A representation associated with an unlabeled set of sites should not depend on arbitrary ordering of those sites.

The aggregation must therefore be permutation invariant with respect to storage order inside the group.

## 53. Labeled Group Representation

If a coarse object remains associated with a parent index, the collection of parent representations can transform equivariantly under reindexing of the parent objects.

## 54. Atomic Permutation and Cluster Assignment

A cluster definition based on physical geometry or invariant properties should remain correspondingly unchanged under pure computational reindexing.

Its stored indices must simply be relabeled consistently.

## 55. Storage-Order-Dependent Clustering Is Invalid

A cluster constructor whose physical result changes under arbitrary array ordering violates the permutation contract unless storage order is itself part of the modeled state.

## 56. Geometric Transformation of Hierarchy

Rigid translation or rotation of a configuration must preserve hierarchy membership when that hierarchy is defined entirely by rigid-motion invariant criteria.

If hierarchy membership depends on orientation relative to an external frame, the external frame must be part of the source state.

## 57. Scale-Dependent Locality

For each scale `ell`, define a locality relation:

`Loc_ell`

The locality may be specified through:

- radius;
- graph depth;
- cluster membership;
- hierarchical parent relation;
- another explicit dependency.

## 58. Locality Radius

If a physical radius is used, define:

`r_ell > 0`

with compatible length units.

No universal sequence of radii is defined by EIF.

## 59. Nested Radius Model

A specialization may impose:

`r_ell0 < r_ell1 < ... < r_ellM`

This defines increasing geometric support.

It remains a model-specific choice.

## 60. Scale Radius Is Not Interaction Cutoff Automatically

A representation radius controls information exposure.

It does not establish that physical interaction vanishes outside that radius.

Therefore:

`representation scale radius ≠ universal physical interaction range`

## 61. Graph-Depth Scale

A model may define scale by:

`k_ell`

graph hops.

This is topological rather than directly geometric.

Therefore:

`graph-depth scale ≠ distance scale`

## 62. Physical and Computational Scales Remain Distinct

A computational hierarchy can be introduced for efficiency without each level corresponding to a distinct physical scale.

The physical interpretation must not be inferred from the hierarchy alone.

## 63. Multiscale Geometry

A scale may retain different geometric orders.

For example, one scale may retain:

- pair distances;

another:

- angular correlations;

another:

- collective tensors.

The representation content must be explicit.

## 64. Multiscale Equivariant Channels

For scale `ell`, an equivariant representation may contain channels:

`Y_(ell,l,p)`

indexed by:

- scale `ell`;
- rotational degree `l`;
- parity `p` where applicable.

## 65. Full Typed Channel Identity

A channel identity may therefore require:

`(ell, l, p, m, c)`

where:

- `ell` is scale;
- `l` is representation degree;
- `p` is parity;
- `m` is representation component;
- `c` is multiplicity or channel index.

The exact storage convention remains implementation-specific.

## 66. Same l Does Not Mean Same Scale

Two channels with equal rotational degree but different scale indices remain distinct representation channels.

Therefore:

`same transformation type ≠ same information scale`

## 67. Same Scale Does Not Mean Same Representation Type

A single scale may contain scalar, vector, and higher-order channels.

Therefore:

`same scale ≠ same symmetry type`

## 68. Scale Fusion

A model may combine information from multiple scales into one representation.

Define:

`F_MS: Y_EIF,MS → Y_fused`

The fusion mapping must declare:

- input scale set;
- output space;
- transformation action;
- information loss;
- locality;
- dimensional meaning.

## 69. Fusion Is Not Concatenation Automatically

Simple concatenation is one possible fusion strategy.

Other strategies include:

- weighted sums;
- tensor-product coupling;
- attention-like mappings;
- invariant contraction;
- hierarchical aggregation.

No universal fusion operator is imposed.

## 70. Scale Weight

If a fusion uses scale weights:

`w_ell`

their mathematical type and provenance must be defined.

A weight may be:

- constant;
- learned;
- state-dependent;
- normalized;
- dimensional;
- dimensionless.

## 71. Scale Weight Is Not Physical Importance Automatically

A learned or numerical scale weight does not automatically measure physical importance.

It is a model parameter unless independently interpreted.

## 72. Normalized Scale Weights

A model may impose:

`Σ_ell w_ell = 1`

This is a normalization convention.

It does not establish that the scales form a physical probability decomposition.

## 73. Scale Attention Boundary

A normalized attention coefficient is not automatically:

- probability;
- causal influence;
- energy fraction;
- force fraction;
- resonance contribution.

Its semantics depend on the declared mapping.

## 74. Hierarchical Message Flow

A computational hierarchy may propagate information:

`fine → coarse`

`coarse → fine`

or both.

The existence of information flow does not itself define physical causality.

## 75. Bottom-Up Mapping

A bottom-up map is:

`B_(f→c): Y_f → Y_c`

It aggregates or transforms fine-scale information into a coarse state.

## 76. Top-Down Mapping

A top-down map is:

`T_(c→f): Y_c → Y_f,target`

It injects coarse information into a fine-scale update or representation.

## 77. Top-Down Mapping Is Not Reconstruction Automatically

A top-down signal may condition fine-scale state without reconstructing its lost information.

Therefore:

`coarse-to-fine feedback ≠ exact fine-state recovery`

## 78. Bidirectional Hierarchy

A bidirectional hierarchy contains both bottom-up and top-down mappings.

Their composition must be defined explicitly.

No inverse relation is implied.

## 79. Hierarchical State Space

Let:

`Y_HIER = ∏_(ell ∈ L_EIF) Y_EIF,ell`

together with declared cross-scale mappings.

The product alone is a multiscale state.

The mapping relations provide the hierarchy.

## 80. Hierarchical Consistency

A hierarchy may impose compatibility relations between scales.

For example:

`C_(f→c)(h_f) = h_c`

for states considered internally consistent.

Such a relation is model-specific.

## 81. Independent Scale State

A model may instead allow scale states to be computed through different mappings without requiring exact coarse-graining consistency.

The architecture must state which semantics apply.

## 82. Hierarchy Residual

When an expected coarse relation exists, define a hierarchy residual:

`e_H = d_c(C_(f→c)(h_f), h_c)`

where:

`d_c`

is a declared comparison measure.

## 83. Exact Hierarchy Consistency

Exact consistency requires:

`e_H = 0`

under exact mathematics.

A numerical implementation may use a declared tolerance.

## 84. Numerical Hierarchy Tolerance

For numerical comparison:

`e_H ≤ epsilon_H`

where:

`epsilon_H ≥ 0`

and its provenance is defined.

The tolerance does not redefine exact consistency.

## 85. Cross-Scale Validation Is Not Physical Validation

A hierarchy may be internally consistent while still being physically inaccurate.

Therefore:

`cross-scale consistency PASS ≠ physical validation`

## 86. Multiscale Physical Output

A physical-output specialization may derive outputs from one or more scales.

Let:

`M_phys,MS: Y_EIF,MS × Λ_phys → Y_phys`

The model must specify which scales contribute.

## 87. Single-Scale Physical Output

A physical output may depend only on one scale:

`M_phys,ell: Y_EIF,ell → Y_phys`

Such a model makes a scale-sufficiency assumption that requires validation.

## 88. Multiscale Energy Mapping

A multiscale energy model may define:

`E_MS: Y_EIF,MS × Λ_E → ℝ`

with a declared physical energy unit.

No universal decomposition is imposed.

## 89. Additive Scale Energy

A specialization may define:

`E_total = Σ_(ell ∈ L_EIF) E_ell`

where each:

`E_ell`

is a declared scale contribution.

This decomposition is model-specific.

## 90. Scale Energy Decomposition Is Not Unique

Different decompositions may yield the same total energy.

Therefore:

`scale energy contribution ≠ uniquely measurable physical energy`

in general.

## 91. Double-Counting Boundary

When multiple scales contain overlapping information, additive energy contributions can double count the same physical interaction if the mapping is not constructed to avoid or compensate for overlap.

A multiscale energy model must define its counting semantics.

## 92. Overlap Does Not Imply Double Counting Automatically

Overlapping representations are allowed.

Double counting occurs only if the physical-output composition counts the same modeled contribution redundantly.

Representation overlap and energy double counting are different concepts.

## 93. Partition-of-Contribution Contract

An additive physical model may impose a relation such as:

`E_total = Σ_ell E_ell`

with the scale terms deliberately defined as a complete nonredundant decomposition.

That property must be established rather than inferred from notation.

## 94. Correction Hierarchy

A model may instead use:

`E_total = E_base + ΔE_1 + ... + ΔE_M`

where each correction is defined relative to prior levels.

This can avoid some forms of repeated baseline contribution.

The correction semantics must be explicit.

## 95. Scale Correction Is Not Error Automatically

A term:

`ΔE_ell`

may be a model correction component.

It is not necessarily prediction error against reference data.

## 96. Force from Multiscale Energy

If:

`E_MS(q)`

is differentiable with respect to atomic coordinates, define:

`f_i = -grad_(x_i) E_MS`

The force includes derivatives through every scale-dependent path by which `x_i` affects the total energy.

## 97. Scale Force Decomposition

If:

`E_MS = Σ_ell E_ell`

and every component is differentiable, then:

`f_i = Σ_ell f_i,ell`

with:

`f_i,ell = -grad_(x_i) E_ell`

This decomposition follows from linearity of differentiation.

## 98. Scale Force Contribution Is Model-Dependent

As with local energy decomposition, a scale force decomposition need not be unique across different model constructions.

## 99. Cross-Scale Derivative Path

If a coarse representation depends on fine geometry through:

`h_c = C(h_f(q))`

then the energy derivative must include the complete chain:

`q → h_f → h_c → E`

A computational implementation that detaches or omits this dependency realizes a different force mapping.

## 100. Gradient Path Must Match Energy Path

For a model claiming energy-derived forces, all result-affecting differentiable paths from coordinates to total energy must be included in the gradient.

Therefore:

`partial computational gradient ≠ full model force`

unless the omitted paths are intentionally outside the declared energy dependence.

## 101. Hierarchy and Conservative Structure

A hierarchical architecture can remain conservative when its final force is derived from one differentiable scalar total energy.

Hierarchy does not break conservativity by itself.

## 102. Direct Multiscale Force Mapping

A model may instead define:

`F_MS,direct: Y_EIF,MS → Y_F`

without a scalar energy.

Such a mapping may be equivariant but is not automatically conservative.

## 103. Multiscale Equivariance Does Not Imply Conservativity

Therefore:

`multiscale equivariant force ≠ conservative force automatically`

## 104. Scale-Specific Stress Contribution

A specialization may define scale-dependent stress-like outputs.

Every such output requires the stress contract from Chapter 04.

Scale labeling does not resolve stress-convention ambiguity automatically.

## 105. Physical Dimensions Across Scales

Channels combined additively must have compatible dimensions.

A dimensional energy contribution cannot be added directly to a dimensionless representation coefficient.

## 106. Scale Normalization and Units

Normalizing a scale representation can change numerical magnitude while preserving its abstract information.

The normalization must not erase the physical-unit relation required by downstream outputs.

## 107. Dimensionless Coarse State

A coarse representation may be dimensionless even when derived from dimensional geometry.

The mapping from dimensional source to dimensionless state must be defined.

## 108. Scale-Dependent Basis

Each scale may use a different basis or feature resolution.

The basis convention must remain explicit wherever representations are exchanged across scales.

## 109. Basis Conversion Across Scales

If two scales use different compatible bases for the same transformation type, a cross-scale mapping must include the basis conversion.

Numeric component identity cannot be assumed.

## 110. Angular Truncation by Scale

A model may use:

`l_max,ell`

as a scale-specific maximum angular degree.

EIF defines no universal relationship between `ell` and `l_max,ell`.

## 111. Coarser Scale Does Not Mean Lower Angular Order Automatically

A coarse spatial scale may still require high-order angular information.

Therefore:

`coarse spatial scale ≠ low angular resolution automatically`

## 112. Fine Scale Does Not Mean Complete Representation

A short-range high-resolution environment can still omit long-range information.

Therefore:

`fine scale ≠ complete system state`

## 113. Scale and Resolution Remain Distinct

Physical support scale and representation resolution are separate model dimensions.

A representation may have:

- large support with low feature resolution;
- small support with high feature resolution;
- large support with high resolution;
- small support with low resolution.

## 114. Resolution Index

If required, define a separate representation-resolution index:

`r ∈ R_EIF`

rather than overloading the physical or topological scale index.

## 115. Scale-Resolution Product Space

A representation may therefore be indexed by:

`(ell, r)`

with state space:

`Y_(ell,r)`

The two indices must retain separate semantics.

## 116. Scale and Time Remain Distinct

This chapter defines interatomic representation scales.

It does not define temporal scale.

Therefore:

`spatial / hierarchical scale ≠ time scale`

Dynamic time dependence belongs to a later evolution layer.

## 117. Scale and Resonance Remain Distinct

EIF scale indices are not TR resonance coordinates.

Therefore:

`EIF scale ≠ resonance state`

and:

`cross-scale transition ≠ resonance transition`

## 118. Scale and Ternary State Remain Distinct

A hierarchy level does not correspond automatically to:

`-1`

`0`

or:

`1`

Therefore:

`fine / intermediate / coarse ≠ -1/0/1`

## 119. Three-Level Hierarchy Is Not Ternary Logic

Even when a model contains exactly three hierarchy levels, those levels are not balanced ternary states unless an explicit mapping defines that semantics.

## 120. Hierarchical Transition Is Not Ternary Transition

Moving information between hierarchy levels is a representation operation.

It is not an executed ternary state transition.

## 121. Cross-Scale Change Is Not Bifurcation

A change in coarse representation or cluster membership is not automatically a dynamical bifurcation.

A bifurcation claim remains governed by the mathematical requirements established in Volume 02.

## 122. Cluster Change Is Not Physical Phase Transition

A computational cluster assignment may change because of:

- cutoff;
- threshold;
- clustering rule;
- geometry change.

This is not automatically a physical phase transition.

## 123. Coarse Structural Descriptor Is Not Physical Phase

A coarse structural descriptor may help classify physical structure.

It does not become a thermodynamic phase state without an independently defined criterion.

## 124. Scale Aggregation Is Not Causality

A bottom-up map:

`fine → coarse`

describes information transformation.

It does not prove that the fine representation physically causes the coarse phenomenon.

## 125. Top-Down Conditioning Is Not Physical Force

A coarse-to-fine computational signal is not automatically a mechanical force.

If it modifies a physical force mapping, that relation must be defined explicitly.

## 126. Hierarchical Edge Is Not Physical Interaction

A parent-child relation in a computational hierarchy is not automatically:

- chemical bond;
- force channel;
- physical contact;
- resonance coupling.

## 127. Scale Graph

A hierarchical realization may define a graph:

`G_H = (V_H, E_H)`

whose nodes represent objects at multiple scales.

The node types and edge semantics must be declared.

## 128. Cross-Scale Edge

An edge connecting a fine object to a coarse object encodes a computational or mathematical relation.

Its physical meaning must not be inferred from graph connectivity alone.

## 129. Typed Hierarchical Graph

Every node and edge in a hierarchical graph should retain:

- scale;
- object identity;
- representation type;
- transformation type;
- locality;
- provenance.

An untyped graph is insufficient for the full EIF contract.

## 130. Cross-Scale Tensor Product

Representations from different scales may be combined through a transformation-compatible tensor product.

The resulting channel type follows the representation-theoretic coupling rules inherited from Chapter 03.

## 131. Cross-Scale Tensor Product Is Not Physical Multiplication

The mathematical product of representation channels does not automatically correspond to multiplication of physical observables.

## 132. Scale-Invariant Scalar Fusion

Invariant scalar channels from different scales may be combined through a declared scalar mapping.

Their dimensions must remain compatible if they represent physical quantities.

## 133. Cross-Scale Vector Fusion

Vector channels from different scales can be added only when:

- they share compatible vector transformation behavior;
- their dimensions are compatible;
- their semantic roles permit addition.

## 134. Same Transformation Type Is Not Sufficient for Addition

Two vectors may both transform as polar vectors yet represent different physical or latent quantities.

Transformation compatibility does not alone establish semantic compatibility.

## 135. Multiscale Permutation Contract

A multiscale model must preserve atomic reindexing through every scale.

This includes:

- fine topology;
- coarse grouping;
- group membership;
- environment extraction;
- representation;
- cross-scale mappings;
- physical outputs.

## 136. Multiscale Translation Contract

Every scale must preserve the declared translation behavior.

Relative geometric representations may be translation invariant, while explicitly position-dependent coarse channels require their own action.

## 137. Multiscale Rotation Contract

Every non-scalar channel must transform through the declared representation action at its scale.

Cross-scale mappings must preserve compatibility between these actions.

## 138. Multiscale Reflection Contract

If `O(3)` or `E(3)` behavior is claimed, parity-sensitive information must remain consistent through aggregation and cross-scale coupling.

## 139. Chirality Across Scales

A coarse representation that removes reflection-sensitive information cannot later support a chirality-sensitive output unless another channel preserves that information.

## 140. Scale Pooling and Chirality Loss

Invariant pooling that identifies reflected states may erase chirality.

The information-loss boundary must be declared.

## 141. Multiscale Completeness

A multiscale representation may be more informative than any one constituent scale.

It is not automatically complete.

Completeness remains relative to a declared equivalence relation and target claim.

## 142. Redundant Scales

Two scales may encode overlapping or redundant information.

Redundancy is not invalid.

It must simply be distinguished from independent information.

## 143. Redundancy and Robustness

A model may deliberately retain redundant channels for numerical or predictive robustness.

That is an implementation or modeling choice.

Redundancy does not imply additional physical degrees of freedom.

## 144. Scale-Specific Provenance

Every scale should retain provenance for:

- scale definition;
- topology rule;
- cutoff or locality rule;
- basis;
- channel types;
- learned parameters;
- calibration state;
- physical-output contribution.

## 145. Cross-Scale Mapping Provenance

Every cross-scale mapping should retain:

- source scale;
- target scale;
- algorithm or equation;
- parameter state;
- information-loss declaration;
- transformation contract;
- validation status.

## 146. Scale Versioning

Changing a scale definition changes the semantics of the corresponding representation.

Therefore artifacts produced under different scale definitions must not be treated as equivalent automatically.

## 147. Multiscale Trace Identity

A future executable multiscale trace must identify the scale of every scale-dependent field.

A numeric value without scale identity may be semantically incomplete.

## 148. Missing Scale Channel

Absence of a scale channel is not equivalent to a zero-valued scale representation.

Therefore:

`missing scale ≠ zero scale state`

## 149. Zero Scale Representation

A valid zero vector or zero scalar at one scale is a mathematical value in its declared space.

It must not be overloaded as:

- missing data;
- inactive scale;
- ternary neutral state.

## 150. Multiscale Validation Classes

A multiscale EIF realization must separate:

- scale-definition validation;
- topology validation;
- environment validation;
- transformation validation;
- cross-scale consistency validation;
- information-loss validation;
- physical-output validation;
- empirical validation.

## 151. Scale-Definition Validation

Scale-definition validation checks that each scale has:

- explicit meaning;
- declared parameters;
- valid source domain;
- valid locality rule;
- valid topology rule;
- provenance.

## 152. Scale Topology Validation

For every scale, topology validation must check:

- node correspondence;
- edge semantics;
- locality;
- periodic handling;
- permutation correspondence;
- transformation consistency.

## 153. Cross-Scale Membership Validation

If fine objects belong to coarse groups, validation must check:

- valid parent identity;
- allowed multiplicity;
- partition or cover semantics;
- deterministic correspondence.

## 154. Partition Validation

For a declared partition, validation must confirm:

- nonempty blocks;
- pairwise disjointness;
- complete coverage of the represented set.

## 155. Cover Validation

For an overlapping cover, validation must confirm the declared coverage semantics without incorrectly enforcing disjointness.

## 156. Cross-Scale Equivariance Validation

For:

`A_(f→c)`

validate:

`A_(f→c)(ρ_f(g)y)`

against:

`ρ_c(g)A_(f→c)(y)`

using exact or declared numerical comparison.

## 157. Cross-Scale Permutation Validation

Reindexing the atomic configuration must produce correspondingly reindexed:

- fine objects;
- coarse memberships;
- scale representations;
- cross-scale outputs.

## 158. Cross-Scale Information-Loss Validation

A model must document whether a coarse map is:

- injective;
- many-to-one;
- invertible on a restricted domain;
- approximate;
- stochastic;
- learned.

Unknown information loss must not be described as exact preservation.

## 159. Coarse-Fine Round-Trip Validation

If both restriction and refinement exist, a round-trip test may evaluate:

`y_f`

against:

`L_(c→f)(R_(f→c)(y_f))`

The expected result depends on the declared information-loss contract.

Exact equality must not be required when the model is intentionally lossy.

## 160. Coarse Consistency Validation

If a coarse state is expected to equal the restriction of a fine state, validate:

`h_c`

against:

`R_(f→c)(h_f)`

using the declared comparison relation.

## 161. Physical-Output Consistency Across Scales

If two representations are claimed to produce the same total physical output, the validation must define the expected equality or tolerance explicitly.

No equality follows merely because they describe the same underlying configuration.

## 162. Energy Decomposition Validation

For an additive multiscale energy model, validate:

`E_total = Σ_ell E_ell`

under the model's exact or numerical arithmetic semantics.

This confirms internal accounting.

It does not establish physical accuracy.

## 163. Force Consistency Validation

If force is claimed to derive from total multiscale energy, validate:

`F = -grad_x E_total`

through the complete multiscale computational graph.

## 164. Double-Counting Validation

An additive multiscale physical model must provide evidence that its composition matches the declared counting semantics.

The test depends on the decomposition design.

There is no universal double-counting detector.

## 165. Transformation Validation Across Physical Outputs

If scale representations are transformed, physical outputs must satisfy their output transformation contracts.

For example:

- energy remains invariant where required;
- force transforms equivariantly;
- stress follows its tensor action.

## 166. Exact and Numerical Validation Remain Distinct

An exact cross-scale relation is not replaced by a numerical tolerance.

Numerical tolerance applies to implementation comparison only.

## 167. Empirical Scale Validation

A claim that one set of scales is physically sufficient requires independent evidence for the intended domain.

Internal hierarchy consistency is not sufficient.

## 168. Scale Ablation Boundary

Removing one scale in a computational study may provide evidence about model dependence on that scale.

It does not by itself prove that the corresponding physical length or hierarchy level is causally fundamental.

## 169. Learned Scale Selection

A model may learn scale weighting or selection.

The learned result is an implementation outcome.

It does not become a universal physical scale law automatically.

## 170. Multiscale Benchmark Boundary

Benchmark improvements from multiscale architecture establish performance under the benchmark conditions.

They do not establish universal physical superiority.

## 171. Core Multiscale Invariants

The following invariants are mandatory.

1. Every scale has explicit semantics.

2. Scale index remains distinct from physical length unless mapped explicitly.

3. Multiscale structure remains distinct from hierarchy.

4. Hierarchy requires explicit cross-scale relations.

5. Scale-specific topology remains explicitly typed.

6. Scale-specific environments remain explicitly typed.

7. Scale identity is preserved.

8. Multiscale representation remains distinct from one scalar aggregate.

9. Aggregation remains distinct from averaging.

10. Coarse-graining may be information-reducing.

11. Refinement remains distinct from exact inversion.

12. Coarse state remains distinct from fine state.

13. Cross-scale equivariance requires source and target actions.

14. Arbitrary pooling is not assumed equivariant.

15. Permutation correspondence must persist across scales.

16. Translation behavior must persist across scales.

17. Rotation behavior must persist across scales.

18. Reflection behavior must persist when claimed.

19. Hierarchy remains distinct from equivariance.

20. Scale remains distinct from representation resolution.

21. Spatial scale remains distinct from temporal scale.

22. EIF scale remains distinct from TR resonance state.

23. Hierarchy level remains distinct from ternary state.

24. Three hierarchy levels do not imply ternary semantics.

25. Hierarchical transition remains distinct from ternary transition.

26. Cross-scale change remains distinct from bifurcation.

27. Cluster change remains distinct from physical phase transition.

28. Computational hierarchy edge remains distinct from physical interaction.

29. Scale weights remain model parameters unless independently interpreted.

30. Attention weights remain distinct from physical probability or energy fraction.

31. Multiscale energy decomposition is not assumed unique.

32. Overlapping representation does not automatically imply physical double counting.

33. Additive physical-output composition requires explicit counting semantics.

34. Energy-derived forces must include every declared differentiable scale path.

35. Direct multiscale force prediction does not imply conservativity.

36. Physical dimensions must remain compatible across scale fusion.

37. Same transformation type does not imply semantic equivalence.

38. Same scale does not imply same representation type.

39. Same representation type does not imply same scale.

40. Missing scale channel remains distinct from zero scale value.

41. Cross-scale consistency remains distinct from physical validation.

42. Scale sufficiency remains claim-relative.

43. Scale-specific provenance is mandatory.

44. Information loss remains traceable.

45. No cross-scale mapping acquires TR semantics without explicit integration.

## 172. Formal Non-Equivalences

The following non-equivalences are mandatory:

`scale index ≠ physical length automatically`

`multiscale ≠ hierarchical automatically`

`hierarchy ≠ equivariance`

`coarse-graining ≠ averaging`

`restriction ≠ exact projection automatically`

`refinement ≠ exact inverse`

`coarse state ≠ fine state`

`multiscale representation ≠ global scalar`

`scale radius ≠ physical interaction boundary`

`graph-depth scale ≠ Euclidean distance scale`

`computational scale ≠ physical scale automatically`

`scale ≠ representation resolution`

`spatial scale ≠ time scale`

`same l ≠ same scale`

`same scale ≠ same symmetry type`

`same symmetry type ≠ same semantic quantity`

`scale fusion ≠ concatenation automatically`

`scale weight ≠ physical importance`

`attention weight ≠ physical probability`

`bottom-up mapping ≠ physical causality`

`top-down mapping ≠ physical force`

`coarse-to-fine feedback ≠ exact reconstruction`

`hierarchy edge ≠ physical interaction`

`hierarchy level ≠ ternary state`

`three hierarchy levels ≠ -1/0/1`

`cross-scale transition ≠ ternary transition`

`cross-scale change ≠ bifurcation`

`cluster change ≠ physical phase transition`

`scale energy contribution ≠ uniquely measurable energy`

`representation overlap ≠ physical double counting automatically`

`multiscale equivariance ≠ conservativity`

`cross-scale consistency PASS ≠ physical validation`

`missing scale ≠ zero scale state`

`zero scale value ≠ ternary neutral 0`

## 173. Formal Multiscale Representation Chain

The EIF multiscale chain is:

`interatomic configuration`

`→ scale definitions`

`→ scale-specific topology`

`→ scale-specific local environments`

`→ scale-specific invariant / equivariant representations`

`→ cross-scale aggregation / restriction / coupling`

`→ hierarchical EIF state`

`→ multiscale physical output where independently defined`

Every scale and every cross-scale arrow has its own typed semantics.

## 174. Formal Hierarchical Chain

For a strict fine-to-coarse hierarchy:

`fine atomic representation`

`→ local group representation`

`→ cluster representation`

`→ coarse collective representation`

may be used when every map is explicitly defined.

The words:

`local`

`cluster`

`coarse`

do not establish universal physical scales.

## 175. Multiscale Physical-Output Chain

A conservative multiscale energy specialization may follow:

`q`

`→ {h_ell(q)}_(ell ∈ L_EIF)`

`→ E_MS({h_ell})`

`→ F = -grad_x E_MS`

All scale dependencies contributing to `E_MS` belong to the force derivative.

## 176. TR-EIF Boundary

The multiscale EIF state remains an EIF object.

It does not belong automatically to:

`X_TR,in`

`X_R`

`R_C`

or:

`T = {-1, 0, 1}`

No scale channel is automatically a resonance coordinate.

No hierarchy level is automatically a ternary state.

## 177. Future EIF-to-TR Multiscale Mapping

A later integration layer may define:

`M_E→TR,MS: Y_EIF,MS → X_TR,in`

or a mapping from a selected subset of scale channels.

The mapping must define:

- source scales;
- source representation types;
- target space;
- transformation behavior;
- locality;
- information loss;
- dimensional behavior;
- provenance.

## 178. Scale Reduction Before TR Integration

If multiple EIF scales are reduced before entering TR, the reduction mapping must remain explicit.

A fused scalar or vector does not preserve the full multiscale state automatically.

## 179. TR Feedback into Multiple EIF Scales

If a later TR state feeds back into several EIF scales, each feedback target must be independently typed.

A single ternary state must not be broadcast across scales without an explicit mapping.

## 180. Symmetry of Future Cross-Layer Mapping

If the later EIF-to-TR map is claimed to preserve symmetry, it must define the source action on the multiscale EIF state and the target action on the TR input space.

Equivariance of the individual EIF scales does not guarantee equivariance of the cross-layer map.

## 181. Dimensional Boundary of Future Integration

Dimensional physical scale outputs must not enter a dimensionless TR coordinate by direct addition or thresholding without an explicit dimensionally valid map.

## 182. Balanced Ternary Boundary

The TR kernel remains exactly:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and active neutral:

`0`

Nothing in the multiscale EIF architecture modifies these semantics.

## 183. No Scale-to-Ternary Shortcut

Rules such as:

`fine scale → -1`

`middle scale → 0`

`coarse scale → 1`

are not part of EIF.

Any such relation would require a separately defined integration mapping and independent semantics.

## 184. No Scale-to-Resonance Shortcut

A scale index or scale-dependent feature is not automatically a resonance coordinate.

Therefore:

`scale value ≠ resonance state`

## 185. No Hierarchy-to-Synchronization Shortcut

Agreement between fine and coarse representations is not synchronization in the TR phase-dynamics sense.

Therefore:

`cross-scale agreement ≠ synchronization`

## 186. No Hierarchy-to-Coherence Shortcut

Hierarchy consistency is not automatically the coherence quantity defined in the TR layer.

Therefore:

`hierarchy consistency ≠ TR coherence`

## 187. No Cross-Scale R(t)/C(t) Collapse

Any future phase-order or coherence quantities associated with integrated scales must preserve the Volume 02 distinction:

`R(t) ≠ C(t)`

Multiscale EIF aggregation does not alter that invariant.

## 188. Minimal Scale Contract

Every EIF scale must define:

1. scale identifier;
2. scale interpretation;
3. parameter space;
4. source state;
5. topology rule;
6. local-environment rule;
7. representation space;
8. symmetry action;
9. locality;
10. physical dimensions where relevant;
11. information retained;
12. information lost;
13. provenance;
14. validation requirements.

## 189. Minimal Cross-Scale Mapping Contract

Every cross-scale mapping must define:

1. source scale;
2. target scale;
3. source space;
4. target space;
5. mapping;
6. transformation action on source;
7. transformation action on target;
8. equivariance or invariance relation where claimed;
9. information loss;
10. locality;
11. dimensional compatibility;
12. provenance;
13. validation relation.

## 190. Minimal Hierarchy Contract

A hierarchical EIF model must additionally define:

1. parent-child relation;
2. partition or cover semantics;
3. membership rules;
4. aggregation direction;
5. top-down relation where used;
6. consistency relation where used;
7. scale-specific object identities;
8. update ordering in a future dynamic realization;
9. trace correspondence;
10. physical-interpretation boundary.

## 191. Minimal Multiscale Energy Contract

A multiscale energy specialization must define:

1. contributing scales;
2. scale representations;
3. total energy mapping;
4. physical units;
5. scale composition rule;
6. overlap and counting semantics;
7. locality and long-range channels;
8. differentiability;
9. parameter provenance;
10. physical reference data;
11. energy validation;
12. force-consistency validation.

## 192. Minimal Cross-Scale Validation Contract

Cross-scale validation must define:

1. tested source scale;
2. tested target scale;
3. test states;
4. expected relation;
5. comparison metric;
6. exact or numerical criterion;
7. numerical tolerance where applicable;
8. symmetry transformations where tested;
9. permutation tests;
10. provenance.

## 193. Conformance Requirements

A multiscale EIF mathematical model conforms to this chapter when:

- every scale is explicitly defined;
- every scale-specific state has a declared space;
- every scale-specific topology is declared;
- every scale-specific environment is declared;
- every scale-specific representation has a declared transformation action;
- hierarchy is not inferred merely from the existence of multiple scales;
- all cross-scale mappings are typed;
- information loss is explicit;
- permutation correspondence is preserved;
- geometric symmetry is preserved where claimed;
- physical dimensions remain compatible;
- physical-output counting semantics are explicit;
- TR semantics are not inserted implicitly.

## 194. Computational Conformance Requirements

A computational multiscale realization additionally conforms when:

- scale metadata are machine-identifiable;
- topology construction is deterministic under the declared contract;
- storage order does not change physical scale membership;
- cross-scale memberships are reproducible;
- transformation tests cover every claimed scale;
- cross-scale equivariance is tested where claimed;
- hierarchy residuals use declared metrics;
- numerical tolerances are explicit;
- missing scale data remain distinct from valid zero values;
- gradient paths preserve the declared energy-force relation;
- artifact provenance identifies all scale definitions.

## 195. Physical Conformance Requirements

A physical multiscale-output specialization additionally conforms when:

- each output has units;
- scale contributions have defined semantics;
- double-counting behavior is controlled;
- local and global contributions are distinguished;
- long-range effects have an explicit representation path;
- physical reference evidence is identified;
- empirical validation is separate from internal hierarchy validation.

## 196. Final Statement

The multiscale EIF layer extends the interatomic architecture from one representation scale into a typed family:

`{Y_EIF,ell}_(ell ∈ L_EIF)`

with explicit cross-scale mappings.

The complete chain is:

`interatomic configuration`

`→ scale-specific geometry and topology`

`→ scale-specific local environments`

`→ scale-specific invariant / equivariant representations`

`→ cross-scale mappings`

`→ hierarchical EIF state`

`→ physical outputs where independently defined`

Multiscale structure does not imply hierarchy automatically.

Hierarchy requires explicit cross-scale relations.

Coarse-graining may lose information.

Refinement is not automatically inversion.

Cross-scale aggregation must preserve the declared symmetry semantics when equivariance is claimed.

Scale-specific physical-output contributions must preserve dimensional compatibility and explicit counting semantics.

In particular:

`scale ≠ resonance state`

`hierarchy level ≠ ternary state`

`cross-scale transition ≠ ternary transition`

`cluster change ≠ physical phase transition`

`cross-scale consistency ≠ physical validation`

remain mandatory distinctions.

The balanced ternary kernel remains separately defined as:

`-1/0/1`

with active:

`0`

No hierarchy level, scale index, aggregation weight, or coarse-grained feature acquires ternary polarity by implication.

The EIF architecture is therefore extended to:

`interatomic state`

`→ geometry`

`→ topology`

`→ local environment`

`→ invariant / equivariant representation`

`→ energy / force / stress interface where defined`

`→ multiscale / hierarchical EIF representation`

This establishes the multiscale mathematical layer required before dynamic interatomic evolution and explicit EIF-to-TR integration are formalized.
