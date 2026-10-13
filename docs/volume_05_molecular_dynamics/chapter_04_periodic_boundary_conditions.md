
# Periodic Boundary Conditions

## 1. Scope and State Variables

This chapter specifies periodic-cell geometry and its interaction with atomic configurations, neighbor selection, molecular-dynamics integration, and volumetric coupling in TR-EIF.

The geometric state comprises `N ≥ 1` atomic species and Cartesian positions, three optional cell vectors, and three periodic-axis flags. The corresponding executable representation is `AtomicConfiguration` in `src/tr_eif/configuration/state.py`.

The periodic operations supply relative spatial geometry to the continuous interatomic model. Resonance variables and balanced-ternary `-1/0/1` execution retain their separately defined state spaces and event schedules.

## 2. Three-Dimensional Cell Geometry

Let the cell consist of ordered lattice vectors `a`, `b`, and `c` in `R^3`. Introduce the matrix `B = [a b c]`, with lattice vectors as columns, and define the cell volume:

`V_cell = |det(B)|`.

`AtomicConfiguration` accepts an optional `cell = (a, b, c)` and `periodic = (p_a, p_b, p_c)` with Boolean components. A supplied cell has three finite three-component vectors and nonzero determinant. The periodic-axis flags require a cell whenever at least one axis is enabled.

The default flags are `(False, False, False)`. Full periodicity is `(True, True, True)`; mixed Boolean triples represent partial periodicity along selected lattice directions. A cell may also be supplied when all periodic flags are false.

The atomic species and position tuples have the same positive cardinality. Every stored Cartesian position has three finite components.

## 3. Cartesian and Fractional Coordinates

For fractional coordinates `q = (q_a, q_b, q_c)`, the Cartesian position relative to the chosen cell origin is:

`r = B q = q_a a + q_b b + q_c c`.

For a nonsingular cell, the inverse mapping is:

`q = B^(-1) r`.

The reference functions are `fractional_to_cartesian(q, cell)` and `cartesian_to_fractional(r, cell)` in `src/tr_eif/geometry/periodic.py`. Their inputs and outputs are three-component vectors.

This representation accommodates orthogonal and skewed lattice bases. The conversion round trip is checked numerically using the declared floating-point comparison tolerance.

## 4. Periodic Image Equivalence

An image index is an integer triple `k = (k_a, k_b, k_c)`; the corresponding lattice translation is:

`L(k) = k_a a + k_b b + k_c c = B k`.

For a periodic axis, translation by an integer multiple of its lattice vector identifies equivalent periodic positions. A nonperiodic axis retains image index zero in the boundary mapping.

For source atom `i` and target atom `j`, the displacement to explicit target image `k` is:

`d_ij(k) = r_j + B k - r_i`.

`periodic_image_displacement(source, target, cell, image)` implements this relation. The `image` parameter is a three-integer tuple, with Boolean values excluded by validation.

The image tuple is a geometric lattice index. It has no relation to the balanced-ternary execution-state alphabet.

## 5. Fractional-Coordinate Image Selection

The reference `minimum_image(source, target, cell, periodic)` computes the Cartesian displacement and its selected image index from fractional-coordinate wrapping.

For the unwrapped Cartesian difference:

`d = r_target - r_source`.

Compute its fractional components:

`u = B^(-1) d`.

For each component `u_j`, the image-selection rule is:

`k_j = -floor(u_j + 0.5)` when `p_j` is true.

`k_j = 0` when `p_j` is false.

The selected fractional displacement is `u_wrapped,j = u_j + k_j`, followed by:

`d_wrapped = B u_wrapped`.

On a periodic axis, this rule places the fractional component in the half-open interval `[-0.5, 0.5)`. In particular, a positive half-cell tie maps to the negative representative. On a nonperiodic axis, the original fractional component is retained.

The returned pair is `(d_wrapped, k)`. The companion `minimum_image_displacement` returns the displacement alone. Applying `periodic_image_displacement` with the returned `k` reconstructs the same Cartesian displacement.

For skewed cells, componentwise fractional wrapping and Euclidean shortest-lattice-vector selection are distinct geometric operations. The latter is characterized by minimizing `|d + B k|` over admissible integer image indices under the cell metric `B^T B`. The executable reference implements the componentwise fractional rule defined above; calculations record the selected cell geometry and image-selection convention.

## 6. Orthogonal-Cell Example

Consider an orthogonal cell with vectors:

`a = (4, 0, 0)`, `b = (0, 6, 0)`, `c = (0, 0, 8)`.

For `r_source = (0.2, 0.5, 0.4)` and `r_target = (3.8, 5.5, 7.6)`, the raw displacement is:

`d = (3.6, 5.0, 7.2)`.

With `periodic = (True, False, True)`, the selected image is:

`k = (-1, 0, -1)`.

