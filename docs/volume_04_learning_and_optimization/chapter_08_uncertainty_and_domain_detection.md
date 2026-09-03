# Uncertainty and Domain Detection

## 1. Purpose

This chapter defines uncertainty representation, confidence estimation, domain detection, and out-of-domain handling for the TR-EIP learning and optimization layer of TR-EIF.

The uncertainty layer operates across:

- atomic configuration;
- local environment;
- learned representation;
- resonance state;
- ternary target;
- energy;
- force;
- stress;
- multiscale state.

Its purpose is to distinguish model uncertainty and domain validity from the physical and semantic state variables of the framework.

The canonical distinction is:

`uncertainty state ≠ physical state`.

Likewise:

`out-of-domain state ≠ resonance class`

and:

`out-of-domain state ≠ ternary state`.

---

## 2. Uncertainty State

Let:

`u ∈ X_U`.

The uncertainty state space:

`X_U`

is separate from:

- configuration space;
- equivariant representation space;
- resonance space;
- ternary state space;
- energy space;
- force space;
- stress space.

---

## 3. Domain State

Let:

`d ∈ X_D`.

A minimal domain-state set may be:

`X_D = {IN_DOMAIN, NEAR_DOMAIN_BOUNDARY, OUT_OF_DOMAIN}`.

The exact domain-state structure is model-specific.

---

## 4. Domain State Is Metadata

Domain classification describes the relation between a sample and the supported model domain.

It is not a physical observable by identity.

---

## 5. Out-of-Domain State

`OUT_OF_DOMAIN`

means that the input lies outside the declared support or reliability domain under the chosen domain detector.

It does not mean:

- resonance OUTSIDE;
- ternary `0`;
- invalid atomistic configuration;
- high energy;
- unstable material;
- physical phase transition.

---

## 6. Uncertainty versus Error

The framework preserves:

`uncertainty ≠ realized prediction error`.

Uncertainty estimates the expected reliability or spread of predictions.

Realized error requires reference data.

---

## 7. Confidence versus Accuracy

The framework preserves:

`confidence ≠ accuracy`.

A high-confidence prediction may be wrong.

A low-confidence prediction may be correct.

---

## 8. Uncertainty versus Confidence

Confidence and uncertainty may be related through a declared mapping.

They are not necessarily exact complements.

---

## 9. Epistemic Uncertainty

Epistemic uncertainty represents uncertainty associated with limited model knowledge.

Typical sources include:

- insufficient training coverage;
- parameter uncertainty;
- representation uncertainty;
- extrapolation.

---

## 10. Aleatoric Uncertainty

Aleatoric uncertainty represents variability associated with the data-generating or reference process under the declared observation model.

---

## 11. Epistemic versus Aleatoric

The framework preserves:

`epistemic uncertainty ≠ aleatoric uncertainty`.

They may be estimated separately or jointly.

---

## 12. Model Uncertainty

Model uncertainty may include uncertainty in:

- energy;
- force;
- stress;
- resonance coordinate;
- resonance class;
- ternary target;
- multiscale closure.

---

## 13. Data Uncertainty

Data uncertainty may originate from:

- reference-method variability;
- finite numerical convergence;
- measurement noise;
- labeling ambiguity;
- heterogeneous provenance.

---

## 14. Provenance Uncertainty

Uncertainty associated with reference provenance must remain distinguishable from model uncertainty.

---

## 15. Uncertainty Mapping

A model may define:

`P_U: X → X_U`.

For prediction output:

`y`

the uncertainty mapping may be:

`u_y = P_U(x,y)`.

---

## 16. Domain Detector

A domain detector is a mapping:

`P_D: X → X_D`

or:

`P_D: X → R`.

A continuous domain score may later be classified.

---

## 17. Domain Score

Let:

`s_D(x)`

be a continuous domain score.

Its interpretation must be explicitly declared.

---

## 18. Score Direction

A model must define whether larger:

`s_D`

means:

- more in-domain;
- more out-of-domain.

The convention must remain fixed.

---

## 19. Domain Threshold

A threshold:

`tau_D`

may define:

`IN_DOMAIN`

versus:

`OUT_OF_DOMAIN`.

---

## 20. Boundary Band

A second threshold pair may define:

`NEAR_DOMAIN_BOUNDARY`.

For example:

`s_D < tau_in`

`s_D ∈ [tau_in, tau_out]`

`s_D > tau_out`.

The exact orientation depends on the score convention.

---

## 21. Domain Boundary Is Not Resonance Boundary

The distinction remains:

`domain boundary ≠ resonance-window boundary`.

---

## 22. Domain Boundary Is Not Ternary Neutral

The distinction remains:

`domain boundary ≠ ternary 0`.

---

## 23. Domain Boundary Is Not Bifurcation

The distinction remains:

`domain-boundary crossing ≠ bifurcation`.

---

## 24. Domain Boundary Is Not Structural Transition

The distinction remains:

`domain-boundary crossing ≠ structural transition`.

---

## 25. Domain Boundary Is Not Physical Phase Transition

The distinction remains:

`domain-boundary crossing ≠ physical phase transition`.

---

## 26. Configuration Domain

The configuration domain may be defined over:

- composition;
- species;
- atomic number;
- coordinate geometry;
- density;
- cell shape;
- volume;
- temperature;
- pressure;
- strain;
- charge state;
- external fields;
- boundary conditions.

---

## 27. Local Environment Domain

For atom:

`i`

a local domain detector may act on:

`x_i`.

---

## 28. Global Domain

A configuration-level detector may act on a pooled global representation.

---

## 29. Edge Domain

An edge-level detector may identify unsupported pair or relation states.

---

## 30. Multiscale Domain

Different scales may have independent domain-state variables:

`d_edge`

`d_atom`

`d_cluster`

`d_global`.

---

## 31. Cross-Scale Domain Disagreement

A sample may be globally familiar while containing locally unfamiliar environments.

Likewise, local environments may appear familiar while their global arrangement is unfamiliar.

---

## 32. Local Out-of-Domain Detection

Per-atom domain scores may identify isolated unsupported local environments.

---

## 33. Global Out-of-Domain Detection

A global detector may identify unsupported compositions, structures, or thermodynamic regimes.

---

## 34. Domain Aggregation

A global domain status may be generated from local scores through an explicit operator:

`A_D({s_D,i})`.

---

## 35. Maximum-Risk Aggregation

One possible rule uses the most out-of-domain local environment.

---

## 36. Mean-Risk Aggregation

