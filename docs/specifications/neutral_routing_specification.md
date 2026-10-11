# Neutral Routing Specification

## 1. Scope

This document defines the repository-level active-neutral routing specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- active-neutral routing state;
- opposite-polarity mediation;
- requested target separation;
- retained executed state;
- pending target semantics;
- first-leg routing;
- active-neutral residence;
- second-leg routing;
- route completion;
- execution guards;
- hold semantics;
- committed self-transitions;
- pending-target immutability;
- multi-node execution;
- deterministic routing;
- trace requirements;
- implementation correspondence;
- prohibited semantic reductions.

The canonical balanced ternary state specification is defined in:

`docs/specifications/ternary_state_specification.md`

Committed transition semantics are defined in:

`docs/specifications/transition_semantics.md`

---

## 2. Canonical Ternary State Space

The balanced ternary execution state space is:

`T = {-1, 0, 1}`

The canonical notation is:

`-1/0/1`

The states:

`-1`

and:

`1`

are opposite ternary polarities.

The state:

`0`

is active neutral.

---

## 3. Active Neutral State

State `0` is an executed state.

It is not a passive placeholder between `-1` and `1`.

Its permitted semantic roles include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

A concrete model may use one or more of these roles when explicitly defined.

---

## 4. Active Neutral Is Not Missing Data

The state:

`0`

must not encode:

- missing data;
- invalid data;
- NaN;
- numerical error;
- unknown state;
- abstention;
- unavailable observable;
- absent validation result.

Absence and invalidity remain separate semantic categories.

Therefore:

`missing ≠ 0`

`invalid ≠ 0`

`unknown ≠ 0`

`error ≠ 0`

---

## 5. Executed Retained State

The retained executed state is:

`t_exec ∈ T`

It represents the state committed by the execution layer.

The retained state persists until another committed execution leg changes it.

A request alone does not change:

`t_exec`

---

## 6. Requested Target

A requested target is:

`t_target ∈ T`

The requested target identifies a desired ternary destination.

It is not automatically the executed state.

Therefore:

`target ≠ executed state`

is an architectural distinction.

A target becomes executed only through an admissible committed transition leg.

---

## 7. Pending Target

A pending target is:

`t_pending ∈ {-1, 1}`

or no pending target is present.

A pending target represents a nonneutral destination that remains unresolved after an opposite-polarity route has entered active neutral.

The pending target is not an executed state.

Therefore:

`pending ≠ executed`

A pending target is also not active neutral.

Therefore:

`pending ≠ 0`

---

## 8. Pending State Requirement

A non-null pending target is valid only when:

`t_exec = 0`

Therefore:

`t_pending ≠ NONE`

implies:

`t_exec = 0`

A pending target attached to retained state `-1` or `1` is invalid.

---

## 9. Opposite-Polarity Definition

The direct opposite-polarity pairs are:

`(-1, 1)`

and:

`(1, -1)`

These pairs are not admissible committed transition legs.

---

## 10. Direct Opposite Transition Prohibition

The committed transitions:

`-1 → 1`

and:

`1 → -1`

are forbidden.

This prohibition applies to each committed execution event.

It is not bypassed by:

- resonance magnitude;
- energy magnitude;
- force magnitude;
- time-step size;
- graph state;
- model scale;
- requested-target urgency.

---

## 11. Required Opposite-Polarity Routes

An opposite-polarity request must be decomposed into separate committed legs.

The route:

`-1 → 1`

must execute as:

`-1 → 0`

followed later by:

`0 → 1`

The route:

`1 → -1`

must execute as:

`1 → 0`

followed later by:

`0 → -1`

Each arrow is one separate execution event.

---

## 12. First-Leg Routing

For retained state:

`t_exec = -1`

and requested target:

`t_target = 1`

the first committed route is:

`-1 → 0`

with:

`t_pending = 1`

For retained state:

`t_exec = 1`

and requested target:

`t_target = -1`

the first committed route is:

`1 → 0`

with:

`t_pending = -1`

---

## 13. First-Leg Result

After the first leg of an opposite-polarity route:

`t_exec = 0`

The opposite destination remains pending.

For the negative-to-positive route:

`(t_exec, t_pending) = (0, 1)`

For the positive-to-negative route:

`(t_exec, t_pending) = (0, -1)`

The final polarity has not yet executed.

---

## 14. Pending Target Registration

Pending target registration occurs only when an opposite-polarity request is routed through active neutral.

A direct request:

`-1 → 0`

does not require a pending target.

A direct request:

`1 → 0`

does not require a pending target.

A direct request:

`0 → -1`

does not create a pending target.

A direct request:

`0 → 1`

does not create a pending target.

---

## 15. Active-Neutral Residence

After opposite-polarity first-leg execution, active neutral may persist across later execution opportunities.

The state may therefore remain:

`t_exec = 0`

with:

`t_pending ∈ {-1, 1}`

until neutral exit becomes eligible.

There is no requirement that the second leg execute in the immediately following numerical or execution step.

---

## 16. Pending Residence and Hold

When a pending target exists and active-neutral exit is not authorized, the execution attempt commits no transition leg.

The state remains unchanged:

`(0, t_pending) → (0, t_pending)`

as retained execution state.

This is a held execution attempt.

It is represented by:

`route = None`

in the executable reference.

A held attempt is distinct from a committed:

`0 → 0`

self-transition.

---

## 17. Hold Is Not a Committed Transition

When:

`route = None`

no ternary transition leg is committed.

The current execution state equals the previous execution state.

Therefore:

`hold ≠ committed self-transition`

This distinction must remain visible in execution traces when committed-event identity matters.

---

## 18. Committed Self-Transitions

The canonical transition system separately permits:

`-1 → -1`

`0 → 0`

`1 → 1`

These are committed retention transitions.

A committed self-transition contains a route.

A held execution attempt does not.

Therefore:

`committed retention ≠ hold`

---

## 19. Second-Leg Routing

If:

`t_exec = 0`

and:

`t_pending = 1`

the pending route may complete through:

`0 → 1`

If:

`t_exec = 0`

and:

`t_pending = -1`

the pending route may complete through:

`0 → -1`

The second leg is a new committed execution event.

---

## 20. Route Completion

After successful second-leg execution:

`t_exec = t_pending_previous`

and the pending target is cleared.

Therefore the completed states are:

`(0, 1) → (1, NONE)`

or:

`(0, -1) → (-1, NONE)`

No pending target remains after completion.

---

## 21. Pending Target Cannot Be Neutral

A pending target must not be:

`0`

because active neutral is the executed mediation state, not the unresolved destination of an opposite-polarity route.

Therefore:

`t_pending ∈ {-1, 1}`

only.

---

## 22. Pending Target Cannot Equal Pre-Neutral Origin

When a pending target is registered by first-leg routing, it must be opposite to the pre-neutral source state.

For:

`-1 → 0`

a valid pending opposite target is:

`1`

For:

`1 → 0`

a valid pending opposite target is:

`-1`

The route constructor rejects a pending target equal to the pre-neutral source.

---

## 23. Existing Pending Target Has Priority

If an execution state already contains a pending target, pending-route handling takes precedence over ordinary target routing.

The executor does not discard the pending route and create another route from the same state.

---

## 24. Pending Target Replacement Is Forbidden

A newly supplied requested target cannot replace an existing pending target.

If:

`t_pending = 1`

then a new request:

`t_target = -1`

does not replace the pending destination.

If:

`t_pending = -1`

then a new request:

`t_target = 1`

does not replace the pending destination.

The executable reference rejects such replacement.

---

## 25. Matching Request During Pending Route

A caller may supply a requested target while a pending route exists only when the supplied request equals the existing pending target.

This equality does not create a new route.

The existing pending route remains authoritative.

---

## 26. Pending Route Without New Request

A pending route may be processed without supplying a new requested target.

The existing:

`t_pending`

is sufficient to identify the unresolved second-leg destination.

---

## 27. No Pending Route Requires Requested Target

When no pending target exists, an execution attempt requires an explicit requested target.

The execution layer does not invent a target.

Therefore:

`no pending + no request`

is invalid input to ordinary ternary execution.

---

## 28. Routing Function

The canonical target-routing operator may be represented as:

`R_route(t_exec, t_target) → (transition, t_pending)`

For non-opposite requests, the committed target is the requested target and no pending destination is introduced.

