# Uncertainty and Domain Detection

## 1. Purpose

This chapter defines uncertainty representation, uncertainty calibration, model-domain detection, selective prediction, and acquisition interfaces for the TR-EIF learning and optimization layer.

The chapter preserves explicit separation among:

- prediction;
- realized error;
- epistemic uncertainty;
- aleatoric uncertainty;
- model-domain state;
- resonance classification;
- ternary state;
- numerical validity;
- rejection or abstention state.

Uncertainty and domain detection are auxiliary model layers.

They do not redefine the physical, resonance, ternary, or mechanical state spaces.

---

## 2. Dependencies

This chapter depends on:

- Volume 01 — Mathematical Foundations;
- Volume 02 — Ternary Resonance Theory;
- Volume 03 — Equivariant Interatomic Framework;
- Volume 04 Chapter 01 — Model Architecture;
- Volume 04 Chapter 02 — Training Data;
- Volume 04 Chapter 03 — Loss Functionals;
- Volume 04 Chapter 04 — Energy-Force-Stress Training;
- Volume 04 Chapter 05 — Ternary Regularization;
- Volume 04 Chapter 06 — Resonance Regularization;
- Volume 04 Chapter 07 — Equivariance Constraints.

---

## 3. Uncertainty State

Let:

`U`

denote the uncertainty state space.

An uncertainty state may be written:

`u ∈ U`.

Its representation must specify:

- quantity being assessed;
- mathematical type;
- scale;
- units or dimensionless status;
- calibration convention;
- aggregation convention;
- provenance.

---

## 4. Prediction and Uncertainty

For model output:

`y_hat`

an associated uncertainty estimate may be:

`u_y`.

The pair:

`(y_hat, u_y)`

contains two distinct quantities.

The framework preserves:

`prediction ≠ uncertainty`.

---

## 5. Uncertainty and Realized Error

For reference value:

`y`

the realized error may be:

`e_y = D(y_hat, y)`.

The framework preserves:

`u_y ≠ e_y`.

Uncertainty is estimated before or independently of observing the realized reference error.

---

## 6. Confidence and Accuracy

A model may expose a confidence score:

`c_y`.

The framework preserves:

`confidence ≠ accuracy`.

A high confidence score does not define a correct prediction.

A low confidence score does not define an incorrect prediction.

---

## 7. Calibration and Accuracy

Calibration concerns agreement between declared predictive confidence or probability and observed frequencies or errors under a calibration protocol.

The framework preserves:

`calibration ≠ accuracy`.

---

## 8. Epistemic Uncertainty

Let:

`u_epi`

denote epistemic uncertainty.

It represents uncertainty associated with model knowledge, parameter determination, representation coverage, or finite training support under the declared uncertainty model.

---

## 9. Aleatoric Uncertainty

Let:

`u_ale`

denote aleatoric uncertainty.

It represents uncertainty associated with conditional variability or noise represented by the predictive model.

---

## 10. Total Uncertainty

Where the model defines a composition rule, total uncertainty may be represented as:

`u_total = C_U(u_epi, u_ale)`.

The composition operator:

`C_U`

must be explicitly defined.

---

## 11. Epistemic and Aleatoric Separation

The framework preserves:

`epistemic uncertainty ≠ aleatoric uncertainty`.

Their decomposition is model-dependent.

---

## 12. Uncertainty Method Families

A TR-EIF implementation may estimate uncertainty using explicitly declared methods such as:

- predictive distributions;
- ensembles;
- posterior approximations;
- latent-space distances;
- density estimators;
- residual models;
- conformal procedures;
- calibrated scores;
- combinations of these mechanisms.

No method is implied by the uncertainty interface itself.

---

## 13. Ensemble Uncertainty

For an ensemble of:

`M`

predictions:

`y_hat^(1), ..., y_hat^(M)`

a dispersion statistic may define an epistemic uncertainty proxy.

The ensemble construction must specify:

- number of members;
- parameter initialization;
- training-data sampling;
- architecture identity or variation;
- aggregation rule.

---

## 14. Predictive Distribution

A probabilistic model may define:

`p(y | X)`.

Uncertainty may then be derived from declared distributional quantities such as:

- variance;
- covariance;
- entropy;
- credible interval;
- predictive interval.

---

## 15. Distance-Based Uncertainty

