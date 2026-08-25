# Energy-Force-Stress Training

## 1. Purpose

This chapter defines joint training of energy, force, and stress within the TR-EIP learning and optimization layer of TR-EIF.

The mechanical training layer connects reference observables to the conservative interatomic model while preserving:

- scalar energy semantics;
- vector force semantics;
- tensor stress semantics;
- conservative energy-force relations where declared;
- E(3) symmetry;
- atom-permutation symmetry;
- unit consistency;
- differentiability;
- explicit target availability;
- deterministic derivative evaluation.

The canonical mechanical learning chain is:

`atomic configuration`

`→ TR-EIP model`

`→ predicted energy`

`→ coordinate/cell derivatives`

`→ predicted force and stress`

`→ typed residuals`

`→ mechanical loss`

`→ parameter update`.

---

## 2. Mechanical Training State

For sample:

`k`

the reference mechanical state may be:

`Y_k,mech^ref = (E_k^ref, F_k^ref, Sigma_k^ref)`.

The predicted state is:

`Y_k,mech^pred = (E_k^pred, F_k^pred, Sigma_k^pred)`.

Not every sample must contain all three reference fields.

---

## 3. Energy Target

Reference energy is a scalar:

`E_k^ref ∈ R`.

Its units and reference zero must be explicit.

---

## 4. Force Target

For atom:

`i`

the reference force is:

`F_ki^ref ∈ R^3`.

The force array must preserve the atom ordering of the corresponding configuration.

---

## 5. Stress Target

Reference stress is:

`Sigma_k^ref ∈ R^(3×3)`

or an explicitly declared reduced representation.

The tensor type, sign convention, units, and component ordering must be explicit.

---

## 6. Conservative Prediction Path

For a conservative model:

`E_k^pred = E(X_k; Theta)`.

Force is derived as:

`F_ki^pred = -grad_(r_ki) E_k^pred`.

Stress is derived through the declared cell or strain derivative.

---

## 7. Direct Force Path

A model may additionally or alternatively define:

`F_k^direct = P_F(X_k; Theta)`.

This path remains distinct from the conservative energy-gradient path.

---

## 8. Direct Stress Path

A model may define:

`Sigma_k^direct = P_Sigma(X_k; Theta)`.

Its tensor semantics and relation to energy must be explicit.

---

## 9. Conservative versus Direct Training

The distinction remains:

`energy-derived force training ≠ direct force-head training`.

Likewise:

`energy-derived stress training ≠ direct stress-head training`.

---

## 10. Energy-Force Consistency

For a conservative model:

`F_i = -grad_(r_i) E`.

This relation is structural.

It is not an empirical approximation.

---

## 11. Energy-Stress Consistency

For an energy-derived stress model, stress must follow the declared derivative relation with respect to cell or strain state.

The exact convention must remain fixed across training and validation.

---

## 12. Energy Loss

A generic energy loss is:

`L_E = A_E(E_pred - E_ref)`.

The reduction and normalization are defined by the training protocol.

---

## 13. Force Loss

A generic force loss is:

`L_F = A_F(F_pred - F_ref)`.

The reduction may operate over:

- atoms;
- vector components;
- configurations.

---

## 14. Stress Loss

A generic stress loss is:

`L_S = A_S(Sigma_pred - Sigma_ref)`.

The tensor reduction and component weighting must be explicit.

---

## 15. Mechanical Objective

A canonical mechanical objective is:

`L_mech = w_E L_E + w_F L_F + w_S L_S`.

---

## 16. Mechanical Loss Weights

The coefficients:

`w_E`

`w_F`

`w_S`

control optimization weighting.

They are training hyperparameters unless explicitly learned.

---

## 17. Unit-Aware Weighting

Energy, force, and stress have different units.

Their loss terms must therefore be normalized or weighted with dimensionally compatible coefficients before summation.

---

## 18. Energy Units

Energy uses declared physical units.

---

## 19. Force Units

Force uses:

`energy / length`.

---

## 20. Stress Units

Stress uses:

`energy / volume`

or an equivalent mechanical unit.

---

## 21. Energy Residual

Define:

`Delta E_k = E_k^pred - E_k^ref`.

---

## 22. Force Residual

Define:

`Delta F_ki = F_ki^pred - F_ki^ref`.

---

## 23. Stress Residual

Define:

`Delta Sigma_k = Sigma_k^pred - Sigma_k^ref`.

---

## 24. Energy MAE

A per-sample energy MAE may be:

`L_E,MAE = (1/K_E) sum_k |Delta E_k|`.

---

## 25. Energy MSE

A per-sample energy MSE may be:

`L_E,MSE = (1/K_E) sum_k (Delta E_k)^2`.

---

## 26. Per-Atom Energy Loss

A size-normalized energy residual may use:

`Delta E_k / N_k`.

---

## 27. Total-Energy Weighting

Using total energy gives larger systems potentially larger absolute residual scale.

This is a deliberate loss-design choice.

---

## 28. Per-Atom Weighting

Using per-atom energy changes system-size weighting.

The choice must remain explicit.

---

## 29. Force Component Loss

A componentwise force MSE may be:

`L_F,comp = [1 / sum_k 3N_k] sum_k sum_i ||Delta F_ki||^2`.

---

## 30. Force Vector Loss

A vector-norm loss may use:

`L_F,vec = [1 / sum_k N_k] sum_k sum_i ||Delta F_ki||`.

---

## 31. Force Direction Loss

A direction-sensitive loss may compare normalized force directions where both reference and predicted magnitudes exceed a declared threshold.

---

## 32. Force Magnitude Loss

A magnitude loss may compare:

`||F_pred||`

and:

`||F_ref||`.

---

## 33. Force Vector versus Magnitude

The distinction remains:

`force vector error ≠ force magnitude error`.

---

## 34. Stress Component Loss

Stress may be trained componentwise.

The stored tensor convention must define which components are included.

---

## 35. Stress Frobenius Loss

A tensor loss may use:

`||Delta Sigma||_F`.

---

## 36. Symmetric Stress Weighting

If stress is symmetric, off-diagonal components must have a consistent counting convention.

---

## 37. Pressure Auxiliary Loss

If pressure is derived from stress, a separate scalar pressure loss may be included.

---

## 38. Pressure versus Stress

The distinction remains:

`pressure objective ≠ full stress objective`.

---

## 39. Partial Mechanical Supervision

A sample may contain:

- energy only;
- force only;
- stress only;
- energy and force;
- energy and stress;
- force and stress;
- all three.

---

## 40. Target Masks

Define availability masks:

`m_E,k`

`m_F,k`

`m_S,k`.

Each is computational metadata.

---

## 41. Masked Energy Loss

Energy loss contributes only when:

`m_E,k = 1`.

---

## 42. Masked Force Loss

Force loss contributes only when:

`m_F,k = 1`.

---

## 43. Masked Stress Loss

Stress loss contributes only when:

`m_S,k = 1`.

---

## 44. Mask versus Active Neutral

The invariant remains:

`target mask 0 ≠ ternary neutral 0`.

---

## 45. Missing Mechanical Target

Missing target state is not zero physical value.

---

## 46. Zero Energy Target

`E_ref = 0`

is a valid physical numeric value under the declared reference convention.

---

## 47. Zero Force Target

`F_ref = 0`

is a valid mechanical vector.

It is not ternary neutral.

---

## 48. Zero Stress Target

`Sigma_ref = 0`

is a valid mechanical tensor.

It is not ternary neutral.

---

## 49. Coordinate Differentiation

Force training of an energy model requires:

`grad_R E`.

---

## 50. Parameter Differentiation

Optimization requires:

`grad_Theta L_mech`.

---

## 51. Mixed Derivative Path

When force loss depends on:

`F = -grad_R E`,

parameter optimization may require derivatives of:

`grad_R E`

with respect to:

`Theta`.

---

## 52. Second-Order Automatic Differentiation

Force training of an energy-based model may therefore require second-order differentiation through the computational graph.

---

## 53. Stress Derivative Path

Energy-derived stress training may require derivatives through cell or strain dependence and then through:

`Theta`.

---

## 54. Derivative Graph

All coordinate- and cell-dependent operations contributing to energy must remain connected to the derivative graph when conservative derivatives are required.

---

## 55. Detached State

If a state is detached from the derivative graph, its coordinate-mediated contribution to force or stress is removed.

This changes the mechanical model.

---

## 56. Detached Resonance State

If resonance:

`X_R`

depends on coordinates but is detached before energy evaluation, the resulting force excludes the resonance-mediated derivative path.

---

## 57. Differentiable Resonance Conditioning

If:

`X_R = P_R(R)`

remains in the computational graph and:

`E = E(R, X_R)`,

then:

`dE/dR`

includes both direct and resonance-mediated dependencies.

---

## 58. Ternary Differentiability Boundary

