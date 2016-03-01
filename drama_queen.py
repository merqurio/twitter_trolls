import re


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
        signs_per_char = num_signs / num_char * 100.0
        capitals_per_char = num_capitals / num_char * 100.0

    if float(user["days_account"]) == 0:
        activity = 0
    else:
        activity = user["user_json"]["statuses_count"] / float(user["days_account"])

    percentage_tweet_with_omg = float(num_omg)/len(user["tweets"])

    return signs_per_char, capitals_per_char, activity, percentage_tweet_with_omg
