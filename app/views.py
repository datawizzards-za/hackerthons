from django.shortcuts import render
from django.views import View
from app.fraud_engine import fraud_models
from app.fraud_engine.fraud_models import RandomForestModel
from pymongo import MongoClient
import numpy as np

from app.fraud_engine.utils import TransactionVerification


# from fraudmaster.auth import MongoBdAuth as DBAuth


class Help(View):
    template_name = 'guidely.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        return render(request, self.template_name)


class Settings(View):
    template_name = 'charts.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        return render(request, self.template_name)


class Financials(View):
    template_name = 'reports.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        return render(request, self.template_name)


class Analysis(View):
    template_name = 'charts.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        return render(request, self.template_name)


class Dashboard(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        
        #data = {'email': 'mabu@itechhub.co.za', 'domain': request.get_host()}
        #data = {'email': 'asivedlaba@gmail.com', 'domain': request.get_host()}
        #tv = TransactionVerification(data)
        #tv.send_verification_mail()
    
        X, y = RandomForestModel().get_data()
        indexes = np.where(y == 1)[0]
        X_anomaly = [[index, X[:, -1][index]] for index in indexes]
        #print X_anomaly
        context = {'values': X_anomaly, 'indexes': indexes}
        return render(request, self.template_name, context)


class ModelTraining(View):
    template_name = 'app.html'

    def get(self, request):
        model = fraud_models.RandomForestModel()
        model.train()
        accuracy, anomaly_points = model.get_accuracy()
        operation = MongoDBOperations()
        db = operation.config()
        # operation.add_transactions(db)
        print operation.get_transactions(db)

        context = {'accuracy': accuracy, 'anomaly_points': anomaly_points}
        return render(request, self.template_name, context)


class MongoDBOperations:
    def config(self):
        connection = MongoClient()
        db = connection["testdatabase"]
        collection = db["fraudstar"]

        return collection

    def add_transactions(self, collection):
        collection.insert({"name": "Canada"})

    def get_transactions(self, collection):
        return collection.find({})
