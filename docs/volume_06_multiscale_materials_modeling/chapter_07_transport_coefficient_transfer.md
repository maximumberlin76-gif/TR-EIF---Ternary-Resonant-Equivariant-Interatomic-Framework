
# Transport Coefficient Transfer

## 1. Scope and System Class

This chapter specifies the transfer of transport coefficients among atomistic, mesoscale, continuum, and engineering representations in TR-EIF. The source class is an open nonlinear dissipative dynamical system with three-dimensional material geometry, mechanical and thermal exchange, continuous resonance dynamics, and separately scheduled balanced-ternary execution.

The cross-scale calculation is organized as:

`source observable and state → coefficient estimation → identified source coefficient → transfer context → evaluator → target coefficient → continuum or engineering closure`.

The executable transfer interface is defined in `src/tr_eif/multiscale/transport_transfer.py`. Microscopic displacement and velocity-correlation series are defined separately in `src/tr_eif/md/transport.py`. Each stage retains its quantity definition, numerical method, units, scale, state domain, and provenance.

## 2. Transport Quantity and Physical State

Let `a` identify a transport coefficient in a declared material state domain `X_l`, at source scale `l`. Denote the coefficient by:

`K_a^(l) = K_a(X_l, method_l, boundary_l)`.

The identifier selects a defined observable, for example species-specific self-diffusion, collective diffusion, thermal conductivity, dynamic viscosity, or an electrical transport coefficient. A source coefficient record specifies its scalar numerical value, physical unit, scale, domain, and source identifier.

A target state at scale `m` has an associated mapping context `C_(l→m)`. The mathematical transfer is written:

`K_a^(m) = M_a(K_a^(l), X_l, X_m; C_(l→m))`.

The selected transfer method specifies state correspondence, geometrical representation, normalization, constitutive assumptions, and any dependent thermodynamic variables. Time-dependent or anisotropic realizations may associate the transfer with additional field, tensor, and history representations.

## 3. Executable TransportCoefficient

`TransportCoefficient` is an immutable dataclass with the following fields:

| Field | Executable meaning |
| --- | --- |
| `coefficient_id` | Normalized nonempty transport-quantity identifier |
| `value` | Finite real scalar normalized to `float` |
| `unit` | Normalized nonempty physical-unit identifier |
| `scale_id` | Normalized nonempty source or target scale identifier |
| `state_domain_id` | Normalized nonempty state-domain identifier |
| `source_id` | Normalized nonempty provenance identifier |

Integer and floating-point inputs are accepted for `value`, excluding Boolean values. The scalar type permits finite positive, zero, and negative values; the selected physical coefficient model defines any additional sign or admissibility conditions.

The `unit` and `state_domain_id` fields are retained independently from the coefficient identity. This allows a transfer method to apply an explicit unit or state transformation while preserving the identity of the transported coefficient.

## 4. Transfer Context

`TransportTransferContext` is an immutable dataclass containing four normalized nonempty identifiers:

- `target_scale_id`: destination model scale;
- `mapping_id`: the selected cross-scale coefficient mapping;
- `normalization_id`: unit, averaging, and normalization procedure;
- `assumptions_id`: declared constitutive and physical-state assumptions.

The corresponding method registration resolves these identifiers into equations, coefficients, units, sampling conventions, state conditions, and numerical parameters. A source-to-target calculation supplies its context explicitly to the transfer evaluator.

## 5. Transfer Record and Exact Binding

`TransportCoefficientTransferRecord` stores three typed objects:

`record = (source, target, context)`.

Its construction enforces:

`target.coefficient_id == source.coefficient_id`.

`target.scale_id == context.target_scale_id`.

The source and target individually retain their numerical values, units, state domains, and source identifiers. A transfer may therefore express a coefficient value at a different scale or in a differently normalized state domain, with these differences represented in the stored records.

The record types, coefficient identity, and destination-scale identity are exact structural contracts.

## 6. Transfer Evaluator

The public call is:

`evaluate_transport_coefficient_transfer(source, context, evaluator)`.

`evaluator` is a callable accepting one `TransportCoefficient` and one `TransportTransferContext`, returning one `TransportCoefficientTransferRecord`.

The evaluation boundary:

1. Validates the source coefficient type.
2. Validates the transfer-context type and evaluator callability.
3. Calls the evaluator with the supplied source and context.
4. Validates the returned record type.
5. Requires `result.source == source`.
6. Requires `result.context == context`.
7. Returns the complete source–target transfer record.

The evaluator supplies the selected numerical and constitutive mapping. The transfer record binds its output to the original input and the declared destination scale.

## 7. Atomistic Trajectory Inputs

For `N >= 1` atoms with Cartesian coordinates `r_i(t)`, velocities `v_i(t)`, and a recorded physical time sequence, `MolecularDynamicsTrajectory` provides the ordered mechanical states used to evaluate microscopic transport observables.

The current transport implementation exposes:

- `mean_squared_displacement(trajectory)` returning `MeanSquaredDisplacementSeries`;
- `velocity_autocorrelation(trajectory)` returning `VelocityAutocorrelationSeries`.

Both series contain ordered tuples `times` and `values`, beginning with an elapsed-time origin. They use all stored atoms with equal weight and the first stored state as their time origin. The velocity correlation accepts signed values; the mean-squared displacement is nonnegative.

These series provide numerical inputs from which a specified coefficient estimator can be constructed.

## 8. Mean-Squared Displacement and Diffusion

For an atomic species or tracer selected by an index set `I_s` with cardinality `N_s > 0`, define a single-origin self-displacement observable:

`MSD_s(tau) = (1/N_s) sum_(i in I_s) |r_i(t_0 + tau) - r_i(t_0)|^2`.

For a stationary isotropic three-dimensional diffusive regime, the Einstein relation is:

`D_self,s = lim_(tau→infinity) MSD_s(tau) / (6 tau)`.

Within an identified linear diffusive interval, a slope estimator is:

`D_self,s = (1/6) d(MSD_s)/d tau`.

The current `mean_squared_displacement` computes the all-atom, single-origin expression for nonperiodic trajectories. A periodic diffusion calculation supplies its declared unwrapped-coordinate history, image convention, and coefficient estimator. The resulting `D_self,s` is registered with a transported-species identifier, temperature, composition, boundary geometry, sampling conditions, and units of length squared per time.

## 9. Velocity Correlations and Green–Kubo Diffusion

For a stationary equilibrium ensemble and a selected species `s`, define the time-origin-averaged Cartesian velocity correlation:

`C_v,s(tau) = <v_s(t_0) · v_s(t_0 + tau)>`.

Under the associated correlation-integrability conditions, the Green–Kubo self-diffusion relation is:

`D_self,s = (1/3) integral_(0→infinity) C_v,s(tau) d tau`.

The executable `velocity_autocorrelation` evaluates the all-atom single-origin mean `v_i(t_0) · v_i(t_0+tau)`. A coefficient calculation specifies its particle subset, time-origin averaging, equilibrium ensemble, numerical quadrature, integration window, and statistical estimator.

The output coefficient is identified separately from the input correlation series in the transfer record.

## 10. Collective Species Transport

For species mass concentration `c_s`, barycentric material velocity `u`, and diffusive mass flux `j_s`, an open-system balance may be written:

`partial_t c_s + div(c_s u + j_s) = q_s`.

A selected isotropic Fickian closure is:

`j_s = -D_s grad(c_s)`.

Multicomponent and charged materials may instead use coupled thermodynamic driving forces, with a constitutive mapping such as:

`j_s = -sum_r L_(s,r) grad(mu_r / T)`.

Here `L_(s,r)` is associated with the chosen flux definitions and thermodynamic forces; the selected formulation fixes whether temperature, electric-field, and other contributions are included in those forces. The closure provider records the species basis, constraint equations, correlation structure, and units.

Self-diffusion coefficients, collective mutual diffusion coefficients, tracer diffusion, and electrical transport coefficients have separately defined identifiers and state domains.

## 11. Viscous and Thermal Transport

For a stationary equilibrium system at temperature `T > 0` and volume `V > 0`, a shear-viscosity Green–Kubo relation for a selected off-diagonal pressure-tensor component is:

`eta = V / (k_B T) integral_(0→infinity) <delta_P_xy(0) delta_P_xy(tau)> d tau`.

For an isotropic system with total heat-current vector `J_Q`, a thermal-conductivity relation is:

`kappa = 1 / (3 k_B T^2 V) integral_(0→infinity) <J_Q(0) · J_Q(tau)> d tau`.

Both equations are associated with their current and stress definitions, ensemble, sampling schedule, and convergence conditions. The coefficient identifiers retain their physical units, for example `Pa*s` for dynamic viscosity and `W/(m*K)` for thermal conductivity in SI units.

The energy and stress evaluators and molecular trajectory records provide typed source observables for independently declared current and correlation estimators.

