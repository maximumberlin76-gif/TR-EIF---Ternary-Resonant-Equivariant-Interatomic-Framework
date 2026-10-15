
# Transport Observables

## 1. Scope and System Class

This chapter specifies time-dependent transport observables for molecular dynamics in TR-EIF and their interfaces with continuous resonance evolution, balanced-ternary execution, and multiscale material models.

The reference system class is an open nonlinear dissipative dynamical system. Its atomistic realization supplies three-dimensional coordinates, velocities, masses, species, boundary geometry, and a declared physical time sequence. Statistical observables are constructed from these trajectories using explicit sampling and normalization operators.

The current Python implementation provides `mean_squared_displacement` and `velocity_autocorrelation` in `src/tr_eif/md/transport.py`. Both consume an ordered `MolecularDynamicsTrajectory` and return immutable elapsed-time series.

## 2. Mechanical Trajectory and Time Coordinates

Let `N >= 1` be the atom count, `r_i[n] in R^3` the Cartesian position of atom `i`, `v_i[n] in R^3` its velocity, and `m_i > 0` its mass at mechanical state index `n`.

The trajectory is represented by:

`X_MD[n] = (S, R[n], V[n], M, C[n], P[n], step[n], t[n])`.

Here `S` is the ordered species tuple, `C[n]` the optional cell, and `P[n]` the periodic-axis flags. `MolecularDynamicsTrajectory` stores an ordered tuple of mechanical step results. For `L` completed steps, its `states` property contains `L + 1` mechanical states, including the initial state.

The transport time coordinate uses the initial state as origin:

`tau[n] = t[n] - t[0]`.

The series therefore begins at `tau[0] = 0`. The reference validates equal atom cardinality through the trajectory structure and requires the species tuple and atomic masses to remain unchanged across the states supplied to each transport operator. Per-index atomic identity follows the trajectory's stored ordering.

## 3. Transport-Series Data Structures

`MeanSquaredDisplacementSeries` stores `(times, values)` where each value is finite and nonnegative. `VelocityAutocorrelationSeries` stores the same tuple structure with finite, signed correlation values.

Both structures enforce:

- tuples for time and observable sequences;
- at least one time–value pair;
- equal sequence lengths;
- finite real values, excluding Boolean inputs;
- nonnegative elapsed times in strictly increasing order;
- floating-point normalization of accepted numeric inputs.

The `state_count` property equals the number of stored pairs. The series values and their meaning are specified by the selected observable operator.

## 4. Mean-Squared Displacement

For the currently implemented single-origin, all-atom observable, define the displacement of atom `i` from the initial stored coordinate:

`Delta_r_i(tau[n]) = r_i[n] - r_i[0]`.

The reference mean-squared displacement (MSD) is:

`MSD_0(tau[n]) = (1/N) sum_(i=1)^N |Delta_r_i(tau[n])|^2`.

Equivalently, in three Cartesian coordinates:

`|Delta_r_i|^2 = Delta_x_i^2 + Delta_y_i^2 + Delta_z_i^2`.

`mean_squared_displacement(trajectory)` evaluates this expression in atom-index order for each stored state. The initial value is exactly zero for finite identical reference and current coordinates. The output has units of length squared, using the length units of the supplied positions.

The operator uses the initial trajectory state as its sole time origin and equal atomic weights. The chosen atom subset, drift treatment, and origin-averaging convention can be declared in additional estimators as separate numerical operations.

## 5. Velocity Autocorrelation

For the same atom ordering and initial time origin, define:

`C_v,0(tau[n]) = (1/N) sum_(i=1)^N v_i[0] · v_i[n]`.

`velocity_autocorrelation(trajectory)` computes this per-atom mean Cartesian dot product at each stored state. Its initial value is:

`C_v,0(0) = (1/N) sum_i |v_i[0]|^2`.

The velocity autocorrelation (VACF) has units of length squared per time squared. Its values are signed; opposing initial and current velocities can produce negative correlations.

This executable definition uses equal atom weights, one initial time origin, and the supplied velocities. It establishes the exact normalization of the stored series for later statistical calculations.

## 6. Reference Three-State Calculation

The integration fixture in `tests/integration/test_molecular_dynamics_transport.py` contains two atoms with elapsed times:

`tau = (0.0, 0.25, 0.50)`.

