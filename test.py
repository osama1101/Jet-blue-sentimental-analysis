import re
from textblob import TextBlob
from twitterscraper import query_tweets
import tweepy
import datetime as dt
import matplotlib.pyplot as plt

# Game plan
begin_date = dt.date(2019, 10, 24)
end_date = dt.date(2019, 10, 26)
tweet_dict = {}
good_tweets = {}
bad_tweets = {}
major_problem = {}
worstTweet = ""
amountDelay = 0
badService = 0
problems = {
    "amountDelay": 0,
    "badService": 0
}
other = 0


def calculateAverageSentiment():
    averagePolarity = 0
    for e in tweet_dict:
        # print(tweet_dict[e].polarity)
        averagePolarity += tweet_dict[e].polarity
    return averagePolarity/len(tweet_dict)

# Function just retrives the sentiments


def getWorstTweet():
    w_Sent = 1
    w_Tweet = ""
    for e in bad_tweets:
        if(w_Sent > bad_tweets[e].polarity):
            w_Tweet = e
            w_Sent = bad_tweets[e].polarity
    return w_Tweet


def printOutput(hypothesis, averagePolarity):
    sen = "nuetral"
    print("With ", problems[hypothesis], " cases ",
          hypothesis, " is the worst problem JetBlue has")
    if(averagePolarity > 0.1):
        sen = "positive"
    else:
        sen = "negative"
    print("JetBlue Has a ", sen, " sentiment among twitter users today")
    print("Here is the worst Tweet we detected \n", getWorstTweet())


def createHypothesis():
    # essentially a get max function lol
    worst_problem = "amountDelay"
    for element in problems:
        if(problems[worst_problem] < problems[element]):
            worst_problem = element

    return worst_problem


def classifyBad():

    worst_negetive_sentiment = 1
    for e in bad_tweets:
        if(bad_tweets[e].polarity > worst_negetive_sentiment):
            #worstTweet = e
            worst_negetive_sentiment = bad_tweets[e]
        if("delayed" or "delay" or "not fixed" in e):
            #amountDelay = amountDelay + 1
            problems["amountDelay"] = problems["amountDelay"] + 1

        elif("attendant" or "pilot" in e):
            #badService = badService + 1
            problems["badService"] = problems["badService"] + 1
        else:
            other = other + 1


def getSentimentOfWord(sentence):
    text = TextBlob(sentence)
    # print('Hi \n')
    # print(text.sentiment.polarity)
    return text.sentiment


def main():
    # meow = "JetBlue is definitely my favorite always treat me right "
    # print(meow)
    # getSentimentOfWord(meow)
    for tweet in query_tweets("jetblue", begindate=begin_date, enddate=end_date, limit=10):
        # print(tweet.text)
        if(tweet.username == "JetBlue"):
            continue
        tweet_dict[tweet.text] = getSentimentOfWord(tweet.text)
        if(tweet_dict[tweet.text].polarity < 0):
            bad_tweets[tweet.text] = tweet_dict[tweet.text]
        else:
            good_tweets[tweet.text] = tweet_dict[tweet.text]

    averagePolarity = calculateAverageSentiment()
    classifyBad()
    hypothesis = createHypothesis()
    printOutput(hypothesis, averagePolarity)

    # print the sentiments


main()
