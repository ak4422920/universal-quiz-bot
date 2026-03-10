from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.commands import start, quiz
from quiz_engines.inline_quiz import handle_answer


def register_handlers(app):

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))

    app.add_handler(CallbackQueryHandler(handle_answer))
