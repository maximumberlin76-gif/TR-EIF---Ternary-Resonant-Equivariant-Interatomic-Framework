
# Continuum Closure

## 1. Scope and System Class

This chapter defines the mesoscale-to-continuum mapping in TR-EIF for open nonlinear dissipative dynamical systems. It specifies the representation of continuum fields, their local and integral balance equations, constitutive inputs, exchange terms, spatial and temporal scale transfer, and the executable closure-provider contract.

The multiscale chain is:

`atomistic configuration → fine-to-coarse mapping → CoarseScaleState → MesoscaleClosureRecord → continuum provider → ContinuumClosureRecord → engineering boundary provider`.

The continuous atomic, mechanical, thermodynamic, and resonance variables remain defined in their respective state spaces. Balanced-ternary `-1/0/1` execution has a separate, explicitly scheduled state and event mapping. The framework couples these components through typed inputs and recorded transformations.

## 2. State Domains and Continuum Fields

Let `Omega(t) ⊂ R^3` denote the selected physical control region with boundary `partial Omega(t)`, and let `x ∈ Omega(t)` be a Cartesian spatial coordinate. The continuum state can be represented by a collection of fields:

`U(x,t) = (rho, u, e, T, species, sigma, q, j, z, ...)`.

Here `rho` is mass density, `u ∈ R^3` is material velocity, `e` is specific internal energy, `T` is thermodynamic temperature, `sigma` is the Cauchy stress tensor, `q` is heat flux, `j` denotes declared species or other transport fluxes, and `z` contains material-specific internal variables. The selected realization assigns each included field its domain, unit, reference frame, and state variables.

The spatial geometry, cell or mesh representation, and material-domain identifiers belong to the continuum model configuration. For a moving region, its boundary velocity is declared separately from material velocity.

## 3. Atomistic and Mesoscale Input State

The source `CoarseScaleState` contains a fine-to-coarse partition, Cartesian coarse positions, and positive coarse masses. For partition membership `I_c`:

`M_c = sum_(i in I_c) m_i`.

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

`MesoscaleClosureRecord` binds that coarse state to `closure_id`, `source_id`, a nonempty canonical collection of `MesoscaleClosureVariable` outputs, and an optional collection of auxiliary variables.

For each mesoscale variable, `name` identifies the quantity within its collection and `values` is a nonempty tuple of finite real numbers. Its physical meaning, spatial support, normalization, and units are defined in the chosen closure context.

The full mesoscale record is passed into the continuum provider, retaining the coarse-state geometry and the preceding closure's provenance.

## 4. Mesoscale-to-Continuum Mapping

Let `X_m` denote a mesoscale state and `C_mc` the explicitly identified mapping context. A continuum state construction is written:

`M_(m→c): (X_m, C_mc) → X_c`.

For a spatially resolved continuum field `a(x,t)`, one possible geometric transfer from discrete mesoscale entities is:

`a(x,t) = sum_c W_c(x,t) A_c(t)`.

The basis or weighting functions `W_c` specify support, normalization, boundary treatment, and spatial reconstruction. A conservative density transfer is defined with weights that preserve the declared integrated source quantity under the selected volume measure.

Alternatively, for a control cell `Omega_alpha`, a cell-average variable is:

`a_alpha(t) = (1/V_alpha) integral_(Omega_alpha) a(x,t) dV`.

The particular reconstruction, filtering, constitutive inference, and numerical discretization are selected by the closure provider and its declared context. `ContinuumClosureRecord` stores the provider's typed output variables and the complete upstream mesoscale record.

## 5. Executable Continuum Variable

`ContinuumClosureVariable` in `src/tr_eif/multiscale/continuum_closure.py` is an immutable dataclass with:

- `name`: a nonempty string, stripped of surrounding whitespace;
- `values`: a nonempty tuple of finite real numbers, normalized to `float`.

The type rejects Boolean and nonnumeric elements and requires a tuple representation. Vector and tensor components may be represented within `values` according to an externally identified component-order and geometry convention.

`ContinuumClosureVariables` denotes a tuple of these typed variables. Collections are checked for unique normalized names and ascending canonical name order. Output and auxiliary collections are validated as separate collections.

A continuum variable's unit, component semantics, spatial support, and temporal sampling are attached through the corresponding provider or dataset context.

## 6. Executable Continuum Record

`ContinuumClosureRecord` is an immutable record with the fields:

| Field | Contract |
| --- | --- |
| `mesoscale` | Exact upstream `MesoscaleClosureRecord` input |
| `closure_id` | Nonempty normalized closure identifier |
| `source_id` | Nonempty normalized provenance identifier |
| `continuum_variables` | Nonempty, canonical tuple of `ContinuumClosureVariable` outputs |
| `auxiliary_variables` | Canonical tuple of caller-supplied `ContinuumClosureVariable` inputs; empty tuple permitted |

The record exposes `variable_count` and `variable(name)`. The latter normalizes the requested name, returns the matching output variable, and raises `KeyError` when the name is absent.

The record retains mesoscale source geometry and closure outputs through its upstream field. Continuum output values and caller-supplied auxiliary inputs occupy distinct record fields.

## 7. Provider Evaluation and Input Binding

The executable interface is:

`evaluate_continuum_closure(mesoscale, evaluator, auxiliary_variables=())`.

The `ContinuumClosureEvaluator` accepts a `MesoscaleClosureRecord` and a tuple of `ContinuumClosureVariable` auxiliary inputs, then returns a `ContinuumClosureRecord`.

The evaluation sequence is:

1. Validate the mesoscale input type and evaluator callability.
2. Validate auxiliary-variable types, unique names, and canonical ordering.
3. Invoke the provider with the complete mesoscale record and validated auxiliary tuple.
4. Validate the returned continuum-record type.
5. Compare the returned `mesoscale` field with the supplied mesoscale record.
6. Compare the returned `auxiliary_variables` field with the supplied auxiliary tuple.
7. Return the typed result with its `closure_id`, `source_id`, and continuum variables.

The provider supplies its selected constitutive equations, parameter values, numerical procedure, and physical-field interpretation. The boundary function enforces typed inputs, explicit provenance, and correspondence between input and returned state.

## 8. Continuum Conservation Form

For a conserved density `a(x,t)`, flux `J_a(x,t)`, and volumetric source `s_a(x,t)`, define the local conservation equation on a fixed spatial domain:

`partial_t a + div(J_a) = s_a`.

For fixed control region `Omega` with outward unit normal `n`, its integral balance is:

`d/dt integral_Omega a dV + integral_(partial Omega) J_a · n dA = integral_Omega s_a dV`.

If the control boundary moves with velocity `w`, the corresponding relative-flux form is:

`d/dt integral_(Omega(t)) a dV + integral_(partial Omega(t)) (J_a - a w) · n dA = integral_(Omega(t)) s_a dV`.

The selected density, flux, source, and boundary motion determine the physical meaning of each term. Multiple coupled conserved variables are represented through a vector balance with consistent component conventions.

## 9. Mass and Species Balances

Let `rho(x,t)` be mass density and `u(x,t)` the barycentric velocity. For a mixture with a declared net mass source `s_m`, the mass balance is:

`partial_t rho + div(rho u) = s_m`.

For species `s`, let `c_s` be mass concentration, `j_s` the diffusive species mass flux relative to `u`, and `q_s` the net species mass source. Its balance is:

`partial_t c_s + div(c_s u + j_s) = q_s`.

The material realization specifies species identifiers, composition definition, chemical or interfacial source terms, and boundary fluxes. For a mixture with all species accounted for, the species balances and total-mass balance are reconciled through their common mass and flux definitions.

When a Fickian closure is selected for a particular state domain, a scalar example is:

`j_s = -D_s grad(c_s)`.

For multicomponent materials, the flux may be a coupled constitutive function of chemical potentials, temperature, electric fields, and other declared state variables.

## 10. Momentum Balance and Stress Closure

For a continuum with mass density `rho`, velocity `u`, Cauchy stress `sigma`, body force per unit mass `b`, and a declared momentum source `s_p`:

`partial_t(rho u) + div(rho u ⊗ u) = div(sigma) + rho b + s_p`.

Here `u ⊗ u` is the second-order outer product and the divergence of a tensor returns a Cartesian vector.

A constitutive stress decomposition can be declared as:

`sigma = -p I + tau`.

For a Newtonian isotropic viscous realization in a specified domain:

`tau = 2 eta D_dev + zeta (div u) I`.

`D = (grad u + (grad u)^T)/2`.

`D_dev = D - (div u / 3) I`.

The shear viscosity `eta`, bulk viscosity `zeta`, equation of state for `p`, and additional constitutive effects are supplied by the selected material model. Atomistic stress observables use their declared volume, differentiation, and averaging conventions when transferred into this continuum representation.

## 11. Energy Balance and Dissipation

Define specific internal energy `e` and total specific energy:

