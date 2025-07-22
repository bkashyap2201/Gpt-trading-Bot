# main.py

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get your tokens from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to SuperOptionsGPT! 💥\nAsk me anything about options trading. Use /ask followed by your question.")

# Ask command
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please ask something like:\n/ask What is your view on ASTRAL 1600 CE?")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("⏳ Thinking...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use gpt-3.5-turbo if gpt-4 is unavailable
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.6
        )
        reply = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("⚠️ Failed to get a reply from ChatGPT.")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))

    print("🤖 Bot is running...")
    app.run_polling()
