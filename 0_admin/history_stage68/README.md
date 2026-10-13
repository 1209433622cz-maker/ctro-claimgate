# CTRO ClaimGate

An original, prospective meta-research project on **claim–evidence alignment in chronic-disease single-cell and single-nucleus transcriptomics**. Its intended empirical contribution is a probability-sampled audit of one rule-selected claim per eligible paper version, with source-linked biological-unit and validation-identity records. It is not a narrative review, a completed disease-mechanism paper or an observed prevalence study.

**Current release: Stage68 public restructuring, 12 October 2026.** This repository now publishes selected Stage67 author-review design material, project-owned frozen aggregate development results and four clearly separated figure objects. Publication here does not approve the protocol, validate the instrument or authorize journal submission.

## Start here

- [Current scientific status](0_admin/SCIENTIFIC_STATUS.md) and [next scientific decision](0_admin/NEXT_STAGE.md)
- [English prospective design manuscript](5_manuscript/author_review/CTRO_Stage67_Prospective_Design.md) and [supplement](5_manuscript/author_review/CTRO_Stage67_Supplementary_Design.md)
- [Results interpretation](3_results/README.md) and [figure/panel selection](4_figures/FIGURE_AND_PANEL_STORYBOARD.md)
- [Stage67 public scientific audit](7.Report/Stage67_PUBLIC_SCIENTIFIC_AUDIT.md) and [Stage68 restructuring action report](7.Report/Stage68_PUBLIC_RESTRUCTURE_ACTION_RECORD.md)

## The formal empirical study has not started

RP v4 controls conditional design development. RP v3 retains the operative execution lock until a genuinely approved final protocol replaces it; V4.1 proposals are not adopted merely by editing a manuscript.

| Requirement | Status | Evidence still needed |
| --- | --- | --- |
| V4-G0: scope and estimand | PARTIAL | Independent population, index-claim and statistical-identification decisions |
| V4-G1: retrieval and coverage | HOLD | Clinical eligibility, independent PRESS review and approved bibliographic frame |
| V4-G2: content validity | HOLD | Two genuine independent content judgments and operable nominal categories |
| V4-G3: people and calibration | HOLD | Qualified named reviewers/coders, conflicts/exposure, consent, capacity and authorized calibration |
| V4-G4: formal study | LOCKED | Approved protocol/registration, frozen frame, justified probability design and analysis plan |
| V4-C5: conditional author computation | SEPARATE HOLD | Exact historical input, output target, participant mapping and runtime/database binding |

Confirmed external reviewers, sent controlled packets and independent opinions: **0 / 0 / 0**. Formal probability sample, independent coding and primary claim-state endpoint: **not produced**. Public release and engineering tests are not independent scientific review. Journal submission remains HOLD.

## Repository architecture

The eight root collections follow the owner's requested structure. `7.Report` deliberately matches the screenshot; the local workspace uses `7_report` and is not renamed by this release.

```text
0_admin/      Scientific authority, current status, gates and next-stage requirements
1_data/       Public data-access/input contracts and schemas; no raw expression data
2_code/       Safe-source tools, tests, public-contract validator and figure renderer
3_results/    Frozen aggregate development summaries and hypothetical planning sources
4_figures/    Fig1–Fig8 storage roles; selected design/historical figures and provenance
5_manuscript/ Public author-review prospective design, supplement and narrative architecture
6_release/    Exact public manifest, provenance and submission-preparation HOLD
7.Report/     Public-safe action reports and dated development history
```

`README.md`, `CONTRIBUTING.md`, `.gitignore` and `.gitattributes` remain at the root. Older `docs`, `workflow`, `src`, `submission` and `checksums` paths were reorganized into these collections with ordinary Git history retained. See [path mapping](0_admin/PUBLIC_PATH_MIGRATION.tsv). Previous commits remain accessible; this is **not another repository deletion/recreation or a force push**.

## Scientific question and denominator

