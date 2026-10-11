# Reproducibility Plan

## 1. Scope

This document defines the repository-level reproducibility plan of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The plan applies to reproducibility of:

- mathematical-executable correspondence;
- Python reference implementation;
- atomic configuration parsing;
- resonance dynamics;
- balanced ternary execution;
- active-neutral routing;
- E(3)-equivariant model execution;
- conservative energy;
- forces;
- stress;
- molecular dynamics;
- observable traces;
- deterministic replay;
- multiscale mappings;
- FLiBe-specific TR-EIP realization;
- structured benchmarks;
- source-backed property reproduction;
- schema validation;
- continuous integration;
- release artifacts.

The determinism architecture is defined in:

`docs/architecture/determinism_contract.md`

The trace wire contract is defined in:

`docs/specifications/trace_specification.md`

Scientific validation is defined in:

`docs/validation/scientific_validation_plan.md`

Numerical validation is defined in:

`docs/validation/numerical_validation_plan.md`

---

## 2. Reproducibility Objective

A reproducible result is one that can be regenerated from a sufficiently complete set of declared result-affecting inputs and execution conditions.

The reproducibility chain is:

`source revision`

`→ model identity`

`→ parameters`

`→ input state`

`→ execution configuration`

`→ environment`

`→ deterministic execution`

`→ structured output`

`→ comparison`

A missing result-affecting element makes a strict reproduction claim incomplete.

---

## 3. Reproducibility Is Not Similarity

A reproduced result must satisfy the declared comparison relation.

Visual or numerical resemblance alone is insufficient.

Therefore:

`similar ≠ identical`

and:

`approximately similar ≠ reproducible identity`

unless approximate equivalence is the explicitly declared comparison contract.

---

## 4. Reproducibility Is Not Physical Validation

Reproducing the same result establishes execution repeatability under the declared contract.

It does not by itself establish physical accuracy.

Therefore:

`reproducible ≠ physically validated`

---

## 5. Reproducibility Is Not Mathematical Proof

Repeated execution does not prove a theorem.

Therefore:

`reproducible execution ≠ mathematical proof`

Mathematical proof remains governed by the mathematical validation plan.

---

## 6. Reproducibility Is Not Ternary State

Reproducibility status is validation metadata.

It is not balanced ternary execution state.

Therefore:

`reproduced ≠ 1`

`not reproduced ≠ -1`

`unresolved reproduction ≠ active neutral 0`

---

## 7. Complete Result-Affecting State

Strict reproducibility requires every result-affecting variable to be either:

- explicitly stored;
- explicitly supplied;
- or deterministically reconstructible.

Hidden result-affecting state is prohibited.

---

## 8. State Closure

The complete deterministic state may include:

- continuous state;
- resonance state;
- retained ternary state;
- pending ternary target;
- molecular-dynamics state;
- model time;
- numerical step;
- history state;
- adaptive state;
- multiscale state;
- random-generator state when applicable.

Only state that affects the reproduced result belongs to the required closure.

---

## 9. Input Closure

Every external input affecting execution belongs to the reproducibility contract.

Examples include:

- atomic configuration;
- target sequence;
- guard sequence;
- external field;
- model parameter;
- benchmark fixture;
- reference dataset;
- source-backed property relation.

---

## 10. Parameter Closure

Every result-affecting model parameter must be recoverable.

Parameters may include:

- message-passing parameters;
- conditioning parameters;
- energy-functional parameters;
- resonance parameters;
- numerical differentiation steps;
- graph cutoff;
- MD time step;
- material parameters;
- source-derived coefficients.

---

## 11. Configuration Closure

Execution configuration includes result-affecting choices such as:

- algorithm;
- operator order;
- numerical precision;
- cutoff;
- integration method;
- integration step;
- differentiation method;
- differentiation step;
- serialization version;
- backend.

Changing a result-affecting configuration value defines a different execution unless equivalence is separately established.

---

## 12. Source Revision

Every reproducibility record must identify the source revision used for execution.

For Git-based execution this should identify an immutable commit.

A mutable branch name alone is insufficient for archival reproduction.

---

## 13. Repository State

A reproducible run must use a repository state corresponding to the declared revision.

Uncommitted modifications invalidate strict source-revision identity unless those modifications are separately recorded.

---

## 14. Model Identity

A concrete TR-EIP execution requires explicit model identity.

The identity may include:

- model family;
- model-family version;
- architecture identifier;
- parameter artifact;
- supported species;
- unit system;
- graph rule;
- representation structure;
- resonance structure;
- ternary structure;
- numerical semantics.

The root schema is:

`schemas/model_manifest.schema.json`

---

## 15. Framework and Model-Family Separation

The identity relation remains:

`TR-EIP ⊂ TR-EIF`

A TR-EIP model version is not the TR-EIF repository version.

A trace version is not the TR-EIP model version.

These version spaces must remain separate.

---

## 16. Atomic Configuration Reproduction

A reproducible atomic configuration requires:

- species ordering;
- Cartesian positions;
- optional cell;
- periodic axes.

The structural representation is governed by:

`schemas/configuration.schema.json`

---

## 17. Configuration Ordering

Species and position ordering are part of configuration identity.

A permutation may describe an equivalent physical configuration under an explicit permutation relation.

It is not byte-identical configuration input.

---

## 18. Configuration Parser Determinism

For identical valid mapping or JSON input, the configuration parser must reproduce the same:

`AtomicConfiguration`

under the same parser contract.

Duplicate JSON keys and nonfinite JSON values are rejected rather than normalized silently.

---

## 19. Resonance-State Reproduction

A reproducible resonance state requires:

- oscillator phases;
- oscillator frequencies;
- stable ordering;
- phase normalization semantics.

The structural state is defined by:

`schemas/resonance_state.schema.json`

---

## 20. Resonance Initial State

A reproduced resonance trajectory requires the same complete initial resonance state.

A descriptor alone is not generally sufficient to reconstruct the source oscillator state.

Therefore:

`resonance descriptor ≠ complete resonance state`

---

## 21. Resonance Parameters

Every result-affecting resonance parameter must be reproduced.

A parameter must not be recovered through heuristic similarity.

If a required parameter is absent, strict reproduction is incomplete.

---

## 22. Resonance Integration

Reproducing numerical resonance evolution requires the same declared:

- derivative model;
- integration method;
- time step;
- step sequence;
- operator ordering.

Changing any of these may define a different numerical trajectory.

---

## 23. Ternary State Reproduction

The canonical retained state belongs to:

`-1/0/1`

A reproducible ternary execution state requires:

- retained state;
- pending target where present.

The structural representation is:

`schemas/ternary_state.schema.json`

---

## 24. Active Neutral Preservation

State:

`0`

must reproduce as active neutral.

It must not be converted during serialization or replay into:

- null;
- missing;
- unknown;
- invalid;
- error;
- abstention.

---

## 25. Pending Target Preservation

A non-null pending target must reproduce separately from retained state.

Therefore:

`pending target ≠ retained state`

and:

`pending target ≠ active neutral`

---

## 26. Opposite-Polarity History

A reproducible execution history must preserve separate events:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

A replay must not collapse these into direct committed opposite transitions.

---

## 27. Requested Target Reproduction

If requested targets affect execution, the target sequence belongs to the reproducibility input.

A retained-state trace alone may be insufficient to reconstruct requested-target history.

---

## 28. Guard-State Reproduction

If neutral entry or exit guards affect execution, guard state or its deterministic source belongs to the reproduction contract.

---

## 29. Operator Ordering

For noncommuting operators, execution order is result-affecting.

A reproducibility record must preserve the declared ordering.

For example:

`continuous update`

`→ descriptor`

`→ target generation`

`→ guard`

`→ ternary execution`

is not assumed equivalent to another ordering.

---

## 30. Hidden Update Prohibition

An executable operator must not modify undeclared result-affecting state.

Hidden mutation invalidates strict reproducibility.

---

## 31. E(3) Model Reproduction

A reproducible E(3)-equivariant execution requires the same:

- atomic configuration;
- graph;
- node features;
- model parameters;
- retained ternary execution state;
- resonance-conditioned channels where applicable.

---

## 32. Interaction Graph Reproduction

Graph topology is result-affecting.

Graph reproduction requires:

- same configuration;
- same cell and periodicity;
- same graph rule;
- same cutoff;
- same geometry semantics;
- same canonical ordering.

---

## 33. Graph Is Not Reconstructed from Trace Node Count

A base trace does not contain complete graph topology.

Therefore:

`trace node count ≠ graph`

A deterministic graph must be rebuilt from sufficient declared configuration and graph rules.

---

## 34. Feature-State Reproduction

If model output depends on input node features, those features or their deterministic constructor must be reproduced.

Hidden feature preprocessing is prohibited.

---

## 35. Resonance-Conditioned Features

Where resonance descriptor channels are appended to node features, reproducibility requires the same descriptor state and channel ordering.

The current FLiBe TR-EIP reference channels include:

`phase_order`

and:

`frequency_spread`

---

