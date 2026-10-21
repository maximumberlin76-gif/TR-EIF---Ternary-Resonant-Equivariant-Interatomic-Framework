
# Transport Properties

## 1. Scope and Material-State Definition

This chapter defines transport observables and constitutive transfer relations for the LiF–BeF2 reference material in TR-EIF. It connects atomistic trajectories, species-resolved diffusion, momentum transport, thermal and electrical conduction, hydrogen-isotope migration, boundary exchange, and cross-scale transport-coefficient records.

The selected physical system belongs to the class of open nonlinear dissipative dynamical systems. Its state description includes three-dimensional atomic geometry, species inventory, material composition, thermodynamic variables, interaction history, and boundary conditions. Continuous resonance variables and retained balanced-ternary `-1/0/1` execution are coupled through separately identified operators and event schedules.

The computational chain is:

`material state → interatomic model and mechanical trajectory → displacement or current observable → transport estimator → coefficient record → scale transfer → continuum flux or engineering boundary`.

The executable observables and transfer contracts are implemented in `src/tr_eif/md/transport.py` and `src/tr_eif/multiscale/transport_transfer.py`.

## 2. Species, Composition, and Transport Identity

For component formula-unit amounts `n_LiF` and `n_BeF2`, define normalized fractions:

`x_LiF = n_LiF / (n_LiF + n_BeF2)`.

`x_BeF2 = n_BeF2 / (n_LiF + n_BeF2)`.

The exact `2 LiF : 1 BeF2` ratio has `(x_LiF, x_BeF2) = (2/3, 1/3)`, corresponding to `Li2BeF4`. The nominal `67 mol% LiF : 33 mol% BeF2` composition uses `(0.67, 0.33)`. The experimental Vidrio 2022 specimen register records `33.58(5) mol% BeF2` from ICP-MS.

Every transport observation identifies its transported entity and transport mechanism. The source register distinguishes Li, Be, and F self-diffusion; collective ionic transport; thermal and viscous fluxes; and hydrogen-isotope diffusion, solubility, and permeation. A measured or calculated coefficient is associated with its composition, temperature, pressure, material state, boundary configuration, units, source method, and uncertainty representation.

## 3. Thermodynamic and Geometric Coordinates

`FLiBeThermodynamicState(temperature, pressure)` stores finite temperature `T > 0` in kelvin and finite pressure `P >= 0` in pascal. `FLiBeConfiguration` associates an ordered Li/Be/F atomic inventory with a three-dimensional `AtomicConfiguration`.

For a periodic cell with ordered vectors forming matrix `B`, the cell volume is:

`V_cell = |det(B)|`.

For a mass inventory `M_total > 0`, its cell-derived density is:

`rho_cell = M_total / V_cell`.

A transport record specifies the spatial reference frame, cell and periodic-image convention, atom ordering, physical sampling times, and the applied mechanical, thermal, and pressure controls. For an open control volume, it also identifies any matter exchange or changing atom inventory.

## 4. Atomistic Trajectories and Sampling Times

For atom `i`, the mechanical state provides position `r_i(t) in R^3`, velocity `v_i(t) in R^3`, and positive mass `m_i`. `MolecularDynamicsTrajectory` stores ordered mechanical states with times `t[n]`.

Define elapsed time from the first recorded state:

`tau[n] = t[n] - t[0]`.

The current `mean_squared_displacement` and `velocity_autocorrelation` functions consume this trajectory and return typed series with matching ordered `times` and `values` tuples. Both reference operators use the first stored state as the time origin and arithmetic averaging over its complete atom inventory.

A species-resolved or multi-origin calculation defines an additional particle-selection and sampling operator, retaining the corresponding species identity and time-origin policy.

## 5. Mean-Squared Displacement

For `N` atoms and an initial time `t_0`, define the single-origin all-atom mean-squared displacement:

`MSD_0(tau) = (1/N) sum_i |r_i(t_0 + tau) - r_i(t_0)|^2`.

