# Optimization

## 1. Purpose

This chapter defines the optimization layer of the TR-EIP model family within TR-EIF.

Optimization acts on the trainable parameter set while preserving the mathematical, ternary, resonance, equivariance, mechanical, uncertainty, and domain constraints established in the preceding volumes and chapters.

The canonical training chain is:

`training data`

`→ model evaluation`

`→ typed predictions`

`→ loss evaluation`

`→ regularization and constraints`

`→ parameter gradients`

`→ optimizer state`

`→ parameter update`

`→ validation`.

Optimization changes model parameters.

It does not redefine the semantic state spaces of TR-EIF.

---

## 2. Trainable Parameter Set

Let:

`Theta`

denote the complete trainable parameter set.

A structured decomposition may be:

`Theta = (Theta_EQ, Theta_R, Theta_T, Theta_E, Theta_F, Theta_S, Theta_U, Theta_aux)`.

Here:

- `Theta_EQ` parameterizes equivariant representations;
- `Theta_R` parameterizes resonance mappings;
- `Theta_T` parameterizes ternary-target mappings;
- `Theta_E` parameterizes energy prediction;
- `Theta_F` parameterizes a direct force branch where present;
- `Theta_S` parameterizes a direct stress branch where present;
- `Theta_U` parameterizes uncertainty and domain components;
- `Theta_aux` contains additional trainable parameters explicitly declared by the architecture.

---

## 3. Parameter Typing

Every trainable parameter belongs to a declared module and mathematical role.

Parameters must not be interpreted solely from storage position or tensor shape.

---

## 4. Fixed Parameters

Not every model parameter is trainable.

Let:

`Phi`

denote fixed parameters.

These may include:

- physical constants;
- architecture constants;
- externally sourced constants;
- calibrated constants frozen during a training stage;
- numerical constants;
- fixed thresholds.

---

## 5. Trainable versus Fixed

The distinction remains:

`Theta ≠ Phi`.

---

## 6. Optimizer State

Let:

`Omega[n]`

denote optimizer state at optimization step:

`n`.

Optimizer state may contain:

- momentum;
- moving averages;
- adaptive second moments;
- step counters;
- learning-rate state;
- parameter-group state.

---

## 7. Optimization Step

The optimization index is:

`n`.

A generic update is:

`(Theta[n+1], Omega[n+1]) = U_OPT(Theta[n], Omega[n], G[n], H[n])`.

Here:

- `G[n]` is gradient information;
- `H[n]` is auxiliary optimization state.

---

## 8. Optimization Step Is Not Physical Time

The framework preserves:

`optimization step ≠ physical timestep`.

---

## 9. Optimization Step Is Not Ternary Tact

The framework preserves:

`optimization step ≠ ternary execution tact`.

---

## 10. Optimization Step Is Not Resonance Transition

The framework preserves:

`optimization step ≠ resonance transition`.

---

## 11. Optimization Step Is Not Bifurcation

The framework preserves:

`optimization step ≠ bifurcation`.

---

## 12. Objective Function

Let:

`L_total(Theta)`

denote the complete optimization objective.

A general decomposition is:

`L_total = L_data + R_total + C_total`.

Here:

- `L_data` contains data-fitting objectives;
- `R_total` contains regularization;
- `C_total` contains soft constraint penalties where used.

---

## 13. Typed Data Objective

The data objective may contain:

`L_data = lambda_E L_E + lambda_F L_F + lambda_S L_S + lambda_R L_R + lambda_T L_T + lambda_U L_U`.

---

## 14. Energy Loss

`L_E`

measures energy-prediction error under the declared units and reduction.

---

## 15. Force Loss

`L_F`

measures force-prediction error.

---

## 16. Stress Loss

`L_S`

measures stress-prediction error.

---

## 17. Resonance Loss

`L_R`

measures supervised or self-consistency error associated with the declared resonance representation.

---

## 18. Ternary Loss

`L_T`

measures error in ternary target prediction or its differentiable training representation.

---

## 19. Uncertainty Loss

`L_U`

may contain:

- likelihood terms;
- calibration surrogates;
- domain-classification terms;
- uncertainty-model objectives.

---

## 20. Regularization Objective

A general regularization decomposition may be:

`R_total = R_param + R_T + R_R + R_EQ + R_U + R_aux`.

---

## 21. Parameter Regularization

`R_param`

acts on trainable parameters or their declared groups.

---

## 22. Ternary Regularization

`R_T`

acts on differentiable ternary-related prediction variables while preserving exact semantic states:

`-1/0/1`.

---

## 23. Resonance Regularization

`R_R`

acts on resonance coordinates, windows, persistence, hysteresis, multiscale relations, or resonance-to-ternary consistency.

---

## 24. Equivariance Regularization

`R_EQ`

contains optional numerical symmetry penalties where equivariance is not already exact by construction or where residual monitoring is included in training.

---

## 25. Uncertainty Regularization

`R_U`

constrains uncertainty parameterization, covariance conditioning, calibration-related variables, or domain-detector behavior.

---

## 26. Auxiliary Regularization

`R_aux`

contains additional explicitly declared optimization terms.

---

## 27. Hard Constraint

A hard constraint defines the admissible model or state space.

It is not merely a weighted loss term.

---

## 28. Soft Constraint

A soft constraint contributes a finite penalty to:

`L_total`.

---

## 29. Hard versus Soft

The framework preserves:

`hard constraint ≠ soft penalty`.

---

## 30. Architectural Constraint

An architectural constraint is satisfied by model construction for every admissible parameter value.

---

## 31. Projection Constraint

A projection constraint maps a proposed state or parameter update back into an admissible set.

---

## 32. Penalty Constraint

A penalty constraint discourages violation without guaranteeing exact satisfaction.

---

## 33. Constraint Priority

Semantic and structural invariants defined as exact must not depend solely on a finite penalty coefficient.

