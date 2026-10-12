# Initial publication hold and subsequent recovery

The first Stage66 CLI deletion attempt returned HTTP 403 because the token lacked `delete_repo`. Repository administration rights in metadata do not guarantee that a particular OAuth token has deletion scope. The initial failure receipt is preserved locally. The owner subsequently obtained the scope, and its presence was independently verified before retrying.

The original remote had numeric identity 1413032204 and main commit befd6975a4cc548070acb7e8ea9a60b1fd1b9d76. Git history, complete remote ref coverage and accessible resource exports were backed up and the bundle was verified and restored. The authorized retry deleted that exact repo and created the public replacement with numeric identity 1414686660. Actual non-force Git push and a fresh remote clone passed payload validation and 28 safe-source tests. No expert dispatch or journal submission occurred.

No token, password, device authorization or broad account permission was automated. Exact old identity/main, verified backup and candidate checks preceded deletion. The deletion/recreation is complete: do not replay it against the replacement. The old-ID guard deliberately refuses the new repository. A same-name URL is not a retained GitHub identity, and the backup does not promise restoration of every GitHub setting or social relationship.
