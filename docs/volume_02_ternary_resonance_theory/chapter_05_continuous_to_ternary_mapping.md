# Continuous-to-Ternary Mapping

## 1. Purpose

This chapter defines the continuous-to-ternary mapping layer of Ternary Resonance Theory.

The layer converts continuous, resonance-derived, synchronization-derived, coherence-derived, or other explicitly typed upstream state into a balanced ternary target:

`T_target = {-1, 0, 1}`.

The chapter formalizes:

- source state spaces;
- continuous decision coordinates;
- scalar and multidimensional decision boundaries;
- threshold mappings;
- window mappings;
- hysteretic mappings;
- history-dependent mappings;
- state-dependent mappings;
- probabilistic mappings;
- target persistence;
- target recomputation;
- target provenance;
- numerical realization;
- validation;
- separation between ternary target and executed ternary state.

The canonical chain is:

`continuous state`

`→ resonance or decision representation`

`→ ternary target`

`→ neutral-mediated ternary execution`.

Target generation does not itself perform committed execution.

---

## 2. Continuous Source Space

Let:

`X_C`

be the continuous source state space.

An element:

`x_C ∈ X_C`

may contain:

- oscillator phase;
- frequency;
- resonance coordinates;
- synchronization observables;
- coherence observables;
- continuous control state;
- geometric descriptors;
- multiscale descriptors;
- material-dependent variables.

The exact contents of:

`X_C`

are model-specific.

---

## 3. Target Space

The ternary target space is:

`T_target = {-1, 0, 1}`.

The canonical notation is:

`-1/0/1`.

Each target is exact after classification.

No fourth target state belongs to:

`T_target`.

---

## 4. Mapping Definition

The continuous-to-ternary mapping is:

`P_CT: X_C → T_target`.

For:

`x_C ∈ X_C`

the resulting target is:

`t_target = P_CT(x_C)`.

The mapping is discrete-valued even when the source space is continuous.

---

## 5. Extended Mapping Definition

A more general mapping may depend on auxiliary state:

`P_CT: X_C × X_aux → T_target`.

The auxiliary state may include:

- previous target;
- executed ternary state;
- history;
- hysteresis state;
- scale;
- topology;
- scheduler-visible state;
- model parameters.

Every result-affecting dependency must be explicit.

---

## 6. Target versus Executed State

The target:

`t_target`

is not the committed executed state:

`t_exec`.

The distinction is:

`target ≠ executed state`.

A target represents the output of the upstream classification layer.

Executed state represents retained committed state after execution semantics are applied.

---

## 7. Target Generation versus Commit

The distinction is:

`target generation ≠ commit`.

Evaluation of:

`P_CT`

does not itself mutate:

`t_exec`.

Commit remains part of the ternary execution layer.

---

## 8. Canonical Continuous-Discrete Boundary

The canonical boundary is:

`X_C`

`→ P_CT`

`T_target`

`→ E_T`

`T_exec`.

The first mapping performs classification.

The second structure performs execution.

---

## 9. Decision Coordinate

A mapping may first derive a decision coordinate:

`z = F_D(x_C)`.

Then:

`P_CT`

may operate on:

`z`.

The decision coordinate belongs to a separate typed space:

`X_D`.

---

## 10. Scalar Decision Coordinate

For:

`X_D ⊆ R`

a scalar coordinate may be:

`z ∈ R`.

The ternary target may then be determined through two boundaries or thresholds.

---

## 11. Symmetric Scalar Threshold Mapping

Let:

`eta > 0`.

Define:

`t_target = 1`

when:

`z > eta`;

`t_target = -1`

when:

`z < -eta`;

otherwise:

`t_target = 0`.

This defines three decision regions.

---

## 12. Canonical Scalar Regions

For symmetric threshold:

`eta`

the regions are:

`D_- = (-infinity, -eta)`

`D_0 = [-eta, eta]`

`D_+ = (eta, infinity)`.

The exact boundary convention must be stated by the specialization.

---

## 13. Active Neutral Target Region

The region:

`D_0`

maps to:

`t_target = 0`.

This target value belongs to the active-neutral ternary domain.

The source region itself is not ternary state.

---

## 14. Asymmetric Threshold Mapping

A model may use:

`eta_-`

and:

`eta_+`

with:

`eta_- < eta_+`.

Then:

`t_target = -1`

for:

`z < eta_-`;

`t_target = 0`

for:

`eta_- ≤ z ≤ eta_+`;

`t_target = 1`

for:

`z > eta_+`.

The thresholds need not be symmetric.

---

## 15. Threshold Provenance

Threshold values may carry provenance:

`AUTHOR_DEFINED`

`CALIBRATED`

`PRIMARY_SOURCE`

or another applicable class.

The provenance must match the origin of the threshold.

---

## 16. Threshold Scope

A threshold value belongs to a specific mapping and model domain.

Repeated use does not make it a universal TR-EIF constant.

---

## 17. Boundary Convention

A mapping must define whether equality with a threshold belongs to:

- the neutral region;
- one polarized region;
- a separately defined boundary class before target generation.

The convention must remain consistent across documentation, implementation, tests, and schemas.

---

## 18. Threshold Crossing

A threshold crossing changes the relation between:

`z`

and a decision boundary.

It may change:

`t_target`.

It is not automatically a bifurcation.

---

## 19. Threshold Crossing versus Ternary Commit

A threshold crossing may produce a new target.

It does not itself constitute a committed transition.

Therefore:

`threshold crossing ≠ ternary commit`.

---

## 20. Window-Based Mapping

A decision may be defined through a window:

`W_D ⊂ X_D`.

The target mapping may depend on whether:

`z`

is:

- outside;
- on the boundary;
- inside.

The mapping from these classes into:

`-1/0/1`

must be explicit.

---

## 21. Resonance-Window Input

A resonance classifier may produce:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

A target mapping may then use:

`P_KT: K_R × X_aux → T_target`.

---

## 22. Resonance Class Is Not Ternary Target

The mapping:

`OUTSIDE → -1`

`BOUNDARY → 0`

`INSIDE → 1`

is not assumed automatically.

If such a mapping is selected, it must be explicitly defined.

---

## 23. Direct Resonance Mapping

A target may be produced directly from resonance state:

`P_RT: X_R → T_target`.

This bypasses explicit storage of:

`K_R`

while preserving the conceptual distinction between resonance state and ternary target.

---

## 24. Multidimensional Decision Space

Let:

`X_D ⊆ R^m`.

Then:

`z = (z_1, ..., z_m)`.

The target mapping may depend on a multidimensional partition:

`X_D = D_- ∪ D_0 ∪ D_+`

under the declared boundary conventions.

---

## 25. Multidimensional Region Mapping

Define:

`P_DT(z) = -1`

for:

`z ∈ D_-`;

`P_DT(z) = 0`

for:

`z ∈ D_0`;

`P_DT(z) = 1`

for:

`z ∈ D_+`.

The three regions must be explicitly defined.

---

## 26. Region Disjointness

For deterministic exact classification, the decision regions should be mutually exclusive under the declared convention.

A valid partition satisfies:

`D_- ∩ D_0 = empty`

`D_- ∩ D_+ = empty`

`D_0 ∩ D_+ = empty`.

---

## 27. Region Coverage

For complete deterministic mapping:

`D_- ∪ D_0 ∪ D_+ = X_D`.

Every admissible input then maps to exactly one target.

---

## 28. Partial Domain Mapping

A model may define:

`X_valid ⊂ X_D`

and perform ternary classification only within:

`X_valid`.

States outside:

`X_valid`

must use a separately typed domain-status mechanism.

They must not be encoded as ternary:

`0`.

---

## 29. Domain Status versus Neutral

The distinction is:

`OUT_OF_DOMAIN ≠ 0`.

Active neutral remains a valid ternary target.

Domain failure belongs to a separate state space.

---

## 30. Invalid Input versus Neutral

Likewise:

`INVALID ≠ 0`.

Input validation status must not overwrite balanced ternary semantics.

---

## 31. Missing Input versus Neutral

Likewise:

`MISSING ≠ 0`.

Missingness requires separate representation.

---

## 32. Decision Function

A target mapping may be defined by a scalar decision function:

`g: X_C → R`.

Then:

`t_target`

depends on:

`g(x_C)`.

---

## 33. Two-Boundary Decision Function

For boundaries:

`b_- < b_+`

define:

`t_target = -1`

if:

`g(x_C) < b_-`;

`t_target = 0`

if:

`b_- ≤ g(x_C) ≤ b_+`;

`t_target = 1`

if:

`g(x_C) > b_+`.

---

## 34. Signed Margin

A signed decision margin may be:

`m_D = g(x_C)`.

Its sign is not ternary polarity by identity.

Only:

`P_CT`

assigns ternary semantics.

---

## 35. Zero Decision Coordinate

The condition:

`g(x_C) = 0`

does not universally imply:

`t_target = 0`.

That depends on the decision regions.

---

## 36. Positive Decision Coordinate

Likewise:

`g(x_C) > 0`

does not universally imply:

`t_target = 1`.

---

## 37. Negative Decision Coordinate

Likewise:

`g(x_C) < 0`

does not universally imply:

`t_target = -1`.

---

## 38. Linear Decision Mapping

A decision coordinate may use:

`g(x) = w^T x + b`.

The target is then produced through the selected ternary decision regions.

The weight vector and offset belong to the model.

---

## 39. Nonlinear Decision Mapping

A decision function may be nonlinear:

`g(x) = F_nonlin(x)`.

The ternary semantics remain determined by the explicit region mapping rather than by function complexity.

---

## 40. Multiple Decision Functions

A mapping may use:

`g_1(x), ..., g_m(x)`.

These jointly define:

`z ∈ X_D`.

This permits multidimensional target boundaries.

---

## 41. Decision Surface

A boundary may be defined by:

`B(z) = 0`.

The sign or region around:

`B`

may participate in target classification.

The decision surface itself is not a ternary state.

---

## 42. Multiple Decision Surfaces

A three-region mapping may require several surfaces.

For example:

`B_-(z) = 0`

and:

`B_+(z) = 0`.

The surfaces determine region geometry.

---

## 43. Curved Decision Boundary

TR-EIF does not require linear thresholds.

Decision boundaries may be:

- nonlinear;
- curved;
- disconnected;
- topology-dependent;
- scale-dependent;
- history-dependent.

---

## 44. Disconnected Decision Region

A target region may contain disconnected components.

For example:

`D_+ = D_+^(1) ∪ D_+^(2)`.

Ternary classification depends on region membership rather than connectedness.

---

## 45. Nested Decision Regions

A model may use nested regions.

The mapping must still resolve every admissible input to one target.

---

## 46. Decision Metric

A decision space may carry a metric:

`d_D`.

This can define:

- distance to target region;
- distance to boundary;
- confidence margin;
- numerical localization.

---

## 47. Distance-to-Boundary Mapping

A classifier may use:

`d(z, ∂D)`.

Distance alone does not identify which target region contains the point unless side information is included.

---

## 48. Decision Margin

A margin may quantify robustness of current target classification.

The margin is an observable.

It is not the target itself.

---

## 49. Target Confidence

A model may associate confidence:

`c_T`

with:

`t_target`.

The pair:

`(t_target, c_T)`

contains more information than the ternary target alone.

---

## 50. Target Confidence Is Not Neutral State

Low confidence does not imply:

`t_target = 0`.

Confidence and target remain separately typed.

---

## 51. Probabilistic Target Distribution

A probabilistic model may define:

`p_T = (p_-, p_0, p_+)`

with:

`p_- + p_0 + p_+ = 1`.

This distribution belongs to a probability simplex.

It is not itself a ternary target.

---

## 52. Probabilistic Decision Rule

A sampling or decision function:

`S_T(p_T, xi) → T_target`

may convert the probability distribution into an exact ternary target.

The random state:

`xi`

must be explicit when reproducibility is required.

---

## 53. Maximum-Probability Target

A deterministic decision policy may select:

`t_target = argmax_t p_t`

with an explicit tie-breaking rule.

The resulting target is exact.

---

## 54. Tie Handling

If two or more target probabilities are equal maxima, the policy must specify:

- deterministic priority;
- previous-target retention;
- neutral preference;
- another explicit rule.

No implicit tie handling is permitted.

---

## 55. History-Dependent Target Mapping

A target mapping may depend on history:

`P_CT,H: X_C × X_H → T_target`.

This permits:

- hysteresis;
- persistence;
- trend dependence;
- previous-state dependence.

---

## 56. Hysteretic Target Mapping

A hysteretic target mapping uses retained target or classifier state.

A general form is:

`t_target[k+1] = F_T(x_C[k], t_target[k], m[k])`.

---

## 57. Entry Threshold

A hysteretic mapping may define an entry threshold for polarized target generation.

---

## 58. Exit Threshold

It may define a separate exit threshold.

The entry and exit thresholds need not coincide.

---

## 59. Positive Hysteresis

A positive target may be entered at:

`eta_+^enter`

and exited at:

`eta_+^exit`.

The relation between these values defines the hysteresis width.

---

## 60. Negative Hysteresis

The negative branch may use:

`eta_-^enter`

and:

`eta_-^exit`.

The positive and negative hysteresis structures need not be symmetric.

---

## 61. Hysteresis State

If target generation depends on the previous target, that previous target is part of the result-affecting state.

---

## 62. Hysteresis versus Ternary Execution

Target hysteresis belongs upstream of execution.

It does not replace:

- neutral mediation;
- pending routing;
- scheduler authorization;
- committed writeback.

---

## 63. Persistence-Based Target Mapping

A target may be emitted only after a decision region remains active for a specified persistence interval.

---

## 64. Consecutive-Step Persistence

A discrete rule may require:

`m`

consecutive samples inside a region before changing target.

The persistence counter becomes state.

---

## 65. Time-Based Persistence

A continuous rule may require:

`tau_persist`.

The time coordinate must be explicit.

---

## 66. Persistence Counter

Let:

`c_persist[k]`

be a counter.

If it affects future target generation, it belongs to complete state.

---

## 67. Persistence Reset

A persistence mechanism must define when:

`c_persist`

is reset.

Possible conditions include:

- leaving the candidate region;
- target change;
- execution completion;
- explicit cancellation.

---

## 68. Filtered Decision State

A target may be based on filtered continuous state:

`z_f[k+1] = F_filter(z_f[k], z[k])`.

Then:

`z_f`

is retained state.

---

## 69. Filtering versus Hysteresis

Filtering and hysteresis are separate mechanisms.

Filtering transforms the continuous decision coordinate.

Hysteresis changes classification behavior based on prior state.

---

## 70. Filtering versus Neutral Routing

Filtering remains upstream of target generation.

Neutral routing remains downstream of target generation.

---

## 71. State-Dependent Target Mapping

The target may depend on current executed state:

`P_CT: X_C × T_exec → T_target`.

This permits context-dependent target semantics.

---

## 72. Executed-State-Dependent Boundary

Decision boundaries may vary with:

`t_exec`.

For example:

`D_+^(-1)`

may differ from:

`D_+^(0)`.

Such asymmetry must be explicit.

---

## 73. Target-Dependent Target Mapping

A mapping may also depend on previous:

`t_target`.

This is a form of target-state memory.

---

## 74. Pending-State-Dependent Target Mapping

A specialization may include:

`t_pending`

in target generation.

This must be used carefully because pending state belongs to execution.

The dependency must not collapse target generation and execution semantics.

---

## 75. Scheduler-Aware Target Mapping

A model may include scheduler-visible context in target generation.

Scheduler state remains separately typed.

---

## 76. Capacity-Aware Target Mapping

A model may incorporate capacity state into target generation.

Capacity remains an execution or resource variable rather than a ternary state.

---

## 77. Topology-Dependent Mapping

The mapping may depend on graph:

`G`.

Then:

`P_CT: X_C × X_G → T_target`.

Dynamic topology becomes part of complete state where result-affecting.

---

## 78. Scale-Dependent Mapping

For scale:

`ell`

define:

`P_CT^(ell): X_C^(ell) → T_target^(ell)`.

Scale identity remains explicit.

---

## 79. Multiscale Target Mapping

A target may depend jointly on several scales:

`P_MT: X_C^(ell_1) × ... × X_C^(ell_m) → T_target`.

The aggregation rule must be explicit.

---

## 80. Scale Arbitration

