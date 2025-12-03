from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

# Serve frontend
@app.route('/')
def index():
    return send_file("translator.html")

# Translation endpoint
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    target_lang = data.get('target')

    if not text or not target_lang:
        return jsonify({"error": "Missing text or target language"}), 400

    try:
        response = requests.post(
            "https://libretranslate.de/translate",
            json={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text"
            },
            timeout=10
        )
        translated = response.json().get("translatedText", "")
        return jsonify({"translatedText": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
