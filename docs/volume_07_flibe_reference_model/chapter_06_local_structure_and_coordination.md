
# Local Structure and Coordination

## 1. Scope and Material State

This chapter specifies local structural observables for the LiF–BeF2 reference system in TR-EIF. It connects ordered Li/Be/F atomic configurations, three-dimensional interaction geometry, species-resolved graph coordination, angular and pair correlations, structural-network descriptors, experimental scattering and spectroscopy, and continuous resonance-conditioned interatomic computation.

A structural observation is associated with its composition, temperature, pressure, physical state, spatial and temporal sampling, geometrical convention, numerical method, and source identity. The system class is an open nonlinear dissipative dynamical system; its structural state can evolve with mechanical motion, material exchange, boundary conditions, and time-dependent interactions.

The executable local-structure chain is:

`FLiBeConfiguration → directed InteractionGraph → FLiBeCoordinationState → resonance parameterization and descriptor → FLiBe TR-EIP conditioned energy`.

Pair distributions, angular statistics, molecular-network descriptors, scattering responses, and spectroscopic assignments are defined by their individually selected structural operators.

## 2. Species and Composition Coordinates

`FLiBeSpecies` specifies Li, Be, and F in canonical order. `FLiBeComposition` describes the component fractions `x_LiF` and `x_BeF2`, satisfying:

`x_LiF >= 0`, `x_BeF2 >= 0`, `x_LiF + x_BeF2 = 1`.

The exact formula-unit ratio `2 LiF : 1 BeF2` gives the atomic inventory ratio:

`N_Li : N_Be : N_F = 2 : 1 : 4`.

The nominal `67 mol% LiF : 33 mol% BeF2` mixture uses component fractions `(0.67, 0.33)`. The Vidrio 2022 experimental register reports an ICP-MS specimen composition of `33.58(5) mol% BeF2`. The source composition remains attached to each local-structure observation.

`FLiBeConfiguration` wraps an `AtomicConfiguration` with a tuple of Li/Be/F species and matching three-dimensional Cartesian positions. Its `composition()` method derives component fractions under the exact binary inventory relation `N_F = N_Li + 2 N_Be`.

## 3. Three-Dimensional Reference Geometry

For atom `i`, let `r_i in R^3` denote its Cartesian position. A configuration may supply a nonsingular simulation cell with matrix `B = [a b c]` and a Boolean periodic-axis tuple `P`.

For source `i`, receiver `j`, and lattice image index `k_ij in Z^3`, define:

`d_ij(k_ij) = r_j + B k_ij - r_i`.

`r_ij(k_ij) = |d_ij(k_ij)|`.

`e_ij(k_ij) = d_ij(k_ij) / r_ij(k_ij)` for positive separation.

`InteractionEdge` records the source, receiver, and three-integer image tuple. `evaluate_edge_geometry` reconstructs the displacement, distance, and unit direction for its recorded image. Cell geometry, axis periodicity, atom order, and units are included in the observable record.

## 4. Periodic Image Selection

The executable `minimum_image` operation converts an initial pair displacement `d = r_j - r_i` into fractional components:

`u = B^(-1) d`.

For each lattice axis `l`, the selected image component is:

`k_l = -floor(u_l + 0.5)` on a periodic axis.

`k_l = 0` on a nonperiodic axis.

The returned displacement is:

`d_selected = B (u + k)`.

This is the implemented componentwise fractional-wrapping rule, including its half-cell tie convention. For a skewed lattice, the Euclidean metric `B^T B` also defines a separate shortest-image optimization. A structure calculation identifies the image-selection convention applied to its source geometry.

## 5. Directed Cutoff Interaction Graph

`build_cutoff_graph(configuration, cutoff)` accepts a finite positive radial cutoff `r_c`. For each ordered pair of distinct atomic indices `(i,j)`, it calculates the selected displacement and includes one directed edge when:

`|d_ij|^2 <= r_c^2`.

