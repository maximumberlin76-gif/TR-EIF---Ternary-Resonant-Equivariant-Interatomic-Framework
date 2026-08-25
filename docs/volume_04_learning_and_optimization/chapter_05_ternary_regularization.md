# Ternary Regularization

## 1. Purpose

This chapter defines ternary regularization within the TR-EIP learning and optimization layer of TR-EIF.

Ternary regularization constrains learned ternary feature channels and their upstream continuous decision variables while preserving the exact semantic kernel:

`-1/0/1`.

The state:

`0`

remains active neutral.

Regularization may shape:

- class occupancy;
- decision margins;
- target persistence;
- neutral-state usage;
- transition frequency;
- target stability;
- target/execution consistency;
- route completion;
- multiscale ternary consistency.

Regularization does not redefine the ternary domain or execution topology.

---

## 2. Ternary Feature State

Let:

`t ∈ {-1,0,1}`.

For multiple channels:

`t ∈ {-1,0,1}^M`.

The ternary state may exist at:

- edge scale;
- atom scale;
- cluster scale;
- global scale.

---

## 3. Exact Semantic Domain

The forward semantic state is exactly:

`-1`

`0`

or:

`1`.

Continuous logits, probabilities, margins, and surrogate variables remain separate computational states.

---

## 4. Active Neutral

The state:

`0`

is active neutral.

It may participate in:

- mediation;
- balancing;
- retention;
- routing;
- transition staging;
- controlled neutralization.

It must not be used as a generic encoding for:

- missing;
- invalid;
- masked;
- padded;
- unknown;
- out-of-domain.

---

## 5. Ternary Regularizer

A ternary regularizer is a scalar optimization term:

`R_T`.

It may depend on:

- hard ternary states;
- continuous pre-classification variables;
- transition sequences;
- target/execution traces;
- channel statistics;
- retained state.

A generic objective is:

`L_total = L_data + lambda_T R_T`.

---

## 6. Regularization Is Not Ternary Semantics

The distinction remains:

`ternary regularization ≠ ternary definition`.

The semantic state set remains fixed independently of the regularizer.

---

## 7. Hard Constraint Boundary

A regularization penalty is soft unless the architecture makes violation impossible.

The following remain hard execution invariants:

`-1 → 1` forbidden

`1 → -1` forbidden.

---

## 8. Canonical Execution Graph

The committed execution graph remains:

`-1 ↔ 0 ↔ 1`.

---

## 9. Opposite-Polarity Routes

The only canonical opposite-polarity committed routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 10. Target State

Let:

`t_target[k] ∈ {-1,0,1}`.

This is the requested ternary state.

---

## 11. Executed State

Let:

`t_exec[k] ∈ {-1,0,1}`.

This is the retained committed state.

---

## 12. Pending State

Let:

`t_pending[k] ∈ {-1,1}`

or:

`NONE`.

---

## 13. Target/Execution Separation

The invariant remains:

`target ≠ executed state`.

A regularizer may couple them but cannot collapse them into one state variable.

---

## 14. Pending/Neutral Separation

The invariant remains:

`pending ≠ neutral`.

`t_pending`

stores a destination.

`t_exec = 0`

stores active-neutral executed state.

---

## 15. Ternary Regularization Domains

Ternary regularization may act on:

1. decision variables;

2. class probabilities;

3. hard targets;

4. executed states;

5. transition traces;

6. occupancy statistics;

7. multiscale state;

8. temporal persistence.

---

## 16. Pre-Classification Variable

Let:

`z`

denote a continuous decision variable.

A hard classifier maps:

`z`

to:

`-1/0/1`.

Regularization may shape:

`z`

without changing the exact output domain.

---

## 17. Logit State

For three-class classification:

`z = (z_-, z_0, z_+)`.

These are continuous logits.

They are not ternary states.

---

## 18. Probability State

Let:

`p = (p_-, p_0, p_+)`.

The probabilities satisfy:

`p_- + p_0 + p_+ = 1`.

They remain distinct from hard ternary state.

---

## 19. Decision Margin

A decision margin quantifies separation from a ternary decision boundary.

It is not ternary state by identity.

---

## 20. Margin Regularization

A margin regularizer may encourage continuous classifier state to remain away from unstable decision boundaries.

---

## 21. Neutral Margin

A model may define a neutral region between negative and positive decision regions.

The width of this region may be fixed, calibrated, or learned.

---

## 22. Neutral Margin Is Not Resonance Window

The distinction remains:

`ternary neutral region ≠ resonance window`.

They belong to different mappings and state spaces.

---

## 23. Symmetric Thresholds

A classifier may use:

`-eta`

and:

`eta`.

---

## 24. Asymmetric Thresholds

A classifier may instead use:

`eta_-`

and:

`eta_+`.

No symmetry around zero is required.

---

## 25. Threshold Regularization

