
# Multiscale Coolant Model

## 1. Scope and System Class

This chapter defines the FLiBe multiscale coolant representation within TR-EIF. The system class is an open nonlinear dissipative dynamical system with three-dimensional atomic geometry, thermal and mechanical evolution, species transport, boundary exchange, continuous resonance variables, and separately scheduled balanced-ternary execution.

The structural mapping connects an ordered Li/Be/F atomic configuration to mass-weighted coarse states through an explicit hierarchy of partitions. Material-specific providers connect these states with mesoscale variables, continuum fields, transport coefficients, thermodynamic relations, uncertainty measures, and engineering boundary conditions.

The reference calculation chain is:

`FLiBeConfiguration → species masses and selected Cartesian positions → MultiscaleHierarchy → MultiscaleStateHierarchy → mesoscale closure → continuum closure → engineering boundary record`.

Each connection is associated with its source state, target representation, spatial and temporal scale, numerical method, and provenance.

## 2. Material and Composition Coordinates

FLiBe is represented in the LiF–BeF2 component basis. For nonnegative component formula-unit amounts with positive sum, define:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

`x_LiF + x_BeF2 = 1`.

The exact ratio `2 LiF : 1 BeF2` corresponds to `(x_LiF, x_BeF2) = (2/3, 1/3)` and atomic count ratio `Li:Be:F = 2:1:4`. Nominal `67 mol% LiF : 33 mol% BeF2` and source-measured specimen compositions retain their own numeric definitions and source metadata.

`FLiBeConfiguration` binds an `AtomicConfiguration` to the canonical Li, Be, and F species domain and provides the ordered atom count and composition mapping. The source composition and atom inventory are retained in the multiscale calculation context.

## 3. Three-Dimensional Fine State

For `N >= 1` atoms, let `S = (s_0, ..., s_(N-1))` be the ordered species, `R = (r_0, ..., r_(N-1))` the Cartesian positions, and `M = (m_0, ..., m_(N-1))` the positive masses, with `r_i in R^3`.

An `AtomicConfiguration` also stores optional cell vectors and three periodic-axis flags. An MD sample can additionally provide velocities, mechanical time, cell evolution, and physical boundary variables.

The executable FLiBe structural mapper receives one `FLiBeConfiguration`, an explicitly configured hierarchy, and species-mass parameters. A selected Cartesian position tuple provides the geometric input to the coarse-state calculations.

## 4. FLiBeMultiscaleCoolantModel

`FLiBeMultiscaleCoolantModel` in `src/tr_eif/flibe/multiscale_coolant.py` is an immutable dataclass with two fields:

| Field | Executable type | Role |
| --- | --- | --- |
| `hierarchy` | `MultiscaleHierarchy` | Ordered sequence of compatible fine-to-coarse partitions |
| `mass_parameters` | `FLiBeMassParameters` | Positive species-mass values for Li, Be, and F |

Construction validates both field types. The main operation is:

`model.build_state(configuration, positions=None) → MultiscaleStateHierarchy`.

The public function `build_flibe_multiscale_coolant_state(model, configuration, positions=None)` delegates to the same model operation after validating the model type.

The hierarchy's `finest_count` equals `configuration.atom_count`. Each completed mapping retains the input hierarchy and produces one coarse state for each partition transition.

## 5. Species Mass Assignment

`FLiBeMassParameters(lithium, beryllium, fluorine)` stores three positive finite numeric mass parameters in canonical species order. `configuration_masses(configuration, parameters)` maps them to the original atomic index order:

`m_i = mass_parameters.mass_for_species(species_i)`.

For species counts `N_Li`, `N_Be`, and `N_F`, the represented total mass is:

`M_total = N_Li m_Li + N_Be m_Be + N_F m_F`.

`total_configuration_mass` evaluates this aggregate. The selected mass unit, isotope or effective-mass convention where applicable, and parameter provenance are specified with the model inputs.

## 6. Fine Cartesian Position Selection

`FLiBeMultiscaleCoolantModel.build_state` selects its fine positions through the following executable rule:

- For a configuration whose periodic-axis flags are all false, `positions=None` selects `configuration.configuration.positions`.
- For a configuration with one or more periodic axes, the caller supplies an explicit `positions` tuple representing the selected unwrapped Cartesian coordinates.
- An explicitly supplied position tuple contains exactly one three-dimensional vector per FLiBe atom.

`build_multiscale_state_hierarchy` subsequently validates the numeric coordinates through the coarse-state construction operations. The selected coordinate frame, cell and image history, and sampling instant accompany a periodic coarse-graining calculation.

## 7. Fine-to-Coarse Partition

Let `p_l(i)` map fine entity `i` at level `l` to coarse entity `c` at level `l+1`. Define its ordered membership set:

`I_c^l = {i | p_l(i) = c}`.

`MultiscalePartition(fine_to_coarse=...)` stores a nonempty integer tuple with nonnegative, contiguous coarse identifiers beginning at zero. Every declared coarse group has at least one fine member.

The exact relations are:

`N_c^l <= N_f^l`.

`union_c I_c^l = {0, ..., N_f^l - 1}`.

`I_c^l intersection I_d^l = empty` for distinct groups `c` and `d`.

The partition exposes `fine_count`, `coarse_count`, `coarse_members`, `fine_indices_for`, and `coarse_index_for`. Structural membership and group identities use exact integer operations.

## 8. Additive Coarse Mass

For partition group `c`, the coarse mass is:

`M_c = sum_(i in I_c) m_i`.

`reduce_masses` validates positive finite fine masses and returns one positive coarse mass for each group. For a complete fixed-inventory partition:

`sum_c M_c = sum_i m_i`.

The numerical summation follows the ordered fine input. The corresponding conservation comparison uses the declared floating-point accumulation and tolerance policy, while group membership and tuple cardinalities use exact comparison.

## 9. Mass-Weighted Cartesian Centroids

For positive group mass `M_c`, the coarse position is:

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

`mass_weighted_centroids` computes this expression componentwise using the supplied Cartesian positions and masses. `build_coarse_scale_state` combines these centroids and `reduce_masses` into a `CoarseScaleState`.

The state stores its partition, ordered three-dimensional coarse positions, and positive coarse masses. It exposes `fine_count`, `coarse_count`, and `total_mass`.

## 10. Ordered Multiscale Hierarchy

`MultiscaleHierarchy(partitions=...)` contains a nonempty tuple of adjacent compatible partitions. For each consecutive pair, the earlier partition's `coarse_count` equals the following partition's `fine_count`.

With `L` transitions, its number of represented structural levels is:

`level_count = L + 1`.

The hierarchy exposes `transition_count`, `level_counts`, `finest_count`, `coarsest_count`, and `partition_at`. For consecutive mappings `p_0` and `p_1`, composition is:

`p_(0→2)(i) = p_1(p_0(i))`.

`composed_partition` returns a selected direct mapping across represented levels. The hierarchy preserves the order and cardinality of every intermediate level.

## 11. Hierarchical State Construction

`build_multiscale_state_hierarchy(positions, masses, hierarchy)` advances through the ordered transitions. At each transition it constructs a `CoarseScaleState` from the current positions, masses, and partition, then supplies the resulting coarse positions and masses to the next transition.

For level `l+1`, the formulas are:

`M_c^(l+1) = sum_(i in I_c^l) M_i^l`.

`R_c^(l+1) = [sum_(i in I_c^l) M_i^l R_i^l] / M_c^(l+1)`.

The immutable `MultiscaleStateHierarchy` stores the supplied hierarchy and one state per transition. Its `state_at(level)` addresses generated levels beginning at level 1; `coarsest_state` returns the last generated state.

## 12. Reference Numerical Hierarchy: Seven to Three to One

`tests/integration/test_flibe_multiscale_coolant_closure.py` defines a deterministic seven-atom FLiBe example with ordered species:

`S = (Li, Li, Be, F, F, F, F)`.

Its mass parameters are `m_Li = 2.0`, `m_Be = 3.0`, and `m_F = 5.0` in the fixture's consistent arbitrary mass unit. Its first partition is:

`p_0 = (0, 0, 1, 1, 2, 2, 2)`.

Its second partition is:

`p_1 = (0, 0, 0)`.

The resulting level counts are `(7, 3, 1)`. The fine positions and their corresponding coarse results are defined in the test fixture.

## 13. Reference Masses and Centroids

For the seven-atom reference, the first coarse level contains:

| Coarse group | Fine indices | Coarse mass | Cartesian centroid |
| --- | --- | ---: | --- |
| 0 | `(0, 1)` | `4.0` | `(0.5, 0, 0)` |
| 1 | `(2, 3)` | `8.0` | `(0.1875, 0.375, 0.625)` |
| 2 | `(4, 5, 6)` | `15.0` | `(1.1666666667, 1.0, 0.3333333333)` |

The final level has total mass:

`M_final = 4 + 8 + 15 = 27`.

Its centroid is:

`R_final = (7/9, 2/3, 10/27)`.

These are the outputs of the executed fixture under its declared mass and position units. The exact membership and numeric state values remain identifiable by hierarchy level.

## 14. Geometric Covariance

For orthogonal `Q in O(3)` and translation `b in R^3`, transform all fine positions by:

`r_i' = Q r_i + b`.

With the same partition and scalar masses, the centroid mapping satisfies:

`R_c' = Q R_c + b`.

Coarse masses are unchanged. A common atomic permutation, applied consistently to species, positions, masses, and partition assignments, preserves the represented coarse groups and their computed masses and centroids.

A periodic calculation transforms the cell and the selected position representation consistently with its geometrical reference frame.

## 15. Coarse Momentum and Internal Mechanical Motion

For a fixed group membership and atom velocities `v_i`, define group momentum and velocity:

`P_c = sum_(i in I_c) m_i v_i`.

`V_c = P_c / M_c`.

The existing `mass_weighted_vector_average` evaluates the corresponding coarse velocity from an explicitly supplied fine vector tuple and masses. For internal velocities `w_i = v_i - V_c`, the group kinetic energy decomposes as:

`(1/2) sum_(i in I_c) m_i |v_i|^2 = (1/2) M_c |V_c|^2 + (1/2) sum_(i in I_c) m_i |w_i|^2`.

Momentum and internal-energy variables can be added to a mesoscale closure through their declared physical units, reductions, and temporal sampling rules. The FLiBe structural `build_state` operation computes the mass-and-centroid hierarchy, while velocity and energy observables are supplied through their corresponding operators.

## 16. Atomistic Evolution and Coarse-State Sampling

An atomic trajectory at mechanical time `t[n]` contains ordered positions, velocities, positive masses, and boundary geometry. For a selected conditioned potential, its mechanical equations take the form:

`d r_i/dt = v_i`.

`m_i d v_i/dt = F_i`.

A multiscale sampling schedule selects the mechanical state, the applicable partition hierarchy, and the position representation supplied to `build_flibe_multiscale_coolant_state`.

The run record includes the MD timestep, sample time, material composition, cell history, partition identifiers, and all generated coarse states.

## 17. Local Structure and Continuous Resonance

The FLiBe atomistic level provides graph-relative coordination through `FLiBeCoordinationState`. A selected resonance parameterization maps this coordination to receiving-node coupling and phase-lag vectors.

For a directed graph with incoming edges `i→j`, continuous Kuramoto–Sakaguchi evolution is:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A scale-aware resonance mapping identifies the source oscillator state, graph, local structural descriptors, fine-to-coarse partition, target descriptor, and sampling instant. Its output can be associated with a selected mesoscale or continuum internal variable through an explicit provider.

## 18. Active Balanced-Ternary Execution

The executed alphabet is `-1/0/1`, including active neutral `0`. Retained state, requested target, pending destination, guards, held opportunity, and committed transition are represented through separately typed execution fields.

Opposite-polarity requests follow separate committed events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

A scale-aware execution mapping specifies the source execution nodes, coarse association, request and guard semantics, retained-state transfer, and event schedule. Structural mass and centroid reductions act on their physical numerical inputs; the selected execution mapping acts on the categorical state and event inputs.

## 19. Mesoscale Closure Provider

`evaluate_mesoscale_closure(state, evaluator, auxiliary_variables=())` supplies a `CoarseScaleState` and ordered auxiliary-variable tuple to an explicitly selected provider.

`MesoscaleClosureRecord` retains the coarse state, `closure_id`, `source_id`, named output variables, and auxiliary inputs. Each `MesoscaleClosureVariable` stores a normalized name and a nonempty tuple of finite numeric values. The collections use canonical unique name ordering.

A FLiBe mesoscale provider may use coarse masses, positions, velocities, internal energy, structural descriptors, and material-specific thermal or mechanical history as its declared input variables. Its constitutive equations and parameter sources are associated with the selected closure identifier.

## 20. Continuum Coolant Closure

`evaluate_continuum_closure(mesoscale, evaluator, auxiliary_variables=())` maps an explicitly supplied mesoscale record and continuum auxiliary inputs to a `ContinuumClosureRecord`.

The output retains the original mesoscale record, continuum `closure_id`, `source_id`, named continuum variables, and its auxiliary inputs. A continuum coolant realization identifies fields such as mass density, velocity, pressure, temperature, species concentration, and selected internal variables together with their units and spatial support.

The provider supplies its constitutive equations, spatial discretization, flux definitions, numerical time integration, and state-domain mapping.

## 21. Conservation Laws for a Coolant Control Region

For a fixed continuum region with total mass density `rho`, barycentric velocity `u`, and mass source `s_m`, the balance is:

`partial_t rho + div(rho u) = s_m`.

For species concentration `c_s`, diffusive flux `j_s`, and source `q_s`:

`partial_t c_s + div(c_s u + j_s) = q_s`.

For momentum density and Cauchy stress `sigma`, with body acceleration `b` and momentum source `s_p`:

`partial_t(rho u) + div(rho u ⊗ u) = div(sigma) + rho b + s_p`.

An energy balance is registered with its selected stored-energy density, total energy flux, external work, heat transport, and species-carried terms. The model context identifies the boundary and flux sign conventions and the corresponding numerical method.

## 22. Thermophysical State and Density

`FLiBeThermodynamicState` stores finite positive absolute temperature in kelvin and finite nonnegative pressure in pascal. `FLiBeDensityModel` associates a supplied evaluator with typed provenance and produces a positive mass-density parameter in `kg/m^3` for a selected thermodynamic state.

For a consistent coarse mass and physical volume:

`rho_coarse = M_coarse / V_coarse`.

The volume is associated with the chosen spatial region, coarse geometry, or continuum discretization. A thermophysical provider separately identifies composition, material-state domain, equation of state, source, and units.

Measured density records, source-derived correlations, simulation-cell density, and continuum density fields enter this calculation through their declared observable definitions and state mappings.

## 23. Thermal and Transport Coefficients

For temperature field `T` and isotropic conductivity `kappa`, a Fourier heat-flux relation is:

`q = -kappa grad(T)`.

With positive mass density `rho` and specific heat capacity `c_p`, thermal diffusivity is:

`alpha_T = kappa / (rho c_p)`.

For species concentration `c_s`, an isotropic Fickian diffusion branch is:

`j_s = -D_s grad(c_s)`.

Dynamic viscosity, thermal conductivity, species diffusion, electrical conduction, and hydrogen-isotope transport each retain their transported quantity, species or current definition, units, composition, and thermodynamic domain. The selected material provider supplies their temperature and composition dependence.

## 24. Cross-Scale Transport Transfer

`TransportCoefficient` records a coefficient identifier, finite scalar, unit, scale, state domain, and source. `TransportTransferContext` records the target scale, mapping, normalization, and assumptions identifiers.

`evaluate_transport_coefficient_transfer(source, context, evaluator)` returns a `TransportCoefficientTransferRecord` with its source coefficient, target coefficient, and exact mapping context.

The executable structural contracts include:

`target.coefficient_id = source.coefficient_id`.

`target.scale_id = context.target_scale_id`.

The provider defines the numerical or constitutive coefficient transformation and its material-state correspondence. Atomistic displacement and velocity-correlation observables can supply independently defined inputs to the selected coefficient-estimation procedure.

## 25. Thermodynamic Consistency and Uncertainty

`ThermodynamicVariable` identifies numerical values by variable, unit, scale, state domain, and provenance. `ThermodynamicConsistencyContext` identifies a selected relation, model, assumptions, and normalization. The evaluator returns a typed record linking the source and target variables to that context.

