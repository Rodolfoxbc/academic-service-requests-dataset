from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "raw" / "academic_service_requests.csv"
OUTPUT_DIR = ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"

PERIODS = ["PERIOD_1", "PERIOD_2"]

UNDESIRABLE_STATES = [
    "Reassigned",
    "Pending-Review Details",
    "Not Applicable",
    "Under Academic Council Review",
]

EXPECTED_COLUMNS = [
    "PERIOD",
    "CAMPUS",
    "TYPE_REQUEST",
    "CURRENT_STATE",
    "TOTAL",
]
