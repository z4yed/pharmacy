from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('service-list/', views.ServiceList.as_view(), name='service-list'),
    path('add-service', views.AddService.as_view(), name='add-service'),
    path('update-service/<int:service_id>', views.EditService.as_view(), name='update-service'),
    path('remove-service/<int:service_id>', views.RemoveService.as_view(), name='remove-service'),
]

