from config_manager import load_config

config = load_config()

print()

for k, v in config.items():

    print(k, "=", v)