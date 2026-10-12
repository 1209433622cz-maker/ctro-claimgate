# Public full-file audit summary - Stage66

Dated logical baseline, 12 October 2026. Integrity results are not scientific findings.

| Check | Actual result |
|---|---:|
| File entries | 79,225 |
| Logical byte sum | 11,984,417,518 |
| Readable files fully SHA-256 hashed | 77,380 |
| Inaccessible entries | 1,845 zero-byte archived POSIX link placeholders |
| Filesystem walk errors | 0 |
| Structured objects inspected | 28,938 |
| Initial format-label failures | 22 known resource-fork/software-fixture exceptions |
| ZIP CRC / safe paths | 87/87 pass |
| Archive manifests | 43/45 close; two historical nested exceptions |
| SHA-256 sidecars | 17/17 match |
| HDF5 metadata/structure | 30/30 pass |
| Duplicate-content groups | 29,195; no cleanup performed |
| Logical redundant bytes | 2,669,332,483; not a physical-space savings promise |

Every readable baseline file is hashed. This is not line-by-line manual review of all dependencies, expression values or serialized objects. Nested archives are not recursively unpacked; RDS/pickle/RAR objects are not executed. Logical directory-junction entries can count the same physical dependency files more than once. The baseline does not include later Stage66 outputs; a local final delta census records them separately.

Source-data text has a capped first-line structural check, without value interpretation. HDF5 objects are inspected for names/shapes/types, not numerical disease analysis. Text-risk categories are stored locally without secret values. Known Mac resource forks and non-gzip joblib test fixtures are preserved. The two nested historical Stage56A/57 source-manifest exceptions remain attached to their original archives.

No real screening pilot, independent coding, primary endpoint, disease effect, author computation or expert dispatch occurs. Submission preparation remains HOLD. The public repository contains curated derived summaries, not the private inventory. See [Stage66 limits and decisions](STAGE66_REBUILD_AUDIT_AND_READINESS.md).
