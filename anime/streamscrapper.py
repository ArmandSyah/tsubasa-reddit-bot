import string
import requests

from crunchyroll.apis.meta import MetaApi


def search_crunchyroll(anime):
    """Searches if anime exists on Crunchyroll and returns a link"""

    crunchy_api = MetaApi()
    crunchyroll_listing = list(crunchy_api.search_anime_series(anime))
    return crunchyroll_listing[0].url


def search_funimation(anime):
    """Checks if anime exists on Funimation website"""
    exclude = set(string.punctuation)
    show_slug = ''.join(ch for ch in anime if ch not in exclude)
    show_slug = '-'.join(show_slug.split(" ")).lower()
    funi_url = f'https://www.funimation.com/shows/{show_slug}/'

    try:
        funi_test = requests.get(funi_url)
        funi_test.raise_for_status()
    except requests.exceptions.HTTPError:
        return 'Got a 404 error, looks like this wasn\'t a valid link'

    return funi_url


def main():
    print(search_crunchyroll('Cowboy Bebop'))
    print(search_crunchyroll('Sword Art Online'))
    print(search_funimation('Cowboy Bebop'))
    print(search_funimation('Sword Art Online'))
    print(search_funimation('My Hero Academia'))


if __name__ == '__main__':
    main()
