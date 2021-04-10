from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('add-purchase', views.AddPurchase.as_view(), name='add-purchase'),
    path('purchase-list', views.PurchaseList.as_view(), name='purchase-list'),
    path('view-purchase/<int:purchase_id>', views.ViewPurchase.as_view(), name='view-purchase'),
    path('update-purchase/<int:purchase_id>', views.UpdatePurchase.as_view(), name='update-purchase'),
    path('remove-purchase/<int:purchase_id>', views.RemovePurchase.as_view(), name='remove-purchase'),

    # Ajax Calls
    path('fetch-medicines/', views.FetchMedicines.as_view(), name='fetch-medicine'),
    path('fetch-price/', views.FetchPrice.as_view(), name='fetch_price'),
    path('fetch-quantity', views.FetchQuantity.as_view(), name='fetch-quantity'),
    path('remove-purchase-item', views.RemovePurchaseItem.as_view(), name='remove-purchase-item'),

]
