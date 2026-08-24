# TR-EIF Documentation

## Ternary Resonant Equivariant Interatomic Framework

This directory contains the formal scientific, mathematical, computational, and engineering documentation of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

TR-EIF is organized as an integrated architecture in which:

- **TR** denotes the **Ternary Resonant** layer;
- **EIF** denotes the **Equivariant Interatomic Framework** layer;
- learning and optimization provide parameterization and model-training mechanisms;
- molecular dynamics provides atomistic time evolution;
- multiscale modeling connects atomistic representations to larger material scales;
- FLiBe provides the principal reference-model domain represented in the documentation structure.

The documentation is organized so that each layer has an explicit mathematical domain, state representation, transformation structure, computational interface, and validation boundary.

---

## Documentation Architecture

The documentation is divided into seven principal volumes and supporting architecture, specification, validation, and reference layers.

### Volume 01 — Mathematical Foundations

Directory:

`volume_01_mathematical_foundations/`

Defines the mathematical foundation used throughout TR-EIF.

The volume covers:

1. foundations;
2. notation and definitions;
3. axiomatic system;
4. state spaces;
5. mathematical operators;
6. mathematical structures;
7. mathematical mappings;
8. framework invariants;
9. fundamental lemmas;
10. fundamental theorems;
11. corollaries;
12. volume summary.

The mathematical foundation establishes the domains, codomains, mappings, invariants, and formal relations required by subsequent volumes.

---

### Volume 02 — Ternary Resonance Theory

Directory:

`volume_02_ternary_resonance_theory/`

Defines the Ternary Resonant layer of TR-EIF.

The volume covers:

1. resonance foundations;
2. Kuramoto–Sakaguchi formalism;
3. synchronization and coherence;
4. resonance-regime transitions;
5. continuous-to-ternary mapping;
6. active-neutral-state dynamics;
7. neutral routing;
8. coupled continuous-discrete dynamics;
9. stability and boundedness;
10. numerical time evolution;
11. volume summary.

The balanced ternary kernel is:

`-1/0/1`

with state space:

`T = {-1, 0, 1}`.

The state `0` is an active state and may participate in balancing, routing, damping, mediation, transition staging, retention, and controlled neutralization.

Direct opposite transitions are excluded:

`-1 → 1`

`1 → -1`

Opposite-polarity transitions are neutral-mediated:

`-1 → 0 → 1`

`1 → 0 → -1`

Each transition leg is a distinct state-transition event.

The resonance layer distinguishes resonance from synchronization, phase locking, coherence, phase order, structural order, bifurcation, ternary transition, structural transition, and physical phase transition.

---

### Volume 03 — Equivariant Interatomic Framework

Directory:

`volume_03_equivariant_interatomic_framework/`

Defines the EIF layer of TR-EIF.

The volume covers:

1. atomic configuration space;
2. interaction graphs;
3. E(3) group actions;
4. equivariant representations;
5. message passing;
6. resonance parameterization;
7. ternary feature channels;
8. conservative energy functional;
9. forces and stress;
10. TR-EIP model family;
11. volume summary.

The EIF layer operates on atomic and interatomic states with explicitly defined geometric and symmetry transformations.

Permutation, translation, and rotation behavior are treated separately.

Invariant and equivariant representations are distinguished formally through their transformation laws.

The EIF layer provides the interatomic representation on which resonance and ternary structures can be defined through explicit mappings.

---

### Volume 04 — Learning and Optimization

Directory:

`volume_04_learning_and_optimization/`

Defines the learning and optimization layer.

The volume covers:

1. learning problem;
2. training data;
3. loss functionals;
4. energy-force-stress training;
5. ternary regularization;
6. resonance regularization;
7. equivariance constraints;
8. uncertainty and domain detection;
9. optimization;
10. volume summary.

This layer connects the mathematical and interatomic architecture to trainable computational models while preserving the explicit TR-EIF structural constraints.

---

### Volume 05 — Molecular Dynamics

Directory:

`volume_05_molecular_dynamics/`

Defines atomistic time evolution using TR-EIF-compatible interatomic models and state representations.

The volume covers:

1. equations of motion;
2. time integrators;
3. thermostats and barostats;
4. periodic boundary conditions;
5. neighbor lists;
6. resonance-state propagation;
7. ternary-state propagation;
8. energy conservation;
9. transport observables;
10. volume summary.

Continuous mechanical state, resonance state, and discrete ternary state remain separately typed components of the computational state.

Their interactions are defined through explicit mappings and update rules.

---

### Volume 06 — Multiscale Materials Modeling

Directory:

`volume_06_multiscale_materials_modeling/`

Defines the multiscale architecture connecting different physical and computational scales.

The volume covers:

1. multiscale architecture;
2. electronic-to-interatomic mapping;
3. atomistic-to-mesoscale mapping;
4. continuum closure;
5. uncertainty transfer;
6. thermodynamic consistency;
7. transport-coefficient transfer;
8. engineering-scale models;
9. volume summary.

Each scale transition is treated as an explicit mapping with defined source space, target space, retained information, transferred observables, and closure assumptions.

---

