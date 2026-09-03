# Summary

## 1. Scope

Volume 04 defines the learning and optimization layer of the TR-EIP model family within TR-EIF.

The volume connects:

- model architecture;
- training data;
- loss functionals;
- energy-force-stress training;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty and domain detection;
- optimization.

The learning layer operates on explicitly typed physical, resonance, ternary, symmetry, uncertainty, and optimization variables.

It does not merge these state spaces.

---

## 2. Model Architecture

The model architecture defines the computational decomposition of the learning system.

The architecture may contain:

- atomic or entity representations;
- local-environment encoders;
- interaction modules;
- equivariant representations;
- resonance modules;
- ternary target modules;
- energy branches;
- force branches;
- stress branches;
- uncertainty modules;
- domain detectors.

Each module requires an explicit input-output contract.

---

## 3. Typed State Spaces

The learning architecture preserves separation among:

- atomic configuration space;
- latent representation space;
- resonance state space;
- ternary state space;
- mechanical output space;
- uncertainty state space;
- model-domain state;
- optimizer state.

A variable in one state space is not identified with a variable in another state space without an explicit mapping.

---

## 4. Training Data

Training data define the empirical input and reference layer.

Each sample must identify the available reference quantities and their semantic roles.

Possible reference fields include:

- atomic positions;
- atomic species;
- cell variables;
- energy;
- forces;
- stress;
- resonance variables;
- resonance classes;
- ternary targets;
- executed ternary states;
- uncertainty references;
- domain labels;
- masks;
- validity metadata.

---

## 5. Data Provenance

Training and validation data use explicit provenance.

The canonical provenance classes are:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 6. Missingness and Semantic States

Missingness, masks, padding, unknown values, invalid values, and non-finite numerical values remain outside the semantic ternary state space.

The framework preserves:

`MISSING ≠ 0`

`MASK ≠ 0`

`PADDING ≠ 0`

`UNKNOWN ≠ 0`

`INVALID ≠ 0`

`NaN ≠ 0`.

---

## 7. Loss Functionals

The optimization objective may combine multiple typed loss components.

A generic total objective may be written:

`L_total = sum_k lambda_k L_k`.

Each component:

`L_k`

must define:

- target variable;
- prediction variable;
- mathematical form;
- reduction;
- normalization;
- coefficient;
- units or dimensionless status;
- provenance.

---

## 8. Loss Coefficients

Each coefficient:

`lambda_k`

must be explicit.

A coefficient may be:

- fixed;
- scheduled;
- calibrated;
- trainable under a declared parameterization.

The coefficient is an optimization variable or parameter.

It is not a physical observable unless separately defined as such.

---

## 9. Energy Training

Energy training acts on scalar energy predictions.

For predicted energy:

`E_hat`

and reference:

`E_ref`

an energy loss may be defined through an explicit metric.

Energy remains a scalar quantity under the declared spatial symmetry group.

---

## 10. Force Training

Force training acts on vector-valued force predictions.

For entity:

`i`

the predicted force is:

`F_hat_i`.

Force transformation behavior must remain consistent with the declared equivariance contract.

---

## 11. Conservative Force Interface

Where the conservative branch is defined:

`F_i = -grad_(R_i) E`.

This relation is separate from direct force prediction.

---

## 12. Stress Training

Stress training acts on the declared stress tensor representation.

The stress convention must define:

- sign;
- tensor ordering;
- normalization;
- volume convention;
- cell relation;
- units.

---

## 13. Energy-Force-Stress Separation

The framework preserves:

`energy ≠ force`

`energy ≠ stress`

`force ≠ stress`.

Joint optimization does not remove these distinctions.

---

## 14. Conservativity and Equivariance

The framework preserves:

`equivariance ≠ conservativity`

`equivariance ≠ accuracy`

`conservativity ≠ accuracy`.

These properties require separate definitions and validation procedures.

---

