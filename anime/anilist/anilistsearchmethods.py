import json
import os

from settings import configloading as config
from anime import utilities


def get_anilist_link_by_google(title):
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


def get_anilist_link(anime_names):
    """
    """

    # Client info to be use to gain access to AniList API.
    anilist_config = config.load_anilist_config()
    anilist_client_info = {'grant_type': anilist_config['grant_type'],
                           'client_id': anilist_config['client_id'],
                           'client_secret': anilist_config['client_secret']}

    anilist_post = utilities.make_post_request('https://anilist.co/api/auth/access_token', anilist_client_info)
    access_data = anilist_post.json()
    title_slugs = anilist_slugs(anime_names)

    for title_slug in title_slugs:
        anilist_link = make_anilist_link(title_slug, anime_names, access_data)
        if anilist_link is None:
            continue
        else:
            print(anilist_link)
            return anilist_link

    print("Couldn't find the anilist link")
    return


def anilist_slugs(names):
    """Designs URL slugs in the form of '%20'"""
    url_slugs = []
    for _, n in names.items():
        if type(n) is str:
            slug = "%20".join(n.split(" "))
            url_slugs.append(slug)
        elif type(n) is list:
            slug_list = ["%20".join(s.split(" ")) for s in n]
            url_slugs.extend(slug_list)
    return url_slugs


def make_anilist_link(title_slug, titles, access_data):
    anilist_url = f'https://anilist.co/api/anime/search/{title_slug}?access_token={access_data["access_token"]}'

    # Make a GET Request to anilist, to get info on specific anime show
    show_info = anilist_json_request(anilist_url, titles)

    if show_info is None:
        return

    anilist_anime_page = f'https://anilist.co/anime/{show_info["id"]}'
    return utilities.make_get_request(anilist_anime_page).url


def anilist_json_request(anilist_url, title):
    """
    Pull JSON data from AniList.co for the requested show
    :param anilist_url: GET request url, obtaining anime show info from AniList API
    :param title: Name entry from anime_info_dict dictionary, in the form 
                 {'Main': name, 'English': name, 'Synonyms': [list of names], 'Japanese': name}
    :return: JSON data for 
    """

    get_anilist_anime = utilities.make_get_request(anilist_url)

    anilist_show_json = json.loads(get_anilist_anime.text)

    if 'error' in anilist_show_json:
        print("Could not find this particular entry")
        return

    for show in anilist_show_json:
        if (True in [t == title['Main'] for t in show['synonyms']] or
                    True in [t == title['English'] for t in show['synonyms']] or
                    True in [t == show['title_english'] for t in title['Synonyms']] or
                    title['Main'] == show["title_romaji"] or
                    title['Japanese'] == show["title_japanese"]):
            return show

    return


def main():
    print(get_anilist_link_by_google(' シュタインズ・ゲート'))

if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()