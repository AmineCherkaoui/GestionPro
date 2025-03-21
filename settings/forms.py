from django import forms

from .models import Settings


class SettingsForm(forms.ModelForm):
    hue = forms.FloatField(required=False)
    saturation = forms.FloatField(required=False)
    fax = forms.CharField(required=False,label='FAX')
    class Meta:
        model = Settings
        fields = "__all__"
        widgets = {
            'hue': forms.HiddenInput(),
            'saturation': forms.HiddenInput()
        }
        labels={
            "name":"Nom de la société  ",
            "type_de_societe":"type de la société",
            "capital":"Le capital social",
            "gerant":" Gérant",
            "location":"Ville",
            "tel":"TEL",
            "fax":"FAX",
            "ice":"ICE",
            "bank_name":"Nom de la banque",
            "rib":"RIB",
            "cnss":"CNSS",
            "IF":"Identifiant Fiscale",
            "RC":"Registre de Commerce",
        }