## 36. Ternary Conditioning

Ternary conditioning depends on retained executed state and explicit conditioning parameters.

Requested or pending targets must not replace retained-state conditioning during reproduction.

---

## 37. Energy Reproduction

A reproducible energy result requires the same:

- configuration;
- graph;
- features;
- execution state;
- message operator;
- conditioning parameters;
- energy functional;
- operation ordering.

---

## 38. Atomic Energy Ordering

Atomic energy contributions preserve node ordering.

A permutation of node ordering changes serialized atomic-energy order unless canonical relabeling is explicitly performed.

---

## 39. Total Energy

For the canonical constructor:

`E_total = Σ E_i`

in declared deterministic tuple order.

A reproduction comparison must specify whether atomic contributions, total energy, or both are compared.

---

## 40. Force Reproduction

The current reference conservative-force evaluator additionally requires:

- coordinate differentiation method;
- differentiation step;
- fixed local graph;
- fixed feature input;
- fixed ternary execution state.

---

## 41. Force Differentiation Step

Changing the coordinate differentiation step defines a different numerical force evaluation unless numerical equivalence is separately declared.

---

## 42. Stress Reproduction

The current reference stress evaluator additionally requires:

- cell;
- strain differentiation method;
- strain step;
- reference-volume convention;
- stress sign convention;
- fixed local graph;
- fixed feature state;
- fixed ternary execution state.

---

## 43. Stress Convention

The current declared reference convention is:

`stress = +(1/V) dE/dε`

A reproduction using another sign convention is not identical output.

---

## 44. Molecular-Dynamics Reproduction

A reproducible MD trajectory requires:

- initial configuration;
- initial velocities;
- masses;
- force model;
- graph rule;
- time step;
- number of steps;
- feature state;
- ternary state;
- operator ordering.

---

## 45. Velocity-Verlet Identity

The current reference MD integrator uses velocity-Verlet.

A trajectory generated by another integration method is not the same numerical realization even if the trajectories are close.

---

## 46. Graph Rebuild in MD

If the MD execution rebuilds graph topology between physical states, the graph-construction rule must be reproduced.

The local force derivative may still hold graph topology fixed inside each derivative.

---

## 47. No Hidden Resonance Evolution in MD

Generic MD does not evolve resonance state internally.

If a composed realization includes resonance propagation, the exact propagation schedule becomes part of reproducibility state/configuration.

---

## 48. No Hidden Ternary Evolution in MD

Generic MD does not execute ternary transitions internally.

If ternary propagation is composed with MD, the execution schedule and guard state belong to the reproducibility contract.

---

## 49. Trace Reproduction

A reproducible trace requires enough execution state and configuration to regenerate every trace field included in the comparison relation.

The trace format is defined by:

`schemas/transition_trace.schema.json`

---

## 50. Trace Is Not Complete State

The current base trace does not contain:

- atomic positions;
- velocities;
- full resonance state;
- interaction graph.

Therefore a base trace alone is not generally a complete restart state.

---

## 51. Trace Version

The current root trace format identifier is:

`tr_eif.trace`

with version:

`1`

A replay must interpret the trace according to the declared version.

---

## 52. Trace Ordering

Reproduction must preserve:

- strictly increasing step order;
- nondecreasing time order;
- node ordering;
- atomic observable ordering.

---

## 53. Missing Observable Reproduction

Missing trace observables reproduce as:

`null`

They must not be converted to numerical zero or active neutral `0`.

---

## 54. Deterministic Replay

The observables layer includes deterministic replay support.

A replay executes a declared producer and compares generated output with expected output under the selected equality relation.

---

## 55. Replay Equality Relation

Replay must explicitly define one of the applicable comparison relations, such as:

- exact object equality;
- exact mapping equality;
- exact JSON equality;
- byte equality;
- declared numerical equivalence.

The relation must not change after the result is observed.

---

## 56. Replay Is Not Guessing

Replay must not reconstruct missing state by heuristic similarity.

Therefore:

`replay ≠ approximate guessing`

If required input is unavailable, the strict replay contract is incomplete.

---

## 57. Byte Determinism

Byte determinism means:

`bytes_run_1 = bytes_run_2`

exactly.

It is stronger than semantic equivalence.

Only artifacts designed for deterministic serialization should make this claim.

---

## 58. Semantic Equivalence

Two outputs may be equivalent under a declared transformation without being byte-identical.

Examples include:

- consistent atom permutation;
- E(3) transformed vector representation;
- representation conversion.

The equivalence relation must be explicit.

---

## 59. Numerical Equivalence

