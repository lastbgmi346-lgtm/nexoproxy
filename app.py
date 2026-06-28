from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "BACKJUMPV1": True,
    "BYPASSV1": True,
    "HIGH_FPS": False,
    "HIGH_JUMP": True,
    "HIGH_SENSI": False,
    "HS_CHEST": True,
    "HS_NECK": False,
    "NO_CD_MICS": False,
    "NO_SWAP": True,
    "RAPID_FIRE": True,
    "SPEED_HACK": False
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ✅ ROOT ROUTE - Ab JSON config return karega
@app.route('/')
def home():
    config = load_config()
    return jsonify(config)  # Direct JSON

# API endpoint (extra rakh sakte ho)
@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'GET':
        config = load_config()
        return jsonify(config)
    elif request.method == 'POST':
        new_config = request.get_json()
        if new_config is None:
            return jsonify({"error": "Invalid JSON"}), 400
        current_config = load_config()
        current_config.update(new_config)
        save_config(current_config)
        return jsonify({"status": "success", "config": current_config})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
