# Open Multi-Campus Academic Service Requests Dataset

This repository contains the reproducible validation and analysis workflow associated
with the manuscript:

**An Open Multi-Campus Dataset of Academic Service Requests Before and After
Administrative Process Redesign**

## Published dataset

The canonical anonymized dataset is publicly available on Figshare:

- DOI: https://doi.org/10.6084/m9.figshare.33113150
- Canonical file: `academic_service_requests.csv`
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)

The dataset contains:

- `PERIOD_1`: 1 September 2022 to 28 February 2023
- `PERIOD_2`: 1 March 2023 to 31 August 2023
- 3 pseudonymized campuses
- 25 request types
- 13 workflow states
- 432 aggregated rows
- 97,809 represented requests

Each row is a unique observed combination of `PERIOD`, `CAMPUS`,
`TYPE_REQUEST`, and `CURRENT_STATE`. `TOTAL` is the number of requests
represented by the row.

The source-system data were obtained through a single retrospective extraction on
5 January 2026. `PERIOD` identifies the historical interval in which a request was
registered, whereas `CURRENT_STATE` represents the state recorded in the source
system at the extraction snapshot.

## Repository structure

```text
.
├── data
│   └── README.md
├── outputs
│   ├── figures
│   └── tables
├── src
│   ├── config.py
│   ├── fetch_data.py
│   ├── generate_results.py
│   └── validate_data.py
├── run_analysis.py
├── data_dictionary.csv
├── requirements.txt
├── CITATION.cff
├── DATA_LICENSE.txt
├── LICENSE
└── README.md
```

The canonical CSV is not duplicated permanently in this repository. On a clean clone,
the analysis workflow retrieves `academic_service_requests.csv` directly from the
published Figshare record and stores the local working copy under `data/raw/`.

## Reproduce the analysis from a clean clone

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Rodolfoxbc/academic-service-requests-dataset.git
cd academic-service-requests-dataset
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the complete workflow:

```bash
python run_analysis.py
```

The script:

1. retrieves the canonical CSV from Figshare if no local copy is present;
2. validates the schema, categories, composite-key uniqueness, missing values, and
   numerical integrity;
3. reproduces the descriptive tables and figures used in the illustrative analysis;
4. generates the revised two-panel request-type visualization;
5. calculates request-type-specific undesirable-state rates and pooled-composition
   standardized rates; and
6. performs the illustrative Pearson chi-squared test and reports Cramer's V.

Generated material is written to `outputs/tables/` and `outputs/figures/`.

## Undesirable workflow states

The institutionally defined set used for the illustrative analysis comprises:

- `Reassigned`
- `Pending-Review Details`
- `Not Applicable`
- `Under Academic Council Review`

This is an institution-specific analytical classification rather than a universal
workflow taxonomy.

## Reproducibility checks

For the published dataset, the workflow validates the following reference totals:

- 432 aggregated rows
- 97,809 represented requests
- 45,699 requests in `PERIOD_1`
- 52,110 requests in `PERIOD_2`
- 2,377 undesirable-state requests in `PERIOD_1`
- 2,324 undesirable-state requests in `PERIOD_2`

The revised workflow also reproduces pooled-composition standardized undesirable-state
rates of approximately 5.13% and 4.54%, and the illustrative period-by-undesirable-state
comparison (Pearson chi-squared approximately 29.27; Cramer's V approximately 0.017).

## Interpretation and limitations

The two periods cover different portions of the academic year and differ slightly in
calendar duration (181 and 184 days). The resource was generated from one retrospective
snapshot rather than separate end-of-period snapshots, so requests in `PERIOD_1` had
a longer potential follow-up interval before the 5 January 2026 extraction.

The dataset contains aggregated counts rather than individual request histories. It
does not provide request-level processing times, event sequences, staffing levels,
resource consumption, or a contemporaneous control group. The illustrative comparisons
should therefore not be interpreted as causal estimates of the administrative redesign.

## Licenses

The published Figshare dataset is licensed under CC BY 4.0. The analysis source code
in this repository is licensed under the MIT License.
