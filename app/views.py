from django.shortcuts import render
from django.views import View
from app.fraud_engine import fraud_models
from pymongo import MongoClient
#from fraudmaster.auth import MongoBdAuth as DBAuth


class Home(View):
    template_name = 'app/index.html'

    def get(self, request):
        model = fraud_models.RandomForestModel()
        model.train()
        accuracy, anomaly_points = model.get_accuracy()
        operation = MongoDBOperations()
        db = operation.config()
        #operation.add_transactions(db)
        print operation.get_transactions(db)

        context = {'accuracy': accuracy, 'anomaly_points':anomaly_points}
        return render(request, self.template_name, context)


class ModelTraining(View):
    template_name = 'app/app.html'


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