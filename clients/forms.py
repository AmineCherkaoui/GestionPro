from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields="__all__"
        labels={
            "name":" Nom du client",
            "address":"Adresse du client",
            "phone":"Téléphone du client",
            "ice":" ICE du client",

        }