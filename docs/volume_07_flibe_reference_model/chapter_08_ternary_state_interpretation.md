
# Ternary State Interpretation

## 1. Scope and Coupled State

This chapter defines the FLiBe resonance-to-ternary interpretation and its connection to retained balanced-ternary execution in TR-EIF. The represented material system combines three-dimensional atomic geometry, thermodynamic state, continuous nonlinear resonance evolution, an explicit request mapping, and atom-associated execution events.

The state-processing chain is:

`FLiBe configuration and resonance state → continuous resonance descriptor → scalar projection → requested -1/0/1 target → guarded execution → retained execution vector → conditioned TR-EIP energy`.

`FLiBeTernaryInterpretation` generates a requested target. `TernaryExecutionState` and `TernaryExecutionVector` represent retained and pending execution states. The caller selects the mapping from descriptor samples to atom-associated requests and the order of their execution opportunities.

## 2. FLiBe Material Context

`FLiBeConfiguration` binds an ordered Li/Be/F atom inventory to an `AtomicConfiguration` with Cartesian positions, optional three-dimensional cell vectors, and periodic-axis flags. `FLiBeThermodynamicState` stores finite positive absolute temperature in kelvin and finite nonnegative pressure in pascal.

`FLiBeResonanceDescriptor` associates this material configuration and thermodynamic state with `FLiBeCoordinationState`, a continuous `ResonanceState`, provenance, and optional source metadata. Its constructor checks the configuration, coordination, and oscillator cardinalities and the ordering of the atomic species.

The exact binary reference composition `2 LiF : 1 BeF2` has component fractions `(2/3, 1/3)` and atomic ratio `Li:Be:F = 2:1:4`. Material composition, formal charge, thermodynamic state, oscillator phase, and execution state are represented by their respective typed variables.

## 3. Continuous Resonance State

For `N >= 1` oscillators, `ResonanceState` stores phases `theta_j` and intrinsic angular frequencies `omega_j`. The reference directed Kuramoto–Sakaguchi dynamics for receiving node `j` are:

`d theta_j/dt = omega_j + kappa_j sum_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

Here `G` is the selected directed interaction graph, `kappa_j >= 0` is receiving-node coupling, and `gamma_j` is receiving-node phase lag. The graph, phase parameters, physical sampling instant, and integration step identify a continuous update.

The reference phase integrator uses:

`theta_j,next = wrap(theta_j + dt_R d theta_j/dt)`.

`omega_j,next = omega_j`.

The phase update and ternary execution use separate operators and event indices.

## 4. Continuous Resonance Descriptor

`resonance_descriptor(state)` constructs `ResonanceDescriptor(phase_order, frequency_spread)`. Its scalar components are:

`R_phase = |(1/N) sum_j exp(i theta_j)|`.

`omega_mean = (1/N) sum_j omega_j`.

`spread_omega = sqrt[(1/N) sum_j (omega_j - omega_mean)^2]`.

The phase-order value and population-frequency spread form the coordinate:

`D_R = (R_phase, spread_omega)`.

`FLiBeResonanceDescriptor.descriptor`, `.coordinate`, `.phase_order`, and `.frequency_spread` expose these values from its bound continuous resonance state. The material configuration, coordination, and thermodynamic state remain available in that containing record.

## 5. Scalar Projection Operator

`ResonanceProjection` contains `phase_order_weight`, `frequency_spread_weight`, and `bias`. For descriptor `D_R`, it evaluates:

`u_R = w_R R_phase + w_omega spread_omega + b`.

All three stored coefficients are finite real numbers, with Boolean inputs excluded. At least one of `w_R` and `w_omega` is nonzero. The coefficients and bias are explicitly supplied parameters of the chosen interpretation.

The projected coordinate `u_R` is a continuous scalar used as the input to the next target mapping. The oscillator state and its individual phases and frequencies remain available for subsequent continuous integration steps.

## 6. Ordered Target Thresholds

`TernaryTargetThresholds` stores the two finite ordered values:

`h_negative < h_positive`.

`ternary_target_from_scalar(u_R, thresholds)` applies the exact request mapping:

| Scalar condition | Requested `TernaryState` | Integer value |
| --- | --- | ---: |
| `u_R < h_negative` | `NEGATIVE` | `-1` |
| `h_negative <= u_R <= h_positive` | `NEUTRAL` | `0` |
| `u_R > h_positive` | `POSITIVE` | `1` |

Both threshold equalities belong to the neutral request interval. The thresholds are part of the supplied interpretation parameters and are recorded with their source and numerical convention.

## 7. FLiBeTernaryInterpretation Contract

`FLiBeTernaryInterpretation` is an immutable record with:

- `projection`: one `ResonanceProjection` instance;
- `thresholds`: one `TernaryTargetThresholds` instance;
- `provenance`: one `ParameterProvenance` member;
- `source`: an optional source identifier.

The record checks these input types, requires a source identifier for `PRIMARY_SOURCE` provenance, and validates provided source strings as nonempty and free of leading or trailing whitespace.

The interpretation retains its original projection and thresholds objects. Its numerical parameter selection belongs to the declared source, derived relation, calibration procedure, author-defined parameter set, or test fixture associated with that record.

## 8. Descriptor and State Entry Points

`FLiBeTernaryInterpretation.target_from_descriptor(descriptor)` accepts a `ResonanceDescriptor` and returns one `TernaryState` request. The public function `interpret_flibe_ternary_target(interpretation, descriptor)` delegates to that method after validating the interpretation type.

`FLiBeTernaryInterpretation.target_from_resonance_state(state)` accepts a `ResonanceState`, constructs its continuous descriptor, applies the stored projection and thresholds, and returns one requested target.

The generic functions `ternary_target_from_descriptor` and `ternary_target_from_resonance_state` provide the corresponding operations in `src/tr_eif/ternary/projection.py`. Both paths retain the supplied continuous resonance state during target generation.

## 9. Exact Target and Execution Types

`TernaryState` is an integer enumeration with canonical values `-1/0/1`. `validate_ternary_state` accepts those integer values or enumeration members, excluding Boolean input. `validate_ternary_vector` constructs a nonempty tuple of validated states.

A requested target has type `TernaryState`. A retained execution node has type `TernaryExecutionState`, which stores `retained_state` and `pending_target`. An executed vector has type `TernaryExecutionVector`.

The interpretation call returns a request. The execution call returns a retained state, any pending destination, and a committed or held event record. This separation determines the exact point at which a projected request becomes an executed state.

## 10. Deterministic Projection Example

The interpretation fixture in `tests/invariants/test_flibe_ternary_interpretation_invariants.py` uses:

`w_R = 1.0`, `w_omega = -1.0`, `b = 0.0`.

`h_negative = -0.25`, `h_positive = 0.25`.

Its requested targets are:

| `R_phase` | `spread_omega` | `u_R` | Requested target |
| ---: | ---: | ---: | ---: |
| `0.0` | `1.0` | `-1.0` | `-1` |
| `0.5` | `0.5` | `0.0` | `0` |
| `1.0` | `0.0` | `1.0` | `1` |
| `0.25` | `0.5` | `-0.25` | `0` |
| `0.5` | `0.25` | `0.25` | `0` |

These values are supplied by the deterministic `TEST_FIXTURE` interpretation. Other source-identified projection weights and thresholds define their own requested-target mapping.

## 11. Projection Bias and Target Sensitivity

With fixed continuous descriptor, changing the bias changes the projected scalar by the same amount:

`u_R(b + delta_b) = u_R(b) + delta_b`.

Changing weights gives the exact scalar difference:

`delta_u_R = delta_w_R R_phase + delta_w_omega spread_omega + delta_b`.

The requested target changes when the resulting scalar crosses one of the two declared thresholds according to the exact comparisons of Section 6. The fixture tests include different projection signs, bias values, and threshold intervals applied to the same descriptor.

A numerical sensitivity record retains the descriptor, supplied parameter sets, threshold values, projected scalar, and resulting requested target for each comparison.

## 12. Node-Associated Request Construction

A single call to `interpret_flibe_ternary_target` yields one requested `TernaryState`. The MD-associated execution bridge expects one requested value for each execution node when a request vector is supplied.

For an atom count `N`, a caller-defined request construction has the form:

`q[k] = (q_0[k], ..., q_(N-1)[k])`.

Each `q_i[k]` can be obtained from a declared descriptor sampling and interpretation rule. A globally sampled descriptor may be reused across nodes by an explicit broadcast policy, while node-specific descriptor mappings may produce distinct requests.

The request-construction policy, atomic index correspondence, descriptor source, and sampling time are recorded before `execute_ternary_vector_step` or `propagate_md_ternary_state` is invoked.

## 13. Committed Transition Relation

For one retained executed state `sigma`, the committed transition relation is:

`R_T = {(-1,-1), (-1,0), (0,-1), (0,0), (0,1), (1,0), (1,1)}`.

`TernaryTransition(source, target)` validates one committed leg of this relation. An opposite-polarity request is routed through active neutral using separate events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

Each arrow represents one committed execution event. `TernaryTransition.changes_state`, `.enters_neutral`, and `.leaves_neutral` identify the relevant relation of each leg to the active-neutral state.

## 14. Active-Neutral Execution State

The executed value `0` is active neutral. Its roles include balancing, routing, damping, mediation, transition staging, retention, and controlled neutralization when bound to the selected execution and conditioning operators.

`TernaryExecutionState` stores:

`X_T,i = (sigma_i, p_i)`.

`sigma_i in {-1,0,1}`.

`p_i in {-1,1} or None`.

The exact pending-state invariant is:

`p_i != None implies sigma_i = 0`.

Active-neutral retention can extend across multiple execution opportunities according to the supplied guards. The retained value and pending destination remain separate fields in every such state.

## 15. Requested Opposite Polarity and Pending Route

`route_ternary_target` transforms an opposite-polarity request into a first leg entering active neutral and retaining the requested polarity as a pending destination.

For retained `-1` and requested `1`:

`(-1, None) → (0, 1)`.

For retained `1` and requested `-1`:

`(1, None) → (0, -1)`.

A subsequent eligible pending-route execution uses `route_pending_target`:

`(0, 1) → (1, None)`.

`(0, -1) → (-1, None)`.

Pending destinations have values `-1` or `1`, while `0` remains the retained executed state during an intermediate pending period.

## 16. Execution Guards

`TernaryExecutionGuard` contains the Boolean permissions `allow_neutral_entry` and `allow_neutral_exit`. The executable constructors provide:

| Constructor | Neutral entry | Neutral exit |
| --- | --- | --- |
| `unrestricted()` | True | True |
| `hold()` | False | False |
| `neutral_entry_only()` | True | False |
| `neutral_exit_only()` | False | True |

The guard is evaluated for the selected committed route leg. If the leg requires an entry or exit whose permission is false, the event retains its prior execution state and produces `route = None`.

A committed self-transition such as `0 → 0` is represented explicitly by its admissible transition route. The guard constructors control neutral entry and exit; their flags remain separate from the committed self-transition semantics.

## 17. Hold and Committed Self-Transition

`TernaryExecutionStep` contains `previous`, `route`, and `current`. Its `committed` property is defined by:

`committed = (route is not None)`.

A guarded hold has `route = None`, leaves `current` equal to `previous`, and contributes to the held count in vector execution.

A committed self-transition has an explicit route with equal source and target, such as `(0,0)` or `(1,1)`. It leaves the retained numeric value unchanged and contributes to the committed count.

These two event forms are preserved in the trace through the presence or absence of the route field.

## 18. Pending-Target Retention

When `pending_target` is present, `execute_ternary_step` first validates an optionally supplied request against the pending destination. A supplied request for the same destination is accepted; the caller may also omit it.

With `allow_neutral_exit = False`, execution retains the entire pending state:

`(0, 1) --hold--> (0, 1)`.

With neutral exit permitted, one committed leg resolves the pending destination. A request with a different destination is rejected according to the pending-route contract.

A state without a pending destination requires a supplied request. The event ordering records each opportunity, guard, pending value, and committed result.

## 19. Vector Execution

`TernaryExecutionVector` stores a nonempty tuple of `TernaryExecutionState` objects and exposes `node_count`, `retained_states`, and `has_pending_targets`.

`execute_ternary_vector_step(state, requested_targets=None, guards=None)` processes nodes in index order. A supplied request vector must contain one `-1/0/1` target per node; a supplied guard tuple must contain one typed guard per node.

When the request tuple is omitted, each processed node must already have a pending destination. Omitted guards are replaced by unrestricted guards for all nodes.

`TernaryVectorExecutionStep` stores previous and current vectors and the per-node execution steps. Its exact counters satisfy:

`committed_count = sum_i indicator(node_step_i.committed)`.

`held_count = node_count - committed_count`.

A committed self-transition contributes to `committed_count`.

## 20. MD-Associated Ternary Event

The public mechanical bridge is:

`propagate_md_ternary_state(md_state, ternary_state, requested_targets=None, guards=None)`.

Its executable contract assigns one ternary execution node to each atom in `MolecularDynamicsState`. It validates node and request/guard cardinalities and delegates execution to `execute_ternary_vector_step`.

`MolecularDynamicsTernaryStep` retains the supplied `md_state` object and records the requested vector and the previous/current execution vectors. Its `committed_count` and `held_count` forward the vector-result counters.

This operator retains Cartesian positions, velocities, masses, cell, MD step, and physical time during its one execution opportunity. A caller specifies how the execution opportunity is scheduled relative to MD advancement.

## 21. Three-Node Route Example

Consider three retained execution nodes with initial states:

`sigma = (-1, 0, 1)`.

`pending = (None, None, None)`.

Supply the requested vector and unrestricted guards:

`q = (1, 1, -1)`.

The first committed event on each node gives:

`sigma_after = (0, 1, 0)`.

`pending_after = (1, None, -1)`.

At the next opportunity, resupplying the same requested vector gives:

`sigma_after = (1, 1, -1)`.

`pending_after = (None, None, None)`.

The middle node commits a self-transition `1 → 1` on the second opportunity; the outer nodes complete their pending routes. Both opportunities contain three committed legs with unrestricted guards.

## 22. Continuous Resonance and Execution Clocks

Let `n` index mechanical steps, `j` resonance-integration steps, and `k` ternary execution opportunities. A declared coupling schedule may take the form:

`X_R[j+1] = Phi_R(X_R[j], dt_R; G_sample, P_R)`.

`D_R[j+1] = resonance_descriptor(X_R[j+1])`.

`q[k] = M_request(D_R[j+1], context)`.

`X_T[k+1] = U_exec(X_T[k], q[k], guards[k])`.

`X_MD[n+1] = Phi_MD(X_MD[n], dt_MD; retained(X_T[k+1]))`.

The actual realization records graph sampling, the interpretation parameter set, request construction, execution opportunity, force-conditioning state, and the physical time associated with each operation. The equations identify separately callable roles assembled by that schedule.

## 23. FLiBe TR-EIP Energy Conditioning

`FLiBeTREIPModel.evaluate` accepts a validated `FLiBeConfiguration`, `InteractionGraph`, `NodeFeatureVector`, `FLiBeResonanceDescriptor`, and `TernaryExecutionVector`.

`append_flibe_resonance_channels` appends continuous `phase_order` and `frequency_spread` scalar channels, in that order, to each atom's existing scalar features while retaining vector features.

The underlying `TernaryConditioning` supplies three explicit feature scales:

`negative_scale`, `neutral_scale`, `positive_scale`.

`condition_feature_vector` selects the scale from each node's retained executed state and applies it to that node's scalar and Cartesian vector features. The conditioned layer enters `ReferenceEnergyModel` and its invariant scalar energy functional.

The energy calculation uses the retained execution vector supplied at its call boundary. The model parameters, geometry, graph, resonance descriptor, and selected execution opportunity are recorded with the energy output.

## 24. Spatial Geometry and Node Indexing

Under an orthogonal spatial transformation `Q in O(3)` and translation `b`, positions and polar vector features transform by their declared E(3) action. `ResonanceProjection` acts on continuous scalar descriptor components. `TernaryState` remains a categorical execution value.

For consistent atom relabeling, the request vector, retained execution vector, graph node indices, and node features use the corresponding permutation. A global resonance descriptor broadcast to all nodes uses an explicitly identified broadcast mapping.

The material geometry, oscillator state, requested target, retained execution state, and physical phase-state variables preserve their individual source and target spaces throughout these mappings.

## 25. Provenance and Parameter Identification

`ParameterProvenance` identifies source classes including `PRIMARY_SOURCE`, `DERIVED`, `CALIBRATED`, `AUTHOR_DEFINED`, `BENCHMARK`, and `TEST_FIXTURE`. `FLiBeTernaryInterpretation` stores the selected class and optional source string alongside its projection and thresholds.

A parameter identification study specifies the training or reference data, resonance-descriptor sampling, projection weights, bias, threshold values, objective or selection method, and the physical state domain used to determine the parameter set.

When a numerical study compares multiple parameter sets, each run retains its original parameters and computed request and execution histories. The selected model and source identifiers accompany the resulting interatomic observable trace.

## 26. Exact Invariants and Numerical Operations

The executable structural contracts include:

- exact requested and retained values in `{-1, 0, 1}`;
- nonempty validated ternary vectors with Boolean inputs excluded;
- finite projection coefficients, with at least one nonzero descriptor weight;
- finite strictly ordered target thresholds;
- inclusive neutral target interval at both threshold equalities;
- immutable typed FLiBe interpretation with explicit provenance and source validation;
- pending destination in `{-1, 1}` or `None`, with retained `0` when pending;
- committed transition membership in the seven-pair relation;
- separate committed neutral-entry and neutral-exit events for opposite polarities;
- held opportunities distinguished from committed self-transitions by route presence;
- request, guard, and execution-vector cardinality matched to the selected atom count;
- `committed_count + held_count = node_count` for vector execution.

Continuous projection values and oscillator integration use the declared floating-point method. Exact threshold branch decisions, state membership, transition relation, pending-target identities, and event counts use the corresponding exact categorical comparisons.

## 27. Reproducibility and Event Record

A reproducible FLiBe ternary-interpretation calculation records:

- atomic species, composition, ordered geometry, and thermodynamic state;
- interaction graph, coordination state, and resonance parameterization;
- oscillator phases, intrinsic frequencies, phase-coupling parameters, and integration times;
- continuous resonance descriptor, projection weights, bias, and target thresholds;
- interpretation provenance, source identity, and parameter-selection procedure;
- projected scalar and exact requested `TernaryState`;
- caller-defined node association and request-vector construction;
- previous retained and pending execution values, guards, routes, holds, and committed events;
- resulting retained execution vector supplied to energy and force operators;
- MD state, graph and feature inputs, mechanical step and physical time;
- deterministic replay inputs, output records, and numerical comparison settings.

Each record binds target generation to its continuous descriptor and each committed event to its previous and resulting execution state.

## 28. Executable Interface Index

| Function | Repository path |
| --- | --- |
| FLiBe interpretation and public target function | `src/tr_eif/flibe/ternary_interpretation.py` |
| FLiBe resonance descriptor and context | `src/tr_eif/flibe/resonance_descriptor.py` |
| FLiBe coordination | `src/tr_eif/flibe/coordination.py` |
| FLiBe configuration and thermodynamic state | `src/tr_eif/flibe/configuration.py`, `src/tr_eif/flibe/thermodynamic_state.py` |
| Interpretation provenance | `src/tr_eif/flibe/units.py` |
| Base continuous descriptor | `src/tr_eif/resonance/descriptor.py` |
| Resonance phase state and dynamics | `src/tr_eif/resonance/state.py`, `src/tr_eif/resonance/dynamics.py` |
| Resonance projection | `src/tr_eif/ternary/projection.py` |
| Scalar ternary threshold mapping | `src/tr_eif/ternary/target.py` |
| Ternary enumeration and validation | `src/tr_eif/ternary/state.py` |
| Committed transition relation | `src/tr_eif/ternary/transition.py` |
| Active-neutral route construction | `src/tr_eif/ternary/routing.py` |
| Retained/pending execution | `src/tr_eif/ternary/execution.py` |
| Execution guards | `src/tr_eif/ternary/guard.py` |
| Vector execution | `src/tr_eif/ternary/vector_execution.py` |
| MD-associated ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| Ternary feature conditioning | `src/tr_eif/equivariant/conditioning.py` |
| FLiBe TR-EIP energy | `src/tr_eif/flibe/tr_eip.py` |
| Resonance target and transition specifications | `docs/specifications/ternary_state_specification.md`, `docs/specifications/transition_semantics.md` |

## 29. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| FLiBe interpretation, projection, and provenance | `tests/invariants/test_flibe_ternary_interpretation_invariants.py` |
| Scalar threshold and resonance-region boundaries | `tests/integration/test_resonance_to_ternary_boundary.py` |
| Resonance requests and guarded execution | `tests/integration/test_resonance_ternary_execution.py` |
| Ternary transitions | `tests/invariants/test_ternary_transition_invariant.py` |
| Per-node vector execution | `tests/invariants/test_ternary_vector_execution.py` |
| MD ternary execution bridge | `tests/integration/test_molecular_dynamics_ternary_propagation.py` |
| FLiBe resonance context | `tests/invariants/test_flibe_resonance_descriptor_invariants.py` |
| FLiBe TR-EIP conditioned energy | `tests/integration/test_flibe_tr_eip.py` |
| Ternary feature conditioning | `tests/invariants/test_ternary_conditioning_invariants.py` |
| Continuous resonance numerical integration | `tests/numerical/test_resonance_integration.py` |

The tests exercise target-generation arithmetic and threshold equality, source and parameter typing, immutable interpretation records, pending-route completion, guarded retention, committed self-transitions, vector cardinality, and energy-conditioning interfaces with their declared fixtures.

## 30. Chapter Integration

FLiBe ternary interpretation converts a continuous resonance descriptor into a requested `-1/0/1` target through an explicitly supplied linear projection and ordered thresholds. The active-neutral execution layer processes that request through retained, pending, guarded, held, and committed states on its own event schedule.

The resulting retained execution vector conditions the FLiBe TR-EIP scalar energy through the selected geometric features and continuous resonance channels. Atomic motion, thermodynamic variables, oscillator dynamics, categorical execution, and material observables remain connected by their declared mapping and sampling operations.
