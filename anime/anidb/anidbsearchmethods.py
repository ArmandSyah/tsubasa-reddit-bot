import os
import json

from anime import utilities
from settings import configloading as config


def get_anidb_by_google_search(title):
    """Get Anime Link by searching anidb through Google and construct link to anime that way"""
    google_config = config.load_google_config()
    try:
        google_search = f"https://www.googleapis.com/customsearch/v1?q=site:anidb.net anime {title.strip()} &start=1&key=" \
                        f"{google_config['google_api_key']}&cx={google_config['custom_search_engine_id']}"
        google_response = utilities.make_get_request(google_search).content.decode('utf8')
        google_result = json.loads(google_response)
        anidb_url = google_result['items'][0]['formattedUrl']
    except Exception as e:
        raise e
    return anidb_url


def get_anidb_brute_force(title):
    """Takes an anime title, and makes a link to the associated AniDB page"""
    try:
        animeid = _get_animeid(title)
    except KeyError:
        print('Either title was mispelled or does not exist')
        return
    return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={animeid}'


def _get_animeid(title):
    """Searches through AniDB Titles found in AniDBTitles.txt"""
    if 'AnimeMessengerRedditBot\\anime\\anidb' not in os.getcwd():
        _set_proper_path()
    print(os.getcwd())
    with open('AniDBTitles.txt', 'r', encoding='utf8') as ani:
        anidb_titles = ani.read()
        anidb_titles = anidb_titles.split("\n")
        anidb_titles = [t.lower() for t in anidb_titles if "|en|" in t or "|x-jat|" in t]
    anime_dict = {}
    for anime in anidb_titles:
        anime = anime.split("|")
        anime_dict[anime[3].lower()] = anime[0]
    return anime_dict[title.lower()]


def _set_proper_path():
    os.chdir('..\\anime\\anidb')