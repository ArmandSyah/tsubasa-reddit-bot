import requests
import bs4
import sys
import re
import config
import json
import pprint
from time import sleep

'''import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Start of program')'''


class MALAnimeInfo(object):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def _soup_maker(url):
        """Create BeautifulSoup Object to parse HTML easily"""
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException as request_error:
            print("Failed to connect to url")
            print(request_error)
            sys.exit(1)
        return bs4.BeautifulSoup(res.text, "html.parser")

    def get_synopsis(self):
        """Get Synopsis of anime from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        synopsis = " ".join(soup.find(itemprop='description').get_text().split(" "))
        return synopsis

    def get_names(self):
        """Get the different names of the anime from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        main_name = soup.select("h1.h1")[0].text.strip()
        english_name = (" ".join(soup.find_all
                                 (text=re.compile(r'^English.*'))[0].string.parent.parent.text.strip().split(" ")[1:])
                        if len(soup.find_all(text=re.compile(r'^English.*'))) > 0 else None)
        synonyms = (" ".join(soup.find_all
                             (text=re.compile(r'^Synonyms.*'))[0].string.parent.parent.text.strip().split(" ")[1:])
                    if len((soup.find_all(text=re.compile(r'^Synonyms.*')))) > 0 else '').split(', ')
        japanese_name = (" ".join(soup.find_all
                                  (text=re.compile(r'^Japanese.*'))[0].string.parent.parent.text.strip().split(" ")[1:])
                         if len(soup.find_all(text=re.compile(r'^Japanese.*'))) > 0 else None)

        return {'Main': main_name, 'English': english_name, 'Synonyms': synonyms, 'Japanese': japanese_name}

    def get_type(self):
        """Get the anime's type from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        anime_type = soup.select("div > a")[15].text
        return anime_type

    def get_number_episodes(self):
        """Get anime's number of episode from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        episodes = [s for s in soup.select("div.spaceit")[0].text.split()][1]
        return episodes

    def get_status(self):
        """Get anime's airing status from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        status = soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                         'Finished Airing',
                                                                         'Not yet aired'])))[0].strip()
        return status

    def get_airdate(self):
        """Get anime's airdate from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        airdate = " ".join(soup.select("div.spaceit")[1].text.strip().split(" ")[2:])
        return airdate

    def get_source(self):
        """Get an anime's original source from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        source = " ".join(soup.select("div.spaceit")[3].text.split() if ("Source:" in soup.select(
            "div.spaceit")[3].text) else soup.select("div.spaceit")[4].text.split()).split(" ")[1]
        return source

    def get_genre_listing(self):
        """Get an anime's genre's from it's MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        genres = soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3]
                                                             if ("Source:" in soup.select("div.spaceit")[3].text)
                                                             else soup.select("div.spaceit")[4]) + 1].text.strip().split("\n")[1]
        return genres

    def get_duration(self):
        """Get the duration of an anime"""
        soup = MALAnimeInfo._soup_maker(self.url)
        duration = " ".join(soup.select("div.spaceit")[4].text.strip().split(" ")[2:]
                            if ("Duration:" in soup.select("div.spaceit")[4].text)
                            else soup.select("div.spaceit")[5].text.strip().split(" ")[2:])
        return duration


def get_anime_links(title):
    """
    Uses beautiful soup to enter anime into search bar and then extract links of anime pages from the search results
    :param title: 
    :return: 
    """

    search_url = f"https://myanimelist.net/anime.php?q={title}"
    print(search_url)

    try:
        res = requests.get(search_url)
        res.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"No such link {search_url} found, exiting program")
        sys.exit(1)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=5)]

    return links


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
            print(f"\nChecking Link #{index + 1}")
            anime = MALAnimeInfo(link)
            anime_name, anime_synopsis, anime_info_dict, link = get_anime_info(link)

            for key, value in anime_name.items():
                pp.pprint(f'{key} : {value}')

            print(f"Synopsis: {anime.get_synopsis()}")

            for key, value in anime_info_dict.items():
                if key is 'Name':
                    continue
                pp.pprint(f"{key}: {value}")

            print("\nNow just wait...")
            sleep(5)
            anilist_page = anilist_link_maker(anime_name)
            print(f"Anilist Link: {anilist_page}")
            print("\nWait again...")
            sleep(5)


if __name__ == '__main__':
    main()