A model may define an uncertainty score from distance in a representation space:

`d_U(z, Z_ref)`.

The representation:

`z`

and reference set:

`Z_ref`

must be specified.

---

## 16. Distance Is Not Uncertainty by Identity

The framework preserves:

`representation distance ≠ uncertainty`

unless an explicit mapping defines uncertainty from that distance.

---

## 17. Density-Based Uncertainty

A density or support estimate:

`p_Z(z)`

may contribute to a domain or uncertainty score.

Low density is not automatically equivalent to:

`OUT_OF_DOMAIN`.

The decision mapping must be explicit.

---

## 18. Model Domain

Let:

`D_M`

denote the declared model domain.

The model domain specifies the set or region of inputs, representations, or task conditions for which the model is designated as in-domain under the declared domain detector.

---

## 19. Domain State Space

A basic domain state space may be:

`D = {IN_DOMAIN, OUT_OF_DOMAIN}`.

A model may additionally define:

`DOMAIN_BOUNDARY`

or another explicit intermediate state.

---

## 20. Domain Boundary

If a domain boundary is defined:

`∂D_M`

denotes the boundary under the declared domain representation.

---

## 21. Domain Score

A scalar domain score may be written:

`s_D(X)`.

A thresholded classifier may use:

`s_D(X)`

to assign a domain state.

---

## 22. Domain Threshold

Let:

`tau_D`

denote a domain decision threshold where a scalar threshold rule is used.

Its provenance must be explicit.

---

## 23. Domain Score Is Not Domain State

The framework preserves:

`s_D ≠ domain class`.

The class is obtained through a declared decision rule.

---

## 24. Out-of-Domain State

`OUT_OF_DOMAIN`

is a model-domain classification.

It is not a physical state.

It is not a resonance class.

It is not a ternary state.

---

## 25. In-Domain State

`IN_DOMAIN`

indicates conformity with the declared model-domain criterion.

It does not establish correctness of a prediction.

---

## 26. In-Domain Is Not Accurate

The framework preserves:

`IN_DOMAIN ≠ accurate prediction`.

---

## 27. Out-of-Domain Is Not Incorrect

The framework preserves:

`OUT_OF_DOMAIN ≠ incorrect prediction`.

---

## 28. Domain Status and Uncertainty

The framework preserves:

`domain state ≠ uncertainty`.

An in-domain sample may carry high uncertainty.

An out-of-domain sample may receive a low numerical uncertainty score if the uncertainty estimator is not calibrated for that region.

---

## 29. Domain Status and Validity

The framework preserves:

`domain status ≠ data validity`.

A numerically valid sample may be out-of-domain.

An invalid sample must be handled by the validity layer rather than reclassified as an ordinary OOD sample.

---

## 30. Validity State

A validity channel may define states such as:

`VALID`

and:

`INVALID`.

This channel remains separate from:

- uncertainty;
- domain state;
- resonance class;
- ternary state.

---

## 31. Missing Data

Missing data require an explicit missingness representation.

The framework preserves:

`MISSING ≠ ternary 0`.

---

## 32. Mask

A mask indicates whether a field participates in a declared computation or loss.

The framework preserves:

`MASK ≠ ternary 0`.

---

## 33. Padding

Padding used for batched representations is not a physical or ternary state.

The framework preserves:

`PADDING ≠ ternary 0`.

---

## 34. Unknown

An unknown value must not be encoded as active neutral.

The framework preserves:

`UNKNOWN ≠ ternary 0`.

---

## 35. NaN

A non-finite numerical value:

`NaN`

is a numerical validity state.

The framework preserves:

`NaN ≠ ternary 0`.

---

## 36. Uncertain

An uncertainty flag or state is not active neutral.

The framework preserves:

`UNCERTAIN ≠ ternary 0`.

---

## 37. Abstention

If selective prediction uses:

`ABSTAIN`

then abstention is represented separately from semantic prediction.

The framework preserves:

`ABSTAIN ≠ ternary 0`.

---

## 38. Rejection

A rejected prediction is a decision-layer state.

The framework preserves:

`REJECTED ≠ ternary 0`.

---

## 39. Resonance State Space

The resonance state remains:

`r ∈ X_R`.

A resonance window remains:

`W_R ⊂ X_R`.

Its boundary remains:

`∂W_R`.

---

## 40. Resonance Classification

