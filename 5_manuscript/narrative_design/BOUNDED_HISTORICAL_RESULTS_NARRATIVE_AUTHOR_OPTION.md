# Optional bounded historical-results narrative — not adopted as the R1 manuscript

AUTHOR DISCUSSION ONLY. This is a source-bound Results draft for a different, selected development-case report. It does not change the active project, authorize a submission, or constitute a complete methods paper. Case selection, pre-outcome protocol versions, uncertainty and chronology must be independently reconstructed before such an article is chosen.

Possible working title: **Frozen stopping rules in organelle-axis transcriptomic development: selected disease cases and failed synthetic validation**.

## Results narrative candidate

### Advancement failures arose at different inferential steps

Six historical disease–organelle development projects stopped under their own frozen criteria, but they did not produce six comparable biological null experiments. Five projects reached expression-based testing; the HFpEF–membrane-contact-site project stopped at measurement and validation feasibility before an expression contrast. The cases were selected during project development and do not represent a probability sample of disease hypotheses, published papers or failed analyses. We therefore describe their distinct stopping points rather than estimate a pooled failure rate.

### Tissue-level SSc association did not establish fibroblast localization

In the SSc discovery cohort, the canonical IMPORT module had an adjusted coefficient of 0.711 within-cohort SD (SE 0.276; P = 0.00990; four-module hard-gate FDR = 0.0396) across 81 baseline donors. An independent bulk baseline cohort contained 157 donors. Its unadjusted coefficient was 0.069 (P = 0.694), whereas the background-adjusted coefficient was 0.289 (SE 0.086; P = 0.000781; replication FDR = 0.00156). Thus, the replication result was model-dependent rather than a uniformly apparent case–control shift. Repeated longitudinal biopsies were not additional independent people.

Donor-level fibroblast pseudobulk from 12 SSc and 10 control donors did not reproduce the positive tissue-level direction after chemistry and log-cell-count adjustment: the coefficient was −0.467 (SE 0.393; P = 0.234). This did not establish absence of transport biology, but it did not support the fibroblast-localization advancement criterion (H1A). A retrospective code audit additionally identified canonical background-program outcomes included as their own predictors in certain full-model comparator fits. These degenerate comparator rows cannot substantiate axis specificity. The transport hard-gate FDR was calculated separately and was not recomputed or replaced in this narrative.

### Discovery and independent replication disagreed in IgAN

The RETRIEVER_CCC_WASH discovery module had Hedges g = −1.534 and an exact four-module maxT family-wise P = 0.00644, using 1,961,256 fixed-margin allocations. Independent replication yielded g = +0.291 rather than the frozen negative direction; the directional one-sided Welch P was 0.825 (two-sided P = 0.351). Twelve of the 13 frozen genes were measurable in replication, with WASHC1 unavailable. These data did not satisfy the frozen directional replication criterion (H1B). The two tests use different inferential families and should not be compared as if P values measured the size of a common effect. The frozen summary did not provide g confidence intervals, so none are invented in the display.

### Strong phase-adjusted Endometriosis contrasts were sensitive to conditional modeling

Among 75 cases and 34 pathology-free controls, phase-adjusted NPC-core, import and export coefficients were −1.090 (95% CI −1.411 to −0.769), −1.359 (−1.684 to −1.033), and −1.212 (−1.547 to −0.877) SD; each four-module maxT P was approximately 0.000100. Ran was not comparably shifted (0.057; CI −0.345 to 0.458; FWER P = 0.991). Adding background and response programs changed the respective coefficients to 0.124, −0.028 and 0.077, and no module satisfied the complete frozen advancement chain.

Maximum VIF in that conditional model was 54.83. Coefficient attenuation therefore cannot be interpreted as proof that causal confounding explains the primary signal: collinearity and conditioning on disease-mediated programs can change the meaning and stability of the coefficient. The conditional analysis uses the same cohort and is not independent replication (H1C). The recorded NO_GO remains a development decision, not a demonstration that nucleocytoplasmic transport is unchanged in all Endometriosis contexts.

### Small discovery studies and measurement feasibility imposed separate limits

The PBC cholangiocyte study compared four donors per group using 70 exact allocations. Four ciliary structural modules had Cohen d values −0.262, −0.348, −0.061 and +0.252, with maxT family-wise P = 1.0 for each. None met the frozen discovery requirements; these small-sample tests are not equivalence demonstrations. A low-cell donor remained a sensitivity record and could not rescue the primary criterion.

The corrected LN endosomal study restored the canonical Ensembl-based mapping to module coverages 5/5, 4/4, 12/13 and 8/8 before interpreting the authoritative run. Hedges g values were 0.248, 0.366, 0.270 and −0.223, with exact maxT P values 0.776, 0.588, 0.784 and 0.807 over 888,030 allocations. An invalid older direct-symbol run remains archived, not mixed into the corrected result. No module passed. In HFpEF, the available bulk and single-nucleus sources shared participants, and an external small cohort used aortic-stenosis comparators; neither resolved independent, phenotype-comparable validation of the stated membrane-contact-site proposition. A contact-compatible orthogonal measurement was also lacking. No HFpEF expression kill-test was performed.

### Reproducible synthetic computation did not meet acceptance requirements

In the separate balanced toy benchmark, V1 correctly classified 146 of 300 projects (accuracy 0.487; macro-F1 0.375) but advanced none of the 50 TRUE_ADVANCE projects. V2 improved accuracy to 265/300 (0.883) and macro-F1 to 0.881, yet remained below the frozen accuracy requirement of 0.90; advancement recall was 32/50 (0.64), below 0.80. Independently recomputed predictions had zero mismatches for both versions. Primary acceptance therefore failed despite deterministic and implementation-level agreement (H2). Wilson intervals in the historical audit summarize toy-benchmark proportions and do not provide real-world literature validity. No V3 was tuned to convert the frozen failure into a positive result.

## Discussion ceiling for this optional route

The useful conclusion is that a reproducible development workflow can expose different limits—measurement mismatch, discovery criteria, conditional-model fragility, failed cross-scale localization and directional replication—without turning every limit into biological absence. It is not a validated universal classifier, an estimate of overclaiming in published single-cell papers, or evidence that stricter gates necessarily improve real-world discoveries. The toy benchmark's advancement failures are themselves a limitation of the rule system.

H1 is a salience-selected display; the complete adjudication table retains all six projects and other outcomes. A full bounded note would need traceable pre-outcome thresholds, source-input identities, exact multiplicity definitions, uncertainty where available, overlap and selection history, and an explicit explanation of why these projects were included. This optional narrative must not be inserted into the prospective R1 paper as its primary empirical Results.
