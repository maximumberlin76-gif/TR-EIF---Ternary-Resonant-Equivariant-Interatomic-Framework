# Learning Problem

## 1. Purpose

This chapter defines the learning problem for the TR-EIP model family within TR-EIF.

Volume 03 established the parameterized interatomic architecture:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ energy`

`→ forces and stress`.

Volume 04 defines how selected model parameters are inferred from reference data while preserving the architectural invariants established in Volumes 01–03.

The canonical learning chain is:

`reference data`

`+ TR-EIP architecture`

`→ parameterized prediction`

`→ loss evaluation`

`→ optimization`

`→ updated parameter state`

`→ validation`.

---

## 2. Parameterized Model

Let:

`M(P)`

denote a TR-EIP model with parameter state:

`P`.

The model maps input:

`X`

and optional retained state:

`S`

to output:

`Y`.

A stateless model may be written:

`Y = M(X; P)`.

A stateful model may be written:

`(Y, S_next) = M(X, S_current; P)`.

---

## 3. Parameter Partition

The complete parameter set may be partitioned:

`P = P_fixed × P_train × P_cal × P_num`.

Here:

- `P_fixed` contains fixed architecture or analytic parameters;
- `P_train` contains trainable parameters;
- `P_cal` contains calibrated parameters;
- `P_num` contains numerical realization parameters.

Only explicitly declared trainable parameters are modified by optimization.

---

## 4. Trainable Parameter Set

Let:

`Theta = P_train`.

The learning problem seeks:

`Theta_star`

such that the declared objective is minimized or otherwise optimized under the model constraints.

---

## 5. Learning Objective

A generic optimization problem is:

`Theta_star = argmin_Theta L(Theta)`.

The objective:

`L`

may depend on multiple datasets, observables, regularizers, and constraints.

---

## 6. Supervised Learning State

A supervised sample may be represented:

`D_k = (X_k, Y_k^ref)`.

Here:

- `X_k` is model input;
- `Y_k^ref` is reference output.

---

## 7. Reference Outputs

Reference outputs may include:

- total energy;
- atomic forces;
- stress;
- resonance descriptors;
- ternary targets;
- structural observables;
- material-specific observables.

Each output remains separately typed.

---

## 8. Prediction

For sample:

`k`:

`Y_k^pred = M(X_k; P)`.

The prediction may contain:

`Y_k^pred = (E_k, F_k, Sigma_k, X_R,k, X_T,k, U_k)`.

---

## 9. Prediction versus Reference

Predicted and reference quantities must belong to compatible state spaces and unit systems before comparison.

---

## 10. Learning Is Not State Redefinition

Optimization changes parameter values.

It does not redefine:

- atomic configuration;
- graph semantics;
- E(3) symmetry;
- resonance state type;
- balanced ternary semantics;
- energy type;
- force type;
- stress type.

---

## 11. Fixed Architectural Invariants

Learning operates subject to the architectural invariants established in earlier volumes.

The balanced ternary domain remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 12. Architecture versus Parameters

The architecture determines the permissible form of the model.

Parameters select one member of that architecture family.

Changing a parameter value does not necessarily define a new architecture.

Changing transformation rules, state semantics, graph topology rules, or execution semantics does.

---

## 13. Training Domain

Let:

`D_train`

denote the training dataset.

A model is optimized over samples:

`X_k ∈ D_train`.

---

## 14. Validation Domain

Let:

`D_val`

denote the validation dataset.

Validation data are not used to update trainable parameters under the declared split.

---

## 15. Test Domain

Let:

`D_test`

denote the test dataset.

The test split is reserved for the declared final evaluation protocol.

---

## 16. Dataset Partition

A dataset may therefore be partitioned:

`D = D_train ∪ D_val ∪ D_test`.

The partitions should satisfy the declared split rules.

---

## 17. Split Disjointness

When strict disjointness is required:

`D_train ∩ D_val = empty`

`D_train ∩ D_test = empty`

`D_val ∩ D_test = empty`.

---

## 18. Configuration-Level Split

A split may operate at the configuration level.

---

## 19. Trajectory-Level Split

For molecular-dynamics data, entire trajectories or time blocks may be separated to reduce temporal leakage.

---

## 20. Composition-Level Split

A split may hold out selected compositions.

---

## 21. Structure-Level Split

A split may hold out structural families.

---

## 22. Thermodynamic-State Split

A split may hold out temperature, pressure, or density regions.

---

## 23. Material-Level Split

A material-general model may hold out complete material systems.

---

## 24. Leakage

Data leakage occurs when information from validation or test evaluation influences parameter optimization outside the declared protocol.

---

## 25. Duplicate Configuration

Symmetry-equivalent or numerically duplicated configurations may create leakage if placed across splits without accounting for equivalence.

---

## 26. Symmetry-Equivalent Samples

Configurations related by rigid E(3) transformation represent equivalent geometry under the declared symmetry.

Their treatment in dataset splitting must be explicit.

---

## 27. Permutation-Equivalent Samples

Atom-permuted copies of the same configuration are not independent physical samples under the permutation symmetry contract.

---

## 28. Energy Reference

A supervised energy target is:

`E_k^ref`.

The model predicts:

`E_k^pred`.

---

## 29. Force Reference

For atom:

`i`:

`F_ki^ref ∈ R^3`.

The model predicts:

`F_ki^pred`.

---

## 30. Stress Reference

A reference stress tensor is:

`Sigma_k^ref`.

The model predicts:

`Sigma_k^pred`.

---

## 31. Resonance Reference

When explicit resonance supervision exists:

`r_k^ref ∈ X_R`.

---

## 32. Ternary Reference

When explicit ternary supervision exists:

`t_k^ref ∈ {-1,0,1}`

or:

`t_k^ref ∈ {-1,0,1}^M`.

---

## 33. Target versus Executed Supervision

If ternary supervision is used, the dataset must distinguish:

- target state;
- executed state.

These are different labels.

---

## 34. Pending-State Supervision

A dataset may additionally contain:

`t_pending`.

This remains distinct from:

`t_target`

and:

`t_exec`.

---

## 35. Learning Energy

Energy learning fits a scalar invariant output.

---

## 36. Learning Force

Force learning fits a per-atom equivariant vector output.

---

## 37. Learning Stress

Stress learning fits a tensor output.

---

## 38. Learning Resonance

Resonance learning fits a separately typed resonance state.

---

## 39. Learning Ternary State

Ternary learning fits exact categorical state.

A continuous surrogate may be used internally for optimization.

The semantic forward state remains separate.

---

## 40. Multi-Task Learning

A TR-EIP model may be trained jointly on several outputs.

A generic objective may be:

`L = w_E L_E + w_F L_F + w_S L_S + w_R L_R + w_T L_T + L_reg`.

---

## 41. Loss Weights

The coefficients:

`w_E`

`w_F`

`w_S`

`w_R`

`w_T`

control relative contribution of loss terms.

They are optimization parameters or fixed hyperparameters, not physical observables by identity.

---

## 42. Unit Compatibility in Loss

Loss terms involving quantities with different units require explicit normalization or weighting.

Raw addition of dimensionally incompatible residuals without a declared normalization is not semantically meaningful.

---

## 43. Energy Residual

Define:

`Delta E_k = E_k^pred - E_k^ref`.

---

## 44. Force Residual

Define:

`Delta F_ki = F_ki^pred - F_ki^ref`.

---

## 45. Stress Residual

Define:

`Delta Sigma_k = Sigma_k^pred - Sigma_k^ref`.

---

## 46. Resonance Residual

For continuous resonance:

`Delta r_k = r_k^pred - r_k^ref`

when both states share a compatible coordinate representation.

---

## 47. Ternary Error

For exact ternary state, error may be measured through:

- categorical mismatch;
- confusion matrix;
- class-specific metrics;
- surrogate loss.

The exact training loss is developed in later chapters.

---

## 48. Extensive Energy Scaling

Total energy generally scales with system size.

A learning objective may normalize energy residual by:

- number of atoms;
- reference scale;
- another declared factor.

---

## 49. Energy per Atom Objective

A normalized residual may use:

`Delta E_k / N_k`.

This changes weighting across system sizes.

---

## 50. Force Component Count

A configuration with:

`N_k`

atoms contains:

`3N_k`

force components.

Loss normalization must define whether configurations or individual components carry equal weight.

---

## 51. Stress Component Weighting

Stress loss must define whether all tensor components are weighted equally or according to another declared rule.

---

## 52. Training Sample Weight

Each sample may carry:

`w_k ≥ 0`.

A weighted objective may be:

`L = sum_k w_k L_k`.

---

## 53. Importance Weighting

Weights may reflect:

- dataset balancing;
- composition balancing;
- state-space coverage;
- uncertainty;
- source confidence;
- target importance.

The weighting rule must be explicit.

---

## 54. Source Provenance Weighting

Reference data from different provenance classes may be weighted differently if the training protocol defines such a rule.

---

## 55. Reference Provenance

Training references retain the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 56. Primary-Source Training Data

Reference observables obtained from external scientific source data carry:

`PRIMARY_SOURCE`

provenance.

---

## 57. Derived Training Target

A target computed from another reference quantity may carry:

`DERIVED`

provenance.

---

## 58. Calibrated Target

A target adjusted through a calibration process carries:

`CALIBRATED`.

---

## 59. Test Fixture Target

Synthetic expected outputs used for invariant tests carry:

`TEST_FIXTURE`.

---

## 60. Learning from Synthetic Data

Synthetic configurations may augment training data.

Their origin and generation process must remain explicit.

---

## 61. Learning from Molecular Dynamics

Trajectory frames may provide correlated samples.

The temporal correlation structure should be accounted for in split and weighting protocols.

---

## 62. Learning from Static Calculations

Independent static configurations may provide energy, force, and stress references.

---

## 63. Learning from Experimental Observables

Experimental observables may enter through direct or indirect loss terms when a forward mapping connects model state to the measured quantity.

---

## 64. Indirect Supervision

If measured observable:

`O_ref`

is not a direct model output, define:

`O_pred = P_O(M(X))`.

The loss compares:

`O_pred`

with:

`O_ref`.

---

## 65. Forward Observable Mapping

The observable map:

`P_O`

must preserve its own units, semantics, and provenance.

---

## 66. Identifiability

A learning problem is identifiable only to the extent that the available data and model structure distinguish relevant parameter states.

---

## 67. Parameter Degeneracy

Different parameter sets may produce equivalent or nearly equivalent predictions over the training domain.

---

## 68. Representation Gauge Freedom

Internal representation basis freedom may create parameter nonuniqueness without changing physical outputs.

---

## 69. Energy Offset Degeneracy

If only forces are trained, adding a constant energy offset does not alter forces.

Absolute energy reference is then underdetermined unless separately constrained.

---

## 70. Species Reference Degeneracy

Species-dependent reference energies may introduce additional gauge-like freedom depending on dataset composition.

---

## 71. Force-Only Learning

A force-only objective may determine energy gradients without uniquely fixing absolute energy.

---

## 72. Energy-Only Learning

Energy-only supervision does not directly constrain every local force component unless the learned energy surface is sufficiently sampled and differentiated.

---

## 73. Joint Energy-Force Learning

Joint energy-force supervision constrains both scalar values and coordinate derivatives.

---

## 74. Stress Supervision

Stress adds constraints on cell or strain derivatives.

---

## 75. Conservative Architecture

For a conservative model:

`F = -grad_R E`.

Force predictions are not independently parameterized unless an additional head is present.

---

## 76. Direct Force Architecture

A direct force head predicts:

`F_direct`.

If used, its relation to energy must be separately constrained when conservative consistency is required.

---

## 77. Energy-Force Consistency Objective

A hybrid model may include:

`L_EF`

penalizing disagreement between:

`F_direct`

and:

`-grad_R E`.

---

## 78. Equivariance Constraint

A learning problem may include exact architectural equivariance or an explicit equivariance loss.

These are distinct mechanisms.

---

## 79. Architectural Equivariance

An equivariant architecture satisfies its transformation law by construction for all admissible parameters.

---

## 80. Equivariance Regularization

A regularizer may penalize:

`M(gX)`

versus transformed:

`M(X)`.

This does not replace architectural equivariance by identity.

---

## 81. Permutation Constraint

Per-atom outputs must remain permutation equivariant.

Global scalar outputs remain permutation invariant.

---

## 82. Energy Symmetry Constraint

Energy must remain invariant under the declared spatial symmetry.

---

## 83. Force Symmetry Constraint

Force must remain equivariant.

---

## 84. Stress Symmetry Constraint

Stress must retain its declared tensor transformation.

---

## 85. Resonance Symmetry Constraint

Resonance channels must preserve their declared transformation type.

---

## 86. Ternary Symmetry Constraint

Canonical scalar ternary channels remain invariant under rigid spatial transformations.

---

## 87. Ternary Domain Constraint

A hard ternary forward state must satisfy:

`t ∈ {-1,0,1}`.

---

## 88. Active-Neutral Constraint

The state:

`0`

remains a valid active semantic state.

Training must not treat:

`0`

as missing or invalid data.

---

## 89. Invalid-State Separation

The learning system must preserve:

`0 ≠ INVALID`

`0 ≠ NONE`

`0 ≠ NaN`

`0 ≠ MASKED`

`0 ≠ PADDED`.

---

## 90. Target/Execution Separation

If target and execution states are both modeled, they must remain separate tensors or state fields.

---

## 91. Direct-Opposite Execution Constraint

Training cannot authorize committed:

`-1 → 1`

or:

`1 → -1`.

---

## 92. Neutral-Mediated Execution Constraint

Execution-bound models preserve:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 93. Transition Loss Boundary

A loss may encourage target behavior.

It cannot redefine the execution graph.

---

## 94. Surrogate Ternary Learning

A continuous surrogate may represent pre-classification logits or scores.

The exact semantic output remains downstream of the hard classifier.

---

## 95. Logit State

For three classes, logits may be:

`z = (z_-, z_0, z_+)`.

These are continuous.

They are not ternary states.

---

## 96. Probability State

Probabilities may be:

`p = (p_-, p_0, p_+)`.

They satisfy:

`p_- + p_0 + p_+ = 1`.

They are not ternary state.

---

## 97. Hard Decision

A decision operator:

`D_T`

maps the continuous classifier state into exact:

`-1/0/1`.

---

## 98. Straight-Through Gradient Boundary

A straight-through estimator may define one backward approximation while retaining an exact hard forward state.

Forward and backward semantics remain distinct.

---

## 99. Ternary Class Imbalance

If:

`-1`

`0`

`1`

occur with unequal frequencies, the training objective may use class weighting.

---

## 100. Neutral-State Imbalance

Active-neutral frequency must be measured as a real class frequency, not merged with invalid or missing samples.

---

## 101. Resonance Supervision

Resonance learning may use direct resonance labels or indirect downstream losses.

---

## 102. Latent Resonance Learning

A resonance state may remain latent while being constrained by:

- energy;
- force;
- ternary;
- structural;
- temporal objectives.

---

## 103. Resonance Identifiability

A latent resonance representation may not be uniquely determined by downstream observables.

Its semantics must therefore be established through architecture, constraints, calibration, or direct supervision.

---

## 104. Resonance Regularization Boundary

Volume 04 Chapter 06 defines resonance regularization.

This chapter establishes only the learning-problem role of resonance state.

---

## 105. Ternary Regularization Boundary

Volume 04 Chapter 05 defines ternary regularization.

---

## 106. Equivariance Constraint Boundary

Volume 04 Chapter 07 defines explicit equivariance constraints.

---

## 107. Uncertainty Boundary

Volume 04 Chapter 08 defines uncertainty and domain detection.

---

## 108. Optimization Boundary

Volume 04 Chapter 09 defines optimization algorithms and numerical training procedure.

---

## 109. Empirical Risk

For dataset:

`D_train`

the empirical objective may be:

`L_emp(Theta) = (1/K) sum_(k=1)^K L_k(Theta)`.

---

## 110. Weighted Empirical Risk

A weighted form is:

`L_emp(Theta) = [sum_k w_k L_k] / [sum_k w_k]`

when:

`sum_k w_k > 0`.

---

## 111. Regularized Objective

A regularized objective is:

`L_total = L_emp + lambda R(Theta)`.

The regularizer:

`R`

may encode model-specific constraints.

---

## 112. Multiple Regularizers

A general objective may contain:

`L_total = L_data + L_ternary + L_resonance + L_equivariance + L_consistency + L_parameter`.

---

## 113. Constraint Formulation

The learning problem may also be expressed:

`min_Theta L(Theta)`

subject to:

`C_j(Theta) = 0`

and:

`G_k(Theta) ≤ 0`.

---

## 114. Hard Constraint

A hard architectural constraint excludes violating parameter states from the admissible model family.

---

## 115. Soft Constraint

A soft constraint adds a finite penalty to the objective.

---

## 116. Constraint Priority

Hard invariants and soft regularizers remain distinct.

A soft penalty does not convert a forbidden state into an allowed one.

---

## 117. Feasible Parameter Set

Define:

`Theta_adm`

as the set of parameter states satisfying all hard model constraints.

The learning problem is:

`Theta_star = argmin_(Theta ∈ Theta_adm) L(Theta)`.

---

## 118. Parameter Initialization

Optimization starts from:

`Theta_0`.

Initialization may be:

- random;
- analytic;
- pretrained;
- transferred;
- calibrated.

---

## 119. Initialization Provenance

The origin of:

`Theta_0`

must be recorded when it affects reproducibility.

---

## 120. Random Initialization

Random initialization requires explicit random-state semantics.

---

## 121. Pretrained Initialization

A pretrained parameter state requires source model identity and parameter artifact provenance.

---

## 122. Transfer Initialization

Transfer learning uses parameters from a related model or domain.

The transferred parameter subset must be explicit.

---

## 123. Frozen Transfer Layers

Transferred parameters may remain frozen while other parameters are optimized.

---

## 124. Fine Tuning

Fine tuning modifies some or all pretrained parameters on a new dataset or domain.

---

## 125. Calibration after Training

A model may undergo a separate calibration stage after parameter optimization.

Training and calibration remain distinct processes when they use distinct objectives or parameter sets.

---

## 126. Hyperparameters

Hyperparameters may include:

- learning rate;
- batch size;
- optimizer configuration;
- regularization coefficients;
- scheduler settings;
- number of epochs.

They are not model observables.

---

## 127. Architecture Hyperparameters

Architecture hyperparameters may include:

- cutoff;
- `l_max`;
- channel multiplicities;
- message depth;
- resonance dimension;
- ternary channel count.

Changing some architecture hyperparameters may define a different architecture member.

---

## 128. Model Selection

Validation performance may be used to select among:

- architectures;
- hyperparameters;
- checkpoints.

---

## 129. Checkpoint

A training checkpoint may include:

- parameter state;
- optimizer state;
- scheduler state;
- random generator state;
- training step;
- validation metrics.

---

## 130. Restart-Complete Training State

Exact training restart may require all result-affecting optimizer and random state.

---

## 131. Training Step

Let:

`n_train`

denote optimization step.

This is not:

- physical time;
- MD timestep;
- message-passing layer;
- ternary execution tact.

---

## 132. Epoch

An epoch denotes one declared traversal of the training dataset or sampler-defined equivalent.

---

## 133. Batch

A batch is a finite collection of training samples evaluated together.

---

## 134. Batch Graph

Independent atomistic systems may be batched computationally.

No physical interaction exists between separate batch members.

---

## 135. Batch Index

Batch identity is computational metadata.

It is not a material or physical state.

---

## 136. Batch Normalization Boundary

Any batch-dependent representation operation must preserve the declared symmetry and graph separation.

---

## 137. Gradient

The optimization gradient is:

`grad_Theta L`.

It is a derivative with respect to model parameters.

---

## 138. Parameter Gradient versus Force

The distinction remains:

`parameter gradient ≠ mechanical force`.

---

## 139. Coordinate Gradient

The force relation uses:

`grad_R E`.

Training uses:

`grad_Theta L`.

These gradients belong to different spaces.

---

## 140. Gradient Flow through Force

When force loss depends on:

`F = -grad_R E`,

optimization may require mixed derivatives involving model parameters and atomic coordinates.

---

## 141. Second-Order Derivative Path

Force training of an energy model can require differentiating coordinate gradients with respect to parameters.

The implementation must support the required derivative graph.

---

## 142. Stress Gradient Path

Stress training may similarly require derivatives through cell or strain dependence.

---

## 143. Hard Ternary Gradient Boundary

Exact ternary classification is nondifferentiable at decision boundaries.

A training method must define how optimization traverses this boundary.

---

## 144. Differentiable Surrogate

A surrogate may provide gradients while the hard classifier preserves semantic outputs.

---

## 145. Surrogate Mismatch

The backward surrogate and hard forward dynamics may differ.

This difference must remain explicit.

---

## 146. Learning Stability

Optimization stability refers to behavior of the training procedure.

It is distinct from dynamical stability of the modeled physical system.

---

## 147. Optimization Convergence

Optimization convergence concerns parameter updates and objective behavior.

It is not physical equilibrium.

---

## 148. Loss Plateau

A stable or flat training loss does not establish model correctness by identity.

It is an optimization-state observation.

---

## 149. Overfitting

Overfitting occurs when the model fits the training domain more closely than it generalizes to the declared validation/test domain.

---

## 150. Underfitting

Underfitting occurs when the model cannot adequately fit the training objective under the selected architecture and optimization process.

---

## 151. Capacity

Model capacity depends on:

- channel multiplicities;
- angular degree;
- message depth;
- parameter count;
- resonance state dimension;
- ternary structure.

---

## 152. Capacity versus Physical Complexity

Large parameter count does not itself define physical fidelity.

---

## 153. Generalization

Generalization is evaluated on configurations outside the training sample set but within the declared evaluation domain.

---

## 154. Interpolation

Interpolation refers to prediction within regions represented by training data under a declared notion of proximity.

---

## 155. Extrapolation

Extrapolation refers to prediction beyond the represented training domain under the selected descriptor or physical state definition.

---

## 156. Domain Definition

The meaning of interpolation or extrapolation depends on the model-domain representation.

---

## 157. Composition Extrapolation

A model may extrapolate to compositions not represented in training.

---

## 158. Structural Extrapolation

A model may encounter new coordination or structural motifs.

---

## 159. Thermodynamic Extrapolation

A model may encounter temperature-, pressure-, or density-related states outside training coverage.

---

## 160. Out-of-Domain Detection

Explicit domain detection is developed in Chapter 08.

Out-of-domain state remains separate from active-neutral ternary state.

---

## 161. Uncertainty

A model may produce uncertainty estimates:

`U(X)`.

Uncertainty remains distinct from error, resonance, and ternary state.

---

## 162. Aleatoric Uncertainty

A model may represent irreducible observational or data variability under a declared probabilistic formulation.

---

## 163. Epistemic Uncertainty

A model may represent uncertainty associated with limited model knowledge or data coverage.

---

## 164. Uncertainty versus Neutral

The distinction remains:

`uncertain ≠ ternary 0`.

---

## 165. Error versus Uncertainty

Observed prediction error and predicted uncertainty are distinct quantities.

---

## 166. Training Metric

A training metric measures behavior on:

`D_train`.

---

## 167. Validation Metric

A validation metric measures behavior on:

`D_val`.

---

## 168. Test Metric

A test metric measures behavior on:

`D_test`.

---

## 169. Optimization Objective versus Reporting Metric

A reported metric need not be identical to the optimized loss.

---

## 170. Energy Metrics

Possible energy metrics include:

- MAE;
- RMSE;
- per-atom MAE;
- relative error under a declared denominator.

---

## 171. Force Metrics

Possible force metrics include:

- component MAE;
- vector-norm MAE;
- RMSE;
- maximum error;
- angular error where relevant.

---

## 172. Stress Metrics

Possible stress metrics include:

- component MAE;
- tensor norm error;
- invariant error.

---

## 173. Ternary Metrics

Possible ternary metrics include:

- exact accuracy;
- class-specific precision;
- class-specific recall;
- confusion matrix;
- transition accuracy.

---

## 174. Neutral-State Metric

Performance for state:

`0`

should be reported separately when its behavior is materially distinct.

---

## 175. Transition Metrics

Execution-bound models may measure:

- first-leg accuracy;
- neutral residence behavior;
- second-leg accuracy;
- direct-opposite violations.

---

## 176. Hard Invariant Metric

The required direct-opposite violation count is:

`0`.

This is an invariant check, not an averaged regression metric.

---

## 177. Equivariance Metric

A numerical residual may evaluate:

`M(gX)`

against transformed:

`M(X)`.

---

## 178. Conservation Metric

A conservative model may evaluate:

`F + grad_R E`.

---

## 179. Deterministic Replay Metric

A model may evaluate exact or tolerance-based replay according to its numerical contract.

---

## 180. Training Determinism

Exact training replay may require deterministic:

- data ordering;
- random state;
- graph construction;
- reductions;
- optimizer updates.

---

## 181. Inference Determinism

Inference determinism can be stricter or simpler than training determinism.

---

## 182. Numerical Precision

Training may use:

- float64;
- float32;
- mixed precision;
- another declared arithmetic.

---

## 183. Mixed Precision

Mixed precision changes numerical behavior and must be part of the training configuration.

---

## 184. Gradient Scaling

Mixed-precision training may use gradient scaling.

This is an optimization mechanism.

---

## 185. Numerical Overflow

Overflow in loss, gradients, or parameters is an invalid numerical event.

It is not ternary active neutral.

---

## 186. NaN Gradient

A:

`NaN`

parameter gradient is an invalid optimization state.

---

## 187. Gradient Clipping

Gradient clipping may restrict optimization update magnitude.

It does not clip physical force unless an entirely separate force operation is defined.

---

## 188. Parameter Regularization

Regularization may constrain:

- parameter norm;
- smoothness;
- sparsity;
- spectral properties;
- channel usage.

---

## 189. Physical Regularization

A loss may encode physical constraints such as:

- equivariance;
- energy-force consistency;
- conservation-related conditions;
- smoothness.

---

## 190. Ternary Regularization

A loss may encourage:

- stable neutral regions;
- channel sparsity;
- balanced occupancy;
- transition consistency.

The exact formulations belong to Chapter 05.

---

## 191. Resonance Regularization

A loss may constrain:

- resonance smoothness;
- window structure;
- scale consistency;
- temporal persistence.

The exact formulations belong to Chapter 06.

---

## 192. Loss Term versus Physical Energy

The training loss:

`L`

is not the physical interatomic energy:

`E`.

---

## 193. Parameter Gradient versus Energy Gradient

The framework preserves:

`grad_Theta L ≠ grad_R E`.

---

## 194. Optimization Landscape versus Energy Landscape

The parameter-space optimization landscape is not the atomic potential-energy surface.

---

## 195. Training Epoch versus Physical Time

The distinction remains:

`training epoch ≠ physical time`.

---

## 196. Optimization Step versus Ternary Tact

The distinction remains:

`optimization step ≠ ternary execution tact`.

---

## 197. Model Checkpoint versus Physical State

A training checkpoint is a computational artifact.

It is not an atomic configuration.

---

## 198. Data Augmentation

Data augmentation may apply symmetry transformations to training configurations.

---

## 199. Rotational Augmentation

A configuration may be rotated:

`R' = QR`.

