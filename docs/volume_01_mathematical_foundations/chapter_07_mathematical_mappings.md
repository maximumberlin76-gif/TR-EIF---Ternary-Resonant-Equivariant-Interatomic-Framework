# Mathematical Mappings

## 1. Purpose

This document defines the mathematical mapping architecture of the Ternary Resonant Equivariant Interatomic Framework.

Mappings establish explicit relations between:

- physical configurations;
- continuous states;
- balanced ternary states;
- interaction graphs;
- local environments;
- oscillatory representations;
- resonance coordinates;
- structural states;
- symmetry-transformed states;
- scale-dependent representations;
- inherited states;
- numerical realizations;
- observable outputs;
- validation states;
- execution traces.

A TR-EIF mapping must specify what is transformed, what is preserved, what is discarded, and what mathematical space contains the result.

No semantic transition between representation layers may remain implicit.

## 2. Status of This Document

The mapping architecture defined here is part of the TR-EIF formal framework.

This document depends on:

- `chapter_01_foundations.md`;
- `chapter_02_notation_and_definitions.md`;
- `chapter_03_axiomatic_system.md`;
- `chapter_04_state_spaces.md`;
- `chapter_05_mathematical_operators.md`;
- `chapter_06_mathematical_structures.md`.

The definitions established in those chapters remain authoritative.

This chapter does not assign one universal mapping to every TR-EIF model.

A specific model must instantiate only the mappings required by its declared state spaces, operators, physical representation, symmetry structure, and validation contract.

## 3. Mapping Definition

A mapping is written as:

`F: A → B`

where:

- `A` is the domain;
- `B` is the codomain;
- `F` is the mapping rule.

For:

`a ∈ A`

the corresponding mapped value is:

`F(a) ∈ B`

A mapping definition is complete only when it identifies:

1. mapping name;
2. symbol;
3. domain;
4. codomain;
5. input variables;
6. output variables;
7. parameter dependencies;
8. units where applicable;
9. transformation behavior;
10. admissibility conditions;
11. information preserved;
12. information discarded;
13. uncertainty behavior;
14. failure behavior;
15. numerical realization where implemented.

## 4. Mapping Classification

TR-EIF distinguishes mappings by semantic role.

The principal classes are:

- state mappings;
- coordinate mappings;
- projection mappings;
- embedding mappings;
- continuous-to-ternary mappings;
- ternary-conditioned continuous mappings;
- local-environment mappings;
- interaction mappings;
- oscillatory mappings;
- resonance-coordinate mappings;
- symmetry-action mappings;
- invariant mappings;
- equivariant mappings;
- structural mappings;
- transition mappings;
- inheritance mappings;
- multiscale mappings;
- observable mappings;
- numerical mappings;
- serialization mappings;
- validation mappings.

The same numerical function must not be assigned several incompatible semantic roles without explicit separation.

## 5. Domain and Codomain Discipline

### 5.1 Domain

The domain contains every admissible input on which a mapping is defined.

For:

`F: A → B`

an input outside `A` is not a valid input to `F`.

### 5.2 Codomain

The codomain defines the mathematical type of every permitted output.

An implementation must not produce an undeclared output type.

### 5.3 Image

The image of `F` is the subset of `B` actually reached by admissible inputs.

It is denoted by:

`Im(F) ⊆ B`

The codomain and image must not be treated as identical unless equality is established.

### 5.4 Model restriction

A mapping may be valid only on:

`A_adm ⊆ A`

In that case the active mapping is the restriction:

`F|A_adm`

### 5.5 Out-of-domain input

Out-of-domain input must result in an explicit:

- rejection;
- unsupported state;
- validation failure;
- documented extrapolation.

It must not be silently forced into the valid domain.

## 6. Typed Mapping Principle

Every mapping preserves or explicitly changes mathematical type.

Examples:

`continuous state → continuous state`

`continuous state → ternary state`

`configuration → graph`

`complete state → observable`

`fine-scale state → coarse-scale state`

`state → validation result`

The type conversion itself is part of the mathematical definition.

A numerical cast is not a substitute for a semantic mapping.

## 7. Identity Mapping

The identity mapping on space `A` is:

`I_A: A → A`

with:

`I_A(a) = a`

for every:

`a ∈ A`

Identity mappings may represent:

- retained state;
- unchanged structural components;
- unchanged boundary variables;
- unchanged ternary states;
- unchanged topology.

Identity must not be confused with missing execution.

A state may remain unchanged because the declared mapping explicitly returns the same state.

## 8. Mapping Composition

Let:

`F: A → B`

and:

`G: B → C`

The composite mapping is:

`G ∘ F: A → C`

with:

`(G ∘ F)(a) = G(F(a))`

Composition requires both:

- mathematical type compatibility;
- semantic compatibility.

A valid codomain-domain match is insufficient if the intermediate object has the wrong scientific meaning.

## 9. Composition Order

Mapping order is part of the model semantics.

In general:

`G ∘ F ≠ F ∘ G`

where both compositions are defined.

Examples in which order may matter include:

- projection and quantization;
- filtering and classification;
- symmetry transformation and discretization;
- topology update and neighborhood extraction;
- ternary projection and state transition;
- structural classification and coarse-graining.

Mappings must not be reordered without establishing equivalence.

## 10. State Mapping

A state mapping acts on a declared state space:

`F_S: S_A → S_B`

The source and destination state spaces may be identical or different.

A state mapping must identify which components are:

- preserved;
- modified;
- created;
- removed;
- aggregated;
- invalidated.

A complete-state mapping must not silently omit a component that affects future evolution.

## 11. Coordinate Mapping

### 11.1 Definition

A coordinate mapping changes the representation of the same declared mathematical or physical state.

A generic coordinate mapping is:

`C: X_coord,A → X_coord,B`

### 11.2 Coordinate change

