import os

from anime import utilities


def _scrape_anidb():
    """Open up anidb dat file, containing anime titles and id's and writting them to a text file"""

    if os.stat('AniDBTitles.txt').st_size > 0:
        print('No need to run this script again, let\'s limit the amount of requests')
        return
    anidb_request = utilities.make_get_request("http://anidb.net/api/anime-titles.dat.gz")
    with open('AniDBTitles.txt', 'w', encoding='utf8') as ani:
        ani.write(anidb_request.text)


def get_anidb_link(title):
    """Takes an anime title, and makes a link to the associated AniDB page"""
    try:
        animeid = _get_animeid(title)
    except KeyError:
        print('Either title was mispelled or does not exist')
        return
    return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={animeid}'


def _get_animeid(title):
    """Searches through AniDB Titles"""
    if 'AnimeMessengerRedditBot\\anime\\anidb' not in os.getcwd():
        _set_proper_path()
    print(os.getcwd())
    with open('AniDBTitles.txt', 'r', encoding='utf8') as ani:
        anidb_titles = ani.read()
        anidb_titles = anidb_titles.split("\n")
        anidb_titles = [t for t in anidb_titles if "|en|" in t or "|x-jat|" in t]
    english_anime_dict = {}
    for anime in anidb_titles:
        anime = anime.split("|")
        english_anime_dict[anime[3].lower()] = anime[0]
    return english_anime_dict[title.lower()]


def _set_proper_path():
    os.chdir('..\\anime\\anidb')