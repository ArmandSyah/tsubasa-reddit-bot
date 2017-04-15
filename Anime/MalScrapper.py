import requests
import bs4
import sys
import re
from time import sleep
import config
import json
import pprint


def get_anime_links(title):
    """
    Uses beautiful soup to enter anime into search bar and then extract links of anime pages from the search results
    :param title: 
    :return: 
    """

    search_url = "https://myanimelist.net/anime.php?q={}".format(title)
    print(search_url)

    try:
        res = requests.get(search_url)
        res.raise_for_status()
    except requests.exceptions.RequestException:
        print("No such link {} found, exiting program".format(search_url))
        sys.exit(1)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=5)]
    print(links)

    return links


def get_anime_info(link):
    """
    Opens up a link to an anime page and then scrapes out all acompanying info
    :param link: A MAL link to a specific anime
    :return: A tuple containing the name of the anime, information about the anime, and a MAL Link to the anime
    """
    try:
        res = requests.get(link)
        res.raise_for_status()
    except requests.exceptions.RequestException as request_error:
        print("Failed to connect to url")
        print(request_error)
        sys.exit(1)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    synopsis = " ".join(soup.find(itemprop='description').get_text().split(" "))

    anime_info_dict = {'Name': {'Main': soup.select("h1.h1")[0].text.strip(),
                                'English': " ".join(soup.find_all
                                                    (text=re.compile(r'^English.*'))[0].string.parent.parent.text.strip().split(" ")[1:])
                                if len(soup.find_all(text=re.compile(r'^English.*'))) > 0 else None,
                                'Synonyms': (" ".join(soup.find_all
                                                      (text=re.compile(r'^Synonyms.*'))[0].string.parent.parent.text.strip().split(" ")[1:])
                                             if len((soup.find_all(text=re.compile(r'^Synonyms.*')))) > 0 else '').split(', '),
                                'Japanese': " ".join(soup.find_all
                                                     (text=re.compile(r'^Japanese.*'))[0].string.parent.parent.text.strip().split(" ")[1:])
                                if len(soup.find_all(text=re.compile(r'^Japanese.*'))) > 0 else None},
                       'Type': soup.select("div > a")[15].text,
                       'Episodes': [int(s) for s in soup.select("div.spaceit")[0].text.split() if s.isdigit()][0],
                       'Status': soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                                         'Finished Airing',
                                                                                         'Not yet aired'])))[0].strip(),
                       'Aired': " ".join(soup.select("div.spaceit")[1].text.strip().split(" ")[2:]),
                       'Source': " ".join(soup.select("div.spaceit")[3].text.split() if ("Source:" in soup.select(
                           "div.spaceit")[3].text) else soup.select("div.spaceit")[4].text.split()).split(" ")[1],
                       'Genres': soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3] if (
                           "Source:" in
                           soup.select
                           ("div.spaceit")[3].text) else soup.select("div.spaceit")[4]) + 1].text.strip().split("\n")[1],
                       'Duration': " ".join(soup.select("div.spaceit")[4].text.strip().split(" ")[2:] if
                                            ("Duration:" in soup.select("div.spaceit")[4].text) else soup.select("div.spaceit")[
                                                                                                         5].text.strip().split(" ")[2:])}

    return anime_info_dict['Name'], synopsis, anime_info_dict, link


