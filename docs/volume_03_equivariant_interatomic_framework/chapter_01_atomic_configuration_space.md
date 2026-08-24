# Atomic Configuration Space

## 1. Purpose

This chapter defines the atomic configuration space of the Equivariant Interatomic Framework within TR-EIF.

The atomic configuration layer provides the formal domain from which:

- atomic geometry;
- species identity;
- local environments;
- interaction graphs;
- symmetry actions;
- equivariant representations;
- resonance descriptors;
- ternary feature channels;
- energy;
- forces;
- stress;
- molecular-dynamics state

are constructed.

The canonical forward chain is:

`atomic configuration`

`→ geometric relations`

`→ interaction graph`

`→ equivariant representation`

`→ resonance parameterization`

`→ ternary feature channels`

`→ energy and observable interfaces`.

The atomic configuration space remains distinct from every derived representation.

---

## 2. Atomic System

An atomic system contains:

`N`

atoms indexed by:

`i ∈ {1, ..., N}`.

Each atom has at least:

- a position;
- a species or atomic identity.

Additional state may include:

- velocity;
- mass;
- charge;
- spin or magnetic descriptor where modeled;
- local state variables;
- periodic-image information;
- material-specific descriptors.

The exact state content is model-specific.

---

## 3. Atomic Position

The position of atom:

`i`

is:

`r_i ∈ R^3`.

The complete coordinate array is:

`R = (r_1, ..., r_N)`.

Therefore:

`R ∈ R^(3N)`.

---

## 4. Atomic Species

Let:

`a_i ∈ A`

denote the species of atom:

`i`.

The complete species assignment is:

`A_N = (a_1, ..., a_N)`.

The species space:

`A`

is discrete.

---

## 5. Minimal Atomic Configuration

A minimal atomic configuration is:

`X = (R, A_N)`.

The corresponding configuration space is:

`X_conf = union over N of (R^(3N) × A^N)`.

A fixed-size model may restrict:

`N`

to one value.

---

## 6. Variable-System Size

TR-EIF permits systems with variable:

`N`.

The framework therefore treats system size as part of the configuration specification where required.

---

## 7. Atomic Labels

Atomic indices are computational labels.

For atoms of identical species, physical predictions must respect the applicable permutation symmetry.

The ordering of identical atoms must not create distinct physical states by identity.

---

## 8. Labeled Configuration Space

The labeled configuration space retains atom indices explicitly:

`X_lab = R^(3N) × A^N`.

This representation is convenient for computation.

It contains representational redundancy for identical particles.

---

## 9. Physical Configuration Equivalence

Two labeled configurations may represent the same physical configuration when related by:

- permutation of identical atoms;
- global translation;
- global rotation where applicable;
- periodic-image equivalence where periodic boundaries are used.

The exact equivalence relation depends on the model boundary conditions.

---

## 10. Configuration Quotient

A physical configuration space may be represented conceptually as a quotient of the labeled configuration space by the applicable symmetry group.

The computational model need not explicitly construct this quotient.

Equivariant and invariant mappings may instead enforce the same transformation structure.

---

## 11. Atomic Mass

Let:

`m_i > 0`

be atomic mass.

Mass may be determined from species or supplied explicitly.

The mass vector is:

`M = (m_1, ..., m_N)`.

Mass remains distinct from species identity even when derived from it.

---

## 12. Atomic Velocity

When dynamics are modeled:

`v_i ∈ R^3`.

The complete velocity state is:

`V = (v_1, ..., v_N)`.

Velocities belong to dynamical state rather than static geometry.

---

## 13. Atomic Momentum

Momentum may be defined:

`p_i = m_i v_i`.

The complete momentum state is:

`P = (p_1, ..., p_N)`.

---

## 14. Static versus Dynamical Configuration

A static interatomic model may use:

`X_static = (R, A_N)`.

A dynamical model may use:

`X_dyn = (R, V, A_N, X_aux)`.

The two state spaces must not be conflated.

---

## 15. Simulation Cell

For periodic systems, define a simulation cell by lattice matrix:

`H ∈ R^(3×3)`.

Its columns or rows represent cell vectors according to the selected convention.

The convention must remain explicit.

---

## 16. Cell Volume

For nonsingular:

`H`

the cell volume is:

`V_cell = |det(H)|`.

The cell must satisfy:

`det(H) ≠ 0`.

---

## 17. Fractional Coordinates

Fractional coordinates may be defined:

`s_i ∈ R^3`

with:

`r_i = H s_i`.

Periodic equivalence may then be represented modulo integer lattice translations.

---

## 18. Cartesian and Fractional Coordinates

Cartesian and fractional coordinates are two representations of atomic geometry.

They are related through:

`r_i = H s_i`.

They are not different physical configurations when the transformation is applied consistently.

---

## 19. Periodic Boundary Conditions

Under periodic boundary conditions:

`s_i`

and:

`s_i + n`

for:

`n ∈ Z^3`

represent equivalent periodic images.

---

## 20. Nonperiodic Configuration

For nonperiodic systems, atomic positions remain in Euclidean space without lattice-image equivalence.

The boundary condition must be explicit.

---

## 21. Mixed Periodicity

A model may be periodic in one or two directions and nonperiodic in others.

The configuration-space definition must specify the periodic subspace.

---

## 22. Relative Position

For atoms:

`i`

and:

`j`

define:

`r_ij = r_j - r_i`

in a nonperiodic system.

For periodic systems, the applicable image convention is used.

---

## 23. Relative Distance

The pair distance is:

`d_ij = ||r_ij||`.

Therefore:

`d_ij ≥ 0`.

For distinct noncoincident atoms:

`d_ij > 0`.

---

## 24. Pair Direction

For:

`d_ij > 0`

define the unit direction:

`e_ij = r_ij / d_ij`.

This is an equivariant vector under rotation.

---

## 25. Pair Displacement Antisymmetry

For a consistent pair representation:

`r_ji = -r_ij`.

Therefore:

`d_ji = d_ij`.

---

## 26. Pair Direction Antisymmetry

When defined:

`e_ji = -e_ij`.

---

## 27. Coincident Positions

If:

`r_i = r_j`

for:

`i ≠ j`

then:

`d_ij = 0`.

Any mapping using:

`1/d_ij`

or:

`e_ij`

must define its admissible domain or collision handling explicitly.

---

## 28. Admissible Atomic Configuration

Let:

`X_adm ⊆ X_conf`

denote the set of admissible configurations.

Admissibility conditions may include:

- nonzero cell volume;
- allowed species;
- minimum pair separation;
- valid periodic cell;
- finite coordinates;
- model-specific domain constraints.

---

## 29. Invalid Configuration

An invalid configuration belongs to a validation-status space.

It does not become a ternary state.

The distinction remains:

`INVALID ≠ 0`.

---

## 30. Configuration Domain

Every interatomic model must define the configuration domain on which its mappings are intended to operate.

The domain may be restricted by:

- species;
- density;
- temperature-related state;
- pressure-related state;
- geometry;
- coordination;
- composition;
- cell shape.

---

## 31. Configuration State versus Representation

The raw configuration:

`X`

is not an equivariant representation.

A representation is produced through an explicit mapping:

`P_EQ: X_conf → X_EQ`.

---

## 32. Configuration State versus Interaction Graph

The atomic configuration and interaction graph are distinct objects.

The graph is derived through:

`P_G: X_conf → X_G`.

---

## 33. Configuration State versus Resonance State

The configuration is not resonance state.

The resonance state appears later through:

`X_conf`

`→ X_EQ`

`→ X_R`.

---

## 34. Configuration State versus Ternary State

The atomic configuration is not a ternary state.

No coordinate or atomic species is identified directly with:

`-1/0/1`.

---

## 35. Configuration State versus Energy

The atomic configuration is an input to an energy functional.

It is not energy itself.

---

## 36. Configuration State versus Force

The atomic configuration is an input to a force model.

It is not mechanical force.

---

## 37. Configuration State versus Stress

The configuration may determine stress through an explicit model.

It is not stress by identity.

---

## 38. Translation Transformation

For translation vector:

`c ∈ R^3`

define:

`r_i' = r_i + c`.

The complete translated configuration is:

`R' = R + c`.

Relative positions satisfy:

`r_ij' = r_ij`.

---

## 39. Translation Invariance of Distance

Under global translation:

`d_ij' = d_ij`.

Thus pair distances are translation invariant.

---

## 40. Rotation Transformation

For:

`Q ∈ SO(3)`

define:

`r_i' = Q r_i`.

Then:

`r_ij' = Q r_ij`.

---

## 41. Rotation Invariance of Distance

Because:

`Q`

preserves Euclidean norm:

`d_ij' = d_ij`.

---

## 42. Rotation Equivariance of Pair Vector

The relative vector transforms as:

`r_ij' = Q r_ij`.

Therefore it is rotation equivariant.

---

## 43. Reflection Transformation

For:

`Q ∈ O(3)`

with:

`det(Q) = -1`

the transformation includes reflection.

Whether the model uses:

`SO(3)`

or:

`O(3)`

symmetry must be declared.

---

## 44. E(3) Transformation

Euclidean transformations combine rotation or reflection with translation.

A generic action is:

`r_i' = Q r_i + c`.

The relevant group may be:

`E(3)`

or a subgroup.

---

## 45. SE(3) Transformation

If reflections are excluded, rigid-body transformations use:

`SE(3)`.

The configuration mapping must specify which group action is used.

---

## 46. Permutation Action

Let:

`pi`

be a permutation of atom indices.

A permuted position array satisfies:

`r_i' = r_(pi(i))`

under the chosen action convention.

Species are permuted consistently.

---

## 47. Species-Preserving Permutation

For physically identical atoms, permutation invariance or equivariance must respect species identity.

A permutation that exchanges unlike species changes the species-labeled configuration unless the model explicitly defines another equivalence.

---

## 48. Permutation-Invariant Scalar

A scalar observable:

`E(X)`

is permutation invariant when:

`E(pi · X) = E(X)`

for admissible species-preserving permutations.

---

## 49. Permutation-Equivariant Vector Output

A per-atom output:

`Y = (y_1, ..., y_N)`

is permutation equivariant when output indices transform consistently with the input permutation.

---

## 50. Translation-Invariant Scalar Output

Energy-like scalar outputs generally satisfy:

`E(R + c) = E(R)`

when no external position-dependent field is included.

The actual model contract must specify applicable external fields.

---

## 51. Rotation-Invariant Scalar Output

A scalar energy functional may satisfy:

`E(QR) = E(R)`.

This is a primary symmetry requirement for rotationally invariant isolated interatomic energy models.

---

## 52. Rotation-Equivariant Vector Output

Force vectors satisfy the geometric transformation form:

`F_i(QR) = Q F_i(R)`

when derived from a rotation-invariant scalar energy under the applicable assumptions.

---

## 53. Tensor Transformation

A second-order tensor quantity:

`T`

transforms as:

`T' = Q T Q^T`

under rotation.

Stress belongs to this transformation class where the selected convention applies.

---

## 54. Atomic Configuration Group Action

Let:

`G`

be the selected symmetry group.

The group action on configuration space is:

`rho_conf(g): X_conf → X_conf`.

The representation space later carries:

`rho_EQ(g)`.

---

## 55. Equivariant Mapping Condition

A mapping:

`F: X_conf → X_Y`

is equivariant if:

`F(rho_conf(g)x) = rho_Y(g) F(x)`.

---

## 56. Invariant Mapping Condition

A mapping is invariant when:

`F(rho_conf(g)x) = F(x)`.

This is equivariance with a trivial output action.

---

## 57. Atomic Configuration Symmetry Contract

Every geometric mapping must declare its behavior under:

- translation;
- rotation;
- reflection where applicable;
- permutation;
- periodic-image transformations where applicable.

---

## 58. Center of Mass

For total mass:

`M_tot = sum_i m_i`

the center of mass is:

`r_cm = (1/M_tot) sum_i m_i r_i`.

It is translation covariant.

---

## 59. Centered Coordinates

Define:

`r_i,c = r_i - r_cm`.

Centered coordinates remove global translation.

They remain rotation equivariant.

---

## 60. Geometric Center

A geometric center may be:

`r_geo = (1/N) sum_i r_i`.

It differs from center of mass when masses differ.

---

## 61. Translation Removal

A representation may remove translation by using:

- relative positions;
- centered coordinates;
- distances;
- local neighborhoods.

The chosen method must preserve required information.

---

## 62. Rotation Handling

Rotation may be handled through:

- invariant scalar descriptors;
- equivariant vector/tensor features;
- irreducible representations;
- local frames.

Volume 03 develops these structures in later chapters.

---

## 63. Local Environment

For atom:

`i`

define a local environment:

`E_i`.

A minimal environment may contain:

- central species;
- neighboring species;
- relative positions;
- pair distances;
- periodic-image information.

---

## 64. Neighborhood Definition

A neighborhood may be defined through cutoff:

`r_cut`.

Then:

`N_i = {j ≠ i | d_ij ≤ r_cut}`.

The exact inequality convention must be explicit.

---

## 65. Cutoff Radius

The cutoff:

`r_cut`

is a model parameter.

It is not a universal TR-EIF constant.

---

## 66. Smooth Cutoff

A model may use a smooth cutoff function:

`f_cut(d)`.

Typical requirements may include continuity or differentiability near:

`r_cut`.

The exact function belongs to the model specialization.

---

## 67. Hard Cutoff

A hard cutoff creates a discontinuous neighborhood membership boundary at:

`r_cut`.

This may be appropriate for some graph constructions.

Its numerical consequences must be handled explicitly.

---

## 68. Neighbor Set

The neighbor set:

`N_i`

is derived from the current configuration.

If geometry changes, the neighbor set may also change.

---

## 69. Dynamic Neighborhood

In molecular dynamics:

`N_i = N_i(t)`.

Neighbor topology therefore becomes time-dependent.

---

## 70. Local Environment Translation Invariance

If local environments use relative coordinates:

`r_ij`

they are invariant to global translation of the complete atomic configuration.

---

## 71. Local Environment Rotation Equivariance

Relative vectors rotate as:

`r_ij → Q r_ij`.

The local environment therefore carries a natural rotation action.

---

## 72. Local Environment Permutation Structure

Neighbor ordering is computational.

A physically valid local representation must handle permutations of equivalent neighbors according to its invariant or equivariant contract.

---

## 73. Local Environment Radius

The geometric extent of a local environment is determined by its neighborhood rule.

This may include:

- fixed radial cutoff;
- adaptive cutoff;
- topological neighborhood;
- graph-hop neighborhood.

---

## 74. Pair Environment

A pair environment may be represented as:

`E_ij = (a_i, a_j, r_ij, d_ij, X_aux)`.

---

## 75. Triplet Environment

A three-body environment may include:

`(i, j, k)`

and angular relations derived from:

`r_ij`

and:

`r_ik`.

---

## 76. Bond Angle

For nonzero relative vectors, an angle may be defined through:

`cos(phi_jik) = (r_ij · r_ik) / (d_ij d_ik)`.

The angle is rotation invariant.

---

## 77. Dihedral Geometry

Four-body geometry may include dihedral-angle relations.

These require explicit orientation conventions.

---

## 78. Many-Body Environment

An interatomic model may depend on the complete local many-body environment rather than a sum of independent pair terms.

TR-EIF does not restrict the EIF layer to pairwise interactions.

---

## 79. Locality

A model is local with respect to a cutoff when each local output depends only on atoms inside the defined neighborhood.

---

## 80. Nonlocal Interactions

A model may include explicitly nonlocal terms.

These must be represented separately from local message-passing or local-environment contributions.

---

## 81. Long-Range Interaction State

Long-range interactions may require:

- electrostatic descriptors;
- reciprocal-space variables;
- multipole variables;
- global graph state;
- additional solver state.

Their inclusion changes the complete configuration-dependent state.

---

## 82. Atomic Attribute Space

Each atom may carry attributes:

`h_i ∈ X_atom`.

Attributes may include:

- species encoding;
- mass;
- charge;
- learned features;
- resonance features;
- ternary channels.

The raw atomic configuration and learned feature state remain distinct.

---

## 83. Species Encoding

Species may be represented computationally through:

- atomic number;
- categorical identifier;
- one-hot vector;
- learned embedding.

The representation must preserve unique species identity within the model domain.

---

## 84. Species Encoding Is Not Species Identity

A learned embedding is a representation of species.

It is not the atomic species itself.

---

## 85. Continuous Atomic Attributes

Some atomic attributes are continuous.

Examples include:

- charge;
- velocity;
- local scalar descriptors;
- learned hidden features.

Their transformation behavior must be declared.

---

## 86. Vector Atomic Attributes

An atom may carry vector features:

`v_i^(f) ∈ R^3`.

These must transform equivariantly under rotation where they represent geometric vectors.

---

## 87. Tensor Atomic Attributes

Higher-order tensor features may also be present.

Their representation class must remain explicit.

---

## 88. Global Attributes

A configuration may contain global variables such as:

- temperature-related control parameter;
- pressure-related control parameter;
- total charge;
- external field;
- composition descriptor.

These remain separate from per-atom state.

---

## 89. External Field

An external field may break some symmetries.

For example, a fixed laboratory-frame vector field breaks full rotational invariance unless the field itself is transformed with the configuration.

The model contract must include the field in the transformation domain where appropriate.

---

## 90. Charge State

If atomic charges:

`q_i`

are included, the charge vector is:

`Q = (q_1, ..., q_N)`.

