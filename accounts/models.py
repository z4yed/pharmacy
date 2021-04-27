from django.db import models

from purchase.models import PAYMENT_TYPES, BANK_CHOICES


class ManufacturerPayment(models.Model):
    voucher_no = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    manufacturer = models.ForeignKey('manufacturer.Manufacturer', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(default=0)
    payment_type = models.IntegerField(choices=PAYMENT_TYPES, null=True, blank=True)
    bank = models.IntegerField(choices=BANK_CHOICES, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.voucher_no} --> {self.amount}"
