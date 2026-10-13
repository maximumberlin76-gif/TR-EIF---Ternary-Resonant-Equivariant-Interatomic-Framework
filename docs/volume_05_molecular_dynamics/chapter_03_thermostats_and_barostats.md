
# Thermostats and Barostats

## 1. Scope and Dynamical Setting

This chapter specifies thermal and volumetric coupling operators for molecular dynamics in TR-EIF. The atomistic subsystem belongs to a declared open nonlinear dissipative dynamical system, with mechanical evolution, boundary exchange, continuous resonance evolution, and balanced-ternary execution represented by distinct state variables and operators.

The current Python reference contains deterministic velocity-rescaling operations in `src/tr_eif/md/thermostat.py` and deterministic isotropic cell-scaling operations in `src/tr_eif/md/barostat.py`. These operators act on `MolecularDynamicsState` and can be composed with the velocity-Verlet integrator through a declared update schedule.

The calculation chain is:

`mechanical state → kinetic/pressure inputs → coupling parameters → thermal or cell update → updated mechanical state → recorded observables`.

## 2. Mechanical State and Control Variables

For `N ≥ 1` atoms, let `r_i ∈ R^3`, `v_i ∈ R^3`, and `m_i > 0` denote position, velocity, and mass. Let `C` be a periodic cell when supplied, and let `n` and `t` denote the current mechanical step and time.

The reference `MolecularDynamicsState` contains:

`X_MD = (configuration, velocities, masses, step, time)`.

Thermal coupling accepts an explicitly supplied target kinetic temperature `T_target`, a number of translational degrees of freedom `f`, and a Boltzmann constant `k_B` consistent with the selected units.

Pressure coupling accepts the scalar inputs `P_current`, `P_target`, compressibility `beta`, integration interval `dt`, and coupling time `tau_p`.

A coupled experiment specifies the source of each control parameter, the measurement or calculation associated with each input observable, and the step at which the operator is applied.

## 3. Kinetic Energy and Temperature

The kinetic-energy observable is:

`K = (1/2) Σ_i m_i (v_i · v_i)`.

`kinetic_energy(state)` in `src/tr_eif/md/observables.py` evaluates the atomwise contributions and their total.

Given a declared `f` and `k_B`, the reference kinetic-temperature estimator is:

`T_kin = 2 K / (f k_B)`.

Its executable function is `kinetic_temperature(state, degrees_of_freedom, boltzmann_constant)`.

The input contract is:

- `f` is an integer with `1 ≤ f ≤ 3N`;
- `k_B` is finite and strictly positive;
- masses are finite and strictly positive;
- Cartesian velocities have three finite components per atom.

The degree-of-freedom convention is declared for the particular dynamical calculation. For example, the selected convention records whether total translational motion is included or constrained; the executable function uses the supplied `f` directly.

Kinetic temperature belongs to the thermodynamic observable space. Oscillator phase, phase coupling, and active neutral `0` in the execution space retain their separate definitions.

## 4. Deterministic Velocity-Rescaling Operator

Let `T_current = T_kin` and `T_target ≥ 0`. For `T_current > 0`, define the scale factor:

`lambda_T = sqrt(T_target / T_current)`.

The updated velocities are:

`v_i' = lambda_T v_i`.

The corresponding kinetic energy and kinetic-temperature transformations are:

`K' = lambda_T^2 K`.

`T_kin' = lambda_T^2 T_current`.

Consequently, for a positive initial kinetic temperature, the requested nonnegative target temperature is attained under the same `f` and `k_B` conventions, subject to floating-point evaluation.

`velocity_rescaling_factor` returns the scale factor, `rescale_velocities` applies a supplied nonnegative factor, and `rescale_to_kinetic_temperature` combines temperature evaluation with the scaling operation.

The reference retains the configuration, masses, step index, and time. Velocity components alone are transformed in this operation.

## 5. Zero-Kinetic-Temperature Branches

The velocity-rescaling contract contains the following exact branches:

| Current kinetic temperature | Target kinetic temperature | Operator result |
| --- | --- | --- |
| Positive | Positive | `sqrt(T_target / T_current)` |
| Positive | Zero | Zero velocity scale |
| Zero | Zero | Identity velocity scale `1.0` |
| Zero | Positive | `ValueError` |

The final branch follows from the homogeneous map `v_i' = lambda_T v_i`: every finite scaling of an all-zero velocity field retains zero kinetic energy. A calculation with a positive-temperature initialization from this state defines an additional velocity-generation or energy-injection operator and its parameters.