Charge is a scalar under spatial rotations.

---

## 91. Total Charge

The total charge is:

`Q_tot = sum_i q_i`.

It is permutation and spatially invariant.

---

## 92. Composition

For species:

`a`

define species count:

`N_a`.

The composition vector contains counts or fractions over species.

---

## 93. Composition Invariance

Composition is invariant under atomic coordinate transformations and atom permutation.

---

## 94. Configuration Measure

A configuration may carry a measure or weighting when used in statistical or learning contexts.

The measure remains distinct from the configuration itself.

---

## 95. Ensemble

An ensemble is a collection or probability distribution over configurations.

It is not one atomic configuration.

---

## 96. Trajectory

A molecular-dynamics trajectory is a time-indexed sequence:

`X(t)`.

A trajectory is not identical to one instantaneous configuration.

---

## 97. Frame

One sampled configuration from a trajectory may be called a frame.

Frame ordering belongs to trajectory state.

---

## 98. Configuration History

A history-dependent model may use:

`H_X(t)`

containing previous configurations or sufficient retained state.

History must be explicit when it affects future outputs.

---

## 99. Markov State

A state representation is Markov-complete for the selected model if the next-state distribution or deterministic update depends only on the current complete state and current input.

---

## 100. Hidden Configuration Memory

If future outputs depend on omitted previous geometry, the declared configuration state is incomplete for that model.

---

## 101. Atomic Configuration and FRP

The atomic configuration space belongs to the EIF layer.

FRP does not replace the atomic configuration space.

The integration direction is:

`atomic configuration`

`→ equivariant interatomic representation`

`→ resonance parameterization`

`→ ternary target/execution interface`.

---

## 102. EIF-to-TR Boundary

The principal forward interface is:

`X_conf`

`→ X_EQ`

`→ X_R`

`→ T_target`.

The atomic configuration is upstream of resonance and ternary state.

---

## 103. TR-to-EIF Feedback Boundary

The reverse interface is:

`X_TR × X_conf → X_EIF,req`.

The output remains an interatomic update request.

It is not direct configuration replacement by semantic identity.

---

## 104. Geometry versus Resonance

A geometric distance:

`d_ij`

is not resonance by identity.

It may become one input to a resonance parameterization.

---

## 105. Geometry versus Ternary State

A positive or negative Cartesian coordinate does not define ternary polarity.

---

## 106. Geometry versus Energy

Coordinates are arguments of an energy functional.

They are not energy themselves.

---

## 107. Geometry versus Force

Relative positions are not force vectors.

Force requires an explicit interatomic model or energy derivative.

---

## 108. Interaction Graph Interface

Chapter 02 defines the interaction graph:

`G = (V, E)`.

The graph is constructed from the atomic configuration and interaction rules.

---

## 109. Graph Nodes

Each atom corresponds to a graph node.

Node state may include:

- species;
- atomic attributes;
- learned features;
- later resonance or ternary channels.

---

## 110. Graph Edges

Edges represent model-defined interactions or message-passing relations.

An edge does not automatically represent a chemical bond.

---

## 111. Interaction Edge versus Chemical Bond

The invariant distinction is:

`interaction edge ≠ chemical bond`.

A graph edge is a computational or modeled interaction relation.

---

## 112. Graph Edge versus Mechanical Force

Likewise:

`interaction edge ≠ mechanical force`.

---

## 113. Edge Geometry

An edge may carry:

- relative displacement;
- distance;
- radial basis;
- directional features;
- periodic image shift.

---

## 114. Periodic Edge

Under periodic boundaries, an edge may include lattice shift:

`n_ij ∈ Z^3`.

Then:

`r_ij = r_j + H n_ij - r_i`

under the selected convention.

---

## 115. Minimum-Image Convention

A periodic pair representation may use the minimum-image displacement when appropriate.

The convention is model-specific and depends on cutoff and cell geometry.

---

## 116. Neighbor-List Representation

For efficient computation, interactions may be represented by a neighbor list.

The neighbor list is a computational representation of graph edges.

---

## 117. Neighbor-List Skin

A molecular-dynamics implementation may use a skin distance larger than the interaction cutoff.

The skin parameter belongs to numerical implementation.

---

## 118. Neighbor-List Update

A neighbor list may be rebuilt when atomic displacements exceed a declared criterion.

This state becomes result-affecting if it changes which interactions are evaluated.

---

## 119. Graph Construction Determinism

For deterministic execution, graph construction must define canonical handling of:

- cutoff equality;
- periodic images;
- duplicate edges;
- node ordering;
- edge ordering.

---

## 120. Configuration Permutation and Graph Permutation

A permutation of atom labels must produce the corresponding permutation of graph nodes and edges.

This is required for permutation-equivariant graph construction.

---

## 121. Geometry Invariance of Graph Connectivity

If graph edges depend only on distances and species, global translation and rotation do not change connectivity.

---

## 122. Directional Graph State

Even when connectivity is invariant, edge vectors remain rotation equivariant.

---

## 123. Atomic Configuration and E(3)

The atomic configuration supports the action of the Euclidean group.

This geometric action is the basis of the E(3) formalism developed in Chapter 03.

---

## 124. Translation Group

Translations form:

`R^3`

under vector addition.

They act globally on atomic positions.

---

## 125. Rotation Group

Proper rotations form:

`SO(3)`.

They preserve:

- distances;
- angles;
- orientation.

---

## 126. Orthogonal Group

`O(3)`

contains rotations and reflections.

The distinction between:

`SO(3)`

and:

`O(3)`

matters for pseudoscalar and pseudovector quantities.

---

## 127. Euclidean Group

The Euclidean group combines orthogonal transformations and translations.

Its action provides the natural symmetry structure of atomic coordinates in Euclidean space.

---

## 128. Group Orbit

The orbit of configuration:

`X`

under group:

`G`

is the set:

`Orb_G(X) = {g · X | g ∈ G}`.

Configurations in one orbit are symmetry-related under the selected action.

---

## 129. Stabilizer

The stabilizer of:

`X`

is:

`Stab_G(X) = {g ∈ G | g · X = X}`.

This set describes symmetries of the specific configuration.

---

## 130. Symmetric Configuration

A configuration may possess nontrivial rotational, reflection, translational, or permutation symmetry.

These symmetries may affect representation degeneracies and model behavior.

---

## 131. Symmetry Breaking

A perturbed configuration may reduce the stabilizer group.

This is a geometric symmetry change.

It is not automatically:

- a resonance transition;
- a ternary transition;
- a physical phase transition.

---

## 132. Structural Classification

A structural classifier may operate on atomic configuration:

`C_S: X_conf → K_S`.

The output remains distinct from the raw configuration.

---

## 133. Structural Transition

A structural transition is a change in structural classification or another explicitly defined structural state.

It remains distinct from ternary transition.

---

## 134. Physical Phase Classification

A physical phase classifier may depend on:

- structure;
- thermodynamic state;
- ensemble observables;
- free-energy relations.

The atomic configuration may contribute to this classification.

---

## 135. Atomic Configuration versus Physical Phase

One atomic configuration does not universally determine a thermodynamic phase without the applicable model and state variables.

---

## 136. Local Coordination Number

A local coordination number may be defined:

`CN_i = number of j in N_i`

under a declared neighborhood rule.

This is a derived local structural observable.

---

## 137. Weighted Coordination

A smooth coordination number may use:

`CN_i = sum_j f_cut(d_ij)`.

The function is model-specific.

---

## 138. Coordination Is Not Bond Order by Identity

A coordination count is not automatically a chemical bond-order measure.

---

## 139. Radial Distribution Relation

A set of configurations may produce radial distribution statistics.

These are ensemble or trajectory observables.

They are not properties of one pair alone.

---

## 140. Local Density

A local density may be defined through a kernel:

`rho_i = sum_j K_rho(d_ij)`.

The kernel defines the model-specific observable.

---

## 141. Local Density versus Physical Mass Density

A dimensionless learned or normalized local density descriptor is not automatically equal to physical mass density.

Dimensional semantics must remain explicit.

---

## 142. Geometric Descriptor

A descriptor is a mapping:

`D: X_conf → X_D`.

Descriptors may be:

- invariant;
- equivariant;
- local;
- global;
- learned;
- analytic.

---

## 143. Descriptor Information Loss

If:

`D`

is non-injective, multiple configurations map to the same descriptor.

This is permitted.

The lost information cannot be recovered by identity.

---

## 144. Complete Descriptor

A descriptor is complete with respect to a chosen equivalence relation if equal descriptors imply equivalent configurations within the declared domain.

Completeness must be established for the specific descriptor.

---

## 145. Invariant Descriptor

An invariant descriptor satisfies:

`D(g · X) = D(X)`.

---

## 146. Equivariant Descriptor

An equivariant descriptor satisfies:

`D(g · X) = rho_D(g) D(X)`.

---

## 147. Local Descriptor

A local descriptor:

`D_i`

depends on:

`E_i`.

---

## 148. Global Descriptor

A global descriptor depends on the complete configuration.

---

## 149. Species-Aware Descriptor

A descriptor may distinguish species through categorical or learned species channels.

Species awareness is required when chemically distinct atoms must be represented differently.

---

## 150. Permutation-Invariant Aggregation

Local neighbor contributions may be aggregated through permutation-invariant operations such as:

- sum;
- mean;
- max;
- invariant tensor contraction.

The choice affects model expressivity.

---

## 151. Sum Aggregation

For neighbor messages:

`m_ij`

a local aggregate may be:

`m_i = sum_(j in N_i) m_ij`.

The sum is invariant to neighbor ordering.

---

## 152. Mean Aggregation

A mean may normalize by neighborhood size.

This changes scaling relative to sum aggregation.

---

## 153. Attention Aggregation

A learned weighted aggregation may also be permutation invariant when weights and normalization are defined consistently.

---

## 154. Message-Passing Boundary

Chapter 05 develops message passing.

This chapter defines the configuration and neighborhood state on which message passing operates.

---

## 155. Equivariant Representation Boundary

Chapter 04 develops equivariant representations.

The configuration layer supplies:

- scalar species state;
- vector geometry;
- tensor geometry;
- graph topology.

---

## 156. Resonance Parameterization Boundary

Chapter 06 maps equivariant interatomic representations into resonance variables.

The canonical direction is:

`X_conf`

`→ X_EQ`

`→ X_R`.

---

## 157. Ternary Feature Boundary

Chapter 07 introduces ternary feature channels.

The ternary domain remains:

`-1/0/1`.

Atomic coordinates do not become ternary features without an explicit mapping.

---

## 158. Energy Boundary

Chapter 08 defines the conservative energy functional.

The configuration enters as an argument:

`E = E(X_conf, X_features, ...)`.

---

## 159. Force Boundary

Chapter 09 defines forces.

For a differentiable conservative energy model:

`F_i = -grad_(r_i) E`

under the corresponding coordinate convention.

---

## 160. Stress Boundary

Stress is derived through an explicitly defined cell or strain derivative or another applicable mechanical relation.

It remains tensor-valued.

---

## 161. Model Family Boundary

Chapter 10 defines the TR-EIP model family.

Atomic configuration space becomes the common geometric input domain for the family.

---

## 162. Configuration Normalization

Coordinates may be rescaled numerically.

Any scaling must define:

- unit;
- scale factor;
- inverse transformation;
- interaction with cell state.

---

## 163. Physical Units

Atomic positions carry units of length when physical units are used.

Distances carry the same length dimension.

Angles are dimensionless.

---

## 164. Unit System

A model must declare the unit system for:

- position;
- cell vectors;
- energy;
- force;
- stress;
- time where dynamics are included.

---

## 165. Unit Conversion

Unit conversion is a mapping between numerical representations of the same physical quantity.

