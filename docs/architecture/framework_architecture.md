# TR-EIF Framework Architecture

## 1. Scope

This document defines the repository-level architectural contract of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The contract specifies:

- framework identity;
- architectural layers;
- state-space separation;
- mapping boundaries;
- dependency direction;
- balanced ternary semantics;
- resonance boundaries;
- equivariant interatomic boundaries;
- conservative energy boundaries;
- molecular-dynamics boundaries;
- multiscale boundaries;
- material-specialization boundaries;
- observable and trace boundaries;
- validation boundaries;
- provenance boundaries;
- determinism requirements;
- relationships between TR-EIF, TR-EIP, and external executable references.

This document does not replace the mathematical definitions contained in the numbered documentation volumes.

Where a mathematical object is defined in a numbered volume, the mathematical definition retains its declared domain, codomain, assumptions, invariants, and scope.

## 2. Framework Identity

TR-EIF denotes:

**Ternary Resonant Equivariant Interatomic Framework**

The framework contains two named formal components:

- `TR` — Ternary Resonant;
- `EIF` — Equivariant Interatomic Framework.

These components are represented as separately typed mathematical and computational layers.

Their integration occurs through explicit mappings and interfaces.

A shared numerical representation does not remove a semantic state-space boundary.

## 3. Model-Family Hierarchy

TR-EIP denotes a model family defined within TR-EIF.

The hierarchy is:

`TR-EIP ⊂ TR-EIF`

TR-EIP and TR-EIF are not interchangeable identifiers.

TR-EIF defines framework-level mathematical, computational, dynamical, validation, multiscale, and material-specialization interfaces.

TR-EIP denotes an equivariant interatomic model family defined within those interfaces.

The relation to FRP is:

`FRP ≠ TR-EIP`

FRP is not the definition of TR-EIF and is not the definition of TR-EIP.

Any correspondence between an FRP mechanism and a TR-EIF mechanism requires an explicitly declared interface or semantic correspondence.

## 4. Architectural Dependency Order

The framework uses the dependency order:

`system class`

`→ boundaries`

`→ state spaces`

`→ variables`

`→ transformations`

`→ invariants`

`→ mathematical model`

`→ numerical realization`

`→ observable trace`

`→ validation`

A later stage does not redefine an earlier stage without an explicit revision of the earlier contract.

A numerical implementation does not silently redefine a mathematical state space.

A validation result does not silently redefine a model invariant.

An observable trace does not silently redefine the state-transition semantics that generated it.

## 5. System Contract

A TR-EIF system may be represented abstractly as:

`S = (B, X, U, P, F, O, I)`

where:

- `B` is the system-boundary specification;
- `X` is the system state space;
- `U` is the admissible input space;
- `P` is the parameter space;
- `F` is the state-evolution structure;
- `O` is the observable structure;
- `I` is the invariant set or invariant-predicate family.

A concrete model may add explicitly declared components.

A component not declared inside the modeled system boundary remains external to the modeled system.

## 6. Composite State Architecture

TR-EIF does not use one universal state space for all quantities.

A model state may contain separately typed components including:

- continuous state;
- geometric state;
- graph state;
- circular phase state;
- resonance state;
- balanced ternary state;
- retained memory state;
- pending transition state;
- molecular-dynamics state;
- multiscale state;
- parameter state;
- observable state;
- provenance state;
- validation state.

A composite state may be represented by a Cartesian product of separately defined spaces.

The product construction does not imply semantic equivalence among its factors.

## 7. State-Type Separation

Semantic type is independent of machine storage type.

Two quantities represented by the same Python type, integer, floating-point value, tuple, array, or serialized field remain distinct when their declared mathematical roles differ.

The following distinctions are architectural constraints:

- oscillator phase is not physical phase of matter;
- resonance coordinate is not ternary state;
- resonance classification is not ternary state;
- phase order is not complete coherence;
- ternary state is not energy;
- ternary state is not force;
- formal ionic charge is not ternary state;
- validation status is not ternary state;
- uncertainty status is not ternary state;
- scale index is not ternary state;
- graph edge is not automatically a chemical bond;
- training-stage transition is not ternary-state transition.

Mappings between separately typed states require explicit definitions.

## 8. Balanced Ternary State Contract

The balanced ternary state space is:

`T = {-1, 0, 1}`

The state `0` is an active neutral state.

Active neutral `0` may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

The symbols `-1`, `0`, and `1` denote ternary states only when the corresponding variable is explicitly typed as a ternary state.

A numerical value equal to `-1`, `0`, or `1` in another state space does not acquire ternary semantics from numerical equality alone.

## 9. Opposite-State Transition Contract

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

are excluded.

Opposite-state transitions use neutral-mediated routes:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

Each leg is a separate transition event.

Completion of the first leg does not automatically execute the second leg.

The active neutral state may persist between the two legs.

The second leg remains subject to its declared execution conditions.

## 10. Requested and Executed Ternary States

The architecture distinguishes:

- continuous source state;
- ternary target;
- retained ternary state;
- pending target;
- transition route;
- execution guard;
- committed transition.

A requested ternary target is not an executed retained state.

A pending target is not the active neutral state.

A hold condition is not a committed self-transition unless the execution contract explicitly represents it as such.

Target generation and transition execution are separate operations.

## 11. Missing and Invalid Data Boundary

The following categories are not represented by active ternary neutral `0` by default:

- missing data;
- invalid data;
- NaN;
- masking;
- padding;
- uncertainty;
- abstention;
- unavailable observable;
- validation failure.

Any mapping from one of these categories into `T` requires an explicit mapping contract.

## 12. Continuous-State Boundary

Continuous quantities may include:

- atomic positions;
- velocities;
- oscillator phases;
- oscillator frequencies;
- resonance coordinates;
- thermodynamic variables;
- invariant features;
- equivariant features;
- energy;
- force;
- stress;
- other explicitly defined real-valued or vector-valued observables.

Continuous state and balanced ternary state remain separate state spaces.

## 13. Continuous-to-Discrete Boundary

A continuous quantity becomes a ternary target only through an explicit mapping.

The architectural sequence is:

`continuous state`

`→ continuous descriptor`

`→ projection or classifier`

`→ ternary target`

`→ ternary execution`

`→ retained ternary state`

The stages in this sequence are distinct.

A threshold crossing is a property of the declared projection or classifier.

A threshold crossing is not automatically a bifurcation.

A threshold crossing is not automatically a committed ternary transition.

## 14. Resonance Architecture

TR-EIF defines resonance through model-declared resonance coordinates and resonance criteria.

A resonance-coordinate space is represented by:

`X_R`

A resonance-coordinate mapping is represented by:

`P_R`

For an admissible source state `x`:

`r = P_R(x)`

with:

`r ∈ X_R`

A resonance window is represented by:

`W_R ⊂ X_R`

with boundary:

`∂W_R`

The resonance window may be:

- multidimensional;
- model-relative;
- history-dependent;
- hysteretic;
- topology-dependent;
- scale-dependent.

## 15. Resonance Classification Boundary

