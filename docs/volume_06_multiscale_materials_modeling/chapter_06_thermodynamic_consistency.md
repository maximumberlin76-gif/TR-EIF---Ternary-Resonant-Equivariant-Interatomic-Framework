
# Thermodynamic Consistency

## 1. Scope and System Class

This chapter specifies thermodynamic variables, state correspondence, balance relations, constitutive identities, and cross-scale consistency evaluation in the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The system class is an open nonlinear dissipative dynamical system. Its physical description combines three-dimensional atomic configurations, mechanical evolution, thermal and material exchange, continuous resonance dynamics, and separately scheduled balanced-ternary execution.

The multiscale thermodynamic chain is:

`electronic and interatomic observables → atomistic state and trajectory → spatial and temporal reduction → mesoscale variables → continuum closure → thermodynamic relation provider → consistency record`.

The executable consistency boundary is `evaluate_thermodynamic_consistency` in `src/tr_eif/multiscale/thermodynamic_consistency.py`. Mathematical relations and provider calculations are identified separately in each evaluation context.

## 2. Thermodynamic State and Observable Identity

Let a source state at scale `l` be `X_l` and a target state at scale `m` be `X_m`. A selected thermodynamic observable `a` is represented with its value, physical unit, state domain, scale, and provenance.

A cross-scale relation takes the general form:

`R_a(a_source, a_target; model, assumptions, normalization) = 0`.

A calculation can report a residual, uncertainty, comparison interval, and a Boolean outcome produced by the selected evaluator. The relation identifier determines the exact mathematical operation, while the model and state-domain identifiers determine the corresponding physical and computational conditions.

Temperature, pressure, composition, density, internal energy, enthalpy, entropy, chemical potential, and transport coefficients retain their individually declared definitions and units.

## 3. Executable Thermodynamic Variable

`ThermodynamicVariable` is an immutable dataclass with the following fields:

| Field | Executable meaning |
| --- | --- |
| `variable_id` | Nonempty normalized quantity identifier |
| `value` | Finite real number stored as `float` |
| `unit` | Nonempty normalized unit identifier |
| `scale_id` | Nonempty normalized scale identifier |
| `state_domain_id` | Nonempty normalized state-domain identifier |
| `source_id` | Nonempty normalized provenance identifier |

Identifiers are stripped of surrounding whitespace. The numerical value accepts finite integer or floating-point input, excluding Boolean input, and retains its sign as supplied.

A `ThermodynamicVariables` collection is a nonempty tuple of these records. Its canonical identity key is:

`key(v) = (v.scale_id, v.variable_id)`.

The executable collection contract requires unique keys and ascending key order. Units, domain identifiers, and source identifiers remain explicit fields of every entry.

## 4. Consistency Context

`ThermodynamicConsistencyContext` contains four normalized, nonempty identifiers:

- `relation_id`: the selected thermodynamic comparison or identity;
- `model_id`: the selected constitutive or thermodynamic model;
- `assumptions_id`: the state-domain, ensemble, and applicability specification;
- `normalization_id`: the unit, reference-state, and residual normalization convention.

A reproducibility manifest resolves these identifiers to concrete mathematical equations, numerical parameters, applicable thermodynamic states, unit transformations, and acceptance criteria defined before evaluation.

The context is supplied in full to the evaluator and retained in its output record.

## 5. Consistency Record

`ThermodynamicConsistencyRecord` contains:

- `source_variables`: canonical source collection;
- `target_variables`: canonical target collection;
- `context`: the full consistency context;
- `is_consistent`: Boolean result supplied by the evaluator;
- `validation_id`: nonempty normalized result identifier.

The record validates the types, cardinalities, canonical ordering, and unique identities of its source and target collections. The `is_consistent` field accepts exactly a Boolean value. Its meaning is determined by the declared relation and evaluator criterion; balanced-ternary execution values are held in their own execution records.

The record preserves both collections with their original scale, domain, unit, and provenance identities.

## 6. Provider Evaluation Contract

The public interface is:

`evaluate_thermodynamic_consistency(source_variables, target_variables, context, evaluator)`.

The `ThermodynamicConsistencyEvaluator` receives the two validated variable tuples and the full `ThermodynamicConsistencyContext`. It returns one `ThermodynamicConsistencyRecord`.

The evaluation boundary performs these operations:

1. Validate both variable collections and their canonical ordering.
2. Validate the context type and evaluator callability.
3. Invoke the evaluator with source collection, target collection, and context.
4. Validate the returned record type.
5. Require returned source variables to equal the supplied source tuple.
6. Require returned target variables to equal the supplied target tuple.
7. Require returned context to equal the supplied context.
8. Return the provider's result and validation identifier.

The provider supplies the thermodynamic relation, any unit conversion, state matching, equation of state, numerical method, tolerance, and criterion used to construct its Boolean result.

## 7. Extensive and Intensive Quantities

The source and target mapping identifies the normalization of each thermodynamic quantity. For a control region with volume `V > 0` and mass `M > 0`, examples are:

`rho = M / V`.

`u = U / M`.

`e_V = U / V`.

Here `rho` is mass density, `U` is internal energy, `u` is specific internal energy, and `e_V` is internal-energy density. Their numerical values depend on the declared physical state and storage convention.

Extensive variables such as total mass, volume, internal energy, and species amounts are mapped with the selected system boundary and additive accounting. Intensive variables such as temperature, pressure, and chemical potential use explicitly identified state and averaging procedures.

## 8. Equilibrium Fundamental Relation

For a simple compressible multicomponent equilibrium system with internal energy `U`, entropy `S`, volume `V`, and species amounts `N_s`, one fundamental differential relation is:

`dU = T dS - P dV + sum_s mu_s dN_s`.

`T`, `P`, and `mu_s` are respectively thermodynamic temperature, pressure, and species chemical potentials in the chosen thermodynamic convention. The relation holds in the specified equilibrium state domain with consistent definitions of the independent variables.

The corresponding partial derivatives are:

`T = (partial U / partial S)_(V,N)`.

`P = -(partial U / partial V)_(S,N)`.

`mu_s = (partial U / partial N_s)_(S,V,N_others)`.

A cross-scale evaluator may use these derivative relations to compare the thermodynamic representation at two selected levels.

## 9. Thermodynamic Potentials

For the equilibrium state domain of Section 8, define enthalpy `H`, Helmholtz free energy `F`, and Gibbs free energy `G`:

`H = U + P V`.

`F = U - T S`.

`G = U + P V - T S`.

Their differential forms are:

`dH = T dS + V dP + sum_s mu_s dN_s`.

`dF = -S dT - P dV + sum_s mu_s dN_s`.

`dG = -S dT + V dP + sum_s mu_s dN_s`.

The electronic/interatomic potential energy, total mechanical energy, and equilibrium thermodynamic potentials are associated with their own definitions, state constraints, and transformations. A mapping between them states the statistical-mechanical ensemble, reference-energy convention, and thermodynamic limit or finite-system convention used.

## 10. Derivative and Maxwell Relations

From a twice continuously differentiable Helmholtz free energy `F(T,V,N)` at fixed composition:

`S = -(partial F / partial T)_(V,N)`.

`P = -(partial F / partial V)_(T,N)`.

Equality of mixed derivatives yields:

`(partial S / partial V)_(T,N) = (partial P / partial T)_(V,N)`.

From a twice continuously differentiable Gibbs free energy `G(T,P,N)`:

`(partial S / partial P)_(T,N) = -(partial V / partial T)_(P,N)`.

A numerical consistency evaluation specifies the differentiable state interval, derivative step or analytic derivative operator, state held fixed, and tolerance selected for the mixed-derivative comparison.

## 11. Response Coefficients and State Domain

Thermodynamic response coefficients can be defined on a selected equilibrium branch:

`C_V = (partial U / partial T)_(V,N)`.

`C_P = (partial H / partial T)_(P,N)`.

`kappa_T = -(1/V) (partial V / partial P)_(T,N)`.

`alpha_P = (1/V) (partial V / partial T)_(P,N)`.

These relations associate heat capacity, isothermal compressibility, and volumetric thermal expansion with the specified independent variables.

A response-coefficient transfer records whether quantities are total, molar, specific-mass, or volumetric and identifies the source state, composition, temperature, pressure, and derivative procedure. For locally stable equilibrium branches, the selected stability conditions enter the relation assumptions and response-coefficient checks.

## 12. Multicomponent Thermodynamic Identities

For a homogeneous extensive equilibrium system under its Euler homogeneity assumptions:

`U = T S - P V + sum_s mu_s N_s`.

Differentiating this relation together with the fundamental differential gives the Gibbs–Duhem relation:

`S dT - V dP + sum_s N_s dmu_s = 0`.

A multicomponent provider identifies species, independent composition coordinates, amount units, and any constraint linking their mole fractions. It can compare chemical-potential variations with the selected Gibbs–Duhem relation at the declared state.

For a mixture with mole fractions `x_s`, the composition relation is:

`sum_s x_s = 1`.

Composition averaging and conversion retain their declared species inventory and normalization.

## 13. Statistical-Mechanical Connection to Atomistic Dynamics

For an equilibrium canonical ensemble with partition function `Z(N,V,T)` and Boltzmann constant `k_B`:

`F = -k_B T ln Z`.

With inverse temperature `beta_T = 1 / (k_B T)`, the associated canonical mean energy relation is:

`<H_micro> = -partial ln Z / partial beta_T`.

`H_micro` denotes the selected microscopic Hamiltonian, including the terms defined by the atomistic model and boundary convention. The mapping from molecular-dynamics observables to equilibrium thermodynamic quantities declares its sampling ensemble, sampling interval, ergodic assumptions where used, and finite-size treatment.

The atomistic TR-EIP energy model supplies a conditioned potential-energy operator, while kinetic energy and thermal coupling are evaluated through the MD interfaces. The equilibrium ensemble and macroscopic thermodynamic mapping are selected by the material realization.

## 14. Open-System Mass and Species Balances

For a fixed control region `Omega` and an identified total mass density `rho`, material velocity `u`, and mass-source field `s_m`:

`partial_t rho + div(rho u) = s_m`.

For species `s` with mass concentration `c_s`, diffusive flux `j_s` relative to `u`, and volumetric production rate `q_s`:

`partial_t c_s + div(c_s u + j_s) = q_s`.

The region, outward boundary-normal convention, species source definitions, and boundary fluxes specify the corresponding integrated balances. Cross-scale transfer records the spatial averaging rule and any exchanges across the selected scale boundary.

## 15. Open-System Energy Balance

For total energy density `e_total,V` and a declared total energy flux `J_E`, the general control-volume form is:

`partial_t e_total,V + div(J_E) = s_E`.

For a fixed region with outward unit normal `n`, integration gives:

`d/dt integral_Omega e_total,V dV = -integral_(partial Omega) J_E · n dA + integral_Omega s_E dV`.

The selected energy density includes its explicitly defined internal, kinetic, and other stored contributions. The flux comprises the declared convective, conductive, mechanical, and species-carried terms; the source contains the declared external work, reaction, or volumetric exchange contributions.

A scale-transfer calculation compares integrated source and target balances using consistent stored-energy, flux, reference-state, and sign conventions.

## 16. Entropy Balance and Dissipation

For specific entropy `s`, mass density `rho`, nonconvective entropy flux `J_s`, external entropy supply `s_s,ext`, and internal entropy-production density `sigma_s`, an entropy balance is:

`partial_t(rho s) + div(rho s u + J_s) = s_s,ext + sigma_s`.

For a continuum model satisfying the local second-law condition:

`sigma_s >= 0`.

For a Fourier heat-flux branch `q = -k grad(T)` with `T > 0` and `k >= 0`, the associated conduction contribution is:

`sigma_s,heat = q · grad(1/T) = k |grad(T)|^2 / T^2`.

For Newtonian viscous stress `tau = 2 eta D_dev + zeta (div u) I`, with `eta >= 0` and `zeta >= 0`:

`sigma_s,visc = (tau : D) / T = [2 eta (D_dev : D_dev) + zeta (div u)^2] / T`.

The constitutive law, entropy-flux convention, species diffusion contributions, temperature domain, and boundary supply determine the complete entropy-production calculation.

## 17. Atomistic Thermostat and Barostat Coupling

The MD kinetic-energy operator evaluates:

`K = (1/2) sum_i m_i |v_i|^2`.

For a declared translational degree-of-freedom count `f` and consistent `k_B`, the reference kinetic-temperature estimator is:

`T_kin = 2 K / (f k_B)`.

The velocity-rescaling thermostat applies a selected target kinetic temperature to the mechanical velocity tuple and records the corresponding change in kinetic energy. Its control input and event time are explicitly supplied.

