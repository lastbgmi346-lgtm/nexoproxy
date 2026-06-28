from flask import Flask, request, jsonify, render_template_string
import json
import os
import requests

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

# ✅ ROOT URL - HTML Control Panel (bilkul Niku server jaisa)
@app.route('/')
def home():
    # User IP fetch karne ke liye
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>NIKU MODS PROXY</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: #0a0a0f;
                color: #e0e0e0;
                min-height: 100vh;
                padding: 20px;
                background-image: radial-gradient(ellipse at center, #0a1628 0%, #0a0a0f 100%);
            }
            .container { max-width: 480px; margin: 0 auto; position: relative; }
            .header { text-align: center; padding: 30px 0 20px 0; position: relative; }
            .header h1 {
                font-size: 28px;
                font-weight: 700;
                background: linear-gradient(135deg, #4fc3f7, #0288d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 2px;
                text-shadow: 0 0 40px rgba(79, 195, 247, 0.3);
            }
            .header h1 i { -webkit-text-fill-color: transparent; background: linear-gradient(135deg, #4fc3f7, #0288d1); -webkit-background-clip: text; }
            .header .subtitle {
                font-size: 12px;
                color: #666;
                margin-top: 5px;
                letter-spacing: 4px;
                text-transform: uppercase;
                opacity: 0.7;
            }
            .header .subtitle i { color: #4fc3f7; margin: 0 4px; }
            .version-badge {
                display: inline-block;
                background: rgba(79, 195, 247, 0.1);
                color: #4fc3f7;
                padding: 2px 10px;
                border-radius: 20px;
                font-size: 9px;
                letter-spacing: 1px;
                margin-top: 8px;
                border: 1px solid rgba(79, 195, 247, 0.15);
            }
            .status-bar {
                background: rgba(255,255,255,0.03);
                border-radius: 12px;
                padding: 12px 20px;
                margin-bottom: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: 1px solid rgba(255,255,255,0.05);
            }
            .status-bar .status-text { font-size: 13px; color: #888; }
            .status-bar .status-text i { color: #4fc3f7; margin-right: 8px; }
            .status-bar .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #4fc3f7;
                display: inline-block;
                animation: pulse 2s infinite;
            }
            .status-bar .ip-display { font-size: 10px; color: #555; font-family: monospace; }
            .status-bar .ip-display i { color: #4fc3f7; margin-right: 4px; }
            @keyframes pulse {
                0% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.5; transform: scale(0.9); }
                100% { opacity: 1; transform: scale(1); }
            }
            .toggle-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-top: 10px;
            }
            .toggle-item {
                background: rgba(255,255,255,0.03);
                border-radius: 16px;
                padding: 16px 14px;
                border: 1px solid rgba(255,255,255,0.06);
                transition: all 0.3s ease;
                cursor: pointer;
                position: relative;
                overflow: hidden;
                user-select: none;
                -webkit-tap-highlight-color: transparent;
            }
            .toggle-item:active { transform: scale(0.97); }
            .toggle-item .label {
                font-size: 13px;
                font-weight: 500;
                color: #aaa;
                margin-bottom: 3px;
                display: flex;
                align-items: center;
                gap: 8px;
                pointer-events: none;
            }
            .toggle-item .label i { color: #4fc3f7; font-size: 14px; width: 18px; text-align: center; }
            .toggle-item .description {
                font-size: 10px;
                color: #555;
                line-height: 1.4;
                padding-left: 26px;
                pointer-events: none;
            }
            .toggle-item .description i { color: #4fc3f7; font-size: 8px; }
            .toggle-item .toggle-switch {
                position: absolute;
                top: 14px;
                right: 14px;
                width: 40px;
                height: 22px;
                background: #222;
                border-radius: 11px;
                transition: all 0.3s ease;
                border: 2px solid #333;
                pointer-events: none;
            }
            .toggle-item .toggle-switch::after {
                content: '';
                position: absolute;
                top: 2px;
                left: 2px;
                width: 14px;
                height: 14px;
                background: #555;
                border-radius: 50%;
                transition: all 0.3s ease;
            }
            .toggle-item.active {
                border-color: rgba(79, 195, 247, 0.4);
                background: rgba(79, 195, 247, 0.05);
            }
            .toggle-item.active .toggle-switch { background: #4fc3f7; border-color: #4fc3f7; }
            .toggle-item.active .toggle-switch::after { left: 20px; background: #fff; }
            .toggle-item.active .label { color: #4fc3f7; }
            .toggle-item.active .label i { color: #4fc3f7; }
            .toggle-item.important { border-color: rgba(255, 50, 50, 0.2); }
            .toggle-item.important .label { color: #ff6b6b; }
            .toggle-item.important .label i { color: #ff6b6b; }
            .toggle-item.important.active {
                border-color: rgba(255, 50, 50, 0.4);
                background: rgba(255, 50, 50, 0.05);
            }
            .toggle-item.important.active .toggle-switch { background: #ff6b6b; border-color: #ff6b6b; }
            .toggle-item.important.active .label { color: #ff6b6b; }
            .toggle-item.important.active .label i { color: #ff6b6b; }
            .social-links {
                margin-top: 25px;
                padding: 20px;
                background: rgba(255,255,255,0.02);
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.05);
                text-align: center;
            }
            .social-links .developer { font-size: 13px; color: #888; margin-bottom: 12px; }
            .social-links .developer i { color: #4fc3f7; margin-right: 6px; }
            .social-links .developer a { color: #4fc3f7; text-decoration: none; font-weight: 500; transition: color 0.3s ease; }
            .social-links .developer a:hover { color: #81d4fa; }
            .social-links .channel {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: rgba(79, 195, 247, 0.08);
                padding: 8px 16px;
                border-radius: 30px;
                border: 1px solid rgba(79, 195, 247, 0.15);
                transition: all 0.3s ease;
                text-decoration: none;
                color: #4fc3f7;
                font-size: 12px;
            }
            .social-links .channel:hover {
                background: rgba(79, 195, 247, 0.15);
                border-color: rgba(79, 195, 247, 0.3);
                transform: translateY(-2px);
            }
            .social-links .channel i { font-size: 16px; }
            .social-links .divider { color: #333; margin: 12px 0; font-size: 20px; }
            .footer {
                text-align: center;
                margin-top: 20px;
                padding: 15px 0;
                color: #333;
                font-size: 11px;
                letter-spacing: 1px;
            }
            .footer i { color: #4fc3f7; margin: 0 4px; }
            .toast {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.9);
                color: #fff;
                padding: 12px 24px;
                border-radius: 30px;
                font-size: 13px;
                opacity: 0;
                transition: all 0.4s ease;
                pointer-events: none;
                border: 1px solid rgba(79, 195, 247, 0.2);
                backdrop-filter: blur(10px);
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .toast i { color: #4fc3f7; }
            .toast.show { opacity: 1; bottom: 40px; }
            .expiry-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                backdrop-filter: blur(20px);
                z-index: 999999;
                display: none;
                justify-content: center;
                align-items: center;
                animation: fadeIn 0.5s ease;
            }
            .expiry-overlay.show { display: flex; }
            .expiry-overlay .expiry-box {
                background: linear-gradient(145deg, #1a1a2e, #0a0a15);
                padding: 50px 30px 40px;
                border-radius: 30px;
                max-width: 420px;
                width: 90%;
                text-align: center;
                border: 2px solid rgba(255, 50, 50, 0.3);
                box-shadow: 0 0 80px rgba(255, 50, 50, 0.15);
                animation: slideUp 0.5s ease;
                position: relative;
                overflow: hidden;
            }
            .expiry-overlay .expiry-box::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at center, rgba(255, 50, 50, 0.08) 0%, transparent 70%);
                animation: rotate 20s linear infinite;
            }
            .expiry-overlay .expiry-icon {
                font-size: 70px;
                margin-bottom: 20px;
                animation: pulse 1.5s ease-in-out infinite;
                color: #ff4444;
                position: relative;
                z-index: 1;
            }
            .expiry-overlay .expiry-title {
                font-size: 28px;
                font-weight: 900;
                color: #ff4444;
                margin-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 3px;
                position: relative;
                z-index: 1;
                text-shadow: 0 0 30px rgba(255, 50, 50, 0.3);
            }
            .expiry-overlay .expiry-message {
                font-size: 17px;
                color: #ddd;
                margin-bottom: 30px;
                line-height: 1.8;
                position: relative;
                z-index: 1;
            }
            .expiry-overlay .expiry-message i { color: #ff4444; margin: 0 6px; }
            .expiry-overlay .expiry-btn {
                display: inline-flex;
                align-items: center;
                gap: 12px;
                background: linear-gradient(135deg, #ff4444, #cc0000);
                color: white;
                padding: 16px 35px;
                border-radius: 50px;
                text-decoration: none;
                font-size: 15px;
                font-weight: 700;
                transition: all 0.3s ease;
                position: relative;
                z-index: 1;
                border: none;
                cursor: pointer;
                box-shadow: 0 4px 30px rgba(255, 50, 50, 0.4);
                letter-spacing: 1px;
            }
            .expiry-overlay .expiry-btn:hover {
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 8px 40px rgba(255, 50, 50, 0.6);
            }
            .expiry-overlay .expiry-btn:active { transform: scale(0.95); }
            .expiry-overlay .expiry-btn i { font-size: 20px; }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from { transform: translateY(30px) scale(0.95); opacity: 0; }
                to { transform: translateY(0) scale(1); opacity: 1; }
            }
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            @media (max-width: 400px) {
                .toggle-grid { gap: 8px; }
                .toggle-item { padding: 12px 10px; }
                .toggle-item .label { font-size: 11px; }
                .toggle-item .label i { font-size: 12px; width: 16px; }
                .toggle-item .description { font-size: 9px; padding-left: 24px; }
                .header h1 { font-size: 22px; }
                .social-links .developer { font-size: 12px; }
                .social-links .channel { font-size: 11px; padding: 6px 14px; }
                .status-bar .ip-display { font-size: 8px; }
                .expiry-overlay .expiry-box { padding: 35px 20px 30px; }
                .expiry-overlay .expiry-title { font-size: 22px; }
                .expiry-overlay .expiry-message { font-size: 15px; }
                .expiry-overlay .expiry-btn { font-size: 13px; padding: 14px 25px; }
                .expiry-overlay .expiry-icon { font-size: 50px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-moon"></i> NIKU MODS</h1>
                <div class="subtitle"><i class="fas fa-shield-alt"></i> Proxy Control Panel <i class="fas fa-shield-alt"></i></div>
                <div class="version-badge"><i class="fas fa-code-branch"></i> v2.0</div>
            </div>
            
            <div class="status-bar">
                <span class="status-text"><i class="fas fa-circle"></i> Proxy Active</span>
                <span class="ip-display"><i class="fas fa-network-wired"></i> <span id="userIp">Loading...</span></span>
            </div>
            
            <div class="toggle-grid" id="toggleGrid">
                <div class="toggle-item" data-key="HS_NECK">
                    <div class="label"><i class="fas fa-crosshairs"></i> HS NECK</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Neck shots = headshot</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="HS_CHEST">
                    <div class="label"><i class="fas fa-bullseye"></i> HS CHEST</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Chest shots = headshot</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="SPEED_HACK">
                    <div class="label"><i class="fas fa-bolt"></i> SPEED HACK</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> 2x movement speed</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="BACKJUMPV1">
                    <div class="label"><i class="fas fa-undo-alt"></i> BACK JUMP</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Old back jump mechanic</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="NO_SWAP">
                    <div class="label"><i class="fas fa-exchange-alt"></i> NO SWAP</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Instant weapon swap</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item important active" data-key="BYPASSV1">
                    <div class="label"><i class="fas fa-shield-halved"></i> BYPASS</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Anti-ban protection</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item" data-key="HIGH_JUMP">
                    <div class="label"><i class="fas fa-arrow-up"></i> HIGH JUMP</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Increased jump height</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="NO_CD_MICS">
                    <div class="label"><i class="fas fa-clock"></i> NO CD MICS</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> No cooldown + fast landing</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item" data-key="RAPID_FIRE">
                    <div class="label"><i class="fas fa-fire"></i> RAPID FIRE</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Increased fire rate</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="HIGH_FPS">
                    <div class="label"><i class="fas fa-tv"></i> HIGH FPS</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Frame rate auto boost</div>
                    <div class="toggle-switch"></div>
                </div>
                
                <div class="toggle-item active" data-key="HIGH_SENSI">
                    <div class="label"><i class="fas fa-eye"></i> HIGH SENSI</div>
                    <div class="description"><i class="fas fa-arrow-right"></i> Sensitivity set to 999</div>
                    <div class="toggle-switch"></div>
                </div>
            </div>
            
            <div class="social-links">
                <div class="developer">
                    <i class="fas fa-code"></i> Developer: <a href="https://t.me/ur_nikuu" target="_blank"><i class="fab fa-telegram"></i> @ur_nikuu</a>
                </div>
                <div class="divider">✦</div>
                <a href="https://polite-moccasin-86ycsnpwcp.edgeone.app/" target="_blank" class="channel">
                    <i class="fab fa-telegram-plane"></i> Join Telegram Channel
                </a>
            </div>
            
            <div class="footer">
                <i class="fas fa-exclamation-triangle"></i> Restart game after changing settings <i class="fas fa-exclamation-triangle"></i>
            </div>
        </div>
        
        <div class="toast" id="toast">
            <i class="fas fa-check-circle"></i>
            <span>Settings saved!</span>
        </div>

        <script>
            let saveTimeout = null;
            const toast = document.getElementById('toast');
            
            async function getUserIp() {
                try {
                    const response = await fetch('https://api.ipify.org?format=json');
                    const data = await response.json();
                    document.getElementById('userIp').textContent = data.ip;
                } catch (error) {
                    document.getElementById('userIp').textContent = '127.0.0.1';
                }
            }
            getUserIp();
            
            document.querySelectorAll('.toggle-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    if (e.target.closest('.toggle-switch')) return;
                    this.classList.toggle('active');
                    const key = this.dataset.key;
                    const isActive = this.classList.contains('active');
                    const label = this.querySelector('.label').textContent.trim();
                    saveConfig(key, isActive);
                    showToast(`${label} ${isActive ? 'enabled' : 'disabled'}`);
                });
            });
            
            async function saveConfig(key, value) {
                try {
                    const response = await fetch('/api/config', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ [key]: value })
                    });
                    const data = await response.json();
                    if (data.status === 'success') {
                        updateStatusBar();
                    }
                } catch (error) {
                    console.error('Error saving config:', error);
                }
            }
            
            async function loadConfig() {
                try {
                    const response = await fetch('/api/config');
                    const config = await response.json();
                    document.querySelectorAll('.toggle-item').forEach(item => {
                        const key = item.dataset.key;
                        if (key in config) {
                            if (config[key]) {
                                item.classList.add('active');
                            } else {
                                item.classList.remove('active');
                            }
                        }
                    });
                } catch (error) {
                    console.error('Error loading config:', error);
                }
            }
            
            function updateStatusBar() {
                const dot = document.querySelector('.status-dot');
                dot.style.background = '#4fc3f7';
                dot.style.animation = 'pulse 2s infinite';
            }
            
            function showToast(message) {
                toast.querySelector('span').textContent = message;
                toast.classList.add('show');
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    toast.classList.remove('show');
                }, 1500);
            }
            
            loadConfig();
        </script>
    </body>
    </html>
    """
    return html_content

# ✅ API CONFIG ENDPOINT - JSON config ke liye (Drip Client yahi use karega)
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
        
        # IMPORTANT: Updated config return karein
        return jsonify(current_config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
