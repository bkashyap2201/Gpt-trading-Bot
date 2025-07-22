import os
from telegram.ext import Updater

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # ⬅ This should fetch from Render

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher
