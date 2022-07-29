from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Transaction
from .serializers import VendorSerializer, TransactionSerializer

# ----------------------------------------------------------------

User = get_user_model()

@api_view()
def vendors(request):
    '''
    Get all vendors 
    '''
    vendors = User.objects.filter(is_seller=True)
    serializer = VendorSerializer(vendors, many=True)
    return Response({ 'vendors': serializer.data })

@api_view()
def transactions(request, vendor_id = ''):
    '''
    Get a list of Transactions 
    
    Can specify vendor_id to get transactions for that vendor
    Returns all transactions if no vendor_id is given
    '''
    if not vendor_id:
        transactions = Transaction.objects.all()
    else:
        try:
            transactions = Transaction.objects.filter(vendor_id=vendor_id)
        except Exception as ex: 
            return Response({ 'error': repr(ex) })
    serializer = TransactionSerializer(transactions, many=True)
    return Response({ 'transactions': serializer.data})


@api_view()
def perform_payment(request, transaction_id):
    ''' 
    Perform the payment specified in transaction with transaction_id
    '''
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response({ 'error': f'Unable to find transaction with id: {transaction_id}'})
    
    # TODO 
    # validate transaction status
    # eg. already completed transactions should not be repeated etc
    
    try:
        with db_transaction.atomic():
            vendor = transaction.vendor
            amount = transaction.amount
            vendor.balance += amount
            vendor.save()
            # transaction.status = 'COM'
            # transaction.save()
    except Exception as ex:
        return Response({ 'error': str(err) })

    return Response({ 'message': f'Successfully added {amount} to balance of vendor {vendor.email}' })


@api_view()
def hello(request):
    return Response({ 'message': 'Hello!' })