Another rule uses an aggregate statistic over all local environments.

---

## 37. Quantile Aggregation

A robust detector may use a high quantile of local risk.

---

## 38. Aggregation Is Model-Specific

No universal aggregation rule is imposed.

---

## 39. Representation-Space Domain Detection

A detector may operate on learned representation:

`h`.

---

## 40. Distance-Based Detector

A detector may define distance from training representations.

---

## 41. Euclidean Representation Distance

A simple form is:

`d(x) = ||h(x) - h_ref||`.

---

## 42. Mahalanobis-Type Distance

A covariance-aware distance may use:

`d_M(x)^2 = (h-mu)^T Sigma^-1 (h-mu)`.

---

## 43. Covariance Regularization

If:

`Sigma`

is estimated from finite data, numerical regularization may be required.

---

## 44. Distance Is Not Physical Distance

The framework preserves:

`representation distance ≠ atomic geometric distance`.

---

## 45. Density-Based Domain Detection

A model may estimate density:

`p(h)`.

Low density may indicate weak training support.

---

## 46. Density Threshold

A threshold on:

`p(h)`

or:

`log p(h)`

may define a domain boundary.

---

## 47. Density versus Probability of Correctness

The distinction remains:

`representation density ≠ probability that prediction is correct`.

---

## 48. Nearest-Neighbor Domain Detection

A domain score may use distance to nearest training representations.

---

## 49. K-Nearest-Neighbor Domain Detection

A score may aggregate distances to:

`k`

nearest references.

---

## 50. Metric Choice

The domain metric must be explicitly defined.

---

## 51. Feature Scaling

Distance-based detectors require declared feature scaling.

---

## 52. Dimensionality Effect

Distance statistics may change substantially with representation dimension.

---

## 53. Learned Domain Detector

A separate classifier may learn:

`IN_DOMAIN`

versus:

`OUT_OF_DOMAIN`.

---

## 54. Detector Training Data

A learned detector requires positive and negative domain examples or a declared surrogate strategy.

---

## 55. Synthetic Out-of-Domain Data

Synthetic OOD samples may be generated through controlled perturbations.

Their provenance must remain explicit.

---

## 56. Synthetic OOD Is Not Physical OOD by Identity

A synthetic perturbation used for training does not define the entire physical out-of-domain space.

---

## 57. Ensemble Uncertainty

An ensemble contains models:

`M_1, ..., M_K`.

---

## 58. Ensemble Prediction

For scalar output:

`y_bar = mean_k y_k`.

---

## 59. Ensemble Spread

A basic ensemble uncertainty estimate is:

`var_ens(y) = mean_k (y_k - y_bar)^2`.

---

## 60. Force Ensemble Uncertainty

For force vectors, uncertainty may be evaluated per atom and per component or through invariant norms.

---

## 61. Rotation-Compatible Force Uncertainty

A force uncertainty scalar should preferably use rotationally invariant quantities such as:

`||F_k - F_bar||`.

---

## 62. Stress Ensemble Uncertainty

Stress uncertainty may be evaluated through tensor norms or invariant components.

---

## 63. Resonance Ensemble Uncertainty

Ensemble spread may be computed in resonance space.

---

## 64. Ternary Ensemble Uncertainty

For ternary targets, ensemble disagreement may be represented through categorical vote distribution.

---

## 65. Ternary Vote Distribution

Define:

`p_ens(-1)`

`p_ens(0)`

`p_ens(1)`.

---

## 66. Ternary Vote Entropy

Ensemble categorical entropy may measure disagreement.

---

## 67. Ternary Disagreement Is Not Active Neutral

The distinction remains:

`ensemble disagreement ≠ ternary 0`.

---

## 68. Neutral Vote

A model voting:

`0`

predicts active neutral.

It does not abstain.

---

## 69. Abstention

If a system supports abstention, abstention must use a separate output state.

---

## 70. Abstention Is Not Neutral

The framework preserves:

`ABSTAIN ≠ 0`.

---

## 71. Dropout-Based Uncertainty

Stochastic inference may generate multiple predictions using dropout or another stochastic mechanism.

---

## 72. Monte Carlo Estimate

Given repeated stochastic predictions:

`y^(1), ..., y^(K)`

uncertainty may be estimated from the empirical distribution.

---

## 73. Stochastic Sample Count

The number:

`K`

must be reported.

---

## 74. Sampling Noise

The uncertainty estimate itself has finite-sample variability.

---

## 75. Bayesian Parameter Uncertainty

A Bayesian model may represent a distribution over parameters:

`p(Theta | D)`.

---

## 76. Predictive Distribution

The predictive distribution is:

`p(y | x,D)`.

---

## 77. Approximate Bayesian Methods

Approximate inference methods must state their approximation explicitly.

---

## 78. Posterior Approximation Is Not Exact Posterior

The framework preserves:

`approximate posterior ≠ exact posterior`.

---

## 79. Heteroscedastic Regression

A model may predict both:

`mu(x)`

and:

`sigma(x)`.

---

## 80. Positive Uncertainty Scale

A predicted standard deviation must satisfy:

`sigma > 0`.

---

## 81. Positive Parameterization

A positive scale may be enforced using a positive-valued transformation.

---

## 82. Energy Uncertainty

For energy:

`u_E`

may be defined per atom, per configuration, or both.

---

## 83. Force Uncertainty

For each atom:

`u_F,i`

may quantify uncertainty in force prediction.

---

## 84. Stress Uncertainty

A model may predict scalar or tensorial uncertainty for stress.

---

## 85. Scalar Stress Uncertainty

A scalar uncertainty may summarize tensor prediction reliability.

---

## 86. Componentwise Stress Uncertainty

Componentwise uncertainty depends on coordinate frame unless transformed appropriately.

---

## 87. Equivariant Uncertainty

Uncertainty associated with equivariant outputs must obey its declared symmetry behavior.

---

## 88. Scalar Uncertainty Invariance

A scalar uncertainty score should satisfy:

`u(gX) = u(X)`

under declared rigid transformations.

---

## 89. Per-Atom Uncertainty Permutation

Per-atom uncertainty must permute with atom indexing.

---

## 90. Vector Uncertainty Representation

If uncertainty itself is represented as a vector or tensor, its transformation law must be explicit.

---

## 91. Covariance Matrix

For vector output:

`y ∈ R^3`

uncertainty may be represented by covariance:

`C_y`.

---

## 92. Covariance Transformation

Under rotation:

`C_y' = Q C_y Q^T`.

