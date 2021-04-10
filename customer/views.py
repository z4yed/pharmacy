from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from customer.models import Customer


class AddCustomer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {

        }
        return render(request, 'customer/add_customer.html', context)

    def post(self, request):
        if request.method == "POST":
            data = request.POST
            customer_name = data.get('customer_name')
            customer_mobile = data.get('customer_mobile')
            first_email = data.get('first_email', '')
            second_email = data.get('second_email', '')
            phone = data.get('phone', '')
            contact = data.get('contact', '')
            first_address = data.get('first_address', '')
            second_address = data.get('second_address', '')
            fax = data.get('fax', '')
            city = data.get('city', '')
            state = data.get('state', '')
            zip_code = data.get('zip', '')
            country = data.get('country', '')
            current_balance = data.get('previous_balance')

            status = 2 if float(current_balance) > 0 else 1

            customer_object = Customer(name=customer_name, mobile_number=customer_mobile, first_email=first_email,
                                       second_email=second_email, phone=phone, contact=contact, first_address=first_address,
                                       second_address=second_address, fax=fax, city=city, state=state, zip=zip_code,
                                       country=country, current_balance=current_balance, status=status)

            messages.success(request, "Customer Added Successfully. ")
            customer_object.save()
            return redirect('customer:add-customer')


class CustomerList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        customers = Customer.objects.filter(is_active=True)
        total_bills = customers.aggregate(Sum('current_balance'))['current_balance__sum']

        context = {
            'customers': customers,
            'total_bills': total_bills,
            'category': 'Customers List',
        }
        return render(request, 'customer/customer_list.html', context)

    def post(self, request):
        pass


class EditCustomer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, customer_id):
        customer_obj = get_object_or_404(Customer, pk=int(customer_id))
        context = {
            'customer': customer_obj
        }
        return render(request, 'customer/edit_customer.html', context)

    def post(self, request, customer_id):
        customer_obj = get_object_or_404(Customer, pk=int(customer_id))
        if request.method == "POST":
            data = request.POST
            customer_name = data.get('customer_name')
            customer_mobile = data.get('customer_mobile')
            first_email = data.get('first_email', '')
            second_email = data.get('second_email', '')
            phone = data.get('phone', '')
            contact = data.get('contact', '')
            first_address = data.get('first_address', '')
            second_address = data.get('second_address', '')
            fax = data.get('fax', '')
            city = data.get('city', '')
            state = data.get('state', '')
            zip_code = data.get('zip', '')
            country = data.get('country', '')
            current_balance = data.get('previous_balance')

            status = 2 if float(current_balance) > 0 else 1

            customer_obj.name = customer_name
            customer_obj.mobile_number = customer_mobile
            customer_obj.first_email = first_email
            customer_obj.second_email = second_email
            customer_obj.phone = phone
            customer_obj.contact = contact
            customer_obj.first_address = first_address
            customer_obj.second_address = second_address
            customer_obj.fax = fax
            customer_obj.city = city
            customer_obj.state = state
            customer_obj.zip = zip_code
            customer_obj.country = country
            customer_obj.current_balance = current_balance
            customer_obj.status = status
            messages.success(request, "Customer Updated Successfully. ")
            customer_obj.save()

            return redirect('customer:edit-customer', customer_id=customer_id)


class RemoveCustomer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, customer_id):
        customer_obj = get_object_or_404(Customer, pk=customer_id)
        customer_obj.is_active = False
        customer_obj.save()
        messages.success(request, 'Customer Deleted Successfully. ')
        return redirect('customer:customer-list')


class PaidCustomer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        paid_customers = Customer.objects.filter(status=1, is_active=True)
        total_bills = paid_customers.aggregate(Sum('previous_balance'))['previous_balance__sum']
        context = {
            'customers': paid_customers,
            'category': 'Paid Customers',
            'total_bills': total_bills,
        }
        return render(request, 'customer/customer_list.html', context)


class CreditCustomer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        credit_customers = Customer.objects.filter(status=2, is_active=True)
        total_bills = credit_customers.aggregate(Sum('previous_balance'))['previous_balance__sum']
        context = {
            'customers': credit_customers,
            'category': 'Credit Customers',
            'total_bills': total_bills,
        }
        return render(request, 'customer/customer_list.html', context)