---

## 34. Balanced Ternary Constraint

The exact semantic ternary state space remains:

`T = {-1,0,1}`.

---

## 35. Active Neutral Constraint

The state:

`0`

remains active neutral.

Optimization must not redefine it as:

- missing;
- unknown;
- invalid;
- mask;
- padding;
- uncertainty;
- abstention;
- out-of-domain state.

---

## 36. Direct-Opposite Constraint

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 37. Canonical Opposite Routes

Opposite-polarity committed execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 38. Optimization Cannot Override Execution Topology

No reduction in training loss authorizes violation of the ternary execution graph.

---

## 39. Target versus Executed State

The framework preserves:

`t_target ≠ t_exec`.

---

## 40. Pending versus Executed State

The framework preserves:

`t_pending ≠ t_exec`.

---

## 41. Pending versus Neutral

The framework preserves:

`t_pending ≠ 0`.

A pending destination is routing state, not active neutral by identity.

---

## 42. Differentiable Ternary Representation

Training may use:

- logits;
- probabilities;
- continuous latent variables;
- smooth thresholds;
- surrogate gradients.

These remain optimization representations.

---

## 43. Semantic Ternary State

The semantic output remains exactly:

`-1`

`0`

or:

`1`.

---

## 44. Soft versus Semantic State

The framework preserves:

`soft ternary representation ≠ committed ternary state`.

---

## 45. Gradient

The parameter gradient is:

`G[n] = grad_Theta L_total(Theta[n])`.

---

## 46. Parameter Gradient Is Not Force

The framework preserves:

`grad_Theta L_total ≠ mechanical force`.

---

## 47. Mechanical Force

For an energy-derived conservative branch:

`F_i = -grad_(r_i) E`.

---

## 48. Distinct Differentiation Spaces

The gradients:

`grad_Theta L`

and:

`grad_R E`

act in different spaces and have different semantics.

---

## 49. Stress Derivative

Stress may depend on derivatives with respect to strain or cell deformation under the declared convention.

---

## 50. Second-Order Differentiation

Force training through an energy-derived force may require derivatives of:

`grad_R E`

with respect to:

`Theta`.

---

## 51. Higher-Order Autodifferentiation

The computational graph must retain the derivative order required by the selected objective.

---

## 52. Gradient Accumulation

For minibatches:

`B_1, ..., B_K`

gradients may be accumulated before an optimizer update.

---

## 53. Accumulation Step versus Optimization Step

A microbatch evaluation does not necessarily correspond to a parameter update.

---

## 54. Batch Objective

For batch:

`B`

the objective may be:

`L_B = A_B({L_k})`.

---

## 55. Mean Reduction

A mean reduction divides by a declared count.

---

## 56. Sum Reduction

A sum reduction preserves additive scaling with the number of terms.

---

## 57. Reduction Semantics

Every objective must declare its reduction.

---

## 58. Masked Reduction

For validity mask:

`m_k`

a masked mean may be:

`L = sum_k m_k l_k / max(sum_k m_k, epsilon)`.

---

## 59. Mask Is Not Neutral

The framework preserves:

`mask ≠ ternary 0`.

---

## 60. Task Availability

Not every training sample must contain every reference quantity.

---

## 61. Partial Labels

A sample may contain energy and force labels without stress, or another declared subset.

---

## 62. Missing-Label Handling

Missing labels are handled through metadata and masks.

They are not encoded as zero-valued semantic targets unless zero is the actual reference value.

---

## 63. Unit Consistency

Loss terms with different physical units require explicit scaling or normalization before combination.

---

## 64. Energy Units

Energy residuals retain declared energy units before normalization.

---

## 65. Force Units

Force residuals retain force units before normalization.

---

## 66. Stress Units

Stress residuals retain stress units before normalization.

---

## 67. Dimensionless Composite Objective

A composite objective should use explicitly normalized or weighted terms so their combination is mathematically defined.

---

## 68. Loss Weight

For objective component:

`L_j`

let:

`lambda_j ≥ 0`.

---

## 69. Fixed Loss Weight

A fixed coefficient remains constant during a declared training stage.

---

## 70. Scheduled Loss Weight

A scheduled coefficient may vary:

`lambda_j = lambda_j[n]`.

---

## 71. Learned Loss Weight

A coefficient may itself be optimized when the objective defines a valid trainable parameterization.

---

## 72. Weight Provenance

Every nontrivial fixed or scheduled coefficient retains provenance.

---

## 73. Multiobjective Optimization

The TR-EIP training problem within TR-EIF is generally multiobjective.

The objectives may include:

- energy accuracy;
- force accuracy;
- stress accuracy;
- resonance consistency;
- ternary accuracy;
- equivariance;
- uncertainty calibration;
- domain discrimination.

---

## 74. Weighted Scalarization

One strategy forms a weighted scalar objective.

---

## 75. Gradient-Based Multiobjective Method

Another strategy operates directly on task gradients.

---

## 76. Pareto Structure

Conflicting objectives may generate a Pareto tradeoff.

---

## 77. Pareto Optimality Is Not Physical Optimality

The framework preserves:

`optimization Pareto optimum ≠ physical equilibrium`.

---

## 78. Gradient Conflict

For task gradients:

`g_a`

and:

`g_b`

a negative inner product may indicate local gradient conflict under the selected parameter metric.

---

## 79. Gradient Alignment

A positive inner product indicates local alignment under the same metric.

---

## 80. Gradient Conflict Is Not Physical Opposition

The framework preserves:

`gradient conflict ≠ opposing physical force`.

---

## 81. Loss Scale

Different task losses may differ by orders of magnitude.

---

## 82. Gradient Scale

Similar loss magnitudes do not guarantee similar gradient magnitudes.

---

## 83. Gradient-Norm Monitoring

A training trace may record gradient norms by parameter group or task.

