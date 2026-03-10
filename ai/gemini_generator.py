import google.generativeai as genai
import json
from config import GEMINI_API_KEY
from database.mongo import questions

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_questions(exam="general", language="en", count=5):

    prompt = f"""
Generate {count} multiple choice quiz questions for {exam} exam.

Language: {language}

Return JSON format like this:

[
{{
"question": "...",
"options": ["A","B","C","D"],
"correct": 0
}}
]
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    try:
        data = json.loads(text)

        for q in data:

            questions.insert_one({
                "exam": exam,
                "question": q["question"],
                "options": q["options"],
                "correct": q["correct"],
                "source": "ai"
            })

        return len(data)

    except Exception:

        return 0
