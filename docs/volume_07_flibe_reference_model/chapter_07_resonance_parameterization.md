
# Resonance Parameterization

## 1. Scope and Mathematical Role

This chapter defines resonance parameterization for the FLiBe reference realization of TR-EIF. It connects LiF–BeF2 atomic configurations, species-resolved local coordination, directed interaction graphs, continuous Kuramoto–Sakaguchi dynamics, resonance descriptors, and the explicitly scheduled balanced-ternary execution layer.

The system class is an open nonlinear dissipative dynamical system. Its atomistic state retains three-dimensional geometry, mechanical variables, composition, temperature, pressure, boundary exchange, continuous oscillator variables, and executed `-1/0/1` states in separately typed representations.

The parameterization chain is:

`FLiBe atomic configuration → directed interaction graph → species-resolved coordination → resonance parameter evaluator → coupling and phase-lag vectors → continuous phase evolution → resonance descriptor`.

A subsequent declared mapping can use the continuous descriptor to generate an execution request and condition the FLiBe TR-EIP energy calculation.

## 2. Material and Atomistic Input

`FLiBeConfiguration` binds a three-dimensional `AtomicConfiguration` to the canonical Li, Be, and F species domain. The underlying atomic configuration retains an ordered species tuple, one finite Cartesian position per atom, optional cell vectors, and three periodic-axis flags.

For a binary composition with LiF and BeF2 formula-unit amounts `n_LiF` and `n_BeF2`, define:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

The exact `2 LiF : 1 BeF2` composition has `x_LiF = 2/3` and `x_BeF2 = 1/3`, with the atomic inventory ratio `Li:Be:F = 2:1:4`. Source-specific nominal and measured compositions are retained with their original definition and precision.

`FLiBeThermodynamicState` stores a finite positive absolute temperature in kelvin and finite nonnegative pressure in pascal. A material-specific parameter study records these thermodynamic coordinates together with composition, atomic geometry, physical-state domain, and method provenance.

## 3. Directed Interaction Graph and Coordination

Let `G` be an `InteractionGraph` constructed from the selected atomic configuration and geometric cutoff. For an ordered edge `i → j`, `i` is the source atom and `j` the receiving atom. An edge also stores its periodic-image index.

`build_flibe_coordination_state(configuration, graph)` counts incoming edges by source species. For receiving node `j` and species `s`:

`z_(j,s) = sum_(i→j in G) indicator(species(i) = s)`.

The three counts are ordered as:

`z_j = (z_(j,Li), z_(j,Be), z_(j,F))`.

`FLiBeCoordinationState` stores one `FLiBeAtomCoordination` per atomic index in contiguous order. Each count is a nonnegative integer; the total incoming-neighbor-record count is the sum over all three species and all receivers. The selected graph, periodic-image rule, and cutoff determine the structural input of the parameter evaluator.

## 4. Continuous Oscillator State

`ResonanceState` stores the continuous oscillator phase tuple `theta` and intrinsic-frequency tuple `omega`, with one oscillator per represented atom. Each phase is an angular coordinate on the circle, represented numerically in `[0, 2 pi)`.

For receiving oscillator `j`:

- `theta_j` is its continuous phase;
- `omega_j` is its intrinsic angular frequency;
- `kappa_j` is its nonnegative receiver-specific coupling coefficient;
- `gamma_j` is its finite receiver-specific phase lag.

`PhaseDynamicsParameters` contains the ordered tuples `coupling` and `phase_lag`. It requires both tuples to have equal nonzero length, all entries to be finite, and every coupling entry to satisfy `kappa_j >= 0`.

The parameter tuple and oscillator state have the same cardinality when used in `phase_derivatives` or `euler_step`.

## 5. Parameterization Mapping

For a coordination state `C = (z_0, ..., z_(N-1))`, a parameterization is the typed mapping:

`P_FLiBe: C × Lambda → (kappa, gamma)`.

`Lambda` denotes any separately declared evaluator parameters and source context. The evaluated output has:

`kappa = (kappa_0, ..., kappa_(N-1))`.

`gamma = (gamma_0, ..., gamma_(N-1))`.

The executable `FLiBeResonanceParameterization` accepts an evaluator with signature:

`ResonanceParameterEvaluator: FLiBeCoordinationState → PhaseDynamicsParameters`.

The evaluator supplies the numerical correspondence between coordination and the two parameter vectors. The enclosing parameterization validates the input, the returned type, and the oscillator-count correspondence.

## 6. Coordination-Dependent Provider

`FLiBeResonanceParameterization` is an immutable dataclass containing `evaluator`, `provenance`, and optional `source`. Its `evaluate(coordination)` operation:

1. Validates the `FLiBeCoordinationState` input.
2. Invokes the supplied evaluator once with that input.
3. Requires the returned value to be a `PhaseDynamicsParameters` instance.
4. Calls `parameters.validate_oscillator_count(coordination.atom_count)`.
5. Returns the validated parameter object.

The evaluator is the explicitly selected function that determines parameter dependence on atom identity, incoming coordination counts, and bound model context. `evaluate_resonance_parameters` dispatches the supported FLiBe parameterization types through the same input and output contract.

## 7. Constant Parameter Set

`ConstantFLiBeResonanceParameters` stores a `PhaseDynamicsParameters` object with provenance and optional source metadata. Its `evaluate(coordination)` method validates the coordination type and atom-count compatibility, then returns the stored parameter object.

For a fixed parameter set:

`kappa_j = kappa_j,fixed`.

`gamma_j = gamma_j,fixed`.

The result is indexed in the same oscillator order as the supplied coordination state. Repeated evaluation with coordination states of the same atom count retains the declared fixed parameter values.

A fixed parameter model and a coordination-dependent evaluator use the same downstream phase-dynamics interface.

## 8. Provenance and Source Binding

The two parameterization dataclasses use `ParameterProvenance`, which supplies the repository's identified provenance classes, including `PRIMARY_SOURCE`, `DERIVED`, `CALIBRATED`, `AUTHOR_DEFINED`, `BENCHMARK`, and `TEST_FIXTURE`.

For `PRIMARY_SOURCE`, the constructor requires a source string. When provided, the source must be nonempty and contain no leading or trailing whitespace. The source field and provenance are retained in the immutable parameterization record.

A model manifest resolves the source identifier to its method, physical state, composition, numerical values, parameter units, and construction procedure. The test suite also exercises the declared `REQUIRES_SOURCE` and `REQUIRES_TEST` enum values as provenance inputs to this interface.

## 9. Directed Kuramoto–Sakaguchi Coupling

For the directed graph `G`, the executable phase equation for receiver `j` is:

`d theta_j/dt = omega_j + kappa_j sum_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

`phase_derivatives(state, parameters, graph)` begins with the intrinsic-frequency tuple and traverses the directed edges in their stored order. Each edge contributes to its receiver using the receiver's `kappa_j` and `gamma_j`.

The edge set supplies connectivity and edge multiplicity. The parameter tuple supplies receiver-specific coupling and phase lag. Both are evaluated at declared points in the coupled mechanical–resonance schedule.

For a receiver with zero incoming edges, the sum is empty and its derivative equals `omega_j`.

## 10. Coupling Normalization and Dimensions

When phase is measured in radians and the integration variable is physical time, `omega_j` and `kappa_j` have dimensions of inverse time, while `gamma_j` is an angular lag in radians. The numerical implementation applies the supplied values under one declared time-unit convention.

The executable phase derivative sums incoming edge contributions without an automatic division by node degree. A coordination-normalized provider can therefore define an explicit relation, for example:

`kappa_j = kappa_ref,j / max(1, z_j,total)`.

Here `z_j,total = z_(j,Li) + z_(j,Be) + z_(j,F)` and `kappa_ref,j >= 0` is an evaluator parameter with the chosen inverse-time unit.

This equation is one possible provider definition. Its use, normalization convention, parameter values, and domain are specified by the corresponding model manifest.

## 11. Species-Resolved Parameter Families

A selected provider can use the ordered incoming coordination vector and receiving-atom species to define:

`kappa_j = K(species_j, z_(j,Li), z_(j,Be), z_(j,F); Lambda)`.

`gamma_j = Gamma(species_j, z_(j,Li), z_(j,Be), z_(j,F); Lambda)`.

The functions `K` and `Gamma` belong to the chosen evaluator. Their outputs satisfy the finite-value and coupling-sign conditions of `PhaseDynamicsParameters`.

`Lambda` may carry fixed coefficients and state-dependent quantities bound when the evaluator is constructed. The callable receives `FLiBeCoordinationState` at its public evaluation boundary; external material context is supplied through the selected provider configuration.

## 12. Deterministic Three-Node Example

The fixture in `tests/invariants/test_flibe_resonance_parameterization_invariants.py` supplies three coordination records:

| Atom index | Receiver species | Li neighbors | Be neighbors | F neighbors | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| `0` | Li | 0 | 1 | 1 | 2 |
| `1` | Be | 1 | 0 | 1 | 2 |
| `2` | F | 1 | 1 | 0 | 2 |

Its explicit test evaluator defines:

`kappa_j = float(z_j,total)`.

`gamma_j = 0.1 (j + 1)`.

It therefore produces:

`coupling = (2.0, 2.0, 2.0)`.

`phase_lag = (0.1, 0.2, 0.3)`.

The tuple is a deterministic `TEST_FIXTURE` input to the parameterization contract. The three-node fixture directly tests the coordination-to-parameter interface; full FLiBe material-state construction uses its own atomic-composition and thermodynamic-state conditions.

## 13. Fixed-Parameter Numerical Example

The fixed-parameter fixture in the same invariant test file defines:

`coupling = (0.2, 0.3, 0.4)`.

`phase_lag = (0.1, 0.2, 0.3)`.

`ConstantFLiBeResonanceParameters` stores these tuples as one `PhaseDynamicsParameters` value. Evaluating the same fixed model against coordination states with matching atom counts returns the same stored parameter object.

This example tests parameter retention, immutability, source metadata, and atom-count compatibility independently of the coordination-dependent evaluator.

## 14. Numerical Phase Integration

For resonance timestep `dt_R > 0` and fixed input graph and parameters during one derivative evaluation:

`f_j = omega_j + kappa_j sum_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

The explicit Euler step is:

`theta_j,next = wrap(theta_j + dt_R f_j)`.

`omega_j,next = omega_j`.

`wrap` maps each updated phase to `[0, 2 pi)`. `euler_step` evaluates all derivatives from the same previous resonance state, then creates the new wrapped state and retains the supplied frequency tuple.

The timestep, graph, parameter record, and phase state are therefore separate inputs to one resonance-integration event.

## 15. Geometry and Parameter Update Schedule

`propagate_md_resonance_state` constructs its phase-coupling graph from a supplied `MolecularDynamicsState` and cutoff. A caller can select a corresponding FLiBe coordination state and evaluate its parameterization at a declared sampling instant.

One explicit composition is:

`G[n] = build_cutoff_graph(X_atom[n], r_c)`.

`C[n] = build_flibe_coordination_state(X_FLiBe[n], G[n])`.

`P_R[n] = evaluate_resonance_parameters(model[n], C[n])`.

`X_R[j+1] = euler_step(X_R[j], P_R[n], G[n], dt_R)`.

This defines one possible coupled schedule. A realization specifies graph and parameter refresh events, timestep ratios, material-state changes, and how each resonance update corresponds to mechanical time.

## 16. Thermodynamic and Compositional Parameter Context

A FLiBe physical-state record may associate the parameterization with composition, temperature, pressure, and a selected local structural regime:

`Lambda = (x_LiF, x_BeF2, T, P, state_id, method_id, ...)`.

