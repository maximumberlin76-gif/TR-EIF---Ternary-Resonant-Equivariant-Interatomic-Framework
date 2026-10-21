
# Engineering Scale Models

## 1. Scope and System Class

This chapter specifies the continuum-to-engineering mapping in TR-EIF, connecting coarse-grained material states and continuum fields with three-dimensional engineering geometry, boundary conditions, external exchange, and numerical solution contexts.

The system class is an open nonlinear dissipative dynamical system. Its engineering realization declares the material domain, physical state, geometry, field variables, constitutive relations, boundary fluxes, time evolution, and coupling schedule. Continuous mechanical, thermodynamic, and resonance variables and balanced-ternary execution remain individually typed.

The mapping chain is:

`electronic/interatomic state → atomistic dynamics → mesoscale state → continuum closure → engineering context → boundary provider → engineering boundary record`.

The executable continuum-to-engineering boundary is `evaluate_engineering_boundaries` in `src/tr_eif/multiscale/engineering_boundary.py`.

## 2. Scale Interfaces and Source State

The engineering boundary receives a complete `ContinuumClosureRecord`. That record contains its upstream `MesoscaleClosureRecord`, named continuum variables, auxiliary variables, closure identifier, and source identifier. The mesoscale record retains its originating `CoarseScaleState`, source and closure identifiers, and closure-variable collections.

For fine atomic masses `m_i` and positions `r_i in R^3`, a coarse structural group `c` has:

`M_c = sum_(i in I_c) m_i`.

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

An engineering mapping selects the spatial reconstruction, state-domain correspondence, and temporal sampling that connect coarse structural observables with continuum variables. The source record and engineering context remain attached to the boundary evaluation.

## 3. Engineering Model State

Let `Omega(t) ⊂ R^3` be a declared engineering material region with boundary `partial Omega(t)`. A selected continuum state may include:

`U(x,t) = (rho, u, T, p, c_s, e, sigma, q, j_s, z, ...)`.

Here `rho` is mass density, `u` is material velocity, `T` is temperature, `p` is pressure, `c_s` is a species concentration, `e` is a specified energy variable, `sigma` is Cauchy stress, `q` is heat flux, `j_s` denotes diffusive species flux, and `z` represents selected internal variables.

The engineering model registers included fields, units, component ordering, geometry, initial conditions, constitutive equations, boundary conditions, numerical discretization, and observation times. Each variable corresponds to its explicitly identified continuum and material-state domain.

## 4. Executable Engineering Boundary Condition

`EngineeringBoundaryCondition` is an immutable dataclass with six fields:

| Field | Stored meaning |
| --- | --- |
| `boundary_id` | Normalized identifier of the selected boundary |
| `variable_id` | Normalized identifier of the affected variable |
| `condition_id` | Normalized identifier of the selected boundary law |
| `values` | Nonempty tuple of finite real values |
| `unit` | Normalized unit identifier for those values |
| `source_id` | Normalized provenance identifier |

Identifier strings are stripped of surrounding whitespace and must remain nonempty. The `values` tuple accepts finite integer and floating-point entries, excluding Boolean values, and normalizes them to floats. Signed and zero values are retained according to the caller-supplied condition.

The provider defines the physical interpretation and component ordering of each condition. A condition may encode prescribed field values, normal fluxes, tractions, exchange coefficients, time-dependent boundary parameters, or other mathematical data identified by `condition_id`.

## 5. Canonical Boundary Collection

For a boundary condition `b`, define its exact identity key:

`key(b) = (b.boundary_id, b.variable_id, b.condition_id)`.

`EngineeringBoundaryConditions` is a tuple of typed conditions. `EngineeringBoundaryRecord` requires a nonempty tuple, unique identity keys, and lexicographically ascending key order.

The record's `condition_count` property returns the tuple cardinality. Units, source identifiers, and numerical values remain stored as distinct fields alongside the identity key. A single boundary may carry multiple variables and multiple identified conditions with distinct keys.

## 6. Engineering Context

`EngineeringBoundaryContext` contains four normalized nonempty identifiers:

- `engineering_model_id`: the selected engineering-scale model;
- `geometry_id`: the spatial domain and its geometrical description;
- `mapping_id`: the selected continuum-to-engineering mapping;
- `assumptions_id`: the constitutive, boundary, and numerical assumptions used by that mapping.

