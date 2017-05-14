from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime
from anime.anidb import anidbsearchmethods as anidbsearch


def mal_object_test():
    food_wars_mal = malsearchmethods.get_links('Food Wars')
    food_wars = MalAnime(food_wars_mal)
    steins_gate_mal = malsearchmethods.get_links('steins;gate')
    steins_gate = MalAnime(steins_gate_mal)
    print(food_wars.synopsis)
    print(steins_gate.genres)


def anidb_link_test():
    anidb_link = anidbsearch.get_anidb_by_google_search('Hinako Note')
    print(anidb_link)


def main():
    # mal_object_test()
    anidb_link_test()


if __name__ == '__main__':
    main()