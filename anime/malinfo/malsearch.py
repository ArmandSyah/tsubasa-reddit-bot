import requests
import bs4


def get_links_by_google_search(title):
    pass


def get_links_by_spice(title):
    pass


def get_links_by_brute_force(title):
    """
    Uses beautiful soup to enter anime into search bar and then extract links of anime pages from the search results
    :type title: str
    :return: Mal Search Links
    """

    title = "%20".join(title.split(" "))
    search_url = f"https://myanimelist.net/anime.php?q={title}"
    try:
        res = requests.get(search_url)
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Might have made too many requests here")
        return
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = [element.get("href") for element in soup.select("a.hoverinfo_trigger.fw-b.fl-l", limit=5)]
    return links