These branches are mechanical-temperature operations. A retained execution state `0` remains governed by the independent active-neutral ternary contract.

## 6. Thermal Coupling and Energy Accounting

At a velocity-rescaling event, with positions, cell, model parameters, and energy-conditioning inputs held fixed, define:

`Delta_K_thermal = K_after - K_before`.

Using the deterministic rescaling relation:

`Delta_K_thermal = (lambda_T^2 - 1) K_before`.

For a separately declared reservoir-coupling convention, this increment is assigned to the corresponding thermal-exchange record with its chosen sign convention. The trace specifies the energy terms evaluated before and after the event.

For continuous motion with nonconservative force `F_i^nc`, the mechanical power contribution is:

`P_nc = Σ_i F_i^nc · v_i`.

A complete open-system energy balance also includes work at moving boundaries, heat exchange, explicit time dependence of conditioned energy, and material fluxes where the subsystem boundary admits particle exchange. Each contribution uses its own operator and integration interval.

## 7. Isotropic Pressure-Coupling Relation

The reference barostat uses an explicitly supplied current pressure, target pressure, positive compressibility, positive timestep, and positive coupling time.

Define the volumetric scale factor:

`mu_V = 1 - (dt / tau_p) beta (P_target - P_current)`.

The linear scale is:

`s = mu_V^(1/3)`.

The operator `isotropic_barostat_scale` requires `mu_V > 0` and returns finite `s > 0`. Current and target pressures accept finite real values; `beta`, `dt`, and `tau_p` are finite and strictly positive.

For the implemented sign convention:

- `P_current > P_target` gives `mu_V > 1` and expansion;
- `P_current < P_target` gives `0 < mu_V < 1` and contraction;
- `P_current = P_target` gives `s = 1`.

Pressure and compressibility use mutually consistent units, making `beta (P_target - P_current)` dimensionless. The ratio `dt / tau_p` is dimensionless.

## 8. Three-Dimensional Periodic-Cell Transformation

Let the cell vectors be `a`, `b`, and `c`, with cell volume:

`V_cell = |det(C)|`.

Under an isotropic scale `s > 0`:

`a' = s a`, `b' = s b`, `c' = s c`.

`r_i' = s r_i`.

Hence:

`V_cell' = s^3 V_cell = mu_V V_cell`.

For a nonsingular cell, fractional coordinates `q_i` satisfying `r_i = C q_i` are retained under the simultaneous transformation of the cell and Cartesian positions, up to numerical rounding.

`scale_periodic_configuration` requires an existing simulation cell and periodicity flags `(True, True, True)`. It returns an `AtomicConfiguration` with transformed positions and cell vectors while retaining species and periodicity flags.

Uniform cell dilation changes physical distances and may change the interaction graph and the conditioned interatomic energy when the next force and graph evaluations occur.

## 9. State-Level Barostat Update

`apply_isotropic_barostat` evaluates the scalar pressure-coupling scale and applies `scale_periodic_configuration` to the input state's atomic configuration.

The resulting `MolecularDynamicsState` retains:

- original velocities;
- original masses;
- original mechanical step index;
- original mechanical time.

The operator updates Cartesian positions and lattice vectors through the same positive linear scale. A subsequent mechanical integrator call uses the returned configuration and its interaction geometry.

For a fixed atom inventory with constant total mass `M_total`, the instantaneous cell-density transformation is:

`rho_cell = M_total / V_cell`.

`rho_cell' = rho_cell / mu_V`.

This relation follows directly from the three-dimensional volume transformation and the retained masses.

## 10. Pressure and Cell-Work Accounting

Pressure is a declared input to the reference barostat. A realization that computes pressure from the atomistic system specifies its estimator, stress convention, kinetic contribution, periodic-cell volume, and the state at which the estimator is sampled.

A pressure-coupling event records:

`Delta_V = V_cell_after - V_cell_before`.

For a specified external pressure history, the corresponding volume-work term follows the sign convention selected for the system energy balance. With work done on the subsystem defined as positive, a constant external pressure over one volume change gives:

`W_on = -P_external Delta_V`.

The conditioned potential energy can also change when geometry changes. A complete event record identifies the pre-update and post-update cell, coordinates, energy-conditioning inputs, and evaluated energy values.

## 11. Composition with Mechanical Time Advancement

The reference MD integration step advances mechanical coordinates and velocities through force evaluation and velocity-Verlet. Thermal and pressure coupling are callable state transformations with independently supplied parameters.