`e_total = e + |u|^2/2`.

For a fixed-frame continuum with symmetric stress, heat flux `q`, body-force acceleration `b`, and a declared external volumetric energy source `s_E`, a total-energy balance is:

`partial_t(rho e_total) + div(rho e_total u) = div(sigma u) - div(q) + rho b · u + s_E`.

The flux `q` and source `s_E` use definitions consistent with species enthalpy transport, reaction energy, and other contributions included in the realization. For a Fourier heat-conduction model:

`q = -k grad(T)`.

The internal-energy balance, where the corresponding matter exchange convention is included in its source terms, takes the form:

`rho D_t e = sigma : D - div(q) + s_e`.

`D_t = partial_t + u · grad` is the material derivative. The `sigma : D` contraction records mechanical stress power, including viscous contributions under the selected stress law.

The open-system energy record associates boundary heat, mechanical work, transported energy, and material exchange with its defined storage and flux operators.

## 12. Constitutive Internal Variables and History

Let `z(x,t)` represent one or more continuous internal material variables. A transport-and-evolution form is:

`partial_t z + u · grad(z) = G_z(U, z, grad U, context)`.

A history-dependent realization can introduce memory states or kernels. For instance, a causal constitutive contribution may be parameterized by:

`H(t) = integral_(0→t) K(t-s) A(s) ds`.

The internal-state domain, initial history, kernel, boundary behavior, and applicable time interval are declared together with the selected model. Such variables may represent local structure, relaxation, composition fields, or material-specific nonequilibrium organization.

This state representation supports continuous residence, relaxation, and transition trajectories within the selected constitutive model.

## 13. Spatial and Temporal Scale Separation

Let `ell_f` be a characteristic fine-scale length and `ell_c` a continuum observation scale, with both positive. A scale ratio is:

`epsilon = ell_f / ell_c`.

A selected averaging or homogenization procedure defines the coarse field, its spatial support, and the dependence of effective parameters on the chosen sampling length and time. For a time window `Delta t`, a time-averaged observable may be defined by:

`A_bar(t) = (1/Delta t) integral_(t→t+Delta t) A(s) ds`.

A coupled schedule identifies the atomistic sampling instants, mesoscale closure evaluations, continuum update times, and any boundary or execution events inside each window.

A change of partition, region geometry, or temporal scale is included in the mapping trace with its source and target state identifiers.

## 14. Numerical Continuum Discretization

For a finite-volume cell `Omega_alpha` with volume `V_alpha`, let:

`Q_alpha(t) = integral_(Omega_alpha) a(x,t) dV`.

Applying the fixed-cell integral balance to a numerical update with positive `dt` gives the conservative form:

`Q_alpha[n+1] = Q_alpha[n] - dt sum_(f in faces(alpha)) A_f J_f · n_(alpha,f) + dt S_alpha`.

Here `J_f` is the defined numerical face flux, `A_f` its face area, `n_(alpha,f)` the outward normal, and `S_alpha` the cell-integrated source under the selected quadrature rule.

For a shared internal face between adjacent cells, equal-and-opposite oriented flux contributions cancel in the global discrete balance when both cells use one consistent numerical face flux.

The continuum provider defines its discretization geometry, boundary values, stabilization, timestep control, constitutive evaluation, and source integration. The typed output record may store resulting field components or derived observables with a declared component ordering.

## 15. Three-Dimensional Geometric Covariance

Under an admissible orthogonal transformation `Q ∈ O(3)` and translation `b ∈ R^3`, spatial coordinates transform as:

`x' = Q x + b`.

A scalar continuum field obeys `a'(x',t) = a(x,t)`; a polar vector field obeys `u'(x',t) = Q u(x,t)`; and a Cartesian second-order stress tensor obeys:

`sigma'(x',t) = Q sigma(x,t) Q^T`.

The corresponding flux, gradient, divergence, boundary-normal, and volume-transformation rules are applied to the complete transformed physical configuration. An equivariant mesoscale-to-continuum provider carries its selected spatial support and input fields through these transformations.

Mass, volume-integrated scalar quantities, and selected invariant energy observables follow their declared transformation and normalization conventions.

## 16. Resonance State Coupling

The atomistic resonance layer evolves continuous oscillator phases through the selected directed Kuramoto–Sakaguchi operator:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A mesoscale-to-continuum resonance mapping receives the continuous resonance state or declared descriptors, the fine-to-coarse partition, spatial averaging context, and sampling times. Its output can be a scalar field, vector field, or continuous internal variable with defined units and transformation behavior.

