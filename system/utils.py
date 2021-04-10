import os
import random

from invoice.models import Invoice
from purchase.models import Purchase

from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



ROLE_CHOICES = (
    (1, 'Admin'),
    (2, 'Advisor'),
    (3, 'Head of Account')
)

CUSTOMER_STATUS = (
    (1, "Paid Customer"),
    (2, "Credit Customer")
)


CURRENCY_CHOICES = (
    (1, "TAKA"),
    (2, "USD"),
)

DISCOUNT_TYPES = (
    (1, 'Discount Percentage %'),
    (2, 'Discount'),
    (3, 'Fixed Discount'),
)

TIMEZONE_CHOICES = (
    (1, 'Asia/Dhaka'),
    (2, 'Asia/Tokyo'),
)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


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
