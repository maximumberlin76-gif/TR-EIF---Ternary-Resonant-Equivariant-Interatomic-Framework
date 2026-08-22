# Multiscale and Hierarchical Resonance

## 1. Purpose

This document defines the multiscale and hierarchical resonance layer of the Ternary Resonant Equivariant Interatomic Framework.

The chapter formalizes:

- nested scale structure;
- local, pair, cluster, supercluster, and global state;
- scale-specific resonance spaces;
- cross-scale mappings;
- hierarchical interaction distance;
- hierarchical coupling weights;
- shell-based resonance interaction;
- multiscale phase order;
- multiscale ternary composition;
- cross-scale regime transitions;
- localized perturbation propagation;
- hierarchical thermal propagation;
- dense and hierarchical computational equivalence;
- scaling semantics;
- hierarchy-preserving transformations;
- the boundary between TR hierarchy and the later EIF layer.

The central principle is:

`local organization ≠ global organization`

while allowing explicit mathematical mappings between scales.

## 2. Dependency

This chapter depends on:

- Volume 01 — Mathematical Foundations;
- `chapter_01_ternary_resonance_formalism.md`;
- `chapter_02_resonance_state_spaces_and_windows.md`;
- `chapter_03_resonance_dynamics.md`;
- `chapter_04_ternary_resonance_transition_semantics.md`;
- `chapter_05_resonance_coupling_synchronization_and_coherence.md`;
- `chapter_06_phase_oscillator_and_kuramoto_sakaguchi_module.md`;
- `chapter_07_resonance_regimes_bifurcations_and_transition_criteria.md`.

All previously established state typing, resonance-window semantics, balanced ternary invariants, and transition distinctions remain authoritative.

## 3. Scientific Status Classes

This chapter separates three layers.

### 3.1 GENERAL MATHEMATICAL STRUCTURE

Nested partitions, mappings, product spaces, phase aggregation, metrics, and hierarchical state relations.

### 3.2 TR-EIF FORMAL EXTENSION

The author-defined use of these structures for multiscale resonance, ternary state organization, and cross-scale dynamic relations.

### 3.3 FRP EXECUTABLE REFERENCE

The concrete dyadic hierarchy, weighted shell coupling, multiscale phase-order calculation, and localized propagation machinery implemented in the FRP reference realization.

FRP-specific numerical values are implementation parameters rather than universal TR-EIF constants.

## 4. Scale Index

Let:

`L = {0, 1, ..., D}`

be a finite ordered set of scale levels.

Level:

`0`

denotes the finest represented level.

Level:

`D`

denotes the global level of the current hierarchy.

Intermediate levels represent progressively coarser organizations.

## 5. Fine State

Let:

`X_0`

be the finest declared state space.

The fine state is:

`x_0 ∈ X_0`

The meaning of the fine state depends on the model.

It may represent:

- processor cells;
- oscillator domains;
- local environments;
- atoms;
- sites;
- graph nodes;
- latent equivariant states;

only when the corresponding model explicitly defines that carrier.

## 6. Scale-Specific State

For every scale:

`ell ∈ L`

define a state space:

`X_ell`

and state:

`x_ell ∈ X_ell`

Different scales need not use identical mathematical representations.

## 7. Coarse-Graining Mapping

A mapping from finer scale `ell` to coarser scale `ell + 1` is:

`A_ell: X_ell → X_ell+1`

The mapping may:

- aggregate;
- summarize;
- project;
- classify;
- construct a collective state.

Its mathematical meaning must be explicit.

## 8. Coarse-Graining Is Generally Lossy

In general:

`A_ell`

may be many-to-one.

Therefore:

`A_ell(x_a) = A_ell(x_b)`

does not imply:

`x_a = x_b`

unless injectivity is established over the declared domain.

## 9. Downward Mapping

A downward mapping may be written as:

`B_ell+1→ell: X_ell+1 → X_ell`

when such a mapping exists.

It is not automatically the inverse of:

`A_ell`

Therefore:

`B_ell+1→ell A_ell ≠ identity`

in general.

## 10. Cross-Scale Comparison Space

Two scale-specific states may be compared through a common comparison space:

`Y_cross`

using:

`M_ell: X_ell → Y_cross`

and:

`M_q: X_q → Y_cross`

A cross-scale similarity claim requires such a compatible representation or another explicitly defined relation.

## 11. Nested Partition

Let:

`V`

be a finite set of fine components.

For every scale `ell`, let:

`P_ell`

be a partition of:

`V`

A hierarchy is nested when every group in:

`P_ell`

is contained in exactly one group in:

`P_ell+1`

for every:

`ell < D`

## 12. Unique Parent

For group:

`G ∈ P_ell`

the unique containing group in:

`P_ell+1`

is its parent.

This relation defines an explicit hierarchy rather than an arbitrary collection of overlapping clusters.

## 13. Ancestor Relation

Repeated parent application defines the ancestor relation.

Every fine component therefore belongs to one unique group at every hierarchy level.

## 14. Global Group

At the global level:

`P_D`

contains one group containing all fine components.

Thus:

`|P_D| = 1`

for a complete single-root hierarchy.

## 15. Local and Global State Separation

The global state is not the same object as the set of local states.

