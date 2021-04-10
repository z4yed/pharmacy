import datetime
from django.shortcuts import render
from django.views.generic.base import View
from invoice.models import Invoice, InvoiceItems
from medicine.models import Medicine, Category
from purchase.models import Purchase, PurchaseItems
from system.utils import filter_queryset


class SalesReport(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        invoices = Invoice.objects.filter(is_active=True)

        context = {
            'invoices': invoices,
        }

        return render(request, 'reports/sales_report.html', context)

    def post(self, request):
        invoices = Invoice.objects.filter(is_active=True)
        from_date = request.POST.get('from_date')
        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        to_date = request.POST.get('to_date')
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')

        lookups = ['date__gte', 'date__lte']
        lookup_values = [from_date, to_date]

        invoices = filter_queryset(invoices, lookups, lookup_values)

        context = {
            'invoices': invoices,
        }
        return render(request, 'reports/sales_report.html', context)


class SalesReportUser(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        invoices = Invoice.objects.filter(is_active=True)
        context = {
            'invoices': invoices,
        }
        return render(request, 'reports/sales_report_user.html', context)

    def post(self, request):
        """ Implement it after adding users. """
        pass


def sales_report_product(request):
    medicines = Medicine.objects.filter(is_active=True)
    invoice_items = InvoiceItems.objects.filter(is_active=True)

    if request.method == "POST":
        medicine_id = request.POST.get('medicine_id')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')

        lookups = ['batch__medicine__id', 'invoice__date__gte', 'invoice__date__lte']
        lookup_values = [medicine_id, from_date, to_date]

        invoice_items = filter_queryset(invoice_items, lookups, lookup_values)

    context = {
        'medicines': medicines,
        'invoice_items': invoice_items,
    }

    return render(request, 'reports/sales_report_product.html', context)


def sales_report_category(request):
    medicines = Medicine.objects.filter(is_active=True)
    invoice_items = InvoiceItems.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    if request.method == "POST":
        category_id = request.POST.get('category_id')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')

        lookups = ['batch__medicine__category__id', 'invoice__date__gte', 'invoice__date__lte']
        lookup_values = [category_id, from_date, to_date]

        invoice_items = filter_queryset(invoice_items, lookups, lookup_values)

    context = {
        'medicines': medicines,
        'invoice_items': invoice_items,
        'categories': categories,
    }

    return render(request, 'reports/sales_report_category.html', context)


def purchase_report(request):
    purchases = Purchase.objects.filter(is_active=True)

    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')

        lookups = ['date__gte', 'date__lte']
        lookup_values = [from_date, to_date]

        purchases = filter_queryset(purchases, lookups, lookup_values)

    context = {
        'purchases': purchases,
    }
    return render(request, 'reports/purchase_list.html', context)


def purchase_report_category(request):
    purchases_items = PurchaseItems.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    if request.method == "POST":
        category_id = request.POST.get('category_id_report')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')

        lookups = ['batch__medicine__category__id', 'order__date__gte', 'order__date__lte']
        lookup_values = [category_id, from_date, to_date]

        purchases_items = filter_queryset(purchases_items, lookups, lookup_values)

    context = {
        'categories': categories,
        'purchases_items': purchases_items,
    }
    return render(request, 'reports/purchase_list_category.html', context)