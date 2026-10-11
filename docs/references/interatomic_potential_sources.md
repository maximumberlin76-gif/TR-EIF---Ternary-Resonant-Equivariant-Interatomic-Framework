# Interatomic Potential Sources

## 1. Scope

This document defines the source register for interatomic potential theory, potential-energy representations, conservative force construction, atomic-environment descriptors, and machine-learned interatomic potentials relevant to the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The register covers sources relevant to:

- pair and many-body potentials;
- environment-dependent potentials;
- embedded-atom models;
- bond-order models;
- local atomic-energy decomposition;
- potential-energy surfaces;
- machine-learned potentials;
- symmetry-preserving atomic descriptors;
- Gaussian approximation potentials;
- spectral neighbor analysis;
- moment tensor potentials;
- neural-network potential-energy surfaces;
- energy-conserving force fields;
- force derivation from scalar energy;
- stress-related energy derivatives;
- locality and transferability;
- training and validation boundaries.

This register does not define the complete TR-EIF architecture.

It does not define balanced ternary execution.

It does not define active-neutral state `0`.

It does not define the TR-EIF resonance layer.

It does not provide FLiBe-specific physical parameters.

---

## 2. Architectural Source Boundary

Interatomic-potential literature provides established methods for mapping atomic configuration to energy and related observables.

The architectural relation is:

`interatomic-potential theory`

`→ TR-EIP conservative interatomic layer`

not:

`interatomic-potential literature = TR-EIP`

TR-EIP is a distinct model family inside TR-EIF.

---

## 3. TR-EIP Nesting

The model-family relation remains:

`TR-EIP ⊂ TR-EIF`

TR-EIP combines the interatomic energy layer with additional TR-EIF structures including:

- E(3)-equivariant representations;
- continuous resonance descriptors;
- balanced ternary conditioning;
- active-neutral execution semantics;
- deterministic traceability;
- multiscale integration.

No source in this register defines that complete architecture.

---

## 4. Interatomic Potential Definition

An interatomic potential represents a mapping from an admissible atomic configuration to a scalar potential energy.

Abstractly:

`E = E(X)`

where:

`X`

contains the declared atomic and geometric state.

A concrete model may additionally depend on:

- species;
- cell;
- charge state;
- electronic descriptors;
- latent features;
- explicitly declared external variables.

---

## 5. Energy Is Scalar

Potential energy is a scalar physical or model observable.

It is not:

- a ternary state;
- a resonance region;
- a graph edge;
- a validation status.

Therefore:

`energy ≠ ternary state`

---

## 6. Force Relation

For a differentiable conservative potential-energy model:

`F_i = -∂E/∂r_i`

or equivalently:

`F = -∇E`

under the declared coordinate convention.

This relation defines the conservative force path used by TR-EIF.

---

## 7. Force Is Not Energy

Force and energy occupy different mathematical spaces.

Energy is scalar.

Force is vector-valued.

Therefore:

`force ≠ energy`

even though force may be derived from energy.

---

## 8. Force Is Not Ternary State

A force component equal numerically to:

`-1`

`0`

or:

`1`

remains a force component.

Therefore:

`force ≠ ternary state`

and:

`zero force ≠ active neutral 0`

---

## 9. Stress Boundary

Stress may be related to an energy derivative with respect to strain under a declared convention.

The sign and normalization convention must remain explicit.

A source using a different stress convention must not be treated as numerically identical without conversion.

---

## 10. Atomic Energy Decomposition

Many interatomic models represent total energy as:

`E_total = Σ_i E_i`

where:

`E_i`

is an atomic or local model contribution.

Such contributions are model decomposition terms.

They are not automatically independently measurable physical atomic energies.

---

## 11. Locality Boundary

A local potential assumes that the relevant contribution to an atomic environment can be represented within a declared neighborhood or cutoff.

Locality is a model assumption.

It is not a universal physical theorem.

---

## 12. Cutoff Boundary

A finite cutoff defines a computational neighborhood.

It does not automatically define:

- a chemical bond;
- a physical coordination shell;
- the complete interaction range.

Therefore:

`cutoff neighbor ≠ chemical bond`

---

## 13. Pair-Potential Boundary

A pair potential has a form based on pairwise separation contributions.

A pair-potential model cannot automatically represent every many-body environmental effect.

Therefore:

`pairwise geometry ≠ complete many-body environment`

---

## 14. Many-Body Potential Boundary

A many-body potential includes dependence beyond independent pair contributions.

Many-body dependence may enter through:

- local density;
- angular terms;
- bond order;
- invariant descriptors;
- tensor moments;
- neural latent features.

Different mechanisms are not identical merely because they are many-body.

---

## 15. DAW-BASKES-1983-EAM-INTRODUCTION

Murray S. Daw.

Michael I. Baskes.

"Semiempirical, Quantum Mechanical Calculation of Hydrogen Embrittlement in Metals."

Physical Review Letters.

Volume 50.

Page 1285.

1983.

DOI:

`10.1103/PhysRevLett.50.1285`

Source class:

foundational primary interatomic-potential source.

Repository role:

early embedded-atom-method source and historical origin of the EAM framework.

Relevant evidence domain:

- semiempirical metallic interaction modeling;
- embedding concept;
- many-body metallic environments;
- hydrogen-metal application.

---

