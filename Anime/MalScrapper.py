import requests
import bs4
import sys
import re
from time import sleep


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
        print(res)
    except requests.exceptions.RequestException:
        print("No such link {} found, exiting program".format(search_url))
        sys.exit(1)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=3)]
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
    except requests.exceptions.RequestException:
        print("Failed to connect to url")
        return

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    synopsis = " ".join(soup.find(itemprop='description').get_text().split(" "))

    anime_info_dict = {'Name': soup.select("h1.h1")[0].text,
                       'Type': soup.select("div > a")[15].text,
                       'Episodes': [int(s) for s in soup.select("div.spaceit")[0].text.split() if s.isdigit()][0],
                       'Status': soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                                         'Finished Airing'])))[0].strip(),
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
    :param title: Full title of anime to search for
    :return: An AniList link to the anime
    """

    title = "%20".join(title.split(" "))
    client_info = {'grant_type': 'client_credentials',
                   'client_id': 'my-id',
                   'client_secret': 'my-secret'}

    # Make a POST Request to anilist, returning back an access token for the GET requests
    try:
        post_anilist = requests.post('https://anilist.co/api/auth/access_token', data=client_info)
        access_data = post_anilist.json()
    except requests.exceptions.RequestException:
        print("Failed to make the post request, returning")
        return

    # Make a GET Request to anilist, to get info on specific anime show
    try:
        anilist_url = 'https://anilist.co/api/anime/search/{0}?access_token={1}'.format(title, access_data['access_token'])
        get_anilist_anime = requests.get(anilist_url)
        show_info = get_anilist_anime.json()[0]
    except requests.exceptions.RequestException:
        print("Failed to make Get Request")
        return

    # Construct a link to the anime's anilist page, and test to see if it works before returning it
    try:
        anilist_anime_page = 'https://anilist.co/anime/{0}/{1}'.format(show_info['id'], "".join(show_info['title_romaji'].split(" ")))
        test_link = requests.get(anilist_anime_page)
        test_link.raise_for_status()
        return anilist_anime_page
    except requests.exceptions.RequestException:
        print("Failed to make the last Request")
        return


def main():
    """
    Main to be used for testing out this specific module
    :return: 
    """
    while True:
        print("What show are you looking up: ")
        title = str(input()).split(" ")
        title = '_'.join(map(str, title))
        print("Searching for anime links on MAL...")
        anime_links = get_anime_links(title)

        for index, link in enumerate(anime_links):
            print("\nChecking Link #{}".format(index + 1))
            anime_name, anime_synopsis, anime_info_dict, link = get_anime_info(link)
            print("Name: {}".format(anime_name))
            print("Synopsis: {}".format(anime_synopsis))

            for key, value in anime_info_dict.items():
                print("{0}: {1}".format(key, value))

            print("\nNow just wait...")
            sleep(5)
            anilist_page = anilist_link_maker(anime_name)
            print("Anilist Link: {}".format(anilist_page))
            print("\nWait again...")
            sleep(5)


if __name__ == '__main__':
    main()
