
#Variables that contains the user credentials to access Twitter API
access_token = '863967955251593216-1ROeE7oZt13sZT8HUBzVpTUW263V1vw'
access_token_secret = "lg1aKA2DEiUaG3exMZhBbSHjwUrep3NfAxX4pTlnSJZEe"
consumer_key = "6TakVUGxzdk3gWLrhy9Qi5PNG"
consumer_secret = "MwKYNv9DlsyqsDhUmc1wcZnSjyuDNcdNEyEqUdgsYkRIMlTWPB"

import tweepy
from datetime import timedelta



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

count = 0

for status in tweepy.Cursor(api.search,
                           q="racism immigrants",
                           count=100,
                           result_type='recent',
                           since='2017-08-12',
                           until='2017-08-14',
                           lang="en").items():
    count += 1

    # eastern_time = status.created_at - timedelta(hours=4)
    # edt_time = eastern_time.strftime('%Y-%m-%d %H:%M')
    #
    #
    print(status.text)
    #
    #
    # data ={}
    # data['name'] = status.user.name
    # data['screen_name'] = status.user.screen_name
    # data['location'] = status.user.location
    # data['text'] = status.text
    # data['created_at'] = edt_time
    # data['geo'] = status.coordinates
    # data['source'] = status.source

print(count)