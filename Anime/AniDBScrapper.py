import requests
from time import sleep
import sys
import datetime


def scrape_anidb():
    """
    Open up anidb dat file, containing anime titles and id's and writting them to a text file
    :return: 
    """

    anidb_request = None
    while anidb_request is None:
        try:
            anidb_request = requests.get("http://anidb.net/api/anime-titles.dat.gz")
            anidb_request.raise_for_status()
        except requests.exceptions.RequestException:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    print(anidb_request.text)
    with open('AniDBTitle.txt', 'w') as ani:
        ani.write(anidb_request.text)


def main():
    scrape_anidb()


if __name__ == '__main__':
    main()