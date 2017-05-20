from anime.mal import mal_search_methods
from anime.mal.mal_anime import MalAnime
from anime.anidb import anidb_search_methods as anidbsearch


def mal_object_test():
    jojo_mal = mal_search_methods.get_mal_links('Hinako Note')
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