def anilist_link_maker(title):
    """
    Takes a title parameter and finds the anilist page for the specific anime
    :param title: Name entry from anime_info_dict dictionary, in the form 
                 {'Main': name, 'English': name, 'Synonyms': [list of names], 'Japanese': name}
    :return: An AniList link to the anime
    """

    title_url = "%20".join(title['Synonyms'][0].split(" "))
    title_url_alt = "%20".join(title['Main'].split(" "))

    # Client info to be use to gain access to AniList API. All fields are hidden in a config.py file
    anilist_client_info = {'grant_type': config.grant_type,
                           'client_id': config.client_id,
                           'client_secret': config.client_secret}

    # Make a POST Request to anilist, returning back an access token for the GET requests
    try:
        post_anilist = requests.post('https://anilist.co/api/auth/access_token', data=anilist_client_info)
        post_anilist.raise_for_status()
        access_data = post_anilist.json()
    except requests.exceptions.RequestException:
        print("Failed to make the post request, returning")
        return

    anilist_url = 'https://anilist.co/api/anime/search/{0}?access_token={1}'.format(title_url, access_data['access_token'])
    anilist_url_alt = 'https://anilist.co/api/anime/search/{0}?access_token={1}'.format(title_url_alt, access_data['access_token'])

    # Make a GET Request to anilist, to get info on specific anime show
    try:
        get_anilist_anime = requests.get(anilist_url)
        get_anilist_anime_alt = requests.get(anilist_url_alt)
        get_anilist_anime.raise_for_status()
        get_anilist_anime_alt.raise_for_status()
        anilist_show_json = json.loads(get_anilist_anime.text)
        anilist_show_json_alt = json.loads(get_anilist_anime_alt.text)
    except requests.exceptions.RequestException:
        print("Failed to make Get Request")
        return

    if 'error' in anilist_show_json and 'error' in anilist_show_json_alt:
        print("This entry probably doesn't exist on AniListDB")
        return

    show_info = None
    for show in anilist_show_json:

        if 'error' in anilist_show_json:
            break

        if len([t for t in title['Synonyms'] if t in show['synonyms']]) > 0:
            show_info = show
            break

        if (title['Main'] in show['synonyms']or
                    title['English'] in show['synonyms']):
            show_info = show
            break

        if (t == show['title_english'] for t in title['Synonyms']):
            show_info = show
            break

        if title['Main'] == show["title_romaji"]:
            show_info = show
            break

        if title['Japanese'] == show["title_japanese"]:
            show_info = show
            break

    if show_info is None:
        for show in anilist_show_json_alt:
            show_synonyms = set(show['synonyms'])
            print(show_synonyms)

            if len([t for t in title['Synonyms'] if t in show_synonyms]) > 0:
                show_info = show
                break

            if (title['Main'] in show['synonyms'] or
                        title['English'] in show['synonyms']):
                show_info = show
                break

            if (t == show['title_english'] for t in title['Synonyms']):
                show_info = show
                break

            if title['Main'] == show["title_romaji"]:
                show_info = show
                break

            if title['Japanese'] == show["title_japanese"]:
                show_info = show
                break

    if show_info is None:
        return

    anilist_anime_page = 'https://anilist.co/anime/{0}'.format(show_info['id'])
    # Construct a link to the anime's anilist page, and test to see if it works before returning it
    try:
        test_link = requests.get(anilist_anime_page)
        test_link.raise_for_status()
    except requests.exceptions.RequestException:
        print("Failed to make the last Request")
        return

    return anilist_anime_page


def main():
    """
    Main to be used for testing out this specific module directly
    :return: 
    """
    pp = pprint.PrettyPrinter(indent=4)
    while True:
        print("What show are you looking up: ")
        title = str(input()).split(" ")
        title = '_'.join(map(str, title))
        print("Searching for anime links on MAL...")
        anime_links = get_anime_links(title)

        for index, link in enumerate(anime_links):
            print("\nChecking Link #{}".format(index + 1))
            anime_name, anime_synopsis, anime_info_dict, link = get_anime_info(link)

            for key, value in anime_name.items():
                print(f'{key} : {value}')

            print("Synopsis: {}".format(anime_synopsis))

            for key, value in anime_info_dict.items():
                if key is 'Name':
                    continue
                pp.pprint("{0}: {1}".format(key, value))

            print("\nNow just wait...")
            sleep(5)
            anilist_page = anilist_link_maker(anime_name)
            print("Anilist Link: {}".format(anilist_page))
            print("\nWait again...")
            sleep(5)


if __name__ == '__main__':
    main()
