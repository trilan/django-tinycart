from decimal import Decimal
from django.db import models


class Book(models.Model):

    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('3.50'))
    is_available = models.BooleanField(default=True)
    storage_on_hand = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'tinycart'

    @property
    def is_in_stock(self):
        return self.storage_on_hand > 0


class Shirt(models.Model):

    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('10.00'))

    class Meta:
        app_label = 'tinycart'