A resonance classifier may produce:

`OUTSIDE`

`BOUNDARY`

or:

`INSIDE`.

These classes remain separate from model-domain states.

---

## 41. OOD Is Not Resonance OUTSIDE

The framework preserves:

`OUT_OF_DOMAIN ≠ OUTSIDE resonance window`.

---

## 42. Domain Boundary Is Not Resonance Boundary

The framework preserves:

`∂D_M ≠ ∂W_R`.

---

## 43. Domain Boundary Is Not Resonance BOUNDARY

The framework preserves:

`DOMAIN_BOUNDARY ≠ BOUNDARY resonance class`.

---

## 44. OOD Is Not Ternary Neutral

The framework preserves:

`OUT_OF_DOMAIN ≠ 0`.

---

## 45. Resonance BOUNDARY Is Not Ternary Neutral

The framework preserves:

`BOUNDARY resonance class ≠ 0`.

---

## 46. Uncertainty Is Not Resonance Boundary

The framework preserves:

`uncertainty ≠ resonance BOUNDARY`.

---

## 47. Domain State Is Not Resonance Classification

The framework preserves:

`domain class ≠ resonance class`.

---

## 48. Resonance Uncertainty

A resonance prediction may carry uncertainty:

`u_R`.

This quantity remains separate from:

- `r`;
- resonance class;
- model-domain state.

---

## 49. Energy Uncertainty

For predicted energy:

`E_hat`

an associated uncertainty estimate may be:

`u_E`.

---

## 50. Force Uncertainty

For predicted force:

`F_hat_i`

an associated uncertainty estimate may be:

`u_F,i`.

---

## 51. Stress Uncertainty

For predicted stress:

`Sigma_hat`

an associated uncertainty estimate may be:

`u_S`.

---

## 52. Ternary-Target Uncertainty

For ternary target prediction:

`t_target`

an associated uncertainty representation may be:

`u_T`.

The uncertainty channel must not replace the semantic target.

---

## 53. Ternary Probability and Uncertainty

A ternary probability vector:

`p_T = (p_-, p_0, p_1)`

may contribute to an uncertainty measure.

The framework preserves:

`p_T ≠ t_target`

and:

`uncertainty(p_T) ≠ ternary state`.

---

## 54. Ternary Semantic Kernel

The exact semantic ternary state space remains:

`T = {-1,0,1}`.

---

## 55. Active Neutral

The state:

`0`

remains active neutral.

Its meaning is not replaced by low confidence, uncertainty, rejection, missingness, or domain status.

---

## 56. Target versus Executed State

The framework preserves:

`t_target ≠ t_exec`.

---

## 57. Pending State

Where the ternary execution layer uses pending routing:

`t_pending`

remains a separate routing state.

---

## 58. Pending Is Not Uncertainty

The framework preserves:

`t_pending ≠ uncertainty`.

---

## 59. Pending Is Not OOD

The framework preserves:

`t_pending ≠ OUT_OF_DOMAIN`.

---

## 60. Uncertainty Does Not Alter Transition Topology

Uncertainty-aware target formation may influence whether a target is issued or accepted.

It does not redefine the committed ternary transition graph.

---

## 61. Direct Opposite Transitions

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 62. Neutral-Mediated Routes

The required opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each leg remains a separate committed event.

---

## 63. Rejection versus Neutral Routing

A rejected or abstained prediction does not constitute:

`-1 → 0`

or:

`1 → 0`

unless the execution layer explicitly commits the active-neutral state through its normal transition semantics.

---

## 64. Selective Prediction

A selective prediction system may define an acceptance function:

`A(X) ∈ {ACCEPT, REJECT}`.

---

## 65. Acceptance Score

A scalar acceptance score may be:

`s_A(X)`.

---

## 66. Acceptance Threshold

A threshold:

`tau_A`

may define the acceptance region.

---

## 67. Acceptance Is Not Domain Status

The framework preserves:

`ACCEPT/REJECT ≠ IN_DOMAIN/OUT_OF_DOMAIN`.

A policy may use domain state as one input to the acceptance rule.

---

## 68. Acceptance Is Not Uncertainty

The framework preserves:

`acceptance decision ≠ uncertainty estimate`.

---

## 69. Selective Risk

For accepted predictions, selective risk may be defined over the accepted subset.

The exact metric must specify:

- task loss;
- acceptance rule;
- normalization;
- evaluation set.

---

## 70. Coverage

Coverage may be defined as the fraction of evaluated samples accepted by the selective prediction policy.

---

## 71. Risk-Coverage Relation

A risk-coverage curve evaluates prediction error as a function of retained coverage under a declared ordering or threshold rule.

---

## 72. Coverage Is Not Accuracy

The framework preserves:

`coverage ≠ accuracy`.

---

## 73. Calibration

For probabilistic or confidence-based outputs, calibration requires a declared relationship between predicted confidence and observed outcomes.

---

## 74. Calibration Dataset

Calibration must identify the dataset or split used to determine calibration parameters.

---

## 75. Calibration Parameter

Let:

`Theta_CAL`

denote trainable or fitted calibration parameters where applicable.

---

## 76. Calibration Provenance

Calibration parameters produced by a documented calibration procedure carry:

`CALIBRATED`.

---

## 77. Calibration Metric

A calibration protocol may use explicitly defined metrics such as:

- calibration error;
- negative log-likelihood;
- Brier-type score;
- interval coverage;
- coverage deviation.

---

## 78. Metric Declaration

Each calibration metric must specify:

- target;
- predicted quantity;
- binning or integration rule where applicable;
- aggregation;
- normalization.

---

## 79. Calibration and Sharpness

Calibration and sharpness are separate properties of a predictive distribution.

---

## 80. Calibration and Domain Detection

A calibrated in-domain uncertainty model does not automatically define calibrated uncertainty for out-of-domain samples.

---

## 81. Local Domain Detection

A per-entity or local-environment domain state may be written:

`D_i`.

---

## 82. Global Domain Detection

A global system-level domain state may be written:

`D_global`.

---

## 83. Local and Global Domain States

The framework preserves:

`D_i ≠ D_global`

by identity.

A mapping between local and global domain state must be explicit.

---

## 84. Multiscale Domain Detection

A model may define:

`D^(ell)`

at multiple scales:

`ell`.

---

## 85. Scale-Specific Domain Criteria

Each scale may use a different:

- representation;
- support set;
- threshold;
- aggregation;
- task definition.

---

## 86. Cross-Scale Domain Mapping

Let:

`P_D^(ell→m)`

map domain evidence between scales.

This mapping must be explicitly defined if used.

---

## 87. Local OOD versus Global OOD

A system may contain local out-of-domain environments while the global sample satisfies a different system-level criterion.

No automatic equivalence is imposed.

---

## 88. Task-Specific Domain State

A model may define separate domain states for:

- energy prediction;
- force prediction;
- stress prediction;
- resonance classification;
- ternary target prediction.

---

## 89. Domain State Is Task-Relative

A sample may be in-domain for one task and out-of-domain for another.

---

## 90. Energy Domain

Let:

`D_E`

denote the domain classification associated with energy prediction.

---

## 91. Force Domain

Let:

`D_F`

denote the domain classification associated with force prediction.

---

## 92. Stress Domain

Let:

`D_S`

denote the domain classification associated with stress prediction.

---

## 93. Resonance Domain

Let:

`D_R`

denote the model-domain classification associated with the resonance prediction task.

This symbol must not be confused with resonance class itself.

---

## 94. Ternary Domain

Let:

`D_T`

denote the model-domain classification associated with ternary target prediction.

---

## 95. Representation-Based Domain Detection

A domain detector may act on latent representation:

`z`.

A distance-based criterion may be:

`s_D = f_D(d(z, Z_ref))`.

---

## 96. Density-Based Domain Detection

A detector may use a density estimate:

`p(z)`.

The classification rule must define how density maps to domain state.

---

## 97. Ensemble-Based Domain Detection

A detector may use disagreement among ensemble members as one domain indicator.

---

## 98. Probabilistic Domain Detection

A probabilistic detector may estimate:

`p(D | X)`.

Its probability output remains distinct from hard domain class.

---

## 99. Composite Domain Detector

A detector may combine multiple indicators:

`s_D = C_D(s_1, ..., s_K)`.

The composition:

`C_D`

must be defined.

---

## 100. Threshold Selection

Thresholds used for domain decisions may be:

- author-defined;
- derived;
- calibrated;
- benchmark-specific.

Their provenance must be explicit.

---

