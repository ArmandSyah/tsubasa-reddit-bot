import pprint
import unittest

from anime.malinfo import malscrapper, malsearch


class TestMalScrapper(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_links(self):
        title = 'Renai Boukun'
        mal_links = malsearch.get_anime_links(title)
        pprint.pprint(mal_links)
        self.assertIsNotNone(mal_links)

    def test_scrape_info(self):
        title = 'Jojo'
        mal_links = malsearch.get_anime_links(title)
        jojo_anime = malscrapper.MALAnimeInfo(mal_links[0])
        pprint.pprint(jojo_anime.get_names())
        pprint.pprint(jojo_anime.get_airdate())
        pprint.pprint(jojo_anime.get_synopsis())
        self.assertIsNotNone(jojo_anime)

    def test_all_mal_links(self):
        title = 'Food Wars'
        mal_links = malsearch.get_anime_links(title)
        for link in mal_links:
            anime = malscrapper.MALAnimeInfo(link)
            with self.subTest(anime=anime):
                self.assertIsNotNone(anime)

if __name__ == '__main__':
    unittest.main()

