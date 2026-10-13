
# Time Integrators

## 1. Scope

This chapter specifies numerical time advancement for molecular dynamics in TR-EIF and its explicit interfaces with continuous resonance evolution and balanced-ternary execution.

The system state combines three-dimensional atomistic motion, continuous auxiliary dynamics, and discrete execution events. Their numerical clocks, state variables, and update operators are defined separately, then composed by an explicit coupling schedule.

The current executable reference provides:

- Cartesian position and velocity primitives in `src/tr_eif/md/kinematics.py`;
- velocity-Verlet drift and velocity updates in `src/tr_eif/md/integrator.py`;
- force-driven MD advancement in `src/tr_eif/md/execution.py`;
- multi-step trajectories in `src/tr_eif/md/trajectory.py`;
- explicit Euler integration of oscillator phases in `src/tr_eif/resonance/integrator.py`;
- MD-associated resonance and ternary operators in `src/tr_eif/md/resonance_propagation.py` and `src/tr_eif/md/ternary_propagation.py`.

## 2. Numerical State and Clocks

For `N` atoms with positive masses, let `R[n]` denote the tuple of Cartesian positions and `V[n]` the tuple of velocities at time `t[n]`. Let `C[n]` identify cell geometry and `A[n]` the declared continuous and discrete conditioning inputs.

The mechanical integration state is:

`X_MD[n] = (S, R[n], V[n], M, C[n], n, t[n])`.

For a positive integration increment:

`dt[n] = t[n+1] - t[n] > 0`.

The explicit reference state `MolecularDynamicsState` stores configuration, velocities, masses, an integer step, and a nonnegative finite time. Its `step` field advances by one per completed mechanical step. The fixed-step trajectory runner supplies the same `time_step` to each invocation.

A coupled realization may additionally track a resonance step index `j`, target-sampling index `m`, and ternary execution-event index `k`. The mapping among these indices is part of the coupling specification.

## 3. Mechanical Initial-Value Problem

For atom `i`:

`d r_i / dt = v_i`.

`d v_i / dt = a_i(R, V, A, t)`.

For a force-based realization with constant mass over an integration interval:

`a_i = F_i / m_i`.

The state initializer supplies positions, velocities, masses, species, cell configuration, boundary controls, and conditioning values at the beginning of the interval. The chosen force evaluation determines the mechanical vector field used during that interval.

The force-driven reference step uses `ReferenceEnergyModel`, `ConservativeForceEvaluator`, `NodeFeatureVector`, `TernaryExecutionVector`, and a cutoff-defined `InteractionGraph`.

## 4. Cartesian Kinematic Primitives

The functions `advance_position` and `advance_velocity` provide componentwise updates:

`r_next = r + dt v`.

`v_next = v + dt a`.

These are separate primitives for constant-input kinematic increments. Their calls validate finite, positive timesteps. They can serve numerical component tests and explicit compositions with specified force and acceleration evaluation points.

## 5. Velocity-Verlet Update

For the mechanical equations with accelerations obtained from forces at the beginning and end of a step, define:

`a_i[n] = F_i[n] / m_i`.

The position drift is:

`r_i[n+1] = r_i[n] + dt v_i[n] + (dt^2 / 2) a_i[n]`.

After evaluating the new acceleration:

`a_i[n+1] = F_i[n+1] / m_i`.

The velocity update is:

`v_i[n+1] = v_i[n] + (dt / 2) (a_i[n] + a_i[n+1])`.

The corresponding executable functions are `velocity_verlet_positions` and `velocity_verlet_velocities`. Both operate on immutable tuples with one three-dimensional vector per atom.

For smooth position-dependent forces, constant mass, and a fixed step, the standard velocity-Verlet method has local truncation error of order `dt^3` and global trajectory error of order `dt^2` over a fixed finite interval, subject to the regularity and stability conditions of the initial-value problem. The realized force evaluator contributes its own approximation error.

## 6. Force and Graph Evaluation Order

The function `velocity_verlet_step` applies the following concrete order:

1. Validate the mechanical state, model, force evaluator, node features, retained execution vector, cutoff, and timestep.
2. Construct `graph_before` from the initial atomic configuration.
3. Evaluate `forces_before` using the initial configuration, graph, features, and execution vector.
4. Convert those forces to `accelerations_before` using atomwise masses.
5. Advance positions with the velocity-Verlet drift.
6. Construct a new atomic configuration retaining species, cell, and periodic-axis metadata.
7. Construct `graph_after` from the advanced configuration.
8. Evaluate `forces_after` using the new configuration and the same supplied features and execution vector.
9. Convert the new forces to `accelerations_after`.
10. Complete the velocity update, increment the step index, and advance physical time by `dt`.
11. Return the two mechanical states, two graphs, and two force states in `MolecularDynamicsStepResult`.

`ConservativeForceEvaluator` approximates coordinate derivatives by central differences while retaining the interaction graph provided to each force evaluation. Thus graph rebuilding between mechanical endpoint evaluations and graph retention during each derivative evaluation are separate parts of the numerical procedure.

