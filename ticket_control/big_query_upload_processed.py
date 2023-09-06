from google.cloud import bigquery
import pandas as pd


def upload_big_query_processed(df):
    print("\033[1;32m 👷Uploading Processed Data to BigQuery Started! 👷")
    client = bigquery.Client()

    dataset_id = "bvg-controller.bvg_test"
    dataset = bigquery.Dataset(dataset_id)

    table_id = "bvg-controller.bvg_test.processed"

    # Define the schema for your BigQuery table
    schema = [
        bigquery.SchemaField("date", "TIMESTAMP"),
        bigquery.SchemaField("station_key", "STRING"),
        bigquery.SchemaField("text", "STRING"),
        bigquery.SchemaField("station name", "STRING"),
        bigquery.SchemaField("lines", "STRING"),
        bigquery.SchemaField("area", "STRING"),
        bigquery.SchemaField("latitude", "FLOAT64"),
        bigquery.SchemaField("longitude", "FLOAT64"),
    ]

    job_config = bigquery.LoadJobConfig(
        autodetect=False, write_disposition="WRITE_APPEND", schema=schema
    )

    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Data uploaded to table {table_id} successfully!")
    except Exception as e:
        print(f"Error uploading data to BigQuery: {str(e)}")
    print("\033[1;32m 👷Uploading Processed Data to BigQuery Completed! 👷\n")


if __name__ == "__main__":
    # Make sure to pass your DataFrame as an argument to the function
    # For example, df = pd.read_csv("your_data.csv")
    # Then call upload_big_query_processed(df)
    pass