Invariant scalar references remain unchanged.

Vector references rotate.

Tensor references transform.

---

## 200. Translation Augmentation

A global translation preserves internal energy and forces under the corresponding isolated model symmetry.

---

## 201. Permutation Augmentation

Species-preserving atom permutation produces equivalent relabeling of per-atom outputs.

---

## 202. Reflection Augmentation

Reflection may be used when the model and reference system support the declared:

`O(3)`

symmetry.

---

## 203. Augmentation versus Equivariance

The framework preserves:

`data augmentation ≠ architectural equivariance`.

---

## 204. Augmentation Consistency

Augmented inputs require correspondingly transformed labels.

---

## 205. Force Label Rotation

For:

`R' = QR`:

`F_i^ref' = QF_i^ref`.

---

## 206. Stress Label Rotation

For:

`R' = QR`:

`Sigma_ref' = Q Sigma_ref Q^T`.

---

## 207. Scalar Label Invariance

Energy and scalar invariant labels remain unchanged under rigid symmetry transformation.

---

## 208. Ternary Label Invariance

Canonical scalar ternary labels remain unchanged under rigid spatial transformation.

---

## 209. Dataset Normalization

Continuous inputs and outputs may be normalized for optimization.

Normalization must preserve units or define nondimensionalization explicitly.

