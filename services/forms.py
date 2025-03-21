from django.forms import ModelForm

from services.models import Service


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"