A global mapping may discard:

- local phase offsets;
- local extremes;
- local ternary composition;
- local thermal hotspots;
- local transition history.

Therefore:

`global descriptor ≠ complete local state`

## 16. Scale-Specific Resonance Space

For scale `ell`, define:

`X_R,ell`

with resonance-coordinate state:

`r_ell ∈ X_R,ell`

The resonance-coordinate mapping is:

`P_R,ell: X_ell × P_ell → X_R,ell`

where the parameter space is declared by the model.

## 17. Scale-Specific Resonance Window

A scale-specific resonance window is:

`W_R,ell ⊂ X_R,ell`

Different scales may have different:

- coordinates;
- dimensions;
- boundaries;
- membership relations.

## 18. No Universal Cross-Scale Window Identity

In general:

`W_R,ell ≠ W_R,q`

for:

`ell ≠ q`

even if similarly named quantities are used at both scales.

## 19. Local Resonance Does Not Imply Global Resonance

The condition:

`r_0,i ∈ W_R,0,i`

for one or more local components does not establish:

`r_D ∈ W_R,D`

A global resonance criterion may depend on relations among local regions.

## 20. Global Resonance Does Not Imply Uniform Local Resonance

Likewise:

`r_D ∈ W_R,D`

does not require every local component to occupy the same local resonance state.

A global organization may contain:

- heterogeneous local states;
- phase gradients;
- local neutral states;
- distinct clusters.

## 21. Cross-Scale Resonance Mapping

A relation between scale-specific resonance states may be written as:

`M_R,ell→q: X_R,ell → X_R,q`

or into a common comparison space.

The mapping must identify:

- preserved information;
- discarded information;
- domain;
- codomain;
- transformation semantics.

## 22. Cross-Scale Consistency

A multiscale model is cross-scale consistent when its scale mappings satisfy the declared compatibility relations.

Consistency does not require numerical equality of all scale descriptors.

## 23. Cross-Scale Feedback

A model may contain:

`fine state`

`→ coarse state`

`→ coarse dynamics`

`→ downward constraint`

`→ updated fine state`

This defines a feedback architecture.

The downward relation must remain explicit.

## 24. Cross-Scale Causality

Temporal ordering between scale changes does not by itself establish causal direction.

A claim such as:

`local transition causes global transition`

requires a declared dynamic mapping supporting that relation.

## 25. FRP Dyadic Specialization

**Status: FRP EXECUTABLE REFERENCE**

The FRP reference implements an exact dyadic hierarchy.

Let:

`N = 2^D`

where:

- `N` is the number of cells;
- `D` is hierarchy depth.

The implementation requires:

`N ≥ 2`

and `N` to be a power of two.

## 26. FRP Cell Index Set

The reference cell set is:

`V = {0, 1, ..., N - 1}`

Every cell index has a binary representation of length at most:

`D`

## 27. Dyadic Groups

For level:

`ell ∈ {0, 1, ..., D}`

define group size:

`m_ell = 2^ell`

For group index:

`k`

define:

`G_ell,k = {k m_ell, ..., (k + 1)m_ell - 1}`

within the valid cell range.

## 28. Number of Groups

At level:

`ell`

the number of groups is:

`g_ell = N / 2^ell`

Therefore:

`g_0 = N`

and:

`g_D = 1`

## 29. Nested Dyadic Property

Every group:

`G_ell,k`

is contained in exactly one group at:

`ell + 1`

because the next group size is:

`2 m_ell`

Thus the FRP cell organization forms a nested dyadic hierarchy.

## 30. Pair Level

At:

`ell = 1`

group size is:

`2`

This is the pair-domain level.

## 31. Four-Cell Cluster Level

For:

`D ≥ 2`

level:

`ell = 2`

has group size:

`4`

This is the cluster level used by the FRP reference cluster analysis.

## 32. Global Level

At:

`ell = D`

the one group contains all:

`N`

cells.

Its phase-order value is the global phase-order value.

## 33. Supercluster Selection

The FRP multiscale reference selects a supercluster descriptor from:

`ell = max(1, D - 1)`

Thus the supercluster level is the penultimate hierarchy level when the hierarchy is sufficiently deep.

## 34. Coincident Named Levels

For small values of:

`D`

some named levels may coincide.

For example, a pair, cluster, or supercluster descriptor may refer to the same actual hierarchy level when no distinct intermediate level exists.

The semantic label must not create a nonexistent independent scale.

## 35. Hierarchical Distance

For two cells:

`i`

and:

`j`

define hierarchical distance:

`d_H(i,j)`

as the smallest positive hierarchy level whose group contains both cells.

For identical cells:

`d_H(i,i) = 0`

In the FRP implementation:

`d_H(i,j) = bit_length(i XOR j)`

for:

`i ≠ j`

## 36. Interpretation of Hierarchical Distance

The value:

`d_H(i,j) = 1`

means the two cells belong to the same pair.

A larger value means that their first common dyadic ancestor occurs at a coarser level.

The distance therefore measures hierarchical separation rather than Euclidean spatial distance.

## 37. Symmetry of Hierarchical Distance

Because:

`i XOR j = j XOR i`

the distance satisfies:

`d_H(i,j) = d_H(j,i)`

