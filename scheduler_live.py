import schedule
import time

from live_trading import run_live_agent

from config_manager import load_config

config = load_config()

def reload_config():

    global config

    config = load_config()

    print("CONFIG RELOADED")


schedule.every().hour.do(
    reload_config
)

print("Live Scheduler Started")

while True:

    schedule.run_pending()

    time.sleep(1)