
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

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

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY is missing"}), 500

    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-2.5-flash:generateContent"
        )

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            },
            json={
                "contents": [
                    {"parts": [{"text": message}]}
                ]
            },
            timeout=30
        )

        result = response.json()

        if response.status_code != 200:
            app.logger.error("Gemini API error: %s", response.status_code)
            return jsonify({
                "error": "Gemini could not respond. Check API access and server logs."
            }), 500

        reply = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No reply received.")
        )

        return jsonify({"reply": reply})

    except Exception:
        app.logger.exception("Gemini request failed")
        return jsonify({"error": "Could not connect to Gemini"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
