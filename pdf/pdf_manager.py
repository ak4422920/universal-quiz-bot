from database.mongo import books


def save_pdf_record(user_id, exam, file_id):

    books.insert_one({
        "uploaded_by": user_id,
        "exam": exam,
        "file_id": file_id,
        "status": "pending"
    })


def approve_pdf(file_id):

    books.update_one(
        {"file_id": file_id},
        {"$set": {"status": "approved"}}
    )


def reject_pdf(file_id):

    books.update_one(
        {"file_id": file_id},
        {"$set": {"status": "rejected"}}
    )
