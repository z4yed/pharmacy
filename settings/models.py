from django.db import models

from system.utils import CURRENCY_CHOICES, DISCOUNT_TYPES, TIMEZONE_CHOICES


class Setting(models.Model):
    company_title = models.CharField(max_length=200, null=True, blank=True)
    menu_title = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    favicon = models.ImageField(upload_to='favicon', null=True, blank=True)
    login_background = models.ImageField(upload_to='login_background', null=True, blank=True)
    currency = models.IntegerField(choices=CURRENCY_CHOICES, null=True, blank=True)
    discount_type = models.IntegerField(choices=DISCOUNT_TYPES, null=True, blank=True)
    time_zone = models.IntegerField(choices=TIMEZONE_CHOICES, null=True, blank=True)
    footer_text = models.TextField(default='Copyright@2021')

    def __str__(self):
        return self.company_title
