import requests
import bs4
import sys
import re

'''import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Start of program')'''


class MALAnimeInfo(object):
    def __init__(self, url):
        self.url = url

    def get_synopsis(self):
        """Get Synopsis of anime from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        synopsis = soup.find(itemprop='description').get_text()
        formatted_synopsis = " ".join(synopsis.split(" "))
        return formatted_synopsis

    def get_names(self):
        """
        Get the different names of the anime from MAL anime page
        Returns a Dictionary in this form {'Main':, 'English':, 'Synonyms', 'Japanese'}
        Note: 'Synonyms' Key contains a list
        """
        soup = MALAnimeInfo._soup_maker(self.url)
        main_name = soup.select("h1.h1")[0].text
        english_name = soup.find_all(text=re.compile(r'^English.*'))[0]
        synonyms = soup.find_all(text=re.compile(r'^Synonyms.*'))[0] \
            if len(soup.find_all(text=re.compile(r'^Synonyms.*'))) > 0 else list()
        japanese_name = soup.find_all(text=re.compile(r'^Japanese.*'))[0]
        formatted_main_name = main_name.strip()
        formatted_english_name = (" ".join(english_name.string.parent.parent.text.strip().split(" ")[1:])
                                  if len(english_name) > 0 else None)
        formatted_synonyms = (" ".join(synonyms.string.parent.parent.text.strip().split(" ")[1:])
                              if len(synonyms) > 0 else '').split(', ')
        formatted_japanese_name = (" ".join(japanese_name.string.parent.parent.text.strip().split(" ")[1:])
                                   if len(japanese_name) > 0 else None)
        name_dict = {'Main': formatted_main_name,
                     'English': formatted_english_name,
                     'Synonyms': formatted_synonyms,
                     'Japanese': formatted_japanese_name}
        return name_dict

    def get_type(self):
        """Get the anime's type from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        anime_type = soup.select("div > a")[15].text
        return anime_type

    def get_number_episodes(self):
        """Get anime's number of episode from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        formatted_episodes = soup.select("div.spaceit")[0].text.split()
        return formatted_episodes

    def get_status(self):
        """Get anime's airing status from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        status = soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                         'Finished Airing',
                                                                         'Not yet aired'])))[0]
        formatted_status = status.strip()
        return formatted_status

    def get_airdate(self):
        """Get anime's airdate from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        airdate = soup.select("div.spaceit")[1].text.strip().split(" ")[2:]
        formatted_airdate = " ".join(airdate)
        return formatted_airdate

    def get_source(self):
        """Get an anime's original source from MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        source = soup.select("div.spaceit")[3].text.split() \
            if ("Source:" in soup.select("div.spaceit")[3].text) \
            else soup.select("div.spaceit")[4].text.split()
        formatted_source = " ".join(source).split(" ")[1]
        return formatted_source

    def get_genre_listing(self):
        """Get an anime's genre's from it's MAL anime page"""
        soup = MALAnimeInfo._soup_maker(self.url)
        genres = soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3]
                                    if ("Source:" in soup.select("div.spaceit")[3].text)
                                    else soup.select("div.spaceit")[4]) + 1]
        formatted_genres = genres.text.strip().split("\n")[1]
        return formatted_genres

    def get_duration(self):
        """Get the duration of an anime"""
        soup = MALAnimeInfo._soup_maker(self.url)
        duration = (soup.select("div.spaceit")[4].text.strip().split(" ")[2:]
                        if ("Duration:" in soup.select("div.spaceit")[4].text)
                        else soup.select("div.spaceit")[5].text.strip().split(" ")[2:])
        formatted_duration = " ".join(duration)
        return formatted_duration

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


