import os
import requests
from dotenv import load_dotenv
from env_loader import BOT_TOKEN, CHAT_ID

load_dotenv()

def send_message(text, is_backtest=False):
    # If it's a backtest, just print it to the console and skip the network call
    if is_backtest:
        return
        
    token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    
    try:
        # Added a strict timeout parameter (3 seconds to connect, 5 to read) 
        # so it doesn't hang forever
        response = requests.post(url, data=payload, timeout=(3, 5))
        return response
    except requests.exceptions.RequestException as e:
        # Log the error but don't let it crash your live trading or backtest
        print(f"Telegram Notification Failed: {e}")