from transactions import data_user


def stalker(json):
    counter = json["mentions"]
    if json["number_mentions"] == 0:
        return 0, "zero"
    result = float(counter.most_common(1)[0][1]) / json["number_mentions"] * 100
    return result, counter.most_common(1)[0][0]


def percentage_stalker(num_stalker, who_stalker, mentions_per_tweet, percentage_tweet_with_mention, api):
    famous = 0
    if num_stalker > 45:
        if data_user(str(who_stalker), api)["user_json"]["verified"]:
            famous = 1
            print("Stop stalking", who_stalker)
            return num_stalker, famous
        if num_stalker > 75:
            result = num_stalker
            print("Stop stalking", who_stalker)
        else:
            result = (6*num_stalker+3*100*percentage_tweet_with_mention-1*100*mentions_per_tweet)/8
    else:
        result = 0
    return result, famous, who_stalker
