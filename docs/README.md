# TR-EIF Documentation

## Ternary Resonant Equivariant Interatomic Framework

This directory contains the committed mathematical and scientific documentation of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

TR-EIF defines interfaces between:

- mathematical state spaces;
- resonance dynamics;
- balanced ternary dynamics;
- continuous-to-discrete mappings;
- equivariant interatomic representations;
- conservative energy interfaces;
- learning and optimization interfaces;
- executable reference layers;
- validation artifacts.

Continuous, resonance, ternary, interatomic, physical, numerical, and validation state spaces remain distinct unless an explicit mapping is defined.

## Current Documentation Structure

The committed documentation contains four volumes:

1. `volume_01_mathematical_foundations/`
2. `volume_02_ternary_resonance_theory/`
3. `volume_03_equivariant_interatomic_framework/`
4. `volume_04_learning_and_optimization/`

This index lists committed documentation directories and files.

## Volume 01 — Mathematical Foundations

Directory:

`volume_01_mathematical_foundations/`

Committed chapters:

1. `chapter_01_foundations.md`
2. `chapter_02_notation_and_definitions.md`
3. `chapter_03_axiomatic_system.md`
4. `chapter_04_state_spaces.md`
5. `chapter_05_mathematical_operators.md`
6. `chapter_06_mathematical_structures.md`
7. `chapter_07_mathematical_mappings.md`
8. `chapter_08_framework_invariants.md`
9. `chapter_09_fundamental_lemmas.md`
10. `chapter_10_fundamental_theorems.md`
11. `chapter_11_corollaries.md`
12. `chapter_12_volume_summary.md`

Volume 01 contains:

- foundational definitions;
- notation;
- state spaces;
- axiomatic statements;
- mathematical operators;
- mathematical structures;
- mappings;
- framework invariants;
- lemmas;
- theorems;
- corollaries;
- dependency relations between mathematical statements.

Definitions, assumptions, lemmas, theorems, proofs, and corollaries are represented as separate mathematical artifact classes.

## Volume 02 — Ternary Resonance Theory

Directory:

`volume_02_ternary_resonance_theory/`

Committed chapters:

1. `chapter_01_resonance_foundations.md`
2. `chapter_02_kuramoto_sakaguchi_formalism.md`
3. `chapter_03_synchronization_and_coherence.md`
4. `chapter_04_resonance_regime_transitions.md`
5. `chapter_05_continuous_to_ternary_mapping.md`
6. `chapter_06_active_neutral_state_dynamics.md`
7. `chapter_07_neutral_routing.md`
8. `chapter_08_coupled_continuous_discrete_dynamics.md`
9. `chapter_09_stability_and_boundedness.md`
10. `chapter_10_numerical_time_evolution.md`
11. `chapter_11_volume_summary.md`

Volume 02 contains formalisms for:

- resonance coordinates;
- resonance windows;
- coupled oscillator dynamics;
- Kuramoto dynamics;
- Kuramoto-Sakaguchi phase lag;
- synchronization;
- phase locking;
- coherence;
- phase order;
- regime transitions;
- stability;
- bifurcations;
- continuous descriptors;
- continuous-to-ternary target mappings;
- active neutral-state dynamics;
- neutral routing;
- coupled continuous-discrete evolution.

## Balanced Ternary State Space

The balanced ternary state space is:

`T = {-1, 0, 1}`

The state `0` is an active neutral state.

The active neutral state may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Direct committed opposite-state transitions are excluded:

`-1 → 1`

`1 → -1`

Opposite-state transitions are neutral-mediated:

`-1 → 0 → 1`

`1 → 0 → -1`

Each leg is a separate transition event.

Completion of the first leg does not automatically execute the second leg.

The intermediate neutral state may persist.

## Ternary Execution Boundary

TR-EIF distinguishes:

- requested ternary target;
- retained ternary state;
- pending target;
- transition route;
- executed state transition.

A requested target is not an executed retained state.

A pending target is not the active neutral state.

Missing data is not active neutral state `0`.

Invalid data is not active neutral state `0`.

Masking is not active neutral state `0`.

Padding is not active neutral state `0`.

NaN is not active neutral state `0`.

Uncertainty is not active neutral state `0`.

Abstention is not active neutral state `0`.

Any mapping between these categories and ternary states requires an explicit model definition.

## Resonance Coordinates

TR-EIF uses a model-defined resonance-coordinate space:

`X_R`

A resonance-coordinate mapping is represented by:

`P_R`

For an admissible source state `x`:

`r = P_R(x)`

with:

`r ∈ X_R`

A resonance window is represented as:

`W_R ⊂ X_R`

with boundary:

`∂W_R`

A resonance window may depend on the model, state variables, history, hysteresis, topology, scale, or other explicitly defined coordinates.

## Resonance Classification

A minimal resonance-region classification contains:

- `OUTSIDE`
- `BOUNDARY`
- `INSIDE`

These classification states are not automatically mapped to balanced ternary states.

In particular:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless an explicit mapping defines that correspondence.

## Resonance and Synchronization Distinctions

The documentation distinguishes:

- resonance from frequency equality;
- resonance from synchronization;
- synchronization from phase locking;
- phase locking from resonance;
- coherence from uniformity;
- coherence from resonance;
- phase order from complete coherence.

The phase-order quantity `R(t)` is not identified with a separately defined coherence quantity `C(t)`:

`R(t) ≠ C(t)`

A resonance-window crossing is not identified with a bifurcation.

A bifurcation is not identified with a ternary transition.

## Continuous and Discrete State Separation

Continuous quantities and balanced ternary states belong to separate state spaces.

Continuous quantities may include:

- positions;
- velocities;
- oscillator phases;
- oscillator frequencies;
- resonance coordinates;
- feature values;
- energy;
- force;
- stress;
- other explicitly defined observables.

A continuous quantity becomes a ternary target only through an explicit mapping.

The general boundary is:

`continuous state → descriptor → projection → ternary target → execution boundary → retained ternary state`

The stages in this chain are not interchangeable.

## Physical and Oscillator Phase Distinction

Oscillator phase is not identified with physical phase of matter.

Phase coupling is not identified with mechanical force.

Phase relation is not identified with chemical bond.

A structural transition is not identified with a physical phase transition.

A ternary transition is not identified with a structural transition.

## Volume 03 — Equivariant Interatomic Framework

Directory:

`volume_03_equivariant_interatomic_framework/`

Committed chapters:

1. `chapter_01_atomic_configuration_space.md`
2. `chapter_02_interaction_graphs.md`
3. `chapter_03_e3_group_actions.md`
4. `chapter_04_equivariant_representations.md`
5. `chapter_05_message_passing.md`
6. `chapter_06_resonance_parameterization.md`
7. `chapter_07_ternary_feature_channels.md`
8. `chapter_08_conservative_energy_functional.md`
9. `chapter_09_forces_and_stress.md`
10. `chapter_10_model_family_tr_eip.md`
11. `chapter_11_volume_summary.md`

Volume 03 contains definitions and interfaces for:

- atomic configuration spaces;
- interaction graphs;
- E(3) group actions;
- invariant representations;
- equivariant representations;
- scalar features;
- vector features;
- message passing;
- resonance-conditioned features;
- ternary-conditioned features;
- conservative energy;
- force interfaces;
- stress interfaces;
- TR-EIP model-family definitions.

## E(3) Boundary

Spatial transformations and ternary transformations belong to separate state spaces.

A spatial rotation is not a ternary polarity reversal.

Translation, rotation, reflection, and permutation behavior are defined through their corresponding mathematical actions.

An interaction-graph edge is not automatically a chemical bond.

## TR-EIP Model Family

TR-EIP is defined as a model family within TR-EIF.

The relation is:

`TR-EIP ⊂ TR-EIF`

TR-EIP and TR-EIF denote different levels of the framework hierarchy.

TR-EIF defines framework-level mathematical and computational interfaces.

TR-EIP denotes an interatomic model family defined within those interfaces.

## Conservative Energy Boundary

The conservative layer distinguishes:

- atomic energy contribution;
- total energy;
- invariant energy functional;
- force;
- stress;
- resonance state;
- ternary state.

Force is associated with the energy-gradient interface defined by the corresponding model contract.

Stress is associated with the strain-derivative interface defined by the corresponding model contract.

Ternary state is not energy.

Ternary state is not force.

Resonance classification is not energy.

## Volume 04 — Learning and Optimization

Directory:

`volume_04_learning_and_optimization/`

Committed chapters:

1. `chapter_01_learning_problem.md`
2. `chapter_02_training_data.md`
3. `chapter_03_loss_functionals.md`
4. `chapter_04_energy_force_stress_training.md`
5. `chapter_05_ternary_regularization.md`
6. `chapter_06_resonance_regularization.md`
7. `chapter_07_equivariance_constraints.md`
8. `chapter_08_uncertainty_and_domain_detection.md`
9. `chapter_09_optimization.md`
10. `chapter_10_summary.md`

Volume 04 contains interfaces for:

- learning problems;
- training data;
- loss functionals;
- energy training;
- force training;
- stress training;
- ternary regularization;
- resonance regularization;
- equivariance constraints;
- uncertainty;
- domain detection;
- optimization.

Training-stage transitions are not ternary-state transitions.

Classifier temperature is not thermodynamic temperature unless an explicit model definition establishes that correspondence.

