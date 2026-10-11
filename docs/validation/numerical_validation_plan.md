# Numerical Validation Plan

## 1. Scope

This document defines the repository-level numerical validation plan of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The plan applies to numerical realization of:

- resonance dynamics;
- continuous descriptor evaluation;
- balanced-ternary execution;
- E(3)-equivariant mappings;
- conservative energy;
- force differentiation;
- stress differentiation;
- molecular-dynamics integration;
- periodic geometry;
- multiscale reductions;
- deterministic replay;
- FLiBe-specific TR-EIP execution;
- benchmarks;
- source-backed property reproduction.

This document validates numerical realization.

It does not replace mathematical proof.

It does not establish physical accuracy without independent physical evidence.

---

## 2. Numerical Validation Objective

Numerical validation determines whether an executable approximation behaves consistently with its declared mathematical and computational contract.

The validation chain is:

`mathematical relation`

`→ numerical method`

`→ discretization parameters`

`→ executable result`

`→ error or invariant measurement`

`→ fixed acceptance criterion`

`→ validation status`

---

## 3. Numerical Validation Is Not Mathematical Proof

A convergent numerical approximation does not prove the corresponding theorem.

Therefore:

`numerical convergence ≠ theorem proof`

and:

`numerical agreement ≠ mathematical identity`

Mathematical proof remains governed by:

`docs/validation/mathematical_validation_plan.md`

---

## 4. Numerical Validation Is Not Physical Validation

A numerically stable implementation may still represent an inaccurate physical model.

Therefore:

`numerical stability ≠ physical accuracy`

and:

`small numerical error ≠ experimental agreement`

Physical validation requires independent reference evidence.

---

## 5. Validation Status Is Not Ternary State

Numerical validation results such as:

- PASS;
- FAIL;
- unresolved;
- not evaluated

are not balanced-ternary execution states.

Therefore:

`PASS ≠ 1`

`FAIL ≠ -1`

`UNRESOLVED ≠ 0`

Active neutral `0` remains an execution state.

---

## 6. Fixed Validation Contract

Every numerical validation must declare before execution:

- numerical method;
- input state;
- numerical parameters;
- reference relation;
- observable;
- error metric;
- tolerance or convergence criterion;
- comparison domain.

The validation contract must not be changed after observing the result solely to obtain PASS.

---

## 7. No Post-Hoc Tolerance Selection

A tolerance selected after observing the error is not an independent validation criterion.

Therefore:

`observed error → chosen tolerance`

is not an acceptable qualification procedure.

The required order is:

`tolerance or convergence criterion`

`→ execution`

`→ observed error`

`→ result`

---

## 8. Exact vs Numerical Comparison

Exact equality must be used when the contract requires exact identity.

Examples include:

- ternary state values;
- enum identities;
- node cardinality;
- deterministic ordering;
- schema constants;
- structured-output fields.

Approximate comparison is permitted only where finite numerical realization requires it.

---

## 9. Floating-Point Boundary

The executable Python reference uses finite-precision floating-point arithmetic.

Therefore mathematical real-number identities and executable bitwise equality are distinct concepts.

Numerical validation must identify when:

- exact equality is expected;
- floating-point tolerance is required;
- convergence rather than one-step equality is the correct criterion.

---

## 10. Finiteness

Every numerical state that requires finite real values must reject:

- NaN;
- positive infinity;
- negative infinity.

Nonfinite values are numerical failures.

They must not be encoded as active-neutral ternary state `0`.

---

## 11. Active Neutral Is Not Numerical Zero

Balanced-ternary state:

`0`

is active neutral.

A continuous numerical quantity equal to:

`0.0`

does not automatically have active-neutral semantics.

Therefore:

`numeric zero ≠ active neutral state`

---

## 12. Numerical Failure Is Not Active Neutral

A failed computation, NaN, overflow, unavailable output, or unresolved convergence result must remain outside the balanced ternary state domain.

Therefore:

`numerical failure ≠ ternary 0`

---

## 13. Resonance-State Numerical Validation

Numerical validation of `ResonanceState` includes:

- finite phases;
- finite frequencies;
- nonempty vectors;
- equal cardinality;
- deterministic phase wrapping;
- stable descriptor construction.

---

## 14. Phase Wrapping

Phase normalization maps finite phases into:

`[0, 2π)`

Validation must include values:

- inside the interval;
- below zero;
- above `2π`;
- multiple turns away from the canonical interval.

Equivalent wrapped phases must represent the same angular state.

---

## 15. Phase-Order Numerical Validation

The executable phase-order observable must satisfy:

`0 ≤ R ≤ 1`

within finite arithmetic.

Validation should include:

- aligned phases;
- symmetric cancellation;
- nontrivial partial order;
- wrapped equivalent phases.

---

## 16. Phase Order Is Not Complete Coherence

Numerical testing of `R` validates the phase-order calculation.

It does not validate complete coherence.

Therefore:

`phase-order numerical test ≠ complete-coherence validation`

---

## 17. Frequency-Spread Validation

Frequency spread must satisfy:

`σ_ω ≥ 0`

Validation should include:

- identical frequencies;
- symmetric frequency sets;
- translated frequency sets;
- nonuniform distributions.

Zero spread does not establish resonance.

---

## 18. Descriptor Determinism

For identical finite `ResonanceState` input, descriptor construction must reproduce identical output under the declared deterministic environment.

No hidden random state is permitted.

---

## 19. Resonance-Window Numerical Boundary

The current executable window uses exact numerical boundary equality.

Therefore numerical validation must distinguish:

- exact boundary;
- strict interior;
- strict exterior.

A tolerance band must not be silently added.

---

## 20. Window Classification Is Not Ternary Classification

Numerical validation must preserve:

`OUTSIDE/BOUNDARY/INSIDE ≠ automatically -1/0/1`

The classifier output and ternary state remain separate numerical domains.

---

## 21. Ternary Execution Numerical Validation

Balanced-ternary execution is discrete.

Its state values require exact comparison:

`-1`

`0`

`1`

No floating-point tolerance is appropriate for ternary state identity.

---

## 22. Direct Opposite Transition Validation

The committed transitions:

`-1 → 1`

and:

`1 → -1`

must fail exactly as prohibited transitions.

The admissible routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

with separate execution events.

---

## 23. Active-Neutral Residence Validation

Validation must include the case where:

`retained_state = 0`

and a pending target persists across more than one execution opportunity.

Numerical or execution code must not force immediate neutral exit.

---

## 24. Pending Target Validation

Pending-target behavior requires exact discrete comparison.

Validation must preserve:

`pending target ≠ executed state`

and:

`pending target ≠ 0`

A pending target is valid only with retained active neutral.

---

## 25. Hold vs Committed Retention

Numerical/execution validation must distinguish:

`route = None`

from a committed:

`0 → 0`

or other self-transition.

Numerical equality of previous and current state does not establish event identity.

---

## 26. E(3) Numerical Validation

E(3) numerical validation must separately test:

- translation;
- rotation;
- reflection.

The selected transformation must be applied consistently to all affected geometric or equivariant quantities.

---

## 27. Scalar Invariance Error

For scalar invariant quantity:

`s`

an E(3) test may measure:

`|s_transformed - s_reference|`

The tolerance must be fixed before execution.

---

## 28. Vector Equivariance Error

For polar vectors, validation compares transformed reference vectors against vectors computed from the transformed system.

A componentwise or norm-based error metric must be explicitly declared.

---

## 29. Energy E(3) Validation

Scalar total energy must remain invariant under admissible E(3) transformations within the declared numerical tolerance.

The tolerance must reflect numerical arithmetic, not desired output.

---

## 30. Force E(3) Validation

Forces must transform according to the declared polar-vector representation.

Force equivariance must not be replaced by mere equality of vector magnitudes.

---

## 31. Reflection Validation

Because the framework declares E(3), not only proper rotations, reference validation includes reflection where the executable representation supports it.

A test suite restricted only to rotations does not fully establish E(3) behavior.

---

## 32. Energy Numerical Validation

Energy validation includes:

