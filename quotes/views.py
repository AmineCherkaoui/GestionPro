from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string


from .models import QuoteOut, QuoteOutProduct, QuoteOutService
from invoices.models import InvoiceOut,InvoiceOutProduct,InvoiceOutService
from .forms import QuoteOutForm, AddProductForm, AddServiceForm

from weasyprint import HTML
from num2words import num2words

from django.db.models import Q



# Create your views here.
@login_required
def quotes_list(request):
    search = request.GET.get('search')
    quotes = QuoteOut.objects.all().select_related("client").order_by("-id")
    if search:
        quotes = quotes.filter(Q(client__name__icontains=search) | Q(id__icontains=search))

    paginator = Paginator(quotes, 7)
    page = request.GET.get('page')
    quotes = paginator.get_page(page)
    return render(request,"quotes/list.html",{'quotes':quotes})




@login_required
@permission_required("quotes.add_quoteout")
def create_quote(request):
    QuoteProductForm = inlineformset_factory(QuoteOut, QuoteOutProduct, form=AddProductForm, extra=1, can_delete=False)
    QuoteServiceForm = inlineformset_factory(QuoteOut, QuoteOutService, form=AddServiceForm, extra=1, can_delete=False)

    if request.method == "POST":
        quote_form = QuoteOutForm(request.POST)
        product_form = QuoteProductForm(request.POST)
        service_form = QuoteServiceForm(request.POST)

        if quote_form.is_valid() and product_form.is_valid() and service_form.is_valid():
            quote = quote_form.save()
            for form in product_form:
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity')
                if product and quantity:
                    existing_product = QuoteOutProduct.objects.filter(quote=quote, product=product).first()
                    if existing_product:
                        existing_product.quantity += quantity
                        existing_product.save()
                    else:
                        quote_product = form.save(commit=False)
                        quote_product.quote = quote
                        quote_product.save()


            for form in service_form:
                service = form.cleaned_data.get('service')
                if service:
                    existing_service = QuoteOutService.objects.filter(quote=quote, service=service).first()
                    if existing_service:
                        existing_service.quantity += form.cleaned_data.get('quantity', 1)
                        existing_service.save()
                    else:
                        quote_service = form.save(commit=False)
                        quote_service.quote = quote
                        quote_service.save()
            messages.success(request,"Devis créé avec succès")
            return redirect('quotes-list')

    else:
        quote_form = QuoteOutForm()
        product_form = QuoteProductForm()
        service_form = QuoteServiceForm()

    return render(request, 'quotes/create.html', {
        'quote_form': quote_form,
        'product_form': product_form,
        'service_form': service_form
    })


@login_required
@permission_required("quotes.delete_quoteout")
def delete_quote(request, quote_id):
    quote = get_object_or_404(QuoteOut, id=quote_id)
    if request.method == "POST":
        quote.delete()
        messages.success(request,"Devis supprimé avec succès")
    return redirect("quotes-list")


@login_required
def quote_details(request, quote_id):
    quote = get_object_or_404(QuoteOut, id=quote_id)
    products = QuoteOutProduct.objects.filter(quote=quote).select_related('product')
    services = QuoteOutService.objects.filter(quote=quote).select_related('service')
    context = {
        'quote': quote,
        'products': products,
        'services': services,
    }
    return render(request, 'quotes/details.html', context)

@login_required
@permission_required("quotes.change_quoteout")
def quote_add_product(request,quote_id):
    quote = get_object_or_404(QuoteOut, id=quote_id)
    form=AddProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        quote_product, created = QuoteOutProduct.objects.get_or_create(
            quote=quote,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            quote_product.quantity += quantity
            quote_product.save()
        messages.success(request,f"Produit ajouté avec succès")
        return redirect('quote-detail', quote_id=quote.id)

    return render(request, 'quotes/add_product.html', {
        'form': form,
        'quote': quote,
    })

@login_required
@permission_required("quotes.change_quoteout")
def quote_delete_product(request, quote_id, product_id):
    if request.method == "POST":
        quote_product = get_object_or_404(QuoteOutProduct, quote_id=quote_id, id=product_id)
        quote_product.delete()
        messages.success(request,f"Produit supprimé avec succès")
    return redirect('quote-detail', quote_id=quote_id)

@login_required
@permission_required("quotes.change_quoteout")
def quote_add_service(request, quote_id):
    quote = get_object_or_404(QuoteOut, id=quote_id)
    form = AddServiceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        service = form.cleaned_data['service']
        quantity = form.cleaned_data['quantity']

        quote_service, created = QuoteOutService.objects.get_or_create(
            quote=quote,
            service=service,
            defaults={'quantity': quantity}
        )

        if not created:
            quote_service.quantity += quantity
            quote_service.save()
        messages.success(request,f"Service ajouté avec succès")
        return redirect('quote-detail', quote_id=quote.id)

    return render(request, 'quotes/add_service.html', {
        'form': form,
        'quote': quote,
    })



@login_required
@permission_required("quotes.change_quoteout")
def  quote_delete_service(request, quote_id, service_id):
    quote_service = get_object_or_404(QuoteOutService, quote_id=quote_id, id=service_id)
    if request.method == "POST":
        quote_service.delete()
        messages.success(request,f"Service supprimé avec succès")
    return redirect('quote-detail', quote_id=quote_id)

@login_required
def quote_pdf(request,quote_id):
    quote = get_object_or_404(QuoteOut, id=quote_id)
    products = quote.quote_out_product.all()
    services = quote.quote_out_service.all()
    total_text=num2words(quote.total_ttc)

    html_string = render_to_string('quotes/pdf.html', {
        'quote': quote,
        'products': products,
        'services': services,
        "total_text": total_text,
    },request)


    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    pdf = html.write_pdf()


    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=quote_N°{quote.id}-OT-{quote.date.year}.pdf'
    return response

@login_required
@permission_required("quotes.change_quoteout")
def convert_quote_to_invoice(request, quote_id):
    quote = get_object_or_404(QuoteOut, id=quote_id)
    if quote.is_converted:
        messages.warning(request, "Ce devis a déjà été converti en facture.")
        return redirect('quote-detail', quote_id=quote.id)
    try:
        invoice = InvoiceOut.objects.create(
            client=quote.client,
        )
        for quote_product in quote.quote_out_product.all():
            InvoiceOutProduct.objects.create(
                invoice=invoice,
                product=quote_product.product,
                quantity=quote_product.quantity,
                price_at_invoice=quote_product.price_at_quote
            )
        for quote_service in quote.quote_out_service.all():
            InvoiceOutService.objects.create(
                invoice=invoice,
                service=quote_service.service,
                quantity=quote_service.quantity,
                price_at_invoice=quote_service.price_at_quote
            )

        quote.is_converted = True
        quote.invoice_id = invoice.id
        quote.save()
        messages.success(request, "Devis converti avec succès en facture.")
        return redirect('invoice-detail', invoice_id=invoice.id)

    except Exception as e:
        messages.error(request, f"Une erreur s'est produite lors de la conversion du devis: {str(e)}")
        return redirect('quotes-list')





