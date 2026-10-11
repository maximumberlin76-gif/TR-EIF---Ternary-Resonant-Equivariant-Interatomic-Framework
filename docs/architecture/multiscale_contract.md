# TR-EIF Multiscale Contract

## 1. Scope

This document defines the repository-level multiscale contract of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The contract specifies:

- scale separation;
- fine-to-coarse partitions;
- deterministic reductions;
- geometric coarse-graining;
- vector reductions and averages;
- coarse-to-fine prolongation;
- multilevel hierarchy composition;
- electronic-reference boundaries;
- interatomic and atomistic boundaries;
- mesoscale closure;
- continuum closure;
- transport-coefficient transfer;
- thermodynamic-consistency validation;
- uncertainty propagation;
- engineering-scale boundary mapping;
- cross-scale provenance;
- deterministic cross-scale execution;
- balanced-ternary boundaries;
- resonance boundaries;
- validation across scales.

This document defines architecture and interface semantics.

It does not introduce material-specific empirical coefficients.

It does not replace the mathematical definitions in the numbered documentation volumes.

---

## 2. Architectural Position

The TR-EIF modeling chain is:

`system class`

`→ boundaries`

`→ state spaces`

`→ variables`

`→ transformations`

`→ invariants`

`→ model`

`→ numerical realization`

`→ observable trace`

`→ validation`

Multiscale modeling operates inside this chain.

A scale mapping does not redefine the source state space.

A coarse representation does not erase the semantic type of the quantities from which it was constructed.

A validation result at one scale does not automatically establish validity at another scale.

---

## 3. Scale Hierarchy

A multiscale realization may contain ordered model levels such as:

`electronic reference`

`→ interatomic model`

`→ atomistic simulation`

`→ mesoscale closure`

`→ continuum closure`

`→ engineering-scale model`

The existence of this ordering does not imply that every adjacent mapping is available for every concrete model.

Each realized mapping must be explicitly defined.

A scale level is not a balanced-ternary state.

Therefore:

`scale index ≠ ternary state`

and:

`coarse index ≠ ternary state`

---

## 4. Multiscale State Separation

TR-EIF distinguishes:

- fine-scale state;
- coarse-scale state;
- partition state;
- geometric state;
- thermodynamic state;
- transport state;
- uncertainty state;
- engineering boundary state;
- resonance state;
- balanced-ternary execution state.

These are separate state types.

Numerical equality between values in different state spaces does not imply semantic identity.

---

## 5. Fine-to-Coarse Partition Contract

A fine-to-coarse partition is represented by:

`P: {0, ..., N_f - 1} → {0, ..., N_c - 1}`

where:

- `N_f` is the fine-entity count;
- `N_c` is the coarse-entity count;
- every fine entity maps to exactly one coarse entity;
- coarse indices form a contiguous range beginning at zero.

The executable reference type is:

`MultiscalePartition`

The mapping is structural.

It does not assign:

- physical phase;
- resonance class;
- ternary state;
- chemical bond;
- validation status.

---

## 6. Partition Membership

For a coarse entity `c`, the fine membership set is:

`M_c = {i | P(i) = c}`

Every valid coarse entity contains at least one fine entity under the current executable partition contract.

Partition membership is deterministic.

Canonical fine-index ordering is retained.

---

## 7. Scalar Reduction Contract

For an additive fine-scale scalar quantity `x_i`, partition-local summation is:

`X_c = Σ x_i for i in M_c`

The executable operator is:

`reduce_scalar_sum`

This operator is appropriate only when the modeled quantity is explicitly declared additive under the selected coarse-graining relation.

A generic scalar value is not automatically additive.

---

## 8. Mass Reduction

Mass uses partition-local summation:

`M_c = Σ m_i for i in M_c`

The executable operator is:

`reduce_masses`

Fine masses must be finite and positive.

Coarse masses must remain finite and positive.

The reduction conserves represented total mass:

`Σ M_c = Σ m_i`

This conservation statement applies to the represented partition mapping.

It does not establish conservation of unrelated quantities.

---

## 9. Geometric Coarse-Graining

The executable geometric coarse position uses a mass-weighted Cartesian centroid.