Uncertainty status is not a balanced ternary state.

## Executable Package Boundary

The executable Python implementation is located under:

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

Mathematical documentation and executable implementation are separate artifact classes.

Executable interfaces implement specified mathematical and computational contracts.

## Molecular-Dynamics Boundary

The committed molecular-dynamics package is located under:

`src/tr_eif/md/`

Its current interfaces include:

- molecular-dynamics state;
- kinematics;
- dynamics;
- velocity-Verlet integration;
- execution;
- trajectories;
- molecular-dynamics observables;
- trajectory observables.

Molecular-dynamics time evolution and ternary-state evolution are separate operations.

Molecular-dynamics time evolution and resonance-state evolution are separate operations unless an explicit coupled operator is defined.

## Multiscale Boundary

The committed multiscale package is located under:

`src/tr_eif/multiscale/`

Its current interfaces include:

- fine-to-coarse partitions;
- additive reduction;
- mass-weighted Cartesian geometry;
- coarse-scale states;
- additive vector reduction;
- mass-weighted vector averages;
- prolongation;
- partition composition;
- multiscale hierarchies;
- hierarchy states.

A scale transition is not a ternary transition.

A scale transition is not a physical phase transition.

A coarse-scale index is not a ternary state.

Generic multiscale reduction does not numerically average ternary states.

Periodic image reconstruction is not hidden inside Cartesian centroid evaluation.

## FLiBe Domain Boundary

The committed FLiBe package is located under:

`src/tr_eif/flibe/`

Its current interfaces include:

- composition;
- species representation;
- FLiBe-domain configuration;
- formal ionic-charge bookkeeping;
- mass parameters;
- thermodynamic state;
- units;
- provenance;
- density models;
- graph-relative coordination;
- resonance parameterization;
- ternary-target interpretation;
- multiscale coolant-state mapping;
- package-level public imports.

The supported FLiBe species identifiers are:

- `Li`
- `Be`
- `F`

Formal ionic charge and balanced ternary state belong to separate domains.

Formal charge neutrality:

`Q = 0`

is not identified with active ternary neutral state:

`0 ∈ T`

Graph-relative coordination is defined from the supplied interaction graph.

Graph-relative coordination is not automatically identified with chemical bonding or an experimentally measured coordination number.

FLiBe resonance parameterization produces continuous phase-dynamics parameters.

Continuous phase-dynamics parameters are not balanced ternary states.

FLiBe ternary interpretation produces a requested ternary target.

A requested ternary target is not an executed retained ternary state.

## Observable and Trace Boundary

The committed observable package is located under:

`src/tr_eif/observables/`

Its current interfaces include:

- trace records;
- trace sequences;
- canonical serialization;
- JSON export;
- file export;
- replay comparison;
- replay execution.

Missing observables are represented separately from ternary state `0`.

A trace is an observable computational artifact.

A trace is not a mathematical proof.

## Validation Boundary

Repository tests are located under:

`tests/`

Committed validation groups include:

- `conservation/`
- `determinism/`
- `equivariance/`
- `integration/`
- `invariants/`
- `numerical/`

Validation status is not a ternary state.

A numerical test result is not a mathematical proof.

A mathematical proof is not a numerical validation result.

Numerical validation does not by itself define physical calibration.

Physical calibration does not by itself define a mathematical invariant.

## Provenance Classes

Where provenance is represented explicitly, TR-EIF uses:

- `PRIMARY_SOURCE`
- `DERIVED`
- `CALIBRATED`
- `AUTHOR_DEFINED`
- `BENCHMARK`
- `TEST_FIXTURE`
- `REQUIRES_SOURCE`
- `REQUIRES_TEST`

A `PRIMARY_SOURCE` physical parameter requires explicit source metadata under the implemented FLiBe provenance contract.

A `TEST_FIXTURE` value is a test value.

A provenance class is metadata.

A provenance class is not a balanced ternary state.

## Modeling Chain

The framework uses the following modeling sequence:

`system class → boundaries → state spaces → variables → transformations → invariants → model → numerical realization → observable trace → validation`

Each stage has a separately defined role.

Mappings between stages are explicit.

## Documentation Protocol

The documentation uses the following requirements:

- symbols are defined before formal use;
- domains and codomains are specified where required;
- definitions are distinguished from assumptions;
- lemmas are distinguished from theorems;
- theorems state their premises;
- proofs are distinguished from numerical tests;
- computational tests are distinguished from empirical data;
- physical parameters require explicit provenance where sourced physical values are used;
- author-defined structures are distinguished from sourced physical quantities;
- continuous and discrete state spaces are not identified without an explicit mapping;
- resonance classifications and ternary states are not identified without an explicit mapping;
- physical observables and ternary states are not identified;
- validation states and ternary states are not identified.
