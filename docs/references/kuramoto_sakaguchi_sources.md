# Kuramoto-Sakaguchi Sources

## 1. Scope

This document defines the source register for the phase-oscillator and Kuramoto-Sakaguchi mathematical background used by the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The register covers sources relevant to:

- populations of coupled oscillators;
- phase reduction;
- natural-frequency distributions;
- mean-field phase coupling;
- mutual entrainment;
- synchronization;
- phase locking;
- phase lag;
- order parameters;
- active-rotator extensions;
- collective-state transitions;
- low-dimensional reductions;
- mathematical interpretation of coupled phase dynamics.

This source register does not define the complete TR-EIF resonance architecture.

It does not define TR-EIF balanced ternary execution.

It does not define active-neutral state `0`.

It does not define TR-EIP.

It does not define FLiBe physical parameters.

---

## 2. Architectural Source Boundary

TR-EIF uses established phase-oscillator theory as one mathematical foundation for continuous nonlinear dynamics.

The architectural relation is:

`coupled phase-oscillator formalism`

`→ TR-EIF continuous resonance layer`

not:

`coupled phase-oscillator formalism = TR-EIF`

Therefore:

`Kuramoto formalism ≠ TR-EIF`

`Sakaguchi-Kuramoto formalism ≠ TR-EIF`

---

## 3. Resonance Boundary

The source literature in this register primarily concerns:

- oscillatory phase dynamics;
- entrainment;
- synchronization;
- phase locking;
- collective order.

TR-EIF preserves the stricter semantic distinctions:

`resonance ≠ frequency equality`

`resonance ≠ synchronization`

`synchronization ≠ phase locking`

`phase locking ≠ resonance`

`coherence ≠ uniformity`

`coherence ≠ resonance`

`phase order ≠ complete coherence`

`R(t) ≠ C(t)`

No cited synchronization result is automatically promoted to a general resonance theorem.

---

## 4. Ternary Boundary

The cited Kuramoto and Sakaguchi literature does not define the TR-EIF balanced ternary state space:

`{-1, 0, 1}`

and does not establish the TR-EIF active-neutral routing semantics.

Therefore:

`Kuramoto phase state ≠ ternary state`

`Sakaguchi phase lag ≠ ternary routing`

`synchronization state ≠ active neutral 0`

---

## 5. Active Neutral Boundary

TR-EIF state:

`0`

is active neutral.

Its architecture may include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

The exact TR-EIF semantics of active neutral are:

`AUTHOR_DEFINED`

within the TR-EIF architecture, with explicitly confirmed semantic correspondence to the separate FRP project where applicable.

They are not attributed to Kuramoto or Sakaguchi.

---

## 6. Source Classification

This register distinguishes:

### Foundational primary sources

Original publications introducing or directly developing relevant phase-oscillator constructions.

### Foundational monographs

Authoritative extended treatments by originators or major developers of the formalism.

### Related primary extensions

Original research extending the formalism in a way directly relevant to TR-EIF mathematical interpretation.

### Review and reference sources

Secondary sources used to cross-check terminology, historical context, mathematical interpretation, and the scope of established results.

A review source is not relabeled as the primary origin of a result.

---

## 7. WINFREE-1967-COUPLED-OSCILLATORS

Arthur T. Winfree.

"Biological Rhythms and the Behavior of Populations of Coupled Oscillators."

Journal of Theoretical Biology.

Volume 16, Issue 1.

Pages 15-42.

1967.

DOI:

`10.1016/0022-5193(67)90051-3`

Source class:

foundational primary source.

Repository role:

historical and mathematical precursor to later mean-field phase-oscillator models.

Relevant evidence domain:

- interacting oscillator populations;
- collective synchronization;
- weakly interacting oscillatory systems;
- population-level temporal organization.

TR-EIF use:

background for the historical development of coupled-oscillator population models.

Non-claim:

this source does not define TR-EIF resonance semantics.

Non-claim:

this source does not define balanced ternary execution.

---

## 8. Winfree-to-Kuramoto Boundary

Winfree's oscillator-population work is an important precursor.

TR-EIF must not describe the Winfree model and Kuramoto model as identical.

Therefore:

`Winfree model ≠ Kuramoto model`

Their historical and mathematical relationship does not erase their distinct formulations.

---

## 9. KURAMOTO-1975-SELF-ENTRAINMENT

Yoshiki Kuramoto.

"Self-entrainment of a Population of Coupled Non-linear Oscillators."

In:

Huzihiro Araki, editor.

International Symposium on Mathematical Problems in Theoretical Physics.

Lecture Notes in Physics.

Volume 39.

Pages 420-422.

Springer.

1975.

DOI:

`10.1007/BFb0013365`

Source class:

foundational primary source.

Repository role:

primary historical source for the canonical mean-field coupled-phase-oscillator model associated with the Kuramoto formalism.

Relevant evidence domain:

- oscillator populations;
- self-entrainment;
- natural-frequency heterogeneity;
- collective phase organization;
- mean-field coupling.

---

## 10. Kuramoto 1975 Source Role

`KURAMOTO-1975-SELF-ENTRAINMENT`

is admitted as a foundational source for the phase-oscillator layer.

It supports the historical and mathematical ancestry of the canonical Kuramoto mean-field construction.

It does not establish:

- TR-EIF active neutral;
- TR-EIF ternary routing;
- E(3)-equivariant interatomic modeling;
- conservative TR-EIP energy;
- FLiBe material physics.

---

## 11. Canonical Kuramoto-Type Form

A common modern representation of the globally coupled phase model is:

`dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i)`

where:

- `θ_i` is oscillator phase;
- `ω_i` is natural frequency;
- `K` is coupling strength;
- `N` is oscillator count.

This expression represents a canonical mathematical form.

Sign and indexing conventions may vary across sources.

Equivalent algebraic conventions must be recognized before comparing equations.

---

## 12. Equation-Convention Requirement

Two oscillator equations must not be treated as different physical models solely because one writes:

`sin(θ_j - θ_i)`

and another writes an algebraically equivalent negative-sign form.

Before declaring a discrepancy, validate:

- sign convention;
- phase-difference ordering;
- coupling normalization;
- phase-lag sign;
- summation normalization.

---

## 13. Natural Frequency Boundary

Natural frequency:

`ω_i`

is a continuous dynamical parameter.

It is not:

- ternary polarity;
- thermodynamic temperature;
- mechanical force;
- chemical species identity.

Therefore:

`ω_i ≠ ternary state`

---

## 14. Coupling Strength Boundary

Kuramoto coupling strength:

`K`

is a model parameter.

It is not automatically:

- energy;
- force constant;
- interatomic bond strength;
- resonance amplitude;
- thermodynamic property.

Any physical interpretation requires a separate mapping.

---

## 15. KURAMOTO-TSUZUKI-1974-REDUCTIVE-PERTURBATION

Yoshiki Kuramoto and Toshio Tsuzuki.

"Reductive Perturbation Approach to Chemical Instabilities."

Progress of Theoretical Physics.

Volume 52, Issue 4.

Pages 1399-1401.

1974.

DOI:

`10.1143/PTP.52.1399`

Source class:

foundational primary source.

Repository role:

background for the reductive perturbation and phase-description development associated with Kuramoto's nonlinear-dynamics program.

Relevant evidence domain:

- nonlinear instabilities;
- reductive perturbation;
- asymptotic reduction;
- development context for later phase descriptions.

---

## 16. Reductive-Perturbation Boundary

A reductive perturbation result is not automatically a phase-only model.

The reduction requires its own assumptions.

Therefore:

`nonlinear system → phase model`

is not a universal identity.

A phase reduction is valid only under the declared reduction regime.

---

## 17. KURAMOTO-1984-CHEMICAL-OSCILLATIONS

Yoshiki Kuramoto.

Chemical Oscillations, Waves, and Turbulence.

Springer Series in Synergetics.

Volume 19.

Springer, Berlin, Heidelberg.

1984.

DOI:

`10.1007/978-3-642-69689-3`

Source class:

foundational monograph.

Repository role:

extended reference for:

- nonlinear oscillatory systems;
- reductive perturbation;
- phase description;
- weakly coupled oscillators;
- mutual entrainment;
- collective synchronization;
- oscillatory media.

---

## 18. Kuramoto 1984 Use Boundary

The monograph is used as an authoritative theoretical reference for phase-description methodology and coupled nonlinear oscillator behavior.

It is not used as a source for:

- TR-EIF ternary semantics;
- TR-EIF source code architecture;
- TR-EIP E(3) representation;
- material-specific FLiBe parameters.

---

