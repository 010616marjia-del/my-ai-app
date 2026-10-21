
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "My AI server is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message"}), 400

    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=message
        )

        return jsonify({"reply": response.output_text})

    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({
            "error": "AI response failed. Please check server settings."
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