Let `Phi_MD(dt)` denote one mechanical step, `Phi_T` a thermostat event, and `Phi_P` an isotropic pressure-coupling event. One declared schedule is:

`X_next = Phi_P(Phi_T(Phi_MD(dt)(X_current)))`.

Other schedules select different operation orderings. The actual run specification records the order, selected state versions, control inputs, and frequency of thermal and pressure updates.

For pressure values derived from velocities and forces, sampling the estimator at a specified point in this sequence determines the input to `Phi_P`. A change in cell geometry also determines when the interaction graph is rebuilt for subsequent force evaluation.

Mechanical time is advanced by the mechanical integration operator. In the current reference, direct thermostat and barostat calls retain the `step` and `time` fields.

## 12. Coupling to Resonance and Ternary Execution

The complete hybrid state may be represented by:

`X = (X_MD, X_R, X_T, X_boundary)`.

Here `X_R` denotes continuous resonance variables, `X_T` the retained/pending balanced-ternary execution state, and `X_boundary` the thermal, volumetric, and exchange controls associated with the chosen system boundary.

The thermal and cell-scaling functions operate on `X_MD`. An explicitly defined coupling schedule determines how updated atomic geometry affects the resonance graph, how continuous resonance descriptors generate requests, and how committed ternary events condition subsequent interatomic computations.

The active-neutral execution state `0` supports its specified routing, retention, mediation, damping, and transition functions. Thermal, mechanical, geometrical, and execution observables remain separately typed throughout the coupled evolution.

## 13. Numerical Parameters and Recorded Observables

A deterministic thermal/pressure-coupling trace records the following inputs and outputs:

| Category | Trace fields |
| --- | --- |
| State | Species, positions, velocities, masses, cell, periodic axes, step, time |
| Thermal inputs | `f`, `k_B`, `T_current`, `T_target`, coupling event index |
| Thermal outputs | `lambda_T`, `K_before`, `K_after`, `T_after` |
| Pressure inputs | `P_current`, `P_target`, `beta`, `dt`, `tau_p` |
| Pressure outputs | `mu_V`, `s`, `V_before`, `V_after`, `Delta_V` |
| Geometry | Cell before/after, positions before/after, neighbor-graph update point |
| Exchange | Kinetic-energy increment, conditioned-energy change, prescribed heat/work/flux records |
| Coupling | MD/resonance/execution operator order and state-sampling instants |

Finite-value requirements and exact discrete fields are checked according to their declared types. Numerical temperature, pressure, volume, and energy comparisons use specified evaluation rules and fixed tolerances associated with the numerical method.

For a timestep refinement experiment, the trajectory records the coupling schedule and compares thermodynamic and geometric observables at common physical times.

## 14. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| Atomistic mechanical state | `src/tr_eif/md/state.py` |
| Kinetic-energy evaluation | `src/tr_eif/md/observables.py` |
| Kinetic temperature and velocity rescaling | `src/tr_eif/md/thermostat.py` |
| Pressure coupling and isotropic cell scaling | `src/tr_eif/md/barostat.py` |
| Velocity-Verlet operations | `src/tr_eif/md/integrator.py` |
| Force-driven MD advancement | `src/tr_eif/md/execution.py` |
| Mechanical trajectory | `src/tr_eif/md/trajectory.py` |
| Resonance update | `src/tr_eif/md/resonance_propagation.py` |
| Ternary execution update | `src/tr_eif/md/ternary_propagation.py` |
| Thermostat integration tests | `tests/integration/test_molecular_dynamics_thermostat.py` |
| Barostat integration tests | `tests/integration/test_molecular_dynamics_barostat.py` |

The thermostat tests cover kinetic temperature, global rescaling, target-temperature branches, preserved state fields, determinism, and input validation. The barostat tests cover pressure-scale arithmetic, expansion and contraction, three-dimensional affine geometry, volume scaling, state retention, periodicity requirements, determinism, and input validation.

## 15. Summary

Thermal coupling transforms velocities through a declared kinetic-temperature relation; isotropic pressure coupling transforms the three-dimensional periodic cell and Cartesian coordinates through a declared volumetric scale. Both operate on the reference MD state with explicit parameters and retained mechanical clock fields.

The composed dynamics record thermal and volumetric inputs, state updates, energy and boundary-exchange quantities, and the selected operator sequence alongside continuous resonance evolution and balanced-ternary execution.
