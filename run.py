from time import sleep
from reddit import reddit_commands


def main():
    reddit = reddit_commands.authenticate()
    while True:
        try:
            print('Parsing')
            reddit_commands.parse_reddit_messages(reddit)
            sleep(5)
        except Exception as e:
            print(e)
            print('Trying again')
            sleep(5)


if __name__ == '__main__':
    main()