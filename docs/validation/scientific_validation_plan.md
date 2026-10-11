# Scientific Validation Plan

## 1. Scope

This document defines the repository-level scientific validation plan of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The plan defines procedures for validating scientific claims across:

- mathematical contracts;
- resonance dynamics;
- balanced ternary dynamics;
- E(3)-equivariant interatomic modeling;
- conservative energy;
- force and stress derivation;
- molecular dynamics;
- multiscale mappings;
- FLiBe material specialization;
- experimental reference data;
- first-principles reference data;
- benchmarks;
- reproducibility artifacts.

This document defines validation requirements.

It does not assert that every validation target described here has already been completed.

Validation status is established only by the corresponding committed evidence.

---

## 2. Validation Principle

Scientific validation requires correspondence between a declared claim and evidence capable of testing that claim.

The basic relation is:

`claim`

`→ assumptions`

`→ observable or invariant`

`→ validation procedure`

`→ evidence`

`→ validation status`

A validation result is invalid when the tested observable does not correspond to the declared claim.

Similarity is not identity.

Numerical resemblance is not model equivalence.

---

## 3. Validation State Is Separate

Validation state is not part of the balanced ternary execution state.

Therefore:

`PASS ≠ 1`

`FAIL ≠ -1`

`UNRESOLVED ≠ 0`

`NOT_EVALUATED ≠ 0`

Active neutral state `0` remains a ternary execution state.

It must not encode validation status.

---

## 4. Claim Classes

TR-EIF distinguishes multiple claim classes.

A claim may be:

- mathematical;
- architectural;
- executable;
- numerical;
- symmetry-related;
- conservation-related;
- material-specific;
- thermodynamic;
- transport-related;
- experimental-comparison;
- first-principles-comparison;
- benchmark-related;
- reproducibility-related.

Each claim class requires a matching validation method.

---

## 5. Mathematical Claim Boundary

A mathematical claim requires mathematical evidence.

Examples include:

- theorem;
- lemma;
- corollary;
- existence statement;
- uniqueness statement;
- boundedness result;
- invariant proof.

A passing executable test does not replace a mathematical proof when the claim itself is mathematical.

Therefore:

`test pass ≠ theorem proof`

---

## 6. Executable Claim Boundary

An executable claim concerns implemented behavior.

Examples include:

- parser behavior;
- transition guard behavior;
- deterministic replay;
- E(3) transformation behavior;
- energy evaluation;
- force evaluation;
- schema validation;
- trace serialization.

Executable claims require direct execution against committed implementation.

---

## 7. Numerical Claim Boundary

A numerical claim concerns behavior of a numerical approximation.

Examples include:

- convergence rate;
- finite-difference consistency;
- integration stability;
- energy drift;
- discretization error;
- tolerance sensitivity.

Numerical claims require explicit numerical parameters and fixed acceptance criteria.

---

## 8. Physical Claim Boundary

A physical claim concerns a physical observable or physical relation.

Examples include:

- density;
- viscosity;
- thermal conductivity;
- diffusion;
- structure factor;
- coordination observable;
- thermodynamic property;
- transport property.

Physical claims require physical provenance.

Synthetic test values do not establish physical validity.

---

## 9. Material Claim Boundary

A claim about a specific material requires evidence for that material and applicable state domain.

For FLiBe, material validation must identify at least:

- composition;
- temperature;
- pressure when applicable;
- physical state;
- observable;
- unit;
- source;
- provenance class;
- applicable range.

---

## 10. Evidence Classes

The canonical provenance classes are:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

These classes describe evidence provenance.

They are not ternary states.

---

## 11. Primary-Source Evidence

`PRIMARY_SOURCE` applies only when the cited source directly supports the referenced datum or claim under the recorded conditions.

A publication must not receive blanket primary-source status for quantities it does not directly report.

---

## 12. Derived Evidence

`DERIVED` applies when a quantity is calculated from source-backed quantities through an explicit transformation.

A derived quantity must retain:

- source dependencies;
- transformation;
- units;
- domain;
- assumptions.

---

## 13. Calibrated Evidence

