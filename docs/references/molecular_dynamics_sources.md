# Molecular Dynamics Sources

## 1. Scope

This document defines the source register for molecular-dynamics theory, numerical integration, statistical ensembles, thermostats, barostats, periodic simulation, transport observables, and finite-size effects relevant to the Ternary Resonant Equivariant Interatomic Framework (TR-EIF).

The register covers sources relevant to:

- classical molecular dynamics;
- Newtonian equations of motion;
- time integration;
- Verlet integration;
- velocity-Verlet integration;
- periodic-boundary simulation;
- neighbor-list concepts;
- canonical sampling;
- isothermal dynamics;
- constant-pressure dynamics;
- Nosé dynamics;
- Nosé-Hoover dynamics;
- Nosé-Hoover chains;
- Parrinello-Rahman cell dynamics;
- isothermal-isobaric algorithms;
- Green-Kubo transport relations;
- diffusion;
- viscosity;
- thermal transport;
- finite-size corrections;
- deterministic and ensemble-sampling boundaries.

This register does not define the complete TR-EIF molecular-dynamics architecture.

It does not define TR-EIF resonance propagation.

It does not define balanced ternary execution.

It does not define active-neutral state `0`.

It does not provide FLiBe-specific physical transport coefficients.

---

## 2. Architectural Source Boundary

Molecular-dynamics literature provides established methods for evolving classical many-particle systems.

The architectural relation is:

`molecular-dynamics theory`

`→ TR-EIF molecular-dynamics layer`

not:

`molecular dynamics = TR-EIF`

TR-EIF additionally contains:

- continuous resonance dynamics;
- balanced ternary execution;
- E(3)-equivariant interatomic modeling;
- deterministic traces;
- multiscale mappings;
- FLiBe specialization.

---

## 3. Molecular Dynamics and Interatomic Potential

An interatomic potential defines potential energy and, under a conservative relation, force.

Molecular dynamics defines time evolution.

Therefore:

`interatomic potential ≠ molecular dynamics`

A potential does not by itself specify:

- integration method;
- thermostat;
- barostat;
- time step;
- ensemble;
- trajectory length.

---

## 4. Molecular Dynamics and Resonance Dynamics

TR-EIF resonance dynamics are a separate continuous dynamical layer.

Therefore:

`molecular dynamics ≠ resonance dynamics`

A composed TR-EIF realization may couple them explicitly.

No hidden identification is permitted.

---

## 5. Molecular Dynamics and Ternary Execution

Balanced ternary execution is also a separate layer.

Therefore:

`molecular dynamics ≠ ternary state machine`

A molecular-dynamics step must not silently execute ternary transitions unless that composition is explicitly declared.

---

## 6. Active Neutral Boundary

TR-EIF state:

`0`

is active neutral.

It must not be interpreted as:

- zero velocity;
- zero force;
- zero energy;
- missing atom;
- failed integration;
- equilibrium state;
- thermostat state.

Therefore:

`active neutral 0 ≠ numerical zero of an MD variable`

---

## 7. ALDER-WAINWRIGHT-1959-MD

B. J. Alder.

T. E. Wainwright.

"Studies in Molecular Dynamics. I. General Method."

The Journal of Chemical Physics.

Volume 31, Issue 2.

Pages 459-466.

1959.

DOI:

`10.1063/1.1730376`

Source class:

foundational primary molecular-dynamics source.

Repository role:

historical foundation for direct computer integration of classical many-particle equations of motion.

Relevant evidence domain:

- many-particle classical dynamics;
- numerical trajectory generation;
- computer simulation;
- equilibrium and nonequilibrium statistical mechanics.

---

## 8. Alder-Wainwright Source Role

This source establishes an early general molecular-dynamics simulation methodology.

It does not define:

- velocity-Verlet specifically;
- modern thermostats;
- modern barostats;
- TR-EIF resonance propagation;
- TR-EIF ternary execution.

---

## 9. RAHMAN-1964-LIQUID-ARGON-MD

A. Rahman.

"Correlations in the Motion of Atoms in Liquid Argon."

Physical Review.

Volume 136, Issue 2A.

Pages A405-A411.

1964.

DOI:

`10.1103/PhysRev.136.A405`

Source class:

foundational primary molecular-dynamics application source.

Repository role:

reference for classical molecular dynamics of a liquid and analysis of dynamical correlation observables.

Relevant evidence domain:

- liquid-state molecular dynamics;
- Lennard-Jones interactions;
- pair correlations;
- self-diffusion;
- velocity autocorrelation;
- time-dependent correlation functions.

---

## 10. Rahman Boundary

Rahman's liquid-argon simulation provides an important early MD validation/application example.

Its numerical values belong to liquid argon under the source conditions.

They are not FLiBe properties.

Therefore:

`liquid-argon MD result ≠ FLiBe validation`

---

## 11. VERLET-1967-CLASSICAL-FLUIDS

Loup Verlet.

"Computer 'Experiments' on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules."

Physical Review.

Volume 159, Issue 1.

Page 98 onward.

1967.

DOI:

`10.1103/PhysRev.159.98`

Source class:

foundational primary molecular-dynamics and numerical-integration source.

Repository role:

reference for classical-fluid molecular dynamics, Verlet integration lineage, and efficient neighbor treatment associated with Verlet-style simulation practice.

Relevant evidence domain:

- Lennard-Jones molecular dynamics;
- trajectory integration;
- thermodynamic properties;
- classical-fluid simulation;
- computational efficiency.

---

## 12. Verlet Integration Boundary

The Verlet integration family is a numerical method for classical equations of motion.

It is not:

- a force field;
- a thermostat;
- a barostat;
- a resonance integrator;
- a ternary transition operator.

Therefore:

`Verlet integrator ≠ molecular model`

---

