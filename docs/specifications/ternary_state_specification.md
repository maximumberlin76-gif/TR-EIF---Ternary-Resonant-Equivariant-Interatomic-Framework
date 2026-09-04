# Ternary State Specification

## 1. Scope

This document defines the repository-level balanced ternary state specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- the canonical balanced ternary state set;
- canonical state notation;
- semantic typing of ternary states;
- polarity labels;
- active-neutral membership;
- target-state typing;
- retained-state typing;
- pending-state separation;
- missing-data separation;
- continuous-to-ternary boundary;
- serialization requirements;
- implementation correspondence;
- cross-domain distinctions;
- validation requirements.

Detailed transition execution, transition guards, and neutral routing are defined by their corresponding mathematical and specification layers.

---

## 2. Canonical State Space

The canonical balanced ternary state space is:

`T = {-1, 0, 1}`

The canonical compact notation is:

`-1/0/1`

No fourth state belongs to the canonical balanced ternary state space.

For every ternary state:

`t ∈ T`

exactly one of the following holds:

`t = -1`

`t = 0`

`t = 1`

---

## 3. Canonical State Labels

The three canonical semantic labels are:

- `NEGATIVE` for `-1`;
- `NEUTRAL` for `0`;
- `POSITIVE` for `1`.

The correspondence is:

`NEGATIVE ↔ -1`

`NEUTRAL ↔ 0`

`POSITIVE ↔ 1`

These labels identify states of the balanced ternary state space.

They do not define physical sign, energy sign, force direction, charge sign, spatial orientation, or validation status.

---

## 4. Semantic Type

A quantity has balanced ternary semantics only when its declared type is a ternary state or a mapping explicitly produces a ternary state.

Numerical equality with one of:

`-1`

`0`

`1`

does not by itself assign ternary semantics.

Examples of quantities that may numerically equal a ternary value while remaining outside `T` include:

- formal charge;
- integer counter;
- scale index;
- graph index;
- classifier code;
- benchmark value;
- validation code;
- scalar feature;
- physical observable.

Semantic type is determined by the declared state space.

---

## 5. Negative State

The state:

`-1`

is the negative-polarity member of `T`.

Its canonical label is:

`NEGATIVE`

The negative ternary state is not automatically identified with:

- negative energy;
- negative force;
- negative electric charge;
- negative spatial direction;
- failed validation;
- outside-resonance classification.

Any such correspondence requires a separate explicit mapping.

---

## 6. Neutral State

The state:

`0`

is the neutral member of `T`.

Its canonical label is:

`NEUTRAL`

The state `0` is an active state of the TR-EIF balanced ternary system.

Its detailed dynamical and routing semantics are defined by the active-neutral and neutral-routing contracts.

The state `0` is not a missing-value marker.

---

## 7. Positive State

The state:

`1`

is the positive-polarity member of `T`.

Its canonical label is:

`POSITIVE`

The positive ternary state is not automatically identified with:

- positive energy;
- positive force;
- positive electric charge;
- positive spatial direction;
- successful validation;
- inside-resonance classification.

Any such correspondence requires a separate explicit mapping.

---

## 8. Polarity

The states:

`-1`

and:

`1`

are opposite ternary polarities.

The state:

`0`

is the active neutral member between the two polarities under the TR-EIF transition semantics.

Polarity is a ternary-state property.

It is not a spatial transformation.

It is not a physical vector direction.

It is not an electric-charge definition.

---

## 9. Canonical State Equality

Ternary-state equality is exact categorical equality within `T`.

For:

`t_a, t_b ∈ T`

the relation:

`t_a = t_b`

means that both variables represent the same ternary state.

No numerical tolerance is applied to exact ternary-state equality.

---

## 10. Ternary State and Boolean State

Balanced ternary state is not Boolean state.

The Boolean set:

`{false, true}`

and the balanced ternary set:

`{-1, 0, 1}`

are distinct state spaces.

Boolean `false` is not ternary `0`.

Boolean `true` is not ternary `1`.

A Boolean predicate must not be used as a substitute for a three-state ternary variable.

---

## 11. Executed Retained State

The executed retained ternary state is denoted:

`t_exec ∈ T`

It represents the ternary state retained after the applicable execution semantics have been applied.

The executed retained state is an execution-state variable.