A trainable threshold may be regularized to remain within an admissible parameter domain.

---

## 26. Threshold Ordering Constraint

For an asymmetric ternary classifier:

`eta_- < eta_+`

must remain satisfied.

This may be enforced structurally or through constrained parameterization.

---

## 27. Neutral Width

Define:

`w_0 = eta_+ - eta_-`.

A model may regularize:

`w_0`

without altering the active-neutral semantics.

---

## 28. Neutral Collapse Boundary

A learned classifier should not collapse:

`w_0`

to an inadmissible value if the architecture requires a nonzero active-neutral interval.

---

## 29. Neutral Expansion Boundary

Likewise, an excessively broad neutral interval may be penalized if it violates the declared model objective.

---

## 30. Occupancy

For a batch or dataset subset, define class occupancy fractions:

`pi_-`

`pi_0`

`pi_+`.

They satisfy:

`pi_- + pi_0 + pi_+ = 1`.

---

## 31. Neutral Occupancy

`pi_0`

is the frequency of active-neutral state.

It is not missing-data frequency.

---

## 32. Occupancy Regularization

A regularizer may constrain empirical occupancy toward a declared reference distribution:

`pi_ref`.

---

## 33. Occupancy Divergence

One possible occupancy objective compares:

`pi_pred`

and:

`pi_ref`

using a declared divergence or distance.

---

## 34. Balanced Occupancy

A model may choose a balanced target distribution.

This is a training choice.

Balanced occupancy is not a universal ternary invariant.

---

## 35. Sparse Occupancy

A model may instead prefer sparse activation of selected ternary classes.

This must be explicitly defined.

---

## 36. Neutral Preference

A model may intentionally prefer:

`0`

in uncertain or low-drive regions through a declared classifier design.

This does not make uncertainty identical to neutral.

---

## 37. Uncertainty versus Neutral

The distinction remains:

`uncertainty ≠ active neutral`.

A model may map uncertainty to neutral only through an explicit policy.

---

## 38. Entropy

The probability vector:

`p`

has classification entropy:

`H(p)`.

This is a continuous uncertainty-related quantity.

---

## 39. Entropy Regularization

A model may penalize or encourage entropy depending on its training objective.

---

## 40. Low-Entropy Objective

A low-entropy regularizer encourages confident class probabilities.

---

## 41. High-Entropy Objective

A high-entropy regularizer may encourage uncertainty in selected domains.

Its scope must remain explicit.

---

## 42. Entropy Is Not Neutral

The distinction remains:

`high entropy ≠ ternary 0`.

---

## 43. Target Stability

A target sequence may be regularized against excessive switching.

---

## 44. Target Switch Event

Define a target switch at step:

`k`

when:

`t_target[k] ≠ t_target[k-1]`.

---

## 45. Target Switch Count

A sequence may define:

`N_switch,target`.

---

## 46. Target Switch Regularization

A regularizer may penalize excessive:

`N_switch,target`.

---

## 47. Target Stability versus Execution Stability

The distinction remains:

`target stability ≠ executed-state stability`.

Executed state is additionally constrained by routing and scheduler semantics.

---

## 48. Executed Switch Event

Define:

`N_switch,exec`

from committed state changes.

---

## 49. Executed Transition Regularization

A model may regularize the frequency of executed transitions when the execution process participates in training.

---

## 50. Direct-Opposite Violation Count

Define:

`N_direct`

as the number of committed:

`-1 → 1`

or:

`1 → -1`

events.

For a conforming execution architecture:

`N_direct = 0`.

---

## 51. Direct-Opposite Penalty

A diagnostic penalty may be:

`R_direct = N_direct`.

The architectural target remains exactly:

`0`.

---

## 52. Structural Enforcement Preferred

When possible, direct-opposite execution should be made unrepresentable rather than merely penalized.

---

## 53. First-Leg Event

An opposite route begins with:

`-1 → 0`

or:

`1 → 0`.

---

## 54. Second-Leg Event

The route completes with:

`0 → 1`

or:

`0 → -1`.

---

## 55. Route Completion

A route-completion objective may compare pending destinations with later executed states.

---

## 56. Pending Consistency

If:

`t_pending = 1`

then the later valid second leg is:

`0 → 1`.

If:

`t_pending = -1`

then the later valid second leg is:

`0 → -1`.

---

## 57. Pending Consistency Regularizer

A regularizer may penalize route completions inconsistent with:

`t_pending`.

---

## 58. Pending Loss Is Not Neutral Loss

The distinction remains:

`pending-destination error ≠ neutral-state error`.

---

## 59. Neutral Residence

Define a neutral residence interval as consecutive executed states:

`t_exec = 0`.

---

## 60. Residence Length

Let:

`L_0`

denote the number of consecutive execution opportunities spent in active neutral.

---

## 61. Residence-Time Regularization

