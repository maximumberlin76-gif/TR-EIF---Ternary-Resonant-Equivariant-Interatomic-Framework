# Notation and Definitions

## 1. Purpose

This document defines the notation, symbol classes, mathematical objects, semantic categories, and terminology used by the Ternary Resonant Equivariant Interatomic Framework.

The definitions in this document establish the common language of TR-EIF.

Every later mathematical statement, implementation contract, schema, trace, test, and validation artifact must use these definitions consistently.

A symbol must not be assigned multiple incompatible meanings within the same mathematical context.

A later document may introduce additional notation only when:

- every new symbol is defined before use;
- its domain and codomain are declared;
- its relation to existing notation is explicit;
- no existing authoritative definition is silently replaced;
- overloaded notation is explicitly disambiguated.

## 2. Definition Classes

TR-EIF separates definitions by scientific and operational status.

### 2.1 Classical definition

A classical definition is a mathematical or physical definition adopted from established literature.

A classical definition must preserve:

- its original mathematical meaning;
- its required assumptions;
- its domain of validity;
- its transformation properties;
- its dimensional interpretation where applicable.

Repository notation may differ from the source notation only when an explicit notation mapping is provided.

### 2.2 TR-EIF definition

A TR-EIF definition introduces an author-defined object, state semantic, mapping, invariant, transition rule, or structural relation specific to the framework.

A TR-EIF definition must identify:

- the object being defined;
- its domain;
- its permitted values;
- its relation to existing classical structures;
- its operational consequences;
- its invariants.

### 2.3 Operational definition

An operational definition specifies how a mathematical or physical quantity is represented, measured, computed, serialized, or tested.

An operational definition does not automatically establish that the represented quantity is a complete physical description.

### 2.4 Derived definition

A derived definition is constructed from previously defined objects.

Its dependency chain must be explicit.

A derived definition must not introduce an undeclared assumption.

## 3. Typographic Conventions

TR-EIF uses the following typographic conventions.

### 3.1 Scalar quantities

Ordinary lowercase symbols represent scalar quantities unless another meaning is declared.

Examples:

- `t` — time;
- `a` — amplitude;
- `ω` — angular frequency;
- `e` — scalar energy value;
- `τ` — delay;
- `λ` — generic parameter.

### 3.2 Vectors

Bold formatting may be used in rendered mathematical documents when supported.

In plain GitHub Markdown, vector quantities are identified by their definitions and component structure.

Examples:

- `x_i(t)` — position vector of atomic site `i`;
- `v_i(t)` — velocity vector of atomic site `i`;
- `f_i(t)` — force vector acting on atomic site `i`;
- `X(t)` — complete continuous state vector.

### 3.3 Matrices and tensors

Uppercase symbols may represent matrices, linear operators, tensors, or complete state objects when explicitly defined.

Examples:

- `A` — matrix or operator;
- `H` — history object;
- `Σ` — stress tensor;
- `J` — Jacobian matrix;
- `X` — continuous state space or continuous state object, depending on context.

The distinction between a space and an element of that space must always be explicit.

### 3.4 Sets and spaces

Uppercase calligraphic-style Unicode symbols or descriptive uppercase names may represent sets and spaces.

Examples:

- `T` — balanced ternary state set;
- `X` — continuous state space;
- `Y` — observable output space;
- `V` — vertex or atomic-site set;
- `E` — edge or interaction set;
- `G` — interaction graph;
- `G_sym` — declared symmetry group;
- `P` — parameter space.

### 3.5 Indices

The following index conventions apply unless a document declares a narrower local convention:

- `i`, `j`, `k` — atomic sites, oscillatory units, nodes, or local components;
- `n` — discrete execution step;
- `m` — secondary discrete index;
- `α`, `β` — components, channels, modes, or coordinate directions;
- `s` — scale index;
- `r` — realization, replay, or run index.

An index must not change meaning within one equation or definition.

## 4. Primitive Number Domains

The following number domains are used.

- `ℕ` — natural numbers.
- `ℤ` — integers.
- `ℝ` — real numbers.
- `ℝ₊` — non-negative real numbers unless strict positivity is explicitly stated.
- `ℂ` — complex numbers.
- `𝕊¹` — phase circle.

When ambiguity is possible, the repository must state whether `ℕ` includes `0`.

For execution counters and array indices, the index origin must be declared explicitly.

## 5. Time Domains

### 5.1 Continuous time

Continuous time is represented by:

`t ∈ I_t`

where `I_t` is the declared time interval.

Possible interval forms include:

- finite interval;
- semi-infinite interval;
- periodic interval;
- experimentally sampled interval.

The units of `t` must be declared wherever the variable represents physical time.

### 5.2 Discrete execution time

Discrete execution steps are represented by:

`n ∈ ℕ`

A discrete step does not automatically represent a fixed physical duration.

When discrete steps correspond to physical time, the mapping must be declared.

A uniform mapping may be written as:

`t_n = t_0 + nΔt`

where:

- `t_0` is the initial physical time;
- `Δt` is the time-step duration;
- `t_n` is the physical time associated with execution step `n`.

### 5.3 Event time

A state transition, structural transition, threshold crossing, or discrete routing action may occur at event time:

`t_k`

The index `k` identifies the event order.

Event time and integration-step time must not be silently identified.

### 5.4 Operational interval

An operational interval is a finite interval over which a declared structure preserves the relations required for its identity or function.

An operational interval may be defined by:

- time;
- number of cycles;
- number of execution steps;
- number of interactions;
- structural retention condition;
- bounded-error condition.

## 6. System Definition

### 6.1 System

A system is a declared collection of state variables, relations, transformations, boundaries, and observables treated as one modeled organization.

A TR-EIF system definition must identify:

- included degrees of freedom;
- excluded degrees of freedom;
- boundary conditions;
- permitted exchanges;
- state spaces;
- time domain;
- observables;
- model assumptions.

### 6.2 Environment

The environment is the set of degrees of freedom excluded from the declared system boundary but permitted to interact with the system.

Environmental interaction may include exchange of:

- energy;
- momentum;
- matter;
- phase influence;
- boundary forcing;
- structural constraints;
- information represented by the model.

### 6.3 System boundary

The system boundary separates included and excluded degrees of freedom for the selected representation.

A boundary may be:

- spatial;
- temporal;
- energetic;
- topological;
- computational;
- observational;
- scale-dependent.

A modeling boundary is not automatically a physical discontinuity.

### 6.4 Open system

An open system permits at least one declared exchange across its boundary.

### 6.5 Closed model approximation

A closed model approximation suppresses or neglects selected exchanges for a declared calculation.

A closed approximation does not establish that the complete represented physical process is fundamentally closed.

## 7. State and State Space

### 7.1 State

A state is the complete set of variables required by a declared model to determine its permitted evolution under the model contract.

A state must always be defined relative to:

- a system;
- a state space;
- a time or execution index;
- a declared evolution rule.

### 7.2 Continuous state space

The continuous state space is denoted by:

`X`

A continuous state at time `t` is denoted by:

`X(t) ∈ X`

The continuous state may contain:

- positions;
- velocities;
- amplitudes;
- phases;
- energies;
- forces;
- stresses;
- coupling variables;
- delay variables;
- memory variables;
- structural descriptors.

### 7.3 Discrete state space

A discrete state space contains a finite or countable set of state values.

The primary TR-EIF discrete state set is the balanced ternary set:

`T = {-1, 0, 1}`

### 7.4 Composite state

A complete TR-EIF model may use a composite state containing continuous, ternary, topological, and historical components.

A generic composite state may be written as:

`S(t) := (X(t), σ(t), G(t), H(t))`

where:

- `X(t)` is the continuous state;
- `σ(t)` is the ternary state configuration;
- `G(t)` is the interaction topology;
- `H(t)` is the declared history or memory state.

Not every TR-EIF model must use every component.

Omitted components must not be referenced implicitly.

## 8. Balanced Ternary State

### 8.1 Ternary state set

The balanced ternary state set is:

`T = {-1, 0, 1}`

The notation must always appear as:

`-1/0/1`

The form `-1/0/+1` is not used.

### 8.2 Local ternary state

The ternary state of component `i` at time `t` is:

`σ_i(t) ∈ T`

The complete ternary configuration for `N` components is:

`σ(t) ∈ T^N`

### 8.3 Negative state

The state `-1` represents the negative branch of the declared ternary relation.

Its exact physical or computational meaning must be defined by the relevant model contract.

It must not be assigned a universal physical meaning across all applications.

### 8.4 Active neutral state

The state `0` is the active neutral state.

It may perform:

- balancing;
- mediation;
- routing;
- damping;
- transition staging;
- retained-state storage;
- capacity regulation;
- conflict resolution;
- temporary stabilization.

The state `0` is not:

- missing data;
- an undefined value;
- an empty state;
- a passive absence;
- an automatic arithmetic zero in every context.

### 8.5 Positive state

The state `1` represents the positive branch of the declared ternary relation.

Its exact physical or computational meaning must be defined by the relevant model contract.

### 8.6 Ternary transition

A ternary transition is an ordered state change:

`σ_i(t_a) → σ_i(t_b)`

where `t_b > t_a`.

### 8.7 Opposite-state transition

An opposite-state transition changes between `-1` and `1`.

Direct opposite-state transitions are forbidden.

Invalid transitions:

`-1 → 1`

`1 → -1`

Valid opposite-state paths:

`-1 → 0 → 1`

`1 → 0 → -1`

Each arrow represents a separate transition event.

### 8.8 Neutral retention

Neutral retention occurs when a component remains in state `0` for a finite interval or number of execution steps.

Neutral retention may be required by:

- damping;
- unresolved competition;
- capacity limits;
- delayed completion;
- routing;
- stability conditions;
- transition guards.

## 9. Atomic and Interatomic Notation

### 9.1 Atomic-site set

The atomic-site set is:

`V = {1, 2, ..., N}`

where `N` is the number of represented atomic sites.

### 9.2 Atomic species

The species or identity label of site `i` is:

`z_i`

The domain of `z_i` must be declared by the model.

It may represent:

- atomic number;
- element label;
- species index;
- learned embedding key;
- another explicitly declared identity representation.

### 9.3 Position

The spatial position of site `i` at time `t` is:

`x_i(t) ∈ ℝ^d`

where `d` is the spatial dimension.

For ordinary three-dimensional representation:

`d = 3`

### 9.4 Velocity

The velocity of site `i` is:

`v_i(t) ∈ ℝ^d`

### 9.5 Force

The force acting on site `i` is:

`f_i(t) ∈ ℝ^d`

### 9.6 Mass

The mass assigned to site `i` is:

`m_i ∈ ℝ₊`

A mass value must include unit and provenance information.

### 9.7 Relative displacement

The relative displacement from site `i` to site `j` is:

`x_ij(t) := x_j(t) - x_i(t)`

### 9.8 Pair distance

The pair distance between sites `i` and `j` is:

`d_ij(t) := ||x_ij(t)||`

The norm must be declared when a non-Euclidean metric is used.

### 9.9 Local environment

The local environment of site `i` is denoted by:

`N_i(t)`

A local environment may include:

- neighboring site identities;
- relative positions;
- distances;
- angular relations;
- local state variables;
- interaction-channel labels;
- boundary information.

The rule that determines membership in `N_i(t)` must be explicit.

### 9.10 Interaction edge

An interaction edge is an ordered or unordered relation between two sites.

An edge is written as:

`e_ij ∈ E`

The repository must declare whether the interaction graph is directed or undirected.

## 10. Graph and Topology Notation

### 10.1 Interaction graph

An interaction graph is written as:

`G(t) = (V, E(t))`

where:

- `V` is the node or atomic-site set;
- `E(t)` is the interaction-edge set.

The graph may be static or time-dependent.

### 10.2 Edge weight

The weight associated with edge `e_ij` is:

`w_ij(t)`

An edge weight may represent:

- coupling strength;
- interaction magnitude;
- geometric weight;
- probability;
- routing capacity;
- learned coefficient.

