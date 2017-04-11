import requests
import bs4
import sys


def get_anime_links(title):
    search_url = "https://myanimelist.net/anime.php?q={}".format(title)
    print(search_url)
    try:
        res = requests.get(search_url)
        res.raise_for_status()
        print(res)
    except requests.exceptions.ConnectionError as e:
        print("No such link {} found, exiting program".format(search_url))
        sys.exit(1)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    table_row_elems = soup.select("a.hoverinfo_trigger.fw-b.fl-l")
    links = [element.get("href") for element in table_row_elems]
    print(links)
    return links


def main():
    print("What show are you looking up: ")
    title = str(input()).split(" ")
    title = '_'.join(map(str, title))
    print("Searching for anime links on MAL...")
    anime_links = get_anime_links(title)
    print('First Link: ' + anime_links[0])


if __name__ == '__main__':
    main()