import requests

# 🔐 ВСТАВЬ СВОИ ДАННЫЕ
ID_INSTANCE = "3100515906"   # <-- твой instance id
API_TOKEN_INSTANCE = "12027ecebb2f49879a2c12a7fb214a90b8857f734bf2430fb1"  # <-- твой токен из Green

url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"

payload = {
    "chatId": "79102180248",   # <-- сюда вставим дальше
    "message": "🔥 ТЕСТ. MAX работает."
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:", response.text)
