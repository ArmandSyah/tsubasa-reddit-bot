from crunchyroll.apis.meta import MetaApi


def search_crunchyroll(anime):
    """Searches if anime exists on Crunchyroll and returns a link"""

    crunchy_api = MetaApi()
    crunchyroll_listing = list(crunchy_api.search_anime_series(anime))
    return crunchyroll_listing[0].url


def main():
    print(search_crunchyroll('Cowboy Bebop'))
    print(search_crunchyroll('Sword Art Online'))


if __name__ == '__main__':
    main()
