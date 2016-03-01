import re


def drama_queen(json):
    num_signs = 0
    num_capitals = 0
    num_char = 0
    num_omg = 0

    for tweet in json["tweets"]:
        text = tweet["text"]
        num_signs += len(re.findall(r'\!|\:|\^|\<|\?|\...', text))
        num_capitals += len(re.findall(r'[A-Z]', text))
        num_char += len(re.findall(r'\S', text))
        num_omg += len(re.findall(r' OMG |Oh My God|OH MY GOD|oh my god| omg |o m g|O M G', text))

    if num_char == 0:
        signs_per_char = 0
        capitals_per_char = 0
    else:
        signs_per_char = float(num_signs) / float(num_char)*100
        capitals_per_char = float(num_capitals) / float(num_char)*100

    if float(json["days_account"]) == 0:
        activity = 0
    else:
        activity = json["user_json"]["statuses_count"] / float(json["days_account"])

    percentage_tweet_with_omg = float(num_omg)/len(json["tweets"])

    # volem que faci servir moltes majuscules i molts signes de puntuacio
    # volem que tingui una activitat elevada
    # volem tambe que faci servir molts hashtags
    # volem tambe que faci moltes mencions a cada tweet i que el percentatge de tweet amb mencio sigui elevat
    # quins valors hi donem?

    return signs_per_char, \
           capitals_per_char, \
           activity, \
           percentage_tweet_with_omg
