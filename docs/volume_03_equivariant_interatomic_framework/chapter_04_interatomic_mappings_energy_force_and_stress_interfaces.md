# Interatomic Mappings, Energy, Force, and Stress Interfaces

## 1. Purpose

This document formalizes the interatomic mapping and physical-output interface layer of the Equivariant Interatomic Framework.

The chapter continues the established EIF chain:

`interatomic configuration`

`→ geometry`

`→ topology`

`→ local atomic environment`

`→ invariant / equivariant representation`

and defines the next typed layer:

`EIF representation`

`→ interatomic mapping`

`→ physical or model output`

The chapter establishes:

- general interatomic mappings;
- local and global output spaces;
- scalar, vector, and tensor output interfaces;
- potential-energy mappings;
- local-energy decomposition boundaries;
- force mappings;
- forces derived from differentiable scalar energy;
- conservative-force structure;
- permutation behavior of energies and forces;
- translation and rotation constraints;
- reflection behavior;
- periodic-cell dependencies;
- deformation and stress interfaces;
- virial-interface boundaries;
- dimensional requirements;
- differentiability requirements;
- locality and long-range boundaries;
- model-output and physical-observable separation;
- learned and analytical mapping boundaries;
- exact and numerical consistency validation;
- energy-force consistency;
- transformation consistency;
- provenance and empirical-validation requirements;
- the boundary between EIF physical outputs and later Ternary Resonant integration.

No universal energy functional, force law, stress law, or material parameter is introduced.

## 2. Dependency

This chapter depends on:

- Volume 01, Mathematical Foundations;
- Volume 02, Ternary Resonance Theory;
- Volume 03, Chapter 01, Equivariant Interatomic Foundations;
- Volume 03, Chapter 02, Interatomic State Spaces, Geometry, and Local Environments;
- Volume 03, Chapter 03, Symmetry Actions, Invariant and Equivariant Representations.

It inherits without redefinition:

- admissible interatomic configuration spaces;
- local atomic environments;
- interaction topology;
- invariant and equivariant representation spaces;
- permutation actions;
- translation actions;
- `SO(3)`, `O(3)`, `SE(3)`, and `E(3)` distinctions;
- representation actions;
- information-loss semantics;
- locality semantics;
- exact and numerical equivariance boundaries;
- provenance classes;
- the closed Ternary Resonant invariants.

## 3. Scientific Status Classes

### 3.1 CLASSICAL

The following are classical mathematical or physical modeling structures:

- scalar potential-energy functions;
- gradients;
- conservative force fields;
- coordinate transformation of gradients;
- tensor transformation;
- deformation gradients;
- derivatives with respect to geometric variables;
- Hessians;
- translational and rotational invariance;
- permutation covariance of indexed outputs.

### 3.2 EIF FORMAL / AUTHOR-DEFINED

The following are author-defined EIF architecture:

- the typed physical-output interface hierarchy;
- interatomic mapping contracts;
- output provenance requirements;
- energy-force consistency contracts;
- local/global decomposition requirements;
- stress-interface requirements;
- output-validation hierarchy;
- EIF-to-TR physical-interface boundary.

### 3.3 DERIVED

Results following mathematically from declared invariant energy mappings and differentiability assumptions are classified as:

`DERIVED`

### 3.4 OPERATIONAL / EXECUTABLE REFERENCE

Existing machine-learning interatomic potentials provide implementation precedents for:

- atom-centered energy mappings;
- global energy aggregation;
- force derivation from total energy;
- symmetry-aware interatomic prediction.

They do not define EIF universally.

### 3.5 EMPIRICAL / CALIBRATED

A numerical energy, force, stress, material property, cutoff, or fitted parameter becomes empirically supported only through independently defined data and validation.

### 3.6 UNVERIFIED

A model output lacking sufficient physical interpretation or empirical support remains unverified even when the mapping is mathematically well typed and symmetry-consistent.

## 4. Position in the EIF Architecture

The current EIF chain is:

`q ∈ Q`

`→ geometry`

`→ topology`

`→ local environments`

`→ h_EIF ∈ Y_EIF`

This chapter introduces mappings from the EIF state into declared output spaces.

A generic output mapping is:

`M_out: Y_EIF × Λ_out → Y_out`

where:

- `Y_EIF` is a declared EIF representation space;
- `Λ_out` is the output-parameter space;
- `Y_out` is the declared output space.

The output mapping must not acquire physical semantics merely from its numerical type.

## 5. Interatomic Mapping

An interatomic mapping is a typed relation whose source contains explicitly represented interatomic state or a representation derived from that state.

A generic direct mapping may be written:

`M_Q: Q_adm × Λ_M → Y_M`

A representation-mediated mapping may be written:

`M_H: Y_EIF × Λ_M → Y_M`

The two mappings are not automatically equivalent.

## 6. Output Space

Every output must have an explicit codomain.

Possible output spaces include:

- `ℝ` for scalar quantities;
- `ℝ^3` for vector quantities;
- `(ℝ^3)^N` for site-indexed vectors;
- `ℝ^(3×3)` for second-order tensors;
- finite categorical spaces;
- structured product spaces.

Numerical storage shape does not establish physical meaning.

## 7. Model Output Is Not Physical Observable Automatically

Let:

`ŷ ∈ Y_out`

be a model output.

The existence of `ŷ` does not establish that it represents a physical observable.

Physical interpretation requires:

- a declared quantity;
- units;
- transformation behavior;
- model relation;
- provenance;
- validation evidence.

Therefore:

`model output ≠ physical observable automatically`

## 8. Scalar Output

A scalar output belongs to:

`Y_scalar ⊆ ℝ`

Its transformation semantics must still be declared.

A numerical scalar may be:

- invariant;
- transformation-dependent through external state;
- dimensionless;
- dimensional.

Therefore:

`scalar ≠ invariant automatically`

## 9. Vector Output

A vector output belongs to a declared vector space.

For an ordinary polar vector in three dimensions:

`v ∈ ℝ^3`

and under:

`R ∈ O(3)`

the standard transformation is:

`v' = R v`

when the complete source state is transformed consistently.

## 10. Site-Indexed Vector Output

For `N` sites, define:

`Y_vec,N = (ℝ^3)^N`

An output is:

`V_out = (v_1, ..., v_N)`

Under atomic permutation, the vectors must follow the corresponding site reindexing.

## 11. Tensor Output

A tensor output must declare its tensor space and transformation law.

For a standard second-order Cartesian tensor:

`A ∈ ℝ^(3×3)`

a rigid orthogonal transformation may act as:

`A' = R A R^T`

when that is the declared tensor convention.

Array dimension alone does not determine the transformation law.

## 12. Physical Units

Every physical output must specify units or dimensional structure.

A representation channel may be dimensionless.

A physical output such as energy, force, or stress is dimensional.

Therefore:

`dimensionless latent channel ≠ dimensional physical output`

without an explicit dimensional mapping.

## 13. Potential-Energy Space

Let:

`Y_E = ℝ`

represent the mathematical scalar codomain of a potential-energy mapping.

Physical energy interpretation additionally requires an energy unit.

## 14. Potential-Energy Mapping

A potential-energy specialization defines:

`E: Q_E × Λ_E → ℝ`

where:

- `Q_E ⊆ Q_adm` is the admissible energy domain;
- `Λ_E` is the energy-model parameter space.

For fixed parameters `λ_E ∈ Λ_E`, write:

`E_λ(q) = E(q, λ_E)`

## 15. Energy Is Not Defined Universally by EIF

EIF does not define one universal:

`E(q)`

Different specializations may use different energy models.

Therefore:

`EIF ≠ one universal interatomic potential`

## 16. Energy and Representation Are Distinct

If:

`Φ_EIF: Q_E → Y_EIF`

and:

`R_E: Y_EIF → ℝ`

then an energy model may be composed as:

`E = R_E ∘ Φ_EIF`

The representation is not the energy.

Therefore:

`Y_EIF ≠ ℝ energy semantics`

even when the final readout is scalar.

## 17. Energy Invariance Under Translation

For a model intended to represent an isolated potential depending only on internal geometry, global translation invariance may require:

`E(T_a q) = E(q)`

for every admissible translation `T_a`.

This condition depends on the complete physical boundary.

It need not hold when an external position-dependent field is part of the modeled state but is not transformed with the configuration.

## 18. Energy Invariance Under Rotation

For a rigid-motion invariant scalar potential:

`E(R · q) = E(q)`

for every admissible:

`R ∈ SO(3)`

when all source-state components are transformed consistently.

## 19. Energy Behavior Under Reflection

If full `O(3)` or `E(3)` invariance is claimed:

`E(R · q) = E(q)`

must also hold for admissible improper transformations.

A model sensitive to chirality or an external parity-breaking state requires a more specific transformation contract.

## 20. Energy Permutation Invariance

For consistent computational reindexing:

`π ∈ S_N`

a global energy intended to describe the same physical configuration must satisfy:

`E(π · q) = E(q)`

when atomic identities move consistently with their indexed states.

## 21. Permutation Invariance Is Not Species Exchange

The relation:

`E(π · q) = E(q)`

does not mean species identities can be exchanged independently of their atomic records.

Therefore:

`permutation invariance ≠ arbitrary species substitution invariance`

## 22. Local Energy Mapping

A model may introduce site-associated scalar contributions:

`ε_i`

through a local mapping such as:

`ε_i = E_local(e_i, λ_E)`

where:

`e_i ∈ X_env`

is the local environment.

## 23. Total Energy Aggregation

A local-energy model may define:

`E_total = Σ_(i=1)^N ε_i`

This is one admissible construction.

EIF does not require every energy model to use this decomposition.

## 24. Local Energy Is Model-Dependent

The quantity:

`ε_i`

is a model decomposition component.

It must not automatically be interpreted as a uniquely measurable physical energy belonging to atom `i`.

Therefore:

`local atomic energy contribution ≠ uniquely defined physical atomic energy`

in general.

## 25. Decomposition Non-Uniqueness

Different local decompositions may produce the same total energy.

If:

`Σ_i ε_i = Σ_i ε_i'`

then equality of total energy does not imply:

`ε_i = ε_i'`

for every site.

The decomposition semantics belong to the model.

## 26. Extensive Energy Boundary

A sum of local contributions has extensive scaling properties under suitable locality and independence assumptions.

This is a model construction.

It does not establish universal thermodynamic extensivity for every system or interaction class.

## 27. Long-Range Energy Boundary

A strictly local finite-cutoff energy mapping may be insufficient for systems whose target energy depends materially on long-range interactions.

Such systems require additional explicitly modeled information.

Possible structures include:

- long-range channels;
- global terms;
- electrostatic models;
- hierarchical mappings;
- reciprocal-space components;
- another declared mechanism.

## 28. Energy Offset

Adding a configuration-independent constant:

`c_E`

to a potential:

`E'(q) = E(q) + c_E`

does not change coordinate-derived forces.

Therefore absolute energy offset and force field are distinct aspects of an energy model.

## 29. Species-Dependent Energy Reference

A model may include species-dependent reference contributions.

Such references must be explicitly defined and retain provenance.

They are not universal atomic energies.

## 30. Differentiability Domain

To derive forces through coordinate gradients, the energy mapping must be differentiable with respect to the relevant coordinates on the declared domain.

Let:

`Q_diff ⊆ Q_E`

be a differentiability domain.

Force derivation is valid only where the required derivative exists.

## 31. Force Space

For fixed `N`, define:

`Y_F = (ℝ^3)^N`

A force state is:

`F = (f_1, ..., f_N)`

with:

`f_i ∈ ℝ^3`

## 32. Energy-Derived Force

For differentiable energy:

`E: Q_diff → ℝ`

define the force on site `i` as:

`f_i = -grad_(x_i) E`

The complete force mapping is:

`F_E: Q_diff → Y_F`

## 33. Gradient Variable Must Be Explicit

The derivative:

`grad_(x_i) E`

is taken with respect to the position of site `i`.

It is not a derivative with respect to:

- species identity;
- computational index;
- ternary state;
- resonance coordinate;
- topology label.

Different derivatives require different source variables.

## 34. Force Is Not Representation

The vector:

`f_i`

may be produced from an equivariant representation.

It is not identical to that representation.

Therefore:

`equivariant feature ≠ force`

## 35. Force Is Not Ternary State

A force belongs to a dimensional vector space.

A ternary state belongs to:

`T = {-1, 0, 1}`

Therefore:

`force ≠ ternary state`

## 36. Conservative Force Structure

If forces are defined everywhere on the relevant domain through:

`F = -grad E`

for one differentiable scalar potential, the resulting model has conservative potential-force structure on that domain.

This is stronger than merely predicting vector forces directly.

## 37. Direct Force Mapping

A model may instead define:

`F_direct: Q_F × Λ_F → Y_F`

without deriving it from a scalar energy.

Such a mapping can be equivariant.

It is not automatically conservative.

## 38. Equivariant Force Is Not Conservative Force

Therefore:

`force equivariance ≠ energy conservation`

and:

`equivariant vector field ≠ gradient field`

The distinction must be preserved.

## 39. Energy-Force Consistency

If a model exposes both energy:

`E_model`

and force:

`F_model`

and claims the force is derived from the energy, it must satisfy:

`f_i,model = -grad_(x_i) E_model`

within the declared mathematical or numerical validation conditions.

## 40. Independent Energy and Force Heads

If energy and force are predicted through independent mappings, consistency is not guaranteed automatically.

A model must not claim gradient consistency unless it is imposed or validated.

## 41. Force Transformation Under Rotation

Assume:

- `E` is rotationally invariant;
- `E` is differentiable;
- `q' = R · q`;
- `R ∈ O(3)`.

Then the corresponding coordinate-derived polar force transforms as:

`f_i(q') = R f_i(q)`

This relation is derived from invariance of the scalar energy and the coordinate transformation.

## 42. Force Transformation Under Reflection

For a polar force vector and:

`R ∈ O(3)`

the same transformation form applies:

`f_i' = R f_i`

including improper orthogonal transformations, provided the source state and scalar-energy symmetry satisfy the corresponding `O(3)` contract.

## 43. Force Transformation Under Permutation

For:

