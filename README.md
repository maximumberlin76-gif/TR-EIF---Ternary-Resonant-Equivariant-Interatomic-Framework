# TR-EIF

## Ternary Resonant Equivariant Interatomic Framework

TR-EIF is a mathematical and computational framework that defines interfaces between balanced ternary dynamics, resonance dynamics, equivariant interatomic representations, conservative observables, molecular dynamics, multiscale mappings, and domain-specific physical-model layers.

The framework separates continuous state spaces, resonance coordinates, resonance classifications, balanced ternary states, interatomic representations, physical observables, numerical execution states, and validation states.

## Balanced Ternary State Space

The balanced ternary state space is:

`T = {-1, 0, 1}`

The state `0` is an active neutral state.

Within the TR-EIF ternary semantics, active neutral `0` may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Direct committed transitions between opposite retained states are excluded:

`-1 → 1`

`1 → -1`

Opposite-state transitions are neutral-mediated:

`-1 → 0 → 1`

`1 → 0 → -1`

Each leg is a separate state-transition event.

Completion of the first leg does not automatically execute the second leg.

The neutral state may persist between the two legs.

A requested ternary target is distinct from an executed retained ternary state.

A pending target is distinct from active neutral state `0`.

Missing data, invalid data, masking, padding, NaN values, uncertainty, and abstention are not represented by ternary `0` unless an explicit mapping defines that representation.

## Continuous and Discrete Dynamics

TR-EIF separates continuous and discrete state spaces.

Continuous quantities may include:

- atomic positions;
- atomic velocities;
- oscillator phases;
- oscillator frequencies;
- resonance coordinates;
- scalar features;
- vector features;
- energy;
- force;
- stress;
- other explicitly defined observables.

A continuous quantity becomes a ternary target only through an explicit mapping.

The continuous-to-discrete chain is represented as:

`continuous state → descriptor → projection → ternary target → execution boundary → retained ternary state`

The target and executed retained state are separate objects.

A continuous threshold crossing is not identified with a bifurcation.

A bifurcation is not identified with a ternary transition.

A ternary transition is not identified with a structural transition.

A structural transition is not identified with a physical phase transition.

## Resonance Layer

TR-EIF distinguishes:

- resonance from frequency equality;
- resonance from synchronization;
- synchronization from phase locking;
- phase locking from resonance;
- coherence from uniformity;
- coherence from resonance;
- phase order from complete coherence.

The phase-order quantity `R(t)` is not identified with a separately defined coherence quantity `C(t)`:

`R(t) ≠ C(t)`

TR-EIF uses a model-defined resonance-coordinate space:

`X_R`

For an admissible source state `x`, a model-defined mapping `P_R` produces:

`r = P_R(x)`

with:

`r ∈ X_R`

A resonance window is represented as:

`W_R ⊂ X_R`

with boundary:

`∂W_R`

A minimal resonance-region classification contains:

- `OUTSIDE`
- `BOUNDARY`
- `INSIDE`

These classes are not automatically identified with balanced ternary states.

In particular:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless an explicit model mapping defines such correspondence.

## Oscillator Dynamics

The resonance implementation contains phase-dynamics interfaces based on coupled oscillator states and phase-dynamics parameters.

The mathematical documentation includes Kuramoto and Kuramoto-Sakaguchi formalisms.

Oscillator phase is not identified with the physical phase of matter.

Phase coupling is not identified with mechanical force.

Phase relation is not identified with chemical bond.

## Equivariant Interatomic Framework

The interatomic layer defines interfaces for:

- atomic configurations;
- interaction graphs;
- E(3) transformations;
- scalar features;
- polar vector features;
- equivariant message passing;
- feature updates;
- resonance conditioning;
- ternary conditioning;
- conservative energy;
- forces;
- stress.

Spatial transformations and ternary transformations belong to separate state spaces.

A spatial rotation is not a ternary polarity reversal.

