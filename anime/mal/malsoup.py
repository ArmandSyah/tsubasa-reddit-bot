import re


def scrape_synopsis(soup):
    scraped_synopsis = soup.find(itemprop='description').get_text()
    formatted_synopsis = scraped_synopsis.strip()
    return formatted_synopsis


def scrape_main_name(soup):
    main_name = soup.select("h1.h1")[0].text
    formatted_main_name = main_name.strip()
    return formatted_main_name


def scrape_english_name(soup):
    english_name = soup.find_all(text=re.compile(r'^English.*'))[0]
    formatted_english_name = (" ".join(english_name.string.parent.parent.text.strip().split(" ")[1:])
                              if len(english_name) > 0 else '')
    return formatted_english_name


def scrape_japanese_name(soup):
    japanese_name = soup.find_all(text=re.compile(r'^Japanese.*'))[0]
    formatted_japanese_name = (" ".join(japanese_name.string.parent.parent.text.strip().split(" ")[1:])
                               if len(japanese_name) > 0 else '')
    return formatted_japanese_name


def scrape_synonyms(soup):
    synonyms = (soup.find_all(text=re.compile(r'^Synonyms.*'))[0]
                if len(soup.find_all(text=re.compile(r'^Synonyms.*'))) > 0 else list())
    formatted_synonyms = (" ".join(synonyms.string.parent.parent.text.strip().split(" ")[1:])
                          if len(synonyms) > 0 else '').split(', ')
    return formatted_synonyms


def scrape_anime_type(soup):
    anime_type = soup.select("div > a")[15].text
    return anime_type


def scrape_episodes(soup):
    episodes = soup.select("div.spaceit")[0].text
    formatted_episodes = episodes.split()[1]
    return formatted_episodes


def scrape_status(soup):
    status = soup.find_all(text=re.compile(r'\b(?:%s)\b' % '|'.join(['Currently Airing',
                                                                     'Finished Airing',
                                                                     'Not yet aired'])))[0]
    formatted_status = status.strip()
    return formatted_status


def scrape_airdate(soup):
    airdate = soup.select("div.spaceit")[1].text
    formatted_airdate = " ".join(airdate.strip().split(" ")[2:])
    return formatted_airdate


def scrape_source(soup):
    source = (soup.select("div.spaceit")[3].text.split()
              if ("Source:" in soup.select("div.spaceit")[3].text)
              else soup.select("div.spaceit")[4].text.split())
    formatted_source = " ".join(source).split(" ")[1]
    return formatted_source


def scrape_genres(soup):
    genres = soup.select("div")[soup.select("div").index(soup.select("div.spaceit")[3]
                                                         if ("Source:" in soup.select("div.spaceit")[3].text)
                                                         else soup.select("div.spaceit")[4]) + 1]
    formatted_genres = genres.text.strip().split("\n")[1]
    formatted_genres = [g.strip() for g in formatted_genres.split(',')]
    return formatted_genres


def scrape_duration(soup):
    duration = (soup.select("div.spaceit")[4].text
                if ("Duration:" in soup.select("div.spaceit")[4].text)
                else soup.select("div.spaceit")[5].text)
    formatted_duration = " ".join(duration.strip().split(" ")[2:])
    return formatted_duration


def scrape_rating(soup):
    rating = soup.select("div.fl-l.score")[0].text
    formatted_rating = rating.strip()
    return formatted_rating