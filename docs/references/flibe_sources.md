# FLiBe Source Register

## 1. Scope

This document defines the source and provenance register for the TR-EIF FLiBe material specialization.

It establishes which external records may support material-specific thermodynamic, phase-equilibrium, structural, and transport claims.

This document does not import numerical physical parameters into the executable implementation.

A bibliographic entry does not automatically authorize every numerical value appearing in that source.

Each numerical parameter introduced later must retain:

- property identity;
- composition;
- thermodynamic state or applicable range;
- unit;
- source identifier;
- provenance class;
- extraction location;
- transformation history when derived;
- applicable uncertainty when supplied by the source.

The canonical TR-EIF provenance classes remain:

- `PRIMARY_SOURCE`
- `DERIVED`
- `CALIBRATED`
- `AUTHOR_DEFINED`
- `BENCHMARK`
- `TEST_FIXTURE`
- `REQUIRES_SOURCE`
- `REQUIRES_TEST`

Provenance metadata does not alter the physical or mathematical value itself.

---

## 2. Source Classification Rule

A source is classified at the level of the specific claim or parameter being used.

A publication that contains both measurements and estimates must not receive blanket `PRIMARY_SOURCE` status for all quantities in the publication.

For one imported quantity:

`PRIMARY_SOURCE`

means that the cited source reports the underlying experimental or first-principles result used for that quantity.

`DERIVED`

means that the quantity is calculated from one or more sourced quantities by an explicitly documented transformation.

`REQUIRES_SOURCE`

means that the quantity must not enter source-backed scientific use until an adequate external source has been identified and recorded.

Secondary reviews, handbooks, assessments, and databases may be used to locate or cross-check primary literature, but they do not automatically replace the primary source.

---

## 3. Composition and Phase-Equilibrium Sources

### FLIBE-PRIMARY-ROY-1950-PHASE

D. M. Roy, R. Roy, and E. F. Osborn.

"Phase Relations and Structural Phenomena in the Fluoride Model Systems LiF-BeF2 and NaF-BeF2."

Journal of the American Ceramic Society, 33, 85-90, 1950.

DOI:

`10.1111/j.1151-2916.1950.tb12766.x`

Source role:

- experimental LiF-BeF2 phase relations;
- structural phase information;
- historical primary phase-diagram evidence.

Allowed provenance:

`PRIMARY_SOURCE`

for quantities directly extracted from the reported experiments.

---

### FLIBE-PRIMARY-ROY-1954-PHASE

D. M. Roy, R. Roy, and E. F. Osborn.

"Fluoride Model Systems: IV, The Systems LiF-BeF2 and PbF2-BeF2."

Journal of the American Ceramic Society, 37, 300-305, 1954.

DOI:

`10.1111/j.1151-2916.1954.tb14042.x`

Source role:

- experimental LiF-BeF2 phase relations;
- refinement of the binary-system description.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported experimental phase-equilibrium observations.

---

### FLIBE-PRIMARY-ROMBERGER-1972-LIQUIDUS

K. A. Romberger, J. Braunstein, and R. E. Thoma.

"New Electrochemical Measurements of the Liquidus in the LiF-BeF2 System."

Journal of Physical Chemistry, 76, 1154-1159, 1972.

DOI:

`10.1021/j100652a012`

Source role:

- high-resolution liquidus measurements;
- invariant-point and composition qualification;
- phase-diagram terminology.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported liquidus measurements.

This source must be consulted before assigning the term `eutectic` to a specific LiF-BeF2 composition.

---

## 4. Exact 2 LiF : 1 BeF2 Composition Boundary

The exact formula-unit ratio

`2 LiF : 1 BeF2`

corresponds to:

- LiF formula-unit fraction: `2/3`;
- BeF2 formula-unit fraction: `1/3`;
- compound stoichiometry: `Li2BeF4`.

This exact stoichiometric definition is mathematically distinct from an experimentally determined invariant composition in a phase diagram.

Therefore:

`exact 2:1 composition ≠ automatically an experimentally established eutectic composition`

The executable helper currently named:

`eutectic_flibe_composition()`

must not be treated as experimentally qualified solely because it returns the exact `2:1` formula-unit ratio.

Its naming and scientific status require a separate implementation audit against the accepted phase-equilibrium sources before Phase 10 closure.

No change to that API is made by this source-register file.

---

## 5. Density and Viscosity Sources

### FLIBE-PRIMARY-CANTOR-WARD-MOYNIHAN-1969

S. Cantor, W. T. Ward, and C. T. Moynihan.

"Viscosity and Density in Molten BeF2-LiF Solutions."

Journal of Chemical Physics, 50(7), 2874-2879, 1969.

DOI:

`10.1063/1.1671478`

Experimental scope:

- molten BeF2-LiF viscosity;
- molten BeF2-LiF density;
- composition dependence;
- temperature dependence;
- volume expansivity derived from density behavior.

Source role:

- primary density evidence;
- primary viscosity evidence;
- composition-dependent liquid-property evidence.

Allowed provenance:

`PRIMARY_SOURCE`

for measurements within the reported composition and temperature domains.

Values outside those domains must not inherit `PRIMARY_SOURCE` status through extrapolation.

---

## 6. Enthalpy and Heat-Capacity Sources

### FLIBE-PRIMARY-DOUGLAS-PAYNE-1969

Thomas B. Douglas and William H. Payne.

"Measured Enthalpy and Derived Thermodynamic Properties of Solid and Liquid Lithium Tetrafluoroberyllate, Li2BeF4, from 273 to 900 K."

Journal of Research of the National Bureau of Standards, Section A, 73A(5), 479-485, 1969.

DOI:

`10.6028/jres.073A.037`

Experimental scope:

- measured enthalpy of Li2BeF4;
- solid and liquid temperature range;
- derived heat capacity;
- derived entropy-related quantities;
- derived Gibbs-energy-function quantities.

Provenance rule:

- directly measured enthalpy data may use `PRIMARY_SOURCE`;
- quantities calculated by TR-EIF from those measurements use `DERIVED`;
- source-authored derived tables retain their source attribution but must be identified as derived quantities rather than direct measurements.

---

### FLIBE-PRIMARY-REDKIN-2021-THERMOPHYSICAL

A. Redkin, A. Khudorozhkova, E. Il'ina, S. Pershina, P. Mushnikov, A. Isakov, Yu. Zaikov, A. Kataev, and M. Laptev.

"Density and Heat Capacity of Some Molten Mixtures in System LiF-BeF2-UF4."

Journal of Molecular Liquids, 341, 117215, 2021.

DOI:

`10.1016/j.molliq.2021.117215`

Experimental scope:

- density measurements for selected LiF-BeF2-UF4 compositions;
- density measurements for UF4-free LiF-BeF2 compositions included in the study;
- heat-capacity measurements;
- thermal expansion derived from density measurements.

Source role:

- modern primary density evidence;
- modern primary heat-capacity evidence;
- comparison point for historical measurements.

Allowed provenance:

`PRIMARY_SOURCE`

only for directly reported measurements at the compositions and state ranges actually studied.

Derived thermal-expansion values must retain their derived status.

---

## 7. Mixed Experimental and Estimated ORNL Reference

### FLIBE-SOURCE-CANTOR-1968-ORNL-TM-2316

S. Cantor, editor.

"Physical Properties of Molten-Salt Reactor Fuel, Coolant, and Flush Salts."

Oak Ridge National Laboratory.

Report:

`ORNL-TM-2316`

Year:

`1968`

DOI:

`10.2172/4492893`

The report includes material on:

- viscosity;
- thermal conductivity;
- electrical conductivity;
- phase-transition behavior;
- heat capacity;
- heat of fusion;
- liquid density;
- expansivity;
- compressibility;
- vapor pressure;
- surface tension;
- derived transport quantities.

This report contains a mixture of:

- experimental values;
- unpublished measurements;
- estimates;
- correlations;
- quantities derived from other data.

Therefore the report as a whole must not be assigned blanket `PRIMARY_SOURCE` provenance.

Every value extracted from this report requires property-level inspection of its stated source and method.

Possible resulting provenance classes include:

- `PRIMARY_SOURCE`
- `DERIVED`
- `REQUIRES_SOURCE`

depending on the specific entry.

---

## 8. Secondary Assessment Sources

The following sources may be used for source discovery, comparison, and audit.

They must not silently replace primary provenance.

### FLIBE-SECONDARY-WILLIAMS-2006

D. F. Williams, L. M. Toth, and K. T. Clarno.

"Assessment of Candidate Molten Salt Coolants for the Advanced High-Temperature Reactor."

Oak Ridge National Laboratory.

Report:

`ORNL/TM-2006/12`

Year:

`2006`

Role:

- review and assessment;
- comparison of candidate molten-salt coolant properties;
- locator for historical experimental literature.

Default provenance for numerical values copied directly from this assessment:

`REQUIRES_SOURCE`

until the underlying primary source is identified, unless the value is explicitly an original result of the report.

---

## 9. Parameter Admission Rule

Before a physical FLiBe parameter enters executable TR-EIF code, a parameter record must establish:

1. parameter name;
2. numerical value or functional form;
3. unit;
4. LiF-BeF2 composition;
5. additional species when applicable;
6. temperature domain;
7. pressure domain when relevant;
8. phase or state domain;
9. source identifier from this register or a subsequently audited source;
10. provenance class;
11. source location such as table, equation, figure, or page;
12. uncertainty when reported;
13. any conversion performed by TR-EIF;
14. any interpolation or extrapolation;
15. whether the quantity is measured, source-derived, or TR-EIF-derived.

A parameter lacking the required provenance remains:

`REQUIRES_SOURCE`

and must not be presented as a validated physical property.

---

## 10. Transport Reference Data

Transport-property evidence is separated by observable, composition, temperature domain, measurement method, and evidence class.

A transport coefficient measured for one transported species is not automatically a transport coefficient of the molten salt as a whole.

In particular:

`tritium diffusivity ≠ salt-ion self-diffusivity`

`deuterium diffusivity ≠ lithium diffusivity`

`electrical conductivity ≠ thermal conductivity`

`viscosity ≠ diffusivity`

`thermal diffusivity ≠ thermal conductivity`

A transport coefficient is not a resonance descriptor and is not a ternary state.

---

### FLIBE-PRIMARY-CANTOR-WARD-MOYNIHAN-1969-VISCOSITY

S. Cantor, W. T. Ward, and C. T. Moynihan.

"Viscosity and Density in Molten BeF2-LiF Solutions."

Journal of Chemical Physics, 50(7), 2874-2879, 1969.

DOI:

`10.1063/1.1671478`

Transport role:

- experimental molten LiF-BeF2 viscosity;
- composition dependence;
- temperature dependence.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported viscosity measurements within the experimental composition and temperature domains.

Any interpolation, extrapolation, or TR-EIF correlation constructed from these measurements must use `DERIVED` provenance.

---

### FLIBE-PRIMARY-COOKE-1971-THERMAL-CONDUCTIVITY

J. W. Cooke.

Thermal-conductivity measurements reported in:

M. W. Rosenthal, R. B. Briggs, and P. N. Haubenreich.

"Molten-Salt Reactor Program: Semiannual Progress Report for Period Ending August 31, 1971."

Oak Ridge National Laboratory.

Report:

`ORNL-4728`

Publication:

`February 1972`

Relevant section:

`5.2 Thermophysical Properties`

Experimental scope reported for the LiF-BeF2 mixture:

- composition: approximately `66 mol% LiF : 34 mol% BeF2`;
- thermal conductivity;
- solid and liquid temperature regions;
- variable-gap measurement technique;
- measurement range extending through the molten state.

The report states that measurements were made over approximately `300–870 °C` and gives an estimated maximum uncertainty below approximately `±10%` for the reported measurement series.

Source role:

- primary FLiBe thermal-conductivity measurement;
- temperature-dependent thermal-conductivity reference;
- validation source for later thermal-conductivity models.

Allowed provenance:

`PRIMARY_SOURCE`

for values directly extracted from the reported experimental series.

Digitized graph values, fitted correlations, or interpolated values use:

`DERIVED`

unless an exact tabulated source value is available.

---

### FLIBE-METHOD-COOKE-1973-VARIABLE-GAP

J. W. Cooke.

"Development of the Variable-Gap Technique for Measuring the Thermal Conductivity of Fluoride Salt Mixtures."

