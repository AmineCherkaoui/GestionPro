from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from quotes.models import QuoteOut

from .models import InvoiceOut, InvoiceOutProduct, InvoiceOutService
from settings.models import Settings
from .forms import InvoiceOutForm, AddProductForm, AddServiceForm

from decimal import Decimal

from weasyprint import HTML


from num2words import num2words
from django.db.models import Q

# Create your views here.
@login_required
def invoices_list(request):
    search = request.GET.get('search')
    invoices = InvoiceOut.objects.all().select_related("client").order_by("-id")

    if search:
        invoices = invoices.filter(Q(client__name__icontains=search) | Q(id__icontains=search))


    paginator = Paginator(invoices, 7)
    page = request.GET.get('page')
    invoices = paginator.get_page(page)
    return render(request,"invoices/list.html",{'invoices':invoices})




@login_required
@permission_required("invoices.add_invoiceout")
def create_invoice(request):
    InvoiceProductForm = inlineformset_factory(InvoiceOut, InvoiceOutProduct, form=AddProductForm, extra=1, can_delete=False)
    InvoiceServiceForm = inlineformset_factory(InvoiceOut, InvoiceOutService, form=AddServiceForm, extra=1, can_delete=False)

    if request.method == "POST":
        invoice_form = InvoiceOutForm(request.POST)
        product_form = InvoiceProductForm(request.POST)
        service_form = InvoiceServiceForm(request.POST)

        if invoice_form.is_valid() and product_form.is_valid() and service_form.is_valid():
            invoice=invoice_form.save()
            for form in product_form:
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity')

                if product and quantity:
                    existing_product = InvoiceOutProduct.objects.filter(invoice=invoice, product=product).first()
                    if existing_product:
                        existing_product.quantity += quantity
                        existing_product.save()
                    else:
                        invoice_product = form.save(commit=False)
                        invoice_product.invoice = invoice
                        invoice_product.save()

                    product.quantity -= quantity
                    product.save()

            for form in service_form:
                service = form.cleaned_data.get('service')
                if service:
                    existing_service = InvoiceOutService.objects.filter(invoice=invoice, service=service).first()
                    if existing_service:
                        existing_service.quantity += form.cleaned_data.get('quantity', 1)
                        existing_service.save()
                    else:
                        invoice_service = form.save(commit=False)
                        invoice_service.invoice = invoice
                        invoice_service.save()
            messages.success(request,"Facture créée avec succès")
            return redirect('invoices-list')

    else:
        invoice_form = InvoiceOutForm()
        product_form = InvoiceProductForm()
        service_form = InvoiceServiceForm()

    return render(request, 'invoices/create.html', {
        'invoice_form': invoice_form,
        'product_form': product_form,
        'service_form': service_form
    })


@login_required
@permission_required("invoices.delete_invoiceout")
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(InvoiceOut, id=invoice_id)
    if request.method == "POST":
        try:
            quote=QuoteOut.objects.get(invoice_id=invoice_id)
            quote.is_converted=False
            quote.save()
        except QuoteOut.DoesNotExist:
            pass
        invoice.delete()
        messages.success(request, "Facture supprimée avec succès")
    return redirect("invoices-list")


@login_required
def invoice_details(request, invoice_id):
    invoice = get_object_or_404(InvoiceOut, id=invoice_id)
    products = InvoiceOutProduct.objects.filter(invoice=invoice).select_related('product')
    services = InvoiceOutService.objects.filter(invoice=invoice).select_related('service')
    context = {
        'invoice': invoice,
        'products': products,
        'services': services,
    }
    return render(request, 'invoices/details.html', context)

@login_required
@permission_required("invoices.change_invoiceout")
def invoice_add_product(request,invoice_id):
    invoice = get_object_or_404(InvoiceOut, id=invoice_id)
    form=AddProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']


        invoice_product, created = InvoiceOutProduct.objects.get_or_create(
            invoice=invoice,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            invoice_product.quantity += quantity
            invoice_product.save()

        product.quantity -= quantity
        product.save()
        messages.success(request, "Produit ajouté avec succès")
        return redirect('invoice-detail', invoice_id=invoice.id)

    return render(request, 'invoices/add_product.html', {
        'form': form,
        'invoice': invoice,
    })

@login_required
@permission_required("invoices.change_invoiceout")
def invoice_delete_product(request, invoice_id, product_id):
    invoice_product = get_object_or_404(InvoiceOutProduct, invoice_id=invoice_id, id=product_id)
    if request.method == "POST":
        product = invoice_product.product
        product.quantity += invoice_product.quantity
        product.save()
        invoice_product.delete()
        messages.success(request, "Produit supprimé avec succès ")
    return redirect('invoice-detail', invoice_id=invoice_id)


@login_required
@permission_required("invoices.change_invoiceout")
def invoice_add_service(request, invoice_id):
    invoice = get_object_or_404(InvoiceOut, id=invoice_id)
    form = AddServiceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        service = form.cleaned_data['service']
        quantity = form.cleaned_data['quantity']
        invoice_service, created = InvoiceOutService.objects.get_or_create(
            invoice=invoice,
            service=service,
            defaults={'quantity': quantity}
        )

        if not created:
            invoice_service.quantity += quantity
            invoice_service.save()
        messages.success(request, "Service ajouté avec succès")
        return redirect('invoice-detail', invoice_id=invoice.id)

    return render(request, 'invoices/add_service.html', {
        'form': form,
        'invoice': invoice,
    })



@login_required
@permission_required("invoices.change_invoiceout")
def  invoice_delete_service(request, invoice_id, service_id):
    invoice_service = get_object_or_404(InvoiceOutService, invoice_id=invoice_id, id=service_id)
    if request.method == "POST":
        invoice_service.delete()
        messages.success(request, "Service supprimé avec succès")
    return redirect('invoice-detail', invoice_id=invoice_id)

@login_required
def invoice_pdf(request,invoice_id):
    invoice = get_object_or_404(InvoiceOut, id=invoice_id)
    products = invoice.invoice_out_product.all()
    services = invoice.invoice_out_service.all()
    total_text=num2words(invoice.total_ttc,lang="fr")

    html_string = render_to_string('invoices/pdf.html', {
        'invoice': invoice,
        'products': products,
        'services': services,
        "total_text": total_text,

    },request)


    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    pdf = html.write_pdf()


    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=invoice_N°{invoice.id}-OT-{invoice.date.year}.pdf'
    return response





