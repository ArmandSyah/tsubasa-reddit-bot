from anime import mal


def main():
    title = 'Food Wars'
    food_wars_mal = mal.malsearchmethods(title)
    food_wars = MalAnime(food_wars_mal)
    print(food_wars.genres)
    print(food_wars.names)
    print(food_wars.episodes)
    print(food_wars.status)


if __name__ == '__main__':
    main()
