# Training Data

## 1. Purpose

This chapter defines training-data structure for the TR-EIP learning and optimization layer of TR-EIF.

Training data provide the reference configurations, observables, labels, provenance, units, and split structure required to optimize model parameters without altering the architectural semantics established in Volumes 01–03.

The canonical data chain is:

`source data`

`→ normalized reference artifact`

`→ dataset manifest`

`→ split assignment`

`→ model input`

`→ reference target`

`→ loss evaluation`

`→ optimization`.

---

## 2. Dataset

Let:

`D`

denote a dataset.

A dataset is a finite or indexed collection of samples:

`D = {d_k}`.

Each sample:

`d_k`

contains an explicitly declared atomic configuration and zero or more reference outputs.

---

## 3. Sample Structure

A generic sample may be represented:

`d_k = (X_k, Y_k, M_k)`.

Here:

- `X_k` is model input state;
- `Y_k` is reference output state;
- `M_k` is metadata.

---

## 4. Atomic Input State

The atomic input state may contain:

`X_k = (R_k, A_k, H_k, PBC_k, X_aux,k)`.

Here:

- `R_k` is atomic position state;
- `A_k` is species state;
- `H_k` is periodic cell where present;
- `PBC_k` is periodicity state;
- `X_aux,k` contains optional declared auxiliary inputs.

---

## 5. Reference Output State

A reference-output state may contain:

`Y_k = (E_k, F_k, Sigma_k, X_R,k, X_T,k, O_k)`.

Here:

- `E_k` is reference energy;
- `F_k` is reference force;
- `Sigma_k` is reference stress;
- `X_R,k` is optional resonance state;
- `X_T,k` is optional ternary state;
- `O_k` contains additional declared observables.

---

## 6. Optional Targets

Not every sample must contain every target.

Missing targets must be represented explicitly.

Missing target state is not ternary active neutral.

---

## 7. Missing Target

If force, stress, energy, resonance, or ternary reference is absent, the absence must be encoded through metadata or mask state.

The framework preserves:

`missing target ≠ ternary 0`.

---

## 8. Invalid Target

A numerically invalid target must be represented separately from a missing target.

The framework preserves:

`INVALID ≠ MISSING ≠ 0`.

---

## 9. Data Source

Each dataset must identify the origin of its samples.

Sources may include:

- ab initio calculations;
- classical simulations;
- experimental measurements;
- published databases;
- internal simulations;
- synthetic fixtures;
- calibrated derived datasets.

---

## 10. Source Provenance

Each data item or dataset component must carry one of the canonical provenance classes where applicable:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 11. Primary-Source Data

Reference values transcribed or imported directly from a documented external scientific source carry:

`PRIMARY_SOURCE`.

---

## 12. Derived Data

Values computed from existing reference state carry:

`DERIVED`.

Examples include:

- energy differences;
- normalized quantities;
- symmetry-transformed labels;
- derived structural descriptors.

---

## 13. Calibrated Data

Values produced through calibration or fitted reconstruction carry:

`CALIBRATED`.

---

## 14. Test Fixture Data

Synthetic deterministic samples constructed for invariant testing carry:

`TEST_FIXTURE`.

---

## 15. Benchmark Data

Samples used primarily for runtime, scaling, or numerical benchmark evaluation may carry:

`BENCHMARK`.

---

## 16. Dataset Manifest

Every dataset should have a manifest describing at least:

- dataset identifier;
- dataset version;
- source;
- species set;
- units;
- configuration domain;
- target fields;
- split policy;
- provenance;
- generation or import procedure.

---

## 17. Dataset Identifier

A dataset identifier uniquely identifies the declared dataset artifact.

---

## 18. Dataset Version

Any change that affects sample content, target values, split structure, units, or semantics requires a new dataset version.

---

## 19. Dataset Hash

A dataset artifact may carry a cryptographic hash for byte-level integrity.

Byte identity remains distinct from scientific equivalence.

---

## 20. Sample Identifier

Each sample should carry a stable identifier when traceability is required.

---

## 21. Configuration Identifier

A configuration identifier may be distinct from sample identifier if multiple target sets or metadata records refer to the same atomic configuration.

---

## 22. Configuration Duplication

Repeated configurations must be detectable where split leakage or weighting depends on uniqueness.

---

## 23. Exact Duplicate

Two samples are exact duplicates when their relevant serialized configuration and target state are identical under the declared serialization contract.

---

## 24. Symmetry-Equivalent Duplicate

Two configurations may differ numerically but be equivalent under:

- translation;
- rotation;
- reflection where applicable;
- species-preserving permutation;
- periodic-image equivalence.

Such samples may represent the same physical geometry.

---

## 25. Near Duplicate

Two configurations may be numerically similar without being exactly or symmetry-equivalent.

The near-duplicate criterion must be explicitly defined if used.

---

## 26. Duplicate Handling

A dataset preparation pipeline may:

- retain duplicates;
- remove duplicates;
- merge duplicates;
- reweight duplicates.

The selected policy must be explicit.

---

## 27. Species Set

Let:

`A_D`

denote the species set represented in a dataset.

A model trained on the dataset must declare compatibility with:

`A_D`.

---

## 28. Unsupported Species

A configuration containing species outside the declared model domain is out of domain.

It is not active neutral.

---

## 29. Composition

Each sample may carry composition metadata.

For species:

`a`

define:

`N_a`.

---

## 30. Composition Vector

A composition vector may be represented by counts or fractions over the species set.

---

## 31. Composition Distribution

A dataset manifest may report the empirical distribution of compositions.

---

## 32. Structural Coverage

A dataset may report coverage of:

- coordination environments;
- phases or structural classes;
- defects;
- interfaces;
- surfaces;
- liquids;
- solids;
- amorphous states.

The exact categories must be explicitly defined.

---

## 33. Thermodynamic Coverage

A dataset may report coverage of:

- temperature;
- pressure;
- density;
- composition;
- cell volume.

These are state-domain descriptors.

---

## 34. Temperature Metadata

Temperature may be metadata associated with a configuration or trajectory state.

A single static configuration does not by itself define a thermodynamic ensemble temperature.

---

## 35. Pressure Metadata

Pressure may be:

- externally imposed condition;
- derived observable;
- target quantity.

These roles must remain distinct.

---

## 36. Density Metadata

Density may refer to:

- mass density;
- number density;
- another explicitly defined quantity.

It must not be confused with graph density.

---

## 37. Static Configuration Data

A static sample may contain:

- positions;
- species;
- cell;
- energy;
- force;
- stress.

---

## 38. Trajectory Data

A trajectory dataset contains ordered configurations:

`X[0], X[1], ..., X[T]`.

The ordering is meaningful.

---

## 39. Trajectory Frame

Each trajectory frame is one atomic configuration plus associated dynamic metadata.

---

## 40. Temporal Correlation

Adjacent trajectory frames may be strongly correlated.

The split protocol must account for temporal correlation where relevant.

---

## 41. Trajectory Identifier

Each frame should identify its parent trajectory when trajectory-level splitting is used.

---

## 42. Time Coordinate

A trajectory sample may store:

- physical time;
- numerical step;
- both.

These remain distinct.

---

## 43. Physical Time

Physical time carries units.

---

## 44. Numerical Step

A numerical step is an integrator index.

It is not physical time by identity.

---

## 45. Training Step Boundary

The framework preserves:

`trajectory timestep ≠ training step`.

---

## 46. Velocity Data

A trajectory sample may include:

`V_k`.

Velocity is a dynamical input.

It is not required by every static interatomic model.

---

## 47. Momentum Data

Momentum may be included when required:

`P_k = M V_k`.

---

## 48. Energy Target

Reference energy must specify:

- value;
- units;
- reference convention;
- total or per-atom semantics.

---

## 49. Total Energy

A total energy target scales with system size.

---

## 50. Energy per Atom

An energy-per-atom target is a normalized derived quantity.

It is not identical to total energy.

---

## 51. Energy Reference Zero

Potential-energy zero may depend on the reference convention.

The convention must be preserved in the dataset manifest.

---

## 52. Species Reference Energies

A dataset may use species-specific reference offsets.

These must be recorded if targets are shifted.

---

## 53. Force Target

Reference force is a per-atom vector:

`F_i^ref ∈ R^3`.

The atom ordering must correspond exactly to the input configuration ordering.

---

## 54. Force Units

Force units must be declared.

---

## 55. Force Symmetry

If a training configuration is transformed by:

`Q`

the force labels must transform:

`F_i' = QF_i`.

---

## 56. Force Permutation

If atoms are permuted, force labels must be permuted consistently.

---

## 57. Stress Target

A stress reference is a tensor:

`Sigma^ref`.

The dataset must declare:

- tensor type;
- sign convention;
- units;
- normalization;
- coordinate convention.

---

## 58. Stress Rotation

For rigid rotation:

`Sigma' = Q Sigma Q^T`.

---

## 59. Stress Component Ordering

Serialized stress must define component ordering.

---

## 60. Symmetric Stress Storage

If only symmetric components are stored, the reconstruction convention must be explicit.

---

## 61. Resonance Target

A dataset may contain resonance reference state:

`r^ref ∈ X_R`.

Its semantics must match the model resonance-state definition.

---

## 62. Resonance Coordinate Metadata

Each resonance coordinate should identify:

- scope;
- units;
- transformation type;
- scale;
- source or derivation.

---

## 63. Resonance Window Metadata

If labels depend on a resonance window:

`W_R`

the window version and definition must be identified.

---

## 64. Resonance Class Label

A categorical resonance label may belong to:

`{OUTSIDE, BOUNDARY, INSIDE}`.

This is not a ternary label.

---

## 65. Ternary Target Label

A ternary target label belongs exactly to:

`-1/0/1`.

---

## 66. Executed Ternary Label

An execution label also belongs to:

`-1/0/1`

but has distinct semantics from target state.

---

## 67. Pending Ternary Label

A pending destination may belong to:

`{-1,1}`

or:

`NONE`.

---

## 68. Target/Execution Serialization

A transition dataset must use separate fields for:

- `t_target`;
- `t_exec`;
- `t_pending`.

---

## 69. Active Neutral Label

The value:

`0`

is an explicit valid label.

It must not be removed by generic missing-value filtering.

---

## 70. Invalid Ternary Encoding

Any value outside:

`-1/0/1`

is invalid semantic ternary state.

---

## 71. Continuous Classifier Data

A dataset may additionally store:

- logits;
- probabilities;
- decision scores;
- margins.

These are continuous classifier data.

They are not ternary states.

---

## 72. Uncertainty Metadata

Reference data may include uncertainty estimates.

These may be:

- standard deviation;
- confidence interval;
- covariance;
- another declared uncertainty representation.

---

## 73. Uncertainty versus Error

Reference uncertainty and observed prediction error are distinct quantities.

---

## 74. Quality Flag

Samples may carry quality flags such as:

- accepted;
- suspect;
- rejected;
- incomplete.

These are data-quality states.

They are not ternary states.

---

## 75. Inclusion Mask

A training pipeline may use an inclusion mask.

Mask value:

`0`

does not mean active neutral.

---

## 76. Target Mask

Each target field may have an independent availability mask.

---

## 77. Multi-Target Sample

A single configuration may contain energy but no stress, or force but no resonance labels.

The loss pipeline must use only available targets.

---

## 78. Partial Supervision

Partial supervision is permitted when target availability is explicit.

---

## 79. Unit System

Every dataset must declare a coherent unit system or explicit per-field units.

---

## 80. Position Units

Atomic positions require length units.

---

## 81. Cell Units

Cell vectors use the same or explicitly convertible length unit.

---

## 82. Energy Units

Energy targets use declared energy units.

---

## 83. Force Unit Relation

Force units must remain dimensionally consistent with:

`energy / length`.

---

## 84. Stress Unit Relation

Stress units must remain dimensionally consistent with:

`energy / volume`.

---

## 85. Unit Conversion

Unit conversion must be deterministic and reversible within the numerical precision contract.

---

## 86. Canonical Internal Units

A training pipeline may convert all data into one canonical internal unit system.

The conversion must be recorded.

---

## 87. Nondimensionalization

A model may use nondimensionalized inputs or targets.

All reference scales must be explicit.

---

## 88. Normalization

Numerical normalization is distinct from physical unit conversion.

---

## 89. Energy Normalization

Energy may be centered or scaled for optimization.

---

## 90. Force Normalization

Force may be scaled by a fixed training factor.

---

## 91. Stress Normalization

Stress may likewise be scaled.

---

## 92. Inverse Transformation

Every normalized reported physical output requires a defined inverse transformation.

---

## 93. Training Statistics

Normalization statistics may include:

- mean;
- variance;
- scale;
- percentile bounds.

---

## 94. Statistics Source

The source split used to compute normalization statistics must be explicit.

---

## 95. Training-Only Statistics

Under a strict split protocol, normalization statistics are computed from:

`D_train`

only.

---

## 96. Validation Leakage

Using:

`D_val`

or:

`D_test`

to compute train-time normalization statistics may violate the declared split protocol.

---

## 97. Split Definition

The canonical dataset partition is:

`D = D_train ∪ D_val ∪ D_test`.

---

## 98. Split Assignment

Each sample must belong to exactly the declared split under a strict partition.

---

## 99. Random Split

A random split assigns samples according to a reproducible random procedure.

---

## 100. Structure-Aware Split

A structure-aware split separates structural families.

---

## 101. Composition-Aware Split

A composition-aware split separates selected compositions.

---

## 102. Trajectory-Aware Split

A trajectory-aware split assigns entire trajectories or temporal blocks to one split.

---

## 103. Temporal Block Split

A trajectory may be divided into contiguous time blocks.

---

## 104. Grouped Split

Samples sharing a group identifier may be kept in the same split.

---

## 105. Source-Aware Split

Samples from different reference sources may be separated to test cross-source generalization.

---

## 106. Thermodynamic Split

Temperature, pressure, density, or composition regions may be held out deliberately.

---

## 107. Extrapolation Split

A split may be designed specifically to test extrapolation.

---

## 108. Split Seed

Any stochastic split must store the random seed and algorithm.

