# Phase Oscillator and Kuramoto–Sakaguchi Module

## 1. Purpose

This document defines the phase-oscillator module used by the Ternary Resonant Equivariant Interatomic Framework.

The chapter connects three strictly separated layers:

1. classical coupled-phase mathematics;
2. the TR-EIF formal resonance interface;
3. the executable FRP reference realization of the corresponding resonant phase-processing chain.

The phase module provides a continuous or tact-by-tact resonant state from which later TR-EIF layers may derive:

- phase relations;
- phase order;
- synchronization descriptors;
- multiscale organization;
- resonance coordinates;
- balanced ternary targets.

The phase module does not replace the complete TR-EIF architecture.

The complete relation is:

`phase state`

`→ coupled phase evolution`

`→ phase-order formation`

`→ resonance-state contribution`

`→ phase-derived ternary qualification`

`→ constrained -1/0/1 execution`

The continuous phase domain and the balanced ternary domain remain separately typed.

## 2. Dependency

This chapter depends on:

- Volume 01 — Mathematical Foundations;
- `chapter_01_ternary_resonance_formalism.md`;
- `chapter_02_resonance_state_spaces_and_windows.md`;
- `chapter_03_resonance_dynamics.md`;
- `chapter_04_ternary_resonance_transition_semantics.md`;
- `chapter_05_resonance_coupling_synchronization_and_coherence.md`.

The definitions established in those chapters remain authoritative.

## 3. Scientific Status Classes

Relations in this chapter are separated into three classes.

### 3.1 CLASSICAL

A relation originating from established phase-oscillator mathematics.

### 3.2 TR-EIF FORMAL

An author-defined TR-EIF relation connecting classical phase dynamics to the resonance-state architecture.

### 3.3 FRP EXECUTABLE REFERENCE

A concrete computational realization present in the Fractal Resonance Processor repository.

An FRP-specific numerical coefficient is therefore an implementation parameter of the reference realization.

It is not automatically a universal TR-EIF constant.

## 4. Core Semantic Separation

The following objects remain distinct:

`phase state`

`frequency state`

`phase lag`

`coupling state`

`phase order`

`synchronization`

`coherence`

`resonance state`

`resonance classification`

`ternary target`

`retained ternary state`

In particular:

`phase order ≠ complete coherence`

`phase order ≠ resonance`

`resonance ≠ ternary state`

`ternary target ≠ retained ternary state`

## 5. Classical Primary Sources

### 5.1 Kuramoto Phase Coupling

Yoshiki Kuramoto.

"Self-entrainment of a population of coupled non-linear oscillators."

International Symposium on Mathematical Problems in Theoretical Physics.

Lecture Notes in Physics, Volume 39.

Springer, 1975.

Pages 420–422.

DOI:

`10.1007/BFb0013365`

### 5.2 Sakaguchi–Kuramoto Phase-Lag Coupling

Hidetsugu Sakaguchi and Yoshiki Kuramoto.

"A Soluble Active Rotator Model Showing Phase Transitions via Mutual Entrainment."

Progress of Theoretical Physics.

Volume 76, Issue 3.

1986.

Pages 576–581.

DOI:

`10.1143/PTP.76.576`

## 6. Phase Domain

For phase domain `i`, define:

`theta_i ∈ S1`

where:

`S1`

denotes the unit-circle phase space.

For `N` phase domains:

`Theta = (theta_1, theta_2, ..., theta_N)`

with:

`Theta ∈ S1^N`

Phase is therefore circular.

A numerical interval used to store phase is a coordinate representation of the circular state.

## 7. Circular Equivalence

For any integer `k`:

`theta_i`

and:

`theta_i + 2 pi k`

represent the same phase state.

A phase implementation must preserve this equivalence.

## 8. Intrinsic Frequency

For phase domain `i`, define:

`omega_i`

as the intrinsic angular-frequency parameter of the classical phase model.

The complete frequency vector is:

`Omega = (omega_1, ..., omega_N)`

The symbol `omega_i` must not be identified automatically with:

- a measured instantaneous frequency;
- a resonant eigenfrequency;
- an external forcing frequency;
- a spectral maximum;
- an interatomic vibrational frequency.

Such interpretations require their own mappings.

## 9. Relative Phase

For phase domains `i` and `j`, define the oriented relative phase:

`Delta_theta_ji = theta_j - theta_i`

with circular equivalence preserved.

The orientation of the subtraction must remain consistent throughout a model.

## 10. Classical Kuramoto Interaction

**Status: CLASSICAL**

A standard globally coupled Kuramoto phase system is represented by:

`d theta_i / dt = omega_i + (K / N) sum_j sin(theta_j - theta_i)`

where:

- `theta_i` is phase;
- `omega_i` is intrinsic angular frequency;
- `K` is global coupling strength;
- `N` is oscillator count.

The phase interaction depends on relative phase rather than absolute phase alone.

## 11. Classical Sakaguchi–Kuramoto Interaction

**Status: CLASSICAL**

The Sakaguchi–Kuramoto form introduces a phase-lag parameter.

Using the orientation adopted in this chapter:

`d theta_i / dt = omega_i + (K / N) sum_j sin(theta_j - theta_i - gamma)`

where:

`gamma`

is the phase-lag parameter.

The sign convention must remain explicit.

## 12. Source Sign Convention

The Sakaguchi–Kuramoto source may equivalently be written in the orientation:

`d phi_i / dt = omega_i - (K / N) sum_j sin(phi_i - phi_j + alpha)`

because:

`-sin(x) = sin(-x)`

The correspondence between the two representations is valid only when the phase-difference and phase-lag conventions are transformed consistently.

## 13. Phase Lag Is Not Phase Difference

The phase lag:

`gamma`

and the evolving phase difference:

`Delta_theta_ji`

are different mathematical objects.

Therefore:

`gamma ≠ Delta_theta_ji`

in general.

## 14. Phase Lag Is Not Time Delay

The phase lag:

`gamma`

and a time delay:

`tau`

are also different objects.

Therefore:

`gamma ≠ tau`

A particular physical model may relate them only through an additional derivation.

## 15. Classical Complex Order Parameter

**Status: CLASSICAL**

For `N` phases, define:

`Z = (1 / N) sum_j exp(i theta_j)`

and:

`Z = R exp(i Psi)`

where:

- `R` is the global phase-order magnitude;
- `Psi` is the collective phase.

For equal unit weighting:

`0 ≤ R ≤ 1`

## 16. Real-Component Form of Phase Order

The same magnitude is:

`R = sqrt(c_mean^2 + s_mean^2)`

where:

`c_mean = (1 / N) sum_j cos(theta_j)`

and:

`s_mean = (1 / N) sum_j sin(theta_j)`

This is the representation used by the FRP executable reference.

## 17. Meaning of R

`R`

measures concentration of phases under the complex phase-average construction.

It does not uniquely reconstruct the complete phase vector.

Therefore:

`same R ≠ same Theta`

## 18. R Is Not General Structural Coherence

The phase-order magnitude:

`R`

must remain distinct from the general TR-EIF concept of structural coherence.

Therefore:

`R(t) ≠ C(t)`

unless a specific reduced model explicitly defines such an identification.

The FRP reference realization also preserves this distinction.

## 19. R Is Not Resonance Classification

`R`

may contribute to resonance coordinates.

It does not replace:

`P_R`

`W_R`

or:

`C_R`

from the preceding chapters.

Therefore:

`R ≠ resonance classifier`

## 20. R Is Not Ternary State

The continuous scalar:

`R`

does not belong to:

`T = {-1, 0, 1}`

A separate projection is required before balanced ternary execution.

## 21. TR-EIF Phase-Module Interface

**Status: TR-EIF FORMAL**

The TR-EIF phase module may be represented by the typed state:

`X_phase = (Theta, Omega, K_state, Gamma_state, H_phase)`

where:

- `Theta` is the phase state;
- `Omega` is the frequency state;
- `K_state` is the declared coupling state;
- `Gamma_state` is the phase-lag state;
- `H_phase` is phase-related memory where required.

The exact product structure is model-specific.

## 22. Phase Module to Resonance Space

The resonance-coordinate mapping may depend on the phase module:

`P_R: S × P → X_R`

with phase-related components supplied from:

`X_phase`

Possible inputs include:

- phase differences;
- phase-order magnitude;
- local phase order;
- frequency relations;
- coupling state;
- phase lag;
- phase history.

No one coordinate is universally mandatory.

## 23. FRP Reference Boundary

**Status: FRP EXECUTABLE REFERENCE**

The FRP implementation provides a concrete executable realization of the phase-to-ternary chain.

The principal floating semantic reference is:

`frp_prototype_v1_7_0.py`

Relevant mathematical documentation includes:

- `docs/mathematical_foundation.md`;
- `docs/resonance_computation.md`.

The retained-state RTL boundary begins after generation of the phase-derived ternary target.

The nonlinear resonant phase field therefore remains an upstream semantic domain relative to the retained ternary execution layer.

## 24. FRP Phase-State Domain

For `N` FRP cells, the floating semantic reference stores:

`theta_i ∈ [0, 2 pi)`

as the numerical coordinate representation of circular phase.

Initial phases are generated inside the complete `2 pi` interval.

After every phase update, the state is wrapped by:

`mod 2 pi`

## 25. FRP Dyadic Cell Requirement

The current FRP hierarchical phase topology requires:

`N`

to be a power of two and:

`N ≥ 2`

The hierarchy depth is:

`D = bit_length(N) - 1`

For a power-of-two population, this equals:

`log2(N)`

## 26. FRP Hierarchical Distance

For two distinct cell indexes `i` and `j`, FRP defines:

`d(i,j) = bit_length(i XOR j)`

For identical indexes:

`d(i,i) = 0`

The nonzero distance takes values:

`1, 2, ..., D`

This defines the dyadic hierarchical shell relation used by the reference implementation.

## 27. Shell Population

For hierarchical distance `d`:

`n_d = 2^(d - 1)`

where:

`n_d`

is the number of cells in the corresponding sibling shell of a given cell.

## 28. Fractal Coupling Exponent

The reference implementation defines the fractal coupling exponent:

`alpha`

The current executable reference uses:

`alpha = 0.70`

This is an FRP reference parameter.

It is not a universal TR-EIF constant.

## 29. Hierarchical Weight Normalizer

For hierarchy depth `D`, define:

`Z_alpha = sum_(d=1..D) 1 / d^alpha`

The normalized pair weight for shell distance `d` is:

`w_d = 1 / (n_d d^alpha Z_alpha)`

## 30. Aggregate Shell Influence

Because each shell contains:

`n_d`

cells, its aggregate normalized influence is:

`n_d w_d = 1 / (d^alpha Z_alpha)`

Therefore the total shell influence satisfies:

`sum_(d=1..D) n_d w_d = 1`

This normalized dyadic relation is the basis of the FRP hierarchical coupling matrix.

## 31. FRP Coupling Matrix

For:

`i ≠ j`

the reference coupling matrix uses:

`W_ij = w_d(i,j)`

and:

`W_ii = 0`

The implementation constructs a symmetric normalized hierarchical matrix from the dyadic distance relation.

## 32. Nominal Coupling Strength

The floating FRP reference defines:

