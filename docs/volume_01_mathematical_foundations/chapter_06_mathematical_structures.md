# Mathematical Structures

## 1. Purpose

This document defines the mathematical structures used to organize states, relations, transformations, interactions, transitions, and multiscale representations in the Ternary Resonant Equivariant Interatomic Framework.

The structures defined here provide the formal containers within which TR-EIF operators act.

This chapter establishes the distinction between:

- sets;
- Cartesian products;
- relations;
- ordered structures;
- graphs;
- vector spaces;
- metric spaces;
- topological spaces;
- manifolds;
- circular phase spaces;
- discrete ternary spaces;
- hybrid spaces;
- transformation groups;
- group actions;
- invariant and equivariant structures;
- quotient structures;
- dynamical systems;
- transition systems;
- structural-state regions;
- multiscale families;
- history spaces;
- observable spaces.

A mathematical structure must not be introduced only through implementation.

Its elements, relations, admissible operations, and applicable invariants must be defined explicitly.

## 2. Status of This Document

The structures in this chapter belong to the TR-EIF formal framework.

This document depends on:

- `chapter_01_foundations.md`;
- `chapter_02_notation_and_definitions.md`;
- `chapter_03_axiomatic_system.md`;
- `chapter_04_state_spaces.md`;
- `chapter_05_mathematical_operators.md`.

The definitions established in those documents remain authoritative.

This chapter does not claim that every TR-EIF model must use every mathematical structure described below.

A specific model must use only the structures required by its declared state spaces, operators, symmetries, interactions, and validation contracts.

## 3. Structural Construction Principle

A TR-EIF mathematical structure is constructed in the following order:

`elements`

`→ domains`

`→ relations`

`→ permitted operations`

`→ transformations`

`→ invariants`

`→ admissible subsets`

`→ model-specific interpretation`

The existence of a numerical representation does not by itself establish a mathematical structure.

For example:

- an array is not automatically a vector space;
- a matrix is not automatically a physical operator;
- a collection of edges is not automatically an interaction graph;
- a finite set of values is not automatically an ordered set;
- a list of phases is not automatically a synchronized state;
- a scalar score is not automatically a metric.

Every claimed structure must satisfy its declared mathematical properties.

## 4. Sets

### 4.1 Definition

A set is a collection of distinguishable elements.

A set is denoted generically by:

`A`

Membership is written as:

`a ∈ A`

Non-membership is written as:

`a ∉ A`

### 4.2 Subset

A set `A₀` is a subset of `A` when every element of `A₀` belongs to `A`:

`A₀ ⊆ A`

### 4.3 Proper subset

A proper subset satisfies:

`A₀ ⊂ A`

when:

`A₀ ⊆ A`

and:

`A₀ ≠ A`

### 4.4 Empty set

The empty set is:

`∅`

The empty set is not equivalent to the balanced ternary state `0`.

### 4.5 Finite and infinite sets

A set may be:

- finite;
- countably infinite;
- uncountable.

The cardinality of a finite set `A` may be written as:

`|A|`

### 4.6 State-set semantics

A state set defines permitted state values.

A state that does not belong to the declared state set is invalid unless an explicit extension is defined.

## 5. Cartesian Product Structures

### 5.1 Definition

For sets `A` and `B`, the Cartesian product is:

`A × B = {(a, b) | a ∈ A and b ∈ B}`

### 5.2 Product state spaces

Composite TR-EIF state spaces are constructed using Cartesian products.

For example:

`S_XT = X × T^N`

contains a continuous state and a ternary configuration.

### 5.3 Multiple factors

For spaces:

`A₁, A₂, ..., A_n`

the product is:

`A₁ × A₂ × ... × A_n`

### 5.4 Typed factors

Each factor retains its own semantics.

Membership in a product space does not merge the meanings of the component spaces.

For:

`(x, σ) ∈ X × T^N`

the continuous state `x` remains continuous and `σ` remains ternary.

### 5.5 Projection from product spaces

A product-space projection may select one component.

For example:

`P_X: X × T^N → X`

and:

`P_T: X × T^N → T^N`

These projections must remain semantically distinct.

## 6. Relations

### 6.1 Definition

A binary relation from set `A` to set `B` is a subset:

`R ⊆ A × B`

If:

`(a, b) ∈ R`

then `a` and `b` satisfy relation `R`.

### 6.2 Relation on one set

A relation on `A` is:

`R ⊆ A × A`

### 6.3 Ternary transition relation

The local ternary transition relation is:

`R_T ⊆ T × T`

where:

`T = {-1, 0, 1}`

The admissible relation contains:

`(-1, -1)`

`(-1, 0)`

`(0, -1)`

`(0, 0)`

`(0, 1)`

`(1, 0)`

`(1, 1)`

It excludes:

`(-1, 1)`

`(1, -1)`

### 6.4 Interaction relation

An interatomic interaction relation may connect atomic sites:

`R_int ⊆ V × V`

Its interpretation depends on the declared interaction model.

### 6.5 Structural relation

A structural relation may connect:

- nodes;
- modes;
- phases;
- scales;
- structural forms;
- state regions;
- transformations.

Every structural relation must define the elements it relates.

## 7. Equivalence Relations

### 7.1 Definition

A relation `~` on set `A` is an equivalence relation when it is:

- reflexive;
- symmetric;
- transitive.

### 7.2 Equivalence class

The equivalence class of `a ∈ A` is:

`[a] = {b ∈ A | b ~ a}`

### 7.3 Physical configuration equivalence

Two coordinate configurations may be treated as equivalent under declared transformations such as:

- translation;
- rotation;
- permutation of equivalent atoms;
- periodic-cell translation.

The transformation set must be defined before an equivalence relation is asserted.

### 7.4 Observable equivalence

Two states may satisfy:

`O(S₁) = O(S₂)`

without being equivalent under the complete state relation.

Observable equality alone does not define full-state equivalence.

## 8. Quotient Structures

### 8.1 Definition

When an equivalence relation `~` is defined on `A`, the quotient set is:

`A / ~`

It contains equivalence classes rather than individual elements.

### 8.2 Symmetry quotient

A symmetry quotient may represent configurations modulo a declared symmetry action.

### 8.3 Information effect

Quotienting removes distinctions considered irrelevant under the declared equivalence relation.

The removed distinctions must be explicit.

### 8.4 No implicit quotient

Two states must not be treated as equivalent merely because an implementation maps them to the same descriptor.

## 9. Ordered Structures

### 9.1 Partial order

A partial order is a relation that is:

- reflexive;
- antisymmetric;
- transitive.

### 9.2 Total order

A total order additionally requires every pair of elements to be comparable.

### 9.3 Ternary values are not universally ordered

Although the numeric labels satisfy:

`-1 < 0 < 1`

TR-EIF does not assign this numerical ordering a universal semantic meaning.

The states represent declared branches and an active neutral state.

A model must not infer that `1` is universally superior to `0` or `-1`.

### 9.4 Event order

Execution events may form a total or partial temporal order.

The selected event-order structure must be declared when simultaneous or concurrent events are possible.

## 10. Sequence Structures

### 10.1 Definition

A sequence is an indexed family:

`{a_n}`

where `n` belongs to a declared index set.

### 10.2 State sequence

A discrete trajectory is:

`{S_n}`

### 10.3 Event sequence

A transition trace may contain:

`{e_k}`

where `k` is the event index.

### 10.4 Ternary sequence

A local ternary history may be represented as:

`{σ_n}`

Every adjacent pair must satisfy the ternary transition relation.

### 10.5 Sequence order

Reordering a state or event sequence changes its meaning unless order invariance is explicitly established.

## 11. Vector Spaces

### 11.1 Definition

A vector space is a set equipped with vector addition and scalar multiplication satisfying the declared vector-space axioms over a scalar field.

### 11.2 Continuous state components

Continuous variables such as positions, velocities, forces, and selected descriptor vectors may belong to vector spaces.

### 11.3 Coordinate space

For spatial dimension `d`:

`x_i ∈ ℝ^d`

### 11.4 Product vector space

A fixed-cardinality collection of positions may belong to:

`(ℝ^d)^N`

### 11.5 Ternary-state distinction

The balanced ternary state set:

`T = {-1, 0, 1}`

is not automatically treated as a vector space.

Arithmetic performed on the numeric labels does not replace the declared ternary transition semantics.

### 11.6 Physical transformation

Vectors must transform according to their declared geometric action.

A vector-valued force and a scalar-valued energy do not share the same transformation rule.

## 12. Affine Structures

### 12.1 Definition

An affine structure permits relative displacement without requiring a distinguished physical origin.

### 12.2 Position and displacement

Absolute coordinates and relative displacement remain distinct.

For positions:

`x_i`

and:

`x_j`

the relative displacement is:

`x_ij = x_j - x_i`

### 12.3 Translation

A global translation may change every coordinate while preserving relative displacement.

This distinction is required for translation-consistent interatomic representations.

## 13. Normed Spaces

### 13.1 Definition

A norm assigns a non-negative magnitude:

`||x||`

to elements of an appropriate vector space.

### 13.2 Euclidean norm

For ordinary Euclidean coordinate space, a Euclidean norm may be used.

### 13.3 Norm declaration

Every use of a norm must identify the norm when multiple choices are possible.

### 13.4 Physical dimensions

A norm of a dimensional vector retains the corresponding physical dimension.

Dimensionally incompatible norms must not be combined without normalization.

## 14. Metric Spaces

### 14.1 Definition

A metric space consists of a set `A` and a distance function:

`d: A × A → ℝ₊`

satisfying the metric axioms.

### 14.2 Continuous metric

A continuous-state metric may be based on a declared norm.

### 14.3 Ternary metric

A global ternary-state distance may count local mismatches.

### 14.4 Circular metric

Phase requires a circular distance rather than unrestricted linear subtraction when wrap equivalence matters.

### 14.5 Graph metric

A graph-state metric may compare:

- edge sets;
- edge weights;
- graph spectra;
- topology descriptors.

### 14.6 Composite metrics

A composite state metric must not add quantities with incompatible units without explicit normalization.

## 15. Pseudometric Structures

### 15.1 Definition

A pseudometric permits distinct elements to have zero distance.

### 15.2 Descriptor-level comparison

Two distinct configurations may have zero descriptor distance under a representation that intentionally discards some distinctions.

### 15.3 Interpretation

Zero pseudometric distance does not imply exact state identity.

## 16. Topological Spaces

### 16.1 Definition

A topological space defines which subsets are open and therefore provides a formal basis for:

- neighborhoods;
- continuity;
- convergence;
- boundaries;
- connectedness.

### 16.2 State-space topology

Continuous state spaces may use their standard topology.

Discrete state spaces may use a discrete topology.

### 16.3 Mixed topology

A hybrid TR-EIF state space may combine continuous and discrete factors.

For example:

`X × T^N`

contains both continuous and discrete structure.

### 16.4 State-space boundary

A boundary may occur around:

- admissible regions;
- resonance windows;
- structural regions;
- saturation regions;
- numerical stability regions.

## 17. Connectedness

### 17.1 Connected regions

A connected state-space region permits continuous paths between its points under the declared topology.

### 17.2 Disconnected regions

Different structural regimes may occupy disconnected regions of the admissible state space.

### 17.3 Discrete transitions

A discrete event may connect regions that cannot be joined by the declared continuous evolution alone.

### 17.4 Ternary mediation

The forbidden direct transition:

`-1 → 1`

cannot be introduced by treating the ternary state set as though every labeled value were continuously adjacent.

The operational path remains:

`-1 → 0 → 1`

and conversely.

## 18. Neighborhood Structures

### 18.1 Mathematical neighborhood

A neighborhood is a set associated with a point under the declared topology or metric.

### 18.2 Interatomic neighborhood

An atomic local environment `N_i` is a model-specific neighborhood structure.

Its membership rule may be based on:

- graph connectivity;
- geometry;
- interaction criterion;
- declared cutoff;
- channel relation.

### 18.3 Distinction

A topological neighborhood and an atomic interaction neighborhood are not automatically the same object.

## 19. Manifold Structures

### 19.1 Definition

A manifold is a space locally represented by coordinate neighborhoods of a declared dimension.

### 19.2 Applicability

A TR-EIF model may use manifold structure when the represented state or configuration space requires it.

### 19.3 Coordinate charts

A chart maps a local region of a manifold into a coordinate representation.

### 19.4 No universal manifold claim

TR-EIF does not assume that every complete hybrid state space is a smooth manifold.

Discrete ternary states, graph changes, and structural events can create non-smooth or hybrid structures.

## 20. Circular Phase Space

### 20.1 Definition

Oscillator phase belongs to:

`𝕊¹`

### 20.2 Periodicity

Phases differing by an integer multiple of one complete revolution represent the same circular phase.

### 20.3 Numerical representation

A phase may be stored on an interval such as:

`[0, 2π)`

or:

`(-π, π]`

### 20.4 Circular relation

Phase difference must use the declared wrap operation when circular equivalence matters.

### 20.5 Phase and state space

The circular phase variable is distinct from dynamical phase space.

## 21. Discrete Ternary Structure

### 21.1 Primitive set

The balanced ternary state set is:

`T = {-1, 0, 1}`

### 21.2 Canonical representation

The canonical textual representation is:

`-1/0/1`

### 21.3 Active neutral state

The state `0` is an active mathematical and operational state.

It may represent:

- mediation;
- balancing;
- routing;
- damping;
- retention;
- transition staging.

### 21.4 Transition graph

The local ternary transition structure may be represented as a directed graph with nodes:

`{-1, 0, 1}`

and admissible edges:

`-1 → -1`

`-1 → 0`

`0 → -1`

`0 → 0`

`0 → 1`

`1 → 0`

`1 → 1`

Forbidden edges:

`-1 → 1`

`1 → -1`

### 21.5 Path semantics

A path through the ternary transition graph is part of the state semantics.

Identical initial and final states do not imply identical transition histories.

## 22. Graph Structures

### 22.1 Definition

A graph is:

`G = (V, E)`

where:

- `V` is the node set;
- `E` is the edge set.

### 22.2 Directed graph

For directed interaction:

`(i, j) ∈ E`

does not imply:

`(j, i) ∈ E`

### 22.3 Undirected graph

For an undirected graph, an edge connects a pair without direction.

### 22.4 Weighted graph

A weighted graph associates weights with edges:

`w_ij`

### 22.5 Dynamic graph

A dynamic graph is:

`G(t) = (V(t), E(t))`

### 22.6 Interatomic graph

In an interatomic representation:

- nodes may represent atomic sites;
- edges may represent declared interaction relations.

An edge does not itself establish a physical bond unless the model defines that interpretation.

## 23. Multigraph and Multi-Channel Structures

### 23.1 Multiple relations

Two components may participate in several distinct interaction channels.

### 23.2 Channel distinction

Different interaction channels must remain separately identifiable.

### 23.3 Multi-channel edge state

An edge may contain a structured state:

`χ_ij = (χ_ij,1, ..., χ_ij,m)`

where each component belongs to a declared interaction channel.

### 23.4 No accidental aggregation

Multiple channels must not be collapsed into one scalar without an explicit aggregation rule.

## 24. Hypergraph Structures

### 24.1 Definition

A hypergraph permits one interaction relation to connect more than two nodes.

### 24.2 Applicability

A model may use a hypergraph when an interaction or structural descriptor is fundamentally multi-body.

### 24.3 Pairwise distinction

A multi-body relation must not be represented as pairwise interaction unless the corresponding reduction is explicitly defined.

## 25. Bipartite and Layered Graph Structures

### 25.1 Bipartite structure

A bipartite graph separates nodes into two declared classes.

### 25.2 Layered structure

A layered graph may represent distinct relation types such as:

- physical interactions;
- resonant couplings;
- control relations;
- information dependencies.

### 25.3 Layer preservation

Edges from distinct semantic layers must remain distinguishable.

## 26. Interaction Networks

### 26.1 Definition

An interaction network consists of components and declared relations through which dynamic influence is represented.

### 26.2 State-dependent network

An interaction network may depend on system state:

`G = G(S)`

### 26.3 Geometry-dependent network

An interaction relation may depend on current geometry.

### 26.4 History-dependent network

An interaction topology may depend on inherited or hysteretic state.

### 26.5 Dynamic consistency

When topology changes, all dependent structures must be updated consistently.

## 27. Group Structures

### 27.1 Definition

A group consists of a set and a binary operation satisfying:

- closure;
- associativity;
- identity;
- inverse existence.

### 27.2 Symmetry groups

A declared symmetry group is denoted by:

`G_sym`

### 27.3 Possible transformation classes

A model may use transformation structures associated with:

- translations;
- rotations;
- reflections;
- permutations;
- combinations of these operations.

### 27.4 Scope

A symmetry group must be declared for the specific model.

TR-EIF does not impose one universal symmetry group on every interatomic representation.

## 28. Group Actions

### 28.1 Definition

A group action describes how transformations act on a space.

For state space `X`:

`ρ_X(g): X → X`

for:

`g ∈ G_sym`

### 28.2 Multiple actions

The same transformation may act differently on:

- positions;
- velocities;
- forces;
- tensors;
- graph indices;
- observables.

### 28.3 Ternary state action

Geometric transformations do not automatically alter ternary values.

A ternary action must be defined explicitly if required.

### 28.4 Action consistency

Composition of transformations must correspond to composition of their declared actions.

## 29. Invariant Structures

### 29.1 Invariant quantity

A quantity is invariant under a declared transformation when its value does not change under that transformation.

### 29.2 Invariant mapping

For:

`F: X → Y`

invariance under input action `ρ_X` means:

`F(ρ_X(g)x) = F(x)`

### 29.3 Scope limitation

Invariance applies only to the declared transformation class.

A quantity invariant under translation may not be invariant under scaling or another transformation.

## 30. Equivariant Structures

### 30.1 Definition

A mapping is equivariant when transformation of the input produces the corresponding declared transformation of the output.

For:

`F: X → Y`

the relation is:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

### 30.2 Structural role

Equivariance preserves transformation consistency rather than numerical equality.

### 30.3 Vector outputs

A vector-valued output may rotate with the input while preserving equivariance.

### 30.4 Scalar outputs

A scalar output may remain invariant when its physical meaning requires invariance.

### 30.5 Graph equivariance

A graph representation may preserve relations under declared node permutation.

## 31. Orbit Structures

### 31.1 Definition

The orbit of state `x` under group `G_sym` is the set of states reachable by the declared symmetry action:

`Orb(x) = {ρ_X(g)x | g ∈ G_sym}`

### 31.2 Symmetry-equivalent configurations

States within one orbit are symmetry-related under the declared action.

### 31.3 Orbit distinction

Dynamic reachability and symmetry orbit membership are different concepts.

A state may be symmetry-related without being dynamically reachable from another state under the model evolution.

## 32. Stabilizer Structures

### 32.1 Definition

The stabilizer of state `x` is the set of transformations that leave `x` unchanged under the declared action.

### 32.2 Structural use

Changes in the stabilizer may be used to characterize changes in symmetry structure when the model explicitly defines that criterion.

### 32.3 No automatic phase-transition claim

A symmetry change alone must not be labeled a physical phase transition without the additional model-specific conditions required for that claim.

## 33. Dynamical-System Structures

### 33.1 Definition

A dynamical system consists of:

- state space;
- time structure;
- evolution rule.

### 33.2 Continuous system

A continuous-time system evolves over a continuous time domain.

### 33.3 Discrete system

A discrete system evolves through indexed state updates.

### 33.4 Hybrid system

A hybrid system combines:

- continuous evolution;
- discrete events;
- guards;
- transition maps.

### 33.5 TR-EIF hybrid structure

TR-EIF permits hybrid state evolution because continuous interatomic or resonant dynamics may coexist with discrete balanced ternary state transitions.

## 34. Flow and Semiflow Structures

### 34.1 Flow

A flow represents time evolution when the required invertibility and composition properties hold.

### 34.2 Semiflow

A semiflow represents forward evolution when reverse-time evolution is not required.

### 34.3 Dissipative systems

A dissipative model may naturally require a forward-time structure without global reversibility.

### 34.4 No default reversibility

TR-EIF does not assume that complete system dynamics are reversible.

## 35. Non-Autonomous Dynamical Structures

### 35.1 Definition

A non-autonomous system depends explicitly on time or an external driving trajectory.

### 35.2 Driving state

The model may depend on:

`b(t)`

where `b(t)` belongs to the declared boundary or forcing state space.

### 35.3 Execution record

The complete forcing trajectory required for deterministic replay must be preserved.

## 36. Delayed Dynamical Structures

### 36.1 Definition

A delayed system depends on prior state values.

### 36.2 History space

The state required for future evolution may therefore include a history object:

`H(t)`

### 36.3 Effective state

For delayed systems, the instantaneous state alone may be insufficient to determine future evolution.

### 36.4 History equivalence

Two equal instantaneous states may remain dynamically different when their histories differ.

## 37. Transition Systems

### 37.1 Definition

A transition system contains:

- state set;
- transition relation;
- optional event labels;
- optional guards.

### 37.2 Ternary transition system

The balanced ternary layer forms a transition system over:

`{-1, 0, 1}`

with forbidden direct opposite-state transitions.

### 37.3 Labeled transition

A transition may carry a label identifying:

- cause;
- guard;
- event type;
- source;
- destination;
- timestamp;
- route.

### 37.4 Transition path

The sequence of intermediate states is part of the transition structure.

## 38. Hybrid Automaton Structure

### 38.1 Definition

A hybrid automaton may contain:

- discrete modes;
- continuous states;
- mode-dependent continuous dynamics;
- guards;
- reset maps.

### 38.2 TR-EIF compatibility

A model may use a hybrid automaton structure when continuous dynamics and discrete ternary or structural transitions require explicit mode separation.

### 38.3 Neutral mode

A model-specific active-neutral mode may correspond to ternary state `0`.

Its continuous dynamics must be defined explicitly.

### 38.4 No universal automaton

TR-EIF does not require every model to be represented as one specific hybrid automaton.

## 39. Attractor Structures

### 39.1 Definition

An attractor is a dynamical object toward which states in a declared basin approach under the declared evolution.

### 39.2 Possible forms

An attractor may be:

- fixed;
- periodic;
- quasiperiodic;
- more complex.

### 39.3 Stability and value

Attractor stability does not imply that the resulting state is structurally constructive.

A stable state may correspond to:

- retention;
- simplification;
- degradation;
- another declared structural outcome.

### 39.4 Model-specific proof

An attractor claim requires the corresponding mathematical or numerical evidence.

## 40. Basin Structures

### 40.1 Basin of attraction

A basin contains initial states whose trajectories approach a declared attractor.

### 40.2 Boundary sensitivity

Different basins may be separated by boundaries where small state changes produce different long-term regimes.

### 40.3 Structural relevance

A basin boundary may be relevant to structural-transition analysis when the model explicitly establishes that relation.

## 41. Resonance-Window Structures

### 41.1 Parameter space

A resonance parameter space is:

`P_R`

### 41.2 Resonance window

A resonance window is:

`W_R ⊂ P_R`

### 41.3 Window geometry

The resonance window may have a nontrivial shape in multidimensional parameter space.

### 41.4 Boundary

Its boundary is:

`∂W_R`

### 41.5 Entry and exit relations

Entry and exit may depend on:

- trajectory direction;
- history;
- hysteresis;
- state;
- coupling;
- dissipation.

### 41.6 No single-frequency reduction

A multidimensional resonance region must not be reduced to one scalar frequency without an explicit derivation.

## 42. Structural-State Regions

### 42.1 Structural state space

The structural state space is:

`X_F`

### 42.2 Structural region

A declared structural form `F_k` corresponds to a region:

`R_F,k ⊆ X_F`

### 42.3 Region overlap

If structural regions overlap, the classification rule must define how ambiguity is resolved.

### 42.4 Region separation

Disjoint structural regions may represent distinguishable structural forms.

### 42.5 Boundary state

A state on:

`∂R_F,k`

may require explicit boundary semantics.

## 43. Structural-Transition Structures

### 43.1 Transition path

A structural transition may be represented by:

`R_pre → R_tr → R_post`

### 43.2 Pre-transition region

`R_pre` contains states belonging to the prior structural form.

### 43.3 Transition region

`R_tr` contains intermediate states associated with reorganization.

### 43.4 Post-transition region

`R_post` contains states satisfying the new structural conditions.

### 43.5 Transition completion

A structural transition is complete only when the declared post-transition conditions and stabilization criteria are satisfied.

## 44. Recursive Structures

### 44.1 Recursive cycle

A recursive structure uses the result of one stage as part of the input to a subsequent stage.

### 44.2 TR-EIF inheritance

For cycle index `n`:

`S_n,final`

`→ I_n→n+1`

`→ S_n+1,initial`

### 44.3 Path dependence

The resulting state may depend on the trajectory that generated the inherited state.

### 44.4 Non-Markovian structure

When current state variables alone are insufficient and history is required, the reduced description is non-Markovian with respect to those current variables.

## 45. History Spaces

### 45.1 Definition

A history space contains state functions or sequences over a declared past interval.

### 45.2 Continuous history

For maximum delay `τ_max`:

`H_X(t) = {X(s) | s ∈ [t - τ_max, t]}`

### 45.3 Discrete history

A finite discrete history may be:

`H_n = (S_n, S_n-1, ..., S_n-L+1)`

### 45.4 History dimension

A history structure may be effectively higher-dimensional than the instantaneous state representation.

### 45.5 Compression

A compressed memory state is a separate mathematical object and must not be assumed equivalent to complete history without proof.

## 46. Probability Spaces

### 46.1 Applicability

A stochastic TR-EIF model may require a probability space.

### 46.2 Required elements

The stochastic construction must declare:

- sample space;
- event structure;
- probability measure;
- random variables;
- distributions used by the model.

### 46.3 Numerical randomness

A pseudorandom generator used by an implementation is a computational realization and must remain distinguishable from the abstract probability model.

### 46.4 Deterministic models

Probability structures must not be introduced into deterministic models without a defined purpose.

## 47. Measure Structures

### 47.1 Applicability

A measure may be used when the model requires quantitative size, integration, probability, or distribution over a space.

### 47.2 Domain

The measured sets and measure definition must be explicit.

### 47.3 Physical interpretation

A mathematical measure does not acquire a physical interpretation without a declared mapping.

## 48. Tensor Structures

### 48.1 Definition

Tensor-valued quantities transform according to declared multilinear transformation rules.

### 48.2 Applicability

TR-EIF may contain tensor-valued representations such as stress or other directional multi-component quantities.

### 48.3 Transformation behavior

Tensor order and transformation law must be declared.

### 48.4 Scalar distinction

A tensor must not be reduced to one scalar quantity without an explicit invariant, projection, or aggregation operator.

## 49. Field Structures

### 49.1 Definition

A field assigns values to locations in a declared spatial, temporal, graph, or configuration domain.

### 49.2 Examples of field domains

A field may be defined over:

- physical space;
- atomic sites;
- graph nodes;
- graph edges;
- time;
- configuration space.

### 49.3 Discrete field

A quantity defined at atomic sites may form a discrete field over the site set.

### 49.4 Continuous field

A spatially continuous representation requires its own domain and regularity assumptions.

## 50. Local and Global Structures

### 50.1 Local structure

A local structure is defined on:

- one site;
- one neighborhood;
- one interaction;
- one mode;
- one state-space region.

### 50.2 Global structure

A global structure is defined over the complete represented system.

### 50.3 Local-to-global relation

A global property must not be inferred automatically from local validity.

### 50.4 Global-to-local relation

A global invariant does not imply that every local component has identical state.

