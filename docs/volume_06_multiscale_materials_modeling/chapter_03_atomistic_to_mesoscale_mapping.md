
# Atomistic-to-Mesoscale Mapping

## 1. Scope and System Class

This chapter defines the transfer of atomistic states and observables to explicit mesoscale representations within TR-EIF. The source level contains three-dimensional atomic geometry, mechanical trajectories, interatomic energy, continuous resonance dynamics, and balanced-ternary execution. The target level contains coarse structural states and typed variables supplied to a mesoscale closure.

The system class is an open nonlinear dissipative dynamical system. Its scale transition identifies the atomic inventory, spatial partition, temporal sampling, boundary exchange, mapping operators, and provenance of each source and target quantity.

The executable geometric chain is:

`atomic positions and masses → fine-to-coarse partition → coarse masses and centroids → coarse-scale state → mesoscale closure provider → mesoscale record`.

Momentum-like vectors, additive fields, reconstruction operations, and hierarchical transfers are handled through the corresponding explicit interfaces.

## 2. Atomistic Source State

For `N_f >= 1` fine entities, let:

- `s_i` denote atomic species;
- `r_i(t) in R^3` denote Cartesian position;
- `v_i(t) in R^3` denote Cartesian velocity;
- `m_i > 0` denote atomic mass;
- `B(t)` denote the cell matrix, when supplied;
- `P` denote the three periodic-axis flags.

A mechanical sample is taken from `MolecularDynamicsState` at its recorded step and physical time. The atom ordering used for positions, velocities, masses, and any auxiliary fields is retained through the mapping.

For a fixed-inventory interval, the tuple of fine positions and positive masses supplies the executable `build_coarse_scale_state` operation. Additional mechanical and thermodynamic quantities are transferred through their declared scalar, vector, or closure mappings.

## 3. Fine-to-Coarse Partition

Define a partition of fine indices into `N_c` coarse groups:

`p: {0, ..., N_f - 1} → {0, ..., N_c - 1}`.

For each coarse group `c`, its member set is:

`I_c = {i | p(i) = c}`.

The executable `MultiscalePartition(fine_to_coarse=...)` accepts a nonempty tuple of nonnegative integer assignments with contiguous coarse identifiers starting at zero. Every coarse identifier is represented by at least one fine entity.

Its exact cardinality relations are:

`1 <= N_c <= N_f`.

`I_c ∩ I_d = empty` for `c != d`.

`union_c I_c = {0, ..., N_f - 1}`.

The fields and accessors `fine_count`, `coarse_count`, `fine_indices_for`, `coarse_index_for`, `coarse_members`, and `is_identity` expose these assignments in a deterministic index order.

A time-dependent partition specifies the instants at which membership is recomputed and records each change of membership as part of the scale-transition history.

## 4. Mass Reduction

For a fixed partition and positive fine masses, define the mass represented by coarse entity `c`:

`M_c = sum_(i in I_c) m_i`.

`reduce_masses(masses, partition)` evaluates this reduction, returning one positive finite mass per coarse group. The mathematical partition identity gives:

`sum_c M_c = sum_i m_i`.

The executable accumulation follows the ordered fine tuple. Its floating-point conservation checks compare the computed values under a declared summation and numerical tolerance policy. The group membership and positive-mass contracts are checked by their exact and typed conditions.

## 5. Three-Dimensional Coarse Positions

For the same partition, define the mass-weighted Cartesian centroid:

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

The operator `mass_weighted_centroids(positions, masses, partition)` calculates three Cartesian components for each coarse group. `build_coarse_scale_state` combines the resulting centroids with `reduce_masses`.

The immutable `CoarseScaleState` stores:

- the originating `MultiscalePartition`;
- a tuple of three-dimensional coarse positions;
- a tuple of positive coarse masses.

Its `fine_count`, `coarse_count`, and `total_mass` properties are derived from that state. The fine-to-coarse mapping therefore retains its structural correspondence with the original atomic inventory.

## 6. Periodic Cells and Coordinate Reconstruction

A Cartesian centroid is evaluated from a consistent spatial representation of all positions in its group. For periodic trajectories, define an image-resolved coordinate history, for example:

`r_i,unwrapped(t) = r_i,wrapped(t) + B(t) k_i(t)`.

Here `k_i(t)` is the declared integer image history under the selected cell and coordinate convention. The coarse centroid uses the chosen unwrapped Cartesian coordinates and records the reference frame when the cell changes with time.

The FLiBe multiscale operator `FLiBeMultiscaleCoolantModel.build_state` accepts explicit `positions` for this purpose. With a periodic FLiBe configuration it requires an explicit position tuple for the fine atoms; with a nonperiodic configuration its supplied atomic positions can be used directly.

The selected unwrapping rule, cell history, coordinate reference, and partition membership are retained alongside periodic mesoscale geometry.

## 7. Additive Scalar and Vector Transfer

For a fine scalar `a_i` defined as an additive quantity under the chosen partition, let:

`A_c = sum_(i in I_c) a_i`.

`reduce_scalar_sum(values, partition)` implements this mapping. Fine scalar inputs are finite and have one entry per fine entity.

For a Cartesian vector `u_i` defined as additive, let:

`U_c = sum_(i in I_c) u_i`.

`reduce_vector_sum(vectors, partition)` evaluates this sum componentwise with one three-dimensional input vector per fine entity.

The variable definition determines whether the mapped quantity uses summation, averaging, a constitutive transform, or an additional geometric operator. Coarse scalars, Cartesian vectors, physical energy, resonance variables, and ternary execution records retain their individual type contracts.

## 8. Coarse Velocity and Linear Momentum

For fine velocities at a common physical time, define coarse linear momentum:

`P_c = sum_(i in I_c) m_i v_i`.

The mass-weighted coarse velocity is:

`V_c = P_c / M_c = (1/M_c) sum_(i in I_c) m_i v_i`.

`mass_weighted_vector_average(vectors, masses, partition)` implements the three-component mass-weighted average. For velocities, the relation yields:

`sum_c M_c V_c = sum_i m_i v_i`.

For constant masses and fixed membership on a differentiable interval, centroid motion obeys:

`dR_c/dt = V_c`.

With fine mechanical forces `F_i`, the corresponding group momentum relation is:

`dP_c/dt = sum_(i in I_c) F_i`.

For material transfer, evolving membership, or open boundaries, the target momentum balance additionally includes the defined transfer and boundary-flux terms.

## 9. Bulk and Internal Kinetic Energy

The kinetic energy of the fine atoms in one coarse group is:

`K_c,fine = (1/2) sum_(i in I_c) m_i |v_i|^2`.

Introduce internal velocity deviations relative to the group velocity:

`w_i = v_i - V_c`.

The mass-weighted definition gives:

`sum_(i in I_c) m_i w_i = 0`.

Expanding `|V_c + w_i|^2` yields the exact mathematical decomposition:

`K_c,fine = (1/2) M_c |V_c|^2 + (1/2) sum_(i in I_c) m_i |w_i|^2`.

The first term represents the resolved centroid motion; the second term represents kinetic motion internal to the coarse group. A mesoscale thermodynamic or dissipative closure can use the internal contribution with its specified degree-of-freedom, temperature, and exchange conventions.

The executable coarse structural state stores centroids and masses. A velocity field and its kinetic decomposition are computed from the separate vector-averaging and mechanical observables when included in the selected mapping schedule.

## 10. Angular Momentum and Internal Structure

For fixed group membership, define fine angular momentum about a shared origin:

`L_c = sum_(i in I_c) r_i × (m_i v_i)`.

Write `r_i = R_c + rho_i` and `v_i = V_c + w_i`. Since the mass-weighted internal position and velocity sums vanish, the exact decomposition is:

`L_c = R_c × (M_c V_c) + sum_(i in I_c) rho_i × (m_i w_i)`.

The internal term describes the group's unresolved angular momentum relative to its centroid. An extended mesoscale record identifies the tensorial or rotational variables used to represent this term, together with their physical units and update equations.

The coarse centroid, coarse velocity, and internal angular-momentum representations are distinct components of a scale-transfer description.

## 11. E(3) Transformation Contract

Under an orthogonal transformation `Q in O(3)` and translation `b in R^3`, let:

`r_i' = Q r_i + b`.

`v_i' = Q v_i`.

For unchanged partition membership and scalar masses, the coarse variables satisfy:

`M_c' = M_c`.

`R_c' = Q R_c + b`.

`V_c' = Q V_c`.

`P_c' = Q P_c`.

Consequently, the group kinetic-energy decomposition is invariant under a common orthogonal spatial transformation of all velocity vectors. The internal angular-momentum term transforms according to the axial-vector convention associated with the selected orthogonal transformation.

A geometry-dependent partition rule specifies how membership is transported under spatial transformations; the reference mapping evaluates a supplied fixed partition.

## 12. Atomistic Energy and Coarse Closure Variables

Let the conditioned interatomic potential be represented as:

`E_atom = E(R, G, Q_features, sigma; Theta)`.

`G` is the selected interaction graph, `Q_features` denotes typed features, and `sigma` is the retained balanced-ternary execution vector. The force operator is derived from the chosen differentiable energy branch.

A scale-transfer calculation defines coarse energy and stress observables through an explicit partition, geometric averaging rule, interaction accounting convention, and closure context. Internal kinetic motion, intra-group interactions, inter-group interactions, boundary fluxes, and external work can be identified as separate contributions.

The `MesoscaleClosureVariable` structure associates each selected quantity with a normalized name and a tuple of finite numeric values. Material-specific interpretation, units, constitutive coefficients, and history are supplied through the corresponding closure configuration and provenance.

## 13. Mesoscale Closure Provider

The executable mesoscale interface uses:

`evaluate_mesoscale_closure(state, evaluator, auxiliary_variables=())`.

Here `state` is a `CoarseScaleState`, `evaluator` is a callable provider, and `auxiliary_variables` is a tuple of typed `MesoscaleClosureVariable` inputs.

The provider returns a `MesoscaleClosureRecord` containing:

- `state`: the input coarse-scale state;
- `closure_id`: the selected closure identifier;
- `source_id`: the declared source identifier;
- `closure_variables`: a nonempty tuple of named finite output variables;
- `auxiliary_variables`: the supplied auxiliary-variable tuple.

Variable names are normalized and placed in canonical sorted order, with unique names within each tuple. The evaluator boundary checks the returned state and auxiliary tuple against the supplied inputs.

The `variable(name)` accessor retrieves one output by its normalized identifier. Constitutive dynamics are defined by the provider and the context used to construct its closure variables.

## 14. Coarse-to-Fine Reconstruction

For a coarse scalar `A_c` and Cartesian vector `U_c`, broadcast prolongation is defined by:

`a_i,reconstructed = A_(p(i))`.

`u_i,reconstructed = U_(p(i))`.

`prolong_scalar_broadcast` and `prolong_vector_broadcast` implement these assignments and return one value per fine entity. Input tuples have one value per coarse entity.

Reconstruction may be followed by evaluation of a fine-scale residual, a comparison observable, or a specified correction operator. Each operation uses a declared definition for additive versus averaged quantities and the physical dimensions of the transferred field.

## 15. Composition of Consecutive Partitions

For fine-to-intermediate partition `p_0` and intermediate-to-coarse partition `p_1`, require matching intermediate entity counts and define:

`p_(0→2)(i) = p_1(p_0(i))`.

`compose_partitions(p_0, p_1)` constructs this direct partition. `MultiscaleHierarchy` stores a nonempty ordered sequence of compatible adjacent partitions.

For `L` transitions, the hierarchy contains `L + 1` scale levels. Its `level_counts`, `finest_count`, `coarsest_count`, and `composed_partition(start_level, end_level)` expose the structural correspondence among levels.

The partition-composition operation is exact on integer assignments. Numerical reductions across a hierarchy preserve their declared accumulation order and compare staged and directly composed results using the selected arithmetic tolerance.

## 16. Construction of a Coarse-State Hierarchy

`build_multiscale_state_hierarchy(positions, masses, hierarchy)` applies mass reduction and centroid construction at each adjacent transition.

At hierarchy level `l`, write its positions and masses as `R_i^l` and `M_i^l`. For coarse entity `c` at level `l + 1`:

`M_c^(l+1) = sum_(i in I_c^l) M_i^l`.

`R_c^(l+1) = [sum_(i in I_c^l) M_i^l R_i^l] / M_c^(l+1)`.

The returned `MultiscaleStateHierarchy` holds one `CoarseScaleState` per transition. Its `state_count`, `state_at(level)`, and `coarsest_state` access the generated coarse states, and each stored state is bound to its matching partition in the hierarchy.

The group membership and state-count checks use exact categorical comparisons; Cartesian sums and normalized positions use the declared floating-point evaluation convention.

## 17. Numerical Example: Four Fine Entities

Let the partition be:

`p = (0, 0, 1, 1)`.

Choose fine positions, masses, and velocities:

| Fine index | Position | Mass | Velocity |
| --- | --- | --- | --- |
| `0` | `(0, 0, 0)` | `1` | `(1, 0, 0)` |
| `1` | `(2, 0, 0)` | `3` | `(3, 0, 0)` |
| `2` | `(10, 0, 0)` | `2` | `(-1, 0, 0)` |
| `3` | `(14, 0, 0)` | `2` | `(1, 0, 0)` |

Mass reduction and centroids give:

`M = (4, 4)`.

`R = ((1.5, 0, 0), (12, 0, 0))`.

Mass-weighted velocity averaging gives:

`V = ((2.5, 0, 0), (0, 0, 0))`.

The total fine and coarse linear momenta both equal `(10, 0, 0)`. The fine kinetic energy is `16`, while coarse centroid kinetic energy is `12.5`; the internal kinetic contribution is `3.5`, satisfying the decomposition in Section 9.

All quantities in this example use one consistent mass–length–time unit system.

## 18. Open-System Exchange and Temporal Transfer

For a fixed group membership over a smooth time interval, the coarse momentum derivative follows the sum of fine forces. An open-system coarse balance additionally contains declared advective, diffusive, dissipative, and boundary-exchange contributions.

A generic coarse conserved-density balance can be written as:

`d/dt integral_(Omega_c) rho_a dV = -integral_(boundary Omega_c) J_a · n dA + integral_(Omega_c) q_a dV`.

`rho_a` is the selected density, `J_a` its outward-oriented flux, and `q_a` the volume source term. Their constitutive definitions depend on the transferred species, momentum component, energy variable, or other physical observable.

A coupled temporal schedule specifies the atomistic sampling times, partition updates, mesoscale closure-evaluation times, and the association between fine and coarse states. Changing group membership is recorded together with its transferred mass, momentum, energy, and auxiliary state.

## 19. Continuous Resonance Transfer

The atomistic resonance state contains continuous oscillator phases and frequencies with parameters and a graph sampled from atomic geometry. The Kuramoto–Sakaguchi evolution uses receiving-node coupling and phase lag:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A mesoscale resonance mapping specifies its fine input phases, coupling graph, partition, descriptor, aggregation or reconstruction method, and coarse time index. Global or local phase order and continuous resonance-window coordinates retain their own mathematical definitions.

The source resonance state, output descriptor, and mapping context are separately recorded at every selected scale-transition event.

## 20. Balanced-Ternary Execution Transfer

The canonical executed-state alphabet is `-1/0/1`, with active neutral `0`. A node execution state contains a retained state and an optional pending destination. Committed opposite-polarity routes consist of separate events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

A mesoscale execution mapping specifies the source execution nodes, coarse membership, request semantics, guard rules, retained-state interpretation, pending destinations, and event ordering. The mapping retains discrete execution identities through exact typed operations.

The scalar mass and centroid reductions apply to their physical numeric quantities. Execution-state transfer is defined through its own operator, with active-neutral retention and committed-event semantics preserved.

## 21. Uncertainty and Cross-Scale Provenance

Each transferred quantity has an identified source scale, target scale, state domain, unit, and mapping context. Measured, calculated, and model-derived quantities retain their respective method and source identifiers.

For an uncertainty-bearing variable, the mapping identifies its input uncertainty representation, correlation model, propagation rule, and normalization. The interfaces `UncertaintyMeasure`, `UncertaintyPropagationContext`, and `evaluate_uncertainty_propagation` bind these inputs to a typed transfer record.

A mesoscale closure associates its output and auxiliary variables with its `closure_id` and `source_id`, and the larger trace links that record to the originating atomistic configuration and partition.

## 22. Numerical and Structural Qualification

The executable structural checks include:

- contiguous integer coarse-group identifiers and complete fine-group membership;
- positive finite masses and one mass/position per fine entity;
- three finite Cartesian components per position and vector;
- one coarse position and mass per coarse group;
- matching adjacent hierarchy cardinalities;
- exact composition of integer partition assignments;
- matching coarse-state and hierarchy transition identities;
- one output variable per declared closure name, in canonical name order;
- returned closure state and auxiliary variables matching provider inputs.

Numerical checks include mass-sum agreement, centroid arithmetic, momentum projection, E(3) transformation relations, hierarchical reduction and reconstruction, internal kinetic-energy decomposition, and deterministic output ordering under selected fixed input data.

The numerical method and comparison tolerances are declared before computing each floating-point qualification result. Exact integer membership, categorical state, and execution-route invariants use exact comparisons.

## 23. Reproducibility Record

A complete atomistic-to-mesoscale transfer record specifies:

- fine species, particle indices, positions, velocities, masses, cell, and periodicity;
- sampling time and reference coordinate frame, including periodic unwrapping;
- partition identity, fine-to-coarse assignments, and any membership-change history;
- reduction operator, weight convention, and source/target units;
- coarse masses, centroids, velocity or additive-vector fields, and selected internal observables;
- hierarchy levels, composed partitions, intermediate states, and output ordering;
- selected closure provider, source identifier, output variables, and auxiliary inputs;
- force/energy model and boundary-exchange convention where coupled to dynamics;
- continuous resonance inputs and selected scale-mapping descriptor;
- ternary request, retained, pending, guarded, and committed event records;
- uncertainty-propagation context and numerical qualification settings.

These fields establish the source-to-target mapping and the temporal, spatial, and numerical context needed for deterministic replay.

## 24. Executable Interface Index

| Operation | Repository path |
| --- | --- |
| Fine-to-coarse membership | `src/tr_eif/multiscale/partition.py` |
| Scalar and mass reduction | `src/tr_eif/multiscale/reduction.py` |
| Mass-weighted centroids | `src/tr_eif/multiscale/geometry.py` |
| Coarse-state construction | `src/tr_eif/multiscale/state.py` |
| Additive vector reduction | `src/tr_eif/multiscale/vector_reduction.py` |
| Mass-weighted vector average | `src/tr_eif/multiscale/vector_average.py` |
| Scalar and vector broadcast | `src/tr_eif/multiscale/prolongation.py` |
| Partition composition | `src/tr_eif/multiscale/composition.py` |
| Multilevel partition hierarchy | `src/tr_eif/multiscale/hierarchy.py` |
| Coarse-state hierarchy | `src/tr_eif/multiscale/hierarchy_state.py` |
| Mesoscale closure provider and record | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Cross-scale uncertainty | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Atomistic mechanical state | `src/tr_eif/md/state.py` |
| Molecular trajectory | `src/tr_eif/md/trajectory.py` |
| Periodic Cartesian image geometry | `src/tr_eif/geometry/periodic.py` |
| Conditioned interatomic energy | `src/tr_eif/energy/model.py` |
| Continuous resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| Ternary execution propagation | `src/tr_eif/md/ternary_propagation.py` |
| FLiBe coarse hierarchy | `src/tr_eif/flibe/multiscale_coolant.py` |

## 25. Existing Test Interfaces

| Domain | Repository test path |
| --- | --- |
| Partition membership | `tests/invariants/test_multiscale_partition_invariants.py` |
| Scalar and mass reductions | `tests/invariants/test_multiscale_reduction_invariants.py` |
| Cartesian centroids | `tests/invariants/test_multiscale_geometry_invariants.py` |
| Coarse-state construction | `tests/invariants/test_multiscale_state_invariants.py` |
| Vector reductions | `tests/invariants/test_multiscale_vector_reduction_invariants.py` |
| Vector averaging | `tests/invariants/test_multiscale_vector_average_invariants.py` |
| Reconstruction operators | `tests/invariants/test_multiscale_prolongation_invariants.py` |
| Partition composition | `tests/invariants/test_multiscale_partition_composition_invariants.py` |
| Hierarchy construction | `tests/invariants/test_multiscale_hierarchy_invariants.py` |
| Hierarchical coarse states | `tests/invariants/test_multiscale_hierarchy_state_invariants.py` |
| Cross-level transfer | `tests/integration/test_multiscale_hierarchy_transfer.py` |
| Mesoscale provider contract | `tests/integration/test_multiscale_mesoscale_closure.py` |
| FLiBe hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |

## 26. Summary

The atomistic-to-mesoscale mapping constructs structural coarse states from explicit atomic partitions, positive masses, and three-dimensional mass-weighted centroids. Scalar and vector reductions, velocity averaging, broadcast prolongation, partition composition, and hierarchy construction provide additional typed scale-transfer operators.

Mesoscale closure records bind those coarse states to identified constitutive variables and supplied auxiliary inputs. Mechanical exchange, continuous resonance dynamics, active balanced-ternary execution, and uncertainty transfer connect through explicitly scheduled and recorded mappings between their respective state spaces.
