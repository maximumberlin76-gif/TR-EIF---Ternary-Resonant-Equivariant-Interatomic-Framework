
# Energy Conservation

## 1. Scope and System Class

This chapter specifies mechanical-energy observables, conservative evolution, exchange-inclusive energy balances, and numerical energy accounting for molecular dynamics in TR-EIF.

The system class is an open nonlinear dissipative dynamical system. Its atomistic representation combines continuous three-dimensional motion, graph-conditioned interatomic energy, continuous resonance variables, and balanced-ternary execution. Each component has its own state variables, update operators, and event record.

The executable reference provides kinetic and potential energy aggregation, coordinate-derived forces, velocity-Verlet trajectories, and ordered energy observations. Thermal coupling, isotropic cell scaling, resonance propagation, and ternary execution are exposed through separate operators.

## 2. Mechanical and Conditioning States

For `N >= 1` atoms, let `r_i(t) in R^3`, `v_i(t) in R^3`, and `m_i > 0` denote Cartesian position, velocity, and mass. Denote the atomic configuration by `C_atom`, the interaction graph by `G`, the cell matrix by `B` when present, and the node features by `Q`.

Let `sigma` be the retained balanced-ternary execution vector, with each executed component in `{-1, 0, 1}`. Let `X_R` denote the continuous resonance state and `A` collect the conditioning variables supplied to the energy functional.

The mechanical state is represented by `MolecularDynamicsState`, containing configuration, velocities, masses, step, and time. The energy calculation uses one atomic contribution per atom and a scalar total.

A coupled trajectory records the mechanical state used for each energy evaluation together with its graph, features, retained execution values, model parameters, and selected update schedule.

## 3. Conditioned Potential Energy

The reference energy operator has the input mapping:

`E_model: (C_atom, G, Q, sigma) -> EnergyModelResult`.

`ReferenceEnergyModel.evaluate` applies `conditioned_equivariant_layer_step`, followed by `LinearInvariantEnergyFunctional.evaluate`. The conditioned layer supplies invariant scalar channels for the energy aggregation.

For the scalar-channel vector `phi_i` at atom `i`, weights `w_a`, and bias `b`, the reference functional evaluates:

`E_i = b + sum_a w_a phi_(i,a)`.

`E_pot = sum_i E_i`.

`EnergyState.from_atomic_energies` constructs the total from its ordered atomic-contribution tuple. The scalar energy depends on the selected geometry, graph, feature inputs, model parameters, and retained execution vector.

The `TernaryConditioning` operator selects the configured feature scale for each retained state `-1`, `0`, or `1`. Active neutral `0` has its own conditioning parameter and execution semantics. Pending targets and committed execution records remain represented in the separate execution-state structures.

## 4. Kinetic and Total Mechanical Energy

The atomic kinetic-energy contribution is:

`K_i = (1/2) m_i (v_i · v_i)`.

The total kinetic energy and combined mechanical energy are:

`K = sum_i K_i`.

`H = K + E_pot`.

`kinetic_energy(state)` constructs `KineticEnergyState`, including the atomic kinetic-energy tuple and its sum. The class requires finite nonnegative kinetic contributions and exact agreement between the stored total and the sum of its contributions.

`molecular_dynamics_energy(state, potential)` constructs `MolecularDynamicsEnergyState`. It requires matching kinetic and potential atom counts and exact equality of the combined total with `K + E_pot` under the executed floating-point aggregation order.

Potential-energy contributions may carry either sign. Kinetic energy is nonnegative for the declared positive masses and finite real velocities.

## 5. Continuous Conservative Mechanical Balance

On a differentiable interval with constant masses, fixed model parameters and conditioning, and a smooth potential-energy branch, consider:

`d r_i / dt = v_i`.

`m_i d v_i / dt = F_i^cons`.

`F_i^cons = -grad_(r_i) E_pot`.

The kinetic-energy derivative is:

`d K / dt = sum_i v_i · F_i^cons`.

The potential-energy derivative along the same coordinate trajectory is:

`d E_pot / dt = sum_i grad_(r_i) E_pot · v_i`.

Substitution yields the conservative balance:

`d H / dt = 0`.

Consequently, the continuous mechanical energy is constant over an interval satisfying these equations and derivative assumptions. For piecewise-smooth trajectories, the balance is applied on each smooth interval, and event boundaries are recorded separately.

## 6. Coordinate-Derived Forces

`ConservativeForceEvaluator` evaluates Cartesian force components through central coordinate differences. With coordinate perturbation `h > 0` and one coordinate basis direction `e_(i,d)`, the executable approximation is:

`F_(i,d) = -[E_pot(R + h e_(i,d)) - E_pot(R - h e_(i,d))] / (2h)`.

The force evaluator retains the supplied interaction graph, node features, and execution vector during both energy evaluations of a coordinate perturbation. `CoordinateDifferentiation` supplies the positive finite perturbation step and its inverse central span.

For a sufficiently smooth potential branch, the central difference has coordinate-derivative truncation error of order `h^2`. Numerical roundoff and the conditioning of the energy evaluations contribute to the computed force values.

The force-gradient consistency tests compare coordinate-derived forces against analytic reference derivatives, symmetry relations, and declared numerical tolerances.

## 7. Interaction-Graph Update Boundary

`velocity_verlet_step` constructs a graph from the initial atomic coordinates, computes forces, advances positions, constructs a second graph from the updated coordinates, and computes endpoint forces.

Within each coordinate-difference force evaluation, graph topology is held at the selected endpoint graph. The interaction cutoff and the graph-construction rule therefore enter both the force calculation and the recorded energy history.

`evaluate_trajectory_energy` constructs a graph independently for each recorded trajectory state before evaluating its potential energy. The graph used for an energy observation is associated with that state's coordinates and supplied cutoff.

Numerical analysis near cutoff crossings records the selected image and cutoff rules, the coordinate perturbation, and the endpoint graph sequence.

## 8. Velocity-Verlet and Discrete Energy Evolution

For a fixed mechanical timestep `dt > 0`, the force-driven reference step uses:

`r_i[n+1] = r_i[n] + dt v_i[n] + (dt^2 / 2) a_i[n]`.

`v_i[n+1] = v_i[n] + (dt / 2) (a_i[n] + a_i[n+1])`.

`a_i[n] = F_i[n] / m_i`.

Let `K[n]`, `E_pot[n]`, and `H[n]` be the energies computed for recorded state `n`. Define the absolute and cumulative total-energy changes:

`delta_H[n] = H[n+1] - H[n]`.

`Delta_H[n] = H[n] - H[0]`.

For a declared reference magnitude `H_scale > 0`, define the normalized change:

`d_H[n] = Delta_H[n] / H_scale`.

An energy-conservation study records the energy sequence, the selected time interval, the force differentiation step, the graph cutoff, the mechanical timestep, and the initial and final conditioning state. Timestep refinement and fixed-horizon comparisons provide numerical convergence observables.

## 9. Trajectory Energy Observation

`run_velocity_verlet_trajectory` produces an ordered `MolecularDynamicsTrajectory` containing one `MolecularDynamicsStepResult` per mechanical step. For `L` completed steps, its `states` property returns `L + 1` states, including the initial state.

`evaluate_trajectory_energy(trajectory, model, features, execution, cutoff)` evaluates the model energy at every state and combines it with that state's kinetic energy.

The result, `MolecularDynamicsTrajectoryEnergy`, contains:

- `energies`: the ordered combined energy-state tuple;
- `kinetic_energies`: one total kinetic energy per state;
- `potential_energies`: one potential energy per state;
- `total_energies`: one combined energy per state;
- `initial` and `final`: endpoint energy observations;
- `state_count` and `atom_count`: trajectory-energy cardinalities.

The current trajectory runner and energy-observation function receive a fixed feature vector and a fixed execution vector for their call. Their common atom count equals the molecular state atom count.

## 10. Reference Energy-Drift Test

`tests/conservation/test_md_trajectory_energy.py` executes a deterministic two-atom reference fixture using:

| Parameter | Test value |
| --- | --- |
| Mechanical integrator | Velocity-Verlet |
| Number of completed steps | `4` |
| Recorded energy observations | `5` |
| Mechanical timestep | `0.01` |
| Interaction cutoff | `2.0` |
| Coordinate-difference step | `1.0e-6` |
| Final-minus-initial energy bound | `abs(H[4] - H[0]) < 2.0e-8` |

The test also checks individual energy components against its declared numeric baseline, reproducible execution from identical inputs, agreement with direct per-state evaluation, and state cardinality.

The drift bound belongs to this specified fixture. Tolerance selection for other trajectories is performed with their numerical methods, scales, integration intervals, and fixed acceptance contracts.

## 11. Continuous Energy Balance with Exchange

For a differentiable conditioned energy `E_pot(R, B, A, t)` and constant masses, let the mechanical forces be:

`F_i = -grad_(r_i) E_pot + F_i^nc`.

Here `F_i^nc` collects declared nonconservative, applied, and boundary-force contributions. Along a smooth interval, the chain rule gives:

`d H / dt = sum_i v_i · F_i^nc + partial_t E_pot + (partial_B E_pot) : (d B / dt) + (grad_A E_pot) · (d A / dt)`.

The cell term is included when `B` evolves. The auxiliary term uses continuous conditioning coordinates and their specified evolution law. The contraction `:` denotes the componentwise matrix inner product.

An open control-volume realization additionally declares thermal exchange, material inflow and outflow, and associated transported energy. Those exchanges enter the balance according to the selected subsystem boundary and sign convention.

For an integration interval `[t_a, t_b]`, the balance record relates the computed change in stored mechanical energy to integrated forces, explicit parameter evolution, cell work, thermal exchanges, and boundary fluxes.

## 12. Dissipative Power

For a specified linear drag law with `zeta_i >= 0`, take:

`F_i^diss = -zeta_i v_i`.

Its mechanical power is:

`P_diss = sum_i F_i^diss · v_i = -sum_i zeta_i |v_i|^2`.

A nonlinear dissipative operator similarly supplies its force or constitutive response and the associated instantaneous power. An energy-balance trace records the work integral over each interval and the reservoir or boundary variables associated with that exchange.

The mechanical balance is evaluated with the declared forces and energy-storage variables for the chosen system boundary.

## 13. Thermal Coupling Events

The deterministic thermostat in `src/tr_eif/md/thermostat.py` applies a global velocity factor `lambda_T` at a selected event. For positive initial kinetic temperature:

`lambda_T = sqrt(T_target / T_current)`.

`v_i,after = lambda_T v_i,before`.

The instantaneous kinetic-energy change is:

`Delta_K_thermal = (lambda_T^2 - 1) K_before`.

During this operator call, atomic positions, cell, masses, mechanical step, and mechanical time are retained. The thermal-exchange record stores the pre-event and post-event energies, target temperature, degrees of freedom, Boltzmann constant, and scale factor.

With energy entering the atomistic subsystem taken as positive, the kinetic-energy increment defines the corresponding event exchange contribution for this velocity transformation.

## 14. Volumetric Coupling and Mechanical Work

For full three-dimensional periodicity, `apply_isotropic_barostat` uses the volume factor:

`mu_V = 1 - (dt / tau_p) beta (P_target - P_current)`.

The resulting linear scale is `s = mu_V^(1/3)` with `mu_V > 0`. The operator transforms:

`B_after = s B_before`.

`r_i,after = s r_i,before`.

`V_after = mu_V V_before`.

Velocities, masses, mechanical step, and mechanical time are retained by this transformation. The kinetic-energy contribution is consequently retained, while the potential energy is reevaluated at the updated geometry when requested.

The cell-event record includes `Delta_V`, applied pressure data, the chosen pressure-work convention, and the conditioned energy before and after the affine transformation. Under a constant external pressure and work-on-subsystem convention:

`W_on = -P_external Delta_V`.

`ConservativeStressEvaluator` evaluates the reference energy derivative under homogeneous cell strain, divided by the reference cell volume, using symmetric Cartesian strain components and a fixed supplied graph during each derivative evaluation.

## 15. Resonance and Ternary Conditioning Events

`propagate_md_resonance_state` advances the continuous oscillator phases using the interaction graph of the supplied mechanical configuration. Its returned event record retains the supplied mechanical state and stores the previous and current resonance states.

`propagate_md_ternary_state` executes one guarded vector opportunity and retains the supplied mechanical state. Its retained execution alphabet is `-1/0/1`, with active neutral `0` and separate pending destinations.

The conditioned interatomic energy is evaluated with the retained execution vector selected by the caller. For two execution records on the same atomic configuration and feature vector, an event energy difference is:

`Delta_E_exec = E_pot(R, G, Q, sigma_after) - E_pot(R, G, Q, sigma_before)`.

The event trace associates this difference with the committed execution legs and their order. A held execution opportunity retains its retained-state vector; the conditioning operator selects its feature scales from those retained values.