- finite atomic energies;
- finite total energy;
- correct atomic cardinality;
- deterministic aggregation;
- declared scalar-channel width;
- E(3) invariance.

---

## 33. Energy Summation

For the canonical `EnergyState.from_atomic_energies` constructor:

`E_total = Σ E_i`

Validation may check exact executable summation for the fixed ordered tuple.

This executable equality is distinct from mathematical associativity over real numbers.

---

## 34. Force-Gradient Validation

The conservative force contract is:

`F = -dE/dr`

The executable reference uses central finite differences.

Numerical validation must compare force estimates under controlled differentiation-step refinement.

---

## 35. Coordinate Differentiation Step

The coordinate differentiation step:

`h`

must be:

- finite;
- positive.

Validation must reject:

- zero step;
- negative step;
- NaN;
- infinity.

---

## 36. Central-Difference Formula

For one coordinate:

`x`

the central derivative approximation is based on:

`E(x + h)`

and:

`E(x - h)`

The conservative force applies the negative derivative sign.

---

## 37. Expected Convergence Order

For sufficiently smooth energy and an appropriate step regime, central difference exhibits second-order truncation behavior.

Under step halving, the asymptotic error ratio approaches approximately:

`4`

until floating-point error becomes dominant.

---

## 38. Convergence Is a Regime Property

Second-order convergence must not be required at arbitrarily small step sizes.

At sufficiently small:

`h`

floating-point cancellation may dominate.

Therefore convergence validation must use an explicitly selected refinement regime.

---

## 39. Independent Reference for Convergence

A convergence benchmark may use a substantially finer fixed numerical estimate as a reference when no analytic derivative exists.

The reference step must be declared before evaluation.

It must not be changed after observing the convergence curve.

---

## 40. Fixed-Graph Force Differentiation

The current force evaluator holds graph topology fixed during paired plus/minus coordinate evaluations.

Numerical validation of this evaluator must preserve that scope.

---

## 41. Graph Rebuild Boundary

Graph topology may be rebuilt between separate physical states.

A validation must not conflate:

`fixed graph inside one derivative`

with:

`fixed graph throughout all dynamics`

---

## 42. Feature State during Force Differentiation

The reference force evaluator holds the supplied input feature state fixed while evaluating coordinate perturbations.

Validation must not silently recompute another feature state unless testing a different higher-level model.

---

## 43. Ternary State during Force Differentiation

The retained ternary execution vector remains fixed during one paired force derivative.

No hidden ternary transition occurs between plus and minus evaluations.

---

## 44. Resonance State during Force Differentiation

The reference force evaluator does not independently evolve resonance state during plus/minus coordinate perturbations.

A coupled geometry-resonance derivative would be a different numerical contract.

---

## 45. Stress Numerical Validation

The declared stress convention is:

`stress = +(1/V) dE/dε`

under the repository strain convention.

Numerical validation must preserve:

- sign;
- strain definition;
- reference volume;
- graph scope.

---

## 46. Strain Differentiation Step

The strain differentiation step must be:

- finite;
- positive.

The same step must be used consistently in the plus and minus evaluations for one component.

---

## 47. Cell Volume Validation

The reference cell volume is derived from:

`abs(det(cell))`

The volume must be nonzero.

Stress validation must reject singular cells.

---

## 48. Symmetric Stress Validation

The current stress evaluator returns a symmetric tensor by construction.

Validation must check off-diagonal consistency where applicable.

---

## 49. Stress Sign Validation

A numerical result with the opposite sign convention must not be accepted merely because its magnitude matches.

The sign convention is part of the validation contract.

---

## 50. Molecular-Dynamics Numerical Validation

The current reference MD integrator uses velocity-Verlet.

Validation must specify:

- initial state;
- masses;
- time step;
- number of steps;
- force evaluator;
- graph construction;
- feature state;
- ternary execution state.

---

## 51. Positive Time Step

MD time step:

`Δt`

must be finite and positive.

Zero or negative time step is invalid.

---

## 52. Mass Validation

Every MD mass must be finite and positive.

Zero, negative, NaN, or infinite mass is invalid.

---