For opposite requests, the committed target is active neutral `0` and the requested opposite polarity becomes pending.

---

## 29. Pending Routing Function

The pending-route operator may be represented as:

`R_pending(0, t_pending) → (0 → t_pending)`

where:

`t_pending ∈ {-1, 1}`

A pending target cannot execute from retained state `-1` or `1`.

---

## 30. Execution Guard

Neutral routing is controlled by:

`TernaryExecutionGuard`

The guard exposes two independent Boolean permissions:

- `allow_neutral_entry`;
- `allow_neutral_exit`.

These permissions control active-neutral boundary crossings.

---

## 31. Neutral Entry Guard

A transition entering active neutral requires:

`allow_neutral_entry = true`

The guarded transitions are:

`-1 → 0`

and:

`1 → 0`

If neutral entry is not allowed, the execution attempt commits no route and the retained state remains unchanged.

---

## 32. Neutral Exit Guard

A transition leaving active neutral requires:

`allow_neutral_exit = true`

The guarded transitions are:

`0 → -1`

and:

`0 → 1`

If a pending target exists and neutral exit is not allowed, the route remains pending and active neutral is retained.

---

## 33. Guard Independence

Neutral entry and neutral exit are independent eligibility dimensions.

The executable guard configurations include:

- both permitted;
- neither permitted;
- neutral entry only;
- neutral exit only.

These guard configurations are execution-control state.

They are not ternary states.

---

## 34. Guard Boundary

The current executable guard controls neutral entry and neutral exit.

It does not define a general prohibition on every committed self-transition.

A requested retention transition may remain a committed self-transition when it does not cross the active-neutral boundary.

Therefore guard semantics must not be generalized beyond the declared entry/exit permissions.

---

## 35. Active Neutral as Mediation

For opposite-polarity routing, active neutral is a real executed intermediate state.

The route is not represented as an atomic symbolic shortcut:

`-1 → 1`

or:

`1 → -1`

with an invisible intermediate value.

The actual committed history contains the active-neutral execution event.

---

## 36. Active Neutral as Retention State

Active neutral may remain retained while a pending route waits for authorization.

This retained interval may span more than one execution opportunity.

Therefore active neutral is not restricted to an instantaneous mathematical crossing.

---

## 37. Active Neutral as Routing State

While a pending target exists:

- the executed state is active neutral;
- the unresolved destination is stored separately;
- route completion requires a later execution event.

This separation preserves:

`executed state ≠ pending destination`

---

## 38. Active Neutral and Damping

The ternary architecture permits active neutral to carry damping semantics in a concrete model.

Routing through `0` does not by itself numerically define a damping coefficient.

Any quantitative damping relation belongs to the continuous or model-specific layer.

---

## 39. Active Neutral and Balancing

The ternary architecture permits active neutral to represent balancing semantics.

Balancing is not equivalent to missing signal, arithmetic cancellation, zero energy, or zero force.

A balancing interpretation requires the declared model semantics.

---

## 40. Active Neutral and Controlled Neutralization

A direct transition:

`-1 → 0`

or:

`1 → 0`

may terminate in active neutral without a pending opposite target.

Such execution represents a committed neutral state rather than an incomplete opposite route.

The absence of a pending target distinguishes committed neutralization from staged opposite-polarity routing.

---

## 41. Active Neutral and Transition Staging

For opposite-polarity routing, active neutral provides the explicit staging state.

The first leg commits neutral entry.

The second leg commits neutral exit.

The two legs must not be collapsed into one committed event.

---

## 42. Route Atomicity

Each committed route leg is atomic at the ternary execution layer.

An opposite-polarity route contains two atomic committed events.

Therefore:

`one opposite request ≠ one opposite committed transition`

Instead:

`one opposite request → two admissible committed legs`

subject to execution eligibility.

---

## 43. Continuous Dynamics Boundary

Continuous dynamics may generate or influence a requested ternary target through an explicitly defined mapping.

Continuous dynamics do not directly bypass ternary routing.

The chain remains:

`continuous state`

`→ requested ternary target`

`→ routing`

`→ guarded committed execution`

`→ retained ternary state`

---

## 44. Resonance Boundary

Resonance remains a continuous dynamical layer.

Resonance may condition target generation when explicitly defined.

Resonance does not itself constitute a committed ternary transition.

Therefore:

`resonance state ≠ ternary state`

`resonance classification ≠ executed ternary state`

`phase order ≠ complete coherence`

`coherence ≠ resonance`

---

## 45. Physical Observable Boundary

Energy, force, stress, temperature, and other physical observables are not ternary execution states.

Therefore:

`ternary state ≠ energy`

`ternary state ≠ force`

`classifier temperature ≠ thermodynamic temperature`

`oscillator phase ≠ physical phase of matter`

A physical observable may affect target generation only through an explicitly defined model mapping.

---

## 46. Multi-Node Execution State

For multiple execution nodes, the retained routing state is represented as a vector of:

`TernaryExecutionState`

objects.

Each node independently contains:

- retained state;
- optional pending target.

The vector must contain at least one node.

---

## 47. Requested Target Vector

A requested target vector contains one ternary target per execution node.

When supplied, its node count must match the execution-state vector node count.

Nodes with pending targets retain pending-route priority.

Nodes without pending targets require requested targets.

---

## 48. Guard Vector

A multi-node execution step may receive one guard per node.

The guard-vector cardinality must match the execution-state vector cardinality.

Each node is evaluated under its corresponding guard.

---

## 49. Mixed Pending and Non-Pending Nodes

A multi-node execution vector may contain:

- nodes with pending targets;
- nodes without pending targets.

If no new target vector is supplied, every node must already contain a pending target.

If a target vector is supplied:

- pending nodes use it only as a consistency check against their existing pending target;
- non-pending nodes use their corresponding requested target for routing.

---

## 50. Vector Execution Result

A multi-node execution attempt produces:

- previous execution vector;
- one node execution result per node;
- current execution vector.

Node count must remain unchanged across the execution step.

---

## 51. Committed Count

The vector execution result exposes the number of nodes that committed a route leg.

A node contributes to the committed count when:

`route ≠ None`

A held node does not contribute to the committed count.

---

## 52. Held Count

The held count is:

`node_count - committed_count`

A held node retained its execution state without committing a transition leg.

Held count is execution metadata.

It is not a ternary-state value.

---

## 53. Deterministic Routing

For identical:

- retained execution state;
- pending target state;
- requested target;
- execution guard;

the routing and execution result must be identical within the declared deterministic execution domain.

No hidden routing state may affect the result.

---

## 54. Deterministic Vector Execution

For identical:

- previous execution vector;
- requested target vector;
- guard vector;

the vector execution result must be identical.

Node ordering is part of the execution-vector representation.

---

## 55. Trace Requirement

A trace of ternary execution must preserve enough information to distinguish:

- previous retained state;
- committed route or hold;
- current retained state;
- pending target;
- committed-event identity.

A trace must not reconstruct a direct opposite transition where the executable history contains active-neutral mediation.

---

## 56. Serialization Requirement

Serialized ternary execution state must preserve:

- `retained_state`;
- `pending_target`.

A non-null pending target is valid only with retained active neutral.

Missing or absent data must not be serialized as ternary `0`.

---

## 57. Direct Neutral Request

A requested target:

`t_target = 0`

is a valid ternary target.

From retained polarity:

`-1 → 0`

or:

`1 → 0`

may commit directly when neutral entry is allowed.

Such a route contains no pending final target unless it originated from an opposite-polarity routing request.

---

## 58. Neutral Self-Retention

From:

`t_exec = 0`

a requested target:

`t_target = 0`

may form the committed retention transition:

`0 → 0`

when no pending route has priority.

This is distinct from holding an unresolved pending route in active neutral.

---

## 59. Polarized Self-Retention

The committed self-transitions:

`-1 → -1`

and:

`1 → 1`

are valid canonical retention transitions.

They do not create pending targets.

---

## 60. Pending-Target Immutability

Once an opposite-polarity target has become pending, the current executable reference preserves that destination until:

- the second leg completes; or
- a future explicitly defined higher-level operation changes the route contract.

The current executable `execute_ternary_step` does not implement generic pending-target replacement.

---

## 61. Cancellation Boundary

The current executable reference does not define a generic pending-route cancellation operator.

Therefore cancellation must not be inferred from:

- a new requested target;
- a guard hold;
- absence of a new request.

