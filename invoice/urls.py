from django.urls import path
from . import views

app_name = 'invoice'

urlpatterns = [
    path('add-invoice', views.AddInvoice.as_view(), name='add-invoice'),
    path('edit-invoice/<int:invoice_id>', views.EditInvoice.as_view(), name='edit-invoice'),
    path('remove-invoice/<int:invoice_id>', views.RemoveInvoice.as_view(), name='remove-invoice'),
    path('invoice-list', views.InvoiceList.as_view(), name='invoice-list'),
    path('invoice-details/<int:invoice_id>', views.ViewInvoice.as_view(), name='invoice-details'),


    # Ajax(s)
    path('fetch-info', views.FetchMedicineInfo.as_view(), name='fetch-med-info'),
    path('fetch-batch', views.FetchBatch.as_view(), name='fetch-batch'),
    path('fetch-customer', views.FetchCustomer.as_view(), name='fetch-customer'),
    path('fetch-batch-list', views.FetchBatchList.as_view(), name='fetch-batch-list'),
    path('remove-invoice-item', views.RemoveInvoiceItem.as_view(), name='remove-invoice-item'),
]
