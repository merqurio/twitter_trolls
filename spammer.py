import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from collections import Counter



def tweet_stemming(tweet, token_freqs):
    """
    Stems tweets words and counts diversty
    
    :param tweet: the tweet to analyze
    :type tweet: str or unicode

    :param token_freqs: counter of words frequency
    :type token_freqs: Counter

    :returns: words added to token_freqs
    :rtype: int
    """
    
    pattern_url = '((https?:\/\/)|www\.)([\da-z\.-]+)\.([\/\w \.-]*)( |$)'
    regexPunctuation = re.compile('[%s]' % re.escape(string.punctuation))
    porter = PorterStemmer()

    counter_tokens = 0
    tweet_URLremoved = re.sub(pattern_url, '', tweet, flags=re.MULTILINE) # remove URL
    tweet_URLremoved_tokenized = word_tokenize(tweet_URLremoved) # tokenize tweet
    tweet_URLremoved_tokenized_cleaned_stemming = [] # cleaned of URLs and hashs, and stemming

    for token in tweet_URLremoved_tokenized:
        new_token = regexPunctuation.sub(u'', token) # remove punctuation and hash
        if not new_token == u'':
            new_token_stemming = porter.stem(new_token)
            tweet_URLremoved_tokenized_cleaned_stemming.append(new_token_stemming)
            token_freqs[new_token_stemming] += 1
            counter_tokens += 1
    
    return counter_tokens


def tweet_hashtags(hashtags, hashtag_freqs):
    """
    Looks for hashtags and counts diversty
    
    :param hashtags: the list of hashtags to analyze
    :type hashtags: list

    :param hashtag_freqs: counter of hashtags frequency
    :type hashtag_freqs: Counter

    :returns: hashtags added to hashtag_freqs
    :rtype: int
    """
    
    for hashtag in hashtags:
        hashtag_freqs[hashtag['text']] += 1
    return len(hashtags)


def tweet_iteration_stemming(user):
    """
    For a given user, returns its ratio of tweets language diversity,
    between 0 and 1 (0: low diversity, 1: high diversity)
    or -1 if no word is used in tweets
    
    :param user: json of the user
    :type user: json

    :returns: ratio of tweets language diversity
    :rtype: float
    """
    
    tweets = user['tweets']
    token_freqs = Counter()
    counter_tokens = 0
    
    for tweet in tweets:
        counter_tokens += tweet_stemming(tweet['text'], token_freqs)
        
    if( counter_tokens == 0 ):
        return -1
    else:
        token_diversity_ratio = float(len(token_freqs))/counter_tokens
        return token_diversity_ratio


def tweet_iteration_hashtags(user):
    """
    For a given user, returns its ratio of hashtags diversity,
    between 0 and 1 (0: low diversity, 1: high diversity), 
    or -1 if no hashtag is used
    
    :param user: json of the user
    :type user: json

    :returns: ratio of hashtags diversity
    :rtype: float
    """
    
    if user["tweets_with_hashtags"] <= 0:
        return -1
    
    tweets = user['tweets']
    hashtag_freqs = Counter()
    counter_hashtags = 0
    
    for tweet in tweets:
        hashtags = tweet['entities']["hashtags"]
        if len(hashtags) > 0:
            counter_hashtags += tweet_hashtags(hashtags, hashtag_freqs)

    hashtag_diversity_ratio = float(len(hashtag_freqs))/counter_hashtags
    
    return hashtag_diversity_ratio
