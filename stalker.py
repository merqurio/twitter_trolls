def stalker(json):
    counter = json["mentions"]
    if json["number_mentions"] == 0:
        return 0
    num_most_common = counter.most_common(1)[0][1]
    result = float(num_most_common) / json["number_mentions"] * 100
    return result
