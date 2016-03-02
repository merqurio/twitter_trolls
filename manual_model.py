import logging
import numpy as np
import tweepy
from bot import periodicity_answer
from spammer import tweet_iteration_stemming, tweet_iteration_hashtags, tweet_iteration_urls
from transactions import data_user
from stalker import stalker
from keys import STREAM
from haters import sentiment
from logging.config import fileConfig
from drama_queen import drama_queen

fileConfig('logging_config.ini', disable_existing_loggers=False)

auth = tweepy.OAuthHandler(STREAM["consumer_key"], STREAM["consumer_secret"])
auth.set_access_token(STREAM["access_key"], STREAM["access_secret"])
api = tweepy.API(auth)


def percentage_drama_queen(activity, percentage_tweet_with_omg, capitals_per_char, signs_per_char, percentage_tweet_with_hashtag, percentage_tweet_with_mention, mentions_per_tweet, hashtags_per_tweet):
    activity_average = 8
    capitals_per_char_average = 0.1113
    signs_per_char_average = 0.03002
    percentage_tweet_with_omg_average = 0.1196
    percentage_tweet_with_mention_average = 0.5950
    percentage_tweet_with_hashtag_average = 0.1758
    mentions_per_tweet_average = 0.7953
    hashtags_per_tweet_average = 0.3431
    compt1 = 0
    compt2 = 0

    activity -= activity_average
    if activity > 20:
        activity = 20
    capitals_per_char -= capitals_per_char_average
    signs_per_char -= signs_per_char_average
    percentage_tweet_with_omg -= percentage_tweet_with_omg_average
    percentage_tweet_with_hashtag -= percentage_tweet_with_hashtag_average
    percentage_tweet_with_mention -= percentage_tweet_with_mention_average
    mentions_per_tweet /= mentions_per_tweet_average
    hashtags_per_tweet /= hashtags_per_tweet_average

    if mentions_per_tweet > 5:
        mentions_per_tweet = 5
    if hashtags_per_tweet > 5:
        hashtags_per_tweet = 5
    if activity > 0:
        compt1 += 1
    if capitals_per_char > 0:
        compt1 += 1
    if signs_per_char > 0:
        compt1 += 1
    if percentage_tweet_with_omg > 0:
        compt1 += 1
    if percentage_tweet_with_hashtag > 0:
        compt2 += 1
    if percentage_tweet_with_mention > 0:
        compt2 += 1
    if mentions_per_tweet > 1:
        compt2 += 1
    if hashtags_per_tweet > 1:
        compt2 += 1
    result = 1.5*max(activity, 0) + 90*max(np.exp(percentage_tweet_with_omg)-1, 0) + 100 * np.sqrt(max(capitals_per_char, 0)) + 100 * np.sqrt(max(signs_per_char, 0))+1.2 * hashtags_per_tweet**1.15+mentions_per_tweet**1.15
    percentage = float(result)/52*100

    if compt1 >= 3 and compt2 >= 2:
        percentage *= (1+0.20*(compt1+compt2)/8)

    if compt1 <= 1:
        percentage *= (1-0.35*(8-(compt1+compt2))/8)

    if percentage > 100:
        percentage = 100

    return percentage


def percentage_bot(periodicity, answer, diversity_tweets):
    if diversity_tweets == -1:
        return max(periodicity, answer)
    else:
        if max(periodicity, answer, (1-diversity_tweets)*100) > 95:
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
    if num_stalker > 45:
        if data_user(str(who_stalker), api)["user_json"]["verified"] == "True":
            famous = 1
            print("Stop stalking", who_stalker)
            return num_stalker, famous
        if num_stalker > 75:
            result = num_stalker
            print("Stop stalking", who_stalker)
        else:
            result = (6*num_stalker+3*100*percentage_tweet_with_mention-1*100*mentions_per_tweet)/8
    else:
        result = 0
    return result, famous


def percentage_spammer(diversity_tweets, diversity_hashtags, urls_percentage):
    if diversity_tweets == -1:
        return 0
    if diversity_hashtags == -1:
        return 90*(1-diversity_tweets)
    return float(600*(1-diversity_tweets)+150*(1-diversity_hashtags)+2.5*urls_percentage) / 10


def troll_bot_analyzer(user):
    try:
        user_data = data_user(user, api)
    except tweepy.TweepError:
        logging.error("This user is protected or does not exist. His  information cannot be accessed")
    else:
        if user_data["user_json"]["verified"]:
            logging.error("This user has a verified account. Therefore it is not a troll or bot")
            return 0
        if len(user_data["tweets"]) == 0:
            logging.error("There is not enough information to classify this user")
            return 0
        hashtags_per_tweet = float(user_data["number_hashtags"]) / len(user_data["tweets"])
        mentions_per_tweet = float(user_data["number_mentions"]) / len(user_data["tweets"])
        percentage_tweet_with_mention = float(user_data["tweet_with_mentions"]) / len(user_data["tweets"])
        percentage_tweet_with_hashtag = float(user_data["tweets_with_hashtags"]) / len(user_data["tweets"])
        signs_per_char, capitals_per_char, activity, percentage_tweet_with_omg = drama_queen(user_data)
        periodicity, answer = periodicity_answer(user_data)
        diversity_hashtags = tweet_iteration_hashtags(user_data)
        diversity_tweets = tweet_iteration_stemming(user_data)
        urls_percentage = tweet_iteration_urls(user_data)
        num_stalker, who_stalker = stalker(user_data)
        per_drama_queen = percentage_drama_queen(activity, percentage_tweet_with_omg, capitals_per_char, signs_per_char,
                                                 percentage_tweet_with_hashtag, percentage_tweet_with_mention,
                                                 mentions_per_tweet, hashtags_per_tweet)
        per_bot = percentage_bot(periodicity, answer, diversity_tweets)
        per_stalker, famous = percentage_stalker(num_stalker, who_stalker, mentions_per_tweet, percentage_tweet_with_mention)
        if per_stalker == 0:
            per_stalker = num_stalker
        per_spammer = percentage_spammer(diversity_tweets, diversity_hashtags, urls_percentage)
        per_hater = (1 - sentiment(user_data)) * 100
        return {per_drama_queen, per_bot, per_stalker, per_spammer, per_hater}

