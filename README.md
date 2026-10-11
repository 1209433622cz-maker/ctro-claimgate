# CTRO ClaimGate

CTRO ClaimGate is an original meta-research project developing a source-linked audit of mechanistic claims in human chronic-disease single-cell and single-nucleus transcriptomics. The intended empirical contribution is a probability-sampled, paper-level assessment of claim–evidence alignment, biological replication and validation independence. It is not a narrative review, a disease biomarker pipeline or a completed prevalence study.

This public repository contains curated project documentation and safe-source inspection utilities. It is not a mirror of the full local workspace. It contains no patient/cell expression data, third-party full text, cloned author repositories, controlled reviewer packets, private correspondence, software environments or unpublished manuscript files.

## Read this first: the empirical study has not started

Research Proposal v4 is conditionally active for **design development**. RP v3 retains the operative formal-execution lock until a final approved protocol replaces it. Internal integrity checks and publicly accessible materials do not authorize scientific execution.

| Requirement | Current status | What remains |
|---|---|---|
| V4-G0: scope and estimand | PARTIAL | Independent scope/statistical review, including unknown eligibility and index-claim selection |
| V4-G1: retrieval and coverage | HOLD | Clinical eligibility, independent PRESS review and approved frame construction |
| V4-G2: content validity | HOLD | Two genuine independent content reviews and category/claim-selection decisions |
| V4-G3: people and calibration | HOLD | Qualified named people, conflict/exposure records, consent, capacity and new authorized calibration |
| V4-G4: formal study | LOCKED | Approved protocol, registration, frozen frame, probability design and analysis plan |
| V4-C5: optional computational reproduction | SEPARATE HOLD | Exact author-input, output-target and historical runtime identity |

Confirmed external reviewers: **0**. Controlled packets sent: **0**. Independent review opinions received: **0**. No formal sample, independent coding or primary claim-state endpoint has been computed. Journal submission is not authorized.

The latest local administrative action is **Stage66, 12 October 2026**: a fresh whole-workspace audit, a byte-conserved author-review preparation package, and preparation of an owner-requested public repository replacement. Scientific gates are unchanged. The deletion request was denied because the current GitHub CLI authorization lacks `delete_repo`; the existing remote is unchanged and this replacement candidate is not published. Git history and accessible records are backed up locally. See [repository rebuild and audit](docs/STAGE66_REBUILD_AUDIT_AND_READINESS.md).

## Proposed scientific question

For one index claim selected by a prespecified rule in each eligible paper, what is the distribution of four proposed claim–evidence states?

- **Aligned:** public evidence supports the stated proposition within its qualifiers.
- **Narrower supported:** evidence supports a specified weaker proposition while the original wording is retained.
- **Material mismatch:** a consequential incompatibility or inferential overextension is identifiable.
- **Not evaluable:** a fixed claim in a confirmed eligible paper cannot be rated from accessible, interpretable public evidence.

These are **draft nominal categories**, not a validated ordinal scale. Their precedence and materiality rules require content review. Unresolved eligibility and an unfixed claim are process states; they must not be assigned to “not evaluable” to fill a row.

The proposed scope is peer-reviewed original human non-oncology chronic-disease papers using single-cell or single-nucleus transcriptomics, provisionally published from 1 January 2022 to 30 September 2026. Candidate claim families are disease-associated cell type/state and inferred intercellular communication. This scope, database coverage, version rules and family-selection rule are not final.

The observable distribution among resolved, eligible papers with fixed claims is not automatically the distribution among all genuinely eligible papers. A known sampling probability does not correct selective eligibility resolution or claim-selection completion. Sensitivity envelopes are not confidence intervals, and an adaptive pilot/main design requires probabilities and variance appropriate to the actual analytic selection process.

## What is useful already

### Historical gate-first bioinformatics work

Six disease–organelle projects were evaluated and not promoted under their own protocols: SSc–nucleocytoplasmic transport, PBC–primary cilium, IgAN–endosome, endometriosis–nucleocytoplasmic transport, lupus nephritis–endosome and HFpEF–membrane-contact sites. Their preflight, gene-set provenance, donor mapping, confounding controls and stopping records are reusable development resources. They are not a random literature sample, and a NO-GO is not a universal biological negative.

The ORGAXIS benchmark subsequently failed both its first and metric-harmonized synthetic validations under frozen criteria. A full methods-paper route was closed and further post-result V3 tuning was prohibited. A bounded negative-results note remains a separate paused route.

### Provenance and input-contract development

RP v3 introduced linked paper, claim, biological-unit, evidence, evaluation and computational-provenance records. Four C5 cases were selected for engineering development, not population inference. ENG04 reconciled donor and cell-annotation metadata and verified a software import/API environment. Its exact historical paired expression/metadata export and author-run database remain unbound. Reconstructed metadata and a processed H5AD are not treated as equivalent to author-original inputs without evidence.

### RP v4 planning, manuscript and audit work

Synthetic planning and finite-population examples identify workload, unknown-eligibility and adaptive-sampling risks. Their reproducibility demonstrates the arithmetic, not real eligibility yield, content validity or scientific approval. A local prospective English manuscript and supplement contain one design Figure 1 and one hypothetical Figure S1, with no empirical outcome figures. The current author-review package preserves these sources and adds readiness records; it is not journal ready.