Exact ternary classification is discontinuous.

A hard ternary-conditioned energy defines a hybrid discrete-continuous model.

---

## 59. Fixed-Mode Derivative

For fixed executed ternary state:

`q`

the conservative force is:

`F_q = -grad_R E_q`.

---

## 60. Mode Switching

A change in executed ternary state changes the active energy surface when energy is execution-conditioned.

---

## 61. Target versus Executed Conditioning

If energy uses:

`t_exec`,

changing only:

`t_target`

does not alter the active conservative surface unless another explicit dependency exists.

---

## 62. Active-Neutral Surface

The state:

`0`

may select:

`E_0`.

It does not imply zero energy.

---

## 63. Active-Neutral Force

The corresponding force is:

`F_0 = -grad_R E_0`.

It does not imply zero force.

---

## 64. Opposite Mode Transition

For executed-state-conditioned mechanics:

`E_-1 → E_0 → E_1`

and:

`E_1 → E_0 → E_-1`.

---

## 65. No Direct Opposite Mechanical Commit

A direct:

`E_-1 → E_1`

or:

`E_1 → E_-1`

commit is not permitted when active mechanics follow canonical executed state.

---

## 66. Training across Mode Boundaries

Samples from different ternary modes may jointly train mode-dependent energy surfaces.

Their mode labels must remain explicit.

---

## 67. Mode-Specific Loss

A mode-specific objective may be:

`L_mech,q`

for:

`q ∈ {-1,0,1}`.

---

## 68. Balanced Mode Training

The dataset or sampler may balance samples across ternary modes.

This is distinct from changing the semantic meaning of the modes.

---

## 69. Neutral-Mode Coverage

Training data must preserve explicit coverage of:

`0`

when the neutral surface is part of the model.

---

## 70. Energy Continuity across Mode Boundary

A model may impose:

`E_a = E_b`

at selected switching boundaries.

This is an optional model constraint.

---

## 71. Force Continuity across Mode Boundary

A stronger constraint may impose matching force at a switching boundary.

---

## 72. Continuity Is Model-Specific

No universal equality among:

`E_-1`

`E_0`

`E_1`

or their gradients is assumed.

---

## 73. Conservative Energy Head

An energy head must produce a scalar invariant.

---

## 74. Energy Invariance during Training

For spatial transformation:

`g`

the model must preserve:

`E(gX) = E(X)`

under the declared symmetry.

---

## 75. Force Equivariance during Training

The force must preserve:

`F(gX) = rho_F(g)F(X)`.

---

## 76. Stress Equivariance during Training

Stress must preserve:

`Sigma(gX) = Q Sigma(X) Q^T`.

---

## 77. Permutation Invariance of Energy

Admissible atom permutation must preserve total energy.

---

## 78. Permutation Equivariance of Force

Per-atom forces must permute with atom ordering.

---

## 79. Permutation Invariance of Global Stress

Global stress must remain unchanged under atom relabeling.

---

## 80. Architectural Symmetry

When the model is equivariant by construction, transformed outputs inherit the correct representation structurally.

---

## 81. Symmetry Loss

Additional transformed-data residuals may still be used for numerical validation or regularization.

---

## 82. Rotation-Augmented Mechanical Training

For:

`R' = QR`:

`E_ref' = E_ref`

`F_ref' = QF_ref`

`Sigma_ref' = Q Sigma_ref Q^T`.

---

## 83. Translation-Augmented Training

For a translation-invariant internal model:

`R' = R + c`.

Energy and force references remain unchanged.

---

## 84. Permutation-Augmented Training

Species-preserving permutation requires corresponding permutation of force labels.

---

## 85. Reflection-Augmented Training

Reflection augmentation is valid when the declared model and reference system support the corresponding symmetry.

---

## 86. Augmentation versus Equivariance

The distinction remains:

`mechanical data augmentation ≠ architectural equivariance`.

---

## 87. Energy-Force Joint Training

Joint training uses both scalar energy values and coordinate derivatives.

---

## 88. Force-Rich Supervision

One configuration supplies:

- one total energy scalar;
- `3N` force components.

The relative weight of these targets must be controlled explicitly.

---

## 89. Force Dominance Risk

Without normalization, force terms may numerically dominate the objective because of their larger component count.

The chosen weighting must account for intended optimization balance.

---

## 90. Energy Dominance Risk

Conversely, large energy residual scales may dominate if not normalized.

---

## 91. Stress Weight Scale

Stress may differ numerically by several orders of magnitude depending on units.

Its weighting must be explicit.

---

## 92. Mechanical Scale Factors

Define:

`s_E`

`s_F`

`s_S`

as positive normalization scales.

A dimensionless mechanical objective may use normalized residuals.

---

## 93. Normalized Energy Residual

`r_E = Delta E / s_E`.

---

## 94. Normalized Force Residual

`r_F = Delta F / s_F`.

---

## 95. Normalized Stress Residual

`r_S = Delta Sigma / s_S`.

---

## 96. Scale Source

Normalization scales may be:

- fixed physical scales;
- training-data statistics;
- calibrated values.

Their source must be explicit.

---

## 97. Train-Split Statistics

Under strict split isolation, training normalization statistics come from:

`D_train`.

---

## 98. Mechanical Loss Balance

A normalized objective may be:

`L_mech = w_E A_E(r_E) + w_F A_F(r_F) + w_S A_S(r_S)`.

---

## 99. Sample Weighting

Mechanical samples may carry weights:

`w_k`.

---

## 100. Species Weighting

Force contributions may be weighted by species.

---

## 101. Structure Weighting

Configurations may be weighted by structural class or coordination environment.

---

## 102. Thermodynamic Weighting

States may be weighted by temperature, pressure, density, or composition region.

---

## 103. Provenance Weighting

Reference data from different provenance classes may receive different training weights.

---

## 104. Uncertainty Weighting

Mechanical targets with known uncertainty may be weighted accordingly.

---

## 105. Energy Uncertainty

Reference energy may have:

`sigma_E`.

---

## 106. Force Uncertainty

Reference force may have per-atom or per-component uncertainty.

---

## 107. Stress Uncertainty

Reference stress may have tensor or component uncertainty.

---

## 108. Probabilistic Mechanical Loss

A model may predict both mean and uncertainty and optimize a declared likelihood.

---

## 109. Mechanical Likelihood

The distribution family and covariance assumptions must be explicit.

---

## 110. Isotropic Force Uncertainty

A simplified model may assume one scalar variance per atom.

---

## 111. Anisotropic Force Uncertainty

A richer model may predict covariance structure.

This must transform consistently under rotation.

---

## 112. Stress Covariance

Stress uncertainty may require tensor-aware covariance semantics.

---

## 113. Robust Mechanical Loss

Mechanical objectives may use robust penalties for large residuals.

---

## 114. High-Force Samples

Large-force configurations may be physically important for short-range repulsion.

They should not be treated automatically as outliers.

---

## 115. High-Energy Samples

High-energy configurations may be required to constrain repulsive or transition regions.

---

## 116. Outlier Definition

An outlier criterion must remain separate from absolute magnitude alone.

---

## 117. Reference Inconsistency

A sample may be flagged when energy, force, and stress references do not satisfy the expected source-method consistency.

---

## 118. Mixed Reference Methods

Mechanical labels from different methods may be combined only with explicit semantics.

---

## 119. Force-Only Data

Force-only samples constrain local energy gradients but not absolute energy reference.

---

## 120. Energy-Only Data

Energy-only samples constrain scalar values but provide weaker direct derivative information.

---

## 121. Stress-Only Data

Stress-only samples constrain cell/strain response.

---

## 122. Energy-Force Data

Energy-force pairs jointly constrain value and coordinate derivative.

---

## 123. Energy-Stress Data

Energy-stress pairs jointly constrain value and cell response.

---

## 124. Force-Stress Data

Force-stress pairs constrain coordinate and cell derivatives.

---

## 125. Full Mechanical Data

Samples with:

`E`

`F`

and:

`Sigma`

provide the complete local mechanical supervision set defined in this volume.

---

## 126. Energy Reference Gauge

Potential energy may be shifted by a constant without changing forces.

---

## 127. Force-Only Gauge Freedom

Force-only training cannot uniquely determine this constant energy offset.

---

## 128. Species Reference Gauge

Composition-dependent reference terms may introduce additional freedom.

---

## 129. Energy Alignment

Energy targets from different source sets may require explicit alignment before joint training.

---

## 130. Energy Offset Fit

An offset may be:

- fixed;
- fitted;
- species-dependent;
- source-dependent.

The choice must be explicit.

---

## 131. Offset versus Learned Interaction

Reference offsets should remain distinguishable from learned interaction energy.

---

## 132. Force Sum Constraint

For an isolated translation-invariant internal model:

`sum_i F_i = 0`.

---

## 133. Net-Force Penalty