The builder visits source and receiver indices in ascending order. For each ordered atomic pair it records the selected image index, producing a deterministic directed graph with `node_count = N`.

`InteractionGraph` stores a tuple of directed `InteractionEdge` records. It validates node-index ranges and uniqueness of complete `(source, receiver, image)` records. Its `incoming_edges(j)` and `outgoing_edges(i)` operations retain the edge orientation selected for the graph.

The graph is a defined computational representation of geometric adjacency. Chemical association, pair-correlation, and experimental coordination are represented by their corresponding structural mappings and criteria.

## 6. Species-Resolved Incoming Coordination

For receiver atom `j` and species `s in {Li, Be, F}`, define the graph-relative incoming count:

`z_(j,s) = sum_(edge i→j in G) indicator(species(i) = s)`.

The atomwise total is:

`z_j = z_(j,Li) + z_(j,Be) + z_(j,F)`.

`build_flibe_coordination_state(configuration, graph)` implements these counts using `graph.incoming_edges(j)` and the species of each edge source. The function requires an `FLiBeConfiguration`, an `InteractionGraph`, equal atom/node counts, and distinct source and receiver indices for every contributing edge.

An isolated graph node has the three valid count values `(0,0,0)`. Count values are nonnegative integers and remain attached to the receiver's original atomic index.

## 7. Executable Atomic Coordination Record

`FLiBeAtomCoordination` is an immutable dataclass storing:

- `atom_index`: nonnegative integer atomic index;
- `species`: the canonical `FLiBeSpecies` member of the receiver;
- `lithium_neighbors`: nonnegative integer count;
- `beryllium_neighbors`: nonnegative integer count;
- `fluorine_neighbors`: nonnegative integer count.

Its `total_neighbors` property returns the sum of these three fields. Its `species_coordination` property returns the canonical ordered tuple of species/count pairs for Li, Be, and F.

The count fields accept integers excluding Boolean values. A count has the graph-neighbor interpretation specified by its `InteractionGraph` and input configuration; its integer value does not encode a retained balanced-ternary execution state.

## 8. Coordination-State Collection

`FLiBeCoordinationState(atoms=...)` stores a nonempty immutable tuple of `FLiBeAtomCoordination` records. It requires consecutive `atom_index` values starting at zero.

The `atom_count` property returns its tuple cardinality, and `total_neighbor_records` sums the atomwise totals. For a state built from a supplied graph with distinct source and receiver on every edge:

`sum_(j=0)^(N-1) z_j = graph.edge_count`.

The builder also preserves the receiver-species order of the supplied `FLiBeConfiguration`. Reordering the input graph's edge tuple leaves the species-resolved integer coordination state unchanged.

## 9. Periodic-Image Multiplicity

An `InteractionGraph` can contain two edges with the same source and receiver but different image indices. The coordination builder counts each incoming edge record separately.

For example, edges `(Li_0 → F_1, image=(0,0,0))` and `(Li_0 → F_1, image=(1,0,0))` give:

`z_(F_1,Li) = 2`.

This example has one source-atom identity and two directed image records. `build_cutoff_graph` selects one image per ordered atomic pair; an explicitly supplied graph may encode additional image-resolved records. The representation used for a structural statistic specifies whether it counts graph edges, unique atom identities, or all selected periodic images.

## 10. Directed Coordination Example

The existing invariant fixture uses the species tuple:

`S = (Li, Be, F, F)`.

Its eight directed edges are:

`0→1, 2→1, 3→1, 1→0, 2→0, 0→2, 1→2, 0→3`.

The resulting graph-relative coordination is:

| Receiver index | Species | Li neighbors | Be neighbors | F neighbors | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| `0` | Li | 0 | 1 | 1 | 2 |
| `1` | Be | 1 | 0 | 2 | 3 |
| `2` | F | 1 | 1 | 0 | 2 |
| `3` | F | 1 | 0 | 0 | 1 |