## 53. Velocity-Verlet State Update

Numerical validation must check consistency of:

- position update;
- force evaluation;
- velocity update;
- state cardinality.

The integrator must not alter species identity or atom count.

---

## 54. MD Determinism

For identical deterministic inputs and identical numerical environment, repeated velocity-Verlet execution must reproduce the same trajectory.

---

## 55. Hidden Resonance Evolution Prohibition

The current generic MD step does not evolve resonance state internally.

Validation must confirm that resonance changes only through explicitly composed resonance propagation.

---

## 56. Hidden Ternary Evolution Prohibition

The current generic MD step does not execute ternary transitions internally.

Validation must confirm that retained ternary state changes only through explicit ternary execution.

---

## 57. Energy Drift

For an isolated conservative benchmark trajectory, numerical total-energy drift may be measured as:

`E_total(t) - E_total(0)`

The drift criterion must be tied to:

- model;
- time step;
- trajectory length;
- force differentiation;
- graph semantics.

---

## 58. Drift Is Not Universally Zero

Finite numerical integration generally need not preserve exact bitwise total energy at every step.

Therefore:

`finite numerical drift ≠ automatically implementation failure`

The declared benchmark bound determines qualification.

---

## 59. Drift Threshold Must Be Fixed

An energy-drift threshold must be fixed before trajectory evaluation.

It must not be widened after observing the trajectory.

---

## 60. Numerical Stability

A numerical execution is stable under a declared test when bounded perturbations do not produce unacceptable numerical growth under the selected method and domain.

Stability claims must identify:

- perturbed quantity;
- perturbation magnitude;
- time or iteration horizon;
- stability metric.

---

## 61. Stability Is Method-Relative

A numerical method may be stable for one time step and unstable for another.

Therefore:

`method name alone ≠ stability proof`

The selected discretization parameters matter.

---

## 62. Convergence Is Not Stability

A method may be consistent and convergent under one regime while still exhibiting instability outside that regime.

Therefore:

`convergence ≠ stability`

---

## 63. Stability Is Not Physical Validity

A numerically stable trajectory may still describe an invalid physical model.

Therefore:

`numerical stability ≠ physical validity`

---

## 64. Periodic Geometry Numerical Validation

Periodic geometry validation must check:

- finite cell values;
- nonzero determinant;
- periodic-axis semantics;
- fractional coordinate transformation;
- Cartesian reconstruction.

---

## 65. Minimum-Image Boundary

The current implementation uses componentwise wrapping in fractional coordinates.

Validation must not claim that this always yields the globally shortest image for strongly skewed cells.

Therefore:

`componentwise wrapped image ≠ universally shortest skew-cell image`

---

## 66. Nonperiodic Axis Validation

A nonperiodic axis must not be wrapped.

Mixed periodic-axis configurations require axis-specific numerical tests.

---

## 67. Neighbor Graph Validation

Graph construction validation includes:

- node cardinality;
- cutoff application;
- deterministic edge ordering;
- periodic geometry where enabled;
- finite edge geometry.

---

## 68. Cutoff Boundary Cases

Validation should include distances:

- below cutoff;
- exactly at the declared inclusion boundary according to implementation semantics;
- above cutoff.

The boundary relation must match executable code exactly.

---

## 69. Empty Graph Boundary

Where an executable layer does not support an empty interaction graph, numerical validation must preserve that limitation.

A passing nonempty-graph test does not establish empty-graph support.

---

## 70. Deterministic Accumulation

Where accumulation order affects finite arithmetic, the implementation uses canonical ordering where declared.

Validation should detect order-dependent drift when deterministic order is part of the contract.

---

## 71. Multiscale Numerical Validation

Multiscale numerical validation includes:

- partition cardinality;
- mass conservation;
- centroid calculation;
- vector reduction;
- vector averaging;
- prolongation;
- partition composition;
- hierarchy construction.

---

## 72. Mass Conservation

For fine masses:

`m_i`

and coarse masses:

`M_c`

validation requires:

`Σ M_c = Σ m_i`

within the declared numerical relation.

---

## 73. Mass-Weighted Centroid

