# Conservative Energy Model Contract

## 1. Scope

This document defines the repository-level conservative energy model contract of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The contract specifies:

- the energy-model domain;
- atomic and total energy representations;
- invariant scalar-energy construction;
- equivariant-model integration;
- resonance-conditioning boundaries;
- ternary-conditioning boundaries;
- retained-state requirements;
- graph and geometry dependencies;
- coordinate dependence;
- force derivation;
- stress derivation;
- coordinate-differentiation semantics;
- strain-differentiation semantics;
- graph-topology treatment during numerical differentiation;
- symmetry requirements;
- dimensional and provenance requirements;
- molecular-dynamics interfaces;
- observable boundaries;
- deterministic evaluation requirements;
- validation requirements;
- executable reference correspondence.

This document defines an architectural contract.

Detailed mathematical derivations remain in the numbered mathematical volumes.

---

## 2. Energy-State Domain

An energy model produces a scalar energy state.

A generic energy-state space may be denoted:

`X_E`

A scalar total energy is:

`E_total ∈ R`

when represented numerically by a finite real value.

Where atomic contributions are defined:

`E_atomic = (E_1, ..., E_N)`

with:

`E_i ∈ R`

for:

`i ∈ {1, ..., N}`

The total energy is obtained from the declared aggregation rule.

---

## 3. Reference Energy-State Representation

The executable reference representation is:

`EnergyState`

with:

- `atomic_energies`;
- `total_energy`.

The atomic-energy collection contains one finite scalar contribution per represented atom.

The total-energy field contains one finite scalar value.

The reference constructor:

`EnergyState.from_atomic_energies(...)`

defines:

`E_total = sum_i E_i`

using the deterministic execution order of the supplied tuple.

---

## 4. Atomic Contribution Boundary

An atomic energy contribution is a component of the selected energy decomposition.

The existence of:

`E_i`

does not require that atomic energy be an independently measurable physical observable.

The decomposition is part of the selected energy functional.

The total energy is the scalar quantity used by the reference force and stress differentiation interfaces.

---

## 5. Total Energy

The total scalar energy is denoted:

`E_total`

or:

`E`

when no ambiguity exists.

The total energy belongs to the energy codomain of the selected model.

It is distinct from:

- ternary state;
- resonance state;
- resonance classification;
- formal ionic charge;
- validation state;
- graph state;
- scheduler state;
- scale index.

---

## 6. Energy and Ternary State

The framework preserves:

`energy ≠ ternary state`

A ternary value:

`-1`

`0`

or:

`1`

is not an energy value solely because the energy model may consume ternary-conditioned features.

A ternary state does not define an energy magnitude without an explicit energy functional.

---

## 7. Energy and Resonance State

A resonance state is not energy.

A resonance descriptor is not energy.

A resonance-region classification is not energy.

The relation:

`resonance classification ≠ energy`

is retained.

Resonance information may affect an energy model only through an explicitly defined representation or conditioning interface.

---

## 8. Energy and Formal Charge

Formal ionic charge and energy belong to separate domains.

A formal-charge value does not define an energy contribution by itself.

An electrostatic or charge-dependent energy model, when introduced, must define an explicit mapping from its charge representation and geometry into energy.

---

## 9. Energy-Model Input

A generic interatomic energy model may be written:

`E_model: X_CFG × X_G × X_F × X_T × P_E → R`

where:

- `X_CFG` is atomic-configuration state;
- `X_G` is interaction-graph state;
- `X_F` is feature state;
- `X_T` is ternary execution state where conditioning is used;
- `P_E` is the energy-model parameter space.

A concrete model may use a different explicitly declared domain.

---

## 10. Reference Energy-Model Inputs

The executable reference model consumes:

- `AtomicConfiguration`;
- `InteractionGraph`;
- `NodeFeatureVector`;
- `TernaryExecutionVector`.

Its stored model components are:

- `RadialMessageOperator`;
- `TernaryConditioning`;
- `LinearInvariantEnergyFunctional`.

The model output is:

`EnergyModelResult`.

---

## 11. Configuration Boundary

Atomic configuration contains the geometric and species information required by the corresponding interatomic layer.

The reference energy model checks that:

`graph.node_count = configuration.atom_count`

`features.node_count = configuration.atom_count`

`execution.node_count = configuration.atom_count`

These cardinality conditions are part of the executable input contract.

---

## 12. Interaction-Graph Boundary

An interaction graph defines the graph structure supplied to the energy model.

An interaction-graph edge is not automatically:

- a chemical bond;
- an energy contribution;
- a force;
- a resonance relation;
- a ternary transition.

Its influence on energy occurs through the declared equivariant message-passing and energy-model interfaces.

---

## 13. Graph Construction and Energy Evaluation

Graph construction and energy evaluation are separate operations.

A graph may be produced from geometry by a graph-building rule.

The energy model consumes the graph supplied to it.

The energy model does not infer a different graph topology unless its own contract explicitly contains graph construction.

---

## 14. Feature Boundary

The interatomic feature state is represented separately from atomic configuration and graph topology.

A feature vector may contain:

- invariant scalar channels;
- equivariant vector channels;
- other explicitly defined representation channels in a specialized model.

Feature semantics are determined by their declared representation type.

---

## 15. Spatial Transformation Boundary

Spatial transformations act on geometric and equivariant quantities according to their representation.

Balanced ternary state is not a spatial transformation variable.

The relation:

`spatial rotation ≠ ternary polarity reversal`

is retained throughout the energy model.

---

## 16. Equivariant Energy Architecture

The interatomic energy chain is represented as:

`atomic configuration`

`→ graph-relative geometric inputs`

`→ invariant/equivariant feature transformation`

`→ conditioned feature state`

`→ invariant scalar energy functional`

`→ atomic energy contributions`

`→ total scalar energy`

Each arrow is an explicit model operation.

---

## 17. Reference Conditioned Layer

The reference energy model evaluates:

`conditioned_equivariant_layer_step(...)`

before applying the scalar energy functional.

The result is represented by:

`ConditionedEquivariantLayerResult`

The energy functional is evaluated on:

`layer_result.current`

---

## 18. Reference Scalar Functional

The executable reference scalar functional is:

`LinearInvariantEnergyFunctional`

It contains:

- `weights`;
- `bias`.

The required number of scalar channels is:

`len(weights)`

The input feature vector must contain the same number of scalar channels.