## 12. Thermal Diffusivity and Unit Relations

For an isotropic continuum with thermal conductivity `kappa`, mass density `rho > 0`, and positive specific heat capacity `c_p` under the selected thermodynamic convention, define:

`alpha_T = kappa / (rho c_p)`.

The SI dimensions are:

| Quantity | SI unit |
| --- | --- |
| Species self-diffusion coefficient | `m^2/s` |
| Thermal diffusivity | `m^2/s` |
| Dynamic viscosity | `Pa*s` |
| Thermal conductivity | `W/(m*K)` |
| Electrical conductivity | `S/m` |

A unit or derived-coefficient mapping records its exact physical definition and dimensional conversion. For a `TransportCoefficientTransferRecord`, the source and target share one `coefficient_id`; transformations between different coefficient identities are expressed by their corresponding derived-observable operators before registration.

## 13. Three-Dimensional Anisotropic Transport

For an anisotropic diffusive system, introduce a rank-two diffusion tensor:

`D_ab = lim_(tau→infinity) <Delta_r_a(tau) Delta_r_b(tau)> / (2 tau)`.

A linear constitutive relation may take the form:

`j_a = -sum_b D_ab partial_b c`.

Under an orthogonal coordinate transformation `Q in O(3)`, the tensor transforms as:

`D' = Q D Q^T`.

The present `TransportCoefficient` stores one finite scalar per record. A tensor representation can be expressed through an explicitly identified component collection and ordering, with an associated tensor transformation and reconstruction contract. A scalar isotropic coefficient is registered with its scalar state-domain definition.

## 14. Finite Sampling and Statistical Estimation

A transport-coefficient estimate specifies the trajectory ensemble and its production interval. With sampled lag values `tau_l`, a multi-origin estimator of the velocity correlation can be written:

`C_v(l) = (1/(N_s |O_l|)) sum_(t_0 in O_l) sum_(i in I_s) v_i(t_0) · v_i(t_0 + tau_l)`.

`O_l` is the declared set of valid origins at lag `l`. The estimator records origin count, sampling interval, integration or fitting window, particle count, statistical weighting, and finite-time response.

Independent trajectories, block averaging, and correlation-aware uncertainty estimates use explicitly defined sample groupings. Convergence comparisons preserve the physical observation time, ensemble, and estimator when changing timestep or sample count.

## 15. Periodic Geometry and Finite-Size Mapping

Periodic transport studies specify the cell matrix, image-selection rule, coordinate unwrapping procedure, and the cell-size dependence of the selected estimator. For displacement observables, continuous Cartesian displacement reconstruction is associated with image counters or an equivalent trajectory history.

A periodic finite-size correction may be represented as a declared mapping:

`D_target = M_size(D_cell, B, T, eta; C_size)`.

The source register `docs/references/molecular_dynamics_sources.md` includes the Yeh–Hummer finite-size treatment for its specified cubic-cell hydrodynamic domain. A provider implementing that treatment records cell length, temperature, viscosity, geometrical factors, and the reference relation used.

The raw simulation coefficient and the corrected coefficient carry separately identifiable source, method, and normalization metadata.

## 16. Source-to-Target State Correspondence

Let the source and target physical states be `X_s` and `X_t`. A coefficient mapping uses an explicit state correspondence:

`X_t = M_state(X_s; context_state)`.

The material mapping identifies its selected variables, which may include temperature, pressure, composition, physical phase, geometry, local structure, external fields, and boundary fluxes. The coefficient transfer is then evaluated with that correspondence and its numerical parameters.

For a material evolving in time, the mapping schedule identifies both the source coefficient evaluation interval and the target closure update time. State, source, and target domains are retained through the corresponding `TransportCoefficient` fields.

## 17. Structural Coarse-Graining and Mesoscale Transport

`MultiscalePartition` maps each fine entity to one coarse group. `reduce_scalar_sum`, `reduce_vector_sum`, and `mass_weighted_vector_average` supply additive and weighted structural reductions for quantities with their declared meaning.

A transport transfer provider can use coarse positions, masses, velocities, and internal variables as context for a selected constitutive closure. For a coarse control volume `Omega_c`, a flux balance has the general form:

`d/dt integral_(Omega_c) a dV = -integral_(partial Omega_c) J_a · n dA + integral_(Omega_c) s_a dV`.

The provider specifies the flux law and its coefficient, including structural correlations and subscale contributions if present in the model. `MesoscaleClosureRecord` binds the resulting coarse-state and closure-variable identities.

