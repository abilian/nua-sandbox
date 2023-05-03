import json


def read_config():
    return json.load(open("_nua-config.json"))
