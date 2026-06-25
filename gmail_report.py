import os
import yagmail
from dotenv import load_dotenv
from env_loader import EMAIL, APP_PASSWORD
from weekly_report import generate_report

load_dotenv()


def send_report():


    yag = yagmail.SMTP(
        EMAIL,
        APP_PASSWORD
    )

    contents = generate_report()

    yag.send(
        to=EMAIL,
        subject="Weekly BTC Trading Report",
        contents=contents
    )

    print("EMAIL SENT")