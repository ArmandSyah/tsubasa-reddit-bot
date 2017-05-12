from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime


def mal_object_test():
    food_wars_mal = malsearchmethods.get_links_by_spice('Food Wars')
    food_wars = MalAnime(food_wars_mal)
    steins_gate_mal = malsearchmethods.get_links_by_mal_api('steins;gate')
    steins_gate = MalAnime(steins_gate_mal)
    print(food_wars.synopsis)
    print(steins_gate.synopsis)
    print(steins_gate.genres)


def main():
    mal_object_test()


if __name__ == '__main__':
    main()