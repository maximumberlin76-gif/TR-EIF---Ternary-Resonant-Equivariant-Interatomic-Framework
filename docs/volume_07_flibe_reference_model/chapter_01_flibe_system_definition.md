
# FLiBe System Definition

## 1. Scope and System Class

This chapter defines the LiF–BeF2 material system represented by the FLiBe specialization of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF). It establishes the chemical inventory, composition coordinates, thermodynamic state, three-dimensional atomic configuration, mechanical and transport variables, open-system boundary, and coupling to continuous resonance and balanced-ternary execution.

The selected physical system is represented as an open nonlinear dissipative dynamical system with explicit atomistic, thermodynamic, and boundary-state variables. A material realization specifies its composition, spatial and temporal domains, applicable material state, constitutive parameters, and measurement or computational provenance.

The principal state chain is:

`LiF–BeF2 composition → atomic configuration → thermodynamic and boundary state → interaction geometry → conditioned interatomic energy and forces → trajectory and observables`.

Continuous resonance evolution and retained `-1/0/1` execution are coupled by separately identified operators and sampling times.

## 2. Material Identity and Chemical Species

The FLiBe domain represents mixtures in the binary lithium fluoride–beryllium fluoride system, with component formula units `LiF` and `BeF2`. The supported atomic species in `FLiBeSpecies` are:

| Symbol | Species identifier | Formal ionic charge |
| --- | --- | ---: |
| `Li` | `FLiBeSpecies.LITHIUM` | `1` |
| `Be` | `FLiBeSpecies.BERYLLIUM` | `2` |
| `F` | `FLiBeSpecies.FLUORINE` | `-1` |

`FLIBE_SPECIES` fixes the canonical species order as Li, Be, F. `validate_flibe_species_sequence` converts a nonempty tuple of exact species symbols into the corresponding enumeration values while preserving atom order.

Formal ionic charges are stored through `FLIBE_FORMAL_CHARGES`. Their role is the defined species-level formal-charge accounting of the configuration. The interatomic energy, Cartesian forces, oscillator phases, and executed ternary states have their own parameter and state definitions.

## 3. Binary Composition Coordinates

Let `n_LiF >= 0` and `n_BeF2 >= 0` be amounts of LiF and BeF2 formula units, with `n_LiF + n_BeF2 > 0`. Define the normalized binary composition:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

Therefore:

`x_LiF + x_BeF2 = 1`.

`FLiBeComposition(lif_fraction, bef2_fraction)` normalizes two supplied finite nonnegative values to these formula-unit fractions. Its `formula_unit_amounts(total_formula_units)` and `atomic_amounts(total_formula_units)` methods expose the corresponding component and species amounts.

The resulting atomic amounts are:

`n_Li = n_LiF`.

`n_Be = n_BeF2`.

`n_F = n_LiF + 2 n_BeF2`.

## 4. Exact Two-to-One Reference Composition

For the exact formula-unit ratio `2 LiF : 1 BeF2`:

`x_LiF = 2/3`.

`x_BeF2 = 1/3`.

The associated stoichiometric formula is `Li2BeF4`, with the atom-count ratio:

`N_Li : N_Be : N_F = 2 : 1 : 4`.

The corresponding atomic fractions are:

`a_Li = 2/7`, `a_Be = 1/7`, `a_F = 4/7`.

The executable helper `eutectic_flibe_composition()` returns this normalized two-to-one formula-unit composition. Phase-equilibrium compositions and invariant-point conditions are recorded separately using the selected experimental phase-diagram source.

The nominal mixture `67 mol% LiF : 33 mol% BeF2` uses decimal composition fractions `0.67` and `0.33`. The exact two-to-one reference uses the rational values `2/3` and `1/3`. Source records retain their original declared composition and precision.

## 5. Composition and Atomic Fractions

For normalized component fractions `x_LiF` and `x_BeF2`, the mean number of atoms per mixture formula unit is:

`n_atoms = 2 x_LiF + 3 x_BeF2`.

The resulting species atomic fractions are:

`a_Li = x_LiF / n_atoms`.

`a_Be = x_BeF2 / n_atoms`.

`a_F = (x_LiF + 2 x_BeF2) / n_atoms`.

These are the relations implemented by the `lithium_fraction`, `beryllium_fraction`, `fluorine_fraction`, and `atomic_fractions` properties of `FLiBeComposition`.

Chemical composition, discrete atom counts, isotope selection where applicable, and numerical particle inventory remain identifiable in the material-state record.

## 6. Three-Dimensional Atomic Configuration

The underlying `AtomicConfiguration` stores an ordered tuple of species symbols and one Cartesian position `r_i in R^3` per atom. It also stores an optional three-vector simulation cell and three periodic-axis flags.

`FLiBeConfiguration(configuration)` associates that general atomistic state with the canonical Li, Be, F species domain. It provides `atom_count`, canonical `species`, `species_counts`, and `atomic_fractions` derived from the discrete atom inventory.

The method `FLiBeConfiguration.composition()` derives LiF–BeF2 formula-unit fractions from the integer Li and Be counts under the exact stoichiometric condition:

`N_F = N_Li + 2 N_Be`.

The method also requires `N_Li + N_Be > 0`. `matches_composition` compares the derived component fractions with a supplied `FLiBeComposition` using an explicitly provided finite nonnegative absolute tolerance; its default is zero.

The configuration includes its spatial domain and atom ordering. A trajectory records any material-inventory or boundary changes at the instants defined by the selected physical model.

## 7. Formal Charge Accounting

For a configuration with species counts `N_Li`, `N_Be`, and `N_F`, the total formal ionic charge in elementary-charge units is:

`Q_formal = N_Li + 2 N_Be - N_F`.

Under the binary formula-unit relation of Section 6:

`Q_formal = 0`.

`configuration_formal_charges`, `total_formal_charge`, `is_formally_neutral`, and `build_formal_charge_state` evaluate and record these quantities. `FormalChargeState` retains the ordered per-atom charges and their sum.

Formal charge and balanced-ternary execution occupy separate types. An executed value of `-1`, `0`, or `1` is supplied by the execution layer and retains its routing and control semantics.

## 8. Thermodynamic State and Material-State Domain

`FLiBeThermodynamicState(temperature, pressure)` stores:

`T > 0`, expressed in kelvin.

`P >= 0`, expressed in pascal.

Both values are finite real numbers. `with_temperature` and `with_pressure` return a new state with one replaced thermodynamic coordinate and the other retained.

A material-state record additionally identifies the selected composition, phase or structural region, source or model state definition, and external conditions. Phase equilibria and liquidus boundaries use the experimentally identified composition–temperature–pressure domain of the selected source.

The atomistic oscillator phases, thermodynamic variables, and physical phase or structural organization are represented through separately identified state quantities and mappings.

## 9. Geometric and Mechanical Variables

For atom `i`, let `m_i > 0`, `r_i(t) in R^3`, and `v_i(t) in R^3` denote mass, position, and velocity. On a fixed-inventory integration interval:

`d r_i/dt = v_i`.

`m_i d v_i/dt = F_i`.

`FLiBeMassParameters` supplies positive finite atomic-mass values by species; `configuration_masses` constructs the mass tuple in configuration order, and `total_configuration_mass` sums it.

For periodic geometry with cell matrix `B = [a b c]`, cell volume is:

`V_cell = |det(B)|`.

The interaction graph is built using the selected cutoff and geometric image convention. Its directed edges carry source, receiver, and periodic-image indices.

## 10. Open-System Inventory and Exchange

A selected region `Omega(t)` defines the subsystem boundary for matter, momentum, energy, and external controls. For species concentration `c_s`, material velocity `u`, diffusive flux `j_s`, and volumetric source `q_s`, the local species balance is:

`partial_t c_s + div(c_s u + j_s) = q_s`.

For a fixed control region with outward unit normal `n`, the integral balance is:

`d/dt integral_Omega c_s dV = -integral_(partial Omega) (c_s u + j_s) · n dA + integral_Omega q_s dV`.

Thermal flux, mechanical work, species exchange, and time-dependent boundary geometry are represented by their declared physical operators. A fixed-inventory atomic integration step retains its own particle cardinality and source mechanical state until the selected inventory-update event.

## 11. Interaction Geometry and Local Coordination

`build_cutoff_graph` constructs a directed atomic interaction graph from the supplied configuration and cutoff. The species-resolved coordination operator receives the validated `FLiBeConfiguration` and an `InteractionGraph` with matching node count.

For receiving atom `j` and species `s`, define the graph coordination count:

`z_(j,s) = count{i → j in G | species(i) = s}`.

`build_flibe_coordination_state` produces `FLiBeAtomCoordination` records with Li, Be, and F incoming-neighbor counts. `FLiBeCoordinationState` stores those records in contiguous atomic index order.

The graph-selection rule, cutoff, cell geometry, periodic images, and sampling time determine the resulting coordination descriptor. Material structural observables use their own declared experimental or computational extraction procedures.

## 12. Interatomic Energy and Conservative Forces

For configuration `X`, graph `G`, node features `Q`, retained ternary execution `sigma`, and model parameters `Theta`, the TR-EIP energy is represented by:

`E_pot = E_Theta(X, G, Q, sigma)`.

For a differentiable branch with the selected conditioning inputs fixed during coordinate differentiation:

`F_i^cons = -grad_(r_i) E_pot`.

Cell-strain derivatives define stress under the selected cell-volume and sign convention. The energy and its derivatives are evaluated by the framework's invariant/equivariant interatomic operators.

The FLiBe specialization `FLiBeTREIPModel` accepts an `FLiBeConfiguration`, interaction graph, feature vector, `FLiBeResonanceDescriptor`, and retained `TernaryExecutionVector`. The returned `FLiBeTREIPResult` binds these inputs to the conditioned features and scalar-energy result.

## 13. Continuous Resonance Dynamics

An atom-associated resonance state retains one oscillator phase `theta_j` and intrinsic angular frequency `omega_j` per atom. For receiving-node coupling `kappa_j` and phase lag `gamma_j`, the graph-based Kuramoto–Sakaguchi equation is:

`d theta_j/dt = omega_j + kappa_j sum_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

`FLiBeResonanceParameterization` and `ConstantFLiBeResonanceParameters` supply typed `PhaseDynamicsParameters` under their selected provenance. `FLiBeResonanceDescriptor` binds the resonance state to the configuration, graph-relative coordination, thermodynamic state, and source metadata.

The continuous descriptor exposes phase order and intrinsic-frequency spread. `append_flibe_resonance_channels` appends these two scalar channels, in that order, to each node's existing feature channels for the FLiBe TR-EIP energy evaluation.

## 14. Balanced-Ternary Execution

The executed state alphabet is `-1/0/1`, with `0` as active neutral. A retained execution node stores `sigma_i in {-1, 0, 1}` and an optional pending destination `p_i in {-1, 1} or None` satisfying:

`p_i != None implies sigma_i = 0`.

Opposite-polarity routes use separate committed events:

`-1 → 0 → 1`.

`1 → 0 → -1`.

Requests, retained values, pending destinations, guarded holds, and committed legs are represented by their respective fields. Active neutral supports its defined balancing, routing, damping, mediation, transition staging, retention, and controlled-neutralization functions.

`FLiBeTernaryInterpretation` maps selected continuous resonance descriptors to requested targets through a projection and thresholds. The execution operator processes these requests and supplies the retained execution vector used for energy conditioning.

## 15. Coupled Mechanical, Resonance, and Execution Schedule

Let `n` index mechanical steps, `j` resonance integration steps, and `k` ternary execution opportunities. A declared coupling schedule may use:

`X_MD[n+1] = Phi_MD(X_MD[n]; dt_MD, sigma[k])`.

`X_R[j+1] = Phi_R(X_R[j]; dt_R, G_sample)`.

`request[k] = M_request(X_R, X_MD, context)`.

`X_T[k+1] = U_exec(X_T[k], request[k], guards[k])`.

`sigma[k+1] = retained(X_T[k+1])`.

The selected schedule identifies graph sampling, resonance integration, execution-commit instants, force evaluations, thermal coupling, and boundary exchanges. Mechanical time and execution-event indices are recorded separately.

## 16. Thermophysical Property Interfaces

`FLiBeDensityModel` evaluates a source-identified density provider at one `FLiBeThermodynamicState`. `ConstantFLiBeDensity` evaluates a declared constant value on the supplied typed state. `evaluate_density` returns a positive finite `PhysicalParameter` with unit `kg/m^3`.

The FLiBe unit enumeration includes `K`, `Pa`, `u`, and `kg/m^3`. `PhysicalParameter` retains the numerical value, typed unit, provenance class, and optional source identifier.

For a fixed mass inventory and a defined physical volume:

`rho = M_total / V`.

A density evaluation and a cell-derived density are identified by their respective model or geometrical calculation context. Additional material observables, including enthalpy, heat capacity, viscosity, and conductivity, use their individual property definitions, state domains, units, and source records.

## 17. Experimental Reference Dataset

The repository contains `data/reference/flibe_vidrio_2022_density_measurements.json`, sourced to Vidrio et al., *Journal of Chemical & Engineering Data* (2022), DOI `10.1021/acs.jced.2c00212`.

The file registers 61 density measurements from four experimental runs `0A`, `1A`, `1B`, and `1C`. Each record contains temperature in degrees Celsius, its reported standard uncertainty, density in `kg/m^3`, and its reported standard uncertainty.

The source identifies nominal composition `2 LiF : 1 BeF2` and an ICP-MS measured BeF2 fraction of `33.58(5) mol%`. The record also includes reported pressure, composition metadata, experimental method, and source locations for its measurements.

These data are retained with their experimental sampling and uncertainty definitions for source-to-model observable calculations.

## 18. First-Principles Reference Dataset

The repository contains `data/reference/flibe_baral_2021_aimd_density.json`, sourced to Baral et al., *ACS Omega* (2021), DOI `10.1021/acsomega.1c02528`.

Its nine registered AIMD table rows contain temperature in kelvin, cubic-cell edge in angstroms, cell volume in cubic angstroms, and calculated density in `g/cm^3`. The material record identifies `Li2BeF4` with an exact `2 LiF : 1 BeF2` formula-unit ratio and a reported 504-atom simulation supercell.

The experiment and first-principles records carry their composition, temperature, method, units, and source provenance through distinct dataset identifiers. Numerical comparisons select the declared source-to-target state correspondence and observable transformation.

## 19. Phase-Equilibrium and Property Sources

`docs/references/flibe_sources.md` registers the primary scientific sources and their property domains. The composition and phase-equilibrium register includes Roy, Roy, and Osborn (1950, 1954) and Romberger, Braunstein, and Thoma (1972). The thermophysical register includes Cantor, Ward, and Moynihan (1969), Douglas and Payne (1969), and additional source-specific records.

The Janz et al. (1974) reference-data compilation is registered for a temperature-dependent density correlation with its stated composition and temperature interval. Individual experimental measurements, first-principles outputs, source-derived correlations, and model calculations retain their identified source and method classes.

The selected property record defines the corresponding physical state, composition, measurement or calculation procedure, units, and uncertainty metadata.

## 20. Transport and Material Evolution

For atomic positions `r_i(t)` and velocities `v_i(t)`, the MD transport layer exposes single-origin mean-squared displacement and velocity autocorrelation series. For a selected species and an applicable stationary isotropic diffusive regime, a self-diffusion relation is:

`D_self = lim_(tau→infinity) MSD(tau) / (6 tau)`.

The corresponding Green–Kubo relation is:

`D_self = (1/3) integral_(0→infinity) C_v(tau) d tau`.

A transport record declares its transported species, physical state, ensemble or open-system conditions, time origins, coordinate reconstruction, fitting or integration interval, and numerical uncertainty procedure. Li, Be, and F self-diffusion coefficients and any additional transported species are indexed by their respective observable and species definitions.

## 21. Multiscale Material Representation

`FLiBeMultiscaleCoolantModel` combines `FLiBeMassParameters` with `MultiscaleHierarchy`. Its `build_state` operation maps species masses and selected Cartesian fine positions into a `MultiscaleStateHierarchy`.

For coarse group `c` with fine member set `I_c`:

`M_c = sum_(i in I_c) m_i`.

`R_c = (1/M_c) sum_(i in I_c) m_i r_i`.

Periodic configurations supply explicit fine-position coordinates selected under the declared unwrapping and cell reference convention. The resulting coarse state provides typed structural inputs to mesoscale, continuum, transport, thermodynamic, uncertainty, and engineering-boundary mappings.

## 22. Dataset Roles and Provenance

`FLiBeDatasetConfiguration` stores a sample identifier, configuration identifier, `FLiBeConfiguration`, `FLiBeThermodynamicState`, dataset split, provenance class, and optional source, group, trajectory, and parent-sample identifiers.

`FLiBeDatasetSplit` defines `TRAINING`, `VALIDATION`, and `TEST`. `validate_flibe_split_isolation` checks the declared dataset identity and group/trajectory relationships across these collections.

`ParameterProvenance` supplies the executable provenance classes `PRIMARY_SOURCE`, `DERIVED`, `CALIBRATED`, `AUTHOR_DEFINED`, `BENCHMARK`, `TEST_FIXTURE`, `REQUIRES_SOURCE`, and `REQUIRES_TEST`. The parameter or dataset record associates its physical values and computational outputs with the selected class and source identifier.

## 23. Exact Structural Invariants and Numerical Operations

The executable FLiBe state includes the following exact structural conditions:

- nonempty canonical Li, Be, F species sequence for the FLiBe atomic wrapper;
- atom-count agreement among configuration, graph, coordination, resonance, feature, and execution inputs where composed;
- nonnegative component formula-unit amounts with positive total amount;
- exact integer stoichiometric condition `N_F = N_Li + 2 N_Be` for configuration-derived binary composition;
- formal-charge accounting by the assigned Li, Be, and F integer charges;
- positive finite temperature and finite nonnegative pressure in the thermodynamic state;
- exact retained ternary alphabet, pending-destination type, and committed-route relation;
- exact dataset identities and declared sampling or grouping identifiers.

Floating-point evaluations of composition normalization, coordinate geometry, forces, energies, density, resonance evolution, and transport use their declared numerical methods, units, and preselected tolerances. Exact categorical and inventory relations use exact comparisons.

## 24. Reproducibility Record

A reproducible FLiBe calculation identifies:

- component composition, formula-unit or atomic-fraction convention, species counts, and charge assignment;
- atomic positions, masses, simulation cell, periodic flags, and atom ordering;
- thermodynamic temperature, pressure, material-state classification, and boundary history;
- interaction graph, cutoff, coordination descriptor, and geometric image convention;
- interatomic model parameters, node features, energy and derivative settings;
- resonance phases, frequencies, coupling coefficients, phase lags, and integration schedule;
- ternary requests, retained and pending states, guards, committed events, and conditioning schedule;
- trajectory and transport observables, physical time sampling, and numerical methods;
- source data, experimental or first-principles method identifiers, units, and supplied uncertainties;
- scale partitions, coarse states, constitutive providers, and target observable definitions;
- deterministic execution inputs, numerical checks, and associated output trace.

Every declared comparison binds its observable to the corresponding composition, state domain, source, transformation, and evaluation time.

## 25. Executable Interface Index

| Role | Repository path |
| --- | --- |
| Chemical species | `src/tr_eif/flibe/species.py` |
| Binary composition | `src/tr_eif/flibe/composition.py` |
| Atomic configuration wrapper | `src/tr_eif/flibe/configuration.py` |
| Formal ionic charges | `src/tr_eif/flibe/charge.py` |
| Species masses | `src/tr_eif/flibe/mass.py` |
| Thermodynamic state | `src/tr_eif/flibe/thermodynamic_state.py` |
| Physical units and provenance | `src/tr_eif/flibe/units.py` |
| Density parameter evaluation | `src/tr_eif/flibe/density.py` |
| Local graph coordination | `src/tr_eif/flibe/coordination.py` |
| Resonance parameters and descriptor | `src/tr_eif/flibe/resonance_parameterization.py`, `src/tr_eif/flibe/resonance_descriptor.py` |
| Continuous-to-ternary request mapping | `src/tr_eif/flibe/ternary_interpretation.py` |
| FLiBe TR-EIP energy realization | `src/tr_eif/flibe/tr_eip.py` |
| Dataset configuration and splits | `src/tr_eif/flibe/dataset_configuration.py` |
| FLiBe coarse structural hierarchy | `src/tr_eif/flibe/multiscale_coolant.py` |
| Atomic geometry and graph | `src/tr_eif/configuration/state.py`, `src/tr_eif/graph/builder.py` |
| Mechanical trajectory and transport | `src/tr_eif/md/trajectory.py`, `src/tr_eif/md/transport.py` |
| Experimental density source | `data/reference/flibe_vidrio_2022_density_measurements.json` |
| AIMD density source | `data/reference/flibe_baral_2021_aimd_density.json` |
| Registered FLiBe references | `docs/references/flibe_sources.md` |

## 26. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| Species and composition | `tests/invariants/test_flibe_species_invariants.py`, `tests/invariants/test_flibe_composition_invariants.py` |
| Configuration and charge | `tests/invariants/test_flibe_configuration_invariants.py`, `tests/invariants/test_flibe_charge_invariants.py` |
| Mass and thermodynamic state | `tests/invariants/test_flibe_mass_invariants.py`, `tests/invariants/test_flibe_thermodynamic_state_invariants.py` |
| Parameter units and density | `tests/invariants/test_flibe_units_invariants.py`, `tests/invariants/test_flibe_density_invariants.py` |
| Coordination and resonance | `tests/invariants/test_flibe_coordination_invariants.py`, `tests/invariants/test_flibe_resonance_descriptor_invariants.py` |
| Resonance parameterization | `tests/invariants/test_flibe_resonance_parameterization_invariants.py` |
| Ternary interpretation | `tests/invariants/test_flibe_ternary_interpretation_invariants.py` |
| FLiBe TR-EIP | `tests/integration/test_flibe_tr_eip.py` |
| Dataset grouping | `tests/invariants/test_flibe_dataset_configuration_invariants.py` |
| Multiscale hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |
| Experimental source table | `tests/integration/test_flibe_vidrio_2022_density_dataset.py` |
| Experimental/AIMD comparison | `tests/integration/test_flibe_experimental_aimd_density_cross_source_diagnostic.py` |

## 27. Chapter Integration

The FLiBe reference-system definition binds LiF–BeF2 composition, Li/Be/F atomic inventory, three-dimensional geometry, thermodynamic state, open-system exchange, interatomic energy, and trajectory observables into explicitly identified physical and computational records.

Continuous resonance and active balanced-ternary execution are coupled through declared request, event, and conditioning operators. Material-source records, dataset identities, and multiscale mappings associate each computed quantity with its composition, state, scale, method, and provenance.
