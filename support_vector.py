"""
Jason Bamford 
7/21/2018
"""

import numpy as np
from sklearn.svm import SVC
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import optunity
import optunity.metrics
import sklearn.svm
from sklearn.datasets import load_digits
import pandas
from sklearn.model_selection import TimeSeriesSplit
from sklearn.externals import joblib
from datetime import datetime


class Support_Vector():
    """
    class used to handle the ML
    """

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.space = space = {'kernel': {'linear': {'C': [0, 2]},
                                         'rbf': {'logGamma': [-5, 0], 'C': [0, 10]},
                                         'poly': {'degree': [2, 5], 'C': [0, 5], 'coef0': [0, 2]}
                                         }
                              }

    def train(self):
        """
        x and y are the featchures and the target values for the differnt pairs that we want the model to learn over
        """

        # splits = TimeSeriesSplit(n_splits=3)
        # index = 1
        # for train_index, test_index in splits.split(self.X):
        #     train = self.X[train_index]
        #     test = self.X[test_index]
        #     print('Observations: %d' % (len(train) + len(test)))
        #     print('Training Observations: %d' % (len(train)))
        #     print('Testing Observations: %d' % (len(test)))
        #     index += 1

        # for train_index, test_index in tscv.split(self.X):
        #     print("TRAIN:", train_index, "TEST:", test_index)
        #     self.X_train, self.X_test = self.X[train_index], self.X[test_index]
        #     self.y_train, self.y_test = self.Y[train_index], self.Y[test_index]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.Y, test_size=0.2)

        # svclassifier = SVC(kernel='rbf', gamma=0.47686340994)
        svclassifier = SVC(kernel='rbf', gamma=0.30084722307,
                           C=9.027665188437386)
        svclassifier.fit(self.X_train, self.y_train)
        self.y_pred = svclassifier.predict(self.X_test)

        confustion_matrix = confusion_matrix(self.y_test, self.y_pred)

        print(classification_report(self.y_test, self.y_pred))

        # clf = SVC()
        # clf.fit(self.X_train, self.y_train)
        self.model = pickle.dumps(svclassifier)
        joblib.dump(svclassifier, 'models/model' +
                    str(datetime.now()) + '.pkl')

        return confustion_matrix[0]  # , confustion_matrix[1]

    def predict_out_put(self, X):
        """
        This method is takes a pair of values and predicts if it will be a good to buy or not
        """
        clf2 = pickle.loads(self.model)
        return clf2.predict(X[0:1])

    def set_up_optunity(self):
        digits = load_digits()
        n = digits.data.shape[0]

        positive_digit = 8
        negative_digit = 9

        positive_idx = [i for i in range(n) if digits.target[
            i] == positive_digit]
        negative_idx = [i for i in range(n) if digits.target[
            i] == negative_digit]

        # add some noise to the data to make it a little challenging
        original_data = digits.data[positive_idx + negative_idx, ...]
        self.data = original_data + 5 * \
            np.random.randn(original_data.shape[0], original_data.shape[1])
        self.labels = [True] * len(positive_idx) + [False] * len(negative_idx)

    def train_model(self, x_train, y_train, kernel, C, logGamma, degree, coef0):
        """A generic SVM training function, with arguments based on the chosen kernel."""
        if kernel == 'linear':
            model = sklearn.svm.SVC(kernel=kernel, C=C)
        elif kernel == 'poly':
            model = sklearn.svm.SVC(
                kernel=kernel, C=C, degree=degree, coef0=coef0)
        elif kernel == 'rbf':
            model = sklearn.svm.SVC(kernel=kernel, C=C, gamma=10 ** logGamma)
        else:
            raise ("Unknown kernel function: %s" % kernel)
        model.fit(x_train, y_train)
        return model

    def svm_tuned_auroc(self, x_train, y_train, x_test, y_test, kernel='linear', C=0, logGamma=0, degree=0, coef0=0):
        model = self.train_model(x_train, y_train, kernel,
                                 C, logGamma, degree, coef0)
        decision_values = model.decision_function(x_test)
        return optunity.metrics.roc_auc(y_test, decision_values)

    def run_optunity(self):
        cv_decorator = optunity.cross_validated(
            x=self.X, y=self.Y, )

        svm_tuned_auroc = cv_decorator(self.svm_tuned_auroc)

        optimal_svm_pars, info, _ = optunity.maximize_structured(
            svm_tuned_auroc, self.space, num_evals=150, pmap=optunity.pmap)
        print("Optimal parameters" + str(optimal_svm_pars))
        print("AUROC of tuned SVM: %1.3f" % info.optimum)

        df = optunity.call_log2dataframe(info.call_log)
        print df.sort_values('value', ascending=False)

if '__main__' == __name__:

    X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
    y = np.array([1, 1, 2, 2])
    # sv = Support_Vector(X, y)
    # sv.train()
    # sv.predict_out_put([[-0.8, -1]])
    sv = Support_Vector(X, y)
    print 'setting up'
    sv.set_up_optunity()
    print 'running...'
    sv.run_optunity()
