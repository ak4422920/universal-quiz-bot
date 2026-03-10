from database.mongo import users


def add_score(user_id, points):

    users.update_one(
        {"user_id": user_id},
        {"$inc": {"score": points}}
    )


def get_top_users(limit=10):

    return list(
        users.find().sort("score", -1).limit(limit)
    )
