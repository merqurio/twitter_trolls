import random
import nltk
from nltk import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

# Check the corpora is installed
try:
    nltk.data.find('movie_reviews')
except LookupError:
    nltk.download('movie_reviews')


def word_feats(words):
    return dict([(word, True) for word in words])


def find_features(document, word_features):
    words = word_tokenize(document["text"])
    features = {}
    for t in word_features:
        for w in t[0].keys():
            features[w] = (w in words)

    return features

neg_ids = movie_reviews.fileids('neg')
pos_ids = movie_reviews.fileids('pos')

neg_features = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
pos_features = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]
all_features = neg_features + pos_features

classifier = NaiveBayesClassifier.train(all_features)


def is_positive(sentence):
    sentence_features = find_features(sentence, all_features)
    return 1 if classifier.classify(sentence_features) == "pos" else 0


def sentiment(user):
    tweets = random.sample(user["tweets"], 10)
    return sum(map(is_positive, tweets))/10.0
