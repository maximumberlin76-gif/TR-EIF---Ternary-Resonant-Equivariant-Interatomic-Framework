# Message Passing

## 1. Purpose

This chapter defines the message-passing layer of the TR-EIF equivariant interatomic framework.

Message passing provides a structured mapping between local interatomic environments and updated entity representations while preserving the declared geometric, permutation, species, and representation-type constraints.

The layer operates on an interaction graph and defines:

- node states;
- edge states;
- neighborhood relations;
- message functions;
- aggregation operators;
- update functions;
- representation types;
- geometric dependencies;
- resonance-conditioned channels;
- multilevel propagation;
- output interfaces.

---

## 2. Dependencies

This chapter depends on:

- Volume 01 — Mathematical Foundations;
- Volume 02 — Ternary Resonance Theory;
- Volume 03 Chapter 01 — Interatomic State Space;
- Volume 03 Chapter 02 — Symmetry Groups;
- Volume 03 Chapter 03 — Invariant Representations;
- Volume 03 Chapter 04 — Equivariant Representations.

---

## 3. Interaction Graph

An interatomic configuration is represented by a graph:

`G = (V, E)`.

Here:

- `V` is the set of entities or atomic sites;
- `E` is the set of declared interaction edges.

An entity is indexed by:

`i ∈ V`.

A directed interaction edge is written:

`(i,j) ∈ E`.

---

## 4. Node State

The state associated with entity:

`i`

at message-passing layer:

`k`

is written:

`h_i^[k]`.

The initial state:

`h_i^[0]`

is constructed from declared input features.

---

## 5. Initial Node Features

Initial node features may contain:

- species identity;
- invariant scalar descriptors;
- equivariant descriptors;
- explicitly defined local state variables;
- externally supplied attributes.

Every component must have a declared semantic and transformation type.

---

## 6. Species Representation

Let:

`Z_i`

denote the species or entity type of node:

`i`.

A species embedding may be written:

`e_Z(Z_i)`.

Species identity is not inferred from spatial coordinates.

---

## 7. Position Variables

Let:

`R_i ∈ R^3`

denote the Cartesian position of entity:

`i`.

Absolute position is not required to be an invariant local descriptor.

Relative geometry is constructed from pairs of positions.

---

## 8. Relative Displacement

For an edge:

`(i,j)`

define:

`R_ij = R_j - R_i`.

Under global translation:

`R_i → R_i + a`

the relative displacement remains unchanged.

---

## 9. Pair Distance

The pair distance is:

`d_ij = ||R_ij||`.

It is invariant under rigid translation and orthogonal spatial transformations.

---

## 10. Relative Direction

For:

`d_ij > 0`

define:

`u_ij = R_ij / d_ij`.

The relative direction transforms equivariantly under rotation.

Behavior for zero or unresolved separation must be explicitly defined by the implementation.

---

## 11. Neighborhood

The neighborhood of node:

`i`

is:

`N(i) = {j | (i,j) ∈ E}`.

The construction of:

`N(i)`

is part of the interaction-topology definition.

---

## 12. Cutoff Neighborhood

A distance-based neighborhood may be defined by:

`d_ij ≤ r_cut`.

Here:

`r_cut`

is the declared interaction cutoff.

---

## 13. Cutoff Function

A cutoff function may be written:

`c(d_ij)`.

Its support, smoothness, boundary behavior, and parameter values must be explicit.

---

## 14. Edge State

The edge representation at layer:

`k`

is written:

`e_ij^[k]`.

It may depend on:

- pair distance;
- relative direction;
- species pair;
- invariant radial basis;
- angular basis;
- resonance variables;
- other explicitly defined pair quantities.

---

## 15. Message Function

The message from node:

`j`

to node:

`i`

at layer:

`k`

is:

`m_ij^[k] = M_k(h_i^[k], h_j^[k], e_ij^[k])`.

The message function:

`M_k`

must preserve the declared representation structure.