Centroid validation must compare the executable result against:

`R_c = (Σ m_i r_i) / (Σ m_i)`

with positive finite masses.

---

## 74. Periodic Coarse-Graining Boundary

The current centroid implementation performs no hidden periodic unwrapping.

A test requiring physical periodic centroid behavior must provide an explicitly unwrapped coordinate representation.

---

## 75. Vector Reduction vs Average

Numerical validation must distinguish:

`vector sum`

from:

`mass-weighted vector average`

They are different operators.

One must not be validated against the other's expected result.

---

## 76. Ternary Averaging Prohibition

Numerical code must not treat ternary states as ordinary continuous numbers for coarse averaging.

Therefore:

`(-1 + 1) / 2 = 0`

does not numerically validate active-neutral coarse state.

---

## 77. Reduction-Prolongation Validation

Validation may test whether:

`Q(R(x))`

satisfies a declared projection property.

It must not assume exact reconstruction unless that property is explicitly defined.

---

## 78. Transport Transfer Numerical Validation

Transport transfer validation must check:

- finite source value;
- finite target value;
- declared source identity;
- target scale;
- deterministic provider output.

It must not silently introduce unit conversion.

---

## 79. Thermodynamic Consistency Numerical Boundary

A Boolean thermodynamic-consistency status is not a numerical ternary state.

Therefore:

`True ≠ 1`

`False ≠ -1`

---

## 80. Uncertainty Numerical Validation

Uncertainty values must be finite and nonnegative under the current generic representation.

Validation must preserve:

- representation identifier;
- scale;
- source;
- propagation context.

---

## 81. Uncertainty Is Not Numerical Error Itself

A stored uncertainty measure and observed numerical error are distinct quantities.

They may be compared only through an explicit uncertainty-validation relation.

---

## 82. FLiBe Numerical Validation

FLiBe numerical validation adds material-specific domain checks.

It must preserve:

- exact species counts;
- composition;
- thermodynamic state;
- provenance;
- source range;
- material-specific model context.

---

## 83. Composition Arithmetic

Composition fractions must reproduce the exact species/formula-unit relation represented by the selected composition model.

Rounded source composition must remain distinguishable from exact stoichiometric composition.

---

## 84. Property-Correlation Reproduction

A source-backed property equation may be evaluated at pinned temperatures inside its stated validity range.

Reference points should be independently calculated and fixed before benchmark execution.

---

## 85. Density Reproduction

For the currently registered source-derived density relation:

`rho(T) = 2413 - 0.488 T`

validation must retain:

- units;
- source identifier;
- source composition;
- temperature range;
- `DERIVED` provenance.

---

## 86. Property Domain Enforcement

Source-derived physical models must reject or explicitly flag inputs outside their declared domain when the executable contract requires strict domain enforcement.

Extrapolation must not be presented as source-qualified reproduction.

---

## 87. Structural Observable Numerical Validation

Numerical comparison of structural observables must preserve compatible:

- coordinate axis;
- normalization;
- units;
- composition;
- temperature;
- state.

Interpolation or resampling must be explicit.

---

## 88. Experimental Comparison

Experimental comparison must not alter source data to improve agreement.

Preprocessing must be documented and deterministic.

---

## 89. First-Principles Comparison

First-principles numerical comparison must preserve the actual computational reference method and sampled state.

It must not be relabeled as experimental evidence.

---

## 90. Direct Comparison Compatibility

A strict direct comparison requires matched:

- observable;
- composition;
- thermodynamic state;
- physical state;
- units;
- normalization;
- axis;
- sample cardinality.

---

## 91. Residual Sign

Where residual is defined as:

`calculated - reference`

the sign convention must remain unchanged across the comparison suite.

---

## 92. MAE Validation

Mean absolute error is:

`MAE = mean(|residual|)`

The executable calculation must use all declared comparison samples.

---

## 93. RMSE Validation

Root-mean-square error is:

`RMSE = sqrt(mean(residual²))`

The sample population and normalization convention must remain explicit.

---

## 94. Maximum Absolute Error

Maximum absolute error is:

`max(|residual|)`

It must not be confused with MAE or RMSE.

---

## 95. Benchmark Correctness

Correctness benchmarks use fixed inputs and pinned expected invariants or outputs.

Pinned reference values must not be updated merely because implementation output changed.

A reference change requires justification.

---

## 96. Determinism Benchmark

A determinism benchmark repeats identical execution.

For byte-deterministic output:

`bytes_run_1 = bytes_run_2`

must hold exactly.

---

## 97. Equivariance Benchmark

Equivariance benchmarks compare transformed-model outputs with transformed reference outputs.

Energy uses scalar invariance.

Forces use vector equivariance.

---

## 98. Conservation Benchmark

Conservation benchmarks record:

- initial energy;
- final energy;
- signed drift;
- maximum absolute drift;
- energy series.

The benchmark tolerance must remain fixed.

---

## 99. Numerical-Convergence Benchmark

A convergence benchmark records:

- refinement steps;
- error at each step;
- error-reduction ratios;
- final error;
- reference step.

A PASS requires all declared checks, not visual appearance of convergence.

---

## 100. Scaling Benchmark

Structural scaling benchmark validates quantities such as:

- atom count;
- edge count;
- energy cardinality;
- extensive total energy for isolated replicated systems;
- invariant channel width.

This is distinct from runtime scaling.

---

## 101. Memory Benchmark

Memory benchmark evidence is runner-dependent measurement.

The current benchmark uses Python `tracemalloc`.

The benchmark may validate:

- positive measurement;
- internal arithmetic consistency;
- structural sample identity.

It must not impose an arbitrary universal memory threshold.

---

## 102. Runtime Benchmark

Runtime evidence depends on:

- machine;
- load;
- Python build;
- OS;
- runner scheduling;
- cache state.

The current runtime benchmark records measurements but does not use a hard runtime threshold as a correctness invariant.

---

## 103. Runtime Monotonicity Is Not a Correctness Invariant

On shared runners, a larger sample may occasionally time faster than a smaller sample due to infrastructure noise.

Therefore:

`runtime monotonicity ≠ correctness requirement`

unless measured under a separately controlled benchmarking environment.

---

## 104. Warm-Up

Runtime benchmarking should separate warm-up executions from measured executions where the benchmark contract declares warm-up.

Warm-up runs must not be silently included in measurement statistics.

---

## 105. Median Runtime

Median runtime is robust to isolated outliers.

The benchmark must calculate it from the declared measurement set.

The median is evidence.

It is not a universal execution-time constant.

---

## 106. Benchmark Structured Output

Numerical benchmarks should emit structured JSON containing:

- benchmark identifier;
- provenance;
- status;
- parameters;
- checks;
- observed values.

Unstructured logging must not contaminate byte-deterministic output benchmarks.

---

## 107. Benchmark Exit Status

A benchmark with failed declared correctness checks must return nonzero process status when it is used as a CI gate.

A measurement-only quantity without a correctness threshold must not fail merely because its measured magnitude changed.

---

## 108. CI Numerical Validation

CI executes numerical tests on a clean runner.

This provides independent execution evidence.

CI runner results must still be interpreted according to the declared benchmark contract.

---

## 109. Local vs CI Numerical Results

Exact deterministic outputs should agree where the contract requires identity.

Runtime and memory magnitudes may differ.

Therefore:

`runtime_local ≠ necessarily runtime_CI`

and:

`memory_local ≠ necessarily memory_CI`

---

## 110. Regression Detection

A numerical regression occurs when a previously satisfied fixed validation criterion fails under unchanged declared semantics.

The criterion must not be weakened automatically.

---

## 111. Intended Numerical Change

If a numerical method is deliberately changed, affected references and tolerances must be reviewed against the new mathematical/numerical contract.

Reference outputs must not be mechanically regenerated without analysis.

---

## 112. Sensitivity Analysis

Where appropriate, numerical validation may vary:

- time step;
- differentiation step;
- cutoff;
- system size;
- perturbation magnitude.

Sensitivity results must not be presented as independent physical parameters.

---

## 113. Cutoff Sensitivity Boundary

Changing graph cutoff may alter graph topology and model output.

Cutoff sensitivity is a model/numerical study.

It must not be confused with finite-difference convergence at fixed graph topology.

---

## 114. Step Refinement Boundary

Coordinate differentiation refinement changes:

`h`

It must not simultaneously change unrelated inputs if the purpose is to isolate differentiation convergence.

---

## 115. MD Time-Step Refinement

An MD convergence study may compare trajectories at decreasing:

`Δt`

but comparison requires a declared common observable and time horizon.

Different numbers of steps alone are not directly comparable without matching physical time.

---

## 116. Long-Time Dynamics

Short-step numerical correctness does not establish long-time stability.

Long-time claims require dedicated trajectory length and stability evidence.

---

## 117. Chaotic Sensitivity Boundary

For nonlinear dynamical systems, trajectory pointwise divergence may occur even when numerical/statistical behavior remains valid.

A validation contract must choose observables appropriate to the system.

Exact long-time trajectory identity must not be assumed without justification.

---

## 118. Resonance Integration

The current resonance reference integrator includes explicit numerical time evolution.

Validation must distinguish:

- derivative correctness;
- one-step integration correctness;
- multi-step stability;
- descriptor evolution.

---

## 119. Resonance Integration Step

A resonance integration step must use a declared positive finite time step.

The integrator must preserve phase wrapping according to its implementation contract.

---

## 120. Delay vs Phase Lag

Numerical code must not interchange delay and phase lag.

Therefore:

`delay ≠ phase lag`

unless the model explicitly derives one from the other.

---

## 121. Classifier Temperature Boundary

Any numerical classifier parameter called temperature remains distinct from thermodynamic temperature unless explicitly mapped.

Therefore:

`classifier temperature ≠ thermodynamic temperature`

---

## 122. High Entropy Boundary

A numerically high entropy value does not automatically indicate active neutral state.

Therefore:

`high entropy ≠ active neutral`

---

## 123. Numerical Error and Uncertainty

Observed numerical discretization error and modeled uncertainty are distinct.

A numerical error estimate may contribute to an uncertainty model only through an explicit mapping.

---

## 124. Reproducibility of Numerical Parameters

Every result-sensitive numerical parameter must be recoverable from:

- code;
- configuration;
- manifest;
- benchmark;
- or documented execution contract.

Hidden defaults that alter results undermine reproducibility.

---

## 125. Default Parameter Audit

Defaults such as:

- differentiation step;
- strain step;
- cutoff;
- time step

must be audited before release when they affect scientific results.

A default value is not automatically a physically validated value.

---

## 126. Unit Consistency

Numerical values representing physical quantities require consistent units.

A numerically correct computation using mismatched units is physically invalid.

---

## 127. Overflow and Underflow

Tests should detect numerical states that exceed representable or meaningful ranges where applicable.

Silent overflow must not become a valid model state.

---

## 128. Cancellation

Central differences at very small step sizes may suffer subtractive cancellation.

Convergence validation must recognize this numerical limit.

---

## 129. Conditioning

Numerical conditioning of an operation is distinct from ternary feature conditioning.

Therefore:

`numerical conditioning ≠ ternary conditioning`

The same word must not collapse the two meanings.

---

## 130. Algorithmic Complexity Boundary

Observed runtime at several sizes does not by itself prove asymptotic complexity.

An asymptotic complexity claim requires algorithmic analysis or sufficiently controlled scaling evidence.

---

## 131. Memory Complexity Boundary

Observed traced allocation at several sizes does not by itself prove asymptotic memory complexity.

It is empirical benchmark evidence for those measured sizes.

---

## 132. Cross-Model Numerical Comparison

Cross-model comparison requires identical or explicitly mapped:

- input system;
- observable;
- unit;
- state domain;
- numerical conditions.

Different numerical methods must remain identified.

---

## 133. FRP Boundary

FRP may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

Numerical validation must not import:

- FRP RTL implementation;
- FRP scheduler modes;
- FRP-specific numerical coefficients;
- FRP module topology

into TR-EIF unless a specific correspondence is separately established.

