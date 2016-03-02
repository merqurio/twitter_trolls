import tweepy
import random
from manual_model import troll_bot_analyzer
from connexion import NoContent
from keys import AUTHS


def get_user(user_id):

    STREAM = random.choice(AUTHS)
    auth = tweepy.OAuthHandler(STREAM["consumer_key"], STREAM["consumer_secret"])
    auth.set_access_token(STREAM["access_key"], STREAM["access_secret"])
    api = tweepy.API(auth)

    u = troll_bot_analyzer(user_id, api)

    return u if u else NoContent, 500