---

## 93. Isotropic Covariance

An isotropic covariance has form:

`C_y = sigma^2 I`.

---

## 94. Anisotropic Covariance

An anisotropic covariance may encode direction-dependent uncertainty.

---

## 95. Positive Semidefinite Covariance

A covariance matrix must remain positive semidefinite.

---

## 96. Covariance Parameterization

A learned covariance may be parameterized structurally to preserve positive semidefiniteness.

---

## 97. Confidence Interval

A probabilistic model may report intervals derived from its predictive distribution.

---

## 98. Confidence Interval versus Coverage

Nominal interval level does not guarantee empirical coverage.

---

## 99. Calibration

Calibration evaluates consistency between predicted confidence or uncertainty and observed outcomes.

---

## 100. Calibration Dataset

Calibration should use data separated from the final test set under a strict evaluation protocol.

---

## 101. Regression Calibration

For continuous outputs, calibration may compare predicted uncertainty with empirical residual distributions.

---

## 102. Classification Calibration

For categorical outputs, calibration compares confidence with observed correctness frequency.

---

## 103. Ternary Calibration

Ternary classifier probabilities may be calibrated separately for:

`-1`

`0`

`1`.

---

## 104. Neutral-Class Calibration

The active-neutral class should have explicit calibration metrics.

---

## 105. Resonance-Class Calibration

Resonance classes:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

may be calibrated separately.

---

## 106. Domain Calibration

A domain score may be calibrated against known in-domain and held-out-domain data.

---

## 107. Calibration Error

A calibration metric measures disagreement between predicted and observed reliability.

---

## 108. Expected Calibration Error

A binned expected calibration error may be used for categorical outputs.

The binning procedure must be explicit.

---

## 109. Reliability Diagram

A reliability diagram may compare predicted confidence against empirical accuracy.

---

## 110. Sharpness

Sharpness describes concentration of predictive distributions.

---

## 111. Sharpness versus Calibration

The distinction remains:

`sharpness ≠ calibration`.

A model may be sharp but miscalibrated.

---

## 112. Accuracy versus Calibration

The distinction remains:

`accuracy ≠ calibration`.

---

## 113. Selective Prediction

A model may choose to report predictions only below or above a declared uncertainty threshold.

---

## 114. Rejection Function

Let:

`A(x) ∈ {ACCEPT, REJECT}`.

---

## 115. Rejection State Separation

`REJECT`

is not a ternary state.

---

## 116. Rejection Threshold

A rejection rule may use:

`u(x) > tau_U`.

---

## 117. Acceptance Region

The accepted prediction region must be declared.

---

## 118. Selective Risk

Selective risk evaluates error only on accepted predictions.

---

## 119. Coverage

Coverage is the fraction of samples accepted.

---

## 120. Risk-Coverage Tradeoff

Reducing accepted coverage may reduce selective error.

The tradeoff must be measured rather than assumed.

---

## 121. Domain-Aware Acceptance

Acceptance may depend jointly on:

- uncertainty;
- domain score;
- numerical validity.

---

## 122. Numerical Validity

A sample with non-finite model outputs must fail numerical validity independently of domain classification.

---

## 123. Invalid versus Out-of-Domain

The distinction remains:

`INVALID ≠ OUT_OF_DOMAIN`.

---

## 124. Invalid versus Uncertain

The distinction remains:

`INVALID ≠ high uncertainty`.

---

## 125. Missing Data

Missing input information must be encoded separately from ternary neutral.

---

## 126. Missing Is Not Neutral

The framework preserves:

`MISSING ≠ 0`.

---

## 127. Mask Is Not Neutral

The framework preserves:

`MASK ≠ 0`.

---

## 128. Padding Is Not Neutral

The framework preserves:

`PADDING ≠ 0`.

---

## 129. Unknown Is Not Neutral

The framework preserves:

`UNKNOWN ≠ 0`.

---

## 130. NaN Is Not Neutral

The framework preserves:

`NaN ≠ 0`.

---

## 131. Uncertain Is Not Neutral

The framework preserves:

`UNCERTAIN ≠ 0`.

---

## 132. Active Neutral

The state:

`0`

remains a valid active ternary state.

It may represent:

- mediation;
- balancing;
- retention;
- transition staging;
- controlled neutralization.

---

## 133. Ternary Target under Uncertainty

A ternary classifier may output:

`t_target ∈ {-1,0,1}`

together with separate uncertainty:

`u_T`.

---

## 134. Ternary Probability

A classifier may produce:

`p_T = (p_-, p_0, p_1)`.

---

## 135. Hard Ternary Target

The hard target may be:

`t_target = argmax p_T`

or another declared decision rule.

---

## 136. Probability Is Not State

The framework preserves:

`p_T ≠ t_target`.

---

## 137. Entropy Is Not State

The framework preserves:

`H(p_T) ≠ ternary state`.

---

## 138. Confidence Is Not State

The framework preserves:

`confidence ≠ ternary state`.

---

## 139. Uncertainty-Gated Ternary Prediction

A model may reject a ternary prediction when uncertainty exceeds a threshold.

The rejected result must not be encoded as:

`0`.

---

## 140. Ternary Target versus Executed State

The distinction remains:

`t_target ≠ t_exec`.

---

## 141. Executed State under Uncertainty

Uncertainty associated with the target does not itself modify committed execution semantics.

---

## 142. Pending State under Uncertainty

A pending destination remains separate from both uncertainty and domain state.

---

## 143. Pending Is Not Uncertainty

The framework preserves:

`pending destination ≠ uncertainty state`.

---

## 144. Direct-Opposite Constraint

No uncertainty estimate may authorize direct committed:

`-1 → 1`

or:

`1 → -1`.

---

## 145. Opposite-Polarity Routes

The canonical routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 146. Uncertain Opposite Request

If an opposite target is uncertain, model policy may:

- retain current target;
- abstain;
- delay request;
- request active neutral.

The exact policy must be explicitly defined.

---

## 147. Uncertainty Policy Is Not Execution Semantics

The uncertainty policy may determine whether a request is issued.

Once committed execution occurs, the execution graph remains unchanged.

---

## 148. Resonance Uncertainty

Let:

`u_R`

represent uncertainty associated with resonance state or resonance classification.

---

## 149. Resonance Coordinate Uncertainty

For continuous resonance coordinate:

`r`

a model may estimate:

`C_R`

or scalar spread.

---

## 150. Resonance-Class Uncertainty

For categorical resonance classification:

`OUTSIDE/BOUNDARY/INSIDE`

a probability distribution may be produced.

---

## 151. Resonance Boundary Uncertainty

Samples close to:

`∂W_R`

may exhibit high classification sensitivity.

---

## 152. Boundary Proximity versus Uncertainty

The distinction remains:

`distance to resonance boundary ≠ uncertainty`.

A model may be certain about a boundary-near sample.

---

## 153. Boundary Distance

A geometric distance:

`d_R,boundary`

may be used as a separate feature.

---

## 154. Resonance OOD

A sample may be out-of-domain for the resonance model even if its computed:

`r`

lies inside:

`W_R`.

---

## 155. Resonance Outside versus OOD

The distinction remains:

`OUTSIDE resonance window ≠ OUT_OF_DOMAIN`.

---

## 156. Resonance Inside versus In-Domain

Likewise:

`INSIDE resonance window ≠ IN_DOMAIN`.

---

## 157. Resonance Uncertainty versus Ternary Neutral

The framework preserves:

`u_R ≠ ternary 0`.

---

## 158. Energy Uncertainty versus Energy

The distinction remains:

`u_E ≠ E`.

---

## 159. Force Uncertainty versus Force

The distinction remains:

`u_F ≠ F`.

---

## 160. Stress Uncertainty versus Stress

The distinction remains:

`u_S ≠ Sigma`.

---

## 161. Uncertainty-Weighted Energy Loss

A training objective may weight energy residuals using estimated uncertainty.

---

## 162. Uncertainty-Weighted Force Loss

Force residuals may likewise be weighted.

---

## 163. Uncertainty-Weighted Stress Loss

Stress residuals may likewise be weighted.

---

## 164. Weight Direction

Whether high-uncertainty samples receive lower or higher weight depends on the training objective.

---

## 165. Noise Modeling

For heteroscedastic likelihood training, uncertainty may directly parameterize the observation model.

---

## 166. Likelihood Loss

A Gaussian-type scalar negative log-likelihood may contain:

`(y-mu)^2 / sigma^2`

and:

`log sigma^2`.

---

## 167. Variance Collapse

Without proper formulation, a model may drive predicted variance toward degenerate values.

---

## 168. Variance Inflation

A model may also inflate uncertainty to reduce residual penalty.

The likelihood structure must prevent trivial optimization.

---

## 169. Uncertainty Regularization

A model may regularize uncertainty scale or covariance conditioning.

---

## 170. Positive Variance

Predicted variance must remain:

`> 0`.

---

## 171. Covariance Conditioning

Extremely ill-conditioned covariance may create unstable likelihood evaluation.

---

## 172. Log-Variance Parameterization

A scalar variance may be parameterized through:

`log sigma^2`

for numerical stability.

---

## 173. Ensemble Diversity

An ensemble requires meaningful member diversity for disagreement-based uncertainty.

---

## 174. Identical Ensemble Collapse

Identical models with identical parameters and deterministic execution produce zero ensemble spread without establishing certainty.

---

## 175. Ensemble Diversity Sources

Diversity may come from:

- initialization;
- data resampling;
- architecture variants;
- stochastic training;
- posterior approximations.

---

## 176. Diversity versus Accuracy

Greater ensemble diversity does not automatically mean better uncertainty estimation.

---

## 177. Deep Ensemble Calibration

Ensemble spread should be validated against actual residuals.

---

## 178. Domain Detection from Ensemble

Large ensemble disagreement may contribute to OOD scoring.

It is not an exact OOD definition.

---

## 179. Extrapolation

Extrapolation occurs when prediction relies on unsupported regions relative to the declared training domain.

---

## 180. Interpolation

Interpolation lies within supported regions under the declared domain representation.

---

## 181. Interpolation versus In-Domain

The concepts may overlap but are not universally identical.

---

## 182. Convex-Hull Boundary

A simple domain detector may use the convex hull of selected descriptors.

---

## 183. Convex-Hull Limitation

High-dimensional physically valid domains are generally not fully characterized by a simple convex hull.

---

## 184. Descriptor Range Test

A domain detector may check whether descriptors lie within observed training ranges.

---

## 185. Marginal Range Limitation

All individual descriptors may lie within training ranges while their joint combination is unsupported.

---

## 186. Joint Domain Detection

Joint density or representation-space methods address combinations of features.

---

## 187. Composition Domain

A model may explicitly restrict allowed species sets or compositions.

---

## 188. Unknown Species

A species absent from the model vocabulary is a structural domain violation.

---

## 189. Unknown Species Is Not Ternary Neutral

The framework preserves:

`unknown species ≠ 0`.

---

## 190. Charge Domain

If charge state is modeled, unsupported charge conditions must be detected separately.

---

## 191. Thermodynamic Domain

A domain declaration may include ranges of:

- temperature;
- pressure;
- density;
- strain;
- chemical potential.

---

## 192. Thermodynamic Metadata

If temperature or pressure is not an explicit model input, nominal metadata alone does not guarantee the model has encoded that condition.

---

## 193. Structural Domain

Structural domain may be characterized through:

- coordination;
- bond-length distributions;
- angular distributions;
- local order parameters;
- graph statistics;
- learned embeddings.

---

## 194. Defect Domain

Defect structures may be in-domain or out-of-domain depending on training coverage.

---

## 195. Interface Domain

Interfaces may require separate domain coverage from bulk structures.

---

## 196. Surface Domain

Surface environments may be unsupported even when bulk chemistry is supported.

---

## 197. High-Energy Structures

High-energy configurations may or may not be OOD.

Energy magnitude alone does not determine domain membership.

---

## 198. High Force

Large force magnitude may indicate extrapolation, but is not an OOD definition.

---

## 199. Geometric Pathology

Extremely short interatomic distances may be explicitly classified as invalid or OOD according to model contract.

---

## 200. Invalid Geometry

A configuration violating declared geometric validity conditions is invalid.

It need not be processed as ordinary OOD.

---

## 201. Domain Hierarchy

A robust evaluation may use:

`validity`

`→ domain detection`

`→ uncertainty estimation`

`→ prediction acceptance`.

---

## 202. Validity Gate

The first gate checks whether the input satisfies structural and numerical validity conditions.

---

## 203. Domain Gate

The second gate evaluates support relative to the trained model domain.

---

## 204. Uncertainty Gate

The third gate evaluates predictive uncertainty.

---

## 205. Prediction Gate

The final policy determines whether prediction is accepted, rejected, or flagged.

---

