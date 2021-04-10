import math
from django.db import models
from manufacturer.models import Manufacturer


class Category(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{a} --> {b}'.format(a=self.name, b=self.is_active)


class Unit(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()

    def __str__(self):
        return '{a} --> {b}'.format(a=self.name, b=self.is_active)


class Type(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()

    def __str__(self):
        return '{a} --> {b}'.format(a=self.name, b=self.is_active)


class Leaf(models.Model):
    leaf_type = models.CharField(max_length=200)
    number_per_box = models.IntegerField(default=0)

    def __str__(self):
        return '{a} --> {b}'.format(a=self.leaf_type, b=self.number_per_box)


class MedicineCSV(models.Model):
    file = models.FileField(upload_to='medicine_csvs', null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Medicine(models.Model):
    code_text = models.CharField(max_length=250, null=True, blank=True)
    strength = models.CharField(max_length=250, null=True, blank=True)
    box_size = models.ForeignKey(Leaf, on_delete=models.SET_NULL, null=True, blank=True)
    shelf = models.CharField(max_length=250, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    vat = models.FloatField(default=0)
    medicine_name = models.CharField(max_length=300)
    generic_name = models.CharField(max_length=200, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    details = models.CharField(max_length=500, null=True, blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='medicines', null=True, blank=True)
    manufacturer_price = models.FloatField()
    barcode_path = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{a}".format(a=self.medicine_name)

    @property
    def image_url(self):
        try:
            url = self.code_image.path
        except:
            url = ''
        return url

    @property
    def price_one(self):
        price = self.price / self.box_size.number_per_box
        floating_point = price - int(price)
        if floating_point >= 0.5:
            return math.ceil(price)
        else:
            return price

    @property
    def manufacturer_price_one(self):
        price = self.manufacturer_price / self.box_size.number_per_box
        floating_point = price - int(price)
        if floating_point >= 0.5:
            return math.ceil(price)
        else:
            return price

    @property
    def total_stock(self):
        stock = 0
        for batch in self.batch_set.filter(is_active=True):
            stock += batch.current_stock
        return stock

    @property
    def total_sold(self):
        sold = 0
        for batch in self.batch_set.filter(is_active=True):
            sold += batch.sold_quantity
        return sold

    @property
    def in_quantity(self):
        return self.total_stock + self.total_sold

    @property
    def stock_sale_price(self):
        return float(self.total_stock) * float(self.price_one)

    @property
    def stock_purchase_price(self):
        return float(self.total_stock) * float(self.manufacturer_price_one)


class Batch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=True)
    batch_number = models.CharField(max_length=200, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    box_pattern = models.ForeignKey(Leaf, on_delete=models.DO_NOTHING, null=True, blank=True)
    box_quantity = models.FloatField(null=True, blank=True)
    batch_stock = models.FloatField(default=0)
    previous_stock = models.FloatField(default=0, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} -- > {}".format(self.medicine, self.batch_number)

    @property
    def total_quantity(self):
        return self.box_pattern.number_per_box * self.box_quantity

    @property
    def sold_quantity(self):
        total = 0
        for quantity in self.invoiceitems_set.filter(is_active=True):
            total += quantity.sell_quantity

        return total

    @property
    def current_stock(self):
        total_returned = 0

        for item in self.returned_batch.filter(order__is_active=True, order__wastage=False):
            total_returned += item.return_quantity  # returned batch is from return Models

        return float(self.batch_stock) - float(self.sold_quantity) + total_returned

