import csv
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Manufacturer, CSV


class AddManufacturer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {

        }
        return render(request, 'manufacturer/add_manufacturer.html', context)

    def post(self, request):
        if request.method == "POST":
            data = request.POST
            manufacture_name = data.get('manufacturer_name')
            customer_mobile = data.get('manufacturer_mobile')
            first_email = data.get('first_email') if data.get('first_email') else ''
            second_email = data.get('second_email') if data.get('second_email') else ''
            phone = data.get('phone') if data.get('phone') else ''
            contact = data.get('contact') if data.get('contact') else ''
            first_address = data.get('first_address') if data.get('first_address') else ''
            second_address = data.get('second_address') if data.get('second_address') else ''
            fax = data.get('fax') if data.get('fax') else ''
            city = data.get('city') if data.get('city') else ''
            state = data.get('state') if data.get('state') else ''
            zip_code = data.get('zip') if data.get('zip') else ''
            country = data.get('country') if data.get('country') else ''
            previous_balance = data.get('previous_balance')

            manufacture_obj = Manufacturer(name=manufacture_name, mobile_number=customer_mobile,
                                           first_email=first_email,
                                           second_email=second_email, phone=phone, contact=contact,
                                           first_address=first_address,
                                           second_address=second_address, fax=fax, city=city, state=state, zip=zip_code,
                                           country=country, previous_balance=previous_balance)

            messages.success(request, "Manufacturer Added Successfully. ")
            manufacture_obj.save()
            return redirect('manufacturer:add-manufacturer')


class ManufacturerList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        manufacturers = Manufacturer.objects.filter(is_active=True)

        context = {
            'manufacturers': manufacturers,
        }
        return render(request, 'manufacturer/manufacturer_list.html', context)


class EditManufacturer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, manufacturer_id):
        manufacturer_obj = get_object_or_404(Manufacturer, pk=int(manufacturer_id))
        context = {
            'manufacturer': manufacturer_obj
        }
        return render(request, 'manufacturer/edit_manufacturer.html', context)

    def post(self, request, manufacturer_id):
        manufacturer_obj = get_object_or_404(Manufacturer, pk=int(manufacturer_id))
        if request.method == "POST":
            data = request.POST
            manufacturer_name = data.get('manufacturer_name')
            manufacturer_mobile = data.get('manufacturer_mobile')
            first_email = data.get('first_email') if data.get('first_email') else ''
            second_email = data.get('second_email') if data.get('second_email') else ''
            phone = data.get('phone') if data.get('phone') else ''
            contact = data.get('contact') if data.get('contact') else ''
            first_address = data.get('first_address') if data.get('first_address') else ''
            second_address = data.get('second_address') if data.get('second_address') else ''
            fax = data.get('fax') if data.get('fax') else ''
            city = data.get('city') if data.get('city') else ''
            state = data.get('state') if data.get('state') else ''
            zip_code = data.get('zip') if data.get('zip') else ''
            country = data.get('country') if data.get('country') else ''
            previous_balance = data.get('previous_balance')

            manufacturer_obj.name = manufacturer_name
            manufacturer_obj.mobile_number = manufacturer_mobile
            manufacturer_obj.first_email = first_email
            manufacturer_obj.second_email = second_email
            manufacturer_obj.phone = phone
            manufacturer_obj.contact = contact
            manufacturer_obj.first_address = first_address
            manufacturer_obj.second_address = second_address
            manufacturer_obj.fax = fax
            manufacturer_obj.city = city
            manufacturer_obj.state = state
            manufacturer_obj.zip = zip_code
            manufacturer_obj.country = country
            manufacturer_obj.previous_balance = previous_balance
            messages.success(request, "Manufacturer Updated Successfully. ")
            manufacturer_obj.save()

            return redirect('manufacturer:edit-manufacturer', manufacturer_id=manufacturer_id)


class RemoveManufacturer(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, manufacturer_id):
        obj = get_object_or_404(Manufacturer, id=manufacturer_id)
        obj.is_active = False
        obj.save()
        messages.success(request, "Manufacturer Removed Successfully. ")
        return redirect('manufacturer:manufacturer-list')


class UploadCsv(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        file = request.FILES.get('csv_file')
        file_name = str(file)
        if not file_name.endswith('.csv'):
            messages.warning(request, 'File Type is not Valid. ')
            return redirect('manufacturer:add-manufacturer')
        else:
            obj = CSV(file=file)
            obj.save()
            with open(obj.file.path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                csv_reader = list(csv_reader)
                if len(csv_reader[0]) != 3:
                    messages.info(request, "Columns didn't matched. View the Sample File. ")
                    return redirect('manufacturer:add-manufacturer')

                csv_reader.remove(csv_reader[0])  # Removes the top row

                skipped_rows = 0
                for line in csv_reader:
                    if line[0] == '' or line[1] == '':
                        skipped_rows += 1
                    else:
                        manufacturer_obj = Manufacturer(name=line[0], mobile_number=line[1], first_address=line[2],
                                                        previous_balance=0)
                        manufacturer_obj.first_email = ''
                        manufacturer_obj.second_email = ''
                        manufacturer_obj.phone = ''
                        manufacturer_obj.contact = ''
                        manufacturer_obj.second_address = ''
                        manufacturer_obj.fax = ''
                        manufacturer_obj.city = ''
                        manufacturer_obj.state = ''
                        manufacturer_obj.zip = ''
                        manufacturer_obj.country = ''

                        manufacturer_obj.save()

                if skipped_rows == len(list(csv_reader)):
                    messages.info(request, 'Name or Mobile Number Missing. Skipped all Rows. ')
                elif skipped_rows == 0:
                    messages.success(request, '{a} Manufacturer(s) Added Successfully. '.format(a=len(list(csv_reader))))
                else:
                    messages.success(request, '{x} Manufacturer(s) created. {y} row(s) Skipped because of NULL value.'.format(x=len(list(csv_reader))-skipped_rows, y=skipped_rows))

                return redirect('manufacturer:manufacturer-list')
