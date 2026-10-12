# Source-access scope correction — Stage53

Base public commit: `53ecb79ae897f483a13ba32252c2c4c1b32e050b`. This correction supersedes the earlier broad statement that no source expression rows were read.

The Stage52 generic source-text audit decoded up to 64 KiB, rather than stopping after a header. Saved inspection records show beyond-header decoding for two ENG04 source-count tables and 36 saved-result tables. That supports a software-access disclosure. It does not establish numerical analysis, human review of values, disease-effect computation or an incorrect author result. Opaque hashing also reads bytes, but does not decode or interpret values; these operations must not be conflated.

Going forward, source material is opaque-hash-only by default. Explicit expression-header access requires a role, immutable hash and ordered metadata expectation; the new inspector stops at the first LF and never decodes a body row. Saved-result files are denied semantic header access. Code repair does not erase earlier exposure. ENG04 remains a development-only engineering case, not a formal blinded main-sample record.

The new inspector is included here and tested on synthetic files. It has not been used to inspect real author counts or treated as an author-analysis reproduction. Author input and runtime-database provenance remain unresolved. R1-00C stays HOLD and R1-01 stays LOCKED.

The 2.190 GB duplicate-byte figure is logical accounting by recorded size and hash, not a guaranteed physical-space saving. No cleanup is authorized.