## 18. Continuum and Engineering Transfer

`ContinuumClosureRecord` stores a mesoscale record, named continuum variables, auxiliary inputs, and closure provenance. A selected continuum constitutive law associates the transferred coefficient with its target transport flux and state domain.

`EngineeringBoundaryRecord` binds continuum variables to explicitly identified engineering boundary conditions. For thermal or material transport, those conditions may prescribe field values, fluxes, exchange coefficients, or coupled boundary laws under a selected physical sign convention.

The coefficient-transfer context identifies how the atomistic or mesoscale property enters the continuum or engineering law. Its output preserves source, target, and context together with the downstream closure identifiers in the reproducibility trace.

## 19. Thermodynamic and Uncertainty Coupling

`ThermodynamicVariable` associates a finite value with its unit, source, scale, and state domain. `ThermodynamicConsistencyContext` identifies the selected relation, model, assumptions, and normalization used to compare thermodynamic quantities across scales.

`UncertaintyMeasure` and `UncertaintyPropagationContext` provide typed numerical uncertainty records and their selected correlation and propagation method. A coefficient transfer may construct a corresponding target uncertainty through the declared propagation evaluator.

For a differentiable coefficient map `y = f(x)` and source covariance `C_x`, a first-order covariance propagation is:

`C_y ≈ J C_x J^T`.

Here `J` is the Jacobian of the specified mapping at its declared evaluation state. Data uncertainty, finite sampling, numerical integration, and model-parameter dependence are represented by their individually identified source quantities and propagation procedures.

## 20. Resonance and Balanced-Ternary Conditioning

TR-EIF associates atomistic evolution with continuous resonance dynamics and the balanced-ternary execution layer. For directed Kuramoto–Sakaguchi coupling, a receiving-node phase equation is:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A conditioned trajectory can be produced through:

`continuous resonance descriptor → execution request → guarded -1/0/1 event → retained execution → conditioned interatomic energy → forces → mechanical trajectory`.

The active-neutral execution state `0` supports its specified routing, balancing, mediation, damping, transition-staging, retention, and controlled-neutralization functions. Requested targets, pending destinations, holds, and committed events preserve distinct records.

A transport source calculated from such a trajectory identifies the resonance and execution parameters and the event order used to generate its mechanical samples. A transfer provider may include these continuous and categorical conditioning inputs in its state and constitutive mapping.

## 21. FLiBe Material-Specific Transport

A FLiBe transport entry identifies the LiF–BeF2 composition, transported species or collective quantity, temperature, pressure, structural state, observable definition, measurement or computational method, and source provenance.

The exact formula-unit ratio `2 LiF : 1 BeF2`, nominal `67 mol% LiF : 33 mol% BeF2`, and measured specimen composition are registered through their individual definitions. Material-state correspondence is evaluated with the source-specific composition and thermodynamic variables.

Li, Be, and F self-diffusion are indexed by species. Hydrogen-isotope transport of H, D, or T uses its own species, solubility, diffusivity, and permeation definitions; cross-property conversions use a declared constitutive relation and its boundary conditions.

The repository's `docs/references/flibe_sources.md` and `docs/references/molecular_dynamics_sources.md` provide registered source and method identities for material-specific transfer studies.

## 22. Executable Numerical Fixture

The integration test `tests/integration/test_multiscale_transport_transfer.py` constructs the source coefficient:

`TransportCoefficient(coefficient_id="thermal_conductivity", value=2.5, unit="W/(m*K)", scale_id="atomistic", state_domain_id="state-a", source_id="source-a")`.

Its transfer context is:

`TransportTransferContext(target_scale_id="mesoscale", mapping_id="mapping-a", normalization_id="normalization-a", assumptions_id="assumptions-a")`.

The fixture evaluator returns:

`TransportCoefficient(coefficient_id="thermal_conductivity", value=1.75, unit="W/(m*K)", scale_id="mesoscale", state_domain_id="state-b", source_id="source-b")`.

The test checks that the returned record binds this target to the exact input source and context. It also checks coefficient identity, target-scale agreement, identifier normalization, finite scalar validation, and deterministic repetition.

The numerical source and target values are the values specified by the test evaluator.

## 23. Exact Invariants and Numerical Qualification

The executable structural checks include:

- normalized nonempty coefficient, unit, scale, state-domain, and source identifiers;
- one finite real scalar per coefficient, with Boolean values excluded;
- normalized nonempty target-scale, mapping, normalization, and assumptions identifiers;
- `TransportCoefficient` source and target fields in every transfer record;
- a typed `TransportTransferContext` field;
- exact equality of source and target `coefficient_id`;
- exact equality of target `scale_id` and `context.target_scale_id`;
- equality of returned source and context to the supplied evaluator inputs;
- deterministic output for identical inputs under a deterministic provider.

Numerical coefficient qualification specifies the source correlation or constitutive calculation, unit conversion, physical-state matching, regression or quadrature interval, statistical procedure, uncertainty, and predeclared numerical tolerances. Exact identifiers and categorical execution-state invariants use exact equality.

## 24. Reproducibility Record

A reproducible transport-coefficient transfer records:

- source coefficient ID, numerical value, unit, source scale, state domain, and provenance;
- transported species or collective observable, composition, temperature, pressure, and material conditions;
- source trajectories and correlation or displacement estimator when coefficient estimation uses MD;
- time-origin and sampling policies, statistical weighting, cutoff or integration interval, and uncertainties;
- geometry, periodic-image and finite-size conventions where applicable;
- transfer method, normalization, target scale, and resolved assumptions identifiers;
- source-to-target thermodynamic and structural state mapping;
- closure-provider identity, target coefficient, target units, state domain, and source ID;
- resonance descriptors and committed ternary events when included in the source trajectory generation;
- numerical checks, deterministic replay inputs, and target continuum or engineering interfaces.

The returned `TransportCoefficientTransferRecord` maintains the source–target–context association for subsequent scale transitions.

## 25. Executable Interface Index

| Role | Repository path |
| --- | --- |
| Transport coefficient, context, record, evaluator | `src/tr_eif/multiscale/transport_transfer.py` |
| Single-origin MSD and VACF | `src/tr_eif/md/transport.py` |
| Molecular trajectory and stored states | `src/tr_eif/md/trajectory.py` |
| Mechanical state and coordinates | `src/tr_eif/md/state.py` |
| Periodic-image geometry | `src/tr_eif/geometry/periodic.py` |
| Atomistic energy model | `src/tr_eif/energy/model.py` |
| Stress evaluation | `src/tr_eif/energy/stress_evaluator.py` |
| Fine-to-coarse partition | `src/tr_eif/multiscale/partition.py` |
| Scalar and vector reductions | `src/tr_eif/multiscale/reduction.py`, `src/tr_eif/multiscale/vector_reduction.py` |
| Mass-weighted vector averages | `src/tr_eif/multiscale/vector_average.py` |
| Mesoscale closure | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Continuum closure | `src/tr_eif/multiscale/continuum_closure.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Engineering boundary records | `src/tr_eif/multiscale/engineering_boundary.py` |
| Resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| Ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| FLiBe multiscale hierarchy | `src/tr_eif/flibe/multiscale_coolant.py` |

## 26. Existing Test Interfaces

| Domain | Repository test path |
| --- | --- |
| Transport transfer and provider binding | `tests/integration/test_multiscale_transport_transfer.py` |
| Molecular transport observables | `tests/integration/test_molecular_dynamics_transport.py` |
| Cross-scale record chain | `tests/integration/test_multiscale_cross_scale_validation.py` |
| Thermodynamic consistency | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Uncertainty propagation | `tests/integration/test_multiscale_uncertainty_propagation.py` |
| Mesoscale closure | `tests/integration/test_multiscale_mesoscale_closure.py` |
| Continuum closure | `tests/integration/test_multiscale_continuum_closure.py` |
| Engineering boundaries | `tests/integration/test_multiscale_engineering_boundary.py` |
| FLiBe multiscale coolant | `tests/integration/test_flibe_multiscale_coolant_closure.py` |

These tests exercise source and target coefficient identities, explicit mapping contexts, provider input binding, source-state records, deterministic evaluation, microscopic transport series, and downstream closure interfaces.

## 27. Chapter Integration

Transport coefficient transfer in TR-EIF combines a named source coefficient, a physical-state and scale mapping, and a typed evaluator that returns the target coefficient with its full provenance. The executable record preserves source identity, destination scale, units, state domains, and method context.

Microscopic displacement and time-correlation procedures, mesoscopic constitutive variables, continuum flux laws, engineering boundaries, thermodynamic consistency, uncertainty propagation, continuous resonance, and balanced-ternary execution are connected through explicitly selected operators and recorded sampling and event schedules.
