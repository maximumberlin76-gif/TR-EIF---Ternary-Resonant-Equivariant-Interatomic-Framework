# Equivariant Model Sources

## 1. Scope

This document defines the source register for geometric equivariance, E(3)/SE(3) representation methods, equivariant message passing, and equivariant atomistic model architectures used as mathematical and architectural references by the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The register covers sources relevant to:

- Euclidean symmetry;
- rotation and translation equivariance;
- reflection and parity treatment;
- scalar, vector, and higher-order representations;
- spherical harmonics;
- tensor products;
- Clebsch-Gordan coupling;
- equivariant message passing;
- invariant scalar outputs;
- equivariant vector outputs;
- atomistic graph representations;
- equivariant interatomic potentials;
- higher-order equivariant interactions;
- local equivariant representations;
- energy-conserving force construction.

This register does not define the complete TR-EIF architecture.

It does not define balanced-ternary execution.

It does not define active-neutral state `0`.

It does not define TR-EIF resonance dynamics.

It does not define FLiBe-specific parameters.

---

## 2. Architectural Source Boundary

TR-EIF combines several distinct mathematical structures.

Equivariant-model literature provides established methods for spatial symmetry handling.

The architectural relation is:

`geometric equivariance literature`

`→ TR-EIF E(3)-equivariant interatomic layer`

not:

`equivariant model literature = TR-EIF`

Therefore:

`equivariant neural network ≠ TR-EIF`

and:

`equivariant interatomic potential ≠ TR-EIP`

unless the model is explicitly the TR-EIP realization.

---

## 3. TR-EIP Nesting

The model-family relation remains:

`TR-EIP ⊂ TR-EIF`

TR-EIP uses E(3)-compatible spatial representations inside the larger TR-EIF framework.

TR-EIF additionally contains:

- continuous resonance dynamics;
- balanced ternary execution;
- active neutral state `0`;
- routing;
- molecular dynamics;
- multiscale mappings;
- FLiBe specialization;
- validation architecture.

No source in this register defines that complete synthesis.

---

## 4. E(3) Boundary

The Euclidean group in three dimensions includes:

- translations;
- proper rotations;
- improper rotations including reflections.

The rotational/reflection part is represented by:

`O(3)`

while proper rotations alone form:

`SO(3)`

and proper roto-translations form:

`SE(3)`.

Therefore:

`SE(3) ≠ E(3)`

because SE(3) does not include reflection parity.

---

## 5. Equivariance Definition

For a group:

`G`

acting on input and output spaces through representations:

`D_X(g)`

and:

`D_Y(g)`

a mapping:

`F`

is equivariant when:

`F(D_X(g)x) = D_Y(g)F(x)`

for all admissible:

`g ∈ G`

and:

`x ∈ X`

under the declared representation.

---

## 6. Invariance Definition

A mapping is invariant when the output representation is trivial:

`F(D_X(g)x) = F(x)`

for every admissible group action.

Therefore:

`invariance ≠ equivariance`

Invariance is a special transformation behavior.

---

## 7. Scalar and Vector Boundary

A scalar invariant output does not transform like a spatial vector.

A polar vector transforms under the applicable spatial linear transformation.

Therefore:

`scalar representation ≠ vector representation`

and:

`scalar invariance ≠ vector equivariance`

---

## 8. Higher-Order Representation Boundary

Higher-order irreducible representations may encode richer angular structure than scalar and vector channels.

Formal higher-order capability in the literature does not imply that every TR-EIF executable realization currently implements every representation order.

Therefore:

`formal higher-order theory ≠ current executable higher-order support`

---

## 9. Translation Boundary

For atomistic systems, translation invariance is commonly obtained through relative geometry such as:

`r_ij = r_j - r_i`

Absolute Cartesian position and relative displacement are distinct objects.

A model using only relative geometry may be translation invariant while retaining rotationally equivariant internal features.

---

## 10. Reflection Boundary

A model described as:

`SE(3)-equivariant`

must not automatically be described as full:

`E(3)-equivariant`

without explicit treatment of reflections or parity.

This distinction is mandatory in TR-EIF source use.

---

## 11. Permutation Boundary

Permutation symmetry of equivalent atomic indexing is distinct from E(3) spatial symmetry.

Therefore:

`permutation symmetry ≠ E(3) symmetry`

A model may enforce both.

They remain mathematically different group actions.

---

## 12. Tensor Product Boundary

Tensor-product operations combine representations according to group-theoretic coupling rules.

A tensor product in equivariant networks is not equivalent to arbitrary numerical multiplication of feature arrays.

Representation type and admissible coupling remain part of the operation.

---

## 13. Spherical Harmonics Boundary

Spherical harmonics provide angular basis functions transforming under rotations.

They are mathematical representation tools.

They are not:

- resonance phases;
- physical phase-of-matter labels;
- ternary states.

Therefore:

`spherical harmonic phase ≠ TR-EIF oscillator phase`

and:

`spherical harmonic index ≠ ternary state`

---

## 14. Clebsch-Gordan Boundary

Clebsch-Gordan coefficients determine admissible coupling between angular-momentum representation channels.

They do not define:

- chemical bond strength;
- ternary routing;
- active neutral;
- resonance state.

---

## 15. THOMAS-ET-AL-2018-TENSOR-FIELD-NETWORKS

Nathaniel Thomas.

Tess Smidt.

Steven Kearnes.

Lusann Yang.

Li Li.

Kai Kohlhoff.

Patrick Riley.

"Tensor Field Networks: Rotation- and Translation-Equivariant Neural Networks for 3D Point Clouds."

2018.

arXiv:

`1802.08219`

Source class:

foundational primary architecture source.

Repository role:

reference for continuous 3D rotation/translation equivariance using tensor-valued features and spherical-harmonic filters.

Relevant evidence domain:

- rotation equivariance;
- translation equivariance;
- permutation handling;
- scalar features;
- vector features;
- higher-order tensor features;
- spherical-harmonic filters.

---

## 16. Tensor Field Network Source Role

The Tensor Field Networks work establishes an important architecture for layerwise geometric equivariance.

TR-EIF uses this literature as conceptual and mathematical background for equivariant representations.

It does not import Tensor Field Networks as the TR-EIP architecture.

Therefore:

`Tensor Field Network ≠ TR-EIP`

---

## 17. TFN Representation Boundary

Tensor Field Networks support scalar, vector, and higher-order tensor representations.

The current TR-EIF executable reference uses a narrower representation subset in its principal reference path.

Therefore:

`TFN representational capacity ≠ current TR-EIF executable feature set`

---

## 18. ANDERSON-HY-KONDOR-2019-CORMORANT

Brandon Anderson.

Truong Son Hy.

Risi Kondor.

"Cormorant: Covariant Molecular Neural Networks."

Advances in Neural Information Processing Systems.

Volume 32.

Pages 14537-14546.

2019.

Source class:

primary molecular equivariant-model source.

Repository role:

reference for rotation-covariant molecular representations using tensor products and Clebsch-Gordan decomposition.

Relevant evidence domain:

- rotational covariance;
- molecular neural networks;
- tensor-product nonlinear structure;
- Clebsch-Gordan representation coupling;
- molecular potential-energy learning.

---

## 19. Cormorant Boundary

Cormorant demonstrates a covariant molecular architecture.

Its architecture is not identical to:

- Tensor Field Networks;
- PaiNN;
- NequIP;
- MACE;
- Allegro;
- TR-EIP.

Therefore:

`common equivariance principle ≠ architecture identity`

---

## 20. FUCHS-ET-AL-2020-SE3-TRANSFORMER

Fabian B. Fuchs.

Daniel E. Worrall.

Volker Fischer.

Max Welling.

"SE(3)-Transformers: 3D Roto-Translation Equivariant Attention Networks."

Advances in Neural Information Processing Systems.

Volume 33.

2020.

Source class:

primary equivariant-attention architecture source.

Repository role:

reference for self-attention constrained by continuous 3D roto-translation equivariance.

Relevant evidence domain:

- SE(3) equivariance;
- attention;
- 3D point clouds;
- graph-local operations;
- equivariant value representations;
- invariant attention weights.

---

## 21. SE(3)-Transformer Boundary

The SE(3)-Transformer guarantees equivariance under proper three-dimensional roto-translations under its declared architecture.

Its source role does not automatically establish reflection equivariance.

Therefore:

`SE(3)-Transformer evidence ≠ automatic E(3) reflection evidence`

---

## 22. Attention Boundary

Attention is one mechanism for information aggregation.

TR-EIP does not become an attention model merely because attention-based equivariant architectures exist.

Therefore:

`equivariance ≠ attention`

and:

`message passing ≠ attention`

---

## 23. SCHUTT-UNKE-GASTEGGER-2021-PAINN

Kristof T. Schütt.

Oliver T. Unke.

Michael Gastegger.

"Equivariant Message Passing for the Prediction of Tensorial Properties and Molecular Spectra."

Proceedings of the 38th International Conference on Machine Learning.

Proceedings of Machine Learning Research.

Volume 139.

Pages 9377-9388.

2021.

Source class:

primary equivariant molecular-message-passing source.

Repository role:

reference for rotationally equivariant message passing using coupled scalar and vector atomic representations.

Relevant evidence domain:

- rotational equivariance;
- molecular graph message passing;
- scalar features;
- vector features;
- tensorial-property prediction;
- molecular spectra.

---

## 24. PaiNN Representation Boundary

PaiNN explicitly demonstrates that atomwise equivariant vector representations can carry directional information that invariant-only representations discard.

This supports the broader architectural principle that:

`invariant scalar representation ≠ complete directional representation`

It does not establish that every interatomic model requires the PaiNN architecture.

---

## 25. Scalar-Vector Interaction Boundary

A model may combine scalar and vector channels while preserving rotational transformation rules.

Scalar/vector interaction is distinct from:

- resonance conditioning;
- ternary conditioning.

Therefore:

`scalar-vector equivariant interaction ≠ resonance conditioning`

and:

`scalar-vector equivariant interaction ≠ ternary routing`

---

## 26. BATZNER-ET-AL-2022-NEQUIP

Simon Batzner.

Albert Musaelian.

Lixin Sun.

Mario Geiger.

Jonathan P. Mailoa.

Mordechai Kornbluth.

Nicola Molinari.

Tess E. Smidt.

Boris Kozinsky.

"E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials."

Nature Communications.

Volume 13.

Article 2453.

2022.

DOI:

`10.1038/s41467-022-29939-5`

Source class:

primary E(3)-equivariant interatomic-potential source.

Repository role:

reference for E(3)-equivariant graph neural networks applied directly to interatomic potential learning.

Relevant evidence domain:

- E(3) equivariance;
- graph neural networks;
- geometric tensor representations;
- interatomic potential learning;
- energy prediction;
- force prediction;
- molecular dynamics;
- data efficiency.

---

## 27. NequIP E(3) Source Role

NequIP is an explicit source for the use of E(3)-equivariant convolutions in interatomic-potential modeling.

This makes it directly relevant to TR-EIP's spatial-symmetry layer.

It does not define the TR-EIF continuous resonance layer or balanced ternary execution.

---

## 28. NequIP Energy Boundary

NequIP belongs to the family of learned interatomic energy models.

TR-EIP may share principles such as:

- local atomic environments;
- E(3) representations;
- invariant scalar energy;
- energy-derived forces.

Shared principles do not imply model identity.

---

## 29. GEIGER-SMIDT-2022-E3NN

Mario Geiger.

Tess Smidt.

"e3nn: Euclidean Neural Networks."

2022.

arXiv:

`2207.09453`

Source class:

equivariant-framework and methodological reference.

Repository role:

reference for composable E(3)-equivariant operations including:

- spherical harmonics;
- tensor products;
- irreducible representations;
- parity-aware Euclidean representations.

---

## 30. e3nn Boundary

e3nn is a general software/mathematical framework for constructing Euclidean-equivariant neural networks.

It is not one specific interatomic potential.

Therefore:

`e3nn ≠ NequIP`

`e3nn ≠ MACE`

`e3nn ≠ Allegro`

`e3nn ≠ TR-EIP`

Models may use related representation machinery while retaining distinct architectures.

---

## 31. BATATIA-ET-AL-2022-MACE

Ilyes Batatia.

Dávid Péter Kovács.

Gregor N. C. Simm.

Christoph Ortner.

Gábor Csányi.

"MACE: Higher Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields."

Advances in Neural Information Processing Systems.

Volume 35.

Pages 11423-11436.

2022.

DOI:

`10.52202/068431-0830`

Source class:

primary higher-order equivariant interatomic-model source.

Repository role:

reference for higher-body-order equivariant message passing in machine-learned force fields.

Relevant evidence domain:

- equivariant message passing;
- higher-body-order messages;
- interatomic force fields;
- atomic cluster expansion connections;
- reduced message-passing depth;
- energy and force modeling.

---

## 32. MACE Higher-Order Boundary

MACE demonstrates one method of increasing body-order expressivity inside an equivariant message-passing architecture.

Higher body order does not mean:

- higher spatial dimension;
- more ternary states;
- more resonance states.

Therefore:

`body order ≠ ternary-state cardinality`

---

## 33. MACE and TR-EIP Boundary

TR-EIP may draw on the general equivariant-model literature.

It is not an implementation of MACE.

Therefore:

`MACE ≠ TR-EIP`

Any future correspondence must identify the exact shared operator or representation.

---

## 34. MUSAELIAN-ET-AL-2023-ALLEGRO

Albert Musaelian.

Simon Batzner.

Anders Johansson.

Lixin Sun.

Cameron J. Owen.

Mordechai Kornbluth.

Boris Kozinsky.

"Learning local equivariant representations for large-scale atomistic dynamics."

Nature Communications.

Volume 14.

Article 579.

2023.

DOI:

`10.1038/s41467-023-36329-y`

Source class:

primary local equivariant interatomic-model source.

Repository role:

reference for strictly local equivariant deep-learning interatomic potentials and scalable atomistic dynamics.

Relevant evidence domain:

- local equivariant representations;
- E(3) symmetry;
- tensor products;
- energy decomposition;
- energy-conserving force derivation;
- atomistic simulations;
- large-system scaling.

---

## 35. Allegro Locality Boundary

Allegro is designed around strict locality rather than atom-centered iterative message passing over expanding receptive fields.

Therefore:

`local equivariant architecture ≠ message-passing architecture`

even though both may use common equivariant tensor-product machinery.

---

## 36. Allegro Force Relation

Allegro explicitly uses forces derived as the negative gradient of total energy.

This provides a relevant literature correspondence for the conservative relation:

`F_i = -∇_i E_total`

TR-EIF's own force implementation remains governed by its committed energy and differentiation contracts.

---

## 37. Conservative-Force Source Boundary

A source showing energy-derived forces supports the conservative modeling principle.

It does not establish that a different implementation is correct.

TR-EIF force correctness requires its own executable validation.

Therefore:

`literature precedent ≠ implementation qualification`

---

## 38. Model-Family Comparison

The registered architectures illustrate distinct approaches:

### Tensor Field Networks

layerwise tensor-field equivariance.

### Cormorant

rotationally covariant molecular networks with Clebsch-Gordan tensor coupling.

### SE(3)-Transformer

roto-translation equivariant self-attention.

### PaiNN

scalar/vector rotationally equivariant molecular message passing.

### NequIP

E(3)-equivariant graph neural interatomic potential.

### MACE

higher-order equivariant message passing.

### Allegro

strictly local equivariant interatomic architecture.

### e3nn

general Euclidean-equivariant representation toolkit.

These models share mathematical concepts without being interchangeable.

---

## 39. Architecture Identity Rule

The following inference is invalid:

`both models are equivariant → same architecture`

Equivariance constrains transformation behavior.

It does not uniquely determine:

- graph structure;
- message function;
- body order;
- locality;
- attention;
- feature hierarchy;
- energy decomposition;
- training objective.

---

## 40. Representation Identity Rule

Two models may both use irreducible representations of O(3) while choosing different:

- representation multiplicities;
- maximum angular order;
- parity channels;
- tensor-product paths;
- nonlinearities.

Therefore:

`same group ≠ same representation architecture`

---

## 41. E(3) and O(3) Representation Boundary

In atomistic modeling, rotation and reflection behavior is commonly represented through O(3) irreducible representations while translation invariance/equivariance is handled through relative geometry.

This representation strategy may realize E(3)-compatible behavior.

The exact transformation contract must remain explicit.

---

## 42. Translation Handling

A model using interatomic displacement vectors:

`r_ij = r_j - r_i`

removes common translation from local relative geometry.

This is distinct from rotational representation handling.

Therefore:

`translation handling ≠ rotation handling`

---

## 43. Parity

Reflection-sensitive representation channels carry parity information.

Parity must not be ignored when full E(3) behavior is claimed.

A model validated only under SO(3) rotations does not automatically establish reflection behavior.

---

## 44. Polar and Axial Vector Boundary

Under inversion, polar and axial vectors transform differently.

A generic label:

`vector`

may therefore be insufficient when parity matters.

TR-EIF's executable representation contract must state the supported vector type.

---

## 45. TR-EIF Current Vector Boundary

The current executable TR-EIF reference primarily uses scalar and polar-vector channels.

It must not claim arbitrary axial-vector or higher-order irreducible support without corresponding implementation and tests.

---

## 46. Feature Equivariance Is Not Output Invariance

An internal feature may transform equivariantly while the final scalar energy is invariant.

Therefore:

`equivariant hidden representation ≠ invariant hidden representation`

and:

`equivariant internal layer → invariant scalar output`

is a valid architecture pattern.

---

## 47. Energy Scalar Boundary

Potential energy is represented as a scalar invariant under rigid spatial coordinate transformation for the declared isolated spatial symmetry setting.

Therefore:

`rotation of geometry ≠ rotation of scalar energy`

---

## 48. Force Vector Boundary

Mechanical force is a spatial polar vector.

Under an admissible orthogonal transformation:

`Q`

the force transforms as:

`F' = QF`

under the declared E(3) convention.

The force does not remain componentwise numerically identical after a nontrivial rotation.

---

## 49. Equivariance Validation Boundary

Valid force-equivariance testing compares:

`force on transformed geometry`

with:

`transformed reference force`

It does not compare the transformed force directly with the untransformed force components.

---

## 50. Reflection Validation Boundary

A full E(3) test includes improper orthogonal transformations when the model claims parity-correct reflection behavior.

Rotation-only validation establishes less.

---

## 51. Atom Permutation

Atom permutation is another symmetry relevant to atomistic modeling.

A consistent permutation must apply to:

- species;
- positions;
- graph indices;
- features;
- outputs.

Permutation validation is distinct from E(3) validation.

---

## 52. Graph Representation Boundary

Equivariant graph models often use atoms as nodes and neighborhood relations as edges.

A graph edge is not automatically a chemical bond.

Therefore:

`graph edge ≠ chemical bond`

This distinction remains mandatory in TR-EIF.

---

## 53. Local Environment Boundary

