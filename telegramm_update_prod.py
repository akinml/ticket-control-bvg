from prefect import flow
from telethon.sync import TelegramClient
import datetime
import pandas as pd
import asyncio


def get_update():
    """This function gets the newest data from the telegram Channel and saves it to our database."""
    print("\033[1;32m 💽 Telegramm update started 💽")

    api_id = 24420176
    api_hash = "9350869041f1e13cb10ecadcb8331367"
    save_df = pd.DataFrame()

    chats = ["freifahren_BE"]
    yesterday = datetime.date.today() - datetime.timedelta(minutes=5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient("test", api_id, api_hash, loop=loop)

    async def get_messages():
        update_df = pd.DataFrame()
        save_df = pd.DataFrame()
        for chat in chats:
            async for message in client.iter_messages(
                chat, offset_date=yesterday, reverse=True
            ):
                data = {
                    "group": chat,
                    "sender": int(message.sender_id),
                    "text": message.text,
                    "date": message.date,
                }
                update_df = pd.DataFrame(data, index=[1])
                save_df = pd.concat([save_df, update_df])
        save_df["sender"] = save_df["sender"].astype("int32")
        print(save_df)
        return save_df

    # Create a single client instance
    with client:
        save_df = client.loop.run_until_complete(get_messages())

    print("💽 Telegramm update finished 💽")
    save_df.to_csv("database_50_days.csv")
    return save_df


if __name__ == "__main__":
    get_update()
