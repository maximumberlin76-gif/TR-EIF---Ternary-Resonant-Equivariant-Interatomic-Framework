# Loss Functionals

## 1. Purpose

This chapter defines the loss-functional layer used to train TR-EIP models within TR-EIF.

The learning objective converts typed prediction errors, regularization terms, and model constraints into optimization quantities while preserving the semantic separation among:

- physical energy;
- mechanical force;
- stress;
- resonance state;
- ternary state;
- uncertainty;
- training loss;
- validation metrics.

The canonical learning chain is:

`training data`

`→ model prediction`

`→ typed residuals`

`→ loss functionals`

`→ regularization`

`→ total objective`

`→ parameter optimization`.

---

## 2. Parameterized Prediction

Let:

`M(X; Theta)`

denote a TR-EIP model with trainable parameter set:

`Theta`.

For sample:

`k`

the model prediction is:

`Y_k^pred = M(X_k; Theta)`.

Reference state is:

`Y_k^ref`.

---

## 3. Output State

A model output may contain:

`Y = (E, F, Sigma, X_R, X_T, U, O)`.

Here:

- `E` is energy;
- `F` is force;
- `Sigma` is stress;
- `X_R` is resonance state;
- `X_T` is ternary state;
- `U` is uncertainty state;
- `O` contains additional observables.

Each output is evaluated in its own state space.

---

## 4. Loss Functional

A loss functional maps prediction and reference state to a scalar optimization quantity:

`L: Y_pred × Y_ref → R`.

The result:

`L`

is an optimization quantity.

It is not physical energy.

---

## 5. Total Objective

A general total loss may be written:

`L_total = L_data + L_reg + L_constraint`.

The decomposition is model-specific.

---

## 6. Data Loss

The data term compares model outputs with reference outputs.

A generic form is:

`L_data = sum_a w_a L_a`.

Here:

`a`

indexes target types.

---

## 7. Regularization Loss

Regularization terms constrain parameter or state behavior beyond direct target matching.

Examples include:

- parameter regularization;
- ternary regularization;
- resonance regularization;
- equivariance regularization;
- smoothness regularization.

---

## 8. Constraint Penalty

A constraint penalty represents a soft approximation to a desired condition.

It remains distinct from a hard architectural invariant.

---

## 9. Hard Constraint Boundary

A hard invariant is enforced by model structure or admissible-state restriction.

A finite loss penalty does not make violation of a hard invariant semantically acceptable.

---

## 10. Loss Is Not Energy

The framework preserves:

`training loss ≠ physical energy`.

Even when energy error contributes to loss, the optimization objective remains a separate scalar.

---

## 11. Loss Is Not Resonance

The framework preserves:

`loss ≠ resonance state`.

---

## 12. Loss Is Not Ternary State

The framework preserves:

`loss ≠ ternary state`.

---

## 13. Loss Is Not Force

The framework preserves:

`loss ≠ mechanical force`.

---

## 14. Loss Gradient Is Not Mechanical Force

The parameter gradient:

`grad_Theta L`

is not:

`F = -grad_R E`.

These gradients belong to different spaces.

---

## 15. Per-Sample Loss

For sample:

`k`

define:

`L_k`.

The empirical objective over:

`K`

samples may be:

`L_emp = (1/K) sum_(k=1)^K L_k`.

---

## 16. Weighted Per-Sample Loss

For nonnegative sample weights:

`w_k`

a weighted objective may be:

`L_emp = [sum_k w_k L_k] / [sum_k w_k]`

when the denominator is nonzero.

---

## 17. Batch Loss

For batch:

`B`

define:

`L_B = A_B({L_k | k ∈ B})`.

The aggregation:

`A_B`

must be explicitly defined.

---

## 18. Mean Batch Loss

A common batch objective is:

`L_B = (1/|B|) sum_(k ∈ B) L_k`.

---

## 19. Sum Batch Loss

A summed batch objective may be used when the optimization schedule accounts for batch-size dependence.

---

## 20. Reduction Semantics

Loss reduction may be performed over:

- samples;
- atoms;
- vector components;
- tensor components;
- transitions;
- time steps.

The reduction axes must be explicit.

---

## 21. Target Availability

If a target is unavailable for one sample, its loss term must be masked explicitly.

Missing supervision is not numerical zero target.

---

## 22. Target Mask

Let:

`m_k,a ∈ {0,1}`

denote target availability.

Then a masked target loss may use:

`m_k,a L_k,a`.

The mask is computational metadata.

It is not ternary state.

---

## 23. Missing Target Boundary

The framework preserves:

`missing target ≠ ternary 0`.

---

## 24. Energy Residual

For sample:

`k`:

`Delta E_k = E_k^pred - E_k^ref`.

---

## 25. Absolute Energy Loss

A per-sample absolute energy loss may be:

`L_E,k = |Delta E_k|`.

---