## 13. Verlet State Boundary

A Verlet-type integrator evolves position and related dynamical state according to the selected force law.

The physical force model remains external to the integration method.

Therefore:

`same integrator + different force model → different dynamics`

---

## 14. Neighbor-List Boundary

Neighbor-list methods are computational acceleration structures.

A neighbor list is not:

- a chemical-bond graph;
- a physical phase graph;
- a ternary routing graph.

Therefore:

`neighbor list ≠ chemical bonding`

---

## 15. Neighbor-List Validity

A neighbor list is valid only while its geometric safety condition remains satisfied.

A stale neighbor list may omit physically relevant neighbors.

Therefore update policy is part of the numerical execution contract.

---

## 16. SWOPE-ANDERSEN-BERENS-WILSON-1982

William C. Swope.

Hans C. Andersen.

Peter H. Berens.

Kent R. Wilson.

"A computer simulation method for the calculation of equilibrium constants for the formation of physical clusters of molecules: Application to small water clusters."

The Journal of Chemical Physics.

Volume 76, Issue 1.

Pages 637-649.

1982.

DOI:

`10.1063/1.442716`

Source class:

primary molecular-dynamics algorithm/application source.

Repository role:

reference within the velocity-Verlet algorithm lineage and practical MD integration literature.

---

## 17. Velocity-Verlet Boundary

Velocity-Verlet is a specific second-order time integration scheme for classical dynamics.

It is distinct from the position-only historical Verlet recurrence.

Therefore:

`Verlet ≠ velocity-Verlet`

even though they belong to the same integration family.

---

## 18. Current TR-EIF Integrator

The current executable TR-EIF reference molecular-dynamics integrator uses:

`velocity-Verlet`

through the repository MD implementation.

Source literature provides numerical-method provenance.

TR-EIF implementation correctness remains validated independently.

---

## 19. Time-Step Boundary

The numerical time step:

`Δt`

is a numerical parameter.

It is not:

- a physical relaxation time by definition;
- a resonance phase lag;
- a ternary transition interval;
- a thermostat time constant unless explicitly assigned that role.

---

## 20. Positive Time Step

A valid explicit MD time step must be finite and positive under the current TR-EIF numerical contract.

Zero or negative time step is invalid.

---

## 21. Time-Step Accuracy Boundary

A numerically smaller time step may reduce integration error.

It does not automatically improve the physical model.

Therefore:

`smaller Δt ≠ more accurate potential`

Numerical error and model error remain distinct.

---

## 22. Symplectic Boundary

Verlet-family methods possess geometric integration properties useful for Hamiltonian dynamics.

This does not imply exact conservation of all invariants at finite time step.

Therefore:

`symplectic-like integration ≠ exact energy equality at every step`

---

## 23. Energy Drift Boundary

Finite-step trajectories may exhibit bounded numerical energy error.

A benchmark drift bound belongs to:

- selected integrator;
- selected time step;
- selected force evaluator;
- selected system;
- selected trajectory length.

Therefore:

`one drift bound ≠ universal MD invariant`

---

## 24. ANDERSEN-1980-CONSTANT-PRESSURE-TEMPERATURE

Hans C. Andersen.

"Molecular dynamics simulations at constant pressure and/or temperature."

The Journal of Chemical Physics.

Volume 72, Issue 4.

Pages 2384-2393.

1980.

DOI:

`10.1063/1.439486`

Source class:

foundational primary ensemble-control source.

Repository role:

reference for molecular-dynamics methods targeting constant-temperature and/or constant-pressure statistical ensembles.

Relevant evidence domain:

- canonical sampling;
- pressure control;
- temperature control;
- isothermal-isobaric sampling;
- ensemble modification.

---

## 25. Andersen Thermostat Boundary

The Andersen thermostat modifies trajectory dynamics through stochastic collisions or velocity reassignment under its declared method.

It is not deterministic Newtonian NVE dynamics.

Therefore:

`Andersen thermostat ≠ NVE trajectory`

---

## 26. Thermostat Is Not Temperature

A thermostat is a dynamical sampling mechanism.

Thermodynamic temperature is a state variable.

Therefore:

`thermostat ≠ temperature`

The thermostat controls or samples according to a temperature parameter.

---

## 27. Thermostat Is Not Ternary State

A thermostat state or collision event is not balanced ternary execution.

Therefore:

`thermostat event ≠ ternary transition`

---

## 28. NOSE-1984-CANONICAL-ENSEMBLE

Shūichi Nosé.

"A molecular dynamics method for simulations in the canonical ensemble."

Molecular Physics.

Volume 52, Issue 2.

Pages 255-268.

1984.

DOI:

`10.1080/00268978400101201`

Source class:

foundational primary thermostat source.

Repository role:

reference for extended-system molecular dynamics designed to generate canonical-ensemble behavior.

Relevant evidence domain:

- constant-temperature molecular dynamics;
- extended-system variables;
- canonical ensemble;
- thermodynamic sampling.

---

## 29. NOSE-1984-UNIFIED-FORMULATION

Shūichi Nosé.

"A unified formulation of the constant temperature molecular dynamics methods."

The Journal of Chemical Physics.

Volume 81, Issue 1.

Pages 511-519.

1984.

DOI:

`10.1063/1.447334`

Source class:

foundational primary thermostat source.

Repository role:

reference for analytical formulation and comparison of constant-temperature molecular-dynamics methods.

---

## 30. Nosé Extended-System Boundary

Nosé dynamics introduces additional dynamical variables to obtain the desired ensemble under its mathematical construction.

These variables are not physical atoms.

They must not be interpreted as additional material degrees of freedom without explicit physical meaning.

---

## 31. HOOVER-1985-CANONICAL-DYNAMICS

William G. Hoover.

"Canonical dynamics: Equilibrium phase-space distributions."