For one coarse entity:

`R_c = (Σ m_i r_i) / (Σ m_i)`

for fine entities assigned to that coarse entity.

The executable operator is:

`mass_weighted_centroids`

The operator acts on Cartesian positions.

It does not perform hidden periodic-boundary unwrapping.

Therefore:

`wrapped coordinates → no implicit unwrapping`

A periodic geometry requiring unwrapped positions must supply that representation explicitly before applying a Cartesian centroid operator.

---

## 10. Periodic Geometry Boundary

Periodic-boundary semantics remain separate from structural coarse-graining.

The current multiscale centroid operator must not be described as producing a physically correct periodic centroid when wrapped coordinates cross a periodic boundary unless explicit unwrapping has already been performed.

No hidden minimum-image reconstruction is performed by the multiscale layer.

---

## 11. Vector Reduction

Partition-local vector summation is distinct from vector averaging.

An additive vector reduction uses componentwise summation.

The executable operator is:

`reduce_vector_sum`

This operation does not automatically apply to every vector-valued physical quantity.

The modeled quantity must explicitly justify additive reduction.

---

## 12. Mass-Weighted Vector Average

A mass-weighted coarse vector may be represented as:

`V_c = (Σ m_i v_i) / (Σ m_i)`

for fine entities assigned to coarse entity `c`.

The executable operator is:

`mass_weighted_vector_average`

A mass-weighted vector average is not equivalent to a vector sum.

The selected operation must match the physical meaning of the represented variable.

---

## 13. Ternary Averaging Prohibition

Balanced-ternary states are not continuous scalars.

Therefore TR-EIF does not define generic arithmetic ternary averaging.

In particular:

`mean(-1, 1) = 0`

as ordinary arithmetic does not establish that the corresponding coarse ternary state is active neutral `0`.

Active neutral `0` has explicit execution semantics.

Therefore:

`arithmetic zero ≠ automatically active neutral state`

and:

`ternary coarse state ≠ arithmetic average of fine ternary states`

Any fine-to-coarse ternary mapping requires a separately defined operator with explicit semantics.

---

## 14. Active Neutral Boundary

The balanced ternary state space remains:

`T = {-1, 0, 1}`

State `0` is active neutral.

Its possible roles include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Multiscale reduction does not erase these semantics.

A coarse-graining operator must not reinterpret active neutral `0` as missing data, scalar zero, or averaged polarity.

---

## 15. Resonance Boundary

Resonance state remains a continuous state.

A resonance descriptor may be transferred, reduced, or reconstructed only through an explicitly declared mapping.

No generic multiscale operator identifies:

`resonance coordinate = ternary state`

or:

`phase order = coarse ternary polarity`

or:

`coherence = uniformity`

or:

`resonance classification = scale classification`

---

## 16. Prolongation Contract

Coarse-to-fine prolongation reconstructs a fine representation from a declared coarse quantity.

Current executable reference operators include:

- scalar broadcast prolongation;
- vector broadcast prolongation.

Broadcast prolongation assigns the selected coarse value to the fine members of the corresponding partition entity.

Broadcast is a declared reconstruction rule.

It is not an inverse of arbitrary fine-to-coarse reduction.

---

## 17. Reduction and Prolongation Are Not Generic Inverses

For a reduction operator `R` and prolongation operator `Q`, TR-EIF does not generally assume:

`Q(R(x)) = x`

Information may be lost under coarse-graining.

Exact reconstruction must be proven for the specific operator and admissible state class if claimed.

---

## 18. Partition Composition

Successive partitions may be composed when the output cardinality of one partition matches the input cardinality of the next.

The executable operator is:

`compose_partitions`

Composition produces a deterministic direct fine-to-coarse mapping.

It does not create new physical semantics.

---

## 19. Multiscale Hierarchy

A multilevel partition structure is represented by:

`MultiscaleHierarchy`

A corresponding multilevel coarse-state structure is represented by:

`MultiscaleStateHierarchy`

The hierarchy records ordered scale relationships.

Each adjacent scale transition must satisfy cardinality compatibility.

The hierarchy is structural.

It is not itself a thermodynamic model.

---

## 20. Coarse-Scale State

The executable reference coarse-scale state contains structural coarse information including:

- partition;
- coarse positions;
- coarse masses.

Construction is performed through:

`build_coarse_scale_state`

The current executable coarse state does not automatically include:

- resonance state;
- ternary state;
- transport coefficients;
- uncertainty state;
- constitutive law;
- thermodynamic closure.

Those quantities require separate declared mappings or closures.

---

## 21. Electronic-Reference Layer

Electronic-reference data are represented through:

`ElectronicReferenceRecord`

The record may bind an atomic configuration to externally supplied:

- total energy;
- forces;
- stress;
- source identifier;
- method identifier.

The multiscale layer does not perform an electronic-structure calculation.

It does not infer missing electronic observables.

An electronic-reference provider remains external unless a concrete implementation explicitly supplies one.

---

## 22. Electronic-to-Interatomic Boundary

An electronic-reference result and an interatomic model are separate model levels.

A mapping between them must specify:

- input configuration domain;
- target observable;
- source method;
- unit convention;
- provenance;
- approximation or fitting procedure;
- validation relation.

The existence of electronic-reference data does not automatically validate an interatomic model.

---

## 23. Interatomic Layer

The TR-EIP model family belongs inside TR-EIF:

`TR-EIP ⊂ TR-EIF`

The interatomic layer may consume:

- atomic geometry;
- interaction graph;
- E(3)-equivariant features;
- continuous resonance channels;
- retained balanced-ternary conditioning.

The interatomic layer produces declared physical observables through its model contract.

The interatomic model is not itself the multiscale hierarchy.

---

## 24. Atomistic Simulation Layer

Atomistic time evolution is represented by the TR-EIF molecular-dynamics layer.

The atomistic simulation layer may use interatomic energy and force models.

Molecular-dynamics time evolution and multiscale coarse-graining remain separate operators.

No hidden coarse-graining occurs inside a molecular-dynamics step.

No hidden resonance or ternary update occurs unless explicitly declared by the selected execution composition.

---

## 25. Mesoscale Closure

A mesoscale closure is represented by:

`MesoscaleClosureRecord`

and evaluated through:

`evaluate_mesoscale_closure`

A closure binds:

- an explicit coarse-scale state;
- closure identifier;
- source identifier;
- explicit closure variables;
- optional auxiliary variables.

No constitutive coefficient is inferred automatically.

No hidden history variable is introduced.

No empirical parameter is introduced without explicit input or provenance.

---

## 26. Continuum Closure

A continuum closure is represented by:

`ContinuumClosureRecord`

and evaluated through:

`evaluate_continuum_closure`

The continuum closure is bound to an explicit mesoscale closure.

Its variables remain explicit.

The contract does not automatically provide:

- constitutive law;
- continuum discretization;
- material coefficient;
- transport relation;
- boundary condition;
- uncertainty model.

---

## 27. Closure Chaining

A valid closure chain may have the form:

`coarse state`

`→ mesoscale closure`

`→ continuum closure`

Each arrow is an explicit provider evaluation.

A later closure record must remain bound to its declared upstream input.

Provider output for another upstream state is invalid under the executable contract.

---

## 28. Transport-Coefficient Transfer

A cross-scale transport coefficient is represented through:

`TransportCoefficient`

Cross-scale transfer uses:

`TransportTransferContext`

and:

`TransportCoefficientTransferRecord`

The context explicitly identifies:

- target scale;
- mapping;
- normalization;
- assumptions.

The transfer function does not infer:

- unit conversion;
- averaging rule;
- constitutive relation;
- empirical correction;
- state-domain conversion.

---

## 29. Transport Identity Preservation

A transport transfer retains coefficient identity.

The target coefficient must correspond to the declared source coefficient identity.

The target scale must equal the target scale declared by the transfer context.

Different units or state domains require explicit provider semantics.

They are not silently converted.

---

## 30. Thermodynamic Consistency

Cross-scale thermodynamic validation is represented through:

`ThermodynamicConsistencyRecord`

The evaluation context identifies:

- relation;
- model;
- assumptions;
- normalization.

