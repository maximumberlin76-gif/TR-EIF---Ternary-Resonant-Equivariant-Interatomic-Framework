# FLiBe Validation Matrix

## 1. Scope

This document defines the repository-level validation matrix for the FLiBe specialization of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The matrix maps:

- Phase 10 FLiBe model requirements;
- Phase 11 FLiBe benchmark requirements;
- executable implementation artifacts;
- committed qualification tests;
- registered source evidence;
- provenance boundaries;
- validation status;
- unresolved evidence conditions.

This document does not introduce new physical parameters.

It does not convert benchmark fixtures into physical evidence.

It does not convert validation status into balanced-ternary state.

The principal FLiBe source register is:

`docs/references/flibe_sources.md`

The principal FLiBe executable package is:

`src/tr_eif/flibe/`

The principal FLiBe benchmarks are:

`benchmarks/flibe/`

---

## 2. Validation Status Vocabulary

This matrix uses the following validation-status labels.

### `EXECUTABLE_QUALIFIED`

The implementation exists and committed qualification tests exercise the declared executable contract.

### `SOURCE_REGISTERED`

External scientific provenance is recorded for the declared evidence class and observable.

This status does not imply that executable numerical data have been created.

### `SOURCE_REGISTERED_PARTIAL`

Source provenance exists for part of the required evidence domain while explicit source gaps remain.

### `CONTRACT_QUALIFIED`

The executable comparison or validation machinery exists and is tested, but source-backed scientific comparison data are not yet sufficient to close the corresponding physical validation claim.

### `BENCHMARK_IMPLEMENTED`

A benchmark implementation exists.

This status does not imply that the benchmark itself is automatically executed by CI.

### `BENCHMARK_CI_QUALIFIED`

A benchmark exists and a committed qualification test executes the benchmark inside the automatic validation path.

### `REQUIRES_SOURCE`

The claim requires additional independent physical or first-principles evidence.

### `REQUIRES_TEST`

The executable artifact exists but the required qualification test or CI execution path is incomplete.

### `NOT_IMPLEMENTED`

The corresponding executable or benchmark artifact is not present.

These labels are validation metadata.

They are not balanced-ternary execution states.

Therefore:

`EXECUTABLE_QUALIFIED ≠ 1`

`REQUIRES_SOURCE ≠ -1`

`REQUIRES_TEST ≠ 0`

---

## 3. Architectural Identity

The project-level relation is:

`TR-EIP ⊂ TR-EIF`

The FLiBe specialization is a domain realization of TR-EIP inside TR-EIF.

The nesting is:

`TR-EIF framework`

`→ TR-EIP model family`

`→ FLiBe TR-EIP realization`

`→ executable components`

FRP remains a separate project and may be used only as a read-only executable reference for explicitly confirmed semantic correspondences.

Therefore:

`FRP ≠ TR-EIF`

`FRP ≠ TR-EIP`

---

## 4. Core FLiBe Semantic Boundaries

The FLiBe validation program preserves:

`formal ionic charge ≠ ternary polarity`

`graph coordination ≠ chemical bond`

`graph coordination ≠ experimental coordination`

`thermodynamic temperature ≠ oscillator phase`

`thermodynamic temperature ≠ oscillator frequency`

`resonance descriptor ≠ thermodynamic property`

`resonance region ≠ ternary state`

`ternary state ≠ energy`

`ternary state ≠ force`

`validation status ≠ ternary state`

`missing data ≠ active neutral 0`

`2 LiF : 1 BeF2 ≠ automatically 67 mol% LiF : 33 mol% BeF2`

---

## 5. Active Neutral Requirement

The balanced ternary state space remains:

`T = {-1, 0, 1}`

State:

`0`

is active neutral.

Its roles may include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

Direct committed opposite-polarity transitions remain prohibited:

`-1 → 1`

`1 → -1`

The required routes remain:

`-1 → 0 → 1`

`1 → 0 → -1`

Each route leg is a separate execution event.

---

## 6. Phase 10 Master-Plan Matrix

| Item | Requirement | Primary repository artifacts | Qualification evidence | Current status |
| --- | --- | --- | --- | --- |
| 10.1 | Composition and species | `species.py`, `composition.py`, `configuration.py`, `charge.py`, `mass.py` | species, composition, configuration, charge, mass invariant tests | `EXECUTABLE_QUALIFIED` |
| 10.2 | Primary thermodynamic sources | `docs/references/flibe_sources.md`, `thermodynamic_state.py`, `density.py`, `units.py` | source register plus thermodynamic/density/unit invariant tests | `SOURCE_REGISTERED` |
| 10.3 | Structural reference data | `docs/references/flibe_sources.md`, `coordination.py` | structural-source register plus coordination invariant tests | `SOURCE_REGISTERED` |
| 10.4 | Transport reference data | `docs/references/flibe_sources.md` | source-register transport sections | `SOURCE_REGISTERED_PARTIAL` |
| 10.5 | Training and validation configurations | `dataset_configuration.py` | `test_flibe_dataset_configuration_invariants.py` | `EXECUTABLE_QUALIFIED` |
| 10.6 | FLiBe-specific resonance descriptors | `resonance_parameterization.py`, `resonance_descriptor.py` | resonance parameterization and descriptor invariant tests | `EXECUTABLE_QUALIFIED` |
| 10.7 | FLiBe-specific TR-EIP realization | `tr_eip.py` | `test_flibe_tr_eip.py` | `EXECUTABLE_QUALIFIED` |
| 10.8 | Molecular-dynamics validation | existing TR-EIF MD layer plus FLiBe TR-EIP realization | `test_flibe_molecular_dynamics_validation.py` | `EXECUTABLE_QUALIFIED` |
| 10.9 | Multiscale coolant closure | `multiscale_coolant.py` plus generic multiscale closures | FLiBe coolant invariant and integration tests | `EXECUTABLE_QUALIFIED` |
| 10.10 | Experimental and first-principles comparison | `reference_comparison.py` | `test_flibe_reference_comparison.py` | `CONTRACT_QUALIFIED` |

---

## 7. Phase 10.1 Composition and Species

### Executable artifacts

The current implementation includes:

`src/tr_eif/flibe/species.py`

`src/tr_eif/flibe/composition.py`

`src/tr_eif/flibe/configuration.py`

`src/tr_eif/flibe/charge.py`

`src/tr_eif/flibe/mass.py`

### Qualification artifacts

Current invariant qualification includes:

`tests/invariants/test_flibe_species_invariants.py`

`tests/invariants/test_flibe_composition_invariants.py`

`tests/invariants/test_flibe_configuration_invariants.py`

`tests/invariants/test_flibe_charge_invariants.py`

`tests/invariants/test_flibe_mass_invariants.py`

### Validated executable boundaries

The qualification establishes executable contracts for:

- accepted FLiBe species;
- composition representation;
- configuration species cardinality;
- formal charge representation;
- mass representation.

### Scientific boundary

Formal charge is not balanced-ternary polarity.

Therefore:

`formal ionic charge ≠ -1/0/1 execution state`

### Status

`EXECUTABLE_QUALIFIED`

---

## 8. Exact Composition Boundary

The repository distinguishes exact formula-unit composition from rounded source compositions.

Exact:

`2 LiF : 1 BeF2`

is not mathematically identical to:

`67 mol% LiF : 33 mol% BeF2`

Therefore:

`2:1 ≠ 67:33`

A source value reported for one composition must not be silently assigned to the other.

Composition-equivalence assumptions require an explicit scientific justification.

---

## 9. Phase 10.2 Primary Thermodynamic Sources

### Source register

The current FLiBe source register contains provenance anchors for thermodynamic and thermophysical evidence including:

- LiF-BeF2 phase-equilibrium sources;
- liquidus qualification;
- density;
- viscosity;
- enthalpy;
- heat capacity;
- modern thermophysical measurements.

### Registered source identifiers include

`FLIBE-PRIMARY-ROY-1950-PHASE`

`FLIBE-PRIMARY-ROY-1954-PHASE`

`FLIBE-PRIMARY-ROMBERGER-1972-LIQUIDUS`

`FLIBE-PRIMARY-CANTOR-WARD-MOYNIHAN-1969`

`FLIBE-REFERENCE-JANZ-1974-DENSITY`

`FLIBE-PRIMARY-DOUGLAS-PAYNE-1969`

`FLIBE-PRIMARY-REDKIN-2021-THERMOPHYSICAL`

`FLIBE-SOURCE-CANTOR-1968-ORNL-TM-2316`

### Executable thermodynamic artifacts

`src/tr_eif/flibe/thermodynamic_state.py`

`src/tr_eif/flibe/density.py`

`src/tr_eif/flibe/units.py`

### Qualification artifacts

`tests/invariants/test_flibe_thermodynamic_state_invariants.py`

`tests/invariants/test_flibe_density_invariants.py`

`tests/invariants/test_flibe_units_invariants.py`

### Status

Source provenance is registered.

The executable density interface is qualified.

The source register itself does not imply that every thermodynamic quantity has an executable physical model.

Current status:

`SOURCE_REGISTERED`

---

## 10. Thermodynamic-State Boundary

`FLiBeThermodynamicState` records thermodynamic state variables.

Thermodynamic temperature and pressure remain distinct from:

- oscillator phase;
- oscillator frequency;
- phase-order observable;
- ternary state;
- validation status.

Therefore:

`temperature ≠ oscillator phase`

`temperature ≠ ternary state`

`pressure ≠ ternary state`

---

## 11. Density Validation Boundary

The executable density model supports explicit provenance.

A density evaluator may use:

- source-backed relation;
- calibrated relation;
- benchmark fixture;
- test fixture.

The provenance class must remain explicit.

A benchmark fixture must not be presented as experimental density evidence.

---

## 12. Registered Density Reproduction Reference

The source register contains:

`FLIBE-REFERENCE-JANZ-1974-DENSITY`

The registered relation is a source-derived density correlation with:

- explicit source identity;
- explicit source composition;
- explicit temperature range;
- explicit units;
- explicit `DERIVED` provenance.

