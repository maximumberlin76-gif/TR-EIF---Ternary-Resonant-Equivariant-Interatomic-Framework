
# Volume 06 — Multiscale Materials Modeling: Summary

## 1. Scope and System Class

Volume 06 defines the multiscale mappings of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF), from electronic-reference configurations and interatomic computations through atomistic trajectories, structural coarse states, mesoscale and continuum representations, and engineering boundary conditions.

The represented system class is an open nonlinear dissipative dynamical system with three-dimensional geometry, continuous state evolution, physical exchange, continuous resonance variables, and separately scheduled balanced-ternary execution `-1/0/1`.

A multiscale realization selects the physical state domain, scale hierarchy, mapping operators, units, boundary conditions, constitutive parameters, time coordinates, numerical methods, and provenance for each represented level.

The principal structural chain is:

`electronic reference → TR-EIP interatomic model → atomistic state and trajectory → partitioned coarse state → mesoscale closure → continuum closure → engineering boundary record`.

Transport coefficients, thermodynamic relations, uncertainty measures, resonance descriptors, and ternary execution events connect to this chain through their separately defined interfaces.

## 2. Chapter Register

| Chapter | Subject | Principal computational or mathematical contract |
| --- | --- | --- |
| 01 — Multiscale Architecture | Levels, partitions, and mapping contexts | Typed state domains, fine/coarse correspondence, scale hierarchy |
| 02 — Electronic-to-Interatomic Mapping | Electronic-reference observables and conservative TR-EIP | Configuration binding, energy, force, stress, provenance |
| 03 — Atomistic-to-Mesoscale Mapping | Structural coarse-graining | Mass and vector reduction, centroids, reconstruction, hierarchy |
| 04 — Continuum Closure | Mesoscale-to-continuum representation | Named fields, provider binding, balance and constitutive operators |
| 05 — Uncertainty Transfer | Propagation across scale mappings | Typed uncertainty measures, covariance, correlation context |
| 06 — Thermodynamic Consistency | State correspondence and thermodynamic balances | Typed variables, relation context, consistency record |
| 07 — Transport Coefficient Transfer | Microscopic-to-macroscopic transport mapping | Typed coefficients, physical state domains, transfer context |
| 08 — Engineering Scale Models | Continuum-to-engineering boundary mapping | Boundary identities, geometry, flux and load conditions |
| 09 — Volume Summary | Integration of Volume 06 | Mapping composition, invariants, event order, reproducibility |

The preceding chapters define the individual operators and their mathematical and numerical contexts. This chapter specifies their composition in a common multiscale record.

## 3. State Hierarchy and Mapping Composition

Let `X_l` be the admissible state space at scale `l`, with an explicitly identified mapping context `C_(l→m)`. A scale transformation is represented by:

`M_(l→m): X_l × C_(l→m) → X_m`.

For compatible mappings over scales `l`, `m`, and `n`, define their composition as:

`M_(l→n) = M_(m→n) ◦ M_(l→m)`.

The composed mapping uses the corresponding ordered contexts and source/target state identities. A complete trace associates every state with its scale identifier, physical domain, sampling time, coordinate frame, units, source, and governing operator.

The executable multiscale package provides structural reductions and typed records for electronic, mesoscopic, continuum, and engineering levels. The selected providers define the constitutive transformations and numeric values attached to those records.

## 4. Electronic-Reference Boundary

For `N >= 1` atoms, let an atomic configuration contain species `S`, Cartesian positions `R`, optional cell `B`, and periodic flags `P`:

`X_atom = (S, R, B, P)`.

`ElectronicReferenceRecord` binds this configuration to a finite total energy, a source identifier, a method identifier, and optional `ForceState` and `StressState` records.

`evaluate_electronic_reference(configuration, evaluator)` supplies the configuration to a callable provider and verifies the configuration correspondence of the returned record.

A source dataset registers the electronic method, composition, units, periodicity, numerical parameters, energy convention, and observable availability. These fields provide the mapping context for corresponding interatomic energy, force, and stress evaluations.

## 5. Conservative Interatomic Mapping

A selected TR-EIP model evaluates scalar energy from atomistic geometry, an interaction graph, features, model parameters, and a retained ternary execution vector:

`E_pot = E_Theta(R, G, Q_features, sigma)`.

For a differentiable coordinate branch with declared conditioning inputs held fixed:

`F_i = -grad_(r_i) E_pot`.

With a declared homogeneous strain parameter `epsilon` and reference cell volume `V_0`, an energy-derived stress component is associated with the corresponding strain derivative under the selected sign and component convention.

The executable reference provides `ReferenceEnergyModel`, `ConservativeForceEvaluator`, and `ConservativeStressEvaluator`. The differentiation operators use declared coordinate or strain perturbations and retain their supplied graph and conditioning inputs during each derivative evaluation.

`TR-EIP ⊂ TR-EIF`: the interatomic potential family supplies one modeled level within the broader multiscale framework.

## 6. Atomistic Dynamics and Sampling

For atom `i`, three-dimensional mechanical evolution has the form:

`d r_i/dt = v_i`.

`m_i d v_i/dt = F_i`.

The molecular-dynamics reference supplies velocity-Verlet integration, kinetic and potential energy observables, and trajectory records. Thermal, pressure, resonance, and ternary operators are composed at declared sampling and event instants.

A fine-to-coarse mapping identifies the source trajectory states, physical time range, atom ordering, cell and periodic-image conventions, and observables used to construct the target representation.

## 7. Fine-to-Coarse Membership and Conservation

Let `p(i)` assign fine entity `i` to coarse group `c`. Each fine entity has one assigned coarse identifier, and each coarse group has a nonempty member set:

`I_c = {i | p(i) = c}`.

For positive fine masses `m_i` and Cartesian positions `r_i`, define:

`M_c = sum_(i in I_c) m_i`.

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

For fine velocities `v_i`, define coarse momentum and mass-weighted velocity:

`P_c = sum_(i in I_c) m_i v_i`.

`V_c = P_c / M_c`.

The corresponding partition identities are:

`sum_c M_c = sum_i m_i`.

`sum_c P_c = sum_i m_i v_i`.

`MultiscalePartition`, `reduce_masses`, `mass_weighted_centroids`, and `mass_weighted_vector_average` implement the associated structural and numerical operations. Integer membership invariants use exact comparison; floating-point reductions use their declared evaluation and tolerance policy.

## 8. Internal Motion and Reconstruction

For coarse group `c`, define internal velocity deviations `w_i = v_i - V_c`. The kinetic-energy decomposition is:

`(1/2) sum_(i in I_c) m_i |v_i|^2 = (1/2) M_c |V_c|^2 + (1/2) sum_(i in I_c) m_i |w_i|^2`.

The group centroid and mean velocity represent resolved motion, while the internal term provides a separate quantity for a selected coarse constitutive state.

Scalar and vector broadcast prolongation are defined by:

`a_i,reconstructed = A_(p(i))`.

`u_i,reconstructed = U_(p(i))`.

`prolong_scalar_broadcast` and `prolong_vector_broadcast` implement these reconstructions. A reconstruction record identifies the source coarse quantity, its normalization, and the comparison observable used at the fine scale.

## 9. Hierarchical Scale Composition

For compatible consecutive partitions `p_0` and `p_1`, composition is:

`p_(0→2)(i) = p_1(p_0(i))`.

`compose_partitions` and `MultiscaleHierarchy` construct and retain these mappings. For `L` adjacent partition transitions, the hierarchy contains `L + 1` structural levels.

`build_multiscale_state_hierarchy` evaluates mass and centroid reductions at each declared transition and stores ordered coarse states. Hierarchical replay records every partition, level cardinality, intermediate state, and accumulation convention.

## 10. Three-Dimensional Covariance

For an orthogonal transformation `Q in O(3)` and translation `b in R^3`:

`r_i' = Q r_i + b`.

With fixed partition membership and scalar masses:

`R_c' = Q R_c + b`.

`V_c' = Q V_c`.

A Cartesian covariance tensor transforms as:

`C' = Q C Q^T`.

A scale mapping declares the corresponding actions on scalar, polar-vector, axial-vector, and higher-order tensor variables. For periodic configurations, cell geometry, unwrapped coordinate histories, and selected image conventions accompany the source and target geometric states.

## 11. Mesoscale Closure Record

`MesoscaleClosureRecord` binds a `CoarseScaleState` to a closure identifier, source identifier, named output variables, and optional auxiliary inputs.

The executable call is:

`evaluate_mesoscale_closure(state, evaluator, auxiliary_variables=())`.

`MesoscaleClosureVariable` stores a normalized nonempty name and nonempty finite numeric tuple. Output and auxiliary collections are canonically ordered and validated by their separate collection contracts.

The selected provider defines the coarse constitutive equations, physical units, history variables, and numerical evolution. The resulting record retains its exact source coarse state and auxiliary-variable association.

## 12. Continuum Closure and Balance Laws

`ContinuumClosureRecord` binds a `MesoscaleClosureRecord` to a closure identifier, source identifier, named continuum variables, and auxiliary variables.

The executable call is:

`evaluate_continuum_closure(mesoscale, evaluator, auxiliary_variables=())`.

For a conserved density `a`, flux `J_a`, and volumetric source `s_a` on a fixed domain, the local balance is:

`partial_t a + div(J_a) = s_a`.

For a fixed control volume `Omega` with outward normal `n`:

`d/dt integral_Omega a dV = -integral_(partial Omega) J_a · n dA + integral_Omega s_a dV`.

A continuum provider identifies the constitutive flux, source definition, spatial representation, boundary conditions, and temporal discretization used in its evaluation.

## 13. Open-System Exchange and Dissipation

A multiscale system boundary specifies the exchange of mass, momentum, energy, entropy, and transported species through selected surfaces and internal sources.

For mass density `rho` and barycentric velocity `u`, a source-inclusive local balance is:

`partial_t rho + div(rho u) = s_m`.

For an entropy density `rho s`, nonconvective entropy flux `J_s`, external supply `s_s,ext`, and internal production `sigma_s`:

`partial_t(rho s) + div(rho s u + J_s) = s_s,ext + sigma_s`.

For a continuum constitutive realization subject to the local second-law condition, internal entropy production satisfies:

`sigma_s >= 0`.

A coupled calculation records source and target storage, surface-flux orientation, volumetric sources, dissipative terms, and the state and time domain used for the balance comparison.

## 14. Uncertainty Propagation

`UncertaintyMeasure` identifies a quantity, finite nonnegative uncertainty magnitude, unit, representation, scale, state domain, and source. `UncertaintyPropagationContext` identifies the target scale, propagation method, assumptions, correlation model, and normalization.

The executable boundary is:

`evaluate_uncertainty_propagation(source_measures, context, evaluator)`.

For a differentiable mapping `y = f(x)` with source covariance matrix `C_x` and Jacobian `J`, a first-order covariance propagation is:

`C_y ≈ J C_x J^T`.

An ensemble procedure, interval operator, or other registered representation follows its own declared propagation rule. `UncertaintyPropagationRecord` retains ordered source and target measures together with the selected context.

The propagation representation and numeric uncertainty are associated with the selected observable, while categorical execution values remain recorded in the execution state space.

## 15. Thermodynamic Consistency

`ThermodynamicVariable` stores a finite value with unit, scale, state domain, and source identifiers. `ThermodynamicConsistencyContext` identifies the selected relation, model, assumptions, and normalization.

`evaluate_thermodynamic_consistency(source_variables, target_variables, context, evaluator)` returns a record binding the canonical source and target variable collections to the context, Boolean evaluation result, and validation identifier.

For a simple compressible multicomponent equilibrium system under its declared assumptions, a fundamental relation is:

`dU = T dS - P dV + sum_s mu_s dN_s`.

A state-matched cross-scale relation may be expressed through an explicitly selected residual:

`r_a = a_target - M_a(a_source; context)`.

Thermodynamic state definitions, units, derivatives, exchange contributions, numerical criteria, and source provenance are supplied with the selected relation.

## 16. Transport Coefficient Transfer

`TransportCoefficient` stores coefficient identity, finite value, unit, scale, state domain, and source. `TransportTransferContext` stores the destination scale, mapping, normalization, and assumptions identifiers.

The executable call is:

`evaluate_transport_coefficient_transfer(source, context, evaluator)`.

The resulting `TransportCoefficientTransferRecord` preserves the source coefficient, destination coefficient, and exact transfer context. Its structural identity contract includes:

`target.coefficient_id = source.coefficient_id`.

`target.scale_id = context.target_scale_id`.

For stationary isotropic three-dimensional self-diffusion under the corresponding statistical assumptions, microscopic estimators can use:

`D_self = lim_(tau→infinity) MSD(tau) / (6 tau)`.

`D_self = (1/3) integral_(0→infinity) C_v(tau) d tau`.

The MD reference stores single-origin MSD and VACF series. A coefficient estimation procedure identifies the particle selection, time origins, integration or fitting interval, trajectory ensemble, periodic-coordinate treatment, and statistical uncertainty. The coefficient transfer then associates that source value with its target scale and constitutive context.

## 17. Engineering Geometry and Boundary Records

`EngineeringBoundaryCondition` stores normalized boundary, variable, and condition identifiers, finite numeric values, unit, and source. `EngineeringBoundaryContext` binds the selected engineering model, geometry, mapping, and assumptions identifiers.

The executable evaluation is:

`evaluate_engineering_boundaries(continuum, context, evaluator)`.

`EngineeringBoundaryRecord` retains the exact continuum input, canonical ordered boundary conditions, and the engineering context.

For a boundary segment `Gamma_b` with outward unit normal `n_b`, representative laws include:

`a|_(Gamma_b) = a_D`.

`J_a · n_b = j_N`.

`t_b = sigma n_b`.

The provider maps each identified condition to its spatial support, physical law, source quantities, numerical values, units, and sampling instant. Flux and load histories enter the corresponding open-system balance records.

## 18. Continuous Resonance and Scale Mapping

The continuous resonance layer evolves oscillator phases through the selected directed Kuramoto–Sakaguchi dynamics:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A cross-scale resonance mapping identifies the input oscillator state, graph and geometry, continuous descriptor, partition or averaging operator, target physical domain, and temporal sampling instant.

Phase order, local relations, resonance-window variables, and continuum material fields retain their specified mathematical definitions. A mapped descriptor is registered with the source phase state, selected transform, target scale, and conditioning or closure input it supplies.

## 19. Active Balanced-Ternary Execution

The execution state alphabet is `-1/0/1`, with active neutral `0` supporting routing, balancing, damping, mediation, transition staging, retention, and controlled neutralization through defined operators.

For execution node `i`, let `sigma_i` be the retained state and `p_i` its optional pending destination:

`sigma_i in {-1, 0, 1}`.

`p_i in {-1, 1} or None`.

`p_i != None implies sigma_i = 0`.

Opposite-polarity routes consist of distinct committed events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

A scale-aware execution mapping identifies its node association, request rule, guard, retained state, pending destination, and committed event order. Coarse physical quantities remain numerical variables, while the selected execution map retains its exact categorical semantics.

## 20. Coupled Temporal Schedule

Let `n` index mechanical steps, `j` continuous resonance steps, `k` ternary execution opportunities, and `l` a selected cross-scale update. A composed calculation declares an operator schedule such as:

`X_MD[n+1] = Phi_MD(X_MD[n]; dt_MD, sigma[k])`.

`X_R[j+1] = Phi_R(X_R[j]; dt_R, G_sample)`.

`request[k] = M_request(X_MD, X_R, context)`.

`X_T[k+1] = U_exec(X_T[k], request[k], guards[k])`.

`X_coarse[l+1] = M_coarse(X_MD, partition, context)`.

`X_continuum[l+1] = M_continuum(X_meso, context)`.

The actual order, sampling locations, times, graph updates, parameterizations, boundary events, and state retention are recorded for the particular realization. The named equations identify separate callable roles; the coupling schedule supplies their composition.

## 21. FLiBe Material-State Registration

The FLiBe reference level associates species and composition, atomic configuration, thermal and pressure state, local structure, resonance descriptors, ternary interpretation, interatomic model, atomistic trajectory, and multiscale coolant representation.

`FLiBeMultiscaleCoolantModel` provides a structural fine-to-coarse hierarchy with an explicit selected Cartesian-position representation. Its result can be associated with mesoscale and continuum providers through the typed multiscale interfaces.

Registered source descriptions distinguish exact formula-unit `2 LiF : 1 BeF2`, nominal `67 mol% LiF : 33 mol% BeF2`, and measured specimen composition. The Vidrio 2022 experimental density record and Baral 2021 AIMD density record retain their source-specific composition, temperature, method, and available state metadata.

Source measurements, first-principles outputs, interatomic calculations, and scale-transferred coefficients have explicit observable and provenance identifiers. Material comparisons use the declared source-to-target state mapping and numerical method.

## 22. Structural and Mathematical Invariants

The cross-scale executable contracts include:

- complete fine-index assignment and canonical coarse-group identifiers;
- positive finite fine and coarse masses and three-component finite Cartesian positions;
- mass and momentum reduction relations under the selected partition;
- matching cardinalities across adjacent partition and hierarchy levels;
- exact composition of integer partition assignments;
- canonical unique names and typed values in mesoscale and continuum variable collections;
- source, target, and context correspondence in typed provider records;
- consistent target-scale identity in transport and uncertainty transfer records;
- canonical unique keys for engineering boundary conditions;
- exact ternary state, pending-route, guard, and committed-event semantics;
- separately recorded physical times and numerical event indices.

Numerical qualification applies declared methods and tolerances to geometric covariance, mass and momentum reductions, energy and exchange balances, thermodynamic identities, transport calculations, uncertainty propagation, and mesh or timestep refinement. Exact categorical and structural fields use exact equality.

## 23. Provenance and Reproducibility

A reproducible multiscale record contains:

- source configuration, species, atom ordering, masses, positions, velocities, cell, and periodicity;
- electronic-reference method and source identifiers with observable units;
- TR-EIP parameters, features, graph cutoff, force and stress derivative settings;
- mechanical trajectory, thermal and pressure events, and sampled physical times;
- partitions, coarse memberships, hierarchy levels, centroids, reductions, and reconstructions;
- mesoscale and continuum provider identities, input records, output variables, and auxiliary fields;
- transport coefficients with their source estimator and transfer context;
- thermodynamic quantities, state-domain matching, relation and normalization identifiers;
- uncertainty inputs, correlation or ensemble model, and propagation method;
- engineering geometry, identified boundary conditions, flux and load conventions;
- continuous resonance states, descriptors, sampling instants, and phase parameters;
- retained and pending ternary states, requests, guards, and committed execution events;
- numerical methods, fixed comparison criteria, source versions, and ordered output traces.

The trace links each target representation to its source state and the operator and context used for the corresponding scale transition.

## 24. Executable Interface Index

