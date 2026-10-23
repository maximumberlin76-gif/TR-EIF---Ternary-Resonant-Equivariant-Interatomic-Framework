# Volume 07 — FLiBe Reference Model: Summary

## 1. Scope and System Class

Volume 07 defines the FLiBe reference realization within the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The material domain is the lithium fluoride–beryllium fluoride system, LiF–BeF2, represented through chemical composition, three-dimensional atomic geometry, thermodynamic states, interatomic interactions, continuous resonance dynamics, balanced-ternary execution, molecular dynamics, transport observables, and multiscale material mappings.

The represented system belongs to the selected class of open nonlinear dissipative dynamical systems.

A material realization is specified by its physical state, composition, spatial and temporal boundaries, interaction model, computational parameters, and source provenance.

The principal material computation chain is:

`composition → atomic configuration → interaction geometry → conditioned interatomic energy → forces and stress → molecular dynamics → material observables → multiscale mappings`.

The coupled resonance and execution chain is:

`directed interaction graph → continuous resonance dynamics → resonance descriptor → requested ternary target → active-neutral routing → retained -1/0/1 execution → conditioned interatomic computation`.

Mechanical evolution, resonance evolution, and ternary execution retain separate state representations and update schedules.

## 2. Volume Chapter Register

Volume 07 consists of eleven chapters.

| Chapter | Subject | Principal mathematical or computational contract |
| --- | --- | --- |
| 01 — FLiBe System Definition | Material identity and system boundaries | Species, composition, geometry, thermodynamics, open-system state |
| 02 — Species and Composition | Chemical inventory and composition mappings | Formula units, atomic counts, formal charge, mass |
| 03 — Interatomic Reference Data | Experimental and computational reference observations | Typed observables, provenance, physical-state correspondence |
| 04 — Thermodynamic Properties | Material thermodynamic variables | Density, energy, enthalpy, heat capacity, phase-equilibrium relations |
| 05 — Transport Properties | Material and species transport | Diffusion, viscosity, conductivity, isotope transport |
| 06 — Local Structure and Coordination | Three-dimensional atomic environments | Directed graph coordination, pair statistics, local structural descriptors |
| 07 — Resonance Parameterization | Continuous resonance dynamics | Coordination-dependent parameters, phase evolution, resonance descriptors |
| 08 — Ternary State Interpretation | Continuous-to-execution mapping | Projection, requested targets, active neutral, pending routes |
| 09 — Multiscale Coolant Model | Atomistic-to-engineering material mappings | Mass, centroids, hierarchy, closures, conservation, transport |
| 10 — Validation Program | Independent numerical and source correspondence | Invariants, residuals, uncertainty, reproducibility, qualification |
| 11 — Volume Summary | Integrated FLiBe reference realization | State composition, cross-layer contracts, executable interfaces |

The preceding chapters define their respective mathematical objects, executable interfaces, source registrations, numerical operations, and qualification procedures.

This chapter assembles these objects into the common FLiBe material-state and computational architecture.

## 3. Architectural Position of FLiBe

TR-EIF is the encompassing mathematical and computational framework.

TR-EIP is the interatomic model family within TR-EIF:

`TR-EIP ⊂ TR-EIF`.

The FLiBe realization provides a material-specific implementation and reference organization for this model family.

The architectural levels are:

1. Continuous physical state.
2. Chemical and geometric material representation.
3. Directed interaction and local environment.
4. Continuous resonance dynamics.
5. Resonance descriptor construction.
6. Explicit ternary request mapping.
7. Active-neutral execution.
8. Resonance- and execution-conditioned interatomic energy.
9. Mechanical and thermodynamic evolution.
10. Material observables.
11. Multiscale transport and engineering mappings.
12. Independent validation and reproducibility.

Each level has its own variables, mathematical domain, operators, and provenance.

A mapping between levels is defined through explicitly identified inputs, outputs, and conditions.

## 4. Material Identity and Chemical Inventory

The canonical atomic species are:

`S_FLiBe = {Li, Be, F}`.

The executable enumeration is:

`FLiBeSpecies`.

The canonical species order is:

`Li, Be, F`.

The binary material composition is represented using the component formula units:

`LiF`.

`BeF2`.

For nonnegative component amounts:

`n_LiF >= 0`.

`n_BeF2 >= 0`.

With:

`n_LiF + n_BeF2 > 0`.

Define:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

Therefore:

`x_LiF + x_BeF2 = 1`.

The executable composition interface is:

`FLiBeComposition`.

Composition records retain their exact numerical definitions and source identities.

## 5. Exact, Nominal, and Measured Composition

The exact reference ratio is:

`2 LiF : 1 BeF2`.

Its normalized composition is:

`x_LiF = 2/3`.

`x_BeF2 = 1/3`.

The resulting formula-unit representation is:

`Li2BeF4`.

The corresponding atomic count ratio is:

`N_Li : N_Be : N_F = 2 : 1 : 4`.

Three separate composition definitions occur in the registered reference program:

| Composition identity | LiF molar fraction | BeF2 molar fraction |
| --- | ---: | ---: |
| Exact `2:1` | `2/3` | `1/3` |
| Nominal `67:33 mol%` | `0.67` | `0.33` |
| Vidrio measured composition | `0.6642` | `0.3358` |

The measured BeF2 fraction reported by Vidrio et al. is:

`33.58(5) mol%`.

Its reported uncertainty is:

`0.05 mol%`.

These composition identities remain distinct in source registration, state correspondence, and numerical comparison.

## 6. Atomic Inventory, Formal Charge, and Mass

For atomic species counts:

`N = N_Li + N_Be + N_F`.

The formal ionic charges are:

`q_Li = 1`.

`q_Be = 2`.

`q_F = -1`.

The total formal charge is:

`Q_formal = N_Li + 2N_Be - N_F`.

For the exact `Li2BeF4` inventory:

`Q_formal = 0`.

For atomic masses `m_i`, the total configuration mass is:

`M = Σ_i m_i`.

The executable interfaces include:

`FLiBeConfiguration`.

`FormalChargeState`.

`FLiBeMassParameters`.

`configuration_masses(...)`.

`total_configuration_mass(...)`.

The formal-charge representation, physical atomic mass, continuous resonance variables, and executed ternary polarity retain separate definitions.

The canonical species inventory and atom ordering are preserved through interatomic and multiscale operations.

## 7. Three-Dimensional Material State

For `N >= 1` atoms, the configuration contains ordered species and Cartesian coordinates:

`R = (r_0, ..., r_(N-1))`.

With:

`r_i ∈ R³`.

A complete material computation may additionally contain:

- atomic velocities;
- atomic masses;
- periodic cell geometry;
- thermodynamic variables;
- interaction graph;
- local coordination;
- resonance oscillator state;
- retained ternary execution state;
- boundary and exchange variables;
- source and model provenance.

The executable configuration representation is:

`FLiBeConfiguration`.

The state maintains the relation:

`number_of_species = number_of_positions`.

Finite coordinates, species membership, valid cell data, and stable index correspondence are structural qualification conditions.

## 8. Thermodynamic State

The executable thermodynamic state is:

`FLiBeThermodynamicState`.

It contains temperature and pressure:

`T > 0`.

`P >= 0`.

The temperature unit is kelvin.

The pressure unit is pascal.

The state requires finite numerical coordinates.

A physical material comparison additionally identifies composition, phase or material-state classification, observable normalization, and applicable sampling conditions.

For a material with total mass `M` and volume `V > 0`:

`ρ = M / V`.

The corresponding specific volume is:

`v = 1/ρ`.

For differentiable density along a declared thermodynamic path, the volumetric expansion coefficient is:

`α_V = -(1/ρ)(∂ρ/∂T)`.

The thermodynamic derivative specifies which additional state coordinates are held fixed.

## 9. Registered Thermodynamic Density Correlation

The registered reference correlation has identifier:

`FLIBE-REFERENCE-JANZ-1974-DENSITY`.

Its nominal composition is:

`67 mol% LiF : 33 mol% BeF2`.

The correlation is:

`ρ(T) = 2413.0 - 0.488 T`.

With:

`ρ` in `kg/m³`.

`T` in `K`.

The registered temperature interval is:

`800 K <= T <= 1080 K`.

At:

`T = 900 K`.

The calculated density is:

`ρ(900 K) = 1973.8 kg/m³`.

The temperature derivative is:

`dρ/dT = -0.488 kg/(m³·K)`.

The executable reference reproduction program is:

`benchmarks/flibe/reference_property_reproduction.py`.

The calculation preserves correlation provenance, temperature domain, composition, units, and numerical residuals.

## 10. Experimental Density Reference

The experimental source is:

Vidrio et al. (2022).

DOI:

`10.1021/acs.jced.2c00212`.

The registered dataset is:

`data/reference/flibe_vidrio_2022_density_measurements.json`.

Dataset identifier:

`tr-eif.flibe.vidrio-2022.experimental-density.v1`.

The dataset contains 61 experimental density measurements.

| Experimental run | Measurements |
| --- | ---: |
| `0A` | 28 |
| `1A` | 7 |
| `1B` | 13 |
| `1C` | 13 |
| Total | 61 |

The source reports hydrostatic-buoyancy density measurements.

The registered physical information includes:

- measured `33.58(5) mol% BeF2`;
- ICP-MS composition analysis;
- pressure `102 ± 1 kPa`;
- temperatures spanning `447–817 °C`;
- reported melting temperature `459.1 ± 0.2 °C`.

Each experimental row preserves temperature, density, and their reported standard uncertainties.

The original experimental run identity is retained during numerical comparison.

## 11. First-Principles AIMD Reference

The registered first-principles source is:

Baral et al. (2021).

DOI:

`10.1021/acsomega.1c02528`.

The dataset is:

`data/reference/flibe_baral_2021_aimd_density.json`.

Dataset identifier:

`tr-eif.flibe.baral-2021.aimd-structural-density.v1`.

The reference material composition is:

`Li2BeF4`.

The dataset registers nine positive-temperature AIMD records.

Each record contains:

- temperature in kelvin;
- cubic cell edge in angstrom;
- reported cell volume in cubic angstrom;
- simulated density in grams per cubic centimeter.

The source metadata identify a 504-atom AIMD supercell.

The source's separate `T0` table entry is retained in the registered metadata.

The AIMD state and experimental state are associated through explicit numerical correspondence records.

## 12. Source Identity and Evidence Classes

The registered reference program distinguishes:

`EXPERIMENTAL`.

`FIRST_PRINCIPLES`.

