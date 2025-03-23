from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields="__all__"
        labels={
            "name":" Nom du fournisseur",
            "address":"Adresse du fournisseur",
            "phone":"Téléphone du fournisseur",
            "ice":" ICE du fournisseur",

        }