---

## 16. Incoming Message Set

The incoming message set for node:

`i`

is:

`{m_ij^[k] | j ∈ N(i)}`.

Neighbor ordering must not change the physical result when the graph semantics are permutation invariant.

---

## 17. Aggregation

The aggregated message is:

`m_i^[k] = A_k({m_ij^[k] | j ∈ N(i)})`.

The aggregation operator:

`A_k`

must have an explicitly defined permutation behavior.

---

## 18. Permutation-Invariant Aggregation

For ordinary unordered neighborhoods, admissible aggregation operators may include:

- sum;
- mean;
- another explicitly permutation-invariant reduction.

The selected operator is part of the model definition.

---

## 19. Sum Aggregation

A sum aggregation is:

`m_i^[k] = sum_(j ∈ N(i)) m_ij^[k]`.

The output representation type is determined by the message representation.

---

## 20. Mean Aggregation

A mean aggregation is:

`m_i^[k] = (1 / |N(i)|) sum_(j ∈ N(i)) m_ij^[k]`

for:

`|N(i)| > 0`.

Behavior for an empty neighborhood must be explicitly defined.

---

## 21. Node Update

The node state is updated through:

`h_i^[k+1] = U_k(h_i^[k], m_i^[k])`.

The update function:

`U_k`

must map compatible representation types to the declared output representation.

---

## 22. Residual Update

A residual update may take the form:

`h_i^[k+1] = h_i^[k] + Delta h_i^[k]`

when both terms have compatible representation types.

---

## 23. Representation Typing

Every message-passing feature must be assigned a declared transformation type.

Possible types include:

- invariant scalar;
- polar vector;
- axial vector;
- higher-order tensor;
- irreducible representation;
- categorical state;
- explicitly typed auxiliary variable.

---

## 24. Scalar Channels

Invariant scalar channels remain unchanged under the declared spatial group action.

Examples include:

- pair distance;
- scalar radial features;
- scalar species embeddings;
- scalar resonance coordinates where defined as invariant.

---

## 25. Vector Channels

Vector channels transform according to the declared vector representation.

A polar vector:

`v`

transforms under rotation:

`Q`

as:

`v → Qv`.

---

## 26. Tensor Channels

Tensor channels transform according to their declared tensor representation.

For a second-order tensor:

`T`

a standard rotational transformation is:

`T → Q T Q^T`.

---

## 27. Irreducible Representation Channels

For rotation-equivariant architectures, latent features may be decomposed into irreducible representation channels.

A channel may be indexed by:

`l`

and, where reflections are included, by parity.

---

## 28. Scalar Irreducible Representation

The:

`l = 0`

representation is rotationally invariant.

---

## 29. Non-Scalar Irreducible Representations

Representations with:

`l > 0`

transform nontrivially under rotation.

Their components must not be treated as independent invariant scalars.

---

## 30. Equivariant Message Mapping

For a group element:

`g`

an equivariant message function satisfies the declared relation:

`M_k(rho(g)x) = rho_M(g) M_k(x)`

for the relevant combined message input:

`x`.

---

## 31. Equivariant Node Update

The update function must satisfy the corresponding representation relation:

`U_k(rho_H(g)h, rho_M(g)m) = rho_H'(g) U_k(h,m)`.

---

## 32. Translation Behavior

Message functions based only on relative geometry and translation-invariant attributes may preserve global translation invariance.

Absolute-coordinate dependence must be explicitly declared if introduced.

---

## 33. Rotation Behavior

Directional inputs must transform consistently with the declared rotation group.

Scalar outputs derived from directional inputs require invariant contractions or another explicitly invariant construction.

---

## 34. Reflection Behavior

If the declared symmetry group includes reflections, parity behavior must be specified.

Polar vectors, axial vectors, scalars, pseudoscalars, and higher-order representations must not be conflated.

---

## 35. Permutation Equivariance

Let:

`pi`

be an admissible species-preserving permutation.

Per-node states satisfy:

`h_i → h_pi(i)`.

A conforming message-passing layer preserves the corresponding node reindexing.

---

## 36. Species-Preserving Permutation

Permutation symmetry applies to relabeling that preserves the association between entity identity, species, position, and all attached state variables.

---

## 37. Edge Permutation

Under node permutation:

`pi`

the edge:

`(i,j)`

maps to:

`(pi(i), pi(j))`.

Edge features must follow the same reindexing.

---

## 38. Graph Topology under Permutation

An admissible permutation changes labels, not the physical interaction topology represented by the graph.

---

## 39. Radial Features

A radial feature may be constructed as:

`phi_n(d_ij)`.

The basis family, index range, cutoff behavior, and normalization must be explicit.

---

## 40. Angular Features

Angular information may be constructed from relative directions or equivariant angular bases.

Its transformation law must be defined under the selected spatial symmetry group.

---

## 41. Radial-Angular Combination

A message may combine radial and angular information through an explicitly typed mapping.

The resulting representation type must be known.

---

## 42. Tensor Products

Equivariant message passing may combine representations using tensor products.

The output must be decomposed into the declared representation channels.

---

## 43. Invariant Contraction

An invariant scalar may be produced by a valid contraction of equivariant quantities.

The contraction rule is part of the model definition.

---

## 44. Scalar Gating

An invariant scalar gate may modulate an equivariant feature.

If:

`a_ij`

is invariant and:

`v_ij`

is equivariant, then:

`a_ij v_ij`

retains the representation type of:

`v_ij`.

---

## 45. Nonlinear Operations

Nonlinear operations must preserve the declared transformation structure.

Ordinary pointwise nonlinearities may act directly on invariant scalar channels.

Non-scalar channels require representation-compatible nonlinear mappings.

---

## 46. Normalization

Normalization must preserve representation type.

A normalization operation that mixes incompatible representation components violates the declared typing contract.

---

## 47. Attention Weight

An attention weight:

`a_ij`

may be used when its transformation behavior is explicit.

An invariant scalar attention weight may multiply an equivariant value without changing the value's spatial representation.

---

## 48. Attention Aggregation

Attention-based aggregation must remain permutation compatible with respect to neighbor ordering.

---

## 49. Local Environment

The local environment of node:

`i`

may be represented as:

`E_i = {Z_j, R_ij, e_ij | j ∈ N(i)}`.

Its exact field set is model-specific.

---

## 50. Locality

A finite-cutoff message-passing layer propagates information through the graph over a finite number of interaction steps.

After:

`K`

layers, information may propagate through graph paths of up to:

`K`

message-passing steps, subject to the architecture.

---

## 51. Message-Passing Depth

Let:

`K_MP`

denote the number of message-passing layers.

This is an architectural parameter.

It is not a physical time variable.

---

## 52. Message-Passing Layer Is Not Time Step

The framework preserves:

`message-passing layer ≠ physical time step`.

---

## 53. Message-Passing Depth Is Not Interaction Range by Identity

The framework preserves:

`network depth ≠ physical interaction range`.

Any relation between them requires an explicit model definition.

---

## 54. Receptive Field

The graph receptive field is determined by:

- graph topology;
- cutoff rule;
- message-passing depth;
- any long-range communication mechanism.

---

## 55. Long-Range Interaction Channel

If long-range interactions are included, they must be represented through an explicit additional mechanism.

A local cutoff graph alone does not define an unbounded interaction channel.

---

## 56. Edge Direction

For a directed graph, messages:

`m_ij`

and:

`m_ji`

are separate quantities unless the model explicitly constrains them.

---

## 57. Pair Symmetry

A pair function may possess exchange symmetry or antisymmetry where explicitly defined.

This property is not inferred solely from the existence of an undirected physical pair.

---

## 58. Self-Edges

If self-edges:

`(i,i)`

are used, their semantics must be explicit.