## 26. Squared Energy Loss

A squared energy loss may be:

`L_E,k = (Delta E_k)^2`.

---

## 27. Energy MAE Objective

For:

`K`

energy-labeled samples:

`L_E,MAE = (1/K) sum_k |Delta E_k|`.

---

## 28. Energy MSE Objective

A mean squared energy objective is:

`L_E,MSE = (1/K) sum_k (Delta E_k)^2`.

---

## 29. Energy RMSE Metric

A corresponding reporting metric may be:

`RMSE_E = sqrt(L_E,MSE)`.

The metric and optimized objective need not be identical.

---

## 30. Energy per Atom Residual

For:

`N_k > 0`

define:

`Delta e_k = Delta E_k / N_k`.

---

## 31. Energy per Atom Loss

A normalized energy objective may use:

`L_E/N = (1/K) sum_k |Delta E_k| / N_k`.

---

## 32. Total-Energy versus Per-Atom Loss

The choice changes relative weighting of differently sized systems.

It must therefore be explicit.

---

## 33. Relative Energy Error

A relative energy residual may use a reference scale:

`s_E,k > 0`.

For example:

`r_E,k = Delta E_k / s_E,k`.

---

## 34. Energy Reference Offset

If energy labels differ by an arbitrary constant reference, the loss must account for the adopted reference convention.

---

## 35. Species Reference Offset

Species-specific baseline energies may be subtracted before residual evaluation.

The reference-energy mapping must remain explicit.

---

## 36. Force Residual

For atom:

`i`

in sample:

`k`:

`Delta F_ki = F_ki^pred - F_ki^ref`.

---

## 37. Force Component Residual

For Cartesian component:

`a`:

`Delta F_kia = F_kia^pred - F_kia^ref`.

---

## 38. Force Component MSE

A componentwise force loss may be:

`L_F = [1 / sum_k 3N_k] sum_k sum_i ||Delta F_ki||^2`.

---

## 39. Force Vector MAE

A vector-norm force loss may be:

`L_F,vec = [1 / sum_k N_k] sum_k sum_i ||Delta F_ki||`.

---

## 40. Force Component MAE

A component MAE may average:

`|Delta F_kia|`

over all atomic components.

---

## 41. Force Loss Normalization

Force loss may normalize by:

- atom count;
- component count;
- configuration count;
- reference-force scale.

The chosen convention changes optimization weighting.

---

## 42. Force Direction Error

A directional loss may compare predicted and reference force direction when both magnitudes exceed a declared threshold.

---

## 43. Force Magnitude Error

A magnitude loss may compare:

`||F_pred||`

and:

`||F_ref||`.

---

## 44. Force Vector Error versus Magnitude Error

The distinction remains:

`vector error ≠ magnitude error`.

A model may predict correct magnitude and incorrect direction.

---

## 45. Conservative Force Loss

For an energy-derived force:

`F_pred = -grad_R E_pred`.

Force loss then optimizes derivatives of the learned energy surface.

---

## 46. Direct Force Loss

For a direct force head:

`F_pred = P_F(X)`.

The force loss acts directly on the vector output.

---

## 47. Energy-Force Consistency Loss

For a model exposing both energy and a direct force head:

`L_EF = A(||F_direct + grad_R E||)`.

This term measures consistency between the two outputs.

---

## 48. Energy-Force Consistency Is Not Force Loss

The distinction is:

`reference force loss ≠ internal energy-force consistency loss`.

One compares against data.

The other compares two model outputs.

---

## 49. Stress Residual

For sample:

`k`:

`Delta Sigma_k = Sigma_k^pred - Sigma_k^ref`.

---

## 50. Stress Component Loss

A stress loss may average squared or absolute differences over stored tensor components.

---

## 51. Tensor-Norm Stress Loss

A tensor loss may use Frobenius norm:

`||Delta Sigma||_F`.

---

## 52. Stress Symmetry Handling

If the reported stress tensor is symmetric, the loss convention must define whether off-diagonal terms are counted once or twice.

---

## 53. Stress Unit Scaling

Stress often has a numerical scale different from energy and force.

Loss normalization must account for the declared unit system and weighting strategy.

---

## 54. Pressure Loss

If scalar pressure is a supervised observable, its loss remains distinct from full stress loss.

---

## 55. Pressure versus Stress Objective

The framework preserves:

`pressure loss ≠ full stress-tensor loss`.

---

## 56. Resonance Residual

For continuous resonance state:

`r_k^pred`

and:

`r_k^ref`

define an appropriate residual in:

`X_R`.

---

## 57. Scalar Resonance Loss

For scalar resonance coordinate:

`r`:

`L_R = |r_pred - r_ref|`

or a declared squared alternative.

---

## 58. Vector Resonance Loss

For equivariant vector resonance state:

`L_R,v = ||r_v^pred - r_v^ref||`.

---

## 59. Tensor Resonance Loss

For tensor resonance:

`L_R,T = ||R_T^pred - R_T^ref||`.

---

## 60. Mixed Resonance State

A resonance state containing several representation types requires blockwise loss composition.

---

## 61. Resonance Representation Weight

Each resonance block may carry its own coefficient.

---

## 62. Resonance Window Classification Loss

If resonance classes are supervised:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

may be trained through a categorical loss.

---

## 63. Resonance Class versus Ternary Loss

The distinction remains:

`resonance-class loss ≠ ternary-state loss`.

---

## 64. Ternary Target

A ternary target belongs to:

`{-1,0,1}`.

---

## 65. Ternary Classification State

A trainable classifier may produce continuous logits:

`z = (z_-, z_0, z_+)`.

---

## 66. Ternary Probability State

A probability state may be:

`p = (p_-, p_0, p_+)`.

These are not ternary semantic states.

---

## 67. Hard Ternary State

A decision map:

`D_T`

produces:

`t_pred ∈ {-1,0,1}`.

---

## 68. Ternary Categorical Loss

For reference class:

`t_ref`

a categorical objective may operate on logits or probabilities before hard classification.

---

## 69. Cross-Entropy Form

For encoded reference class:

`c_ref`

one possible loss is:

`L_T = -log p_(c_ref)`.

The probability representation is an optimization construct.

---

## 70. Class-Weighted Ternary Loss

For class weight:

`w_c`

the categorical loss may be:

`L_T = -w_(c_ref) log p_(c_ref)`.

---

## 71. Active-Neutral Class Weight

The active-neutral class:

`0`

may have its own weight:

`w_0`.

It must not be treated as missing state.

---

## 72. Exact Ternary Mismatch

A reporting error may use:

`I(t_pred ≠ t_ref)`.

---

## 73. Ternary Confusion Matrix

A confusion matrix should preserve the exact class ordering:

`-1`

`0`

`1`.

---

## 74. Ternary Transition Loss

For sequential data, a loss may evaluate predicted transition behavior.

---

## 75. Target Transition Loss

A target-state transition loss applies to:

`t_target`.

---

## 76. Executed Transition Loss

An execution-state transition loss applies to:

`t_exec`.

These objectives remain distinct.

---

## 77. Pending-State Loss

A separate loss may supervise:

`t_pending`.

---

## 78. Target/Execution Separation

Loss tensors and labels must preserve:

`target ≠ executed state`.

---

## 79. Direct-Opposite Execution Invariant

No loss functional may redefine committed:

`-1 → 1`

or:

`1 → -1`

as valid.

---

## 80. Execution Violation Penalty

A diagnostic penalty may count direct-opposite predictions.

The required valid count remains:

`0`.

---

## 81. Hard Execution Enforcement

The preferred execution architecture may make direct-opposite committed transitions unrepresentable.

Then the invariant is structural rather than statistical.

---

## 82. Neutral-Mediated Transition Objective

Sequential training may explicitly reward or supervise:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 83. First-Leg Loss

A first-leg objective may supervise transition into:

`0`.

---

## 84. Neutral-Residence Loss

A sequential loss may supervise persistence of active neutral before second-leg completion.

---

## 85. Second-Leg Loss

A second-leg objective may supervise completion from:

`0`

to the pending destination.

---

## 86. Neutral-State Occupancy

A training objective may regulate occupancy frequency of:

`0`.

This is developed further in Chapter 05.

---

## 87. Ternary Occupancy Is Not Class Balance by Identity

Dataset frequency and desired model occupancy may differ.

The objective must define the intended relation.

---

## 88. Binary Mask versus Ternary State

A loss mask value:

`0`

is not active-neutral ternary:

`0`.

---

## 89. Soft Ternary Surrogate

A continuous surrogate may approximate exact ternary classification for gradient-based optimization.

---

## 90. Surrogate Loss

The surrogate loss acts on the continuous pre-classification state.

The hard semantic output remains separate.

---

## 91. Straight-Through Boundary

A straight-through estimator may use:

- hard forward state;
- surrogate backward derivative.

Forward and backward semantics remain distinct.

---

## 92. Multi-Objective Loss

A full mechanical and TR objective may be:

`L_data = w_E L_E + w_F L_F + w_S L_S + w_R L_R + w_T L_T`.

---

## 93. Loss Weight Vector

Define:

`w = (w_E, w_F, w_S, w_R, w_T)`.

The weights determine optimization tradeoffs.

---

## 94. Nonnegative Loss Weights

A standard objective may require:

`w_a ≥ 0`.

Other formulations must explicitly define their semantics.

---

## 95. Zero Loss Weight

Setting:

`w_a = 0`

removes that term from the current optimization objective.

It does not delete the output from the model architecture.

---

## 96. Fixed Loss Weights

Weights may remain constant throughout training.

---

## 97. Scheduled Loss Weights

Weights may vary with training step:

`w_a = w_a[n]`.

---

## 98. Adaptive Loss Weights

Weights may be generated dynamically from observed loss scales, uncertainties, or gradient statistics.

The adaptation rule must be explicit.

---

## 99. Loss-Scale Normalization

Different terms may be normalized before weighting.

---

## 100. Reference-Scale Normalization

For quantity:

`y`

a normalized residual may use:

`(y_pred - y_ref) / s_y`.

---

## 101. Dimensionless Loss

Loss terms may be made dimensionless through explicit scaling.

---

## 102. Dimensional Loss

A loss may retain physical squared units internally.

When terms with different dimensions are summed, coefficients must carry the corresponding inverse dimensions or normalization must be introduced.

---

## 103. Unit-Aware Objective

The objective construction must remain dimensionally interpretable.

---

## 104. Extensive versus Intensive Weighting

Total energy and per-atom energy produce different weighting across system sizes.

The choice belongs to the loss definition.

---

## 105. Configuration Weighting

A model may weight each configuration equally.

---

## 106. Atom Weighting

A model may instead weight each atom equally through force or local-energy reductions.

---

## 107. Species Weighting

Residuals may be weighted by species.

---

## 108. Composition Weighting

Configurations may be weighted by composition.

---

## 109. Thermodynamic Weighting

State regions may receive different loss weights.

---

## 110. Provenance Weighting

Targets from different provenance classes may receive different weights when explicitly defined.

---

## 111. Uncertainty-Weighted Loss

If reference uncertainty:

`sigma_y`

is available, a residual may be weighted by a function of:

`sigma_y`.

---

## 112. Inverse-Variance Weighting

One possible form is:

`w_y = 1 / sigma_y^2`

for positive:

`sigma_y`.

The probabilistic assumptions must be explicit.

---

## 113. Heteroscedastic Loss

A model may predict state-dependent uncertainty and optimize a probabilistic likelihood objective.

---

## 114. Negative Log-Likelihood

A probabilistic loss may be defined as a negative log-likelihood under an explicitly selected distribution.

---

## 115. Likelihood Model

The likelihood must define:

- distribution family;
- parameterization;
- units;
- independence assumptions.

---

## 116. Uncertainty Is Not Residual

The framework preserves:

`predicted uncertainty ≠ observed error`.

---

## 117. Uncertainty Is Not Neutral

The framework preserves:

`uncertainty ≠ ternary 0`.

---

## 118. Robust Loss

A robust loss may reduce sensitivity to large residuals.

---

## 119. Huber-Type Loss

A piecewise quadratic-linear loss may be used with threshold:

`delta`.

The exact formula and units must be explicit.

---

## 120. Absolute Loss Robustness

Absolute error grows linearly with residual magnitude.

---

## 121. Squared Loss Sensitivity

Squared loss weights large residuals more strongly.

---

## 122. Robustness versus Outlier Removal

Using a robust loss is distinct from removing samples from the dataset.

---

## 123. Outlier Weighting

A sample may receive reduced weight according to a declared quality or uncertainty rule.

---

## 124. Parameter Regularization

A parameter regularizer acts on:

`Theta`.

---

## 125. L2 Parameter Penalty

One possible regularizer is:

`R_2 = ||Theta||^2`.

---

## 126. L1 Parameter Penalty

A sparsity-promoting regularizer may use:

`R_1 = sum_j |Theta_j|`.

---

## 127. Parameter Norm versus Physical Energy

The framework preserves:

`parameter norm ≠ physical energy`.

---

## 128. Weight Decay

Weight decay may be implemented directly by the optimizer or through an explicit regularizer.

The two implementations need not be numerically identical for every optimizer.

---

## 129. Representation Regularization

A model may regularize latent representation norms or statistics.

---

## 130. Representation Norm versus Physical Quantity

A latent norm is not energy, force, coherence, or resonance by identity.

---

## 131. Smoothness Loss

A smoothness objective may penalize rapid changes in selected model outputs with respect to state variables.

---

## 132. Coordinate Smoothness

A coordinate-smoothness term may penalize large derivatives or curvature.

---

## 133. Energy Smoothness

Energy smoothness may be relevant near cutoffs or learned switching regions.

---

## 134. Force Smoothness

Force smoothness may penalize rapid spatial variation.

---

## 135. Stress Smoothness

Stress smoothness may apply over nearby cell states.

---

## 136. Temporal Smoothness

For time-ordered data, a loss may penalize changes between consecutive predicted states.

---

## 137. Temporal Smoothness versus Physical Dynamics

A temporal regularizer must not be substituted for an actual equation of motion.

---

## 138. Resonance Smoothness

A resonance trajectory may be regularized against unstructured rapid changes.

This is developed in Chapter 06.

---

## 139. Ternary Smoothness Boundary

A categorical ternary state cannot be made continuously smooth by identity.