The isotropic barostat scales a fully periodic three-dimensional cell and Cartesian positions using its declared current/target pressures, compressibility, timestep, and coupling time. For a positive volume ratio `mu_V`:

`V_after = mu_V V_before`.

Cell work, thermal exchange, and changes in conditioned potential energy are included according to the selected mechanical/thermal event schedule. The thermodynamic consistency provider receives the resulting observables through explicitly constructed source and target variable collections.

## 18. Spatial Stress and Pressure Relations

`ConservativeStressEvaluator` computes a Cartesian stress tensor from homogeneous cell-strain derivatives of the selected scalar interatomic energy. The operator's strain sign convention, reference volume, energy graph, features, and execution vector are retained in its calculation context.

For an isotropic hydrostatic stress under the convention `sigma = -P I`, the pressure is:

`P = -trace(sigma) / 3`.

A source-to-target pressure relation declares whether the source variable is a mechanical virial pressure, hydrostatic stress-derived pressure, external barostat pressure, or thermodynamic equation-of-state pressure. Units and finite-system normalization are matched through the selected model context.

Under a common spatial orthogonal transformation `Q`, stress transforms as `sigma' = Q sigma Q^T`, while the scalar trace and hydrostatic pressure follow the corresponding invariant relation.

## 19. Cross-Scale Balance Residuals

For a specified source observable vector `a_source` and target observable vector `a_target`, let `M` denote the declared conversion or coarse-graining map. Define the comparison residual:

`r_a = a_target - M(a_source; context)`.

A normalization scale `a_scale > 0` yields a dimensionless residual where applicable:

`r_a,normalized = r_a / a_scale`.

For integrated mass or energy balances, the comparison may instead use the difference between the source and target conserved inventories and their accounted boundary fluxes over a declared interval.

The evaluator's decision function and its fixed numerical criteria are associated with `relation_id`, `assumptions_id`, and `normalization_id`. The output record stores the original source and target variables with the provider's Boolean result and validation identifier.

## 20. Uncertainty and Numerical Tolerances

The uncertainty-transfer layer provides `UncertaintyMeasure`, `UncertaintyPropagationContext`, and `evaluate_uncertainty_propagation` for named source and target quantities across scales.

Thermodynamic comparisons distinguish measured or source-provided uncertainty, numerical derivative error, temporal/spatial discretization error, parameter uncertainty, and chosen acceptance tolerances by their identifiers and procedures.

For a differentiable mapping `y = f(x)` with source covariance matrix `C_x`, a first-order covariance estimate is:

`C_y ≈ J C_x J^T`.

`J` is the Jacobian of the declared state map. The correlation model, source units, representation, and numerical method enter the uncertainty context. Exact collection ordering and identifier relations are checked categorically; numerical thermodynamic relations use their predeclared tolerances.

## 21. FLiBe Material-State Correspondence

The FLiBe domain module `FLiBeThermodynamicState` stores absolute temperature and pressure. Its executable contract requires finite positive temperature and finite nonnegative pressure.

The repository registers primary-source experimental density measurements in `data/reference/flibe_vidrio_2022_density_measurements.json` and published AIMD density values in `data/reference/flibe_baral_2021_aimd_density.json`.

The experimental record includes specimen composition and reported measurement uncertainties. The AIMD record includes its simulation composition, temperature labels, cell metadata, and computed densities. A thermodynamic source-to-target map identifies each source state by composition, pressure, temperature, phase or structural conditions where supplied, observable definition, and unit convention.

The exact formula-unit ratio `2 LiF : 1 BeF2`, nominal `67 mol% LiF : 33 mol% BeF2`, and measured specimen composition are represented by their respective source definitions. A material-specific evaluator supplies the mathematical relation and mapping between the selected state domains.

## 22. Executable Numerical Fixture

The existing integration test `tests/integration/test_multiscale_thermodynamic_consistency.py` constructs two source variables at scale `atomistic`:

`energy_density = 5.0 J/m^3`.

`pressure = 2.0 Pa`.

It constructs two target variables at scale `continuum` with the same numerical values and units. The source uses `state_domain_id = "state-a"` and `source_id = "source-a"`; the target uses `state_domain_id = "state-b"` and `source_id = "source-b"`.

