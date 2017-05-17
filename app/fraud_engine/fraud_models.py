from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from app.fraud_engine.utils import DataSample
from sklearn.metrics import accuracy_score


class RandomForestModel:

    def __init__(self):
        self.classifier = RandomForestClassifier()
        self.Xtrain, self.ytrain, self.Xtest, self.ytest, self.Xsim, self.ysim \
            = DataSample()

    def train(self):
        self.classifier.fit(self.Xtrain, self.ytrain)

    def get_data(self):
        return self.Xsim, self.ysim

    def get_accuracy(self):
        predicted = self.classifier.predict(self.Xtest)
        anomaly_points = predicted.tolist().index(0)
        self.classifier.fit(self.Xtest, self.ytest)
        accuracy = accuracy_score(self.ytest, predicted)
        return accuracy, anomaly_points
    
"""
class CombinedModels:

    def __init__(self):
        models = []
        models.append(('LR', LogisticRegression()))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))
        self.classifier = RandomForestClassifier()
        self.Xtrain, self.ytrain, self.Xtest, self.ytest, self.Xsim, self.ysim \
            = DataSample()

    def train(self):
        self.classifier.fit(self.Xtrain, self.ytrain)

    def get_data(self):
        return self.Xsim, self.ysim

    def get_accuracy(self):
        predicted = self.classifier.predict(self.Xtest)
        anomaly_points = predicted.tolist().index(0)
        self.classifier.fit(self.Xtest, self.ytest)
        accuracy = accuracy_score(self.ytest, predicted)
        return accuracy, anomaly_points
"""