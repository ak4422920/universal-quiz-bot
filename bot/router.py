from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.commands import start, quiz, challenge, createtournament, leaderboard, elite, profile, uploadpdf, receive_pdf
from quiz_engines.inline_quiz import handle_answer
from challenges.challenge_handlers import accept_challenge
from pdf.pdf_handlers import handle_pdf_approval
from bot.commands import join_tournament_command


def register_handlers(app):

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("challenge", challenge))
    app.add_handler(CommandHandler("createtournament", createtournament))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("elite", elite))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("uploadpdf", uploadpdf))

    app.add_handler(MessageHandler(filters.Document.PDF, receive_pdf))

    app.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer"))
    app.add_handler(CallbackQueryHandler(accept_challenge, pattern="^accept_challenge"))
    app.add_handler(CallbackQueryHandler(join_tournament_command, pattern="^join_tournament"))
    app.add_handler(CallbackQueryHandler(handle_pdf_approval, pattern="^(approve_pdf|reject_pdf)"))