The fixture context uses `relation_id = "relation-a"`, `model_id = "model-a"`, `assumptions_id = "assumptions-a"`, and `normalization_id = "normalization-a"`. Its supplied evaluator creates a `ThermodynamicConsistencyRecord` with `is_consistent = True` and `validation_id = "validation-a"`.

The test verifies record typing, provider input binding, canonical ordering, source and target identity, explicit Boolean status, and deterministic evaluation.

## 23. Exact Invariants and Numerical Qualification

The executable structural contract includes:

- finite, non-Boolean thermodynamic numerical values, including signed values;
- normalized nonempty variable, unit, scale, state-domain, and source identifiers;
- nonempty source and target tuples of `ThermodynamicVariable`;
- unique `(scale_id, variable_id)` keys within each tuple;
- canonical ascending key order for both variable collections;
- a `ThermodynamicConsistencyContext` with four normalized nonempty identifiers;
- an explicitly Boolean `is_consistent` field and a normalized nonempty `validation_id`;
- provider-returned source, target, and context values equal to the supplied inputs;
- deterministic records for identical inputs and a deterministic provider.

A material-specific numerical qualification additionally declares its state domain, equations of state, equilibrium or nonequilibrium conditions, derivative methods, conservation residuals, entropy production, uncertainty representation, and fixed numerical acceptance criteria.

## 24. Reproducibility Record

A reproducible thermodynamic consistency evaluation specifies:

- ordered source and target variable tuples, with values, units, scales, domains, and sources;
- reference state and material composition, temperature, pressure, and other declared state variables;
- `relation_id`, `model_id`, `assumptions_id`, and `normalization_id` with resolved mathematical definitions;
- mapping coefficients, state normalization, unit conversions, and reference-zero choices;
- source and target sampling times, spatial supports, coarse-graining partitions, and boundary histories;
- balance-law terms, flux orientations, constitutive equations, and reservoir exchange conventions;
- integration/derivative parameters, numerical precision, and tolerance policy;
- uncertainty representations, correlations, and propagation procedure;
- continuous resonance and ternary execution event indices when the thermodynamic observable is conditioned by those operators;
- provider identity, `validation_id`, the Boolean result, and the associated numerical observables.

These fields connect the returned typed record to its source data and to the complete mathematical and computational evaluation context.

## 25. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| Thermodynamic variable, context, record, and evaluator | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Multiscale namespace exports | `src/tr_eif/multiscale/__init__.py` |
| Atomistic mechanical energy observables | `src/tr_eif/md/observables.py` |
| Mechanical trajectory and energy sampling | `src/tr_eif/md/trajectory_observables.py` |
| Kinetic temperature and thermostat | `src/tr_eif/md/thermostat.py` |
| Isotropic barostat | `src/tr_eif/md/barostat.py` |
| Cell-strain stress derivative | `src/tr_eif/energy/stress_evaluator.py` |
| Electronic-reference observables | `src/tr_eif/multiscale/electronic_reference.py` |
| Mesoscale closure | `src/tr_eif/multiscale/mesoscale_closure.py` |
| Continuum closure | `src/tr_eif/multiscale/continuum_closure.py` |
| Transport coefficient transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| FLiBe thermodynamic state | `src/tr_eif/flibe/thermodynamic_state.py` |
| FLiBe density model | `src/tr_eif/flibe/density.py` |
| Continuous resonance evolution | `src/tr_eif/md/resonance_propagation.py` |
| Balanced-ternary execution | `src/tr_eif/md/ternary_propagation.py` |
| Thermodynamic consistency integration tests | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Multiscale cross-boundary tests | `tests/integration/test_multiscale_cross_scale_validation.py` |
| FLiBe thermodynamic state invariants | `tests/invariants/test_flibe_thermodynamic_state_invariants.py` |
| Stress consistency tests | `tests/conservation/test_stress_consistency.py` |

## 26. Chapter Integration

Thermodynamic consistency in TR-EIF couples named physical observables to their scale, state domain, units, and provenance. The executable boundary preserves the supplied source and target collections and the selected relation/model context in one typed evaluation record.

The mathematical layer supplies equilibrium identities, open-system mass/energy/entropy balances, constitutive derivatives, and cross-scale residual definitions for the selected physical domains. Mechanical, resonance, active `-1/0/1` execution, uncertainty, transport, and continuum interfaces participate through the declared mapping and event schedule.
