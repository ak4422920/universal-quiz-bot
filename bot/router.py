from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.commands import start, quiz, challenge, createtournament, leaderboard, elite, profile
from quiz_engines.inline_quiz import handle_answer
from challenges.challenge_handlers import accept_challenge
from bot.commands import join_tournament_command


def register_handlers(app):

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("challenge", challenge))
    app.add_handler(CommandHandler("createtournament", createtournament))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("elite", elite))
    app.add_handler(CommandHandler("profile", profile))

    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer"))
    app.add_handler(CallbackQueryHandler(accept_challenge, pattern="^accept_challenge"))
    app.add_handler(CallbackQueryHandler(join_tournament_command, pattern="^join_tournament"))
