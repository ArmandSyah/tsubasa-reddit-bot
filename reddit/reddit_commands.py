import praw
import os
from time import sleep

from reddit import message


def authenticate():
    """
    Logs into reddit, using credentials from praw.ini file
    :return: Instance of Reddit
    """
    print('Authenticating')
    reddit = praw.Reddit('TsubasaRedditBot')
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def parse_reddit_messages(reddit):
    """Sifts through all reddit messages in inbox and replies to the ones marked unread"""
    for item in reddit.inbox.unread(limit=None):
        item.mark_read()
        comment_body = item.body
        search_title = _parse_message(comment_body)
        if search_title is None:
            continue
        message_reply = message.make_message(search_title)
        item.reply(message_reply)
    return


def _parse_message(comment_body):
    if not comment_body.startswith('>'):
        return
    search_title = comment_body.split(' ')
    first_word = search_title.pop(0).translate({ord('>'): None})
    search_title.insert(0, first_word)
    return ' '.join(search_title).strip()


def main():
    reddit = authenticate()
    while True:
        try:
            print('Parsing')
            parse_reddit_messages(reddit)
        except:
            print('Trying again')
            sleep(5)

if __name__ == '__main__':
    os.chdir('\\'.join(os.getcwd().split('\\')[:-1]))
    main()