# Mathematical Operators

## 1. Purpose

This chapter defines the canonical mathematical operators used throughout the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The operators act on the state spaces established in Chapters 01–04 and provide the formal machinery required for:

- continuous evolution;
- discrete evolution;
- circular phase dynamics;
- graph-based interactions;
- geometric transformations;
- resonance construction;
- balanced ternary execution;
- invariant and equivariant representations;
- energy, force, and stress relations;
- history and memory;
- multiscale transfer;
- numerical realization;
- validation predicates.

The governing rule is:

`operator semantics follow state-space type`.

An operator is admissible only when its domain, codomain, mathematical action, and required invariants are explicit.

---

## 2. Operator Definition

An operator is a mapping:

`A: X → Y`

between declared spaces:

`X`

and:

`Y`.

For:

`x ∈ X`

the result is:

`A(x) ∈ Y`.

An operator is not fully defined by its symbolic expression alone.

Its definition includes:

- domain;
- codomain;
- admissibility conditions;
- mathematical action;
- transformation behavior where relevant;
- dimensional behavior where relevant.

---

## 3. Unary Operator

A unary operator has the form:

`A: X → Y`.

Examples include:

- projection;
- normalization;
- phase wrapping;
- classification;
- differentiation;
- invariant extraction.

---

## 4. Binary Operator

A binary operator has the form:

`B: X × Y → Z`.

For:

`x ∈ X`

and:

`y ∈ Y`

the result is:

`B(x, y) ∈ Z`.

Binary operation requires compatibility of both input spaces with the operator definition.

---

## 5. N-Ary Operator

An `n`-ary operator has the form:

`A_n: X_1 × ... × X_n → Y`.

Each argument retains its own semantic type.

No argument may be replaced by another merely because its numerical representation is compatible.

---

## 6. Operator Composition

For:

`A: X → Y`

and:

`B: Y → Z`

the composition is:

`B ∘ A: X → Z`

with:

`(B ∘ A)(x) = B(A(x))`.

Composition is admissible only when the codomain of `A` matches the domain required by `B`.

---

## 7. Identity Operator

The identity operator on `X` is:

`Id_X: X → X`

defined by:

`Id_X(x) = x`.

---

## 8. Projection Operator

For product space:

`X = X_1 × ... × X_n`

the projection onto component `i` is:

`pi_i: X → X_i`.

For:

`x = (x_1, ..., x_n)`

the projection is:

`pi_i(x) = x_i`.

---

## 9. Inclusion Operator

For:

`A ⊆ X`

the canonical inclusion is:

`i_A: A → X`

defined by:

`i_A(a) = a`.

Inclusion preserves the value while changing the declared ambient space.

---

## 10. Restriction Operator

For:

`F: X → Y`

and:

`A ⊆ X`

the restricted operator is:

`F|_A: A → Y`.

Restriction changes the domain while preserving the original action of `F` on admissible elements.

---

## 11. Product Operator

For mappings:

`F_i: X → Y_i`

for:

`i = 1, ..., n`

define:

`F = (F_1, ..., F_n): X → Y_1 × ... × Y_n`.

For:

`x ∈ X`

the result is:

`F(x) = (F_1(x), ..., F_n(x))`.

---

## 12. Aggregation Operator

An aggregation operator maps collections of local states or observables into a declared aggregate space.

Let:

`X_loc`

be a local state space.

An aggregation operator may have the form:

`A_G: X_loc^N → Y_G`.

Aggregation semantics must specify:

- ordering sensitivity;
- normalization;
- weighting;
- locality;
- dimensional consistency.

---

## 13. Sum Operator

For compatible elements:

`x_1, ..., x_N`

in a vector space:

`V`

the sum is:

`sum_i x_i ∈ V`.

Addition is admissible only when the operands belong to a common additive structure.

---

## 14. Mean Operator

For:

`x_1, ..., x_N ∈ V`

where scalar division by positive integer `N` is defined:

`mean(x) = (1/N) sum_i x_i`.

A mean requires semantic and dimensional compatibility among all terms.

---

## 15. Weighted Sum Operator

For:

`x_i ∈ V`

and scalar weights:

`w_i`

the weighted sum is:

`sum_i w_i x_i`.

The weights must be dimensionally compatible with the intended output.

If normalized averaging is intended:

`sum_i w_i = 1`

must be stated explicitly.

---

## 16. Norm Operator

For normed space:

`X`

the norm is:

`|| · ||: X → R_0+`.

For Euclidean vector:

`x ∈ R^n`

the standard Euclidean norm is:

`||x||_2 = sqrt(sum_i x_i^2)`.

---

## 17. Distance Operator

For metric space:

`(X, d)`

the distance operator is:

`d: X × X → R_0+`.

The metric must be appropriate to the state-space topology.

---

## 18. Euclidean Distance

For:

`x, y ∈ R^n`

the Euclidean distance is:

`d_E(x, y) = ||x - y||_2`.

---

## 19. Circular Difference Operator

For:

`theta_a, theta_b ∈ S^1`

define a wrapped phase difference operator:

`Delta_S1: S^1 × S^1 → I_phase`

where:

`I_phase`

is a selected canonical phase-difference interval.

A common representative interval is:

`(-pi, pi]`.

The circular difference is the representative of:

`theta_a - theta_b`

modulo:

`2 pi`

inside the declared interval.

---

## 20. Circular Distance Operator

A circular distance may be defined as:

`d_S1(theta_a, theta_b) = |Delta_S1(theta_a, theta_b)|`.

Its codomain is:

`[0, pi]`

for the standard shortest-arc convention.

---

## 21. Phase-Wrap Operator

Define:

`Wrap: R → S^1`.

A numerical representative may be returned in:

`[0, 2 pi)`.

The operator identifies real values differing by:

`2 pi k`

for:

`k ∈ Z`.

---

## 22. Sign Operator

The classical sign operator is:

`sgn: R → {-1, 0, 1}`

with:

`sgn(x) = -1` for `x < 0`

`sgn(x) = 0` for `x = 0`

`sgn(x) = 1` for `x > 0`.

The codomain shares the same numerical values as `T`.

This does not make `sgn` a universal TR-EIF ternary-state operator.

A TR-EIF ternary target requires an explicitly defined semantic mapping.

---

## 23. Absolute-Value Operator

For:

`x ∈ R`

define:

`abs: R → R_0+`

by:

`abs(x) = |x|`.

For ternary state:

`t ∈ T`

the value:

`|t|`

belongs to:

`{0, 1}`.

This derived value is not itself a ternary state unless explicitly typed as such.

---

## 24. Clipping Operator

For real bounds:

`a ≤ b`

define:

`clip(x; a, b) = min(max(x, a), b)`.

The operator maps:

`R → [a, b]`.

A numerical clipping operation must not be interpreted automatically as physical saturation.

---

## 25. Threshold Operator

Let:

`eta`

be a declared threshold.

A binary threshold predicate may be defined:

`H_eta: R → {false, true}`

with:

`H_eta(x) = true`

when the declared threshold condition holds.

Threshold semantics must be specified explicitly.

---

## 26. Three-Region Classification Operator

For thresholds:

`eta_- < eta_+`

define a classifier:

`C_eta: R → K_3`

where:

`K_3 = {LOW, MID, HIGH}`.

A possible definition is:

`LOW` when `x < eta_-`

`MID` when `eta_- ≤ x ≤ eta_+`

`HIGH` when `x > eta_+`.

This classifier is distinct from balanced ternary execution.

---

## 27. Ternary Target Classification Operator

A model may define:

`P_T: X_src → T_target`.

The operator produces:

`t_target ∈ {-1, 0, 1}`.

Its thresholds, regions, features, and auxiliary variables are model-specific.

The output is a target.

It is not an automatic state commit.

---

## 28. Ternary State Validation Operator

Define:

`V_T: Z → {true, false}`

by:

`V_T(x) = true`

if and only if:

`x ∈ {-1, 0, 1}`.

This is an exact categorical predicate.

No tolerance is used.

---

## 29. Ternary Transition Predicate

Define:

`A_T: T_exec × T_exec → {true, false}`

for committed transitions.

The predicate must satisfy:

`A_T(-1, 1) = false`

and:

`A_T(1, -1) = false`.

The exact status of same-state retention and adjacent transitions is determined by the execution model.

---

## 30. Opposite-Polarity Predicate

Define:

`Opp: T × T → {true, false}`

by:

`Opp(a, b) = true`

if:

`a = -1 and b = 1`

or:

`a = 1 and b = -1`.

Otherwise:

`Opp(a, b) = false`.

---

## 31. Neutral-Mediation Operator

Define a routing operator:

`NRoute: T_exec × T_target → T_exec`.

