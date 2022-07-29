from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Transaction

User = get_user_model()

class TransactionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.vendor1 = User.objects.create_user(
                    email='test.vendor1@email.com',
                    password="secret",
                    phone='+919800011111',
                    balance = 0.0,
                    is_seller=True,
        )
        cls.customer1 = User.objects.create_user(
                    email='test.customer1@email.com',
                    password="secret",
                    phone='+919800022222',
                    balance = 0.0,
                    is_seller=False,
        )
        cls.customer2 = User.objects.create_user(
                    email='test.customer2@email.com',
                    password="secret",
                    phone='+919800033333',
                    balance = 0.0,
                    is_seller=False,
        )

    def test_transaction_vendor_should_be_seller(self):
        not_a_seller = self.customer1
        transaction = Transaction.objects.create(
            amount='6',
            vendor=not_a_seller,
            status='PEN', 
            customer=self.customer2
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()