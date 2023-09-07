from prefect import flow
from ticket_control import telegramm_update_prod
from ticket_control.telegramm_update_prod import get_update


@flow(name="telegramm_update_prod")
def flow_telegramm_update():
    df = get_update()
    df.to_csv("telegramm_update.csv")


if __name__ == "__main__":
    flow_telegramm_update()
