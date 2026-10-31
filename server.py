
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "My AI server is running!",
        "mode": "DEMO",
        "subjects": ["English", "Math", "Science"]
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message"}), 400

    text = message.lower()

    # Greetings
    if any(word in text for word in ["hello", "hi", "হ্যালো", "হাই"]):
        reply = "Hello! Welcome to My AI Learning App!"

    # English
    elif "noun" in text:
        reply = "A noun is the name of a person, place, animal or thing. Example: Boy, School, Cat, Book."

    elif "verb" in text:
        reply = "A verb is an action word. Examples: Run, Eat, Play, Read."

    elif "adjective" in text:
        reply = "An adjective describes a noun. Examples: Beautiful, Big, Small, Happy."

    elif "pronoun" in text:
        reply = "A pronoun is a word used instead of a noun. Examples: He, She, It, They."

    elif "vowel" in text:
        reply = "The five vowels are A, E, I, O, U."

    elif "plural" in text:
        reply = "Plural means more than one. Example: Cat becomes Cats."

    # Mathematics
    elif re.search(r"\d+\s*[+]\s*\d+", text):
        match = re.search(r"(\d+)\s*\+\s*(\d+)", text)
        reply = f"The answer is {int(match.group(1)) + int(match.group(2))}."

    elif re.search(r"\d+\s*[-]\s*\d+", text):
        match = re.search(r"(\d+)\s*-\s*(\d+)", text)
        reply = f"The answer is {int(match.group(1)) - int(match.group(2))}."

    elif re.search(r"\d+\s*[*x]\s*\d+", text):
        match = re.search(r"(\d+)\s*[*x]\s*(\d+)", text)
        reply = f"The answer is {int(match.group(1)) * int(match.group(2))}."

    elif re.search(r"\d+\s*/\s*\d+", text):
        match = re.search(r"(\d+)\s*/\s*(\d+)", text)
        a, b = int(match.group(1)), int(match.group(2))
        if b == 0:
            reply = "Division by zero is not possible."
        else:
            reply = f"The answer is {a / b:g}."

    # Science
    elif "plant" in text:
        reply = "Plants are living things. They need sunlight, water, air and nutrients to grow."

    elif "animal" in text:
        reply = "Animals are living things. They need food, water and air to live."

    elif "water" in text:
        reply = "Water is essential for life. Humans, animals and plants need water."

    elif "sun" in text:
        reply = "The Sun is a star. It gives Earth light and heat."

    elif "human body" in text:
        reply = "The human body has many parts. The heart pumps blood and the brain controls the body."

    elif "butterfly" in text:
        reply = "A butterfly has four life cycle stages: Egg → Caterpillar → Pupa → Adult butterfly."

    elif "earth" in text:
        reply = "Earth is the planet where we live. It is our home."

    else:
        reply = (
            "Welcome to My AI Learning App!\n"
            "I can answer some prepared questions in three subjects:\n"
            "English: noun, verb, adjective, pronoun, vowel.\n"
            "Math: Try 25 + 15, 20 - 5, 6 * 4 or 12 / 3.\n"
            "Science: plants, animals, water, sun, Earth.\n"
            "Try asking me a question!"
        )

    return jsonify({
        "reply": reply,
        "mode": "DEMO"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
