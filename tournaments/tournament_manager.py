import uuid
from database.mongo import tournaments


def create_tournament(name, exam, total_questions=10):

    tournament_id = str(uuid.uuid4())

    tournament_data = {
        "tournament_id": tournament_id,
        "name": name,
        "exam": exam,
        "total_questions": total_questions,
        "participants": [],
        "scores": {},
        "status": "upcoming"
    }

    tournaments.insert_one(tournament_data)

    return tournament_data


def join_tournament(tournament_id, user_id):

    tournaments.update_one(
        {"tournament_id": tournament_id},
        {"$addToSet": {"participants": user_id}}
    )


def update_score(tournament_id, user_id, score):

    tournaments.update_one(
        {"tournament_id": tournament_id},
        {"$set": {f"scores.{user_id}": score}}
    )


def get_tournament(tournament_id):

    return tournaments.find_one({"tournament_id": tournament_id})


def start_tournament(tournament_id):

    tournaments.update_one(
        {"tournament_id": tournament_id},
        {"$set": {"status": "active"}}
    )


def end_tournament(tournament_id):

    tournaments.update_one(
        {"tournament_id": tournament_id},
        {"$set": {"status": "finished"}}
    )
