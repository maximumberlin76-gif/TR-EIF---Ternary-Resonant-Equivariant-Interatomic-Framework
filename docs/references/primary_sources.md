# Primary Sources

## 1. Scope

This document defines the repository-level source-provenance and evidence-admission contract of the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

It defines:

- source classes;
- evidence roles;
- primary-source admission;
- derived-source admission;
- calibration provenance;
- author-defined content;
- benchmark provenance;
- test-fixture provenance;
- unresolved source state;
- unresolved test state;
- bibliographic identity;
- claim-to-source correspondence;
- source-domain correspondence;
- quotation and paraphrase boundaries;
- numerical data extraction;
- interpolation;
- extrapolation;
- unit conversion;
- derived values;
- source conflicts;
- source supersession;
- repository source registers;
- release citation audit.

This document is a source-policy and source-index artifact.

Detailed domain-specific bibliographies are maintained separately.

---

## 2. Repository Source Registers

The approved reference structure contains:

`docs/references/primary_sources.md`

`docs/references/kuramoto_sakaguchi_sources.md`

`docs/references/equivariant_model_sources.md`

`docs/references/interatomic_potential_sources.md`

`docs/references/molecular_dynamics_sources.md`

`docs/references/flibe_sources.md`

These registers have different scopes.

They must not be collapsed into one undifferentiated bibliography.

---

## 3. Source Register Roles

The intended roles are:

### `primary_sources.md`

Repository-level evidence and provenance contract.

### `kuramoto_sakaguchi_sources.md`

Primary and foundational sources for phase-oscillator dynamics, Kuramoto-type coupling, Sakaguchi phase lag, synchronization, and directly related mathematical background used by TR-EIF.

### `equivariant_model_sources.md`

Sources for E(3), SE(3), O(3), SO(3), equivariant representations, equivariant message passing, and equivariant interatomic model architectures.

### `interatomic_potential_sources.md`

Sources for conservative interatomic modeling, energy-based potentials, force derivation, stress derivation, machine-learned interatomic potentials, and related model families.

### `molecular_dynamics_sources.md`

Sources for equations of motion, time integration, periodic boundaries, neighbor methods, thermostats, barostats, conservation, transport observables, and molecular-dynamics numerical methods.

### `flibe_sources.md`

Material-specific sources for FLiBe composition, phase relations, thermodynamic properties, transport properties, structural evidence, and material-specific comparison data.

---

## 4. Source Provenance Classes

TR-EIF uses the canonical provenance classes:

`PRIMARY_SOURCE`

`DERIVED`

`CALIBRATED`

`AUTHOR_DEFINED`

`BENCHMARK`

`TEST_FIXTURE`

`REQUIRES_SOURCE`

`REQUIRES_TEST`

These classes describe evidence provenance.

They are not balanced-ternary execution states.

---

## 5. Provenance Is Not Ternary State

The following identifications are invalid:

`PRIMARY_SOURCE ≠ 1`

`REQUIRES_SOURCE ≠ -1`

`REQUIRES_TEST ≠ 0`

`TEST_FIXTURE ≠ active neutral`

Validation and provenance state remain separate from:

`T = {-1, 0, 1}`

---

## 6. PRIMARY_SOURCE

`PRIMARY_SOURCE` applies when the cited source directly reports, derives as its own principal result, or formally introduces the specific quantity, method, observation, or relation being referenced.

Primary-source status is claim-specific.

A publication is not globally primary for every statement mentioned within it.

---

## 7. Primary-Source Claim Correspondence

For a claim:

`C`

and source:

`S`

primary-source admission requires that:

`S`

directly supports:

`C`

under the relevant conditions.

The fact that:

`S`

is scientifically reputable does not establish claim correspondence by itself.

---

## 8. Primary Source Is Not Review Source

A review article, handbook, database, technical assessment, or later compilation may provide useful evidence.

It is not automatically the primary source of the underlying measurement or method.

Its evidence role must be recorded accurately.

---

## 9. Reference Compilation

A reference-data compilation may be used when it:

- identifies the underlying source;
- reproduces a defined relation;
- provides evaluated values;
- documents a standard correlation.

Such evidence must remain identified as compilation or evaluated reference evidence where applicable.

It must not be silently relabeled as direct experimental measurement.

---

## 10. DERIVED

`DERIVED` applies when a repository quantity is calculated from one or more source-backed inputs through an explicit transformation.

A derived quantity must preserve its derivation chain.

---

## 11. Derived-Value Requirements

A derived value must identify, where applicable:

- source input;
- source identifier;
- mathematical transformation;
- unit transformation;
- assumptions;
- applicable domain;
- output value;
- output provenance.

---

## 12. Derived Does Not Become Primary

A value calculated from a primary-source datum remains derived.

Therefore:

`derived from PRIMARY_SOURCE ≠ PRIMARY_SOURCE`

The upstream provenance remains part of the derivation chain.

---

## 13. CALIBRATED

`CALIBRATED` applies to a parameter or quantity obtained through a declared calibration process.

Calibration must identify:

- calibration data;
- objective or fitting relation;
- parameter set;
- applicable domain;
- calibration procedure.

---

## 14. Calibration Is Not Independent Validation

A dataset used to calibrate a parameter is not independent validation evidence for the same fitted relation.

Therefore:

`calibration fit ≠ independent validation`

Independent validation requires a separate evidence path.

---

## 15. AUTHOR_DEFINED

`AUTHOR_DEFINED` applies to a framework-defined:

- mathematical construction;
- architecture;
- operator;
- semantic distinction;
- model interface;
- state contract;
- validation relation.

Author-defined status must not be presented as external empirical evidence.

---

## 16. Author-Defined Does Not Mean Arbitrary

An author-defined construct may be mathematically constrained and executable.

Its provenance class identifies origin.

It does not determine mathematical validity.

---

## 17. BENCHMARK

`BENCHMARK` applies to fixed benchmark inputs, outputs, thresholds, or reference artifacts created for repeatable evaluation.

Benchmark values may establish:

- correctness;
- determinism;
- equivariance;
- conservation;
- convergence;
- scaling behavior;
- runtime measurement;
- memory measurement.

They do not automatically establish physical material properties.

---

## 18. Benchmark Is Not Experimental Evidence

The following relation is invalid:

`benchmark PASS → experimental validation`

Benchmark evidence remains benchmark evidence.

---

## 19. TEST_FIXTURE

`TEST_FIXTURE` applies to synthetic data used solely to exercise executable behavior.

Test fixtures may intentionally use simplified or artificial:

- coordinates;
- masses;
- energies;
- temperatures;
- pressures;
- feature values;
- resonance states;
- ternary states.

They must not be cited as physical measurements.

---

## 20. Test Fixture Is Not Physical Parameter

A test-fixture numerical value must not migrate into material-specific public claims without independent source provenance.

Therefore:

`TEST_FIXTURE ≠ physical evidence`

---

## 21. REQUIRES_SOURCE

`REQUIRES_SOURCE` identifies a scientific value or claim whose required external provenance is not yet established.

It is an explicit unresolved evidence state.

It must not be replaced by a guessed source.

---

## 22. REQUIRES_TEST

`REQUIRES_TEST` identifies an executable claim or artifact that requires qualification before being treated as validated implementation behavior.

It is distinct from:

`REQUIRES_SOURCE`

---

## 23. Source Requirement vs Test Requirement

A quantity may simultaneously have:

- adequate source provenance;
- incomplete executable qualification.

Likewise an executable contract may be fully tested while lacking physical source evidence.

Therefore:

`source closure ≠ executable closure`

---

## 24. Evidence-Layer Separation

TR-EIF distinguishes at least:

`formal evidence`

`executable evidence`

`numerical evidence`

`source evidence`

`experimental evidence`

`first-principles evidence`

`benchmark evidence`

These evidence classes may support one claim from different directions.

They must remain distinguishable.

---

## 25. Citation Presence Is Not Evidence Sufficiency

The presence of a citation does not establish that the citation supports the specific statement.

Therefore:

`citation present ≠ claim supported`

A citation audit must verify claim correspondence.

---

## 26. Bibliographic Identity

Every source record should contain sufficient bibliographic information to identify the source unambiguously.

Depending on source type, this may include:

- authors;
- title;
- journal or report series;
- volume;
- issue;
- pages;
- year;
- DOI;
- report number;
- institutional identifier;
- stable archive identifier.

---

## 27. DOI Boundary

A DOI identifies a publication or registered object.

It does not by itself establish:

- relevance;
- primary-source status;
- data quality;
- claim correspondence.

---

## 28. URL Boundary

A mutable web URL is not sufficient archival identity by itself when stronger bibliographic identity exists.

URLs may be included for access.

Persistent identifiers are preferred for scientific source identity.

---

## 29. Repository Source Identifier

