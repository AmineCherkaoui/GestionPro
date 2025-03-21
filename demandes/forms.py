from django import forms
from .models import DemandeCaution,DemandeVirement

class DemandeCautionForm(forms.ModelForm):
    class Meta:
        model = DemandeCaution
        fields = [
            'type_caution', 'AON','numero_marche', 'montant', 'administration_interessee',
            'nature_travaux', 'delai_execution_marche', 'delai_prononciation_reception'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['AON'].required = False
        self.fields['numero_marche'].required = False
        self.fields['delai_execution_marche'].required = False
        self.fields['delai_prononciation_reception'].required = False



class DemandeVirementForm(forms.ModelForm):
    class Meta:
        model = DemandeVirement
        fields = '__all__'