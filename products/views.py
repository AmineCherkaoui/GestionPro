from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.db.models import Q

# Create your views here.

@login_required
def products_list(request):
    search = request.GET.get('search')
    products = Product.objects.all().order_by('-id')
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
    pagination = Paginator(products, 7)
    page = request.GET.get('page')
    products = pagination.get_page(page)
    return render(request,"products/list.html", {"products":products,"search":search})

@login_required
@permission_required("products.add_product")
def create_product(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Produit créé avec succès")
            return redirect("products-list")
    return render(request, 'products/create.html', {'form': form})

@login_required
# @permission_required("products.edit_product")
# @permission_required("products.change_quantity_only")
def edit_product(request, product_id):
    if not request.user.has_perm("products.edit_product") and not request.user.has_perm("products.change_quantity_only"):
        return redirect("products-list")
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=product,user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request,"Produit modifié avec succès")
        return redirect("products-list")
    return render(request, 'products/create.html', {'form': form})
        
@login_required
@permission_required("products.delete_product")
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request,"Produit supprimé avec succès")
    return redirect("products-list")