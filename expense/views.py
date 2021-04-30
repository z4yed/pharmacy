import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

from expense.models import ExpenseItem, Expense
from purchase.models import PAYMENT_TYPES, BANK_CHOICES


class ExpenseItemList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        items = ExpenseItem.objects.filter(is_active=True)
        context = {
            'items': items
        }
        return render(request, 'expense/expense_items_list.html', context)



class AddExpenseItem(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        name = request.POST.get('item_name')
        obj = ExpenseItem(name=name)
        obj.save()

        messages.success(request, "Expense Item Added Successfully. ")
        return redirect('expense:expense_items')


class UpdateExpenseItem(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, item_id):  # used to remove Expense Item
        item_obj = ExpenseItem.objects.get(id=item_id)
        item_obj.is_active = False
        item_obj.save()

        messages.success(request, 'Item Removed Successfully. ')
        return redirect('expense:expense_items')

    def post(self, request, item_id):
        data = request.POST
        name = data.get('item_name')

        item_obj = ExpenseItem.objects.get(id=item_id)
        item_obj.name = name
        item_obj.save()

        messages.success(request, 'Item Updated Successfully. ')
        return redirect('expense:expense_items')


class ExpenseList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        expenses = Expense.objects.filter(is_active=True)
        context = {
            'expenses': expenses
        }
        return render(request, 'expense/expense_list.html', context)

    def post(self, request):
        pass


class AddExpense(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        expense_items = ExpenseItem.objects.filter(is_active=True)
        context = {
            'payment_types': list(PAYMENT_TYPES),
            'banks': list(BANK_CHOICES),
            'expense_items': expense_items,
        }

        return render(request, 'expense/add_expense.html', context)

    def post(self, request):
        data = request.POST
        date = data.get('dtpDate')
        date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        expense_type = data.get('expense_type')
        item_obj = ExpenseItem.objects.get(id=expense_type)

        payment_type = data.get('payment_type')
        bank = data.get('bank_id')
        amount = data.get('amount')
        note = data.get('note', '')

        expense_obj = Expense(date=date, expense_type=item_obj, payment_type=payment_type, amount=float(amount),
                              remarks=note)
        if bank:
            expense_obj.bank = bank
        expense_obj.save()

        messages.success(request, 'Expense Added Successfully. ')
        return redirect('expense:expense_list')


class UpdateExpense(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, expense_id):  # used to remove Expense Item
        expense_obj = Expense.objects.get(id=expense_id)
        expense_obj.is_active = False
        expense_obj.save()

        messages.success(request, 'Expense Removed Successfully. ')
        return redirect('expense:expense_list')

    def post(self, request, item_id):  # not required
        pass