A soft penalty may be:

`L_netF = ||sum_i F_i||^2`.

---

## 134. Structural versus Redundant Constraint

If the force comes from a translation-invariant scalar energy, the net-force property may already follow structurally.

---

## 135. Torque Constraint

For rotationally invariant isolated internal energy, total internal torque obeys the corresponding relation.

---

## 136. Torque Penalty

A soft numerical penalty may be used where appropriate:

`L_tau = ||sum_i r_i × F_i||^2`

under the declared origin and assumptions.

---

## 137. Conservative Consistency Head

For a model with direct force:

`F_direct`

and energy:

`E`,

define:

`L_cons = ||F_direct + grad_R E||^2`.

---

## 138. Conservative Consistency Weight

The coefficient:

`w_cons`

controls its contribution.

---

## 139. Direct Stress Consistency

A direct stress head may likewise be constrained against an energy-derived stress.

---

## 140. Stress Consistency Loss

Define:

`L_S,cons = ||Sigma_direct - Sigma_E||`.

---

## 141. Energy Gradient Validation

Training may periodically compare automatic differentiation with finite-difference estimates on selected fixtures.

---

## 142. Finite-Difference Force Check

For coordinate perturbation:

`delta`

a central difference approximates:

`F_i,a`.

---

## 143. Finite-Strain Stress Check

Small controlled strain perturbations may approximate the declared energy-stress derivative.

---

## 144. Finite-Difference Checks Are Validation

Finite differences need not be part of every training update.

They may serve as independent derivative validation.

---

## 145. Cutoff Differentiability

Mechanical training requires attention to graph and energy behavior near interaction cutoffs.

---

## 146. Hard Cutoff Boundary

A hard neighbor cutoff can create derivative discontinuities if energy terms do not vanish smoothly.

---

## 147. Smooth Cutoff

A smooth cutoff can preserve continuity of energy and selected derivatives.

---

## 148. Force-Smooth Requirement

If continuous force is required, cutoff behavior must provide the necessary first derivative continuity.

---

## 149. Stress-Smooth Requirement

Cell-dependent cutoff changes may affect stress derivatives.

---

## 150. Higher-Order Smoothness

Second-derivative applications require additional smoothness.

---

## 151. Graph Topology Change

A graph edge entering or leaving the cutoff may create a discrete computational event.

---

## 152. Graph Event versus Physical Transition

The distinction remains:

`graph topology change ≠ physical phase transition`.

---

## 153. Learned Graph Boundary

If graph structure is learned, derivative handling must follow the declared graph-learning mechanism.

---

## 154. Energy Conservation Boundary

Static mechanical fitting does not by itself test trajectory energy conservation.

---

## 155. Molecular-Dynamics Energy Drift

Trajectory drift depends on:

- force model;
- integrator;
- timestep;
- thermostat/barostat state;
- numerical precision.

This belongs to Volume 05 validation.

---

## 156. Static Conservativity

The mechanical training layer can test:

`F = -grad_R E`

without running molecular dynamics.

---

## 157. Trajectory-Based Mechanical Training

A later model may include rollout losses through an MD integrator.

This is separate from static energy-force-stress fitting.

---

## 158. Multi-Step Mechanical Objective

A rollout objective may compare predicted future configurations, energies, or observables.

---

## 159. Rollout Gradient

Gradient propagation through multiple MD steps creates a different optimization problem from static fitting.

---

## 160. Mechanical Curriculum

Training may proceed in stages.

---

## 161. Energy Pretraining

A first stage may fit energy.

---

## 162. Force Fine Tuning

A later stage may introduce force supervision.

---

## 163. Stress Fine Tuning

Stress supervision may be introduced after force/energy convergence.

---

## 164. Joint Final Training

A final stage may optimize all mechanical targets together.

---

## 165. Stage Semantics

Training stage changes do not alter the physical meaning of outputs.

---

## 166. Mechanical Batch

A batch may contain configurations with different atom counts.

---

## 167. Variable-Size Batch

Graph batching must preserve per-configuration identity.

---

## 168. Per-Configuration Reduction

Energy loss may average once per configuration.

---

## 169. Per-Atom Reduction

Force loss may average over atoms.

---

## 170. Per-Component Reduction

Force and stress may average over components.

---

## 171. Reduction Choice

Reduction semantics directly affect effective sample weighting.

---

## 172. Distributed Mechanical Training

Mechanical training may be distributed across multiple devices or processes.

---

## 173. Global Force Count

