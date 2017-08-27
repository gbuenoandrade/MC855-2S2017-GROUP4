from hadoop import *
from twitter import *
from analyzer import *

def get_tweets(since, until, max_num):
    keywords = []
    with open('keywords.txt') as f:
        keywords = [line.rstrip('\n') for line in f]
    return Twitter.get_tweets(keywords, since, until, max_num)

def main():
    # print(Hadoop('/user/gandrade').run('input.txt'))

    # tweets = get_tweets('2017-08-20', '2017-08-27', 10)
    # for tweet in tweets:
    #     print(tweet)

    PROJECT = '/Users/gandrade/Desktop/MC855-2S2017-group4/p1'
    analyzer = Analyzer(PROJECT)
    print(analyzer.classify('it was amazing'))
    print(analyzer.classify('it was impressive'))
    print(analyzer.classify('I hated it'))
    print(analyzer.classify('almost killed myself'))
    print(analyzer.classify('yes'))
    print(analyzer.classify('water'))

if __name__ == '__main__':
    main()
