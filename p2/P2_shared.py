# Databricks notebook source
# MAGIC %md
# MAGIC # Mensurando potencial onda conservadora
# MAGIC ## via Twitter e Spark
# MAGIC ***
# MAGIC * Danilo Mendes
# MAGIC * Felipe Rodrigues
# MAGIC * Guilherme Andrade

# COMMAND ----------

# MAGIC %md
# MAGIC # Twitter - Nova abordagem
# MAGIC ***
# MAGIC * Rest API
# MAGIC     * Limitação temporal
# MAGIC * Spark RDD

# COMMAND ----------

import urllib
import requests
from requests_oauthlib import OAuth1
import datetime
from pyspark.sql import *

class SimpleTweet:
    def __init__(self, date, retweets, text, favorites):
        self.date = date
        self.retweets = retweets
        self.text = text
        self.favorites = favorites

    def __repr__(self):
        return '%d - %s' % (self.score(), self.text)

    def score(self):
        return min(1 + 2*self.retweets + self.favorites, 1000)
      
class Twitter:
    API_KEY = '6TakVUGxzdk3gWLrhy9Qi5PNG'
    API_SECRET = 'MwKYNv9DlsyqsDhUmc1wcZnSjyuDNcdNEyEqUdgsYkRIMlTWPB'
    ACCESS_TOKEN = '863967955251593216-1ROeE7oZt13sZT8HUBzVpTUW263V1vw'
    ACCESS_TOKEN_SECRET = 'lg1aKA2DEiUaG3exMZhBbSHjwUrep3NfAxX4pTlnSJZEe'
    BASE_URL = 'https://api.twitter.com/1.1/search/tweets.json'
    
    @staticmethod
    def _is_english(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    @staticmethod
    def get_tweets(query, until, count):
        f = {'q': query, 'count': 100, 'lang': 'en', 'until': until, 'result_type': 'recent'}
        params = urllib.urlencode(f)
        url = Twitter.BASE_URL + '?' + params
        tweets = []
        while url != '' and len(tweets) < count:
            try:
              auth = OAuth1(Twitter.API_KEY, Twitter.API_SECRET, Twitter.ACCESS_TOKEN, Twitter.ACCESS_TOKEN_SECRET)
              response = requests.get(url, auth=auth).json()
              data = response['statuses']
              meta = response['search_metadata']
              url = (Twitter.BASE_URL + meta['next_results']) if 'next_results' in meta else ''
              for entry in data:
                  text = entry['text'].encode('ascii', 'ignore').replace('…', '').replace('\n', '')
                  if Twitter._is_english(text):
                      tweet = SimpleTweet(entry['created_at'], entry['retweet_count'], text, entry['favorite_count'])
                      tweets.append(tweet)
            except Exception as e:
                print(e)
                break
        return tweets[:count]

    @staticmethod
    def get_twitter_rdd(query, since, until, count):
      cur = datetime.datetime.strptime(since, '%Y-%m-%d')
      until = datetime.datetime.strptime(until, '%Y-%m-%d')
      delta = datetime.timedelta(days=1)
      days = (until - cur + delta).days
      rows = []
      while cur <= until:
        tweets = Twitter.get_tweets(query, str(cur.date() + delta), max(int(count/days), 1))
        for tweet in tweets:
          rows.append(Row(timestamp=str(cur.date()), text=tweet.text, score=float(tweet.score())))
        cur += delta
      return sc.parallelize(rows)

# COMMAND ----------

# MAGIC %md
# MAGIC # Queries
# MAGIC ***
# MAGIC * Keywords
# MAGIC * Desde
# MAGIC * Até
# MAGIC * Número máximo de tweets

# COMMAND ----------

QUERY = 'muslims OR immigrants'
FROM = '2017-09-18'
TO = '2017-09-28'
N = 1000

twitter_rdd = Twitter.get_twitter_rdd(QUERY, FROM, TO, N)
display(twitter_rdd.toDF())

# COMMAND ----------

# MAGIC %md
# MAGIC # Setup do Classificador
# MAGIC ***
# MAGIC * Uso do classifier treinado na primeira parte

# COMMAND ----------

hdfs_words = requests.get('https://raw.githubusercontent.com/gbuenoandrade/MC855-2S2017-group4/master/p2/aux_files/words.txt').text.split()

hdfs_stop_words = requests.get('https://raw.githubusercontent.com/gbuenoandrade/MC855-2S2017-group4/master/p2/aux_files/stop_words.txt').text.split()

r = requests.get('https://github.com/gbuenoandrade/MC855-2S2017-group4/raw/master/p2/aux_files/classifier.pickle')
classifier_path = '/tmp/classifier.pickle'
with open(classifier_path, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024): 
        if chunk:
            f.write(chunk)
            
import nltk
nltk.download('punkt')

# COMMAND ----------

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import nltk
import pickle


class Analyzer:
    def __init__(self):
        self.st = PorterStemmer()
        self.stop_words = set(hdfs_stop_words)
        self._load()

    def _tokenize(self, text):
        raw_tokens = word_tokenize(text)
        tokens = []
        for token in raw_tokens:
            # removing stop words and simple punctuation
            if token not in self.stop_words and len(token) >= 2:
                tokens.append(self.st.stem(token.lower()))
        return tokens

    def _load(self):
      with open(classifier_path, 'rb') as f:
        self.classifier = pickle.load(f)

      self.words = set([line.rstrip('\n') for line in hdfs_words])

    def _get_features(self, tokens):
        features = {}
        for word in self.words:
            features[word] = word in tokens
        return features

    def classify(self, text):
        features = self._get_features(self._tokenize(text))
        ans = self.classifier.prob_classify(features)
        pos = ans._prob_dict['pos']
        neg = ans._prob_dict['neg']
        dist = abs(pos-neg)
        if dist > 0.25:
            return 1 if pos > neg else -1
        return 0

# COMMAND ----------

# MAGIC %md
# MAGIC # Spark
# MAGIC ***
# MAGIC * Ambiente do *Databricks* já configurado
# MAGIC * Integração 'natural' com *Python*
# MAGIC * Maior nível de abstração oferecido pelo *Apache Spark*
# MAGIC * Mapping step
# MAGIC     * Score com sinal

# COMMAND ----------

def signedScore(x):
  sign = analyzer.classify(x['text'])
  return Row(timestamp=x['timestamp'], text=x['text'], score=sign*x['score'])

analyzer = Analyzer()
signed_twitter_rdd = twitter_rdd.map(signedScore)
display(signed_twitter_rdd.toDF())

# COMMAND ----------

# MAGIC %md
# MAGIC # Spark
# MAGIC ***
# MAGIC * Reducing step
# MAGIC     * Acumulação de scores por dia

# COMMAND ----------

reduced = signed_twitter_rdd.map(lambda x: Row(key=x['timestamp'], score=x['score'])).reduceByKey(lambda accum, n: accum + n)
display(reduced.toDF())

# COMMAND ----------

# MAGIC %md
# MAGIC # Visualização dos resultados
# MAGIC ***
# MAGIC * Obtenção do acumulado geral
# MAGIC * Exibição de data frames
# MAGIC * Geração de gráficos

# COMMAND ----------

final = []
prev = 0
for idx, val in enumerate(sorted(reduced.collect())):
  final.append(Row(date=val[0], acc=val[1] + prev))
  prev += val[1]
final = sc.parallelize(final)
display(final.toDF())
