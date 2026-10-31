
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "My AI server is running!",
        "mode": "DEMO"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message"}), 400

    text = message.lower()

    # Greeting
    if any(word in text for word in ["hello", "hi", "হ্যালো", "হাই"]):
        reply = "Hello! Welcome to My AI App. How can I help you?"

    # Name
    elif "your name" in text or "তোমার নাম" in text:
        reply = "My name is My AI Assistant."

    # English learning
    elif "what is a noun" in text or "noun" in text:
        reply = "A noun is the name of a person, place, animal or thing. Example: Boy, School, Cat, Book."

    elif "what is a verb" in text or "verb" in text:
        reply = "A verb is an action word. Examples: Run, Eat, Play, Read."

    elif "what is a plant" in text or "plant" in text:
        reply = "A plant is a living thing. Plants need sunlight, water, air and nutrients to grow."

    # Simple maths
    elif "2+2" in text or "2 + 2" in text:
        reply = "2 + 2 = 4. Great question!"

    elif "capital of bangladesh" in text:
        reply = "The capital of Bangladesh is Dhaka."

    # Default response
    else:
        reply = (
            "Thank you for your question! "
            "I am currently running in Demo Mode. "
            "I can answer a few prepared questions. "
            "Try asking about nouns, verbs, plants or simple maths."
        )

    return jsonify({
        "reply": reply,
        "mode": "DEMO"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)