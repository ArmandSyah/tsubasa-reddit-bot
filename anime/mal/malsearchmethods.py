import requests
import json
import os
from bs4 import BeautifulSoup

import spice_api as spice

from settings import configloading as config


def get_links_by_google_search(title):
    """Get Anime Link by searching MAL through Google and construct link to anime that way"""
    google_config = config.load_google_config()
    try:
        google_search = f"https://www.googleapis.com/customsearch/v1?q=site:myanimelist.net anime{title.strip()}" + \
                        f"&start=1&key={google_config['google_api_key']}&cx={google_config['custom_search_engine_id']}"
        google_response = make_get_request(google_search).content.decode('utf8')
        google_result = json.loads(google_response)
        mal_url = google_result['items'][0]['formattedUrl']
    except:
        return
    return mal_url


def get_links_by_spice(title):
    """Use Spice_API MAL Wrapper to retrive anime_id and use it to construct MAL link"""
    mal_config = config.load_mal_config()
    try:
        mal_credentials = spice.init_auth(mal_config['mal_username'], mal_config['mal_password'])
        mal_search = spice.search(title.strip(), spice.get_medium('anime'), mal_credentials)
    except:
        return
    anime_id = mal_search[0].id
    mal_url = f"https://myanimelist.net/anime/{anime_id}"
    return mal_url


def get_links_by_mal_api(title):
    """Use MAL's Official API to retrieve anime_id and use it to construct a MAL link"""
    mal_config = config.load_mal_config()
    try:
        mal_api_search = f"https://myanimelist.net/api/anime/search.xml?q={title.strip()}"
        mal_credentials = (mal_config['mal_username'], mal_config['mal_password'])
        mal_request = make_get_request(mal_api_search, mal_credentials)
        mal_soup = BeautifulSoup(mal_request.text, 'lxml')
        mal_entries = mal_soup.anime
        anime_listings = [anime for anime in mal_entries.findAll('entry')]
        anime_id = anime_listings[0].id.get_text()
        mal_url = f"https://myanimelist.net/anime/{anime_id}"
    except:
        return
    return mal_url


def get_links_by_brute_force(title):
    """Enter anime into MAL search bar and scrape for the first available MAL anime link"""

    title = "%20".join(title.split(" "))
    mal_search_url = f"https://myanimelist.net/anime.php?q={title}"
    mal_request = make_get_request(mal_search_url)
    soup = BeautifulSoup(mal_request.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=5)]
    mal_url = links[0]
    return mal_url


def make_get_request(url, credentials=None):
    try:
        r = requests.get(url, auth=credentials)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        return
    return r


def main():
    print(get_links_by_mal_api('naruto'))

if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()