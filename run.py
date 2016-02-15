import json
import tweepy
import logging
import pymongo
from time import sleep
from keys import AUTHS, STREAM
from threading import Thread
from transactions import data_user
from logging.config import fileConfig
from tweepy.error import TweepError
from pymongo.errors import DuplicateKeyError

fileConfig('logging_config.ini', disable_existing_loggers=False)

# setup mongo
conn = pymongo.MongoClient()
db = conn["twitter_trolls"]
users = db["users"]
screen_names = db["screen_names"]


class HandlerListener(tweepy.StreamListener):
    """
    Collects user screen names and stores them in th DB
    """
    def on_data(self, status):
        try:
            json_data = json.loads(status)
            user = json_data["user"]["screen_name"]
            try:
                screen_names.insert_one({"_id": user, "collected": False, "completed": False})

            except DuplicateKeyError:
                logging.info("User {} already exists.".format(user))
                pass

        except KeyError:
            sleep(1000)
            logging.error("Users not stored.")

    def on_error(self, status):
        logging.error(status)


# Auth for stream
# authorization = tweepy.OAuthHandler(STREAM["consumer_key"], STREAM["consumer_secret"])
# authorization.set_access_token(STREAM["access_key"], STREAM["access_secret"])

# Start stream in a separate thread
# twitterStream = tweepy.Stream(authorization, HandlerListener())
# twitterStream.filter(locations=[-129.19921875, 23.1832796706,
#                                 -70.48828125, 50.3296890942],
#                      async=True)


class TwitterThread(Thread):
    """
    Creates a thread with a unique api Access,
    to make all the request under that account
    :param api: The credentials that the thread should use
    :type api: tweepy.API
    """
    def __init__(self, api):
        Thread.__init__(self)
        self.api = api

    def run(self):
        while screen_names.count() > users.count():

            s_name = screen_names.find_one_and_update({"collected": False},
                                                      {"$set": {"collected": True}})
            logging.info("User {} in thread {}.".format(s_name["_id"], self.getName()))

            try:
                users.insert_one(data_user(s_name["_id"], self.api))
                screen_names.update_one({"_id": s_name["_id"]},
                                        {"$set": {"completed": True}})

            except TweepError as e:
                logging.error("Ups, Arrived to API limit in thread {}. Exception: {}".format(self.getName(), e))
                sleep(60 * 15)

            except Exception as e:
                logging.error("Could not store user {}, the Exceception was {}.".format(s_name["user"], e))


for auth in AUTHS:

    authorization = tweepy.OAuthHandler(auth["consumer_key"], auth["consumer_secret"])
    authorization.set_access_token(auth["access_key"], auth["access_secret"])

    new_thread = TwitterThread(tweepy.API(authorization))
    new_thread.start()