It is not identical to a requested target by definition.

---

## 12. Requested Target State

A requested ternary target is denoted:

`t_target ∈ T`

It represents a requested or computed ternary destination.

The target-state domain is:

`T_target = {-1, 0, 1}`

The target is distinct from the executed retained state.

Therefore:

`t_target ≠ t_exec`

may hold during a valid execution sequence.

Target generation does not itself constitute committed execution.

---

## 13. Target and Retained-State Separation

The architecture preserves the sequence:

`source state`

`→ ternary target`

`→ execution boundary`

`→ retained ternary state`

The target and retained state occupy separate semantic roles even though both take values in `T`.

A target value does not become the retained value until the applicable execution rule commits that state.

---

## 14. Pending Destination

A pending destination is execution-control state associated with an incomplete routed transition.

Where the canonical opposite-polarity routing representation is used:

`t_pending ∈ {NONE, -1, 1}`

`NONE`

denotes the absence of a pending destination.

`NONE`

is not a member of:

`T`

and:

`NONE ≠ 0`

A pending destination is not the active neutral state.

---

## 15. State and Absence Separation

The canonical ternary state space contains no missing-state token.

The following conditions are outside `T` unless an explicit separate mapping is declared:

- missing;
- unavailable;
- undefined;
- invalid;
- NaN;
- masked;
- padded;
- unresolved;
- abstained;
- absent;
- uninitialized.

These conditions must remain representationally distinguishable from:

`0`

---

## 16. Neutral and Missingness

The relation:

`0 ≠ missing`

is a framework invariant.

Likewise:

`0 ≠ invalid`

`0 ≠ NaN`

`0 ≠ masked`

`0 ≠ padding`

`0 ≠ unavailable`

`0 ≠ abstention`

A data representation that contains both neutral state and missingness must encode them separately.

---

## 17. Continuous-to-Ternary Boundary

A continuous variable is not a ternary state.

Let:

`X_C`

be a continuous source space.

A ternary-target mapping may be defined as:

`P_CT: X_C → T`

For:

`x_C ∈ X_C`

the mapping produces:

`t_target = P_CT(x_C)`

The source value remains an element of `X_C`.

The resulting target is an element of `T`.

The mapping establishes the semantic boundary between the two spaces.

---

## 18. Threshold Classification

A scalar threshold mapping may classify a continuous value into:

`-1`

`0`

or:

`1`

only through an explicitly defined threshold contract.

The current reference target mapping uses two ordered thresholds:

`eta_negative < eta_positive`

with:

`x < eta_negative → -1`

`eta_negative ≤ x ≤ eta_positive → 0`

`x > eta_positive → 1`

Exact threshold values therefore map to:

`0`

under this reference mapping.

The numerical threshold values themselves are model parameters.

They are not universal values of the balanced ternary state space.

---

## 19. Resonance-to-Ternary Boundary

A resonance coordinate or resonance descriptor is not a ternary state.

Let:

`X_R`

be a resonance-coordinate space.

A model may define:

`P_RT: X_R → T`

or a history-dependent extension.

The existence of such a mapping does not identify:

`X_R`

with:

`T`

---

## 20. Resonance Classification Separation

The resonance classification set:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`

is distinct from:

`T = {-1, 0, 1}`

The following identifications are not automatic:

`OUTSIDE = -1`

`BOUNDARY = 0`

`INSIDE = 1`

A specialized model may define a mapping between these sets only by an explicit contract.

---

## 21. Phase-Order Separation

A phase-order value is a continuous quantity.

A phase-order value numerically equal to:

`0`

or:

`1`

does not become a ternary state from numerical equality.

The relation:

`phase order ≠ ternary state`

is retained.

---

## 22. Coherence Separation

A coherence observable is not a ternary state.

A coherence observable must enter the ternary domain only through an explicit mapping if such a mapping is defined.

The relation:

`coherence ≠ ternary state`

is retained.

---

## 23. Energy Separation

Energy and ternary state belong to different codomains.

Therefore:

`ternary state ≠ energy`

The ternary labels `-1`, `0`, and `1` must not be interpreted as energy levels unless a separate model explicitly defines such a mapping.

---

## 24. Force Separation

Force and ternary state belong to different mathematical spaces.

Therefore:

`ternary state ≠ force`

A ternary polarity does not define a force-vector direction.

---

## 25. Formal Charge Separation

Formal ionic charge and balanced ternary state belong to separate semantic domains.

A formal charge numerically equal to:

`-1`

`0`

or:

`1`

remains a formal-charge value.

In particular:

`formal charge neutrality ≠ active ternary neutral state`

Therefore:

`Q = 0`

does not imply:

`t = 0`

---

## 26. Spatial Transformation Separation

Spatial transformations and ternary polarity are distinct.

The following relations apply:

`spatial rotation ≠ ternary polarity reversal`

`spatial reflection ≠ ternary polarity reversal`

`atomic permutation ≠ ternary-state transition`

A spatial transformation does not automatically alter a ternary state.

---

## 27. Scale Separation

A scale label or scale index is not a ternary state.

A numerical scale index equal to `0` or `1` retains scale semantics.

The relation:

`scale index ≠ ternary state`

is retained.

---

## 28. Validation Separation

Validation status and balanced ternary state belong to separate sets.

For:

`K_val = {PASS, FAIL, UNRESOLVED}`

the relation is:

`K_val ≠ T`

A validation result must not be encoded as a ternary state unless an independent mapping is explicitly defined.

---

## 29. Provenance Separation

A provenance class is metadata.

The provenance classes:

- `PRIMARY_SOURCE`;
- `DERIVED`;
- `CALIBRATED`;
- `AUTHOR_DEFINED`;
- `BENCHMARK`;
- `TEST_FIXTURE`;
- `REQUIRES_SOURCE`;
- `REQUIRES_TEST`

are not ternary states.

---

## 30. Training-State Separation

A training-stage identifier is not a ternary state.

A training-stage transition is not a ternary-state transition.

An optimization variable numerically equal to `-1`, `0`, or `1` remains an optimization variable unless explicitly mapped into `T`.

---

## 31. Physical Phase Separation

Physical phase of matter and balanced ternary state are distinct state concepts.

A solid, liquid, gaseous, or other material-phase classification is not a ternary state by default.

A structural transition is not a ternary transition.

A physical phase transition is not a ternary transition.

---

## 32. Machine Representation

A machine representation of ternary state must preserve an unambiguous one-to-one correspondence with:

`{-1, 0, 1}`

A representation must not collapse:

- neutral state and missingness;
- neutral state and unavailable data;
- target state and retained state;
- ternary state and Boolean state.

Storage format does not redefine semantic type.

---

## 33. Integer Representation

The reference Python implementation represents the canonical states through integer-valued enum members:

`NEGATIVE = -1`

`NEUTRAL = 0`

`POSITIVE = 1`

This is an implementation correspondence to the formal state set.

The integer storage representation does not imply that arbitrary Python integers are valid ternary states.

---

## 34. Boolean Exclusion in the Reference Implementation

The reference Python validation boundary rejects Boolean values as ternary states.

Although Boolean values have integer behavior in Python, the implementation preserves:

`Boolean state ≠ ternary state`

This prevents machine-language type inheritance from changing the mathematical state contract.

---

## 35. Ternary Vector

A ternary state vector is an ordered tuple:

`t_vec = (t_1, ..., t_N)`

with:

`t_i ∈ T`

for every component.

The vector domain is:

`T^N`

for the declared positive component count `N`.

Each component preserves the same state specification defined in this document.

---

## 36. Vector Component Independence

Membership of a vector in:

`T^N`

does not imply that all components have identical state.

Each component has its own ternary state.

Relations between components require an additional model or coupling definition.

---

## 37. State Conversion

Conversion into `T` must be explicit.

A valid conversion operation must identify:

- source domain;
- target domain;
- mapping rule;
- all parameters affecting classification;
- boundary behavior;
- history dependence when present.

Implicit numeric casting is not a scientific state mapping.

---

## 38. State Serialization

A serialized ternary state must preserve the exact state identity.

A serialization-deserialization cycle must preserve semantic state:

`deserialize(serialize(t)) = t`

for every:

`t ∈ T`

under the declared serialization contract.

---

## 39. Target Serialization

If target state and retained state are serialized in the same artifact, they must remain separately identifiable fields or separately typed values.

Serialization must not collapse:

`t_target`

and:

`t_exec`

into one state field when their values or roles differ.

---

## 40. Pending-State Serialization

A pending destination must remain distinguishable from:

- no pending destination;
- retained neutral state;
- requested neutral target.

In particular:

`pending NONE ≠ neutral 0`

---

## 41. Trace Representation

A ternary execution trace may record:

- previous retained state;
- requested target;
- pending destination;
- transition route;
- resulting retained state.

The trace representation is an observable record.

The trace is not itself the ternary state machine.

---

## 42. Determinism Requirement

For a deterministic ternary mapping or execution operator, identical admissible inputs and identical declared state must produce identical ternary outputs under the same execution contract.

Any history-dependent input that affects the result belongs to the deterministic state closure.

---

## 43. Exact-State Validation

Tests of canonical ternary state membership use exact state identity.

The validation conditions include:

- only `-1`, `0`, and `1` are accepted as canonical states;
- Boolean values are not accepted as ternary states by the reference Python validator;
- no missing-state token is accepted as active neutral;
- target and retained-state objects remain separately representable.

---

## 44. Cross-Layer Invariants

The following relations are preserved across TR-EIF layers:

`T = {-1, 0, 1}`

`0 ∈ T`

`target ≠ executed retained state`

`pending target ≠ active neutral state`

`missing ≠ 0`

`invalid ≠ 0`

`formal charge ≠ ternary state`

`validation status ≠ ternary state`

`scale index ≠ ternary state`

`resonance classification ≠ ternary state`

`energy ≠ ternary state`

`force ≠ ternary state`

`spatial rotation ≠ ternary polarity reversal`

---

## 45. Transition-Semantics Boundary

This specification defines the ternary state domain.

It does not independently define the complete transition relation.

Transition semantics additionally define:

- allowed committed transitions;
- forbidden committed transitions;
- neutral entry;
- neutral exit;
- execution guards;
- pending-route semantics;
- conflict handling;
- retention behavior.

Those rules operate on the state space defined here.

---

## 46. Active-Neutral Boundary

This specification establishes that:

`0`

is the active neutral member of the canonical state space.

The detailed operational meaning of active neutral is defined by the active-neutral dynamics and neutral-routing layers.

State identity and state dynamics remain separate specification levels.

---

## 47. Framework References

The mathematical notation used by this specification is defined in:

`docs/volume_01_mathematical_foundations/chapter_02_notation_and_definitions.md`

The continuous-to-ternary mapping formalism is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_05_continuous_to_ternary_mapping.md`