It also retains source-derived correlations, numerical fixtures, interatomic-model outputs, benchmark results, and executable qualification records through their respective interfaces.

The typed reference-comparison layer uses:

`FLiBeEvidenceKind`.

`FLiBeReferenceObservable`.

`FLiBeReferenceComparison`.

`compare_flibe_experimental_first_principles(...)`.

Each observable binds:

- observable identity;
- physical composition;
- thermodynamic state;
- physical-state identifier;
- evidence kind;
- numerical values;
- units;
- normalization;
- source and method;
- provenance;
- optional sampling axis.

An executable comparison uses its declared state-correspondence conditions before calculating residual metrics.

## 13. Interatomic Reference Observables

The interatomic reference organization connects the selected physical state to numerical and experimental observables.

Its observable families include:

| Observable family | Representative variables |
| --- | --- |
| Electronic | Energy, forces, stress |
| Geometric | Cartesian positions, distances, periodic images |
| Local structural | Coordination and local environments |
| Pair statistical | Radial distribution and pair correlations |
| Reciprocal-space | Structure factors and scattering coordinates |
| Spectroscopic | NMR and local-environment assignments |
| Thermodynamic | Temperature, pressure, density, enthalpy |
| Dynamical | Time correlations, trajectories, diffusion |
| Transport | Viscosity, conductivity, species flux |
| Multiscale | Coarse mass, centroids, constitutive variables |

Each reference observable has an identified unit, physical state, normalization, sampling domain, source, and computational or experimental method.

The corresponding reference and model states are connected through an explicit mapping.

## 14. Directed Interaction Geometry

For a selected atomic configuration, define an interaction graph:

`G = (V, E)`.

A directed edge:

`i → j`

identifies source node `i` and receiving node `j`.

For Cartesian coordinates:

`d_ij = r_j - r_i`.

With periodic boundaries, displacement evaluation uses the declared cell and image convention.

The interaction graph may be constructed from distance cutoffs, neighbor lists, or explicitly provided edges.

Graph topology and atomic geometry remain independently identifiable.

Local structural calculations use the selected graph definition, including direction, periodic images, and multiplicity.

Graph connectivity, chemical bonding, and experimentally inferred coordination retain their respective observable definitions.

## 15. Local Structure and Coordination

The executable coordination interfaces are:

`FLiBeAtomCoordination`.

`FLiBeCoordinationState`.

`build_flibe_coordination_state(configuration, graph)`.

For receiving atom `j` and species `s`, define:

`z_(j,s) = count{(i → j) ∈ E | species(i) = s}`.

The ordered species-resolved coordination vector is:

`z_j = (z_(j,Li), z_(j,Be), z_(j,F))`.

The total graph-relative coordination is:

`z_(j,total) = z_(j,Li) + z_(j,Be) + z_(j,F)`.

A complete coordination state preserves:

- receiving atom index;
- receiver species;
- ordered neighbor counts;
- graph identity;
- source configuration;
- geometric cutoff and periodic-image conditions.

The local-structure chapter additionally defines reference correspondence for Be–F coordination, fluoroberyllate structures, pair distributions, scattering observables, NMR assignments, and dynamic structural environments.

## 16. Structural and Spatial Symmetry

The three-dimensional spatial action is:

`r_i' = Qr_i + b`.

Where:

`Q ∈ O(3)`.

`b ∈ R³`.

For an appropriately transformed physical configuration, scalar energy satisfies:

`E(QR + b) = E(R)`.

Cartesian forces transform as:

`F_i(QR + b) = QF_i(R)`.

A second-order Cartesian tensor follows its declared tensor transformation:

`σ' = QσQ^T`.

The qualification program separately checks atomic permutation consistency and E(3) covariance.

Atomic species, graph indices, tensor representations, and boundary geometry are transformed consistently.

Spatial rotations and ternary polarity transitions belong to different transformation domains.

## 17. FLiBe Resonance Parameterization

The resonance parameterization connects graph-relative atomic coordination with continuous oscillator parameters.

The executable interfaces are:

`FLiBeResonanceParameterization`.

`ConstantFLiBeResonanceParameters`.

`evaluate_resonance_parameters(model, coordination)`.

For a coordination state `C`:

`P_FLiBe(C, λ) = (κ, γ)`.

Where:

`κ = (κ_0, ..., κ_(N-1))`.

`γ = (γ_0, ..., γ_(N-1))`.

The parameterization retains the correspondence between receiving-node coordination and the evaluated coupling and phase-lag vectors.

The evaluator may be constant or coordination-dependent under its explicitly supplied model contract.

The resulting numerical parameters remain associated with source metadata, composition, geometry, and thermodynamic context.

## 18. Continuous Phase Dynamics

The resonance evolution uses a directed Kuramoto–Sakaguchi representation.

For incoming edges `i → j`:

`dθ_j/dt = ω_j + κ_j Σ_(i→j) sin(θ_i - θ_j - γ_j)`.

Here:

`θ_j` is the continuous oscillator phase.

`ω_j` is the intrinsic angular frequency.

`κ_j` is the receiving-node coupling parameter.

`γ_j` is the receiving-node phase lag.

The executable reference includes:

`phase_derivatives(...)`.

`euler_step(...)`.

The oscillator dynamics use their own integration timestep and phase-wrapping convention.

The interaction graph and parameter state are sampled according to an explicitly defined coupling schedule.

Oscillator phase and the physical phase of matter remain separate variables.

## 19. Resonance Descriptor and Regime Representation

A resonance descriptor is constructed from the selected continuous oscillator state and its material context.

The executable FLiBe interface is:

`FLiBeResonanceDescriptor`.

The constructor function is:

`build_flibe_resonance_descriptor(...)`.

For `N >= 1` oscillators, the phase-order parameter is:

`R(t) = |(1/N) Σ_j exp(iθ_j(t))|`.

Its mathematical range is:

`0 <= R(t) <= 1`.

A frequency-spread observable may be associated with the same oscillator state under its declared definition.

The framework retains the following distinctions:

`resonance ≠ frequency equality`.

`resonance ≠ synchronization`.

`synchronization ≠ phase locking`.

`phase locking ≠ resonance`.

`coherence ≠ uniformity`.

`coherence ≠ resonance`.

`R(t) ≠ C(t)`.

Resonance-window membership, stability, bifurcation, and phase-order behavior have their respective mathematical predicates and state domains.

## 20. Continuous-to-Ternary Request Mapping

The FLiBe interpretation layer maps a continuous resonance descriptor to a requested balanced-ternary target.

Its executable interface is:

`FLiBeTernaryInterpretation`.

The interpretation function is:

`interpret_flibe_ternary_target(interpretation, descriptor)`.

For a continuous descriptor with phase order `R_phase` and frequency spread `spread_ω`, define a projection:

`u_R = w_R R_phase + w_ω spread_ω + b`.

The projection weights and bias are supplied parameters.

For ordered thresholds:

`h_negative < h_positive`.

The request mapping is:

| Projection condition | Requested target |
| --- | --- |
| `u_R < h_negative` | `-1` |
| `h_negative <= u_R <= h_positive` | `0` |
| `u_R > h_positive` | `1` |

Both threshold equalities map to the neutral requested target.

The request is subsequently processed through the separately defined ternary execution operator.

## 21. Active Balanced-Ternary Execution

The canonical execution alphabet is:

`T = {-1, 0, 1}`.

The state `0` is the active neutral execution state.

Its functional semantics include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

The execution layer maintains the distinction:

`target ≠ executed state`.

`pending ≠ executed state`.

`pending ≠ active neutral`.

`hold ≠ committed self-transition`.

Direct committed transitions between opposite polarities are excluded by the transition relation.

Permitted opposite-polarity routes are:

`-1 → 0 → 1`.

`1 → 0 → -1`.

Each arrow is one committed execution event.

## 22. Pending Routes, Guards, and Retention

The execution state may contain both:

- retained executed polarity;
- pending destination.

A pending destination is either `-1` or `1`.

For a request from retained `-1` to target `1`:

`(-1, None) → (0, 1)`.

For a request from retained `1` to target `-1`:

`(1, None) → (0, -1)`.

After the corresponding eligible execution opportunity:

`(0, 1) → (1, None)`.

`(0, -1) → (-1, None)`.

A guard may retain the active neutral state for multiple execution opportunities.

The state `0` retains its execution identity while a destination is pending.

The executable operators include:

`execute_ternary_step`.

`execute_ternary_vector_step`.

`propagate_md_ternary_state`.

Invalid, unknown, missing, and nonfinite numerical conditions are represented separately from the active neutral execution state.

## 23. Conditioned Interatomic Energy

The FLiBe TR-EIP specialization is implemented in:

`src/tr_eif/flibe/tr_eip.py`.

The principal model is:

`FLiBeTREIPModel`.

The model evaluation receives:

`configuration, graph, features, resonance, execution`.

The returned result is:

`FLiBeTREIPResult`.

The conditioned interatomic energy may be represented as:

`E = E_λ(R, S, G, z, τ)`.

Where:

`R` denotes Cartesian atomic positions.

`S` denotes atomic species.

`G` denotes interaction geometry.

`z` denotes the continuous resonance descriptor.

`τ` denotes retained executed ternary states.

`λ` denotes the selected model parameters.

The resonance and executed ternary inputs condition the energy computation through their explicitly defined feature interfaces.

The energy remains a continuous scalar quantity.

## 24. Cartesian Forces and Stress

For a differentiable conservative energy functional:

`F_i = -∇_(r_i) E`.

The force-evaluation procedure specifies whether the graph, features, resonance descriptor, and execution state are held fixed or updated during differentiation.

The reference numerical implementation includes:

`ConservativeForceEvaluator`.

For a Cartesian coordinate perturbation `h > 0`, central differences have the form:

`F_(i,a) ≈ -[E(r_(i,a) + h) - E(r_(i,a) - h)] / (2h)`.

For homogeneous strain `ε` and reference volume `V`, the stress convention is:

`σ_ab = (1/V) ∂E/∂ε_ab`.

The corresponding reference implementation includes:

`ConservativeStressEvaluator`.

Energy, force, and stress qualification records include numerical differentiation settings, selected physical variables, units, geometric transformations, and comparison tolerances.

## 25. Molecular-Dynamics Evolution

The molecular-dynamics layer represents atomic positions and velocities:

`R(t) = (r_0(t), ..., r_(N-1)(t))`.

`V(t) = (v_0(t), ..., v_(N-1)(t))`.

The governing mechanical equations are:

`dr_i/dt = v_i`.

