import pandas as pd
from sklearn.cross_validation import train_test_split
from app.fraud_engine import config


def read_data():
    return pd.read_csv(config.DATAFILE)


class DataSample(object):

    def __new__(self):
        attribs = ['Xtrain', 'ytrain', 'Xtest', 'ytest', 'Xsim', 'ysim']
        if not self._hasattrs(attribs):
            self.Xtrain = super(DataSample, self).__new__(self)
            self.ytrain = super(DataSample, self).__new__(self)
            self.Xtest = super(DataSample, self).__new__(self)
            self.ytest = super(DataSample, self).__new__(self)
            self.Xsim = super(DataSample, self).__new__(self)
            self.ysim = super(DataSample, self).__new__(self)
            self._setdata(read_data())

        return (self.Xtrain, self.ytrain, self.Xtest, self.ytest, self.Xsim,
                self.ysim)

    @classmethod
    def _hasattrs(self, attribs):
        for attr in attribs:
            if not hasattr(self, attr):
                return False
        return True

    @classmethod
    def _setdata(self, data):
        X = data.values[:, :-1]
        y = data.Class.values
        self.Xtrain, X_test, self.ytrain, y_test = \
            train_test_split(X, y, test_size=0.4)
        self.Xtest, self.Xsim, self.ytest, self.ysim = \
            train_test_split(X_test, y_test, test_size=0.1)
