# scheduler.py

import schedule
import time

from config_manager import load_config

config = load_config()

def reload_config():

    global config

    config = load_config()

    print("Config Reloaded")


schedule.every().hour.do(
    reload_config
)

while True:

    schedule.run_pending()

    time.sleep(10)