The chosen evaluator binds the required components of `Lambda` to the accepted coordination input. A time-dependent realization records which version of the context is used for each parameter evaluation.

Exact `2 LiF : 1 BeF2`, nominal `67:33`, and measured specimen composition remain separately identified source descriptions. The parameter record associates each value with its chosen composition basis and temperature–pressure domain.

## 17. Local Structural Evolution

For a material trajectory, coordination is sampled from three-dimensional atomic geometry at selected physical times:

`C[n] = C(R[n], B[n], periodic[n], r_c, G_policy)`.

A local structural change can alter the integer counts entering the evaluator. When the parameterization is recomputed, the resulting `kappa` and `gamma` vectors may change with this local coordination state.

The event trace links the selected configuration, graph, coordination, parameter object, previous phase state, and current phase state. The model specifies the update schedule at changes of graph topology or material boundary conditions.

## 18. Species Ordering and E(3) Covariance

A common rigid spatial transformation uses:

`r_i' = Q r_i + b`, with `Q in O(3)`.

For a graph-construction rule transported consistently under this transformation, species and graph-relative incoming coordination remain associated with their transformed atoms. A parameterization based on scalar species identities and invariant coordination counts produces corresponding scalar coupling and phase-lag entries.

For an atomic permutation `pi`, the input coordination records and receiver-specific parameter vectors use the same permutation. A permutation-compatible evaluator satisfies:

`P_FLiBe(pi · C) = pi · P_FLiBe(C)`.

An evaluator explicitly depending on atom indices, as in the test fixture, records that index dependence as part of its parameterization rule and ordering contract.

## 19. Periodic Images and Edge Multiplicity

The directed graph stores source, receiver, and periodic-image indices. `FLiBeCoordinationState` counts incoming graph records by species; two records with the same source and receiver but distinct image indices contribute twice to the corresponding count.

`phase_derivatives` likewise sums the contributions of all stored directed edges. A parameterization using total incoming count and a phase update using directed-edge multiplicity therefore depend on the same graph semantics through two explicitly identified operations.

Graph construction, cutoff, cell basis, periodic-image selection, and edge ordering are included in the parameterization and integration record.

## 20. Resonance Descriptor and FLiBe Context

`resonance_descriptor(state)` constructs a two-component continuous descriptor:

`D_R = (R_phase, spread_omega)`.

Its phase-order component is:

`R_phase = |(1/N) sum_j exp(i theta_j)|`.

Its frequency-spread component is the population standard deviation:

`spread_omega = sqrt[(1/N) sum_j (omega_j - omega_mean)^2]`.

`FLiBeResonanceDescriptor` binds an `FLiBeConfiguration`, `FLiBeCoordinationState`, `FLiBeThermodynamicState`, `ResonanceState`, and provenance. The computed descriptor uses the supplied continuous resonance state; the FLiBe configuration, coordination, and thermodynamic coordinates remain accessible as its source context.

The constructor requires matching atom, coordination, and oscillator counts, matching species order, and a binary composition derived from the FLiBe configuration.

## 21. Resonance Windows and Regime Coordinates

`ResonanceSpace` defines a finite-dimensional coordinate space, and `ResonanceWindow` supplies strictly ordered finite lower and upper bounds for each coordinate. The reference two-component descriptor can be supplied as a coordinate through `resonance_coordinate` with a matching space dimension.

`classify_resonance_region` evaluates `OUTSIDE`, `BOUNDARY`, or `INSIDE` for the declared window and coordinate. The window bounds, coordinate normalization, classification instant, and history or retention variables are associated with their chosen resonance-regime model.

Phase order, frequency spread, local phase relation, window position, synchronization, phase locking, and coherence retain their individually specified mathematical meanings.

## 22. Coupling to Balanced-Ternary Execution

A selected `FLiBeTernaryInterpretation` supplies `ResonanceProjection`, `TernaryTargetThresholds`, provenance, and optional source metadata. It produces a requested `TernaryState` from a continuous `ResonanceDescriptor` or `ResonanceState`.

