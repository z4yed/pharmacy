import os
import random

from invoice.models import Invoice
from purchase.models import Purchase

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from accounts.models import ManufacturerPayment as MP, CustomerReceipt as CR
from settings.models import Setting


ROLE_CHOICES = (
    (1, 'Admin'),
    (2, 'Advisor'),
    (3, 'Head of Account')
)

CUSTOMER_STATUS = (
    (1, "Paid Customer"),
    (2, "Credit Customer")
)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_mp_pdf_view(payment_id):  # mp stands for Manufacturer Payment
    payment_obj = MP.objects.get(id=payment_id)
    template_path = 'accounts/payment_pdf.html'

    context = {
        'object': payment_obj,
        'setting': Setting.objects.last(),
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Payment Invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_cr_pdf_view(receipt_id):  # cr stands for Customer Receipt
    receipt_obj = CR.objects.get(id=receipt_id)
    template_path = 'accounts/receipt_pdf.html'

    context = {
        'object': receipt_obj,
        'setting': Setting.objects.last(),
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Receipt Invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def random_id_generator(module):
    generated_id = random.randint(100000000000, 999999999999)
    if module == 'Purchase':
        if Purchase.objects.filter(purchase_id=generated_id).exists():
            random_id_generator('Purchase')

        return generated_id

    if module == 'Invoice':
        if Invoice.objects.filter(invoice_id=generated_id).exists():
            random_id_generator('Invoice')

        return generated_id


# filter function
def check_parameter(param):
    return param != '' and param is not None
# returns either True or False


def filter_queryset(queryset, lookups, lookup_values):
    i = 0
    for lookup in lookups:
        if check_parameter(lookup_values[i]):
            queryset = queryset.filter(**{lookup: lookup_values[i]})
        i += 1
    return queryset.distinct()
