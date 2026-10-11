# Energy Output Specification

## 1. Scope

This document defines the repository-level energy output specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- scalar energy output;
- atomic energy contributions;
- total energy;
- conservative energy semantics;
- energy-model output structure;
- invariant scalar functional input;
- resonance-conditioning boundary;
- balanced-ternary conditioning boundary;
- retained-state semantics;
- geometry and graph dependencies;
- E(3) invariance requirements;
- deterministic aggregation;
- force derivation;
- stress derivation;
- fixed-graph numerical differentiation;
- output serialization;
- unit boundary;
- provenance boundary;
- numerical validity;
- validation requirements;
- executable reference correspondence.

The architecture contract is defined in:

`docs/architecture/energy_model_contract.md`

The formal energy model is developed in:

`docs/volume_03_equivariant_interatomic_framework/chapter_08_conservative_energy_functional.md`

Force and stress semantics are developed in:

`docs/volume_03_equivariant_interatomic_framework/chapter_09_forces_and_stress.md`

The structural JSON representation is defined by:

`schemas/energy_output.schema.json`

---

## 2. Energy Output Domain

Energy output belongs to a continuous scalar physical domain.

A total energy is represented as:

`E_total ∈ R`

subject to finite numerical representation.

Energy is not a balanced-ternary state.

Therefore:

`energy ≠ ternary state`

---

## 3. Reference Energy Output

The executable reference energy representation is:

`EnergyState`

with fields:

- `atomic_energies`;
- `total_energy`.

The representation is immutable after construction.

---

## 4. Atomic Energy Contributions

For a configuration containing:

`N`

represented atoms, the reference atomic-energy vector is:

`E_atomic = (E_1, E_2, ..., E_N)`

Each:

`E_i`

is a finite real scalar.

The executable type alias is:

`AtomicEnergies`

---

## 5. Atomic Contribution Cardinality

The atomic-energy vector must be nonempty.

For an `EnergyModelResult`, its cardinality must equal the node count of the conditioned equivariant layer result.

Therefore:

`energy.atom_count = layer_result.current.node_count`

---

## 6. Total Energy

The total energy is one finite scalar:

`E_total`

The canonical constructor:

`EnergyState.from_atomic_energies(...)`

defines:

`E_total = Σ E_i`

using the deterministic tuple order supplied to the constructor.

---

## 7. Atomic Energy Is a Model Decomposition

An atomic energy contribution is part of the selected energy decomposition.

It is not automatically an independently measurable physical observable.

Therefore:

`atomic contribution ≠ independently measured atomic energy`

unless a concrete physical model establishes that interpretation.

---

## 8. Energy Is Not Ternary State

The balanced ternary labels:

`-1`

`0`

`1`

are execution states.

They are not energy values.

Therefore:

`-1 ≠ negative energy by definition`

`0 ≠ zero energy by definition`

`1 ≠ positive energy by definition`

---

## 9. Active Neutral Is Not Zero Energy

Active neutral state:

`0`

may support:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Those semantics do not mean:

`E = 0`

Therefore:

`active neutral 0 ≠ zero energy`

---

## 10. Zero Energy Is Not Active Neutral

A physical or model energy may numerically equal:

`0`

This does not create balanced-ternary active-neutral semantics.

Therefore:

`energy zero ≠ ternary neutral 0`

---

## 11. Energy Sign Is Not Ternary Polarity

The sign of energy does not define ternary polarity.

Therefore:

`negative energy ≠ ternary -1`

and:

`positive energy ≠ ternary 1`

A concrete target-generation mapping may use energy-derived information only when that mapping is explicitly defined.

---

## 12. Missing Energy Is Not Active Neutral

Missing or unavailable energy output must not be encoded as:

`0`

Missing energy is represented separately.

In serialized observable records, absence may be represented as:

`null`

Therefore:

`missing energy ≠ active neutral`

---

## 13. Invalid Energy Is Not Active Neutral

An invalid, NaN, infinite, failed, or unavailable energy calculation remains outside the balanced-ternary state space.

Therefore:

`invalid energy ≠ ternary 0`

`NaN ≠ ternary 0`

`numerical failure ≠ ternary 0`

---

## 14. Reference Energy Model

The executable reference interatomic energy model is:

`ReferenceEnergyModel`

Its stored components are:

- `RadialMessageOperator`;
- `TernaryConditioning`;
- `LinearInvariantEnergyFunctional`.

Its output type is:

`EnergyModelResult`

---

## 15. Energy Model Result

`EnergyModelResult` contains:

- `layer_result`;
- `energy`.

The layer result records the conditioned equivariant feature transformation.

The energy field contains the resulting:

`EnergyState`

These two structures are not interchangeable.

---

## 16. Reference Energy Inputs

The executable reference model consumes:

- `AtomicConfiguration`;
- `InteractionGraph`;
- `NodeFeatureVector`;
- `TernaryExecutionVector`.

The energy model requires all four inputs explicitly.

---

## 17. Input Cardinality

The executable model requires:

`graph.node_count = configuration.atom_count`

`features.node_count = configuration.atom_count`

`execution.node_count = configuration.atom_count`

A cardinality mismatch is invalid.

---

## 18. Interaction Graph Boundary

The interaction graph is an input to the model.

A graph edge is not itself:

- energy;
- force;
- chemical bond;
- resonance relation;
- ternary transition.

Therefore:

`graph edge ≠ energy contribution`

unless the selected functional explicitly defines such a decomposition.

---

## 19. Graph Construction Is Separate

Graph construction and energy evaluation are separate operations.

The energy model consumes the graph that is supplied.

The reference model does not silently reconstruct another graph inside:

`ReferenceEnergyModel.evaluate`

---

## 20. Equivariant Feature Boundary

Energy is produced from the current conditioned equivariant feature state.

The reference model executes:

`conditioned_equivariant_layer_step(...)`

before energy evaluation.

The scalar energy functional consumes:

`layer_result.current`

---

## 21. Scalar Energy Functional

The executable reference scalar functional is:

`LinearInvariantEnergyFunctional`

It contains:

- one tuple of scalar weights;
- one scalar bias.

Its required scalar-channel count is:

`len(weights)`

---

## 22. Scalar Channel Cardinality

The scalar feature width must equal the energy-functional weight count.

Therefore:

`features.scalar_channel_count = len(weights)`

at the functional evaluation boundary.

Mismatch is invalid.

---

## 23. Reference Atomic-Energy Formula

For node:

`i`

with invariant scalar channels:

`s_i,1, ..., s_i,K`

and energy weights:

`w_1, ..., w_K`

the reference atomic contribution is:

`E_i = Σ w_k s_i,k + b`

where:

`b`

is the configured scalar bias.

---

## 24. Reference Total-Energy Formula

The reference total energy is:

`E_total = Σ E_i`

over all represented nodes.

The executable constructor performs the aggregation in deterministic tuple order.

---

## 25. Vector Channels and Reference Functional

The current `LinearInvariantEnergyFunctional` directly consumes scalar channels.

It does not directly contract vector channels into energy.

Vector channels may influence later scalar state through explicitly implemented equivariant operations.

