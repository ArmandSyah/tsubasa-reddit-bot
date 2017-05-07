import unittest

from anime.malinfo import malsearch
from anime.malinfo.malscrapper import MALAnimeInfo as Anime


class TestMalScrapper(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_links(self):
        title = 'Renai Boukun'
        mal_links = malsearch.get_mal_anime_links(title)
        self.assertIsNotNone(mal_links)

    def test_scrape_info(self):
        title = 'Jojo'
        mal_links = malsearch.get_mal_anime_links(title)
        jojo_anime = Anime(mal_links[0])
        print(mal_links[0])
        self.assertIsNotNone(jojo_anime)

    def test_all_mal_links(self):
        title = 'Food Wars'
        mal_links = malsearch.get_mal_anime_links(title)
        for link in mal_links:
            anime = Anime(link)
            with self.subTest(anime=anime):
                self.assertIsNotNone(anime)


if __name__ == '__main__':
    unittest.main()