---

## 210. Energy Centering

Energy references may be centered by subtracting a reference energy.

This does not change force labels.

---

## 211. Force Scaling

Force targets may be scaled numerically for optimization.

The inverse transformation must be explicit.

---

## 212. Stress Scaling

Stress targets may likewise be normalized.

---

## 213. Feature Standardization

Invariant scalar features may be standardized.

Equivariant vector/tensor channels require transformation-compatible normalization.

---

## 214. Dataset Statistics

Normalization statistics should be derived from the declared training data unless another source is explicitly specified.

---

## 215. Validation Leakage through Statistics

Using validation/test statistics in training normalization can create leakage if the protocol requires strict separation.

---

## 216. Training Artifact

A complete training artifact may include:

- model manifest;
- parameter checkpoint;
- optimizer state;
- dataset identifiers;
- split definition;
- loss definition;
- hyperparameters;
- random state;
- metrics;
- provenance.

---

## 217. Model Artifact

The trained model artifact is distinct from the training-process artifact.

---

## 218. Parameter Artifact

A parameter artifact stores optimized parameter values.

---

## 219. Optimizer Artifact

An optimizer artifact stores training-state variables required for continuation.

---

## 220. Dataset Manifest

A dataset manifest identifies:

- source;
- version;
- split;
- units;
- species;
- state domain;
- reference quantities.

