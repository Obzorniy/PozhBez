import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

url = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = None

print("🚀 Bot started...")

while True:
    try:
        response = requests.get(f"{url}/getUpdates", params={"timeout": 10})
        data = response.json()

        for update in data["result"]:
            update_id = update["update_id"]

            if last_update_id is None or update_id > last_update_id:
                last_update_id = update_id

                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")

                    print(f"📩 Message: {text}")

                    if text == "/start":
                        requests.get(f"{url}/sendMessage", params={
                            "chat_id": chat_id,
                            "text": "🔥 Бот работает! Напиши что-нибудь"
                        })

                    else:
                        requests.get(f"{url}/sendMessage", params={
                            "chat_id": chat_id,
                            "text": f"Ты написал: {text}"
                        })

        time.sleep(2)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)
