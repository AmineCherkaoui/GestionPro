from datetime import datetime, timedelta
from django.utils import timezone

from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from clients.models import Client
from django.db.models import Count
from invoices.models import InvoiceOut
from purchase_orders.models import PurchaseOrderOut
from quotes.models import QuoteOut
from suppliers.models import Supplier




@login_required
def dashboard(request):
    top_clients = Client.objects.annotate(contribution=Count('invoiceout')).order_by('-contribution')[:5]
    top_suppliers = Supplier.objects.annotate(contribution=Count('purchase_order_out')).order_by('-contribution')[:5]
    current_month = datetime.now().month
    current_year = datetime.now().year
    filter = request.GET.get('filter', '7')
    if filter == '7':
        start_date = timezone.now() - timedelta(days=7)
    elif filter == '15':
        start_date = timezone.now() - timedelta(days=15)
    elif filter == '30':
        start_date = timezone.now() - timedelta(days=30)
    else:
        start_date = timezone.now() - timedelta(days=365)

    invoices = InvoiceOut.objects.filter(date__gte=start_date)
    total_invoices_amount = sum(invoice.total_ttc for invoice in invoices)

    context = {
        "filter":filter,
        'invoices_count': InvoiceOut.objects.filter(date__gte=start_date).count(),
        "total_invoices_amount":total_invoices_amount,
        'quotes_count': QuoteOut.objects.filter(date__gte=start_date).count(),
        'purchase_orders_count': PurchaseOrderOut.objects.filter(date__gte=start_date).count(),
        'clients_count': Client.objects.count(),
        'top_clients':top_clients,
        "top_suppliers":top_suppliers
    }

    return render(request,"dashboard/index.html",context)