## 15. Balanced Ternary State Space

The exact ternary semantic state space is:

`T = {-1,0,1}`.

The state:

`0`

is active neutral.

---

## 16. Active Neutral

The active-neutral state may participate in:

- mediation;
- balancing;
- routing;
- damping;
- transition staging;
- retention;
- controlled neutralization.

It is not a missing or undefined state.

---

## 17. Ternary Roles

The learning and execution interfaces distinguish:

`t_target`

`t_pending`

`t_exec`.

These variables have separate semantic roles.

The framework preserves:

`t_target ≠ t_pending`

`t_pending ≠ t_exec`

`t_target ≠ t_exec`.

---

## 18. Ternary Transition Graph

The canonical committed state graph is:

`-1 ↔ 0 ↔ 1`.

---

## 19. Forbidden Direct Opposite Transitions

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

are forbidden.

---

## 20. Neutral-Mediated Routes

Opposite-polarity execution uses:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each leg is a separate committed transition event.

The neutral state may persist between the two legs.

---

## 21. Ternary Regularization

Ternary regularization acts on differentiable training representations associated with ternary prediction.

It may constrain:

- logits;
- probabilities;
- margins;
- class occupancy;
- persistence;
- hysteresis;
- switching;
- transition proposals;
- resonance-to-ternary consistency.

---

## 22. Soft Representation and Semantic State

A differentiable ternary representation is not itself a semantic ternary state.

The framework preserves:

`soft ternary representation ≠ t_target`.

Semantic commitment occurs through an explicit decision mapping.

---

## 23. Ternary Regularization and Execution

A finite regularization penalty does not replace structural execution constraints.

The direct-opposite transition prohibition remains an execution invariant.

---

## 24. Resonance State Space

The resonance state space is:

`X_R`.

A resonance state is:

`r ∈ X_R`.

---

## 25. Resonance Window

A resonance window is:

`W_R ⊂ X_R`.

Its boundary is:

`∂W_R`.

---

## 26. Resonance Classification

A resonance classifier may assign:

`OUTSIDE`

`BOUNDARY`

or:

`INSIDE`.

These are resonance classes.

---

## 27. Resonance Classes and Ternary States

The framework preserves:

`OUTSIDE/BOUNDARY/INSIDE ≠ -1/0/1`.

Any mapping from resonance information to a ternary target must be explicit.

---

## 28. Resonance-to-Ternary Mapping

A resonance-to-ternary mapping may be represented as:

`P_RT: X_R × X_context → {-1,0,1}`.

The mapping must define:

- resonance input;
- context;
- scale;
- history dependence where used;
- decision rule;
- output target.

---

## 29. Resonance Regularization

Resonance regularization may act on:

- resonance coordinates;
- resonance windows;
- boundary geometry;
- persistence;
- hysteresis;
- multiscale relations;
- resonance-to-ternary mappings;
- symmetry constraints.

---

## 30. Resonance Persistence

Persistence requires an explicitly ordered sequence.

The sequence may be defined by:

- physical time;
- simulation step;
- execution tact;
- another declared index.

The sequence index must not be identified with physical time unless an explicit mapping defines that relation.

---

## 31. Resonance Hysteresis

A hysteretic resonance classifier requires explicit history-dependent state or thresholds.

Entry and exit conditions remain separately defined.

---

## 32. Multiscale Resonance

Resonance variables may exist at several scales.

A scale-indexed resonance state may be written:

`r^(ell) ∈ X_R^(ell)`.

Cross-scale consistency requires an explicit mapping.

---

## 33. Resonance Distinctions

The framework preserves:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`.

---

## 34. Transition Distinctions

The framework preserves:

`resonance-window crossing ≠ bifurcation`

`resonance-window crossing ≠ ternary transition`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 35. Physical Distinctions

The framework preserves:

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`

`ternary state ≠ force`

`resonance classification ≠ energy`.