---

## 221. Training Manifest

A training manifest binds:

- model;
- data;
- objective;
- optimizer;
- numerical realization.

---

## 222. Reproducibility

A reproducible learning result requires sufficient information to reconstruct the declared training procedure.

---

## 223. Training Replay

Exact training replay may require:

- identical model initialization;
- identical data order;
- identical random state;
- identical arithmetic;
- identical optimizer state.

---

## 224. Inference Replay after Training

The final parameter artifact should permit deterministic inference under the model's inference contract.

---

## 225. Hyperparameter Search

A model-selection procedure may evaluate multiple hyperparameter configurations.

Each configuration is a separate experiment.

---

## 226. Search Objective

The hyperparameter search objective may differ from the parameter-training loss.

---

## 227. Validation-Based Selection

A selected model may minimize or otherwise optimize a declared validation criterion.

---

## 228. Test Isolation

The test split should not drive iterative hyperparameter selection under a strict holdout protocol.

---

## 229. Early Stopping

Training may terminate when a declared validation criterion stops improving.

---

## 230. Early-Stopping State

The best checkpoint and stopping criterion must be explicit.

---

## 231. Learning Rate Schedule

The optimization learning rate may vary with training step.

---

## 232. Optimizer State

Adaptive optimizers retain internal moments or other state.

