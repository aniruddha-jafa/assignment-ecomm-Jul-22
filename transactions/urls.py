from django.urls import path 

from . import views

urlpatterns = [
    path('vendors/', views.vendors, name='all_vendors'),
    path('transactions/', views.transactions, name='all_transaction'),
    path('transactions/<uuid:vendor_id>/', views.transactions, name='vendor_transactions'),
    path('transaction/<uuid:transaction_id>', views.perform_payment, name='perform_payment'),
    path('', views.hello, name='hello'),
]