The energy functional itself remains scalar-output.

---

## 26. Energy Must Be Spatially Invariant

For a model declaring E(3) invariance, total scalar energy must remain unchanged under admissible rigid spatial transformations when all relevant geometric and equivariant inputs are transformed consistently.

Therefore:

`E(g · X) = E(X)`

for admissible:

`g ∈ E(3)`

under the declared model assumptions.

---

## 27. Energy Is a Scalar

Energy is not a spatial vector.

Therefore rigid rotation does not rotate the scalar energy value.

Likewise, reflection does not introduce a vector transformation law for energy.

---

## 28. Spatial Rotation Is Not Ternary Polarity Reversal

A spatial rotation belongs to E(3) geometry.

Ternary polarity belongs to balanced-ternary execution.

Therefore:

`spatial rotation ≠ ternary polarity reversal`

Energy invariance under rotation does not imply any ternary-state inversion.

---

## 29. Resonance Boundary

Resonance state is not energy.

A resonance descriptor is not energy.

A resonance-region classification is not energy.

Therefore:

`resonance state ≠ energy`

`resonance descriptor ≠ energy`

`resonance classification ≠ energy`

---

## 30. Resonance-Conditioned Energy

A specialized model may make energy depend on resonance information through explicit feature or parameter channels.

The current FLiBe TR-EIP realization appends continuous resonance descriptor components as explicit scalar feature channels before reference energy evaluation.

That architecture preserves:

`resonance conditioning ≠ energy itself`

---

## 31. Resonance Is Not Silently Inferred

The base `ReferenceEnergyModel` does not internally derive:

- oscillator phase;
- frequency;
- resonance descriptor;
- resonance region.

If resonance affects energy, the corresponding information must already be present in the supplied model inputs or specialized wrapper.

---

## 32. Ternary Conditioning Boundary

The reference energy model consumes:

`TernaryExecutionVector`

through:

`TernaryConditioning`

The conditioning input is retained executed ternary state.

---

## 33. Retained State Determines Ternary Conditioning

Energy conditioning uses the retained executed state.

A requested target is not automatically substituted for the retained state.

A pending target is not automatically substituted for the retained state.

Therefore:

`requested target ≠ energy conditioning state`

and:

`pending target ≠ energy conditioning state`

---

## 34. Pending Target Does Not Replace Executed State

If a node retains:

`0`

with a pending target:

`1`

the energy model still conditions on the executed retained state:

`0`

until the transition to `1` is actually committed.

Therefore:

`pending 1 ≠ executed 1`

---

## 35. Active Neutral Conditioning Is Explicit

The current reference conditioning assigns an explicit model parameter to active neutral state `0`.

The active-neutral scale is not required to equal zero.

Therefore:

`ternary neutral 0 ≠ numerical multiplication by zero`

---

## 36. Ternary Conditioning Is Model-Defined

The numerical conditioning associated with:

- `-1`;
- `0`;
- `1`

is supplied by the explicit `TernaryConditioning` model parameters.

The state labels alone do not prescribe one universal numerical multiplier.

---

## 37. No Hidden Ternary Execution

Energy evaluation does not execute ternary transitions.

It consumes a supplied execution vector.

Therefore:

`energy evaluation ≠ ternary commit`

and:

`energy evaluation ≠ neutral routing`

---

## 38. Geometry Dependence

The reference energy model may depend on atomic geometry through graph-relative equivariant message passing.

Coordinate dependence enters through the supplied configuration and graph-aware operations.

---

## 39. Energy and Physical Phase

Energy output does not directly encode a thermodynamic phase label.

Therefore:

`energy value ≠ physical phase of matter`

A phase transition requires the applicable thermodynamic or structural model.

---

## 40. Energy and Structural Transition

A change in energy does not automatically establish a structural transition.

Therefore:

`energy change ≠ structural transition`

Likewise:

`structural transition ≠ ternary transition`

---

## 41. Force Output Boundary

Force is a downstream mechanical observable derived from energy under the conservative reference path.

Force is represented separately by:

`ForceState`

Energy and force are distinct output types.

---

## 42. Conservative Force Definition

The canonical conservative force relation is:

`F_i = -dE/dr_i`

for each atomic Cartesian coordinate under the declared differentiation contract.

The negative sign is part of the force convention.

---

## 43. Force Is Not Energy

A force vector is not an energy value.

Therefore:

`force ≠ energy`

A vector-valued message is also not automatically mechanical force.

---

## 44. Force Is Not Ternary State

A force component numerically equal to:

`-1`

`0`

or:

`1`

remains a force component.

Therefore:

`force ≠ ternary state`

and:

`zero force ≠ active neutral 0`

---

## 45. Phase Coupling Is Not Mechanical Force

A phase-coupling term belongs to resonance dynamics.

It is not automatically an interatomic mechanical force.

Therefore:

`phase coupling ≠ mechanical force`

---

## 46. Reference Force Differentiation

The executable reference force evaluator is:

`ConservativeForceEvaluator`

It uses:

`CoordinateDifferentiation`

with a positive finite differentiation step.

The current default step is:

`1e-6`

as an implementation default.

---

## 47. Central Difference Force Evaluation

For one Cartesian coordinate component:

`x`

the reference evaluator approximates the energy derivative symmetrically from:

`E(x + h)`

and:

`E(x - h)`

with:

`h > 0`

The force applies the canonical negative energy-gradient sign.

---

## 48. One Coordinate at a Time

The reference force evaluator perturbs exactly one Cartesian component of one atom at a time.

Other coordinate components remain at their reference values for that derivative component.

---

## 49. Fixed-Graph Force Contract

Within one coordinate finite-difference derivative, the reference force evaluator holds the supplied interaction graph fixed.

Therefore:

`graph fixed within one force derivative`

This is part of the executable numerical contract.

---

## 50. Graph May Rebuild Between Physical States

Fixed graph topology within one derivative does not mean graph topology must remain fixed during an entire trajectory.

A molecular-dynamics layer may rebuild the graph between physical states according to its graph-construction contract.

Therefore:

`graph fixed within derivative`

and:

`graph may rebuild between physical states`

are compatible statements.

---

## 51. Fixed Feature Input during Force Differentiation

The supplied input feature vector is held fixed as an input object during the paired plus/minus coordinate energy evaluations.

Coordinate dependence then enters through the perturbed atomic configuration and the energy-model operations.

---

## 52. Fixed Ternary State during Force Differentiation

The supplied:

`TernaryExecutionVector`

is held fixed during paired plus/minus force evaluations.

No ternary transition is executed between those evaluations.

---

## 53. Force Evaluation Does Not Evolve Resonance Automatically

If resonance-conditioned channels are already contained in the supplied features, the reference force evaluator uses those supplied features.

It does not independently evolve resonance state between the plus and minus coordinate evaluations.

Any geometry-dependent resonance update requires an explicitly composed higher-level model.

---

## 54. Stress Output Boundary

Stress is another downstream mechanical observable derived from scalar energy.

It is represented by:

`StressState`

with a Cartesian:

`3 × 3`

tensor.

---

## 55. Stress Requires a Cell

The executable reference stress evaluator requires an atomic configuration with a cell.

A configuration without a cell is invalid for this stress path.

---

## 56. Reference Cell Volume

The reference stress evaluator computes:

`V = abs(det(cell))`

The reference cell volume must be nonzero.

---

## 57. Stress from Strain Derivative

The current reference stress convention derives each stress component from a homogeneous strain derivative of total energy.

The implemented sign convention is:

`stress = +(1/V) dE/dε`

under the current declared strain convention.

---

## 58. No Additional Stress Minus Sign

Unlike force, the current reference stress evaluator does not introduce an additional leading minus sign.

Therefore:

`force = -dE/dr`

while the current reference stress path uses:

`stress = +(1/V) dE/dε`

under its declared convention.

---

## 59. Stress Convention Must Remain Explicit

Other scientific communities may use different stress sign conventions.

TR-EIF must not silently switch conventions.

Any alternative convention requires explicit declaration and validation.

---

## 60. Reference Strain Differentiation

The executable stress evaluator uses:

`CellStrainDifferentiation`

with a positive finite strain step.

The current default is:

`1e-6`

as an implementation default.

---

## 61. Homogeneous Strain

The reference evaluator applies homogeneous Cartesian strain to:

- atomic positions;
- cell vectors.

The same transformation is applied consistently to both.

---

## 62. Diagonal Strain Components

For a diagonal strain component, the selected diagonal entry of the identity transformation is incremented by the requested strain value.

---

## 63. Off-Diagonal Strain Components

For an off-diagonal symmetric strain component, the reference implementation distributes half of the selected strain to each symmetric off-diagonal matrix position.

This is part of the current executable strain convention.

---

## 64. Symmetric Stress Output

The reference evaluator calculates only the upper-triangular component set directly and copies each off-diagonal result symmetrically.

Therefore the returned reference stress tensor is symmetric by construction.

---

## 65. Generic Stress State Boundary

The generic `StressState` representation can report whether a tensor is exactly symmetric.

The reference conservative stress evaluator produces a symmetric tensor.

Representation type and evaluator behavior remain distinct concepts.

---

## 66. Fixed-Graph Stress Contract

Within one strain finite-difference derivative, the same interaction graph is supplied to the plus-strain and minus-strain energy evaluations.

Therefore graph topology is fixed inside one reference stress derivative.

---

## 67. Fixed Feature Input during Stress Differentiation

The same supplied feature vector is used as the input object for the plus-strain and minus-strain evaluations.

No hidden feature update is performed by the stress evaluator.

---

## 68. Fixed Ternary State during Stress Differentiation

The same supplied:

`TernaryExecutionVector`

is used for plus-strain and minus-strain energy evaluations.

Stress differentiation does not execute a ternary transition.

---

## 69. Stress Is Not Ternary State

A stress tensor component numerically equal to:

`-1`

`0`

or:

`1`

remains a mechanical tensor component.

Therefore:

`stress ≠ ternary state`

and:

`zero stress ≠ active neutral 0`

---

## 70. Stress Is Not Resonance Classification

