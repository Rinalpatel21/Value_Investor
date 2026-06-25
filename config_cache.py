import json


def save_cache(config):

    with open(
        "config_cache.json",
        "w"
    ) as f:

        json.dump(
            config,
            f,
            indent=4
        )


def load_cache():

    try:

        with open(
            "config_cache.json",
            "r"
        ) as f:

            config = json.load(f)

        return config

    except FileNotFoundError:

        print("Using default config")

        return {

            "dca_pct": 3,

            "atr_multiplier": 2,

            "stop_loss_multiplier": 2.5,

            "take_profit_multiplier": 5,

            "portfolio_stop": 25

        }