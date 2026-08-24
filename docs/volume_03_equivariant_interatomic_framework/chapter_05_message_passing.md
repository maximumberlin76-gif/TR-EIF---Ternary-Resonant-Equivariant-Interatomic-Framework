# Message Passing

## 1. Purpose

This chapter defines the message-passing layer of the Equivariant Interatomic Framework within TR-EIF.

Message passing propagates information over the interaction graph while preserving:

- spatial equivariance;
- atom-permutation equivariance;
- representation-type separation;
- locality;
- deterministic update semantics;
- explicit source/receiver orientation;
- interfaces to resonance parameterization;
- interfaces to ternary feature channels;
- interfaces to energy, force, and stress.

The canonical chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

Message passing is a computational feature-propagation mechanism.

It is not mechanical force, physical energy transfer, chemical bonding, oscillator phase coupling, or ternary execution by identity.

---

## 2. Graph Domain

Let:

`G = (V, E)`

be the interaction graph.

The node set is:

`V = {1, ..., N}`.

A directed edge:

`j → i`

represents information propagation from source:

`j`

to receiver:

`i`.

---

## 3. Receiver Convention

Throughout this chapter:

`j → i`

means:

- source = `j`;
- receiver = `i`.

The corresponding relative displacement is:

`r_ij = r_j - r_i`

under the applicable periodic-image convention.

This orientation must remain fixed throughout equations, code, tests, and serialized artifacts.

---

## 4. Node Representation

At message-passing layer:

`k`

let the node state be:

`h_i^[k] ∈ X_node^[k]`.

The index:

`k`

denotes message-passing depth.

It is not:

- physical time;
- numerical timestep;
- ternary execution tact;
- irrep degree.

---

## 5. Edge Representation

For edge:

`j → i`

let:

`e_ij^[k] ∈ X_edge^[k]`.

The edge representation may include:

- distance;
- relative direction;
- radial basis features;
- angular representation;
- species-pair features;
- periodic-image shift;
- learned latent state;
- resonance-related features at later stages.

---

## 6. Global Representation

A message-passing layer may also consume:

`g^[k] ∈ X_global^[k]`.

Global state may include:

- composition;
- cell information;
- global invariant descriptors;
- external control state;
- global resonance variables.

---

## 7. Message Function

For directed edge:

`j → i`

define:

`m_ij^[k] = M^[k](h_i^[k], h_j^[k], e_ij^[k], g^[k])`.

The function:

`M^[k]`

is the message map.

---

## 8. Message Space

The message belongs to:

`m_ij^[k] ∈ X_msg^[k]`.

The message space may contain multiple irreducible representation channels.

---

## 9. Directed Message

A message is receiver-specific.

In general:

`m_ij ≠ m_ji`.

Even when pair geometry is symmetric, source and receiver node states may differ.

---

## 10. Message versus Edge

The distinction is:

`message ≠ graph edge`.

The edge defines a relation.

The message is a computed feature propagated over that relation.

---

## 11. Message versus Force

The invariant distinction is:

`message ≠ mechanical force`.

A vector-valued message may transform like a vector without carrying force semantics.

---

## 12. Message versus Energy Transfer

The distinction is:

`message ≠ physical energy transfer`.

A learned message carries computational information unless an explicit physical mapping assigns another interpretation.

---

## 13. Message versus Chemical Bond

The distinction remains:

`message ≠ chemical bond`.

---

## 14. Message versus Oscillator Coupling

The distinction remains:

`message passing ≠ Kuramoto-Sakaguchi phase coupling`.

The two mechanisms may later interact through explicit mappings.

---

## 15. Message versus Ternary Transition

A message update does not directly constitute:

`-1 → 0`

`0 → 1`

or any other ternary transition.

---

## 16. Incoming Neighborhood

For receiver:

`i`

define:

`N_i = {j | j → i ∈ E}`.

All incoming messages for node:

`i`

are:

`{m_ij | j ∈ N_i}`.

---

## 17. Aggregation

Define an aggregation operator:

`A`.

The aggregated message is:

`m_i^[k] = A({m_ij^[k] | j ∈ N_i})`.

---

## 18. Permutation-Invariant Aggregation

The aggregation must not depend on arbitrary neighbor ordering.

For admissible permutation of incoming messages:

`A({m_ij})`

must produce the same receiver aggregate under the corresponding reindexing.

---

## 19. Sum Aggregation

A canonical aggregation is:

`m_i = sum_(j ∈ N_i) m_ij`.

This is invariant to neighbor ordering.

---

## 20. Mean Aggregation

A mean aggregation may use:

`m_i = (1 / |N_i|) sum_(j ∈ N_i) m_ij`

when:

`|N_i| > 0`.

---

## 21. Maximum Aggregation

Selected scalar channels may use a maximum operation.

Such an operation requires compatible transformation semantics.

A componentwise maximum over vector coordinates does not generally preserve rotation equivariance.

---

## 22. Weighted Aggregation

A weighted aggregation may be:

`m_i = sum_j w_ij m_ij`.

If:

`w_ij`

is an invariant scalar, the representation type of:

`m_ij`

is preserved.

---

## 23. Learned Weights

A learned weight may be:

`w_ij = F_w(h_i, h_j, e_ij)`.

If it is used as a scalar multiplier in an equivariant sum, it must transform as an invariant scalar.

---

## 24. Attention

An attention-style aggregation may use:

`alpha_ij`.

For scalar attention:

`alpha_ij`

must be permutation-consistent and spatially invariant when multiplying equivariant messages.

---

## 25. Attention Normalization

A normalized attention coefficient may use:

`alpha_ij = exp(s_ij) / sum_(q ∈ N_i) exp(s_iq)`.

The score:

`s_ij`

must have the transformation behavior required by the message architecture.

---

## 26. Attention Is Not Physical Weight

A learned attention coefficient is not automatically:

- coupling energy;
- bond strength;
- force magnitude;
- resonance amplitude.

Its semantics depend on the model.

---

## 27. Empty Neighborhood

If:

`N_i = empty`

the aggregation contract must define the result.

Possible valid designs include:

- zero representation of each channel type;
- retained node state;
- self-interaction path;
- explicit isolated-node branch.

---

## 28. Zero Aggregate

A zero aggregate is a representation zero.

It is not ternary active neutral by identity.

---

## 29. Node Update

The node update is:

`h_i^[k+1] = U^[k](h_i^[k], m_i^[k], g^[k])`.

The update must preserve the declared representation types.

---

## 30. Residual Node Update

A residual update may use:

`h_i^[k+1] = h_i^[k] + Delta h_i^[k]`.

The two terms must carry compatible transformation types.

---

## 31. Gated Node Update

An invariant scalar gate may control an equivariant feature:

`h_out^(l) = g h_in^(l)`.

This preserves the transformation type.

---

## 32. Edge Update

Edge state may also evolve:

`e_ij^[k+1] = U_E^[k](e_ij^[k], h_i^[k], h_j^[k], m_ij^[k], g^[k])`.

---

## 33. Static Edge Representation

A model may keep geometric edge features fixed across message-passing layers.

For example:

`r_ij`

and:

`d_ij`

may remain unchanged while node latent state evolves.

---

## 34. Dynamic Edge Representation

A model may update learned edge features across layers.

This does not require graph topology to change.

---

## 35. Dynamic Topology

A stronger model may alter:

`E`

between layers.

If topology changes, the graph-update rule must remain explicit and equivariant.

---

## 36. Message-Passing Layer

One message-passing layer consists of:

1. edge message construction;
2. neighbor aggregation;
3. node update;
4. optional edge update;
5. optional global update.

---

## 37. Layer Composition

For:

`L`

layers:

`X_EQ^[0]`

`→ X_EQ^[1]`

`→ ...`

`→ X_EQ^[L]`.

The output of one layer becomes input to the next.

---

## 38. Layer Depth

The number:

`L`

is an architecture parameter.

It controls computational propagation depth.

---

## 39. Graph-Hop Receptive Field

After one local layer, node:

`i`

can depend directly on one-hop neighbors.

After:

`L`

layers, information may propagate across paths of up to:

`L`

graph hops, subject to architecture details.

---

## 40. Receptive Field versus Physical Range

The distinction remains:

`graph-hop receptive field ≠ physical interaction range`.

---

## 41. Message-Passing Depth versus Physical Time

The distinction remains:

`message-passing depth ≠ physical time`.

---

## 42. Message-Passing Depth versus Ternary Tact

The distinction remains:

`message-passing layer ≠ ternary execution tact`.

---

## 43. Message-Passing Depth versus Oscillator Phase Step

Likewise:

`message layer ≠ phase integration step`.

---

## 44. Spatial Equivariance

For group element:

`g`

a message-passing layer must satisfy:

`MP(rho_in(g)x) = rho_out(g) MP(x)`.

---

## 45. Node Equivariance

Per-node features transform according to:

- spatial representation;
- atom permutation.

---

## 46. Message Equivariance

A message:

`m_ij`

must transform as:

`m_ij' = rho_msg(g) m_ij`

when all inputs are transformed consistently.

---

## 47. Aggregation Equivariance

Summation of same-type equivariant messages preserves spatial transformation type.

---

## 48. Permutation Equivariance

Under atom permutation:

`pi`

the updated node state must satisfy:

`h_i'(pi · X) = h_(pi(i))(X)`

under the selected indexing convention.

---

## 49. Combined Equivariance

A complete message-passing layer may satisfy:

`MP((g,pi) · X) = (g,pi) · MP(X)`.

---

## 50. Scalar Message Channel

A scalar message is invariant under spatial rotation.

Its value may still depend on geometry through invariant descriptors such as:

- distance;
- norms;
- dot products;
- scalar latent features.

---

## 51. Vector Message Channel

A vector message transforms:

`m_ij' = Q m_ij`.

---

## 52. Tensor Message Channel

A tensor message transforms according to its declared tensor or irreducible representation.

---

## 53. Irreducible Message Channel

An irrep message may be indexed by:

`(l,p)`.

The message function must preserve the corresponding representation law.

---

## 54. Tensor-Product Message

A message may be formed through tensor product between:

- source representation;
- edge angular representation;
- receiver representation;
- invariant gates.

---

## 55. Example Tensor-Product Structure

A generic structure may be:

`m_ij = TP(h_j, B_ang(r_ij), w_ij)`.

Here:

- `TP` is an equivariant tensor-product operator;
- `B_ang` is an angular representation;
- `w_ij` contains invariant radial or learned scalar weights.

---

## 56. Receiver-State-Conditioned Message

The message may additionally depend on receiver state:

`m_ij = M(h_i, h_j, e_ij)`.

This permits directed adaptation without breaking equivariance when the operation is representation-compatible.

---

## 57. Source-State-Only Message

A simpler architecture may use:

`m_ij = M(h_j, e_ij)`.

The receiver state then enters only through aggregation or node update.

---

## 58. Pair-State Message

A pair representation may combine:

`h_i`

and:

`h_j`

before generating a message.

---

## 59. Relative Geometry in Message

Absolute positions should not enter a translation-invariant message arbitrarily.

Relative geometry:

`r_ij`

provides the natural translation-invariant/equivariant geometric input.

---

## 60. Distance Message

A distance-only message can remain rotationally invariant.

Such a message cannot encode full directional information by itself.

---

## 61. Directional Message

Directional dependence requires an equivariant angular representation.

---

## 62. Angular Message

A directional message may use:

`Y_lm(e_hat_ij)`.

The representation must transform under the appropriate:

`D^l(Q)`.

---

## 63. Radial-Angular Message

A message may combine:

`R_n(d_ij)`

and:

`Y_lm(e_hat_ij)`.

This separates radial and angular geometry.

---

## 64. Pair-Species Conditioning

Messages may depend on ordered species pair:

`(a_i, a_j)`.

This permits chemically differentiated interactions while preserving spatial symmetry.

---

## 65. Species-Pair Symmetry

A model may choose either:

- ordered species pairs;
- unordered species pairs.

The choice affects directed message semantics.

---

## 66. Message Parameter Sharing

The same message function may be shared across:

- all nodes;
- all edges;
- species classes;
- relation types.

Parameter sharing must preserve permutation semantics.

---

## 67. Species-Specific Parameters

A model may use species-dependent parameters.

The parameter lookup must depend on species identity rather than arbitrary node index.

---

## 68. Edge-Type-Specific Parameters

Different relation types may use different message maps:

`M_tau`.

The relation type:

`tau`

must remain explicit.

---

## 69. Multi-Relation Message Passing

For edge families:

`E^(1), ..., E^(M)`

the receiver may aggregate relation-specific messages separately before fusion.

---

## 70. Relation Fusion

A node update may use:

`m_i = F_rel(m_i^(1), ..., m_i^(M))`.

The fusion must preserve representation compatibility.

---

## 71. Scalar Fusion

Invariant scalar channels may be mixed through arbitrary learned scalar maps.

---

## 72. Equivariant Fusion

Equivariant channels require transformation-compatible fusion.

---

## 73. Message Normalization

Messages may be normalized by:

- degree;
- cutoff volume;
- learned invariant scale;
- representation norm.

The normalization must preserve equivariance.

---

## 74. Degree Normalization

A normalized sum may use:

`m_i = 1 / c_i sum_j m_ij`

with invariant scalar:

`c_i`.

---

## 75. Symmetric Degree Normalization

Graph-style normalization may use source and receiver degree factors.

These factors are scalar graph quantities.

---

## 76. Message Magnitude Control

A scalar gate may constrain message magnitude while preserving direction or representation type.

---

## 77. Message Clipping

Componentwise clipping of vector or tensor features may break equivariance.

Any clipping mechanism must be representation-aware.

---

## 78. Norm Clipping

A vector may be norm-clipped:

`v' = min(1, c/||v||) v`

for positive threshold:

`c`.

This preserves vector direction and equivariance.

---

## 79. Representation-Aware Regularization

Regularization may operate on invariant norms of irrep blocks.

---

## 80. Message Dropout

Randomly dropping complete representation channels or whole edge messages may preserve symmetry statistically if the mask is applied consistently across representation components.

The stochastic contract must remain explicit.

---

## 81. Componentwise Dropout

Independent dropout of vector Cartesian components can break rotational equivariance.

---

## 82. Edge Dropout

An edge may be stochastically removed during training.

The induced graph distribution must remain permutation-consistent.

---

## 83. Training versus Inference Graph

A model may use stochastic graph modifications during training and deterministic graph construction during inference.

The two modes must be explicit.

---

## 84. Deterministic Message Passing

For deterministic inference, identical:

- graph;
- node state;
- edge state;
- parameters;
- arithmetic semantics;
- aggregation order

must produce identical declared outputs.

---

## 85. Reduction Order

Floating-point summation depends on reduction order.

Canonical aggregation order may be required for byte-identical replay.

---

## 86. Parallel Aggregation

Parallel execution may change floating-point reduction order.

A reproducibility contract must define whether:

- byte-identical;
- exact categorical;
- tolerance-based numerical

comparison is required.

---

## 87. Message-Passing State Closure

If future results depend only on current node, edge, global state, graph, and parameters, the message-passing layer is Markov-complete with respect to those variables.

---

## 88. Hidden Message Memory

If a layer depends on previous hidden states beyond current representation, that memory must be explicit.

---

## 89. Recurrent Message Passing

A recurrent architecture may use:

`h_i[k+1] = U(h_i[k], m_i[k])`

over repeated internal iterations.

The recurrent index must remain distinct from physical time unless explicitly coupled.

---

## 90. Message Persistence

A retained message state may exist in recurrent architectures.

This is computational memory.

It is not ternary neutral residence.

---

## 91. Message-Passing Fixed Point

An iterative message-passing system may converge to:

`h_star`

satisfying:

`h_star = MP(h_star)`.

This is a representation fixed point.

It is not automatically a physical equilibrium.

---

## 92. Fixed Point versus Physical Equilibrium

The distinction is:

`message-passing fixed point ≠ atomic equilibrium`.

---

## 93. Fixed Point versus Resonance

Likewise:

`message-passing fixed point ≠ resonance`.

---

## 94. Locality

For a cutoff graph, one layer is local with respect to the graph neighborhood.

Multiple layers enlarge the computational receptive field.

---

## 95. Strict Locality

A strictly local model uses only graph-connected information within a finite depth.

---

## 96. Global State Injection

Adding global features to every node creates a nonlocal information path even when the graph is sparse.

---

## 97. Long-Range Messages

A model may use explicit long-range edges or separate nonlocal operators.

These must remain distinct from local graph messages.

---

## 98. Local and Nonlocal Fusion

A hybrid model may combine:

`m_i = m_i,local + m_i,nonlocal`

when both messages have compatible representation types.

---

## 99. Long-Range Electrostatic Boundary

Electrostatic interactions may require a dedicated long-range model.

A generic message-passing edge does not by identity represent electrostatic force or energy.

---

## 100. Message Passing and Periodicity

Periodic graphs use image-aware relative vectors.

Messages must therefore use the serialized periodic displacement:

`r_ij = r_j + H n_ij - r_i`.

---

## 101. Periodic Translation

Equivalent periodic images must produce equivalent message semantics under the periodic graph contract.

---

## 102. Cell Rotation

If positions and cell rotate together, periodic edge vectors rotate accordingly.

Message equivariance must remain preserved.

---

## 103. Cell Deformation

Cell deformation changes geometry.

The resulting message state may change physically and numerically.

This is not a rigid E(3) symmetry operation.

---

## 104. Message Passing under Atom Permutation

Permuting atomic labels permutes:

- node states;
- edge endpoints;
- edge features;
- incoming neighborhoods.

The resulting per-atom output must permute consistently.

---

## 105. Neighbor Ordering Independence

A message aggregation must not depend on arbitrary storage order of:

`N_i`.

---

## 106. Edge Ordering and Determinism

Although physical semantics are ordering-independent, deterministic floating-point execution may require canonical edge ordering.

---

## 107. Global Message Passing

A global node may be introduced as a computational structure.

If used, its transformation behavior must be explicit.

---

## 108. Virtual Node

A virtual node may aggregate system-wide scalar or equivariant information.

It is not an atomic particle unless explicitly modeled as such.

---

## 109. Virtual Node versus Physical Atom

The distinction remains:

`virtual node ≠ physical atom`.

---

## 110. Virtual Edge versus Physical Interaction

Likewise:

`virtual edge ≠ physical interaction by identity`.

---

## 111. Hierarchical Message Passing

Message passing may operate across:

- atom-to-atom;
- atom-to-cluster;
- cluster-to-cluster;
- cluster-to-atom

relations.

---

## 112. Atom-to-Cluster Message

A fine-scale representation may be pooled into a cluster representation through an equivariant aggregation.

---

## 113. Cluster-to-Atom Message

A coarse representation may provide feedback to fine-scale nodes.

The mapping must preserve spatial and permutation semantics.

---

## 114. Cross-Scale Message

A cross-scale message belongs to a declared source and destination representation space.

---

## 115. Cross-Scale Message versus Physical Force

A cross-scale feature transfer is not force by identity.

---

## 116. Multiscale Message State

A multiscale representation may contain:

`H_atom`

`H_cluster`

`H_global`.

Messages may connect these spaces explicitly.

---

## 117. Pooling

Pooling is an aggregation from a finer node set to a coarser representation.

---

## 118. Unpooling

Unpooling distributes coarse information to a finer node set.

It is generally not the inverse of pooling.

---

## 119. Information Loss

Pooling may be non-injective.

The complete fine-scale state cannot generally be reconstructed from pooled features alone.

---

## 120. Closure Variables

A multiscale message architecture may introduce closure features to encode effects not retained explicitly after pooling.

---

## 121. Resonance Parameterization Interface

Chapter 06 maps message-passed equivariant representations into resonance state:

`P_R: X_EQ^[L] → X_R`.

---

## 122. Local Resonance Input

For node:

`i`

the local resonance state may depend on:

`h_i^[L]`.

---

## 123. Edge Resonance Input

Edge representation:

`e_ij^[L]`

may contribute to pair or directional resonance descriptors.

---

## 124. Cluster Resonance Input

Cluster representations may produce cluster-level resonance coordinates.

---

## 125. Global Resonance Input

A pooled invariant or equivariant global representation may produce global resonance state.

---

## 126. Message Passing versus Resonance

The distinction remains:

`message passing ≠ resonance`.

Message passing produces representation state.

Resonance is produced by a separate parameterization.

---

## 127. Resonance Feedback into Message Passing

A later model may feed resonance state back into message computation:

`m_ij = M(h_i, h_j, e_ij, r_i, r_j)`.

This creates a coupled representation-resonance loop.

---

## 128. Feedback Ordering

If resonance feeds message passing, the update order must be explicit.

---

## 129. Same-Step Feedback

A simultaneous or implicit representation-resonance solve requires a separately defined joint update rule.

---

## 130. Previous-Step Resonance Feedback

A simpler recurrent model may use retained prior resonance state.

Then the resonance state belongs to message-passing memory.

---

## 131. Ternary Feature Interface

Chapter 07 may introduce ternary feature channels associated with:

- nodes;
- edges;
- clusters;
- global state.

---

## 132. Ternary-Gated Message

A specialization may use ternary feature:

`t_i ∈ {-1, 0, 1}`

to modulate a message.

The modulation rule must be explicit.

---

## 133. Ternary State as Scalar Gate

A scalar ternary value may multiply a compatible representation:

`m'_ij = t_i m_ij`.

This is a mathematical operation.

Its physical meaning depends on the model.

---

## 134. Active Neutral Gate

If:

`t_i = 0`

and direct multiplication is used:

`m'_ij = 0`.

This particular mapping produces a zero message.

It does not imply that active-neutral semantics universally mean zero message propagation.

---

## 135. Active Neutral Message Policy

A model may define a nonzero active-neutral message operator:

`M_0`.

Therefore:

`ternary 0 ≠ zero message by identity`.

---

## 136. Ternary-Conditioned Message Family

A message family may be:

`M_-1`

`M_0`

`M_1`.

The selected function depends on current ternary state.

---

## 137. Ternary Routing versus Message Routing

The distinction remains:

`neutral routing ≠ graph message routing`.

Neutral routing governs committed ternary transitions.

Message routing governs computational propagation over graph edges.

---

## 138. Pending Ternary State versus Message Queue

The distinction remains:

`pending ternary destination ≠ pending message`.

---

## 139. Ternary Target versus Message Output

A message may contribute to target generation through later mappings.

It is not a ternary target by identity.

---

## 140. Message-to-Target Chain

The canonical path is:

`message state`

`→ equivariant node state`

`→ resonance state`

`→ decision state`

`→ ternary target`.

---

## 141. Direct Message-to-Target Specialization

A specialization may define:

`P_MT: X_msg → {-1,0,1}`.

Such a map must preserve the target/execution boundary.

---

## 142. Message-to-Execution Prohibition

No message directly changes:

`t_exec`

without passing through the declared ternary execution contract.

---

## 143. Energy Interface

Chapter 08 consumes final node, edge, and global representations to produce an invariant scalar energy.

---

## 144. Local Energy Head

A local scalar head may produce:

`E_i = F_E(h_i)`.

The total may be:

`E = sum_i E_i`.

---

## 145. Edge Energy Head

An edge-based scalar head may contribute pair terms.

Counting conventions must be explicit.

---

## 146. Message State versus Energy

The distinction remains:

`message state ≠ energy`.

---

## 147. Force Interface

Force may be obtained from:

`F_i = -grad_(r_i) E`

for a conservative differentiable model.

Message passing affects force indirectly through the energy functional.

---

## 148. Direct Force Head

A message-passed equivariant representation may also feed a direct vector force head.

Such a model must separately define conservativity.

---

## 149. Message Vector versus Force Vector

Both may transform as vectors.

They remain semantically distinct.

---

## 150. Stress Interface

Stress may be derived from energy, cell deformation, virial relations, or another explicitly declared mechanical mapping.

Message state is upstream representation state.

---

## 151. Conservation Boundary

Equivariant message passing alone does not guarantee:

- energy conservation;
- momentum conservation;
- conservative force;
- stable molecular dynamics.

These properties require separate model structure.

---

## 152. Equivariance versus Conservation

The distinction remains:

`equivariance ≠ conservation`.

---

## 153. Permutation Symmetry versus Conservation

Permutation equivariance does not imply energy or momentum conservation.

---

## 154. Locality versus Conservation

Local message passing does not itself imply conservative interactions.

---

## 155. Message Reciprocity

A model may impose a relation between:

`m_ij`

and:

`m_ji`.

No universal reciprocity rule is imposed.

---

## 156. Message Reciprocity versus Newton Pair Force

Even if:

`m_ji = -m_ij`

for a vector message, this does not automatically establish a Newtonian pair force interpretation.

---

## 157. Symmetric Pair Message

A scalar pair message may satisfy:

`m_ij = m_ji`.

This is a representation symmetry.

---

## 158. Antisymmetric Pair Message

A vector pair message may satisfy:

`m_ji = -m_ij`.

This may be useful for selected constructions but is not universally required.

---

## 159. Receiver-State Asymmetry

Directed message passing may intentionally violate pair symmetry at the latent representation level.

Physical outputs may still preserve required invariants.

---

## 160. Extensive Output Scaling

If local node energy contributions are summed, energy can scale extensively with system size under appropriate locality assumptions.

---

## 161. Intensive Global Representation

A mean-pooled global state scales differently from a sum-pooled state.

The aggregation must match intended output semantics.

---

## 162. Message-Passing Stability

The boundedness or convergence of hidden message states is a computational dynamical property.

It is distinct from physical stability of the interatomic system.

---

## 163. Hidden-State Boundedness

A message representation may be norm-bounded through architecture or normalization.

This does not establish boundedness of atomic trajectories.

---

## 164. Message Amplification

Repeated layers may amplify feature norms.

Normalization, residual design, gating, or spectral constraints may control this behavior.

---

## 165. Oversmoothing

Repeated message aggregation may make node representations increasingly similar.

This is a representation phenomenon.

---

## 166. Oversmoothing versus Synchronization

The distinction is:

`graph representation oversmoothing ≠ oscillator synchronization`.

---

## 167. Oversmoothing versus Coherence

Likewise:

`representation similarity ≠ physical coherence`.

---

## 168. Oversquashing

Long-range graph information may be compressed through limited representation capacity.

This is an architecture limitation.

---

## 169. Oversquashing versus Information Conservation

Loss of representational information is not a physical conservation-law violation.

---

## 170. Message-Passing Expressivity

Expressivity depends on:

- graph structure;
- feature types;
- aggregation;
- tensor products;
- network depth;
- channel multiplicities;
- nonlinearities.

---

## 171. Expressivity versus Physical Validity

A more expressive message-passing model is not automatically more physically constrained.

Physical invariants remain separate requirements.

---

## 172. Message-Passing Complexity

For edge count:

`|E|`

message computation commonly scales with:

`|E|`

times representation-dependent cost.

---

## 173. Sparse Graph Complexity

For bounded average degree:

`d_bar`

the edge count is approximately:

`N d_bar`.

This can yield approximately linear node-count scaling in the graph layer under suitable conditions.

---

## 174. Dense Graph Complexity

A fully connected directed graph without self edges has:

`N(N-1)`

edges.

Message cost may therefore scale quadratically with system size.

---

## 175. Angular Complexity

Tensor-product message cost increases with:

- angular degree;
- multiplicity;
- number of coupling paths.

---

## 176. Radial Complexity

Increasing radial basis size increases scalar edge-feature dimension and message cost.

---

## 177. Layer Complexity

Total message cost grows with message-passing depth:

`L`.

---

## 178. Memory Cost

Memory may include:

- node states;
- edge states;
- messages;
- intermediate tensor products;
- gradients during training.

---

## 179. Streaming Message Computation

Messages may be computed and aggregated without storing every edge message simultaneously.

This is an implementation optimization.

---

## 180. Fused Message Aggregation

Message generation and aggregation may be fused.

The fused implementation must preserve the same mathematical semantics.

---

## 181. Implementation Fusion versus Semantic Fusion

Combining computational kernels does not remove the formal distinction between:

- message;
- aggregation;
- update.

---

## 182. Parallel Message Passing

Independent edge messages may be evaluated in parallel when no sequential dependency exists.

---

## 183. Atomic Reduction

Parallel aggregation may use atomic operations or segmented reductions.

The arithmetic ordering may influence finite-precision replay.

---

## 184. Deterministic Reduction

A deterministic implementation may use canonical segmented reduction order.

---

## 185. Hardware Representation

A hardware implementation may encode:

- graph indices;
- scalar features;
- vector features;
- fixed-point values;
- ternary channels.

Encoding does not alter the formal transformation semantics.

---

## 186. Fixed-Point Message Passing

Fixed-point message passing requires explicit:

- scaling;
- rounding;
- overflow;
- saturation;
- representation ranges.

---

## 187. Fixed-Point Equivariance Residual

Quantization may introduce nonzero numerical equivariance residuals.

These must be measured under the declared numerical contract.

---

## 188. Message Quantization

Quantizing a message feature is numerical compression.

It is not balanced ternary semantic mapping unless explicitly mapped into:

`-1/0/1`.

---

## 189. Message Serialization

A message-passing trace may contain:

- layer index;
- source node;
- receiver node;
- edge type;
- representation type;
- message norm;
- selected message components;
- aggregate state;
- node update state.

---

## 190. Trace Scope

A full message trace may be large.

Reduced traces may store derived observables rather than all hidden channels.

---

## 191. Message Trace versus Restart State

A diagnostic message trace need not contain enough information for restart.

Restart state and observability state remain distinct.

---

## 192. Deterministic Replay State

A message-passing replay requires:

- graph;
- node features;
- edge features;
- global state;
- model parameters;
- canonical ordering;
- arithmetic semantics.

---

## 193. Layerwise Replay

Each message-passing layer may be replayed and compared independently.

---

## 194. End-to-End Replay

The entire:

`graph → message passing → representation`

chain may be replayed as one deterministic artifact.

---

## 195. Message Validation

A message validator may check:

- source/receiver convention;
- feature dimensions;
- representation types;
- finite values;
- symmetry transformation;
- permutation behavior;
- deterministic aggregation.

---

## 196. Source/Receiver Validation

For every directed edge:

`j → i`

the message must use the declared source and receiver positions and features consistently.

---

## 197. Edge-Reversal Validation

Controlled reverse edges may verify sign and ordered-feature behavior.

---

## 198. Scalar Equivariance Test

For scalar message:

`m_ij(gX) = m_ij(X)`

under the relevant mapped edge.

---

## 199. Vector Equivariance Test

For vector message:

`m_ij(gX) = Q m_ij(X)`.

---

## 200. Higher-Irrep Validation

For representation:

`l`

the transformed message must match the corresponding:

`D^l(Q)`

action.

---

## 201. Parity Validation

For:

`O(3)`

models, reflection or inversion tests verify parity behavior.

---

## 202. Permutation Validation

After atom permutation:

- edge indices permute;
- messages permute;
- receiver aggregates permute;
- node outputs permute.

---

## 203. Neighbor-Order Validation

Randomizing neighbor-list storage order must not change the mathematical aggregated result beyond the declared finite-precision comparison relation.

---

## 204. Translation Validation

For translation-invariant graph geometry, global translation must not alter messages except for channels whose transformation law explicitly includes the translated quantity.

