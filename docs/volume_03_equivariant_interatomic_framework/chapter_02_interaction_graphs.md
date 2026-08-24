# Interaction Graphs

## 1. Purpose

This chapter defines interaction graphs within the Equivariant Interatomic Framework of TR-EIF.

The interaction graph converts an atomic configuration into an explicit relational structure suitable for:

- geometric neighborhood construction;
- local and nonlocal interactions;
- equivariant representations;
- message passing;
- resonance parameterization;
- ternary feature channels;
- energy evaluation;
- force propagation;
- multiscale coupling.

The canonical chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ energy / force / stress interfaces`.

An interaction graph is a model-defined computational structure.

It is not a chemical-bond graph by identity.

---

## 2. Graph Definition

Let:

`G = (V, E)`.

Here:

- `V` is the node set;
- `E` is the edge set.

For an atomic system with:

`N`

atoms:

`V = {1, ..., N}`.

Each graph node corresponds to one atom.

---

## 3. Node Identity

Node:

`i ∈ V`

is associated with atom:

`i`.

The node may carry:

- species;
- position;
- mass;
- charge;
- scalar features;
- vector features;
- tensor features;
- resonance features;
- ternary feature channels.

The graph node is a computational representation of the atomic entity.

---

## 4. Node Feature State

Let:

`h_i ∈ X_node`.

The complete node-feature state is:

`H = (h_1, ..., h_N)`.

The node-feature space may contain several representation types.

---

## 5. Raw Node Features

Raw node features may include:

- species encoding;
- atomic number;
- mass;
- charge;
- externally supplied scalar state.

Raw node features remain distinct from learned hidden representations.

---

## 6. Learned Node Features

A learned node representation may be:

`h_i^(l)`

at layer:

`l`.

The superscript identifies representation depth or processing stage.

It is not a physical time coordinate unless explicitly defined.

---

## 7. Edge Set

An edge:

`(i, j) ∈ E`

indicates that the graph model permits an interaction or information-transfer relation between nodes:

`i`

and:

`j`.

The exact meaning of an edge is determined by the graph-construction rule.

---

## 8. Directed Edge

A directed edge is written:

`j → i`.

It represents a contribution from source node:

`j`

to receiver node:

`i`.

Direction must remain consistent throughout message-passing equations and implementation.

---

## 9. Undirected Edge

An undirected relation:

`{i, j}`

may be represented computationally by two directed edges:

`i → j`

and:

`j → i`.

This preserves receiver-specific message semantics.

---

## 10. Directed and Undirected Graphs

TR-EIF permits:

- directed graphs;
- undirected graphs;
- symmetrized directed representations;
- asymmetric interaction graphs.

The selected graph type must be explicit.

---

## 11. Edge Feature State

Each edge may carry:

`e_ij ∈ X_edge`.

Possible edge features include:

- relative position;
- distance;
- direction;
- radial basis values;
- angular descriptors;
- species-pair descriptors;
- periodic image shift;
- cutoff weight;
- resonance-related variables;
- learned features.

---

## 12. Relative Position Edge Feature

For source:

`j`

and receiver:

`i`

define:

`r_ij = r_j - r_i`

under the applicable boundary-condition convention.

This relative vector is translation invariant and rotation equivariant.

---

## 13. Pair Distance

Define:

`d_ij = ||r_ij||`.

Distance is:

- translation invariant;
- rotation invariant;
- reflection invariant.

For a consistent displacement convention:

`d_ij = d_ji`.

---

## 14. Pair Direction

For:

`d_ij > 0`

define:

`e_hat_ij = r_ij / d_ij`.

The direction is rotation equivariant.

---

## 15. Edge Direction Convention

If edge:

`j → i`

uses:

`r_ij = r_j - r_i`

then this convention must remain fixed.

Changing to:

`r_i - r_j`

changes the vector sign and can alter directional message semantics.

---

## 16. Edge Antisymmetry

Under the corresponding reverse-edge convention:

`r_ji = -r_ij`.

Therefore:

`e_hat_ji = -e_hat_ij`

when both are defined.

---

## 17. Graph Construction Mapping

The graph is generated through:

`P_G: X_conf → X_G`.

A more complete construction may be:

`P_G: X_conf × P_Graph → X_G`.

Here:

`P_Graph`

contains graph-construction parameters.

---

## 18. Graph State Space

Let:

`X_G`

denote the graph-state space.

A graph state may contain:

- node set;
- edge set;
- node features;
- edge features;
- global graph features;
- periodic-image information;
- graph-generation metadata.

---

## 19. Cutoff Graph

A radial cutoff graph may use:

`r_cut > 0`.

The neighbor relation is:

`j ∈ N_i`

when:

`j ≠ i`

and:

`d_ij ≤ r_cut`

under the selected equality convention.

---

## 20. Neighbor Set

For receiver:

`i`

define:

`N_i = {j | j → i ∈ E}`.

The set may depend on:

- geometry;
- cutoff;
- species;
- topology;
- material state;
- model parameters.

---

## 21. Cutoff Boundary

The cutoff surface is:

`d_ij = r_cut`.

The graph-construction rule must define whether equality creates an edge.

---

## 22. Hard Cutoff

A hard cutoff uses a discontinuous edge-membership rule.

For example:

`d_ij ≤ r_cut → edge`

`d_ij > r_cut → no edge`.

This creates discrete topology changes under continuous geometric motion.

---

## 23. Smooth Cutoff

A smooth cutoff may preserve a fixed candidate graph while multiplying interaction strength by:

`f_cut(d_ij)`.

This can reduce discontinuities in interaction magnitude near the cutoff.

---

## 24. Candidate Graph

A candidate graph may include edges within a larger radius:

`r_list > r_cut`.

The actual interaction weight may then vanish beyond:

`r_cut`.

---

## 25. Neighbor-List Skin

Define:

`r_skin = r_list - r_cut`.

A positive skin may reduce graph rebuild frequency in molecular-dynamics implementations.

This is a numerical implementation parameter.

---

## 26. Graph Rebuild

A dynamic neighbor graph may be rebuilt when geometric displacement exceeds a declared criterion.

The rebuild rule belongs to the numerical graph realization.

---

## 27. Dynamic Graph

For time-dependent configuration:

`X(t)`

the graph may evolve:

`G(t) = P_G(X(t))`.

In discrete time:

`G[n] = P_G(X[n])`.

---

## 28. Continuous Geometry and Discrete Topology

Atomic positions may evolve continuously while edge membership changes discretely.

Therefore the combined geometry-graph system may be hybrid.

---

## 29. Edge Creation Event

An edge-creation event occurs when a pair becomes admissible under the graph rule.

This is a graph-topology event.

---

## 30. Edge Removal Event

An edge-removal event occurs when a pair leaves the admissible graph relation.

---

## 31. Graph Event versus Structural Transition

The distinction remains:

`graph edge event ≠ structural transition`.

An edge may appear or disappear because of a computational cutoff.

---

## 32. Graph Edge versus Chemical Bond

The invariant distinction is:

`interaction edge ≠ chemical bond`.

A graph edge represents a model-defined interaction relation.

Chemical-bond semantics require a separate definition.

---

## 33. Graph Edge versus Mechanical Force

The invariant distinction is:

`interaction edge ≠ mechanical force`.

An edge may participate in force computation.

It is not itself a force vector.

---

## 34. Graph Edge versus Resonance Relation

The distinction remains:

`interaction edge ≠ resonance relation`.

A graph edge may provide a channel through which resonance parameters are computed.

---

## 35. Graph Edge versus Ternary State

An edge does not encode:

`-1/0/1`

by identity.

Ternary feature channels are introduced through a separate mapping.

---

## 36. Fully Connected Graph

A fully connected graph contains all admissible atom pairs.

For directed representation without self-edges:

`|E| = N(N - 1)`.

---

## 37. Sparse Graph

A sparse graph contains only selected interactions.

Sparse graphs reduce computational complexity when locality is valid for the selected model.

---

## 38. Local Graph

A local graph derives edges from a local neighborhood criterion.

Typical examples include:

- radial cutoff;
- nearest neighbors;
- topological shells.

---

## 39. Nonlocal Graph

A nonlocal graph may include long-range interactions between distant nodes.

Such edges require an explicitly defined interaction rule.

---

## 40. Hybrid Local-Nonlocal Graph

A model may combine:

`E = E_local ∪ E_nonlocal`.

The two edge classes may carry different message functions and parameters.

---

## 41. Multi-Graph

A model may define multiple edge sets:

`E^(1), E^(2), ..., E^(m)`.

Each edge family may represent a different interaction channel.

---

## 42. Typed Edges

An edge may carry a relation type:

`tau_ij ∈ K_edge`.

The type may distinguish:

- local geometric interaction;
- long-range interaction;
- cross-scale interaction;
- material-specific relation.

---

## 43. Edge Type versus Ternary State

An edge type is categorical graph metadata.

It is not a balanced ternary state unless explicitly mapped into a ternary feature channel.

---

## 44. Self Edge

A self edge is:

`i → i`.

A graph construction must explicitly define whether self edges are present.

---

## 45. Self-Edge Exclusion

A common atomic interaction graph uses:

`i ≠ j`

and excludes self edges.

This is not a universal requirement.

---

## 46. Self-Edge Features

If self edges are included, their geometric features must be defined.

For example:

`r_ii = 0`

and:

`d_ii = 0`.

Directional normalization is undefined at zero distance unless separately handled.

---

## 47. Periodic Graph

For periodic systems, graph construction must account for periodic images.

An edge may connect atom:

`i`

to a periodic image of atom:

`j`.

---

## 48. Periodic Image Shift

Let:

`n_ij ∈ Z^3`

denote a lattice-image shift.

The displacement may be written:

`r_ij = r_j + H n_ij - r_i`.

The exact sign convention must remain fixed.

---

## 49. Periodic Edge Identity

A periodic edge may require the tuple:

`(i, j, n_ij)`.

This distinguishes interactions with different periodic images.

---

## 50. Duplicate Periodic Edges

A graph builder must define whether multiple periodic images of the same atom pair may appear simultaneously.

The decision depends on:

- cell size;
- cutoff;
- physical interaction model.

---

## 51. Minimum-Image Graph

A minimum-image graph selects one displacement representative according to the minimum-image convention where applicable.

The convention is valid only under the declared geometric conditions.

---

## 52. Cell-Dependent Graph

Periodic graph connectivity may change when:

`H`

changes.

Therefore the cell matrix belongs to graph-generation state.

---

## 53. Deforming Cell

Under cell deformation:

`H → H'`

periodic edge vectors and neighbor relations must be recomputed consistently.

---

## 54. Graph under Translation

For global translation:

`r_i' = r_i + c`

relative edge vectors satisfy:

`r_ij' = r_ij`.

Therefore a geometry-based graph is translation invariant.

---

## 55. Graph under Rotation

For rotation:

`Q`

relative vectors transform:

`r_ij' = Q r_ij`.

Distance-based connectivity remains unchanged.

Directional edge features transform equivariantly.

---

## 56. Graph under Reflection

If the model is:

`O(3)`

compatible, reflection leaves distance-based connectivity unchanged while directional features transform under the declared representation.

---

## 57. Graph under Permutation

For atom permutation:

`pi`

nodes are relabeled.

The graph must transform consistently:

`i → pi(i)`.

Edge endpoints and features must be permuted consistently.

---

## 58. Permutation Equivariance of Graph Construction

Graph construction is permutation equivariant when:

`P_G(pi · X) = pi · P_G(X)`.

This is a foundational graph property.

---

## 59. Translation Invariance of Connectivity

If connectivity depends only on relative geometry, then:

`E(R + c) = E(R)`.

---

## 60. Rotation Invariance of Connectivity

If connectivity depends only on pair distances or rotation-invariant geometry:

`E(QR) = E(R)`.

---

## 61. Directional Feature Equivariance

Even when connectivity remains unchanged under rotation, edge vectors satisfy:

`r_ij → Q r_ij`.

