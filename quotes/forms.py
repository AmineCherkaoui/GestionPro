from django import forms
from .models import QuoteOut, QuoteOutProduct, QuoteOutService
from products.models import Product
from services.models import Service


class QuoteOutForm(forms.ModelForm):
    class Meta:
        model = QuoteOut
        fields = ["date", "client"]
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'placeholder': 'Select a date', 'type': 'date'}
            )
        }
        labels={
            "date":"Date du devis",
        }


class AddProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all().order_by('name'),label="Produit")
    quantity = forms.IntegerField(min_value=1, label="Quantité")

    class Meta:
        model = QuoteOutProduct
        fields = ['product', 'quantity']






class AddServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all().order_by('name'))
    quantity = forms.IntegerField(min_value=1, label="Quantité")

    class Meta:
        model = QuoteOutService
        fields = ['service', 'quantity']

