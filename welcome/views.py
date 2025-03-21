from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from settings.forms import SettingsForm
from settings.models import Settings



def welcome(request):
    user_exist = User.objects.exists()
    settings_exist = Settings.objects.exists()

    if user_exist and settings_exist:
        if request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('login')

    return render(request, 'welcome/welcome.html')

def create_user(request):
    if User.objects.exists():
        return redirect('welcome-create-settings')

    user_form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('welcome-create-settings')

    return render(request, 'welcome/create-user.html', {
        'user_form': user_form,
    })

def create_settings(request):
    if not User.objects.exists():
        return redirect('welcome-create-user')

    if Settings.objects.exists():
        return redirect('dashboard')


    settings_form = SettingsForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if settings_form.is_valid():
            settings = settings_form.save(commit=False)
            if settings.hue is None:
                settings.hue = Settings._meta.get_field('hue').default
            if settings.saturation is None:
                settings.saturation = Settings._meta.get_field('saturation').default
            settings.save()
            return redirect('login')

    return render(request, 'welcome/create-settings.html', {
        'settings_form': settings_form,
    })