If different scales propose different targets, an arbitration mapping may resolve them:

`A_scale: T_target^m × X_aux → T_target`.

---

## 81. Arbitration Is Not Execution

Scale arbitration produces one target.

It does not commit the executed state.

---

## 82. Local Target

Each entity:

`i`

may have:

`t_target_i ∈ {-1, 0, 1}`.

The target vector is:

`T_target_vec = (t_target_1, ..., t_target_N)`.

---

## 83. Global Target

A model may also define one global target.

Local and global targets remain distinct.

---

## 84. Cluster Target

A cluster may have:

`t_target,Ca`.

A cluster target does not automatically overwrite entity-level targets.

A mapping must define propagation or aggregation.

---

## 85. Hierarchical Target Structure

A hierarchy may contain:

- pair targets;
- local targets;
- cluster targets;
- supercluster targets;
- global target.

Each level must define its own semantics and mapping relations.

---

## 86. Target Aggregation

A global target may be derived from local targets:

`t_target,G = A_T(t_target_1, ..., t_target_N)`.

No universal aggregation rule is imposed.

---

## 87. Majority Aggregation

A specialization may use majority logic.

This remains an author-defined or implementation-specific aggregation rule.

---

## 88. Weighted Aggregation

A target aggregator may use weights.

Weights may depend on:

- scale;
- topology;
- confidence;
- material state;
- local resonance strength.

---

## 89. Neutral-Aware Aggregation

Any ternary aggregation must preserve the active semantics of:

`0`.

Neutral cannot be treated as absent vote unless explicitly represented by a different state.

---

## 90. Target Cancellation

A mapping may change:

`t_target`

to:

`0`.

This is a target change.

It does not automatically clear a pending execution route.

---

## 91. Pending Route Cancellation

If target cancellation should cancel a pending route, the execution contract must define the cancellation operation explicitly.

---

## 92. Target Reversal

A target may change:

`1 → -1`

or:

`-1 → 1`

at the target layer.

This is allowed because target transitions are not committed executed-state transitions.

---

## 93. Target Reversal versus Executed Reversal

A direct target change:

`-1 → 1`

does not authorize a direct committed:

`-1 → 1`.

The execution layer remains neutral-mediated.

---

## 94. Stable Target

A target may remain constant across many execution coordinates.

Target stability does not imply executed-state equality.

---

## 95. Target Residence

The duration for which a target is retained is a target-layer property.

It remains distinct from neutral residence in executed state.

---

## 96. Target Chatter

Repeated switching of:

`t_target`

near a decision boundary may occur.

Possible control mechanisms include:

- hysteresis;
- persistence;
- filtering;
- deadband.

---

## 97. Target Chatter versus Execution Chatter

Rapid target changes and rapid executed-state changes are separate behaviors.

The execution layer may suppress or delay target chatter.

---

## 98. Deadband Target Mapping

A deadband may map a finite continuous region into:

`t_target = 0`.

This is one valid specialization.

The deadband region is not identical to the ternary state itself.

---

## 99. Adaptive Threshold

A threshold may evolve:

`eta[k+1] = F_eta(eta[k], x[k])`.

Then:

`eta`

belongs to result-affecting state.

---

## 100. Adaptive Decision Boundary

More generally:

`B[k+1] = F_B(B[k], x[k])`.

Dynamic boundary state must be retained for deterministic continuation.

---

## 101. Calibrated Target Mapping

A mapping may contain calibrated thresholds or parameters.

The calibration context must remain explicit.

---

## 102. Learned Target Mapping

A learned mapping may be:

`P_CT,theta`.

The trainable parameters:

`theta`

belong to parameter state.

The output codomain remains:

`{-1, 0, 1}`.

---

## 103. Learning Does Not Redefine Ternary Domain

Optimization of:

`theta`

cannot change:

`T_target = {-1, 0, 1}`

without changing the formal mapping contract.

---

## 104. Learned Logit Representation

A learned classifier may first produce logits:

`l = (l_-, l_0, l_+)`.

The logits are continuous outputs.

They are not ternary targets.

---

## 105. Logit-to-Target Mapping

A separate decision rule maps logits into:

`t_target`.

This maintains continuous/discrete separation.

---

## 106. Soft Target Distribution

A model may retain a probability distribution over ternary targets for learning.

The soft distribution is not committed ternary state.

---

## 107. Hard Target

A hard target is exactly one element of:

`{-1, 0, 1}`.

The conversion from soft representation to hard target must be explicit.

---

## 108. Differentiable Approximation

Training may use a differentiable approximation of ternary decision boundaries.

Such an approximation belongs to the optimization layer.

The inference or execution target remains exact when hard ternary semantics are required.

---

## 109. Surrogate Mapping

A numerical surrogate may approximate:

`P_CT`.

The surrogate is conforming only if its output semantics and acceptance criteria preserve the declared target contract.

---

## 110. Quantization versus Ternary Mapping

The distinction remains:

`quantization ≠ ternary mapping`.

A generic three-level numerical quantizer does not automatically carry TR-EIF ternary semantics.

---

## 111. Ternary Encoding

An implementation may encode:

`-1`

`0`

`1`

using arbitrary machine values.

The encoding must be injective over the ternary state set.

---

## 112. Exact Target Equality

Once classified, target equality is exact.

Tolerance is applied only to upstream numerical quantities or decision boundaries.

---

## 113. Floating-Point Decision Mapping

A floating-point implementation evaluates continuous decision variables approximately.

The mathematical target mapping remains defined by the formal boundaries.

---

## 114. Numerical Boundary Tolerance