`CALIBRATED` identifies quantities obtained through an explicit calibration procedure.

Calibration must declare:

- calibration data;
- calibration objective;
- parameter set;
- applicable domain;
- validation separation.

Calibration data and validation data must not be silently merged.

---

## 14. Author-Defined Evidence

`AUTHOR_DEFINED` identifies a declared mathematical or computational construction introduced by the framework author.

It must not be presented as experimentally measured or first-principles derived unless such evidence exists separately.

---

## 15. Benchmark Evidence

`BENCHMARK` identifies fixed evaluation fixtures or performance/correctness benchmark artifacts.

Benchmark outputs establish only the benchmarked property under the benchmark contract.

They do not automatically establish physical accuracy.

---

## 16. Test-Fixture Evidence

`TEST_FIXTURE` identifies synthetic data constructed solely to test execution semantics.

A test fixture must not be cited as physical material evidence.

---

## 17. Requires-Source State

`REQUIRES_SOURCE` means that a scientific quantity or claim lacks sufficient source provenance for source-backed use.

It is not a ternary state.

---

## 18. Requires-Test State

`REQUIRES_TEST` means that an executable or numerical assertion requires qualification before it can be treated as validated implementation behavior.

It is not a ternary state.

---

## 19. Validation Target Declaration

Every scientific validation target must declare:

- target identifier;
- claim;
- claim class;
- applicable assumptions;
- input domain;
- expected observable;
- evidence source;
- comparison relation;
- acceptance criterion;
- provenance;
- validation output.

---

## 20. Acceptance Criteria

An acceptance criterion must be fixed before evaluation.

It must not be chosen after inspecting the result.

Therefore:

`acceptance threshold selected after result ≠ valid qualification`

A numerical tolerance requires a numerical reason.

It must not exist solely to turn a failing result into a passing result.

---

## 21. Exact Equality

Exact equality is used when the contract requires identity.

Examples may include:

- balanced-ternary states;
- enum values;
- deterministic structured output;
- schema fields;
- state cardinality;
- exact routing semantics;
- canonical ordering;
- byte-deterministic benchmark output.

Where exact equality is required, tolerance-based comparison must not replace it.

---

## 22. Numerical Equivalence

Numerical equivalence may use a fixed tolerance when floating-point or discretization behavior makes exact equality inappropriate.

The validation record must retain:

- tolerance;
- quantity;
- unit;
- comparison method;
- numerical method.

---

## 23. Structural Equality

Structural equality concerns typed organization rather than numerical closeness.

Examples include:

- graph cardinality;
- tensor dimensions;
- schema shape;
- trace structure;
- model-manifest structure;
- node ordering.

Structural validation must remain separate from physical accuracy.

---

## 24. Semantic Equality

Two objects are semantically identical only under a declared semantic identity relation.

Visual similarity or similar numerical magnitude does not establish semantic identity.

Therefore:

`similar ≠ identical`

---

## 25. Resonance Validation

Resonance validation must preserve the distinctions:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

A validation test must identify which quantity it actually measures.

---

## 26. Resonance State Validation

Executable resonance-state validation includes:

- nonempty phase vector;
- nonempty frequency vector;
- equal cardinality;
- finite values;
- phase normalization;
- deterministic state construction.

---

## 27. Resonance Descriptor Validation

Descriptor validation includes:

- phase-order calculation;
- frequency-spread calculation;
- coordinate dimensionality;
- finite coordinate values;
- deterministic construction;
- declared resonance-space compatibility.

---

## 28. Resonance Window Validation

A resonance-window validation must distinguish:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

These classes are not automatically:

`-1/0/1`

Therefore a window classifier does not validate ternary target semantics unless a separate mapping is also tested.

---

## 29. Resonance-Window Crossing Boundary

A resonance-window crossing does not establish a bifurcation.

Therefore:

`resonance-window crossing ≠ bifurcation`

A bifurcation claim requires the corresponding dynamical-system evidence.

---

## 30. Ternary Validation

Balanced-ternary validation must preserve the exact state space:

`{-1, 0, 1}`

Canonical notation remains:

`-1/0/1`

---

## 31. Active Neutral Validation

State `0` is active neutral.

Validation must preserve its possible roles:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

A test must not treat `0` as missing data.

---

## 32. Direct-Transition Prohibition

Executable validation must reject direct committed transitions:

`-1 → 1`

and:

`1 → -1`

---

## 33. Neutral-Mediated Routing

Opposite-polarity execution must preserve separate committed events:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

Each leg must remain independently observable at the execution layer.

---

## 34. Target and Execution Separation

Validation must preserve:

`target ≠ executed state`

A requested target alone does not prove that a transition was committed.

---

## 35. Pending-State Separation

Validation must preserve:

`pending ≠ executed state`

and:

`pending ≠ active neutral`

A non-null pending target is valid only while retained state is active neutral.

---

## 36. Missing-State Boundary

The following must not be encoded through active neutral `0`:

- missing;
- invalid;
- NaN;
- error;
- unknown;
- abstention.

Tests must detect violations of this boundary.

---

## 37. E(3) Validation

An E(3)-equivariant model requires validation under declared spatial transformations.

The validation set must distinguish:

- scalar invariance;
- polar-vector equivariance;
- higher-order behavior when executable support exists.

---

## 38. Translation Validation

Translation validation checks that translationally invariant quantities remain invariant under common spatial translation.

Relative geometry must behave consistently with the declared geometry contract.

---

## 39. Rotation Validation

Rotation validation checks:

- scalar invariance;
- vector covariance/equivariance;
- graph invariance where geometry permits;
- total-energy invariance.

---

## 40. Reflection Validation

When E(3), rather than only SE(3), is claimed, validation must include reflection behavior.

Representation parity must remain explicit.

---

## 41. Permutation Validation

Atom permutation must be applied consistently to:

- species;
- positions;
- graph;
- node features;
- ternary execution state.

Permutation validation must not compare inconsistently permuted inputs.

---

## 42. Higher-Order Representation Boundary

Formal documentation may define higher-order equivariant representations.

The current executable reference primarily implements scalar and polar-vector channels.

Scientific validation must not claim executable higher-order support unless the corresponding implementation and tests exist.

---

## 43. Energy Validation

Energy validation must check the declared conservative scalar model.

The reference energy state contains:

- atomic contributions;
- total energy.

---

## 44. Energy Algebra

For the canonical executable constructor:

`E_total = Σ E_i`

This relation requires executable validation.

Structural JSON validity alone does not prove it.

---

## 45. Energy Invariance

For an E(3)-invariant scalar energy model:

`E(g · X) = E(X)`

under admissible transformations and consistent transformation of all relevant inputs.

---

## 46. Energy Is Not Ternary State

Validation must preserve:

`energy ≠ ternary state`

`zero energy ≠ active neutral 0`

`negative energy ≠ ternary -1`

`positive energy ≠ ternary 1`

---

## 47. Force Validation

The declared conservative force relation is:

`F = -dE/dr`

Force-gradient validation must use the same energy model being validated.

---

## 48. Fixed-Graph Force Scope

For the current finite-difference reference evaluator, graph topology remains fixed within one local derivative evaluation.

Validation must not silently rebuild graph topology inside one derivative if testing that reference contract.

---

## 49. Graph Rebuild Between States

A graph may be rebuilt between separate physical states.

This does not contradict the fixed-graph local derivative contract.

The two validation scopes must remain distinct.

---

## 50. Stress Validation

The current declared stress convention is:

`stress = +(1/V) dE/dε`

under the repository strain convention.

Validation must retain this sign convention unless an explicitly different convention is being tested.

---

## 51. Force and Stress Are Distinct

Force-gradient validation does not substitute for stress validation.

Stress validation does not substitute for force-gradient validation.

Both derive from energy but use different perturbation spaces.

---

## 52. Molecular-Dynamics Validation

Molecular-dynamics validation must identify:

- equations of motion;
- integration method;
- time step;
- force model;
- graph-update rule;
- initial conditions;
- conserved or monitored quantities;
- propagation semantics.

---

## 53. Velocity-Verlet Validation

For the current reference velocity-Verlet implementation, validation includes:

- state cardinality;
- finite positions;
- finite velocities;
- finite forces;
- deterministic stepping;
- declared energy-drift behavior.

---

## 54. Hidden Evolution Prohibition

A molecular-dynamics step must not silently evolve resonance or ternary state unless the selected composed execution explicitly includes those operations.

Validation must detect hidden state evolution.

---

## 55. Energy-Drift Validation

Energy drift is a numerical trajectory observable.

A drift acceptance bound must declare:

- trajectory length;
- time step;
- model;
- derivative method;
- graph semantics;
- initial condition;
- tolerance.

A bound from one fixture must not be universalized without evidence.

---

## 56. Thermostat Validation

A thermostat validation must test the implemented thermostat contract.

Absence of a thermostat implementation must not be represented as a validated thermostat.

---

## 57. Barostat Validation

A barostat validation must test the implemented barostat contract.

Absence of a barostat implementation must not be represented as a validated barostat.

---

## 58. Transport-Observable Validation

A transport observable requires:

- defined observable;
- sampling protocol;
- time domain;
- state domain;
- units;
- statistical procedure;
- reference relation.

A short deterministic trajectory alone does not establish bulk transport accuracy.

---

## 59. Multiscale Validation

Multiscale validation must operate at each declared mapping boundary.

The chain may include:

`electronic reference`

`→ interatomic`

`→ atomistic`

`→ mesoscale`

`→ continuum`

`→ engineering scale`

Each arrow requires its own validation relation.

---

## 60. Scale Mapping Is Not Validation

The existence of a mapping does not establish its physical validity.

Therefore:

`mapping implemented ≠ mapping scientifically validated`

---

## 61. Mass-Conservation Validation

For additive mass reduction, validation must check:

`Σ coarse mass = Σ fine mass`

within the applicable numerical contract.

---

## 62. Geometry Coarse-Graining Validation

Mass-weighted centroid validation must distinguish Cartesian coarse-graining from periodic coordinate unwrapping.

The current implementation performs no hidden PBC unwrapping.

A validation case crossing a periodic boundary must therefore supply explicit unwrapped geometry if that physical interpretation is required.

---

## 63. Ternary Coarse-Graining Boundary

Ternary states must not be arithmetically averaged.

Therefore:

`mean(-1, 1) = 0`

does not validate a coarse active-neutral state.

Any coarse ternary mapping requires explicit semantics.

---

## 64. Transport Transfer Validation

Transport-coefficient transfer validation must preserve:

- coefficient identity;
- source scale;
- target scale;
- mapping identifier;
- normalization;
- assumptions;
- units;
- provenance.

---

## 65. Thermodynamic-Consistency Validation

Thermodynamic consistency is a Boolean validation result under an explicitly declared relation and model.

It is not balanced-ternary execution state.

Therefore:

`thermodynamic consistency status ≠ ternary state`

---

## 66. Uncertainty Validation

Uncertainty propagation validation must identify:

- representation;
- source scale;
- target scale;
- propagation rule;
- correlation model;
- assumptions;
- normalization.

No Gaussian or independence assumption may be inserted implicitly.

---

## 67. Engineering Boundary Validation

Engineering-scale validation must retain explicit:

- engineering model;
- geometry;
- boundary identifier;
- variable;
- condition;
- unit;
- mapping;
- assumptions.

The boundary type must not be inferred from an arbitrary identifier.

---

## 68. FLiBe Composition Validation

FLiBe validation requires an explicit LiF-BeF2 composition.

The exact ratio:

`2 LiF : 1 BeF2`

is mathematically distinct from a source-defined nearby composition such as:

`67 mol% LiF : 33 mol% BeF2`

Therefore:

`2:1 ≠ automatically 67/33`

---

## 69. Eutectic Terminology Boundary

A stoichiometric ratio must not be called an experimentally established eutectic solely because it is close to a reported invariant composition.

Phase-diagram terminology requires phase-equilibrium evidence.

---

## 70. FLiBe Source Validation

Material-specific FLiBe values require source qualification through:

`docs/references/flibe_sources.md`

