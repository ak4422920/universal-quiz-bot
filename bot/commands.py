from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.mongo import users
from utils.chat_register import register_chat
from quiz_engines.poll_quiz import send_poll_quiz
from quiz_engines.inline_quiz import send_inline_quiz
from challenges.challenge_manager import create_challenge
from tournaments.tournament_manager import create_tournament, join_tournament
from utils.leaderboard import get_top_users
from utils.elite_ranking import get_elite_players
from pdf.pdf_manager import save_pdf_record
from config import PDF_REVIEW_CHANNEL


async def start(update, context):

    user = update.effective_user
    chat = update.effective_chat

    register_chat(chat)

    existing = users.find_one({"user_id": user.id})

    if not existing:

        users.insert_one({
            "user_id": user.id,
            "name": user.first_name,
            "username": user.username,
            "language": "en",
            "score": 0,
            "badges": [],
            "joined_at": str(update.message.date)
        })

    await update.message.reply_text(
        "Welcome to Universal Quiz Bot!"
    )


async def quiz(update, context):

    chat = update.effective_chat

    if chat.type == "private":
        await send_inline_quiz(update, context)
    else:
        await send_poll_quiz(update, context)


async def uploadpdf(update, context):

    user = update.effective_user

    if not context.args:

        await update.message.reply_text(
            "Usage: /uploadpdf EXAM\nThen send the PDF."
        )

        return

    exam = context.args[0]

    context.user_data["upload_exam"] = exam

    await update.message.reply_text(
        "Now send the PDF file."
    )


async def receive_pdf(update, context):

    if "upload_exam" not in context.user_data:
        return

    document = update.message.document

    if not document.file_name.endswith(".pdf"):

        await update.message.reply_text("Please upload a PDF file.")
        return

    exam = context.user_data["upload_exam"]

    save_pdf_record(update.effective_user.id, exam, document.file_id)

    keyboard = [
        [
            InlineKeyboardButton(
                "Approve",
                callback_data=f"approve_pdf|{document.file_id}"
            ),
            InlineKeyboardButton(
                "Reject",
                callback_data=f"reject_pdf|{document.file_id}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_document(
        chat_id=PDF_REVIEW_CHANNEL,
        document=document.file_id,
        caption=f"PDF Upload\nExam: {exam}",
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "PDF sent for admin approval."
    )
