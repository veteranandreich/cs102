import math
import copy


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.a = alpha
        self.labels = []
        self.table = []

    def fit(self, X, Y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [label for label in set(Y)]
        self.labels.sort()
        labels_counter = dict.fromkeys(self.labels, 0)
        word_dict = {}
        for idx, st in enumerate(X):
            st.lower()
            st.replace(',', '')
            words = st.split()
            for word in words:
                if word not in word_dict:
                    word_dict[word] = dict.fromkeys(self.labels, 0)
                word_dict[word][Y[idx]] += 1
                labels_counter[Y[idx]] += 1
        self.table = [[] * (2 * len(self.labels) + 1) for _ in range(len(word_dict))]
        for idx, word in enumerate(word_dict):
            self.table[idx][0] = word
            i = 0
            for param in word:
                self.table[idx][i + 1] = param
                self.table[idx][i + 2] = (word[param] + self.a) / (labels_counter[param] + len(word_dict))
                i += 2

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass
