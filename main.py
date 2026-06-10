from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=data)

def ask_claude(signal_type, price, score):
    prompt = f"Kamu adalah AI Market Analyst pakar XAUUSD. Signal: {signal_type}, Harga: {price}, Score: {score}/7. Berikan analisis ringkas dalam Bahasa Melayu. Format: ANALISIS, CADANGAN, AMARAN. Maksimum 150 patah perkataan."
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"Content-Type": "application/json", "x-api-key": CLAUDE_API_KEY, "anthropic-version": "2023-06-01"},
        json={"model": "claude-sonnet-4-20250514", "max_tokens": 500, "messages": [{"role": "user", "content": prompt}]}
    )
    return response.json()["content"][0]["text"]

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        signal = data.get("signal", "UNKNOWN")
        price = data.get("price", "0")
        score = data.get("score", "0")
        analysis = ask_claude(signal, price, score)
        emoji = "🟢" if "BUY" in signal else "🔴"
        message = f"{emoji} <b>AI SIGNAL XAUUSD</b>\n\n<b>Signal:</b> {signal}\n<b>Harga:</b> {price}\n<b>Score:</b> {score}/7\n\n{analysis}\n\n⚠️ <i>Education Only - Not Financial Advice</i>"
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
