# Neutral Routing

## 1. Purpose

This chapter defines the neutral-routing architecture of Ternary Resonance Theory.

Neutral routing governs staged execution when a requested ternary target is opposite to the currently executed polarity.

The canonical balanced ternary execution domain remains:

`T = {-1, 0, 1}`.

The active-neutral state:

`0`

is the mandatory routing state between opposite polarities.

The canonical opposite-polarity routes are:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

This chapter formalizes:

- route creation;
- first-leg execution;
- pending destination registration;
- neutral residence;
- route retention;
- second-leg authorization;
- route completion;
- route cancellation;
- route replacement;
- route conflict;
- arbitration;
- scheduler interaction;
- capacity interaction;
- route ordering;
- deterministic replay;
- route validation;
- executable specialization boundaries.

---

## 2. Routing State

Let the complete ternary routing state be:

`X_route`.

A minimal staged routing state may contain:

`x_route = (t_exec, t_target, t_pending)`.

A richer implementation may additionally contain:

- route phase;
- scheduler state;
- residence counters;
- authorization state;
- capacity state;
- request queues;
- route identifiers;
- execution metadata.

Only result-affecting components belong to the deterministic state closure.

---

## 3. Executed State

The executed state is:

`t_exec ∈ {-1, 0, 1}`.

It represents the retained committed ternary state.

---

## 4. Target State

The target state is:

`t_target ∈ {-1, 0, 1}`.

It represents the current requested ternary state.

The invariant remains:

`target ≠ executed state`.

---

## 5. Pending State

The pending destination state is:

`t_pending ∈ {NONE, -1, 1}`

under the canonical opposite-route representation.

`NONE`

means no pending opposite destination is active.

It is not ternary neutral.

---

## 6. Route Creation

A neutral route is created when:

- the executed state is polarized;
- the target is the opposite polarity;
- execution authorizes the first leg.

For:

`t_exec = -1`

and:

`t_target = 1`

the route begins with:

`-1 → 0`.

For:

`t_exec = 1`

and:

`t_target = -1`

the route begins with:

`1 → 0`.

---

## 7. First-Leg Atomicity

The first leg is one committed execution event.

It changes the executed state to:

`0`.

A canonical implementation may simultaneously register the pending destination.

For example:

`(-1, NONE) → (0, 1)`.

The reverse route is:

`(1, NONE) → (0, -1)`.

---

## 8. First-Leg Completion

After first-leg completion:

`t_exec = 0`.

The route remains incomplete.

The pending destination stores the intended opposite polarity.

---

## 9. Pending Destination Registration

A canonical pending registration rule is:

if:

`t_exec_prev = -1`

and:

`t_target = 1`

and first leg commits,

then:

`t_pending = 1`.

If:

`t_exec_prev = 1`

and:

`t_target = -1`

then:

`t_pending = -1`.

---

## 10. Pending Destination Is Not Executed State

The state:

`t_pending = 1`

does not imply:

`t_exec = 1`.

During the route:

`t_exec = 0`.

Likewise:

`t_pending = -1`

does not imply:

`t_exec = -1`.

---

## 11. Pending Destination Is Not Target

The current target and pending destination may be equal.

They are still distinct state variables.

A specialization may permit them to diverge after route creation.

---

## 12. Route Identity

A route may be represented by:

`r_route = (origin, destination)`.

For canonical opposite routes:

`(-1, 1)`

or:

`(1, -1)`.

If route origin matters after entry into neutral, it must be stored explicitly or reconstructed from retained trace state.

---

## 13. Route Phase

A route-control state may use phases such as:

`IDLE`

`FIRST_LEG_READY`

`NEUTRAL_PENDING`

`SECOND_LEG_READY`

`COMPLETE`

`CANCELLED`.

These values belong to route-control space.

They are not ternary states.

---

## 14. Idle Route State

A canonical idle state may satisfy:

`t_pending = NONE`.

The executed state may be:

`-1`

`0`

or:

`1`.

Neutral without pending route is therefore possible when allowed by the specialization.

---

## 15. Neutral-Pending Route State

A canonical active opposite route satisfies:

`t_exec = 0`

and:

`t_pending ∈ {-1, 1}`.

This is the core neutral-routing state.

---

## 16. Route Retention

A pending route may remain active across multiple execution opportunities.

A retention transition may preserve:

`t_exec = 0`

`t_pending = destination`.

---

## 17. Neutral Residence

The route may remain in:

`NEUTRAL_PENDING`

for multiple tacts or numerical steps.

This permits:

`0 → 0`

retention before second-leg completion.

---

## 18. Second-Leg Eligibility

A pending route becomes eligible for second-leg completion when all required conditions are satisfied.

A generic predicate is:

`G_second(X_route, X_sched, X_capacity, X_aux) = true`.

---

## 19. Second-Leg Destination

Under strict pending routing, the second-leg destination equals:

`t_pending`.

Therefore:

`t_pending = 1`

permits:

`0 → 1`.

`t_pending = -1`

permits:

`0 → -1`.

---

## 20. Second-Leg Commit