Physical Review A.

Volume 31, Issue 3.

Pages 1695-1697.

1985.

DOI:

`10.1103/PhysRevA.31.1695`

Source class:

foundational primary thermostat source.

Repository role:

reference for Nosé-Hoover canonical dynamics without explicit Nosé time scaling in the commonly used form.

Relevant evidence domain:

- canonical ensemble;
- extended dynamics;
- thermodynamic friction variable;
- phase-space distribution.

---

## 32. Nosé-Hoover Boundary

Nosé-Hoover dynamics is deterministic under fixed initial conditions.

Determinism does not guarantee ergodicity.

Therefore:

`deterministic thermostat ≠ guaranteed canonical sampling for every system`

Sampling quality requires separate validation.

---

## 33. Thermostat Ergodicity Boundary

A thermostat may generate the desired invariant distribution under appropriate conditions while failing to sample it ergodically for specific systems.

Therefore:

`formal stationary distribution ≠ practical ergodic sampling`

---

## 34. MARTYNA-KLEIN-TUCKERMAN-1992-NHC

Glenn J. Martyna.

Michael L. Klein.

Mark Tuckerman.

"Nosé-Hoover chains: The canonical ensemble via continuous dynamics."

The Journal of Chemical Physics.

Volume 97, Issue 4.

Pages 2635-2643.

1992.

DOI:

`10.1063/1.463940`

Source class:

primary thermostat-extension source.

Repository role:

reference for Nosé-Hoover chain dynamics and improved canonical sampling in systems where a single thermostat variable may be insufficient.

---

## 35. Thermostat-Chain Boundary

Adding thermostat-chain variables changes the extended dynamical system.

Therefore:

`Nosé-Hoover chain ≠ single Nosé-Hoover thermostat`

Both target canonical sampling under different dynamical constructions.

---

## 36. Current TR-EIF Thermostat Boundary

The existence of thermostat literature in this register does not imply that every thermostat is currently implemented in TR-EIF.

Executable support must be confirmed from:

`src/tr_eif/md/`

and qualification tests.

Source registration and implementation are separate states.

---

## 37. PARRINELLO-RAHMAN-1981

M. Parrinello.

A. Rahman.

"Polymorphic transitions in single crystals: A new molecular dynamics method."

Journal of Applied Physics.

Volume 52.

Pages 7182-7190.

1981.

DOI:

`10.1063/1.328693`

Source class:

foundational primary variable-cell molecular-dynamics source.

Repository role:

reference for flexible-cell dynamics and simulation under externally applied stress conditions.

Relevant evidence domain:

- variable simulation cells;
- cell degrees of freedom;
- stress-controlled dynamics;
- polymorphic transitions;
- extended Lagrangian formulation.

---

## 38. Parrinello-Rahman Boundary

Parrinello-Rahman cell dynamics modifies the simulation cell as a dynamical object.

It is distinct from:

- fixed-cell NVE;
- fixed-cell NVT;
- isotropic-only volume scaling.

Therefore:

`flexible-cell dynamics ≠ fixed-volume MD`

---

## 39. Cell Dynamics Is Not Structural Transition by Definition

A changing simulation cell may permit structural transformations.

Cell motion alone does not prove a physical phase transition.

Therefore:

`cell change ≠ physical phase transition`

---

## 40. MARTYNA-TOBIAS-KLEIN-1994

Glenn J. Martyna.

Douglas J. Tobias.

Michael L. Klein.

"Constant pressure molecular dynamics algorithms."

The Journal of Chemical Physics.

Volume 101, Issue 5.

Pages 4177-4189.

1994.

DOI:

`10.1063/1.467468`

Source class:

primary constant-pressure molecular-dynamics source.

Repository role:

reference for modularly invariant isothermal-isobaric molecular-dynamics algorithms including isotropic and flexible-cell motion.

---

## 41. Barostat Boundary

A barostat is an ensemble-control mechanism.

It is not:

- pressure itself;
- an interatomic potential;
- a ternary state;
- a resonance operator.

Therefore:

`barostat ≠ pressure`

---

## 42. Pressure-Control Boundary

A target pressure parameter and instantaneous pressure observable are distinct.

Therefore:

`target pressure ≠ instantaneous pressure`

The control method defines their dynamical relation.

---

## 43. Ensemble Identity

Common classical ensembles include:

`NVE`

`NVT`

`NPT`

These labels describe statistical constraints or target ensembles.

They are not balanced-ternary states.

Therefore:

`NVE/NVT/NPT ≠ -1/0/1`

---

## 44. Ensemble vs Trajectory

An ensemble is a probability distribution or statistical state.

A trajectory is one dynamical realization.

Therefore:

`one trajectory ≠ ensemble`

Ensemble properties require appropriate sampling assumptions.

---

## 45. Time Average vs Ensemble Average

Equality between time averages and ensemble averages requires applicable ergodic assumptions.

It is not a universal identity for every finite trajectory.

Therefore:

`finite time average ≠ exact ensemble average`

without further conditions.

---

## 46. Initial-Condition Boundary

A deterministic trajectory depends on initial:

- positions;
- velocities;
- masses;
- model state.

Different initial conditions generally produce different trajectories.

Therefore initial state is part of reproducibility closure.

---

## 47. Velocity Distribution Boundary

Assigning velocities from a statistical distribution is an initialization procedure.

The resulting random state requires:

- generator;
- seed;
- sampling method

for strict reproduction.

---

## 48. Momentum Removal Boundary

Removing center-of-mass momentum changes the initialized state.

It must be explicit when applied.

Therefore:

`raw sampled velocities ≠ momentum-corrected velocities`

---

## 49. Periodic-Boundary Conditions

Periodic boundaries represent a finite simulation cell tiled through space according to the declared lattice.