TR-EIF may assign a stable internal source identifier such as:

`SOURCE-ID`

to a registered external source.

The internal identifier must map to one unambiguous bibliographic source record.

---

## 30. Internal Identifier Is Not External Citation

An internal source identifier supports repository traceability.

It does not replace the external bibliographic citation.

---

## 31. Claim Granularity

Source qualification operates at claim granularity.

For example, one paper may directly support:

- density;

while not directly supporting:

- viscosity;
- thermal conductivity;
- phase diagram;
- diffusivity.

Each property requires its own source-role statement.

---

## 32. Observable Identity

A source record must preserve the exact observable being supported.

The following must not be interchanged:

`density ≠ viscosity`

`viscosity ≠ thermal conductivity`

`thermal conductivity ≠ electrical conductivity`

`diffusivity ≠ permeability`

`permeability ≠ solubility`

---

## 33. Structural Observable Identity

Structural observables remain distinct:

`structure factor ≠ pair-distribution function`

`pair-distribution function ≠ coordination number`

`coordination number ≠ chemical bond`

A source supporting one must not be cited as direct evidence for another without an explicit transformation.

---

## 34. Resonance Source Boundary

Sources for oscillator dynamics may support:

- phase equations;
- coupling structures;
- synchronization analysis;
- phase lag;
- order parameters.

They do not automatically support TR-EIF-specific:

- ternary routing;
- active-neutral semantics;
- interatomic realization;
- FLiBe parameterization.

---

## 35. Kuramoto Boundary

Classical Kuramoto-type literature supports the applicable phase-oscillator formalism.

It does not define the complete TR-EIF resonance architecture.

Therefore:

`Kuramoto model ≠ TR-EIF`

---

## 36. Sakaguchi Boundary

Sakaguchi-type phase-lag literature supports the applicable phase-lag extension.

It does not define:

- ternary active neutral;
- TR-EIP;
- E(3)-equivariant energy;
- FLiBe realization.

---

## 37. Synchronization Boundary

A synchronization source does not automatically establish resonance.

Therefore:

`synchronization source ≠ resonance proof`

The repository preserves:

`resonance ≠ synchronization`

---

## 38. Equivariant-Model Source Boundary

Sources for equivariant neural or interatomic models may support:

- representation theory usage;
- E(3)/SE(3) architecture;
- equivariant message passing;
- invariant energy design.

They do not automatically support TR-EIF ternary semantics.

---

## 39. Interatomic-Potential Source Boundary

A source for an interatomic potential or potential architecture may support:

- energy representation;
- force derivation;
- stress relation;
- fitting procedure.

It does not automatically validate TR-EIP or FLiBe-specific behavior.

---

## 40. Molecular-Dynamics Source Boundary

A molecular-dynamics source may support:

- integration method;
- thermostat;
- barostat;
- neighbor method;
- transport relation.

The source must correspond to the exact method being claimed.

---

## 41. Material-Specific Source Boundary

A FLiBe source must be used only within the material, composition, thermodynamic, and observable domain it supports.

A generic molten-salt result is not automatically FLiBe-specific evidence.

---

## 42. Composition Domain

Material-source qualification must preserve composition.

Exact:

`2 LiF : 1 BeF2`

is not identical to:

`67 mol% LiF : 33 mol% BeF2`

Therefore:

`2:1 ≠ 67:33`

unless an explicit approximation or equivalence relation is declared.

---

## 43. Temperature Domain

A temperature-dependent source must retain its applicable temperature range.

Values outside that range are not direct in-domain source values.

---

## 44. Pressure Domain

Where pressure affects the source result, pressure must remain explicit.

A value at one pressure must not be silently generalized to another.

---

## 45. Physical-State Domain

Source records should preserve relevant physical state such as:

- solid;
- liquid;
- gas;
- glass;
- metastable state;
- multiphase state.

A solid-state measurement must not be relabeled as liquid-state evidence.

---

## 46. Method Domain

A source method must remain identifiable.

Examples include:

- experiment;
- diffraction;
- NMR;
- calorimetry;
- first-principles calculation;
- classical molecular dynamics;
- fitted correlation;
- evaluated data compilation.

Method identity affects interpretation.

---

## 47. Experimental Evidence

Experimental evidence must retain:

- measured observable;
- measurement conditions;
- experimental method;
- uncertainty where available;
- source.

Experimental values must not be replaced by model predictions during validation.

---

## 48. First-Principles Evidence

