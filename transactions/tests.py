from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from .models import Transaction

User = get_user_model()

class TransactionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.vendor1 = User.objects.create_user(
                    email='test.vendor1@email.com',
                    password='secret',
                    balance = 0.0,
                    is_seller=True,
        )
        cls.customer1 = User.objects.create_user(
                    email='test.customer1@email.com',
                    password='secret',
                    is_seller=False,
        )
        cls.customer2 = User.objects.create_user(
                    email='test.customer2@email.com',
                    password='secret',
                    is_seller=False,
        )

    def test_transaction_vendor_should_be_seller(self):
        not_a_seller = self.customer1
        transaction = Transaction.objects.create(
            amount=50.0,
            vendor=not_a_seller,
            status='COM', 
            customer=self.customer2
        )
        with self.assertRaises(ValidationError) as ex:
            transaction.full_clean()

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = User.objects.create_user(
                    email='test.vendor1@email.com',
                    password='secret',
                    is_seller=True,
        )
        self.customer1 = User.objects.create_user(
                    email='test.customer1@email.com',
                    password='secret',
                    is_seller=False,
        )
        self.transaction1 = Transaction.objects.create(
            amount=50.0,
            status='COM',
            vendor=self.vendor1,
            customer=self.customer1,
        )
    
    def test_get_all_vendors(self):
        response = self.client.get('/api/vendors/', format='json')
        self.assertEqual(response.status_code, 200)
        
        data = response.data
        self.assertIsNotNone(data)
        
        vendors = data.get('vendors', None)
        self.assertIsNotNone(vendors)
        self.assertGreater(len(vendors), 0)
        self.assertEqual(vendors[0]['email'], 'test.vendor1@email.com')

    def test_get_all_transaction(self):
        response = self.client.get('/api/transactions/', format='json')
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertIsNotNone(data)

        transactions = data.get('transactions', None)
        self.assertIsNotNone(transactions)
        self.assertGreater(len(transactions), 0)
        amount = float(transactions[0]['amount'])
        self.assertEqual(amount, 50.0)