For opposite polarity:

`NRoute(-1, 1) = 0`

`NRoute(1, -1) = 0`.

For non-opposite cases, the exact output follows the selected transition policy.

The operator does not itself authorize the later second leg.

---

## 32. Pending-Destination Operator

A staged transition may use:

`P_pending: T_exec × T_target → X_pending`.

For opposite polarity:

`P_pending(-1, 1) = 1`

`P_pending(1, -1) = -1`.

For other cases:

`P_pending`

may return:

`NONE`

according to the selected execution semantics.

---

## 33. Pending Completion Predicate

Define:

`A_pending: T_exec × X_pending × X_ctrl → {true, false}`

where:

`X_ctrl`

contains the control state required to authorize completion.

This predicate determines whether a retained pending destination may execute.

The existence of a pending destination does not imply:

`A_pending = true`.

---

## 34. Retention Operator

Define:

`Retain_X: X → X`

by:

`Retain_X(x) = x`.

For ternary active neutral:

`Retain_T(0) = 0`.

Retention is a valid state operation and is distinct from missing execution.

---

## 35. Commit Operator

A commit operator maps an admissible pre-commit state and authorized update into a retained post-commit state.

A generic typed form is:

`Commit: X × X_auth → X`.

The authorization input must correspond to the update being committed.

---

## 36. Request Operator

A request-producing operator has the form:

`Req: X → X_req`

or:

`Req: X × U → X_req`.

The request is an intermediate execution object.

It does not mutate retained state by itself.

---

## 37. Authorization Operator

Define:

`Authorize: X_req × X_ctrl × X → X_auth`.

The operator evaluates the requested action under the applicable:

- state invariants;
- control state;
- capacity constraints;
- transition rules.

---

## 38. Rejection Operator

A rejection operator maps an inadmissible request or proposal into an explicit rejection result:

`Reject: X_req → X_reject`.

Rejection is not active ternary `0`.

---

## 39. State-Update Operator

A general discrete state-update operator is:

`F_step: X × U × P → X`.

For execution index:

`k`

the update is:

`x[k+1] = F_step(x[k], u[k], p)`.

---

## 40. Continuous Vector-Field Operator

For Euclidean continuous state:

`X_c ⊆ R^n`

define:

`f: X_c × U × P × I_t → R^n`.

The continuous evolution law is:

`dx/dt = f(x, u, p, t)`.

---

## 41. Flow Operator

Where a continuous dynamical system admits a flow, define:

`phi_t: X → X`.

The flow satisfies the evolution law of the selected system.

The exact conditions for existence and uniqueness are model-dependent and are treated in later mathematical analysis.

---

## 42. Numerical Step Operator

For numerical state space:

`X_num`

and numerical step:

`Delta t`

define:

`Phi_Delta_t: X_num → X_num`.

This operator is a numerical realization.

It is distinct from exact flow:

`phi_Delta_t`.

---

## 43. Forward Euler Operator

For Euclidean system:

`dx/dt = f(x, t)`

the forward Euler step is:

`Phi_FE(x_n) = x_n + Delta t f(x_n, t_n)`.

Its numerical properties depend on:

- `f`;
- `Delta t`;
- state domain.

---

## 44. Generic Explicit Runge-Kutta Operator

An explicit Runge-Kutta method constructs stage values:

`k_s`

from previously available stages and forms:

`x_(n+1) = x_n + Delta t sum_s b_s k_s`.

The coefficients define the selected method.

No particular Runge-Kutta scheme is universal to TR-EIF.

---

## 45. Numerical Acceptance Operator

Define:

`A_num: X_prop × X_diag → {ACCEPT, REJECT}`.

A proposed numerical state enters accepted numerical state only if:

`A_num = ACCEPT`.

---

## 46. Numerical Rollback Operator

For rejected proposal:

`x_prop`

and previously accepted state:

`x_acc`

define rollback:

`Rollback(x_acc, x_prop) = x_acc`.

A rejected proposal does not mutate accepted retained state.

---

## 47. Error-Estimation Operator

A numerical error estimator has the form:

`E_num: X_num → X_error_est`.

Its output is an estimated error quantity.

An error estimate is distinct from exact mathematical error.

---

## 48. Residual Operator

For equation:

`F(x) = 0`

define residual:

`Res(x) = F(x)`.

A residual norm may be:

`||Res(x)||`.

Residual acceptance requires a separately defined criterion.

---

## 49. Differentiation Operator

For differentiable scalar function:

`f: R → R`

the derivative operator is:

`D f = df/dx`.

For multivariable scalar function:

`f: R^n → R`

the derivative structure includes its gradient.

---

## 50. Gradient Operator

For differentiable:

`f: R^n → R`

define:

`grad f: R^n → R^n`.

The gradient depends on the coordinate structure of the domain.

---

## 51. Jacobian Operator

For differentiable:

`F: R^n → R^m`

the Jacobian is:

`J_F(x) ∈ R^(m×n)`.

Its entries are the first partial derivatives of the output components with respect to input coordinates.

---

## 52. Hessian Operator

For twice-differentiable scalar:

`f: R^n → R`

the Hessian is:

`H_f(x) ∈ R^(n×n)`.

Its entries contain second partial derivatives.

---

## 53. Divergence Operator

For vector field:

`v: R^n → R^n`

the divergence is a scalar differential operator:

`div v`.

Its exact coordinate expression follows the selected coordinate system.

---

## 54. Laplacian Operator

For sufficiently differentiable scalar field:

`f`

the Laplacian is:

`Delta f = div(grad f)`.

The operator is distinct from discrete time-step notation:

`Delta t`.

Context and subscripts must prevent ambiguity.

---

## 55. Energy Operator

A scalar energy functional is:

`E: X_E → R`.

The input domain:

`X_E`

must be explicitly defined.

The energy operator is distinct from:

- ternary classification;
- resonance classification;
- phase order;
- validation.

---

## 56. Conservative Force Operator

Where:

`E: X_pos → R`

is differentiable, define:

`F_cons = -grad_R E`.

For atom `i`:

`F_i = -partial E / partial r_i`.

This produces a vector-valued force field on the coordinate domain.

---

## 57. Stress Operator

A stress operator has the form:

`S_sigma: X_sigma,src → X_stress`.

Its exact form depends on:

- geometry;
- boundary convention;
- virial convention;
- kinetic contribution;
- interaction model.

No universal stress operator is imposed in Volume 01.

---

## 58. Position-Difference Operator

For nonperiodic positions:

`r_i, r_j ∈ R^3`

define:

`D_ij = r_j - r_i`.

This returns:

`D_ij ∈ R^3`.

---

## 59. Distance Operator for Atomic Geometry

Define:

`d_ij = ||r_j - r_i||`.

For periodic geometry, the displacement operator must be replaced by the applicable periodic-image displacement operator.

---

## 60. Periodic-Wrap Operator

For a periodic simulation cell, define a coordinate wrapping operator:

`Wrap_cell: X_pos × X_cell → X_pos,wrapped`.

The exact coordinate convention depends on the selected cell representation.

Wrapping changes coordinate representation.

It does not by itself represent physical motion.

---

## 61. Minimum-Image Operator

Where the minimum-image convention is applicable, define:

`MI: X_disp × X_cell → X_disp`.

The output is the selected periodic representative displacement.

The operator is valid only under the geometric conditions of the chosen periodic model.

---

## 62. Neighbor Predicate

For geometry-dependent neighborhood relation, define:

`N_pred(i, j, x_conf) ∈ {true, false}`.

A common cutoff form may test:

`d_ij < r_c`.

The cutoff:

`r_c`

must be defined by the interaction model.

---

## 63. Neighbor-Set Operator

Define:

`N_i: X_conf → P(V)`

where:

`P(V)`

denotes the power set of the entity set.

The operator returns the declared neighborhood of entity `i`.

---

## 64. Graph-Construction Operator

A graph-construction operator is:

`G_build: X_conf → X_G`.

Its output is an interaction graph determined by declared geometry, topology, and model rules.

---

## 65. Adjacency Operator

For graph:

`G`

define an adjacency representation operator:

`Adj: X_G → X_adj`.

The target representation may be:

- matrix;
- edge list;
- indexed sparse structure.

Representation choice does not alter graph semantics.

---

## 66. Message Aggregation Operator

For graph messages:

`m_ij ∈ X_msg`

a permutation-compatible aggregation may be:

`Agg_i({m_ij | j ∈ N_i})`.

The aggregation codomain must be declared.

Common choices include:

- sum;
- mean;
- normalized sum.

---

## 67. Local Message Operator

A local message operator may have the form:

`M_ij: X_node × X_node × X_edge → X_msg`.

For entities `i` and `j`:

`m_ij = M_ij(z_i, z_j, e_ij)`.

---

## 68. Node-Update Operator

A node-update operator may have the form:

`U_node: X_node × X_msg,agg → X_node'`.

This operator updates a representation state.

It does not automatically update atomic geometry or ternary execution state.

---

## 69. Permutation Operator

For:

`pi ∈ S_N`

define the permutation action:

`rho_perm(pi): X_indexed → X_indexed`.

The operator reorders indexed components according to the declared action.

Semantic entity identity is preserved.

---

## 70. Translation Operator

For:

`a ∈ R^3`

define translation:

`T_a(r_i) = r_i + a`.

For a full atomic configuration, the operator acts consistently on all position components.

---

## 71. Rotation Operator

For:

`Q ∈ SO(3)`

define:

`R_Q(v) = Qv`.

For a collection of vectors, rotation acts componentwise according to the declared representation.

---

## 72. Orthogonal Transformation Operator

For:

`Q ∈ O(3)`

define:

`O_Q(v) = Qv`.

This operator includes both proper and improper orthogonal transformations.

---

## 73. Euclidean Transformation Operator

An element of:

`E(3)`

may be represented by:

`(Q, a)`

with:

`Q ∈ O(3)`

and:

`a ∈ R^3`.

Its action on position is:

`r → Qr + a`.

---

## 74. Group Action Operator

For transformation group:

`G_sym`

and state space:

`X`

define:

`rho_X: G_sym × X → X`.

For:

`g ∈ G_sym`

the state transforms as:

`x → rho_X(g, x)`.

Equivalent notation:

`rho_X(g)x`.

---

## 75. Invariant Operator

A mapping:

`F_inv: X → Y`

is invariant under the declared group action when:

`F_inv(rho_X(g)x) = F_inv(x)`.

---

## 76. Equivariant Operator

A mapping:

`F_eq: X → Y`

is equivariant when:

`F_eq(rho_X(g)x) = rho_Y(g)F_eq(x)`.

Both:

`rho_X`

and:

`rho_Y`

must be defined.

---

## 77. Symmetry-Averaging Operator

For finite transformation set:

`G_f`

an invariantization operator may be defined:

`A_G(F)(x) = (1/|G_f|) sum_(g∈G_f) F(rho_X(g)x)`.

Its validity depends on:

- finite `G_f`;
- additive codomain;
- defined averaging operation.

This is one construction of an invariant operator, not the only one.

---

## 78. Centering Operator

For positions:

`r_1, ..., r_N`

define center:

`r_bar = (1/N) sum_i r_i`.

A centering operation may be:

`C_pos(r_i) = r_i - r_bar`.

This removes global translation under the selected unweighted convention.

Mass-weighted centering is a distinct operator.

---

## 79. Mass-Weighted Center Operator

For masses:

`m_i > 0`

define:

`r_CM = (sum_i m_i r_i) / (sum_i m_i)`.

The corresponding centered position is:

`r_i' = r_i - r_CM`.

This operator requires a defined mass state.

---

## 80. Normalization Operator

For nonzero vector:

`x ∈ R^n`

define:

`Norm(x) = x / ||x||`.

Its domain excludes:

`x = 0`.

A zero-vector policy must be declared separately if normalization may encounter zero.

---

## 81. Feature Normalization Operator

A feature normalization operator may map:

`X_feat → X_feat,norm`.

Its exact form must declare:

- reference scale;
- mean or offset;
- variance or norm;
- zero-scale handling.

Feature normalization is distinct from physical nondimensionalization.

---

## 82. Nondimensionalization Operator

For dimensional quantity:

`q`

and nonzero reference scale:

`q_ref`

with compatible dimension, define:

`N_q(q) = q / q_ref`.

The result is dimensionless.

The reference scale is part of the operator definition.

---

## 83. Redimensionalization Operator

Given dimensionless:

`q_star`

and reference:

`q_ref`

define:

`R_q(q_star) = q_star q_ref`.

When paired consistently:

`R_q(N_q(q)) = q`.

---

## 84. Resonance Projection Operator

The canonical resonance projection is:

`P_R: X_src → X_R`.

Its role is to construct a resonance state:

`r = P_R(x)`.

The detailed coordinate construction belongs to the selected resonance model.

---

## 85. Resonance-Window Membership Predicate

Define:

`M_R: X_R → {false, true}`

with:

`M_R(r) = true`

when:

`r ∈ W_R`.

For state-dependent windows, extend the domain explicitly.

---

## 86. Resonance-Boundary Predicate

Define:

`B_R: X_R → {false, true}`

with:

`B_R(r) = true`

when:

`r ∈ ∂W_R`.

Exact boundary membership is a mathematical relation.

A numerical boundary tolerance is a separate computational predicate.

---

## 87. Resonance Classification Operator

Define:

`C_R: X_R → K_R`

where:

`K_R = {OUTSIDE, BOUNDARY, INSIDE}`.

The classifier must distinguish:

- interior;
- boundary;
- exterior

according to the topology and window definition.

---

## 88. History-Dependent Resonance Classification

For history-dependent classification:

`C_RH: X_R × X_H → K_R`.

This operator explicitly includes history state in its domain.

---

## 89. Topology-Dependent Resonance Operator

For topology-dependent resonance:

`P_RTg: X_src × X_G → X_R`.

The topology state is an explicit operator argument.

---

## 90. Scale-Dependent Resonance Operator

For:

`ell ∈ L`

a scale-dependent resonance projection may be:

`P_R^(ell): X^(ell) → X_R^(ell)`.

Scale identity remains explicit.

---

## 91. Phase-Order Operator

For:

`Theta ∈ (S^1)^N`

define:

`O_R(Theta) = |(1/N) sum_j exp(i theta_j)|`.

Equivalent real form:

`O_R(Theta) = sqrt(mean(cos(theta))^2 + mean(sin(theta))^2)`.

The codomain is:

`[0, 1]`.

---

## 92. Coherence Operator

A coherence operator is independently defined:

`O_C: X → X_C`.

The architecture preserves:

`O_R ≠ O_C`

unless a selected model explicitly identifies them.

---

## 93. Phase-Locking Predicate

A phase-locking predicate may be defined:

`L_ij: X_phase × X_H → {false, true}`

where history is included if locking is evaluated over an interval.

The exact criterion is model-specific.

---

## 94. Synchronization Operator

A synchronization classifier or observable is represented by its own mapping:

`S_sync: X → K_sync`

or:

`O_sync: X → Y_sync`.

It is not replaced by resonance classification.

---

## 95. Coupling Operator

A generic pairwise coupling operator is:

`K_pair: X_i × X_j × P_K → Y_K`.

The output may be:

- scalar;
- vector;
- phase contribution;
- message;
- interaction descriptor.

The physical meaning is defined by the selected model.

---

## 96. Kuramoto Coupling Operator

For phase states:

`theta_i, theta_j ∈ S^1`

a classical pairwise phase interaction may be:

`K_K(theta_i, theta_j) = sin(theta_j - theta_i)`.

The subtraction is interpreted circularly.

---

## 97. Sakaguchi Coupling Operator

With phase lag:

`gamma`

define:

`K_S(theta_i, theta_j, gamma) = sin(theta_j - theta_i - gamma)`.

The parameter:

`gamma`

is a phase lag.

It is not a temporal delay.

---

## 98. Weighted Phase-Coupling Operator

For weights:

`w_ij`

define:

`K_i(Theta) = sum_j w_ij sin(theta_j - theta_i - gamma_ij)`.

The weight matrix and phase-lag structure must be declared by the selected model.

---

## 99. Local Phase-Lag Operator

Where the receiving state determines phase lag:

`Gamma: X_i → S^1`

define:

`gamma_i = Gamma(x_i)`.

A pairwise phase interaction may then use:

`sin(theta_j - theta_i - gamma_i)`.

The operator semantics remain distinct from pairwise delay.

---

## 100. Frequency-Update Operator

A frequency-state update may be defined:

`F_omega: X_omega × X_aux → X_omega`.

For relaxation toward target:

`omega_next = omega + alpha_omega (omega_target - omega)`.

The coefficient and target construction are model-specific.

---

## 101. Relaxation Operator

For state:

`x`

target:

`x_target`

and coefficient:

`alpha`

define:

`Relax(x, x_target; alpha) = x + alpha(x_target - x)`.

For convex interpolation:

`0 ≤ alpha ≤ 1`.

Other parameter ranges require separate analysis.

---

## 102. Exponential Relaxation Flow

For continuous relaxation:

`dx/dt = lambda(x_target - x)`

with:

`lambda > 0`.

