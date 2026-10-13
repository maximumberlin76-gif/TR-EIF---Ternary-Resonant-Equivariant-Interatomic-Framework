
# Neighbor Lists

## 1. Scope and System Variables

This chapter defines deterministic neighbor-list construction, retention, rebuilding, and interaction-graph extraction for the TR-EIF molecular-dynamics reference. The operations act on three-dimensional atomic configurations and use the geometry, cutoff, and periodic-image conventions established in Chapter 04.

For `N ≥ 1` atoms, let `R = (r_0, ..., r_(N-1))` be Cartesian coordinates, `S` the species tuple, `C` an optional three-dimensional simulation cell, and `P` its three periodic-axis flags. The state `AtomicConfiguration(S, R, C, P)` supplies these quantities to the neighbor-list operators.

A neighbor list stores candidate atomic pairs within a search radius. The current interaction graph is obtained by reevaluating those candidates at the interaction cutoff and recording directed edges with current periodic-image indices.

## 2. Cutoff and Skin Parameters

Let `r_c` denote the interaction cutoff and `s_skin` the neighbor-list skin. The executable input contract is:

- `r_c` is a finite real number with `r_c > 0`;
- `s_skin` is a finite real number with `s_skin ≥ 0`;
- `r_search = r_c + s_skin` is finite.

Boolean values are excluded from both scalar inputs. The derived search radius is used at snapshot construction, while `r_c` determines the directed edges produced from a retained snapshot.

For a selected pair displacement `d_ij` at the reference configuration, the candidate condition is:

`|d_ij|^2 ≤ r_search^2`.

For the current configuration, the interaction condition is:

`|d_ij,current|^2 ≤ r_c^2`.

Both conditions include equality at their respective cutoffs.

## 3. Reference Snapshot

`NeighborList` in `src/tr_eif/md/neighbor_list.py` is an immutable dataclass with the fields:

- `interaction_cutoff`;
- `skin`;
- `reference_configuration`;
- `candidate_pairs`.

Its properties are `search_cutoff` and `candidate_pair_count`.

`reference_configuration` identifies the coordinates, species, cell, and periodic flags at the time of candidate construction. Each candidate is stored as the integer pair `(i, j)` with `0 ≤ i < j < N`.

The `candidate_pairs` tuple is sorted lexicographically, contains unique pairs, and preserves the canonical pair order. The snapshot represents pair membership at its reference geometry; current edge membership and image indices are evaluated by a separate operation.

## 4. Candidate Construction

`build_neighbor_list(configuration, interaction_cutoff, skin)` performs the following steps:

1. Validate the configuration and scalar parameters.
2. Compute `r_search = r_c + s_skin`.
3. Call `build_cutoff_graph(configuration, r_search)`.
4. Retain the graph's pairs whose directed indices satisfy `source < receiver`.
5. Construct an immutable `NeighborList` with the original configuration and canonical candidate pairs.

The directed cutoff-graph builder iterates over ordered atom pairs. Each selected unordered candidate appears once in `candidate_pairs`; the directed interaction edges are constructed later.

For `N` atoms, the current direct cutoff-graph construction examines `N(N - 1)` ordered source–receiver pairs. The snapshot therefore has a direct pair-enumeration construction cost proportional to `N^2` in the current implementation, with additional geometric work per pair.

## 5. Periodic and Nonperiodic Pair Geometry

For nonperiodic configurations, pair displacement is the Cartesian difference:

`d_ij = r_j - r_i`.

Its periodic image index is `(0, 0, 0)`.

For a periodic configuration, the neighbor-list operations call `minimum_image` from `src/tr_eif/geometry/periodic.py`. With cell matrix `B = [a b c]`, first compute:

`u = B^(-1) (r_j - r_i)`.

For each component `u_k`, the selected image index is:

`m_k = -floor(u_k + 0.5)` on an enabled periodic axis.

`m_k = 0` on a nonperiodic axis.

The returned Cartesian displacement is:

`d_ij = B (u + m)`.

This is the componentwise fractional-wrapping convention used by the executable reference. Cell geometry and periodic flags determine the selection rule, including its half-cell tie convention.

## 6. Snapshot Rebuild Decision

`neighbor_list_requires_rebuild(neighbor_list, configuration)` compares the current configuration against the retained reference snapshot.

A rebuild is requested immediately when any of these fields changes:

- atom count;
- species tuple;
- periodic-axis flags;
- simulation-cell geometry.

With these fields unchanged, the operator compares each atom's current position against its reference position. It uses direct Cartesian displacement for nonperiodic configurations and `minimum_image` displacement for periodic configurations.

For atom `i`, denote this reference-to-current displacement by `delta_i`. The positional rebuild condition is:

`|delta_i|^2 > (s_skin / 2)^2` for at least one atom.

The inequality is strict. Displacement exactly equal to `s_skin / 2` retains the snapshot; displacement greater than this threshold requests a rebuild.

At `s_skin = 0`, the positional threshold is zero, so every nonzero selected displacement requests a rebuild. Under periodic boundaries, the displacement comparison follows the same fractional-wrapping convention as the geometry operator.

## 7. Relative-Motion Basis of the Skin Criterion

For a pair of atoms, reference-to-current displacements `delta_i` and `delta_j` give a change in relative Cartesian displacement:

`d_ij,current - d_ij,reference = delta_j - delta_i`.

The triangle inequality yields:

`|delta_j - delta_i| ≤ |delta_j| + |delta_i|`.

When both displacement magnitudes are at most `s_skin / 2`, the relative displacement change is at most `s_skin`. In a consistent Euclidean image representation, a pair moving into `r_c` from its reference location is therefore covered by candidate enumeration through `r_c + s_skin`.

For periodic configurations, application of this bound follows the selected image convention, cell geometry, and continuity of the tracked displacements. The reference implementation uses componentwise fractional wrapping; the full cell metric and the image-selection schedule are recorded when analyzing skewed cells or trajectories with repeated boundary crossings.

## 8. Current Interaction Graph from a Snapshot

`interaction_graph_from_neighbor_list(neighbor_list, configuration)` first evaluates the rebuild predicate. A configuration requiring a rebuild produces a `ValueError`; the caller then constructs a new snapshot before evaluating its graph.

For each canonical candidate `(i, j)` in a retained snapshot:

1. Evaluate the current directed displacement and periodic image from `i` to `j`.
2. Compare its squared distance with `r_c^2`.
3. For a pair within the interaction cutoff, evaluate the reverse image from `j` to `i` independently.
4. Append both directed edges, `(i, j, image_ij)` and `(j, i, image_ji)`.
5. Sort all edges by `(source, receiver, image)`.
6. Return `InteractionGraph(node_count=N, edges=...)`.

Thus a candidate can be retained in the snapshot while its current distance is outside the interaction cutoff. It can also enter the interaction cutoff during a valid snapshot interval and be represented by the current graph.

The returned graph uses the current geometry and current periodic-image indices. Its node count equals the number of atoms in the supplied configuration.

## 9. Reference Example

Consider three atoms at Cartesian positions:

`r_0 = (0.0, 0.0, 0.0)`.

`r_1 = (0.8, 0.0, 0.0)`.

`r_2 = (1.4, 0.0, 0.0)`.

Choose `r_c = 1.0` and `s_skin = 0.5`, so `r_search = 1.5`. For this nonperiodic configuration, the reference candidate pairs are:

`((0, 1), (0, 2), (1, 2))`.

At the current reference coordinates, pairs `(0, 1)` and `(1, 2)` lie within the interaction cutoff. Pair `(0, 2)` remains a candidate, with separation `1.4`.

The directed interaction graph contains edges `0 → 1`, `1 → 0`, `1 → 2`, and `2 → 1`, each with image index `(0, 0, 0)`.

A subsequent displacement that respects the retained-snapshot rebuild condition updates the graph through the current coordinates without changing the original candidate tuple.

## 10. Periodic Example

For an orthogonal periodic cell of length `10` along each Cartesian axis, place two atoms at:

`r_0 = (0.2, 0.0, 0.0)`.

`r_1 = (9.8, 0.0, 0.0)`.

The selected forward wrapped displacement is `(-0.4, 0.0, 0.0)`, with image index `(-1, 0, 0)`. The reverse displacement is `(0.4, 0.0, 0.0)`, with image index `(1, 0, 0)`.

With `r_c = 0.5` and `s_skin = 0.2`, the pair belongs to the candidate list and produces both directed interaction edges. Each edge retains its own source, receiver, and image index.

## 11. Structural Invariants

The executable neighbor-list contract includes:

- a positive finite interaction cutoff and nonnegative finite skin;
- a finite sum of cutoff and skin;
- an `AtomicConfiguration` as reference state;
- a tuple of candidate pairs in canonical sorted order;
- unique pair indices satisfying `0 ≤ source < receiver < N`;
- a strict positional rebuild boundary at half the skin;
- an immediate rebuild condition on atom-count, species, cell, or periodic-axis changes;
- directed interaction edges with current source-specific periodic images;
- current cutoff comparison using inclusive squared distance;
- a graph node count equal to the current atom count.

Exact structural comparisons use exact equality. Geometric floating-point tests use the specified numerical operations and declared comparison tolerances.

## 12. Integration with Molecular Dynamics

The neighbor-list primitives are exported through `src/tr_eif/md/__init__.py` and can be called to construct and update an interaction graph for a sequence of atomic configurations.

The existing `velocity_verlet_step` in `src/tr_eif/md/execution.py` calls `build_cutoff_graph` directly for the pre-drift and post-drift configurations. The neighbor-list snapshot and graph-extraction operations are separately available through their own API.

An MD coupling schedule using retained snapshots specifies:

`reference configuration → candidate snapshot → current configuration → rebuild decision → current interaction graph → force evaluation`.

The schedule also identifies when the graph is recalculated during coordinate differentiation, mechanical integration, cell changes, and execution-state conditioning. The molecular state, continuous resonance state, and balanced-ternary `-1/0/1` execution state retain their respective update clocks and contracts.

## 13. Reproducibility and Cost Observables

For deterministic replay, record the reference atomic configuration, interaction cutoff, skin, cell and periodic flags, candidate-pair ordering, current configurations, rebuild decisions, and resulting directed interaction graphs.

The relevant per-snapshot and per-step observables include:

- candidate-pair count;
- number of directed interaction edges;
- rebuild-event count and event step indices;
- maximum reference-to-current selected atomic displacement;
- elapsed time for snapshot construction and current-graph extraction;
- memory occupied by retained candidate pairs and reference configuration.

In the present implementation, candidate construction invokes full pair enumeration. With `P` retained candidate pairs, subsequent graph extraction evaluates up to `P` candidate distances plus the `N` atom displacements in the rebuild check. Measurement procedures specify the atomic configurations, hardware, Python runtime, numerical parameters, and repetition policy before reporting scaling results.

## 14. Executable Interfaces and Tests

| Function | Repository path |
| --- | --- |
| Atomic configuration and periodic flags | `src/tr_eif/configuration/state.py` |
| Fractional-wrapped image geometry | `src/tr_eif/geometry/periodic.py` |
| Direct Cartesian relative geometry | `src/tr_eif/geometry/relative.py` |
| Cutoff graph construction | `src/tr_eif/graph/builder.py` |
| Graph and image-index structures | `src/tr_eif/graph/interaction.py` |
| Neighbor-list creation and rebuild | `src/tr_eif/md/neighbor_list.py` |
| MD namespace exports | `src/tr_eif/md/__init__.py` |
| Force-driven mechanical step | `src/tr_eif/md/execution.py` |
| Neighbor-list integration tests | `tests/integration/test_molecular_dynamics_neighbor_list.py` |
| Directed-graph invariant tests | `tests/invariants/test_interaction_graph_invariants.py` |
| Geometry invariant tests | `tests/invariants/test_geometry_invariants.py` |
| Barostat geometry tests | `tests/integration/test_molecular_dynamics_barostat.py` |

The tests exercise candidate inclusion, retained-snapshot behavior, zero-skin behavior, rebuild triggers, periodic crossings, graph equivalence at the reference state, canonical pair ordering, numerical input validation, and directed image geometry.

## 15. Summary

TR-EIF neighbor lists retain a deterministic, ordered set of candidate atom pairs selected at the interaction cutoff plus skin. A displacement and metadata-based rebuild predicate governs reuse of this snapshot, while the current graph is constructed from active cutoff comparisons and directed periodic-image indices.

This procedure supplies explicit geometric state, rebuild events, and graph data for atomistic trajectory calculations and for coupling to resonance and ternary-conditioned interatomic operations.
