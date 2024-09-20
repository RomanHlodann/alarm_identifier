import asyncio
import os
import datetime

from telethon import TelegramClient
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import send_notifications


load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

client = TelegramClient("session_name", api_id, api_hash)

dangerous_words = [
    "Жовкв", "Шахед", "Ува", "Львівщин", "Ракет"
]


def check_if_message_contains_dangerous_words(message: str):
    for word in dangerous_words:
        if word.lower() in message.lower():
            return True

    return False


async def check_if_alarm_really_dangerous():
    chat = await client.get_entity("https://t.me/trlviv")\

    ten_minutes_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=10)

    async for message in client.iter_messages(chat, limit=50):
        if message.date > ten_minutes_ago:
            if check_if_message_contains_dangerous_words(message.message):
                send_notifications()
                return


async def main():
    await client.start()

    scheduler = AsyncIOScheduler()

    scheduler.add_job(check_if_alarm_really_dangerous, "interval", minutes=10)

    scheduler.start()

    while True:
        await asyncio.sleep(1)


with client:
    client.loop.run_until_complete(main())
