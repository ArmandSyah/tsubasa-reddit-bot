import json
import re

from anime import utilities
from anime.anidb import anidbdatadumpscrape as anidbdata
from settings import configloading as config


def get_anidb_links(title):
    """Iterates through all search methods until link is constructed"""
    anidb_regex = re.compile(r'http(s)?://anidb.net/a([0-9]){1,5}')
    anidb_regex_alt = re.compile(r'http(s)?://anidb.net/perl-bin/animedb.pl\?show=anime&aid=([0-9]){1,5}')
    link_dispatcher = {'google': get_anidb_by_google_search,
                       'api': get_anidb_brute_force}

    for _, v in link_dispatcher.items():
        anidb_url = v(title)
        if re.match(anidb_regex, anidb_url) is not None or re.match(anidb_regex_alt, anidb_url) is not None:
            return anidb_url

    return


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
        animeid = anidbdata.get_animeid(title)
    except KeyError:
        print('Either title was mispelled or does not exist')
        return
    return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={animeid}'
