import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from customer.models import Customer
from purchase.models import PAYMENT_TYPES, BANK_CHOICES
from manufacturer.models import Manufacturer
from accounts.models import ManufacturerPayment as MP, CustomerReceipt as CR
from system.utils import render_mp_pdf_view, render_cr_pdf_view


class ManufacturerPayment(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        manufacturers = Manufacturer.objects.filter(is_active=True)
        all_payments = MP.objects.count()

        context = {
            'manufacturers': manufacturers,
            'payment_types': list(PAYMENT_TYPES),
            'banks': list(BANK_CHOICES),
            'next_voucher': all_payments+1,
        }
        return render(request, 'accounts/manufacturer_payment.html', context)

    def post(self, request):
        voucher_no = request.POST.get('txtVNo')
        date = request.POST.get('dtpDate')
        date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        manufacturer_id = request.POST.get('manufacturer_id')
        amount = request.POST.get('txtAmount')
        payment_type = request.POST.get('payment_type')
        bank = request.POST.get('bank_id')
        note = request.POST.get('txtRemarks', '')

        manufacturer_obj = Manufacturer.objects.get(id=manufacturer_id)

        obj = MP(voucher_no=voucher_no, date=date, manufacturer=manufacturer_obj, amount=amount,
                 payment_type=payment_type, remarks=note)
        obj.bank = bank if bank else None
        obj.save()

        manufacturer_obj.previous_balance -= float(amount)
        manufacturer_obj.save()

        messages.success(request, f'BDT: {amount} paid Successfully to Manufacturer: {manufacturer_obj.name}')
        return redirect('accounts:manufacturer_payment')


class PaymentList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        payments = MP.objects.filter(is_active=True)
        total_payments = 0

        context = {
            'payments': payments,
            'total_payments': total_payments,
        }
        return render(request, 'accounts/manufacturer_payment_list.html', context)


class PrintPaymentInvoice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, payment_id):
        response = render_mp_pdf_view(payment_id)
        return response


class RemovePayment(View):
    pass


class CustomerReceipt(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        customers = Customer.objects.filter(is_active=True)
        all_receipts = CR.objects.count()

        context = {
            'customers': customers,
            'payment_types': list(PAYMENT_TYPES),
            'banks': list(BANK_CHOICES),
            'next_voucher': all_receipts + 1,
        }
        return render(request, 'accounts/customer_receipt.html', context)

    def post(self, request):
        voucher_no = request.POST.get('txtVNo')
        date = request.POST.get('dtpDate')
        date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        customer_id = request.POST.get('customer_id')
        amount = request.POST.get('txtAmount')
        payment_type = request.POST.get('payment_type')
        bank = request.POST.get('bank_id')
        note = request.POST.get('txtRemarks', '')

        customer_obj = Customer.objects.get(id=customer_id)

        obj = CR(voucher_no=voucher_no, date=date, customer=customer_obj, amount=amount,
                 payment_type=payment_type, remarks=note)

        obj.bank = bank if bank else None
        obj.save()

        customer_obj.current_balance -= float(amount)
        customer_obj.save()

        messages.success(request, f'BDT: {amount} Received Successfully from : {customer_obj.name}')
        return redirect('accounts:customer_receipt')


class ReceiptList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        receipts = CR.objects.filter(is_active=True)

        context = {
            'receipts': receipts
        }
        return render(request, 'accounts/customer_receipt_list.html', context)


class PrintReceiptInvoice(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, receipt_id):
        response = render_cr_pdf_view(receipt_id)
        return response

