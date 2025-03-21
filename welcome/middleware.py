from django.shortcuts import redirect
from django.contrib.auth.models import User
from settings.models import Settings

class CheckSettings:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        users_exist = User.objects.exists()
        settings_exist = Settings.objects.exists()
        if (not users_exist or not settings_exist) and not request.path.startswith('/welcome/'):
            return redirect('welcome')
        return self.get_response(request)

class RedirectAuthenticatedUsers:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/login/':
            return redirect('dashboard')
        return self.get_response(request)