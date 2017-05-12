import requests
import re
from bs4 import BeautifulSoup


def scrape_synopsis(mal_url):
    soup = make_beatiful_soup(mal_url)
    scraped_synopsis = soup.find(itemprop='description').get_text()
    formatted_synopsis = " ".join(scraped_synopsis.split(" "))
    return formatted_synopsis


def scrape_names(mal_url):
    soup = make_beatiful_soup(mal_url)

    main_name = soup.select("h1.h1")[0].text
    english_name = soup.find_all(text=re.compile(r'^English.*'))[0]
    synonyms = soup.find_all(text=re.compile(r'^Synonyms.*'))[0] \
        if len(soup.find_all(text=re.compile(r'^Synonyms.*'))) > 0 else list()
    japanese_name = soup.find_all(text=re.compile(r'^Japanese.*'))[0]

    formatted_main_name = main_name.strip()
    formatted_english_name = (" ".join(english_name.string.parent.parent.text.strip().split(" ")[1:])
                              if len(english_name) > 0 else '')
    formatted_synonyms = (" ".join(synonyms.string.parent.parent.text.strip().split(" ")[1:])
                          if len(synonyms) > 0 else '').split(', ')
    formatted_japanese_name = (" ".join(japanese_name.string.parent.parent.text.strip().split(" ")[1:])
                               if len(japanese_name) > 0 else '')

    name_dict = {'Main': formatted_main_name,
                 'English': formatted_english_name,
                 'Synonyms': formatted_synonyms,
                 'Japanese': formatted_japanese_name}

    return name_dict


def scrape_anime_type(mal_url):
    soup = make_beatiful_soup(mal_url)
    anime_type = soup.select("div > a")[15].text
    return anime_type


def scrape_episodes(mal_url):
    soup = make_beatiful_soup(mal_url)
    episodes = soup.select("div.spaceit")[0].text
    formatted_episodes = episodes.split()
    return formatted_episodes


def scrape_status(mal_url):
    soup = make_beatiful_soup(mal_url)
    status = soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                     'Finished Airing',
                                                                     'Not yet aired'])))[0]
    formatted_status = status.strip()
    return formatted_status


def scrape_airdate(mal_url):
    soup = make_beatiful_soup(mal_url)
    airdate = soup.select("div.spaceit")[1].text
    formatted_airdate = " ".join(airdate.strip().split(" ")[2:])
    return formatted_airdate


def scrape_source(mal_url):
    soup = make_beatiful_soup(mal_url)
    source = soup.select("div.spaceit")[3].text.split() \
        if ("Source:" in soup.select("div.spaceit")[3].text) \
        else soup.select("div.spaceit")[4].text.split()
    formatted_source = " ".join(source).split(" ")[1]
    return formatted_source


def scrape_genres(mal_url):
    soup = make_beatiful_soup(mal_url)
    genres = soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3]
                                                         if ("Source:" in soup.select("div.spaceit")[3].text)
                                                         else soup.select("div.spaceit")[4]) + 1]
    formatted_genres = genres.text.strip().split("\n")[1]
    return formatted_genres


def scrape_duration(mal_url):
    soup = make_beatiful_soup(mal_url)
    duration = (soup.select("div.spaceit")[4].text.strip().split(" ")[2:]
                if ("Duration:" in soup.select("div.spaceit")[4].text)
                else soup.select("div.spaceit")[5].text.strip().split(" ")[2:])
    formatted_duration = " ".join(duration)
    return formatted_duration


def make_beatiful_soup(mal_url):
    """Create BeautifulSoup Object to parse HTML easily"""
    res = ''
    try:
        res = requests.get(mal_url)
        res.raise_for_status()
    except requests.exceptions.RequestException as request_error:
        print("Failed to connect to url")
        print(request_error)
    return BeautifulSoup(res.text, "html.parser")