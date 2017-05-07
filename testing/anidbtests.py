import unittest
import requests
from time import sleep

import anime.malinfo.malsearch as search
from anime.malinfo.malscrapper import MALAnimeInfo as Anime
from anime.anidbinfo import anidbscrapper as anidb


class TestAniDB(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_anidb_exists(self):
        link = anidb.get_anidb_link('nanbaka')
        test_url = requests.get(link)
        self.assertIsNotNone(test_url)

    def test_fail_check(self):
        link = anidb.get_anidb_link('Non-existent anime')
        self.assertIsNone(link)

    def test_with_mal(self):
        mal_search = search.get_mal_anime_links('nanbaka 2017')
        nanbaka_anime = Anime(mal_search[0])
        names = nanbaka_anime.get_names()
        url = anidb.get_anidb_link(names['Main'])
        self.assertEqual(url, 'https://anidb.net/perl-bin/animedb.pl?show=anime&aid=12558')

    def test_fail_mal(self):
        mal_search = search.get_mal_anime_links('nanbaka 2017')
        nanbaka_anime = Anime(mal_search[0])
        names = nanbaka_anime.get_names()
        url = anidb.get_anidb_link(names['English'])
        self.assertNotEqual(url, 'https://anidb.net/perl-bin/animedb.pl?show=anime&aid=12558')

    def tearDown(self):
        sleep(5)

if __name__ == '__main__':
    unittest.main()