---

## 134. Numerical Correspondence Is Not Architectural Identity

Even when two implementations produce matching outputs under a test:

`matching result ≠ identical architecture`

Validation claims must remain bounded to the tested correspondence.

---

## 135. Core Numerical Validation Invariants

The numerical validation layer preserves the following invariants:

1. Numerical methods are declared before evaluation.
2. Tolerances are fixed before observing results.
3. Exact discrete identities are not replaced by floating tolerances.
4. NaN and infinity are invalid where finite state is required.
5. Numerical failure is not active neutral `0`.
6. Resonance descriptors remain continuous.
7. Ternary states remain exact `-1/0/1`.
8. Direct opposite ternary transitions remain prohibited.
9. Active-neutral residence remains valid.
10. E(3) scalar invariance and vector equivariance are tested separately.
11. Energy remains scalar.
12. Force follows the negative energy gradient.
13. Stress retains the declared positive strain-derivative convention.
14. Graph topology remains fixed inside the current local force/stress derivative.
15. Graph topology may rebuild between physical states.
16. Central-difference convergence is evaluated in a declared refinement regime.
17. Velocity-Verlet uses declared positive finite time step and masses.
18. Generic MD does not silently evolve resonance or ternary state.
19. Energy drift is benchmark-specific.
20. Periodic geometry does not claim universal shortest image for skew cells.
21. Multiscale mass reduction preserves represented total mass.
22. Ternary states are not numerically averaged.
23. Property reproduction remains source-domain constrained.
24. Runtime and memory magnitudes are environment-dependent.
25. Benchmark correctness and benchmark measurement remain distinct.
26. CI success means only that the configured numerical contract passed.
27. Numerical stability does not establish physical validity.
28. Numerical convergence does not establish theorem proof.
29. Similar numerical values do not establish semantic identity.
30. Hidden result-affecting numerical parameters are prohibited under strict reproducibility.

---

## 136. Numerical Validation Evidence

Numerical validation evidence includes:

- pytest qualification tests;
- structured benchmark JSON;
- convergence sequences;
- energy-drift traces;
- equivariance residuals;
- deterministic replay comparisons;
- CI reports;
- source-backed property residuals.

Each evidence artifact must be interpreted only under its declared contract.

---

## 137. Related Validation Documents

This plan operates together with:

`docs/validation/scientific_validation_plan.md`

`docs/validation/mathematical_validation_plan.md`

and the planned:

`docs/validation/invariant_validation_plan.md`

`docs/validation/reproducibility_plan.md`

`docs/validation/flibe_validation_matrix.md`

---

## 138. Release Numerical Audit

Before release, numerical validation must audit:

- complete test suite;
- benchmark execution;
- deterministic outputs;
- convergence evidence;
- force-gradient consistency;
- stress consistency;
- MD stability evidence;
- schema-linked structured output;
- fixed tolerances;
- result-affecting defaults.

---

## 139. Non-Claims

This numerical validation plan does not assert that:

- numerical convergence proves physical truth;
- numerical stability proves scientific validity;
- benchmark runtime proves asymptotic complexity;
- memory measurement proves universal resource requirements;
- one FLiBe property reproduction validates all FLiBe properties;
- one energy-drift benchmark validates all trajectories.

Each claim remains bounded to its actual evidence.

---

## 140. Summary

TR-EIF numerical validation verifies that executable approximations correspond to their declared numerical contracts without post-hoc fitting of acceptance criteria.

The numerical chain is:

`formal relation`

`→ explicit discretization`

`→ fixed numerical parameters`

`→ execution`

`→ structured error or invariant measurement`

`→ predeclared criterion`

`→ validation result`

The repository preserves:

`numerical agreement ≠ proof`

`numerical stability ≠ physical accuracy`

`numeric zero ≠ active neutral 0`

`runtime variation ≠ correctness failure`

`memory variation ≠ correctness failure`

`convergence ≠ stability`

and:

`similar ≠ identical`

A numerical result is qualified only when the numerical method, inputs, comparison relation, and acceptance criterion were explicit before the result was evaluated.