The wrapped displacement is:

`d_wrapped = (-0.4, 5.0, -0.8)`.

The second Cartesian component remains unwrapped because the corresponding lattice axis is nonperiodic. These values form part of the executable geometry invariant tests.

## 7. Directed Periodic Interaction Graph

`build_cutoff_graph(configuration, cutoff)` in `src/tr_eif/graph/builder.py` evaluates each ordered pair of distinct atoms `(i, j)` against a finite positive radial cutoff `r_c`.

The selected pair displacement uses `minimum_image` when any periodic axis is enabled, and direct Cartesian subtraction when all axes are nonperiodic.

An edge is included when:

`|d_ij|^2 ≤ r_c^2`.

The inclusive comparison assigns interactions at the exact cutoff distance to the graph. The builder iterates over source and receiver indices in ascending order and stores `InteractionEdge(source=i, receiver=j, image=k)`.

Each ordered atom pair contributes at most one selected-image edge. The periodic image is retained in the directed edge record; reverse directions are constructed through their own displacement and image evaluations.

`InteractionGraph` records a positive node count and immutable directed edges, with validation of node indices, image tuples, and duplicate edges.

## 8. Edge Geometry from Recorded Images

`evaluate_edge_geometry(configuration, edge)` in `src/tr_eif/graph/geometry.py` reconstructs the displacement for the edge's stored lattice image and evaluates:

`distance_ij = |d_ij(k)|`.

`direction_ij = d_ij(k) / distance_ij`.

The direction expression requires positive distance. A zero-length geometric edge causes a `ValueError` during edge-geometry evaluation.

For a cell-free configuration, the permitted image is `(0, 0, 0)`. With a supplied cell, a nonzero image component is accepted only along an enabled periodic axis.

Image coordinates, distances, and directions provide geometric inputs to downstream equivariant message and energy operations. A graph edge carries its defined computational adjacency and image geometry.

## 9. Neighbor-List Candidate Construction

`build_neighbor_list(configuration, interaction_cutoff, skin)` in `src/tr_eif/md/neighbor_list.py` stores a neighbor-list snapshot for a reference configuration.

The interaction cutoff `r_c` is finite and positive, and skin `s_skin` is finite and nonnegative. The search radius is:

`r_search = r_c + s_skin`.

The builder constructs a cutoff graph using `r_search` and retains one canonical unordered candidate pair `(i, j)` when `i < j`. Candidate pairs are sorted and unique.

The neighbor list retains the reference atomic configuration, interaction cutoff, skin, and candidate-pair tuple. The search radius and candidate-pair count are exposed as properties.

## 10. Neighbor-List Rebuild Criterion

`neighbor_list_requires_rebuild(neighbor_list, configuration)` compares the current configuration with the retained reference configuration.

A rebuild is requested when atom count, species, periodic flags, or cell geometry differ from the reference. With these fields unchanged, each atomic displacement from its reference position is calculated using fractional periodic wrapping for periodic configurations or direct Cartesian subtraction otherwise.

The positional criterion is:

`|d_i(reference → current)|^2 > (s_skin / 2)^2` for any atom `i`.

The strict inequality gives the equality case a retained neighbor-list snapshot. With zero skin, any nonzero atomic displacement meets the rebuild criterion.

`interaction_graph_from_neighbor_list` first applies this rebuild check. For a retained snapshot, it re-evaluates current pair displacements and selects directed edges whose distances satisfy the inclusive interaction cutoff `|d_ij|^2 ≤ r_c^2`. Both directions carry their respective current image indices, and the output edges are sorted by source, receiver, and image.

The snapshot and selected graph are separate objects: the former retains potential interacting pairs, while the latter represents interactions at the supplied current configuration.

## 11. Periodic Geometry During Molecular-Dynamics Steps

`velocity_verlet_step` in `src/tr_eif/md/execution.py` builds the cutoff graph from the initial configuration, evaluates forces, advances Cartesian positions, rebuilds a new cutoff graph from the updated positions, and evaluates endpoint forces before completing the velocity update.

The step constructs the updated `AtomicConfiguration` with the original species, cell vectors, and periodic-axis flags. Cartesian positions are propagated by the mechanical integrator; periodic images are selected when the graph and edge geometry are evaluated.

`ConservativeForceEvaluator` uses central coordinate perturbations with the supplied graph retained during each force-derivative evaluation. Graph reconstruction occurs at the explicitly chosen mechanical integration boundaries.

Thus a trajectory records both the stored Cartesian positions and the image-selection rules used to evaluate interatomic interactions.

## 12. Cell Evolution Under Isotropic Pressure Coupling

For a fully periodic cell, the reference pressure-coupling primitive defines:

`mu_V = 1 - (dt / tau_p) beta (P_target - P_current)`.

