
# Thermodynamic Properties

## 1. Scope and Material System

This chapter defines thermodynamic state coordinates, constitutive property relations, source-data representation, and thermodynamic balances for the LiF–BeF2 reference material within TR-EIF.

The material representation combines a declared composition, absolute temperature, pressure, three-dimensional atomic geometry, material-state region, and boundary exchange. Interatomic energy, mechanical motion, continuous resonance, and balanced-ternary `-1/0/1` execution retain their separately typed states and computational operators.

The property calculation chain is:

`composition and physical state → source or constitutive model → typed property → state-specific calculation → observable record → multiscale mapping`.

The executable FLiBe thermodynamic and density interfaces are defined in `src/tr_eif/flibe/thermodynamic_state.py`, `src/tr_eif/flibe/density.py`, and `src/tr_eif/flibe/units.py`.

## 2. Composition Coordinates

Let `n_LiF` and `n_BeF2` denote nonnegative LiF and BeF2 formula-unit amounts with positive total. The binary composition coordinates are:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

`x_LiF + x_BeF2 = 1`.

For the exact formula-unit ratio `2 LiF : 1 BeF2`, the coordinates are `x_LiF = 2/3` and `x_BeF2 = 1/3`. The nominal `67 mol% LiF : 33 mol% BeF2` composition uses `0.67` and `0.33` as its reported decimal fractions. The Vidrio 2022 specimen record reports `33.58(5) mol% BeF2` from ICP-MS.

`FLiBeComposition` stores normalized component fractions. Property records carry the source composition and its basis, precision, and applicable temperature–pressure domain.

## 3. Executable Thermodynamic State

`FLiBeThermodynamicState` is an immutable record containing:

| Field | Unit | Executable domain |
| --- | --- | --- |
| `temperature` | `K` | Finite real, strictly positive |
| `pressure` | `Pa` | Finite real, nonnegative |

The constructor accepts integer or floating-point values, excludes Boolean values, and stores normalized floats. The methods `with_temperature` and `with_pressure` construct new records while retaining the coordinate not selected for replacement.

A full material-state specification additionally associates this pair with the component composition, material phase or structural regime, boundary conditions, and the selected source or constitutive model.

## 4. Physical Parameter and Unit Contract

`FLiBeUnit` defines the current typed parameter units `K`, `Pa`, `u`, and `kg/m^3`. `PhysicalParameter` associates a finite numerical value with one of these units, a `ParameterProvenance` member, and optional source metadata under the class-specific source contract.

The executable helpers `temperature_parameter`, `pressure_parameter`, `atomic_mass_parameter`, and `density_parameter` construct typed parameter values. Property-specific validators apply the corresponding physical-domain conditions.

A thermodynamic quantity expressed in another unit is converted using its identified conversion rule before entering a typed interface. Source-provided units, converted units, and uncertainty units remain recorded with the numerical value.

## 5. Density-Model Interface

`FLiBeDensityModel(evaluator, provenance, source)` accepts a callable of signature:

`evaluator: FLiBeThermodynamicState → density_kg_m3`.

Its `evaluate(state)` method returns a `PhysicalParameter` with strictly positive finite density and unit `kg/m^3`. `ConstantFLiBeDensity` provides a state-typed constant-density evaluator with the same output unit and provenance fields.

`evaluate_density(model, state)` dispatches to either supported model type and returns the density parameter. The supplied evaluator receives temperature and pressure through `FLiBeThermodynamicState`. Composition and other constitutive parameters are bound by the evaluator configuration or its associated model manifest.

## 6. Mass, Volume, and Density

For a specified atomic inventory with masses `m_i` and physical volume `V > 0`:

`M_total = sum_i m_i`.

`rho = M_total / V`.

For a periodic cell with matrix `B = [a b c]` and nonzero determinant:

`V_cell = |det(B)|`.

`rho_cell = M_total / V_cell`.

`FLiBeMassParameters`, `configuration_masses`, and `total_configuration_mass` provide species-mass assignment and mass aggregation. Cell-derived density also identifies the mass and length units of the configuration, including conversion from the atomic mass unit and the simulation-cell length unit to SI when reporting `kg/m^3`.

The thermodynamic density-provider and cell-density calculations have distinct input records and can be compared at a declared composition and material state.

## 7. Registered Temperature-Dependent Density Correlation

The FLiBe reference register identifies the Janz et al. (1974) compilation under `FLIBE-REFERENCE-JANZ-1974-DENSITY`. It registers the following attributed linear correlation, reproduced in a later thermophysical assessment:

`rho_ref(T) = 2413 - 0.488 T`.

The registered conditions are:

| Quantity | Registered specification |
| --- | --- |
| Density unit | `kg/m^3` |
| Temperature unit | `K` |
| LiF component fraction | `67 mol%` |
| BeF2 component fraction | `33 mol%` |
| Temperature interval | `800–1080 K` |
| Correlation source ID | `FLIBE-REFERENCE-JANZ-1974-DENSITY` |

The executable calculation is in `benchmarks/flibe/reference_property_reproduction.py`. The benchmark uses a `FLiBeDensityModel` with `ParameterProvenance.DERIVED`, the registered source identifier, a declared reference composition, and an explicit temperature-domain check.

## 8. Density Correlation Example at 900 K

For the registered `67:33` correlation at `T = 900 K`:

`rho_ref(900 K) = 2413 - 0.488 × 900 = 1973.8 kg/m^3`.

The corresponding specific volume is:

`v_ref = 1/rho_ref = 0.000506636943965954 m^3/kg`.

The temperature derivative of the registered correlation is:

`d rho_ref/dT = -0.488 kg/(m^3 K)`.

The benchmark registers seven source-derived reference points at 800, 850, 900, 950, 1000, 1050, and 1080 K. It retains the calculated density, corresponding reference value, residual, source identity, and unit metadata for each point.

## 9. Thermal Expansion from Density

For a fixed mass inventory and a differentiable isobaric density relation, define the volumetric thermal-expansion coefficient:

`alpha_P = (1/V) (partial V/partial T)_(P,n)`.

Using `rho = M/V` at fixed `M`:

`alpha_P = -(1/rho) (partial rho/partial T)_(P,n)`.

For the registered linear density correlation, its derivative-based coefficient is:

`alpha_ref(T) = 0.488 / (2413 - 0.488 T)`.

At `900 K` this gives:

`alpha_ref(900 K) = 0.000247238828655386 K^(-1)`.

This derivative calculation uses the registered composition and temperature interval under an explicitly selected fixed-pressure interpretation of the temperature-only density relation. A source record links the derived coefficient to the parent correlation and differentiation method.

## 10. Experimental Density Record: Vidrio 2022

The dataset `data/reference/flibe_vidrio_2022_density_measurements.json` registers density measurements from Vidrio et al., *Journal of Chemical & Engineering Data* (2022), DOI `10.1021/acs.jced.2c00212`.

The recorded table contains 61 measurements in runs `0A`, `1A`, `1B`, and `1C`. Each row contains:

`(temperature_c, temperature_standard_uncertainty_c, density_kg_m3, density_standard_uncertainty_kg_m3)`.

The material record includes a nominal `2 LiF : 1 BeF2` component ratio, measured `33.58(5) mol% BeF2`, measurement pressure `102 kPa` with reported standard uncertainty `1 kPa`, and measurement temperatures from `447` to `817 °C`. The source reports a melting-temperature value of `459.1 °C` with standard uncertainty `0.2 °C`.

The density measurement method is hydrostatic buoyancy. The original Celsius values can be mapped to kelvin by `T_K = T_C + 273.15`, preserving the temperature uncertainty interval in kelvin increments.

## 11. First-Principles Structural Density: Baral 2021

The dataset `data/reference/flibe_baral_2021_aimd_density.json` registers nine temperature-labeled rows from Baral et al., *ACS Omega* (2021), DOI `10.1021/acsomega.1c02528`.

Each row contains:

`(temperature_k, cubic_cell_edge_angstrom, cell_volume_angstrom3, simulated_density_g_cm3)`.

The source material is described by `Li2BeF4`, with the exact formula-unit ratio `2 LiF : 1 BeF2`, and the source metadata identify a 504-atom simulation supercell.

For the registered 750 K row:

`rho_AIMD(750 K) = 1.757 g/cm^3 = 1757 kg/m^3`.

The recorded cell edge and volume for that row are `18.915 angstrom` and `6767.367 angstrom^3`. The structural density is associated with the specified supercell and first-principles calculation record.

## 12. Thermodynamic Data Correspondence

A source-to-model thermodynamic comparison identifies the tuple:

`C_state = (composition, temperature, pressure, physical_state, observable, unit, normalization)`.

The reference representation additionally records source identifier, numerical or experimental method, available uncertainty, sampling axis, and data transformation.

`FLiBeReferenceObservable` stores this material correspondence for experimental and first-principles observable vectors. `compare_flibe_experimental_first_principles` calculates signed and absolute residuals and aggregate error metrics for records satisfying its exact correspondence contract.

The existing source-based density scripts in `benchmarks/flibe/` supply explicit temperature-domain selection, source-table lookup, and interpolation records for their defined comparisons.

## 13. Enthalpy and Heat Capacity

For a selected equilibrium branch, define enthalpy:

`H = U + P V`.

At fixed pressure and composition, the heat capacity is:

`C_P = (partial H/partial T)_(P,n)`.

At fixed volume and composition:

`C_V = (partial U/partial T)_(V,n)`.

Specific-mass heat capacities are obtained by dividing the appropriate extensive heat capacity by the declared sample mass. Molar heat capacities use the corresponding amount basis.

`docs/references/flibe_sources.md` registers Douglas and Payne (1969), DOI `10.6028/jres.073A.037`, for measured enthalpy and source-derived thermodynamic properties of solid and liquid `Li2BeF4` over the reported 273–900 K domain. It also registers Redkin et al. (2021), DOI `10.1016/j.molliq.2021.117215`, for density and heat-capacity measurements at the compositions studied in the LiF–BeF2–UF4 system.

## 14. Enthalpy Differences and Heat-Capacity Integration

For two temperatures `T_a` and `T_b` on one differentiable branch at fixed pressure and composition:

`H(T_b) - H(T_a) = integral_(T_a→T_b) C_P(T) dT`.

With a declared constant specific heat capacity `c_p` in a specified interval, the specific-enthalpy increment is:

`h(T_b) - h(T_a) = c_p (T_b - T_a)`.

Numerical integration uses the source's reported temperature and phase domain, enthalpy reference, units, and uncertainty metadata. When a thermodynamic path crosses a phase boundary, phase-specific branches and their associated transition enthalpy are represented in the selected path integral and state sequence.

## 15. Free Energies and Chemical Potentials

For the selected equilibrium thermodynamic description, define Helmholtz and Gibbs free energies:

`F = U - T S`.

`G = U + P V - T S`.

For a simple compressible multicomponent equilibrium state:

`dG = -S dT + V dP + sum_s mu_s dN_s`.

The chemical potential of component `s` is:

`mu_s = (partial G/partial N_s)_(T,P,N_others)`.

The component basis (LiF and BeF2 formula units, or a separately identified chemical-species representation) is declared for each chemical-potential calculation. A source or model supplies the free-energy functional, reference states, mixing terms, and constitutive parameters used by that calculation.

## 16. Mixing and Partial Molar Properties

For a two-component equilibrium mixture with component mole fractions `x_s`, molar Gibbs energy may be decomposed using a selected ideal reference:

`g_mix = R_gas T sum_s x_s ln(x_s) + g_excess`.

The endpoint convention uses the limiting value `x ln(x) → 0` as `x → 0`. `g_excess` is the specified nonideal mixing contribution in that reference convention.

For any extensive property `Y` of the mixture, its partial molar component property is:

`Ybar_s = (partial Y/partial N_s)_(T,P,N_others)`.

The source model declares its component identity, composition domain, standard state, and differentiability conditions. Material-specific structure, association, and correlations enter the corresponding chosen constitutive representation.

## 17. Phase-Equilibrium Relations

A phase-region record identifies composition, temperature, pressure, material phases present, and the corresponding phase-equilibrium source. For coexisting equilibrium phases `alpha` and `beta`, the chemical-potential condition for transferable component `s` is:

`mu_s^alpha(T,P,x^alpha) = mu_s^beta(T,P,x^beta)`.

For a one-component phase boundary with the corresponding coexistence assumptions, the Clapeyron relation is:

`dP/dT = Delta_S / Delta_V`.

The FLiBe register contains phase-diagram sources Roy, Roy, and Osborn (1950, 1954) and liquidus measurements by Romberger, Braunstein, and Thoma (1972). The chosen invariant-point composition and associated liquidus or solidus data are represented by their experimentally reported composition and thermodynamic coordinates.

## 18. Compressibility and Pressure Dependence

For a selected differentiable thermodynamic state branch, the isothermal compressibility is:

`kappa_T = -(1/V) (partial V/partial P)_(T,n)`.

For fixed mass, an equivalent density derivative is:

`kappa_T = (1/rho) (partial rho/partial P)_(T,n)`.

The corresponding isobaric expansion coefficient is:

`alpha_P = -(1/rho) (partial rho/partial T)_(P,n)`.

An equation of state `rho = rho(T,P,x)` supplies these derivatives at the declared composition, temperature, pressure, and material state. The pressure-dependence parameterization is identified separately from a temperature-only density correlation.

## 19. Pressure Coupling and Three-Dimensional Cell Volume

`src/tr_eif/md/barostat.py` provides an isotropic pressure-coupling operator for fully periodic three-dimensional configurations. With current and target pressures, positive compressibility `beta`, positive step `dt`, and coupling time `tau_p`, the volume factor is:

`mu_V = 1 - (dt/tau_p) beta (P_target - P_current)`.

For `mu_V > 0`:

`scale_linear = mu_V^(1/3)`.

`B_after = scale_linear B_before`.

`r_i,after = scale_linear r_i,before`.

`V_after = mu_V V_before`.

The barostat retains atom masses, velocities, mechanical step, and mechanical time during this geometry transformation. Pressure estimation, compressibility provenance, state dependence, and the schedule for force and graph updates are supplied by the selected calculation.

## 20. Mechanical and Thermal Energy Accounting

For atomwise positive masses `m_i` and velocities `v_i`, kinetic energy is:

`K = (1/2) sum_i m_i |v_i|^2`.

For a conditioned interatomic potential `E_pot`:

`H_mech = K + E_pot`.

`kinetic_energy` and `molecular_dynamics_energy` in `src/tr_eif/md/observables.py` construct ordered atomic and total energy records.

For a declared translational degree-of-freedom count `f` and consistent Boltzmann constant `k_B`, the kinetic-temperature estimator is:

`T_kin = 2K / (f k_B)`.

`velocity_rescaling_factor` defines `lambda_T = sqrt(T_target/T_current)` for positive `T_current`, and the thermostat updates `v_i,after = lambda_T v_i,before`. Its kinetic-energy increment is `Delta_K = (lambda_T^2 - 1) K_before`. Exchange accounting registers that event with the selected reservoir convention and recorded mechanical state.

## 21. Open-System Thermodynamic Balances

For a physical control region `Omega` with mass density `rho`, material velocity `u`, and mass source `s_m`:

`partial_t rho + div(rho u) = s_m`.

For a total-energy density `e_total,V`, energy flux `J_E`, and energy source `s_E`:

`partial_t e_total,V + div(J_E) = s_E`.

For specific entropy `s`, nonconvective entropy flux `J_s`, external supply `s_s,ext`, and entropy-production density `sigma_s`:

`partial_t(rho s) + div(rho s u + J_s) = s_s,ext + sigma_s`.

A constitutive realization satisfying the local second-law condition has `sigma_s >= 0`. Each balance uses its declared boundary, stored quantities, flux orientations, volumetric source terms, and integration or sampling intervals.