Distributed force-loss reduction must use the declared global atom/component denominator.

---

## 174. Unequal Batch Sizes

Equal averaging across devices is not equivalent to global sample averaging when device batch sizes differ.

---

## 175. Gradient Synchronization

Distributed parameter gradients must be reduced according to the optimizer contract.

---

## 176. Deterministic Reduction

Exact replay may require deterministic cross-device reduction ordering.

---

## 177. Mixed Precision

Mechanical training may use mixed numerical precision.

---

## 178. Energy Precision

Energy forward evaluation may use one precision.

---

## 179. Force Gradient Precision

Coordinate gradients may require higher precision in sensitive regimes.

---

## 180. Stress Gradient Precision

Cell derivatives may likewise require explicit precision control.

---

## 181. Loss Accumulation Precision

Mechanical losses may be accumulated in higher precision than model activations.

---

## 182. Gradient Scaling

Mixed-precision training may use loss scaling.

This affects numerical optimization, not physical unit semantics.

---

## 183. Gradient Clipping

Parameter-gradient clipping acts on:

`grad_Theta L`.

It does not clip mechanical force.

---

## 184. Force Clipping Boundary

Clipping predicted force changes the mechanical output and therefore changes the model.

It is separate from gradient clipping.

---

## 185. Non-Finite Mechanical Output

NaN or infinite:

- energy;
- force;
- stress

is invalid numerical state.

---

## 186. Non-Finite Mechanical Loss

A non-finite mechanical loss requires explicit handling.

---

## 187. Invalid Batch Policy

A training protocol may:

- reject the batch;
- reject invalid samples;
- abort;
- apply another explicit policy.

---

## 188. Silent Replacement Prohibition

Invalid mechanical values must not be silently replaced with:

`0`

as though they were valid physical outputs or ternary neutral states.

---

## 189. Mechanical Training Determinism

For deterministic training, identical:

- batch;
- model state;
- parameters;
- random state;
- graph;
- arithmetic;
- derivative path

must reproduce the declared mechanical losses and updates.

---

## 190. Conservative Replay

Energy-derived force replay must reproduce both:

`E`

and:

`F = -grad_R E`

under the declared numerical contract.

---

## 191. Stress Replay

Energy-derived stress must also reproduce under the declared cell/strain derivative convention.

---

## 192. Mechanical Checkpoint

A restart-complete training checkpoint may contain:

- model parameters;
- optimizer state;
- scheduler state;
- random state;
- normalization state;
- training step.

---

## 193. Energy Metrics

Reporting may include:

- MAE;
- RMSE;
- per-atom MAE;
- maximum error.

---

## 194. Force Metrics

Reporting may include:

- component MAE;
- vector MAE;
- RMSE;
- maximum vector error;
- angular error.

---

## 195. Stress Metrics

Reporting may include:

- component MAE;
- tensor norm error;
- pressure error;
- stress invariant error.

---

## 196. Conservative Consistency Metric

A model may report:

`epsilon_EF = ||F_direct + grad_R E||`.

---

## 197. Net-Force Metric

A model may report:

`||sum_i F_i||`.

---

## 198. Torque Metric

A model may report total internal torque residual.

---

## 199. Equivariance Metric

A mechanical model may report transformed-output residuals for:

- energy;
- force;
- stress.

---

## 200. Mechanical Metric versus Loss

A reported mechanical metric need not be identical to the training objective.

---

## 201. Validation Split

Mechanical validation uses:

`D_val`.

No parameter update occurs.

---

## 202. Test Split

Mechanical test evaluation uses:

`D_test`

under the declared protocol.

---

## 203. Energy Validation Domain

Validation should cover the energy range relevant to the declared model domain.

---

## 204. Force Validation Domain

Validation should include both low- and high-force regions relevant to the declared model.

---

## 205. Stress Validation Domain

Validation should include relevant cell and mechanical states.

---

## 206. Structural Coverage

Mechanical validation may be stratified by:

- coordination;
- structure;
- defect class;
- composition;
- phase label where independently defined.

---

## 207. Thermodynamic Coverage

Metrics may be stratified by:

- temperature;
- pressure;
- density;
- composition.

---

## 208. Ternary-Mode Stratification

When mechanics are ternary-conditioned, metrics should be separable by:

`-1`

`0`

`1`.

---

## 209. Neutral-Mode Mechanical Metrics

The active-neutral mode should be evaluated explicitly rather than merged with missing data.

---

## 210. Resonance-Stratified Mechanical Metrics

