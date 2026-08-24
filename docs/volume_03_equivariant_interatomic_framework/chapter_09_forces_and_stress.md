# Forces and Stress

## 1. Purpose

This chapter defines forces and stress within the Equivariant Interatomic Framework of TR-EIF.

The force and stress layer converts the scalar energy and interatomic representation into explicitly typed mechanical outputs while preserving:

- spatial equivariance;
- atom-permutation equivariance;
- dimensional consistency;
- conservative energy-force relations where declared;
- explicit tensor semantics;
- periodic-cell consistency;
- resonance and ternary conditioning without semantic collapse;
- deterministic numerical evaluation;
- mechanical validation interfaces.

The canonical chain is:

`atomic configuration`

`→ interaction graph`

`→ equivariant representation`

`→ message passing`

`→ resonance parameterization`

`→ ternary feature channels`

`→ conservative energy`

`→ forces and stress`.

Force and stress remain distinct from:

- graph edges;
- message vectors;
- oscillator phase coupling;
- resonance state;
- ternary state;
- energy itself.

---

## 2. Force State

For atom:

`i`

the force is:

`F_i ∈ R^3`.

For:

`N`

atoms the complete force state is:

`F = (F_1, ..., F_N)`.

Therefore:

`F ∈ R^(3N)`.

---

## 3. Force Units

Force has physical dimensions:

`energy / length`.

The model must declare the force unit system.

---

## 4. Conservative Force

For a differentiable scalar energy functional:

`E(R)`

the conservative force is:

`F_i = -grad_(r_i) E`.

This relation defines the conservative force path.

---

## 5. Complete Coordinate Gradient

For:

`R = (r_1, ..., r_N)`

the complete force vector is:

`F = -grad_R E`.

---

## 6. Energy-Force Sign Convention

The canonical conservative sign convention is:

`force = negative energy gradient`.

The sign must remain fixed in:

- documentation;
- implementation;
- tests;
- exported artifacts.

---

## 7. Force as Polar Vector

Force is a polar vector.

Under:

`Q ∈ O(3)`

the force transforms as:

`F_i' = Q F_i`.

---

## 8. Translation Behavior

A force vector is unaffected by a static global translation of the coordinate origin when the internal energy is translation invariant.

---

## 9. Rotation Equivariance

For rotation:

`Q`

and a rotation-invariant energy:

`E(QR) = E(R)`,

the force satisfies:

`F_i(QR) = Q F_i(R)`.

---

## 10. Reflection Equivariance

For an:

`O(3)`-invariant energy,

force transforms under improper orthogonal transformations by the same polar-vector rule:

`F_i(QR) = Q F_i(R)`.

---

## 11. Permutation Equivariance

For admissible atom permutation:

`pi`,

the force array must permute consistently with atomic labels.

Global relabeling does not change the physical force field.

---

## 12. Force versus Generic Vector

The distinction remains:

`generic equivariant vector ≠ mechanical force`.

Force semantics require:

- physical units;
- atomic association;
- declared mechanical mapping;
- validation.

---

## 13. Force versus Message

The distinction remains:

`message vector ≠ force vector`.

A graph message may transform as a vector without representing mechanical force.

---

## 14. Force versus Phase Coupling

The invariant remains:

`phase coupling ≠ mechanical force`.

A Kuramoto-Sakaguchi interaction term belongs to oscillator phase dynamics.

It is not an interatomic force law.

---

## 15. Force versus Resonance State

The distinction remains:

`resonance state ≠ force`.

Resonance may condition an energy or direct force model.

---

## 16. Force versus Ternary State

The distinction remains:

`ternary state ≠ force`.

Values:

`-1`

`0`

`1`

are categorical states.

They are not force magnitudes or directions.

---

## 17. Zero Force versus Active Neutral

The distinction remains:

`F_i = 0 ≠ ternary state 0`.

A zero force vector and active-neutral ternary state belong to different state spaces.

---

## 18. Direct Force Model

A model may predict force directly:

`F_direct = P_F(X_conf, X_G, X_EQ, X_R, X_T)`.

The output must preserve vector equivariance.

---

## 19. Direct Force Equivariance

A direct force model must satisfy:

`P_F(g · X) = rho_F(g) P_F(X)`.

For rigid spatial action:

`rho_F(g)F = QF`.

---

## 20. Direct Force versus Conservative Force

The distinction remains:

`direct equivariant force ≠ conservative force`.

A direct force model is conservative only when the applicable integrability relation is established.

---

## 21. Energy-Derived Force

For the conservative path:

`X`

`→ E(X)`

`→ -grad_R E`

`→ F`.

This construction structurally links energy and force.

---

## 22. Energy-Force Consistency

If both:

`E_pred`

and:

`F_pred`

are outputs of a model claiming conservative consistency, the applicable relation is:

`F_pred = -grad_R E_pred`.

---

## 23. Force Consistency Residual

