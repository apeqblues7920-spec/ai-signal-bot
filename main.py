from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        signal = data.get("signal", "UNKNOWN")
        price = data.get("price", "0")
        score = data.get("score", "0")

        emoji = "🟢" if "BUY" in signal else "🔴"
        message = f"{emoji} <b>AI SIGNAL XAUUSD</b>\n\nSignal: {signal}\nPrice: {price}\nScore: {score}"
        send_telegram(message)
        return {"status": "ok"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def home():
    return "AI Signal Bot Running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
