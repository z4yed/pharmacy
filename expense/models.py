from django.db import models

from purchase.models import PAYMENT_TYPES, BANK_CHOICES


class ExpenseItem(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name[:20]


class Expense(models.Model):
    date = models.DateField()
    expense_type = models.ForeignKey(ExpenseItem, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.IntegerField(choices=PAYMENT_TYPES, null=True, blank=True)
    bank = models.IntegerField(choices=BANK_CHOICES, null=True, blank=True)
    amount = models.FloatField(default=0)
    remarks = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.expense_type} --> {self.amount}"