`m_i dv_i/dt = F_i`.

The reference mechanical integrator includes:

`velocity_verlet_step(...)`.

Trajectory construction includes:

`run_velocity_verlet_trajectory(...)`.

A mechanical computation specifies:

- initial atomic positions;
- initial velocities;
- atomic masses;
- potential and force evaluator;
- timestep;
- periodic boundary conditions;
- interaction graph updates;
- thermal and pressure controls when selected;
- trajectory sampling;
- applicable physical exchanges.

The resonance and ternary operators have their own integration and execution schedules.

## 26. Mechanical Energy and Open-System Balances

For fixed atomic inventory:

`K = (1/2) Σ_i m_i |v_i|²`.

The total mechanical energy is:

`H = K + E`.

For a closed conservative fixed-Hamiltonian interval, the discrete energy residual is:

`ΔH_n = H_n - H_0`.

For an open system, the energy balance includes applicable heat, mechanical work, material exchange, and imposed state changes.

A signed integral balance can be represented as:

`H(t_1) - H(t_0) = Q + W + E_exchange + R_balance`.

The balance terms retain their declared orientations and sign conventions.

`R_balance` is the recorded residual of the selected accounting procedure.

Mass, species, momentum, and energy balances are identified separately.

Thermal and mechanical boundary events remain associated with their respective numerical and physical source records.

## 27. Material Transport Observables

The FLiBe transport layer organizes species-resolved and continuum transport quantities.

For species `s`, the three-dimensional Einstein self-diffusion relation is:

`D_s = lim_(t→∞) MSD_s(t) / (6t)`.

The molecular-dynamics layer includes:

`mean_squared_displacement(...)`.

`velocity_autocorrelation(...)`.

The transport program distinguishes:

- Li self-diffusion;
- Be self-diffusion;
- F self-diffusion;
- collective diffusion;
- species-resolved flux;
- dynamic viscosity;
- kinematic viscosity;
- thermal conductivity;
- electrical conductivity.

A transport record identifies its species, physical state, temperature, pressure, composition, statistical estimator, unit, and sampling domain.

Green–Kubo and Einstein estimators use their corresponding time-correlation and long-time-limit definitions.

## 28. Hydrogen-Isotope Transport

The FLiBe source organization separately represents transport associated with hydrogen isotopes.

The isotope identities are:

`H`.

`D`.

`T`.

The relevant physical observables include:

- diffusion;
- solubility;
- permeability;
- isotope-bearing species concentration;
- transport flux;
- interface and membrane conditions.

For a steady one-dimensional solution–diffusion model under its stated assumptions:

`J_h = (D_h S_h / L)(p_1 - p_2)`.

The associated permeability convention is:

`P_h = D_h S_h`.

The transport model retains the effective thickness, boundary partial pressures, material-state conditions, species identity, and units.

The registered source organization includes deuterium-transport and tritium-permeation publications with their own experimental conditions and source metadata.

## 29. Multiscale Material Architecture

The FLiBe multiscale realization connects:

`electronic reference → interatomic model → atomistic state → structural coarse state → mesoscale closure → continuum closure → engineering boundaries`.

Each scale has a state space and declared mapping context.

For state spaces `X_l` and `X_m`, a scale transformation has the form:

`M_(l→m): X_l × C_(l→m) → X_m`.

Here `C_(l→m)` contains the mapping parameters, source identities, assumptions, and applicable physical state.

The current FLiBe structural interface is:

`FLiBeMultiscaleCoolantModel`.

Its principal builder is:

`build_flibe_multiscale_coolant_state(...)`.

Structural coarse-graining uses explicitly configured partitions and species mass parameters.

## 30. Mass-Weighted Structural Reduction

Let `I_c` denote the fine-level atom indices belonging to coarse group `c`.

Define coarse mass:

`M_c = Σ_(i∈I_c) m_i`.

For `M_c > 0`, the mass-weighted Cartesian centroid is:

`R_c = [Σ_(i∈I_c) m_i r_i] / M_c`.

For a complete partition of fixed atomic inventory:

`Σ_c M_c = Σ_i m_i`.

For a rigid transformation:

`r_i' = Qr_i + b`.

The corresponding centroid transformation is:

`R_c' = QR_c + b`.

The multiscale hierarchy preserves its ordered membership definitions and compatible adjacent level cardinalities.

Periodic configurations use the declared position-unwrapping convention before geometric reduction.

## 31. Deterministic FLiBe Multiscale Reference

The existing FLiBe multiscale integration fixture contains seven atoms:

`S = (Li, Li, Be, F, F, F, F)`.

The fixture assigns mass parameters:

`m_Li = 2.0`.

`m_Be = 3.0`.

`m_F = 5.0`.

The first partition is:

`p_0 = (0, 0, 1, 1, 2, 2, 2)`.

The second partition is:

`p_1 = (0, 0, 0)`.

The hierarchy is:

`7 → 3 → 1`.

The first coarse masses are:

`M_0 = 4.0`.

`M_1 = 8.0`.

`M_2 = 15.0`.

The final mass is:

`M_final = 27.0`.

The final centroid is:

`R_final = (7/9, 2/3, 10/27)`.

These quantities belong to the registered deterministic test fixture and retain its assigned mass and coordinate units.

The corresponding test is:

`tests/integration/test_flibe_multiscale_coolant_closure.py`.

