from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Config file ka naam
CONFIG_FILE = "config.json"

# Default config (pehli baar jab file na ho)
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
    """Config file se data load karein"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(data):
    """Config file mein data save karein"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'GET':
        # Current config return karein
        config = load_config()
        return jsonify(config)
    
    elif request.method == 'POST':
        # Naya config save karein
        new_config = request.get_json()
        if new_config is None:
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Pehle purana config load karein
        current_config = load_config()
        # Update karein with new values
        current_config.update(new_config)
        # Save karein
        save_config(current_config)
        return jsonify({"status": "success", "config": current_config})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