Numerical equivalence may use a fixed tolerance when appropriate.

Tolerance must be declared before execution.

It must not be selected after observing the result.

---

## 60. Environment Identity

Strict numerical reproducibility may depend on execution environment.

Relevant environment metadata may include:

- operating system;
- architecture;
- Python version;
- dependency versions;
- numerical backend;
- precision;
- locale when serialization is affected.

Only result-affecting environment state belongs to strict reproduction metadata.

---

## 61. Python Version

The project currently declares support for Python:

- `3.11`;
- `3.12`;
- `3.13`.

Current automatic Python CI executes on Python:

`3.12`

CI reproduction claims must retain this execution context unless the workflow changes.

---

## 62. Package Installation

Current CI installs the package through:

`python -m pip install -e ".[dev]"`

The package dependency contract is declared in:

`pyproject.toml`

A reproduced CI environment must use compatible dependency resolution.

---

## 63. Dependency Versions

Strict environment reproduction requires resolved dependency versions when dependency behavior can alter results.

A version range alone identifies an admissible dependency domain.

It does not identify one unique dependency environment.

---

## 64. Dependency Resolution Boundary

When exact dependency locking is absent, strict byte-for-byte reproduction across future dependency resolution is not implied.

A release reproducibility bundle should record the resolved environment used for release validation.

---

## 65. Development Dependencies

Development validation currently depends on tooling including:

- pytest;
- pytest-cov;
- ruff;
- jsonschema.

Tool versions used for an archived release should be recoverable when they affect validation output.

---

## 66. Randomness

If an execution uses randomness, reproducibility requires:

- random-number generator identity;
- seed;
- initialization procedure;
- sampling order;
- any retained generator state required for restart.

---

## 67. Current Deterministic Reference Boundary

Deterministic reference paths that do not use randomness must not introduce an arbitrary seed merely for appearance of reproducibility.

No random state is required where no random process exists.

---

## 68. Random Seed Is Not a Substitute for State Closure

A seed alone is insufficient when:

- the generator state has already advanced;
- multiple generators are used;
- sampling order differs;
- other hidden state affects execution.

---

## 69. Input File Integrity

External input artifacts used for reproduction should be identifiable by:

- stable path or artifact identity;
- content digest when archival identity is required;
- version metadata where applicable.

File name alone is not strong content identity.

---

## 70. Digest Use

A cryptographic digest may identify immutable file content.

A digest verifies content identity.

It does not establish scientific correctness.

Therefore:

`matching digest ≠ scientific validation`

---

## 71. Model Parameter Artifact

If a concrete model uses an external parameter artifact, reproducibility requires:

- artifact identifier;
- artifact version;
- content identity;
- applicable model architecture.

Parameter files from another architecture must not be substituted merely because their shapes are compatible.

---

## 72. Model Manifest

A release-grade executable model should have a manifest sufficient to identify all result-affecting model-level structure.

The root manifest schema is:

`schemas/model_manifest.schema.json`

---

## 73. Provenance Reproduction

Reproduction must preserve provenance metadata where it affects interpretation of output.

The canonical provenance classes are:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

---

## 74. Provenance Is Not Numerical State

A reproduced numeric value with changed provenance is not the same scientific evidence record.

Therefore:

`same value + different provenance ≠ same evidence artifact`

---

## 75. Source-Backed Property Reproduction

A source-derived physical property benchmark requires:

- source identifier;
- source composition;
- state range;
- coefficients;
- units;
- provenance;
- independent fixed reference points or relation.

---

## 76. FLiBe Composition Reproduction

FLiBe material reproduction must preserve composition identity.

Exact:

`2 LiF : 1 BeF2`

must not be silently replaced by:

`67 mol% LiF : 33 mol% BeF2`

Therefore:

`2:1 ≠ 67:33`

---

## 77. FLiBe Thermodynamic State

A source-backed reproduction must preserve the declared:

- temperature;
- pressure when applicable;
- physical state;
- composition.

A result outside the source domain must not be described as direct source reproduction.

---

## 78. FLiBe Dataset Reproduction

Training/validation/test dataset reproduction requires:

- sample identifiers;
- configuration identifiers;
- split assignments;
- provenance;
- source identifiers where applicable;
- group identities;
- trajectory identities;
- parent-derived relations.

---

## 79. Dataset Split Isolation

The strict FLiBe split contract must reproduce the same isolation constraints.

A sample must not move between TRAINING, VALIDATION, and TEST merely because a regenerated split is statistically similar.

---

## 80. Data Ordering

When execution depends on dataset ordering, ordering belongs to reproducibility state.

