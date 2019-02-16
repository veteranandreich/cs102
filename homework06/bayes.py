import math
import copy


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.a = alpha
        self.labels = []
        self.table = []
        self.label_chance = []

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
        self.table = [[0] * (2 * len(self.labels) + 1) for _ in range(len(word_dict))]
        for idx, word in enumerate(word_dict):
            self.table[idx][0] = word
            i = 0
            for param in word_dict[word]:
                self.table[idx][i + 1] = word_dict[word][param]
                self.table[idx][i + 2] = (word_dict[word][param] + self.a) / (labels_counter[param] + len(word_dict))
                i += 2
        labels_sum = [0] * len(self.labels)
        for value in Y:
            labels_sum[self.labels.index(value)] += 1
        self.label_chance = [math.log(value / sum(labels_sum)) for value in labels_sum]

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        labels_for_titles = []
        for st in X:
            st.lower()
            st.replace(',', '')
            words = st.split()
            labels_chance = copy.deepcopy(self.label_chance)
            for word in words:
                for td in range(len(self.table)):
                    if self.table[td][0] == word:
                        for i in range(len(labels_chance)):
                            labels_chance[i] += math.log(self.table[td][2 * i + 2])
            labels_for_titles.append(self.labels[labels_chance.index(max(labels_chance))])
        return labels_for_titles

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(X_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        score = count / len(y_test)
        return score
