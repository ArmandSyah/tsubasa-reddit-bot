import requests
from bs4 import BeautifulSoup


def make_post_request(url, query_parameters=None):
    """Makes an HTTP Post Request and returns page data"""
    try:
        post_data = requests.post(url, data=query_parameters)
        post_data.raise_for_status()
    except requests.exceptions.RequestException:
        print("Failed to make the post request, returning")
        return
    return post_data


def make_get_request(url, credentials=None):
    """Makes an HTTP Get Request and returns page data"""
    try:
        get_data = requests.get(url, auth=credentials)
        get_data.raise_for_status()
    except requests.exceptions.RequestException:
        print("Failed to make the last Request")
        return
    return get_data


def make_beatiful_soup_url(url, parser="html.parser"):
    """Create BeautifulSoup Object to parse HTML/XML easily when passing in a url"""
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequestException:
        print("Failed to connect to url")
        return
    return BeautifulSoup(res.text, parser)


def make_beautful_soup_doc(doc, parser="lxml"):
    """Create BeautifulSoup Object to parse HTML/XML easily, when passing in a text doc of some form"""
    return BeautifulSoup(doc, parser)

