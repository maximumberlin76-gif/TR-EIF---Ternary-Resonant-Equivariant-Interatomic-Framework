
# Interatomic Reference Data

## 1. Scope and Reference-State Structure

This chapter defines the interatomic reference-data organization for the FLiBe specialization of TR-EIF. It connects LiF–BeF2 material composition, three-dimensional configurations, electronic-reference observables, experimentally resolved local structure, first-principles and molecular-dynamics calculations, and the inputs and outputs of the TR-EIP interatomic layer.

A reference datum consists of an identified observable, a physical and computational state, its numerical representation, a source and method, units, and the transformations used to bring it into a selected comparison or model-construction procedure.

The reference-data chain is:

`material and atomic state → source measurement or calculation → typed observable → mapping context → interatomic model input/output → numerical comparison → recorded result`.

The separately scheduled continuous resonance and active balanced-ternary `-1/0/1` operators retain their defined roles in construction of conditioned interatomic states.

## 2. Reference-Observable Classes

A material study can use the following observable classes:

| Class | Representative quantities | Data representation |
| --- | --- | --- |
| Electronic | Total energy, atomic forces, cell stress | Scalar, Cartesian vector tuple, Cartesian tensor |
| Pair geometry | Interatomic displacement, distance, periodic image | Directed-edge geometry and image tuple |
| Local structure | Species coordination, Be–F environments | Per-atom counts, typed structural descriptors |
| Pair statistics | Species-pair distance distribution | Radius axis and partial radial-distribution samples |
| Reciprocal-space structure | Neutron or X-ray scattering response | Scattering-vector axis and source-defined intensity or structure factor |
| Spectroscopy | NMR chemical shift and structural assignments | Spectroscopic coordinates and assigned environments |
| Thermophysical context | Density, cell volume, temperature, pressure | Typed scalar state and source-specific numeric table |
| Dynamical structure | Time correlations and trajectory-derived observables | Time axis, selected particle set, correlation series |

Each observable uses its defined independent variable, normalization, physical unit, material composition, state domain, and measurement or computational method. A multicomponent structural observable additionally identifies the ordered atomic species or pair species to which it applies.

## 3. Composition and Physical-State Coordinates

The binary component composition is described by normalized LiF and BeF2 formula-unit fractions:

`x_LiF + x_BeF2 = 1`.

The exact `2 LiF : 1 BeF2` reference has `(x_LiF, x_BeF2) = (2/3, 1/3)`, corresponding to `Li2BeF4` and a Li:Be:F atomic count ratio of `2:1:4`.

The nominal `67 mol% LiF : 33 mol% BeF2` mixture uses `(0.67, 0.33)`. The experimental Vidrio 2022 specimen has an ICP-MS reported BeF2 component value `33.58(5) mol%`. These compositions are retained with their individual bases and source precisions.

`FLiBeThermodynamicState` stores a finite positive absolute temperature in kelvin and finite nonnegative pressure in pascal. A complete reference state identifies temperature, pressure, composition, material phase or structural state, boundary conditions, and sampling or preparation method.

## 4. Atomic Configuration and Reference Geometry

Let `N >= 1` be the atom count, `S = (s_1, ..., s_N)` the ordered species tuple, and `R = (r_1, ..., r_N)` with `r_i in R^3`. An atomic reference configuration is represented by:

`X_atom = (S, R, B, P)`.

`B` denotes the optional lattice cell and `P` its periodic-axis flags. `AtomicConfiguration` stores these fields; `FLiBeConfiguration` validates the Li, Be, and F species domain and provides atom counts and composition methods.

For an explicit periodic image vector `k_ij` associated with a directed edge, its relative Cartesian displacement is:

`d_ij = r_j + B k_ij - r_i`.

Reference records preserve the cell-vector order, periodic-image convention, atom ordering, and Cartesian units. Geometrical quantities are evaluated at the source's declared configuration and time.

## 5. Primary-Source and Computational Provenance

The repository maintains scientific source registers in `docs/references/flibe_sources.md`, `docs/references/interatomic_potential_sources.md`, `docs/references/equivariant_model_sources.md`, and `docs/references/primary_sources.md`.

