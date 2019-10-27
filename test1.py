import os
import tweepy as tw
import pandas as pd
from textblob import TextBlob

consumer_key= 'sE75ErERpo003dZoFhRvvmXTW'
consumer_secret= 'bbEzDK8RWCWJyWrKorDolqePoL6jdFFdPZWjwR44FbYjib5LWV'
access_token= '255602049-DCTg1hRhNsNZsVpgL7VgFgw1Fh2JeUkhFoAXVf8Z'
access_token_secret= 'E5Hb9wDLJjf30x2U7nKZIDVqNELVpAhL2ES5PvSqLUIIP'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
tweet_dict = {}
good_tweets = []
bad_tweets = []
# Post a tweet from Python
#api.update_status("Look, I'm tweeting from #Python in my #earthanalytics class! LOL @EarthLabCU")
# Your tweet has been posted!
# Define the search term and the date_since date as variables
search_words = "jetblue -filter:retweets"
date_since = "2018-11-16"
# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(10)

def getSentimentOfWord(sentence):
    text = TextBlob(sentence)
    # print('Hi \n')
    return text.sentiment

def getPositiveComments():
    for tweet in good_tweets:
        filt = tweet.text.encode('ascii', 'ignore').decode('ascii')
        print(filt, tweet.user.location, tweet.created_at)

def getNegativeComments():
    for tweet in bad_tweets:
        filt = tweet.text.encode('ascii', 'ignore').decode('ascii')
        print(filt, tweet.user.location, tweet.created_at)

def calculateAverageSentiment():
    averagePolarity = 0
    for e in tweet_dict:
        # print(tweet_dict[e].polarity)
        averagePolarity += tweet_dict[e].polarity
    return averagePolarity/len(tweet_dict)

# Iterate and print tweets
for tweet in tweets:
    filtered = tweet.text.encode('ascii', 'ignore').decode('ascii')
    #if(tweet.username )
    #Tweet dict hash
    tweet_dict[tweet.text] = getSentimentOfWord(tweet.text)
    if(tweet_dict[tweet.text].polarity < 0):
            bad_tweets.append(tweet)
            #bad_tweets[tweet.text] = tweet_dict[tweet.text]//DELETE
    else:
            good_tweets.append(tweet)
            #good_tweets[tweet.text] = tweet_dict[tweet.text]//DELETE
            #tweet dict hash end
    if(tweet.user.screen_name == "JetBlue" or tweet.user.screen_name == "JetBlue Airways"):
        continue
    if("Here's another way #airlines are creating a calming atmosphere for a better #flight experience." in tweet.text):
        continue
    #print(filtered, tweet.user.screen_name)
getNegativeComments()
print(calculateAverageSentiment())