---

## 36. Symmetry Group

Let:

`G`

denote the declared symmetry group.

For:

`g ∈ G`

the input transformation is:

`rho_X(g)`.

---

## 37. Equivariance

A mapping:

`F: X → Y`

is equivariant when:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

---

## 38. Invariance

An invariant mapping satisfies:

`F(rho_X(g)x) = F(x)`.

---

## 39. Group Selection

The symmetry contract must explicitly identify the applicable group or subgroup.

Possible examples include:

`SO(3)`

`O(3)`

`SE(3)`

`E(3)`

and species-preserving permutation groups.

These groups are not interchangeable.

---

## 40. Scalar, Vector, and Tensor Types

Every geometric quantity must have a declared transformation type.

The learning architecture may contain:

- invariant scalars;
- polar vectors;
- axial vectors;
- tensors;
- irreducible representations;
- permutation-indexed quantities.

---

## 41. Energy Symmetry

Scalar energy remains invariant under the declared admissible rigid transformations when the physical model contains no untransformed symmetry-breaking input.

---

## 42. Force Symmetry

Force transforms as a polar vector under the declared spatial transformation.

---

## 43. Stress Symmetry

Stress transforms according to its declared second-order tensor law.

---

## 44. Permutation Symmetry

Per-entity quantities permute with their corresponding entities.

Permutation-invariant global quantities remain unchanged under admissible species-preserving relabeling.

---

## 45. Graph Equivariance

Graph-based representations must preserve consistency under admissible node permutation.

Neighbor aggregation must follow an explicitly permutation-compatible rule.

---

## 46. Latent Equivariance

Latent features must retain their declared representation types throughout:

- linear mappings;
- tensor products;
- nonlinearities;
- gating;
- normalization;
- aggregation;
- residual connections.

---

## 47. Ternary Symmetry

Scalar ternary values:

`-1/0/1`

are semantic states.

They are not spatial vectors.

---

## 48. Spatial Transformations and Ternary Polarity

The framework preserves:

`spatial rotation ≠ ternary polarity reversal`

and:

`spatial reflection ≠ ternary polarity reversal`

unless an independent semantic transformation is explicitly defined.

---

## 49. Resonance Symmetry

Every resonance quantity must declare whether it is:

- invariant;
- equivariant;
- tensorial;
- permutation-indexed.

Resonance windows and classifiers must use compatible transformation rules.

---

## 50. Architectural and Soft Equivariance

The framework distinguishes:

- architectural equivariance;
- symmetry augmentation;
- soft symmetry penalties;
- numerical symmetry validation.

These mechanisms remain separately represented.

---

## 51. Uncertainty State Space

Let:

`U`

denote the uncertainty state space.

An uncertainty value:

`u ∈ U`

must identify its target quantity and mathematical representation.

---

## 52. Prediction and Uncertainty

The framework preserves:

`prediction ≠ uncertainty`.

---

## 53. Uncertainty and Error

The framework preserves:

`uncertainty ≠ realized error`.

---

## 54. Epistemic Uncertainty

Epistemic uncertainty is associated with the declared model-knowledge or support representation.

---

## 55. Aleatoric Uncertainty

Aleatoric uncertainty is associated with the conditional variability represented by the predictive model.

---

## 56. Uncertainty Decomposition

Where both components are used:

`u_epi`

and:

`u_ale`

remain separately typed.

Any total uncertainty composition must be explicit.

---

## 57. Model Domain

Let:

`D_M`

denote the declared model domain.

A basic domain state space may be:

`{IN_DOMAIN, OUT_OF_DOMAIN}`.

A domain boundary state may be added explicitly.

---

## 58. Domain Score

A domain detector may expose:

`s_D(X)`.

A hard domain class is obtained only through a declared decision rule.

---

## 59. Domain Status and Uncertainty

The framework preserves:

`domain state ≠ uncertainty`.

---

