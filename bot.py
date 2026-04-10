import requests
from bs4 import BeautifulSoup
import os 
from dotenv import load_dotenv

load_dotenv()

my_token = os.getenv("TELEGRAM_BOT_TOKEN")
my_chat = os.getenv("TELEGRAM_CHAT_ID")

url = "https://news.ycombinator.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        all_news = soup.find_all(class_="titleline")

        message_text = "🔥 ТОП 5 ТЕХНИЧЕСКИХ НОВОСТЕЙ\n"
        message_text += "=" * 50 + "\n\n"

        for i, news in enumerate(all_news[:5], 1):
            headline = news.get_text().strip()
            link_tag = news.find("a")
            link = link_tag.get("href") if link_tag else "No link"

            message_text += f"{i}. 📰 {headline}\n"
            message_text += f"   🔗 {link}\n"
            message_text += "-" * 50 + "\n"

        message_text += "\n✅ Новости обновлены!"

        # 🚀 ОТПРАВКА В TELEGRAM
        tele_url = f"https://api.telegram.org/bot{my_token}/sendMessage"

        tg_response = requests.post(tele_url, data={
            "chat_id": my_chat,
            "text": message_text
        })

        print("Telegram response:", tg_response.text)
        print("✅ Telegram Sent!")
        print(message_text)

    else:
        print("❌ Server Error")

except Exception as e:
    print(f"ERROR : {e}")