`K_0 = 0.28`

as the nominal coupling multiplier.

This coefficient belongs to the concrete FRP reference realization.

It must not be promoted to a universal TR-EIF coupling constant.

## 33. Thermal Coupling Factor

FRP modifies effective coupling through a local thermal factor.

For local overload:

`q_i ≥ 0`

the node factor is:

`h_i = exp(-0.5 g_T q_i)`

The executable reference uses:

`g_T = 2.50`

Therefore:

`0 < h_i ≤ 1`

for finite nonnegative overload.

## 34. Pair Thermal Factor

For cells `i` and `j`, the phase-coupling interaction contains:

`h_i h_j`

Thus thermal state can attenuate the effective pair interaction without changing the underlying hierarchical weight:

`W_ij`

## 35. Nominal FRP Phase Lag

The executable reference defines:

`gamma_nominal = 0.30 pi`

This is the nominal FRP phase-lag setting.

It is a concrete reference parameter rather than a universal TR-EIF value.

## 36. Local Effective Phase Lag

Unlike the uniform classical Sakaguchi–Kuramoto model, FRP maintains a local effective phase lag:

`gamma_effective_i`

The receiving cell `i` therefore uses its own current phase-lag state.

## 37. Correlated Gamma State

Let:

`xi_i[n]`

denote the retained local gamma-noise state and:

`xi_target_i[n]`

its current target.

The executable reference updates:

`xi_i[n+1] = xi_i[n] + 0.15 (xi_target_i[n] - xi_i[n])`

The target is refreshed periodically in the reference implementation.

## 38. Gamma Target Refresh

The floating reference refreshes gamma-noise targets on ticks satisfying:

`n mod 8 = 0`

Each refreshed target is drawn from the interval:

`[-1, 1]`

using the seeded reference pseudorandom generator.

The retained filtered state therefore changes gradually rather than being replaced immediately by the new target.

## 39. Thermal Gamma Drift

The current local effective phase lag is:

`gamma_effective_i[n] = gamma_nominal + 0.08 q_i[n] xi_i[n]`

where:

- `q_i[n]` is local thermal overload;
- `xi_i[n]` is the retained correlated gamma state.

The phase-lag drift is:

`Delta_gamma_i[n] = gamma_effective_i[n] - gamma_nominal`

## 40. Local Asymmetry

The FRP interaction of receiving cell `i` uses:

`gamma_effective_i`

rather than a universal pair value.

Therefore the interaction term contains:

`sin(theta_j - theta_i - gamma_effective_i)`

The local phase-lag field can differ across receiving cells.

## 41. FRP Dense Coupling Field

The exact dense reference form is:

`F_i[n] = K_0 sum_(j != i) W_ij h_i h_j sin(theta_j[n] - theta_i[n] - gamma_effective_i[n])`

where:

- `K_0` is nominal coupling;
- `W_ij` is the normalized hierarchical weight;
- `h_i` and `h_j` are thermal node factors;
- `gamma_effective_i` belongs to the receiving cell.

## 42. Dense Form Is Not Uniform Mean Field

The FRP dense field is not the simple uniform:

`K / N`

all-to-all Kuramoto interaction.

Its coupling contains:

- hierarchical distance weighting;
- local thermal attenuation;
- local effective Sakaguchi lag.

It therefore belongs to the TR-EIF/FRP extension layer rather than the unmodified classical model.

## 43. FRP Hierarchical Coupling Path

The executable reference also implements a hierarchical evaluation path.

Instead of evaluating every pair contribution independently, the hierarchical path aggregates weighted real and imaginary phase components over dyadic sibling shells.

For cell `i`, define the local phase offset:

`phi_i = theta_i + gamma_effective_i`

The shell contribution is obtained from the imaginary projection of the shell's complex phase sum relative to:

`phi_i`

and multiplied by the shell weight.

## 44. Hierarchical Shell Projection

For a sibling shell with weighted real sum:

`A_d`

and weighted imaginary sum:

`B_d`

the phase projection relative to cell `i` is:

`cos(phi_i) B_d - sin(phi_i) A_d`

This is the aggregated form of the corresponding sine interactions.

## 45. Hierarchical Coupling Field

The resulting hierarchical field has the form:

`F_i[n] = K_0 h_i sum_d w_d ImShell_i,d[n]`

where:

`ImShell_i,d`

denotes the shell imaginary projection defined by the phase state and the local phase offset.

The reference implementation contains both dense and hierarchical coupling paths.

## 46. Dense–Hierarchical Semantic Relation

The dense path and hierarchical path represent two evaluation forms of the same dyadic coupling structure in the FRP semantic reference.

The implementation maintains explicit dense/hierarchical equivalence machinery and a declared numerical equivalence tolerance.

This is an implementation property of the FRP reference.

## 47. Stateful Frequency Domain

FRP does not use only one immutable frequency vector.

Each cell retains:

- base frequency;
- target frequency;
- current frequency.

Denote them:

`omega_base_i`

`omega_target_i[n]`

`omega_i[n]`

## 48. FRP Base Frequency

The floating executable reference initializes:

`omega_base_i = 1.0`

for every reference cell.

This value belongs to the reference configuration.

It is not a universal physical frequency.

## 49. State-Conditioned Frequency Target

The FRP reference defines:

`omega_target_i[n] = omega_base_i + 0.06 abs(sigma_i[n]) + 0.12 a_i[n]`

where:

- `sigma_i[n] ∈ {-1,0,1}`;
- `a_i[n]` is the current cell switch-activity indicator.

The absolute ternary magnitude satisfies:

`abs(0) = 0`

and:

`abs(-1) = abs(1) = 1`

## 50. Stateful Frequency Memory

