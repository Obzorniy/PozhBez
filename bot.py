import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("🚀 Bot started...")

url = "https://news.ycombinator.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    news = soup.find_all(class_="titleline")

    message = "🔥 ТОП 5 ТЕХНО НОВОСТЕЙ\n\n"

    for i, item in enumerate(news[:5], 1):
        title = item.get_text()
        link = item.find("a")["href"]

        message += f"{i}. {title}\n{link}\n\n"

    # 🔥 ВАЖНО: правильный URL
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    r = requests.post(send_url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

    print("📡 Telegram response:", r.text)

except Exception as e:
    print("ERROR:", e)
