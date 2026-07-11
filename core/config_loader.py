import json


def load_config():

    with open("core/config.json","r") as file:

        config = json.load(file)

    return config