`π ∈ S_N`

the force collection must reindex consistently:

`F(π · q) = π · F(q)`

when the underlying physical state is unchanged by computational reindexing.

Thus force is permutation equivariant rather than globally permutation invariant.

## 44. Force and Translation

A force collection derived from a globally translation-invariant energy satisfies additional derived constraints under appropriate differentiability assumptions.

Translation invariance is not represented by adding the same translation vector to the force.

Forces are unaffected by a common coordinate translation of an isolated translationally invariant system.

## 45. Net Force from Translation-Invariant Potential

Let:

`E(x_1 + a, ..., x_N + a) = E(x_1, ..., x_N)`

for every admissible infinitesimal translation `a`.

Differentiating with respect to `a` gives:

`Σ_i grad_(x_i) E = 0`

and therefore:

`Σ_i f_i = 0`

for the energy-derived internal force field.

This is a derived model identity under the stated assumptions.

## 46. Net-Force Identity Is Scope-Dependent

The identity:

`Σ_i f_i = 0`

does not apply automatically when the modeled system includes an external field, constraint, fixed boundary, or another source of external force not transformed together with the system.

The system boundary determines applicability.

## 47. Rotational Invariance and Torque Relation

For an isolated differentiable scalar potential invariant under infinitesimal rigid rotations, the energy-derived internal forces satisfy the corresponding zero-total-torque relation about the chosen origin:

`Σ_i x_i × f_i = 0`

under the assumptions required by that rigid-rotation symmetry.

## 48. Torque Relation Is Not Universal Without Boundary Conditions

External fields, imposed constraints, periodic conventions, or incomplete modeled state can modify the applicable torque balance.

Therefore:

`rotational invariance-derived torque identity ≠ universal external-force law`

## 49. Pairwise Force Decomposition Is Not Required

A many-body energy model can define valid atomic forces without assigning a unique pairwise force:

`f_ij`

to every pair.

Therefore:

`interatomic force model ≠ pairwise force decomposition`

## 50. Newton-Pair Shortcut Is Forbidden

For a general many-body model, one must not infer a unique pairwise relation:

`f_ij = -f_ji`

unless a pairwise decomposition has been independently defined.

Global translation invariance can constrain total internal force without supplying a unique pair decomposition.

## 51. Hessian

For a twice-differentiable energy, define the coordinate Hessian:

`H_E = grad_x grad_x E`

where `x` denotes the complete coordinate vector.

The Hessian belongs to a higher-order linear map space.

## 52. Force Jacobian

Because:

`F = -grad_x E`

the force Jacobian satisfies:

`J_F = -H_E`

where both derivatives exist.

This relation belongs to the differentiable energy-derived model.

## 53. Hessian Symmetry

For sufficiently smooth scalar energy under ordinary Cartesian coordinates:

`H_E^T = H_E`

This is a mathematical consequence of equality of mixed partial derivatives under the required regularity assumptions.

## 54. Hessian Is Not Stress

The energy Hessian is a coordinate second derivative.

Stress is a different physical tensor interface.

Therefore:

`energy Hessian ≠ stress tensor`

## 55. Force Constant Boundary

A Hessian or its negative may be interpreted as a force-constant matrix only under an explicitly defined physical and coordinate convention.

The name must not be assigned from array shape alone.

## 56. Periodic Energy Domain

For a periodic system, an energy may depend on both atomic state and cell state:

`E_per: Q_per × X_cell × Λ_E → ℝ`

where:

`X_cell`

contains the declared periodic-cell variables.

## 57. Cell Matrix

For a three-dimensional periodic cell, let:

`H ∈ ℝ^(3×3)`

with:

`det(H) ≠ 0`

under the chosen cell convention.

The cell is part of the energy source state when energy depends on it.

## 58. Cell Dependence Is Not Coordinate Dependence Only

A periodic energy can change when the cell changes even when fractional atomic coordinates remain fixed.

Therefore:

`cell derivative ≠ atomic-position derivative`

## 59. Deformation Map

Let:

`F_def ∈ GL(3)`

denote an admissible deformation gradient acting on a reference cell or coordinates according to the selected continuum convention.

The symbol `F_def` is not the atomic-force collection `F`.

Distinct notation must be maintained in executable implementations if ambiguity would arise.

## 60. Rigid Rotation and Deformation Remain Distinct

A proper rigid rotation is a special orthogonal transformation.

A general deformation may include:

- stretch;
- shear;
- volume change.

Therefore:

`deformation ≠ rigid rotation`

## 61. Strain Interface

A stress-producing specialization may introduce a strain variable:

`ε ∈ X_strain`

with an explicitly defined strain measure.

Different strain measures have different mathematical meanings.

EIF does not select one universal strain tensor.

## 62. Stress Space

A stress output requires a declared tensor space:

`Y_sigma`

A common three-dimensional representation uses:

`σ ∈ ℝ^(3×3)`

but the physical convention must specify:

- stress measure;
- reference configuration;
- sign convention;
- volume convention;
- units.

## 63. Stress Mapping

A generic stress mapping may be written:

`Σ: Q_sigma × X_cell × Λ_sigma → Y_sigma`

This mapping is independent unless it is explicitly derived from energy or another physical relation.

## 64. Energy-Derived Stress Interface

A specialization may derive a stress-like quantity from differentiation of energy with respect to a declared strain or cell-deformation variable.

The exact formula depends on:

- strain definition;
- cell convention;
- reference/current volume choice;
- stress measure.

No one formula is imposed universally here.

## 65. Stress Requires Convention

A matrix of derivatives with respect to cell entries is not automatically the physical Cauchy stress.

A valid stress interface must state the conversion from the chosen derivative variables to the declared stress measure.

## 66. Stress Transformation

For an ordinary second-order spatial stress tensor under rigid orthogonal coordinate transformation:

`σ' = R σ R^T`

when that is the declared stress convention.

This transformation law does not define the numerical stress value.

## 67. Stress Symmetry

Many classical continuum stress models use a symmetric Cauchy stress tensor under specific angular-momentum assumptions.

EIF does not impose stress symmetry universally on every generalized interatomic tensor output.

The model must state the intended physical tensor.

## 68. Virial Boundary

A virial quantity may be defined in atomistic models through positions, forces, momenta, or pair/many-body decompositions depending on convention.

Therefore:

`virial ≠ stress automatically`

A virial-to-stress relation requires the declared normalization, sign, volume, and physical convention.

## 69. Virial Mapping

A model that exposes a virial quantity must define its codomain and calculation separately.

The word:

`virial`

must not be attached to an arbitrary second-order tensor output.

## 70. Pressure Boundary

Pressure is a scalar physical quantity requiring an independently declared relation.

It must not be identified automatically with:

- trace of an arbitrary latent tensor;
- FRP processor quantity `P`;
- topology density;
- local neighbor count;
- resonance classification.

## 71. EIF Pressure and FRP P Remain Distinct

The processor-specific `P` quantity from the FRP executable specialization belongs to the TR/processor telemetry domain.

A physical pressure in an interatomic model belongs to a dimensional physical-output space.

Therefore:

`physical pressure ≠ FRP P`

unless an independent mapping is explicitly defined and calibrated.