---

## 109. Split Manifest

The exact sample identifiers belonging to each split should be recoverable.

---

## 110. Split Immutability

Once benchmark results are tied to a split version, changing split membership creates a new dataset/split version.

---

## 111. Leakage through Duplicates

Exact or symmetry-equivalent duplicates across splits may reduce split independence.

---

## 112. Leakage through Trajectories

Adjacent frames from one trajectory in different splits may create temporal leakage.

---

## 113. Leakage through Derived Samples

A derived sample must not cross splits in a way that exposes its source sample contrary to the split policy.

---

## 114. Augmented Sample Split

Symmetry-augmented copies should normally inherit the split of their source configuration under strict separation.

---

## 115. Dataset Balance

A dataset may be unbalanced across:

- species;
- compositions;
- structures;
- thermodynamic states;
- ternary classes.

---

## 116. Class Balance

For ternary labels, report frequencies of:

`-1`

`0`

`1`

separately.

---

## 117. Neutral-Class Frequency

The active-neutral frequency must remain explicit.

---

## 118. Resonance-Class Balance

If resonance classes are supervised, report:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

separately.

---

## 119. Reweighting

Training may reweight samples or classes without altering the underlying dataset labels.

---

## 120. Oversampling

A sampler may present selected samples more frequently.

This changes training exposure, not dataset identity.

---

## 121. Undersampling

A sampler may reduce exposure of common classes.

---

## 122. Sampling Distribution

The training sampling distribution should be distinguishable from the raw empirical dataset distribution.

---

## 123. Active Learning Data

A dataset may be expanded iteratively using model-driven acquisition.

Each acquisition round must be traceable.

---

## 124. Acquisition Round

An active-learning round may contain:

- candidate generation;
- model scoring;
- selection;
- reference evaluation;
- dataset append.

---

## 125. Active Learning versus Online Learning

Active learning selects new reference samples.

Online learning updates parameters during data arrival.

The two are distinct.

---

## 126. Data Generation

Synthetic configurations may be generated through:

- random displacement;
- strained cells;
- defect construction;
- molecular dynamics;
- interpolation;
- perturbation;
- composition changes.

---

## 127. Random Displacement

A random-displacement generator must define the displacement distribution and amplitude.

---

## 128. Strain Generation

Cell strain samples must define:

- strain measure;
- magnitude;
- cell transformation;
- coordinate update.

---

## 129. Defect Data

Defect configurations may include:

- vacancy;
- interstitial;
- substitution;
- surface;
- interface.

The defect semantics must be explicit.

---

## 130. High-Energy Configurations

Training may include high-energy or short-distance configurations to define repulsive behavior.

Their admissibility and weighting must be explicit.

---

## 131. Collision Exclusion

Configurations violating the declared minimum-distance domain may be rejected or retained for specialized short-range training.

The policy must be explicit.

---

## 132. Configuration Filtering

A data filter may reject samples based on:

- non-finite values;
- invalid species;
- invalid cell;
- impossible metadata;
- target inconsistency.

---

## 133. Filter Provenance

The filtering rule and removed-sample count should be recorded.

---

## 134. Data Cleaning

Data cleaning may include:

- unit correction;
- metadata correction;
- duplicate removal;
- invalid-row removal.

Cleaning must not silently alter scientific values without provenance.

---

## 135. Reference Recalculation

If targets are recomputed, the new values belong to a new derived dataset artifact.

---

## 136. Data Correction

A corrected source error requires a new dataset version.

---

## 137. Label Consistency

Energy, force, and stress labels for the same sample should correspond to the same physical and numerical reference calculation where joint consistency is assumed.

---

## 138. Energy-Force Consistency

If force is expected to equal the negative coordinate gradient of reference energy, the dataset source should preserve that relation within its numerical method.

---

## 139. Stress-Energy Consistency

If stress is expected to derive from energy/cell response, the reference source should use a compatible convention.

---

## 140. Mixed Reference Sources

Energy and force from different reference methods may be combined only when the learning problem explicitly defines the intended relation.

---

## 141. Reference Method Metadata

A sample may record:

- electronic-structure method;
- basis;
- pseudopotential;
- functional;
- convergence parameters;
- classical potential;
- another source-method description.

---

## 142. Reference Precision

Reference numerical tolerances may affect target quality.

These should be recorded where available.

---

## 143. SCF Convergence Metadata

Electronic-structure reference data may contain convergence status.

Nonconverged results should be flagged explicitly.

---

## 144. Force Convergence Metadata

Force calculation tolerance may be recorded separately from energy convergence.

---

## 145. Stress Convergence Metadata

Stress convergence may require its own tolerance.

---

## 146. Experimental Data Alignment

Experimental observables may not correspond directly to one atomic configuration.

A forward observable model must define the relation.

---

## 147. Ensemble Observable

An ensemble observable may require multiple configurations or a trajectory.

It should not be attached to one frame as if it were a direct per-frame target unless the mapping justifies it.

---

## 148. Thermodynamic Observable

Thermodynamic observables may require averaging over state distributions.

---

## 149. Transport Observable

Transport coefficients generally require temporal or ensemble information.

They belong to later molecular-dynamics and multiscale layers.

---

## 150. Structural Descriptor Target

A derived structural descriptor may be used as an auxiliary target.

Its definition and symmetry must be explicit.

---

## 151. Graph Target

A graph label may supervise graph construction or learned edge scoring.

It remains a computational relation unless separately defined physically.

---

## 152. Chemical Bond Label

A chemical-bond label is distinct from generic graph-edge labels.

---

## 153. Resonance Label Source

A resonance label may be:

- directly measured;
- derived;
- calibrated;
- author-defined;
- generated by an upstream model.

Its provenance must be explicit.

---

## 154. Ternary Label Source

A ternary label may be generated through a declared:

`P_T`

or supplied independently.

Its source mapping must be versioned.

---

## 155. Ternary Label Stability

If ternary labels depend on thresholds or hysteresis, those parameters are part of the dataset-labeling specification.

---

## 156. Transition Dataset

A transition dataset contains temporally or sequentially ordered ternary state information.

---

## 157. Transition Sample

A transition record may contain:

`(t_exec[k], t_target[k], t_pending[k], t_exec[k+1])`.

---

## 158. Allowed Transition Labels

Committed state transitions must belong to:

`-1 → -1`

`-1 → 0`

`0 → -1`

`0 → 0`

`0 → 1`

`1 → 0`

`1 → 1`.

---

## 159. Forbidden Transition Labels

Committed labels must exclude:

`-1 → 1`

and:

`1 → -1`.

---

## 160. Transition Dataset Validation

A transition dataset must be scanned for direct-opposite violations before training.

---

## 161. Scheduler Metadata

Execution-bound traces may include scheduler state.

Scheduler state is not ternary state.

---

## 162. FRP Scheduler Reference

Where FRP-derived execution data are used, scheduler modes:

`7/1`

and:

`1/7`

must remain explicitly identified.

---

## 163. FRP Data Scope

FRP-derived data represent executable reference specialization data.

They do not define the complete TR-EIP training domain.

---

## 164. FRP Ternary Kernel

Any FRP-derived ternary sample must preserve:

`-1/0/1`.

---

## 165. FRP Active Neutral

FRP-derived state:

`0`

must remain a valid active class.

---

## 166. FRP Phase Data

FRP-derived phase traces may include:

- `theta`;
- retained frequency;
- phase order;
- target state;
- executed state;
- scheduler state.

---

## 167. FRP Phase Order

FRP phase order is:

`R = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

The distinction remains:

`R(t) ≠ C(t)`.

---

## 168. FRP Threshold Data

Where the FRP phase-to-target classifier is represented, the threshold magnitude:

`0.33`

must be identified as FRP-specific.

---

## 169. FRP Nominal Lag

If phase-coupling metadata are included, the FRP specialization value:

`gamma_nominal = 0.30 pi`

must remain FRP-specific.

---

## 170. FRP Coupling Baseline

If included:

`K_0 = 0.28`

must remain FRP-specific.

---

## 171. Data Augmentation

Training data may be augmented through transformations that preserve model semantics.

---

## 172. Translation Augmentation

For internal isolated configurations:

`R' = R + c`.

Energy labels remain unchanged.

Forces remain unchanged.

Relative geometry remains unchanged.

---

## 173. Rotation Augmentation

For:

`R' = QR`:

- scalar energy remains unchanged;
- force rotates;
- stress transforms as a tensor;
- scalar ternary channels remain unchanged.

---

## 174. Reflection Augmentation

Reflection augmentation is valid only when the model and source physics support the declared reflection symmetry.

---

## 175. Permutation Augmentation

Species-preserving permutation changes atom ordering while preserving physical state.

Per-atom labels must permute consistently.

---

## 176. Periodic Image Augmentation

Equivalent periodic images may provide consistency tests.

They should not be counted as independent physical samples without an explicit policy.

---

## 177. Augmentation Provenance

Generated augmented samples should retain linkage to their source sample.

---

## 178. Augmentation Split Inheritance

Augmented samples should inherit source split under strict leakage control.

---

## 179. Augmentation Weight

Generated symmetry copies may be reweighted to avoid unintended overrepresentation.

---

## 180. Noise Augmentation

Numerical or physical noise may be added to selected inputs or labels.

The noise distribution and intended semantics must be explicit.

---

## 181. Coordinate Noise

Coordinate perturbation changes the configuration.

It is not a symmetry transformation.

Targets may need recomputation.

---

## 182. Label Noise

Perturbing labels creates synthetic supervision uncertainty.

This must be explicit.

---

## 183. Symmetry Augmentation versus Physical Perturbation

The distinction remains:

`symmetry transform ≠ physical perturbation`.

---

## 184. Dataset Serialization

A serialized sample must preserve enough information to reconstruct:

- atomic configuration;
- target values;
- units;
- masks;
- provenance;
- split;
- identifiers.

---

## 185. Configuration Serialization

Configuration serialization must preserve:

- species order;
- positions;
- cell;
- periodicity;
- units.

---

## 186. Force Serialization

Force arrays must preserve the same atom ordering as positions.

---

## 187. Stress Serialization

Stress serialization must preserve tensor convention.

---

## 188. Ternary Serialization

Ternary fields must restrict valid values exactly to:

`-1`

`0`

`1`.

---

## 189. Optional Ternary Field

An absent ternary field must be represented using optional-field semantics, not numeric zero.

---

## 190. Dataset Schema

A dataset schema should define:

- required fields;
- optional fields;
- data types;
- shapes;
- units;
- masks;
- valid categorical states.

---

## 191. Shape Validation

For:

`N`

atoms:

- positions must have `N` atomic entries;
- forces must have `N` vector entries when present;
- species must have `N` entries.

---

## 192. Cell Validation

A periodic sample must contain a valid cell matrix.

---

## 193. Finite-Value Validation

Continuous numeric reference fields must be checked for:

- NaN;
- infinity;
- malformed values.

---

## 194. Unit Validation

Unit metadata must be present or inherited from a declared dataset-level unit system.

---

## 195. Ternary Domain Validation

Every ternary label must satisfy:

`t ∈ {-1,0,1}`.

---

## 196. Transition Validation

Every consecutive executed-state pair must respect the canonical transition graph.

---

## 197. Symmetry Validation

Selected samples may be transformed to verify that labels obey the declared transformation laws.

---

## 198. Energy Rotation Validation

Energy must remain invariant under rigid rotation.

---

## 199. Force Rotation Validation

Force must transform by:

`Q`.

---

## 200. Stress Rotation Validation

Stress must transform by:

`Q Sigma Q^T`.

---

## 201. Permutation Validation

Per-atom targets must permute consistently.

Global scalar targets must remain invariant.

---

## 202. Periodic Equivalence Validation

Equivalent periodic representations must produce equivalent reference semantics where the source method is periodic.

---

## 203. Dataset Consistency Check

A dataset consistency pass may verify:

- target shapes;
- units;
- split membership;
- duplicates;
- finite values;
- symmetry behavior;
- transition invariants.

---

## 204. Data Quality Score

A dataset may attach a quality score.

The score definition must be explicit.

---

## 205. Quality Score versus Training Weight

A quality score may influence sample weighting.

The mapping from score to weight must be separately defined.

---

## 206. Data Rejection

Rejected samples must remain traceable when reproducibility requires auditability.

---

## 207. Data Retention

A dataset may retain rejected records in a quarantine or excluded set.

This is distinct from the active training split.

---

## 208. Training Dataset

`D_train`

contains the samples used to compute training losses.

---

## 209. Validation Dataset

`D_val`

contains samples used for model selection and training diagnostics.

---

## 210. Test Dataset

`D_test`

contains samples used for the declared test evaluation.

---

## 211. Benchmark Dataset

A separate:

`D_bench`

may be used for performance benchmarking.

Benchmark data need not overlap with scientific evaluation splits.

---

## 212. Calibration Dataset

A separate:

`D_cal`

may be used for calibration of selected parameters or uncertainty models.

---

## 213. Calibration versus Validation

Calibration data influence fitted calibration parameters.

Validation data evaluate model selection or generalization under the declared protocol.

---

## 214. Dataset Hierarchy

A complete data system may contain:

`D_source`

`→ D_clean`

`→ D_normalized`

`→ D_split`

`→ D_train / D_val / D_test`.

---

## 215. Source Dataset

`D_source`

contains imported or generated raw reference data.

---

## 216. Clean Dataset

`D_clean`

contains validated and corrected source records.

---

## 217. Normalized Dataset

`D_normalized`

contains training-ready units and numerical scaling metadata.

---

## 218. Split Dataset

`D_split`

contains immutable split assignments.

---

## 219. Data Lineage

Every processed dataset should be traceable back to its source artifact.

---

## 220. Transformation Log

A transformation log may record:

- filtering;
- unit conversion;
- normalization;
- augmentation;
- split assignment;
- label derivation.

---

## 221. Reproducible Data Preparation

A reproducible preparation pipeline must define deterministic transformation steps or explicit random state.

---

## 222. Data Preparation Seed

Any stochastic preparation operation must store its seed and algorithm.

---

## 223. Parallel Data Processing

Parallel processing must preserve deterministic sample identity and transformation semantics when exact reproducibility is required.

---

## 224. Ordering

Dataset ordering is computational metadata.

Training samplers may reorder samples without changing dataset identity.

---

## 225. Canonical Ordering

Canonical ordering may be useful for byte-identical manifests or deterministic preprocessing.

---

## 226. Sharding

Large datasets may be partitioned into shards.

Sharding must not alter sample semantics.

---

## 227. Shard Identifier

Each shard should be traceable in the dataset manifest.

---

## 228. Compression

Serialized datasets may use compression.

Compression must preserve the required numerical fidelity.

---

## 229. Lossless Compression

Lossless compression preserves serialized values exactly.

---

## 230. Lossy Compression

Lossy compression changes numerical data.

Its error bounds must be explicit if used.

---

## 231. Quantized Dataset

Coordinates or targets may be quantized for specialized implementations.

Quantization error becomes part of the data artifact.

---

## 232. Quantization versus Ternary State

The distinction remains:

`numeric quantization ≠ semantic ternary mapping`.

---

## 233. Data Precision

Each continuous field should define numerical precision.

---

## 234. Position Precision

Coordinate precision may affect graph construction near cutoff boundaries.

---

## 235. Force Precision

Reference-force precision influences achievable loss floor.

---

## 236. Energy Precision

Reference-energy precision influences target resolution.

---

## 237. Stress Precision

Stress precision may differ from energy/force precision.

---

## 238. Reference Noise Floor

Reference numerical uncertainty may establish a practical lower error scale for supervised fitting.

---

## 239. Data Coverage

Training coverage should be described in the state variables relevant to the model.

---

## 240. Geometric Coverage

Coverage may include distributions of:

- pair distance;
- coordination;
- local density;
- bond-angle-like geometry;
- cell strain.

---

## 241. Energy Coverage

Energy distribution may be reported relative to a declared reference.

---

## 242. Force Coverage

Force-magnitude distribution may identify high-force regions.

---

## 243. Stress Coverage

Stress-state distribution may identify mechanical coverage.

---

## 244. Resonance Coverage

Resonance-state coverage may be characterized in:

`X_R`.

---

## 245. Ternary Coverage

Ternary coverage may report occupancy of:

`-1`

`0`

`1`.

---

## 246. Transition Coverage

Execution-bound data should report counts of:

- retention;
- first-leg transitions;
- second-leg transitions;
- neutral residence;
- opposite-route requests.

---

## 247. Direct-Opposite Count

The committed direct-opposite count must be:

`0`

for conforming execution data.

---

## 248. Domain Coverage versus Validation

Coverage statistics describe the dataset.

They remain distinct from model validation metrics.

---

## 249. Data Extension Rule

Any new dataset must define:

1. source;
2. identifier;
3. version;
4. species;
5. configuration fields;
6. targets;
7. units;
8. provenance;
9. split;
10. quality policy;
11. preparation pipeline;
12. validation.

---

## 250. Energy-Target Extension Rule

Any new energy target must define:

1. total or local semantics;
2. units;
3. reference zero;
4. source method;
5. uncertainty where available.

---

## 251. Force-Target Extension Rule

Any new force target must define:

1. atom ordering;
2. vector units;
3. source method;
4. convergence;
5. transformation behavior.

---

## 252. Stress-Target Extension Rule

Any new stress target must define:

1. tensor type;
2. component order;
3. sign;
4. units;
5. normalization;
6. reference method.

---

## 253. Resonance-Target Extension Rule

Any resonance target must define:

1. state space;
2. coordinate semantics;
3. transformation law;
4. units;
5. scale;
6. provenance.

---

## 254. Ternary-Target Extension Rule

Any ternary target dataset must define:

1. source mapping;
2. target or executed semantics;
3. exact `-1/0/1` domain;
4. active-neutral handling;
5. hysteresis/persistence where used;
6. validation.

---

## 255. Transition-Data Extension Rule

Any execution-transition dataset must define:

1. state ordering;
2. target;
3. executed state;
4. pending state;
5. scheduler state;
6. timing coordinate;
7. direct-opposite validation.

---

## 256. Split Extension Rule

Any split protocol must define:

1. grouping unit;
2. random state where used;
3. target fractions or counts;
4. duplicate policy;
5. leakage policy;
6. immutable membership artifact.

---

## 257. Normalization Extension Rule

Any normalization must define:

1. source split;
2. statistic;
3. transformation;
4. inverse transformation;
5. units;
6. stored parameters.

---

## 258. Canonical Training-Data Invariants

Every conforming training dataset preserves:

1. explicit atomic configuration;

2. explicit target typing;

3. explicit units;

4. explicit provenance;

5. explicit split membership;

6. explicit missing/invalid handling;

7. explicit transformation semantics;

