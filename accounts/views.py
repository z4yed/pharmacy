import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from purchase.models import PAYMENT_TYPES, BANK_CHOICES
from manufacturer.models import Manufacturer
from accounts.models import ManufacturerPayment as MP


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