The first atom moves from `(0, 0, 0)` through `(1, 0, 0)` to `(2, 0, 0)`. The second atom moves from `(1, 0, 0)` through `(1, 2, 0)` to `(1, 4, 0)`.

The resulting displacement series is:

`MSD_0 = (0.0, 2.5, 10.0)`.

The initial velocities are `(1, 0, 0)` and `(0, 2, 0)`. At the second state they are `(0.5, 0, 0)` and `(0, 1, 0)`; at the third state they are `(-1, 0, 0)` and `(0, -1, 0)`.

The velocity-correlation series is:

`C_v,0 = (2.5, 1.25, -1.5)`.

Both values and elapsed times are checked directly by the transport integration tests. The fixture supplies the states explicitly through ordered mechanical step records.

## 7. Periodic Coordinates and Displacement Histories

For a periodic cell `B(t)`, an image-resolved Cartesian position can be represented as:

`r_i,unwrapped(t) = r_i,wrapped(t) + B(t) k_i(t)`.

Here `k_i(t)` is an integer image-counter vector following the declared periodic-coordinate convention. For a changing cell, the selected coordinate reference frame and cell-deformation contribution are specified when reconstructing an unwrapped trajectory.

The current `mean_squared_displacement` function accepts trajectories with nonperiodic configurations throughout. A periodic configuration activates its explicit periodic-coordinate validation error. Periodic transport analysis supplies a separately defined unwrapped position history and displacement estimator with recorded image counters or an equivalent continuous coordinate reconstruction.

The reference `velocity_autocorrelation` accepts periodic trajectories because its input is the stored velocity sequence. It retains the supplied Cartesian velocity-frame convention and time ordering.

## 8. Species-Resolved and Collective Motion

For a selected species `s` with atom-index set `I_s` and positive count `N_s`, a species-resolved single-origin displacement statistic is:

`MSD_s(tau) = (1/N_s) sum_(i in I_s) |r_i(tau) - r_i(0)|^2`.

The corresponding velocity statistic is:

`C_v,s(tau) = (1/N_s) sum_(i in I_s) v_i(0) · v_i(tau)`.

These formulas define species selection and its normalization. The present `md/transport.py` operators average over the full stored atom tuple; a species-resolved evaluation introduces an explicit selection operation and tracks stable particle indices.

For multicomponent ionic systems, collective charge, mass, and species currents use their declared weighting, reference frame, and cross-correlation definitions. Individual species self-diffusion, collective diffusion, and transport of dissolved hydrogen isotopes are represented as separately identified material observables.

## 9. Einstein Relation for Translational Diffusion

For a stationary, isotropic three-dimensional diffusive regime, the long-time Einstein relation defines self-diffusion through the displacement growth rate:

`D_self = lim_(tau→infinity) MSD(tau) / (6 tau)`.

Under an established linear diffusive interval, an equivalent slope estimator is:

`D_self = (1/6) d(MSD)/d tau`.

In spatial dimension `d`, the corresponding isotropic denominator is `2d`. An anisotropic calculation uses a displacement-covariance tensor, with components:

`D_ab = lim_(tau→infinity) <Delta_r_a(tau) Delta_r_b(tau)> / (2 tau)`.

A numerical diffusion estimate declares its stationary-state sampling, coordinate reconstruction, fitting interval, time origins, ensemble averaging, and uncertainty procedure. The short-time ballistic contribution, where displacement can scale quadratically with time, is identified through the observed time dependence before selecting a diffusive interval.

## 10. Green–Kubo Diffusion Relation

For stationary equilibrium dynamics with the applicable correlation-decay and convergence conditions, define the ensemble- or time-origin-averaged three-dimensional velocity correlation:

`C_v(tau) = <v(0) · v(tau)>`.

The Green–Kubo representation of isotropic self-diffusion is:

`D_self = (1/3) integral_(0→infinity) C_v(tau) d tau`.

The `1/3` factor corresponds to the three Cartesian velocity components in the dot product. For an anisotropic medium, the diffusion tensor uses component correlations:

`D_ab = integral_(0→infinity) <v_a(0) v_b(tau)> d tau`.

The executable `VelocityAutocorrelationSeries` provides a single-origin discrete correlation history. Construction of a Green–Kubo coefficient additionally specifies origin averaging, quadrature, integration-window selection, statistical convergence, and treatment of finite observation times.

## 11. Time-Origin and Ensemble Averaging

