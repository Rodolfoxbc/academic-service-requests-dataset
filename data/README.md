# Data directory

The canonical public dataset is maintained on Figshare:

- DOI: https://doi.org/10.6084/m9.figshare.33113150
- Canonical file: `academic_service_requests.csv`

The repository intentionally retrieves the canonical CSV from the published Figshare
record rather than maintaining a second independent copy. On a clean clone,
`python run_analysis.py` downloads the CSV automatically into `data/raw/` if it is
not already present.

The source-system records were obtained through a single retrospective extraction on
5 January 2026. The dataset contains requests registered during 1 September 2022 to
31 August 2023 and groups them into the two historical process conditions documented
in the manuscript.