---

## 19. Reference Atomic-Energy Formula

For one node with invariant scalar channels:

`(s_1, ..., s_M)`

and weights:

`(w_1, ..., w_M)`

the reference atomic contribution is:

`E_i = sum_j w_j s_ij + b`

where:

- `w_j` is the weight of scalar channel `j`;
- `s_ij` is scalar channel `j` at atom `i`;
- `b` is the reference functional bias.

The total is:

`E_total = sum_i E_i`

---

## 20. Scalar-Channel Boundary

The reference `LinearInvariantEnergyFunctional` directly consumes scalar feature channels.

Vector channels do not enter that linear scalar functional directly.

Vector channels may participate in upstream equivariant computation according to the corresponding equivariant-layer contract.

---

## 21. Invariant Energy Output

The final total energy is a scalar.

For an energy model intended to preserve a specified spatial symmetry, the scalar energy output must satisfy the corresponding invariance relation under that symmetry.

The applicable transformation group and assumptions must be declared by the model.

---

## 22. E(3) Boundary

Where the model declares E(3)-invariant scalar energy:

`E(g · X) = E(X)`

for admissible:

`g ∈ E(3)`

under the declared transformation actions and model assumptions.

The exact transformation contract is defined by the equivariant representation layer.

---

## 23. Translation Boundary

A translation-invariant energy model must satisfy:

`E(X translated by a) = E(X)`

for admissible translations:

`a ∈ R^3`

under the declared representation and boundary conditions.

Translation invariance is a property of the complete energy mapping, not of a scalar storage type alone.

---

## 24. Rotation Boundary

A rotation-invariant energy model must satisfy:

`E(QX) = E(X)`

for admissible:

`Q ∈ SO(3)`

under the declared representation.

Rotation of geometry is not a ternary polarity transformation.

---

## 25. Reflection Boundary

Where the selected model is O(3)- or E(3)-invariant, reflection behavior follows the declared representation contract.

Reflection semantics are separate from ternary-state semantics.

---

## 26. Permutation Boundary

For equivalent atomic reindexing under the selected model, total scalar energy must preserve the declared permutation symmetry.

A permutation of atomic indices is not a ternary-state transition.

---

## 27. Ternary Conditioning

The reference energy model contains:

`TernaryConditioning`

The conditioning input is a retained ternary execution vector.

Ternary conditioning acts on feature channels according to its declared conditioning rule.

It does not redefine the mathematical type of energy.

---

## 28. Retained-State Conditioning

The reference energy model consumes:

`TernaryExecutionVector`

The conditioning state corresponds to retained ternary execution state.

A requested ternary target is not automatically substituted for retained execution state.

Therefore:

`target ≠ conditioning retained state`

unless a specialized energy model explicitly defines target-based conditioning.

---

## 29. Neutral Conditioning

Active neutral state:

`0`

may produce a model-defined conditioning response.

The response is determined by the explicit conditioning parameters.

Active neutral conditioning is not required to annihilate the feature state.

Therefore:

`ternary neutral 0 ≠ numerical multiplication by zero`

as a universal rule.

---

## 30. Ternary Conditioning and Energy Sign

Ternary polarity does not determine energy sign.

The following implications are not framework identities:

`-1 → negative energy`

`0 → zero energy`

`1 → positive energy`

Any such relation requires a separately defined energy model.

---

## 31. Resonance Conditioning

A specialized energy model may consume resonance-conditioned features or resonance-derived parameters.

The mapping must specify:

- resonance source state;
- descriptor or parameter mapping;
- representation being conditioned;
- parameters;
- transformation behavior;
- numerical update order.

Resonance state is not energy.

---

## 32. Phase Coupling Boundary

Phase coupling is not mechanical force.

The relation:

`phase coupling ≠ mechanical force`

is retained.

A phase-coupling parameter can influence an energy model only through an explicit model mapping.

---

## 33. Phase Relation Boundary

A phase relation is not automatically a chemical bond.

The relation:

`phase relation ≠ chemical bond`

is retained.

An energy model that uses both graph relations and phase relations must define their roles independently.

---

## 34. Conservative Model Definition

Within this repository contract, a conservative interatomic model defines force through the spatial derivative of a declared scalar energy model.

For a differentiable exact model:

`F_i = - partial E / partial r_i`

where:

`r_i ∈ R^3`

is the Cartesian position of atom `i`.

The sign convention is part of the force contract.

---

## 35. Reference Force Approximation

The executable reference force evaluator uses central finite differences.

For atom `i` and Cartesian component `alpha`:

`F_i,alpha ≈ -[E(X_i,alpha+h) - E(X_i,alpha-h)] / (2h)`

where:

`h > 0`

is the coordinate differentiation step.

---

## 36. Coordinate Differentiation Policy

The executable coordinate-differentiation policy is:

`CoordinateDifferentiation`

Its parameter is:

`step`

The step must be:

- a real non-Boolean number;
- finite;
- strictly positive.

The default executable value is:

`1.0e-6`

This value is an implementation default of the reference numerical differentiation policy.

It is not a universal TR-EIF physical constant.

---

## 37. Central-Difference Span

For coordinate step:

`h`

the reference implementation uses:

`1 / (2h)`

as:

`inverse_central_span`

The force derivative is therefore evaluated symmetrically around the reference coordinate.

---

## 38. Coordinate Perturbation

One force derivative perturbs exactly one Cartesian component of one atom at a time.

For atom:

`i`

and component:

`alpha ∈ {0, 1, 2}`

the two configurations are:

`X_plus = X with r_i,alpha increased by h`

`X_minus = X with r_i,alpha decreased by h`

Species, cell, and periodic flags are retained by the reference coordinate perturbation.

---

## 39. Fixed-Graph Force Differentiation

During one coordinate derivative evaluation, the reference force evaluator supplies the same:

`InteractionGraph`

to both:

`E(X_plus)`

and:

`E(X_minus)`

Therefore the graph topology is held fixed within that numerical derivative evaluation.

---

## 40. Fixed Graph Does Not Mean Globally Fixed Graph

The fixed-graph derivative contract applies to the local central-difference energy derivative.

It does not require the interaction graph to remain fixed across different physical states.

A molecular-dynamics or other geometry-evolution layer may rebuild the graph between physical states according to its own graph-construction contract.

---

## 41. Force Graph Scope

The two statements:

`graph fixed within one force derivative`

