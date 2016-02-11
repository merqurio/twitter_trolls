import tweepy
from time import sleep
from datetime import datetime
from collections import Counter


def limit_handled(cursor):
    """
    :param cursor: A cursor to iterate
    :type cursor: tweepy.Cursor
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            sleep(60)


def data_user(handler, api):
    """
    Stores  a user in MongoDB
    :param handler the twitter @username
    :type handler: str or unicode

    :param api: an instance of tweepy api
    :type api: tweepy.api.API

    :returns: All the users values
    :rtype: dict

    :Example:
        >>> data_user("gabimaeztu")
        >>> users.find({"user":"gabimaeztu"})
        <pymongo.cursor.Cursor at 0x1052e9050>
    """
    today = datetime.today()
    user = api.get_user(handler)

    model = {"id": user.id,
             "user": user.screen_name,
             "user_json": user._json,
             "days_account": (today - user.created_at).days,
             "tweets": [],
             "tweets_with_hashtags": 0,
             "number_hashtags": 0,
             "tweet_with_mentions": 0,
             "number_mentions": 0,
             "mentions": [],
             "followers": []}

    for tweet in limit_handled(tweepy.Cursor(api.user_timeline, screen_name=handler).items()):
        model["tweets"].append(tweet._json)

    for follower in limit_handled(tweepy.Cursor(api.followers, screen_name=handler).items()):
        model["followers"].append({"user": follower.screen_name,
                                   "followers_count": follower.followers_count,
                                   "language": follower.lang,
                                   "tweets_num": follower.statuses_count,
                                   "account_age": (today - follower.created_at).days
                                   })
    mentions = []

    for tweet in model["tweets"]:

        if len(tweet["entities"]["hashtags"]) > 0:
            model["tweets_with_hashtags"] += 1
            model["number_hashtags"] += len(tweet["entities"]["hashtags"])

        if len(tweet["entities"]["user_mentions"]) > 0:
            model["tweet_with_mentions"] += 1
            model["number_mentions"] += len(tweet["entities"]["user_mentions"])

            for x in range(0, len(tweet["entities"]["user_mentions"])):
                mentions.append(tweet["entities"]["user_mentions"][x]["screen_name"])

    model["mentions"] = Counter(mentions)

    return model
