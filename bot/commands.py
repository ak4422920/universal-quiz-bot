from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.mongo import users
from utils.chat_register import register_chat
from quiz_engines.poll_quiz import send_poll_quiz
from quiz_engines.inline_quiz import send_inline_quiz
from challenges.challenge_manager import create_challenge


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


async def challenge(update, context):

    user = update.effective_user

    if not context.args:

        await update.message.reply_text(
            "Usage: /challenge USER_ID"
        )

        return

    opponent_id = int(context.args[0])

    challenge = create_challenge(user.id, opponent_id)

    keyboard = [
        [
            InlineKeyboardButton(
                "Accept Challenge",
                callback_data=f"accept_challenge|{challenge['challenge_id']}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"You challenged user {opponent_id}!",
        reply_markup=reply_markup
    )
