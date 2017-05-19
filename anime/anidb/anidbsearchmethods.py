import json
import re

from anime import utilities
from anime.anidb import anidbsearchhelper
from settings import configloading as config


def get_anidb_links(title):
    """Iterates through all search methods until link is constructed"""
    anidb_regex = re.compile(r'http(s)?://anidb.net/a([0-9]){1,5}')
    anidb_regex_alt = re.compile(r'http(s)?://anidb.net/perl-bin/animedb.pl\?show=anime&aid=([0-9]){1,5}')
    link_dispatcher = {'google': _get_anidb_by_google_search,
                       'dat': _get_anidb_brute_force,
                       'xml': _get_anidb_by_xml}

    for _, v in link_dispatcher.items():
        anidb_url = v(title)
        if re.match(anidb_regex, anidb_url) is not None or re.match(anidb_regex_alt, anidb_url) is not None:
            return anidb_url

    return


def _get_anidb_by_google_search(title):
    """Get Anime Link by searching anidb through Google and construct link to anime that way"""
    google_config = config.load_google_config()
    try:
        google_search = f"https://www.googleapis.com/customsearch/v1?q=site:anidb.net anime {title.strip()} &start=1&key=" \
                        f"{google_config['google_api_key']}&cx={google_config['custom_search_engine_id']}"
        google_response = utilities.make_get_request(google_search).content.decode('utf8')
        google_result = json.loads(google_response)
        anidb_url = google_result['items'][0]['link']
    except Exception as e:
        raise e
    return anidb_url


def _get_anidb_by_xml(title):
    with open("AniDBTitlesXML.txt", "r", encoding='utf8') as anidb:
        anidb_xml_content = anidb.read()
    xml_soup = utilities.make_beautful_soup_doc(anidb_xml_content, 'lxml')
    anidb_animetitles = xml_soup.animetitles
    anidb_id = anidbsearchhelper.get_animeid_xml(title, anidb_animetitles)
    if anidb_id is None:
        return
    return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={anidb_id}'


def _get_anidb_brute_force(title):
    """Takes an anime title, and makes a link to the associated AniDB page"""
    try:
        anidb_id = anidbsearchhelper.get_animeid(title)
    except KeyError:
        print('Either title was mispelled or does not exist')
        return
    return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={anidb_id}'


def test_module():
    print(_get_anidb_brute_force('Nanbaka'))
    print(_get_anidb_by_xml('Nanbaka'))

if __name__ == '__main__':
    test_module()