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
tweetWeight = {}
tweetTimes = {}
amountDelay = 0
t4hourArray = []
badService = 0
problems = {
    "delays": 0,
    "bad air service": 0,
    "staff problems": 0
}
good_things = {
    "Service": 0,
    "Time": 0
}
other = 0

for i in range(25):
    t4hourArray.append(0)


def calculateAverageSentiment():
    averagePolarity = 0
    for e in tweet_dict:
        # print(tweet_dict[e].polarity)
        averagePolarity += tweet_dict[e].polarity
    return averagePolarity/len(tweet_dict)

# Function just retrives the sentiments


def printPositive():
    for e in good_tweets:
        print(e)


def getGoodLocation():
    # for e in location_array:
    print("sd")


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
    # if(pr)
    print("With", problems[hypothesis], "cases",
          hypothesis, " is the worst problem JetBlue has")
    if(averagePolarity > 0.1):
        sen = "positive"
    else:
        sen = "negative"
    print("JetBlue Has a ", sen, "sentiment among twitter users today")
    print("Here is the worst Tweet we detected \n", getWorstTweet())
    print(problems)


def createHypothesis():
    # essentially a get max function lol
    worst_problem = "delays"
    best_aspect = ""
    for element in problems:
        if(problems[worst_problem] < problems[element]):
            worst_problem = element

    return worst_problem


def classifyBad():

    worst_negetive_sentiment = 1
    for e in bad_tweets:
        if(bad_tweets[e].polarity > worst_negetive_sentiment):
            # worstTweet = e
            worst_negetive_sentiment = bad_tweets[e]
        if("delayed" or "delay" or "not fixed" or "stranded" or "stuck" in e):
            # amountDelay = amountDelay + 1
            problems["delays"] = problems["delays"] + 1

        if("attendant" or "pilot" or "food" in e):
            # badService = badService + 1
            problems["bad air service"] = problems["bad air service"] + 1
        if ("staff" or "airport" in e):
            problems["staff problems"] = problems["staff problems"] + 1
        else:
            other = other + 1


def classifyGood():

    best_sentiment = -1
    for e in good_tweets:
        if(good_tweets[e].polarity > best_sentiment):
            # worstTweet = e
            best_sentiment = good_tweets[e]
        if("on time" or "fast" or "quick" or "good" in e):
            # amountDelay = amountDelay + 1
            good_things["Time"] = good_things["Time"] + 1

        if("attendant" or "pilot" or "food" in e):
            # badService = badService + 1
            problems["Service"] = good_things["Service"] + 1
        else:
            other = other + 1


def getSentimentOfWord(sentence):
    text = TextBlob(sentence)
    # print('Hi \n')
    # print(text.sentiment.polarity)
    return text.sentiment


def addNegetive(tweets):
    for i in tweets:
        hours = i.timestamp.hour
        if(i.text in bad_tweets):
            t4hourArray[hours] = t4hourArray[hours] + 1
    max = 0
    for i in range(24):
        if(t4hourArray[max] < t4hourArray[i]):
            max = i
    return max


def mostHappy(tweets):
    for i in tweets:
        hours = i.timestamp.hour
        if(i.text in good_tweets):
            t4hourArray[hours] = t4hourArray[hours] + 1
    max = 0
    for i in range(25):
        t4hourArray.append(0)

    for i in range(24):
        if(t4hourArray[max] < t4hourArray[i]):
            max = i
    return max


def main():
    # meow = "JetBlue is definitely my favorite always treat me right "
    # print(meow)
    # getSentimentOfWord(meow)
    tweetArray = query_tweets(
        "jetblue", begindate=begin_date, enddate=end_date, limit=100)
    for tweet in tweetArray:

       # tweetTimes[tweet.name] = tweet.datetime
       # dateArray = (tweet.timestamp).split("-")
       # desired_array = [int(numeric_string) for numeric_string in dateArray]
       # tweet_date = dt.datetime(
       #     desired_array[0], desired_array[1], desired_array[2], desired_array[3], desired_array[5])  # on date

        if(tweet.username == "JetBlue"):
            continue
        tweet_dict[tweet.text] = getSentimentOfWord(tweet.text)
        if(tweet.likes < 5000):
            tweetWeight[tweet.text] = ((tweet.likes)/5000)
        else:
            tweetWeight[tweet.text] = 5000

        if(tweet_dict[tweet.text].polarity < 0):
            bad_tweets[tweet.text] = tweet_dict[tweet.text]
        else:
            good_tweets[tweet.text] = tweet_dict[tweet.text]

    averagePolarity = calculateAverageSentiment()
    classifyBad()
    # classifyGood()
    hypothesis = createHypothesis()
    printOutput(hypothesis, averagePolarity)
    print("Number of negative tweets", len(bad_tweets), "\n")
    print("Number of positive tweets", len(good_tweets), "\n")

    print("Customers are most unhappy during the",
          addNegetive(tweetArray), "hour")
    # print("Customers are most happy during the",
    #       mostHappy(tweetArray), "hour")
    # printPositive()
    # print the sentiments


main()
