# Conservative Energy Functional

## 1. Purpose

This chapter defines the conservative energy functional of the Equivariant Interatomic Framework within TR-EIF.

The energy layer maps atomic, graph, equivariant, resonance, and ternary feature state into a scalar physical energy while preserving:

- spatial invariance;
- atom-permutation invariance;
- dimensional consistency;
- differentiability where force derivation requires it;
- explicit separation between representation state and physical energy;
- explicit separation between ternary state and energy;
- compatibility with force and stress derivation;
- deterministic evaluation semantics;
- provenance of analytic, learned, calibrated, and benchmark components.

The canonical chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy functional`

`→ forces and stress`.

---

## 2. Energy Functional

Let:

`X_conf`

be the atomic configuration space.

A conservative energy functional is:

`E: X_conf × X_aux → R`.

The auxiliary state may include explicitly declared:

- equivariant representations;
- resonance state;
- ternary feature channels;
- cell state;
- material parameters;
- global control parameters.

---

## 3. Scalar Output

Energy is a scalar physical quantity.

For rigid spatial transformation:

`g`

within the declared symmetry group:

`E(g · X) = E(X)`

when all relevant state variables transform consistently and no symmetry-breaking external field is held fixed.

---

## 4. Energy Units

Energy carries physical units.

A model must declare its energy unit system.

Examples may include:

- electronvolt;
- joule;
- another explicitly defined unit.

Internal latent features need not carry energy units unless explicitly assigned.

---

## 5. Energy Is Not Representation State

The invariant distinction is:

`equivariant representation ≠ energy`.

An invariant scalar hidden feature is not physical energy by identity.

---

## 6. Energy Is Not Resonance State

The invariant distinction is:

`resonance state ≠ energy`.

Resonance may condition the energy functional.

It is not energy itself.

---

## 7. Resonance Classification Is Not Energy

The distinction remains:

`resonance classification ≠ energy`.

A state classified as:

`INSIDE`

`BOUNDARY`

or:

`OUTSIDE`

does not numerically define energy.

---

## 8. Ternary State Is Not Energy

The invariant distinction is:

`ternary state ≠ energy`.

Values:

`-1`

`0`

`1`

are categorical ternary states.

They are not energy values.

---

## 9. Energy Input State

A general TR-EIF energy functional may be written:

`E = F_E(X_conf, X_G, X_EQ, X_R, X_T, X_global)`.

Only result-affecting state belongs in the concrete realization.

---

## 10. Reduced Energy Functional

When graph, representation, resonance, and ternary states are deterministic functions of the atomic configuration and model parameters, the complete composition may be written conceptually as:

`E = E(R, A, H, PBC; phi)`.

The internal state decomposition remains semantically preserved.

---

## 11. Conservative Force Relation

For differentiable energy:

`E(R)`

the force on atom:

`i`

is:

`F_i = -grad_(r_i) E`.

This relation defines the conservative force path.

---

## 12. Force Units

Force carries:

`energy / length`

units.

Dimensional consistency must be preserved through coordinate differentiation.

---

## 13. Energy Gradient

The gradient:

`grad_(r_i) E`

is a polar vector with respect to atomic coordinate:

`r_i`.

---

## 14. Force Equivariance

For rotation:

`Q`

and invariant energy:

`E(QR) = E(R)`,

the conservative force transforms:

`F_i(QR) = Q F_i(R)`

under the applicable assumptions.

---

## 15. Translation Invariance

For an isolated internal energy:

`E(R + c) = E(R)`.

A global translation does not change internal energy.

---

## 16. Translation Invariance and Net Internal Force

Differentiating translation invariance gives:

`sum_i F_i = 0`

for the conservative internal force model under the corresponding assumptions.

---

## 17. Rotation Invariance

For rigid rotation:

`Q`

the energy satisfies:

`E(QR) = E(R)`.

This is distinct from energy invariance under general deformation.

---

## 18. Reflection Invariance

If the model is:

`O(3)`

invariant:

`E(QR) = E(R)`

also holds for:

`det(Q) = -1`.

If only:

`SO(3)`

symmetry is intended, reflection behavior must be separately defined.

---

## 19. Permutation Invariance

For an admissible species-preserving atom permutation:

`pi`

the energy satisfies:

`E(pi · X) = E(X)`.

---

## 20. Periodic-Image Invariance

Equivalent periodic images of the same physical configuration must produce the same energy under the declared periodic boundary contract.

---

## 21. Energy and Cell State

For periodic systems:

`E = E(R, H, A, ...)`.

The cell matrix:

`H`

belongs to energy input state when energy depends on periodic geometry.

---

## 22. Rigid Cell Rotation

If:

`H' = QH`

and:

`R' = QR`

then rigid rotation must preserve scalar energy under the declared symmetry.

---

## 23. Cell Deformation

A deformation:

`H → H'`

that changes the cell metric is not a rigid E(3) transformation.

Energy may change under deformation.

---

## 24. Energy and Strain

A strain parameter:

`epsilon`

may enter through cell or coordinate deformation.

The energy derivative with respect to strain provides one route toward stress.

---

## 25. Stress Interface

A stress tensor may be derived from an energy derivative with respect to strain or cell deformation according to the declared mechanical convention.

The exact stress formula is developed in Chapter 09.

