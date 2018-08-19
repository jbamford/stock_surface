import support_vector as support_vector
import numpy as np


def test_support_vector():
    """ 
    Test the support vcecot with the exaampole on sklearns site
    """
    X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
    y = np.array([1, 1, 2, 2])
    sv = support_vector.Support_Vector(X, y)
    sv.train()
    assert sv.predict_out_put([[-0.8, -1]]) == [1]