They are a simulation construction.

They are not literal finite physical boundaries of the modeled bulk material.

---

## 50. Periodic Cell Requirement

Periodic geometry requires an explicit simulation cell.

The cell defines lattice vectors and coordinate conversion.

A periodic flag without valid cell geometry is incomplete.

---

## 51. Minimum-Image Boundary

A minimum-image convention chooses a periodic displacement representative according to the declared cell algorithm.

Different cell geometries may require different algorithms.

Therefore:

`componentwise fractional wrapping ≠ universal shortest Cartesian image`

for arbitrary strongly skewed cells.

---

## 52. Periodic Replica Boundary

Periodic images are mathematical replicas of the simulation cell.

They are not additional independent atoms in the base cell.

Therefore atom count and periodic-image count must not be conflated.

---

## 53. Cutoff and Periodicity

A cutoff under periodic boundaries must be compatible with the cell geometry and selected minimum-image or neighbor algorithm.

An invalid cutoff/cell relation can produce ambiguous or duplicated interactions.

---

## 54. Neighbor-List Rebuild

A Verlet-style neighbor list may use a buffer or skin.

The list must be rebuilt before particle motion invalidates the safety margin.

Rebuild policy is part of numerical correctness.

---

## 55. Neighbor List Is Not Interaction Graph Identity

A computational neighbor list may contain candidates beyond the actual interaction cutoff.

Therefore:

`neighbor-list entry ≠ active interaction edge`

unless the model graph defines them identically.

---

## 56. GREEN-1954-IRREVERSIBLE-FLUIDS

Melville S. Green.

"Markoff Random Processes and the Statistical Mechanics of Time-Dependent Phenomena. II. Irreversible Processes in Fluids."

The Journal of Chemical Physics.

Volume 22, Issue 3.

Pages 398-413.

1954.

DOI:

`10.1063/1.1740082`

Source class:

foundational primary transport-theory source.

Repository role:

reference for equilibrium time-correlation expressions for transport phenomena in fluids.

Relevant evidence domain:

- diffusion;
- viscosity;
- thermal conductivity;
- time-correlation functions;
- irreversible transport.

---

## 57. KUBO-1957-IRREVERSIBLE-PROCESSES

Ryogo Kubo.

"Statistical-Mechanical Theory of Irreversible Processes. I. General Theory and Simple Applications to Magnetic and Conduction Problems."

Journal of the Physical Society of Japan.

Volume 12, Issue 6.

Pages 570-586.

1957.

DOI:

`10.1143/JPSJ.12.570`

Source class:

foundational primary linear-response and transport-theory source.

Repository role:

reference for fluctuation-dissipation theory and time-correlation representations of response/transport coefficients.

---

## 58. Green-Kubo Boundary

Green-Kubo relations connect transport coefficients to equilibrium time-correlation functions under their statistical-mechanical assumptions.

They are not simply arbitrary trajectory averages.

Therefore:

`time correlation ≠ transport coefficient`

until the required integral, normalization, and physical relation are applied.

---

## 59. Transport Coefficient Boundary

Transport coefficients are macroscopic statistical observables.

They are not instantaneous per-step state variables.

Therefore:

`single MD step ≠ transport coefficient`

---

## 60. Diffusion Boundary

Self-diffusion may be estimated from:

- mean-square displacement;
- velocity autocorrelation

under appropriate statistical relations.

The two methods are theoretically related under applicable conditions.

They remain distinct numerical estimators.

---

## 61. Diffusion Is Species-Specific

A diffusion coefficient belongs to a declared transported species or tracer.

Therefore:

`hydrogen-isotope diffusion ≠ Li diffusion`

`Li diffusion ≠ Be diffusion`

`Be diffusion ≠ F diffusion`

unless the source explicitly reports the same quantity.

---

## 62. Viscosity Boundary

Viscosity is a collective transport property.

It may be computed from stress correlation or related methods under declared conditions.

It is not equal to instantaneous stress.

Therefore:

`stress ≠ viscosity`

---

## 63. Thermal-Conductivity Boundary

Thermal conductivity involves heat-current correlations or other declared transport relations.

It is not equal to instantaneous energy.

Therefore:

`energy ≠ thermal conductivity`

---

## 64. Transport-Sampling Requirement

Reliable transport estimates generally require:

- sufficient trajectory length;
- equilibrated sampling;
- statistically appropriate analysis;
- convergence assessment.

A short deterministic smoke test does not establish bulk transport accuracy.

---

## 65. Autocorrelation Boundary

An autocorrelation function is a time-dependent observable.

Its integral or asymptotic behavior may define other quantities under specific theory.

The autocorrelation function itself is not the derived transport coefficient.

---

## 66. Finite-Time Boundary

A finite simulation provides a finite estimate of an infinite-time relation.

Truncation and statistical uncertainty must be considered.

Therefore:

`finite correlation integral ≠ exact infinite-time coefficient`

---

## 67. Statistical Error Boundary

Transport estimates may exhibit correlated statistical error.

Independent-sample formulas must not be applied blindly to strongly correlated trajectories.

---

## 68. YE-HUMMER-2004-FINITE-SIZE

In-Chul Yeh.

Gerhard Hummer.

"System-Size Dependence of Diffusion Coefficients and Viscosities from Molecular Dynamics Simulations with Periodic Boundary Conditions."

The Journal of Physical Chemistry B.

Volume 108, Issue 40.

Pages 15873-15879.

2004.

DOI:

`10.1021/jp0477147`

Source class:

primary finite-size transport-analysis source.

Repository role:

reference for periodic-boundary finite-size effects in translational diffusion and viscosity estimates.

---

## 69. Diffusion Finite-Size Boundary

Diffusion coefficients obtained under periodic boundary conditions can depend on simulation-cell size.

