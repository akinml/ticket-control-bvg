from google.cloud import bigquery
import pandas as pd


def download_big_query_processed():
    print("\033[1;32m 👷Downloading from BigQuery Started! 👷\n")
    client = bigquery.Client()
    query = """
    SELECT *
    FROM `bvg-controller.bvg_test.processed`
    """
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    print("\033[1;32m 👷Downloading from BigQuery Completed! 👷\n")
    return results


if __name__ == "__main__":
    download_big_query_processed()
