from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime
from anime.anidb import anidbsearchmethods as anidbsearch


def mal_object_test():
    jojo_mal = malsearchmethods._get_mal_links_by_google_search('Hinako Note')
    jojo = MalAnime(jojo_mal)
    print(f"Synopsis: {jojo.synopsis}")


def anidb_link_test():
    anidb_link = anidbsearch.get_anidb_links('Hinako Note')
    print(anidb_link)


def main():
    mal_object_test()
    anidb_link_test()


if __name__ == '__main__':
    main()