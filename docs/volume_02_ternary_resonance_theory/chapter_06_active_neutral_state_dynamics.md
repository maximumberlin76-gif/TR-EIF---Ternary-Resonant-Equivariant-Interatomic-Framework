# Active Neutral State Dynamics

## 1. Purpose

This chapter defines the active-neutral state dynamics of Ternary Resonance Theory.

The balanced ternary execution domain is:

`T = {-1, 0, 1}`.

The state:

`0`

is active neutral.

It is a valid internal execution state with explicit dynamical, routing, retention, mediation, and transition roles.

This chapter formalizes:

- active-neutral state identity;
- neutral entry;
- neutral residence;
- neutral retention;
- neutral exit;
- opposite-polarity mediation;
- target/execution separation;
- pending destination state;
- first-leg and second-leg execution;
- neutral-state persistence;
- neutral-state control;
- neutral-state interaction with continuous dynamics;
- deterministic state closure;
- multiscale neutral semantics;
- numerical realization;
- validation;
- executable specialization boundaries.

The central transition invariant is:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

are forbidden.

---

## 2. Balanced Ternary Execution Domain

The executed ternary state space is:

`T_exec = {-1, 0, 1}`.

The canonical compact notation is:

`-1/0/1`.

Every committed ternary execution state belongs exactly to this set.

No fourth committed ternary value belongs to the canonical execution domain.

---

## 3. Active Neutral

The state:

`0`

is a genuine member of:

`T_exec`.

Therefore:

`0 ∈ T_exec`.

Active neutral is not an external marker.

It is not:

- missing;
- undefined;
- unavailable;
- invalid;
- unresolved;
- error;
- uninitialized.

These conditions belong to separate state spaces.

---

## 4. Neutral-State Semantics

Active neutral may participate in:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization;
- capacity-controlled execution;
- intermediate state preservation.

The exact operational realization is specialization-specific.

The invariant identity remains:

`0` is active.

---

## 5. Neutral versus Missingness

Let:

`X_optional = {-1, 0, 1, NONE}`.

Then:

`0 ≠ NONE`.

A semantics-preserving representation must encode these states distinctly.

---

## 6. Neutral versus Invalid State

If an implementation defines:

`INVALID`

then:

`INVALID ∉ T_exec`.

Therefore:

`INVALID ≠ 0`.

---

## 7. Neutral versus Error State

Likewise:

`ERROR ≠ 0`.

An error condition must not silently become an active-neutral execution state.

---

## 8. Neutral versus Validation State

A validation value such as:

`UNRESOLVED`

does not equal:

`0`.

Validation state and ternary execution state remain separately typed.

---

## 9. Canonical Transition Relation

Let:

`R_T ⊆ T_exec × T_exec`

be the committed transition relation.

The canonical relation permits:

`-1 → -1`

`-1 → 0`

`0 → -1`

`0 → 0`

`0 → 1`

`1 → 0`

`1 → 1`.

The direct opposite transitions:

`-1 → 1`

and:

`1 → -1`

are excluded.

---

## 10. Retention Transitions

The self-transitions:

`-1 → -1`

`0 → 0`

`1 → 1`

are retention transitions.

They preserve the currently executed ternary state.

---

## 11. Polarized-to-Neutral Transitions

The transitions:

`-1 → 0`

and:

`1 → 0`

enter active neutral.

These transitions may serve as first legs of opposite-polarity routes.

---

## 12. Neutral-to-Polarized Transitions

The transitions:

`0 → -1`

and:

`0 → 1`

exit active neutral.

They may serve as second legs of opposite-polarity routes.

---

## 13. Direct Opposite Transition Exclusion

The canonical execution relation excludes:

`-1 → 1`

and:

`1 → -1`.

This is an exact categorical invariant.

It is not tolerance-based.

---

## 14. Neutral Mediation

Every valid committed opposite-polarity route contains:

`0`.

Therefore:

`-1 → 1`

must be executed as:

`-1 → 0 → 1`.

The reverse route:

`1 → -1`

must be executed as:

`1 → 0 → -1`.

---

## 15. First-Leg Transition

For current state:

`t_exec = -1`

and opposite target:

`t_target = 1`

the first committed state-changing leg is:

`-1 → 0`.

For:

`t_exec = 1`

and:

`t_target = -1`

the first leg is:

`1 → 0`.

---

## 16. Second-Leg Transition

After the first leg, the second leg may later complete:

`0 → 1`

or:

`0 → -1`.

The second leg is a distinct committed transition event.

---

## 17. Independent-Leg Invariant

The two legs of an opposite-polarity route are independent committed events.

Completion of:

`-1 → 0`

does not imply that:

`0 → 1`

has also occurred.

Completion of:

`1 → 0`

does not imply that:

`0 → -1`

has also occurred.

---

## 18. Minimum Route Length

Counting only state-changing committed edges, an opposite-polarity route requires at least two legs.

The shortest routes are exactly:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 19. Neutral Residence

After entering:

`0`

the execution may remain neutral before completing the next state-changing transition.

A valid route may therefore be:

`-1 → 0 → 0 → ... → 0 → 1`.

Likewise:

`1 → 0 → 0 → ... → 0 → -1`.

---

## 20. Neutral Retention

A neutral retention event is:

`0 → 0`.

It preserves the executed neutral state.

It does not count as an additional polarity-changing leg.

---

## 21. Neutral Residence Duration

The foundational kernel does not impose one universal neutral residence duration.

Residence may be measured in:

- execution tacts;
- scheduler cycles;
- numerical steps;
- physical time where explicitly mapped.

The applicable coordinate must remain explicit.

---

## 22. Minimum Neutral Residence

A specialization may require a minimum neutral residence.

For example:

`n_neutral ≥ n_min`.

Such a constraint is a specialization-level execution rule.

---

## 23. Maximum Neutral Residence

A specialization may also define a maximum neutral residence.

If used, the resulting timeout or fallback semantics must be explicit.

---

## 24. Unbounded Neutral Residence

The foundational state topology permits continued neutral retention when:

`0 → 0`

remains admissible.

This does not imply that every specialization permits unlimited residence.

---

## 25. Neutral Entry Event

A neutral-entry event is a committed transition:

`-1 → 0`

or:

`1 → 0`.

The event may include metadata describing:

- source state;
- target;
- pending destination;
- scheduler state;
- authorization;
- execution coordinate.

---

## 26. Neutral Exit Event

A neutral-exit event is:

`0 → -1`

or:

`0 → 1`.

The event may complete a pending route or represent another authorized neutral-to-polarized transition.

---

## 27. Neutral Retention Event

A neutral-retention event is:

`0 → 0`.

Its occurrence must remain distinguishable from:

- no execution opportunity;
- invalid update;
- rejected request;
- missing trace sample.

---

## 28. No-Operation versus Neutral Retention

A computational no-operation is not automatically equivalent to:

`0 → 0`.

A neutral-retention event is a semantic execution event only when the execution contract defines it as such.

---

## 29. Target Space

The target space remains:

`T_target = {-1, 0, 1}`.

Target and executed state share the same value set but remain distinct semantic spaces.

---

## 30. Target/Execution Separation

The invariant is:

`target ≠ executed state`.

The target expresses requested state.

The executed state expresses retained committed state.

---

## 31. Opposite Target while Polarized

A valid configuration may be:

`t_exec = -1`

`t_target = 1`.

This is not a contradiction.

It represents an opposite-polarity request pending execution semantics.

---

## 32. Opposite Target First Leg

From:

`t_exec = -1`

`t_target = 1`

a valid first-leg commit produces:

`t_exec,next = 0`.

The target may remain:

`1`.

---

## 33. Reverse Opposite Target First Leg

From:

`t_exec = 1`

`t_target = -1`

a valid first-leg commit produces:

`t_exec,next = 0`.

The target may remain:

`-1`.

---

## 34. Target during Neutral Residence

A valid state may be:

`t_exec = 0`

`t_target = 1`.

Likewise:

`t_exec = 0`

`t_target = -1`.

These states remain distinct.

---

## 35. Neutral Target

A valid configuration may also be:

`t_exec = 0`

`t_target = 0`.

This represents alignment between executed neutral and neutral target.

---

## 36. Polarized Execution with Neutral Target

A valid upstream state may contain:

`t_exec = -1`

`t_target = 0`

or:

`t_exec = 1`

`t_target = 0`.

Execution semantics determine whether and when:

`-1 → 0`

or:

`1 → 0`

is committed.

---

## 37. Pending Destination

A staged opposite route may contain:

`t_pending`.

The canonical pending-state domain may be:

`X_pending = {NONE, -1, 1}`.

---

## 38. Pending Destination versus Executed State

The pending destination and executed state are distinct.

For example:

`t_exec = 0`

`t_pending = 1`

is not equivalent to:

`t_exec = 1`.

---

## 39. Pending Destination versus Target

Pending destination and current target may also differ if the target changes after route staging.

Therefore:

`t_pending ≠ t_target`

is admissible under a specialization that permits target recomputation during a pending route.

---

## 40. No Pending Route

The value:

`NONE`

means no pending opposite destination is retained.

It is not active neutral.

---

## 41. First-Leg Pending Registration

A first-leg transition may atomically establish:

`t_exec,next = 0`

and:

`t_pending,next = t_opposite`.

For example:

`(-1, NONE) → (0, 1)`.

---

## 42. Reverse First-Leg Pending Registration

Likewise:

`(1, NONE) → (0, -1)`.

---

## 43. Pending Route Completion

A second-leg commit may perform:

`(0, 1) → (1, NONE)`.

The reverse route may perform:

`(0, -1) → (-1, NONE)`.

---

## 44. Pending State Clearing

Successful second-leg completion clears the pending destination under the canonical staged-route interpretation.

The resulting value is:

`NONE`.

---

## 45. Pending State Retention

During neutral residence:

`(0, 1) → (0, 1)`

or:

`(0, -1) → (0, -1)`

may occur when the route remains pending.

---

## 46. Pending-State Invariant

If:

`t_pending = 1`

during a canonical pending route, then:

`t_exec = 0`.

If:

`t_pending = -1`

during a canonical pending route, then:

`t_exec = 0`.

A specialization that allows pending metadata outside neutral execution must define that broader semantics explicitly.

---

## 47. Pending Direction

The pending destination encodes intended second-leg polarity.

It does not necessarily encode the route origin.

---

## 48. Route-Origin State

If route origin is required for future logic or audit, it must be stored explicitly or reconstructible from the trace.

---

## 49. Route State

A complete route state may be represented as:

`x_route = (t_exec, t_target, t_pending, q_route)`.

Here:

`q_route`

may encode additional route-control state.

---

## 50. Route Phase

A specialization may define route phases such as:

- IDLE;
- FIRST_LEG_REQUESTED;
- NEUTRAL_PENDING;
- SECOND_LEG_READY;
- COMPLETE.

These are control states.

They are not ternary values.

---

## 51. Route Control versus Ternary State

A route-control enum must not be encoded semantically as:

`-1/0/1`

unless a separate explicit encoding map is used.

---

## 52. Pending Route Cancellation

A pending route may be cancelled only through an explicit execution operation.

Cancellation must define the resulting:

- executed state;
- pending state;
- target state;
- route-control state.

---

## 53. Cancellation while Neutral

A canonical cancellation may leave:

`t_exec = 0`

and clear:

`t_pending`.

The subsequent target remains governed by the selected policy.

---

## 54. Cancellation Does Not Mean Missingness

Clearing:

`t_pending`

to:

`NONE`

does not change:

`t_exec = 0`

into missing state.

---

## 55. Pending Route Replacement

A specialization may permit:

`t_pending = 1 → -1`

or the reverse while:

`t_exec = 0`.

This is a route-control state update.

It must be explicitly authorized.

---

## 56. Pending Replacement versus Direct Commit

Changing pending destination directly does not violate the opposite-transition invariant because:

`t_exec`

has not moved directly between opposite polarities.

---

## 57. Target Change during Pending Route

While:

`t_exec = 0`

and:

`t_pending = 1`

the target may change.

The execution policy must define whether to:

- preserve pending;
- replace pending;
- cancel route;
- hold neutral;
- recompute authorization.

---

## 58. Target Return to Neutral

If:

`t_target = 0`

during a pending route, the route does not automatically disappear.

Pending semantics remain governed by the explicit route policy.

---

## 59. Target Return to Origin

If an opposite target returns to the original polarity during neutral residence, the route policy must define whether the route:

- reverses;
- cancels;
- waits;
- completes the original pending destination.

---

## 60. Route Conflict

A route conflict exists when target, pending destination, and control state impose incompatible requested outcomes under the selected specialization.

A deterministic resolver must define the resulting action.

---

## 61. Route Arbitration

An arbitration mapping may be:

`A_route: X_Texec × X_ctrl × X_request → X_action`.

The output remains an execution action request before commit.

---

## 62. Request

An execution request proposes an admissible state change.

A request is not a committed transition.

---

## 63. Authorization

Authorization determines whether a requested transition may proceed.

Authorization is not the commit itself.

---

## 64. Commit

A commit mutates retained execution state.

Therefore:

`request ≠ authorization`

and:

`authorization ≠ commit`.

---

## 65. Neutral Entry Authorization

A transition:

`-1 → 0`

or:

`1 → 0`

may require scheduler, capacity, or other control authorization.

---

## 66. Neutral Exit Authorization

A second leg:

`0 → 1`

or:

`0 → -1`

may require separate authorization.

First-leg authorization does not imply second-leg authorization.

---

## 67. Independent Authorization

Each state-changing leg is independently authorized unless a specialization explicitly defines a stronger atomic contract while still preserving two distinct committed states.

---

## 68. Scheduler State

Let:

`X_sched`

be scheduler state.

The scheduler may determine when a transition opportunity exists.

Scheduler state is not ternary state.

---

## 69. Scheduler Opportunity

A scheduler opportunity may permit one execution-stage evaluation.

It does not guarantee state change.

---

## 70. Scheduler Retention

If the scheduler does not authorize a state change, the executed state may remain retained.

This may or may not be recorded as an explicit retention event depending on the trace contract.

---

## 71. Neutral Scheduler Interaction

While:

`t_exec = 0`

the scheduler may:

- retain neutral;
- authorize second-leg completion;
- process cancellation;
- process replacement;
- defer execution.

---

## 72. Capacity State

A specialization may include:

`X_capacity`.

Capacity may restrict whether an otherwise valid transition can commit.

---

## 73. Capacity Guard

A capacity guard may map:

`G_capacity: X_state → {ALLOW, BLOCK}`.

Its result remains a control value.

It is not:

`-1/0/1`.

---

## 74. Blocked Neutral Exit

If:

`0 → 1`

or:

`0 → -1`

is structurally valid but capacity-blocked, the system may retain:

`0`.

The pending destination may remain preserved.

---

## 75. Blocked Neutral Entry

If:

`-1 → 0`

or:

`1 → 0`

is blocked, the current polarized state remains retained unless another valid action is defined.

---

## 76. Capacity Block versus Invalid Transition

A capacity-blocked transition may be structurally valid but currently unauthorized.

This is different from a transition excluded by the canonical ternary relation.

---

## 77. Structurally Forbidden Transition

The direct opposite transitions are structurally forbidden:

`-1 → 1`

`1 → -1`.

No scheduler or capacity state can make them canonical valid edges.

---

## 78. Structurally Valid but Temporarily Blocked Transition

Examples include:

`0 → 1`

or:

`0 → -1`

when the route is valid but authorization is absent.

---

## 79. Neutral as Mediation State

Active neutral is the unique canonical intermediate vertex between opposite polarities.

This follows from the exact three-state domain and exclusion of direct opposite edges.

---

## 80. Neutral as Routing State

A pending route may use:

`0`

as the executed routing state while retaining a destination.

This makes neutral part of the execution-state machine rather than merely a classification outcome.

---

## 81. Neutral as Balancing State

A specialization may use neutral to reduce or balance an accumulated execution quantity.

The balancing mechanism must be explicitly defined.

---

## 82. Neutral as Damping State

A specialization may associate neutral residence with damping in an auxiliary continuous subsystem.

The damping variable and physical dimensions remain separate from ternary state.

---

## 83. Neutral as Controlled Neutralization State

A specialization may use:

`0`

to represent an explicitly controlled neutralized execution state.

The process producing neutralization must be defined separately from the ternary label itself.

---

## 84. Neutral as Transition Staging State

For opposite polarity, neutral provides the required committed intermediate state.

The staging semantics remain framework-wide.

---

## 85. Neutral Is Not Arithmetic Zero State of Every Variable

The condition:

`t_exec = 0`

does not imply:

`theta = 0`

`omega = 0`

`R = 0`

`C = 0`

`energy = 0`

`force = 0`.

These quantities belong to separate spaces.

---

## 86. Neutral versus Zero Phase

The invariant distinction is:

`t_exec = 0 ≠ theta = 0`.

The equality sign here refers to semantic non-identity, not numeric comparison.

---

## 87. Neutral versus Zero Phase Difference

`Delta theta_ij = 0`

indicates phase alignment for a pair.

It does not imply active neutral.

---

## 88. Neutral versus Zero Frequency

`omega_i = 0`

does not imply:

`t_exec_i = 0`.

---

## 89. Neutral versus Zero Phase Order

`R = 0`

does not imply:

`t_exec = 0`.

---

## 90. Neutral versus Zero Coherence

`C = 0`

does not imply:

`t_exec = 0`.

---

## 91. Neutral versus Zero Energy

`E = 0`

does not imply:

`t_exec = 0`.

---

## 92. Neutral versus Zero Force

A zero force vector does not imply active neutral.

---

## 93. Neutral versus Resonance Boundary