For stored positions sampled at interval `dt_sample`, let `n0` denote a selected time origin and `ell` a lag index. A multi-origin MSD estimator is:

`MSD(ell) = (1/(N |O_ell|)) sum_(n0 in O_ell) sum_i |r_i[n0+ell] - r_i[n0]|^2`.

Here `O_ell` is the declared set of admissible origins for lag `ell`. An analogous velocity estimator is:

`C_v(ell) = (1/(N |O_ell|)) sum_(n0 in O_ell) sum_i v_i[n0] · v_i[n0+ell]`.

For species-specific estimates, replace the all-atom sum and normalization with the selected species index set. Ensemble averaging combines independent trajectory realizations using a declared weighting policy.

The current reference fixes `n0 = 0`. The multi-origin equations define the statistical extension while retaining the single-origin reference values as reproducible inputs.

## 12. Stress and Heat-Current Correlations

A wider transport calculation introduces stress and heat-current time series with explicitly declared microscopic operators. In a stationary equilibrium, an illustrative shear-viscosity Green–Kubo relation for the selected off-diagonal pressure-tensor component is:

`eta = V / (k_B T) integral_(0→infinity) <delta_P_xy(0) delta_P_xy(tau)> d tau`.

Here `V` is the equilibrium volume, `T` the thermodynamic temperature, and `delta_P_xy` the fluctuation about the selected mean under a specified stress convention.

For a three-dimensional isotropic system, a heat-current representation using the total heat-current vector `J_Q` is:

`kappa = 1 / (3 k_B T^2 V) integral_(0→infinity) <J_Q(0) · J_Q(tau)> d tau`.

The microscopic definitions of stress, heat current, and their partition among kinetic and interaction contributions follow the selected interatomic energy model and boundary convention. The repository provides energy and stress evaluators; transport-correlation definitions are constructed using their associated state and flux conventions.

## 13. Open-System Transport and Exchange

For a control volume `Omega` with boundary `partial Omega`, a species balance can be expressed as:

`d/dt integral_Omega c_s dV = -integral_(partial Omega) J_s · n dA + integral_Omega q_s dV`.

Here `c_s` is species concentration, `J_s` the total species flux, `n` the outward surface normal, and `q_s` the declared volumetric source or sink term. A decomposition with fluid velocity `u` is:

`J_s = c_s u + j_s`.

Under a selected isotropic Fickian closure, the diffusive contribution may be written:

`j_s = -D_s grad(c_s)`.

For multicomponent and charged media, the constitutive representation specifies cross-couplings, electrochemical driving forces, boundary exchange, and the chosen thermodynamic state variables. The microscopic trajectory, coarse-graining operator, and transport coefficient therefore belong to one declared state-domain and scale mapping.

## 14. Resonance and Ternary Coupling

Continuous phase dynamics and balanced-ternary execution can condition the interatomic model used to generate a mechanical trajectory:

`X_MD → G(R, C) → X_R → request → U_T → executed conditioning → E → F → X_MD,next`.

The resonance state `X_R` evolves through its continuous phase integrator; `U_T` advances retained execution nodes in `-1/0/1`, including active neutral `0`. The mechanical integrator advances Cartesian coordinates and velocities under the selected conditioned energy and force operators.

A coupled transport trace associates each sampled mechanical state with the graph, resonance state, requested targets, committed execution events, boundary controls, and physical time. Correlations and displacement histories are computed from the resulting mechanical records according to the specified statistical estimator.

## 15. Three-Dimensional Geometry and Symmetry

Under a common time-independent orthogonal transformation `Q in O(3)` and translation `b`, positions and velocities transform as:

`r_i' = Q r_i + b`.

`v_i' = Q v_i`.

The displacement norm and velocity dot product obey:

`|Q Delta_r_i|^2 = |Delta_r_i|^2`.

`(Q v_i[0]) · (Q v_i[n]) = v_i[0] · v_i[n]`.

Thus the scalar MSD and VACF calculations preserve their values under a common rigid spatial transformation of the full trajectory. Tensor transport quantities transform according to their corresponding tensor representations and the selected spatial frame.

## 16. Multiscale Transport-Coefficient Transfer

The multiscale package contains `TransportCoefficient`, `TransportTransferContext`, `TransportCoefficientTransferRecord`, and `evaluate_transport_coefficient_transfer` in `src/tr_eif/multiscale/transport_transfer.py`.