This state belongs to restart-complete training state.

---

## 233. Parameter Constraint Projection

An optimizer may project updated parameters back into:

`Theta_adm`.

---

## 234. Symmetry-Preserving Parameterization

A stronger strategy encodes constraints directly in the parameterization so invalid states cannot be represented.

---

## 235. Conservative Parameterization

Energy-based force construction is one example of structural constraint.

---

## 236. Exact Ternary Execution Constraint

Neutral-mediated execution is another hard architectural constraint.

It is not learned through a penalty.

---

## 237. Learned Ternary Decision Boundary

Thresholds or decision surfaces may be trainable.

Their learned values do not alter the exact output set:

`-1/0/1`.

---

## 238. Learned Resonance Window

A resonance window may be parameterized and learned.

Its geometry remains defined in:

`X_R`.

---

## 239. Learned Graph Parameters

Graph cutoffs or edge scores may be learned if the architecture defines a differentiable or discrete graph-learning mechanism.

---

## 240. Learned Cutoff Boundary

A learned cutoff remains a graph parameter.

It is not a resonance boundary or ternary decision boundary by identity.

---

## 241. Learned Energy Surface

A learned energy functional approximates or represents the declared interatomic energy mapping over the training domain.

---

## 242. Learned Force Surface

A direct force model approximates or represents the declared mechanical vector field.

---

## 243. Learned Stress Mapping

A learned stress head approximates the declared tensor mapping.

---

## 244. Learning Problem Extension Rule

Any new learning problem must define:

1. model family member;
2. trainable parameter set;
3. training domain;
4. validation domain;
5. target outputs;
6. units;
7. loss terms;
8. hard constraints;
9. regularizers;
10. optimizer interface;
11. metrics;
12. reproducibility state;
13. provenance.

---

## 245. Dataset Extension Rule

Any new training dataset must define:

1. source;
2. version;
3. species;
4. configurations;
5. units;
6. target quantities;
7. split;
8. provenance;
9. quality flags;
10. duplicate handling.

---

## 246. Target Extension Rule

Any new target must define:

1. output space;
2. units;
3. symmetry behavior;
4. reference source;
5. uncertainty where available;
6. loss interface.

---

## 247. Constraint Extension Rule

Any new hard constraint must define:

1. constrained state;
2. mathematical condition;
3. enforcement mechanism;
4. validation.

---

## 248. Regularizer Extension Rule

Any regularizer must define:

1. target quantity;
2. formula;
3. coefficient;
4. units or normalization;
5. optimization role.

---

## 249. Metric Extension Rule

Any reporting metric must define:

1. quantity;
2. aggregation;
3. normalization;
4. units;
5. split;
6. interpretation.

