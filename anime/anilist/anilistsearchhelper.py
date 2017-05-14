import json

from anime import utilities


def make_anilist_link(title, access_data):
    """Construct the anilist listing url"""
    anilist_url = f'https://anilist.co/api/anime/search/{title}?access_token={access_data["access_token"]}'

    # Make a GET Request to anilist, to get info on specific anime show
    show_info = _anilist_json_request(anilist_url, title)

    if show_info is None:
        return

    anilist_anime_page = f'https://anilist.co/anime/{show_info["id"]}'
    anilist_anime_page = utilities.make_get_request(anilist_anime_page)
    return anilist_anime_page.url


def _anilist_json_request(anilist_url, title):
    """Process through json obtained through anilist api search, and match the names"""
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