A minimal resonance-region classifier may contain:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`.

These classifier states are not automatically identified with:

`-1/0/1`

In particular:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless a model explicitly defines that mapping.

## 16. Resonance, Synchronization, and Coherence

TR-EIF preserves the distinctions:

- resonance is not frequency equality;
- resonance is not synchronization;
- synchronization is not phase locking;
- phase locking is not resonance;
- coherence is not uniformity;
- coherence is not resonance;
- phase order is not complete coherence.

The phase-order quantity:

`R(t)`

is not identified with a separately defined coherence quantity:

`C(t)`

Therefore:

`R(t) ≠ C(t)`

unless a specialized model explicitly defines a relation between them.

## 17. Bifurcation and Transition Boundary

The following events remain distinct:

- resonance-window crossing;
- bifurcation;
- ternary target change;
- ternary committed transition;
- structural transition;
- physical phase transition.

The relations:

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

are framework-level semantic boundaries.

## 18. Equivariant Interatomic Architecture

The interatomic architecture contains separately defined interfaces for:

- atomic configuration;
- interaction graph;
- geometric relations;
- E(3) actions;
- invariant representations;
- equivariant representations;
- message passing;
- resonance parameterization;
- ternary-conditioned features;
- conservative energy;
- forces;
- stress.

A concrete TR-EIP realization declares the components it implements.

## 19. Spatial Symmetry Boundary

Spatial transformations and ternary transformations belong to different state spaces.

Translation, rotation, reflection, and permutation behavior are defined through their corresponding mathematical actions.

A spatial rotation is not a ternary polarity reversal.

A spatial reflection is not a ternary polarity reversal.

A permutation of equivalent atomic indices is not a ternary-state transition.

## 20. Interaction-Graph Boundary

An interaction graph represents explicitly defined graph relations between modeled entities.

An interaction-graph edge is not automatically:

- a chemical bond;
- a mechanical constraint;
- a resonance relation;
- a ternary relation.

Such semantics require separately declared mappings or model definitions.

Graph construction and graph interpretation remain separate contracts.

## 21. Equivariant Representation Boundary

Invariant and equivariant feature channels have declared transformation behavior.

A scalar invariant channel and a polar vector channel are different representation types.

Transformation behavior is part of the feature definition.

Ternary conditioning does not redefine the spatial transformation type of a feature.

Resonance conditioning does not redefine the spatial transformation type of a feature.

## 22. Resonance-Conditioning Boundary

An interatomic representation may receive explicitly mapped resonance information.

The existence of resonance conditioning does not imply that:

- oscillator phase is atomic position;
- phase locking is chemical bonding;
- resonance coordinate is energy;
- resonance coordinate is force.

The conditioning mapping defines the interface between the resonance layer and the equivariant representation layer.

## 23. Ternary-Conditioning Boundary

Ternary-conditioned features use explicitly retained ternary state under their declared conditioning contract.

A target state and a retained state are not interchangeable at this boundary.

The neutral conditioning response is defined by the selected model and is not required to be numerically zero.

## 24. Conservative Energy Architecture

A conservative model defines a scalar energy through an explicit energy functional.

The energy layer is separate from:

- resonance classification;
- ternary classification;
- validation state;
- provenance state.

Energy is not inferred from ternary state alone.

Ternary state is not interpreted as an energy level unless a separate model explicitly defines such a quantity.

## 25. Force Boundary

Force is associated with the spatial derivative of the declared energy model under the selected differentiation contract.

The force interface does not identify:

- phase coupling with force;
- ternary state with force;
- graph connectivity with force.

The graph and feature structures used during differentiation are governed by their declared numerical contract.

## 26. Stress Boundary

Stress is associated with the declared strain-derivative contract.

The stress sign convention, strain construction, cell transformation, and numerical differentiation semantics belong to the selected stress model.

Stress is not a ternary state.

Stress is not a resonance classification.

## 27. Molecular-Dynamics Architecture

The molecular-dynamics layer contains state and execution interfaces for atomistic time evolution.

Molecular-dynamics state may contain:

- atomic configuration;
- velocities;
- masses;
- integration step;
- physical simulation time.

Molecular-dynamics time evolution is a separate operation from:

- resonance-state evolution;
- ternary-state evolution;
- scale transformation.

A coupled realization must define the order and interface of these operations explicitly.

## 28. Integration Boundary

A numerical integrator advances the variables declared within its integration contract.

An integrator does not implicitly update unrelated state spaces.

In particular, a molecular-dynamics integrator does not implicitly execute resonance or ternary updates unless such coupled behavior is explicitly defined.

## 29. Periodic Geometry Boundary

Periodic geometry is represented through explicit cell and periodicity information.

Minimum-image operations, periodic-image selection, coordinate wrapping, and coordinate unwrapping are separate geometric operations.

A Cartesian centroid operation does not implicitly perform periodic unwrapping.

## 30. Multiscale Architecture

The multiscale layer defines mappings between explicitly declared scales.

The multiscale architecture distinguishes:

- fine-scale state;
- scale mapping;
- coarse-scale entity;
- coarse-scale state;
- reduction;
- prolongation;
- hierarchy;
- cross-scale transfer.

Multiscale mapping is not message aggregation.

A coarse entity is not automatically an atom, cluster, resonance region, finite-volume cell, or continuum material point.

Its semantics are defined by the selected scale model.

## 31. Multiscale State Boundary

A scale index and a balanced ternary state belong to separate domains.

Numerical scale identifiers such as `0`, `1`, or other integers do not acquire ternary semantics.

Generic coarse-graining does not numerically average ternary states.

A scale transition is not a ternary transition.

A scale transition is not a physical phase transition.

## 32. Multiscale Geometry Boundary

Additive reduction and geometric averaging are separate operations.

Position is not an additive quantity under the generic reduction contract.

Mass-weighted Cartesian centroid construction is a separately defined operation.

Periodic-image reconstruction is not implicit in Cartesian centroid evaluation.

## 33. Material-Specialization Boundary

A material-specific package defines a specialization within the framework.

A material-specific specialization may define:

- species;
- composition;
- physical parameters;
- structural descriptors;
- reference data;
- thermodynamic variables;
- transport variables;
- resonance parameterization;
- ternary interpretation;
- molecular-dynamics interfaces;
- multiscale interfaces;
- validation data.

Material specialization does not redefine framework-wide state semantics unless an explicit framework revision is made.

## 34. FLiBe Specialization Boundary

The FLiBe package is a material-domain layer inside TR-EIF.

Its committed interfaces include:

- species;
- composition;
- configuration;
- formal ionic-charge bookkeeping;
- mass parameters;
- thermodynamic state;
- units and provenance;
- density models;
- graph-relative coordination;
- resonance parameterization;
- ternary-target interpretation;
- multiscale coolant-state mapping.

Formal ionic charge and balanced ternary state are separate domains.

Formal charge neutrality:

`Q = 0`

is not active ternary neutral state:

`0 ∈ T`

## 35. Provenance Architecture

Physical, empirical, calibrated, derived, benchmark, test, and author-defined values require explicit provenance classification where the corresponding layer implements provenance metadata.

The declared provenance classes are:

- `PRIMARY_SOURCE`;
- `DERIVED`;
- `CALIBRATED`;
- `AUTHOR_DEFINED`;
- `BENCHMARK`;
- `TEST_FIXTURE`;
- `REQUIRES_SOURCE`;
- `REQUIRES_TEST`.

A provenance class is metadata.

A provenance class is not a ternary state.

A `TEST_FIXTURE` value is not a physical reference value unless separately sourced and reclassified.

## 36. Observable Architecture

An observable is produced from a declared model state through an explicit observable mapping.

State and observable remain distinct.

Examples of observables include:

- energy;
- force;
- stress;
- phase-order quantity;
- trajectory-derived quantities;
- trace records.

An observable value does not automatically become a state variable.

## 37. Trace Architecture

A trace is a computational artifact representing selected observable and execution data.

Trace generation does not redefine the state-transition contract.

Missing trace observables are represented separately from active ternary neutral state `0`.

Serialization semantics are separate from physical and mathematical semantics.

## 38. Determinism Boundary

For a deterministic execution path, identical admissible inputs and identical declared parameters must produce identical outputs under the same declared numerical and serialization contract.

Sources of nondeterminism must be explicit when present.

Deterministic replay is evaluated against the declared replay representation.

A deterministic trace does not establish physical validity by itself.

A physically calibrated model does not establish deterministic execution by itself.

These are separate validation properties.

## 39. Validation Architecture

Validation artifacts are associated with the claim or invariant they test.

Validation classes may include:

- mathematical consistency;
- invariant preservation;
- unit tests;
- integration tests;
- determinism tests;
- equivariance tests;
- conservation tests;
- numerical tests;
- schema tests;
- benchmark tests;
- empirical comparisons.

A passing computational test is not a mathematical proof.

A mathematical proof is not a computational test result.

A computational validation result is not automatically an empirical validation result.

A validation status is not a ternary state.

## 40. Documentation and Implementation Boundary

Mathematical documentation and executable implementation are separate artifact classes.

Documentation defines mathematical objects, assumptions, contracts, and semantic boundaries.

Executable modules provide numerical realizations of declared interfaces.

An implementation-specific storage representation does not silently alter the corresponding mathematical definition.

An implementation-specific optimization does not remove a declared semantic boundary.

## 41. Contract Consistency

Repository layers must preserve declared framework invariants within their stated scope.

A specialized layer may introduce additional restrictions.

A specialized layer may not silently weaken a framework-wide invariant.

When two contracts operate at different scopes, both scopes must be stated.

A local implementation rule is not automatically a framework-wide law.

A framework-wide invariant applies to every layer within its declared scope.

## 42. Dependency Direction

Architectural dependencies follow declared interfaces.

A downstream layer may consume outputs of an upstream layer.

A downstream layer does not redefine the upstream state semantics by consumption alone.

The following distinctions remain explicit across dependency boundaries:

- source state versus descriptor;
- descriptor versus classification;
- classification versus target;
- target versus execution;
- execution versus retained state;
- retained state versus observable;
- observable versus validation state.

## 43. Modeling Chain

The framework-level modeling chain is:

`system class → boundaries → state spaces → variables → transformations → invariants → model → numerical realization → observable trace → validation`

Each stage has a separately declared role.

Mappings between stages are explicit.

## 44. Existing Formal Documentation

The mathematical definitions associated with this architecture are contained in:

- `docs/volume_01_mathematical_foundations/`;
- `docs/volume_02_ternary_resonance_theory/`;
- `docs/volume_03_equivariant_interatomic_framework/`;
- `docs/volume_04_learning_and_optimization/`.

The documentation index is:

`docs/README.md`

## 45. Current Executable Layers

The committed executable implementation is located under:

`src/tr_eif/`

Current package layers include:

- `configuration/`;
- `energy/`;
- `equivariant/`;
- `flibe/`;
- `geometry/`;
- `graph/`;
- `md/`;
- `multiscale/`;
- `observables/`;
- `resonance/`;
- `ternary/`.

The existence of an executable package does not imply completion of every framework-level specialization or validation category.

## 46. Architectural Invariants

The architectural contract preserves the following relations:

`TR-EIP ⊂ TR-EIF`

`FRP ≠ TR-EIP`

`T = {-1, 0, 1}`

`-1 → 1` is not a direct committed transition.

`1 → -1` is not a direct committed transition.

Opposite committed transitions are neutral-mediated.

`target ≠ executed retained state`

`pending target ≠ active neutral state`

`R(t) ≠ C(t)`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`

`ternary state ≠ force`

`formal charge neutrality ≠ active ternary neutral state`

`validation status ≠ ternary state`

`scale transition ≠ ternary transition`

`scale transition ≠ physical phase transition`

These relations remain in force unless an explicit framework revision changes the corresponding definition.
