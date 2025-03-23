from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Supplier
from .forms import SupplierForm



@login_required
def suppliers_list(request):
    search = request.GET.get('search')
    suppliers = Supplier.objects.all().order_by("-id")

    if search:
        suppliers = suppliers.filter(name__icontains=search)

    paginator = Paginator(suppliers, 7)
    page_number = request.GET.get('page')
    suppliers = paginator.get_page(page_number)

    return render(request, 'suppliers/list.html', {'suppliers': suppliers, 'search': search})

@login_required
@permission_required("suppliers.add_supplier")
def create_supplier(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Fournisseur créé avec succès")
            return redirect('suppliers-list')

    return render(request, 'suppliers/create.html', {'form': form})

@login_required
@permission_required("suppliers.change_supplier")
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request,"Fournisseur modifié avec succès")
            return redirect('suppliers-list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/create.html', {'form': form})

@login_required
@permission_required("suppliers.delete_supplier")
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request,"Fournisseur supprimé avec succès")
    return redirect('suppliers-list')