and:

`graph may be rebuilt between physical states`

refer to different scopes.

They are not contradictory.

The force derivative uses the first scope.

Molecular-dynamics graph reconstruction may use the second scope.

---

## 42. Feature State during Force Differentiation

The reference force evaluator supplies the same input:

`NodeFeatureVector`

to the plus and minus energy evaluations.

Coordinate dependence then enters through the perturbed atomic configuration and the computations performed by the reference energy model using that configuration and fixed graph.

---

## 43. Ternary Execution State during Force Differentiation

The reference force evaluator supplies the same:

`TernaryExecutionVector`

to both plus and minus energy evaluations.

Ternary execution is not performed inside one coordinate finite-difference derivative.

---

## 44. No Hidden Ternary Evolution in Force Evaluation

A force evaluation must not be interpreted as a ternary execution step.

The relations remain:

`force evaluation ≠ target generation`

`force evaluation ≠ neutral routing`

`force evaluation ≠ ternary commit`

unless a different explicitly coupled model defines such operations.

---

## 45. Force-State Representation

The executable force representation is:

`ForceState`

It contains:

`forces = (F_1, ..., F_N)`

with:

`F_i ∈ R^3`

Each force component must be a finite real number.

The force collection must be nonempty.

---

## 46. Force Cardinality

The reference force result contains one Cartesian force vector per atom.

Therefore:

`force_state.atom_count = configuration.atom_count`

for a successful reference force evaluation.

---

## 47. Force and Graph Edge

A graph edge is not a force vector.

Graph topology influences the energy representation through the model.

Force is obtained from the energy derivative under the force-evaluation contract.

Therefore:

`graph edge ≠ mechanical force`

---

## 48. Force and Message

An equivariant message is not itself a force unless a model explicitly defines that message as a force representation.

The reference force interface derives force from the scalar energy output.

---

## 49. Force and Ternary State

The framework preserves:

`force ≠ ternary state`

A force component numerically equal to:

`-1`

`0`

or:

`1`

remains a force component.

It does not become a balanced ternary state through numerical equality.

---

## 50. Stress Domain

Stress is represented separately from energy and force.

A Cartesian stress tensor is denoted:

`sigma ∈ R^(3×3)`

under the selected stress convention.

The executable stress representation is:

`StressState`

---

## 51. Reference Stress Representation

`StressState`

contains:

`tensor`

with exactly three rows and three components per row.

All tensor components must be finite real values.

The class exposes:

- `trace`;
- `is_symmetric`.

The constructor validates tensor shape and numerical finiteness.

---

## 52. Stress Symmetry Boundary

The generic `StressState` representation does not itself require symmetry at construction.

The property:

`is_symmetric`

tests exact component symmetry.

The reference conservative stress evaluator produces a mirrored symmetric tensor by construction.

---

## 53. Stress from Strain Derivative

The reference stress evaluator derives stress from homogeneous strain derivatives of the scalar energy.

For Cartesian components:

`a`

and:

`b`

the reference finite-difference form is:

`sigma_ab ≈ [E(epsilon_ab=+h) - E(epsilon_ab=-h)] / (2h V_0)`

where:

`V_0`

is the absolute reference-cell volume.

---

## 54. Stress Sign Convention

The reference stress evaluator uses:

`positive energy derivative divided by reference volume`

under its implemented strain convention.

No additional leading minus sign is introduced by the executable reference stress evaluator.

This sign convention belongs to the reference stress contract.

Alternative stress sign conventions must be declared separately.

---

## 55. Cell Requirement

Reference stress evaluation requires an atomic configuration with a simulation cell.

If:

`configuration.cell is None`

the reference evaluator rejects the stress evaluation.

---

## 56. Cell Volume

The reference cell volume is:

`V_0 = abs(det(H))`

where:

`H`

is the reference cell matrix under the repository cell representation.

Stress evaluation requires:

`V_0 ≠ 0`

---

## 57. Strain Differentiation Policy

The executable strain-differentiation policy is:

`CellStrainDifferentiation`

Its parameter is:

`step`

The step must be:

- a real non-Boolean number;
- finite;
- strictly positive.

The default executable value is:

`1.0e-6`

This is an implementation default of the reference strain-differentiation policy.

---

## 58. Homogeneous Strain

The reference stress evaluator applies homogeneous Cartesian strain to:

- atomic positions;
- simulation-cell vectors.

Both are transformed by the same Cartesian transformation matrix.

---

## 59. Diagonal Strain Components

For:

`a = b`

the reference strain matrix adds:

`h`

to the corresponding diagonal component of the identity transformation.

---

## 60. Off-Diagonal Strain Components

For:

`a ≠ b`

the reference strain matrix distributes the selected strain symmetrically:

`h/2`

into:

`(a,b)`

and:

`(b,a)`

This defines the executable off-diagonal strain convention.

---

## 61. Stress Tensor Construction

The reference evaluator computes only:

`a ≤ b`

components directly.

Each computed component is then assigned symmetrically:

`sigma_ab = sigma_ba`

The resulting tensor is symmetric by construction.

---

## 62. Fixed-Graph Stress Differentiation

During one strain derivative evaluation, the same:

`InteractionGraph`

is supplied to:

`E(H_plus, R_plus)`

and:

`E(H_minus, R_minus)`

Therefore graph topology is held fixed within that strain derivative.

---

## 63. Stress Graph Scope

Fixed graph topology inside one numerical strain derivative does not require graph topology to remain fixed across independent physical configurations.

Graph rebuilding between physical states remains a separate operation.

---

## 64. Feature State during Stress Differentiation

The reference stress evaluator supplies the same:

`NodeFeatureVector`

to plus-strain and minus-strain energy evaluations.

The strain operation changes positions and cell according to the strain contract.

---

## 65. Ternary State during Stress Differentiation

The reference stress evaluator supplies the same:

`TernaryExecutionVector`

to plus-strain and minus-strain energy evaluations.

Stress differentiation does not execute a ternary-state transition.

---

## 66. Stress and Ternary State

The framework preserves:

`stress ≠ ternary state`

A stress component numerically equal to one of the balanced ternary labels remains a stress component.

---

## 67. Stress and Resonance Classification

Stress is not a resonance-region classification.

A resonance-region transition does not by itself define a stress change.

Any coupling requires an explicit physical or learned model.

---

## 68. Conservative Differentiation Chain

The reference force chain is:

`configuration`

`→ plus/minus coordinate perturbation`

`→ scalar energy evaluations`

`→ central energy derivative`

`→ negative derivative`

`→ ForceState`

The reference stress chain is:

`configuration with cell`

`→ plus/minus homogeneous strain`

`→ scalar energy evaluations`

`→ central strain derivative`

`→ division by reference volume`

`→ symmetric StressState`

---

## 69. Energy as Derivative Source

The force and stress interfaces use the same scalar energy-model interface as their derivative source.

Force and stress are therefore downstream observables of the declared energy mapping under the reference differentiation policies.

---

## 70. Energy-Model Result

The executable reference result is:

`EnergyModelResult`

It contains:

- `layer_result`;
- `energy`.

The result validates that:

`energy.atom_count = layer_result.current.node_count`

This preserves cardinality between the conditioned feature state and atomic energy contributions.

---

## 71. Layer Result and Energy

`layer_result`

and:

`energy`

are distinct objects.

The layer result contains interatomic feature information.

The energy object contains atomic scalar contributions and total scalar energy.

---

## 72. Energy Functional and Model

The energy functional and the complete energy model are different architectural objects.

The reference functional:

`LinearInvariantEnergyFunctional`

maps a feature vector into energy.

The reference model:

`ReferenceEnergyModel`

first computes a conditioned equivariant layer result and then applies the energy functional.

---

## 73. Functional Parameter Boundary

The reference linear functional contains weights and a bias.

These numerical parameters must be finite.

The weights tuple must be nonempty.

The functional does not assign physical units or empirical provenance by itself.

Those properties belong to the surrounding physical-model contract.

---

## 74. Parameter Provenance

Physical or empirically fitted energy-model parameters require provenance appropriate to their origin.

Relevant provenance classes may include:

- `PRIMARY_SOURCE`;
- `DERIVED`;
- `CALIBRATED`;
- `AUTHOR_DEFINED`;
- `BENCHMARK`;
- `TEST_FIXTURE`;
- `REQUIRES_SOURCE`;
- `REQUIRES_TEST`.

A numeric value without a declared physical provenance must not be presented as a sourced physical constant.

---

## 75. Test-Fixture Parameters

A parameter classified as:

`TEST_FIXTURE`

is a test value.

It is not a physical reference value unless separately sourced and reclassified.

---

## 76. Units Boundary

The generic energy package does not impose one universal physical unit system.

A physical specialization must define units for:

- positions;
- energy;
- force;
- stress;
- differentiation steps;
- model parameters;

where these quantities receive physical interpretation.

---

## 77. Dimensional Consistency

For a physical energy model:

`dim(force) = dim(energy) / dim(length)`

under the selected coordinate convention.

For stress:

`dim(stress) = dim(energy) / dim(volume)`

under the reference strain derivative convention.

A numerical implementation must preserve the selected unit contract.

---

## 78. Differentiation-Step Units

The coordinate differentiation step has the same length dimension as the perturbed Cartesian coordinate when the model uses physical units.

The strain differentiation step is dimensionless under the homogeneous strain convention.

The generic Python representation stores these steps as finite floating-point values.

---

## 79. Energy-Scale Boundary

The balanced ternary values:

`-1/0/1`

do not define an energy scale.

A scalar energy functional may return any finite value permitted by its declared parameterization and feature state.

---

## 80. Offset Energy

The reference linear functional contains a per-node bias.

Changing this bias changes atomic and total energy according to the declared formula.

The physical interpretation of an energy offset belongs to the specialized model and validation contract.

---

## 81. Force under Constant Energy Offset

For an exact differentiable energy model, a coordinate-independent constant total-energy offset does not alter spatial derivatives.

For the reference per-node bias, the effect on derivatives depends on whether the number of represented nodes remains fixed and whether the bias itself is coordinate-independent.

The reference coordinate perturbation preserves atom count.

---

## 82. Stress under Constant Energy Offset

A coordinate- and strain-independent constant energy offset does not alter the corresponding energy derivative.

The reference stress differentiation preserves atom count while perturbing positions and cell.

---

## 83. Graph Discontinuity Boundary

A graph-construction rule based on a geometric cutoff may change topology when geometry changes.

The reference finite-difference force and stress evaluators do not rebuild graph topology inside one derivative evaluation.

Therefore the reference derivative is explicitly a fixed-graph numerical derivative.

---

## 84. Fixed-Graph Derivative Interpretation

A fixed-graph derivative differentiates the energy realization associated with the supplied graph topology while perturbing the declared geometric variables.

It is not automatically identical to a derivative of a model in which graph topology is reconstructed for every infinitesimal perturbation.

The derivative contract must identify which interpretation is used.

---

## 85. Molecular-Dynamics Graph Boundary

The reference molecular-dynamics execution may rebuild the interaction graph between physical states.

Each force evaluation performed at one physical state may still use fixed topology internally for its coordinate finite differences.

The scopes are:

`physical-state graph construction`

and:

`local derivative evaluation`

---

## 86. Molecular-Dynamics Energy Interface

Molecular dynamics may evaluate potential energy through:

`ReferenceEnergyModel`

or another model implementing the declared energy interface.

The molecular-dynamics state and the energy-model state remain separate objects.

---

## 87. Potential Energy

Within molecular dynamics, the scalar energy returned by the interatomic energy model may serve as potential energy under the selected MD contract.

Kinetic energy is defined separately from velocities and masses.

The relation:

`total MD energy = kinetic energy + potential energy`

belongs to the corresponding molecular-dynamics observable contract.

---

## 88. Potential and Ternary State

Potential energy is not a ternary state.

Retained ternary state may condition the model that produces potential energy.

Conditioning does not merge their codomains.

---

## 89. Energy Drift Boundary

Energy drift is a trajectory-derived numerical observable.

It is not the same object as the instantaneous energy functional.

An energy-drift test evaluates properties of a numerical trajectory under specified conditions.

It does not redefine the energy functional.

---

## 90. Thermostat Boundary

A thermostat, when present in a molecular-dynamics specialization, may exchange energy with modeled degrees of freedom according to its declared dynamics.

Such a trajectory is not described by an isolated-energy conservation statement unless the relevant extended-system invariant is defined.

The generic energy-model contract remains unchanged.

---

## 91. Barostat Boundary

A barostat, when present, introduces cell or pressure-control dynamics under its declared model.