A numerical implementation may define:

`epsilon_D`

for boundary detection.

This tolerance belongs to the numerical realization.

---

## 115. Exact Boundary versus Numerical Band

The exact boundary may be:

`B(z) = 0`.

A numerical band may be:

`|B(z)| ≤ epsilon_D`.

These are distinct objects.

---

## 116. Numerical Band versus Neutral Target

The numerical boundary band does not automatically imply:

`t_target = 0`.

That policy must be explicitly defined if used.

---

## 117. Rounding

Rounding of continuous decision variables is a numerical operation.

It must not silently change target semantics.

---

## 118. Saturation

Numerical saturation of a continuous input is not a ternary transition.

---

## 119. Overflow

Numerical overflow is not:

`t_target = 0`.

Overflow requires a separately typed error path.

---

## 120. NaN Handling

A non-finite numerical value must not silently map to active neutral.

The implementation must define explicit invalid-input handling.

---

## 121. Infinity Handling

The same applies to positive or negative infinity unless those values are explicitly part of the mathematical source domain.

---

## 122. Target Validation

A target validator checks:

`t_target ∈ {-1, 0, 1}`.

This is exact categorical validation.

---

## 123. Mapping Validation

A mapping validator checks that the produced target matches the declared decision rule for the supplied complete input.

---

## 124. Boundary Validation

Boundary tests should include values:

- below boundary;
- on boundary;
- above boundary.

The expected target must follow the declared convention.

---

## 125. Symmetric Threshold Validation

For symmetric:

`eta`

the test suite should verify both positive and negative branches.

---

## 126. Neutral-Region Validation

Inputs in the neutral decision region must produce:

`t_target = 0`.

This validates target generation only.

---

## 127. Target/Execution Separation Validation

A validator must allow:

`t_target ≠ t_exec`

where execution staging requires it.

---

## 128. Opposite-Target Validation

For:

`t_exec = -1`

and:

`t_target = 1`

the target is valid.

The execution validator separately verifies the route:

`-1 → 0 → 1`.

---

## 129. Reverse Opposite-Target Validation

For:

`t_exec = 1`

and:

`t_target = -1`

the target is valid.

Execution remains:

`1 → 0 → -1`.

---

## 130. Target Trace

A target-generation trace may contain:

- source coordinate;
- resonance coordinate;
- decision coordinate;
- threshold or boundary state;
- target;
- confidence;
- hysteresis state;
- persistence state.

---

## 131. Target Trace versus Execution Trace

A target trace records classification.

An execution trace records committed state evolution.

The artifacts may be linked by execution coordinate but remain distinct.

---

## 132. Target Replay

For deterministic target generation, identical complete input state and parameters produce the same:

`t_target`.

---

## 133. Restart State for Target Generation

A restart-complete target layer may require:

- previous target;
- hysteresis state;
- persistence counters;
- adaptive thresholds;
- filtered state;
- random state where applicable.

---

## 134. Target Provenance

The mapping itself and its parameters may carry provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 135. Author-Defined Mapping

A TR-EIF-specific continuous-to-ternary rule carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 136. Calibrated Boundary

A data-derived threshold or decision boundary carries:

`CALIBRATED`

provenance.

---

## 137. Derived Boundary

A decision boundary analytically derived from other model quantities may carry:

`DERIVED`

provenance.

---

## 138. Primary-Source Component

If a mapping uses a classical relation from literature, that component retains:

`PRIMARY_SOURCE`

provenance.

The TR-EIF ternary interpretation remains separately identified.

---

## 139. Benchmark Mapping Result

Measured classification performance from an implementation may carry:

`BENCHMARK`

provenance.

---

## 140. Target Test Fixture

Controlled inputs designed to exercise each target region may carry:

`TEST_FIXTURE`

provenance.

---

## 141. Phase-Derived Target Mapping

For oscillator phase:

`theta_i`

a specialization may use:

`z_i = sin(theta_i)`.

Then:

`z_i ∈ [-1, 1]`.

---

## 142. Phase Threshold Mapping

For threshold magnitude:

`eta`

define:

`sin(theta_i) > eta → t_target_i = 1`

`sin(theta_i) < -eta → t_target_i = -1`

otherwise:

`t_target_i = 0`.

---

## 143. Phase Target Is Not Phase State

The result:

`t_target_i`

is not:

`theta_i`.

The mapping reduces continuous circular phase information into one ternary target.

---

## 144. Phase Target Is Information Reducing

Many phase values produce the same target.

Therefore the mapping is non-injective.

---

## 145. Phase Order Target Mapping

A specialization may use global or local:

`R`

as one input to target generation.

The mapping must define how phase order contributes to ternary semantics.

---

## 146. Coherence Target Mapping

Likewise, coherence:

`C`

may enter:

`P_CT`.

The target remains distinct from coherence.

---

## 147. Synchronization Target Mapping

Synchronization state may contribute to target generation.

The synchronization class remains distinct from ternary target.

---

## 148. Resonance Target Mapping

Resonance coordinates may provide the primary decision state for:

`P_RT`.

This is the canonical Ternary Resonance path.

---

## 149. Joint Phase-Resonance Mapping

A target may depend jointly on:

`Theta`

and:

`r`.

This is allowed when the complete domain is declared.

---

## 150. Joint Synchronization-Coherence Mapping

A target may depend on:

`X_sync × X_C`.

The mapping remains model-specific.

---

## 151. Joint Multimodal Mapping

A general target mapping may be:

`P_CT: X_phase × X_sync × X_C × X_R × X_EIF,desc × X_H → T_target`.

A concrete specialization should include only the required components.

---

## 152. EIF-Derived Continuous Input

The EIF layer may provide continuous descriptors:

`x_EIF,desc`.

These may feed resonance or target mappings.

The descriptor remains distinct from physical force or energy unless separately typed.

---

## 153. Equivariant Input

A target mapping may consume equivariant representation only if the resulting target transformation contract is explicitly defined.

---

## 154. Invariant Target Mapping

If ternary target is intended to be invariant under geometric transformation, the complete mapping must satisfy:

`P_CT(rho_X(g)x) = P_CT(x)`.

---

## 155. Geometry Does Not Flip Ternary Polarity by Identity

No geometric transformation automatically produces:

`-1 ↔ 1`.

Any such relation requires an explicit target transformation law.

---

## 156. Local Target Mapping

For entity:

`i`

a local map may be:

`P_CT,i: X_loc,i → T_target,i`.

A local map cannot silently access undeclared global state.

---

## 157. Pair Target Mapping

For pair:

`i, j`

a pair mapping may produce:

`t_target,ij`.

The relation between pair target and entity target must be explicitly defined.

---

## 158. Cluster Target Mapping

A cluster mapping may produce:

`t_target,C`.

Cluster semantics remain separate from local semantics.

---

## 159. Global Target Mapping

A global target may represent one system-level ternary target.

It does not automatically overwrite local targets.

---

## 160. Target Propagation

If higher-level targets affect lower-level targets, the propagation mapping must be explicit.

---

## 161. Bottom-Up Target Aggregation

Likewise, aggregation from local targets to higher scales must be explicit.

---

## 162. Target Conflict

Different target sources may disagree.

For example:

`t_target,local = 1`

while:

`t_target,global = -1`.

The conflict requires an arbitration rule.

---

## 163. Target Arbitration

Define:

`A_T: X_candidate → T_target`.

The candidate space may contain multiple target proposals and associated metadata.

---

## 164. Arbitration Priority

A deterministic arbitration policy may use:

- fixed priority;
- confidence;
- scale;
- recency;
- safety constraint;
- author-defined precedence.

The policy must be declared.

---

## 165. Arbitration Neutral Result

An arbitration policy may produce:

`0`.

This is an active-neutral target, not absence of a decision.

---

## 166. Arbitration Rejection

A policy may also reject all proposals.

Rejection must use a state separate from:

`0`.

---

## 167. Target Request

The result of target generation may be packaged as a request:

`q_T = (t_target, metadata)`.

The request remains upstream of execution authorization.

---

## 168. Target Registration

An implementation may register the target at a boundary before execution.

Registration does not itself imply commit.

---

## 169. Registered Target

A registered target may be retained across execution tacts.

It belongs to target state.

---

## 170. Target Update Ordering

If multiple target updates occur within one numerical or execution cycle, the ordering rule must be explicit.

---

## 171. Last-Writer Policy

A specialization may use last-writer semantics.

This is an implementation policy, not a universal framework rule.

---

## 172. First-Writer Policy

A specialization may instead retain the first accepted target until execution or cancellation.

---

## 173. Queue-Based Target Policy

Multiple target requests may be queued.

If queue state affects future execution, it belongs to complete computational state.

---

## 174. Target Queue versus Pending Route

A target queue and pending ternary route are different structures.

The first stores upstream requests.

The second stores execution-stage route state.

---

## 175. Target Versioning

A target request may carry a sequence number or generation coordinate.

This can preserve ordering.

The identifier is metadata, not ternary state.

---

## 176. Stale Target

A specialization may define when a target becomes stale.

Staleness is a target-management property.

It is not active neutral.

---

## 177. Target Expiration

An expiring target requires an explicit expiration rule.

Expiration may generate cancellation or recomputation.

---

## 178. Target Refresh

A target may be periodically recomputed.

Refresh cadence remains separate from execution cadence.

---

## 179. Target Cadence

The target-generation cadence may differ from phase integration or ternary scheduler cadence.

All coordinates must remain explicit.

---

## 180. Physical Time versus Target Step

The target evaluation index is not automatically physical time.

A mapping must connect them where necessary.

---

## 181. Target Step versus Execution Tact

Likewise:

`target evaluation step ≠ execution tact`.

---

## 182. Continuous Event-Driven Targeting

A continuous model may generate targets at localized event times.

This is event-driven target generation.

---

## 183. Periodic Targeting

A discrete implementation may recompute targets at fixed intervals.

This is periodic target generation.

---

## 184. Conditional Targeting

A mapping may be evaluated only when an upstream condition is true.

The triggering condition must be explicit.

---

## 185. Target Mapping Determinism

A deterministic:

`P_CT`

must return the same target for the same complete admissible input.

---

## 186. Target Mapping State Closure

Every result-affecting variable must belong to:

- current source state;
- history;
- retained mapping state;
- parameters;
- declared external input.

---

## 187. Hidden Mapping State

Undeclared hysteresis, adaptive threshold, filter state, or random state breaks complete deterministic target closure.

---

## 188. Mapping Idempotence

A target mapping need not be idempotent because its domain and codomain may differ.

If a mapping from target to target is introduced separately, its properties must be analyzed independently.

---

## 189. Mapping Surjectivity

A specialization need not necessarily produce all three target values on every restricted operating domain.

The formal codomain remains:

`{-1, 0, 1}`.

---

## 190. Reachable Target Set

For domain:

`D ⊆ X_C`

define:

`T_reachable(D) = {P_CT(x) | x ∈ D}`.

This may be a subset of:

`{-1, 0, 1}`.

---

## 191. Neutral-Only Domain

A restricted domain may map entirely to:

`0`.

This does not redefine the ternary target space.

---

## 192. Polarized-Only Domain

A restricted domain may produce only:

`-1`

and:

`1`.

The execution layer still retains active neutral for opposite routing.

---

## 193. Target Reachability versus Execution Reachability

A target value being reachable does not mean it can be committed immediately from every executed state.

---

## 194. Opposite Target Reachability

If:

`1`

is a valid target while:

`t_exec = -1`,

the target is reachable immediately at the target layer.

Execution still requires two legs.

---

## 195. Execution Path Independence from Target Mapping Complexity

Whether the target arose from:

- one threshold;
- neural model;
- resonance classifier;
- multiscale aggregation

does not change the canonical opposite-polarity execution path.

---

## 196. Canonical Execution Kernel

The executed domain remains:

`T_exec = {-1, 0, 1}`.

The state:

`0`

remains active.

The forbidden direct committed transitions are:

`-1 → 1`

and:

`1 → -1`.

---

## 197. Canonical Opposite Routes

The required routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Target mapping cannot weaken this invariant.

---

## 198. First-Leg Semantics

For:

`t_exec = -1`

and:

`t_target = 1`

the first committed leg may produce:

`t_exec,next = 0`

with pending destination:

`1`.

---

## 199. Reverse First-Leg Semantics

For:

`t_exec = 1`

and:

`t_target = -1`

the first committed leg may produce:

`t_exec,next = 0`

with pending destination:

`-1`.

---

## 200. Second-Leg Semantics

The pending route completes later through:

`0 → 1`

or:

`0 → -1`

under the applicable authorization condition.

---

## 201. Target Persistence during Pending Route

A specialization may preserve the opposite target while the execution remains neutral.

This is consistent with:

`target ≠ executed state`.

---

## 202. Target Change during Pending Route

If the target changes during pending execution, the route policy must define how the pending destination is handled.

---

## 203. Target Neutralization during Pending Route

If:

`t_target → 0`

while a pending route exists, this does not automatically clear:

`t_pending`.

An explicit cancellation rule is required.

---

## 204. Target Return to Origin

If target returns to the original polarity during neutral residence, the execution contract must define whether the pending route:

- reverses;
- cancels;
- remains;
- awaits arbitration.

---

## 205. Target Override

Any override mechanism must preserve separate target and execution state.

It must not introduce a direct opposite committed edge.

---

## 206. Safety or Guard Override

A supervisory layer may force:

`t_target = 0`

under explicit conditions.

The target remains active neutral.

The supervisory condition itself belongs to another state space.

---

## 207. Guard Rejection

A guard may reject a target request entirely.

Rejection must not be encoded as active neutral unless the formal policy explicitly creates a new neutral target request.

---

## 208. Mapping and Scheduler Boundary

The target mapper determines desired ternary state.

The scheduler determines when execution opportunities occur.

The two layers remain distinct.

---

## 209. Mapping and Capacity Boundary

The target mapper does not guarantee execution capacity.

Capacity checks belong downstream.

---

## 210. Mapping and Pending-Routing Boundary

The target mapper does not implement pending opposite routes.

Pending routing belongs to the execution architecture.

---

## 211. Mapping and Commit Boundary

The target mapper has no implicit retained-state write authority.

Commit belongs to the execution boundary.

---

## 212. FRP Phase-to-Target Reference

The FRP executable reference uses:

`z_i = sin(theta_i)`.

The target mapping uses threshold magnitude:

`0.33`.

---

## 213. FRP Positive Target Rule

The FRP reference mapping uses:

`sin(theta_i) > 0.33 → t_target_i = 1`.

---

## 214. FRP Negative Target Rule

The FRP reference mapping uses:

`sin(theta_i) < -0.33 → t_target_i = -1`.

---

## 215. FRP Neutral Target Rule

Otherwise:

`t_target_i = 0`.

The result is active-neutral target state.

---

## 216. FRP Threshold Scope

The value:

`0.33`

is an FRP executable specialization parameter.

It is not a universal TR-EIF threshold.

---

## 217. FRP Target Boundary

The phase-derived FRP target remains upstream of scheduler and execution logic.

It is not immediate retained-state replacement.

---

## 218. FRP Opposite Target

When:

`t_exec = -1`

and:

`t_target = 1`

the FRP executable reference preserves:

`-1 → 0`

with pending destination:

`1`

followed later by:

`0 → 1`.

---

## 219. FRP Reverse Opposite Target

When:

`t_exec = 1`

and:

`t_target = -1`

the reference preserves:

`1 → 0`

with pending destination:

`-1`

followed later by:

`0 → -1`.

---

## 220. FRP Scheduler Interface

FRP scheduler modes:

`7/1`

and:

`1/7`

operate downstream of target generation.

They do not redefine the target mapping.

---

## 221. FRP Phase Layer Interface

The FRP target mapping consumes phase-derived state produced by the phase layer.

The phase layer may include:

- retained frequency;
- receiving-state phase lag;
- coupling attenuation;
- phase evolution.

These upstream mechanisms remain distinct from target classification.

---

## 222. FRP Target versus Coherence

The FRP phase target is not a coherence classification.

The distinction:

`R(t) ≠ C(t)`

remains unchanged.

---

## 223. FRP Target versus Resonance Class

The FRP executable phase target does not imply that resonance classification and ternary target are identical mathematical spaces.

It is one executable specialization of the upstream-to-target interface.

---

## 224. Mapping Provenance Chain

