
# Uncertainty Transfer

## 1. Scope and System Class

This chapter specifies uncertainty representation and transfer between electronic-reference, interatomic, atomistic, mesoscale, continuum, and engineering levels of TR-EIF. The associated system class is an open nonlinear dissipative dynamical system with continuous physical states, three-dimensional geometry, resonance evolution, and separately scheduled balanced-ternary execution.

The multiscale uncertainty chain is:

`source quantity and uncertainty representation → scale mapping and correlation context → propagation provider → target uncertainty record → numerical qualification and provenance`.

The executable contract is defined by `UncertaintyMeasure`, `UncertaintyPropagationContext`, `UncertaintyPropagationRecord`, and `evaluate_uncertainty_propagation` in `src/tr_eif/multiscale/uncertainty_propagation.py`.

## 2. Quantity, Domain, and Uncertainty Representation

For a source quantity `x` in a declared state domain `X_l`, denote its uncertainty representation by `U_l(x)`. A transfer to target scale `m` is an explicitly selected mapping:

`(y, U_m(y)) = M_(l→m)(x, U_l(x); C_(l→m))`.

The context `C_(l→m)` identifies the physical state domain, numerical method, source and target scales, uncertainty representation, correlation treatment, normalization, and provenance. The representation may be a standard uncertainty, variance, interval, ensemble distribution, covariance structure, or another explicitly defined measure.

A single numerical uncertainty magnitude is meaningful together with its quantity identity, unit, representation, physical state, scale, and source. The state variable itself and its uncertainty are stored as distinct quantities.

## 3. Executable Uncertainty Measure

`UncertaintyMeasure` is an immutable dataclass with the following fields:

| Field | Meaning |
| --- | --- |
| `quantity_id` | Identifier of the physical or numerical quantity |
| `value` | Finite nonnegative numerical magnitude |
| `unit` | Identifier of the uncertainty unit |
| `representation_id` | Identifier of the uncertainty representation |
| `scale_id` | Scale associated with the measure |
| `state_domain_id` | Domain of the represented quantity |
| `source_id` | Source or provenance identifier |

Identifier fields are nonempty strings normalized by removal of surrounding whitespace. The value accepts finite real numbers, excluding Boolean values, and is stored as `float`. Zero is an admissible explicitly supplied magnitude.

`UncertaintyMeasures` is an immutable tuple of `UncertaintyMeasure` instances. The collection contract requires at least one measure, unique identity keys, and canonical key ordering.

## 4. Canonical Measure Identity

For a measure `u`, its executable identity key is:

`key(u) = (scale_id, quantity_id, representation_id, source_id)`.

`UncertaintyPropagationRecord` requires the source and target collections to be sorted by this key, without repeated keys inside either collection. The key provides deterministic ordering and identity for the exported transfer record.

The `state_domain_id`, `unit`, and numerical `value` remain explicit fields of each measure. Consequently, changes in physical state or units remain visible even when the canonical identity fields are unchanged. A transfer method associates its canonical collection with the complete domain and unit metadata.

## 5. Propagation Context

`UncertaintyPropagationContext` stores five normalized nonempty identifiers:

- `target_scale_id`: destination scale of the propagated measures;
- `propagation_id`: selected numerical or mathematical propagation method;
- `assumptions_id`: assumptions and applicability conditions;
- `correlation_id`: correlation or dependence specification;
- `normalization_id`: normalization and representation convention.

A method registry or calculation manifest associates each identifier with its mathematical definition and parameter values. The context therefore accompanies the source collection during propagation and remains attached to the target collection.

## 6. Propagation Record and Evaluator Binding

`UncertaintyPropagationRecord` contains `source_measures`, `target_measures`, and `context`. Its constructor validates canonical measure collections, the context type, and the equality:

`target_measure.scale_id = context.target_scale_id`

for every target entry.

The public evaluator boundary is:

`evaluate_uncertainty_propagation(source_measures, context, evaluator)`.

The supplied `evaluator` receives the complete source tuple and context and returns an `UncertaintyPropagationRecord`. The boundary validates the source collection and input types, invokes the provider, and checks the returned record's source measures and context against the supplied inputs.

The provider defines the propagation calculation, including the treatment of covariance, nonlinear response, numerical sampling, representation conversion, and units. The returned record carries its selected method through `context`.

## 7. Source Categories and Their Covariance Structure

A source collection can contain uncertainty contributions from measured observables, electronic-reference calculations, fitted interatomic parameters, geometric reconstruction, numerical integration, boundary inputs, and multiscale constitutive maps. Each contribution has its own quantity, unit, scale, method, and source identifier.

A joint model specifies dependence among these contributions. If `x = (x_1, ..., x_n)` is a vector of uncertain source quantities, define its covariance matrix for finite second moments:

`C_x[i,j] = Cov(x_i, x_j)`.

The diagonal elements satisfy `C_x[i,i] = u(x_i)^2` when `u(x_i)` denotes standard uncertainty. Covariance units equal the product of the corresponding quantity units. The matrix is symmetric and positive semidefinite for a valid covariance representation.

## 8. Linear Propagation

For a declared affine mapping:

`y = A x + b`,

the covariance transformation is:

`C_y = A C_x A^T`.

For a scalar target `y = sum_i a_i x_i + b`, its variance is:

`u(y)^2 = sum_i sum_j a_i a_j C_x[i,j]`.

For independent source variables, the off-diagonal covariance terms vanish, giving:

`u(y)^2 = sum_i a_i^2 u(x_i)^2`.

The selected correlation model is identified by `context.correlation_id`; the coefficient matrix, units, and input covariance data belong to the propagation provider's method context.

## 9. Differentiable Nonlinear Propagation

For a differentiable mapping `y = f(x)` near a declared expansion state `x_0`, define its Jacobian:

`J[i,j] = partial f_i / partial x_j at x_0`.

A first-order covariance approximation is:

`C_y ≈ J C_x J^T`.

The evaluation record identifies `x_0`, the derivative method, the domain of the approximation, the covariance input, and the numerical precision. For curvature-sensitive mappings, additional terms, higher-order expansions, or numerical propagation procedures are defined by the selected method.

The propagated uncertainty is associated with the chosen target observable and physical state, rather than with a categorical model or execution status.

## 10. Numerical and Distribution-Based Propagation

For a nonlinear provider `f` and an explicitly defined joint input distribution `p_X`, an ensemble method evaluates samples `x^(k)` and their images:

`y^(k) = f(x^(k))`.

For `K >= 2` equally weighted sampled outputs, one sample covariance estimator is:

`C_y = (1/(K - 1)) sum_(k=1)^K (y^(k) - y_bar)(y^(k) - y_bar)^T`.

The numerical record identifies the input distribution, correlations, sample count, pseudorandom generator and seed where applicable, weighting, convergence checks, and the estimator used.

An interval propagation method instead carries the defined source intervals through an enclosure or bound operator with its own arithmetic and geometric rules. The selected representation is recorded through `representation_id` and the propagation method through `propagation_id`.

## 11. Additive Mass and Scalar Reduction

Let `I_c` be the fine-entity membership of coarse group `c`. For an additive fine quantity `x_i`, define:

`X_c = sum_(i in I_c) x_i`.

For a covariance representation over the fine variables:

`Var(X_c) = sum_(i in I_c) sum_(j in I_c) Cov(x_i, x_j)`.

For positive fine masses, the existing `reduce_masses` operator constructs `M_c = sum_(i in I_c) m_i`. An uncertainty provider can use the same membership partition and the joint mass covariance to propagate mass uncertainty into coarse masses.

If the mapping uses fixed known fine masses, their role in the uncertainty context is recorded explicitly. If masses themselves are uncertain variables, their joint covariance enters the transfer calculation.

## 12. Three-Dimensional Centroid Uncertainty

For a coarse group with total mass `M_c > 0`, define the Cartesian mass-weighted centroid:

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

With fixed masses, introduce weights `w_i = m_i / M_c`. For a three-dimensional position covariance block `C_(r_i,r_j)`, the centroid covariance is:

`C_Rc = sum_(i in I_c) sum_(j in I_c) w_i w_j C_(r_i,r_j)`.

For uncertain masses, the corresponding first derivatives are:

`partial R_c / partial r_i = w_i I_3`.

`partial R_c / partial m_i = (r_i - R_c) / M_c`.

The full Jacobian therefore contains both coordinate and mass contributions and their cross-covariances. The coordinate reference frame, cell geometry, periodic unwrapping convention, partition, and sampling instant accompany the coarse-state uncertainty record.

## 13. Velocity and Momentum Transfer

For a fixed coarse membership and positive total mass:

`P_c = sum_(i in I_c) m_i v_i`.

`V_c = P_c / M_c`.

For fixed masses, coarse-velocity covariance follows the weighted-vector form:

`C_Vc = sum_(i in I_c) sum_(j in I_c) w_i w_j C_(v_i,v_j)`.

A provider handling uncertain masses augments this mapping with the mass derivatives and joint mass–velocity covariance. Internal velocity fluctuations and epistemic or measurement uncertainty are represented through their corresponding declared statistical models.

The deterministic coarse velocity is computed by `mass_weighted_vector_average`; the uncertainty transfer is evaluated through its separately selected provider.

## 14. E(3) Covariance Transfer

For an orthogonal transformation `Q in O(3)` and translation `b in R^3`, a Cartesian position vector transforms as:

`r' = Q r + b`.

For a covariance matrix of a three-dimensional polar vector under a deterministic common transformation:

`C_r' = Q C_r Q^T`.

The centroid covariance follows the same transformation when the partition and scalar weights are transported consistently. Scalar uncertainty measures associated with invariant quantities retain their values under the corresponding symmetry assumptions.

For tensorial uncertainty representations, the transformation is defined by the tensor's representation and index structure. The propagation context records the spatial frame and representation convention used for the source and target.

## 15. Hierarchical Propagation and Cross-Scale Correlation

For consecutive scale transformations `y = f(x)` and `z = g(y)`, the composed deterministic mapping is:

`z = g(f(x))`.

Where differentiable, its Jacobian is:

`J_(z,x) = J_(z,y) J_(y,x)`.

The first-order covariance transfer is:

`C_z ≈ J_(z,x) C_x J_(z,x)^T`.

If model discrepancies, boundary inputs, or stochastic increments are introduced at intermediate scales, the chosen correlation specification includes those additional variables and their dependence on upstream states.

`MultiscaleHierarchy` and `compose_partitions` supply the structural mapping of fine groups between levels. A covariance provider uses the selected composed or staged partition together with the declared state and correlation representation.

## 16. Time-Dependent Uncertainty Evolution

For a continuous dynamical system with uncertain initial conditions and parameters:

`d x / dt = f(x, p, t)`.

A linearized perturbation around a reference trajectory satisfies:

`d(delta x)/dt ≈ A(t) delta x + B(t) delta p`,

where `A(t) = partial f / partial x` and `B(t) = partial f / partial p` along that trajectory.

For a discrete state mapping `x[n+1] = F_n(x[n], p[n])`, one covariance step with specified independent process increment `w[n]` may use:

`C[n+1] = J_n C[n] J_n^T + C_w[n]`.

Here `J_n` is the state Jacobian and `C_w[n]` the increment covariance under the declared independence assumption. With correlated increments, the propagation includes the corresponding cross-covariance terms.

A coupled multiscale calculation records the mechanical timestep, resonance integration times, coarse sampling instants, model parameters, and boundary-event times for its uncertainty evolution.

## 17. Nonlinear Regimes and Transition-Conditioned Transfer

For a mapping with multiple locally defined regimes, an uncertainty provider identifies its regime-selection rule, physical state variables, switching surfaces, and temporal history. A piecewise differentiable model may apply a local Jacobian within a declared regime and a specified cross-regime procedure at transitions.

If a model uses an ensemble of alternative regimes, a distributional representation can apply the law of total covariance:

`Cov(Y) = E[Cov(Y | Z)] + Cov(E[Y | Z])`,

where `Z` identifies the selected regime variable in the joint model.

