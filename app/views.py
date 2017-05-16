from django.shortcuts import render
from django.views import View
from app.fraud_engine import fraud_models
from app.fraud_engine.fraud_models import RandomForestModel
from numpy import where

from app.fraud_engine.utils import TransactionVerification


class Demo(View):
    template_name = 'demo.html'

    def get(self, request, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:

        Returns:

        """
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

        indexes = where(y == 1)[0]
        X_anomaly = [{'account': int(X[:, -1][index]), 'amount': X[:, 0][index]
                      ,'fraud':y[index], 'index': index} for index in indexes]
                      
        context = {'data': X_anomaly}
        
        return render(request, self.template_name, context)


class ModelTraining(View):
    template_name = 'app.html'

    def get(self, request):
        model = fraud_models.RandomForestModel()
        model.train()
        accuracy, anomaly_points = model.get_accuracy()
        context = {'accuracy': accuracy, 'anomaly_points': anomaly_points}
        return render(request, self.template_name, context)
