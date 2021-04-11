import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from customer.models import Customer
from invoice.models import Invoice, InvoiceItems
from medicine.models import Medicine, Batch
from purchase.models import PAYMENT_TYPES, BANK_CHOICES
from settings.models import Setting
from system.utils import random_id_generator


class AddInvoice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        medicines = Medicine.objects.filter(is_active=True)
        current_invoice = 1000 + Invoice.objects.all().count() + 1
        customers = Customer.objects.filter(is_active=True)

        context = {
            'payment_types': list(PAYMENT_TYPES),
            'bank_choices': list(BANK_CHOICES),
            'medicines': medicines,
            'current_invoice': current_invoice,
            'customers': customers,
        }
        return render(request, 'invoice/add_invoice.html', context)

    def post(self, request):
        data = request.POST

        customer_id = data.get('customer')
        customer_obj = Customer.objects.get(id=customer_id)

        date = data.get('date')
        date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        invoice_no = data.get('invoice_no')
        details = data.get('details')
        payment_type = data.get('payment_type')
        bank_id = data.get('bank_id')

        medicine_ids_list = data.getlist('medicine_id[]')
        batch_ids_list = data.getlist('batch_id[]')
        sell_quantity_list = data.getlist('product_quantity[]')
        product_rate_list = data.getlist('product_rate[]')
        discount_list = data.getlist('discount[]')

        invoice_discount = data.get('invoice_discount') if data.get('invoice_discount') else 0
        total_vat = data.get('total_tax_amount') if data.get('total_tax_amount') else 0
        paid_amount = data.get('paid_amount') if data.get('paid_amount') else 0

        invoice_id = random_id_generator(module='Invoice')

        invoice_obj = Invoice(customer=customer_obj, date=date, invoice_number=invoice_no,
                              invoice_id=invoice_id, details=details, payment_types=payment_type,
                              bank=bank_id if bank_id != 'default' else None, invoice_discount=invoice_discount,
                              total_vat=total_vat, paid_amount=paid_amount)
        invoice_obj.save()


        # Saving InvoiceItems
        for i in range(len(medicine_ids_list)):

            batch_id = batch_ids_list[i]
            batch_obj = Batch.objects.get(id=batch_id)

            item_obj = InvoiceItems(batch=batch_obj, sell_quantity=sell_quantity_list[i] if sell_quantity_list[i] else 0,
                                    price=product_rate_list[i] if product_rate_list[i] else 0,
                                    discount=discount_list[i] if discount_list[i] else 0)

            item_obj.invoice = invoice_obj
            item_obj.save()

        # Calculating Customer's Current Balance

        if customer_obj.name == "Walking Customer":
            # No calculation needed for Walking Customers.
            pass
        else:
            customer_obj.previous_balance = customer_obj.current_balance
            if float(invoice_obj.due_amount) > 0:
                customer_obj.current_balance = float(invoice_obj.due_amount)
            else:
                if invoice_obj.change > 0:
                    customer_obj.current_balance = invoice_obj.change * -1
                else:
                    customer_obj.current_balance = invoice_obj.change

            # Changing Customer Status
            status = 2 if float(customer_obj.current_balance) > 0 else 1
            customer_obj.status = status
            customer_obj.save()

        messages.success(request, 'Invoice Added Successfully. ')
        return redirect('invoice:add-invoice')


class InvoiceList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        invoices = Invoice.objects.filter(is_active=True)

        all_invoice_total = 0
        for invoice in invoices:
            all_invoice_total += invoice.net_total

        context = {
            'invoices': invoices,
            'invoices_total': all_invoice_total,
        }

        return render(request, 'invoice/invoice_list.html', context)