## 72. Local Stress Boundary

A model may introduce site-resolved or local stress-like contributions.

Such decompositions are model-dependent and may not be unique.

Therefore:

`local stress contribution ≠ uniquely defined measurable local stress automatically`

## 73. Total and Local Output Separation

Global physical outputs and local decomposition channels must remain distinct.

A global energy can be physically meaningful even when the chosen local energy decomposition is not uniquely identifiable.

## 74. Output Aggregation

Let local output channels be:

`y_i ∈ Y_local`

A global aggregation is a mapping:

`A_out: Y_local^N → Y_global`

The aggregation rule must be explicitly declared.

## 75. Aggregation and Physical Scaling

Sum, mean, maximum, and other aggregation rules have different cardinality and physical scaling behavior.

They are not interchangeable.

## 76. Invariant Global Scalar Readout

A global scalar energy readout must be invariant under all transformations included in the physical symmetry contract.

This may be achieved through:

- invariant local scalar contributions;
- invariant contraction of equivariant features;
- another symmetry-compatible construction.

## 77. Equivariant Vector Readout

A vector output must retain a nontrivial output action.

For force:

`f_i' = R f_i`

under the standard polar-vector action.

An invariant final readout cannot produce orientation-dependent force information without another equivariant source.

## 78. Tensor Readout

A tensor-valued physical output requires the corresponding representation type throughout the downstream mapping or a valid tensor construction from lower-order channels.

## 79. Local Mapping Scope

A local output mapping:

`M_i: X_env,i → Y_i`

depends only on the declared local environment.

Its physical validity is therefore conditional on the locality assumption being sufficient for the target quantity.

## 80. Global Mapping Scope

A global mapping may depend on the full configuration or global representation.

Global dependence may be necessary for:

- long-range interactions;
- collective constraints;
- total-charge state;
- global fields;
- other nonlocal effects.

## 81. Hybrid Local-Global Mapping

A physical model may combine:

`local contribution`

and:

`global correction`

through a separately defined composition.

The two channels must preserve compatible units and transformation semantics.

## 82. Long-Range Electrostatic Boundary

Electrostatic interactions can require long-range information.

A finite local neighbor environment does not universally determine the electrostatic contribution.

Therefore:

`finite local equivariant representation ≠ universal electrostatic model`

## 83. Charge State

If atomic or distributed charges are represented, define their state space explicitly.

A charge may be:

- prescribed;
- predicted;
- dynamically updated;
- constrained globally.

Each case has different model semantics.

## 84. Charge Is Not Atomic Species

Atomic identity and charge state remain separate variables.

Therefore:

`species ≠ charge state`

even when one constrains possible charge values.

## 85. Charge Is Not Ternary State

A physical or model charge variable is not the balanced ternary state.

Therefore:

`charge ≠ -1/0/1 state`

even if a numerical charge value happens to be `-1`, `0`, or `1` in some unit convention.

## 86. External Field Interface

If a physical output depends on an external field, the field belongs to the source state.

Its transformation law must be included when symmetry claims are evaluated.

## 87. Energy with External Field

An energy may be written:

`E(q, ξ_ext)`

where:

`ξ_ext`

is declared external state.

A symmetry transformation of `q` alone need not preserve `E` if the external state is held fixed.

## 88. Complete-State Symmetry

A physical symmetry claim must act on the complete modeled state.

Transforming only one subsystem can describe a different physical configuration rather than a symmetry-equivalent representation.

## 89. Constraints

Geometric or dynamical constraints must be represented explicitly if they affect physical outputs.

Constraint forces must not be silently mixed with unconstrained potential forces.

## 90. Fixed Sites

A site fixed by a boundary condition may still have a mathematically defined energy gradient.

Whether that gradient is interpreted as force, reaction force, or excluded dynamical update depends on the boundary convention.

## 91. Physical Force and Execution Update Are Distinct

A computed force does not itself specify a numerical integrator or position update.

Therefore:

`force law ≠ time integration scheme`

Dynamics require a separately defined evolution model.

## 92. Energy Mapping and Dynamics Are Distinct

A potential-energy surface determines a conservative force field when differentiated appropriately.

It does not determine:

- masses;
- thermostat;
- time step;
- integrator;
- stochastic forcing;
- damping;
- boundary update.

Therefore:

`interatomic potential ≠ complete molecular dynamics model`

## 93. Mass State

If Newtonian dynamics are later defined, mass is a separately typed physical parameter or state associated with atomic identity or isotope state.

Mass is not implied by coordinate geometry alone.

## 94. Force-to-Acceleration Boundary

A later dynamical model may define:

`a_i = f_i / m_i`

for nonzero mass `m_i`.

This is outside the static interatomic mapping itself.

## 95. Temperature Boundary

Temperature is not a direct coordinate of the minimal EIF configuration.

A simulation temperature, thermostat variable, or thermodynamic temperature requires an independently defined state or ensemble relation.

Therefore:

`interatomic energy ≠ temperature`

## 96. Model Energy and Total Physical Energy

A potential energy model generally does not include kinetic energy unless explicitly defined.

Therefore:

`potential energy ≠ total mechanical energy`

## 97. Learned Mapping

A learned interatomic mapping has model parameters selected from data.

The transformation and physical-output contract remains mathematical and does not depend solely on the training procedure.

## 98. Analytical Mapping

An analytical interatomic mapping may satisfy the same EIF interface contract without any learned parameters.

Therefore:

`EIF physical-output mapping ≠ machine learning requirement`

## 99. Hybrid Mapping

A hybrid model may combine analytical and learned components.

Every component must preserve:

- units;
- transformation behavior;
- output semantics;
- provenance.

## 100. Parameter Space

Let:

`Λ_M`

denote model parameters affecting an interatomic mapping.

Different parameter classes must remain distinguishable.

Examples include:

- analytically fixed constants;
- learned coefficients;
- calibrated parameters;
- numerical cutoffs;
- regularization parameters;
- test fixtures.

## 101. Parameter Provenance

Every claim-relevant parameter must use the inherited provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

## 102. Learned Parameter Is Not Physical Constant

A trained weight is an implementation parameter.

It does not become a physical constant because the model fits physical data.

Therefore:

`learned parameter ≠ universal physical constant`

## 103. Cutoff Is Not Physical Interaction Boundary Automatically

A computational cutoff may determine which local interactions are represented directly.

It does not establish that the physical interaction vanishes exactly at that distance.

Therefore:

`model cutoff ≠ universal physical interaction boundary`

## 104. Energy Cutoff Smoothness

If forces are obtained through energy differentiation, non-smooth cutoff behavior can produce non-smooth or discontinuous forces.

A differentiable-force model must therefore validate the differentiability of the complete energy mapping over its operational domain.

## 105. Topology Discontinuity Boundary

A hard topology change can affect differentiability even when individual edge functions are smooth.

The complete model must be evaluated, not only one edge kernel.

## 106. Continuous Weighting

A smooth cutoff or weighting function can reduce certain boundary discontinuities.

It does not by itself guarantee global differentiability if another part of the topology or mapping remains discontinuous.

## 107. Differentiability and Equivariance Are Independent

A mapping can be:

- equivariant but non-differentiable;
- differentiable but not equivariant;
- both;
- neither.

Therefore:

`equivariance ≠ differentiability`

## 108. Continuity and Physical Accuracy Are Independent

A continuous smooth model may still be physically inaccurate.

Therefore:

`smoothness ≠ physical validation`

## 109. Conservative Structure and Accuracy Are Independent

A force model can be exactly conservative but quantitatively incorrect.

Therefore:

`conservative force structure ≠ predictive accuracy`

## 110. Energy Conservation and Physical Completeness Are Distinct

A conservative potential can omit relevant dissipative, electronic, magnetic, reactive, or long-range effects.

Therefore:

`energy-conserving potential ≠ complete physical model`

## 111. Physical Interpretation Boundary

Physical meaning is attached to the explicitly defined output mapping.

It is not inherited automatically from:

- input geometry;
- representation degree;
- latent feature name;
- graph edge;
- numerical sign.

## 112. Scalar Sign Boundary

The sign of an invariant scalar does not automatically mean:

- attraction;
- repulsion;
- negative energy;
- ternary `-1`;
- resonance outside.

Interpretation requires the declared mapping.

## 113. Vector Direction Boundary

The direction of an equivariant vector does not automatically mean force direction.

It may encode another geometric feature.

Therefore:

`vector orientation ≠ force direction automatically`

## 114. Energy Sign Boundary

A potential-energy zero is convention-dependent in many models.

The sign of energy alone does not universally determine:

- stability;
- bonding;
- resonance;
- phase;
- ternary state.

## 115. Force Sign Boundary

Individual Cartesian force-component signs depend on coordinate basis.

They are not ternary polarity.

Therefore:

`negative force component ≠ ternary -1`

and:

`positive force component ≠ ternary 1`

## 116. Stress Sign Boundary

Stress sign conventions can differ between communities and implementations.

The convention must be declared.

A negative tensor component must not be assigned semantic meaning without the selected stress convention.

## 117. Energy and Chemical Bond

A low-energy configuration may be associated with stable structure under a specific physical model.

This does not define a chemical bond relation automatically.

Therefore:

`energy minimum ≠ chemical bond definition`

## 118. Force and Chemical Bond

A force between atoms or sites does not by itself define a chemical bond.

Therefore:

`force interaction ≠ chemical bond`

## 119. Energy and Structural State

An energy value alone may be insufficient to identify structure because distinct configurations can share the same energy.

Therefore:

`energy value ≠ structural state`

## 120. Energy and Physical Phase

A potential-energy value alone does not determine a thermodynamic phase.

Therefore:

`energy ≠ physical phase`

## 121. Force and Resonance

An interatomic force is not automatically a TR resonance state or resonance coordinate.

Therefore:

`force ≠ resonance`

## 122. Energy and Resonance

Potential energy is also not automatically a resonance coordinate.

Therefore:

`energy ≠ resonance state`

## 123. Stress and Resonance

Stress does not automatically define resonance classification.

Therefore:

`stress ≠ resonance classification`

## 124. Physical Output and Ternary Target

No physical output maps automatically into:

`T = {-1, 0, 1}`

A later integration mapping must define any such relation explicitly.

## 125. Energy-to-Ternary Shortcut Is Forbidden

The following rule is not part of EIF:

`low energy → -1`

`intermediate energy → 0`

`high energy → 1`

or any equivalent thresholding scheme.

## 126. Force-to-Ternary Shortcut Is Forbidden

No force magnitude, sign, or direction is automatically a ternary state.

The mapping requires explicit definition if introduced later.

## 127. Stress-to-Ternary Shortcut Is Forbidden

No stress component or invariant determines ternary polarity by implication.

## 128. Energy-to-Resonance Shortcut Is Forbidden

An energy value or energy minimum does not automatically imply resonance.

The TR resonance-coordinate mapping remains independently defined.

## 129. Force-to-Resonance Shortcut Is Forbidden

A force equilibrium condition:

`f_i = 0`

is not a resonance classification.

Therefore:

`mechanical equilibrium ≠ resonance`

## 130. Stationary Point

A configuration satisfying:

`grad_x E = 0`

is a stationary point of the energy under the relevant coordinate variables.

It may be:

- local minimum;
- local maximum;
- saddle point;
- degenerate stationary point.

Additional Hessian information is required for local classification.

## 131. Energy Minimum

A local energy minimum requires appropriate second-order or other sufficient conditions in addition to first-order stationarity.

A zero force alone does not prove a local minimum.

## 132. Hessian Local Classification

For an unconstrained non-degenerate stationary point:

- positive-definite Hessian indicates a strict local minimum;
- negative-definite Hessian indicates a strict local maximum;
- indefinite Hessian indicates a saddle.

Zero modes or constraints require additional analysis.

## 133. Rigid-Motion Zero Modes

For isolated invariant systems, global translations and rotations can create symmetry-related directions that complicate naive Hessian definiteness tests.

The appropriate reduced or constrained space must be defined for structural stability analysis.

## 134. Mechanical Stability Is Not TR Stability

A local minimum of an interatomic potential is a mechanical/model stability concept.

It is not automatically the TR coherence or resonance-stability quantity.

Therefore:

`mechanical local minimum ≠ TR stable resonance regime`

## 135. Local Energy Decomposition and Force

Even when:

`E_total = Σ_i ε_i`

the force on site `k` generally receives derivatives from every local term that depends on `x_k`:

`f_k = -Σ_i grad_(x_k) ε_i`

It is not generally:

`f_k = -grad_(x_k) ε_k`

only.

## 136. Environment Overlap

Because local environments overlap, one site's coordinate can affect multiple local energy contributions.

This is a normal many-body dependency structure.

## 137. Site Energy and Site Force Are Not One-to-One

Therefore:

`atomic energy contribution of site i ≠ force contribution on site i`

without an independently defined decomposition.

## 138. Edge Energy Boundary

A model may assign pair or edge energy contributions.

Such a decomposition must define whether edges are:

- directed;
- undirected;
- double counted;
- symmetrized.

No universal edge-energy convention is assumed.

## 139. Many-Body Mapping

EIF allows mappings whose output depends jointly on multiple atoms or environments.

Therefore:

`interatomic mapping ≠ pairwise potential`

## 140. Pair Potential Specialization

A pairwise specialization may define:

`E_pair = Σ_(i<j) φ(z_i, z_j, d_ij)`

for a declared pair function `φ`.

This is a restricted model class rather than the general EIF architecture.

## 141. Pair Potential Rotation Invariance

If `φ` depends on distance only, its pair-energy contribution is invariant under orthogonal transformations of the pair geometry.

This does not establish physical adequacy of the pair approximation.

## 142. Pair Potential Force Direction

For differentiable distance-only pair potential, the corresponding pair-force direction is constrained by the pair separation direction.

This result belongs to that specific pairwise model.

It must not be generalized to arbitrary many-body force decompositions.

## 143. Angular Potential

A many-body energy may depend on angles or higher-order geometric invariants.

Such terms can remain rotationally invariant while producing forces not decomposable into one unique distance-only pair law.

## 144. Equivariant Internal Features and Invariant Energy

