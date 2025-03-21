from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from datetime import date

from suppliers.models import Supplier
from products.models import Product
from services.models import Service

class PurchaseOrderOut(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,related_name='purchase_order_out')
    date = models.DateField(default=date.today)
    products = models.ManyToManyField(Product, blank=True, through="PurchaseOrderOutProduct")
    services = models.ManyToManyField(Service, blank=True, through="PurchaseOrderOutService")

    @property
    def total_ht(self):
        product_total = self.purchase_order_out_product.aggregate(
            total=models.Sum(models.ExpressionWrapper(
                models.F('price_at_purchase_order') * models.F('quantity'),
                output_field=models.DecimalField()
            ))
        )['total'] or Decimal('0.00')

        service_total = self.purchase_order_out_service.aggregate(
            total=models.Sum(models.ExpressionWrapper(
                models.F('price_at_purchase_order') * models.F('quantity'),
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

class PurchaseOrderOutProduct(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrderOut, on_delete=models.CASCADE, related_name='purchase_order_out_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_order_out_product')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_purchase_order = models.DecimalField(decimal_places=2, max_digits=15,null=False)
    def save(self, *args, **kwargs):
        if not self.price_at_purchase_order:
            self.price_at_purchase_order = self.product.price
        super().save(*args, **kwargs)

class PurchaseOrderOutService(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrderOut, on_delete=models.CASCADE, related_name='purchase_order_out_service')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='purchase_order_out_service')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_purchase_order = models.DecimalField(decimal_places=2, max_digits=15,null=False)
    def save(self, *args, **kwargs):
        if not self.price_at_purchase_order:
            self.price_at_purchase_order = self.service.price
        super().save(*args, **kwargs)