A second-leg commit performs:

`(0, 1) → (1, NONE)`

or:

`(0, -1) → (-1, NONE)`.

This completes the opposite-polarity route.

---

## 21. Route Completion

Route completion requires:

- successful second-leg commit;
- pending-state clearing or route-state update;
- preservation of the canonical transition invariant.

The resulting executed state equals the completed destination.

---

## 22. Route Completion Event

A route-completion event is distinct from:

- target generation;
- first-leg commit;
- neutral retention;
- second-leg authorization.

It corresponds to completion of the staged execution route.

---

## 23. Direct Opposite Route Exclusion

The following one-step commits remain forbidden:

`-1 → 1`

`1 → -1`.

No routing policy may bypass this invariant while remaining canonical TR-EIF execution.

---

## 24. Route Length

The minimum state-changing route length between opposite polarities is two committed edges.

Neutral retention may increase total execution duration but not reduce this minimum.

---

## 25. Route Persistence

A route may persist while:

`t_exec = 0`

and:

`t_pending`

remains unchanged.

Persistence may span:

- one tact;
- many tacts;
- one scheduler cycle;
- multiple scheduler cycles.

---

## 26. Route Timeout

A specialization may define a timeout:

`tau_route`

or:

`n_route,max`.

The timeout policy must define what happens when the pending route is not completed within the allowed interval.

---

## 27. Timeout Actions

Possible explicit timeout actions include:

- retain neutral;
- cancel route;
- reset target;
- generate a supervisory request;
- block further route creation.

No universal timeout action is imposed.

---

## 28. Route Cancellation

A pending route may be cancelled through an explicit control operation.

Cancellation must define:

- resulting `t_exec`;
- resulting `t_pending`;
- resulting route phase;
- target handling.

---

## 29. Canonical Neutral Cancellation

A cancellation while:

`t_exec = 0`

may clear:

`t_pending → NONE`.

The executed state may remain:

`0`.

---

## 30. Cancellation versus Completion

The distinction is:

`route cancellation ≠ route completion`.

Completion reaches the pending destination.

Cancellation terminates the route without that completion.

---

## 31. Cancellation versus Neutral Retention

Neutral retention keeps the route active.

Cancellation removes or changes the route state.

---

## 32. Route Replacement

A specialization may allow pending destination replacement while neutral.

For example:

`t_pending = 1 → -1`.

This is a route-state update.

It does not change:

`t_exec = 0`.

---

## 33. Replacement Authorization

Pending replacement must be explicitly authorized.

The replacement policy must define:

- source of new destination;
- priority;
- route-phase update;
- counter reset;
- target interaction.

---

## 34. Route Reversal

A route may reverse while neutral if the pending destination is replaced by the opposite pending destination.

The executed state remains:

`0`

during reversal.

---

## 35. Route Reversal Is Not Direct Polarity Reversal

Changing:

`t_pending = 1 → -1`

does not constitute:

`t_exec = 1 → -1`.

The executed state remains neutral.

---

## 36. Target Change during Pending Route

While:

`t_exec = 0`

and:

`t_pending ≠ NONE`

the upstream target may change.

The route policy must define how to handle the new target.

---

## 37. Preserve-Pending Policy

Under preserve-pending policy:

`t_pending`

remains unchanged until completion or explicit cancellation.

New targets may be retained separately.

---

## 38. Replace-Pending Policy

Under replace-pending policy:

`t_pending`

may be replaced by the new authorized destination.

---

## 39. Cancel-on-Target-Neutral Policy

A specialization may cancel the route when:

`t_target = 0`.

This policy must be explicit.

---

## 40. Hold-Neutral Policy

A specialization may retain:

`t_exec = 0`

without completing or cancelling the route until another condition is satisfied.

---

## 41. Target Return to Origin

Suppose a route began:

`-1 → 0`

with pending:

`1`.

If the target later returns to:

`-1`

the route policy must define whether to:

- cancel pending `1`;
- replace pending with `-1`;
- hold neutral;
- complete the original route first.

---

## 42. Target Equal to Pending Destination

When:

`t_target = t_pending`

the route remains aligned with current upstream request.

This alignment does not itself authorize second-leg commit.

---

## 43. Target Opposes Pending Destination

When:

`t_target = -t_pending`

the route is in conflict.

A conflict resolver is required.

---

## 44. Neutral Target during Pending Route

When:

`t_target = 0`

and:

`t_pending ≠ NONE`

the target is neutral while the route remains polarized in pending intent.

This is a valid state only if the route policy defines how it is handled.

---

## 45. Route Conflict State

A route conflict may contain:

`(t_exec = 0, t_pending = 1, t_target = -1)`.

The reverse configuration is also possible.

No implicit resolution is assumed.

---

## 46. Route Conflict Resolver

A deterministic resolver may be:

`F_conflict: X_route × X_ctrl → X_route_action`.

Possible outputs include:

- preserve;
- cancel;
- replace;
- hold;
- reject new target.

---

## 47. Route Action Space

Let:

`K_route_action`

contain route-control actions.

These may include:

`HOLD`

`COMPLETE`

`CANCEL`

`REPLACE`

`REJECT`

`RETAIN`.

This control space is distinct from:

`T_exec`.

---

## 48. Route Arbitration

Multiple candidate actions may require arbitration.

A generic mapping is:

`A_route: X_candidates × X_route × X_ctrl → K_route_action`.

---

## 49. Arbitration Priority

Priority may depend on:

- safety guards;
- scheduler state;
- route age;
- target age;
- capacity;
- model-specific precedence.

The rule must be deterministic when deterministic replay is required.

---

## 50. Request Layer

Neutral routing may receive one or more route requests.

A request describes desired state change.

It does not mutate retained state.

---

## 51. Request Types

Possible request types include:

- enter neutral;
- exit neutral;
- complete pending route;
- cancel route;
- replace pending destination;
- retain current state.

These are execution-control requests.

---

## 52. Request Queue

An implementation may maintain:

`Q_req`.

If queue contents affect future execution, the queue belongs to complete state.

---

## 53. Queue Ordering

A queue must define ordering semantics such as:

- FIFO;
- priority;
- timestamp;
- route class;
- explicit arbitration.

---

## 54. Queue Entry Is Not Pending Route

An upstream queued request and:

`t_pending`

are separate structures.

A request may exist before a pending route is registered.

---

## 55. Pending Registration Boundary

Pending destination becomes execution-route state only when the route-registration operation commits that state.

---

## 56. Request Rejection

A request may be rejected.

Rejection is not equivalent to:

`t_exec = 0`.

---

## 57. Authorization Layer

An authorization stage evaluates whether a structurally valid route action may proceed.

A generic predicate is:

`G_auth(request, X_route, X_ctrl) ∈ {ALLOW, BLOCK}`.

---

## 58. Structurally Valid Route Action

A route action is structurally valid if it respects the canonical transition graph.

Examples include:

`-1 → 0`

`0 → 1`

`0 → -1`

`1 → 0`.

---

## 59. Structurally Invalid Route Action

The direct opposite edges remain invalid:

`-1 → 1`

`1 → -1`.

They are not merely blocked.

They are absent from the canonical transition relation.

---

## 60. Authorization versus Structural Validity

A structurally valid action may still be blocked by authorization.

A structurally invalid action cannot become canonical valid merely because an authorization flag is true.

---

## 61. Commit Boundary

Commit is the only stage that mutates:

`t_exec`.

This preserves:

`request ≠ authorization ≠ commit`.

---

## 62. First-Leg Commit Boundary

The first leg commits:

`polarized → 0`.

It may also register:

`t_pending`.

---

## 63. Second-Leg Commit Boundary

The second leg commits:

`0 → pending destination`.

It then clears or updates pending state.

---

## 64. Neutral-Retention Commit

A specialization may treat:

`0 → 0`

as an explicit committed retention event.

Another may treat lack of state change as retained state without a separate event.

The trace contract must distinguish these semantics.

---

## 65. Scheduler Interface

Neutral routing may depend on scheduler state:

`X_sched`.

The scheduler determines execution opportunities and ordering.

---

## 66. Scheduler Opportunity

A scheduler opportunity permits route evaluation.

It does not guarantee a commit.

---

## 67. Scheduler Phase

A scheduler may expose phases such as:

- balance;
- excite;
- neutralize;
- commit.

These are scheduler-control semantics.

They are not ternary states.

---

## 68. Scheduler-Ternary Separation

The scheduler phase:

`neutralize`

does not equal:

`t_exec = 0`

by semantic identity.

A scheduler operation may affect neutral execution, but the spaces remain distinct.

---

## 69. Scheduler Route Gate

A route gate may permit only selected transitions during selected scheduler phases.

The gate must preserve the canonical ternary relation.

---

## 70. First-Leg Scheduler Gate

A specialization may allow first-leg entry into neutral only on selected scheduler opportunities.

---

## 71. Second-Leg Scheduler Gate

Second-leg completion may use different scheduler opportunities.

This preserves independent leg timing.

---

## 72. Scheduler Retention

When the scheduler does not allow second-leg completion, the route may remain neutral-pending.

---

## 73. Capacity Interface

A route may depend on capacity state:

`X_capacity`.

Capacity can block otherwise valid state-changing events.

---

## 74. Capacity Guard

A generic guard is:

`G_capacity(X_route, X_capacity) ∈ {ALLOW, BLOCK}`.

---

## 75. Capacity-Blocked First Leg

If:

`-1 → 0`

or:

`1 → 0`

is blocked, the current state remains polarized under the canonical retain policy unless another action is defined.

---

## 76. Capacity-Blocked Second Leg

If:

`0 → t_pending`

is blocked, the route may remain:

`0`

with pending destination preserved.

---

## 77. Capacity Recovery

When capacity later becomes available, second-leg authorization may be reevaluated.

---

## 78. Capacity Is Not Neutral State

A zero-capacity condition is not active neutral.

Capacity state remains separately typed.

---

## 79. Active-Neutral Interface