A collection with identical elements in a different result-affecting order is a different input sequence.

---

## 81. Multiscale Reproduction

A multiscale reproduction requires the same:

- fine state;
- partitions;
- hierarchy;
- reduction operators;
- prolongation operators;
- closure providers;
- transport-transfer context;
- thermodynamic-validation context;
- uncertainty-propagation context;
- engineering-boundary context.

---

## 82. Partition Identity

A partition is result-affecting.

Reordering or changing fine-to-coarse membership defines a different multiscale mapping.

---

## 83. Ternary Coarse-Graining Prohibition

Reproduction must not reconstruct coarse ternary state through arithmetic averaging unless such an operator is explicitly part of the model.

Therefore:

`mean(-1, 1) = 0`

does not reconstruct active-neutral coarse state.

---

## 84. Multiscale Provenance

Derived coarse quantities must retain their transformation and source relationships.

A reproduced coarse value without its scale-transfer provenance is incomplete scientific evidence.

---

## 85. Benchmark Identity

Every benchmark reproduction must identify:

- benchmark identifier;
- benchmark version where applicable;
- fixed input construction;
- provenance;
- validation checks;
- output schema or structure.

---

## 86. Correctness Benchmark Reproduction

Pinned correctness benchmark values must not be regenerated automatically from current implementation and then used as expected values.

That procedure would compare implementation with itself.

---

## 87. Determinism Benchmark Reproduction

A determinism benchmark must perform at least two independent executions under the same declared inputs.

Where byte determinism is claimed, output bytes must be identical.

---

## 88. Equivariance Benchmark Reproduction

An equivariance benchmark requires the same:

- reference configuration;
- transformations;
- transformed feature procedure;
- tolerances;
- force differentiation;
- model parameters.

---

## 89. Conservation Benchmark Reproduction

A conservation benchmark requires the same:

- initial MD state;
- masses;
- time step;
- step count;
- force evaluator;
- energy model;
- drift criterion.

---

## 90. Numerical-Convergence Benchmark Reproduction

A convergence benchmark requires the same:

- refinement sequence;
- reference step;
- error metric;
- minimum reduction ratio;
- final error criterion.

Changing the refinement sequence defines a different benchmark.

---

## 91. Scaling Benchmark Reproduction

A structural scaling benchmark requires the same:

- base fixture;
- replica counts;
- replica spacing;
- graph cutoff;
- feature pattern;
- resonance state pattern;
- ternary state pattern.

---

## 92. Memory Benchmark Reproduction

Memory benchmarks using:

`tracemalloc`

measure traced Python allocations.

Exact byte values may vary with environment.

Reproducibility means the measurement procedure is reproducible, not that every environment must report identical memory magnitude.

---

## 93. Runtime Benchmark Reproduction

Runtime benchmarks using:

`time.perf_counter_ns`

measure execution duration.

Exact durations are environment-dependent.

Reproducibility requires the same measurement contract, not identical elapsed time across unrelated machines.

---

## 94. Measurement vs Deterministic Output

Environment-dependent measurements such as runtime and memory are not byte-deterministic model outputs.

They must not be treated as such.

---

## 95. Structured Benchmark Output

Benchmark structured output must remain machine-readable.

Current benchmark output uses structured JSON.

Correctness-gated output must include declared checks and status.

---

## 96. Canonical JSON Output

Where a benchmark claims canonical structured output, serializer formatting and key ordering become part of the byte-determinism contract.

---

## 97. Continuous Integration

Current automatic Python CI executes on:

- push to `main`;
- pull request targeting `main`;
- manual workflow dispatch.

This clean-runner path is independent from local snapshot execution.

---

## 98. Current Python CI Jobs

The current Python CI contains independent jobs for:

- smoke test;
- structured output;
- deterministic validation bench;
- full self-test.

Each job validates a different aspect of repository execution.

---

## 99. Smoke-Test Reproduction

Smoke validation includes:

- package compilation;
- import of principal public package layers.

A smoke test establishes import/execution viability.

It does not establish full scientific validity.

---

## 100. Structured-Output Reproduction

Structured-output CI validates selected trace export and trace-schema contracts.

This ensures machine-readable execution artifacts retain their declared structure.

---

## 101. Deterministic Validation Bench

The deterministic-validation job executes committed test groups including:

- determinism;
- equivariance;
- conservation;
- numerical validation.

The exact test set is defined by the workflow revision.

---

## 102. Full Self-Test

The full self-test executes the complete committed pytest suite.

A green result means the configured suite passed for that revision and environment.

It does not extend claims beyond the tested contracts.

