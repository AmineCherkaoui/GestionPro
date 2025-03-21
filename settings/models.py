from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models

# Create your models here.
phone_validator=RegexValidator(
    regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
    message="Please enter the right phone number"
)


ice_validator=RegexValidator(
    regex=r'^\d{15}$',
    message="Please enter the right ICE number"
)


rib_validator = RegexValidator(
    regex=r'^\d{24}$',
    message="Please enter the right RIB number"
)



class Settings(models.Model):
    TYPE_DE_SOCIETE_CHOICES = [
        ('SARL', 'Société à Responsabilité Limitée'),
        ('SAS', 'Société Anonyme Simplifiée'),
        ('SA', 'Société Anonyme'),
        ('SNC', 'Société en Nom Collectif'),
        ('SCI', 'Société Civile Immobilière'),
    ]
    name = models.CharField(max_length=255,null=False)

    type_de_societe = models.CharField( max_length=4, choices=TYPE_DE_SOCIETE_CHOICES, null=False  )
    capital = models.DecimalField( max_digits=15, decimal_places=2, null=False,)
    gerant=models.CharField(max_length=255,null=False)
    logo = models.ImageField(upload_to='logos/',blank=True)
    location = models.CharField(max_length=255, null=False)
    ice = models.CharField(max_length=15, null=False, validators=[ice_validator])
    tel = models.CharField(max_length=20, null=False,validators=[phone_validator])
    fax = models.CharField(max_length=20,blank=True, null=True,validators=[phone_validator])
    address = models.TextField(blank=True, null=False)
    bank_name = models.CharField(max_length=255, null=False)
    numero_de_compte=models.CharField(max_length=16, null=False)
    rib = models.CharField(max_length=24, null=False, validators=[rib_validator])
    cnss = models.CharField(max_length=10, null=False)
    patente=models.CharField(max_length=10, null=False)
    IF=models.CharField(max_length=10, null=False)
    RC=models.CharField(max_length=8, null=False)
    hue = models.FloatField(default=220,blank=True, null=False)
    saturation=models.FloatField(default=80,blank=True, null=False)



    def __str__(self):
        return "Settings"
