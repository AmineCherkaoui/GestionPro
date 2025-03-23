from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Client
from .forms import ClientForm


@login_required
def clients_list(request):
        search = request.GET.get('search')
        clients = Client.objects.all().order_by("-id")
        if search:
            clients = clients.filter(name__icontains=search)
        paginator = Paginator(clients, 7)
        page_number = request.GET.get('page')
        clients = paginator.get_page(page_number)

        return render(request, 'clients/list.html', {'clients': clients, 'search': search})


@login_required
@permission_required("clients.add_client")
def create_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Client créé avec succès")
            return redirect('clients-list')

    return render(request, 'clients/create.html', {'form': form})

@login_required
@permission_required("clients.change_client")
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request,"Client modifié avec succès")
            return redirect('clients-list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/create.html', {'form': form})

@login_required
@permission_required("clients.delete_client")
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client supprimé avec succès")
    return redirect('clients-list')