---

## 103. Schema CI

Dedicated schema validation provides an additional independent validation path for the root schema contract.

The schema workflow does not replace Python semantic tests.

---

## 104. Local Snapshot Validation

Local validation uses a specific repository snapshot.

The snapshot must correspond to the intended source revision when strict comparison with CI is claimed.

---

## 105. Local and CI Dual Validation

Where both are available, reproducibility can use:

`local snapshot execution`

plus:

`clean CI execution`

Agreement across these contexts provides two independent execution paths.

---

## 106. Local/CI Mismatch

If local and CI results differ, the mismatch must be investigated.

Possible result-affecting causes include:

- source revision;
- dependency resolution;
- Python version;
- filesystem behavior;
- environment;
- hidden state.

The acceptance criterion must not be changed merely to hide the mismatch.

---

## 107. CI Artifact Retention

Current CI produces JUnit XML validation reports for selected jobs.

These reports identify:

- executed test suite;
- pass/fail state;
- failure details.

Retention duration is controlled by the hosting platform and is not permanent archival storage by itself.

---

## 108. Release Reproducibility Artifact

A release should preserve enough information to recreate the validated release execution environment.

This may include:

- commit hash;
- release version;
- Python version;
- resolved dependencies;
- validation commands;
- benchmark commands;
- model manifests;
- reference artifacts;
- structured benchmark results.

---

## 109. Release Archive

An archived release must correspond to the released source revision.

The archive must not contain uncommitted or post-release modifications under the same release identity.

---

## 110. Version Tag

A release version tag should identify the exact released repository state.

A mutable branch does not replace an immutable version tag for archival release identity.

---

## 111. CITATION Boundary

`CITATION.cff` is created only during Phase 12 after release metadata are stabilized.

Reproducibility does not require creating it early.

---

## 112. Release DOI Boundary

If a DOI or archival identifier is introduced, it must correspond to the actual archived release artifact.

A DOI is not a substitute for executable reproducibility metadata.

---

## 113. Release Notes

Release notes should identify changes affecting:

- model semantics;
- mathematical contracts;
- numerical behavior;
- schema versions;
- benchmark references;
- reproducibility.

---

## 114. Reproduction Command

A release reproducibility record should provide exact commands required to execute relevant validation paths.

Commands must correspond to the committed repository structure.

---

## 115. Working Directory

Commands whose behavior depends on path resolution must declare the expected repository working directory.

---

## 116. Output Destination

Generated reproducibility artifacts should have explicit output paths where path identity matters.

Temporary runtime paths must not be mistaken for persistent release artifacts.

---

## 117. Time and Date Independence

A deterministic scientific output must not depend on wall-clock time unless time is explicitly part of the input contract.

Timestamps added only as metadata must not affect model output.

---

## 118. Hostname Independence

Scientific output must not depend on machine hostname unless the hostname is explicitly a result-affecting input, which is not part of the current reference model contract.

---

## 119. Filesystem Ordering

Code must not depend on unspecified directory iteration order when ordering affects scientific output.

Canonical ordering is required where filesystem discovery contributes to deterministic execution.

---

## 120. Dictionary Ordering Boundary

Although current Python preserves insertion ordering, scientific determinism should rely on declared canonical ordering where key order affects serialization or aggregation.

---

## 121. Locale Boundary

Locale-sensitive formatting must not affect canonical machine-readable output.

Structured JSON numeric output must remain locale-independent.

---

## 122. Floating-Point Environment

Strict bitwise numerical identity may depend on:

- architecture;
- Python build;
- math-library behavior;
- backend.

A bitwise reproducibility claim must declare its applicable execution domain.

---

## 123. Cross-Platform Reproduction

Cross-platform numerical agreement may use a declared numerical equivalence relation when bitwise equality is not guaranteed.

The chosen relation must be fixed before comparison.

---

## 124. No Hidden Caches

A cache that can alter scientific output is result-affecting state and must be controlled.

A performance-only cache that leaves declared output unchanged does not alter scientific result identity.

---

## 125. No Hidden Network Dependency

Strict reproduction should not require mutable external network content during scientific execution unless the remote artifact is immutable and explicitly identified.

Source-backed data used for release reproduction should be preserved or uniquely identified.

---

## 126. External Source Availability

A bibliographic source may be externally hosted.

The reproducibility record must retain enough citation metadata to identify the source even if the original URL later changes.

---

## 127. Reference Data Integrity

Material reference data used in comparisons should preserve:

- source;
- extraction location;
- transformation;
- unit;
- composition;
- state domain.

---

