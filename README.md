# Open Multi-Campus Academic Service Requests Dataset

This repository contains the anonymized dataset and reproducible analysis code
for the manuscript:

**An Open Multi-Campus Dataset of Academic Service Requests Before and After
Administrative Process Redesign**

## Dataset

The dataset contains aggregated academic service requests extracted from the
Sistema Nacional Académico (SNA).

- `PERIOD_1`: 1 September 2022 to 28 February 2023
- `PERIOD_2`: 1 March 2023 to 31 August 2023
- 3 anonymized campuses
- 25 request types
- 13 workflow states
- 432 aggregated rows
- 97,809 represented requests

Each row is a unique combination of:

- `PERIOD`
- `CAMPUS`
- `TYPE_REQUEST`
- `CURRENT_STATE`

`TOTAL` is the number of individual requests represented by the row. It is not
a processing duration or number of workflow steps.

## Repository structure

```text
.
├── data
│   ├── raw
│   │   ├── academic_service_requests.csv
│   │   └── processDataset.xlsx
│   └── processed
├── outputs
│   ├── figures
│   └── tables
├── src
│   ├── config.py
│   ├── generate_results.py
│   └── validate_data.py
├── run_analysis.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

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

## Generate results

Run:

```bash
python run_analysis.py
```

The script validates the dataset and generates publication-ready tables and
figures in `outputs/`.

## Undesirable workflow states

The institutional classification used in the analysis includes:

- `Reassigned`
- `Pending-Review Details`
- `Not Applicable`
- `Under Academic Council Review`

The analysis reports both absolute counts and rates relative to the total number
of requests.

## Main outputs

Tables:

- total requests by period
- requests by campus and period
- workflow-state distribution
- undesirable states by period
- undesirable rates by campus and period
- request types by period

Figures:

- total requests by period
- request volume by campus and period
- undesirable-state rate by period
- undesirable-state counts by period
- top 10 request types
- undesirable-state rate heatmap

## Data availability

The anonymized dataset is intended for publication on Figshare. The persistent
DOI will be added after the repository record is published.

## Limitations

The two periods cover different parts of the academic year. Comparisons may be
affected by academic-calendar and seasonal demand. The dataset contains
aggregated counts and does not include individual request histories, processing
times, staffing levels, or resource consumption.
