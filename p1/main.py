from hadoop import *
from twitter import *

HADOOP_USER_FOLDER = '/user/gandrade'


def get_graph_points(keywords, since, until):
    Twitter.get_tweets(keywords, since, until)
    return Hadoop(HADOOP_USER_FOLDER).run('tweets.txt')


def main():
    keywords = []
    with open('keywords.txt') as f:
        keywords = [line.rstrip('\n') for line in f]
    since = '2016-08-27'
    until = '2017-08-27'
    points = get_graph_points(keywords, since, until)
    print(points)

if __name__ == '__main__':
    main()