## 19. Phase-Reduction Boundary

A phase reduction replaces a higher-dimensional oscillator state by an angular variable only under applicable assumptions.

Therefore:

`phase description ≠ complete original state`

The reduced phase model is a model-relative representation.

---

## 20. Oscillator Phase Boundary

Oscillator phase:

`θ`

is a dynamical coordinate.

It is not the same concept as a physical material phase.

Therefore:

`oscillator phase ≠ physical phase of matter`

---

## 21. SHINOMOTO-KURAMOTO-1986-ACTIVE-ROTATOR

Shigeru Shinomoto and Yoshiki Kuramoto.

"Phase Transitions in Active Rotator Systems."

Progress of Theoretical Physics.

Volume 75, Issue 5.

Pages 1105-1110.

1986.

DOI:

`10.1143/PTP.75.1105`

Source class:

related primary extension.

Repository role:

reference for active-rotator population dynamics and collective transitions in oscillator systems.

Relevant evidence domain:

- active rotators;
- oscillator populations;
- collective transitions;
- statistical phase dynamics.

---

## 22. Active Rotator Is Not Active Neutral

The phrase:

`active rotator`

in oscillator literature is not the TR-EIF concept:

`active neutral state 0`

Therefore:

`active rotator ≠ active neutral`

The shared adjective does not establish semantic identity.

---

## 23. SAKAGUCHI-KURAMOTO-1986-PHASE-LAG

Hidetsugu Sakaguchi and Yoshiki Kuramoto.

"A Soluble Active Rotator Model Showing Phase Transitions via Mutual Entrainment."

Progress of Theoretical Physics.

Volume 76, Issue 3.

Pages 576-581.

1986.

DOI:

`10.1143/PTP.76.576`

Source class:

foundational primary source.

Repository role:

primary source for the phase-lagged extension conventionally associated with the Sakaguchi-Kuramoto model.

Relevant evidence domain:

- phase-lagged coupling;
- mutual entrainment;
- active-rotator populations;
- collective phase transitions;
- deterministic coupled phase dynamics.

---

## 24. Sakaguchi-Kuramoto Equation

The original paper uses a convention algebraically expressible in the phase-lagged form:

`dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i - α)`

under the corresponding sign convention.

Equivalent source expressions may instead write the phase difference in reversed order with an overall minus sign.

The comparison must be algebraic, not typographic.

---

## 25. Phase-Lag Parameter

The phase-lag parameter is commonly denoted:

`α`

or another explicitly declared symbol.

It modifies the phase relation inside the coupling term.

It is a continuous model parameter.

---

## 26. Phase Lag Is Not Temporal Delay

A phase lag and a temporal delay are not generally identical quantities.

Therefore:

`phase lag ≠ time delay`

A relation between them requires additional dynamical assumptions, including an applicable frequency relation.

---

## 27. Phase Lag Is Not Ternary Routing

The phase-lag parameter does not define:

- `-1`;
- `0`;
- `1`;
- pending target;
- active-neutral entry;
- active-neutral exit.

Therefore:

`phase lag ≠ ternary transition rule`

---

## 28. Phase Lag Is Not Mechanical Force

The phase-lagged oscillator coupling term belongs to the continuous phase-dynamics layer.

It is not automatically a mechanical interatomic force.

Therefore:

`phase coupling ≠ mechanical force`

---

## 29. Phase Relation Is Not Chemical Bond

A phase relation between oscillators does not establish a chemical bond.

Therefore:

`phase relation ≠ chemical bond`

A physical interatomic interpretation requires an explicit model mapping.

---

## 30. Sakaguchi-Kuramoto Source Role

`SAKAGUCHI-KURAMOTO-1986-PHASE-LAG`

is admitted as the primary source for the phase-lagged coupled-oscillator extension used as mathematical background by TR-EIF.

It does not define the full TR-EIF continuous-discrete architecture.

---

## 31. Phase-Lag Sign Convention Audit

Every TR-EIF mathematical equation using a Sakaguchi-type phase lag must preserve an explicit sign convention.

For example, the forms:

`sin(θ_j - θ_i - α)`

and:

`-sin(θ_i - θ_j + α)`

are algebraically equivalent.

A validation audit must compare the complete expression before declaring inconsistency.

---

## 32. Coupling Normalization Audit

Source equations may normalize coupling through:

`K/N`

or another explicitly declared graph or population normalization.

