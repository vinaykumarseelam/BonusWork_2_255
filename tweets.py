import tweepy
from tweepy import OAuthHandler
import pandas as pd


class TwitterClient(object): 
    def __init__(self):
        # Access Credentials 
        consumer_key = 'GXiPV0P6hJenfSfOHwHi3qfAR'
        consumer_secret = 'AAGUf3AkwHHtICARCBuoirCnBtfPQEquGsQH7HVPOnPrq6Mu5G'
        access_token = '1520529519374786560-ynmwaEA5FEelmUsO0Etcx89PEpnSKF'
        access_token_secret = '2yNBlLypZEF1g4G6DM8S6bTHrvYHAhWWCOuLlwcDe20wq'
        # OAuthHandler object 
        auth = OAuthHandler(consumer_key, consumer_secret) 
        # set access token and secret 
        auth.set_access_token(access_token, access_token_secret) 
        # create tweepy API object to fetch tweets 
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
    
    
    # We are keeping cleaned tweets in a new column called 'tidy_tweets'
   

    # Function to fetch tweets
    def get_tweets(self, query, maxTweets = 100): 
        # empty list to store parsed tweets 
        tweets = [] 
        sinceId = None
        max_id = -1
        tweetCount = 0
        tweetsPerQry = 100
        
        while tweetCount < maxTweets:
            
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry)
                else:
                    new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry,
                                                since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry,
                                                max_id=str(max_id - 1))
                else:
                    new_tweets = self.api.search_tweets(q=query, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
                    
            for tweet in new_tweets:
                parsed_tweet = {} 
                parsed_tweet['tweets'] = tweet.text 

                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
                        
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id

            
        
        return pd.DataFrame(tweets)