A source record must identify the exact observable and domain for which it is used.

---

## 71. Structural FLiBe Validation

Structural validation may use observables such as:

- structure factor;
- pair-distribution function;
- coordination;
- local structural units.

These observables remain distinct.

Therefore:

`structure factor ≠ pair-distribution function`

`pair-distribution function ≠ coordination number`

`coordination number ≠ chemical bond`

---

## 72. Graph Coordination Boundary

Graph-relative coordination does not automatically equal experimental coordination.

A validation mapping between them must define:

- cutoff or graph rule;
- observable;
- normalization;
- source;
- comparison procedure.

---

## 73. Thermophysical FLiBe Validation

A thermophysical property comparison must use reference data at compatible:

- composition;
- temperature;
- pressure when applicable;
- phase;
- unit.

Values outside a source range must not be labeled source-qualified interpolation unless the source relation explicitly permits it.

---

## 74. Density Validation

A source-backed density correlation must retain:

- source;
- coefficients;
- composition;
- temperature range;
- units;
- provenance.

A benchmark may reproduce the correlation exactly.

Such reproduction validates implementation of the correlation.

It does not independently validate the original experiment.

---

## 75. Transport Validation

FLiBe transport validation must distinguish:

- viscosity;
- thermal conductivity;
- electrical conductivity;
- species diffusivity;
- permeability;
- solubility.

These quantities are not interchangeable.

---

## 76. Species-Specific Transport

A hydrogen-isotope diffusivity must not be relabeled as Li, Be, or F self-diffusivity.

Therefore:

`tritium diffusivity ≠ salt-ion self-diffusivity`

---

## 77. Experimental Evidence

Experimental comparison must preserve the source measurement as an independent evidence path.

Model predictions must not be inserted into the experimental reference record.

---

## 78. First-Principles Evidence

First-principles evidence must preserve its computational-method provenance.

Required context may include:

- electronic-structure method;
- exchange-correlation treatment;
- pseudopotential or all-electron method;
- basis or plane-wave settings;
- convergence controls;
- system composition;
- thermodynamic state;
- sampling protocol.

---

## 79. Experimental and First-Principles Comparison

Direct comparison requires matched:

- observable;
- composition;
- thermodynamic state;
- physical state;
- unit;
- normalization;
- sample coordinates where applicable.

No hidden interpolation is permitted in a direct comparison contract.

---

## 80. Comparison Residual

A comparison residual may be defined as:

`calculated - reference`

The sign convention must be explicit.

A residual is not a ternary state.

---

## 81. Comparison Metrics

Possible comparison metrics include:

- pointwise residual;
- absolute residual;
- mean absolute error;
- root-mean-square error;
- maximum absolute error.

Metric selection must be fixed by the validation contract.

---

## 82. No Automatic Pass/Fail from Residual

A numerical residual alone does not define PASS or FAIL.

A validation threshold must be independently declared.

Therefore:

`residual ≠ validation status`

---

## 83. Benchmark Validation

A benchmark must declare:

- benchmark identifier;
- fixed inputs;
- provenance;
- measured or validated output;
- acceptance condition where applicable;
- structured output.

---

## 84. Correctness Benchmark

A correctness benchmark verifies pinned executable outputs or invariants.

Pinned outputs must originate from a declared reference execution or independently defined expected relation.

They must not be changed merely because implementation output changed.

---

## 85. Determinism Benchmark

A determinism benchmark requires repeated execution with identical inputs.

Where byte determinism is claimed:

`output_bytes_run_1 = output_bytes_run_2`

must hold exactly.

---

## 86. Equivariance Benchmark

An equivariance benchmark must test the declared group actions.

For scalar energy:

`E(g · X) = E(X)`

For force vectors:

`F(g · X) = g · F(X)`

under the declared E(3) transformation rules.

---

## 87. Conservation Benchmark

A conservation benchmark must identify the conserved or approximately conserved quantity and numerical context.

A trajectory drift bound is valid only for the declared benchmark configuration.

---

## 88. Numerical-Convergence Benchmark

A convergence benchmark must refine a declared numerical parameter and measure error against a fixed reference.