A model may regulate neutral residence length.

The desired residence distribution is specialization-specific.

---

## 62. Zero Residence Boundary

A route that requires active-neutral mediation cannot complete with zero committed neutral residence between opposite polarities.

---

## 63. Minimum Residence

A model may impose a minimum neutral residence.

---

## 64. Maximum Residence

A model may impose a maximum neutral residence where required.

---

## 65. Residence Constraint

Residence bounds may be:

- hard;
- soft;
- scheduler-determined.

The mechanism must be explicit.

---

## 66. Persistence

A target decision may require a condition to persist before target change.

---

## 67. Persistence Counter

Let:

`n_persist`

denote a retained persistence count.

---

## 68. Persistence Regularization

A regularizer may penalize unstable target changes before persistence criteria are satisfied.

---

## 69. Persistence versus Neutral Residence

The distinction remains:

`target persistence ≠ executed neutral residence`.

---

## 70. Hysteresis

A ternary classifier may use state-dependent decision boundaries.

---

## 71. Hysteresis Regularization

A model may regularize hysteresis width or transition consistency.

---

## 72. Hysteresis Width

A hysteresis gap may be constrained to remain positive and bounded.

---

## 73. Hysteresis versus Routing

The distinction remains:

`classifier hysteresis ≠ neutral routing`.

---

## 74. Temporal Regularization

For ordered data, ternary behavior may be regularized across:

`k`.

---

## 75. Temporal Smoothness Boundary

Ternary state is categorical.

Therefore temporal regularization should operate on:

- switch counts;
- persistence;
- probabilities;
- margins;
- transition consistency

rather than pretending categorical values form a continuous physical trajectory.

---

## 76. Numeric Difference Boundary

The arithmetic quantity:

`|t[k] - t[k-1]|`

may be used computationally.

Its magnitude does not itself encode semantic transition cost universally.

---

## 77. Semantic Transition Cost

A transition-cost matrix may explicitly define costs among ternary states.

---

## 78. Transition Cost Matrix

Let:

`C_T(a,b)`

define the training cost for transition:

`a → b`.

---

## 79. Forbidden-Cost Entries

For committed execution:

`C_T(-1,1)`

and:

`C_T(1,-1)`

may be treated as inadmissible rather than merely large finite costs.

---

## 80. Retention Cost

`C_T(a,a)`

may be zero or model-specific.

---

## 81. First-Leg Cost

The cost of:

`-1 → 0`

and:

`1 → 0`

may be regularized separately.

---

## 82. Second-Leg Cost

The cost of:

`0 → 1`

and:

`0 → -1`

may likewise be separate.

---

## 83. Transition Asymmetry

No universal requirement forces:

`C_T(a,b) = C_T(b,a)`.

The cost structure may be directional.

---

## 84. Scheduler-Conditioned Regularization

A training setup may condition ternary regularizers on scheduler state.

---

## 85. Scheduler State

Scheduler state remains separate from:

- target;
- executed state;
- pending destination.

---

## 86. FRP Scheduler Modes

Where FRP executable-reference traces are used, modes:

`7/1`

and:

`1/7`

remain explicitly identified.

---

## 87. 7/1 Mode

The FRP reference mode:

`7/1`

means:

`seven balance tacts → one commit tact`.

---

## 88. 1/7 Mode

The FRP reference mode:

`1/7`

means:

`one excite tact → seven neutralize tacts`.

---

## 89. Scheduler Regularization Scope

A regularizer may encourage behavior appropriate to the active scheduler mode.

The scheduler ratio itself remains an execution-control parameter.

---

## 90. Scheduler Is Not Ternary State

The distinction remains:

`scheduler mode ≠ ternary state`.

---

## 91. FRP Ternary Reference

FRP provides executable reference behavior for selected ternary target and execution mechanisms.

FRP remains distinct from the complete TR-EIP learning architecture.

---

## 92. FRP Phase-to-Target Mapping

Where FRP-derived supervision is used, the executable reference mapping uses:

`sin(theta_i)`

with threshold magnitude:

`0.33`.

---

## 93. FRP Threshold Scope

The value:

`0.33`

remains FRP-specific.

It is not a universal TR-EIP ternary regularization constant.

---

## 94. FRP Direct-Transition Invariant

Applicable qualified FRP artifacts preserve:

`actual_direct_events = 0`.

---

## 95. FRP Reserved-State Invariant

Applicable qualified FRP artifacts preserve:

`reserved_state_events = 0`.

---

## 96. FRP Queue Invariant

Applicable qualified FRP artifacts preserve:

`queue_overflow_events = 0`

under the corresponding configuration.

---

## 97. Ternary Sparsity

A model may regularize the fraction of nonzero ternary features.

Define:

`pi_active = pi_- + pi_+`.

---

## 98. Nonzero Sparsity Objective