## 206. Gate Separation

The framework preserves:

`validity gate ≠ domain gate ≠ uncertainty gate ≠ ternary execution gate`.

---

## 207. Domain-Aware Training

Domain information may be incorporated during training through:

- sample weighting;
- contrastive objectives;
- boundary sampling;
- OOD exposure;
- active learning.

---

## 208. OOD Exposure

A training set may include known out-of-domain examples to improve rejection behavior.

---

## 209. OOD Exposure Boundary

Known OOD examples represent only the sampled exposure domain.

They do not define all possible OOD states.

---

## 210. Contrastive Domain Objective

A contrastive loss may separate in-domain and OOD representations.

---

## 211. Domain Margin

A learned detector may impose a margin between supported and unsupported representations.

---

## 212. Domain Margin Is Not Resonance Margin

The distinction remains:

`domain margin ≠ resonance-window margin`.

---

## 213. Domain Margin Is Not Ternary Margin

The distinction remains:

`domain margin ≠ ternary decision margin`.

---

## 214. Uncertainty-Aware Active Learning

A model may select new reference calculations using uncertainty.

---

## 215. Acquisition Function

Let:

`a(x)`

be an acquisition score.

---

## 216. Maximum-Uncertainty Acquisition

One strategy selects samples with largest:

`u(x)`.

---

## 217. Diversity-Aware Acquisition

Another strategy combines uncertainty with representation diversity.

---

## 218. Domain-Boundary Acquisition

Samples near a domain boundary may be prioritized.

---

## 219. Resonance-Boundary Acquisition

Samples near:

`∂W_R`

may be prioritized independently of domain boundary.

---

## 220. Ternary-Transition Acquisition

Samples near unstable ternary target boundaries may also be prioritized.

---

## 221. Acquisition Distinctions

The framework preserves:

`domain-boundary acquisition ≠ resonance-boundary acquisition ≠ ternary-boundary acquisition`.

---

## 222. Batch Acquisition

A batch acquisition rule should avoid selecting many nearly duplicate configurations.

---

## 223. Acquisition Cost

Reference-evaluation cost may enter the acquisition function.

---

## 224. Active Learning Loop

A canonical loop is:

`train`

`→ evaluate uncertainty/domain`

`→ select candidates`

`→ obtain reference data`

`→ append with provenance`

`→ retrain`

`→ revalidate`.

---

## 225. Active Learning and Data Leakage

Newly acquired training samples must not contaminate frozen test sets.

---

## 226. Domain Expansion

Adding supported reference data may expand the declared in-domain region.

---

## 227. Domain Versioning

The domain definition should be versioned with:

- dataset;
- representation;
- model;
- detector;
- thresholds.

---

## 228. Domain Drift

A change in representation can change domain scores even with the same raw dataset.

---

## 229. Detector Drift

Updating the detector may change classifications.

---

## 230. Threshold Drift

Changing:

`tau_D`

changes domain classification even when model predictions remain unchanged.

---

## 231. Domain Comparability

Domain scores from different model versions are not necessarily directly comparable.

---

## 232. Uncertainty Versioning

Uncertainty outputs must be interpreted with the exact model and calibration version that produced them.

---

## 233. Calibration Drift

Retraining the predictor may invalidate previous calibration.

---

## 234. Recalibration

A new predictor should undergo uncertainty recalibration before its confidence values are treated as equivalent to the previous version.

---

## 235. Symmetry of Domain Detection

A domain detector for a symmetry-equivalent atomistic system should preserve the declared spatial symmetry.

---

## 236. Rotation-Invariant Domain Score

For scalar domain score:

`s_D(gX) = s_D(X)`.

---

## 237. Translation-Invariant Domain Score

For internal atomistic state:

`s_D(R+c) = s_D(R)`.

---

## 238. Permutation-Invariant Global Domain Score

For admissible atom permutation:

`s_D(pi X) = s_D(X)`.

---

## 239. Per-Atom Domain Equivariance

Per-atom domain scores permute with atoms.

---

## 240. Domain Detector Symmetry Residual

A validation may measure:

`epsilon_D = |s_D(gX) - s_D(X)|`.

---

## 241. Uncertainty Symmetry Residual

A scalar uncertainty estimator may be tested through:

`epsilon_U = |u(gX) - u(X)|`.

---

## 242. Force-Covariance Symmetry Test

For force covariance:

`C_F(gX)`

must be compared with:

`Q C_F(X) Q^T`.

---

## 243. Stress-Uncertainty Symmetry

Tensorial uncertainty outputs require the declared tensor transformation law.

---

## 244. Symmetry-Breaking External State

If an external field reduces symmetry, domain and uncertainty estimators must respect the reduced complete-system symmetry.

---

## 245. Domain Detection under Periodicity

Periodic systems require domain descriptors consistent with:

- lattice equivalence;
- wrapped coordinates;
- periodic images;
- cell geometry.

---

## 246. Translation by Lattice Vector

A periodic domain detector must not change under a physically equivalent lattice translation.

---

## 247. Cell Representation

Equivalent cell representations should not create artificial OOD classifications when they represent the same physical periodic state.

---

## 248. Supercell Consistency

A model may require domain-score consistency between equivalent primitive-cell and supercell descriptions.

The exact scaling relation must be defined.

---

## 249. Size Extensivity of Domain Score

A global OOD score based on sums may grow with system size.

Normalization must therefore be explicit.

---

## 250. Per-Atom Normalization

Some global uncertainty metrics may use per-atom normalization.

---

## 251. Maximum Local Uncertainty

Another global metric may use:

`max_i u_i`.

---

## 252. Mean Local Uncertainty

Another may use:

`mean_i u_i`.

---

## 253. Quantile Uncertainty

A high quantile may provide robust sensitivity to localized uncertainty.

---

## 254. Aggregation Rule Declaration

The aggregation rule must be reported with every global uncertainty result.

---

## 255. Energy Extensivity and Uncertainty

Total-energy uncertainty and per-atom-energy uncertainty are distinct metrics.

---

## 256. Force Aggregation

Force uncertainty is naturally local per atom but may also be summarized globally.

---

## 257. Stress Aggregation

Stress uncertainty is configuration-level unless a decomposition is explicitly defined.

---

## 258. Multitask Uncertainty

A model predicting energy, force, stress, resonance, and ternary targets may have distinct uncertainty channels.

---

## 259. Composite Uncertainty

A composite uncertainty score may combine:

`u_E`

`u_F`

`u_S`

`u_R`

