# Zenodo access and DOI status

The owner authorized Zenodo/DOI publication and reports being logged in. The connected plugin search returned no Zenodo integration; the two specifically checked local Zenodo token environment variables were absent. The available in-app browser exposed a Zenodo homepage tab, but page-state capture repeatedly timed out, including after the owner reported login. Thus neither authenticated upload access nor a draft/published record has been verified.

No token, password or cookie was read from a browser profile or placed in a repository. No record was created, no file uploaded to Zenodo and no reserved or registered DOI is claimed. This is an access boundary, not a research-data application requirement.

Prepared metadata can be used once a controllable authenticated browser or locally configured `ZENODO_ACCESS_TOKEN` with `deposit:write` and `deposit:actions` is available. Official API documentation: https://developers.zenodo.org/. A reserved DOI is not registered until publication; the final record and downloadable file checks must be verified before a DOI is inserted into the manuscript or citation file.
