import json

CONFIG_FILE = "./config.json"


def loadConfiguration(config_path=CONFIG_FILE):
    config = {}
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    return config