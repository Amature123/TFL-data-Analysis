import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_TABLE = f"{GCP_PROJECT_ID}.tfl_raw.line_status_raw"


def test_bigquery():
    client = bigquery.Client(project=GCP_PROJECT_ID)
    query = f"""
        SELECT extracted_at, source_file, LENGTH(raw_json) AS raw_json_len
        FROM `{BQ_TABLE}`
        ORDER BY extracted_at DESC
        LIMIT 5
    """
    rows = list(client.query(query).result())
    print(f"Found {len(rows)} row(s) in {BQ_TABLE}")
    for row in rows:
        print(dict(row))


if __name__ == "__main__":
    test_bigquery()
