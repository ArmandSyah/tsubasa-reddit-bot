import json


def load_anilist_config():
    with open('..\\settings\\anilist_config.json', 'r') as f:
        return json.load(f)


def load_mal_config():
    with open('..\\settings\\mal_config.json', 'r') as f:
        return json.load(f)


def load_google_config():
    with open('..\\settings\\google_config.json', 'r') as f:
        return json.load(f)