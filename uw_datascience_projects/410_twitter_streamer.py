# Import libraries
import json
import numpy as np
import pandas as pd
import sys
import csv
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('tweet_output.json','a') as json_file:
                all_data = unicode(json.loads(data), 'utf-8')
                json_file.write(data)
                # print(type(data)) ==> returns string type
                # csv_data = next(data) ==> returns error since 'str' cannot be subject to next() method
                # print(type(csv_data))
            # if 'text' in all_data:
            #     created = all_data["created_at"]
            #     short_text = all_data["text"]
            #     source = all_data["source"]
            #     screen_name = all_data["user"]["screen_name"]
            #     location = all_data["user"]["location"]
            #     description = all_data["user"]["description"]
            #     followers = all_data["user"]["followers_count"]
            #     listed = all_data["user"]["listed_count"]
            #     favourites = all_data["user"]["favourites_count"]
            #     statuses = all_data["user"]["statuses_count"]
            #     user_created = all_data["user"]["created_at"]
            #     #full_text = all_data["extended_tweet"]["full_text"]
            #     tweet_replies = all_data["reply_count"]
            #     tweet_retweets = all_data["retweet_count"]
            #     tweet_favourites = all_data["favorite_count"]
            # tweet = [created,short_text,source,screen_name,location,description,followers,listed,favourites,statuses,user_created,full_text,tweet_replies,tweet_retweets,tweet_favourites]
            # with open('tweet_output.csv', 'a', newline='') as csv_file:
            #     writer = csv.writer(csv_file)
            #     writer.writerow(tweet)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

# Import Twitter and assign secrets from csv file
def load_api():
    secrets = pd.read_csv('twitter_secrets.csv')
    consumer_key = secrets['consumer_key'][0]
    consumer_secret = secrets['consumer_secret'][0]
    token = secrets['access_token'][0]
    token_secret = secrets['access_secret'][0]
    twitter_oauth = OAuth(token, token_secret, consumer_key, consumer_secret)
    tweepy_oauth = OAuthHandler(consumer_key, consumer_secret)
    tweepy_oauth.set_access_token(token,token_secret)
    return twitter_oauth, tweepy_oauth

# Function to test twitter stream
def test_twitter_stream(oauth):
    try:
        twitter_stream = TwitterStream(auth=oauth)
        iterator = twitter_stream.statuses.sample()

        tweet_count = 1
        for tweet in iterator:
            tweet_count -= 1
            print(json.dumps(tweet))

            if tweet_count <= 0:
                break
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

# Function to test connectivity to my timeline
def test_my_timeline(oauth):
    try:
        t = Twitter(auth=oauth)
        timeline = t.statuses.home_timeline()
        print(timeline[0])
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

def test_btcusd_hashtag(oauth):
    t = Twitter(auth=oauth)
    btcusd_search = t.search.tweets(q='#btcusd', result_type='recent', lang='en', count=10)
    print(json.dumps(btcusd_search, indent=4))

def fetch_crypto_tweets(oauth):
    currency_list = ['#BTCUSD', '#ETHUSD', '#XRPUSD', '#BCHUSD', '#ADAUSD', '#LTCUSD', '#XLMUSD', '#XEMUSD', '#EOSUSD', '#NEOUSD']
    tweets = []
    t = Twitter(auth=oauth)

    for currency in currency_list:
        currency_tweets = t.search.tweets(q=currency, result_type='recent', lang='en', count=10)
        tweets.append(currency_tweets)

    return tweets

def crypto_stream(oauth):
    #api = tweepy.API(oauth)
    stream = Stream(oauth, MyListener())
    stream.filter(track=['BTCUSD', 'ETHUSD', 'XRPUSD', 'BCHUSD', 'ADAUSD', 'LTCUSD', 'XLMUSD', 'XEMUSD', 'EOSUSD', 'NEOUSD',\
                         '#BTCUSD', '#ETHUSD', '#XRPUSD', '#BCHUSD', '#ADAUSD', '#LTCUSD', '#XLMUSD', '#XEMUSD', '#EOSUSD', '#NEOUSD',\
                         'Bitcoin','Ethereum','Ripple','Litecoin','Cardano','Bitcoin Cash','NEO','Stellar','EOS','#btc'], languages=["en"])

if __name__ == "__main__":
    twitter_oauth, tweepy_oauth = load_api()
    #test_twitter_stream(twitter_oauth)
    #test_my_timeline(twitter_oauth)
    #test_btcusd_hashtag(twitter_oauth)
    #tweet_list = fetch_crypto_tweets(twitter_oauth)
    #print(json.dumps(tweet_list[0], indent=4))
    crypto_stream(tweepy_oauth)