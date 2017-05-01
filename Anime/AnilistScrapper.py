import requests
import config
import json


def post_request(url, query_parameters):
    """Makes an HTTP Post Request"""
    try:
        post_data = requests.post(url, data=query_parameters)
        post_data.raise_for_status()
    except requests.exceptions.RequestException:
        print("Failed to make the post request, returning")
        return
    return post_data


def get_request(url):
    try:
        get_data = requests.get(url)
        get_data.raise_for_status()
    except requests.exceptions.RequestException:
        print("Failed to make the last Request")
        return
    return get_data


def anilist_link_maker(titles):
    """
    Takes a title parameter and finds the anilist page for the specific anime
    :param titles: Name entry from anime_info_dict dictionary, in the form 
                 {'Main': name, 'English': name, 'Synonyms': [list of names], 'Japanese': name}
    :return: An AniList link to the anime
    """

    # Client info to be use to gain access to AniList API. All fields are hidden in a config.py file
    anilist_client_info = {'grant_type': config.grant_type,
                           'client_id': config.client_id,
                           'client_secret': config.client_secret}

    # Make a POST Request to anilist, returning back an access token for the GET requests
    anilist_post = post_request('https://anilist.co/api/auth/access_token', anilist_client_info)
    access_data = anilist_post.json()

    title_slugs = anilist_slugs(titles)

    for t in title_slugs:
        anilist_url = f'https://anilist.co/api/anime/search/{t}?access_token={access_data["access_token"]}'

        # Make a GET Request to anilist, to get info on specific anime show
        show_info = anilist_json_request(anilist_url, titles)

        if show_info is None:
            continue

        anilist_anime_page = f'https://anilist.co/anime/{show_info["id"]}'

        # Construct a link to the anime's anilist page, and test to see if it works before returning it
        testing_link = get_request(anilist_anime_page)
        if testing_link is not None:
            return anilist_anime_page
        else:
            continue

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


def anilist_json_request(anilist_url, title):
    """
    Pull JSON data from AniList.co for the requested show
    :param anilist_url: GET request url, obtaining anime show info from AniList API
    :param title: Name entry from anime_info_dict dictionary, in the form 
                 {'Main': name, 'English': name, 'Synonyms': [list of names], 'Japanese': name}
    :return: JSON data for 
    """

    get_anilist_anime = get_request(anilist_url)

    anilist_show_json = json.loads(get_anilist_anime.text)

    if 'error' in anilist_show_json:
        print("Could not find this particular entry")
        return

    for show in anilist_show_json:
        if True in [t == title['Main'] for t in show['synonyms']]:
            return show

        if True in [t == title['English'] for t in show['synonyms']]:
            return show

        if True in [t == show['title_english'] for t in title['Synonyms']]:
            return show

        if title['Main'] == show["title_romaji"]:
            return show

        if title['Japanese'] == show["title_japanese"]:
            return show

    return