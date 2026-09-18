import requests

from config import DATA_FILE

FIGSHARE_ARTICLE_ID = 33113150
FIGSHARE_API = f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}"
CANONICAL_FILENAME = "academic_service_requests.csv"


def ensure_dataset():
    """Download the canonical CSV from the published Figshare record if needed."""
    if DATA_FILE.exists():
        return DATA_FILE

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(FIGSHARE_API, timeout=30)
    response.raise_for_status()
    metadata = response.json()

    match = next(
        (f for f in metadata.get("files", []) if f.get("name") == CANONICAL_FILENAME),
        None,
    )
    if match is None:
        raise FileNotFoundError(
            f"{CANONICAL_FILENAME} was not found in Figshare record {FIGSHARE_ARTICLE_ID}."
        )

    download_url = match.get("download_url")
    if not download_url:
        raise RuntimeError("Figshare metadata did not provide a file download URL.")

    file_response = requests.get(download_url, timeout=60)
    file_response.raise_for_status()
    DATA_FILE.write_bytes(file_response.content)
    return DATA_FILE
