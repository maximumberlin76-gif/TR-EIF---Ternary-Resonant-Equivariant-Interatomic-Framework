
# Volume 05 — Molecular Dynamics: Summary

## 1. Scope

Volume 05 specifies molecular-dynamics evolution within the Ternary Resonant Equivariant Interatomic Framework (TR-EIF). Its system class is an open nonlinear dissipative dynamical system with three-dimensional atomic geometry, continuous mechanical and resonance variables, and a separately defined balanced-ternary execution layer.

The volume organizes the computational chain:

`atomic configuration → interaction geometry → conditioned interatomic energy → forces → mechanical integration → trajectory → observables`.

The coupled resonance and execution chain is:

`atomic interaction graph → continuous phase evolution → resonance descriptor → execution request → active-neutral routing → retained -1/0/1 execution → conditioned interatomic computation`.

The requested and executed ternary variables, mechanical coordinates, and resonance phases retain their respective state spaces. The update schedule specifies how the two chains exchange information.

## 2. Chapter Structure

| Chapter | Subject | Principal objects and operations |
| --- | --- | --- |
| 01 — Equations of Motion | Mechanical state and balance equations | Positions, velocities, masses, force operators, continuous energy balance |
| 02 — Time Integrators | Numerical time advancement | Velocity-Verlet, explicit phase Euler, composition schedule, timestep refinement |
| 03 — Thermostats and Barostats | Thermal and volumetric coupling | Kinetic temperature, velocity rescaling, isotropic cell scaling, exchange records |
| 04 — Periodic Boundary Conditions | Three-dimensional cell and image geometry | Fractional coordinates, periodic images, cutoff graph, cell transformation |
| 05 — Neighbor Lists | Candidate interactions and rebuilding | Cutoff plus skin, canonical pairs, rebuild decision, directed graph extraction |
| 06 — Resonance State Propagation | Continuous oscillator dynamics | Directed Kuramoto–Sakaguchi coupling, wrapped phase integration, descriptors |
| 07 — Ternary State Propagation | Balanced-ternary execution | Active neutral, retained and pending states, guarded committed routes |
| 08 — Energy Conservation | Energy and exchange accounting | Kinetic and potential energy, force gradients, trajectory energy, event balances |
| 09 — Transport Observables | Trajectory-derived transport quantities | Mean-squared displacement, velocity autocorrelation, diffusion and scale transfer |

The nine chapters provide definitions, equations, executable interfaces, numerical examples, and verification contracts for their respective operators.

## 3. Atomistic Mechanical State

For `N >= 1` atoms with fixed inventory over one mechanical integration interval, define:

`R(t) = (r_1(t), ..., r_N(t))`, with `r_i(t) in R^3`.

`V(t) = (v_1(t), ..., v_N(t))`, with `v_i(t) in R^3`.

`M = (m_1, ..., m_N)`, with `m_i > 0`.

Species, optional cell vectors, and periodic-axis flags are retained in the atomic configuration. The reference `MolecularDynamicsState` contains the configuration, velocity tuple, mass tuple, integer step, and physical time.

The mechanical evolution is governed by:

`d r_i / dt = v_i`.

`m_i d v_i / dt = F_i`.

For a declared force decomposition:

`F_i = F_i^cons + F_i^ext + F_i^diss + F_i^boundary`.

External and boundary terms are supplied through explicitly selected physical operators and control-volume conventions. Particle-exchange events additionally specify inventory and flux updates.

## 4. Conditioned Energy and Mechanical Forces

The interatomic energy is a scalar constructed from three-dimensional atomic configuration, directed interaction graph, node features, model parameters, and the retained ternary execution vector:

`E_pot = E(R, G, Q, sigma; Theta)`.

The executable `ReferenceEnergyModel.evaluate` applies ternary-conditioned equivariant features and an invariant scalar energy functional. For an atomic scalar-channel vector `phi_i`, the reference aggregation is:

`E_i = b + sum_a w_a phi_(i,a)`.

`E_pot = sum_i E_i`.

On a differentiable coordinate branch, holding the specified conditioning inputs fixed during differentiation:

`F_i^cons = -grad_(r_i) E_pot`.

`ConservativeForceEvaluator` approximates each Cartesian derivative with a central coordinate difference of positive increment `h`:

`F_(i,d) ≈ -[E(R + h e_(i,d)) - E(R - h e_(i,d))] / (2h)`.

Each derivative evaluation retains its supplied interaction graph, node features, and executed ternary vector. The graph-construction schedule determines the geometry evaluated at later mechanical steps.

## 5. Numerical Mechanical Time Evolution

For mechanical step `dt_MD > 0`, the reference velocity-Verlet formulas are:

`r_i[n+1] = r_i[n] + dt_MD v_i[n] + (dt_MD^2 / 2) a_i[n]`.

`v_i[n+1] = v_i[n] + (dt_MD / 2)(a_i[n] + a_i[n+1])`.

`a_i[n] = F_i[n] / m_i`.

`velocity_verlet_step` builds the initial interaction graph, evaluates initial forces, advances positions, builds the graph at the new positions, reevaluates forces, and completes the velocity update. The result retains both endpoint graphs and force states.

`run_velocity_verlet_trajectory` composes these steps. A trajectory with `L` completed mechanical steps contains `L + 1` ordered mechanical states, including its initial state. The trajectory runner receives a fixed execution vector and feature vector for its invocation.

For a smooth position-dependent force field on a fixed finite interval, standard fixed-step velocity-Verlet exhibits second-order global trajectory convergence under the corresponding regularity and stability assumptions. Force-difference resolution, cutoff geometry, and event placement enter the numerical study as separately recorded parameters.

## 6. Periodic Geometry and Interaction Graphs

For ordered cell vectors `a`, `b`, and `c`, define `B = [a b c]` and:

`V_cell = |det(B)|`.

Fractional and Cartesian coordinates satisfy:

`r = B q`.

`q = B^(-1) r`.

For source–receiver displacement `d = r_j - r_i`, the executable periodic image convention uses fractional components `u = B^(-1) d` and image indices:

`k_l = -floor(u_l + 0.5)` for each enabled periodic axis `l`.

`k_l = 0` for each other axis.

The selected displacement is:

`d_ij = B(u + k)`.

This componentwise fractional rule and the periodic-axis flags define the image selection recorded by the reference. The graph builder includes each ordered pair at squared selected distance `|d_ij|^2 <= r_c^2`, retaining the directed image index. The cell basis and image convention are part of the geometrical input contract, including for skewed cells.

## 7. Neighbor-List Snapshot and Rebuild

Let `r_c > 0` be the interaction cutoff and `s_skin >= 0` the skin. Neighbor-list construction uses:

`r_search = r_c + s_skin`.

`build_neighbor_list` retains an ordered tuple of unique canonical candidate pairs `(i, j)` with `i < j` from the reference configuration at the search radius.

A snapshot rebuild is requested when atom count, species, periodic flags, or cell geometry changes, or when at least one selected reference-to-current atomic displacement satisfies:

`|delta_i|^2 > (s_skin / 2)^2`.

For a retained snapshot, `interaction_graph_from_neighbor_list` reevaluates candidate-pair distances at `r_c` and produces directed current edges and periodic images. The existing `velocity_verlet_step` uses direct `build_cutoff_graph` calls at its two mechanical endpoints; neighbor-list operations are separately exposed for a caller-defined schedule.

## 8. Kinetic Temperature and Thermal Events

The kinetic energy is:

`K = (1/2) sum_i m_i |v_i|^2`.

For a declared number `f` of translational degrees of freedom and consistent Boltzmann constant `k_B`, the kinetic-temperature estimator is:

`T_kin = 2 K / (f k_B)`.

For `T_current > 0`, deterministic rescaling to a nonnegative target uses:

`lambda_T = sqrt(T_target / T_current)`.

`v_i,after = lambda_T v_i,before`.

`K_after = lambda_T^2 K_before`.

The kinetic-energy increment for this event is:

`Delta_K_thermal = K_after - K_before`.

`rescale_to_kinetic_temperature` changes velocities and retains positions, cell, masses, mechanical step, and mechanical time. The zero-temperature branches follow the explicit contract in Chapter 03 and `velocity_rescaling_factor`.

## 9. Pressure Coupling and Three-Dimensional Cell Evolution

The reference isotropic pressure-coupling relation is:

`mu_V = 1 - (dt / tau_p) beta (P_target - P_current)`.

`s = mu_V^(1/3)`, with `mu_V > 0`.

For a fully periodic three-dimensional configuration:

`B_after = s B_before`.

`r_i,after = s r_i,before`.

`V_after = mu_V V_before`.

`apply_isotropic_barostat` updates cell vectors and positions while retaining velocities, masses, MD step, and MD time. The calculation supplies current pressure, target pressure, compressibility, timestep, and coupling time. Cell-work accounting uses a declared pressure and sign convention, with the geometry and energy observations recorded before and after scaling.

## 10. Continuous Resonance Propagation

Associate one oscillator with each atom. Let `theta_j` be its phase, `omega_j` its retained intrinsic angular frequency, `kappa_j >= 0` its receiving-node coupling, and `gamma_j` its receiving-node phase lag.

For the directed graph sampled from the selected atomic configuration, the reference Kuramoto–Sakaguchi vector field is:

`d theta_j / dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

`euler_step` evaluates the full derivative from one input resonance state and advances phases using:

`theta_j,next = wrap(theta_j + dt_R d theta_j/dt)`.

`omega_j,next = omega_j`.

The wrapper maps angles into `[0, 2π)`. `propagate_md_resonance_state` samples the MD interaction graph and returns the previous and current resonance states together with the retained input MD state, graph, cutoff, and `dt_R`.

A global phase-order observable and frequency-spread descriptor are:

`R_phase = |(1/N) sum_j exp(i theta_j)|`.

`spread_omega = sqrt((1/N) sum_j (omega_j - omega_mean)^2)`.

Resonance-window classification, oscillator phase, mechanical material state, and physical phase of matter are represented by individually defined operators and state variables.

## 11. Balanced-Ternary State Propagation

Each atom-associated execution node retains:

`X_T,i = (sigma_i, p_i)`.

The executed state belongs to `{-1, 0, 1}` and is written canonically as `-1/0/1`. State `0` is active neutral, supporting routing, balancing, mediation, damping, transition staging, retention, and controlled neutralization under the declared operators.

The pending destination `p_i` belongs to `{-1, 1}` or is `None`, with the exact invariant:

`p_i != None implies sigma_i = 0`.

The committed transition relation is:

`R_T = {(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 0), (1, 1)}`.

Opposite-polarity requests follow separate committed legs:

`-1 → 0 → 1`.

`1 → 0 → -1`.

A guard-held opportunity has `route = None` and retains its execution state. A committed self-transition has an explicit `route` and contributes to the committed-event count. Active-neutral retention can span multiple execution opportunities.

`propagate_md_ternary_state` advances the vector through `execute_ternary_vector_step` and returns committed and held event counts while retaining the supplied MD mechanical state. `ReferenceEnergyModel.evaluate` and `velocity_verlet_step` accept the retained execution vector selected by the caller.

## 12. Mechanical and Exchange-Inclusive Energy Balances

The total mechanical energy is:

`H = K + E_pot`.

For smooth conservative motion with fixed masses, fixed cell, and fixed conditioning:

`F_i = -grad_(r_i) E_pot`.

`dH/dt = 0`.

For continuously evolving conditioning `A`, cell `B`, explicitly time-dependent potential, and supplied nonconservative forces, the chain-rule balance is:

`dH/dt = sum_i v_i · F_i^nc + partial_t E_pot + (partial_B E_pot) : (dB/dt) + (grad_A E_pot) · (dA/dt)`.

The selected open-system control volume also registers heat, external work, and material fluxes according to its declared energy-storage and boundary-exchange convention.

For an execution-conditioning event at fixed geometry, an associated energy difference is:

`Delta_E_exec = E_pot(R, G, Q, sigma_after) - E_pot(R, G, Q, sigma_before)`.

Thermal, volumetric, and execution events retain their before/after states and accounting fields. A discrete trajectory balance can be written using declared contributions:

`R_balance = (H_final - H_initial) - (W_forces + W_cell + Q_thermal + J_boundary + W_conditioning)`.

`evaluate_trajectory_energy` constructs ordered kinetic, potential, and total-energy observations for the stored mechanical trajectory. The reference conservation tests include an explicit short-trajectory energy-change bound with fixed numerical parameters.

## 13. Time-Dependent Transport Observables

The executable `mean_squared_displacement` computes the all-atom, initial-origin mean-squared displacement for the stored nonperiodic mechanical trajectory:

`MSD_0(tau) = (1/N) sum_i |r_i(t_0 + tau) - r_i(t_0)|^2`.

`velocity_autocorrelation` computes the all-atom, initial-origin velocity correlation:

`C_v,0(tau) = (1/N) sum_i v_i(t_0) · v_i(t_0 + tau)`.

Both return ordered elapsed-time series. Periodic displacement analysis uses an explicitly reconstructed unwrapped position history; the reference MSD function enforces its nonperiodic input contract. VACF uses the supplied Cartesian velocity history, including for periodic mechanical configurations.

For a stationary isotropic three-dimensional diffusive regime, the chapter defines the Einstein and Green–Kubo self-diffusion relations:

`D_self = lim_(tau→infinity) MSD(tau) / (6 tau)`.

`D_self = (1/3) integral_(0→infinity) C_v(tau) d tau`.

Coefficient calculations specify their sampling origins, time window, species selection, equilibrium or open-system state conditions, numerical estimator, and uncertainty procedure. Transport-coefficient transfer across scales is represented by the typed interfaces in `src/tr_eif/multiscale/transport_transfer.py`.

## 14. Coupled Mechanical, Resonance, and Execution Clocks

A coupled trajectory identifies its mechanical step index `n`, resonance integration index `j`, and ternary execution-opportunity index `k`.

An explicitly selected composition may take the form:

`X_MD[n+1] = Phi_MD(X_MD[n], dt_MD; sigma[k])`.

`X_R[j+1] = Phi_R(X_R[j], dt_R; G_sample, P_R)`.

`q[k] = M_request(X_MD, X_R, context)`.

`X_T[k+1] = U_exec(X_T[k], q[k], guards[k])`.

`sigma[k+1] = retained(X_T[k+1])`.

The model selects the sampling instants, parameter updates, graph recomputation points, and execution vector used for each force evaluation. Thermal and cell-scaling events are added at their declared positions in this sequence. The state and trace retain each event index and its associated physical time.

Continuous mechanical and oscillator variables retain their numerical evolution, while the balanced-ternary operator manages exact discrete execution events.

## 15. Structural Invariants and Symmetry

The exact executable contracts include:

- one position, velocity, mass, node-feature record, and executed state per atom in the corresponding coupled operation;
- positive finite masses and positive finite integration timesteps;
- graph node count equal to the supplied atom count;
- sorted unique canonical neighbor-list candidate pairs;
- committed ternary routes belonging to `R_T`;
- pending destinations and active-neutral retained-state compatibility;
- distinct held and committed event records;
- mechanical step increment of one for each completed velocity-Verlet step;
- ordered trajectory state continuity and `L + 1` recorded states for `L` mechanical steps;
- retained intrinsic frequencies during the reference Euler phase update;
- deterministic ordering of source/receiver graph edges and stored event records.

Under a common rigid E(3) action with orthogonal matrix `Q` and translation `b`, Cartesian positions transform as `r_i' = Q r_i + b`, and velocities and forces transform as `v_i' = Q v_i` and `F_i' = Q F_i` under the corresponding model covariance assumptions.

Scalar energy, displacement norms, and velocity dot products obey their specified invariant transformation laws. Cell and periodic-image geometry use the same transformed physical configuration and declared image convention.

## 16. Numerical Reproducibility Record

A reproducible MD study specifies:

- atomic species, ordered positions, velocities, masses, cell vectors, and periodic-axis flags;
- model parameters, node features, interaction cutoff, and periodic image convention;
- coordinate-difference force increment and graph update policy;
- MD timestep sequence and initial/final physical times;
- neighbor-list skin, reference snapshots, and rebuild events where used;
- thermostat target and kinetic-temperature degrees of freedom;
- barostat pressure inputs, compressibility, coupling time, and cell transform;
- resonance phases, intrinsic frequencies, couplings, phase lags, graph-sampling instants, and integration steps;
- requested targets, retained and pending execution states, guards, and committed/held event order;
- energy observations, exchange-accounting convention, and selected balance residuals;
- displacement and velocity histories, sampling conventions, and transport observables;
- numerical tolerance definitions, convergence comparisons, test fixtures, and output provenance.

Exact discrete invariants use exact equality. Numerical coordinate, force, energy, and transport comparisons use the declared methods, units, and fixed tolerances selected for each computation.

## 17. Executable Reference Index

| Role | Repository path |
| --- | --- |
| Atomic MD state | `src/tr_eif/md/state.py` |
| Mechanical integrator | `src/tr_eif/md/integrator.py` |
| Force-driven mechanical step | `src/tr_eif/md/execution.py` |
| Mechanical trajectory | `src/tr_eif/md/trajectory.py` |
| Kinetic and total energy observables | `src/tr_eif/md/observables.py` |
| Trajectory energy observations | `src/tr_eif/md/trajectory_observables.py` |
| Coordinate-derived forces | `src/tr_eif/energy/force_evaluator.py` |
| Conservative stress evaluation | `src/tr_eif/energy/stress_evaluator.py` |
| Periodic geometry | `src/tr_eif/geometry/periodic.py` |
| Directed cutoff graph | `src/tr_eif/graph/builder.py` |
| Neighbor-list snapshots | `src/tr_eif/md/neighbor_list.py` |
| Kinetic-temperature coupling | `src/tr_eif/md/thermostat.py` |
| Isotropic cell coupling | `src/tr_eif/md/barostat.py` |
| MD-associated resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| Phase dynamics and integration | `src/tr_eif/resonance/dynamics.py`, `src/tr_eif/resonance/integrator.py` |
| MD-associated ternary propagation | `src/tr_eif/md/ternary_propagation.py` |
| Vector ternary execution | `src/tr_eif/ternary/vector_execution.py` |
| Conditioned energy evaluation | `src/tr_eif/energy/model.py` |
| Molecular transport observables | `src/tr_eif/md/transport.py` |
| Transport-coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |

## 18. Test and Validation Index

| Domain | Existing test path |
| --- | --- |
| Mechanical step | `tests/integration/test_molecular_dynamics_step.py` |
| Mechanical trajectory | `tests/integration/test_molecular_dynamics_trajectory.py` |
| Kinetic-temperature coupling | `tests/integration/test_molecular_dynamics_thermostat.py` |
| Isotropic pressure coupling | `tests/integration/test_molecular_dynamics_barostat.py` |
| Neighbor-list construction | `tests/integration/test_molecular_dynamics_neighbor_list.py` |
| Resonance propagation | `tests/integration/test_molecular_dynamics_resonance_propagation.py` |
| Ternary execution propagation | `tests/integration/test_molecular_dynamics_ternary_propagation.py` |
| MD energy observables | `tests/conservation/test_md_energy_observables.py` |
| Trajectory energy and drift | `tests/conservation/test_md_trajectory_energy.py` |
| Force-gradient consistency | `tests/conservation/test_force_gradient_consistency.py` |
| Stress consistency | `tests/conservation/test_stress_consistency.py` |
| Transport observables | `tests/integration/test_molecular_dynamics_transport.py` |
| Geometric invariants | `tests/invariants/test_geometry_invariants.py` |
| Ternary transition invariants | `tests/invariants/test_ternary_transition_invariant.py` |
| Ternary vector execution invariants | `tests/invariants/test_ternary_vector_execution.py` |
| Multiscale transport transfer | `tests/integration/test_multiscale_transport_transfer.py` |

The existing `TR-EIF Python CI` runs package compilation, public-package imports, deterministic/conservation/numerical checks, structured-output checks, and the complete repository pytest suite through its respective jobs. `TR-EIF Markdown Validation` is a separate manual workflow using the repository Markdown contract.

## 19. Volume Integration

Volume 05 connects the mathematical state spaces of Volume 01, the continuous resonance and active-ternary semantics of Volume 02, the equivariant interatomic energy and force operators of Volume 03, and the model parameters and training interfaces of Volume 04.

The resulting molecular-dynamics layer supplies trajectories, geometric interaction histories, phase and execution event records, energy and boundary-exchange observations, and transport time series. These records are typed inputs to material-specific calculations and cross-scale mappings, including the FLiBe reference model and transport-coefficient transfer interfaces.

The volume's complete computational sequence is:

`initial atomistic state → graph and energy inputs → force integration → mechanical trajectory → resonance and ternary events → thermal and boundary exchange → energy and transport observables → reproducibility record`.
