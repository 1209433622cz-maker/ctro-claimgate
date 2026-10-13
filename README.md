# CTRO target dependent interval coverage

Current study: **CTRO-SOLO-01 under RP V5.1**, an original computational study of donor-nested gene-module contrasts. It is not the earlier RP V4 probability-sampled literature-audit proposal. Historical R0/R1 failures and external-review gates remain preserved as history; they are not retrospectively turned into PASS.

Authors: Zhi Chen and Teng Qi. School of Medicine, The Chinese University of Hong Kong, Shenzhen. Correspondence: Teng Qi, tengqi@link.cuhk.edu.cn. ORCID: [Zhi Chen](https://orcid.org/0009-0001-0072-5576), [Teng Qi](https://orcid.org/0009-0007-7648-4776).

## Current release

Version `ctro-rpv5.1-v1.0.0`, 13 October 2026. The owner explicitly approved PDF/Markdown author review and public release. The article is not submitted, peer-reviewed or accepted. The author-reported funding/competing interests/ethics declarations are in the manuscript. Specific CRediT roles and target journal remain unconfirmed; roles have not been invented or randomly assigned.

The main simulation completed **192 scenarios × 5000 replicates = 960000 existing instances**, with no failed modules. This release does not generate new primary instances. It preserves the original main endpoints and primary display coordinates. Its contribution is a bounded quantitative comparison of complete-donor, observed-donor and population-cell targets, not a novel universal scoring method or disease mechanism.

- [Current manuscript](5_manuscript/rp_v5_1/v1.0.0/Full_Manuscript_English_Release79.pdf) and [editable Markdown](5_manuscript/rp_v5_1/v1.0.0/Full_Manuscript_English_Release79.md)
- [Analytical supplement](5_manuscript/rp_v5_1/v1.0.0/Analytical_Supplement_and_Result_Index_Release79.pdf) and [Markdown](5_manuscript/rp_v5_1/v1.0.0/Analytical_Supplement_and_Result_Index_Release79.md)
- [Synthetic reproduction ZIP](6_release/rp_v5_1/v1.0.0/TierA_Synthetic_Reproduction.zip) and [current payload/source manifest](6_release/rp_v5_1/v1.0.0/PUBLIC_RELEASE_MANIFEST.json)
- [Data and license scope](1_data/RP_V5_1_DATA_AND_LICENSE_SCOPE.md), [current state](0_admin/SCIENTIFIC_STATUS.md), [next stage](0_admin/NEXT_STAGE.md) and [action record](7.Report/Stage79_RP_V5_1_PUBLIC_RELEASE_ACTION_RECORD.md)

## Reproduce the tested synthetic results

Download and extract the Tier A ZIP into a new directory. Use Python 3.12.14 and the versions in its `requirements.txt`. From the extracted root:

```powershell
python -I 2_code/77_analytic_portable/portable_replay.py
```

The packet's own script forbids network calls and access to the original project directory. It checks 576 **existing** IDs (0, 2499 and 4999 in all 192 scenarios), complete aggregate joins, exact mask/variance/C expectations and seven synthetic figure reconstructions. Prior clean-directory pinned-runtime/same-Windows tests matched 14 PNG/SVG files and passed seven refusal-boundary tests. This is not a full raw rerun, cross-platform certification or independently implemented generator. Source code under `2_code/rp_v5_1_source` is an inspection mirror; run the standalone ZIP rather than assuming that mirror is a second root-injected entry point.

## Results and limits

In the frozen A126 sparse partial-member scenario, donor coverage was 94.90% for the observed target and 88.54% for the complete target. The secondary paired difference was 6.36 percentage points, with 95% Monte Carlo interval 5.52–7.20. Exact shared-mask target variance was 0.04. This explains an uncertainty component but does not derive exact Welch coverage or propose a calibrated correction.

Sparse direct signal was evaluated only in M1 with five members. A078 is a post-main descriptive extreme, not a replacement primary coordinate. The model is continuous and arithmetic-mean based, not a count/rank scoring benchmark. C zero-FDR results can arise because all matching targets are non-null; they do not prove interval calibration.

The existing PBC illustration has eight donors and all four inherited maxT P-values equal to 1.0. Publicly included author-created illustrations do not make the human inputs part of the synthetic reproduction packet. Raw patient matrices, local donor derivatives/mappings and their private figure source objects are excluded. No source-human-data license is granted here.

## Repository layout

The existing eight-root architecture is retained: `0_admin`, `1_data`, `2_code`, `3_results`, `4_figures`, `5_manuscript`, `6_release`, `7.Report`. Current RP V5.1 material has explicit versioned subfolders. Other plans, manuscripts and development assets are historical unless specifically listed in the current manifest. The prior active README/status/next-stage files are preserved under `0_admin/history_stage68`; Git history is not deleted or force-rewritten.

## Licenses and citation

Current project-owned simulation/reproduction software is [MIT](LICENSE). Current manuscript, author-created figures and project-generated synthetic results are [CC BY 4.0](LICENSE-DATA-AND-MANUSCRIPT.md). Historical materials, third-party articles/code/skills, and upstream human data are not blanket-relicensed. The file scope takes precedence over assumptions based on the root license badge.

Use [CITATION.cff](CITATION.cff) for the current authors/version. Zenodo metadata is prepared in `.zenodo.json`, but **no Zenodo record or DOI is claimed as published**. Login, prepared metadata, a Git tag and a reserved DOI are not equivalent to an archival publication. See [Zenodo access status](0_admin/ZENODO_ACCESS_STATUS.md).

## Publication boundary

PDF and Markdown are the owner-approved current document route. Unrendered DOCX is not distributed. All source/numeric boundaries remain; public release is not journal submission, external validation or a guarantee of acceptance. Generative AI assistance is disclosed; the actual authors remain responsible for the work.
