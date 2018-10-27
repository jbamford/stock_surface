import support_vector as support_vector
import numpy as np
from sklearn import datasets


def test_support_vector():
    """ 
    Test the support vcecot with the exaampole on sklearns site
    """
    X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
    y = np.array([1, 1, 2, 2])
    sv = support_vector.Support_Vector(X, y)
    sv.train()
    assert sv.predict_out_put([[-0.8, -1]]) == [1]


def test_support_vector_on_datasets():
    """
    Used to test the SVM on training data from the sklean website
    """
    iris = datasets.load_iris()
    X = iris.data[:, [0, 2]]
    y = iris.target

    sv = support_vector.Support_Vector([], [])

    sv.X = X
    sv.Y = y
    sv.train()
