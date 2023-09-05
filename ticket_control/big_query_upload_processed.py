from google.cloud import bigquery
import pandas as pd


def upload_big_query_processed(df):
    print("\033[1;32m 👷Uploading Processed Data to BigQuery Started! 👷")
    client = bigquery.Client()

    dataset_id = "bvg-controller.bvg_test"
    dataset = bigquery.Dataset(dataset_id)

    table_id = "bvg-controller.bvg_test.processed"
    job_config = bigquery.LoadJobConfig(
        autodetect=True, write_disposition="WRITE_APPEND"
    )
    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Data uploaded to table {table_id} successfully!")
    except Exception as e:
        print(f"Error uploading data to BigQuery: {str(e)}")
    print("\033[1;32m 👷Uploading Processed Data to BigQuery Completed! 👷\n")


if __name__ == "__main__":
    upload_big_query_processed()