Mechanical error may be stratified by resonance region or coordinate range.

---

## 211. Out-of-Domain Mechanical State

Out-of-domain mechanical predictions remain a separate domain-detection problem.

They are developed in Chapter 08.

---

## 212. Mechanical Uncertainty

A model may attach uncertainty to:

- energy;
- force;
- stress.

---

## 213. Calibration of Mechanical Uncertainty

Uncertainty calibration remains separate from mean prediction fitting unless jointly optimized.

---

## 214. Active Learning Interface

Mechanical uncertainty or error indicators may drive selection of new configurations for reference calculation.

---

## 215. High-Force Acquisition

Active learning may prioritize high-force or low-confidence states.

---

## 216. Stress-Space Acquisition

Cell or strain states may be selected to improve stress coverage.

---

## 217. Resonance-Conditioned Acquisition

A model may prioritize underrepresented resonance regions.

---

## 218. Ternary-Conditioned Acquisition

A model may prioritize underrepresented ternary states or transition neighborhoods.

---

## 219. Mechanical Provenance

Mechanical training artifacts retain canonical provenance classes.

---

## 220. Primary-Source Mechanical Data

External reference:

- energies;
- forces;
- stresses

carry:

`PRIMARY_SOURCE`

where applicable.

---

## 221. Derived Mechanical Target

A force derived numerically from an energy surface may carry:

`DERIVED`.

---

## 222. Calibrated Mechanical Target

A mechanically adjusted or aligned target may carry:

`CALIBRATED`.

---

## 223. Benchmark Mechanical Result

Measured validation and runtime results may carry:

`BENCHMARK`.

---

## 224. Mechanical Test Fixture

Controlled configurations with analytic or deterministic expected derivatives may carry:

`TEST_FIXTURE`.

---

## 225. Author-Defined Mechanical Coupling

TR-EIF-specific resonance/ternary conditioning of energy or force may carry:

`AUTHOR_DEFINED`.

---

## 226. Energy-Training Extension Rule

Any energy-training setup must define:

1. target energy;
2. units;
3. total/per-atom semantics;
4. reference zero;
5. normalization;
6. reduction;
7. weight;
8. provenance.

---

## 227. Force-Training Extension Rule

Any force-training setup must define:

1. conservative or direct force path;
2. atom/component reduction;
3. units;
4. normalization;
5. weight;
6. derivative semantics;
7. provenance.

---

## 228. Stress-Training Extension Rule

Any stress-training setup must define:

1. tensor type;
2. sign convention;
3. units;
4. component ordering;
5. cell/strain derivative relation;
6. normalization;
7. weight.

---

## 229. Mechanical Multi-Task Extension Rule

Any joint E/F/Sigma objective must define:

1. target availability;
2. normalization scales;
3. weights;
4. reduction axes;
5. derivative paths;
6. validation metrics.

---

## 230. Conservative-Consistency Extension Rule

Any consistency term between direct and energy-derived outputs must define:

1. compared outputs;
2. norm;
3. weight;
4. derivative path;
5. validation threshold.

---

## 231. Ternary-Conditioned Mechanical Extension Rule

Any ternary-conditioned mechanical model must define:

1. source ternary channel;
2. target or executed state;
3. energy/force/stress behavior for `-1`;
4. behavior for `0`;
5. behavior for `1`;
6. switching order;
7. derivative semantics;
8. continuity conditions where present.

---

## 232. Resonance-Conditioned Mechanical Extension Rule

Any resonance-conditioned mechanical model must define:

1. source resonance state;
2. transformation law;
3. energy or direct-force coupling;
4. gradient path;
5. units;
6. scale;
7. feedback.

---

## 233. Canonical Mechanical Training Invariants

Every conforming mechanical training setup preserves:

1. energy as scalar;

2. force as vector;

3. stress as tensor;

4. explicit physical units;

5. explicit target availability;

6. explicit loss reduction;

7. explicit derivative path;

8. explicit symmetry contract;

9. explicit provenance.

---

## 234. Canonical Conservative Invariant

For energy-derived force:

`F = -grad_R E`.

Training changes model parameters.

It does not change this relation.

---

## 235. Canonical Stress Invariant

For energy-derived stress, the selected cell/strain derivative convention remains fixed through:

- training;
- validation;
- inference.

---

## 236. Canonical Symmetry Invariants

Mechanical training preserves:

`energy → invariant`

`force → equivariant`

`stress → tensor transformed`.

---

