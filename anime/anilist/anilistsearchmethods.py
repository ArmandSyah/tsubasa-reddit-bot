import json
import os

from settings import configloading as config
from anime import utilities


def get_anilist_link_by_google(title):
    """Obtain anime's anilist page through custom google search"""
    google_config = config.load_google_config()
    try:
        google_search = f"https://www.googleapis.com/customsearch/v1?q=site:anilist.co anime{title.strip()}&start=1&key=" \
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

    anilist_link = make_anilist_link(title, access_data)
    return anilist_link


def make_anilist_link(title, access_data):
    """Construct the anilist listing url"""
    anilist_url = f'https://anilist.co/api/anime/search/{title}?access_token={access_data["access_token"]}'

    # Make a GET Request to anilist, to get info on specific anime show
    show_info = anilist_json_request(anilist_url, title)

    if show_info is None:
        return

    anilist_anime_page = f'https://anilist.co/anime/{show_info["id"]}'
    anilist_anime_page = utilities.make_get_request(anilist_anime_page)
    return anilist_anime_page.url


def anilist_json_request(anilist_url, title):

    get_anilist_anime = utilities.make_get_request(anilist_url)

    anilist_show_json = json.loads(get_anilist_anime.text)

    if 'error' in anilist_show_json:
        print("Could not find this particular entry")
        return

    for show in anilist_show_json:
        if (title.lower() == show['title_english'].lower() or
                    title.lower() == show['title_romaji'].lower() or
                    title == show['title_japanese'] or
                    title.lower() in [s.lower() for s in show['synonyms']]):
            return show

    print('couldn\'t find name')
    return


def main():
    print(get_anilist_link_by_api('prison school'))


if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()
