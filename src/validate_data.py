import pandas as pd

from config import DATA_FILE, EXPECTED_COLUMNS, PERIODS


def load_and_validate_data(path=DATA_FILE):
    df = pd.read_csv(path)
    errors = []

    if list(df.columns) != EXPECTED_COLUMNS:
        errors.append(f"Expected columns {EXPECTED_COLUMNS}, found {list(df.columns)}.")
    if df.empty:
        errors.append("Dataset is empty.")
    if df.isna().any().any():
        errors.append("Missing values were detected.")

    if "TOTAL" in df.columns:
        converted = pd.to_numeric(df["TOTAL"], errors="coerce")
        if converted.isna().any() or not (converted % 1 == 0).all():
            errors.append("TOTAL contains non-integer values.")
        else:
            df["TOTAL"] = converted.astype(int)
            if (df["TOTAL"] <= 0).any():
                errors.append("TOTAL contains zero or negative values.")

    if all(c in df.columns for c in EXPECTED_COLUMNS[:4]):
        duplicate_keys = df.duplicated(EXPECTED_COLUMNS[:4]).sum()
        if duplicate_keys:
            errors.append(f"{duplicate_keys} duplicate composite keys were detected.")

    if "PERIOD" in df.columns:
        found = sorted(df["PERIOD"].dropna().unique().tolist())
        if found != sorted(PERIODS):
            errors.append(f"Unexpected PERIOD categories: {found}.")

    if errors:
        raise ValueError("Dataset validation failed:\n- " + "\n- ".join(errors))

    summary = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_composite_keys": int(df.duplicated(EXPECTED_COLUMNS[:4]).sum()),
        "period_categories": int(df["PERIOD"].nunique()),
        "campus_categories": int(df["CAMPUS"].nunique()),
        "request_type_categories": int(df["TYPE_REQUEST"].nunique()),
        "workflow_state_categories": int(df["CURRENT_STATE"].nunique()),
        "minimum_total": int(df["TOTAL"].min()),
        "maximum_total": int(df["TOTAL"].max()),
        "sum_total": int(df["TOTAL"].sum()),
    }
    return df, summary
