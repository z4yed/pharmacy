from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View

from service.models import Service


class ServiceList(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        services = Service.objects.filter(is_active=True)

        context = {
            'services': services,
        }
        return render(request, 'service/service_list.html', context)


class AddService(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {

        }
        return render(request, 'service/add_service.html', context)

    def post(self, request):
        data = request.POST
        service_name = data.get('service_name')
        charge = data.get('charge')
        description = data.get('description', '')
        tax0 = data.get('tax0')
        tax1 = data.get('tax1')

        obj = Service(name=service_name, charge=charge, description=description, vat=tax0, igta=tax1)
        obj.save()
        messages.success(request, 'Service added successfully. ')

        return redirect('service:service-list')


class EditService(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, service_id):
        service_obj = Service.objects.get(id=service_id)

        context = {
            'object': service_obj
        }
        return render(request, 'service/update_service.html', context)

    def post(self, request, service_id):
        data = request.POST
        service_name = data.get('service_name')
        charge = data.get('charge')
        description = data.get('description')
        tax0 = data.get('tax0')
        tax1 = data.get('tax1')

        service_obj = Service.objects.get(id=service_id)
        service_obj.name = service_name
        service_obj.charge = charge
        service_obj.description = description
        service_obj.vat = tax0
        service_obj.igta = tax1
        service_obj.save()

        messages.success(request, 'Service Updated Successfully. ')
        return redirect('service:update-service', service_id=service_id)


class RemoveService(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, service_id):
        service_obj = Service.objects.get(id=service_id)
        service_obj.is_active = False
        service_obj.save()

        messages.success(request, 'Service Removed Successfully. ')
        return redirect('service:service-list')