`u_T`.

---

## 260. Composite Score

A generic form is:

`u_total = A_U(u_E,u_F,u_S,u_R,u_T)`.

---

## 261. Composite Score Weighting

The aggregation weights must be explicit.

---

## 262. Unit Compatibility

Raw uncertainty values with different units cannot be meaningfully summed without normalization.

---

## 263. Dimensionless Normalization

A composite score may use dimensionless calibrated uncertainty components.

---

## 264. Maximum-Risk Composite

A safety-oriented policy may use the maximum normalized uncertainty channel.

---

## 265. Weighted Composite

Another policy may use a weighted sum.

---

## 266. Composite Uncertainty Is Not Physical Observable

The framework preserves:

`u_total ≠ physical energy/force/stress/resonance state`.

---

## 267. Task-Specific Acceptance

A configuration may be acceptable for one prediction task and unacceptable for another.

---

## 268. Energy-Domain State

A model may define:

`d_E`.

---

## 269. Force-Domain State

A model may define:

`d_F`.

---

## 270. Stress-Domain State

A model may define:

`d_S`.

---

## 271. Resonance-Domain State

A model may define:

`d_R`.

---

## 272. Ternary-Domain State

A model may define:

`d_T`.

---

## 273. Task-Domain Separation

The framework preserves:

`d_E`

`d_F`

`d_S`

`d_R`

`d_T`

as potentially distinct support states.

---

## 274. Domain Intersection

A strict all-task acceptance rule may require:

`d_E = d_F = d_S = d_R = d_T = IN_DOMAIN`.

---

## 275. Task-Selective Acceptance

A task-specific workflow may require only the relevant subset.

---

## 276. Uncertainty Thresholds

Each task may have its own threshold:

`tau_E`

`tau_F`

`tau_S`

`tau_R`

`tau_T`.

---

## 277. Threshold Provenance

Thresholds may be:

- calibrated;
- benchmark-defined;
- author-defined;
- source-derived.

---

## 278. Threshold Optimization

A threshold may be optimized against a validation criterion.

---

## 279. Threshold Selection Metric

Possible objectives include:

- target coverage;
- maximum tolerated error;
- false-accept rate;
- false-reject rate;
- calibration criterion.

---

## 280. Threshold Selection Is Not Physics

An uncertainty threshold is a decision-policy parameter.

---

## 281. Domain Detector Evaluation

A detector should be tested on:

- known in-domain samples;
- near-boundary samples;
- known held-out domains;
- synthetic stress cases where appropriate.

---

## 282. True Positive Definition

OOD evaluation requires explicit designation of which class is considered positive.

---

## 283. False Accept

A false accept occurs when an OOD sample is classified as acceptable.

---

## 284. False Reject

A false reject occurs when an in-domain sample is rejected.

---

## 285. ROC-Type Evaluation

A continuous domain score may be evaluated across thresholds.

---

## 286. Precision-Recall Evaluation

Precision-recall analysis may be appropriate for strongly imbalanced OOD datasets.

---

## 287. AUROC Boundary

A single AUROC value does not determine operating-point behavior.

---

## 288. Operating Threshold

Deployment or benchmark reports must state the actual threshold used.

---

## 289. Calibration under Distribution Shift

Calibration measured in-domain may degrade under distribution shift.

---

## 290. Shift Detection

Domain detectors may identify shift before uncertainty calibration fails catastrophically.

---

## 291. Covariate Shift

Input distribution may change while the conditional target relation remains similar.

---

## 292. Concept Shift

The mapping from input to target may itself change.

---

## 293. Label Shift

Target distribution may change independently of some input statistics.

---

## 294. Shift Terminology

The specific shift definition must be explicit.

---

## 295. Distribution Shift Is Not OOD by Identity

A shifted distribution may still remain inside the declared model domain.

---

## 296. OOD Is Model-Relative

Out-of-domain status is defined relative to:

- training data;
- representation;
- detector;
- task;
- thresholds.

---

## 297. Domain Is Version-Relative

The same physical configuration may be OOD for one model version and in-domain for another.

---

## 298. Uncertainty Is Model-Relative

The same configuration may receive different uncertainty estimates from different models.

---

## 299. Validation against Reference Error

Uncertainty quality must be evaluated against held-out prediction errors where reference data exist.

---

## 300. Rank Correlation

A useful uncertainty estimator may rank high-error samples above low-error samples even if absolute calibration is imperfect.

---

## 301. Error-Conditioned Uncertainty

Plots or statistics may compare uncertainty quantiles against observed errors.

---

## 302. Sparsification Curve

A sparsification evaluation removes high-uncertainty samples and measures residual error on the remaining set.

---

## 303. Oracle Comparison

An oracle sparsification curve removes samples by true error.

The gap between uncertainty-based and oracle curves measures ranking quality.

---

## 304. Calibration and Ranking Are Distinct

The framework preserves:

`uncertainty ranking quality ≠ uncertainty calibration`.

---

## 305. Domain Detection and Uncertainty Are Distinct

The framework preserves:

`OOD detection ≠ uncertainty estimation`.

---

## 306. High Uncertainty In-Domain

An in-domain sample may have high uncertainty.

---

## 307. Low Uncertainty OOD

A model may incorrectly assign low uncertainty to an OOD sample.

---

## 308. Failure Detection

A robust system should therefore validate both uncertainty and domain detection independently.

---

## 309. Numerical Uncertainty

Finite precision may contribute additional computational variability.

---

## 310. Floating-Point Sensitivity

Numerically sensitive predictions may vary across arithmetic configurations.

---

## 311. Mixed-Precision Uncertainty

A benchmark may compare predictions across precision modes.

---

## 312. Quantization Uncertainty

Quantized inference may introduce additional error not represented by statistical model uncertainty.

---

## 313. Numerical Error versus Model Uncertainty

The framework preserves:

`numerical error ≠ epistemic uncertainty`.

---

## 314. Numerical Error versus Aleatoric Uncertainty

Likewise:

`numerical error ≠ aleatoric uncertainty`.

---

## 315. Deterministic Model

A deterministic model may still require uncertainty estimation through:

- ensembles;
- external detectors;
- calibrated residual models;
- distance-based methods.

---

## 316. Determinism Is Not Certainty

The framework preserves:

`deterministic output ≠ certain prediction`.

---

## 317. Replay Consistency

Deterministic replay verifies reproducibility of a computation.

It does not establish predictive reliability.

---

## 318. Replay Consistency versus Calibration

The framework preserves:

`deterministic replay ≠ uncertainty calibration`.

---

## 319. Uncertainty Logging

A prediction record may include:

- model version;
- dataset version;
- detector version;
- uncertainty method;
- uncertainty value;
- domain score;
- domain class;
- thresholds;
- acceptance state.

---

## 320. Local Uncertainty Trace

For each atom, a trace may include:

- atom index;
- species;
- local uncertainty;
- local domain score;
- resonance uncertainty;
- ternary uncertainty.

---

## 321. Global Uncertainty Trace

A global trace may include task-specific aggregated scores.

---

## 322. Ternary Trace Integration

A ternary trace may record separately:

`t_target`

`t_exec`

`t_pending`

`u_T`

`d_T`.

---

## 323. Resonance Trace Integration

A resonance trace may record separately:

`r`

`C_R`

`u_R`

`d_R`.

---

## 324. Mechanical Trace Integration

Mechanical predictions may record:

`E`

`u_E`

`F`

`u_F`

`Sigma`

`u_S`.

---

## 325. Trace Separation

Uncertainty and domain fields must not overwrite semantic state fields.

---

## 326. Uncertainty Metrics

A validation suite may report:

- negative log-likelihood;
- calibration error;
- interval coverage;
- sharpness;
- rank correlation;
- sparsification error;
- OOD AUROC;
- OOD precision-recall;
- false-accept rate;
- false-reject rate.

---

## 327. Task-Specific Metrics

Metrics should be reported separately for:

- energy;
- force;
- stress;
- resonance;
- ternary state.

---

## 328. Force Uncertainty Metric

Force uncertainty may be evaluated per atom using residual norm:

`||F_pred - F_ref||`.

---

## 329. Stress Uncertainty Metric

Stress uncertainty may be compared against a declared tensor residual.

---

## 330. Ternary Uncertainty Metric

Ternary uncertainty may be evaluated through:

- calibration;
- entropy;
- disagreement;
- class-conditional error.

---

## 331. Neutral-Class Metrics

The active-neutral class requires its own:

- precision;
- recall;
- calibration;
- uncertainty statistics.

---

## 332. Resonance Boundary Metrics

Boundary samples should be evaluated separately where resonance classification is used.

---

## 333. OOD Benchmark Composition

An OOD benchmark must state which changes create the OOD set.

---

## 334. Composition Shift Benchmark

Examples may hold geometry regime fixed while changing composition coverage.

---

## 335. Structural Shift Benchmark

Examples may preserve chemistry while changing structural regime.

---

## 336. Thermodynamic Shift Benchmark

Examples may probe temperature, pressure, density, or strain ranges beyond training support.

---

## 337. Defect Shift Benchmark

Examples may introduce defect classes absent from training.

---

## 338. Surface and Interface Shift Benchmark

Examples may introduce surfaces or interfaces not represented in bulk training data.

---

## 339. OOD Difficulty Levels

A benchmark may classify shifts as near-domain or far-domain.

The criteria must be explicit.

---

## 340. Near-OOD

Near-OOD samples lie close to supported data under the declared domain metric but outside a selected support threshold.

---

## 341. Far-OOD

Far-OOD samples lie substantially outside support under the declared metric.

---

## 342. Near-OOD Is Not Resonance Boundary

The distinction remains:

`near-OOD ≠ resonance BOUNDARY`.

---

## 343. Domain Test Fixture

Synthetic or curated domain examples may carry:

`TEST_FIXTURE`.

---

## 344. Uncertainty Provenance

Uncertainty definitions and results use the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 345. Primary-Source Uncertainty Method

An established uncertainty method adopted from literature carries:

`PRIMARY_SOURCE`.

---

## 346. Derived Domain Score

A domain score deterministically constructed from defined model features may carry:

`DERIVED`.

---

## 347. Author-Defined Detector

A TR-EIF-specific domain detector or composite uncertainty policy may carry:

`AUTHOR_DEFINED`.

---

## 348. Calibrated Threshold

A threshold fitted on calibration data carries:

`CALIBRATED`.

---

## 349. Benchmark Uncertainty Result

Measured calibration or OOD performance carries:

`BENCHMARK`.

---

## 350. Test Fixture

Synthetic uncertainty or domain examples carry:

`TEST_FIXTURE`.

---

## 351. Uncertainty-Model Extension Rule

Any uncertainty model must define:

1. target quantity;

2. uncertainty type;

3. representation;

4. units;

5. estimation method;

6. calibration method;

7. symmetry behavior;

8. validation metric;

9. provenance.

---

## 352. Domain-Detector Extension Rule

Any domain detector must define:

1. input representation;

2. task scope;

3. domain score;

4. score direction;

5. thresholds;

6. reference support set;

7. aggregation;

8. symmetry behavior;

9. benchmark protocol.

---

## 353. Ensemble Extension Rule

Any ensemble uncertainty method must define:

1. number of members;

2. diversity mechanism;

3. prediction aggregation;

4. spread metric;

5. calibration;

6. inference cost.

---

## 354. Probabilistic Regression Extension Rule

Any probabilistic regression model must define:

1. predictive distribution;

2. parameterization;

3. positivity constraints;

4. likelihood;

5. calibration;

6. numerical stabilization.

---

## 355. Ternary-Uncertainty Extension Rule

Any ternary uncertainty model must define:

1. ternary logits or probabilities;

2. hard decision rule;

3. active-neutral semantics;

4. uncertainty measure;

5. abstention state where used;

6. target/execution distinction;

7. calibration.

---

## 356. Resonance-Uncertainty Extension Rule

Any resonance uncertainty model must define:

1. resonance coordinate or class;

2. uncertainty representation;

3. window relation;

4. boundary relation;

5. OOD separation;

6. resonance-to-ternary interface.

---

## 357. Mechanical-Uncertainty Extension Rule

Any energy/force/stress uncertainty model must define:

1. predicted mechanical quantity;

2. uncertainty units;

3. aggregation;

4. symmetry law;

5. calibration target;

6. benchmark metric.

---

## 358. Multiscale-Uncertainty Extension Rule

Any multiscale uncertainty model must define:

1. scale set;

2. uncertainty per scale;

3. aggregation;

4. cross-scale consistency;

5. localized failure rule;

6. global acceptance rule.

---

## 359. Active-Learning Extension Rule

Any uncertainty-driven acquisition method must define:

1. candidate pool;

2. acquisition score;

3. diversity criterion;

4. reference cost;

5. batch selection;

6. data split update;