It must be applied consistently to all coupled quantities.

---

## 166. Dimensionless Coordinates

A model may nondimensionalize coordinates:

`r_star = r / L_ref`.

The reference length:

`L_ref`

becomes part of the model definition.

---

## 167. Nondimensionalization versus Geometry

Nondimensionalization changes representation scale.

It does not change the underlying geometric relations when applied consistently.

---

## 168. Finite Coordinates

A valid numerical configuration requires finite coordinate values unless the mathematical model explicitly includes extended values.

---

## 169. NaN Coordinates

A coordinate containing:

`NaN`

is an invalid numerical configuration state.

It must not be interpreted as active neutral or another physical configuration.

---

## 170. Infinite Coordinates

Infinite coordinate values require explicit treatment.

They are not ordinary atomic positions in the finite Euclidean configuration space.

---

## 171. Collision Domain

Some models exclude pair distances below:

`d_min`.

Then admissibility requires:

`d_ij ≥ d_min`

for the applicable pairs.

---

## 172. Collision Handling

Collision handling may use:

- rejection;
- regularized potential;
- constrained integration;
- explicit short-range repulsion.

The selected mechanism belongs to the model specialization.

---

## 173. Configuration Constraints

A model may impose constraints such as:

- fixed bond lengths;
- fixed angles;
- rigid groups;
- fixed atoms;
- cell constraints.

These reduce the accessible configuration manifold.

---

## 174. Constraint Manifold

A holonomic constraint may be represented:

`g(X) = 0`.

The admissible state then lies on the corresponding constraint manifold under regularity assumptions.

---

## 175. Constrained Dynamics

When constraints are present, forces or integration steps may include constraint reactions.

These belong to the dynamics layer rather than raw configuration identity.

---

## 176. Atomic Configuration Topology

The configuration space may contain disconnected components when constraints, species assignments, or topological restrictions prevent continuous paths between some states.

---

## 177. Connectivity of Configuration Space

Connectedness depends on:

- fixed species;
- collision exclusions;
- periodicity;
- constraints;
- permutation quotient.

No universal connectedness is assumed.

---

## 178. Configuration Path

A continuous path between configurations may be represented:

`X(lambda)`

for:

`lambda ∈ [0,1]`.

---

## 179. Structural Path

A configuration path may represent a structural transformation.

The path itself is not automatically a minimum-energy path.

---

## 180. Minimum-Energy Path

A minimum-energy path requires an energy functional and optimization criterion.

It is not defined by geometry alone.

---

## 181. Reaction Coordinate

A reaction coordinate is a derived mapping from configuration space.

It is not identical to the full atomic configuration.

---

## 182. Resonance Coordinate

Likewise, a resonance coordinate is derived from an interatomic/equivariant state.

It is not identical to the raw geometry.

---

## 183. Configuration Metric

A metric:

`d_conf`

may be defined on configuration space.

Its definition must account for the selected equivalences if physical comparison is intended.

---

## 184. RMSD-Type Metric

A root-mean-square displacement metric may compare two coordinate sets after an alignment procedure.

The alignment and permutation handling must be defined.

---

## 185. Symmetry-Aware Distance

A symmetry-aware configuration distance may minimize over allowed transformations:

`d_sym(X,Y) = inf_g d_conf(g · X, Y)`.

This is one possible construction.

---

## 186. Periodic Configuration Distance

Periodic systems require image-aware distance definitions.

A naive Cartesian difference may compare equivalent configurations incorrectly.

---

## 187. Configuration Similarity

Similarity is model-dependent.

No universal configuration-similarity scalar is imposed by TR-EIF.

---

## 188. Dataset Configuration

A dataset entry may contain:

- configuration;
- energy;
- forces;
- stress;
- metadata;
- provenance;
- conditions.

The configuration remains one component of the sample.

---

## 189. Training Configuration

A training configuration is a configuration used in parameter optimization.

Its use does not change its mathematical state type.

---

## 190. Validation Configuration

A validation configuration belongs to an evaluation split or validation protocol.

Its atomic-state semantics remain identical.

---

## 191. Reference Configuration

A reference configuration may serve as:

- equilibrium geometry;
- baseline structure;
- calibration state;
- test fixture.

Its role must be explicit.

---

## 192. Configuration Provenance

Atomic configurations may carry provenance such as:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`BENCHMARK`

`TEST_FIXTURE`.

The appropriate class depends on origin.

---

## 193. Primary-Source Configuration

An atomic structure obtained from an external scientific source carries:

`PRIMARY_SOURCE`

provenance.

---

## 194. Derived Configuration

A configuration generated through a documented transformation or simulation may carry:

`DERIVED`

provenance.

---

## 195. Calibrated Configuration

A geometry adjusted through calibration may carry:

`CALIBRATED`

provenance.

---

## 196. Test Fixture Configuration

A synthetic configuration designed for deterministic tests carries:

`TEST_FIXTURE`

provenance.

---

## 197. Benchmark Configuration

A configuration used for performance or numerical benchmarking may carry:

`BENCHMARK`

provenance when the associated result is benchmark-derived.

---

## 198. Configuration Serialization

A configuration artifact must preserve enough information to reconstruct the intended atomic state.

This may include:

- species;
- positions;
- cell;
- periodicity;
- units;
- optional attributes.

---

## 199. Atom Ordering in Serialization

A serialized file may impose an atom order.

Physical predictions must remain consistent under allowed species-preserving permutations.

---

## 200. Canonical Serialization

Deterministic replay or hashing may require canonical ordering and canonical numeric formatting.

This is an artifact-level requirement.

---

## 201. Configuration Hash

A configuration hash depends on serialization unless defined through a symmetry-aware canonicalization.

Byte identity and physical equivalence are distinct.

---

## 202. Byte Identity versus Physical Equivalence

Two files may differ byte-for-byte while encoding symmetry-equivalent atomic configurations.

The distinction must remain explicit.

---

