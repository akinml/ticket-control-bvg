from google.cloud import bigquery
import pandas as pd


def download_big_query_raw():
    print("\033[1;32m 👷Downloading Raw Data from BigQuery Started! 👷\n")
    client = bigquery.Client()
    query = """
    SELECT *
    FROM `bvg-controller.bvg_test.raw`
    """
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    print("\033[1;32m 👷Downloading Raw Data from BigQuery Completed! 👷\n")
    return results


if __name__ == "__main__":
    download_big_query_raw()
