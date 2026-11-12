
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)

LESSONS = {
    "english": {
        "lesson": """CAMBRIDGE STAGE 3 - ENGLISH (ESL)

Topic: Parts of Speech

1. Noun: A naming word.
Examples: Boy, School, Book.

2. Verb: An action word.
Examples: Run, Eat, Read.

3. Adjective: A describing word.
Examples: Beautiful, Tall, Happy.

4. Pronoun: A word used instead of a noun.
Examples: He, She, It, They.

Now try to make your own sentences!""",

        "practice": """ENGLISH PRACTICE

1. Find the noun: The cat is sleeping.
2. Find the verb: Birds fly in the sky.
3. Find the adjective: She has a beautiful flower.
4. Choose a pronoun for Rahim: He / They.

Write your answers.""",

        "quiz": """ENGLISH QUIZ

1. Which word is a noun?
A. Run
B. School
C. Quickly

2. Which word is a verb?
A. Jump
B. Beautiful
C. Blue

3. Which word is an adjective?
A. Book
B. Eat
C. Happy

Reply: answers: 1B, 2A, 3C""",

        "key": ["B", "A", "C"]
    },

    "math": {
        "lesson": """CAMBRIDGE STAGE 3 - MATHEMATICS

Topic: Place Value

Example: 347

3 = 3 Hundreds = 300
4 = 4 Tens = 40
7 = 7 Ones = 7

347 = 300 + 40 + 7

Addition means putting together.
Subtraction means taking away.
Multiplication means equal groups.
Division means sharing equally.""",

        "practice": """MATHEMATICS PRACTICE

1. What is the value of 5 in 352?
2. Calculate: 125 + 34
3. Calculate: 90 - 25
4. Calculate: 6 x 4
5. Calculate: 20 / 5

Try to solve them yourself.""",

        "quiz": """MATHEMATICS QUIZ

1. What is 200 + 30 + 5?
A. 235
B. 253
C. 325

2. What is 8 x 3?
A. 11
B. 24
C. 32

3. What is 40 / 5?
A. 5
B. 6
C. 8

Reply: answers: 1A, 2B, 3C""",

        "key": ["A", "B", "C"]
    },

    "science": {
        "lesson": """CAMBRIDGE STAGE 3 - SCIENCE

Topic: Plants

Plants are living things.

Plants need:
1. Sunlight
2. Water
3. Air
4. Nutrients from the soil

Roots take in water.
The stem supports the plant.
Leaves help plants make food.

Plants provide food and oxygen.""",

        "practice": """SCIENCE PRACTICE

1. What do plants need to grow?
2. Which part takes in water?
3. Which part supports the plant?
4. Why are plants important?

Answer in simple sentences.""",

        "quiz": """SCIENCE QUIZ

1. Which part takes in water?
A. Flower
B. Root
C. Fruit

2. What do plants need to grow?
A. Water
B. Plastic
C. Glass

3. Which is a living thing?
A. Stone
B. Chair
C. Tree

Reply: answers: 1B, 2A, 3C""",

        "key": ["B", "A", "C"]
    }
}


def find_subject(text):
    if "english" in text:
        return "english"
    if "math" in text or "গণিত" in text:
        return "math"
    if "science" in text or "বিজ্ঞান" in text:
        return "science"
    return None





def check_practice_answers(text, subject):
    answer_keys = {
        "english": {
            "1": ["cat"],
            "2": ["fly"],
            "3": ["beautiful"],
            "4": ["he"]
        },
        "math": {
            "1": ["50"],
            "2": ["159"],
            "3": ["65"],
            "4": ["24"],
            "5": ["4"]
        },
        "science": {
            "1": ["sunlight", "water", "air", "nutrients"],
            "2": ["root"],
            "3": ["stem"],
            "4": ["food", "oxygen"]
        }
    }

    if subject not in answer_keys:
        return "Subject not found."

    keys = answer_keys[subject]
    result = subject.upper() + " PRACTICE RESULTS\n\n"

    for number, keywords in keys.items():
        pattern = rf"(?:^|[,;\n])\s*{number}\s*[.)-]?\s*(.*?)(?=(?:[,;\n]\s*[1-5]\s*[.)-]?)|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

        if match:
            user_answer = match.group(1).strip().lower()

            if any(word in user_answer for word in keywords):
                result += f"Question {number}: Correct!\n"
            else:
                result += f"Question {number}: Try again!\n"
        else:
            result += f"Question {number}: Not answered.\n"

    return result


MODE = "FREE_LEARNING"

@app.route("/")
def home():
    return jsonify({
        "message": "My Cambridge Learning App is running!",
        "mode": MODE,
        "subjects": ["English (ESL)", "Mathematics", "Science"],
        "features": ["Lesson", "Practice", "Quiz"]
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please enter a message"}), 400

    text = message.lower().strip()
    subject = find_subject(text)

    if subject:

        if "answer" in text or "answers" in text:
            reply = check_answers(text, subject)

        elif "quiz" in text or "কুইজ" in text:
            reply = LESSONS[subject]["quiz"]

        elif "practice" in text or "প্র্যাকটিস" in text:
            reply = LESSONS[subject]["practice"]

        elif "lesson" in text or "পাঠ" in text:
            reply = LESSONS[subject]["lesson"]

        else:
            reply = (
                f"Welcome to {subject.title()}!\n\n"
                "Type:\n"
                f"{subject.title()}: lesson\n"
                f"{subject.title()}: practice\n"
                f"{subject.title()}: quiz"
            )

    elif any(word in text for word in ["hello", "hi", "হ্যালো", "হাই"]):
        reply = "Hello! Welcome to My Cambridge Learning App!"

    else:
        reply = (
            "Welcome to My Cambridge Learning App!\n\n"
            "Choose a subject:\n\n"
            "English: lesson / practice / quiz\n"
            "Math: lesson / practice / quiz\n"
            "Science: lesson / practice / quiz"
        )

    return jsonify({
        "reply": reply,
        "mode": "DEMO",
        "subject": subject
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)