# Transition Semantics

## 1. Scope

This document defines the repository-level committed transition semantics for the balanced ternary state space of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- the committed transition relation;
- allowed retained-state transitions;
- forbidden direct opposite-polarity transitions;
- retention transitions;
- active-neutral entry;
- active-neutral exit;
- opposite-polarity route decomposition;
- target and execution separation;
- pending-route interaction;
- execution guards;
- hold semantics;
- committed-event semantics;
- deterministic transition requirements;
- continuous/discrete separation;
- trace requirements;
- validation requirements;
- executable reference correspondence.

The canonical balanced ternary state space is defined separately by:

`docs/specifications/ternary_state_specification.md`

Neutral-routing semantics are defined in:

`docs/volume_02_ternary_resonance_theory/chapter_07_neutral_routing.md`

---

## 2. Canonical Ternary Domain

The balanced ternary state space is:

`T = {-1, 0, 1}`

The canonical compact notation is:

`-1/0/1`

The state:

`0`

is active neutral.

The states:

`-1`

and:

`1`

are opposite ternary polarities.

---

## 3. Executed State Domain

The executed retained state belongs to:

`T_exec = {-1, 0, 1}`

An executed retained state is denoted:

`t_exec ∈ T_exec`

A committed transition changes or retains this state according to the transition relation defined in this specification.

---

## 4. Target State Domain

A requested target belongs to:

`T_target = {-1, 0, 1}`

A target is denoted:

`t_target ∈ T_target`

The value sets of:

`T_exec`

and:

`T_target`

are identical.

Their semantic roles are distinct.

Therefore:

`target ≠ executed retained state`

remains a framework invariant.

---

## 5. Committed Transition Relation

The committed transition relation is:

`R_T ⊆ T_exec × T_exec`

The canonical relation contains exactly the following ordered pairs:

`(-1, -1)`

`(-1, 0)`

`(0, -1)`

`(0, 0)`

`(0, 1)`

`(1, 0)`

`(1, 1)`

The ordered pairs:

`(-1, 1)`

and:

`(1, -1)`

are excluded.

---

## 6. Allowed Transition Set

The complete canonical set of allowed committed transitions is:

`R_T = {(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 0), (1, 1)}`

Every committed ternary transition must belong to:

`R_T`

No other ordered pair is a canonical committed transition.

---

## 7. Forbidden Direct Opposite Transitions

The direct committed transitions:

`-1 → 1`

and:

`1 → -1`

are forbidden.

Equivalently:

`(-1, 1) ∉ R_T`

and:

`(1, -1) ∉ R_T`

This prohibition is categorical.

It is not tolerance-based.

It is not conditional on a continuous value.

It is not conditional on the magnitude of a resonance descriptor.

It is not conditional on numerical step size.

---

## 8. Opposite-Polarity Definition

Two executed ternary states are opposite polarities when one is:

`-1`

and the other is:

`1`

The ordered opposite pairs are therefore:

`(-1, 1)`

and:

`(1, -1)`

No other pair is classified as a direct opposite-polarity pair.

---

## 9. Retention Transitions

The committed retention transitions are:

`-1 → -1`

`0 → 0`

`1 → 1`

A retention transition has identical source and target state.

For a committed transition:

`source = target`

the retained ternary state remains unchanged.

---

## 10. State-Changing Transitions

The canonical state-changing committed transitions are:

`-1 → 0`

`0 → -1`

`0 → 1`

`1 → 0`

These are the only canonical committed transition edges that change state.

---

## 11. Active-Neutral Entry

A committed transition enters active neutral when:

`source ∈ {-1, 1}`

and:

`target = 0`

The canonical neutral-entry transitions are:

`-1 → 0`

and:

`1 → 0`

---

## 12. Active-Neutral Exit

A committed transition leaves active neutral when:

`source = 0`

and:

`target ∈ {-1, 1}`

The canonical neutral-exit transitions are:

`0 → -1`

and:

`0 → 1`

---

## 13. Opposite-Polarity Mediation

A committed transition between opposite polarities requires active-neutral mediation.

The route from:

`-1`

to:

`1`

is:

`-1 → 0 → 1`

The route from:

`1`

to:

`-1`

is:

`1 → 0 → -1`

The state:

`0`

is therefore an execution state in the route.

It is not an annotation placed between two otherwise direct commits.

---

## 14. First Leg

For the route:

`-1 → 0 → 1`

the first committed state-changing leg is:

`-1 → 0`

For the route:

`1 → 0 → -1`

the first committed state-changing leg is:

`1 → 0`

The first leg terminates in active neutral.

---

## 15. Second Leg

For the route:

`-1 → 0 → 1`

the second committed state-changing leg is:

`0 → 1`

For the route:

`1 → 0 → -1`

the second committed state-changing leg is:

`0 → -1`

The second leg starts from an already retained neutral state.

---

## 16. Independent-Leg Requirement

The two legs of an opposite-polarity route are separate committed transition events.

Completion of:

`-1 → 0`

does not imply completion of:

`0 → 1`

Completion of:

`1 → 0`

does not imply completion of:

`0 → -1`

The state after first-leg completion is:

`0`

until another committed transition changes it.

---

## 17. Minimum State-Changing Route Length

An opposite-polarity route requires at least two state-changing committed edges.

The minimum route length from:

`-1`

to:

`1`

is two.

The minimum route length from:

`1`

to:

`-1`

is two.

Neutral retention may increase the number of committed events without reducing the minimum number of state-changing legs.

---

## 18. Neutral Residence

After the first leg of an opposite route, active neutral may persist.

A route may therefore contain:

`-1 → 0 → 0 → ... → 0 → 1`

or:

`1 → 0 → 0 → ... → 0 → -1`

Each committed:

`0 → 0`

is a neutral retention transition.

---

## 19. Target versus Transition

A requested target is not a committed transition.

A target may change directly from:

`-1`

to:

`1`

at the target-generation layer.

This does not permit the retained execution state to commit:

`-1 → 1`

The execution layer must apply the committed transition relation independently of the target-generation path.

---

## 20. Opposite Requested Target

A valid execution configuration may contain:

`t_exec = -1`

and:

`t_target = 1`

Likewise, a valid configuration may contain:

`t_exec = 1`

and:

`t_target = -1`

These configurations represent an opposite-polarity request.

They do not represent a committed direct opposite transition.

---

## 21. Opposite Target Routing

For:

`t_exec = -1`

and:

`t_target = 1`

the first admissible state-changing execution result is:

`t_exec,next = 0`

For:

`t_exec = 1`

and:

`t_target = -1`

the first admissible state-changing execution result is:

`t_exec,next = 0`

The requested opposite destination may remain represented separately as pending execution state.

---

## 22. Pending Destination

A staged opposite route may retain a pending destination.

A canonical pending destination domain is:

`X_pending = {NONE, -1, 1}`

The value:

`NONE`

represents absence of a pending opposite destination.

It is not a ternary state.

Therefore:

`NONE ∉ T`

and:

`NONE ≠ 0`

---

## 23. Pending Destination after First Leg

A first-leg route may produce:

`(-1, NONE) → (0, 1)`

where the tuple represents:

`(t_exec, t_pending)`

The reverse route may produce:

`(1, NONE) → (0, -1)`

The pending destination records the remaining destination.

The executed state remains:

`0`

---

## 24. Pending Destination and Neutral State

A pending destination and active neutral are distinct state variables.

For:

`t_exec = 0`

`t_pending = 1`

the executed state is not:

`1`

For:

`t_exec = 0`

`t_pending = -1`

the executed state is not:

`-1`

---

## 25. Pending Route Completion

A canonical pending route may complete through:

`(0, 1) → (1, NONE)`

or:

`(0, -1) → (-1, NONE)`

The second-leg commit clears the pending destination under this route representation.

---

## 26. Pending Target Replacement Boundary

The executable reference transition layer does not replace an existing pending target with a different newly requested target during the same pending route.

If a different requested target is supplied while a distinct pending target exists, the reference execution contract rejects the replacement.

Alternative route-replacement policies require a separately defined specialization contract.

---

## 27. Same-State Request

If:

`t_target = t_exec`

