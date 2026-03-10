from telegram.ext import Application
from config import BOT_TOKEN
from bot.router import register_handlers


def start_bot():

    app = Application.builder().token(BOT_TOKEN).build()

    register_handlers(app)

    print("Quiz Bot Started")

    app.run_polling()