## 203. Configuration Validation

A configuration validator may check:

- atom count;
- species validity;
- finite coordinates;
- cell validity;
- periodic flags;
- pair-distance constraints;
- dimensional consistency.

---

## 204. Symmetry Validation

A symmetry validator may apply known transformations and verify the declared invariant or equivariant behavior of downstream mappings.

---

## 205. Translation Test

For translation:

`c`

construct:

`R' = R + c`.

Translation-invariant outputs must remain unchanged.

Translation-equivariant outputs must transform according to their declared action.

---

## 206. Rotation Test

For:

`Q ∈ SO(3)`

construct:

`R' = QR`.

Scalar invariant outputs remain unchanged.

Vector outputs transform by:

`Q`.

---

## 207. Reflection Test

If the model claims:

`O(3)`

equivariance, reflection tests must be included.

If the model is only:

`SO(3)`

equivariant, reflection behavior remains separately defined.

---

## 208. Permutation Test

For an allowed species-preserving permutation:

`pi`

the configuration is permuted.

Global scalar outputs remain invariant.

Per-atom outputs permute consistently.

---

## 209. Periodic-Image Test

Equivalent periodic representations must produce equivalent model outputs under the declared periodicity contract.

---

## 210. Graph Consistency Test

Equivalent transformed configurations must generate graph structures consistent with the declared transformation rules.

---

## 211. Local Environment Test

A local environment extracted before and after a rigid-body transformation must preserve the appropriate invariant/equivariant relations.

---

## 212. Deterministic Configuration Processing

Given identical configuration, parameters, and canonical ordering, a deterministic preprocessing pipeline must produce identical declared outputs.

---

## 213. Configuration Replay

A restart or replay artifact must preserve every configuration-state component required by the downstream model.

---

## 214. Geometry Precision

The numeric precision of coordinates must be sufficient for the declared model and artifact role.

Rounding may change neighbor membership near cutoff boundaries.

---

## 215. Cutoff Boundary Sensitivity

If:

`d_ij`

is numerically close to:

`r_cut`

small numerical perturbations may change graph topology.

The cutoff comparison convention must therefore be explicit.

---

## 216. Graph Chatter

In dynamics, repeated edge creation and removal near:

`r_cut`

may occur.

Smooth cutoffs or neighbor-list skin may alter numerical behavior without changing the formal configuration space.

---

## 217. Configuration Continuity

Atomic positions may evolve continuously even while graph topology changes discretely.

This creates a hybrid geometric-graph state.

---

## 218. Graph Transition versus Structural Transition

An interaction edge appearing or disappearing at a cutoff boundary is not automatically a structural transition.

It may be a graph-construction event.

---

## 219. Graph Transition versus Chemical Bond Transition

Likewise:

`graph edge change ≠ chemical bond change`

unless the graph is explicitly defined as a bond graph.

---

## 220. Geometry Transition versus Ternary Transition

A change in atomic coordinates is not a ternary transition.

The ternary channel is produced only through explicit mappings.

---

## 221. Geometry Transition versus Resonance Transition

A geometric change may alter resonance state.

The two transitions remain distinct.

---

## 222. Structural Transition versus Resonance Transition

A structural classifier may change independently of resonance classification.

No identity is assumed.

---

## 223. Configuration and Locality Scale

The configuration can be partitioned into local environments at a selected interaction scale.

Different cutoff scales produce different local-state decompositions.

---

## 224. Multiscale Configuration

A multiscale model may retain:

- atomic configuration;
- cluster configuration;
- mesoscale descriptors;
- continuum fields.

Each scale has its own state space.

---

## 225. Atomistic-to-Mesoscale Mapping

A mapping:

`M_A→M`

may aggregate atomistic information into mesoscale state.

This mapping is generally non-injective.

---

## 226. Configuration Information Loss

Any coarse-graining map may discard:

- atom identity;
- local geometry;
- phase information;
- high-frequency modes.

The lost information cannot be reconstructed by identity.

---

## 227. Closure Variables

A coarse model may require closure variables representing effects of discarded atomistic degrees of freedom.

These are introduced explicitly in Volume 06.

---

## 228. Atomic Configuration and FLiBe

Volume 07 later specializes the configuration space for FLiBe.

That specialization will define:

- species set;
- composition;
- local coordination;
- interatomic reference data;
- thermodynamic state;
- transport-related observables.

---

## 229. FLiBe Species Boundary

The FLiBe species set belongs to the material specialization.

It is not imposed universally on Volume 03.

---

## 230. General Material Domain

Volume 03 remains material-general.

The atomic configuration formalism applies to arbitrary declared species sets and admissible interatomic configurations.

---

## 231. Atomic Configuration Extension Rule

Any extension of the atomic configuration state must define:

1. new state variable;
2. domain;
3. physical or mathematical meaning;
4. units;
5. symmetry transformation;
6. locality;
7. persistence;
8. serialization;
9. validation;
10. provenance.

---

## 232. Species Extension Rule

Any new species representation must define:

1. species identity;
2. encoding;
3. permutation semantics;
4. associated physical attributes;
5. provenance.

---

## 233. Cell Extension Rule

Any cell representation must define:

1. lattice convention;
2. periodic directions;
3. coordinate convention;
4. determinant requirement;
5. deformation behavior;
6. serialization.

---

## 234. Periodicity Extension Rule

Any periodic boundary implementation must define:

1. periodic axes;
2. image convention;
3. displacement rule;
4. graph-edge image representation;
5. cell update semantics;
6. validation.

---

## 235. Local-Environment Extension Rule

Any local-environment definition must define:

1. central atom;
2. neighbor criterion;
3. cutoff;
4. periodic treatment;
5. species handling;
6. geometric features;
7. permutation behavior.

---

## 236. Descriptor Extension Rule

Any atomic descriptor must define:

1. source configuration state;
2. output space;
3. transformation law;
4. locality;
5. dimensional structure;
6. information loss;
7. provenance.

---

## 237. Canonical Configuration Invariants

Every conforming atomic configuration representation preserves:

1. explicit atom count;

2. explicit species identity;

3. explicit positions;

4. explicit cell when periodic;

5. explicit periodicity;

6. finite valid numerical coordinates;

7. explicit unit system;

8. explicit symmetry behavior.

---

## 238. Canonical Geometry Invariants

The geometric layer preserves:

`r_ij = r_j - r_i`

under the applicable image convention,

`r_ji = -r_ij`

and:

`d_ij = d_ji`.

Distances are translation and rotation invariant.

Relative vectors are translation invariant and rotation equivariant.

---

## 239. Canonical Symmetry Invariants

The configuration layer preserves explicit handling of:

- translation;
- rotation;
- reflection where applicable;
- species-preserving permutation;
- periodic-image equivalence.

---

## 240. Canonical Type-Separation Invariants

The framework preserves:

`atomic configuration ≠ graph`

`atomic configuration ≠ equivariant representation`

`atomic configuration ≠ resonance state`

`atomic configuration ≠ ternary state`

`atomic configuration ≠ energy`

`atomic configuration ≠ force`

`atomic configuration ≠ stress`

`interaction edge ≠ chemical bond`

`interaction edge ≠ force`.

---

## 241. Canonical TR Separation Invariants

The framework preserves:

`geometry ≠ resonance`

`resonance classification ≠ ternary state`

`ternary target ≠ executed state`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 242. Canonical Scientific Distinctions

The EIF configuration layer preserves:

`oscillator phase ≠ physical phase of matter`

`phase relation ≠ chemical bond`

`phase coupling ≠ mechanical force`

`resonance classification ≠ energy`

`ternary state ≠ energy`

`graph edge ≠ bond`

`descriptor ≠ configuration`

`bounded descriptor ≠ bounded complete configuration state`.

---

## 243. Configuration-to-EIF Chain

The canonical EIF forward chain begins:

`atomic configuration`

`→ interaction graph`

`→ geometric features`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ energy functional`

`→ force and stress`.

---

## 244. Configuration-to-TR Chain

The TR integration path is:

`X_conf`

`→ X_EQ`

`→ X_R`

`→ T_target`

`→ T_exec`.

The configuration state is never collapsed directly into executed ternary state.

---

## 245. Feedback Chain

The reverse path may be:

`T_exec`

`+ X_R`

`+ X_EQ`

`+ X_conf`

`→ update request`

`→ interatomic state evolution`.

The feedback mapping remains explicit.

---

## 246. Interface to Chapter 02

Chapter 02 develops Interaction Graphs.

It defines:

- graph nodes;
- edges;
- cutoff topology;
- periodic edges;
- dynamic graph construction;
- edge attributes;
- graph symmetry;
- deterministic graph generation.

The atomic configuration defined here is the source state for graph construction.

---

## 247. Interface to Chapter 03

Chapter 03 develops E(3) Group Actions.

It formalizes:

- translations;
- rotations;
- reflections;
- Euclidean group action;
- permutation interaction;
- invariant and equivariant transformation rules.

---

## 248. Interface to Chapter 04

Chapter 04 develops Equivariant Representations.

It maps raw atomic and geometric state into structured scalar, vector, tensor, and irreducible representation channels.

---

## 249. Interface to Chapter 05

Chapter 05 develops Message Passing.

It operates on interaction graphs and equivariant node/edge features derived from the atomic configuration.

---

## 250. Interface to Chapter 06

Chapter 06 develops Resonance Parameterization.

It maps equivariant interatomic features into resonance coordinates while preserving the distinction:

`geometry ≠ resonance`.

---

## 251. Interface to Chapter 07

Chapter 07 develops Ternary Feature Channels.

It defines the mapping from continuous/equivariant/resonance representations into exact:

`-1/0/1`

feature channels.

---

## 252. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

Atomic configuration, equivariant features, resonance state, and ternary channels become explicitly typed inputs to the energy model.

---

## 253. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

It defines vector and tensor outputs with the required symmetry and dimensional semantics.

---

## 254. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

The atomic configuration space becomes the common geometric domain for the family.

---

## 255. Final Formal Structure

The atomic configuration layer may be represented as:

`AC = (N, A_N, R, H, PBC, X_atom, X_global, X_adm, rho_conf)`.

Here:

- `N` is atom count;
- `A_N` is species assignment;
- `R` is atomic position state;
- `H` is simulation cell where present;
- `PBC` is periodic-boundary state;
- `X_atom` contains optional per-atom attributes;
- `X_global` contains optional global attributes;
- `X_adm` defines admissible configurations;
- `rho_conf` defines the applicable symmetry-group action.

The principal geometric quantities are:

`r_ij`

`d_ij`

`e_ij`.

The principal symmetry requirements are:

- translation handling;
- rotation handling;
- reflection handling where applicable;
- species-preserving permutation handling;
- periodic-image equivalence.

---

## 256. Final Statement

Atomic configuration space is the geometric and species-resolved foundation of the Equivariant Interatomic Framework.

A configuration contains explicitly typed atomic positions, species identities, optional cell state, periodicity, and additional declared attributes.

The atomic configuration is transformed through explicit mappings into:

- interaction graphs;
- geometric descriptors;
- equivariant representations;
- resonance state;
- ternary feature channels;
- energy;
- force;
- stress.

The framework preserves the exact distinctions:

`atomic configuration ≠ graph`

`atomic configuration ≠ equivariant representation`

`geometry ≠ resonance`

`resonance ≠ ternary state`

`ternary target ≠ executed state`

`interaction edge ≠ chemical bond`

`phase coupling ≠ mechanical force`

`ternary state ≠ energy`.

Spatial symmetry begins from the explicit action of translation, rotation, reflection where applicable, permutation, and periodic-image transformations on the atomic configuration.

These definitions establish the geometric state domain required for the Interaction Graph formalism developed in Chapter 02.