Its meaning, domain, and units must be declared.

### 10.3 Adjacency relation

The adjacency relation is represented by:

`A_ij(t)`

The value domain of `A_ij(t)` must be declared.

It may be:

- binary;
- weighted;
- ternary;
- continuous;
- channel-dependent.

### 10.4 Topology

Topology means the declared pattern of relations among system components.

Topology is not identical to geometry.

Two configurations may share topology while differing geometrically.

Two configurations may share geometry locally while differing topologically.

### 10.5 Dynamic topology

A dynamic topology permits the relation set `E(t)` to change with time, state, scale, or structural transition.

Every topology-changing rule must preserve declared graph invariants or report their violation.

## 11. Continuous Oscillatory Notation

### 11.1 Oscillatory component

An oscillatory component is indexed by `i`.

It may contain amplitude, phase, frequency, and additional internal variables.

### 11.2 Amplitude

The amplitude of component `i` is:

`a_i(t) ∈ ℝ₊`

Amplitude is not assumed constant unless the model explicitly imposes that condition.

### 11.3 Phase

The phase of component `i` is:

`θ_i(t) ∈ 𝕊¹`

A numeric implementation may represent phase over a selected interval such as:

`[0, 2π)`

or:

`(-π, π]`

The chosen interval and wrap rule must be declared.

### 11.4 Angular frequency

The angular frequency of component `i` is:

`ω_i(t)`

Frequency may be:

- intrinsic;
- instantaneous;
- effective;
- externally imposed;
- state-dependent;
- scale-dependent.

These meanings must not be conflated.

### 11.5 Relative phase

The relative phase between components `i` and `j` is:

`Δθ_ij(t) := wrap(θ_j(t) - θ_i(t))`

The `wrap` operation maps the phase difference into the declared phase interval.

### 11.6 Coupling strength

The coupling strength from component `j` to component `i` is:

`K_ij(t)`

The repository must declare:

- whether coupling is directed;
- whether coupling is symmetric;
- its units;
- its state dependence;
- its spatial dependence;
- its delay dependence.

### 11.7 Detuning

Detuning is the declared difference between relevant frequencies.

A generic pair detuning may be written as:

`Δω_ij(t) := ω_j(t) - ω_i(t)`

Detuning does not alone determine whether resonance or synchronization occurs.

## 12. Resonance Terminology

### 12.1 Mode

A mode is a distinguishable pattern of dynamic organization supported by the declared system and boundary conditions.

A mode may be:

- local;
- collective;
- spatial;
- temporal;
- structural;
- propagating;
- standing;
- damped;
- unstable.

### 12.2 Resonant relation

A resonant relation is a selective dynamic relation among internal modes, external excitation, geometry, coupling, propagation, phase, and dissipation.

A resonant relation must not be reduced automatically to equality of two scalar frequencies.

### 12.3 Resonant response

A resonant response is the system response associated with a declared resonant relation.

The response may appear through:

- amplitude change;
- phase organization;
- selective transmission;
- selective suppression;
- energy exchange;
- mode activation;
- mode competition;
- topology change;
- structural transition.

### 12.4 Resonance window

A resonance window is a finite region in a declared parameter or state space within which a specified resonant relation or structural response occurs.

A resonance window is denoted by:

`W_R ⊂ P`

where:

- `P` is the declared parameter or state space;
- `W_R` is the resonance-window region.

The coordinates of `P` must be stated explicitly.

### 12.5 Resonance-window boundary

The boundary of a resonance window is:

`∂W_R`

Crossing `∂W_R` does not automatically imply a phase transition.

The resulting behavior depends on the declared model and structural conditions.

## 13. Synchronization, Phase Locking, and Coherence

### 13.1 Synchronization

Synchronization is the development or preservation of a defined temporal relation among dynamic components.

The synchronized relation must be stated explicitly.

### 13.2 Phase locking

Phase locking occurs when a declared phase relation remains bounded or constant over a declared interval.

Phase locking may involve:

- zero phase difference;
- non-zero fixed phase difference;
- rational frequency relation;
- clustered phase organization.

