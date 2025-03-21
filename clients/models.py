from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

# Create your models here.

phone_validator=RegexValidator(
    regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
    message="Please enter the right phone number"
)

ice_validator=RegexValidator(
    regex=r'^\d{1,15}$',
    message="Please enter the right ICE number"
)

class Client(models.Model):
    name=models.CharField(max_length=60)
    address = models.TextField(default="", null=False)
    phone = models.CharField(max_length=15,default="", null=False,validators=[phone_validator])
    ice = models.CharField(max_length=15,default="", null=False,validators=[ice_validator,MinLengthValidator(15, 'the ice must contain 15 numbers')])

    def __str__(self):
        return self.name