A calculation manifest resolves each identifier to its complete equations, units, parameter values, geometry, applicability domain, and numerical procedure. The context accompanies the continuum input and all returned conditions.

## 7. Engineering Boundary Record and Evaluator

`EngineeringBoundaryRecord` stores exactly three typed components:

`record = (continuum, conditions, context)`.

Its `continuum` field is a `ContinuumClosureRecord`; its `conditions` field is the validated canonical condition tuple; its `context` field is an `EngineeringBoundaryContext`.

The public call is:

`evaluate_engineering_boundaries(continuum, context, evaluator)`.

The evaluator is a callable taking the continuum record and engineering context and returning an `EngineeringBoundaryRecord`. The executable boundary performs the following operations:

1. Validate the continuum-record and engineering-context types and evaluator callability.
2. Invoke the evaluator with the supplied continuum and context.
3. Validate the returned engineering-record type and its canonical boundary collection.
4. Require the returned `continuum` to equal the supplied continuum record.
5. Require the returned `context` to equal the supplied engineering context.
6. Return the complete engineering boundary record.

The evaluator supplies the chosen boundary interpretation, engineering geometry mapping, physical coefficients, units, and numerical values through its registered method.

## 8. Three-Dimensional Boundary Geometry

An engineering geometry identifies the region `Omega`, its material subregions, and oriented boundary surfaces `Gamma_b`. For each smooth surface segment, let `n_b` be the outward unit normal of its associated control region.

A boundary-condition provider resolves `boundary_id` to the selected geometrical support, including area measure, coordinate frame, and boundary-motion law where applicable. For a moving boundary, the boundary velocity `w_b` is recorded separately from the material velocity `u`.

An interface between adjacent regions has two opposing outward normals. Coupled balance equations use a common orientation convention when matching flux contributions from those regions.

## 9. Mathematical Boundary Operators

For a scalar field `a` and a selected boundary segment `Gamma_b`, commonly used physical operators include:

- Prescribed value: `a|_(Gamma_b) = a_D`.
- Prescribed outward normal flux: `J_a · n_b = j_N`.
- Linear exchange: `J_a · n_b = h_a (a_surface - a_environment)`.

For a displacement or velocity vector, the corresponding boundary values are vector-valued. For a stress field, mechanical traction uses a vector derived from the stress tensor and surface normal.

These equations are mathematical boundary-law definitions. The provider assigns each selected law to its `condition_id`, declares the units and ordering of its `values`, and binds the parameters to its geometry and material context.

## 10. Mass and Species Boundary Exchange

For total mass density `rho` and velocity `u`, a fixed-domain mass balance with volumetric source `s_m` is:

`partial_t rho + div(rho u) = s_m`.

For species `s`, with concentration `c_s`, diffusive flux `j_s` relative to `u`, and source `q_s`:

`partial_t c_s + div(c_s u + j_s) = q_s`.

The outward species mass flow through boundary segment `Gamma_b` is:

`Phi_s,b = integral_(Gamma_b) (c_s u + j_s) · n_b dA`.

An exchange provider identifies the transported species, concentration convention, constitutive flux, boundary geometry, and any applied reservoir or interface condition. The integral balance connects the region inventory change with these oriented fluxes and internal sources.

## 11. Momentum Loads and Mechanical Traction

For the Cauchy stress tensor `sigma`, the traction acting across a surface with outward normal `n_b` is:

`t_b = sigma n_b`.

The net boundary force is:

`F_b = integral_(Gamma_b) t_b dA`.

With mass density `rho`, velocity `u`, body acceleration `b`, and an identified momentum source `s_p`, a continuum momentum balance is:

`partial_t(rho u) + div(rho u ⊗ u) = div(sigma) + rho b + s_p`.

A boundary model specifies prescribed displacement, velocity, traction, pressure loading, or coupled contact and exchange laws through its selected condition identifiers. Mechanical work and power follow the matching velocity and traction conventions.

## 12. Heat Exchange and Thermal Boundaries

For heat flux `q = -k grad(T)` with conductivity `k` in an isotropic Fourier representation, the outward conductive heat power on a boundary segment is:

`Qdot_out,b = integral_(Gamma_b) q · n_b dA`.

A linear convective exchange boundary may be written:

`q · n_b = h_T (T_surface - T_environment)`.

Here `h_T` is the declared heat-transfer coefficient and the ambient temperature is a separately identified input. For a fully specified thermal balance, the model includes energy carried by advected species, mechanical work, volumetric sources, and any additional declared heat-exchange operators.

The engineering record can carry boundary values and exchange parameters; their units and surface associations are resolved by the chosen provider and geometry context.

## 13. Engineering Energy Accounting

Let `e_total,V` be a defined total-energy density and `J_E` its total energy flux. For a fixed control volume:

`partial_t e_total,V + div(J_E) = s_E`.

Integrated over `Omega`:

`d/dt integral_Omega e_total,V dV = -integral_(partial Omega) J_E · n dA + integral_Omega s_E dV`.

The total energy flux combines the selected advective, conductive, mechanical, and species-carried terms using one physical sign and storage convention. Boundary work, externally applied power, and material exchange are identified by their contributing conditions and associated physical times.

When boundaries move, the control-volume balance uses the relative flux `J_E - e_total,V w_b` and the selected boundary motion.

## 14. Interface Matching Between Engineering Regions

Consider two neighboring control regions with opposing outward normals `n_1 = -n_2` at a shared interface. A flux-conserving interface with zero interfacial storage and source satisfies:

`J_1 · n_1 + J_2 · n_2 = 0`.

An interface law with storage or source terms uses the corresponding interfacial balance. Coupled fields may also use prescribed continuity, partition, jump, or resistance relations according to their constitutive definitions.

A geometry-aware engineering mapping registers both boundary identities, orientation, shared interface, coefficient provenance, and numerical flux formulation.

## 15. Continuum Discretization at Engineering Scale

For a fixed finite-volume cell `Omega_alpha`, define its integrated conserved quantity:

`Q_alpha = integral_(Omega_alpha) a(x,t) dV`.

With face areas `A_f`, outward normals `n_(alpha,f)`, and source integral `S_alpha`, a forward finite-volume update is:

`Q_alpha[n+1] = Q_alpha[n] - dt sum_(f in faces(alpha)) A_f J_f · n_(alpha,f) + dt S_alpha`.

A boundary provider supplies the face condition and any required ghost, surface, or interface states through the numerical method. Shared interior-face fluxes use opposite orientations for adjacent cells, yielding cancellation when summed over the combined region.

The discretization context specifies cell geometry, field representation, timestep, flux evaluation, source quadrature, and numerical boundary rule.

## 16. Discrete Conservation Example

Consider two fixed cells with initial inventories `Q_0 = 10 kg` and `Q_1 = 4 kg`. A single interior face carries mass flux `2 kg/s` from cell 0 to cell 1 over an interval `dt = 0.1 s`, with zero external boundary flux and zero source.

The conservative update gives:

`Q_0,next = 10 - 0.1(2) = 9.8 kg`.

`Q_1,next = 4 + 0.1(2) = 4.2 kg`.

The combined inventory remains:

`Q_0,next + Q_1,next = 14 kg = Q_0 + Q_1`.

The calculation uses explicitly oriented face fluxes and a common numerical update interval. The same cancellation structure applies to an appropriately defined discretized conserved quantity and its corresponding internal face flux.

## 17. Geometry and E(3) Transformation

Under an orthogonal transformation `Q in O(3)` and translation `b`, positions and surface normals transform as:

`x' = Q x + b`.

`n_b' = Q n_b`.

Cartesian flux vectors and stress tensors transform as:

`J' = Q J`.

`sigma' = Q sigma Q^T`.

Consequently:

`J' · n_b' = J · n_b`.

`t_b' = sigma' n_b' = Q t_b`.

A geometry mapping associates the transformed domain, boundary supports, field components, and orientation conventions with the corresponding model context. Scalar flux integrals retain their geometrical meaning under these transformations.

## 18. Thermal, Mechanical, and Chemical Coupling

A material engineering state may couple temperature, pressure, velocity, concentration, and internal variables through nonlinear constitutive operators. An example coefficient dependence is:

`k = k(T, c, p, z)`.

`eta = eta(T, c, p, z)`.

`j_s = J_s(U, grad(U), z; Theta)`.

Here `Theta` denotes the selected constitutive parameters and `z` the internal state. The numerical coupling specifies how each field and parameter is sampled and updated and how boundary values enter its equations.

A time-dependent provider records the state and history used to evaluate an engineering condition at each boundary update instant.

## 19. Transport and Thermodynamic State Transfer

`TransportCoefficientTransferRecord` binds source and target coefficient records to `TransportTransferContext`; each coefficient retains its unit, scale, state domain, and source identifier. An engineering flux law uses the corresponding target coefficient under its declared state conditions.

