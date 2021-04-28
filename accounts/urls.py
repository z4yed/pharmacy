from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('manufacturer-payment', views.ManufacturerPayment.as_view(), name='manufacturer_payment'),
    path('payment-list', views.PaymentList.as_view(), name='payment_list'),
    path('print-payment-pdf/<int:payment_id>', views.PrintPaymentInvoice.as_view(), name='print_payment_pdf'),

    path('customer-receipt', views.CustomerReceipt.as_view(), name='customer_receipt'),
    path('customer-receipt-list', views.ReceiptList.as_view(), name='receipt_list'),
    path('print-receipt-pdf/<int:receipt_id>', views.PrintReceiptInvoice.as_view(), name='print_receipt_pdf'),


]