## 128. Derived Reference Data

Derived reference values must preserve their derivation.

A derived value without its derivation chain is incomplete provenance.

---

## 129. Digitized Data

If data are digitized from a figure, reproducibility requires:

- source figure identity;
- digitization method;
- axis calibration;
- resulting sampled values;
- uncertainty or extraction limitations where applicable.

---

## 130. Interpolation

If interpolation is used, reproducibility requires:

- source points;
- interpolation method;
- interpolation domain;
- resulting values.

Interpolation must not be hidden.

---

## 131. Extrapolation

Extrapolation must be explicitly identified.

An extrapolated result does not inherit direct source-domain validation.

---

## 132. Unit Conversion

Unit conversion must record:

- source unit;
- target unit;
- conversion relation.

Implicit conversion is prohibited in strict reproduction records.

---

## 133. Experimental Comparison Reproduction

Experimental comparison requires the same:

- source observable;
- sampled values;
- composition;
- thermodynamic state;
- unit;
- normalization;
- comparison axis.

---

## 134. First-Principles Comparison Reproduction

First-principles comparison additionally requires the relevant computational-method identity.

Method metadata must remain separate from experimental provenance.

---

## 135. Cross-Model Comparison Reproduction

Cross-model reproduction requires compatible:

- input configuration;
- observable;
- units;
- normalization;
- state domain;
- comparison relation.

Model names alone do not establish comparable input state.

---

## 136. Reproduction of Failure

A valid reproducibility system must also reproduce expected failures where the contract requires rejection.

Examples include:

- malformed configuration;
- direct opposite ternary transition;
- invalid pending target;
- invalid schema;
- domain-outside property request.

Failure behavior is part of the executable contract.

---

## 137. Exception Identity Boundary

Exact exception text may or may not be part of a reproduction contract.

Tests requiring specific error messages make those messages part of the tested interface.

Otherwise exception type and semantic rejection may be sufficient.

---

## 138. Reproduction of Boundary Cases

Boundary cases must remain stable where they distinguish architectural semantics.

Examples include:

- active neutral versus null;
- resonance boundary versus active neutral;
- hold versus committed retention;
- exact `2:1` versus `67/33`;
- valid versus invalid pending route.

---

## 139. Regression Reproduction

When a regression is discovered, a minimal reproducible case should be retained as a committed test when appropriate.

This converts the discovered failure into future regression protection.

---

## 140. Contract Change and Reproduction

If a contract intentionally changes, the previous reproduction result may no longer be the expected result.

The change must be explicit.

Affected expected artifacts must not be silently overwritten.

---

## 141. Benchmark Reference Changes

Pinned benchmark reference values may change only when justified by:

- corrected contract;
- corrected implementation reference;
- deliberate model change;
- corrected source evidence.

The reason belongs in release/change documentation.

---

## 142. Schema Versioning

A breaking change to a serialized schema requires explicit schema-version handling where the artifact contract defines versioning.

Silent reinterpretation of old serialized data is prohibited.

---

## 143. Trace Versioning

Trace wire semantics remain tied to trace version.

A replay must not interpret an old trace using incompatible later semantics without explicit conversion.

---

## 144. Model Versioning

A model-family version must identify result-affecting model semantics sufficiently for the declared reproduction scope.

Version strings without semantic correspondence are insufficient archival identity by themselves.

---

## 145. Reproducibility Metadata Is Not Model Input Unless Declared

Metadata such as:

- author;
- repository URL;
- citation;
- timestamp

does not become model input merely because it is stored with a reproduction bundle.

Only result-affecting metadata belongs to execution state.

---

## 146. Reproducibility Checklist: Source

Record:

- repository identity;
- immutable commit;
- branch when useful;
- release tag when applicable;
- working-tree cleanliness where applicable.

---

## 147. Reproducibility Checklist: Environment

Record as needed:

- Python version;
- resolved dependencies;
- platform;
- architecture;
- numerical backend;
- precision.

---

## 148. Reproducibility Checklist: Model

Record:

- framework identity;
- model family;
- architecture;
- parameter artifact;
- graph rule;
- representation;
- resonance structure;
- ternary structure;
- numerical semantics.

---

## 149. Reproducibility Checklist: State

Record all result-affecting:

- configuration;
- resonance state;
- ternary retained state;
- pending target;
- velocities;
- masses;
- time;
- history;
- adaptive state;
- multiscale state.

Only the state relevant to the execution path is required.

---

## 150. Reproducibility Checklist: Numerical Configuration

Record:

- cutoff;
- time step;
- step count;
- differentiation step;
- strain step;
- integrator;
- graph update policy;
- operator ordering.

