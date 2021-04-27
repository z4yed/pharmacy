from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('users_auth.urls')),
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('manufacturer/', include('manufacturer.urls')),
    path('medicine/', include('medicine.urls')),
    path('bank/', include('bank.urls')),
    path('service/', include('service.urls')),
    path('purchase/', include('purchase.urls')),
    path('invoice/', include('invoice.urls')),
    path('settings/', include('settings.urls')),
    path('reports/', include('reports.urls')),
    path('employee/', include('employee.urls')),
    path('return/', include('return.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
