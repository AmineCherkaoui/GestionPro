from settings.models import Settings

def settings_context(request):
    settings = Settings.objects.first()
    return {'settings': settings}