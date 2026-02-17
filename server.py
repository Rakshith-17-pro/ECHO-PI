from flask import Flask, request, jsonify
from flask_cors import CORS
from offline_translator.translator import OfflineTranslator
import os
import logging

from ai import create_default_manager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create Ollama manager (may auto-start Ollama if configured)
logging.basicConfig(level=logging.INFO)
ollama_manager = create_default_manager()

logging.info("Ollama manager configured for %s", ollama_manager.url)
# Initialize translator
# Ensure we are in the correct directory to find the model
# The model path in translator.py is relative ("./model"), so we need to be careful where we run this from.
# Best to run from project root.
try:
    translator = OfflineTranslator(model_path="./model")
except Exception as e:
    print(f"Error loading model: {e}")
    translator = None

# Global stats
sos_counter = 0

@app.route('/translate', methods=['POST'])
def translate_text():
    if not translator:
        return jsonify({"error": "Translator model not loaded"}), 500

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data['text']
    # Default to Kannada (>>kan<<) as per our translator implementation
    # We can ignore source/target from request for now as this is a specific En->Kn translator
    
    try:
        translated_text = translator.translate(text)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        print(f"Translation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/sos/alert', methods=['POST'])
def trigger_sos():
    global sos_counter
    sos_counter += 1
    return jsonify({"status": "alert_received", "total_alerts": sos_counter})

@app.route('/admin/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "totalSOS": sos_counter,
        "lastSOS": "Just now" if sos_counter > 0 else "N/A",
        "nodeStatus": "Active"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "model_loaded": translator is not None})


@app.route('/chat', methods=['POST'])
def chat_proxy():
    """Proxy chat requests to Ollama (model: phi3:mini).

    Expected frontend payload: { "text": "user message" }
    Returns: { "assistant": "response text" }
    """
    data = request.get_json() or {}
    user_text = data.get("text")
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # Build Ollama prompt — send the user's text directly; adjust as needed for system prompts
    payload = {
        "model": "phi3:mini",
        "prompt": user_text,
        "max_length": 512
    }

    try:
        assistant_text = ollama_manager.generate(user_text, model="phi3:mini")
        return jsonify({"assistant": assistant_text})
    except Exception as e:
        logging.exception("Error generating from Ollama: %s", e)
        return jsonify({"error": "Failed to generate from Ollama", "detail": str(e)}), 502

if __name__ == '__main__':
    import atexit

    # Ensure Ollama process is stopped when the server exits
    atexit.register(lambda: getattr(ollama_manager, "stop", lambda: None)())

    print("Starting Flask server on 10.139.20.130:5001...")
    app.run(host='10.139.20.130', port=5001, debug=True)
