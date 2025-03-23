from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from settings.forms import SettingsForm

from .models import Settings


# Create your views here.

def settings(request):
    settings = Settings.objects.first()
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request,"Settings modifié avec succès")
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings)
    return  render(request,"settings/index.html",{'form':form})