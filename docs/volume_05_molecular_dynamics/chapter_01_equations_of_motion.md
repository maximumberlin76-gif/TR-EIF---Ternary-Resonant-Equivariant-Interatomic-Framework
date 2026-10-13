
# Equations of Motion

## 1. Scope and System Class

This chapter defines the continuous mechanical evolution of an atomic subsystem within TR-EIF, including its coupling to resonance dynamics, balanced-ternary execution, and boundary exchange.

The reference system class is an open nonlinear dissipative dynamical system. An atomistic realization declares its system boundary, interacting degrees of freedom, constitutive operators, external exchange, and numerical time evolution.

TR-EIP belongs to the interatomic model family within TR-EIF. Its energy and force operators connect three-dimensional atomic geometry with separately typed resonance and execution variables.

The canonical mechanical chain is:

`atomic state → interaction graph → conditioned energy → forces → acceleration → motion → observables`.

## 2. Atomic State

For an atomistic integration interval, let `N ≥ 1` denote the number of atoms. For `i ∈ {1, ..., N}` define:

- `s_i`: atomic species;
- `r_i(t) ∈ R^3`: Cartesian position;
- `v_i(t) ∈ R^3`: Cartesian velocity;
- `m_i > 0`: mass;
- `F_i(t) ∈ R^3`: total mechanical force.

Define `R = (r_1, ..., r_N)`, `V = (v_1, ..., v_N)`, and `M = (m_1, ..., m_N)`.

The complete declared mechanical state is represented by:

`x_MD = (S, R, V, M, C, B)`.

Here `C` denotes cell geometry where specified; `B` denotes boundary-state variables and controls. Time `t` remains continuous, while `n` labels a numerical integration step with `t[n+1] = t[n] + Δt[n]` and `Δt[n] > 0`.

In the current Python reference, `MolecularDynamicsState` stores an `AtomicConfiguration`, velocities, masses, step, and time. Each recorded state has one positive finite mass and one Cartesian velocity per atom. A particle-exchange realization must additionally define changes of atom inventory and boundary fluxes.

## 3. Continuous Mechanical Dynamics

For a differentiable interval of motion:

`d r_i / dt = v_i`.

`m_i d v_i / dt = F_i`.

Consequently:

`a_i = d v_i / dt = F_i / m_i`.

A useful force decomposition is:

`F_i = F_i^cons + F_i^ext + F_i^diss + F_i^boundary`.

Here the terms are energy-derived force, applied external force, dissipative force, and force transferred through a declared mechanical boundary. Every included term has its own physical units and constitutive definition.

Nonlinearity may enter through interatomic geometry, velocity-dependent response, auxiliary-state evolution, boundary conditions, and changes in the interaction neighborhood.

## 4. Conditioned Interatomic Energy

Let the scalar energy functional have the form:

`E = E(R, C, A; Θ)`.

`Θ` denotes model parameters; `A` denotes typed auxiliary inputs such as equivariant representations, resonance-derived descriptors, and executed ternary channels.

For a differentiable branch of `E`, with `C`, `A`, and `Θ` fixed during coordinate differentiation:

`F_i^cons = -grad_(r_i) E(R, C, A; Θ)`.

Collectively:

`F^cons = -grad_R E`.

The executable `ConservativeForceEvaluator` uses central coordinate differences. During each evaluation it retains the provided interaction graph, features, and ternary execution vector. The graph-building policy determines when the neighborhood is recalculated between energy evaluations.

This specifies the derivative convention independently of the rule used to update resonance descriptors or execution states.

## 5. Open Boundaries and Dissipation

An open-system description identifies exchanges of mechanical work, heat, momentum, and, when allowed by the chosen subsystem boundary, material.

For a fixed atom inventory, external and dissipative forces can enter the momentum equation through explicit operators. For example:

`F_i^diss = -D_i(R, V, t)`.

A linear velocity-drag realization takes `D_i = ζ_i v_i` with `ζ_i ≥ 0`. Its mechanical power is:

`P_i^diss = F_i^diss · v_i = -ζ_i |v_i|^2`.

This constitutes one specified dissipative operator. A nonlinear realization supplies its own `D_i`, and any memory or stochastic variables are incorporated into the declared auxiliary state.

For a control volume admitting material exchange, the corresponding balance includes mass, momentum, and energy fluxes across the specified surface. The fixed-`N` reference state remains the local atomistic representation used between such boundary events.

## 6. Mechanical Energy Balance

Define kinetic and total mechanical energies:

`K = (1/2) Σ_i m_i |v_i|^2`.

`H = K + E`.

On a smooth interval with constant masses, fixed cell, differentiable energy, and a continuously evolving auxiliary state `A(t)`, let:

`F_i = -grad_(r_i) E + F_i^nc`.

Application of the chain rule yields:

`d H / dt = Σ_i v_i · F_i^nc + partial_t E + (grad_A E) · (d A / dt)`.

The partial time derivative holds `R` and `A` fixed. Cell evolution introduces an additional cell-derivative term, and particle exchange introduces its declared flux terms.

When `E` is time independent, `A` and `C` are fixed, and all `F_i^nc` vanish, the equation reduces to:

`d H / dt = 0`.

At an executed discrete conditioning event, one-sided energy values define an event difference at fixed coordinates:

`ΔE_event = E(R, C, A_after; Θ) - E(R, C, A_before; Θ)`.

The coupled energy budget records this difference with the corresponding control, switching, or boundary-exchange event. The integration trace keeps the event ordering and the mechanical coordinates used in both evaluations.

## 7. E(3) Geometry and Mechanical Covariance

Under an admissible spatial transformation with `Q ∈ O(3)` and translation `b ∈ R^3`:

`r_i' = Q r_i + b`.

`v_i' = Q v_i`.

For a transformed cell and consistently transformed auxiliary state, the invariant energy contract is:

`E(R', C', A'; Θ) = E(R, C, A; Θ)`.

Differentiation then gives the force-equivariance relation:

`F_i^cons(R', C', A') = Q F_i^cons(R, C, A)`.

For an admissible atomic permutation, species, mass, coordinate, velocity, auxiliary, and force arrays use the same index permutation.

An externally imposed directional field follows its own transformation rule when comparing transformed physical systems.

## 8. Interaction Geometry and Graph Evolution

A graph-building operator maps an atomic configuration and its geometric parameters to an interaction graph:

`G = G(R, C, B; cutoff)`.

Graph construction and coordinate differentiation are separate operations. The current `velocity_verlet_step` constructs a graph at the initial coordinates, evaluates forces, advances positions, constructs a graph at the new coordinates, and evaluates forces again.

Regularity at neighborhood changes depends on the declared cutoff rule and energy representation. A numerical experiment records the graph construction parameters and the force-evaluation points.

## 9. Continuous Resonance State

Let `θ_j(t)` be an oscillator phase, `ω_j` its angular frequency, `κ_j` the receiving-node coupling, and `γ_j` the receiving-node phase lag.

For the oriented edge set of `InteractionGraph`, the executable Kuramoto–Sakaguchi equation is:

`d θ_j / dt = ω_j + κ_j Σ_(i→j) sin(θ_i - θ_j - γ_j)`.

The edge orientation is defined by graph source and receiver indices. `phase_derivatives` uses the receiver-specific coupling and phase lag.

The MD resonance operator builds its graph from the supplied atomic configuration and advances the continuous resonance state with the phase integrator. That operator retains the input mechanical state during this operation.

Oscillator phase and thermodynamic phase of matter are distinct state variables; any material-state interpretation uses an explicit observable or mapping.

## 10. Balanced-Ternary Execution State

Let each atom-associated execution node retain:

`σ_i ∈ {-1, 0, 1}`.

The canonical notation is `-1/0/1`, and `0` is active neutral.

Committed opposite-polarity routes consist of separate events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

The retained execution value, current target, pending route, hold, and committed event have distinct semantics. A pending opposite-polarity destination belongs to `{-1, 1}` and can accompany retained active neutral. Active neutral may persist over multiple execution opportunities.

The existing `propagate_md_ternary_state` accepts explicit requested targets and optional guards. It returns the execution result while retaining the supplied MD mechanical state.

## 11. Hybrid Coupling and Event Order

A complete coupled realization declares three operators:

`request[n] = M_request(x_MD(t[n]), x_R(t[n]), auxiliary[n])`.

`execution[n] = U_exec(retained[n], pending[n], request[n], guards[n])`.

`A[n] = M_condition(x_R(t[n]), execution[n], features[n])`.

These equations specify the roles of request generation, discrete execution, and conditioning. Concrete types and internal retained fields are defined by their respective modules.

