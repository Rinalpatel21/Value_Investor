import schedule
import time

from gmail_report import send_report


schedule.every().monday.at(
    "09:00"
).do(send_report)


print("Weekly Email Scheduler Started")


while True:

    schedule.run_pending()

    time.sleep(60)