---

## 26. Energy Decomposition

A model may decompose total energy:

`E = sum_i E_i`.

Here:

`E_i`

is a local atomic energy contribution.

---

## 27. Local Atomic Energy

A local contribution may be:

`E_i = F_E,local(h_i, r_i, t_i, ...)`.

It must be a scalar invariant.

---

## 28. Local Energy Nonuniqueness

The decomposition:

`E = sum_i E_i`

need not be unique.

Only the total energy is necessarily a physically defined scalar under the model.

---

## 29. Pair Energy

A pairwise model may use:

`E = sum_(i<j) E_ij`.

The counting convention must be explicit.

---

## 30. Directed Edge Energy

A directed graph representation may instead compute edge terms for:

`j → i`.

If both directions are included, pair double counting must be handled explicitly.

---

## 31. Many-Body Energy

TR-EIF does not restrict energy to pairwise interactions.

A local energy may depend on the full many-body environment:

`E_i = F_E(E_i,local)`.

---

## 32. Graph-Based Energy

A graph-based functional may use:

`E = F_E(G, H_node, H_edge, H_global)`.

Graph state remains computational input.

It is not energy by identity.

---

## 33. Message-Passed Energy Representation

A final message-passed node representation:

`h_i^[L]`

may feed a scalar head:

`E_i = H_E(h_i^[L])`.

---

## 34. Energy Head

An energy head maps representation state to a scalar with energy semantics:

`H_E: X_EQ → R_energy`.

---

## 35. Scalar Invariance of Energy Head

The energy head must terminate in an invariant scalar channel.

---

## 36. Energy Head versus Generic Scalar Head

A generic scalar predictor is not an energy functional unless:

- output semantics are energy;
- units are declared;
- symmetry is correct;
- force relation is defined where conservative force is claimed.

---

## 37. Resonance-Conditioned Energy

A general model may use:

`E = F_E(X_EQ, X_R)`.

Resonance state conditions the energy mapping.

---

## 38. Local Resonance-Conditioned Energy

A local contribution may be:

`E_i = F_E(h_i, r_i)`.

Here:

`r_i`

is local resonance state.

---

## 39. Global Resonance-Conditioned Energy

A global resonance descriptor may condition all local energy heads or a global correction term.

---

## 40. Multiscale Resonance Energy

A multiscale energy model may consume:

`r^(atom)`

`r^(cluster)`

`r^(global)`.

Each input remains separately typed.

---

## 41. Resonance State Does Not Add Energy by Identity

A numerical resonance coordinate cannot be added directly to physical energy unless a dimensional mapping converts it to an energy contribution.

---

## 42. Ternary-Conditioned Energy

A general model may use:

`E = F_E(X_EQ, X_R, X_T)`.

---

## 43. Ternary Scalar Conditioning

A ternary feature may select or modulate model parameters.

For example:

`phi_E = F_phi(t)`.

This does not make:

`t`

an energy value.

---

## 44. Mode-Specific Energy Functions

A model may define:

`E_-1(X)`

`E_0(X)`

`E_1(X)`.

The active energy function is selected by a declared ternary channel.

---

## 45. Piecewise Energy Functional

A piecewise functional may be:

`E(X,t) = E_t(X)`.

Such a construction may be discontinuous when:

`t`

changes unless continuity constraints are imposed.

---

## 46. Continuous Ternary Conditioning

An alternative may blend mode-dependent parameters through a transformation that preserves exact ternary semantic input but continuous energy output.

---

## 47. Active Neutral Energy Mode

The state:

`0`

may select a distinct energy mapping:

`E_0`.

The neutral mode need not correspond to zero energy.

---

## 48. Ternary Zero Is Not Zero Energy

The invariant remains:

`ternary 0 ≠ energy 0`.

---

## 49. Negative Ternary State Is Not Negative Energy

Likewise:

`ternary -1 ≠ negative energy`.

---

## 50. Positive Ternary State Is Not Positive Energy

Likewise:

`ternary 1 ≠ positive energy`.

---

## 51. Target-Conditioned Energy

A model may use:

`t_target`

to condition energy.

This is distinct from conditioning on:

`t_exec`.

---

## 52. Execution-Conditioned Energy

A model may use:

`t_exec`

as the active energy-mode state.

---

## 53. Target versus Executed Energy Conditioning

The two architectures are different.

The model must explicitly state which channel influences energy.

---

## 54. Pending-Route Energy Conditioning

A pending route state may participate in energy conditioning if explicitly defined.

The pending destination remains separate from executed state.

---

## 55. Scheduler-Conditioned Energy

A scheduler state may influence a computational energy path in a hybrid implementation.

Scheduler state remains separate from physical energy.

---

## 56. Conservative Energy and Discrete Mode

A hybrid conservative model may be conservative within each fixed ternary mode while switching among mode-dependent energy surfaces.

The switching semantics must be separately defined.

---

## 57. Hybrid Energy Surface

Let:

`E_q(R)`

be an energy surface for:

`q ∈ {-1,0,1}`.

The executed mode determines the active surface under an execution-conditioned model.

---

## 58. Surface Switching

When:

`t_exec`

changes, the active energy functional may change.

This is a hybrid model event.

---

## 59. Surface Switching Is Not Atomic Structural Transition

The distinction remains:

`energy-mode switch ≠ structural transition`.

A structural change requires separately defined structural state.

---

## 60. Energy Surface Crossing

Equality:

`E_a(R) = E_b(R)`

between two model surfaces does not automatically define:

- resonance;
- ternary transition;
- bifurcation;
- physical phase transition.

---

## 61. Energy Minimum

A local minimum:

`R_star`

satisfies:

`grad_R E(R_star) = 0`

and the applicable second-order conditions.

---

## 62. Stationary Point

A stationary configuration satisfies:

`grad_R E = 0`.

It may be:

- minimum;
- maximum;
- saddle;
- degenerate stationary point.

---

## 63. Energy Minimum versus Stability

A local energy minimum may correspond to local mechanical stability under appropriate assumptions.

The exact stability relation depends on constraints and dynamical model.

---

## 64. Energy Minimum versus Resonance

The distinction remains:

`energy minimum ≠ resonance state`.

---

## 65. Energy Minimum versus Ternary Neutral

The distinction remains:

`energy minimum ≠ ternary 0`.

---

## 66. Hessian

The energy Hessian is:

`H_E = d^2 E / dR^2`

under the selected coordinate representation.

---

## 67. Hessian Symmetry

For sufficiently smooth scalar energy:

`H_E`

is symmetric under ordinary equality of mixed partial derivatives.

---

## 68. Hessian and Local Curvature

The Hessian encodes local curvature of the energy surface.

---

## 69. Hessian versus Interaction Graph

A nonzero Hessian block does not by identity define an interaction graph edge.

---

## 70. Hessian versus Resonance Coupling

Likewise:

`energy Hessian coupling ≠ resonance coupling`.

---

## 71. Normal Modes

For a mass-weighted Hessian near a stable equilibrium, eigenvectors may define harmonic normal modes under the applicable approximation.

---

## 72. Normal Mode versus Oscillator Phase

A normal-mode coordinate is not oscillator phase by identity.

---

## 73. Normal Mode versus Resonance

A normal mode may contribute to resonance parameterization.

It does not define resonance universally.

---

## 74. Conservative Force

A force field is conservative if there exists a scalar potential energy:

`E`

such that:

`F = -grad E`

on the declared domain under the applicable regularity and topology assumptions.

---

## 75. Equivariant Force versus Conservative Force

The distinction remains:

`equivariant force ≠ conservative force`.

A vector field may transform correctly without being derivable from a scalar potential.

---

## 76. Direct Force Model

A model may predict:

`F_direct`.

If no scalar:

`E`

is defined such that:

`F_direct = -grad E`,

the force model is not conservative under this definition.

---

## 77. Conservative Energy Contract

A model claiming conservative force must define:

1. scalar energy;
2. coordinate dependence;
3. differentiability;
4. force derivative;
5. unit consistency;
6. symmetry;
7. boundary/domain assumptions.

---

## 78. Energy Differentiability

Force derivation requires energy differentiability with respect to atomic coordinates over the applicable domain.

---

## 79. Graph Cutoff Differentiability

A hard graph cutoff can introduce discontinuities in energy if edge appearance/removal changes contributions discontinuously.

---

## 80. Smooth Cutoff Energy

A smooth cutoff may be used to make local energy contributions approach zero continuously at the interaction boundary.

---

## 81. Derivative Continuity

If smooth force is required, the energy cutoff should possess the necessary derivative continuity.

The required order depends on the intended numerical and physical model.

---

## 82. Hard Ternary Conditioning and Differentiability

If:

`t`

changes discretely and selects different energy functions, energy may be nonsmooth across ternary switching events.

This is part of the hybrid model.

---

## 83. Differentiability within Fixed Ternary Mode

Each:

`E_q(R)`

may remain differentiable with respect to:

`R`

for fixed:

`q`.

---

## 84. Discrete Switch Boundary

The ternary switching event is not a derivative with respect to coordinate by identity.

It is a separate discrete state change.

---

## 85. Target Switching versus Energy Switching

If energy uses executed state:

`t_exec`,

a change in:

`t_target`

does not change the active energy surface until execution commits.

---

## 86. Neutral-Mediated Energy Switching

For execution-conditioned energy, opposite energy-mode switching follows:

`E_-1`

`→ E_0`

`→ E_1`

or the reverse according to committed state.

---

## 87. No Direct Opposite Energy-Mode Commit

If the active energy mode is keyed directly to:

`t_exec`,

then committed opposite mode switching inherits:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

---

## 88. Energy Continuity across Neutral Route

A specialization may impose continuity conditions between:

`E_-1`

`E_0`

and:

`E_1`.

Such continuity is model-specific and must be defined explicitly.

---

## 89. Energy Discontinuity

A hybrid model may permit discrete energy-function changes.

The resulting physical interpretation and numerical integration semantics must be explicit.

---

## 90. Energy Conservation

For an isolated conservative system with time-independent potential and appropriate equations of motion, total mechanical energy may be conserved under the continuous dynamics.

This property belongs to the complete dynamical model.

---

## 91. Potential Energy versus Total Energy

The interatomic functional:

`E(R)`

may represent potential energy.

Total mechanical energy may additionally include kinetic energy.

---

## 92. Kinetic Energy

For masses:

`m_i`

and velocities:

`v_i`:

`K = 1/2 sum_i m_i ||v_i||^2`.

---

## 93. Total Mechanical Energy

A classical total mechanical energy may be:

`H = K + E`.

---

## 94. Conservative Energy versus Hamiltonian

The potential energy functional:

`E`

is not necessarily the complete Hamiltonian.

---

## 95. Energy Conservation versus Numerical Conservation

The exact continuous model may conserve energy while a numerical integrator introduces drift.

The distinction remains:

`mathematical conservation ≠ numerical conservation`.

---

## 96. Energy Drift

For numerical trajectory:

`E_n`

a drift may be measured relative to a reference value.

The metric must be defined.

---

## 97. Relative Energy Drift

A numerical metric may be:

`delta_E = |E_n - E_0| / max(|E_0|, epsilon_ref)`.

The exact metric is implementation-specific.

---

## 98. Symplectic Integration Interface

Volume 05 may use symplectic or other structure-preserving integrators.

Integrator choice is separate from the energy functional itself.

---

## 99. Energy Offset

Adding a constant:

`C`

to energy:

`E'(R) = E(R) + C`

does not change conservative forces.

---

## 100. Energy Gauge Offset

The absolute zero of potential energy may therefore be arbitrary under many models.

The chosen reference must remain explicit when absolute energy comparison is used.

---

## 101. Force Invariance under Energy Offset

Because:

`grad C = 0`,

forces satisfy:

`F_i' = F_i`.

---

## 102. Energy Reference

Training datasets may use different energy references.

Reference alignment belongs to data and learning contracts.

---

## 103. Per-Atom Energy Offset

Species-dependent reference energies may be used in atomistic learning models.

Their role must be explicit.

---

## 104. Species Reference Energy

A decomposition may include:

`E_ref = sum_i epsilon_ref(a_i)`.

The residual model then predicts the remaining interaction contribution.

---

## 105. Reference Energy and Forces

A constant species-only reference does not contribute to coordinate forces.

---

## 106. Energy Extensivity

For separated noninteracting subsystems:

`A`

and:

`B`,

an extensive energy model may satisfy:

`E(A ∪ B) = E(A) + E(B)`.

The required separation conditions must be explicit.

---

## 107. Size Extensivity

Sum of local atomic contributions naturally supports size-extensive scaling when interactions remain local under the model assumptions.

---

## 108. Intensive versus Extensive Outputs

Energy is generally extensive.

Energy per atom is an intensive or normalized derived quantity only under a declared convention.

---

## 109. Energy per Atom

Define:

`E_atom = E / N`

for:

`N > 0`.

This is distinct from total energy.

---

## 110. Energy Density

An energy density may be defined per volume:

`u = E / V`

under a declared physical interpretation.

---

## 111. Local Energy Density

A local energy-density assignment is not unique in general.

Its definition must be explicit.

---

## 112. Long-Range Energy

A complete energy model may contain:

`E = E_local + E_long`.

---

## 113. Local Energy

`E_local`

may be represented through finite-cutoff message passing.

---

## 114. Long-Range Electrostatic Energy

A long-range electrostatic model may require separate charge and boundary-condition treatment.

Its specific form belongs to the concrete specialization.

---

## 115. Dispersion Energy

Long-range dispersion may likewise require a separate functional.

---

## 116. Hybrid Energy Decomposition

A model may use:

`E = E_local + E_long + E_global + E_TR`.

Here:

`E_TR`

may denote a ternary/resonance-conditioned correction if explicitly defined.

---

## 117. Energy-Term Semantics

Every additive term must define:

- units;
- state dependence;
- symmetry;
- provenance;
- double-counting relation.

---

## 118. Double Counting

Two model terms must not count the same physical contribution twice unless that decomposition is intentionally defined.

---

## 119. Baseline plus Correction

A model may use:

`E = E_base + Delta E`.

The correction may depend on resonance or ternary state.

---

## 120. Residual Energy Learning

A learned model may predict:

`Delta E`

relative to an analytic baseline.

---

## 121. Analytic Baseline

An analytic baseline may encode known short-range, long-range, or reference-state physics.

---

## 122. Learned Energy Functional

A learned energy model may be:

`E = F_E(X; phi_E)`.

The parameter set:

`phi_E`

is learned from reference data.

---

## 123. Hybrid Analytic-Learned Energy

A model may combine analytic and learned terms.

Each term retains its own provenance.

---

## 124. Energy Parameterization

Energy-model parameters may include:

- embedding parameters;
- radial basis parameters;
- tensor-product weights;
- resonance coupling coefficients;
- ternary-conditioned parameters;
- reference energies.

---

## 125. Parameter Units

Any parameter with physical dimensional role must have declared units.

---

## 126. Parameter Sharing

Parameters may be shared across:

- atoms;
- species;
- edges;
- relation types;
- scales.

---

## 127. Species-Dependent Energy Parameters

A model may use species-specific energy terms.

---

## 128. Pair-Dependent Energy Parameters

Parameters may depend on species pair.

---

## 129. Environment-Adaptive Energy Parameters

A parameter may be generated dynamically from local invariant state.

Such a parameter becomes state-dependent model output.

---

## 130. Energy Functional and External Field

An external scalar or vector field may contribute to energy.

