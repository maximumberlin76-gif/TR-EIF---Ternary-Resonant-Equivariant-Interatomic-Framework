# Notation and Definitions

## 1. Purpose

This chapter defines the canonical notation used throughout the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The purpose of the notation layer is to ensure that:

- each symbol has one declared semantic role within its scope;
- domains and codomains are explicit;
- continuous and discrete variables remain distinguishable;
- state and observable variables remain distinguishable;
- local and global quantities remain distinguishable;
- geometric, resonance, ternary, energetic, numerical, and validation quantities remain separately typed;
- transformation behavior is explicit;
- history and memory are represented when required;
- implementation-specific notation does not silently redefine formal notation.

Unless a later chapter explicitly introduces a more specialized local convention, the notation defined here is authoritative.

---

## 2. General Symbol Convention

Uppercase Roman symbols generally denote:

- sets;
- spaces;
- mappings;
- graphs;
- structured mathematical objects.

Lowercase Roman symbols generally denote:

- elements of spaces;
- scalar variables;
- indices;
- parameters.

Greek symbols are used where established mathematical convention or model structure makes them appropriate.

Boldface notation is not required by the repository notation system.

Vector and tensor meaning is determined by the declared mathematical type rather than typography alone.

---

## 3. Set Membership

For a set:

`X`

and element:

`x`,

membership is written:

`x ∈ X`.

Non-membership is written:

`x ∉ X`.

A subset relation is written:

`A ⊆ B`.

A strict subset relation is written:

`A ⊂ B`.

---

## 4. Standard Number Sets

The following standard sets are used:

`N`

for positive integers where explicitly stated;

`N_0 = {0, 1, 2, ...}`

for nonnegative integers;

`Z`

for integers;

`R`

for real numbers;

`R^n`

for the `n`-dimensional real vector space;

`C`

for complex numbers.

Whenever zero-indexed discrete coordinates are required, `N_0` is preferred over an ambiguous use of `N`.

---

## 5. Cartesian Product

For spaces:

`X_1, X_2, ..., X_n`,

their Cartesian product is:

`X_1 × X_2 × ... × X_n`.

An element of the product is written:

`x = (x_1, x_2, ..., x_n)`.

The product structure does not imply that all component spaces have the same mathematical type.

---

## 6. Function Notation

A mapping from domain `X` to codomain `Y` is written:

`F: X → Y`.

For:

`x ∈ X`,

the mapped value is:

`F(x) ∈ Y`.

The domain and codomain are part of the definition of `F`.

A symbol for a mapping must not be used before its domain and codomain are established.

---

## 7. Composition

For:

`F: X → Y`

and:

`G: Y → Z`,

the composition is:

`G ∘ F: X → Z`

with:

`(G ∘ F)(x) = G(F(x))`.

Composition is valid only when the codomain of `F` is compatible with the domain of `G`.

---

## 8. Identity Mapping

The identity mapping on `X` is:

`Id_X: X → X`

defined by:

`Id_X(x) = x`.

---

## 9. Indexed Families

For an indexed family:

`{x_i}_{i=1}^N`

the index:

`i ∈ {1, ..., N}`

identifies one member of the family.

An index is not automatically a persistent semantic identity.

Where persistent identity is required, a separate identity variable or identifier space is defined.

---

## 10. State Space

The complete state space of a selected system is denoted:

`X`.

A state is:

`x ∈ X`.

When the state is decomposed:

`X = X_1 × ... × X_m`

the state may be written:

`x = (x_1, ..., x_m)`.

Each component has its own declared type.

---

## 11. Continuous State Space

A continuous state space is generally denoted:

`X_c`.

For a finite-dimensional Euclidean state:

`X_c ⊆ R^n`.

A continuous state is:

`x_c ∈ X_c`.

---

## 12. Discrete State Space

A discrete state space is generally denoted:

`X_d`.

A discrete state is:

`x_d ∈ X_d`.

A discrete state is not treated as continuous unless an explicit embedding is defined.

---

## 13. Balanced Ternary State Space

The balanced ternary state space is:

`T = {-1, 0, 1}`.

The canonical kernel notation is:

`-1/0/1`.

The state:

`0`

is active.

The notation:

`-1/0/1`

is not used.

---

## 14. Executed Ternary State

The executed retained ternary state is denoted:

`t_exec ∈ T`.

Where indexed by execution coordinate:

`t_exec[k] ∈ T`.

This is the state that has actually passed the applicable transition and commit semantics.

---

## 15. Ternary Target

A ternary target is denoted:

`t_target ∈ T`.

Where indexed:

`t_target[k] ∈ T`.

A target represents a requested or computed destination.

It is distinct from:

`t_exec`.

In general:

`t_target ≠ t_exec`

may hold.

---

## 16. Pending Destination

A pending ternary destination is denoted:

`t_pending`.

Where the model uses pending routing, the valid pending destination is defined by the applicable transition mechanism.

The absence of a pending destination is represented separately from active ternary `0`.

---

## 17. Ternary Transition Relation

The ternary transition relation is denoted:

`R_T ⊆ T × T`.

The direct opposite transitions:

`(-1, 1)`

and:

`(1, -1)`

are excluded from the committed transition relation.

The admissible opposite-polarity paths are:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

Each arrow is a separate transition event.

---

## 18. Execution Coordinate

The logical execution coordinate is denoted:

`k ∈ N_0`.

The sequence:

`x[k]`

denotes state indexed by execution step.

The execution coordinate is distinct from model time unless an explicit mapping is defined.

---

## 19. Model Time

Continuous model time is denoted:

`t ∈ I_t`

where:

`I_t ⊆ R`

is the declared temporal domain.

The symbol `t` is reserved for continuous or physical model time within a scope where no ambiguity exists.

It must not simultaneously denote a ternary state.

---

## 20. Numerical Step Index

A numerical step index is denoted:

`n ∈ N_0`.

The numerical state may be written:

`x_n`

or:

`x[n]`

when the meaning is unambiguous.

The notation must preserve the distinction:

`numerical step ≠ execution step ≠ model time`.

---

## 21. Time Step

A numerical time step is denoted:

`Delta t`

with:

`Delta t > 0`.

For variable-step integration, the local step may be written:

`Delta t_n`.

Time-step dimensions must be compatible with the model-time convention.

---

## 22. Circular Phase Space

The oscillator phase space is:

`S^1 = R / (2 pi Z)`.

A phase is denoted:

`theta ∈ S^1`.

For indexed oscillators:

`theta_i ∈ S^1`.

A computational representative may be stored in a canonical interval, but the mathematical phase remains circular.

---

## 23. Phase Vector

For `N` oscillators:

`Theta = (theta_1, ..., theta_N) ∈ (S^1)^N`.

The uppercase symbol:

`Theta`

denotes the full phase state when required.

---

## 24. Natural Frequency

A natural or intrinsic angular-frequency variable is denoted:

`omega_i`.

Its units must be declared by the selected model.

The symbol:

`omega`

must not simultaneously denote a generic scalar unrelated to frequency within the same scope.

---

## 25. Phase Lag

A phase-lag parameter is denoted:

`gamma`

or, where local:

`gamma_i`.

A phase lag is a circular or angular interaction parameter.

It is distinct from temporal delay.

---

## 26. Temporal Delay

A temporal delay is denoted:

`tau`

or:

`tau_ij`

where pair-dependent.

A delayed state may be written:

`x_j(t - tau_ij)`.

The notation preserves:

`tau ≠ gamma`.

---

## 27. Coupling Strength

A coupling parameter may be denoted:

`K`

when no conflict with another local definition exists.

For structured coupling:

`K_ij`

may denote a coupling coefficient between indexed components.

The physical interpretation and units of `K` must be defined by the selected model.

---

## 28. Kuramoto Phase Order

For phases:

`theta_1, ..., theta_N`,

the complex order parameter is:

`Z = (1/N) sum_j exp(i theta_j)`.

Its magnitude is:

`R = |Z|`.

The scalar:

`R ∈ [0, 1]`

is the phase-order magnitude for this definition.

---

## 29. Coherence Observable

A broader coherence observable is denoted:

`C`

or:

`C(t)`

when time-dependent.

It must be defined independently.

The notation permanently preserves:

`R(t) ≠ C(t)`.

---

## 30. Resonance Coordinate Space

The resonance-coordinate space is denoted:

`X_R`.

A resonance state is:

`r ∈ X_R`.

The dimensionality and coordinate structure of `X_R` are model-dependent.

---

## 31. Resonance Projection

The mapping into resonance-coordinate space is denoted:

`P_R`.

Its general typed form is:

`P_R: X_src → X_R`.

For:

`x ∈ X_src`,

the resonance state is:

`r = P_R(x)`.

---

## 32. Resonance Window

A resonance window is denoted:

`W_R`

with:

`W_R ⊂ X_R`.

Its boundary is:

`∂W_R`.

The window may depend on additional state or parameters when explicitly defined.

---

## 33. Resonance Classification

The minimal resonance classification set is:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

A classifier may be written:

`C_R: X_R → K_R`.

The resonance classifier:

`C_R`

must not be confused with a coherence observable:

`C`.

Where both occur in one local scope, the notation must be qualified to prevent ambiguity.

---

## 34. Resonance Classification and Ternary State

The notation preserves:

`K_R ≠ T`.

Therefore:

`OUTSIDE ≠ -1`

`BOUNDARY ≠ 0`

`INSIDE ≠ 1`

unless a separate mapping is explicitly defined.

---

## 35. Resonance-to-Ternary Mapping

A resonance-to-ternary target mapping may be denoted:

`P_RT`.

Its simplest form is:

`P_RT: X_R → T`.

For history-dependent mapping:

`P_RT: X_R × X_H → T`.

The output is a ternary target unless explicitly stated otherwise.

---

## 36. History Space

A history state space is denoted:

`X_H`.

A history state is:

`h ∈ X_H`.

History state contains information from prior model or execution coordinates required for future evolution.

---

## 37. Memory State

A memory state space is denoted:

`X_M`.

A memory variable is:

`m ∈ X_M`.

History and memory may overlap in a particular realization, but the relation must be explicitly defined.

---

## 38. Input Space

The external input space is denoted:

`U`.

An input is:

`u ∈ U`.

For time-dependent input:

`u(t)`.

For discrete execution:

`u[k]`.

---

## 39. Parameter Space

The parameter space is denoted:

`P`.

A parameter is:

`p ∈ P`.

Dynamic parameters that evolve during execution become part of state rather than remaining static parameters.

---

## 40. Observable Space

An observable space is denoted:

`Y`.

An observation mapping is:

`O: X → Y`.

The observable is:

`y = O(x)`.

---

## 41. Local State

A local state associated with entity `i` is written:

`x_i ∈ X_i`.

Where all local states share one type:

`x_i ∈ X_loc`.

---

## 42. Global State

The global state is denoted:

`x_G`

or simply:

`x`

when unambiguous.

A global state is not defined as the arithmetic average of local states unless an explicit aggregation mapping establishes that relation.

---

## 43. Local Observable

A local observable may be written:

`O_i: X_i → Y_i`.

Its value is:

`y_i = O_i(x_i)`.

---

## 44. Global Observable

A global observable is written:

`O_G: X → Y_G`.

Its value is:

`y_G = O_G(x)`.

Local and global observables remain separately typed.

---

## 45. Scale Set

The modeled scale set is denoted:

`L`.

A scale label is:

`ell ∈ L`.

The symbol:

`ell`

denotes scale identity rather than a numerical length unless explicitly defined otherwise.

---

## 46. Scale-Indexed State

A state at scale `ell` is written:

`x^(ell) ∈ X^(ell)`.

A cross-scale mapping is:

`M_(ell_a→ell_b): X^(ell_a) → X^(ell_b)`.

---

## 47. Atomic Entity Count

The number of modeled atomic entities is denoted:

`N`.

The interpretation of `N` must be clear from context.

If `N` is already used for another indexed population in the same scope, a more specific symbol must be introduced.

---

## 48. Species Space

The atomic species-label space is denoted:

`A_sp`.

For atom `i`:

`a_i ∈ A_sp`.

The symbol `A_sp` distinguishes species space from general artifact or action notation.

---

## 49. Atomic Position

The Cartesian position of entity `i` is:

`r_i ∈ R^3`.

The complete position state is:

`R_pos = (r_1, ..., r_N) ∈ R^(3N)`.

The symbol `R_pos` is distinct from phase-order magnitude `R`.

---

## 50. Velocity

The velocity of entity `i` is:

`v_i ∈ R^3`.

The complete velocity state is:

`V = (v_1, ..., v_N)`.

Velocity carries physical dimensions of length divided by time.

---

## 51. Momentum

Momentum of entity `i` is denoted:

`p_i`.

When momentum and parameter symbol `p` occur in the same scope, the notation must be qualified to avoid ambiguity.

A complete momentum state may be written:

`P_mom`.

---

## 52. Force

Force on entity `i` is:

`F_i ∈ R^3`.

The complete force collection is:

`F = (F_1, ..., F_N)`.

Where `F` is already used for a generic mapping, the local scope must use a more explicit notation such as:

`F_force`.

---

## 53. Energy

A scalar energy functional is denoted:

`E`.

Its typed form is:

`E: X_E → R`

for its declared energy-domain state space `X_E`.

Energy must not be conflated with ternary state or resonance classification.

---

## 54. Stress

Stress is denoted:

`sigma`.

For three-dimensional Cartesian representation:

`sigma ∈ R^(3×3)`

subject to the selected physical and model convention.

---

## 55. Simulation Cell

A periodic simulation cell may be represented by a matrix:

`H ∈ R^(3×3)`.

The precise interpretation of columns or rows as lattice vectors must be declared by the selected convention.

---

## 56. Interaction Graph

An interaction graph is:

`G = (V, E_G)`.

Here:

- `V` is the vertex set;
- `E_G` is the edge set.

The notation `E_G` avoids collision with scalar energy `E`.

---

## 57. Vertex Identity

A vertex or entity identity is denoted:

`i`

or by a stable identifier:

`id_i`.

An array index must not automatically be interpreted as persistent identity.

---

## 58. Neighborhood

The neighborhood of entity `i` is:

`N_i`.

A neighbor relation may be derived from geometry, topology, or another explicitly defined rule.

The symbol `N_i` is a neighborhood set, not the total entity count `N`.

---

## 59. Relative Displacement

The relative displacement from entity `i` to entity `j` is denoted:

`r_ij`.

For a nonperiodic Cartesian system:

`r_ij = r_j - r_i`.

Periodic systems require the applicable image convention.

---

## 60. Distance

The scalar distance is:

`d_ij = ||r_ij||`.

Distance and displacement remain distinct:

`d_ij ∈ R_0+`

while:

`r_ij ∈ R^3`.

---

## 61. Euclidean Transformation Group

The Euclidean group is denoted:

`E(3)`.

The special Euclidean group is:

`SE(3)`.

The rotation group is:

`SO(3)`.

The orthogonal group is:

`O(3)`.

The selected EIF model must state which group acts on each representation.

---

## 62. Group Element

A generic transformation-group element is denoted:

`g ∈ G_sym`.

When the transformation is specifically rotational:

`Q ∈ SO(3)`.

When specifically translational:

`a ∈ R^3`.

---

## 63. Group Action

The action of transformation `g` on input space `X` is:

`rho_X(g): X → X`.

The action on output space `Y` is:

`rho_Y(g): Y → Y`.

---

## 64. Invariant Mapping

A mapping:

`F: X → Y`

is invariant under `G_sym` when:

`F(rho_X(g)x) = F(x)`.

---

## 65. Equivariant Mapping

A mapping:

`F: X → Y`

is equivariant when:

`F(rho_X(g)x) = rho_Y(g)F(x)`.

The input and output actions must be declared explicitly.

---

## 66. Permutation Group

The permutation group on `N` entities is:

`S_N`.

A permutation is denoted:

`pi ∈ S_N`.

The action of `pi` on an indexed state must be explicitly defined by the selected representation.

---

## 67. Equivariant Representation Space

An equivariant representation space is denoted:

`X_EQ`.

An equivariant representation is:

`z_EQ ∈ X_EQ`.

---

## 68. Invariant Representation Space

An invariant representation space is denoted:

`X_INV`.

An invariant representation is:

`z_INV ∈ X_INV`.

---

## 69. Interatomic-to-Equivariant Mapping

The mapping from atomic or interatomic state to equivariant representation is denoted:

`P_E`.

Its typed form is:

`P_E: X_A → X_EQ`.

---

## 70. Equivariant-to-Resonance Mapping

The mapping from equivariant representation to resonance representation is denoted:

`P_ER`.

Its typed form is:

`P_ER: X_EQ → X_R`.

---

## 71. Ternary Feedback Mapping

A feedback mapping from ternary and interatomic representation state may be denoted:

`P_TE`.

Its domain and codomain must be explicitly declared in the selected model.

For example:

`P_TE: T × X_EQ → X_EQ'`.

No universal codomain is assumed.

---

## 72. Learning Parameter Space

The trainable parameter space is denoted:

`Theta`.

A trainable parameter state is:

`theta_param ∈ Theta`.

The symbol `theta_param` is used when necessary to distinguish trainable parameters from oscillator phase `theta`.

---

## 73. Loss Functional

A loss functional is denoted:

`L`.

A simple typed form is:

`L: Theta → R`.

Where the loss depends explicitly on data:

`L: Theta × D → R`

for dataset space `D`.

---

## 74. Dataset

A dataset is denoted:

`D`.

An individual datum may be written:

`d ∈ D`.

The internal structure of a datum is defined by the learning problem.

---

## 75. Regularization Functional

A regularization functional may be denoted:

`Omega`.

For:

`Omega: Theta → R`.

Specific ternary, resonance, or equivariance regularizers receive explicit subscripts where required.

---

## 76. Optimization Variable

An optimization variable is denoted:

`theta_param`

when it belongs to `Theta`.

Iteration index is denoted:

`m ∈ N_0`

or another locally defined index.

---

## 77. Molecular Dynamics State

A molecular-dynamics state space is denoted:

`X_MD`.

A state is:

`x_MD ∈ X_MD`.

A possible decomposition is:

`X_MD = X_pos × X_mom × X_cell × X_aux`.

The auxiliary state may contain TR-EIF-specific resonance, ternary, routing, thermostat, barostat, or memory variables.

---

## 78. Equation of Motion

A continuous evolution equation is written generally as:

`dx/dt = f(x, u, p, t)`.

The mapping:

`f`

must have a codomain compatible with the tangent or derivative structure of the selected state space.

---

## 79. Numerical Integrator

A numerical step operator is denoted:

`Phi_Delta_t`.

Its typed form is:

`Phi_Delta_t: X_num → X_num`

for the selected numerical state space.

The numerical step operator is distinct from the exact flow.

---

## 80. Exact Flow

Where the continuous system has a flow, it may be denoted:

`phi_t`.

The notation preserves:

`Phi_Delta_t ≠ phi_Delta_t`

unless exact equality has been established for the selected system and integrator.

---

## 81. Numerical Error

A numerical error quantity may be denoted:

`e_num`.

The associated norm or metric must be defined.

---

## 82. Absolute Tolerance

Absolute tolerance is denoted:

`atol`.

Its dimensional type must match the quantity being compared unless the comparison is dimensionless.

---

## 83. Relative Tolerance

Relative tolerance is denoted:

`rtol`.

It is dimensionless.

---

## 84. Generic Numerical Tolerance

A generic tolerance may be denoted:

`epsilon`

with:

`epsilon ≥ 0`.

Its meaning is local to a specified comparison contract.

---

## 85. Numerical Metric

A metric or distance used for numerical comparison is denoted:

`d`.

Its typed form is:

`d: X × X → R_0+`.

The selected metric must be appropriate to the state space.

For circular phase, a circular metric must be used.

---

## 86. Norm

A norm is denoted:

`||x||`.

The specific norm must be declared where multiple choices are possible.

---

## 87. Validation Result Set

The validation result set is:

`K_val = {PASS, FAIL, UNRESOLVED}`.

A validation result is:

`v_val ∈ K_val`.

This set is distinct from:

`T = {-1, 0, 1}`.

---

## 88. Boolean Predicate

A Boolean predicate is written:

`B: X → {true, false}`.

Boolean values are not balanced ternary states.

---

## 89. Invariant Predicate

An invariant predicate is denoted:

`I`.

For:

`I: X → {true, false}`,

a state satisfies the invariant when:

`I(x) = true`.

---

## 90. Provenance Set

The provenance set is:

`P_prov = {PRIMARY_SOURCE, DERIVED, CALIBRATED, AUTHOR_DEFINED, BENCHMARK, TEST_FIXTURE, REQUIRES_SOURCE, REQUIRES_TEST}`.

A provenance label is:

`p_prov ∈ P_prov`.

---

## 91. Primary Source

`PRIMARY_SOURCE`

identifies a classical definition, equation, relation, or scientific statement grounded in its cited primary source.

---

## 92. Derived

`DERIVED`

identifies a quantity or statement obtained from previously defined mathematical objects or calculations.

---

## 93. Calibrated

`CALIBRATED`

identifies a value established through an explicit calibration procedure.

---

## 94. Author Defined

`AUTHOR_DEFINED`