The local full-file audit inventories sizes and SHA-256 values and applies format-aware checks. Its coverage and exceptions are reported explicitly. No duplicate cleanup is implied. The local Fig1–Fig8 folders also hold reference, software and QA assets; they do not imply eight scientific figures.

## Public repository layout

```text
README.md                         Project question, status, use and limits
CONTRIBUTING.md                    Contribution and scope boundaries
docs/                             Decisions, bounded audit summaries and next stage
workflow/                         Gate matrix, stage register and ENG04 input contract
submission/                       Public preparation outline and readiness matrix
src/                              Safe-source inspector, tests and contract validator
checksums/                        Exact public payload manifest
```

The public manifest lists every distributable payload file except itself. Git internals and transient Python caches are outside the payload. Older stage documents remain dated history; the current gate table above and [scientific status](docs/SCIENTIFIC_STATUS.md) govern interpretation.

## Local working architecture

The private/local workspace uses the following English-named collections. This is a navigation description, not a promise that these contents are publicly available.

| Folder | Purpose |
|---|---|
| `0_admin` | Protocol authority, current status, research plans and controlled governance |
| `1_data` | Source/working data, metadata, upstream inputs and engineering environments |
| `2_code` | Project-owned analysis, provenance, validation and audit scripts |
| `3_results` | Results, input receipts, audit inventories and test outputs |
| `4_figures` | Fig1–Fig8 collections with source identity and usage classification |
| `5_manuscript` | Historical outlines, prospective drafts and author-review preparation |
| `6_release` | Frozen deliveries and curated public working checkout |
| `7_report` | Detailed per-action reports and scientific checkpoints |
| `8_archive` | Preserved imports, replaced working copies and GitHub recovery backups |
| `8_reference` | Third-party publications, source materials and writing references |
| `9_version` | Changelog, manifests and transfer/version notes |

Exact file identities, work-record indexes, path redirects and reuse registers remain local because they include restricted paths and source information. Files are classified by purpose, provenance and rights, not just filename or extension. Historical frozen archives are retained unchanged.

## Verify the public package

Python 3.10 or newer is sufficient for the public checks; no third-party Python package is needed.

```bash
git clone https://github.com/1209433622cz-maker/ctro-claimgate.git
cd ctro-claimgate
python -B src/validate_public_contract.py
cd src
python -B -m unittest -v test_safe_source_inspector
```

The contract validator checks payload membership, byte counts and SHA-256, prohibited file types, retained formal locks and the submission boundary. The 28 safe-source tests exercise bounded metadata/source inspection. They do **not** reproduce upstream authors' findings, validate the classification instrument or establish a biological effect.

The source inspector is a read-only engineering aid, not an analysis pipeline. Read [reproducibility boundaries](docs/REPRODUCIBILITY_AND_DATA_BOUNDARIES.md) and [read-access scope](docs/READ_ACCESS_SCOPE.md) before adapting it. Do not execute source notebooks or infer expression representation from a processed filename alone.

## Interpretation and publication safeguards

1. A stage PASS concerns only its stated exit criterion. It is not independent scientific approval.
2. Methodological guidance cannot predetermine a real paper's rating.
3. Cells, libraries, sections and donors are distinct units; sample independence must be evidenced.
4. Orthogonal assays and new biological replication are different forms of support.
5. Tool agreement is not independent functional validation.
6. Reconstructed inputs, clean-install resources and historical author-run inputs have different identities.
7. Adjudicated consensus must not replace the original independent agreement record.
8. Purposive computational cases retain a separate denominator; their outcomes cannot estimate population reproducibility.
9. Synthetic planning values remain explicitly hypothetical.
10. Public release, document formatting and journal-readiness checks do not unlock formal research.

## Next scientific decision

The immediate target remains:

```text
R1_00D_STAGE56B1_REAL_REVIEWER_ROSTER_AND_DISPATCH_AUTHORIZATION
```

Record real expert identities, qualifications, independence, conflicts, prior exposure, consent and available time. Obtain owner authorization for each named recipient and exact material version before dispatch. Then collect independent written scope/statistical, clinical, PRESS and two content-validity opinions. Decide **GO_V4**, **GO_NARROW** or **STOP_R1** before formal sampling or outcome access. If no qualified people are available, retain HOLD rather than substitute more internal PASS reports. See [next-stage requirements](docs/NEXT_STAGE.md).

## Submission preparation

`submission/` is a public planning shell. The local package contains a prospective main manuscript and supplement (DOCX/PDF/Markdown), design and hypothetical figures, assumption-labelled planning sources, editorial declarations awaiting confirmation, QA receipts and source-copy hashes. Neither the local package nor this repository is ready for journal submission. Authorship, journal/article type, independent methodological approval and empirical results remain unresolved. The cover-letter development template must not be sent.

## Rights, security and citation

No project-wide open-source license is asserted. Public visibility is not a license; third-party data, papers, software and writing materials retain their original terms. Obtain upstream inputs from their original repositories. This repository does not authorize redistribution of local or third-party materials.

Do not post participant identifiers, reviewer identities, controlled forms, correspondence, credentials or raw-data files in an issue or pull request. Contributions must preserve the HOLD/LOCKED boundary and distinguish observed evidence from planning assumptions; see [CONTRIBUTING.md](CONTRIBUTING.md).

There is no final study citation or DOI. For the public design materials, cite this repository URL with the exact commit hash and access date and describe it as an unapproved prospective meta-research design. A protocol/manuscript citation can replace this only after genuine registration or publication.