The benchmark implementation is:

`benchmarks/flibe/reference_property_reproduction.py`

Its scientific scope is density-correlation reproduction.

It does not validate all FLiBe thermophysical properties.

---

## 13. Phase 10.3 Structural Reference Data

### Registered structural evidence

The source register currently contains structural provenance anchors including:

`FLIBE-PRIMARY-FAYFAR-2024-TOTAL-SCATTERING`

`FLIBE-PRIMARY-FU-2023-NMR`

`FLIBE-PRIMARY-GARDNER-2025-SOLID-DIFFRACTION`

`FLIBE-COMPUTATIONAL-SALANNE-2006-NETWORK`

### Evidence classes represented

The current structural register includes evidence for:

- experimental total scattering;
- experimental NMR local structure;
- solid diffraction structure;
- computational Be-F network structure.

### Executable structural artifact

`src/tr_eif/flibe/coordination.py`

### Qualification artifact

`tests/invariants/test_flibe_coordination_invariants.py`

### Boundary

The executable coordination state is graph-relative.

Therefore:

`graph coordination ≠ chemical bond`

and:

`graph coordination ≠ experimental coordination`

unless a validated mapping explicitly establishes the correspondence.

### Status

`SOURCE_REGISTERED`

---

## 14. Structural Numerical Dataset Boundary

The source register establishes provenance anchors.

It does not itself introduce a complete executable numerical structural dataset.

Therefore:

`source registered ≠ numerical dataset implemented`

A later executable structural comparison must preserve:

- observable identity;
- source;
- composition;
- thermodynamic state;
- axis;
- normalization;
- units;
- provenance.

---

## 15. Phase 10.4 Transport Reference Data

### Registered transport evidence

The source register currently contains provenance anchors for:

- viscosity;
- thermal conductivity;
- electrical conductivity;
- deuterium diffusivity and solubility;
- tritium diffusivity, permeability, and solubility.

### Registered transport identifiers include

`FLIBE-PRIMARY-CANTOR-WARD-MOYNIHAN-1969-VISCOSITY`

`FLIBE-PRIMARY-COOKE-1971-THERMAL-CONDUCTIVITY`

`FLIBE-METHOD-COOKE-1973-VARIABLE-GAP`

`FLIBE-PRIMARY-ROBBINS-BRAUNSTEIN-1970-ELECTRICAL-CONDUCTIVITY`

`FLIBE-PRIMARY-ANDERL-2004-DEUTERIUM-TRANSPORT`

`FLIBE-PRIMARY-CALDERONI-2008-TRITIUM-PERMEATION`

### Explicit current source boundary

Experimental salt-ion self-diffusion coefficients for:

- Li;
- Be;
- F

are not established by the current source register.

Computational self-diffusion data, if admitted, must remain computational evidence and must not be relabeled as experimental evidence.

### Executable dataset boundary

The current source-register section does not create executable transport-property datasets.

### Status

`SOURCE_REGISTERED_PARTIAL`

---

## 16. Transport Observable Separation

Transport observables must remain distinct.

Examples include:

`viscosity ≠ thermal conductivity`

`thermal conductivity ≠ electrical conductivity`

`species diffusivity ≠ permeability`

`permeability ≠ solubility`

`hydrogen-isotope diffusivity ≠ Li/Be/F self-diffusivity`

A source for one transport quantity must not be used as direct evidence for another.

---

## 17. Phase 10.5 Training and Validation Configurations

### Executable artifact

`src/tr_eif/flibe/dataset_configuration.py`

### Principal types

`FLiBeDatasetSplit`

`FLiBeDatasetConfiguration`

`validate_flibe_split_isolation`

### Dataset roles

The declared split labels are:

`TRAINING`

`VALIDATION`

`TEST`

These labels are dataset metadata.

They are not ternary states.

Therefore:

`TRAINING/VALIDATION/TEST ≠ -1/0/1`

### Qualification

`tests/invariants/test_flibe_dataset_configuration_invariants.py`

### Qualification scope

The test suite validates:

- required identifiers;
- provenance metadata;
- source identifiers;
- split labels;
- exact configuration isolation;
- group isolation;
- trajectory isolation;
- known parent-derived isolation;
- deterministic validation.

### Status

`EXECUTABLE_QUALIFIED`

---

## 18. Dataset Leakage Invariant

The strict split-isolation contract prohibits the same declared configuration identity from crossing dataset roles.

Related data identified by:

- group;
- trajectory;
- known parent-derived relationship

must remain isolated under the declared split contract.

This is a dataset-validation invariant.

It is not a ternary transition rule.

---

## 19. Phase 10.6 FLiBe-Specific Resonance Descriptors

### Executable artifacts

`src/tr_eif/flibe/resonance_parameterization.py`

`src/tr_eif/flibe/resonance_descriptor.py`

### Principal interfaces

`FLiBeResonanceParameterization`

`ConstantFLiBeResonanceParameters`

`evaluate_resonance_parameters`

`FLiBeResonanceDescriptor`

`build_flibe_resonance_descriptor`

### Qualification artifacts

`tests/invariants/test_flibe_resonance_parameterization_invariants.py`

`tests/invariants/test_flibe_resonance_descriptor_invariants.py`

### Validated boundaries

The executable descriptor preserves explicit separation among:

- FLiBe configuration;
- graph-relative coordination;
- thermodynamic state;
- continuous resonance state;
- provenance.

The base resonance coordinate remains continuous.

### Status

`EXECUTABLE_QUALIFIED`

---

## 20. FLiBe Resonance Coordinate

The current executable base descriptor uses:

`phase_order`

and:

`frequency_spread`

as continuous descriptor channels.

The descriptor does not automatically encode:

- density;
- temperature;
- pressure;
- coordination;
- ternary state.

Therefore:

`resonance descriptor ≠ thermodynamic state`

and:

`resonance descriptor ≠ ternary state`

---

## 21. Resonance Provenance Boundary

An executable resonance parameterization may carry:

`ParameterProvenance`

The existence of an executable parameterization interface does not establish source-backed physical parameter values.

A physical FLiBe resonance parameter set requires explicit provenance.

---

## 22. Phase 10.7 FLiBe-Specific TR-EIP Realization

### Executable artifact

`src/tr_eif/flibe/tr_eip.py`

### Principal interfaces

`FLiBeTREIPModel`

`FLiBeTREIPResult`

`append_flibe_resonance_channels`

### Qualification artifact

`tests/integration/test_flibe_tr_eip.py`

### Architecture validated

The executable chain is:

`FLiBe atomic geometry`

`→ E(3)-equivariant representation`

`→ continuous resonance scalar channels`

`→ retained -1/0/1 conditioning`

`→ conservative scalar energy`

### Status

`EXECUTABLE_QUALIFIED`

---

## 23. Independent Resonance Pathway

Qualification demonstrates that changing resonance state while retaining the same ternary state can change the energy pathway under the configured model.

This establishes an executable resonance-conditioning path.

It does not establish a universal physical resonance law for FLiBe.

---

## 24. Independent Ternary Pathway

Qualification demonstrates that changing retained ternary execution state while retaining the same resonance state can change the energy pathway under the configured model.

This establishes an executable ternary-conditioning path.

It does not convert ternary state into energy.

---

## 25. Active-Neutral TR-EIP Path

Retained active neutral:

`0`

uses its own explicit conditioning semantics.

It is not implemented as missing conditioning.

It is not required to multiply features by numerical zero.

Therefore:

`active neutral ≠ passive absence`

---

## 26. Phase 10.8 Molecular-Dynamics Validation

### Existing generic MD layer

FLiBe uses the existing TR-EIF molecular-dynamics layer.

A separate FLiBe MD engine is not introduced.

### FLiBe qualification artifact

`tests/integration/test_flibe_molecular_dynamics_validation.py`

### Validated executable relations include

- TR-EIP-conditioned energy enters force evaluation;
- species identity is preserved;
- composition is preserved;
- atom cardinality is preserved;
- retained ternary state is not silently evolved;
- resonance state is not silently evolved;
- pending target does not replace retained state;
- resonance state can affect forces;
- ternary state can independently affect forces;
- post-step resonance rebinding is explicit;
- benchmark fixture energy drift is bounded.

### Status

`EXECUTABLE_QUALIFIED`

---

## 27. MD Physical-Validation Boundary

The FLiBe MD integration test uses controlled executable fixtures.

It validates execution architecture.

It does not by itself establish:

- experimental transport accuracy;
- first-principles trajectory agreement;
- bulk thermodynamic accuracy;
- phase-equilibrium accuracy;
- chemically complete FLiBe dynamics.

Therefore:

`MD executable qualification ≠ complete FLiBe physical validation`

---

## 28. Phase 10.9 Multiscale Coolant Closure

### Executable artifact

`src/tr_eif/flibe/multiscale_coolant.py`

### Principal interface

`FLiBeMultiscaleCoolantModel`

### Qualification artifacts

`tests/invariants/test_flibe_multiscale_coolant_invariants.py`

`tests/integration/test_flibe_multiscale_coolant_closure.py`

### Generic multiscale layers used

The integration path uses existing TR-EIF structures for:

- partitioning;
- reduction;
- geometry;
- hierarchy;
- mesoscale closure;
- continuum closure;
- transport transfer;
- thermodynamic consistency;
- uncertainty propagation;
- engineering boundaries.

### Status

`EXECUTABLE_QUALIFIED`

---

## 29. Multiscale Physical-Closure Boundary

Executable closure chaining does not by itself establish physical validity of every closure coefficient or constitutive relation.

Therefore:

`closure implemented ≠ closure physically validated`

Material-specific physical closure requires source-backed data and cross-scale validation.

---

## 30. Ternary Multiscale Boundary

Balanced ternary states are not arithmetically averaged across scales.

Therefore:

`mean(-1, 1) = 0`

does not establish active-neutral coarse state.

No generic ternary averaging operator is admitted.

---