Therefore:

`D_PBC ≠ automatically infinite-system D`

Finite-size treatment is part of transport validation when quantitatively relevant.

---

## 70. Yeh-Hummer Correction Boundary

For the source's applicable cubic-cell hydrodynamic treatment, finite-size diffusion correction depends on:

- cell size;
- temperature;
- viscosity;
- hydrodynamic assumptions.

It is not a universal correction for arbitrary geometries or transport models.

---

## 71. Finite-Size Correction Is Derived

A corrected diffusion coefficient calculated from a source relation is:

`DERIVED`

unless directly reported as the source's own value.

The underlying simulation measurement retains its original provenance.

---

## 72. Thermostat and Transport Boundary

Thermostats can affect dynamical correlation functions.

A transport calculation must declare the sampling dynamics and assess whether the thermostat is compatible with the intended observable.

Therefore:

`correct ensemble sampling ≠ automatically correct transport dynamics`

---

## 73. Barostat and Transport Boundary

Cell fluctuations may affect transport analysis.

A transport result obtained under NPT dynamics must retain its ensemble and algorithm context.

---

## 74. Equilibration Boundary

Equilibration and production sampling are different stages.

Therefore:

`equilibration trajectory ≠ production trajectory`

unless the declared protocol intentionally combines them.

---

## 75. Equilibration Criterion

Equilibration must be judged using explicit observables or convergence criteria.

Elapsed step count alone does not prove equilibrium.

---

## 76. Production Sampling

Production data used for physical observables must be collected under the declared stationary or sampling conditions.

Changing parameters during production defines a different sampling process.

---

## 77. Time Origin

Time-correlation calculations may average over multiple time origins.

The averaging procedure must remain explicit for reproducibility.

---

## 78. Trajectory Sampling Frequency

Output sampling frequency affects stored time-series resolution.

It is distinct from integration time step.

Therefore:

`trajectory write interval ≠ MD integration step`

---

## 79. Integrator and Output Frequency

A trajectory may integrate every:

`Δt`

while saving every:

`n × Δt`

The omitted intermediate states still affect dynamics.

---

## 80. Force-Evaluation Frequency

In ordinary velocity-Verlet, force evaluation follows the integrator schedule.

A multiple-time-step algorithm changes this schedule and defines another numerical method.

---

## 81. Multiple-Time-Step Boundary

A multiple-time-step method is not the same integrator merely because one component uses Verlet-like updates.

Its stability properties require separate validation.

---

## 82. Constraint Boundary

Holonomic constraints modify the allowed configuration manifold.

A constrained MD method is not identical to unconstrained Newtonian integration.

---

## 83. Rigid-Body Boundary

Rigid-body dynamics and flexible atomistic dynamics have different degrees of freedom.

A rigid constraint must remain explicit.

---

## 84. Ensemble Control vs Physical Dissipation

A thermostat variable may exchange energy with the modeled subsystem.

This algorithmic energy exchange is not automatically the same as a physical microscopic dissipative mechanism.

Therefore:

`thermostat friction ≠ physical dissipation mechanism by definition`

---

## 85. TR-EIF Open-System Boundary

TR-EIF may model open nonlinear dissipative dynamics in broader architectures.

Standard thermostat algorithms are one specific numerical/statistical mechanism.

They must not be identified with the complete TR-EIF open-system theory.

---

## 86. Resonance Propagation Boundary

A composed TR-EIF molecular-dynamics realization may explicitly propagate resonance state.

That propagation belongs to the TR-EIF resonance model.

It is not inherited from classical MD sources in this register.

---

## 87. Ternary Propagation Boundary

A composed TR-EIF molecular-dynamics realization may explicitly execute ternary state transitions.

That execution belongs to the TR-EIF ternary contract.

It is not defined by Verlet, Andersen, Nosé, Hoover, or Parrinello-Rahman.

---

## 88. Operator-Ordering Boundary

When MD, resonance, and ternary updates are composed, operator ordering may affect the result.

Therefore reproducibility requires explicit order.

For example:

`MD step`

`→ resonance update`

`→ ternary target`

`→ ternary execution`

is not assumed equivalent to another order.

---

## 89. Hidden-State Prohibition

Molecular-dynamics execution must not silently modify:

- resonance state;
- ternary pending target;
- model parameters;
- graph rule

unless that operation is explicitly part of the declared step.

---

## 90. Graph-Rebuild Boundary

TR-EIF may rebuild the interaction graph between physical MD states.

This is compatible with holding graph topology fixed inside one finite-difference force derivative.

Therefore:

`graph fixed inside derivative`

does not imply:

`graph fixed for entire trajectory`

---

## 91. Force Consistency

The force evaluator used in MD must correspond to the declared energy model if the trajectory is claimed to use conservative forces.

Therefore:

`MD force ≠ arbitrary independent force`

under the conservative TR-EIP path.

---

## 92. Energy Consistency

Potential energy recorded along a trajectory must correspond to the same model state and configuration used for force evaluation when energy-conservation claims are made.

---

## 93. Total MD Energy

Under the declared classical MD observable convention:

`E_total = E_kinetic + E_potential`

This relation is distinct from the atomic energy decomposition of potential energy.

---

## 94. Kinetic Energy

Classical translational kinetic energy depends on:

- masses;
- velocities.

It is not determined by ternary state.

Therefore:

`kinetic energy ≠ ternary execution state`

---

## 95. Mass Boundary

Mass is a physical parameter.

A test-fixture mass remains:

`TEST_FIXTURE`

and must not be presented as material-specific physical mass evidence.

---

## 96. Temperature Estimator Boundary

Kinetic-temperature estimators depend on:

- kinetic energy;
- degrees of freedom;
- constraints;
- statistical convention.

Temperature is not simply mean velocity magnitude.

---

## 97. Degrees-of-Freedom Boundary

The number of thermodynamic degrees of freedom may differ from:

`3N`

when constraints or conserved collective motions are removed.

The temperature estimator must match the declared degrees-of-freedom convention.

---

## 98. Pressure Estimator Boundary

Instantaneous pressure may contain:

- kinetic contribution;
- virial contribution;
- volume normalization

under the selected classical formulation.

Pressure is not equivalent to stress tensor without an explicit convention.

---

## 99. Virial Boundary

Virial expressions depend on force and geometry conventions.

They must not be imported without matching the model's force and periodic-boundary definitions.

---

## 100. Current TR-EIF MD Boundary

The current TR-EIF executable reference supports a defined subset of general molecular-dynamics functionality.

Source presence in this register does not imply implementation of every:

- thermostat;
- barostat;
- constraint method;
- transport estimator;
- finite-size correction.

Implementation status must be read from the repository.

---

## 101. Source Registered vs Implemented

The relation remains:

`source registered ≠ feature implemented`

Likewise:

`feature implemented ≠ source-backed physical validation`

These are separate evidence dimensions.

---

## 102. Source Classification Matrix

| Source identifier | Repository role |
| --- | --- |
| `ALDER-WAINWRIGHT-1959-MD` | foundational MD method |
| `RAHMAN-1964-LIQUID-ARGON-MD` | foundational liquid-state MD application |
| `VERLET-1967-CLASSICAL-FLUIDS` | Verlet integration and classical-fluid MD lineage |
| `ANDERSEN-1980-CONSTANT-PRESSURE-TEMPERATURE` | temperature/pressure ensemble control |
| `SWOPE-ANDERSEN-BERENS-WILSON-1982` | velocity-Verlet algorithm lineage/application |
| `NOSE-1984-CANONICAL-ENSEMBLE` | Nosé canonical-ensemble dynamics |
| `NOSE-1984-UNIFIED-FORMULATION` | constant-temperature MD formulation |
| `HOOVER-1985-CANONICAL-DYNAMICS` | Nosé-Hoover canonical dynamics |
| `PARRINELLO-RAHMAN-1981` | flexible-cell constant-stress dynamics |
| `MARTYNA-KLEIN-TUCKERMAN-1992-NHC` | Nosé-Hoover chain dynamics |
| `MARTYNA-TOBIAS-KLEIN-1994` | constant-pressure MD algorithms |
| `GREEN-1954-IRREVERSIBLE-FLUIDS` | transport time-correlation theory |
| `KUBO-1957-IRREVERSIBLE-PROCESSES` | fluctuation-dissipation and transport theory |
| `YEH-HUMMER-2004-FINITE-SIZE` | periodic finite-size transport correction |

---

## 103. Source-Use Rule

A source is used only for the method or relation it establishes.

For example:

`PARRINELLO-RAHMAN-1981`

supports variable-cell molecular-dynamics methodology.

It does not directly establish TR-EIF ternary routing.

---

## 104. Method Source vs Material Source

A molecular-dynamics method paper provides method provenance.

It does not provide FLiBe-specific material-property evidence unless the paper actually studies FLiBe.

Therefore:

`MD method source ≠ FLiBe source`

---

## 105. Algorithm Accuracy Boundary

Published accuracy or stability observations for one system do not become universal limits for TR-EIF.

A numerical method must be validated on the actual model/domain of interest.

---

## 106. Time-Step Transfer Boundary

A stable time step in one system does not automatically transfer to another.

The appropriate time step depends on:

- fastest relevant dynamics;
- masses;
- force stiffness;
- integrator;
- model coupling.

---

## 107. Thermostat-Parameter Transfer Boundary

A thermostat relaxation or collision parameter from another system must not be imported without justification.

Parameter provenance remains explicit.

---

## 108. Barostat-Parameter Transfer Boundary

Likewise barostat masses, relaxation times, or coupling constants are numerical parameters requiring domain-specific validation.

---

## 109. Transport-Parameter Boundary

A source-derived diffusion coefficient or viscosity belongs to its:

- material;
- species;
- composition;
- temperature;
- pressure;
- phase;
- method.

Transport values are not generic MD parameters.

---

## 110. FLiBe Transport Boundary

FLiBe-specific transport evidence remains governed by:

`docs/references/flibe_sources.md`

The MD source register provides method/theory provenance only.

---

## 111. Statistical Ensemble Boundary

An ensemble label states a statistical constraint.

It does not define the exact trajectory generated by every algorithm targeting that ensemble.

Different algorithms may sample the same intended ensemble through different dynamics.

---

## 112. Ensemble Equivalence Boundary

Different statistical ensembles may become equivalent in particular thermodynamic limits for selected observables.

They are not exactly identical finite-system distributions in general.

Therefore:

`NVE ≠ NVT ≠ NPT`

as finite-system ensemble definitions.

---

## 113. Determinism Boundary

NVE velocity-Verlet with deterministic force evaluation is deterministic for fixed complete initial state.

Stochastic thermostat methods are not deterministic unless their random state is also included.

---

## 114. Random-State Reproducibility

A stochastic MD method requires reproducibility metadata including:

- random generator;
- seed;
- generator state where necessary;
- sampling order.

A seed alone may be insufficient for mid-trajectory restart.

---

## 115. Continuous-Time vs Discrete-Time Boundary

Classical equations of motion are continuous in time.

A numerical MD integrator produces discrete time-step approximations.

Therefore:

`continuous trajectory ≠ discrete numerical trajectory`

The integrator defines the approximation.

---

## 116. Numerical Trajectory Identity

Two integrations with different:

- time steps;
- integrators;
- floating-point environments

may approximate the same continuous model without producing identical trajectories.

Therefore:

`same continuous model ≠ byte-identical trajectory`