class EditInvoice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, invoice_id):
        invoice_obj = Invoice.objects.get(id=invoice_id)
        medicines = Medicine.objects.filter(is_active=True)
        customers = Customer.objects.filter(is_active=True)
        invoice_items = invoice_obj.invoiceitems_set.filter(is_active=True)

        context = {
            'object': invoice_obj,
            'payment_types': list(PAYMENT_TYPES),
            'bank_choices': list(BANK_CHOICES),
            'medicines': medicines,
            'customers': customers,
            'invoice_items': invoice_items,

        }

        return render(request, 'invoice/update_invoice.html', context)

    def post(self, request, invoice_id):
        invoice_obj = Invoice.objects.get(id=invoice_id)

        data = request.POST
        customer_id = data.get('customer')
        customer_obj = Customer.objects.get(id=customer_id)

        date = data.get('date')
        try:
            date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        except:
            date = invoice_obj.date

        invoice_no = data.get('invoice_no')
        details = data.get('details')
        payment_type = data.get('payment_type')
        bank_id = data.get('bank_id')

        medicine_ids_list = data.getlist('medicine_id[]')
        batch_ids_list = data.getlist('batch_id[]')
        sell_quantity_list = data.getlist('product_quantity[]')
        product_rate_list = data.getlist('product_rate[]')
        discount_list = data.getlist('discount[]')
        item_ids_list = data.getlist('items[]')

        invoice_discount = data.get('invoice_discount') if data.get('invoice_discount') else 0
        total_vat = data.get('total_tax_amount') if data.get('total_tax_amount') else 0

        paid_amount = data.get('paid_amount') if data.get('paid_amount') else 0

        invoice_obj.customer = customer_obj
        invoice_obj.date = date
        invoice_obj.invoice_number = invoice_no
        invoice_obj.details = details
        invoice_obj.payment_types = payment_type
        invoice_obj.bank = bank_id if bank_id != 'default' else None
        invoice_obj.invoice_discount = float(invoice_discount)
        invoice_obj.total_vat = total_vat
        invoice_obj.paid_amount = paid_amount
        invoice_obj.save()

        updated_items = len(item_ids_list)

        # Updating Existing Items
        for index, item_id in enumerate(item_ids_list):

            batch_obj = Batch.objects.get(id=int(batch_ids_list[index]))

            item_obj = InvoiceItems.objects.get(id=int(item_id))
            item_obj.sell_quantity = sell_quantity_list[index]
            item_obj.discount = discount_list[index]
            item_obj.batch = batch_obj
            item_obj.price = product_rate_list[index]
            item_obj.save()

        if len(medicine_ids_list) > updated_items:
            # Adding New InvoiceItems
            for i in range(updated_items, len(medicine_ids_list)):
                batch_id = batch_ids_list[i]
                batch_obj = Batch.objects.get(id=batch_id)

                item_obj = InvoiceItems(batch=batch_obj,
                                        sell_quantity=sell_quantity_list[i] if sell_quantity_list[i] else 0,
                                        price=product_rate_list[i] if product_rate_list[i] else 0,
                                        discount=discount_list[i] if discount_list[i] else 0)

                item_obj.invoice = invoice_obj
                item_obj.save()

                # Rechecking Quantity
                if batch_obj.sold_quantity > batch_obj.batch_stock:
                    item_obj.delete()
                    messages.info(request, "PURCHASE ERROR! Recheck Quantity.")
                    return redirect('invoice:edit-invoice', invoice_id=invoice_id)

        # Calculating Customer's Current Balance
        if customer_obj.name == "Walking Customer":
            # No calculation needed for Walking Customers.
            pass
        else:
            if float(invoice_obj.due_amount) > 0:
                customer_obj.current_balance = float(invoice_obj.due_amount)
            else:
                if invoice_obj.change > 0:
                    customer_obj.current_balance = invoice_obj.change * -1
                else:
                    customer_obj.current_balance = invoice_obj.change

            # Changing Customer Status
            status = 2 if float(customer_obj.current_balance) > 0 else 1
            customer_obj.status = status
            customer_obj.save()

        messages.success(request, 'Invoice Updated Successfully. ')
        return redirect('invoice:edit-invoice', invoice_id=invoice_id)


class RemoveInvoice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, invoice_id):
        invoice_obj = Invoice.objects.get(id=invoice_id)
        invoice_obj.is_active = False
        invoice_obj.save()

        # for item in invoice_obj.invoiceitems_set.filter(is_active=True):
        #     item.batch.batch_stock -= item.sell_quantity
        #     item.batch.save()

        messages.success(request, 'Invoice Removed Successfully. ')
        return redirect('invoice:invoice-list')


class ViewInvoice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, invoice_id):
        invoice_obj = Invoice.objects.get(invoice_id=int(invoice_id))
        company = Setting.objects.last()

        context = {
            'object': invoice_obj,
            'company': company,
        }
        return render(request, 'invoice/view_invoice.html', context)



# Ajax calls
class FetchMedicineInfo(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        medicine_id = request.GET.get('medicine_id')
        medicine_obj = Medicine.objects.get(id=medicine_id)

        batches = dict()
        for batch in medicine_obj.batch_set.filter(is_active=True):
            batches[batch.id] = batch.batch_number

        context = {
            'id': medicine_obj.id,
            'total_stock': medicine_obj.total_stock,
            'batches': batches,
            'unit': medicine_obj.unit.name,
            'price_of_one': medicine_obj.price_one,
            'vat': medicine_obj.vat,
        }
        # print(context)
        return JsonResponse(context)


class FetchBatch(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        batch_id = request.GET.get('batch_id')

        batch_obj = Batch.objects.get(id=batch_id)

        context = {
            'id': batch_obj.id,
            'expiry_date': batch_obj.expiry_date,
            'batch_stock': batch_obj.current_stock,
        }
        # print(context)
        return JsonResponse(context)


class FetchCustomer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        customer_id = request.GET.get('customer_id')
        customer_obj = Customer.objects.get(id=customer_id)
        context = {
            'balance': customer_obj.current_balance,
        }

        return JsonResponse(context)


class FetchBatchList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        medicine_id = request.GET.get('medicine_id')
        medicine_obj = Medicine.objects.get(id=medicine_id)

        context = dict()

        for index, batch in enumerate(medicine_obj.batch_set.filter(is_active=True)):
            id = batch.id
            batch_number = batch.batch_number
            stock = batch.current_stock
            info = {'id': id, 'batch_number': batch_number, 'available': stock}

            context[index] = info

        print(context)

        return JsonResponse(context)


class RemoveInvoiceItem(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        item_id = request.GET.get('item_id')
        item_obj = InvoiceItems.objects.get(id=int(item_id))

        # line_total & net_total is required for calculating customer's current balance
        invoice_object = item_obj.invoice  # Parent Class
        customer_object = invoice_object.customer
        line_total = float(item_obj.total_bill_exclude_vat)
        net_total = float(invoice_object.net_total) - line_total

        item_obj.is_active = False
        item_obj.batch.sold_quantity -= item_obj.sell_quantity
        item_obj.batch.save()
        item_obj.save()

        # Recalculating Customer Balance
        if customer_object.name == 'Walking Customer':
            # No calculation needed for Walking Customer
            pass
        else:

            paid_amount = float(invoice_object.paid_amount)
            change = net_total - paid_amount

            if change > 0:
                customer_object.current_balance = change * -1
            else:
                customer_object.current_balance = change

            # Changing Customer Status
            status = 2 if float(customer_object.current_balance) > 0 else 1
            customer_object.status = status
            customer_object.save()

        context = {
            'deleted': 'Successful'
        }

        return JsonResponse(context)
