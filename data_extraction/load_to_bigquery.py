import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from google.cloud import bigquery, storage

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
BQ_TABLE = f"{GCP_PROJECT_ID}.tfl_raw.line_status_raw"


def get_latest_blob():
    client = storage.Client(project=GCP_PROJECT_ID)
    blobs = list(client.list_blobs(GCS_BUCKET_NAME))
    return max(blobs, key=lambda b: b.time_created)


def get_blob_by_name(blob_name: str):
    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.bucket(GCS_BUCKET_NAME)
    return bucket.blob(blob_name)


def load_blob_to_bigquery(blob):
    raw_json = blob.download_as_text()
    row = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source_file": blob.name,
        "raw_json": raw_json,
    }

    client = bigquery.Client(project=GCP_PROJECT_ID)
    errors = client.insert_rows_json(BQ_TABLE, [row])
    if errors:
        raise RuntimeError(f"Failed to insert row: {errors}")


if __name__ == "__main__":
    latest_blob = get_latest_blob()
    load_blob_to_bigquery(latest_blob)
    print(f"Loaded {latest_blob.name} into {BQ_TABLE}")
