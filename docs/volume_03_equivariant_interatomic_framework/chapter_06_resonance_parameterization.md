# Resonance Parameterization

## 1. Purpose

This chapter defines resonance parameterization within the Equivariant Interatomic Framework of TR-EIF.

The resonance-parameterization layer maps equivariant interatomic representations into explicitly typed resonance state.

The canonical forward chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

The resonance layer does not replace atomic geometry, graph topology, equivariant representation, physical energy, force, stress, oscillator phase, or ternary execution.

It provides the formal intermediate state connecting continuous interatomic representations to Ternary Resonance Theory.

---

## 2. Resonance State Space

Let:

`X_R`

denote the resonance state space.

A resonance state is:

`r ∈ X_R`.

The dimensionality and internal structure of:

`X_R`

are model-specific.

The space may contain:

- invariant scalar coordinates;
- equivariant vector coordinates;
- tensor coordinates;
- local resonance state;
- edge resonance state;
- cluster resonance state;
- global resonance state;
- retained resonance memory;
- resonance-window metadata.

---

## 3. Resonance Parameterization Mapping

Let:

`x_EQ ∈ X_EQ`

denote the equivariant interatomic representation.

The resonance mapping is:

`P_R: X_EQ → X_R`.

A more general mapping may be:

`P_R: X_EQ × X_G × X_conf × X_aux → X_R`.

Only result-affecting inputs belong to the concrete model.

---

## 4. Message-Passed Resonance Input

When message passing is used:

`x_EQ^[L]`

denotes the final message-passed representation.

The resonance mapping may then be:

`r = P_R(x_EQ^[L])`.

---

## 5. Local Resonance State

For atom:

`i`

define:

`r_i ∈ X_R,local`.

The local resonance state may depend on:

- local scalar features;
- vector features;
- tensor features;
- neighboring representations;
- species;
- geometry;
- retained state.

---

## 6. Edge Resonance State

For directed edge:

`j → i`

define:

`r_ij ∈ X_R,edge`.

An edge resonance state may depend on:

- pair distance;
- relative direction;
- source representation;
- receiver representation;
- message state;
- species pair;
- local environment.

---

## 7. Cluster Resonance State

For cluster:

`C_a`

define:

`r_a ∈ X_R,cluster`.

The cluster state may be produced from pooled atom and edge representations.

---

## 8. Global Resonance State

A global resonance descriptor is:

`r_G ∈ X_R,global`.

It may depend on:

- pooled node state;
- pooled edge state;
- global equivariant state;
- collective phase state;
- multiscale state.

---

## 9. Multiscale Resonance State

For scale:

`ell`

define:

`r^(ell) ∈ X_R^(ell)`.

Different scales may simultaneously occupy different resonance regimes.

---

## 10. Resonance Coordinates

A resonance state may be represented by coordinate vector:

`r = (r_1, ..., r_m)`.

The coordinates may represent different model-defined aspects of resonance.

No universal coordinate basis is imposed.

---

## 11. Scalar Resonance Coordinate

A scalar resonance coordinate:

`r_s`

is spatially invariant when:

`r_s(g · X) = r_s(X)`.

---

## 12. Vector Resonance Coordinate

A vector resonance coordinate:

`r_v`

transforms as:

`r_v(g · X) = Q r_v(X)`

under the declared spatial action.

---

## 13. Tensor Resonance Coordinate

A tensor resonance coordinate transforms according to its declared tensor representation.

---

## 14. Resonance Transformation Law

Let:

`rho_R(g)`

denote the group action on resonance state.

A symmetry-preserving resonance parameterization satisfies:

`P_R(rho_EQ(g)x) = rho_R(g) P_R(x)`.

---

## 15. Invariant Resonance Parameterization

If all resonance coordinates are scalar invariants:

`rho_R(g) = I`.

Then:

`P_R(rho_EQ(g)x) = P_R(x)`.

---

## 16. Equivariant Resonance Parameterization

If resonance state contains non-scalar channels:

`P_R(rho_EQ(g)x) = rho_R(g)P_R(x)`.

---

## 17. Permutation Behavior

Per-atom resonance state must permute consistently with atom labels.

For atom permutation:

`pi`

the local state satisfies the corresponding reindexing law.

---

## 18. Global Resonance Permutation Invariance

A global scalar resonance state intended to characterize the full atomic system is permutation invariant.

---

## 19. Resonance and Geometry

The distinction remains:

`geometry ≠ resonance`.

Atomic positions and relative vectors may determine resonance coordinates through:

`P_R`.

They are not resonance state by identity.

---

## 20. Resonance and Equivariant Representation

The distinction remains:

`equivariant representation ≠ resonance state`.

The representation is the source space.

Resonance is the mapped state.

---

## 21. Resonance and Message State

The distinction remains:

`message state ≠ resonance state`.

Messages contribute to representation evolution before resonance parameterization.

---

## 22. Resonance and Graph Topology

Graph topology may influence resonance.

It is not itself resonance.

---

## 23. Resonance and Energy

The invariant distinction remains:

`resonance classification ≠ energy`.

A resonance coordinate may enter an energy model.

It is not physical energy by identity.

---

## 24. Resonance and Force

The distinction remains:

`resonance state ≠ mechanical force`.

---

## 25. Resonance and Stress

The distinction remains:

`resonance state ≠ stress`.

---

## 26. Resonance and Ternary State

The distinction remains:

`resonance state ≠ ternary state`.

A separate mapping produces:

`-1/0/1`.

---

## 27. Resonance and Oscillator Phase

Oscillator phase:

`theta`

may contribute to resonance state.

The distinction remains:

`oscillator phase ≠ resonance`.

---

## 28. Resonance and Synchronization

The distinction remains:

`resonance ≠ synchronization`.

Synchronization may be one input to:

`P_R`.

---

## 29. Resonance and Phase Locking

The distinction remains:

`phase locking ≠ resonance`.

---

## 30. Resonance and Coherence

The distinction remains:

`coherence ≠ resonance`.

A coherence observable may become one resonance coordinate.

---

## 31. Resonance Source State

The source state for:

`P_R`

must be explicitly defined.

Possible sources include:

- node representation;
- edge representation;
- global representation;
- phase state;
- synchronization observables;
- coherence observables;
- retained history;
- material descriptors.

---

## 32. Representation-Level Parameterization

A simple local mapping may use:

`r_i = P_R(h_i)`.

---

## 33. Edge-Conditioned Parameterization

A local resonance mapping may use:

`r_i = P_R(h_i, {e_ij | j ∈ N_i})`.

---

## 34. Message-Conditioned Parameterization

A local resonance state may depend on aggregated message:

`r_i = P_R(h_i, m_i)`.

---

## 35. Global-Conditioned Parameterization

A local state may additionally depend on global representation:

`r_i = P_R(h_i, g)`.

---

## 36. Phase-Conditioned Resonance

A specialization may include oscillator phase state:

`r_i = P_R(h_i, theta_i, x_phase_aux)`.

This creates an explicit EIF-to-TR phase interface.

---

## 37. Frequency-Conditioned Resonance

Retained frequency may enter:

`P_R`.

Its role must remain separately typed from geometric or energy state.

---

## 38. Synchronization-Conditioned Resonance

A synchronization descriptor:

`s_i`

may enter:

`P_R`.

The output remains resonance state.

---

## 39. Coherence-Conditioned Resonance

A coherence descriptor:

`C_i`

or:

`C_global`

may contribute to resonance coordinates.

---

## 40. Historical Resonance State

A history-dependent resonance model may use:

`r[k+1] = F_R(x_EQ[k+1], r[k], x_M[k])`.

The retained resonance state then belongs to complete deterministic state.

---

## 41. Memoryless Resonance Parameterization

A memoryless mapping uses only current input:

`r[k] = P_R(x_EQ[k])`.

---

## 42. Resonance Memory

Resonance memory may contain:

- previous resonance coordinate;
- filtered state;
- hysteresis state;
- persistence counter;
- adaptive window state.

---

## 43. Resonance Memory versus Frequency Memory

The distinction remains:

`resonance memory ≠ retained frequency memory`.

They may coexist.

---

## 44. Resonance Memory versus Temporal Delay

The distinction remains:

`resonance memory ≠ explicit pairwise temporal delay`.

---

## 45. Resonance Parameter

A resonance parameter is a model quantity participating in:

`P_R`

or the definition of:

`X_R`.

Examples may include:

- projection coefficients;
- normalization scales;
- local coupling descriptors;
- window parameters;
- learned weights;
- material-specific coefficients.

---

## 46. Universal versus Specialized Parameters

A resonance parameter used by one model is not automatically a universal TR-EIF constant.

Its scope must remain explicit.

---

## 47. Learned Resonance Parameterization

A learnable mapping may be:

`r = P_R(x_EQ; phi_R)`.

Here:

`phi_R`

is the resonance-parameterization parameter set.

---

## 48. Analytic Resonance Parameterization

A resonance map may instead be defined analytically from geometry or physical observables.

---

## 49. Hybrid Analytic-Learned Parameterization

A model may combine:

- analytic invariant descriptors;
- learned equivariant features;
- calibrated coefficients.

---

## 50. Resonance Coordinate Normalization

A resonance coordinate may be normalized:

`r_norm = N_R(r)`.

The normalization must preserve its transformation type.

---

## 51. Scalar Resonance Normalization

A scalar resonance coordinate may use:

`r_norm = (r - mu) / sigma`

when:

`sigma ≠ 0`.

The parameters and provenance must be explicit.

---

## 52. Vector Resonance Normalization

An equivariant vector may be scaled by an invariant scalar.

Independent Cartesian normalization may break rotational equivariance.

---

## 53. Tensor Resonance Normalization

Tensor normalization must preserve the declared tensor representation.

---

## 54. Resonance Coordinate Units

Resonance coordinates may be:

- dimensionless;
- dimensional;
- normalized physical quantities;
- learned latent variables.

Units must remain explicit when physical interpretation is assigned.

---

## 55. Dimensionless Resonance Coordinate

A dimensionless resonance coordinate may be formed from ratios or normalized descriptors.

---

## 56. Dimensional Resonance Coordinate

A resonance coordinate may retain physical units if the model defines it that way.

It must not be combined additively with incompatible dimensions without an explicit mapping.

---

## 57. Resonance Descriptor

A resonance descriptor is a function:

`D_R: X_EQ → X_D,R`.

It may become part of:

`X_R`.

---

## 58. Descriptor versus Classification

The distinction is:

`resonance descriptor ≠ resonance classification`.

A descriptor may be continuous.

Classification is a separate mapping.

---

## 59. Resonance Window

A resonance window is:

`W_R ⊂ X_R`.

The boundary is:

`∂W_R`.

---

## 60. Minimal Resonance Classification

A canonical minimal classification is:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

---

## 61. Resonance Classifier

Define:

`C_R: X_R → K_R`.

The classifier determines relation to the declared resonance regime or window.

---

## 62. Resonance Class versus Ternary State

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

No automatic identification is permitted.

---

## 63. Scalar Resonance Window

For scalar:

`r`

a window may be:

`W_R = [r_min, r_max]`

under a declared boundary convention.

---

## 64. Open Resonance Window

A model may use:

`W_R = (r_min, r_max)`.

Boundary handling differs from the closed case.

---

## 65. Asymmetric Resonance Window

No symmetry around zero is required.

A window may satisfy:

`|r_min| ≠ |r_max|`.

---

## 66. Multidimensional Resonance Window

For:

`r ∈ R^m`

a window may be:

`W_R ⊂ R^m`.

Its geometry may be nonrectangular.

---

## 67. Ellipsoidal Resonance Window

A window may be defined through:

`(r - mu)^T A (r - mu) ≤ 1`

for appropriate:

`A`.

---

## 68. Polyhedral Resonance Window

A window may be defined by linear inequalities.

---

## 69. Learned Resonance Region

A learned classifier may define:

`W_R`

implicitly.

The resulting decision semantics must still be explicit at the interface level.

---

## 70. Disconnected Resonance Window

A resonance window may contain multiple disconnected components.

---

## 71. Nested Resonance Windows

A model may define nested windows:

`W_R^(1) ⊂ W_R^(2)`.

These may represent different resonance grades or regimes.

---

## 72. Scale-Dependent Resonance Window

At scale:

`ell`

define:

`W_R^(ell)`.

Different scales may use different window geometries.

---

## 73. Species-Dependent Resonance Window

A local resonance window may depend on species:

`W_R(a_i)`.

---

## 74. Pair-Dependent Resonance Window

An edge resonance window may depend on ordered or unordered species pair.

---

## 75. Environment-Dependent Resonance Window

A window may depend on local structural context.

Such dependency must be part of complete model state or deterministically derived from it.

---

## 76. Time-Dependent Resonance Window

A model may define:

`W_R(t)`.

This introduces explicit temporal dependence.

---

## 77. Adaptive Resonance Window

A window may adapt from retained model state:

`W_R[k+1] = F_W(W_R[k], x[k])`.

The adaptive state belongs to deterministic state closure.

---

## 78. Resonance Boundary

The resonance boundary:

`∂W_R`

separates interior from exterior according to the selected topology.

---

## 79. Boundary Function

A boundary may be represented implicitly by:

`B_R(r) = 0`.

---

## 80. Inside Relation

For a suitable scalar boundary function, a convention may use:

`B_R(r) < 0`

for inside.

The sign convention is model-specific.

---

## 81. Boundary Relation

`B_R(r) = 0`

indicates boundary.

---

## 82. Outside Relation

`B_R(r) > 0`

may indicate outside under the selected convention.

---

## 83. Boundary Convention

The sign convention must remain fixed across:

- documentation;
- code;
- tests;
- traces.

---

## 84. Boundary Margin

A resonance margin may quantify distance from:

`∂W_R`.

The metric must be explicit.

---

## 85. Euclidean Margin

In Euclidean resonance coordinates, one possible margin is distance to the boundary.

---

## 86. Signed Margin

A signed margin may distinguish inside from outside.

The sign convention remains model-specific.

---

## 87. Resonance Margin versus Energy

The distinction remains:

`resonance margin ≠ energy margin`.

---

## 88. Resonance Margin versus Stability Margin

Likewise:

`resonance margin ≠ stability margin`.

---

## 89. Resonance Margin versus Ternary Decision Margin

The distinction remains:

`resonance margin ≠ ternary target margin`

unless explicitly defined through the target map.

---

## 90. Resonance Entry

A resonance entry event occurs when a trajectory moves from outside to inside through the declared boundary semantics.

---

## 91. Resonance Exit

A resonance exit occurs when the trajectory moves from inside to outside.

---

## 92. Boundary Contact

Boundary contact does not necessarily imply entry or exit.

A trajectory may touch and return.

---

## 93. Boundary Residence

A trajectory may remain on or numerically near the resonance boundary over an interval.

---

## 94. Resonance Persistence

A resonance condition may be required to persist before a regime transition is registered.

---

## 95. Resonance Hysteresis

A model may use separate entry and exit conditions.

This prevents direct reversal near the same boundary.

---

## 96. Hysteresis State

The previous resonance regime becomes result-affecting state when hysteresis is used.

---

## 97. Resonance Transition

A resonance transition is a change in declared resonance regime or classification.

---

## 98. Resonance Transition versus Threshold Crossing

The distinction remains:

`resonance transition ≠ threshold crossing by identity`.

A transition may require persistence or hysteresis beyond one crossing.

---

## 99. Resonance Transition versus Bifurcation

The invariant remains:

`resonance transition ≠ bifurcation`.

---

## 100. Resonance Transition versus Ternary Transition

The invariant remains:

`resonance transition ≠ ternary transition`.

---

## 101. Resonance Transition versus Structural Transition

The invariant remains:

`resonance transition ≠ structural transition`.

---

## 102. Resonance Transition versus Physical Phase Transition

The invariant remains:

`resonance transition ≠ physical phase transition`.

---

## 103. Local Resonance Aggregation

Local resonance states:

`r_i`

may be aggregated into a global descriptor.

A mapping may be:

`A_R: {r_i} → r_G`.

---

## 104. Permutation-Invariant Resonance Aggregation

A global scalar resonance state must be invariant to atom ordering.

Sum, mean, invariant pooling, or other symmetric operators may be used.

---

## 105. Weighted Resonance Aggregation

A weighted aggregate may be:

`r_G = sum_i w_i r_i`.

The weights must preserve the required symmetry.

---

## 106. Species-Weighted Resonance Aggregation

Weights may depend on species or local environment.

---

## 107. Cluster Resonance Aggregation

Atoms may be pooled into cluster resonance state before global aggregation.

---

## 108. Hierarchical Resonance Chain

A multiscale chain may be:

`edge resonance`

`→ atom resonance`

`→ cluster resonance`

`→ supercluster resonance`

`→ global resonance`.

---

## 109. Scale Index

Every resonance state used in a multiscale model should identify its scale.

---

## 110. Cross-Scale Resonance Mapping

A map:

`M_R^(a→b): X_R^(a) → X_R^(b)`

may transfer resonance information across scales.

---

## 111. Cross-Scale Resonance Feedback

Higher-scale resonance may influence lower-scale parameterization.

This creates a feedback loop and requires explicit update ordering.

---

## 112. Multiscale Consistency

A global resonance state need not equal any local resonance state.

Different scales may occupy different regimes simultaneously.

---

## 113. Resonance Coarse Graining

Aggregation of fine-scale resonance is generally non-injective.

Fine state cannot be reconstructed from coarse resonance alone.

---

## 114. Resonance Closure State

A coarse model may require closure variables representing unresolved fine-scale resonance effects.

---

## 115. Phase Resonance Parameterization

A resonance model may incorporate oscillator phases:

`Theta = (theta_1, ..., theta_N)`.

A local or collective map may combine:

- phase differences;
- retained frequencies;
- interatomic representation;
- graph topology.

---

## 116. Phase Difference

For oscillators:

`i`

and:

`j`

define circular phase difference according to the selected wrapping convention.

This phase relation remains distinct from atomic relative orientation.

---

## 117. Kuramoto-Sakaguchi Interface

A phase coupling specialization may contain:

`sin(theta_j - theta_i - gamma_effective_i)`.

Such terms may contribute to resonance descriptors.

---

## 118. Receiving-State Phase Lag

The receiving-state lag:

`gamma_effective_i`

belongs to the phase subsystem.

It may become an input to:

`P_R`.

---

## 119. Phase Order Input

The phase-order quantity:

`R`

may enter resonance parameterization.

It remains distinct from coherence:

`R(t) ≠ C(t)`.

---

## 120. Coherence Input

A separately defined coherence state may enter:

`P_R`.

---

## 121. Synchronization Input

Synchronization observables may enter the resonance state.

---

## 122. Phase-Locking Input

Phase-locking state may likewise contribute.

---

## 123. Resonance Is Not Any One Input

No single phase, coherence, synchronization, geometry, or graph quantity defines resonance universally.

Resonance is defined through the complete declared:

`P_R`.

---

## 124. Interatomic Resonance Descriptor

An interatomic resonance descriptor may depend on:

- relative geometry;
- local equivariant state;
- species;
- message-passed environment;
- phase state;
- retained frequency;
- collective state.

---

## 125. Pair Resonance Descriptor

For edge:

`j → i`

a pair descriptor may be:

`r_ij = P_R,edge(h_i, h_j, e_ij, ...)`.

---

## 126. Local Resonance Descriptor

For atom:

`i`

a local descriptor may aggregate edge resonance contributions:

`r_i = A_R({r_ij | j ∈ N_i})`.

---

## 127. Global Resonance Descriptor

Global resonance may be produced by pooling:

`r_G = P_R,global({r_i}, g)`.

---

## 128. Anisotropic Resonance State

An anisotropic environment may require vector or tensor resonance channels.

Scalar resonance alone is not assumed sufficient.

---

## 129. Directional Resonance State

A vector resonance coordinate may encode a preferred direction derived equivariantly from geometry.

---

## 130. Tensor Resonance State

A tensor resonance coordinate may encode anisotropic local organization.

---

## 131. Scalar Resonance Classification from Tensor State

A scalar classifier may consume tensor invariants such as:

- trace;
- determinant;
- norm;
- invariant contractions.

---

## 132. Coordinate-Component Prohibition

A geometry-invariant scalar resonance classifier must not depend arbitrarily on one laboratory Cartesian component unless an external frame is part of the model.

---

## 133. Invariant Reduction

An equivariant resonance state may be reduced to invariant scalars before regime classification.

---

## 134. Resonance Feature Channel

A resonance feature channel is one component of:

`X_R`.

It may be local, edge, cluster, global, scalar, vector, or tensor.

---

## 135. Resonance Feature Multiplicity

A model may contain several resonance channels of the same representation type.

---

## 136. Resonance Feature Fusion

Compatible resonance features may be combined through transformation-preserving operations.

---

## 137. Resonance Scalar Fusion

Scalar invariant resonance channels may be combined by scalar functions.

---

## 138. Resonance Vector Fusion

Vector channels require equivariant fusion.

---

## 139. Resonance Tensor Fusion

Tensor channels require compatible tensor operations.

---

## 140. Resonance State Compression

A high-dimensional resonance state may be compressed before target generation.

The compression may be non-injective.

---

## 141. Resonance Latent State

A learned latent resonance representation may be used internally.

Its semantic role must remain distinct from physical energy or force.

---

## 142. Resonance State Expansion

A low-dimensional resonance descriptor may be expanded into a richer learned state before downstream processing.

---

## 143. Resonance Bottleneck

A resonance bottleneck may intentionally restrict the information passed toward ternary classification.

---

## 144. Resonance Information Loss

If:

`P_R`

or a later compression is non-injective, upstream interatomic state cannot be reconstructed from resonance alone.

---

## 145. Resonance-to-Ternary Mapping

Chapter 07 defines:

`P_RT: X_R → T_target`

or a more general target mapping involving additional state.

---

## 146. Ternary Target Space

The target space remains:

`T_target = {-1, 0, 1}`.

---

## 147. Resonance Class Is Not Ternary Target

A resonance class such as:

`INSIDE`

does not automatically map to:

`1`.

Likewise:

`OUTSIDE`

does not automatically map to:

`-1`.

And:

`BOUNDARY`

does not automatically map to:

`0`.

---

## 148. Explicit Target Mapping

Any relation between resonance state and ternary target must be defined through:

`P_RT`.

---

## 149. Scalar Resonance Target Mapping

A scalar resonance decision variable may use explicit thresholds.

---

## 150. Multidimensional Resonance Target Mapping

A multidimensional resonance state may use explicit decision regions:

`D_-`

`D_0`

`D_+`.

---

## 151. Learned Resonance-to-Ternary Mapping

A learned mapping may generate the exact categorical output:

`-1/0/1`.

Its decision semantics and output contract must remain explicit.

---

## 152. Active Neutral Target

A resonance-to-target mapping may produce:

`0`.

This is an active-neutral ternary target.

It is not resonance boundary by identity.

---

## 153. Target versus Executed State

The invariant remains:

`target ≠ executed state`.

Resonance parameterization ends upstream of the execution boundary.

---

## 154. Opposite Target

A resonance change may generate a target opposite to current:

`t_exec`.

This creates a routing request.

It does not directly perform the opposite transition.

---

## 155. Neutral-Mediated Execution

Committed opposite-polarity execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Resonance parameterization cannot bypass this invariant.

---

## 156. Resonance Feedback from Ternary Execution

A coupled model may use executed ternary state as an input to subsequent resonance parameterization:

`r[k+1] = P_R(x_EQ[k+1], t_exec[k], ...)`.

---

## 157. Feedback versus Identity

Ternary feedback may change resonance state.

This does not make:

`ternary state = resonance`.

---

## 158. Active Neutral Resonance Feedback

When:

`t_exec = 0`

the resonance mapping may use a distinct neutral-mode parameterization.

The output need not be numerically zero.

---

## 159. Ternary-Conditioned Resonance Family

A model may define:

`P_R^-`

`P_R^0`

`P_R^+`.

The selected mapping depends on executed ternary state.

---

## 160. Target-Conditioned Resonance

A model may instead use:

`t_target`

as an input.

Target-conditioned and execution-conditioned feedback are distinct architectures.

---

## 161. Pending-Route Resonance Feedback

A model may permit pending route state to affect resonance parameterization.

This creates another feedback channel and must be explicit.

---

## 162. Scheduler-Conditioned Resonance

Scheduler state may affect the resonance update in a specialized hybrid model.

Scheduler state remains distinct from resonance.

---

## 163. Numerical Resonance Evaluation

In discrete numerical time:

`r[n] = P_R(x_EQ[n], x_aux[n])`.

The evaluation coordinate must be explicit.

---

## 164. Pre-Update Resonance Evaluation

A model may evaluate resonance from state at:

`n`.

---

## 165. Post-Update Resonance Evaluation

Another model may evaluate from updated state:

`n+1`.

---

## 166. Resonance Update Ordering

The order relative to:

- message passing;
- target generation;
- scheduler;
- ternary commit;
- feedback

must be explicit.

---

## 167. Resonance Sampling

A model may evaluate resonance less frequently than the interatomic representation updates.

---

## 168. Resonance Sample-and-Hold

The latest resonance state may be retained between evaluation points.

---

## 169. Resonance Evaluation Rate

The resonance rate may differ from:

- molecular-dynamics timestep;
- message-passing evaluation rate;
- target rate;
- scheduler rate.

---

## 170. Multirate Resonance State

A multirate implementation must define synchronization points between resonance and other subsystems.

---

## 171. Numerical Resonance Error

Finite-precision representation and numerical transformations may introduce error into:

`r`.

---

## 172. Resonance Error Metric

An error metric must be compatible with the structure of:

`X_R`.

Scalar, vector, tensor, and categorical components require appropriate comparisons.

---

## 173. Resonance Equivariance Residual

For equivariant resonance state:

`epsilon_R(g,x) = d_R(P_R(gx), rho_R(g)P_R(x))`.

---

## 174. Resonance Invariance Residual

For scalar invariant resonance:

`epsilon_R = ||P_R(gx) - P_R(x)||`.

---

## 175. Permutation Residual

For local resonance state, atom permutation must produce corresponding reindexing.

---

## 176. Numerical Boundary Sensitivity

A resonance coordinate close to:

`∂W_R`

may change classification under small numerical perturbation.

This is boundary sensitivity.

---

## 177. Boundary Tolerance

A numerical implementation may use:

`epsilon_R`

for boundary evaluation.

The tolerance does not redefine the exact mathematical boundary.

---

## 178. Numerical Boundary Band

A finite numerical band may approximate:

`∂W_R`.

It remains a numerical construct.

---

## 179. Boundary Band versus Active Neutral

The distinction remains:

`numerical resonance boundary band ≠ ternary neutral`.

---

## 180. NaN Resonance State

A non-finite resonance coordinate is invalid numerical state.

It must not silently map to:

`0`.

---

## 181. Infinite Resonance State

Infinite values require explicit handling according to the model domain.

---

## 182. Invalid Resonance Input

If upstream representation is invalid, the resonance layer must use an explicit invalid-state path.

---

## 183. Resonance Domain Detection

A model may define:

`D_R ⊂ X_EQ`

as the domain on which its resonance map is intended to operate.

---

## 184. Out-of-Domain State

An out-of-domain representation does not automatically imply any resonance class or ternary state.

---

## 185. Uncertainty State

A resonance model may output uncertainty:

`u_R`.

This uncertainty remains distinct from:

`r`

and from ternary state.

---

## 186. Resonance Confidence

A confidence value may accompany resonance classification.

It is not resonance itself.

---

## 187. Probabilistic Resonance State

A model may represent a distribution over resonance coordinates or classes.

A later decision rule converts this distribution into a target if required.

---

## 188. Probability versus Ternary State

A probability is continuous.

It is not:

`-1/0/1`.

---

## 189. Calibration

Resonance parameters may be calibrated against reference data.

Calibrated values retain:

`CALIBRATED`

provenance.

---

## 190. Calibration Objective

A calibration objective must state:

- target observables;
- parameter set;
- loss or fitting criterion;
- reference dataset;
- parameter domain.

---

## 191. Calibration versus Learning

Calibration and learned representation optimization may overlap computationally but remain semantically distinct when their objectives and parameter roles differ.

---

## 192. Resonance Regularization

Volume 04 later introduces resonance-specific regularization during training.

This chapter defines only the resonance state and parameterization interface.

---

## 193. Resonance Parameter Identifiability

Different parameter sets may produce similar resonance outputs.

Identifiability is a model-specific property.

---

## 194. Parameter Degeneracy

A parameter degeneracy exists when distinct parameter states produce equivalent relevant outputs.

---

## 195. Gauge-Like Representation Freedom

Internal representation basis freedom may leave resonance outputs unchanged.

Such basis freedom is distinct from physical spatial symmetry.

---

## 196. Resonance Parameter Sharing

Parameters may be shared across:

- atoms;
- edges;
- species;
- clusters;
- scales.

The sharing rule must be explicit.

---

## 197. Species-Specific Resonance Parameters

A model may use:

`phi_R(a_i)`.

This permits different resonance behavior by species.

---

## 198. Pair-Specific Resonance Parameters

Edge parameters may depend on:

`(a_i, a_j)`.

---

## 199. Environment-Adaptive Resonance Parameters

A parameter may be produced from local representation:

`phi_R,i = F_phi(h_i)`.

Then parameterization becomes state-dependent.

---

## 200. Resonance Parameter versus Observable

A parameter belongs to the model definition or adaptive state.

An observable is derived from current system state.

The two must not be conflated.

---

## 201. Resonance Trace

A resonance trace may contain:

- numerical step;
- physical time;
- node/edge/cluster/global scope;
- resonance coordinates;
- resonance class;
- boundary margin;
- retained resonance state;
- uncertainty;
- provenance.

---

## 202. Minimal Resonance Trace

A minimal trace may include:

- coordinate;
- class;
- target output.

Its adequacy depends on the intended validation.

---

## 203. Full Resonance Trace

A complete diagnostic trace may include upstream feature references and all result-affecting resonance memory.

---

## 204. Resonance Trace versus Restart State

A diagnostic trace is not necessarily restart complete.

---

## 205. Restart-Complete Resonance State

If future resonance depends on retained memory, a restart artifact must preserve that memory.

---

## 206. Resonance Determinism

A deterministic resonance mapping produces identical resonance state for identical:

- complete upstream representation;
- resonance memory;
- parameters;
- ordering;
- arithmetic semantics.

---

## 207. Resonance Replay

A deterministic replay may compare resonance trajectories under identical complete inputs.

---

## 208. Exact versus Tolerance Replay

Categorical resonance class may require exact equality.

Continuous coordinates may be compared according to the declared numerical relation.

---

## 209. Resonance Validation

A resonance validator may check:

- state dimensions;
- transformation law;
- finite values;
- window definition;
- classifier consistency;
- memory update;
- deterministic replay;
- target-interface consistency.

---

## 210. Symmetry Validation

Transform the atomic configuration and verify resonance state obeys:

`rho_R(g)`.

---

## 211. Scalar Resonance Invariance Test

For invariant scalar resonance:

`r(gX) = r(X)`

within numerical tolerance.

---

## 212. Vector Resonance Equivariance Test

For vector resonance:

`r_v(gX) = Q r_v(X)`.

---

## 213. Tensor Resonance Equivariance Test

For tensor resonance:

`R_T(gX) = Q R_T(X) Q^T`.

---

## 214. Permutation Validation

Per-atom resonance states must permute consistently with atoms.

Global scalar resonance state remains invariant.

---

## 215. Window Validation

For each test coordinate, verify:

- inside classification;
- boundary classification;
- outside classification.

---

## 216. Boundary Equality Validation

Exact equality with the mathematical boundary must follow the declared classifier semantics.

---

## 217. Hysteresis Validation

A hysteresis fixture must test both entry and exit paths.

---

## 218. Persistence Validation

A persistence fixture must verify the required number of samples or duration before regime registration.

---

## 219. Multiscale Validation

Scale-specific resonance states and cross-scale mappings must be validated independently.

---

## 220. Target-Interface Validation

A resonance-to-target fixture must verify that the declared:

`P_RT`

produces exact:

`-1/0/1`.

---

## 221. Target/Execution Separation Validation

A resonance test must not assume that target generation changes executed state immediately.

---

## 222. Direct-Opposite Execution Validation

If resonance generates an opposite target, downstream execution must still preserve neutral-mediated routing.

---

## 223. Resonance Provenance

Resonance components may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 224. Primary-Source Resonance Component

A resonance relation adopted directly from established source material carries:

`PRIMARY_SOURCE`

provenance.

---

## 225. Derived Resonance Coordinate

A coordinate analytically derived from upstream representation may carry:

`DERIVED`.

---

## 226. Author-Defined Resonance Mapping

A TR-EIF-specific resonance parameterization carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 227. Calibrated Resonance Parameter

A fitted threshold, scale, coefficient, or window parameter carries:

`CALIBRATED`.

---

## 228. Benchmark Resonance Result

Measured:

- evaluation cost;
- scaling;
- numerical residual;
- replay behavior;
- target frequency

may carry:

`BENCHMARK`.

---

## 229. Resonance Test Fixture

Synthetic resonance states and expected classifications carry:

`TEST_FIXTURE`.

---

## 230. FRP Executable Reference

FRP provides executable reference behavior for selected resonance-related phase and ternary mechanisms.

FRP remains an executable specialization/reference.

It does not define the complete EIF resonance parameterization.

---

## 231. FRP Phase Input

FRP uses oscillator phase and retained frequency state in its executable reference layer.

---

## 232. FRP Phase Coupling

The phase interaction includes:

`sin(theta_j - theta_i - gamma_effective_i)`.

---

## 233. FRP Nominal Phase Lag

The FRP specialization uses:

`gamma_nominal = 0.30 pi`.

This remains FRP-specific.

---

## 234. FRP Coupling Baseline

The FRP specialization uses:

`K_0 = 0.28`.

This remains FRP-specific.

---

## 235. FRP Retained Frequency Memory

FRP retains frequency state and relaxes it toward a target frequency under its implementation-specific update rule.

---

## 236. FRP Phase Order

FRP computes:

`R = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

The distinction remains:

`R(t) ≠ C(t)`.

---

## 237. FRP Phase-to-Target Boundary

FRP maps:

`sin(theta_i)`

to ternary target using threshold magnitude:

`0.33`.

This is an executable reference specialization.

---

## 238. FRP Positive Target

The mapping includes:

`sin(theta_i) > 0.33 → 1`.

---

## 239. FRP Negative Target

The mapping includes:

`sin(theta_i) < -0.33 → -1`.

---

## 240. FRP Neutral Target

The intermediate region maps to:

`0`.

---

## 241. FRP Threshold Scope

The value:

`0.33`

is FRP-specific.

It is not a universal EIF resonance-window boundary.

---

## 242. FRP Scheduler Boundary

FRP scheduler modes:

`7/1`

and:

`1/7`

belong to downstream execution control.

They do not define resonance state.

---

## 243. FRP Neutral Routing Boundary

When an opposite target is produced, FRP preserves:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 244. FRP Reference Boundary

The relation remains:

`FRP ≠ TR-EIF`.

TR-EIF resonance parameterization generalizes the interface from equivariant interatomic state into resonance and ternary layers.

---

## 245. Resonance Parameterization Extension Rule

Any new resonance parameterization must define:

1. input state;
2. resonance state space;
3. coordinate semantics;
4. transformation law;
5. dimensional semantics;
6. memory;
7. parameters;
8. scale;
9. window or regime definition where used;
10. validation;
11. provenance.

---

## 246. Resonance Window Extension Rule

Any resonance window must define:

1. state space;
2. geometry;
3. boundary;
4. inclusion convention;
5. units;
6. scale;
7. history dependency;
8. adaptation;
9. provenance.

---

## 247. Resonance Classifier Extension Rule

Any classifier must define:

1. input resonance state;
2. class set;
3. boundary semantics;
4. hysteresis;
5. persistence;
6. invalid-state handling;
7. numerical tolerance;
8. validation.

---

## 248. Multiscale Resonance Extension Rule

Any multiscale resonance model must define:

1. scale set;
2. scale-specific resonance spaces;
3. aggregation;
4. cross-scale mappings;
5. feedback;
6. information loss;
7. update cadence;
8. validation.

---

## 249. Resonance Memory Extension Rule

Any memory mechanism must define:

1. retained state;
2. initialization;
3. update;
4. reset;
5. restart serialization;
6. relation to current resonance state;
7. validation.

---

## 250. Learned Resonance Extension Rule

Any learned resonance map must define:

1. trainable parameter set;
2. architecture;
3. symmetry constraints;
4. output state space;
5. calibration/training data;
6. target interface;
7. provenance.

---

## 251. Canonical Resonance Invariants

Every conforming resonance parameterization preserves:

1. explicit input state;

2. explicit resonance state space;

3. explicit transformation law;

4. explicit local/global/scale scope;

5. explicit window or regime semantics where used;

6. explicit memory when result-affecting;

7. explicit provenance;

8. explicit downstream target interface.

---

## 252. Canonical Symmetry Invariants

The resonance layer preserves the declared:

- spatial invariance;
- spatial equivariance;
- parity;
- atom-permutation behavior.

---

## 253. Canonical State-Separation Invariants

The framework preserves:

`geometry ≠ resonance`

`graph ≠ resonance`

`equivariant representation ≠ resonance`

`message state ≠ resonance`

`resonance ≠ synchronization`

`resonance ≠ phase locking`

`coherence ≠ resonance`

`resonance classification ≠ ternary state`

`resonance classification ≠ energy`

`resonance state ≠ force`

`resonance state ≠ stress`.

---

## 254. Canonical Transition Distinctions

The framework preserves:

`resonance-window crossing ≠ bifurcation`

`resonance transition ≠ bifurcation`

`resonance transition ≠ ternary transition`

`resonance transition ≠ structural transition`

`resonance transition ≠ physical phase transition`.

---

## 255. Canonical Ternary Boundary

The resonance layer may generate:

`t_target ∈ {-1, 0, 1}`

only through an explicit mapping.

The state:

`0`

remains active neutral.

The resonance boundary:

`BOUNDARY`

is not ternary:

`0`

by identity.

---

## 256. Canonical Execution Boundary

Resonance parameterization remains upstream of execution.

An opposite target generated from resonance must still execute through:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

---

## 257. Canonical Numerical Distinctions

The framework preserves:

`numerical boundary band ≠ resonance boundary`

`numerical resonance error ≠ ternary state`

`NaN ≠ active neutral`

`invalid resonance input ≠ 0`

`out-of-domain ≠ resonance class by identity`.

---

## 258. Canonical Scientific Distinctions

The resonance layer preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`phase lag ≠ temporal delay`

`threshold crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`.

---

## 259. Canonical Resonance Chain

The local forward chain is:

`atomic local environment`

`→ interaction graph`

`→ equivariant representation`

`→ message-passed state`

`→ resonance parameterization`

`→ local resonance state`.

---

## 260. Canonical Multiscale Resonance Chain

The multiscale chain may be:

`edge resonance`

`→ atom resonance`

`→ cluster resonance`

`→ global resonance`.

Each scale remains separately typed.

---

## 261. Canonical Ternary Integration Chain

The TR-facing chain is:

`X_EQ`

`→ X_R`

`→ P_RT`

`→ T_target`

`→ scheduler/routing`

`→ T_exec`.

---

## 262. Canonical Feedback Chain

A coupled realization may use:

`T_exec`

`→ resonance-feedback mapping`

`→ X_R,next`.

The feedback path must remain explicit.

---

## 263. Interface to Chapter 07

Chapter 07 develops Ternary Feature Channels.

It defines:

- node ternary channels;
- edge ternary channels;
- cluster ternary channels;
- global ternary channels;
- invariant decision variables;
- active-neutral channel semantics;
- target generation;
- ternary feature propagation.

The present chapter supplies the resonance state consumed by those mappings.

---

## 264. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

The energy model may consume:

- equivariant representation;
- resonance state;
- ternary feature channels.

Each remains separately typed.

---

## 265. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

Resonance-modulated energy or force mappings must preserve the symmetry and mechanical contracts defined by the EIF layer.

---

## 266. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each family member must declare:

- resonance input features;
- resonance state dimension;
- local/global/scale structure;
- memory;
- window geometry;
- classifier;
- target interface;
- resonance parameters;
- provenance.

---

## 267. Final Formal Structure

The resonance-parameterization layer may be represented as:

`RP = (X_EQ, X_R, P_R, rho_R, W_R, C_R, X_R,M, A_R)`.

Here:

- `X_EQ` is equivariant input state;
- `X_R` is resonance state;
- `P_R` is resonance parameterization;
- `rho_R` is the resonance transformation action;
- `W_R` is the resonance window or family of windows where used;
- `C_R` is resonance classification;
- `X_R,M` is retained resonance memory where used;
- `A_R` is local-to-global or cross-scale resonance aggregation.

The canonical downstream target mapping is:

`P_RT: X_R → {-1, 0, 1}`

or a declared state-augmented generalization.

---

## 268. Final Statement

Resonance parameterization is the formal bridge between equivariant interatomic representation and ternary state generation.

Atomic geometry, interaction graphs, equivariant features, message-passed state, oscillator phase, retained frequency, synchronization, coherence, and history may contribute to resonance through explicit mappings.

The resulting resonance state belongs to:

`X_R`.

It may contain:

- scalar invariant channels;
- vector equivariant channels;
- tensor channels;
- local state;
- edge state;
- cluster state;
- global state;
- multiscale state;
- retained memory.

Resonance windows and regime classifiers operate in:

`X_R`.

They do not redefine:

`-1/0/1`.

The framework preserves:

`geometry ≠ resonance`

`equivariant representation ≠ resonance`

`message passing ≠ resonance`

`resonance ≠ synchronization`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`resonance classification ≠ ternary state`

`resonance classification ≠ energy`

`resonance transition ≠ bifurcation`

`resonance transition ≠ structural transition`

`resonance transition ≠ physical phase transition`.

The exact ternary target remains downstream:

`X_R`

`→ T_target = {-1, 0, 1}`.

The state:

`0`

remains active neutral.

Any opposite target produced by the resonance layer remains subject to neutral-mediated execution:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

These definitions establish the resonance state and parameterization layer required for the Ternary Feature Channels developed in Chapter 07.
