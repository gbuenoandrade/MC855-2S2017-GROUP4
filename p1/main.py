from hadoop import *
from twitter import *


def get_tweets(since, until, max_num):
    keywords = []
    with open('keywords.txt') as f:
        keywords = [line.rstrip('\n') for line in f]
    return Twitter.get_tweets(keywords, since, until, max_num)

def main():
    tweets = get_tweets('2017-08-20', '2017-08-27', 10)
    for tweet in tweets:
        print(tweet)

if __name__ == '__main__':
    # print(Hadoop('/user/gandrade').run('input.txt'))
    main()