The execution state alphabet is `-1/0/1`, including active neutral `0`. The request enters a separate guarded execution operator. Pending opposite-polarity destinations belong to `{-1, 1}` while the retained state is `0`.

Opposite-polarity committed routes have separate legs:

`-1 → 0 → 1`.

`1 → 0 → -1`.

The complete trace preserves the distinct resonance descriptor, request, retained execution state, pending destination, hold, and committed event.

## 23. Resonance-Conditioned Interatomic Energy

`FLiBeTREIPModel` receives a validated FLiBe configuration, graph, initial node features, `FLiBeResonanceDescriptor`, and retained `TernaryExecutionVector`.

`append_flibe_resonance_channels` appends phase order and frequency spread, in that order, to each atom's scalar features. The conditioned energy model then evaluates the selected scalar energy using the retained execution vector.

For atomistic configuration `X`, graph `G`, initial features `Q`, and retained execution `sigma`, the interatomic energy relation may be written:

`E_pot = E_Theta(X, G, augmented_features(D_R), sigma)`.

Coordinate and strain derivatives of the selected differentiable energy branch supply the conservative force and stress operators. Parameter and execution update times are recorded with the energy evaluation.

## 24. Parameter Sensitivity

For fixed graph and oscillator state, define the receiving-node derivative:

`f_j = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

Its parameter sensitivities are:

`partial f_j / partial kappa_j = sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

`partial f_j / partial gamma_j = -kappa_j sum_(i→j) cos(theta_i - theta_j - gamma_j)`.

For a differentiable evaluator `P_FLiBe(C; Lambda)`, derivatives with respect to continuous components of `Lambda` follow the chain rule. Discrete coordination changes are recorded through separately sampled graph and coordination events.

A numerical sensitivity study specifies initial phases, graph, source parameters, perturbation intervals, timestep, observables, and comparison criteria.

## 25. Open-System and Multiscale Parameter Context

The material system can exchange heat, momentum, and species across its declared boundary. Its mechanical and thermodynamic state supplies the inputs selected for coordination sampling and resonance parameterization.

At a coarse scale, an explicit mapping may transfer continuous phase descriptors or parameter fields from fine groups to mesoscale or continuum variables. Such a mapping identifies the source oscillator population, spatial partition, reduction rule, physical state domain, and temporal sampling.

The atomistic phase-parameter tuple, coarse-scale continuous variables, and retained ternary execution channels retain their respective numerical and categorical representations throughout this coupling.

## 26. Exact Invariants and Numerical Checks

The executable parameterization contract includes:

- immutable `FLiBeResonanceParameterization` and `ConstantFLiBeResonanceParameters` records;
- a callable dynamic evaluator or a stored `PhaseDynamicsParameters` object;
- a typed `FLiBeCoordinationState` input;
- finite equal-length coupling and phase-lag tuples;
- nonnegative coupling entries;
- exact parameter-vector cardinality equal to coordination atom count;
- typed provenance and validated source metadata;
- the source requirement for `PRIMARY_SOURCE` provenance;
- retained object identity for successfully evaluated dynamic and fixed parameter objects;
- one phase derivative contribution per stored incoming directed edge;
- retained intrinsic-frequency vector during the reference Euler step;
- deterministic results under identical parameter, graph, state, and time-step inputs.

The parameterization tests exercise invalid source and evaluator types, provenance checks, mismatched cardinality, coordination-driven evaluator behavior, fixed parameter retention, and dispatcher input contracts.

## 27. Reproducibility Record

A reproducible resonance-parameterization evaluation records:

- FLiBe atomic composition, ordered species, geometry, cell, and periodic flags;
- interaction graph construction, cutoff, directed edges, and image indices;
- `FLiBeCoordinationState` and its ordered species-resolved counts;
- dynamic or constant parameterization type, evaluator identity, and resolved parameters;
- `ParameterProvenance`, source identifier, parameter units, and material-state context;
- full coupling and phase-lag tuples, including receiver index ordering;
- resonance phases, intrinsic frequencies, graph-sampling time, and integration timestep;
- computed phase derivatives, updated phases, and continuous descriptor values;
- resonance-window model and classification when selected;
- execution requests and retained/pending/committed ternary events when coupled;
- energy-conditioning inputs, model parameters, mechanical state, and output observables;
- numerical methods, fixed comparison criteria, and deterministic replay identifiers.

The resulting record connects each parameter set to its source coordination state, selected physical context, phase evolution, and downstream conditioning operation.

## 28. Executable Interface Index

| Role | Repository path |
| --- | --- |
| FLiBe species and composition | `src/tr_eif/flibe/species.py`, `src/tr_eif/flibe/composition.py` |
| FLiBe atomic configuration | `src/tr_eif/flibe/configuration.py` |
| FLiBe thermodynamic state | `src/tr_eif/flibe/thermodynamic_state.py` |
| Directed interaction graph | `src/tr_eif/graph/interaction.py`, `src/tr_eif/graph/builder.py` |
| Graph-relative coordination | `src/tr_eif/flibe/coordination.py` |
| FLiBe phase-parameter evaluators | `src/tr_eif/flibe/resonance_parameterization.py` |
| Parameter tuple validation | `src/tr_eif/resonance/parameters.py` |
| Oscillator state and phase wrapping | `src/tr_eif/resonance/state.py` |
| Directed phase derivatives | `src/tr_eif/resonance/dynamics.py` |
| Explicit Euler phase integration | `src/tr_eif/resonance/integrator.py` |
| Phase order and descriptor | `src/tr_eif/resonance/order.py`, `src/tr_eif/resonance/descriptor.py` |
| Resonance coordinate and window | `src/tr_eif/resonance/window.py`, `src/tr_eif/resonance/classification.py` |
| FLiBe descriptor and material binding | `src/tr_eif/flibe/resonance_descriptor.py` |
| FLiBe request interpretation | `src/tr_eif/flibe/ternary_interpretation.py` |
| MD resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| MD ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| FLiBe conditioned interatomic model | `src/tr_eif/flibe/tr_eip.py` |
| Parameter provenance | `src/tr_eif/flibe/units.py` |
| Kuramoto–Sakaguchi source register | `docs/references/kuramoto_sakaguchi_sources.md` |
| FLiBe primary sources | `docs/references/flibe_sources.md` |

## 29. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| FLiBe resonance parameterization | `tests/invariants/test_flibe_resonance_parameterization_invariants.py` |
| FLiBe coordination invariants | `tests/invariants/test_flibe_coordination_invariants.py` |
| FLiBe descriptor context | `tests/invariants/test_flibe_resonance_descriptor_invariants.py` |
| FLiBe interatomic conditioning | `tests/integration/test_flibe_tr_eip.py` |
| Continuous phase integration | `tests/numerical/test_resonance_integration.py` |
| MD resonance propagation | `tests/integration/test_molecular_dynamics_resonance_propagation.py` |
| Resonance-to-ternary mapping | `tests/integration/test_resonance_to_ternary_boundary.py` |
| Resonance and guarded execution | `tests/integration/test_resonance_ternary_execution.py` |
| FLiBe ternary interpretation | `tests/invariants/test_flibe_ternary_interpretation_invariants.py` |
| Graph and geometry invariants | `tests/invariants/test_interaction_graph_invariants.py`, `tests/invariants/test_geometry_invariants.py` |

## 30. Chapter Integration

FLiBe resonance parameterization maps species-resolved graph coordination to typed Kuramoto–Sakaguchi coupling and phase-lag vectors. Dynamic and constant evaluator interfaces share the same oscillator-count, finite-value, and source-binding contracts.

The resulting parameter vectors enter directed continuous phase dynamics at declared atomic configurations and physical times. The continuous resonance descriptor, active-neutral `-1/0/1` execution, and conditioned TR-EIP energy remain connected through explicit mappings and independently recorded state and event variables.