The energy/stress interfaces used by a barostat must retain their declared sign, unit, and differentiation conventions.

---

## 92. Continuous-Discrete Ordering

When energy depends on retained ternary conditioning, the coupled numerical realization must define which retained ternary state is supplied to a given energy evaluation.

A target value is not substituted implicitly.

Operator ordering is part of the coupled model contract.

---

## 93. Fixed Ternary State within One Derivative

The reference force and stress evaluators hold the supplied ternary execution vector fixed throughout one finite-difference derivative evaluation.

This prevents hidden ternary execution from occurring between the plus and minus energy evaluations.

---

## 94. Fixed Features within One Derivative

The reference force and stress evaluators hold the supplied input feature vector fixed as an input object across the paired energy evaluations.

The energy model may recompute geometry-dependent conditioned layer results from the perturbed configuration according to its own internal operations.

---

## 95. Force-Energy Consistency

A force result is consistent with the reference differentiation contract when each component equals the negative central difference of the same scalar energy model using:

- the same reference graph;
- the same input feature state;
- the same retained ternary execution state;
- the configured coordinate step.

---

## 96. Stress-Energy Consistency

A stress result is consistent with the reference differentiation contract when each tensor component equals the declared symmetric homogeneous-strain central difference using:

- the same reference graph;
- the same input feature state;
- the same retained ternary execution state;
- the configured strain step;
- the reference cell volume.

---

## 97. Energy Consistency and Physical Calibration

Mathematical or numerical consistency between energy, force, and stress does not itself establish empirical calibration.

Empirical calibration requires a corresponding data and provenance contract.

These validation categories remain distinct.

---

## 98. Energy Consistency and Determinism

Energy-gradient consistency and deterministic replay are distinct properties.

A model may be tested separately for:

- deterministic energy evaluation;
- force-gradient consistency;
- stress-strain consistency.

No one property substitutes for another.

---

## 99. Deterministic Energy Evaluation

For a deterministic energy model, identical complete admissible inputs and identical parameters produce identical declared energy output under the same numerical execution contract.

The complete result-affecting input includes every state variable consumed by the energy mapping.

---

## 100. Deterministic Force Evaluation

For deterministic force evaluation, identical:

- model;
- configuration;
- interaction graph;
- features;
- retained ternary execution state;
- coordinate differentiation policy

produce identical declared force output under the same execution environment contract.

---

## 101. Deterministic Stress Evaluation

For deterministic stress evaluation, identical:

- model;
- configuration;
- interaction graph;
- features;
- retained ternary execution state;
- strain differentiation policy

produce identical declared stress output under the same execution environment contract.

---

## 102. Floating-Point Boundary

The executable reference model uses floating-point arithmetic.

Floating-point results belong to the numerical realization.

Exact mathematical identities and floating-point equality are separate validation categories.

Tolerance-based numerical comparisons must state their tolerance contract.

---

## 103. Energy-State Finiteness

The reference `EnergyState` requires finite atomic-energy contributions and finite total energy.

NaN and infinite values are rejected by the state constructor.

A rejected numerical energy is not represented as ternary neutral `0`.

---

## 104. Force-State Finiteness

The reference `ForceState` requires finite Cartesian components.

NaN and infinite force components are rejected.

Numerical failure is not encoded as a ternary state.

---

## 105. Stress-State Finiteness

The reference `StressState` requires finite Cartesian tensor components.

NaN and infinite stress components are rejected.

Numerical failure remains separate from balanced ternary semantics.

---

## 106. Missing Observable Boundary

An unavailable energy, force, or stress observable is represented separately from valid numerical zero.

The relation:

`missing observable ≠ active ternary neutral 0`

is retained.

---

## 107. Zero Energy

A scalar energy value:

`E = 0`

is an energy value.

It is not the active ternary neutral state.

Therefore:

`energy zero ≠ ternary neutral 0`

---

## 108. Zero Force

A force vector:

`F_i = (0, 0, 0)`

is a physical or numerical force value.

It is not a ternary neutral state.

---

## 109. Zero Stress

A zero stress tensor is a stress value.

It is not a ternary neutral state.

---

## 110. Energy Output Serialization

A serialized energy output must preserve:

- atomic contributions where included;
- total energy;
- field identity;
- numerical values;
- schema version where a schema is defined.

Serialization does not redefine the physical or mathematical meaning of energy.

---

## 111. Force Output Serialization

A serialized force output must preserve one three-component force vector per represented atom under the declared schema.

Atomic ordering must remain identifiable.

---

## 112. Stress Output Serialization

A serialized stress output must preserve the complete `3 × 3` tensor under the declared component-order convention.

A schema must state tensor ordering when machine interchange is required.

---

## 113. Trace Boundary

Energy, force, and stress may appear in an observable trace.

A trace record is an observable artifact.

It is not the energy model itself.

The relation:

`state ≠ trace`

is retained.

---

## 114. Trace Reproducibility

Where deterministic replay includes energy outputs, canonical replay must reproduce the declared serialized representation according to the replay contract.

Force and stress may be included when the trace schema declares them.

---

## 115. Validation Categories

Energy-model validation may contain separate tests for:

- type and cardinality contracts;
- finite-value requirements;
- invariant scalar-energy construction;
- equivariance/invariance behavior;
- deterministic energy evaluation;
- force-gradient consistency;
- stress-strain consistency;
- translation behavior;
- rotation behavior;
- reflection behavior where applicable;
- permutation behavior;
- numerical differentiation convergence;
- molecular-dynamics energy behavior;
- empirical energy/force/stress reproduction where sourced data exist.

Each category tests its declared property.

---

## 116. Force-Gradient Validation

Force-gradient validation compares the declared force output against the energy derivative under a stated differentiation method.

The reference implementation defines force directly through central finite differentiation of the energy model.

Alternative analytic-gradient implementations must preserve the same declared energy derivative semantics if they claim correspondence to this contract.

---

## 117. Stress Validation

Stress validation compares the declared stress output with the selected strain derivative of the same scalar energy model under a stated stress convention.

The sign and strain conventions must be included in the validation definition.

---

## 118. Numerical Convergence

Finite-difference derivative validation may evaluate behavior across multiple positive differentiation steps.

Convergence testing belongs to numerical validation.

The existence of a default step does not establish universal convergence for every model or configuration.

---

## 119. Singular and Nonsmooth Boundaries