An EIF model may use non-scalar equivariant internal features and produce an invariant scalar energy.

This separation is an established symmetry-aware architecture pattern.

The internal feature transformation type need not match the final scalar output type.

## 145. Invariant Energy and Equivariant Gradient

An invariant differentiable scalar energy can generate equivariant coordinate gradients.

Thus an invariant output can produce a nontrivially transforming derivative.

This does not mean the scalar itself becomes equivariant as a vector.

## 146. Automatic Differentiation Boundary

A computational implementation may use automatic differentiation to evaluate:

`-grad_x E`

Automatic differentiation is a numerical/software mechanism for obtaining derivatives of the implemented mapping.

It does not alter the mathematical definition of force.

## 147. Symbolic and Automatic Differentiation

Symbolic, analytical, automatic, and finite-difference derivative methods are different computational realization methods.

A force-consistency claim concerns the derivative of the same energy mapping, not which derivative engine is used.

## 148. Finite-Difference Force Check

A numerical validation may compare predicted force component with an energy finite difference.

For coordinate component `x_k,α` and small nonzero step `h`, a centered difference may use:

`dE_dx ≈ [E(x + h e_kα) - E(x - h e_kα)] / (2h)`

and compare:

`f_k,α ≈ -dE_dx`

The approximation error depends on `h`, smoothness, and numerical precision.

## 149. Finite Difference Is Not Exact Derivative

Therefore:

`finite-difference agreement ≠ exact symbolic identity`

unless an additional proof establishes the exact relation.

## 150. Numerical Force Tolerance

A force comparison requires a tolerance with compatible force units.

A dimensionless tolerance cannot be applied directly to dimensional force without a normalization rule.

## 151. Energy Error

A predicted energy may be compared with reference energy through an explicitly defined metric.

Possible metrics include:

- absolute error;
- squared error;
- per-atom normalized error.

These metrics answer different questions.

## 152. Force Error

A force error metric must specify whether it operates on:

- vector norm;
- Cartesian components;
- per-site average;
- global maximum;
- another declared measure.

## 153. Stress Error

Stress validation must specify:

- tensor components;
- tensor norm or invariant;
- units;
- sign convention;
- symmetry convention;
- reference stress measure.

## 154. Reference Data

A reference value may originate from:

- experiment;
- electronic-structure calculation;
- another accepted simulation;
- analytic solution;
- benchmark fixture.

Its provenance determines what kind of validation claim it can support.

## 155. Computational Reference Is Not Experiment

A force or energy generated by DFT is computational reference data.

It is not experimental measurement.

Therefore provenance must distinguish the two.

## 156. Training Data and Validation Data

Data used to fit parameters and data used for independent evaluation have different evidential roles.

A model must not describe training-set fit as independent validation.

## 157. Extrapolation Boundary

Good accuracy within one sampled configuration distribution does not establish accuracy over the full admissible configuration space.

Therefore:

`test-set PASS ≠ universal interatomic validity`

## 158. Transformation Validation and Physical Validation Are Distinct

A model may pass exact symmetry tests while failing energy or force accuracy tests.

It may also fit selected data while violating a required symmetry.

Both dimensions require independent validation.

## 159. Energy-Force Consistency Validation

A model claiming energy-derived forces must validate:

`F_model ≈ -grad E_model`

to the appropriate exact or numerical standard.

Reference-force accuracy alone does not prove internal energy-force consistency.

## 160. Energy Symmetry Validation

A rigid-motion invariant energy model must validate energy invariance under all claimed transformation classes.

For full `E(3)` claims this includes:

- translations;
- proper rotations;
- improper transformations.

## 161. Force Symmetry Validation

Force validation under transformed input must compare against the transformed force state:

`F(g · q)`

versus:

`ρ_F(g)F(q)`

rather than checking numerical equality of Cartesian components under a nontrivial rotation.

## 162. Stress Symmetry Validation

A stress output must be compared using its declared tensor action.

Elementwise equality after rotation is generally not the correct equivariance criterion.

## 163. Permutation Validation

For local forces:

`F(π · q) = π · F(q)`

must hold under the declared permutation convention.

For global scalar energy:

`E(π · q) = E(q)`

must hold.

These are different validation relations.

## 164. Periodic Consistency Validation

Periodic models must test that physically equivalent periodic representations produce compatible outputs under the declared cell and image convention.

Wrapped coordinate differences alone must not create artificial physical discontinuities.

## 165. Cell Transformation Validation

If cell rotation belongs to the symmetry test, both:

- cell state;
- atomic coordinates;

must be transformed consistently.

## 166. Deformation Validation

A deformation test is not a symmetry test when deformation changes physical geometry.

Energy and stress may legitimately change under deformation.

Therefore:

`deformation response ≠ symmetry violation`

## 167. Physical-Output Trace

An executable implementation may record:

- configuration identity;
- energy;
- forces;
- stress;
- cell state;
- model parameters;
- units;
- provenance;
- validation metadata.

Such a trace is an output-evidence layer.

It is not the mathematical model itself.

## 168. Missing Physical Output

If a model does not define stress, absence of stress is not equivalent to zero stress.

Therefore:

`missing stress ≠ σ = 0`

## 169. Missing Energy

Likewise:

`missing energy ≠ E = 0`

and:

`missing force ≠ f = 0`

Missing-data semantics must remain outside valid physical values.

## 170. Zero Force

A valid value:

`f_i = 0`

means the defined force vector is zero.

It is not:

- missing data;
- active neutral ternary state;
- resonance boundary;
- absence of atom.

## 171. Zero Energy

A valid energy value:

`E = 0`

is interpreted only relative to the model's energy reference.

It is not the active ternary state.

## 172. Zero Stress

A valid zero stress tensor is a physical/model tensor state under the selected convention.

It is not missing data or ternary neutral.

## 173. Output Status Must Be Separate

A computational output may need a validity status.

The status must use a separate field or state space.

It must not overload physical zero values.

## 174. Energy and Force Provenance

Every output artifact claiming physical meaning must retain enough information to identify:

- model version;
- parameter state;
- units;
- source configuration;
- boundary conditions;
- output definition;
- numerical precision;
- calibration or training provenance.

## 175. Stress Provenance

Stress additionally requires:

- stress convention;
- cell convention;
- volume convention;
- strain/deformation definition;
- sign convention.

## 176. Model Revision Boundary

Changing:

- architecture;
- parameters;
- cutoff;
- basis;
- training data;
- energy reference;
- stress convention;

can change output semantics or values.

Artifacts from different revisions must not be treated as identical evidence automatically.

## 177. Interatomic Mapping Conformance

An interatomic mapping conforms to EIF when:

- source space is declared;
- codomain is declared;
- units are declared where physical;
- transformation behavior is declared;
- locality is declared;
- information loss is declared;
- parameter provenance is declared;
- numerical realization is separated from formal semantics.

## 178. Energy Interface Contract

A potential-energy interface must define:

1. admissible configuration domain;
2. parameter space;
3. scalar codomain;
4. physical energy unit;
5. permutation behavior;
6. translation behavior;
7. rotation behavior;
8. reflection behavior where claimed;
9. boundary-condition dependence;
10. locality or nonlocality;
11. differentiability domain;
12. provenance;
13. validation criteria.

