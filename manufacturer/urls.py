from django.urls import path
from . import views

app_name = 'manufacturer'

urlpatterns = [
    path('add-manufacturer/', views.AddManufacturer.as_view(), name='add-manufacturer'),
    path('manufacturer-list/', views.ManufacturerList.as_view(), name='manufacturer-list'),
    path('edit-manufacturer/<int:manufacturer_id>', views.EditManufacturer.as_view(), name='edit-manufacturer'),
    path('remove-manufacturer/<int:manufacturer_id>', views.RemoveManufacturer.as_view(), name='remove-manufacturer'),
    path('upload-csv/', views.UploadCsv.as_view(), name='upload-manufacturer-csv')
]