A regularizer may penalize excessive:

`pi_active`.

---

## 99. Neutral Sparsity Objective

Alternatively, a model may penalize excessive neutral occupancy.

No universal preference is imposed.

---

## 100. Channel-Wise Occupancy

For channel:

`c`

define:

`pi_c,-`

`pi_c,0`

`pi_c,+`.

---

## 101. Channel Collapse

A channel collapses when it predicts essentially one state across its effective domain.

---

## 102. Collapse Regularization

A regularizer may discourage collapse when multi-state usage is required.

---

## 103. Intentional Collapse

A channel may legitimately become constant if the model definition or learned optimum supports it.

Collapse is not automatically an error.

---

## 104. Cross-Channel Redundancy

Multiple ternary channels may become highly correlated.

A regularizer may discourage redundant channels.

---

## 105. Channel Correlation

A channel-correlation statistic may be computed from encoded ternary values or categorical joint distributions.

---

## 106. Redundancy versus Semantic Equality

Two channels may be numerically correlated while retaining different semantic definitions.

---

## 107. Multichannel Orthogonality Boundary

Orthogonality of numeric encodings is not a universal semantic requirement for ternary channels.

---

## 108. Multiscale Ternary State

A model may define:

`t^(atom)`

`t^(cluster)`

`t^(global)`.

---

## 109. Cross-Scale Consistency

A regularizer may enforce a declared relationship between fine- and coarse-scale ternary states.

---

## 110. Aggregated Target

For example, global target may derive from local states through:

`A_T`.

---

## 111. Cross-Scale Loss

A regularizer may compare predicted coarse state with:

`A_T({t_i})`.

---

## 112. Cross-Scale Identity Boundary

The framework does not assume:

`all local states = global state`.

---

## 113. Multiscale Disagreement

Local and global ternary states may legitimately differ.

Regularization must encode only the declared relation.

---

## 114. Resonance-to-Ternary Consistency

A ternary regularizer may compare classifier state against resonance-derived target semantics.

---

## 115. Resonance Source

Let:

`r ∈ X_R`.

The target map is:

`P_RT(r)`.

---

## 116. Resonance Consistency Loss

A regularizer may penalize disagreement between:

`t_pred`

and:

`P_RT(r)`.

---

## 117. Resonance Class Boundary

The relation remains:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

A regularizer must use the explicit mapping.

---

## 118. Resonance Margin and Ternary Margin

A resonance margin may influence ternary classifier confidence through a declared transformation.

The two margins remain distinct.

---

## 119. Ternary Regularization and Energy

A ternary channel may condition energy:

`E = E(X,t)`.

Regularization may therefore influence the learned energy surface indirectly.

---

## 120. Ternary State Is Not Energy

The invariant remains:

`ternary state ≠ energy`.

---

## 121. Mechanical Smoothness across Ternary Modes

A regularizer may constrain differences among:

`E_-1`

`E_0`

`E_1`

at selected state boundaries.

---

## 122. Energy Matching Loss

One possible boundary objective may compare:

`E_a`

and:

`E_b`

for selected paired states.

---

## 123. Force Matching Loss

A stronger objective may compare:

`F_a`

and:

`F_b`.

---

## 124. No Universal Mode Matching

TR-EIF does not assume mode surfaces must be equal or smoothly connected everywhere.

---

## 125. Neutral Surface Regularization

A model may regularize:

`E_0`

or:

`F_0`

to satisfy a declared mediation role.

---

## 126. Neutral Surface Is Not Arithmetic Mean

The invariant remains:

`E_0 ≠ (E_-1 + E_1)/2`

by identity.

Likewise:

`F_0 ≠ (F_-1 + F_1)/2`

by identity.

---

## 127. Ternary Regularization and Message Passing

A ternary feature may condition message maps:

`M_-1`

`M_0`

`M_1`.

---

## 128. Message-Mode Regularization

A model may regularize separation or consistency among these message families.

---

## 129. Neutral Message Operator

`M_0`

need not produce zero message.

---

## 130. Zero Message versus Neutral

The distinction remains:

`zero message ≠ ternary 0`.

---

## 131. Ternary Regularization and Representation

A regularizer may constrain how strongly latent representations differ across ternary modes.

---

## 132. Representation Separation Loss

A mode-separation objective may encourage latent states for different ternary classes to remain distinguishable.

---

## 133. Representation Compactness Loss

A class-compactness objective may encourage latent states belonging to the same class to cluster.

---

## 134. Representation Geometry Boundary

Latent clustering is not physical phase separation by identity.

---

## 135. Contrastive Ternary Objective

A contrastive objective may use ternary labels to define positive and negative pairs.

---

## 136. Metric-Learning Boundary

The learned embedding metric remains a representation construct.

It is not physical distance.

---

## 137. Class-Conditional Representation

A model may learn class-specific latent distributions.

---

## 138. Ternary Calibration

A ternary classifier may be calibrated after training.

---

## 139. Probability Calibration

Calibration may align predicted class probabilities with observed frequencies.

---

## 140. Hard-State Semantics after Calibration

Calibration does not alter:

`-1/0/1`.

It changes the continuous decision mapping or probability interpretation.

---

## 141. Threshold Calibration

Thresholds:

`eta_-`

and:

`eta_+`

may be calibrated from validation or calibration data.

---

## 142. Calibration Data Separation

Calibration data should remain distinct from test data under a strict evaluation protocol.

---

## 143. Ternary Class Weighting

Class weights may compensate for unequal frequencies.

---

## 144. Inverse-Frequency Weighting

One possible strategy uses weights inversely related to class frequency.

---

## 145. Effective-Number Weighting

Other weighting rules may account for sample counts differently.

The chosen formula must be explicit.

---

## 146. Neutral-Class Weight

The neutral class may have its own dedicated weight.

---

## 147. Transition-Class Weighting

First-leg, second-leg, retention, and neutral-residence events may have separate weights.

---

## 148. Rare Transition Weighting

Rare but valid transition events may receive higher training weight.

---

## 149. Forbidden Event Weighting Boundary

Forbidden committed events are not simply rare classes.

They remain invalid.

---

## 150. Ternary Focal-Type Objective

A focal-style classification loss may emphasize hard examples.

The exact formulation must be explicit if used.

---

## 151. Margin-Based Classification Loss

A margin-based objective may enforce separation between the correct class score and competing class scores.

---

## 152. Neutral-Specific Margin

A model may use distinct margins for neutral versus polar classes.

---

## 153. Polar Symmetry Regularization

If a specialization declares symmetric positive/negative treatment, a regularizer may constrain corresponding parameters.

---

## 154. No Universal Polar Symmetry

TR-EIF does not require:

`-1`

and:

`1`

to have symmetric parameterization in every model.

---

## 155. Polarity Bias

A model may learn or impose asymmetric class priors.

The bias must remain explicit.

---

## 156. Active-Neutral Bias

A prior may favor neutral state under declared conditions.

---

## 157. Prior versus Hard Rule

A probabilistic or loss prior remains soft.

It does not alter hard execution semantics.

---

## 158. Class Prior

Let:

`p_ref(-1)`

`p_ref(0)`

`p_ref(1)`

denote a declared prior distribution.

---

## 159. Prior Regularization

A divergence between predicted occupancy and prior occupancy may be added to the objective.

---

## 160. Prior Source

A prior may be:

- empirical;
- calibrated;
- author-defined;
- derived.

Its provenance must be explicit.

---

## 161. Sequence Likelihood

A stateful ternary model may define a probability over target or execution sequences.

---

## 162. Markov-Type Target Model

A target sequence may use:

`P(t_target[k+1] | t_target[k], x[k])`.

---

## 163. Execution-State Model

Execution sequences require the constrained transition graph.

---

## 164. Invalid Transition Probability

For a hard execution model:

`P(1 | -1) = 0`

and:

`P(-1 | 1) = 0`

for one committed step.

---

## 165. Neutral-Mediated Sequence Probability

Opposite-polarity sequence probability is represented through two or more valid steps via:

`0`.

---

## 166. Sequence Loss

A sequence negative log-likelihood may supervise valid transition trajectories.

---

## 167. Transition Matrix

A learned transition matrix must preserve structural zeros for forbidden committed transitions.

---

## 168. Structural Zero

A structural zero is an impossible transition under the model.

It is not a low-probability event.

---

## 169. Transition Regularization

A regularizer may constrain allowed transition probabilities.

---

## 170. Retention Probability

A model may learn probabilities for:

`-1 → -1`

`0 → 0`

`1 → 1`.

---

## 171. First-Leg Probability

A model may learn probabilities for:

`-1 → 0`

and:

`1 → 0`.

---

## 172. Second-Leg Probability

A model may learn probabilities for:

`0 → -1`

and:

`0 → 1`.

---

## 173. Pending-Aware Transition Model

A route-aware execution model may condition second-leg probability on:

`t_pending`.

---

## 174. Scheduler-Aware Transition Model

Transition probability may also depend on scheduler state.

---

## 175. Execution Probability versus Commit

A probabilistic proposal does not itself commit a state.

The execution mechanism remains separate.

---

## 176. Differentiable Relaxation

A training model may use a continuous relaxation of ternary classes.

---

## 177. Relaxed State

Let:

`q ∈ Delta^2`

be a probability-simplex state.

This remains distinct from:

`t ∈ {-1,0,1}`.

---

## 178. Temperature Parameter

A softmax-like relaxation may use temperature:

`tau > 0`.

---

## 179. Low-Temperature Limit

Reducing:

`tau`

