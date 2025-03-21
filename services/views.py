from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ServiceForm
from .models import Service


# Create your views here.
@login_required
def services_list(request):
    search = request.GET.get('search')
    services = Service.objects.all().order_by('-id')
    if search:
        services = services.filter(name__icontains=search)

    paginator = Paginator(services, 7)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    return render(request,"services/list.html",{'services':services,"search":search})

@login_required
@permission_required("services.add_service")
def create_service(request):
    form = ServiceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Service successfully created")
            return redirect("services-list")

    return render(request, 'services/create.html', {'form': form})

@login_required
@permission_required("services.change_service")
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Service successfully updated")
            return redirect("services-list")
    return render(request, 'services/create.html', {'form': form})

@login_required
@permission_required("services.delete_service")
def delete_service(request,service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        service.delete()
        messages.success(request,"Service successfully deleted")
        return redirect("services-list")
    return render(request, 'services/delete.html', {'service': service})