The total incoming edge count is `2 + 3 + 2 + 1 = 8`, equal to `graph.edge_count`. The fixture is constructed by `_reference_graph()` in `tests/invariants/test_flibe_coordination_invariants.py`.

## 11. Species-to-Species Coordination Matrix

For a source species `s` and receiver species `t`, define the directed population count:

`C_(s→t) = sum_(j:species(j)=t) z_(j,s)`.

For receiver population `N_t > 0`, define its species-average incoming coordination:

`zbar_(t,s) = C_(s→t) / N_t`.

The complete species-resolved matrix is indexed by ordered pairs `(s,t)`. For a graph whose off-diagonal directed edges occur in reciprocal pairs, the counts satisfy `C_(s→t) = C_(t→s)` for distinct species under the corresponding image and counting conventions.

The chosen averaging ensemble, source and receiver populations, directed-edge convention, and time samples accompany the resulting matrix.

## 12. Cutoff and Neighborhood Dependence

Coordination counts are functions of the graph-building rule:

`z_(j,s) = z_(j,s)(R, B, P, r_c, G_policy)`.

A parameter study can evaluate a fixed configuration under a declared increasing sequence of positive cutoffs. The record contains every cutoff, the resulting directed edges, and the atomwise coordination vectors.

For trajectory analysis, graph evaluations occur at selected mechanical times. A neighbor-list snapshot can retain candidate pairs within `r_search = r_c + skin`; the current interaction graph is recovered from the retained candidates under the selected rebuild rule and actual interaction cutoff.

The existing `velocity_verlet_step` constructs its interaction graphs directly at mechanical endpoints. The separately exposed neighbor-list API supports caller-specified graph reuse and rebuilding.

## 13. Species-Resolved Radial Distribution

For a homogeneous isotropic structural ensemble with species number density `rho_t = N_t/V`, define the partial radial distribution `g_(s,t)(r)` through the conditional density of species `t` at separation `r` from a reference species `s`.

For a shell `[r, r+Delta_r)` of volume `Delta_V_shell`, an ordered distinct-pair histogram `H_(s,t)` can be normalized as:

`g_(s,t)(r) ≈ H_(s,t)(r,Delta_r) / (N_s rho_t Delta_V_shell)`.

For sufficiently narrow shells:

`Delta_V_shell ≈ 4 pi r^2 Delta_r`.

The same-species finite-population normalization, pair-ordering convention, periodic cell treatment, and source ensemble are declared with the histogram. This representation is a radial statistical operator applied to stored configurations or trajectories.

## 14. Radial Coordination Integral

For the same reference state and a selected radial integration boundary `r_c`, define:

`N_(s,t)(r_c) = 4 pi rho_t integral_(0→r_c) r^2 g_(s,t)(r) dr`.

The integration window, pair-count convention, density normalization, and sampling ensemble determine this radial coordination statistic. A numerical estimator additionally specifies radial binning and quadrature.

The graph-relative count `z_(j,t)` is constructed directly from a selected graph. The radial integral is constructed from a pair-distribution estimator. Their relationship is evaluated through an explicit common cutoff and pair-count mapping when both are computed for a corresponding state and ensemble.

## 15. Be–F Coordination Geometry

For a selected Be center `b` and two chosen F neighbors `f_1` and `f_2`, define the Be-to-F displacement vectors:

`u_1 = d_(b,f_1)`.

`u_2 = d_(b,f_2)`.

For positive distances, the F–Be–F angle is:

`theta_(f_1,b,f_2) = arccos[(u_1 · u_2)/(|u_1| |u_2|)]`.

Displacements use the declared periodic-image selections. A structural-angle distribution identifies the central species, neighbor-selection rule, angular-bin convention, and sample times. The ideal regular-tetrahedron angle has cosine `-1/3`, corresponding to approximately `109.47 degrees`.

An observed four-F graph coordination for a Be center, a geometric tetrahedral classification, and a spectroscopic BeF4 structural assignment are separately recorded quantities with their respective criteria.

## 16. Fluoroberyllate Units and Bridging Fluorine

A selected Be–F structural association rule can represent tetrahedral BeF4 units, shared-fluorine connections, and larger connected Be–F formations. A source-defined chemical-association operator may use distances, angles, electronic information, temporal persistence, or an identified combination of these inputs.

For an association graph `G_BeF`, let `b_F(j)` be the number of distinct associated Be centers adjacent to fluorine atom `j`. A local connectivity classification can distinguish terminal and multiply connected F environments by their declared values of `b_F(j)`.

The spectroscopy source Fu et al. (2023) reports structural assignments involving BeF4, Be2F7, Be3F10, and extended fluoroberyllate structures. The computational reference Salanne et al. (2006) examines composition-dependent Be–F network formation. Each structural assignment uses the source's chemical model and physical-state conditions.

## 17. Connected Structural Networks

From a declared Be–F association graph, a network descriptor may contain connected-component membership, component sizes, Be–F coordination, branching indices, and cycles or ring statistics.

For a component `A`, its species-resolved inventory is:

`N_s(A) = count{i in A | species(i) = s}`.

A spatial network record specifies the edge or association criterion, periodic-image handling, cell topology, component-wrapping convention, and atomic identities. Time-dependent network calculations additionally identify the association persistence and component correspondence across successive configurations.

These descriptors can be introduced as separately typed structural variables for a selected TR-EIF material realization.

## 18. Neutron and X-Ray Structural Observables

A reciprocal-space species-density mode for species `s` can be written:

`rho_s(q) = sum_(i:species(i)=s) exp(i q · r_i)`.

For a specified finite ensemble and normalization, a partial reciprocal correlation is:

`S_(s,t)(q) = <delta_rho_s(q) delta_rho_t(-q)> / sqrt(N_s N_t)`.

The total neutron or X-ray observable combines source-defined partial contributions with the relevant scattering lengths or atomic form factors. The experimental record specifies the scattering-vector axis, temperature, composition, background subtraction, normalization, instrumental resolution, and processing procedure.

The source Fayfar et al. (2024), DOI `10.1103/PRXEnergy.3.013001`, reports liquid FLiBe neutron and X-ray total scattering together with AIMD and neural-network molecular-dynamics structural calculations.

## 19. Reciprocal-to-Real-Space Transformation

For a homogeneous isotropic material and a declared partial-structure-factor convention, the relationship between a pair distribution and reciprocal correlation can be represented by a spherical Fourier transform, for example:

`S_(s,t)(q) - delta_(s,t) = 4 pi sqrt(rho_s rho_t) integral_(0→infinity) r^2 [g_(s,t)(r)-1] sin(qr)/(qr) dr`.

This expression uses one specified normalization and requires consistent species densities, diagonal terms, and Fourier conventions. A source or model mapping records the adopted partial-structure-factor definition, radial window, reciprocal axis, termination handling, and numerical transform.

The resulting structural comparison associates its measured or calculated reciprocal observable with the corresponding real-space quantity through that recorded transformation.

## 20. High-Temperature NMR and Local Structure

The source Fu et al. (2023), DOI `10.1039/D3CP01096A`, reports in situ high-temperature NMR and solidified-salt spectroscopy for LiF–BeF2 compositions.

A structural NMR record identifies the observed isotope or nucleus, chemical-shift reference, experimental temperature, composition, spectral coordinate, peak or component assignment, and extraction method. The associated structural descriptor identifies the geometric or chemical model used to map an atomistic configuration into an assigned fluoroberyllate environment.

NMR-derived structural populations, Be–F association graphs, graph-relative incoming-edge counts, and angular distributions are retained with their own normalization and sampling procedures.

## 21. Computational Structural References

The source Salanne et al. (2006), DOI `10.1021/jp061002u`, examines network formation in molten LiF–BeF2 using a first-principles-derived polarizable interaction model. Its numerical structural outputs are associated with their simulation composition, interaction model, temperatures, cell and sampling conventions.

The AIMD study Baral et al. (2021), DOI `10.1021/acsomega.1c02528`, provides computed FLiBe structural and thermophysical quantities on reported simulation states. The committed table `data/reference/flibe_baral_2021_aimd_density.json` retains temperature, cell edge, cell volume, and calculated density as separately typed reference data.

The structural source register `docs/references/flibe_sources.md` connects these computational and experimental references with their bibliographic and method identifiers.

## 22. Solid-State Local Structure

The source Gardner et al. (2025), DOI `10.1107/S1600576725000548`, provides temperature-dependent solid Li2BeF4 neutron and X-ray diffraction data.

A solid reference configuration identifies crystallographic cell vectors, atomic sites, symmetry, phase, and temperature. A liquid reference identifies its corresponding melt composition, temperature, pressure, and structural sampling. Transformations between source states are expressed through explicitly selected physical and numerical models.

The structure register therefore accommodates crystalline lattice geometry and liquid pair/network correlations under their respective source-domain identifiers.

## 23. Dynamic Coordination and Residence

For a selected graph-construction rule, let `a_ij(t)` be the indicator of a specified directed edge or atom-pair association at physical time `t`:

`a_ij(t) in {0,1}`.

A time-averaged occupancy is:

`p_ij = (1/M) sum_(n=0)^(M-1) a_ij(t_n)`.

For a stationary sampled process, a conditional persistence function can be defined as:

`C_ij(tau) = <a_ij(t) a_ij(t+tau)> / <a_ij(t)>`, when `<a_ij(t)> > 0`.

A continuous-residence statistic additionally specifies the treatment of temporary edge interruptions, observation boundaries, and censoring. These structural indicators are defined by an explicit graph or association operator and remain distinct from the retained ternary execution state.

## 24. Spatial Symmetry and Atom Permutation

For an orthogonal spatial transformation `Q in O(3)` and translation `b`:

`r_i' = Q r_i + b`.

For a consistently transformed cell and selected pair-image rule, distances and angular dot products obey their corresponding invariant relations. Species-resolved graph coordination is unchanged under a rigid transformation that preserves the graph edge relation.

An atomic permutation reorders species, coordinates, and node-associated records with the same index mapping. The atomwise coordination vector transforms by the same permutation. Species population statistics retain their values under consistent atom relabeling.

Higher-order geometric and structural descriptors use the transformation rule associated with their scalar, vector, axial-vector, or tensor representation.

## 25. Coordination-to-Resonance Parameters

`FLiBeResonanceParameterization` accepts an `FLiBeCoordinationState` and invokes a supplied evaluator returning `PhaseDynamicsParameters`. The returned parameter vector has one receiver-specific coupling and one phase lag per oscillator, validated against `coordination.atom_count`.

`ConstantFLiBeResonanceParameters` supplies an explicitly declared fixed phase-parameter vector for the same cardinality. Both parameterization interfaces retain typed `ParameterProvenance` and optional source metadata.

The selected coordination rule, its cutoff or graph origin, the parameter evaluator, and the sampled physical state are recorded with the resulting coupling and lag vectors.

## 26. Continuous FLiBe Resonance Descriptor

`FLiBeResonanceDescriptor` binds:

- an `FLiBeConfiguration`;
- an `FLiBeCoordinationState`;
- an `FLiBeThermodynamicState`;
- a continuous `ResonanceState`;
- typed provenance and optional source metadata.

Its constructor validates matching atom, coordination-record, and oscillator counts, matching coordination and configuration species order, and the exact binary composition of its bound configuration.

Its `descriptor`, `coordinate`, `phase_order`, and `frequency_spread` properties are computed from the supplied continuous `ResonanceState`. Coordination, thermodynamic context, and source metadata are retained in the containing FLiBe descriptor record.

## 27. Phase Dynamics and Graph Sampling