A model may contain points at which the energy mapping is nondifferentiable or the numerical derivative is not stable under the selected step.

Such cases belong to the model-domain and numerical-validation contracts.

They are not represented by a ternary state unless a separate mapping is defined.

---

## 120. Domain Detection

A model-domain detector, where present, may identify whether an input lies inside a declared model domain.

Domain status is not energy.

Domain status is not ternary state.

The relation:

`validation or domain status ≠ ternary state`

is retained.

---

## 121. Uncertainty Boundary

An uncertainty estimate associated with energy, force, or stress is a separate observable or metadata quantity.

High uncertainty is not active ternary neutral state.

The relation:

`uncertainty ≠ ternary state`

is retained.

---

## 122. Learning Boundary

A learned energy model may parameterize the scalar energy functional or upstream feature transformations.

Training state and inference state remain separate.

A training-stage transition is not a ternary-state transition.

---

## 123. Energy Training

Energy-reference data may contribute to a training objective through an explicitly defined energy loss.

The training loss is not the physical energy itself.

The relation:

`loss functional ≠ energy functional`

must remain explicit when both are present.

---

## 124. Force Training

Force-reference data may contribute to training through a force loss.

A force loss compares model-derived forces with reference forces under the selected learning contract.

The loss value is not a physical force.

---

## 125. Stress Training

Stress-reference data may contribute to training through a stress loss.

The training contract must preserve the same component ordering and stress convention used by the reference data and model.

---

## 126. Reference-Data Provenance

Physical training and validation data must retain their data provenance.

Reference energy, force, stress, geometry, and cell data require source or generation metadata according to the project provenance system.

---

## 127. First-Principles Reference Boundary

First-principles energy, force, or stress values, when used, are reference data.

They do not become framework axioms.

Their computational method, configuration, and provenance belong to the reference-data contract.

---

## 128. Experimental Reference Boundary

Experimental observables and model energy quantities may belong to different measurement spaces.

Comparison requires an explicit observable mapping where direct equality is not defined.

An experimental observable must not be silently identified with a latent model quantity.

---

## 129. Material Specialization

A material-specific energy model may define:

- species-specific parameters;
- material-specific descriptors;
- sourced training data;
- calibrated energy parameters;
- domain constraints;
- material-specific validation criteria.

These additions specialize the energy model without redefining framework-wide ternary or equivariance semantics.

---

## 130. FLiBe Energy Boundary

A FLiBe-specific TR-EIP realization must define its energy mapping separately from:

- formal ionic-charge bookkeeping;
- FLiBe thermodynamic-state metadata;
- density model;
- coordination descriptor;
- resonance parameterization;
- ternary target interpretation.

These quantities may interact only through declared mappings.

---

## 131. Formal Charge in FLiBe Energy

The committed FLiBe formal-charge layer defines bookkeeping charges.

Those formal charges are not automatically:

- partial charges;
- effective charges;
- force-field charges;
- learned charges;
- electrostatic-energy parameters.

A FLiBe energy realization using charge information must declare the charge model it consumes.

---

## 132. FLiBe Coordination Boundary

Graph-relative FLiBe coordination is a structural descriptor.

It is not automatically a chemical-bond count.

It is not itself an energy.

A FLiBe energy model may consume coordination-derived features only through an explicit model interface.

---

## 133. FLiBe Resonance Boundary

FLiBe resonance parameterization produces phase-dynamics parameters under its declared contract.

Those parameters are not energy values.

Any influence on a FLiBe energy realization requires an explicit conditioning or feature mapping.

---

## 134. FLiBe Ternary Boundary

FLiBe ternary interpretation produces a requested target.

The energy reference model uses retained execution state where ternary conditioning is applied.

Therefore:

`FLiBe requested target ≠ retained energy-conditioning state`

unless a specialized energy model explicitly defines a different interface.

---

## 135. Multiscale Energy Boundary

A multiscale reduction does not automatically preserve energy unless the corresponding coarse-graining and closure contract explicitly defines energy transfer.

Additive scalar reduction, mass reduction, centroid construction, and energy coarse-graining are separate operations.

---

## 136. Scale Transition and Energy

A scale transition is not an energy change by definition.

A coarse-state construction may change representation while preserving, approximating, or redefining selected observables according to its explicit closure.

Energy transfer across scales requires its own mapping.

---

## 137. Continuum Boundary

A continuum energy density, total atomistic energy, and coarse-scale energy variable are different quantities unless a cross-scale mapping defines their relationship.

Dimensional consistency must be preserved across such mappings.

---

## 138. Thermodynamic Consistency Boundary

Thermodynamic quantities such as temperature and pressure are not inferred from the scalar interatomic energy alone without the corresponding statistical-mechanical and ensemble definitions.

The energy model contract does not by itself define a thermostat, barostat, equation of state, or free-energy model.

---

## 139. Internal Energy Boundary

A model potential energy and thermodynamic internal energy are not interchangeable terms without a declared thermodynamic mapping.

The energy variable must retain the name and definition of the selected layer.

---

## 140. Free-Energy Boundary

Free energy is not automatically the same object as the reference potential-energy functional.

A free-energy model requires its own state variables, ensemble assumptions, and thermodynamic definition.

---

## 141. Enthalpy Boundary

Enthalpy is not automatically produced by the reference interatomic energy model.

A thermodynamic enthalpy definition requires the corresponding pressure-volume terms and conventions.

---

## 142. Conservation Statement Boundary

A conservative energy model defines force from an energy derivative under its declared contract.

This does not by itself guarantee exact numerical conservation of total energy for every time integrator, timestep, trajectory, or coupled control system.

Numerical conservation is tested separately.

---

## 143. Continuous Energy Conservation

Where a continuous isolated dynamical model has a conserved energy, the conservation statement must specify:

- the complete state;
- energy functional;
- equations of motion;
- assumptions;
- boundary conditions.

The existence of the energy functional alone is not the complete conservation proof.

---

## 144. Numerical Energy Conservation

A numerical trajectory may exhibit finite energy drift.

Energy-drift behavior depends on:

- integration method;
- timestep;
- force accuracy;
- model smoothness;
- graph treatment;
- arithmetic;
- coupled control operations.

Numerical energy-conservation tests therefore belong to the numerical validation layer.

---

## 145. Graph Rebuild and Energy Continuity

A discrete change of interaction-graph topology may alter the numerical energy realization if the model depends explicitly on that topology.

Continuity across graph changes is a property requiring separate analysis or validation.

The fixed-graph derivative contract does not assert continuity across graph-topology changes.

---

## 146. Cutoff Boundary

A geometric cutoff used to construct the interaction graph is not itself an energy threshold.

If cutoff smoothing or continuous cutoff functions are required by a specialized model, those operations must be explicitly defined.

---

## 147. Neighbor List Boundary

A neighbor list or interaction graph is a computational representation of selected interactions.

It is not the scalar energy state.

A neighbor-list update policy belongs to geometry or molecular-dynamics execution rather than to the mathematical definition of energy.

---

## 148. Periodic Boundary Conditions

Periodic boundary conditions affect geometric relations according to the selected geometry contract.

Energy evaluation under periodic conditions must use the corresponding explicit image and graph representation.

Periodic image selection is not a ternary operation.

---

## 149. Cell Convention

A stress-capable model requires a defined cell representation.

The orientation of cell vectors and transformation convention must remain consistent between:

- configuration representation;
- geometric operations;
- homogeneous strain;
- volume evaluation;
- stress output.

---

## 150. Coordinate Convention

Cartesian coordinates used by the reference force evaluator have three components per atom.

Coordinate indexing is:

`0, 1, 2`

in the executable implementation.

This machine index is not a ternary state.

---

## 151. Energy Functional Extensibility

A specialized energy functional may replace the reference linear invariant functional.

A replacement must define:

- input feature space;
- parameter space;
- output energy state;
- symmetry behavior;
- differentiability assumptions;
- dimensional convention;
- deterministic behavior;
- validation requirements.

---

## 152. Analytic Force Implementation

A specialized implementation may compute analytic or automatic-differentiation forces.

If it is declared conservative with respect to the same energy model, it must implement:

`F_i = - partial E / partial r_i`

under the declared coordinate and state convention.

The numerical method may differ while the semantic derivative contract remains.

---

## 153. Analytic Stress Implementation

A specialized implementation may compute analytic or automatic-differentiation stress.

Its stress convention must remain explicitly defined and must correspond to the declared energy-strain derivative relation.

---

## 154. Differentiation State Closure

Every variable held fixed during a derivative must be identified by the derivative contract.

For the executable reference force derivative, fixed inputs include:

- graph;
- input features;
- retained ternary execution vector;
- model parameters.

The perturbed variable is one Cartesian coordinate component.

---

## 155. Strain-Derivative State Closure

For the executable reference stress derivative, fixed inputs include:

- graph;
- input features;
- retained ternary execution vector;
- model parameters.

The transformed variables are:

- atomic positions;
- simulation cell.

---

## 156. Parameter Differentiation Boundary

Coordinate and strain differentiation do not imply differentiation with respect to model parameters.

Parameter derivatives belong to learning or sensitivity-analysis contracts.

---

## 157. Ternary Differentiation Boundary

Balanced ternary state is discrete.

The reference coordinate and strain derivatives do not differentiate with respect to ternary state.

Ternary-state changes are handled by discrete execution semantics.

---

## 158. Graph Differentiation Boundary

The reference force and stress evaluators do not differentiate graph topology.

Graph topology is treated as fixed input during each local derivative.

---

## 159. Feature Differentiation Boundary

The input `NodeFeatureVector` is held fixed as an external input object during each reference finite-difference derivative.

Geometry-dependent feature changes internal to the energy-model layer follow that model's declared computation.

---

## 160. Energy Model and Scheduler

The generic energy model does not define scheduler state.

A scheduler may determine when energy is evaluated in a coupled runtime.

Scheduler execution does not alter the mathematical energy definition.

---

## 161. Energy Model and Routing

Neutral routing belongs to the ternary execution layer.

The energy model may consume retained ternary state after routing.

It does not itself define pending-route completion.

---

## 162. Energy Model and Active Neutral

Active neutral state may condition features through the selected ternary-conditioning parameters.

The energy model does not redefine active-neutral transition semantics.

---

## 163. Energy Model and Resonance Dynamics

Resonance dynamics are upstream or separately coupled dynamics.

The reference energy model does not integrate oscillator phase.

A coupled model must define the operator ordering between resonance evolution and energy evaluation.

---

## 164. Energy Model and Molecular-Dynamics Time

Energy evaluation is an instantaneous model operation at a supplied configuration and state.

It does not advance molecular-dynamics time.

Time advancement belongs to the molecular-dynamics integrator.

---

## 165. Force Evaluation and Molecular-Dynamics Time

Reference force evaluation performs multiple internal energy evaluations at perturbed configurations.

These perturbations are differentiation samples.

They are not additional physical molecular-dynamics time states.

---

## 166. Stress Evaluation and Molecular-Dynamics Time

Reference stress evaluation performs multiple energy evaluations at strained configurations.

These strained configurations are differentiation samples.

They are not additional physical trajectory states unless a separate simulation explicitly treats them as such.

---

## 167. Observable Ownership

Energy is owned by the energy-model observable layer.

Force is owned by the force observable layer.

Stress is owned by the stress observable layer.

A trace may record these values without becoming their defining mathematical model.

---

## 168. Validation Ownership

A PASS or FAIL result associated with energy tests belongs to validation state.

It is not an energy value.

It is not a ternary state.

---

## 169. Schema Boundary

A machine-readable energy-output schema may define serialization structure.

The schema must not redefine the mathematical energy functional.

Schema validity and physical validity are separate properties.

---

## 170. Energy Output Schema Requirements

A future energy-output schema must identify at minimum:

- schema identity;
- schema version;
- total energy field;
- atomic-energy field when present;
- numeric type requirements;
- atom-count relation where atomic contributions are present;
- unit metadata when physical units are claimed.

---

## 171. Force Output Schema Requirements

A future force-output schema must identify:

- atom ordering;
- vector component ordering;
- vector dimension;
- numeric finiteness requirements;
- unit metadata when physical units are claimed.

---

## 172. Stress Output Schema Requirements

A future stress-output schema must identify:

- tensor shape;
- component ordering;
- stress convention;
- unit metadata when physical units are claimed;
- symmetry expectation where applicable.

---

## 173. Reproducibility Inputs

A reproducible energy evaluation requires the result-affecting inputs, including:

- model implementation;
- model parameters;
- atomic configuration;
- graph;
- feature state;
- retained ternary execution state;
- numerical environment where required by the reproducibility contract.