The current frequency is updated by:

`omega_i[n+1] = omega_i[n] + 0.30 (omega_target_i[n] - omega_i[n])`

The coefficient:

`0.30`

is the reference delay-response coefficient.

This update retains unresolved difference from the preceding tact.

## 51. Frequency Lag

After the retained-frequency update, FRP evaluates the magnitude of the remaining lag:

`L_i[n] = abs(omega_target_i[n] - omega_i[n+1])`

The lag is subsequently available to the thermal and stability layers.

## 52. FRP Delay Semantics

The concrete FRP reference therefore realizes temporal memory through retained frequency relaxation.

It does not implement the phase interaction as a universal explicit delayed term of the form:

`theta_j(t - tau_ij)`

The two mechanisms must remain distinct.

## 53. TR-EIF Delay Boundary

TR-EIF may define other mathematically valid delay models in other implementations.

However, when this chapter describes the FRP executable realization, its current delay mechanism is:

`target frequency`

`→ retained current frequency`

`→ unresolved frequency lag`

rather than an invented pairwise phase-delay term.

## 54. Scheduler Modes

The FRP reference contains the scheduler modes:

`free`

`7/1`

`1/7`

The modes generate scheduler states with an eight-tact period where applicable.

## 55. 7/1 Scheduler Sequence

For mode:

`7/1`

the scheduler sequence is:

`balance`

`balance`

`balance`

`balance`

`balance`

`balance`

`balance`

`commit`

and then repeats.

Thus:

`7/1 = seven balance tacts followed by one commit tact`

## 56. 1/7 Scheduler Sequence

For mode:

`1/7`

the scheduler sequence is:

`excite`

`neutralize`

`neutralize`

`neutralize`

`neutralize`

`neutralize`

`neutralize`

`neutralize`

and then repeats.

Thus:

`1/7 = one excite tact followed by seven neutralize tacts`

## 57. Scheduler Phase Contribution

The floating phase reference assigns a scheduler-dependent phase contribution:

| Scheduler state | Phase push |
|---|---:|
| `commit` | `0.010` |
| `excite` | `0.006` |
| `free` | `0.003` |
| `balance` | `0.003` |
| `neutralize` | `0.003` |

These values are FRP reference coefficients.

They are not universal TR-EIF constants.

## 58. FRP Phase Velocity

The floating executable reference evaluates:

`v_theta_i[n] = 0.060 omega_i[n] + u_sched[n] + F_i[n]`

where:

- `omega_i[n]` is current retained frequency;
- `u_sched[n]` is scheduler phase push;
- `F_i[n]` is the current coupling field.

## 59. FRP Phase Update

The tact-by-tact phase update is:

`theta_i[n+1] = (theta_i[n] + v_theta_i[n]) mod 2 pi`

This is the operational discrete phase-evolution rule of the floating FRP reference.

## 60. Continuous and Operational Equations

The classical continuous phase equation:

`d theta_i / dt = ...`

and the FRP tact update:

`theta_i[n+1] = theta_i[n] + ...`

must not be identified as the same mathematical object.

The first is a continuous phase differential equation.

The second is the concrete discrete execution rule used by the reference processor.

## 61. No Hidden Time-Step Claim

The executable update does not introduce a separate explicit physical:

`Delta t`

inside the phase-update expression.

Its coefficients therefore belong to the tact-based reference realization.

They must not be interpreted automatically as continuous physical coefficients with undeclared units.

## 62. FRP Global Phase Order

After phase update, FRP computes:

`c[n] = (1/N) sum_i cos(theta_i[n])`

`s[n] = (1/N) sum_i sin(theta_i[n])`

and:

`R[n] = sqrt(c[n]^2 + s[n]^2)`

The implementation stores this quantity using field names associated with phase coherence.

Mathematically, it is the phase-order magnitude.

## 63. Phase-Order Naming Boundary

A field name containing:

`phase_coherence`

does not change the mathematical type of the quantity.

When the value is calculated only from:

`cos(theta_i)`

and:

`sin(theta_i)`

it is a phase-order diagnostic.

It does not independently establish full phase-amplitude or structural coherence.

## 64. Dyadic Multiscale Phase Order

FRP evaluates phase order at multiple hierarchy levels.

For hierarchy level:

`ell = 1, 2, ..., D`

the group size is:

`m_ell = 2^ell`

The cell population is divided into contiguous dyadic groups of that size.

## 65. Group Phase Order

For group `g` at level `ell`, define:

`R_ell,g = phase_order(Theta_ell,g)`

using the same complex phase-average magnitude as the global phase-order calculation.

## 66. Level Mean

For a level containing:

`G_ell`

groups, FRP evaluates:

`R_mean_ell = (1/G_ell) sum_g R_ell,g`

## 67. Level Minimum and Maximum

The implementation also retains:

`R_min_ell = min_g R_ell,g`

and:

`R_max_ell = max_g R_ell,g`

These preserve information hidden by the level mean.

## 68. Level Dispersion

For level mean:

`R_mean_ell`

the implementation evaluates:

`D_ell = sqrt((1/G_ell) sum_g (R_ell,g - R_mean_ell)^2)`

This provides a phase-order dispersion measure across groups.

## 69. Named Multiscale Levels

The reference exposes selected hierarchy levels as:

- pair-domain phase order;
- cluster phase order;
- supercluster phase order;
- global phase order.

These names identify levels within the dyadic hierarchy.

They do not create additional primitive mathematical state domains.

## 70. Local and Global Non-Equivalence

The multiscale implementation preserves the fact that:

`high global R ≠ identical local R`

and:

`high local R ≠ guaranteed high global R`

A global phase-order scalar therefore does not replace the hierarchy of local phase relations.