## 51. Hierarchical Structures

### 51.1 Definition

A hierarchical structure contains multiple organizational levels with declared relations between levels.

### 51.2 Scale index

A scale may be identified by:

`s`

with state space:

`S_s`

### 51.3 Cross-scale relation

A mapping:

`M_s→r: S_s → S_r`

connects declared scales.

### 51.4 Carrier distinction

Similar organizational relations across scales do not imply identical physical carriers.

### 51.5 No automatic self-similarity claim

Self-similarity must be defined through explicit preserved relations or invariants.

Visual resemblance is insufficient.

## 52. Multiscale Product Structures

### 52.1 Complete multiscale state

A multiscale state may be represented as:

`S_multi = ∏ S_s`

over the declared scale set.

### 52.2 Coupled scales

The complete evolution may contain mappings between scales.

### 52.3 Scale-specific variables

Different scales may use different:

- state variables;
- time resolutions;
- spatial resolutions;
- operators;
- observables.

### 52.4 Cross-scale consistency

Compatibility relations must be defined explicitly.

## 53. Coarse-Grained Structures

### 53.1 Definition

A coarse-grained structure is produced by reducing fine-scale information.

### 53.2 Coarse-graining map

`C_s→r: S_s → S_r`

### 53.3 Information loss

The mapping must identify discarded information.

### 53.4 Emergent variables

A coarse-scale variable may not have a one-to-one correspondence with one microscopic variable.

### 53.5 Reconstruction limitation

A coarse-grained state must not be treated as a complete microscopic state.

## 54. Partition Structures

### 54.1 Definition

A partition divides a set into non-overlapping subsets whose union is the original set.

### 54.2 Possible uses

Partitions may represent:

- phase clusters;
- graph communities;
- structural classes;
- spatial regions;
- mode groups.

### 54.3 Partition dynamics

A dynamic partition may change with time.

The transition of an element between subsets must be represented explicitly when semantically relevant.

## 55. Cluster Structures

### 55.1 Definition

A cluster is a declared group of components satisfying a model-specific relation.

### 55.2 Phase cluster

A phase cluster may contain oscillatory components satisfying a defined phase relation.

### 55.3 Structural cluster

A structural cluster may group atomic sites by a declared environment or connectivity relation.

### 55.4 No implicit meaning

A computational clustering algorithm does not automatically establish a physical structural class.

The cluster interpretation requires a declared criterion.

## 56. Mode Structures

### 56.1 Definition

A mode is a distinguishable dynamic organization supported by the declared model and boundary conditions.

### 56.2 Mode state

A model may represent:

- mode amplitude;
- mode phase;
- mode occupation;
- mode coupling.

### 56.3 Mode basis

A modal decomposition requires a declared basis or decomposition procedure.

### 56.4 Basis dependence

Mode coordinates may depend on the selected representation.

A mode label must not be treated as universally invariant without establishing that property.

## 57. Coherence Structures

### 57.1 Definition

A coherence structure represents a declared relation maintained across components, time, space, or scales.

### 57.2 Nonuniform coherence

Coherence may include:

- nonzero phase offsets;
- counterphase relations;
- multiple clusters;
- spatial gradients.

### 57.3 Coherence relation

The relation used to define coherence must be explicit.

### 57.4 Coherence measure

A scalar or vector coherence measure is an observable or descriptor of the coherence structure.

It is not identical to the structure itself.

## 58. Synchronization Structures

### 58.1 Definition

A synchronization structure represents a declared stable temporal relation among dynamic components.

### 58.2 Phase locking

Phase locking is one possible synchronization structure.

### 58.3 Frequency relation

Synchronization may involve a declared frequency relation.

### 58.4 Cluster synchronization

Different subsets may synchronize internally while maintaining different relations between clusters.

### 58.5 Resonance distinction

Synchronization structure and resonance structure remain distinct unless a model explicitly relates them.

## 59. Energy-Accounting Structures

### 59.1 Definition

An energy-accounting structure organizes declared energy terms and transfers.

### 59.2 Components

It may include:

- stored energy;
- input energy;
- output energy;
- dissipated energy;
- transferred energy;
- structural-work term;
- numerical residual.

### 59.3 Dimensional consistency

All terms combined in one accounting relation must use compatible dimensions.

### 59.4 Numerical residual

A residual remains a separate quantity until its source is established.

It must not be assigned automatically to physical dissipation.

## 60. Constraint Structures

### 60.1 Definition

A constraint structure is a collection of conditions defining an admissible subset of a state space.

### 60.2 Admissible region

For state space `S`:

`S_adm ⊆ S`

### 60.3 Constraint intersection

Several constraints may define:

`S_adm = S₁ ∩ S₂ ∩ ... ∩ S_k`

### 60.4 Empty admissible region

If the intersection is empty, the parameterization or model configuration is inconsistent.

The implementation must not create a valid state artificially.

## 61. Invariant Sets

### 61.1 Definition

A set is invariant under an evolution when states starting in that set remain within it under the declared evolution.

### 61.2 Application

Invariant sets may represent:

- admissible regimes;
- structural regimes;
- bounded dynamic regions.

### 61.3 Failure

Leaving a required invariant set must produce a visible validation event.

## 62. Boundary Structures

### 62.1 State-space boundary

A mathematical boundary separates regions of a state space.

### 62.2 Physical boundary

A physical boundary describes a declared interface of the represented system.

### 62.3 Computational boundary

A computational boundary may define:

- valid input range;
- representable numerical range;
- schema limit;
- implementation capacity.

### 62.4 Distinction

Mathematical, physical, and computational boundaries must not be silently conflated.

## 63. Observable Structures

