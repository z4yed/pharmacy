from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('bank-list/', views.BankList.as_view(), name='bank-list'),
    path('add-bank/', views.AddBank.as_view(), name='add-bank'),
    path('update-bank/<int:bank_id>', views.UpdateBank.as_view(), name='update-bank'),
    path('remove-bank/<int:bank_id>', views.RemoveBank.as_view(), name='remove-bank')
]