---

## 117. Chaotic Sensitivity

Many nonlinear many-particle trajectories exhibit sensitivity to small perturbations.

Long-time pointwise trajectory divergence does not automatically invalidate statistical observables.

Validation must use the correct relation for the intended claim.

---

## 118. Deterministic Replay Boundary

TR-EIF deterministic replay refers to the declared executable state and output contract.

It does not claim that two mathematically equivalent but numerically perturbed chaotic trajectories remain pointwise identical forever.

---

## 119. Ensemble Validation vs Replay

Deterministic replay and ensemble validation answer different questions.

Replay tests identity under fixed execution.

Ensemble validation tests statistical behavior.

Therefore:

`replay ≠ ensemble validation`

---

## 120. Transport Validation vs Replay

A bitwise reproducible trajectory does not guarantee correct transport coefficients.

Therefore:

`determinism ≠ transport accuracy`

---

## 121. Conservation vs Ensemble Control

An NVE benchmark may test numerical total-energy behavior.

A thermostatted NVT trajectory intentionally exchanges energy with an extended or stochastic control mechanism.

Therefore:

`NVT trajectory ≠ NVE energy-conservation test`

---

## 122. Pressure Control vs Energy Conservation

A variable-cell or barostatted system may exchange work with the extended cell/control variables.

Naive fixed-volume energy-conservation interpretation may therefore be inappropriate.

---

## 123. Extended Hamiltonian Boundary

Some extended-system algorithms possess conserved extended quantities under their own formalism.

Those quantities must not be confused with the physical subsystem energy.

---

## 124. Observable-Sampling Boundary

A simulation may generate many observables from one trajectory.

Each observable still requires its own:

- estimator;
- normalization;
- convergence analysis;
- uncertainty analysis.

---

## 125. Radial Distribution Boundary

A radial distribution function is a structural observable.

It is not a transport coefficient.

Therefore:

`RDF ≠ diffusion`

---

## 126. Structure Factor Boundary

A structure factor is a reciprocal-space structural observable.

It is not automatically the Fourier transform of every repository structural quantity without the applicable definition and normalization.

---

## 127. Coordination Boundary

Coordination derived from MD depends on its definition.

A cutoff-based coordination number is model-relative.

Therefore:

`coordination count ≠ chemical bond count`

---

## 128. MSD Boundary

Mean-square displacement is a time-dependent statistic.

Its long-time slope may define self-diffusion under the applicable dimensional relation.

A short-time ballistic regime must not be used as a diffusive slope without justification.

---

## 129. VACF Boundary

Velocity autocorrelation contains dynamical information.

Its time integral can relate to diffusion under the applicable Green-Kubo relation.

The raw correlation function is not itself the diffusion coefficient.

---

## 130. Stress Autocorrelation Boundary

Stress autocorrelation may contribute to viscosity evaluation.

Instantaneous stress is not viscosity.

The integral, tensor-component convention, temperature, volume, and normalization must be explicit.

---

## 131. Heat-Flux Boundary

Heat-current correlations may be used for thermal conductivity.

The heat-current definition is model-dependent.

It must correspond to the energy/interaction representation being used.

---

## 132. Potential Energy Decomposition and Heat Flux

Different energy decompositions can affect microscopic heat-current expressions while preserving macroscopic observables under appropriate theory.

A heat-flux implementation must therefore match the selected potential architecture.

---

## 133. Long-Range Electrostatics Boundary

Periodic ionic systems may require long-range electrostatic methods.

A short-range neighbor list alone does not establish complete ionic dynamics.

Therefore:

`short-range cutoff ≠ complete ionic interaction`

---

## 134. Ewald Boundary

Ewald-type methods provide one class of periodic long-range interaction treatments.

The presence of periodic boundaries does not imply that an Ewald method is automatically active.

Implementation must be explicit.

---

## 135. FLiBe Ionic Boundary

Because FLiBe is ionic, physical MD validation must account for the selected treatment of ionic interactions.

The generic TR-EIF reference fixture does not automatically establish a physically complete FLiBe interaction model.

---

## 136. Current FLiBe MD Qualification Boundary

Current FLiBe MD tests validate executable architecture and invariants using declared fixtures.

They do not by themselves establish:

- experimentally accurate FLiBe diffusion;
- experimentally accurate viscosity;
- phase-equilibrium dynamics;
- full ionic long-range physics.

---

## 137. Source-to-TR-EIF Mapping

The principal mapping is:

### Alder-Wainwright / Rahman / Verlet

classical MD foundations and trajectory simulation.

### Swope et al.

velocity-Verlet lineage.

### Andersen / Nosé / Hoover / Martyna et al.

ensemble-control methods.

### Parrinello-Rahman / Martyna-Tobias-Klein

variable-cell and constant-pressure methods.

### Green / Kubo

time-correlation transport foundations.

### Yeh-Hummer

periodic finite-size transport corrections.

---

## 138. TR-EIF-Specific Extensions

The following are TR-EIF-specific or repository-specific and are not defined by the MD sources above:

- resonance propagation;
- balanced ternary state propagation;
- active-neutral routing;
- pending-target semantics;
- resonance-conditioned energy;
- ternary-conditioned energy;
- deterministic trace contract;
- TR-EIP model family;
- FLiBe multiscale closure.

---

## 139. No Hidden Import of Source Parameters

No numerical parameter from the MD literature is automatically imported into TR-EIF.

Examples include:

- time step;
- thermostat mass;
- collision rate;
- barostat mass;
- coupling time;
- neighbor skin;
- sampling interval.

Every result-affecting parameter remains explicit.

---

## 140. Method Provenance vs Parameter Provenance

Citing a method paper establishes method provenance.

It does not establish the correctness of a chosen numerical parameter.

Therefore:

`method source ≠ parameter validation`

