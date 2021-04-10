from django.contrib import admin
from .models import *

admin.site.register(InvoiceReturn)
admin.site.register(InvoiceReturnItems)
admin.site.register(PurchaseReturn)
admin.site.register(PurchaseReturnItems)
