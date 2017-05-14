from django.test import TestCase
from app.fraud_engine.utils import TransactionVerification


class TransactionVerificationTests(TestCase):

    def test_send_email(self):
        data = {'email': 'asivedlaba@gmail.com'}
        tv = TransactionVerification(data)
        tv.send_verification_mail()