They are not ordinary interatomic displacement edges because:

`R_ii = 0`.

---

## 59. Empty Neighborhood

For:

`N(i) = empty`

the aggregation and update behavior must be explicitly defined.

---

## 60. Duplicate Edges

Duplicate graph edges must either be prohibited or assigned explicit multiplicity semantics.

---

## 61. Periodic Systems

For periodic systems, relative displacement must use the declared periodic-image convention.

The graph representation must remain consistent under equivalent periodic representations.

---

## 62. Periodic Image Index

An edge may carry a periodic image index:

`n_ij`.

Then a displacement may be written using the cell matrix:

`H`

as:

`R_ij = R_j + H n_ij - R_i`.

---

## 63. Periodic Equivalence

Equivalent periodic-image choices representing the same physical neighbor relation must produce consistent model behavior under the declared convention.

---

## 64. Cell Transformation

If the simulation cell transforms under rotation:

`H → QH`.

Periodic geometric features must transform consistently.

---

## 65. Resonance-Conditioned Message Passing

A message function may depend on resonance information:

`m_ij^[k] = M_k(h_i^[k], h_j^[k], e_ij^[k], r_ij^[k])`.

Here:

`r_ij^[k]`

is an explicitly defined resonance variable or representation.

---

## 66. Resonance State Space

A resonance quantity belongs to a declared resonance state space:

`r ∈ X_R`.

Its inclusion in message passing does not change its semantic type.

---

## 67. Scalar Resonance Conditioning

If a resonance variable is an invariant scalar, it may condition scalar coefficients or gates without introducing spatial orientation.

---

## 68. Equivariant Resonance Conditioning

If a resonance variable is vectorial or tensorial, the message function must preserve its declared transformation law.

---

## 69. Resonance Window

A resonance window remains:

`W_R ⊂ X_R`.

Its boundary remains:

`∂W_R`.

---

## 70. Resonance Classification

The classes:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

describe relation to a declared resonance window.

They are not message-passing representation types by identity.

---

## 71. Resonance Class Encoding

If resonance class is supplied to a message function, its encoding must be explicit.

The encoding must not silently identify resonance class with the ternary state space.

---

## 72. Resonance and Ternary Separation

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

---

## 73. Ternary Node State

A node may carry a semantic ternary state:

`t_i ∈ {-1,0,1}`.

This state is distinct from continuous latent features.

---

## 74. Active Neutral

The state:

`0`

is active neutral.

It is not:

- missing data;
- padding;
- invalid state;
- unknown value;
- uncertainty flag.

---

## 75. Ternary State as Message Input

If:

`t_i`

is supplied to a message function, it acts through an explicitly defined semantic encoding.

The numerical values:

`-1`

`0`

`1`

must not be interpreted as spatial vector components.

---

## 76. Ternary State and Rotation

For a scalar semantic ternary variable, spatial rotation does not exchange:

`-1`

and:

`1`.

---

## 77. Ternary State and Reflection

Spatial reflection does not automatically exchange:

`-1`

and:

`1`.

Any polarity-reversal operation must be separately defined.

---

## 78. Ternary Target

A message-passing network may produce or contribute to a target:

`t_target`.

The target is not automatically the executed retained state.

---

## 79. Executed Ternary State

The executed state:

`t_exec`

is determined by the declared ternary execution semantics.

---

## 80. Pending State

Where opposite-polarity routing is used, a pending destination:

`t_pending`

remains distinct from active neutral.

---

## 81. Ternary Role Separation

The framework preserves:

`t_target ≠ t_pending`

`t_pending ≠ t_exec`

`t_target ≠ t_exec`.

---

## 82. Ternary Transition Graph

The committed semantic transition graph remains:

`-1 ↔ 0 ↔ 1`.

---

## 83. Forbidden Direct Opposite Transitions

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

are forbidden.

---

## 84. Neutral-Mediated Routes

Opposite-polarity execution uses:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each leg is a separate committed event.