## 237. Canonical Ternary Mechanical Invariants

If mechanics are execution-conditioned:

`-1/0/1`

remains exact.

The state:

`0`

remains active neutral.

---

## 238. Canonical Opposite Mechanical Route

Executed-state-conditioned mechanics preserve:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 239. Canonical State Separation

The mechanical training layer preserves:

`energy ≠ loss`

`force ≠ parameter gradient`

`stress ≠ generic tensor`

`zero force ≠ active neutral`

`zero stress ≠ active neutral`

`target mask ≠ ternary state`

`resonance state ≠ force`.

---

## 240. Canonical Scientific Distinctions

The mechanical training layer preserves:

`equivariance ≠ conservativity`

`force fitting ≠ trajectory integration`

`static conservativity ≠ numerical energy conservation`

`graph topology change ≠ physical phase transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`.

---

## 241. Canonical Mechanical Training Chain

The conservative training chain is:

`configuration`

`→ invariant energy`

`→ coordinate/cell derivatives`

`→ force/stress`

`→ reference comparison`

`→ mechanical loss`

`→ parameter update`.

---

## 242. Canonical Direct-Force Chain

A direct-force training chain is:

`configuration`

`→ equivariant force head`

`→ force loss`

`→ parameter update`.

Conservativity requires a separate condition.

---

## 243. Canonical Hybrid Chain

A hybrid model may use:

`energy head`

`+ direct force/stress heads`

`→ data losses`

`+ consistency losses`

`→ joint optimization`.

---

## 244. Interface to Chapter 05

Chapter 05 develops Ternary Regularization.

It defines losses and constraints for:

- ternary occupancy;
- active-neutral behavior;
- target stability;
- transition semantics;
- routing consistency.

---

## 245. Interface to Chapter 06

Chapter 06 develops Resonance Regularization.

It defines resonance-space constraints that may influence mechanical outputs through resonance-conditioned energy and force.

---

## 246. Interface to Chapter 07

Chapter 07 develops Equivariance Constraints.

It formalizes transformation residuals for energy, force, stress, resonance, and intermediate representations.

---

## 247. Interface to Chapter 08

Chapter 08 develops Uncertainty and Domain Detection.

It defines uncertainty-aware mechanical fitting and out-of-domain mechanical-state handling.

---

## 248. Interface to Chapter 09

Chapter 09 develops Optimization.

It defines the parameter-update algorithms that consume:

`L_mech`

and its gradients.

---

## 249. Final Formal Structure

The mechanical training layer may be represented as:

`MTR = (E_ref, F_ref, Sigma_ref, E_pred, F_pred, Sigma_pred, L_E, L_F, L_S, L_cons, W, M, D)`.

Here:

- `E_ref` is reference energy;
- `F_ref` is reference force;
- `Sigma_ref` is reference stress;
- `E_pred` is predicted energy;
- `F_pred` is predicted force;
- `Sigma_pred` is predicted stress;
- `L_E` is energy loss;
- `L_F` is force loss;
- `L_S` is stress loss;
- `L_cons` is optional conservative/direct consistency loss;
- `W` is mechanical loss weighting;
- `M` is target availability state;
- `D` is the derivative and numerical contract.

A canonical objective is:

`L_mech = w_E L_E + w_F L_F + w_S L_S + w_cons L_cons`.

---

## 250. Final Statement

Energy-force-stress training provides the mechanical supervision layer for TR-EIP.

Energy remains a scalar physical quantity.

Force remains a per-atom polar vector.

Stress remains a mechanical tensor.

For conservative models:

`F = -grad_R E`.

The force relation is part of the architecture, not a learned semantic convention.

Energy-derived stress follows the explicitly declared cell or strain derivative relation.

Mechanical training may combine:

- energy values;
- force vectors;
- stress tensors;
- conservative consistency;
- symmetry constraints;
- resonance conditioning;
- ternary conditioning.

The framework preserves:

`energy ≠ training loss`

`force ≠ parameter gradient`

`stress ≠ generic tensor`

`equivariance ≠ conservativity`

`zero force ≠ active-neutral 0`

`zero stress ≠ active-neutral 0`

`mask 0 ≠ ternary 0`.

When mechanics are conditioned on executed ternary state, the exact kernel remains:

`-1/0/1`.

The active-neutral state:

`0`

remains a real intermediate mechanical mode where defined.

Opposite-polarity mechanical mode changes therefore remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

These definitions establish the mechanical training layer required for Ternary Regularization developed in Chapter 05.