First-principles evidence must retain sufficient computational-method metadata for scientific interpretation.

Depending on the study, this may include:

- electronic-structure method;
- exchange-correlation functional;
- pseudopotential or all-electron treatment;
- basis or plane-wave cutoff;
- k-point treatment;
- convergence controls;
- simulation cell;
- composition;
- thermodynamic state.

---

## 49. First-Principles Is Not Experimental

The following identification is invalid:

`first-principles result = experimental measurement`

They are independent evidence classes.

Agreement between them is a comparison result.

---

## 50. Computational Evidence

Computational evidence that is not classified as first-principles must retain its actual method classification.

For example:

- classical potential;
- polarizable-ion model;
- machine-learned potential;
- empirical correlation.

Method classes must not be upgraded by terminology.

---

## 51. Source Extraction

When a numerical value is extracted from a source, the extraction method should be identifiable.

Possible extraction classes include:

- directly tabulated;
- explicitly stated equation;
- explicitly stated fitted coefficient;
- digitized figure;
- calculated from reported values;
- converted units.

---

## 52. Directly Tabulated Value

A directly tabulated source value may retain primary-source provenance when the table directly reports the measurement or calculation relevant to the claim.

---

## 53. Source Equation

If a source explicitly provides a functional relation, repository values calculated from that relation are:

`DERIVED`

unless the repository stores the equation itself as the reported source relation.

The calculated sample values remain derived.

---

## 54. Digitized Figure

A value digitized from a figure requires explicit notation of:

- figure identity;
- axis calibration;
- digitization procedure;
- estimated extraction uncertainty where applicable.

Digitized data are not identical to original raw measurement data.

---

## 55. Unit Conversion

A converted value must preserve:

- source value;
- source unit;
- target unit;
- conversion relation.

The converted value is normally:

`DERIVED`

---

## 56. Dimensional Consistency

A source transformation must remain dimensionally valid.

Quantities with incompatible physical dimensions cannot be directly compared.

---

## 57. Interpolation

Interpolation may be admitted when:

- source data bound the interpolation interval;
- the interpolation method is explicit;
- the source/domain permits the represented interpolation;
- no phase or regime boundary invalidates the interpolation.

Interpolated values are derived.

---

## 58. Interpolation Is Not Measurement

Therefore:

`interpolated value ≠ directly measured value`

The source measurement remains upstream evidence.

---

## 59. Extrapolation

Extrapolation outside the source-supported domain must be explicitly identified.

An extrapolated value must not be presented as direct source-supported property reproduction.

---

## 60. Extrapolation Provenance

An extrapolated value is:

`DERIVED`

or another explicitly justified non-primary provenance class.

It must retain the source-domain boundary it exceeds.

---

## 61. Calibration

When source data are used to calibrate a model parameter, the parameter receives:

`CALIBRATED`

provenance.

The original source data retain their original provenance.

---

## 62. Fit Coefficients

A coefficient reported by the original source as its own fitted result may be recorded as source-reported evidence.

A coefficient re-fitted inside TR-EIF is calibrated or derived according to the procedure used.

---

## 63. Source Uncertainty

When a source reports uncertainty, the repository should preserve it where relevant to the scientific claim.

Absence of reported uncertainty must not be replaced by invented uncertainty.

---

## 64. Repository-Derived Uncertainty

An uncertainty calculated by TR-EIF from source data must retain:

- derivation;
- assumptions;
- correlation treatment;
- provenance.

It is not a directly reported source uncertainty.

---

## 65. Conflicting Sources

When two admissible sources disagree, the repository must not silently choose the numerically convenient value.

The conflict must be resolved through an explicit criterion such as:

- domain compatibility;
- measurement method;
- source quality;
- chronology;
- uncertainty;
- independent replication;
- authoritative evaluated assessment.

---

## 66. Source Conflict Is Not Averaging Requirement

Conflicting source values must not automatically be averaged.

Averaging requires a declared statistical or scientific justification.

---

## 67. Source Supersession

A later source may supersede an earlier relation when it provides:

- corrected data;
- improved measurement;
- revised calibration;
- wider validated domain;
- authoritative re-evaluation.

Supersession must be explicit.

The earlier source remains part of provenance history.

---

## 68. Historical Source

A historically foundational source may remain scientifically important even when newer data replace its quantitative values.

Historical role and current quantitative authority are separate.

---

## 69. Foundational Theory Sources

Foundational mathematical or physical sources support established theory used by TR-EIF.

