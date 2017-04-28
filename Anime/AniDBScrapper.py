import requests
import os


def scrape_anidb():
    """
    Open up anidb dat file, containing anime titles and id's and writting them to a text file
    :return: 
    """

    if os.stat('AniDBTitle.txt').st_size > 0:
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

    with open('AniDBTitle.txt', 'w', encoding='utf8') as ani:
        ani.write(anidb_request.text)


def main():
    scrape_anidb()


if __name__ == '__main__':
    main()