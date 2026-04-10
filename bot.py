import requests
import time
import os
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = None

print("🚀 Bot started...")

def get_news():
    url = "https://news.ycombinator.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "❌ Ошибка загрузки новостей"

    soup = BeautifulSoup(response.content, "html.parser")
    all_news = soup.find_all(class_="titleline")

    message = "🔥 ТОП 5 ТЕХНО НОВОСТЕЙ\n"
    message += "=" * 40 + "\n\n"

    for i, news in enumerate(all_news[:5], 1):
        title = news.get_text().strip()
        link = news.find("a").get("href")

        message += f"{i}. {title}\n"
        message += f"{link}\n\n"

    return message


while True:
    try:
        response = requests.get(f"{BASE_URL}/getUpdates", timeout=10)
        data = response.json()

        if not data.get("ok"):
            print("❌ Telegram error:", data)
            time.sleep(2)
            continue

        updates = data.get("result", [])

        for update in updates:
            update_id = update["update_id"]

            if last_update_id is None or update_id > last_update_id:
                last_update_id = update_id

                if "message" not in update:
                    continue

                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")

                print("📩 Message:", text)

                # 🔥 команды
                if text == "/start":
                    msg = "👋 Бот работает!\n\nНапиши /news чтобы получить новости"

                elif text == "/news":
                    msg = get_news()

                else:
                    msg = "❓ Не понял команду\n\nНапиши /news"

                requests.get(f"{BASE_URL}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": msg
                })

        time.sleep(2)

    except Exception as e:
        print("❌ ERROR:", e)
        time.sleep(5)
