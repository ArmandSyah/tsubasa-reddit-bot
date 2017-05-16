import praw
import time
import os
import requests


def authenticate():
    """
    Logs into reddit, using credentials from praw.ini file
    :return: Instance of Reddit
    """
    print('Authenticating')
    reddit = praw.Reddit('tsubasa_reddit_bot', user_agent='TsubasaBot (by /u/kwespell')
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit