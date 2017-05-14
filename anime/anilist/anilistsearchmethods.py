import json
import os
import re

from settings import configloading as config
from anime import utilities
from anime.anilist import anilistsearchhelper


def get_anilist_links(title):
    """Iterates through all search methods until link is constructed"""
    anilist_regex = re.compile(r'http(s)?://anilist.co/anime/([0-9]){1,5}(/.*)?')
    link_dispatcher = {'google': get_anilist_link_by_google,
                       'api': get_anilist_link_by_api}

    for _, v in link_dispatcher.items():
        anilist_url = v(title)
        if re.match(anilist_regex, anilist_url) is not None:
            return anilist_url

    return


def get_anilist_link_by_google(title):
    """Obtain anime's anilist page through custom google search"""
    google_config = config.load_google_config()
    try:
        google_search = f"https://www.googleapis.com/customsearch/v1?q=site:anilist.co anime {title.strip()}&start=1&key=" \
                        f"{google_config['google_api_key']}&cx={google_config['custom_search_engine_id']}"
        google_response = utilities.make_get_request(google_search).content.decode('utf8')
        google_result = json.loads(google_response)
        anilist_url = google_result['items'][0]['formattedUrl']
    except:
        return
    return anilist_url


def get_anilist_link_by_api(title):
    """Obtain anime's anilist page through using it's api"""

    # Client info to be use to gain access to AniList API.
    anilist_config = config.load_anilist_config()
    anilist_client_info = {'grant_type': anilist_config['grant_type'],
                           'client_id': anilist_config['client_id'],
                           'client_secret': anilist_config['client_secret']}

    anilist_post = utilities.make_post_request('https://anilist.co/api/auth/access_token', anilist_client_info)
    access_data = anilist_post.json()

    anilist_link = anilistsearchhelper.make_anilist_link(title, access_data)
    return anilist_link


def main():
    print(get_anilist_link_by_api('prison school'))


if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()