## 101. Threshold Is Not Universal

A domain threshold is specific to:

- representation;
- task;
- dataset;
- detector;
- calibration protocol;
- version.

---

## 102. Symmetry of Domain Scores

A scalar global domain score should satisfy:

`s_D(gX) = s_D(X)`

for admissible symmetry transformations when the domain criterion itself is symmetry invariant.

---

## 103. Per-Entity Domain Scores

Per-entity domain scores must permute with the corresponding entities.

---

## 104. Scalar Uncertainty Symmetry

A scalar uncertainty quantity should remain invariant under admissible rigid spatial transformations.

---

## 105. Per-Entity Scalar Uncertainty

Per-entity scalar uncertainty must permute with entity indexing.

---

## 106. Vector Uncertainty

If an uncertainty quantity is vector-valued, its transformation law must be explicitly declared.

---

## 107. Tensor Uncertainty

A covariance tensor or tensor uncertainty representation transforms according to its declared tensor law.

---

## 108. Symmetry Residual Is Not Uncertainty

The framework preserves:

`equivariance residual ≠ predictive uncertainty`.

---

## 109. Symmetry Failure Is Not OOD

The framework preserves:

`equivariance failure ≠ OUT_OF_DOMAIN`.

---

## 110. OOD Is Not Symmetry Failure

The converse also remains:

`OUT_OF_DOMAIN ≠ equivariance failure`.

---

## 111. External Fields

If model inputs include external vectors or tensors, uncertainty and domain detection must use the same declared transformation contract as the predictive model.

---

## 112. Reduced Symmetry

A fixed external field may reduce the admissible symmetry group.

Domain and uncertainty invariance tests must use the same reduced group.

---

## 113. Periodic Systems

For periodic systems, domain detection must be invariant to equivalent periodic-image representations under the declared cell convention.

---

## 114. Numerical Precision

Uncertainty and domain scores may depend on:

- floating-point precision;
- mixed precision;
- fixed-point arithmetic;
- quantization.

---

## 115. Numerical Sensitivity

A domain score near:

`tau_D`

may change classification under numerical perturbation.

---

## 116. Threshold Sensitivity Test

A validation may perturb arithmetic representation and record:

- score deviation;
- domain-class changes;
- acceptance changes.

---

## 117. Numerical Instability Is Not OOD

The framework preserves:

`numerical instability ≠ OUT_OF_DOMAIN`.

---

## 118. Quantization Error Is Not Uncertainty

The framework preserves:

`quantization error ≠ predictive uncertainty`.

A model may explicitly include quantization effects in an uncertainty model, but the quantities remain separately identified.

---

## 119. Active Learning

Uncertainty and domain detection may provide acquisition signals for active learning.

---

## 120. Candidate Pool

Let:

`P_candidate`

denote a candidate configuration pool.

---

## 121. Acquisition Score

An acquisition score may be:

`a(X)`.

---

## 122. Acquisition Inputs

The acquisition score may depend on:

- epistemic uncertainty;
- domain score;
- representation novelty;
- resonance coverage;
- ternary-transition coverage;
- structural diversity;
- task-specific residual proxies.

---

## 123. Acquisition Rule

A selection operator:

`A_acq`

maps candidate scores and constraints to selected configurations.

---

## 124. Acquisition Is Not Physical Dynamics

The framework preserves:

`active-learning acquisition ≠ physical evolution`.

---

## 125. Acquisition Is Not Ternary Execution

The framework preserves:

`acquisition decision ≠ ternary-state transition`.

---

## 126. Diversity Constraint

An active-learning selector may include a diversity criterion in configuration or representation space.

---

## 127. Resonance Coverage Acquisition

Candidate selection may target sparsely represented regions of:

`X_R`

or specific resonance-window relations.

---

## 128. Ternary Coverage Acquisition

Candidate selection may target underrepresented:

- ternary states;
- transition legs;
- neutral residence regimes;
- pending-route cases.

---

## 129. Domain-Boundary Acquisition

Candidates near:

`∂D_M`

may be selected when the acquisition protocol explicitly targets model-domain refinement.

---

## 130. Resonance-Boundary Acquisition

Candidates near:

`∂W_R`

may be selected independently.

---

## 131. Domain and Resonance Boundaries Remain Separate

The framework preserves:

`∂D_M ≠ ∂W_R`.

---

