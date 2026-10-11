# Invariant Validation Plan

## 1. Scope

This document defines the repository-level invariant validation plan of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The plan applies to invariants associated with:

- repository structure;
- atomic configuration;
- geometry;
- interaction graphs;
- continuous resonance state;
- resonance descriptors;
- balanced ternary execution;
- active neutral state 0;
- transition routing;
- deterministic execution;
- E(3)-equivariant features;
- conservative energy;
- forces;
- stress;
- molecular dynamics;
- observables and traces;
- JSON schemas;
- multiscale mappings;
- FLiBe specialization;
- benchmark execution.

This document defines how invariants are identified, qualified, executed, and audited.

It does not replace mathematical proof.

It does not replace numerical validation.

It does not replace physical validation.

---

## 2. Invariant Definition

An invariant is a property that must remain true under a declared domain and operation.

An invariant specification requires:

- invariant identifier;
- domain;
- preconditions;
- operation or transition;
- preserved property;
- failure condition;
- validation method.

An invariant without a declared operation or scope is incomplete.

---

## 3. Invariant Validation Chain

The repository-level invariant chain is:

`formal invariant`

`→ executable contract`

`→ qualification test`

`→ clean-runner CI execution`

`→ regression status`

The same invariant may have both mathematical and executable evidence.

Those evidence forms remain distinct.

---

## 4. Invariant Is Not Validation Status

Invariant validity and balanced ternary state are separate concepts.

Therefore:

`invariant holds ≠ ternary 1`

`invariant fails ≠ ternary -1`

`invariant unresolved ≠ active neutral 0`

Validation status must remain outside the ternary execution state space.

---

## 5. Active Neutral Is Not an Error State

Balanced ternary state:

`0`

is active neutral.

It may support:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Invariant-validation failures must never be encoded as:

`0`

Therefore:

`failed invariant ≠ active neutral`

---

## 6. Exact Invariants

Some invariants require exact discrete identity.

Examples include:

- canonical ternary states;
- prohibited transition pairs;
- enum values;
- node cardinality;
- schema constants;
- pending-target state;
- deterministic ordering;
- required file names.

Exact invariants must not be weakened by floating-point tolerances.

---

## 7. Numerical Invariants

Some invariants are evaluated numerically.

Examples include:

- finite values;
- mass conservation;
- E(3) residual bounds;
- force-gradient consistency;
- stress consistency;
- energy drift bounds.

Numerical invariants require a fixed comparison relation and tolerance where applicable.

---

## 8. Structural Invariants

Structural invariants concern organization rather than magnitude.

Examples include:

- field presence;
- tuple cardinality;
- tensor shape;
- graph node count;
- trace node count;
- schema set completeness;
- package structure.

Structural correctness does not imply physical correctness.

---

## 9. Semantic Invariants

Semantic invariants preserve architectural meaning.

Examples include:

`target ≠ executed state`

`pending ≠ active neutral`

`energy ≠ ternary state`

`resonance classification ≠ ternary state`

`validation status ≠ ternary state`

These invariants must survive serialization, replay, documentation, and cross-layer mappings.

---

## 10. Repository Invariant Boundary

Repository layout is part of the project contract.

A required path must:

- exist when the phase requires it;
- use the approved name;
- contain the declared artifact type;
- not be replaced by a similarly named but incompatible path.

For example:

`.json ≠ .j`

even when file contents are otherwise identical.

---

## 11. Naming Invariants

TR-EIF naming preserves:

`TR-EIF = Ternary Resonant Equivariant Interatomic Framework`

and:

`TR-EIP ⊂ TR-EIF`

FRP remains a separate project.

Therefore:

`FRP ≠ TR-EIF`

`FRP ≠ TR-EIP`

Global substitutions that collapse these identities are invalid.

---

## 12. Canonical Ternary Notation

The canonical balanced ternary state space is:

`T = {-1, 0, 1}`

Canonical textual notation is:

`-1/0/1`

The additional sign before positive one is not used in canonical repository notation.

---

## 13. Ternary State Membership

Every retained ternary execution state must belong exactly to:

`{-1, 0, 1}`

