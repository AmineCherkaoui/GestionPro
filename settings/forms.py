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
            "type_de_societe":"Type de la société",
            "capital":"Capital social",
            "gerant":" Gérant",
            "location":"Ville",
            "tel":"Téléphone",
            "fax":"FAX",
            "ice":"ICE",
            "bank_name":"Nom de la banque",
            "rib":"RIB",
            "cnss":"CNSS",
            "IF":"Identifiant Fiscale",
            "RC":"Registre de Commerce",
        }