The field and its transformation law must be part of the model state.

---

## 131. External Position-Dependent Potential

A potential:

`V_ext(r_i)`

breaks global translation invariance unless the external potential is transformed with the system.

---

## 132. External Vector Field

A coupling to vector field may reduce rotational symmetry if the field is fixed in the laboratory frame.

---

## 133. Residual Symmetry

The energy functional must be invariant under the actual residual symmetry group of the complete state.

---

## 134. Energy and Charge

If charges:

`q_i`

are included, the energy functional may depend on them.

Charge remains scalar under spatial transformations.

---

## 135. Variable Charge

A model may predict environment-dependent charges.

Then charge prediction and energy evaluation form a coupled architecture.

---

## 136. Charge Conservation

If total charge is constrained, the charge model must preserve the declared total-charge condition.

This is separate from energy conservation.

---

## 137. Magnetic or Spin State

If magnetic or spin degrees of freedom are included, their transformation law must be explicit.

They are not automatically scalar node features.

---

## 138. Energy Domain

Let:

`D_E`

denote the admissible energy-model domain.

It may restrict:

- species;
- composition;
- geometry;
- density;
- cell state;
- charge state;
- resonance state;
- ternary state.

---

## 139. Out-of-Domain Input

An out-of-domain state must be represented explicitly.

It is not active neutral.

---

## 140. Invalid Energy Input

Non-finite or invalid upstream state must not silently produce a physically interpreted energy.

---

## 141. NaN Energy

A non-finite energy output is an invalid numerical result.

It is not a ternary state.

---

## 142. Infinite Energy

Some analytic potentials may diverge as interatomic distance approaches an excluded configuration.

The admissible domain must define such singular behavior.

---

## 143. Collision Singularity

A short-range repulsive term may diverge as:

`d_ij → 0`.

This is a property of the selected energy model.

---

## 144. Regularized Energy

A model may regularize short-range singularities.

The regularization must be explicitly documented.

---

## 145. Energy Smoothness

The energy functional may be required to have:

- continuity;
- first derivatives;
- second derivatives

over the intended domain.

The required smoothness depends on downstream use.

---

## 146. Force Training Requirement

Energy-force training requires differentiability with respect to coordinates.

---

## 147. Stress Training Requirement

Stress training may require differentiability with respect to cell or strain variables.

---

## 148. Hessian or Phonon Requirement

Second-derivative applications require sufficient smoothness of the energy functional.

---

## 149. Energy Training Target

Reference energy values may be used in Volume 04 optimization.

The energy objective remains separate from force and stress objectives.

---

## 150. Energy Loss

A generic energy loss may compare:

`E_pred`

and:

`E_ref`.

The exact loss functional belongs to Volume 04.

---

## 151. Force Loss

A force loss compares coordinate derivatives or force outputs.

---

## 152. Stress Loss

A stress loss compares tensor outputs.

---

## 153. Multi-Objective Training

Energy, force, and stress terms may be optimized jointly.

Weighting among them is a learning-layer choice.

---

## 154. Conservative Consistency

When forces are derived from the same energy used for training, energy-force consistency is structural.

---

## 155. Separate Direct Force Head

If a separate force head is used alongside energy, consistency between the two requires an explicit additional constraint.

---

## 156. Energy/Force Consistency Residual

A residual may compare:

`F_direct`

with:

`-grad E`.

---

## 157. Integrability

For a direct force field to admit a scalar potential on a suitable simply connected domain, the applicable integrability conditions must hold.

---

## 158. Curl-Free Condition Boundary

In ordinary Euclidean coordinates, a conservative field satisfies the corresponding zero-curl/integrability relations under applicable assumptions.

This is separate from E(3) equivariance.

---

## 159. Conservativity versus Equivariance

The framework preserves:

`conservativity ≠ equivariance`.

Both may be required.

Neither substitutes for the other.

---

## 160. Conservative Energy versus Resonance

The existence of a conservative energy does not define resonance state.

---

## 161. Conservative Energy versus Ternary Routing

The existence of a conservative energy does not alter the canonical ternary transition graph.

---

## 162. Energy and Scheduler

Scheduler state belongs to execution control.

It does not enter physical energy unless a hybrid model explicitly defines such dependence.

---

## 163. Energy and Pending Route

Pending route state may condition a hybrid energy mapping only if explicitly declared.

---

## 164. Neutral-State Energy

An active-neutral executed state may select an energy function:

`E_0`.

The state:

`0`

remains semantically active.

---

## 165. Neutral-State Energy Is Not Zero

The framework preserves:

`E_0 ≠ 0`

by identity.

Its value is determined by the energy model.

---

## 166. Opposite Route and Energy State

If energy depends on executed ternary state, an opposite route changes active energy mode in two committed legs.

---

## 167. First-Leg Energy Mode

For:

`-1 → 0`

the active mode becomes:

`E_0`.

---

## 168. Second-Leg Energy Mode

For:

`0 → 1`

the active mode becomes:

`E_1`.

---

## 169. Reverse Route Energy Modes

Likewise:

`E_1 → E_0 → E_-1`

for:

`1 → 0 → -1`.

---

## 170. No Direct Executed Energy-Mode Reversal

The energy-mode sequence cannot skip the neutral mode when keyed to canonical:

`t_exec`.

---

## 171. Target Energy Prediction

A model may evaluate hypothetical energy under:

`t_target`

without committing execution.

This is a prediction branch.

It must remain distinct from active executed energy state.

---

## 172. Counterfactual Energy

A model may compute:

`E(R, q)`

for multiple hypothetical:

`q`.

These are counterfactual mode energies.

They do not change:

`t_exec`.

---

## 173. Energy-Based Target Decision

A specialization may use energy differences to construct a ternary target.

The decision mapping must be explicit.

---

## 174. Energy Difference

For modes:

`a`

and:

`b`

define:

`Delta E_ab = E_a - E_b`.

This is an energy-valued scalar.

---

## 175. Energy Difference versus Ternary State

A sign of:

`Delta E`

does not automatically define:

`-1/0/1`

without an explicit classifier.

---

## 176. Energy-Based Neutral Region

A target map may define a neutral band around:

`Delta E = 0`.

The band is a decision region.

Its semantics must be explicit.

---

## 177. Energy Crossing versus Bifurcation

The distinction remains:

`energy crossing ≠ bifurcation`.

---

## 178. Energy Crossing versus Physical Phase Transition

Likewise:

`energy crossing ≠ physical phase transition`

without the corresponding thermodynamic construction.

---

## 179. Potential Energy Surface

For fixed species and other discrete state, the energy functional defines a potential energy surface over atomic coordinates.

---

## 180. Multiple Energy Surfaces

Ternary or electronic discrete state may define a family of potential energy surfaces.

The coupling among them must be explicit.

---

## 181. Surface Label versus Physical Phase

An energy-surface label is not a thermodynamic phase by identity.

---

## 182. Energy Barrier

An energy barrier is defined relative to an energy path or transition-state construction.

---

## 183. Energy Barrier versus Neutral State

The active-neutral ternary state is not an energy barrier by identity.

---

## 184. Minimum-Energy Path

A minimum-energy path is defined relative to:

`E(R)`.

It is a geometric path selected by an energy criterion.

---

## 185. Reaction Coordinate

A reaction coordinate may parameterize a path on the energy landscape.

It remains distinct from resonance coordinates unless explicitly related.

---

## 186. Resonance Coordinate versus Reaction Coordinate

The distinction remains:

`resonance coordinate ≠ reaction coordinate`.

---

## 187. Energy Landscape versus Resonance Landscape

A resonance-state landscape and potential-energy landscape may both be defined.

They are different mathematical objects.

---

## 188. Energy Curvature versus Resonance Width

The curvature of:

`E`

near a minimum is not resonance-window width by identity.

---

## 189. Energy Hessian versus Coherence

The Hessian does not equal coherence.

---

## 190. Energy and Phase Dynamics

A later coupled model may allow phase or resonance state to modulate energy.

The phase-coupling equation itself is not a mechanical force law.

---

## 191. Phase Coupling versus Energy Gradient

The invariant remains:

`phase coupling ≠ energy gradient`.

---

## 192. Oscillator Phase versus Atomic Coordinate

The distinction remains:

`oscillator phase ≠ atomic position`.

---

## 193. Energy Trace

An energy trace may contain:

- physical time;
- numerical step;
- total energy;
- local energy contributions;
- energy terms;
- ternary mode;
- resonance state;
- cell state;
- provenance.

---

## 194. Energy Component Trace

A decomposed trace may record:

`E_local`

`E_long`

`E_res`

`E_ternary`

or other declared terms.

The decomposition must match the actual model.

---

## 195. Force Trace

A force trace belongs to the output layer and may be paired with energy traces for consistency tests.

---

## 196. Stress Trace

Stress traces may likewise accompany cell-dependent energy evaluation.

---

## 197. Energy Determinism

A deterministic energy model produces identical declared output for identical:

- complete atomic state;
- graph;
- representation;
- resonance state;
- ternary state;
- parameters;
- arithmetic semantics.

---

## 198. Energy Replay

A deterministic replay may require exact or tolerance-based agreement according to the numerical contract.

---

## 199. Exact Categorical Conditioning

Any ternary conditioning state must compare exactly.

---

## 200. Continuous Energy Comparison

Floating-point energy may be compared within declared tolerance unless byte-identical replay is required.

---

## 201. Energy Serialization

A serialized energy artifact must include:

- value;
- units;
- configuration identifier;
- model identifier;
- relevant state coordinates;
- provenance.

---

## 202. Energy Schema

The schema must distinguish:

- total energy;
- local contribution;
- reference energy;
- residual energy;
- uncertainty;
- invalid state.

---

## 203. Invalid Energy State

An invalid energy result must not be encoded as:

`0`

without explicitly meaning zero physical energy.

---

## 204. Zero Energy

Physical energy value:

`0`

is a valid scalar numeric value under a selected reference.

It is not ternary active neutral.

---

## 205. Zero Energy versus Neutral State

The framework preserves:

`energy 0 ≠ ternary 0`.

---

## 206. Energy Validation

An energy validator may check:

- finite output;
- units;
- permutation invariance;
- translation invariance;
- rotation invariance;
- reflection invariance where applicable;
- periodic equivalence;
- deterministic replay.

---

## 207. Translation Invariance Test

Translate all atomic positions by:

`c`.

For an internal isolated energy:

`E(R+c) = E(R)`.

---

## 208. Rotation Invariance Test

Rotate positions and cell consistently:

`E(QR, QH) = E(R,H)`.

---

## 209. Reflection Invariance Test

If:

`O(3)`

invariance is declared:

`E(QR) = E(R)`

for improper orthogonal:

`Q`.

---

## 210. Permutation Invariance Test

Permuting equivalent atoms must preserve energy.

---

## 211. Periodic Equivalence Test

Equivalent periodic representations must produce equal energy under the declared numerical tolerance.

---

## 212. Energy Offset Test

Adding a constant reference offset should leave forces unchanged.

---

## 213. Finite-Difference Force Test

A coordinate finite difference may verify:

`F_i ≈ -grad_(r_i) E`.

The perturbation size and numerical tolerance must be explicit.

---

## 214. Automatic-Differentiation Force Test

When automatic differentiation is used, force may be compared against an independent numerical derivative or fixture.

---

## 215. Translation/Force Consistency Test

For internal conservative forces:

`sum_i F_i`

should satisfy the declared numerical tolerance around zero.

---

## 216. Rotation/Force Equivariance Test

Rotate the configuration and verify:

`F_i(QR) = QF_i(R)`.

---

## 217. Stress Consistency Test

Where stress is derived from energy, compare against finite cell/strain perturbations under the declared convention.

---

## 218. Energy Continuity Test

If continuity is required at a cutoff or switching boundary, controlled fixtures should verify it.

---

## 219. Force Continuity Test

If force continuity is required, derivative behavior across the same boundary must also be tested.

---

## 220. Ternary-Mode Energy Test

For ternary-conditioned energy, evaluate:

`E_-1`

`E_0`

`E_1`

on controlled identical geometric input.

---

## 221. Neutral Energy Test

Verify that:

`t = 0`

selects the declared neutral energy behavior rather than a missing-state path.

---

## 222. Target/Execution Conditioning Test

If the energy model uses:

`t_exec`,

changing only:

`t_target`

must not change energy unless another declared coupling exists.

---

## 223. Pending-State Conditioning Test

If pending state participates in energy, test it independently of target and execution state.

---

## 224. Direct-Opposite Execution Test

An opposite target must not cause direct energy-mode commit from:

`E_-1`

to:

`E_1`

when energy is keyed to executed ternary state.

---

## 225. Energy Conservation Test

For an isolated conservative MD fixture, total mechanical energy may be evaluated under a suitable integrator and timestep.

The test belongs to the complete dynamics layer.

---

## 226. Energy Drift Benchmark

A numerical benchmark may report energy drift over a declared trajectory duration.

---

## 227. Energy Provenance

Energy terms, parameters, and artifacts may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 228. Primary-Source Energy Term

An analytic energy term adopted directly from a cited physical model carries:

`PRIMARY_SOURCE`.

---

## 229. Derived Energy Quantity

A total or transformed energy quantity derived from declared terms may carry:

`DERIVED`.

---

## 230. Author-Defined Energy Coupling

A TR-EIF-specific coupling between:

- equivariant state;
- resonance state;
- ternary channels;
- energy

carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 231. Calibrated Energy Parameter

A fitted energy parameter carries:

`CALIBRATED`.

---

## 232. Benchmark Energy Result

Measured energy error, drift, throughput, or scaling behavior may carry:

`BENCHMARK`.

---

## 233. Energy Test Fixture

Controlled atomic configurations with expected energy/force relations carry:

`TEST_FIXTURE`.

---

## 234. Energy Extension Rule

Any energy functional must define:

1. input state;
2. output units;
3. spatial symmetry;
4. permutation behavior;
5. periodic behavior;
6. differentiability;
7. decomposition;
8. ternary/resonance conditioning where present;
9. provenance;
10. validation.

---

## 235. Local Energy Extension Rule

Any local energy decomposition must define:

1. locality;
2. neighborhood;
3. local representation;
4. aggregation;
5. extensive scaling;
6. double-counting convention.

---

## 236. Long-Range Energy Extension Rule

Any long-range contribution must define:

1. physical interaction;
2. boundary conditions;
3. solver or representation;
4. units;
5. coupling to local energy;
6. double-counting treatment.

---

## 237. Ternary-Conditioned Energy Extension Rule

Any ternary-conditioned energy model must define:

1. source ternary channel;
2. target or executed state usage;
3. `-1` behavior;
4. `0` behavior;
5. `1` behavior;
6. continuity or discontinuity;
7. force derivation;
8. switching order.

---

## 238. Resonance-Conditioned Energy Extension Rule

Any resonance-conditioned energy model must define:

1. resonance source;
2. resonance transformation type;
3. energy coupling;
4. units;
5. scale;
6. differentiability;
7. feedback.

---

## 239. Conservative Force Extension Rule

Any conservative force model must define:

1. scalar potential;
2. coordinate variables;
3. force derivative;
4. boundary conditions;
5. units;
6. symmetry;
7. numerical validation.

---

## 240. Stress Extension Rule

Any energy-derived stress model must define:

1. cell/strain parameterization;
2. derivative convention;
3. sign convention;
4. normalization by volume where applicable;
5. tensor transformation;
6. units.

---

## 241. Canonical Energy Invariants