## 31. Phase 10.10 Experimental and First-Principles Comparison

### Executable artifact

`src/tr_eif/flibe/reference_comparison.py`

### Principal interfaces

`FLiBeEvidenceKind`

`FLiBeReferenceObservable`

`FLiBeReferenceComparison`

`compare_flibe_experimental_first_principles`

### Qualification artifact

`tests/integration/test_flibe_reference_comparison.py`

### Qualified comparison contract

Direct comparison requires matched:

- observable;
- composition;
- thermodynamic state;
- physical state;
- value unit;
- normalization;
- axis;
- sample count.

Experimental and first-principles evidence remain separate.

### Residual convention

The executable comparison uses:

`first_principles - experimental`

for residuals.

It also reports:

- absolute residual;
- MAE;
- RMSE;
- maximum absolute error.

### Status

`CONTRACT_QUALIFIED`

---

## 32. Phase 10.10 Scientific Evidence Gap

The comparison machinery is executable and qualified.

However, the current repository does not yet contain a committed matched source-backed numerical pair that performs an actual experimental-versus-first-principles FLiBe comparison through this contract.

Therefore:

`comparison contract qualified ≠ physical comparison completed`

The current scientific status of the actual experimental/first-principles comparison is:

`REQUIRES_SOURCE`

This is a scientific-evidence gap, not an executable-contract failure.

---

## 33. First-Principles Evidence Boundary

The source register defines the admission boundary for first-principles data.

An admitted first-principles dataset must preserve applicable metadata such as:

- method;
- exchange-correlation treatment where applicable;
- basis or plane-wave settings where applicable;
- convergence controls;
- composition;
- state;
- sampling protocol.

First-principles evidence must not be relabeled as experimental evidence.

---

## 34. Phase 10 Current Revision Result

The current Phase 10 implementation and source matrix shows:

| Phase 10 item | Revision result |
| --- | --- |
| 10.1 Composition and species | `EXECUTABLE_QUALIFIED` |
| 10.2 Primary thermodynamic sources | `SOURCE_REGISTERED` |
| 10.3 Structural reference data | `SOURCE_REGISTERED` |
| 10.4 Transport reference data | `SOURCE_REGISTERED_PARTIAL` |
| 10.5 Training and validation configurations | `EXECUTABLE_QUALIFIED` |
| 10.6 FLiBe-specific resonance descriptors | `EXECUTABLE_QUALIFIED` |
| 10.7 FLiBe-specific TR-EIP realization | `EXECUTABLE_QUALIFIED` |
| 10.8 Molecular-dynamics validation | `EXECUTABLE_QUALIFIED` |
| 10.9 Multiscale coolant closure | `EXECUTABLE_QUALIFIED` |
| 10.10 Experimental/first-principles comparison | `CONTRACT_QUALIFIED`, scientific comparison `REQUIRES_SOURCE` |

This matrix distinguishes functional executable coverage from physical evidence closure.

---

## 35. Phase 11 Benchmark Matrix

| Item | Requirement | Benchmark artifact | CI qualification artifact | Current status |
| --- | --- | --- | --- | --- |
| 11.1 | Correctness | `reference_correctness.py` | `tests/determinism/test_flibe_reference_correctness_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.2 | Determinism | byte-determinism checks embedded in qualified FLiBe benchmarks | determinism qualification tests | `BENCHMARK_CI_QUALIFIED` |
| 11.3 | Equivariance | `reference_equivariance.py` | `tests/equivariance/test_flibe_reference_equivariance_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.4 | Conservation | `reference_conservation.py` | `tests/conservation/test_flibe_reference_conservation_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.5 | Numerical convergence | `reference_numerical_convergence.py` | `tests/numerical/test_flibe_reference_numerical_convergence_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.6 | Scaling | `reference_scaling.py` | `tests/determinism/test_flibe_reference_scaling_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.7 | Memory use | `reference_memory.py` | `tests/numerical/test_flibe_reference_memory_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.8 | Runtime | `reference_runtime.py` | `tests/numerical/test_flibe_reference_runtime_benchmark.py` | `BENCHMARK_CI_QUALIFIED` |
| 11.9 | FLiBe property reproduction | `reference_property_reproduction.py` | no dedicated committed benchmark qualification test in the current snapshot | `BENCHMARK_IMPLEMENTED`, `REQUIRES_TEST` |
| 11.10 | Cross-model comparison | no dedicated FLiBe cross-model benchmark artifact in the current snapshot | none | `NOT_IMPLEMENTED` |

---

## 36. Phase 11.1 Correctness

The correctness benchmark validates fixed executable TR-EIP reference-path outputs.

It includes structured checks for:

- configuration cardinality;
- graph cardinality;
- composition;
- resonance coordinate;
- retained ternary state;
- feature-channel width;
- atomic energies;
- total energy.

Pinned benchmark values use:

`BENCHMARK`

provenance.

They are not physical FLiBe property evidence.

---

## 37. Phase 11.2 Determinism

Determinism qualification includes independent repeated execution and byte-identical structured JSON checks where the benchmark output is intended to be deterministic.

Runtime and memory measurements are excluded from exact byte-value identity because their measured magnitudes are environment-dependent.

Therefore:

`deterministic model output ≠ deterministic runtime`

and:

`deterministic model output ≠ deterministic memory magnitude`

---

## 38. Phase 11.3 Equivariance

The E(3) benchmark covers transformations including:

- translation;
- proper rotation;
- reflection;
- additional axis rotation.

The benchmark checks:

- graph cardinality preservation;
- resonance-coordinate preservation;
- scalar energy invariance;
- force equivariance.

This benchmark validates the declared executable transformation behavior of the reference fixture.

---

## 39. Phase 11.4 Conservation

The conservation benchmark executes a fixed FLiBe TR-EIP molecular-dynamics fixture.

It records:

- kinetic energy;
- potential energy;
- total energy;
- final signed drift;
- maximum absolute drift;
- retained ternary state;
- resonance coordinate.

The drift bound is benchmark-specific.

It is not a universal FLiBe conservation constant.

---

## 40. Phase 11.5 Numerical Convergence

The numerical-convergence benchmark refines the coordinate differentiation step for force evaluation.

It records:

- refinement steps;
- maximum force-component error;
- reduction ratios;
- reference differentiation step;
- final error.

The benchmark checks the declared second-order central-difference convergence regime.

---

## 41. Phase 11.6 Scaling

The scaling benchmark uses isolated replicated FLiBe fixtures.

It validates structural scaling such as:

- atom count;
- graph edge count;
- atomic-energy cardinality;
- extensive total energy for noninteracting replicas;
- constant energy per replica;
- composition preservation;
- resonance-coordinate preservation;
- ternary cardinality;
- feature-channel width.

This is structural size scaling.

It is not a runtime-complexity proof.

---

## 42. Phase 11.7 Memory Use

The memory benchmark uses:

`python-tracemalloc`

It measures:

- current traced allocation;
- peak traced allocation;
- peak bytes per atom.

The benchmark deliberately contains no universal absolute memory limit.

Memory magnitude is execution-environment dependent.

---

## 43. Phase 11.8 Runtime

The runtime benchmark uses:

`time.perf_counter_ns`

with:

- warm-up executions;
- repeated measured executions;
- minimum runtime;
- median runtime;
- maximum runtime;
- median runtime per atom.

The benchmark deliberately contains no hard runtime correctness threshold.

Runtime magnitude is shared-runner dependent.

---

## 44. Phase 11.9 Property Reproduction

### Benchmark artifact

`benchmarks/flibe/reference_property_reproduction.py`

### Current property target

The current benchmark reproduces the registered source-derived FLiBe density relation.

### Source identity

`FLIBE-REFERENCE-JANZ-1974-DENSITY`

### Benchmark boundary

The benchmark checks:

- source composition;
- source temperature domain;
- density metadata;
- registered reference points;
- monotonic relation across the sampled source interval;
- rejection outside the registered domain.

### Current qualification status

The benchmark implementation exists.

A dedicated committed CI qualification test invoking this benchmark is not present in the current reviewed snapshot.

Therefore current status is:

`BENCHMARK_IMPLEMENTED`

plus:

`REQUIRES_TEST`

---

## 45. Property Reproduction Does Not Validate All FLiBe Properties

Successful density-correlation reproduction does not establish:

- viscosity reproduction;
- thermal-conductivity reproduction;
- electrical-conductivity reproduction;
- diffusivity reproduction;
- phase-equilibrium reproduction;
- structural-observable reproduction.

Each observable requires its own source-backed comparison.

---

## 46. Phase 11.10 Cross-Model Comparison

A dedicated FLiBe cross-model benchmark is not present in the current reviewed snapshot.

The existing:

`reference_comparison.py`

compares experimental and first-principles reference observables.

That is not automatically the Phase 11.10 cross-model benchmark.

A cross-model benchmark requires at least two concrete model outputs under a common declared comparison domain.

### Current status

`NOT_IMPLEMENTED`

---

## 47. Cross-Model Comparison Requirements

A future valid cross-model comparison must preserve identical or explicitly mapped:

- atomic configuration;
- composition;
- thermodynamic state;
- observable;
- units;
- normalization;
- model domain;
- sampling conditions.

Model-name similarity does not establish comparability.

---

## 48. Cross-Model Identity Boundary

A cross-model comparison may establish:

- numerical agreement;
- residual relation;
- observable equivalence under a declared mapping.

It does not establish architectural identity.

Therefore:

`matching output ≠ identical model`

---

## 49. Experimental Evidence Matrix

| Evidence domain | Current source state | Executable comparison state |
| --- | --- | --- |
| Phase equilibrium | source provenance registered | no dedicated executable reproduction benchmark |
| Density | source provenance registered | source-derived density model and reproduction benchmark exist |
| Viscosity | source provenance registered | no dedicated physical reproduction benchmark |
| Enthalpy / heat capacity | source provenance registered | no dedicated physical reproduction benchmark |
| Total scattering | source provenance registered | no committed numerical structural comparison dataset |
| NMR local structure | source provenance registered | no committed numerical structural comparison dataset |
| Solid diffraction | source provenance registered | no committed numerical structural comparison dataset |
| Thermal conductivity | source provenance registered | no dedicated physical reproduction benchmark |
| Electrical conductivity | source provenance registered | no dedicated physical reproduction benchmark |
| Deuterium transport | source provenance registered | no dedicated physical reproduction benchmark |
| Tritium transport | source provenance registered | no dedicated physical reproduction benchmark |

---

## 50. First-Principles Evidence Matrix

The current repository contains an explicit first-principles evidence admission boundary.

The current reviewed snapshot does not contain a matched executable first-principles numerical dataset used through:

`FLiBeReferenceComparison`

against experimental values.

Therefore the actual Phase 10.10 physical comparison remains:

`REQUIRES_SOURCE`

---

## 51. Computational Structural Evidence

`FLIBE-COMPUTATIONAL-SALANNE-2006-NETWORK`

is recorded as computational structural evidence.

Computational evidence remains distinct from:

- experimental evidence;
- first-principles evidence unless the registered method satisfies that classification;
- executable TR-EIP output.

The evidence class must be preserved exactly.

---

## 52. Provenance Admission Matrix

| Provenance | Permitted role |
| --- | --- |
| `PRIMARY_SOURCE` | directly source-reported datum under matching conditions |
| `DERIVED` | explicit transformation of source-backed data |
| `CALIBRATED` | parameter or quantity obtained by declared calibration |
| `AUTHOR_DEFINED` | framework-defined construction |
| `BENCHMARK` | fixed benchmark fixture/result |
| `TEST_FIXTURE` | synthetic execution-test data |
| `REQUIRES_SOURCE` | scientific source provenance incomplete |
| `REQUIRES_TEST` | executable qualification incomplete |

No provenance class is a ternary state.

---

## 53. Source Admission Requirements

Before a physical FLiBe quantity enters executable scientific validation, its record must identify applicable metadata including:

- observable;
- composition;
- transported species where applicable;
- temperature;
- pressure where applicable;
- physical state;
- method;
- numerical value or functional form;
- unit;
- source identifier;
- provenance;
- source location;
- uncertainty when available;
- measured, fitted, derived, or computational status;
- interpolation or extrapolation status;
- applicable domain.

---

## 54. Comparison Admission Requirements

A direct source/model comparison requires compatibility of:

- observable;
- composition;
- thermodynamic state;
- physical state;
- units;
- normalization;
- axis;
- sample coordinates;
- sample cardinality.

If one of these conditions differs, a direct comparison is invalid unless an explicit transformation maps the domains.

---

## 55. Unit Boundary

No physical comparison may rely on implicit unit conversion.

Any conversion must preserve:

- source unit;
- target unit;
- conversion relation.

Numerical equality without unit compatibility has no scientific validation meaning.

---

## 56. Interpolation Boundary

Interpolation is admissible only when:

- it remains inside the declared source domain;
- the interpolation relation is explicit;
- the source permits the represented relation.

Interpolation must retain:

`DERIVED`

provenance when applicable.

---

## 57. Extrapolation Boundary

Extrapolation outside a source validity domain must be identified explicitly.

It must not be presented as direct source-qualified reproduction.

---

## 58. Experimental and Computational Separation

Experimental measurements and computational outputs must remain distinguishable.

Therefore:

`experimental ≠ computational`

even when the values agree.

Agreement is a comparison result.

It does not merge evidence classes.

---

## 59. FLiBe TR-EIP Validation Chain

The current executable FLiBe TR-EIP validation chain is:

`FLiBeConfiguration`

`→ graph-relative coordination`

`→ FLiBeResonanceDescriptor`

`→ continuous resonance channels`

`→ retained -1/0/1 conditioning`

`→ E(3)-equivariant message passing`

`→ conservative energy`

`→ force/stress or MD`

`→ multiscale closure where selected`

`→ structured validation`

Each layer retains its own semantic type.

---

## 60. No Semantic Collapse

The validation matrix prohibits the following collapses:

`thermodynamic temperature = resonance frequency`

`resonance region = ternary state`

`graph coordination = chemical bond`

`formal ionic charge = ternary polarity`

`active neutral 0 = missing`

`zero energy = active neutral`

`validation PASS = ternary 1`

`validation FAIL = ternary -1`

---

## 61. Physical Validation Does Not Rewrite Ternary State

A physical comparison result must not modify the recorded ternary execution state merely to encode agreement or disagreement.

Validation evidence remains separate from execution state.

---

## 62. Benchmark Validation Does Not Rewrite Physical Evidence

A green benchmark status does not transform:

`BENCHMARK`

or:

`TEST_FIXTURE`

data into:

`PRIMARY_SOURCE`

evidence.

Provenance remains invariant under test success.

---

## 63. CI Matrix

Current automatic CI provides independent validation paths including:

- Python smoke test;
- structured output;
- deterministic validation bench;
- full self-test;
- complete root schema validation.

FLiBe benchmark qualification tests are executed according to their test directories and workflow configuration.