A numerical consistency residual may be:

`epsilon_EF = ||F_pred + grad_R E_pred||`.

The norm and tolerance must be explicit.

---

## 24. Integrability

A direct force field admits a scalar potential only under the applicable integrability and domain conditions.

This is independent of spatial equivariance.

---

## 25. Mixed Partial Symmetry

For sufficiently smooth conservative energy:

`dF_i,a / dr_j,b = dF_j,b / dr_i,a`

with the appropriate sign convention inherited from the energy Hessian.

This is a local integrability relation.

---

## 26. Energy Hessian

The Hessian is:

`H_E = d^2 E / dR^2`.

For conservative force:

`dF / dR = -H_E`.

---

## 27. Hessian Symmetry

For sufficiently smooth:

`E`

the Hessian is symmetric.

---

## 28. Force Jacobian

The force Jacobian is:

`J_F = dF / dR`.

For a conservative model:

`J_F = -H_E`.

---

## 29. Pair Force

A pairwise model may define:

`F_ij`

as the force contribution associated with pair:

`i,j`.

The pair decomposition must be explicitly defined.

---

## 30. Pair Force Antisymmetry

For an isolated pair potential depending only on:

`d_ij`,

one obtains:

`F_ji = -F_ij`.

This relation belongs to that specific pairwise conservative structure.

---

## 31. Many-Body Force

In a many-body model, total force on atom:

`i`

may depend on the complete local environment.

A unique pair-force decomposition is not generally required.

---

## 32. Force Decomposition Nonuniqueness

A many-body force can sometimes be decomposed into pair-like contributions in more than one way.

The total atomic force remains the primary mechanical output.

---

## 33. Newton Pair Relation Boundary

The relation:

`F_ij = -F_ji`

must not be imposed automatically on arbitrary latent message vectors or arbitrary many-body decompositions.

---

## 34. Net Internal Force

For a translation-invariant conservative internal energy:

`sum_i F_i = 0`.

This follows from global translation invariance under the corresponding assumptions.

---

## 35. Total Force

When external forces exist:

`F_total,i = F_internal,i + F_external,i`.

Then:

`sum_i F_total,i`

need not be zero.

---

## 36. External Force

An external force may arise from:

- external potential;
- electric field;
- imposed mechanical field;
- other declared external interaction.

Its transformation law must be included in the complete model.

---

## 37. External Potential Force

For external scalar potential:

`V_ext(r_i)`

the corresponding force is:

`F_ext,i = -grad_(r_i) V_ext`.

---

## 38. Constant External Force

A constant laboratory-frame force breaks full rotational symmetry unless the external vector is transformed together with the system.

---

## 39. Torque

The torque about origin:

`o`

may be defined:

`tau = sum_i (r_i - o) × F_i`.

---

## 40. Torque Units

Torque has energy units.

It remains distinct from scalar energy.

---

## 41. Rotational Invariance and Internal Torque

For an isolated rotationally invariant conservative system, the total internal torque satisfies the corresponding zero-torque relation under the applicable assumptions.

---

## 42. Torque Origin Dependence

Torque about an origin can change when net force is nonzero.

The origin must therefore be explicit when relevant.

---

## 43. Force and Momentum

Classical momentum evolution obeys:

`dp_i/dt = F_i`.

This relation is introduced fully in Volume 05.

---

## 44. Force and Acceleration

For mass:

`m_i > 0`:

`m_i a_i = F_i`.

Force and acceleration remain distinct quantities.

---

## 45. Force Field

The interatomic force field may be written:

`F: X_conf → R^(3N)`.

A state-augmented model may use:

`F: X_conf × X_R × X_T × X_aux → R^(3N)`.

---

## 46. Resonance-Conditioned Force

A force model may depend on resonance state:

`F = F(X_EQ, X_R)`.

This may occur directly or through resonance-conditioned energy.

---

## 47. Ternary-Conditioned Force

A force model may depend on ternary features:

`F = F(X_EQ, X_R, X_T)`.

The source ternary channel must be explicit.

---

## 48. Target-Conditioned Force

A model may condition force on:

`t_target`.

This is distinct from execution-conditioned force.

---

## 49. Execution-Conditioned Force

A model may condition force on:

`t_exec`.

The active force law then follows committed ternary execution state.

---

## 50. Pending-Conditioned Force

A pending route may influence force only if explicitly defined.

`t_pending`

remains separately typed.

---

## 51. Active-Neutral Force Mode

A model may define:

`F_0`

for executed state:

`0`.

This force need not be the zero vector.

---

## 52. Neutral Force Is Not Zero by Identity

The invariant remains:

`ternary 0 ≠ zero force`.

---

## 53. Mode-Specific Force Family

A hybrid model may define:

`F_-1(R)`

`F_0(R)`

`F_1(R)`.

---

## 54. Conservative Mode-Specific Force

If each mode derives from:

`E_q(R)`,

then:

`F_q = -grad_R E_q`.

---

## 55. Opposite Force-Mode Routing

If the active force mode is keyed to:

`t_exec`,

an opposite state change follows:

`F_-1`

`→ F_0`

`→ F_1`

or the reverse.

---

## 56. No Direct Opposite Execution

The force-mode sequence cannot bypass:

`0`

when keyed directly to canonical executed ternary state.

---

## 57. Target Prediction Branch

A model may compute hypothetical:

`F(R, t_target)`

without committing:

`t_exec`.

Such force is a predicted or counterfactual branch.

It is not the currently executed force mode unless defined as such.

---

## 58. Stress State

Stress is represented by a second-order tensor:

`Sigma ∈ R^(3×3)`.

The exact sign and normalization convention must be declared.

---

## 59. Stress Units

Stress has physical dimensions:

`energy / volume`

or equivalently:

`force / area`.

The unit system must be explicit.

---

## 60. Stress Transformation

Under rigid rotation:

`Q`

stress transforms as:

`Sigma' = Q Sigma Q^T`.

---

## 61. Stress Is Not Scalar

Stress is tensor-valued.

A scalar pressure derived from stress is a separate observable.

---

## 62. Stress versus Generic Tensor

The distinction remains:

`generic tensor feature ≠ stress`.

Stress requires mechanical semantics and units.

---

## 63. Stress versus Resonance Tensor

A tensor resonance coordinate is not stress by identity.

---

## 64. Stress versus Ternary State

The distinction remains:

`ternary state ≠ stress`.

---

## 65. Zero Stress versus Active Neutral

The distinction remains:

`Sigma = 0 ≠ ternary 0`.

---

## 66. Cell-Dependent Energy

For periodic configuration:

`E = E(R,H)`.

Stress may be derived from response of energy to cell deformation.

---

## 67. Deformation Gradient

Let:

`F_def`

denote a deformation gradient.

This symbol must remain distinct from mechanical force:

`F_i`.

When ambiguity exists, an alternate symbol should be used in a concrete implementation.

---

## 68. Infinitesimal Strain

An infinitesimal strain tensor may be represented:

`epsilon`.

The exact strain measure depends on the mechanical formulation.

---

## 69. Energy-Strain Derivative

A stress convention may use an energy derivative with respect to strain:

`dE / d epsilon`.

The normalization and sign convention must be explicitly defined.

---

## 70. Volume Normalization

Stress derivation commonly introduces the cell volume:

`V_cell`.

The exact relation depends on the selected stress convention.

---

## 71. Stress Sign Convention

Different communities may define tensile/compressive signs differently.

TR-EIF requires the adopted sign convention to be explicit in each concrete model and artifact.

---

## 72. Cauchy Stress

A model may report Cauchy stress.

Its definition must be tied to the corresponding configuration and deformation measure.

---

## 73. First Piola-Kirchhoff Stress

A finite-deformation model may instead use first Piola-Kirchhoff stress.

This is a distinct tensor quantity.

---

## 74. Second Piola-Kirchhoff Stress

A model may use second Piola-Kirchhoff stress.

Stress type must never be inferred solely from a field named:

`stress`.

---

## 75. Stress Type Metadata

A stress artifact must identify:

- tensor type;
- reference configuration;
- sign convention;
- units;
- normalization.

---

## 76. Virial Tensor

A virial-like tensor may contain terms involving:

`r_i`

and:

`F_i`

or pair contributions.

The exact definition depends on the mechanical and statistical formulation.

---

## 77. Virial Stress

A virial stress is not identical to every energy-derivative stress definition under all conditions.

The relation must be stated for the selected model.

---

## 78. Pair Virial

A pairwise contribution may involve:

`r_ij ⊗ F_ij`.

The counting convention must be explicit.

---

## 79. Kinetic Stress Contribution

In dynamical systems, a kinetic contribution may enter a microscopic stress expression.

This requires velocities and belongs to the complete MD state.

---

## 80. Static Stress

A static energy-derived stress can be evaluated without kinetic terms under the corresponding definition.

---

## 81. Pressure

A scalar pressure may be obtained from stress through a declared convention.

A common isotropic scalar construction uses the trace of stress.

The sign convention must be explicit.

---

## 82. Pressure versus Stress

The distinction remains:

`pressure ≠ stress tensor`.

Pressure may be one scalar derived from stress.

---

## 83. Hydrostatic Stress

A hydrostatic tensor is proportional to identity:

`Sigma = p I`

up to the adopted sign convention.

---

## 84. Deviatoric Stress

Stress may be decomposed into:

- isotropic part;
- deviatoric part.

---

## 85. Stress Trace

The trace:

`tr(Sigma)`

is rotationally invariant.

---

## 86. Deviatoric Stress Tensor

The deviatoric component transforms as a tensor under rotation.

---

## 87. Stress Invariants