---

## 250. Canonical Learning Invariants

Every conforming TR-EIP learning problem preserves:

1. explicit model architecture;

2. explicit trainable parameter set;

3. explicit data domain;

4. explicit output types;

5. explicit unit handling;

6. explicit loss composition;

7. explicit hard constraints;

8. explicit split semantics;

9. explicit reproducibility state;

10. explicit provenance.

---

## 251. Canonical Symmetry Invariants

Learning does not alter the declared:

- translation behavior;
- rotation behavior;
- reflection behavior where applicable;
- atom-permutation behavior;
- output representation types.

---

## 252. Canonical Ternary Invariants

Learning preserves:

`-1/0/1`.

The state:

`0`

remains active neutral.

Target and executed state remain distinct.

Direct committed opposite transitions remain forbidden.

---

## 253. Canonical Conservative Invariants

For conservative models:

`F = -grad_R E`.

Optimization may change:

`E`

through parameters.

It does not change the formal relation.

---

## 254. Canonical State-Separation Invariants

The learning layer preserves:

`loss ≠ physical energy`

`parameter gradient ≠ mechanical force`

`optimization step ≠ physical time`

`training checkpoint ≠ atomic state`

`probability ≠ ternary state`

`uncertainty ≠ active neutral`

`validation status ≠ ternary state`.