No other integer, float, string, null value, or error code is a retained ternary state.

---

## 14. Missing-State Separation

The following must not be represented through active neutral state `0`:

- missing;
- invalid;
- NaN;
- error;
- unknown;
- abstention;
- unevaluated state.

Therefore:

`missing ≠ 0`

`invalid ≠ 0`

`NaN ≠ 0`

---

## 15. Direct Opposite Transition Prohibition

The committed transitions:

`-1 → 1`

and:

`1 → -1`

are forbidden.

This invariant is exact.

It does not depend on numerical tolerance.

---

## 16. Required Opposite Routes

Opposite-polarity execution requires:

`-1 → 0 → 1`

or:

`1 → 0 → -1`

Each leg is a separate committed execution event.

The intermediate active-neutral state must remain observable.

---

## 17. Active-Neutral Residence

Active neutral may remain retained for multiple execution opportunities.

Therefore:

`entry into 0 ≠ mandatory immediate exit`

An implementation that forces immediate exit violates the routing contract.

---

## 18. Target Separation

Requested target and executed state remain distinct types.

Therefore:

`target ≠ executed state`

even when their numerical values later become equal after execution.

---

## 19. Pending Target Separation

A pending target is distinct from the retained execution state.

A pending target is also distinct from active neutral.

Therefore:

`pending ≠ executed`

and:

`pending ≠ 0`

---

## 20. Pending-State Requirement

A non-null pending target is valid only while retained state is active neutral.

Therefore:

`pending != null → retained_state = 0`

This invariant is exact.

---

## 21. Pending Target Domain

A pending target belongs only to:

`{-1, 1}`

The value:

`0`

is invalid as a pending target.

---

## 22. Pending Target Immutability

The current executable routing contract does not silently replace an existing pending target with a conflicting new target.

Pending replacement requires an explicitly different higher-level contract.

---

## 23. Hold vs Committed Retention

A held execution attempt:

`route = None`

is distinct from a committed self-transition.

Therefore:

`hold ≠ committed retention`

Numerically identical previous/current state does not erase this event distinction.

---

## 24. Vector Execution Cardinality

For a ternary execution vector:

`node_count > 0`

Requested-target vectors and guard vectors must match execution node count where supplied.

Vector execution must preserve node cardinality.

---

## 25. Atomic Configuration Invariants

A valid `AtomicConfiguration` preserves:

- nonempty species;
- species/position cardinality equality;
- finite Cartesian positions;
- Boolean periodic axes;
- valid optional cell;
- nonzero cell determinant where a cell exists;
- cell presence when periodicity requires it.

---

## 26. Species Identity

Species labels must remain nonempty identifiers.

Whitespace-only species are invalid.

Species order is part of configuration identity.

---

## 27. Position Finiteness

Every Cartesian position component must be finite.

NaN and infinity are invalid configuration state.

---

## 28. Cell Determinant

A supplied cell must be nonsingular.

A zero determinant is invalid.

Numerically degenerate cell handling belongs to the declared geometry contract.

---

## 29. Periodic Configuration Requirement

A periodic configuration requires an explicit cell.

Periodic axes must not be enabled without a corresponding cell representation.

---

## 30. Parser Invariants

The configuration parser preserves:

- required-field checking;
- allowed-field checking;
- duplicate-key rejection;
- non-object-root rejection;
- NaN/Infinity rejection;
- typed species;
- typed positions;
- optional cell parsing;
- Boolean periodic-axis parsing;
- delegation to `AtomicConfiguration` invariants.

---

## 31. Parser Determinism

Identical valid input mappings or JSON text must produce identical configuration values.

No hidden parser state is permitted.

---

## 32. Geometry Invariants

Geometry operations preserve their declared coordinate semantics.

Relative displacement, periodic displacement, fractional coordinates, and Cartesian coordinates must not be silently interchanged.

---

## 33. Minimum-Image Boundary

The current periodic implementation uses componentwise fractional wrapping.

It must not be described as universally producing the globally shortest Cartesian image for strongly skewed cells.

This limitation is part of the geometry invariant boundary.

---

## 34. Nonperiodic Axes

A nonperiodic axis must not be wrapped.

Mixed periodic/nonperiodic geometry must preserve axis-specific behavior.

---

## 35. Interaction Graph Node Count

An interaction graph is bound to a fixed node count.

Graph node count must match the represented configuration when used by configuration-dependent model layers.

---

## 36. Graph Edge Geometry

Every graph edge must contain finite geometric information consistent with the graph-construction contract.

Invalid geometry must not become a graph edge.

---

## 37. Graph Ordering

Where deterministic graph accumulation is required, canonical edge ordering must remain stable.

Different insertion ordering must not silently change a deterministic result.

---

## 38. Graph Is Not Chemical Bond

Graph connectivity is model-relative.

Therefore:

`graph edge ≠ chemical bond`

unless an explicit physical mapping establishes that interpretation.

---

## 39. Resonance-State Invariants

A valid resonance state preserves:

- nonempty phase vector;
- nonempty frequency vector;
- equal cardinality;
- finite values;
- normalized executable phases.

---

## 40. Phase Domain

Executable phases are normalized into:

`[0, 2π)`

Equivalent angular representations must map to the same canonical phase.

---

## 41. Frequency Finiteness

All oscillator frequencies must be finite.

NaN and infinity are invalid resonance-state values.

---

## 42. Phase-Order Range

The phase-order observable must satisfy:

`0 ≤ R ≤ 1`

within the declared numerical contract.

---

## 43. Frequency-Spread Range

Frequency spread must satisfy:

`σ_ω ≥ 0`

Zero spread does not establish resonance.

---

## 44. Resonance Semantic Invariants

Invariant validation must preserve:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

---

## 45. Resonance Region Separation

The classes:

`OUTSIDE`

`BOUNDARY`

`INSIDE`

are not automatically:

`-1`

`0`

`1`

Therefore:

`resonance region ≠ ternary state`

unless an explicit mapping is defined.

---

## 46. Resonance Boundary Is Not Active Neutral

A coordinate on:

`∂W_R`

is a resonance-window boundary classification.

It is not active-neutral ternary state.

Therefore:

`BOUNDARY ≠ automatically 0`

---

## 47. Resonance-Window Crossing

Invariant validation preserves:

`resonance-window crossing ≠ bifurcation`

A window crossing must not be relabeled as a dynamical bifurcation without separate evidence.

---

## 48. Bifurcation Separation

A bifurcation is not itself a ternary transition.

Therefore:

`bifurcation ≠ ternary transition`

---

## 49. Structural Transition Separation

A ternary transition is not automatically a structural transition.

A structural transition is not automatically a physical phase transition.

Therefore:

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

---

## 50. Oscillator Phase Separation

Oscillator phase is not physical phase of matter.

Therefore:

`oscillator phase ≠ physical phase of matter`

---

## 51. Phase Coupling Separation

Phase coupling is not mechanical force.

Therefore:

`phase coupling ≠ mechanical force`

---

## 52. Phase Relation Separation

A phase relation is not automatically a chemical bond.

Therefore:

`phase relation ≠ chemical bond`

---

## 53. E(3) Transformation Invariants

An E(3) transformation must preserve its declared mathematical structure.

Validation includes:

- identity behavior;
- composition behavior;
- translation;
- rotation;
- reflection.

---

## 54. Scalar Invariance

Scalar invariant channels remain unchanged under admissible spatial transformation.

For invariant scalar:

`s`

the relation is:

`s(g · X) = s(X)`

within the applicable numerical contract.

---

## 55. Polar-Vector Equivariance

Polar vectors transform according to the spatial linear transformation.

Translation does not alter a pure polar vector.

Rotation and reflection act according to the declared E(3) matrix.

---

## 56. Spatial Rotation Is Not Ternary Reversal

Spatial E(3) transformations do not automatically change ternary polarity.

Therefore:

`spatial rotation ≠ ternary polarity reversal`

---

## 57. Feature Cardinality

A `NodeFeatureVector` preserves:

- positive node count;
- consistent scalar-channel width;
- consistent vector-channel width;
- finite channel values.

---

## 58. Feature Type Separation

