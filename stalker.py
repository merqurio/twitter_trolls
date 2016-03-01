def stalker(json):
    counter = json["mentions"]
    if json["number_mentions"] == 0:
        return 0, "zero"
    result = float(counter.most_common(1)[0][1]) / json["number_mentions"] * 100
    return result, counter.most_common(1)[0][0]
