from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from ticket_control.pipeline import *
from ticket_control.big_query_download_raw import *
from ticket_control.big_query_upload_raw import *
from ticket_control.big_query_download_processed import *
from ticket_control.big_query_upload_processed import *
from ticket_control.telegramm_update_prod import *
import pandas as pd


@task(name="Update Telegram Data")
def flow_telegramm_update():
    df = get_update()
    return df


@task(name="Upload and Preprocess")
def update_flow(df_tele_raw):
    df_tele_processed = pipeline(df_tele_raw)
    upload_big_query_raw(df_tele_raw)
    upload_big_query_processed(df_tele_processed)


@flow(name="pipeline")
def get_update_flow():
    task1_future = flow_telegramm_update.submit()
    update_flow.submit(task1_future.result(), wait_for=[task1_future])


if __name__ == "__main__":
    get_update_flow()
