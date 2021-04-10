import csv
import barcode
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from manufacturer.models import Manufacturer
from medicine.models import Category, Unit, Type, Leaf, Medicine, MedicineCSV, Batch
from system.utils import render_to_pdf


class CategoryList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'medicine/category_list.html', context)


class AddCategory(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        name = request.POST.get('category_name')
        status = request.POST.get('category_status')

        active = True if status == '1' else False

        obj = Category(name=name, is_active=active)
        obj.save()
        messages.success(request, 'Category Added Successfully.')

        return redirect('medicine:category-list')


class UpdateCategory(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, category_id):
        name = request.POST.get('category_name')
        status = request.POST.get('category_status')

        active = True if status == '1' else False

        category_obj = Category.objects.get(pk=category_id)
        category_obj.name = name
        category_obj.is_active = active
        category_obj.save()

        messages.success(request, 'Category Updated Successfully. ')
        return redirect('medicine:category-list')


class RemoveCategory(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, category_id):
        category_obj = Category.objects.get(pk=category_id)
        category_obj.delete()
        messages.success(request, 'Category Removed Successfully. ')
        return redirect('medicine:category-list')


class UnitList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        units = Unit.objects.all()
        context = {
            'units': units
        }
        return render(request, 'medicine/unit_list.html', context)


class AddUnit(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        name = request.POST.get('unit_name')
        status = request.POST.get('unit_status')

        active = True if status == '1' else False
        obj = Unit(name=name, is_active=active)
        obj.save()

        messages.success(request, 'Unit Added Successfully. ')
        return redirect('medicine:unit-list')


class UpdateUnit(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, unit_id):
        name = request.POST.get('unit_name')
        status = request.POST.get('unit_status')

        active = True if status == '1' else False

        obj = Unit.objects.get(pk=unit_id)
        obj.name = name
        obj.is_active = active
        obj.save()
        messages.success(request, 'Unit Updated Successfully. ')

        return redirect('medicine:unit-list')


class RemoveUnit(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, unit_id):
        obj = Unit.objects.get(pk=unit_id)
        obj.delete()
        messages.success(request, 'Unit Removed Successfully. ')
        return redirect('medicine:unit-list')


class TypeList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        types = Type.objects.all()
        context = {
            'types': types
        }
        return render(request, 'medicine/type_list.html', context)


class AddType(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        name = request.POST.get('type_name')
        status = request.POST.get('type_status')

        active = True if status == '1' else False

        obj = Type(name=name, is_active=active)
        obj.save()
        messages.success(request, 'Type Added Successfully. ')
        return redirect('medicine:type-list')


class UpdateType(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, type_id):
        obj = Type.objects.get(pk=type_id)

        name = request.POST.get('type_name')
        status = request.POST.get('type_status')

        active = True if status == '1' else False

        obj.name = name
        obj.is_active = active
        obj.save()

        messages.success(request, 'Type Updated Successfully. ')
        return redirect('medicine:type-list')


class RemoveType(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, type_id):
        type_obj = Type.objects.get(pk=type_id)
        type_obj.delete()
        messages.success(request, 'Type Removed Successfully. ')
        return redirect('medicine:type-list')


class LeafList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        leafs = Leaf.objects.all()
        context = {
            'leafs': leafs
        }
        return render(request, 'medicine/leaf_list.html', context)


class AddLeaf(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        leaf_type = request.POST.get('leaf_type')
        total_per_box = request.POST.get('total_box')

        obj = Leaf(leaf_type=leaf_type, number_per_box=total_per_box)
        obj.save()

        messages.success(request, 'Successfully Saved. ')
        return redirect('medicine:leaf-list')


class UpdateLeaf(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, leaf_id):
        obj = Leaf.objects.get(pk=leaf_id)

        leaf_type = request.POST.get('leaf_type')
        total_per_box = request.POST.get('total_box')
        obj.leaf_type = leaf_type
        obj.number_per_box = total_per_box
        obj.save()

        messages.success(request, 'Updated Successfully. ')
        return redirect('medicine:leaf-list')


class RemoveLeaf(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, leaf_id):
        obj = Leaf.objects.get(pk=leaf_id)
        obj.delete()
        messages.success(request, 'Removed Successfully. ')
        return redirect('medicine:leaf-list')


class MedicineList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        medicines = Medicine.objects.filter(is_active=True)
        context = {
            'medicines': medicines
        }
        return render(request, 'medicine/medicine_list.html', context)


class AddMedicine(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        box_sizes = Leaf.objects.all()
        categories = Category.objects.filter(is_active=True)
        types = Type.objects.filter(is_active=True)
        manufacturers = Manufacturer.objects.filter(is_active=True)
        units = Unit.objects.filter(is_active=True)

        context = {
            'box_sizes': box_sizes,
            'categories': categories,
            'types': types,
            'manufacturers': manufacturers,
            'units': units,
        }

        return render(request, 'medicine/add_medicine.html', context)

    def post(self, request):
        data = request.POST
        code = data.get('barcode_id', '')
        medicine_name = data.get('medicine_name')
        strength = data.get('strength', '')
        generic_name = data.get('generic_name', '')

        box_size = data.get('box_size')
        leaf_obj = Leaf.objects.get(id=int(box_size))

        unit = data.get('unit')
        unit_obj = Unit.objects.get(id=int(unit))

        product_location = data.get('product_location', '')
        product_details = data.get('product_details', '')

        category_id = data.get('category_id')
        category_obj = Category.objects.get(id=category_id)

        price = request.POST.get('price')

        product_type = data.get('product_type', '')

        if product_type:
            type_obj = Type.objects.get(id=product_type)

        image = request.FILES.get('image')

        manufacturer_id = data.get('manufacturer_id')
        manufacturer = Manufacturer.objects.get(id=manufacturer_id)

        manufacturer_price = data.get('manufacturer_price')
        tax0 = data.get('tax0', '')
        tax = data.get('tax1', '')

        status = data.get('status')

        manufacturer_price = float(manufacturer_price)
        price = float(price)

        if manufacturer_price > price:
            messages.info(request, "Manufacturer Price Shouldn't be greater than Sell Price. ")
            return redirect('medicine:add-medicine')

        obj = Medicine(medicine_name=medicine_name, box_size=leaf_obj, unit=unit_obj, category=category_obj,
                       price=price, manufacturer=manufacturer, manufacturer_price=manufacturer_price,
                       code_text=code, strength=strength, generic_name=generic_name, shelf=product_location,
                       details=product_details, vat=tax0, igta=tax)

        if image:
            obj.image = image
            obj.save()

        if code:
            barcode_class = barcode.get_barcode_class('ean8')
            image = barcode_class(code)

            image = image.save('static/barcodes/barcode_%s' % code)
            obj.barcode_path = image
            obj.save()

        obj.is_active = True if status == '1' else False

        if product_type:
            obj.type = type_obj

        obj.save()
        messages.success(request, 'Medicine Added Successfully. ')

        return redirect('medicine:medicine-list')


class UpdateMedicine(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, medicine_id):
        box_sizes = Leaf.objects.all()
        medicine_obj = Medicine.objects.get(id=medicine_id)
        categories = Category.objects.filter(is_active=True)
        types = Type.objects.filter(is_active=True)
        manufacturers = Manufacturer.objects.filter(is_active=True)
        units = Unit.objects.filter(is_active=True)

        context = {
            'box_sizes': box_sizes,
            'categories': categories,
            'types': types,
            'manufacturers': manufacturers,
            'units': units,
            'object': medicine_obj,
        }

        return render(request, 'medicine/edit_medicine.html', context)

    def post(self, request, medicine_id):
        data = request.POST
        code = data.get('barcode_id', '')
        medicine_name = data.get('medicine_name')
        strength = data.get('strength', '')
        generic_name = data.get('generic_name', '')

        box_size = data.get('box_size')
        leaf_obj = Leaf.objects.get(id=int(box_size))

        unit = data.get('unit')
        unit_obj = Unit.objects.get(id=int(unit))

        product_location = data.get('product_location', '')
        product_details = data.get('product_details', '')

        category_id = data.get('category_id')
        category_obj = Category.objects.get(id=category_id)

        price = request.POST.get('price')

        product_type = data.get('product_type', '')

        if product_type:
            type_obj = Type.objects.get(id=product_type)

        image = request.FILES.get('image')

        manufacturer_id = data.get('manufacturer_id')
        manufacturer = Manufacturer.objects.get(id=manufacturer_id)

        manufacturer_price = data.get('manufacturer_price')
        tax = data.get('tax0', '')
        igta = data.get('tax1', '')

        status = data.get('status')

        manufacturer_price = float(manufacturer_price)
        price = float(price)

        if manufacturer_price > price:
            messages.info(request, "Manufacturer Price Shouldn't be greater than Sell Price. ")
            return redirect('medicine:update-medicine', medicine_id=medicine_id)

        # Updating Medicine Object
        obj = Medicine.objects.get(id=medicine_id)
        obj.medicine_name = medicine_name
        obj.box_size = leaf_obj
        obj.unit = unit_obj
        obj.category = category_obj
        obj.price = price
        obj.manufacturer = manufacturer
        obj.manufacturer_price = manufacturer_price
        obj.code_text = code
        obj.strength = strength
        obj.generic_name = generic_name
        obj.shelf = product_location
        obj.details = product_details
        obj.vat = tax
        obj.igta = igta

        if image:
            obj.image = image

        obj.is_active = True if status == '1' else False

        if code == '':
            obj.barcode_path = ''

        if code != obj.code_text:
            barcode_class = barcode.get_barcode_class('ean8')
            image = barcode_class(code)

            image = image.save('static/barcodes/barcode_%s' % code)

            obj.barcode_path = image
            obj.save()

        if product_type:
            obj.type = type_obj

        obj.save()

        messages.success(request, 'Medicine Updated Successfully. ')

        return redirect('medicine:update-medicine', medicine_id=medicine_id)


class RemoveMedicine(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, medicine_id):
        medicine_obj = Medicine.objects.get(id=medicine_id)
        medicine_obj.is_active = False
        medicine_obj.save()

        messages.success(request, 'Medicine Removed Successfully. ')
        return redirect('medicine:medicine-list')


class UploadMedicineCsv(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        uploaded_file = request.FILES.get('csv_file')

        file_name = str(uploaded_file)
        if not file_name.endswith(".csv"):
            messages.info(request, "File type not supported. ")
            return redirect('medicine:add-medicine')
        else:
            obj = MedicineCSV(file=uploaded_file)
            obj.save()

            with open(obj.file.path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                csv_reader = list(csv_reader)

                if len(csv_reader[0]) != 8:
                    messages.info(request, "Columns didn't matched with Sample File. ")
                    return redirect('medicine:add-medicine')

                csv_reader.remove(csv_reader[0])  # Removes the top rows

                skipped_rows = 0

                for rows in csv_reader:
                    if "" in rows:
                        skipped_rows += 1
                    else:
                        manufacturer = rows[0]
                        manufacturer_obj, created = Manufacturer.objects.get_or_create(name=manufacturer.title())

                        medicine_name = rows[1]
                        generic_name = rows[2]
                        strength = rows[3]
                        category = rows[4]

                        category_obj, created = Category.objects.get_or_create(name=category.title())

                        manufacturer_price = rows[5]
                        box_price = rows[6]
                        box_size = rows[7]  # Not Used.

                        medicine_obj = Medicine(medicine_name=medicine_name, manufacturer=manufacturer_obj,
                                                generic_name=generic_name,
                                                strength=strength, category=category_obj,
                                                manufacturer_price=manufacturer_price,
                                                price=box_price, is_active=True)
                        medicine_obj.details = ''
                        medicine_obj.code = ''
                        medicine_obj.save()

                        if skipped_rows == 0:
                            messages.success(request, '{a} rows inserted successfully. '.format(a=len(csv_reader)))
                        elif skipped_rows == len(csv_reader):
                            messages.warning(request, "No Medicine Added. Please re-check the CSV file. ")
                        else:
                            messages.success(request, "{a} rows inserted. {b} rows skipped. ".format(
                                a=len(csv_reader) - skipped_rows, b=skipped_rows))

                        return redirect('medicine:medicine-list')


class BarCodes(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, medicine_id):

        medicine_obj = Medicine.objects.get(id=medicine_id)
        context = {
            'object': medicine_obj
        }

        return render(request, 'medicine/barcodes.html', context)


class ViewBarcodePDF(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, medicine_id):
        medicine_obj = Medicine.objects.get(id=medicine_id)

        data = {
            'object': medicine_obj,
        }

        pdf = render_to_pdf('medicine/barcode_print_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# class DownloadPDF(View):
#     def get(self, request, medicine_id, *args, **kwargs):
#
#         medicine_obj = Medicine.objects.get(id=medicine_id)
#
#         data = {
#             'object': medicine_obj,
#         }
#
#         pdf = render_to_pdf('medicine/barcode_print_template.html', data)
#
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = "Invoice_%s.pdf" % medicine_obj.id
#         content = "attachment; filename='%s'" % filename
#         response['Content-Disposition'] = content
#         return response


class StockList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        medicines = Medicine.objects.filter(is_active=True)
        context = {
            'medicines': medicines
        }
        return render(request, 'medicine/stock/stock_list.html', context)


class StockListBatchWise(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        batches = Batch.objects.filter(is_active=True)
        context = {
            'batches': batches
        }
        return render(request, 'medicine/stock/stock_list_batch.html', context)


class AvailableStock(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        all_medicines = Medicine.objects.filter(is_active=True)
        stocked_medicines = []

        for medicine in all_medicines:
            if medicine.total_stock > 0:
                stocked_medicines.append(medicine)

        context = {
            'medicines': stocked_medicines,
        }
        return render(request, 'medicine/stock/stock_medicines.html', context)