Stress is not:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`.

Therefore:

`stress ≠ resonance classification`

A resonance-window crossing does not automatically define a stress transition.

---

## 71. Unit Boundary

The generic TR-EIF energy package does not impose one universal physical unit system.

A physical specialization must declare applicable units for:

- energy;
- length;
- force;
- stress;
- cell volume;
- differentiation coordinate.

---

## 72. Force Units

Under a declared physical unit system:

`force unit = energy unit / length unit`

The numerical differentiation step must use the same length dimension as the perturbed coordinate.

---

## 73. Stress Units

Under the current strain convention:

`stress unit = energy unit / volume unit`

Homogeneous strain itself is dimensionless.

---

## 74. Reference Functional Has No Hidden Unit

`LinearInvariantEnergyFunctional`

does not automatically assign physical energy units to its scalar output.

Unit semantics must come from the concrete model and feature/parameter contract.

---

## 75. Provenance Boundary

Generic energy output does not automatically receive:

`PRIMARY_SOURCE`

provenance.

A concrete physical specialization must retain provenance for:

- learned parameters;
- calibrated parameters;
- empirical coefficients;
- source-backed energy references;
- benchmark fixtures.

---

## 76. Benchmark Energy Is Not Physical Evidence

An energy generated from:

`BENCHMARK`

or:

`TEST_FIXTURE`

parameters is benchmark evidence.

It must not be presented as an experimentally validated physical material energy solely because it is produced by the same executable interface.

---

## 77. Numerical Finiteness

`EnergyState` requires every atomic energy contribution to be finite.

It also requires total energy to be finite.

NaN and infinity are invalid.

---

## 78. Force Finiteness

`ForceState` requires:

- a nonempty force tuple;
- exactly three components per force;
- finite real components.

---

## 79. Stress Finiteness

`StressState` requires a finite Cartesian:

`3 × 3`

tensor.

Numerical failure remains separate from balanced-ternary semantics.

---

## 80. Deterministic Energy Evaluation

For identical admissible:

- configuration;
- interaction graph;
- input feature vector;
- retained ternary execution vector;
- message operator;
- conditioning parameters;
- energy-functional parameters;

the deterministic reference model must reproduce the same energy result under the same numerical execution contract.

---

## 81. Deterministic Atomic Ordering

Atomic energy contributions preserve node ordering.

Changing atom or node order without the corresponding consistent permutation of all model inputs is not the same model input.

---

## 82. Permutation Invariance of Total Energy

For an admissible atom relabeling applied consistently to:

- configuration;
- graph;
- features;
- execution state;

the physical total energy of a permutation-invariant model must remain unchanged.

Atomic contributions must permute consistently.

---

## 83. E(3) Validation

Energy invariance validation must include admissible:

- translation;
- rotation;
- reflection

when the concrete model claims E(3) invariance.

Force validation must additionally verify polar-vector equivariance.

---

## 84. Force-Gradient Consistency

A conservative force implementation must satisfy the declared relation to the same scalar energy model.

For the reference numerical implementation, validation uses the declared central-difference coordinate derivative and fixed-graph scope.

---

## 85. Stress-Energy Consistency

A reference stress output must agree with the declared homogeneous-strain derivative of the same scalar energy model under:

- the same graph;
- the same feature state;
- the same retained ternary execution state;
- the declared strain step;
- the declared sign convention.

---

## 86. Differentiation Convergence

Finite-difference validation may evaluate several positive differentiation steps.

Expected convergence properties belong to the numerical method.

A benchmark tolerance does not alter the underlying energy or force definition.

---

## 87. Nondifferentiable Boundary

A concrete energy model may contain states at which the selected numerical derivative is unstable or the energy mapping is nondifferentiable.

Such states require explicit numerical or domain handling.

They are not encoded as active neutral `0`.

---

## 88. Domain Status Is Not Ternary State

A model-domain status such as:

- valid;
- invalid;
- outside domain;
- uncertain;
- requires source;
- requires test

is not automatically a ternary state.

Therefore:

`validation status ≠ ternary state`

---

## 89. Uncertainty Is Not Ternary State

An uncertainty estimate attached to energy output remains uncertainty metadata.

Therefore:

`uncertainty ≠ ternary state`

High uncertainty is not active neutral `0`.

---

## 90. Energy Output Serialization

The canonical structural JSON fields are:

`atomic_energies`

and:

`total_energy`

The root structural schema is:

`schemas/energy_output.schema.json`

---

## 91. Serialized Atomic Energies

`atomic_energies`

is serialized as a nonempty ordered array of numeric values.

Order corresponds to the represented node/atom order.

---

## 92. Serialized Total Energy

`total_energy`

is serialized as one numeric scalar.

The structural JSON schema does not independently enforce the executable algebraic relation:

`total_energy = sum(atomic_energies)`

That relation remains an executable invariant.

---

## 93. Observable Bundle

Energy may appear inside a larger observable bundle together with:

- forces;
- stress.

The bundle schema is:

`schemas/observables.schema.json`

A missing optional energy observable is represented as:

`null`

not ternary `0`.

---

## 94. Transition Trace

Energy may also be associated with a time-ordered execution trace.

The trace schema is:

`schemas/transition_trace.schema.json`

The trace preserves energy separately from ternary execution state.

---

## 95. Trace Separation

A trace record containing:

`retained_state = 0`

does not imply:

`energy = 0`

Likewise:

`energy = 0`

does not imply:

`retained_state = 0`

These values occupy different semantic spaces.

---

## 96. Energy and Molecular Dynamics

In molecular dynamics, the energy model supplies potential energy.

Velocity-derived kinetic energy belongs to the molecular-dynamics state/observable layer.

Therefore:

`potential energy ≠ kinetic energy`

and:

`total MD energy = kinetic + potential`

under the declared MD observable convention.

---

## 97. No Hidden Resonance Evolution in MD Energy Evaluation

A single energy evaluation does not advance oscillator phases or frequencies.

Any resonance propagation in molecular dynamics requires an explicitly composed propagation step.

---

## 98. No Hidden Ternary Evolution in MD Energy Evaluation

A single potential-energy evaluation does not commit ternary transitions.

Ternary propagation, if used, remains a separate explicit execution step.

---

## 99. Graph Scope in Molecular Dynamics

A molecular-dynamics implementation may rebuild the interaction graph between physical states.

Each local force evaluation may still use fixed graph topology within its own finite-difference derivative.

These two scopes must not be conflated.

---

## 100. Energy Conservation Boundary

An energy-conservation benchmark evaluates the behavior of a complete numerical trajectory.

It does not redefine the instantaneous energy output specification.

Observed numerical drift depends on:

- integrator;
- time step;
- derivative approximation;
- model smoothness;
- graph-update semantics;
- execution composition.

---

## 101. Learning Boundary

A model may be trained against:

- energy references;
- force references;
- stress references.

Training-stage optimization state is not balanced-ternary execution state.

Therefore:

`training-stage transition ≠ ternary-state transition`

---

## 102. Energy Reference Boundary

An external energy reference may be supplied by:

`ElectronicReferenceRecord`

or another explicitly typed source.

Reference evidence and model prediction remain distinct artifacts.

---

## 103. Model Prediction Is Not Reference Evidence

An energy predicted by TR-EIP is not automatically:

- experimental evidence;
- first-principles evidence;
- primary-source evidence.

Its evidentiary class depends on its provenance and validation path.

---

## 104. FLiBe TR-EIP Boundary

The FLiBe-specific TR-EIP realization uses the generic conservative energy path while adding explicit FLiBe and resonance context.

The architectural relation remains:

`FLiBe TR-EIP realization ⊂ TR-EIP model family ⊂ TR-EIF framework`

---

## 105. FRP Boundary

FRP may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

The energy-output specification does not import:

- FRP RTL architecture;
- FRP scheduler modes;
- FRP-specific coefficients;
- FRP module naming.

Therefore:

`FRP ≠ TR-EIP`

and:

`FRP ≠ TR-EIF`

---

## 106. Core Energy Output Invariants

The energy-output layer preserves the following invariants:

1. Energy output is continuous scalar physical/model state.
2. `EnergyState` is nonempty and finite.
3. Atomic contributions retain deterministic node order.
4. `EnergyState.from_atomic_energies` defines total energy by ordered summation.
5. Energy is not ternary state.
6. Active neutral `0` is not zero energy.
7. Zero energy is not active neutral `0`.
8. Missing or invalid energy is not ternary `0`.
9. Resonance descriptor is not energy.
10. Resonance conditioning is explicit.
11. Ternary conditioning uses retained executed state.
12. Requested target does not replace retained state.
13. Pending target does not replace retained state.
14. Energy evaluation does not execute ternary transitions.
15. Energy evaluation does not evolve resonance state.
16. Energy is scalar under E(3).
17. Force uses the negative energy gradient.
18. Current reference stress uses the positive strain derivative divided by reference volume.
19. Force differentiation holds graph topology fixed locally.
20. Stress differentiation holds graph topology fixed locally.
21. Graph topology may be rebuilt between physical states.
22. Feature and retained ternary inputs are held fixed during paired numerical derivatives.
23. Force, stress, and energy remain separate output types.
24. Physical units must be explicitly declared by concrete models.
25. Provenance is not inferred from numeric values.
26. Validation status and uncertainty are not ternary states.
27. Serialized missing observables use `null`, not active neutral `0`.
28. Deterministic complete inputs produce deterministic reference energy output.

---

## 107. Executable Reference Correspondence

The principal executable energy interfaces are:

`src/tr_eif/energy/state.py`

`src/tr_eif/energy/functional.py`

`src/tr_eif/energy/model.py`

`src/tr_eif/energy/differentiation.py`

`src/tr_eif/energy/force.py`

`src/tr_eif/energy/force_evaluator.py`

`src/tr_eif/energy/strain.py`

`src/tr_eif/energy/stress.py`

`src/tr_eif/energy/stress_evaluator.py`

The principal public types are:

`EnergyState`

`LinearInvariantEnergyFunctional`

`EnergyModelResult`

`ReferenceEnergyModel`

`CoordinateDifferentiation`

`ForceState`

`ConservativeForceEvaluator`

`CellStrainDifferentiation`

`StressState`

`ConservativeStressEvaluator`

---

## 108. Non-Claims

The generic energy-output layer does not by itself establish:

- experimental energy accuracy;
- first-principles accuracy;
- chemical reaction pathway;
- material phase transition;
- chemical bond formation;
- resonance classification;
- ternary target;
- ternary transition;
- thermodynamic completeness;
- material transmutation.

Those claims require their own model, provenance, and validation layers.

---

## 109. Summary

TR-EIF energy output is a conservative scalar-model interface with explicitly separated downstream mechanical observables.

The reference execution chain is:

`configuration + graph + features + retained ternary state`

`→ conditioned equivariant layer`

`→ invariant scalar atomic contributions`

`→ total energy`

and, when requested:

`total energy`

`→ coordinate derivative`

`→ force`

or:

`total energy`

`→ homogeneous strain derivative`

`→ stress`

Resonance, balanced ternary execution, energy, force, stress, validation status, uncertainty, and missing data remain separate typed domains.

Numerical equality between values from those domains does not establish semantic identity.# Energy Output Specification

## 1. Scope

This document defines the repository-level energy output specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- scalar energy output;
- atomic energy contributions;
- total energy;
- conservative energy semantics;
- energy-model output structure;
- invariant scalar functional input;
- resonance-conditioning boundary;
- balanced-ternary conditioning boundary;
- retained-state semantics;
- geometry and graph dependencies;
- E(3) invariance requirements;
- deterministic aggregation;
- force derivation;
- stress derivation;
- fixed-graph numerical differentiation;
- output serialization;
- unit boundary;
- provenance boundary;
- numerical validity;
- validation requirements;
- executable reference correspondence.

The architecture contract is defined in:

`docs/architecture/energy_model_contract.md`

The formal energy model is developed in:

`docs/volume_03_equivariant_interatomic_framework/chapter_08_conservative_energy_functional.md`

Force and stress semantics are developed in:

`docs/volume_03_equivariant_interatomic_framework/chapter_09_forces_and_stress.md`

The structural JSON representation is defined by:

`schemas/energy_output.schema.json`

---

## 2. Energy Output Domain

Energy output belongs to a continuous scalar physical domain.

A total energy is represented as:

`E_total ∈ R`

subject to finite numerical representation.

Energy is not a balanced-ternary state.

Therefore:

`energy ≠ ternary state`

---

## 3. Reference Energy Output

The executable reference energy representation is:

`EnergyState`

with fields:

- `atomic_energies`;
- `total_energy`.

The representation is immutable after construction.

---

## 4. Atomic Energy Contributions

For a configuration containing:

`N`

represented atoms, the reference atomic-energy vector is:

`E_atomic = (E_1, E_2, ..., E_N)`

Each:

`E_i`

is a finite real scalar.

The executable type alias is:

`AtomicEnergies`

---

## 5. Atomic Contribution Cardinality

The atomic-energy vector must be nonempty.

For an `EnergyModelResult`, its cardinality must equal the node count of the conditioned equivariant layer result.

Therefore:

`energy.atom_count = layer_result.current.node_count`

---

## 6. Total Energy

The total energy is one finite scalar:

`E_total`

The canonical constructor:

`EnergyState.from_atomic_energies(...)`

defines:

`E_total = Σ E_i`

using the deterministic tuple order supplied to the constructor.

---

## 7. Atomic Energy Is a Model Decomposition

An atomic energy contribution is part of the selected energy decomposition.

It is not automatically an independently measurable physical observable.

Therefore:

`atomic contribution ≠ independently measured atomic energy`

unless a concrete physical model establishes that interpretation.

---

## 8. Energy Is Not Ternary State

The balanced ternary labels:

`-1`

`0`

`1`

are execution states.

They are not energy values.

Therefore:

`-1 ≠ negative energy by definition`

`0 ≠ zero energy by definition`

`1 ≠ positive energy by definition`

---

## 9. Active Neutral Is Not Zero Energy

Active neutral state:

`0`

may support:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Those semantics do not mean:

`E = 0`

Therefore:

`active neutral 0 ≠ zero energy`

---

## 10. Zero Energy Is Not Active Neutral

A physical or model energy may numerically equal:

`0`

This does not create balanced-ternary active-neutral semantics.

Therefore:

`energy zero ≠ ternary neutral 0`

---

## 11. Energy Sign Is Not Ternary Polarity

The sign of energy does not define ternary polarity.

Therefore:

`negative energy ≠ ternary -1`

and:

`positive energy ≠ ternary 1`

A concrete target-generation mapping may use energy-derived information only when that mapping is explicitly defined.

---

## 12. Missing Energy Is Not Active Neutral

Missing or unavailable energy output must not be encoded as:

`0`

Missing energy is represented separately.

In serialized observable records, absence may be represented as:

`null`

Therefore:

`missing energy ≠ active neutral`

---

## 13. Invalid Energy Is Not Active Neutral

An invalid, NaN, infinite, failed, or unavailable energy calculation remains outside the balanced-ternary state space.

Therefore:

`invalid energy ≠ ternary 0`

`NaN ≠ ternary 0`

`numerical failure ≠ ternary 0`

---

## 14. Reference Energy Model

The executable reference interatomic energy model is:

`ReferenceEnergyModel`

Its stored components are:

- `RadialMessageOperator`;
- `TernaryConditioning`;
- `LinearInvariantEnergyFunctional`.

Its output type is:

`EnergyModelResult`

---

## 15. Energy Model Result

`EnergyModelResult` contains:

- `layer_result`;
- `energy`.

The layer result records the conditioned equivariant feature transformation.

The energy field contains the resulting:

`EnergyState`

These two structures are not interchangeable.

---

## 16. Reference Energy Inputs

The executable reference model consumes:

- `AtomicConfiguration`;
- `InteractionGraph`;
- `NodeFeatureVector`;
- `TernaryExecutionVector`.

The energy model requires all four inputs explicitly.

---

## 17. Input Cardinality

The executable model requires:

`graph.node_count = configuration.atom_count`

`features.node_count = configuration.atom_count`

`execution.node_count = configuration.atom_count`

A cardinality mismatch is invalid.

---

## 18. Interaction Graph Boundary

The interaction graph is an input to the model.

A graph edge is not itself:

- energy;
- force;
- chemical bond;
- resonance relation;
- ternary transition.

Therefore:

`graph edge ≠ energy contribution`

unless the selected functional explicitly defines such a decomposition.

---

## 19. Graph Construction Is Separate

Graph construction and energy evaluation are separate operations.

The energy model consumes the graph that is supplied.

The reference model does not silently reconstruct another graph inside:

`ReferenceEnergyModel.evaluate`

---

## 20. Equivariant Feature Boundary

Energy is produced from the current conditioned equivariant feature state.

The reference model executes:

`conditioned_equivariant_layer_step(...)`

before energy evaluation.

The scalar energy functional consumes:

`layer_result.current`

---

## 21. Scalar Energy Functional

The executable reference scalar functional is:

`LinearInvariantEnergyFunctional`

It contains:

- one tuple of scalar weights;
- one scalar bias.

Its required scalar-channel count is:

`len(weights)`

---

## 22. Scalar Channel Cardinality

The scalar feature width must equal the energy-functional weight count.

Therefore:

`features.scalar_channel_count = len(weights)`

at the functional evaluation boundary.

Mismatch is invalid.

---

## 23. Reference Atomic-Energy Formula

For node:

`i`

with invariant scalar channels:

`s_i,1, ..., s_i,K`

and energy weights:

`w_1, ..., w_K`

the reference atomic contribution is:

`E_i = Σ w_k s_i,k + b`

where:

`b`

is the configured scalar bias.

---

## 24. Reference Total-Energy Formula

The reference total energy is:

`E_total = Σ E_i`

over all represented nodes.

The executable constructor performs the aggregation in deterministic tuple order.

---

## 25. Vector Channels and Reference Functional

The current `LinearInvariantEnergyFunctional` directly consumes scalar channels.

It does not directly contract vector channels into energy.

Vector channels may influence later scalar state through explicitly implemented equivariant operations.

The energy functional itself remains scalar-output.

---

## 26. Energy Must Be Spatially Invariant

For a model declaring E(3) invariance, total scalar energy must remain unchanged under admissible rigid spatial transformations when all relevant geometric and equivariant inputs are transformed consistently.

Therefore:

`E(g · X) = E(X)`

for admissible:

`g ∈ E(3)`

under the declared model assumptions.

---

## 27. Energy Is a Scalar

Energy is not a spatial vector.

Therefore rigid rotation does not rotate the scalar energy value.

Likewise, reflection does not introduce a vector transformation law for energy.

---

## 28. Spatial Rotation Is Not Ternary Polarity Reversal

A spatial rotation belongs to E(3) geometry.

Ternary polarity belongs to balanced-ternary execution.

Therefore:

`spatial rotation ≠ ternary polarity reversal`

Energy invariance under rotation does not imply any ternary-state inversion.

---

## 29. Resonance Boundary

Resonance state is not energy.

A resonance descriptor is not energy.

A resonance-region classification is not energy.

Therefore:

`resonance state ≠ energy`

`resonance descriptor ≠ energy`

`resonance classification ≠ energy`

---

## 30. Resonance-Conditioned Energy

A specialized model may make energy depend on resonance information through explicit feature or parameter channels.

The current FLiBe TR-EIP realization appends continuous resonance descriptor components as explicit scalar feature channels before reference energy evaluation.

That architecture preserves:

`resonance conditioning ≠ energy itself`

---

## 31. Resonance Is Not Silently Inferred

The base `ReferenceEnergyModel` does not internally derive:

- oscillator phase;
- frequency;
- resonance descriptor;
- resonance region.

If resonance affects energy, the corresponding information must already be present in the supplied model inputs or specialized wrapper.

---

## 32. Ternary Conditioning Boundary

The reference energy model consumes:

`TernaryExecutionVector`

through:

`TernaryConditioning`

The conditioning input is retained executed ternary state.

---

## 33. Retained State Determines Ternary Conditioning

Energy conditioning uses the retained executed state.

A requested target is not automatically substituted for the retained state.

A pending target is not automatically substituted for the retained state.

Therefore:

`requested target ≠ energy conditioning state`

and:

`pending target ≠ energy conditioning state`

---

## 34. Pending Target Does Not Replace Executed State

If a node retains:

`0`

with a pending target:

`1`

the energy model still conditions on the executed retained state:

`0`

until the transition to `1` is actually committed.

Therefore:

`pending 1 ≠ executed 1`

---

## 35. Active Neutral Conditioning Is Explicit

The current reference conditioning assigns an explicit model parameter to active neutral state `0`.

The active-neutral scale is not required to equal zero.

Therefore:

`ternary neutral 0 ≠ numerical multiplication by zero`

---

## 36. Ternary Conditioning Is Model-Defined

The numerical conditioning associated with:

- `-1`;
- `0`;
- `1`

is supplied by the explicit `TernaryConditioning` model parameters.

The state labels alone do not prescribe one universal numerical multiplier.

---

## 37. No Hidden Ternary Execution

Energy evaluation does not execute ternary transitions.

It consumes a supplied execution vector.

Therefore:

`energy evaluation ≠ ternary commit`

and:

`energy evaluation ≠ neutral routing`

---

## 38. Geometry Dependence

The reference energy model may depend on atomic geometry through graph-relative equivariant message passing.

Coordinate dependence enters through the supplied configuration and graph-aware operations.

---

## 39. Energy and Physical Phase

Energy output does not directly encode a thermodynamic phase label.

Therefore:

`energy value ≠ physical phase of matter`

A phase transition requires the applicable thermodynamic or structural model.

---

## 40. Energy and Structural Transition

A change in energy does not automatically establish a structural transition.

Therefore:

`energy change ≠ structural transition`

Likewise:

`structural transition ≠ ternary transition`

---

## 41. Force Output Boundary

Force is a downstream mechanical observable derived from energy under the conservative reference path.

Force is represented separately by:

`ForceState`

Energy and force are distinct output types.

---

## 42. Conservative Force Definition

The canonical conservative force relation is:

`F_i = -dE/dr_i`

for each atomic Cartesian coordinate under the declared differentiation contract.

The negative sign is part of the force convention.

---

## 43. Force Is Not Energy

A force vector is not an energy value.

Therefore:

`force ≠ energy`

A vector-valued message is also not automatically mechanical force.

---

## 44. Force Is Not Ternary State

A force component numerically equal to:

`-1`

`0`

or:

`1`

remains a force component.

Therefore:

`force ≠ ternary state`

and:

`zero force ≠ active neutral 0`

---

## 45. Phase Coupling Is Not Mechanical Force

A phase-coupling term belongs to resonance dynamics.

It is not automatically an interatomic mechanical force.

Therefore:

`phase coupling ≠ mechanical force`

---

## 46. Reference Force Differentiation

The executable reference force evaluator is:

`ConservativeForceEvaluator`

It uses:

`CoordinateDifferentiation`

with a positive finite differentiation step.

The current default step is:

`1e-6`

as an implementation default.

---

## 47. Central Difference Force Evaluation

For one Cartesian coordinate component:

`x`

the reference evaluator approximates the energy derivative symmetrically from:

`E(x + h)`

and:

`E(x - h)`

with:

`h > 0`

The force applies the canonical negative energy-gradient sign.

---

## 48. One Coordinate at a Time

The reference force evaluator perturbs exactly one Cartesian component of one atom at a time.

Other coordinate components remain at their reference values for that derivative component.

---

## 49. Fixed-Graph Force Contract

Within one coordinate finite-difference derivative, the reference force evaluator holds the supplied interaction graph fixed.

Therefore:

`graph fixed within one force derivative`

This is part of the executable numerical contract.

---

## 50. Graph May Rebuild Between Physical States

Fixed graph topology within one derivative does not mean graph topology must remain fixed during an entire trajectory.

A molecular-dynamics layer may rebuild the graph between physical states according to its graph-construction contract.

Therefore:

`graph fixed within derivative`

and:

`graph may rebuild between physical states`

are compatible statements.

---

## 51. Fixed Feature Input during Force Differentiation

The supplied input feature vector is held fixed as an input object during the paired plus/minus coordinate energy evaluations.

Coordinate dependence then enters through the perturbed atomic configuration and the energy-model operations.

---

## 52. Fixed Ternary State during Force Differentiation

The supplied:

`TernaryExecutionVector`

is held fixed during paired plus/minus force evaluations.

No ternary transition is executed between those evaluations.

---

## 53. Force Evaluation Does Not Evolve Resonance Automatically

If resonance-conditioned channels are already contained in the supplied features, the reference force evaluator uses those supplied features.

It does not independently evolve resonance state between the plus and minus coordinate evaluations.

Any geometry-dependent resonance update requires an explicitly composed higher-level model.

---

## 54. Stress Output Boundary

Stress is another downstream mechanical observable derived from scalar energy.

It is represented by:

`StressState`

with a Cartesian:

`3 × 3`

tensor.

---

## 55. Stress Requires a Cell

The executable reference stress evaluator requires an atomic configuration with a cell.

A configuration without a cell is invalid for this stress path.

---

## 56. Reference Cell Volume

The reference stress evaluator computes:

`V = abs(det(cell))`

The reference cell volume must be nonzero.

---

## 57. Stress from Strain Derivative

The current reference stress convention derives each stress component from a homogeneous strain derivative of total energy.

The implemented sign convention is:

`stress = +(1/V) dE/dε`

under the current declared strain convention.

---

## 58. No Additional Stress Minus Sign

Unlike force, the current reference stress evaluator does not introduce an additional leading minus sign.

Therefore:

`force = -dE/dr`

while the current reference stress path uses:

`stress = +(1/V) dE/dε`

under its declared convention.

---

## 59. Stress Convention Must Remain Explicit

Other scientific communities may use different stress sign conventions.

TR-EIF must not silently switch conventions.

Any alternative convention requires explicit declaration and validation.

---

## 60. Reference Strain Differentiation

The executable stress evaluator uses:

`CellStrainDifferentiation`

with a positive finite strain step.

The current default is:

`1e-6`

as an implementation default.

---

## 61. Homogeneous Strain

The reference evaluator applies homogeneous Cartesian strain to:

- atomic positions;
- cell vectors.

The same transformation is applied consistently to both.

---

## 62. Diagonal Strain Components

For a diagonal strain component, the selected diagonal entry of the identity transformation is incremented by the requested strain value.

---

## 63. Off-Diagonal Strain Components

For an off-diagonal symmetric strain component, the reference implementation distributes half of the selected strain to each symmetric off-diagonal matrix position.

This is part of the current executable strain convention.

---

## 64. Symmetric Stress Output

The reference evaluator calculates only the upper-triangular component set directly and copies each off-diagonal result symmetrically.

Therefore the returned reference stress tensor is symmetric by construction.

---

## 65. Generic Stress State Boundary

The generic `StressState` representation can report whether a tensor is exactly symmetric.

The reference conservative stress evaluator produces a symmetric tensor.

Representation type and evaluator behavior remain distinct concepts.

---

## 66. Fixed-Graph Stress Contract

Within one strain finite-difference derivative, the same interaction graph is supplied to the plus-strain and minus-strain energy evaluations.

Therefore graph topology is fixed inside one reference stress derivative.

---

## 67. Fixed Feature Input during Stress Differentiation

The same supplied feature vector is used as the input object for the plus-strain and minus-strain evaluations.

No hidden feature update is performed by the stress evaluator.

---

## 68. Fixed Ternary State during Stress Differentiation

The same supplied:

`TernaryExecutionVector`

is used for plus-strain and minus-strain energy evaluations.

Stress differentiation does not execute a ternary transition.

---

## 69. Stress Is Not Ternary State

A stress tensor component numerically equal to:

`-1`

`0`

or:

`1`

remains a mechanical tensor component.

Therefore:

`stress ≠ ternary state`

and:

`zero stress ≠ active neutral 0`

---

## 70. Stress Is Not Resonance Classification

Stress is not:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`.

Therefore:

`stress ≠ resonance classification`

A resonance-window crossing does not automatically define a stress transition.

---

## 71. Unit Boundary

The generic TR-EIF energy package does not impose one universal physical unit system.

A physical specialization must declare applicable units for:

- energy;
- length;
- force;
- stress;
- cell volume;
- differentiation coordinate.

---

## 72. Force Units

Under a declared physical unit system:

`force unit = energy unit / length unit`

The numerical differentiation step must use the same length dimension as the perturbed coordinate.

---

## 73. Stress Units

Under the current strain convention:

`stress unit = energy unit / volume unit`

Homogeneous strain itself is dimensionless.

---

## 74. Reference Functional Has No Hidden Unit

`LinearInvariantEnergyFunctional`

does not automatically assign physical energy units to its scalar output.

Unit semantics must come from the concrete model and feature/parameter contract.

---

## 75. Provenance Boundary

Generic energy output does not automatically receive:

`PRIMARY_SOURCE`

provenance.

A concrete physical specialization must retain provenance for:

- learned parameters;
- calibrated parameters;
- empirical coefficients;
- source-backed energy references;
- benchmark fixtures.

---

## 76. Benchmark Energy Is Not Physical Evidence

An energy generated from:

`BENCHMARK`

or:

`TEST_FIXTURE`

parameters is benchmark evidence.

It must not be presented as an experimentally validated physical material energy solely because it is produced by the same executable interface.

---

## 77. Numerical Finiteness

`EnergyState` requires every atomic energy contribution to be finite.

It also requires total energy to be finite.

NaN and infinity are invalid.

---

## 78. Force Finiteness

`ForceState` requires:

- a nonempty force tuple;
- exactly three components per force;
- finite real components.

---

## 79. Stress Finiteness

`StressState` requires a finite Cartesian:

`3 × 3`

tensor.

Numerical failure remains separate from balanced-ternary semantics.

---

## 80. Deterministic Energy Evaluation

For identical admissible:

- configuration;
- interaction graph;
- input feature vector;
- retained ternary execution vector;
- message operator;
- conditioning parameters;
- energy-functional parameters;

the deterministic reference model must reproduce the same energy result under the same numerical execution contract.

---

## 81. Deterministic Atomic Ordering

Atomic energy contributions preserve node ordering.

Changing atom or node order without the corresponding consistent permutation of all model inputs is not the same model input.

---

## 82. Permutation Invariance of Total Energy

For an admissible atom relabeling applied consistently to:

- configuration;
- graph;
- features;
- execution state;

the physical total energy of a permutation-invariant model must remain unchanged.

Atomic contributions must permute consistently.

---

## 83. E(3) Validation

Energy invariance validation must include admissible:

- translation;
- rotation;
- reflection

when the concrete model claims E(3) invariance.

Force validation must additionally verify polar-vector equivariance.

---

## 84. Force-Gradient Consistency

A conservative force implementation must satisfy the declared relation to the same scalar energy model.

For the reference numerical implementation, validation uses the declared central-difference coordinate derivative and fixed-graph scope.

---

## 85. Stress-Energy Consistency

A reference stress output must agree with the declared homogeneous-strain derivative of the same scalar energy model under:

- the same graph;
- the same feature state;
- the same retained ternary execution state;
- the declared strain step;
- the declared sign convention.

---

## 86. Differentiation Convergence

Finite-difference validation may evaluate several positive differentiation steps.

Expected convergence properties belong to the numerical method.

A benchmark tolerance does not alter the underlying energy or force definition.

---

## 87. Nondifferentiable Boundary

A concrete energy model may contain states at which the selected numerical derivative is unstable or the energy mapping is nondifferentiable.

Such states require explicit numerical or domain handling.

They are not encoded as active neutral `0`.

---

## 88. Domain Status Is Not Ternary State

A model-domain status such as:

- valid;
- invalid;
- outside domain;
- uncertain;
- requires source;
- requires test

is not automatically a ternary state.

Therefore:

`validation status ≠ ternary state`

---

## 89. Uncertainty Is Not Ternary State

An uncertainty estimate attached to energy output remains uncertainty metadata.

Therefore:

`uncertainty ≠ ternary state`

