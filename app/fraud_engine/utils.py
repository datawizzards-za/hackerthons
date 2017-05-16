import pandas as pd
import json

from sklearn.cross_validation import train_test_split
from pymongo import MongoClient
#from sklearn.model_selection import train_test_split
from django.conf import settings
from django.core.mail import send_mail
from numpy import random
from django.core.mail import EmailMultiAlternatives

from app.models import DeepLink
from app.fraud_engine import config


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

    def fraud_detect_update(self, unique_id, collection):
        # Trasaction status
        # 0 - normal
        # 1 - locked
        # 2 - suspicious
        # 3 - released
        # ______________#

        collection.update_one({'_id': unique_id},
                              {'$set': {'Class': 0}},upsert=False)

        return unique_id

    def release_transaction(self, unique_id, collection):

        collection.update_one({'_id': unique_id},
                              {'$set': {'status': 3}}, upsert=False)

        return unique_id

    def lock_transaction(self, unique_id, collection):

        collection.update_one({'_id': unique_id},
                              {'$set': {'status': 1}}, upsert=False)

        return unique_id

    def suspect_transaction(self, unique_id, collection):

        collection.update_one({'_id': unique_id},
                              {'$set': {'status': 2}}, upsert=False)

        return unique_id

class LoadData:
    def load_data(self):
        operation = MongoDBOperations()
        print 'Importing dataset...'
        dataframe = pd.read_csv(config.DATAFILE)
        dataframe['_id'] = dataframe.index.values
        length = len(dataframe)
        dataframe['type'] = random.randint(0, 3, size=(length, 1))
        dataframe['status'] = random.randint(0, 4, size=(length, 1))
        records = json.loads(dataframe.T.to_json()).values()
        db = operation.config()
        print('Loading data..')
        operation.load_data_mongo(db, records)
        print 'DONE!!!'

    def get_data(self):
        collection = MongoDBOperations().config()
        json_data = MongoDBOperations().get_transactions(collection)
        dataframe = pd.DataFrame(list(json_data))
        dataframe = dataframe.reindex_axis(sorted(dataframe.columns), axis=1)
        #print dataframe.columns
        return dataframe


class DataSample(object):
    """Singleton to split data three ways; train, test and simulation.

    Attributes:
        Xtrain (vector): training features.
        ytrain (scalar): training labels.
        Xtest (vector): testing features.
        ytest (scalar): testing labels.
        Xsim (vector): simulation features.
        ysim (scalar): simulation labels.
    
    """

    def __new__(self):
        """Create new objects only if they have not yet been
        instantiated.

        Args:
            None.

        Returns (tuple):
            Dataset partitioned into train, test, and simulation data.

        """

        attribs = ['Xtrain', 'ytrain', 'Xtest', 'ytest', 'Xsim', 'ysim']

        if not self._hasattrs(attribs):
            self.Xtrain = super(DataSample, self).__new__(self)
            self.ytrain = super(DataSample, self).__new__(self)
            self.Xtest = super(DataSample, self).__new__(self)
            self.ytest = super(DataSample, self).__new__(self)
            self.Xsim = super(DataSample, self).__new__(self)
            self.ysim = super(DataSample, self).__new__(self)
            self._setdata(LoadData().get_data())

        return (self.Xtrain, self.ytrain, self.Xtest, self.ytest, self.Xsim,
                self.ysim)

    @classmethod
    def _hasattrs(self, attribs):
        """Check if class objects have not yet been instantiated
        
        Args:
            attribs(list):  List of class objects names as strings.

        Returns (Boolean):
            True if all attributes have already been instantiated
            otherwise false.

        """

        for attr in attribs:
            if not hasattr(self, attr):
                return False

        return True

    @classmethod
    def _setdata(self, data):
        """Split data according to predefined proportions.

        Args:
            data (pandas): dataframe representing the whole dataset.
        
        Returns:
            Void.
            
        """

        y = data.Class.values
        X = data.drop('Class', axis=1).values
        self.Xtrain, X_test, self.ytrain, y_test = \
            train_test_split(X, y, test_size=0.4)
        self.Xtest, self.Xsim, self.ytest, self.ysim = \
            train_test_split(X_test, y_test, test_size=0.1)


class TransactionVerification:
    """Lets user verify the flagged transaction as a precaution and
    attempt to successfully identify fraudulent transactions.

    Attributes:
        data (dict): transaction data. 
    
    """

    def __init__(self, data):
        """Initialise transaction verification object with transaction
        data.
       
        Args:
            data (dict): transaction data. 

        Returns:
            Void.
        
        """

        self.data = data

    def send_verification_mail(self):
        """Given transaction data, send the user verification email to
        let them acknowledge the fraud while also verifying whether or
        not the transaction is fraudulent.
        
        Args:
            None.
            
        Returns (Boolean):
            State of the mail sending; true when sent successfully,
            otherwise false.

        """

        subject = 'Fraudmaster detected a fraudulent activity on your \
                   BankZ cheque account.'
        from_email = settings.EMAIL_HOST_USER
        to = self.data['email']
        text_content = 'Hi banker suspicious activities have been \
                        detected on your account.'
        deep_link = 'http://' + self._get_deep_link()
        html_content = '''<p>Please click on the link below to verify the 
        transaction on your account. <br><a href="''' + deep_link + \
                       '''">''' + deep_link + '''</a></p>'''

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def _get_deep_link(self):
        """Add a onetime DeepLink object in the database.
        
        Args:
            None.

        Returns (uuid):
            DeepLink object uuid.

        """

        host_name = self.data['domain']
        uuid = DeepLink.objects.create().uuid
        deep_link = host_name + '/app/' + str(uuid) + '/'

        return deep_link
