from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View

from bank.models import Bank


class BankList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        banks = Bank.objects.filter(is_active=True)
        context = {
            'banks': banks,
        }
        return render(request, 'bank/bank_list.html', context)


class AddBank(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {

        }
        return render(request, 'bank/add_bank.html', context)

    def post(self, request):
        data = request.POST
        bank_name = data.get('bank_name')
        ac_name = data.get('ac_name')
        ac_number = data.get('ac_number')
        branch = data.get('branch')
        signature = request.FILES.get('signature')
        status = data.get('status')

        active = True if status == '1' else False

        bank_exists = Bank.objects.filter(name__iexact=bank_name).exists()
        account_exists = Bank.objects.filter(account_number__iexact=ac_number).exists()

        if bank_exists or account_exists:
            messages.warning(request, 'Bank Name & Account Number must be unique. ')
            return redirect('bank:add-bank')

        else:
            obj = Bank(name=bank_name, account_name=ac_name, account_number=ac_number, branch=branch, is_active=active)
            if signature:
                obj.signature = signature
            obj.save()
            messages.success(request, 'Bank Added Successfully. ')

        return redirect('bank:bank-list')


class UpdateBank(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, bank_id):
        bank_obj = Bank.objects.get(id=bank_id)
        context = {
            'object': bank_obj
        }
        return render(request, 'bank/update_bank.html', context)

    def post(self, request, bank_id):
        data = request.POST
        bank_name = data.get('bank_name')
        ac_name = data.get('ac_name')
        ac_number = data.get('ac_number')
        branch = data.get('branch')
        signature = request.FILES.get('signature')
        status = data.get('status')

        active = True if status == '1' else False

        bank_obj = Bank.objects.get(id=bank_id)

        """
           Bank Name & Account  Number must be unique. 
           Admin can't update bank name if the bank name is already assigned to another person. 
           Admin can't update account number if the account number is already assigned to another person. 
                    
        """

        bank_exists = account_exists = ''

        if bank_obj.name.lower() != bank_name.lower():
            bank_exists = Bank.objects.filter(name__iexact=bank_name).exists()

        if bank_obj.account_number != ac_number:
            account_exists = Bank.objects.filter(account_number__iexact=ac_number).exists()

        if bank_exists or account_exists:
            messages.warning(request, 'Bank Name & Account Number must be unique. ')

        else:
            bank_obj.name = bank_name
            bank_obj.account_name = ac_name
            bank_obj.account_number = ac_number
            bank_obj.branch = branch
            if signature:
                bank_obj.signature = signature
            bank_obj.is_active = active
            bank_obj.save()
            messages.success(request, "Bank Updated Successfully. ")

        return redirect('bank:update-bank', bank_id=bank_id)


class RemoveBank(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, bank_id):
        bank_obj = Bank.objects.get(id=bank_id)
        bank_obj.is_active = False
        bank_obj.save()

        messages.success(request, "Bank Removed Successfully. ")
        return redirect('bank:bank-list')
