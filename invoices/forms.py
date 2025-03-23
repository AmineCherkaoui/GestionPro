from django import forms

from .models import InvoiceOut,InvoiceOutProduct,InvoiceOutService
from products.models import Product
from services.models import Service
class InvoiceOutForm(forms.ModelForm):
    class Meta:
        model = InvoiceOut
        fields=["date","client"]
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'placeholder': 'Select a date',
                       'type': 'date'
                })
        }

        labels={
            "date":"Date de la facture",
        }





class AddProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),label="Produit")
    quantity = forms.IntegerField(min_value=1,label="Quantité")
    class Meta:
        model = InvoiceOutProduct
        fields = ['product', 'quantity']





    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if product and quantity:
            if quantity > product.quantity:
                raise forms.ValidationError(
                    f"Only {product.quantity} available in the stock."
                )
        return cleaned_data



class AddServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label="Service")
    quantity = forms.IntegerField(min_value=1, label="Quantité")
    class Meta:
        model = InvoiceOutService
        fields = ['service', 'quantity']

