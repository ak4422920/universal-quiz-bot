async def start(update, context):

    await update.message.reply_text(
        "Welcome to Universal Quiz Bot!"
    )


async def quiz(update, context):

    await update.message.reply_text(
        "Quiz system will start soon."
    )
