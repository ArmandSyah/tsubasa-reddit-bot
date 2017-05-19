import os
import re

from settings import configloading as config
from anime import utilities
from anime.anilist import anilistsearchhelper


def get_anilist_links(title):
    """Iterates through all search methods until link is constructed"""
    anilist_regex = re.compile(r'http(s)?://anilist.co/anime/([0-9]){1,5}(/.*)?')
    link_dispatcher = {'api': _get_anilist_link_by_api}

    for _, v in link_dispatcher.items():
        anilist_url = v(title)
        if anilist_url is None:
            continue
        if re.match(anilist_regex, anilist_url) is not None:
            return anilist_url

    return


def _get_anilist_link_by_api(title):
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


def test_in_module():
    print(_get_anilist_link_by_api('prison school'))


if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    test_in_module()
