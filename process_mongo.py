import dataset
from bot import periodicity_answer
from drama_queen import drama_queen
from spammer import tweet_iteration_stemming, tweet_iteration_hashtags
from haters import sentiment

sql = dataset.connect("postgresql://root:abc123@localhost/users")
table = sql["users"]


def process_cursor(cursor):
    for user in cursor:

        ans_period, ans_percent = periodicity_answer(user)
        signs, capitals, activity, omg = drama_queen(user)

        new_user = {
            "account_name": user["user"],
            "account_old": user["days_account"],
            "account_desc": user["user_json"]["description"],
            "account_mentions": user["number_mentions"],
            "account_hashtags": user["number_hashtags"],
            "account_language": user["user_json"]["lang"],
            "account_followers": user["user_json"]["followers_count"],
            "account_followees": user["user_json"]["friends_count"],
            "account_geo": user["user_json"]["geo_enabled"],
            "account_location": user["user_json"]["location"],
            "account_total_tweets": user["user_json"]["statuses_count"],
            "account_verified": user["user_json"]["verified"],
            "tweet_period": ans_period,
            "tweet_signs": signs,
            "tweet_capitals": capitals,
            "tweet_activity": activity,
            "tweet_omg": omg,
            "tweet_steeming": tweet_iteration_stemming(user),
            "tweet_hashtags": tweet_iteration_hashtags(user),
            "tweets_with_hashtags": user["tweets_with_hashtags"],
            "tweets_positive": sentiment(user),
            "answer_percent": ans_percent
        }

        table.insert(new_user)