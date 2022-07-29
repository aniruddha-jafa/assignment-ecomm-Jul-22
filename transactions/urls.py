from django.urls import path 

from . import views

urlpatterns = [
    path('vendors/', views.vendors, name='all_vendors'),
    path('transactions/', views.transactions, name='all_transaction'),
    path('transactions/<str:vendor_id>/', views.transactions, name='vendor_transactions'),
    path('hello/', views.hello, name='hello'),
]