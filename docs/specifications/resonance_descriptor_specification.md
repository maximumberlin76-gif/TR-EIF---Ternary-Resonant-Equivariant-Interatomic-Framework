# Resonance Descriptor Specification

## 1. Scope

This document defines the repository-level resonance descriptor specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- continuous resonance state;
- oscillator phase and frequency state;
- phase-order observable;
- frequency-spread observable;
- executable reference descriptor;
- resonance coordinate;
- resonance space;
- resonance window;
- resonance-region classification;
- descriptor dimensionality;
- descriptor validation;
- source-state separation;
- geometry separation;
- thermodynamic-state separation;
- coherence separation;
- synchronization separation;
- balanced-ternary separation;
- continuous-to-ternary boundary;
- E(3) representation boundary;
- FLiBe specialization boundary;
- deterministic descriptor construction;
- executable reference correspondence.

The formal resonance theory is defined in:

`docs/volume_02_ternary_resonance_theory/`

The continuous-to-ternary mapping is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_05_continuous_to_ternary_mapping.md`

Balanced ternary state semantics are defined in:

`docs/specifications/ternary_state_specification.md`

Neutral routing is defined in:

`docs/specifications/neutral_routing_specification.md`

---

## 2. Resonance Layer

The resonance layer is continuous.

Its state is not restricted to the balanced ternary set:

`{-1, 0, 1}`

The resonance layer and balanced-ternary execution layer are distinct architectural layers.

Therefore:

`resonance state ≠ ternary state`

and:

`resonance descriptor ≠ ternary state`

---

## 3. Source State

A resonance descriptor is constructed from a declared resonance source state.

The current executable reference source type is:

`ResonanceState`

A model may define a higher-level source mapping into `ResonanceState`.

Such a mapping remains separate from descriptor construction.

---

## 4. Executable Resonance State

The executable reference resonance state contains:

- oscillator phases;
- oscillator frequencies.

It is represented by:

`ResonanceState`

with fields:

`phases`

and:

`frequencies`

Both vectors are nonempty.

Both vectors contain finite real values.

Both vectors have equal cardinality.

---

## 5. Oscillator Count

For a resonance state:

`x_R`

the oscillator count is:

`N = len(phases) = len(frequencies)`

The executable property is:

`oscillator_count`

The state is invalid when the phase and frequency vectors have different cardinalities.

---

## 6. Phase Domain

Each oscillator phase is represented as a finite real angle.

The executable state normalizes every phase to:

`[0, 2π)`

through phase wrapping.

The canonical executable operations are:

`wrap_phase`

and:

`wrap_phases`

Phase wrapping changes angular representation.

It does not change the represented point on the phase circle.

---

## 7. Oscillator Phase Is Not Physical Phase of Matter

Oscillator phase belongs to the dynamical resonance model.

It is not automatically:

- solid phase;
- liquid phase;
- gas phase;
- crystalline phase;
- thermodynamic phase;
- material phase label.

Therefore:

`oscillator phase ≠ physical phase of matter`

---

## 8. Frequency State

Each oscillator frequency is represented by one finite real value.

The executable reference does not impose one universal physical unit on the frequency vector.

Unit semantics belong to the concrete model contract.

---

## 9. Frequency Equality Is Not Resonance

Equal oscillator frequencies do not by themselves establish resonance.

Therefore:

`frequency equality ≠ resonance`

Resonance requires the declared resonance model, descriptor, relation, window, history, or other applicable model conditions.

---

## 10. Synchronization Is Not Resonance

Synchronization and resonance are distinct concepts.

Therefore:

`synchronization ≠ resonance`

A synchronized oscillator state may participate in a resonance model.

Synchronization alone does not establish the complete resonance classification.

---

## 11. Phase Locking Is Not Resonance

Phase locking is a dynamical relation.

It is not identical to resonance.

Therefore:

`phase locking ≠ resonance`

and:

`synchronization ≠ phase locking`

unless a concrete model explicitly establishes the applicable implication under declared assumptions.

---

## 12. Coherence Is Not Resonance

Coherence and resonance remain separate model concepts.

Therefore:

`coherence ≠ resonance`

A coherence observable may be used as one component of a resonance descriptor.

That use does not make the two concepts identical.

---

## 13. Coherence Is Not Uniformity

A coherent state is not defined as a uniformly identical state.

Therefore:

`coherence ≠ uniformity`

The framework does not replace structured collective organization with a generic equality condition.

---

## 14. Phase-Order Observable

For oscillator phases:

`θ_1, θ_2, ..., θ_N`

the executable phase-order observable is the magnitude of the mean complex phase vector.

Define:

`C = (1/N) Σ cos(θ_i)`

and:

`S = (1/N) Σ sin(θ_i)`

Then the phase-order value is:

`R = sqrt(C² + S²)`

The executable function is:

`phase_order_parameter`

For a complete `ResonanceState`, the executable function is:

`state_phase_order`

---

## 15. Phase-Order Range

For a nonempty finite phase vector:

`0 ≤ R ≤ 1`

within numerical arithmetic.

A value near:

`1`

indicates strong concentration of oscillator phases around a common angular direction.

A value near:

`0`

may arise from angular cancellation or broad phase distribution.

Neither endpoint alone defines complete resonance.

---

## 16. Phase Order Is Not Complete Coherence

The phase-order observable is one scalar collective descriptor.

It is not the complete coherence state of an arbitrary nonlinear system.

Therefore:

`phase order ≠ complete coherence`

A complete coherence model may require additional local, topological, temporal, or multiscale observables.

---

## 17. Phase Order Is Not Resonance

The scalar:

`R`

does not itself constitute a resonance classification.

Therefore:

`R ≠ resonance`

A resonance model may use `R` as one coordinate.

The classification still requires the declared resonance-space and resonance-window semantics.

---

## 18. Frequency Spread

The executable frequency-spread observable is the population standard deviation of oscillator frequencies.

For frequencies:

`ω_1, ω_2, ..., ω_N`

define the mean:

`ω_mean = (1/N) Σ ω_i`

Then:

`σ_ω = sqrt((1/N) Σ (ω_i - ω_mean)²)`

The executable function is:

`frequency_spread`

---

## 19. Frequency-Spread Range

The executable frequency spread satisfies:

`σ_ω ≥ 0`

A zero value means that all represented oscillator frequencies are equal.

This condition does not by itself establish resonance.

Therefore:

`σ_ω = 0 ≠ resonance`

---

## 20. Reference Resonance Descriptor

The current executable reference descriptor is:

`D_R = (R, σ_ω)`

where:

- `R` is phase order;
- `σ_ω` is population frequency spread.

It is represented by:

`ResonanceDescriptor`

with fields:

`phase_order`

and:

`frequency_spread`

---

## 21. Reference Descriptor Construction

The executable constructor is:

`resonance_descriptor(state)`

It maps:

`ResonanceState → ResonanceDescriptor`

The current executable mapping depends only on the supplied:

`ResonanceState`

No geometry, thermodynamic variable, ternary state, or validation result is silently inserted into this base descriptor.

---

## 22. Descriptor Coordinate

The executable descriptor exposes:

`as_coordinate()`

The resulting coordinate is:

`(phase_order, frequency_spread)`

The current executable reference therefore produces a two-dimensional resonance coordinate.

---

## 23. Two-Dimensional Reference Is a Specialization

The current executable descriptor has dimension:

`2`

This is an executable reference specialization.

The formal TR-EIF resonance theory does not assert that every resonance model is two-dimensional.

A concrete model may define a different descriptor dimension when its mapping and validation contract are explicit.

Therefore:

`current executable dimension = 2`

does not imply:

`all resonance spaces have dimension 2`

---

## 24. Resonance Coordinate

A resonance coordinate is an element:

`r ∈ X_R`

The executable type alias is:

`ResonanceCoordinate`

The current representation is a tuple of finite real values.

A coordinate must be nonempty.

Every coordinate component must be finite.

---

## 25. Resonance Space

The executable resonance space is represented by:

`ResonanceSpace`

It declares a positive integer:

`dimension`

A coordinate belongs to the declared executable space only when its cardinality equals the space dimension.

---

## 26. Resonance-Space Validation

The executable method:

`validate_coordinate`

requires:

- nonempty coordinate;
- finite coordinate components;
- exact dimension equality.

Dimension mismatch is invalid.

No implicit truncation or padding is performed.

---

## 27. Reference Coordinate Construction

The executable function:

`resonance_coordinate(state, space)`

performs:

`ResonanceState`

`→ ResonanceDescriptor`

`→ ResonanceCoordinate`

`→ ResonanceSpace validation`

It does not perform resonance-region classification.

---

## 28. Descriptor Construction Is Not Classification

The operation:

`resonance_descriptor(state)`

constructs a continuous descriptor.

It does not return:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`;
- `-1`;
- `0`;
- `1`.

Therefore:

`descriptor construction ≠ resonance classification`

and:

`descriptor construction ≠ ternary target generation`

---

## 29. Resonance Window

The executable reference resonance window is represented by:

`ResonanceWindow`

It contains:

- a `ResonanceSpace`;
- lower coordinate bounds;
- upper coordinate bounds.

The current executable window is finite and axis-aligned.

---

## 30. Window Bounds

For each coordinate axis:

`j`

the executable window requires:

`lower_j < upper_j`

Strict inequality is required for every axis.

A zero-width interval is invalid.

---

## 31. Closed Window Membership

The executable `contains` relation treats the window bounds as included.

A coordinate is contained when, for every axis:

`lower_j ≤ r_j ≤ upper_j`

This defines the executable closed-window membership rule.

---

## 32. Window Interior

A coordinate belongs to the executable window interior when, for every axis:

`lower_j < r_j < upper_j`

The executable method is:

`is_interior`

---

## 33. Window Boundary

A contained coordinate belongs to the executable window boundary when at least one coordinate component is exactly equal to its corresponding lower or upper bound.

The executable method is:

`is_boundary`

The current executable implementation uses exact numeric boundary equality.

No implicit tolerance is inserted.

---

## 34. Resonance Region

The executable resonance classification enum is:

`ResonanceRegion`

with values:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`.

The classifier is:

`classify_resonance_region`

---

## 35. Region Classification Order

The executable classifier applies the following order:

1. validate the coordinate against the resonance space;
2. test exact window boundary;
3. test window interior;
4. otherwise classify as outside.

This ordering preserves explicit boundary classification.

---

## 36. Region Is Not Ternary State

The set:

`{OUTSIDE, BOUNDARY, INSIDE}`

is a resonance-region classification.

It is not automatically the balanced ternary set:

`{-1, 0, 1}`

Therefore:

`OUTSIDE ≠ automatically -1`

`BOUNDARY ≠ automatically 0`

`INSIDE ≠ automatically 1`

Any mapping between these sets must be separately defined.

---

## 37. Boundary Is Not Active Neutral

A resonance-window boundary is a geometric classification in resonance space.

Active neutral `0` is a balanced-ternary execution state.

Therefore:

`resonance boundary ≠ active neutral`

and:

`neutral region ≠ resonance window classifier`

unless a concrete mapping explicitly defines such a relation.

---

## 38. Resonance Window Is Model-Relative

A resonance window belongs to a declared model.

A coordinate that is `INSIDE` one window may be `OUTSIDE` another.

Therefore resonance-window classification is not universal.

The window definition must remain explicit.

---

## 39. Resonance Window Is Finite in the Executable Reference

The current executable `ResonanceWindow` uses finite coordinate bounds.

Every lower and upper component must be finite through coordinate validation.

The current reference implementation does not represent an infinite window boundary.

---

## 40. Current Window Is Stateless

The current executable `ResonanceWindow` contains no history variable.

Therefore the base executable window classification is stateless for identical:

- coordinate;
- window bounds.

Formal resonance models may define history-dependent or hysteretic classification separately.

Such behavior must not be attributed to the current `ResonanceWindow` implementation unless an explicit higher-level state is supplied.

---

## 41. Hysteresis Is Separate

Hysteresis requires state or history beyond a stateless coordinate-window comparison.

Therefore:

`window classification ≠ hysteresis`

and:

`hysteresis ≠ neutral routing`

A hysteretic resonance classifier must declare its additional state explicitly.

---

## 42. Resonance-Window Crossing Is Not Bifurcation

A trajectory may cross:

`∂W_R`

without undergoing a dynamical bifurcation.

Therefore:

`resonance-window crossing ≠ bifurcation`

A bifurcation requires the corresponding dynamical-system conditions.

---

## 43. Bifurcation Is Not Ternary Transition

A dynamical bifurcation is not itself a balanced-ternary execution event.

Therefore:

`bifurcation ≠ ternary transition`

A model may map bifurcation-related observables to ternary targets through an explicit mapping.

The transition remains a separate execution-layer operation.

---

## 44. Descriptor and Ternary Target

A resonance descriptor may be an input to a continuous-to-ternary mapping.

The architectural chain is:

`ResonanceState`

`→ ResonanceDescriptor`

`→ resonance or decision classification`

`→ requested ternary target`

`→ ternary execution`

These stages remain semantically distinct.

---

## 45. Target Is Not Descriptor

A requested target belongs to:

`{-1, 0, 1}`

A resonance descriptor belongs to a continuous coordinate space.

Therefore:

`resonance descriptor ≠ ternary target`

and:

`continuous descriptor ≠ executed ternary state`

---

## 46. Target Is Not Executed State

Even after a resonance-derived target is produced:

`target ≠ executed state`

The ternary execution layer determines whether and how the requested target becomes committed.

Opposite-polarity execution remains subject to active-neutral mediation.

---

## 47. Active Neutral Is Not Descriptor Zero

A resonance coordinate component may numerically equal:

`0`

This numerical equality does not create active-neutral ternary semantics.

Therefore:

`continuous scalar 0 ≠ active neutral state 0`

unless an explicit mapping assigns that semantic meaning.

---

## 48. Missing Descriptor Is Not Active Neutral

A missing, invalid, NaN, unavailable, or failed resonance descriptor must not be represented by ternary state `0`.

Therefore:

`missing descriptor ≠ active neutral`

`invalid descriptor ≠ active neutral`

`NaN descriptor ≠ active neutral`

Such conditions remain outside the ternary state space.

---

## 49. Descriptor and Energy

A resonance descriptor is not energy.

Therefore:

`resonance descriptor ≠ energy`

A model may condition an energy model on resonance channels.

That conditioning is an explicit model operation.

It does not identify the descriptor with the energy output.

---

## 50. Descriptor and Force

A resonance descriptor is not mechanical force.

Therefore:

`resonance descriptor ≠ force`

A resonance-conditioned energy model may affect forces derived from the conditioned energy.

The force remains a distinct physical observable.

---

## 51. Phase Coupling Is Not Mechanical Force

Oscillator phase coupling is a dynamical coupling term.

It is not automatically a mechanical force.

Therefore:

`phase coupling ≠ mechanical force`

A mechanical force in the interatomic layer remains governed by the declared energy-gradient contract.

---

## 52. Phase Relation Is Not Chemical Bond

A relation between oscillator phases does not automatically define a chemical bond.

Therefore:

`phase relation ≠ chemical bond`

Graph connectivity, coordination, phase relation, and chemical bonding remain distinct concepts.

---

## 53. Geometry Boundary

The base executable `resonance_descriptor` receives only:

`ResonanceState`

It does not directly receive:

- atomic positions;
- interaction graph;
- cell;
- periodic axes;
- E(3) transformation.

Therefore geometry is not silently inserted into the base descriptor.

If geometry affects resonance state in a concrete model, that dependency belongs to an explicit upstream mapping.

---

## 54. E(3) Boundary

The current base descriptor components:

- phase order;
- frequency spread

are scalar quantities with no Cartesian vector indices.

However, E(3) invariance of a complete geometry-to-resonance pipeline depends on the declared source mapping that constructs the resonance state.

The descriptor specification does not assume an undeclared geometry-to-phase transformation.

---

## 55. Spatial Rotation Is Not Ternary Polarity Reversal

A spatial E(3) rotation acts on spatial representation.

Balanced ternary polarity belongs to a discrete execution state.

Therefore:

`spatial rotation ≠ ternary polarity reversal`

No spatial rotation automatically maps:

`-1 ↔ 1`

---

## 56. Thermodynamic Boundary

The base executable descriptor does not receive thermodynamic temperature or pressure.

Therefore:

`thermodynamic temperature ≠ oscillator frequency`

`thermodynamic temperature ≠ classifier temperature`

`pressure ≠ phase order`

unless a concrete model introduces an explicit mapping.

---

## 57. FLiBe Resonance Descriptor

The FLiBe specialization is represented by:

`FLiBeResonanceDescriptor`

It binds explicit context:

- `FLiBeConfiguration`;
- `FLiBeCoordinationState`;
- `FLiBeThermodynamicState`;
- `ResonanceState`;
- provenance;
- source metadata.

The base continuous descriptor is still computed from the supplied:

`ResonanceState`

through:

`resonance_descriptor`

---

## 58. FLiBe Context Does Not Silently Rewrite the Base Coordinate

In the current executable FLiBe descriptor:

- composition;
- graph-relative coordination;
- thermodynamic temperature;
- pressure

are retained as explicit context.

They are not silently folded into:

`(phase_order, frequency_spread)`

Therefore changing those context values does not by itself redefine the base descriptor unless the supplied `ResonanceState` also changes.

---

## 59. FLiBe Cardinality Contract

For a valid executable FLiBe resonance descriptor:

`configuration atom count = coordination atom count = resonance oscillator count`

Species ordering in the coordination state must match configuration species ordering.

The FLiBe composition contract must also remain valid.

---

## 60. Graph Coordination Is Not Experimental Coordination

The FLiBe coordination context may contain graph-relative coordination.

This is not automatically experimental or chemical coordination.

Therefore:

`graph coordination ≠ experimental coordination`

unless the mapping and validation procedure are explicitly defined.

---

## 61. Graph Coordination Is Not Chemical Bond

A graph-relative neighbor count is not automatically a chemical-bond count.

Therefore:

`graph coordination ≠ chemical bond`

The descriptor contract does not infer bonding from graph topology.

---

## 62. FLiBe Provenance

FLiBe resonance descriptor context retains:

`ParameterProvenance`

and optional source metadata.

`PRIMARY_SOURCE` provenance requires an explicit source identifier under the executable FLiBe contract.

Provenance describes evidence origin.

It does not change descriptor value semantics.

---

## 63. Resonance-Conditioned Features

A higher-level TR-EIP realization may append resonance descriptor components as explicit scalar channels.

In the current FLiBe TR-EIP reference realization, the declared resonance scalar channels are:

`phase_order`

and:

`frequency_spread`

These channels remain separate from ternary conditioning.

---

## 64. Resonance Conditioning Is Not Ternary Conditioning

Resonance conditioning uses continuous descriptor information.

Ternary conditioning uses retained balanced-ternary execution state.

Therefore:

`resonance conditioning ≠ ternary conditioning`

The two channels may interact within one interatomic model while retaining distinct semantic types.

---

## 65. Descriptor Evolution Boundary

Constructing a resonance descriptor does not evolve the resonance state.

The operation:

`resonance_descriptor(state)`

is observational.

It returns a descriptor from the supplied state.

It does not update phases or frequencies.

---

## 66. Dynamics Boundary

Resonance-state evolution is implemented separately through the resonance dynamics and integration layers.

The executable components include:

`phase_derivatives`

and:

`euler_step`

Therefore:

`descriptor construction ≠ resonance integration`

---

## 67. Deterministic Descriptor Construction

For identical valid:

`ResonanceState`

the current executable:

`resonance_descriptor`

must return the same descriptor within the declared numerical environment.

The function contains no hidden random state.

---

## 68. Deterministic Classification

For identical valid:

- resonance coordinate;
- resonance window;

the executable:

`classify_resonance_region`

returns the same `ResonanceRegion`.

The current base classifier contains no hidden history state.

---

## 69. Descriptor Validation

A descriptor-related validation suite must distinguish at least:

- source-state validity;
- phase wrapping;
- phase-order calculation;
- frequency-spread calculation;
- coordinate dimensionality;
- coordinate finiteness;
- window validity;
- boundary classification;
- interior classification;
- exterior classification;
- deterministic reconstruction;
- separation from ternary state.

---

## 70. Numerical Validation

Numerical validation of the phase-order observable must preserve its mathematical range.

Numerical validation of frequency spread must preserve nonnegativity.

A numerical tolerance used in testing does not alter the mathematical definition of the descriptor.

---

## 71. Boundary-Tolerance Policy

The current executable `ResonanceWindow.is_boundary` uses exact coordinate equality with a window bound.

A tolerance-based boundary layer is not silently present.

If a future numerical application requires a tolerance band, that behavior requires a separately declared classifier or numerical contract.

---

## 72. No Automatic Threshold Mapping

The base resonance descriptor specification does not define a universal threshold from descriptor coordinate to:

`-1/0/1`

A continuous-to-ternary mapping must explicitly declare:

- decision coordinate;
- thresholds or regions;
- hysteresis if used;
- history if used;
- provenance;
- target semantics.

---

## 73. No Universal Resonance Window

The executable framework does not define one universal:

`W_R`

for all systems.

A resonance window is model-relative.

Material-, scale-, topology-, or application-specific windows require their own definition and evidence.

---

## 74. No Frequency-Equality Shortcut

The descriptor contract must not be reduced to:

`frequencies equal → resonant`

or:

`frequencies unequal → nonresonant`

The current reference descriptor explicitly includes both phase order and frequency spread.

Even that two-component descriptor still requires a declared model/window for resonance classification.

---

## 75. No Synchronization Shortcut

The descriptor contract must not be reduced to:

`high phase order → resonance`

High phase order is one observable.

Resonance remains a model-level classification.

Therefore:

`high R ≠ automatically resonance`

---

## 76. No Ternary Shortcut

The descriptor contract must not be reduced to:

`OUTSIDE → -1`

`BOUNDARY → 0`

`INSIDE → 1`

without an explicit mapping.

Resonance-region classification and ternary target generation remain distinct operations.

---

## 77. No Physical-Phase Shortcut

The descriptor contract must not infer:

- melting;
- crystallization;
- physical phase transition;
- structural transition

from oscillator phase or resonance-window classification without an explicit physical model.

Therefore:

`resonance-window crossing ≠ physical phase transition`

and:

`structural transition ≠ physical phase transition`

---

## 78. Executable Reference Correspondence

The base executable resonance descriptor implementation is distributed across:

`src/tr_eif/resonance/state.py`

`src/tr_eif/resonance/order.py`

`src/tr_eif/resonance/descriptor.py`

`src/tr_eif/resonance/window.py`

`src/tr_eif/resonance/classification.py`

The principal executable interfaces are:

`ResonanceState`

`phase_order_parameter`

`state_phase_order`

`frequency_spread`

`ResonanceDescriptor`

`resonance_descriptor`

`resonance_coordinate`

`ResonanceSpace`

`ResonanceWindow`

`ResonanceRegion`

`classify_resonance_region`

---

## 79. FLiBe Executable Correspondence

The material-specific FLiBe descriptor implementation is:

`src/tr_eif/flibe/resonance_descriptor.py`

The principal interfaces are:

`FLiBeResonanceDescriptor`

and:

`build_flibe_resonance_descriptor`

The FLiBe wrapper preserves the base continuous descriptor while binding material-specific context explicitly.

---

## 80. Core Invariants

The resonance descriptor layer preserves the following invariants:

1. Resonance state is continuous.
2. Phase and frequency vectors are nonempty.
3. Phase and frequency vectors have equal cardinality.
4. Phases are represented in `[0, 2π)` after executable normalization.
5. Phase order is the magnitude of the mean complex phase vector.
6. Phase order is bounded by `0` and `1`.
7. Frequency spread is a population standard deviation.
8. Frequency spread is nonnegative.
9. Frequency equality is not resonance.
10. Synchronization is not resonance.
11. Phase locking is not resonance.
12. Coherence is not resonance.
13. Coherence is not uniformity.
14. Phase order is not complete coherence.
15. Descriptor construction is not classification.
16. Resonance-region classification is not ternary state.
17. `OUTSIDE/BOUNDARY/INSIDE` do not automatically map to `-1/0/1`.
18. Active neutral `0` is not continuous descriptor zero.
19. Missing or invalid descriptor data are not ternary `0`.
20. Resonance-window crossing is not bifurcation.
21. Bifurcation is not ternary transition.
22. Oscillator phase is not physical phase of matter.
23. Phase coupling is not mechanical force.
24. Phase relation is not chemical bond.
25. Spatial rotation is not ternary polarity reversal.
26. Thermodynamic temperature is not oscillator phase or frequency.
27. Base descriptor construction does not silently consume geometry or thermodynamic state.
28. Resonance conditioning and ternary conditioning remain separate channels.
29. Descriptor construction does not evolve resonance state.
30. Deterministic inputs produce deterministic descriptor outputs.

---

## 81. Non-Claims

The base resonance descriptor does not by itself establish:

- physical resonance of a material;
- chemical bonding;
- mechanical force;
- energy transfer magnitude;
- thermodynamic phase;
- phase transition;
- bifurcation;
- ternary target;
- ternary execution;
- synchronization regime;
- complete coherence;
- material transmutation.

Those claims require their corresponding explicit model and validation layers.

---

## 82. Summary

The TR-EIF resonance descriptor is a continuous typed representation.

The current executable reference uses:

`D_R = (phase_order, frequency_spread)`

as a two-dimensional specialization.

Descriptor construction, resonance-window classification, continuous-to-ternary target generation, and balanced-ternary execution remain separate operations.

The architectural chain is:

`continuous resonance state`

`→ continuous descriptor`

`→ resonance coordinate`

`→ model-relative classification`

`→ explicit target mapping`

`→ balanced-ternary execution`

No stage is collapsed into another by numerical similarity alone.# Resonance Descriptor Specification

## 1. Scope

This document defines the repository-level resonance descriptor specification of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The specification defines:

- continuous resonance state;
- oscillator phase and frequency state;
- phase-order observable;
- frequency-spread observable;
- executable reference descriptor;
- resonance coordinate;
- resonance space;
- resonance window;
- resonance-region classification;
- descriptor dimensionality;
- descriptor validation;
- source-state separation;
- geometry separation;
- thermodynamic-state separation;
- coherence separation;
- synchronization separation;
- balanced-ternary separation;
- continuous-to-ternary boundary;
- E(3) representation boundary;
- FLiBe specialization boundary;
- deterministic descriptor construction;
- executable reference correspondence.

The formal resonance theory is defined in:

`docs/volume_02_ternary_resonance_theory/`

The continuous-to-ternary mapping is defined in:

`docs/volume_02_ternary_resonance_theory/chapter_05_continuous_to_ternary_mapping.md`

Balanced ternary state semantics are defined in:

`docs/specifications/ternary_state_specification.md`

Neutral routing is defined in:

`docs/specifications/neutral_routing_specification.md`

---

## 2. Resonance Layer

The resonance layer is continuous.

Its state is not restricted to the balanced ternary set:

`{-1, 0, 1}`

The resonance layer and balanced-ternary execution layer are distinct architectural layers.

Therefore:

`resonance state ≠ ternary state`

and:

`resonance descriptor ≠ ternary state`

---

## 3. Source State

A resonance descriptor is constructed from a declared resonance source state.

The current executable reference source type is:

`ResonanceState`

A model may define a higher-level source mapping into `ResonanceState`.

Such a mapping remains separate from descriptor construction.

---

## 4. Executable Resonance State

The executable reference resonance state contains:

- oscillator phases;
- oscillator frequencies.

It is represented by:

`ResonanceState`

with fields:

`phases`

and:

`frequencies`

Both vectors are nonempty.

Both vectors contain finite real values.

Both vectors have equal cardinality.

---

## 5. Oscillator Count

For a resonance state:

`x_R`

the oscillator count is:

`N = len(phases) = len(frequencies)`

The executable property is:

`oscillator_count`

The state is invalid when the phase and frequency vectors have different cardinalities.

---

## 6. Phase Domain

Each oscillator phase is represented as a finite real angle.

The executable state normalizes every phase to:

`[0, 2π)`

through phase wrapping.

The canonical executable operations are:

`wrap_phase`

and:

`wrap_phases`

Phase wrapping changes angular representation.

It does not change the represented point on the phase circle.

---

## 7. Oscillator Phase Is Not Physical Phase of Matter

Oscillator phase belongs to the dynamical resonance model.

It is not automatically:

- solid phase;
- liquid phase;
- gas phase;
- crystalline phase;
- thermodynamic phase;
- material phase label.

Therefore:

`oscillator phase ≠ physical phase of matter`

---

## 8. Frequency State

Each oscillator frequency is represented by one finite real value.

The executable reference does not impose one universal physical unit on the frequency vector.

Unit semantics belong to the concrete model contract.

---

## 9. Frequency Equality Is Not Resonance

Equal oscillator frequencies do not by themselves establish resonance.

Therefore:

`frequency equality ≠ resonance`

Resonance requires the declared resonance model, descriptor, relation, window, history, or other applicable model conditions.

---

## 10. Synchronization Is Not Resonance

Synchronization and resonance are distinct concepts.

Therefore:

`synchronization ≠ resonance`

A synchronized oscillator state may participate in a resonance model.

Synchronization alone does not establish the complete resonance classification.

---

## 11. Phase Locking Is Not Resonance

Phase locking is a dynamical relation.

It is not identical to resonance.

Therefore:

`phase locking ≠ resonance`

and:

`synchronization ≠ phase locking`

unless a concrete model explicitly establishes the applicable implication under declared assumptions.

---

## 12. Coherence Is Not Resonance

Coherence and resonance remain separate model concepts.

Therefore:

`coherence ≠ resonance`

A coherence observable may be used as one component of a resonance descriptor.

That use does not make the two concepts identical.

---

## 13. Coherence Is Not Uniformity

A coherent state is not defined as a uniformly identical state.

Therefore:

`coherence ≠ uniformity`

The framework does not replace structured collective organization with a generic equality condition.

---

## 14. Phase-Order Observable

For oscillator phases:

`θ_1, θ_2, ..., θ_N`

the executable phase-order observable is the magnitude of the mean complex phase vector.

Define:

`C = (1/N) Σ cos(θ_i)`

and:

`S = (1/N) Σ sin(θ_i)`

Then the phase-order value is:

`R = sqrt(C² + S²)`

The executable function is:

`phase_order_parameter`

For a complete `ResonanceState`, the executable function is:

`state_phase_order`

---

## 15. Phase-Order Range

For a nonempty finite phase vector:

`0 ≤ R ≤ 1`

within numerical arithmetic.

A value near:

`1`

indicates strong concentration of oscillator phases around a common angular direction.

A value near:

`0`

may arise from angular cancellation or broad phase distribution.

Neither endpoint alone defines complete resonance.

---

## 16. Phase Order Is Not Complete Coherence

The phase-order observable is one scalar collective descriptor.

It is not the complete coherence state of an arbitrary nonlinear system.

Therefore:

`phase order ≠ complete coherence`

A complete coherence model may require additional local, topological, temporal, or multiscale observables.

---

## 17. Phase Order Is Not Resonance

The scalar:

`R`

does not itself constitute a resonance classification.

Therefore:

`R ≠ resonance`

A resonance model may use `R` as one coordinate.

The classification still requires the declared resonance-space and resonance-window semantics.

---

## 18. Frequency Spread

The executable frequency-spread observable is the population standard deviation of oscillator frequencies.

For frequencies:

`ω_1, ω_2, ..., ω_N`

define the mean:

`ω_mean = (1/N) Σ ω_i`

Then:

`σ_ω = sqrt((1/N) Σ (ω_i - ω_mean)²)`

The executable function is:

`frequency_spread`

---

## 19. Frequency-Spread Range

The executable frequency spread satisfies:

`σ_ω ≥ 0`

A zero value means that all represented oscillator frequencies are equal.

This condition does not by itself establish resonance.

Therefore:

`σ_ω = 0 ≠ resonance`

---

## 20. Reference Resonance Descriptor

The current executable reference descriptor is:

`D_R = (R, σ_ω)`

where:

- `R` is phase order;
- `σ_ω` is population frequency spread.

It is represented by:

`ResonanceDescriptor`

with fields:

`phase_order`

and:

`frequency_spread`

---

## 21. Reference Descriptor Construction

The executable constructor is:

`resonance_descriptor(state)`

It maps:

`ResonanceState → ResonanceDescriptor`

The current executable mapping depends only on the supplied:

`ResonanceState`

No geometry, thermodynamic variable, ternary state, or validation result is silently inserted into this base descriptor.

---

## 22. Descriptor Coordinate

The executable descriptor exposes:

`as_coordinate()`

The resulting coordinate is:

`(phase_order, frequency_spread)`

The current executable reference therefore produces a two-dimensional resonance coordinate.

---

## 23. Two-Dimensional Reference Is a Specialization

The current executable descriptor has dimension:

`2`

This is an executable reference specialization.

The formal TR-EIF resonance theory does not assert that every resonance model is two-dimensional.

A concrete model may define a different descriptor dimension when its mapping and validation contract are explicit.

Therefore:

`current executable dimension = 2`

does not imply:

`all resonance spaces have dimension 2`

---

## 24. Resonance Coordinate

A resonance coordinate is an element:

`r ∈ X_R`

The executable type alias is:

`ResonanceCoordinate`

The current representation is a tuple of finite real values.

A coordinate must be nonempty.

Every coordinate component must be finite.

---

## 25. Resonance Space

The executable resonance space is represented by:

`ResonanceSpace`

It declares a positive integer:

`dimension`

A coordinate belongs to the declared executable space only when its cardinality equals the space dimension.

---

## 26. Resonance-Space Validation

The executable method:

`validate_coordinate`

requires:

- nonempty coordinate;
- finite coordinate components;
- exact dimension equality.

Dimension mismatch is invalid.

No implicit truncation or padding is performed.

---

## 27. Reference Coordinate Construction

The executable function:

`resonance_coordinate(state, space)`

performs:

`ResonanceState`

`→ ResonanceDescriptor`

`→ ResonanceCoordinate`

`→ ResonanceSpace validation`

It does not perform resonance-region classification.

---

## 28. Descriptor Construction Is Not Classification

The operation:

`resonance_descriptor(state)`

constructs a continuous descriptor.

It does not return:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`;
- `-1`;
- `0`;
- `1`.

