import unittest
import requests
from time import sleep

import anime.mal.malsearchmethods as search
from anime.mal.malanime import MalAnime as Anime
from anime.streams import streamsearchmethods as streams


class TestStreams(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.skip('Focus on MAL Search')
    def test_crunchyroll1(self):
        crunchyroll_url = streams.search_crunchyroll('Attack on Titan')
        print(crunchyroll_url)
        crunchyroll_url = requests.get(crunchyroll_url)
        self.assertTrue(crunchyroll_url.status_code == 200)

    @unittest.skip('Focus on MAL Search')
    def test_crunchyroll2(self):
        crunchyroll_url = streams.search_crunchyroll('Twin Star Exorcists')
        print(crunchyroll_url)
        crunchyroll_url = requests.get(crunchyroll_url)
        self.assertTrue(crunchyroll_url.status_code == 200)

    def test_mal_search_chrunchyroll(self):
        mal_links = search.get_links_by_brute_force('Shingeki No Kyojin')
        shingeki_anime = Anime(mal_links[0])
        names = shingeki_anime.names()
        print(names['English'])
        crunchyroll_url = streams.search_crunchyroll(names['English'])
        crunchyroll_url = requests.get(crunchyroll_url)
        self.assertTrue(crunchyroll_url.status_code == 200)

    def tearDown(self):
        sleep(5)

if __name__ == '__main__':
    unittest.main()