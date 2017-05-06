import pprint
import unittest
from anime import malscrapper, anidbscrapper, anilistscrapper, streamscrapper


class TestMalScrapper(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_links(self):
        title = 'Renai Boukun'
        mal_links = malscrapper.get_anime_links(title)
        pprint.pprint(mal_links)
        self.assertIsNotNone(mal_links)

    def test_scrape_info(self):
        title = 'Jojo'
        mal_links = malscrapper.get_anime_links(title)
        jojo_anime = malscrapper.MALAnimeInfo(mal_links[0])
        pprint.pprint(jojo_anime.get_names())
        self.assertIsNotNone(jojo_anime)


if __name__ == '__main__':
    unittest.main()

