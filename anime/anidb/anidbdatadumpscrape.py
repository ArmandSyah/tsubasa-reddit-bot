import os

from anime import utilities


def _scrape_anidb_data_dump():
    """
        Open up anidb dat file, containing anime titles and id's and writting them to a text file
        Do not run this module more than once a day
    """

    anidb_request = utilities.make_get_request("http://anidb.net/api/anime-titles.dat.gz")
    with open('AniDBTitles.txt', 'w', encoding='utf8') as ani:
        ani.write(anidb_request.text)


def _scrape_anidb_xml():
    """
        Open up AniDB's XML dump and copy it into our xml
        Do not run this module more than once a day
    """
    anidb_request = utilities.make_get_request("http://anidb.net/api/anime-titles.xml.gz")
    with open('AniDBTitlesXML.txt', 'w', encoding='utf8') as ani:
        ani.write(anidb_request.text)


def get_animeid(title):
    """Searches through AniDB Titles found in AniDBTitles.txt"""
    if 'AnimeMessengerRedditBot\\anime\\anidb' not in os.getcwd():
        print(os.getcwd())
    with open('AniDBTitles.txt', 'r', encoding='utf8') as ani:
        anidb_titles = ani.read()
        anidb_titles = anidb_titles.split("\n")
        anidb_titles = [t.lower() for t in anidb_titles if "|en|" in t or "|x-jat|" in t]
    anime_dict = {}
    for anime in anidb_titles:
        anime = anime.split("|")
        anime_dict[anime[3].lower()] = anime[0]
    return anime_dict[title.lower()]
