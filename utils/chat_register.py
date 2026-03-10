from database.mongo import chats


def register_chat(chat):

    existing = chats.find_one({"chat_id": chat.id})

    if not existing:

        chats.insert_one({
            "chat_id": chat.id,
            "type": chat.type,
            "quiz_style": "inline",
            "exam": "general"
        })