Scalar invariants may be formed from:

- trace;
- determinant;
- tensor contractions.

These are distinct from the full stress tensor.

---

## 88. Stress and Symmetry

Material or configuration symmetry may constrain allowable stress structure.

The exact constraints depend on the state and constitutive model.

---

## 89. Atomic Virial State

A model may define per-atom virial or local stress-like quantities.

Such decompositions are convention-dependent.

---

## 90. Local Stress Nonuniqueness

Local stress assignments are not universally unique.

The global stress tensor remains separately defined.

---

## 91. Force from Local Energy

For local decomposition:

`E = sum_j E_j`

the force on atom:

`i`

is:

`F_i = -sum_j grad_(r_i) E_j`.

Thus a local energy contribution may affect multiple atomic forces.

---

## 92. Atomic Energy versus Atomic Force

The force on atom:

`i`

is not generally obtained only from:

`E_i`.

All energy terms depending on:

`r_i`

contribute.

---

## 93. Edge Contribution to Force

An edge-dependent energy term may contribute force to both incident atoms.

---

## 94. Graph Edge versus Pair Force

The distinction remains:

`graph edge ≠ pair force`.

An edge defines a computational interaction path.

---

## 95. Message Gradient Contribution

A force obtained by differentiating message-passed energy propagates through all differentiable graph and representation operations that depend on coordinates.

---

## 96. Automatic Differentiation

Automatic differentiation may compute:

`grad_R E`.

This is a numerical differentiation mechanism.

It does not change the formal conservative relation.

---

## 97. Analytic Differentiation

A model may derive explicit analytic forces.

The analytic result must be consistent with the declared energy functional if conservative force is claimed.

---

## 98. Finite-Difference Differentiation

Finite differences may approximate force:

`F_i,a ≈ -[E(R + delta e_i,a) - E(R - delta e_i,a)] / (2 delta)`.

The approximation depends on:

`delta`.

---

## 99. Finite-Difference Force Error

The finite-difference error depends on:

- perturbation size;
- floating-point precision;
- energy smoothness;
- local curvature.

---

## 100. Force Validation by Finite Difference

Finite-difference force validation compares analytic or automatic-differentiation force against energy differences.

---

## 101. Stress Validation by Finite Strain

Stress may be validated by small controlled cell/strain perturbations and comparison with energy response under the adopted convention.

---

## 102. Differentiability of Graph Construction

If graph topology changes discontinuously with coordinates, force differentiation across graph-cutoff boundaries requires explicit handling.

---

## 103. Hard Cutoff

A hard graph cutoff may introduce discontinuous energy or force if the interaction contribution does not vanish smoothly.

---

## 104. Smooth Cutoff

A smooth cutoff function can regularize the energy near an interaction boundary.

---

## 105. Force-Smooth Cutoff

To preserve force continuity, the derivative of the cutoff behavior must satisfy the declared smoothness requirement.

---

## 106. Higher-Derivative Applications

Phonons, Hessians, and higher-order response require additional energy smoothness.

---

## 107. Ternary Switching and Force Discontinuity

A hard switch between:

`E_-1`

`E_0`

and:

`E_1`

may produce discontinuous force across execution events.

This behavior must be part of the declared hybrid dynamics.

---

## 108. Continuous Mode Matching

A model may impose matching conditions at mode-switch boundaries.

These may include:

- equal energy;
- equal force;
- selected derivative continuity.

Such conditions are specialization-specific.

---

## 109. Neutral Bridge Surface

A neutral energy surface:

`E_0`

may provide an intermediate mechanical regime between:

`E_-1`

and:

`E_1`.

Its exact form is model-defined.

---

## 110. Neutral Bridge Does Not Imply Arithmetic Interpolation

The relation:

`0`

does not imply:

`E_0 = (E_-1 + E_1)/2`.

No arithmetic interpolation is assumed.

---

## 111. Neutral Force Does Not Imply Average Force

Likewise:

`F_0`

need not equal:

`(F_-1 + F_1)/2`.

---

## 112. Resonance-Dependent Force Surface

A continuous resonance coordinate may parameterize the active energy or force surface.

The mapping must preserve symmetry and units.

---

## 113. Resonance-Modulated Energy

A general form may be:

`E = E(R, r)`.

Then force with respect to:

`R`

must account for all coordinate dependence of:

`r(R)`

when:

`r`

is part of the differentiable computational graph.

---

## 114. Total Derivative through Resonance

If:

`r = P_R(R)`,

then:

`dE/dR`

contains both direct and resonance-mediated dependencies.

---

## 115. Detached Resonance Conditioning

A model may intentionally stop gradient propagation through resonance state.

That produces a different force model and must be explicit.

---

## 116. Differentiable Ternary Boundary

Exact hard ternary classification is discontinuous.

A conservative energy conditioned on a hard ternary state is therefore a hybrid discrete-continuous model.

---

## 117. Soft Training Surrogate

A continuous surrogate may be used during training.

The forward hard ternary state remains separately defined when exact ternary semantics are used.

---

## 118. Surrogate Force Boundary

Forces computed through a continuous training surrogate are not automatically identical to forces of the hard hybrid execution model.

The distinction must remain explicit.

---

## 119. Force Conservation

In classical dynamics, conservative internal forces derived from translation-invariant energy support momentum conservation under the corresponding isolated-system equations.

The complete conservation law is developed in Volume 05.

---

## 120. Angular Momentum Interface

Rotational symmetry of the conservative internal energy supports the corresponding angular-momentum conservation structure under applicable isolated dynamics.

---

## 121. Energy Conservation Interface

Time-independent conservative forces provide the potential-energy component of total mechanical energy conservation.

---

## 122. Thermostat Boundary

Thermostats may introduce nonconservative or extended-system forces.

These belong to Volume 05.

---

## 123. Barostat Boundary

Barostats alter cell and mechanical dynamics.

They belong to Volume 05.

---

## 124. Constraint Force

A constrained dynamical system may contain constraint forces in addition to interatomic conservative forces.

---

## 125. Constraint Force versus Model Force

Constraint force must remain separately identifiable when required by the integrator or analysis.

---

## 126. Fixed Atom

An atom may be constrained not to move even when the energy gradient is nonzero.

A fixed-coordinate constraint does not imply zero model force.

---

## 127. Force Mask

A numerical force mask may suppress selected force components for constrained dynamics.

A mask value:

`0`

is not active-neutral ternary state.

---

## 128. Force Clipping

A numerical implementation may clip large forces.

This changes the executed force from the formal conservative gradient and must be explicit.

---

## 129. Clipped Force Is Not Conservative Gradient

If clipping alters:

`F_i`,

the resulting applied force generally differs from:

`-grad E`.

---

## 130. Force Regularization

Training may penalize large force magnitude or inconsistency.

This belongs to the optimization layer.

---

## 131. Force Uncertainty

A model may output:

`u_F`

for force uncertainty.

This uncertainty is not force and not ternary state.

---

## 132. Stress Uncertainty

Likewise:

`u_Sigma`

may accompany stress.

---

## 133. Force Confidence versus Magnitude

A confidence scalar must not be interpreted as force magnitude.

---

## 134. Force Domain

Let:

`D_F`

denote the admissible force-model domain.

It inherits or refines the energy-model domain.

---

## 135. Stress Domain

Let:

`D_Sigma`

denote the admissible stress domain.

Periodic cell validity may be required.

---

## 136. Non-Finite Force

A force containing:

`NaN`

or infinity is an invalid numerical state.

It is not ternary neutral.

---

## 137. Non-Finite Stress

A stress tensor containing non-finite values is likewise invalid numerical state.

---

## 138. Force Overflow

Numerical overflow must be handled explicitly.

---

## 139. Force Underflow

Numerical underflow is a representation effect.

It does not define physical zero force by semantic identity.

---

## 140. Force Precision

Numerical force precision may differ from energy precision.

The arithmetic contract must be explicit.

---

## 141. Mixed Precision Force Evaluation

A model may evaluate representation and energy in mixed precision while accumulating gradients in another precision.

Validation must measure resulting force errors.

---

## 142. Fixed-Point Force Representation

A hardware-facing implementation may encode forces in fixed-point form.

Scaling and saturation must be explicit.

---

## 143. Force Quantization

Quantized force remains a numerical approximation of a physical vector.

It is not ternary state.

---

## 144. Stress Quantization

Stress may likewise be quantized numerically.

---

## 145. Force Trace

A force trace may contain:

- atom identifier;
- force vector;
- units;
- numerical step;
- physical time;
- resonance state;
- ternary target;
- ternary executed state;
- model identifier;
- provenance.

---

## 146. Stress Trace

A stress trace may contain:

- tensor components;
- units;
- tensor convention;
- sign convention;
- cell;
- volume;
- physical time;
- model state;
- provenance.

---

## 147. Energy-Force Trace

A combined trace may include:

- total energy;
- atomic forces;
- force consistency residual;
- ternary conditioning state;
- resonance state.

---

## 148. Force Restart State

Force itself need not be stored for restart if it is deterministically recomputed from complete current state.

If a model retains force history, that history becomes restart state.

---

## 149. Stress Restart State

Likewise, stress may be recomputed unless a stateful constitutive model retains stress history.

---

## 150. History-Dependent Force Model

A force model may depend on retained history:

`F[k] = F(X[k], X_M[k])`.

The memory must then be explicit.

---

## 151. History-Dependent Stress Model

A constitutive or coarse-grained model may retain stress history.

This lies beyond a purely memoryless interatomic potential.

---

## 152. Deterministic Force Evaluation

A deterministic force calculation produces identical declared output for identical:

- complete state;
- model parameters;
- graph;
- arithmetic semantics;
- differentiation path.

---

## 153. Deterministic Stress Evaluation

Stress evaluation must likewise preserve deterministic ordering where exact replay is required.

---

## 154. Force Replay

A replay test may compare:

- exact output;
- byte-identical output;
- tolerance-based vector equality

according to the numerical contract.

---

## 155. Stress Replay

Stress replay follows the corresponding tensor comparison contract.

---

## 156. Force Symmetry Validation

A force validator must verify:

- translation behavior;
- rotation equivariance;
- reflection behavior where applicable;
- permutation equivariance.

---

## 157. Translation Test

Translate all positions by:

`c`.

For an internal translation-invariant model:

`F_i(R+c) = F_i(R)`.

---

## 158. Rotation Test

Rotate:

`R → QR`.

Verify:

`F_i(QR) = QF_i(R)`.

---

## 159. Reflection Test

For an:

`O(3)`-compatible model and improper orthogonal:

`Q`:

`F_i(QR) = QF_i(R)`.

---

## 160. Permutation Test

Apply an admissible atom permutation.

Forces must permute consistently.

---

## 161. Net-Force Test

For an isolated internal conservative model:

`sum_i F_i`

must satisfy the declared numerical tolerance around zero.

---

## 162. Torque Test

For an isolated rotationally invariant conservative system, total internal torque may be tested against the declared numerical tolerance.

---

## 163. Energy-Gradient Test

Compare model force to:

`-grad_R E`.

---

## 164. Finite-Difference Test

Controlled coordinate perturbations may provide an independent numerical gradient check.

---

## 165. Force Jacobian Symmetry Test

For sufficiently smooth conservative models, selected force-Jacobian blocks may be compared against the symmetry implied by the energy Hessian.

---

## 166. Stress Rotation Test

Rotate the complete configuration and cell.

Verify:

`Sigma' = Q Sigma Q^T`.

---

## 167. Stress Permutation Test

Atom reordering must not alter global stress.

---

## 168. Stress Finite-Strain Test

Apply a small declared strain.

Compare the numerical energy derivative with predicted stress under the adopted convention.

---

## 169. Pressure Consistency Test

If pressure is derived from stress, verify the declared trace/sign relation.

---

## 170. Periodic Image Test

Equivalent periodic representations must produce equivalent forces and stress.

---

## 171. Cell Rotation Test

For:

`H' = QH`

and:

`R' = QR`

energy remains invariant, force rotates, and stress transforms tensorially.

---

## 172. Ternary-Conditioned Force Test

For identical geometry, evaluate the declared force behavior under:

`-1`

`0`

`1`.

---

## 173. Active-Neutral Force Test

Verify that:

`t_exec = 0`

invokes the declared neutral force behavior rather than a missing-data branch.

---

## 174. Target/Execution Force Test

If force is keyed to:

`t_exec`,

changing only:

`t_target`

must not change active force unless another explicit dependency exists.

---

## 175. Pending-State Force Test

If:

`t_pending`

affects force, validate it independently.

---

## 176. Opposite-Route Force Test

For force keyed to executed mode, an opposite target must produce mode sequence:

`F_-1 → F_0 → F_1`

or:

`F_1 → F_0 → F_-1`.

---

## 177. No Direct Opposite Force-Mode Commit

A direct:

`F_-1 → F_1`

commit is forbidden when the force mode is defined solely by canonical:

`t_exec`.

---

## 178. Resonance-Conditioned Force Validation

Controlled changes in:

`X_R`

may verify the declared force-conditioning path.

---

## 179. Equivariance under Resonance Conditioning

If resonance state includes equivariant channels, all transformed resonance inputs must be transformed consistently before force comparison.

---

## 180. Ternary Scalar Invariance

A scalar ternary conditioning channel remains spatially invariant under rigid transformations.

---

## 181. Force Training

Volume 04 defines force-based loss functionals.

Reference forces may supervise the energy gradient directly.

---

## 182. Energy and Force Joint Training

A model may jointly fit:

- energy;
- forces;
- stress.

The loss weights belong to the learning layer.

---

## 183. Conservative Training

When forces are computed from model energy, energy-force consistency is preserved structurally during training.

---

## 184. Separate Force-Head Training

A direct force head requires additional consistency terms if agreement with energy gradient is required.

---

## 185. Stress Training

Stress reference data may supervise the cell/strain response of energy or a direct tensor output.

---

## 186. Force Scaling in Loss

Force loss may require normalization by:

- number of atoms;
- number of components;
- physical scale.

The exact rule belongs to Volume 04.

---

## 187. Stress Scaling in Loss

Stress loss weighting must respect units and tensor-component conventions.

---

## 188. Force Benchmark

A benchmark may report:

- force MAE;
- force RMSE;
- maximum force error;
- equivariance residual;
- energy-gradient consistency;
- runtime.