may sharpen class probabilities.

It does not by itself enforce execution routing.

---

## 180. Temperature Schedule

A training schedule may vary:

`tau[n]`.

---

## 181. Relaxation Schedule versus Physical Temperature

The distinction remains:

`classifier temperature ≠ thermodynamic temperature`.

---

## 182. Gumbel-Type Relaxation Boundary

A stochastic categorical relaxation may be used for gradient-based training.

Its random state and hard/soft semantics must be explicit.

---

## 183. Straight-Through Ternary Relaxation

A model may use hard forward classes and soft backward gradients.

---

## 184. Backward Approximation

The backward derivative is an optimization approximation.

It does not alter the forward semantic state.

---

## 185. Gradient Bias

Surrogate-gradient estimators may introduce biased parameter gradients.

This is an optimization property.

---

## 186. Surrogate Validation

A trained model should be evaluated using the actual hard forward semantics intended for deployment or reference execution.

---

## 187. Hard-Soft Gap

The difference between soft surrogate behavior and hard forward behavior may be measured explicitly.

---

## 188. Hard-Soft Consistency Loss

A regularizer may compare soft predictions with hard-state outputs.

---

## 189. Ternary Robustness

A classifier may be regularized for robustness to small continuous perturbations.

---

## 190. Input Perturbation

A small perturbation:

`delta x`

may be applied to the classifier input.

---

## 191. Robust Margin

A robust decision requires sufficient distance from class boundaries under the declared perturbation model.

---

## 192. Robustness versus Hysteresis

The distinction remains:

`robustness margin ≠ hysteresis`.

---

## 193. Robustness versus Neutral Region

Likewise:

`robustness margin ≠ active-neutral region`.

---

## 194. Adversarial Ternary Perturbation

A worst-case perturbation objective may be defined within an admissible norm ball.

The norm and domain must be explicit.

---

## 195. Physical Perturbation Boundary

A mathematical adversarial perturbation is not automatically a physically realizable atomic perturbation.

---

## 196. Noise Regularization

Classifier inputs may be perturbed with declared stochastic noise.

---

## 197. Noise Distribution

The noise distribution must be explicit.

---

## 198. Stochastic Consistency

A regularizer may encourage stable hard class under selected perturbations.

---

## 199. Symmetry Consistency

Canonical scalar ternary channels should remain unchanged under declared rigid spatial transformations.

---

## 200. Ternary Symmetry Loss

A consistency objective may penalize:

`t(gX) ≠ t(X)`

or compare corresponding classifier probabilities.

---

## 201. Permutation Consistency

Per-atom ternary channels must permute consistently with atom labels.

---

## 202. Global Ternary Invariance

Global scalar ternary state remains invariant under admissible atom permutation.

---

## 203. Reflection Consistency

If the channel is scalar invariant under:

`O(3)`,

reflection must leave the hard ternary state unchanged.

---

## 204. Spatial Rotation versus Polarity

The invariant remains:

`spatial rotation ≠ ternary polarity reversal`.

---

## 205. Ternary Equivariance Boundary

A non-scalar or orientation-dependent ternary channel requires an explicitly defined transformation rule.

The canonical scalar ternary channel remains invariant.

---

## 206. Ternary Regularization and Domain Detection

Out-of-domain state must remain separate from:

`-1/0/1`.

---

## 207. Domain Mask

A domain mask may determine whether ternary loss is evaluated.

Mask value:

`0`

does not mean neutral.

---

## 208. Abstention

If the model supports abstention, abstention must use a separate state outside the ternary kernel.

---

## 209. Rejection State

A rejected classifier result must not be encoded as:

`0`.

---

## 210. NaN Handling

NaN in classifier input, logits, probabilities, or loss is invalid numerical state.

---

## 211. Infinite Value Handling

Infinite classifier values require explicit numerical handling.

---

## 212. Reserved Encoding

Machine encodings outside:

`-1/0/1`

remain reserved or invalid.

---

## 213. Reserved-State Regularization Boundary

Reserved machine codes are not classes to be regularized.

They must be excluded structurally or rejected.

---

## 214. Ternary Metric

Regularization may be accompanied by metrics including:

- class occupancy;
- exact accuracy;
- neutral precision;
- neutral recall;
- switch rate;
- first-leg accuracy;
- second-leg accuracy;
- route-completion rate;
- direct-opposite violations.

---

## 215. Neutral Precision

Neutral precision measures how often predicted:

`0`

matches neutral reference among predicted-neutral cases.

---

## 216. Neutral Recall

Neutral recall measures how often reference:

`0`

is recovered.

---

## 217. Polar-Class Metrics

`-1`

and:

`1`

should be reported separately when their roles differ.

---

## 218. Transition Confusion Matrix

A transition matrix may report counts among all valid committed source/destination pairs.

---

## 219. Route Completion Rate