7. retraining protocol.

---

## 360. Acceptance-Policy Extension Rule

Any acceptance/rejection policy must define:

1. validity gate;

2. domain gate;

3. uncertainty gate;

4. task thresholds;

5. abstention state;

6. fallback behavior;

7. reporting.

---

## 361. Canonical Uncertainty Invariants

Every conforming uncertainty layer preserves:

1. explicit uncertainty state;

2. explicit task scope;

3. explicit uncertainty type;

4. explicit calibration;

5. explicit domain distinction;

6. explicit symmetry behavior;

7. explicit acceptance policy where used;

8. explicit provenance.

---

## 362. Canonical Domain Invariants

Every conforming domain detector preserves:

1. explicit support definition;

2. explicit score;

3. explicit threshold;

4. explicit task scope;

5. explicit version dependence;

6. explicit OOD benchmark.

---

## 363. Canonical Active-Neutral Separation

The framework preserves:

`0 ≠ OUT_OF_DOMAIN`

`0 ≠ UNCERTAIN`

`0 ≠ ABSTAIN`

`0 ≠ INVALID`

`0 ≠ MISSING`

`0 ≠ MASK`

`0 ≠ PADDING`

`0 ≠ UNKNOWN`

`0 ≠ NaN`.

---

## 364. Canonical Resonance Separation

The framework preserves:

`OUTSIDE resonance window ≠ OUT_OF_DOMAIN`

`BOUNDARY resonance class ≠ domain boundary`

`INSIDE resonance window ≠ IN_DOMAIN`

`resonance uncertainty ≠ resonance state`.

---

## 365. Canonical Mechanical Separation

The framework preserves:

`energy uncertainty ≠ energy`

`force uncertainty ≠ force`

`stress uncertainty ≠ stress`

`uncertainty score ≠ physical observable`.

---

## 366. Canonical Learning Separation

The framework preserves:

`uncertainty ≠ realized error`

`confidence ≠ accuracy`

`calibration ≠ accuracy`

`sharpness ≠ calibration`

`determinism ≠ certainty`

`OOD detection ≠ uncertainty estimation`.

---

## 367. Canonical Scientific Distinctions

The uncertainty layer preserves:

`domain-boundary crossing ≠ bifurcation`

`domain-boundary crossing ≠ ternary transition`

`domain-boundary crossing ≠ structural transition`

`structural transition ≠ physical phase transition`

`resonance-window crossing ≠ bifurcation`

`ternary state ≠ energy`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`.

---

## 368. Canonical Ternary Invariants

The exact ternary domain remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

---

## 369. Canonical Execution Invariants

Uncertainty and domain detection do not modify the committed execution topology:

`-1 ↔ 0 ↔ 1`.

---

## 370. Canonical Direct-Transition Invariant

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 371. Canonical Opposite Routes

Opposite-polarity execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 372. Canonical Domain Chain

A canonical domain-evaluation chain is:

`input`

`→ validity check`

`→ representation`

`→ domain score`

`→ domain classification`

`→ task-specific acceptance policy`.

---

## 373. Canonical Uncertainty Chain

A canonical uncertainty chain is:

`input`

`→ model prediction`

`→ uncertainty estimation`

`→ calibration`

`→ task-specific uncertainty score`

`→ acceptance policy`.

---

## 374. Canonical Combined Chain

A complete prediction-control chain may be:

`configuration`

`→ validity`

`→ domain detection`

`→ prediction`

`→ uncertainty estimation`

`→ calibration`

`→ acceptance/rejection`

`→ semantic output`.

---

## 375. Canonical Ternary-Uncertainty Chain

For ternary target:

`resonance state`

`→ ternary logits/probabilities`

`→ uncertainty estimate`

`→ optional acceptance gate`

`→ t_target ∈ {-1,0,1}`

`→ downstream execution`.

---

## 376. No Semantic Overloading

The same machine code must not be reused ambiguously for:

- neutral;
- uncertainty;
- rejection;
- missing data;
- invalid state;
- out-of-domain state.

---

## 377. Interface to Chapter 09

Chapter 09 develops Optimization.

It integrates:

- mechanical objectives;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty-aware weighting;
- domain-aware sampling;
- parameter update rules.

---

## 378. Interface to Chapter 10

Chapter 10 summarizes the complete Learning and Optimization volume and consolidates the interfaces among:

- model architecture;
- training data;
- loss functionals;
- energy-force-stress training;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty and domain detection;
- optimization.

---

## 379. Final Formal Structure

The uncertainty and domain layer may be represented as:

`UDD = (X_U, X_D, P_U, P_D, C_U, C_D, A_U, A_D, V_U, V_D)`.

Here:

- `X_U` is uncertainty state;
- `X_D` is domain state;
- `P_U` is uncertainty estimation;
- `P_D` is domain scoring;
- `C_U` is uncertainty calibration;
- `C_D` is domain classification;
- `A_U` is uncertainty aggregation;
- `A_D` is domain aggregation;
- `V_U` is uncertainty validation;
- `V_D` is domain validation.

A task-specific prediction contract may be written:

`Y_task = (y, u_y, d_y, a_y)`.

Here:

- `y` is the semantic prediction;
- `u_y` is uncertainty;
- `d_y` is domain state;
- `a_y` is acceptance state.

These fields remain semantically distinct.

---

## 380. Final Statement

Uncertainty and domain detection provide a separate control layer for evaluating prediction reliability and model support within TR-EIP.

The framework distinguishes:

- epistemic uncertainty;
- aleatoric uncertainty;
- confidence;
- calibration;
- domain support;
- out-of-domain state;
- numerical validity;
- prediction acceptance.

The following distinctions remain invariant:

`uncertainty ≠ error`

`confidence ≠ accuracy`

`calibration ≠ accuracy`

`determinism ≠ certainty`

`OUT_OF_DOMAIN ≠ OUTSIDE resonance window`

`domain boundary ≠ resonance boundary`

`domain boundary ≠ ternary 0`

`uncertainty ≠ ternary 0`

`ABSTAIN ≠ ternary 0`

`INVALID ≠ OUT_OF_DOMAIN`

`MISSING ≠ ternary 0`

`NaN ≠ ternary 0`.

The exact balanced ternary kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

Uncertainty may influence whether a target is accepted, delayed, rejected, or flagged.

It does not redefine the ternary state space and does not authorize any forbidden execution event.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

These definitions establish the uncertainty and domain-control layer required for Optimization developed in Chapter 09.