Oak Ridge National Laboratory.

Report:

`ORNL-4831`

Publication:

`February 1973`

Source role:

- experimental-method qualification;
- variable-gap apparatus definition;
- high-temperature fluoride-salt thermal-conductivity methodology;
- measurement-error and correction analysis.

This report qualifies the measurement method.

It must not be used by itself as provenance for a FLiBe numerical thermal-conductivity value unless that exact value is explicitly reported in the document.

---

### FLIBE-PRIMARY-ROBBINS-BRAUNSTEIN-1970-ELECTRICAL-CONDUCTIVITY

G. D. Robbins and J. Braunstein.

Electrical-conductivity measurements reported in:

M. W. Rosenthal.

"Molten-Salt Reactor Program: Semiannual Progress Report for Period Ending February 28, 1970."

Oak Ridge National Laboratory.

Report:

`ORNL-4548`

Publication:

`August 1970`

Relevant section:

`Electrical Conductivities and Ionic Mobilities in the Molten LiF-BeF2 System`

Experimental scope:

- molten LiF-BeF2 mixtures;
- electrical conductivity;
- composition dependence;
- temperature dependence;
- ionic-mobility analysis using conductivity, transference, and density information.

Source role:

- primary electrical-conductivity evidence;
- composition-dependent conductivity reference;
- ionic-transport evidence.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported electrical-conductivity measurements.

Derived ionic mobilities must retain their derived status and the complete dependency chain used by the source.

Electrical conductivity must not be interpreted as a direct salt-ion self-diffusion measurement.

---

### FLIBE-PRIMARY-ANDERL-2004-DEUTERIUM-TRANSPORT

R. A. Anderl, S. Fukada, G. R. Smolik, R. J. Pawelko, S. T. Schuetz, J. P. Sharpe, B. J. Merrill, D. A. Petti, H. Nishimura, T. Terai, and S. Tanaka.

"Deuterium/tritium behavior in Flibe and Flibe-facing materials."

Journal of Nuclear Materials, 329-333, 1327-1331, 2004.

DOI:

`10.1016/j.jnucmat.2004.04.220`

Experimental scope:

- molten `2 LiF : 1 BeF2`;
- deuterium transport;
- diffusion;
- solubility;
- permeation-probe measurements;
- temperature-dependent transport behavior.

Source role:

- primary experimental deuterium-transport reference;
- diffusion and solubility validation for hydrogen-isotope transport.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported experimental observations.

Diffusion coefficients obtained by fitting the measured transient transport process must retain the source-described derivation method.

These values describe deuterium transport and must not be relabeled as intrinsic Li, Be, or F self-diffusion coefficients.

---

### FLIBE-PRIMARY-CALDERONI-2008-TRITIUM-PERMEATION

P. Calderoni, P. Sharpe, M. Hara, and Y. Oya.

"Measurement of tritium permeation in flibe (2LiF-BeF2)."

Fusion Engineering and Design, 83(7-9), 1331-1334, 2008.

DOI:

`10.1016/j.fusengdes.2008.05.016`

Experimental scope:

- molten `2 LiF : 1 BeF2`;
- temperature range approximately `500–700 °C`;
- tritium permeation;
- tritium diffusivity;
- tritium solubility;
- steady-state and transient transport measurements.

Source role:

- primary experimental tritium-transport reference;
- independent hydrogen-isotope transport validation path.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported experimental measurements and source-derived transport quantities when their derivation method is retained.

Tritium permeability, diffusivity, and solubility are separate observables.

None is automatically equivalent to bulk molten-salt ionic diffusivity.

---

## 10.1 Transport Data Admission Rule

Before a transport quantity enters executable FLiBe validation, its record must establish:

1. transport observable;
2. transported species when applicable;
3. LiF-BeF2 composition;
4. additional species when applicable;
5. temperature or temperature range;
6. pressure when relevant;
7. liquid or solid state;
8. measurement or computational method;
9. numerical value or functional form;
10. unit;
11. source identifier;
12. provenance class;
13. exact source location;
14. uncertainty when reported;
15. fitted or directly measured status;
16. interpolation or extrapolation status;
17. any unit conversion;
18. applicable state-domain limits.

A correlation constructed from primary measurements is:

`DERIVED`

unless the correlation itself is explicitly reported by the primary source.

---

## 10.2 Current Transport Evidence Boundary

The source register now contains provenance anchors for:

- viscosity;
- thermal conductivity;
- electrical conductivity;
- deuterium diffusivity and solubility;
- tritium diffusivity, permeability, and solubility.

Experimental salt-ion self-diffusion coefficients for Li, Be, and F are not established here.

Computational self-diffusion data may be introduced later through an explicitly identified computational evidence path and must not be relabeled as experimental measurements.

Executable numerical transport datasets are not introduced by this source-register section.

---

## 11. Structural Reference Data

Structural reference data are separated by physical state, measurement method, composition, and evidence class.

A graph-relative coordination count in TR-EIF is not automatically a chemical bond count or an experimentally measured coordination number.

A structural observable is not automatically a resonance descriptor.

A structural classification is not automatically a ternary state.

---

### FLIBE-PRIMARY-FAYFAR-2024-TOTAL-SCATTERING

S. Fayfar, R. Chahal, H. Williams, D. N. Gardner, G. Zheng, D. Sprouster, J. C. Neuefeind, D. Olds, A. Hwang, J. McFarlane, R. C. Gallagher, M. Asta, S. Lam, R. O. Scarlat, and B. Khaykovich.

"Complex Structure of Molten FLiBe (2LiF-BeF2) Examined by Experimental Neutron Scattering, X-Ray Scattering, and Deep-Neural-Network Based Molecular Dynamics."

PRX Energy, 3, 013001, 2024.

DOI:

`10.1103/PRXEnergy.3.013001`

Experimental scope:

- liquid `2 LiF : 1 BeF2`;
- neutron total scattering;
- X-ray total scattering;
- atomic liquid structure;
- short-range ordering;
- intermediate-range ordering.

Computational scope reported in the same work:

- ab initio molecular dynamics;
- neural-network molecular dynamics;
- comparison of simulated and experimentally measured structure.

Source role:

- primary experimental total-scattering reference for liquid FLiBe;
- experimental reference for validation of structural simulation output;
- source for structure-factor and pair-correlation qualification where the exact observable, composition, state, and extraction location are recorded.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported experimental scattering observations.

Simulation-derived structural quantities from the same publication must remain explicitly identified as computational results and must not be relabeled as experimental measurements.

The paper reports Be-F tetrahedral units and intermediate-range structural ordering.

Those structural entities must not be identified with TR-EIF graph edges, ternary states, or resonance classes without an explicit validated mapping.

---

### FLIBE-PRIMARY-FU-2023-NMR

X. Fu, Y. Liu, H. Huang, H. Wu, J. Sun, L. Han, M. Ge, Y. Qian, and H. Liu.

"Probing the Local Structure of FLiBe Melts and Solidified Salts by In Situ High-Temperature NMR."

Physical Chemistry Chemical Physics, 25, 19446-19452, 2023.

DOI:

`10.1039/D3CP01096A`

Experimental scope:

- high-temperature in situ NMR of LiF-BeF2 melts;
- local ionic coordination;
- composition-dependent structural evolution;
- solid-state NMR of solidified salts.

Reported structural classes include:

- tetrahedral BeF4 units;
- Be2F7 units;
- Be3F10 units;
- polymeric intermediate-range Be-F structures.

Source role:

- primary experimental local-structure reference;
- spectroscopic evidence for Be-F coordination environments;
- source for composition-dependent structural classification.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported NMR observations and source-supported structural assignments.

NMR-derived structural assignments must retain the composition and measurement conditions reported by the source.

A spectroscopic structural assignment is not automatically equivalent to a graph-relative coordination count generated from an arbitrary geometric cutoff.

---

### FLIBE-PRIMARY-GARDNER-2025-SOLID-DIFFRACTION

D. N. Gardner, H. Williams, S. C. Vogel, S. Fayfar, B. Khaykovich, S. Srivastava, A. Hwang, M. Asta, D. Sprouster, D. Olds, G. Vershbow, J. C. Neuefeind, and R. O. Scarlat.

"Solid Structure of Li2BeF4 (FLiBe) from Room Temperature to Melting Studied by Neutron and X-Ray Diffraction."

Journal of Applied Crystallography, 58, 435-446, 2025.

DOI:

`10.1107/S1600576725000548`

Experimental scope:

- solid Li2BeF4;
- neutron diffraction;
- X-ray diffraction;
- lattice parameters;
- unit-cell volume;
- temperature-dependent crystal structure;
- solid-state thermal expansion up to melting.

Source role:

- primary solid-state structural reference;
- structural boundary for distinguishing crystalline Li2BeF4 from liquid FLiBe;
- temperature-dependent solid-structure validation.

Allowed provenance:

`PRIMARY_SOURCE`

for directly reported diffraction measurements.

Solid-state lattice parameters and crystal-structure observables must not be transferred to liquid FLiBe without an explicit physical transformation model and validation.

---

### FLIBE-COMPUTATIONAL-SALANNE-2006-NETWORK

M. Salanne, C. Simon, P. Turq, R. J. Heaton, and P. A. Madden.

"A First-Principles Description of Liquid BeF2 and Its Mixtures with LiF: 2. Network Formation in LiF-BeF2."

Journal of Physical Chemistry B, 110(23), 11461-11467, 2006.

DOI:

`10.1021/jp061002u`

Computational scope:

- liquid BeF2-LiF mixtures;
- first-principles-derived polarizable interaction model;
- composition-dependent Be-F network formation;
- structural and transport relationships.

Source role:

- computational structural reference;
- comparison source for BeF4-network formation across composition;
- historical computational evidence path for local and intermediate-range structure.

This source is not an experimental structural measurement.

Numerical quantities imported from this source must retain explicit computational-method provenance.

---

## 12. Structural Data Admission Rule

Before structural reference data enter executable TR-EIF validation, each record must establish:

1. observable identity;
2. composition;
3. temperature;
4. pressure when relevant;
5. solid or liquid state;
6. experimental or computational method;
7. source identifier;
8. provenance class;
9. source location;
10. independent variable and unit;
11. observable value and unit where applicable;
12. uncertainty where reported;
13. preprocessing or normalization;
14. interpolation or digitization procedure when used;
15. mapping to the executable TR-EIF observable being validated.

Structural observables remain distinct.

In particular:

`structure factor ≠ pair-distribution function`

`pair-distribution function ≠ coordination number`

`coordination number ≠ chemical bond`

`graph coordination ≠ experimental coordination unless the mapping is defined and validated`

`local structural unit ≠ ternary state`

`structural transition ≠ ternary transition`

`structural transition ≠ physical phase transition`

`structural descriptor ≠ resonance classification`

No coordination cutoff may be introduced as a physical FLiBe parameter without provenance or an explicit model-defined status.

No experimental structural observable is encoded through ternary state `0`.

---

## 13. First-Principles Boundary

A first-principles calculation is not classified as an experimental `PRIMARY_SOURCE` measurement.

When first-principles data are introduced, their provenance must identify:

- electronic-structure method;
- exchange-correlation treatment;
- dispersion treatment when applicable;
- pseudopotential or all-electron treatment;
- basis or plane-wave settings;
- convergence controls;
- simulation-cell composition;
- thermodynamic state;
- trajectory or sampling protocol when molecular dynamics is used.

First-principles reference data and experimental reference data remain distinct evidence paths.

---

## 14. Current Phase 10 Source Status

The source register currently establishes provenance anchors for:

- LiF-BeF2 phase equilibria;
- liquidus qualification;
- density;
- viscosity;
- Li2BeF4 enthalpy and derived thermodynamic properties;
- selected modern density and heat-capacity measurements;
- experimental liquid total-scattering structure;
- experimental NMR local structure;
- solid Li2BeF4 diffraction structure;
- computational Be-F network formation.

Structural-source provenance is established, but executable numerical structural datasets are not introduced by this document.

The following Phase 10 evidence groups remain separate work items:

- complete transport reference data;
- training and validation configurations;
- FLiBe-specific resonance descriptors backed by explicit model provenance;
- FLiBe TR-EIP realization;
- molecular-dynamics validation;
- multiscale coolant validation;
- experimental and first-principles comparison.

No missing evidence group is encoded through ternary state `0`.

No validation status is encoded as a ternary state.
