from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from game.session_engine import create_session, get_session, update_session, end_session
from utils.leaderboard import add_score
from badges.badge_manager import check_and_assign_badges


async def send_inline_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    session = create_session(user.id, 5)

    question = session["questions"][0]

    await send_question(update, context, question, session["session_id"])


async def send_question(update, context, question, session_id):

    q_text = question["question"]
    options = question["options"]
    correct = question["correct"]

    keyboard = []

    for i, option in enumerate(options):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"answer|{session_id}|{i}|{correct}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=q_text,
        reply_markup=reply_markup
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data.split("|")

    session_id = data[1]
    chosen = int(data[2])
    correct = int(data[3])

    session = get_session(query.from_user.id)

    if not session:
        await query.edit_message_text("Session expired.")
        return

    score = session["score"]
    index = session["current_index"]

    if chosen == correct:
        score += 1

    index += 1

    if index >= session["total_questions"]:

        end_session(session_id)

        add_score(query.from_user.id, score)

        new_badges = check_and_assign_badges(query.from_user.id)

        text = f"Quiz finished!\n\nScore: {score}/{session['total_questions']}"

        if new_badges:
            text += "\n\n🎖 New Badges Earned:\n"
            for badge in new_badges:
                text += f"{badge}\n"

        await query.edit_message_text(text)

        return

    update_session(session_id, score, index)

    next_question = session["questions"][index]

    q_text = next_question["question"]
    options = next_question["options"]
    correct = next_question["correct"]

    keyboard = []

    for i, option in enumerate(options):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"answer|{session_id}|{i}|{correct}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=q_text,
        reply_markup=reply_markup
    )
