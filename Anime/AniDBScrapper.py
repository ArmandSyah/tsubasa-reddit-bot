import requests
import pprint
import os


def scrape_anidb():
    """
    Open up anidb dat file, containing anime titles and id's and writting them to a text file
    :return: 
    """

    if os.stat('AniDBTitles.txt').st_size > 0:
        print('No need to run this script again, let\'s limit the amount of requests')
        return

    anidb_request = None
    while anidb_request is None:
        try:
            anidb_request = requests.get("http://anidb.net/api/anime-titles.dat.gz")
            anidb_request.raise_for_status()
        except requests.exceptions.RequestException:
            print('Didn\'t work')
            continue

    with open('AniDBTitles.txt', 'w', encoding='utf8') as ani:
        ani.write(anidb_request.text)


def search_titles():
    """Searches through AniDB Titles"""
    with open('AniDBTitles.txt', 'r', encoding='utf8') as ani:
        anidb_titles = ani.read()
        anidb_titles = anidb_titles.split("\n")
        anidb_titles = [t for t in anidb_titles if "|en|" in t]
    pprint.pprint(anidb_titles)


def main():
    scrape_anidb()
    search_titles()


if __name__ == '__main__':
    main()