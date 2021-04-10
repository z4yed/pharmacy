from django.contrib import admin
from .models import Category, Unit, Type, Leaf, Medicine, Batch
# Register your models here.

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Type)
admin.site.register(Leaf)
admin.site.register(Medicine)
admin.site.register(Batch)