A guard hold retains the pending route.

---

## 62. Conflict Boundary

A conflicting new requested target does not silently arbitrate against an existing pending target.

The current executable reference rejects replacement of the pending destination.

Higher-level arbitration, if introduced, requires a separate explicit contract.

---

## 63. Scheduler Boundary

The neutral-routing specification does not import FRP scheduler architecture.

TR-EIF routing semantics require only the declared ternary execution and guard contracts.

Therefore no FRP-specific:

- scheduler mode;
- coefficient;
- RTL module;
- timing architecture

is implied by this specification.

---

## 64. FRP Semantic Correspondence Boundary

FRP may be used as a read-only executable reference for explicitly confirmed semantic correspondences.

The shared semantic correspondences relevant here include:

- canonical `-1/0/1`;
- active neutral `0`;
- prohibition of direct committed opposite-polarity transitions;
- explicit mediation through `0`;
- separation of target and executed state.

This does not make FRP and TR-EIF identical architectures.

Therefore:

`FRP ≠ TR-EIF`

`FRP ≠ TR-EIP`

---

## 65. Multiscale Boundary

A scale transition does not modify the neutral-routing contract.

Where balanced ternary execution exists at a scale, direct opposite-polarity committed transitions remain forbidden.

No generic coarse-graining operator may replace:

`-1 → 0 → 1`

with:

`-1 → 1`

or replace:

`1 → 0 → -1`

with:

`1 → -1`

---

## 66. Validation Status Boundary

Validation outcomes are not ternary routing states.

Therefore:

`PASS ≠ 1`

`FAIL ≠ -1`

`unknown validation ≠ 0`

Validation state must remain explicitly typed outside the balanced-ternary execution domain.

---

## 67. Core Routing Invariants

The neutral-routing layer preserves the following invariants:

1. The canonical state space is `-1/0/1`.
2. State `0` is active neutral.
3. Direct committed `-1 → 1` is forbidden.
4. Direct committed `1 → -1` is forbidden.
5. Opposite-polarity routes require active-neutral mediation.
6. Each route leg is a separate committed execution event.
7. A pending target is distinct from the executed state.
8. A pending target is never `0`.
9. A pending target requires retained active neutral.
10. A pending target cannot be silently replaced.
11. A held attempt is distinct from a committed self-transition.
12. Active neutral may persist across multiple execution opportunities.
13. Missing or invalid data are not encoded as active neutral.
14. Continuous dynamics do not bypass routing.
15. Resonance state is not ternary state.
16. Physical observables are not ternary states.
17. Multi-node cardinality is preserved across execution.
18. Routing is deterministic for identical declared inputs.

---

## 68. Executable Reference Correspondence

The current executable neutral-routing implementation is distributed across:

`src/tr_eif/ternary/routing.py`

`src/tr_eif/ternary/execution.py`

`src/tr_eif/ternary/guard.py`

`src/tr_eif/ternary/vector_execution.py`

The principal executable types and operators are:

`TernaryRoute`

`route_ternary_target`

`route_pending_target`

`TernaryExecutionState`

`TernaryExecutionStep`

`execute_ternary_step`

`TernaryExecutionGuard`

`TernaryExecutionVector`

`TernaryVectorExecutionStep`

`execute_ternary_vector_step`

These executable interfaces implement the routing semantics declared in this specification.

---

## 69. Non-Claims

The neutral-routing layer does not by itself define:

- physical energy flow magnitude;
- force magnitude;
- thermodynamic temperature;
- chemical bond formation;
- physical phase transition;
- resonance frequency;
- synchronization state;
- material transmutation mechanism;
- scheduler timing;
- hardware implementation.

Those quantities and mechanisms belong to their respective model layers.

---

## 70. Summary

TR-EIF neutral routing is an active execution mechanism.

State `0` is not a null placeholder.

It is the explicit active-neutral state through which opposite-polarity execution is mediated.

The canonical execution routes are:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

with each leg committed separately.

The architecture preserves:

`target ≠ executed state`

`pending ≠ executed state`

`pending ≠ active neutral`

and:

`hold ≠ committed transition`

This separation permits continuous nonlinear dynamics, resonance dynamics, balanced-ternary execution, and physical observables to remain distinct while interacting through explicit typed mappings.