Therefore:

`descriptor construction ≠ resonance classification`

and:

`descriptor construction ≠ ternary target generation`

---

## 29. Resonance Window

The executable reference resonance window is represented by:

`ResonanceWindow`

It contains:

- a `ResonanceSpace`;
- lower coordinate bounds;
- upper coordinate bounds.

The current executable window is finite and axis-aligned.

---

## 30. Window Bounds

For each coordinate axis:

`j`

the executable window requires:

`lower_j < upper_j`

Strict inequality is required for every axis.

A zero-width interval is invalid.

---

## 31. Closed Window Membership

The executable `contains` relation treats the window bounds as included.

A coordinate is contained when, for every axis:

`lower_j ≤ r_j ≤ upper_j`

This defines the executable closed-window membership rule.

---

## 32. Window Interior

A coordinate belongs to the executable window interior when, for every axis:

`lower_j < r_j < upper_j`

The executable method is:

`is_interior`

---

## 33. Window Boundary

A contained coordinate belongs to the executable window boundary when at least one coordinate component is exactly equal to its corresponding lower or upper bound.

The executable method is:

`is_boundary`

The current executable implementation uses exact numeric boundary equality.

No implicit tolerance is inserted.

---

## 34. Resonance Region

The executable resonance classification enum is:

`ResonanceRegion`

