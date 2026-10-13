
# Ternary State Propagation

## 1. Scope and Coupled State

This chapter specifies balanced-ternary execution during molecular-dynamics calculations in TR-EIF. The executable reference associates one ternary execution node with each atom in a three-dimensional `MolecularDynamicsState` and advances the execution nodes through explicitly requested, guarded events.

The hybrid calculation maintains distinct variables for atomic positions, velocities, cell geometry, continuous resonance dynamics, and retained balanced-ternary execution. Its coupling schedule determines when continuous descriptors are sampled, when targets are requested, when execution events commit, and which retained execution vector conditions subsequent interatomic calculations.

The MD-associated entry point is `propagate_md_ternary_state` in `src/tr_eif/md/ternary_propagation.py`. Its underlying vector executor is `execute_ternary_vector_step` in `src/tr_eif/ternary/vector_execution.py`.

## 2. Balanced-Ternary State Space

The canonical executed state space is:

`T = {-1, 0, 1}`.

The canonical notation is `-1/0/1`, with the executable labels `NEGATIVE`, `NEUTRAL`, and `POSITIVE` defined by `TernaryState`.

State `0` is active neutral. The framework assigns it explicit routing, balancing, mediation, transition staging, retention, damping, and controlled-neutralization roles when the corresponding operators are defined.

A ternary execution value has its declared execution semantics. Atomic charge, coordinate direction, kinetic energy, mechanical force, stress, physical phase of matter, missing data, and numerical error have their own types and state spaces. The continuous atomic and resonance states retain their numerical dimensions throughout the coupled calculation.

`validate_ternary_state` accepts the three integer values or `TernaryState` members and returns a `TernaryState`. `validate_ternary_vector` returns a nonempty tuple of validated states. Boolean inputs are excluded from the ternary-state type contract.

## 3. Retained State and Pending Destination

For execution node `i`, define:

`X_T,i = (sigma_i, p_i)`.

Here `sigma_i ∈ T` is the retained executed state, and `p_i ∈ {-1, 1} or None` is an optional pending destination. The data structure is `TernaryExecutionState(retained_state, pending_target)`.

The exact pending-state invariant is:

`p_i != None implies sigma_i = 0`.

A pending destination therefore records a later nonneutral execution leg while the current retained state is active neutral. Requested target, pending destination, and executed retained state are separate fields.

`TernaryExecutionVector` holds a nonempty tuple of node execution states. Its `node_count`, `retained_states`, and `has_pending_targets` properties expose cardinality, current executed values, and pending-route presence. `from_retained_states` constructs a vector with every pending field initially `None`.

## 4. Requested Targets and Continuous Mappings

An execution request `q_i` belongs to `T`. The MD-associated operator receives `requested_targets` as a tuple of one requested value per atom or as `None` when the pending-route rules permit it.

The repository supplies separately callable continuous-to-ternary mappings. `ternary_target_from_scalar(value, thresholds)` uses two strictly ordered thresholds:

- `value < negative` produces `-1`;
- `negative <= value <= positive` produces `0`;
- `value > positive` produces `1`.

`ResonanceProjection` maps the continuous resonance descriptor to a scalar through phase-order weight, frequency-spread weight, and bias. `ternary_target_from_descriptor` and `ternary_target_from_resonance_state` then evaluate a requested target using the declared thresholds.

These mappings produce requests. A caller constructing an atom-associated request vector specifies the association between descriptor evaluations and execution nodes. `propagate_md_ternary_state` consumes the supplied requests and preserves the associated mechanical state during the execution event.

## 5. Committed Transition Relation

One committed execution leg belongs to the exact relation:

`R_T = {(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 0), (1, 1)}`.

The direct opposite-polarity pairs `(-1, 1)` and `(1, -1)` are excluded. The admissible opposite-polarity routes therefore have two distinct committed legs:

`-1 → 0 → 1`.

`1 → 0 → -1`.

`TernaryTransition(source, target)` validates membership of the committed leg in the relation. Its `changes_state`, `enters_neutral`, and `leaves_neutral` properties describe the committed leg. Self-transitions in the relation are explicit committed events and can retain the same executed state.

## 6. Active-Neutral Routing

`route_ternary_target(retained_state, requested_target)` constructs one admissible route leg. For an opposite-polarity request, the first route has a neutral executed destination and registers the requested polarity as pending.

For example, a requested target `1` from retained state `-1` produces:

`(-1, None) → (0, 1)`.

A subsequent eligible pending-route event produces:

`(0, 1) → (1, None)`.

The corresponding reverse sequence is:

`(1, None) → (0, -1) → (-1, None)`.

Each arrow represents one committed event. `route_pending_target` constructs a pending-route exit from retained active neutral, consuming the pending destination when the event commits.

## 7. Active-Neutral Retention

A pending destination can remain registered during successive execution opportunities. A guard that withholds neutral exit retains both the executed `0` and the pending polarity.

