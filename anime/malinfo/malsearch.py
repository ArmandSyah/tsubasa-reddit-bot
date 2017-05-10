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
    pass


def get_links_by_brute_force(title):
    """
    Uses beautiful soup to enter anime into search bar and then extract links of anime pages from the search results
    :type title: str
    :return: Mal Search Links
    """

    title = "%20".join(title.split(" "))
    mal_search_url = f"https://myanimelist.net/anime.php?q={title}"
    try:
        res = requests.get(mal_search_url)
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Might have made too many requests here")
        return
    soup = BeautifulSoup(res.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=5)]
    return links


def make_get_request(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        return
    return r


def main():
    print(get_links_by_google_search('steins;gate'))

if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()