---

## 84. Gradient Clipping

A clipping operator may constrain optimizer gradients.

---

## 85. Global-Norm Clipping

One strategy clips the total parameter-gradient norm.

---

## 86. Per-Group Clipping

Another strategy clips parameter groups separately.

---

## 87. Gradient Clipping Is Not State Clipping

The framework preserves:

`gradient clipping ≠ resonance clipping`

and:

`gradient clipping ≠ force clipping`.

---

## 88. Gradient Clipping Is Not Hard Semantic Enforcement

Gradient clipping cannot enforce exact ternary transition semantics.

---

## 89. Learning Rate

Let:

`eta[n]`

denote learning rate.

---

## 90. Constant Learning Rate

A training stage may use:

`eta[n] = eta_0`.

---

## 91. Scheduled Learning Rate

A schedule may vary:

`eta[n]`

with optimization step.

---

## 92. Warmup

A warmup schedule increases learning rate over an initial interval.

---

## 93. Decay

A decay schedule reduces learning rate according to a declared rule.

---

## 94. Piecewise Schedule

Different training intervals may use different learning-rate rules.

---

## 95. Learning-Rate Schedule Is Not Physical Dynamics

The framework preserves:

`learning-rate evolution ≠ physical temporal evolution`.

---

## 96. Gradient Descent

A basic update is:

`Theta[n+1] = Theta[n] - eta[n] G[n]`.

---

## 97. Momentum

Momentum introduces retained optimizer state.

---

## 98. Momentum State

Let:

`v[n]`

denote momentum.

A generic form is:

`v[n+1] = beta v[n] + G[n]`.

---

## 99. Momentum Update

A corresponding parameter update may use:

`Theta[n+1] = Theta[n] - eta[n] v[n+1]`.

---

## 100. Optimizer Memory Is Not Physical Memory

The framework preserves:

`optimizer momentum ≠ resonance memory`

and:

`optimizer momentum ≠ retained frequency memory`.

---

## 101. Adaptive Optimization

Adaptive methods use parameter-dependent or coordinate-dependent update scaling derived from gradient history.

---

## 102. First-Moment Estimate

A method may maintain:

`m[n]`.

---

## 103. Second-Moment Estimate

A method may maintain:

`v[n]`.

---

## 104. Bias Correction

Early-step moment estimates may require declared bias correction.

---

## 105. Adaptive Denominator

A small numerical constant may stabilize division by the second-moment estimate.

---

## 106. Optimizer Epsilon

Optimizer stabilization constant:

`epsilon_OPT`

is a numerical parameter.

---

## 107. Optimizer Epsilon Is Not Physical Tolerance

The framework preserves:

`epsilon_OPT ≠ physical error tolerance`.

---

## 108. Weight Decay

Weight decay modifies parameter updates according to a declared rule.

---

## 109. Weight Decay versus L2 Penalty

Decoupled weight decay and an L2 loss penalty are not universally identical under adaptive optimization.

---

## 110. Parameter Groups

Different parameter groups may use different:

- learning rates;
- weight decay;
- clipping;
- schedules.

---

## 111. Equivariant Parameter Group

`Theta_EQ`

may use a dedicated optimization configuration.

---

## 112. Resonance Parameter Group

`Theta_R`

may use a different configuration.

---

## 113. Ternary Parameter Group

`Theta_T`

may use another configuration.

---

## 114. Mechanical Parameter Group

Energy, force, and stress parameters may be grouped according to architecture.

---

## 115. Uncertainty Parameter Group

Uncertainty and domain parameters may use dedicated optimization settings.

---

## 116. Frozen Parameter Group

A parameter group may be frozen during a training stage.

---

## 117. Unfreezing

A later stage may activate previously frozen parameters.

---

## 118. Freeze State

Trainability state must be explicitly recorded.

---

## 119. Freezing Is Not Parameter Deletion

A frozen parameter remains part of the model.

---

## 120. Stagewise Optimization

Training may be divided into declared stages.

---

## 121. Representation Stage

A stage may optimize equivariant representation parameters.

---

## 122. Mechanical Stage

A stage may optimize energy-force-stress objectives.

---

## 123. Resonance Stage

A stage may introduce or strengthen resonance objectives.

---

## 124. Ternary Stage

A stage may introduce ternary-target objectives and regularization.

---

## 125. Uncertainty Stage

A stage may fit or calibrate uncertainty and domain components.

---

## 126. Joint Stage

A final stage may optimize several or all trainable modules jointly.

---

## 127. Training Stage Is Not Ternary State

The framework preserves:

`training stage ≠ ternary state`.

---

## 128. Training Stage Is Not Physical Phase

The framework preserves:

`training stage ≠ physical phase of matter`.

---

## 129. Pretraining

A model may initialize selected parameters using an auxiliary objective.

---

## 130. Fine-Tuning

A model may subsequently optimize on a target dataset or task set.

---

## 131. Pretraining Domain

The pretraining domain must be documented separately from the fine-tuning domain.

---

## 132. Transfer Learning

Transferred parameters retain provenance from the source model or training procedure.

---

## 133. Initialization

The initial trainable state is:

`Theta[0]`.

---

## 134. Random Initialization

A stochastic initializer requires a controlled random seed for deterministic replay.

---

## 135. Deterministic Initialization

A fixed initialization may be specified directly.

---

## 136. Initialization Scale

Parameter initialization must be compatible with:

- layer dimensions;
- representation types;
- nonlinearities;
- numerical precision.

---

## 137. Symmetry-Preserving Initialization

Initialization must not introduce symmetry-breaking parameters where the architecture requires exact equivariance.

---

## 138. Random Seed

A seed controls a declared random-number stream.

---

## 139. Seed Is Not Complete Reproducibility

The framework preserves:

`fixed seed ≠ guaranteed deterministic execution`.