8. explicit preparation lineage.

---

## 259. Canonical Ternary Data Invariants

Any ternary training data preserve:

`-1/0/1`.

The state:

`0`

remains active neutral.

Missing, invalid, masked, padded, and out-of-domain states remain separate.

---

## 260. Canonical Execution-Data Invariants

Any execution dataset preserves:

`target ≠ executed state`

and:

`pending ≠ neutral`.

Committed direct:

`-1 → 1`

and:

`1 → -1`

remain absent.

---

## 261. Canonical Mechanical Data Invariants

Energy remains scalar.

Force remains vector.

Stress remains tensor.

Their units and transformation laws remain explicit.

---

## 262. Canonical Symmetry Data Invariants

Rigid transformations preserve reference semantics:

`energy → invariant`

`force → equivariant`

`stress → tensor transformed`

`scalar ternary → invariant`.

---

## 263. Canonical State-Separation Invariants

The data layer preserves:

`dataset label ≠ model state by identity`

`mask ≠ ternary neutral`

`quality flag ≠ ternary state`

`uncertainty ≠ ternary state`

`graph edge label ≠ chemical bond unless explicitly defined`

`trajectory step ≠ training step`.

---

## 264. Canonical Scientific Distinctions

The data layer preserves:

`graph density ≠ material density`

`resonance class ≠ ternary state`

`phase order ≠ coherence`

`R(t) ≠ C(t)`

`phase coupling ≠ mechanical force`

`ternary state ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`.

---

## 265. Canonical Data Pipeline

The complete data pipeline is:

`source data`

`→ provenance assignment`

`→ validation`

`→ unit harmonization`

`→ cleaning`

`→ duplicate handling`

`→ normalization`

`→ split assignment`

`→ training-ready dataset`.

---

## 266. Canonical Supervision Chain

For one sample:

`configuration`

`+ reference targets`

`→ model prediction`

`→ typed residual`

`→ loss contribution`.

---

## 267. Canonical Augmentation Chain

For symmetry augmentation:

`source sample`

`→ symmetry transform`

`→ transformed labels`

`→ inherited split`

`→ augmented sample`.

---

## 268. Interface to Chapter 03

Chapter 03 develops Loss Functionals.

It consumes the typed training-data fields defined here and constructs:

- energy loss;
- force loss;
- stress loss;
- resonance loss;
- ternary loss;
- multi-objective loss.

---

## 269. Interface to Chapter 04

Chapter 04 develops Energy-Force-Stress Training.

It uses consistent joint reference data for mechanical derivative supervision.

---

## 270. Interface to Chapter 05

Chapter 05 develops Ternary Regularization.

It uses ternary occupancy and transition statistics derived from the data layer.

---

## 271. Interface to Chapter 06

Chapter 06 develops Resonance Regularization.

It uses resonance coordinates, windows, and reference-state coverage.

---

## 272. Interface to Chapter 07

Chapter 07 develops Equivariance Constraints.

It uses symmetry-transformed sample pairs and expected transformation laws.

---

## 273. Interface to Chapter 08

Chapter 08 develops Uncertainty and Domain Detection.

It uses dataset coverage, density, split structure, and provenance.

---

## 274. Interface to Chapter 09

Chapter 09 develops Optimization.

It consumes batched, normalized, split-aware training data through the declared sampler and loader.

---

## 275. Final Formal Structure

The training-data layer may be represented as:

`TD = (D, S, Y, U, P, Q, A, N, Split, V)`.

Here:

- `D` is the configuration dataset;
- `S` is species and structural metadata;
- `Y` is reference target state;
- `U` is unit metadata;
- `P` is provenance;
- `Q` is quality metadata;
- `A` is augmentation state;
- `N` is normalization state;
- `Split` is immutable split assignment;
- `V` is dataset validation state.

A training sample is:

`d_k = (X_k, Y_k, M_k)`.

---

## 276. Final Statement

Training data form the reference layer connecting the TR-EIP model family to optimization.

Every training artifact must preserve explicit:

- atomic configuration;
- species;
- cell and periodicity;
- target type;
- units;
- provenance;
- split;
- quality state;
- transformation semantics;
- lineage.

Energy remains a scalar reference.

Force remains a per-atom vector reference.

Stress remains a tensor reference.

Resonance remains separately typed.

Ternary state remains exactly:

`-1/0/1`.

The state:

`0`

remains active neutral and must never be reused as a generic missing, invalid, masked, padded, or out-of-domain value.

Execution data preserve:

`target ≠ executed state`

and the committed graph:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain invalid dataset transitions.

The canonical training-data pipeline is:

`source`

`→ validate`

`→ normalize`

`→ split`

`→ supervise`

`→ optimize`.

These definitions establish the reference-data layer required for the Loss Functionals developed in Chapter 03.