A resonance classification:

`BOUNDARY`

does not automatically imply:

`t_target = 0`

or:

`t_exec = 0`.

An explicit mapping is required.

---

## 94. Neutral versus Resonance Outside

Likewise:

`OUTSIDE`

does not automatically imply:

`-1`.

---

## 95. Neutral versus Resonance Inside

Likewise:

`INSIDE`

does not automatically imply:

`1`.

---

## 96. Continuous-to-Neutral Target

A continuous mapping may produce:

`t_target = 0`.

The execution layer then determines whether the current executed state:

- remains 0;
- enters 0 from -1;
- enters 0 from 1;
- awaits authorization.

---

## 97. Neutral Target from Negative Execution

If:

`t_exec = -1`

and:

`t_target = 0`

the structurally valid state-changing route is:

`-1 → 0`.

---

## 98. Neutral Target from Positive Execution

If:

`t_exec = 1`

and:

`t_target = 0`

the structurally valid state-changing route is:

`1 → 0`.

---

## 99. Neutral Target from Neutral Execution

If:

`t_exec = 0`

and:

`t_target = 0`

the state may retain:

`0 → 0`.

---

## 100. Polarized Target from Neutral Execution

If:

`t_exec = 0`

and:

`t_target = 1`

a structurally valid transition is:

`0 → 1`.

If:

`t_target = -1`

a structurally valid transition is:

`0 → -1`.

---

## 101. Same-Polarity Target

If:

`t_exec = 1`

and:

`t_target = 1`

the state may retain:

`1 → 1`.

Likewise for:

`-1`.

---

## 102. Opposite Target

If:

`t_exec = -1`

and:

`t_target = 1`

direct:

`-1 → 1`

is forbidden.

The route must first enter neutral.

---

## 103. Reverse Opposite Target

If:

`t_exec = 1`

and:

`t_target = -1`

direct:

`1 → -1`

is forbidden.

---

## 104. Execution Transition Function

A generic execution function may be:

`F_exec: X_Texec × T_target × X_ctrl → X_Texec`.

The function must preserve the canonical transition relation.

---

## 105. Complete Ternary Execution State

A complete execution state may be:

`X_Texec = T_exec × T_target × X_pending × X_sched × X_route × X_aux`.

A concrete specialization includes only result-affecting required components.

---

## 106. State Closure

If any omitted variable can alter:

`F_exec`

then the declared execution state is incomplete.

---

## 107. Deterministic Execution

For deterministic execution, identical complete execution state and identical inputs produce the same next execution state.

---

## 108. Hidden Route State

Undeclared pending, persistence, scheduler, capacity, arbitration, or route state breaks deterministic state closure when result-affecting.

---

## 109. Restart Completeness

A restart-complete execution representation must preserve every result-affecting state required to continue the route exactly.

---

## 110. Neutral Restart State

If the system restarts while:

`t_exec = 0`

the restart artifact must preserve the information required to determine why neutral is retained and what future route remains valid.

---

## 111. Pending-State Restart

When:

`t_pending ≠ NONE`

the pending destination must be retained for exact staged-route continuation.

---

## 112. Scheduler-State Restart

If scheduler state affects when the next leg may commit, scheduler state belongs to restart-complete execution state.

---

## 113. Capacity-State Restart

If capacity state is deterministic and result-affecting, it must also be recoverable or deterministically reconstructed.

---

## 114. Route Counter Restart

If neutral residence uses a counter:

`n_neutral`

that affects future eligibility, it belongs to restart state.

---

## 115. Neutral Residence Counter

A specialization may define:

`n_neutral[k]`.

On entry into neutral:

`n_neutral = 0`

or another declared initial value.

Each neutral retention may increment the counter.

---

## 116. Residence Counter versus Physical Time

The neutral counter measures execution events or tacts unless explicitly mapped to physical time.

---

## 117. Time-Based Neutral Residence

A physical-time model may instead retain:

`t_entry`

and evaluate:

`t - t_entry`.

The timing source must be explicit.

---

## 118. Neutral Exit Condition

A neutral exit may require a predicate:

`G_exit(X_Texec, X_ctrl) = true`.

This predicate may include:

- pending destination;
- minimum residence;
- scheduler state;
- capacity;
- external guard.

---

## 119. Neutral Retention Condition

If:

`G_exit = false`

the system may remain:

`0`.

The precise retained-state update must be defined.

---

## 120. Neutral Re-entry

A system already at:

`0`

does not perform a new entry transition when it retains:

`0`.

`0 → 0`

is retention, not entry from a polarized state.

---

## 121. Neutral Exit without Pending Route

A model may permit:

`0 → -1`

or:

`0 → 1`

without a pending route when the current target and control state authorize the transition.

This is distinct from pending-route completion.

---

## 122. Neutral Exit with Pending Route

When a pending route exists, the second leg may be constrained to match:

`t_pending`.

---

## 123. Pending-Destination Consistency

Under strict pending-route semantics:

`t_pending = 1`

authorizes only the pending route direction:

`0 → 1`.

Likewise:

`t_pending = -1`

corresponds to:

`0 → -1`.

---

## 124. Pending-Destination Mismatch

If current target conflicts with:

`t_pending`

the route policy must resolve the conflict before commit.

---

## 125. Second-Leg Completion

After successful second-leg commit:

`t_pending → NONE`.

Any route counters or route-control states must update according to the route-completion contract.

---

## 126. Route Completion Event

A route-completion event is distinct from the second-leg target generation event.

The completion event corresponds to committed execution state.

---

## 127. Route Abort Event

A route abort is a control event that terminates the staged route without completing the pending destination.

Its semantics must be explicit.

---

## 128. Route Abort versus Neutral Retention

An aborted route may leave:

`t_exec = 0`.

This differs from retaining an active pending route in neutral.

---

## 129. Neutral Orphan State

A specialization may define whether:

`t_exec = 0`

with:

`t_pending = NONE`

and polarized target is valid.

If valid, its execution policy must be explicit.

---

## 130. Neutral Stable State

The state:

`t_exec = 0`

may itself be a stable or retained execution state when target and control logic maintain neutral.

It is not required to be merely transient.

---

## 131. Neutral Persistence

Neutral may persist indefinitely under a specialization that continually authorizes retention and never authorizes exit.

This remains a valid ternary state trajectory if all invariants are preserved.

---

## 132. Neutral Attractor Language

Calling neutral an attractor requires an independently defined dynamical-system analysis.

Simple repeated:

`0 → 0`

retention does not by itself establish attractor semantics.

---

## 133. Neutral Stability

Likewise, neutral stability must be defined with respect to a specific execution or hybrid dynamical criterion.

Retention alone is not a universal stability proof.

---

## 134. Neutral Boundedness

Because:

`t_exec ∈ {-1, 0, 1}`

the ternary state itself is bounded.

This does not establish boundedness of the complete hybrid system.

---

## 135. Neutral and Continuous Dynamics

While:

`t_exec = 0`

continuous upstream variables may continue evolving.

Examples include:

- phase;
- frequency;
- resonance coordinates;
- coherence;
- geometry;
- learned state.

---

## 136. Continuous Evolution during Neutral Residence

Neutral residence does not imply frozen continuous state.

The hybrid system may therefore satisfy:

`t_exec[k] = 0`

for several execution coordinates while:

`x_C[k+1] ≠ x_C[k]`.

---

## 137. Target Recalculation during Neutral Residence

Because continuous state may evolve, the target may be recomputed while execution remains neutral.

The route policy must define how this affects pending execution.

---

## 138. Neutral-State Feedback

The executed neutral state may participate in feedback mappings.

For example:

`F_FB: T_exec × X_EIF → X_EIF,req`.

When:

`t_exec = 0`

the feedback mapping may produce a model-specific neutral-state response.

---

## 139. Neutral Feedback Is Not Zero Feedback by Identity

The fact that:

`t_exec = 0`

does not imply that every feedback output is numerically zero.

The feedback mapping determines the actual effect.

---

## 140. Neutral Energy Contribution

A model may define an energy contribution dependent on:

`t_exec = 0`.

This contribution need not be zero.

Ternary state and energy remain separately typed.

---

## 141. Neutral Force Contribution

Likewise, a neutral ternary state may influence a force model through an explicit mapping without implying zero force.

---

## 142. Neutral Geometry Relation

Neutral state does not imply any fixed geometry.

Geometric consequences require an explicit EIF feedback mapping.

---

## 143. Neutral Physical Phase Relation

Neutral state is not a physical material phase.

---

## 144. Neutral Structural Relation

Neutral execution state is not a structural classification.

---

## 145. Neutral Coherence Relation

Neutral execution state is not a coherence class.

---

## 146. Neutral Synchronization Relation

Neutral execution state is not a synchronization class.

---

## 147. Neutral Resonance Relation

Neutral execution state is not a resonance class.

---

## 148. Hierarchical Ternary State

A multiscale model may define ternary execution states at several scales.

For scale:

`ell`

let:

`t_exec^(ell) ∈ {-1, 0, 1}`.

---

## 149. Scale-Specific Neutral

The state:

`0`

at one scale does not imply:

`0`

at another scale.

Each scale-specific ternary state remains separately indexed.

---

## 150. Local Neutral and Global Polarization

A model may permit local:

`t_exec_i = 0`

while a higher-level target or execution state is polarized.

The cross-scale relation must be defined.

---

## 151. Global Neutral and Local Polarization

Likewise, a global neutral state may coexist with local polarized states if the aggregation contract permits it.

---

## 152. Multiscale Ternary Aggregation

A mapping:

`A_T: T^N → T`

may aggregate lower-scale states.

The active-neutral semantics of:

`0`

must be preserved.

---

## 153. Neutral Is Not Absent Vote

In aggregation, neutral must not be silently discarded as if no state were present.

If abstention is required, it needs a separate state.

---

## 154. Weighted Ternary Aggregation

A specialization may weight ternary states.

The mathematical output before final ternary classification may be continuous.

A separate mapping then returns:

`-1/0/1`.

---

## 155. Neutral Aggregation Region

A continuous aggregate may map to:

`0`

through an explicit decision region.

The aggregate value itself remains distinct from the ternary state.

---

## 156. Multiscale Opposite Transition

At every scale using the canonical ternary execution semantics, direct opposite committed transitions remain forbidden.

---

## 157. Cross-Scale Transition Coordination

A model may coordinate transition opportunities across scales.

The coordination policy remains separate from the local ternary transition relation.

---

## 158. Local Route State

Each local entity may maintain:

`t_exec_i`

`t_target_i`

`t_pending_i`.

---

## 159. Vector Ternary State

For:

`N`

entities:

`T_exec_vec ∈ {-1, 0, 1}^N`.

Each component preserves the canonical local transition invariant.

---

## 160. Simultaneous Local Transitions

Several entities may commit transitions in one execution coordinate.

The transition legality is checked per applicable state component and any coupled capacity constraints.

---

## 161. Global Direct-Opposite Count

An implementation may track:

`actual_direct_opposite_events`.

For a conforming execution:

`actual_direct_opposite_events = 0`.

---

## 162. Reserved-State Count

An implementation may track use of invalid or reserved encodings.

A conforming ternary state representation should preserve:

`reserved_state_events = 0`

under the applicable implementation contract.

---

## 163. Queue Overflow Boundary

If routing uses queues, overflow is an implementation event.

It is not active neutral.

The queue policy must define whether overflow is prohibited, rejected, or otherwise handled.

---

## 164. Exact Neutral Encoding

A ternary encoder:

`Enc_T`

must map:

`0`

to one unique semantic encoding distinct from:

`-1`

and:

`1`.

---

## 165. Encoding Injectivity

For exact ternary state recovery:

`Enc_T`

must be injective on:

`{-1, 0, 1}`.

---

## 166. Optional-State Encoding

If:

`NONE`

is also encoded, then the encoding must remain injective over:

`{-1, 0, 1, NONE}`.

---

## 167. Fixed-Width Machine Encoding

A machine representation may use more binary patterns than required by the ternary domain.

Unused patterns remain reserved or invalid according to the implementation contract.

---

## 168. Reserved Encoding Is Not Neutral

An unused machine code must not be decoded as:

`0`

unless it is explicitly the canonical encoding of neutral.

---

## 169. Numerical Approximation Does Not Apply to Ternary State Identity

Executed ternary state is categorical.

There is no approximate:

`0.0001 ≈ 0`

state inside:

`T_exec`.

A continuous value must be classified before entering the ternary domain.

---

## 170. Ternary Validation

A validator must verify:

`t_exec ∈ {-1, 0, 1}`

exactly.

---

## 171. Direct-Opposite Validation

For every consecutive committed state pair:

`(t_exec[k], t_exec[k+1])`

the validator must reject:

`(-1, 1)`

and:

`(1, -1)`.

---

## 172. First-Leg Validation

For an opposite request, the first committed change must enter:

`0`.

---

## 173. Second-Leg Validation

The second committed change must depart from:

`0`

toward the authorized destination.

---

## 174. Pending-State Validation

Where pending routing is used, the validator must verify consistency among:

- executed state;
- pending destination;
- route-control state;
- committed transition.

---

## 175. Neutral Retention Validation

A neutral retention event must preserve:

`t_exec = 0`.

If pending state is required to persist, the validator must verify that preservation as well.

---

## 176. Cancellation Validation

A cancellation validator must verify the declared clearing or replacement semantics.

---

## 177. Restart Validation

A restart test should reproduce the same future staged route from the same complete neutral-state checkpoint.

---

## 178. Deterministic Replay Validation

Deterministic replay may compare:

- executed state;
- target;
- pending destination;
- scheduler state;
- route counters;
- event sequence.

The comparison scope must be declared.

---

## 179. Trace Requirements

An execution trace intended to audit active-neutral behavior should contain sufficient information to distinguish:

- target;
- executed state;
- pending destination where applicable;
- first-leg commit;
- neutral retention;
- second-leg commit.

---

## 180. Trace Ordering

Execution events must be ordered.

Without ordering, the absence of direct opposite transitions cannot be verified reliably.

---

## 181. Presence of Neutral Is Not Sufficient

A trace containing:

`0`

does not alone prove correct neutral mediation.

The route ordering must show that opposite polarity changes were staged through neutral.

---

## 182. Presence of Both Polarities Is Not a Violation

A trace may contain both:

`-1`

and:

`1`.

The invariant is violated only if a direct committed edge connects them.

---

## 183. Neutral Route Trace Example

A valid committed state sequence is:

`-1`

`0`

`0`

`1`.

This contains:

- first leg;
- one neutral retention;
- second leg.

---

## 184. Reverse Neutral Route Trace Example

A valid reverse sequence is:

`1`

`0`

`0`

`0`

`-1`.

---

## 185. Invalid Route Trace Example

The sequence:

`-1`

`1`

contains a forbidden direct opposite committed transition.

---

## 186. Invalid Reverse Route Trace Example

The sequence:

`1`

`-1`

is likewise invalid.

---

## 187. Target Trace versus Execution Trace

A target sequence may contain:

`-1`

`1`

in consecutive target evaluations.

That alone is not a ternary execution invariant violation.

The prohibition concerns committed executed-state transitions.

---

## 188. Target Reversal Example

A valid target sequence may be:

`t_target: -1 → 1`.

If:

`t_exec = -1`

the execution must still route through:

`0`.

---

## 189. Continuous-State Trigger

A continuous variable may trigger an opposite target.

The active-neutral execution semantics remain unchanged regardless of the upstream trigger.

---

## 190. Resonance Trigger

A resonance-regime transition may produce an opposite target.

The execution route remains neutral-mediated.

---

## 191. Synchronization Trigger

A synchronization-derived target follows the same execution invariant.

---

## 192. Coherence Trigger

A coherence-derived target follows the same execution invariant.

---

## 193. Learned Trigger

A learned classifier may generate an opposite target.

Learning does not permit direct opposite commit.

---

## 194. Multiscale Trigger

A multiscale aggregator may generate an opposite target.

The same execution boundary applies.

---

## 195. Guard-Generated Neutral Target

A supervisory guard may generate:

`t_target = 0`.

This is a legitimate target value.

The guard condition itself remains separately typed.

---

## 196. Neutral Priority

A specialization may define that a neutral target has priority over polarized targets under selected conditions.

This is an arbitration rule.

It is not a foundational universal rule.

---

## 197. Neutral Fallback

A specialization may use neutral as an explicitly commanded fallback state.

Such a fallback is still a valid active ternary state, not an error marker.

---

## 198. Neutral Recovery State

A specialization may route certain rejected or conflicting requests toward:

`t_target = 0`.

This must be an explicit state-transition policy.

---

## 199. Rejection versus Neutralization

Rejecting a request and actively requesting neutral are different operations.

---

## 200. Neutralization Request

A neutralization request explicitly sets:

`t_target = 0`.

Execution then applies:

`-1 → 0`

`1 → 0`

or:

`0 → 0`

as appropriate.

---

## 201. Neutralization Commit

The actual committed state becomes:

`0`

only after the execution mapping performs the valid transition.

---

## 202. Neutral Persistence after Neutralization

After neutralization, the system may remain:

`0`

until another valid polarized transition is authorized.

---

## 203. Active-Neutral Hybrid Dynamics

A hybrid model may be written as:

`x_C[k+1] = F_C(x_C[k], t_exec[k], ...)`

`t_target[k+1] = P_CT(x_C[k+1], ...)`

`X_Texec[k+1] = F_exec(X_Texec[k], t_target[k+1], X_ctrl[k])`.

This preserves continuous and discrete state separation.

---

## 204. Continuous Feedback from Neutral State

The continuous update may explicitly depend on:

`t_exec = 0`.

This is one route by which active neutral can influence future continuous evolution.

