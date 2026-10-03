import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

TFL_APP_KEY = os.getenv("TFL_APP_KEY")

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


def fetch_line_status():
    response = requests.get(
        "https://api.tfl.gov.uk/Line/Mode/tube/Status",
        params={"app_key": TFL_APP_KEY},
    )
    response.raise_for_status()
    return response.text


def upload_raw(data: str):
    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.bucket(GCS_BUCKET_NAME)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = f"line_status_{timestamp}.json"
    bucket.blob(blob_name).upload_from_string(data, content_type="application/json")
    return blob_name


if __name__ == "__main__":
    raw_data = fetch_line_status()
    uploaded_name = upload_raw(raw_data)
    print(f"Uploaded raw response to gs://{GCS_BUCKET_NAME}/{uploaded_name}")