identifies a TR-EIF-specific formal structure, mapping, classification, execution rule, or architecture contract introduced by the framework.

---

## 95. Benchmark

`BENCHMARK`

identifies an implementation measurement obtained under a declared benchmark setup.

---

## 96. Test Fixture

`TEST_FIXTURE`

identifies controlled data or state constructed for deterministic or validation testing.

---

## 97. Requires Source

`REQUIRES_SOURCE`

identifies a statement that requires an external source before it is treated as sourced scientific content.

---

## 98. Requires Test

`REQUIRES_TEST`

identifies a computational claim requiring executable evidence.

---

## 99. Physical Dimensions

The dimension of quantity `q` may be denoted:

`dim(q)`.

Two quantities may be added or subtracted only when their dimensions are compatible.

For admissible addition:

`dim(a) = dim(b)`.

---

## 100. Dimensionless Quantity

A dimensionless quantity satisfies:

`dim(q) = 1`

under the adopted dimensional notation.

Phase-order magnitude `R` is dimensionless.

A phase angle may be represented numerically as dimensionless but retains circular semantics.

---

## 101. Unit Convention

A unit convention is denoted locally by:

`U_q`

when explicit notation is required.

Unit identity and physical dimension are distinct.

Different units may represent quantities of the same dimension.

---

## 102. Energy and Ternary State

The notation preserves:

`E ≠ t_exec`.

Energy and ternary state belong to different codomains.

---

## 103. Force and Ternary State

The notation preserves:

`F_i ≠ t_exec`.

A force vector and a ternary state belong to distinct mathematical spaces.

---

## 104. Resonance Classification and Energy

The notation preserves:

`C_R(r) ≠ E(x)`.

Resonance classification and energy have distinct codomains and meanings.

---

## 105. Phase Relation and Chemical Bond

A phase relation may be written:

`Delta theta_ij`.

A chemical-bond descriptor, if defined, must use an independent symbol and mapping.

The notation does not identify the two objects.

---

## 106. Structural State

A structural state space may be denoted:

`X_S`.

A structural state is:

`s ∈ X_S`.

It is distinct from balanced ternary state unless a mapping between `X_S` and `T` is explicitly defined.

---

## 107. Physical Phase State

A thermodynamic or material phase state, where defined, belongs to a separately declared space:

`X_P`.

It is distinct from oscillator phase:

`theta ∈ S^1`.

---

## 108. Bifurcation Parameter

A parameter varied in a bifurcation analysis may be denoted:

`mu ∈ P_mu`.

A named bifurcation requires the mathematical conditions associated with the selected bifurcation class.

---

## 109. Threshold

A model threshold may be denoted:

`eta`.

The threshold's domain, units, and provenance must be defined.

A threshold crossing is not denoted or treated as a bifurcation by default.

---

## 110. Cutoff

A geometric or interaction cutoff may be denoted:

`r_c`.

A cutoff radius is distinct from a resonance window.

The notation preserves:

`r_c ≠ W_R`.

---

## 111. Uncertainty Space

An uncertainty representation space is denoted:

`X_U`.

An uncertainty value is:

`u_unc ∈ X_U`.

This notation distinguishes uncertainty from external input `u`.

---

## 112. Domain Status

A model-domain classification set may be denoted:

`K_D`.

A domain detector is:

`D_dom: X → K_D`.

The domain-status set must not be conflated with balanced ternary state.

---

## 113. Reference Data

A reference-data space may be denoted:

`D_ref`.

A reference datum is:

`d_ref ∈ D_ref`.

Its provenance must be recorded where the value enters scientific or validation claims.

---

## 114. Benchmark Record

A benchmark result may be denoted:

`b ∈ B_data`

where `B_data` is the benchmark-record space.

Benchmark records must preserve implementation and configuration context.

---

## 115. Trace Space

A trace-record space is denoted:

`X_trace`.

A trace record is:

`e_trace ∈ X_trace`.

A trace projection is:

`P_trace: X_exec → X_trace`.

---

## 116. State and Trace

The notation preserves:

`X_exec ≠ X_trace`.

A trace is a projection or record of execution.

It is not automatically a complete execution state.

---

## 117. Checkpoint State

A restart-complete checkpoint representation may be denoted:

`x_CP`.

Its semantic source is the complete result-affecting retained state required by the restart contract.

A checkpoint is distinct from an arbitrary state snapshot.

---

## 118. Snapshot

A state snapshot is denoted:

`x_snap`.

The notation preserves:

`x_snap ≠ x_CP`

unless the snapshot is explicitly complete for restart.

---

## 119. Scheduler State

Scheduler state is denoted:

`x_sched ∈ X_sched`.

It belongs to execution-control state.

It is distinct from model time and physical state unless a specific model defines a mapping.

---

## 120. Request

A computational request is denoted:

`q_req ∈ X_req`.

A request proposes an operation.

It is distinct from an authorization and a commit.

---

## 121. Authorization

An authorization result is denoted:

`a_auth ∈ X_auth`.

The notation preserves:

`q_req ≠ a_auth`.

---

## 122. Commit

A commit event is denoted:

`e_commit ∈ X_commit`.

The notation preserves:

`authorization ≠ commit`.

---

## 123. Execution Event

A generic execution event is denoted:

`e ∈ X_event`.

Where confusion with energy `E` is possible, lowercase event notation is retained.

---

## 124. Event Sequence

An ordered event sequence is:

`(e_0, e_1, ..., e_m)`.

Event ordering must identify the coordinate used to establish order.

---

## 125. Numerical Proposal

A proposed numerical state is denoted:

`x_prop`.

It is distinct from accepted or committed retained state.

---

## 126. Accepted Numerical State

An accepted numerical state may be denoted:

`x_acc`.

Numerical acceptance and architectural commit remain distinct operations.

---

## 127. Solver State

Solver state is denoted:

`x_solver ∈ X_solver`.

Any result-affecting solver state belongs to computational state closure.

---

## 128. Random State

Random generator state, when required, is denoted:

`x_rng ∈ X_rng`.

A random seed is denoted:

`s_rng`.

Seed and complete generator state are distinct unless the selected generator contract makes them equivalent.

---

## 129. Configuration

A computational configuration is denoted:

`c ∈ X_cfg`.

A configuration identifier may be written:

`id_cfg`.

Immutable configuration and evolving state remain distinct.

---

## 130. Execution Profile

An execution profile is denoted:

`P_exec`.

It specifies the computational conditions associated with a reproducibility or qualification claim.

---

## 131. Reproducibility Relation

A declared reproducibility relation is denoted:

`~_rep`.

For results `a` and `b`:

`a ~_rep b`

means that they satisfy the declared comparison relation.

---

## 132. Semantic Equivalence

Generic semantic equivalence may be denoted:

`≡`.

The exact meaning of `≡` must be declared for the space in which it is used.

It must not be substituted automatically for exact equality `=`.

---

## 133. Backend

A computational backend is denoted:

`B`.

Where several backends exist:

`B_a`, `B_b`, and so on.

Backend identity is distinct from model identity.

---

## 134. Environment

An execution environment is denoted:

`E_env`.

This notation distinguishes environment from energy `E`.

---

## 135. Artifact

A generic artifact is denoted:

`a_art ∈ A_art`.

Artifact class, schema, and semantic role must be explicit where machine interpretation is required.

---

## 136. Schema

A schema is denoted:

`S_schema`.

A schema identity may be written:

`id_schema`.

Schema version may be written:

`v_schema`.

---

## 137. Artifact Serialization

A serialization mapping is:

`Ser: A_art → B_ser`.

A deserialization mapping is:

`Des: B_ser,valid → A_art`.

For lossless semantic serialization:

`Des(Ser(a_art)) ≡ a_art`.

---

## 138. Information Loss

For mapping:

`F: X → Y`,

information loss must be described relative to the source domain and target representation.

Non-injectivity is written:

`F(x_1) = F(x_2)`

for some:

`x_1 ≠ x_2`.

This demonstrates that source states are not uniquely recoverable through `F` over that domain.

---

## 139. Injective Mapping

A mapping:

`F: X → Y`

is injective when:

`F(x_1) = F(x_2)`

implies:

`x_1 = x_2`.

---

## 140. Surjective Mapping

A mapping:

`F: X → Y`

is surjective when every:

`y ∈ Y`

has at least one:

`x ∈ X`

such that:

`F(x) = y`.

---

## 141. Bijective Mapping

A mapping is bijective when it is both injective and surjective.

A bijection has an inverse over its complete domain and codomain.

---

## 142. Restriction of a Mapping

For:

`A ⊆ X`

and:

`F: X → Y`,

the restriction of `F` to `A` is denoted:

`F|_A`.

---

## 143. Image

The image of set `A ⊆ X` under:

`F: X → Y`

is:

`F(A) = {F(x) | x ∈ A}`.

---

## 144. Preimage

For:

`B ⊆ Y`,

the preimage under `F` is:

`F^(-1)(B) = {x ∈ X | F(x) ∈ B}`.

This notation does not require `F` to be invertible.

---

## 145. Boundary

The boundary of a set `A` is written:

`∂A`.

For resonance window:

`∂W_R`.

The topology under which the boundary is defined must be appropriate to the selected space.

---

## 146. Interior

The interior of a set `A` is written:

`int(A)`.

---

## 147. Closure

The closure of a set `A` is written:

`cl(A)`.

This mathematical closure is distinct from repository or qualification closure.

Context must make the intended meaning explicit.

---

## 148. Neighborhood in Topology

A topological neighborhood of point `x` may be denoted:

`U_x`.

This notation is distinct from external input space `U`.

Where both occur in the same scope, a more explicit local symbol must be used.

---

## 149. Metric Space

A metric space is written:

`(X, d)`.

The metric:

`d: X × X → R_0+`

must satisfy the metric axioms.

---

## 150. Circular Metric

For phase space `S^1`, a circular distance is denoted:

`d_S1(theta_a, theta_b)`.

Its exact expression depends on the chosen representative convention.

---

## 151. Graph Distance

A graph distance may be denoted:

`d_G(i, j)`.

It is distinct from Euclidean geometric distance `d_ij`.

---

## 152. Probability Notation

Where probability is introduced, a probability space is written:

`(Omega_P, F_P, P_P)`.

This notation avoids collision with optimization functional `Omega`, mapping `F`, and parameter space `P`.

Probability notation must be introduced locally when required.

---

## 153. Expectation

Expectation may be denoted:

`E_P[X]`

where the subscript distinguishes expectation from energy `E`.

---

## 154. Variance

Variance may be denoted:

`Var(X)`.

Its probabilistic domain must be explicitly defined.

---

## 155. Gradient

For scalar functional:

`E: R^n → R`,

