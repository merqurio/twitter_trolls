from bot import periodicity_answer
from spammer import tweet_iteration_stemming, tweet_iteration_hashtags
from transactions import data_user
from stalker import stalker
import tweepy
import numpy as np
from drama_queen import drama_queen

consumer_key = "iaAqgOyzLb2qbTsjOZXoZpbIB"
consumer_secret = "QZrExTZsMeqykJpw0EogLH5uEiOqj0bJquy5rJEQhehrlCBTAY"
access_key = "155609363-VOaTTLbdRZKkgRSnHmu30ht9pLY9VJ0ArZZOy2uD"
access_secret = "AycYj44tusCbzLZgyW6hENvIe6kXbKujluGXw1kpsEfJ6"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def percentage_drama_queen(activity, percentage_tweet_with_omg, capitals_per_char, signs_per_char, percentage_tweet_with_hashtag, percentage_tweet_with_mention, mentions_per_tweet, hashtags_per_tweet):
    activity_average = 10
    capitals_per_char_average = 11.13
    signs_per_char_average = 3.002
    percentage_tweet_with_omg_average = 0.00259
    percentage_tweet_with_mention_average = 0.5950
    percentage_tweet_with_hashtag_average = 0.1758
    mentions_per_tweet_average = 0.7953
    hashtags_per_tweet_average = 0.3431

    activity -= activity_average
    if activity > 40:
        activity = 40
    capitals_per_char -= capitals_per_char_average
    signs_per_char -= signs_per_char_average
    percentage_tweet_with_omg -= percentage_tweet_with_omg_average
    percentage_tweet_with_hashtag -= percentage_tweet_with_hashtag_average
    percentage_tweet_with_mention -= percentage_tweet_with_mention_average
    mentions_per_tweet -= mentions_per_tweet_average
    if mentions_per_tweet > 5:
        mentions_per_tweet = 5
    hashtags_per_tweet -= hashtags_per_tweet_average
    if hashtags_per_tweet > 5:
        hashtags_per_tweet = 5
    result = max(activity, 1)**1.15 + 12 * max(np.exp(percentage_tweet_with_omg)-1, 0) + np.sqrt(max(capitals_per_char,
            0)) + 2 * np.sqrt(max(signs_per_char, 0))+0.5 * np.sqrt(100 * max(percentage_tweet_with_hashtag, 0))+0.5 * \
            np.sqrt(100 * max(percentage_tweet_with_mention, 0)) + max(hashtags_per_tweet, 0)**1.5 + \
             max(mentions_per_tweet, 0)**1.5

    normalizer = 40**1.15 + 12 * np.exp(1-percentage_tweet_with_omg_average)-1 + np.sqrt(100-capitals_per_char_average) \
                 + 2 * np.sqrt(100-signs_per_char_average)+0.5 * np.sqrt(100 * (1-percentage_tweet_with_hashtag_average)
                )+0.5 * np.sqrt(100 * (1-percentage_tweet_with_mention_average)) + (5-hashtags_per_tweet_average)**1.5 + \
                 (5-mentions_per_tweet_average)**1.5

    return float(result)/normalizer*100


def percentage_bot(periodicity, answer, diversity_tweets):
    if max(periodicity, answer, (1-diversity_tweets)) > 95:
        return max(periodicity, answer, (1-diversity_tweets)*100)
    periodic_bot = float(6*periodicity+400*(1-diversity_tweets))/10
    repetitive_bot = float(6*answer+400*(1-diversity_tweets))/10
    if periodic_bot > repetitive_bot:
        result = periodic_bot
    else:
        result = repetitive_bot
    return result


def percentage_stalker(num_stalker, who_stalker, mentions_per_tweet, percentage_tweet_with_mention):
    famous = 0
    if num_stalker > 50:
        if data_user(str(who_stalker), api)["user_json"]["verified"] == "True":
            famous = 1
        if num_stalker > 85:
            result = num_stalker
        else:
            result = (6*num_stalker+3*100*percentage_tweet_with_mention-1*100*mentions_per_tweet)/10
    else:
        result = 0

    return result, famous


def run(user):
    try:
        user_data = data_user(user, api)
    except tweepy.TweepError:
        print "This user is protected. His  information cannot be accessed"
    else:
        if user_data["user_json"]["verified"] == "True":
            print "This user has a verified account. Therefore it is not a troll or bot"
            return 0
        if len(user_data["tweets"]) == 0:
            print "There is not enough information to classify this user"
            return 0
        hashtags_per_tweet = float(user_data["number_hashtags"]) / len(user_data["tweets"])
        mentions_per_tweet = float(user_data["number_mentions"]) / len(user_data["tweets"])
        percentage_tweet_with_mention = float(user_data["tweet_with_mentions"]) / len(user_data["tweets"])
        percentage_tweet_with_hashtag = float(user_data["tweets_with_hashtags"]) / len(user_data["tweets"])
        signs_per_char, capitals_per_char, activity, percentage_tweet_with_omg = drama_queen(user_data)
        periodicity, answer = periodicity_answer(user_data)
        diversity_hashtags = tweet_iteration_hashtags(user_data)
        diversity_tweets = tweet_iteration_stemming(user_data)
        num_stalker, who_stalker = stalker(user_data)
        per_drama_queen = percentage_drama_queen(activity, percentage_tweet_with_omg, capitals_per_char, signs_per_char,
                                                 percentage_tweet_with_hashtag, percentage_tweet_with_mention,
                                                 mentions_per_tweet, hashtags_per_tweet)
        per_bot = percentage_bot(periodicity, answer, diversity_tweets)
        per_stalker, famous = percentage_stalker(num_stalker, who_stalker, mentions_per_tweet, percentage_tweet_with_mention)
        print per_drama_queen, per_bot, per_stalker
