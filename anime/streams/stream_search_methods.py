import string

from crunchyroll.apis.meta import MetaApi

from anime import utilities


def search_crunchyroll(anime):
    """Searches if anime exists on Crunchyroll and returns a link"""

    crunchy_api = MetaApi()
    crunchyroll_listing = list(crunchy_api.search_anime_series(anime))
    if len(crunchyroll_listing) <= 0:
        print('No crunchyroll listings found')
        return
    return crunchyroll_listing[0].url


def search_funimation(anime):
    """Checks if anime exists on Funimation website and returns a link"""
    exclude = set(string.punctuation)
    show_slug = ''.join(ch for ch in anime if ch not in exclude)
    show_slug = '-'.join(show_slug.split(" ")).lower()
    funi_url = f'https://www.funimation.com/shows/{show_slug}/'
    funi_url = utilities.make_get_request(funi_url)
    if funi_url is None:
        return
    return funi_url.url


def search_animelab(anime):
    """Checks if anime title exists on AnimeLab website and returns a link"""
    show_slug = '-'.join(anime.split(" "))
    animelab_url = f'https://www.animelab.com/shows/{show_slug}'
    animelab_url = utilities.make_get_request(animelab_url)
    if animelab_url is None:
        return
    return animelab_url.url