A coordinate change must define:

- original coordinate convention;
- target coordinate convention;
- transformation;
- inverse where available;
- singular regions;
- transformation behavior of vectors and tensors.

### 11.3 Physical-state preservation

A coordinate mapping may change numeric coordinates without changing the represented physical state.

### 11.4 Coordinate and state distinction

A coordinate change is not automatically a state transition.

## 12. Projection Mapping

A projection mapping reduces or selects information:

`P: A → B`

where `B` represents a reduced view of `A`.

A projection must declare:

- retained components;
- discarded components;
- aggregation;
- dimensional reduction;
- reconstruction limits.

Projection loss must remain explicit.

## 13. Component Projection

For composite state:

`S = X × T^N × X_G × X_H × X_F`

component projections may include:

`P_X: S → X`

`P_T: S → T^N`

`P_G: S → X_G`

`P_H: S → X_H`

`P_F: S → X_F`

Each projection extracts a declared state component without redefining its semantics.

## 14. Embedding Mapping

An embedding maps a reduced or lower-dimensional representation into a larger state representation:

`E: A → B`

An embedding must define every newly introduced component.

New values require declared provenance.

Unknown information must not be filled by undocumented defaults.

## 15. Projection–Embedding Relation

For compatible projection and embedding mappings:

`P(E(a)) = a`

may hold.

The reverse relation:

`E(P(b)) = b`

does not generally hold when projection discards information.

Therefore:

`projection`

and:

`reconstruction`

remain separate mathematical operations.

## 16. Restriction Mapping

A restriction limits a mapping to a declared subset:

`F|A₀: A₀ → B`

where:

`A₀ ⊆ A`

Restriction is used when a mathematical relation is valid only within a specific:

- parameter range;
- structural regime;
- symmetry sector;
- numerical regime;
- resonance window;
- boundary condition.

The validity subset must be stated explicitly.

## 17. Continuous-to-Continuous Mapping

A continuous mapping has the form:

`F_X: X_A → X_B`

Possible roles include:

- evolution;
- coordinate transformation;
- coupling;
- filtering;
- normalization;
- dimensional reduction;
- structural descriptor generation.

A continuous mapping must not silently produce a ternary interpretation.

## 18. Continuous-to-Ternary Mapping

The continuous-to-ternary mapping is:

`Π: X → T^N`

where:

`T = {-1, 0, 1}`

This mapping connects continuous model variables to balanced ternary state semantics.

## 19. Continuous-to-Ternary Decision Regions

For a local mapping:

`Π_i: X_i → T`

the source domain must be partitioned into declared decision regions:

`R_-1`

`R_0`

`R_1`

with:

`Π_i(x) = -1`

for:

`x ∈ R_-1`

`Π_i(x) = 0`

for:

`x ∈ R_0`

and:

`Π_i(x) = 1`

for:

`x ∈ R_1`

The boundaries and overlap rules of these regions must be explicit.

## 20. Active Neutral Region

The region mapped to `0` is an active-neutral region.

It may represent a declared condition associated with:

- balancing;
- mediation;
- damping;
- routing;
- transition staging;
- retention;
- conflict resolution.

The active-neutral region must not serve automatically as a container for:

- missing data;
- undefined states;
- invalid values;
- failed measurements.

## 21. Transition-Constrained Projection

A continuous projection may produce a requested target polarity that differs from the current ternary state.

The executed ternary state must still obey the transition relation.

For current state:

`-1`

and projected target:

`1`

the executed path is:

`-1 → 0 → 1`

For current state:

`1`

and projected target:

`-1`

the executed path is:

`1 → 0 → -1`

The projection target and executed transition path are distinct objects.

## 22. History-Dependent Ternary Mapping

When classification depends on prior state, the mapping may be:

`Π_H: X × H × T^N → T^N`

The history dependence must identify:

- required previous values;
- retained state;
- hysteresis rule;
- transition timing.

A stateful mapping must not be implemented as though it were memoryless.

## 23. Ternary-to-Continuous Mapping

A mapping from ternary state into a continuous representation may be written as:

`M_TX: T^N → X_C`

Its meaning must be model-specific.

The numeric labels:

`-1`

`0`

`1`

must not automatically be interpreted as physical amplitudes, energies, forces, or coordinates.

A physical continuous meaning requires an explicit mapping.

## 24. Ternary-Conditioned Continuous Mapping

The ternary-conditioned continuous mapping is:

`Γ: X × T^N → X`

It modifies continuous evolution according to the current ternary state.

The state `0` must have an explicitly declared action.

Possible model-specific actions may include:

- damping;
- balancing;
- retention;
- reduced excitation;
- routing;
- transition preparation.

No universal physical action is assigned by this chapter.

## 25. Bidirectional Continuous–Ternary Coupling

When both mappings are present:

`Π: X → T^N`

and:

`Γ: X × T^N → X`

the system contains bidirectional continuous–ternary coupling.

The execution contract must define the order:

`continuous state`

`→ ternary projection`

`→ transition validation`

`→ ternary update`

`→ ternary-conditioned continuous update`

or another explicitly declared order.

No hidden algebraic loop may be introduced.

## 26. Configuration Mapping

A configuration mapping acts on interatomic configuration space:

`F_Q: Q_A → Q_B`

It may represent:

- coordinate transformation;
- periodic wrapping;
- canonicalization;
- subset extraction;
- symmetry transformation;
- structural reconstruction.

A configuration mapping must preserve atomic identities unless identity transformation is explicitly part of the model.

## 27. Atomic Identity Mapping

An atomic identity mapping acts on species labels:

`F_Z: Z_A → Z_B`

Atomic identity must remain distinct from:

- position;
- local descriptor;
- node index;
- embedding vector.

A reindexing operation is not an atomic transmutation.

A descriptor change is not an atomic identity change.

## 28. Index Mapping

An index mapping changes computational labels:

`F_idx: I_A → I_B`

Reindexing may occur after:

- sorting;
- partitioning;
- graph transformation;
- serialization;
- node insertion;
- node removal.

Reindexing must preserve correspondence between all dependent state components.

## 29. Relative-Geometry Mapping

For atomic positions:

`x_i`

and:

`x_j`

the relative displacement mapping is:

`R_ij: Q → ℝ^d`

with:

`R_ij(Q) = x_j - x_i`

The associated pair-distance mapping is:

`D_ij: Q → ℝ₊`

with:

`D_ij(Q) = ||x_j - x_i||`

Boundary conventions must be included where required.

## 30. Local-Environment Mapping

A local-environment mapping extracts the declared neighborhood of site `i`:

`N_i: Q × G → X_N`

The mapping must define:

- neighborhood membership;
- geometric treatment;
- topology treatment;
- boundary conditions;
- ordering;
- included state variables;
- excluded variables.

The local environment is not identical to its encoded descriptor.

## 31. Descriptor Mapping

A descriptor mapping transforms a local environment into a mathematical representation:

`D_i: X_N → X_D`

The descriptor may contain:

- distances;
- angular relations;
- species information;
- local graph structure;
- declared continuous states.

The descriptor mapping must identify information loss.

A descriptor is a representation of the environment, not the physical environment itself.

## 32. Permutation-Invariant Local Mapping

For equivalent reorderings of local elements, a mapping may be permutation invariant.

If:

`π`

is a permitted permutation, invariance requires:

`F(πx) = F(x)`

The permitted permutation class must be defined.

Permutation invariance must not erase physically distinct atomic identities.

## 33. Permutation-Equivariant Mapping

A mapping may instead preserve ordering relations equivariantly:

`F(πx) = πF(x)`

where the output action of `π` is explicitly defined.

Invariant and equivariant permutation mappings are different constructions.

## 34. Graph Construction Mapping

A graph construction mapping creates an interaction graph from a declared configuration:

`G_C: Q → X_G`

The mapping must define:

- node construction;
- edge criterion;
- directionality;
- edge channels;
- boundary behavior;
- dynamic update conditions.

A graph edge exists because the mapping defines it.

It must not acquire additional physical meaning implicitly.

## 35. Graph-to-Local Mapping

A graph-local mapping extracts graph-dependent information for one node:

`L_i: G × S → X_local`

Possible outputs may include:

- adjacent nodes;
- edge states;
- edge weights;
- local topology;
- local interaction channels.

The mapping must preserve node correspondence.

## 36. Interaction Mapping

An interaction mapping converts relevant state information into an interaction representation:

`F_int: X_i × X_j × X_env → Y_int`

The exact domain depends on the model.

Possible dependencies may include:

- atomic identity;
- relative geometry;
- local environment;
- phase;
- amplitude;
- topology;
- delay;
- ternary state.

No dependency may remain hidden.

## 37. Pairwise Mapping

A pairwise mapping acts on two declared components:

`F_ij: X_i × X_j → Y_ij`

The mapping must define whether:

`F_ij = F_ji`

is required.

Symmetry must not be assumed from pairwise notation alone.

## 38. Many-Body Mapping

A many-body mapping depends on more than one pair relation:

`F_MB: X_local → Y_MB`

A genuinely many-body mapping must not be described as pairwise unless a reduction is derived explicitly.

## 39. Local-to-Global Aggregation Mapping

Local contributions may be combined through:

`A: {y_i} → Y`

or:

`A: {y_ij} → Y`

The aggregation rule must match the quantity semantics.

Possible aggregation structures include:

- sum;
- average;
- weighted aggregation;
- set aggregation;
- graph aggregation.

The aggregation rule must be explicit.

## 40. Energy Mapping

A model-specific energy mapping may be written as:

`E_map: S_E → ℝ`

where `S_E` is the declared state information required to evaluate energy.

The mapping must define:

- included state variables;
- units;
- reference level;
- boundary assumptions;
- decomposition where used;
- provenance.

TR-EIF does not prescribe one universal interatomic energy formula in this chapter.

## 41. Force Mapping

A model-specific force mapping may be written as:

`F_force: S_F → (ℝ^d)^N`

The mapping must define its mathematical relation to the model from which force is obtained.

A force mapping must preserve the declared transformation behavior of vectors.

No force relation is introduced without its governing mathematical definition.

## 42. Stress Mapping

A stress mapping may be written generically as:

`F_stress: S_Σ → X_Σ`

where `X_Σ` is the declared tensor-valued stress space.

The mapping must define:

- stress convention;
- coordinate convention;
- units;
- tensor transformation behavior;
- averaging volume or region where applicable.

## 43. Oscillatory-State Mapping

An oscillatory mapping extracts or constructs oscillatory variables:

`F_osc: S → X_osc`

Possible components include:

- amplitude;
- phase;
- frequency;
- mode variables;
- coupling variables.

The mapping must identify whether these quantities are:

- primitive states;
- derived states;
- estimated observables.

## 44. Phase Mapping

A phase mapping is:

`F_θ: S → 𝕊¹`

Phase must remain a circular variable.

Any numerical interval used for storage is a coordinate representation of the circular state.

## 45. Phase-Difference Mapping

For phases `θ_i` and `θ_j`:

`F_Δθ: 𝕊¹ × 𝕊¹ → 𝕊¹`

may be defined through the declared wrap convention.

Raw linear subtraction must not replace circular phase difference when periodic equivalence matters.

## 46. Frequency Mapping

A frequency mapping may be:

`F_ω: S → Ω`

The output must identify whether it represents:

- intrinsic frequency;
- instantaneous frequency;
- effective frequency;
- fitted frequency;
- external driving frequency.

These quantities are not interchangeable.

## 47. Resonance-Coordinate Mapping

A resonance-coordinate mapping projects complete state and parameters into a declared resonance space:

`P_R: S × P → X_R`

The output coordinates may include model-specific combinations of:

- frequency relations;
- phase relations;
- amplitudes;
- coupling;
- delay;
- dissipation;
- geometry;
- structural state.

Every coordinate must be defined before constructing the resonance window.

## 48. Resonance-Window Classification Mapping

For resonance space `X_R`, classification is:

`C_R: X_R → {OUTSIDE, BOUNDARY, INSIDE}`

The resonance window is:

`W_R ⊂ X_R`

Classification must define:

- boundary;
- tolerance;
- entry condition;
- exit condition;
- history dependence where present.

## 49. Resonance Classification and State Transition

The mapping:

`C_R`

does not itself perform a structural transition.

The following remain distinct:

`resonance-coordinate mapping`

`→ resonance-window classification`

`→ transition guard`

`→ structural-transition mapping`

A state may remain inside a resonance window without changing structural form.

## 50. Coherence Mapping

A coherence mapping has the generic form:

`Coh: S → Y_coh`

The specific mapping must define:

- source variables;
- relation being evaluated;
- normalization;
- spatial scope;
- temporal scope;
- output range;
- weighting.

No universal coherence formula is introduced by this chapter.

## 51. Synchronization Mapping

A synchronization mapping evaluates a declared temporal relation:

`Sync: H → Y_sync`

where history may be required to establish persistence.

Synchronization must not be inferred solely from an instantaneous state when the definition requires temporal behavior.

## 52. Structural Descriptor Mapping

A structural descriptor mapping projects state into structural state space:

`D_F: S → X_F`

Its output may represent declared structural properties such as:

- topology;
- symmetry;
- mode organization;
- phase organization;
- local-environment distribution;
- ternary-state organization.

The descriptor variables must be defined explicitly.

## 53. Structural Classification Mapping

A structural classifier maps structural descriptors into structural forms:

`C_F: X_F → F_set`

where:

`F_set`

is the declared set of structural forms.

The classification rule must define:

- structural regions;
- boundaries;
- ambiguous states;
- stabilization criteria where relevant.

## 54. Structural Region Mapping

For each form `F_k`, a membership mapping may be defined:

`M_F,k: X_F → {true, false}`

with:

`M_F,k(x) = true`

when:

`x ∈ R_F,k`

Overlapping regions require an explicit resolution rule.

## 55. Structural-Transition Mapping

A structural-transition mapping is:

`Ψ_F: R_pre × C_F → R_post`

or, when a trajectory is represented:

`Ψ_F: R_pre × C_F → Γ_tr`

where `Γ_tr` is a transition trajectory ending in a declared post-transition region.

The mapping must identify:

- trigger;
- guard;
- changed variables;
- preserved variables;
- changed topology;
- changed symmetry;
- ternary transitions;
- final stabilization condition.

## 56. Structural-Work Mapping

A structural-work mapping evaluates a declared trajectory relative to a declared form:

`W_F: Γ × F_k → X_W`

The output space `X_W` must be defined by the specific model.

No universal scalar structural-work formula is imposed here.

The mapping must identify:

- reference form;
- evaluated variables;
- sign convention;
- accumulation rule;
- units or normalization;
- interpretation.

## 57. History Mapping

A history extraction mapping is:

`H_ext: S_trajectory → X_H`

It selects the prior state information required by future evolution.

The extraction interval, resolution, and retained variables must be explicit.

## 58. History-Update Mapping

A history update mapping is:

`U_H: X_H × S_new → X_H`

It must define:

- inserted state;
- removed state;
- retained interval;
- compression;
- precision.

No hidden historical state may affect execution.

## 59. Memory Compression Mapping

A memory compression mapping is:

`C_H: X_H → X_μ`

where `X_μ` is a reduced memory-state space.

The mapping must identify:

- retained historical information;
- discarded information;
- reconstruction limitations.

A compressed memory state must not be described as full history unless equivalence is established.

## 60. Delay Mapping

For delay `τ`, the delay mapping evaluates:

`D_τ: X_H → X`

returning the state associated with:

`t - τ`

The mapping must define:

- delay value;
- interpolation;
- history boundary behavior;
- units;
- provenance.

## 61. Boundary Mapping

A boundary mapping connects external or boundary state to internal state:

`B_in: X_B × S → X`

An output boundary mapping may be:

`B_out: S → X_B,out`

Boundary mappings must identify the direction of influence.

## 62. External-Forcing Mapping

A forcing mapping may be:

`F_ext: I_t → X_B`

or:

`F_ext: I_t × P → X_B`

The forcing trajectory is part of the execution input when it affects deterministic evolution.

## 63. Symmetry Mapping

For:

`g ∈ G_sym`

a symmetry mapping acts as:

`ρ_X(g): X → X`

The action must define how the transformation affects every relevant state type.

## 64. Position Transformation Mapping

A geometric action on positions is:

`ρ_x(g): Q → Q`

It may transform coordinates while preserving declared physical equivalence.

The transformation class must be explicit.

## 65. Vector Transformation Mapping

A vector-valued state has its own transformation action:

`ρ_v(g): X_v → X_v`

A vector must not be transformed using the scalar action unless that is mathematically correct for the declared transformation.

## 66. Tensor Transformation Mapping

A tensor-valued state uses a declared tensor action:

`ρ_Σ(g): X_Σ → X_Σ`

Tensor transformation rules must match tensor order and coordinate convention.

## 67. Graph Transformation Mapping

A graph transformation mapping may act on:

- node identities;
- edge identities;
- edge weights;
- node-associated states.

A graph permutation must preserve all corresponding indexed state relations.

## 68. Ternary Transformation Mapping

A symmetry transformation does not automatically modify ternary values.