### Volume 07 — FLiBe Reference Model

Directory:

`volume_07_flibe_reference_model/`

Defines the FLiBe reference-model layer.

The volume covers:

1. FLiBe system definition;
2. species and composition;
3. interatomic reference data;
4. thermodynamic properties;
5. transport properties;
6. local structure and coordination;
7. resonance parameterization;
8. ternary-state interpretation;
9. multiscale coolant model;
10. validation program;
11. volume summary.

The FLiBe layer provides a concrete reference domain in which the mathematical, equivariant, resonance, ternary, molecular-dynamics, and multiscale components can be connected through a common model structure.

---

## Supporting Architecture

Directory:

`architecture/`

Contains cross-volume architectural contracts:

- `framework_architecture.md`
- `continuous_discrete_contract.md`
- `energy_model_contract.md`
- `determinism_contract.md`
- `multiscale_contract.md`

These documents define interfaces and invariants that span multiple volumes.

---

## Specifications

Directory:

`specifications/`

Contains normative computational specifications:

- `ternary_state_specification.md`
- `transition_semantics.md`
- `neutral_routing_specification.md`
- `resonance_descriptor_specification.md`
- `energy_output_specification.md`
- `trace_specification.md`

Specifications translate formal definitions into explicit computational contracts.

---

## Validation

Directory:

`validation/`

Contains validation structures for the mathematical and computational architecture:

- `scientific_validation_plan.md`
- `mathematical_validation_plan.md`
- `numerical_validation_plan.md`
- `invariant_validation_plan.md`
- `reproducibility_plan.md`
- `flibe_validation_matrix.md`

Validation is separated by claim type so that mathematical consistency, numerical behavior, invariants, reproducibility, and reference-domain results can be evaluated under their corresponding criteria.

---

## References

Directory:

`references/`

Contains the scientific source layer:

- `primary_sources.md`
- `kuramoto_sakaguchi_sources.md`
- `equivariant_model_sources.md`
- `interatomic_potential_sources.md`
- `molecular_dynamics_sources.md`
- `flibe_sources.md`

Classical definitions, equations, established physical relations, and literature-derived parameters are linked to their corresponding sources through this layer.

Author-defined TR-EIF structures remain distinguishable from literature-derived structures.

---

## Core TR-EIF Architecture

The principal conceptual chain is:

`mathematical foundations`

`→ ternary resonance theory`

`→ equivariant interatomic framework`

`→ learning and optimization`

`→ molecular dynamics`

`→ multiscale materials modeling`

`→ FLiBe reference model`

Within the integrated computational architecture, a principal state-transformation chain is:

`atomic configuration`

`→ interaction topology`

`→ equivariant representation`

`→ resonance representation`

`→ ternary representation`

`→ interatomic output`

`→ dynamical evolution`

`→ multiscale observables`

The mappings between these layers are explicit components of the framework.

---

## Resonance State

TR-EIF represents resonance through a resonance-coordinate space:

`X_R`.

A resonance-coordinate mapping is written:

`P_R`.

For an admissible source state `x`, the resonance state is:

`r = P_R(x)`

with:

`r ∈ X_R`.

A model-defined resonance window is:

`W_R ⊂ X_R`

with boundary:

`∂W_R`.

The minimal resonance classification is:

`OUTSIDE`

`BOUNDARY`

`INSIDE`.

These classes are not identified automatically with ternary states.

In particular:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless an explicit model mapping defines that correspondence.

Resonance windows may depend on multiple coordinates, history, topology, scale, and hysteretic state.

---

## Continuous and Discrete State Separation

TR-EIF maintains explicit separation between continuous and discrete state spaces.

Examples of continuous quantities include:

- positions;
- velocities;
- phase coordinates;
- resonance coordinates;
- energy;
- force;
- stress;
- thermodynamic observables.

The ternary state belongs to the discrete set:

`T = {-1, 0, 1}`.

A continuous quantity becomes a ternary target only through an explicitly defined mapping.

A ternary target and an executed ternary state are distinct objects.

---

## Active Neutral State

The neutral state:

`0`

is structurally active.

Its possible roles include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

It is not intrinsically equivalent to:

- missing data;
- invalid state;
- absent signal;
- computational error;
- unavailable value.

This distinction is preserved throughout the documentation, schemas, implementation, and validation layers.

---

## Transition Semantics

For the balanced ternary kernel:

`-1/0/1`

direct opposite transitions are excluded.

The transition:

`-1 → 1`

must be decomposed as:

`-1 → 0 → 1`.

The transition:

`1 → -1`

must be decomposed as:

`1 → 0 → -1`.

The first and second legs are separate events.

Completion of the first leg does not automatically execute the second leg.

A model may retain the active neutral state for one or more admissible execution steps before a subsequent transition is authorized.

---

## Equivariance

Equivariance is treated as a mathematical transformation property.

For a transformation group `G`, an input space `X`, an output space `Y`, input action `ρ_X`, output action `ρ_Y`, and mapping:

`F: X → Y`

equivariance requires:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for admissible:

`g ∈ G`

and:

`x ∈ X`.

Invariant mappings are the special case in which the output action leaves the output unchanged under the relevant transformation.

Permutation behavior, translation behavior, and rotation behavior are specified independently where required.

---

## Energy, Force, and Stress

Energy, force, and stress are defined through the EIF model layer and its associated mathematical contracts.

Where a differentiable conservative scalar energy functional:

`E`

is defined over atomic coordinates, forces may be obtained from the corresponding coordinate gradient according to the selected model convention.

Stress requires its own geometric, boundary, and normalization conventions.

The framework does not identify ternary state, resonance classification, phase relation, energy, force, or stress with one another.

Their relationships exist only through explicitly defined mappings.

---

## Molecular Dynamics State

A molecular-dynamics realization may contain several coupled state components, including:

- atomic positions;
- velocities or momenta;
- species;
- simulation-cell state;
- interaction topology;
- resonance state;
- ternary state;
- routing state;
- thermostat state;
- barostat state;
- model memory.

Each state component is updated according to its own mathematical and computational contract.

---

## Multiscale State Transfer

TR-EIF treats scale transfer as a typed mapping problem.

A multiscale mapping must define:

- source state space;
- target state space;
- source observables;
- transferred quantities;
- aggregation or projection;
- information retained;
- information discarded;
- dimensional transformation;
- uncertainty representation;
- closure relation.

This prevents quantities defined at different scales from being combined without an explicit transformation.

---

## Provenance

TR-EIF uses the following provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

These classes identify the origin and evidentiary status of equations, parameters, mappings, computational results, fixtures, and framework-defined structures.

---

## Scientific Distinctions

The documentation preserves the following distinctions:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`

`resonance classification ≠ energy`

These distinctions define typed boundaries between mathematical objects and prevent unrelated quantities from being collapsed into a single interpretation.

---

## Numerical Realization

Numerical realization is treated separately from the mathematical model.

A numerical implementation must define the computational representation required by its algorithm, including where applicable:

- numerical precision;
- integration method;
- time-step convention;
- convergence criteria;
- tolerances;
- state-update order;
- periodic wrapping;
- neighbor-list update policy;
- deterministic ordering;
- random-state handling.

Numerical tolerance is not substituted for exact mathematical equality unless the relevant computational contract explicitly defines a tolerance-based comparison.

---

## Determinism

Deterministic execution requires explicit control of all result-affecting state and execution ordering relevant to the selected implementation.

The determinism layer covers:

- initial state;
- configuration;
- scheduler state;
- random state where applicable;
- operation ordering;
- serialization;
- replay artifacts.

Deterministic behavior is tested through dedicated validation and benchmark structures.

---

## Traceability

Important TR-EIF claims are structured for traceability through:

`claim`

`→ definition or source`

`→ mathematical or computational scope`

`→ implementation`

`→ observable or artifact`

`→ validation evidence`.

Implementation-specific mechanisms are traced to their executable source rather than inferred from filenames or descriptive metadata.

---

## FRP Executable Reference

The Fractal Resonance Processor (FRP) provides an executable reference architecture for selected Ternary Resonant computational mechanisms.

The relation is:

`TR-EIF formal architecture`

`→ FRP executable specialization/reference`.

FRP mechanisms used as TR-EIF implementation references are identified from executable artifacts and remain distinguishable from general TR-EIF definitions.

The reference includes implementations of mechanisms such as:

- balanced ternary `-1/0/1` execution;
- active neutral state;
- neutral-mediated opposite transitions;
- pending transition destinations;
- scheduler-controlled state evolution;
- nonlinear phase evolution;
- hierarchical phase coupling;
- retained frequency memory;
- phase-order observables;
- phase-derived ternary targets.

Implementation parameters remain associated with the corresponding executable realization.

---

## Repository Relationship

The documentation layer is connected to the remaining repository structure:

`docs/`

`→ src/tr_eif/`

`→ schemas/`

`→ tests/`

`→ examples/`

`→ benchmarks/`

`→ data/`

`→ scripts/`

`→ .github/workflows/`

The documentation defines the mathematical and computational contracts.

The source tree implements those contracts.

Schemas define machine-readable interfaces.

Tests verify computational properties.

Examples provide controlled realizations.

Benchmarks measure defined computational behaviors.

Reference data and fixtures provide controlled inputs.

Scripts provide repository-level validation and artifact-generation operations.

Workflows execute repository qualification procedures.

---

## Documentation Rule

Every TR-EIF document must preserve:

1. explicit mathematical typing;
2. defined domains and codomains;
3. dimensional consistency;
4. separation of continuous and discrete state;
5. separation of target and executed state;
6. separation of local and global observables;
7. explicit treatment of memory and history;
8. explicit symmetry actions for equivariance claims;
9. active-neutral `0` semantics;
10. neutral-mediated opposite ternary transitions;
11. separation of mathematical models from numerical realization;
12. traceable provenance;
13. compatibility with the integrated TR-EIF architecture.

The documentation therefore treats TR-EIF as one connected mathematical and computational framework while preserving the formal boundaries between its constituent state spaces, mappings, physical quantities, numerical realizations, and execution mechanisms.
