import string

from crunchyroll.apis.meta import MetaApi

from anime import utilities


def search_crunchyroll(anime):
    """Searches if anime exists on Crunchyroll and returns a link"""
    try:
        exclude = set(string.punctuation)
        anime = ''.join(ch for ch in anime if ch not in exclude)
        keywords = anime.split(' ')
        crunchy_api = MetaApi()
        crunchyroll_listing = []
        while len(keywords) > 0:
            crunchyroll_listing = list(crunchy_api.search_anime_series(' '.join(keywords)))
            if len(crunchyroll_listing) <= 0:
                print('No crunchyroll listings found')
                keywords.pop()
                continue
            else:
                break
    except:
        print('Crunchyroll url couldn\'t be retrieved')
        return

    return crunchyroll_listing[0].url if len(crunchyroll_listing) > 0 else None


def search_funimation(anime):
    """Checks if anime exists on Funimation website and returns a link"""
    try:
        exclude = set(string.punctuation)
        anime = ''.join(ch for ch in anime if ch not in exclude)
        keywords = anime.split(' ')
        funi_url = None
        while len(keywords) > 0:
            show_slug = '-'.join(keywords).lower()
            funi_url = f'https://www.funimation.com/shows/{show_slug}/'
            funi_url = utilities.make_get_request(funi_url)
            if funi_url is None:
                keywords.pop()
                continue
            else:
                break
    except:
        print('Funimation url couldn\'t be retrieved')
        return
    return funi_url.url if funi_url is not None else None


def search_animelab(anime):
    """Checks if anime title exists on AnimeLab website and returns a link"""
    try:
        keywords = anime.split(' ')
        animelab_url = None
        while len(keywords) > 0:
            show_slug = '-'.join(keywords).lower()
            animelab_url = f'https://www.animelab.com/shows/{show_slug}'
            animelab_url = utilities.make_get_request(animelab_url)
            if animelab_url is None:
                keywords.pop()
                return
            else:
                break
    except:
        print('Animelab url couldn\'t be retrieved')
        return
    return animelab_url.url