## 179. Force Interface Contract

A force interface must define:

1. source state;
2. site-indexed vector codomain;
3. force units;
4. permutation action;
5. geometric transformation action;
6. derivation from energy or independent mapping;
7. differentiability assumptions where energy-derived;
8. boundary-condition semantics;
9. validation criteria;
10. provenance.

## 180. Stress Interface Contract

A stress interface must define:

1. source state;
2. tensor codomain;
3. stress measure;
4. stress units;
5. tensor transformation action;
6. sign convention;
7. cell convention;
8. volume convention;
9. strain or deformation variable if derivative-based;
10. derivation or direct mapping;
11. validation criteria;
12. provenance.

## 181. Conservative-Model Contract

A model claiming conservative potential forces must define one scalar potential:

`E`

such that:

`F = -grad_x E`

over the declared domain.

If the relation holds only approximately, the approximation boundary and tolerance must be stated.

## 182. Direct-Force Contract

A direct-force model must define:

- vector output action;
- permutation action;
- physical units;
- training/calibration provenance;
- whether conservativity is imposed, tested, or not claimed.

Direct force prediction must not imply hidden energy existence.

## 183. Physical-Meaning Contract

Before any EIF output is called a physical quantity, the model must define:

1. physical meaning;
2. units;
3. source variables;
4. transformation law;
5. parameter provenance;
6. calibration or reference relation;
7. validation scope.

## 184. Core Physical-Interface Invariants

The following invariants are mandatory.

1. EIF representation remains distinct from physical output.

2. Scalar output remains distinct from energy until energy semantics are defined.

3. Vector output remains distinct from force until force semantics are defined.

4. Tensor output remains distinct from stress until stress semantics are defined.

5. Energy is a scalar mapping with declared units.

6. Force is a site-indexed vector mapping with declared units.

7. Stress requires a declared tensor convention.

8. Global energy remains permutation invariant under computational reindexing when the physical state is unchanged.

9. Site-indexed force remains permutation equivariant.

10. Rigid-motion invariant energy remains distinct from the equivariant force derived from it.

11. Energy-derived force requires differentiability.

12. Direct force prediction does not imply a conservative potential.

13. Conservative structure does not imply predictive accuracy.

14. Equivariance does not imply conservativity.

15. Equivariance does not imply physical validity.

16. Local energy decomposition is not assumed unique.

17. Pairwise force decomposition is not assumed for many-body models.

18. Graph edge remains distinct from physical interaction law.

19. Model cutoff remains distinct from universal physical interaction boundary.

20. Local mapping remains distinct from globally sufficient physical model.

21. Long-range interactions require an explicit information path.

22. Cell dependence remains distinct from atomic-coordinate dependence.

23. Deformation remains distinct from rigid symmetry transformation.

24. Virial remains distinct from stress until a relation is defined.

25. Pressure remains distinct from arbitrary scalar model channels.

26. Physical pressure remains distinct from FRP processor `P`.

27. Zero physical output remains distinct from missing data.

28. Energy zero remains distinct from ternary neutral.

29. Force-component sign remains distinct from ternary polarity.

30. Stress-component sign remains distinct from ternary polarity.

31. Energy remains distinct from resonance state.

32. Force remains distinct from resonance state.

33. Stress remains distinct from resonance classification.

34. Mechanical equilibrium remains distinct from resonance.

35. Energy minimum remains distinct from chemical-bond definition.

36. Energy value remains distinct from physical phase.

37. Physical output remains distinct from ternary target.

38. Energy-to-ternary shortcut remains forbidden.

39. Force-to-ternary shortcut remains forbidden.

40. Stress-to-ternary shortcut remains forbidden.

41. Energy-to-resonance shortcut remains forbidden.

42. Force-to-resonance shortcut remains forbidden.

43. Training fit remains distinct from independent validation.

44. Computational reference remains distinct from experimental measurement.

45. Symmetry validation remains distinct from physical-output validation.

## 185. Formal Non-Equivalences

The following non-equivalences are mandatory:

`EIF representation ≠ physical observable`

`scalar output ≠ energy automatically`

`vector output ≠ force automatically`

`tensor output ≠ stress automatically`

`latent scalar ≠ energy`

`equivariant vector ≠ force`

`higher-order channel ≠ stress`

`local atomic energy ≠ uniquely measurable atomic energy`

`total energy equality ≠ local decomposition equality`

`force equivariance ≠ conservativity`

`equivariant force field ≠ gradient force field automatically`

`energy model ≠ complete dynamics`

`interatomic potential ≠ molecular dynamics integrator`

`potential energy ≠ total mechanical energy`

`pairwise potential ≠ general interatomic mapping`

`many-body force ≠ unique pair-force decomposition`

`graph edge ≠ force interaction`

`graph edge ≠ energy contribution automatically`

`model cutoff ≠ physical interaction boundary`

`equivariance ≠ differentiability`

`differentiability ≠ physical accuracy`

`smoothness ≠ physical validation`

`conservative force structure ≠ predictive accuracy`

`virial ≠ stress automatically`

`stress derivative array ≠ Cauchy stress automatically`

`pressure ≠ arbitrary scalar output`

`physical pressure ≠ FRP P`

`missing energy ≠ zero energy`

`missing force ≠ zero force`

`missing stress ≠ zero stress`

`energy zero ≠ ternary 0`

`force sign ≠ ternary polarity`

`stress sign ≠ ternary polarity`

`energy ≠ resonance`

`force ≠ resonance`

`stress ≠ resonance classification`

`mechanical equilibrium ≠ resonance`

`energy minimum ≠ chemical bond`

`energy value ≠ structural state`

`energy value ≠ physical phase`

`physical output ≠ ternary state`

`training accuracy ≠ independent validation`

`DFT reference ≠ experimental measurement`

`symmetry PASS ≠ physical validation`

## 186. Primary Computational Reference: Behler–Parrinello

Behler and Parrinello introduced a high-dimensional neural-network representation of potential-energy surfaces using atom-centered local environments.

Their construction provides an established precedent for obtaining total energy from atom-centered contributions while preserving the required permutation and geometric behavior of the potential-energy surface.

The work does not define EIF.

Provenance:

`PRIMARY_SOURCE`

## 187. Primary Computational Reference: SchNet

Schütt et al. introduced SchNet, a continuous-filter convolutional architecture for atomistic quantum-interaction modeling.

The work provides a computational precedent for joint modeling of total energy and interatomic forces from continuous atomic geometry.

SchNet does not define the equivariant representation architecture of EIF and does not define TR-EIF.

Provenance:

`PRIMARY_SOURCE`

## 188. Primary Computational Reference: NequIP

Batzner et al. introduced NequIP as an E(3)-equivariant interatomic-potential architecture.

The model produces an invariant total potential energy and derives forces as negative gradients of that predicted energy with respect to atomic positions.

This provides a direct primary reference for the distinction:

`equivariant internal representation`

`→ invariant scalar potential energy`

`→ equivariant coordinate-derived forces`

The architecture remains one executable specialization rather than the definition of EIF.

Provenance:

`PRIMARY_SOURCE`

## 189. Literature Boundary

