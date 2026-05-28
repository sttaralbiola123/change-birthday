import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Kukunin nito ang values mula sa Environment Variables ng Render mamaya
COOKIE_VALUE = os.environ.get("ROBLOSECURITY")
PASSWORD = os.environ.get("ROBLOX_PASSWORD")

cookies = {
    ".ROBLOSECURITY": COOKIE_VALUE
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_csrf_token():
    url = "https://auth.roblox.com/v2/logout"
    response = requests.post(url, cookies=cookies, headers=headers)
    csrf_token = response.headers.get("x-csrf-token")
    if not csrf_token:
        raise Exception("Failed to fetch CSRF token. Pakisuri kung valid ang cookie mo.")
    return csrf_token

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Buhay ang server! Bisitahin ang /run para i-trigger ang birthday changer."
    })

@app.route('/run')
def run_script():
    # Siguraduhing may laman ang credentials
    if not COOKIE_VALUE or not PASSWORD:
        return jsonify({"error": "Missing Environment Variables sa Render!"}), 400

    try:
        csrf_token = get_csrf_token()
        url = "https://accountinformation.roblox.com/v1/birthdate"
        
        req_headers = headers.copy()
        req_headers["X-CSRF-Token"] = csrf_token
        req_headers["Content-Type"] = "application/json"
        
        # Pwede mo nang baguhin ang birthday details dito
        payload = {
            "birthMonth": 1,
            "birthDay": 15,
            "birthYear": 2000,
            "password": PASSWORD
        }
        
        response = requests.post(url, cookies=cookies, headers=req_headers, json=payload)
        
        # Subukang i-parse ang response bilang json kung maaari
        try:
            roblox_resp = response.json()
        except:
            roblox_resp = response.text

        return jsonify({
            "status_code": response.status_code,
            "roblox_response": roblox_resp
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Awtomatikong gagamitin ang port na ibibigay ng Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
