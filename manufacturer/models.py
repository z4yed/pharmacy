from django.db import models


class CSV(models.Model):
    file = models.FileField(upload_to='csvs', null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=13)
    first_email = models.EmailField(max_length=50, null=True, blank=True)
    second_email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    first_address = models.CharField(max_length=200, null=True, blank=True)
    second_address = models.CharField(max_length=200, null=True, blank=True)
    fax = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zip = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    previous_balance = models.FloatField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