the gradient is:

`grad E`.

For atomic coordinates:

`grad_R E`.

---

## 156. Partial Derivative

The partial derivative with respect to variable `x_i` is written:

`partial F / partial x_i`.

This textual notation is used consistently in repository Markdown without raw LaTeX delimiters.

---

## 157. Time Derivative

For time-dependent state `x(t)`:

`dx/dt`

denotes its derivative with respect to model time.

---

## 158. Discrete Difference

For a discrete sequence `x[k]`, a first difference may be defined locally as:

`Delta x[k] = x[k+1] - x[k]`.

This notation is valid only when subtraction is defined in the state space.

It is not used directly for categorical ternary transition semantics.

---

## 159. Ternary Transition Event

A ternary transition is represented relationally:

`t_exec[k] → t_exec[k+1]`.

The transition event is not represented by arithmetic subtraction between ternary labels.

---

## 160. Indicator Function

For set `A`, an indicator may be denoted:

`1_A(x)`.

It takes values in:

`{0, 1}`.

This binary indicator is distinct from balanced ternary state.

---

## 161. Sign Function

If used, the sign function is:

`sgn: R → {-1, 0, 1}`.

Its existence does not make every sign classification a TR-EIF ternary state.

A TR-EIF ternary target requires its own explicitly defined mapping.

---

## 162. Kronecker Delta

The Kronecker delta is:

`delta_ij = 1`

when:

`i = j`

and:

`delta_ij = 0`

otherwise.

It is a binary mathematical object and is unrelated to active ternary neutral semantics.

---

## 163. Matrix

A matrix is denoted:

`A ∈ R^(m×n)`.

Its semantic role must be defined locally.

---

## 164. Tensor

A tensor is specified by its transformation law and component structure.

Array rank alone is not sufficient to establish tensor meaning.

---

## 165. Scalar

A scalar belongs to a one-dimensional scalar field such as `R`.

Scalar status does not imply invariance under every transformation.

Its transformation behavior must be defined where relevant.

---

## 166. Vector

A vector in three-dimensional Cartesian space is an element of:

`R^3`.

Its transformation under rotations is defined by the applicable group action.

---

## 167. Pseudovector and Other Representations

Where nonstandard transformation representations are required, they must be introduced explicitly.

No output is assumed to transform as an ordinary Cartesian vector solely because it has three numerical components.

---

## 168. State Update Mapping

A discrete state-update mapping may be denoted:

`F_step: X × U × P → X`.

For:

`x[k+1] = F_step(x[k], u[k], p)`.

The update mapping must not be confused with a continuous vector field.

---

## 169. Vector Field

A continuous-time vector field may be denoted:

`f`.

For Euclidean state:

`f: X × U × P × I_t → R^n`.

The lowercase symbol distinguishes it from a discrete update map where useful.

---

## 170. Event Guard

An event guard may be denoted:

`G_event: X → {true, false}`.

A guard determines eligibility of an event under its declared semantics.

It does not itself execute the state transition.

---

## 171. Reset Map

A hybrid reset map may be denoted:

`J: X_pre → X_post`.

The pre-event and post-event spaces must be defined.

---

## 172. Scheduler Decision

A scheduler decision may be denoted:

`d_sched ∈ X_dec`.

It is execution-control state, not a physical observable.

---

## 173. Capacity

Computational capacity may be denoted:

`c_cap`.

If physical capacity is also modeled, a distinct symbol must be used.

---

## 174. Queue

A request queue may be denoted:

`Q_req`.

The symbol is distinct from rotation matrix `Q`.

Where both appear locally, explicit subscripts are mandatory.

---

## 175. Topology State

A topology state space is denoted:

`X_G`.

A topology state is:

`g_top ∈ X_G`.

The symbol avoids collision with transformation-group element `g`.

---

## 176. Model Family

A parameterized family of models may be denoted:

`M(theta_param)`

or:

`M_p`

depending on context.

The family notation must specify which parameters vary.

---

## 177. TR Layer State

The complete Ternary Resonant state space may be denoted:

`X_TR`.

A state is:

`x_TR ∈ X_TR`.

This state may contain multiple components such as phase, resonance, memory, classification, target, and executed ternary state.

---

## 178. EIF Layer State

The complete Equivariant Interatomic Framework state space may be denoted:

`X_EIF`.

A state is:

`x_EIF ∈ X_EIF`.

---

## 179. Integrated TR-EIF State

The integrated state space may be denoted:

`X_TR-EIF`

in prose and code-style mathematical notation.

An integrated state is:

`x_TR-EIF ∈ X_TR-EIF`.

Where a notation system does not admit the hyphen conveniently, a local alias must be explicitly defined rather than assumed.

---

## 180. Forward Integration Mapping

The EIF-to-TR mapping is denoted:

`F_E→TR`.

Its general typed form is:

`F_E→TR: X_EIF → X_TR,in`

or another explicitly declared domain containing required history, scale, or auxiliary state.

---

## 181. Reverse Integration Mapping

The TR-to-EIF mapping is denoted:

`F_TR→E`.

Its output is normally an EIF update request space:

`X_EIF,req`.

Its typed form is:

`F_TR→E: X_TR × X_EIF → X_EIF,req`

or another explicitly defined model-specific mapping.

---

## 182. Integrated Mapping Chain

The canonical conceptual chain is:

`X_EIF`

`→ X_EQ`

`→ X_R`

`→ T_target`

`→ T_exec`

