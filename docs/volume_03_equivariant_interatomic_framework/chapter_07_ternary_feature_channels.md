# Ternary Feature Channels

## 1. Purpose

This chapter defines ternary feature channels within the Equivariant Interatomic Framework of TR-EIF.

The ternary feature layer maps selected invariant or transformation-compatible continuous and resonance representations into exact balanced ternary channels:

`-1/0/1`.

The canonical forward chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

Ternary feature channels provide discrete state information without collapsing the distinctions among:

- geometry;
- equivariant representation;
- resonance;
- target state;
- executed state;
- energy;
- force;
- stress.

---

## 2. Canonical Ternary Domain

The canonical ternary domain is:

`T = {-1, 0, 1}`.

The compact notation is:

`-1/0/1`.

No additional numerical state belongs to this domain.

---

## 3. Active Neutral State

The state:

`0`

is active neutral.

It may represent framework-defined operations such as:

- mediation;
- balancing;
- retention;
- routing;
- controlled neutralization;
- transition staging.

It is not:

- missing data;
- invalid state;
- padding;
- mask value;
- numerical zero by identity;
- absence of interaction.

---

## 4. Ternary Feature Space

Let:

`X_T`

denote a ternary feature space.

For:

`M`

channels:

`X_T = {-1, 0, 1}^M`.

A feature vector is:

`t = (t_1, ..., t_M)`.

---

## 5. Local Ternary Feature

For atom:

`i`

define:

`t_i ∈ X_T,local`.

The local feature may contain one or multiple ternary channels.

---

## 6. Edge Ternary Feature

For directed edge:

`j → i`

define:

`t_ij ∈ X_T,edge`.

An edge ternary feature is associated with an interaction relation.

It is not edge presence by identity.

---

## 7. Cluster Ternary Feature

For cluster:

`C_a`

define:

`t_a ∈ X_T,cluster`.

---

## 8. Global Ternary Feature

A complete system may contain:

`t_G ∈ X_T,global`.

Global ternary state must be defined through an explicit aggregation or classification rule.

---

## 9. Multiscale Ternary State

For scale:

`ell`

define:

`t^(ell) ∈ X_T^(ell)`.

Different scales may hold different ternary states simultaneously.

---

## 10. Source State

A ternary feature may be generated from:

- invariant equivariant-representation channels;
- resonance state;
- synchronization descriptors;
- coherence descriptors;
- local environment state;
- multiscale state;
- retained memory;
- explicitly declared control state.

---

## 11. Ternary Mapping

The canonical feature map is:

`P_T: X_source → {-1, 0, 1}`.

For multiple channels:

`P_T: X_source → {-1, 0, 1}^M`.

---

## 12. Resonance-to-Ternary Mapping

A principal TR-EIF mapping is:

`P_RT: X_R → T_target`.

A state-augmented version may be:

`P_RT: X_R × X_M × X_aux → T_target`.

---

## 13. Exact Output

The output of a ternary classifier is exactly one of:

`-1`

`0`

`1`.

There is no approximate ternary semantic state.

---

## 14. Continuous Source

A continuous decision variable may be:

`z ∈ R`.

A scalar mapping may use threshold:

`eta > 0`.

---

## 15. Canonical Scalar Threshold Form

One valid ternary map is:

`z < -eta → -1`

`-eta ≤ z ≤ eta → 0`

`z > eta → 1`.

Boundary equality semantics must remain explicit.

---

## 16. Asymmetric Thresholds

A model may instead define:

`eta_-`

and:

`eta_+`

with:

`eta_- < eta_+`.

Then:

`z < eta_- → -1`

`eta_- ≤ z ≤ eta_+ → 0`

`z > eta_+ → 1`.

Symmetry around zero is not required.

---

## 17. Multidimensional Decision Space

For:

`z ∈ R^m`

define regions:

`D_-`

`D_0`

`D_+`.

The ternary map is:

`z ∈ D_- → -1`

`z ∈ D_0 → 0`

`z ∈ D_+ → 1`.

---

## 18. Decision Partition

A complete deterministic classifier requires the declared admissible domain to be partitioned consistently among its outcome regions or to define explicit boundary handling.

---

## 19. Decision Surface

A boundary between decision regions is a target-classification boundary.

It is not automatically:

- a resonance boundary;
- a bifurcation boundary;
- a structural-transition boundary;
- a physical phase-transition boundary.