Persistence or switching penalties must respect exact categorical semantics.

---

## 140. Equivariance Loss

For transformation:

`g`

define:

`Y_1 = M(gX)`

and:

`Y_2 = rho_Y(g)M(X)`.

An equivariance residual compares:

`Y_1`

and:

`Y_2`.

---

## 141. Scalar Invariance Loss

For scalar energy:

`L_eq,E = |E(gX) - E(X)|`.

---

## 142. Force Equivariance Loss

For force:

`L_eq,F = ||F(gX) - rho_F(g)F(X)||`.

---

## 143. Stress Equivariance Loss

For stress:

`L_eq,S = ||Sigma(gX) - Q Sigma(X) Q^T||`.

---

## 144. Resonance Equivariance Loss

For resonance:

`L_eq,R = d_R(P_R(gX), rho_R(g)P_R(X))`.

---

## 145. Ternary Invariance Loss

For canonical scalar ternary channel:

`t(gX) = t(X)`.

A categorical mismatch may be used as a validation or surrogate training signal.

---

## 146. Architectural versus Loss-Based Equivariance

The framework preserves:

`architectural equivariance ≠ equivariance penalty`.

---

## 147. Permutation Loss

A transformation loss may also verify atom-permutation behavior.

---

## 148. Energy Permutation Loss

Global energy should remain invariant under admissible permutation.

---

## 149. Force Permutation Loss

Forces must permute with atoms.

---

## 150. Graph Consistency Loss

If graph construction or edge scoring is learned, a loss may constrain consistency under geometric and permutation transformations.

---

## 151. Graph Loss versus Physical Energy

The framework preserves:

`graph loss ≠ physical energy`.

---

## 152. Conservative Consistency Loss

A model may penalize:

`F_direct + grad_R E`.

---

## 153. Net-Force Constraint Loss

For isolated internal forces, a soft numerical objective may penalize:

`||sum_i F_i||`.

---

## 154. Torque Constraint Loss

A rotationally invariant isolated system may include a soft torque residual where appropriate.

---

## 155. Hard versus Soft Mechanical Consistency

When a property follows structurally from invariant energy differentiation, it need not be learned through a penalty.

---

## 156. Energy Conservation Loss Boundary

Trajectory energy conservation is a property of the coupled dynamical model and numerical integrator.

It must not be conflated with static energy-fitting loss.

---

## 157. MD Trajectory Loss

A later learning setup may compare predicted trajectories with references.

Such a loss depends on the molecular-dynamics layer, not only the static interatomic model.

---

## 158. Multi-Step Loss

A multi-step rollout objective may compare states after repeated model/integrator applications.

---

## 159. Single-Step versus Multi-Step Loss

The distinction is:

`single-step fitting ≠ rollout fitting`.

---

## 160. Structural Loss

A model may include losses on structural observables.

---

## 161. Pair-Distribution Loss

A loss may compare pair-distribution-like observables if a differentiable or estimable mapping exists.

---

## 162. Coordination Loss

A coordination-based loss may compare derived local structure.

The coordination definition must be explicit.

---

## 163. Observable Loss

For derived observable:

`O = P_O(Y)`

define:

`L_O = d_O(O_pred, O_ref)`.

---

## 164. Observable Mapping

The map:

`P_O`

must remain part of the objective specification.

---

## 165. Loss on Derived Quantity

A derived observable may depend on many model outputs.

Gradient flow follows the declared computational graph.

---

## 166. Loss Decomposition

A total objective may be decomposed by target family:

`L_total = L_mech + L_TR + L_sym + L_reg`.

---

## 167. Mechanical Loss

Define:

`L_mech = w_E L_E + w_F L_F + w_S L_S`.

---

## 168. TR Loss

Define:

`L_TR = w_R L_R + w_T L_T`.

---

## 169. Symmetry Loss

A symmetry term may combine equivariance and permutation residuals.

---

## 170. Regularization Loss

A regularization block may include parameter, smoothness, ternary, and resonance terms.

---

## 171. Hierarchical Objective

A training process may optimize different loss groups in separate stages.

---

## 172. Pretraining Objective

A pretraining stage may optimize representation or mechanical targets.

---

## 173. Resonance Fine-Tuning Objective

A later stage may emphasize resonance-related targets.

---

## 174. Ternary Fine-Tuning Objective

Another stage may emphasize ternary classification or transition behavior.

---

## 175. Joint Objective

A final stage may optimize all declared terms jointly.

---

## 176. Curriculum Loss

Loss weights may evolve according to a curriculum.

The schedule must be explicit.

---

## 177. Stage Transition

A change in training objective is an optimization protocol event.

It is not a ternary state transition.

---

## 178. Loss Schedule

For training step:

`n`

the objective may be:

`L_total[n]`.

---

## 179. Dynamic Weighting

A dynamic weighting algorithm may use current residual magnitudes or gradient norms.

---

