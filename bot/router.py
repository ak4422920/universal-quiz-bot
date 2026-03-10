from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.commands import start, quiz, challenge
from quiz_engines.inline_quiz import handle_answer
from challenges.challenge_handlers import accept_challenge


def register_handlers(app):

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("challenge", challenge))

    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer"))
    app.add_handler(CallbackQueryHandler(accept_challenge, pattern="^accept_challenge"))
