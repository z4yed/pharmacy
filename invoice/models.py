from django.db import models
from medicine.models import Medicine, Batch
from purchase.models import PAYMENT_TYPES, BANK_CHOICES


class Invoice(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    invoice_id = models.CharField(max_length=20, null=True, blank=True)
    details = models.CharField(max_length=200, null=True, blank=True)
    payment_types = models.IntegerField(choices=PAYMENT_TYPES, default=1)
    bank = models.IntegerField(choices=BANK_CHOICES, null=True, blank=True)

    invoice_discount = models.FloatField(default=0, null=True, blank=True)
    total_vat = models.FloatField(default=0, null=True, blank=True)
    paid_amount = models.FloatField(default=0, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_number

    @property
    def total_discount(self):
        total_discount = float(self.invoice_discount)
        discounts = []
        line_totals = []

        for item in self.invoiceitems_set.filter(is_active=True):
            if item.discount:
                discounts.append(item.discount)
            else:
                discounts.append(0)

            line_totals.append(item.total_bill)

        for index, value in enumerate(line_totals):
            line_discount = (value * discounts[index]) / 100
            total_discount += line_discount

        return total_discount

    @property
    def grand_total(self):
        line_totals = 0.0
        for item in self.invoiceitems_set.filter(is_active=True):
            line_totals += item.total_bill_exclude_vat

        return line_totals - self.invoice_discount

    @property
    def line_totals(self):
        line_totals = 0.0
        for item in self.invoice_items:
            line_totals += item.total_bill_exclude_vat
        return line_totals

    @property
    def net_total(self):
        return self.grand_total + self.customer.previous_balance

    @property
    def due_amount(self):
        due = 0.0
        if float(self.paid_amount) < float(self.net_total):
            due = float(self.net_total) - float(self.paid_amount)
        return due

    @property
    def change(self):
        change = 0.0
        if float(self.due_amount) == 0:
            change = float(self.paid_amount) - float(self.net_total)
        return change

    @property
    def invoice_items(self):
        return self.invoiceitems_set.filter(is_active=True)


class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    sell_quantity = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.sell_quantity)

    @property
    def total_bill(self):
        return float(self.sell_quantity) * float(self.price)

    @property
    def total_bill_exclude_vat(self):  # vat is not vat. It should be Discount. :|
        return float(self.total_bill) - (float(self.total_bill) * float(self.discount)) / 100

    @property
    def vat_amount(self):  # vat is not vat. It should be Discount. :|
        return float(self.total_bill) - float(self.total_bill_exclude_vat)

    @property
    def sell_return_combined(self):
        returned = 0
        for item in self.returned_item.filter(order__is_active=True):
            returned += item.return_quantity

        return self.sell_quantity - returned