Consistency status is Boolean validation evidence.

Therefore:

`thermodynamic validation status ≠ ternary state`

and:

`False ≠ ternary -1`

and:

`True ≠ ternary 1`

No thermodynamic validation status is encoded through active neutral `0`.

---

## 31. Thermodynamic Variable Boundary

Thermodynamic variables remain explicitly typed by:

- variable identity;
- value;
- unit;
- scale;
- state domain;
- source.

The multiscale contract does not infer:

- temperature from ternary state;
- pressure from resonance state;
- entropy from coherence;
- physical phase from oscillator phase.

---

## 32. Uncertainty Propagation

Uncertainty propagation is represented through:

`UncertaintyMeasure`

`UncertaintyPropagationContext`

and:

`UncertaintyPropagationRecord`

The propagation context explicitly declares:

- target scale;
- propagation rule;
- assumptions;
- correlation model;
- normalization.

The contract does not assume:

- Gaussian uncertainty;
- independence;
- covariance structure;
- linear error propagation;
- Monte Carlo sampling;
- confidence level.

---

## 33. Uncertainty Is Not Ternary State

An uncertainty magnitude or uncertainty classification is not a balanced-ternary state.

Therefore:

`uncertainty = 0 ≠ automatically active neutral`

and:

`unknown uncertainty ≠ ternary 0`

Missing uncertainty metadata must remain missing or explicitly unresolved.

It must not be encoded through active neutral state `0`.

---

## 34. Engineering-Scale Boundary Conditions

Engineering-scale boundaries are represented through:

`EngineeringBoundaryCondition`

`EngineeringBoundaryContext`

and:

`EngineeringBoundaryRecord`

The contract keeps explicit:

- engineering model identity;
- geometry identity;
- mapping identity;
- assumptions;
- boundary identity;
- variable identity;
- condition identity;
- values;
- units;
- provenance source.

---

## 35. Boundary-Type Non-Inference

The engineering boundary contract does not infer that a condition is:

- Dirichlet;
- Neumann;
- Robin;
- periodic;
- convective;
- radiative;
- mechanical;
- electrical.

The meaning of a boundary condition is supplied by the declared external model or provider.

---

## 36. Cross-Scale Determinism

For a deterministic cross-scale mapping:

`M: X_a × C → X_b`

identical:

- source state;
- mapping configuration;
- parameters;
- auxiliary variables;
- execution environment within the declared determinism domain

must produce the same declared target state.

Hidden result-affecting inputs violate the determinism contract.

---

## 37. Canonical Ordering

Where deterministic collections are required, TR-EIF uses canonical ordering.

Examples include:

- partition membership ordering;
- named closure-variable ordering;
- uncertainty-measure ordering;
- deterministic graph accumulation;
- deterministic serialization.

Changing insertion order must not silently change the declared mathematical result when canonical ordering is part of the contract.

---

## 38. Provenance Across Scales

Every source-backed cross-scale quantity must retain sufficient provenance to identify:

- source quantity;
- source scale;
- target scale;
- mapping;
- assumptions;
- normalization;
- unit transformation when applicable;
- derived or calibrated status;
- source identifier.

A quantity does not become `PRIMARY_SOURCE` merely because its upstream input was primary-source data.

A transformed quantity normally requires its own derived provenance classification.

---

## 39. Validation Across Scales

Cross-scale validation must identify:

- source observable;
- target observable;
- comparison relation;
- applicable units;
- state domain;
- model scale;
- uncertainty treatment;
- reference source;
- acceptance criterion when one exists.

Agreement at one scale does not prove agreement at every scale.

---

## 40. Structural Transition Boundary

A multiscale mapping is not automatically a structural transition.

A structural transition is not automatically a physical phase transition.

A physical phase transition is not a ternary transition.

Therefore:

`scale transition ≠ structural transition`

`structural transition ≠ physical phase transition`

`physical phase transition ≠ ternary transition`

---

## 41. Resonance and Multiscale Mapping

A resonance state may be associated with a scale only through an explicit scale-aware mapping.

The framework does not define generic resonance averaging.

