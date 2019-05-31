# a version of word frequency example from mapreduce tutorial

def mapper():
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import load_digits
    digits = load_digits()
    digits.images.shape
    X = digits.data
    X.shape
    y = digits.target
    y.shape

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=0)

    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(Xtrain, ytrain)
    y_model = model.predict(Xtest)
    from sklearn.metrics import accuracy_score
    return accuracy_score(ytest, y_model)



if __name__ == '__main__':
    import dispy, logging
    import os

    # assume nodes node1 and node2 have 'doc1', 'doc2' etc. on their
    # local storage, so no need to transfer them
    #map_cluster = dispy.SharedJobCluster(mapper,nodes=['*'], scheduler_node="192.168.43.50")
    map_cluster = dispy.JobCluster(mapper)

    # any node can work on reduce
    job = map_cluster.submit()
    integer = job()
    print(integer)