---

## 205. Continuous Feedback Does Not Redefine Neutral

Different specializations may assign different continuous effects to:

`0`.

The ternary identity of:

`0`

remains unchanged.

---

## 206. Neutral and Resonance Memory

Neutral residence may coexist with evolving resonance memory.

The two memory structures remain distinct.

---

## 207. Neutral and Frequency Memory

Neutral residence may coexist with retained frequency dynamics.

For example, retained frequency may continue relaxing while:

`t_exec = 0`.

---

## 208. Neutral and Phase Evolution

Phase evolution may continue while the ternary execution state remains neutral.

Therefore neutral does not imply phase freeze.

---

## 209. Neutral and Coherence Evolution

Coherence may increase or decrease during neutral residence.

No direct identity exists between the two.

---

## 210. Neutral and Structural Evolution

Interatomic structure may evolve during neutral residence under the applicable coupled model.

Neutral does not imply structural stasis.

---

## 211. Neutral and Physical Time

A neutral state may persist over physical time if execution tact and physical time are explicitly related.

The mapping must be defined by the numerical or hardware realization.

---

## 212. Neutral-State Stability Analysis Boundary

Chapter 09 develops stability and boundedness.

This chapter defines state-transition semantics only.

Statements such as:

`neutral is stable`

require a specific stability definition and model.

---

## 213. Neutral-State Bifurcation Boundary

Entry into or exit from:

`0`

is a ternary transition.

It is not a bifurcation by identity.

---

## 214. Neutral-State Structural Boundary

Entry into:

`0`

is not a structural transition by identity.

---

## 215. Neutral-State Physical Phase Boundary

Entry into:

`0`

is not a physical phase transition.

---

## 216. Neutral-State Resonance Boundary

Entry into:

`0`

does not itself mean resonance entry, exit, or boundary contact.

---

## 217. Neutral-State Synchronization Boundary

Entry into:

`0`

does not imply synchronization or desynchronization.

---

## 218. Neutral-State Coherence Boundary

Entry into:

`0`

does not define coherence.

---

## 219. Transition Provenance

The balanced ternary execution semantics and active-neutral routing defined within TR-EIF carry the applicable framework provenance.

Implementation-specific scheduler, capacity, encoding, or timing rules retain their own provenance.

---

## 220. Author-Defined Execution Semantics

The TR-EIF active-neutral execution architecture is represented as:

`AUTHOR_DEFINED`

where it originates from the framework's ternary execution contract.

---

## 221. Derived Neutral Properties

Graph-separation and minimum-route properties derived from the transition topology carry:

`DERIVED`

provenance.

---

## 222. Implementation Benchmark Evidence

Measured execution behavior from a concrete implementation carries:

`BENCHMARK`

provenance.

---

## 223. Execution Test Fixtures

Controlled route vectors may carry:

`TEST_FIXTURE`

provenance.

Examples include:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 224. FRP Executable Reference

FRP provides an executable specialization/reference for the active-neutral execution architecture.

Its execution boundary preserves:

`-1/0/1`.

---

## 225. FRP Active Neutral

In the FRP executable reference:

`0`

is active.

It participates in:

- balance;
- routing;
- neutralization;
- transition staging;
- retention.

---

## 226. FRP Direct-Opposite Exclusion

FRP preserves:

`actual_direct_opposite_events = 0`

under the qualified execution behavior represented by the applicable reference artifacts.

---

## 227. FRP First-Leg Routing

For:

`-1`

toward target:

`1`

FRP preserves first-leg execution:

`-1 → 0`

with pending destination:

`1`.

---

## 228. FRP Reverse First-Leg Routing

For:

`1`

toward target:

`-1`

FRP preserves:

`1 → 0`

with pending destination:

`-1`.

---

## 229. FRP Pending Completion

The pending destination completes later through:

`0 → 1`

or:

`0 → -1`.

---

## 230. FRP Scheduler Modes

FRP scheduler modes include:

`7/1`

and:

`1/7`.

These modes control execution cadence and eligibility.

They do not redefine active-neutral state semantics.

---

## 231. FRP 7/1 Mode

The `7/1` scheduler mode represents seven balance tacts followed by one commit tact in the FRP specialization.

The ratio belongs to FRP execution control.

---

## 232. FRP 1/7 Mode

The `1/7` scheduler mode represents one excite tact followed by seven neutralize tacts in the FRP specialization.

The ratio belongs to FRP execution control.

---

## 233. FRP Scheduler Boundary

Scheduler mode affects when transition opportunities occur.

It does not change the canonical valid transition graph.

---

## 234. FRP Target Boundary

The FRP phase-derived target remains upstream of active-neutral execution.

A direct opposite target is permitted at the target layer.

A direct opposite committed transition remains forbidden.

---

## 235. FRP Phase-to-Target Rule

The FRP executable reference uses:

`sin(theta_i)`

with threshold magnitude:

`0.33`

to produce:

`t_target_i`.

This parameter remains FRP-specific.

---

## 236. FRP Retained Frequency during Neutral State

FRP retained-frequency behavior may continue while executed state is neutral.

This illustrates separation between continuous retained memory and discrete ternary execution.

---

## 237. FRP Phase Lag during Neutral State

The receiving-state:

`gamma_effective_i`

remains part of the phase layer.

It is not changed into ternary semantics when:

`t_exec = 0`.

---

## 238. FRP Phase Order during Neutral State

The phase-order observable:

`R`

may take any valid value in:

`[0, 1]`

while a ternary cell or aggregate is neutral according to the applicable state definition.

No identity:

`t_exec = 0 → R = 0`

exists.

---

## 239. FRP Deterministic Routing Evidence

The executable reference may be used to test deterministic staged routing, pending completion, and exclusion of direct opposite commits.

Implementation evidence remains scoped to the corresponding FRP artifact and configuration.

---

## 240. Active-Neutral Extension Rule

Any extension of active-neutral dynamics must define:

1. executed state space;
2. valid transition relation;
3. neutral-entry semantics;
4. neutral-retention semantics;
5. neutral-exit semantics;
6. target/execution relation;
7. pending-route semantics;
8. scheduler interaction;
9. restart state;
10. validation criteria.

---

## 241. Pending-Route Extension Rule

Any pending-route extension must define:

1. pending-state domain;
2. registration condition;
3. retention rule;
4. second-leg rule;
5. cancellation;
6. replacement;
7. conflict resolution;
8. restart serialization.

---

## 242. Neutral-Residence Extension Rule

Any residence mechanism must define:

1. time or tact coordinate;
2. minimum duration where applicable;
3. maximum duration where applicable;
4. counter or timestamp state;
5. exit predicate;
6. reset behavior.

---

## 243. Scheduler Integration Rule

Any scheduler integration must define:

1. scheduler state;
2. execution opportunity;
3. transition eligibility;
4. retention behavior;
5. ordering;
6. deterministic replay state.

---

## 244. Capacity Integration Rule

Any capacity guard must define:

1. capacity state;
2. allowed transitions;
3. blocked-transition behavior;
4. interaction with pending routes;
5. restart semantics.

---

## 245. Trace Extension Rule

Any trace intended to audit neutral dynamics must preserve enough state to distinguish:

- first leg;
- active neutral;
- neutral retention;
- pending route;
- second leg;
- cancellation;
- direct-opposite violation.

---

## 246. Canonical Active-Neutral Invariants

Every conforming active-neutral execution model preserves:

1. `T_exec = {-1, 0, 1}`;

2. `0` is active;

3. `0` is not missingness;

4. direct committed `-1 → 1` is forbidden;

5. direct committed `1 → -1` is forbidden;

6. opposite-polarity execution requires `0`;

7. first and second legs are distinct commits;

8. neutral may persist;

9. target remains distinct from executed state;

10. pending state remains distinct from executed state.

---

## 247. Canonical Route Invariants

For an active pending route:

1. the first leg terminates at `0`;

2. the pending destination is retained explicitly;

3. neutral retention does not complete the route;

4. second-leg completion begins from `0`;

5. completion clears or updates pending state according to the route contract;

6. no direct opposite commit occurs.

---

## 248. Canonical State-Separation Invariants

The active-neutral layer preserves:

`neutral ≠ missing`

`neutral ≠ invalid`

`neutral ≠ error`

`neutral ≠ unresolved`

`neutral ≠ zero phase`

`neutral ≠ zero frequency`

`neutral ≠ zero coherence`

`neutral ≠ zero phase order`

`neutral ≠ zero energy`

`neutral ≠ zero force`

`neutral ≠ resonance boundary`

`neutral ≠ synchronization class`

`neutral ≠ physical phase`.

---

## 249. Canonical Event-Separation Invariants

The layer preserves:

`target change ≠ commit`

`first leg ≠ second leg`

`neutral retention ≠ route completion`

`route cancellation ≠ route completion`

`scheduler opportunity ≠ commit`

`capacity block ≠ invalid transition`

`ternary transition ≠ bifurcation`

`ternary transition ≠ structural transition`

`ternary transition ≠ physical phase transition`.

---

## 250. Canonical Hybrid Architecture

The active-neutral execution layer occupies the discrete part of the hybrid chain:

`continuous state`

`→ resonance state`

`→ ternary target`

`→ execution request`

`→ first leg`

`→ active neutral`

`→ neutral residence`

`→ second leg`

`→ committed polarized state`.

For non-opposite targets, the required route may terminate earlier.

---

## 251. Interface to Chapter 07

Chapter 07 develops Neutral Routing in full detail.

It expands:

- pending-route state;
- route registration;
- route conflict;
- route replacement;
- route cancellation;
- second-leg eligibility;
- route completion;
- multi-request arbitration.

The present chapter establishes the active-neutral state semantics on which that routing layer operates.

---

## 252. Interface to Chapter 08

Chapter 08 develops coupled continuous-discrete dynamics.

Active neutral becomes an explicit discrete state interacting with:

- phase evolution;
- resonance evolution;
- target generation;
- feedback;
- interatomic state.

---

## 253. Interface to Chapter 09

Chapter 09 develops stability and boundedness.

It analyzes:

- neutral retention stability;
- polarized-state persistence;
- bounded hybrid trajectories;
- stability of coupled continuous-discrete dynamics.

The exact definitions remain separate from the state semantics established here.

---

## 254. Interface to Chapter 10

Chapter 10 develops numerical time evolution.

It defines:

- update order;
- target sampling;
- scheduler tact;
- pending-state update;
- neutral residence counters;
- committed writeback;
- deterministic replay.

---

## 255. Final Formal Structure

The active-neutral execution layer may be represented as:

`AN = (T_exec, T_target, X_pending, X_sched, X_route, R_T, F_exec)`.

Here:

- `T_exec = {-1, 0, 1}`;
- `T_target = {-1, 0, 1}`;
- `X_pending` stores pending opposite destinations;
- `X_sched` stores scheduler state;
- `X_route` stores additional route-control state;
- `R_T` is the canonical committed transition relation;
- `F_exec` is the execution update.

The core opposite-polarity paths remain:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 256. Final Statement

Active neutral is a first-class execution state of Ternary Resonance Theory.

The canonical balanced ternary kernel is:

`-1/0/1`.

The state:

`0`

is active.

It performs the mandatory mediation role between opposite polarities.

The direct committed transitions:

`-1 → 1`

and:

`1 → -1`

are forbidden.

Every opposite-polarity committed route therefore contains two distinct state-changing legs:

`-1 → 0`

followed later by:

`0 → 1`

or:

`1 → 0`

followed later by:

`0 → -1`.

Neutral retention:

`0 → 0`

may occur between these legs.

Target, pending destination, and executed state remain distinct semantic objects.

Continuous phase, resonance, synchronization, coherence, energy, force, geometry, and physical phase remain separate from active-neutral ternary state.

The active-neutral layer therefore provides the exact execution-state substrate required by the neutral-routing architecture developed in Chapter 07.
