from prefect import flow
from pipeline import *
from ticket_control.big_query_download_raw import *
from ticket_control.big_query_upload_raw import *
from ticket_control.big_query_download_processed import *
from ticket_control.big_query_upload_processed import *
from ticket_control.telegramm_update_prod import *


# @flow(name="pipeline")
def get_update_flow():
    return get_update()


def update_flow(df_tele_raw):
    df_tele_processed = pipeline(df_tele_raw)
    upload_big_query_raw(df_tele_raw)
    upload_big_query_processed(df_tele_processed)


if __name__ == "__main__":
    raw = get_update_flow()
    update_flow(raw)
