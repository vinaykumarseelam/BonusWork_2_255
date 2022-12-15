import tweepy
import time
import pandas as pd
pd.set_option('display.max_colwidth', 1000)

# api key
api_key = "GXiPV0P6hJenfSfOHwHi3qfAR"
# api secret key
api_secret_key = "AAGUf3AkwHHtICARCBuoirCnBtfPQEquGsQH7HVPOnPrq6Mu5G"
# access token
access_token = "1520529519374786560-ynmwaEA5FEelmUsO0Etcx89PEpnSKF"
# access token secret
access_token_secret = "2yNBlLypZEF1g4G6DM8S6bTHrvYHAhWWCOuLlwcDe20wq"

authentication = tweepy.OAuthHandler(api_key, api_secret_key)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)

def get_related_tweets(text_query):
    # list to store tweets
    tweets_list = []
    # no of tweets
    count = 20
    try:
        # Pulling individual tweets from query
        for tweet in api.search_tweets(q=text_query, count=count):
            print(tweet.text)
            # Adding to list that contains all tweets
            tweets_list.append({'created_at': tweet.created_at,
                                'tweet_id': tweet.id,
                                'tweet_text': tweet.text})
        return pd.DataFrame.from_dict(tweets_list)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)