Scalar channels and vector channels are not interchangeable.

A vector must not be silently flattened into scalar channels.

A scalar channel must not be interpreted as a Cartesian vector.

---

## 59. Higher-Order Boundary

Formal higher-order representations do not imply current executable higher-order feature channels.

Invariant validation must preserve the distinction between formal and executable coverage.

---

## 60. Ternary Conditioning

Ternary conditioning acts on retained executed state.

Requested targets and pending targets must not replace retained-state conditioning.

---

## 61. Active-Neutral Conditioning

Active neutral `0` may have an explicit nonzero conditioning scale.

Therefore:

`active neutral ≠ numerical multiplication by zero`

---

## 62. Resonance Conditioning

Continuous resonance channels remain separate from ternary conditioning.

Therefore:

`resonance conditioning ≠ ternary conditioning`

---

## 63. Energy-State Invariants

A valid energy state preserves:

- nonempty atomic-energy tuple;
- finite atomic contributions;
- finite total energy;
- deterministic atom ordering.

---

## 64. Energy Algebra

For the canonical constructor:

`E_total = Σ E_i`

must hold under the declared deterministic summation order.

---

## 65. Energy Is Not Ternary State

Invariant validation preserves:

`energy ≠ ternary state`

`zero energy ≠ active neutral 0`

`negative energy ≠ ternary -1`

`positive energy ≠ ternary 1`

---

## 66. Energy Node Cardinality

Energy atom count must match the represented model node count at the energy-model result boundary.

---

## 67. Energy E(3) Invariance

For an E(3)-invariant scalar energy model, total energy must remain invariant under admissible spatial transformations.

---

## 68. Force-State Invariants

A valid force state preserves:

- positive atom count;
- exactly three Cartesian components per force;
- finite components;
- stable node ordering.

---

## 69. Conservative Force Relation

The declared conservative force relation is:

`F = -dE/dr`

The negative sign is invariant under the current energy/force contract.

---

## 70. Force Is Not Ternary State

A force component equal to:

`0`

does not imply active neutral state.

Therefore:

`force ≠ ternary state`

---

## 71. Fixed-Graph Force Derivative

Within one finite-difference force derivative, graph topology remains fixed under the current reference evaluator.

A graph rebuild inside that local derivative would violate this numerical invariant.

---

## 72. Graph Rebuild Between Physical States

The local fixed-graph invariant does not prohibit graph reconstruction between separate physical states.

These scopes must remain distinct.

---

## 73. Stress-State Invariants

A valid stress state contains a finite:

`3 × 3`

Cartesian tensor.

The reference conservative stress evaluator returns a symmetric tensor.

---

## 74. Stress Convention

The current declared convention is:

`stress = +(1/V) dE/dε`

The sign convention is part of the invariant contract.

---

## 75. Stress Is Not Ternary State

Zero stress is not active neutral.

Therefore:

`stress ≠ ternary state`

---

## 76. Molecular-Dynamics State Invariants

A valid MD state preserves:

- atom cardinality;
- species ordering;
- finite positions;
- finite velocities;
- finite positive masses.

---

## 77. Velocity-Verlet Cardinality

One velocity-Verlet step must preserve:

- atom count;
- species ordering;
- velocity count;
- mass count.

---

## 78. Generic MD Does Not Hide Resonance Evolution

The generic MD layer must not silently update resonance state.

Resonance propagation requires explicit composition.

---

## 79. Generic MD Does Not Hide Ternary Evolution

The generic MD layer must not silently execute ternary transitions.

Ternary propagation requires explicit composition.

---

## 80. MD Time-Step Validity

A numerical MD time step must be finite and positive.

Zero or negative time steps are invalid.

---

## 81. Energy-Drift Invariant Boundary

Energy-drift bounds are benchmark-specific numerical invariants.

They are not universal exact invariants of every finite-step trajectory.

The benchmark context must remain attached to the drift criterion.

---

## 82. Trace Record Invariants

A valid trace record preserves:

- nonnegative integer step;
- finite nonnegative time;
- nonempty execution vector;
- energy cardinality when energy is present;
- force cardinality when forces are present;
- valid stress tensor when stress is present.