---

## 140. Reproducibility State

Deterministic training may additionally require control of:

- data order;
- parallel reductions;
- hardware kernels;
- arithmetic precision;
- stochastic layers;
- library versions.

---

## 141. Minibatch Sampling

A minibatch sampler selects training examples.

---

## 142. Uniform Sampling

Uniform sampling assigns equal sampling probability under the declared sample unit.

---

## 143. Weighted Sampling

Weighted sampling may compensate for:

- rare species;
- rare structures;
- resonance regimes;
- ternary classes;
- domain boundaries;
- high-value reference data.

---

## 144. Sampling Weight Is Not Loss Weight

The framework preserves:

`sampling probability ≠ objective coefficient`.

---

## 145. Class-Balanced Sampling

Ternary classes may be sampled according to a declared balancing strategy.

---

## 146. Neutral-Class Sampling

The active-neutral class must be treated as a semantic class, not as discarded background.

---

## 147. Resonance-Balanced Sampling

Resonance classes may be sampled separately from ternary classes.

---

## 148. Domain-Boundary Sampling

Samples near a model-domain boundary may receive targeted sampling.

---

## 149. Resonance-Boundary Sampling

Samples near:

`∂W_R`

may be targeted independently.

---

## 150. Boundary Separation

The framework preserves:

`domain boundary ≠ resonance boundary ≠ ternary decision boundary`.

---

## 151. Curriculum Sampling

Sampling distribution may change across training stages.

---

## 152. Hard-Example Mining

Examples with large declared residuals may receive increased sampling probability.

---

## 153. High Loss Is Not Necessarily OOD

The framework preserves:

`high training loss ≠ OUT_OF_DOMAIN`.

---

## 154. High Uncertainty Is Not Necessarily High Loss

The framework preserves:

`high uncertainty ≠ high current residual`.

---

## 155. Data Shuffle

Training order may be randomized.

---

## 156. Deterministic Shuffle

A deterministic shuffle requires controlled seed and algorithm.

---

## 157. Epoch

An epoch is a dataset-iteration convention.

---

## 158. Epoch Is Not Physical Cycle

The framework preserves:

`training epoch ≠ physical cycle`.

---

## 159. Epoch Is Not Scheduler Cycle

The framework preserves:

`training epoch ≠ ternary scheduler cycle`.

---

## 160. Convergence

Optimization convergence must be defined through explicit numerical criteria.

---

## 161. Loss Convergence

One criterion monitors change in objective value.

---

## 162. Gradient Convergence

Another monitors gradient norm.

---

## 163. Parameter Convergence

Another monitors parameter displacement.

---

## 164. Validation Convergence

A practical stopping rule may monitor held-out metrics.

---

## 165. Constraint Convergence

A model may require constraint residuals below declared tolerances.

---

## 166. Convergence Is Not Global Optimality

The framework preserves:

`numerical convergence ≠ global optimum`.

---

## 167. Convergence Is Not Physical Equilibrium

The framework preserves:

`optimization convergence ≠ physical equilibrium`.

---

## 168. Stationary Point

A small parameter gradient indicates a stationary or approximately stationary optimization state under the selected objective.

---

## 169. Stationary Point Is Not Bifurcation

The framework preserves:

`optimization stationary point ≠ physical bifurcation`.

---

## 170. Early Stopping

Training may stop when a monitored validation metric fails to improve under a declared criterion.

---

## 171. Patience

An early-stopping rule may use a finite patience interval.

---

## 172. Best Checkpoint

The selected checkpoint must be defined by an explicit metric and tie-breaking rule.

---

## 173. Final Checkpoint versus Best Checkpoint

The framework preserves:

`last optimization state ≠ best validation state`.

---

## 174. Checkpoint

A checkpoint contains sufficient state to reproduce or resume the declared optimization process.

---

## 175. Model State

A checkpoint may contain:

`Theta[n]`.

---

## 176. Optimizer State

A resumable checkpoint may also contain:

`Omega[n]`.

---

## 177. Scheduler State

Learning-rate scheduler state may be required.

---

## 178. Random State

Random-number generator states may be required for exact continuation.

---

## 179. Sampler State

Data sampler state may be required for exact continuation.

---

## 180. Configuration State

Training configuration and objective coefficients must accompany the checkpoint.

---

## 181. Dataset Identity

Checkpoint metadata must identify the training-data version.

---

## 182. Code Identity

Checkpoint metadata should identify the executable code revision.

---

## 183. Resume

Resuming optimization restores the required state and continues from a defined optimization step.

---

## 184. Warm Restart

A warm restart may restore model parameters while resetting some optimizer state.

---

## 185. Resume versus Fine-Tune

The framework preserves:

`resume ≠ fine-tune`.

---

## 186. Checkpoint Provenance

Checkpoint origin must remain traceable.

---

## 187. Validation Split

Optimization must not update parameters from the final test split.

---

## 188. Validation Feedback

Validation metrics may influence:

- early stopping;
- hyperparameter selection;
- checkpoint selection.

---

## 189. Test Isolation

Final test data must remain isolated from parameter and hyperparameter optimization under a strict benchmark protocol.

---

## 190. Hyperparameter

Let:

`Psi`

denote optimization hyperparameters.

---

## 191. Hyperparameter Examples

`Psi`

may include:

- learning rate;
- batch size;
- optimizer coefficients;
- loss weights;
- regularization strengths;
- clipping thresholds;
- schedule parameters;
- domain thresholds where calibrated jointly.

---

## 192. Hyperparameter versus Trainable Parameter

The framework preserves:

`Psi ≠ Theta`.

---

## 193. Hyperparameter Search

A search procedure evaluates candidate:

`Psi`.

---

## 194. Grid Search

A finite Cartesian set of candidate values may be evaluated.

---

## 195. Random Search

Candidate hyperparameters may be sampled from declared distributions.

