from datetime import timedelta
from google.cloud import bigquery
import pandas as pd
from prefect_gcp import GcpCredentials

gcp_credentials_block = GcpCredentials.load("gcp")


def download_big_query_processed():
    print("\033[1;32m 👷Downloading from BigQuery Started! 👷\n")
    client = bigquery.Client.from_service_account_info(gcp_credentials_block)
    query = """
    SELECT *
    FROM `bvg-controller.bvg_test.processed`
    """
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    print("\033[1;32m 👷Downloading from BigQuery Completed! 👷\n")
    return results


def download_last_three_hours(current_time):
    cutoff = current_time - timedelta(hours=3)
    print("\033[1;32m 👷Downloading from BigQuery Started! 👷\n")
    client = bigquery.Client()
    query = f"""
    SELECT *
    FROM `bvg-controller.bvg_test.processed`
    WHERE date >= '{str(cutoff)}'
    """
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    print("\033[1;32m 👷Downloading from BigQuery Completed! 👷\n")
    return results


if __name__ == "__main__":
    download_big_query_processed()
