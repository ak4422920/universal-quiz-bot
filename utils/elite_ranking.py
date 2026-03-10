from database.mongo import users


ELITE_THRESHOLD = 200


def get_elite_players(limit=20):

    elite_players = users.find(
        {"score": {"$gte": ELITE_THRESHOLD}}
    ).sort("score", -1).limit(limit)

    return list(elite_players)
