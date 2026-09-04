# TR-EIF Documentation

## Ternary Resonant Equivariant Interatomic Framework

This directory contains the committed scientific and mathematical documentation of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

TR-EIF combines a Ternary Resonant layer with an Equivariant Interatomic Framework layer while preserving explicit boundaries between continuous dynamics, resonance descriptors, balanced ternary state semantics, interatomic representations, conservative observables, and computational execution.

## Current Documentation Tree

The committed documentation contains four volumes:

1. `volume_01_mathematical_foundations/`
2. `volume_02_ternary_resonance_theory/`
3. `volume_03_equivariant_interatomic_framework/`
4. `volume_04_learning_and_optimization/`

Only committed directories and files are represented in this index.

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

This volume defines notation, state spaces, mappings, invariants, lemmas, theorems, corollaries, and the mathematical dependency structure used by the subsequent volumes.

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

The balanced ternary state space is:

`T = {-1, 0, 1}`

The state `0` is active and may participate in balancing, routing, damping, mediation, transition staging, retention, and controlled neutralization.

Direct committed opposite-state transitions are excluded:

`-1 → 1`

`1 → -1`

Opposite-state transitions are neutral-mediated:

`-1 → 0 → 1`

`1 → 0 → -1`

Each leg is a separate state-transition event. Completion of the first leg does not automatically execute the second leg.

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

This volume defines atomic configuration spaces, interaction graphs, E(3) actions, invariant and equivariant representations, message passing, resonance and ternary conditioning interfaces, conservative energy, forces, stress, and the TR-EIP model family.

The model-family relation is:

`TR-EIP ⊂ TR-EIF`

TR-EIP is a model family defined within TR-EIF. It is not identified with the complete TR-EIF framework.

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

This volume defines the learning problem, training-data interfaces, loss functionals, energy-force-stress training, ternary and resonance regularization, equivariance constraints, uncertainty and domain-detection interfaces, and optimization semantics.

## Core Semantic Boundaries

The documentation preserves the following distinctions:

- resonance is not frequency equality;
- resonance is not synchronization;
- synchronization is not phase locking;
- phase locking is not resonance;
- coherence is not uniformity;
- coherence is not resonance;
- phase order is not complete coherence;
- `R(t) ≠ C(t)`;
- resonance-window crossing is not bifurcation;
- bifurcation is not a ternary transition;
- a ternary transition is not a structural transition;
- a structural transition is not a physical phase transition;
- oscillator phase is not physical phase of matter;
- phase coupling is not mechanical force;
- phase relation is not chemical bond;
- ternary state is not energy;
- ternary state is not force;
- resonance classification is not energy;
- validation status is not ternary state.

## Resonance Coordinates

TR-EIF uses a model-defined resonance-coordinate space `X_R`, a resonance-coordinate mapping `P_R`, and a resonance window `W_R ⊂ X_R` with boundary `∂W_R`.

For an admissible source state `x`:

`r = P_R(x)`

with:

`r ∈ X_R`

The minimal resonance-region classification is:

- `OUTSIDE`
- `BOUNDARY`
- `INSIDE`

These classes are not automatically identified with ternary states. In particular:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless an explicit model mapping defines that correspondence.

## Continuous and Discrete State Separation

Continuous quantities and ternary states belong to separate state spaces.

Examples of continuous quantities include positions, velocities, oscillator phases, resonance coordinates, energy, force, stress, and other explicitly defined observables.

A continuous quantity becomes a ternary target only through an explicit mapping.

A ternary target is distinct from an executed retained ternary state.

Pending routing state is distinct from active neutral state.

Missing data, invalid data, masking, padding, uncertainty, and abstention are not represented by the active ternary state `0` unless a separate explicit mapping is defined.

## Executable Package Boundary

The executable Python implementation is located under:

`src/tr_eif/`

Committed package layers include:

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

The implementation and the mathematical documentation are separate artifacts. Implementation interfaces must preserve the semantics established by the corresponding formal definitions and contracts.

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

Validation evidence is associated with the claim type being tested. Numerical success does not replace a mathematical proof, and a mathematical result does not by itself establish numerical accuracy, physical calibration, or empirical validation.

## Provenance Classes

TR-EIF uses the following provenance classes where provenance is represented explicitly:

- `PRIMARY_SOURCE`
- `DERIVED`
- `CALIBRATED`
- `AUTHOR_DEFINED`
- `BENCHMARK`
- `TEST_FIXTURE`
- `REQUIRES_SOURCE`
- `REQUIRES_TEST`

Literature-derived physical values require explicit source provenance. Test-fixture values are not physical reference values unless separately sourced and classified.