## 38. Identity Property

The distance satisfies:

`d_H(i,j) = 0`

if and only if:

`i = j`

under the defined cell index domain.

## 39. Strong Hierarchical Triangle Property

**Status: DERIVED**

For any cells:

`i`

`j`

and:

`k`

the dyadic hierarchical distance satisfies:

`d_H(i,k) ≤ max(d_H(i,j), d_H(j,k))`

Reason:

let:

`m = max(d_H(i,j), d_H(j,k))`

At level `m`, cells `i` and `j` belong to one group, and cells `j` and `k` belong to one group.

A nested partition gives every cell one unique group at level `m`.

Both groups contain `j`, so they are the same group.

Therefore `i` and `k` are also contained in that group, and their first common level cannot exceed `m`.

## 40. Hierarchical Shell

For cell `i` and distance:

`d ∈ {1, ..., D}`

define the shell:

`S_d(i) = {j ∈ V | d_H(i,j) = d}`

## 41. Shell Population

**Status: DERIVED**

For the dyadic hierarchy:

`|S_d(i)| = 2^(d - 1)`

for every valid:

`i`

and:

`d`

The shell is exactly the sibling half of the level-`d` group containing cell `i`.

## 42. Fractal Coupling Exponent

**Status: FRP EXECUTABLE REFERENCE**

Let:

`alpha > 0`

be the hierarchical coupling exponent.

The current FRP reference uses:

`alpha = 0.70`

This value is an implementation parameter.

It is not a universal TR-EIF constant.

## 43. Shell Normalizer

Define:

`Z_alpha = sum_(d=1..D) 1 / d^alpha`

## 44. Pair Weight by Hierarchical Distance

For:

`d ∈ {1, ..., D}`

define:

`w_d = 1 / (2^(d - 1) d^alpha Z_alpha)`

Every pair at the same hierarchical distance receives the same normalized pair weight in the current FRP specialization.

## 45. Zero Self-Coupling

The reference coupling matrix satisfies:

`W_ii = 0`

## 46. Hierarchical Coupling Matrix

For:

`i ≠ j`

define:

`W_ij = w_d_H(i,j)`

The matrix therefore depends only on hierarchical distance.

## 47. Coupling Symmetry

Because hierarchical distance is symmetric:

`W_ij = W_ji`

for the current FRP reference topology.

This symmetry belongs to the reference topology.

A general TR-EIF hierarchy is not required to use symmetric coupling.

## 48. Row Normalization

**Status: DERIVED**

For every cell `i`:

`sum_(j != i) W_ij = 1`

Proof:

`sum_(j != i) W_ij`

equals:

`sum_(d=1..D) |S_d(i)| w_d`

Substituting:

`|S_d(i)| = 2^(d - 1)`

and:

`w_d = 1 / (2^(d - 1) d^alpha Z_alpha)`

gives:

`sum_(d=1..D) 1 / (d^alpha Z_alpha) = 1`

by the definition of:

`Z_alpha`

## 49. Aggregate Shell Influence

The aggregate normalized influence of shell `d` is:

`I_d = |S_d(i)| w_d`

Therefore:

`I_d = 1 / (d^alpha Z_alpha)`

## 50. Monotone Shell Influence

For:

`alpha > 0`

the aggregate shell influence decreases strictly as:

`d`

increases.

Thus closer hierarchical shells have greater aggregate coupling weight in the FRP specialization.

## 51. Pair Weight and Shell Influence Are Different

The quantities:

`w_d`

and:

`I_d`

must not be confused.

`w_d`

is the weight of one pair.

`I_d`

is the total normalized influence of all members of shell `d`.

## 52. General Hierarchical Phase Interaction

A TR-EIF hierarchical phase field may have the form:

`F_i = sum_(j != i) K_ij sin(theta_j - theta_i - gamma_i)`

where:

`K_ij`

is a declared hierarchical coupling coefficient.

The exact structure remains model-specific.

## 53. FRP Hierarchical Phase Interaction

**Status: FRP EXECUTABLE REFERENCE**

In the current FRP phase specialization:

`F_i = K_0 sum_(j != i) W_ij h_i h_j sin(theta_j - theta_i - gamma_i)`

where:

- `K_0` is nominal coupling;
- `W_ij` is hierarchical pair weight;
- `h_i` and `h_j` are local thermal coupling factors;
- `gamma_i` is the local effective phase lag of the receiving cell.

## 54. Shell-Decomposed Field

Using hierarchical shells:

`F_i = K_0 h_i sum_(d=1..D) w_d sum_(j in S_d(i)) h_j sin(theta_j - theta_i - gamma_i)`

This form separates the interaction by hierarchy level.

## 55. Complex Shell Aggregation

For shell:

`S_d(i)`

define:

`A_i,d = sum_(j in S_d(i)) h_j cos(theta_j)`

and:

`B_i,d = sum_(j in S_d(i)) h_j sin(theta_j)`

Define:

`phi_i = theta_i + gamma_i`

## 56. Shell Projection Identity

**Status: DERIVED**

The weighted phase interaction over one shell satisfies:

`sum_(j in S_d(i)) h_j sin(theta_j - phi_i)`

equals:

`cos(phi_i) B_i,d - sin(phi_i) A_i,d`

This follows from the sine-difference identity.

## 57. Hierarchical Evaluation Form

Therefore the FRP field can be evaluated as:

`F_i = K_0 h_i sum_(d=1..D) w_d [cos(phi_i) B_i,d - sin(phi_i) A_i,d]`

This is mathematically equivalent to the corresponding dense pair sum when both use the same state and weights.

## 58. Dense and Hierarchical Paths

The FRP semantic reference contains both:

- a dense pairwise coupling path;
- a hierarchical shell-aggregation path.

They provide two computational representations of the same declared dyadic interaction relation.

## 59. Equivalence Requirement

A model claiming dense–hierarchical equivalence must verify:

- identical phase input;
- identical thermal factors;
- identical gamma state;
- identical hierarchical weights;
- numerical agreement within the declared tolerance.

Implementation names alone do not establish equivalence.

## 60. Hierarchical Evaluation Scaling

The shell hierarchy has depth:

`D = log2(N)`

A shell-based evaluation that processes every cell across all hierarchy levels therefore has declared interaction scaling:

`O(N log N)`

when shell aggregates are available through the declared hierarchical accumulation method.

This is distinct from the direct dense pair evaluation with:

`O(N^2)`

pair interactions.

## 61. Complexity Claim Boundary

An asymptotic execution claim and a measured runtime claim are different.

Therefore:

`declared O(N log N) ≠ measured hardware timing result`

A measured implementation-performance claim requires its own benchmark evidence.

## 62. Separate Thermal Hierarchy

The FRP reference uses a second hierarchical matrix for thermal propagation.

Let:

`beta > 0`

be the thermal hierarchy exponent.

The current floating reference uses:

`beta = 1.20`

This is an FRP implementation parameter.

## 63. Thermal Pair Weights

The thermal matrix is constructed through the same dyadic-distance normalization structure using exponent:

`beta`

instead of:

`alpha`

Therefore resonance coupling and thermal propagation share hierarchy geometry while retaining separate weight profiles.

## 64. Coupling Hierarchy and Thermal Hierarchy Are Distinct

Even when both use the same dyadic topology:

`W_coupling ≠ W_thermal`

in general.

Different exponents and physical roles keep the two operators distinct.

## 65. Local Thermal State

For cell `i`, let:

`T_i[n]`

denote its retained thermal state.

Let:

`T_amb`

denote the ambient reference state.

The thermal state is not a ternary state.

## 66. Local Generated Thermal Input

The FRP executable reference constructs local generated thermal input from:

- base contribution;
- current switching activity;
- retained frequency lag.

This links local discrete activity and retained frequency memory to the local thermal field.

## 67. Local Dissipation

The reference thermal dissipation term depends on:

`T_i[n] - T_amb`

and a declared thermal time constant.

Thus thermal retention and dissipation are local stateful processes.

## 68. Hierarchical Thermal Diffusion

The reference cross-cell thermal diffusion contribution has the form:

`D_i = g_diff sum_j W_thermal,ij (T_j - T_i)`

where:

`g_diff`

is the thermal diffusion gain.

This creates cross-scale thermal propagation over the same dyadic hierarchy.

## 69. Thermal Update

The reference state update has the semantic structure:

`new local heat`

`= previous local heat`

`+ generated input`

`- local dissipation`

`+ hierarchical diffusion`

with a lower bound at the declared ambient state.

## 70. Thermal Overload

The local overload state is derived relative to a declared soft thermal limit.

The overload state may then modify:

- local effective gamma;
- local coupling attenuation.

This produces feedback from local thermal hierarchy into resonant phase dynamics.

## 71. Cross-Scale Feedback Loop

The resulting reference loop contains:

`ternary switching`

`→ local thermal generation`

`→ hierarchical thermal propagation`

`→ local overload`

`→ gamma and coupling modification`

`→ phase dynamics`

`→ phase-derived ternary target`

This is a concrete multiscale feedback specialization.

## 72. Phase-Order Function

For any nonempty phase group:

`G`

with size:

`m`

define:

`R(G) = sqrt(c_G^2 + s_G^2)`

where:

`c_G = (1/m) sum_(i in G) cos(theta_i)`

and:

`s_G = (1/m) sum_(i in G) sin(theta_i)`

## 73. Scale-Level Group Phase Order

For dyadic group:

`G_ell,k`

define:

`R_ell,k = R(G_ell,k)`

with:

`0 ≤ R_ell,k ≤ 1`

## 74. Level Mean Phase Order

For:

`g_ell`

groups at level `ell`, define:

`R_mean,ell = (1/g_ell) sum_k R_ell,k`

## 75. Level Minimum

Define:

`R_min,ell = min_k R_ell,k`

## 76. Level Maximum

Define:

`R_max,ell = max_k R_ell,k`

## 77. Level Dispersion

Define:

`D_R,ell = sqrt((1/g_ell) sum_k (R_ell,k - R_mean,ell)^2)`

This measures variation of phase order among groups at the same hierarchy level.

## 78. Global-Level Identity

At:

`ell = D`

there is exactly one group.

Therefore:

`R_mean,D = R_min,D = R_max,D = R_global`

and:

`D_R,D = 0`