`ThermodynamicConsistencyRecord` binds source and target thermodynamic variables to a selected relation, model, assumptions, normalization, and evaluator result. Pressure, temperature, density, chemical potential, and energy definitions are matched to their selected state and units when used in the engineering model.

The engineering provider links these multiscale records to boundary-condition values and constitutive coefficients through its `mapping_id` and associated resolved method configuration.

## 20. Uncertainty and Parameter Propagation

`UncertaintyPropagationRecord` retains source and target `UncertaintyMeasure` collections and `UncertaintyPropagationContext`. The uncertainty representation includes quantity, unit, state domain, scale, source, and correlation or method identifiers.

For an engineering output `y = f(x)` with differentiable dependence on uncertain inputs and source covariance `C_x`, a first-order covariance mapping is:

`C_y ≈ J C_x J^T`, with `J = partial f / partial x` at the declared evaluation state.

An engineering uncertainty evaluation identifies boundary measurements, geometry parameters, transport coefficients, model parameters, numerical error, and their correlations as applicable to the chosen output. The boundary record retains the underlying numerical boundary conditions separately from the associated uncertainty representation.

## 21. Continuous Resonance at Engineering Scale

A coupled atomistic source can evolve its continuous oscillator state through directed Kuramoto–Sakaguchi dynamics:

`d theta_j / dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A cross-scale mapping may reconstruct a continuous resonance-related field or internal variable from the declared fine-scale phase state, spatial partition, temporal averaging rule, and descriptor definition. The resulting field enters an engineering constitutive or boundary operator through its typed mapping context.

The engineering trace identifies phase-state sampling, graph geometry, parameterization, scale transfer, and the selected continuum variable used in the boundary calculation.

## 22. Balanced-Ternary Execution and Boundary Conditioning

The execution alphabet is `-1/0/1`, with `0` as active neutral. Requests, retained values, pending destinations, guards, holds, and committed transitions have distinct execution semantics.

Opposite-polarity committed routes use separate events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

A selected engineering control mapping can use executed states to condition a material coefficient, routing decision, boundary mode, or control input. That mapping identifies its categorical execution operator, physical state inputs, and update schedule. Continuous physical field values retain their independent numerical state spaces.

A coupling trace records the executed vector and event index used for every engineering-boundary evaluation conditioned by ternary execution.

## 23. FLiBe Engineering-State Identification

A FLiBe engineering realization can connect species and composition records, interatomic and atomistic observables, coarse-scale geometry, thermodynamic variables, transport coefficients, and coolant boundary conditions.

The `FLiBeMultiscaleCoolantModel` produces a structural hierarchy from a `FLiBeConfiguration`, mass parameters, and an explicitly selected fine-position representation. Periodic configurations supply the selected unwrapped Cartesian positions for their structural mapping.

The downstream engineering state identifies LiF–BeF2 composition, temperature, pressure, geometry, flow regime, boundary heat or species flux, constitutive coefficients, and source provenance. Exact `2 LiF : 1 BeF2`, nominal `67 mol% LiF : 33 mol% BeF2`, and measured specimen compositions remain separate source definitions.

A boundary provider links the selected FLiBe state and continuum closure to identified thermal, mechanical, and species-transfer conditions.

## 24. Existing Numerical Test Fixture

`tests/integration/test_multiscale_engineering_boundary.py` constructs a two-entity `CoarseScaleState` with:

`partition = (0, 0, 1, 1)`.

`coarse_positions = ((0.5, 0, 0), (2.5, 0, 0))`.

`coarse_masses = (2.0, 4.0)`.

The fixture's mesoscale record contains `flux = (1.0, -1.0)`, while its continuum record contains `field_a = (1.0, 2.0)`. The engineering context has model, geometry, mapping, and assumptions identifiers.

The engineering provider returns a canonical two-condition collection:

| Boundary | Variable | Condition | Values | Unit |
| --- | --- | --- | --- | --- |
| `boundary-a` | `field_a` | `condition-a` | `(1.0, 2.0)` | `unit-a` |
| `boundary-b` | `field_b` | `condition-b` | `(-1.0,)` | `unit-b` |

The fixture checks `condition_count = 2`, identity of the supplied continuum and context, condition normalization, ordering, provider binding, and deterministic reconstruction. Its identifiers and units are those declared by the fixture.

## 25. Exact Invariants and Numerical Checks

The executable structural checks include:

- `EngineeringBoundaryCondition` identifiers normalized to nonempty strings;
- a nonempty immutable tuple of finite real `values` for each condition;
- Boolean values excluded from numeric boundary components;
- a nonempty canonical tuple of uniquely keyed conditions;
- exact identity keys `(boundary_id, variable_id, condition_id)`;
- a typed engineering context with four normalized identifiers;
- a typed `ContinuumClosureRecord` as the upstream state;
- `condition_count` equal to the number of stored conditions;
- returned continuum and context equal to the input values;
- deterministic output ordering for a deterministic provider.

Numerical qualification of an engineering realization uses its selected conservation balances, interface-flux continuity, transformed geometry, material constitutive operators, boundary response, timestep or mesh refinement, and uncertainty propagation. Each numerical comparison uses its declared quantities, method, units, and preselected tolerance.

## 26. Reproducibility Record

A reproducible engineering-scale evaluation records:

- the upstream `ContinuumClosureRecord`, including mesoscale and coarse-state provenance;
- `engineering_model_id`, `geometry_id`, `mapping_id`, and `assumptions_id`;
- identified material regions, meshes, boundaries, orientations, and boundary-motion laws;
- every `EngineeringBoundaryCondition` with its key, values, units, and source;
- the resolved physical condition type and its constitutive parameters;
- continuum field definitions, component order, initial values, and physical units;
- supplied transport and thermodynamic coefficients and their material-state domains;
- spatial discretization, numerical flux, integration schedule, and convergence method;
- external forcing, thermal exchange, mechanical work, and material flux definitions;
- resonance descriptor inputs and execution-event indices when used;
- uncertainty representation, correlation context, and parameter provenance;
- numerical output fields, balance observables, and deterministic replay inputs.

The resulting engineering record provides one typed boundary-condition collection linked to the exact continuum state and engineering context used for its construction.

## 27. Executable Interface Index

| Role | Repository path |
| --- | --- |
| Engineering conditions, context, record, evaluator | `src/tr_eif/multiscale/engineering_boundary.py` |
| Continuum variables and closure provider | `src/tr_eif/multiscale/continuum_closure.py` |
| Mesoscale variables and closure provider | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Coarse structural state | `src/tr_eif/multiscale/state.py` |
| Fine-to-coarse partitions | `src/tr_eif/multiscale/partition.py` |
| Mass and geometric reductions | `src/tr_eif/multiscale/reduction.py`, `src/tr_eif/multiscale/geometry.py` |
| Transport coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Interatomic energy provider | `src/tr_eif/energy/model.py` |
| Molecular trajectory | `src/tr_eif/md/trajectory.py` |
| MD resonance and ternary execution | `src/tr_eif/md/resonance_propagation.py`, `src/tr_eif/md/ternary_propagation.py` |
| FLiBe structural scale transfer | `src/tr_eif/flibe/multiscale_coolant.py` |

## 28. Existing Test Interfaces

| Domain | Repository test path |
| --- | --- |
| Engineering boundary conditions and provider binding | `tests/integration/test_multiscale_engineering_boundary.py` |
| Complete typed cross-scale chain | `tests/integration/test_multiscale_cross_scale_validation.py` |
| Continuum closure interface | `tests/integration/test_multiscale_continuum_closure.py` |
| Mesoscale closure interface | `tests/integration/test_multiscale_mesoscale_closure.py` |
| Thermodynamic consistency | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Transport coefficient transfer | `tests/integration/test_multiscale_transport_transfer.py` |
| Uncertainty propagation | `tests/integration/test_multiscale_uncertainty_propagation.py` |
| FLiBe structural hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |

These tests exercise typed boundary identities, finite values, canonical ordering, provider input binding, context retention, cross-scale records, and deterministic execution with fixed fixtures.

## 29. Chapter Integration

Engineering-scale modeling in TR-EIF maps a typed continuum closure and an identified model/geometry context into a canonical collection of boundary conditions. The executable record retains source and target associations, field and boundary identities, units, and numerical values.

The mathematical engineering layer connects conservation equations, surface and interface fluxes, mechanical loads, thermal and species exchange, three-dimensional geometry, and constitutive mappings. Transport, thermodynamic, uncertainty, continuous resonance, and active-ternary inputs are incorporated through individually identified scale and event mappings.
