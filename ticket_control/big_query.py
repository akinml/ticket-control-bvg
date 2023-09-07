import os
from google.cloud import bigquery
from pathlib import Path

path_main = Path(__file__).parent.parent
path_to_data = path_main / "data/"


def upload_big_query(csv_path):
    print("\033[1;32m 👷Uploading to BigQuery Started! 👷\n")
    client = bigquery.Client()

    dataset_id = "bvg-controller.bvg_test"
    dataset = bigquery.Dataset(dataset_id)
    client.create_dataset(dataset, exists_ok=True)

    table_id = "bvg-controller.bvg_test.processed"
    job_config = bigquery.LoadJobConfig(
        autodetect=True, write_disposition="WRITE_TRUNCATE"
    )
    with open(csv_path, "rb") as file:
        job = client.load_table_from_file(file, table_id, job_config=job_config)
        job.result()
    print("\033[1;32m 👷Uploading to BigQuery Completed! 👷\n")


def download_big_query():
    print("\033[1;32m 👷Downloading from BigQuery Started! 👷\n")
    client = bigquery.Client()

    # Specify the BigQuery SQL query
    query = """
    SELECT *
    FROM `lewagon-396609.telegram.processed`
    """

    # Run the query and fetch the results into a DataFrame
    query_job = client.query(query)
    results = query_job.result().to_dataframe()

    # Save the DataFrame to a local CSV file
    results.to_csv(path_to_data + "/preprocessed_database_telegram.csv", index=False)
    print("\033[1;32m 👷Downloading from BigQuery Completed! 👷\n")


if __name__ == "__main__":
    csv_path = str(path_to_data) + "/telegramm_update.csv"
    upload_big_query(csv_path)