for the single global group.

## 79. Pair-Domain Descriptor

The FRP reference uses level:

`ell = 1`

as its pair-domain phase-order level.

Its reported pair-domain mean is:

`R_mean,1`

## 80. Cluster Descriptor

For hierarchies with at least four cells, the FRP cluster phase-order descriptor uses level:

`ell = 2`

with four-cell dyadic groups.

## 81. Supercluster Descriptor

The FRP reference uses the selected penultimate-scale level for its supercluster phase-order descriptor.

This provides an intermediate representation between local clusters and the complete global population.

## 82. Global Descriptor

The global phase-order descriptor is:

`R_global = R_D,0`

where the one level-`D` group contains every cell.

## 83. Multiscale Phase-Order State

A multiscale phase-order state may be represented as:

`R_multi = {R_ell,k | ell = 1..D}`

or through derived level statistics.

The full set contains more information than one global scalar.

## 84. Global Phase Order Does Not Reconstruct Local Order

Because aggregation is many-to-one:

`same R_global`

does not imply:

`same R_multi`

Two systems may therefore have identical global phase order and different local cluster organization.

## 85. High Local Order Does Not Guarantee High Global Order

Several internally ordered groups may have different collective phases.

Their global vector average may therefore be small even when each local:

`R_ell,k`

is large.

## 86. Low Local Minimum Is Hidden by Global Mean

A high:

`R_mean,ell`

does not guarantee a high:

`R_min,ell`

Therefore minimum and dispersion observables preserve information that the mean alone discards.

## 87. Phase Order Is Not Complete Coherence

As established in Chapter 06, the executable FRP field names may use the term:

`coherence`

for phase-order quantities.

Mathematically:

`R_ell,k`

is a phase-order magnitude.

It does not by itself define complete TR-EIF structural coherence.

## 88. Multiscale Coherence Requires Additional Definition

If a model claims multiscale structural coherence, it must define a mapping beyond the phase-order hierarchy when additional state variables are relevant.

Therefore:

`multiscale phase order ≠ complete multiscale coherence`

## 89. Multiscale Ternary State

For group:

`G_ell,k`

define ternary counts:

`n_-1(ell,k)`

`n_0(ell,k)`

`n_1(ell,k)`

where:

`n_-1 + n_0 + n_1 = |G_ell,k|`

## 90. Group Ternary Fractions

Define:

`f_-1 = n_-1 / |G|`

`f_0 = n_0 / |G|`

`f_1 = n_1 / |G|`

with:

`f_-1 + f_0 + f_1 = 1`

## 91. Active Neutral Fraction

The value:

`f_0`

measures occupancy of active neutral state:

`0`

within the declared group.

It does not measure missing data.

## 92. No Automatic Group Ternary State

A collection of local ternary states does not automatically have one group ternary state.

For example, majority voting is not part of the primitive TR-EIF ternary semantics.

Any mapping:

`T^m → T`

must be explicitly defined.

## 93. No Cancellation Assumption

The numerical sum:

`sum_i sigma_i`

does not by itself define group resonance, group coherence, or group structural state.

Opposite branch counts may cancel numerically while representing a highly structured configuration.

## 94. Multiscale Transition State

A group may contain:

- retained local states;
- first-leg neutral routes;
- pending opposite-state routes;
- completed routes.

A coarse representation must preserve whichever transition information is required by the model.

## 95. Local Transition Does Not Imply Group Transition

One cell changing:

`-1 → 0`

does not automatically change the declared group regime.

The group transition criterion must be evaluated independently.

## 96. Group Transition Does Not Require Uniform Local Transition

A group-level regime may change through collective reorganization without every local component performing the same ternary transition.

## 97. Scale-Specific Regime

For scale:

`ell`

define regime set:

`R_reg,ell`

and classifier:

`K_reg,ell`

A single execution may therefore contain different regime states at different scales.

## 98. Multiscale Regime Descriptor

A multiscale regime descriptor may contain:

- local resonance classifications;
- level phase-order means;
- level minima;
- level maxima;
- level dispersion;
- ternary fractions;
- thermal state;
- coupling state;
- topology state.

The actual descriptor must be declared by the model.

## 99. Cross-Scale Regime Transition

A transition at scale:

`ell`

and another transition at scale:

`q`

are distinct events.

A cross-scale transition claim must identify their temporal and mathematical relationship.

## 100. Local-to-Global Cascade

A model may investigate a sequence:

`local reorganization`

`→ cluster reorganization`

`→ supercluster reorganization`

`→ global reorganization`

This sequence is a candidate cascade structure.

Temporal ordering alone does not prove the causal arrows.

## 101. Global-to-Local Cascade

The reverse influence is also possible in a coupled model:

`global state`

`→ changed collective field`

`→ local dynamics`

`→ local regime change`

The governing mappings must establish this relation.

## 102. Multiscale Bifurcation Boundary

A bifurcation established at one hierarchy level does not automatically establish a bifurcation at every other level.

The scale of the analyzed dynamic object must remain explicit.

## 103. Localized Perturbation

Let:

`A ⊂ V`

be a declared active subset receiving a localized perturbation.

The perturbation may affect:

- thermal state;
- phase state;
- coupling;
- ternary requests;
- another declared variable.

## 104. Active, Adjacent, and Remote Regions

A hierarchy-aware perturbation study may distinguish:

- active group;
- adjacent group;
- remote group;
- inactive remainder.

The region definitions must follow the declared hierarchy or topology.

## 105. Propagation Observable

For a local field:

`q_i`

define group aggregate:

`Q(G)`

using a declared mean, maximum, norm, or another explicit mapping.

A propagation relation may compare:

`Q(remote)`

with:

`Q(active)`

## 106. Propagation Ratio

When the denominator is valid and nonzero, a model may define:

`rho_prop = Q(remote) / Q(active)`

This is one possible propagation observable.

It does not define universal containment by itself.

## 107. Containment Criterion

A localized-containment criterion requires a declared bound or relation.

Any numerical bound used for qualification is a model or test parameter and must retain provenance.

No universal TR-EIF containment threshold is introduced here.

## 108. FRP Localized Propagation Reference

**Status: FRP EXECUTABLE REFERENCE**

The current FRP repository contains a localized hotspot/containment analysis that records:

- active-cluster heat;
- adjacent-cluster heat;
- remote-cluster heat;
- inactive-cluster heat;
- active-cluster phase order;
- remote-cluster phase order;
- recovery behavior.

This provides a concrete implementation example of hierarchical perturbation analysis.

## 109. Scaling Reference

**Status: FRP EXECUTABLE REFERENCE**

The current FRP scaling harness exercises dyadic cell populations:

`N ∈ {8, 16, 32}`

with four-cell analysis clusters.

The scaling profiles preserve:

- hierarchy depth;
- cluster partition;
- global state reconstruction from cluster counts;
- scheduler state;
- multiscale observations.

These values define the current executable verification footprint rather than a maximum TR-EIF system size.

## 110. Scaling Range Is Not Architectural Limit

The fact that a qualification harness evaluates:

`8`

`16`

and:

`32`

cells does not imply:

`N ≤ 32`

as a mathematical TR-EIF restriction.

The formal dyadic construction applies to:

`N = 2^D`

subject to implementation resource limits and validation.

## 111. Hierarchy and Indexing

The FRP dyadic hierarchy is constructed from cell index structure.

Therefore arbitrary relabeling of cells may change hierarchical distance.

Index permutation is not automatically hierarchy-invariant.

## 112. Hierarchy-Preserving Permutation

A permutation:

`pi: V → V`

is hierarchy-preserving when it preserves the nested partition relation.

Equivalently, for the dyadic specialization it must preserve:

`d_H(pi(i), pi(j)) = d_H(i,j)`

for all:

`i`

and:

`j`

## 113. Coupling Invariance Under Hierarchy-Preserving Relabeling

Because:

`W_ij`

depends only on:

`d_H(i,j)`

a hierarchy-preserving permutation preserves the FRP hierarchical weight relation.

This is a derived symmetry of the topology model.

## 114. Arbitrary Permutation Is Not Automatically Admissible

A general permutation may map close hierarchical neighbors to remote hierarchical positions.

Therefore the dyadic reference topology is not permutation-invariant under arbitrary cell relabeling.

This boundary becomes important when connecting the TR layer to an equivariant interatomic representation.

## 115. Geometric Distance and Hierarchical Distance

The hierarchical distance:

`d_H`

is not automatically Euclidean distance.

Therefore:

`d_H(i,j) ≠ |x_i - x_j|`

in general.

A mapping is required if physical geometry is intended to determine hierarchy.

## 116. Graph Distance and Hierarchical Distance

Likewise, ordinary shortest-path graph distance and dyadic hierarchical distance are different objects unless a model establishes their relation.

## 117. Hierarchy Construction Boundary

TR-EIF does not universally require the FRP index hierarchy for all physical systems.

A general model may derive hierarchy from:

- interaction topology;
- geometry;
- local environments;
- learned equivariant representation;
- physical scale;
- another declared construction.

The hierarchy source must remain explicit.

## 118. EIF Integration Boundary

The later Equivariant Interatomic Framework must determine how an interatomic representation maps into:

- local resonance domains;
- interaction groups;
- hierarchy or graph structure;
- coupling channels;
- multiscale descriptors.

The TR layer must not invent this correspondence from cell index order.

## 119. Required EIF-to-TR Mapping

A future integrated model therefore requires an explicit relation of the form:

`equivariant interatomic state`

`→ interaction topology / hierarchy`

`→ resonance-domain state`

`→ hierarchical resonant dynamics`

## 120. Required TR-to-EIF Feedback Mapping

If feedback is present, a separate relation is required:

`resonance / ternary state`

`→ equivariant interatomic update`

This mapping must preserve the transformation semantics of the EIF state.

## 121. Equivariance Is Not Established by Hierarchy Alone

A hierarchical resonance model is not automatically:

- rotationally equivariant;
- translationally equivariant;
- permutation equivariant.

Those properties depend on how the hierarchy and its state variables transform.

## 122. Hierarchical Resonance Validation

A validator must verify at minimum:

1. hierarchy identity;

2. level count;

3. partition completeness;

4. unique group membership;

5. parent consistency;

6. state-space identity at every scale;

7. resonance-space identity at every scale;

8. cross-scale mapping identity;

9. numerical validity.

## 123. Dyadic Topology Validation

For the FRP specialization, validation must additionally verify:

- `N` is a power of two;
- `N ≥ 2`;
- `D = log2(N)`;
- group sizes are powers of two;
- every cell occurs exactly once at each level;
- hierarchical distance agrees with the dyadic partition;
- shell populations are correct.

## 124. Coupling Weight Validation

The FRP hierarchical coupling validator must verify:

- `alpha > 0`;
- diagonal weights are zero;
- matrix symmetry where the reference symmetric topology is claimed;
- row sums equal one within the declared numerical tolerance;
- shell influence decreases with hierarchical distance;
- pair weights agree with the declared formula.

## 125. Dense–Hierarchical Validation

When computational equivalence is claimed, the validator must compare dense and hierarchical coupling outputs from identical state.

A difference beyond the declared tolerance is an execution failure of the equivalence claim.

## 126. Multiscale Phase-Order Validation

Validation must verify for every level:

- group size;
- group count;
- group boundaries;
- every group phase-order value;
- level mean;
- level minimum;
- level maximum;
- level dispersion.

## 127. Ternary Composition Validation

For every group:

`n_-1 + n_0 + n_1`

must equal the number of cells in that group.

At a complete partition level, aggregated group counts must reconstruct the global ternary counts.

## 128. Thermal Hierarchy Validation

A thermal hierarchy validator must distinguish:

- local generated input;
- local retained heat;
- local dissipation;
- hierarchical diffusion;
- overload;
- coupling attenuation.

These quantities must not collapse into one generic thermal scalar when local propagation is being analyzed.

## 129. Cross-Scale Transition Validation

A claimed cross-scale transition must preserve:

- source scale;
- destination scale;
- event time or index;
- scale-specific regime definitions;
- mapping between scales;
- causal status.

## 130. Localized Perturbation Validation

A localized perturbation study must preserve:

- perturbed region;
- perturbation interval;
- active group;
- adjacent group;
- remote group;
- baseline state;
- propagation observables;
- recovery interval where applicable.

## 131. Scaling Validation

A scaling study must distinguish:

- mathematical asymptotic structure;
- algorithmic operation count;
- measured runtime;
- memory use;
- hardware resource use.

These are separate claims.

## 132. Deterministic Replay

A complete replay of a hierarchical resonance execution requires every result-affecting state, including where applicable:

- hierarchy;
- phase state;
- ternary state;
- coupling weights;
- thermal weights;
- gamma state;
- frequency-memory state;
- scheduler state;
- pending ternary routes;
- parameter state;
- pseudorandom state.

## 133. Invalid Hierarchy

An invalid or incomplete hierarchy must not be replaced silently by a flat topology.

Such fallback would change the mathematical model.

## 134. Invalid Group State

A group with missing required local states must not be assigned a valid phase-order or resonance value without an explicit missing-data rule.

## 135. Empty Group

An empty group is invalid under the nested partition defined in this chapter.

It must not be assigned:

`R = 0`

as though that were a measured phase-order state.

## 136. Failure Is Not Active Neutral

Failure of hierarchical aggregation is not balanced ternary:

`0`

The active neutral state remains a valid ternary state.

## 137. Failure Is Not Global Disorder

Failure to compute global phase order is not equivalent to a valid low global phase-order state.

## 138. Failure Is Not Containment

Failure to observe remote propagation is not sufficient evidence of physical containment when the observation itself is invalid.

## 139. Core Multiscale Invariants

The following invariants are mandatory.

1. Every scale has a declared state space.

2. Every coarse-graining mapping has a declared domain and codomain.

3. Coarse-graining is not assumed invertible.

4. Local and global states remain distinct.

5. Local and global resonance remain distinct.

6. Different scales may use different resonance spaces.

7. Cross-scale comparison requires an explicit mapping.

8. Cross-scale temporal ordering does not by itself prove causality.

9. Hierarchy groups form a valid nested partition when a nested hierarchy is claimed.

10. FRP dyadic cell count is a power of two.

11. FRP hierarchical distance remains distinct from Euclidean distance.

12. FRP shell populations follow the dyadic hierarchy.

13. Hierarchical coupling weights remain normalized.

14. Coupling hierarchy and thermal hierarchy remain separately parameterized.

15. Dense and hierarchical evaluation remain mathematically distinguishable computational paths.

16. Their equivalence must be tested when claimed.

17. Multiscale phase order remains richer than one global scalar.

18. Phase order remains distinct from complete structural coherence.

19. A group ternary composition does not automatically define one group ternary state.

20. State `0` remains active at every local ternary component.

21. Direct local `-1 → 1` remains forbidden.

22. Direct local `1 → -1` remains forbidden.

23. Coarse-graining must not hide invalid direct local transitions.

24. Local transition does not automatically imply global transition.

25. Global transition does not require uniform local transition.

26. A qualification cell count does not define a universal architecture limit.

27. Arbitrary cell permutation does not automatically preserve a dyadic hierarchy.

28. Hierarchy alone does not establish geometric equivariance.

29. Interatomic-to-hierarchy mapping belongs to the EIF integration boundary.

30. Invalid multiscale data remain distinct from valid zero-valued states.

## 140. Formal Non-Equivalences

The following non-equivalences are mandatory:

`local state ≠ global state`

`local resonance ≠ global resonance`

`local phase order ≠ global phase order`

`global phase order ≠ complete multiscale organization`

`phase-order mean ≠ phase-order minimum`

`phase-order mean ≠ phase-order dispersion`

`multiscale phase order ≠ complete structural coherence`

`coarse state ≠ fine state`

`coarse-graining ≠ invertible encoding`

`hierarchical distance ≠ Euclidean distance`

`hierarchical distance ≠ graph shortest-path distance`

`coupling hierarchy ≠ thermal hierarchy`

`pair weight ≠ aggregate shell influence`

`dense evaluation ≠ hierarchical evaluation method`

`algorithmic O(N log N) ≠ measured hardware performance`

`group ternary counts ≠ group ternary state`

`local ternary transition ≠ group regime transition`

`local regime transition ≠ global regime transition`

`temporal cascade ≠ proven causal cascade`

`localized perturbation ≠ global transition`

`low remote response ≠ physical isolation`

`hierarchy ≠ equivariance`

`cell index ≠ atomic identity`

`FRP dyadic hierarchy ≠ universal interatomic hierarchy`

## 141. Formal Multiscale Dependency Chain

The TR-EIF multiscale chain is:

`fine state`

`→ nested local organization`

`→ scale-specific aggregation`

`→ scale-specific resonance coordinates`

`→ local / cluster / global resonance classification`

`→ cross-scale relation`

`→ multiscale regime state`

`→ possible scale-specific transition`

`→ possible cross-scale feedback`

For the FRP executable specialization:

`dyadic cells`

`→ hierarchical distance`

`→ normalized shell weights`

`→ hierarchical phase coupling`

`+ hierarchical thermal propagation`

`→ tact-by-tact phase state`

`→ pair / cluster / supercluster / global phase order`

`→ phase-derived ternary targets`

`→ active-neutral -1/0/1 execution`

## 142. Minimal General Multiscale Contract

A TR-EIF multiscale model must define:

- fine component set;
- scale set;
- state space at every scale;
- partition or grouping relation;
- coarse-graining mappings;
- cross-scale comparison mappings;
- scale-specific resonance spaces;
- scale-specific resonance criteria;
- feedback relations where used;
- transition relations where used;
- validation conditions.

## 143. Minimal Hierarchical Coupling Contract

A hierarchical coupling model must additionally define:

- hierarchy topology;
- hierarchical distance or parent relation;
- shell or neighborhood structure;
- coupling weight rule;
- normalization;
- directionality;
- local parameter dependence;
- computational evaluation rule.

## 144. Minimal FRP Dyadic Reference Contract

A model claiming equivalence to the current FRP hierarchical specialization must preserve the relevant implemented semantics:

- `N = 2^D`;
- dyadic nested groups;
- XOR-derived hierarchical distance;
- shell population `2^(d - 1)`;
- normalized distance-dependent pair weights;
- zero diagonal;
- symmetric reference coupling;
- hierarchical phase aggregation;
- multiscale dyadic phase-order calculation;
- separate thermal hierarchical matrix;
- local thermal feedback into phase coupling;
- downstream balanced ternary boundary.

## 145. Conformance Requirements

A mathematical model conforms to this chapter when:

- its scales are explicitly defined;
- its hierarchy or grouping structure is explicit;
- local and global states remain separately typed;
- scale mappings are explicit;
- information loss is acknowledged where mappings are many-to-one;
- resonance windows remain scale-specific where appropriate;
- cross-scale claims use declared mappings;
- ternary semantics remain local and valid;
- multiscale aggregation does not conceal forbidden local transitions;
- hierarchy does not silently substitute for physical geometry;
- equivariance is not claimed without transformation analysis.

A computational realization conforms when:

- group membership is deterministic;
- hierarchy state is reproducible;
- hierarchical weights are reproducible;
- multiscale phase-order outputs are reproducible;
- dense/hierarchical equivalence is testable where claimed;
- cluster ternary counts reconstruct the represented population;
- local propagation observables remain traceable;
- failures remain distinct from valid neutral or zero-valued states.

## 146. Final Multiscale and Hierarchical Resonance Statement

TR-EIF represents resonant organization across multiple scales without assuming that one global quantity uniquely determines local structure.

The general architecture is:

`local state`

`→ local organization`

`→ nested groups`

`→ multiscale resonance state`

`→ cross-scale relations`

`→ global organization`

while preserving:

`local ≠ global`

and:

`coarse representation ≠ complete fine state`

The FRP executable reference provides one concrete realization through:

`N = 2^D`

`→ dyadic hierarchy`

`→ hierarchical distance`

`→ normalized fractal shell coupling`

`→ local thermal hierarchy`

`→ hierarchical phase evolution`

`→ pair / cluster / supercluster / global phase order`

`→ balanced ternary target`

The hierarchy does not itself define an interatomic representation.

That next mapping belongs to the Equivariant Interatomic Framework.

This establishes the multiscale TR boundary required before TR-EIF can connect hierarchical resonance dynamics to symmetry-aware interatomic state representations.