For finite valid inputs with `mu_V > 0`, its isotropic linear scale is:

`s = mu_V^(1/3)`.

`scale_periodic_configuration` applies this same positive scale to all three lattice vectors and every Cartesian position:

`B_next = s B`.

`r_i,next = s r_i`.

Accordingly:

`V_cell,next = s^3 V_cell = mu_V V_cell`.

The fractional coordinates are retained by this affine transformation up to numerical rounding. `apply_isotropic_barostat` retains velocities, masses, MD step, and MD time, while returning the scaled configuration.

The executable barostat requires `periodic = (True, True, True)`. An updated cell is recorded with the subsequent neighbor-graph reconstruction and force evaluation schedule.

## 13. Cell Geometry and Other State Spaces

Periodic-cell geometry enters mechanical distance calculations, directed interaction graphs, the equivariant interatomic mapping, and the cell-strain evaluation of stress.

Continuous resonance propagation can construct its coupling graph from the current atomic configuration. The resonance state evolves on its own continuous integration clock.

Balanced-ternary execution is represented through retained `-1/0/1` values, requests, pending destinations, and committed events. The coupling specification maps geometry and resonance descriptors to execution requests and conditions the energy or other selected computational operators.

Mechanical positions, lattice-image indices, oscillator phases, thermodynamic state variables, and ternary execution values are separately typed quantities in the coupled trace.

## 14. Transport Observables and Coordinate Histories

A trajectory can store Cartesian positions for every mechanical step. For periodic trajectories, displacement-sensitive transport analysis specifies how positions are unwrapped through boundary crossings, including image counters or an explicitly reconstructed unwrapped position history.

The existing `mean_squared_displacement` operator in `src/tr_eif/md/transport.py` computes Cartesian displacement relative to the first trajectory state for nonperiodic configurations. Its input validator requires an explicit unwrapped-coordinate representation for periodic-trajectory displacement studies.

The boundary metadata accompanying a transport calculation include cell history, periodic flags, image or unwrapped-coordinate conventions, and the physical sampling times.

## 15. Numerical Contracts and Reproducibility

The exact structural contracts include the three periodic Boolean flags, three integer image components, cell-vector cardinality, species/position cardinality, graph endpoint indices, and unique canonical neighbor candidate pairs.

Geometric numerical checks include fractional–Cartesian round trips, image-displacement reconstruction, distance and direction evaluation, cutoff inclusion, neighbor-list rebuild thresholds, and cell-volume scaling under isotropic transformations.

For a reproduced periodic calculation, record:

- atomic species, Cartesian coordinates, cell vectors, and periodic-axis flags;
- the cell-vector ordering and fractional-coordinate convention;
- the selected componentwise image-wrapping rule and image-index tie convention;
- graph cutoff, neighbor-list skin, graph-update schedule, and cutoff comparison;
- force-derivative increments, integration timesteps, and barostat parameters where used;
- initial and final graph edges with their image indices;
- positions and cell history for transport or moving-cell observables;
- declared numerical tolerances for floating-point geometric comparisons.

## 16. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| Atomic configuration and periodic flags | `src/tr_eif/configuration/state.py` |
| Fractional coordinates and periodic images | `src/tr_eif/geometry/periodic.py` |
| Direct Cartesian relative geometry | `src/tr_eif/geometry/relative.py` |
| Directed cutoff-graph builder | `src/tr_eif/graph/builder.py` |
| Edge and graph structures | `src/tr_eif/graph/interaction.py` |
| Directed edge geometry | `src/tr_eif/graph/geometry.py` |
| Neighbor-list snapshot and rebuild | `src/tr_eif/md/neighbor_list.py` |
| Mechanical step and graph updates | `src/tr_eif/md/execution.py` |
| Isotropic cell transformation | `src/tr_eif/md/barostat.py` |
| Transport displacement observables | `src/tr_eif/md/transport.py` |
| Geometry invariant tests | `tests/invariants/test_geometry_invariants.py` |
| Configuration invariant tests | `tests/invariants/test_atomic_configuration_invariants.py` |
| Directed graph invariant tests | `tests/invariants/test_interaction_graph_invariants.py` |
| Neighbor-list integration tests | `tests/integration/test_molecular_dynamics_neighbor_list.py` |
| Barostat integration tests | `tests/integration/test_molecular_dynamics_barostat.py` |

## 17. Summary

TR-EIF periodic geometry is defined by three-dimensional lattice vectors, Boolean periodic-axis flags, and explicit integer image indices. The current reference uses componentwise fractional-coordinate image wrapping to calculate relative displacements for periodic graph construction and neighbor updates.

The molecular-dynamics integrator, neighbor-list builder, isotropic barostat, and transport-observable interfaces use these geometric conventions through separately identified operations. Their input parameters and update order are included in the reproducibility record.