---

## 196. Sequential Search

A search method may select new candidates using previous evaluations.

---

## 197. Hyperparameter Objective

The selection metric must be explicit.

---

## 198. Multiobjective Hyperparameter Selection

Hyperparameters may be selected using several validation metrics.

---

## 199. Hyperparameter Leakage

Repeated tuning against the final test set invalidates strict test isolation.

---

## 200. Nested Validation

A nested protocol may separate model selection from final performance estimation.

---

## 201. Optimization Stability

Training stability concerns the behavior of the numerical optimization process.

---

## 202. Optimization Stability Is Not Dynamical Stability

The framework preserves:

`optimization stability ≠ physical dynamical stability`.

---

## 203. Divergence

Optimization divergence may include:

- non-finite loss;
- exploding parameter norms;
- exploding gradients;
- unstable optimizer state.

---

## 204. Divergence Is Not Physical Instability

The framework preserves:

`optimizer divergence ≠ physical instability`.

---

## 205. Non-Finite Loss

A non-finite objective is an invalid numerical optimization state.

---

## 206. Non-Finite Gradient

A non-finite parameter gradient is an invalid optimization state.

---

## 207. Numerical Failure Gate

An optimizer update must not silently apply non-finite gradients.

---

## 208. Gradient Validation

Before update, implementations may check:

- finite values;
- gradient norm;
- parameter-group validity.

---

## 209. Parameter Validation

After update, implementations may check:

- finite parameters;
- hard parameter constraints;
- declared bounds.

---

## 210. Rollback

A training system may restore the previous valid checkpoint after an invalid update.

---

## 211. Rollback Is Not Ternary Transition

The framework preserves:

`optimizer rollback ≠ ternary-state transition`.

---

## 212. Loss Scaling

Mixed-precision training may scale the loss before backpropagation.

---

## 213. Scaled Gradient

The gradient must be unscaled according to the declared mixed-precision procedure before operations that require the true gradient scale.

---

## 214. Dynamic Loss Scaling

A dynamic scaler may adjust scale according to overflow behavior.

---

## 215. Loss Scale Is Not Loss Weight

The framework preserves:

`mixed-precision loss scale ≠ objective coefficient`.

---

## 216. Precision

Optimization arithmetic may use:

- full precision;
- mixed precision;
- reduced precision.

---

## 217. Master Parameters

A mixed-precision implementation may retain higher-precision master parameters.

---

## 218. Precision Contract

The training configuration must record arithmetic precision by relevant operation or parameter group.

---

## 219. Quantized Training

Quantization-aware training may simulate reduced-precision inference behavior.

---

## 220. Quantization Constraint

Quantization must preserve declared semantic and symmetry contracts within the specified numerical implementation.

---

## 221. Symmetry under Optimization

Parameter updates must remain inside the symmetry-compatible model family when architectural equivariance is required.

---

## 222. Equivariant Architecture

For structurally equivariant modules, arbitrary permitted parameter updates preserve the transformation law.

---

## 223. Symmetry-Breaking Parameter Update

A parameterization that allows arbitrary laboratory-frame directional parameters may leave the declared equivariant model family.

Such parameters must be structurally constrained or excluded when full equivariance is required.

---

## 224. Equivariance Residual

An approximately equivariant model may include:

`L_EQ`.

---

## 225. Symmetry Validation

Even structurally equivariant architectures require numerical validation of implementation residuals.

---

## 226. Rotation Constraint

Scalar energy remains invariant under admissible rigid rotation.

---

## 227. Force Constraint

Force remains polar-vector equivariant.

---

## 228. Stress Constraint

Stress remains tensorially equivariant.

---

## 229. Ternary Symmetry Constraint

Scalar ternary semantic states remain invariant under rigid spatial transformation and permute with their associated entities.

---

## 230. Spatial Rotation Is Not Ternary Polarity Reversal

The framework preserves:

`spatial rotation ≠ -1/1 polarity reversal`.

---

## 231. Resonance Optimization

Trainable resonance parameters may be optimized through:

- supervised resonance targets;
- mechanical objectives;
- ternary objectives;
- multiscale consistency;
- regularization.

---

## 232. Resonance Window Parameters

If resonance-window geometry is trainable, its admissibility constraints must remain enforced during optimization.

---

## 233. Positive Width

A trainable finite interval must preserve positive declared width.

---

## 234. Window Collapse Control

If collapse is forbidden by the model, optimization must structurally or explicitly prevent it.

---

## 235. Resonance Classification Is Not Energy

The framework preserves:

`resonance classification ≠ energy`.

---

## 236. Resonance Loss Is Not Physical Energy

The framework preserves:

`resonance loss ≠ physical energy`.

---

## 237. Ternary Optimization

Ternary training may optimize logits or continuous decision variables.

---

## 238. Class Weighting

The three classes:

`-1`

`0`

`1`

may use explicit class weights.

---

## 239. Neutral-Class Weight

The weight for:

`0`

does not indicate that neutral is less or more semantically active than the other states.

It is an optimization coefficient.

---

## 240. Direct-Transition Penalty

A soft penalty may detect predicted direct-opposite transition tendencies.

---

## 241. Hard Direct-Transition Invariant

The actual committed execution layer must still enforce the prohibition structurally.

---

## 242. Transition-Aware Objective

A sequential ternary objective may evaluate:

- current executed state;
- target;
- pending destination;
- proposed next state.

---

## 243. First-Leg Objective

An opposite request from:

`-1`

toward:

`1`

must first train or validate the transition:

`-1 → 0`.

---

## 244. Second-Leg Objective

The later:

`0 → 1`

leg is a distinct event.

---

## 245. No Automatic Second Leg

Optimization must not encode the first leg as automatic authorization of the second.

---

## 246. Neutral Residence Objective

Where temporal training data define neutral residence, the model may optimize its duration or persistence behavior.

