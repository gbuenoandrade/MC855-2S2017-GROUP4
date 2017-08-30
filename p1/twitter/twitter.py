from datetime import datetime, timedelta
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
        return min(1 + self.retweets + self.favorites, 50)


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
    def _get_tweets(keywords, since, until, max_num):
        criteria = got.manager.TweetCriteria().setQuerySearch(Twitter._build_query(keywords)).setLang('en')
        criteria.setMaxTweets(max_num)
        criteria.setSince(since)
        criteria.setUntil(until)
        simple_tweets = [SimpleTweet(t) for t in got.manager.TweetManager.getTweets(criteria)]
        return simple_tweets

    @staticmethod
    def _is_english(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    @staticmethod
    def get_tweets(keywords, since, until, points=5, tweets_per_point=5):
        cur = datetime.strptime(since, '%Y-%m-%d')
        until = datetime.strptime(until, '%Y-%m-%d')
        days = (until - cur).days
        frame = max(days/points, 1)
        with open('tweets.txt', 'w') as f:
            while cur <= until:
                x = str(cur.date())
                y = str((cur + timedelta(days=1)).date())
                tweets = Twitter._get_tweets(keywords, x, y, tweets_per_point)
                for tweet in tweets:
                    text = tweet.text.replace('…', '')
                    if Twitter._is_english(text):
                        entry = '%s %f %s\n' % (cur.date(), float(tweet.score()), text)
                        print(entry)
                        f.write(entry)
                cur += timedelta(days=frame)