For opposite requests, a metric may measure successful completion through neutral mediation.

---

## 220. Direct-Opposite Violation Metric

The required conforming value remains:

`0`.

---

## 221. Neutral Residence Distribution

A model may report the empirical distribution of:

`L_0`.

---

## 222. Target Chatter Metric

A target chatter metric may report switches per unit sequence length.

---

## 223. Executed Chatter Metric

Executed-state chatter is measured separately.

---

## 224. Scheduler-Stratified Metrics

Metrics may be stratified by scheduler mode.

---

## 225. Resonance-Stratified Ternary Metrics

Metrics may be stratified by resonance region or coordinate range.

---

## 226. Species-Stratified Ternary Metrics

Local ternary performance may be stratified by species.

---

## 227. Structural-Stratified Metrics

Metrics may be stratified by local coordination or structure class.

---

## 228. Class-Balance Metric

Dataset and prediction occupancy distributions may both be reported.

---

## 229. Regularizer Logging

Training logs may record individual ternary regularization terms separately.

---

## 230. Total Ternary Regularization

A composite ternary regularizer may be:

`R_T = lambda_occ R_occ + lambda_margin R_margin + lambda_switch R_switch + lambda_route R_route + lambda_scale R_scale`.

The exact component set is specialization-specific.

---

## 231. Coefficient State

The coefficients:

`lambda_occ`

`lambda_margin`

`lambda_switch`

`lambda_route`

`lambda_scale`

are training hyperparameters unless explicitly learned.

---

## 232. Scheduled Coefficients

Regularization weights may vary during training.

---

## 233. Curriculum Ternary Training

A training curriculum may increase or decrease ternary regularization through training stages.

---

## 234. Stage Change versus Ternary Transition

The distinction remains:

`training-stage transition ≠ ternary-state transition`.

---

## 235. Learned Regularization Weight

A regularization weight may be learned under a constrained objective.

The anti-degeneracy mechanism must be explicit.

---

## 236. Ternary Regularization Provenance

Regularization definitions may carry canonical provenance classes.

---

## 237. Primary-Source Regularizer

A method adopted from established literature may carry:

`PRIMARY_SOURCE`.

---

## 238. Author-Defined Regularizer

A TR-EIF-specific active-neutral or routing regularizer may carry:

`AUTHOR_DEFINED`.

---

## 239. Derived Regularizer

A term deterministically constructed from defined state traces may carry:

`DERIVED`.

---

## 240. Calibrated Coefficient

A coefficient selected through calibration may carry:

`CALIBRATED`.

---

## 241. Benchmark Result

Measured occupancy, switching, route-completion, or violation statistics may carry:

`BENCHMARK`.

---

## 242. Test Fixture

Synthetic ternary trajectories with expected regularization values may carry:

`TEST_FIXTURE`.

---

## 243. Occupancy-Regularization Extension Rule

Any occupancy regularizer must define:

1. channel scope;
2. empirical occupancy;
3. target occupancy;
4. distance or divergence;
5. reduction;
6. coefficient.

---

## 244. Margin-Regularization Extension Rule

Any margin regularizer must define:

1. classifier variable;
2. decision boundaries;
3. margin definition;
4. neutral region;
5. coefficient;
6. invalid-state handling.

---

## 245. Transition-Regularization Extension Rule

Any transition regularizer must define:

1. target or executed state;
2. source state;
3. destination state;
4. allowed transitions;
5. forbidden transitions;
6. temporal coordinate;
7. coefficient.

---

## 246. Neutral-Residence Extension Rule

Any neutral-residence regularizer must define:

1. residence start;
2. residence end;
3. minimum or maximum duration where used;
4. scheduler relation;
5. coefficient.

---

## 247. Pending-Route Extension Rule

Any pending-route regularizer must define:

1. pending-state domain;
2. creation event;
3. retention;
4. completion;
5. cancellation where allowed;
6. consistency condition.

---

## 248. Multiscale-Ternary Extension Rule

Any multiscale ternary regularizer must define:

1. scale set;
2. state per scale;
3. cross-scale mapping;
4. permitted disagreement;
5. loss function;
6. coefficient.

---

## 249. Symmetry-Ternary Extension Rule

Any ternary symmetry regularizer must define:

1. transformation group;
2. channel transformation law;
3. hard-state or probability comparison;
4. reduction;
5. coefficient.

---

## 250. Surrogate-Ternary Extension Rule

Any continuous relaxation must define:

1. soft state;
2. hard decision;
3. forward semantics;
4. backward semantics;
5. temperature or equivalent parameters;
6. inference behavior.

---

## 251. Canonical Ternary-Regularization Invariants

Every conforming ternary regularization layer preserves:

1. exact semantic domain `{-1,0,1}`;

2. active-neutral `0`;

3. explicit target/execution separation;

4. explicit pending-state separation;