An interaction-graph edge is not automatically a chemical bond.

## TR-EIP Model Family

TR-EIP is defined as a model family within TR-EIF.

The relation is:

`TR-EIP ⊂ TR-EIF`

TR-EIP and TR-EIF are not interchangeable identifiers.

TR-EIF defines the framework-level mathematical and computational interfaces.

TR-EIP denotes a concrete interatomic model family defined within those interfaces.

## Conservative Energy Boundary

The executable energy layer defines interfaces for:

- atomic energy contributions;
- total energy;
- invariant energy functionals;
- reference energy models;
- coordinate differentiation;
- force evaluation;
- strain differentiation;
- stress evaluation.

Force is derived from the energy gradient under the implemented differentiation contract.

Stress is derived from strain differentiation under the implemented stress convention.

Energy, force, stress, resonance state, resonance classification, and ternary state are separate quantities.

A ternary state is not energy.

A ternary state is not force.

A resonance classification is not energy.

## Molecular Dynamics Layer

The executable molecular-dynamics package is located under:

`src/tr_eif/md/`

The committed implementation includes interfaces for:

- molecular-dynamics state;
- kinematics;
- dynamics;
- velocity-Verlet integration;
- force-driven execution;
- trajectories;
- molecular-dynamics observables;
- trajectory observables.

The molecular-dynamics execution boundary keeps physical time integration separate from hidden resonance or ternary-state evolution.

Periodic atomic configurations are represented by the configuration and geometry layers.

## Multiscale Layer

The executable multiscale package is located under:

`src/tr_eif/multiscale/`

The committed implementation includes interfaces for:

- fine-to-coarse partitions;
- additive scalar reduction;
- mass-weighted Cartesian geometry;
- coarse-scale states;
- additive vector reduction;
- mass-weighted vector averages;
- prolongation;
- partition composition;
- multiscale hierarchies;
- multiscale hierarchy states.

A scale transition is not a ternary transition.

A scale transition is not a physical phase transition.

A coarse-scale index is not a ternary state.

Ternary states are not numerically averaged by the generic multiscale reduction layer.

Periodic image reconstruction is not hidden inside Cartesian centroid evaluation.

## FLiBe Domain Layer

The FLiBe domain package is located under:

`src/tr_eif/flibe/`

The committed package contains interfaces for:

- composition;
- species;
- FLiBe-domain atomic configuration;
- formal ionic-charge bookkeeping;
- mass parameters;
- thermodynamic state;
- units and provenance;
- density models;
- species-resolved graph coordination;
- resonance parameterization;
- ternary-target interpretation;
- multiscale coolant-state mapping;
- package-level public imports.

The supported species identifiers are:

- `Li`
- `Be`
- `F`

Formal ionic charge and balanced ternary state belong to separate domains.

Formal charge neutrality:

`Q = 0`

is not identified with active ternary neutral state:

`0 ∈ T`

Graph-relative coordination is defined from the supplied interaction graph.

Graph-relative coordination is not automatically identified with a chemical bond or an experimentally measured coordination number.

FLiBe resonance parameterization produces continuous phase-dynamics parameters.

Continuous phase-dynamics parameters are not ternary states.

FLiBe ternary interpretation produces a requested ternary target.

A requested ternary target is not an executed retained ternary state.

## Physical Parameter Provenance

Where physical-parameter provenance is represented explicitly, TR-EIF uses the following provenance classes:

- `PRIMARY_SOURCE`
- `DERIVED`
- `CALIBRATED`
- `AUTHOR_DEFINED`
- `BENCHMARK`
- `TEST_FIXTURE`
- `REQUIRES_SOURCE`
- `REQUIRES_TEST`

A value classified as `TEST_FIXTURE` is a test value.

A value classified as `PRIMARY_SOURCE` requires explicit source metadata in the implemented FLiBe parameter contract.

Provenance classes are metadata states.

They are not balanced ternary states.

## Trace and Replay Layer

The observable layer is located under:

`src/tr_eif/observables/`

The committed implementation includes:

- trace records;
- trace sequences;
- canonical serialization;
- JSON export;
- file export;
- replay comparison;
- replay execution.

Missing observables are represented separately from ternary state `0`.

Deterministic replay compares canonical serialized output.

## Mathematical Documentation

Documentation is located under:

`docs/`

The current committed documentation contains four volumes.

### Volume 01 — Mathematical Foundations

Directory:

`docs/volume_01_mathematical_foundations/`

The volume contains chapters covering:

- foundations;
- notation and definitions;
- axiomatic system;
- state spaces;
- mathematical operators;
- mathematical structures;
- mathematical mappings;
- framework invariants;
- fundamental lemmas;
- fundamental theorems;
- corollaries;
- volume summary.

### Volume 02 — Ternary Resonance Theory

Directory:

`docs/volume_02_ternary_resonance_theory/`

The volume contains chapters covering:

- resonance foundations;
- Kuramoto-Sakaguchi formalism;
- synchronization and coherence;
- resonance-regime transitions;
- continuous-to-ternary mapping;
- active neutral-state dynamics;
- neutral routing;
- coupled continuous-discrete dynamics;
- stability and boundedness;
- numerical time evolution;
- volume summary.

### Volume 03 — Equivariant Interatomic Framework

Directory:

`docs/volume_03_equivariant_interatomic_framework/`

The volume contains chapters covering:

- atomic configuration space;
- interaction graphs;
- E(3) group actions;
- equivariant representations;
- message passing;
- resonance parameterization;
- ternary feature channels;
- conservative energy functional;
- forces and stress;
- TR-EIP model family;
- volume summary.

### Volume 04 — Learning and Optimization

Directory:

`docs/volume_04_learning_and_optimization/`

The volume contains chapters covering:

- learning problem;
- training data;
- loss functionals;
- energy-force-stress training;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty and domain detection;
- optimization;
- summary.

The documentation index is:

[`docs/README.md`](docs/README.md)

## Python Package Structure

The executable Python package is located under:

`src/tr_eif/`

Committed package directories are:

- `configuration/`
- `energy/`
- `equivariant/`
- `flibe/`
- `geometry/`
- `graph/`
- `md/`
- `multiscale/`
- `observables/`
- `resonance/`
- `ternary/`

## Validation Structure

Repository tests are located under:

`tests/`

Committed validation groups include:

- `tests/conservation/`
- `tests/determinism/`
- `tests/equivariance/`
- `tests/integration/`
- `tests/invariants/`
- `tests/numerical/`

Validation status and balanced ternary state are separate domains.

A numerical test result is not a mathematical proof.

A mathematical proof is not a numerical validation result.

A numerical validation result does not by itself establish empirical calibration.

An empirical comparison does not by itself define a mathematical invariant.

## Modeling Chain

The framework uses the following modeling sequence:

`system class → boundaries → state spaces → variables → transformations → invariants → model → numerical realization → observable trace → validation`

Each stage has its own definitions, interfaces, and validation conditions.

## Scientific Protocol

Repository materials use the following requirements:

- symbols are defined before formal use;
- domains and codomains are specified where required by the formalism;
- definitions, lemmas, theorems, computational tests, and empirical data remain separate artifact classes;
- physical constants and empirical parameters require explicit provenance;
- author-defined structures are identified separately from sourced physical quantities;
- implementation interfaces preserve their declared mathematical semantics;
- validation evidence is associated with the corresponding claim type;
- continuous, resonance, ternary, equivariant, physical, multiscale, and validation state spaces are not identified without an explicit mapping.

## License

Licensed under the Apache License 2.0.

See [LICENSE](LICENSE).

## Author

Maksym Marnov (Alchimist)

Berlin, 04.08.2026
