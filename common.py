import json
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CONFIG_FILE = os.path.join(__location__, "config.json")


def loadConfiguration(config_path=CONFIG_FILE):
    config = {}
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    return config
