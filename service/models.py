from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    charge = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    vat = models.FloatField(default=0)
    igta = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
