from telegram import Update
from telegram.ext import ContextTypes
from database.mongo import questions


async def send_poll_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    # Try getting question from database
    question = questions.find_one()

    if question:

        q_text = question["question"]
        options = question["options"]
        correct = question["correct"]

    else:
        # fallback question
        q_text = "What is the capital of India?"
        options = ["Mumbai", "Delhi", "Kolkata", "Chennai"]
        correct = 1

    await context.bot.send_poll(
        chat_id=chat_id,
        question=q_text,
        options=options,
        type="quiz",
        correct_option_id=correct,
        is_anonymous=False
    )