---

## 83. Trace Sequence Invariants

A valid trace sequence preserves:

- nonempty record collection;
- common node count;
- strictly increasing step;
- nondecreasing time.

---

## 84. Trace Ternary Semantics

Trace serialization must preserve:

- retained state;
- pending target;
- active neutral identity.

It must not collapse:

`-1 → 0 → 1`

into:

`-1 → 1`

---

## 85. Trace Missing-Observable Semantics

Missing optional observables serialize as:

`null`

They must not serialize as active neutral:

`0`

Therefore:

`null ≠ active neutral`

---

## 86. Trace Determinism

Identical complete deterministic execution inputs must reproduce identical trace output under the declared determinism contract.

---

## 87. Replay Invariants

Deterministic replay requires:

- fixed inputs;
- fixed model identity;
- fixed execution order;
- fixed serialization contract;
- declared equality relation.

Replay must not infer missing state by similarity.

---

## 88. Replay Is Not Guessing

Invariant validation preserves:

`replay ≠ approximate reconstruction`

When required replay state is absent, the replay contract is incomplete.

---

## 89. Schema-Set Invariants

The approved root schema set contains exactly:

`configuration.schema.json`

`resonance_state.schema.json`

`ternary_state.schema.json`

`transition_trace.schema.json`

`energy_output.schema.json`

`observables.schema.json`

`model_manifest.schema.json`

under the current repository plan.

---

## 90. Schema Dialect

Every root schema uses:

`JSON Schema Draft 2020-12`

unless a future versioned schema contract explicitly changes the dialect.

---

## 91. Cross-Schema References

Every local external `$ref` must resolve to an existing committed schema artifact.

Broken local references invalidate schema-set qualification.

---

## 92. Schema and Runtime Separation

Structural schema validity does not replace runtime invariants.

For example, a schema may validate field shapes while executable code additionally enforces cross-field cardinality.

Therefore:

`schema-valid ≠ runtime-valid`

---

## 93. Model Manifest Invariants

A valid model manifest preserves:

- `TR-EIP` model-family identity;
- explicit architecture identifier;
- supported species;
- unit-system identifier;
- `E(3)` symmetry declaration;
- graph rule;
- representation structure;
- resonance structure;
- ternary structure;
- output capabilities;
- numerical semantics;
- provenance.

---

## 94. Manifest Ternary Contract

The model manifest must preserve canonical states:

`[-1, 0, 1]`

and active-neutral state:

`0`

It must also preserve:

`direct_opposite_committed_transitions = false`

---

## 95. Manifest Resonance Contract

The manifest resonance state domain remains:

`continuous`

under the current model-manifest contract.

A binary or ternary replacement of continuous resonance state violates that declaration.

---

## 96. Multiscale Partition Invariants

A valid partition preserves:

- one coarse index per fine index;
- nonempty fine mapping;
- contiguous coarse index domain;
- deterministic membership ordering.

---

## 97. Mass-Reduction Invariant

For additive mass reduction:

`Σ coarse masses = Σ fine masses`

within the declared numerical relation.

---

## 98. Coarse Geometry Invariant

Mass-weighted centroid calculation preserves the declared Cartesian mass-weighted formula.

No hidden periodic unwrapping occurs.

---

## 99. Ternary Averaging Prohibition

Balanced ternary state must not be arithmetically averaged across scales.

Therefore:

`mean(-1, 1) = 0`

does not establish active-neutral coarse state.

---

## 100. Prolongation Boundary

Broadcast prolongation reproduces the declared coarse value across the fine members of one partition entity.

It is not generally the inverse of reduction.

---

## 101. Partition Composition

Partition composition must preserve mapping compatibility between successive levels.

The output cardinality of one level must match the input cardinality of the next.

---

## 102. Multiscale Hierarchy

A multiscale hierarchy preserves ordered scale relations.

Scale index is structural metadata.

Therefore:

`scale index ≠ ternary state`

---

## 103. Mesoscale Closure Invariants

A mesoscale closure preserves:

- source coarse state;
- closure identifier;
- source identifier;
- declared closure variables;
- canonical variable ordering where required.