Neutral routing operates on the active-neutral execution semantics defined in Chapter 06.

The state:

`0`

is the actual committed intermediate state.

It is not merely route metadata.

---

## 80. Neutral Residence State

During an active route:

`t_exec = 0`

while continuous upstream dynamics may continue.

The route state can therefore evolve independently from continuous phase or resonance state.

---

## 81. Neutral Residence Counter

A route may maintain:

`n_neutral`.

The counter can measure retained neutral execution opportunities.

---

## 82. Counter Initialization

The route contract must define whether:

`n_neutral`

starts at:

`0`

or:

`1`

upon first-leg completion.

---

## 83. Counter Increment

A neutral retention event may update:

`n_neutral ← n_neutral + 1`.

---

## 84. Counter Reset

The counter may reset on:

- route completion;
- route cancellation;
- route replacement;
- new route creation.

The rule must be explicit.

---

## 85. Minimum Residence Gate

A second leg may require:

`n_neutral ≥ n_min`.

This is a specialization-level routing rule.

---

## 86. Maximum Residence Gate

A route timeout may use:

`n_neutral > n_max`.

The resulting action must be defined.

---

## 87. Physical-Time Residence

A time-based implementation may use:

`t_neutral_entry`.

Then residence duration is:

`t_now - t_neutral_entry`.

---

## 88. Tact-Time Separation

Neutral tact count and physical duration remain distinct unless linked by an explicit timing model.

---

## 89. Route Age

A route age variable may track time since route creation rather than time since neutral entry.

The two quantities may differ.

---

## 90. Route Identifier

A route may carry:

`route_id`.

The identifier supports tracing and arbitration.

It is metadata.

---

## 91. Route Generation Number

A monotonically increasing generation counter may distinguish successive routes.

If it affects execution ordering, it belongs to deterministic state.

---

## 92. Stale Route

A route may be declared stale according to an explicit age or version rule.

Staleness is not ternary neutral.

---

## 93. Route Supersession

A newer authorized route may supersede an older route under a declared policy.

Supersession must update pending state deterministically.

---

## 94. Route Ownership

In a multi-source system, a route may carry source identity.

Source identity may participate in arbitration.

---

## 95. Multi-Source Targets

Targets may originate from:

- resonance;
- synchronization;
- coherence;
- supervisory logic;
- multiscale aggregation;
- learned policy.

Neutral routing receives the resolved target or explicit candidate set.

---

## 96. Route Source Does Not Change Transition Topology

The source of the target does not change the canonical valid ternary edges.

---

## 97. Resonance-Derived Route

A resonance-derived opposite target enters the same:

`-1 → 0 → 1`

or:

`1 → 0 → -1`

routing mechanism.

---

## 98. Synchronization-Derived Route

The same applies to synchronization-derived targets.

---

## 99. Coherence-Derived Route

The same applies to coherence-derived targets.

---

## 100. Learned Route

The same applies to learned target generation.

---

## 101. Supervisory Route

A supervisory target may request neutralization or polarization.

It remains subject to the same execution transition topology.

---

## 102. Route Neutralization

A target:

`t_target = 0`

may request:

`-1 → 0`

or:

`1 → 0`.

This is not an opposite-polarity route because the destination is neutral.

---

## 103. Neutralization Route Completion

A route whose requested destination is:

`0`

may complete after the single polarized-to-neutral commit.

No second leg is required.

---

## 104. Polarization from Neutral

A target:

`1`

or:

`-1`

from:

`t_exec = 0`

may complete in one neutral-to-polarized committed edge when authorized.

---

## 105. Same-Polarity Retention

If:

`t_target = t_exec`

the route system may retain the current state without creating a pending route.

---

## 106. Route Creation Predicate

A generic route-creation predicate is:

`CreateRoute(t_exec, t_target)`

true only when:

`t_exec ∈ {-1, 1}`

and:

`t_target = -t_exec`.

---

## 107. No Route for Same Polarity

If:

`t_target = t_exec`

no opposite route is required.

---

## 108. No Opposite Route for Neutral Target

If:

`t_target = 0`

from a polarized state, the transition is a direct valid polarized-to-neutral transition, not an opposite-polarity route.

---

## 109. No Opposite Route from Neutral

If:

`t_exec = 0`

a polarized target requires only one valid neutral-to-polarized edge.

---

## 110. Route State Machine

A minimal route state machine may use:

`IDLE`

`NEUTRAL_PENDING`.

Transitions include:

`IDLE → NEUTRAL_PENDING`

on first-leg opposite route creation;

`NEUTRAL_PENDING → IDLE`

on completion or cancellation.

---

## 111. Extended Route State Machine

A richer state machine may include explicit:

`FIRST_LEG_AUTH`

`FIRST_LEG_COMMIT`

`NEUTRAL_HOLD`

`SECOND_LEG_AUTH`

`SECOND_LEG_COMMIT`.

This supports more detailed audit traces.

---

## 112. Route State Machine versus Ternary Machine

The route-control machine and ternary execution state machine are distinct but coupled.

A route-control transition may occur without a ternary state change.