## 16. DAW-BASKES-1984-EAM

Murray S. Daw.

Michael I. Baskes.

"Embedded-atom method: Derivation and application to impurities, surfaces, and other defects in metals."

Physical Review B.

Volume 29.

Page 6443.

1984.

DOI:

`10.1103/PhysRevB.29.6443`

Source class:

foundational primary interatomic-potential source.

Repository role:

principal foundational reference for the embedded-atom method.

Relevant evidence domain:

- many-body metallic potentials;
- local host electron-density representation;
- embedding energy;
- pair contributions;
- defects;
- surfaces;
- impurity environments.

---

## 17. Embedded-Atom Energy Structure

A generic EAM-type total-energy structure may be represented schematically as:

`E = Σ_i F_i(ρ_i) + 1/2 Σ_i Σ_(j≠i) φ_ij(r_ij)`

where:

- `F_i` is an embedding function;
- `ρ_i` is a local host-density measure;
- `φ_ij` is a pair contribution.

Exact source conventions and parameterizations vary.

---

## 18. EAM Boundary

The embedded local density in EAM is a model quantity.

It is not automatically the physical electron density field of a full electronic-structure calculation.

Therefore:

`EAM density ≠ complete electronic density`

---

## 19. EAM Is Not Universal

EAM was developed for metallic systems.

Its successful application to particular metals does not establish universal validity for:

- covalent systems;
- ionic melts;
- molecular systems;
- FLiBe.

Therefore:

`EAM success in metals ≠ FLiBe validation`

---

## 20. FINNIS-SINCLAIR-1984

M. W. Finnis.

J. E. Sinclair.

"A simple empirical N-body potential for transition metals."

Philosophical Magazine A.

Volume 50, Issue 1.

Pages 45-55.

1984.

DOI:

`10.1080/01418618408244210`

Source class:

foundational many-body metallic-potential source.

Repository role:

reference for compact many-body energy representations in transition-metal atomistic simulation.

Relevant evidence domain:

- transition-metal many-body potentials;
- local density-like bonding term;
- repulsive pair term;
- cohesive and defect energetics.

---

## 21. Finnis-Sinclair Boundary

Finnis-Sinclair and EAM share related many-body concepts.

They are not automatically identical formulations.

Therefore:

`Finnis-Sinclair ≠ EAM`

unless a specific mathematical equivalence is explicitly established for the selected forms.

---

## 22. STILLINGER-WEBER-1985

Frank H. Stillinger.

Thomas A. Weber.

"Computer simulation of local order in condensed phases of silicon."

Physical Review B.

Volume 31.

Page 5262.

1985.

DOI:

`10.1103/PhysRevB.31.5262`

Source class:

foundational many-body covalent-potential source.

Repository role:

reference for explicit two-body plus three-body interatomic interactions and angular local-order modeling.

Relevant evidence domain:

- silicon;
- two-body interactions;
- three-body interactions;
- angular structure;
- local order;
- molecular-dynamics application.

---

## 23. Stillinger-Weber Boundary

The Stillinger-Weber model includes explicit angular many-body structure.

It does not establish that every many-body system can be represented by the same functional form.

Therefore:

`three-body term ≠ universal many-body potential`

---

## 24. TERSOFF-1988-BOND-ORDER

J. Tersoff.

"New empirical approach for the structure and energy of covalent systems."

Physical Review B.

Volume 37.

Page 6991.

1988.

DOI:

`10.1103/PhysRevB.37.6991`

Source class:

foundational bond-order potential source.

Repository role:

reference for environment-dependent bond-order treatment in covalent interatomic models.

Relevant evidence domain:

- covalent systems;
- local environment dependence;
- bond order;
- structural energetics;
- silicon potential modeling.

---

## 25. Bond-Order Boundary

Bond-order potentials encode environmental dependence of interaction strength.

A model bond-order variable is not automatically a directly measured chemical bond order.

Therefore:

`model bond order ≠ experimentally measured bond order`

unless a validated correspondence is supplied.

---

## 26. Empirical Potential Boundary

An empirical potential is defined by its model form and calibration evidence.

Empirical success in one training/calibration domain does not establish transferability to another domain.

Therefore:

`fit accuracy ≠ universal transferability`

---

## 27. Potential-Energy Surface

A potential-energy surface maps configuration variables to energy.

The dimensionality of the full surface grows with the represented degrees of freedom.

A machine-learned model may approximate such a surface from reference data.

---

## 28. Reference-Energy Boundary

Reference energies used to construct an interatomic potential may come from:

- experiment;
- first-principles calculations;
- higher-level electronic structure;
- another potential;
- synthetic benchmarks.

The evidence class must remain explicit.

---

## 29. Training Data Are Not Model Output

Training targets belong to the reference evidence path.

Model prediction belongs to the evaluated model path.

Therefore:

`training target ≠ prediction`

even when their numerical values coincide.

---

## 30. BEHLER-PARRINELLO-2007

Jörg Behler.

Michele Parrinello.

"Generalized Neural-Network Representation of High-Dimensional Potential-Energy Surfaces."

Physical Review Letters.

Volume 98.

Article 146401.

2007.

DOI:

`10.1103/PhysRevLett.98.146401`

Source class:

foundational primary neural-network-potential source.

Repository role:

reference for atom-centered decomposition and neural-network representation of high-dimensional potential-energy surfaces.

Relevant evidence domain:

- high-dimensional potential-energy surfaces;
- atom-centered local representations;
- neural-network atomic contributions;
- energies;
- forces;
- periodic and nonperiodic systems.

---

## 31. Behler-Parrinello Source Role

The Behler-Parrinello construction is a foundational machine-learning interatomic-potential architecture.

It demonstrates a route from local atomic environments to extensive total energy.

It is not TR-EIP.

Therefore:

`Behler-Parrinello potential ≠ TR-EIP`

---

## 32. Atom-Centered Symmetry Boundary

An atom-centered descriptor is designed to remove or control irrelevant degrees of freedom such as translation, rotation, and permutation.

The precise descriptor determines what information is retained.

Therefore:

`symmetry-adapted descriptor ≠ complete local environment automatically`

---

## 33. Descriptor Completeness Boundary

Two distinct atomic environments can be indistinguishable under an insufficient descriptor.

Therefore descriptor quality must consider:

- invariance;
- uniqueness or faithfulness;
- smoothness;
- differentiability;
- numerical stability.

---

## 34. BARTOK-ET-AL-2010-GAP

Albert P. Bartók.

Mike C. Payne.

Risi Kondor.

Gábor Csányi.

"Gaussian Approximation Potentials: The Accuracy of Quantum Mechanics, without the Electrons."

Physical Review Letters.

Volume 104.

Article 136403.

2010.

DOI:

`10.1103/PhysRevLett.104.136403`

Source class:

foundational machine-learning interatomic-potential source.

Repository role:

reference for Gaussian-process-based interatomic potential construction from quantum-mechanical energy and force data.

Relevant evidence domain:

- Gaussian approximation potentials;
- nonparametric potential fitting;
- energy and force reference data;
- systematically improvable data-driven potentials.

---

## 35. GAP Boundary

A Gaussian Approximation Potential is one machine-learning potential family.

It is not equivalent to every Gaussian-process model.

It is not equivalent to every descriptor used with GAP.

Therefore:

`GAP ≠ SOAP`

SOAP may serve as one representation used within GAP or other models.

---

## 36. BARTOK-KONDOR-CSANYI-2013-SOAP

Albert P. Bartók.

Risi Kondor.

Gábor Csányi.

"On representing chemical environments."

Physical Review B.

Volume 87.

Article 184115.

2013.

DOI:

`10.1103/PhysRevB.87.184115`

Source class:

primary atomic-environment-representation source.

Repository role:

reference for rigorous analysis of atomic-environment representations and the smooth overlap of atomic positions construction.

Relevant evidence domain:

- atomic environment representation;
- translation invariance;
- rotation/reflection invariance;
- permutation invariance;
- differentiability;
- representation faithfulness.

---

## 37. SOAP Boundary

SOAP is an atomic-environment representation.

It is not an interatomic potential by itself.

Therefore:

`SOAP ≠ potential`

A potential requires an additional mapping from representation to energy or another observable.

---

## 38. Representation vs Regression

Atomic representation and regression/model architecture are distinct layers.

Therefore:

`descriptor ≠ regressor`

and:

`descriptor ≠ energy functional`

A single descriptor may be used by different model families.

---

## 39. THOMPSON-ET-AL-2015-SNAP

A. P. Thompson.

L. P. Swiler.

C. R. Trott.

S. M. Foiles.

G. J. Tucker.

"Spectral neighbor analysis method for automated generation of quantum-accurate interatomic potentials."

Journal of Computational Physics.

Volume 285.

Pages 316-330.

2015.

DOI:

`10.1016/j.jcp.2014.12.018`

Source class:

primary machine-learning interatomic-potential source.

Repository role:

reference for Spectral Neighbor Analysis Potentials and bispectrum-based local environment representation.

Relevant evidence domain:

- spectral neighbor analysis;
- bispectrum components;
- local environment descriptors;
- automated fitting;
- energies;
- forces;
- stress tensors.

---

## 40. SNAP Boundary

SNAP combines a spectral local-environment representation with a fitted potential form.

Its bispectrum representation and fitting architecture are specific to SNAP.

Therefore:

`SNAP ≠ GAP`

`SNAP ≠ MTP`

`SNAP ≠ TR-EIP`

---

## 41. SHAPEEV-2016-MTP

Alexander V. Shapeev.

"Moment Tensor Potentials: A Class of Systematically Improvable Interatomic Potentials."

Multiscale Modeling & Simulation.

Volume 14, Issue 3.

Pages 1153-1173.

2016.

DOI:

`10.1137/15M1054183`

Source class:

primary mathematical machine-learning interatomic-potential source.

Repository role:

reference for systematically improvable moment-tensor representations of local atomic environments.

Relevant evidence domain:

- moment tensor potentials;
- invariant local representations;
- approximation of quantum-mechanical interactions;
- systematic improvability;
- interatomic-potential construction.

---

## 42. MTP Boundary

Moment Tensor Potentials use a specific invariant basis construction.

They are not identical to:

- SOAP;
- SNAP;
- neural-network potentials;
- equivariant tensor neural networks.

Common goals do not imply identical mathematics.

---

## 43. CHMIELA-ET-AL-2017-GDML

Stefan Chmiela.

Alexandre Tkatchenko.

Huziel E. Sauceda.

Igor Poltavsky.

Kristof T. Schütt.

Klaus-Robert Müller.

"Machine learning of accurate energy-conserving molecular force fields."

Science Advances.

Volume 3, Issue 5.

Article e1603015.

2017.

DOI:

`10.1126/sciadv.1603015`

Source class:

primary energy-conserving machine-learning force-field source.

Repository role:

reference for construction of conservative machine-learned molecular force fields through gradient-domain learning.

Relevant evidence domain:

- force-field learning;
- conservative vector fields;
- energy conservation;
- force learning;
- potential-energy reconstruction;
- ab initio trajectory references.

---

## 44. GDML Boundary

Gradient-domain machine learning provides one route to conservative learned force fields.

TR-EIF's reference force evaluator instead derives forces from its scalar energy path through the declared differentiation contract.

Therefore:

`GDML architecture ≠ TR-EIP force architecture`

---

## 45. Conservative Force Requirement

A conservative force field must correspond to a scalar potential under the applicable mathematical conditions.

Training independent unconstrained force components does not automatically guarantee conservativity.

Therefore:

`force predictor ≠ conservative force field`

unless the relevant integrability/conservative structure is established.

---

## 46. Energy-Conserving Boundary

Energy conservation in a closed conservative system is a physical/dynamical property.

A model being derived from an energy potential supports conservative force structure.

Finite numerical integration may still introduce numerical energy drift.

Therefore:

`conservative potential ≠ zero numerical drift at finite step`

---

## 47. Reference Data Boundary

Machine-learning interatomic potentials inherit information from their reference data.

Their physical validity cannot exceed evidence solely because the regression architecture is sophisticated.

Therefore:

`advanced architecture ≠ source-quality upgrade`

---

## 48. First-Principles Training Boundary

A potential trained on first-principles calculations approximates the selected first-principles reference within its learned domain.

It is not automatically experimental evidence.

Therefore:

`DFT-trained potential ≠ experimental measurement`

---

## 49. First-Principles Method Identity

A first-principles training set must retain the relevant computational method.

Different electronic-structure settings may define different reference surfaces.

Therefore:

`all DFT data ≠ one identical reference model`

---

## 50. Local Energy Boundary

Local atomic energy decompositions may enable extensive total-energy models.

The decomposition is often not unique.

Therefore:

`same total energy ≠ unique atomic energy decomposition`

unless uniqueness is separately established.

---

## 51. Extensive Energy

For isolated noninteracting replicated subsystems, an extensive energy model should satisfy an additive relation under the corresponding model assumptions.

This principle underlies structural scaling tests.

It is not a universal claim for interacting replicas.

---

## 52. Interaction Range

Two replicas separated beyond the model interaction range may become independent under a strictly local model.

This independence is model-specific.

Long-range interactions can violate the assumption.

---

## 53. Long-Range Boundary

Electrostatic, polarization, dispersion, or other long-range contributions may require explicit treatment.

A short-range learned local potential does not automatically represent them.

Therefore:

`local ML potential ≠ complete long-range physics`

---

## 54. Ionic-System Boundary

Ionic materials may contain long-range electrostatic structure and polarization effects.

A potential designed for neutral covalent environments must not be assumed transferable to ionic melts.

Therefore:

`covalent-potential success ≠ ionic-melt validity`

---

## 55. FLiBe Boundary

FLiBe is an ionic molten-salt system.

No generic interatomic-potential source in this register automatically validates a FLiBe potential.

FLiBe-specific evidence belongs to:

`docs/references/flibe_sources.md`

---

## 56. Classical Potential vs TR-EIP

A classical analytic potential specifies an explicit functional form.

TR-EIP is a separate model-family architecture.

Therefore:

`classical potential ≠ TR-EIP`

even when both map atomic configuration to energy.

---

## 57. Machine-Learned Potential vs TR-EIP

A machine-learned interatomic potential may share:

- atomic-energy decomposition;
- local environments;
- energy-gradient forces;
- symmetry constraints

with TR-EIP.

Shared structures do not establish model identity.

---

## 58. Equivariant Potential Boundary

Modern equivariant interatomic potentials are registered separately in:

`docs/references/equivariant_model_sources.md`

This register focuses on the broader interatomic-potential lineage.

Overlap is allowed only where the evidence role requires it.

---

## 59. Source-Register Separation

The source-register separation is:

`interatomic_potential_sources.md`

for energy-model and potential lineage,

and:

`equivariant_model_sources.md`

for geometric representation and equivariant architecture lineage.

The two domains intersect.

They are not identical.

---

## 60. Potential vs Dynamics

An interatomic potential defines potential energy.

Molecular dynamics defines time evolution using forces and an integration scheme.

Therefore:

`interatomic potential ≠ molecular dynamics`

A valid potential does not by itself define a complete trajectory algorithm.

---

## 61. Potential vs Thermostat

A thermostat modifies or controls dynamical sampling.

It is not part of the potential-energy function unless explicitly coupled by the selected model.

Therefore:

`potential ≠ thermostat`

---

## 62. Potential vs Barostat

A barostat controls pressure/cell degrees of freedom under a declared dynamics algorithm.

It is not the scalar interatomic potential itself.

---

## 63. Potential vs Resonance Dynamics

TR-EIF resonance dynamics are a separate continuous layer.

Therefore:

`potential-energy model ≠ resonance dynamics`

A resonance descriptor may condition the energy path through an explicit TR-EIP mapping.

---

## 64. Potential vs Ternary Execution

Balanced ternary execution is also a separate state layer.

Therefore:

`interatomic potential ≠ ternary state machine`

A retained ternary state may condition the model without becoming the energy itself.

---

## 65. Active Neutral Boundary

State:

`0`

is active neutral.

An energy model may assign a distinct numerical conditioning behavior to it.

Active neutral is not:

- zero energy;
- zero force;
- missing potential;
- failed evaluation.

---

## 66. Potential Zero Boundary

A potential energy value of zero depends on the selected energy reference convention.

Zero potential energy does not imply absence of interaction.

Therefore:

`E = 0 ≠ no physics`

and:

`E = 0 ≠ active neutral`

---

## 67. Energy Reference Shift

Adding a constant to total potential energy may leave forces unchanged:

`E'(X) = E(X) + C`

implies:

`∇E' = ∇E`

for constant:

`C`

Therefore absolute energy reference and force field contain different information.

---

## 68. Relative Energy Boundary

Many applications depend on energy differences.

A model may reproduce energy differences while using a different arbitrary zero.

Comparison contracts must specify whether absolute or relative energy is evaluated.

---

## 69. Force-Only Validation Boundary

Good force agreement does not automatically establish correct absolute energy.

Therefore:

`force agreement ≠ complete energy agreement`

---

## 70. Energy-Only Validation Boundary

Good energy agreement does not automatically establish accurate gradients everywhere.

Therefore:

`energy agreement ≠ force validation`

Energy and force validation are related but distinct.

---

## 71. Stress Validation Boundary

Energy and force agreement do not automatically establish stress accuracy.

Stress requires its own declared derivative/convention validation.

---

## 72. Training Objective Boundary

Machine-learning potentials may train against combinations of:

- energy;
- forces;
- stress;
- virial;
- other targets.

Training weights alter the optimization problem.

They must not be inferred from architecture name.

---

## 73. Optimization Boundary

An interatomic model architecture and the optimizer used to fit it are different objects.

Therefore:

`potential architecture ≠ optimization algorithm`

---

## 74. Regularization Boundary

Regularization affects fitting and generalization.

It is not the physical interaction law itself.

---

## 75. Descriptor Hyperparameters

Descriptor settings such as:

- cutoff;
- radial basis;
- angular resolution;
- smoothing;
- representation degree

are result-affecting model parameters.

They require reproducibility control.

---

## 76. Cutoff Smoothness

A hard discontinuous cutoff may introduce force discontinuities.

Many potential architectures use smooth cutoff functions.

The exact smoothness requirement depends on the model.

---

## 77. Differentiability Boundary

If forces are obtained through an energy gradient, the relevant energy mapping must possess the required differentiability.

A nondifferentiable descriptor or cutoff may violate smooth-force assumptions.

---

## 78. Descriptor Invariance

An invariant atomic descriptor should remain unchanged under the spatial symmetries it is designed to quotient.

The exact symmetry group must be declared.

---

## 79. Descriptor Equivariance

An equivariant descriptor changes predictably under the declared group action.

Invariant and equivariant descriptors are different constructions.

---

## 80. Descriptor Uniqueness Boundary

Perfect invariance is not sufficient if distinct environments collapse to the same representation in a physically relevant domain.

Representation faithfulness remains a separate criterion.

---

## 81. Descriptor Smoothness

Small geometric perturbations should produce appropriately controlled descriptor changes when differentiable force modeling is required.

Smoothness is distinct from invariance.

---

## 82. Training-Domain Boundary

Model validation must distinguish:

- interpolation inside represented training domain;
- extrapolation outside represented training domain.

A low training error does not establish safe extrapolation.

---

## 83. Uncertainty Boundary

A model uncertainty estimate is separate from model error.

Therefore:

`estimated uncertainty ≠ observed error`

The relationship requires calibration.

---

## 84. Out-of-Domain Boundary

An out-of-domain condition is validation/model metadata.

It is not a balanced ternary state.

Therefore:

`outside domain ≠ ternary -1`

unless an explicit target mapping exists.

---

## 85. Transferability

Transferability describes performance across configurations beyond the immediate fitting examples.

It must be demonstrated.

It is not guaranteed by model architecture name.

---

## 86. Data Efficiency

Data efficiency is dataset- and model-dependent.

Results from one published architecture cannot be inherited by TR-EIP.

---

## 87. Model Capacity

Greater representation capacity may reduce approximation bias but can increase data and optimization requirements.

Capacity alone does not establish accuracy.

---

## 88. Systematic Improvability

Some model families define systematic routes for increasing representation complexity.

Such a property belongs to the specific mathematical construction.

It must not be generalized automatically to every ML potential.

---

## 89. Overfitting Boundary

Excellent training performance with poor independent validation indicates insufficient generalization.

Therefore:

`training accuracy ≠ validation accuracy`

---

## 90. Split Isolation

Training, validation, and test data must remain isolated according to the declared split contract.

Related structures from the same trajectory or parent configuration may require grouped isolation.

---

## 91. Reference Leakage

A validation structure used directly or indirectly during fitting is not fully independent validation evidence.

Data lineage must be considered.