## 180. Gradient-Norm Balancing

A multi-task optimizer may balance objectives by their parameter-gradient magnitudes.

---

## 181. Loss-Value Balancing

Alternatively, objective scales may be balanced by running statistics of loss values.

---

## 182. Gradient Conflict

Different loss terms may produce opposing parameter gradients.

This is an optimization phenomenon.

---

## 183. Gradient Conflict versus Physical Force Opposition

The distinction remains:

`opposing parameter gradients ≠ opposing mechanical forces`.

---

## 184. Pareto Objective

A multi-objective formulation may treat several loss terms without reducing them immediately to one weighted scalar.

---

## 185. Scalarized Objective

A weighted sum converts multiple objectives into one scalar objective.

---

## 186. Constraint-Based Objective

Some quantities may remain explicit constraints instead of penalties.

---

## 187. Admissible Parameter Space

Define:

`Theta_adm`.

Optimization proceeds only within the hard-admissible parameter space.

---

## 188. Hard Symmetry Constraint

An equivariant architecture may guarantee transformation laws for all:

`Theta ∈ Theta_adm`.

---

## 189. Hard Ternary Constraint

The exact output domain remains:

`-1/0/1`.

---

## 190. Hard Execution Constraint

Committed state topology remains:

`-1 ↔ 0 ↔ 1`.

---

## 191. Hard Conservative Constraint

For a conservative member:

`F = -grad_R E`.

---

## 192. Soft Loss Cannot Override Hard Constraint

No finite objective weight authorizes violation of these structural invariants.

---

## 193. Loss Masking

A loss term may be masked by:

- target availability;
- sample validity;
- domain membership;
- training policy.

---

## 194. Domain Mask

An out-of-domain sample may be excluded from a target loss according to the declared protocol.

---

## 195. Mask versus Neutral

The framework preserves:

`loss mask 0 ≠ ternary neutral 0`.

---

## 196. NaN Loss

A non-finite loss is an invalid numerical event.

It is not a valid training state.

---

## 197. Infinite Loss

Infinite loss requires explicit numerical handling.

---

## 198. Numerical Epsilon

Loss formulas involving division, logarithms, or norms may use:

`epsilon`.

The numerical role and value must be explicit.

---

## 199. Log Probability Floor

A probability-based loss may clamp or stabilize logarithms.

This modifies numerical implementation, not class semantics.

---

## 200. Loss Precision

The loss may be accumulated in a precision different from model forward precision.

---

## 201. Mixed-Precision Loss

Mixed-precision training may use higher-precision accumulation for selected objectives.

---

## 202. Loss Scaling

Gradient scaling may multiply the optimization loss temporarily.

The scale factor does not change the semantic objective after inverse scaling.

---

## 203. Gradient Clipping Boundary

Gradient clipping acts on:

`grad_Theta L`.

It does not act on physical force unless a separate mechanical operation is defined.

---

## 204. Loss Determinism

For deterministic training, identical:

- model state;
- batch;
- parameters;
- random state;
- arithmetic;
- reduction order

must reproduce the declared loss.

---

## 205. Reduction Ordering

Floating-point loss sums may depend on reduction order.

Exact replay may therefore require deterministic aggregation.

---

## 206. Distributed Reduction

Distributed training may combine loss statistics across devices or processes.

The reduction contract must remain explicit.

---

## 207. Global Batch Objective

A distributed global mean must define the denominator across all participating samples or components.

---

## 208. Local Batch Objective

A per-device mean followed by equal device averaging is not necessarily identical when batch sizes differ.

---

## 209. Sample Count Weighting

Distributed reductions should preserve the declared sample/component weighting.

---

## 210. Missing-Target Distributed Reduction

Availability counts must be aggregated consistently for partially supervised batches.

---

## 211. Loss Logging

Training logs may record:

- total loss;
- component losses;
- regularizers;
- constraint residuals;
- learning rate;
- gradient statistics.

---

## 212. Loss Log Units

When a loss component retains dimensional units, those units should be identified.

---

## 213. Reporting Metric

A metric is a reported evaluation quantity.

It need not contribute to optimization.

---

## 214. Loss versus Metric

The framework preserves:

`optimized loss ≠ reporting metric`.

---

## 215. Validation Loss

A validation loss evaluates the same or another declared objective on:

`D_val`

without parameter update.

---

## 216. Test Loss

A test loss evaluates the declared test objective on:

`D_test`.

---

## 217. Model-Selection Metric

A model may be selected using:

- validation loss;
- energy MAE;
- force RMSE;
- composite score;
- another declared metric.

---

## 218. Composite Selection Score

A composite score must define all component scaling and weights.

---

## 219. Early-Stopping Loss

Early stopping may monitor one validation metric.

---

## 220. Loss Plateau

A plateau in loss is an optimization observation.

It is not physical equilibrium.

---

## 221. Minimum Training Loss

