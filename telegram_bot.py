import os
import requests
from dotenv import load_dotenv
from env_loader import BOT_TOKEN, CHAT_ID

load_dotenv()



def send_message(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    payload = {

        "chat_id": CHAT_ID,

        "text": message

    }

    response = requests.post(
        url,
        data=payload
    )

    return response.json()