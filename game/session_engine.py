import uuid
from database.mongo import sessions, questions


def create_session(user_id, total_questions=5):

    session_id = str(uuid.uuid4())

    # get questions from database
    question_list = list(questions.find().limit(total_questions))

    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "questions": question_list,
        "current_index": 0,
        "score": 0,
        "total_questions": total_questions,
        "status": "active"
    }

    sessions.insert_one(session_data)

    return session_data


def get_session(user_id):

    return sessions.find_one({
        "user_id": user_id,
        "status": "active"
    })


def update_session(session_id, score, index):

    sessions.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "score": score,
                "current_index": index
            }
        }
    )


def end_session(session_id):

    sessions.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "status": "finished"
            }
        }
    )