---

## 113. Route-Control Retention

A route-control state may remain unchanged while:

`t_exec`

also remains neutral.

These are two distinct retained variables.

---

## 114. State Transition Tuple

A committed routing update may be represented as:

`(x_route, request, auth) → x_route_next`.

The implementation must ensure that the projected:

`t_exec → t_exec_next`

edge belongs to the canonical ternary relation.

---

## 115. Route Determinism

A deterministic router returns the same next route state for identical:

- current route state;
- target;
- scheduler state;
- capacity state;
- authorization inputs;
- queue state;
- parameters.

---

## 116. Hidden Routing State

Undeclared route counters, priorities, queue contents, arbitration state, or pending metadata break deterministic closure when result-affecting.

---

## 117. Restart-Complete Route State

A restart-complete route snapshot may require:

- `t_exec`;
- `t_target`;
- `t_pending`;
- route phase;
- scheduler state;
- neutral residence state;
- capacity state;
- pending request queue;
- arbitration state.

Only result-affecting variables are required.

---

## 118. Restart while Polarized

A polarized restart with:

`t_pending = NONE`

must recover the same execution state and future routing behavior under identical inputs.

---

## 119. Restart while Neutral Pending

A restart during:

`t_exec = 0`

`t_pending = ±1`

must preserve the pending route exactly.

---

## 120. Restart after Cancellation

A cancelled route must not reappear after restart unless regenerated by the same deterministic upstream inputs.

---

## 121. Restart after Replacement

If pending destination was replaced before checkpointing, the replacement must persist across restart.

---

## 122. Route Serialization

A route serialization must encode every required state distinctly.

It must not conflate:

`0`

with:

`NONE`.

---

## 123. Route Schema

A route schema may contain:

- executed state;
- target;
- pending destination;
- route phase;
- residence counter;
- scheduler state;
- route identifier;
- authorization metadata.

Field presence depends on artifact purpose.

---

## 124. Route Trace

A route trace should preserve ordered execution events.

A minimal audit trace contains:

- execution coordinate;
- previous executed state;
- current executed state;
- target;
- pending destination.

---

## 125. Detailed Route Trace

A detailed trace may additionally contain:

- route phase;
- request type;
- authorization result;
- scheduler state;
- capacity state;
- route age;
- event type.

---

## 126. First-Leg Trace Event

A first-leg trace event records:

`-1 → 0`

or:

`1 → 0`

plus pending registration.

---

## 127. Neutral-Hold Trace Event

A neutral-hold event records:

`0 → 0`

with route state preserved or updated according to policy.

---

## 128. Second-Leg Trace Event

A second-leg event records:

`0 → 1`

or:

`0 → -1`

and pending-state clearing.

---

## 129. Cancellation Trace Event

A cancellation event records route termination without second-leg completion.

---

## 130. Replacement Trace Event

A replacement event records pending-destination change while:

`t_exec = 0`.

---

## 131. Route Validation

A route validator checks:

- canonical transition legality;
- pending registration;
- pending consistency;
- neutral residence;
- second-leg direction;
- pending clearing;
- cancellation semantics;
- deterministic ordering.

---

## 132. Direct-Opposite Validator

For each consecutive committed executed-state pair, reject:

`(-1, 1)`

and:

`(1, -1)`.

---

## 133. First-Leg Validator

If a route is created from opposite polarized states, verify that the first executed-state change terminates at:

`0`.

---

## 134. Pending Validator

Verify that the pending destination matches the intended opposite destination after first-leg completion.

---

## 135. Neutral-State Validator

Verify that an active pending route uses:

`t_exec = 0`

under the canonical route representation.

---

## 136. Second-Leg Validator

Verify that second-leg completion begins from:

`0`

and terminates at:

`t_pending`.

---

## 137. Pending-Clear Validator

Verify that route completion clears or transitions pending state according to the route contract.

---

## 138. Cancellation Validator

Verify that cancellation does not accidentally commit the pending destination.

---

## 139. Replacement Validator

Verify that replacement changes route-control state without direct opposite executed-state mutation.

---

## 140. Residence Validator

If minimum residence is configured, verify that second-leg completion does not occur before the required residence condition.

---

## 141. Capacity Validator

Verify that capacity-blocked transitions remain uncommitted.

---

## 142. Scheduler Validator

Verify that commits occur only on scheduler opportunities allowed by the specialization.

---

## 143. Queue Validator

If requests are queued, verify deterministic ordering and absence of unhandled overflow under the declared contract.

---

## 144. Replay Validator

Checkpoint and replay tests should reproduce:

- route state;
- pending destination;
- future event ordering;
- final executed state.

---

## 145. Route Invariant Counters

An implementation may expose counters such as:

`actual_direct_opposite_events`

`route_first_leg_events`

`route_second_leg_events`

`neutral_retention_events`

`route_cancel_events`

`route_replace_events`.

---

## 146. Direct-Opposite Counter Invariant

For conforming execution:

`actual_direct_opposite_events = 0`.

---

## 147. Reserved-State Counter

An implementation may track:

`reserved_state_events`.

Under the applicable canonical encoding contract:

`reserved_state_events = 0`.

---

## 148. Queue Overflow Counter

An implementation may track:

`queue_overflow_events`.

The expected value depends on the declared queue contract.

A configuration requiring no overflow preserves:

`queue_overflow_events = 0`.

---

## 149. Event Count Is Not State Semantics

Counters are observables.

They do not redefine route or ternary state.

---

## 150. Route Metrics

Possible route metrics include:

- first-leg count;
- completion count;
- cancellation count;
- mean neutral residence;
- maximum neutral residence;
- replacement count;
- blocked-leg count.

These are derived execution observables.

---

## 151. Route Latency

Route latency may be measured from:

- target generation;
- first-leg commit;
- route registration

to:

- second-leg commit.

The chosen start and end definitions must be explicit.

---

## 152. Tact Latency

Latency measured in execution tacts is not automatically physical time.

---

## 153. Physical-Time Latency

Physical route latency requires a timing mapping between execution and physical time.

---

## 154. Route Throughput

An implementation may measure completed routes per execution interval.

This is a benchmark quantity.

---

## 155. Route Capacity

Route capacity may describe the number of simultaneous pending routes supported by an implementation.

This is implementation-specific.

---

## 156. Single-Pending-Route Model

A simple local router may permit at most one pending destination per entity.

---

## 157. Multi-Route Queue Model

A more complex implementation may queue multiple future requests.

Only one executed ternary state exists per canonical local state component.

---

## 158. Queue versus State Explosion

Queued requests do not enlarge:

`T_exec`.

They enlarge execution-control state.

---

## 159. Per-Entity Routing

For entities:

`i = 1, ..., N`

each may maintain:

`t_exec_i`

`t_target_i`

`t_pending_i`.

---

## 160. Vector Routing State

The complete execution vector is:

`t_exec_vec ∈ {-1, 0, 1}^N`.

The pending vector may be:

`t_pending_vec ∈ {NONE, -1, 1}^N`.

---

## 161. Independent Local Routes

A model may route each entity independently if no shared constraints exist.

---

## 162. Coupled Local Routes

Routes may be coupled through:

- shared capacity;
- topology;
- scheduler;
- resource constraints;
- arbitration.

---

## 163. Shared-Capacity Routing

A shared capacity guard may allow only a bounded number of simultaneous transitions.

---

## 164. Shared Scheduler

One scheduler may coordinate multiple route components.

The scheduling policy must preserve deterministic ordering where required.

---

## 165. Simultaneous First Legs

Several local:

`polarized → 0`

transitions may occur in one commit boundary if capacity and scheduler rules allow.

---

## 166. Simultaneous Second Legs

Several local pending routes may complete simultaneously under the same conditions.

---

## 167. Mixed-Leg Commit

One entity may execute a first leg while another executes a second leg in the same global execution coordinate.

The route semantics remain local to each component.

---

## 168. Global Invariant Checking

A vector execution validator checks each local transition pair for direct opposite edges.

---

## 169. Local Neutral Count

A derived observable may count:

`N_0 = number of i such that t_exec_i = 0`.

This is not the same as global ternary state.

---

## 170. Neutral Fraction

A normalized observable may be:

`f_0 = N_0 / N`.

It remains a continuous or rational aggregate observable.

---

## 171. Neutral Fraction Is Not Global Neutral State

`f_0 = 1`

means all local states are neutral.

It does not create a separate new ternary state beyond the defined global model.

---

## 172. Multiscale Routing

A multiscale model may maintain route states at several scales.

For scale:

`ell`

define:

`X_route^(ell)`.

---

## 173. Scale-Specific Pending State

A pending route at one scale does not imply a pending route at another.

---

## 174. Cross-Scale Route Trigger

Completion or creation of a route at one scale may generate a request at another scale through an explicit mapping.

---

## 175. Cross-Scale Route Arbitration

Different scale-level requests may require arbitration before affecting a shared execution state.

---

## 176. Global Route Aggregation

A global route state may be derived from local route observables.

This aggregation is not generally invertible.

---

## 177. Neutral Routing and Resonance

Resonance determines or contributes to target generation.

Neutral routing begins after the target boundary.

Therefore:

`resonance classification ≠ route state`.

---

## 178. Neutral Routing and Synchronization

Synchronization may affect target generation.

It does not directly create a pending route unless the mapping and route-creation conditions are satisfied.

---

## 179. Neutral Routing and Coherence

The same applies to coherence.

---

## 180. Neutral Routing and Phase State

Phase state may continue evolving during routing.

Route state and phase state remain separately typed.

---

## 181. Neutral Routing and Frequency Memory

Retained frequency may continue evolving during neutral residence.

This does not alter the route invariant.

---

## 182. Neutral Routing and EIF State

The EIF layer may receive feedback based on route or executed state.

The route itself is not interatomic geometry, energy, or force.

---

## 183. Route-State Feedback

A feedback mapping may use:

`F_route→E: X_route × X_EIF → X_EIF,req`.

This is an explicit integration path.

