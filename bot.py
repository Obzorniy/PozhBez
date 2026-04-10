import requests
import time
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = None

print("🚀 Bot started...")

while True:
    try:
        params = {
            "timeout": 10
        }

        if last_update_id is not None:
            params["offset"] = last_update_id + 1

        response = requests.get(f"{BASE_URL}/getUpdates", params=params)
        data = response.json()

        if not data.get("ok"):
            print("❌ Telegram error:", data)
            time.sleep(2)
            continue

        updates = data.get("result", [])

        for update in updates:
            last_update_id = update["update_id"]

            if "message" not in update:
                continue

            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            print("📩 Message:", text)

            requests.get(f"{BASE_URL}/sendMessage", params={
                "chat_id": chat_id,
                "text": f"Ответ: {text}"
            })

        time.sleep(2)

    except Exception as e:
        print("❌ ERROR:", e)
        time.sleep(5)