with values:

- `OUTSIDE`;
- `BOUNDARY`;
- `INSIDE`.

The classifier is:

`classify_resonance_region`

---

## 35. Region Classification Order

The executable classifier applies the following order:

1. validate the coordinate against the resonance space;
2. test exact window boundary;
3. test window interior;
4. otherwise classify as outside.

This ordering preserves explicit boundary classification.

---

## 36. Region Is Not Ternary State

The set:

`{OUTSIDE, BOUNDARY, INSIDE}`

is a resonance-region classification.

It is not automatically the balanced ternary set:

`{-1, 0, 1}`

Therefore:

`OUTSIDE ≠ automatically -1`

`BOUNDARY ≠ automatically 0`

`INSIDE ≠ automatically 1`

Any mapping between these sets must be separately defined.

---

## 37. Boundary Is Not Active Neutral

A resonance-window boundary is a geometric classification in resonance space.

Active neutral `0` is a balanced-ternary execution state.

Therefore:

`resonance boundary ≠ active neutral`

and:

`neutral region ≠ resonance window classifier`

unless a concrete mapping explicitly defines such a relation.

---

## 38. Resonance Window Is Model-Relative

A resonance window belongs to a declared model.

A coordinate that is `INSIDE` one window may be `OUTSIDE` another.