## 60. Domain Status and Accuracy

The framework preserves:

`IN_DOMAIN ≠ accurate`

and:

`OUT_OF_DOMAIN ≠ incorrect`.

---

## 61. Domain and Resonance Separation

The framework preserves:

`OUT_OF_DOMAIN ≠ OUTSIDE resonance window`

`IN_DOMAIN ≠ INSIDE resonance window`

`DOMAIN_BOUNDARY ≠ BOUNDARY resonance class`

`∂D_M ≠ ∂W_R`.

---

## 62. Domain and Ternary Separation

The framework preserves:

`OUT_OF_DOMAIN ≠ ternary 0`

`IN_DOMAIN ≠ ternary 1`

`DOMAIN_BOUNDARY ≠ ternary 0`.

---

## 63. Selective Prediction

A selective prediction policy may define:

`A(X) ∈ {ACCEPT, REJECT}`.

Acceptance remains separate from:

- domain status;
- uncertainty;
- ternary state.

---

## 64. Calibration

Calibration relates predicted confidence or probability to observed outcomes under a declared calibration protocol.

The framework preserves:

`calibration ≠ accuracy`.

---

## 65. Risk and Coverage

Selective prediction may define:

- coverage;
- selective risk;
- risk-coverage curves.

The exact task loss and acceptance rule must be declared.

---

## 66. Active Learning

Uncertainty and domain detection may provide signals for active-learning acquisition.

An acquisition score may depend on:

- uncertainty;
- domain score;
- representation novelty;
- resonance coverage;
- ternary-state coverage;
- transition coverage;
- structural diversity.

---

## 67. Active Learning Separation

The framework preserves:

`active-learning acquisition ≠ physical dynamics`

and:

`active-learning acquisition ≠ ternary transition`.

---

## 68. Optimization Variables

Let:

`Theta`

denote trainable model parameters.

The optimization problem may be written:

`Theta* = argmin_Theta L_total(Theta)`.

---

## 69. Composite Objective

A general objective may include:

`L_total = L_mech + L_ternary + L_resonance + L_equivariance + L_uncertainty + L_regularization`.

Each component must remain separately identifiable.

---

## 70. Mechanical Objective

The mechanical objective may include:

- energy loss;
- force loss;
- stress loss;
- consistency terms.

---

## 71. Ternary Objective

The ternary objective may include:

- classification loss;
- state-concentration terms;
- transition penalties;
- persistence;
- hysteresis;
- switching constraints.

---

## 72. Resonance Objective

The resonance objective may include:

- coordinate regularization;
- window regularization;
- boundary regularization;
- persistence;
- hysteresis;
- multiscale consistency;
- resonance-to-ternary consistency.

---

## 73. Equivariance Objective

The equivariance objective may contain numerical residuals where symmetry is not fully guaranteed by architecture.

---

## 74. Uncertainty Objective

The uncertainty objective may contain:

- likelihood terms;
- calibration terms;
- variance objectives;
- domain-detector objectives;
- selective-prediction terms.

---

## 75. Optimization State

Optimizer internal variables remain separate from model state.

Examples include:

- momentum;
- adaptive first moments;
- adaptive second moments;
- learning-rate schedules.

---

## 76. Optimizer Memory and Physical Memory

The framework preserves:

`optimizer memory ≠ physical memory`

`optimizer momentum ≠ mechanical momentum`

`optimizer state ≠ resonance history`.

---

## 77. Training Stage

A training procedure may define multiple stages.

A training-stage transition is an optimization-control event.

---

## 78. Training Stage and Ternary Transition

The framework preserves:

`training-stage transition ≠ ternary-state transition`.

---

## 79. Training Stage and Physical Transition

The framework preserves:

`training-stage transition ≠ physical phase transition`.

---

## 80. Classifier Temperature

A classifier may use a temperature parameter.

The framework preserves:

`classifier temperature ≠ thermodynamic temperature`.

---

## 81. Learning Rate

The learning rate is an optimizer parameter.

It is not a physical rate unless a separate mapping is explicitly defined.

---

## 82. Gradient

A gradient in parameter space is an optimization quantity.

It is distinct from a spatial gradient used in a physical derivative.

---

## 83. Gradient Conflict

Different objective components may generate non-aligned parameter gradients.

The framework preserves:

`optimization gradient conflict ≠ physical opposition`.

---

## 84. Constraints

Optimization constraints may be enforced through:

- architecture;
- parameterization;
- projection;
- constrained optimization;
- finite penalties.

The selected mechanism must be explicit for each constraint.

---

## 85. Hard and Soft Constraints

The framework distinguishes:

- hard structural constraints;
- soft finite penalties.

A finite penalty does not redefine an exact invariant.

---

## 86. Exact Ternary Execution Constraint

The direct-opposite transition prohibition is an exact committed execution constraint.

It must not depend only on finite regularization strength.

---

## 87. Exact Symmetry Constraints

Architectural equivariance may enforce exact transformation structure up to arithmetic implementation effects.

Soft symmetry losses remain separate optimization terms.

---

## 88. Parameter Constraints

Trainable constrained parameters may include:

- positive widths;
- ordered hysteresis thresholds;
- bounded coefficients;
- normalized distributions;
- symmetry-compatible tensors.

Their admissible parameterization must be explicit.

---

## 89. Numerical Precision

Training and inference may use:

- floating-point arithmetic;
- mixed precision;
- fixed-point arithmetic;
- quantization.

Arithmetic behavior forms part of the implementation contract.

---

## 90. Numerical Precision and Semantics

Finite arithmetic does not redefine:

- ternary states;
- resonance classes;
- domain classes;
- symmetry transformation laws.

---

## 91. Determinism

Deterministic replay may be defined under fixed:

- input;
- parameters;
- arithmetic;
- execution order;
- random seed;
- hardware or software execution contract.

---

## 92. Determinism and Correctness

The framework preserves:

`determinism ≠ correctness`.

---

## 93. Determinism and Equivariance

The framework preserves:

`determinism ≠ equivariance`.

---

## 94. Determinism and Physical Validation

The framework preserves:

`deterministic replay ≠ physical validation`.

---

## 95. Validation Layers

The learning and optimization layer requires separately typed validation for:

- data;
- energy;
- force;
- stress;
- ternary semantics;
- ternary execution;
- resonance;
- equivariance;
- uncertainty;
- domain detection;
- optimization;
- numerical stability.

---

## 96. Ternary Validation

Ternary validation includes:

- valid semantic states;
- target typing;
- pending typing;
- executed-state typing;
- direct-opposite event count;
- neutral-mediated route integrity;
- active-neutral handling.

---

## 97. Resonance Validation

Resonance validation includes:

- coordinate behavior;
- window occupancy;
- boundary relations;
- crossing counts;
- persistence;
- hysteresis;
- multiscale consistency;
- resonance-to-ternary mapping.

---

## 98. Equivariance Validation

Equivariance validation includes transformed fixtures for:

- translation;
- rotation;
- reflection where declared;
- permutation;
- periodic representations where applicable.

---

## 99. Uncertainty Validation

Uncertainty validation may include:

- calibration;
- interval coverage;
- error-versus-uncertainty statistics;
- task-specific uncertainty metrics.

---

## 100. Domain Validation

Domain detection validation may include:

- in-domain classification;
- out-of-domain classification;
- boundary classification where defined;
- threshold sensitivity;
- task-specific domain detection.

---

## 101. Selective Prediction Validation

Selective prediction validation may include:

- coverage;
- selective risk;
- acceptance counts;
- rejection counts;
- risk-coverage relations.

---

## 102. Provenance of Validation Results

Measured validation results use:

`BENCHMARK`

