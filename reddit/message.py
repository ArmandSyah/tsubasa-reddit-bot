from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime
from anime.anilist import anilistsearchmethods
from anime.anidb import anidbsearchmethods
from anime.streams import streamsearchmethods


def make_message(title):
    """Constructs message to be sent to reddit user"""
    comment = ""
    anime_info = _set_up(title)


def _set_up(title):
    mal_url = malsearchmethods.get_mal_links(title)
    anilist_url = anilistsearchmethods.get_anilist_links(title)
    anidb_url = anidbsearchmethods.get_anidb_links(title)
    anime = MalAnime(mal_url)
    crunchyroll_url = streamsearchmethods.search_crunchyroll(title)
    funimation_url = streamsearchmethods.search_funimation(title)
    animelab_url = streamsearchmethods.search_animelab(title)

    comment_info_dict = {'mal_url': mal_url,
                         'anilist_url': anilist_url,
                         'anidb_url': anidb_url,
                         'crunchyroll_url': crunchyroll_url,
                         'funimation_url': funimation_url,
                         'animelab_url': animelab_url,
                         'anime': anime}

    return comment_info_dict