## 71. Phase Order and Coherence Support

Within FRP, phase-order quantities participate in the downstream operational coherence-support calculation.

The dependency is:

`phase trajectory`

`→ phase order`

`→ multiscale phase order`

`→ coherence-support projection`

The phase-order measure itself remains distinct from the resulting projection.

## 72. Nonlinear Coherence Compression

The FRP reference defines a coherence-support compression factor:

`kappa_C[n] = exp(-(3.0 q_mean[n]^2 + 1.5 m[n]^2))`

where:

- `q_mean[n]` is mean thermal overload;
- `m[n]` is the nonnegative soft-margin pressure term used by the implementation.

The exact variables and coefficients belong to the FRP reference model.

## 73. Effective Phase-Order Support

The compressed phase-order support is:

`R_eff[n] = R[n] kappa_C[n]`

The implementation names this quantity:

`effective_coherence`

Its mathematical construction remains a compressed phase-order support quantity.

## 74. Operational FRP Coherence Projection

The floating reference evaluates:

`C_FRP[n] = 0.82 + 0.34 R_eff[n] + 0.16 R_cluster_mean[n] + 0.08 f_0[n] - 0.10 L_mean[n]`

where:

- `R_eff[n]` is compressed global phase-order support;
- `R_cluster_mean[n]` is mean cluster phase order;
- `f_0[n]` is the fraction of cells currently in active neutral state `0`;
- `L_mean[n]` is mean retained frequency lag.

This is an operational processor projection.

It is not the universal definition of general TR-EIF structural coherence.

## 75. Operational Pressure Projection

The same reference defines:

`P_FRP[n] = heat[n] + switch_load[n]`

and evaluates:

`C_FRP[n] - P_FRP[n]`

as a processor-specific dynamic stability margin.

This relation remains separate from the classical Kuramoto order parameter.

## 76. Mandatory Separation of R and C

The following distinction is mandatory:

`R[n] ≠ C_FRP[n]`

and, more generally:

`R(t) ≠ C(t)`

`R`

is a phase-order magnitude.

`C_FRP`

is a composite operational projection containing phase-order support together with other state variables.

## 77. Phase-to-Ternary Mapping

The FRP executable reference contains an explicit phase-derived ternary target mapping.

For phase:

`theta_i`

define:

`x_i = sin(theta_i)`

The target is:

`1` when `x_i > 0.33`

`-1` when `x_i < -0.33`

`0` otherwise.

## 78. Reference Target Function

The FRP target mapping is therefore:

`Q_FRP(theta_i) = 1` if `sin(theta_i) > 0.33`

`Q_FRP(theta_i) = -1` if `sin(theta_i) < -0.33`

`Q_FRP(theta_i) = 0` otherwise

This mapping is a concrete reference implementation choice.

It is not a universal TR-EIF resonance threshold.

## 79. Active Zero Interval

Under this reference mapping, target:

`0`

corresponds to the interval satisfying:

`-0.33 ≤ sin(theta_i) ≤ 0.33`

The resulting `0` is a valid balanced ternary target.

It must not be described as missing, undefined, or passive.

## 80. Target Is Not Full Phase State

The mapping:

`theta_i → {-1,0,1}`

is many-to-one.

Therefore:

`Q_FRP(theta_a) = Q_FRP(theta_b)`

does not imply:

`theta_a = theta_b`

The continuous phase state remains separately retained.

## 81. Target Is Not Immediate Retained State

The phase-derived target does not authorize an illegal ternary transition.

If current state and target have opposite nonzero polarity, the target must be routed through active neutral state `0`.

Thus the phase module supplies a target.

The transition layer determines the admissible executed path.

## 82. Required Ternary Paths

The balanced ternary execution invariant remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

Direct:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

## 83. FRP Pending Route

When an opposite-polarity target is requested, FRP:

1. records the attempted opposite target;
2. executes the first leg into `0`;
3. retains the destination polarity as a pending route;
4. assigns the route a later readiness point;
5. completes the second leg only through a later admissible execution event.

The active neutral state is therefore an actual retained state.

## 84. Minimum Tick Separation

In the floating and fixed-point semantic reference, an opposite-polarity route created at tick:

`n`

is given readiness:

`n + 1`

Thus both state-changing legs cannot collapse into one semantic transition event.

## 85. Phase Evolution During Ternary Routing

The continuous resonant state and the retained ternary state remain different layers.

Consequently, the phase field can continue evolving while a cell occupies:

`0`

or while a pending destination is retained.

The active neutral state does not erase the resonant phase state.

## 86. Scheduler Transition Classes

At the retained-state execution boundary, the scheduler distinguishes two major transition capabilities.

Commit-capable scheduler states are:

`free`

`commit`

`excite`

Neutralize-capable scheduler states are:

`free`

`balance`

`neutralize`

## 87. Commit-Capable Transition Class

Commit-capable states admit transition classes including:

`0 → -1`

and:

`0 → 1`

as well as pending-route completion from active neutral state.

## 88. Neutralize-Capable Transition Class

Neutralize-capable states admit:

`-1 → 0`

and:

`1 → 0`

including the first leg required by an opposite-polarity route.

## 89. Scheduler and Phase Are Distinct Roles

The FRP scheduler therefore participates in two distinct interfaces:

1. upstream, it contributes a scheduler-dependent term to phase evolution;
2. downstream, the retained-state execution architecture uses scheduler state as a temporal eligibility operator for ternary transition classes.

These roles must not be collapsed into one operation.

## 90. FRP Reference Tick Ordering

The floating executable reference uses an explicit tact ordering.

At a high level:

`resolve scheduler state`

`→ reset current switch activity`

`→ process ready pending neutral routes`

`→ process explicit transition requests`

`→ derive and process automatic phase-based ternary targets`

`→ calculate switching load`

`→ update retained frequency dynamics`

`→ update thermal field`

`→ update local gamma drift`

`→ update thermal coupling factors`

`→ calculate phase coupling`

`→ update phase field`

`→ calculate multiscale phase order`

`→ update operational stability projection`

This ordering is part of the executable reference semantics.

## 91. Phase Target Temporal Boundary

Because automatic phase-derived targets are processed before the same tact's phase update, the target consumed during tact `n` is derived from the phase state available at the beginning of that target-evaluation stage.

The newly updated phase state becomes available for subsequent evaluation.

This prevents an undocumented same-stage algebraic loop.

## 92. RTL Boundary

The retained-state RTL layer receives a registered phase-derived ternary target from the upstream resonant-computation domain.

The RTL retained-state execution chain does not itself calculate:

- Kuramoto–Sakaguchi phase coupling;
- phase state;
- gamma drift;
- thermal phase attenuation;
- phase-order metrics;
- the phase-to-ternary target function.

This establishes a clear implementation boundary:

`nonlinear resonant field`

`→ registered ternary target`

`→ retained -1/0/1 execution`

## 93. TR-EIF Interpretation of the FRP Reference

The FRP realization provides an executable specialization of the more general TR-EIF interfaces.

The relation is:

`TR-EIF formal phase space`

`→ FRP phase-field specialization`

`→ FRP hierarchical Sakaguchi coupling`

`→ FRP tact-by-tact phase evolution`

`→ FRP phase-order diagnostics`

`→ FRP phase-derived ternary target`

`→ TR-EIF-compatible active-neutral ternary execution`

FRP therefore supplies an implementation reference.

It does not reduce TR-EIF to one processor implementation.

## 94. No Universalization of FRP Coefficients

The following current FRP values are implementation parameters:

- `gamma_nominal = 0.30 pi`;
- `alpha = 0.70`;
- `K_0 = 0.28`;
- frequency response coefficient `0.30`;
- state-frequency gain `0.06`;
- switching-frequency gain `0.12`;
- phase-frequency coefficient `0.060`;
- phase target threshold magnitude `0.33`;
- scheduler phase pushes `0.010`, `0.006`, and `0.003`;
- gamma-state response coefficient `0.15`;
- thermal gamma gain `0.08`;
- thermal coupling gain `2.50`.

A TR-EIF model using different validated parameters remains mathematically possible.

The provenance of its parameters must be explicit.

## 95. No Universal Atomic Interpretation

A TR-EIF phase variable must not automatically be identified with the literal physical phase of an atom.

A later EIF layer must define what interatomic object is mapped to the phase domain.

Possible mathematical carriers may include:

- atomic sites;
- local environments;
- interaction modes;
- latent equivariant features;
- collective modes;

only when the corresponding mapping is explicitly defined.

## 96. No Automatic Electron–Nucleus Resonance Claim

The presence of a Kuramoto–Sakaguchi phase module does not establish a mechanical resonance relation between an electron and a nucleus.

Atomic and electronic dynamics require their own physical state definitions and models.

## 97. No Automatic Bond Claim

A stable phase relation does not by itself establish a chemical bond.

Therefore:

`phase locking ≠ chemical bond`

and:

`resonance classification ≠ chemical bond`

## 98. No Automatic Force Claim

The phase-coupling field:

`F_i`

defined in this chapter is a phase-evolution contribution.

It must not be confused with an interatomic mechanical force.

The later EIF force layer requires a separately typed mapping.

## 99. No Automatic Energy Claim

The quantities:

`theta_i`

`gamma_i`

`R`

`K_0`

and:

`F_i`

are not automatically energy variables.

Any energy relation requires explicit dimensional definition.

## 100. No Automatic Physical Phase Transition Claim

Oscillator phase evolution and a physical material phase transition are not identical.

Therefore:

`oscillator phase change ≠ physical phase transition`

`resonance-window crossing ≠ physical phase transition`

`ternary transition ≠ physical phase transition`

A physical phase-transition claim requires its own order parameter, state definition, and evidence.

## 101. Classical-to-FRP Construction

The mathematical progression represented by this chapter is:

`classical relative-phase interaction`

`→ Sakaguchi phase lag`

`→ hierarchical weighted interaction`

`→ local thermal attenuation`

`→ local effective phase lag`

`→ retained frequency memory`

`→ tact-by-tact phase evolution`

`→ multiscale phase order`

`→ phase-derived ternary target`

The first two layers are classical foundations.

The subsequent specialization is the FRP executable reference realization.

## 102. Parameter Provenance Requirement

Every nonclassical numerical coefficient introduced into a TR-EIF model must identify its provenance.

Permitted provenance classes remain those established in Volume 01, including:

- `PRIMARY_SOURCE`;
- `DERIVED`;
- `CALIBRATED`;
- `AUTHOR_DEFINED`;
- `BENCHMARK`;
- `TEST_FIXTURE`;
- `REQUIRES_SOURCE`;
- `REQUIRES_TEST`.

FRP executable constants used as implementation-reference parameters must not be relabeled as independently established physical constants.

## 103. Numerical Phase Validation

A phase implementation must verify:

1. every stored phase is numerically finite;

2. phase wrapping preserves the declared circular representation;

3. every active frequency state is valid;

4. every coupling state is valid;

5. every effective phase lag is valid;

6. the active coupling path is declared;

7. every required history variable is present;

8. the phase update is deterministic when determinism is claimed.

## 104. Hierarchical Topology Validation

A model using the FRP dyadic specialization must verify:

- `N` is a power of two;
- `N ≥ 2`;
- hierarchy depth is consistent with `N`;
- diagonal coupling is zero;
- pair weights correspond to hierarchical distance;
- row normalization is preserved;
- dense and hierarchical representations agree within the declared numerical contract when equivalence is claimed.

## 105. Phase-Order Validation

For every phase-order calculation, validation must identify:

- phase population;
- group boundaries where applicable;
- population count;
- weighting;
- normalization;
- phase-state version.

A stale or differently sampled phase state must not be substituted silently.

## 106. Gamma-State Validation

A model using the FRP local phase-lag specialization must retain:

- nominal gamma;
- local effective gamma;
- local gamma state;
- local overload;
- update ordering.

This is required to reproduce the interaction term exactly.

## 107. Frequency-Memory Validation

A model using retained frequency relaxation must preserve:

- base frequency;
- target frequency;
- previous current frequency;
- response coefficient;
- current ternary state;
- current switch activity.

Without these quantities, the next retained frequency cannot be reproduced completely.

## 108. Scheduler Validation

A scheduler-aware phase execution must preserve:

- scheduler mode;
- scheduler state;
- tact index;
- scheduler phase contribution.

A scheduler-aware ternary execution must additionally preserve its transition-eligibility semantics.

## 109. Phase-to-Ternary Validation

The phase-derived target validator must verify:

- source phase state;
- sine evaluation;
- threshold value;
- target in `{-1,0,1}`;
- active-zero interval;
- target-generation ordering.

Target validation alone does not establish transition-path validity.

## 110. Transition-Boundary Validation

After the target is generated, ternary execution must independently verify:

- current retained state;
- target state;
- scheduler eligibility;
- capacity eligibility;
- active-neutral routing;
- pending-route state;
- final writeback.

The phase module therefore cannot authorize an illegal direct opposite-state event.

## 111. Deterministic Replay State

A complete deterministic replay of the FRP phase reference requires the result-affecting state, including where applicable:

- phase vector;
- base frequencies;
- target frequencies;
- current frequencies;
- retained ternary state;
- switch activity;
- thermal state;
- gamma state;
- pseudorandom generator state or seed;
- hierarchy;
- coupling parameters;
- scheduler mode and tact;
- pending routes;
- explicit requests.

## 112. Invalid Phase Input

An invalid phase value is not ternary state:

`0`

The phase evaluation must report or propagate invalidity according to the model contract.

## 113. Invalid Coupling Input

An invalid coupling coefficient is not equivalent to:

`K = 0`

unless a separate explicit recovery rule defines that transformation.

## 114. Invalid Frequency Input

An unavailable or invalid frequency state must not be silently replaced by the reference base value.

Validity and fallback behavior must remain separate.

## 115. Invalid Gamma Input

An invalid phase lag must not be silently interpreted as:

`gamma = 0`

because:

`gamma = 0`

is itself a valid model state with specific phase semantics.

## 116. Failure Is Not Desynchronization

Failure of the numerical phase module is not a valid synchronization result.

Therefore:

`solver or state failure ≠ desynchronization`

## 117. Failure Is Not Resonance Exit

Likewise:

`phase-module failure ≠ OUTSIDE resonance window`

unless a separate failure-handling mapping explicitly produces such a state after valid evaluation.

## 118. Failure Is Not Active Neutral

A phase failure must not be encoded silently as balanced ternary:

`0`

The active neutral state is a valid state of the ternary kernel.

## 119. Core Phase-Module Invariants

The following invariants are mandatory.

1. Phase remains a circular state.

2. Phase difference and phase lag remain distinct.

3. Phase lag and retained frequency memory remain distinct.

4. Classical Kuramoto dynamics remain distinguishable from Sakaguchi–Kuramoto dynamics.

5. Classical models remain distinguishable from FRP extensions.

6. The FRP coupling field preserves its declared hierarchical weighting.

7. The local effective phase lag belongs to the receiving cell in the current FRP realization.

8. Thermal coupling attenuation remains explicit.

9. Frequency target and current retained frequency remain distinct.

10. Retained frequency lag remains explicit.

11. The scheduler phase contribution remains distinguishable from the coupling field.

12. The tact-based FRP phase equation remains distinguishable from the classical continuous equation.

13. Global phase order remains distinct from the complete phase vector.

14. Multiscale phase order remains distinct from global phase order alone.

15. Phase order remains distinct from general structural coherence.

16. `R(t)` remains distinct from `C(t)`.

17. Phase-derived target remains distinct from retained ternary state.

18. The target domain remains exactly `-1/0/1`.

19. State `0` remains active.

20. Direct `-1 → 1` remains forbidden.

21. Direct `1 → -1` remains forbidden.

22. Opposite-state execution remains neutral-mediated.

23. Continuous phase state remains retained during neutral ternary routing.

24. Invalid data remain distinct from valid ternary `0`.

25. FRP implementation constants remain distinct from universal TR-EIF constants.

## 120. Formal Non-Equivalences

The following non-equivalences are mandatory:

`phase ≠ ternary state`

`phase difference ≠ phase lag`

`phase lag ≠ time delay`

`frequency target ≠ retained frequency`

`frequency lag ≠ propagation delay`

`coupling field ≠ mechanical force`

`phase order ≠ complete phase state`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

`R(t) ≠ resonance classifier`

`resonance classifier ≠ ternary target`

`ternary target ≠ executed state`

`active 0 ≠ missing data`

`active 0 ≠ failed phase computation`

`active 0 ≠ zero coupling`

`active 0 ≠ frozen phase`

`Kuramoto model ≠ TR-EIF`

`Sakaguchi–Kuramoto model ≠ TR-EIF`