---

## 20. Resonance Boundary and Ternary Boundary

The distinction remains:

`resonance boundary ≠ ternary decision boundary`

unless an explicit mapping identifies them.

---

## 21. Resonance Class and Ternary State

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

A resonance class must be mapped explicitly into a ternary target if used for that purpose.

---

## 22. Boundary Is Not Neutral by Identity

The relation:

`BOUNDARY`

does not imply:

`0`.

Active neutral is a ternary semantic state.

Boundary is a classification relation in another state space.

---

## 23. Invariant Decision Variable

A scalar ternary channel intended to remain unchanged under rigid spatial transformation should be generated from an invariant decision variable.

---

## 24. Vector Source

If source feature:

`v`

is equivariant:

`v → Qv`,

a scalar ternary decision may use an invariant reduction such as:

`||v||`.

---

## 25. Dot-Product Decision

A scalar decision may use:

`u · v`

for compatible equivariant vectors.

This quantity is invariant under orthogonal spatial transformations.

---

## 26. Tensor-Invariant Decision

A tensor source may be reduced through invariant quantities such as:

- trace;
- determinant;
- norm;
- invariant contractions.

---

## 27. Cartesian-Component Decision

A decision based directly on one laboratory Cartesian component is not rotationally invariant unless the corresponding external frame belongs to the model state.

---

## 28. Spatial Transformation of Scalar Ternary Channel

A scalar ternary channel satisfies:

`t(g · X) = t(X)`

under the declared rigid spatial symmetry.

---

## 29. Ternary Polarity and Spatial Rotation

Rigid spatial rotation does not imply:

`-1 ↔ 1`.

The signs:

`-1`

and:

`1`

belong to ternary semantics.

They are not spatial directions by identity.

---

## 30. Ternary Polarity and Reflection

Reflection does not automatically exchange ternary polarity.

Any such transformation requires an explicit channel-specific definition.

---

## 31. Zero Vector versus Ternary Neutral

The distinction is:

`zero vector ≠ ternary 0`.

A zero representation feature may map to any ternary state according to:

`P_T`.

---

## 32. Zero Scalar versus Ternary Neutral

Likewise:

`numerical scalar 0 ≠ ternary neutral 0`

unless explicitly defined by the target map.

---

## 33. Missing State

Missing data belongs to a separate state space.

It must not be silently encoded as:

`0`.

---

## 34. Invalid State

Invalid input belongs to a validation or error state.

The invariant remains:

`INVALID ≠ 0`.

---

## 35. Mask State

A binary mask value:

`0`

is not active neutral.

---

## 36. Padding State

A padding value:

`0`

is not active neutral.

---

## 37. None State

`NONE`

is not:

`0`.

This distinction is mandatory for pending-route and optional-state representations.

---

## 38. Ternary Target

A generated ternary feature intended for execution may be registered as:

`t_target ∈ {-1, 0, 1}`.

---

## 39. Target versus Feature

Not every ternary feature must become an execution target.

A ternary feature may remain:

- latent;
- local;
- edge-level;
- energy-conditioning state;
- message-conditioning state.

---

## 40. Target Projection

A feature-to-target map may be:

`P_FT: X_T → T_target`.

This mapping must be explicit when local or multichannel features are reduced to an execution target.

---

## 41. Executed State

The committed execution state is:

`t_exec ∈ {-1, 0, 1}`.

---

## 42. Target versus Executed State

The invariant remains:

`target ≠ executed state`.

A target change is upstream of committed execution.

---

## 43. Ternary Feature versus Executed State

Likewise:

`ternary feature ≠ executed state`

unless that specific channel is explicitly defined as the retained execution channel.

---

## 44. Direct Target Reversal

A target may change:

`-1 → 1`

or:

`1 → -1`

between evaluations.

This is permitted at the target layer.

---

## 45. Direct Executed Reversal

Committed execution may not perform:

`-1 → 1`

or:

`1 → -1`.

---

## 46. Canonical Opposite Route

Opposite-polarity committed execution requires:

`-1 → 0 → 1`

or:

`1 → 0 → -1`.

---

## 47. First Execution Leg

The first leg is:

`-1 → 0`

or:

`1 → 0`.

---

## 48. Pending Destination

After the first leg, the opposite destination may be stored as:

`t_pending ∈ {-1, 1}`.

---

## 49. Neutral Residence

While a pending route is active:

`t_exec = 0`.

The neutral state may persist for multiple execution opportunities.

---

## 50. Second Execution Leg

The second leg is:

`0 → 1`

or:

`0 → -1`.

---

## 51. Ternary Feature Layer Boundary

The feature layer produces ternary information.

The scheduler and routing layers determine committed state transition.

The feature layer therefore cannot bypass execution semantics.

---

## 52. Node Ternary Target

A node may have:

`t_target,i`.

This target may be generated independently for each atom or computational cell.

---

## 53. Node Executed State

A local executed state may be:

`t_exec,i`.

Each local state preserves the canonical transition topology.

---

## 54. Vector Ternary State

For:

`N`

entities:

`t_exec_vec ∈ {-1, 0, 1}^N`.

---

## 55. Local Direct-Opposite Exclusion

For every entity:

`i`

the consecutive committed pair must never be:

`(-1, 1)`

or:

`(1, -1)`.

---

## 56. Edge Ternary Channel

An edge may carry:

`t_ij ∈ {-1, 0, 1}`.

This is separate from:

- edge mask;
- edge type;
- edge direction;
- edge weight;
- edge resonance class.

---

## 57. Edge Presence versus Ternary State

The distinction remains:

`edge presence ≠ ternary edge state`.

An edge may exist while:

`t_ij = -1`

`t_ij = 0`

or:

`t_ij = 1`.

---

## 58. Edge Absence

An absent edge does not automatically correspond to:

`t_ij = 0`.

There is no ternary feature when the edge is outside the declared feature domain unless the model explicitly creates one.

---

## 59. Ternary Edge Channel and Chemical Bond

The invariant remains:

`ternary edge feature ≠ chemical bond`.

---

## 60. Ternary Edge Channel and Force

The invariant remains:

`ternary edge feature ≠ mechanical force`.

---

## 61. Local Ternary Feature Generation

A local target may be generated from local resonance:

`t_i = P_RT(r_i)`.

---

## 62. Edge Ternary Feature Generation

An edge feature may be:

`t_ij = P_RT,edge(r_ij)`.

---

## 63. Cluster Ternary Feature Generation

A cluster feature may be:

`t_a = P_RT,cluster(r_a)`.

---

## 64. Global Ternary Feature Generation

A global feature may be:

`t_G = P_RT,global(r_G)`.

---

## 65. Multichannel Feature State

A node may carry:

`t_i = (t_i,1, ..., t_i,M)`.

Each channel must have its own semantic definition.

---

## 66. Channel Identity

Two ternary channels may share the same numeric domain while representing different semantics.

The numeric values alone do not identify the channel.

---

## 67. Channel Metadata

Each ternary channel should define:

- scope;
- source;
- target semantics;
- thresholds or decision regions;
- memory;
- update cadence;
- symmetry behavior;
- provenance.

---

## 68. Independent Channels

Two ternary channels may evolve independently.

Their states need not be equal.

---

## 69. Coupled Channels

A model may couple multiple ternary channels through an explicit update rule.

---

## 70. Channel Aggregation

Multiple local ternary features may be aggregated into another target through:

`A_T`.

The aggregation must be explicitly defined.

---

## 71. Majority Aggregation

A possible aggregation may use majority state.

Tie handling must be explicit.

---

## 72. Weighted Aggregation

A weighted decision may first construct a continuous score from ternary inputs and then reclassify into:

`-1/0/1`.

---

## 73. Sum of Ternary Inputs

The arithmetic sum of ternary values is generally not itself ternary.

For example:

`1 + 1 = 2`.

A reclassification or saturation rule is required if the result must return to:

`T`.

---

## 74. Ternary Arithmetic versus Ternary Semantics

Arithmetic on the numerical encodings must not silently redefine semantic state transitions.

---

## 75. Ternary Product

The numeric product of two ternary values remains in:

`{-1,0,1}`.

However, its semantic interpretation still requires an explicit operator definition.

---

## 76. Ternary Negation

Numeric negation maps:

`-1 ↔ 1`

and:

`0 → 0`.

This algebraic operation is not the same as committed execution from one polarity to the other.

---

## 77. Algebraic Negation versus Execution Transition

The distinction is:

`numeric ternary negation ≠ direct committed polarity reversal`.

A computed target may be negated instantly.

Executed state remains constrained by routing.

---

## 78. Ternary Channel Update

A feature channel may update:

`t_feature[k+1] = F_T(t_feature[k], x[k])`.

If previous feature state affects the update, the channel contains memory.

---

## 79. Memoryless Feature

A memoryless classifier is:

`t_feature[k] = P_T(x[k])`.

---

## 80. Stateful Feature

A stateful classifier may use:

`t_feature[k+1] = F_T(x[k+1], t_feature[k], x_M[k])`.

---

## 81. Hysteresis

A ternary classifier may use separate transition boundaries depending on current state.

This produces hysteresis.

---

## 82. Hysteresis State

The previous ternary feature value becomes result-affecting state when hysteresis is used.

---

## 83. Persistence

A ternary state change may require a decision condition to persist for:

- several samples;
- several numerical steps;
- several execution tacts;
- a physical-time interval.

---

## 84. Persistence Counter

A persistence counter:

`n_persist`

belongs to complete state when it affects target generation.

---

## 85. Debounce

A classifier may use a debounce rule before registering a new target.

Debounce is a target-generation mechanism.

It is not active-neutral routing.

---

## 86. Target Hysteresis versus Neutral Routing

The distinction remains:

`ternary classifier hysteresis ≠ neutral routing`.

---

## 87. Target Persistence versus Neutral Residence

The distinction remains:

`target persistence ≠ executed neutral residence`.

---

## 88. Target State Machine

A target classifier may itself be a finite-state machine over:

`-1/0/1`.

This is upstream target state.

It remains distinct from execution state machine.

---

## 89. Execution State Machine

The execution state machine preserves:

`-1 ↔ 0 ↔ 1`.

Its transition semantics are defined by the execution layer.

---

## 90. Two Ternary State Machines

A system may therefore contain:

- target state machine;
- executed state machine.

They may temporarily disagree.

---

## 91. Target Lag

The executed state may lag the target because of:

- scheduler cadence;
- capacity;
- pending routing;
- neutral residence.

---

## 92. Target Chatter

The target may change rapidly near a decision boundary.

---

## 93. Execution Chatter

Executed-state switching is constrained by the neutral-mediated transition graph.

Target chatter and execution chatter are distinct.

---

## 94. Ternary Feature and Message Passing

A ternary feature may condition message passing.

A message family may be:

`M_-1`

`M_0`

`M_1`.

---

## 95. Ternary-Gated Message

A simple map may use:

`m'_ij = t_i m_ij`.

This is one specialization.

---

## 96. Neutral Message Operator

A richer model may define:

`m'_ij = M_0(m_ij, x_i)`

when:

`t_i = 0`.

Therefore active neutral need not imply zero message.

---

## 97. Ternary-Conditioned Node Update

A node-update family may be:

`U_-1`

`U_0`

`U_1`.

---

## 98. Ternary-Conditioned Edge Update

Edge representations may likewise use ternary-conditioned update operators.

---

## 99. Ternary-Conditioned Resonance

Executed or target ternary state may feed back into resonance parameterization.

The exact source channel must be declared.

---

## 100. Target-Conditioned Feedback

Using:

`t_target`

creates one feedback architecture.

---

## 101. Execution-Conditioned Feedback

Using:

`t_exec`

creates a different feedback architecture.

The two must not be conflated.

---

## 102. Pending-Conditioned Feedback

A pending destination may also participate in a feedback mapping.

It remains separately typed.

---

## 103. Ternary Feature and Energy

An energy functional may depend on ternary features:

`E = F_E(X_EQ, X_R, X_T)`.

---

## 104. Ternary State Is Not Energy

The invariant remains:

`ternary state ≠ energy`.

The ternary channel is an input to the energy mapping.

---

## 105. Ternary-Conditioned Energy

A model may define mode-specific energy terms:

`E_-1`

`E_0`

`E_1`.

The complete functional must remain scalar invariant.

---

## 106. Continuous Ternary Conditioning

A ternary state may parameterize continuous model coefficients.

This does not turn the discrete state into the resulting physical quantity.

---

## 107. Ternary Feature and Force

Force may depend indirectly on ternary features through the energy functional.

---

## 108. Direct Ternary-Conditioned Force

A direct equivariant force mapping may also consume ternary channels.

Such a model must separately define conservativity if required.

---

## 109. Ternary State Is Not Force

The distinction remains:

`ternary state ≠ mechanical force`.

---

## 110. Ternary Feature and Stress

Stress may depend on ternary-conditioned energy or direct tensor outputs.

The ternary feature itself is not stress.

---

## 111. Differentiability Boundary

A hard ternary classifier is discontinuous at decision boundaries.

This matters when gradients are propagated through:

`P_T`.

---

## 112. Hard Classification

A hard classifier outputs exact:

`-1/0/1`.

---

## 113. Soft Surrogate

Training may use a continuous surrogate before hard classification.

The surrogate state is not the ternary state.

---

## 114. Soft versus Hard State

The distinction is:

`continuous surrogate ≠ exact ternary feature`.

---

## 115. Straight-Through Estimation Boundary

A training implementation may use a straight-through or related estimator for gradient propagation.

The forward semantic state remains exact ternary when the hard output is used.

---

## 116. Probabilistic Ternary State

A model may predict probabilities:

`p_-`

`p_0`

`p_+`.

These probabilities belong to a continuous simplex.

---

## 117. Probability-to-Ternary Decision

A decision map:

`D_P`

converts probabilities into exact ternary state.

---

## 118. Probability Is Not Ternary State

The distinction remains:

`probability distribution ≠ ternary state`.

---

## 119. Logits

Raw logits are continuous model outputs.

They are not ternary state.

---

## 120. Ternary Confidence

A classifier may attach confidence to a ternary target.

Confidence remains separate metadata.

---

## 121. Uncertainty

Uncertainty may accompany a ternary decision.

It is not active neutral.

---

## 122. Out-of-Domain State

An out-of-domain flag must remain distinct from:

`-1/0/1`.

---

## 123. Abstention

If a model supports abstention, abstention must use a separate state.

It must not be silently mapped to:

`0`.

---

## 124. Invalid Decision

A failed classifier produces an explicit invalid result rather than active neutral.

---

## 125. Numerical Threshold Evaluation

Finite precision may influence target classification near boundaries.

The numerical comparison semantics must be explicit.

---

## 126. Boundary Tolerance

A numerical implementation may use:

`epsilon_T`.

This tolerance belongs to numerical decision handling.

It does not redefine the semantic ternary domain.

---

## 127. Exact Categorical Output

After numerical classification:

`t ∈ {-1,0,1}`

exactly.

---

## 128. NaN Input

A:

`NaN`

decision variable requires explicit invalid handling.

It must not default to:

`0`.

---

## 129. Infinite Input

Infinite decision values require an explicitly defined domain rule.

---

## 130. Feature Quantization

Quantizing a continuous representation into finite numeric levels is not automatically ternary semantic classification.

---

## 131. Ternary Encoding

A machine representation may encode:

`-1`

`0`

`1`

using bits or integers.

Encoding remains distinct from semantic state.

---

## 132. Reserved Encoding

Unused machine encodings must remain invalid or reserved according to the schema.

---

## 133. Reserved State versus Neutral

A reserved code must not decode silently as:

`0`.

---

## 134. Serialization

A ternary feature artifact must preserve:

- channel identity;
- scope;
- value;
- source;
- target/execution role;
- time or step coordinate where applicable.

---

## 135. Ternary Schema

A schema must restrict valid semantic values to:

`-1`

`0`

`1`.

Optional absence must be represented separately.

---

## 136. Local Ternary Trace

A local trace may contain:

- atom identifier;
- source resonance state;
- target;
- executed state;
- pending destination;
- step;
- scheduler state.

---

## 137. Edge Ternary Trace

An edge trace may contain:

- source node;
- receiver node;
- ternary edge channel;
- resonance source;
- graph coordinate.

---

## 138. Multiscale Ternary Trace

A multiscale trace must identify the scale of each ternary channel.

---

## 139. Target Trace

A target trace may include direct opposite changes.

This is valid upstream behavior.

---

## 140. Execution Trace

An execution trace must preserve neutral mediation for opposite polarity.

---

## 141. Pending Trace

A pending trace must distinguish:

`NONE`

from:

`0`.

---

## 142. Deterministic Ternary Mapping

A deterministic classifier produces identical ternary output for identical:

- complete source state;
- classifier state;
- parameters;
- numerical comparison semantics.

---

## 143. Ternary Replay

A deterministic replay must reproduce exact categorical outputs.

---

## 144. Target Replay

Target replay should compare:

`t_target`

exactly.

---

## 145. Execution Replay

Execution replay should compare:

`t_exec`

and:

`t_pending`

exactly.

---

## 146. Continuous-Upstream Replay

If continuous upstream values are compared within tolerance, the resulting categorical target must still satisfy the declared replay contract.

---

## 147. Decision-Boundary Replay Sensitivity

Tiny floating-point differences near a classification boundary may produce different categorical outputs.

Deterministic replay therefore requires controlled arithmetic and comparison semantics where exact target replay is required.

---

## 148. Ternary Validation

A validator must verify every semantic ternary value belongs to:

`{-1, 0, 1}`.

---

## 149. Invalid-Encoding Validation

Any machine value outside the declared encoding must be rejected.

---

## 150. Source Mapping Validation

Controlled source states should verify expected:

`-1`

`0`

`1`

outputs.

---

## 151. Boundary Validation

Tests must cover:

- below negative threshold;
- negative boundary;
- neutral region;
- positive boundary;
- above positive threshold.

---

## 152. Multidimensional Region Validation

For multidimensional mappings, fixtures must cover every decision region and shared boundary.

---

## 153. Symmetry Validation

For spatially invariant ternary channels:

`t(gX) = t(X)`.

---

## 154. Permutation Validation

Per-atom ternary channels must permute consistently with atom indexing.

Global ternary channels remain permutation invariant when defined as global scalar categories.

---

## 155. Reflection Validation

Reflection must leave a scalar invariant ternary channel unchanged unless another transformation law is explicitly declared.

---

## 156. Active-Neutral Validation

Tests must verify that:

`0`

is handled as a valid semantic state rather than missing or invalid data.

---

## 157. Target/Execution Validation

Tests must preserve separate fields for:

`t_target`

and:

`t_exec`.

---

## 158. Direct-Opposite Validation

For every executed-state trace, reject direct:

`-1 → 1`

and:

`1 → -1`.

---

## 159. First-Leg Validation

An opposite target must first produce executed:

`0`

when a state-changing commit is authorized.

---

## 160. Pending Validation

The pending destination must preserve the intended opposite state after first-leg commit.

---

## 161. Second-Leg Validation

The second leg must begin from:

`0`.

---

## 162. Neutral-Retention Validation

A pending route may remain:

`0`

for multiple execution opportunities.

---

## 163. Hysteresis Validation

A stateful target classifier must be tested along both increasing and decreasing decision trajectories.

---

## 164. Persistence Validation

The target must change only after the declared persistence condition is satisfied.

---

## 165. Invalid-State Validation

Tests must verify:

`INVALID`

`NONE`

`NaN`

`MASKED`

`PADDED`

do not become ternary:

`0`.

---

## 166. Energy Interface Validation

When energy depends on ternary features, the final energy must retain its declared scalar symmetry and units.

---

## 167. Force Interface Validation

When force depends on ternary-conditioned state, force must retain vector equivariance.

---

## 168. Stress Interface Validation

Stress must retain its tensor transformation law.

---

## 169. Differentiable Training Validation

When surrogate gradients are used, tests must distinguish:

- forward hard ternary state;
- backward surrogate behavior.

---

## 170. Ternary Provenance

Ternary feature definitions and artifacts may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 171. Author-Defined Ternary Semantics

The balanced ternary active-neutral execution semantics of TR-EIF carry:

`AUTHOR_DEFINED`

provenance within the framework architecture.

---

## 172. Derived Ternary Feature

A ternary feature produced deterministically from a declared resonance state may carry:

`DERIVED`

provenance for the resulting artifact.

---

## 173. Calibrated Threshold

A target threshold obtained from calibration carries:

`CALIBRATED`

provenance.

---

## 174. Primary-Source Decision Relation

A decision relation adopted directly from an external scientific source carries:

`PRIMARY_SOURCE`

provenance.

---

## 175. Benchmark Ternary Result

Measured transition counts, channel occupancy, throughput, or replay results may carry:

`BENCHMARK`.

---

## 176. Test Fixture

Controlled ternary trajectories carry:

`TEST_FIXTURE`.

---

## 177. FRP Executable Reference

FRP provides executable reference behavior for selected ternary target and execution semantics used by TR-EIF.

FRP remains an executable specialization/reference.

---

## 178. FRP Ternary Kernel

The FRP kernel is exactly:

`-1/0/1`.

---

## 179. FRP Active Neutral

The FRP state:

`0`

is active and participates in opposite-polarity execution.

---

## 180. FRP Phase-to-Target Source

FRP uses:

`sin(theta_i)`

as the decision variable for its executable phase-to-target mapping.

---

## 181. FRP Threshold

The FRP specialization uses threshold magnitude:

`0.33`.

---

## 182. FRP Positive Target

The mapping includes:

`sin(theta_i) > 0.33 → 1`.

---

## 183. FRP Negative Target

The mapping includes:

`sin(theta_i) < -0.33 → -1`.

---

## 184. FRP Neutral Target

The intermediate region maps to:

`0`.

---

## 185. FRP Threshold Scope

The value:

`0.33`

is specific to the FRP executable specialization.

It is not a universal TR-EIF ternary threshold.

---

## 186. FRP Target Registration

The generated target is registered upstream of execution.

It does not immediately replace retained executed state.

---

## 187. FRP Opposite Target

When target is opposite to current executed state, FRP uses staged active-neutral routing.

---

## 188. FRP First Leg

The first leg is:

`-1 → 0`

or:

`1 → 0`.

---

## 189. FRP Pending State

The opposite destination is retained as pending state.

---

## 190. FRP Second Leg

The route later completes:

`0 → 1`

or:

`0 → -1`.

---

## 191. FRP Scheduler Modes

FRP execution includes:

`7/1`

and:

`1/7`

scheduler modes.

---

## 192. FRP Scheduler Scope

The scheduler modes regulate execution timing.

They do not redefine ternary semantics.

---

## 193. FRP Direct-Transition Invariant

Applicable qualified FRP execution artifacts preserve:

`actual_direct_events = 0`.

---

## 194. FRP Reserved-State Invariant

Applicable qualified artifacts preserve:

`reserved_state_events = 0`.

---

## 195. FRP Queue Invariant

The applicable qualified configuration preserves:

`queue_overflow_events = 0`.

---

## 196. FRP Reference Boundary

The relation remains:

`FRP ≠ TR-EIF`.

FRP supplies executable reference behavior for selected ternary mechanisms.

EIF supplies the broader atomic, graph, equivariant, resonance, energy, force, stress, learning, and multiscale layers.

---

## 197. Ternary Feature Extension Rule

Any new ternary feature must define:

1. scope;
2. source state;
3. channel semantics;
4. decision mapping;
5. symmetry behavior;
6. memory;
7. update cadence;
8. target or latent role;
9. validation;
10. provenance.

---

## 198. Threshold Extension Rule

Any threshold classifier must define:

1. decision variable;
2. units;
3. negative threshold;
4. positive threshold;
5. equality semantics;
6. invalid-input handling;
7. numerical tolerance;
8. provenance.

---

## 199. Multidimensional Mapping Extension Rule

Any multidimensional ternary classifier must define:

1. source space;
2. `D_-`;
3. `D_0`;
4. `D_+`;
5. shared boundaries;
6. overlap resolution;
7. out-of-domain handling.

---

## 200. Stateful Classifier Extension Rule

Any stateful ternary classifier must define:

1. retained state;
2. initialization;
3. hysteresis;
4. persistence;
5. reset;
6. restart state;
7. deterministic update order.

---

## 201. Multiscale Ternary Extension Rule

Any multiscale ternary system must define:

1. scale set;
2. scale-specific source states;
3. scale-specific ternary channels;
4. aggregation;
5. cross-scale feedback;
6. update ordering.

---

## 202. Ternary-Conditioned Energy Extension Rule

Any energy functional using ternary state must define:

1. source ternary channel;
2. target or executed state usage;
3. energy coupling;
4. symmetry;
5. dimensional semantics;
6. differentiability behavior.

---

## 203. Ternary-Conditioned Message Extension Rule

Any message operator using ternary state must define:

1. source channel;
2. `-1` behavior;
3. `0` behavior;
4. `1` behavior;
5. source/receiver scope;
6. update order;
7. feedback path.

---

## 204. Canonical Ternary Feature Invariants

Every conforming ternary feature layer preserves:

1. exact state set `{-1,0,1}`;

2. active neutral `0`;

3. explicit channel semantics;

4. explicit source mapping;

5. explicit target/execution distinction;

6. explicit invalid-state separation;

7. explicit symmetry behavior;

8. explicit provenance.

---

## 205. Canonical Active-Neutral Invariants

The framework preserves:

`0 ≠ NONE`

`0 ≠ INVALID`

`0 ≠ NaN`

`0 ≠ MASKED`

`0 ≠ PADDING`

`0 ≠ zero vector`

`0 ≠ zero message`

unless a specific explicit mapping defines a relation.

---

## 206. Canonical Execution Invariants

Committed execution preserves:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 207. Canonical Opposite Routes

The only canonical opposite-polarity routes are:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

First and second legs remain distinct commits.

---

## 208. Canonical Target Invariants

The target may change directly between opposite polarities.

The execution state may not.

This preserves:

`target transition ≠ executed transition`.

---

## 209. Canonical State-Separation Invariants

The framework preserves:

`equivariant representation ≠ ternary feature`

`resonance state ≠ ternary feature`

`resonance class ≠ ternary state`

`ternary feature ≠ executed state`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`

`graph mask ≠ ternary neutral`

`edge presence ≠ ternary edge state`.

---

## 210. Canonical Scientific Distinctions

The ternary feature layer preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`resonance transition ≠ ternary transition`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`spatial rotation ≠ ternary polarity reversal`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`.

---

## 211. Canonical Forward Feature Chain

The canonical local chain is:

`equivariant local representation`

`→ local resonance state`

`→ invariant decision variable`

`→ ternary feature`.

---

## 212. Canonical Global Feature Chain

The global chain may be:

`local resonance states`

`→ permutation-invariant aggregation`

`→ global resonance state`

`→ global ternary feature`.

---

## 213. Canonical Execution Chain

For execution-bound channels:

`resonance`

`→ ternary target`

`→ target registration`

`→ scheduler`

`→ request handling`

`→ neutral routing`

`→ committed ternary state`.

---

## 214. Canonical Feedback Chain

A committed or target ternary channel may feed back through an explicitly defined mapping:

`X_T`

`→ message / resonance / energy conditioning`

`→ next continuous interatomic state`.

---

## 215. Interface to Chapter 08

Chapter 08 develops the Conservative Energy Functional.

It defines how:

- equivariant representations;
- resonance state;
- ternary feature channels

enter an invariant scalar energy model.

The present chapter establishes the exact categorical state and its semantic boundaries.

---

## 216. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

Ternary-conditioned energy or direct output models must preserve:

- force equivariance;
- stress tensor transformation;
- energy/force dimensional semantics;
- conservative relations where declared.

---

## 217. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each family member must declare:

- ternary feature scope;
- source features;
- resonance-to-ternary mapping;
- target channels;
- executed channels;
- hysteresis;
- persistence;
- scheduler interface;
- feedback role;
- energy-conditioning role.

---

## 218. Final Formal Structure

The ternary feature layer may be represented as:

`TF = (X_source, X_T, P_T, X_M,T, A_T, P_FT, rho_T)`.

Here:

- `X_source` is the selected continuous, equivariant, or resonance source state;
- `X_T` is the ternary feature state space;
- `P_T` is the ternary classification mapping;
- `X_M,T` is optional retained classifier memory;
- `A_T` is optional ternary aggregation;
- `P_FT` maps feature channels into execution targets where required;
- `rho_T` is the declared transformation action on ternary channels.

For canonical scalar channels:

`rho_T(g)t = t`.

The semantic domain remains:

`{-1,0,1}`.

---

## 219. Final Statement

Ternary feature channels form the exact discrete interface between resonance/equivariant state and downstream interatomic control and execution layers.

Every canonical ternary feature belongs exactly to:

`-1/0/1`.

The state:

`0`

is active neutral.

It is not missing data, invalid state, graph mask, padding, zero vector, zero message, or absent interaction by identity.

Ternary features may exist at:

- edge level;
- atomic level;
- cluster level;
- global level;
- multiple scales.

They may condition:

- message passing;
- resonance parameterization;
- energy;
- forces;
- stress;
- downstream execution targets.

The framework preserves:

`resonance state ≠ ternary state`

`resonance class ≠ ternary state`

`ternary feature ≠ executed state`

`target ≠ executed state`

`edge presence ≠ ternary edge state`

`zero representation ≠ active neutral`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`.

For execution-bound channels, opposite target polarity remains subject to the canonical routes:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

No feature mapping, symmetry transform, learned classifier, energy model, graph message, or numerical tolerance may bypass the active-neutral execution invariant.

These definitions establish the ternary feature layer required for the Conservative Energy Functional developed in Chapter 08.
