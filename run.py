import pymongo
import tweepy
from transactions import data_user
from keys import AUTHS
from threading import Thread


conn = pymongo.MongoClient()
db = conn['twitter_trolls']
users = db['users']


class TwitterThread(Thread):

    def __init__(self, api):
        ''' Constructor. '''
        Thread.__init__(self)
        self.api = api

    def run(self):
        while handlers:
            users.insert_one(data_user(handlers.pop(), self.api))


for auth in AUTHS:

    authorization = tweepy.OAuthHandler(auth["consumer_key"], auth["consumer_secret"])
    authorization.set_access_token(auth["access_key"], auth["access_secret"])

    new_thread = TwitterThread(tweepy.API(authorization))
    new_thread.start()