The model specifies when a mechanical force evaluation uses the retained execution vector relative to the resonance advance and committed execution event. Its trace records the order of those operations and the selected conditioning state.

## 12. Numerical Time Advancement

With acceleration `a_i[n] = F_i[n] / m_i`, the velocity-Verlet drift is:

`r_i[n+1] = r_i[n] + Δt v_i[n] + (Δt^2 / 2) a_i[n]`.

After new forces are evaluated, the velocity update is:

`v_i[n+1] = v_i[n] + (Δt / 2)(a_i[n] + a_i[n+1])`.

The current `velocity_verlet_step` retains masses, species, cell, features, and the supplied ternary execution vector during the mechanical step. The graph is rebuilt after the position drift.

Mechanical time advancement, continuous resonance integration, and discrete execution opportunities each have a declared numerical schedule. A coupled calculation specifies their sequencing, timestep relations, and synchronization points.

## 13. Thermal and Volumetric Control

The MD reference provides kinetic-energy and combined-energy observables. Its kinetic-temperature estimator uses:

`T_kin = 2 K / (f k_B)`.

Here `f` is the declared number of translational degrees of freedom and `k_B` is a supplied Boltzmann constant consistent with the chosen energy units.

The thermostat layer contains velocity-rescaling operators. The barostat layer contains isotropic cell-scaling operators for fully periodic three-dimensional configurations, with Cartesian positions and cell vectors scaled together.

Thermal exchange, cell deformation, and pressure coupling have explicit update operators and energy-accounting conventions. Thermodynamic temperature, pressure, oscillator phase, and ternary execution retain their individual physical and computational types.

## 14. Units and Invariants

| Quantity | Dimension or state space |
| --- | --- |
| Position and lattice vector | Length |
| Velocity | Length / Time |
| Acceleration | Length / Time^2 |
| Mass | Mass |
| Force | Mass × Length / Time^2 |
| Energy | Mass × Length^2 / Time^2 |
| Pressure | Energy / Length^3 |
| Temperature | Thermodynamic temperature |
| Oscillator frequency | 1 / Time |
| Oscillator phase | Angular variable |
| Executed state | Enum `-1/0/1` |

Masses and timesteps are strictly positive. Coordinate, velocity, force, and declared numerical parameters obey their finite-value contracts.

Exact discrete invariants include atom cardinality, execution state membership, guard outcomes, retained/pending distinctions, and committed route structure. Numerical comparisons of coordinate derivatives, force consistency, and time integration use explicitly defined discretizations and predeclared tolerances.

## 15. Trace and Qualification Interface

A reproducible MD trace specifies initial positions and velocities, species, masses, cell, boundaries, energy parameters, interaction graph rule, force evaluator, timestep sequence, and the resulting coordinates, forces, and energies.

When resonance and ternary execution are coupled, the trace additionally identifies phase state, coupling parameters, requested targets, retained execution values, pending destinations, and committed events.

The repository contains the following corresponding source modules:

| Function | Path |
| --- | --- |
| Molecular state | `src/tr_eif/md/state.py` |
| Force-to-acceleration mapping | `src/tr_eif/md/dynamics.py` |
| Position and velocity primitives | `src/tr_eif/md/kinematics.py` |
| Velocity-Verlet formulas | `src/tr_eif/md/integrator.py` |
| Force-driven mechanical step | `src/tr_eif/md/execution.py` |
| Energy-gradient force evaluation | `src/tr_eif/energy/force_evaluator.py` |
| Mechanical energy observables | `src/tr_eif/md/observables.py` |
| Resonance update | `src/tr_eif/md/resonance_propagation.py` |
| Ternary execution update | `src/tr_eif/md/ternary_propagation.py` |
| Temperature control | `src/tr_eif/md/thermostat.py` |
| Pressure coupling | `src/tr_eif/md/barostat.py` |

The associated executable tests are located under `tests/integration/`, `tests/conservation/`, and `tests/invariants/`, with method-specific numerical tests in `tests/numerical/`.

## 16. Summary

The molecular equations evolve continuous three-dimensional coordinates and momenta under declared force and boundary operators. Conservative forces follow the energy gradient, while open-system exchange enters through specified additional terms and state evolution.

Continuous resonance descriptors and active balanced-ternary execution are coupled through explicit request and conditioning mappings, preserving the separate semantics of physical motion, oscillator phases, and committed execution events.