Thus graph topology may be invariant while graph features are equivariant.

---

## 62. Graph Symmetry Contract

A graph construction must define behavior under:

- translation;
- rotation;
- reflection where applicable;
- permutation;
- periodic-image transformation.

---

## 63. Graph Is Not Required to Be Geometrically Invariant

A graph may contain orientation-dependent connectivity if the model explicitly defines such a rule.

In that case the relevant symmetry group is reduced or the external directional state must transform with the system.

---

## 64. External Field Graph

An external directional field may influence edge construction.

The field then belongs to graph input state.

Its transformation behavior must be included in the symmetry contract.

---

## 65. Species-Dependent Cutoff

The cutoff may depend on species:

`r_cut(a_i, a_j)`.

This permits different local interaction ranges for different species pairs.

---

## 66. Pair-Type Cutoff

A species-pair cutoff matrix may be defined:

`R_cut = [r_cut^(ab)]`.

This is a model parameter set.

---

## 67. Adaptive Cutoff

A cutoff may depend on local state:

`r_cut,i = F_cut(x_i)`.

If it changes dynamically, it becomes result-affecting graph state or is derived from complete state.

---

## 68. Density-Dependent Graph

Neighborhood radius or edge weight may depend on local density.

The resulting graph remains state-dependent.

---

## 69. Resonance-Dependent Graph

A specialization may permit graph construction to depend on resonance state:

`E = P_G(X_conf, X_R)`.

This creates a feedback path from resonance to graph topology.

The relation must be explicit.

---

## 70. Ternary-Dependent Graph

A specialization may permit:

`E = P_G(X_conf, T_exec)`.

This creates a hybrid discrete-geometric graph.

The ternary state does not become the graph itself.

---

## 71. Graph Feedback Boundary

If graph topology depends on ternary or resonance state, update ordering becomes part of model semantics.

---

## 72. Graph Update Ordering

A coupled implementation must define whether graph reconstruction occurs:

- before resonance evaluation;
- after ternary commit;
- before message passing;
- on selected numerical steps.

---

## 73. Graph State Memory

If graph topology is retained between rebuilds rather than recomputed every step, the retained graph belongs to computational state.

---

## 74. Stateless Graph Construction

A stateless graph builder recomputes:

`G = P_G(X_conf)`

from the current configuration whenever called.

No graph memory is then required.

---

## 75. Cached Graph

A cached graph uses prior graph state and update criteria.

The cache becomes result-affecting state.

---

## 76. Graph Cache Validity

A cached graph must define a validity condition.

When the condition fails, rebuild is required.

---

## 77. Graph Determinism

A deterministic graph builder returns the same graph and canonical edge ordering for identical complete input and parameters.

---

## 78. Edge Ordering

The mathematical graph edge set is unordered.

A computational representation may impose an edge ordering.

This ordering may affect deterministic reductions or serialization.

---

## 79. Canonical Edge Ordering

A canonical ordering may sort edges by:

- receiver;
- source;
- periodic shift;
- edge type.

The chosen ordering must be fixed when byte-identical replay depends on it.

---

## 80. Node Ordering

The node sequence follows atomic indexing in the labeled representation.

Physical predictions must remain permutation-consistent.

---

## 81. Graph Serialization

A graph artifact may contain:

- node indices;
- edge indices;
- node features;
- edge features;
- periodic shifts;
- cell;
- graph metadata.

---

## 82. Edge Index Representation

A directed graph may use an edge-index matrix containing source and receiver arrays.

The convention must be explicit.

---

## 83. Source-Receiver Convention

If:

`edge_index[0] = source`

and:

`edge_index[1] = receiver`

that convention must remain fixed across:

- graph construction;
- message passing;
- tests;
- serialization.

---

## 84. Reversed Convention

A different implementation may store receiver first.

This is valid only if every dependent operation uses the same convention.

---

## 85. Graph Feature Schema

A graph schema should distinguish:

- scalar node features;
- vector node features;
- scalar edge features;
- vector edge features;
- tensor features;
- categorical metadata.

---

## 86. Feature Type Safety

A scalar invariant feature must not be silently treated as a vector equivariant feature.

Transformation type is part of feature semantics.

---

## 87. Scalar Edge Feature

Distance:

`d_ij`

is a scalar invariant feature.

---

## 88. Vector Edge Feature

Relative displacement:

`r_ij`

is a vector equivariant feature.

---

## 89. Angular Feature

An angle or cosine constructed from pair vectors is rotationally invariant when defined from inner products and norms.

---

## 90. Tensor Edge Feature

A dyadic quantity such as:

`r_ij ⊗ r_ij`

transforms as a second-order tensor.

---

## 91. Radial Basis

A radial basis maps:

`d_ij`

to:

`phi_rad(d_ij)`.

The basis may be:

- analytic;
- learned;
- finite;
- orthogonal;
- compactly supported.

---

## 92. Radial Basis Output

Radial basis values are rotation and translation invariant because they depend only on distance.

---

## 93. Angular Basis

Angular features may depend on:

- spherical harmonics;
- angular polynomials;
- invariant dot products;
- other explicitly defined directional bases.

---

## 94. Edge Cutoff Weight

A cutoff weight may be:

`w_ij = f_cut(d_ij)`.

This scalar can modulate messages continuously near the interaction boundary.

---

## 95. Zero-Weight Edge

An edge with:

`w_ij = 0`

may remain in a candidate graph while contributing zero through the selected interaction function.

The edge remains computationally present unless removed explicitly.

---

## 96. Edge Presence versus Interaction Weight

The distinction is:

`edge presence ≠ nonzero interaction weight`.

A graph may contain structurally present edges with zero current weight.

---

## 97. Edge Multiplicity

A multigraph may permit several edges between the same ordered node pair.

Each edge must carry a distinct relation or periodic-image identifier.

---

## 98. Hypergraph Boundary

A three-body or higher-order relation may be represented through:

- multiple pair edges;
- triplet enumeration;
- hyperedges;
- tensor-product message structure.

TR-EIF does not require one universal representation.

---

## 99. Triplet Set

For central atom:

`i`

a triplet may be:

`(j, i, k)`

with:

`j ∈ N_i`

and:

`k ∈ N_i`.

The ordering and duplicate policy must be explicit.

---

## 100. Triplet Geometry

Triplet features may include:

- `d_ij`;
- `d_ik`;
- angle between `r_ij` and `r_ik`.

---

## 101. Triplet Permutation

If neighbor roles are symmetric, the representation must preserve the intended symmetry under:

`j ↔ k`.

---

## 102. Higher-Order Interaction Graph

A higher-order model may augment the pair graph with explicit triplet or many-body relation structures.

---

## 103. Graph Locality

A graph is local if each node communicates only through a bounded neighborhood under the declared graph rule.

---

## 104. Message-Passing Receptive Field

After one message-passing layer, information may propagate across one graph edge.

After multiple layers, the effective receptive field can span multiple graph hops.

---

## 105. Graph Hop

A path of one edge is one graph hop.

Graph-hop distance differs from Euclidean distance.

---

## 106. Graph Distance

Graph distance counts the minimum number of edges connecting nodes under the selected graph.

It is not physical distance.

---

## 107. Graph Distance versus Euclidean Distance

The distinction remains:

`graph distance ≠ Euclidean distance`.

A graph may connect physically distant nodes through nonlocal edges.

---

## 108. Connected Component

A connected component is a maximal connected node subset under the graph topology.

---

## 109. Disconnected Graph

An atomic configuration may generate several disconnected graph components if the cutoff or interaction rule separates regions.

---

## 110. Disconnected Graph versus Separate Physical Systems

Disconnected graph components need not imply physically independent systems if omitted long-range interactions still couple them.

---

## 111. Graph Connectivity

Connectivity is a property of the chosen graph representation.

It is not a universal physical observable.

---

## 112. Degree

For node:

`i`

the in-degree may be:

`deg_in(i) = |N_i|`

for directed incoming neighborhoods.

The out-degree is separately defined.

---

## 113. Degree versus Coordination Number

Graph degree may equal a chosen coordination count when both use the same neighbor definition.

The two are not universally identical.

---

## 114. Weighted Degree

A weighted degree may use:

`deg_w(i) = sum_j w_ij`.

This is a graph observable.

---

## 115. Adjacency Matrix

A graph may be represented by:

`A = [A_ij]`.

For a binary directed graph:

`A_ij = 1`

when:

`j → i`

exists under the selected convention.

---

## 116. Weighted Adjacency

A weighted adjacency matrix may use:

`A_ij = w_ij`.

The weight semantics must be explicit.

---

## 117. Adjacency versus Coupling Matrix

A phase coupling matrix:

`K_ij`

may be derived from the interaction graph.

However:

`adjacency ≠ coupling strength`

unless explicitly defined.

---

## 118. Graph-to-Phase Coupling

A mapping may be:

`K_ij = F_K(e_ij, h_i, h_j, ...)`.

This connects EIF graph structure to the TR phase layer.

---

## 119. Graph-to-Resonance Mapping

Graph features may contribute to resonance state:

`r_i = P_R(h_i, {e_ij}, ...)`.

The graph remains upstream of resonance.

---

## 120. Graph-to-Ternary Mapping

A graph-derived feature may eventually influence:

`t_target`.

The canonical chain remains:

`graph`

`→ representation`

`→ resonance`

`→ target`.

---

## 121. Direct Graph-to-Target Specialization

A specialization may define:

`P_GT: X_G → T_target`.

Such a mapping remains upstream of executed ternary state.

---

## 122. Graph-to-Energy Mapping

An energy model may consume graph state:

`E = F_E(G, H, ...)`.

The graph is an argument to the energy model.

It is not energy.

---

## 123. Graph-to-Force Mapping

Force may be obtained from an energy functional or another declared equivariant force model.

The graph provides interaction structure.

It is not the force itself.

---

## 124. Graph-to-Stress Mapping

Stress may depend on graph-mediated energy and geometry.

The resulting tensor remains separately typed.

---

## 125. Message Function

For edge:

`j → i`

a message function may be:

`m_ij = M(h_i, h_j, e_ij)`.

Chapter 05 develops the full message-passing formalism.

---

## 126. Receiver Update

A node update may aggregate incoming messages:

`m_i = A({m_ij | j ∈ N_i})`.

The aggregation must preserve permutation semantics.

---

## 127. Permutation-Invariant Aggregation

Common aggregation operators include:

- sum;
- mean;
- max;
- invariant learned aggregation.

---

## 128. Sum Aggregation

A sum is independent of neighbor ordering:

`m_i = sum_(j ∈ N_i) m_ij`.

---

## 129. Mean Aggregation

A mean normalizes by neighborhood size:

`m_i = (1 / |N_i|) sum_j m_ij`

when:

`|N_i| > 0`.

---

## 130. Empty Neighborhood

The model must define behavior when:

`N_i = empty`.

Possible policies include:

- zero aggregate;
- self feature only;
- explicit isolated-node state.

The policy must be explicit.

---

## 131. Isolated Node

An isolated graph node has no active incident interaction edges under the selected graph.

This does not mean the atom is invalid.

---

## 132. Edge Mask

A graph representation may use a mask:

`M_ij ∈ {0,1}`

or another boolean encoding.

A binary graph mask is not a balanced ternary state.

---

## 133. Mask versus Ternary Channel

The distinction is:

`edge mask ≠ ternary feature`.

A ternary feature requires explicit semantic mapping into:

`-1/0/1`.

---

## 134. Graph Sparsification

A dense graph may be sparsified according to:

- cutoff;
- learned score;
- top-k neighbors;
- physical interaction range.

The sparsification rule must preserve the intended symmetry contract.

---

## 135. Top-k Graph

A top-k graph selects a fixed number of nearest or highest-score neighbors.

Tie handling must be deterministic where deterministic execution is required.

---

## 136. Top-k Tie Handling

Equal distances or scores require a canonical tie rule.

Possible deterministic criteria include node index after symmetry-equivalent candidate construction.

