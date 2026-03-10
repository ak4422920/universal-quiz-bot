import uuid
from database.mongo import challenges


def create_challenge(challenger_id, opponent_id):

    challenge_id = str(uuid.uuid4())

    challenge_data = {
        "challenge_id": challenge_id,
        "challenger": challenger_id,
        "opponent": opponent_id,
        "status": "pending",
        "scores": {
            str(challenger_id): 0,
            str(opponent_id): 0
        }
    }

    challenges.insert_one(challenge_data)

    return challenge_data


def get_challenge(challenge_id):

    return challenges.find_one({"challenge_id": challenge_id})


def update_challenge_status(challenge_id, status):

    challenges.update_one(
        {"challenge_id": challenge_id},
        {"$set": {"status": status}}
    )
