from datetime import date
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from clients.models import Client
from products.models import Product
from services.models import Service

class QuoteOut(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='quotes')
    date = models.DateField(default=date.today)
    products = models.ManyToManyField(Product, blank=True, through="QuoteOutProduct")
    services = models.ManyToManyField(Service, blank=True, through="QuoteOutService")
    is_converted = models.BooleanField(default=False)
    invoice_id=models.IntegerField(default=0,blank=True, null=True)

    @property
    def total_ht(self):
        product_total = self.quote_out_product.aggregate(
            total=models.Sum(models.ExpressionWrapper(
                models.F('price_at_quote') * models.F('quantity'),
                output_field=models.DecimalField()
            ))
        )['total'] or Decimal('0.00')

        service_total = self.quote_out_service.aggregate(
            total=models.Sum(models.ExpressionWrapper(
                models.F('price_at_quote') * models.F('quantity'),
                output_field=models.DecimalField()
            ))
        )['total'] or Decimal('0.00')

        return product_total + service_total

    @property
    def total_tva(self):
        return round(self.total_ht * Decimal("0.2"), 2)

    @property
    def total_ttc(self):
        return round(self.total_ht * Decimal("1.2"), 2)

class QuoteOutProduct(models.Model):
    quote = models.ForeignKey(QuoteOut, on_delete=models.CASCADE, related_name='quote_out_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quote_out_product')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_quote = models.DecimalField(decimal_places=2, max_digits=15,null=False)
    def save(self, *args, **kwargs):
        if not self.price_at_quote:
            self.price_at_quote = self.product.price
        super().save(*args, **kwargs)

class QuoteOutService(models.Model):
    quote = models.ForeignKey(QuoteOut, on_delete=models.CASCADE, related_name='quote_out_service')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='quote_out_service')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_quote = models.DecimalField(decimal_places=2, max_digits=15,null=False)
    def save(self, *args, **kwargs):
        if not self.price_at_quote:
            self.price_at_quote = self.service.price
        super().save(*args, **kwargs)