when produced under a declared benchmark protocol.

Synthetic cases used only for verification use:

`TEST_FIXTURE`.

Unsupported empirical claims require:

`REQUIRES_TEST`.

---

## 103. Interface to Molecular Dynamics

The output of Volume 04 supplies trained model components and typed prediction interfaces to the molecular-dynamics layer.

The interface may include:

- energy;
- force;
- stress;
- resonance state;
- resonance classification;
- ternary targets;
- uncertainty;
- domain state.

---

## 104. Mechanical Dynamics Boundary

Molecular-dynamics evolution is defined by its own equations of motion and numerical integration scheme.

The learning objective is not the equation of motion.

---

## 105. Optimization Step and Dynamics Step

The framework preserves:

`optimization step ≠ molecular-dynamics integration step`.

---

## 106. Learning State and Physical State

The framework preserves:

`optimizer state ≠ physical system state`.

---

## 107. Final Formal Structure

The complete Volume 04 layer may be represented as:

`L_OPT = (A_M, D_TR, L, R_T, R_R, EQ, UD, OPT, V)`.

Here:

- `A_M` is the model architecture;
- `D_TR` is the training-data contract;
- `L` is the loss-functional system;
- `R_T` is ternary regularization;
- `R_R` is resonance regularization;
- `EQ` is the equivariance constraint system;
- `UD` is the uncertainty and domain-detection system;
- `OPT` is the optimization procedure;
- `V` is the validation interface.

The complete optimization objective may be written:

`Theta* = argmin_Theta L_total(Theta)`.

The learned parameter set:

`Theta*`

does not replace the semantic state definitions established elsewhere in TR-EIF.

---

## 108. Final State-Space Separation

The following spaces remain distinct:

`X_atomic`

`X_latent`

`X_R`

`T = {-1,0,1}`

`X_mechanical`

`U`

`D_M`

`X_optimizer`.

Mappings among them must be explicitly defined.

---

## 109. Final Ternary Invariants

The semantic kernel remains:

`-1/0/1`.

The state:

`0`

remains active neutral.

The framework preserves:

`t_target ≠ t_pending`

`t_pending ≠ t_exec`

`t_target ≠ t_exec`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

The opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 110. Final Resonance Invariants

The resonance layer preserves:

`r ∈ X_R`

`W_R ⊂ X_R`

and:

`∂W_R`.

The resonance classes:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

remain separate from:

`-1/0/1`.

---

## 111. Final Symmetry Invariants

The declared symmetry group:

`G`

acts through explicit representations.

The defining equivariance relation remains:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

Scalar invariants remain invariant.

Vectors and tensors transform according to their declared representations.

---

## 112. Final Uncertainty and Domain Invariants

The framework preserves:

`uncertainty ≠ error`

`confidence ≠ accuracy`

`calibration ≠ accuracy`

`domain state ≠ uncertainty`

`OUT_OF_DOMAIN ≠ OUTSIDE resonance window`

`domain state ≠ ternary state`

`uncertainty ≠ ternary state`.

---

## 113. Final Semantic Boundary

The learning and optimization layer does not redefine:

- physical state;
- resonance state;
- ternary state;
- symmetry type;
- uncertainty state;
- domain state.

It provides trainable mappings, objectives, constraints, and validation interfaces connecting these explicitly defined structures.

---

## 114. Volume Closure

Volume 04 establishes the learning and optimization formalism of the TR-EIP model family within TR-EIF for use by subsequent TR-EIF volumes.

Its interfaces provide:

- trained mechanical mappings;
- resonance-conditioned representations;
- ternary target generation;
- equivariant outputs;
- uncertainty estimates;
- domain-state outputs;
- optimization metadata;
- validation traces.

The next volume defines the molecular-dynamics layer and its equations of motion, integration procedures, thermodynamic control interfaces, conservation analysis, long-time stability, and resonance-driven dynamics.
