from django.db import models
from invoice.models import Invoice
from purchase.models import Purchase


class InvoiceReturn(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    wastage = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.invoice)

    @property
    def total_deduction(self):
        pass

    @property
    def total_tax(self):
        pass

    @property
    def net_return(self):
        pass


class InvoiceReturnItems(models.Model):
    order = models.ForeignKey('return.InvoiceReturn', on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey('medicine.Batch', on_delete=models.SET_NULL, related_name='returned_batch', null=True, blank=True)
    item = models.ForeignKey('invoice.InvoiceItems', on_delete=models.SET_NULL, related_name='returned_item', null=True, blank=True)
    return_quantity = models.IntegerField(default=0)
    deduction = models.FloatField(default=0)

    def __str__(self):
        return str(self.order)


class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, blank=True)
    return_date = models.DateField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)
    wastage = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.purchase)


class PurchaseReturnItems(models.Model):
    order = models.ForeignKey(PurchaseReturn, on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey('medicine.Batch', on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey('purchase.PurchaseItems', on_delete=models.SET_NULL, null=True, blank=True)
    return_quantity = models.IntegerField(default=0)
    deduction = models.FloatField(default=0)

    def __str__(self):
        return str(self.return_quantity)