## 132. Reference Evaluation

Selected active-learning candidates receive reference values through the declared reference procedure.

---

## 133. Dataset Update

New samples must retain:

- source;
- reference method;
- acquisition reason;
- configuration identity;
- split assignment;
- version identity.

---

## 134. Dataset Split Integrity

Acquired samples must not silently enter held-out test data used for final benchmark evaluation.

---

## 135. Uncertainty Diagnostics

An uncertainty evaluation may report:

- mean uncertainty;
- median uncertainty;
- quantiles;
- calibration metrics;
- interval coverage;
- error-versus-uncertainty relation;
- task-specific uncertainty.

---

## 136. Domain Diagnostics

A domain evaluation may report:

- in-domain count;
- out-of-domain count;
- boundary count where defined;
- domain-score distribution;
- false acceptance;
- false rejection;
- task-specific domain status.

---

## 137. Selective Prediction Diagnostics

A selective prediction evaluation may report:

- coverage;
- selective risk;
- risk-coverage curve;
- acceptance threshold;
- accepted count;
- rejected count.

---

## 138. OOD Detection Metrics

Where labeled in-domain and out-of-domain fixtures exist, evaluation may use explicitly declared discrimination metrics.

The exact metric and positive-class convention must be stated.

---

## 139. Error-Uncertainty Correlation

A diagnostic may compare uncertainty with realized error.

Such correlation is an empirical statistic and does not identify uncertainty with error.

---

## 140. Calibration under Distribution Shift

Calibration must be evaluated separately for each declared evaluation distribution where distribution-specific claims are made.

---

## 141. Uncertainty for Forces

Force uncertainty may be:

- per component;
- per vector norm;
- per atom;
- aggregated globally.

The selected representation must be explicit.

---

## 142. Force Covariance

A probabilistic force model may define covariance:

`C_F,i`.

Its transformation law must follow the force-coordinate representation.

---

## 143. Energy Uncertainty

Energy uncertainty may require system-size normalization when comparing configurations with different numbers of entities.

The normalization convention must be explicit.

---

## 144. Stress Uncertainty

Stress uncertainty must specify:

- tensor components;
- coordinate basis;
- aggregation;
- units.

---

## 145. Resonance Uncertainty Diagnostics

A resonance uncertainty evaluation may include:

- coordinate uncertainty;
- class probability;
- boundary-distance uncertainty;
- window-parameter uncertainty;
- history-state uncertainty.

---

## 146. Ternary Uncertainty Diagnostics

A ternary uncertainty evaluation may include:

- class entropy;
- probability margin;
- ensemble disagreement;
- target stability under perturbation.

These remain uncertainty diagnostics rather than semantic states.

---

## 147. Ternary Confidence Margin

For class probabilities, a margin may be defined from the highest and second-highest class scores.

The margin is not the ternary state itself.

---

## 148. Low Margin Is Not Neutral

The framework preserves:

`low ternary classification margin ≠ 0`.

---

## 149. High Entropy Is Not Neutral

The framework preserves:

`high ternary entropy ≠ 0`.

---

## 150. Domain Score Is Not Neutral

The framework preserves:

`domain score ≠ 0`.

---

## 151. Calibration Parameters Are Not Physical Parameters

The framework preserves:

`calibration parameter ≠ physical material parameter`

unless a separately defined model establishes such a role.

---

## 152. Classifier Temperature

A classifier may use a temperature parameter:

`tau_C`.

---

## 153. Classifier Temperature Is Not Thermodynamic Temperature

The framework preserves:

`classifier temperature ≠ physical temperature`.

---

## 154. Domain Temperature Scaling

If temperature scaling is used for calibration, the parameter remains an optimization/calibration variable.

---

## 155. Provenance Classes

Uncertainty and domain detection use the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 156. Primary-Source Method

An uncertainty or OOD method adopted from an external source uses:

`PRIMARY_SOURCE`

for its sourced definition.

---

## 157. Derived Score

A domain or uncertainty score derived from already defined TR-EIF quantities may use:

`DERIVED`.

---

## 158. Author-Defined Detector

A TR-EIF-specific domain detector, uncertainty mapping, or acceptance rule may use:

`AUTHOR_DEFINED`.

---

## 159. Calibrated Threshold

A threshold selected through a declared calibration procedure uses:

`CALIBRATED`.