---

## 247. Chattering Control

Sequential objectives may penalize excessive switching.

---

## 248. Chattering Penalty Is Not Hysteresis

The framework preserves:

`switch penalty ≠ hysteresis`.

---

## 249. Hysteresis Optimization

Trainable hysteresis parameters must preserve declared entry/exit ordering.

---

## 250. Resonance-to-Ternary Optimization

The mapping:

`P_RT`

may be optimized while maintaining explicit separation between resonance classification and ternary classification.

---

## 251. Resonance Class Is Not Ternary Class

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

---

## 252. Uncertainty-Aware Optimization

Uncertainty may influence:

- loss weighting;
- sampling;
- active learning;
- rejection-model training.

---

## 253. Uncertainty Weighting

For sample:

`k`

a weight may depend on:

`u_k`.

---

## 254. Weighting Direction

High uncertainty may receive lower weight when modeling noisy labels or higher weight when emphasizing difficult regions.

The rule must be explicit.

---

## 255. Uncertainty Weight Is Not Confidence Truth

An uncertainty-derived weight is an optimization choice.

---

## 256. Domain-Aware Optimization

Domain information may influence training through:

- in-domain weighting;
- OOD exposure;
- boundary sampling;
- representation separation.

---

## 257. OOD Samples

Known OOD samples may train a detector without being used as ordinary physical target samples.

---

## 258. OOD Is Not Neutral

The framework preserves:

`OUT_OF_DOMAIN ≠ 0`.

---

## 259. Abstention Is Not Neutral

The framework preserves:

`ABSTAIN ≠ 0`.

---

## 260. Invalid Is Not Neutral

The framework preserves:

`INVALID ≠ 0`.

---

## 261. Missing Is Not Neutral

The framework preserves:

`MISSING ≠ 0`.

---

## 262. Domain Threshold Optimization

A detector threshold may be calibrated on a dedicated validation or calibration set.

---

## 263. Domain Threshold Is Not Model Parameter by Necessity

A threshold may be:

- fixed;
- calibrated;
- learned.

Its status must be explicit.

---

## 264. Calibration Stage

Uncertainty calibration may occur after predictive-model training.

---

## 265. Calibration Parameter

Calibration may introduce parameters:

`Theta_CAL`.

---

## 266. Calibration Data Isolation

Calibration data must remain distinct from the final test set.

---

## 267. Joint Calibration

A model may alternatively train calibration-related parameters jointly if the objective explicitly defines this procedure.

---

## 268. Calibration Is Not Accuracy Optimization

The framework preserves:

`calibration objective ≠ prediction-error objective`.

---

## 269. Active Learning

Optimization may participate in an active-learning loop.

---

## 270. Candidate Evaluation

A candidate pool is evaluated for:

- uncertainty;
- domain state;
- representation diversity;
- resonance coverage;
- ternary-transition coverage.

---

## 271. Acquisition

An acquisition function selects new reference candidates.

---

## 272. Reference Evaluation

Selected candidates receive reference labels through the declared reference process.

---

## 273. Dataset Update

New reference samples are added with provenance and split-control rules.

---

## 274. Retraining

The model is retrained or fine-tuned according to a declared protocol.

---

## 275. Active-Learning Cycle Is Not Physical Cycle

The framework preserves:

`active-learning iteration ≠ physical temporal cycle`.

---

## 276. Optimization and Multiscale State

A multiscale model may optimize losses at:

- edge;
- atom;
- cluster;
- global levels.

---

## 277. Scale-Specific Loss

Let:

`L^(ell)`

denote the loss at scale:

`ell`.

---

## 278. Multiscale Objective

A composite form is:

`L_MS = sum_ell lambda_ell L^(ell)`.

---

## 279. Cross-Scale Consistency

Additional terms may compare mapped fine-scale and coarse-scale predictions.

---

## 280. Cross-Scale Equality Is Not Required Universally

Different scales need not have identical states.

They must satisfy only the declared mappings.

---

## 281. Local versus Global Optimization

Local losses may improve local predictions without guaranteeing global consistency.

Global losses may constrain aggregate behavior without uniquely determining local state.

---

## 282. Scale Weighting

Scale weights must be explicit.

---

## 283. Distributed Optimization

Training may execute across multiple compute devices or processes.

---

## 284. Data Parallelism

Different workers may process different minibatch partitions and aggregate gradients.

---

## 285. Model Parallelism

Different model components may execute on different devices.

---

## 286. Gradient Reduction

Distributed gradients require a declared reduction operation.

---

## 287. Reduction Order

Floating-point reduction order may affect exact numerical replay.

---

## 288. Distributed Determinism

Deterministic distributed optimization requires control of communication and reduction behavior where implementation permits.

---

## 289. Synchronization Barrier

A compute synchronization barrier is an implementation mechanism.

---

## 290. Compute Synchronization Is Not Physical Synchronization

The framework preserves:

`distributed-compute synchronization ≠ oscillator synchronization`.

---

## 291. Checkpoint Sharding

Large model or optimizer state may be stored across multiple checkpoint shards.

---

## 292. Shard Integrity

A resumable checkpoint requires all declared shards and metadata.

---

## 293. Optimization Trace

A training trace should record sufficient information to reconstruct optimization behavior.

---

## 294. Step Record

A step record may contain:

- optimization step;
- epoch;
- learning rate;
- total loss;
- component losses;
- regularization terms;
- gradient norm;
- parameter norm;
- uncertainty metrics;
- symmetry residuals;
- domain metrics.

---

## 295. Ternary Training Metrics

A trace may include:

- class accuracy;
- neutral precision;
- neutral recall;
- direct-opposite proposal count;
- route-consistency metrics;
- switching metrics.

---

## 296. Resonance Training Metrics

A trace may include:

- coordinate error;
- window-class error;
- boundary residual;
- persistence residual;
- hysteresis residual;
- cross-scale residual.

---

## 297. Mechanical Training Metrics

A trace may include:

- energy MAE;
- energy RMSE;
- force MAE;
- force RMSE;
- stress MAE;
- stress RMSE;
- energy-force consistency residual.

---

## 298. Equivariance Metrics

A trace may include:

- scalar invariance residual;
- force equivariance residual;
- stress equivariance residual;
- resonance equivariance residual.

---

## 299. Uncertainty Metrics

A trace may include:

- negative log-likelihood;
- calibration error;
- coverage;
- sharpness;
- OOD metrics.

---

## 300. Training Metric Is Not Validation Metric

Metrics computed on optimization batches must remain distinguishable from held-out validation metrics.

---

## 301. Training Metric Is Not Benchmark Result

A training trace is not automatically a benchmark.

---

## 302. Benchmark Promotion

A result becomes benchmark evidence only under the declared benchmark protocol.

---

## 303. Optimization Provenance

Optimization artifacts use the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 304. Primary-Source Optimizer

An established optimization method adopted from the literature carries:

`PRIMARY_SOURCE`

for its sourced definition.

---

## 305. Derived Optimization Relation

A relation derived from previously defined TR-EIF objectives or invariants carries:

`DERIVED`.

---

## 306. Author-Defined Optimization Policy

A TR-EIF-specific combination of objectives, stages, routing constraints, or parameter groups carries:

`AUTHOR_DEFINED`.

---

## 307. Calibrated Hyperparameter

A value selected through a declared calibration procedure carries:

`CALIBRATED`.

---

## 308. Benchmark Optimization Result

Measured convergence, runtime, memory, or final predictive metrics under a benchmark protocol carry:

`BENCHMARK`.

---

## 309. Optimization Test Fixture

Synthetic gradients, objective values, or deterministic update cases used for testing carry:

`TEST_FIXTURE`.

---

## 310. Optimizer Extension Rule

Any optimizer configuration must define:

1. update algorithm;

2. learning rate;

3. optimizer coefficients;

4. numerical epsilon;

5. weight decay;

6. parameter groups;

7. precision;

8. gradient clipping;

9. schedule;

10. provenance.

---

## 311. Objective Extension Rule

Any new objective term must define:

1. target quantity;

2. prediction quantity;

3. units;

4. metric;

5. reduction;

6. mask behavior;

7. coefficient;

8. differentiability;

9. provenance;

10. validation.

---

## 312. Hard-Constraint Extension Rule

Any hard optimization constraint must define:

1. constrained object;

2. admissible set;

3. enforcement mechanism;

4. update ordering;

5. failure behavior;

6. validation.

---

## 313. Parameter-Group Extension Rule

Any parameter group must define:

1. included parameters;

2. trainability state;

3. learning rate;

4. regularization;

5. clipping;

6. schedule.

---

## 314. Training-Stage Extension Rule

Any training stage must define:

1. active parameters;

2. frozen parameters;

3. active objectives;

4. sampling policy;

5. optimizer configuration;

6. entry condition;

7. exit condition;

8. checkpoint policy.

---

## 315. Checkpoint Extension Rule

Any resumable checkpoint must define:

1. model state;

2. optimizer state;

3. scheduler state;

4. optimization step;

5. random state where required;

6. sampler state where required;

7. dataset identity;

8. code identity;

9. configuration identity.

---

## 316. Hyperparameter-Search Extension Rule

Any hyperparameter search must define:

1. search space;

2. search method;

3. validation metric;

4. budget;

5. stopping rule;

6. final-selection rule;

7. test isolation.

---

## 317. Mixed-Precision Extension Rule

Any mixed-precision training mode must define:

1. parameter precision;

2. activation precision;

3. accumulation precision;

4. loss scaling;

5. overflow handling;

6. validation tolerance.

---

## 318. Distributed-Optimization Extension Rule

Any distributed optimization configuration must define:

1. parallelism type;

2. worker count;

3. data partitioning;

4. gradient reduction;

5. synchronization;

6. checkpoint strategy;

7. determinism contract.

---

## 319. Ternary-Optimization Extension Rule

Any ternary optimization procedure must define:

1. soft training representation;

2. hard decision rule;

3. active-neutral semantics;

4. target field;

5. executed-state field;

6. pending-state field;

7. transition constraints;

8. sequential loss where applicable;

9. exact validation.

---

## 320. Resonance-Optimization Extension Rule

Any resonance optimization procedure must define:

1. resonance state;

2. resonance target where supervised;

3. window structure;

4. regularization;

5. persistence;

6. hysteresis;

7. scale;

8. resonance-to-ternary interface.

---

## 321. Equivariance-Optimization Extension Rule

Any symmetry-related optimization term must define:

1. symmetry group;

2. transformed input;

3. expected transformed output;

4. residual;

5. reduction;

6. coefficient;

7. numerical tolerance.

---

## 322. Uncertainty-Optimization Extension Rule

Any uncertainty optimization procedure must define:

1. uncertainty type;

2. predictive distribution or score;

3. objective;

4. calibration;

5. domain relation;

6. acceptance relation;

7. validation.

---

## 323. Canonical Optimization Invariants

Every conforming TR-EIP optimization procedure within TR-EIF preserves:

1. explicit trainable parameter set;

2. explicit fixed parameter set;

3. explicit objective decomposition;

4. explicit units and reductions;

5. explicit optimizer state;

6. explicit parameter-update rule;

7. explicit hard constraints;

8. explicit training/validation separation;

9. explicit checkpoint identity;

10. explicit provenance.

---

## 324. Canonical Gradient Invariants

The framework preserves:

`parameter gradient ≠ mechanical force`

`optimizer momentum ≠ physical momentum`

`optimizer memory ≠ resonance memory`

