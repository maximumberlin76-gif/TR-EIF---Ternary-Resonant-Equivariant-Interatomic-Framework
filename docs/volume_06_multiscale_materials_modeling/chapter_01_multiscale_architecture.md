
# Multiscale Architecture

## 1. Scope and System Class

This chapter defines the multiscale architecture of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF), linking electronic-reference records, conservative interatomic models, atomistic trajectories, structural coarse-graining, mesoscale and continuum closures, and engineering boundary conditions.

The reference system class is an open nonlinear dissipative dynamical system. Its physical state may include three-dimensional atomic geometry, momentum, thermodynamic variables, boundary exchanges, continuous resonance dynamics, and separately scheduled balanced-ternary execution.

The framework organizes these quantities through typed state spaces and explicitly identified mappings. A material realization specifies the state domain, spatial and temporal scale, governing operators, units, parameter sources, numerical method, and recorded observables at each selected level.

## 2. Architectural Levels

A multiscale realization may organize its model levels as:

`electronic reference → TR-EIP interatomic representation → atomistic dynamics → structural coarse state → mesoscale closure → continuum closure → engineering boundary representation`.

| Level | State or representation | Executable interface |
| --- | --- | --- |
| Electronic reference | Atomic configuration, total energy, optional forces and stress | `ElectronicReferenceRecord` |
| Interatomic model | Geometry, interaction graph, features, conditioned scalar energy | `ReferenceEnergyModel` |
| Atomistic dynamics | Coordinates, velocities, masses, cell, trajectory | `MolecularDynamicsState`, `MolecularDynamicsTrajectory` |
| Structural coarse state | Partition, Cartesian centroids, coarse masses | `CoarseScaleState` |
| Mesoscale | Coarse state and explicitly named closure variables | `MesoscaleClosureRecord` |
| Continuum | Mesoscale record and continuum variables | `ContinuumClosureRecord` |
| Engineering | Continuum record and identified boundary conditions | `EngineeringBoundaryRecord` |

Transport-coefficient transfer, thermodynamic consistency, uncertainty propagation, continuous resonance, and ternary execution connect through separately defined mappings associated with these levels.

TR-EIP is the interatomic model family within TR-EIF: `TR-EIP ⊂ TR-EIF`. The atomistic and multiscale interfaces are framework-level components that can be coupled to a selected member of that family.

## 3. Scale State and Mapping Contract

Let `X_l` denote the admissible state space at scale index `l`, and let `C_l` denote the explicit context of a mapping between adjacent levels. A directed scale mapping is written:

`M_(l→l+1): X_l × C_l → X_(l+1)`.

A context identifies the source and target scales, variable meanings, domain, mapping algorithm, units, assumptions, and any external parameters that affect the result. A coupled chain is formed by composing compatible mappings in a declared order.

For a time-dependent realization, the multiscale state may be represented as:

`X_multi(t) = (X_0(t), X_1(t), ..., X_L(t); C_0(t), ..., C_(L-1)(t))`.

The selected temporal coupling defines when a source state is sampled and when a target state is recomputed. Mechanical timesteps, resonance integration steps, ternary execution opportunities, and coarse-scale update opportunities retain their individual indices.

## 4. Fine-to-Coarse Partition

For `N_f ≥ 1` fine entities, a partition maps each fine index to one coarse index:

`P: {0, ..., N_f - 1} → {0, ..., N_c - 1}`.

The executable `MultiscalePartition` stores this relation in `fine_to_coarse`. Its invariant requires every coarse index from `0` through `N_c - 1` to occur at least once, so `1 ≤ N_c ≤ N_f`.

For coarse entity `c`, define its ordered membership set:

`I_c = {i in {0, ..., N_f - 1} | P(i) = c}`.

The sets `I_c` form a disjoint partition of the fine index set. The interface exposes `fine_count`, `coarse_count`, `coarse_index_for`, `fine_indices_for`, `coarse_members`, and `is_identity`.

Partition indices identify structural membership. Physical phase, oscillator phase, chemical species, resonance descriptors, and retained ternary execution values are stored through their corresponding state types.

## 5. Additive Scalar and Mass Reduction

For a fine scalar `x_i` declared additive under the selected partition, define:

`X_c = sum_(i in I_c) x_i`.

`reduce_scalar_sum` implements this partition-local operation. For positive fine masses `m_i`, the mass reduction is:

`M_c = sum_(i in I_c) m_i`.

`reduce_masses` implements the mass operation and constructs positive finite coarse masses. The partition identity gives the exact mathematical relation:

`sum_c M_c = sum_i m_i`.

The executable tuple accumulation is deterministic for a fixed fine index ordering. Numerical conservation checks specify the floating-point summation method and comparison policy separately from exact partition membership.

## 6. Three-Dimensional Geometric Reduction

Let `r_i ∈ R^3` be fine Cartesian positions. For coarse entity `c`, the mass-weighted centroid is:

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

`mass_weighted_centroids` evaluates this expression componentwise. `build_coarse_scale_state` combines it with mass reduction to construct `CoarseScaleState(partition, positions, masses)`.

The resulting coarse state exposes `fine_count`, `coarse_count`, and `total_mass`. The coordinates are represented in the Cartesian frame supplied by the caller.

For periodic atomic trajectories, position reconstruction specifies the image history and unwrapped Cartesian positions used for centroid evaluation. A time-dependent cell also requires a declared reference frame and treatment of cell deformation.

## 7. Vector Reduction and Averaging

For a fine vector quantity `u_i ∈ R^3` declared additive, the partition-local sum is:

`U_c = sum_(i in I_c) u_i`.

`reduce_vector_sum` implements componentwise summation.

For a vector quantity defined by mass-weighted averaging, introduce:

`V_c = (1/M_c) sum_(i in I_c) m_i v_i`.

`mass_weighted_vector_average` evaluates this relation. The source variable's physical definition selects the corresponding reduction; for example, a total additive vector and a coarse average velocity carry different normalization contracts.

Under a common orthogonal spatial transformation `Q`, the vector operations obey their ordinary Cartesian transformation rules when the partition and scalar masses are retained.

## 8. E(3) Geometry Across Scales

For an orthogonal matrix `Q ∈ O(3)` and translation `b ∈ R^3`, the fine position transformation is:

`r_i' = Q r_i + b`.

For an unchanged membership partition and positive scalar masses, the coarse centroid obeys:

`R_c' = (1/M_c) sum_(i in I_c) m_i (Q r_i + b) = Q R_c + b`.

Likewise, mass-weighted averages of Cartesian vectors transform by `Q` when their fine vectors do. This supplies a geometric covariance condition for coarse representations assembled from an E(3)-transformed atomic configuration.

Scale-aware equivariant mappings declare how scalar, vector, and higher-order features transform, including the partition-selection rule when membership is computed from geometry.

## 9. Coarse-to-Fine Prolongation

For a coarse scalar `X_c`, the broadcast prolongation is:

`x_i^broadcast = X_(P(i))`.

For a coarse vector `V_c`, the corresponding operation is:

`v_i^broadcast = V_(P(i))`.

`prolong_scalar_broadcast` and `prolong_vector_broadcast` implement these operations with exact coarse-to-fine cardinality matching. The chosen prolongation defines the reconstructed fine representation and its meaning.

Reduction and prolongation are separately typed operators. For a selected source space, a reconstruction analysis records the information retained by the reduction and the residual between the original fine state and its prolonged coarse representation.

## 10. Partition Composition and Hierarchy

For consecutive partitions `P_0: I_0 → I_1` and `P_1: I_1 → I_2`, composition is:

`P_(0→2)(i) = P_1(P_0(i))`.

`compose_partitions` implements this mapping when the first coarse count equals the second fine count.

`MultiscaleHierarchy` stores a nonempty ordered tuple of adjacent compatible partitions. Its properties include `level_count`, `transition_count`, `finest_count`, `coarsest_count`, and `level_counts`. The `composed_partition` method returns a direct partition between selected hierarchy levels.

For `L` stored transitions, the hierarchy represents `L + 1` structural levels. This cardinality relation is checked exactly.

## 11. Coarse-State Hierarchy

`build_multiscale_state_hierarchy(positions, masses, hierarchy)` applies `build_coarse_scale_state` sequentially to each hierarchy transition.

For coarse level `l + 1`:

`M_c^(l+1) = sum_(i in I_c^(l)) M_i^l`.

`R_c^(l+1) = [sum_(i in I_c^(l)) M_i^l R_i^l] / M_c^(l+1)`.

`MultiscaleStateHierarchy` retains one `CoarseScaleState` for every transition, with its partition bound to the corresponding hierarchy entry. The generated states can be accessed by `state_at(level)` and `coarsest_state`.

This construction defines a reproducible structural hierarchy of masses and Cartesian positions, with each state linked to its source partition.

## 12. Electronic-Reference Boundary

An electronic-reference record binds one `AtomicConfiguration` to a finite scalar total energy, a `source_id`, and a `method_id`, with optional `ForceState` and `StressState` values.

`evaluate_electronic_reference(configuration, evaluator)` invokes a supplied provider and checks that its returned `ElectronicReferenceRecord` is bound to the input atomic configuration. When force data are supplied, their atom count matches the configuration atom count.

An electronic-to-interatomic mapping declares the source computational method, atomic configuration domain, observables, units, and procedure used to relate the reference record to the selected TR-EIP energy, force, and stress interfaces.

## 13. Interatomic and Atomistic Dynamics

The interatomic layer uses three-dimensional atomic geometry, directed interaction graphs, equivariant features, and retained ternary execution channels to evaluate a conditioned scalar energy.

For a differentiable energy branch, the conservative force relation is:

`F_i = -grad_(r_i) E_pot`.

The molecular-dynamics layer advances coordinates and velocities through the selected numerical integrator. A trajectory retains its mechanical state order, geometry and boundary conditions, and the corresponding force and energy evaluation configuration.

The scale-transfer schedule identifies the atomistic state or trajectory observable supplied to structural coarse-graining. An open-system realization additionally specifies mechanical, thermal, and material exchange through its declared boundary operators.

## 14. Mesoscale Closure

The mesoscale boundary receives a `CoarseScaleState` and an explicit collection of auxiliary variables. `MesoscaleClosureVariable` stores a named tuple of finite numeric values.

`MesoscaleClosureRecord` contains the coarse state, `closure_id`, `source_id`, `closure_variables`, and `auxiliary_variables`.

`evaluate_mesoscale_closure` calls a supplied provider and verifies correspondence between the returned record, input coarse state, and auxiliary variables. The selected provider defines its constitutive relation, history variables, physical parameters, and response observables.

## 15. Continuum Closure

`ContinuumClosureRecord` contains the upstream `MesoscaleClosureRecord`, `closure_id`, `source_id`, explicitly named `continuum_variables`, and caller-supplied `auxiliary_variables`.

`evaluate_continuum_closure` invokes the selected provider and verifies that the returned continuum record is associated with the supplied mesoscale closure and auxiliary collection.

A continuum realization supplies its constitutive fields, balance equations, spatial discretization, flux laws, boundary variables, and temporal update method through the selected provider and model configuration.

## 16. Transport-Coefficient Transfer

`TransportCoefficient` identifies a coefficient by `coefficient_id`, numerical `value`, `unit`, `scale_id`, `state_domain_id`, and `source_id`.

`TransportTransferContext` declares the target scale, `mapping_id`, `normalization_id`, and `assumptions_id`. The result type `TransportCoefficientTransferRecord` binds the source coefficient, target coefficient, and context.

`evaluate_transport_coefficient_transfer` calls the selected provider with its complete source and transfer context and checks that the returned record refers to those inputs. The provider defines any constitutive mapping, physical-state correspondence, normalization, unit conversion, and numerical uncertainty treatment used to compute the target.

## 17. Thermodynamic Consistency

`ThermodynamicVariable` associates a value and unit with a variable identifier, scale identifier, state-domain identifier, and source identifier.

`ThermodynamicConsistencyContext` identifies the relation, model, assumptions, and normalization. `evaluate_thermodynamic_consistency` applies a provided evaluator to source and target thermodynamic variable collections and returns `ThermodynamicConsistencyRecord`.

Its `is_consistent` field has Boolean validation semantics. Thermodynamic state quantities, consistency status, resonance descriptors, and balanced-ternary execution remain separately typed throughout the mapping.

## 18. Uncertainty Propagation

`UncertaintyMeasure` stores a quantity identifier, uncertainty value, unit, representation identifier, scale identifier, state-domain identifier, and source identifier.

`UncertaintyPropagationContext` declares the target scale, propagation rule, assumptions, correlation model, and normalization through its identifier fields. The resulting `UncertaintyPropagationRecord` binds its source measures, target measures, and context.

`evaluate_uncertainty_propagation` calls a supplied propagation provider. The uncertainty model defines correlation handling and the transformation used for each declared representation. Scale identities, units, and provenance remain available in the returned measures.

## 19. Engineering-Scale Boundary Mapping

`EngineeringBoundaryCondition` identifies the boundary, variable, condition, numerical values, unit, and provenance source.

`EngineeringBoundaryContext` carries `engineering_model_id`, `geometry_id`, `mapping_id`, and `assumptions_id`.

`evaluate_engineering_boundaries` binds a selected provider to a `ContinuumClosureRecord` and this context. The returned `EngineeringBoundaryRecord` stores the continuum input and the ordered collection of identified boundary conditions.

A material and device realization specifies its boundary-condition interpretation, engineering geometry, applied fluxes and loads, numerical scheme, and corresponding observable trace.

## 20. Continuous Resonance Across Scales

The atomistic resonance state evolves through continuous Kuramoto–Sakaguchi phase dynamics on a selected directed graph. A receiver-specific phase equation has the form:

`d theta_j / dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A scale-aware resonance mapping specifies its input phase state, graph and geometry context, descriptor space, reduction or reconstruction rule, and sampling instant. Phase-order and frequency-spread descriptors are continuous quantities, each with its own normalization and state domain.

A coupled scale-transfer trace records resonance integration steps and the particular descriptor values used for interatomic conditioning or execution requests.

## 21. Balanced-Ternary Execution Across Scales

The canonical executed state space is `-1/0/1`, with active neutral `0` supporting its defined functions of balancing, routing, damping, mediation, transition staging, retention, and controlled neutralization.

A fine-to-coarse ternary mapping is a separately defined operator with declared state semantics. The membership partition and continuous scalar reductions act on their corresponding structural and numeric types; execution states retain exact categorical values.

Committed opposite-polarity routes preserve their two-event structure:

`-1 → 0 → 1`.

`1 → 0 → -1`.

Pending destinations belong to `{-1, 1}` and accompany retained active neutral. Requests, pending destinations, holds, committed self-transitions, and executed states remain distinct fields at each level using this execution contract.

## 22. Cross-Scale Provenance and Reproducibility

A reproducible multiscale calculation records:

- the source and target model-scale identifiers and their state domains;
- the atomic configuration, mechanical time coordinate, and boundary history;
- electronic-reference source and method identifiers where used;
- fine-to-coarse membership, partitions, hierarchy levels, and canonical ordering;
- scalar and vector reduction operators, mass and position inputs, and cell-coordinate conventions;
- coarse-to-fine reconstruction operators and reconstruction observables;
- closure-provider identifiers, auxiliary variables, and declared constitutive contexts;
- transport mapping, units, thermodynamic relation, and normalization identifiers;
- uncertainty representation, correlation and propagation contexts;
- engineering boundary conditions, geometry, and provenance identifiers;
- resonance integration instants, descriptor states, ternary requests, and committed execution events;
- numerical method, spatial and temporal discretization, and predeclared tolerance policies.

Exact categorical and structural invariants are checked through exact comparison. Continuous physical quantities use the declared numerical operators, units, and tolerances.

## 23. Executable Reference Index

| Function | Repository path |
| --- | --- |
| Fine-to-coarse partition | `src/tr_eif/multiscale/partition.py` |
| Scalar and mass reduction | `src/tr_eif/multiscale/reduction.py` |
| Cartesian centroid | `src/tr_eif/multiscale/geometry.py` |
| Vector reduction and averaging | `src/tr_eif/multiscale/vector_reduction.py`, `src/tr_eif/multiscale/vector_average.py` |
| Scalar and vector prolongation | `src/tr_eif/multiscale/prolongation.py` |
| Partition composition and hierarchy | `src/tr_eif/multiscale/composition.py`, `src/tr_eif/multiscale/hierarchy.py` |
| Coarse-scale state hierarchy | `src/tr_eif/multiscale/state.py`, `src/tr_eif/multiscale/hierarchy_state.py` |
| Electronic-reference record | `src/tr_eif/multiscale/electronic_reference.py` |
| Mesoscale and continuum closures | `src/tr_eif/multiscale/mesoscale_closure.py`, `src/tr_eif/multiscale/continuum_closure.py` |
| Transport-coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Engineering boundaries | `src/tr_eif/multiscale/engineering_boundary.py` |
| Interatomic energy | `src/tr_eif/energy/model.py` |
| Molecular trajectory | `src/tr_eif/md/trajectory.py` |
| Resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| Ternary propagation | `src/tr_eif/md/ternary_propagation.py` |
| FLiBe structural hierarchy | `src/tr_eif/flibe/multiscale_coolant.py` |

## 24. Existing Test Interfaces

| Scope | Repository test path |
| --- | --- |
| Partition and composition invariants | `tests/invariants/test_multiscale_partition_invariants.py`, `tests/invariants/test_multiscale_partition_composition_invariants.py` |
| Coarse state and hierarchical state invariants | `tests/invariants/test_multiscale_state_invariants.py`, `tests/invariants/test_multiscale_hierarchy_state_invariants.py` |
| Multilevel transfers | `tests/integration/test_multiscale_hierarchy_transfer.py` |
| Electronic-reference provider | `tests/integration/test_multiscale_electronic_reference.py` |
| Mesoscale and continuum closures | `tests/integration/test_multiscale_mesoscale_closure.py`, `tests/integration/test_multiscale_continuum_closure.py` |
| Transport transfer and thermodynamic consistency | `tests/integration/test_multiscale_transport_transfer.py`, `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Uncertainty propagation and engineering boundaries | `tests/integration/test_multiscale_uncertainty_propagation.py`, `tests/integration/test_multiscale_engineering_boundary.py` |
| Cross-scale records and provider binding | `tests/integration/test_multiscale_cross_scale_validation.py` |
| FLiBe hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |

## 25. Volume Integration

Volume 06 links the state-space and mapping contracts of Volume 01, continuous resonance and active-ternary execution of Volume 02, equivariant interatomic modeling of Volume 03, and the molecular dynamics of Volume 05 through an explicit hierarchy of scale transformations.

The resulting data flow is:

`reference configuration → interatomic model → atomistic state and trajectory → declared partition → structural coarse state → mesoscale variables → continuum variables → engineering boundary state`.

Transport, thermodynamics, uncertainty, resonance, and ternary execution participate through individually identified operators and recorded coupling schedules. Every scale transition retains its source variables, target representation, parameter context, and provenance.