## 32. Mesoscale, Continuum, and Engineering Transfer

The FLiBe hierarchy connects structural coarse states with the generic multiscale provider interfaces.

These include:

`evaluate_mesoscale_closure(...)`.

`evaluate_continuum_closure(...)`.

`evaluate_transport_coefficient_transfer(...)`.

`evaluate_thermodynamic_consistency(...)`.

`evaluate_uncertainty_propagation(...)`.

`evaluate_engineering_boundaries(...)`.

Each provider has its own input state, output state, source and destination scale identities, and mapping context.

For continuum mass density `ρ`, velocity `u`, and source `s_m`:

`∂ρ/∂t + div(ρu) = s_m`.

For species concentration `c_s`, diffusive flux `j_s`, and source `q_s`:

`∂c_s/∂t + div(c_su + j_s) = q_s`.

Engineering boundary records associate continuum variables with selected geometry, loads, transport conditions, and external exchanges.

The mapping chain preserves source and target variable identities throughout the scale hierarchy.

## 33. Thermodynamic Consistency and Uncertainty Transfer

Thermodynamic consistency is represented through explicit relations between registered state variables and mapped quantities.

For a differentiable mapping:

`y = f(x)`.

Let:

`J = ∂f/∂x`.

For input covariance `C_x`, first-order covariance propagation is:

`C_y ≈ JC_xJ^T`.

A transfer record identifies:

- source uncertainty;
- covariance convention;
- transformation;
- source and target scales;
- physical-state correspondence;
- numerical method;
- source provenance.

Transport and thermodynamic parameters retain their units and state-domain identities.

Correlations shared between samples, measurements, and model parameters are included according to the declared covariance model.

## 34. Experimental and Numerical State Correspondence

The Volume 07 validation program establishes correspondence between source observations and model outputs.

A comparison state may contain:

`X = (composition, T, P, material_state, observable, normalization, sampling_domain)`.

The comparison operation requires compatible definitions for the variables relevant to the selected observable.

The registered density sources have distinct composition definitions:

- exact `2 LiF : 1 BeF2`;
- nominal `67:33 mol%`;
- measured `33.58(5) mol% BeF2`.

Temperature-screened source comparisons retain this composition information.

The executable density procedures include:

`experimental_density_cross_source_diagnostic.py`.

`experimental_aimd_density_cross_source_diagnostic.py`.

The former evaluates the registered density correlation against selected experimental measurements.

The latter evaluates AIMD density records against within-run experimental interpolation at corresponding temperatures.

Each procedure preserves source identities, selected samples, residual definitions, numerical metrics, and applicable source-state information.

## 35. Numerical Comparison Metrics

For matched reference values `y_i^(ref)` and calculated values `y_i^(calc)`, define:

`r_i = y_i^(calc) - y_i^(ref)`.

For `N >= 1` observations:

`Bias = (1/N) Σ_i r_i`.

`MAE = (1/N) Σ_i |r_i|`.

`RMSE = sqrt[(1/N) Σ_i r_i²]`.

`E_max = max_i |r_i|`.

The selected sign convention, sample grouping, unit, normalization, and weighting procedure are recorded with each result.

A numerical acceptance relation may be written:

`|y_calc - y_ref| <= δ_abs + δ_rel |y_ref|`.

The tolerances are specified by the individual mathematical or numerical qualification contract before execution.

Exact categorical invariants use exact equality.

## 36. Registered Cross-Source Density Results

The experimental–correlation procedure selects 39 observations from the 61 registered Vidrio density measurements under its temperature-screening contract.

Its recorded metrics are:

| Metric | Value, kg/m³ |
| --- | ---: |
| Mean absolute residual | `8.0768307692` |
| Root mean square residual | `11.3200522371` |
| Maximum absolute residual | `24.2572` |

The experimental–AIMD procedure evaluates three AIMD temperatures:

`750 K`.

`850 K`.

`1000 K`.

Within-run experimental interpolation produces nine paired residuals.

The registered numerical metrics are:

| Metric | Value, kg/m³ |
| --- | ---: |
| Mean signed residual | `-273.7386067518` |
| Mean absolute residual | `273.7386067518` |
| Root mean square residual | `273.8555291548` |
| Minimum signed residual | `-285.30625` |
| Maximum signed residual | `-260.1731481481` |

These records preserve the comparison method and source-state coordinates.

The independently registered interatomic-model output is evaluated through its own specified reference-state correspondence.

## 37. Mathematical and Execution Invariants

Volume 07 inherits the framework invariants and specializes their qualification to the FLiBe material state.

| Domain | Invariant or relation | Qualification |
| --- | --- | --- |
| Species | `S_i ∈ {Li, Be, F}` | Exact |
| Atomic cardinality | Species and positions have equal count | Exact |
| Binary composition | `x_LiF + x_BeF2 = 1` | Declared numerical representation |
| Formal charge | `Q_formal = N_Li + 2N_Be - N_F` | Exact integer |
| Directed graph | Node identity and edge orientation | Exact |
| Local coordination | Incoming species-count definition | Exact |
| Ternary alphabet | `{-1, 0, 1}` | Exact |
| Pending destination | `{-1, 1}` or absent | Exact |
| Execution transitions | Permitted committed relation | Exact |
| Active-neutral routing | Opposite polarities pass through `0` | Exact |
| Energy | Scalar invariance under applicable E(3) action | Numerical |
| Force | Cartesian covariance | Numerical |
| Stress | Tensor covariance | Numerical |
| Force derivative | `F_i = -∇_(r_i) E` | Numerical |
| Coarse mass | `Σ_c M_c = Σ_i m_i` | Numerical reduction |
| Coarse centroid | Mass-weighted Cartesian mapping | Numerical |
| Determinism | Repeated evaluation under identical inputs | Declared replay comparison |
| Source correspondence | Required typed state coordinates | Exact structural and numerical |

A mathematical invariant is evaluated under its corresponding assumptions and data domain.

## 38. Coupled Time Schedules

The FLiBe computation maintains separate event schedules for:

1. Mechanical integration.
2. Resonance integration.
3. Interaction graph updates.
4. Resonance descriptor sampling.
5. Ternary request generation.
6. Ternary execution opportunities.
7. Thermodynamic control events.
8. Multiscale sampling.
9. Engineering boundary updates.

Define the event-time sequences:

`t_MD[n]`.

`t_R[k]`.

`t_T[m]`.

`t_MS[p]`.

The coupling schedule defines the state sampled at each event and the ordering of coincident operations.

The mechanical operator uses the retained executed ternary state associated with its declared evaluation time.

The resonance operator uses its selected graph and receiving-node parameters.

The ternary operator processes requested targets through retained state, pending destination, and guard conditions.

The recorded event sequence permits deterministic reconstruction of the coupled numerical evolution.

## 39. Reproducibility Contract

A complete FLiBe computation record contains:

1. Repository revision.
2. Executable package version.
3. Source-dataset identifiers.
4. Dataset file fingerprints.
5. Material composition.
6. Ordered atomic species.
7. Initial atomic geometry.
8. Thermodynamic state.
9. Periodic boundary conditions.
10. Interaction graph construction.
11. Interatomic-model parameters.
12. Resonance parameterization.
13. Initial oscillator state.
14. Numerical phase-integration settings.
15. Ternary projection parameters.
16. Initial retained and pending states.
17. Execution guards and schedules.
18. Mechanical integration parameters.
19. Thermal and pressure-control settings.
20. Multiscale hierarchy and providers.
21. Numerical precision.
22. Statistical sampling parameters.
23. Predeclared acceptance criteria.
24. Raw numerical observables.
25. Comparison metrics.
26. Uncertainty records.
27. Test identities and execution results.
28. CI and execution-environment identifiers.

The reproducibility record preserves the correspondence between source data, transformations, executable calculations, and numerical outputs.

## 40. Executable Interface Register

The FLiBe-specific executable package is:

`src/tr_eif/flibe/`.

Its principal components are:

| Component | File |
| --- | --- |
| Species | `species.py` |
| Composition | `composition.py` |
| Configuration | `configuration.py` |
| Formal charge | `charge.py` |
| Atomic mass | `mass.py` |
| Thermodynamic state | `thermodynamic_state.py` |
| Physical parameters and provenance | `units.py` |
| Density operators | `density.py` |
| Reference comparison | `reference_comparison.py` |
| Dataset configuration | `dataset_configuration.py` |
| Atomic coordination | `coordination.py` |
| Resonance parameterization | `resonance_parameterization.py` |
| Resonance descriptor | `resonance_descriptor.py` |
| Ternary interpretation | `ternary_interpretation.py` |
| FLiBe TR-EIP specialization | `tr_eip.py` |
| Multiscale coolant model | `multiscale_coolant.py` |

The FLiBe-specific interfaces compose with existing generic implementations under:

`src/tr_eif/resonance/`.

`src/tr_eif/ternary/`.

`src/tr_eif/energy/`.

`src/tr_eif/md/`.

`src/tr_eif/multiscale/`.

`src/tr_eif/observables/`.

The model-specific and framework-generic components retain their corresponding type and operator boundaries.

## 41. Reference Data Register

The executable primary-source datasets are:

| Dataset | Evidence kind | Registered source |
| --- | --- | --- |
| `flibe_vidrio_2022_density_measurements.json` | Experimental | Vidrio et al. 2022 |
| `flibe_baral_2021_aimd_density.json` | First-principles | Baral et al. 2021 |

Both reside under:

`data/reference/`.

The source organization additionally includes registered literature metadata for thermodynamic, structural, and transport observables in the corresponding technical chapters.

The source registry distinguishes:

- publication metadata;
- physical measurement;
- first-principles calculation;
- registered numerical dataset;
- model prediction;
- numerical comparison;
- test fixture;
- executable qualification.

Each source-supported observable retains its state coordinates and provenance through the selected computational transformation.

## 42. FLiBe Benchmark Register

The existing FLiBe benchmark directory is:

`benchmarks/flibe/`.

The registered executable benchmark programs are:

| Benchmark | File |
| --- | --- |
| Correctness | `reference_correctness.py` |
| Equivariance | `reference_equivariance.py` |
| Conservation | `reference_conservation.py` |
| Numerical convergence | `reference_numerical_convergence.py` |
| Property reproduction | `reference_property_reproduction.py` |
| Scaling | `reference_scaling.py` |
| Memory | `reference_memory.py` |
| Runtime | `reference_runtime.py` |
| Experimental–correlation comparison | `experimental_density_cross_source_diagnostic.py` |
| Experimental–AIMD comparison | `experimental_aimd_density_cross_source_diagnostic.py` |

Each benchmark is associated with its explicit inputs, numerical method, physical or computational observable, and output metrics.

Correctness, numerical convergence, resource measurement, and source comparison are separately identified qualification categories.

## 43. Test and CI Integration

The existing test architecture includes:

`tests/invariants/`.

`tests/integration/`.

`tests/determinism/`.

`tests/equivariance/`.

`tests/conservation/`.

`tests/numerical/`.

The FLiBe-specific tests cover:

- composition and formal charge;
- atomic configuration and mass;
- thermodynamic state and density;
- source-data registration;
- reference comparison;
- dataset separation;
- local coordination;
- resonance parameterization;
- resonance descriptors;
- ternary interpretation and execution;
- conditioned interatomic evaluation;
- molecular dynamics;
- structural multiscale mapping;
- cross-scale transfer and closure.

The principal CI workflow files are:

`.github/workflows/python-tests.yml`.

`.github/workflows/schema-validation.yml`.

Each CI result is associated with its specific repository revision, selected checks, and execution record.

## 44. Relationship to Volumes 01–06

Volume 07 composes mathematical and executable foundations established by the preceding volumes.

| Volume | Contribution to the FLiBe realization |
| --- | --- |
| 01 — Mathematical Foundations | State spaces, operators, mappings, axioms, invariants |
| 02 — Ternary Resonance Theory | Phase dynamics, resonance regimes, active neutral, execution routes |
| 03 — Equivariant Interatomic Framework | Atomic geometry, graph representations, energy, forces, stress |
| 04 — Learning and Optimization | Dataset organization, loss construction, constraints, parameter optimization, uncertainty |
| 05 — Molecular Dynamics | Equations of motion, numerical integrators, boundaries, trajectories, transport |
| 06 — Multiscale Materials Modeling | Scale hierarchy, structural reduction, closures, balances, transfer |
| 07 — FLiBe Reference Model | Material composition, source data, specialized operators, reference comparisons, validation |

The common computational state preserves the distinctions between continuous variables, categorical execution, physical material state, and validation metadata.

The mathematical and executable dependencies are identified through their corresponding interfaces rather than inferred from shared terminology.

## 45. Integrated FLiBe State Representation

A coupled FLiBe state may be represented schematically as:

`X_FLiBe = (S, R, V, B, X_thermo, G, C, Θ, P_R, D_R, X_T, X_MS, X_boundary)`.

Where:

`S` — ordered atomic species.

`R` — Cartesian atomic positions.

`V` — Cartesian atomic velocities.

`B` — cell and periodic-boundary state.

`X_thermo` — thermodynamic state.

`G` — directed interaction graph.

`C` — local coordination state.

`Θ` — continuous oscillator state.

`P_R` — resonance parameter state.

`D_R` — continuous resonance descriptor.

`X_T` — retained, requested, pending, and guarded ternary execution state.

`X_MS` — multiscale state and hierarchy.

`X_boundary` — physical exchange and engineering boundary variables.

The state tuple is a mathematical composition of the corresponding typed domains.

Its event-driven evolution is specified through distinct operators:

`Φ_MD` — mechanical evolution.

`Φ_R` — continuous resonance evolution.

`Φ_T` — balanced-ternary execution.

`Φ_MS` — multiscale mapping and transfer.

The coupled evolution is determined by the declared ordering, sampling, and parameter-update rules.

## 46. Integrated Observable Representation

Let an observable operator be:

`O_a: X_FLiBe × C_a → Y_a`.

Where:

`C_a` is the observable-specific context.

The output space `Y_a` may represent:

- scalar energy;
- Cartesian force vectors;
- stress tensors;
- density;
- thermodynamic derivatives;
- pair distributions;
- local coordination;
- phase-order parameters;
- resonance-region classifications;
- discrete execution traces;
- trajectory correlations;
- transport coefficients;
- coarse-state variables;
- continuum fluxes;
- boundary-response quantities.

Each observable retains its dimensional, geometric, thermodynamic, temporal, and provenance context.

The corresponding validation relation connects it to an independently identified reference or mathematical invariant through the procedure defined in Chapter 10.

## 47. Volume Integration

Volume 07 establishes the FLiBe specialization of TR-EIF through an ordered combination of material chemistry, three-dimensional structure, thermodynamic state, continuous resonance, active balanced-ternary execution, conservative interatomic modeling, molecular dynamics, transport, and multiscale transformations.

Its integrated computational sequence is:

`material identity and composition`

`→ ordered atomic configuration`

`→ thermodynamic and geometric state`

`→ directed interaction graph and coordination`

`→ continuous resonance parameterization`

`→ continuous phase dynamics and resonance descriptor`

`→ explicit balanced-ternary request`

`→ guarded active-neutral execution`

`→ retained execution-conditioned interatomic energy`

`→ Cartesian forces and stress`

`→ molecular-dynamics evolution`

`→ structural and transport observables`

`→ multiscale state and constitutive transfer`

`→ source-resolved comparison and reproducible qualification`.

The resulting state, operator, observable, and provenance records connect the FLiBe material realization with the mathematical, dynamical, equivariant, numerical, and multiscale architecture of TR-EIF.

The eleven chapters of Volume 07 form the complete documented FLiBe reference-model volume.
