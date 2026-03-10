from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.mongo import users
from utils.chat_register import register_chat
from quiz_engines.poll_quiz import send_poll_quiz
from quiz_engines.inline_quiz import send_inline_quiz
from challenges.challenge_manager import create_challenge
from tournaments.tournament_manager import create_tournament, join_tournament
from utils.leaderboard import get_top_users
from utils.elite_ranking import get_elite_players


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


async def createtournament(update, context):

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage: /createtournament NAME EXAM"
        )

        return

    name = context.args[0]
    exam = context.args[1]

    tournament = create_tournament(name, exam)

    keyboard = [
        [
            InlineKeyboardButton(
                "Join Tournament",
                callback_data=f"join_tournament|{tournament['tournament_id']}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🏆 Tournament Created!\n\n{name}\nExam: {exam}",
        reply_markup=reply_markup
    )


async def leaderboard(update, context):

    top_users = get_top_users()

    text = "🏆 Leaderboard\n\n"

    rank = 1

    for user in top_users:

        text += f"{rank}. {user['name']} - {user['score']}\n"

        rank += 1

    await update.message.reply_text(text)


async def elite(update, context):

    elite_players = get_elite_players()

    text = "👑 Elite Ranking\n\n"

    rank = 1

    for user in elite_players:

        text += f"{rank}. {user['name']} - {user['score']}\n"

        rank += 1

    if rank == 1:
        text += "No elite players yet."

    await update.message.reply_text(text)


async def profile(update, context):

    user = update.effective_user

    data = users.find_one({"user_id": user.id})

    if not data:
        return

    badges = data.get("badges", [])

    text = f"👤 {data['name']}\n"
    text += f"⭐ Score: {data['score']}\n\n"

    if badges:

        text += "🎖 Badges:\n"

        for badge in badges:
            text += f"{badge}\n"

    else:
        text += "No badges yet."

    await update.message.reply_text(text)