---

## 141. Reproducibility Boundary

Reproducing an MD trajectory requires:

- source revision;
- initial configuration;
- velocities;
- masses;
- force model;
- integrator;
- time step;
- graph policy;
- thermostat/barostat state where applicable;
- random state where applicable;
- composed resonance/ternary state when enabled.

---

## 142. MD Restart Boundary

A restart state must include all result-affecting state required to continue the same trajectory.

Coordinates and velocities alone may be insufficient for:

- thermostat chains;
- barostat state;
- adaptive algorithms;
- resonance state;
- pending ternary routes.

---

## 143. Trajectory Output Boundary

A stored trajectory may contain only selected state variables.

Therefore:

`trajectory file ≠ complete restart state`

unless the format contract explicitly guarantees complete state closure.

---

## 144. Trace Boundary

A TR-EIF observable trace and an MD trajectory are distinct artifacts.

A base trace does not contain complete coordinates or velocities.

Therefore:

`trace ≠ trajectory`

---

## 145. Validation Matrix Boundary

The presence of method sources in this register does not change the validation state recorded in:

`docs/validation/flibe_validation_matrix.md`

Only actual implementation, qualification, and source-backed comparison evidence may change validation status.

---

## 146. Citation Audit

Before release, this register must be audited for:

- author names;
- title;
- publication venue;
- year;
- volume;
- issue where applicable;
- pages/article number;
- DOI;
- source role;
- method-to-claim correspondence.

---

## 147. Primary vs Review Source

This register emphasizes primary methodological sources.

Later textbooks and reviews may be useful for synthesis.

They must not replace primary attribution for the original methods where primary sources are available.

---

## 148. Source Conflict Boundary

If different sources define different algorithm conventions, the repository must state which convention is used.

It must not average incompatible algorithms into one undefined method.

---

## 149. Algorithm Naming Boundary

Names such as:

- Verlet;
- velocity-Verlet;
- Nosé;
- Nosé-Hoover;
- Nosé-Hoover chain;
- Andersen;
- Parrinello-Rahman

refer to distinct numerical/dynamical constructions.

They must not be treated as interchangeable labels.

---

## 150. Core Source Invariants

This register preserves:

1. Molecular dynamics and interatomic potential remain distinct.
2. Molecular dynamics and resonance dynamics remain distinct.
3. Molecular dynamics and ternary execution remain distinct.
4. Active neutral `0` is not an MD numerical zero.
5. Verlet and velocity-Verlet remain distinct algorithms.
6. Integrator and force model remain distinct.
7. Time step is a numerical parameter, not a physical validation result.
8. Neighbor lists are computational structures, not chemical bonds.
9. Periodic replicas are not independent base-cell atoms.
10. NVE, NVT, and NPT remain distinct ensembles.
11. Ensemble and trajectory remain distinct.
12. Thermostat and thermodynamic temperature remain distinct.
13. Barostat and pressure remain distinct.
14. Deterministic dynamics does not imply ergodic sampling.
15. Green-Kubo correlation functions are not themselves transport coefficients.
16. Diffusion, viscosity, and thermal conductivity remain distinct observables.
17. Transport estimates require statistical convergence.
18. Finite periodic cells can bias transport estimates.
19. FLiBe transport values require FLiBe-specific evidence.
20. Graph-fixed force differentiation does not imply trajectory-wide fixed graph.
21. Generic MD does not silently evolve resonance state.
22. Generic MD does not silently evolve ternary state.
23. Numerical energy drift is benchmark- and method-dependent.
24. A method source does not validate a chosen parameter value.
25. Reproducible trajectory identity requires complete state closure.
26. Trajectory is not automatically complete restart state.
27. Trace is not trajectory.
28. Source registration does not imply implementation.
29. Implementation does not imply physical validation.
30. Similarity is not identity.

---

## 151. Related Documentation

This register supports:

`docs/volume_05_molecular_dynamics/`

`docs/architecture/energy_model_contract.md`

`docs/architecture/determinism_contract.md`

`docs/specifications/energy_output_specification.md`

`docs/specifications/trace_specification.md`

`docs/validation/numerical_validation_plan.md`

`docs/validation/reproducibility_plan.md`

`docs/validation/flibe_validation_matrix.md`

and:

`docs/references/interatomic_potential_sources.md`

---

## 152. Non-Claims

This register does not assert that:

- every listed thermostat is implemented in TR-EIF;
- every listed barostat is implemented in TR-EIF;
- TR-EIF uses Ewald electrostatics;
- current TR-EIF MD is a complete physical FLiBe simulator;
- source-listed transport methods already have executable TR-EIF implementations;
- method provenance establishes FLiBe transport accuracy;
- energy conservation alone validates all molecular dynamics;
- deterministic replay establishes ensemble correctness.

Each such claim requires separate implementation and evidence.

---

## 153. Summary

Molecular-dynamics literature provides the established numerical and statistical-mechanical foundation for evolving atomistic systems in time.

The methodological lineage relevant to TR-EIF includes:

`Alder-Wainwright`

`→ Rahman`

`→ Verlet-family integration`

`→ temperature/pressure ensemble control`

`→ Nosé-Hoover and chain dynamics`

`→ flexible-cell constant-pressure methods`

`→ Green-Kubo transport analysis`

`→ finite-size transport correction`

while TR-EIF adds its own separate architecture:

`conservative TR-EIP force model`

`+ explicit molecular dynamics`

`+ optional explicit resonance propagation`

`+ optional explicit ternary propagation`

`+ deterministic trace`

`+ multiscale and FLiBe validation`

The controlling rules remain:

`method ≠ model`

`trajectory ≠ ensemble`

`determinism ≠ physical accuracy`

`source registered ≠ feature implemented`

and:

`similar ≠ identical`
