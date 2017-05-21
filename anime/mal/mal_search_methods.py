import os
import re
from collections import OrderedDict

import spice_api as spice

from settings import configloading as config
from anime import utilities


def get_mal_links(title):
    """Iterates through all search methods until link is constructed"""
    mal_regex = re.compile(r'http(s)?://myanimelist.net/anime/([0-9]){1,5}(/.*)?')
    link_dispatcher = {'spice': _get_mal_links_by_spice,
                       'mal': _get_mal_links_by_mal_api,
                       'brute': _get_mal_links_by_brute_force}

    for _, v in link_dispatcher.items():
        mal_url = v(title)
        if mal_url is None:
            continue
        if re.match(mal_regex, mal_url) is not None:
            return mal_url


def _get_mal_links_by_spice(title):
    """Use Spice_API MAL Wrapper to retrive anime_id and use it to construct MAL link"""
    mal_config = config.load_mal_config()
    anime_id = None
    try:
        mal_credentials = spice.init_auth(mal_config['mal_username'], mal_config['mal_password'])
        mal_search = spice.search(title.strip(), spice.get_medium('anime'), mal_credentials)
        for m in mal_search:
            if m.title.lower() == title.lower() or m.english.lower() == title.lower():
                anime_id = mal_search[0].id
                break
    except Exception as e:
        print(e)
        return
    mal_url = f"https://myanimelist.net/anime/{anime_id}"
    return mal_url if anime_id is not None else None


def _get_mal_links_by_mal_api(title):
    """Use MAL's Official API to retrieve anime_id and use it to construct a MAL link"""
    mal_config = config.load_mal_config()
    anime_id = None
    try:
        mal_api_search = f"https://myanimelist.net/api/anime/search.xml?q={title.strip()}"
        mal_credentials = (mal_config['mal_username'], mal_config['mal_password'])
        mal_request = utilities.make_get_request(mal_api_search, mal_credentials)
        mal_soup = utilities.make_beautiful_soup_doc(mal_request.text, 'lxml')
        mal_entries = mal_soup.anime
        for m in mal_entries.findAll('entry'):
            synonyms = [s for s in m.synonyms.get_text().lower().split('; ')]
            if m.title.get_text().lower() == title.lower() or m.english.get_text().lower() == title.lower() or \
                    title.lower() in synonyms:
                anime_id = m.id.get_text()
                break
    except Exception as e:
        print(e)
        return
    mal_url = f"https://myanimelist.net/anime/{anime_id}"
    return mal_url if anime_id is not None else None


def _get_mal_links_by_brute_force(title):
    """Enter anime into MAL search bar and scrape for the first available MAL anime link"""

    title_slug = "%20".join(title.split(" "))
    mal_search_url = f"https://myanimelist.net/anime.php?q={title_slug}"
    mal_request = utilities.make_get_request(mal_search_url)
    soup = utilities.make_beatiful_soup_url(mal_request.url, "html.parser")
    links = [element for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=5)]
    link_dict = {link.get('href'): utilities.similar(link.get_text(), title) for link in links}
    ordered_links = list(OrderedDict(sorted(link_dict.items(), key=lambda t: t[1])))
    return ordered_links[-1] if len(ordered_links) > 0 else None


def main():
    print(_get_mal_links_by_brute_force('My Hero Academia Season 2'))
    print(_get_mal_links_by_mal_api('Pokemon'))

if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-2]))
    print(os.getcwd())
    main()