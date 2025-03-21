from django.forms import ModelForm
from .models import Product



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser and user.has_perm('products.change_quantity_only'):
            allowed_fields = ['quantity',"name"]
            for field in list(self.fields):
                if field !="quantity":
                    self.fields[field].disabled=True
                if field not in allowed_fields:
                    del self.fields[field]