The tie rule is computational metadata and must not alter permutation consistency of physical outputs.

---

## 137. k-Nearest-Neighbor Graph

A k-nearest-neighbor graph need not be symmetric.

Node:

`j`

may be among the nearest neighbors of:

`i`

without the reverse relation holding.

---

## 138. Symmetrized kNN Graph

A kNN graph may be symmetrized by:

- union;
- intersection;
- explicit bidirectional completion.

The chosen rule must be stated.

---

## 139. Radius Graph

A radius graph uses a geometric cutoff.

It may be naturally symmetric in pair membership while still represented as directed edges.

---

## 140. Hybrid Radius-kNN Graph

A model may combine radius and neighbor-count constraints.

The rule must remain deterministic and explicit.

---

## 141. Learned Edge Score

A learned score may be:

`s_ij = F_score(h_i, h_j, e_ij)`.

It may modulate edge weight or determine graph sparsification.

---

## 142. Learned Graph Topology

If learned scores determine edge presence, graph topology becomes trainable or state-dependent.

This may introduce discrete graph changes during optimization or inference.

---

## 143. Differentiable Graph Weight

A continuous edge weight can preserve differentiability even when the candidate graph remains fixed.

---

## 144. Discrete Learned Edge Selection

Hard learned edge selection is a discrete operation.

Its gradient treatment belongs to the learning layer.

---

## 145. Graph Equivariance Requirement

Learned graph construction must preserve the declared symmetry.

For example, a distance-only score can remain rotation invariant.

A directional score must transform consistently with its output semantics.

---

## 146. Graph Permutation Requirement

Learned edge generation must remain permutation consistent with atomic relabeling.

---

## 147. Graph Local Feature Frame

A model may construct a local frame from geometry.

Any frame construction must define behavior under:

- rotation;
- reflection;
- degeneracy.

---

## 148. Frame Degeneracy

A local frame may become undefined when its defining vectors are collinear or zero.

The model must define fallback or invariant handling.

---

## 149. Frame-Free Representation

Equivariant representations may avoid explicit local frames by using group representations directly.

This is developed in Chapters 03 and 04.

---

## 150. Spherical Direction

The unit vector:

`e_hat_ij`

may be represented through spherical coordinates or spherical harmonics.

The underlying geometric vector remains the source object.

---

## 151. Spherical Harmonic Edge Feature

A directional basis may use:

`Y_lm(e_hat_ij)`.

Its transformation behavior is governed by the corresponding rotational representation.

---

## 152. Radial-Angular Factorization

An edge feature may be factorized into:

`radial part × angular part`.

This structure is common in E(3)-equivariant models.

---

## 153. Graph Feature Irreducible Type

An equivariant feature may carry an angular representation label such as:

`l`.

The precise irreducible representation formalism is developed in Chapter 04.

---

## 154. Scalar Channel

A scalar channel transforms trivially under rotation.

Examples include:

- species embedding;
- distance;
- radial basis value.

---

## 155. Vector Channel

A vector channel transforms under the standard three-dimensional rotation representation.

Examples include:

- relative displacement;
- force;
- velocity.

---

## 156. Higher-Order Channel

Higher-order features transform under the corresponding tensor or irreducible representation.

---

## 157. Graph Edge Symmetry Pair

For bidirectional geometric edges:

`r_ji = -r_ij`.

A model may exploit this relation explicitly.

---

## 158. Symmetric Scalar Edge Feature

Distance-based scalar features satisfy:

`e_scalar,ij = e_scalar,ji`

when species-order effects are absent.

---

## 159. Species-Ordered Edge Feature

A directed edge feature may depend on ordered species pair:

`(a_i, a_j)`.

Then reverse edges may have different learned embeddings.

---

## 160. Symmetric Species-Pair Feature

A model may instead use an unordered pair representation.

This enforces symmetry under exchanging source and receiver species in that feature.

---

## 161. Directed Message Asymmetry

Even with symmetric geometric edges, message functions may be directed because receiver node state differs from source node state.

---

## 162. Edge Update

A message-passing model may update edge features:

`e_ij^(l+1) = F_E(e_ij^(l), h_i^(l), h_j^(l), ...)`.

This creates dynamic latent graph features while topology may remain fixed.

---

## 163. Node Update

Node state may evolve:

`h_i^(l+1) = F_H(h_i^(l), m_i^(l))`.

---

## 164. Global Graph State

A graph may contain global feature:

`g ∈ X_global`.

It may encode:

- composition;
- cell descriptor;
- thermodynamic control state;
- global resonance state.

---

## 165. Global-to-Node Message

A global state may influence local node updates.

The mapping must preserve required symmetries.

---

## 166. Node-to-Global Aggregation

Node features may be aggregated into a global graph representation.

The aggregation must preserve permutation invariance for global scalar outputs.

---

## 167. Edge-to-Global Aggregation

Edge features may also contribute to global state.

Duplicate edge counting must be handled consistently.

---

## 168. Double Counting

In bidirectional graphs, pair contributions may be counted twice if each directed edge contributes independently.

Energy or other symmetric pair quantities must define whether a factor such as:

`1/2`

or another aggregation rule is required.

---

## 169. Directed Messages and Pair Energy

Directed message representation does not require directed physical pair energy.

The representation and physical functional remain separate.

---

## 170. Energy Decomposition

An energy may be decomposed:

`E = sum_i E_i`

where each:

`E_i`

depends on a local graph environment.

The decomposition itself may not be unique.

---

## 171. Edge Energy Decomposition

A pair model may use:

`E = sum_(i,j) E_ij`

with a counting convention.

The counting convention must be explicit.

---

## 172. Message Passing versus Physical Interaction

A message is a computational feature transformation.

It is not a mechanical interaction force by identity.

---

## 173. Message Passing versus Energy Transfer

A learned message does not automatically represent physical energy transfer.

---

## 174. Graph Depth

The number of message-passing layers determines computational propagation depth through graph hops.

It is a model architecture parameter.

---

## 175. Graph Depth versus Physical Time

Message-passing depth is not physical time.

---

## 176. Graph Depth versus Resonance Tact

Likewise:

`message-passing layer ≠ ternary execution tact`.

---

## 177. Static Graph Message Passing

A model may hold graph topology fixed across all representation layers.

---

## 178. Dynamic Latent Graph

A model may update edge weights or topology between layers.

The update semantics must remain explicit.

---

## 179. Graph Pooling

A graph may be pooled into a coarser graph.

This creates a multiscale representation.

---

## 180. Cluster Node

A coarse node may represent a cluster of atoms.

Its state is derived from fine-scale nodes.

---

## 181. Fine-to-Coarse Mapping

A pooling map may be:

`P_pool: X_G,fine → X_G,coarse`.

This mapping is generally information reducing.

---

## 182. Coarse-to-Fine Mapping

A reverse mapping may distribute coarse state back to atoms.

It is not necessarily an inverse of pooling.

---

## 183. Multiscale Graph

A multiscale graph may contain:

- atomic nodes;
- cluster nodes;
- mesoscale nodes;
- cross-scale edges.

---

## 184. Cross-Scale Edge

A cross-scale edge connects nodes belonging to different abstraction levels.

Its semantics must be explicitly defined.

---

## 185. Cross-Scale Edge versus Physical Bond

A cross-scale edge is not a chemical bond.

---

## 186. Graph Hierarchy

A hierarchical graph may be represented as:

`G^(0) → G^(1) → ... → G^(L)`.

Each level has its own node and edge state spaces.

---

## 187. Graph-to-Resonance Hierarchy

Resonance features may be computed at:

- edge level;
- node level;
- cluster level;
- global level.

---

## 188. Edge Resonance Descriptor

An edge may carry a resonance descriptor:

`r_ij ∈ X_R,edge`.

This descriptor is derived from graph and equivariant features.

It is not the edge itself.

---

## 189. Node Resonance Descriptor

A node may carry:

`r_i ∈ X_R,node`.

---

## 190. Global Resonance Descriptor

The full graph may produce:

`r_G ∈ X_R,global`.

---

## 191. Resonance Aggregation

Local resonance states may be aggregated into higher-scale resonance state.

The aggregation must remain explicit.

---

## 192. Ternary Edge Feature

Chapter 07 may define:

`t_ij ∈ {-1, 0, 1}`.

This is a ternary feature associated with an edge.

It is distinct from edge presence.

---

## 193. Ternary Node Feature

Likewise:

`t_i ∈ {-1, 0, 1}`

may be associated with a node.

---

## 194. Ternary Graph Feature

A global graph ternary state may also exist under a separately defined aggregation.

---

## 195. Active Neutral Graph Feature

A ternary graph feature equal to:

`0`

is active neutral under the corresponding ternary semantics.

It is not a missing graph feature.

---

## 196. Missing Edge Feature

A missing or unavailable edge feature must use an explicit mask or validation state.

It must not be encoded semantically as ternary neutral.

---

## 197. Graph Mask and Neutral Separation

The framework preserves:

`graph mask 0 ≠ ternary state 0`

unless an explicit encoding conversion is defined.

---

## 198. Graph Validation

A graph validator may verify:

- node count;
- edge endpoint validity;
- self-edge policy;
- periodic-image validity;
- cutoff consistency;
- feature dimensions;
- canonical ordering;
- symmetry behavior.

---

## 199. Endpoint Validation

Every edge endpoint must satisfy:

`i ∈ V`

and:

`j ∈ V`.

---

## 200. Self-Edge Validation

If self edges are prohibited:

`i ≠ j`

must hold for every edge.

---

## 201. Cutoff Validation

For a hard radius graph:

`d_ij ≤ r_cut`

must hold for every included edge under the selected convention.

---

## 202. Completeness Validation

If the graph is intended to include all admissible neighbors, every qualifying pair must be represented.

---

## 203. Duplicate-Edge Validation

The graph contract must define whether duplicate directed edges are permitted.

A validator checks that policy.

---

## 204. Periodic-Shift Validation

Periodic edge shifts must reproduce the serialized displacement consistently:

`r_ij = r_j + H n_ij - r_i`.

---

## 205. Translation Validation

Translate the complete configuration by:

`c`.

Graph connectivity must remain invariant when the graph rule is translation invariant.

Relative vectors remain unchanged.

---

## 206. Rotation Validation

Rotate the configuration by:

`Q`.

Distance-based connectivity must remain unchanged.

Vector edge features must transform by:

`Q`.

---

## 207. Reflection Validation

If:

`O(3)`

equivariance is claimed, reflection tests must verify the declared feature transformation rules.

---

## 208. Permutation Validation

Apply a species-preserving permutation.

The graph must permute consistently with nodes and edges.

---

## 209. Periodic Equivalence Validation

Equivalent periodic images must produce equivalent graph relations under the declared periodic graph contract.

---

## 210. Deterministic Graph Replay

Identical configuration, graph parameters, and ordering rules must generate the same graph under a deterministic graph builder.

---

## 211. Edge-Ordering Replay

If edge ordering affects downstream byte-identical artifacts, canonical edge ordering must be reproduced exactly.

---

## 212. Graph Hash

A graph hash depends on its serialized representation.

Physical equivalence under permutation or symmetry does not automatically imply identical graph hash unless canonicalization is applied.

---

## 213. Graph Provenance

Graph definitions and artifacts may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 214. Derived Graph

A graph generated deterministically from an atomic configuration and declared graph rule carries:

`DERIVED`

provenance where applicable.

---

## 215. Author-Defined Graph Rule

A TR-EIF-specific graph-generation rule carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 216. Calibrated Cutoff

A cutoff fitted to material or dataset behavior carries:

`CALIBRATED`

provenance.

---

## 217. Primary-Source Graph Parameter

A graph parameter taken directly from a cited scientific source carries:

`PRIMARY_SOURCE`

provenance.

---

## 218. Benchmark Graph

A graph used to measure scaling, memory, throughput, or neighbor-search performance may carry:

`BENCHMARK`

provenance for the associated result.

---

## 219. Graph Test Fixture

A synthetic graph or atomic configuration designed for invariant testing carries:

`TEST_FIXTURE`

provenance.

---

## 220. Graph Scaling

For:

`N`

nodes and average degree:

`d_bar`

a sparse directed graph contains approximately:

`N d_bar`

edges.

The exact count depends on graph topology.

---

## 221. Dense Scaling

A fully connected directed graph without self edges contains:

`N(N - 1)`

edges.

This scales quadratically with:

`N`.

---

## 222. Local Graph Scaling

For bounded physical density and finite local cutoff, average degree may remain approximately bounded with increasing system size under suitable conditions.

Then edge count can scale approximately linearly with:

`N`.

---

## 223. Graph Memory

Memory cost depends on:

- number of nodes;
- number of edges;
- feature dimensions;
- representation precision;
- periodic metadata.

---

## 224. Graph Compute Cost

Message-passing cost commonly depends on edge count and feature dimensions.

The exact complexity depends on architecture.

---

## 225. Graph Scaling Benchmark

A benchmark should state:

- atom count;
- edge count;
- average degree;
- cutoff;
- hardware/software environment;
- precision;
- measured operation.

---

## 226. Graph Density

Define:

`rho_G = |E| / [N(N - 1)]`

for a directed graph without self edges and:

`N > 1`.

This is a graph-density measure.

It is not physical mass density.

---

## 227. Graph Density versus Physical Density

The distinction is:

`graph density ≠ material density`.

---

## 228. Graph Degree Distribution

A graph may be characterized by its node-degree distribution.

This is a derived topology observable.

---

## 229. Graph Topology versus Material Structure

Graph topology may reflect material structure when the graph rule is physically motivated.

It remains a representation-dependent object.

---

## 230. Graph Topology versus Physical Phase

A graph topology change is not automatically a physical phase transition.

---

## 231. Graph Topology versus Resonance Regime

A graph change may alter resonance state.

It is not identical to a resonance-regime transition.

---

## 232. Graph Topology versus Ternary Transition

Likewise:

`graph topology change ≠ ternary transition`.

---

## 233. Dynamic Graph and Hybrid State

A complete dynamic graph system may contain:

`X_dyn = X_conf × X_G × X_EQ × X_R × X_T`.

This forms a hybrid geometric-graph-resonance-ternary state when graph topology changes discretely.

---

## 234. Graph State Closure

If future outputs depend on retained graph topology or cached neighbor state, those variables belong to the complete state.

---

## 235. Graph Restart

A restart-complete artifact may either:

- serialize the graph;
- deterministically rebuild it from configuration and parameters.

The choice must be explicit.

---

## 236. Rebuild-on-Restart

If graph reconstruction is deterministic and stateless, storing the graph may be unnecessary.

---

## 237. Cached-Restart State

If neighbor-list skin, displacement counters, or cache state affect future rebuild timing, this state must be preserved for exact replay.

---

## 238. Graph Numerical Precision

Finite coordinate precision may alter cutoff membership near:

`r_cut`.

The numerical comparison contract must therefore be explicit.

---

## 239. Cutoff Chatter

Pairs oscillating near:

`r_cut`

may repeatedly enter and exit a hard graph.

This is graph-topology chatter.

---

## 240. Cutoff Hysteresis

A graph builder may use different entry and exit radii:

`r_enter`

and:

`r_exit`.

This creates graph hysteresis.

It is a graph-control mechanism, not ternary neutral routing.

---

## 241. Graph Hysteresis State

When edge membership depends on previous graph state, the graph contains memory.

Previous edge state then becomes result-affecting.

---

## 242. Graph Hysteresis versus Ternary Hysteresis

Graph hysteresis and ternary target hysteresis are distinct mechanisms.

---

## 243. Graph Hysteresis versus Neutral Routing

The distinction remains:

`graph hysteresis ≠ neutral routing`.

---

## 244. Edge Persistence

A model may require an edge condition to persist before graph creation or removal.

This is graph-topology persistence.

---

## 245. Edge Persistence versus Dynamical Stability

Persistent graph connectivity does not establish dynamical stability.

---

## 246. Graph Spectral Representation

A graph may be analyzed using:

- adjacency spectrum;
- Laplacian;
- normalized Laplacian;
- learned spectral operators.

These are graph-theoretic representations.

---

## 247. Graph Laplacian

For a weighted undirected graph:

`L = D - A`

where:

`D`

is the degree matrix.

The precise form depends on the graph convention.

---

## 248. Laplacian versus Physical Operator

A graph Laplacian is not automatically a physical mechanical or quantum operator.

Any physical interpretation requires an explicit model.

---

## 249. Graph Eigenmode

A graph eigenmode is an eigenvector of a selected graph operator.

It is not an oscillator phase mode by identity.

---

## 250. Graph Spectral Feature to Resonance

Graph spectral features may enter resonance parameterization through an explicit mapping.

---

## 251. Interaction Graph Extension Rule

Any graph extension must define:

1. node set;
2. edge set;
3. directedness;
4. self-edge policy;
5. graph-construction rule;
6. node features;
7. edge features;
8. periodic treatment;
9. symmetry behavior;
10. deterministic ordering;
11. validation;
12. provenance.

---

## 252. Cutoff Extension Rule

Any cutoff-based graph must define:

1. cutoff value;
2. units;
3. equality convention;
4. species dependence;
5. periodic handling;
6. smoothing;
7. rebuild policy;
8. provenance.

---

## 253. Periodic Graph Extension Rule

Any periodic graph must define:

1. cell convention;
2. image-shift convention;
3. duplicate-image policy;
4. minimum-image policy where used;
5. deformation behavior;
6. validation.

---

## 254. Dynamic Graph Extension Rule

Any dynamic graph must define:

1. update trigger;
2. retained graph state;
3. creation rule;
4. removal rule;
5. hysteresis where used;
6. event ordering;
7. restart semantics.

---

## 255. Learned Graph Extension Rule

Any learned graph construction must define:

1. candidate edge set;
2. learned score;
3. hard or soft selection;
4. symmetry behavior;
5. permutation behavior;
6. tie handling;
7. training/inference semantics.

---

## 256. Multiscale Graph Extension Rule

Any multiscale graph must define:

1. scale-specific node sets;
2. scale-specific edge sets;
3. pooling;
4. unpooling or feedback;
5. cross-scale edges;
6. information loss;
7. symmetry behavior.

---

## 257. Canonical Graph Invariants

Every conforming interaction graph preserves:

1. explicit node identity;

2. explicit edge identity;

3. explicit source/receiver convention;

4. explicit graph-construction rule;

5. explicit edge geometry;

6. explicit symmetry behavior;

7. explicit periodic-image handling where applicable;

8. explicit deterministic ordering when required.

---

## 258. Canonical Geometric Graph Invariants

For geometry-derived edges:

`r_ij = r_j - r_i`

under the applicable image convention,

`r_ji = -r_ij`

and:

`d_ij = d_ji`.

Distance is invariant under rigid translation and rotation.

Relative displacement is rotation equivariant.

---

## 259. Canonical Permutation Invariant

Graph construction preserves:

`P_G(pi · X) = pi · P_G(X)`

for admissible atom permutations.

---

## 260. Canonical Type Separation

The framework preserves:

`graph ≠ atomic configuration`

`edge ≠ chemical bond`

`edge ≠ mechanical force`

`edge ≠ resonance state`

`edge ≠ ternary state`

`edge mask ≠ active neutral`

`graph distance ≠ Euclidean distance`

`graph density ≠ physical density`

`message ≠ physical interaction by identity`.

---

## 261. Canonical TR Integration Invariants

The interaction graph remains upstream of:

- equivariant representation;
- resonance state;
- ternary target;
- executed ternary state.

The canonical chain remains:

`graph`

`→ equivariant representation`

`→ resonance`

`→ target`

`→ execution`.

---

## 262. Canonical Ternary Boundary

Any graph-derived ternary feature must map explicitly into:

`-1/0/1`.

The state:

`0`

remains active neutral.

Graph absence, masking, invalidity, or missing data remain separately represented.

---

## 263. Canonical Scientific Distinctions

The interaction-graph layer preserves:

`interaction edge ≠ chemical bond`

`interaction edge ≠ force`

`graph topology change ≠ structural transition`

`graph topology change ≠ physical phase transition`

`graph topology change ≠ ternary transition`

`graph topology change ≠ resonance transition`

`phase relation ≠ chemical bond`

`phase coupling ≠ mechanical force`

`resonance classification ≠ energy`

`ternary state ≠ energy`

`descriptor ≠ configuration`

`graph ≠ physical system by identity`.

---

## 264. EIF Graph Chain

The canonical EIF graph chain is:

`atomic configuration`

`→ graph construction`

`→ node/edge geometric state`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary channels`

`→ energy / force / stress`.

---

## 265. Graph-to-TR Chain

The TR-facing path is:

`X_G`

`→ X_EQ`

`→ X_R`

`→ T_target`

`→ T_exec`.

No graph edge directly becomes an executed ternary transition.

---

## 266. Feedback into Graph State

A later specialization may use:

`X_TR`

to influence:

- graph weights;
- graph topology;
- local cutoff;
- interaction classes.

Such feedback must be defined as an explicit graph update mapping.

---

## 267. Interface to Chapter 03

Chapter 03 develops E(3) Group Actions.

It formalizes the transformations already introduced here for:

- positions;
- relative vectors;
- scalar features;
- vector features;
- tensor features;
- graph permutations.

---

## 268. Interface to Chapter 04

Chapter 04 develops Equivariant Representations.

The interaction graph supplies:

- node attributes;
- relative vectors;
- invariant distances;
- angular relations;
- periodic-image state;
- graph topology.

---

## 269. Interface to Chapter 05

Chapter 05 develops Message Passing.

It defines how information propagates over:

`j → i`

edges while preserving permutation and E(3) transformation structure.

---

## 270. Interface to Chapter 06

Chapter 06 develops Resonance Parameterization.

Graph-derived equivariant features become inputs to local and collective resonance coordinates.

---

## 271. Interface to Chapter 07

Chapter 07 develops Ternary Feature Channels.

Graph-derived continuous or resonance features may be mapped into exact:

`-1/0/1`

channels while preserving active-neutral semantics.

---

## 272. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

The graph provides the interaction structure used by local or global energy representations.

---

## 273. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

The graph mediates geometry-dependent model interactions while vector and tensor outputs preserve the required equivariance.

---

## 274. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Graph architecture becomes one configurable structural component of the model family.

---

## 275. Final Formal Structure

The interaction-graph layer may be represented as:

`IG = (V, E, H, E_feat, G_global, P_G, rho_G)`.

Here:

- `V` is the atomic node set;
- `E` is the interaction edge set;
- `H` is node-feature state;
- `E_feat` is edge-feature state;
- `G_global` is optional global graph state;
- `P_G` is graph construction;
- `rho_G` is the graph symmetry action.

For geometric edges, principal edge quantities include:

`r_ij`

`d_ij`

`e_hat_ij`

and optional periodic shift:

`n_ij`.

---

## 276. Final Statement

Interaction graphs provide the explicit relational structure connecting atomic configuration space to equivariant interatomic computation.

Atoms become graph nodes.

Model-defined interaction relations become graph edges.

Edges may carry:

- relative displacement;
- distance;
- direction;
- periodic image shift;
- radial features;
- angular features;
- learned features;
- later resonance and ternary channels.

Graph topology may be static or dynamic, local or nonlocal, directed or symmetrized, single-scale or multiscale.

The graph construction must preserve the declared behavior under:

- translation;
- rotation;
- reflection where applicable;
- species-preserving permutation;
- periodic-image equivalence.

The framework preserves:

`interaction edge ≠ chemical bond`

`interaction edge ≠ mechanical force`

`graph topology change ≠ structural transition`

`graph topology change ≠ ternary transition`

`graph mask 0 ≠ active-neutral 0`.

The canonical forward path remains:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ energy / forces / stress`.

These definitions establish the graph structure required for the E(3) Group Actions developed in Chapter 03.
