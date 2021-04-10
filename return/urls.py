from django.urls import path
from . import views

app_name = 'return'

urlpatterns = [
    path('return', views.ReturnHome.as_view(), name='return-home'),
    path('return-invoice/', views.InvoiceReturn.as_view(), name='return_invoice'),
    path('return-purchase/', views.PurchaseReturn.as_view(), name='return_purchase'),

]