---

## 184. Pending-State Feedback

A specialization may use pending-route state as an input to feedback.

The physical interpretation must be defined through the feedback mapping.

---

## 185. Route-Control Feedback Is Not Mechanical Force

A route-control variable is not a force vector.

---

## 186. Route-Control Feedback Is Not Energy

A route-control variable is not physical energy.

---

## 187. Route-Control Feedback Is Not Physical Phase

A route-control state is not material phase.

---

## 188. Route Transition versus Bifurcation

The invariant remains:

`route transition ≠ bifurcation`.

---

## 189. Route Transition versus Structural Transition

The invariant remains:

`route transition ≠ structural transition`.

---

## 190. Route Transition versus Physical Phase Transition

The invariant remains:

`route transition ≠ physical phase transition`.

---

## 191. Route Transition versus Resonance Transition

A route event and resonance regime event may be causally linked through target generation.

They remain distinct events.

---

## 192. Route Provenance

TR-EIF neutral-routing semantics carry:

`AUTHOR_DEFINED`

provenance where they originate in the framework.

Derived graph and route properties may carry:

`DERIVED`.

Implementation measurements carry:

`BENCHMARK`.

Test vectors carry:

`TEST_FIXTURE`.

---

## 193. Route Test Fixture

Canonical route fixtures include:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Additional fixtures may test:

- neutral retention;
- cancellation;
- replacement;
- capacity block;
- scheduler delay.

---

## 194. Invalid Route Fixture

A negative fixture may intentionally contain:

`-1 → 1`

or:

`1 → -1`

and must be rejected by validation.

---

## 195. FRP Executable Reference

FRP provides an executable specialization/reference of the neutral-routing architecture.

The relevant execution path is:

`target`

`→ scheduler`

`→ request handling`

`→ pending routing`

`→ active neutral`

`→ capacity`

`→ retained writeback`.

---

## 196. FRP First-Leg Reference

For opposite target:

`-1 → 1`

FRP executes:

`-1 → 0`

and retains pending destination:

`1`.

---

## 197. FRP Reverse First-Leg Reference

For:

`1 → -1`

FRP executes:

`1 → 0`

and retains pending destination:

`-1`.

---

## 198. FRP Second-Leg Reference

Pending routes later complete:

`0 → 1`

or:

`0 → -1`.

---

## 199. FRP Scheduler Reference

FRP scheduler modes include:

`7/1`

and:

`1/7`.

These modes regulate route execution timing.

---

## 200. FRP 7/1 Routing Context

The `7/1` mode represents seven balance tacts followed by one commit tact in the FRP specialization.

Routing events occur under the corresponding scheduler contract.

---

## 201. FRP 1/7 Routing Context

The `1/7` mode represents one excite tact followed by seven neutralize tacts in the FRP specialization.

This mode remains an implementation scheduler specialization.

---

## 202. FRP Capacity Boundary

FRP includes a capacity guard in the execution chain.

Capacity enforcement remains downstream of target generation and upstream of retained writeback.

---

## 203. FRP Pending-Routing Boundary

Pending routing is an explicit execution layer.

It is not inferred from target values alone.

---

## 204. FRP Active-Neutral Boundary

The active-neutral stage preserves the executed intermediate state:

`0`.

---

## 205. FRP State Update Boundary

Final retained-state writeback occurs after the applicable routing and execution conditions are satisfied.

---

## 206. FRP Invariant Counters

FRP qualification artifacts include execution invariant counters such as:

`actual_direct_events`

`reserved_state_events`

`queue_overflow_events`

under the applicable artifact schema.

The canonical direct-opposite invariant requires the corresponding direct-event count to remain zero.

---

## 207. FRP Route Parameter Scope

Scheduler ratios, queue capacities, internal counters, and other routing implementation parameters remain FRP-specific.

They are not universal TR-EIF constants.

---

## 208. Routing Extension Rule

Any new routing model must define:

1. executed state;
2. target state;
3. pending-state domain;
4. route-creation condition;
5. first-leg semantics;
6. neutral-retention semantics;
7. second-leg semantics;
8. cancellation;
9. replacement;
10. conflict handling;
11. scheduler interface;
12. restart state.

---

## 209. Route-Arbitration Extension Rule

Any arbitration mechanism must define:

1. candidate requests;
2. precedence;
3. tie handling;
4. stale-request handling;
5. cancellation policy;
6. deterministic ordering;
7. output action.

---

## 210. Queue Extension Rule

Any queue-based router must define:

1. queue capacity;
2. ordering;
3. admission;
4. overflow policy;
5. removal;
6. replay serialization.

---

## 211. Capacity Extension Rule

Any shared-capacity router must define:

1. capacity quantity;
2. allocation rule;
3. priority;
4. blocking behavior;
5. fairness or ordering where applicable;
6. replay state.

---

## 212. Trace Extension Rule

Any neutral-routing trace intended for audit must preserve enough information to reconstruct:

- first leg;
- pending registration;
- neutral residence;
- route conflict;
- cancellation or replacement;
- second leg;
- completion.

