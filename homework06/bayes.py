import math
import copy


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.a = alpha
        self.word_dict = {}

    def fit(self, X, Y):
        """ Fit Naive Bayes classifier according to X, y. """
        word_list = []
        for st in X:
            st.lower()
            st.replace(',', '')
            words = st.split()
            for word in words:
                if word not in word_list:
                    word_list.append(word)
        d = dict.fromkeys(word_list, {"pos": 0, "maybe": 0, "never": 0, "pos_var": 0, "never_var": 0, "maybe_var": 0})
        pos_counter = 0
        maybe_counter = 0
        never_counter = 0
        for idx, st in enumerate(X):
            st.lower()
            st.replace(',', '')
            words = st.split()
            for word in words:
                if Y[idx] == 'good':
                    d[word]['pos'] += 1
                    pos_counter += 1
                if Y[idx] == 'maybe':
                    d[word]['maybe'] += 1
                    maybe_counter += 1
                if Y[idx] == 'good':
                    d[word]['never'] += 1
                    never_counter += 1
        for word in word_list:
            d[word]['pos_var'] = (d[word]['pos'] + self.a) / (pos_counter + len(word_list))
            d[word]['maybe_var'] = (d[word]['maybe'] + self.a) / (maybe_counter + len(word_list))
            d[word]['never_var'] = (d[word]['never'] + self.a) / (never_counter + len(word_list))
        self.word_dict = copy.deepcopy(d)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """


    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass
