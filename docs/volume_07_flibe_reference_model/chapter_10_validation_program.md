# Validation Program

## 1. Scope and System Class

This chapter establishes the mathematical, computational, and source-resolved validation program for the FLiBe reference realization within the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The program connects experimental observations, first-principles calculations, interatomic model outputs, molecular-dynamics trajectories, continuous resonance dynamics, balanced-ternary execution, and multiscale material representations through explicitly defined state correspondence and reproducible numerical procedures.

The principal qualification sequence is:

`mathematical contract → source and state registration → observable construction → numerical comparison → uncertainty accounting → independent qualification → reproducible result record`.

Every procedure identifies its input state, mathematical operator, output observable, units, source provenance, numerical method, and predeclared comparison criteria.

The represented material system is an open nonlinear dissipative dynamical system with three-dimensional atomic geometry, thermal and mechanical evolution, continuous resonance variables, categorical execution events, and explicitly defined material and energy exchanges.

## 2. Architectural Validation Levels

The architectural nesting is:

`TR-EIP ⊂ TR-EIF`.

The FLiBe realization belongs to the TR-EIP model family within TR-EIF.

Validation records are organized by the object undergoing examination:

| Level | Mathematical or computational object | Principal observables |
| --- | --- | --- |
| Framework | State spaces, operators, invariants, mappings | Mathematical relations and domain conditions |
| Resonance | Continuous oscillator dynamics and descriptors | Phase trajectories, frequencies, order parameters |
| Ternary execution | Retained, requested, pending, and committed states | Execution events and transition traces |
| Interatomic model | Conditioned scalar energy functional | Energy, forces, stress |
| Atomistic dynamics | Mechanical state and trajectories | Positions, velocities, energy, transport |
| FLiBe material | Composition and thermodynamic state | Density, structure, thermophysical properties |
| Multiscale | Fine-to-coarse mappings and closures | Mass, centroids, transported variables, fluxes |
| Numerical implementation | Executable operators and tests | Errors, convergence, determinism, resource use |

Each result retains the identity of its validation level and the dependencies used to construct it.

## 3. Evidence and Result Classes

The program distinguishes the following research records:

1. Mathematical definition or derived relation.
2. Mathematical invariant with stated assumptions.
3. Experimental observation.
4. First-principles computational result.
5. Interatomic-model output.
6. Numerical reference fixture.
7. Source-derived correlation.
8. Numerical comparison.
9. Executable qualification result.
10. Benchmark measurement.
11. Multiscale transformation result.

The executable `FLiBeEvidenceKind` enumeration currently represents `EXPERIMENTAL` and `FIRST_PRINCIPLES` for the typed experimental–first-principles comparison interface.

Other records retain their respective model, benchmark, or provenance identities in the relevant interfaces.

A validation-status field describes the result of a specified test procedure. It remains separate from the physical observable and from balanced-ternary execution.

## 4. Validation Case Contract

Each validation case is identified before execution by a case identifier and an immutable set of declared inputs.

The case record contains:

| Field | Required information |
| --- | --- |
| `case_id` | Unique qualification-case identifier |
| `contract_id` | Mathematical or executable contract |
| `observable_id` | Quantity being compared or tested |
| `state_id` | Material, thermodynamic, and computational state |
| `source_id` | Primary source or numerical reference identity |
| `method_id` | Measurement, simulation, or numerical method |
| `implementation_id` | Selected executable operator or model |
| `configuration_id` | Atomic configuration or dataset sample |
| `normalization_id` | Observable normalization convention |
| `unit` | Physical or numerical unit |
| `comparison_id` | Selected correspondence procedure |
| `uncertainty_id` | Applicable uncertainty model |
| `criterion_id` | Predeclared acceptance condition |
| `environment_id` | Software and numerical environment |
| `result_id` | Recorded execution result |

A case additionally records spatial boundaries, temporal sampling, composition, physical state, stochastic inputs where applicable, and model parameters.

Exact mathematical conditions and numerical comparison conditions are declared separately.

## 5. Mathematical Invariant Catalogue

The validation program preserves exact categorical and structural invariants alongside numerical relations.

| Invariant family | Relation or condition | Comparison |
| --- | --- | --- |
| Species domain | `S_i ∈ {Li, Be, F}` | Exact |
| Atomic cardinality | `N_species = N_positions` | Exact |
| Configuration ordering | Stable ordered atom identities | Exact |
| Formula-unit inventory | Integer Li/Be/F count relations | Exact |
| Formal charge | `Q_formal = N_Li + 2N_Be − N_F` | Exact integer arithmetic |
| Ternary alphabet | `T = {-1, 0, 1}` | Exact |
| Pending domain | `pending ∈ {-1, 1}` or `None` | Exact |
| Committed transitions | Membership in permitted transition relation | Exact |
| Graph cardinality | Graph nodes equal configuration atoms | Exact |
| Dataset isolation | Disjoint declared split identities | Exact |
| Hierarchy compatibility | Adjacent level cardinalities agree | Exact |
| Mass balance | Source mass equals mapped mass | Numerical accumulation |
| Geometric covariance | Transformed outputs follow the group action | Numerical |
| Energy-force relation | `F_i = −∇_(r_i) E` | Numerical derivative |
| Stress relation | Declared energy–strain derivative | Numerical derivative |
| Deterministic replay | Repeated outputs under identical inputs | Exact or predeclared numerical comparison |

Mathematical statements involving real-valued operations retain their assumptions concerning differentiability, finiteness, domain, and numerical representation.

## 6. FLiBe Composition Coordinates

For nonnegative LiF and BeF2 formula-unit amounts with positive total:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

The composition constraint is:

`x_LiF + x_BeF2 = 1`.

For the exact ratio `2 LiF : 1 BeF2`:

`x_LiF = 2/3`.

`x_BeF2 = 1/3`.

The corresponding atomic inventory is:

`N_Li : N_Be : N_F = 2 : 1 : 4`.

Three distinct composition records occur in the registered FLiBe references:

| Composition record | LiF molar fraction | BeF2 molar fraction |
| --- | ---: | ---: |
| Exact `2 LiF : 1 BeF2` | `2/3` | `1/3` |
| Nominal `67:33 mol%` | `0.67` | `0.33` |
| Vidrio measured composition | `0.6642` | `0.3358` |

The measured BeF2 composition is `33.58(5) mol%`, reported from ICP-MS analysis.

The measured uncertainty corresponds to `0.05 mol%`, or `0.0005` in molar-fraction units.

A composition-comparison procedure retains the original source composition, its uncertainty, and any selected composition transformation.

## 7. Thermodynamic and Physical-State Coordinates

The executable `FLiBeThermodynamicState` contains:

`T > 0`, in kelvin.

`P >= 0`, in pascal.

Both coordinates are finite real values.

A complete material-state comparison additionally identifies:

- LiF–BeF2 composition;
- material phase or physical-state classification;
- temperature and pressure;
- density or volume definition;
- simulation or measurement ensemble;
- spatial averaging region;
- temporal averaging interval;
- applicable external fields;
- boundary and exchange conditions.

A direct observable comparison requires explicit correspondence of the state coordinates relevant to that observable.

The state record distinguishes experimentally measured coordinates, computationally imposed coordinates, inferred coordinates, and coordinates requiring additional source information.

## 8. State Correspondence Operator

Let an observation be associated with state:

`X = (x, T, P, phase, geometry, ensemble, normalization, time_domain)`.

For reference state `X_ref` and model state `X_model`, define a correspondence record:

`M_state(X_ref, X_model, assumptions)`.

The record stores the comparison result for each required coordinate.

| Coordinate | Correspondence requirement |
| --- | --- |
| Composition | Same numerical definition or registered composition mapping |
| Temperature | Same unit and selected temperature correspondence |
| Pressure | Registered values and applicable pressure correspondence |
| Material state | Declared physical-state classification |
| Observable | Identical quantity definition |
| Normalization | Identical or explicitly transformed normalization |
| Sampling domain | Compatible spatial and temporal support |
| Ensemble | Applicable statistical-mechanical correspondence |
| Units | Explicit conversion to common units |
| Uncertainty | Source-supported uncertainty and transformation |

The direct-comparison branch is selected when its required coordinates satisfy the declared matching contract.

Temperature-screened comparisons with unresolved composition, pressure, or phase coordinates remain separately identified numerical comparison records.

## 9. Experimental Reference: Vidrio et al. 2022

The registered experimental dataset is:

`data/reference/flibe_vidrio_2022_density_measurements.json`

Dataset identifier:

`tr-eif.flibe.vidrio-2022.experimental-density.v1`.

Primary publication:

Vidrio et al., *Density and Thermal Expansivity of Molten 2LiF-BeF2 (FLiBe): Measurements and Uncertainty Quantification*, Journal of Chemical & Engineering Data, 67 (2022), 3517–3531.

DOI: `10.1021/acs.jced.2c00212`.

The registered source location is Table 4. The measurement method is hydrostatic buoyancy.

The executable dataset contains 61 density measurements distributed across four experimental runs:

| Run | Measurements |
| --- | ---: |
| `0A` | 28 |
| `1A` | 7 |
| `1B` | 13 |
| `1C` | 13 |
| Total | 61 |

Each measurement row contains:

`(temperature_c, temperature_standard_uncertainty_c, density_kg_m3, density_standard_uncertainty_kg_m3)`.

The registered source metadata include:

- measured BeF2 composition: `33.58(5) mol%`;
- composition measurement method: ICP-MS;
- measurement pressure: `102 ± 1 kPa`;
- registered temperature interval: `447–817 °C`;
- reported melting temperature: `459.1 ± 0.2 °C`;
- three recorded temperatures below the reported melting-temperature central value.

The temperature, density, and composition uncertainties retain their respective source definitions.

Individual run identities remain attached to each numerical comparison and statistical aggregation.

## 10. First-Principles Reference: Baral et al. 2021

The registered first-principles dataset is:

`data/reference/flibe_baral_2021_aimd_density.json`

Dataset identifier:

`tr-eif.flibe.baral-2021.aimd-structural-density.v1`.

Primary publication:

Baral et al., *Temperature-Dependent Properties of Molten Li2BeF4 Salt Using Ab Initio Molecular Dynamics*, ACS Omega, 6 (2021), 19822–19835.

DOI: `10.1021/acsomega.1c02528`.

The registered source location is Table 1.

The dataset contains nine positive-temperature AIMD records associated with the exact `Li2BeF4` composition.

Each row contains:

`(temperature_k, cubic_cell_edge_angstrom, reported_cell_volume_angstrom3, simulated_density_g_cm3)`.

The source metadata identify an AIMD supercell containing 504 atoms.

The `T0` table entry is retained separately in the dataset metadata.

The registered table does not provide a pressure value or a numerical density uncertainty for these nine records. Those coordinates retain their respective source-information status during comparison.

Each temperature record is associated with its original computational method and reported geometric quantities.

## 11. Registered Density Correlation

The repository contains a source-derived FLiBe density correlation evaluated through:

`benchmarks/flibe/reference_property_reproduction.py`.

The registered source identifier is:

`FLIBE-REFERENCE-JANZ-1974-DENSITY`.

The correlation represents the nominal composition:

`67 mol% LiF : 33 mol% BeF2`.

Its registered linear form is:

`ρ(T) = a + bT`.

With:

`a = 2413.0 kg/m³`.

`b = −0.488 kg/(m³·K)`.

The registered temperature domain is:

`800 K <= T <= 1080 K`.

The executable benchmark evaluates this correlation through the `FLiBeDensityModel` and `FLiBeThermodynamicState` interfaces.

Reference-value reproduction compares the calculated correlation values against independently declared benchmark fixture values at the registered sample temperatures.

Experimental observations, source-derived correlation values, and TR-EIP model outputs retain separate source and method identifiers.

## 12. Unit Normalization

Every comparison selects a common unit system before residual calculation.

The registered conversions include:

`T_K = T_°C + 273.15`.

`P_Pa = 1000 P_kPa`.

`ρ_kg/m³ = 1000 ρ_g/cm³`.

`V_m³ = 10^(-30) V_Å³`.

For temperature standard uncertainty under the exact additive conversion:

`u(T_K) = u(T_°C)`.

For pressure standard uncertainty:

`u(P_Pa) = 1000 u(P_kPa)`.

The source numeric values, original units, conversion constants, and converted values are retained in the comparison record.

Atomic masses, simulation-cell volumes, and density calculations use a dimensionally consistent mass–length–time representation.

## 13. Experimental–First-Principles Typed Comparison

The executable comparison implementation is:

`src/tr_eif/flibe/reference_comparison.py`.

`FLiBeReferenceObservable` stores:

- `observable_id`;
- `composition`;
- `thermodynamic_state`;
- `physical_state_id`;
- `evidence_kind`;
- `values`;
- `value_unit`;
- `normalization_id`;
- `source_id`;
- `method_id`;
- `provenance`;
- optional `axis` and `axis_unit`.

The function:

`compare_flibe_experimental_first_principles(experimental, first_principles)`

returns `FLiBeReferenceComparison`.

The implemented direct-comparison contract requires equal observable identity, composition, thermodynamic state, physical-state identity, value unit, normalization, sample axis, axis unit, and sample cardinality.

It also requires `EXPERIMENTAL` for the first record and `FIRST_PRINCIPLES` for the second.

For matched values, the residual convention is:

`r_i = y_i^(first_principles) − y_i^(experimental)`.

The result exposes the ordered residuals, absolute residuals, mean absolute error, root mean square error, and maximum absolute error.

Unit conversion, interpolation, state mapping, and uncertainty propagation are performed through separately declared preprocessing or comparison procedures.

## 14. Temperature-Screened Source Comparisons

The repository contains two executable density-comparison procedures with explicitly recorded temperature screening.

### Experimental density and registered correlation

Implementation:

`benchmarks/flibe/experimental_density_cross_source_diagnostic.py`.

For each retained experimental point:

`r_i = ρ_correlation(T_i) − ρ_experimental(T_i)`.

The screening intersects the source measurement temperatures with the registered correlation temperature domain and the selected melting-temperature condition.

The procedure preserves experimental run identity and the measured uncertainties.

The registered correlation's nominal BeF2 composition is `33 mol%`, while the experimental specimen's measured composition is `33.58(5) mol%`.

### Experimental density and AIMD structural density

Implementation:

`benchmarks/flibe/experimental_aimd_density_cross_source_diagnostic.py`.

For each selected AIMD temperature, experimental density is interpolated between adjacent measurements within an individual experimental run.

For bracket temperatures `T_a <= T <= T_b`:

`w = (T − T_a) / (T_b − T_a)`.

`ρ_interp(T) = (1 − w)ρ_a + wρ_b`.

The resulting residual is:

`r_i = ρ_AIMD(T_i) − ρ_experimental,interp(T_i)`.

Interpolation records identify the source run, bounding measurements, interpolation weight, and selected temperature.

Composition, pressure, phase, and density-uncertainty correspondence are represented separately from the temperature-screening result.

## 15. Registered Numerical Density Comparisons

The executable density procedures contain reproducible numerical outputs for the registered datasets.

| Comparison | Selected observations | Numerical procedure |
| --- | ---: | --- |
| Vidrio versus registered correlation | 39 | Experimental-point evaluation inside the correlation temperature domain |
| Baral versus Vidrio | 9 paired residuals | Within-run experimental interpolation at three AIMD temperatures |

For the registered correlation comparison, 22 of the 61 experimental points lie outside the selected correlation temperature domain. Three below-melting-temperature records are included within those excluded points.

The executable comparison produces:

| Metric | Correlation minus experiment, kg/m³ |
| --- | ---: |
| Mean absolute residual | `8.0768307692` |
| Root mean square residual | `11.3200522371` |
| Maximum absolute residual | `24.2572` |

For the registered AIMD comparison, the evaluated AIMD temperatures are:

`750 K`, `850 K`, and `1000 K`.

Six other positive-temperature AIMD records are screened out by the declared temperature procedure.

The resulting nine paired residuals yield:

| Metric | AIMD minus interpolated experiment, kg/m³ |
| --- | ---: |
| Mean signed residual | `−273.7386067518` |
| Mean absolute residual | `273.7386067518` |
| Root mean square residual | `273.8555291548` |
| Minimum signed residual | `−285.30625` |
| Maximum signed residual | `−260.1731481481` |

These tables identify numerical outcomes of the source-to-source comparison procedures. The associated records retain their source compositions, known and unresolved thermodynamic coordinates, and interpolation metadata.

A material-model comparison uses independently identified model outputs and its own state-correspondence contract.

## 16. Interatomic Model Output Correspondence

The FLiBe interatomic realization is implemented in:

`src/tr_eif/flibe/tr_eip.py`.

`FLiBeTREIPModel.evaluate` receives:

`configuration, graph, features, resonance, execution`.

It returns an `FLiBeTREIPResult` containing the configuration, interaction graph, resonance descriptor, retained execution vector, input features, resonance-conditioned features, and energy-model result.

For model parameters `λ`, atomic positions `R`, continuous resonance descriptor `z`, and retained ternary execution state `τ`, define the conditioned energy:

`E = E_λ(R, S, G, z, τ)`.

A validation case records the selected model parameters, graph construction, feature definitions, resonance provider, execution state, and physical configuration.

Energy, Cartesian forces, stress, and trajectory-derived quantities are compared with reference observables defined using the corresponding physical and numerical conventions.

A density comparison derived from a simulation cell additionally requires mass and volume:

`ρ_model = M_cell / V_cell`.

The calculation records the atomic mass convention, simulation volume, thermodynamic ensemble, sampled state, and uncertainty procedure.

## 17. Residual and Error Metrics

For `N >= 1` matched numerical samples, define:

`r_i = y_i^(calculated) − y_i^(reference)`.

The mean signed residual is:

`Bias = (1/N) Σ_i r_i`.

The mean absolute error is:

`MAE = (1/N) Σ_i |r_i|`.

The root mean square error is:

`RMSE = sqrt[(1/N) Σ_i r_i²]`.

The maximum absolute error is:

`E_max = max_i |r_i|`.

For reference values with a declared nonzero normalization scale `s_i`, define the normalized residual:

`r_i,normalized = r_i / s_i`.

Metric records retain their units, sample count, source grouping, normalization, sign convention, and numerical accumulation method.

Distinct reference-state groups are aggregated using a declared weighting procedure.

## 18. Measurement and Model Uncertainty

For a measured observable `y_exp` and calculated observable `y_calc`, let:

`r = y_calc − y_exp`.

With covariance matrices `C_calc`, `C_exp`, and cross-covariance `C_cross`, the residual covariance is:

`C_r = C_calc + C_exp − C_cross − C_cross^T`.

For independent scalar uncertainties:

`u_r² = u_calc² + u_exp²`.

When the standard uncertainty `u_r > 0` is established, the standardized residual is:

`z = r / u_r`.

For a nonsingular covariance matrix and a declared statistical comparison, the quadratic discrepancy measure is:

`Q = r^T C_r^(-1) r`.

The covariance model identifies correlations between observations, simulation samples, measurements, and shared calibration or reference parameters.

The selected statistical acceptance criterion is established before calculating the comparison result.

## 19. Temperature and Composition Uncertainty Propagation

A temperature-dependent correlation `ρ(T, x, λ)` may depend on temperature, composition, and source parameters.

For a differentiable mapping with input vector:

`q = (T, x, λ)`,

and covariance matrix `C_q`, first-order uncertainty propagation gives:

`u_ρ² ≈ J_ρ C_q J_ρ^T`,

where:

`J_ρ = ∂ρ/∂q`.

For the registered linear density relation with fixed coefficients:

`∂ρ/∂T = b`.

A temperature-only uncertainty component is therefore:

`u_ρ,T = |b| u_T`.

Coefficient uncertainties and covariance terms are incorporated when their numerical values and correlation model are registered.

Composition-dependent corrections require a specified composition-response relation and its domain of applicability.

Interpolation uncertainty retains the source measurement uncertainties and their applicable covariance assumptions. The interpolation procedure and the uncertainty-propagation procedure are recorded as distinct transformations.

## 20. Independent Sampling and Statistical Dependence

Experimental series, atomistic trajectories, and first-principles calculations have different sampling structures.

The validation program identifies:

- experimental run identity;
- independent specimen or batch identity;
- shared calibration conditions;
- AIMD trajectory or supercell identity;
- MD trajectory identity;
- equilibration interval;
- sampling interval;
- autocorrelation structure;
- independent replica or initial-condition identity.

For a stationary time series with integrated autocorrelation time `τ_int` and sampling interval `Δt`, an approximate effective sample count can be represented as:

`N_eff ≈ N Δt / (2τ_int)`.

The convention used to estimate `τ_int` is recorded with the calculation.

Statistical confidence intervals are constructed through a specified estimator and resampling or covariance procedure.

Experimental run identities and related simulation trajectories remain available for grouped statistical analysis.

## 21. Atomic Configuration and Formal-Charge Qualification

The FLiBe atomic configuration uses an ordered species tuple:

`S = (s_0, ..., s_(N−1))`.

Each atom has a three-dimensional Cartesian position:

`r_i ∈ R³`.

The exact structural qualification includes:

- permitted species membership;
- equal species and position cardinality;
- finite Cartesian coordinates;
- valid periodic-cell representation;
- preservation of ordered species identities;
- correct species counting;
- composition mapping under the declared stoichiometric condition;
- formal-charge accounting.

For species counts:

`Q_formal = N_Li + 2N_Be − N_F`.

For an exact `Li2BeF4` inventory:

`Q_formal = 0`.

The executable configuration, composition, formal-charge, and mass functions are located in `src/tr_eif/flibe/`.

Atomic inventory, formal ionic charge, and ternary execution polarity retain separate data types and physical meanings.

## 22. Local Structure and Coordination

Local structure is evaluated from the selected atomic configuration, periodic geometry, and interaction graph.

For a receiving atom `j` and source species `s`, define:

`z_(j,s) = count{(i→j) ∈ G | species(i) = s}`.

The executable function:

`build_flibe_coordination_state(configuration, graph)`

returns the ordered FLiBe coordination records.

Qualification includes:

1. Directed source and receiver identity.
2. Graph-node and configuration cardinality.
3. Canonical species-resolved neighbor counts.
4. Periodic-image selection and multiplicity.
5. Cutoff-boundary behavior.
6. Atomic permutation consistency.
7. Geometric transformation behavior.
8. Deterministic graph construction.

Reference structural observables may include species-resolved pair distributions, coordination integrals, structure factors, and local-environment statistics.

Each structural comparison specifies its radial or reciprocal-space axis, normalization, binning, cutoff, finite-size conditions, temperature, composition, and measurement or computational method.

Graph coordination and experimentally inferred coordination are related through an explicitly selected observable-extraction procedure.

## 23. E(3) Symmetry Qualification

For an orthogonal transformation `Q ∈ O(3)` and translation `b ∈ R³`, atomic positions transform as:

`r_i' = Qr_i + b`.

For scalar energy under equivalent transformed physical input:

`E(QR + b) = E(R)`.

For Cartesian forces:

`F_i(QR + b) = QF_i(R)`.

For a second-order Cartesian tensor under the corresponding transformation convention:

`σ' = QσQ^T`.

Qualification is performed with the cell, graph, feature tensors, and boundary representations transformed consistently.

The numerical error measures include:

`ε_E = |E' − E|`.

`ε_F = max_i ||F_i' − QF_i||`.

`ε_σ = ||σ' − QσQ^T||`.

Atomic permutations are tested by applying a common index permutation to every atom-indexed input and reversing that permutation when comparing node outputs.

Scalar invariant values use the selected numerical tolerance. Species identities, tensor ranks, dimensions, and index associations use exact structural checks.

Spatial rotation remains separate from ternary-polarity reversal.

## 24. Conservative Energy, Forces, and Stress

The reference energy interface produces an `EnergyState` containing ordered atomic energies and their total.

For a differentiable scalar energy functional:

`E_total = Σ_i E_i`.

The Cartesian conservative-force relation is:

`F_i = −∂E_total/∂r_i`.

The current `ConservativeForceEvaluator` computes fixed-graph central differences:

`F_(i,a) ≈ −[E(r_(i,a) + h) − E(r_(i,a) − h)] / (2h)`.

The selected graph, node features, and executed ternary vector are retained during the finite-difference evaluation.

For homogeneous strain `ε` and reference cell volume `V`, the stress convention used by `ConservativeStressEvaluator` is:

`σ_ab = (1/V) ∂E_total/∂ε_ab`.

Its finite-difference implementation uses symmetric strain perturbations and explicitly symmetrizes the returned tensor.

Qualification records include differentiation step sizes, graph conditions, fixed or geometry-dependent feature assumptions, energy units, Cartesian units, and comparison errors.

For a coupled model whose descriptor changes with geometry, the total derivative is evaluated under the corresponding declared chain-rule and parameter-update contract.

## 25. Continuous Resonance Dynamics

The resonance layer represents continuous oscillator phases and intrinsic frequencies on a directed interaction graph.

For incoming edges `i→j`, the implemented receiving-node Kuramoto–Sakaguchi derivative is:

`dθ_j/dt = ω_j + κ_j Σ_(i→j) sin(θ_i − θ_j − γ_j)`.

Here `κ_j` and `γ_j` are associated with the receiving node.

The executable functions include:

`phase_derivatives(state, parameters, graph)`.

`euler_step(state, parameters, graph, time_step)`.

The resonance qualification program evaluates:

- graph orientation and receiving-node parameter indexing;
- oscillator and graph cardinality;
- finite phase and frequency values;
- phase-wrapping behavior;
- integration-step correspondence;
- deterministic phase evolution;
- dependence on initial conditions and coupling parameters;
- numerical convergence over declared integration intervals.

The phase-order parameter is:

`R(t) = |(1/N) Σ_j exp(iθ_j(t))|`.

For a nonempty oscillator state:

`0 <= R(t) <= 1`, within numerical evaluation tolerance.

Resonance windows, resonance-region classifications, phase order, and broader coherence measures retain their distinct mathematical definitions.

In particular:

`R(t) ≠ C(t)`.

A resonance-window crossing, bifurcation, ternary transition, and structural transition are registered as distinct event classes.

## 26. FLiBe Resonance Parameterization

The FLiBe resonance parameterization receives the declared structural and coordination state.

Executable interfaces include:

`FLiBeResonanceParameterization`.

`ConstantFLiBeResonanceParameters`.

`evaluate_resonance_parameters(model, coordination)`.

`build_flibe_resonance_descriptor(...)`.

A resonance case records the selected atomic configuration, directed graph, coordination state, thermodynamic state, oscillator state, and parameter-provider provenance.

Parameter qualification includes:

- finite coupling and phase-lag vectors;
- oscillator-count correspondence;
- reproducible parameter-provider output;
- deterministic coordination-dependent parameter selection;
- spatial and species-index consistency;
- explicit graph sampling and update times;
- recorded sensitivity to parameter variation.

Resonance descriptors remain continuous numerical objects.

The mappings from resonance descriptors to requests and from requests to executed states are qualified separately.

## 27. Balanced-Ternary Interpretation and Active Neutral

The canonical execution alphabet is:

`T = {-1, 0, 1}`.

The state `0` is an active neutral execution state.

Its execution semantics include balancing, routing, damping, mediation, transition staging, retention, and controlled neutralization.

The FLiBe interpretation operator uses:

`FLiBeTernaryInterpretation`.

`interpret_flibe_ternary_target(interpretation, descriptor)`.

The projection maps an explicitly selected continuous descriptor to a requested ternary target using declared projection weights, bias, and ordered thresholds.

The executable execution-state contract distinguishes:

`requested target ≠ retained state`.

`pending target ≠ retained state`.

`held opportunity ≠ committed self-transition`.

The permitted opposite-polarity routes are:

`-1 → 0 → 1`.

`1 → 0 → -1`.

Each arrow represents one committed execution event.

A pending destination belongs to `{-1, 1}` and requires retained state `0`.

The invariant qualification checks target generation, threshold equality, pending retention, guard behavior, committed event identity, and exact state membership.

Missing, invalid, unknown, and nonfinite numerical values use their respective error or data-availability representations.

## 28. Ternary Execution Trace Qualification

The execution trace records the state before and after each opportunity.

An event record includes:

| Quantity | Description |
| --- | --- |
| Node identity | Atom-associated execution index |
| Previous retained state | Executed value before the opportunity |
| Requested target | Explicit categorical request |
| Pending target | Retained final destination, when present |
| Guard | Neutral-entry and neutral-exit eligibility |
| Route | Selected committed transition leg |
| Hold | Opportunity with no committed route |
| Current retained state | Executed value after the opportunity |
| Current pending target | Destination retained for a later opportunity |
| Event index | Ordering within the execution schedule |

For vector execution:

`committed_count + held_count = node_count`.

The exact relation is checked for each execution opportunity.

The current interfaces are:

`execute_ternary_step`.

`execute_ternary_vector_step`.

`propagate_md_ternary_state`.

The MD-associated execution operator preserves its supplied mechanical state and returns the typed execution result.

The committed execution vector is subsequently supplied to the selected interatomic energy evaluation.

## 29. Coupled Time-Schedule Qualification

The coupled system uses separately declared schedules for:

1. Mechanical integration.
2. Continuous resonance integration.
3. Resonance descriptor sampling.
4. Ternary request generation.
5. Ternary execution opportunities.
6. Thermodynamic and boundary updates.
7. Multiscale sampling and transfer.

Let the corresponding event times be:

`t_MD[n]`, `t_R[k]`, `t_T[m]`, and `t_MS[p]`.

A coupling record defines the state sampled at each event and the ordering of coincident events.

For mechanical evolution:

`r_i[n+1], v_i[n+1] = Φ_MD(state[n], Δt_MD)`.

For resonance evolution:

`θ[k+1] = Φ_R(θ[k], G[k], parameters[k], Δt_R)`.

For one ternary opportunity:

`τ[m+1] = Φ_T(τ[m], request[m], guard[m])`.

The execution trace identifies the retained state used by each mechanical energy or force evaluation.

Sampling and operator composition follow an explicitly registered schedule, including any retained values between updates.

## 30. Molecular-Dynamics Qualification

The generic molecular-dynamics layer provides force-driven velocity-Verlet integration.

For atom `i`:

`dr_i/dt = v_i`.

`m_i dv_i/dt = F_i`.

A position step has the form:

`r_i[n+1] = r_i[n] + v_i[n]Δt + (1/2)a_i[n]Δt²`.

The velocity update is:

`v_i[n+1] = v_i[n] + (1/2)(a_i[n] + a_i[n+1])Δt`.

The current executable entry point is:

`velocity_verlet_step(...)`.

The trajectory interface is:

`run_velocity_verlet_trajectory(...)`.

The qualification program records:

- atom ordering and masses;
- timestep and integration interval;
- initial positions and velocities;
- interaction cutoff and graph-update method;
- force-evaluator and energy-model identities;
- periodic cell and image conventions;
- retained ternary execution vector;
- thermal and pressure-control operations when selected;
- trajectory observables and sampling intervals.

Resonance evolution and ternary execution are evaluated by their explicit propagation operators.

## 31. Energy and Mechanical Balance

For a fixed particle inventory, define kinetic energy:

`K = (1/2) Σ_i m_i |v_i|²`.

For the selected potential:

`H = K + E_total`.

On a closed conservative fixed-Hamiltonian interval, energy-drift qualification uses:

`ΔH[n] = H[n] − H[0]`.

A normalized measure can be defined using a predeclared nonzero energy scale `E_scale`:

`d_H[n] = |ΔH[n]| / E_scale`.

The numerical acceptance condition accounts for timestep, integration length, force-differentiation error, and the declared conservative dynamics.

For an open or controlled system, the balance includes external energy transport, heat, work, material exchange, and explicitly applied state or parameter updates.

With signed energy transfers `Q`, `W`, and `E_exchange`:

`H(t_1) − H(t_0) = Q + W + E_exchange + R_balance`.

Here `R_balance` is the registered numerical balance residual under the declared sign convention.

Thermostat, barostat, boundary, and execution events are associated with their respective energy-accounting records.

## 32. FLiBe Transport Observable Qualification

Transport qualification uses independently identified quantities and species.

For atomic species `s`, a three-dimensional self-diffusion estimator may use the long-time Einstein relation:

`D_s = lim_(t→∞) MSD_s(t) / (6t)`.

The corresponding displacement record uses unwrapped Cartesian trajectories where periodic motion is represented.

The executable MD layer contains:

`mean_squared_displacement(...)`.

`velocity_autocorrelation(...)`.

Transport comparisons identify the definition and sampling domain of each coefficient.

The program distinguishes:

- Li self-diffusion;
- Be self-diffusion;
- F self-diffusion;
- collective diffusion;
- species-resolved fluxes;
- dynamic and kinematic viscosity;
- thermal conductivity;
- electrical conductivity;
- hydrogen-isotope diffusion;
- hydrogen-isotope solubility;
- permeability.

Hydrogen, deuterium, and tritium retain their isotope-specific transport identities.

A transport coefficient includes its physical unit, temperature, pressure, composition, material-state domain, trajectory or experimental source, estimator, and statistical uncertainty.

## 33. Multiscale Mass and Geometry Qualification

The FLiBe structural multiscale model is implemented in:

`src/tr_eif/flibe/multiscale_coolant.py`.

The principal interfaces are:

`FLiBeMultiscaleCoolantModel.build_state(configuration, positions=None)`.

`build_flibe_multiscale_coolant_state(model, configuration, positions=None)`.

For fine-to-coarse partition groups `I_c`, coarse mass is:

`M_c = Σ_(i∈I_c) m_i`.

The mass-weighted centroid is:

`R_c = [Σ_(i∈I_c) m_i r_i] / M_c`.

For a complete fixed-inventory partition:

`Σ_c M_c = Σ_i m_i`.

Under a common rigid transformation:

`R_c' = QR_c + b`.

The executable hierarchy validates compatible adjacent partitions and constructs one coarse state per hierarchy transition.

For periodic configurations, explicit unwrapped Cartesian positions are supplied to the FLiBe structural builder.

## 34. Reference Multiscale Fixture

The committed FLiBe multiscale integration fixture uses seven atoms with species ordering:

`(Li, Li, Be, F, F, F, F)`.

The fixture mass parameters are:

`m_Li = 2.0`.

`m_Be = 3.0`.

`m_F = 5.0`.

The hierarchy is:

`7 → 3 → 1`.

Its first partition is:

`(0, 0, 1, 1, 2, 2, 2)`.

The second partition is:

`(0, 0, 0)`.

The first coarse masses are:

`(4.0, 8.0, 15.0)`.

The final mass is:

`27.0`.

The final Cartesian centroid is:

`(7/9, 2/3, 10/27)`.

The qualification compares the calculated hierarchy against these independently declared fixture quantities, with exact partition identities and preselected numerical tolerances for floating-point reductions.

## 35. Multiscale Thermodynamic and Transport Transfer

The downstream multiscale interfaces include:

`evaluate_mesoscale_closure(...)`.

`evaluate_continuum_closure(...)`.

`evaluate_transport_coefficient_transfer(...)`.

`evaluate_thermodynamic_consistency(...)`.

`evaluate_uncertainty_propagation(...)`.

`evaluate_engineering_boundaries(...)`.

Each provider binds source variables, target variables, state-domain identifiers, mapping context, and provenance.

For a continuum coolant region with mass density `ρ`, velocity `u`, and mass source `s_m`:

`∂ρ/∂t + div(ρu) = s_m`.

For species concentration `c_s`, diffusive flux `j_s`, and source `q_s`:

`∂c_s/∂t + div(c_su + j_s) = q_s`.

The validation program evaluates discretized balance residuals over declared spatial cells and time intervals.

Transport transfer records preserve coefficient identity, unit, source scale, target scale, and state-domain correspondence.

For a differentiable scale mapping `y = f(x)` with Jacobian `J`:

`C_y ≈ JC_xJ^T`.

The target uncertainty record retains the selected input covariance, transformation, and assumptions.

## 36. Numerical Convergence and Error Budgets

Numerical qualification separates the principal error contributions:

- source measurement uncertainty;
- first-principles sampling and methodological uncertainty;
- interatomic-model approximation error;
- finite-size error;
- finite-time sampling error;
- mechanical integration error;
- resonance integration error;
- numerical differentiation error;
- spatial discretization error;
- multiscale transfer error;
- floating-point accumulation error.

For a numerical approximation `y_h` with refinement parameter `h`, define:

`ε_h = ||y_h − y_reference||`.

Where a reference solution is unavailable, a refinement comparison can be defined as:

`ε_(h,h/2) = ||y_h − y_(h/2)||`.

The selected norm, compared state variables, refinement sequence, and convergence estimator are specified before execution.

When a method has an applicable asymptotic error model:

`ε_h ≈ C h^p`,

the observed convergence order may be estimated from suitably refined calculations under the declared assumptions.

Numerical tolerances are established from the method, precision, expected discretization behavior, and independent reference requirements before executing the corresponding qualification case.

## 37. Dataset Separation and Model Qualification

The FLiBe dataset interface is implemented in:

`src/tr_eif/flibe/dataset_configuration.py`.

`FLiBeDatasetConfiguration` stores sample identity, configuration identity, atomic configuration, thermodynamic state, provenance, split, and optional source, group, trajectory, and parent-sample identifiers.

The supported split values are:

`TRAINING`.

`VALIDATION`.

`TEST`.

The function:

`validate_flibe_split_isolation(samples)`

checks the executable split-isolation contract.

A model qualification record identifies:

- training-source identities;
- independent validation-source identities;
- test-source identities;
- related configuration groups;
- shared trajectory or parent relationships;
- preprocessing and calibration procedures;
- parameter-selection history;
- final frozen model parameters;
- independent comparison criteria.

Repeated physical observations or correlated trajectory samples retain their shared grouping identities during split construction.

Training-stage transitions and validation metadata remain separate from balanced-ternary execution.

## 38. Determinism and Reproducibility

For a deterministic executable mapping `F` with fully specified inputs `X` and environment `E`, the replay condition is:

`F(X, E) = Y`.

Repeated evaluations use identical registered inputs, operator selections, and ordering conventions.

A reproducibility record contains:

1. Repository revision or archive identity.
2. Package and interpreter versions.
3. Source-data identifiers and file fingerprints.
4. Atomic configuration and composition.
5. Model parameters and provenance.
6. Thermodynamic and boundary state.
7. Graph and neighbor-list construction settings.
8. Resonance initial state and integration settings.
9. Ternary retained, pending, requested, and guarded states.
10. Mechanical initial state and integration schedule.
11. Multiscale hierarchy and provider identities.
12. Numeric precision and accumulation conventions.
13. Random seeds and sampling algorithms where applicable.
14. Predeclared comparison tolerances.
15. Ordered output and execution-trace identifiers.
16. Test result and execution-environment identity.

Source data and transformed data are associated through explicit transformation records.

The existing observable and replay modules provide executable mechanisms for ordered trace construction, serialization, file export, and replay qualification.

## 39. Predeclared Acceptance Criteria

Acceptance criteria are attached to specific tests before their execution.

| Test class | Predeclared criterion |
| --- | --- |
| Species and composition | Exact membership, cardinality, and composition contract |
| Formal charge | Exact integer relation |
| Ternary execution | Exact permitted-state and transition membership |
| Pending and guard behavior | Exact route and event-state relation |
| Dataset isolation | Exact group and split constraints |
| Source identity | Expected dataset identifier, source metadata, and fingerprint |
| Direct reference comparison | Exact compatibility of required typed coordinates |
| Unit conversion | Declared algebraic conversion and numerical precision |
| Energy and forces | Declared derivative-error bound |
| Stress | Declared strain-derivative and tensor-error bounds |
| E(3) | Declared scalar, vector, and tensor transformation-error bounds |
| Resonance integration | Declared method and refinement-error bounds |
| MD conservation | Declared conserved-system error budget |
| Open-system balance | Declared flux and boundary residual budget |
| Multiscale reduction | Exact partition structure and numerical conservation tolerance |
| Reproducibility | Exact output identity or predeclared floating-point comparison |
| Runtime and memory | Declared input scale, measurement method, and resource metric |

For a scalar numerical comparison, an acceptance condition may be expressed as:

`|y_calc − y_ref| <= δ_abs + δ_rel |y_ref|`.

The absolute tolerance `δ_abs` and relative tolerance `δ_rel` are defined in the case contract and associated with the relevant numeric method and reference.

An exact categorical invariant uses exact equality.

## 40. Result Registration Procedure

Each executable qualification follows the sequence:

1. Register the mathematical contract.
2. Register the physical or computational input state.
3. Register source evidence and provenance.
4. Identify the selected executable implementation.
5. Define the observable and its units.
6. Apply the declared state and unit correspondence.
7. Freeze numerical methods and acceptance criteria.
8. Execute the calculation.
9. Preserve ordered raw results.
10. Calculate residuals and uncertainty measures.
11. Evaluate the predeclared criteria.
12. Register the execution and result identifiers.
13. Associate the result with the repository revision.
14. Preserve the corresponding test and CI evidence.

The result record contains the observed metric values and the outcome of each applicable declared criterion.

Cases with incomplete comparison coordinates retain those coordinates and their associated information requirements.

## 41. FLiBe Benchmark Coverage

The current repository contains the following executable benchmark programs:

| Benchmark | Executable path |
| --- | --- |
| Correctness | `benchmarks/flibe/reference_correctness.py` |
| Equivariance | `benchmarks/flibe/reference_equivariance.py` |
| Conservation | `benchmarks/flibe/reference_conservation.py` |
| Numerical convergence | `benchmarks/flibe/reference_numerical_convergence.py` |
| Property reproduction | `benchmarks/flibe/reference_property_reproduction.py` |
| Scaling | `benchmarks/flibe/reference_scaling.py` |
| Memory use | `benchmarks/flibe/reference_memory.py` |
| Runtime | `benchmarks/flibe/reference_runtime.py` |
| Experimental density comparison | `benchmarks/flibe/experimental_density_cross_source_diagnostic.py` |
| Experimental–AIMD density comparison | `benchmarks/flibe/experimental_aimd_density_cross_source_diagnostic.py` |

Each benchmark has its own input fixture, observable, normalization, method, and result fields.

Resource measurements are associated with their input size, interpreter, execution environment, repetition policy, and aggregation procedure.

Cross-model comparisons use separately identified implementations, matched physical states, common observable definitions, and registered numerical settings.

## 42. Independent Test and CI Qualification

The repository contains the following principal test directories:

`tests/invariants/`.

`tests/integration/`.

`tests/determinism/`.

`tests/equivariance/`.

`tests/conservation/`.

`tests/numerical/`.

The existing Python CI workflow is:

`.github/workflows/python-tests.yml`.

Its jobs include:

- package compilation and public-module imports;
- structured-output qualification;
- deterministic, equivariance, conservation, and numerical qualification;
- complete repository pytest execution.

The workflow uses Python 3.12 and installs the package with its development dependencies before running the tests.

The schema-validation workflow is:

`.github/workflows/schema-validation.yml`.

Structured test reports preserve the corresponding CI execution identity and repository revision.

A test report records the actual executed test selection, collected count, completed count, results, and any execution interruption.

## 43. Executable Interface Index

| Component | Repository path |
| --- | --- |
| FLiBe species and composition | `src/tr_eif/flibe/species.py`, `src/tr_eif/flibe/composition.py` |
| Atomic configuration | `src/tr_eif/flibe/configuration.py` |
| Formal-charge accounting | `src/tr_eif/flibe/charge.py` |
| Atomic masses | `src/tr_eif/flibe/mass.py` |
| Thermodynamic state | `src/tr_eif/flibe/thermodynamic_state.py` |
| Density operators | `src/tr_eif/flibe/density.py` |
| Units and provenance | `src/tr_eif/flibe/units.py` |
| Experimental–first-principles comparison | `src/tr_eif/flibe/reference_comparison.py` |
| Dataset and split records | `src/tr_eif/flibe/dataset_configuration.py` |
| Local coordination | `src/tr_eif/flibe/coordination.py` |
| Resonance parameters | `src/tr_eif/flibe/resonance_parameterization.py` |
| Resonance descriptor | `src/tr_eif/flibe/resonance_descriptor.py` |
| Ternary interpretation | `src/tr_eif/flibe/ternary_interpretation.py` |
| FLiBe TR-EIP model | `src/tr_eif/flibe/tr_eip.py` |
| FLiBe multiscale builder | `src/tr_eif/flibe/multiscale_coolant.py` |
| Continuous phase dynamics | `src/tr_eif/resonance/dynamics.py`, `src/tr_eif/resonance/integrator.py` |
| Ternary execution | `src/tr_eif/ternary/execution.py`, `src/tr_eif/ternary/vector_execution.py` |
| Energy and differentiation | `src/tr_eif/energy/` |
| Molecular dynamics | `src/tr_eif/md/` |
| Multiscale transfer and closure | `src/tr_eif/multiscale/` |
| Trace and replay | `src/tr_eif/observables/` |

## 44. FLiBe Qualification Test Index

| Validation area | Repository test |
| --- | --- |
| Species and composition | `tests/invariants/test_flibe_composition_invariants.py` |
| Configuration | `tests/invariants/test_flibe_configuration_invariants.py` |
| Formal charge | `tests/invariants/test_flibe_charge_invariants.py` |
| Mass and density | `tests/invariants/test_flibe_mass_invariants.py`, `tests/invariants/test_flibe_density_invariants.py` |
| Thermodynamic state | `tests/invariants/test_flibe_thermodynamic_state_invariants.py` |
| Experimental dataset | `tests/integration/test_flibe_vidrio_2022_density_dataset.py` |
| Source comparison | `tests/integration/test_flibe_reference_comparison.py` |
| Experimental correlation comparison | `tests/integration/test_flibe_experimental_density_cross_source_diagnostic.py` |
| Experimental–AIMD comparison | `tests/integration/test_flibe_experimental_aimd_density_cross_source_diagnostic.py` |
| Dataset isolation | `tests/invariants/test_flibe_dataset_configuration_invariants.py` |
| Coordination | `tests/invariants/test_flibe_coordination_invariants.py` |
| Resonance parameters | `tests/invariants/test_flibe_resonance_parameterization_invariants.py` |
| Resonance descriptor | `tests/invariants/test_flibe_resonance_descriptor_invariants.py` |
| Ternary interpretation | `tests/invariants/test_flibe_ternary_interpretation_invariants.py` |
| FLiBe TR-EIP | `tests/integration/test_flibe_tr_eip.py` |
| FLiBe molecular dynamics | `tests/integration/test_flibe_molecular_dynamics_validation.py` |
| FLiBe multiscale invariants | `tests/invariants/test_flibe_multiscale_coolant_invariants.py` |
| FLiBe multiscale closure | `tests/integration/test_flibe_multiscale_coolant_closure.py` |
| Cross-scale qualification | `tests/integration/test_multiscale_cross_scale_validation.py` |
| Energy and force covariance | `tests/equivariance/test_energy_invariance.py`, `tests/equivariance/test_force_equivariance.py` |
| MD resonance propagation | `tests/integration/test_molecular_dynamics_resonance_propagation.py` |
| MD ternary propagation | `tests/integration/test_molecular_dynamics_ternary_propagation.py` |
| Trace replay | `tests/determinism/test_trace_replay.py` |
| Trace schema | `tests/invariants/test_trace_schema_contract.py` |

The benchmark qualification tests additionally cover reference correctness, equivariance, conservation, numerical convergence, property reproduction, scaling, memory, and runtime.

## 45. Reproducibility Matrix

A completed validation record associates each observable with its source, transformation, comparison procedure, and executable evidence.

| Observable or condition | Input provenance | Operation | Recorded result |
| --- | --- | --- | --- |
| Experimental density | Vidrio 2022 | Source-table registration | Temperature, density, reported uncertainties |
| AIMD structural density | Baral 2021 | Source-table registration | Cell geometry, density, temperature |
| Registered density correlation | Janz 1974 source identifier | Temperature-dependent evaluator | Calculated density and fixture residual |
| Experimental–correlation comparison | Experimental and correlation records | Temperature screening | Ordered residuals and metrics |
| Experimental–AIMD comparison | Experimental and AIMD records | Within-run interpolation | Ordered residuals and metrics |
| Atomic structure | FLiBe configuration | Coordination operator | Ordered species-resolved counts |
| Resonance | Configuration, graph, parameters | Phase integration | Phase trajectory and descriptor |
| Ternary execution | Descriptor, request, guards, previous state | Execution operator | Event trace and retained state |
| Interatomic energy | Configuration and conditioned features | TR-EIP energy evaluation | Atomic and total energy |
| Cartesian force | Energy functional and differentiation settings | Coordinate derivative | Force vectors and numerical error |
| Stress | Energy, cell, strain settings | Strain derivative | Stress tensor and numerical error |
| Molecular dynamics | Mechanical state and force model | Time integration | Trajectory, energy, transport |
| Multiscale geometry | Atomic positions, masses, partitions | Hierarchical reduction | Coarse masses and centroids |
| Continuum transfer | Mesoscale state and closure context | Constitutive mapping | Target variables and balance records |
| Uncertainty transfer | Source covariance and selected mapping | Propagation operator | Target uncertainty representation |

Source identifiers, transformation versions, comparison criteria, and executable results are preserved together with the repository revision used for the calculation.

## 46. Scientific and Numerical Applicability Domains

Each mathematical or computational method has an explicitly defined applicability domain.

For experimental density, the domain includes the reported specimen composition, measurement temperatures, pressure, measurement method, and source uncertainties.

For AIMD structural density, the domain includes the registered composition, temperature, supercell, computational method, and reported state coordinates.

For density correlations, the domain includes the source composition, temperature interval, functional form, and registered coefficients.

For interatomic calculations, the domain includes species, configurations, parameterization, reference-state coverage, geometric boundary conditions, and model inputs.

For molecular dynamics, the domain includes the integration ensemble, timestep, physical boundary, potential, trajectory length, and sampling conditions.

For resonance integration, the domain includes the directed graph, oscillator state, coupling and phase-lag parameters, time integration, and descriptor definitions.

For ternary execution, the domain includes exact state membership, requested targets, retained and pending states, guards, and execution opportunities.

For multiscale transfer, the domain includes partitions, state mappings, averaging operations, closure assumptions, constitutive parameters, and transferred uncertainties.

Comparison results remain associated with their applicable domains and any explicitly registered extrapolation or transformation procedure.

## 47. Chapter Integration

The FLiBe validation program establishes a common qualification structure for source-backed material observations, first-principles results, conditioned interatomic calculations, mechanical trajectories, resonance dynamics, ternary execution, and multiscale transfers.

Its governing sequence is:

`registered source or model state → explicit correspondence → mathematical operator → observable → numerical metric → uncertainty → predeclared criterion → reproducible execution record`.

Exact categorical invariants, continuous numerical relations, physical observables, source evidence, and test outcomes are recorded through their respective representations.

The resulting validation records connect the FLiBe reference realization to the mathematical foundations, resonance formalism, balanced-ternary dynamics, equivariant interatomic model, molecular dynamics, and multiscale material architecture defined in Volumes 01–06.