`UncertaintyMeasure` similarly identifies a quantity, magnitude, unit, representation, scale, state domain, and source. `evaluate_uncertainty_propagation` links canonical input measures to target-scale measures through a declared propagation and correlation context.

For a differentiable cross-scale mapping `y = f(x)` with Jacobian `J` and source covariance `C_x`, a first-order covariance mapping is:

`C_y ≈ J C_x J^T`.

The selected FLiBe material state, constitutive model, spatial averaging, data source, and numerical settings accompany the comparison and uncertainty records.

## 26. Engineering Boundaries and Exchange

`evaluate_engineering_boundaries(continuum, context, evaluator)` binds a `ContinuumClosureRecord` to an `EngineeringBoundaryContext` and a canonical tuple of `EngineeringBoundaryCondition` records.

The context identifies the engineering model, geometry, mapping, and assumptions. Each boundary condition identifies its spatial boundary, field, condition type, finite values, unit, and provenance source.

For boundary segment `Gamma_b` with outward unit normal `n_b`, representative conditions include:

`T|_(Gamma_b) = T_b`.

`q · n_b = q_b`.

`sigma n_b = t_b`.

A material and device realization associates those conditions with its coolant region geometry, thermal loads, applied pressure and flow, species exchange, and physical update schedule.

## 27. Reference Cross-Scale Test Chain

`tests/integration/test_flibe_multiscale_coolant_closure.py` composes the deterministic structural fixture with explicitly declared downstream providers.

The source hierarchy represents seven atoms at the finest level, three groups at the first coarse level, and one group at the coarsest level, carrying mass `27.0` in the fixture's mass unit.

The mesoscale evaluator records `total_mass_marker = (27.0,)`; the continuum evaluator records `coolant_mass_marker = (27.0,)`; and the engineering boundary evaluator binds a condition to the continuum variable value `(27.0,)`.

The same test module supplies independent typed transport-transfer, uncertainty-propagation, and thermodynamic-consistency fixtures. Their identifiers, sample values, source/target scales, context binding, and deterministic replay are checked by the integration tests.

## 28. Structural Invariants and Numerical Qualification

The executable contracts include:

- a typed `FLiBeMultiscaleCoolantModel` containing one compatible hierarchy and one species-mass parameter set;
- hierarchy finest-level cardinality equal to the supplied FLiBe atom count;
- one canonical Li/Be/F mass value assigned to each atom in configuration order;
- a valid selected Cartesian position tuple for the finest level;
- explicit position supply for configurations using periodic axes;
- contiguous integer coarse identifiers and complete fine-group membership;
- one `CoarseScaleState` per hierarchy transition;
- state partitions and coarse counts matching the corresponding hierarchy entries;
- positive finite coarse masses and finite three-component centroids;
- typed mesoscale, continuum, transport, thermodynamic, uncertainty, and engineering-provider records;
- exact `-1/0/1` execution-state membership and pending-route semantics when execution is coupled.

Mass and centroid calculations use their declared accumulation order and preselected numerical tolerances. Exact indices, cardinalities, identifiers, and categorical events use exact comparisons. Repeated evaluations with identical inputs and deterministic providers are compared through their ordered output records.

## 29. Reproducibility and Scale-Transition Trace

A complete FLiBe multiscale coolant calculation records:

- LiF–BeF2 component composition, atomic species sequence, and mass-parameter values and units;
- fine positions, cell and periodic flags, explicit unwrapping representation, and sampling instant;
- each `MultiscalePartition`, level count, member set, coarse mass, and centroid;
- the complete `MultiscaleStateHierarchy`, including source and target level identities;
- mechanical trajectory samples, energy and momentum observations, and boundary exchanges when coupled;
- coordination and continuous resonance state, phase-parameter values, and integration times when included;
- ternary requests, retained and pending states, guard permissions, and committed execution indices;
- mesoscale and continuum providers, named variables, auxiliary inputs, and resolved constitutive context;
- transported coefficients and physical state-domain mappings;
- thermodynamic variables, source relations, uncertainties, and correlation models;
- engineering geometry, boundary identifiers, values, units, and flux or load conventions;
- numerical methods, source versions, comparison criteria, and deterministic output identifiers.