A target mapping should admit the applicable chain:

`source state`

`→ decision coordinate`

`→ boundary or classifier`

`→ target`

`→ implementation`

`→ trace`

`→ validation`.

---

## 225. Mapping Extension Rule

Any new continuous-to-ternary mapping must define:

1. source domain;
2. target codomain;
3. decision variables;
4. decision regions or rule;
5. boundary convention;
6. history dependence;
7. scale;
8. topology dependence;
9. parameterization;
10. provenance;
11. numerical realization;
12. validation criteria.

---

## 226. Hysteretic Mapping Extension Rule

Any hysteretic target mapping must additionally define:

1. retained classifier state;
2. entry conditions;
3. exit conditions;
4. persistence conditions;
5. reset semantics;
6. restart state.

---

## 227. Probabilistic Mapping Extension Rule

Any probabilistic mapping must define:

1. probability model;
2. normalization;
3. random state;
4. decision or sampling rule;
5. tie handling;
6. reproducibility semantics.

---

## 228. Learned Mapping Extension Rule

Any learned mapping must define:

1. input representation;
2. trainable parameters;
3. continuous output representation;
4. hard-target conversion;
5. equivariance or invariance behavior;
6. domain;
7. uncertainty handling;
8. validation.

---

## 229. Multiscale Mapping Extension Rule

Any multiscale target mapping must define:

1. scale-indexed inputs;
2. cross-scale aggregation;
3. arbitration;
4. target scope;
5. information loss;
6. conflict handling.

---

## 230. Canonical Mapping Invariants

Every conforming continuous-to-ternary mapping preserves:

1. explicit source space;

2. exact codomain `{-1, 0, 1}`;

3. active-neutral `0`;

4. explicit decision semantics;

5. explicit handling of invalid and missing input;

6. explicit history when history affects the result;

7. explicit parameter scope;

8. separation between target and execution.

---

## 231. Canonical Type Invariants

The mapping preserves:

`continuous value ≠ ternary target`

`resonance class ≠ ternary target`

`synchronization class ≠ ternary target`

`coherence value ≠ ternary target`

`target ≠ executed state`

`invalid state ≠ active neutral`

`missing state ≠ active neutral`.

---

## 232. Canonical Event Invariants

The mapping preserves:

`threshold crossing ≠ bifurcation`

`threshold crossing ≠ ternary commit`

`target change ≠ ternary commit`

`target reversal ≠ executed direct reversal`.

---

## 233. Canonical Execution Invariants

The downstream execution layer preserves:

`-1/0/1`.

The state:

`0`

remains active.

Direct opposite committed transitions remain forbidden.

---

## 234. Canonical Continuous-Discrete Architecture

The complete architecture is:

`continuous source state`

`→ decision representation`

`→ ternary target`

`→ target registration`

`→ execution request`

`→ scheduler/authorization`

`→ pending routing where required`

`→ active-neutral execution`

`→ committed ternary state`.

---

## 235. Interface to Chapter 06

Chapter 06 develops the dynamics of active-neutral executed state.

The current chapter terminates at:

`T_target`.

Chapter 06 begins from the requirement that:

`0`

is an active execution state rather than missingness or a passive placeholder.

---

## 236. Interface to Chapter 07

Chapter 07 develops neutral routing.

It defines:

- first-leg execution;
- pending destination;
- neutral residence;
- second-leg authorization;
- route completion;
- route cancellation and replacement policies.

---

## 237. Interface to Chapter 08

Chapter 08 develops the complete coupled continuous-discrete dynamical system.

The mapping:

`P_CT`

becomes the formal boundary between continuous state evolution and discrete ternary target state.

---

## 238. Interface to Chapter 09

Chapter 09 develops stability and boundedness.

It distinguishes stability of:

- continuous source dynamics;
- target classification;
- executed ternary state;
- coupled hybrid evolution.

---

## 239. Interface to Chapter 10

Chapter 10 develops numerical time evolution.

It defines:

- sampling;
- event localization;
- target-update timing;
- numerical threshold handling;
- target registration;
- execution ordering;
- deterministic replay.

---

## 240. Final Formal Structure

The continuous-to-ternary layer may be represented as:

`CT = (X_C, X_D, F_D, D_-, D_0, D_+, X_M, P_CT, T_target)`.

Here:

- `X_C` is the continuous source space;
- `X_D` is the decision space;
- `F_D` is the source-to-decision mapping;
- `D_-` is the negative target region;
- `D_0` is the active-neutral target region;
- `D_+` is the positive target region;
- `X_M` is retained mapping state where required;
- `P_CT` is the decision-to-target mapping;
- `T_target = {-1, 0, 1}`.

The execution interface is:

`T_target → X_Texec`.

---

## 241. Final Statement

The continuous-to-ternary layer converts explicitly typed upstream state into an exact balanced ternary target.

The canonical target domain is:

`T_target = {-1, 0, 1}`

with notation:

`-1/0/1`.

The state:

`0`

is active neutral.

Continuous variables, resonance classes, synchronization classes, coherence measures, margins, probabilities, invalid states, and missing values remain distinct from ternary targets.

The mapping may use:

- scalar thresholds;
- multidimensional regions;
- resonance windows;
- hysteresis;
- persistence;
- adaptive boundaries;
- learned decision functions;
- multiscale arbitration.

Every such mapping terminates at:

`t_target`.

It does not directly commit:

`t_exec`.

Therefore an opposite target remains subject to the execution paths:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

This chapter defines the exact continuous-discrete target boundary required by the active-neutral execution dynamics developed in Chapter 06.