TR-EIF extensions using weighted graphs must state the chosen normalization separately.

A weighted graph model must not be presented as identical to globally uniform all-to-all coupling.

---

## 33. Weighted Graph Extension Boundary

The classical globally coupled model and a weighted interaction graph are distinct constructions.

Therefore:

`global all-to-all Kuramoto coupling ≠ arbitrary weighted graph coupling`

TR-EIF may generalize the interaction structure.

That generalization is part of the TR-EIF model architecture and requires its own validation.

---

## 34. Local vs Global Coupling

A global order parameter summarizes population organization.

It does not uniquely determine every local phase relation.

Therefore:

`global order ≠ complete local state`

TR-EIF must preserve this distinction in multiscale and local-resonance analysis.

---

## 35. Order Parameter

For phases:

`θ_1, ..., θ_N`

the standard complex order parameter is commonly represented as:

`Z = (1/N) Σ_j exp(i θ_j)`

with magnitude:

`R = |Z|`

and collective phase given by the argument of:

`Z`

This provides a collective phase-order measure.

---

## 36. Order Parameter Boundary

The magnitude:

`R`

does not encode the complete oscillator state.

Many distinct phase configurations may have the same:

`R`

Therefore:

`R ≠ complete state`

---

## 37. Phase Order Is Not Resonance

TR-EIF preserves:

`R ≠ resonance`

A high phase-order magnitude is not by itself sufficient to establish the broader TR-EIF resonance classification.

---

## 38. Phase Order Is Not Complete Coherence

TR-EIF also preserves:

`phase order ≠ complete coherence`

A complete coherence model may require:

- local structure;
- topology;
- temporal persistence;
- multiple scales;
- additional observables.

---

## 39. Synchronization Boundary

The source literature uses synchronization in established oscillator-dynamics senses.

TR-EIF must not redefine every synchronized state as resonant.

Therefore:

`synchronization ≠ resonance`

---

## 40. Phase-Locking Boundary

Phase locking may occur when relevant relative phases remain bounded or stationary under the declared dynamical conditions.

TR-EIF preserves:

`phase locking ≠ resonance`

and:

`synchronization ≠ phase locking`

as general semantic distinctions.

---

## 41. Entrainment Boundary

Frequency entrainment and phase locking may be related in specific oscillator regimes.

They are not universally identical concepts.

The exact relation must follow the applicable source/model conditions.

---

## 42. Frequency Equality Boundary

Equal natural or observed frequencies do not by themselves establish resonance.

Therefore:

`frequency equality ≠ resonance`

This distinction remains mandatory throughout TR-EIF documentation.

---

## 43. Collective Transition Boundary

A collective synchronization transition in an oscillator population is not automatically:

- a physical material phase transition;
- a structural atomic transition;
- a ternary transition;
- a resonance-window crossing.

Therefore these terms must not be interchanged.

---

## 44. STROGATZ-2000-KURAMOTO-CRAWFORD

Steven H. Strogatz.

"From Kuramoto to Crawford: Exploring the Onset of Synchronization in Populations of Coupled Oscillators."

Physica D: Nonlinear Phenomena.

Volume 143, Issues 1-4.

Pages 1-20.

2000.

DOI:

`10.1016/S0167-2789(00)00094-4`

Source class:

review and mathematical reference.

Repository role:

secondary reference for the historical and mathematical development of synchronization onset in Kuramoto-type oscillator populations.

---

## 45. Strogatz 2000 Evidence Boundary

This source is admitted as a review/reference source.

It is not assigned primary provenance for the original Kuramoto construction.

It is useful for:

- mathematical context;
- bifurcation history;
- synchronization onset;
- interpretation of established literature.

---

## 46. ACEBRON-ET-AL-2005-KURAMOTO-REVIEW

Juan A. Acebrón.

Luis L. Bonilla.

Conrad J. Pérez Vicente.

Félix Ritort.

Renato Spigler.

"The Kuramoto Model: A Simple Paradigm for Synchronization Phenomena."

Reviews of Modern Physics.

Volume 77.

Page 137.

2005.

DOI:

`10.1103/RevModPhys.77.137`

Source class:

review and reference source.

Repository role:

broad reference for:

- Kuramoto-model mathematics;
- synchronization phenomena;
- numerical methods;
- model variants;
- applications.

---

## 47. Acebrón Review Boundary

`ACEBRON-ET-AL-2005-KURAMOTO-REVIEW`

is not used as primary provenance for the original Kuramoto or Sakaguchi equations.

Its role is literature synthesis and cross-checking.

---

## 48. PIKOVSKY-ROSENBLUM-KURTHS-2001-SYNCHRONIZATION

Arkady Pikovsky.

Michael Rosenblum.

Jürgen Kurths.

Synchronization: A Universal Concept in Nonlinear Sciences.

Cambridge University Press.

Cambridge Nonlinear Science Series.

Volume 12.

2001.

DOI:

`10.1017/CBO9780511755743`

Source class:

reference monograph.

Repository role:

general reference for synchronization concepts including:

- phase;
- frequency entrainment;
- phase locking;
- forced synchronization;
- mutual synchronization;
- oscillator populations.

---

## 49. Synchronization Monograph Boundary

This monograph is used to clarify synchronization terminology.

It does not establish that synchronization and resonance are identical.

TR-EIF explicitly rejects that identification.

---

## 50. OTT-ANTONSEN-2008-LOW-DIMENSIONAL

Edward Ott and Thomas M. Antonsen.

"Low Dimensional Behavior of Large Systems of Globally Coupled Oscillators."

Chaos.

Volume 18, Issue 3.

Article 037113.

2008.

DOI:

`10.1063/1.2930766`

Source class:

primary methodological extension.

Repository role:

reference for exact low-dimensional reduction of specified large coupled-oscillator systems under the assumptions treated by the paper.

---

## 51. Ott-Antonsen Boundary

The Ott-Antonsen reduction is not a universal reduction for arbitrary oscillator systems.

Its applicability depends on the mathematical conditions of the selected model and state/distribution class.

Therefore:

`Ott-Antonsen reduction ≠ universal oscillator reduction`

---

## 52. Reduced Dynamics Boundary

A reduced macroscopic system may reproduce specified collective dynamics.

It does not necessarily reconstruct every microscopic oscillator state.

Therefore:

`macroscopic reduction ≠ complete microscopic identity`

---

## 53. Source-to-TR-EIF Mapping

The source roles in TR-EIF are:

### Winfree

historical precursor for interacting oscillator populations.

### Kuramoto 1975

foundational mean-field coupled-phase-oscillator construction.

### Kuramoto 1984

extended phase-description and nonlinear-oscillator reference.

### Shinomoto-Kuramoto 1986

active-rotator and collective-transition extension.

### Sakaguchi-Kuramoto 1986

phase-lagged coupled-oscillator extension.

### Strogatz 2000

historical/mathematical review of synchronization onset.

### Acebrón et al. 2005

broad Kuramoto review and reference.

### Pikovsky, Rosenblum, and Kurths 2001

general synchronization reference.

### Ott-Antonsen 2008

low-dimensional analytical reduction under specified conditions.

---

## 54. TR-EIF Author-Defined Extensions

The following TR-EIF concepts are not attributed directly to the source literature above unless a specific source record states otherwise:

- balanced ternary execution layer;
- active neutral state `0`;
- neutral routing;
- pending-target semantics;
- prohibition of direct committed `-1 ↔ 1`;
- continuous-to-ternary request mapping;
- E(3)-equivariant TR-EIP integration;
- resonance-conditioned interatomic features;
- ternary-conditioned interatomic features;
- FLiBe TR-EIP realization;
- TR-EIF multiscale architecture.

These remain TR-EIF-specific constructions or integrations.

---

## 55. Continuous Dynamics Preserve Their Domain

Kuramoto-Sakaguchi-type dynamics are continuous phase dynamics.

TR-EIF does not replace that continuous state with three discrete values.

The architectural relation is:

`continuous nonlinear dynamics`

`→ continuous descriptor`

`→ explicit target mapping`

`→ ternary execution`

not:

`continuous dynamics = ternary state`

---

## 56. Ternary Layer Is Not a Numerical Approximation of Phase

Balanced ternary execution must not be described merely as coarse quantization of oscillator phase.

State:

`0`

has active execution semantics that are not equivalent to a midpoint angle or zero phase.

Therefore:

`ternary state ≠ phase quantization`

---

## 57. Three-State Architecture Boundary

The existence of three ternary execution states does not imply that the continuous physical or dynamical state has only three possible values.

Therefore:

`three execution states ≠ three-valued physical dynamics`

