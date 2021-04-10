from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('sales-report', views.SalesReport.as_view(), name='sales-report'),
    path('sales-report-userwise', views.SalesReportUser.as_view(), name='sales-report-user'),
    path('sales-report-productwise', views.sales_report_product, name='sales-report-product'),
    path('sales-report-categorywise', views.sales_report_category, name='sales-report-category'),

    path('purchase-report', views.purchase_report, name='purchase_report'),
    path('purchase-report-category', views.purchase_report_category, name='purchase_report_category'),
]
