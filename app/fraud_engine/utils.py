import pandas as pd
from sklearn.cross_validation import train_test_split
from app.fraud_engine import config
from pymongo import MongoClient
import json


class MongoDBOperations:
    def config(self):
        """

        :return: 
        """
        connection = MongoClient()
        db = connection["testdatabase"]
        collection = db["fraudstar"]

        return collection

    def add_transactions(self, collection):
        """

        :param collection: 
        """
        collection.insert({"name": "Canada"})

    def get_transactions(self, collection):
        """

        :param collection: 
        :return: 
        """
        return collection.find({})

    def load_data_mongo(self, collection, records):
        """

        :param collection: 
        :param records: 
        """
        collection.insert_many(records)


class LoadData:
    def load_data(self):
        operation = MongoDBOperations()
        dataframe = pd.read_csv(config.DATAFILE)
        dataframe['_id'] = dataframe.index.values
        records = json.loads(dataframe.T.to_json()).values()
        db = operation.config()
        operation.load_data_mongo(db, records)
        print 'DONE'

    def get_data(self):
        collection = MongoDBOperations().config()
        dataframe = MongoDBOperations().get_transactions(collection)
        return pd.DataFrame(list(dataframe))


class DataSample(object):
    def __new__(self):
        self.ytest = super(DataSample, self).__new__(self)
        
        attribs = ['Xtrain', 'ytrain', 'Xtest', 'ytest', 'Xsim', 'ysim']
        
        if not self._hasattrs(attribs):
            self.Xtrain = super(DataSample, self).__new__(self)
            self.ytrain = super(DataSample, self).__new__(self)
            self.Xtest = super(DataSample, self).__new__(self)
            self.Xsim = super(DataSample, self).__new__(self)
            self.ysim = super(DataSample, self).__new__(self)
            self._setdata(LoadData().get_data())

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
        y = data.Class.values
        X = data.drop('Class', axis=1).values
        self.Xtrain, X_test, self.ytrain, y_test = \
            train_test_split(X, y, test_size=0.4)
        self.Xtest, self.Xsim, self.ytest, self.ysim = \
            train_test_split(X_test, y_test, test_size=0.1)


