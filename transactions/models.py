from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

def is_vendor(account_id):
    account = User.objects.get(pk=account_id)
    if not account.is_seller:
        raise ValidationError('Account must be of a vendor')

class TransactionStatus(models.TextChoices):
    PENDING = 'PEN'
    COMPLETE = 'COM'
    FAILED = 'FAI'
    CANCELLED = 'CAN'
    REFUNDED = 'REF'
    UNKNOWN = 'UNK'

class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    
    amount = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=4, choices=TransactionStatus.choices)

    vendor = models.ForeignKey(User, related_name='vendor_id', on_delete=models.CASCADE, validators=[is_vendor])
    customer = models.ForeignKey(User, related_name='customer_id', on_delete=models.CASCADE)
    
    date = models.DateTimeField(auto_now_add=True)

