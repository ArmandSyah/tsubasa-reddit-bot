import unittest
from time import sleep

import anime.mal.malsearchmethods as search
from anime.mal.malanime import MalAnime as Anime
from anime.anilist import anilistsearchmethods


class TestAnilistInfo(unittest.TestCase):

    def setUp(self):
        pass

    def test_anilist_link_exists(self):
        title = 'Pokemon'
        mal_links = search.get_links_by_brute_force(title)
        pokemon_anime = Anime(mal_links[0])
        anilist_url = anilistsearchmethods.get_anilist_links(pokemon_anime.names())
        print(anilist_url)
        self.assertIsNotNone(anilist_url)

    def test_correct_anilist_link(self):
        title = 'Jojo'
        mal_links = search.get_links_by_brute_force(title)
        jojo_anime = Anime(mal_links[0])
        anilist_url = anilistsearchmethods.get_anilist_links(jojo_anime.names())
        self.assertEqual(anilist_url, 'https://anilist.co/anime/666')

    def test_correct_anilist_link2(self):
        title = 'Pokemon'
        mal_links = search.get_links_by_brute_force(title)
        pokemon_anime = Anime(mal_links[0])
        anilist_url = anilistsearchmethods.get_anilist_links(pokemon_anime.names())
        self.assertEqual(anilist_url, 'https://anilist.co/anime/527')

    def tearDown(self):
        sleep(5)


if __name__ == '__main__':
    unittest.main()