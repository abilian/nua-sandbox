import json


def read_config():
    config = json.load(open("_nua-config.json"))
    return config