---

## 104. Continuum Closure Invariants

A continuum closure remains explicitly bound to its mesoscale closure input.

Provider output must not silently substitute another upstream state.

---

## 105. Transport Transfer Invariants

Transport transfer preserves:

- coefficient identity;
- declared target scale;
- mapping context;
- normalization context;
- assumptions.

No hidden unit conversion is permitted.

---

## 106. Thermodynamic Consistency Boundary

Thermodynamic consistency status remains validation evidence.

Therefore:

`thermodynamic consistency ≠ ternary state`

---

## 107. Uncertainty Propagation Invariants

Uncertainty propagation preserves:

- quantity identity;
- representation;
- source scale;
- target scale;
- propagation context;
- assumptions;
- normalization.

---

## 108. Uncertainty Is Not Ternary State

An uncertainty value or uncertainty status must not be encoded through active neutral `0`.

---

## 109. Engineering Boundary Invariants

Engineering boundary records preserve:

- continuum closure input;
- engineering context;
- canonical boundary identity;
- condition values;
- units;
- source identifier.

---

## 110. FLiBe Species Invariants

The FLiBe specialization recognizes only its declared species domain.

Species identity must remain explicit.

No species is inferred from ternary state or resonance classification.

---

## 111. FLiBe Composition Invariants

A valid FLiBe composition preserves its LiF-BeF2 formula-unit relation.

Exact:

`2 LiF : 1 BeF2`

must remain distinguishable from:

`67 mol% LiF : 33 mol% BeF2`

Therefore:

`2:1 ≠ 67:33`

---

## 112. FLiBe Charge Boundary

Formal ionic charge is a physical/chemical model attribute.

It is not balanced-ternary polarity.

Therefore:

`formal ionic charge ≠ ternary state`

---

## 113. FLiBe Mass Invariants

Material mass parameters must be:

- finite;
- positive;
- species-addressable.

Test-fixture masses remain test-fixture evidence.

---

## 114. FLiBe Thermodynamic State Invariants

Thermodynamic variables such as temperature and pressure remain distinct from:

- oscillator phase;
- oscillator frequency;
- ternary state;
- validation status.

---

## 115. FLiBe Coordination Boundary

Graph-relative coordination is not automatically:

- chemical bond count;
- experimental coordination;
- resonance classification.

These relations require separate mappings.

---

## 116. FLiBe Resonance Descriptor Invariants

The FLiBe resonance descriptor preserves:

- configuration cardinality;
- coordination cardinality;
- resonance oscillator cardinality;
- species ordering;
- explicit thermodynamic context;
- provenance.

Its base resonance coordinate remains continuous.

---

## 117. FLiBe Dataset-Split Invariants

Strict dataset isolation preserves separation among:

- TRAINING;
- VALIDATION;
- TEST.

Exact configuration identity, explicit groups, trajectories, and known parent-derived lineages must not cross split boundaries under the strict isolation contract.

---

## 118. Dataset Split Is Not Ternary State

Dataset roles are metadata.

Therefore:

`TRAINING/VALIDATION/TEST ≠ -1/0/1`

---

## 119. FLiBe TR-EIP Invariants

The FLiBe TR-EIP realization preserves the architecture:

`E(3) geometry`

`→ continuous resonance channels`

`→ retained -1/0/1 conditioning`

`→ conservative scalar energy`

These layers interact without becoming semantically identical.

---

## 120. Resonance Path Independence

Changing the continuous resonance descriptor while retaining the same ternary state must be capable of changing the conditioned energy path where model weights make that channel active.

This validates an independent resonance pathway.

---

## 121. Ternary Path Independence

Changing retained ternary execution state while keeping resonance state fixed must be capable of changing the conditioned energy path where conditioning parameters distinguish the states.

This validates an independent ternary pathway.

---

## 122. Active-Neutral Energy Path

Active neutral may produce a distinct nonzero conditioning behavior.

Therefore active neutral remains executable, not passive absence.

---

## 123. FLiBe MD Invariants

FLiBe MD validation preserves:

- species identity;
- composition;
- atom cardinality;
- explicit masses;
- retained ternary state unless separately evolved;
- resonance state unless separately evolved.

---

## 124. FLiBe Multiscale Invariants

FLiBe multiscale coolant closure preserves:

- composition at fine scale;
- represented total mass;
- explicit closure chaining;
- transport-transfer scale identity;
- explicit uncertainty propagation;
- explicit thermodynamic validation;
- explicit engineering boundary state.

---

## 125. Property-Reference Domain

A source-derived physical property model must remain inside its registered source domain.

Composition and temperature boundaries are part of the invariant.

---

## 126. Property Provenance

A source-derived property must retain:

- source identifier;
- provenance class;
- units;
- applicable composition;
- applicable state range.

---

## 127. Benchmark Invariants

Every correctness-gated benchmark preserves:

- benchmark identifier;
- provenance;
- structured output;
- declared checks;
- nonzero failure exit status when checks fail.

---

## 128. Benchmark Determinism

Where a benchmark claims byte determinism, repeated independent execution must produce byte-identical structured output.

Runtime and memory benchmarks are excluded from byte-equality requirements when their measured values are intentionally environment-dependent.

---

## 129. Runtime Measurement Boundary

Runtime magnitude is measurement evidence.

It is not an invariant of correctness.

Therefore:

`runtime changed ≠ automatically regression`

A regression exists only if a declared runtime criterion exists and fails.

---

## 130. Memory Measurement Boundary

Memory magnitude is environment-dependent measurement evidence.

It is not a universal invariant of correctness.

---

## 131. Property-Reproduction Invariant

A property-reproduction benchmark must compare executable output against an independently fixed source-backed reference relation or values.

The model must not generate both sides of the comparison through the same hidden path.

---

## 132. Invariant Qualification Test Location

Executable invariant qualification tests reside primarily under:

`tests/invariants/`

Additional invariant-relevant qualification may also reside in:

`tests/determinism/`

`tests/equivariance/`

`tests/conservation/`

`tests/numerical/`

`tests/integration/`

The directory name does not replace semantic classification.

---

## 133. Current Invariant-Test Coverage

The repository currently contains invariant qualification for areas including:

- active neutral;
- atomic configuration;
- configuration parser;
- root schemas;
- geometry;
- interaction graph;
- ternary transitions;
- ternary conditioning;
- ternary vector execution;
- trace schema;
- MD validation;
- multiscale partitioning;
- multiscale geometry;
- multiscale reduction;
- multiscale prolongation;
- multiscale hierarchy;
- FLiBe species;
- FLiBe composition;
- FLiBe charge;
- FLiBe mass;
- FLiBe thermodynamic state;
- FLiBe coordination;
- FLiBe resonance;
- FLiBe dataset configuration;
- FLiBe multiscale coolant;
- FLiBe public API.

This list describes committed qualification coverage.

It does not imply that every possible scientific invariant is closed.

---

## 134. CI Invariant Validation

Invariant qualification must execute on a clean CI runner.

CI execution provides an independent environment from local snapshot checking.

---

## 135. Local and CI Agreement

A committed invariant should ideally satisfy:

`local qualification`

and:

`clean-runner qualification`

when both contexts execute the same declared contract.

Disagreement must be investigated rather than hidden.

---

## 136. Regression Policy

A previously passing fixed invariant that fails under unchanged semantics is a regression.

The validation criterion must not be weakened automatically.

---

## 137. Intentional Contract Change

A deliberate invariant change requires coordinated updates to applicable:

- formal documentation;
- architecture;
- specifications;
- implementation;
- tests;
- schemas;
- benchmarks;
- release notes.

---

## 138. Invariant Failure Reporting

A failed invariant report must identify:

- invariant;
- input;
- expected relation;
- observed relation;
- execution context.

A failure must not be translated into a ternary execution state.

---

## 139. Counterexample Preservation

When a counterexample exposes an invalid universal claim, the counterexample should be retained as a regression fixture where appropriate.

This prevents reintroduction of the invalid claim.

---

## 140. Boundary-Case Preservation

Invariant suites should retain boundary cases that distinguish neighboring semantic classes.

