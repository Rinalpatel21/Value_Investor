import schedule
import time

from live_trading import run_live_agent
from gmail_report import send_report

schedule.every(30).minutes.do(
    run_live_agent
)

schedule.every().monday.at(
    "09:00"
).do(
    send_report
)

print("BTC Agent Started")

while True:

    schedule.run_pending()

    time.sleep(60)