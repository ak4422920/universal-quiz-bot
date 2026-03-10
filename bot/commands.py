from database.mongo import users
from utils.chat_register import register_chat
from quiz_engines.poll_quiz import send_poll_quiz


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

    await send_poll_quiz(update, context)
