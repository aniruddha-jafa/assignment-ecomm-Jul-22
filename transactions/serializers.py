from rest_framework import serializers 
from django.contrib.auth import get_user_model

from .models import Transaction

User = get_user_model() 

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = (
            'id',
            'email',
            'balance',
            'updated',
        )

class TransactionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Transaction
        fields = (
            'id',
            'amount',
            'vendor',
            'customer',
            'date',
        )
