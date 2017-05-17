from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views import View

from app.fraud_engine import fraud_models
from app.fraud_engine.fraud_models import RandomForestModel
from app.fraud_engine.utils import MongoDBOperations
#from app.fraud_engine.utils import TransactionVerification
from numpy import where
import json
from models import DeepLink



class Phone(View):
    def post(self, request,  *args, **kwargs):
        account = kwargs['ac']
        response = {
        "contacts": [
            {
                    "id": "c200",
                    "name": "Mabu Manaileng",
                    "email": "mabu@gmail.com",
                    "address": "xx-xx-xxxx,x - street, x - country",
                    "gender" : "male",
                    "phone": {
                        "mobile": "+91 0000000000",
                        "home": "00 000000",
                        "office": "00 000000"
                    }
            },
            {
                    "id": "c201",
                    "name": "Doctor Lero",
                    "email": "doctor.lero@gmail.com",
                    "address": "xx-xx-xxxx,x - street, x - country",
                    "gender" : "male",
                    "phone": {
                        "mobile": "+91 0000000000",
                        "home": "00 000000",
                        "office": "00 000000"
                    }
            }
                ]
            }

        dictionary = json.dumps(response)
        return HttpResponse(dictionary)

    def get(self, request,  *args, **kwargs):
        response = {
        "contacts": [
            {
                    "id": "c200",
                    "name": "Ravi Tamada",
                    "email": "ravi@gmail.com",
                    "address": "xx-xx-xxxx,x - street, x - country",
                    "gender" : "male",
                    "phone": {
                        "mobile": "+91 0000000000",
                        "home": "00 000000",
                        "office": "00 000000"
                    }
            },
            {
                    "id": "c201",
                    "name": "Johnny Depp",
                    "email": "johnny_depp@gmail.com",
                    "address": "xx-xx-xxxx,x - street, x - country",
                    "gender" : "male",
                    "phone": {
                        "mobile": "+91 0000000000",
                        "home": "00 000000",
                        "office": "00 000000"
                    }
            }
                ]
            }

        dictionary = json.dumps(response)
        return HttpResponse(dictionary)

class Dashboard(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """

        # data = {'email': 'mabu@itechhub.co.za', 'domain': request.get_host()}
        # data = {'email': 'asivedlaba@gmail.com', 'domain': request.get_host()}
        # tv = TransactionVerification(data)
        # tv.send_verification_mail()

        X, y = RandomForestModel().get_data()
        #print X[0]
        indexes = where(y == 1)[0]

        X_fraud = [{'account': int(X[:, -3][index]), 'amount': X[:, 0][index],
                    'fraud': y[index], 'type': int(X[:, -1][index]),'index': index,
                    'status': int(X[:, -2][index])} for index in indexes]
                      
        context = {'data': X_fraud}

        return render(request, self.template_name, context)


class UpdateTrasaction(View):
    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        collection = MongoDBOperations().config()
        MongoDBOperations().fraud_detect_update(int(kwargs['ac']),
                                                collection)
        return HttpResponseRedirect('/')

class LockTrasaction(View):
    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        collection = MongoDBOperations().config()
        MongoDBOperations().lock_transaction(int(kwargs['ac']),
                                                collection)
        return HttpResponseRedirect('/')

class UnlockTrasaction(View):
    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
        collection = MongoDBOperations().config()
        MongoDBOperations().release_transaction(int(kwargs['ac']),
                                                collection)
        return HttpResponseRedirect('/')

class Demo(View):
    template_name = 'demo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


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
    template_name = 'modal.html'

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


class ModelTraining(View):
    template_name = 'app.html'

    def get(self, request):
        model = fraud_models.RandomForestModel()
        model.train()
        accuracy, anomaly_points = model.get_accuracy()
        context = {'accuracy': accuracy, 'anomaly_points': anomaly_points}
        return render(request, self.template_name, context)