The global phase-order quantity `R_phase`, local phase relationships, resonance-window coordinates, and continuum material fields have separate definitions. A mapped descriptor is associated with the selected physical state, scale, and numerical update time in the continuum closure trace.

## 17. Balanced-Ternary Execution Coupling

The balanced-ternary execution layer uses retained values `-1/0/1`, with `0` as active neutral. Its retained state, pending destination, target request, guard, held event, and committed event are separately recorded.

Opposite-polarity committed routes proceed by distinct events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

The continuum coupling specifies a mapping from continuous or mesoscale descriptors to an execution request, followed by guarded execution and a selected conditioning operator. Fine-to-coarse arithmetic reductions apply to physical numerical quantities; execution-state aggregation follows an explicitly defined categorical mapping.

A continuum variable may be conditioned by the executed state while preserving its continuous numerical domain. The trace identifies the retained execution vector and committed-event indices used in each continuum update.

## 18. Thermodynamic and Transport Transfer

`ThermodynamicVariable` identifies a numeric value by variable, unit, scale, state domain, and source. `ThermodynamicConsistencyContext` identifies the relation, model, assumptions, and normalization; the evaluator returns a `ThermodynamicConsistencyRecord` with its explicit result field.

`TransportCoefficient` similarly carries coefficient identity, numerical value, unit, scale, state domain, and source. `TransportTransferContext` identifies destination scale, mapping, normalization, and assumptions. `evaluate_transport_coefficient_transfer` binds a provider's target coefficient to its source record and context.

A continuum constitutive law draws its coefficients from the selected transfer records and material context. Species self-diffusion, cross-diffusion, thermal conductivity, viscosity, and other coefficients retain their separate physical definitions and operating domains.

## 19. Uncertainty Transfer

`UncertaintyMeasure` identifies quantity, numerical uncertainty, unit, representation, scale, state domain, and source. `UncertaintyPropagationContext` specifies destination scale, propagation rule, assumptions, correlation model, and normalization.

`evaluate_uncertainty_propagation` invokes the declared provider and produces the associated `UncertaintyPropagationRecord`. A continuum uncertainty report identifies how source measurement uncertainty, model parameters, spatial averaging, numerical integration, and boundary-input variability enter each selected output observable.

The representation and correlation model determine the applicable propagation operation. Numerical tolerance, source uncertainty, and categorical execution-state semantics retain their distinct types.

## 20. Engineering Boundary Mapping

The continuum-to-engineering interface is:

`evaluate_engineering_boundaries(continuum, context, evaluator)`.

`EngineeringBoundaryContext` supplies `engineering_model_id`, `geometry_id`, `mapping_id`, and `assumptions_id`. Each `EngineeringBoundaryCondition` contains a boundary identifier, variable identifier, condition identifier, finite value tuple, unit, and source identifier.

The resulting `EngineeringBoundaryRecord` retains the continuum record, the complete context, and a nonempty canonically ordered set of boundary conditions. The provider binds the selected physical boundary law and engineering geometry to these typed records.

For continuum evolution, the boundary model may prescribe or relate field values, normal fluxes, mechanical tractions, thermal exchange, material transfer, and geometry evolution according to its declared condition identifiers.

## 21. Numerical Example from the Executable Contract

The continuum integration fixture defines a two-entity coarse state from the partition:

`p = (0, 0, 1, 1)`.

Its coarse positions and masses are:

`R = ((0.5, 0, 0), (2.5, 0, 0))`.

`M = (2.0, 4.0)`.

The mesoscale fixture has `closure_id = "mesoscale-a"`, `source_id = "source-m"`, and two named output variables: `flux = (1.0, -1.0)` and `source = (0.25, 0.5)`.

The continuum provider fixture returns `closure_id = "continuum-a"`, `source_id = "source-c"`, and the ordered output variables:

`field_a = (1.0, 2.0)`.

`field_b = (-0.5, 0.75)`.

Auxiliary inputs `boundary_input = (3.0, 4.0)` and `history_input = (0.1, 0.2)` are passed to the provider and retained in the result. The test verifies the returned input binding, named variable access, and deterministic reconstruction of the record.

These values are the defined numerical test fixture; material units and constitutive interpretation are supplied separately in a material realization.

## 22. Exact Invariants and Numerical Qualification

The executable categorical checks include:

- a `MesoscaleClosureRecord` input to the continuum provider;
- a callable evaluator and a `ContinuumClosureRecord` output;
- nonempty normalized `closure_id`, `source_id`, and variable names;
- a nonempty tuple of finite real values for each `ContinuumClosureVariable`;
- unique names and ascending canonical name order within each variable collection;
- a nonempty continuum output collection and an optional empty auxiliary collection;
- equality of the returned upstream mesoscale record and supplied mesoscale input;
- equality of returned and supplied auxiliary-variable tuples;
- lookup of an output variable by normalized name;
- deterministic results for identical inputs and a deterministic provider.

Numerical qualification of a selected physical continuum realization may include integral conservation residuals, surface-flux cancellation, E(3) transformation checks, spatial and timestep refinement, constitutive consistency, thermodynamic identities, uncertainty propagation, and response to prescribed boundary changes. Each numerical comparison uses its declared method and preselected tolerance.

## 23. Reproducibility Record

A reproducible continuum evaluation identifies:

- source atomic configuration, coarse partition, masses, centroids, and sampling time;
- the complete mesoscale record and its closure and source identifiers;
- continuum provider identity, mathematical mapping, and material state domain;
- names, component ordering, physical units, and spatial support of continuum variables;
- supplied auxiliary variables, initial conditions, and history inputs;
- governing balance equations, constitutive terms, and source definitions;
- spatial discretization, cell or mesh geometry, numerical flux, and timestep scheme;
- thermal, mechanical, and material boundary conditions and exchange sign conventions;
- thermodynamic and transport coefficient sources and normalization contexts;
- continuous resonance descriptor inputs and integration instants, where coupled;
- retained and pending ternary states, guards, and committed event order, where coupled;
- numerical tolerances, refinement parameters, output observables, and uncertainty context.

The provider result is associated with these inputs and the ordered sequence of evaluated scale-transfer operators.

## 24. Executable Interface Index

| Role | Repository path |
| --- | --- |
| Fine-to-coarse structural partition | `src/tr_eif/multiscale/partition.py` |
| Coarse masses and Cartesian centroids | `src/tr_eif/multiscale/reduction.py`, `src/tr_eif/multiscale/geometry.py` |
| Coarse-scale state construction | `src/tr_eif/multiscale/state.py` |
| Mesoscale closure input | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Continuum closure record and evaluator | `src/tr_eif/multiscale/continuum_closure.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Transport coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Engineering boundary mapping | `src/tr_eif/multiscale/engineering_boundary.py` |
| Multiscale partition hierarchy | `src/tr_eif/multiscale/hierarchy.py` |
| Atomistic energy provider | `src/tr_eif/energy/model.py` |
| Mechanical state and trajectory | `src/tr_eif/md/state.py`, `src/tr_eif/md/trajectory.py` |
| Resonance and execution bridges | `src/tr_eif/md/resonance_propagation.py`, `src/tr_eif/md/ternary_propagation.py` |
| FLiBe structural scale transfer | `src/tr_eif/flibe/multiscale_coolant.py` |

## 25. Existing Test Interfaces

| Scope | Repository test path |
| --- | --- |
| Continuum variable and provider contracts | `tests/integration/test_multiscale_continuum_closure.py` |
| Mesoscale closure input | `tests/integration/test_multiscale_mesoscale_closure.py` |
| End-to-end typed scale boundary chain | `tests/integration/test_multiscale_cross_scale_validation.py` |
| Engineering boundary record | `tests/integration/test_multiscale_engineering_boundary.py` |
| Thermodynamic relation records | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Transport-coefficient transfer | `tests/integration/test_multiscale_transport_transfer.py` |
| Uncertainty propagation | `tests/integration/test_multiscale_uncertainty_propagation.py` |
| Fine-to-coarse geometry invariants | `tests/invariants/test_multiscale_geometry_invariants.py` |
| Coarse-state invariants | `tests/invariants/test_multiscale_state_invariants.py` |
| FLiBe hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |

The tests exercise typed variables, source-state correspondence, canonical ordering, provider input and output binding, cross-scale records, and deterministic evaluation with their specified test fixtures.

## 26. Summary

The TR-EIF continuum closure maps a typed mesoscale state into ordered, named continuum variables through an explicitly selected evaluator. The continuum mathematical structure combines spatial fields, mass/momentum/energy balances, exchange fluxes, constitutive relations, boundary conditions, and numerical discretization.

The executable continuum record retains its mesoscale input, source identifier, output variables, and auxiliary inputs. Thermodynamic, transport, uncertainty, engineering, continuous-resonance, and active-ternary interfaces connect through separately identified mappings and schedules within the multiscale architecture.