For a second-order method, observed error ratios under step halving may be compared with the expected order.

The acceptance bound must be fixed before evaluation.

---

## 89. Scaling Benchmark

Scaling validation must distinguish:

- structural scaling;
- runtime scaling;
- memory scaling.

Increasing node count alone does not prove runtime complexity.

---

## 90. Memory Benchmark

Memory measurement must declare:

- measurement mechanism;
- measured scope;
- system sizes;
- repetitions when applicable.

Runner-dependent memory values must not be promoted to universal invariants.

---

## 91. Runtime Benchmark

Runtime measurement must declare:

- clock;
- warm-up procedure;
- measurement repetitions;
- measured scope;
- system sizes.

A shared-runner timing measurement must not be converted into a hard physical correctness threshold.

---

## 92. Property-Reproduction Benchmark

Property reproduction must compare an executable property model to independently recorded source-backed reference values or source equations.

A model must not generate both the prediction and the reference values through the same evaluation path.

---

## 93. Cross-Model Comparison

A cross-model comparison requires compatible:

- inputs;
- state domain;
- observable;
- unit;
- normalization;
- model conditions;
- comparison relation.

Model names alone do not establish comparability.

---

## 94. Reproducibility

A reproducible scientific result requires sufficient artifacts to repeat the declared computation.

Required artifacts may include:

- source revision;
- model manifest;
- configuration;
- parameters;
- dependencies;
- execution command;
- random seed when applicable;
- numerical settings;
- expected structured outputs.

---

## 95. Hidden State Prohibition

Strict reproducibility requires all result-affecting state to be explicit or fixed by the declared execution environment.

Hidden mutable state invalidates strict reproducibility claims.

---

## 96. Randomness

When randomness is used, validation must declare:

- random-number generator;
- seed;
- sampling procedure.

When no randomness is used, deterministic execution must not silently introduce it.

---

## 97. Software Environment

Reproducibility evidence must identify relevant software environment information where result sensitivity requires it.

Examples include:

- Python version;
- dependency versions;
- platform-sensitive numerical implementation.

Environment metadata must not be added when it does not affect the declared claim.

---

## 98. Continuous Integration

CI provides independent clean-runner execution evidence.

A green CI result demonstrates successful completion of the configured checks for the tested revision.

It does not automatically establish every scientific claim in the repository.

---

## 99. Local and CI Validation

TR-EIF validation may use two independent execution contexts:

`local snapshot validation`

and:

`clean CI runner validation`

Agreement between them reduces dependence on one execution environment.

The two contexts must still execute the same declared validation contract.

---

## 100. Schema Validation

Schema validation establishes structural compatibility with committed schema contracts.

It does not replace executable semantic validation.

Therefore:

`schema-valid ≠ scientifically valid`

---

## 101. Trace Validation

Trace validation establishes:

- structural trace validity;
- ordering;
- cardinality;
- ternary execution semantics;
- observable structure;
- deterministic serialization where claimed.

A valid trace does not automatically establish physical accuracy.

---

## 102. Scientific Claim Audit

Before release, every public scientific claim must be classified as one of:

- formally established;
- executable behavior;
- benchmark result;
- source-backed material statement;
- validated comparison;
- unresolved;
- unsupported.

Unsupported claims must not be presented as validated results.

---

## 103. Citation Audit

Every externally sourced scientific value or physical claim requiring external provenance must have a resolvable source record.

Citation presence alone is insufficient.

The citation must actually support the specific claim.

---

## 104. Source Domain Audit

For every imported physical value, validation must verify compatibility of:

- composition;
- temperature;
- pressure;
- phase;
- method;
- unit;
- observable.

---

## 105. Extrapolation Audit

An extrapolated value must be identified as extrapolated.

It must not inherit direct measurement provenance.

---

## 106. Interpolation Audit

Interpolation is permitted only when:

- the source relation permits it;
- the interpolation domain is inside the applicable source range;
- the interpolation method is explicit.

---

## 107. Unit Audit

Every physical comparison requires compatible units.

Implicit unit conversion is prohibited.

A conversion must be explicit and reproducible.

---

## 108. Dimensional Audit

A scientific relation must be dimensionally consistent under its declared unit system.

Numerical equality between quantities with different dimensions has no validation meaning.

---

## 109. Model-Domain Validation

Every concrete model has a validity domain.

Validation must distinguish:

- inside-domain evaluation;
- outside-domain evaluation;
- unavailable domain information.

Outside-domain execution must not automatically be described as physically validated prediction.

---

## 110. Uncertainty and Domain Detection

Uncertainty and domain status remain separate from balanced-ternary execution.

Therefore:

`high uncertainty ≠ active neutral`

`outside domain ≠ ternary -1`

`inside domain ≠ ternary 1`

unless an explicit model mapping defines those targets.

---

## 111. Training and Validation Separation

Training, validation, and test roles must remain explicitly separated.

Exact duplicates, group-related samples, trajectory-related samples, and declared parent-derived relations must not cross split boundaries under the strict FLiBe split-isolation contract.

---

## 112. Training Result Boundary

A training loss value does not establish independent validation performance.

Therefore:

`training fit ≠ validation`

---

## 113. Calibration Result Boundary

Calibration against one dataset does not establish independent reproduction of that same dataset as validation evidence.

Calibration and validation evidence paths must remain distinguishable.

---

## 114. FRP Boundary

FRP may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

TR-EIF scientific validation must not import:

- FRP repository structure;
- RTL architecture;
- scheduler modes;
- FRP-specific coefficients;
- FRP module naming.

Therefore:

`FRP ≠ TR-EIF`

and:

`FRP ≠ TR-EIP`

---

## 115. Confirmed FRP Semantic Correspondences

Confirmed semantic correspondences may include:

- canonical `-1/0/1`;
- active neutral `0`;
- prohibited direct committed opposite-polarity transition;
- explicit mediation through `0`;
- target distinct from executed state.

Each correspondence must remain limited to the semantic property actually established.

---

## 116. Validation Across Architectural Levels

TR-EIF validation operates at nested levels:

`framework`

`→ model family`

`→ domain realization`

`→ executable component`

A validation result at one level must not be automatically generalized to another.

---

## 117. Framework Validation

Framework-level validation concerns:

- definitions;
- contracts;
- invariants;
- mappings;
- architecture boundaries.

---

## 118. TR-EIP Validation

TR-EIP model-family validation concerns:

- E(3) behavior;
- message passing;
- resonance conditioning;
- ternary conditioning;
- conservative energy;
- forces;
- stress.

---

## 119. FLiBe Realization Validation

FLiBe-specific validation additionally concerns:

- composition;
- source-backed physical data;
- material-specific structure;
- thermophysical properties;
- transport properties;
- domain-specific TR-EIP realization;
- MD behavior;
- multiscale coolant closure.

---

## 120. Component Validation

Component-level validation concerns one explicit executable function, type, module, schema, or serializer.

Component correctness does not automatically establish whole-model scientific validity.

---

## 121. Evidence Aggregation

Multiple independent evidence classes may support one scientific claim.

Their roles must remain distinguishable.

For example:

`mathematical proof`

`+ executable invariant test`

`+ numerical benchmark`

may support different aspects of one model relation.

They must not be collapsed into one undifferentiated PASS value.

---

## 122. Negative Validation Result

A failed validation result must remain recorded as a failed validation result.

The acceptance criterion must not be altered after the failure solely to erase the failure.

---

## 123. Regression

A previously validated invariant that later fails constitutes a regression until explained by an explicit contract change.

Silent contract drift is prohibited.

---

## 124. Contract Change

A deliberate change to an invariant or validation target requires coordinated updates to applicable:

- mathematical documentation;
- architecture;
- specification;
- executable implementation;
- tests;
- schemas;
- benchmark references;
- release notes.

---

## 125. Scientific Traceability

A validated public scientific claim should be traceable through:

`claim`

`→ contract`

`→ implementation or source`

`→ validation artifact`

`→ recorded result`

This chain defines repository-level scientific traceability.

---

## 126. Validation Artifact Naming

Validation artifacts must have stable names that identify their purpose.

Names must not imply broader scientific scope than the artifact actually validates.

---

## 127. Structured Validation Output

Machine-generated validation output should be structured where automated comparison is required.

Structured output must separate:

- identifier;
- provenance;
- status;
- checks;
- observed values;
- tolerance or criterion where applicable.

---

## 128. Human Interpretation Boundary

Automated output records the declared checks and observations.

Scientific interpretation remains dependent on the applicable model and evidence contracts.

A green status must not be expanded into claims not tested by the artifact.

---

## 129. Release Validation

Release validation requires all release-scoped checks declared by Phase 12.

Scientific validation status must be evaluated before release claims are finalized.

---

## 130. Core Scientific Validation Invariants

The scientific validation process preserves the following invariants:

1. Claim type determines required evidence type.
2. Validation state is not balanced-ternary state.
3. Active neutral `0` is not missing or unresolved validation.
4. Mathematical proof and executable test are different evidence forms.
5. Executable correctness does not automatically establish physical accuracy.
6. Physical claims require physical provenance.
7. FLiBe claims require compatible composition and thermodynamic domain.
8. Experimental and first-principles evidence remain separate evidence paths.
9. Calibration evidence and validation evidence remain distinguishable.
10. Resonance is not frequency equality.
11. Resonance is not synchronization.
12. Phase locking is not resonance.
13. Coherence is not resonance.
14. Phase order is not complete coherence.
15. Resonance region is not automatically ternary state.
16. Direct committed opposite-polarity ternary transitions remain forbidden.
17. Active-neutral mediation remains explicit.
18. Energy, force, stress, resonance, and ternary state remain distinct.
19. E(3) claims require applicable transformation validation.
20. Force-gradient claims require the same declared energy model.
21. Stress claims require the declared strain convention.
22. MD validation requires explicit numerical settings.
23. Multiscale mappings require boundary-specific validation.
24. Ternary states are not arithmetically coarse-grained by default.
25. Uncertainty remains separate from ternary state.
26. Benchmark fixtures are not physical source data.
27. Source ranges and composition domains must be respected.
28. Tolerances are fixed before evaluation.
29. Similarity is not identity.
30. Hidden result-affecting state invalidates strict reproducibility.
31. Schema validity is not scientific validity.
32. Trace validity is not physical accuracy.
33. CI success establishes only the checks actually executed.
34. Validation failure must not be erased by post-result criterion changes.
35. Scientific claims remain traceable to their evidence.

---

## 131. Repository Validation Interfaces

Scientific validation is supported by committed artifacts under:

`tests/`

`benchmarks/`

`schemas/`

`docs/validation/`

`docs/references/`

`.github/workflows/`

and the executable packages under:

`src/tr_eif/`

These artifact classes serve different validation roles.

---

## 132. Related Validation Documents

The scientific validation plan is the umbrella scientific-evidence contract.

Specialized validation contracts are maintained separately for:

- mathematical validation;
- numerical validation;
- invariant validation;
- reproducibility;
- FLiBe validation.

Each specialized document must remain compatible with this plan.

---

## 133. Non-Claims

This plan does not assert that:

- every physical property is validated;
- every FLiBe property is reproduced;
- every formal theorem has executable physical realization;
- every future TR-EIP model is scientifically validated;
- every scale closure is experimentally validated;
- benchmark success implies material prediction accuracy.

Validation status is determined only by committed evidence for the specific claim.

---

## 134. Summary

TR-EIF scientific validation is claim-specific, provenance-preserving, executable where applicable, and separated from balanced-ternary execution state.

The validation chain is:

`claim`

`→ explicit contract`

`→ appropriate evidence`

`→ fixed validation procedure`

`→ reproducible result`

`→ bounded scientific statement`

The framework preserves:

`similar ≠ identical`

`validation status ≠ ternary state`

`benchmark evidence ≠ physical source evidence`

`implementation correctness ≠ physical accuracy`

`source citation ≠ source applicability`

and:

`green CI ≠ universal scientific validation`

Scientific validation is established only where the declared claim, evidence, execution, and acceptance relation correspond to one another.