`mean_squared_displacement(trajectory)` evaluates this expression from the stored nonperiodic Cartesian coordinates. Its initial value is zero, its output unit is squared length, and its series length equals the number of trajectory states.

For species `s` with selected atom set `I_s` and count `N_s > 0`, the corresponding species-resolved quantity is:

`MSD_s(tau) = (1/N_s) sum_(i in I_s) |r_i(t_0 + tau) - r_i(t_0)|^2`.

A species-specific result records the particle-selection rule and stable atom identities throughout the sampled interval.

## 6. Periodic Displacement Reconstruction

For a fixed periodic cell and an integer image history `k_i(t)`, a continuous Cartesian position representation is:

`r_i,unwrapped(t) = r_i,wrapped(t) + B k_i(t)`.

For a time-dependent cell, the coordinate reconstruction specifies the reference frame and treatment of cell deformation. Periodic transport analysis records image counters or an equivalent unwrapped trajectory with the original cell and sampling history.

The current `mean_squared_displacement` operator accepts nonperiodic trajectories. A periodic MSD calculation is assembled from an explicitly reconstructed unwrapped-coordinate history and its declared estimator. `velocity_autocorrelation` operates on the stored velocities for either periodic or nonperiodic mechanical configurations.

## 7. Einstein Self-Diffusion Relation

For a stationary, isotropic, three-dimensional diffusive regime, species self-diffusion is defined by the long-time Einstein relation:

`D_self,s = lim_(tau→infinity) MSD_s(tau) / (6 tau)`.

Within a selected linear diffusive interval, a slope-based estimator is:

`D_self,s = (1/6) d(MSD_s)/d tau`.

The coefficient has dimensions length squared per time and SI unit `m^2/s`. A numerical estimator identifies its observation interval, time-origin averaging, sample ensemble, finite-size and coordinate conventions, fit method, and parameter uncertainty.

For a two-point finite-interval slope between `tau_a` and `tau_b`, the declared estimator is:

`D_s,interval = [MSD_s(tau_b) - MSD_s(tau_a)] / [6(tau_b - tau_a)]`.

Its input includes `tau_b > tau_a` and the specified diffusive-regime selection.

## 8. Velocity Autocorrelation

The executable single-origin, all-atom velocity autocorrelation is:

`C_v,0(tau) = (1/N) sum_i v_i(t_0) · v_i(t_0 + tau)`.

`velocity_autocorrelation(trajectory)` evaluates this Cartesian dot-product average, preserving signed correlations. The output unit is squared length per squared time. The initial value is the mean squared speed of the supplied atoms.

For species-resolved time-origin averaging, define:

`C_v,s(tau) = <v_s(t_0) · v_s(t_0 + tau)>`.

The angle brackets identify the chosen ensemble and time-origin average. Its particle identity, reference frame, correlation normalization, and temporal sampling are part of the source-observable record.

## 9. Green–Kubo Self-Diffusion

For a stationary equilibrium state with convergent velocity correlation, the isotropic Green–Kubo relation is:

`D_self,s = (1/3) integral_(0→infinity) C_v,s(tau) d tau`.

A finite observation computes a specified numerical quadrature over an interval `[0, tau_max]`, with an explicit tail or window policy. The resulting coefficient record retains the source correlation series, quadrature rule, time step, integration interval, and statistical estimator.

The Einstein and Green–Kubo expressions define two calculation paths for the same species-specific self-diffusion observable under their shared physical-state and statistical conditions.

## 10. Diffusion Tensor and Spatial Symmetry

For anisotropic transport, define a Cartesian diffusion tensor:

`D_ab = lim_(tau→infinity) <Delta_r_a(tau) Delta_r_b(tau)> / (2 tau)`.

For a linear constitutive mapping in Cartesian coordinates:

`j_a = -sum_b D_ab partial_b c`.

Under an orthogonal spatial transformation `Q in O(3)`, the tensor representation transforms as:

`D' = Q D Q^T`.

