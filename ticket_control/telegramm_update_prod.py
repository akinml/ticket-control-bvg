from prefect import flow
from telethon.sync import TelegramClient
import datetime
import pandas as pd


def get_update():
    """This function gets the newest data from the telegram Channel and saves it to our database."""
    print("\033[1;32m 💽 Database update started 💽")

    api_id = 24420176
    api_hash = "9350869041f1e13cb10ecadcb8331367"

    chats = ["freifahren_BE"]
    yesterday = datetime.date.today() - datetime.timedelta(hours=0.25)
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
                update_df = pd.DataFrame(data, index=[1])
    print("\n 💽 Database update finished 💽")
    print(update_df)
    return update_df


if __name__ == "__main__":
    get_update()
