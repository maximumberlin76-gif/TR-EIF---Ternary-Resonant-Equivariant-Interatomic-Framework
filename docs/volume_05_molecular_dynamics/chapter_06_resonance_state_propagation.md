
# Resonance State Propagation

## 1. Scope and Dynamical System

This chapter specifies propagation of continuous oscillator phases associated with a three-dimensional atomic configuration in TR-EIF. The executable reference couples an atomic interaction graph to Kuramoto–Sakaguchi phase dynamics and records the resulting continuous resonance state alongside the molecular-dynamics state used for graph construction.

The coupled state comprises separately typed mechanical coordinates, oscillator variables, and balanced-ternary execution variables. The reference resonance propagation operator advances oscillator phases on a selected atomic configuration. A complete multirate calculation declares the order of mechanical integration, graph sampling, phase integration, descriptor evaluation, and execution events.

The executable entry point is `propagate_md_resonance_state` in `src/tr_eif/md/resonance_propagation.py`.

## 2. Atomistic and Oscillator State

Let `N ≥ 1` be the number of atoms and the number of associated oscillators. The molecular-dynamics state `X_MD` contains an `AtomicConfiguration`, three-dimensional velocities, positive masses, mechanical step index, and mechanical time.

For oscillator `j`, define:

- `theta_j`: continuous oscillator phase, represented modulo `2π`;
- `omega_j`: retained intrinsic angular frequency;
- `kappa_j`: nonnegative coupling coefficient for receiving node `j`;
- `gamma_j`: phase lag for receiving node `j`.

The resonance state and phase parameters are:

`X_R = (theta, omega)`.

`P_R = (kappa, gamma)`.

`ResonanceState` and `PhaseDynamicsParameters` contain immutable tuples with one entry per oscillator. The executable contract requires equal positive cardinality across the phase, frequency, coupling, and phase-lag vectors and the MD atom count.

Phases, frequencies, coupling coefficients, and phase lags are finite. Coupling coefficients satisfy `kappa_j ≥ 0`; the phase-lag entries are finite real values. The reference state normalizes phase angles to `[0, 2π)`.

## 3. Interaction Graph from Three-Dimensional Geometry

For an atomic configuration with positions `r_i ∈ R^3`, let `G(R, C, P; r_c)` denote the directed interaction graph constructed at positive radial cutoff `r_c`, using the supplied cell `C` and periodic flags `P`.

For each ordered pair of distinct atoms `(i, j)`, `build_cutoff_graph` evaluates the selected displacement `d_ij`. The inclusion condition is:

`|d_ij|^2 ≤ r_c^2`.

Nonperiodic configurations use Cartesian differences. Periodic configurations use the componentwise fractional-coordinate image convention defined in Chapter 04. Each included edge stores source, receiver, and its periodic-image index.

The graph defines the connectivity used in the phase derivative. Its node count equals `N`; the ordered edge tuple determines a reproducible summation order. The edge image participates in the geometric graph construction, while the phase derivative uses the source and receiver node indices of each edge.

## 4. Kuramoto–Sakaguchi Phase Dynamics

For every receiving node `j`, the reference phase equation is:

`d theta_j / dt = omega_j + kappa_j Σ_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

Each directed edge `i → j` contributes to the derivative of receiver `j` through its source phase, receiver phase, and receiver-specific lag. The sum includes all directed edges entering `j`.

The executable function `phase_derivatives` first initializes the derivative vector with the intrinsic frequencies. It then traverses the stored edges and accumulates each coupling contribution at the receiving node.

For a node with an empty incoming-edge set, its phase derivative is `omega_j`. The cutoff graph is therefore part of the declared continuous vector field, and changes in atomic geometry can change the phase-coupling topology at the selected graph-sampling instant.

## 5. Explicit Euler Propagation

Let `dt_R > 0` be a finite resonance-integration step. For a graph and parameters held fixed over one evaluation, compute:

`f_j = omega_j + kappa_j Σ_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

The reference explicit Euler update is:

`theta_j,next = wrap(theta_j + dt_R f_j)`.

`omega_j,next = omega_j`.

Here `wrap(x) = x mod (2π)` maps a finite angle to `[0, 2π)`.

`euler_step` evaluates every component of `f` from the input `ResonanceState` and the same supplied graph, then constructs a new `ResonanceState` with wrapped phases and the original frequency tuple. The update uses one simultaneous derivative evaluation for the entire oscillator vector.

For a smooth, fixed-topology phase vector field over a fixed finite interval, explicit Euler has local truncation error of order `dt_R^2` and global trajectory error of order `dt_R`, under the corresponding regularity and stability conditions. A numerical refinement study specifies the graph-sampling policy when geometry and connectivity evolve.

## 6. MD-Associated Propagation Operator

The public call has the following signature:

`propagate_md_resonance_state(md_state, resonance_state, parameters, cutoff, time_step)`.

The operator performs these steps:

1. Validate the MD state, resonance state, and phase parameters.
2. Confirm that oscillator and parameter cardinalities equal the MD atom count.
3. Validate positive finite cutoff and resonance timestep.
4. Construct a directed cutoff graph from `md_state.configuration`.
5. Apply `euler_step` to the supplied resonance state using that graph.
6. Construct `MolecularDynamicsResonanceStep` with the MD state, previous and current resonance states, graph, cutoff, and timestep.

The returned MD state is the same input object. Its positions, velocities, masses, mechanical step index, and mechanical time are retained. The phase propagation result records the resonance update separately from mechanical advancement.

## 7. Result Record and Invariants

`MolecularDynamicsResonanceStep` contains:

| Field | Meaning |
| --- | --- |
| `md_state` | Atomic configuration and mechanical state used to build the graph |
| `previous` | Input continuous oscillator state |
| `current` | Continuous oscillator state after one Euler step |
| `graph` | Directed interaction graph sampled from `md_state.configuration` |
| `cutoff` | Validated positive radial cutoff |
| `time_step` | Validated positive resonance step |

Construction checks the types and records these exact structural relations:

- `previous.oscillator_count = md_state.atom_count`;
- `current.oscillator_count = md_state.atom_count`;
- `graph.node_count = md_state.atom_count`;
- `current.frequencies = previous.frequencies`.

The immutable record preserves the input resonance state as `previous` and the newly computed state as `current`. The phase-state constructor enforces finite wrapped angular coordinates in the output.

## 8. Two-Oscillator Numerical Example

Take two atoms with one directed edge in each direction, and set:

`theta = (0, π/2)`.

`omega = (0.1, -0.2)`.

`kappa = (0.5, 0.25)`.

`gamma = (0, 0)`.

`dt_R = 0.2`.

For receiving node `0`, the incoming source phase is `π/2`:

`f_0 = 0.1 + 0.5 sin(π/2) = 0.6`.

For receiving node `1`, the incoming source phase is `0`:

`f_1 = -0.2 + 0.25 sin(-π/2) = -0.45`.

Thus one Euler step gives:

`theta_0,next = 0.12`.

`theta_1,next = π/2 - 0.09`.

The frequency tuple remains `(0.1, -0.2)`. This example is represented in `tests/integration/test_molecular_dynamics_resonance_propagation.py`.

At a smaller cutoff that excludes both directed edges, the same initial state gives intrinsic-frequency updates `theta_0,next = 0.02` and `theta_1,next = π/2 - 0.04`.

## 9. Phase Order and Continuous Resonance Descriptors

A global phase-order observable for `N` oscillators is:

`R_phase = |(1/N) Σ_j exp(i theta_j)|`.

The executable `state_phase_order` evaluates this magnitude from the oscillator phases. It belongs to `[0, 1]`, subject to floating-point roundoff.

The reference frequency-spread descriptor uses the population standard deviation:

`omega_mean = (1/N) Σ_j omega_j`.

`spread_omega = sqrt((1/N) Σ_j (omega_j - omega_mean)^2)`.

The `resonance_descriptor` operator returns the ordered pair of continuous quantities:

`D_R = (R_phase, spread_omega)`.

A `ResonanceSpace` validates coordinate dimension, and a `ResonanceWindow` supplies closed finite lower and upper bounds. `classify_resonance_region` assigns `OUTSIDE`, `BOUNDARY`, or `INSIDE` from the coordinate and window. These are separately invoked descriptor and classification operators operating on a continuous resonance state.

Phase order, resonance-window membership, local phase relations, and system-level coherence retain their individual definitions in the resonance-theory contracts.

## 10. Parameterization and Material Context

`PhaseDynamicsParameters` supplies one coupling and one phase-lag value per receiving node. Parameter values and their construction are part of a specified dynamical realization.

The FLiBe domain layer includes `FLiBeResonanceParameterization` and `ConstantFLiBeResonanceParameters` in `src/tr_eif/flibe/resonance_parameterization.py`. These interfaces evaluate phase-parameter vectors from a validated coordination context or return a declared fixed vector with provenance metadata.

The FLiBe descriptor layer also retains configuration, graph-relative coordination, thermodynamic state, oscillator state, and source provenance in separately identified fields. A coupled calculation records which parameterization produced the phase-dynamics inputs at each update.

## 11. Scheduling with Molecular Dynamics

Let `Phi_MD` denote a mechanical advancement, `Phi_R` the resonance update, and `G_sample` the graph obtained from a selected configuration. A coupled step may be composed in a declared order such as:

`X_MD[n+1] = Phi_MD(X_MD[n], dt_MD; conditioning[n])`.

`G_sample = G(X_MD[n+1].configuration; r_c)`.

`X_R[j+1] = Phi_R(X_R[j], P_R[j], G_sample, dt_R)`.

This example samples the graph after the mechanical step. A run may instead define graph sampling before a mechanical step or at designated resonance substeps. The recorded schedule identifies the selected positions, cell, boundary conditions, cutoff, and parameter vector for each phase update.

For a multirate schedule, a ratio such as `dt_MD = q dt_R`, where `q` is a positive integer, defines `q` resonance integration intervals per mechanical interval. The calculation additionally declares whether the interaction graph and phase parameters are retained or recomputed at substep boundaries.

The reference `propagate_md_resonance_state` performs one phase step on the supplied MD configuration; the scheduling relation is specified by the caller.

## 12. Coupling to Balanced-Ternary Execution

The continuous resonance state can enter a declared request mapping and conditioning pipeline:

`X_R → continuous descriptor → request mapping → ternary execution → conditioned interatomic computation`.

The canonical executed states are `-1/0/1`, with active neutral `0`. Opposite-polarity committed transitions occur as separate events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

The retained state, request, pending destination, hold, and committed event use distinct fields and update rules. `propagate_md_ternary_state` provides a separate executable MD-associated operator for requested targets and guards.

A combined trace links resonance-step indices and ternary execution-event indices through explicit sampling and event-order records. Continuous oscillator phases and the physical phases of matter remain separately typed quantities.

## 13. Open-System Boundary and Exchange Variables

An open nonlinear dissipative atomistic realization defines its mechanical boundary, imposed exchanges, and any auxiliary evolution affecting resonance parameters or graph geometry. For example, temperature-dependent or boundary-dependent parameterization can be written:

`P_R[j] = M_parameters(X_MD, X_boundary, context)[j]`.

The parameter mapping supplies a `PhaseDynamicsParameters` object with explicit values and provenance. Its evaluation instant is declared in the update schedule. The underlying mechanical system retains its three-dimensional coordinates, energy operators, thermal variables, and exchange equations.

This keeps graph sampling, phase evolution, energy-gradient forces, and executed control events as individually reproducible operations within the coupled system.

## 14. Numerical Qualification and Reproducibility

A reproducible propagation trace records:

- atomic species, positions, cell, periodic-axis flags, and MD step/time;
- oscillator phase and intrinsic-frequency vectors before and after propagation;
- receiving-node couplings and phase lags;
- cutoff and directed graph edges, including image indices;
- resonance integration timestep and phase-wrapping convention;
- graph-sampling instant and any mechanical/resonance step correspondence;
- phase-order and other computed descriptors with their evaluation instants;
- classification window and its coordinate-space definition when used;
- execution requests and committed events when coupled to the ternary layer.

Discrete cardinality, graph indexing, and frequency-retention invariants use exact comparisons. Floating-point phase updates and numerical convergence observables use predeclared methods and tolerances. Deterministic replay applies the same ordered graph, initial state, parameters, timestep, and operator sequence.

## 15. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| MD state and atomic configuration | `src/tr_eif/md/state.py` |
| MD-associated resonance step | `src/tr_eif/md/resonance_propagation.py` |
| Cutoff interaction graph | `src/tr_eif/graph/builder.py` |
| Resonance state and angle wrapping | `src/tr_eif/resonance/state.py` |
| Receiving-node coupling and phase lag | `src/tr_eif/resonance/parameters.py` |
| Continuous phase derivatives | `src/tr_eif/resonance/dynamics.py` |
| Euler phase integrator | `src/tr_eif/resonance/integrator.py` |
| Global phase-order observable | `src/tr_eif/resonance/order.py` |
| Continuous descriptor | `src/tr_eif/resonance/descriptor.py` |
| Resonance coordinate window | `src/tr_eif/resonance/window.py` |
| Resonance-region classification | `src/tr_eif/resonance/classification.py` |
| FLiBe resonance parameterization | `src/tr_eif/flibe/resonance_parameterization.py` |
| FLiBe resonance descriptor | `src/tr_eif/flibe/resonance_descriptor.py` |
| MD-associated ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| MD resonance integration tests | `tests/integration/test_molecular_dynamics_resonance_propagation.py` |
| Resonance numerical integration tests | `tests/numerical/test_resonance_integration.py` |

The integration tests cover graph construction from nonperiodic and periodic configurations, known phase updates, empty-edge evolution, input cardinality and scalar validation, retained MD state, retained frequencies, and deterministic repetition. The numerical tests cover repeated phase updates, angular wrapping, frequency preservation, phase-order observables, and timestep validation.

## 16. Summary

TR-EIF associates a continuous oscillator state with the directed interaction graph sampled from three-dimensional atomic geometry. Receiver-specific Kuramoto–Sakaguchi coupling determines the phase derivatives, and an explicit Euler operator advances wrapped phases while retaining the frequency vector.

The propagation result records its input mechanical state, previous and current resonance states, graph, cutoff, and timestep. Continuous descriptors, parameterization, mechanical advancement, and balanced-ternary execution are composed through separately declared operators and trace schedules.