A cutoff-defined atomic neighborhood is a model construct.

It must not automatically be described as a physically complete coordination shell.

Therefore:

`model neighborhood ≠ experimental coordination shell`

without an explicit validation relation.

---

## 54. Message Passing Boundary

Message passing propagates representation information along declared graph relations.

It is not itself:

- physical force transmission;
- energy flow;
- chemical reaction;
- ternary routing.

Therefore:

`message passing ≠ physical energy flow`

---

## 55. Tensor Product Is Not Physical Interaction by Itself

A tensor-product operation combines mathematical representations.

Its presence does not prove a specific physical many-body interaction.

Physical interpretation requires the model and validation context.

---

## 56. Higher Body Order Boundary

Body-order expressivity describes dependence on multi-atom configurations.

It is distinct from message-passing depth.

Therefore:

`body order ≠ message depth`

although specific architectures may relate them.

---

## 57. Locality Boundary

A strictly local architecture and a multi-layer message-passing architecture may have different effective receptive fields.

Both may remain equivariant.

Equivariance does not determine locality.

---

## 58. Long-Range Interaction Boundary

None of the registered equivariant architectures establishes that every material can be represented adequately by one finite local cutoff.

Long-range electrostatic or other interactions may require explicit modeling.

Therefore:

`equivariance ≠ physical completeness`

---

## 59. Accuracy Boundary

A model's published benchmark accuracy belongs to that model, dataset, training procedure, and evaluation domain.

It must not be copied as expected TR-EIP accuracy.

Therefore:

`NequIP accuracy ≠ TR-EIP accuracy`

`MACE accuracy ≠ TR-EIP accuracy`

`Allegro accuracy ≠ TR-EIP accuracy`

---

## 60. Dataset Boundary

QM9, MD17, rMD17, 3BPA, and other published benchmark datasets are distinct evidence domains.

Performance on one does not imply performance on FLiBe.

Therefore:

`molecular benchmark accuracy ≠ FLiBe validation`

---

## 61. FLiBe Boundary

No source in this register is admitted as direct FLiBe material-property evidence merely because it describes atomistic potentials.

FLiBe evidence remains governed by:

`docs/references/flibe_sources.md`

---

## 62. Training Architecture Boundary

Equivariant-model sources may include particular:

- losses;
- optimizers;
- data splits;
- precision;
- training schedules.

Those choices are model-specific.

They must not be silently imported into TR-EIP.

---

## 63. Learned Model Boundary

Many sources in this register concern learned neural models.

The TR-EIF framework itself is broader than one learning architecture.

Therefore:

`TR-EIF ≠ neural network`

TR-EIF may contain learned or non-learned model realizations.

---

## 64. Reference Implementation Boundary

TR-EIF's current `ReferenceEnergyModel` is an executable reference realization.

It is not claimed to reproduce the full architecture of NequIP, MACE, Allegro, PaiNN, or any other registered model.

---

## 65. Linear Invariant Functional Boundary

The current TR-EIF reference energy functional is deliberately simple.

Its simplicity does not imply that the full TR-EIP model family is limited to linear scalar readout forever.

Executable claims remain bounded to the actual implementation.

---

## 66. Resonance Conditioning Boundary

The registered equivariant architectures do not define the TR-EIF continuous resonance descriptor.

Therefore:

`equivariant feature ≠ resonance feature`

TR-EIF resonance conditioning is an additional explicitly typed channel.

---

## 67. Ternary Conditioning Boundary

The registered equivariant architectures do not define the TR-EIF retained:

`-1/0/1`

conditioning layer.

Therefore:

`equivariant representation ≠ ternary execution`

and:

`equivariant message passing ≠ active-neutral routing`

---

## 68. Active Neutral Boundary

State:

`0`

is active neutral in TR-EIF.

Its semantic roles include:

- balancing;
- routing;
- damping;
- mediation;
- transition staging;
- retention;
- controlled neutralization.

These semantics are not attributed to Tensor Field Networks, PaiNN, NequIP, MACE, Allegro, or other equivariant-model sources.

---

## 69. Continuous/Discrete Composition

TR-EIF combines:

`continuous E(3)-equivariant spatial state`

with:

`continuous resonance state`

and:

`discrete balanced-ternary execution state`

without identifying them.

Therefore:

`spatial representation ≠ resonance state`

`resonance state ≠ ternary state`

`spatial transformation ≠ ternary polarity reversal`

---

## 70. Spatial Rotation Boundary

A spatial rotation acts on geometric representations.

It does not automatically transform:

`-1 ↔ 1`

Therefore:

`spatial rotation ≠ ternary polarity reversal`

---

## 71. Energy/Resonance Boundary

Resonance-conditioned features may influence an energy model.

This does not identify:

`resonance descriptor = energy`

The descriptor is an input channel.

Energy is a scalar model output.

---

## 72. Energy/Ternary Boundary

Retained ternary state may condition an energy pathway.

This does not identify:

`ternary state = energy`

The state is an execution variable.

Energy is a continuous observable.

---

## 73. Equivariant Representation and Physical Units

Representation transformation type does not determine physical units.

A vector feature may be dimensionless or dimensional depending on the model.

Therefore:

`representation type ≠ physical unit`

---

## 74. Feature Meaning Boundary

A learned equivariant feature is not automatically a directly measurable physical observable.

Interpretation requires explicit mapping and validation.

---

## 75. Learned Latent State Boundary

Latent equivariant tensors in a neural model should not be labeled as physical fields unless a physical correspondence is established.

Therefore:

`latent tensor ≠ physical tensor observable`

---

## 76. Energy Decomposition Boundary

Several interatomic architectures use atomic or local energy decomposition.

Such decomposition is a model representation.

An atomic energy term is not automatically an independently measurable atomic observable.

---

## 77. Force Derivation Boundary

If forces are obtained from:

`F = -∇E`

then energy conservation properties depend on using the same differentiable scalar energy model.

Separate independently learned force outputs require their own conservative-consistency validation.

---

## 78. Stress Boundary

Equivariant interatomic-potential literature may support energy and force modeling.

Stress conventions must still be treated explicitly.

A force-valid model is not automatically stress-validated.

---

## 79. Mathematical Representation vs Implementation

A source may establish mathematical equivariance.

A software implementation may still contain an error.

Therefore:

`correct theory ≠ correct implementation`

TR-EIF requires its own executable equivariance tests.

---

## 80. Implementation Validation

TR-EIF validates its E(3)-related executable behavior through committed tests and structured benchmarks.

Literature citation supplies theoretical and architectural provenance.

It does not replace those tests.

---

## 81. Source-to-TR-EIF Mapping

The principal source roles are:

### Tensor Field Networks

foundational tensor-field equivariant architecture.

### Cormorant

rotation-covariant molecular tensor coupling.

### SE(3)-Transformer

equivariant attention under proper roto-translations.

### PaiNN

scalar/vector rotationally equivariant molecular message passing.

### NequIP

E(3)-equivariant graph interatomic potentials.

### e3nn

general Euclidean-equivariant representation machinery.

### MACE

higher-order equivariant message passing for force fields.

### Allegro

strictly local scalable equivariant interatomic potentials.

---

## 82. Source Classification Matrix

| Source identifier | Repository role |
| --- | --- |
| `THOMAS-ET-AL-2018-TENSOR-FIELD-NETWORKS` | foundational equivariant architecture |
| `ANDERSON-HY-KONDOR-2019-CORMORANT` | covariant molecular architecture |
| `FUCHS-ET-AL-2020-SE3-TRANSFORMER` | SE(3)-equivariant attention |
| `SCHUTT-UNKE-GASTEGGER-2021-PAINN` | equivariant molecular message passing |
| `BATZNER-ET-AL-2022-NEQUIP` | E(3)-equivariant interatomic potential |
| `GEIGER-SMIDT-2022-E3NN` | Euclidean-equivariant framework |
| `BATATIA-ET-AL-2022-MACE` | higher-order equivariant force field |
| `MUSAELIAN-ET-AL-2023-ALLEGRO` | local scalable equivariant interatomic potential |

---

## 83. Source-Use Rule

A source is used only for the architecture or mathematical property it actually establishes.

For example:

`FUCHS-ET-AL-2020-SE3-TRANSFORMER`

supports an SE(3)-equivariant attention architecture.

It does not directly support a full E(3) reflection claim for TR-EIP.

---

## 84. Reflection Claim Rule

TR-EIF E(3) reflection claims must be supported by:

- the mathematical representation contract;
- executable reflection tests;
- applicable E(3)/O(3) source foundations.

A source restricted to SE(3) cannot alone establish reflection behavior.

---

## 85. Higher-Order Claim Rule

A source supporting higher-order irreducible features does not establish that the current TR-EIF executable implementation supports them.

The repository must distinguish:

`theoretical source capability`

from:

`implemented capability`

---

## 86. Interatomic Accuracy Claim Rule

Published model accuracy cannot be inherited by TR-EIP.

TR-EIP accuracy claims require direct TR-EIP validation.

Therefore:

`literature architecture accuracy ≠ TR-EIP validation result`

---

## 87. Scaling Claim Rule

Published scaling of Allegro or another architecture belongs to that architecture and implementation.

TR-EIP scaling requires its own benchmark.

---

## 88. Data-Efficiency Claim Rule

Published NequIP data efficiency belongs to NequIP under its published datasets and training conditions.

TR-EIP must not claim the same data efficiency without direct evidence.

---

## 89. Force-Field Speed Claim Rule

Published MACE or Allegro speed belongs to those implementations and environments.

TR-EIP runtime is measured independently.

---

## 90. Architectural Inspiration vs Derivation

TR-EIF may use ideas established across the equivariant-model literature.

A repository artifact should state whether its relation is:

- direct mathematical correspondence;
- architectural inspiration;
- explicit generalization;
- independent TR-EIF construction.

These relations are not interchangeable.

---

## 91. No Global Copy Claim

TR-EIP is not defined as a copy of:

- TFN;
- Cormorant;
- SE(3)-Transformer;
- PaiNN;
- NequIP;
- MACE;
- Allegro.

TR-EIP is a separate model family combining its own declared structures.

---

## 92. Source Independence

Multiple equivariant architectures may share common representation theory and software infrastructure.

Their published results are not necessarily statistically independent evidence for every architectural claim.

Evidence independence must be evaluated claim by claim.

---

## 93. Common e3nn Infrastructure Boundary

Some modern E(3)-equivariant atomistic models use e3nn.

Shared use of e3nn does not make the models identical.

Therefore:

`shared library ≠ shared model architecture`

---

## 94. Software Version Boundary

Published results may depend on specific software versions.

When reproducing an external model result, the source's software/version metadata may be result-affecting.

TR-EIF's own implementation does not inherit those versions unless explicitly used.

---

## 95. Mathematical Source vs Software Source

A software package may implement group-theoretic operations.

The mathematical validity of equivariance derives from the implemented representation relations, not merely from the package name.

---

## 96. Equivariance Test Requirement

An equivariance claim requires direct testing of the implementation.

Current TR-EIF validation includes transformations such as:

- translation;
- rotation;
- reflection

where applicable.

---

## 97. Scalar Test Requirement

For an invariant scalar energy:

`E(g · X)`

must agree with:

`E(X)`

within the fixed numerical criterion.

---

## 98. Vector Test Requirement

For force vector:

`F`

the transformed-system output must agree with the transformed reference vector:

`g · F`

within the fixed numerical criterion.

---

## 99. Graph Cardinality Under Rigid Motion

A distance-cutoff graph should preserve connectivity under exact rigid E(3) transformations when the transformation preserves all pair distances and the cutoff relation remains numerically unchanged.

This provides one structural equivariance invariant.

---

## 100. Resonance Coordinate Under Spatial E(3)

The current base resonance descriptor is not directly a Cartesian representation.

A rigid spatial E(3) transformation should not silently alter its continuous oscillator coordinate when resonance state is held fixed.

This is a TR-EIF architectural validation condition, not a claim inherited directly from the equivariant-model literature.

---

## 101. Ternary State Under Spatial E(3)

A rigid spatial transformation must not automatically alter retained ternary execution state.

Therefore:

`E(3) transformation ≠ ternary transition`

---

## 102. Permutation vs Spatial Transformation

Permutation and spatial transformation may be composed.

Their validation relations remain distinct:

`permutation consistency`

and:

`E(3) consistency`

A single test must not conflate them.

---

## 103. Source Provenance

Sources in this register are literature provenance for mathematical and architectural concepts.

They are not physical-material provenance.

Material-specific evidence belongs to specialized material registers.

---

## 104. Citation Audit Requirements

Before release, each source entry must be checked for:

- author names;
- title;
- publication venue;
- year;
- volume where applicable;
- pages or article number where applicable;
- DOI or stable identifier where applicable;
- evidence role;
- source-to-claim correspondence.

---

## 105. Preprint Boundary

Tensor Field Networks and e3nn are registered here through their stable preprint/project publications where applicable.

Their publication form must not be misrepresented as a journal article if no such source record is being cited.

---

## 106. Conference Source Boundary

NeurIPS and ICML proceedings papers are primary research sources.

They are not journal articles.

Their bibliographic form should remain accurate.

---

## 107. Journal Source Boundary

NequIP and Allegro are registered through their Nature Communications versions of record.

The journal article identity should be preferred over an earlier preprint when citing the final published result.

---

## 108. Review Boundary

This register primarily contains original architecture papers and framework sources.

A later review may be added for synthesis.

It must not replace primary-source attribution for original architectures.

---

## 109. Source Conflict Rule

If later literature disputes an equivariance property or exposes a limitation, the conflict must be recorded rather than removed to preserve a preferred narrative.

---

## 110. Terminology Audit

The repository must use:

`invariant`

`equivariant`

`covariant`

`E(3)`

`SE(3)`

`O(3)`

`SO(3)`

according to their mathematical scope.

These terms must not be treated as stylistic synonyms.

---

## 111. Covariance Terminology

Some literature uses:

`covariant`

where modern machine-learning literature often uses:

`equivariant`

for transformation-compatible feature behavior.

When citing a source, preserve its title and terminology.

When defining TR-EIF semantics, use the repository's declared mathematical terminology.

---

## 112. Symmetry Does Not Imply Conservation

Spatial symmetry and energy conservation are related through physical theory under appropriate assumptions, but a network being equivariant does not by itself prove that its learned force field is conservative.

Therefore:

`equivariance ≠ conservative force`

A conservative-force claim requires an energy-gradient relation.

---

## 113. Equivariance Does Not Imply Accuracy

A perfectly equivariant model may still be quantitatively inaccurate.

Therefore:

`equivariance ≠ predictive accuracy`

Both require separate validation.

---

## 114. Equivariance Does Not Imply Completeness

An equivariant representation may omit physically relevant:

- long-range interactions;
- electronic degrees of freedom;
- charge transfer;
- history;
- thermodynamic state.

Therefore:

`equivariance ≠ physical completeness`

---

## 115. Symmetry Does Not Replace Data

Symmetry constraints can improve model structure and data efficiency.

They do not eliminate the need for appropriate training or parameter evidence in a learned physical model.

---

## 116. TR-EIF Learning Boundary

TR-EIF contains a learning-and-optimization volume.

The existence of equivariant learning literature does not force every TR-EIP realization to be trained through the same learning algorithm.

---

## 117. Source-to-Documentation Mapping

This register supports:

`docs/volume_03_equivariant_interatomic_framework/`

especially:

- E(3) group actions;
- equivariant representations;
- message passing;
- conservative energy;
- forces and stress;
- TR-EIP model family.

---

## 118. Source-to-Architecture Mapping

This register also supports:

`docs/architecture/framework_architecture.md`

`docs/architecture/energy_model_contract.md`

and relevant portions of:

`docs/architecture/continuous_discrete_contract.md`

It does not define the continuous-discrete coupling contract by itself.

---

## 119. Source-to-Validation Mapping

This register supports validation of:

- spatial transformation claims;
- scalar invariance;
- vector equivariance;
- representation terminology;
- architecture comparisons.

Executable validation remains under:

`tests/equivariance/`

and related test suites.

---

## 120. Source-to-Benchmark Boundary

The existence of published equivariant benchmarks does not replace TR-EIF's committed:

`benchmarks/flibe/reference_equivariance.py`

or its qualification tests.

External and internal benchmark evidence remain separate.

---

## 121. Core Source Invariants

This register preserves:

1. E(3) and SE(3) remain distinct.
2. O(3) and SO(3) remain distinct.
3. Invariance and equivariance remain distinct.
4. Scalar and vector representations remain distinct.
5. Higher-order formal support is not automatically executable support.
6. Permutation symmetry remains distinct from spatial symmetry.
7. Tensor products are representation operations, not physical interactions by definition.
8. Spherical harmonics are not resonance phases.
9. Equivariance does not determine architecture identity.
10. Equivariance does not determine locality.
11. Equivariance does not determine body order.
12. Equivariance does not prove conservative force behavior.
13. Equivariance does not prove predictive accuracy.
14. Equivariance does not prove physical completeness.
15. Graph edges are not automatically chemical bonds.
16. Local neighborhoods are not automatically experimental coordination shells.
17. Latent equivariant tensors are not automatically physical observables.
18. Published model accuracy is not inherited by TR-EIP.
19. Published model runtime is not inherited by TR-EIP.
20. Published model scaling is not inherited by TR-EIP.
21. Resonance conditioning remains distinct from equivariant representation.
22. Ternary conditioning remains distinct from equivariant representation.
23. Active neutral semantics are not attributed to external equivariant architectures.
24. Spatial rotation is not ternary polarity reversal.
25. Literature provenance does not replace executable qualification.
26. Shared software infrastructure does not imply shared model architecture.
27. Similarity is not identity.

---

## 122. Non-Claims

This register does not assert that:

- TR-EIP is NequIP;
- TR-EIP is MACE;
- TR-EIP is Allegro;
- TR-EIP is PaiNN;
- TR-EIP is a Tensor Field Network;
- TR-EIP is an SE(3)-Transformer;
- TR-EIP inherits published accuracy from any registered model;
- TR-EIP inherits published scaling from any registered model;
- E(3) equivariance validates FLiBe physical properties;
- literature citation proves implementation correctness.

Each such claim would require separate evidence.

---

## 123. Summary

The equivariant-model literature provides established methods for preserving geometric transformation structure in molecular and atomistic learning systems.

The relevant development chain includes:

`Tensor Field Networks`

`→ covariant molecular networks`

`→ equivariant attention`

`→ scalar/vector equivariant message passing`

`→ E(3)-equivariant interatomic potentials`

`→ higher-order and strictly local equivariant architectures`

TR-EIF uses this body of work as mathematical and architectural provenance for its spatial representation layer while retaining separate:

- resonance dynamics;
- balanced ternary execution;
- active-neutral routing;
- energy contracts;
- molecular dynamics;
- multiscale modeling;
- FLiBe specialization.

The controlling rule remains:

`equivariant ≠ identical architecture`

and:

`similar ≠ identical`
