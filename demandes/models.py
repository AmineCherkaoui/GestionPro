from datetime import date

from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

class DemandeCaution(models.Model):
    TYPE_CAUTION = [
        ('Définitive', 'Définitive'),
        ('Provisoire', 'Provisoire'),
        ('Retenue de garantie', 'Retenue de garantie'),
    ]

    DELAI_EXECUTION = [
        ('1 mois', '1 mois'),
        ('2 mois', '2 mois'),
        ('3 mois', '3 mois'),
        ('4 mois', '4 mois'),
        ('5 mois', '5 mois'),
        ('6 mois', '6 mois'),
        ('7 mois', '7 mois'),
        ('8 mois', '8 mois'),
        ('9 mois', '9 mois'),
        ('10 mois', '10 mois'),
        ('11 mois', '11 mois'),
        ('12 mois', '12 mois'),
    ]

    DELAI_PRONONCIATION = [
    ('12 mois', '12 mois'),
    ('2 ans', '2 ans'),
    ('3 ans', '3 ans'),
    ('4 ans', '4 ans'),
    ('5 ans', '5 ans'),
    ('6 ans', '6 ans'),
    ('7 ans', '7 ans'),
    ('8 ans', '8 ans'),
    ('9 ans', '9 ans'),
    ('10 ans', '10 ans'),
    ]

    type_caution = models.CharField(max_length=20, choices=TYPE_CAUTION)
    numero_marche = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    administration_interessee = models.CharField(max_length=100, verbose_name="Administration intéressée")
    nature_travaux = models.TextField(verbose_name="Nature des travaux")
    numero_marche = models.CharField(max_length=50, verbose_name="Numéro de marché")
    AON = models.CharField(max_length=50, verbose_name="A.O.N")
    delai_execution_marche = models.CharField(max_length=100, verbose_name="Délai d'exécution du marché",choices=DELAI_EXECUTION)
    delai_prononciation_reception = models.CharField(max_length=100, verbose_name="Délai fixe pour la prononciation de la réception définitive",choices=DELAI_PRONONCIATION )
    date = models.DateField(auto_now_add=True)

class DemandeVirement(models.Model):
    titulaire = models.CharField(max_length=50, verbose_name="Titulaire")
    rib = models.CharField(max_length=24, null=False,verbose_name="RIB",validators=[MinLengthValidator(24, 'the rib must contain 24 numbers')])
    montant=models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)