A registered observation retains the publication identifier, source location, material state, method, independent variables, value units, available uncertainty, and numerical processing steps. `ParameterProvenance` provides the executable labels `PRIMARY_SOURCE`, `DERIVED`, `CALIBRATED`, `AUTHOR_DEFINED`, `BENCHMARK`, `TEST_FIXTURE`, `REQUIRES_SOURCE`, and `REQUIRES_TEST`.

An additional evidence-kind field distinguishes `EXPERIMENTAL` and `FIRST_PRINCIPLES` in `FLiBeReferenceObservable`. A directly reported experimental measurement and a directly reported first-principles result can therefore carry source provenance while retaining their respective measurement and computational evidence kinds.

## 6. Registered Structural Publications

The FLiBe source register identifies the following structural references:

| Register identifier | Publication | Observables and method |
| --- | --- | --- |
| `FLIBE-PRIMARY-FAYFAR-2024-TOTAL-SCATTERING` | Fayfar et al., PRX Energy 3, 013001 (2024), DOI `10.1103/PRXEnergy.3.013001` | Liquid neutron/X-ray scattering and computational structural comparisons |
| `FLIBE-PRIMARY-FU-2023-NMR` | Fu et al., Phys. Chem. Chem. Phys. 25, 19446–19452 (2023), DOI `10.1039/D3CP01096A` | High-temperature NMR and Be–F local structural environments |
| `FLIBE-PRIMARY-GARDNER-2025-SOLID-DIFFRACTION` | Gardner et al., J. Appl. Crystallogr. 58, 435–446 (2025), DOI `10.1107/S1600576725000548` | Solid Li2BeF4 neutron/X-ray diffraction and temperature-dependent lattice geometry |
| `FLIBE-COMPUTATIONAL-SALANNE-2006-NETWORK` | Salanne et al., J. Phys. Chem. B 110, 11461–11467 (2006), DOI `10.1021/jp061002u` | Computational Be–F network formation in LiF–BeF2 mixtures |

Each reported measurement or calculated observable uses the physical state and method attached to its source record. Liquid-scattering, high-temperature NMR, solid diffraction, and computational network variables are indexed independently within the reference-data mapping.

## 7. Electronic-Reference Observables

`ElectronicReferenceRecord` in `src/tr_eif/multiscale/electronic_reference.py` binds one `AtomicConfiguration` to:

- `total_energy`: finite scalar energy;
- `forces`: optional `ForceState` with one three-dimensional force per atom;
- `stress`: optional `StressState` containing a Cartesian stress tensor;
- `source_id` and `method_id`: normalized method and provenance identifiers.

The executable entry point `evaluate_electronic_reference(configuration, evaluator)` calls the selected electronic-reference provider and checks equality between its returned configuration and the requested one. The provider supplies the numerical electronic observables and the resolved electronic-method metadata.

A reference-data manifest associates an electronic result with its charge and spin specification, exchange-correlation method, basis or plane-wave settings, pseudopotential treatment, reciprocal-space sampling, cell, convergence controls, energy zero, and units.

## 8. Energy, Force, and Stress Correspondence

For model parameters `Theta` and conditioning variables `A`, a differentiable interatomic energy is represented as:

`E_int = E_Theta(R, B, G, A)`.

Its conservative Cartesian force relation is:

`F_int,i = -grad_(r_i) E_int`.

For a homogeneous strain `epsilon` applied to atomic positions and the cell, stress components follow the selected cell-strain derivative and reference-volume convention. The executable `ConservativeStressEvaluator` uses symmetric strain perturbations.

Define corresponding source residuals with common units and matching atom and tensor-component order:

`delta_E = E_int - E_ref`.

`delta_F,i,a = F_int,i,a - F_ref,i,a`.

`delta_sigma_a,b = sigma_int,a,b - sigma_ref,a,b`.

A comparison declares the source energy-zero convention, species and atom correspondence, stress sign, cell normalization, conditioning state, and numerical differentiation parameters.

## 9. Interatomic Energy Model Inputs

`ReferenceEnergyModel` combines a `RadialMessageOperator`, `TernaryConditioning`, and `LinearInvariantEnergyFunctional`. It receives an atomic configuration, directed interaction graph, `NodeFeatureVector`, and retained `TernaryExecutionVector`.