A minimum of the training objective is a point in parameter space.

It is not a minimum of the atomic potential-energy surface.

---

## 222. Optimization Landscape

The function:

`Theta → L(Theta)`

defines an optimization landscape.

---

## 223. Energy Landscape

The function:

`R → E(R)`

defines an atomic potential-energy landscape.

---

## 224. Landscape Separation

The framework preserves:

`optimization landscape ≠ physical energy landscape`.

---

## 225. Parameter Hessian

Second derivatives:

`d^2L / dTheta^2`

describe local optimization curvature.

---

## 226. Energy Hessian

Second derivatives:

`d^2E / dR^2`

describe local atomic-energy curvature.

---

## 227. Hessian Separation

The framework preserves:

`loss Hessian ≠ energy Hessian`.

---

## 228. Regularization Coefficient

A regularization term may use:

`lambda ≥ 0`.

---

## 229. Coefficient Units

If the regularized quantity is dimensional, the coefficient must restore compatible objective units or the term must be normalized.

---

## 230. Hyperparameter Status

Loss weights and regularization coefficients are training hyperparameters unless explicitly learned.

---

## 231. Learned Loss Weight

A loss weight may itself be trainable under a declared formulation.

Its optimization must avoid degenerate trivial reduction of objective weight unless the formulation prevents it.

---

## 232. Constraint Multiplier

A constrained optimization method may introduce Lagrange multipliers or penalty parameters.

---

## 233. Lagrangian Objective

A constrained problem may use a Lagrangian-type construction:

`L_aug = L_data + sum_j lambda_j C_j`.

The exact method belongs to the optimization layer.

---

## 234. Penalty Method

Constraint violation may be penalized quadratically or through another declared function.

---

## 235. Barrier Method

A barrier may restrict optimization near an inadmissible boundary.

---

## 236. Projection Method

Parameters may be projected onto:

`Theta_adm`

after an update.

---

## 237. Loss Provenance

Loss definitions may carry provenance when derived from external methods or introduced by the framework.

---

## 238. Primary-Source Loss

A loss formulation adopted from established literature may carry:

`PRIMARY_SOURCE`.

---

## 239. Author-Defined Loss

A TR-EIF-specific loss coupling may carry:

`AUTHOR_DEFINED`.

---

## 240. Derived Loss

A loss computed deterministically from established residuals may carry:

`DERIVED`.

---

## 241. Calibrated Loss Weight

A loss coefficient selected through calibration may carry:

`CALIBRATED`.

---

## 242. Benchmark Loss Result

Measured loss values on a declared benchmark dataset may carry:

`BENCHMARK`.

---

## 243. Test Fixture Loss

Expected loss values for synthetic deterministic samples may carry:

`TEST_FIXTURE`.

---

## 244. Energy-Loss Extension Rule

Any new energy loss must define:

1. target energy semantics;
2. total/per-atom status;
3. units;
4. residual;
5. normalization;
6. reduction;
7. weight.

---

## 245. Force-Loss Extension Rule

Any new force loss must define:

1. vector/component representation;
2. units;
3. atom weighting;
4. component weighting;
5. reduction;
6. normalization;
7. weight.

---

## 246. Stress-Loss Extension Rule

Any new stress loss must define:

1. tensor type;
2. stored components;
3. units;
4. tensor norm or component reduction;
5. sign convention;
6. weight.

---

## 247. Resonance-Loss Extension Rule

Any resonance loss must define:

1. resonance state space;
2. representation type;
3. units;
4. metric;
5. scale;
6. aggregation.

---

## 248. Ternary-Loss Extension Rule

Any ternary loss must define:

1. target or executed state;
2. exact class domain;
3. logits/probability representation where used;
4. class weighting;
5. active-neutral handling;
6. invalid-state handling.

---

## 249. Transition-Loss Extension Rule

Any transition loss must define:

1. source state;
2. destination state;
3. target/executed semantics;
4. pending-state handling;
5. temporal coordinate;
6. direct-opposite invariant.

---

## 250. Multi-Objective Extension Rule

Any multi-objective loss must define:

1. component set;
2. component units;
3. normalization;
4. weights;
5. scheduling;
6. reduction;
7. selection metric.

---

## 251. Constraint-Loss Extension Rule

Any soft constraint must define:

1. constrained quantity;
2. residual;
3. penalty function;
4. coefficient;
5. relation to hard invariants.

---

## 252. Canonical Loss Invariants

Every conforming loss-functional layer preserves:

1. explicit target typing;

2. explicit residual definition;

3. explicit reduction;

4. explicit unit handling;

5. explicit weighting;

6. explicit masking;

7. explicit hard/soft constraint separation;

8. explicit provenance where applicable.

---

## 253. Canonical Mechanical Loss Invariants

Energy loss acts on scalar energy.

Force loss acts on vector force.

Stress loss acts on tensor stress.

The state types remain distinct.

---

## 254. Canonical Ternary Loss Invariants

Ternary supervision preserves exact semantic classes:

`-1/0/1`.

The state:

`0`

remains active neutral.

Missing or masked labels remain separate.

---

## 255. Canonical Execution-Loss Invariants

Sequential execution losses preserve:

`target ≠ executed state`

and:

`pending ≠ active neutral`.

Committed direct:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 256. Canonical Conservative Invariant

For a conservative model:

`F = -grad_R E`.

No weighting of loss terms changes this formal architecture relation.

---

## 257. Canonical Symmetry Invariant

Loss construction does not change the declared spatial and permutation transformation laws.

---

## 258. Canonical State Separation

The loss layer preserves:

`loss ≠ energy`

`loss gradient ≠ force`

`loss minimum ≠ energy minimum`

`class probability ≠ ternary state`

`mask ≠ active neutral`

`uncertainty ≠ residual`

`regularizer ≠ physical observable`.

---

## 259. Canonical Scientific Distinctions

The loss layer preserves:

`equivariance ≠ conservativity`

`architectural equivariance ≠ equivariance penalty`

`optimization convergence ≠ physical equilibrium`

`optimization stability ≠ dynamical stability`

`representation similarity ≠ coherence`

`resonance class ≠ ternary state`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 260. Canonical Loss Chain

For one target:

`reference quantity`

`+ predicted quantity`

`→ typed residual`

`→ normalized residual`

`→ loss term`

`→ weighted contribution`.

---

## 261. Canonical Multi-Objective Chain

For multiple targets:

`L_E`

`+ L_F`

`+ L_S`

`+ L_R`

`+ L_T`

`+ regularization`

`→ L_total`.

---

## 262. Canonical Optimization Interface

The loss layer exports:

`L_total(Theta)`

and:

`grad_Theta L_total`

to the optimization layer.

---

## 263. Interface to Chapter 04

Chapter 04 develops Energy-Force-Stress Training.

It specializes the mechanical loss terms and derivative paths defined here.

---

## 264. Interface to Chapter 05

Chapter 05 develops Ternary Regularization.

It defines specialized loss terms for:

- ternary occupancy;
- neutral-state structure;
- switching;
- persistence;
- routing consistency.

---

## 265. Interface to Chapter 06

Chapter 06 develops Resonance Regularization.

It defines specialized penalties on:

- resonance coordinates;
- windows;
- persistence;
- multiscale consistency.

---

## 266. Interface to Chapter 07

Chapter 07 develops Equivariance Constraints.

It formalizes transformation residuals and symmetry-related regularization.

---

## 267. Interface to Chapter 08

Chapter 08 develops Uncertainty and Domain Detection.

It defines uncertainty-aware objectives and domain-aware weighting.

---

## 268. Interface to Chapter 09

Chapter 09 develops Optimization.

It consumes:

`L_total`

and its parameter gradients to update:

`Theta`.

---

## 269. Final Formal Structure

The loss-functional layer may be represented as:

`LF = (L_E, L_F, L_S, L_R, L_T, L_O, L_reg, L_constraint, W, M, A)`.

Here:

- `L_E` is energy loss;
- `L_F` is force loss;
- `L_S` is stress loss;
- `L_R` is resonance loss;
- `L_T` is ternary loss;
- `L_O` is auxiliary observable loss;
- `L_reg` is regularization;
- `L_constraint` is soft constraint loss;
- `W` is the loss-weight state;
- `M` is masking state;
- `A` is reduction and aggregation semantics.

A canonical scalarized objective is:

`L_total = w_E L_E + w_F L_F + w_S L_S + w_R L_R + w_T L_T + L_reg + L_constraint`.

Optimization remains constrained to:

`Theta ∈ Theta_adm`.

---

## 270. Final Statement

Loss functionals provide the scalar optimization interface between typed TR-EIP predictions and their reference targets.

Energy residuals remain scalar.

Force residuals remain vector-derived quantities.

Stress residuals remain tensor-derived quantities.

Resonance remains separately typed.

Ternary state remains exactly:

`-1/0/1`.

The state:

`0`

remains active neutral.

A loss mask, missing target, invalid sample, probability, or zero-valued residual does not become ternary neutral.

The framework preserves:

`training loss ≠ physical energy`

`parameter gradient ≠ mechanical force`

`loss minimum ≠ atomic energy minimum`

`probability ≠ ternary state`

`target ≠ executed state`

`equivariance penalty ≠ architectural equivariance`

`regularization ≠ hard invariant`.

For conservative models:

`F = -grad_R E`.

For execution-bound ternary state:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

remain the canonical opposite-polarity routes.

No optimization coefficient, loss weighting, surrogate gradient, or regularization term may redefine the balanced ternary kernel or bypass active-neutral execution.

These definitions establish the objective-function layer required for Energy-Force-Stress Training developed in Chapter 04.
