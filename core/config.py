import json

def load_config():

    with open("core/config.json", "r") as f:
        config = json.load(f)

    return config