The conditioned layer supplies scalar channels to the invariant energy functional. With scalar channel `phi_i,a`, channel weights `w_a`, and per-node bias `b`:

`E_i = b + sum_a w_a phi_i,a`.

`E_total = sum_i E_i`.

`EnergyModelResult` stores the conditioned layer result and `EnergyState`, including per-atom energy contributions and their total. The configuration, graph, feature and execution cardinalities correspond to the same ordered atom inventory.

## 10. FLiBe TR-EIP Specialization

`FLiBeTREIPModel` binds the FLiBe configuration, directed graph, initial features, `FLiBeResonanceDescriptor`, retained ternary execution, and a `ReferenceEnergyModel`.

`append_flibe_resonance_channels` adds the continuous scalar descriptors `phase_order` and `frequency_spread`, in that order, to each atom's existing scalar channels. The original vector-feature channels are retained. The subsequent energy evaluation receives these extended features and the executed `-1/0/1` conditioning vector.

`FLiBeTREIPResult` stores the input features, resonance-augmented features, graph, resonance descriptor, execution vector, and energy result. It verifies their shared atomic cardinality and associated input identities.

## 11. Directed Geometry and Coordination Records

`build_cutoff_graph` creates directed interaction edges using three-dimensional distances and the selected periodic-image convention. An edge stores source index, receiver index, and lattice-image index.

For receiver `j` and source species `s`, the executable species-coordination count is:

`z_(j,s) = count{i → j in G | species(i) = s}`.

`build_flibe_coordination_state` constructs one `FLiBeAtomCoordination` per atom, recording incoming Li, Be, and F neighbor counts. `FLiBeCoordinationState` retains these records in contiguous atom order.

The cutoff, periodic geometry, graph sampling time, and species identities define this graph-relative coordination observable. Chemical structural assignments from scattering, spectroscopy, or electronic calculations use explicit source-specific correspondence operators.

## 12. Species-Resolved Pair Distributions

For a homogeneous isotropic sampled material state, let `rho_beta = N_beta / V` be the number density of species `beta`. A partial radial distribution `g_(alpha,beta)(r)` describes the conditional radial density of species `beta` around reference atoms of species `alpha`, normalized to its bulk number density.

For shell radii `(r, r + dr)` and an ordered ensemble of source configurations, the shell-count estimator has the form:

`g_(alpha,beta)(r) ≈ <N_(alpha,beta)(r,r+dr)> / [N_alpha rho_beta 4 pi r^2 dr]`.

`N_(alpha,beta)` counts ordered distinct-atom pairs in the shell; same-species estimators apply their declared finite-population normalization. Cell geometry, coordinate handling, ensemble, bin width, and pair-selection policy accompany the computed curve.

For a specified coordination integration boundary `r_c`, the corresponding radial coordination statistic is:

`n_(alpha,beta)(r_c) = 4 pi rho_beta integral_(0→r_c) r^2 g_(alpha,beta)(r) dr`.

The pair distribution, its integrated coordination, and graph-relative neighbor counts are recorded as separate observables with explicitly selected cutoff and averaging conventions.

## 13. Reciprocal-Space Structural Observables

For a microscopic configuration, define the species density mode at wavevector `q`:

`rho_alpha(q) = sum_(i in alpha) exp(i q · r_i)`.

For a specified ensemble and reciprocal-space convention, a partial density-correlation observable may be written:

`S_(alpha,beta)(q) = <delta_rho_alpha(q) delta_rho_beta(-q)> / sqrt(N_alpha N_beta)`.

Here `delta_rho` denotes the selected mean-subtracted density mode. The experimental neutron or X-ray observable is constructed from the corresponding partial structural terms, scattering lengths or form factors, normalization, background treatment, and instrumental resolution of the source method.

A reciprocal-space comparison records the source wavevector coordinate, typically in inverse length, measured quantity and normalization, composition, temperature, physical state, and any reciprocal-to-real-space transformation.

## 14. Neutron and X-Ray Total-Scattering Inputs

The registered Fayfar 2024 study combines liquid FLiBe neutron and X-ray total-scattering measurements with atomistic computational structure analysis. For each imported scattering series, the reference manifest identifies:

- radiation type and associated scattering-weight convention;
- source sample composition and thermodynamic state;
- reciprocal-space axis and intensity or structure-factor definition;
- instrumental calibration, background, and normalization;
- numerical axis sampling and available measurement uncertainty;
- source location, dataset version, and applied transformations.

A model-side scattering observable is computed from a trajectory or configuration ensemble using the same declared species weighting and observable definition. Reference and model series are aligned through an explicit coordinate and unit mapping.

## 15. NMR and Local Structural Environments

The Fu 2023 study registers high-temperature NMR observations of FLiBe melts and structural assignments involving BeF4, Be2F7, Be3F10, and extended Be–F environments.

A spectroscopic reference record specifies the observed nucleus, chemical-shift axis, reference convention, temperature, composition, sample state, spectral processing method, and structural assignment procedure.

An atomistic representation may construct structural descriptors from Be–F coordination geometry, angular distributions, and connected-environment statistics. The mapping from these descriptors to an NMR observable or assigned structural population is identified by its selected physical method and source context.

## 16. Solid-State Structural Inputs

The Gardner 2025 reference provides temperature-dependent solid Li2BeF4 diffraction information. A solid structural record may store lattice vectors, cell volume, atomic sites, species occupancy, symmetry, temperature, and associated diffraction observables.

A transformation between crystal-cell and atomistic-reference representations specifies lattice conventions, supercell construction, atomic coordinates, unit conversion, and symmetry operations. Solid and liquid structural records retain their source state identifiers throughout a temperature-dependent material calculation.

## 17. Computational Be–F Network References

The Salanne 2006 computational register concerns network formation across LiF–BeF2 mixture compositions using a first-principles-derived interaction description. A computational structural reference identifies the interaction model, composition, simulation cell, temperature, sampling procedure, and reported network or coordination observable.

For a model-generated Be–F environment, possible descriptors include species-neighbor distributions, tetrahedral geometry, bridging-fluorine statistics, and connected-cluster sizes. Each descriptor is paired with a defined graph or bonding criterion and a numerical extraction procedure.

The directed `InteractionGraph` remains the geometric adjacency representation supplied to TR-EIP; a chemically interpreted network is constructed by its registered structural mapping.

## 18. Registered AIMD Numerical Table

The committed file `data/reference/flibe_baral_2021_aimd_density.json` registers nine temperature-labeled rows transcribed from Baral et al., *ACS Omega* 6, 19822–19835 (2021), DOI `10.1021/acsomega.1c02528`.

Its dataset identifier is `tr-eif.flibe.baral-2021.aimd-structural-density.v1`. The source describes a 504-atom Li2BeF4 simulation supercell. The table columns are temperature in kelvin, cubic-cell edge in angstroms, cell volume in cubic angstroms, and AIMD density in `g/cm^3`.

For the registered `T750` row:

`T = 750 K`.

`a = 18.915 angstrom`.

`V = 6767.367 angstrom^3`.

`rho = 1.757 g/cm^3 = 1757 kg/m^3`.

The unit transformation uses `1 g/cm^3 = 1000 kg/m^3`. The dataset retains its temperature labels, supercell method, composition, cell metadata, and source location.

## 19. Registered Experimental Density Table

The committed file `data/reference/flibe_vidrio_2022_density_measurements.json` registers 61 density observations from the four experimental runs `0A`, `1A`, `1B`, and `1C`, reported by Vidrio et al., *Journal of Chemical & Engineering Data* 67, 3517–3531 (2022), DOI `10.1021/acs.jced.2c00212`.

Each table row contains:

`(temperature_C, standard_uncertainty_C, density_kg_m3, standard_uncertainty_kg_m3)`.

The record includes hydrostatic-buoyancy method metadata, measurement pressure, nominal component ratio, and the ICP-MS reported BeF2 composition `33.58(5) mol%`.

Density is registered as a thermophysical observable associated with material inventory and volume. Its use alongside interatomic structural and electronic records is determined by the selected model-to-observable calculation and shared physical-state metadata.

## 20. Source-Resolved Numerical Comparison

The repository contains two executed FLiBe density cross-source programs:

- `benchmarks/flibe/experimental_density_cross_source_diagnostic.py`, for the experimental table and the registered density correlation;
- `benchmarks/flibe/experimental_aimd_density_cross_source_diagnostic.py`, for the experimental Vidrio table and published Baral AIMD values.

The Vidrio–Baral comparison selects three AIMD temperature rows and constructs nine within-run interpolated density comparisons under its declared temperature-screening procedure. Each residual is calculated in `kg/m^3` with its source row and interpolation bracket recorded.

Experimental composition, AIMD formula-unit composition, source pressure metadata, and available uncertainties remain separate fields. The numerical comparison procedure identifies the selection and transformation that produced each pointwise residual.

## 21. Typed Experimental and First-Principles Comparison

`FLiBeReferenceObservable` in `src/tr_eif/flibe/reference_comparison.py` stores `observable_id`, `FLiBeComposition`, `FLiBeThermodynamicState`, `physical_state_id`, `FLiBeEvidenceKind`, values, value unit, normalization identifier, source identifier, method identifier, and provenance.

An optional independent axis is stored as a finite numeric tuple with an associated axis unit and the same length as the values tuple. This representation accommodates scalar observables and sampled structural curves through the same typed interface.

`compare_flibe_experimental_first_principles` constructs `FLiBeReferenceComparison` when the two records have matching:

- observable identifier and composition;
- thermodynamic and physical-state identifiers;
- value unit and normalization identifier;
- sample axis, axis unit, and sample count.

The result exposes `residuals`, `absolute_residuals`, `mean_absolute_error`, `root_mean_square_error`, and `max_absolute_error`, using first-principles minus experimental values in its signed residual definition.

## 22. Dataset Configuration and Source Separation

`FLiBeDatasetConfiguration` associates a unique sample identifier and configuration identifier with an `FLiBeConfiguration`, a thermodynamic state, `FLiBeDatasetSplit`, and provenance. Optional source, group, trajectory, and parent-sample identifiers preserve sample relationships.

The split enumeration contains `TRAINING`, `VALIDATION`, and `TEST`. `validate_flibe_split_isolation` checks exact configuration identity and value, group and trajectory identifiers, and known parent relationships across those splits.

An interatomic dataset pairs each source observable with the configuration and method from which it was obtained. Reference-energy labels, forces, stresses, structural curves, and material-property observations retain their own output definitions and sampling coordinates.

## 23. Symmetry and Numerical Comparison

Under an admissible orthogonal spatial transformation `Q in O(3)` and translation `b`, the configuration transforms as:

`r_i' = Q r_i + b`.

For the corresponding equivariant energy-and-force realization:

`E_int(R') = E_int(R)`.

`F_int,i(R') = Q F_int,i(R)`.

A Cartesian stress tensor follows `sigma' = Q sigma Q^T` under the corresponding convention. Atomic permutations are applied consistently to species, coordinates, node features, retained execution, and per-atom observables.

For sampled source and model values on matched axes, a pointwise residual may be defined by `d_j = y_model,j - y_reference,j`. The numerical record associates the residual with source uncertainties, any axis conversion, the comparison normalization, and its declared statistical aggregation.

## 24. Continuous Resonance and Active-Ternary Conditioning

`FLiBeResonanceDescriptor` binds the continuous resonance state, coordination state, atomic configuration, thermodynamic state, and provenance. Its `phase_order` and `frequency_spread` are continuous scalar descriptors calculated from the supplied oscillator state.

A separately selected request mapping produces targets for guarded execution. The retained execution alphabet is `-1/0/1`, with active neutral `0`, pending-target retention, and two committed legs for opposite-polarity routes:

`-1 → 0 → 1`.

`1 → 0 → -1`.

The interatomic model receives the retained execution vector and resonance-augmented feature channels. The record identifies the descriptor sampling time, requested target, pending state, committed event, and executed conditioning used for the energy evaluation.

## 25. Data Transformation and Reproducibility

For each selected reference series, the calculation record includes:

- source publication and exact table, figure, or data location;
- evidence kind, provenance class, sample identifier, and method identifier;
- composition basis, atomic inventory, and material-state variables;
- coordinates, lattice and periodic-image conventions, and source sampling times;
- observable identity, independent axes, units, and normalization;
- source-provided uncertainty and its representation;
- unit conversion, interpolation, integration, or digitization operation when applied;
- generated graph, cutoff, features, resonance state, and ternary execution inputs;
- model parameters, energy/force/stress derivative settings, and output values;
- comparison axes, residual definitions, numeric criteria, and output provenance.

Exact source identifiers, sample ordering, graph and state cardinalities, and categorical execution invariants use exact comparisons. Numerical operations use their declared methods, resolutions, and fixed comparison parameters.

## 26. Executable Interface Index

| Role | Repository path |
| --- | --- |
| FLiBe configuration and composition | `src/tr_eif/flibe/configuration.py`, `src/tr_eif/flibe/composition.py` |
| Thermodynamic source state | `src/tr_eif/flibe/thermodynamic_state.py` |
| Species and formal-charge records | `src/tr_eif/flibe/species.py`, `src/tr_eif/flibe/charge.py` |
| Graph geometry and construction | `src/tr_eif/graph/geometry.py`, `src/tr_eif/graph/builder.py` |
| Species-resolved graph coordination | `src/tr_eif/flibe/coordination.py` |
| Electronic-reference record and provider | `src/tr_eif/multiscale/electronic_reference.py` |
| Interatomic scalar energy | `src/tr_eif/energy/model.py` |
| Coordinate-derived forces and cell-derived stress | `src/tr_eif/energy/force_evaluator.py`, `src/tr_eif/energy/stress_evaluator.py` |
| FLiBe TR-EIP energy specialization | `src/tr_eif/flibe/tr_eip.py` |
| Resonance descriptor | `src/tr_eif/flibe/resonance_descriptor.py` |
| Dataset configuration and split isolation | `src/tr_eif/flibe/dataset_configuration.py` |
| Typed source comparison | `src/tr_eif/flibe/reference_comparison.py` |
| Experimental density table | `data/reference/flibe_vidrio_2022_density_measurements.json` |
| First-principles density table | `data/reference/flibe_baral_2021_aimd_density.json` |
| Structural source register | `docs/references/flibe_sources.md` |
| Interatomic potential sources | `docs/references/interatomic_potential_sources.md` |

## 27. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| Electronic-reference provider | `tests/integration/test_multiscale_electronic_reference.py` |
| FLiBe configuration and composition | `tests/invariants/test_flibe_configuration_invariants.py`, `tests/invariants/test_flibe_composition_invariants.py` |
| Species coordination | `tests/invariants/test_flibe_coordination_invariants.py` |
| FLiBe resonance descriptor | `tests/invariants/test_flibe_resonance_descriptor_invariants.py` |
| FLiBe TR-EIP energy evaluation | `tests/integration/test_flibe_tr_eip.py` |
| Force and stress consistency | `tests/conservation/test_force_gradient_consistency.py`, `tests/conservation/test_stress_consistency.py` |
| Typed FLiBe source comparison | `tests/integration/test_flibe_reference_comparison.py` |
| FLiBe dataset grouping | `tests/invariants/test_flibe_dataset_configuration_invariants.py` |
| Experimental table integrity | `tests/integration/test_flibe_vidrio_2022_density_dataset.py` |
| Vidrio–Baral numerical comparison | `tests/integration/test_flibe_experimental_aimd_density_cross_source_diagnostic.py` |

These tests exercise typed configuration identity, source and method binding, numerical observables, geometry and energy operators, per-atom cardinality, canonical dataset ordering, and deterministic computation using their specified inputs.

## 28. Chapter Integration

The FLiBe interatomic reference-data structure binds chemical composition, physical state, source observables, atomic geometry, and computational provenance into reproducible mappings. Experimental scattering and spectroscopy, first-principles records, source density tables, and model-generated interatomic quantities retain their individual observable definitions and methods.

The TR-EIP layer evaluates conditioned scalar energy from the selected geometry, resonance channels, and retained `-1/0/1` execution. Derived forces, stress, structural descriptors, and cross-source observables connect through explicitly identified numerical operators and comparison contexts.