---

## 255. Canonical Scientific Distinctions

The learning layer preserves:

`equivariance ≠ conservativity`

`data augmentation ≠ architectural equivariance`

`optimization convergence ≠ physical equilibrium`

`training stability ≠ dynamical stability`

`loss minimum ≠ energy minimum`

`representation similarity ≠ coherence`

`resonance ≠ synchronization`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 256. Canonical Learning Chain

The complete learning chain is:

`TR-EIP architecture`

`+ reference dataset`

`→ prediction`

`→ typed residuals`

`→ loss functionals`

`→ regularization / constraints`

`→ optimization`

`→ updated parameter state`

`→ validation`

`→ model checkpoint`.

---

## 257. Canonical Energy-Force-Stress Learning Chain

For mechanical supervision:

`configuration`

`→ model energy`

`→ force/stress derivatives`

`→ compare with reference E/F/Sigma`

`→ optimize parameters`.

---

## 258. Canonical Ternary Learning Chain

For ternary supervision:

`continuous / resonance state`

`→ classifier state`

`→ exact ternary target`

`→ categorical or surrogate loss`

`→ parameter update`.

Execution semantics remain downstream and fixed.

---

## 259. Canonical Resonance Learning Chain

For resonance supervision:

`equivariant representation`

`→ resonance parameterization`

`→ resonance target comparison`

`→ parameter update`.

---

## 260. Interface to Chapter 02

Chapter 02 develops Training Data.

It defines:

- dataset schemas;
- configuration sampling;
- energy/force/stress references;
- trajectory data;
- dataset splits;
- provenance;
- normalization;
- data quality.

---

## 261. Interface to Chapter 03

Chapter 03 develops Loss Functionals.

It formalizes:

- energy loss;
- force loss;
- stress loss;
- resonance loss;
- ternary loss;
- multi-objective composition.

---

## 262. Interface to Chapter 04

Chapter 04 develops Energy-Force-Stress Training.

It defines derivative-based training and consistency relations among mechanical outputs.

---

## 263. Interface to Chapter 05

Chapter 05 develops Ternary Regularization.

It defines regularization of:

- ternary occupancy;
- transition behavior;
- active-neutral state;
- target stability.

---

## 264. Interface to Chapter 06

Chapter 06 develops Resonance Regularization.

It defines constraints and penalties on resonance coordinates, windows, persistence, and scale consistency.

---

## 265. Interface to Chapter 07

Chapter 07 develops Equivariance Constraints.

It defines explicit symmetry penalties and transformation tests used during training.

---

## 266. Interface to Chapter 08

Chapter 08 develops Uncertainty and Domain Detection.

It defines model uncertainty, data coverage, and out-of-domain state.

---

## 267. Interface to Chapter 09

Chapter 09 develops Optimization.

It defines:

- optimizers;
- schedules;
- batching;
- gradient handling;
- checkpointing;
- convergence criteria.

---

## 268. Final Formal Structure

The TR-EIP learning problem may be represented as:

`LP = (M, Theta, D_train, D_val, D_test, Y_ref, L, C, R, O, V)`.

Here:

- `M` is the selected TR-EIP model;
- `Theta` is the trainable parameter set;
- `D_train` is the training domain;
- `D_val` is the validation domain;
- `D_test` is the test domain;
- `Y_ref` is the reference output state;
- `L` is the data loss;
- `C` is the hard-constraint set;
- `R` is the regularization set;
- `O` is the optimization procedure;
- `V` is the evaluation and validation contract.

The canonical optimization problem is:

`Theta_star = argmin_(Theta ∈ Theta_adm) L_total(Theta)`.

---

## 269. Final Statement

The learning problem defines how a fixed TR-EIP architecture becomes a parameterized model instance through reference data and optimization.

Training acts on explicitly declared trainable parameters.

It does not redefine the architecture's state semantics.

The learning layer preserves:

`atomic configuration`

`interaction graph`

`E(3) equivariance`

`resonance state`

`-1/0/1`

`active neutral 0`

`target/execution separation`

`conservative energy`

`force equivariance`

`stress tensor semantics`.

The framework preserves the distinctions:

`loss ≠ physical energy`

`parameter gradient ≠ force`

`training step ≠ physical time`

`probability ≠ ternary state`

`uncertainty ≠ active neutral`

`optimization convergence ≠ physical equilibrium`

`data augmentation ≠ architectural equivariance`.

For conservative models:

`F = -grad_R E`.

For execution-bound ternary state:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

remain the canonical opposite-polarity routes.

These definitions establish the learning problem required for the Training Data formalism developed in Chapter 02.