For one index claim fixed independently of its eventual evidence rating, what is the distribution of four candidate public-evidence states among papers in an approved human non-oncology chronic-disease frame?

| Candidate nominal state | Meaning and boundary |
| --- | --- |
| Aligned | Accessible evidence supports the original proposition within its qualifiers; not a certificate of universal biological truth |
| Narrower supported | A specified weaker proposition is supported while the original wording remains recorded |
| Material mismatch | An identifiable consequential incompatibility or inferential overextension, not inferred from missing files alone |
| Not evaluable | Insufficient accessible/interpretable evidence for a fixed claim in a confirmed eligible paper |

Materiality and precedence remain unapproved. These labels are not an ordinal ladder or validated quality scale. Unknown eligibility and unfixed claim identity remain outside this four-state denominator. Known sampling weights alone do not correct selective eligibility/claim resolution. Identification envelopes are not confidence intervals. Pilot-driven adaptation requires the actual joint selection probabilities and approved variance method.

The provisional scope considers original human non-oncology chronic-disease scRNA/snRNA papers from 1 January 2022 to 30 September 2026, with descriptive disease-associated cell-state and inferred communication claim families. The scope, frame, version rules and claim-selection rule are not final. Neither conceptual guidance nor a reproducible query supplies a population mismatch estimate.

## What the existing results actually support

The [15-row evidence adjudication register](3_results/scientific_result_adjudication.tsv) distinguishes historical analysis, synthetic validation, current design and separate C5 work. Frozen aggregate tables are under [frozen development sources](3_results/frozen_development/README.md); they are not formal R1 sample records.

- **SSc:** discovery bulk IMPORT association and a background-adjustment-dependent independent baseline association did not establish donor-level fibroblast localization. A newly disclosed self-predictor defect makes some full-model background-program comparator rows scientifically uninterpretable; the canonical transport hard-gate FDR was calculated separately.
- **PBC:** four cholangiocyte ciliary modules did not meet frozen discovery criteria in four donors per group; this is not an equivalence result.
- **IgAN:** retrieval-complex discovery g = −1.534 reversed to +0.291 in independent replication, failing the frozen negative-direction criterion.
- **Endometriosis:** strong phase-adjusted transport contrasts attenuated in a conditional model with maximum VIF 54.83. The same-cohort model is not independent replication, and attenuation does not prove causal confounding.
- **LN:** corrected canonical identifier mapping remained NO_GO; the invalid earlier symbol-only run is not included as valid evidence.
- **HFpEF:** stopped at measurement/independent-validation feasibility before an expression kill-test; there is no measured negative membrane-contact-site effect.
- **ORGAXIS:** both frozen toy benchmark versions failed primary acceptance. V2 accuracy 265/300 = 0.883 was below 0.90 and advancement recall 32/50 = 0.64 below 0.80, despite exact prediction recomputation. No V3 was tuned to rescue the result.

These selected projects are not a probability sample of diseases, hypotheses or papers. A NO_GO is a development decision, not universal biological absence. Deterministic calculation does not establish scientific validity, and historical cases cannot fill the future R1 Results section.

## Figures: four objects, not eight completed results

| Public storage | Object | Permitted interpretation |
| --- | --- | --- |
| Fig1 | Manuscript Figure 1, prospective design | Proposed sequence and denominator; no observed counts |
| Fig2 | Supplementary S1, hypothetical precision/workload | Assumption-based planning; no observed yield or four-state CI |
| Fig3 | Historical H1, selected frozen coefficients | Separate SSc/IgAN/Endometriosis development contrasts; not R1 primary results |
| Fig4 | Historical H2, frozen synthetic failure precision | Original V1/V2 failure and thresholds; no new simulation or human validation |
| Fig5–Fig8 | Explicitly unfilled/reserved or excluded roles | No implied scientific panels; third-party, QA and software images are not uploaded |

![Prospective Figure 1 — no empirical counts](4_figures/Fig1/Figure_1_Prospective_Design.png)

PNG and editable SVG exports are provided. Historical H1 discloses the model, cohort-specific scale and uncertainty limits; H2's “Independent” title refers to computational rechecking, not a second human reviewer. Read [legends and boundaries](4_figures/HISTORICAL_LEGENDS_AND_BOUNDARIES.md) before reusing a panel. The local 517-asset catalog was a provenance/usage census, not 517 publishable result figures; excluded source-paper images and software fixtures are not mirrored here.

Public UTF-8 text, including SVG markup, uses Git-consistent LF line endings; original source and public byte hashes are distinguished in the provenance register. PNG bytes, SVG geometry/labels and frozen numeric values are preserved. Private/local masters are not modified by this normalization.

## Verification and reproducibility

Python 3.10+ and the standard library suffice for integrity and safe-source tests:

```bash
git clone https://github.com/1209433622cz-maker/ctro-claimgate.git
cd ctro-claimgate
python -B 2_code/safe_source/validate_public_contract.py
python -B -m unittest discover -s 2_code/safe_source -p "test_*.py" -v
```

The manifest checks exact distributable file membership, byte sizes and SHA-256; it excludes itself, Git internals and transient caches. Validation also checks the eight-folder structure, nominal/gate boundaries, safe file types, manuscript links and private-path/credential screens. These are engineering checks, not biological reproduction or content-validity tests.

The optional historical display renderer uses Matplotlib/NumPy and frozen summary coordinates only:

```bash
python 2_code/figures/render_historical_exhibit.py --output-dir /path/to/new/empty/output
```

It does not load expression matrices, refit models, change gates or generate new synthetic predictions. Original main/S1 masters are retained, not claimed to be rebuilt by this renderer. Planning sources carry `ASSUMPTION_NOT_OBSERVED`; frozen tables retain their different model and multiplicity definitions.

## Public data and manuscript boundaries

This is a curated public package, not a full workstation mirror. It excludes patient/cell-level expression and mappings, raw upstream downloads, third-party full text and images, author-repository clones, software environments, reviewer identities/forms/packets, correspondence, local absolute-path inventories, QiTeng's third-party skill package and private release ZIPs. `1_data` contains contracts and documentation, not missing or fabricated data.

The published English text is explicitly **AUTHOR REVIEW — NOT FOR SUBMISSION**, a prospective design with unresolved scientific approvals. It is not a registered protocol, accepted manuscript, complete empirical study or new journal-compliant DOCX/PDF export. The historical bounded-note narrative is a separate author option, not an adopted replacement for R1. [Submission readiness](6_release/submission_preparation/README.md) remains HOLD.

## Next scientific decision

`R1_00D_STAGE56B1_REAL_REVIEWER_ROSTER_AND_DISPATCH_AUTHORIZATION`

Obtain real scope/statistical, clinical, PRESS and two independent content opinions. Record qualifications, independence, conflicts/exposure, consent and capacity. Authorize each named recipient and exact packet before dispatch. Decide **GO_V4 / GO_NARROW / STOP_R1** before formal sampling and outcome access. If the construct or resources fail, narrow prospectively to objective biological-unit/validation-identity questions or stop; more internal PASS reports do not replace this evidence.

## Rights, contributions and citation

No project-wide license, DOI, ethics determination, journal acceptance or priority claim is asserted. Public visibility is not permission to reuse material without considering its terms. Obtain upstream data from the original repositories and respect their licenses. QiTeng was used locally for guarded manuscript/figure construction; its release is not redistributed.

For a reference to these design materials, cite the repository URL, exact commit and access date, describing them as an unapproved prospective design and bounded development record. Do not cite toy results as population estimates. Contributions must preserve the evidence/authority boundaries; see [CONTRIBUTING.md](CONTRIBUTING.md). Never post identities, raw data, controlled forms or credentials in issues or pull requests.
