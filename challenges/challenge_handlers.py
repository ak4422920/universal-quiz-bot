from telegram import Update
from telegram.ext import ContextTypes
from challenges.challenge_manager import get_challenge, update_challenge_status


async def accept_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data.split("|")

    challenge_id = data[1]

    challenge = get_challenge(challenge_id)

    if not challenge:

        await query.edit_message_text("Challenge not found.")
        return

    update_challenge_status(challenge_id, "active")

    await query.edit_message_text(
        "Challenge accepted! Quiz battle starting soon."
    )