Every conforming conservative energy functional preserves:

1. scalar physical output;

2. explicit energy units;

3. declared spatial invariance;

4. species-preserving permutation invariance;

5. explicit periodic behavior where applicable;

6. explicit coordinate differentiability where conservative forces are derived;

7. explicit provenance.

---

## 242. Canonical Conservative Force Invariant

For the conservative force path:

`F_i = -grad_(r_i) E`.

This relation is exact at the formal level.

---

## 243. Canonical Symmetry Invariants

The energy layer preserves:

`E(gX) = E(X)`

under the declared symmetry group.

Derived forces transform equivariantly.

Derived stress transforms as a tensor under rigid rotation.

---

## 244. Canonical State-Separation Invariants

The framework preserves:

`equivariant representation ≠ energy`

`resonance state ≠ energy`

`resonance classification ≠ energy`

`ternary state ≠ energy`

`ternary 0 ≠ energy 0`

`generic scalar ≠ physical energy`

`generic vector ≠ force`

`generic tensor ≠ stress`.

---

## 245. Canonical Conservative Distinctions

The framework preserves:

`equivariance ≠ conservativity`

`potential energy ≠ total mechanical energy`

`energy minimum ≠ resonance`

`energy minimum ≠ ternary neutral`

`energy crossing ≠ bifurcation`

`energy crossing ≠ physical phase transition`

`energy barrier ≠ active neutral`.

---

## 246. Canonical TR Execution Boundary

Energy conditioning does not alter the canonical ternary transition graph:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 247. Canonical Opposite Energy-Mode Chain

When the active energy functional is keyed to executed ternary state, opposite mode switching follows:

`E_-1`

`→ E_0`

`→ E_1`

or:

`E_1`

`→ E_0`

`→ E_-1`.

---

## 248. Canonical Scientific Distinctions

The energy layer preserves:

`resonance ≠ energy`

`coherence ≠ energy`

`phase order ≠ energy`

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`oscillator phase ≠ physical phase of matter`

`ternary state ≠ energy`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`equivariant force ≠ conservative force`

`numerical energy conservation ≠ mathematical energy conservation`.

---

## 249. Canonical Energy Chain

The conservative path is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance state`

`→ ternary feature conditioning`

`→ invariant scalar energy`

`→ coordinate gradient`

`→ equivariant force`.

---

## 250. Canonical Stress Chain

For cell-dependent energy:

`atomic configuration + cell`

`→ invariant energy`

`→ strain/cell derivative`

`→ stress tensor`.

---

## 251. Canonical Learning Interface

Volume 04 will use:

- reference energy;
- reference force;
- reference stress

to optimize the energy-model parameter set.

---

## 252. Canonical Molecular-Dynamics Interface

Volume 05 will use forces derived from the energy functional within equations of motion and numerical integrators.

---

## 253. Interface to Chapter 09

Chapter 09 develops Forces and Stress.

It formalizes:

- conservative force;
- direct equivariant force;
- energy-gradient consistency;
- stress tensors;
- virial relations;
- cell derivatives;
- force/stress validation.

The present chapter supplies the scalar energy functional on which those relations operate.

---

## 254. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each model-family member must declare:

- energy decomposition;
- local/global terms;
- resonance conditioning;
- ternary conditioning;
- conservative force relation;
- stress interface;
- units;
- symmetry;
- differentiability.

---

## 255. Final Formal Structure

The conservative energy layer may be represented as:

`CEF = (D_E, E, X_EQ, X_R, X_T, H, PBC, phi_E)`.

Here:

- `D_E` is the admissible energy-model domain;
- `E` is the scalar energy functional;
- `X_EQ` is equivariant representation state;
- `X_R` is resonance state;
- `X_T` is ternary feature state;
- `H` is optional periodic cell state;
- `PBC` is periodicity state;
- `phi_E` is the parameter set.

For a conservative coordinate force:

`F_i = -grad_(r_i) E`.

For rigid symmetry:

`E(g · X) = E(X)`.

---

## 256. Final Statement

The Conservative Energy Functional is the scalar physical-output layer connecting equivariant interatomic representation to mechanical force and stress.

The energy functional may depend on:

- atomic configuration;
- interaction graph;
- equivariant representation;
- message-passed state;
- resonance state;
- ternary feature channels;
- periodic cell state;
- explicitly declared global variables.

Energy remains a scalar physical quantity with declared units.

It is not:

- a representation coordinate;
- a resonance class;
- a ternary state;
- a graph edge;
- a message;
- a scheduler state.

For conservative force:

`F_i = -grad_(r_i) E`.

The framework preserves:

`equivariance ≠ conservativity`

`resonance state ≠ energy`

`ternary state ≠ energy`

`ternary 0 ≠ energy 0`

`energy minimum ≠ resonance`

`energy crossing ≠ physical phase transition`

`phase coupling ≠ mechanical force`.

When the energy functional is conditioned by executed ternary state, opposite mode changes inherit the canonical active-neutral route:

`E_-1 → E_0 → E_1`

and:

`E_1 → E_0 → E_-1`.

The execution graph itself remains:

`-1 ↔ 0 ↔ 1`.

These definitions establish the scalar conservative energy layer required for the Forces and Stress formalism developed in Chapter 09.