The scalar `TransportCoefficient` interface stores one finite numerical value per record. A tensor transport realization identifies its component collection, ordering, reference frame, unit, and reconstruction operator.

## 11. Species Flux and Collective Diffusion

For species amount concentration `c_s`, barycentric material velocity `u`, diffusive amount flux `j_s`, and a volumetric source `q_s`, the fixed-frame balance is:

`partial_t c_s + div(c_s u + j_s) = q_s`.

A selected isotropic Fickian relation is:

`j_s = -D_s grad(c_s)`.

For multicomponent molten salts, a coupled constitutive relation can be expressed as:

`j_s = -sum_r L_(s,r) grad(mu_r/T)`.

The coefficients `L_(s,r)` use the declared flux basis, thermodynamic-force convention, electroneutrality or composition constraints, and temperature dependence. Self-diffusion, tracer diffusion, collective mutual diffusion, and species-current transport use their respective coefficient identities and normalization rules.

## 12. Dynamic and Kinematic Viscosity

For material velocity `u`, define the symmetric strain-rate tensor and its deviatoric part:

`D = [grad(u) + grad(u)^T]/2`.

`D_dev = D - [div(u)/3] I`.

A Newtonian isotropic viscous law is:

`tau_visc = 2 eta D_dev + zeta div(u) I`.

Here `eta` is dynamic shear viscosity in `Pa*s` and `zeta` is bulk viscosity in `Pa*s`. With mass density `rho > 0`, kinematic viscosity is:

`nu = eta / rho`.

Its SI unit is `m^2/s`. A molten-salt viscosity calculation registers composition, temperature, pressure, physical state, shear-rate conditions, constitutive model, source, and units.

## 13. Green–Kubo Viscosity

For a selected stationary equilibrium state with volume `V`, temperature `T > 0`, and zero-mean off-diagonal pressure-tensor fluctuation `delta_P_xy`, the shear-viscosity relation is:

`eta = [V/(k_B T)] integral_(0→infinity) <delta_P_xy(0) delta_P_xy(tau)> d tau`.

The stress and pressure-tensor conventions, kinetic and interatomic contributions, cell volume, sampling ensemble, and correlation window are supplied by the chosen calculation. `ConservativeStressEvaluator` provides an energy-strain stress interface, and the MD trajectory supplies ordered mechanical states used by a separately defined stress-correlation estimator.

The source-to-coefficient path stores the tensor component, numerical time series, integration method, estimated coefficient, and provenance.

## 14. Viscosity Reference: Cantor, Ward, and Moynihan

The FLiBe source register contains `FLIBE-PRIMARY-CANTOR-WARD-MOYNIHAN-1969-VISCOSITY`, corresponding to Cantor, Ward, and Moynihan, *Journal of Chemical Physics* 50, 2874–2879 (1969), DOI `10.1063/1.1671478`.

The study reports molten BeF2–LiF viscosity using coaxial-cylinder viscometry, with reported compositions covering `36–99 mol% BeF2` and temperature measurements within the study's stated ranges. It provides composition- and temperature-dependent viscosity observations and analysis of viscous flow in relation to the BeF2 network structure.

A reference entry imported from the study identifies the individual measured mixture composition, temperature, viscosity unit, source table or figure, measurement procedure, and reported uncertainty. An interpolated or parameterized relation records its transformation from those source observations.

## 15. Thermal Conductivity

For temperature field `T` and conductive heat flux `q`, the isotropic Fourier constitutive relation is:

`q = -kappa grad(T)`.

The thermal conductivity `kappa` has SI unit `W/(m*K)`. For mass density `rho > 0` and a declared positive specific heat capacity `c_p`, define thermal diffusivity:

`alpha_T = kappa / (rho c_p)`.

`alpha_T` has unit `m^2/s`. A thermal engineering calculation associates `kappa`, `rho`, and `c_p` with compatible composition, temperature, pressure, material state, and constitutive conventions.

## 16. Green–Kubo Thermal Conductivity

For a stationary isotropic equilibrium system with total microscopic heat-current vector `J_Q`, cell volume `V`, and temperature `T > 0`, a Green–Kubo expression is:

`kappa = [1/(3 k_B T^2 V)] integral_(0→infinity) <J_Q(0) · J_Q(tau)> d tau`.

Here `J_Q` is the total heat current under the chosen microscopic energy-partition, convective subtraction, and component convention. A heat-flux-density convention requires its corresponding volume normalization.

The calculation record includes the microscopic heat-current definition, sampling ensemble, material state, volume history, correlation estimator, quadrature method, and uncertainty representation.

## 17. Thermal-Conductivity Sources: Cooke

The FLiBe register includes `FLIBE-PRIMARY-COOKE-1971-THERMAL-CONDUCTIVITY`, citing Cooke's measurements reported in *Molten-Salt Reactor Program: Semiannual Progress Report for Period Ending August 31, 1971*, `ORNL-4728` (published 1972), section 5.2.

The registered FLiBe mixture is approximately `66 mol% LiF : 34 mol% BeF2`. The report describes thermal-conductivity measurements using a variable-gap technique over the reported solid and liquid temperature regions.

`FLIBE-METHOD-COOKE-1973-VARIABLE-GAP` refers to Cooke, *Development of the Variable-Gap Technique for Measuring the Thermal Conductivity of Fluoride Salt Mixtures*, `ORNL-4831` (1973). The experimental-property record and the measurement-method record retain their individual source roles.

## 18. Electrical Conductivity and Ionic Currents

For electrical field `E` and electrical current density `J_e`, an isotropic linear law is:

`J_e = sigma_e E`.

Electrical conductivity `sigma_e` has unit `S/m`. For ionic species with effective transported charge `q_i`, define a microscopic total charge current:

`I_e(t) = sum_i q_i v_i(t)`.

Under the corresponding stationary equilibrium and current conventions, an isotropic Green–Kubo expression is:

`sigma_e = [1/(3 V k_B T)] integral_(0→infinity) <I_e(0) · I_e(tau)> d tau`.

The charge assignment, correlation procedure, finite-size treatment, and material state are specified by the selected electrical transport model. `FLIBE_FORMAL_CHARGES` supplies the formal ionic-charge accounting of Li, Be, and F; an electrical current model declares the charge representation used in its microscopic operator.

## 19. Electrical-Conductivity Reference: Robbins and Braunstein

The register entry `FLIBE-PRIMARY-ROBBINS-BRAUNSTEIN-1970-ELECTRICAL-CONDUCTIVITY` refers to Robbins and Braunstein, *Electrical Conductivities and Ionic Mobilities in the Molten LiF-BeF2 System*, reported in `ORNL-4548` (1970).

The reported experiments cover molten LiF–BeF2 compositions and temperature-dependent electrical conductivity; the source analysis uses conductivity, transference-number, and density data to examine ionic mobilities.

An imported record identifies the measured conductivity or source-derived mobility, mixture composition, temperature, source position, unit, and the method used for the reported quantity. Collective charge-current and species self-diffusion calculations retain their individual observable definitions.

## 20. Correlated Ionic Transport

For an idealized independent-species conductivity estimate with species number density `n_s`, assigned transported charge `z_s e`, and species self-diffusion `D_self,s`, define the Nernst–Einstein expression:

`sigma_NE = [e^2/(k_B T)] sum_s n_s z_s^2 D_self,s`.

The derivation uses its independent-carrier and charge-transport assumptions. A direct current-correlation conductivity evaluates collective cross-species and same-species correlations under its specified charge-current model.

The two quantities are recorded with distinct estimator identifiers and their common material-state context. A correlation-factor or collective correction is introduced through an explicitly defined relation between the selected estimates.

## 21. Hydrogen-Isotope Diffusion and Solubility

Hydrogen-bearing species are identified independently as H-, D-, or T-containing chemical forms under the selected melt chemistry and boundary state. For an identified transported species `h`, define a diffusive concentration flux:

`j_h = -D_h grad(c_h)`.

For a selected dilute equilibrium dissolution model with partial pressure `p_h`, a linear solubility boundary relation is:

`c_h,surface = S_h p_h`.

`D_h` has unit `m^2/s`, while `S_h` has unit `mol/(m^3*Pa)` when `c_h` is molar concentration and `p_h` is pascal. The particular chemical species, reaction and speciation model, pressure convention, interface geometry, and applicable temperature range accompany each coefficient.

## 22. Deuterium Transport Reference: Anderl et al. 2004

`FLIBE-PRIMARY-ANDERL-2004-DEUTERIUM-TRANSPORT` refers to Anderl et al., *Journal of Nuclear Materials* 329–333, 1327–1331 (2004), DOI `10.1016/j.jnucmat.2004.04.220`.

The study reports deuterium transport measurements for molten `2 LiF : 1 BeF2` using a dual permeation-probe arrangement and fits a cylindrical transport solution to measured permeation transients. The publication reports these derived deuterium diffusion coefficients:

| Source temperature | Reported deuterium diffusion coefficient |
| --- | ---: |
| `600 °C` | `8.0e-10 m^2/s` |
| `650 °C` | `3.0e-9 m^2/s` |

The experimental record identifies the measured permeation response, fitted cylindrical transport operator, chemical-species conditions, temperature, salt composition, derived coefficient, and associated source uncertainty when available.

## 23. Tritium Permeation Reference: Calderoni et al. 2008

`FLIBE-PRIMARY-CALDERONI-2008-TRITIUM-PERMEATION` refers to Calderoni, Sharpe, Hara, and Oya, *Fusion Engineering and Design* 83, 1331–1334 (2008), DOI `10.1016/j.fusengdes.2008.05.016`.

The study reports tritium permeation experiments with molten `2 LiF : 1 BeF2` at temperatures within approximately `500–700 °C`, using a membrane-coupled permeation cell. Steady transport signals and transient responses provide the experimental inputs for permeability, diffusivity, and solubility determinations under the source's apparatus and model conventions.

A source entry retains membrane material and thickness, salt and gas-side boundary conditions, tritium-bearing species, temperature, source signal, transport-model parameters, and the derived property identity.

## 24. Diffusion–Solubility–Permeability Relation

For a one-dimensional steady solution–diffusion model across an effective thickness `L > 0`, with constant `D_h`, linear solubility `S_h`, and specified partial pressures `p_1` and `p_2`, the flux magnitude with the selected orientation is:

`J_h = (D_h S_h / L) (p_1 - p_2)`.

Define permeability for this convention as:

`P_h = D_h S_h`.

For `D_h` in `m^2/s` and `S_h` in `mol/(m^3*Pa)`, `P_h` has unit `mol/(m*s*Pa)`. A composite salt–membrane–gas system includes its identified interfacial and membrane resistances, chemical boundary conditions, and reaction/speciation operators.

The source record associates each inferred coefficient with the measured steady or transient signal and the particular mathematical transport model used for parameter identification.

## 25. Open-System Species and Heat Balance

For species concentration `c_s`, total species flux `J_s`, and volumetric source `q_s` within a control region `Omega`, the local balance is:

`partial_t c_s + div(J_s) = q_s`.

For a fixed control volume with outward normal `n`:

`d/dt integral_Omega c_s dV = -integral_(partial Omega) J_s · n dA + integral_Omega q_s dV`.

For heat and mechanical work, the associated energy balance records advective and conductive transport, boundary power, volumetric sources, and changing stored energy. A numerical engineering realization assigns its transport coefficients and boundary conditions to these flux operators through the selected continuum and engineering mapping contexts.

## 26. TransportCoefficient and Transfer Context

`TransportCoefficient` in `src/tr_eif/multiscale/transport_transfer.py` contains:

- `coefficient_id`: identified transport quantity;
- `value`: finite scalar stored as `float`;
- `unit`: declared property unit;
- `scale_id`: source or target model scale;
- `state_domain_id`: physical and computational state domain;
- `source_id`: parameter and data provenance.

`TransportTransferContext` stores `target_scale_id`, `mapping_id`, `normalization_id`, and `assumptions_id`. `TransportCoefficientTransferRecord` retains the source coefficient, target coefficient, and full context and enforces exact equality of source and target coefficient identifiers and target/context scale identifiers.

The public call is:

`evaluate_transport_coefficient_transfer(source, context, evaluator)`.

The selected evaluator computes the target coefficient using its registered physical mapping, source state, constitutive assumptions, and normalization procedure.

## 27. Deterministic Transfer Fixture

`tests/integration/test_multiscale_transport_transfer.py` supplies a numerical reference fixture with source coefficient:

`thermal_conductivity = 2.5 W/(m*K)` at scale `atomistic`.

Its evaluator returns:

`thermal_conductivity = 1.75 W/(m*K)` at scale `mesoscale`.

The fixture supplies `mapping-a`, `normalization-a`, `assumptions-a`, source and target state-domain identifiers, and their corresponding source identifiers. The integration test checks normalized identifiers, finite values, exact source/context binding, destination scale, and deterministic repetition.

These values are the explicitly supplied fixture inputs and outputs of the transfer evaluator.

## 28. FLiBe Molecular-Dynamics and Multiscale Coupling

For selected model parameters and a retained execution vector, `FLiBeTREIPModel` evaluates the conditioned interatomic energy through geometry, a directed interaction graph, node features, and continuous resonance descriptors. The energy-gradient force evaluator supplies mechanical forces to the selected trajectory integrator.

The transport source state records:

`configuration → conditioned energy → force evaluation → mechanical trajectory → MSD/VACF or current history → coefficient estimator`.

`FLiBeMultiscaleCoolantModel` supplies a structural mass-and-centroid hierarchy. A selected transport transfer maps an identified source coefficient to its mesoscale or continuum target domain while retaining state, normalization, source, and mapping identifiers.

## 29. Continuous Resonance and Balanced-Ternary Execution

For receiving oscillator `j`, a directed Kuramoto–Sakaguchi evolution is:

`d theta_j/dt = omega_j + kappa_j sum_(i→j) sin(theta_i - theta_j - gamma_j)`.

The continuous resonance state may enter a descriptor and execution-request mapping. The retained execution alphabet is `-1/0/1`, with active neutral `0` and separate committed legs for opposite-polarity routes:

`-1 → 0 → 1`.

`1 → 0 → -1`.

The trajectory trace identifies resonance integration times, request values, retained and pending execution states, guards, committed events, and the execution vector supplied to each energy or force evaluation. Transport estimators use the resulting mechanical state and time history under the selected sampling procedure.

## 30. Thermodynamic State Transfer and Uncertainty

Transport-source and target values are associated with composition, temperature, pressure, physical state, species or current definition, unit, method, and provenance. `ThermodynamicConsistencyContext` and `UncertaintyPropagationContext` bind selected cross-scale relations, normalization, state-domain identity, and uncertainty procedure.

For a differentiable mapping `y = f(x)` with covariance `C_x` and Jacobian `J`, a first-order uncertainty mapping is:

`C_y ≈ J C_x J^T`.

A data-derived transport coefficient records its measurement or simulation uncertainty and its estimator's numerical sampling and finite-size contributions using separately identified quantities and correlation assumptions.

## 31. Numerical Qualification and Reproducibility

A reproducible transport study specifies:

- source publication, data location, method, observable, and provenance;
- LiF–BeF2 composition and any added transported chemical species;
- temperature, pressure, material phase, preparation, and boundary conditions;
- atomic inventory, simulation cell, periodic images, masses, and sampling times;
- interatomic model, graph cutoff, force evaluation, resonance, and execution inputs;
- particle selection, coordinate unwrapping, time origins, and trajectory ensemble;
- correlation or displacement estimator, fit or quadrature interval, and units;
- current, stress, and heat-flux definitions when used;
- source coefficient identity, uncertainty and normalization;
- target scale, constitutive mapping, thermodynamic domain, and engineering boundary;
- numerical precision, convergence tests, deterministic replay inputs, and output records.