This is a continuous dynamical operator distinct from the discrete relaxation update.

---

## 103. Delay Operator

For history state:

`h ∈ X_H`

and delay:

`tau ≥ 0`

define:

`D_tau(h) = h(-tau)`

when the history representation is centered at the current time and supports this evaluation.

---

## 104. History-Shift Operator

A history state may evolve through a shift operator:

`Shift_Delta_t: X_H → X_H`.

The exact function-space action depends on the history representation.

---

## 105. History-Append Operator

For retained discrete history:

`h`

and newly committed state:

`x_new`

define:

`Append_H(h, x_new)`.

The operator must preserve the ordering semantics of the history state.

---

## 106. Memory-Update Operator

A memory state may evolve through:

`M_update: X_M × X → X_M`.

The update rule is model-specific.

Any memory affecting future evolution must remain explicit.

---

## 107. Hysteresis Operator

A hysteretic operator has the general form:

`Hys: X_current × X_M → Y × X_M`.

The output depends on both current input and retained memory state.

This distinguishes hysteresis from memoryless classification.

---

## 108. Exponential Moving Memory Operator

A simple retained memory update may be:

`m_next = beta m + (1 - beta)x`

for:

`0 ≤ beta ≤ 1`.

The spaces of `m` and `x` must support the required linear combination.

---

## 109. Saturating Memory Operator

A memory update may combine relaxation and clipping:

`m_next = clip(Relax(m, x; alpha); a, b)`.

The bounds and parameters belong to the model definition.

---

## 110. Graph Message Operator

For edge:

`(i, j)`

a message operator may be:

`M: X_node × X_node × X_edge → X_msg`.

This forms the elementary local interaction operator in message-passing architectures.

---

## 111. Message Aggregation

For entity `i`:

`m_i = Agg({m_ij | j ∈ N_i})`.

The aggregation must satisfy the required permutation behavior.

---

## 112. Equivariant Message Operator

A message operator is equivariant when its transformation under the declared group action satisfies the corresponding output action.

The exact transformation equation depends on:

- node representation;
- edge representation;
- output representation.

---

## 113. Invariant Readout Operator

A global invariant readout may have the form:

`R_inv: X_node^N → Y_inv`.

The operator must preserve the declared permutation and spatial invariances.

---

## 114. Local Equivariant Readout Operator

A local equivariant readout may have the form:

`R_eq: X_node → Y_eq`

with:

`R_eq(rho_X(g)x) = rho_Y(g)R_eq(x)`.

---

## 115. Energy Readout Operator

An interatomic energy model may define:

`E_total = sum_i E_i`

where each local energy contribution:

`E_i`

is produced by a model-defined invariant local operator.

The decomposition itself belongs to the selected energy model.

---

## 116. Force-from-Energy Operator

Given differentiable:

`E_total(R_pos)`

define:

`F_i = -partial E_total / partial r_i`.

This operator couples scalar energy to vector force through differentiation.

---

## 117. Virial-Type Operator

A model may define a virial-type tensor from positions and forces.

Its exact normalization, sign convention, kinetic contribution, and periodic-cell treatment must be declared by the molecular-dynamics model.

No single virial convention is imposed here.

---

## 118. Feature Concatenation Operator

For feature spaces:

`X_1`

and:

`X_2`

define:

`Concat: X_1 × X_2 → X_1 × X_2`.

Concatenation preserves both components without semantic mixing.

---

## 119. Feature Projection Operator

A feature projection may be:

`P_feat: X_feat → X_red`.

If dimension reduction occurs, information loss must be characterized.

---

## 120. Linear Operator

For vector spaces:

`V`

and:

`W`

a mapping:

`L: V → W`

is linear when:

`L(a x + b y) = aL(x) + bL(y)`.

TR-EIF does not assume all operators are linear.

---

## 121. Affine Operator

An affine operator has the form:

`A(x) = L(x) + b`

where:

`L`

is linear and:

`b`

is fixed in the codomain.

---

## 122. Nonlinear Operator

Any operator not satisfying the relevant linearity relation is nonlinear.

Nonlinearity may arise through:

- activation;
- phase interaction;
- normalization;
- thresholding;
- geometric dependence;
- state-dependent coupling;
- saturation.

---

## 123. Local Linearization Operator

For differentiable:

`F`

near reference state:

`x_0`

define the first-order local approximation:

`F(x) ≈ F(x_0) + J_F(x_0)(x - x_0)`.

This is a local approximation.

It does not replace `F` globally.

---

## 124. Differential Operator on Phase State

For phase trajectory:

`theta_i(t) ∈ S^1`

the angular velocity is represented locally by:

`d theta_i / dt`.

Its numerical representative depends on the chosen local chart or wrapped-difference convention.

---

## 125. Discrete Phase-Step Operator

A discrete wrapped phase update may be written:

`theta_i[n+1] = Wrap(theta_i[n] + Delta theta_i[n])`.

The increment:

`Delta theta_i[n]`

must be defined by the selected numerical phase model.

---

## 126. Continuous-to-Discrete Event Operator

A continuous state may generate an event through:

`E_cd: X_c → X_event`.

The event may then generate a ternary target through a separate operator.

This preserves:

`continuous state`

`→ event`

`→ target`

`→ execution`

as distinct stages where the model uses them.

---

## 127. Resonance-to-Ternary Operator

A canonical typed interface is:

`P_RT: X_R → T_target`.

For history dependence:

`P_RT: X_R × X_H → T_target`.

This operator does not mutate:

`T_exec`.

---

## 128. Ternary Execution Operator

Define:

`E_T: X_Texec × X_ctrl → X_Texec`.

This operator applies:

- transition admissibility;
- neutral mediation;
- pending routing;
- retention;
- authorization.

The exact decomposition may be implemented through several suboperators.

---

## 129. Ternary Execution Invariant

For every valid execution:

`t_exec,next ∈ {-1, 0, 1}`.

No execution operator may produce any other retained ternary state.

---

## 130. Direct-Opposite Guard

Define:

`G_opp: T_exec × T_target → {true, false}`

where:

`G_opp = true`

exactly when current and target states are opposite polarity.

When:

`G_opp = true`

the direct target cannot be committed in one event.

---

## 131. First-Leg Operator

For opposite-polarity state and target:

`FirstLeg: T_exec × T_target → T_exec`

with:

`FirstLeg(-1, 1) = 0`

`FirstLeg(1, -1) = 0`.

---

## 132. Pending-Route Initialization Operator

Define:

`InitPending: T_exec × T_target → X_pending`.

For opposite polarity:

`InitPending(-1, 1) = 1`

`InitPending(1, -1) = -1`.

---

## 133. Second-Leg Operator

A second-leg operator acts only when:

- current executed state is `0`;
- a valid pending destination exists;
- authorization is satisfied.

Its output is the pending polarity.

The operator cannot execute from the first-leg event alone.

---

## 134. Neutral Retention Operator

Define:

`NeutralHold(0) = 0`.

The number of repeated neutral-retention events is unconstrained at the framework level unless a specialization defines an additional condition.

---

## 135. Same-State Retention Operator

For:

`t ∈ T`

define:

`Hold_T(t) = t`.

This operator permits retained state under an admissible no-change event.

---

## 136. Interatomic-to-Representation Operator

Define:

`P_E: X_EIF → X_EQ`

for the selected equivariant representation.

The operator may depend on geometry, topology, species, and local environments.

---

## 137. Equivariant-to-Resonance Operator

Define:

`P_ER: X_EQ → X_R`.

This operator forms the explicit interface between EIF representation and resonance state.

---

## 138. Forward TR-EIF Integration Operator

A general forward operator may be:

`F_E→TR: X_EIF × X_H × P → X_TR,in`.

Only required arguments are included by the selected model.

The operator must preserve:

- domain typing;
- symmetry behavior;
- scale identity;
- dimensional semantics.

---

## 139. Reverse TR-EIF Integration Operator

A reverse operator may be:

`F_TR→E: X_TR × X_EIF × P → X_EIF,req`.

Its output is an EIF update request.

It is not an automatic interatomic state mutation.

---

## 140. Feedback Commit Operator

An accepted EIF request may be applied through:

`Commit_EIF: X_EIF × X_EIF,auth → X_EIF`.

The authorization structure must correspond to the requested update.

---

## 141. Cross-Layer Projection Operator

A cross-layer projection:

`P_XY: X → Y`

must define:

- source representation;
- target representation;
- retained information;
- discarded information.

---

## 142. Injectivity Test Operator

For a finite fixture or analytically defined domain, injectivity may be evaluated through a predicate:

`Test_inj(F, D)`.

This computational operator is distinct from a general mathematical proof of injectivity.

---

## 143. Symmetry Test Operator