Active-neutral dynamics are defined in:

`docs/volume_02_ternary_resonance_theory/chapter_06_active_neutral_state_dynamics.md`

Neutral routing is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_07_neutral_routing.md`

The repository-level architectural boundary is defined in:

`docs/architecture/framework_architecture.md`

---

## 48. Reference Implementation

The executable balanced ternary state representation is located in:

`src/tr_eif/ternary/state.py`

The executable target-mapping layer is located in:

`src/tr_eif/ternary/target.py`

The retained execution-state layer is located in:

`src/tr_eif/ternary/execution.py`

The executable implementation must preserve the canonical state set and semantic distinctions defined by this specification.

---

## 49. Specification Invariants

A TR-EIF ternary-state realization satisfies this specification only when all of the following hold:

1. the state domain contains exactly `-1`, `0`, and `1`;
2. the canonical notation is `-1/0/1`;
3. `0` remains a valid active ternary state;
4. arbitrary missingness is not encoded as `0`;
5. target and retained state remain separate semantic variables;
6. pending destination remains separate from neutral state;
7. Boolean state is not substituted for ternary state;
8. continuous values enter `T` only through explicit mappings;
9. resonance classification is not automatically identified with ternary state;
10. physical quantities do not acquire ternary semantics from numeric equality;
11. provenance and validation states remain separate from `T`;
12. machine serialization preserves exact state identity.

---

## 50. Specification Closure

The balanced ternary state contract is defined by:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and semantic labels:

`NEGATIVE / NEUTRAL / POSITIVE`

The state space is used by target-generation and execution layers while preserving:

`target ≠ executed retained state`

and:

`missingness ≠ active neutral 0`

Transition execution, active-neutral dynamics, and neutral routing apply additional rules to this state space without redefining its canonical membership.