| Role | Repository path |
| --- | --- |
| Electronic-reference record and provider | `src/tr_eif/multiscale/electronic_reference.py` |
| Interatomic energy and derived forces | `src/tr_eif/energy/model.py`, `src/tr_eif/energy/force_evaluator.py` |
| Derived stress | `src/tr_eif/energy/stress_evaluator.py` |
| MD state and trajectory | `src/tr_eif/md/state.py`, `src/tr_eif/md/trajectory.py` |
| Fine-to-coarse partition and reductions | `src/tr_eif/multiscale/partition.py`, `src/tr_eif/multiscale/reduction.py` |
| Mass-weighted centroids and vector averages | `src/tr_eif/multiscale/geometry.py`, `src/tr_eif/multiscale/vector_average.py` |
| Vector reduction and reconstruction | `src/tr_eif/multiscale/vector_reduction.py`, `src/tr_eif/multiscale/prolongation.py` |
| Partition composition and hierarchy | `src/tr_eif/multiscale/composition.py`, `src/tr_eif/multiscale/hierarchy.py` |
| Coarse and hierarchical state | `src/tr_eif/multiscale/state.py`, `src/tr_eif/multiscale/hierarchy_state.py` |
| Mesoscale closure | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Continuum closure | `src/tr_eif/multiscale/continuum_closure.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Transport coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Engineering boundary record | `src/tr_eif/multiscale/engineering_boundary.py` |
| Atomistic transport observables | `src/tr_eif/md/transport.py` |
| Resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| Ternary execution propagation | `src/tr_eif/md/ternary_propagation.py` |
| FLiBe multiscale state | `src/tr_eif/flibe/multiscale_coolant.py` |

## 25. Existing Test and Benchmark Interfaces

| Domain | Repository test path |
| --- | --- |
| Partition and scalar reduction invariants | `tests/invariants/test_multiscale_partition_invariants.py`, `tests/invariants/test_multiscale_reduction_invariants.py` |
| Geometric coarse state and hierarchy | `tests/invariants/test_multiscale_geometry_invariants.py`, `tests/invariants/test_multiscale_hierarchy_state_invariants.py` |
| Vector averaging and reconstruction | `tests/invariants/test_multiscale_vector_average_invariants.py`, `tests/invariants/test_multiscale_prolongation_invariants.py` |
| Electronic-reference inputs | `tests/integration/test_multiscale_electronic_reference.py` |
| Mesoscale closure | `tests/integration/test_multiscale_mesoscale_closure.py` |
| Continuum closure | `tests/integration/test_multiscale_continuum_closure.py` |
| Uncertainty transfer | `tests/integration/test_multiscale_uncertainty_propagation.py` |
| Thermodynamic consistency | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Transport transfer | `tests/integration/test_multiscale_transport_transfer.py` |
| Engineering boundary conditions | `tests/integration/test_multiscale_engineering_boundary.py` |
| Cross-scale record binding | `tests/integration/test_multiscale_cross_scale_validation.py` |
| FLiBe structural hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |
| Source-resolved FLiBe density comparisons | `tests/integration/test_flibe_experimental_aimd_density_cross_source_diagnostic.py` |

The existing Python CI runs the repository test suite in `TR-EIF Self Test`. Markdown Validation applies its separate manually dispatched documentation checks.

## 26. Volume Integration

Volume 06 composes the mathematical spaces and operators of Volume 01, continuous resonance and active-ternary execution of Volume 02, conservative E(3)-equivariant interatomic representations of Volume 03, learning interfaces of Volume 04, and molecular dynamics of Volume 05 into a multiscale mapping hierarchy.

The resulting data flow is:

`reference observables → interatomic energy and forces → atomic trajectory → coarse structural state → mesoscale closure → continuum variables → engineering boundary conditions`.

Thermodynamic relations, uncertainty propagation, transport coefficients, resonance evolution, and executed ternary controls are attached through their individually identified state and method contexts. Material-specific realizations, including the FLiBe reference model of Volume 07, supply the composition, source data, constitutive parameters, and boundary states for the selected multiscale calculation.