---

## 92. Model Comparison Boundary

Cross-model comparison requires common:

- configuration;
- species;
- state;
- observable;
- units;
- normalization;
- reference convention.

Different benchmark conditions invalidate direct comparison.

---

## 93. Published Benchmark Boundary

Published errors for Behler-Parrinello, GAP, SNAP, MTP, GDML, or another potential belong to their:

- datasets;
- train/test split;
- reference method;
- units;
- error metric;
- hyperparameters.

They must not be copied as TR-EIP benchmark expectations.

---

## 94. Source Classification Matrix

| Source identifier | Repository role |
| --- | --- |
| `DAW-BASKES-1983-EAM-INTRODUCTION` | early EAM source |
| `DAW-BASKES-1984-EAM` | foundational EAM formulation |
| `FINNIS-SINCLAIR-1984` | many-body transition-metal potential |
| `STILLINGER-WEBER-1985` | explicit two-/three-body covalent potential |
| `TERSOFF-1988-BOND-ORDER` | environment-dependent bond-order potential |
| `BEHLER-PARRINELLO-2007` | neural-network potential-energy surface |
| `BARTOK-ET-AL-2010-GAP` | Gaussian approximation potential |
| `BARTOK-KONDOR-CSANYI-2013-SOAP` | atomic-environment representation |
| `THOMPSON-ET-AL-2015-SNAP` | spectral neighbor analysis potential |
| `SHAPEEV-2016-MTP` | moment tensor potential |
| `CHMIELA-ET-AL-2017-GDML` | conservative ML molecular force field |

---

## 95. Source Use Rule

Each source must be used only for the specific architecture, method, or principle it supports.

For example:

`BARTOK-KONDOR-CSANYI-2013-SOAP`

supports atomic-environment representation.

It does not directly establish TR-EIF active-neutral routing.

---

## 96. Historical Lineage

A simplified historical development relevant to TR-EIF interatomic modeling is:

`empirical pair/many-body models`

`→ environment-dependent analytic models`

`→ atom-centered learned energy models`

`→ symmetry-adapted descriptors`

`→ systematically improvable ML potentials`

`→ equivariant interatomic models`

This is a conceptual lineage.

It is not a strict replacement sequence.

---

## 97. Classical Potentials Remain Valid Locally

Newer machine-learning architectures do not make classical potentials mathematically meaningless.

A classical potential may remain highly effective inside its validated domain.

Therefore:

`newer model ≠ automatic universal replacement`

---

## 98. Model Hierarchy Principle

Different interatomic models occupy different approximation classes.

Their validity depends on:

- domain;
- required accuracy;
- computational cost;
- available data;
- physical interactions.

No single potential form is universally optimal.

---

## 99. TR-EIP Evolution Boundary

TR-EIP is not presented as eliminating established interatomic-potential theory.

It extends the modeling apparatus by combining established conservative and equivariant principles with TR-EIF-specific continuous resonance and balanced-ternary execution layers.

---

## 100. Energy-Conservation Correspondence

The established relation:

`F = -∇E`

provides the conservative force foundation used by TR-EIF.

TR-EIF retains this relation while adding conditioning channels.

Those conditioning channels must remain part of the same scalar energy pathway for conservative force consistency.

---

## 101. Conditioning and Conservativity

A conditioned energy:

`E(X, c)`

may remain a conservative spatial potential for fixed conditioning state:

`c`

when force is derived as:

`F = -∂E/∂X`

under the declared state-freezing convention.

If conditioning itself depends on geometry during differentiation, the full derivative contract must state that dependence explicitly.

---

## 102. Retained-State Force Boundary

The current reference differentiation holds retained ternary state fixed during a local force derivative.

Therefore the derivative corresponds to the selected retained execution state.

A ternary transition during the derivative would define a different model operation.

---

## 103. Resonance-State Force Boundary

The current reference path similarly does not silently evolve resonance state inside one local derivative.

A fully coupled geometry-dependent resonance derivative would require a separately declared derivative contract.

---

## 104. Model Discontinuity Boundary

A discrete conditioning-state change can change the energy function used by subsequent execution.

The model must not pretend that a discrete state transition is an infinitesimal spatial derivative.

Therefore:

`ternary transition ≠ coordinate perturbation`

---

## 105. State Transition and Energy Surface

Different retained ternary states may define different conditioned energy pathways.

The transition between them belongs to the execution architecture.

The energy on each retained state remains evaluated under that state's model conditions.

---

## 106. Active Neutral Energy Surface

Active neutral `0` may correspond to a distinct conditioned energy surface or feature scaling.

It is not the absence of an energy model.

---

## 107. Resonance-Conditioned Energy Surface

Continuous resonance descriptors may alter scalar energy channels continuously.

This pathway is distinct from discrete ternary conditioning.

Therefore:

`continuous resonance conditioning ≠ ternary switching`

---

## 108. Independent Conditioning Paths

A valid TR-EIP realization may contain independent information pathways:

`geometry`

`resonance`

`ternary execution`

which jointly influence energy.

Validation must test that these pathways are not accidentally collapsed.

---

## 109. Conservative Output Boundary

If force and stress are derived from the same scalar conditioned energy under fixed declared state, the outputs are structurally tied to that scalar model.

This does not by itself prove physical accuracy.

---

## 110. Empirical Accuracy Boundary

A mathematically conservative energy model can still be empirically wrong.

Therefore:

`conservative ≠ accurate`

and:

`equivariant ≠ accurate`

Physical validation remains independent.

---

## 111. Material Transmutation Boundary

The interatomic-potential literature in this register does not itself establish controlled material transmutation.

Any transmutation claim requires:

- explicit physical mechanism;
- state variables;
- dynamical pathway;
- conservation analysis;
- experimental or first-principles evidence.

Therefore:

`interatomic potential ≠ proof of transmutation`

---

## 112. Structural Transition Boundary

An interatomic model may represent changing atomic structures.

A structural transition is not automatically:

- a ternary transition;
- resonance;
- physical phase transition.

These concepts remain separate until explicitly mapped.

---

## 113. Chemical Reaction Boundary

A potential capable of bond rearrangement may model reactive structural changes.

That does not mean every graph-edge change is a chemical reaction.

Chemical interpretation requires the physical model.

---

## 114. Physical Phase Transition Boundary

A potential-energy landscape contributes to phase behavior.

A physical phase transition requires thermodynamic and statistical evidence beyond one local energy change.

Therefore:

`energy change ≠ physical phase transition`

---

## 115. Potential Validation Layers

Interatomic-potential validation may include:

- energy validation;
- force validation;
- stress validation;
- structural validation;
- equation-of-state validation;
- defect validation;
- phase validation;
- dynamical validation;
- transport validation.

Passing one layer does not automatically close the others.

---

## 116. Energy Validation

Energy validation must specify:

- configurations;
- reference method;
- energy convention;
- normalization;
- metric;
- domain.

---

## 117. Force Validation

Force validation must specify:

- reference forces;
- coordinate convention;
- units;
- metric;
- per-component or vector treatment.

---

## 118. Stress Validation

Stress validation must specify:

- tensor convention;
- sign;
- unit;
- cell convention;
- comparison metric.

---

## 119. Structural Validation

Structural validation may involve:

- radial distribution;
- pair distribution;
- structure factor;
- coordination;
- angular distributions.

These observables remain distinct.

---

## 120. Dynamical Validation

Dynamical validation may examine:

- trajectory stability;
- diffusion;
- vibrational behavior;
- energy conservation;
- phase-space sampling.

A static energy benchmark does not establish dynamical validity.

---

## 121. Transport Validation

Transport properties require sufficient trajectory sampling and statistical analysis.

A short test trajectory is not automatically a transport validation dataset.

---

## 122. Error Metric Boundary

Common error metrics include:

- MAE;
- RMSE;
- maximum error.

Different metrics emphasize different error structures.

They must not be interchanged without declaration.

---

## 123. Normalization Boundary

Energy error may be reported:

- per atom;
- per configuration;
- per formula unit;
- absolute total.

These metrics are not numerically interchangeable.

---

## 124. Force Aggregation Boundary

Force error may be aggregated:

- per Cartesian component;
- per atom vector;
- over all atoms;
- by species.

The comparison method must remain explicit.

---

## 125. Training Loss Boundary

A weighted training loss may combine energy, force, and stress terms.

The loss value is optimization state.

It is not itself a physical observable.

---

## 126. Potential Provenance

A concrete potential should retain provenance for:

- architecture;
- parameters;
- training data;
- reference method;
- version;
- units;
- domain.

A parameter file detached from this context is insufficient scientific identity.

---

## 127. Parameter Artifact Identity

Two parameter artifacts for the same architecture define different concrete models unless their parameter values are identical under the declared artifact identity relation.

---

## 128. Architecture Identity

Two models with identical parameters but different architecture definitions are not the same concrete model.

Therefore model identity requires both:

`architecture`

and:

`parameters`

---

## 129. Reproducibility

Potential reproduction requires:

- source revision;
- architecture;
- parameter artifact;
- configuration;
- graph rules;
- feature construction;
- numerical semantics.

Hidden preprocessing invalidates strict reproducibility.

---

## 130. Version Boundary

Repository version, model-family version, parameter-artifact version, and dataset version remain separate identifiers.

They must not be conflated.

---

## 131. Source-to-TR-EIF Mapping

The registered source roles are:

### Daw-Baskes

many-body embedded-environment energy modeling.

### Finnis-Sinclair

compact many-body transition-metal potential.

### Stillinger-Weber

explicit angular three-body modeling.

### Tersoff

environment-dependent bond-order modeling.

### Behler-Parrinello

atom-centered neural potential-energy surfaces.

### GAP

nonparametric machine-learning interatomic potentials.

### SOAP

symmetry-adapted atomic-environment representation.

### SNAP

spectral/bispectrum local-environment potential.

### MTP

systematically improvable invariant moment representation.

### GDML

energy-conserving learned force-field construction.

---

## 132. TR-EIF-Specific Additions

TR-EIF adds structures not defined by these source models:

- continuous resonance state;
- resonance descriptors;
- continuous-to-ternary target generation;
- active-neutral ternary execution;
- pending-target routing;
- resonance-conditioned features;
- ternary-conditioned features;
- TR-EIP model-family contract;
- explicit multiscale integration.

---

## 133. No Source Overclaim

No source in this register is cited as direct evidence for TR-EIF-specific constructs unless that construct genuinely appears in the source.

Source correspondence must remain exact.

---

## 134. Source Provenance vs Architecture Validation

Literature provenance answers:

`Where does this general method or principle come from?`

Executable validation answers:

`Does the TR-EIF implementation satisfy its own contract?`

These questions are distinct.

---

## 135. Citation Audit

Before release, this register must be audited for:

- author names;
- titles;
- year;
- journal;
- volume;
- pages or article number;
- DOI;
- source role;
- claim correspondence.

---

## 136. Errata Boundary

Where a source has a published correction or erratum relevant to a used claim, the correction must be considered.

A source must not be treated as frozen independently from material corrections.

---

## 137. DOI Boundary

DOI identity confirms the publication.

It does not establish that the publication supports every repository claim.

Claim-to-source audit remains necessary.

---

## 138. Review Boundary

A future review article may be added for synthesis.

It must not replace attribution to foundational primary sources for original methods.

---

## 139. Model Comparison Rule

Two interatomic potentials may be compared only under a common declared domain.

Required compatibility may include:

- species;
- configuration;
- units;
- physical state;
- energy zero convention;
- reference method;
- observable;
- normalization.

---

## 140. Cross-Model Comparison Rule

A Phase 11 cross-model benchmark must not compare unrelated model outputs simply because they have the same numeric type.

Semantic compatibility is required.

---

## 141. Reference Potential Boundary

A model used as a reference in a benchmark remains another model unless its evidence class is explicitly first-principles or experimental.

Therefore:

`reference potential ≠ ground truth automatically`

---

## 142. First-Principles Boundary

First-principles electronic-structure data provide a higher-level reference under a declared computational method.

They are not mathematically exact physical truth.

Their method and convergence settings remain part of provenance.

---

## 143. Experimental Boundary

Experimental data provide independent physical evidence under measurement conditions.

They are not model outputs.

Therefore:

`experiment ≠ first-principles`

and:

`experiment ≠ interatomic potential`

---

## 144. Core Source Invariants

This register preserves:

1. Interatomic potential and molecular dynamics remain distinct.
2. Energy and force remain distinct.
3. Force and stress remain distinct.
4. Conservative force uses the negative energy gradient.
5. Atomic energy decomposition is model-dependent.
6. Pairwise and many-body models remain distinct.
7. Local neighborhoods are model constructs.
8. Graph edges are not automatically chemical bonds.
9. EAM and Finnis-Sinclair are not automatically identical.
10. Stillinger-Weber and Tersoff are distinct many-body formulations.
11. SOAP is a representation, not a potential by itself.
12. GAP and SOAP remain distinct concepts.
13. SNAP and MTP remain distinct model families.
14. Neural-network architecture does not guarantee physical accuracy.
15. First-principles training data remain computational evidence.
16. Training accuracy is not validation accuracy.
17. Energy agreement is not force validation.
18. Force agreement is not stress validation.
19. Conservative structure is not physical accuracy.
20. Equivariance is not physical accuracy.
21. Locality is not physical completeness.
22. Published accuracy is not inherited by TR-EIP.
23. Published runtime is not inherited by TR-EIP.
24. Published transferability is not inherited by TR-EIP.
25. Resonance conditioning remains separate from interatomic-potential lineage.
26. Ternary conditioning remains separate from interatomic-potential lineage.
27. Active neutral `0` is not zero energy.
28. Active neutral `0` is not missing model state.
29. TR-EIP remains a distinct model family.
30. Similarity is not identity.

---

## 145. Related Documentation

This register supports:

`docs/volume_03_equivariant_interatomic_framework/`

`docs/volume_04_learning_and_optimization/`

`docs/volume_05_molecular_dynamics/`

`docs/architecture/energy_model_contract.md`

`docs/specifications/energy_output_specification.md`

`docs/validation/scientific_validation_plan.md`

`docs/validation/numerical_validation_plan.md`

and:

`docs/references/equivariant_model_sources.md`

---

## 146. Non-Claims

This register does not assert that:

- TR-EIP is EAM;
- TR-EIP is Finnis-Sinclair;
- TR-EIP is Stillinger-Weber;
- TR-EIP is Tersoff;
- TR-EIP is a Behler-Parrinello potential;
- TR-EIP is GAP;
- TR-EIP is SNAP;
- TR-EIP is MTP;
- TR-EIP is GDML;
- any registered potential validates FLiBe;
- published accuracy transfers automatically to TR-EIP;
- conservative architecture alone establishes physical truth.

Each such claim would require separate evidence.

---

## 147. Summary

Interatomic-potential theory provides the established energy-model foundation on which the TR-EIP conservative layer can be constructed and evaluated.

The relevant development lineage includes:

`many-body empirical potentials`

`→ environment-dependent analytic potentials`

`→ atom-centered neural energy models`

`→ symmetry-adapted environment descriptors`

`→ Gaussian and spectral ML potentials`

`→ systematically improvable invariant potentials`

`→ conservative learned force fields`

while TR-EIF adds its own distinct architecture:

`E(3)-structured geometry`

`+ continuous resonance conditioning`

`+ retained -1/0/1 conditioning`

`+ active-neutral execution`

`→ conservative scalar energy`

`→ force and stress`

The controlling rules remain:

`potential architecture ≠ physical validation`

`shared principle ≠ model identity`

and:

`similar ≠ identical`
