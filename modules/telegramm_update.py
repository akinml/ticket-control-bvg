from prefect import Flow
from telethon.sync import TelegramClient
import datetime
import pandas as pd
import config


def get_update():
    api_id = 24420176
    api_hash = "9350869041f1e13cb10ecadcb8331367"

    chats = ["freifahren_BE"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    # Create a single client instance
    with TelegramClient("test", api_id, api_hash) as client:
        update_df = pd.DataFrame()
        for chat in chats:
            for message in client.iter_messages(
                chat, offset_date=yesterday, reverse=True
            ):
                print(message)
                data = {
                    "group": chat,
                    "sender": message.sender_id,
                    "text": message.text,
                    "date": message.date,
                }
                temp_df = pd.DataFrame(data, index=[1])
                update_df = pd.concat([update_df, temp_df], axis=0)

    database = pd.read_csv("notebooks/data_2018_08.2023.csv")
    database["comp_key"] = str(database["sender"]) + database["text"] + database["date"]
    update_df["comp_key"] = (
        str(update_df["sender"]) + update_df["text"] + update_df["date"]
    )
    for key in update_df["comp_key"]:
        if key not in list(database["comp_key"]):
            print(f"Message Update:{key}")
            database = pd.concat(
                [database, update_df[update_df["comp_key"] == key]], axis=0
            )
    database.to_csv("save.csv")
    return database


if __name__ == "__main__":
    get_update()