---

## 213. Canonical Routing Invariants

Every conforming neutral-routing model preserves:

1. `T_exec = {-1, 0, 1}`;

2. active `0`;

3. no direct committed `-1 → 1`;

4. no direct committed `1 → -1`;

5. opposite route begins with `polarized → 0`;

6. active pending route retains explicit destination;

7. second leg begins from `0`;

8. completion reaches the pending destination;

9. first and second legs are distinct commits;

10. target, pending, and executed state remain distinct.

---

## 214. Canonical Pending Invariants

Under canonical pending-route semantics:

1. `t_pending ∈ {NONE, -1, 1}`;

2. `NONE ≠ 0`;

3. active pending route uses `t_exec = 0`;

4. pending destination is not committed state;

5. neutral retention may preserve pending state;

6. completion clears or explicitly updates pending state.

---

## 215. Canonical Request Invariants

The routing layer preserves:

`request ≠ authorization`

`authorization ≠ commit`

`queued request ≠ pending destination`

`pending destination ≠ executed state`.

---

## 216. Canonical Event Invariants

The routing layer preserves:

`first leg ≠ second leg`

`neutral retention ≠ completion`

`cancellation ≠ completion`

`replacement ≠ commit`

`scheduler opportunity ≠ commit`

`capacity block ≠ invalid transition`

`route transition ≠ bifurcation`

`route transition ≠ structural transition`.

---

## 217. Canonical State-Separation Invariants

The routing layer preserves:

`0 ≠ NONE`

`0 ≠ INVALID`

`0 ≠ ERROR`

`pending ≠ target`

`pending ≠ executed state`

`route phase ≠ ternary state`

`scheduler phase ≠ ternary state`

`capacity state ≠ ternary state`.

---

## 218. Canonical Route Architecture

The canonical opposite-polarity route is:

`opposite target`

`→ first-leg request`

`→ first-leg authorization`

`→ polarized-to-neutral commit`

`→ pending registration`

`→ neutral residence`

`→ second-leg request`

`→ second-leg authorization`

`→ neutral-to-polarized commit`

`→ pending clear`

`→ route completion`.

---

## 219. Canonical Cancellation Architecture

A cancellation path is:

`active pending route`

`→ cancellation request`

`→ cancellation authorization`

`→ pending clear or replacement`

`→ retained neutral or policy-defined next state`.

No direct opposite commit is introduced.

---

## 220. Canonical Replacement Architecture

A replacement path is:

`active pending route`

`→ replacement request`

`→ arbitration`

`→ replacement authorization`

`→ pending destination update`

while:

`t_exec = 0`.

---

## 221. Canonical Hybrid Position

Neutral routing occupies the discrete execution layer of the broader chain:

`continuous dynamics`

`→ resonance state`

`→ ternary target`

`→ neutral routing`

`→ executed ternary state`

`→ feedback`.

---

## 222. Interface to Chapter 08

Chapter 08 develops Coupled Continuous-Discrete Dynamics.

The route state becomes an explicit discrete state component of the hybrid TR system.

Continuous phase and resonance state may evolve while a route remains:

`NEUTRAL_PENDING`.

---

## 223. Interface to Chapter 09

Chapter 09 develops stability and boundedness.

It will distinguish:

- route persistence;
- neutral residence;
- execution-state stability;
- continuous-state stability;
- hybrid stability.

---

## 224. Interface to Chapter 10

Chapter 10 develops Numerical Time Evolution.

It will define exact update ordering among:

- continuous integration;
- resonance evaluation;
- target registration;
- scheduler update;
- route request;
- pending update;
- capacity guard;
- committed ternary writeback.

---

## 225. Final Formal Structure

The neutral-routing layer may be represented as:

`NR = (T_exec, T_target, X_pending, X_route, X_sched, X_capacity, Q_req, F_route)`.

Here:

- `T_exec = {-1, 0, 1}`;
- `T_target = {-1, 0, 1}`;
- `X_pending = {NONE, -1, 1}` under the canonical local route model;
- `X_route` stores route-control state;
- `X_sched` stores scheduler state;
- `X_capacity` stores execution-capacity state;
- `Q_req` stores queued requests where applicable;
- `F_route` defines deterministic routing evolution.

The canonical opposite-polarity routes remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 226. Final Statement

Neutral routing defines how opposite ternary targets become legal committed execution paths.

The target layer may request:

`-1 → 1`

or:

`1 → -1`

as a change in desired state.

The executed state may not commit either change directly.

The routing layer therefore creates the staged paths:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

The first leg enters active neutral.

The pending destination preserves route intent.

Neutral residence may persist for multiple execution opportunities.

The second leg completes the route only after independent authorization.

Cancellation, replacement, arbitration, scheduling, capacity, queueing, and restart state remain explicit execution-control structures.

The balanced ternary kernel remains exactly:

`-1/0/1`.

The state:

`0`

remains active.

Direct committed opposite transitions remain forbidden.

This chapter therefore completes the neutral-routing layer required for the coupled continuous-discrete dynamics developed in Chapter 08.