### 63.1 Observable space

Observable outputs belong to:

`Y`

### 63.2 Product output

For multiple observables:

`Y = Y₁ × ... × Y_n`

### 63.3 Observable subset

Only selected state information may be visible in `Y`.

### 63.4 Observable trajectory

An observable time series is:

`y(t) = O(S(t))`

or, in discrete execution:

`y_n = O(S_n)`

### 63.5 Observation structure

The observation chain may contain:

`state`

`→ projection`

`→ measurement model`

`→ sampling`

`→ quantization`

`→ output`

Every stage must remain identifiable.

## 64. Trace Structures

### 64.1 Definition

A trace is an ordered representation of execution-relevant states and events.

### 64.2 Trace elements

A trace may contain:

- state snapshots;
- event records;
- transition legs;
- invariant results;
- numerical status;
- observable outputs;
- version metadata.

### 64.3 Trace order

Trace ordering must preserve causal or execution order as defined by the model.

### 64.4 Ternary path preservation

A trace must preserve neutral-mediated opposite-state transition paths.

Recording only the final state is insufficient when transition-path validity is part of the invariant set.

## 65. Validation Structures

### 65.1 Definition

A validation structure associates mathematical or computational requirements with explicit evaluation states.

### 65.2 Invariant collection

A validation state may contain:

`V = (v₁, v₂, ..., v_m)`

where each `v_k` corresponds to one declared invariant.

### 65.3 Required states

A validation structure must distinguish at least where relevant:

- pass;
- fail;
- not evaluated;
- unsupported.

### 65.4 Aggregation

A required invariant failure cannot be hidden by aggregation with successful unrelated checks.

## 66. Error Structures

### 66.1 Numerical error

A numerical error belongs to the numerical realization.

### 66.2 Modeling error

A modeling discrepancy represents difference between the mathematical model and the compared reference or physical system under the declared comparison.

### 66.3 Measurement uncertainty

Measurement uncertainty belongs to the observation process unless mapped explicitly into another layer.

### 66.4 Structural distinction

Numerical error, model discrepancy, and measurement uncertainty are different objects.

## 67. Uncertainty Structures

### 67.1 Set-based uncertainty

An uncertain state may belong to:

`U_S ⊆ S`

### 67.2 Interval representation

A scalar uncertainty may be represented by a declared interval.

### 67.3 Distribution representation

A probabilistic uncertainty may use a probability distribution.

### 67.4 Ternary distinction

Uncertainty is not encoded automatically as ternary state `0`.

## 68. Numerical Structures

### 68.1 Floating-point representation

A floating-point state is a finite numerical representation of a mathematical quantity.

### 68.2 Fixed-point representation

A fixed-point state is a discrete numerical representation determined by:

- width;
- scale;
- signedness;
- rounding;
- overflow behavior.

### 68.3 Integer representation

An integer encoding may represent:

- index;
- count;
- label;
- quantized physical quantity;
- ternary state.

The semantic role must be explicit.

### 68.4 Ternary encoding

A binary machine encoding of `-1`, `0`, and `1` does not change the mathematical ternary state domain.

## 69. Hybrid Mathematical Structure

The complete TR-EIF architecture may combine:

- continuous state spaces;
- discrete ternary spaces;
- graph structures;
- history spaces;
- symmetry actions;
- structural regions;
- boundary states;
- numerical states;
- observable spaces.

A generic hybrid state structure is:

`S = X × T^N × X_G × X_H × X_F × X_B × X_num × X_val`

A model may use a strict subset.

The semantic distinction between the factors must remain preserved.

## 70. Structure-Preserving Maps

### 70.1 Definition

A structure-preserving map retains the declared relation or operation relevant to a mathematical structure.

### 70.2 Examples

Depending on the declared structure, a mapping may preserve:

- metric relation;
- topology;
- graph adjacency;
- symmetry action;
- ordering;
- algebraic operation;
- structural invariant.

### 70.3 Declared preservation

A mapping must identify exactly which structure it preserves.

The generic phrase `structure-preserving` is insufficient without this declaration.

## 71. Isomorphism

### 71.1 Definition

An isomorphism is a bijective mapping preserving the declared mathematical structure.

### 71.2 Structural equivalence

Two representations may be structurally equivalent under an isomorphism while using different labels or coordinates.

### 71.3 Model dependence

The relevant preserved structure must be specified.

Graph isomorphism, vector-space isomorphism, and dynamical equivalence are different claims.

## 72. Homomorphism

### 72.1 Definition

A homomorphism preserves a declared algebraic operation.

### 72.2 Scope

The operation being preserved must be stated.

### 72.3 No generic substitution

A structure-preserving mapping must not be called a homomorphism unless the relevant algebraic structures and operations are defined.

## 73. Embedding Structures

### 73.1 Mathematical embedding

An embedding represents one structure inside another while preserving the declared relevant structure.

### 73.2 Descriptor embedding

A learned or computational embedding is a representation map and does not automatically satisfy the mathematical definition of a topological or algebraic embedding.

### 73.3 Terminological separation

The repository must distinguish:

- mathematical embedding;
- numerical encoding;
- learned representation;
- state-space inclusion.

## 74. Structural Closure

### 74.1 Definition

A set is closed under an operation when applying that operation to admissible elements produces an element within the declared set.

### 74.2 Ternary transition closure

The ternary update operator must return a value in:

`{-1, 0, 1}`

### 74.3 Admissibility distinction

Closure of the value set does not guarantee transition admissibility.

For example, both `-1` and `1` belong to `T`, but:

`-1 → 1`

remains forbidden.

## 75. Structural Consistency

A mathematical structure is internally consistent when:

- elements belong to their declared domains;
- operations act on valid inputs;
- outputs belong to declared codomains;
- relations satisfy their definitions;
- transformation rules are compatible;
- invariants are preserved where required.

A numerical implementation must not be used to redefine an inconsistent mathematical structure silently.

## 76. Cross-Structure Compatibility

When several mathematical structures coexist, their shared objects must have compatible semantics.

Examples include:

- a graph node and its atomic-site state;
- a phase variable and its circular metric;
- a ternary state and its transition relation;
- a vector and its transformation action;
- a structural region and its classification operator;
- a history state and its delay operator.

An object must not belong simultaneously to incompatible structures under the same interpretation.

## 77. Structure Dependency Rules

The following dependency rules apply:

1. A relation requires defined sets.

2. A transition system requires a state set and transition relation.

3. A graph requires node and edge sets.

4. A metric requires a declared domain.

5. A topology requires a declared underlying set.

6. A group action requires a group and a target space.

7. An equivariant structure requires declared input and output actions.

8. A dynamical system requires a state space and evolution rule.

9. A delayed system requires a history structure.

10. A structural-transition system requires defined structural regions.

11. A multiscale system requires declared scale-indexed state spaces.

12. A quotient requires an equivalence relation.

13. A validation structure requires defined invariants.

14. A trace requires ordered states or events.

## 78. Structural Non-Substitution Rules

The following structures remain distinct:

`set ≠ vector space`

`array ≠ vector space`

`numeric labels ≠ ordered physical meaning`

`graph ≠ geometry`

`graph edge ≠ physical bond`

`metric ≠ observable`

`descriptor space ≠ physical configuration space`

`phase circle ≠ dynamical phase space`

`symmetry orbit ≠ dynamic trajectory`

`equivalence ≠ equality`

`observable equivalence ≠ state equivalence`

`resonance window ≠ structural region`

`structural region ≠ attractor`

`attractor stability ≠ constructive outcome`

`history state ≠ instantaneous state`

`coarse-grained state ≠ microscopic state`

`mathematical embedding ≠ arbitrary encoded representation`

`numerical structure ≠ physical structure`

## 79. Mathematical-Structure Invariants

The following invariants apply throughout TR-EIF.

1. Every mathematical structure has a declared underlying set or space.

2. Every relation identifies the sets it connects.

3. Every operation identifies its admissible inputs.

4. Every structure-preserving claim states which structure is preserved.

5. Continuous and ternary structures remain distinct.

6. The balanced ternary set remains exactly `{-1, 0, 1}`.

7. The canonical representation remains `-1/0/1`.

8. State `0` remains active.

9. Direct `-1 → 1` transition edges remain forbidden.

10. Direct `1 → -1` transition edges remain forbidden.

11. Transition paths remain distinct from final-state equality.

12. Graph topology remains distinct from spatial geometry.

13. Oscillator phase remains defined on a circular space.

14. Symmetry actions are declared before invariance or equivariance claims.

15. Quotient structures require explicit equivalence relations.

16. Delayed dynamics require history structures.

17. Structural transitions require pre-transition and post-transition structures.

18. Multiscale mappings identify information loss or reconstruction assumptions.

19. Numerical representations remain distinguishable from abstract mathematical structures.

20. Validation failures remain explicit.

## 80. Conformance Requirements

A TR-EIF mathematical model conforms to this chapter when:

- every mathematical object belongs to a defined structure;
- every relation has a declared domain;
- every graph has defined node and edge semantics;
- every vector, tensor, or scalar transformation is correctly typed;
- every ternary state obeys the declared transition structure;
- every symmetry claim identifies its group action;
- every structural region is mathematically defined;
- every history-dependent model includes its history structure;
- every multiscale relation identifies its source and target structures;
- every observable remains separated from the complete internal state.

An implementation conforms when:

- data structures preserve the approved mathematical semantics;
- serialization does not merge incompatible state types;
- graph updates preserve graph-state consistency;
- ternary encodings preserve `-1/0/1` semantics;
- numerical representation does not introduce undeclared state values;
- transformation implementations preserve their declared actions;
- structural and validation states remain traceable.

## 81. Structural Dependency Architecture

The mathematical-structure dependency architecture is:

`sets`

`→ products and relations`

`→ continuous and discrete spaces`

`→ metrics and topology`

`→ graph and interaction structures`

`→ phase and oscillatory structures`

`→ transformation groups and actions`

`→ invariant and equivariant structures`

`→ dynamical and transition systems`

`→ resonance and structural regions`

`→ history and recursive structures`

`→ multiscale structures`

`→ observable and trace structures`

`→ validation`

The dependency architecture determines logical construction order.

It does not require one implementation module for each mathematical structure.

## 82. Final Mathematical-Structure Statement

TR-EIF combines explicitly defined continuous, discrete, relational, graph, topological, transformational, dynamical, historical, structural, and multiscale mathematical structures.

The framework preserves a strict distinction between the mathematical carrier of a state and the physical or computational interpretation assigned to it.

Its balanced ternary layer is defined by the active state structure:

`-1/0/1`

with neutral-mediated opposite-state paths:

`-1 → 0 → 1`

`1 → 0 → -1`

Its continuous and interatomic layers remain connected through declared mappings rather than implicit state substitution.

Its equivariant layer operates through declared transformation groups and actions.

Its resonant and structural layers operate over declared state and parameter regions.

Its recursive layer preserves explicitly represented inherited state.

The complete mathematical organization therefore follows:

`defined mathematical objects`

`→ declared structures`

`→ admissible relations`

`→ typed operators`

`→ transformations`

`→ dynamic evolution`

`→ structural transitions`

`→ observable traces`

`→ validation`
