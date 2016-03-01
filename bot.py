from dateutil import parser
import pandas as pd


def list_tweets(user):
    tweet_time = []
    answer = 0
    for tweet in user["tweets"]:
        tweet_time.append(parser.parse(tweet["created_at"]))
        if tweet["in_reply_to_status_id"]:
            answer += 1
    return tweet_time, answer*100.0/len(tweet_time)


def distance_tweets(tweet_time):
    distance_tweet_time = []
    for x in range(1, len(tweet_time),1):
        distance = (tweet_time[x-1]-tweet_time[x]).total_seconds()
        distance_tweet_time.append(distance)
    return distance_tweet_time


def periodicity_answer(user):
    """ Gives the percentage of tweets that are answers of another tweet and a parameter that gives a relation
    of the periodicity of them.

    :param user: the twitter @username data
    :type user: dict

    .:return: periodicity (1 periodic, 0 random), percentage of answers
    :rtype: float, float
    """
    tweet_time, answer = list_tweets(user)
    distance_tweet_time = distance_tweets(tweet_time)
    distance_panda = pd.Series(distance_tweet_time)
    inside = 0
    for distance in distance_tweet_time:
        if abs(distance-distance_panda.median()) < 0.10*distance_panda.median():
            inside += 1
    result = float(inside)/len(distance_tweet_time)*100
    return result, answer
