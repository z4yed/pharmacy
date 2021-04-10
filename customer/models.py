from django.db import models as dbModel
from system.utils import CUSTOMER_STATUS


class Customer(dbModel.Model):
    name = dbModel.CharField(max_length=200)
    mobile_number = dbModel.CharField(max_length=13)
    first_email = dbModel.EmailField(max_length=50, null=True, blank=True)
    second_email = dbModel.EmailField(max_length=50, null=True, blank=True)
    phone = dbModel.CharField(max_length=15, null=True, blank=True)
    contact = dbModel.CharField(max_length=200, null=True, blank=True)
    first_address = dbModel.CharField(max_length=200, null=True, blank=True)
    second_address = dbModel.CharField(max_length=200, null=True, blank=True)
    fax = dbModel.CharField(max_length=200, null=True, blank=True)
    city = dbModel.CharField(max_length=200, null=True, blank=True)
    state = dbModel.CharField(max_length=200, null=True, blank=True)
    zip = dbModel.CharField(max_length=200, null=True, blank=True)
    country = dbModel.CharField(max_length=200, null=True, blank=True)
    previous_balance = dbModel.FloatField(default=0.00, null=True, blank=True)
    current_balance = dbModel.FloatField(default=0.00, null=True, blank=True)
    status = dbModel.IntegerField(choices=CUSTOMER_STATUS)

    is_active = dbModel.BooleanField(default=True)

    def __str__(self):
        return self.name
