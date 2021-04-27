from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('manufacturer-payment', views.ManufacturerPayment.as_view(), name='manufacturer_payment'),
    path('payment-list', views.PaymentList.as_view(), name='payment_list'),
]
