import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

GREEN_API_URL = os.getenv("GREEN_API_URL")          # например: https://api.green-api.com
GREEN_ID_INSTANCE = os.getenv("GREEN_ID_INSTANCE")  # только цифры
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")      # токен инстанса

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")
WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN", "")      # опционально

def send_to_max(chat_id: str, text: str):
    url = f"{GREEN_API_URL}/waInstance{GREEN_ID_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
    r = requests.post(url, json={"chatId": chat_id, "message": text}, timeout=30)
    r.raise_for_status()
    return r.json()

def ask_gpt(text: str) -> str:
    resp = client.responses.create(model=OPENAI_MODEL, input=text)
    return (resp.output_text or "").strip() or "…"

@app.get("/health")
def health():
    return "ok", 200

@app.post("/webhook")
def webhook():
    # защита вебхука (если включишь токен в Green API)
    if WEBHOOK_TOKEN:
        auth = request.headers.get("Authorization", "")
        if WEBHOOK_TOKEN not in auth:
            return "unauthorized", 401

    data = request.get_json(silent=True) or {}

    # берём только входящий текст
    if data.get("typeWebhook") != "incomingMessageReceived":
        return "ignored", 200

    message_data = data.get("messageData", {}) or {}
    if message_data.get("typeMessage") != "textMessage":
        return "ignored", 200

    chat_id = (data.get("senderData", {}) or {}).get("chatId")
    text = ((message_data.get("textMessageData", {}) or {}).get("textMessage") or "").strip()

    if not chat_id or not text:
        return "ignored", 200

    answer = ask_gpt(text)
    send_to_max(chat_id, answer)

    return jsonify({"status": "ok"}), 200

