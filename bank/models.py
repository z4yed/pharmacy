from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    account_name = models.CharField(max_length=200, null=True, blank=True)
    account_number = models.CharField(max_length=200, null=True, blank=True, unique=True)
    branch = models.CharField(max_length=200, null=True, blank=True)
    signature = models.ImageField(upload_to='bank_signatures', null=True, blank=True)
    balance = models.FloatField(default=0.0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        url = ''
        if self.signature:
            url = self.signature.url
        return url