---

## 64. Clean-Runner Evidence

A green CI result establishes successful execution of the configured checks for the exact tested revision.

It does not establish unconfigured scientific comparisons.

Therefore:

`green CI ≠ untested physical validation`

---

## 65. Local Snapshot Evidence

The fresh repository ZIP remains the authoritative snapshot for full revision.

Local review and clean-runner CI are independent validation contexts.

A discrepancy between them requires investigation.

---

## 66. Current Unresolved Validation Conditions

The current revision matrix identifies the following explicit unresolved conditions:

1. Transport source coverage does not establish experimental Li/Be/F salt-ion self-diffusion data.
2. Registered structural sources are not yet represented as complete executable numerical structural datasets.
3. The experimental-versus-first-principles comparison contract is qualified, but a committed matched source-backed numerical comparison pair is not present.
4. The FLiBe property-reproduction benchmark exists but lacks a dedicated committed CI qualification test in the reviewed snapshot.
5. A dedicated Phase 11.10 FLiBe cross-model comparison benchmark is not present.

These are validation-state statements.

None is encoded through ternary state `0`.

---

## 67. Revision Rule

A matrix row may move to a stronger validation status only when the required evidence artifact exists.

For example:

`BENCHMARK_IMPLEMENTED`

may become:

`BENCHMARK_CI_QUALIFIED`

only after the benchmark is actually executed by a committed qualification test in CI.

Likewise:

`CONTRACT_QUALIFIED`

may become a source-backed scientific-comparison status only after actual independent evidence is admitted and compared.

---

## 68. No Status Promotion by Similarity

A validation state must not be promoted because an adjacent artifact looks similar to the required artifact.

Therefore:

`similar evidence ≠ required evidence`

`related test ≠ missing qualification test`

`comparison contract ≠ completed comparison`

---

## 69. Phase Closure Rule

A master-plan phase is scientifically closed only when every required item is satisfied at the evidence level implied by that item.

Executable implementation and physical evidence are separate closure dimensions where the plan requires both.

---

## 70. Phase 10 Revision Boundary

The current revision confirms broad executable coverage of Phase 10.

It also identifies source-level limitations that remain explicit.

In particular, Phase 10.10 has an executable comparison contract but lacks a committed matched experimental/first-principles numerical comparison dataset.

The matrix therefore does not represent Phase 10.10 as fully source-closed.

---

## 71. Phase 11 Revision Boundary

The current revision confirms CI-qualified benchmark coverage through:

- correctness;
- determinism;
- equivariance;
- conservation;
- numerical convergence;
- scaling;
- memory;
- runtime.

Property reproduction is implemented but requires dedicated CI qualification.

Cross-model comparison remains unimplemented as a dedicated benchmark.

---

## 72. Release Relevance

Before Phase 12 release closure, this matrix must be reviewed against:

- scientific claim audit;
- citation audit;
- schema audit;
- reproducibility audit;
- benchmark status;
- source status;
- unresolved evidence conditions.

No unresolved row may be silently described as validated.

---

## 73. Core FLiBe Validation Invariants

The FLiBe validation matrix preserves:

1. Exact composition identity.
2. Explicit species identity.
3. Formal charge separation from ternary state.
4. Thermodynamic state separation from resonance state.
5. Resonance state separation from ternary state.
6. Active neutral `0` as an executed state.
7. Direct opposite committed transition prohibition.
8. Pending target separation.
9. E(3) geometry preservation.
10. Conservative energy semantics.
11. Force-gradient semantics.
12. Stress-convention semantics.
13. No hidden resonance evolution in generic MD.
14. No hidden ternary evolution in generic MD.
15. No arithmetic ternary averaging across scales.
16. Source provenance preservation.
17. Experimental/computational evidence separation.
18. Benchmark/test-fixture separation from physical evidence.
19. Dataset split isolation.
20. Validation status separation from ternary state.
21. Source-domain enforcement.
22. Unit compatibility.
23. Comparison-domain compatibility.
24. Similarity does not establish identity.

---

## 74. Related Artifacts

The FLiBe validation matrix is used together with:

`docs/validation/scientific_validation_plan.md`

`docs/validation/mathematical_validation_plan.md`

`docs/validation/numerical_validation_plan.md`

`docs/validation/invariant_validation_plan.md`

`docs/validation/reproducibility_plan.md`

`docs/references/flibe_sources.md`

and the committed FLiBe implementation, test, benchmark, and schema artifacts.

---

## 75. Summary

The FLiBe validation program is divided into three separate evidence layers:

`source provenance`

`+ executable qualification`

`+ scientific comparison`

A source record does not automatically create an executable model.

An executable model does not automatically establish physical accuracy.

A benchmark does not automatically become physical evidence.

The current repository contains substantial executable FLiBe coverage, while the matrix preserves the remaining source and comparison boundaries explicitly.

The controlling rule remains:

`similar ≠ identical`

and:

`green execution ≠ untested scientific claim`

Validation closes only where the required artifact, provenance, comparison domain, and qualification evidence all exist.