5. explicit classifier/semantic-state separation;

6. explicit soft/hard distinction;

7. explicit invalid-state handling;

8. explicit provenance.

---

## 252. Canonical Active-Neutral Invariants

The regularization layer preserves:

`0 ≠ NONE`

`0 ≠ INVALID`

`0 ≠ MASK`

`0 ≠ PADDING`

`0 ≠ NaN`

`0 ≠ uncertainty`

`0 ≠ zero message`

`0 ≠ zero force`

`0 ≠ zero energy`.

---

## 253. Canonical Execution Invariants

Committed execution preserves:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain impossible in conforming execution state.

---

## 254. Canonical Route Invariants

Opposite-polarity execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

First leg, neutral residence, pending state, and second leg remain separately represented.

---

## 255. Canonical Learning Boundary

A regularizer may shape:

- probabilities;
- thresholds;
- occupancy;
- persistence;
- transitions;
- route statistics.

It may not redefine the ternary kernel.

---

## 256. Canonical State Separation

The framework preserves:

`probability ≠ ternary state`

`entropy ≠ ternary neutral`

`margin ≠ ternary state`

`target ≠ executed state`

`pending ≠ neutral`

`regularizer ≠ execution rule`

`classifier temperature ≠ physical temperature`.

---

## 257. Canonical Scientific Distinctions

The ternary regularization layer preserves:

`resonance class ≠ ternary state`

`resonance window ≠ neutral region`

`target persistence ≠ neutral residence`

`classifier hysteresis ≠ neutral routing`

`spatial rotation ≠ ternary polarity reversal`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`phase coupling ≠ mechanical force`

`ternary state ≠ energy`.

---

## 258. Canonical Regularization Chain

A canonical classifier-training chain is:

`continuous source state`

`→ logits/probabilities`

`→ ternary decision`

`→ occupancy/transition statistics`

`→ ternary regularization`

`→ optimization`.

---

## 259. Canonical Execution-Regularization Chain

For execution-bound data:

`t_target`

`→ request`

`→ first leg`

`→ t_exec = 0`

`+ t_pending`

`→ neutral residence`

`→ second leg`

`→ completed executed state`.

Regularization may evaluate each stage separately.

---

## 260. Interface to Chapter 06

Chapter 06 develops Resonance Regularization.

It defines regularization of:

- resonance coordinates;
- resonance windows;
- persistence;
- multiscale resonance;
- resonance-to-ternary consistency.

---

## 261. Interface to Chapter 07

Chapter 07 develops Equivariance Constraints.

It defines symmetry constraints on continuous representations, resonance state, ternary channels, energy, force, and stress.

---

## 262. Interface to Chapter 08

Chapter 08 develops Uncertainty and Domain Detection.

It defines uncertainty-aware classification and explicit out-of-domain handling without reusing active neutral.

---

## 263. Interface to Chapter 09

Chapter 09 develops Optimization.

It consumes the composite:

`R_T`

together with the other loss terms to update trainable parameters.

---

## 264. Final Formal Structure

The ternary regularization layer may be represented as:

`TRG = (X_T, Z_T, P_T, R_occ, R_margin, R_switch, R_route, R_res, R_scale, R_sym, Lambda)`.

Here:

- `X_T` is exact ternary state;
- `Z_T` is continuous classifier state;
- `P_T` is the hard ternary mapping;
- `R_occ` is occupancy regularization;
- `R_margin` is decision-margin regularization;
- `R_switch` is switching regularization;
- `R_route` is route-consistency regularization;
- `R_res` is neutral-residence regularization;
- `R_scale` is multiscale consistency regularization;
- `R_sym` is symmetry consistency regularization;
- `Lambda` is the regularization-weight state.

A composite form is:

`R_T = sum_j lambda_j R_j`.

The exact semantic state remains:

`X_T ⊂ {-1,0,1}^M`.

---

## 265. Final Statement

Ternary regularization shapes learned ternary behavior without changing the exact semantics of the balanced ternary kernel.

The forward state remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Regularization may control:

- occupancy;
- class margins;
- hysteresis;
- persistence;
- target stability;
- neutral residence;
- route completion;
- multiscale consistency;
- symmetry consistency;
- surrogate-to-hard agreement.

The framework preserves:

`probability ≠ ternary state`

`entropy ≠ active neutral`

`margin ≠ ternary state`

`target ≠ executed state`

`pending ≠ neutral`

`regularization ≠ hard execution rule`

`classifier hysteresis ≠ neutral routing`

`resonance window ≠ neutral region`.

For execution-bound state, the committed topology remains:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

Opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

No loss coefficient, soft surrogate, occupancy prior, class weight, entropy term, or learned threshold may bypass the active-neutral execution invariant.

These definitions establish the ternary regularization layer required for Resonance Regularization developed in Chapter 06.