High uncertainty is not active neutral `0`.

---

## 90. Energy Output Serialization

The canonical structural JSON fields are:

`atomic_energies`

and:

`total_energy`

The root structural schema is:

`schemas/energy_output.schema.json`

---

## 91. Serialized Atomic Energies

`atomic_energies`

is serialized as a nonempty ordered array of numeric values.

Order corresponds to the represented node/atom order.

---

## 92. Serialized Total Energy

`total_energy`

is serialized as one numeric scalar.

The structural JSON schema does not independently enforce the executable algebraic relation:

`total_energy = sum(atomic_energies)`

That relation remains an executable invariant.

---

## 93. Observable Bundle

Energy may appear inside a larger observable bundle together with:

- forces;
- stress.

The bundle schema is:

`schemas/observables.schema.json`

A missing optional energy observable is represented as:

`null`

not ternary `0`.

---

## 94. Transition Trace

Energy may also be associated with a time-ordered execution trace.

The trace schema is:

`schemas/transition_trace.schema.json`

The trace preserves energy separately from ternary execution state.

---

## 95. Trace Separation

A trace record containing:

`retained_state = 0`

does not imply:

`energy = 0`

Likewise:

`energy = 0`

does not imply:

`retained_state = 0`

These values occupy different semantic spaces.

---

## 96. Energy and Molecular Dynamics

In molecular dynamics, the energy model supplies potential energy.

Velocity-derived kinetic energy belongs to the molecular-dynamics state/observable layer.

Therefore:

`potential energy ≠ kinetic energy`

and:

`total MD energy = kinetic + potential`

under the declared MD observable convention.

---

## 97. No Hidden Resonance Evolution in MD Energy Evaluation

A single energy evaluation does not advance oscillator phases or frequencies.

Any resonance propagation in molecular dynamics requires an explicitly composed propagation step.

---

## 98. No Hidden Ternary Evolution in MD Energy Evaluation

A single potential-energy evaluation does not commit ternary transitions.

Ternary propagation, if used, remains a separate explicit execution step.

---

## 99. Graph Scope in Molecular Dynamics

A molecular-dynamics implementation may rebuild the interaction graph between physical states.

Each local force evaluation may still use fixed graph topology within its own finite-difference derivative.

These two scopes must not be conflated.

---

## 100. Energy Conservation Boundary

An energy-conservation benchmark evaluates the behavior of a complete numerical trajectory.

It does not redefine the instantaneous energy output specification.

Observed numerical drift depends on:

- integrator;
- time step;
- derivative approximation;
- model smoothness;
- graph-update semantics;
- execution composition.

---

## 101. Learning Boundary

A model may be trained against:

- energy references;
- force references;
- stress references.

Training-stage optimization state is not balanced-ternary execution state.

Therefore:

`training-stage transition ≠ ternary-state transition`

---

## 102. Energy Reference Boundary

An external energy reference may be supplied by:

`ElectronicReferenceRecord`

or another explicitly typed source.

Reference evidence and model prediction remain distinct artifacts.

---

## 103. Model Prediction Is Not Reference Evidence

An energy predicted by TR-EIP is not automatically:

- experimental evidence;
- first-principles evidence;
- primary-source evidence.

Its evidentiary class depends on its provenance and validation path.

---

## 104. FLiBe TR-EIP Boundary

The FLiBe-specific TR-EIP realization uses the generic conservative energy path while adding explicit FLiBe and resonance context.

The architectural relation remains:

`FLiBe TR-EIP realization ⊂ TR-EIP model family ⊂ TR-EIF framework`

---

## 105. FRP Boundary

FRP may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

The energy-output specification does not import:

- FRP RTL architecture;
- FRP scheduler modes;
- FRP-specific coefficients;
- FRP module naming.

Therefore:

`FRP ≠ TR-EIP`

and:

`FRP ≠ TR-EIF`

---

## 106. Core Energy Output Invariants

The energy-output layer preserves the following invariants:

1. Energy output is continuous scalar physical/model state.
2. `EnergyState` is nonempty and finite.
3. Atomic contributions retain deterministic node order.
4. `EnergyState.from_atomic_energies` defines total energy by ordered summation.
5. Energy is not ternary state.
6. Active neutral `0` is not zero energy.
7. Zero energy is not active neutral `0`.
8. Missing or invalid energy is not ternary `0`.
9. Resonance descriptor is not energy.
10. Resonance conditioning is explicit.
11. Ternary conditioning uses retained executed state.
12. Requested target does not replace retained state.
13. Pending target does not replace retained state.
14. Energy evaluation does not execute ternary transitions.
15. Energy evaluation does not evolve resonance state.
16. Energy is scalar under E(3).
17. Force uses the negative energy gradient.
18. Current reference stress uses the positive strain derivative divided by reference volume.
19. Force differentiation holds graph topology fixed locally.
20. Stress differentiation holds graph topology fixed locally.
21. Graph topology may be rebuilt between physical states.
22. Feature and retained ternary inputs are held fixed during paired numerical derivatives.
23. Force, stress, and energy remain separate output types.
24. Physical units must be explicitly declared by concrete models.
25. Provenance is not inferred from numeric values.
26. Validation status and uncertainty are not ternary states.
27. Serialized missing observables use `null`, not active neutral `0`.
28. Deterministic complete inputs produce deterministic reference energy output.

---

## 107. Executable Reference Correspondence

The principal executable energy interfaces are:

`src/tr_eif/energy/state.py`

`src/tr_eif/energy/functional.py`

`src/tr_eif/energy/model.py`

`src/tr_eif/energy/differentiation.py`

`src/tr_eif/energy/force.py`

`src/tr_eif/energy/force_evaluator.py`

`src/tr_eif/energy/strain.py`

`src/tr_eif/energy/stress.py`

`src/tr_eif/energy/stress_evaluator.py`

The principal public types are:

`EnergyState`

`LinearInvariantEnergyFunctional`

`EnergyModelResult`

`ReferenceEnergyModel`

`CoordinateDifferentiation`

`ForceState`

`ConservativeForceEvaluator`

`CellStrainDifferentiation`

`StressState`

`ConservativeStressEvaluator`

---

## 108. Non-Claims

The generic energy-output layer does not by itself establish:

- experimental energy accuracy;
- first-principles accuracy;
- chemical reaction pathway;
- material phase transition;
- chemical bond formation;
- resonance classification;
- ternary target;
- ternary transition;
- thermodynamic completeness;
- material transmutation.

Those claims require their own model, provenance, and validation layers.

---

## 109. Summary

TR-EIF energy output is a conservative scalar-model interface with explicitly separated downstream mechanical observables.

The reference execution chain is:

`configuration + graph + features + retained ternary state`

`→ conditioned equivariant layer`

`→ invariant scalar atomic contributions`

`→ total energy`

and, when requested:

`total energy`

`→ coordinate derivative`

`→ force`

or:

`total energy`

`→ homogeneous strain derivative`

`→ stress`

Resonance, balanced ternary execution, energy, force, stress, validation status, uncertainty, and missing data remain separate typed domains.

Numerical equality between values from those domains does not establish semantic identity.
