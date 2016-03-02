import re
import numpy as np


def drama_queen(user):
    """ Different values to evaluate if it's a dramaqueen

    :param user: the twitter @username data
    :type user: dict

    :return: Use of signs,
             Use of capital letter,
             Activity of user,
             OMG usage
    :rtype: float, float, float, float
    """

    num_signs = 0
    num_capitals = 0
    num_char = 0
    num_omg = 0

    for tweet in user["tweets"]:
        text = tweet["text"]
        num_signs += len(re.findall(r"\!|\:|\^|\<|\?|\...", text))
        num_capitals += len(re.findall(r"[A-Z]", text))
        num_char += len(re.findall(r"\S", text))
        num_omg += len(re.findall(r"OMG|Oh\sMy\sGod|OH\sMY\sGOD|oh\smy\sgod|omg|o\sm\sg|O\sM\sG|WTF|wtf|LOL|lol|W\sT\sF|"
                                  r"um|like|awe|AWE", text))

    if num_char == 0:
        signs_per_char = 0
        capitals_per_char = 0
    else:
        signs_per_char = float(num_signs) / num_char
        capitals_per_char = float(num_capitals) / num_char

    if float(user["days_account"]) == 0:
        activity = 0
    else:
        activity = user["user_json"]["statuses_count"] / float(user["days_account"])

    percentage_tweet_with_omg = float(num_omg)/len(user["tweets"])

    return signs_per_char, capitals_per_char, activity, percentage_tweet_with_omg


def percentage_drama_queen(activity, percentage_tweet_with_omg, capitals_per_char, signs_per_char, percentage_tweet_with_hashtag, percentage_tweet_with_mention, mentions_per_tweet, hashtags_per_tweet):
    activity_average = 8
    capitals_per_char_average = 0.1113
    signs_per_char_average = 0.03002
    percentage_tweet_with_omg_average = 0.1196
    percentage_tweet_with_mention_average = 0.5950
    percentage_tweet_with_hashtag_average = 0.1758
    mentions_per_tweet_average = 0.7953
    hashtags_per_tweet_average = 0.3431
    compt1 = 0
    compt2 = 0

    activity -= activity_average
    if activity > 20:
        activity = 20
    capitals_per_char -= capitals_per_char_average
    signs_per_char -= signs_per_char_average
    percentage_tweet_with_omg -= percentage_tweet_with_omg_average
    percentage_tweet_with_hashtag -= percentage_tweet_with_hashtag_average
    percentage_tweet_with_mention -= percentage_tweet_with_mention_average
    mentions_per_tweet /= mentions_per_tweet_average
    hashtags_per_tweet /= hashtags_per_tweet_average

    if mentions_per_tweet > 5:
        mentions_per_tweet = 5
    if hashtags_per_tweet > 5:
        hashtags_per_tweet = 5
    if activity > 0:
        compt1 += 1
    if capitals_per_char > 0:
        compt1 += 1
    if signs_per_char > 0:
        compt1 += 1
    if percentage_tweet_with_omg > 0:
        compt1 += 1
    if percentage_tweet_with_hashtag > 0:
        compt2 += 1
    if percentage_tweet_with_mention > 0:
        compt2 += 1
    if mentions_per_tweet > 1:
        compt2 += 1
    if hashtags_per_tweet > 1:
        compt2 += 1
    result = 1.5*max(activity, 0) + 90*max(np.exp(percentage_tweet_with_omg)-1, 0) + 100 * np.sqrt(max(capitals_per_char, 0)) + 100 * np.sqrt(max(signs_per_char, 0))+1.2 * hashtags_per_tweet**1.15+mentions_per_tweet**1.15
    percentage = float(result)/52*100

    if compt1 >= 3 and compt2 >= 2:
        percentage *= (1+0.20*(compt1+compt2)/8)

    if compt1 <= 1:
        percentage *= (1-0.35*(8-(compt1+compt2))/8)

    if percentage > 100:
        percentage = 100

    return percentage