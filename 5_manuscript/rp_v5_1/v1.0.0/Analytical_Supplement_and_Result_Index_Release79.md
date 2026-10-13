# Analytical supplement and complete result index

Author-review material, 13 October 2026. These deterministic calculations were developed **after** the main simulation. They explain the frozen generator; they are not a newly prespecified endpoint, a new random validation sample, a new interval method or a proof of exact Welch coverage. The original manuscript and all primary numerical results are preserved; the current revision integrates a disclosed explanation.

## Random membership preserves the mean but adds target variation

Let a complete module have coefficients `b_1,...,b_K`, complete mean `theta_full`, and a uniformly sampled subset O of size m without replacement. The observed target is

`theta_observed(O) = sum_{g in O} b_g / m`.

Each position is included with probability m/K. Therefore

`E_O(theta_observed) = theta_full`.

Writing `S_b^2 = sum_g (b_g-theta_full)^2/(K-1)`, the finite-population variance identity is

`Var_O(theta_observed) = (1-m/K) S_b^2 / m`.

This algebraic identity is not a new general module-size experiment. In the frozen sparse M1 mechanism, K=5, m=3 and `b=(1,1,0,0,0)`. The ten equiprobable masks give:

| Observed target | Number of masks | Probability |
| --- | --- | --- |
| 0 | 1 | 1/10 |
| 1/3 | 6 | 6/10 |
| 2/3 | 3 | 3/10 |

Thus `E_O(theta_observed)=2/5=0.4`, `S_b^2=3/10`, and `Var_O(theta_observed)=1/25=0.04`. Enumeration of all ten masks and the variance formula agree as exact rational numbers. A single mask is shared across all donors in a replicate. Its target displacement is consequently not an independent within-donor fluctuation that disappears when more cells or donors are averaged.

Uniform coefficients or complete membership have zero membership-target variance. The sparse direct-effect experiment was performed only in this five-member module. Gene detectability, condition-specific masks and expression-dependent missingness were not modeled.

## Conditional expression uncertainty differs from complete target uncertainty

For the A/B independent-factor, fixed-count mechanism, the score with m observed genes has residual cell variance

`nu_m = gamma + (1-rho-gamma)/m`.

Its within-donor cell-score covariance is `rho + nu_m` on the diagonal and `rho` off the diagonal. The donor mean has variance

`v_d = rho + nu_m/N_d`.

With n donors in each arm, the equal-donor contrast has conditional noise variance

`V_noise = sum_{d in both arms} v_d/n^2`.

This expression was independently checked by forming each donor's cell-score covariance matrix and evaluating its quadratic form with cell weights `1/(n N_d)`. Across all 160 A/B scenarios and four modules, the 640 variance rows agreed with the rational formula to a maximum absolute difference of 1.11×10^-16. Agreement with the frozen single-donor helper was also checked, but it was not the independent derivation.

In these mechanisms, conditional on a mask, the contrast has expectation `theta_observed(O)` and the expression factors are independent of the mask. The conditional noise variance depends on m, not on which positions are retained. The law of total variance then gives

`E(hat_theta - theta_full) = 0`,

`E[(hat_theta - theta_observed)^2] = V_noise`,

`E[(hat_theta - theta_full)^2] = V_noise + Var_O(theta_observed)`.

The membership term can therefore be absent from the within-arm uncertainty used by a Welch comparison, despite an unbiased full-target point estimator over masks. The shared mask changes the case-group mean; it does not generate corresponding within-arm donor dispersion. This distinguishes correct conditional targeting from uncertainty about a randomly changed target.

| Frozen M1 coordinate | Conditional expression variance | Membership-target variance | Full-target total variance |
| --- | --- | --- | --- |
| A062: n=4, rho=0.4, repeating counts, partial sparse | 421/1920 = 0.2192708333 | 1/25 = 0.04 | 2489/9600 = 0.2592708333 |
| A126: n=12, rho=0.4, repeating counts, partial sparse | 103/1440 = 0.0715277778 | 1/25 = 0.04 | 803/7200 = 0.1115277778 |
| A078: n=12, rho=0, equal counts, partial sparse | 7/1800 = 0.0038888889 | 1/25 = 0.04 | 79/1800 = 0.0438888889 |

A126 remains the prespecified main-coordinate example, with previously reported observed/full coverage of 94.90%/88.54%. A062 illustrates the smaller main-coordinate gap. A078 is retained solely as a post-main full-design explanatory boundary, not substituted into the abstract or main figure. The membership variance stays fixed while expression uncertainty varies, explaining why a low average bias does not settle the coverage question. The decomposition alone does **not** derive these empirical coverage percentages, establish exact Student-t calibration or validate a proposed correction.