---

## 160. Benchmark Result

Measured uncertainty, domain, or selective-prediction metrics under a benchmark protocol use:

`BENCHMARK`.

---

## 161. Test Fixture

Synthetic uncertainty or OOD cases used for verification use:

`TEST_FIXTURE`.

---

## 162. Requires Source

An external uncertainty or domain claim without an established source uses:

`REQUIRES_SOURCE`.

---

## 163. Requires Test

An implementation or empirical claim without validation uses:

`REQUIRES_TEST`.

---

## 164. Uncertainty Extension Rule

Any new uncertainty quantity must define:

1. target prediction;

2. uncertainty type;

3. mathematical representation;

4. units or dimensionless status;

5. estimator;

6. aggregation;

7. symmetry behavior;

8. calibration;

9. provenance;

10. validation.

---

## 165. Domain Detector Extension Rule

Any new domain detector must define:

1. target task;

2. input representation;

3. reference support or training domain;

4. detector score;

5. threshold or decision rule;

6. boundary semantics where used;

7. symmetry behavior;

8. calibration;

9. provenance;

10. validation.

---

## 166. Selective Prediction Extension Rule

Any selective prediction policy must define:

1. prediction;

2. uncertainty or score inputs;

3. acceptance rule;

4. rejection state;

5. threshold;

6. coverage metric;

7. selective-risk metric;

8. calibration;

9. validation.

---

## 167. Active Learning Extension Rule

Any acquisition procedure must define:

1. candidate pool;

2. acquisition score;

3. uncertainty input where used;

4. domain input where used;

5. diversity rule;

6. selection budget;

7. reference procedure;

8. dataset-update rule;

9. provenance;

10. validation.

---

## 168. Multiscale Domain Extension Rule

Any multiscale domain detector must define:

1. scale set;

2. detector at each scale;

3. score at each scale;

4. threshold at each scale;

5. cross-scale mapping;

6. aggregation;

7. task association;

8. validation.

---

## 169. Resonance-Uncertainty Extension Rule

Any resonance uncertainty model must define:

1. resonance coordinate;

2. resonance window where relevant;

3. uncertainty target;

4. estimator;

5. class relation;

6. domain relation;

7. scale;

8. symmetry behavior;

9. calibration;

10. validation.

---

## 170. Ternary-Uncertainty Extension Rule

Any ternary uncertainty model must define:

1. soft prediction representation;

2. semantic target;

3. uncertainty estimator;

4. decision rule;

5. active-neutral separation;

6. pending-state separation;

7. domain-state separation;

8. calibration;

9. validation.

---

## 171. Mechanical-Uncertainty Extension Rule

Any mechanical uncertainty model must define:

1. energy uncertainty where used;

2. force uncertainty where used;

3. stress uncertainty where used;

4. covariance structure where used;

5. units;

6. aggregation;

7. symmetry behavior;

8. calibration;

9. validation.

---

## 172. Canonical Uncertainty Invariants

Every conforming TR-EIF uncertainty layer preserves:

1. uncertainty is distinct from prediction;

2. uncertainty is distinct from realized error;

3. epistemic and aleatoric uncertainty are separately typed where both are used;

4. calibration is distinct from accuracy;

5. uncertainty is distinct from domain state;

6. uncertainty is distinct from resonance class;

7. uncertainty is distinct from ternary state;

8. uncertainty is distinct from numerical validity;

9. symmetry behavior is explicit;

10. provenance is explicit.

---

## 173. Canonical Domain Invariants

Every conforming TR-EIF domain detector preserves:

1. explicit target task;

2. explicit domain representation;

3. explicit detector score;

4. explicit decision rule;

5. explicit threshold provenance;

6. explicit boundary semantics where present;

7. explicit separation from resonance classification;

8. explicit separation from ternary semantics;

9. explicit symmetry behavior;

10. explicit validation.

---

## 174. Canonical Missingness Distinctions

The framework preserves:

`MISSING ≠ 0`

`MASK ≠ 0`

`PADDING ≠ 0`

`UNKNOWN ≠ 0`

`INVALID ≠ 0`

`NaN ≠ 0`

`UNCERTAIN ≠ 0`

`ABSTAIN ≠ 0`.

---

## 175. Canonical Resonance Distinctions

The framework preserves:

`OUTSIDE resonance window ≠ OUT_OF_DOMAIN`

`BOUNDARY resonance class ≠ DOMAIN_BOUNDARY`

`INSIDE resonance window ≠ IN_DOMAIN`

`resonance uncertainty ≠ resonance class`

`resonance boundary ≠ model-domain boundary`.

---

## 176. Canonical Ternary Distinctions

The framework preserves:

`uncertainty ≠ ternary state`

`domain state ≠ ternary state`

`rejection ≠ ternary state`

`t_target ≠ t_exec`

`t_pending ≠ t_exec`

`t_pending ≠ active neutral`.

---

## 177. Canonical Physical Distinctions

The framework preserves:

`uncertainty ≠ energy`

`uncertainty ≠ force`

`domain score ≠ physical energy`

`domain class ≠ physical phase`

`classifier temperature ≠ thermodynamic temperature`.

---

## 178. Canonical Resonance-Theory Distinctions

The framework preserves:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ resonance`

`R(t) ≠ C(t)`.

---

## 179. Canonical Transition Distinctions

The framework preserves:

`resonance-window crossing ≠ bifurcation`

`resonance-window crossing ≠ ternary transition`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 180. Canonical Symmetry Distinctions

The framework preserves:

`symmetry residual ≠ uncertainty`

`symmetry failure ≠ OUT_OF_DOMAIN`

`spatial rotation ≠ ternary polarity reversal`.

---

## 181. Interface to Chapter 09

Chapter 09 defines optimization.

The uncertainty and domain layer supplies:

- uncertainty losses;
- calibration objectives;
- domain-detector objectives;
- selective-prediction metrics;
- active-learning acquisition signals;
- task-specific thresholds;
- uncertainty-aware sampling or weighting variables.

Optimization must preserve all semantic separations established in this chapter.

---

## 182. Interface to Chapter 10

Chapter 10 summarizes the complete Volume 04 learning and optimization layer.

The summary interface includes:

- uncertainty state;
- epistemic and aleatoric decomposition;
- domain state;
- selective prediction;
- calibration;
- active learning;
- mechanical uncertainty;
- resonance uncertainty;
- ternary uncertainty.

---

## 183. Final Formal Structure

The uncertainty and domain layer may be represented as:

`UD = (U, U_EPI, U_ALE, D_M, s_D, C_D, A, C_CAL, A_ACQ, V_UD)`.

Here:

- `U` is the uncertainty state space;
- `U_EPI` is the epistemic uncertainty component where used;
- `U_ALE` is the aleatoric uncertainty component where used;
- `D_M` is the declared model domain;
- `s_D` is the domain score;
- `C_D` is the domain classifier;
- `A` is the selective acceptance operator;
- `C_CAL` is the calibration procedure;
- `A_ACQ` is the active-learning acquisition operator;
- `V_UD` is the validation contract.

A task-specific predictive interface may be written:

`X → (y_hat, u_y, d_y, a_y)`.

Here:

- `y_hat` is the task prediction;
- `u_y` is uncertainty;
- `d_y` is domain state;
- `a_y` is acceptance state.

These outputs remain separately typed.

---

## 184. Final Statement

The TR-EIF uncertainty and domain-detection layer defines separate representations for predictive uncertainty, model-domain state, numerical validity, and selective acceptance.

The framework preserves:

`uncertainty ≠ prediction`

`uncertainty ≠ realized error`

`confidence ≠ accuracy`

`calibration ≠ accuracy`

`domain state ≠ uncertainty`

`OUT_OF_DOMAIN ≠ OUTSIDE resonance window`

`DOMAIN_BOUNDARY ≠ BOUNDARY resonance class`

`OUT_OF_DOMAIN ≠ ternary 0`

`UNCERTAIN ≠ ternary 0`

`ABSTAIN ≠ ternary 0`

`INVALID ≠ ternary 0`

`MISSING ≠ ternary 0`

`MASK ≠ ternary 0`

`PADDING ≠ ternary 0`.

The resonance classes:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

remain distinct from model-domain classes.

The exact ternary semantic kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

The target, pending, and executed ternary states remain separate.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Uncertainty and domain detection may condition target acceptance, calibration, selective prediction, training weights, sampling, and active-learning acquisition.

They do not replace the resonance state space, the ternary state space, the mechanical state variables, or the committed ternary execution rules.