## 22. Cross-Scale Thermodynamic Consistency

`ThermodynamicVariable` stores a finite numerical value with variable, unit, scale, state-domain, and source identifiers. `ThermodynamicConsistencyContext` stores the selected relation, model, assumptions, and normalization identifiers.

The executable call is:

`evaluate_thermodynamic_consistency(source_variables, target_variables, context, evaluator)`.

`ThermodynamicConsistencyRecord` retains the canonical source and target variable collections, context, provider-supplied Boolean result, and validation identifier.

A material-specific evaluator supplies its chosen thermodynamic relation, source-to-target state mapping, normalization, units, and numerical comparison criteria. The resulting record is associated with the corresponding atomistic, mesoscale, continuum, or engineering-scale variables.

## 23. Uncertainty and Thermophysical Data Processing

For a differentiable scalar property `y = f(x)` with source covariance `C_x` and Jacobian `J`, first-order uncertainty propagation is:

`C_y ≈ J C_x J^T`.

For a density-derived expansion coefficient, source density uncertainty and parameter uncertainty propagate through the chosen derivative and ratio mapping. Temperature uncertainty, sample composition, measurement covariance, and regression-parameter covariance are included when supplied by the selected source and method.

The executable `UncertaintyMeasure` and `evaluate_uncertainty_propagation` interfaces preserve the scale, representation, state-domain, method, and source identifiers in the uncertainty-transfer record. Measurement uncertainty, model-parameter uncertainty, and numerical comparison tolerance are stored as separately defined quantities.

## 24. Continuous Resonance and Executed Ternary Conditioning

The continuous atom-associated resonance layer evolves phases through its selected Kuramoto–Sakaguchi vector field:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A declared mapping may associate the continuous resonance state and material thermodynamic context with a descriptor and an execution request. The execution layer retains the canonical state alphabet `-1/0/1`, with active neutral `0`, pending destinations, execution guards, and separate committed transitions for opposite polarities:

`-1 → 0 → 1`.

`1 → 0 → -1`.

`FLiBeResonanceDescriptor` binds an atomic configuration, graph-relative coordination, resonance state, thermodynamic state, and provenance. `FLiBeTREIPModel` uses the supplied retained execution vector and resonance-augmented node features in the conditioned interatomic energy calculation.

## 25. Reference-Dataset and Model Qualification

A thermophysical calculation records its source observable, physical state, method, units, composition, independent sampling coordinates, and source-provided uncertainty. For an identified reference series and a model output evaluated on the corresponding coordinates, a residual is:

`delta_y,k = y_model,k - y_reference,k`.

For `N` residuals, define:

`MAE = (1/N) sum_k |delta_y,k|`.

`RMSE = sqrt((1/N) sum_k delta_y,k^2)`.

The comparison record associates these values with the chosen state-matching operation, interpolation or differentiation scheme, sampling interval, numerical tolerance, and uncertainty procedure. Repeated trajectory frames, independent experiments, source compilations, and first-principles outputs retain their individual source and sampling identifiers.

## 26. Exact Invariants and Numerical Contracts

The applicable executable structural contracts include:

- `FLiBeThermodynamicState.temperature` is finite and strictly positive;
- `FLiBeThermodynamicState.pressure` is finite and nonnegative;
- `FLiBeDensityModel` accepts a callable and typed provenance, returning a strictly positive density in `kg/m^3`;
- the constant-density evaluator returns its specified density at a typed input state;
- the binary formula-unit composition has two nonnegative components with positive total and normalized sum;
- atomic inventory, masses, cell geometry, and property source identities remain linked to the sampled material state;
- the target/source mapping and provider return have their declared type and identity correspondence;
- categorical execution states, pending targets, and committed transitions use the exact `-1/0/1` contract.

Numerical qualification declares units, source-state constraints, derivative or quadrature method, physical sampling coordinates, uncertainty representation, and fixed floating-point tolerances for the selected calculation.

## 27. Reproducibility Record

A thermophysical-property computation retains:

- source identifier, property name, source method, and provenance;
- component formula-unit basis, material composition, atomic inventory, and material state;
- temperature, pressure, phase-region information, physical units, and supported state domain;
- experimental sampling series and uncertainty definitions or computational reference data;
- selected property evaluator, constitutive parameters, and numerical method;
- reference density correlation and its registered composition and temperature range when used;
- derivatives, integration intervals, covariance inputs, and normalization;
- mechanical masses, cell volume, energy observables, and thermal/pressure event history when coupled to MD;
- resonance phase parameters and executed ternary conditioning states when included;
- cross-scale transfer context, numerical comparison data, and deterministic output record.

## 28. Executable Interface Index

| Role | Repository path |
| --- | --- |
| FLiBe thermodynamic state | `src/tr_eif/flibe/thermodynamic_state.py` |
| FLiBe density evaluators | `src/tr_eif/flibe/density.py` |
| Units and parameter provenance | `src/tr_eif/flibe/units.py` |
| Composition and species inventory | `src/tr_eif/flibe/composition.py`, `src/tr_eif/flibe/configuration.py` |
| Species masses | `src/tr_eif/flibe/mass.py` |
| Reference observable comparison | `src/tr_eif/flibe/reference_comparison.py` |
| Experimental density measurements | `data/reference/flibe_vidrio_2022_density_measurements.json` |
| AIMD structural density | `data/reference/flibe_baral_2021_aimd_density.json` |
| Registered thermophysical sources | `docs/references/flibe_sources.md` |
| Density-correlation benchmark | `benchmarks/flibe/reference_property_reproduction.py` |
| Cross-source density comparison | `benchmarks/flibe/experimental_aimd_density_cross_source_diagnostic.py` |
| Atomistic kinetic and total energy | `src/tr_eif/md/observables.py` |
| Kinetic temperature and thermostat | `src/tr_eif/md/thermostat.py` |
| Isotropic pressure coupling | `src/tr_eif/md/barostat.py` |
| Energy-derived stress | `src/tr_eif/energy/stress_evaluator.py` |
| Thermodynamic consistency interface | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| FLiBe resonance descriptor | `src/tr_eif/flibe/resonance_descriptor.py` |
| FLiBe TR-EIP energy specialization | `src/tr_eif/flibe/tr_eip.py` |

## 29. Existing Test Interfaces

| Scope | Repository test path |
| --- | --- |
| Thermodynamic state validation | `tests/invariants/test_flibe_thermodynamic_state_invariants.py` |
| Typed parameter units | `tests/invariants/test_flibe_units_invariants.py` |
| Density-model validation | `tests/invariants/test_flibe_density_invariants.py` |
| Composition validation | `tests/invariants/test_flibe_composition_invariants.py` |
| Species mass validation | `tests/invariants/test_flibe_mass_invariants.py` |
| Janz density benchmark qualification | `tests/numerical/test_flibe_reference_property_reproduction_benchmark.py` |
| Vidrio source-table integrity | `tests/integration/test_flibe_vidrio_2022_density_dataset.py` |
| Experimental–AIMD comparison | `tests/integration/test_flibe_experimental_aimd_density_cross_source_diagnostic.py` |
| Thermostat integration | `tests/integration/test_molecular_dynamics_thermostat.py` |
| Barostat integration | `tests/integration/test_molecular_dynamics_barostat.py` |
| Mechanical energy observations | `tests/conservation/test_md_energy_observables.py` |
| Thermodynamic consistency provider | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Cross-scale validation | `tests/integration/test_multiscale_cross_scale_validation.py` |

## 30. Chapter Integration

The FLiBe thermodynamic-property layer binds LiF–BeF2 composition, temperature, pressure, material-state definition, measured or calculated observables, units, and provenance to explicitly selected density and thermodynamic operators.

The framework associates those property records with atomistic mechanical and energy calculations, selected phase and constitutive relations, uncertainty transfer, and mesoscale-to-continuum mappings. Continuous resonance variables and active balanced-ternary execution retain their own state and event descriptions within the coupled calculation.
