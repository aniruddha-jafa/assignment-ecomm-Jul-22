from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Transaction
from .serializers import VendorSerializer, TransactionSerializer

# ----------------------------------------------------------------

User = get_user_model()

@api_view()
def hello(request):
    return Response({ 'message': 'hello!' })

@api_view()
def vendors(request):
    vendors = User.objects.filter(is_seller=True)
    serializer = VendorSerializer(vendors, many=True)
    return Response({ 'vendors': serializer.data })

@api_view()
def transactions(request, vendor_id = ''):
    if not vendor_id:
        transactions = Transaction.objects.all()
    else:
        try:
            transactions = Transaction.objects.filter(vendor_id=vendor_id)
        except Exception as ex: 
            return Response({ 'error': repr(ex) })
    serializer = TransactionSerializer(transactions, many=True)
    return Response({ 'transactions': serializer.data})

