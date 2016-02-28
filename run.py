from bot import periodicity_answer
from spammer import tweet_iteration_stemming, tweet_iteration_hashtags
from transactions import data_user
from stalker import stalker
import tweepy
from drama_queen import drama_queen

consumer_key = "iaAqgOyzLb2qbTsjOZXoZpbIB"
consumer_secret = "QZrExTZsMeqykJpw0EogLH5uEiOqj0bJquy5rJEQhehrlCBTAY"
access_key = "155609363-VOaTTLbdRZKkgRSnHmu30ht9pLY9VJ0ArZZOy2uD"
access_secret = "AycYj44tusCbzLZgyW6hENvIe6kXbKujluGXw1kpsEfJ6"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def run(user):
    user_data = data_user(user, api)
    if user_data["user_json"]["verified"] == "True":
        print "This user has a verified account. Therefore it is not a troll or bot"
        return 0
    if len(user_data["tweets"]) == 0:
        print "There is not enough information to classify this user"
        return 0
    #TODO: mira si la cuenta da el error 401
    periodicity, answer = periodicity_answer(user_data)
    diversity_hashtags = tweet_iteration_hashtags(user_data)
    diversity_tweets = tweet_iteration_stemming(user_data)
    num_stalker = stalker(user_data)
    print periodicity
    print answer
    print diversity_hashtags
    print diversity_tweets
    print num_stalker

    return 0

