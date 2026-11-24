import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://shop.travisscott.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"Fehler beim Senden: {e}")

def check_shop():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15, allow_redirects=True)
        text = response.text.upper()
        final_url = response.url.lower()

        if "password" in final_url or ("SOON" in text and "AIR FORCE" in text and "ADD TO CART" not in text and "BUY" not in text):
            return False

        if "AIR FORCE 1" in text and ("ADD TO CART" in text or "BUY" in text or "SOLD OUT" in text or "RAFFLE" in text):
            return True

        return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fehler: {e}")
        return None

def main():
    print("Bot gestartet...")
    send_telegram("🌵 AF1 Monitor (Railway) gestartet\nPrüfe jetzt jede Minute.")

    notified = False

    while True:
        is_open = check_shop()

        if is_open is True and not notified:
            send_telegram("🚨 <b>SHOP / RAFFLE IST LIVE!</b>\n\n→ https://shop.travisscott.com/")
            notified = True
            print("Benachrichtigung gesendet!")

        elif is_open is False:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Noch SOON")

        time.sleep(60)

if __name__ == "__main__":
    main()
