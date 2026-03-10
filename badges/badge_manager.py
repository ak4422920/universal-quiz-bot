from database.mongo import users


BADGE_RULES = [
    (500, "👑 Legend"),
    (250, "🏆 Quiz Master"),
    (100, "🥇 Expert"),
    (50, "🥈 Skilled"),
    (10, "🥉 Beginner")
]


def check_and_assign_badges(user_id):

    user = users.find_one({"user_id": user_id})

    if not user:
        return

    score = user.get("score", 0)
    current_badges = user.get("badges", [])

    new_badges = []

    for points, badge in BADGE_RULES:

        if score >= points and badge not in current_badges:
            new_badges.append(badge)

    if new_badges:

        users.update_one(
            {"user_id": user_id},
            {"$push": {"badges": {"$each": new_badges}}}
        )

        return new_badges

    return []
