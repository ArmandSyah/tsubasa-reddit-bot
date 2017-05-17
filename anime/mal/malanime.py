from anime import utilities
from . import malsoup


class MalAnime(object):
    def __init__(self, url):
        """Computation of fields only done when necessary"""
        self._soup = utilities.make_beatiful_soup_url(url)
        self._id = pull_mal_id(url)
        self._synopsis = None
        self._main_name = None
        self._english_name = None
        self._japanese_name = None
        self._synonyms = None
        self._anime_type = None
        self._episodes = None
        self._status = None
        self._airdate = None
        self._source = None
        self._genres = None
        self._duration = None
        self._rating = None

    @property
    def id(self):
        return self._id

    @property
    def synopsis(self):
        if self._synopsis is None:
            self._synopsis = malsoup.scrape_synopsis(self._soup)
        return self._synopsis

    @property
    def main_name(self):
        if self._main_name is None:
            self._main_name = malsoup.scrape_main_name(self._soup)
        return self._main_name

    @property
    def english_name(self):
        if self._english_name is None:
            self._english_name = malsoup.scrape_english_name(self._soup)
        return self._english_name

    @property
    def japanese_name(self):
        if self._japanese_name is None:
            self._japanese_name = malsoup.scrape_japanese_name(self._soup)
        return self._japanese_name

    @property
    def synonyms(self):
        if self._synonyms is None:
            self._synonyms = malsoup.scrape_synonyms(self._soup)
        return self._synonyms

    @property
    def anime_type(self):
        if self._anime_type is None:
            self._anime_type = malsoup.scrape_anime_type(self._soup)
        return self._anime_type

    @property
    def episodes(self):
        if self._episodes is None:
            self._episodes = malsoup.scrape_episodes(self._soup)
        return self._episodes

    @property
    def status(self):
        if self._status is None:
            self._status = malsoup.scrape_status(self._soup)
        return self._status

    @property
    def airdate(self):
        if self._airdate is None:
            self._airdate = malsoup.scrape_airdate(self._soup)
        return self._airdate

    @property
    def source(self):
        if self._source is None:
            self._source = malsoup.scrape_source(self._soup)
        return self._source

    @property
    def genres(self):
        if self._genres is None:
            self._genres = malsoup.scrape_genres(self._soup)
        return self._genres

    @property
    def duration(self):
        if self._duration is None:
            self._duration = malsoup.scrape_duration(self._soup)
        return self._duration

    @property
    def rating(self):
        if self._rating is None:
            self._rating = malsoup.scrape_rating(self._soup)
        return self._rating


def pull_mal_id(mal_url):
    return [s for s in mal_url.split('/') if s.isdigit()][0]
