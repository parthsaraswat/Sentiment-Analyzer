import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import random
import pickle
from collections import Counter
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
hm_lines = 10000


def create_lexicon(pos, neg):
    lexicon = []
    with open(pos, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            all_words = word_tokenize(l)
            lexicon += list(all_words)
    with open(neg, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            all_words = word_tokenize(l)
            lexicon += list(all_words)

    # Lemmatizing
    lexicon = [lemmatizer.lemmatize(i) for i in lexicon]
    # Removing common and uncommon words
    w_counts = Counter(lexicon)
    l2 = []  # Our final lexicon
    for w in w_counts:
        if 50 < w_counts[w] < 1000:
            l2.append(w)
    print(len(l2))  # Checking final length of lexicon
    return l2


def sample_handler(sample, lexicon, classification):

    featureset = []

    with open(sample, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            current_words = word_tokenize(l.lower())
            current_words = [lemmatizer.lemmatize(i) for i in current_words]
            features = np.zeros(len(lexicon))
            for word in current_words:
                if word.lower() in lexicon:
                    index_value = lexicon.index(word.lower())
                    features[index_value] += 1
            features = list(features)
            featureset.append([features, classification])
    return featureset


def create_features_and_labels(pos, neg, test_size=0.1):

    lexicon = create_lexicon(pos, neg)
    features = []
    features += sample_handler('pos.txt', lexicon, [1, 0])
    features += sample_handler('neg.txt', lexicon, [0, 1])
    random.shuffle(features)
    features = np.array(features)

    testing_size = int(test_size*len(features))

    train_x = list(features[:, 0][:-testing_size])
    train_y = list(features[:, 1][:-testing_size])
    test_x = list(features[:, 0][-testing_size:])
    test_y = list(features[:, 1][-testing_size:])

    return train_x, train_y, test_x, test_y


if __name__ == '__main__':
    train_x,train_y,test_x,test_y = create_features_and_labels('pos.txt','neg.txt')
# if you want to pickle this data:

    with open('sentiment_set.pickle','wb') as f: # wb means writing to a file in binary
        pickle.dump([train_x,train_y,test_x,test_y],f)