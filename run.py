import json
import tweepy
import logging
import pymongo
from time import sleep
from keys import AUTHS
from threading import Thread
from transactions import data_user
from logging.config import fileConfig
from pymongo.errors import DuplicateKeyError

fileConfig('logging_config.ini', disable_existing_loggers=False)

# setup mongo
conn = pymongo.MongoClient()
db = conn["twitter_trolls"]
users = db["users"]
handlers = db["screen_names"]


class HandlerListener(tweepy.StreamListener):
    """
    Collects user screen names and stores them in th DB
    """
    def on_data(self, status):
        try:
            json_data = json.loads(status)
            user = json_data["user"]["screen_name"]
            try:
                handlers.insert_one({"_id": user, "collected": False})

            except DuplicateKeyError:
                logging.info("User {} already exists".format(user))
                pass

        except KeyError:
            sleep(360)
            logging.error("Users not stored")

    def on_error(self, status):
        logging.error(status)


# Auth for stream
authorization = tweepy.OAuthHandler(AUTHS[0]["consumer_key"], AUTHS[0]["consumer_secret"])
authorization.set_access_token(AUTHS[0]["access_key"], AUTHS[0]["access_secret"])

# Start stream in a separate thread
twitterStream = tweepy.Stream(authorization, HandlerListener())
twitterStream.filter(locations=[-129.19921875, 23.1832796706,
                                -70.48828125, 50.3296890942],
                     async=True)


class TwitterThread(Thread):
    """
    Creates a thread with a unique api Access,
    to make all the request under that account
    """
    def __init__(self, api):
        Thread.__init__(self)
        self.api = api

    def run(self):
        while handlers.count() > users.count():

            handler = handlers.find_one({"collected": False})

            try:
                users.insert_one(data_user(handler["_id"], self.api))
                handlers.update_one({"name": handler["_id"]},
                                    {"$set": {"collected": True}})

            except Exception as e:
                logging.error("Could not store user {}, ther Exceception was {}".format(handler["user"], e))


for auth in AUTHS:

    authorization = tweepy.OAuthHandler(auth["consumer_key"], auth["consumer_secret"])
    authorization.set_access_token(auth["access_key"], auth["access_secret"])

    new_thread = TwitterThread(tweepy.API(authorization))
    new_thread.start()
