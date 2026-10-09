from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="tfl_line_status_pipeline",
    schedule="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
)
def tfl_line_status_pipeline():
    @task
    def extract():
        from data_extraction.extract_script import fetch_line_status, upload_raw

        raw_data = fetch_line_status()
        return upload_raw(raw_data)

    @task
    def load(blob_name: str):
        from data_extraction.load_to_bigquery import get_blob_by_name, load_blob_to_bigquery

        load_blob_to_bigquery(get_blob_by_name(blob_name))

    load(extract())


tfl_line_status_pipeline()