The scale-transition trace retains each generated state and the operator and context associated with its construction.

## 30. Executable Interface Index

| Function | Repository path |
| --- | --- |
| FLiBe multiscale coolant model and public builder | `src/tr_eif/flibe/multiscale_coolant.py` |
| FLiBe atomic configuration and composition | `src/tr_eif/flibe/configuration.py`, `src/tr_eif/flibe/composition.py` |
| Species masses and assignment | `src/tr_eif/flibe/mass.py` |
| Three-dimensional configuration | `src/tr_eif/configuration/state.py` |
| Fine-to-coarse partition | `src/tr_eif/multiscale/partition.py` |
| Scalar and mass reduction | `src/tr_eif/multiscale/reduction.py` |
| Mass-weighted centroids | `src/tr_eif/multiscale/geometry.py` |
| Coarse structural state | `src/tr_eif/multiscale/state.py` |
| Partition composition and hierarchy | `src/tr_eif/multiscale/composition.py`, `src/tr_eif/multiscale/hierarchy.py` |
| Hierarchical coarse-state construction | `src/tr_eif/multiscale/hierarchy_state.py` |
| Mass-weighted vector averaging | `src/tr_eif/multiscale/vector_average.py` |
| Mesoscale closure | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Continuum closure | `src/tr_eif/multiscale/continuum_closure.py` |
| Transport coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Engineering boundary mapping | `src/tr_eif/multiscale/engineering_boundary.py` |
| FLiBe thermodynamic state and density | `src/tr_eif/flibe/thermodynamic_state.py`, `src/tr_eif/flibe/density.py` |
| FLiBe coordination and resonance | `src/tr_eif/flibe/coordination.py`, `src/tr_eif/flibe/resonance_descriptor.py` |
| FLiBe TR-EIP energy | `src/tr_eif/flibe/tr_eip.py` |
| MD mechanical trajectory and transport | `src/tr_eif/md/trajectory.py`, `src/tr_eif/md/transport.py` |
| MD-associated resonance and execution | `src/tr_eif/md/resonance_propagation.py`, `src/tr_eif/md/ternary_propagation.py` |

## 31. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| FLiBe model types, hierarchy input, and periodic positions | `tests/invariants/test_flibe_multiscale_coolant_invariants.py` |
| Complete FLiBe structural and provider chain | `tests/integration/test_flibe_multiscale_coolant_closure.py` |
| Coarse-state invariants | `tests/invariants/test_multiscale_state_invariants.py` |
| Multilevel state construction | `tests/invariants/test_multiscale_hierarchy_state_invariants.py` |
| Partition and hierarchy invariants | `tests/invariants/test_multiscale_partition_invariants.py`, `tests/invariants/test_multiscale_hierarchy_invariants.py` |
| Geometric reduction and vector averaging | `tests/invariants/test_multiscale_geometry_invariants.py`, `tests/invariants/test_multiscale_vector_average_invariants.py` |
| Mesoscale and continuum providers | `tests/integration/test_multiscale_mesoscale_closure.py`, `tests/integration/test_multiscale_continuum_closure.py` |
| Transport coefficient transfer | `tests/integration/test_multiscale_transport_transfer.py` |
| Thermodynamic consistency and uncertainty | `tests/integration/test_multiscale_thermodynamic_consistency.py`, `tests/integration/test_multiscale_uncertainty_propagation.py` |
| Engineering boundaries | `tests/integration/test_multiscale_engineering_boundary.py` |
| MD trajectory and transport observables | `tests/integration/test_molecular_dynamics_trajectory.py`, `tests/integration/test_molecular_dynamics_transport.py` |

## 32. Chapter Integration

The executable FLiBe multiscale coolant model maps Li/Be/F atomic inventory and selected three-dimensional coordinates into an ordered hierarchy of positive coarse masses and mass-weighted centroids. Every transition retains its partition and the correspondence to its source scale.

Typed mesoscale, continuum, transport, thermodynamic, uncertainty, and engineering operators attach the selected constitutive and boundary information to those coarse states. Continuous resonance and active balanced-ternary execution participate through separately sampled descriptors and event-conditioned interatomic computation within the declared multiscale schedule.