A coarse resonance descriptor must not be produced by arbitrary arithmetic averaging unless that operation is explicitly defined and validated for the selected descriptor.

---

## 42. Ternary and Multiscale Mapping

Balanced-ternary execution state remains subject to the transition contract at every scale where ternary semantics are used.

Direct committed opposite-polarity transitions remain forbidden:

`-1 → 1`

`1 → -1`

Required routes remain:

`-1 → 0 → 1`

`1 → 0 → -1`

Each route leg remains a separate execution event.

A scale mapping does not waive the active-neutral transition semantics.

---

## 43. No Hidden FRP Architecture Transfer

FRP may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

The multiscale TR-EIF contract does not import:

- FRP repository structure;
- FRP RTL architecture;
- FRP scheduler modes;
- FRP-specific coefficients;
- FRP module naming.

Therefore:

`FRP ≠ TR-EIF`

and:

`FRP ≠ TR-EIP`

---

## 44. Material Specialization

A material specialization such as FLiBe may instantiate the multiscale interfaces.

Material-specific values require explicit provenance.

A generic multiscale contract must not invent:

- material density;
- viscosity;
- thermal conductivity;
- diffusion coefficient;
- coordination cutoff;
- thermodynamic coefficient;
- transport coefficient.

Material-specific evidence remains in the material-specialization and reference-data layers.

---

## 45. Executable Reference Boundary

The current executable multiscale layer provides reference implementations for:

- fine-to-coarse partitions;
- scalar reduction;
- mass reduction;
- Cartesian centroid construction;
- vector reduction;
- mass-weighted vector averaging;
- scalar and vector broadcast prolongation;
- partition composition;
- multiscale hierarchy construction;
- multiscale state hierarchy construction;
- electronic-reference records;
- mesoscale closure records;
- continuum closure records;
- transport-coefficient transfer;
- thermodynamic-consistency validation;
- uncertainty propagation;
- engineering boundary records.

This executable coverage does not imply a complete physical model for every scale.

---

## 46. Non-Claims

The multiscale layer does not by itself establish:

- first-principles accuracy;
- mesoscale physical validity;
- continuum constitutive validity;
- transport-property accuracy;
- engineering predictive accuracy;
- uncertainty calibration;
- thermodynamic completeness;
- physical phase-transition prediction.

Such claims require separate evidence and validation.

---

## 47. Core Multiscale Invariants

The multiscale architecture preserves the following invariants:

1. Fine-to-coarse membership is explicit.
2. Coarse indices are structural identifiers, not ternary states.
3. Reduction operators are quantity-specific.
4. Ternary states are not numerically averaged by default.
5. Active neutral `0` retains its execution semantics.
6. Resonance state is not implicitly averaged or converted to ternary state.
7. Periodic unwrapping is never hidden inside Cartesian coarse-graining.
8. Reduction and prolongation are not assumed to be inverses.
9. Electronic-reference data do not automatically validate an interatomic model.
10. Mesoscale closure is explicit.
11. Continuum closure is explicit.
12. Transport transfer requires declared mapping assumptions.
13. Thermodynamic consistency is validation evidence, not ternary state.
14. Uncertainty propagation requires an explicit correlation and propagation contract.
15. Engineering boundary conditions are not inferred from identifiers.
16. Provenance survives scale transfer.
17. Deterministic mappings require complete result-affecting state.
18. Validation at one scale does not imply validation at another scale.

---

## 48. Architectural Summary

The TR-EIF multiscale chain is an explicit composition of typed mappings.

It is not a single implicit reduction operator.

The architectural relation is:

`electronic reference`

`→ interatomic representation`

`→ atomistic simulation`

`→ structural coarse state`

`→ mesoscale closure`

`→ continuum closure`

`→ engineering boundary state`

with separately declared:

- transport transfer;
- thermodynamic validation;
- uncertainty propagation;
- resonance state;
- balanced-ternary execution state;
- provenance;
- validation evidence.

Each mapping retains its own domain, codomain, assumptions, and invariants.

No scale boundary is permitted to collapse continuous physical dynamics, resonance state, balanced-ternary execution, uncertainty, or validation status into one undifferentiated numerical state.