### 13.3 Coherence

Coherence is the preservation of a declared relation across time, space, scale, or transformation.

Coherence does not require uniformity.

A coherent configuration may contain:

- differentiated phases;
- counterphase organization;
- multiple synchronized clusters;
- spatial gradients;
- distinct local modes.

### 13.4 Coherence measure

A coherence measure is denoted generically by:

`c(t)`

The range, normalization, interpretation, and calculation of `c(t)` must be declared by the specific model.

No universal physical meaning is assigned to an undefined coherence scalar.

## 14. Energy and Dissipation Notation

### 14.1 Energy

A generic energy quantity is denoted by:

`E(t)`

A specific energy term must identify:

- physical meaning;
- units;
- included degrees of freedom;
- reference level;
- sign convention.

### 14.2 Local energy

The energy associated with component or site `i` is:

`E_i(t)`

A local-energy decomposition must declare whether the decomposition is unique, approximate, or model-dependent.

### 14.3 Energy transfer

Energy transferred from component `j` to component `i` over a declared interval is denoted by:

`ΔE_j→i`

The direction convention must remain consistent.

### 14.4 Dissipation

Dissipation is irreversible redistribution of organized energy into other represented or environmental degrees of freedom.

A generic dissipation rate is denoted by:

`D(t)`

The units and included channels must be declared.

### 14.5 Numerical loss

Numerical loss is error produced by discretization, truncation, rounding, unstable integration, insufficient resolution, or implementation defects.

Numerical loss is not physical dissipation.

The two quantities must be reported separately.

### 14.6 Saturation

Saturation is a state-dependent limitation that prevents indefinite growth of a declared variable or response.

A saturation mechanism must identify:

- affected variable;
- activation condition;
- limiting rule;
- reversibility;
- hysteresis where present.

## 15. Delay, Propagation, and Memory Notation

### 15.1 Delay

A delay is denoted by:

`τ`

A pair-dependent delay may be denoted by:

`τ_ij`

A delay may represent:

- propagation time;
- response latency;
- control latency;
- structural relaxation time;
- measurement delay;
- discrete execution delay.

Its meaning and units must be declared.

### 15.2 Delayed state

A delayed state is written as:

`X(t - τ)`

The model must specify how the state is defined when `t - τ` precedes the initial simulation time.

### 15.3 History state

The history available at time `t` is denoted by:

`H(t)`

A history object may contain a finite interval of prior states:

`H(t) = {X(s) | s ∈ [t - τ_max, t]}`

where `τ_max` is the maximum required delay.

### 15.4 Memory

Memory is retained dependence on previous system evolution.

Memory may be represented through:

- delayed states;
- history buffers;
- internal memory variables;
- hysteresis variables;
- path-dependent topology;
- inherited structural descriptors.

### 15.5 Propagation

Propagation is the finite transmission of a disturbance, state influence, interaction, or energy redistribution through space or topology.

Propagation speed is denoted generically by:

`u_p`

The represented propagation law must identify its medium, scale, and boundary conditions.

## 16. Mapping and Operator Notation

### 16.1 Mapping

A mapping from domain `A` to codomain `B` is written as:

`F: A → B`

Every mapping must declare:

- domain;
- codomain;
- input;
- output;
- parameter dependence;
- regularity assumptions where required.

### 16.2 Operator

An operator acts on a mathematical object and returns another object.

An operator is denoted generically by:

`L`

Its domain and codomain must be specified.

### 16.3 Continuous evolution map

A continuous evolution map may be denoted by:

`Φ_t: X → X`

where `Φ_t` maps an initial continuous state to the state after elapsed time `t`.

This notation does not assume that every model forms a reversible flow.

### 16.4 Discrete update map

A discrete update map is denoted by:

`U: S_n → S_n+1`

The update order, retained values, and failure states must be explicit.

### 16.5 Continuous-to-ternary projection

A continuous-to-ternary mapping is denoted by:

`Π: X → T^N`

The projection must define:

- input variables;
- decision rule;
- active-neutral region;
- threshold provenance;
- uncertainty handling;
- transition timing;
- retained information;
- discarded information.

### 16.6 Ternary-conditioned continuous update

A ternary-conditioned continuous update is denoted by:

`Γ: X × T^N → X`

The mapping must state how ternary states affect continuous evolution.

### 16.7 Observable map

An observable map is denoted by:

`O: S → Y`

where:

- `S` is the complete represented state space;
- `Y` is the observable output space.

The output `O(S)` is not automatically identical to the complete internal state.

## 17. Symmetry and Equivariance Notation

### 17.1 Symmetry group

A declared symmetry group is denoted by:

`G_sym`

The group must be identified explicitly.

Possible classes include:

- translations;
- rotations;
- reflections;
- permutations;
- combined transformations.

### 17.2 Group element

A transformation element is denoted by:

`g ∈ G_sym`

### 17.3 Input action

The action of `g` on input space `X` is denoted by:

`ρ_X(g)`

### 17.4 Output action

The action of `g` on output space `Y` is denoted by:

`ρ_Y(g)`

### 17.5 Invariant mapping

A mapping `F: X → Y` is invariant under the declared action when:

`F(ρ_X(g)x) = F(x)`

for every permitted `g` and `x`.

### 17.6 Equivariant mapping

A mapping `F: X → Y` is equivariant under the declared input and output actions when:

`F(ρ_X(g)x) = ρ_Y(g)F(x)`

for every permitted `g` and `x`.

An equivariance claim is incomplete unless both actions are defined.

### 17.7 Symmetry breaking

Symmetry breaking is a transition from a state or regime preserving a declared symmetry to one preserving a smaller symmetry set or a different structural relation.

Symmetry breaking must not be inferred from visual asymmetry alone.

## 18. Structural Work and Structural Transition

### 18.1 Declared form

A declared form is a dynamically maintained organization identified by a set of relations and invariants.

The form is denoted generically by:

`F_k`

where `k` identifies the structural regime.

### 18.2 Structural work

Structural work is dynamic activity that changes the capacity of a declared form to maintain, reproduce, or transform its organization.

A generic structural-work quantity is denoted by:

`W_s`

The sign of structural work is always relative to a declared form.

### 18.3 Positive structural work

Positive structural work relative to form `F_k` increases the capacity of `F_k` to maintain or reproduce its declared organization.

### 18.4 Negative structural work

Negative structural work relative to form `F_k` decreases the capacity of `F_k` to maintain or reproduce its declared organization.

### 18.5 Structural transition

A structural transition is denoted by:

`F_k → F_k+1`

The transition must be defined by changes in declared structural variables or relations.

A scalar threshold crossing alone is insufficient unless the model proves that it uniquely identifies the structural change.

### 18.6 Constructive transition

A constructive transition increases a declared structural capacity relative to the selected evaluation criterion.

### 18.7 Degradative transition

A degradative transition decreases a declared structural capacity relative to the selected evaluation criterion.

A degradative result may still form a stable attractor.

### 18.8 Transition trajectory

The transition trajectory is the sequence of states connecting the pre-transition and post-transition regimes.

It may include:

- neutral ternary staging;
- mode competition;
- topology modification;
- symmetry change;
- energy redistribution;
- transient instability;
- delayed stabilization.

## 19. Recursive Inheritance

### 19.1 Inherited state

The inherited state passed from cycle `n` to cycle `n + 1` is denoted by:

`I_n→n+1`

It may contain:

- topology;
- residual stress;
- defects;
- phase relations;
- mode populations;
- local environments;
- coupling weights;
- hysteresis variables;
- dissipation pathways;
- retained ternary states.

### 19.2 Recursive cycle

A recursive dynamic cycle is represented by:

`S_n → W_s,n → W_R,n → F_n+1 → I_n→n+1 → S_n+1`

where:

- `S_n` is the state entering cycle `n`;
- `W_s,n` is accumulated structural work;
- `W_R,n` is the reached resonance-window condition;
- `F_n+1` is the resulting structural form;
- `I_n→n+1` is the inherited state;
- `S_n+1` is the state entering the next cycle.

### 19.3 Path dependence

Path dependence occurs when future evolution depends on the trajectory by which the current observable state was reached.

Two systems with equal instantaneous observables may differ in future evolution when their inherited states differ.

## 20. Observation and Projection

### 20.1 Observable

An observable is a declared output obtained from the represented state by a measurement or projection rule.

An observable is denoted by:

`y(t) ∈ Y`

### 20.2 Projection

A projection selects or compresses information from a larger state representation.

A projection is not assumed lossless.

### 20.3 Observation interval

The observation interval is denoted by:

`Δt_obs`

The relation between process time scale and observation interval affects whether the process appears:

- resolved;
- instantaneous;
- stationary;
- averaged;
- aliased.

### 20.4 Process time scale

A characteristic process time scale is denoted by:

`τ_proc`

The relation:

`τ_proc << Δt_obs`

indicates that the internal process may appear instantaneous at the selected observation resolution.

The relation:

`τ_proc >> Δt_obs`

indicates that the process may appear static over the selected observation interval.

### 20.5 Instrumental projection

An instrumental projection is the output produced by a measurement chain with finite:

- bandwidth;
- sampling rate;
- spatial resolution;
- temporal resolution;
- sensitivity;
- dynamic range;
- averaging window.

The instrumental output must not be identified silently with the complete physical process.

## 21. Numerical and Execution Notation

### 21.1 Time step

The numerical time step is:

`Δt`

Its value, units, and provenance must be declared.

### 21.2 Numerical state

The numerical approximation of state `X(t_n)` is:

`X_n`

The distinction between exact and numerical states must be preserved.

### 21.3 Numerical error

A generic numerical error is:

`ε_num`

The error definition and norm must be declared.

### 21.4 Tolerance

A numerical tolerance is:

`ε_tol`

A tolerance is a computational parameter, not a physical constant.

### 21.5 Random seed

A random seed is denoted by:

`seed`

A deterministic execution using stochastic components must record the seed and random-number-generator identity.

### 21.6 Execution trace

An execution trace is denoted by:

`Trace`

A trace must identify:

- input state;
- configuration;
- parameter values;
- state updates;
- transition events;
- invariant states;
- errors;
- outputs;
- schema version;
- software version.

### 21.7 Replay

A replay is a repeated execution using the same declared execution contract.

A deterministic replay must reproduce the declared reference outputs within the exact or explicitly bounded comparison rule.

## 22. Parameter Provenance

Every parameter must be assigned a provenance class.

The permitted provenance classes are:

- `PRIMARY_SOURCE`
- `DERIVED`
- `CALIBRATED`
- `BENCHMARK`
- `AUTHOR_DEFINED`
- `TEST_FIXTURE`
- `REQUIRES_SOURCE`
- `REQUIRES_TEST`

### 22.1 Primary-source parameter

`PRIMARY_SOURCE` identifies a value taken from a verified primary source.

### 22.2 Derived parameter

`DERIVED` identifies a value calculated from declared inputs and equations.

### 22.3 Calibrated parameter

`CALIBRATED` identifies a value obtained through a documented calibration procedure.

### 22.4 Benchmark parameter

`BENCHMARK` identifies a value selected for a declared benchmark configuration.

### 22.5 Author-defined parameter

`AUTHOR_DEFINED` identifies a value introduced as part of a TR-EIF model or contract.

### 22.6 Test fixture

`TEST_FIXTURE` identifies a value used solely for software, schema, regression, or invariant testing.

### 22.7 Requires source

`REQUIRES_SOURCE` identifies a value that must not be treated as scientifically established until its source is verified.

### 22.8 Requires test

`REQUIRES_TEST` identifies a value or relation that requires numerical or empirical validation.

## 23. Logical Statement Classes

TR-EIF separates the following statement classes.

### 23.1 Definition

A definition assigns an exact meaning to a term or symbol.

### 23.2 Assumption

An assumption declares a condition accepted for a specific model or derivation.

### 23.3 Axiom

An axiom is a foundational statement adopted within the formal framework.

### 23.4 Lemma

A lemma is a derived result used to establish another result.

### 23.5 Theorem

A theorem is a statement derived from declared definitions, axioms, assumptions, and prior results.

### 23.6 Corollary

A corollary follows directly from an established result.

### 23.7 Hypothesis

A hypothesis is a testable statement not yet established by proof or evidence.

### 23.8 Numerical result

A numerical result is produced by a declared implementation and execution configuration.

### 23.9 Empirical result

An empirical result is obtained from measurement or experiment under declared conditions.

These statement classes must not be merged into one undifferentiated narrative.

## 24. Reserved Symbols

The following symbols are reserved by this chapter.

| Symbol | Meaning |
|---|---|
| `T` | Balanced ternary state set `{-1, 0, 1}` |
| `σ_i(t)` | Local ternary state |
| `σ(t)` | Complete ternary configuration |
| `X` | Continuous state space |
| `X(t)` | Continuous state |
| `S(t)` | Composite system state |
| `Y` | Observable output space |
| `V` | Atomic-site or graph-vertex set |
| `E` | Interaction-edge set |
| `G(t)` | Interaction graph |
| `G_sym` | Declared symmetry group |
| `x_i(t)` | Position of site `i` |
| `v_i(t)` | Velocity of site `i` |
| `f_i(t)` | Force on site `i` |
| `m_i` | Mass assigned to site `i` |
| `z_i` | Atomic species or identity label |
| `N_i(t)` | Local environment of site `i` |
| `a_i(t)` | Oscillatory amplitude |
| `θ_i(t)` | Oscillatory phase |
| `ω_i(t)` | Angular frequency |
| `K_ij(t)` | Coupling strength |
| `τ` | Delay |
| `H(t)` | History or memory state |
| `W_R` | Resonance-window region |
| `W_s` | Structural work |
| `F_k` | Declared structural form |
| `I_n→n+1` | Inherited state |
| `Π` | Continuous-to-ternary projection |
| `Γ` | Ternary-conditioned continuous update |
| `O` | Observable mapping |
| `ρ_X` | Input transformation action |
| `ρ_Y` | Output transformation action |
| `ε_num` | Numerical error |
| `ε_tol` | Numerical tolerance |

A later file must not assign an incompatible meaning to a reserved symbol without formally revising this document.

## 25. Semantic Separation Rules

The following terms must remain distinct:

- state and observable;
- physical system and computational representation;
- atom and atomic descriptor;
- local environment and encoded local environment;
- interaction and interaction model;
- energy transfer and numerical loss;
- resonance and synchronization;
- synchronization and phase locking;
- coherence and uniformity;
- stability and staticity;
- resonance window and single frequency;
- structural transition and ordinary state update;
- physical time and execution step;
- system boundary and physical discontinuity;
- continuous value and ternary state;
- neutral state and missing value;
- model output and empirical measurement;
- hypothesis and validated result.

## 26. Definition Consistency Requirements

Every later TR-EIF file must satisfy the following requirements:

1. Every symbol is defined before use.

2. Every state variable has a declared domain.

3. Every mapping has a declared domain and codomain.

4. Every physical quantity has declared units where applicable.

5. Every threshold has provenance.

6. Every ternary-state meaning is defined by its model contract.

7. The active state `0` remains operationally active.

8. Direct `-1 ↔ 1` transitions remain forbidden.

9. Continuous and discrete variables remain separately represented.

10. Every equivariance claim defines its transformation actions.

11. Every observable identifies its source state and projection rule.

12. Every numerical result identifies its execution configuration.

13. Every inherited variable identifies the cycle or transition from which it originates.

14. Every overloaded symbol is disambiguated locally.

15. No undefined abbreviation is introduced.

## 27. Foundational Notation Statement

TR-EIF uses explicit notation to preserve the distinction between:

`physical configuration`

`→ continuous dynamic state`

`→ balanced ternary state`

`→ structural and equivariant mappings`

`→ observable projection`

`→ deterministic trace`

The notation defined in this document is authoritative for subsequent TR-EIF mathematical, computational, validation, and publication artifacts.
