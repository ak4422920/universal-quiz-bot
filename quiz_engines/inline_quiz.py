from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database.mongo import questions

async def send_inline_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    # try getting question from database
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

    keyboard = []

    for i, option in enumerate(options):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"answer_{i}_{correct}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=q_text,
        reply_markup=reply_markup
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data.split("_")

    chosen = int(data[1])
    correct = int(data[2])

    if chosen == correct:
        text = "✅ Correct answer!"
    else:
        text = "❌ Wrong answer!"

    await query.edit_message_text(text=text)