For:

`F: X → Y`

define a transformation residual:

`E_eq(g, x) = d_Y(F(rho_X(g)x), rho_Y(g)F(x))`.

Exact equivariance corresponds to zero residual under an exact metric-compatible representation.

Numerical qualification may use a declared tolerance.

---

## 144. Invariance Test Operator

For invariant:

`F`

define:

`E_inv(g, x) = d_Y(F(rho_X(g)x), F(x))`.

The comparison rule depends on the codomain.

---

## 145. Permutation-Aggregation Operator

A symmetric aggregation operator:

`Agg`

satisfies:

`Agg(x_1, ..., x_N) = Agg(x_(pi(1)), ..., x_(pi(N)))`

for:

`pi ∈ S_N`.

Sum and mean are examples on compatible spaces.

---

## 146. Scale-Transfer Operator

For:

`ell_a, ell_b ∈ L`

define:

`M_(ell_a→ell_b): X^(ell_a) → X^(ell_b)`.

Its semantics must define:

- aggregation;
- projection;
- closure;
- uncertainty;
- dimensional transformation.

---

## 147. Coarse-Graining Operator

A coarse-graining operator has the form:

`C_ab: X^(ell_a) → X^(ell_b)`

for a transition from finer to coarser scale.

It may be non-injective.

Information loss must be explicit.

---

## 148. Refinement Operator

A refinement operator has the form:

`R_ba: X^(ell_b) → X^(ell_a)`.

A refinement generally requires additional closure information when the coarse state does not uniquely determine the fine state.

---

## 149. Uncertainty-Propagation Operator

Define:

`U_prop: X × X_U → X_U'`.

The operator propagates an uncertainty representation through a declared model relation.

Its form depends on the uncertainty representation.

---

## 150. Domain-Detection Operator

Define:

`D_dom: X → K_D`.

The codomain:

`K_D`

is a domain-status classification space.

It is distinct from:

`T`

and:

`K_R`.

---

## 151. Loss Operator

For trainable parameters:

`theta_param ∈ Theta`

and data:

`d ∈ D`

define:

`L: Theta × D → R`.

The loss is a scalar optimization quantity.

It is not automatically physical energy.

---

## 152. Composite Loss Operator

For loss components:

`L_1, ..., L_m`

and weights:

`lambda_1, ..., lambda_m`

define:

`L_total = sum_j lambda_j L_j`.

The weighting convention must preserve meaningful scaling of all components.

---

## 153. Ternary Regularization Operator

A ternary regularizer may be defined:

`Omega_T: X_feat → R`.

Its exact form belongs to Volume 04.

The operator must not alter the exact execution state domain:

`T = {-1, 0, 1}`.

---

## 154. Resonance Regularization Operator

A resonance regularizer may be:

`Omega_R: X_R → R`

or operate on derived resonance descriptors.

Its definition must preserve the distinction between optimization objective and resonance state.

---

## 155. Equivariance Regularization Operator

An equivariance penalty may use transformation residual:

`Omega_EQ = E_eq(g, x)`.

Aggregated versions may average or sum over fixtures and transformations.

---

## 156. Gradient-Based Optimization Operator

For differentiable loss:

`L(theta_param)`

a gradient step may be:

`theta_next = theta_param - eta grad L(theta_param)`.

The learning rate:

`eta`

is an optimization parameter.

---

## 157. Generic Optimizer Operator

A stateful optimizer has the form:

`Opt: Theta × X_opt × X_grad → Theta × X_opt`.

Optimizer state remains explicit.

---

## 158. Equation-of-Motion Operator

For molecular dynamics, a state derivative operator may be:

`F_MD: X_MD → T(X_MD)`

where:

`T(X_MD)`

denotes the applicable tangent structure.

For Cartesian positions and momenta, the equations are expressed componentwise.

---

## 159. Position Evolution Operator

For particle `i`:

`dr_i/dt = v_i`

or:

`dr_i/dt = p_i / m_i`

depending on the selected state representation.

---

## 160. Momentum Evolution Operator

For force:

`F_i`

the momentum equation is:

`dp_i/dt = F_i`

for the standard Newtonian form.

Additional terms require their own model definition.

---

## 161. Velocity Evolution Operator

Where velocity state is used:

`dv_i/dt = F_i / m_i`

for:

`m_i > 0`.

---

## 162. Thermostat Operator

A thermostat operator acts on the extended molecular-dynamics state according to its selected formalism.

The exact operator is defined in Volume 05.

No universal thermostat operator is imposed here.

---

## 163. Barostat Operator

A barostat operator acts on:

- cell state;
- momentum or velocity state;
- internal barostat state

according to the selected barostat model.

Its detailed definition belongs to Volume 05.

---

## 164. Conservation Diagnostic Operator

For quantity:

`Q: X → R`

define conservation deviation:

`Delta_Q(t) = Q(x(t)) - Q(x(0))`.

For discrete execution:

`Delta_Q[n] = Q(x[n]) - Q(x[0])`.

This is a diagnostic operator.

---

## 165. Relative Conservation Error Operator

Where:

`Q(x[0]) ≠ 0`

define:

`E_Q,rel[n] = |Q(x[n]) - Q(x[0])| / |Q(x[0])|`.

The operator is undefined at zero denominator unless an alternative convention is declared.

---

## 166. Transport Observable Operator

A transport observable is represented by a mapping:

`O_transport: X_MD × X_H → Y_transport`

where history is included when the observable depends on time correlations.

The detailed operators belong to Volume 05.

---

## 167. Time-Average Operator

For continuous observable:

`y(t)`

over interval:

`[t_0, t_1]`

with:

`t_1 > t_0`

define:

`Avg_t(y) = (1/(t_1 - t_0)) integral_(t_0)^(t_1) y(t) dt`.

The integral notation here denotes the standard definite integral.

---

## 168. Discrete-Time Average Operator

For sequence:

`y[0], ..., y[N-1]`

define:

`Avg_N(y) = (1/N) sum_(k=0)^(N-1) y[k]`.

---

## 169. Correlation Operator

For suitable scalar or vector observables, a correlation operator may be defined over time or ensemble state.

Its exact normalization and statistical assumptions must be stated by the selected model.

---

## 170. Autocorrelation Operator

A generic stationary-form autocorrelation may be written:

`C_A(tau) = <A(t) A(t + tau)>`.

The averaging operator and stationarity assumptions must be defined in the applicable context.

---

## 171. Differentiable Composition Operator

For differentiable:

`F: X → Y`

and:

`G: Y → Z`

the derivative of composition follows the chain rule:

`D(G ∘ F)(x) = DG(F(x)) DF(x)`.

This becomes relevant for learned interatomic energy and force construction.

---

## 172. Gradient Through Representation Operator

If:

`E = E_model(P_E(R_pos))`

then the force gradient is obtained through the derivative of the complete composition.

The representation mapping therefore participates in the derivative chain.

---

## 173. Symmetrization Operator

A tensor symmetrization operator may be defined:

`Sym(A) = (A + A^T)/2`.

Its domain is a square matrix space.

---

## 174. Antisymmetrization Operator

Define:

`Skew(A) = (A - A^T)/2`.

Then:

`A = Sym(A) + Skew(A)`.

---

## 175. Trace Operator on Matrices

For square matrix:

`A ∈ R^(n×n)`

define:

`tr(A) = sum_i A_ii`.

This matrix trace is distinct from execution trace artifacts.

Context must make the meaning explicit.

---

## 176. Determinant Operator

For square matrix:

`A`

define:

`det(A)`.

For simulation-cell matrix:

`H`

the cell volume magnitude may be related to:

`|det(H)|`

under the selected geometric convention.

---

## 177. Inverse Operator

For invertible mapping or matrix, an inverse may be defined.

For matrix:

`A`

with:

`det(A) ≠ 0`

the matrix inverse is:

`A^(-1)`.

An inverse is not assumed for non-injective mappings.

---

## 178. Pseudoinverse Operator

Where applicable, a generalized inverse may be introduced explicitly.

The existence of a pseudoinverse does not make the original mapping bijective.

---

## 179. Indicator Operator

For set:

`A ⊆ X`

define:

`1_A: X → {0, 1}`

with:

`1_A(x) = 1`

when:

`x ∈ A`

and:

`1_A(x) = 0`

otherwise.

This binary output is not active-neutral ternary state.

---

## 180. Membership Operator

Set membership is represented by:

`x ∈ A`.

A machine implementation may use a Boolean predicate corresponding to this relation.

---

## 181. Boundary-Distance Operator

For metric state space and set:

`A`

define:

`d_A(x) = inf_(a∈A) d(x, a)`.

For resonance boundary:

`d_boundary(r) = inf_(b∈∂W_R) d_R(r, b)`.

Numerical use requires a defined metric and computable representation.

---

## 182. Projection onto Constraint Set

For a metric space and admissible set:

`X_adm`

a projection operator may be written:

`Proj_Xadm(x)`.

Existence and uniqueness depend on the geometry of the set and metric.

No universal projection is assumed.

---

## 183. Constraint Predicate

For admissible state set:

`X_adm`

define:

`C_adm: X → {true, false}`

by:

`C_adm(x) = true`

if:

`x ∈ X_adm`.

---

## 184. Dimensional-Compatibility Predicate

Define:

`D_comp(a, b) = true`

when:

`dim(a) = dim(b)`.

This predicate is required for direct addition or subtraction of dimensional quantities.

---

## 185. Unit-Conversion Operator

For compatible units:

`U_a`

and:

`U_b`

define:

`Conv_(a→b): X_(U_a) → X_(U_b)`.

The conversion preserves physical dimension while changing numerical representation.

---

## 186. Serialization Operator

A serialization operator is:

`Ser: X_art → B_ser`.

Its codomain is a serialized representation space.

Serialization does not change the formal mathematical meaning of the underlying object.

---

## 187. Deserialization Operator

Define:

`Des: B_ser,valid → X_art`.

For a lossless semantic serialization:

`Des(Ser(x)) ≡ x`.

---

## 188. Checkpoint Projection Operator

Define:

`P_CP: X_comp → X_CP`.

The operator selects or encodes all state required for restart under the declared checkpoint contract.

---

## 189. Restore Operator

Define:

`Restore: X_CP,valid → X_comp`.

Restore reconstructs computational state.

It does not perform a model-evolution step.

---

## 190. Trace Projection Operator

Define:

`P_trace: X_exec → X_trace`.

A trace projection selects the execution information required by its declared trace contract.

---

## 191. Validation Operator

A validation operator has the form:

`V: X_val → K_val`

where:

`K_val = {PASS, FAIL, UNRESOLVED}`.

Validation output remains separate from model state.

---

## 192. Exact-Invariant Validator

For invariant predicate:

`I: X → {true, false}`

define:

`V_I(x) = PASS`

when:

`I(x) = true`

and:

`V_I(x) = FAIL`

when:

`I(x) = false`.

`UNRESOLVED`

is used only when the evidence required to evaluate `I` is unavailable or insufficient under the validation contract.

---

## 193. Numerical-Comparison Operator

For metric:

`d`

and tolerance:

`epsilon ≥ 0`

define:

`Cmp_epsilon(a, b) = true`

when:

`d(a, b) ≤ epsilon`.

The operator is valid only for variables admitting tolerance-based comparison.

---

## 194. Mixed-State Comparison Operator

For composite state:

`x = (x_1, ..., x_n)`

a comparison operator may combine component-specific relations:

`Cmp_X(x, y) = AND_i Cmp_i(x_i, y_i)`.

Each component comparison uses the semantics appropriate to its state space.

---

## 195. Exact Ternary Comparison

For:

`t_a, t_b ∈ T`

define:

`Cmp_T(t_a, t_b) = true`

if and only if:

`t_a = t_b`.

No numerical tolerance is permitted.

---

## 196. Circular Phase Comparison

For:

`theta_a, theta_b ∈ S^1`

define:

`Cmp_phase(theta_a, theta_b; epsilon)`

through:

`d_S1(theta_a, theta_b) ≤ epsilon`.

Exact circular equality corresponds to zero circular distance.

---

## 197. Symmetry-Residual Operator

For equivariant:

`F`

define:

`Res_EQ(g, x) = d_Y(F(rho_X(g)x), rho_Y(g)F(x))`.

This operator supports numerical equivariance checking.

---

## 198. Permutation-Residual Operator

For permutation:

`pi ∈ S_N`

define:

`Res_perm(pi, x)`

using the declared output permutation action.

The exact metric depends on the output space.

---

## 199. Conservation-Residual Operator

For quantity:

`Q`

define:

`Res_Q(x_t, x_0) = Q(x_t) - Q(x_0)`.

A numerical conservation validator may evaluate its magnitude under a declared tolerance.

---

## 200. Transition-Trace Validator

A ternary transition validator operates on an ordered sequence of executed states.

For each adjacent pair:

`(t_exec[k], t_exec[k+1])`

it tests the committed transition relation.

A valid trace contains no:

`-1 → 1`

or:

`1 → -1`.

---

## 201. Pending-Route Validator

A pending-route validator checks consistency among:

- current executed state;
- target;
- pending destination;
- committed transition;
- later completion event.

It must detect collapsed opposite-polarity transitions.

---

## 202. Active-Neutral Validator

An active-neutral validator checks that:

`0`

is treated as a valid state and is not conflated with:

- absence;
- invalidity;
- error;
- unresolved validation.

---

## 203. Resonance-Ternary Separation Validator

This validator verifies that resonance classification and ternary state occupy separate fields or spaces unless an explicit mapping connects them.

---

## 204. R-C Separation Validator

Where both observables exist, the validator checks that:

`R`

and:

`C`

are separately defined and separately stored or computed.

The invariant remains:

`R(t) ≠ C(t)`.

---

## 205. Delay-Lag Separation Validator

A delay-lag validator verifies that:

- delayed state access uses explicit history;
- phase lag modifies phase relation;
- neither mechanism is silently substituted for the other.

---

## 206. State-Observable Separation Validator

This validator verifies that an observable computation does not mutate retained state unless an explicit update operator is defined.

---

## 207. Local-Global Separation Validator

This validator verifies that local states and global aggregates remain separately represented.

---

## 208. Dimensional Validator

A dimensional validator checks the dimensional admissibility of operations involving physical quantities.

It rejects direct addition or subtraction of incompatible dimensions.

---

## 209. State-Domain Validator

For any declared state space:

`X`

define:

`V_X: X_candidate → {true, false}`

to test admissibility.

The actual computational implementation may require a broader candidate carrier than the formal state space.

---

## 210. Operator Closure

An operator is closed on state space:

`X`

when:

`A: X → X`.

Closure must be stated explicitly.

Not every operator in TR-EIF is closed on its domain space.

---

## 211. Operator Invariance

An operator may preserve a property:

`I`

when:

`I(x) = true`

implies:

`I(A(x)) = true`

for all admissible:

`x`.

The property and domain must be specified.

---

## 212. Ternary-Domain Preservation

Every ternary execution operator must satisfy:

`t_exec ∈ T`

implies:

`t_exec,next ∈ T`.

Thus:

`T`

is invariant under valid ternary execution.

---

## 213. Neutral-Mediation Preservation

Every operator that can commit ternary state must preserve the exclusion of direct opposite transitions.

No surrounding EIF, MD, learning, or multiscale operator may bypass this condition.

---

## 214. Symmetry Preservation

A composed operator preserves a declared symmetry only if the complete composition satisfies the relevant invariant or equivariant relation.

Symmetry of one suboperator does not automatically establish symmetry of the whole composition.

---

## 215. Dimensional Preservation

A dimension-preserving operator satisfies:

`dim(A(x)) = dim(x)`

where such comparison is meaningful.

Dimension-changing operators must declare the transformation explicitly.

---

## 216. Information-Preserving Operator

An injective operator preserves distinguishability of source states over its domain.

For:

`A: X → Y`

injectivity means:

`A(x_1) = A(x_2)`

implies:

`x_1 = x_2`.

---

## 217. Information-Losing Operator

A non-injective operator maps at least two distinct source states to the same target state.

Such information loss is explicit.

---

## 218. Idempotent Operator

An operator:

`A: X → X`

is idempotent when:

`A(A(x)) = A(x)`.

Examples may include specific projection or canonicalization operators where defined.

---

## 219. Involution

An operator:

`A: X → X`

is an involution when:

`A(A(x)) = x`.

No TR-EIF operator is assumed involutive without explicit proof or construction.

---

## 220. Commuting Operators

Two operators:

`A`

and:

`B`

commute on their common admissible domain when:

`A(B(x)) = B(A(x))`.

Commutativity is not assumed.

---

## 221. Noncommuting Execution Operators

Execution operators involving:

- state update;
- scheduling;
- commit;
- history;
- memory

may be order-sensitive.

Their order must therefore be part of the execution contract.

---

## 222. Associative Operator

A binary operator:

`*`

is associative when:

`(a * b) * c = a * (b * c)`.

Associativity must be established for the selected operator and domain.

---

## 223. Commutative Operator

A binary operator is commutative when:

`a * b = b * a`.

Graph message aggregation may use commutative operators where permutation invariance is required.

---

## 224. Neutral Element

