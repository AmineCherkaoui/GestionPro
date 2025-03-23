from django import forms
from .models import PurchaseOrderOut,PurchaseOrderOutProduct,PurchaseOrderOutService
from products.models import Product
from services.models import Service


class PurchaseOrderOutForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderOut
        fields = ["date", "supplier"]
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'placeholder': 'Select a date', 'type': 'date'}
            )
        }

        labels={
            "date":"Date du bon de commande",
            "supplier":"Fournisseur",
        }


class AddProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all().order_by('name'),label="Produit")
    quantity = forms.IntegerField(min_value=1, label="Quantité")

    class Meta:
        model = PurchaseOrderOutProduct
        fields = ['product', 'quantity']





class AddServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all().order_by('name'))
    quantity = forms.IntegerField(min_value=1,label="Quantité")

    class Meta:
        model = PurchaseOrderOutService
        fields = ['service', 'quantity']