Continuous nonlinear dynamics remain continuous.

---

## 58. Energy-Flow Claim Boundary

The Kuramoto and Sakaguchi sources support phase-dynamical formalism.

They do not by themselves establish a TR-EIF physical theory of energy flow through `-1/0/1`.

Any such physical claim requires an explicit TR-EIF model and corresponding scientific evidence.

---

## 59. Interatomic Claim Boundary

The phase-oscillator sources do not establish:

- interatomic potential accuracy;
- force accuracy;
- stress accuracy;
- chemical bonding;
- FLiBe property prediction.

These claims belong to separate evidence registers.

---

## 60. E(3) Boundary

Kuramoto-Sakaguchi phase dynamics do not by themselves define spatial E(3) equivariance.

TR-EIF combines distinct mathematical structures:

`phase dynamics`

and:

`E(3)-equivariant spatial modeling`

Their combination is part of TR-EIF architecture.

---

## 61. Coupling Graph Boundary

A TR-EIF oscillator interaction graph may be:

- local;
- weighted;
- geometry-dependent;
- model-relative.

Classical globally coupled source equations must not be cited as direct proof of every graph-generalized property.

---

## 62. Heterogeneous Coupling Boundary

Introducing edge-dependent:

`K_ij`

or another local coupling structure is an extension of the globally uniform model.

The extension requires its own mathematical and executable validation.

---

## 63. Local Phase Lag Boundary

Introducing node- or edge-dependent phase lag is an extension beyond a single global Sakaguchi phase-lag parameter.

Such extensions must not be attributed directly to the 1986 source unless that exact structure is supported.

---

## 64. Time-Varying Coupling Boundary

Time-dependent coupling is another extension.

A static-coupling source does not directly establish theorems for a time-dependent system.

---

## 65. Thermal Coupling Boundary

Thermodynamic temperature may influence a concrete TR-EIF coupling law through an explicit model.

Kuramoto-Sakaguchi sources do not identify thermodynamic temperature with phase dynamics.

Therefore:

`thermodynamic temperature ≠ oscillator phase parameter`

---

## 66. Material Parameter Boundary

No source in this register supplies a validated FLiBe-specific:

- coupling constant;
- phase lag;
- resonance window;
- ternary threshold;
- TR-EIP parameter

unless separately admitted through the FLiBe source register.

---

## 67. Source Provenance Classes in This Register

The principal source classes are:

| Source identifier | Evidence role |
| --- | --- |
| `WINFREE-1967-COUPLED-OSCILLATORS` | foundational primary precursor |
| `KURAMOTO-TSUZUKI-1974-REDUCTIVE-PERTURBATION` | foundational primary method background |
| `KURAMOTO-1975-SELF-ENTRAINMENT` | foundational primary Kuramoto source |
| `KURAMOTO-1984-CHEMICAL-OSCILLATIONS` | foundational monograph |
| `SHINOMOTO-KURAMOTO-1986-ACTIVE-ROTATOR` | primary extension |
| `SAKAGUCHI-KURAMOTO-1986-PHASE-LAG` | foundational primary phase-lag source |
| `PIKOVSKY-ROSENBLUM-KURTHS-2001-SYNCHRONIZATION` | reference monograph |
| `STROGATZ-2000-KURAMOTO-CRAWFORD` | review/reference |
| `ACEBRON-ET-AL-2005-KURAMOTO-REVIEW` | review/reference |
| `OTT-ANTONSEN-2008-LOW-DIMENSIONAL` | primary methodological extension |

---

## 68. Source-Use Rule

A source may be cited only for the claim it supports.

For example:

`SAKAGUCHI-KURAMOTO-1986-PHASE-LAG`

supports phase-lagged oscillator coupling.

It must not be used as direct evidence for TR-EIF active-neutral semantics.

---

## 69. Review-Use Rule

Review sources may support:

- terminology;
- historical synthesis;
- literature context;
- known result summaries.

Where the origin of a specific model or theorem matters, use the primary source.

---

## 70. Equation Provenance Rule

When TR-EIF documentation presents a canonical Kuramoto or Sakaguchi-Kuramoto equation, the applicable source lineage should be identifiable from this register.

TR-EIF-specific modifications must be identified as modifications.

---

## 71. Sign-Convention Rule

Sign differences in phase equations must be checked algebraically.

The source audit must not report false discrepancies produced only by:

- reversing phase-difference order;
- moving an overall minus sign;
- changing the sign convention for phase lag.

---

## 72. Order-Parameter Provenance

The Kuramoto literature supports use of a collective complex order parameter for phase organization.

TR-EIF may use the phase-order magnitude as one continuous descriptor component.

This does not make the order parameter identical to the entire TR-EIF resonance concept.

---

## 73. Coherence Terminology Rule

If TR-EIF uses the term:

`coherence`

the relevant definition must be stated explicitly.

It must not be assumed to mean exactly the same quantity as the canonical Kuramoto order-parameter magnitude unless that equality is declared.

---

## 74. R(t) and C(t)

TR-EIF preserves:

`R(t) ≠ C(t)`

unless a particular model explicitly defines those quantities to coincide.

The source register must not erase this distinction through generic synchronization terminology.

---

## 75. Stability Source Boundary

A source discussing stability in one oscillator model does not automatically establish stability of a TR-EIF generalized graph, resonance, or ternary-coupled system.

Stability results remain assumption-dependent.

---

## 76. Bifurcation Source Boundary

A bifurcation result for a source model must retain its:

- model;
- parameter domain;
- population limit;
- distribution assumptions;
- coupling structure.

It must not be generalized automatically to TR-EIF.

---

## 77. Infinite-Population Boundary

Results established in the:

`N → ∞`

limit must not automatically be asserted for a finite oscillator population without an applicable finite-size argument.

---

## 78. Frequency-Distribution Boundary

Results depending on a specific natural-frequency distribution must preserve that assumption.

A Lorentzian-distribution theorem is not automatically a theorem for arbitrary distributions.

---

## 79. Mean-Field Boundary

A mean-field result is not automatically a local-network result.

Therefore:

`mean-field theorem ≠ arbitrary graph theorem`

Graph-generalized TR-EIF results require separate justification.

---

## 80. Noise Boundary

Deterministic source equations do not automatically establish stochastic oscillator behavior.

Adding noise defines another model.

Its stochastic assumptions require their own sources and validation.

---

## 81. Delay Boundary

A delayed oscillator system is not identical to a phase-lagged instantaneous system.

Therefore:

`time delay ≠ phase lag`

even when approximations may relate them in specific regimes.

---

## 82. Active-Rotator Terminology

The source phrase:

`active rotator`

must be preserved in its oscillator-model meaning.

TR-EIF documentation must not use the phrase as evidence for active-neutral ternary state.

---

## 83. Mutual Entrainment Terminology

`mutual entrainment`

belongs to coupled oscillator dynamics.

It must not be used as a synonym for:

- interatomic bonding;
- energy conservation;
- ternary routing;
- material phase locking.

---

## 84. Synchronization Terminology

Synchronization may involve relationships among oscillator frequencies and phases.

The exact definition must follow the applicable model.

TR-EIF does not treat synchronization as a universal synonym for coherence or resonance.

---

## 85. Phase-Locking Terminology

Phase locking concerns phase relationships under a declared oscillator model.

It is not a statement about spatial atomic locking or crystal structure.

---

## 86. Source Register Release Audit

Before release, this source register must be audited for:

- author spelling;
- title accuracy;
- publication year;
- journal/book identity;
- volume and pages;
- DOI accuracy;
- evidence-role accuracy;
- source-to-claim correspondence.

---

## 87. DOI Audit

The DOI values recorded in this register are identifiers of the corresponding publications.

They must not be altered to tracking or redirect URLs.

Canonical DOI strings are preferred.

---

## 88. Source Stability

Once these identifiers are referenced by other repository artifacts, unnecessary renaming should be avoided.

If an identifier changes, dependent references must be updated together.

---

## 89. No Physical Parameter Extraction by Default

This source register does not extract numeric physical parameters for TR-EIF.

A source citation alone does not authorize insertion of a coupling parameter into executable code.

Parameter admission requires a separate parameter provenance record.

---

## 90. No Hidden Parameter Transfer

No Kuramoto, Sakaguchi, or review-source parameter is silently imported into:

- FLiBe;
- TR-EIP;
- MD;
- multiscale closure;
- ternary execution.

All result-affecting parameters remain explicit.

---

## 91. FRP Boundary

FRP remains a separate project.

Confirmed semantic correspondences may be used as read-only references.

This source register does not import FRP-specific:

- `γ_nominal`;
- `K_0`;
- scheduler modes;
- RTL architecture;
- retained-frequency parameters;
- thresholds.

Such values are not Kuramoto-Sakaguchi literature values for TR-EIF.

---

## 92. TR-EIF Equation Audit

Every TR-EIF equation derived from or inspired by these sources must be classified as one of:

- source-equivalent form;
- algebraically equivalent notation;
- explicit generalization;
- TR-EIF-specific extension.

The classification prevents similarity from being mistaken for identity.

---

## 93. Source-Equivalent Form

A source-equivalent form differs only by mathematically equivalent notation.

Examples may include:

- phase-difference order;
- summation index naming;
- equivalent sine-sign convention.

---

## 94. Explicit Generalization

A generalization changes the mathematical model.

Examples include:

- weighted graphs;
- local couplings;
- state-dependent couplings;
- heterogeneous phase lag;
- geometry-conditioned coupling.

Such changes must be labeled as extensions.

---

## 95. TR-EIF-Specific Extension

A TR-EIF-specific extension may combine:

- continuous oscillator dynamics;
- resonance descriptors;
- balanced ternary target mapping;
- active-neutral execution;
- E(3)-equivariant interatomic modeling.

No single source in this register defines that complete synthesis.

---

## 96. Source Evidence and Mathematical Proof

A source citation identifies external literature.

A TR-EIF theorem using the source formalism still requires its own assumptions and proof if the theorem is claimed within TR-EIF.

Therefore:

`citation ≠ proof`

---

## 97. Source Evidence and Executable Test

Likewise:

`citation ≠ executable qualification`

Implementation must be tested independently.

---

## 98. Source Evidence and Physical Validation

A correct historical citation does not establish physical validity of a TR-EIF material model.

Therefore:

`theory source ≠ FLiBe validation`

---

## 99. Core Source Invariants

This register preserves:

1. Winfree and Kuramoto models remain distinct.
2. Kuramoto formalism remains distinct from TR-EIF.
3. Sakaguchi-Kuramoto formalism remains distinct from TR-EIF.
4. Synchronization remains distinct from resonance.
5. Phase locking remains distinct from resonance.
6. Frequency equality remains distinct from resonance.
7. Phase order remains distinct from complete coherence.
8. Oscillator phase remains distinct from physical phase of matter.
9. Phase coupling remains distinct from mechanical force.
10. Phase relation remains distinct from chemical bond.
11. Phase lag remains distinct from temporal delay.
12. Phase dynamics remain continuous.
13. Continuous phase state remains distinct from balanced ternary execution.
14. Active-neutral semantics are not attributed to Kuramoto/Sakaguchi.
15. E(3) spatial equivariance is not supplied by Kuramoto-Sakaguchi theory.
16. Material-specific parameters are not supplied by generic oscillator theory.
17. Mean-field results are not automatically graph-general results.
18. Infinite-population results are not automatically finite-population results.
19. Distribution-specific results remain distribution-specific.
20. Source-equivalent notation remains distinguishable from model generalization.
21. Review sources remain distinct from primary origin sources.
22. Source citation does not replace mathematical proof.
23. Source citation does not replace executable validation.
24. Similarity is not identity.

---

## 100. Related Documentation

This register supports:

`docs/volume_02_ternary_resonance_theory/`

`docs/specifications/resonance_descriptor_specification.md`

`docs/architecture/continuous_discrete_contract.md`

`docs/validation/mathematical_validation_plan.md`

`docs/validation/scientific_validation_plan.md`

and future source-specific audits.

---

## 101. Summary

The Kuramoto-Sakaguchi literature provides an established mathematical foundation for coupled continuous phase dynamics.

TR-EIF uses that foundation without collapsing its own architectural layers into the source models.

The source chain is:

`Winfree oscillator populations`

`→ Kuramoto mean-field phase dynamics`

`→ phase-description development`

`→ Sakaguchi-Kuramoto phase-lag extension`

`→ later analytical and review literature`

while TR-EIF adds its own explicitly separated architecture:

`continuous phase dynamics`

`→ continuous resonance descriptor`

`→ explicit continuous-to-ternary request mapping`

`→ active-neutral -1/0/1 execution`

`→ E(3)-equivariant interatomic realization`

The controlling scientific rule remains:

`source correspondence must be exact`

and:

`similar ≠ identical`