For binary operator:

`*`

an algebraic neutral element:

`e`

satisfies:

`e * x = x * e = x`.

An algebraic neutral element is conceptually distinct from active ternary state `0`.

The two must not be identified without an explicit algebraic construction.

---

## 225. Inverse Element

For a binary operation with identity:

`e`

an inverse of:

`x`

is an element:

`x^(-1)`

such that:

`x * x^(-1) = e`

where defined.

Balanced ternary opposite polarity is not an algebraic inverse relation by default.

---

## 226. Operator Ordering

For ordered execution:

`A_1, A_2, ..., A_n`

the composite update is:

`A_n ∘ ... ∘ A_2 ∘ A_1`.

Changing operator order may change the result when the operators do not commute.

---

## 227. Scheduler as Operator Selector

A scheduler may be represented as selecting an operator from an admissible family:

`S: X_sched × X → A_set`.

The selected operator is then applied under the execution contract.

The scheduler does not redefine the mathematical meaning of the operator.

---

## 228. Conditional Operator

A conditional operator may be defined:

`A(x) = A_1(x)`

when predicate:

`G(x) = true`

and:

`A(x) = A_2(x)`

otherwise.

Both branches require compatible output semantics.

---

## 229. Event-Triggered Operator

An event-triggered update applies only when its event guard is satisfied.

The event and update remain distinct mathematical objects.

---

## 230. Operator with Memory

A stateful operator has the form:

`A: X × X_M → Y × X_M`.

Its output depends on retained memory and may update that memory.

---

## 231. Operator with History

A history-dependent operator has the form:

`A_H: X × X_H → Y`.

History is part of the domain.

---

## 232. Operator with Delay

A delay-dependent operator explicitly invokes:

`D_tau`

or another history-access operation.

Delay cannot be hidden inside an operator described as memoryless.

---

## 233. Operator with Scale

A scale-aware operator may be:

`A: X × L → Y`

or a family:

`A^(ell): X^(ell) → Y^(ell)`.

Scale identity remains explicit.

---

## 234. Operator with Topology

A topology-dependent operator may be:

`A_G: X × X_G → Y`.

Changing graph topology may therefore change operator output.

---

## 235. Operator with Parameters

A parameterized operator is:

`A_p: X → Y`

for:

`p ∈ P`.

Equivalently:

`A: X × P → Y`.

Parameter dependence must be explicit when result-affecting.

---

## 236. Trainable Operator

A trainable operator may be:

`F_theta: X → Y`

with:

`theta_param ∈ Theta`.

The learned parameter state is external to the physical input state unless the model explicitly includes adaptation during evolution.

---

## 237. Deterministic Operator

An operator is deterministic when identical complete inputs and state produce the same output under the declared execution semantics.

Determinism is defined relative to the complete result-affecting domain.

---

## 238. Stochastic Operator

A stochastic operator may be represented as:

`A: X × X_rng → Y × X_rng`.

Random state is explicit.

---

## 239. Operator Purity

A pure operator returns output without mutating retained external state.

Its semantics are completely represented by its explicit inputs and outputs.

---

## 240. Stateful Operator

A stateful operator changes retained state.

Its state transition must be represented explicitly in its codomain or execution contract.

---

## 241. Numerical Encoding Operator

A mathematical state may be encoded through:

`Enc: X_math → X_num`.

The encoding must preserve the information required by the computational realization.

---

## 242. Numerical Decoding Operator

A decoding operator is:

`Dec: X_num,valid → X_math`.

For exact lossless encoding:

`Dec(Enc(x)) = x`.

For approximate encoding, the applicable equivalence relation must be defined.

---

## 243. Quantization Operator

A quantization operator maps a continuous numerical domain into a finite representable set:

`Q_num: X_cont → X_quant`.

Quantization is a numerical operation.

It is distinct from balanced ternary classification.

---

## 244. Dequantization Operator

A dequantization operator maps encoded finite values into their reconstructed numerical representation.

It does not recover information discarded by quantization unless the encoding was lossless over the source domain.

---

## 245. Fixed-Point Scaling Operator

A fixed-point representation may use:

`Enc_q(x) = round(s x)`

for scale:

`s > 0`.

The corresponding reconstructed value may be:

`Dec_q(n) = n / s`.

Rounding and overflow behavior must be defined.

---

## 246. Numerical Saturation Operator

A finite-range implementation may define:

`Sat_num: X_num → X_num,bounded`.

This remains a computational representation operator.

It is not automatically a physical saturation mechanism.

---

## 247. Overflow Operator

Where overflow is possible, its behavior must be explicitly defined as:

- error;
- saturation;
- modular wrap;
- another declared rule.

No default semantic interpretation is assumed.

---

## 248. Interpolation Operator

For state values at known coordinates, an interpolation operator reconstructs an intermediate numerical value.

Its form depends on the state space.

Linear interpolation is not generally valid for:

- categorical ternary state;
- arbitrary graph state;
- circular phase without circular treatment.

---

## 249. Linear Interpolation

For vector-space values:

`x_0`

and:

`x_1`

define:

`Interp(lambda) = (1 - lambda)x_0 + lambda x_1`

for:

`lambda ∈ [0, 1]`.

---

## 250. Circular Interpolation

Phase interpolation must follow a declared path on:

`S^1`.

Ordinary linear interpolation of representatives can be invalid across the branch cut.

---

## 251. Ternary Interpolation Prohibition

No continuous interpolation is defined between ternary categorical states by default.

In particular, a transition:

`-1 → 1`

cannot be represented as continuous interpolation through arbitrary real values.

Its execution path is:

`-1 → 0 → 1`.

---

## 252. Event Localization Operator

A numerical event-localization operator determines an estimated event coordinate from numerical trajectory information.

Its output is a numerical estimate.

It does not classify the event as a bifurcation.

---

## 253. Bifurcation Analysis Operator

A bifurcation-analysis operator acts on a parameterized dynamical-system family and the mathematical structures required by the selected bifurcation criterion.

Threshold classification is not a substitute for such an operator.

---

## 254. Structural Classification Operator

A structural classifier is:

`C_struct: X_S → K_struct`.

It is independent of ternary transition classification unless explicitly connected.

---

## 255. Physical Phase Classification Operator

A physical phase classifier is:

`C_phys: X_phys → K_phys`.

It must be defined from the selected physical model and observables.

---

## 256. Scientific Separation Operators

Distinct classifiers and observables must remain separately implemented for:

- resonance;
- synchronization;
- phase locking;
- coherence;
- phase order;
- structural state;
- physical phase state;
- ternary state.

No universal shared classifier is defined.

---

## 257. Canonical Operator Chain

The principal TR-EIF computational chain may be represented by operators:

`X_EIF`

`→ P_E`

`X_EQ`

`→ P_ER`

`X_R`

`→ C_R`

`K_R`

`→ P_RT`

`T_target`

`→ E_T`

`T_exec`

`→ F_TR→E`

`X_EIF,req`.

Each arrow has a distinct mathematical role.

---

## 258. Forward Integration Composition

Where the relevant domains align, the forward representation chain may be composed as:

`P_ER ∘ P_E`.

Its typed form is:

`X_EIF → X_R`.

A further ternary-target composition is:

`P_RT ∘ P_ER ∘ P_E`.

Its codomain is:

`T_target`.

---

## 259. Execution Boundary

The operator:

`P_RT`

ends at:

`T_target`.

The transition from:

`T_target`

to:

`T_exec`

is governed by:

`E_T`

and its associated guards, routing, and control state.

Therefore:

`P_RT ≠ E_T`.

---

## 260. Feedback Composition

A feedback chain may contain:

`F_TR→E`

followed by an EIF authorization and commit operator.

The result is committed EIF state only after the applicable update contract is satisfied.

---

## 261. Learning-to-Model Operator

Training produces parameters through an optimization operator:

`Train: D × Theta_init → Theta_trained`

together with any required optimizer state and configuration.

The trained parameter state then parameterizes selected EIF or TR operators.

---

## 262. Model-to-Dynamics Operator

A trained interatomic model may provide energy, force, or other outputs used by molecular-dynamics evolution operators.

The mapping from model output into dynamics must preserve dimensional type.

---

## 263. Dynamics-to-Observable Operator

A molecular-dynamics trajectory may be projected through:

`O_MD: X_MD × X_H → Y_obs`.

Transport observables may require history-dependent operators.

---

## 264. Atomistic-to-Multiscale Operator

A scale-transfer operator may map atomistic state or observables into mesoscale or continuum variables.

Its definition must specify:

- averaging;
- projection;
- closure;
- uncertainty.

---

## 265. FRP Executable Operator Boundary

FRP may instantiate selected TR-EIF operators through executable code.

Verified FRP mechanisms may correspond to operators for:

- phase update;
- coupling;
- phase-order calculation;
- retained frequency update;
- ternary target generation;
- scheduling;
- neutral routing;
- pending destination handling;
- retained ternary commit.

These are implementation instances of broader formal contracts.

---

## 266. FRP Parameter Scope

Any FRP-specific operator parameters remain associated with the verified executable realization.

They do not become universal coefficients of the operators defined in this chapter.

---

## 267. FRP Phase-to-Target Boundary

A verified FRP phase-derived target operator belongs to the upstream target-generation layer.

Its output belongs to:

`T_target`.

It does not replace the ternary execution operator:

`E_T`.

---

## 268. FRP Pending-Route Boundary

A verified FRP pending-route mechanism provides an executable instance of neutral-mediated opposite-polarity routing.

Its stateful semantics correspond to:

- first-leg execution;
- pending destination retention;
- later second-leg eligibility.

---

## 269. Operator Provenance

An operator may carry provenance from:

`P_prov`.

Examples:

- classical differential operator — `PRIMARY_SOURCE`;
- TR-EIF-specific mapping — `AUTHOR_DEFINED`;
- calibrated threshold operator — `CALIBRATED`;
- executable measurement operator — `BENCHMARK`;
- controlled validator fixture — `TEST_FIXTURE`.

---

## 270. Operator Traceability

Every important operator should admit the chain:

`operator`

`→ domain`

`→ codomain`

`→ definition`

`→ provenance`

`→ implementation where applicable`

`→ observable or artifact`

`→ validation`.

---

## 271. Operator Validation

Operator validation must evaluate properties appropriate to the operator.

Examples include:

- domain validity;
- codomain validity;
- exact invariants;
- dimensional consistency;
- symmetry behavior;
- numerical tolerance;
- deterministic behavior;
- state-transition legality.

---

## 272. Operator Domain Invariant

For:

`A: X → Y`

every valid call requires:

`x ∈ X`.

Out-of-domain input must not silently enter valid semantic execution.

---

## 273. Operator Codomain Invariant

Every valid result must satisfy:

`A(x) ∈ Y`.

A result outside the declared codomain is invalid.

---

## 274. Operator Dimensional Invariant

Every operation on physical quantities must preserve its declared dimensional relation.

Numerical compatibility alone is insufficient.

---

## 275. Operator Circular-State Invariant

Every phase operator must preserve circular phase semantics.

Real-valued storage must not convert phase into unrestricted Euclidean state.

---

## 276. Operator Ternary Invariant

Every ternary execution operator must preserve:

`T = {-1, 0, 1}`

and canonical semantics:

`-1/0/1`.

---

## 277. Operator Neutral-State Invariant

No ternary operator may use:

`0`

as a generic marker for:

- invalid input;
- unavailable data;
- failure;
- missing state.

---

## 278. Operator Transition Invariant

No operator with commit authority may directly commit:

`-1 → 1`

or:

`1 → -1`.

---

## 279. Operator Target-State Invariant

No target-generation operator may silently mutate executed ternary state.

---

## 280. Operator Resonance-State Invariant

No resonance operator may identify:

`OUTSIDE`

with:

`-1`

`BOUNDARY`

with:

`0`

or:

`INSIDE`

with:

`1`

without an explicit separate mapping.

---

## 281. Operator Phase-Order Invariant

A phase-order operator and coherence operator remain distinct.

The canonical distinction is:

`R(t) ≠ C(t)`.

---

## 282. Operator Delay Invariant

A phase-lag operator does not access past state.

A delay operator does.

The distinction:

`delay ≠ phase lag`

is preserved by operator typing.

---

## 283. Operator Geometry Invariant

Translation, rotation, reflection, or permutation operators do not automatically transform ternary polarity.

---

## 284. Operator Force Invariant

A phase or ternary operator does not automatically produce mechanical force.

Force must arise through an explicitly typed force operator.

---

## 285. Operator Energy Invariant

A ternary state or resonance classification operator does not automatically produce physical energy.

Energy must arise through an energy functional or explicitly typed energy mapping.

---

## 286. Operator Structural Invariant

A ternary-transition operator is not a structural-transition operator.

---

## 287. Operator Physical-Phase Invariant

A structural classifier is not automatically a physical-phase classifier.

---

## 288. Operator Bifurcation Invariant

A threshold operator, resonance classifier, scheduler, or ternary execution operator is not a bifurcation-analysis operator.

---

## 289. Repository-Wide Operator Consistency

Operator semantics defined in documentation must remain consistent with:

- source implementation;
- schemas;
- tests;
- examples;
- benchmarks;
- validation artifacts.

A source function name does not authorize a conflicting mathematical meaning.

---

## 290. Operator Extension Rule

A new operator must define:

1. operator name;
2. domain;
3. codomain;
4. action;
5. dimensional behavior where applicable;
6. symmetry behavior where applicable;
7. state mutation semantics;
8. history or memory dependence where applicable;
9. provenance;
10. validation criteria.

---

## 291. Operator Specialization Rule

A specialization may fix:

- parameters;
- topology;
- numerical method;
- backend;
- scheduler;
- material system.

The specialized operator remains an instance of the general typed contract.

---

## 292. Operator Replacement Rule

Replacing one implementation operator with another is admissible only when the replacement satisfies the required domain, codomain, invariants, and interface semantics of the selected model.

---

## 293. Operator Equivalence

Two operators:

`A`

and:

`B`

are equivalent on domain:

`D`

under relation:

`≡`

when:

`A(x) ≡ B(x)`

for every:

`x ∈ D`.

The equivalence relation must be declared.

---

## 294. Exact Operator Equality

Exact operator equality on domain:

`D`

requires:

`A(x) = B(x)`

for every:

`x ∈ D`.

---

## 295. Numerical Operator Equivalence

Numerical operator equivalence may use:

`d(A(x), B(x)) ≤ epsilon`

for every tested:

`x`

under a declared validation scope.

This is distinct from exact equality.

---

## 296. Operator Determinism

For deterministic:

`A`

and complete input:

`x`

repeated evaluation must produce the same declared result under the selected comparison relation.

Hidden result-affecting state violates the deterministic operator contract.

---

## 297. Operator Closure for Integrated TR-EIF

A complete integrated execution operator may be represented abstractly as:

`F_TR-EIF: X_TR-EIF × U × P → X_TR-EIF`.

Its internal composition must preserve all component state-space boundaries and invariants.

---

## 298. Integrated Operator Decomposition

The integrated operator may be decomposed conceptually into:

`F_TR-EIF`

`= EIF commit`

`∘ TR-to-EIF feedback`

`∘ ternary execution`

`∘ resonance-to-target`

`∘ resonance classification`

`∘ resonance projection`

`∘ equivariant representation`

`∘ interatomic state evaluation`.

The actual mathematical composition requires compatible domains and explicit intermediate state.

---

## 299. Fundamental Operator Non-Equivalences

The following distinctions are mandatory:

`classification operator ≠ execution operator`

`target operator ≠ commit operator`

`request operator ≠ authorization operator`

`authorization operator ≠ commit operator`

`resonance operator ≠ synchronization operator`

`phase-order operator ≠ coherence operator`

`phase-lag operator ≠ delay operator`

`ternary operator ≠ energy operator`

`ternary operator ≠ force operator`

`phase-coupling operator ≠ mechanical-force operator`

`structural classifier ≠ physical-phase classifier`

`threshold operator ≠ bifurcation operator`

`exact flow ≠ numerical step operator`

`state projection ≠ state evolution`

`serialization ≠ physical transformation`

`quantization ≠ ternary classification`.

---

## 300. Final Operator Statement

The mathematical operator layer of TR-EIF provides typed transformations between the state spaces established in Chapters 01–04.

The canonical integration path is:

`X_EIF`

`→ equivariant operator`

`X_EQ`

`→ resonance projection`

`X_R`

`→ resonance classification`

`K_R`

`→ ternary target mapping`

`T_target`

`→ neutral-mediated execution`

`T_exec`

`→ feedback operator`

`X_EIF,req`.

The balanced ternary execution domain remains exactly:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`.

The state:

`0`

remains active.

Direct committed transitions:

`-1 → 1`

and:

`1 → -1`

remain forbidden.

Opposite-polarity execution remains:

`-1 → 0 → 1`

and:

`1 → 0 → -1`

through separate execution events.

The operator layer also preserves:

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

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

`mathematical model ≠ numerical realization`.

These operators provide the formal action layer required for the mathematical structures, mappings, invariants, lemmas, theorems, corollaries, and computational realizations developed in subsequent chapters and volumes.
