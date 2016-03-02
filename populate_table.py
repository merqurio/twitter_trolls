import threading
import pymongo
from process_mongo import process_cursor

client = pymongo.MongoClient("188.166.145.237", 27017)
db = client["twitter_trolls"]
users = db["users"]

cursors = users.parallel_scan(1)
threads = [threading.Thread(target=process_cursor, args=(cursor,)) for cursor in cursors]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()