---

## 85. Message Prediction Is Not Transition Execution

A message-passing output proposing a new ternary target does not itself constitute a committed ternary transition.

---

## 86. Latent State Is Not Ternary State

The framework preserves:

`latent representation ≠ semantic ternary state`.

---

## 87. Resonance State Is Not Ternary State

The framework preserves:

`resonance state ≠ ternary state`.

A mapping between them must be explicit.

---

## 88. Energy Readout

A global or local energy readout may be constructed from invariant node representations.

For example:

`E = sum_i E_i`.

Each:

`E_i`

must have the declared scalar transformation behavior.

---

## 89. Local Energy Readout

A local scalar energy contribution may be written:

`E_i = U_E,k(h_i^[K_MP])`.

The mapping:

`U_E,k`

must produce an invariant scalar under the declared symmetry group.

---

## 90. Force Interface

If force is obtained from energy:

`F_i = -grad_(R_i) E`.

This relation belongs to the declared energy-force interface.

---

## 91. Direct Force Readout

If force is predicted directly from latent features, the force readout must produce a polar-vector equivariant output.

---

## 92. Energy and Force Distinction

The framework preserves:

`energy ≠ force`.

Message passing may contribute to both outputs without identifying them.

---

## 93. Stress Interface

A stress readout must produce the declared second-order tensor representation.

Its sign, normalization, and cell convention must be explicit.

---

## 94. Message Passing and Mechanical Force

The framework preserves:

`message ≠ mechanical force`.

A learned message is an internal computational quantity unless an explicit physical mapping defines another role.

---

## 95. Message Passing and Chemical Bond

The framework preserves:

`graph edge ≠ chemical bond`.

An interaction edge represents a computational or model interaction relation under the declared graph construction.

---

## 96. Message Passing and Phase Coupling

The framework preserves:

`message ≠ phase coupling`

unless an explicit mapping identifies a message component with a defined phase-coupling quantity.

---

## 97. Phase Relation and Chemical Bond

The framework preserves:

`phase relation ≠ chemical bond`.

---

## 98. Multiscale Message Passing

Message passing may be defined at multiple scales.

Let:

`ell`

index scale.

A scale-specific node state may be:

`h_i^(ell)`.

---

## 99. Cross-Scale Mapping

A mapping between scales may be written:

`P^(ell→m)`.

The mapping must specify:

- source scale;
- target scale;
- representation type;
- aggregation or projection;
- normalization.

---

## 100. Scale Consistency

Cross-scale message passing must preserve the declared semantic and symmetry types of transferred quantities.

---

## 101. Scale Is Not Time

The framework preserves:

`scale index ≠ physical time`.

---

## 102. Scale Is Not Ternary State

The framework preserves:

`scale index ≠ ternary state`.

---

## 103. Scale Is Not Resonance Class

The framework preserves:

`scale index ≠ resonance class`.

---

## 104. Message-Passing Recurrence

If parameters are shared across layers, the recurrence must be explicit.

Parameter sharing does not make layer index a physical time coordinate.

---

## 105. State Persistence

If a latent state persists across physical simulation steps, the persistence mechanism must be explicitly defined outside ordinary within-evaluation message-passing depth.

---

## 106. Memory Channel

A persistent memory channel requires an explicit state variable and update rule.

It must not be inferred from repeated message-passing layers alone.

---

## 107. Deterministic Message Passing

For fixed:

- graph;
- input state;
- parameters;
- arithmetic;
- execution order;

a deterministic implementation produces a reproducible output under its declared execution contract.

---

## 108. Determinism and Equivariance

The framework preserves:

`determinism ≠ equivariance`.

---

## 109. Determinism and Accuracy

The framework preserves:

`determinism ≠ predictive accuracy`.

---

## 110. Equivariance and Accuracy

The framework preserves:

`equivariance ≠ predictive accuracy`.

---

## 111. Numerical Precision

Message passing may be implemented using:

- floating-point arithmetic;
- mixed precision;
- fixed-point arithmetic;
- quantized arithmetic.

The arithmetic contract must be explicit.

---

## 112. Reduction Order

Floating-point aggregation may depend numerically on reduction order.

Permutation-equivariance validation must account for the declared arithmetic tolerance.

---

## 113. Exact Mathematical Symmetry and Numerical Residual

Finite numerical residual does not redefine the exact mathematical symmetry relation.

---

## 114. Quantization

Quantized message-passing implementations must define:

- scale;
- zero point where applicable;
- rounding;
- saturation;
- accumulator width;
- output conversion.

---

## 115. Reserved Numerical Codes

Storage-level reserved values must remain separate from semantic ternary states.

---

## 116. Missing Node Data

Missing node data require an explicit validity or mask channel.

They must not be encoded as ternary:

`0`.

---

## 117. Missing Edge Data

Missing edge data require an explicit validity representation.

An absent edge and an edge with a zero-valued feature are not identical by default.

---

## 118. Padding

Padding nodes or edges used for batching must be excluded through explicit masks or equivalent structural handling.

---

## 119. Empty Graph

Behavior for an empty graph must be explicitly defined if the implementation permits one.

---

## 120. Isolated Node

Behavior for an isolated node must be defined through the empty-neighborhood aggregation contract.

---

## 121. Duplicate Entity Identity

Each graph entity must have an unambiguous identity within the represented configuration.

---

## 122. Graph Construction Provenance

Graph-construction parameters must carry explicit provenance.

These may include:

- cutoff;
- neighbor count;
- periodic-image convention;
- species filters;
- long-range edge rules.

---

## 123. Canonical Provenance Classes

The message-passing layer uses:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 124. Primary-Source Construction

An externally defined message-passing or representation method uses:

`PRIMARY_SOURCE`

for the sourced definition.

---

## 125. Derived Quantity

A feature derived from previously defined TR-EIF variables may use:

`DERIVED`.

---

## 126. Author-Defined Mapping

A TR-EIF-specific message, update, aggregation, or resonance-conditioning rule may use:

`AUTHOR_DEFINED`.

---

## 127. Calibrated Parameter

A cutoff, width, threshold, or other parameter selected through an explicit calibration procedure uses:

`CALIBRATED`.

---

## 128. Benchmark Result

Measured message-passing performance or numerical residual under a benchmark protocol uses:

`BENCHMARK`.

---

## 129. Test Fixture

Synthetic graph structures used for verification use:

`TEST_FIXTURE`.

---

## 130. Requires Source

An external architectural or physical claim without established support uses:

`REQUIRES_SOURCE`.

---

## 131. Requires Test

An implementation-level property without validation uses:

`REQUIRES_TEST`.

---

## 132. Message Function Extension Rule

Any new message function must define:

1. input node representations;

2. input edge representations;

3. geometric inputs;

4. resonance inputs where used;

5. ternary inputs where used;

6. output representation;

7. symmetry behavior;

8. units where applicable;

9. provenance;

10. validation.

---

## 133. Aggregation Extension Rule

Any new aggregation operator must define:

1. input set;

2. permutation behavior;

3. normalization;

4. empty-neighborhood behavior;

5. output representation;

6. numerical reduction rule;

7. validation.

---

## 134. Update Function Extension Rule

Any new node update must define:

1. previous node representation;

2. aggregated message representation;

3. output representation;

4. residual structure where used;

5. nonlinear operations;

6. normalization;

7. symmetry behavior;

8. validation.

---

## 135. Edge Feature Extension Rule

Any new edge feature must define:

1. source variables;

2. geometric meaning;

3. transformation type;

4. exchange behavior;

5. units;

6. cutoff behavior where applicable;

7. provenance;

8. validation.

---

## 136. Resonance Message Extension Rule

Any resonance-conditioned message must define:

1. resonance variable;

2. resonance state space;

3. transformation behavior;

