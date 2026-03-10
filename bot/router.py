from telegram.ext import CommandHandler
from bot.commands import start, quiz


def register_handlers(app):

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