The 1280 correspondence rows compare the existing complete/observed-target mean squared errors with these variances, using the recorded Monte Carlo standard errors. The maximum absolute standardized discrepancy was 3.166. No joint acceptance claim was based on all correlated diagnostics falling within individual 95% intervals; such a rule was neither prespecified nor statistically appropriate. These were checks against already available summaries, not new simulations or independent experiments.

The variance equations use only second moments and apply to the tested Gaussian and unit-variance Laplace factors under the stated A/B conditions. They are not a normality proof for Laplace contrasts. Disjoint modules still share donor and cell factors, so agreement with these variance formulas also supplies no general BH-control theorem. The independence assumptions do not hold for informative C counts, and these formulas were not applied to that block.

## Population ratios and finite sample ratio expectations in C

Write `U=sqrt(3/2) Z`, where Z is equally likely to be -1, 0 or 1. Case counts are N=5,20,80 in that order; control counts are reversed. Both arms have `E(N)=35`. In the case arm,

`E(NZ)/E(N) = 75/105 = 5/7`;

the control value is its negative. With rho=0.4, the population contrast shift is

`Delta_population = sqrt(0.6) * (5/7 - (-5/7)) = 1.1065666703`.

For n finite donors, the case expectation is instead

`R_n = E[sum_i N_i Z_i / sum_i N_i]`.

Two exact algorithms were used: a factorial-weighted sum over multinomial compositions and an integer convolution over ordered draws of `(N,NZ)`. Case and control mappings were evaluated separately, giving opposite rational expectations. The convolution represents all 81 ordered case draws at n=4 and all 531441 at n=12 through 15 and 91 distinct states, respectively; these counts are probability-support calculations, not simulated donors or new observed data.

| n per group | Finite-n contrast shift | Population contrast shift | Finite minus population |
| --- | --- | --- | --- |
| 4 | 0.8475456225 | 1.1065666703 | -0.2590210479 |
| 12 | 1.0436783188 | 1.1065666703 | -0.0628883515 |

The two algorithms agree as exact fractions before multiplication by `sqrt(0.6)`; results also agree with the original frozen helper within 10^-12. This independently checks the target definition, not the generator itself. The population target is not replaced by a finite-n expectation as a primary endpoint. Neither a correct mean nor target relabelling repairs the dependence ignored by naive cell-level intervals.

## Portable reproduction and its limits

A virtual-only Tier A packet was extracted to a newly created temporary directory and tested with the installed Python 3.12.14/NumPy 2.3.5 runtime in isolated mode. Python audit events blocked original-workspace access and network operations. Seven explicit negative tests checked three normalized forbidden-path variants, two network events and wrong source size/hash; these were synthetic guard tests, not attempted network communication or patient-file reads.

The packet contains 576 **existing** replay fixtures: IDs 0,2499,4999 per scenario. Reconstructed input SHA values, metadata and method fields matched. Joining all 192 existing scenario summaries reproduced the 4608 target, 384 FDR and 2304 paired rows, including the export's frozen `scenario_parameters` annotation. This is not a new full readback or rerun of all 960000 raw instances.

Seven synthetic figures—Figure2, Figure3 and S1–S5—were reconstructed with unchanged plotting instructions, explicit runtime-root injection and omission of patient-related setup/figures. All 14 PNG/SVG objects matched canonical bytes, and all seven panel-source structures matched. New source JSON documents the different package scope, so its bytes are not claimed identical to original provenance objects. All five analytical output files matched between the source workspace and extracted run.

Original generator, numerics, runner and plotting source files remained byte-identical. A transparent adapter replaces the historical full-workspace guard with a package-payload guard; it does not pretend that omitted historical inputs are present. The original full workspace guard was not weakened or overwritten. PBC derived inputs, Figure4, the PBC-containing overview Figure1, third-party article files and skill distributions are excluded from Tier A. The prior PBC results remain in the local manuscript as a separate negative illustration, with all four inherited maxT-adjusted P-values equal to 1.0, not a required input for synthetic reproduction.

This is pinned-runtime, same-OS portability, not a clean OS image, cross-platform certification, independent generator implementation or biological validation. The owner subsequently authorized public release, with MIT software and CC BY 4.0 manuscript/figures/synthetic-result licenses; reproduction alone did not confer that authority. Exact source locators, checks and artifact identities are provided in the local Stage77 receipts and separate Tier A manifest.


## Complete result inventory

- `ALL_4608_TARGET_ROWS.json`: 192 scenarios × 2 methods × 4 modules × 3 targets. Coverage, bias, RMSE, CI length, generated/valid/failed denominators and MC uncertainty are retained.
- `ALL_384_FDR_ROWS.json`: 192 scenarios × 2 methods. Each is one four-module family result, not four independent module observations.
- `ALL_2304_PAIRED_ROWS.json`: 192 scenarios × 4 modules × 3 targets. Coverage and CI-length differences between methods share the same generated inputs.
- `ALL_192_SCENARIOS_AND_MASK_LOCATORS.json`: frozen parameter catalog, identities of all192 scenario summaries and the3840-chunk raw-record manifest. Complete empirical member-mask frequencies remain in each original `SCENARIO_SUMMARY.json`; they are not replaced with a sample of masks.
- `WITHIN_METHOD_TARGET_COVERAGE_PAIRING.json` in the parent directory: 32 secondary paired target comparisons across16 unchanged main-display scenarios. It records the320 existing chunks read and80000 unique existing instances. No simulation was added.

These linked scenario summaries and raw gzip blocks remain in the project/Stage74 archive; the Stage75 delta is not a full raw-data mirror. The tested virtual-only packet provides the specified replay and aggregate reconstruction tasks, not a full raw archive mirror.

## Secondary pairing calculation

For targets A and B, each valid existing replicate supplies I_B−I_A, where I indicates that the same interval covers that target. The mean is coverage(B)−coverage(A); MCSE is the sample standard deviation of these differences divided by sqrt(5000). The displayed secondary interval is mean±1.96 MCSE. It is Monte Carlo uncertainty, not a clinical effect interval and not a subtraction of independent Wilson endpoints. The analysis was added after the main output existed on coordinates frozen earlier; it is explicitly secondary.

## Supplementary figure legends

**Supplementary Figure S1. Coverage in all 128 A scenarios.** Panels a/b display cell/donor results for M1 in frozen catalog order, evaluating the same intervals against the complete donor and matching observed targets. Filled circles denote complete targets and open triangles matching targets. Error bars are Wilson 95% Monte Carlo intervals over 5000 instances. Only every sixteenth scenario label is printed; all scenarios are displayed and their parameters are in the complete JSON tables. The horizontal reference is 95%.

**Supplementary Figure S2. Background expression detection in all 32 B scenarios and four modules.** Panels a–d correspond to M1–M4. Orange squares and blue circles show raw matching-target rejection by cell/donor Welch methods, with Wilson 95% Monte Carlo intervals. A nonzero background expression target is not a statistical null despite a zero direct core component. Complete truth formulas, overlap and eta parameters are specified in Methods and the catalog; no background-detection point is relabelled as a direct mechanism effect.

Abbreviations: G/L, Gaussian/unit-variance Laplace noise; n, donors per group; r, donor variance component rho. All/partial refer to observed membership coverage.

**Supplementary Figure S3. Coverage in all 32 C scenarios.** Cell/donor panels show complete donor versus matching population-cell/observed-donor coverage, with Wilson 95% Monte Carlo intervals. Population targets and finite-n estimator expectations remain distinct. Parameters and all 5000-replicate denominators are retained; the display is not averaged across mechanisms.

**Supplementary Figure S4. Four-module Type I error across all 64 A null design labels.** Panels correspond to M1–M4; both methods use their matching null targets and Wilson 95% Monte Carlo intervals. Each point has 5000 instances. Some labels coincide as effective null generating mechanisms, and are not independent biological mechanisms. Larger modules contain no comparable direct signal experiment, so this is not a test of a general module-size signal law.

Abbreviations: G/L, Gaussian/unit-variance Laplace noise; n, donors per group; r, donor variance component rho. All/partial refer to observed membership coverage.

**Supplementary Figure S5. Complete sparse-member sensitivity rather than primary-coordinate reselection.** (a) All 16 sparse delta=0.4 partial-coverage A scenarios show donor interval coverage against complete and observed targets. (b) Their 16 full-member counterparts show complete-target coverage; x labels identify the associated partial scenario, while source rows identify the actual full scenario. Wilson 95% Monte Carlo intervals use 5000 instances per point. The full set was in the frozen supplement scope; the author-review display was assembled after main execution. No extremal scenario replaced the frozen Figure3 main coordinates.

Abbreviations: G/L, Gaussian/unit-variance Laplace noise; K, full module member count; n, donors per group; r, donor variance component rho.
