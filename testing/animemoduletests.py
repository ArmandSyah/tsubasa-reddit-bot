import pprint
import unittest
from anime import malscrapper, anidbscrapper, anilistscrapper, streamscrapper


class TestMalScrapper(unittest.TestCase):

    def setUp(self):
        pass

    def mal_scrapper_test(self):
        title = 'Renai Boukun'
        mal_links = malscrapper.get_anime_links(title)
        pprint.pprint(mal_links)
        self.assertIsNotNone(mal_links)

if __name__ == '__main__':
    unittest.main()

