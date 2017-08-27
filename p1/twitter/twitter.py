import sys
if sys.version_info[0] < 3:
    import twitter.got
else:
    import twitter.got3 as got


class SimpleTweet:
    def __init__(self, tweet):
        self.date = tweet.date
        self.retweets = tweet.retweets
        self.text = tweet.text
        self.link = tweet.permalink
        self.favorites = tweet.favorites

    def __repr__(self):
        return '%d - %s' % (self.score(), self.text)

    def score(self):
        return 1 + self.retweets + self.favorites  # TODO improve this


class Twitter:
    @staticmethod
    def _build_query(keywords):
        query = ''
        for word in keywords:
            if query != '':
                query += ' OR '
            query += word
        return query + ' -porn'

    @staticmethod
    def get_tweets(keywords, since, until, max_num):
        criteria = got.manager.TweetCriteria().setQuerySearch(Twitter._build_query(keywords)).setLang('en')
        criteria.setMaxTweets(max_num)
        criteria.setSince(since)
        criteria.setUntil(until)
        simple_tweets = [SimpleTweet(t) for t in got.manager.TweetManager.getTweets(criteria)]
        return simple_tweets
