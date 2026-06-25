import schedule
import time
import subprocess


def run_strategy():

    print("Running BTC Agent...")

    subprocess.run(
        ["python","test.py"]
    )


schedule.every(30).minutes.do(
    run_strategy
)

print("BTC Agent Started")

while True:

    schedule.run_pending()

    time.sleep(1)