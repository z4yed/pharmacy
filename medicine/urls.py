from django.urls import path
from . import views

app_name = 'medicine'

urlpatterns = [
    path('category-list', views.CategoryList.as_view(), name='category-list'),
    path('add-category', views.AddCategory.as_view(), name='add-category'),
    path('update-category/<int:category_id>', views.UpdateCategory.as_view(), name='update-category'),
    path('remove-category/<int:category_id>', views.RemoveCategory.as_view(), name='remove-category'),

    path('unit-list', views.UnitList.as_view(), name='unit-list'),
    path('add-unit', views.AddUnit.as_view(), name='add-unit'),
    path('update-unit/<int:unit_id>', views.UpdateUnit.as_view(), name='update-unit'),
    path('remove-unit/<int:unit_id>', views.RemoveUnit.as_view(), name='remove-unit'),

    path('type-list', views.TypeList.as_view(), name='type-list'),
    path('add-type', views.AddType.as_view(), name='add-type'),
    path('update-type/<int:type_id>', views.UpdateType.as_view(), name='update-type'),
    path('remove-type/<int:type_id>', views.RemoveType.as_view(), name='remove-type'),

    path('leaf-list', views.LeafList.as_view(), name='leaf-list'),
    path('add-leaf', views.AddLeaf.as_view(), name='add-leaf'),
    path('update-leaf/<int:leaf_id>', views.UpdateLeaf.as_view(), name='update-leaf'),
    path('remove-leaf/<int:leaf_id>', views.RemoveLeaf.as_view(), name='remove-leaf'),


    path('medicine-list', views.MedicineList.as_view(), name='medicine-list'),
    path('add-medicine', views.AddMedicine.as_view(), name='add-medicine'),
    path('update-medicine/<int:medicine_id>', views.UpdateMedicine.as_view(), name='update-medicine'),
    path('remove-medicine/<int:medicine_id>', views.RemoveMedicine.as_view(), name='remove-medicine'),
    path('upload-medicine-csv/', views.UploadMedicineCsv.as_view(), name='upload-medicine-csv'),
    path('bar-codes/<int:medicine_id>', views.BarCodes.as_view(), name='bar-code'),
    path('print-bar-code/<int:medicine_id>', views.ViewBarcodePDF.as_view(), name='barcode-pdf'),


    # Stock
    path('stock-list', views.StockList.as_view(), name='stock-list'),
    path('stock-list-batch', views.StockListBatchWise.as_view(), name='stock-list-batch'),
    path('stocked-medicines', views.AvailableStock.as_view(), name='available-stock')

]
