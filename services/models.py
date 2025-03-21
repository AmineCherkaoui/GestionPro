from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(decimal_places=2, max_digits=15,null=False)

    def __str__(self):
        return self.name