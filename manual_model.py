import logging
import tweepy
from bot import percentage_bot, periodicity_answer
from spammer import tweet_iteration_stemming, tweet_iteration_hashtags, tweet_iteration_urls, percentage_spammer
from transactions import data_user
from stalker import percentage_stalker, stalker
from haters import sentiment
from logging.config import fileConfig
from drama_queen import percentage_drama_queen, drama_queen

fileConfig('logging_config.ini', disable_existing_loggers=False)


def troll_bot_analyzer(user, api):
    try:
        user_data = data_user(user, api)
    except tweepy.TweepError:
        logging.error("This user is protected or does not exist. His  information cannot be accessed")
    else:
        if len(user_data["tweets"]) == 0:
            logging.error("There is not enough information to classify this user")
            return False
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
        per_stalker, famous, non_famous = percentage_stalker(num_stalker, who_stalker, mentions_per_tweet, percentage_tweet_with_mention, api)
        if per_stalker == 0:
            per_stalker = num_stalker
        per_spammer = percentage_spammer(diversity_tweets, diversity_hashtags, urls_percentage)
        per_hater = (1 - sentiment(user_data)) * 100

        max_value = [per_bot, per_drama_queen, per_stalker, per_hater, per_spammer]
        index = max_value.index(max(max_value))
        labels = ["bot", "drama_queen", "stalker", "hater", "spammer"]
        final = labels[index]

        return {"user_id": user, "bot": per_bot, "drama_queen": per_drama_queen, "stalker": per_stalker, "hater": per_hater, "spammer": per_spammer, "famous": famous, "non_famous": non_famous, "stalked": who_stalker, "final": final}