the requested target does not require a state-changing transition.

The canonical transition relation contains the corresponding retention transition.

Examples are:

`-1 → -1`

`0 → 0`

`1 → 1`

---

## 28. Neutral Target from Polarized State

For:

`t_exec = -1`

and:

`t_target = 0`

the transition:

`-1 → 0`

is allowed.

For:

`t_exec = 1`

and:

`t_target = 0`

the transition:

`1 → 0`

is allowed.

No pending opposite destination is required solely because the requested target is neutral.

---

## 29. Polarized Target from Neutral State

For:

`t_exec = 0`

and:

`t_target = -1`

the transition:

`0 → -1`

is allowed when execution conditions permit neutral exit.

For:

`t_exec = 0`

and:

`t_target = 1`

the transition:

`0 → 1`

is allowed when execution conditions permit neutral exit.

---

## 30. Transition Guard

A transition guard controls execution eligibility.

The reference execution guard separates:

- neutral-entry permission;
- neutral-exit permission.

The corresponding logical controls are:

`allow_neutral_entry`

and:

`allow_neutral_exit`

A guard changes whether an otherwise valid transition leg may commit.

It does not change the membership of:

`R_T`

---

## 31. Unrestricted Guard

An unrestricted guard permits:

- neutral entry;
- neutral exit.

It does not permit forbidden direct opposite transitions.

The transition relation remains unchanged.

---

## 32. Hold Guard

A hold guard permits neither:

- neutral entry;
- neutral exit.

A blocked transition attempt does not automatically become a committed retention transition.

In the reference executable implementation, a blocked execution attempt is represented separately from a committed transition route.

---

## 33. Neutral-Entry-Only Guard

A neutral-entry-only guard permits:

`-1 → 0`

and:

`1 → 0`

when otherwise applicable.

It blocks neutral exit.

Therefore a first leg may commit while the second leg remains pending.

---

## 34. Neutral-Exit-Only Guard

A neutral-exit-only guard permits:

`0 → -1`

and:

`0 → 1`

when otherwise applicable.

It blocks new polarized-to-neutral entry.

---

## 35. Guard and Transition Relation

Execution eligibility and transition validity are separate predicates.

A transition may belong to:

`R_T`

while being blocked by the current guard.

A transition outside:

`R_T`

cannot become valid through guard authorization.

Therefore:

`guard authorization ≠ transition validity`

---

## 36. Hold versus Retention

A hold condition and a committed self-transition are distinct.

A committed retention transition belongs to:

`R_T`

and records an execution transition with:

`source = target`

A hold condition represents absence of a committed route under the reference execution boundary.

Therefore:

`hold ≠ committed retention transition`

---

## 37. Committed Transition Event

A committed transition event contains a validated source and validated target that belong to:

`R_T`

The event may be:

- state-changing;
- retention.

A committed event cannot contain a direct opposite ordered pair.

---

## 38. State-Change Predicate

For a committed transition:

`source → target`

the transition changes state exactly when:

`source ≠ target`

The canonical state-changing edges are therefore:

`-1 → 0`

`0 → -1`

`0 → 1`

`1 → 0`

---

## 39. Neutral-Entry Predicate

A committed transition enters neutral exactly when:

`source ≠ 0`

and:

`target = 0`

This predicate identifies:

`-1 → 0`

and:

`1 → 0`

---

## 40. Neutral-Exit Predicate

A committed transition leaves neutral exactly when:

`source = 0`

and:

`target ≠ 0`

This predicate identifies:

`0 → -1`

and:

`0 → 1`

---

## 41. Direct-Opposite Predicate

A source-target pair is a direct opposite transition exactly when:

`source = -1 and target = 1`

or:

`source = 1 and target = -1`

The predicate is evaluated categorically over ternary-state identity.

---

## 42. No Numerical Tolerance

The transition relation uses exact categorical state identity.

No tolerance such as:

`atol`

`rtol`

or:

`epsilon`

is part of direct-opposite transition validation.

Numerical proximity between unrelated continuous values does not modify the transition relation.

---

## 43. Continuous-State Separation

Continuous evolution does not directly alter the committed transition relation.

Continuous state may affect:

- descriptors;
- targets;
- guards;
- scheduler inputs;
- control variables.

The committed ternary transition still must belong to:

`R_T`

---

## 44. Continuous Bypass Exclusion

A continuous variable may cross directly between any numerical values allowed by its own state space.

Such a crossing does not permit:

`-1 → 1`

or:

`1 → -1`

at the committed ternary execution boundary.

---

## 45. Resonance Bypass Exclusion

A resonance descriptor may move between regions that generate different ternary targets.

A resonance classifier may change classification without passing through a ternary-neutral target.

Neither case permits a direct opposite committed retained-state transition.

The committed execution relation remains:

`R_T`

---

## 46. Threshold Crossing Separation

A continuous-to-ternary threshold crossing may change:

`t_target`

It does not itself change:

`t_exec`

Therefore:

`threshold crossing ≠ committed ternary transition`

---

## 47. Bifurcation Separation

A bifurcation is a property of a declared dynamical system under its corresponding mathematical conditions.

A ternary committed transition is an execution event in:

`R_T`

Therefore:

`bifurcation ≠ ternary transition`

---

## 48. Structural Transition Separation

A structural transition is not a ternary-state transition by definition.

Therefore:

`ternary transition ≠ structural transition`

Any coupling between them requires an explicit mapping.

---

## 49. Physical Phase Transition Separation

A physical phase transition is not a ternary-state transition by definition.

Therefore:

`structural transition ≠ physical phase transition`

and:

`ternary transition ≠ physical phase transition`

unless a separate physical model defines a relation between their observables.

---

## 50. Spatial Transformation Separation

Spatial transformation does not modify the committed transition relation.

The relations remain:

`spatial rotation ≠ ternary polarity reversal`

`spatial reflection ≠ ternary polarity reversal`

`atomic permutation ≠ ternary transition`

---

## 51. Formal Charge Separation

Formal ionic charge does not define ternary transition direction.

A change in formal charge, if modeled elsewhere, does not itself constitute a ternary-state transition.

Formal-charge values and ternary-state values remain separately typed.

---

## 52. Scale Separation

A transition between multiscale levels is not a ternary transition.

A scale mapping may contain indices numerically equal to:

`0`

or:

`1`

without acquiring ternary-state semantics.

Therefore:

`scale transition ≠ ternary transition`

---

## 53. Learning-State Separation

An optimization-stage transition or classifier-training transition is not a ternary execution event.

Therefore:

`training-stage transition ≠ ternary-state transition`

A learned model that generates ternary targets remains upstream of the committed ternary transition boundary.

---

## 54. Request and Commit Separation

A request proposes a target or operation.

A commit changes or retains the execution state through a validated transition event.

Therefore:

`request ≠ commit`

An opposite request may exist while the direct opposite commit remains forbidden.

---

## 55. Authorization and Commit Separation

Execution authorization permits a transition attempt to proceed.

Authorization alone does not constitute a committed transition.

Therefore:

`authorization ≠ commit`

The committed source-target pair must still belong to:

`R_T`

---

## 56. Scheduler and Transition Separation

A scheduler determines execution opportunities according to its declared control contract.

Scheduler state is not ternary state.

A scheduler decision cannot redefine:

`R_T`

A scheduler may block an allowed transition.

It may not convert a forbidden direct opposite transition into an allowed committed edge.

---

## 57. Capacity and Transition Separation

A capacity constraint may prevent an allowed transition from committing.

Capacity does not modify the canonical committed transition set.

Therefore:

`capacity eligibility ≠ transition validity`

---

## 58. Deterministic Transition Function

For a deterministic transition operator, identical complete execution state and identical requested input must produce identical execution results under identical guards and parameters.

Any result-affecting pending state belongs to the deterministic execution state closure.

Any result-affecting guard state belongs to the deterministic execution input or state closure.

---

## 59. History Dependence

A transition controller may depend on history.

When history affects execution, the required history state must be represented explicitly or through an equivalent complete retained state.

History dependence does not change the prohibition on direct opposite committed transitions.

---

## 60. Trace Semantics

A transition trace may record:

- previous retained state;
- requested target;
- pending target;
- transition route;
- resulting retained state;
- execution guard;
- execution coordinate.

A trace records execution information.

It does not redefine transition validity.

---

## 61. Direct-Transition Trace Invariant

A canonical execution trace must contain no committed event with:

`previous = -1 and current = 1`

and no committed event with:

`previous = 1 and current = -1`

unless the record explicitly represents multiple committed legs rather than one transition event.

Each committed leg must remain individually represented.

---

## 62. Intermediate Neutral Visibility

For an opposite-polarity route, the intermediate executed neutral state must remain semantically observable in the execution sequence.

A representation must not collapse:

`-1 → 0 → 1`

into one committed event:

`-1 → 1`

Likewise, it must not collapse:

`1 → 0 → -1`

into:

`1 → -1`

---

## 63. Serialization Requirement

Serialized transition data must preserve enough information to distinguish:

- source state;
- target state;
- retained result;
- pending destination where present;
- absence of a committed route where represented.

Serialization must not create a direct opposite event by collapsing multiple committed legs.

---

## 64. Replay Requirement

Deterministic replay of a serialized transition sequence must reproduce the same ordered committed transition legs under the declared replay contract.

The replay representation must preserve active-neutral mediation.

---

## 65. Validation Requirement

Transition validation must test at minimum:

- every canonical allowed pair;
- both forbidden direct opposite pairs;
- retention transitions;
- neutral-entry transitions;
- neutral-exit transitions;
- opposite-target routing;
- pending-route completion;
- guard-blocked neutral entry;
- guard-blocked neutral exit;
- hold versus committed retention separation.

---

## 66. Exhaustive Pair Validation

Since:

`|T| = 3`

there are:

`3 × 3 = 9`

possible ordered source-target pairs.

Seven belong to:

`R_T`

Two do not.

The excluded pairs are exactly:

`(-1, 1)`

and:

`(1, -1)`

---

## 67. Reference Implementation

The executable state representation is located in:

`src/tr_eif/ternary/state.py`

The executable transition relation is located in:

`src/tr_eif/ternary/transition.py`

The executable routing layer is located in:

`src/tr_eif/ternary/routing.py`

The executable guard layer is located in:

`src/tr_eif/ternary/guard.py`

The retained execution-state layer is located in:

`src/tr_eif/ternary/execution.py`

---

## 68. Mathematical References

The notation contract is defined in:

`docs/volume_01_mathematical_foundations/chapter_02_notation_and_definitions.md`

The active-neutral dynamics are defined in:

`docs/volume_02_ternary_resonance_theory/chapter_06_active_neutral_state_dynamics.md`

Neutral routing is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_07_neutral_routing.md`

Coupled continuous-discrete dynamics are defined in:

`docs/volume_02_ternary_resonance_theory/chapter_08_coupled_continuous_discrete_dynamics.md`

The repository-level architecture is defined in:

`docs/architecture/framework_architecture.md`

The canonical state specification is defined in:

`docs/specifications/ternary_state_specification.md`

---

## 69. Transition Invariants

The transition contract preserves:

`T = {-1, 0, 1}`

`R_T = {(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 0), (1, 1)}`

`(-1, 1) ∉ R_T`

`(1, -1) ∉ R_T`

`-1 → 0 → 1`

`1 → 0 → -1`

`target ≠ executed retained state`

`pending target ≠ active neutral state`

`hold ≠ committed retention transition`

`request ≠ commit`

`authorization ≠ commit`

`guard authorization ≠ transition validity`

`threshold crossing ≠ committed ternary transition`

`bifurcation ≠ ternary transition`

`scale transition ≠ ternary transition`

---

## 70. Specification Closure

The canonical committed transition graph contains three vertices:

`{-1, 0, 1}`

and seven allowed directed committed edges:

`-1 → -1`

`-1 → 0`

`0 → -1`

`0 → 0`

`0 → 1`

`1 → 0`

`1 → 1`

The direct opposite edges:

`-1 → 1`

and:

`1 → -1`

are excluded.

Opposite-polarity execution is represented only through separate active-neutral-mediated committed legs.