Examples of source domains include:

- coupled oscillator dynamics;
- phase-lagged oscillator dynamics;
- group actions;
- equivariant representations;
- conservative mechanics;
- molecular-dynamics integration.

Detailed citations belong to the corresponding specialized source registers.

---

## 70. Source Role Labels

A source record may declare roles such as:

- foundational theory;
- method introduction;
- primary experiment;
- first-principles calculation;
- computational benchmark;
- reference compilation;
- evaluated correlation;
- validation target;
- background review.

Role labels must correspond to actual source content.

---

## 71. One Source, Multiple Roles

One publication may have several valid roles.

Each role must identify the specific claim or dataset it supports.

The presence of one valid role does not grant unrestricted use.

---

## 72. Source Admission Procedure

Before an external source becomes a validation anchor:

1. identify the intended claim or observable;
2. verify bibliographic identity;
3. verify evidence class;
4. verify applicable domain;
5. verify method;
6. verify unit;
7. verify composition or system;
8. verify source location of the relevant evidence;
9. assign repository source identifier;
10. assign provenance role;
11. record limitations.

---

## 73. Source Rejection Conditions

A source must not be used as direct claim evidence when:

- the claim is not present;
- the domain is incompatible;
- the composition is incompatible without mapping;
- the observable differs;
- the unit is unresolved;
- the source is only secondary when primary evidence is required;
- the cited value cannot be located;
- the method is incompatible with the claimed evidence class.

---

## 74. Unresolved Source

When a required source has not been established, the correct status is:

`REQUIRES_SOURCE`

The repository must not fabricate a citation to remove the unresolved state.

---

## 75. Bibliographic Verification

Bibliographic metadata should be cross-checked against stable publisher, DOI, institutional, or archival records where possible.

Author names, title, year, and identifier must not be guessed.

---

## 76. Citation Audit

A citation audit must verify:

- citation exists;
- citation resolves to the intended source;
- source supports the claim;
- domain is compatible;
- source role is correctly classified;
- derived transformations are recorded.

---

## 77. Scientific Claim Audit

A public scientific claim must be traceable to one or more of:

- formal derivation;
- executable evidence;
- primary source;
- derived source chain;
- experimental comparison;
- first-principles comparison.

Claims without sufficient evidence remain unresolved.

---

## 78. Source Register Audit

Each specialized source register must be audited for:

- duplicate source identifiers;
- inconsistent bibliographic metadata;
- conflicting provenance classes;
- broken DOI or report identifiers;
- unsupported role descriptions;
- unresolved `REQUIRES_SOURCE` entries.

---

## 79. Duplicate Source Identity

The same external publication should use one canonical repository source identity unless multiple records intentionally represent different evidence extractions from the same source.

If multiple role-specific records exist, their common bibliographic identity must remain clear.

---

## 80. Source Identifier Stability

Once a source identifier is used by committed data or code, unnecessary renaming should be avoided.

If renaming is required, dependent references must be updated together.

---

## 81. Source Register Is Not Dataset

A Markdown source register records provenance.

It is not automatically an executable dataset.

Therefore:

`source registered ≠ executable data available`

---

## 82. Dataset Requires Explicit Values

An executable reference dataset requires actual machine-readable values or a deterministic source-derived relation.

A citation alone does not supply numerical data to code.

---

## 83. Dataset Requires Provenance

Conversely, a numerical dataset without source provenance is not sufficient physical reference evidence when the data are externally derived.

Both value and provenance are required.

---

## 84. Benchmark Reference Boundary

Benchmark reference values may be committed without external physical provenance when their purpose is executable qualification.

They must use:

`BENCHMARK`

or:

`TEST_FIXTURE`

provenance as appropriate.

---

## 85. Physical Reference Boundary

A value used to claim physical reproduction requires appropriate physical source provenance.

A benchmark number cannot silently become a physical reference number.

---

## 86. Validation Comparison Boundary

A direct validation comparison must preserve evidence independence.

The tested model must not generate both:

- prediction;
- reference

through the same execution path.

---

## 87. Experimental/First-Principles Independence

When experimental and first-principles evidence are compared, both records must retain their independent provenance.

Agreement does not merge them into one evidence class.

---

## 88. Source Independence

Two publications that reuse the same underlying dataset are not automatically independent validation sources.

Data lineage must be considered where independence matters.

---

## 89. Review Source Use

A review may be used to:

- locate primary literature;
- summarize established background;
- identify competing values;
- document consensus or uncertainty.

When a primary measurement is required, the primary source should be registered directly where available.

---

## 90. Handbook and Database Use

A handbook or scientific database may be an authoritative evaluated reference.

Its role must be identified as:

- evaluated;
- compiled;
- recommended;
- or database-derived

rather than direct experimental measurement when appropriate.

---

## 91. Standards and Technical Reports

Standards and technical reports may serve as primary or authoritative sources for:

- methods;
- engineering conventions;
- evaluated data;
- institutional measurements.

Their evidence role depends on the specific claim.

---

## 92. Preprint Boundary

A preprint may be cited when relevant.

Its publication state must not be misrepresented.

If a peer-reviewed version exists and is materially identical, the stable published version is preferred for archival citation.

---

## 93. Retraction and Correction Audit

A source known to be retracted or materially corrected must not be used without recording that status.

Corrections affecting used values must propagate into the source register.

---

## 94. Versioned Online Sources

For versioned online scientific artifacts, the specific version used should be identifiable.

Mutable landing pages do not define immutable scientific content.

---

## 95. Software Sources

External software may require citation when scientific results depend materially on its implementation.

Software citation is distinct from physical-data provenance.

---

## 96. Method Sources

A method source supports the method.

It does not automatically support every result generated using that method.

For example:

`velocity-Verlet source ≠ FLiBe physical validation`

---

## 97. Mathematical Source Boundary

A mathematical source may establish:

- theorem;
- formalism;
- representation;
- method.

It does not become empirical material evidence.

---

## 98. TR-EIF Author-Defined Content

TR-EIF-specific architecture, including its exact synthesis of:

- ternary execution;
- active neutral;
- resonance layer;
- E(3)-equivariant interatomic realization;
- validation architecture

is recorded as author-defined framework content unless a specific component is explicitly sourced to established prior literature.

---

## 99. Active Neutral Source Boundary

The current TR-EIF active-neutral execution semantics are part of the framework contract.

External sources for ternary logic or oscillator dynamics must not be presented as defining the exact TR-EIF active-neutral routing semantics unless they actually do.

---

## 100. FRP Correspondence

FRP may serve as a read-only executable reference for confirmed semantic correspondences such as:

- canonical `-1/0/1`;
- active neutral `0`;
- opposite-polarity mediation through `0`;
- target/executed-state separation.

FRP is not an external scientific source replacing the literature registers.

---

## 101. FRP Architecture Boundary

The following are not imported into TR-EIF source provenance as TR-EIF architecture:

- FRP RTL;
- scheduler modes;
- FRP-specific coefficients;
- module naming;
- repository structure.

Therefore:

`FRP semantic correspondence ≠ architecture identity`

---

## 102. Source-to-Claim Traceability

A source-backed claim should support the trace:

`public claim`

`→ repository source identifier`

`→ bibliographic source`

`→ exact evidence location`

`→ domain`

`→ transformation if derived`

This trace enables citation audit.

---

## 103. Source-to-Executable Traceability

When a source-backed value enters executable code, traceability should support:

`source`

`→ extracted datum or relation`

`→ repository parameter/data artifact`

`→ executable consumer`

`→ validation artifact`

---

## 104. Exact Evidence Location

Where practical, the source register should record a precise evidence location such as:

- page;
- table;
- equation;
- figure;
- section.

This reduces ambiguity in later audits.

---

## 105. Evidence Location Is Not Quotation Requirement

A source location may be recorded without reproducing copyrighted text.

Repository documentation should paraphrase scientific content unless a short quotation is necessary and legally appropriate.

---

## 106. Quotation Boundary

Quoted text must remain limited to the minimum required wording.

Scientific data and equations should normally be cited and represented through independent notation or paraphrase.

---

## 107. Source Equation Boundary

An equation may be reproduced when appropriate under scientific citation practice.

Its variables, units, and source domain must remain explicit.

---

## 108. Source Transformation Audit

Every derived executable relation must be auditable from:

`source relation`

through:

`repository transformation`

to:

`executable form`

No hidden coefficient conversion is permitted.

---

## 109. Coefficient Precision

When a source reports limited numerical precision, the repository must not invent unsupported extra significant digits.

Derived arithmetic may produce more digits computationally.

Those digits do not increase source precision.

---

## 110. Significant Figures

Scientific reporting should preserve meaningful precision appropriate to:

- source precision;
- derivation;
- validation purpose.

Benchmark exactness and physical significant figures are different concerns.

---

## 111. Rounded Composition

A rounded percentage must remain identified as rounded.

It must not be promoted to exact rational composition.

---

## 112. Source Range

A fitted relation must retain its source-reported range where one is given.

A relation evaluated outside that range is extrapolation unless another source extends the domain.

---

## 113. Phase-Boundary Source Domain

A thermophysical correlation must not be applied across a physical phase boundary without evidence that the relation remains applicable.

---

## 114. Method-Change Boundary

Measurements obtained by materially different methods may require separate comparison or uncertainty treatment.

Numerical agreement alone does not make the methods identical.

---

## 115. Source Conflict Record

When unresolved source disagreement matters to the model, the register should preserve the competing values rather than deleting the conflict.

The model-selection decision must remain traceable.

---

## 116. Preferred Source Rule

A preferred source may be selected under an explicit rule such as:

- closer domain match;
- direct primary measurement;
- lower uncertainty;
- corrected later measurement;
- evaluated authoritative compilation.

Preference must not be based solely on better agreement with TR-EIF output.

---

## 117. No Agreement-Based Source Selection

Selecting the source that makes the model look best is invalid validation practice.

Therefore:

`best agreement ≠ source authority`

Source selection precedes model comparison.

---

## 118. Blind Validation Principle

Where practical, validation reference selection and acceptance criteria should be fixed before observing the final model-comparison result.

This reduces post-hoc selection bias.

---

## 119. Source Registration Before Parameter Use

A physical coefficient should not enter committed production model behavior before its source/provenance contract is established, unless explicitly marked:

`REQUIRES_SOURCE`

and prevented from being represented as validated physical evidence.

---

## 120. Temporary Research Values

A temporary exploratory value may exist outside release claims.

If committed into the repository, it must use an explicit non-source provenance class and must not masquerade as validated physical data.

---

## 121. Release Source Audit

Before release, the source audit must check:

- every physical coefficient;
- every material-specific numerical claim;
- every external mathematical attribution;
- every method attribution;
- every experimental claim;
- every first-principles claim;
- every public comparison.

---

## 122. Release Citation Audit

Release citation audit must verify:

- correct source;
- correct authors;
- correct title;
- correct year;
- correct identifier;
- claim correspondence;
- applicable domain;
- provenance classification.

---

## 123. Unresolved Source Release Rule

An unresolved:

`REQUIRES_SOURCE`

item must not be represented in release documentation as source-validated.

The unresolved status may remain documented explicitly.

---

## 124. Source Register Completion

A source register is complete for a declared scope only when every source-dependent claim in that scope is either:

- source-qualified;
- explicitly derived;
- explicitly unresolved.

Silence is not a provenance class.

---

## 125. Specialized Register Forward References

The repository architecture permits semantic references to specialized source registers before those registers are created.

Such a reference means the register belongs to the approved architecture.

It must not state that the absent file already exists.

---

## 126. Kuramoto-Sakaguchi Register

The approved specialized file is:

`docs/references/kuramoto_sakaguchi_sources.md`

Its intended scope includes primary and foundational sources for:

- Kuramoto-type oscillator dynamics;
- Sakaguchi phase lag;
- synchronization;
- order parameters;
- relevant phase-dynamical stability results.

---

## 127. Equivariant-Model Register

The approved specialized file is:

`docs/references/equivariant_model_sources.md`

Its intended scope includes sources for:

- group-equivariant modeling;
- E(3)/SE(3) representations;
- invariant and equivariant neural operations;
- equivariant interatomic architectures.

---

## 128. Interatomic-Potential Register

The approved specialized file is:

`docs/references/interatomic_potential_sources.md`

Its intended scope includes sources for:

- interatomic potential theory;
- energy-based machine-learning models;
- conservative-force construction;
- stress relations;
- atomistic energy decomposition.

---

## 129. Molecular-Dynamics Register

The approved specialized file is:

`docs/references/molecular_dynamics_sources.md`

Its intended scope includes sources for:

- equations of motion;
- time integration;
- periodic boundaries;
- neighbor methods;
- thermostats;
- barostats;
- transport observables;
- MD numerical validation.

---

## 130. FLiBe Register

The material-specific source register is:

`docs/references/flibe_sources.md`

It records evidence for:

- phase relations;
- composition;
- thermodynamic properties;
- structural data;
- transport properties;
- material-specific validation anchors.

---

## 131. Source Register Separation

A source may appear in more than one specialized register only when its evidence role genuinely crosses those domains.

Unnecessary duplication should be avoided.

---

## 132. Source Identifier Reuse

When the same publication supports multiple repository artifacts, the same canonical source identifier should be reused where practical.

Role-specific sub-identifiers may be introduced only when needed for unambiguous evidence extraction.

---

## 133. Provenance in Executable Artifacts

Executable physical records should carry provenance sufficient to reconnect them to the corresponding source register.

A numerical value detached from provenance must not be treated as source-qualified physical evidence.

---

## 134. Provenance in Benchmarks

A benchmark may use source-backed physical data.

In that case, distinguish:

- benchmark execution provenance;
- upstream physical-data provenance.

A benchmark output may be `BENCHMARK` while its reference values trace to `PRIMARY_SOURCE` or `DERIVED` evidence.

---

## 135. Validation Status vs Provenance

Provenance answers:

`Where did this evidence come from?`

Validation status answers:

`Did this declared validation relation pass?`

These are different dimensions.

Therefore:

`provenance ≠ validation status`

---

## 136. Source Quality vs Model Agreement

Source quality must be evaluated independently of model agreement.

A high-quality source remains valid evidence even when the model disagrees with it.

Model disagreement is a validation result.

---

## 137. Negative Evidence

A source that contradicts a model claim is not removed because it produces an unfavorable comparison.

Contradictory evidence is part of scientific validation.

---

## 138. Absence of Evidence

Absence of a source is not evidence for the opposite claim.

Therefore:

`no source found ≠ claim false`

The correct repository state is unresolved evidence.

---

## 139. Evidence Scope

Every source-backed statement must remain within the scope of the evidence.

A narrow measurement must not be generalized into a universal material law without additional justification.

---

## 140. Core Source-Provenance Invariants

The source architecture preserves:

1. Provenance class is explicit.
2. Provenance is not ternary state.
3. Primary-source status is claim-specific.
4. Derived values remain derived.
5. Calibration is not independent validation.
6. Author-defined structures are not empirical evidence.
7. Benchmark evidence is not physical source evidence.
8. Test fixtures are not physical evidence.
9. Missing provenance remains `REQUIRES_SOURCE`.
10. Missing qualification remains `REQUIRES_TEST`.
11. Citation presence does not establish claim correspondence.
12. Observable identity is preserved.
13. Composition identity is preserved.
14. Thermodynamic domain is preserved.
15. Physical-state domain is preserved.
16. Method identity is preserved.
17. Experimental evidence remains distinct from first-principles evidence.
18. Computational evidence retains its actual method class.
19. Interpolation is derived evidence.
20. Extrapolation is explicitly identified.
21. Unit conversion is explicit.
22. Digitized values retain extraction provenance.
23. Conflicting sources are not silently averaged.
24. Source preference is not selected by model agreement.
25. Source registers are not executable datasets.
26. Executable datasets require numerical content.
27. Physical datasets require provenance.
28. Similarity is not identity.
29. A source must support the exact claim for which it is cited.
30. Release claims cannot silently promote unresolved source status.

---

## 141. Related Validation Documents

This source contract operates with:

`docs/validation/scientific_validation_plan.md`

`docs/validation/mathematical_validation_plan.md`

`docs/validation/numerical_validation_plan.md`

`docs/validation/invariant_validation_plan.md`

`docs/validation/reproducibility_plan.md`

`docs/validation/flibe_validation_matrix.md`

Source provenance is one dimension of the complete validation architecture.

---

## 142. Non-Claims

This document does not assert that:

- every approved specialized source register already exists;
- every physical parameter is source-qualified;
- every registered source is primary;
- every source-backed value has an executable model;
- every executable model has physical validation;
- bibliography completeness establishes scientific correctness.

Those states require their own evidence.

---

## 143. Summary

TR-EIF source handling is provenance-preserving and claim-specific.

The evidence chain is:

`scientific claim`

`→ exact evidence requirement`

`→ source identification`

`→ source-domain verification`

`→ repository source record`

`→ extraction or derivation`

`→ executable or documentary use`

`→ validation`

The repository preserves:

`citation ≠ evidence sufficiency`

`derived ≠ primary`

`calibrated ≠ independently validated`

`benchmark ≠ physical source`

`test fixture ≠ measurement`

`first-principles ≠ experimental`

`source registered ≠ executable dataset`

and:

`similar ≠ identical`

A source is admitted only for the claim, observable, method, and domain that it actually supports.