The primary references support established computational precedent for:

- atom-centered energy representation;
- invariant total-energy prediction;
- energy-derived atomic forces;
- joint energy-force atomistic modeling;
- E(3)-equivariant internal features with invariant energy readout.

They do not establish:

- one universal energy functional;
- one universal local energy decomposition;
- one universal force law;
- one universal stress law;
- universal locality;
- universal interatomic accuracy;
- TR resonance semantics;
- balanced ternary semantics;
- automatic EIF-to-TR physical mappings.

## 190. Primary Sources

1. Behler, J., and Parrinello, M. "Generalized Neural-Network Representation of High-Dimensional Potential-Energy Surfaces." Physical Review Letters 98, 146401, 2007. DOI: `10.1103/PhysRevLett.98.146401`

2. Schütt, K. T., Kindermans, P.-J., Sauceda, H. E., Chmiela, S., Tkatchenko, A., and Müller, K.-R. "SchNet: A Continuous-Filter Convolutional Neural Network for Modeling Quantum Interactions." Advances in Neural Information Processing Systems 30, 2017.

3. Batzner, S., Musaelian, A., Sun, L., Geiger, M., Mailoa, J. P., Kornbluth, M., Molinari, N., Smidt, T. E., and Kozinsky, B. "E(3)-Equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials." Nature Communications 13, 2453, 2022. DOI: `10.1038/s41467-022-29939-5`

These sources establish relevant classical computational precedent.

EIF-specific interface contracts, state separation, provenance requirements, validation hierarchy, TR-EIF boundaries, and conformance requirements remain author-defined framework structure.

## 191. Formal Physical-Output Chain

The EIF physical-output chain is:

`interatomic configuration`

`→ geometry`

`→ topology`

`→ local environment`

`→ invariant / equivariant representation`

`→ typed interatomic mapping`

`→ physical or model output`

For a conservative energy-derived specialization:

`EIF representation`

`→ invariant scalar energy`

`→ coordinate gradient`

`→ equivariant atomic force`

For a stress-producing specialization:

`configuration + cell / deformation state`

`→ declared energy or stress mapping`

`→ typed stress tensor`

Every arrow requires independently defined source and target semantics.

## 192. Energy-Force Dependency Chain

A gradient-consistent conservative model follows:

`q`

`→ E(q)`

`→ grad_x E(q)`

`→ F(q) = -grad_x E(q)`

The force field is downstream of the energy mapping.

A direct-force architecture follows a different chain:

`q`

`→ F_direct(q)`

and no scalar potential is implied.

## 193. Physical Validation Chain

A physical-output claim must support:

`output definition`

`→ units`

`→ transformation contract`

`→ model calculation`

`→ reference evidence`

`→ uncertainty / tolerance`

`→ validation result`

A symmetry proof alone does not complete this chain.

## 194. EIF-to-TR Boundary

The physical outputs defined by an EIF specialization may include:

- energy;
- forces;
- stress;
- other typed quantities.

None belongs automatically to:

`X_R`

`R_C`

or:

`T = {-1, 0, 1}`

The future integration layer must define any mapping from EIF physical or representation state into the TR source space.

## 195. Future EIF-to-TR Mapping

A later integration model may define a typed relation such as:

`M_E→TR: Y_EIF,int → X_TR,in`

where:

`Y_EIF,int`

is a deliberately selected EIF integration-output space.

The source may contain:

- representation channels;
- physical outputs;
- geometric state;
- multiscale descriptors;
- another explicitly defined subset.

No such selection is automatic.

## 196. Physical-Unit Boundary Across Integration

If dimensional EIF quantities enter the TR layer, the cross-layer mapping must define how their dimensions are transformed, normalized, combined, or preserved.

A dimensional force or energy cannot be inserted directly into a dimensionless resonance coordinate without a dimensionally valid mapping.

## 197. Transformation Boundary Across Integration

If the source EIF channel transforms nontrivially, the integration map must define the corresponding action on its TR target.

An equivariant force vector cannot be silently collapsed into one scalar resonance coordinate without declaring the reduction and its information loss.

## 198. Feedback Boundary

If a TR state later modifies an EIF energy, force, or representation mapping, the feedback must define:

- source TR state;
- target EIF object;
- units;
- transformation behavior;
- locality;
- update order;
- physical interpretation;
- provenance.

A ternary state is not itself an energy correction or force vector.

## 199. Balanced Ternary Boundary

The TR kernel remains exactly:

`T = {-1, 0, 1}`

with canonical notation:

`-1/0/1`

and active neutral:

`0`

Nothing in the physical-output layer modifies this definition.

## 200. No Numeric-Type Collapse

The values:

`-1`

`0`

and:

`1`

may occur numerically in:

- energies under a chosen reference;
- force components;
- tensor entries;
- parity labels;
- normalized descriptors;
- ternary state.

These objects remain mathematically distinct because their domains and units differ.

## 201. Conformance Requirements

An EIF physical-output specialization conforms to this chapter when:

- every physical output has a typed codomain;
- physical units are declared;
- representation and physical output remain distinct;
- energy symmetry is explicitly defined;
- force transformation behavior is explicitly defined;
- energy-derived forces use the derivative of the same declared energy;
- direct-force models do not claim conservativity without evidence;
- local energy decomposition is not treated as universally unique;
- stress convention is explicit;
- virial and stress remain distinct unless related explicitly;
- long-range dependencies have an explicit information path;
- exact and numerical validation remain distinct;
- physical reference provenance is explicit;
- no physical output is converted to TR state without an explicit mapping.

## 202. Final Statement

The EIF physical-output layer extends the established architecture:

`interatomic state`

`→ geometry`

`→ topology`

`→ local environment`

`→ invariant / equivariant representation`

into:

`→ typed interatomic mapping`

`→ physical or model output`

The core scalar physical interface is a separately defined potential-energy mapping:

`E: Q_E × Λ_E → ℝ`

When differentiability and the physical model require energy-derived forces:

`f_i = -grad_(x_i) E`

The scalar energy can remain invariant under the declared rigid transformations while its gradient transforms as a site-indexed equivariant vector field.

This relation does not mean:

`equivariance = force`

or:

`invariant scalar = energy`

The physical semantics arise only from the declared output mapping.

Stress requires an additional tensor interface with independently defined:

- deformation or strain variable;
- cell convention;
- stress measure;
- units;
- sign convention;
- transformation behavior.

Accordingly:

`virial ≠ stress automatically`

`tensor output ≠ stress automatically`

and:

`force equivariance ≠ conservative force structure`

remain mandatory distinctions.

No energy, force, stress, or mechanical-equilibrium quantity is identified automatically with:

- resonance;
- resonance classification;
- oscillator phase;
- balanced ternary state.

The balanced ternary kernel remains independently defined as:

`-1/0/1`

with active:

`0`

The resulting EIF chain is therefore:

`interatomic state`

`→ geometric and topological state`

`→ local environment`

`→ symmetry-aware representation`

`→ typed interatomic mapping`

`→ energy / force / stress interface where independently defined`

This provides the physical-output boundary required before multiscale EIF mappings, dynamic interatomic evolution, and explicit EIF-to-TR integration can be formalized.
