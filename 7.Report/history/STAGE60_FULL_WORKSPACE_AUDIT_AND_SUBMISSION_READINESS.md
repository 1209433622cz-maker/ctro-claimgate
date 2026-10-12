# Stage60 full-workspace audit and submission readiness

## Aggregate snapshot

| Check | Result |
|---|---:|
| File entries | 71,074 |
| Snapshot bytes | 11,241,356,763 |
| Readable files hashed | 69,086 |
| Zero-byte POSIX/Conda link placeholders | 1,988 |
| Structured objects inspected | 24,875 |
| ZIP integrity | 71/71 pass |
| SHA-256 sidecars | 12/12 pass |
| HDF5/H5AD structural opens | 26/26 pass |
| Manifest checks | 39/41 close |
| Duplicate groups | 27,262 |
| Redundant bytes | 2,537,072,510 |

The 22 structural label failures are 12 macOS `._` resource-fork placeholders and 10 joblib runtime test fixtures. The two manifest exceptions are nested historical source-manifests inside Stage56A/57 delta snapshots; the delta releases' top-level manifests pass, and their immutable source archives are preserved separately.

## Submission status

A journal-agnostic internal submission-preparation package now exists. It contains a prospective manuscript outline, claim ceiling, display plan, contribution/declaration templates and a readiness matrix. It contains no empirical Results section and is not ready for submission.

The blocking scientific items remain target-frame/estimand approval, PRESS and clinical review, content validity, real people and dispatch authorization, registered protocol/SAP, formal sampling/coding, the primary endpoint, authorship and target-journal selection.