## 7. Force Approximation and Geometric Resolution

With fixed graph `G`, fixed features `Q`, and retained execution `sigma`, one Cartesian force component is approximated using a positive coordinate perturbation `h`:

`F_(i,d) ≈ -[E(R + h e_(i,d), G, Q, sigma) - E(R - h e_(i,d), G, Q, sigma)] / (2h)`.

For a sufficiently smooth energy functional, the central-difference derivative has truncation error of order `h^2`. Floating-point roundoff, conditioning of the energy evaluation, and graph geometry also contribute to the computed force.

The perturbation scale `h`, interaction cutoff, neighborhood geometry, and mechanical timestep `dt` are independently specified numerical parameters.

At a change of graph topology, the force and energy regularity is determined by the graph-construction rule and energy representation. A convergence study includes configurations that approach or cross cutoff boundaries when such configurations belong to the declared domain.

## 8. Repeated Mechanical Steps

`run_velocity_verlet_trajectory` calls `velocity_verlet_step` sequentially using one fixed timestep, one energy model, one force evaluator, one feature vector, one execution vector, and one cutoff supplied to the runner.

For requested step count `L > 0`:

`X_MD[n + L] = Phi_MD^L(X_MD[n]; dt, model, features, execution, cutoff)`.

The trajectory object contains an ordered tuple of `MolecularDynamicsStepResult` records. Every step begins with the previous step's `current` state. The resulting state sequence contains the initial state followed by each completed state.

The trajectory data expose initial and final state, intermediate state records, and the force and graph boundaries of every step.

## 9. Continuous Resonance Integration

The separate resonance state is `X_R = (theta, omega)`. Its graph-coupled Kuramoto–Sakaguchi vector field uses receiver-specific coupling and phase lag. For an oriented graph edge `i → j`, its contribution to receiver `j` is:

`kappa_j sin(theta_i - theta_j - gamma_j)`.

The complete derivative for receiver `j` is:

`d theta_j / dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

The current `euler_step` computes all derivatives from the supplied initial resonance state and graph, then performs:

`theta_j_next = wrap(theta_j + dt_R d theta_j / dt)`.

The frequency tuple is retained by this integration operation. `wrap_phases` normalizes the resulting angular coordinates. For a smooth vector field, explicit Euler has local truncation error of order `dt_R^2` and global error of order `dt_R` over a fixed finite interval under the corresponding regularity and stability conditions.

`propagate_md_resonance_state` constructs its graph from the supplied MD configuration, advances the resonance state with `euler_step`, and returns both resonance states, the graph, cutoff, timestep, and associated MD state.

## 10. Balanced-Ternary Execution Events

The canonical executed state space is `-1/0/1`, including active neutral `0`. The ternary execution operator advances retained and pending execution state under explicit requests and guards.

Opposite-polarity committed routes pass through separate execution events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

A pending opposite-polarity target has value `-1` or `1` while the retained state is `0`. Hold, target registration, active-neutral retention, and committed state changes are distinct operations.

`propagate_md_ternary_state` associates one execution node with each MD atom. It accepts optional requested targets and guards and returns an execution event record alongside the same MD mechanical state. Its state-transition semantics are implemented by `execute_ternary_vector_step`.

Ternary execution-event index `k` and mechanical integration-step index `n` may advance at different schedules. A coupled trace records the mapping between them.

## 11. Coupling and Composition

A coupled realization defines an ordered composition of continuous and discrete operators, for example:

`X_MD[n+1] = Phi_MD(X_MD[n], dt_MD; A[n])`.

`X_R[j+1] = Phi_R(X_R[j], dt_R; G_selected)`.

`request[m] = M_request(X_MD, X_R, auxiliary)`.

`X_T[k+1] = U_exec(X_T[k], request[m], guards[k])`.

`A_next = M_condition(X_R, X_T, features)`.

The equations name the integration and mapping roles. The selected sampling instants and ordering specify which state versions enter each operator. The current reference exposes mechanical, resonance, and ternary advancement as callable operations with explicit inputs.

For multirate evolution, a declared relation such as `dt_MD = q dt_R` with positive integer `q` can define resonance substeps inside one mechanical interval. Such a composition additionally specifies graph sampling, event processing, force conditioning, and retained-state writeback.

## 12. Open-System Exchange Operators

An open nonlinear dissipative atomistic model includes specified boundary and exchange dynamics. An operator-composition scheme can interleave the mechanical update with thermal, pressure, or boundary-state updates:

`X_next = Phi_boundary ◦ Phi_thermal ◦ Phi_MD (X_current)`.

The order shown is one explicitly chosen composition; the order of operators is part of the numerical experiment. Different compositions may have different truncation errors and exchange bookkeeping.

The repository contains separate thermostat and barostat operations in `src/tr_eif/md/thermostat.py` and `src/tr_eif/md/barostat.py`. Their parameters, application schedule, and energy or work accounting accompany the trajectory record when used.

For material exchange or changing atom inventory, the realization defines the inventory update, associated state mapping, and mass/momentum/energy fluxes at the exchange event.

## 13. Time-Step Selection and Numerical Convergence

The selected mechanical timestep resolves the fastest modeled atomic motions, force variations, neighbor-graph changes, and externally imposed control timescales within the investigated domain. The resonance timestep resolves the phase vector field and its coupling scales. Execution opportunities resolve the discrete scheduling contract.

A numerical refinement study declares the initial state, final physical time, parameter set, step sequences, and comparison observables before execution. For a refinement ratio of two, compare results obtained with `dt`, `dt/2`, and `dt/4` at common physical times.

For an observable `O`, define:

`D_1 = norm(O_dt - O_dt/2)`.

`D_2 = norm(O_dt/2 - O_dt/4)`.

Where an asymptotic error regime applies and both differences are positive, an observed convergence order is:

`p_obs = log2(D_1 / D_2)`.

The stated reference orders of velocity-Verlet and explicit Euler apply under their respective smoothness assumptions. Numerical studies of changing graph topology, external exchange, and committed execution events identify their separate event times and refinement policies.

## 14. Energy and Momentum Diagnostics

For a fixed inventory, define kinetic energy:

`K[n] = (1/2) sum_i m_i |v_i[n]|^2`.

Let `E[n]` be the conditioned interatomic energy evaluated at the specified configuration, cell, graph, and execution inputs. Then:

`H[n] = K[n] + E[n]`.

An absolute energy-change observable is:

`D_H[n] = H[n] - H[0]`.

For a declared nonzero reference scale `H_scale`, a dimensionless observable is:

`d_H[n] = D_H[n] / H_scale`.

For open-system evolution, the bookkeeping additionally registers heat, work, boundary fluxes, and discrete conditioning events according to the defined balance equations.

The momentum observable is `P[n] = sum_i m_i v_i[n]`. Momentum evolution is compared with integrated external impulses and declared boundary exchanges. Force consistency and derivative perturbation effects are recorded together with the chosen numerical tolerances.

## 15. Determinism and Exact Invariants

A reproducible trajectory fixes initial configuration, masses, velocities, model parameters, feature vector, execution vector, cutoff, coordinate-difference increment, timestep sequence, and all scheduled external inputs.

The following are exact discrete contracts in the present reference:

- one mass, position, velocity, and force vector per atom;
- positive finite masses and positive finite integration timesteps;
- matching graph and node-feature cardinalities;
- a mechanical step-index increment of exactly one;
- the ordered `previous` and `current` chain in trajectory records;
- the execution state alphabet `-1/0/1`;
- distinct requested, pending, retained, held, and committed execution semantics;
- separate committed legs for opposite-polarity routes.

Coordinates, velocities, numerical energies, derivatives, and convergence metrics use declared numerical methods and preselected floating-point tolerances. Exact categorical invariants use exact equality.

## 16. Executable Interfaces and Qualification

| Role | Repository path |
| --- | --- |
| State and clock | `src/tr_eif/md/state.py` |
| Kinematic increments | `src/tr_eif/md/kinematics.py` |
| Velocity-Verlet primitives | `src/tr_eif/md/integrator.py` |
| Force-to-acceleration mapping | `src/tr_eif/md/dynamics.py` |
| Coupled force and geometry evaluation | `src/tr_eif/md/execution.py` |
| Repeated MD advancement | `src/tr_eif/md/trajectory.py` |
| Coordinate-difference force | `src/tr_eif/energy/force_evaluator.py` |
| Resonance time step | `src/tr_eif/resonance/integrator.py` |
| MD-associated resonance step | `src/tr_eif/md/resonance_propagation.py` |
| MD-associated ternary event | `src/tr_eif/md/ternary_propagation.py` |
| Thermostat operator | `src/tr_eif/md/thermostat.py` |
| Barostat operator | `src/tr_eif/md/barostat.py` |

Executable checks of these interfaces are present in:

- `tests/integration/test_molecular_dynamics_step.py`;
- `tests/integration/test_molecular_dynamics_trajectory.py`;
- `tests/integration/test_molecular_dynamics_resonance_propagation.py`;
- `tests/integration/test_molecular_dynamics_ternary_propagation.py`;
- `tests/numerical/test_resonance_integration.py`;
- `tests/conservation/test_md_trajectory_energy.py`;
- `tests/invariants/test_md_validation_invariants.py`.

The numerical record associates each computed observable with its input state, operator, discretization parameters, time coordinate, and integration event order.

## 17. Summary

The current TR-EIF MD reference integrates three-dimensional mechanical coordinates using velocity-Verlet with force and interaction-graph evaluation at both step boundaries. Continuous oscillator phases evolve through a separately invoked Euler integrator, and active balanced-ternary execution advances through explicit committed events.

An end-to-end realization specifies the composition schedule, physical boundaries, numerical tolerances, and trace state needed to reproduce the coupled evolution.