Examples include:

- `0` as active neutral versus null;
- pending target versus executed state;
- exact boundary versus interior resonance coordinate;
- exact `2:1` composition versus `67/33`;
- hold versus committed self-transition.

---

## 141. No Test Tailoring to Implementation Error

Expected invariant values must not be changed merely to match an incorrect implementation.

The invariant contract determines the expected behavior.

Implementation must be corrected when it violates the contract.

---

## 142. No Implementation Tailoring to Test Artifact

A test that contradicts the approved invariant contract must itself be corrected.

Passing an incorrect test is not validation.

---

## 143. Invariant Priority

When documentation, implementation, and tests disagree, resolution requires identifying the authoritative contract for that invariant.

The inconsistency must not be resolved by similarity or convenience.

---

## 144. Formal and Executable Correspondence

A formal invariant may have an executable specialization.

The executable invariant may be narrower than the formal statement.

That restriction must remain explicit.

---

## 145. Scientific Boundary

An invariant may establish architecture or numerical correctness without establishing physical truth.

For example:

`mass conserved by coarse reduction`

does not prove that the selected coarse model is physically complete.

---

## 146. Release Invariant Audit

Before release, invariant audit must verify:

- all declared core invariants have qualification evidence;
- no known failing invariant is hidden;
- no stale test encodes superseded semantics;
- schemas and runtime invariants are compatible;
- CI executes required suites;
- active-neutral semantics remain preserved;
- no direct opposite ternary transition has been introduced;
- public claims match evidence scope.

---

## 147. Core Invariant Catalogue

The release-level core catalogue includes at least:

1. canonical `-1/0/1`;
2. active neutral `0`;
3. direct opposite-transition prohibition;
4. active-neutral mediated routing;
5. target/executed separation;
6. pending/executed separation;
7. missing/invalid separation from `0`;
8. atomic configuration cardinality;
9. finite geometry;
10. valid periodic cell;
11. deterministic graph structure;
12. continuous resonance-state validity;
13. phase-order range;
14. nonnegative frequency spread;
15. resonance/ternary separation;
16. E(3) scalar invariance;
17. E(3) vector equivariance;
18. energy-state finiteness;
19. energy aggregation;
20. force-gradient sign;
21. stress convention;
22. trace ordering;
23. trace cardinality;
24. deterministic replay;
25. root schema-set validity;
26. multiscale mass conservation;
27. no arithmetic ternary averaging;
28. explicit uncertainty propagation;
29. explicit thermodynamic-validation status;
30. FLiBe composition identity;
31. FLiBe provenance boundaries;
32. split isolation;
33. FLiBe resonance/ternary independent pathways;
34. benchmark contract integrity.

---

## 148. Related Validation Documents

This plan operates together with:

`docs/validation/scientific_validation_plan.md`

`docs/validation/mathematical_validation_plan.md`

`docs/validation/numerical_validation_plan.md`

and the remaining validation artifacts:

`docs/validation/reproducibility_plan.md`

`docs/validation/flibe_validation_matrix.md`

Each artifact covers a different validation dimension.

---

## 149. Non-Claims

Invariant validation does not by itself establish:

- theorem proof;
- experimental accuracy;
- first-principles accuracy;
- material transmutation;
- physical completeness;
- universal runtime complexity;
- universal memory complexity;
- complete uncertainty calibration.

Each of those claims requires its own evidence path.

---

## 150. Summary

TR-EIF invariant validation protects the semantic and executable structure of the framework.

The invariant chain is:

`declared invariant`

`→ formal or architectural contract`

`→ executable specialization`

`→ qualification test`

`→ clean-runner execution`

`→ regression protection`

The framework preserves exact distinctions such as:

`-1/0/1`

`active neutral 0 ≠ missing`

`target ≠ executed state`

`pending ≠ active neutral`

`resonance ≠ synchronization`

`resonance region ≠ ternary state`

`energy ≠ ternary state`

`force ≠ ternary state`

`validation status ≠ ternary state`

and:

`similar ≠ identical`

An invariant is qualified only when the implementation and validation evidence preserve the exact relation declared by the corresponding contract.
