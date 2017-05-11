import requests
import re
from bs4 import BeautifulSoup


class MALAnimeInfo(object):
    def __init__(self, url):
        """Computation of fields only done when necessary"""
        self.url = url
        self._synopsis = None
        self._names = None
        self._anime_type = None
        self._episodes = None
        self._status = None
        self._airdate = None
        self._source = None
        self._genres = None
        self._duration = None

    @property
    def synopsis(self):
        """Get Synopsis of anime from MAL anime page"""
        if self._synopsis is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            synopsis = soup.find(itemprop='description').get_text()
            formatted_synopsis = " ".join(synopsis.split(" "))
            self._synopsis = formatted_synopsis
        return self._synopsis

    @property
    def names(self):
        """
        Get the different names of the anime from MAL anime page
        Returns a Dictionary in this form {'Main':, 'English':, 'Synonyms', 'Japanese'}
        Note: 'Synonyms' Key contains a list
        """
        if self._names is None:
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
            self._names = name_dict
        return self._names

    @property
    def anime_type(self):
        """Get the anime's type from MAL anime page"""
        if self._anime_type is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            anime_type = soup.select("div > a")[15].text
            self._anime_type = anime_type
        return self._anime_type

    @property
    def episodes(self):
        """Get anime's number of episode from MAL anime page"""
        if self._episodes is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            formatted_episodes = soup.select("div.spaceit")[0].text.split()
            self._episodes = formatted_episodes
        return self._episodes

    @property
    def status(self):
        """Get anime's airing status from MAL anime page"""
        if self._status is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            status = soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                             'Finished Airing',
                                                                             'Not yet aired'])))[0]
            formatted_status = status.strip()
            self._status = formatted_status
        return self._status

    @property
    def airdate(self):
        """Get anime's airdate from MAL anime page"""
        if self._airdate is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            airdate = soup.select("div.spaceit")[1].text.strip().split(" ")[2:]
            formatted_airdate = " ".join(airdate)
            self._airdate = formatted_airdate
        return self._airdate

    @property
    def source(self):
        """Get an anime's original source from MAL anime page"""
        if self._source is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            source = soup.select("div.spaceit")[3].text.split() \
                if ("Source:" in soup.select("div.spaceit")[3].text) \
                else soup.select("div.spaceit")[4].text.split()
            formatted_source = " ".join(source).split(" ")[1]
            self._source = formatted_source
        return self._source

    @property
    def genres(self):
        """Get an anime's genre's from it's MAL anime page"""
        if self._genres is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            genres = soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3]
                                        if ("Source:" in soup.select("div.spaceit")[3].text)
                                        else soup.select("div.spaceit")[4]) + 1]
            formatted_genres = genres.text.strip().split("\n")[1]
            self._genres = formatted_genres
        return self._genres

    @property
    def duration(self):
        """Get the duration of an anime"""
        if self._duration is None:
            soup = MALAnimeInfo._soup_maker(self.url)
            duration = (soup.select("div.spaceit")[4].text.strip().split(" ")[2:]
                            if ("Duration:" in soup.select("div.spaceit")[4].text)
                            else soup.select("div.spaceit")[5].text.strip().split(" ")[2:])
            formatted_duration = " ".join(duration)
            self._duration = formatted_duration
        return self._duration

    @staticmethod
    def _soup_maker(url):
        """Create BeautifulSoup Object to parse HTML easily"""
        res = ''
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException as request_error:
            print("Failed to connect to url")
            print(request_error)
        return BeautifulSoup(res.text, "html.parser")