For receiving oscillator `j`, the directed Kuramoto–Sakaguchi phase equation is:

`d theta_j/dt = omega_j + kappa_j sum_(i→j in G) sin(theta_i - theta_j - gamma_j)`.

The selected interaction graph supplies directed phase-coupling adjacency. The phase integrator advances continuous oscillator phases with its declared timestep and phase-wrapping rule. Graph and coordination evaluations are sampled at identified mechanical configurations and times.

A multirate calculation records MD time, resonance time, graph-update instants, parameter-vector generation, and the order in which structural state affects subsequent phase evolution.

## 28. Balanced-Ternary Execution and Interatomic Energy

A continuous resonance descriptor can enter a selected projection and ternary-request operator. The execution alphabet is `-1/0/1`, including active neutral `0`, and its retained state, pending destination, request, guard, and committed event have separate semantics.

Opposite-polarity committed routes are:

`-1 → 0 → 1`.

`1 → 0 → -1`.

`FLiBeTREIPModel` receives the configuration, graph, initial features, FLiBe resonance descriptor, and retained `TernaryExecutionVector`. `append_flibe_resonance_channels` adds the continuous phase-order and frequency-spread scalars to every node's features, after which the energy model applies retained-state conditioning and evaluates a scalar energy.

The force-derived mechanical trajectory and subsequent local coordination states are connected through the declared MD, resonance, and execution-event schedule.

## 29. Open-System Structural Evolution

For species concentration `c_s`, flux `J_s`, and volumetric source `q_s` in a selected material region:

`partial_t c_s + div(J_s) = q_s`.

A time-dependent structural calculation associates coordination and network descriptors with species inventory, composition, temperature, pressure, mechanical deformation, and external exchange. The atomistic boundary identifies any insertion/removal or reaction event and its mapping to the next stored configuration.

A structural state trajectory can therefore retain ordered geometric graphs, species coordination states, pair distributions, and resonance-conditioned outputs alongside the physical time and boundary state.

## 30. Source Correspondence and Numerical Comparisons

A structural comparison identifies the observable and its source method, composition, temperature, pressure, phase or physical state, spatial sampling, numerical representation, independent-axis unit, and uncertainty when reported.

For matched structural series `y_model,k` and `y_source,k`, a selected residual is:

`delta_y,k = y_model,k - y_source,k`.

An aggregation may use:

`MAE = (1/M) sum_k |delta_y,k|`.

`RMSE = sqrt[(1/M) sum_k delta_y,k^2]`.

The calculation records axis selection, normalization, interpolation or transform method, correlation treatment, statistical estimator, and predefined numerical tolerances. Experimental scattering, spectroscopic observations, and computational structural outputs retain their individual provenance records.

## 31. Exact Invariants and Numerical Qualification

The executable local-structure checks include:

- canonical Li, Be, and F species identifiers and ordered atomic inventory;
- one coordination record per atom, indexed contiguously from zero;
- nonnegative integer Li, Be, and F incoming-neighbor counts, excluding Boolean values;
- graph node count equal to configuration atom count;
- one increment for each counted incoming directed edge, including distinct image records;
- rejection of source-equals-receiver coordination edges;
- exact identity `total_neighbor_records = graph.edge_count` for the accepted graph;
- exact canonical ordering of `species_coordination` as Li, Be, F;
- cardinality and species-order binding of coordination and resonance descriptor records;
- exact `-1/0/1` execution and pending-route state contracts when coupled.

Numerical structure procedures declare cutoff geometry, image convention, angular or radial binning, time and ensemble averages, source-data processing, and fixed comparison criteria. Exact integer and categorical invariants use exact equality.

## 32. Reproducibility Record

A reproducible structural calculation records:

- atomic species, order, positions, cell, periodic flags, composition, and material state;
- interaction graph construction, cutoff, directed edges, and image indices;
- species-resolved coordination and zero-based atom indexing;
- radial and angular sampling, species pair selection, binning, normalization, and numerical transforms;
- any Be–F association, network construction, bridging and residence definitions;
- scattering or NMR source, experiment or simulation method, axes, and processing procedure;
- physical sampling times, trajectory ensemble, and mechanical graph-update schedule;
- resonance parameter evaluator, oscillator state, phase dynamics, and descriptor sampling;
- ternary requests, retained and pending states, guards, committed events, and conditioning;
- compared observables, source identity, uncertainty, numerical procedure, and recorded results.

The resulting trace links the source configuration and each structural output to its explicit geometrical, material, method, and time context.

## 33. Executable Interface Index

| Function | Repository path |
| --- | --- |
| FLiBe species and composition | `src/tr_eif/flibe/species.py`, `src/tr_eif/flibe/composition.py` |
| FLiBe atomic configuration | `src/tr_eif/flibe/configuration.py` |
| Source atomic geometry | `src/tr_eif/configuration/state.py` |
| Directed graph and edge records | `src/tr_eif/graph/interaction.py` |
| Cutoff graph construction | `src/tr_eif/graph/builder.py` |
| Periodic image selection | `src/tr_eif/geometry/periodic.py` |
| Directed edge geometry | `src/tr_eif/graph/geometry.py` |
| FLiBe coordination and state records | `src/tr_eif/flibe/coordination.py` |
| MD neighbor-list snapshots | `src/tr_eif/md/neighbor_list.py` |
| FLiBe resonance parameterization | `src/tr_eif/flibe/resonance_parameterization.py` |
| FLiBe continuous resonance descriptor | `src/tr_eif/flibe/resonance_descriptor.py` |
| FLiBe ternary-request mapping | `src/tr_eif/flibe/ternary_interpretation.py` |
| FLiBe TR-EIP energy | `src/tr_eif/flibe/tr_eip.py` |
| Continuous resonance dynamics | `src/tr_eif/resonance/dynamics.py` |
| MD resonance and ternary bridges | `src/tr_eif/md/resonance_propagation.py`, `src/tr_eif/md/ternary_propagation.py` |
| FLiBe structural source register | `docs/references/flibe_sources.md` |

## 34. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| FLiBe graph coordination | `tests/invariants/test_flibe_coordination_invariants.py` |
| FLiBe configuration | `tests/invariants/test_flibe_configuration_invariants.py` |
| Atomic geometry | `tests/invariants/test_geometry_invariants.py` |
| Directed interaction graph | `tests/invariants/test_interaction_graph_invariants.py` |
| MD neighbor-list interaction graph | `tests/integration/test_molecular_dynamics_neighbor_list.py` |
| FLiBe resonance parameters | `tests/invariants/test_flibe_resonance_parameterization_invariants.py` |
| FLiBe resonance descriptor | `tests/invariants/test_flibe_resonance_descriptor_invariants.py` |
| FLiBe ternary interpretation | `tests/invariants/test_flibe_ternary_interpretation_invariants.py` |
| FLiBe TR-EIP integration | `tests/integration/test_flibe_tr_eip.py` |
| MD resonance propagation | `tests/integration/test_molecular_dynamics_resonance_propagation.py` |

The associated tests exercise input typing, graph cardinality, species-resolved edge counts, periodic-image handling, source/receiver orientation, deterministic ordering, and the coupling interfaces using specified atomistic fixtures.

## 35. Chapter Integration

The FLiBe local-structure layer maps ordered three-dimensional atomic configurations and directed interactions to species-resolved coordination records. Pair and angular distributions, Be–F network descriptors, scattering, and spectroscopy use identified observation and transformation operators with source-specific material states.

Coordination may parameterize continuous Kuramoto–Sakaguchi dynamics through the FLiBe resonance interface. The resulting continuous descriptors and retained active `-1/0/1` execution can condition the TR-EIP energy and its molecular-dynamics evolution. The combined record preserves each state type, sampling instant, numerical method, and material-source identity.
