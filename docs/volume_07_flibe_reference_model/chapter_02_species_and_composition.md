
# Species and Composition

## 1. Scope and Material-State Structure

This chapter defines the species inventory and composition mappings of the LiF–BeF2 reference material in TR-EIF. The representation connects binary formula-unit composition, discrete Li/Be/F atom counts, formal ionic-charge accounting, species masses, three-dimensional atomic configurations, and material-source metadata.

The physical state of the selected open nonlinear dissipative system includes atomistic geometry, thermodynamic variables, transport and exchange fields, and continuous resonance dynamics. Balanced-ternary `-1/0/1` execution is coupled through separately defined request and conditioning operators.

The chemical mapping chain is:

`LiF/BeF2 formula-unit amounts → normalized component fractions → Li/Be/F atomic amounts → ordered atomic configuration → formal-charge and mass records`.

## 2. Canonical Atomic Species

`FLiBeSpecies` in `src/tr_eif/flibe/species.py` defines the atomic species identifiers of the reference domain.

| Chemical symbol | Enumeration value | Canonical position |
| --- | --- | ---: |
| `Li` | `FLiBeSpecies.LITHIUM` | 0 |
| `Be` | `FLiBeSpecies.BERYLLIUM` | 1 |
| `F` | `FLiBeSpecies.FLUORINE` | 2 |

`FLIBE_SPECIES` and `flibe_species_symbols()` return Li, Be, F in this order. `flibe_species_from_symbol()` resolves exact symbols, `is_flibe_species_symbol()` checks a candidate, and `validate_flibe_species_sequence()` converts a nonempty tuple of exact symbols to enumeration values in the supplied atom order.

The three symbol values are case-sensitive, and the validator retains the order of the input tuple.

## 3. Binary Formula-Unit Composition

Let `n_LiF >= 0` and `n_BeF2 >= 0` be amounts of the two component formula units. Define:

`n_formula = n_LiF + n_BeF2 > 0`.

The normalized component fractions are:

`x_LiF = n_LiF / n_formula`.

`x_BeF2 = n_BeF2 / n_formula`.

The binary composition domain is:

`X_comp = {(x_LiF, x_BeF2) | x_LiF >= 0, x_BeF2 >= 0, x_LiF + x_BeF2 = 1}`.

Formula-unit fractions, atomic fractions, and integer atomic counts are separate representations of the chemical inventory, connected by explicit mapping equations.

## 4. Executable FLiBeComposition

`FLiBeComposition(lif_fraction, bef2_fraction)` in `src/tr_eif/flibe/composition.py` accepts two finite nonnegative real inputs, excluding Boolean values. The constructor requires their sum to be positive and normalizes both components by that sum.

The inputs `(2.0, 1.0)` and `(20.0, 10.0)` therefore represent the same normalized component ratio. `formula_unit_fractions` returns the stored fractions in LiF, BeF2 order.

The supported binary domain includes pure-component endpoints `(1, 0)` and `(0, 1)`.

For a positive finite amount `n_formula`, the method `formula_unit_amounts(total_formula_units=n_formula)` returns:

`(n_LiF, n_BeF2) = (n_formula x_LiF, n_formula x_BeF2)`.

## 5. Formula Units to Atomic Amounts

Each LiF formula unit contributes one Li and one F. Each BeF2 unit contributes one Be and two F. Hence:

`n_Li = n_LiF`.

`n_Be = n_BeF2`.

`n_F = n_LiF + 2 n_BeF2`.

The total atomic amount is:

`n_atoms = n_Li + n_Be + n_F = 2 n_LiF + 3 n_BeF2`.

For unit total formula-unit amount:

`n_atoms,unit = 2 x_LiF + 3 x_BeF2`.

`FLiBeComposition.atomic_amounts(total_formula_units=...)` implements the Li/Be/F amount mapping and returns values in canonical species order.

## 6. Atomic Fractions

For atomic fractions `a_Li`, `a_Be`, and `a_F`, the component-to-atomic transformation is:

`a_Li = x_LiF / (2 x_LiF + 3 x_BeF2)`.

`a_Be = x_BeF2 / (2 x_LiF + 3 x_BeF2)`.

`a_F = (x_LiF + 2 x_BeF2) / (2 x_LiF + 3 x_BeF2)`.

The mathematical identity is `a_Li + a_Be + a_F = 1`.

The executable properties `lithium_fraction`, `beryllium_fraction`, `fluorine_fraction`, and `atomic_fractions` provide these quantities. `atomic_fractions` returns ordered symbol/value pairs for Li, Be, and F.

## 7. Exact 2:1 Reference Ratio

For the exact component formula-unit ratio `2 LiF : 1 BeF2`:

`x_LiF = 2/3`, `x_BeF2 = 1/3`.

Three component formula units imply the atomic inventory:

`n_Li : n_Be : n_F = 2 : 1 : 4`.

Its inventory formula is `Li2BeF4`; the corresponding atomic fractions are:

`a_Li = 2/7`, `a_Be = 1/7`, `a_F = 4/7`.

The executable helper `eutectic_flibe_composition()` returns the normalized `FLiBeComposition(2.0, 1.0)` reference. Phase-equilibrium conditions and invariant-point composition are attached to their source-specific temperature, pressure, and phase-diagram definitions.

## 8. Nominal and Measured Compositions

Composition records preserve the input basis and reported precision.

| Composition record | LiF component | BeF2 component | Recorded basis |
| --- | ---: | ---: | --- |
| Exact 2:1 | `2/3` | `1/3` | Formula-unit ratio |
| Nominal 67:33 | `67 mol%` | `33 mol%` | Decimal component fractions |
| Vidrio 2022 specimen | `66.42 mol%` by binary complement | `33.58(5) mol%` | ICP-MS composition |

The measured BeF2 value and its parenthetical uncertainty notation are retained from the Vidrio source record. The binary complement is calculated in the same LiF–BeF2 component basis.

A numerical mapping retains each sample's original composition description, method, unit, and uncertainty representation.

## 9. Atomic Amounts for Nominal 67:33

For 100 nominal component formula units, with 67 LiF and 33 BeF2 units:

`n_Li = 67`.

`n_Be = 33`.

`n_F = 67 + 2(33) = 133`.

`n_atoms = 233`.

Thus the atomic fractions are:

`(a_Li, a_Be, a_F) = (67/233, 33/233, 133/233)`.

This calculation uses the nominal 67:33 input composition. The exact 2:1 calculation uses the rational values in Section 7.

## 10. Discrete Atomic Configuration

`AtomicConfiguration` in `src/tr_eif/configuration/state.py` stores an ordered nonempty species tuple, one finite Cartesian position per atom, optional cell vectors, and three periodic-axis flags.

`FLiBeConfiguration(configuration)` in `src/tr_eif/flibe/configuration.py` binds the atomic configuration to the Li/Be/F species domain. Its accessors include:

- `atom_count`: total number of atoms;
- `species`: ordered canonical `FLiBeSpecies` tuple;
- `species_counts`: Li, Be, F integer counts in canonical order;
- `atomic_fractions`: counts divided by the total atom count.

For a configuration containing counts `N_Li`, `N_Be`, and `N_F`, the exact inventory cardinality is:

`N = N_Li + N_Be + N_F >= 1`.

## 11. Exact Configuration Stoichiometry

`FLiBeConfiguration.composition()` derives binary formula-unit fractions from atomic counts under the integer stoichiometric relation:

`N_F = N_Li + 2 N_Be`.

It additionally requires `N_Li + N_Be > 0`. The derived component formula-unit counts are:

`N_LiF = N_Li`, `N_BeF2 = N_Be`.

Therefore:

`x_LiF = N_Li / (N_Li + N_Be)`.

`x_BeF2 = N_Be / (N_Li + N_Be)`.

The `FLiBeConfiguration` wrapper represents the declared Li/Be/F atom sequence. The `composition()` method applies the binary component-stoichiometry contract when the composition is requested.

## 12. Composition Comparison Operator

`FLiBeConfiguration.matches_composition(composition, absolute_tolerance=0.0)` compares the derived normalized fractions with a supplied `FLiBeComposition`.

For a finite nonnegative absolute tolerance `epsilon`, its two conditions are:

`|x_LiF,config - x_LiF,request| <= epsilon`.

`|x_BeF2,config - x_BeF2,request| <= epsilon`.

The default tolerance is exactly zero. The independent integer stoichiometric condition in Section 11 is evaluated exactly when the configuration composition is derived.

A composition comparison records its source basis, normalized target values, and the selected numerical tolerance.

## 13. Formal Ionic Charges

`FLIBE_FORMAL_CHARGES` in `src/tr_eif/flibe/charge.py` provides these integer formal-charge assignments in units of the elementary charge:

| Species | Formal ionic charge |
| --- | ---: |
| Li | `1` |
| Be | `2` |
| F | `-1` |

`formal_charge()` accepts a `FLiBeSpecies` enumeration member, while `formal_charge_from_symbol()` accepts the exact chemical symbol.

The total formal charge of a discrete configuration is:

`Q_formal/e = N_Li + 2 N_Be - N_F`.

The binary stoichiometric condition of Section 11 gives `Q_formal = 0`. Formal ionic charge, electronic-state variables, and retained ternary execution values are represented in their respective state and parameter spaces.

## 14. Formal-Charge State

`configuration_formal_charges(configuration)` generates one formal-charge entry per atom in the stored atom order. `total_formal_charge()` returns their integer sum; `is_formally_neutral()` evaluates equality of that sum to zero.

`FormalChargeState` stores the ordered tuple of formal charges and their exact sum. `build_formal_charge_state()` constructs the record for one `FLiBeConfiguration`.

The constructor requires equality between `total_charge` and the exact sum of its stored charge entries. The formula-unit inventory, atomic charge sum, and numerical interatomic energy remain distinguishable typed quantities.

## 15. Species Masses and Total Mass

`FLiBeMassParameters(lithium, beryllium, fluorine)` in `src/tr_eif/flibe/mass.py` stores three finite, strictly positive mass parameters. The accepted numeric inputs are normalized to floating-point values with Boolean values excluded.

`species_masses` returns the parameters in Li/Be/F order. `mass_for_species()` and `mass_for_symbol()` retrieve one parameter by canonical species identity.

`configuration_masses(configuration, parameters)` returns an ordered atomwise mass tuple. `total_configuration_mass()` evaluates:

`M_total = N_Li m_Li + N_Be m_Be + N_F m_F`.

The mass unit and source of the supplied parameters belong to the material-model configuration. A trajectory uses the corresponding per-atom mass tuple in its mechanical equations.

## 16. Component Mass and Cell Density

With consistent atomic mass units, the component formula-unit masses are:

`m_LiF = m_Li + m_F`.

`m_BeF2 = m_Be + 2 m_F`.

A mean mass per mixture formula unit is:

`m_formula,mean = x_LiF m_LiF + x_BeF2 m_BeF2`.

For a periodic cell with positive volume `V_cell`, the cell-derived mass density is:

`rho_cell = M_total / V_cell`.

Unit conversion follows the mass and length units of the selected simulation state. A thermodynamic density-provider evaluation carries its separately declared composition, temperature, pressure, source, and property units.

## 17. E(3) Geometry and Permutation

For orthogonal matrix `Q in O(3)` and translation `b in R^3`, spatial coordinates transform as:

`r_i' = Q r_i + b`.

The species counts, normalized composition, formal-charge sum, and total species mass are invariant under this common spatial transformation. A consistent atomic permutation reorders symbols, coordinates, charges, masses, and per-atom features using the same index mapping.

Geometric interaction graphs and phase-coupling operators use the transformed atomic configuration and its declared image and cutoff conventions.

## 18. Local Structural Coordination

`build_flibe_coordination_state()` in `src/tr_eif/flibe/coordination.py` associates a validated configuration with a directed interaction graph and calculates incoming-neighbor counts for each of the three species.

For receiving atom `j` and atomic species `s`, define:

`z_(j,s) = count{i → j in G | species(i) = s}`.

The graph cutoff, cell geometry, periodic images, and sampling time identify this coordination observable. Experimentally derived structural coordination retains its source measurement and analysis procedure.

Bulk composition determines the global species inventory; the coordination state records the selected local neighborhood at the sampled configuration.

## 19. Thermodynamic State and Composition

`FLiBeThermodynamicState(temperature, pressure)` stores a finite positive temperature in kelvin and finite nonnegative pressure in pascal. The material-state record associates these coordinates with a selected composition, configuration, physical state domain, and boundary conditions.

A composite material state may be written:

`X_material = (composition, configuration, T, P, boundary, provenance)`.

Physical phase equilibria and structural classifications use their respective material definitions and source-specific conditions. Formula-unit composition and atom inventory remain explicitly recorded across such material-state changes.

## 20. Species Exchange in an Open System

Let `c_s(x,t)` denote a concentration of atomic species `s`, `J_s` its total flux, and `q_s` its volumetric source in a declared control region `Omega` with outward normal `n`.

The balance equation is:

`partial_t c_s + div(J_s) = q_s`.

For a fixed control volume:

`d/dt integral_Omega c_s dV = -integral_(partial Omega) J_s · n dA + integral_Omega q_s dV`.

A composition record at time `t` is constructed from the species amounts and the selected component-basis mapping. Material inflow, outflow, and source events retain their flux definitions and physical time coordinates.

## 21. Formal-Charge Flux Accounting

Using formal-charge coefficients `z_Li = 1`, `z_Be = 2`, and `z_F = -1`, define:

`rho_formal/e = c_Li + 2 c_Be - c_F`.

`J_formal/e = J_Li + 2 J_Be - J_F`.

The species equations give:

`partial_t(rho_formal/e) + div(J_formal/e) = q_Li + 2 q_Be - q_F`.

The boundary and source definitions specify any applied charge-conservation or electroneutrality constraint. Formal ionic-charge fluxes and electronic transport observables retain their individually declared mathematical definitions.

## 22. Dataset State and Provenance

`FLiBeDatasetConfiguration` binds sample and configuration identifiers, a validated `FLiBeConfiguration`, thermodynamic state, dataset split, provenance class, and optional source, group, trajectory, and parent identifiers.

Its `composition` property delegates to `FLiBeConfiguration.composition()` and therefore uses the exact binary stoichiometry of Section 11.

`FLiBeDatasetSplit` contains `TRAINING`, `VALIDATION`, and `TEST`. `validate_flibe_split_isolation` enforces identity and recorded group/trajectory relationships across the split collections.

Composition, state domain, observable, unit, uncertainty, source method, and split identity remain associated with each material sample.

## 23. Experimental and AIMD Composition Records

The experimental source `data/reference/flibe_vidrio_2022_density_measurements.json` contains 61 density measurements across runs `0A`, `1A`, `1B`, and `1C`, identified with Vidrio et al. (2022), DOI `10.1021/acs.jced.2c00212`. It records nominal `2 LiF : 1 BeF2` composition and the ICP-MS measured BeF2 value `33.58(5) mol%`.

The first-principles dataset `data/reference/flibe_baral_2021_aimd_density.json`, identified with Baral et al. (2021), DOI `10.1021/acsomega.1c02528`, contains nine registered AIMD density records. Its material composition is described as `Li2BeF4` at an exact 2:1 LiF–BeF2 formula-unit ratio.

Each dataset stores source-specific composition definitions, reported temperatures, calculation or measurement method, units, and available state metadata. A cross-source comparison supplies the selected physical-state and observable correspondence.

## 24. Additional Species and Isotopic Coordinates

The current elemental FLiBe reference enumeration contains Li, Be, and F. A material extension with isotopic distinctions, impurities, dissolved H/D/T, or additional constituents defines its corresponding species identifiers, inventories, masses, charges, and source records.

The extended composition space identifies its component basis, normalization, atom inventory mapping, and physical transport or reaction operators. The original LiF–BeF2 binary component fractions retain their declared basis when such additional coordinates are introduced.

## 25. Resonance and Ternary Coupling

FLiBe atomic geometry and the interaction graph can be associated with continuous Kuramoto–Sakaguchi oscillator dynamics:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

A resonance descriptor and local coordination can enter a declared interatomic feature or execution-request mapping.

The executed alphabet is `-1/0/1`, with active neutral `0`. Retained execution state, pending destination, request, guard, and committed event have distinct typed fields. Opposite-polarity committed routes use:

`-1 → 0 → 1`.

`1 → 0 → -1`.

Atomic species, formula-unit fractions, formal charge, oscillator phase, and retained execution state are represented through their independent physical and computational types.

## 26. Seven-Atom Reference Inventory

Consider the ordered species sequence:

`S = (Li, Li, Be, F, F, F, F)`.

Its exact counts are `N_Li = 2`, `N_Be = 1`, `N_F = 4`, and `N = 7`. The stoichiometric relation gives:

`N_F = N_Li + 2 N_Be = 4`.

The derived binary composition and atomic fractions are:

`(x_LiF, x_BeF2) = (2/3, 1/3)`.

`(a_Li, a_Be, a_F) = (2/7, 1/7, 4/7)`.

The ordered formal charges are:

`(1, 1, 2, -1, -1, -1, -1)`.

The sum is zero. For species mass parameters `m_Li`, `m_Be`, and `m_F`:

`M_total = 2 m_Li + m_Be + 4 m_F`.

Spatial coordinates and periodic geometry are supplied as independent fields of this same ordered atomic configuration.

## 27. Exact Invariants and Numerical Qualification

The executable species and composition contracts include:

- exact canonical Li, Be, F symbols and enumeration order;
- nonempty tuple validation for atom-species sequences;
- two-component normalized formula-unit composition with finite nonnegative inputs and positive total;
- component-to-atomic amount and atomic-fraction mapping;
- one finite Cartesian position per atom and exact atom-count cardinality;
- integer species counts and exact stoichiometry `N_F = N_Li + 2 N_Be` for binary composition derivation;
- exact formal-charge assignments and total-charge equality;
- finite positive atomic-mass parameters and ordered per-atom mass assignment;
- exact atom ordering through species, formal-charge, and mass arrays;
- declared nonnegative tolerance for floating-point composition comparison;
- identified provenance and source composition basis for registered datasets.

Categorical symbols, integer stoichiometry, and formal-charge sums use exact comparisons. Normalized floating-point composition and geometry calculations use the declared numerical operations and fixed comparison criteria.

## 28. Reproducibility Record

A species and composition trace records:

- component basis, formula-unit amounts, and normalized fractions;
- ordered atom symbols, integer counts, and atomic fractions;
- formal-charge assignments and stoichiometric relation;
- mass parameter values, units, and provenance;
- positions, simulation cell, periodic flags, and coordinate reference;
- material temperature, pressure, and physical-state conditions;
- nominal, calculated, or measured composition metadata and uncertainties;
- material boundary, species flux, and inventory-update events;
- local coordination, continuous resonance variables, and ternary execution events when coupled;
- numerical methods, tolerances, dataset split, and source identifiers.

The trace binds a chemical inventory and source-state definition to the corresponding interatomic, atomistic, or multiscale computation.

## 29. Executable Interface Index

| Function | Repository path |
| --- | --- |
| Canonical atomic species | `src/tr_eif/flibe/species.py` |
| Binary composition and atomic amounts | `src/tr_eif/flibe/composition.py` |
| Atomic configuration and composition | `src/tr_eif/flibe/configuration.py` |
| Formal ionic-charge representation | `src/tr_eif/flibe/charge.py` |
| Species masses and total mass | `src/tr_eif/flibe/mass.py` |
| General atomic geometry | `src/tr_eif/configuration/state.py` |
| FLiBe thermodynamic state | `src/tr_eif/flibe/thermodynamic_state.py` |
| Units and source provenance | `src/tr_eif/flibe/units.py` |
| Dataset configurations and split isolation | `src/tr_eif/flibe/dataset_configuration.py` |
| Species-resolved graph coordination | `src/tr_eif/flibe/coordination.py` |
| Resonance descriptors | `src/tr_eif/flibe/resonance_descriptor.py` |
| Ternary request mapping | `src/tr_eif/flibe/ternary_interpretation.py` |
| FLiBe interatomic model | `src/tr_eif/flibe/tr_eip.py` |
| Multiscale material hierarchy | `src/tr_eif/flibe/multiscale_coolant.py` |
| Registered FLiBe sources | `docs/references/flibe_sources.md` |
| Experimental density data | `data/reference/flibe_vidrio_2022_density_measurements.json` |
| AIMD density data | `data/reference/flibe_baral_2021_aimd_density.json` |

## 30. Executable Test Index

| Domain | Repository test path |
| --- | --- |
| Species symbols | `tests/invariants/test_flibe_species_invariants.py` |
| Component and atomic composition | `tests/invariants/test_flibe_composition_invariants.py` |
| Discrete atomic configuration | `tests/invariants/test_flibe_configuration_invariants.py` |
| Formal-charge invariants | `tests/invariants/test_flibe_charge_invariants.py` |
| Species mass invariants | `tests/invariants/test_flibe_mass_invariants.py` |
| Public FLiBe API | `tests/invariants/test_flibe_public_api.py` |
| Dataset split and provenance | `tests/invariants/test_flibe_dataset_configuration_invariants.py` |
| Local coordination invariants | `tests/invariants/test_flibe_coordination_invariants.py` |
| Thermodynamic state invariants | `tests/invariants/test_flibe_thermodynamic_state_invariants.py` |
| Experimental source dataset | `tests/integration/test_flibe_vidrio_2022_density_dataset.py` |
| Experiment/AIMD source comparison | `tests/integration/test_flibe_experimental_aimd_density_cross_source_diagnostic.py` |

## 31. Chapter Integration

The FLiBe species and composition representation maps normalized LiF–BeF2 formula-unit fractions to exact Li/Be/F atomic inventories and associated three-dimensional configurations, formal ionic charges, and species mass parameters.

Material thermodynamic state, recorded source composition, coordination geometry, continuous resonance, and active balanced-ternary execution connect through explicit data types and operator schedules. Their associated computation records retain the chemical basis, state variables, mapping context, and provenance of each physical observable.
