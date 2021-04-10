from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('add-customer/', views.AddCustomer.as_view(), name='add-customer'),
    path('customer-list/', views.CustomerList.as_view(), name='customer-list'),
    path('edit-customer/<str:customer_id>', views.EditCustomer.as_view(), name='edit-customer'),
    path('remove-customer/<int:customer_id>', views.RemoveCustomer.as_view(), name='remove-customer'),
    path('paid-customer/', views.PaidCustomer.as_view(), name='paid-customer'),
    path('credit-customer/', views.CreditCustomer.as_view(), name='credit-customer'),
]