Resonance-window classification, structural reconfiguration, physical material phase, and ternary execution events remain separately defined processes. The uncertainty mapping records which observable and conditioning state was used when its source data were generated.

## 18. Resonance Uncertainty

The continuous resonance state contains oscillator phases, intrinsic frequencies, coupling coefficients, and phase lags. An uncertainty model may assign joint perturbations to these variables under the specified phase-dynamics operator:

`d theta_j / dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

For angular variables, the selected uncertainty procedure uses a defined representation on the circle. Circular residuals, wrapped phase differences, and uncertainties of derived phase-order observables are handled through the chosen circular-statistical or ensemble method.

The resonance propagation trace provides the phase state, directed graph, coupling parameters, graph-sampling instant, and integration timestep. A derived uncertainty record carries the corresponding quantity identifier, state domain, and provenance.

## 19. Balanced-Ternary Execution and Uncertainty

The execution layer uses the exact state alphabet `-1/0/1`, with active neutral `0`. Requested targets, retained states, pending destinations, execution guards, holds, and committed events are categorical fields with exact state-transition rules.

An uncertainty magnitude and a balanced-ternary execution state have distinct types. In particular:

`zero uncertainty ≠ active neutral 0`.

`unknown uncertainty ≠ active neutral 0`.

An uncertainty model over requested targets or execution events declares its own probability, interval, or alternative representation and its mapping to the execution schedule. The committed execution record retains exact `-1/0/1` values and event indices.

## 20. Thermodynamic and Transport Variables

The executable `TransportCoefficient` and `ThermodynamicVariable` records carry quantity identifiers, units, scale and state-domain identifiers, and provenance. Their uncertainty measures can be linked using these same physical and computational domains.

For a constitutive transport mapping `D_target = f(D_source, T, c, p, ...)`, the propagation context specifies the joint uncertainties and correlations of the source coefficient, temperature, composition, pressure, and other model parameters used.

For an equation of state or continuum closure, the target uncertainty belongs to the selected observable and state domain, including its boundary, compositional, and thermodynamic conditions.

## 21. FLiBe Source and Composition Metadata

The repository holds an experimental FLiBe density dataset in `data/reference/flibe_vidrio_2022_density_measurements.json` and an AIMD reference dataset in `data/reference/flibe_baral_2021_aimd_density.json`.

The Vidrio dataset records per-measurement density and temperature uncertainties and ICP-MS composition metadata, including `33.58(5) mol% BeF2`. The Baral dataset records density values calculated at specified AIMD temperatures and associated cell metadata.

A FLiBe uncertainty transfer identifies the corresponding measurement or computation, observable, material composition, temperature, pressure, reference state, unit, and source. Exact `2 LiF : 1 BeF2`, nominal `67 mol% LiF : 33 mol% BeF2`, and measured specimen composition remain separately identified descriptions.

Source-specific uncertainty availability is retained within each source record. A chosen material mapping defines its target uncertainty representation and its connection to these inputs.

## 22. Numerical Example: Correlated Linear Mapping

Consider a numerical example with source variables `x_1 = 2` and `x_2 = 3`, both in the same illustrative unit, and source standard uncertainties:

`u(x_1) = 0.1`.

`u(x_2) = 0.2`.

Choose the linear mapping:

`y = 2 x_1 - x_2 = 1`.

With zero source covariance, the resulting variance and standard uncertainty are:

`u(y)^2 = 4(0.1)^2 + (0.2)^2 = 0.08`.

`u(y) = sqrt(0.08) ≈ 0.2828427125`.

For correlation coefficient `rho_12 = 0.5`, the covariance is `Cov(x_1,x_2) = 0.5(0.1)(0.2) = 0.01`. With Jacobian `(2, -1)`, the mapped variance becomes:

`u(y)^2 = 0.08 - 4(0.01) = 0.04`.

`u(y) = 0.2`.

The two results use the same deterministic mapping and different explicitly defined correlation inputs. The example quantities are mathematical inputs to the transfer method.

## 23. Deterministic Reference Fixture

`tests/integration/test_multiscale_uncertainty_propagation.py` supplies two source measures on the atomistic scale: `energy = 0.2 eV` and `force = 0.1 eV/angstrom`, each identified as `standard_deviation` and bound to the fixture's source state domain.

Its provider returns target measures on the mesoscale: `energy = 0.15 eV` and `force = 0.08 eV/angstrom`. The test checks the typed provider result, canonical ordering, source and context binding, destination scale, and deterministic reconstruction.

The fixture values are provided explicitly by the fixture evaluator. The source and target measures and the context are returned within one `UncertaintyPropagationRecord`.

## 24. Exact Invariants and Numerical Qualification

The executable structural contract includes:

- finite nonnegative numerical magnitudes, stored as floats;
- normalized nonempty quantity, unit, representation, scale, state-domain, and source identifiers;
- nonempty source and target measure tuples;
- canonical ordering by `(scale_id, quantity_id, representation_id, source_id)`;
- unique measure identity keys within each tuple;
- a typed propagation context with five nonempty identifiers;
- target measure `scale_id` equal to the context's `target_scale_id`;
- returned source measures and returned context matching the supplied inputs;
- deterministic results for identical inputs under a deterministic provider.

A numerical uncertainty model additionally declares its correlation structure, propagation rule, sample or derivative method, convergence procedure, and units. Numerical qualification can compare calculated covariance matrices, transformed intervals, source and target normalization, sensitivity derivatives, and repeated provider outputs against independently specified reference calculations.

Exact categorical and collection invariants use exact equality. Floating-point calculations use the numerical method and predeclared comparison tolerances associated with that calculation.

## 25. Reproducibility and Provenance Record

A reproducible uncertainty-transfer evaluation records:

- source quantities, units, physical state domains, scale identifiers, and source identifiers;
- source uncertainty representations and source numeric magnitudes;
- associated covariance, correlation, interval, or ensemble inputs when used;
- the complete `UncertaintyPropagationContext` and its resolved method parameters;
- the source-to-target physical mapping, partition, geometry, and temporal sampling;
- derivative, quadrature, interval, or sampling procedures and numerical precision;
- target measures, representation identifiers, units, scale, and provenance;
- model, boundary, and constitutive parameters included in the selected transfer;
- resonance update times and execution-event indices when conditioning is used;
- deterministic ordering, source data versions, and numerical qualification results.

The output `UncertaintyPropagationRecord` preserves the supplied source collection, target collection, and propagation context under their executable contracts.

## 26. Executable Interfaces and Tests

| Role | Repository path |
| --- | --- |
| Uncertainty measures, context, record, provider | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Multiscale public namespace | `src/tr_eif/multiscale/__init__.py` |
| Structural partition | `src/tr_eif/multiscale/partition.py` |
| Mass and scalar reduction | `src/tr_eif/multiscale/reduction.py` |
| Cartesian coarse centroids | `src/tr_eif/multiscale/geometry.py` |
| Vector averaging | `src/tr_eif/multiscale/vector_average.py` |
| Partition hierarchy | `src/tr_eif/multiscale/hierarchy.py` |
| Transport coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Mesoscale closure | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Continuum closure | `src/tr_eif/multiscale/continuum_closure.py` |
| Resonance propagation | `src/tr_eif/md/resonance_propagation.py` |
| Ternary execution propagation | `src/tr_eif/md/ternary_propagation.py` |
| Uncertainty propagation integration tests | `tests/integration/test_multiscale_uncertainty_propagation.py` |
| Cross-scale integration tests | `tests/integration/test_multiscale_cross_scale_validation.py` |
| FLiBe experimental density data | `data/reference/flibe_vidrio_2022_density_measurements.json` |
| FLiBe AIMD density data | `data/reference/flibe_baral_2021_aimd_density.json` |

## 27. Chapter Integration

Uncertainty transfer associates source quantities and source representations with target scales through explicit method, correlation, assumptions, and normalization identifiers. The executable boundary preserves these associations in a typed provider result with canonical source and target collections.

The mathematical operators in this chapter define covariance, nonlinear, temporal, geometric, and hierarchical propagation procedures for selected source and target state domains. The resulting measures accompany interatomic, atomistic, mesoscale, continuum, and engineering variables with their method, units, and provenance.