A coupled run identifies the selected mechanical state, resonance state, request mapping, guard configuration, committed events, and energy-evaluation order. Any accompanying control work or boundary exchange is registered through the declared energy-accounting convention.

## 16. Piecewise Evolution and Balance Residuals

Let a trajectory consist of smooth integration intervals separated by explicitly recorded thermal, volumetric, and conditioning events. Define the cumulative stored-energy change:

`Delta_H_total = H_final - H_initial`.

Let `W_forces`, `W_cell`, `Q_thermal`, `J_boundary`, and `W_conditioning` denote the exchange contributions computed according to one declared, consistently applied accounting convention. The corresponding balance residual is:

`R_balance = Delta_H_total - (W_forces + W_cell + Q_thermal + J_boundary + W_conditioning)`.

A calculation specifies how each event contribution is constructed from pre-event and post-event states, including any explicit changes to the stored energy functional. Each transfer is included once according to the selected boundary and bookkeeping definitions.

The balance residual and its refinement history are computed at declared physical times. Smooth-interval integration error and event-time alignment are recorded separately.

## 17. Exact Invariants and Numerical Qualification

The structural and categorical checks include:

- atom-count agreement across mechanical, kinetic, potential, feature, and execution states;
- positive finite masses and integration timesteps;
- finite kinetic, potential, and total-energy scalars;
- ordered trajectory-state continuity and state-count relation `L + 1`;
- exact `KineticEnergyState` total aggregation and exact `MolecularDynamicsEnergyState` combination contracts;
- retained executed states in `{-1, 0, 1}` and the declared committed-event transition relation;
- deterministic ordering of graph construction, energy evaluation, and stored observations.

Numerical qualification includes central-difference force consistency, energy-drift histories, trajectory timestep refinement, periodic-image and cutoff conditions, cell-strain derivatives, and open-system exchange-balance residuals. Floating-point comparison tolerances are declared with the corresponding method and accepted before execution.

For repeated deterministic calculations, the initial states, model parameters, integration sequence, graph and execution inputs, and resulting energy observations are compared according to the selected reproducibility contract.

## 18. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| Atomic and scalar potential-energy state | `src/tr_eif/energy/state.py` |
| Invariant scalar energy functional | `src/tr_eif/energy/functional.py` |
| Conditioned reference energy evaluation | `src/tr_eif/energy/model.py` |
| Retained-state feature conditioning | `src/tr_eif/equivariant/conditioning.py` |
| Coordinate-derived force evaluation | `src/tr_eif/energy/force_evaluator.py` |
| Homogeneous-strain stress evaluation | `src/tr_eif/energy/stress_evaluator.py` |
| Kinetic and total MD energy | `src/tr_eif/md/observables.py` |
| Mechanical state and timeline | `src/tr_eif/md/state.py` |
| Velocity-Verlet mechanical step | `src/tr_eif/md/execution.py` |
| Repeated MD integration | `src/tr_eif/md/trajectory.py` |
| Ordered trajectory energy observations | `src/tr_eif/md/trajectory_observables.py` |
| Velocity rescaling | `src/tr_eif/md/thermostat.py` |
| Isotropic cell scaling | `src/tr_eif/md/barostat.py` |
| MD-associated resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| MD-associated ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| Energy aggregation tests | `tests/conservation/test_energy_consistency.py` |
| Force-gradient tests | `tests/conservation/test_force_gradient_consistency.py` |
| MD energy-observable tests | `tests/conservation/test_md_energy_observables.py` |
| Trajectory energy and drift tests | `tests/conservation/test_md_trajectory_energy.py` |
| Stress consistency tests | `tests/conservation/test_stress_consistency.py` |

These test modules exercise reference energy aggregation, force derivatives, kinetic and potential combination, trajectory-state ordering, reproducibility, finite-value contracts, and numerical energy-drift criteria.

## 19. Summary

TR-EIF evaluates molecular-dynamics mechanical energy as the sum of kinetic and conditioned interatomic potential energy. Continuous conservative dynamics admit a constant-energy balance under explicitly stated derivative assumptions, while open-system motion and controlled events are represented through defined energy-exchange contributions.

The executable reference records per-state energy observations over velocity-Verlet trajectories and provides independent thermal, volumetric, resonance, and balanced-ternary operators. Their coupling schedule determines the complete energy-accounting trace and the numerical balance observables.