A `TransportCoefficient` records:

- `coefficient_id` and finite numerical `value`;
- `unit` and `scale_id`;
- `state_domain_id` and `source_id`.

`TransportTransferContext` records `target_scale_id`, `mapping_id`, `normalization_id`, and `assumptions_id`. The transfer evaluator receives a source coefficient and context and returns a record containing the same source, the same context, and the target coefficient at the requested scale.

The executable contract checks coefficient identity and destination-scale consistency. A chosen transfer provider supplies the constitutive mapping, numerical normalization, state-domain correspondence, and uncertainty propagation used for its target coefficient.

## 17. FLiBe Transport-State Identification

A FLiBe transport record identifies composition, chemical species, temperature, pressure, phase-state conditions, ionic or molecular transport observable, and its provenance. For example, Li, Be, and F self-diffusion are indexed separately; dissolved hydrogen-isotope transport uses its own species and constitutive identifiers.

The exact formula-unit ratio `2 LiF : 1 BeF2`, the nominal mixture `67 mol% LiF : 33 mol% BeF2`, and measured specimen composition are retained as separate composition records. Each source or prediction carries its own temperature, pressure, uncertainty, and preparation or simulation conditions.

The reference-source registers in `docs/references/flibe_sources.md` and `docs/references/molecular_dynamics_sources.md` provide the evidence and method provenance for transport-property studies.

## 18. Numerical Qualification and Reproducibility

A reproducible transport calculation records:

- atom order, species, masses, initial positions and velocities, and the trajectory state count;
- cell and periodicity history, with image reconstruction for periodic displacement statistics;
- mechanical timestep, recorded physical times, and transport sampling intervals;
- force, energy, graph, resonance, and executed ternary inputs used during trajectory generation;
- the chosen time origin or origin set, particle subset, statistical weights, and correlation normalization;
- diffusion fitting interval or Green–Kubo quadrature and integration interval where a coefficient is calculated;
- thermodynamic controls, boundary fluxes, ensemble assumptions, and units;
- numerical convergence study, replicate trajectories, and uncertainty estimator;
- provenance and scale-transfer identifiers for transported coefficients.

Exact checks cover series cardinality, unchanged per-index species and masses, finite values, time ordering, and the stored execution-state alphabet. Numerical checks cover source-coordinate arithmetic, dot products, geometric transformations, timestep refinement, and correlation or slope convergence under the declared methods and tolerances.

## 19. Executable Interfaces and Tests

| Role | Repository path |
| --- | --- |
| Mechanical trajectory and ordered states | `src/tr_eif/md/trajectory.py` |
| Mechanical state and particle fields | `src/tr_eif/md/state.py` |
| MSD and VACF series and evaluators | `src/tr_eif/md/transport.py` |
| MD namespace exports | `src/tr_eif/md/__init__.py` |
| Periodic image geometry | `src/tr_eif/geometry/periodic.py` |
| Periodic atomic configuration | `src/tr_eif/configuration/state.py` |
| Velocity-Verlet integration | `src/tr_eif/md/execution.py` |
| Molecular-dynamics kinetic energy | `src/tr_eif/md/observables.py` |
| Stress evaluation | `src/tr_eif/energy/stress_evaluator.py` |
| MD resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| MD ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| Multiscale transport transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Transport-observable integration tests | `tests/integration/test_molecular_dynamics_transport.py` |
| Multiscale transfer integration tests | `tests/integration/test_multiscale_transport_transfer.py` |

The MD transport tests cover MSD and VACF arithmetic, elapsed time, signed correlations, periodic-coordinate handling, invariant particle metadata, validation of series inputs, and deterministic repetition. The multiscale tests cover coefficient and context typing, explicit evaluator binding, source consistency, and destination-scale identity.

## 20. Summary

The current TR-EIF molecular-dynamics reference evaluates single-origin, all-atom mean-squared displacement and velocity autocorrelation from stored mechanical trajectories. Each observable retains its physical time coordinate and precisely defined arithmetic normalization.

Diffusion estimators, equilibrium time-correlation integrals, periodic-coordinate reconstruction, species-specific statistics, and cross-scale transport mappings are defined through separate mathematical and computational operators. Continuous resonance evolution and active `-1/0/1` execution enter through the explicitly selected interatomic trajectory-generation and event-order contracts.