4. scale;

5. window relation where used;

6. conditioning mechanism;

7. provenance;

8. validation.

---

## 137. Ternary Message Extension Rule

Any ternary-conditioned message must define:

1. ternary semantic role;

2. target, pending, or executed source;

3. encoding;

4. permutation behavior;

5. spatial transformation behavior;

6. active-neutral semantics;

7. validation.

---

## 138. Mechanical Readout Extension Rule

Any mechanical readout must define:

1. source representation;

2. output physical quantity;

3. units;

4. transformation law;

5. aggregation;

6. derivative relation where used;

7. validation.

---

## 139. Canonical Message-Passing Invariants

Every conforming message-passing layer preserves:

1. explicit graph topology;

2. explicit node-state typing;

3. explicit edge-state typing;

4. explicit message function;

5. explicit aggregation;

6. explicit update function;

7. explicit permutation behavior;

8. explicit spatial transformation behavior;

9. explicit resonance interface where used;

10. explicit ternary interface where used;

11. explicit provenance;

12. explicit validation.

---

## 140. Canonical Semantic Distinctions

The framework preserves:

`graph edge ≠ chemical bond`

`message ≠ mechanical force`

`message-passing layer ≠ physical time step`

`latent state ≠ ternary state`

`resonance state ≠ ternary state`

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`

`missing data ≠ ternary 0`

`pending state ≠ active neutral`.

---

## 141. Canonical Ternary Invariants

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

The opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 142. Interface to Interaction Topology

The message-passing layer receives the graph topology from the declared interaction-topology construction.

The topology interface defines:

- nodes;
- edges;
- neighborhoods;
- periodic images;
- cutoff relations;
- long-range channels where present.

---

## 143. Interface to Energy Functionals

Invariant node or graph representations may be supplied to the energy-functional layer.

The energy interface requires an invariant scalar output under the declared spatial symmetry group.

---

## 144. Interface to Force Derivation

Force may be derived from a differentiable scalar energy or predicted through an explicitly equivariant force branch.

The selected relation must be explicit.

---

## 145. Interface to Stress

Stress prediction receives appropriately typed latent, geometric, or energy-derived quantities and returns the declared tensor representation.

---

## 146. Interface to Resonance-Conditioned Interactions

Resonance variables may condition:

- edge messages;
- node updates;
- interaction weights;
- gates;
- readout functions.

The resonance variables retain their own state-space and classification semantics.

---

## 147. Final Formal Structure

A message-passing layer may be represented as:

`MP_k = (G, H_k, E_k, M_k, A_k, U_k)`.

Here:

- `G` is the interaction graph;
- `H_k` is the node representation space at layer `k`;
- `E_k` is the edge representation space;
- `M_k` is the message function;
- `A_k` is the aggregation operator;
- `U_k` is the node update.

For node:

`i`

the canonical computation is:

`m_ij^[k] = M_k(h_i^[k], h_j^[k], e_ij^[k])`

`m_i^[k] = A_k({m_ij^[k] | j ∈ N(i)})`

`h_i^[k+1] = U_k(h_i^[k], m_i^[k])`.

A stack of:

`K_MP`

layers defines:

`h^[0] → h^[1] → ... → h^[K_MP]`.

The layer index is a computational index.

It is not physical time.

---

## 148. Final Statement

The TR-EIF message-passing layer maps typed local interatomic information through graph-structured message, aggregation, and update operations.

Node and edge representations retain explicit transformation types.

Permutation behavior follows entity reindexing.

Relative geometry supplies translation-invariant and rotation-compatible spatial information.

Invariant, vector, tensor, and irreducible representation channels remain separately typed.

Resonance variables may condition message passing through explicitly defined mappings.

Resonance classes remain separate from ternary states.

The semantic ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Target, pending, and executed ternary roles remain distinct.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Message-passing outputs remain computational representations until mapped through explicitly defined physical, resonance, ternary, or mechanical interfaces.
