from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from clients.models import Client
from django.db.models import Count
from invoices.models import InvoiceOut
from suppliers.models import Supplier




@login_required
def dashboard(request):
    top_clients = Client.objects.annotate(contribution=Count('invoiceout')).order_by('-contribution')[:5]
    top_suppliers = Supplier.objects.annotate(contribution=Count('purchase_order_out')).order_by('-contribution')[:5]
    return render(request,"dashboard/index.html",{'top_clients':top_clients,"top_suppliers":top_suppliers})