Therefore resonance-window classification is not universal.

The window definition must remain explicit.

---

## 39. Resonance Window Is Finite in the Executable Reference

The current executable `ResonanceWindow` uses finite coordinate bounds.

Every lower and upper component must be finite through coordinate validation.

The current reference implementation does not represent an infinite window boundary.

---

## 40. Current Window Is Stateless

The current executable `ResonanceWindow` contains no history variable.

Therefore the base executable window classification is stateless for identical:

- coordinate;
- window bounds.

Formal resonance models may define history-dependent or hysteretic classification separately.

Such behavior must not be attributed to the current `ResonanceWindow` implementation unless an explicit higher-level state is supplied.

---

## 41. Hysteresis Is Separate

Hysteresis requires state or history beyond a stateless coordinate-window comparison.

Therefore:

`window classification ≠ hysteresis`

and:

`hysteresis ≠ neutral routing`

A hysteretic resonance classifier must declare its additional state explicitly.

---

## 42. Resonance-Window Crossing Is Not Bifurcation

A trajectory may cross:

`∂W_R`

without undergoing a dynamical bifurcation.

Therefore:

`resonance-window crossing ≠ bifurcation`

A bifurcation requires the corresponding dynamical-system conditions.

---

## 43. Bifurcation Is Not Ternary Transition

A dynamical bifurcation is not itself a balanced-ternary execution event.

Therefore:

`bifurcation ≠ ternary transition`

A model may map bifurcation-related observables to ternary targets through an explicit mapping.

The transition remains a separate execution-layer operation.

---

## 44. Descriptor and Ternary Target

A resonance descriptor may be an input to a continuous-to-ternary mapping.

The architectural chain is:

`ResonanceState`

`→ ResonanceDescriptor`

`→ resonance or decision classification`

`→ requested ternary target`

`→ ternary execution`

These stages remain semantically distinct.

---

## 45. Target Is Not Descriptor

A requested target belongs to:

`{-1, 0, 1}`

A resonance descriptor belongs to a continuous coordinate space.

Therefore:

`resonance descriptor ≠ ternary target`

and:

`continuous descriptor ≠ executed ternary state`

---

## 46. Target Is Not Executed State

Even after a resonance-derived target is produced:

`target ≠ executed state`

The ternary execution layer determines whether and how the requested target becomes committed.

Opposite-polarity execution remains subject to active-neutral mediation.

---

## 47. Active Neutral Is Not Descriptor Zero

A resonance coordinate component may numerically equal:

`0`

This numerical equality does not create active-neutral ternary semantics.

Therefore:

`continuous scalar 0 ≠ active neutral state 0`

unless an explicit mapping assigns that semantic meaning.

---

## 48. Missing Descriptor Is Not Active Neutral

A missing, invalid, NaN, unavailable, or failed resonance descriptor must not be represented by ternary state `0`.

Therefore:

`missing descriptor ≠ active neutral`

`invalid descriptor ≠ active neutral`

`NaN descriptor ≠ active neutral`

Such conditions remain outside the ternary state space.

---

## 49. Descriptor and Energy

A resonance descriptor is not energy.

Therefore:

`resonance descriptor ≠ energy`

A model may condition an energy model on resonance channels.

That conditioning is an explicit model operation.

It does not identify the descriptor with the energy output.

---

## 50. Descriptor and Force

A resonance descriptor is not mechanical force.

Therefore:

`resonance descriptor ≠ force`

A resonance-conditioned energy model may affect forces derived from the conditioned energy.

The force remains a distinct physical observable.

---

## 51. Phase Coupling Is Not Mechanical Force

Oscillator phase coupling is a dynamical coupling term.

It is not automatically a mechanical force.

Therefore:

`phase coupling ≠ mechanical force`

A mechanical force in the interatomic layer remains governed by the declared energy-gradient contract.

---

## 52. Phase Relation Is Not Chemical Bond

A relation between oscillator phases does not automatically define a chemical bond.

Therefore:

`phase relation ≠ chemical bond`

Graph connectivity, coordination, phase relation, and chemical bonding remain distinct concepts.

---

## 53. Geometry Boundary

The base executable `resonance_descriptor` receives only:

`ResonanceState`

It does not directly receive:

- atomic positions;
- interaction graph;
- cell;
- periodic axes;
- E(3) transformation.

Therefore geometry is not silently inserted into the base descriptor.

If geometry affects resonance state in a concrete model, that dependency belongs to an explicit upstream mapping.

---

## 54. E(3) Boundary

The current base descriptor components:

- phase order;
- frequency spread

are scalar quantities with no Cartesian vector indices.

However, E(3) invariance of a complete geometry-to-resonance pipeline depends on the declared source mapping that constructs the resonance state.

The descriptor specification does not assume an undeclared geometry-to-phase transformation.

---

## 55. Spatial Rotation Is Not Ternary Polarity Reversal

A spatial E(3) rotation acts on spatial representation.

Balanced ternary polarity belongs to a discrete execution state.

Therefore:

`spatial rotation ≠ ternary polarity reversal`

No spatial rotation automatically maps:

`-1 ↔ 1`

---

## 56. Thermodynamic Boundary

The base executable descriptor does not receive thermodynamic temperature or pressure.

Therefore:

`thermodynamic temperature ≠ oscillator frequency`

`thermodynamic temperature ≠ classifier temperature`

`pressure ≠ phase order`

unless a concrete model introduces an explicit mapping.

---

## 57. FLiBe Resonance Descriptor

The FLiBe specialization is represented by:

`FLiBeResonanceDescriptor`

It binds explicit context:

- `FLiBeConfiguration`;
- `FLiBeCoordinationState`;
- `FLiBeThermodynamicState`;
- `ResonanceState`;
- provenance;
- source metadata.

The base continuous descriptor is still computed from the supplied:

`ResonanceState`

through:

`resonance_descriptor`

---

## 58. FLiBe Context Does Not Silently Rewrite the Base Coordinate

In the current executable FLiBe descriptor:

- composition;
- graph-relative coordination;
- thermodynamic temperature;
- pressure

are retained as explicit context.

They are not silently folded into:

`(phase_order, frequency_spread)`

Therefore changing those context values does not by itself redefine the base descriptor unless the supplied `ResonanceState` also changes.

---

## 59. FLiBe Cardinality Contract

For a valid executable FLiBe resonance descriptor:

`configuration atom count = coordination atom count = resonance oscillator count`

Species ordering in the coordination state must match configuration species ordering.

The FLiBe composition contract must also remain valid.

---

## 60. Graph Coordination Is Not Experimental Coordination

The FLiBe coordination context may contain graph-relative coordination.

This is not automatically experimental or chemical coordination.

Therefore:

`graph coordination ≠ experimental coordination`

unless the mapping and validation procedure are explicitly defined.

---

## 61. Graph Coordination Is Not Chemical Bond

A graph-relative neighbor count is not automatically a chemical-bond count.

Therefore:

`graph coordination ≠ chemical bond`

The descriptor contract does not infer bonding from graph topology.

---

## 62. FLiBe Provenance

FLiBe resonance descriptor context retains:

`ParameterProvenance`

and optional source metadata.

`PRIMARY_SOURCE` provenance requires an explicit source identifier under the executable FLiBe contract.

Provenance describes evidence origin.

It does not change descriptor value semantics.

---

## 63. Resonance-Conditioned Features

A higher-level TR-EIP realization may append resonance descriptor components as explicit scalar channels.

In the current FLiBe TR-EIP reference realization, the declared resonance scalar channels are:

`phase_order`

and:

`frequency_spread`

These channels remain separate from ternary conditioning.

---

## 64. Resonance Conditioning Is Not Ternary Conditioning

Resonance conditioning uses continuous descriptor information.

Ternary conditioning uses retained balanced-ternary execution state.

Therefore:

`resonance conditioning ≠ ternary conditioning`

The two channels may interact within one interatomic model while retaining distinct semantic types.

---

## 65. Descriptor Evolution Boundary

Constructing a resonance descriptor does not evolve the resonance state.

The operation:

`resonance_descriptor(state)`

is observational.

It returns a descriptor from the supplied state.

It does not update phases or frequencies.

---

## 66. Dynamics Boundary

Resonance-state evolution is implemented separately through the resonance dynamics and integration layers.

The executable components include:

`phase_derivatives`

and:

`euler_step`

Therefore:

`descriptor construction ≠ resonance integration`

---

## 67. Deterministic Descriptor Construction

For identical valid:

`ResonanceState`

the current executable:

`resonance_descriptor`

must return the same descriptor within the declared numerical environment.

The function contains no hidden random state.

---

## 68. Deterministic Classification

For identical valid:

- resonance coordinate;
- resonance window;

the executable:

`classify_resonance_region`

returns the same `ResonanceRegion`.

The current base classifier contains no hidden history state.

---

## 69. Descriptor Validation

A descriptor-related validation suite must distinguish at least:

- source-state validity;
- phase wrapping;
- phase-order calculation;
- frequency-spread calculation;
- coordinate dimensionality;
- coordinate finiteness;
- window validity;
- boundary classification;
- interior classification;
- exterior classification;
- deterministic reconstruction;
- separation from ternary state.

---

## 70. Numerical Validation

Numerical validation of the phase-order observable must preserve its mathematical range.

Numerical validation of frequency spread must preserve nonnegativity.

A numerical tolerance used in testing does not alter the mathematical definition of the descriptor.

---

## 71. Boundary-Tolerance Policy

The current executable `ResonanceWindow.is_boundary` uses exact coordinate equality with a window bound.

A tolerance-based boundary layer is not silently present.

If a future numerical application requires a tolerance band, that behavior requires a separately declared classifier or numerical contract.

---

## 72. No Automatic Threshold Mapping

The base resonance descriptor specification does not define a universal threshold from descriptor coordinate to:

`-1/0/1`

A continuous-to-ternary mapping must explicitly declare:

- decision coordinate;
- thresholds or regions;
- hysteresis if used;
- history if used;
- provenance;
- target semantics.

---

## 73. No Universal Resonance Window

The executable framework does not define one universal:

`W_R`

for all systems.

A resonance window is model-relative.

Material-, scale-, topology-, or application-specific windows require their own definition and evidence.

---

## 74. No Frequency-Equality Shortcut

The descriptor contract must not be reduced to:

`frequencies equal → resonant`

or:

`frequencies unequal → nonresonant`

The current reference descriptor explicitly includes both phase order and frequency spread.

Even that two-component descriptor still requires a declared model/window for resonance classification.

---

## 75. No Synchronization Shortcut

The descriptor contract must not be reduced to:

`high phase order → resonance`

High phase order is one observable.

Resonance remains a model-level classification.

Therefore:

`high R ≠ automatically resonance`

---

## 76. No Ternary Shortcut

The descriptor contract must not be reduced to:

`OUTSIDE → -1`

`BOUNDARY → 0`

`INSIDE → 1`

without an explicit mapping.

Resonance-region classification and ternary target generation remain distinct operations.

---

## 77. No Physical-Phase Shortcut

The descriptor contract must not infer:

- melting;
- crystallization;
- physical phase transition;
- structural transition

from oscillator phase or resonance-window classification without an explicit physical model.

Therefore:

`resonance-window crossing ≠ physical phase transition`

and:

`structural transition ≠ physical phase transition`

---

## 78. Executable Reference Correspondence

The base executable resonance descriptor implementation is distributed across:

`src/tr_eif/resonance/state.py`

`src/tr_eif/resonance/order.py`

`src/tr_eif/resonance/descriptor.py`

`src/tr_eif/resonance/window.py`

`src/tr_eif/resonance/classification.py`

The principal executable interfaces are:

`ResonanceState`

`phase_order_parameter`

`state_phase_order`

`frequency_spread`

`ResonanceDescriptor`

`resonance_descriptor`

`resonance_coordinate`

`ResonanceSpace`

`ResonanceWindow`

`ResonanceRegion`

`classify_resonance_region`

---

## 79. FLiBe Executable Correspondence

The material-specific FLiBe descriptor implementation is:

`src/tr_eif/flibe/resonance_descriptor.py`

The principal interfaces are:

`FLiBeResonanceDescriptor`

and:

`build_flibe_resonance_descriptor`

The FLiBe wrapper preserves the base continuous descriptor while binding material-specific context explicitly.

---

## 80. Core Invariants

The resonance descriptor layer preserves the following invariants:

1. Resonance state is continuous.
2. Phase and frequency vectors are nonempty.
3. Phase and frequency vectors have equal cardinality.
4. Phases are represented in `[0, 2π)` after executable normalization.
5. Phase order is the magnitude of the mean complex phase vector.
6. Phase order is bounded by `0` and `1`.
7. Frequency spread is a population standard deviation.
8. Frequency spread is nonnegative.
9. Frequency equality is not resonance.
10. Synchronization is not resonance.
11. Phase locking is not resonance.
12. Coherence is not resonance.
13. Coherence is not uniformity.
14. Phase order is not complete coherence.
15. Descriptor construction is not classification.
16. Resonance-region classification is not ternary state.
17. `OUTSIDE/BOUNDARY/INSIDE` do not automatically map to `-1/0/1`.
18. Active neutral `0` is not continuous descriptor zero.
19. Missing or invalid descriptor data are not ternary `0`.
20. Resonance-window crossing is not bifurcation.
21. Bifurcation is not ternary transition.
22. Oscillator phase is not physical phase of matter.
23. Phase coupling is not mechanical force.
24. Phase relation is not chemical bond.
25. Spatial rotation is not ternary polarity reversal.
26. Thermodynamic temperature is not oscillator phase or frequency.
27. Base descriptor construction does not silently consume geometry or thermodynamic state.
28. Resonance conditioning and ternary conditioning remain separate channels.
29. Descriptor construction does not evolve resonance state.
30. Deterministic inputs produce deterministic descriptor outputs.

---

## 81. Non-Claims

The base resonance descriptor does not by itself establish:

- physical resonance of a material;
- chemical bonding;
- mechanical force;
- energy transfer magnitude;
- thermodynamic phase;
- phase transition;
- bifurcation;
- ternary target;
- ternary execution;
- synchronization regime;
- complete coherence;
- material transmutation.

Those claims require their corresponding explicit model and validation layers.

---

## 82. Summary

The TR-EIF resonance descriptor is a continuous typed representation.

The current executable reference uses:

`D_R = (phase_order, frequency_spread)`

as a two-dimensional specialization.

Descriptor construction, resonance-window classification, continuous-to-ternary target generation, and balanced-ternary execution remain separate operations.

The architectural chain is:

`continuous resonance state`

`→ continuous descriptor`

`→ resonance coordinate`

`→ model-relative classification`

`→ explicit target mapping`

`→ balanced-ternary execution`

No stage is collapsed into another by numerical similarity alone.
