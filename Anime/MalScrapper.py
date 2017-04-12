import requests
import bs4
import sys
import re
from time import sleep


def get_anime_links(title):
    """
    Uses beautiful soup to enter anime into search bar and then extract links of anime pages from the search results
    :param title: 
    :return: 
    """
    search_url = "https://myanimelist.net/anime.php?q={}".format(title)
    print(search_url)
    try:
        res = requests.get(search_url)
        res.raise_for_status()
        print(res)
    except requests.exceptions.ConnectionError:
        print("No such link {} found, exiting program".format(search_url))
        sys.exit(1)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l")]
    print(links)
    return links


def get_anime_info(link):
    """
    Opens up a link to an anime page and then scrapes out all acompanying info
    :param link: 
    :return: 
    """
    try:
        res = requests.get(link)
        res.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Failed to connect to url")
        return
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    synopsis = soup.find(itemprop='description').get_text()
    print(synopsis)
    anime_info_dict = {'Type': soup.select("div > a")[15].text,
                       'Episodes': [int(s) for s in soup.select("div.spaceit")[0].text.split() if s.isdigit()][0],
                       'Status': soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                                         'Finished Airing'])))[
                           0].strip(),
                       'Aired': " ".join(soup.select("div.spaceit")[1].text.strip().split(" ")[2:]),
                       'Source': " ".join(soup.select("div.spaceit")[3].text if ("Source:" in soup.select(
                           "div.spaceit")[
                           3].text) else soup.select("div.spaceit")[4].text.strip().split(" ")[2:]),
                       'Genres': soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3] if (
                           "Source:" in
                           soup.select
                           ("div.spaceit")[3].text) else soup.select("div.spaceit")[4]) + 1].text.strip().split(
                           "\n")[1],
                       'Duration': [int(s) for s in (soup.select("div.spaceit")[4].text if ("Duration:" in soup.select(
                           "div.spaceit")[
                           4].text) else soup.select("div.spaceit")[5].text).split() if s.isdigit()][0]}
    """print(anime_info_dict['Type'])
    print(anime_info_dict['Episodes'])
    print(anime_info_dict['Status'])
    print(anime_info_dict['Aired'])
    print(anime_info_dict['Source'])
    print(anime_info_dict['Genres'])
    print(anime_info_dict['Duration'])"""


def main():
    # Retrieving title of anime
    while True:
        print("What show are you looking up: ")
        title = str(input()).split(" ")
        title = '_'.join(map(str, title))
        print("Searching for anime links on MAL...")
        anime_links = get_anime_links(title)
        print('First Link: ' + anime_links[0])
        get_anime_info(anime_links[0])
        sleep(5)


if __name__ == '__main__':
    main()
