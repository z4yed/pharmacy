from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('pharmacy-details/', views.SettingView.as_view(), name='pharmacy_details'),
]