Exact structural invariants apply to atom identity, sample and coefficient identifiers, scale correspondence, and ternary execution states. Floating-point comparisons use fixed numerical criteria linked to their calculation method.

## 32. Executable Interface Index

| Role | Repository path |
| --- | --- |
| FLiBe composition and species | `src/tr_eif/flibe/composition.py`, `src/tr_eif/flibe/species.py` |
| FLiBe configuration and thermodynamic state | `src/tr_eif/flibe/configuration.py`, `src/tr_eif/flibe/thermodynamic_state.py` |
| FLiBe mass and formal-charge records | `src/tr_eif/flibe/mass.py`, `src/tr_eif/flibe/charge.py` |
| FLiBe energy model | `src/tr_eif/flibe/tr_eip.py` |
| Mechanical state and trajectory | `src/tr_eif/md/state.py`, `src/tr_eif/md/trajectory.py` |
| MSD and VACF observables | `src/tr_eif/md/transport.py` |
| Interatomic energy and force | `src/tr_eif/energy/model.py`, `src/tr_eif/energy/force_evaluator.py` |
| Stress evaluation | `src/tr_eif/energy/stress_evaluator.py` |
| Transport coefficient and transfer | `src/tr_eif/multiscale/transport_transfer.py` |
| Thermodynamic consistency | `src/tr_eif/multiscale/thermodynamic_consistency.py` |
| Uncertainty propagation | `src/tr_eif/multiscale/uncertainty_propagation.py` |
| Mesoscale and continuum closures | `src/tr_eif/multiscale/mesoscale_closure.py`, `src/tr_eif/multiscale/continuum_closure.py` |
| Engineering boundary interface | `src/tr_eif/multiscale/engineering_boundary.py` |
| FLiBe coarse structural hierarchy | `src/tr_eif/flibe/multiscale_coolant.py` |
| MD resonance and ternary propagation | `src/tr_eif/md/resonance_propagation.py`, `src/tr_eif/md/ternary_propagation.py` |
| FLiBe material sources | `docs/references/flibe_sources.md` |
| MD transport-method sources | `docs/references/molecular_dynamics_sources.md` |

## 33. Executable Test Index

| Scope | Repository test path |
| --- | --- |
| Trajectory MSD and VACF | `tests/integration/test_molecular_dynamics_transport.py` |
| Multiscale transport transfer | `tests/integration/test_multiscale_transport_transfer.py` |
| Multiscale thermodynamic consistency | `tests/integration/test_multiscale_thermodynamic_consistency.py` |
| Multiscale uncertainty propagation | `tests/integration/test_multiscale_uncertainty_propagation.py` |
| Continuum and engineering interfaces | `tests/integration/test_multiscale_continuum_closure.py`, `tests/integration/test_multiscale_engineering_boundary.py` |
| FLiBe TR-EIP model | `tests/integration/test_flibe_tr_eip.py` |
| FLiBe multiscale hierarchy | `tests/integration/test_flibe_multiscale_coolant_closure.py` |
| FLiBe source comparison | `tests/integration/test_flibe_reference_comparison.py` |
| Trajectory conservation | `tests/conservation/test_md_trajectory_energy.py` |

## 34. Chapter Integration

The FLiBe transport-property representation connects source-specific viscosity, thermal conductivity, electrical conductivity, species diffusion, solubility, and permeation to typed material states and numerical observables. Atomistic MSD and VACF series and externally selected coefficient estimators feed explicit transport records and their scale-transfer contexts.

Three-dimensional mechanical trajectories, continuous resonance, active balanced-ternary execution, thermodynamic exchange, and continuum boundary conditions are linked through identified sampling and mapping operators. Each resulting coefficient retains its observable, transported entity, composition, physical state, units, source, and numerical procedure.
