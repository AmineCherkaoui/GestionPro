from datetime import date
from django.core.validators import MinValueValidator
from decimal import Decimal


from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from clients.models import Client
from products.models import Product
from services.models import Service


# Create your models here.

class InvoiceOut(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    products = models.ManyToManyField(Product, blank=True, through="InvoiceOutProduct")
    services = models.ManyToManyField(Service, blank=True, through="InvoiceOutService")

    @property
    def total_ht(self):
        product_total = self.invoice_out_product.aggregate(
            total=models.Sum(models.ExpressionWrapper(
                models.F('price_at_invoice') * models.F('quantity'),
                output_field=models.DecimalField()
            ))
        )['total'] or Decimal('0.00')

        service_total = self.invoice_out_service.aggregate(
            total=models.Sum(models.ExpressionWrapper(
                models.F('price_at_invoice') * models.F('quantity'),
                output_field=models.DecimalField()
            ))
        )['total'] or Decimal('0.00')

        return product_total + service_total

    @property
    def total_tva(self):
        return round(self.total_ht * Decimal("0.2"), 2)
    @property
    def total_ttc(self):
        return round(self.total_ht * Decimal("1.2"),2)
class InvoiceOutProduct(models.Model):
    invoice = models.ForeignKey(InvoiceOut, on_delete=models.CASCADE,related_name='invoice_out_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1 ,validators=[MinValueValidator(1)])
    price_at_invoice = models.DecimalField(decimal_places=2, max_digits=15,null=False)
    def save(self, *args, **kwargs):
        if not self.price_at_invoice:
            self.price_at_invoice = self.product.price
        super().save(*args, **kwargs)

class InvoiceOutService(models.Model):
    invoice = models.ForeignKey(InvoiceOut, on_delete=models.CASCADE,related_name='invoice_out_service')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    price_at_invoice = models.DecimalField(decimal_places=2, max_digits=15,null=False)
    def save(self, *args, **kwargs):
        if not self.price_at_invoice:
            self.price_at_invoice = self.service.price
        super().save(*args, **kwargs)