`optimizer memory ≠ retained frequency memory`.

---

## 325. Canonical Time Invariants

The framework preserves:

`optimization step ≠ physical timestep`

`training epoch ≠ physical cycle`

`training stage ≠ physical phase`

`active-learning cycle ≠ physical cycle`.

---

## 326. Canonical State Invariants

The framework preserves:

`loss ≠ energy`

`resonance loss ≠ resonance state`

`ternary loss ≠ ternary state`

`uncertainty loss ≠ uncertainty state`

`domain loss ≠ domain state`.

---

## 327. Canonical Symmetry Invariants

Optimization must preserve the declared transformation laws:

`energy → invariant`

`force → polar-vector equivariant`

`stress → tensor transformed`

`scalar resonance → invariant`

`scalar ternary → invariant`.

---

## 328. Canonical Ternary Invariants

The semantic state space remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

---

## 329. Canonical Execution Invariants

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 330. Canonical Route Invariants

Opposite-polarity committed routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each leg remains a separate event.

---

## 331. Canonical Resonance Distinctions

The optimization layer preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`R(t) ≠ C(t)`

`resonance classification ≠ ternary state`.

---

## 332. Canonical Transition Distinctions

The optimization layer preserves:

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 333. Canonical Domain Distinctions

The optimization layer preserves:

`OUT_OF_DOMAIN ≠ OUTSIDE resonance window`

`OUT_OF_DOMAIN ≠ ternary 0`

`UNCERTAIN ≠ ternary 0`

`ABSTAIN ≠ ternary 0`

`INVALID ≠ ternary 0`.

---

## 334. Canonical Mechanical Distinctions

The optimization layer preserves:

`ternary state ≠ energy`

`resonance classification ≠ energy`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`.

---

## 335. Canonical Optimization Chain

The complete optimization chain is:

`dataset`

`→ minibatch`

`→ forward model`

`→ typed outputs`

`→ typed losses`

`→ regularization`

`→ constraint evaluation`

`→ total objective`

`→ parameter gradients`

`→ optimizer update`

`→ parameter validation`

`→ checkpoint`

`→ held-out validation`.

---

## 336. Canonical Mechanical Training Chain

For an energy-derived force model:

`R`

`→ equivariant representation`

`→ resonance-conditioned representation`

`→ E`

`→ -grad_R E`

`→ F`

`→ mechanical losses`

`→ grad_Theta L`

`→ optimizer update`.

---

## 337. Canonical Ternary Training Chain

A ternary training path is:

`upstream representation`

`→ resonance state`

`→ ternary logits/probabilities`

`→ t_target`

`→ transition-aware objective`

`→ downstream execution validation`.

---

## 338. Canonical Uncertainty Training Chain

An uncertainty path is:

`prediction`

`→ uncertainty estimate`

`→ uncertainty objective`

`→ calibration`

`→ domain/acceptance validation`.

---

## 339. Canonical Multiscale Training Chain

A multiscale path is:

`local objectives`

`+ cluster objectives`

`+ global objectives`

`+ cross-scale consistency`

`→ composite optimization objective`.

---

## 340. Interface to Chapter 10

Chapter 10 summarizes Volume 04 and consolidates:

- model architecture;
- training-data contracts;
- loss functionals;
- energy-force-stress training;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty and domain detection;
- optimization.

---

## 341. Interface to Molecular Dynamics

The optimized interatomic model supplies the learned mappings required by the molecular-dynamics layer developed in Volume 05.

The interface includes:

- energy where defined;
- force;
- stress where defined;
- resonance state where consumed;
- ternary state where consumed;
- uncertainty and domain metadata.

---

## 342. Optimization Does Not Define Molecular Dynamics

The framework preserves:

`parameter optimization ≠ molecular dynamics`.

Training updates model parameters.

Molecular dynamics updates physical configuration state under declared equations of motion.

---

## 343. Final Formal Structure

The optimization layer may be represented as:

`OPT = (Theta, Phi, Omega, Psi, L, R, C, U_OPT, S, K, V)`.

Here:

- `Theta` is the trainable parameter state;
- `Phi` is the fixed parameter state;
- `Omega` is optimizer state;
- `Psi` is the hyperparameter state;
- `L` is the typed data objective;
- `R` is regularization;
- `C` is the constraint system;
- `U_OPT` is the parameter-update operator;
- `S` is the sampling policy;
- `K` is the checkpoint contract;
- `V` is the validation contract.

The generic update is:

`G[n] = grad_Theta L_total(Theta[n])`

followed by:

`(Theta[n+1], Omega[n+1]) = U_OPT(Theta[n], Omega[n], G[n], Psi[n])`.

This update is admissible only when all hard architectural and semantic constraints remain satisfied.

---

## 344. Final Statement

Optimization provides the parameter-learning procedure connecting TR-EIP training data within TR-EIF to a validated model state.

It integrates:

- typed mechanical objectives;
- ternary objectives;
- resonance objectives;
- uncertainty objectives;
- regularization;
- equivariance constraints;
- domain-aware sampling;
- numerical optimization;
- checkpointing;
- validation.

The optimization layer does not redefine the mathematical meaning of any upstream or downstream state.

The framework preserves:

`optimization step ≠ physical timestep`

`parameter gradient ≠ mechanical force`

`optimizer momentum ≠ physical momentum`

`loss ≠ physical energy`

`training stage ≠ physical phase`

`optimization convergence ≠ physical equilibrium`

`equivariance ≠ conservativity`

`uncertainty ≠ error`

`OUT_OF_DOMAIN ≠ ternary 0`

`resonance classification ≠ ternary state`.

The exact balanced ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Optimization may alter the learned mapping that proposes a ternary target.

It cannot alter the committed execution topology.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each leg remains a separate committed event.

These definitions complete the optimization layer required for the Volume 04 summary developed in Chapter 10.
