from django.contrib import admin
from .models import ExpenseItem, Expense

admin.site.register(ExpenseItem)
admin.site.register(Expense)