---

## 205. Rotation Validation

Rotate all positions and transform all external geometric states consistently.

Message outputs must satisfy the declared equivariance relation.

---

## 206. Combined Symmetry Validation

A strong test may combine:

- atom permutation;
- translation;
- rotation;
- reflection where applicable.

---

## 207. Empty-Neighborhood Validation

A fixture with isolated nodes must verify the declared empty-neighborhood policy.

---

## 208. Periodic Validation

Equivalent periodic images must produce equivalent messages.

---

## 209. Graph-Cutoff Validation

Configurations near graph cutoffs must distinguish:

- graph topology differences;
- message-function differences.

---

## 210. Numerical Validation

Validation should test:

- finite values;
- overflow behavior;
- equivariance residuals;
- deterministic replay;
- reduction consistency.

---

## 211. NaN Handling

A message containing:

`NaN`

is invalid numerical state.

It must not silently become ternary:

`0`.

---

## 212. Infinity Handling

Non-finite message values require explicit handling.

---

## 213. Masked Message

A masked message may be excluded from aggregation.

A binary mask value:

`0`

does not mean active-neutral ternary state.

---

## 214. Padding

Batching may use padded nodes or edges.

Padding must be excluded through explicit masks.

---

## 215. Padding versus Physical Node

A padded graph entry is not a physical atom.

---

## 216. Padding versus Neutral State

The distinction remains:

`padding zero ≠ ternary neutral 0`.

---

## 217. Batched Graph

Several independent graphs may be represented in one batch.

No message may cross graph boundaries unless explicitly defined.

---

## 218. Batch Index

A batch identifier is computational metadata.

It is not a physical state.

---

## 219. Batch Permutation

Reordering independent graphs within a batch must not change per-graph outputs.

---

## 220. Global Aggregation by Graph

Global pooling must respect graph membership within batched representations.

---

## 221. Message Provenance

Message-passing structures may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 222. Primary-Source Message Architecture

Established equivariant message-passing constructions retain applicable:

`PRIMARY_SOURCE`

provenance.

---

## 223. Author-Defined TR-EIF Message Integration

TR-EIF-specific integration of:

- equivariant messages;
- resonance parameterization;
- ternary channels;
- active-neutral execution interfaces

carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 224. Derived Message Feature

A message analytically derived from geometric features may carry:

`DERIVED`

provenance.

---

## 225. Calibrated Message Parameter

Cutoff scales, radial parameters, normalization factors, or other fitted values carry:

`CALIBRATED`

provenance where applicable.

---

## 226. Benchmark Message Result

Measured:

- throughput;
- memory;
- scaling;
- equivariance residual;
- replay behavior

may carry:

`BENCHMARK`

provenance.

---

## 227. Message Test Fixture

Synthetic graphs and transformed configurations used for message tests carry:

`TEST_FIXTURE`

provenance.

---

## 228. Message-Passing Extension Rule

Any new message-passing layer must define:

1. source state;
2. receiver state;
3. edge state;
4. message output type;
5. aggregation;
6. node update;
7. edge update where present;
8. global-state handling;
9. spatial transformation law;
10. permutation behavior;
11. numerical semantics;
12. validation.

---

## 229. Attention Extension Rule

Any attention mechanism must define:

1. score space;
2. score transformation law;
3. normalization domain;
4. source/receiver convention;
5. masking;
6. symmetry behavior;
7. deterministic tie or ordering behavior where applicable.

---

## 230. Dynamic-Edge Extension Rule

Any layer that changes edge features or topology must define:

1. update rule;
2. graph-state dependency;
3. geometry dependency;
4. symmetry behavior;
5. event ordering;
6. restart state.

---

## 231. Recurrent Message-Passing Extension Rule

Any recurrent message architecture must define:

1. recurrent state;
2. iteration coordinate;
3. initialization;
4. termination;
5. convergence criterion where used;
6. restart semantics.

---

## 232. Multiscale Message Extension Rule

Any cross-scale message system must define:

1. source scale;
2. destination scale;
3. pooling or mapping;
4. representation transformation law;
5. permutation handling;
6. information loss;
7. feedback semantics.

---

## 233. Ternary-Conditioned Message Extension Rule

Any ternary-conditioned message mechanism must define:

1. source ternary variable;
2. whether target or executed state is used;
3. `-1` message semantics;
4. `0` message semantics;
5. `1` message semantics;
6. update ordering;
7. feedback path;
8. separation from ternary commit.

---

## 234. Canonical Message-Passing Invariants

Every conforming message-passing layer preserves:

1. explicit source/receiver orientation;

2. explicit graph neighborhood;

3. explicit message function;

4. permutation-safe aggregation;

5. explicit representation type;

6. spatial equivariance;

7. explicit node update;

8. deterministic ordering where required.

---

## 235. Canonical Equivariance Invariants

For a declared group action:

`message transformed input`

must equal:

`transformed message output`

under the applicable representation.

Aggregation of compatible channels preserves their representation type.

---

## 236. Canonical Permutation Invariants

Atom relabeling produces corresponding relabeling of:

- node state;
- edge state;
- messages;
- aggregates;
- updated node state.

Global scalar outputs remain invariant.

---

## 237. Canonical Type-Separation Invariants

The framework preserves:

`message ≠ edge`

`message ≠ force`

`message ≠ energy`

`message ≠ chemical bond`

`message ≠ resonance`

`message ≠ ternary target`

`message ≠ executed ternary state`

`message queue ≠ pending ternary route`

`message layer ≠ physical time`.

---

## 238. Canonical Ternary Invariants

Any ternary-conditioned message layer preserves the exact balanced ternary set:

`-1/0/1`.

The state:

`0`

remains active neutral.

A representation zero, edge mask zero, padding zero, or zero-valued message is not automatically ternary neutral.

---

## 239. Canonical TR Execution Boundary

Message passing may influence:

`t_target`

only through an explicit downstream mapping.

Committed execution remains governed by:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

No graph message may bypass the neutral-mediated execution layer.

---

## 240. Canonical Scientific Distinctions

The message-passing layer preserves:

`message passing ≠ phase coupling`

`message passing ≠ mechanical force`

`message passing ≠ physical energy transfer`

`interaction edge ≠ chemical bond`

`message fixed point ≠ physical equilibrium`

`oversmoothing ≠ synchronization`

`representation similarity ≠ coherence`

`equivariance ≠ conservation`

`message vector ≠ force vector`

`zero message ≠ active-neutral state`

`graph routing ≠ neutral routing`.

---

## 241. Canonical Message Chain

The local message chain is:

`source node state`

`+ receiver node state`

`+ edge geometry`

`→ equivariant message`

`→ permutation-safe aggregation`

`→ equivariant receiver update`.

---

## 242. Canonical Representation Chain

Across layers:

`X_EQ^[0]`

`→ MP^[0]`

`→ X_EQ^[1]`

`→ ...`

`→ MP^[L-1]`

`→ X_EQ^[L]`.

---

## 243. Canonical Resonance Interface

The final message-passed representation becomes input to:

`P_R`.

The chain is:

`message-passed equivariant representation`

`→ resonance parameterization`

`→ resonance state`.

---

## 244. Canonical Ternary Interface

The broader chain is:

`X_EQ`

`→ X_R`

`→ T_target`

`→ neutral-mediated execution`.

---

## 245. Canonical Energy Interface

The energy chain is:

`message-passed representation`

`→ invariant scalar energy head`

`→ energy`.

---

## 246. Canonical Force Interface

For a conservative model:

`message-passed representation`

`→ invariant energy`

`→ coordinate derivative`

`→ equivariant force`.

---

## 247. Canonical Stress Interface

Stress is produced through the explicitly defined energy/cell or mechanical output mapping.

Message state remains upstream computational representation.

---

## 248. Interface to Chapter 06

Chapter 06 develops Resonance Parameterization.

It defines how message-passed equivariant features become:

- local resonance coordinates;
- edge resonance coordinates;
- cluster resonance coordinates;
- global resonance coordinates;
- resonance windows;
- resonance-control parameters.

The distinction remains:

`equivariant representation ≠ resonance state`.

---

## 249. Interface to Chapter 07

Chapter 07 develops Ternary Feature Channels.

It defines mappings from selected invariant or transformation-compatible message/resonance features into exact:

`-1/0/1`

channels.

---

## 250. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

The energy model consumes the final message-passed representation together with explicitly declared resonance and ternary features where included.

---

## 251. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

It uses invariant energy or direct equivariant output mappings while preserving the geometric transformation contract.

---

## 252. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each model-family member must declare:

- graph type;
- message depth;
- message representations;
- aggregation;
- radial/angular basis;
- tensor-product paths;
- recurrence where used;
- global-state coupling;
- resonance interface;
- ternary-conditioning interface.

---

## 253. Final Formal Structure

The message-passing layer may be represented as:

`MP = (X_node, X_edge, X_global, X_msg, M, A, U_N, U_E, U_G, rho_MP)`.

Here:

- `X_node` is node-representation state;
- `X_edge` is edge-representation state;
- `X_global` is optional global state;
- `X_msg` is message state;
- `M` is the directed message function;
- `A` is neighbor aggregation;
- `U_N` is node update;
- `U_E` is optional edge update;
- `U_G` is optional global update;
- `rho_MP` is the declared spatial and permutation transformation action.

For edge:

`j → i`:

`m_ij = M(h_i, h_j, e_ij, g)`.

For receiver:

`i`:

`m_i = A({m_ij | j ∈ N_i})`.

Then:

`h_i' = U_N(h_i, m_i, g)`.

---

## 254. Final Statement

Message passing propagates equivariant information across the interaction graph without collapsing the distinction between computational representation and physical state.

Each directed edge:

`j → i`

produces a receiver-oriented message from explicitly typed source, receiver, and edge representations.

Incoming messages are aggregated through permutation-safe operations.

Node, edge, and global updates preserve the declared E(3), O(3), SO(3), SE(3), parity, and permutation structure of their channels.

Message passing may be:

- local;
- nonlocal;
- multirelational;
- recurrent;
- multiscale;
- resonance-conditioned;
- ternary-conditioned.

The framework preserves:

`message ≠ edge`

`message ≠ force`

`message ≠ energy`

`message ≠ chemical bond`

`message passing ≠ phase coupling`

`message ≠ resonance`

`message ≠ ternary state`

`zero message ≠ active-neutral 0`

`graph routing ≠ neutral routing`.

The canonical integration path remains:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

These definitions establish the propagation layer required for the Resonance Parameterization developed in Chapter 06.
