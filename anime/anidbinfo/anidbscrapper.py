import requests
import os


def scrape_anidb():
    """Open up anidb dat file, containing anime titles and id's and writting them to a text file"""

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


def _get_animeid(title):
    """Searches through AniDB Titles"""
    with open('AniDBTitles.txt', 'r', encoding='utf8') as ani:
        anidb_titles = ani.read()
        anidb_titles = anidb_titles.split("\n")
        anidb_titles = [t for t in anidb_titles if "|en|" in t]
    english_anime_dict = {}
    for anime in anidb_titles:
        anime = anime.split("|")
        english_anime_dict[anime[3]] = anime[0]
    return english_anime_dict[title]


def get_anidb_link(title):
    """Takes an anime title, and makes a link to the associated AniDB page"""
    try:
        animeid = _get_animeid(title)
    except KeyError:
        print('Either title was mispelled or does not exist')
        return
    return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={animeid}'


def main():
    scrape_anidb()
    print(get_anidb_link('Nanbaka (2017)'))
    print(get_anidb_link('Attack on Titan'))


if __name__ == '__main__':
    main()