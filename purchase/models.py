from django.db import models
from medicine.models import Medicine, Leaf, Batch
from manufacturer.models import Manufacturer


PAYMENT_TYPES = (
    (1, 'Cash Payment'),
    (2, 'Bank Payment')
)

BANK_CHOICES = (
    (1, 'City Bank'),
    (2, 'UCB'),
    (3, 'DBBl'),
    (4, 'Prime Asia'),
)


class Purchase(models.Model):
    purchase_id = models.IntegerField(unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    invoice = models.CharField(max_length=100, null=True, blank=True)
    details = models.TextField()
    payment_types = models.IntegerField(choices=PAYMENT_TYPES, default=1)
    bank = models.IntegerField(choices=BANK_CHOICES, null=True, blank=True)

    vat = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice

    @property
    def subtotal(self):
        subtotal = 0
        for value in self.purchaseitems_set.filter(is_active=True):
            subtotal += value.calculated_price
        return subtotal

    @property
    def grand_total(self):
        return self.subtotal + self.vat - self.discount

    @property
    def due_amount(self):
        return self.grand_total - self.paid_amount

    @property
    def purchase_items(self):
        return self.purchaseitems_set.filter(is_active=True)


class PurchaseItems(models.Model):
    order = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{a}".format(a=self.order)

    @property
    def calculated_price(self):
        medicine_price = self.batch.medicine.manufacturer_price
        return self.batch.box_quantity * medicine_price