`→ X_EIF,req`.

Each arrow must correspond to an explicit mapping or execution relation.

---

## 183. Scientific Distinction Notation

The symbol:

`≠`

is used to indicate that two concepts, variables, spaces, or interpretations are not generally identical.

The following relations are canonical:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`resonance-window crossing ≠ bifurcation`

`bifurcation ≠ ternary transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`oscillator phase ≠ physical phase of matter`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`ternary state ≠ energy`

`resonance classification ≠ energy`

`delay ≠ phase lag`

`target ≠ executed state`

`state ≠ observable`

`local state ≠ global observable`

`mathematical model ≠ numerical realization`.

---

## 184. Reserved Semantic Symbols

The following symbols have framework-wide preferred meanings:

- `T` — balanced ternary state set;
- `X_R` — resonance-coordinate space;
- `P_R` — resonance-coordinate mapping;
- `W_R` — resonance window;
- `∂W_R` — resonance-window boundary;
- `R` — Kuramoto-style phase-order magnitude when phase order is in scope;
- `C` — separately defined coherence observable;
- `theta` — oscillator phase;
- `gamma` — phase lag;
- `tau` — temporal delay;
- `X_EIF` — EIF state space;
- `X_TR` — TR state space;
- `P_prov` — provenance set;
- `K_val` — validation result set.

A chapter introducing a conflicting local use must rename the local symbol instead of redefining these reserved meanings.

---

## 185. Symbol Introduction Rule

Every nonstandard symbol must be defined before first substantive use.

A symbol definition must provide enough information to determine:

- semantic role;
- domain;
- codomain where it is a mapping;
- dimensions where applicable;
- indexing where applicable.

---

## 186. Symbol Reuse Rule

A symbol must not be reused for a different semantic object within the same active scope.

When established notation creates unavoidable collisions, explicit subscripts or qualified names must be used.

---

## 187. Domain Rule

Every mapping must have an explicit domain.

A formula without a defined admissible input space is incomplete.

---

## 188. Codomain Rule

Every mapping must have an explicit codomain.

A numeric implementation type is not automatically the mathematical codomain.

---

## 189. Dimensional Rule

Dimensional quantities must preserve dimensional compatibility.

The mathematical validity of an operation is not determined solely by machine representability.

---

## 190. Circular-State Rule

Circular phase must remain circular under:

- comparison;
- differentiation;
- numerical storage;
- interpolation;
- observable construction.

A branch cut is a representation convention, not a physical discontinuity by itself.

---

## 191. Continuous-Discrete Rule

Continuous and discrete state spaces remain separately typed.

A continuous variable may produce a discrete target only through an explicit mapping.

---

## 192. Target-Execution Rule

A target is not a committed executed state.

Every chapter involving ternary execution must preserve:

`t_target`

and:

`t_exec`

as separate semantic objects.

---

## 193. Local-Global Rule

Local and global variables must carry notation that preserves their scale and ownership.

An aggregate must not be used as an alias for its constituents.

---

## 194. History Rule

History dependence requires explicit history state or an equivalent complete state representation.

A history-dependent relation must not be written as though it were memoryless.

---

## 195. Delay Rule

A temporal delay requires a time-shifted or history-dependent state.

A phase lag does not.

The notation must preserve the difference.

---

## 196. Exact-Numerical Rule

Exact mathematical relations and numerical comparison predicates must remain distinct.

A numerical tolerance must not be inserted into an exact categorical invariant.

---

## 197. Provenance Rule

Every sourced, derived, calibrated, author-defined, benchmark, or fixture quantity may be associated with the applicable provenance class.

Provenance is metadata about origin and evidence.

It is not mathematical state.

---

## 198. Implementation-Parameter Rule

Implementation-specific constants must be qualified by implementation context.

They must not be denoted or described as universal TR-EIF constants unless the formal theory explicitly defines them as such.

---

## 199. FRP Reference Notation

Where FRP is used as an executable reference, FRP-specific variables retain the notation of the verified executable source when necessary for exact traceability.

Their relation to TR-EIF notation must be stated explicitly.

The architectural relation is:

`TR-EIF formal theory → FRP executable specialization/reference`.

---

## 200. Notation Closure

A mathematical section is notation-complete when:

1. every symbol is defined before substantive use;
2. every mapping has a domain;
3. every mapping has a codomain;
4. state variables are distinguishable from observables;
5. continuous variables are distinguishable from discrete variables;
6. circular variables are identified;
7. dimensional quantities have compatible operations;
8. local and global states are distinguishable;
9. targets and executed states are distinguishable;
10. history and memory are explicit where required;
11. exact relations and numerical tolerances are distinct;
12. transformation behavior is explicit where required;
13. provenance is identifiable where relevant.

---

## 201. Canonical Foundation

The notation established in this chapter supports the complete repository architecture:

`Mathematical Foundations`

`→ Ternary Resonance Theory`

`→ Equivariant Interatomic Framework`

`→ Learning and Optimization`

`→ Molecular Dynamics`

`→ Multiscale Materials Modeling`

`→ FLiBe Reference Model`.

The central typed integration chain remains:

`interatomic state`

`→ equivariant representation`

`→ resonance state`

`→ ternary target`

`→ neutral-mediated -1/0/1 execution`

`→ interatomic feedback`.

All subsequent mathematical definitions must preserve the domains, codomains, state distinctions, symmetry actions, dimensional structure, and notation invariants established here.