When the ternary layer transforms under a symmetry, the action must be declared explicitly:

`ρ_T(g): T^N → T^N`

The action must preserve the ternary state set and transition invariants.

## 69. Invariant Mapping

For:

`F: X → Y`

and input action:

`ρ_X(g)`

the mapping is invariant when:

`F(ρ_X(g)x) = F(x)`

for every permitted:

`g ∈ G_sym`

and:

`x ∈ X`

The transformation scope must be explicit.

## 70. Equivariant Mapping

For:

`F: X → Y`

with actions:

`ρ_X(g)`

and:

`ρ_Y(g)`

equivariance requires:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for every admissible:

`g`

and:

`x`

An equivariance statement is incomplete without both actions.

## 71. Transformation-Compatible Composition

Let:

`F: X → Y`

and:

`G: Y → Z`

If both mappings are equivariant under compatible actions, their composition may preserve the corresponding transformation structure.

The compatibility of intermediate actions must be established explicitly.

It must not be inferred from labels alone.

## 72. Mapping Between Equivalent Configurations

If:

`x₂ = ρ_X(g)x₁`

then an equivariant output relation is:

`F(x₂) = ρ_Y(g)F(x₁)`

while an invariant output relation is:

`F(x₂) = F(x₁)`

The required relation depends on output type.

## 73. Quotient Mapping

A quotient mapping sends an element to its equivalence class:

`Q_~: A → A/~`

The equivalence relation must be defined before the quotient mapping exists.

Information distinguishing elements inside one equivalence class is intentionally removed.

## 74. Canonicalization Mapping

A canonicalization mapping selects one declared representative from an equivalence class:

`C_can: A/~ → A_can`

The selection rule must be deterministic when canonicalization is used for reproducible computation.

Canonicalization and quotienting are different operations.

## 75. Fine-to-Coarse Mapping

For scale `s` and coarser scale `r`:

`M_s→r: S_s → S_r`

The mapping must define:

- source variables;
- target variables;
- aggregation;
- retained invariants;
- discarded information;
- uncertainty;
- validity domain.

## 76. Coarse-to-Fine Mapping

A downward mapping is:

`M_r→s: S_r → S_s`

It may impose:

- boundary conditions;
- constraints;
- coarse fields;
- structural information.

It does not reconstruct discarded microscopic detail automatically.

## 77. Multiscale Compatibility Mapping

For two scale representations, a compatibility mapping may compare quantities after transfer into a common representation.

The comparison domain and mapped quantities must be explicit.

Qualitative similarity is not sufficient to establish cross-scale equivalence.

## 78. Recursive Inheritance Mapping

The inheritance extraction mapping is:

`Λ_I: S_n,final → X_I`

where:

`X_I`

is the inherited-state space.

The mapping identifies which information survives from one structural cycle into the next.

## 79. Next-Cycle Initialization Mapping

The next-cycle state is constructed through:

`J_I: X_I × X_B × P → S_n+1,initial`

The mapping must identify:

- inherited state;
- new boundary conditions;
- new parameters;
- reset components;
- preserved components.

## 80. Inheritance Composition

The recursive mapping chain is:

`S_n,final`

`→ Λ_I`

`→ I_n→n+1`

`→ J_I`

`→ S_n+1,initial`

This chain must remain explicit when recursive inheritance is part of the model.

## 81. Observable Mapping

The observable mapping is:

`O: S → Y`

It projects complete state into an observable representation.

The mapping must identify:

- source state;
- observable variables;
- units;
- precision;
- sampling rule;
- uncertainty;
- omitted state information.

## 82. Local Observable Mapping

A local observable may be:

`O_i: S → Y_i`

Its spatial or graph locality must be defined.

## 83. Global Observable Mapping

A global observable may be:

`O_G: S → Y_G`

A global quantity may aggregate local states through a declared rule.

Local validity does not automatically imply global validity.

## 84. Temporal Observable Mapping

A temporal observable may depend on history:

`O_H: X_H → Y_H`

The observation window must be declared.

A temporally averaged observable must not be presented as an instantaneous value.

## 85. Measurement Mapping

A physical measurement representation may be modeled as:

`M_obs: Y_phys → Y_meas`

The measurement mapping may include declared:

- finite bandwidth;
- finite resolution;
- delay;
- calibration;
- sampling;
- quantization;
- noise.

The measurement representation remains distinct from the underlying modeled physical quantity.

## 86. Sampling Mapping

A sampling mapping converts a continuous-time signal into a discrete sequence:

`S_Δt: y(t) → {y_n}`

where:

`t_n`

is the declared sampling schedule.

Uniform sampling may use:

`t_n = t_0 + nΔt`

Nonuniform sampling requires explicit timestamps.

## 87. Quantization Mapping

A quantization mapping is:

`Q_num: A → A_q`

It must define:

- representable values;
- resolution;
- rounding;
- saturation;
- overflow;
- precision.

Quantization is not balanced ternary projection unless the codomain and ternary semantics are explicitly those of `T`.

## 88. Numerical Discretization Mapping

A continuous mathematical object may be mapped into a numerical representation:

`D_h: X → X_h`

where `h` contains declared discretization parameters.

The mapping must identify:

- temporal resolution;
- spatial resolution;
- basis or grid where applicable;
- approximation order where applicable;
- error measure;
- boundary treatment.

## 89. Numerical-to-Mathematical Interpretation Mapping

A numerical state may be interpreted as an approximation of a mathematical state through:

`I_num: X_h → X_approx`

The numerical representation and the exact mathematical object remain distinct.

Finite precision must not be erased from the interpretation.

## 90. Normalization Mapping

A normalization mapping is:

`N: A → A_norm`

It must define:

- reference value;
- scale;
- offset;
- output range;
- inverse relation where available.

Normalization must not change physical meaning silently.

## 91. Nondimensionalization Mapping

A nondimensionalization mapping converts dimensional quantities into dimensionless quantities using declared reference scales.

Every reference scale must have:

- definition;
- units;
- provenance.

The dimensional reconstruction rule must be preserved when required.

## 92. Serialization Mapping

A serialization mapping converts mathematical or computational state into a machine-readable representation:

`Ser: S_serializable → B_serial`

The serialization must preserve the semantics required by the schema.

## 93. Deserialization Mapping

A deserialization mapping is:

`Des: B_serial → S_serialized`

The relation:

`Des(Ser(S)) = S`

may be required for exactly serialized components.

When serialization is lossy, the loss must be declared.

## 94. Schema Mapping

A schema maps semantic state fields into named serialized fields.

Each schema field must identify:

- semantic source;
- data type;
- units;
- range;
- missing-value behavior;
- version.

A schema field name must not replace the mathematical definition of the quantity.

## 95. Trace Mapping

A trace mapping converts execution state and events into an ordered trace record:

`TraceMap: S × E × X_val → Trace`

The trace must preserve every event required for reconstruction of the declared execution path.

## 96. Ternary Trace Mapping

For a neutral-mediated transition:

`-1 → 0 → 1`

the trace mapping must preserve both transition legs.

A final-state-only mapping is insufficient when transition-path validity is an invariant.

## 97. Validation Mapping

A validation mapping evaluates a declared condition:

`V_k: S → X_val,k`

A validation codomain may include:

`{PASS, FAIL, NOT_EVALUATED}`

or another explicitly defined validation-state set.

A failed condition must remain distinguishable from an unevaluated condition.

## 98. Admissibility Mapping

The admissibility predicate is:

`A_S: S → {true, false}`

It determines membership in:

`S_adm`

The predicate must evaluate every required condition or identify conditions not evaluated.

## 99. Transition-Validation Mapping

A transition validator maps:

`V_T: T × T × H_T → X_val`

where `H_T` may contain required transition history.

The validator must reject:

`-1 → 1`

and:

`1 → -1`

as direct state events.

## 100. Equivariance-Validation Mapping

For mapping `F`, transformation `g`, and state `x`, an equivariance-validation mapping compares:

`F(ρ_X(g)x)`

with:

`ρ_Y(g)F(x)`

The numerical comparison rule must be declared when exact equality is not representable computationally.

## 101. Replay Mapping

A deterministic replay mapping may be written as:

`Replay: ExecutionRecord → Trace`

The execution record must contain all information required to reproduce the declared result.

Missing replay dependencies invalidate deterministic replay claims.

## 102. Error Mapping

An error mapping compares two declared representations:

`E_map: A × A_ref → X_err`

The mapping must identify:

- compared quantities;
- norm or metric;
- units;
- reference;
- normalization.

Numerical error, model discrepancy, and measurement error require separate mappings.

## 103. Uncertainty Mapping

An uncertainty mapping may transform uncertainty between spaces:

`U_F: U_A → U_B`

The mapping must define the uncertainty representation.

Possible representations include:

- intervals;
- sets;
- distributions;
- covariance structures.

Uncertainty must not be encoded implicitly as ternary state `0`.

## 104. Injective Mapping

A mapping `F: A → B` is injective when distinct admissible inputs do not map to the same output.

Injectivity matters when output is used for state reconstruction.

Injectivity must not be assumed from dimensional equality alone.

## 105. Surjective Mapping

A mapping is surjective onto its declared codomain when every codomain element has at least one admissible preimage.

A declared codomain may be larger than the actual image.

Therefore surjectivity must be established rather than presumed.

## 106. Bijective Mapping

A bijective mapping is both injective and surjective.

A bijection admits an inverse mapping over its declared domain and codomain.

Many TR-EIF projections, aggregations, quantizations, and coarse-graining mappings are not expected to be bijective.

Their invertibility must not be assumed.

## 107. Inverse Mapping

For invertible:

`F: A → B`

the inverse is:

`F^-1: B → A`

with the corresponding inverse relations.

Approximate reconstruction is not an exact inverse.

It must be defined as a separate mapping.

## 108. Partial Mapping

A partial mapping is defined only for a subset of its nominal source space.

Its domain of definition must be explicit.

An undefined result must not be replaced silently by zero or neutral ternary state.

## 109. Many-to-One Mapping

A many-to-one mapping intentionally maps several source states to one destination value.

Examples may include:

- projection;
- classification;
- aggregation;
- coarse-graining.

The resulting loss of identifiability must be recognized.

## 110. One-to-Many Relation

A deterministic mathematical mapping assigns one output to each admissible input.

When one input admits several possible outputs, the object is not an ordinary deterministic function unless an additional selection variable is included.

Such behavior may require:

- a relation;
- a stochastic mapping;
- a set-valued mapping.

The mathematical type must be declared correctly.

## 111. Set-Valued Mapping

A set-valued mapping may be written as:

`F_set: A → P(B)`

where `P(B)` denotes the set of subsets of `B`.

It may represent multiple admissible outcomes.

A set-valued mapping must not be implemented as an arbitrary single-output function without a declared selection rule.

## 112. Stochastic Mapping

A stochastic mapping returns a probability law rather than one deterministic state.

The model must define:

- stochastic variables;
- probability structure;
- distribution;
- parameters;
- random-state dependence.

Computational pseudorandomness and mathematical stochasticity remain distinct.

## 113. Time-Dependent Mapping

A time-dependent mapping is:

`F_t: A → B`

or:

`F: A × I_t → B`

Time dependence may arise from:

- external forcing;
- scheduled modulation;
- dynamic boundaries;
- changing topology;
- explicitly time-dependent parameters.

## 114. State-Dependent Mapping

A state-dependent mapping may have the form:

`F(S): A → B`

The state variables that determine the mapping must belong to the declared execution dependency.

The mapping must not change because of hidden mutable implementation state.

## 115. Parameterized Mapping

A parameterized mapping is:

`F_p: A → B`

with:

`p ∈ P`

Every parameter must have declared provenance.

The valid parameter subset must be explicit.

## 116. Continuous Mapping

When topology is defined on source and target spaces, continuity means that the mapping preserves the declared topological notion of local variation.

Continuity must not be claimed across an explicitly discrete ternary transition unless the relevant topology supports that statement.

## 117. Differentiable Mapping

A differentiable mapping requires an appropriate differentiable structure.

Differentiability must be stated only on domains where it is mathematically defined.

A hybrid mapping containing discrete events is not globally differentiable merely because its continuous branches are differentiable.

## 118. Piecewise Mapping

A mapping may be defined by different rules on distinct source regions.

A piecewise mapping must define:

- all regions;
- region boundaries;
- overlap behavior;
- boundary values;
- discontinuities.

Balanced ternary projections commonly require explicit decision regions and therefore may be piecewise-defined.

## 119. Hysteretic Mapping

A hysteretic mapping depends on both current input and prior state.

A generic form is:

`F_H: X × H → Y`

The same instantaneous input may produce different outputs for different histories.

Hysteresis must not be represented as unexplained nondeterminism.

## 120. Causal Mapping

A causal mapping at time `t` depends only on information available at or before `t`.

A mapping using future states is non-causal with respect to that time orientation.

Offline analysis mappings and real-time mappings must not be conflated.

## 121. Local Mapping

A local mapping depends on a declared local subset of the system state.

Locality may refer to:

- spatial neighborhood;
- graph neighborhood;
- finite interaction range;
- one state component;
- one scale.

The locality criterion must be explicit.

## 122. Global Mapping

A global mapping may depend on the entire represented system.

A global property must not be inferred from local mappings unless an aggregation or proof establishes the relation.

## 123. Sparse Mapping

A mapping is computationally sparse when each output depends on a restricted subset of inputs.

Computational sparsity and physical interaction locality are distinct properties.

A sparse implementation does not by itself prove short-range physical interaction.

## 124. Mapping Dimensional Consistency

A physical mapping must preserve dimensional consistency.

If a mapping combines physical quantities, the mathematical operation must respect their units.

Dimensionless normalization must occur explicitly before incompatible dimensional values are combined.

## 125. Mapping Provenance

Every nontrivial model-specific mapping must identify its provenance class.

Permitted provenance categories include:

- `PRIMARY_SOURCE`;
- `DERIVED`;
- `CALIBRATED`;
- `AUTHOR_DEFINED`;
- `BENCHMARK`;
- `TEST_FIXTURE`;
- `REQUIRES_SOURCE`;
- `REQUIRES_TEST`.

A mapping may contain parameters with different provenance classes.

Each parameter must remain individually traceable.

## 126. Mapping Failure Semantics

A mapping may fail because of:

- invalid input;
- out-of-domain state;
- missing required history;
- unsupported parameter;
- singularity;
- numerical overflow;
- invalid topology;
- failed invariant.

Failure must produce an explicit failure representation.

Failure must not be silently mapped to:

`0`

`-1`

`1`

or another valid state value.

## 127. Mapping Uncertainty Semantics

When input uncertainty affects output, the mapping must define how uncertainty is propagated or bounded.

An exact-looking scalar output must not hide an uncertain input state when uncertainty is material to interpretation.

## 128. Mapping Information Accounting

Every reduction mapping must identify whether it is:

- lossless;
- conditionally lossless;
- lossy.

A lossy mapping must identify the lost distinctions.

This applies particularly to:

- descriptors;
- observables;
- coarse-graining;
- aggregation;
- quantization;
- serialization;
- normalization where inverse reconstruction is incomplete.

## 129. Mapping Consistency Across Versions

A semantic mapping change occurs when any of the following changes:

- domain;
- codomain;
- decision region;
- transformation rule;
- threshold;
- unit convention;
- output meaning;
- retained information;
- failure behavior;
- ternary semantics.

Such a change requires corresponding version and validation impact analysis.

## 130. Mapping Compatibility

Two mappings are compatible for composition only when:

- codomain and domain types match;
- units are compatible;
- coordinate conventions are compatible;
- state semantics are compatible;
- transformation conventions are compatible;
- version semantics are compatible.

Parser compatibility alone does not establish semantic compatibility.

## 131. Mapping Equivalence

Two mappings:

`F`

and:

`G`

are equivalent only under a declared criterion and domain.

Possible criteria include:

- exact output equality;
- symmetry-equivalent output;
- bounded numerical error;
- observable equivalence;
- structural equivalence.

The equivalence criterion must be explicit.

## 132. Mathematical and Numerical Mapping Separation

A mathematical mapping and its numerical implementation are distinct objects.

The chain is:

`mathematical mapping`

`→ discretization`

`→ numerical representation`

`→ implementation`

`→ numerical output`

`→ validation against mathematical contract`

Implementation behavior must not silently redefine the mathematical mapping.

## 133. Mapping Test Requirements

A mapping test must identify:

- mapping under test;
- input domain;
- selected test states;
- expected output relation;
- boundary cases;
- invalid inputs;
- precision rule;
- invariant checks.

For ternary mappings, tests must include opposite-state requests to verify neutral mediation.

## 134. Boundary-Case Mapping Tests

Boundary cases may include:

- decision-region boundaries;
- resonance-window boundaries;
- structural-region boundaries;
- zero amplitude;
- phase wrap boundaries;
- graph topology changes;
- numerical representability limits;
- delay-history limits.

Boundary behavior must be deterministic where the mathematical contract requires determinism.

## 135. Symmetry Mapping Tests

A symmetry mapping test must verify the declared transformation relation.

For invariant mapping:

`F(ρ_X(g)x) = F(x)`

For equivariant mapping:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

Testing one transformation does not validate transformations outside the declared tested set.

## 136. Mapping Dependency Structure

The mapping dependency structure is:

`defined source space`

`→ defined target space`

`→ mapping rule`

`→ admissibility conditions`

`→ parameter provenance`

`→ transformation behavior`

`→ information accounting`

`→ failure semantics`

`→ numerical realization`

`→ validation`

No mapping may depend on a symbol, space, operator, or parameter that has not been defined.

## 137. Core TR-EIF Mapping Chain

A generic TR-EIF representation may contain the chain:

`physical configuration`

`→ configuration state`

`→ local environment`

`→ continuous dynamic representation`

`→ resonance-coordinate representation`

`→ balanced ternary projection`

`→ neutral-mediated transition`

`→ structural representation`

`→ observable projection`

`→ numerical serialization`

`→ deterministic trace`

A specific model may use only a subset of this chain.

No unused stage is implied automatically.

## 138. Continuous–Ternary Mapping Invariants

The following invariants apply:

1. The ternary codomain is exactly `{-1, 0, 1}`.

2. The canonical notation is `-1/0/1`.

3. State `0` remains active.

4. Missing data are not mapped to `0` silently.

5. Invalid data are not mapped to `0` silently.

6. Direct `-1 → 1` execution is forbidden.

7. Direct `1 → -1` execution is forbidden.

8. Opposite-polarity execution passes through `0`.

9. Projection target and executed transition path remain distinct.

10. Every decision boundary has declared provenance.

## 139. Equivariant Mapping Invariants

Every equivariant mapping must preserve:

1. declared transformation group or set;

2. declared input action;

3. declared output action;

4. declared domain;

5. declared codomain;

6. object transformation type;

7. semantic consistency under transformation.

An equivariance claim without these elements is incomplete.

## 140. Interatomic Mapping Invariants

Every interatomic mapping must preserve the distinction between:

- atomic identity;
- node index;
- position;
- local environment;
- local descriptor;
- interaction representation;
- energy output;
- force output;
- structural classification.

No one of these objects substitutes automatically for another.

## 141. Structural Mapping Invariants

Structural mappings must preserve:

1. explicit structural state variables;

2. explicit form definitions;

3. explicit pre-transition region;

4. explicit transition condition;

5. explicit post-transition region;

6. retained and broken invariants;

7. transition history where required;

8. inherited state where required.

A scalar threshold crossing alone is not a structural transition unless the model establishes that equivalence.

## 142. Multiscale Mapping Invariants

Every cross-scale mapping must identify:

- source scale;
- target scale;
- source variables;
- target variables;
- information loss;
- reconstruction assumptions;
- preserved invariants;
- validity region.

Self-similarity must not be inferred from visual resemblance.

## 143. Observable Mapping Invariants

Every observable mapping must identify:

- source state;
- output domain;
- units;
- sampling;
- precision;
- uncertainty;
- omitted information.

Observable equality does not imply full-state equality unless injectivity is established.

## 144. Trace Mapping Invariants

A conforming trace mapping must preserve:

- event order;
- state-transition order;
- neutral-mediated ternary paths;
- failure events;
- invariant states;
- version metadata;
- parameter provenance;
- execution identifiers required by the deterministic contract.

## 145. Mapping Non-Substitution Rules

The following mappings must remain distinct:

`coordinate mapping ≠ state transition`

`projection ≠ embedding`

`projection ≠ reconstruction`

`quantization ≠ ternary projection`

`descriptor mapping ≠ physical interaction`

`graph construction ≠ physical bond definition`

`energy mapping ≠ force mapping`

`resonance classification ≠ structural transition`

`coherence mapping ≠ synchronization mapping`

`symmetry mapping ≠ dynamic evolution`

`invariant mapping ≠ equivariant mapping`

`fine-to-coarse mapping ≠ exact inverse reduction`

`observable mapping ≠ full-state mapping`

`measurement mapping ≠ physical state`

`serialization mapping ≠ mathematical definition`

`validation mapping ≠ model evolution`

## 146. Mapping Conformance Requirements

A TR-EIF mathematical mapping conforms to this chapter when:

- its domain is defined;
- its codomain is defined;
- its inputs are typed;
- its outputs are typed;
- its parameter dependencies are declared;
- its units are consistent;
- its transformation behavior is declared;
- information loss is explicit;
- failure behavior is explicit;
- its relation to the TR-EIF axioms is preserved.

A TR-EIF implementation conforms when:

- implemented inputs match the mathematical domain;
- implemented outputs match the mathematical codomain;
- no hidden state modifies the mapping;
- ternary transitions preserve neutral mediation;
- numerical conversions are explicit;
- mapping order is preserved;
- versioned serialization preserves semantics;
- validation covers required boundary and invariant conditions.

## 147. Final Mathematical-Mapping Statement

TR-EIF connects its continuous, ternary, resonant, equivariant, interatomic, structural, multiscale, numerical, and observable layers only through explicitly declared mathematical mappings.

Every mapping must define:

`source space`

`→ mapping rule`

`→ target space`

`→ preserved information`

`→ discarded information`

`→ transformation behavior`

`→ admissibility`

`→ failure semantics`

`→ validation`

The balanced ternary mapping layer remains governed by:

`-1/0/1`

with active neutral mediation and forbidden direct opposite-state transitions.

The equivariant layer remains governed by explicitly declared input and output transformation actions.

The interatomic layer preserves the distinction between physical configuration and mathematical representation.

The structural layer preserves explicit transition and inheritance mappings.

The observable and numerical layers remain projections and realizations of declared model states rather than substitutes for those states.

This mapping architecture establishes the formal connections required for subsequent TR-EIF mathematical definitions and results without collapsing distinct representation layers into one semantic object.