---

## 189. Stress Benchmark

A stress benchmark may report:

- tensor MAE;
- componentwise error;
- invariant error;
- rotation residual;
- runtime.

---

## 190. Mechanical Benchmark Scope

Every benchmark must identify:

- dataset;
- species;
- state domain;
- unit system;
- model version;
- numerical precision.

---

## 191. Force Provenance

Force definitions and artifacts may carry:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`.

---

## 192. Derived Conservative Force

A force obtained from:

`-grad E`

carries:

`DERIVED`

provenance relative to the declared energy model.

---

## 193. Author-Defined Force Coupling

A TR-EIF-specific resonance- or ternary-conditioned force architecture carries:

`AUTHOR_DEFINED`

provenance where applicable.

---

## 194. Primary-Source Mechanical Relation

A mechanical relation adopted directly from established source material carries:

`PRIMARY_SOURCE`.

---

## 195. Calibrated Mechanical Parameter

A fitted stress, force, cutoff, or constitutive parameter carries:

`CALIBRATED`.

---

## 196. Benchmark Force Result

Measured force errors or performance carry:

`BENCHMARK`.

---

## 197. Force Test Fixture

Controlled geometries with reference derivatives carry:

`TEST_FIXTURE`.

---

## 198. Stress Provenance

Stress definitions, parameters, and benchmark artifacts follow the same provenance system.

---

## 199. Force Extension Rule

Any new force output must define:

1. source state;
2. vector semantics;
3. units;
4. spatial transformation;
5. permutation behavior;
6. conservative or direct path;
7. resonance conditioning;
8. ternary conditioning;
9. domain;
10. validation;
11. provenance.

---

## 200. Conservative Force Extension Rule

Any conservative force must define:

1. scalar energy;
2. coordinate state;
3. differentiability;
4. gradient convention;
5. unit conversion;
6. boundary handling;
7. numerical differentiation validation.

---

## 201. Direct Force Extension Rule

Any direct force head must define:

1. equivariant output architecture;
2. force units;
3. conservativity status;
4. energy-consistency relation where applicable;
5. validation.

---

## 202. Pair-Force Extension Rule

Any pair-force decomposition must define:

1. pair indexing;
2. source/receiver convention;
3. antisymmetry if required;
4. double counting;
5. relation to total force;
6. physical interpretation.

---

## 203. Stress Extension Rule

Any stress output must define:

1. stress tensor type;
2. sign convention;
3. units;
4. cell/strain variable;
5. normalization;
6. rotation law;
7. periodic requirements;
8. validation.

---

## 204. Virial Extension Rule

Any virial-based stress must define:

1. configurational term;
2. kinetic term where used;
3. pair counting;
4. volume normalization;
5. sign convention;
6. relation to reported stress.

---

## 205. Ternary-Conditioned Force Extension Rule

Any ternary-conditioned force model must define:

1. source ternary channel;
2. target or executed state;
3. `-1` force law;
4. `0` force law;
5. `1` force law;
6. switching order;
7. conservative relation;
8. continuity conditions where required.

---

## 206. Resonance-Conditioned Force Extension Rule

Any resonance-conditioned force model must define:

1. source resonance state;
2. transformation law;
3. coupling to energy or direct force;
4. differentiability path;
5. units;
6. feedback ordering.

---

## 207. Canonical Force Invariants

Every conforming force layer preserves:

1. explicit vector output;

2. explicit physical units;

3. spatial equivariance;

4. atom-permutation equivariance;

5. explicit conservative or direct-force status;

6. explicit resonance/ternary conditioning where present;

7. explicit validation.

---

## 208. Canonical Conservative Relation

For the conservative path:

`F_i = -grad_(r_i) E`.

No other relation may be substituted silently.

---

## 209. Canonical Stress Invariants

Every conforming stress output preserves:

1. explicit tensor type;

2. explicit units;

3. explicit sign convention;

4. explicit strain/cell convention;

5. tensor transformation under rotation;

6. permutation invariance of the global tensor.

---

## 210. Canonical Translation Consequence

For isolated translation-invariant conservative internal energy:

`sum_i F_i = 0`

under the applicable assumptions.

---

## 211. Canonical Rotation Consequence

For isolated rotationally invariant conservative energy, the corresponding internal torque relation is preserved.

---

## 212. Canonical State-Separation Invariants

The framework preserves:

`message vector ≠ force`

`resonance vector ≠ force`

`ternary state ≠ force`

`zero force ≠ active-neutral 0`

`generic tensor ≠ stress`

`resonance tensor ≠ stress`

`zero stress ≠ active-neutral 0`

`pressure ≠ stress tensor`.

---

## 213. Canonical Mechanical Distinctions

The framework preserves:

`equivariance ≠ conservativity`

`force ≠ acceleration`

`force ≠ momentum`

`pair message ≠ pair force`

`graph edge ≠ force`

`energy Hessian ≠ interaction graph`

`stress ≠ energy`

`virial tensor ≠ every stress definition by identity`.

---

## 214. Canonical TR Execution Invariant

Mechanical output conditioning does not alter the execution topology:

`-1 ↔ 0 ↔ 1`.

Direct committed:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

---

## 215. Canonical Opposite Mechanical Mode Chain

When mechanical outputs are keyed to:

`t_exec`,

opposite mode switching follows:

`mode -1`

`→ mode 0`

`→ mode 1`

or:

`mode 1`

`→ mode 0`

`→ mode -1`.

---

## 216. Canonical Scientific Distinctions

The force/stress layer preserves:

`phase coupling ≠ mechanical force`

`phase relation ≠ chemical bond`

`oscillator phase ≠ physical phase of matter`

`resonance state ≠ force`

`resonance classification ≠ energy`

`ternary state ≠ force`

`ternary state ≠ stress`

`ternary state ≠ energy`

`energy crossing ≠ physical phase transition`

`ternary transition ≠ structural transition`

`structural transition ≠ physical phase transition`.

---

## 217. Canonical Conservative Mechanical Chain

The conservative chain is:

`atomic configuration`

`→ equivariant interatomic representation`

`→ resonance/ternary-conditioned invariant energy`

`→ coordinate gradient`

`→ atomic force`.

---

## 218. Canonical Stress Chain

The stress chain is:

`atomic configuration + cell`

`→ invariant energy`

`→ cell/strain derivative`

`→ stress tensor`.

---

## 219. Canonical Dynamics Interface

The output to Volume 05 is:

- atomic force;
- optional stress;
- potential energy;
- cell state;
- associated model metadata.

These drive molecular-dynamics evolution.

---

## 220. Interface to Chapter 10

Chapter 10 defines the TR-EIP Model Family.

Each model-family member must declare:

- conservative energy path;
- force construction;
- direct-force path where present;
- stress type;
- stress convention;
- resonance conditioning;
- ternary conditioning;
- symmetry contract;
- unit system;
- differentiability;
- validation.

---

## 221. Interface to Volume 04

Volume 04 develops Learning and Optimization.

The force/stress layer exports:

- energy targets;
- force targets;
- stress targets;
- gradient relations;
- equivariance constraints;
- conservative consistency relations.

---

## 222. Interface to Volume 05

Volume 05 develops Molecular Dynamics.

The force state enters:

`dp_i/dt = F_i`

or the equivalent second-order equations of motion.

Stress interfaces with:

- barostats;
- cell dynamics;
- transport and mechanical observables.

---

## 223. Interface to Volume 06

Volume 06 develops multiscale materials modeling.

Force and stress become interfaces for:

- atomistic-to-mesoscale transfer;
- continuum closure;
- thermodynamic consistency;
- engineering-scale models.

---

## 224. Interface to Volume 07

Volume 07 specializes the framework for FLiBe.

The force and stress layer becomes material-specific through:

- species set;
- reference interatomic data;
- thermodynamic state;
- local coordination;
- transport and validation conditions.

---

## 225. Final Formal Structure

The mechanical output layer may be represented as:

`MECH = (D_F, D_Sigma, E, F, Sigma, P_F, P_Sigma, rho_F, rho_Sigma)`.

Here:

- `D_F` is the force-model domain;
- `D_Sigma` is the stress-model domain;
- `E` is the scalar energy functional;
- `F` is atomic force state;
- `Sigma` is stress tensor;
- `P_F` is the force construction;
- `P_Sigma` is the stress construction;
- `rho_F` is the spatial action on force;
- `rho_Sigma` is the spatial action on stress.

For conservative force:

`F_i = -grad_(r_i) E`.

For rigid rotation:

`F_i' = Q F_i`

and:

`Sigma' = Q Sigma Q^T`.

---

## 226. Final Statement

Forces and stress form the mechanical-output layer of the Equivariant Interatomic Framework.

Force is a per-atom polar vector with declared physical units.

Stress is a second-order mechanical tensor with an explicitly declared tensor type, sign convention, normalization, and cell/strain relation.

For the conservative path:

`F_i = -grad_(r_i) E`.

The framework preserves:

`equivariance ≠ conservativity`

`generic vector ≠ force`

`message vector ≠ force`

`resonance state ≠ force`

`ternary state ≠ force`

`zero force ≠ active-neutral 0`

`generic tensor ≠ stress`

`ternary state ≠ stress`

`pressure ≠ stress tensor`

`phase coupling ≠ mechanical force`.

Resonance and ternary state may condition the mechanical model only through explicitly defined mappings.

When force or energy modes are keyed to executed ternary state, opposite-polarity mode switching remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`.

No force head, stress head, energy gradient, resonance mapping, or numerical operation alters this execution invariant.

These definitions establish the mechanical interface required for the TR-EIP Model Family developed in Chapter 10.
