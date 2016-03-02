import tweepy
import random
from manual_model import troll_bot_analyzer
from connexion import NoContent
from keys import AUTHS


def get_user(user_id):

    keys = random.choice(AUTHS)
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_key"], keys["access_secret"])
    api = tweepy.API(auth)

    u = troll_bot_analyzer(user_id, api)

    return u if u else NoContent, 500