---

## 151. Reproducibility Checklist: Randomness

Record when applicable:

- generator;
- seed;
- retained generator state;
- sampling order.

If no randomness exists, declare none rather than fabricating a seed.

---

## 152. Reproducibility Checklist: Output

Record:

- output format;
- version;
- serializer;
- comparison relation;
- expected structured result;
- digest where content identity is required.

---

## 153. Reproducibility Checklist: Validation

Record:

- test command;
- benchmark command;
- tolerance;
- expected PASS/FAIL behavior;
- CI workflow;
- CI environment when relevant.

---

## 154. Reproducibility Checklist: Provenance

Record:

- source identifiers;
- provenance classes;
- derived transformations;
- calibration status;
- benchmark/test-fixture classification.

---

## 155. Clean-Runner Requirement

Release-level executable validation should include execution in a clean environment independent from the developer's working tree.

Current GitHub Actions CI provides this independent runner context.

---

## 156. Local Snapshot Requirement

A local full audit should use the exact repository snapshot being qualified.

The snapshot is authoritative for file-by-file review.

---

## 157. Dual-Context Requirement

Where practical, release-critical executable claims should have:

`local snapshot evidence`

and:

`clean CI evidence`

A mismatch blocks strict reproduction closure until explained.

---

## 158. Core Reproducibility Invariants

The reproducibility architecture preserves the following invariants:

1. Immutable source revision identifies the executed code.
2. Every result-affecting input is explicit or deterministically reconstructible.
3. Every result-affecting parameter is explicit.
4. Every result-affecting numerical setting is explicit.
5. Hidden mutable state is prohibited.
6. Operator ordering is preserved.
7. Active neutral `0` remains an executed ternary state.
8. Missing state is not encoded as `0`.
9. Pending target remains distinct from executed state.
10. Opposite-polarity execution preserves separate neutral-mediated events.
11. Resonance state remains continuous.
12. Resonance descriptor is not complete resonance state.
13. Graph topology is reproduced from explicit graph rules.
14. Feature construction is explicit.
15. Ternary conditioning uses retained executed state.
16. Energy, force, and stress numerical semantics are reproduced explicitly.
17. MD initial state and integration configuration are complete.
18. Generic MD does not hide resonance or ternary updates.
19. Trace version and ordering are preserved.
20. Replay uses declared equality semantics.
21. Replay does not guess missing state.
22. Byte determinism is claimed only where applicable.
23. Environment-dependent measurements are not treated as deterministic scientific outputs.
24. Provenance remains attached to source-backed and derived evidence.
25. FLiBe composition identity is preserved.
26. Dataset split assignments are preserved.
27. Multiscale mappings and partitions are reproduced explicitly.
28. Benchmark expected values are not regenerated from the tested implementation without justification.
29. Validation tolerances are fixed before execution.
30. CI and local validation remain independent execution contexts.
31. Dependency resolution is part of strict environment reproduction when result-affecting.
32. A reproducible result is not automatically a physically valid result.
33. Similarity is not identity.

---

## 159. Release Reproducibility Closure

Reproducibility is considered release-closed only after the release audit confirms:

- exact source revision;
- complete required environment metadata;
- model identity;
- input state;
- parameters;
- numerical configuration;
- deterministic replay where applicable;
- benchmark reproduction;
- schema validation;
- local validation;
- clean CI validation;
- release artifact identity.

---

## 160. Non-Claims

This reproducibility plan does not assert that:

- every environment produces bitwise-identical floating-point results;
- runtime is identical across machines;
- memory use is identical across machines;
- reproducibility proves physical validity;
- reproducibility proves mathematical correctness;
- deterministic replay contains all physical state;
- every current artifact is already a complete release bundle.

Those properties require their own declared contracts and evidence.

---

## 161. Summary

TR-EIF reproducibility requires complete control of result-affecting state rather than approximate regeneration.

The reproducibility chain is:

`immutable source`

`→ complete input`

`→ complete parameters`

`→ complete execution configuration`

`→ declared environment`

`→ deterministic execution`

`→ structured output`

`→ fixed comparison relation`

The framework preserves:

`replay ≠ guessing`

`similar ≠ identical`

`determinism ≠ physical validity`

`reproducibility ≠ mathematical proof`

`runtime equality ≠ scientific reproducibility`

`memory equality ≠ scientific reproducibility`

and:

`active neutral 0 ≠ missing state`

A result is reproducible only when another execution can reconstruct the declared result from the declared complete execution contract without hidden state or post-hoc adjustment.
