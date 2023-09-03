from telethon.sync import TelegramClient
import datetime
import pandas as pd
from pathlib import Path

path_main = Path(__file__).parent.parent
path_to_data = path_main / "data/"


def get_update():
    """This function gets the newest data from the telegram Channel and saves it to our database."""
    print("Database update started 💽")
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
                data = {
                    "group": chat,
                    "sender": message.sender_id,
                    "text": message.text,
                    "date": message.date,
                }
                temp_df = pd.DataFrame(data, index=[1])
                update_df = pd.concat([update_df, temp_df], axis=0)

    database = pd.read_csv(str(path_to_data) + "/database_telegram.csv")
    database["comp_key"] = (
        str(database["sender"]) + database["text"] + str(database["date"])
    )
    update_df["comp_key"] = (
        str(update_df["sender"]) + update_df["text"] + str(update_df["date"])
    )
    for key in update_df["comp_key"]:
        if key not in list(database["comp_key"]):
            database = pd.concat(
                [database, update_df[update_df["comp_key"] == key]], axis=0
            )
    database.drop(["Unnamed: 0", "comp_key"], inplace=True, axis=1, errors="ignore")
    database.to_csv(str(path_to_data) + "/database_telegram.csv")
    print("Database update finished 💽")
    return database


if __name__ == "__main__":
    get_update()
