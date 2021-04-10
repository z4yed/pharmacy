from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View

from invoice.models import Invoice, InvoiceItems
from medicine.models import Batch
from purchase.models import Purchase

from .models import InvoiceReturn as IRModel, PurchaseReturn as PRModel, InvoiceReturnItems as IRItems, PurchaseReturnItems as PRItems
from django.utils import timezone


class ReturnHome(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = dict()
        return render(request, 'return/return_home.html', context)

    def post(self, request):
        pass


class InvoiceReturnList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        returned_invoices = IRModel.objects.filter(is_active=True)

        context = {
            'invoices': returned_invoices,
        }

        return render(request, 'return/invoice_return_list.html', context)


class PurchaseReturnList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        returned_purchases = PRModel.objects.filter(is_active=True)

        context = {
            'purchases': returned_purchases,
        }

        return render(request, 'return/purchase_return_list.html', context)


class WastageList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = dict()
        pass


class InvoiceReturn(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        invoice_no = request.GET.get('invoice_no')

        try:
            invoice_obj = Invoice.objects.get(invoice_number=invoice_no)
        except:
            messages.info(request, "Invoice doesn't exists. ")
            return redirect('return:return-home')

        context = {
            'object': invoice_obj,
        }
        return render(request, 'return/invoice_return.html', context)

    def post(self, request):
        data = request.POST
        invoice_number = data.get('invoice_number')
        invoice_obj = Invoice.objects.get(invoice_number=invoice_number)

        details = data.get('details', '')
        wastage = data.get('wastage')

        invoice_return_obj = IRModel(invoice=invoice_obj, details=details, return_date=timezone.now().date())
        invoice_return_obj.wastage = True if wastage == '1' else False
        invoice_return_obj.save()

        batch_id_list = data.getlist('batch_ids[]')
        return_quantity_list = data.getlist('return_qty[]')
        deductions_list = data.getlist('deductions[]')
        invoice_items_list = data.getlist('invoice_items_ids[]')

        for i in range(len(batch_id_list)):
            batch_obj = Batch.objects.get(id=int(batch_id_list[i]))
            invoice_item = InvoiceItems.objects.get(id=int(invoice_items_list[i]))
            return_quantity = int(return_quantity_list[i]) if return_quantity_list[i] else 0
            deduction = float(deductions_list[i]) if deductions_list[i] else 0  # value might be ''

            return_items = IRItems(order=invoice_return_obj, batch=batch_obj, item=invoice_item, return_quantity=return_quantity, deduction=deduction)
            return_items.save()

        messages.success(request, 'Return Added Successfully. ')
        return redirect('return:return-home')


class PurchaseReturn(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        purchase_id = request.GET.get('purchase_id')

        try:
            purchase_obj = Purchase.objects.get(purchase_id=purchase_id)
        except:
            messages.info(request, "Purchase doesn't Exists.")
            return redirect('return:return-home')

        context = {
            'object': purchase_obj,
        }
        return render(request, 'return/purchase_return.html', context)

    def post(self, request):
        pass