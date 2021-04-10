from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View

from employee.models import Designation, Employee, RATE_TYPE


class DesignationList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        designations = Designation.objects.filter(is_active=True)

        context = {
            'designations': designations,
        }

        return render(request, 'employee/designation_list.html', context)


class AddDesignation(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        name = request.POST.get('designation_name')
        details = request.POST.get('details')

        obj = Designation(name=name, details=details)
        obj.save()

        messages.success(request, 'Designation Added Successfully. ')
        return redirect('employee:designation_list')


class UpdateDesignation(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, designation_id):
        obj = Designation.objects.get(id=designation_id)

        name = request.POST.get('designation_name')
        details = request.POST.get('details')

        obj.name = name
        obj.details = details
        obj.save()

        messages.success(request, 'Designation Updated Successfully. ')
        return redirect('employee:designation_list')


class RemoveDesignation(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, designation_id):
        obj = Designation.objects.get(id=designation_id)
        obj.is_active = False
        obj.save()

        messages.success(request, 'Designation Removed Successfully. ')
        return redirect('employee:designation_list')


class EmployeeList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        employees = Employee.objects.filter(is_active=True)
        context = {
            'employees': employees,
        }
        return render(request, 'employee/employee_list.html', context)


class AddEmployee(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        designations = Designation.objects.filter(is_active=True)

        context = {
            'rate_types': list(RATE_TYPE),
            'designations': designations,
        }

        return render(request, 'employee/add_employee.html', context)

    def post(self, request):
        data = request.POST
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        designation_id = data.get('designation_id')
        phone = data.get('emp_phone')
        rate_type = data.get('rate_type')
        hrate = data.get('hrate')
        email = data.get('email')
        blood_group = data.get('blood_group', '')
        address_line_1 = data.get('address_line_1', '')
        address_line_2 = data.get('address_line_2', '')
        country = data.get('country', '')
        image = request.FILES.get('image')
        city = data.get('city', '')
        zip_code = data.get('zip', '')
        status = data.get('status')

        designation_obj = Designation.objects.get(id=designation_id)

        employee_obj = Employee(first_name=firstname, last_name=lastname, designation=designation_obj,
                                phone=phone, rate_type=rate_type, salary=hrate, email=email, blood_group=blood_group,
                                first_address=address_line_1, second_address=address_line_2,
                                country=country, city=city, zip_code=zip_code)
        if image:
            employee_obj.image = image
        employee_obj.is_active = True if status == '1' else False
        employee_obj.save()

        messages.success(request, 'Employee Added Successfully. ')
        return redirect('employee:employee_list')


class UpdateEmployee(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, employee_id):
        employee_obj = Employee.objects.get(id=employee_id)
        context = {
            'object': employee_obj,
            'rate_types': list(RATE_TYPE),
            'designations': Designation.objects.filter(is_active=True),
        }
        return render(request, 'employee/update_employee.html', context)

    def post(self, request, employee_id):
        employee_obj = Employee.objects.get(id=employee_id)

        data = request.POST
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        designation_id = data.get('designation_id')
        phone = data.get('emp_phone')
        rate_type = data.get('rate_type')
        hrate = data.get('hrate')
        email = data.get('email')
        blood_group = data.get('blood_group', '')
        address_line_1 = data.get('address_line_1', '')
        address_line_2 = data.get('address_line_2', '')
        country = data.get('country', '')
        image = request.FILES.get('image')
        city = data.get('city', '')
        zip_code = data.get('zip', '')
        status = data.get('status')

        designation_obj = Designation.objects.get(id=designation_id)

        # Updating Employee Object
        employee_obj.first_name = firstname
        employee_obj.last_name = lastname
        employee_obj.designation = designation_obj
        employee_obj.phone = phone
        employee_obj.rate_type = rate_type
        employee_obj.salary = hrate
        employee_obj.blood_group = blood_group
        employee_obj.email = email
        employee_obj.second_address = address_line_2
        employee_obj.first_address = address_line_1
        employee_obj.city = city
        employee_obj.country = country
        employee_obj.zip_code = zip_code

        if image:
            employee_obj.image = image
        employee_obj.is_active = True if status == '1' else False
        employee_obj.save()

        messages.success(request, 'Employee Updated Successfully. ')
        return redirect('employee:update_employee', employee_id=employee_id)


class RemoveEmployee(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, employee_id):
        employee_obj = Employee.objects.get(id=employee_id)
        employee_obj.is_active = False
        employee_obj.save()

        messages.success(request, 'Employee Removed Successfully. ')
        return redirect('employee:employee_list')

