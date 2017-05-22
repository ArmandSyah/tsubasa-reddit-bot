import json
from collections import OrderedDict

from anime import utilities


def make_anilist_link(title, access_data):
    """Construct the anilist listing url"""
    anilist_url = f'https://anilist.co/api/anime/search/{title.strip()}?access_token={access_data["access_token"]}'

    show_id = _process_anilist_json_request(anilist_url, title)
    anilist_anime_page = f'https://anilist.co/anime/{show_id}'
    anilist_anime_page = utilities.make_get_request(anilist_anime_page)
    return anilist_anime_page.url


def _process_anilist_json_request(anilist_url, title):
    """Process through json obtained through anilist api search, and match the names"""
    get_anilist_anime = utilities.make_get_request(anilist_url)
    anilist_show_json = json.loads(get_anilist_anime.text)
    if 'error' in anilist_show_json:
        print("Could not find this particular entry through anilist api")
        return
    anilist_dict = {show['id']: max(utilities.similar(title.lower(), show['title_english'].lower()), utilities.similar(
                    title.lower(), show['title_romaji'].lower())) for show in anilist_show_json}
    ordered_links = list(OrderedDict(sorted(anilist_dict.items(), key=lambda t: t[1])))
    return ordered_links[-1] if len(ordered_links) > 0 else None