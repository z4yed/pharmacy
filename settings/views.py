from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

from settings.models import Setting


class SettingView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        company = Setting.objects.last()
        context = {
            'company': company
        }
        return render(request, 'settings/company_details.html', context)

    def post(self, request):
        data = request.POST
        title = data.get('title', '')
        address = data.get('address', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        footer_text = data.get('footer_text', '')

        logo = request.FILES.get('logo')
        background_image = request.FILES.get('login_background')

        company_obj = Setting.objects.last()
        if not company_obj:
            company_obj = Setting()
        company_obj.company_title = title
        company_obj.address = address
        company_obj.email = email
        company_obj.phone = phone
        company_obj.footer_text = footer_text

        if logo:
            company_obj.logo = logo
        if background_image:
            company_obj.login_background = background_image
        company_obj.save()

        messages.success(request, 'Details Updated Successfully. ')
        return redirect('settings:pharmacy_details')