---

## 174. Reproducibility Inputs for Forces

Force reproducibility additionally requires:

- coordinate differentiation policy;
- graph-topology treatment;
- coordinate convention.

---

## 175. Reproducibility Inputs for Stress

Stress reproducibility additionally requires:

- strain differentiation policy;
- cell representation;
- volume convention;
- strain convention;
- stress sign convention.

---

## 176. Reference Package

The executable conservative energy package is located under:

`src/tr_eif/energy/`

The package currently contains:

- `state.py`;
- `functional.py`;
- `model.py`;
- `differentiation.py`;
- `force.py`;
- `force_evaluator.py`;
- `strain.py`;
- `stress.py`;
- `stress_evaluator.py`;
- `__init__.py`.

---

## 177. Reference Public Interfaces

The current public energy package exports:

- `AtomicEnergies`;
- `AtomicForces`;
- `CellStrainDifferentiation`;
- `ConservativeForceEvaluator`;
- `ConservativeStressEvaluator`;
- `CoordinateDifferentiation`;
- `EnergyModelResult`;
- `EnergyState`;
- `ForceState`;
- `LinearInvariantEnergyFunctional`;
- `ReferenceEnergyModel`;
- `StressState`;
- `StressTensor`.

These are executable interfaces of the current reference implementation.

---

## 178. Mathematical References

The conservative energy formalism is documented in:

`docs/volume_03_equivariant_interatomic_framework/chapter_08_conservative_energy_functional.md`

Force and stress are documented in:

`docs/volume_03_equivariant_interatomic_framework/chapter_09_forces_and_stress.md`

The TR-EIP model family is documented in:

`docs/volume_03_equivariant_interatomic_framework/chapter_10_model_family_tr_eip.md`

---

## 179. Learning References

Energy, force, and stress training are documented in:

`docs/volume_04_learning_and_optimization/chapter_04_energy_force_stress_training.md`

The general loss-functional layer is documented in:

`docs/volume_04_learning_and_optimization/chapter_03_loss_functionals.md`

---

## 180. Repository-Level References

The framework architecture is defined in:

`docs/architecture/framework_architecture.md`

The continuous-discrete dynamics boundary is defined in:

`docs/architecture/continuous_discrete_contract.md`

The balanced ternary state specification is defined in:

`docs/specifications/ternary_state_specification.md`

Committed ternary transition semantics are defined in:

`docs/specifications/transition_semantics.md`

---

## 181. Energy Contract Invariants

The repository-level energy contract preserves:

`energy ≠ ternary state`

`force ≠ ternary state`

`stress ≠ ternary state`

`resonance classification ≠ energy`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`graph edge ≠ chemical bond`

`graph edge ≠ force`

`target ≠ retained ternary conditioning state`

`formal charge ≠ ternary state`

`formal charge ≠ energy`

`zero energy ≠ active ternary neutral state`

`zero force ≠ active ternary neutral state`

`zero stress ≠ active ternary neutral state`

`force evaluation ≠ ternary execution`

`stress evaluation ≠ ternary execution`

`coordinate perturbation ≠ physical time evolution`

`strain perturbation ≠ physical time evolution`

`graph fixed within derivative ≠ graph fixed across physical states`

`loss functional ≠ energy functional`

`validation status ≠ energy`

`validation status ≠ ternary state`

---

## 182. Reference Force Contract

The executable force contract is:

`configuration + fixed graph + features + retained ternary execution + energy model + coordinate differentiation`

`→ central energy differences`

`→ negative spatial derivative`

`→ ForceState`

No direct opposite ternary transition, target-generation event, or neutral-routing event is part of this derivative operator.

---

## 183. Reference Stress Contract

The executable stress contract is:

`configuration with cell + fixed graph + features + retained ternary execution + energy model + strain differentiation`

`→ symmetric plus/minus homogeneous strain`

`→ central energy differences`

`→ division by absolute reference-cell volume`

`→ symmetric StressState`

The stress sign convention is the one defined by this executable derivative.

---

## 184. Model Extension Rule

A specialized energy realization may add:

- additional invariant features;
- additional equivariant representations;
- nonlinear scalar functionals;
- material-specific parameters;
- resonance-conditioned parameters;
- ternary-conditioned parameters;
- analytic derivatives;
- learned potentials;
- multiscale energy mappings.

Such additions must preserve the framework-wide semantic boundaries unless an explicit framework revision changes them.

---

## 185. No Hidden Physical Semantics Rule

A computational variable receives physical meaning only through its declared physical model and unit contract.

A scalar output is not automatically physical energy solely because it is stored in `EnergyState`.

A calibrated or physical realization must define the units, parameter provenance, and validation domain associated with the scalar output.

---

## 186. No Hidden Ternary Semantics Rule

Energy, force, stress, differentiation steps, graph indices, atomic indices, and scalar feature values do not acquire balanced ternary semantics from numerical equality with `-1`, `0`, or `1`.

Only explicitly typed ternary state belongs to:

`T = {-1, 0, 1}`

---

## 187. No Hidden Bond Semantics Rule

An interaction edge, message, phase relation, or coordination count is not identified with chemical bonding unless a separately defined model introduces that mapping.

The energy model may depend on these quantities without changing this distinction.

---

## 188. No Hidden Conservation Claim Rule

The existence of a scalar energy functional and derivative-derived forces defines the conservative energy interface.

Claims about trajectory-level conservation require the corresponding dynamical equations, numerical method, boundary conditions, and validation evidence.

---

## 189. Contract Closure

The repository-level conservative energy architecture is:

`atomic/interatomic state`

`→ explicit interaction graph`

`→ invariant/equivariant representation`

`→ explicit retained-state conditioning`

`→ invariant scalar energy functional`

`→ atomic energy contributions`

`→ total scalar energy`

with the derivative interfaces:

`total scalar energy`

`→ coordinate derivative`

`→ force`

and:

`total scalar energy`

`→ homogeneous strain derivative`

`→ stress`

The reference force derivative uses fixed graph topology within each central-difference evaluation.

The reference stress derivative uses fixed graph topology within each central-difference strain evaluation.

Graph topology may be reconstructed between separate physical states under the corresponding graph or molecular-dynamics contract.

Energy, force, stress, resonance state, ternary state, formal charge, graph state, and validation state remain separately typed.
