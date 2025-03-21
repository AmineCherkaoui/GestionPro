from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string


from .models import PurchaseOrderOut,PurchaseOrderOutProduct,PurchaseOrderOutService

from .forms import PurchaseOrderOutForm, AddProductForm, AddServiceForm
from settings.models import Settings

from decimal import Decimal
from weasyprint import HTML
from num2words import num2words
from datetime import date


# Create your views here.
@login_required
def purchase_orders_list(request):
    search = request.GET.get('search')
    purchase_orders = PurchaseOrderOut.objects.all().select_related("supplier").order_by("-id")
    if search:
        purchase_orders = purchase_orders.filter(supplier__name__icontains=search)

    paginator = Paginator(purchase_orders, 7)
    page = request.GET.get('page')
    purchase_orders = paginator.get_page(page)
    return render(request,"purchase_orders/list.html",{'purchase_orders':purchase_orders})




@login_required
@permission_required("purchase_orders.add_purchaseorderout")
def create_purchase_order(request):
    PurchaseOrderProductForm=inlineformset_factory(PurchaseOrderOut,PurchaseOrderOutProduct,form=AddProductForm, extra=1, can_delete=False)
    PurchaseOrderServiceForm=inlineformset_factory(PurchaseOrderOut,PurchaseOrderOutService,form=AddServiceForm, extra=1, can_delete=False)

    if request.method == "POST":
        purchase_order_form = PurchaseOrderOutForm(request.POST)
        product_form = PurchaseOrderProductForm(request.POST)
        service_form = PurchaseOrderServiceForm(request.POST)

        if purchase_order_form.is_valid() and product_form.is_valid() and service_form.is_valid():
            purchase_order = purchase_order_form.save()
            for form in product_form:
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity')
                if product and quantity:
                    existing_product = PurchaseOrderOutProduct.objects.filter(purchase_order=purchase_order, product=product).first()
                    if existing_product:
                        existing_product.quantity += quantity
                        existing_product.save()
                    else:
                        purchase_order_product = form.save(commit=False)
                        purchase_order_product.purchase_order = purchase_order
                        purchase_order_product.save()


            for form in service_form:
                service = form.cleaned_data.get('service')
                if service:
                    existing_service = PurchaseOrderOutService.objects.filter(purchase_order=purchase_order, service=service).first()
                    if existing_service:
                        existing_service.quantity += form.cleaned_data.get('quantity', 1)
                        existing_service.save()
                    else:
                        purchase_order_service = form.save(commit=False)
                        purchase_order_service.purchase_order = purchase_order
                        purchase_order_service.save()
            messages.success(request,"Puchase order successfully created")
            return redirect('purchase-orders-list')
    else:
        purchase_order_form = PurchaseOrderOutForm()
        product_form = PurchaseOrderProductForm()
        service_form = PurchaseOrderServiceForm()

    return render(request, 'purchase_orders/create.html', {
        'purchase_order_form': purchase_order_form,
        'product_form': product_form,
        'service_form': service_form
    })

@login_required
@permission_required("purchase_orders.change_purchaseorderout")
def delete_purchase_order(request, purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrderOut, id=purchase_order_id)
    if request.method == "POST":
        purchase_order.delete()
        messages.success(request,"Purchase order successfully deleted")
        return redirect("purchase-orders-list")
    return render(request,"purchase_orders/delete.html",{"purchase_order":purchase_order})

@login_required

def purchase_order_details(request, purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrderOut, id=purchase_order_id)
    products = PurchaseOrderOutProduct.objects.filter(purchase_order=purchase_order).select_related('product')
    services = PurchaseOrderOutService.objects.filter(purchase_order=purchase_order).select_related('service')
    context = {
        'purchase_order': purchase_order,
        'products': products,
        'services': services,
    }
    return render(request, 'purchase_orders/details.html', context)


@login_required
@permission_required("purchase_orders.change_purchaseorderout")
def purchase_order_add_product(request,purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrderOut, id=purchase_order_id)
    form=AddProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        purchase_order_product, created = PurchaseOrderOutProduct.objects.get_or_create(
            purchase_order=purchase_order,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            purchase_order_product.quantity += quantity
            purchase_order_product.save()
        messages.success(request,f"Product successfully added")
        return redirect('purchase-order-detail', purchase_order.id)

    return render(request, 'purchase_orders/add_product.html', {
        'form': form,
        'purchase_order': purchase_order,
    })

@login_required
@permission_required("purchase_orders.change_purchaseorderout")
def purchase_order_delete_product(request, purchase_order_id, product_id):
    purchase_order_product = get_object_or_404(PurchaseOrderOutProduct, purchase_order_id=purchase_order_id, id=product_id)
    purchase_order_product.delete()
    messages.success(request,f"Product successfully deleted")
    return redirect('purchase-order-detail', purchase_order_id)


@login_required
@permission_required("purchase_orders.change_purchaseorderout")
def purchase_order_add_service(request, purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrderOut, id=purchase_order_id)
    form = AddServiceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        service = form.cleaned_data['service']
        quantity = form.cleaned_data['quantity']

        purchase_order_service, created = PurchaseOrderOutService.objects.get_or_create(
            purchase_order=purchase_order,
            service=service,
            defaults={'quantity': quantity}
        )

        if not created:
            purchase_order_service.quantity += quantity
            purchase_order_service.save()
        messages.success(request,f"Service successfully added")
        return redirect('purchase-order-detail', purchase_order_id=purchase_order.id)

    return render(request, 'purchase_orders/add_service.html', {
        'form': form,
        'purchase_order': purchase_order,
    })
@login_required
@permission_required("purchase_orders.change_purchaseorderout")
def  purchase_order_delete_service(request, purchase_order_id, service_id):
    purchase_order_service = get_object_or_404(PurchaseOrderOutService, purchase_order_id=purchase_order_id, id=service_id)
    purchase_order_service.delete()
    messages.success(request,f"Service successfully deleted")
    return redirect('purchase-order-detail', purchase_order_id=purchase_order_id)


@login_required
def purchase_order_pdf(request,purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrderOut, id=purchase_order_id)
    products = purchase_order.purchase_order_out_product.all()
    services = purchase_order.purchase_order_out_service.all()
    total_text=num2words(purchase_order.total_ttc)



    html_string = render_to_string('purchase_orders/pdf.html', {
        'purchase_order': purchase_order,
        'products': products,
        'services': services,
        "total_text": total_text,
    },request)


    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    pdf = html.write_pdf()


    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=quote_N°{purchase_order.id}-OT-{purchase_order.date.year}.pdf'
    return response







