import datetime
import random

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from manufacturer.models import Manufacturer
from medicine.models import Leaf, Medicine, Batch
from settings.models import Setting
from system.utils import random_id_generator
from .models import BANK_CHOICES, PAYMENT_TYPES, Purchase, PurchaseItems


class AddPurchase(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        manufacturers = Manufacturer.objects.filter(is_active=True)
        leafs = Leaf.objects.all()

        context = {
            'manufacturers': manufacturers,
            'leafs': leafs,
            'banks': list(BANK_CHOICES),
            'payment_types': list(PAYMENT_TYPES),
        }

        return render(request, 'purchase/add_purchase.html', context)

    def post(self, request):
        data = request.POST

        purchase_id = random_id_generator('Purchase')

        manufacturer_id = data.get('manufacturer_id')
        manufacturer_obj = Manufacturer.objects.get(id=manufacturer_id)

        purchase_date = request.POST.get('date')  # Dec 18, 2020
        purchase_date = datetime.datetime.strptime(purchase_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        invoice_no = data.get('invoice_no')
        details = data.get('details', '')
        payment_type = data.get('payment_type')
        bank_id = data.get('bank_id')

        medicine_list = data.getlist('medicine_name[]')
        batch_id_list = data.getlist('batch_id[]')
        expire_date_list = data.getlist('expire_date[]')
        leaf_type_list = data.getlist('leaf_type[]')
        box_quantity_list = data.getlist('box_quantity[]')
        product_quantity_list = data.getlist('product_quantity[]')

        vat = data.get('vat')
        discount = data.get('discount')
        paid_amount = float(data.get('paid_amount'))

        purchase_obj = Purchase(purchase_id=purchase_id, manufacturer=manufacturer_obj, date=purchase_date, invoice=invoice_no,
                                details=details, payment_types=payment_type, bank=bank_id if bank_id else None,
                                vat=vat if vat else 0, discount=discount if discount else 0, paid_amount=paid_amount if paid_amount else 0)
        purchase_obj.save()

        # Saving Purchase Items
        for i in range(len(medicine_list)):  # loop will execute number of rows times

            expire_date = expire_date_list[i]  # Dec 18, 2020 format
            expire_date = datetime.datetime.strptime(expire_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

            item_obj = PurchaseItems()

            medicine_obj = Medicine.objects.get(pk=medicine_list[i])
            leaf_obj = Leaf.objects.get(id=leaf_type_list[i])

            batch, created = Batch.objects.get_or_create(medicine=medicine_obj, batch_number=batch_id_list[i])

            batch.expiry_date = expire_date
            batch.box_pattern = leaf_obj
            batch.box_quantity = box_quantity_list[i]
            batch.previous_stock = batch.batch_stock
            batch.batch_stock += int(product_quantity_list[i])
            batch.save()

            item_obj.order = purchase_obj
            item_obj.batch = batch
            item_obj.save()

        messages.success(request, 'Purchase Added Successfully. ')
        return redirect('purchase:purchase-list')


class PurchaseList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        purchases = Purchase.objects.filter(is_active=True)

        total_purchases = 0
        for purchase in purchases:
            total_purchases += purchase.grand_total

        context = {
            'purchases': purchases,
            'total_purchases': total_purchases,
        }
        return render(request, 'purchase/purchase_list.html', context)


class UpdatePurchase(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, purchase_id):
        purchase_obj = Purchase.objects.get(id=purchase_id)
        manufacturers = Manufacturer.objects.filter(is_active=True)
        leafs = Leaf.objects.all()

        context = {
            'object': purchase_obj,
            'manufacturers': manufacturers,
            'payment_types': list(PAYMENT_TYPES),
            'banks': list(BANK_CHOICES),
            'items': purchase_obj.purchaseitems_set.filter(is_active=True),
            'leafs': leafs,
        }
        return render(request, 'purchase/update_purchase.html', context)

    def post(self, request, purchase_id):
        data = request.POST

        manufacturer_id = data.get('manufacturer_id')
        manufacturer_obj = Manufacturer.objects.get(id=manufacturer_id)

        purchase_date = request.POST.get('date')  # Dec 18, 2020

        try:
            purchase_date = datetime.datetime.strptime(purchase_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        except:
            purchase_date = purchase_date

        details = data.get('details', '')
        invoice_no = data.get('invoice_no')
        payment_type = data.get('payment_type')
        bank_id = data.get('bank_id')

        medicine_list = data.getlist('medicine_name[]')
        batch_id_list = data.getlist('batch_id[]')
        expire_date_list = data.getlist('expire_date[]')
        leaf_type_list = data.getlist('leaf_type[]')
        box_quantity_list = data.getlist('box_quantity[]')
        product_quantity_list = data.getlist('product_quantity[]')
        items_id_list = data.getlist('items[]')

        vat = data.get('vat')
        discount = data.get('discount')
        paid_amount = data.get('paid_amount')

        purchase_obj = Purchase.objects.get(id=purchase_id)
        purchase_obj.manufacturer = manufacturer_obj
        purchase_obj.date = purchase_date
        purchase_obj.invoice = invoice_no
        purchase_obj.details = details
        purchase_obj.payment_types = payment_type
        purchase_obj.bank = bank_id if bank_id else None
        purchase_obj.vat = vat if vat else 0
        purchase_obj.discount = discount if discount else 0
        purchase_obj.paid_amount = paid_amount if paid_amount else 0
        purchase_obj.save()

        # Updating Existing Objects
        for index, item_id in enumerate(items_id_list):
            expire_date = expire_date_list[index]
            try:
                expire_date = datetime.datetime.strptime(expire_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
            except:
                expire_date = expire_date

            item_obj = PurchaseItems.objects.get(id=int(item_id))
            batch_obj = item_obj.batch

            medicine_obj = Medicine.objects.get(pk=medicine_list[index])
            leaf_obj = Leaf.objects.get(id=leaf_type_list[index])

            batch_obj.medicine = medicine_obj
            batch_obj.box_pattern = leaf_obj
            batch_obj.box_quantity = float(box_quantity_list[index])
            batch_obj.batch_number = batch_id_list[index]
            batch_obj.batch_stock = int(float(product_quantity_list[index]))
            batch_obj.expiry_date = expire_date
            batch_obj.save()
            item_obj.save()

        updated_batches = len(items_id_list)

        if len(medicine_list) > updated_batches:

            # Saving New Purchase Items
            for i in range(updated_batches, len(medicine_list)):  # loop will execute number of rows times
                expire_date = expire_date_list[updated_batches]  # Dec 18, 2020

                try:
                    expire_date = datetime.datetime.strptime(expire_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
                except:
                    expire_date = expire_date

                batch = Batch()
                item_obj = PurchaseItems()

                medicine_obj = Medicine.objects.get(pk=medicine_list[updated_batches])
                leaf_obj = Leaf.objects.get(id=leaf_type_list[updated_batches])

                batch.box_pattern = leaf_obj
                batch.box_quantity = float(box_quantity_list[updated_batches])
                batch.batch_stock = int(float(product_quantity_list[updated_batches]))
                batch.medicine = medicine_obj
                batch.batch_number = batch_id_list[updated_batches]
                batch.expiry_date = expire_date
                batch.save()

                item_obj.order = purchase_obj
                item_obj.batch = batch
                item_obj.save()

        messages.success(request, 'Purchase Updated Successfully. ')
        return redirect('purchase:purchase-list')


class RemovePurchase(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, purchase_id):
        purchase_obj = Purchase.objects.get(id=purchase_id)
        purchase_obj.is_active = False

        for item in purchase_obj.purchase_items:
            item.batch.batch_stock -= item.batch.total_quantity
            item.batch.save()

        purchase_obj.save()

        messages.success(request, 'Purchase Removed Successfully. ')
        return redirect('purchase:purchase-list')


class ViewPurchase(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, purchase_id):
        purchase_obj = Purchase.objects.get(id=purchase_id)
        company = Setting.objects.first()
        items = purchase_obj.purchase_items # property

        context = {
            'object': purchase_obj,
            'company': company,
            'items': items,
        }
        return render(request, 'purchase/view_purchase.html', context)


# Ajax Calls
class FetchMedicines(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        manufacturer_id = request.GET.get('manufacturer_id')
        manufacturer_obj = Manufacturer.objects.get(id=manufacturer_id)

        medicines = manufacturer_obj.medicine_set.filter(is_active=True)
        id_name_strengths = dict()

        for index, medicine in enumerate(medicines):
            id = medicine.id
            name = medicine.medicine_name
            strength = medicine.strength

            info = {
                'id': id, 'name': name, 'strength': strength,
            }

            id_name_strengths[index] = info

        data = id_name_strengths
        print(data)

        return JsonResponse(data, safe=False)


class FetchPrice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        medicine_id = request.GET.get('medicine_id')
        medicine_obj = Medicine.objects.get(id=medicine_id)

        data = {
            'manufacturer_price': medicine_obj.manufacturer_price,
            'box_price': medicine_obj.price,
            'stock': medicine_obj.total_stock,
            'vat': medicine_obj.vat,
        }

        return JsonResponse(data, safe=False)


class FetchQuantity(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        leaf_id = request.GET.get('leaf_id')
        leaf_obj = Leaf.objects.get(id=leaf_id)

        data = {
            'number_per_box': leaf_obj.number_per_box
        }
        return JsonResponse(data)


class RemovePurchaseItem(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        item_id = request.GET.get('item_id')

        item_obj = PurchaseItems.objects.get(id=item_id)
        item_obj.is_active = False
        item_obj.save()

        item_obj.batch.is_active = False  # Deleting the batch.
        item_obj.batch.save()

        context = {
            'deleted': 'Successful'
        }

        return JsonResponse(context)
