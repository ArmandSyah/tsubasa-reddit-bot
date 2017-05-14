from anime.mal import malsearchmethods
from anime.mal.malanime import MalAnime
from anime.anidb import anidbsearchmethods as anidbsearch


def mal_object_test():
    jojo_mal = malsearchmethods._get_mal_links_by_google_search('Hinako Note')
    jojo = MalAnime(jojo_mal)
    print(f"Main Name: {jojo.main_name}")
    print(f"English Name: {jojo.english_name}")
    print(f"Japanese Name: {jojo.japanese_name}")
    print(f"Synonyms: {jojo.synonyms}")
    print(f"Synopsis: {jojo.synopsis}")
    print(f"Genres: {jojo.genres}")
    print(f"Airdate: {jojo.airdate}")
    print(f"Rating: {jojo.rating}/10")


def anidb_link_test():
    anidb_link = anidbsearch.get_anidb_links('Hinako Note')
    print(anidb_link)


def main():
    mal_object_test()
    anidb_link_test()


if __name__ == '__main__':
    main()