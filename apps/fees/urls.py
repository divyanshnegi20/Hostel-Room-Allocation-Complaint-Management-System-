from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fee_dashboard, name='fee_dashboard'),
    path('pay/', views.make_payment, name='make_payment'),
    path('receipt/<int:pk>/', views.payment_receipt, name='payment_receipt'),
    path('all/', views.all_payments, name='all_payments'),
]
