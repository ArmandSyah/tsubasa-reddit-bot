import unittest

from anime.malinfo import malsearch
from anime.malinfo.malscrapper import MALAnimeInfo as Anime
from anime.anilistinfo import anilistscrapper


class TestAnilistInfo(unittest.TestCase):

    def setUp(self):
        pass

    def test_anilist_link_exists(self):
        title = 'Pokemon'
        mal_links = malsearch.get_mal_anime_links(title)
        pokemon_anime = Anime(mal_links[0])
        anilist_url = anilistscrapper.get_anilist_links(pokemon_anime.get_names())
        print(anilist_url)
        self.assertIsNotNone(anilist_url)

    def test_correct_anilist_link(self):
        title = 'Jojo'
        mal_links = malsearch.get_mal_anime_links(title)
        jojo_anime = Anime(mal_links[0])
        anilist_url = anilistscrapper.get_anilist_links(jojo_anime.get_names())
        self.assertEqual(anilist_url, 'https://anilist.co/anime/666')

    def test_correct_anilist_link2(self):
        title = 'Pokemon'
        mal_links = malsearch.get_mal_anime_links(title)
        pokemon_anime = Anime(mal_links[0])
        anilist_url = anilistscrapper.get_anilist_links(pokemon_anime.get_names())
        self.assertEqual(anilist_url, 'https://anilist.co/anime/527')


if __name__ == '__main__':
    unittest.main()