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
        # Reliable LibreTranslate endpoint
        response = requests.post(
            "https://translate.argosopentech.com/translate",
            json={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text"
            },
            headers={"accept": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        translated = response.json().get("translatedText")
        if not translated:
            return jsonify({"error": "No translation returned from API"}), 500
        return jsonify({"translatedText": translated})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Translation API timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Translation API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unknown error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
