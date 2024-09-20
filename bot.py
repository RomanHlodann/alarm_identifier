import os
import telebot

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = os.environ.get("CHAT_ID")


def send_notifications(message):
    bot.send_message(CHAT_ID, message)