For a pending `1`:

`(0, 1) --hold--> (0, 1)`.

Here `hold` represents an execution opportunity without a committed transition leg. The result carries `route = None`, and `current` equals `previous`.

A request to replace an existing pending destination with a different target is rejected. An omitted request or a request equal to the pending destination permits the pending-route logic to proceed under its guard. Active neutral also admits an explicit committed self-transition `0 → 0` when an ordinary `0` request is routed with no pending destination.

Thus active-neutral residence can be expressed by retention during a guarded hold or by an explicitly committed neutral self-transition; their event records remain distinct.

## 8. Execution Guards

`TernaryExecutionGuard` defines two Boolean permissions: `allow_neutral_entry` and `allow_neutral_exit`.

| Guard constructor | Neutral entry | Neutral exit |
| --- | --- | --- |
| `unrestricted()` | Allowed | Allowed |
| `hold()` | Blocked | Blocked |
| `neutral_entry_only()` | Allowed | Blocked |
| `neutral_exit_only()` | Blocked | Allowed |

The guard applies to neutral-entry and neutral-exit legs. A blocked leg yields a noncommitted execution step with unchanged retained and pending state. A committed self-transition remains governed by the transition relation; `hold()` blocks neutral entry and exit, rather than every possible self-transition.

Execution guards are supplied per node in the vector form. A held node and a committing node may coexist in the same vector execution opportunity.

## 9. Single-Node Execution Order

`execute_ternary_step(state, requested_target=None, guard=None)` performs one guarded execution attempt.

When `state.pending_target` is present, the executor first validates any supplied request against the pending destination. If neutral exit is permitted, it commits the pending leg; otherwise it retains the full execution state with `route = None`.

When no pending destination is present, a requested target is required. The executor obtains a route through `route_ternary_target`, checks the applicable neutral-entry or neutral-exit permission, and either returns a held result or commits the selected route leg.

`TernaryExecutionStep` contains `previous`, `route`, and `current`. Its Boolean `committed` is defined by `route is not None`. In particular:

- guard-blocked execution: `route = None`, `committed = False`;
- committed self-transition: `route` contains the validated self-transition, `committed = True`;
- opposite-polarity first leg: `route` enters `0` and registers the pending destination;
- pending-route second leg: `route` leaves `0` for the pending polarity.

## 10. Vector Execution

`execute_ternary_vector_step(state, requested_targets=None, guards=None)` processes each node in the execution vector in index order. Each node receives its own execution state, requested target, and execution guard.

The requested vector, when provided, has exactly one ternary target per node. With `requested_targets=None`, every node must already have a pending target for its execution attempt; a node without pending state requires an explicit request. Missing guards are replaced by `TernaryExecutionGuard.unrestricted()` for all nodes.

The immutable result `TernaryVectorExecutionStep` contains `previous`, `node_steps`, and `current`, all with the same node cardinality. Its counters are:

`committed_count = sum(step.committed for step in node_steps)`.

`held_count = node_count - committed_count`.

The counters refer to committed execution legs and held execution attempts, respectively. A committed self-transition contributes to `committed_count`.

## 11. MD-Associated Execution Bridge

The public call is:

`propagate_md_ternary_state(md_state, ternary_state, requested_targets=None, guards=None)`.

Its executable sequence is:

1. Validate `MolecularDynamicsState` and `TernaryExecutionVector` input types.
2. Require one execution node per MD atom.
3. Validate the request tuple and guard tuple cardinalities when supplied.
4. Require every supplied guard to be a `TernaryExecutionGuard`.
5. Execute one vector opportunity through `execute_ternary_vector_step`.
6. Return `MolecularDynamicsTernaryStep` containing the MD state, supplied requests, and execution result.

`MolecularDynamicsTernaryStep` exposes `previous`, `current`, `committed_count`, and `held_count` through the underlying vector result. The bridge retains the input `md_state` object, including Cartesian positions, velocities, masses, cell, mechanical step, and mechanical time.

The ternary opportunity is recorded on its own execution schedule. A caller specifies how those opportunities correspond to mechanical integration steps and continuous resonance updates.

## 12. Three-Node Execution Example

Consider an MD state with three atoms and the initial retained vector:

`sigma = (-1, 0, 1)`.

Set every pending destination to `None`, and supply:

`q = (1, 1, -1)`.

With unrestricted guards, the first vector execution opportunity produces:

`retained_after = (0, 1, 0)`.

`pending_after = (1, None, -1)`.

The committed legs are `-1 → 0`, `0 → 1`, and `1 → 0`; therefore `committed_count = 3` and `held_count = 0`.

At the next opportunity, supplying the same requested vector permits the two pending exits and a self-transition on the middle node:

`retained_after = (1, 1, -1)`.

`pending_after = (None, None, None)`.

The second opportunity contains the legs `0 → 1`, `1 → 1`, and `0 → -1`. Each transition is recorded independently at its node. The example's first opportunity and the separate completion of opposite requests follow the behavior exercised in the existing vector and MD integration tests.

## 13. Coupling to Resonance and Conditioned Energy

A coupled computation may define an explicit chain:

`X_R → D_R → request vector → U_T → retained execution vector → E(R, G, Q, execution)`.

Here `X_R` is the continuous oscillator state; `D_R` is a continuous resonance descriptor; `U_T` is the guarded ternary execution operator; `R` is three-dimensional atomic geometry; `G` is the interaction graph; and `Q` denotes typed node features.

`ReferenceEnergyModel.evaluate(configuration, graph, features, execution)` accepts a `TernaryExecutionVector` and computes conditioned equivariant features and a scalar energy. `velocity_verlet_step` also accepts an explicitly supplied execution vector for its mechanical force evaluations.

The caller selects whether a mechanical step uses the execution vector retained before or after an execution opportunity. The selected vector and its event index are part of the coupled trace. During `propagate_md_ternary_state`, the mechanical coordinates and energy-evaluation inputs are retained as supplied.

## 14. Numerical Schedules and Open-System Coupling

Let `n` index mechanical steps, `j` index resonance integration steps, and `k` index ternary execution opportunities. A declared composition may be written:

`X_MD[n+1] = Phi_MD(X_MD[n]; dt_MD, execution[k])`.

`X_R[j+1] = Phi_R(X_R[j]; dt_R, G_sample)`.

`q[k] = M_request(X_R[j+1], X_MD[n+1], context)`.

`X_T[k+1] = U_T(X_T[k], q[k], guards[k])`.

The displayed order is one explicit composition. A realization records the ordering actually used, the graph-sampling instant, request-generation rule, execution guards, and conditioning state supplied to the next energy and force evaluation.

Boundary controls, dissipation, thermal coupling, pressure coupling, and material exchange remain attached to their declared physical and numerical operators. Ternary execution indices and mechanical physical time are recorded as separate quantities.

## 15. Exact Invariants and Event Trace

The following structural invariants are evaluated through exact categorical comparisons:

- executed node values belong to `{-1, 0, 1}`;
- pending values belong to `{-1, 1}` or are `None`;
- a present pending value requires retained active neutral;
- committed legs belong to the seven-pair transition relation;
- each opposite-polarity route passes through a committed neutral-entry leg and a separate neutral-exit leg;
- a held attempt has `route = None`, while a committed self-transition has an explicit route;
- vector node count equals MD atom count;
- `committed_count + held_count = node_count`;
- retained and pending states are preserved by a blocked event;
- the MD state referenced by the ternary bridge is retained through that execution opportunity.

An event trace records MD step and time, execution-opportunity index, input retained and pending vectors, supplied request vector, per-node guard permissions, per-node committed routes, output retained and pending vectors, and committed/held counts.

Numerical resonance descriptors and mechanically derived quantities preserve their declared floating-point methods, units, and tolerances; exact ternary states, route membership, and event cardinality use exact equality.

## 16. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| MD-associated ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| Mechanical state | `src/tr_eif/md/state.py` |
| Ternary state and vector validation | `src/tr_eif/ternary/state.py` |
| Committed transition relation | `src/tr_eif/ternary/transition.py` |
| Active-neutral route construction | `src/tr_eif/ternary/routing.py` |
| Retained and pending execution state | `src/tr_eif/ternary/execution.py` |
| Guard definitions | `src/tr_eif/ternary/guard.py` |
| Multi-node execution | `src/tr_eif/ternary/vector_execution.py` |
| Scalar request thresholds | `src/tr_eif/ternary/target.py` |
| Continuous resonance projection | `src/tr_eif/ternary/projection.py` |
| Conditioned energy model | `src/tr_eif/energy/model.py` |
| Force-driven mechanical step | `src/tr_eif/md/execution.py` |
| MD ternary integration tests | `tests/integration/test_molecular_dynamics_ternary_propagation.py` |
| Resonance-to-execution tests | `tests/integration/test_resonance_ternary_execution.py` |
| Continuous request boundary tests | `tests/integration/test_resonance_to_ternary_boundary.py` |
| Transition invariant tests | `tests/invariants/test_ternary_transition_invariant.py` |
| Vector execution invariant tests | `tests/invariants/test_ternary_vector_execution.py` |

The tests exercise opposite-polarity routing, pending-route completion, guarded retention, per-node independent execution, exact route invariants, explicit requested targets, MD-state retention, input cardinality, and deterministic repetition.

## 17. Summary

TR-EIF ternary propagation operates on a retained `-1/0/1` execution state per MD atom. The active-neutral state supports explicit intermediate routing and retention, while pending destinations and execution guards control subsequent committed legs.

The MD-associated operator records one vector execution opportunity while retaining the supplied mechanical state. Continuous resonance mappings, energy-conditioned interatomic computation, and force-driven MD advancement are composed through explicitly supplied inputs and an event-order trace.
