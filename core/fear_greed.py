import requests
import json

URL = "https://api.alternative.me/fng/"


def get_fear_greed():

    response = requests.get(URL)

    response.raise_for_status()

    data = response.json()["data"][0]

    result= {

        "value": int(data["value"]),

        "classification": data["value_classification"],

        "timestamp": data["timestamp"]

    }

    with open(

    "core/data/fear_greed.json",

    "w") as f:

      json.dump(result, f, indent=4)

    return result

if __name__ == "__main__":

    result = get_fear_greed()

    print(result)