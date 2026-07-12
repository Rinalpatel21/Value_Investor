from config_sheet import load_sheet_config
from config_cache import save_cache, load_cache



def load_config():

    try:

        config = load_sheet_config()

        save_cache(config)

        print("Loaded config from Google Sheet")

        return config

    except Exception:

        print("Google Sheet unavailable")

        return load_cache()