`FRP implementation ≠ complete TR-EIF`

`phase locking ≠ resonance`

`resonance ≠ physical phase transition`

`phase coupling ≠ chemical bond`

## 121. Formal TR-EIF Phase Chain

The general TR-EIF chain established by this chapter is:

`phase-space state`

`→ relative-phase interaction`

`→ coupled phase dynamics`

`→ phase trajectory`

`→ local and global phase-order observables`

`→ resonance-coordinate mapping`

`→ resonance classification`

`→ balanced ternary target`

`→ admissible -1/0/1 transition`

The phase model supplies continuous-state information.

The ternary layer supplies constrained discrete execution.

## 122. FRP Executable Specialization

The corresponding FRP specialization is:

`theta_i[n]`

`+ retained omega_i[n]`

`+ hierarchical W_ij`

`+ thermal factors h_i[n]`

`+ local gamma_effective_i[n]`

`+ scheduler phase push`

`→ coupling field F_i[n]`

`→ phase velocity v_theta_i[n]`

`→ theta_i[n+1]`

`→ global and multiscale phase order`

`→ phase-derived target in -1/0/1`

`→ active-neutral retained-state execution`

This chain is directly grounded in the current executable FRP semantic implementation.

## 123. Interface to the EIF Layer

The phase module does not yet define how interatomic states become phase-domain inputs.

That mapping belongs to the Equivariant Interatomic Framework layer.

The later integration must therefore explicitly define a relation of the form:

`interatomic state`

`→ equivariant representation`

`→ phase/resonance state`

and, where feedback exists:

`ternary/resonance state`

`→ equivariant interatomic update`

No implicit conversion is permitted.

## 124. Interface Requirement for Atomic or Local Environments

If an EIF representation supplies one phase-domain state per atom, site, environment, or latent channel, it must define:

- carrier identity;
- source feature space;
- transformation behavior;
- phase mapping;
- coupling mapping;
- dimensional interpretation;
- locality;
- topology;
- information loss.

The phase module itself does not invent this mapping.

## 125. Equivariance Boundary

A later EIF layer may require the phase-input construction to respect transformations such as:

- translation;
- rotation;
- permutation;
- another declared symmetry action.

The present phase equation does not by itself prove those equivariance properties.

They must be established at the mapping boundary.

## 126. Minimal Classical Phase Contract

A classical phase-oscillator model used by TR-EIF must define:

- oscillator count;
- phase domain;
- phase state;
- intrinsic frequencies;
- coupling relation;
- phase-lag relation where used;
- initial state;
- evolution domain.

## 127. Minimal TR-EIF Phase Contract

A TR-EIF phase module must additionally define:

- relation to `X_R`;
- phase-derived observables;
- synchronization relation where claimed;
- coherence relation where claimed;
- history where required;
- ternary target mapping where used;
- feedback dependencies where used;
- parameter provenance;
- validation conditions.

## 128. Minimal FRP Reference Contract

A model claiming compatibility with the FRP phase specialization must additionally preserve the relevant implemented semantics:

- dyadic hierarchical topology;
- normalized fractal shell coupling;
- receiving-cell local effective gamma;
- thermal pair attenuation;
- retained frequency relaxation;
- scheduler phase contribution;
- tact-based phase update;
- phase-order calculation;
- multiscale dyadic phase-order calculation;
- explicit phase-to-ternary target mapping;
- active-neutral ternary boundary.

A model may implement only a declared subset, but it must not claim full FRP phase-reference equivalence when required components are absent.

## 129. Conformance Requirements

A mathematical phase model conforms to this chapter when:

- classical source equations are identified as classical;
- TR-EIF extensions are identified as author-defined;
- FRP implementation equations are identified as reference-realization equations;
- every symbol is typed;
- phase remains circular;
- phase lag remains distinct from delay;
- phase order remains distinct from general coherence;
- resonance remains distinct from synchronization;
- the balanced ternary domain remains exactly `-1/0/1`;
- the active neutral state remains valid and explicit;
- no continuous phase quantity is silently substituted for ternary state;
- no FRP implementation coefficient is presented as universal without independent evidence.

A computational realization conforms when:

- the declared update order is reproducible;
- phase wrapping is deterministic;
- hierarchical coupling is reproducible;
- frequency memory is reproducible;
- gamma state is reproducible;
- scheduler contribution is reproducible;
- phase-order outputs are reproducible;
- phase-derived ternary targets are reproducible;
- invalid data remain distinguishable from active neutral state;
- the downstream ternary execution preserves neutral-mediated opposite-state paths.

## 130. Final Phase-Oscillator Statement

TR-EIF uses coupled phase dynamics as one mathematical layer inside a larger hybrid architecture.

The classical basis is:

`Kuramoto relative-phase coupling`

and:

`Sakaguchi–Kuramoto phase-lag coupling`

The FRP executable reference specializes this basis through:

`dyadic hierarchical coupling`

`+ local thermal attenuation`

`+ local effective Sakaguchi lag`

`+ retained frequency memory`

`+ scheduler phase contribution`

`→ tact-by-tact phase evolution`

`→ global and multiscale phase order`

`→ phase-derived -1/0/1 target`

The balanced ternary kernel remains:

`-1/0/1`

with active:

`0`

and mandatory routes:

`-1 → 0 → 1`

`1 → 0 → -1`

The resulting architecture preserves the central separation:

`continuous resonant phase dynamics`

`≠`

`discrete balanced ternary execution`

while connecting the two through an explicit, reproducible phase-derived qualification boundary.

This phase module therefore establishes the concrete mathematical and executable bridge required before the Equivariant Interatomic Framework can map interatomic representations into the TR-EIF resonant domain.
